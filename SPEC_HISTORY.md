# SPEC_HISTORY v1.0 — per-spec version history, moved off the execution path

GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, Wave 2 (partial). Framework_PYQCore EC-P42
prices SPECIFICATION-READ COST as a session resource. Every routed spec carried its
entire version history in a comment block at the top of the file, so an EXECUTING
session paid for the complete EDITORIAL record before it could do any work — 283,247 B
across the 23 specs, of which 196,024 B is history of releases that have already
shipped.

THE NARRATIVE IS NOT WASTE AND IS NOT DELETED. The v2.39 record is explicit about why:
five sessions paraphrased the spec and silently repaired bugs; the one session that
executed the fences verbatim found a P0 no other session hit. The defect archaeology is
why this corpus stopped regressing. It is moved, byte-for-byte, into this file — which
is tracked in MANIFEST.json and verified by bootstrap.py exactly as a spec is, and is
routed to NO trigger, so it is never read during execution.

WHAT STAYED BEHIND in each spec: line 1 (the version header bootstrap verifies), the
CURRENT version's entry (Z-VERSION requires the highest changelog entry to equal the
header), and every STRUCTURAL block — MINIMUM COMPANION VERSIONS, step-number notes,
and anything else that is operational rather than historical. Only entries for versions
ALREADY SUPERSEDED were moved.

To read the full history of a spec: find its section below. Entries are verbatim,
newest first, exactly as they appeared in the file.

---

## Framework_Blueprint.md

Entries v1.48.0–v1.63.0 moved at framework release 2026.11.06 (EC-P42; v1.64.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_Blueprint.md.

````
# v1.63.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY G05 + OD-10 (paired with
#   blueprint_core v1.30, MockTestCreate v5.90, MockTestAnalyse v2.59.0, ScopedBlueprint
#   v1.13.0). (1) §7-8 SHAPE TARGETS: blueprint.shape_target_per_paper[mock] =
#   bc.shape_targets(exam shape shares, total_questions, mock index) — FLOOR for every shape
#   with share x Q >= 1, CAP = round(share x Q) + 2 (owner OD-6 c), rare shapes rotated
#   across the series — shares = sum over PYQ subtopics of (r_avg x the subtopic's QUALITY
#   shape_shares) read by bc.quality_block_for_subtopic from section_rules (Step 5 v2.59.0);
#   paper-level (one plan per mock, all sections pooled — Create S3-12d plans per paper). {}
#   (dormant, printed) when fewer than bc.SHAPE_MIN_POOL PYQ items carry a QUALITY block.
#   (2) --refresh (bp_refresh, OD-10 a): with the EXISTING mock blueprint attached, writes
#   ONLY the new fields (shape_target_per_paper, schema_version, producer) for mocks AFTER
#   the last mock registered in the attached registry; every other field is copied
#   byte-for-byte — a series in progress keeps its continuity. (3) blueprint.schema_version
#   = 2. OD-1: nothing in this release stops a run — dormancy is printed and recorded.
# v1.62.0 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY F8 (paired with
#   blueprint_core v1.29, MockTestCreate v5.89, MockTestAnalyse v2.58.0). S7-7 also emits
#   fig_ask_target_per_mock[mock][section] — the exam's own figural ASK-TYPE mix
#   (figure_types.FIGURAL_ASK_TYPES) apportioned over the series by bc.fig_ask_series;
#   {} (dormant) when section_rules carries no figural_ask_type_counts. The difficulty
#   default is UNCHANGED ('+30% harder', positional — owner decision O3 confirmed).
# v1.61.0 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (LAW F1.4;
#   paired with blueprint_core v1.28, figure_types v1.0, Framework_ScopedBlueprint v1.11.0,
#   Framework_MockTestCreate v5.88). §6 decided FORMAT feasibility (can a section carry
#   figural questions?) and never TYPE feasibility (can the dominant figure type of a
#   FIGURAL subtopic be drawn?). A reaction-dominant subtopic therefore reached Step 7 with
#   a dominant type no renderer existed for; the generator's only lawful moves were to
#   mislabel or omit, and every paper audited green. NEW S6-1c KIND-COVERAGE PRE-FLIGHT
#   (bc.kind_coverage_preflight over figure_types.FIGURE_TYPES, run BEFORE the S6-2 flags
#   so a fallback changes the flags too): a dominant type the registry marks UNSUPPORTED
#   HARD STOPs naming subtopic + type unless exam_config.figure_fallback_policy ==
#   'text_disclosed' (the subtopic's format becomes TEXT for the series and
#   blueprint.figural_fallbacks records it for the footer); an UNREGISTERED type is an
#   advisory, never a stop (EC-V18 — ~200 legacy exams keep running). The S6-2 flag
#   derivation is unchanged (it was already correct here; ScopedBlueprint now shares it
#   through bc.derive_presence_flags). blueprint.json gains figure_type_coverage +
#   figural_fallbacks (§14, additive). DoD gains one item.
# v1.60.1 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2; DeliveryFooter v1.35
#   rule R6 / section 9). Delivery site gains the PHASE 1 print of its closed set (S10-1/§3 set unchanged), PHASE 2 echo of the RETURNED paths and PHASE 3 result-built footer. Text only; no set, gate or engine change; never a halt. B1, B2 and B3 sites.
# v1.60.0 — 2026-09-03 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE C: transition allocation; requires Framework_PYQSort v1.21.0 and Framework_PYQCount v1.7 (era fields + n_new must exist)
# v1.59.0 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY: blueprint.json gains the additive
#   `style_profile_expected` flag (§14) so Step 7 can distinguish EC-22 (a profile that
#   vanished after planning) from an exam that never had one; the Axis-2 schedule accepts
#   AXIS2_CLASSES (11). Both additive: zero observations schedule zero, so an exam that
#   observes none of the new classes produces a byte-identical schedule to v1.58.0.
# v1.58.0 — 2026-08-29 — GAP-2026-08-29-DIFFICULTY-HARDER-PRESET + GAP-2026-08-29-PROFILE-
#   UNSCORED-QUESTIONS (paired with blueprint_core Cluster DP — DP_HARDER_FRAC, dp_harder,
#   dp_guardrail_bounds, DP_EXAM_WORD, dp_add_paper paper_positions/unscored, DP_TOLERANCE_FRAC 0.30 → 0.50;
#   PYQExplain v2.20 S7A-6; MockDeliver v1.19.0 §FOOTER-DS; audit_canonical v2.24).
#   Exam-agnostic, zero per-exam change. §7 S7-0: (1) the S7-0 table now shows TWO mixes per
#   section — "Exam (measured)" (the last-3-sittings mix, unchanged arithmetic) and
#   "Ours (+30% harder)" (bc.dp_harder: each band moves 30% of its measured share up to the
#   next band the exam actually sets; a 0% band stays 0; Medium absent → Easy shifts straight
#   to Hard) — every cell carrying BOTH the percentage and the per-mock question count;
#   (2) the DEFAULT on OK is "Ours (+30% harder)" (operator decision 2026-08-29); EXAM accepts
#   the measured mix; the ready-to-edit "[section]: E:M:H" lines are PRINTED for the preset
#   so the operator sees exactly what OK applies; (3) the preset is framework-owned:
#   difficulty_source.mode 'profile_harder', never a CONFIRM prompt; --difficulty harder is
#   the no-prompt form; (4) the guard-rail on TYPED lines widens to ±50% relative (engine
#   constant), still measured against the EXAM mix, 0% still admits only 0; (5) per-sitting
#   rows show "scored/held" (e.g. 58/60) — a question with no derived answer is UNSCORED in
#   the profile (never excludes its paper, never enters the arithmetic) and is listed under
#   the table. Trigger summary line and usage text updated. S7-5 unchanged in shape.
# v1.57.1 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE doc sync (prose only): the header usage
#   line and §15-4 Sheet-4 header rule still described the retired silent 25:25:50 default;
#   exam_config schema now lists the optional cycle_gap_days and states that `level` scales
#   no number. No rule, fence, engine or file change.
# v1.57.0 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with blueprint_core Cluster
#   DP, PYQExplain v2.18 S7A-6, MockTestAnalyse v2.55, MockTestCreate v5.75, MockDeliver
#   v1.17.0, ScopedBlueprint v1.10.0, audit_canonical v2.21). NEW §7 S7-0:
#   the DEFAULT Easy:Medium:Hard split is the exam's OWN measured mix per section, computed
#   from [ExamCode]_difficulty_profile.json (latest 3 sittings by date clustering, equal
#   weight, exact rounding), SHOWN and accepted with OK or replaced line by line; every
#   deviation beyond ±30% (a band the exam never has: any value) needs the word CONFIRM;
#   the silent 25:25:50 default is RETIRED. --difficulty exam / E:M:H / progressive kept,
#   all guard-railed. S7-5 difficulty_schedule[] gains by_section counts (paper totals
#   unchanged for legacy readers); blueprint.json gains difficulty_source (mode, sittings,
#   confirmed overrides) that the delivery footer prints. No profile / dormant → operator
#   types the mix, recorded as operator_no_pyq. Blueprint never re-tunes the engine constants.
# v1.56.0 — 2026-08-25 — GAP-2026-08-25-BLUEPRINT-PHASE1 (paired with blueprint_core
#   CLUSTER P, self-test 527 -> 559; audit_canonical v2.18). One MockBlueprint run halted
#   three times on IIT_JAM_CHEMISTRY; seven defects, all exam-independent. NOTHING IN
#   §4 HALTS ANY MORE — every geometry problem is DERIVED and REPORTED, never handed
#   to the operator. (1) DEF-01 batch_size_qs was a constant (10) standing in for a
#   computed quantity: any mechanism-partitioned exam (MCQ/MSQ/NAT sections that each
#   carry the full taxonomy) breaks it whenever taxonomy > 10 x smallest section. New
#   §4-0 FEASIBILITY PREFLIGHT (B1 Step 5A, after §5 so ZP slots are known) derives the
#   exact minimum window per section (closed form, proven minimal vs brute force) and a
#   three-tier verdict: 1 default holds / 2 window widened, one Assumptions row /
#   3 the section cannot hold every subtopic even once in the whole series -> it keeps
#   the highest-r_avg subtopics it can (bc.capacity_split) and the rest are DECLARED
#   in blueprint.json uncovered_subtopics and guaranteed by the OTHER sections that
#   carry them (coverage promise moves from per-section to per-exam for that section).
#   Silent exclusion remains a BV-0A hard stop; declared exclusion is verified exam-wide
#   (BV-0A Check 4, BV-9B). The EC-11 halt and its unparsed --batch_coverage flag are
#   retired. (2) DEF-02 §4-4 Phase-1 stagger int((k+0.5)N/q)+1 has no subtopic term, so
#   every q=1 rare subtopic computed the SAME mock and the forward-only conflict scan
#   packed them into the tail (mocks 1-10 held ZERO rare Qs) — present since the first
#   commit, masked by a resonance band rare_count ~ [N, 1.3N]; the §4-5 v1.13 offset fix
#   was never back-ported and, measured, does not work here. Replaced by
#   bc.phase1_positions (segment-constrained + rank-spread): F4 89.6->98.2%, F2
#   91.2->99.7%, BV-4 96.3->100%, dead-stretch 53.5->98.9% over 1,792 adversarial
#   shapes. (3) DEF-05 that formula lived in THREE places (§4-4, §9-2 BV-2, §8-4 prose);
#   all three now CALL the engine. (4) DEF-03 BV-7 F2 threshold 1.5*avg was
#   unsatisfiable at integer boundaries -> bc.f2_threshold = max(ceil(avg), 1.5*avg).
#   (5) DEF-04 F2 inspected only the tail -> new F2b no-dead-stretch (WARN; ratchet
#   after corpus replay). (6) DEF-07 BV-9B assumed window == 10-mock B2 batch -> scoped
#   to the coverage window via bc.coverage_window, DEFERRED (never failed) until the
#   window closes. (7) DEF-06 Step 8A ran the auditor self-test from the outputs
#   directory where blueprint_core is absent by design (v2.12.1) -> 253/255; the
#   self-test now runs INSIDE the clone and audit_canonical ABORTS rather than shed
#   fixtures. max_rare_per_mock is derived in §4-3 from the FINAL rare pool (exact, no
#   fixed-point chase with batch_size_qs). §14: batch_size_qs / max_rare_per_mock become
#   REQUIRED+DERIVED (an exam_config value is honoured only if >= the derived minimum);
#   + feasibility_tier, uncovered_subtopics, uncovered_exam_wide. F4 is unchanged (it
#   was never the defect). Subject-partitioned exams derive tier 1 / bs 10 / cap 2 —
#   byte-identical allocation for every exam that never hit the band.
# v1.55.0 — 2026-08-23 — HYGIENE-2026-08-23-STEP6-AUDIT (line-by-line audit closure;
#   no allocation rule, gate, schema, or artefact-shape changes). FIVE fixes:
#   (1) DELIVERY-COUNT-DRIFT, 5th recurrence: §13-7 "All 6 must be present" and
#   AUDIT_SCRIPT_TEMPLATE "Includes all 6 files" still counted the two engines
#   v2.12.1 removed from B3 delivery — both now say 5, and the template's duplicate
#   step "3." is renumbered "4.". (2) The main DoD's final item is renumbered
#   ☐26 -> ☐30 (☐26 was used TWICE: main-DoD "no engine provisioning" vs the
#   DoD-additions "S2-MANIFEST-COMPLETENESS") and its stale "Step 8 copies both"
#   is corrected to Step 7 (Step 8 retired at v1.43.0; §8-5 Step 8B was already
#   correct). (3) CFG PASSTHROUGH — the v1.38 dead-tier rule applied to the four
#   tuning knobs: rare_threshold, max_rare_per_mock, max_per_mechanic_per_mock and
#   batch_size_qs were read via bp.get() with defaults while §4-3 claimed
#   "set rare_threshold in exam_config.json" — a path NOTHING implemented (the
#   exact class v1.38 called "a silently dead fallback tier is worse than no
#   tier"). S2-1 now copies each key VERBATIM from exam_config.json into
#   blueprint.json top level WHEN PRESENT — never a fabricated default — and §14
#   S14-1 declares all four as OPTIONAL. Absent keys leave every bp.get() default
#   and all behaviour byte-identical on every deployed exam. (4) §8-2 Step 7's
#   illustrative blueprint.json key list gains the fields §6/§14 already write
#   (level, medium, marking_scheme, nat_*, difficulty_labels + the optional
#   passthrough note) so the summary can no longer be misread as the schema.
#   (5) §7-7 figural_capacity WRITER NOTE: no Step-5 writer emits max_q_per_mock
#   yet, so capacity is 1 for every subtopic estate-wide (== the safe default)
#   until GAP-2026-08-23-FIGCAPACITY-WRITER lands in MockTestAnalyse; the v1.46
#   plumbing is live and absent-safe. Companion: Framework_MockTestCreate v5.65
#   removes its own dead bp.get('option_label_format') fallback tier (Blueprint
#   writes option_label, documented visibility-only, so that tier could never
#   fire — and its value shape is a label list, not a format template).
# v1.54.0 — 2026-08-23 — GAP-2026-08-23-AXIS-ADVISORY-TRUTH (BV-AXIS gains the
#   AXIS-TRUTH cross-check; paired with blueprint_core axis_truth_check, self-test
#   520 -> 527; companion Framework_ScopedBlueprint v1.9.0). The parent defect was
#   found because a §7-7 advisory contradicted directly observable data — a
#   121-subtopic taxonomy with 66 TEXT / 55 FIGURAL entries reported as containing
#   neither — and NOTHING in the pipeline compared an advisory against the manifest
#   that would falsify it. S9-12 now cross-examines each stored schedule's
#   axis1_unreachable_formats (both contradiction directions) and
#   guarantee_feasibility verdicts against a FIRST-PRINCIPLES recomputation
#   (bc.axis_truth_check — deliberately never via axis1_feasibility /
#   section_axis2_pool_caps, since a checker sharing the audited code path
#   reproduces the audited corruption and passes vacuously) and HARD-FAILS on any
#   contradiction: a corrupted instrument is structural corruption, not a format
#   shortfall, and guards the class — any future defect that corrupts the
#   advisories is caught at the first affected exam's B3 instead of by a human
#   noticing a contradiction. Format shortfalls themselves remain advisory
#   (Subtopic is hard #1), and no_pyq schedules stay SEC-8's territory.
# v1.53.0 — 2026-08-23 — GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE closure (spec
#   mandate + ratchet; no allocation rule, gate, schema, or output changes). §2-1
#   FIX D now states the mandate EXTENDS ACROSS FUNCTION BOUNDARIES: passing an
#   unbridged MANIFEST_IDS to an engine that joins manifest 'section' against a
#   section label is the same violation as writing the raw compare in-spec, with
#   the two sanctioned patterns named — a no-join engine taking pre-resolved ids
#   (bc.axis1_mock_feasibility form; the two v1.49.0-repaired functions now match
#   it), or a bridged per-section local view. Enforcement moves from prose to a
#   build gate: audit_sync gains ENGINE-SECTIONJOIN (AST-level Eq/NotEq detector
#   over every engine .py, section['name'] operand shape included, content-
#   anchored Subject-to-Subject allow-list, 3 subprocess fixtures). Companion:
#   Framework_ScopedBlueprint v1.8.1 corrects §6-3's pre-fix rationale.
# v1.52.0 — 2026-08-22 — STEP6-READ-SET (the S0-3 precedent applied to Step 6;
#   closes SPEC_BUDGET_BASELINE to empty). NEW S0-READSET: NON-FINAL = a B2 batch
#   session (blueprint.json valid, len(mocks) < total_mocks) — it works entirely
#   from blueprint.json state, so it skips the input phase (§2, §3, §6, §7, §10,
#   S2-MANIFEST, S2-MANIFEST-COMPLETENESS) and the closing phase (§12, §13, §15,
#   both DoD sections): ~162 KB, a 44% reduction, verified by forward AND reverse
#   cross-reference sweeps (B2's own steps reference none of them; kept-section
#   references into them are pointer-style, and BV-0A states it RUNS IN B1). §5
#   stays — zp_slot/MAX_ZERO are recomputed from §5-1/§5-2, explicitly not stored.
#   FINAL = B1, B3, malformed, unknown — read everything; escalation mandatory and
#   one-way. Ranges GENERATED (spec_sections.py v4); bootstrap.py --trigger
#   MockBlueprint decides the class from blueprint.json (mocks vs total_mocks).
#   SPEC_BUDGET_BASELINE is now EMPTY and RETIRED with its exemption branch and
#   fixture (audit_specs_ext.py): every route above threshold must carry a read
#   set — there is no exemption left to widen.
# v1.51.2 — 2026-08-22 — GAP-1A-STEP7-UNBOUND-NAMES Release B (one-line binding;
#   no rule changed). EXAM is now bound at the top of the S2-MANIFEST fence with the
#   MockTestCreate S3-1 house idiom (EXAM = "[ExamCode]"  # from trigger). It was
#   read at S2-MANIFEST module scope (manifest_path + the not-found hard stop) and
#   inside resolve_subtopic_id()'s branch-(c) hard-stop message — the latter a
#   guaranteed NameError in a function the spec calls, carried as
#   GRANDFATHERED_MUST_FIX since 2026.08.16.3. Baseline entry deleted (dict +
#   _grandfathered). Companion release: 2026.08.22.4.
# v1.51.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 2 code islands -> tagged fences (load_taxonomy, recency_split); V5 prose to no-paren form; superseded-entry hygiene none.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.51.0 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (paired with
#   MockTestCreate v5.60 / blueprint_core Cluster E2c). S7-3 gains V5: every band's
#   resolved Q counts must be honestly authorable on the exam's shape — the bottom
#   difficulty band is capacity-bound by the shared rubric's MSQ/NAT qtype floors
#   (bc.difficulty_feasibility), while Medium/Hard stay uncapped and the user's
#   ratio remains the law for counts. The (then-)default 25:25:50 path ran the same check
#   [that default is retired since v1.57.0 — S7-0].
#   Errors name the achievable maximum; nothing is silently clamped. Vacuous pass
#   for non-position-typed exams and non-3-band vocabularies (Cluster-E2 contract).
# v1.50.0 — 2026-08-19 — GAP-2026-08-19-LEARNINGS-FILENAME-SEAM (paired with
#   MockTestCreate v5.56). ONE file carried THREE names across the estate: this spec's
#   Step 6 generated [ExamCode]_ExplainLearnings.md; MockTestCreate Step 7 (GAP-07)
#   loaded {EXAM}_ExplainLearnings.md; MockTestExplain/PYQExplain P1 load
#   [ExamCode]_EXPLAIN_LEARNINGS_v*.md via parse_learnings (the S24 frozen schema).
#   CONSEQUENCE, every exam: the Step-6 stub never matched Step 9's glob, so the
#   learnings mechanism the stub exists to seed was dead on arrival — and an exam that
#   adopted the CORRECT versioned name silently lost Step 7's GAP-07 load instead. No
#   auditor covers filename seams (audit_seam tracks JSON fields), so only a human
#   reading both ends could catch it. FIX — one name, one schema, both ends:
#   Step 6 now generates [ExamCode]_EXPLAIN_LEARNINGS_v1.md with an S24-compatible
#   header (S13-5 rewritten); every inventory/delivery/upload list renamed (15 sites).
#   STALE-PROSE also corrected: RS-8 claimed the file is "appended after every Step 4
#   session" and S13-5 claimed "Step 9 fills" — no step writes it (Explain v1.21.0
#   retired the automatic producer, S24-4); it is human-authored, EX-rules accumulate,
#   the _v suffix advances only on an S24 schema change. MockTestCreate v5.56 loads the
#   versioned glob (highest version), keeps its BANNED:/VERIFIED DEFECT: extraction,
#   and prints a one-line migration warning when only a legacy-named file exists.
# v1.49.0 — 2026-08-19 — GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE (engine-side fix,
#   blueprint_core.py; no fence code changes). section_axis2_pool_caps() and
#   axis1_feasibility() RE-filtered their already section-scoped id lists with
#   ``manifest_ids[sid]['section'] == section_name`` — a raw string comparison joining
#   the taxonomy Subject namespace (the manifest 'section' field holds Subject names,
#   e.g. 'Organic Chemistry') against the OTS section-label namespace ('Section A').
#   On any exam whose sections[].subjects maps multiple Subjects into one section the
#   two namespaces never intersect, so the re-filter excluded EVERY id: the Axis-2
#   capability union came back EMPTY (every guarantee-mode class silently reported
#   'unsatisfiable' — shortfall accepted, never generated) and axis1_feasibility's
#   ``avail`` came back EMPTY (every targeted format flagged unreachable, target
#   steered best-effort against a false advisory). Exams with 1:1 section↔Subject
#   configs were unaffected — which is exactly why the defect stayed silent.
#   HISTORY RHYME: spec v1.35 BUG 2 fixed this same namespace join in the fence's own
#   subtopic_in_section() ('==' → list membership via sections_for_subtopic); the two
#   engine-side re-filters were missed then. FIX: the re-filter is REMOVED — the
#   contract (already true at both real call sites: this file's §7-7 fence builds
#   pyq_ids/zp_ids via subtopic_in_section(), ScopedBlueprint passes its scope's own
#   ids) is that id lists arrive PRE-SCOPED; ids absent from manifest_ids are still
#   skipped; signatures unchanged (section_name retained for stability/context).
#   Locked by a 5-fixture regression pack (AXIS-SECTIONKEY-*) proving cross-namespace
#   caps/avail, still-flagged genuine absences, missing-id skip, and the DIRECT
#   default. blueprint_core self-test 490 → 495.
# v1.48.0 — 2026-08-12 — GAP-2026-08-12-AXIS3-MECHLOCK: PYQ-measured axis3 target
#   could directly CONTRADICT the exam's own marking_scheme on any exam that locks a
#   mechanism (question_type) to a fixed Q-range by position (e.g. Q1-30 declared
#   pure MCQ) rather than letting it float by category — the target then named
#   MSQ/NAT counts inside a Q-range that can only ever produce MCQ, a permanent,
#   paper-unfixable A-AXIS3 finding no re-generation could ever clear (root-caused
#   on IIT_JAM_BIOTECHNOLOGY Mock 10's gap analysis §6; the spec's own §7-7 docstring
#   already named this exact failure mode as "masked on exams whose sections are
#   DEFINED per mechanism" without fixing it). bc.derive_axis_schedule now accepts
#   optional marking_scheme + q_range and detects whether this section's Q-range is
#   fully or partially PARTITIONED by single-question_type marking_scheme entries
#   (bc.axis3_mechanism_lock, new); when it is, axis3_target_per_mock is overridden
#   from that position partition — fully (no PYQ blending) or, for a partially-locked
#   section, the locked portion's exact counts plus the PYQ-measured distribution
#   re-apportioned to exactly the remaining gap (never fabricated when there is no
#   PYQ signal for the gap). Conditional, not universal: an exam whose marking_scheme
#   defines marks by CATEGORY has no partition to detect and gets byte-identical
#   pre-v1.48 behaviour — confirmed by a dedicated self-test asserting the omitted-
#   parameters call path is unchanged, and Framework_ScopedBlueprint's own call site
#   (§6-2 of Framework_ScopedBlueprint.md) never passes either new parameter, so
#   scoped tests are completely unaffected. New provenance keys on every section's
#   axis_schedule entry: axis3_target_source ('pyq_measured' / 'mechanism_lock_full'
#   / 'mechanism_lock_partial') and axis3_mechanism_lock (the full detection result)
#   — additive only, BV-AXIS's (S9-12) REQUIRED-key check is a subset check, never a
#   no-extra-keys check, so this cannot regress it; the §14 AXIS-SUM contract BV-AXIS
#   enforces downstream is defensively re-asserted at the source in blueprint_core.py
#   itself. S7-7's call site (below) threads blueprint['marking_scheme'] and this
#   section's own q_range through. blueprint_core.py self-test: 365/365 -> 377/377
#   (12 new fixtures, including the exact Mock-10 wrong-distribution scenario from
#   the gap analysis, mutation-verified: neutering the override makes the new tests
#   fail/crash, confirming they are load-bearing, not decorative).
````

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_Blueprint.md.

```
# v1.47.0 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v1.46.0 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v1.45.0 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: the exemption became the budget.
#   v2.26 replaced `has_img = any(...)` with a rate and then decided REDUCIBILITY
#   with a fresh any(). One question in a 22-year corpus made a subtopic permanently
#   exempt, and irreducible grants pass even over budget by design. First real
#   PYQExtract run: 21 of 133 subtopics exempt, 14.3 figures/mock against a budget
#   of 5, 13 of 15 mocks over. Reducibility is now rate-based (figural_rate >= 0.50
#   AND option_image_rate >= 0.50) -> 3 subtopics, 1.5 forced, 0 mocks over.
#   Figures are now SCHEDULED at measured frequency rather than forced at render
#   time, the audit band is the exam's own volatility, and per-mock targets follow
#   the exam's observed shape. No feasibility halt exists or is needed.
# v1.44.0 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v1.43.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   B3's deliverable set drops from 6 files to 5: [ExamCode]_ExplainAuditLearnings.md is
#   NO LONGER GENERATED (§13-6), because its only filler — canonical Step 10 — is retired.
#   An ExplainAuditLearnings file already accumulated in an exam project STAYS VALID and is
#   still loaded and obeyed by Step 9; never delete one.
#   §13-7A is KEPT IN FULL: audit_canonical.py remains the single canonical auditor and B3
#   still copies it verbatim to [ExamCode]_mock_test_audit.py. What changed is who runs it —
#   Step 7 only, and optionally, which means an absent audit.py now leaves the paper with no
#   machine gate at any step. Every "audited within tolerance at Step 8" advisory in this
#   file is restated as "audited within tolerance by Step 7's audit.py"; the engine copy
#   duty (blueprint_core.py + figural_core.py from $FW) moves from Step 8 to Step 7.
#   EDITOR CAUTION added at the internal/canonical step map: this file uses "Step 8" for its
#   own B3 sub-steps as well, and those must never be mass-replaced.
#
# v1.42.8 — 2026-08-02 — self-test count refresh only (107/107 -> 139/139).
#   The five LIVE normative sites still quoted "the v2.13 canonical build prints
#   107/107" as the expected auditor count. That was stale twice over (the canonical
#   is v2.21.7 at 139/139) and misattributed the version. Historical changelog lines
#   below are left EXACTLY as written — they record what was true at their release
#   and are not restated. AUTH_GATE_FLOOR stays 35: the count is informational, the
#   floor is the binding condition, and that is now stated at each site so the next
#   count change does not require another sweep.
# v1.42.7 — 2026-08-01 — self-test count refresh only (105/105 -> 107/107).
# v1.42.6 — 2026-08-01 — self-test count refresh only (97/97 -> 107/107).
# v1.42.5 — 2026-08-01 — self-test count refresh only (89/89 -> 107/107, D2+D4 vision
#   fixtures). AUTH_GATE_FLOOR unchanged at 35.
# v1.42.4 — 2026-08-01 — self-test count refresh only (78/78 -> 107/107, C1
#   checkpoint fixtures). AUTH_GATE_FLOOR unchanged at 35.
# v1.42.3 — 2026-08-01 — SELF-TEST COUNT REFRESH ONLY (documentation; zero rule
#   change). audit_canonical.py gained five C5 fact-record fixtures at
#   Framework_MockTestCreateAudit v2.14 (B3), so every §13-7A site stating the
#   expected fixture-based count moves 73/73 -> 107/107. AUTH_GATE_FLOOR stays at
#   35 — the floor gates DEPLOYED copies, and raising it would HARD STOP every
#   un-refreshed exam.
# v1.42.2 — 2026-08-01 — SELF-TEST COUNT REFRESH ONLY (documentation; zero rule
#   change). The canonical auditor B3 ships (audit_canonical.py) gained eleven
#   fixtures at Framework_MockTestCreateAudit v2.13
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT), so every §13-7A site that states the
#   expected fixture-based count moves 61/61 -> 107/107. AUTH_GATE_FLOOR is
#   UNCHANGED at 35 and is deliberately NOT raised: the floor gates the deployed
#   copies, and raising it above their printed count would HARD STOP every
#   un-refreshed exam. A v2.11 copy (51/51), a v2.12 copy (61/61) and a v2.13
#   copy (107/107) all pass the floor, so the estate migrates exam by exam with
#   zero downtime. B3 cardinality (6) and every generation rule are untouched.
# v1.42.1 — 2026-08-01 — B3 STAYS AT 6 OUTPUTS; NO ENGINE PROVISIONING
#   (post-deploy correction). v1.42 raised B3 to 8 by shipping blueprint_core.py +
#   figural_core.py per exam. Wrong remedy: CLAUDE.md states engines live ONLY in
#   the central repo and no per-project provisioning should ever be performed,
#   because a project copy is a second unverified source that can go stale. Step 8
#   P0 now copies both engines from the Step-0 verified clone ($FW) instead — the
#   same pattern §S1-2b already uses for blueprint_core — so the B3 contract
#   returns to 6 and no exam project needs touching. Superseded v1.42 entry:
# v1.42 — 2026-08-01 — B3 SHIPS THE RUNTIME ENGINES (8 outputs, was 6)
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D2/D3). The canonical auditor delegates
#   A-FIGPROFILE to blueprint_core and the 12 A-FIG* gates to figural_core, but
#   NEITHER engine was ever copied into an exam project — not in the B3 output set,
#   not in project knowledge, not named as a Step-8 input anywhere. B3 now copies
#   both VERBATIM under their BARE names (a [ExamCode]_ prefix breaks the module
#   import and silently disables the gates). Also corrected here: the B3 checklist
#   still asserted "--self-test passed (13/13 PASS)", a stale reference to the
#   RETIRED hollow MVP; it now asserts a FIXTURE-BASED N/N with N >= 35.
# v1.41.2 — 2026-07-31 — §13-7A COPY SOURCE now audit_canonical.py (repo engine); the
#   canonical auditor no longer requires opening Framework_MockTestCreateAudit.md
#   mid-session. Behaviour identical (byte-identical script).
# v1.41.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   825 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_Blueprint'. The current companion block, the
#   v1.41 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.41 — 2026-07-26 — S2-2 LOADS THROUGH load_taxonomy(). Read and gate collapse to
#         one call, and the taxonomy comes from approval_record.json where the record
#         carries it rather than from a Word document. Step 6 is the worst place for a
#         wrong taxonomy — the blueprint built from one is internally consistent,
#         passes every BV check and is indistinguishable from a correct one at Steps
#         7-11 — so removing the parse step here removes the largest remaining way to
#         get one. Pre-1.3 records fall back to the doc, gated, and need no re-run.
#         MINIMUM COMPANION: corpus_io.py >= v1.4.
#
```

## Framework_DeliveryFooter.md

Entries v1.27–v1.40.0 moved at framework releases 2026.11.06 and 2026.11.07 (EC-P42; v1.41.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — this file rides on every route, so every header byte is paid by every session).
Current-version entry remains in Framework_DeliveryFooter.md.

```
# v1.40.0 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY Part D (owner decisions D3-R5 (a),
#   D10 (B); paired with blueprint_core v1.32, paper_pipeline v5.40, MockTestCreate v5.92,
#   MockTestExplain v1.53.0, MockDeliver v1.26.0). §FOOTER-FT ONLY gains the DIFFICULTY
#   DISCLOSURE LINES — every string bc.difficulty_unverified_lines returns ("DIFFICULTY
#   UNVERIFIED — <reason>", "Hard target missed: k item(s)", "Step 9: k/n assessed", the
#   small-pool and coverage lines), engine-sourced, prefixed "⚠️ ", disclosure only (no
#   verdict change, no certification effect, no stop); pp.dg_footer_lines adds the Step-9
#   coverage line for a w2 record. §1, §2, §4-§7 and the §3 STEP 1 block are byte-identical
#   (PYQPrepare freeze, owner P1).
# v1.39.0 — 2026-11-04 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE (owner decisions D0, D2 (a),
#   D3 (a), D5 (a), D6; paired with MockTestCreate v5.91, MockReview v2.0.0, MockDeliver
#   v1.25.0, audit_canonical v2.36, final_assembly v1.13, STEP_CONTRACTS.json). STEP 7 FINAL
#   DELIVERABLES are EXACTLY two files again — [ExamCode]_[slug]_Create.docx +
#   [ExamCode]_registry.json — and NEXT STEP is Step 9. The v1.38.0 AWAITING_REVIEW end, the
#   review packet deliverable and the whole STEP 7R block are RETIRED (the review runs inside
#   Step 7; the MockReview / TestReview triggers no longer exist). The v1.37.0 conditional
#   third / fourth files (in-run blueprint, repo auditor copy) are RETIRED: one
#   INFORMATIONAL line each. §LADDER gains the INFORMATIONAL independent-review line and the
#   Step 11 re-certification line.
# v1.38.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (paired with
#   MockTestCreate v5.90, MockDeliver v1.24.0, MockReview v1.0.0, audit_canonical v2.35).
#   §LADDER gains the QUALITY disclosure lines: the DEGRADED QUALITY line
#   (bc.degraded_footer_line — OD-1: dormant controls listed, nothing stopped), the
#   NOT CERTIFIED line with uncertified_items (OD-9), the AWAITING_REVIEW / review-round
#   lines (OD-5), the shape-plan infeasibility line (OD-6) and the bench-card pointer.
# v1.37.0 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (paired with
#   MockTestCreate v5.89, audit_canonical v2.34, final_assembly v1.11). NEW §LADDER —
#   the repair-ladder and drawing/level disclosure lines for Step 7 (terminal-rung items,
#   systemic flags, schedule/allocation amendments, style defaults, renderer degraded,
#   level control dormant, difficulty schedule unverified, upload blueprint / auditor).
#   §5 Q0: an AMBER advisory is now a WARN line in the auditor (no exit 1) and forces
#   F1 through the S13-2F certificate's amber_notes, never through the exit code. §3
#   STEP 7 final set: two CONDITIONAL additions (in-run blueprint when it differs from
#   the project copy; the per-exam auditor when the run audited with the repo copy).
# v1.36.0 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (paired with
#   paper_pipeline v5.40, final_assembly v1.10, MockTestCreate v5.88, MockDeliver v1.23.0).
#   NEW §FOOTER-FT — FIGURE-RECORD DISCLOSURE LINES, engine-sourced from
#   pp.figure_footer_lines(reg, bp, paper_id): a text_disclosed fallback subtopic, a
#   committed record whose blueprint flag said otherwise (registry.paper_flags), a legacy
#   paper whose figures were never recorded (absent_legacy — NOT AUDITED), legacy figure
#   records annotated by the migration (label mismatch / degenerate reaction), and
#   unregistered dominant figure types. A clean current paper prints nothing — the legacy
#   estate's footers are byte-identical (§7 P1). A healed or annotated registry must never
#   look identical to a clean one (§FOOTER-DG precedent). No other set, gate or badge change.
# v1.35.1 — 2026-09-21 — GAP-2026-09-21-LINKED-PLACEMENT (paired with MockTestAnalyse
#   v2.57.2, MockTestCreate v5.85). Step 5 final set gains [ExamCode]_stimulus_profile.json
#   (MANDATORY, badge "Upload to Project Files" — Step 7 stops at a new paper without it):
#   8 mandatory + 2 conditional. NEW Step 5 mode `PYQExtract --stimulus-profile` delivers
#   that one file only. No other set, gate or engine change.
# v1.35 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2). §9 now carries
#   the CANONICAL print_delivery_set fence (byte-identical to the PYQScan / PYQExplain /
#   MockTestAnalyse copies) so the fourteen prose-only delivery sites — Steps 1, 2a, 2c, 3,
#   4, 6, 6S, PYQ-3, PYQ-4, L2, NB, NC, NA, ND — can name it without each carrying a copy;
#   STEP COVERAGE updated to "every step". Sets unchanged; no gate, no engine, no halt.
# v1.34 — 2026-09-14 — GAP-2026-09-14-DELIVERY-ECHO (owner decision 2026-09-14; paired
#   with PYQExplain v2.24, MockTestAnalyse v2.57.1, PYQScan v1.6.1). Reference incident:
#   PYQExplain final batch shipped ONLY the Explanation docx and left
#   pyq_explain_progress.json + difficulty_profile.json unattached, while the F2 footer
#   listed all three. Root cause is structural, not per-step: present_files is a
#   CLASS T stub (`pass`) — the model performs the real call from what it REMEMBERS,
#   and nothing ever read the call's RESULT. NEW §4-0 R6 + §9 DELIVERY-ECHO: (1) the
#   closed set is printed in the tool output immediately before the call, EVERY batch;
#   (2) after the call the RETURNED paths are compared to that set; any missing file
#   is re-presented at once; (3) footer rows and the F2 header count come ONLY from
#   returned paths. NEVER a halt (owner decision): a file absent on disk is delivered as
#   a named ❌ row, not silently dropped, not a stop. §3 registry drift fixed in the same
#   release: Step 5 FINAL now lists the v2.56 style_profile.json + pyq_index.json (7
#   mandatory + 2 conditional, matching MockTestAnalyse S11-3), and the PYQ EXPLANATION
#   TRACK (PYQ-1 / PYQ-3 / PYQ-4 / L2) gains its registry block — it had none.
# v1.33 — 2026-09-14 — GAP-2026-09-14-REGISTRY-SOURCE (REGISTRY-SOURCE-LAW; owner decision
#   2026-09-14; paired with MockTestCreate v5.84, MockTestExplain v1.51.0, MockDeliver
#   v1.22.0, paper_pipeline CLUSTER RS). The "Replace in Project Files" badge on
#   [ExamCode]_registry.json is UNCHANGED (MS-14 greps it verbatim), but what the operator
#   may DO with the delivered file gains a second lawful option: attach it to the next
#   step's trigger instead of replacing it in Project Files (an attachment wins over the
#   Files copy). §8 now states both lanes; the §3 STEP 7 / STEP 9 / STEP 11 blocks and
#   BADGE 2 carry a one-line note. pp.handoff_set's operator line already says it.
# v1.32 — 2026-09-03 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE C: §5.9 active transition lines wired
# v1.31 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE A: NEW
#   §FOOTER-SYL — the syllabus-declaration disclosure line. Every footer (F1 and F2)
#   of an exam whose exam_config.syllabus_transition block records a TRACED-INACTIVE
#   declaration (T1 rows 4/5/7) prints EVERY string returned by
#   bc.syllabus_footer_lines(st), one per line, prefixed "ℹ️ " — Release A set:
#   "Syllabus declaration present but inactive: <reason>". The engine is the ONLY
#   source; keys-absent and silently-inactive exams print NOTHING (§7 P1 / R25). The
#   ACTIVE-mode §5.9 lines (n_new blend label, coverage, style donors) ship with
#   Release C. R15/R19: this footer is the ONLY disclosure surface — nothing on
#   questions, options, or student-visible layout, ever.
# v1.30 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY: §FOOTER-STYLE defines the single style-profile status line
#   (ACTIVE with schema + corpus hash8, or DORMANT with a reason). pp.style_footer_line is
#   its ONLY source; the engine drops unknown keys, so a richer record cannot widen the
#   footer.
# v1.29 — 2026-08-27 — REPAIR-RETIRED-2026-08-27 (operator decision; paired with
#   paper_pipeline v5.76, MockTestCreate v5.76, MockTestExplain v1.47.0, MockDeliver
#   v1.18.0). The four *Repair triggers are RETIRED: §3 blocks STEP 7-R and STEP 9-R are
#   DELETED, §5 flow drops the repair lines (after Step 9 → Step 11 ALWAYS; the gate
#   discloses, it never blocks), §8 writer list is Step 7 / Step 9, the two
#   _Create_Repaired* patterns leave LOCAL_ONLY (no step produces them; a stray one is
#   an unexpected file). §FOOTER-DG gains the DISCLOSED/0 line ("the difficulty gate was
#   not met; labels are as planned at Step 7") and marks DISCLOSED/1 as a legacy repair.
# v1.28 — 2026-08-26 — GAP-2026-08-26-REPAIR-BATCH-LAW (MockTestCreate v5.74): STEP 7-R
#   batched — F1 per non-final batch with _Create_Repaired_PARTIAL_[k]of[K].docx
#   (registry withheld), F2 at the final batch. LOCAL_ONLY gains the PARTIAL pattern.
# v1.27 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (MockTestCreate v5.73,
#   MockTestExplain v1.46.0, MockDeliver v1.16.0, paper_pipeline v5.74). NEW §8
#   REGISTRY-HANDOFF-LAW; §3 Step 7 drops the dossier, Step 9 final delivers registry
#   (Replace) + Explain_Report.docx, NEW STEP 7-R / 9-R, Step 11 delivers a healed
#   registry; §6 repair path. Full text: SPEC_HISTORY.md.
```

Full v1.27 entry (header carries the short form since v1.28 — SPEC-BUDGET on the PYQPrepare route):

```
# v1.27 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestCreate
#   v5.73, MockTestExplain v1.46.0, MockDeliver v1.16.0, paper_pipeline v5.74 Cluster RH,
#   explain_engine v2.9, final_assembly v5.60). NEW §8 REGISTRY-HANDOFF-LAW: a step that
#   CHANGES registry.json DELIVERS it (Replace); badge lines are
#   pp.handoff_footer_lines(HANDOFF) verbatim. §3: Step 7 no longer delivers the audit
#   dossier (internal); Step 9 final delivers registry.json (Replace) +
#   [ExamCode]_[slug]_Explain_Report.docx (the old "registry not delivered" note was wrong
#   since MockTestExplain v1.42.0); NEW blocks STEP 7-R and STEP 9-R; Step 11 delivers a
#   healed registry. §6 gains the repair path. LOCAL_ONLY gains '*_Explain_Report.docx' and
#   '*_Create_Repaired.docx'.
```

Entries v1.24–v1.26 moved at framework release 2026.08.26.3 (EC-P42; v1.27 supersedes;
the PYQPrepare route's pre-work read crossed the SPEC-BUDGET threshold).

```
# v1.26 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS (paper_pipeline v5.72,
#   MockDeliver v1.15.0, MockTestExplain v1.45.0). Prose only. §FOOTER-DG DISCLOSED
#   example shows the windowed shape ("(not gated)" / "in window").
# v1.25 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with
#   paper_pipeline v5.71 Cluster DG, MockDeliver v1.14.0, MockTestExplain v1.44.0).
#   MINOR bump: registry/prose only, NO badge changes, NO artefact changes.
#   * §3 STEP 11 gains §FOOTER-DG, which MockDeliver v1.13.0 referenced but no spec
#     defined: the difficulty-gate disclosure lines are pp.dg_footer_lines(rec) —
#     the measured-band line on DISCLOSED, the not-applicable line on DORMANT, and
#     one healed-registry line per rec['migrations'] entry — so a corrected record
#     is always disclosed in the delivered footer and never composed by hand.
#   Superseded v1.23 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
# v1.24 — 2026-08-24 — GAP-2026-08-24-STEP9-AUDIT-R2: SCOPED-PAPER NEXT-STEP + 6S REGISTRY.
#   MINOR bump: registry/prose only, NO logic changes, NO badge changes, NO artefact
#   changes. Release 2 of the Step-9 audit (R1 = 2026.08.24.1).
#   * §3 STEP 7 / 9 / 11, §4-1 Step-11 variant and §6 named ONLY the mock triggers
#     (MockCreate M / MockExplain M / MockDeliver M) and "Mock [N]". A scoped paper
#     (ScopedBlueprint → TestCreate P[N] → TestExplain P[N] → TestDeliver P[N]) got a
#     footer pointing at a trigger whose --level mock alias would HARD STOP on its
#     scoped docx (MockTestExplain S2-1 / MockDeliver S1-2 slug gates). Every next-step
#     line now names both forms; "Mock [N]" → "[paper_slug]".
#   * §3 had NO entry for Step 6S (ScopedBlueprint), which rides this file on its route
#     and had no deliverable/badge/next-step registry to follow. Added.
#   Superseded v1.22 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
```

Entry v1.23 moved at framework release 2026.08.25.3 (EC-P42; v1.25 supersedes).

```
# v1.23 — 2026-08-23 — REGISTRY SYNC (Step 6 learnings filename; Step 5 tiers).
#   MINOR bump: registry/prose only, NO logic changes, NO artefact changes beyond
#   the filename the Step 6 footer badge table prints.
#   * §3 STEP 6 B3 still listed [ExamCode]_ExplainLearnings.md; Blueprint v1.50.0
#     generates [ExamCode]_EXPLAIN_LEARNINGS_v1.md, because the legacy name
#     matched NO consumer's glob (Steps 7 and 9 load *_EXPLAIN_LEARNINGS_v*.md).
#     The registry now names the file Step 6 actually emits — a footer that
#     badges a filename no step produces sends the operator hunting for it.
#   * §3 STEP 5 FINAL heading said "6 mandatory + taxonomy.xlsx when written",
#     counting exam_config.json as mandatory while its own list line says
#     "delivered only when generated". Restated as the two-tier set that
#     MockTestAnalyse S11-3 and mock_sync_audit MS-11 enforce: 5 mandatory +
#     2 conditional. Fourth recurrence of the delivery-count-drift class; this
#     was the last site still carrying a fixed count.
```

Entry v1.22 moved at framework release 2026.08.24.2 (EC-P42; v1.24 supersedes).

```
# v1.22 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: adds a CLASS: T stub for present_files(). NO ARTEFACT CHANGES.
#   present_files() was CALLED from compiling python here while DEFINED nowhere — a
#   guaranteed NameError; spec_name_audit_baseline.json had accepted it as
#   known-unbound in all four affected specs, so the ratchet reported OK.
#   FULL NARRATIVE: SPEC_HISTORY.md + CHANGELOG.md 2026.08.16.2.
```

Moved from the file header at framework release 2026.08.15.14; entry v1.21
at framework release 2026.08.20.9 — this file rides on ALL 23 routes, so
every byte in its header is paid by every session of every step.
Current-version entry remains in Framework_DeliveryFooter.md.

```
# v1.21 — 2026-08-13 — SYNC AUDIT ROUND 2: footer registry caught up with the steps.
#   (1) GAP-2026-08-13-DELIVERY-COUNT-DRIFT (mirrored): §3's Step-5 final list said "5
#   files" — no badge for exam_config.json (mandatory-when-generated since MockTestAnalyse
#   v2.24.9) and none for taxonomy.xlsx (v2.24), which therefore fell through to an Upload
#   badge for an xlsx this spec itself marks unreadable. List now matches S11-3's derived
#   set. (2) GAP-2026-08-13-FOOTER-SCOPED-PATTERNS: §2 LOCAL_ONLY only knew Mock*_ name
#   forms; scoped papers ({EXAM}_SUBJ_*/TOPIC_*/SUBTOPIC_* slugs) fell through to
#   Upload/Replace. Added slug-agnostic suffix patterns (*_Create.docx, *_Explanation.docx,
#   *_Final.docx, *_Q1to*.docx, *_audit_dossier.json, *_taxonomy.xlsx).
# MockTestFramework | Cross-step | Exam-agnostic
#
# PURPOSE:
#   Define the visual delivery footer that Claude renders after every
#   present_files call in the 11-step pipeline. Two footer types exist:
#   mid-step (amber) and step-complete (green). This file is the single
#   source of truth — all spec files reference it instead of embedding
#   their own footer logic.
#
# SCOPE:
#   Steps 1–11 (all pipeline steps, all exams, all projects).
#   This file is uploaded to the MockTestFramework project AND to each
#   [ExamCode] project so it is available in project knowledge everywhere.
#
# REFERENCED BY:
#   Every Framework_*.md file's delivery section references this spec:
#   "Follow Framework_DeliveryFooter.md for post-delivery footer rendering."
#
# VERSION HISTORY:
#
# v1.20 — 2026-08-12 — NOTES HANDOFF BY ATTACHMENT (GAP-2026-08-12-NADOCX P2;
#   pairs with Framework_NotesAudit v3.0.0 / NotesCreate v2.3.0 / NotesDeliver
#   v1.2.0). The section 3 NC/NA/ND entries change: the notes .docx now moves
#   between steps as a CHAT ATTACHMENT, not through Project Files, so its badge
#   is "Use locally" at every step and the Next callout says to attach it. Only
#   notes_registry.json is still filed — every step reads it from there, and it
#   now carries draft_ref, final_ref and audit_summary (notes-registry/2.1).
#   [ExamCode]_<unit>_Audit.md is REMOVED from ND's and NA's deliverable lists:
#   NA no longer writes one. Filenames are the three engine authorities
#   (notes_filename / notes_final_filename / notes_deliver_filename). The
#   4-cell NOTES bar and every rendering rule are UNCHANGED — ND survives, so
#   the pipeline is still 4 steps.
# v1.19 — 2026-08-10 — NOTES CROSS-CHAT HANDOFF (supersedes v1.18's "NC/NA
#   present nothing"). v1.18 marked NC and NA intermediate, which only holds if
#   all four Notes steps run in ONE session — but the framework idiom is a new
#   chat per step, so NC's draft .docx and NA's audited .docx must persist across
#   chats exactly like NB's bank. NC and NA now PRESENT their handoff artifacts
#   (draft / audited .docx + audit report + the updated registry) and render a
#   footer, so their §6 next-step line actually prints. §3 NC/NA entries rewritten
#   (F2, deliverables, Upload to Project Files); the §4-4 NOTES bar now applies to
#   all four Notes F2 footers (NB=1, NC=2, NA=3, ND=4). Also: notes_pyq_bank.json
#   is NAMED in the get_badge context-dependent note (its mid-batch checkpoint is
#   Upload/Replace for a fresh-chat resume, Use locally for an in-session
#   continue), resolving the §3-vs-get_badge disagreement. Additive to Step 1-11.
# v1.18 — 2026-08-10 — NOTES PIPELINE INTEGRATED. The Notes pipeline
#   (NB/NC/NA/ND) routes this footer but had ZERO §3 registry entries and no
#   pipeline bar, so once NB began calling present_files (NB v2.0.4) it owed a
#   footer it could not render. Added: §3 entries for NB/NC/NA/ND (NB and ND
#   deliver + render a footer; NC/NA are intermediate and present no files, so
#   render none — the contract binds only a present_files call); a 4-cell NOTES
#   PIPELINE BAR in §4-4 for Notes F2 footers (the 11-cell Mock/PYQ bar never
#   applies to Notes); and the Notes chain in §6. Additive only — no Step 1-11
#   entry, badge, severity, F1/F2 shape, or §5 flowchart changed.
# v1.17 — 2026-08-10 — LOCAL_ONLY PATTERN MADE AIRTIGHT. v1.16 added
#   '*_pyq_registry.json', but get_badge() matches via endswith(pat) / fnmatch(*pat),
#   so a BARE 'pyq_registry.json' with no '[ExamCode]_' prefix did NOT match and fell
#   through to the upload/replace branch — the v1.16 "never routed to Project Files"
#   guarantee was narrower than stated (the spec always names the file with a prefix,
#   so it was not reachable in practice, but the guarantee should be exact). FIX: the
#   pattern is now '*pyq_registry.json' (underscore dropped), which matches BOTH the
#   prefixed and bare forms while still excluding the mock '_registry.json',
#   'blueprint.json', and unrelated files (verified: zero false positives). Surfaced in
#   the 2026.08.10.1 deployment review. Badge-only; no severity/F1/F2/flowchart change.
# v1.16 — 2026-08-10 — PYQ REGISTRY IS LOCAL-ONLY (structural badge guarantee).
#   Added '*_pyq_registry.json' to the §2 LOCAL_ONLY set so get_badge() can NEVER
#   route the PYQ corpus tracker to Project Files on any step, for any exam — it
#   always badges 📁 Use locally. Pairs with Framework_PYQDeliver v1.10, which demotes
#   the registry from a required Project-Files deliverable to an OPTIONAL, absence-
#   tolerant, local-only continuity aid (closing the silent cross-session reset that
#   the routinely-skipped manual upload caused across the ~200-exam corpus). BADGE
#   ONLY — no severity routing, no F1/F2 change, no §5 flowchart change; no condition
#   may halt a run, and that is untouched.
# v1.15 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. Updated the PYQ VOID_ITEM /
#   CERTIFIED-DEGRADED (VISION) wording that named PYQ-2 as the reader of the voided-
#   question list (now the human reviewer), and the v1.13 note that called PYQExplainAudit
#   a still-live step (it is now also retired). F1/F2 shape, Q0/Q0b, severity unchanged.
# v1.14 — 2026-08-03 — NEW §2A SPEC PROVENANCE DISCLOSURE (project-first specs).
#   Specs are now PROJECT-FIRST: a Framework_*.md in an exam project's Files section
#   overrides the repo copy and CANNOT be byte-verified. Every footer must now state
#   whether the run used repo-verified specs or project overrides, naming them.
#   DISCLOSURE ONLY — no severity routing, no AMBER/VOID_ITEM/BLOCKING change, no F1/F2
#   change, no §5 flowchart change. No condition may halt a run, and that is untouched.
#
# v1.13 — 2026-08-03 — DEFECT FIX: this file still routed operators to the RETIRED steps.
#   2026.08.03.5 retired canonical Steps 8 and 10 but left §2's step registry intact, so
#   every Step 7 footer printed "NEXT STEP: Step 8: MockCreateAudit M[N]" and every Step 9
#   footer printed "NEXT STEP: Step 10: MockExplainAudit M[N]" — triggers that no longer
#   resolve. This file is routed to ALL triggers, so the defect printed on every delivery.
#   FIXED: the STEP 8 and STEP 10 template blocks are removed, Step 7 -> Step 9 -> Step 11
#   is the printed chain, and the §7 chain map matches. The pipeline bar STAYS at 11 cells.
#   The three retired filenames stay in LOCAL_ONLY so pre-retirement files on disk badge
#   correctly. ZERO CHANGE to §5 Q0b, to the v1.12 PYQ-1 VOID_ITEM producer clause, to any
#   severity routing, or to F1/F2 shape: no colour or vision condition may halt a run.
#
# v1.12 — 2026-08-03 — §5 Q0b GAINS A SECOND PRODUCER: PYQExplain §13A VOID_ITEM.
#   Q0b already fires on a MEASURED vision outage in the mock pipeline. PYQ-1 can
#   now measure the same condition (Framework_PYQExplain v1.2 §13A-5) and had no
#   amber path, so it HALTED instead — the one place the corpus rule 'a CLASS T
#   failure must be LOUD and must NOT halt' (CLAUDE.md) was not applied. Same
#   measured condition, same AMBER, one more producer. The PYQ wording NAMES the
#   voided questions, because an unexplained question that is not named reads as
#   an oversight and the human reviewer must be told where to look (PYQExplain RE-20).
#   Zero change to F1/F2 shape, to Q0, to Q1, or to any severity routing:
#   no colour or vision condition may halt a run, and that stays untouched.
#
# v1.11 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   B3 final deliverables drop 6 -> 5 (ExplainAuditLearnings.md is no longer generated);
#   the engine-copy duty moves from Step 8 to Step 7. The former audit-rule cross-reference
#   is inlined because the spec that defined it no longer exists. No footer rule, severity, or
#   AMBER/VOID_ITEM/BLOCKING routing changes: no colour condition may halt a run, and
#   that is untouched here.
#
# v1.10 — 2026-08-01 — §5 Q0b: CERTIFIED-DEGRADED (VISION) forces F1 AMBER.
#   A paper certified under a MEASURED vision outage (the retired audit-side rule on
#   vision outage, now carried by Step 7's own handling) delivers, but must
#   never render green: some figures were machine-checked and never eyeballed. — Universal Delivery Footer Contract
# v1.9.1 — 2026-08-01 — B3 STAYS AT 6 FILES; ENGINES COME FROM THE CLONE
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING, post-deploy correction). v1.9 briefly
#   raised B3 to 8 by shipping blueprint_core.py + figural_core.py per exam. That was
#   the wrong remedy: CLAUDE.md states engines live ONLY in the central repo and no
#   per-project provisioning should ever be performed, because a project copy is a
#   second unverified source that can go stale. Step 8 P0 now copies both engines
#   from the Step-0 verified clone ($FW) instead — the same pattern Blueprint §S1-2b
#   already uses — so the delivery contract returns to 6 and no exam project needs
#   touching. Superseded v1.9 entry:
# v1.9 — 2026-08-01 — STEP 6 B3 DELIVERABLE LIST 6 -> 8 FILES
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D2/D3). B3 now also delivers
#   blueprint_core.py and figural_core.py under their BARE names. Step 8's auditor
#   delegates A-FIGPROFILE to the former and the 12 A-FIG* gates to the latter, but
#   until v1.9 neither engine ever reached an exam project. Bare names are
#   mandatory: they are imported as Python modules and an [ExamCode]_ prefix breaks
#   the import, silently reducing audit coverage. Absence is never fatal — the
#   dependent gates report an explicit WARN skip and the audit still completes.
# v1.8.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   79 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_DeliveryFooter'. The current companion block, the
#   v1.8 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.8 — 2026-07-26 — §5 QUALITY GATE: A FAILING CHECK FORCES AMBER
#          (GAP-2026-07-26-003). A step could report a FAIL and still render the
#          GREEN "Step Complete" footer, because §5 asked only whether the WORK was
#          finished, never whether the RESULT was sound. That is what shipped the
#          reference run: Step 5 finished all 22 papers with 153/153 figural
#          questions unobserved and 45/45 FIGURAL subtopics carrying an empty
#          object-type profile — and rendered F2 green.
#          New Q0 runs BEFORE Q1: any FAIL from the step's own checks (Step 5
#          QV-1..QV-14, Step 8 audit gates, Step 1 unobserved-image count) renders
#          F1 AMBER with the failing check and its remedy named.
#          WARN does NOT force amber — if it did, every run would turn amber and
#          the signal would be lost again.
#          THIS IS NOT A HALT: the step completes, every file is delivered, and the
#          operator may proceed. Amber REPORTS; it does not block.
```

Entry v1.41.0 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v1.42.0 supersedes).

```
# v1.41.0 — 2026-11-07 — GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS (RE-25; paired with
#   PYQExplain v2.28, MockTestExplain v1.54.0). §LADDER gains the three RE-25 lines (two
#   AMBER-CLASS through the existing classes "renderer degraded (…)" / "Q<n> explanation
#   degraded (…)", one INFORMATIONAL "document size … (RE-25 figures)"), and Q0c names
#   PYQExplain as a producer of those lines. Disclosure only — no stop, no verdict change.
#   Every other line of the file is byte-identical (PYQPrepare freeze, owner P1: the
#   PYQPrepare footer path is untouched).
```

Entry v1.42.0 moved at framework release 2026.11.08.1 (GAP-2026-11-07-RE25-HARDENING; v1.43.0 supersedes).

```
# v1.42.0 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (paired with blueprint_core v1.33,
#   MockTestCreate v5.94, MockDeliver v1.27.0). §FOOTER-FT gains the DIFFICULTY LAYER LINES —
#   bc.difficulty_layer_lines over the paper's recorded difficulty_state.paper_gate / l2_model:
#   delivered vs target counts, DR3 items (accepted below their slot after full repair, disclosed),
#   unmeasured slots, the organic ruler's state and the source of its shares. "ℹ️ "-prefixed,
#   disclosure only; a paper without the records prints nothing (byte-identical).
```

Entry v1.43.0 moved at framework release 2026.11.09 (GAP-2026-11-08-DR3-QINDEX-CONFLICT; OD-2026-11-09).

```
# v1.43.0 — 2026-11-08 — GAP-2026-11-07-RE25-HARDENING (paired with MockTestExplain v1.55.0,
#   PYQExplain v2.30, explain_engine v2.14). §LADDER RE-25 gains two engine-written lines:
#   "OPSIN_UNAVAILABLE — …" (AMBER-CLASS) and "RE-25 open findings on <N> question(s) — …"
#   (AMBER-CLASS), both taken VERBATIM from the explanation engine's chs_report_lines output ['footer_amber'];
#   a paper with no RE-25 question prints nothing new (byte-identical).
```

## Framework_MockDeliver.md

Entries v1.12.2–v1.25.0 moved at framework release 2026.11.06 (EC-P42; v1.26.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_MockDeliver.md.

```
# v1.25.0 — 2026-11-04 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE (owner decisions D0, D5 (a);
#   paired with MockTestCreate v5.91, audit_canonical v2.36, blueprint_core v1.31,
#   DeliveryFooter v1.39.0). S1-2 item 3f reads the certificate through
#   bc.certificate_uncertified_active(statuses, entry.quality_readiness, stamps release):
#   an item whose only UNRESOLVED finding is an A-TEMPLATE stamp written by release
#   2026.11.03 (its default template cap of 2 — untrustworthy) is RE-CERTIFIED
#   automatically with one INFORMATIONAL line (RECERTIFIED_ITEMS -> footer). OD-9 restated
#   (D0): NOT CERTIFIED only from an ACTIVE, measured gate; --accept-uncertified is needed
#   only for such a genuine, measured defect.
# v1.24.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (owner decision OD-9 (a);
#   paired with MockTestCreate v5.90, audit_canonical v2.35, blueprint_core v1.30,
#   DeliveryFooter v1.38.0). S1-1 gains the trigger flag --accept-uncertified; S1-2 gains
#   item 3f: the paper's S13-2F certificate (registry question_index[].quality_status ->
#   bc.certificate_uncertified) is read and bc.deliver_allowed(cert, accept) decides — a NOT
#   CERTIFIED paper (items whose quality findings survived ladder R5) is REFUSED with the
#   item list unless the trigger carries --accept-uncertified, in which case it is
#   delivered, the footer says so, and registry.accepted_uncertified records owner +
#   timestamp (written by the 3f block itself; the registry is then delivered under §8).
#   A refusal is a printed, recorded verdict that ENDS the step before any rendering
#   (SystemExit 0 — not a stop class of any kind: nothing is broken, the owner's one-flag re-run
#   is the remedy); no other step changes (Explain is untouched — it reads the status).
#   Release review 2026-11-03: the 3f block lives in §5 Phase 1 (after total_questions),
#   so every name it reads is bound by executable code.
# v1.23.0 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (paired with
#   DeliveryFooter v1.36.0, paper_pipeline v5.40). S1-2 gains item 3e: after the
#   §FOOTER-STYLE line print EVERY string returned by pp.figure_footer_lines(registry,
#   blueprint, paper_id) (§FOOTER-FT) — fallback subtopics, committed-despite-flag records, absent
#   legacy records, migration annotations, unregistered dominant types. A clean current
#   paper prints nothing. Text only; no set, gate or engine change; never a halt.
# v1.22.0 — 2026-09-14 — GAP-2026-09-14-REGISTRY-SOURCE (REGISTRY-SOURCE-LAW; owner decision
#   2026-09-14; paired with MockTestCreate v5.84, MockTestExplain v1.51.0, DeliveryFooter,
#   paper_pipeline CLUSTER RS). [ExamCode]_registry.json is REQUIRED by this step but no
#   longer has to sit in Project Files: it is lawful in EITHER lane — (1) attached to the
#   trigger in chat beside the _Explanation.docx, (2) Project Files. Phase 1 resolves it
#   through pp.resolve_registry (the ONE implementation Steps 7/9/11 share): attachment
#   WINS when both lanes hold a file (a difference is PRINTED, never a stop); HARD STOP [HS:PROSE]
#   only when BOTH are empty; exact filename + registry.exam_code == [ExamCode] validated.
#   The v1.16.0 wildcard scan of /mnt/project (`*_registry.json`, HARD STOP [HS:PROSE] on two files)
#   is RETIRED: the resolver looks for the exact name, so a sibling exam's registry is
#   simply invisible and "the file is in two places" is never a stop. The registry is
#   resolved AFTER EXAM is bound from the blueprints (it needs the exact name). The §8
#   handoff fingerprint is REG_SRC['fingerprint']. S1-2 item 3 and the stop message name
#   both lanes. The heal-then-deliver rule, the closed set, the Replace badge, all 17
#   gates and every artefact are unchanged — only WHERE the file is read. Enforced by
#   LAW_REGISTRY REGISTRY-SOURCE-LAW + mock_sync_audit MS-20.
# v1.21.0 — 2026-09-03 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE C: coverage cursor sole writer + BV-DEL
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
```

Entry v1.12.1 moved at framework release 2026.08.25.3 (EC-P42; v1.14.0 supersedes).

```
# v1.12.1 — 2026-08-13 — SYNC AUDIT ROUND 2: gate-count prose fix. §2 item 4 said "All 16
#   audit gates" while §6 is headed "all 17 must PASS" and runs C1–C17 (C17 = NAT charset).
#   Prose corrected to 17; no gate logic changed.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockDeliver.md.

```
# v1.12.0 — 2026-08-10 — LEDGER INTEGRITY CHECK + REMEDIATION CLASSIFIER
#   (GAP-2026-08-10-QINDEX-FK-ENFORCEMENT). Two changes, both to the FAILURE
#   side of S1-2/S1-3 — the clean-path JOIN, the tagging pipeline, and every
#   C-gate are byte-untouched.
#   (1) S1-2 step 3 now ALSO runs a whole-registry ledger↔index agreement check:
#       a paper listed in mocks_completed/papers_completed with NO question_index
#       entry is a Class-A finding named as REGISTRY DATA LOSS (the entry was
#       dropped by a later write), with remedy "re-run Step 7" — replacing the
#       misleading suggestion that Step 7 was never run.
#   (2) S1-3 build_tag_lookup now COLLECTS every unresolved question, CLASSIFIES
#       each stale subtopic_id, and hard-stops with a per-question remediation
#       report instead of failing on the first and printing "ensure both files
#       are from the same run" (proven misleading: on the reference corpus both
#       files WERE from the same run — the ids were invented at Step-7 write
#       time). Classes: W1 = stale leaf exists on exactly ONE current subtopic
#       (deterministic registry patch, printed ready-to-apply); W2 = leaf
#       reworded, no verbatim match (candidate targets printed; HUMAN must
#       confirm — never auto-applied); D = leaf matches MULTIPLE subtopics
#       (all candidates printed; human decision). Companion to MockTestCreate
#       v5.48.0 (S13-4 copy-by-reference + engine gate A-QINDEX) and
#       MockTestExplain v1.23 (P10 tripwire), which together make reaching this
#       classifier require multiple independent upstream failures.
# v1.11.0 — 2026-08-09 — DELIVERED FILE NOW PRESERVES NATIVE OMML — the OMML→Unicode
#   linearization (Rule 19) is RETIRED from the delivery path. ROOT CAUSE of the
#   reported math-mutation defect: the "WHY THE RENDER-SOURCE DOCX IS SEPARATE"
#   section + Phase 4/5 named the RENDER-SOURCE docx (every `<m:oMath>` flattened
#   to a one-line Unicode text run by Rule 19) as the final delivered `_Final.docx`.
#   That silently DESTROYED all structured math — fractions, radicals,
#   integrals/sums, matrices, sub/superscripts — in every delivered mock paper.
#   The two-artifact design was justified by python-docx round-trip corruption, but
#   Step 11 edits raw `word/document.xml` (unzip→XML→zip) and NEVER round-trips
#   through python-docx, so OMML already survives byte-perfect: the INTEGRITY
#   artifact proves it (gate C5: integrity OMML count == source). FIX: Phase 4's
#   transforms are retired and Phase 5 now delivers the INTEGRITY artifact (native
#   OMML, tag blocks inserted, headers stripped, NO render transforms) as
#   `_Final.docx`. The delivered file is byte-identical to the Step-9 Solutions
#   input except for the pipeline-mandated tag-block insertion (and the safety-net
#   header strip, which is normally a no-op). CONSEQUENCE: Rule 21 (non-ASCII
#   safe-font) and Rule 22 (underline recolor) no longer apply to the delivered
#   file — content fidelity supersedes those portal-cosmetic transforms. Math
#   preservation is now gated: C5 (unchanged) plus C11 INVERTED from "zero OMML in
#   render-source" to "delivered OMML count == source; zero linearization." Mirrors
#   PYQDeliver v1.9, which fixes the identical defect the same way. Touched:
#   ZERO-MUTATION RULE, the render-source rationale section, DEFINITION OF DONE
#   (items 5/6/8), preflight step 7, Phase 4 (retired), Phase 5 (delivers
#   integrity), §6 gates C11/C14/C15, the delivery report, the assembly checklist,
#   the hard invariants, and Rule 19/21/22 headers (marked RETIRED).
# v1.10.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   No logic change: preflight already accepted the Step-9 [ExamCode]_[paper_slug]_
#   Explanation.docx, and that is now the only input that exists. The _Complete filename
#   is retained in the accept-regex purely so papers produced before this release still
#   deliver. What DID change is every certification claim: tag values are Step-7-written,
#   not Step-8-certified, and the pre-Q.1 SAFETY-NET is now a genuine net rather than a
#   formality, because no A-HEADER gate runs upstream of it. Stated plainly and not
#   hidden: the JOIN is still fully deterministic, but its inputs carry one fewer
#   independent check than they did.
#
# v1.9.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   187 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockDeliver'. The current companion block, the
#   v1.9 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.9 — 2026-07-20 — TEST* TRIGGERS + MULTI-BLUEPRINT SUPPORT (paper_pipeline.py
#       integration). Adds TestDeliver P[N]
#       as the primary trigger (works for mock AND every scoped tier via --level/--scope),
#       keeping MockDeliver M[N] as a working alias (implicitly level='mock'). WHAT CHANGED:
#         §1 S1-1 — new PRIMARY trigger TestDeliver P[N] [--level ...] [--scope ...];
#           MockDeliver M[N] retained as the mock-only alias.
#         §1 S1-2 — Solutions-docx filename acceptance generalised from Mock[N] to
#           [paper_slug] (pp.paper_slug); blueprint verification now refers to the
#           RESOLVED blueprint (§5 Phase 1), not an assumed single file.
#         §5 Phase 1 — STRUCTURAL FIX: the old collision check HARD-STOPPED if more than
#           one *_blueprint.json existed in project knowledge. That is now the NORMAL
#           state once any scoped tier has been generated alongside the mock series, so
#           this was blocking every scoped delivery. Replaced with: load every
#           *_blueprint.json present, derive EXAM from them, parse paper_slug from the
#           UPLOADED docx filename, then pp.pick_blueprint(blueprints, level=LEVEL,
#           docx_slug=paper_slug) selects the ONE blueprint this delivery is for
#           (PickError → HARD STOP, never a guess). registry.json collision check is
#           UNCHANGED (still exactly one registry per project — the shared cross-tier
#           ledger). paper_slug itself is now ALWAYS pp.paper_slug(paper_id) (zero-padded
#           for a mock), replacing the old inline `f'Mock{N}' if ... else .replace(':','_')`
#           — the render pipeline (§5 Phase 1 onward, e.g. render_out_path) already
#           consumed the `paper_slug` variable from prior C3 work, so this fix propagates
#           through unchanged.
#       Shared logic (paper_slug, pick_blueprint) lives ONLY in paper_pipeline.py. Does
#       not touch the C1–C17 gate logic, the NAT portal-grading charset validation, or any
#       render/tagging logic.
#
```

Entry v1.26.0 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v1.27.0 supersedes).

```
# v1.26.0 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY Part D (paired with blueprint_core
#   v1.32, paper_pipeline v5.40, MockTestCreate v5.92, DeliveryFooter v1.40.0). S1-2 gains
#   item 3f' — the DIFFICULTY DISCLOSURE LINES reprinted from the paper's recorded
#   difficulty_state / quality_readiness / difficulty_gate coverage through
#   bc.difficulty_unverified_lines (engine-sourced, "⚠️ "-prefixed, disclosure only). The
#   Complexity tag stays the canonical label (guard G9); nothing here stops, withholds or
#   re-certifies. Legacy series (no difficulty_state) print nothing — byte-identical.
```

Entry v1.27.0 moved at framework release 2026.11.09 (GAP-2026-11-08-DR3-QINDEX-CONFLICT; OD-2026-11-09).

```
# v1.27.0 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (paired with blueprint_core v1.33,
#   MockTestCreate v5.94, DeliveryFooter v1.42.0). S1-2 gains item 3f'' — the DIFFICULTY LAYER LINES
#   reprinted from the paper's recorded difficulty_state (paper_gate: delivered vs target counts, DR3
#   items accepted below their slot after full repair, unmeasured slots; l2_model: the organic
#   ruler's state and where its shares came from) through bc.difficulty_layer_lines (engine-sourced,
#   "ℹ️ "-prefixed, disclosure only). The Complexity tag stays the canonical label (guard G9);
#   nothing here stops, withholds or re-certifies. A paper without these records prints nothing —
#   legacy footers byte-identical.
```

## Framework_MockReview.md

Entries v1.0.0–v2.0.0 moved at framework release 2026.11.06 (EC-P42; v2.0.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_MockReview.md.

```
# v2.0.0 — 2026-11-04 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE (owner decisions D0 — OD-5
#   restated, D1, D2 (a), D4; paired with MockTestCreate v5.91 S13-2G, blueprint_core v1.31,
#   audit_canonical v2.36 A-REVIEW, DeliveryFooter v1.39.0). This file is NO LONGER a user
#   step. v1.0.0 made it "Step 7R": the owner ran it in a NEW chat with a review packet,
#   downloaded a verdict file and carried it back to the author's chat for --resume — the
#   two-session protocol that made Step 7 end at AWAITING_REVIEW instead of delivering its
#   two files (incident 2026-11-04, SSC GD Tier 1 TestCreate P2). The MockReview /
#   TestReview TRIGGERS ARE RETIRED (D2 a; routes.json, SKILL.md, PIPELINE). This file is
#   now the brief a FRESH REVIEWER executes INSIDE the Create run: Create S13-2G phase 2
#   starts one fresh sub-agent per packet part (<= bc.REVIEW_PART_MAX items, a passage group
#   never split) and hands it ONLY the part folder; when the runtime has no sub-agent tool
#   the author session applies §2 itself as a same-session cold review (D1; disclosed).
#   Nothing here ever asks the user for anything, writes to the user's output folder or
#   calls present_files. The checklist (§2) and the verdict record (§3, bc.review_verdict_file)
#   are UNCHANGED from v1.0.0, so verdicts bind exactly as before.
#
# v1.0.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY G12 (owner decision OD-5 (a):
#   MANDATORY independent review on every paper, WITH correction). (History: v1.0.0 was a
#   user-run step in a new chat; superseded by v2.0.0 above.)
```

Entry v2.0.1 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v2.1.0 supersedes).

```
# v2.0.1 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY DL-52 (paired with MockTestCreate
#   v5.92). Brief-only: difficulty_band_with_exemplar is now consumed by Create S13-2G phase 3
#   (compared with the slot band; "below" on a Hard slot → bounded R2 repair, residue a
#   level_note). Reviewer isolation is unchanged — the packet carries no band, no
#   difficulty_obs and no level record (handshake H6).
```

## Framework_MockTestAnalyse.md

Entries v2.51.0–v2.59.0 moved at framework release 2026.11.06 (EC-P42; v2.60.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_MockTestAnalyse.md.

````
# v2.59.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (paired with
#   analyse_engine v1.2, blueprint_core v1.30, MockTestCreate v5.90, PYQExplain v2.26).
#   Step 5 MEASURES what the new Create / audit gates read: (1) every subtopic entry of
#   section_rules.md gains a QUALITY (v2.59) block — named_concept_rate,
#   shown_entity_named_rate, stem_word_count p10/p50/p90, tested_concept_lexicon,
#   shape_shares, fingerprint_max_per_paper, near_isomer_share, data_block_layout —
#   written by analyse_engine.synthesise_subtopic/format_quality_block and READ by
#   blueprint_core.read_quality_block / quality_block_for_subtopic (the named consumer);
#   (2) the file ends with an '=== EXAM_QUALITY ===' block (analyse_engine.
#   exam_quality_lines): PYQ_COMMON_ENTITIES, PYQ_TEXT_LEAK_CALIBRATED, PYQ_MODE and the
#   §4.6 GATE_CALIBRATION false-FAIL guard; (3) the style profile's item_rules carry stable
#   ids (bc.ITEM_RULES) and MIDDLE_VALUE_KEY; (4) NEW S11-1b: [ExamCode]_exemplar_bank.json
#   — the content-carrying exemplar bank the difficulty judge reads — written by
#   analyse_engine.write_exemplar_bank and delivered as a RUN FILE (owner decision OD-11:
#   kept beside the registry, attached to Create, NEVER uploaded to project knowledge;
#   absent at Create -> the judge is DORMANT, printed, never a halt). Nothing here stops.
#   RELEASE REVIEW (2026-11-03, cold read): the QUALITY block's lexicon / drawn-name /
#   near-isomer rates and the EXEMPLAR BANK are built from the exam's own EXPLAINED PYQ —
#   [ExamCode]_difficulty_profile.json (PYQExplain v2.26 named_concepts / concept /
#   drawn_names / near_isomer_set per item) JOINED to this step's stems by stem text
#   (analyse_engine.profile_quality_inputs / exemplar_rows / entity_paper_sets, run_synthesise
#   + S11-1b). The first draft fed only the subtopic/topic titles (an always-empty
#   lexicon) and read band fields Step 5 never had (an always-empty bank). QUALITY blocks
#   now carry `n` (the pool size the blueprints' shape targets need). Absent / legacy /
#   foreign profile: everything reads 'unmeasured' and the bank is empty — printed, never
#   a halt.
# v2.58.0 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (paired with
#   analyse_engine v1.1, blueprint_core v1.29, figural_core v5.89, MockTestCreate v5.89).
#   run_synthesise measures FIGURE_STYLE_PROFILE from the exam's own PYQ documents
#   (generic flags over every picture of every exam; chem-R print metrics over pictures
#   typed chemistry by this run's own per-question object_type) and aggregates PYQExplain
#   §13A tags (abbreviations seen, site-mark devices, ask / representation / grammar
#   counts). section_rules.md gains one '=== FIGURE_STYLE ===' line (read by figural_core
#   .parse_figure_style_block — byte-identical, drift-locked) and, per figural subtopic,
#   figural_ask_type_counts / representation_counts / scheme_grammar_counts (read by
#   blueprint_core.parse_image_analysis_blocks). Absent evidence -> documented defaults,
#   disclosed downstream; never a halt. No other extraction change.
# v2.57.3 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (LAW F1.2;
#   paired with figure_types v1.0, analyse_engine, MockTestCreate v5.88). PATCH: the
#   PYQ_IMAGE_ANALYSIS contract is unchanged in shape; object_type strings are now
#   NORMALISED onto the figure-type registry vocabulary at Phase C (analyse_engine.
#   apply_vision_observations → figure_types.normalise; the raw Phase-B string is kept as
#   object_type_raw), so Step 7 and the auditor see ONE name for one kind of figure, and
#   QV-14's line names every object_type the registry does not know (advisory, never a
#   FAIL — the vocabulary grows by evidence). Phase B step 3 asks for the registry's
#   canonical names where one fits. Step 5 output on an exam whose strings were already
#   canonical is byte-identical.
# v2.57.2 — 2026-09-21 — GAP-2026-09-21-LINKED-PLACEMENT (paired with MockTestCreate v5.85,
#   blueprint_core Cluster SG, audit_canonical v2.30, mock_sync_audit MS-11 name set).
#   NEW S1-1b: [ExamCode]_stimulus_profile.json — how this exam builds its question SETS
#   (sizes, member mix/order, position), built by bc.build_stimulus_profile from the
#   progress records (current-pattern papers only; a set = consecutive questions sharing
#   one run of >=30 words; type seen in >=2 papers). Written by every final synthesis
#   (MANDATORY delivery tier: 8 mandatory files, 10 on a normal run) and by the NEW mode
#   `PYQExtract --stimulus-profile` — for exams whose Step 5 already finished: reads the
#   progress file, writes and delivers ONLY the profile, HALTS; no PYQ: link; no other
#   artefact touched. Step 7 needs it before any new paper (MockTestCreate S3-12b).
# v2.57.1 — 2026-09-14 — GAP-2026-09-14-DELIVERY-ECHO (DeliveryFooter v1.34 §9 / R6; paired
#   with PYQExplain v2.24, PYQScan v1.6.1). present_files is CLASS T (`pass`): the model
#   performs the call from what it can SEE. deliver_final built `delivery` (7 mandatory
#   + 2 conditional) and never printed it — and its own printed handoff named only
#   section_rules / progress / summary, three of nine — so the call was made from
#   memory; the per-batch site had the same shape for one file. Both sites now print
#   the closed set through print_delivery_set() (PHASE 1) immediately before ONE
#   present_files call, and deliver_final's handoff lists the full S11-2 PART C set.
#   PATCH bump: emitted stamps stay v2.57 (no engine change, no artefact change —
#   deliver_final prints only; run_synthesise never reaches it). MS-11 parses the
#   deliver_final construction block by its append/+= lines, which are unchanged.
#   Reports only — no new stop.
# v2.57 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: era-filtered mining + sample papers; requires PYQSort >= v1.21.0
# v2.56 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY (Stage 1, reading side). Step 5 now
#   MEASURES style instead of looking it up: determine_strip_mode is RETIRED as a synthesis
#   input (Q9) — the content signature is derived from the questions themselves and maps
#   aptitude-class corpora to the five legacy masking modes (byte-identical output, EC-26)
#   while content-class corpora (science/engineering/medical/law/commerce, previously
#   silently mislabelled 'reasoning') get v2 masking that keeps notation and units.
#   ADDED: 24-mechanic ordered classifier (unknown REPORTED never defaulted), 15-value
#   option-shape vocabulary, Axis-2 ladder 8→11 (IDENTIFY / SELECT_PLOT / RANK; STATEMENT
#   widened per E-7), pattern_keys (KEY = mechanic|form|polarity|answer_type|option_shape;
#   S7-STYLE composes from these, never from template text — RC-3), numeric distractor
#   mining, per-unit number ranges {min,max,p10,p50,p90,n} + PYQ_EXCLUDE_VALUES (EC-49
#   universal-constant exemption), EC-9 low-entropy detection, stimulus_stats (Q11), and
#   medium stamping (§6.1.9: style computed on 'en' renderings; other-medium counted).
#   THREE-ARTEFACT CONTRACT (§6.1.8): the SAME PYQExtract run now also writes
#   <EXAM>_style_profile.json (activation-gated, DORMANT is a written status with a
#   reason, never a missing file — P-3) and <EXAM>_pyq_index.json (shingle/hash index,
#   no question text), both stamped with the SAME corpus_hash (sha256 over sorted
#   per-paper file hashes, stamped by process_pyq_paper). E-13: stem/option text now
#   reads corpus_io.text_of(para) so <w:t>/<m:t> interleave in document order;
#   enrich_paragraph_with_omml retained for flags only. E-3: content-path approach
#   derives from the measured mechanic (MECHANIC_TO_APPROACH); the aptitude path keeps
#   infer_approach VERBATIM. AXIS2_CLASSES defined ONCE in blueprint_core (P-7).
#   Additive-only: every pre-existing section_rules field is byte-identical on the
#   aptitude reference corpus except the version stamps. Engine self-test 120 → 183
#   (+50 style fixtures, +13 mutation-kill pack; B4 pipeline mutation within budget 1).
# v2.55 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE. E-9 keyword difficulty scorer
#   RETIRED (blueprint_core.score_difficulty, analyse_engine adapter, build_diff_criteria
#   deleted; Step 5 writes no PYQ_DIFFICULTY_CALIBRATION; QV-3 reports 'retired'). Difficulty
#   is measured once, by PYQExplain §7A with the derivation rubric, into the exam's
#   difficulty profile (PYQExplain S7A-6 / blueprint_core Cluster DP), which Blueprint §S7-0
#   and Step 7 / ScopedBlueprint read. EC-6 marks no longer scale a threshold. §14 schema and
#   MockCreate handoff text updated. analyse_engine self-test 120 (−3 E-9, +2 guards).
# v2.54.1 — 2026-08-23 — GAP-2026-08-23-STEP5-YEARLESS-TEMPLATES (P1) + DOC SYNC.
#   PATCH bump: emitted stamps stay v2.54; the golden (all-dated) corpus is
#   byte-identical — the fix is a filter that is a no-op when every year is set.
#   THE DEFECT. generate_templates (analyse_engine) read
#       years = sorted(set(q.get('year', 2020) for q in questions))
#   Extraction stamps q['year'] UNCONDITIONALLY (process_pyq_paper), so a paper
#   whose filename carries no year stores None WITH THE KEY PRESENT — and a .get
#   default never fires for a present key. sorted() over {int, None} raises
#   TypeError inside synthesise_subtopic, which runs for every subtopic: a hard
#   stop of the WHOLE synthesis for any corpus that mixes dated and undated paper
#   filenames. Found by executing this file's own fences end-to-end against a
#   production-shaped corpus (the D1/D2 method); every static gate was green.
#   SAME FAMILY as D7 and ONE FUNCTION from D7's own fix — which survived because
#   the D7-era fixtures modelled a year-less question as key-ABSENT, the one shape
#   the dead default could satisfy. A fixture in the wrong shape consumes the
#   suspicion that would have found the defect (the D7 lesson, replayed).
#   SECOND SITE swept in the same function: the cluster 'years' set collected
#   i['year'] unfiltered, so the identical crash waited one line behind the first.
#   FIX. Year-less questions drop out of the RECENCY basis only — years/last2 and
#   per-pattern years now filter None — exactly the rule subtopic_option_format
#   already applies to its recency vote (D7). All-dated corpora are unchanged. An
#   all-undated corpus previously emitted years=[None] and stamped observed_recent
#   from a None-in-{None} membership accident; it now emits years=[] with
#   confidence from raw_count, which is what the D7 principle requires. Engine
#   fixtures added in the PRODUCTION shape (year key present, value None): mixed,
#   all-None, and an all-dated equivalence guard.
#   DOC SYNC in the same release (no behavioural rule changes beyond the above):
#   * PARAMETER 4 still described the pre-v2.50.0 auto-redirect to --synthesise
#     ALL on an empty corpus — the exact fall-through EC-P39 forbids and this
#     file's own DoD [25] names as the dangerous path. Rewritten to state EC-P39.
#   * §1-6 / compute_coverage_mode carried contradictory inserted lines (a
#     "guideline, not a blocker" sentence inside a NON-NEGOTIABLE rule, and a
#     phantom min_pyq_years project/trigger parameter that no parser anywhere
#     reads). Aligned to the enforcement code: min(5, available), never waivable,
#     with fewer-than-5-years exams processing ALL available years.
#   * E-9/E-10 CROSS-FILE SYNC RULE still demanded a byte-identical mirrored COPY
#     in blueprint_core; v2.30 replaced the copy with a delegating adapter.
#     Restated as a delegation rule so no editor re-introduces a second copy.
#   * DoD [4] said "QV-1 through QV-12"; the suite is QV-1..QV-16 (+QV-5b,
#     +QV-13b). S11-2 PART A's example extended to show all 16.
#   * DoD numbering collision: the v2.24.6 additions in §15 reused [24]-[26],
#     numbers already taken by the transport/corpus items in the main DoD list.
#     Renumbered [27]-[29]; content unchanged.
#   * S8-7 schema now documents q_num / question_type / terminated_by_heading
#     (stamped at the one emission point since v2.37/v2.39) and that year is
#     null when the paper filename carries no detectable year.
#   * S8-0b's incident byte/line counts annotated as historical measurements —
#     the live numbers come from bootstrap and SPEC_SECTIONS.json at run time.
# v2.54.0 — 2026-08-23 — STAMP-DEDUP + TRANSPORT-HELPER EXTRACTION (Items 3a+3b;
#   MINOR — changes one artefact line per section_rules.md). 3a: the section_rules
#   header line read "# Generated by Generated by ..." since v2.3 —
#   GENERATED_BY_STAMP already begins with "Generated by" and write_section_rules
#   prepended it again (analyse_engine L2900). Fixed at the f-string; stamps
#   cascade v2.53 -> v2.54 (MS-3). EXPECTED ARTEFACT DIFF, documented before
#   capture: the dedup line + every v2.53 stamp line; nothing else. Golden set
#   RE-CAPTURED from this release's output — prior hashes are superseded and
#   recorded in the harness doc as the pre-fix reference. 3b: the six transport
#   helpers left this file's fences for transport_core.py — build_session_re,
#   make_drive_list_fn, make_paper_id, is_already_processed VERBATIM;
#   sort_papers_recency_first gains a session_re PARAMETER (it closed over the
#   session global SESSION_RE — an engine cannot); collect_pyq_papers gains a
#   required listing_cache parameter. Both keep one-line DELEGATING ADAPTERS here
#   preserving the session defaults (SESSION_RE, DRIVE_LISTING_CACHE), per the
#   DELEGATION contract. collect_pyq_papers.last_rejects attribute DROPPED —
#   read nowhere in the corpus (verified by grep); rejects remain ATTACHED via
#   the returned tuple (the v2.29 rule, unchanged).
# v2.53.6 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: helpers fence tagged + def-wrapped (signatures unchanged); A0 prose to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v2.53.5 — 2026-08-20 — WAVE 2 PART C, BATCH 9. §S8-0 DRIVE TRANSPORT MOVES TO
#   transport_core.py. PATCH bump: code moved VERBATIM into a routed engine changes no
#   emitted value, and holding major.minor holds the emitted stamps at v2.53. NO
#   ARTEFACT VALUES CHANGE — all six IIT_JAM_MATHEMATICS artefacts verified
#   byte-identical against the golden set from deployed 2026.08.19.3.
#
#   WHAT MOVED. One fence, 346 lines, 8 functions, ZERO top-level session-flow
#   statements: acquire_listing, probe_transport, probe_drive_channel, plan_transport,
#   acquire_paper, read_transport_verdict, record_transport, log_session, plus the
#   derived constant SESSION_INLINE_BUDGET. The same definition/flow split that governed
#   batches 2, 3 and 5, applied unchanged. Spec python 2,352 -> 2,051 lines.
#
#   WHAT DID NOT MOVE, AND WHY THE BLOCK WAS EXTRACTABLE AT ALL. gdrive_search and
#   gdrive_download_file stay here. They are CLASS T markers — operations the MODEL
#   performs in its own turn — and an engine cannot perform a tool call. Every function
#   that moved takes the RESULT of a CLASS T operation as an argument (pages,
#   probe_payload, drive_payloads, resolver), which is exactly what made the boundary
#   clean.
#
#   WHY NOW. This fence was INVISIBLE until release 2026.08.20.2. It carries a triple
#   backtick inside a docstring, and four auditors extracted fenced python with a
#   non-greedy regex that ended at the first such marker — so the fence was cut
#   mid-string, failed to parse, and was discarded by each caller's parse guard. Nothing
#   failed; the tools simply never read the Drive transport contract, and code that is
#   never read produces no findings. The line scanner made it readable. This release
#   makes it TESTABLE: 49 self-test fixtures and a mutation gate, neither of which can
#   exist for code that lives in a fence.
#
#   VERIFICATION IS NOT THE GOLDEN SET, AND SAYING SO MATTERS. run_synthesise — the
#   path `--synthesise ALL` exercises — calls NO function in this block, so the golden
#   set proves the synthesis is unchanged and proves nothing about the transport. What
#   stands in its place: the extraction is byte-verbatim (the divergence baseline's
#   fingerprints for plan_transport, acquire_paper and probe_drive_channel are IDENTICAL
#   before and after the move, which is the refactor proving itself), 49 fixtures that
#   inject every dependency rather than touching a filesystem, and a pipeline mutation
#   gate at 3/3.
#
#   THE STEP 4 DIVERGENCE SURVIVED THE MOVE — BY ONE LINE OF FORESIGHT AND ONE
#   CORRECTION. Framework_PYQCount S5-0 defines its own probe_drive_channel,
#   plan_transport and acquire_paper; the divergence is declared and pinned in
#   XSPEC_DIVERGENCE_BASELINE.json. When this batch landed, all three entries reported
#   "no longer diverges" and demanded deletion — the ratchet was right that something had
#   changed and wrong about what. Deleting them would have let this refactor quietly
#   retire the only check watching those pairs. audit_deep now reads ENGINE definitions
#   as well as spec fences, and a new XSPEC-ENGINE-DRIFT check reports a spec that
#   re-localises an engine-defined function without delegating, so the exemptions
#   suppress a real finding again instead of being decorative.
#
# v2.53.4 — 2026-08-20 — WAVE 2 PART C, BATCH 7. DEFECT D7, AND THE WRITERS ENTER THE
#   MUTATION GATE. PATCH bump: the emitted stamps stay at v2.53 and NO ARTEFACT VALUES
#   CHANGE — all six IIT_JAM_MATHEMATICS artefacts verified byte-identical against the
#   golden set from deployed 2026.08.17.1.
#
#   D7 (P1) — ONE QUESTION WITH NO YEAR CRASHED THE WHOLE SYNTHESIS.
#   subtopic_option_format() bucketed formats with `by_year.setdefault(q.get('year',
#   '?'), ...)`, then sorted those keys on the very next line. The '?' sentinel puts a
#   str into a dict whose other keys are ints, so the moment a corpus contained BOTH a
#   year-bearing question and a year-less one:
#       TypeError: '<' not supported between instances of 'str' and 'int'
#   raised inside synthesise_subtopic(), which runs for EVERY subtopic. Same family as
#   D1/D2/D6: a hard stop of Step 5, invisible on the reference corpus because every
#   IIT_JAM_MATHEMATICS question happens to carry a year. Across ~200 exams a single
#   failed year extraction is not an edge case, it is a Tuesday.
#
#   The same sentinel had a second effect: it made the function's own `if not years:`
#   guard UNREACHABLE. by_year gained a key for every question, so `years` was never
#   empty and the branch written for a year-less corpus could never run. Year-less
#   questions are now dropped from the RECENCY vote only — they cannot inform which
#   option format is most recent — which fixes the crash and restores that guard to the
#   job it was written for. Equivalence is exact where it matters: with every question
#   carrying a year (the golden set) by_year is unchanged; with NO question carrying one
#   the old path returned recent_format == primary and changed_recently == False, which
#   is precisely what the restored guard returns.
#
#   HOW D7 WAS FOUND, which matters more than D7. The mutation gate reported the
#   `sorted(` on that unreachable branch as a SURVIVING MUTANT while a fixture named
#   `no_year_branch_all_observed_sorted` — added one release earlier — passed. Both
#   statements were true at once, and only one reading explains both: the fixture never
#   reached the line it was named after. A fixture that passes without executing the
#   code it claims to cover is worse than no fixture, because it also consumes the
#   suspicion that would have found the defect.
#
#   THE WRITERS ARE NOW TESTED AT ALL. Nine of the twenty surviving mutants lived in
#   five functions the engine self-test had NEVER CALLED — synthesise_subtopic,
#   compute_section_axis_distribution, write_section_rules, write_subtopic_manifest and
#   rebuild_subtopic_manifest_from_section_rules. The reason was mechanical, not
#   editorial: each writes to a hardcoded '/mnt/user-data/outputs/', which does not
#   exist on a CI runner, so no fixture COULD call them. An additive `out_dir=None`
#   (default unchanged, every production call site untouched) removes that blocker —
#   the same remedy `search_dirs` applied to load_mechanic_overrides after
#   GAP-2026-08-17-B4-ENV-SKEW. An `if os.path.isdir(...)` guard around the fixture
#   would NOT do: a guarded assertion is a dormant one, and a dormant assertion is
#   exactly where a survivor hides while CI reports green.
#
#   The new fixture is a different SHAPE from B5/B6, which asserted on directly-callable
#   pure functions. The remaining ordering defects live BEHIND the writers, so a small
#   corpus is driven end to end — questions -> synthesise_subtopic -> write_section_rules
#   -> write_subtopic_manifest -> rebuild — and the assertions read the artefacts back.
#   It is adversarial by construction, not merely representative: four sections colliding
#   on one prefix supplied out of alphabetical order (1 in 24), four papers whose figural
#   counts are all different so the per-paper series is a permutation detector rather
#   than a bag of equal numbers (1 in 24), and four years whose set-iteration order is
#   not their sorted order. A fixture whose values are all equal cannot see an ordering
#   defect at all; that is how nine of these survived a suite of eighty-six checks.
#
#   QV-13 WAS HALF A GATE. It is named MECHANIC IDENTITY INTEGRITY and identity is the
#   PAIR (collision_domain, form_key) — the uniqueness test buckets by exactly that
#   pair. It re-derived form_key to detect drift and threw the freshly-derived
#   collision_domain away, so a drifted domain passed unnoticed while the check that
#   exists to catch drift reported PASS. Not hypothetical: build_section_prefix_map
#   assigns colliding prefixes by iteration order, which is the defect v2.53.3's B6
#   batch fixed in mint_subtopic_ids and stamp_mechanic_axes. Those two were pinned; the
#   GATE that notices when they drift was not. QV-13 now compares both halves, with the
#   same curator-override escape hatch form_key already had.
#
#   DIAGNOSTIC TEXT IS PART OF THE CONTRACT. Five survivors were a `sorted(...)` inside
#   a hard-stop message, and the tempting verdict is "equivalent mutant — only word
#   order in an error changes". It is not. Each enumerates a SET, so the same corrupt
#   overrides file produces a differently-worded refusal on every run: a curator cannot
#   diff two runs, cannot grep a log for a known message, and cannot tell a second fault
#   from the same fault re-ordered. Artefact nondeterminism (D4) applies to what the
#   operator READS, not only to what the writers EMIT. Each message is now asserted
#   verbatim, with three or more members, because a two-element set is a coin flip.
#
#   MEASURED. Pipeline mutation survivors 20 -> 1; score 60.0% -> 97.9%; engine
#   self-test 86 -> 116 checks. The single remaining survivor is PROVEN EQUIVALENT and
#   documented at its own site: `years_seen` in _compute_structural_changes is read on
#   four lines and every one is order-invariant (truthiness, max, min, len), so no
#   fixture can kill it and none is faked. MUTATION_BUDGETS.json ratchets 20 -> 1.
#
#   AND THE WATCHER GAINED A WATCHER. audit_mutation.py — the gate whose entire job is
#   proving other tests are connected — had no --self-test, and validate.yml never ran
#   one. The cost showed up here: a `sorted(` inside a NESTED test helper's DOCSTRING was
#   listed as a live target and counted as a surviving mutant of the production engine.
#   The scaffolding exclusion tested only the innermost frame, so a helper defined inside
#   self_test was fair game. It now tests the whole enclosing chain, ships ten fixtures
#   plus a meta-assertion, and runs as a blocking CI step before the gate it guards.
#
# v2.53.3 — 2026-08-17 — WAVE 2 PART C, BATCH 3. §3 + §5 + §6 MOVED TO analyse_engine.py.
#   PATCH bump, same reasoning as B2 and the §16 precedent: code moved verbatim into a
#   routed engine changes no emitted value, and holding major.minor holds the emitted
#   stamps at v2.53. NO ARTEFACT VALUES CHANGE — all six IIT_JAM_MATHEMATICS artefacts
#   verified byte-identical against the golden set from deployed 2026.08.17.1, across
#   PYTHONHASHSEED 1/17/2029/7.
#
#   WHAT MOVED. The 8 python fences of §3 (document pipeline), §5 (synthesis engine) and
#   §6 (QV-1..QV-16) — 3,882 lines, 95 definitions, ZERO top-level session-flow
#   statements. 7 of 8 fences are byte-identical in the engine; the 8th (§3 L1884-2046)
#   is modified by design, for the session_re injection below. No copy remains here.
#
#   THIS COMPLETES THE EXTRACTION. What is left in this file is §1 (session start,
#   CLASS: T Drive tool calls, 31 top-level flow statements) and §8 (batch orchestration,
#   the model-turn loop). Neither can move: they ARE the session, not library code.
#
#   SESSION_RE — the ONE session global in the whole 4,582-line scope, and the only
#   behavioural change in either batch. §1 builds it from exam_config.json's
#   session_keyword; extract_shift_from_filename() read it as a module global. An engine
#   has its own globals and inherits nothing, so it is now INJECTED:
#     extract_shift_from_filename(path, session_re=None)  -> raises if omitted
#     process_pyq_paper(..., session_re=None)             -> threads it down
#   and §8's three call sites pass session_re=SESSION_RE.
#   A PARAMETER, NOT MODULE STATE, DELIBERATELY: a configure()-style global would let a
#   caller that forgot to set it use a STALE regex from a previous exam — a wrong answer
#   rather than an error, which is this corpus's most expensive failure shape. Omission
#   now raises immediately and names what to pass, following the v2.39 vision_pending
#   precedent. Mutation-tested: replacing the raise with a silent default fails the
#   engine self-test.
#
#   MASKED DEPENDENCIES SURFACED, AGAIN. Analysed inside the spec, §3+§5+§6 looked to
#   need nothing but §2's names; imported as a module it also needed `json` and `os`,
#   which §1 had been supplying through the shared namespace. That is the same
#   inheritance that hid `collections` for ten days in D2. python's symtable now
#   confirms the engine has ZERO free globals.
#
#   A BUG THE GOLDEN SET COULD NOT SEE. Threading session_re into §8's call sites
#   introduced a double comma, which made that fence fail ast.parse. The golden set
#   still passed — the broken fence was silently SKIPPED, and --synthesise ALL does not
#   use run_batch_loop. A parse gate over all 42 fences now runs alongside the artefact
#   assertion; byte-identical output is necessary and NOT sufficient.
#
#   audit_seam.py — CAUGHT AT DEPLOY, NOT BY ME. The first cut of this release was
#   rejected: audit_seam reported 5 ORPHAN-READ findings because it identifies producers
#   and consumers from hardcoded five-file maps and analyse_engine.py was in neither, so
#   every field whose writer moved lost its visible producer. Pure relocation — figural_rate
#   14 in the old spec, 14 in the engine, 0 left behind. SAME CLASS release 2026.08.17.1
#   already fixed once for audit_callgraph C4; this batch repeated the extraction at four
#   times the scale and audit_seam did not receive the same widening.
#   Registering the engine surfaced two more, figural_no_image and image_not_figural,
#   whose real writer is corpus_io.figural_consistency() — unregistered, so BOTH sides
#   had been invisible and that seam had never actually been checked. Its writer is now
#   registered too: the honest completion, not an ALLOW entry.
#   ROOT CAUSE OF THE MISS: I verified against ten auditors recalled from memory.
#   .github/workflows/validate.yml runs fifteen gates plus audit_mutation. The gate list
#   is now read from validate.yml, not remembered.
#
#   MS-3 STAMP-PARITY. The three emitted-stamp literals moved into the engine, so MS-3 —
#   a PRESENCE check over this file's fences — reported it could match nothing, the
#   disarmed state its own comment names. Fixed the way MS-3 asks: one literal per
#   pattern retained in the §5 stub, with the cross-file sync rule stated. Widening MS-3
#   to the routed engines was NOT done, for the same reason Y-IMGGATE was not widened in
#   B2. A CALL-SITE check may follow the code into an engine; a PRESENCE check may not.
#
# v2.53.2 — 2026-08-17 — WAVE 2 PART C, BATCH 2. §2 + §4 MOVED TO analyse_engine.py.
#   PATCH bump, following the §16 precedent exactly: when §16 moved to
#   frequency_xlsx.py the release was v2.39.1 -> v2.39.2, because moving code
#   verbatim into a routed engine changes NO emitted value. Holding the major.minor
#   also holds the FRAMEWORK_STAMP at v2.53, so mock_sync_audit MS-3 stays satisfied
#   and the artefacts are literally unchanged rather than changed-by-one-stamp-line.
#   NO ARTEFACT VALUES CHANGE — all six IIT_JAM_MATHEMATICS artefacts verified byte-identical against the
#   golden set captured from deployed 2026.08.16.3, across PYTHONHASHSEED 1/17/2029/7.
#
#   WHAT MOVED. The 14 python fences of §2 (universal extraction primitives E-1..E-11)
#   and §4 (vision aggregation) — 700 lines, 33 definitions, ZERO top-level session-flow
#   statements — moved VERBATIM into analyse_engine.py. Verified: all 14 fence bodies
#   are byte-identical in the engine, and NO copy remains in this file. One writer.
#   Each fence is replaced by a stub that RETAINS THE CONTRACT and imports the names,
#   exactly as §16 was replaced when its code moved to frequency_xlsx.py at v2.39.2.
#
#   WHY §2+§4 AND NOT §2+§3+§4 as first planned. The boundary was chosen by the CALL
#   GRAPH, not by section number. Measured: §2+§4 needs NOTHING from any other
#   extractable section; §2+§3+§4 does NOT close, because §3's process_pyq_paper calls
#   §5's tag_axes and an engine's globals inherit nothing from the spec; and §3+§5+§6
#   needs 16 names from §2. So §2+§4 ships first and §3+§5+§6 follows as B3.
#
#   THE ENGINE IS SELF-CONTAINED, PROVEN BY symtable. A free-name analysis of §2+§4
#   inside the spec reports nothing missing, because §1 imports re / bc / corpus_io /
#   Counter / SequenceMatcher at module scope and every later fence inherits them. That
#   inheritance is exactly what hid GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE D2 for
#   ten days. An engine inherits nothing, so every dependency is now declared at the top
#   of analyse_engine.py where a reader and an auditor can both see it. Python's own
#   symtable confirms ZERO free globals remain.
#
#   COST. This file: 533,663 -> ~507,000 B; §2 567 -> 110 py-lines, §4 133 -> 44.
#   The PYQExtract route still exceeds SPEC_BUDGET_BYTES and still needs its read set;
#   extraction cures the model RE-EMITTING the code, not the byte gate. §1 (817 lines,
#   31 flow nodes) and §8 (1,233 lines, CLASS: T tool calls) stay permanently.
#
#   TWO AUDITOR CONSEQUENCES, one fixed and one deliberately NOT.
#   * audit_callgraph C4 reported 5 live blueprint_core/corpus_io functions as dead
#     (derive_image_roles, gates_passed, merge_vision_observations, verify_images,
#     vision_profile) because their call sites moved into the engine. analyse_engine.py
#     is now a C4 call-site source — the same treatment, with the same stated reason,
#     that audit_canonical.py already had after an earlier extraction.
#   * validator Y-IMGGATE fired for the same reason. Widening IT was built,
#     mutation-tested and REJECTED: Y-IMGGATE matches a NAME ANYWHERE IN TEXT, and
#     corpus_io.py and blueprint_core.py both contain those names, so widening its
#     corpus would have made the gate vacuous for nearly every spec in the estate. The
#     accounting contract is retained in the §2 stub instead, keeping the check at
#     exactly its original strength. A CALL-SITE check may follow the code into an
#     engine; a PRESENCE check may not.
#
#   ALSO CORRECTED: SKILL.md declared "10 routed engine scripts" against 15 actually
#   routed — stale by five BEFORE this batch. MUTATION_BUDGETS.json named this exact
#   risk ("SKILL.md's declared counts are exactly the kind of hand-written number this
#   corpus has watched drift before, and nothing currently proves the check that guards
#   them still fires"). It had drifted. Now 16 and matching.
#
# v2.53.1 — 2026-08-16 — GAP-2026-08-16-BASELINE-SUPPRESSED-NAMEERRORS (D5, D6).
#   PATCH bump: two guaranteed NameErrors are fixed. NO ARTEFACT VALUES CHANGE and the
#   v2.53 stamps are deliberately untouched — verified byte-identical against the
#   IIT_JAM_MATHEMATICS golden set captured from deployed 2026.08.16.2.
#
#   BOTH WERE SUPPRESSED BY spec_name_audit_baseline.json, and both survived the very
#   release that fixed D2/D3 — because `--write-baseline` re-freezes whatever is
#   currently unbound, including defects the previous release introduced. A ratchet
#   wired to a working detector, with a switch in between that accepts everything the
#   detector finds, is not a ratchet. That switch is closed in this release.
#
#   D5 — process_pyq_paper() raised NameError on `n_vision`, on EVERY paper of EVERY
#     exam, unguarded, on its second-to-last statement, after all work was done and
#     before `return questions, linked_groups` could run. `n_vision` is a LOCAL of
#     run_batch_loop() in §8. So Step 5's EXTRACTION phase was broken too, not only
#     synthesis. The per-paper figural count is len(vision_candidates); §8's n_vision
#     is the BATCH queue size and was never the right number here.
#
#   D6 — run_qv() read `options_count`, a SESSION parameter bound nowhere at module
#     scope. QV-15's comprehension only EVALUATES it when _tbh is non-empty — that is,
#     when at least one question WAS terminated by an inferred heading. So QV-15 raised
#     EXACTLY when it had something to report and passed silently when it did not: a
#     check that crashes only on the defect it exists to detect, and reads as a clean
#     PASS on every corpus that never triggers it. IIT_JAM_MATHEMATICS has 0 such
#     questions, which is the ONLY reason the v2.53.0 certification run survived it.
#     Now read from progress._meta.options_count, the parameter's persisted home, with
#     the documented safe default of 4.
#
# v2.53.0 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE.
#   MINOR bump: EMITTED ARTEFACT VALUES CHANGE (D4 orders one list), a function's
#   contract is tightened (print_qv), and a defect CLASS is swept across four specs.
#
#   STEP 5 SYNTHESIS HAS NOT BEEN ABLE TO EMIT AN ARTEFACT SINCE 2026-08-05.
#   Found while building the Wave 2 Part C regression harness: executing this file's
#   own fenced python against the real 884-question IIT_JAM_MATHEMATICS corpus raised
#   TypeError before anything was written; neutralising that raised NameError four
#   frames later. Both unconditional, both corpus-independent, both on the single path
#   every exam takes. Every auditor was green throughout.
#
#   D1 (P1) — print_qv could not read what run_qv returns. run_qv returns ONE dict
#     holding two kinds of entry; print_qv unpacked EVERY value as (status, detail).
#     v2.41.0 added results['_counter_questions_terminated_by_heading'] = len(_tbh),
#     an int, unconditional, "reported even when 0" — written once, read nowhere.
#     From that release: TypeError: cannot unpack non-iterable int object, raised
#     BEFORE write_section_rules. 11 days, 11 minor versions, zero artefacts.
#     FIX: the dict's contract is now explicit and ENFORCED — 'QV-*' keys are checks
#     and must be 2-tuples; '_'-prefixed keys are counters, reported on their own
#     line (preserving v2.41.0's intent, which was visibility, not check-hood);
#     anything else raises AT ITS SOURCE naming the offending key.
#
#   D2 (P1) — `collections` used, imported nowhere. compute_section_axis_distribution
#     is module-qualified (collections.defaultdict / collections.Counter) but
#     `import collections` appears NOWHERE in this file — every import is the
#     `from collections import ...` form, which never binds the module name.
#     NameError on every call since v2.46.0 (2026-08-06). write_section_rules calls
#     it, so section_rules.md was never written. FIX: function-local import, this
#     file's dominant idiom.
#
#   D3 (P3) — present_files() called from python, defined nowhere. FIVE call sites
#     across FOUR specs (this file twice, PYQScan, PYQExplain, MockTestExplain).
#     SAME SHAPE as D2 of GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed
#     the INSTANCE and left the CLASS standing. Swept now: a CLASS: T stub is
#     declared in EACH calling spec, matching this corpus's established house
#     pattern — gdrive_search and gdrive_download_file are each declared in both
#     this file and Framework_PYQCount.md. Per-file declaration is deliberate: a
#     pass-bodied marker has no logic to drift, and spec_name_audit is a PER-FILE
#     auditor, so a declaration held only in a route peer would be invisible to it
#     — which is how a route-level fix would have re-created the very blind spot
#     this gap is about. Framework_DeliveryFooter.md keeps the F1/F2 contract and
#     gains the same stub (it is on all 23 routes).
#     P3 only because deliver_final runs AFTER all five artefacts are on disk.
#
#   D4 (P1 for reproducibility) — NO STEP 5 ARTEFACT WAS EVER REPRODUCIBLE.
#     E-8 subtopic_option_format returned 'all_observed': list(set(fmts)). Set
#     iteration order over str depends on PYTHONHASHSEED, randomised PER PROCESS,
#     and §14 emits the list verbatim as option_format_all_observed. MEASURED: two
#     runs, identical code and corpus, section_rules.md identical at 433,260 bytes
#     with a different sha256, differing at 34 lines — one per subtopic. No diff
#     between two runs could separate a real regression from hash-seed noise.
#     FIX: sorted(set(...)). VERIFIED: all six artefacts now byte-stable across
#     PYTHONHASHSEED 1, 7 and 99.
#     THIS IS THE ONLY INTENDED ARTEFACT CHANGE IN THIS RELEASE — one list, sorted.
#
#   WHY FOUR AUDITORS WERE GREEN. bootstrap 48/48, audit_specs_ext 0, callgraph 0,
#   audit_deep 0, validate_framework_md clean, mutation at budget — all pass with
#   Step 5 unable to emit anything. They read the spec as TEXT or as an AST; not one
#   EXECUTES the synthesis path. D1 needs run_qv's value to reach print_qv; D2 needs
#   write_section_rules to call compute_section_axis_distribution; D4 needs two
#   processes. All three are runtime facts.
#   WORSE — AND THE REAL LESSON: spec_name_audit DID detect D2 and D3. `collections`
#   and `present_files` were both sitting in spec_name_audit_baseline.json under this
#   file, accepted as known-unbound, so the ratchet reported OK. An untyped baseline
#   cannot distinguish "legitimately bound elsewhere at runtime" from "guaranteed
#   NameError". Both entries are REMOVED in this release, and the baseline now
#   carries a typed reason per entry so neither can be re-frozen silently.
#   MECHANISM: audit_callgraph C12 (new, route-aware) fails the build on any name
#   CALLED from compiling python that is neither bound on its route nor declared
#   CLASS: T/J.
#
#   RE-RUN REQUIRED for every exam. Any exam that produced a section_rules.md after
#   2026-08-05 had its code path repaired IN-SESSION by the executing model, not by
#   this spec, and that artefact is not reproducible from the spec as written.
#
# v2.52.0 — 2026-08-16 — GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION.
#   MINOR bump: EMITTED ARTEFACT VALUES CHANGE. This is NOT disclosure-only — contrast
#   v2.51.0, which correctly declared "NO ARTEFACT CHANGES".
#   S3-2's inner body loop terminated only on a question start or a taxonomy heading. A
#   PYQSort position label is NEITHER (measured: is_taxonomy_heading fires on 0 of 60
#   labels), so the label was absorbed as a stem continuation and the OUTER loop's
#   cur_date_label branch became UNREACHABLE after the first question of each taxonomy
#   block. Every question inherited that block's FIRST exam position.
#   MEASURED (IIT_JAM_MATHEMATICS, 3 papers, declared A=90/B=30/C=60): bands read
#   150/17/13; is_msq 18 against 30; 179 of 180 stems carried embedded label text.
#   After the fix: 90/30/60 exact, is_msq 30, 0 pollution; held to 884/884 across the
#   full 22-paper corpus.
#   CONSEQUENCE: the v2.39 (GAP-2026-08-13-E) positional MSQ branch has NEVER fired as
#   designed on any exam — it consumes question_type, which consumes original_q_num.
#   WHY IT SURVIVED REVIEW: E-10 strip_variables already scrubbed date labels from
#   TEMPLATES, hiding the leak in the one artefact a reviewer inspects by eye, while
#   stem/stem_raw/original_q_num/question_type stayed corrupt. Same shape as
#   GAP-2026-08-15-BAREQ: producer and consumer shared one blind spot.
#   FIX: terminate the body loop at a position label, ABOVE the heading test, breaking
#   WITHOUT advancing i so the outer loop re-examines and owns the assignment —
#   cur_date_label keeps exactly ONE writer.
#   DEFECT-CLASS SWEEP: the raw literal r'\[\d{1,2}-' stood at THREE sites in this file
#   (E-1 is_shift_tag, the S3-2 outer loop, and the new terminator). bc.DATE_TAG_RE has
#   been the single definition since GAP-2026-07-26-001 and its own comment claims to
#   have replaced the S3-2 copy — IT HAD NOT. All three now delegate to the new
#   bc.is_position_label(); zero raw literals remain in this file.
#   NEW QV-16 (FAIL, non-halting): one distinct original_q_num per question per paper.
#   Vacuous PASS on a pre-v1.18 corpus. Verified against the real 884-question
#   IIT_JAM_MATHEMATICS artefact — PASS clean, FAIL on a defect-injected copy.
#   ALSO: bootstrap.py's fresh-corpus SESSION CLASS said FINAL, contradicting §S8-0b
#   L6782; the first live run therefore did a FULL read on session 1. Corrected to
#   NON-FINAL with re-decision at A1b. FINAL is retained for an UNREADABLE progress
#   file, which is a corrupt state rather than a fresh one.
#   RE-RUN REQUIRED for any exam sorted by PYQSort v1.18+ whose marking_scheme declares
#   more than one question_type; Step 6 must re-run after Step 5.
# v2.51.0 — 2026-08-16 — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION (SESSION-BUDGET LAW).
#   MINOR bump: a function signature changes, a section is added, a persisted key is
#   renamed, and the batch contract's READING changes. Reference incident:
#   IIT_JAM_MATHEMATICS, two consecutive sessions, 54 tool calls, ZERO of 22 papers
#   processed. Three independent stalls, each sufficient alone:
#     G-1/G-4 THE DOMINANT DEFECT IS NOT IN THE TRANSPORT CODE v2.50.0 REWROTE. The
#       framework budgets payload characters (INLINE_BUDGET_CHARS) and paper pacing
#       (BATCH_SIZE) and has never budgeted SPECIFICATION-READ COST or TOOL-CALL COUNT.
#       Measured: this file 8,850 lines / 504,240 B / ~126,060 tok, plus
#       Framework_DeliveryFooter — 556,834 B, ~139,208 tok, >=36 view calls, MANDATORY
#       before any work under SKILL Rule 2. 40 of session 1's 50 tool calls went to
#       reading the specification and the step stalled before its first productive
#       operation. New §S8-0b routes the READ SET by SESSION CLASS (FINAL vs NON-FINAL,
#       NOT fresh vs resume — routing on fresh/resume would leave session 1 of every
#       exam exactly as broken), with mandatory one-way escalation before synthesis.
#     G-2 THE PROBE WAS NEVER CHARGED. plan_transport computed the partition against
#       the full budget as though the probe were free: probe 107,968 + admitted paper
#       127,008 = 234,976 real chars against a 200,000 ceiling, printed as feasible.
#       plan_transport gains probe_consumed and passes it to bc.partition_by_transport,
#       which gains consumed=. Framework_PYQCore EC-P40.
#     G-3 THE PROBE PAPER WAS THE SMALLEST, SO ITS PAYLOAD WAS DISCARDED. Step 5's
#       admitted set is recency-first, so the smallest paper is almost never fetched.
#       New deviation P4f: probe admitted[0] — the paper the plan will fetch anyway.
#   Also: EC-P43 DIRECT EGRESS LANE tried FIRST (PHASE A/A0) — when the container can
#   reach Drive and the folder is link-shared, python fetches the bytes itself, EC-P36's
#   double charge disappears and the whole corpus fits one session; proven per exam on a
#   real paper, never assumed, never fatal. A1 now routes the listing through
#   corpus_io.write_drive_listing with an independently declared observed_count and
#   HARD STOPS on a short listing (EC-P41) — a partial listing is worse than an empty
#   one, which EC-P39 already caught. S8-1 restates BATCH_SIZE as a CEILING, not a
#   floor, reconciling it with EC-P37 which had already settled the question. S8-3's
#   template becomes variable-length. _meta._transport.papers_admitted is RENAMED
#   papers_planned (it is written before the acquisition loop, so it is a forecast, not
#   a fact) and gains session_log[] recording what each session actually consumed;
#   readers MUST tolerate the old key for one release per EC-P38.
#   NO ARTEFACT CHANGES. Every fix is additive, disclosure-only, or changes which paper
#   is fetched first. No exam re-runs any step — except an exam whose listing was
#   silently short, which now hard stops, which is the desired outcome.
````

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockTestAnalyse.md.

```
# v2.50.0 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (EXECUTION-
#   BOUNDARY LAW, Step 5). MINOR bump, not a patch: a function signature changes, a
#   section is added, a persisted schema key is added and two DoD items are added.
#   v2.49.1 was a patch release for a comment-only touch and its changelog called this
#   spec "the reference implementation"; nobody then re-read it against the new
#   contract, and its Drive lane was dead the whole time while four auditors reported
#   0 findings. FOUR defects, all measured on IIT_JAM_MATHEMATICS (22 papers):
#     D1 collect_drive_docx_recursive read results.get('items', []). The connector
#        returns {'files': [...]}. Engine: 22 papers; that line: []. And an empty
#        corpus was NOT loud here — the no-PYQ branch rewrote mode to '--synthesise
#        ALL', so a broken listing became "this exam has no past papers" and Step 5
#        shipped a complete, green, F2-footered deliverable of zero-PYQ scaffolds that
#        Steps 6 and 7 then built an entire paper from. Step 4 could only stall; THIS
#        STEP COULD PRODUCE A WRONG ANSWER. Now EC-P39: HARD STOP, never a fall-through.
#     D2 that walker called gdrive_search() — a CLASS T marker — from python and
#        consumed the result. Both call sites deleted; the walk is corpus_io's.
#     D3 run_batch_loop's drive_payloads had NO PRODUCER anywhere in the spec and
#        defaulted to {}, so every paper raised TransportFallback and the whole corpus
#        routed to manual upload. It now fails loudly, mirroring v2.39's vision_pending.
#     D4 no channel probe, no transport plan, no context budget, no persistence — in
#        the one step that is inherently multi-session. New §S8-0 TRANSPORT PREFLIGHT.
#   Step-5-specific deviations from PYQCount S5-0, because Step 4 is single-session and
#   Step 5 is batched: the inline budget is PER SESSION and a fresh chat resets it (so
#   the remainder is carried, never demanded as uploads); the budget is halved because
#   an inline payload is charged twice (inbound + re-emitted); the partition runs AFTER
#   sort_papers_recency_first (measured: listing order admits 2017/2021/2014 instead of
#   2026/2025/2024 and can leave §1-6 unreachable); and PYQCompress is excluded from the
#   remedy text — these papers are 213x UNDER the cap, the constraint is the channel.
#   ROOT CAUSE OF THE CI BLINDNESS: this file's CLASS T stubs sat in an untagged fence
#   spanning 321-603 that fails ast.parse at line 328 on an em-dash IN PROSE.
#   any_python_blocks() yields only compiling fences, so C6 built an empty stub set,
#   returned early, and never reached the two live violations in the fence next door
#   that compiles fine. The fence is now split; C6-PRE fails the build if any governed
#   spec ever hides a CLASS marker in a non-compiling fence again, and C9 fails the
#   build for a correctly-injected resolver whose container has no producer.
# v2.49.1 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (invariant
#   correction only; zero rule/functionality change). The CLASS T transport block
#   asserted that a Drive result "for any file of consequence is spilled to a JSON file
#   on disk rather than returned inline". MEASURED FALSE 2026-08-15: one 40,488-byte
#   sorted paper spilled to a file in one deployment and returned inline in another,
#   and the two spill directories differed. Delivery form is a property of the
#   DEPLOYMENT, not of the file size; both shapes are accepted and the channel is now
#   PROBED in Framework_PYQCount S5-0 (PYQCore EC-P35/EC-P36). This spec's resolver
#   bridge was already correct and is unchanged — it is the reference implementation
#   the PYQ counting path was missing for 20 days.
# v2.49.0 — 2026-08-15 — GAP-2026-08-15-BAREQ (F-1 mirror + F-2 primary).
#   E-2 Q_PATTERNS mirrors the engine's widened four-entry table: entries 3/4 are the
#   BARE-LABEL forms, for a stem paragraph whose whole payload is <m:oMath>, a drawing,
#   or nothing (PYQPrepare S1-4). p.text is <w:t>-only, so such a stem read as "Q.N",
#   entries 1/2 require whitespace AFTER the digits, and the question did not exist for
#   this step. Updated ATOMICALLY with blueprint_core, PYQSort S3-1 and PYQScan S3-2 —
#   engine-only patching turns audit_deep TABLE-PARITY red by design.
#   S3-2 extract_presorted (F-2, INDEPENDENT and broader): stem_parts[0] was built from
#   para.text and never passed through enrich_paragraph_with_omml(), which every
#   CONTINUATION line already used. So a stem paragraph's equation was silently dropped
#   from full_stem / 'stem' / 'stem_raw' / detect_is_msq / detect_blank_position / the
#   negative test / taxonomy keys / PYQ_STEM_PATTERNS and every mock derived from the
#   item. Measured on IIT_JAM_MATHEMATICS 12-Feb-2017: 46 of 60 stems (77%) lost part or
#   all of their maths, and an OMML-only stem extracted as ''. omml_present/omml_ok were
#   likewise seeded from the body loop alone, so QV-8 (OMML recovery) SKIPPED exactly
#   those questions (om == [] -> PASS). Both flags are now seeded from the stem.
# v2.48.2 — 2026-08-14 — S11-2 PART B FIXED FOR REAL + ONE ORDER EVERYWHERE
#   (GAP-2026-08-14-S11-2-PARTB-UNFIXED, primary; GAP-2026-08-14-DELIVERY-ORDER-
#   DRIFT, secondary; release-manager hold on 2026.08.13.6.) v2.48.1 claimed
#   "S11-2's download step now agrees" but S11-2 has TWO delivery sites and the
#   fix landed on PART C (future re-run note) while PART B — the operative
#   present_files list — still said "All 6", exam_config unconditional,
#   taxonomy.xlsx absent. Combined with v2.48.1's own NEVER-TRIM rule that
#   stale list turned into a hard stop on every normal run (taxonomy.xlsx
#   exists → Check 1 fires → STOP). PART B is now the same two-tier contract
#   as S11-3/checklist/QV[19], in the order the delivery code emits (rules →
#   manifest → xlsx → exam_config → taxonomy → progress → summary), and the
#   bare "All 6" count line is deleted — a bare count is what regenerated this
#   defect each time the set changed. S11-3's numbering is reconciled to that
#   same emission order (v2.48.1 had introduced a third order). The NEVER-TRIM
#   rule stays exactly as written — it is what made this visible. PERMANENT
#   GUARD: mock_sync_audit MS-11 now parses the delivery code's unconditional/
#   conditional sets and asserts all five prose sites (PART B, PART C, S11-3,
#   checklist expected, QV[19]) declare the same two sets — self-tested with
#   the v2.48.1 PART B text as the must-flag fixture. Emitted stamps stay
#   v2.48 (major.minor unchanged). Prose fences only; no python fence touched.
# v2.48.1 — 2026-08-14 — DELIVERY TIERS TOLD STRAIGHT + NEVER TRIM SILENTLY
#   (GAP-2026-08-13-DELIVERY-COUNT-DRIFT, residual layer; field report from a
#   live exam project). v2.47.1 moved exam_config.json to the checklist's
#   WHEN-IT-EXISTS tier, but three prose sites still said "the 6 mandatory
#   files" with exam_config listed among them — the same count-drift class one
#   layer down. S11-3's FINAL DELIVERY list now prints the SAME two tiers the
#   checklist enforces (5 mandatory; exam_config.json + taxonomy.xlsx when
#   they exist, which is every normal run); S11-2's download step and QV item
#   [19] now agree. NEW RULE in the pre-delivery checklist: a failed check is
#   a FINDING, never a trim — the run STOPS and reports the differing
#   filenames in chat; observed in the field: a generated taxonomy.xlsx held
#   back to satisfy a stale six-file reading, discovered only when the
#   operator asked. Emitted stamps stay v2.48 (major.minor unchanged).
# v2.48.0 — 2026-08-14 — TAXONOMY ORDER IS TEACHING ORDER
#   (GAP-2026-08-14-TAXONOMY-ORDER; owner decision of 2026-08-14). Two changes,
#   one rule:
#     (1) S5-3 write_taxonomy_xlsx no longer re-sorts rows alphabetically —
#         that resort silently DISCARDED the manifest's curated order, which
#         notes_core.assign_numbering has been freezing into the permanent
#         S/T/ST unit numbers all along (verified against delivered
#         filenames: syllabus order, not alphabet). Rows now emit in MANIFEST
#         ORDER with a new "Upload Order" column (E) and a How-to-use
#         instruction to upload to the portal top-to-bottom. Columns A-D are
#         unchanged in position and meaning, so every downstream "column D"
#         reference (Framework_NotesCreate section 0 among them) still holds.
#         The standalone converter manifest_to_taxonomy_xlsx.py is changed
#         identically in the same release — two writers, one behaviour.
#     (2) S5-3 gains the SUBTOPIC ORDERING RULE above write_subtopic_manifest:
#         first extraction of a NEW exam enters each topic's subtopics in
#         TEACHING order (syllabus order default, SME-adjusted); re-runs
#         APPEND new subtopics at the end of their topic, never mid-list; an
#         exam whose numbering is already persisted is NEVER reordered.
# v2.47.1 — 2026-08-13 — SYNC AUDIT ROUND 2: two more delivery-set fixes.
#   (1) exam_config.json moved from the unconditional to the WHEN-IT-EXISTS tier of
#   S11-3's expected set: the delivery code appends it only if generated and S-SECMAP
#   tolerates its absence with a WARN, so the unconditional listing made Check 1 forbid
#   delivery on runs the spec itself had blessed (the inverse of v2.47's taxonomy fix).
#   (2) write_section_rules' "# Generated by ..." comment stamp still said v2.23 (the
#   parseable framework_version field was fixed at v2.47; the comment was missed).
# v2.47.0 — 2026-08-13 — CROSS-STEP SYNC AUDIT FIXES (Steps 5→11 handshake audit)
#   Three desyncs found by a dedicated 3-pass producer↔consumer audit of the whole
#   Step 5 → TestDeliver chain, all fixed in this file:
#   1. GAP-2026-08-13-STALE-NAME-MATCH-RULE — S1-4's CROSS-STEP SUBTOPIC NAME RULE
#      still claimed "Step 7 matches subtopics by EXACT name" and prescribed re-running
#      Steps 5+6 on any rename. FALSE since MockTestCreate v3.4 (its SUBTOPIC_ID
#      CONTRACT section: joins are by subtopic_id ONLY; the display name is
#      decorative) — and contradicted by this
#      file's own §15 SUBTOPIC_ID CONTRACT. Rewritten to the id-based truth, keeping
#      the one obligation that IS real (a rename that changes the derived id still
#      requires re-running Step 5 AND Step 6 together).
#   2. GAP-2026-08-13-DELIVERY-COUNT-DRIFT — three sites disagreed on the final
#      deliverable count: DoD [19] said "EXACTLY 5" (predating BOTH the v2.24.9
#      exam_config 6th file and the v2.24 taxonomy.xlsx conditional 7th), S11-3's
#      closed list said "all 6", and the delivery code has appended taxonomy.xlsx
#      since v2.24 — so S11-3's own Check 2 ("no unexpected files") would veto the
#      code's own 7-file delivery. All sites now agree: 6 mandatory + taxonomy.xlsx
#      when written (= 7 on a normal run), with the expected set DERIVED from what
#      the code actually writes (the same v5.36 lesson Step 7's S13-7 learned).
#   3. Provenance stamp drift — section_rules framework_version and the manifest
#      generated_by stamps still said v2.22/v2.23. No consumer parses them (verified
#      by grep across Framework_Blueprint/MockTestCreate/blueprint_core/corpus_io —
#      Step 6's v2.22+ gate checks the per-entry `format` FIELD, never the stamp),
#      so severity was cosmetic-only; updated to v2.47 for honest provenance. NOTE:
#      this stamp-drift class has now recurred at least four times (v2.14/v2.15/
#      v2.17 fixed it before) — future version bumps must update these literals.
# v2.46.0 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v2.45.0 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v2.44.0 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: the exemption became the budget.
#   v2.26 replaced `has_img = any(...)` with a rate and then decided REDUCIBILITY
#   with a fresh any(). One question in a 22-year corpus made a subtopic permanently
#   exempt, and irreducible grants pass even over budget by design. First real
#   PYQExtract run: 21 of 133 subtopics exempt, 14.3 figures/mock against a budget
#   of 5, 13 of 15 mocks over. Reducibility is now rate-based (figural_rate >= 0.50
#   AND option_image_rate >= 0.50) -> 3 subtopics, 1.5 forced, 0 mocks over.
#   Figures are now SCHEDULED at measured frequency rather than forced at render
#   time, the audit band is the exam's own volatility, and per-mock targets follow
#   the exam's observed shape. No feasibility halt exists or is needed.
# v2.43.0 — 2026-08-06 — GAP-2026-08-06-DI: DI becomes measurable.
#   DI was the one budgeted Axis-1 stimulus class leaving NO trace anywhere, so
#   A-AXIS1 could only ever report it UNESTABLISHED. It cannot be recovered from the
#   docx: G-MATCH-TABLE mandates a real Word table for every MATCH question, so on a
#   real paper table-presence finds 3 candidates where exactly 1 is DI. Step 7 now
#   records di_manifests (the producer's own record) and asks the Axis-1 budget
#   before building a table stimulus; Step 5 emits di_rate/di_q_count/di_reducible.
#   Absent-safe: no di_manifest -> DI stays unestablished, exactly as before.
# v2.42.0 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v2.41.0 — 2026-08-05 — GAP-2026-08-05-001. S3-2 takes bc.sorted_body_lookahead(doc)
#   and the per-FILE colour probe. QV-1a severity WARN -> FAIL (SG-6): the identical
#   condition was a HARD STOP at Step 4 and a silent green footer here. QV-15 BODY
#   TERMINATION SANITY added (SG-7) with a NAT-specific colour assertion, since an
#   option-count threshold is meaningless for a question that has no options. New counter
#   questions_terminated_by_heading, reported even when 0.
# v2.40.0 — 2026-08-03 — DEFECT FIX: live cross-step contracts still named the retired
#   Step 8. The axis classifier's propagation contract read "MUST PROPAGATE (byte-identical)
#   to Step 8 MockCreateAudit S6-1b" — a binding instruction pointing at a spec deleted in
#   2026.08.03.5. The contract itself is UNCHANGED and still binding; its target is
#   restated as audit_canonical.py, which is where the verbatim classifier copy actually
#   lives and which Step 7 runs. Internal/canonical step map marks slots 3 and 5 RETIRED
#   without renumbering, so unlabelled internal step references keep their meanings.
#
# v2.39.2 — 2026-07-31 — §16 XLSX IMPLEMENTATION EXTRACTED to frequency_xlsx.py (repo
#   engine, hash-tracked). 664 lines of workbook code (aggregation, derived metrics,
#   generation, 5 sheet writers) moved byte-identically; §16 keeps the sheet spec (§16-3),
#   the 9-item validation checklist (§16-9) and the EC-F* edge cases (§16-10), each
#   subsection now naming the engine functions it governs. Call sites use
#   `import frequency_xlsx as fx`. Zero behavioural change.
# v2.39.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   1157 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestAnalyse'. The current companion block, the
#   v2.39 entry, and all structural notes remain in-file. Body byte-untouched.
# v2.39 — 2026-07-27 — GAP-2026-07-27: SIX DEFECTS FOUND BY SIX SESSIONS ON ONE CORPUS.
#     Six independent sessions ran Step 5 on IIT_JAM_BIOTECHNOLOGY (22 papers, 1,719 Qs).
#     FIVE rediscovered the same vision defect and each invented a DIFFERENT workaround;
#     the one session that executed these python fences VERBATIM found a P0 no other
#     session hit. Every earlier session had paraphrased the spec into hand-written
#     modules and, in paraphrasing, silently repaired a bug present here as written.
#     The lesson generalises past these six fixes: THIS SPEC WAS LESS CORRECT THAN ANY
#     IMPLEMENTATION OF IT THAT HAD EVER SHIPPED, and its defects were invisible in
#     exact proportion to how competently it was reimplemented.
#
#     A — TAXONOMY SOURCE-2 CONCATENATED INSTEAD OF MERGING (P0). The Source-2 append
#         was unguarded while Source 1 was guarded, so the stated contract — "merged,
#         Analysis docs win for names" — held in NEITHER half. MEASURED: 260 subtopic
#         blocks for 134 distinct ids; 126 emitted TWICE (the 8 singletons are zero-PYQ
#         scaffolds, which enter through the guarded path). mint_subtopic_ids() could
#         not recover: its `_2` disambiguator fires only when the KEY differs, and these
#         keys were identical, so both copies took one id and QV-13 refused the run.
#         The 126 duplicate blocks were verified BYTE-IDENTICAL — a delivery blocker,
#         not content corruption.
#         FIXED: real merge; renames carried into progress keys by apply_taxonomy_renames()
#         (the lookup key includes topic, so a rename not propagated would silently
#         orphan every question under it); _dedupe_analysis_docs() by realpath + SHA-256,
#         applied at BOTH call sites — the S1-4 one was never reported and inflated the
#         subtopic count shown to the operator; RuntimeError from the v2.31 lock gate no
#         longer swallowed by `except Exception: pass` (the gate was armed and disarmed
#         six lines apart); new QV-13b HARD STOP pre-mint, so the failure is attributed
#         to the MERGE rather than surfacing as an opaque id collision — which is what
#         sent six sessions to inspect the one function behaving correctly.
#
#     B — build_vision_queue() OVERWROTE, AND WAS CALLED PER PAPER (P0). It writes
#         vision_queue.json and vision_sheet_NNN.png, both FIXED names, and never read
#         an existing queue; the sole call site sat inside process_pyq_paper(), writing
#         into a workdir S4-2a defines as one-per-RUN. Only a batch's LAST paper reached
#         Phase B. MEASURED: 153 figural questions across 22 papers, _meta.vision
#         recorded queued=8; batch 7 queued 24 and 3 survived. The stated Phase A
#         invariant was violated in the OPPOSITE direction — sheets existed that no
#         queue referenced.
#         FIXED, both halves: the call is HOISTED to the batch boundary (candidates
#         accumulate in a run-level list; a missing accumulator RAISES rather than
#         silently dropping figures), and corpus_io v1.9 makes the write IDEMPOTENT by
#         unioning with the on-disk queue. Hoisting alone still loses prior sessions;
#         idempotence alone still loses papers 1..N-1 within a batch.
#
#     D — XLSX-F9 COMPARED A CORPUS TOTAL TO A PER-PAPER DENOMINATOR (P1).
#         exam_total_all is one paper's size (60); mapped_total is the corpus sum
#         (1,719). The gate fired on EVERY multi-paper corpus ever run, and printed
#         `60 - 1719` as a count of unclassified questions: "-1659 questions were not
#         classified to any subtopic." Not merely wrong — INVERTED. A gate that cannot
#         fire correctly trains operators to ignore gates.
#         FIXED: denominator is papers_processed x total_questions, taken from
#         counting_progress so --frequency-scope current-era counts only its own papers;
#         a negative shortfall is guarded and reported as a SURPLUS, which is legitimately
#         reachable on an era-mixed corpus.
#
#     E — MSQ UNDER-DETECTION ORIGINATES IN STEP 3 (P2). MEASURED: 24 MSQ across 1,719
#         questions against a marking scheme reserving Q31-40 (~10/paper). Not a weak
#         regex — CROSS-STEP INFORMATION DESTRUCTION: PYQSort renumbers into taxonomy
#         order, so the positions identifying the MSQ band are gone before Step 5 reads
#         the paper. Step 5 cannot recover what Step 3 discarded.
#         FIXED at the source: PYQSort v1.18 stamps the original position into the date
#         label (OPTIONAL field — pre-v1.18 files parse unchanged, no re-sort forced);
#         this spec retains the label instead of skipping it and gains a positional
#         branch. The EC-A option-shape guard keeps HIGHEST precedence, so a paper that
#         deviates from its own declared scheme is not mis-typed. Codec lives in
#         corpus_io Cluster Q — one writer, one reader, one definition — because a
#         format defined in two specs is exactly the drift v2.36 had to unwind.
#         Also persists original_q_num + question_type, arming classify_paper_era()'s
#         type-corroboration branch (GAP-X residual: type_checked was False on all 22
#         reference papers, so era rested on question COUNT alone).
#
#     F — NAT SATURATED AXIS-2 FILL_BLANK (P2). Ladder rule 5 fired on the answer-entry
#         blank every NAT question carries. MEASURED: 218 of 261 NAT (83.5%) against 37
#         of 1,434 MCQ (2.6%) — 32x enrichment tracking the ANSWER MECHANISM, not the
#         question form. Control: across 300 legacy-era questions, which carry almost no
#         NAT, FILL_BLANK moved by exactly 1. The axes are orthogonal so nothing was
#         corrupted, but Section C's Axis-2 profile read ~100% cloze and Step 7 rendering
#         that literally emits NAT stems as fill-in-the-blank.
#         FIXED: rule 5 gated on the question having options. Verified against the live
#         corpus: 255 -> 37, all 218 reclassified are NAT, zero MCQ/MSQ touched.
#
#     H — RESUME PRECEDENCE SILENTLY DISCARDED A BATCH (P3 -> P1 on operator evidence).
#         load_progress() returned the FIRST existing path with /mnt/project/ first and
#         the live session's outputs LAST, so a mid-run reload reverted to stale state.
#         The documented workflow — download the output, re-upload to project knowledge —
#         makes stale-project-copy the NORMAL state, not an edge case; one session lost a
#         completed 3-paper batch this way.
#         FIXED: directory order cannot express the rule, because which copy is freshest
#         depends on cold-start vs mid-run and this function cannot know which. It no
#         longer guesses: it reads every candidate and takes the most advanced by
#         papers_processed — correct in BOTH cases, no mode flag — and REPORTS divergence.
#
#     NOT FIXED HERE, TRACKED: GAP-C (Phase B degradation has no cross-session
#     persistence contract — the queue lives in an ephemeral workdir, so six sessions of
#     observation produced a 46%-complete figural record) and GAP-G (no defined delivery
#     behaviour when the closed six-file set is written but DoD reports FAIL).
#
```

Entry v2.60.0 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v2.61.0 supersedes).

```
# v2.60.0 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY Part C (paired with analyse_engine
#   v1.3, blueprint_core v1.32, figure_types v1.3, PYQExplain v2.27, Blueprint v1.64.0,
#   MockTestCreate v5.92, audit_canonical v2.37). The Step-5 <-> profile JOIN is paper + Row
#   q-number first (analyse_engine.profile_record_for; the 60-character stem key collapsed
#   every "Identify the major product, P ..." item to AMBIGUOUS — DL-25), then the stem key,
#   then a figure hash; the join rate and the DL-20 profile coverage line are printed.
#   Questions carry their MINTED subtopic_id (stamp_question_subtopic_ids, DL-29) so the
#   figural quota is measured per subtopic (Create guards it with bc.figural_quota_guard, G6).
#   The exemplar bank: an exemplar's band is its LEVEL band when the Level Model is active
#   (bc.level_bands over the window — the ONE builder bc.level_model_for_scope; the measured
#   mix keeps the stored band), rows carry structures / option SMILES / the derived key / the
#   vector, stems are kept to 1,200 characters and never cut inside a list block, image
#   options are their SMILES, Hard leaves are ranked by typicality, newest first by ISO
#   date, and the size cap is a per-section budget (DL-23/24/26/27). Every QUALITY block
#   gains figure_complexity_pct {field: {p10,p50,p90}}, closeness_pct and ask_format_shares
#   (indented, never a line starting subtopic_id:), each stamped `rule.<key>: q2` (G5 — a
#   QQ FAIL resting on a new key is WARN for this release cycle). The distractor mix is
#   MEASURED from the profile's closeness records when they exist (existing S9 tokens),
#   else the prior with `distractor_mix_source: default prior (unmeasured)` and an AMBER
#   line (DL-23). The structure-option prior keys on the figure family (DL-04 leak). Run
#   files are found under /mnt/project then /mnt/user-data/uploads (DL-30). Nothing here
#   stops; a project without content records is byte-identical except the new QUALITY keys.
```

## Framework_MockTestCreate.md

Entries v5.54.1–v5.92 moved at framework release 2026.11.06 (EC-P42; v5.93 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the Step 7 route is read against a measured session budget).
Current-version entry remains in Framework_MockTestCreate.md.

```
# v5.92 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY (paired with blueprint_core v1.32,
#   audit_canonical v2.37, paper_pipeline v5.40, figure_types v1.3, Framework_PYQExplain
#   v2.27, MockTestAnalyse v2.60.0, Blueprint v1.64.0, ScopedBlueprint v1.14.0, MockReview
#   v2.0.1, MockTestExplain v1.53.0, MockDeliver v1.26.0, DeliveryFooter v1.40.0; STEP_
#   CONTRACTS override floors raised under owner decision D8). Raised by CSIR_NET_
#   CHEMICALSCIENCES TestCreate SUBJ Organic Chemistry Test 01 (2026-11-03): 40/40 correct,
#   far below the real paper — its "Hard" items were one-step textbook reactions while the
#   real Hard items (Dec-2025 Q95/Q114, Jul-2026 Q88/Q116) carry polycyclic stereodefined
#   substrates and options differing only in stereo / regiochemistry. Root cause: no step
#   defined what a band MEANS for the subject; the labels never bound to the content, and
#   every control failed open (dormant judge echoed the plan; CCP floor dormant and
#   lower-only; footer green). OWNER DECISIONS (2026-11-04/05), binding: D1 the ground
#   truth for a past question's band is its COMPLEXITY RANKING within its own exam; D2 a
#   subject test is written to the measured tier mix; D3 produce Hard exactly as the
#   blueprint writes it, with D3-R5 (a): after the 6 tries an item ships at its measured
#   band, the schedule is amended and the footer counts the miss; D4 no certification
#   gating and no manual review; F1 the graphics-team Row docx is the figure source; F2 no
#   official answer key, ever; P1 PYQPrepare untouched; D6/D7 one release, every exam;
#   D8 override floors raised; D9 this release = drawn chemistry + estate-wide guards (the
#   non-chemistry figure families are a follow-up GAP); D10 (B) LEVEL_MIN_POOL 12 with a
#   small-pool footer line; D11 (A) judge-vs-level disagreement on a Hard slot spends one
#   extra RETRY inside the same budget; D12 (A) staged build, one bundle.
#   WHAT CHANGES HERE. S3: the LEVEL MODEL (bc.level_model_for_scope — ONE builder shared
#   with Step 5 and the auditor) and the read-time method lexicon are built beside
#   CCP_MODEL; the profile coverage line prints; DIFFICULTY_STATE (judge-dormant items,
#   Hard misses, level items) is persisted with batch_state and 'difficulty_schedule_
#   original' is kept beside the amended plan (DL-42/51). S3-2e: readiness measures the
#   content floor instead of trusting field presence (DL-46). CHECK 3c: authoring under
#   rubric r2 (inferential MOVES by bc.INFERENTIAL_STEP_RULE, quoted verbatim; obs stamped
#   rubric_rule 'r2' — guard G1); for an item carrying drawn chemistry the band is the
#   LEVEL band (bc.level_record: composite at full precision, qtype-clamped) and a
#   below / above measurement is exactly a G-DIFF RETRY toward the slot band with an
#   escalating brief (DL-41, D3-R5) — ONE budget, bc.MAX_DIFF_TRIES_DEFAULT; the blind
#   judge is advisory for a level item (level_note; D11 (A) one extra retry on a Hard
#   slot) and DORMANT on a figural-chemistry snippet fallback (DL-37: decision stays
#   agree, level_note 'unverified', footer AMBER); g_diff_gate runs only when a plan
#   exists (DL-39); R2 gains complexity-below-p10 / closeness-below-target reject reasons
#   (DL-47); R4' simplifies layout only and re-measures the vector (DL-43/58); a two-row
#   option layout is tried before R4' on width overflow (DL-48); R5 counts a Hard miss
#   (D3-R5 (a)). S13-2G phase 3 compares the reviewer's band with the slot band (DL-52;
#   the packet still carries no band). S13-6: AMBER lines from bc.difficulty_unverified_
#   lines (`DIFFICULTY UNVERIFIED — <reason>`, `Hard target missed: k item(s)`, coverage,
#   small pool) — informational; the two-file contract is unchanged (STEP_CONTRACTS).
#   figural_reducible defaults False for chem_structure / chem_scheme families (DL-50);
#   S3-12e places top-band slots by the blueprint's measured subtopic share (bc.band_
#   subtopic_plan, DL-33) and prints the ask-format floors (DL-34); S7-NEW-B withdraws a
#   figural quota below the A-AXIS1 band low (bc.figural_quota_guard, DL-29 / G6).
#   No new run-stop of any class, no CONFIRM, no deliverable, end state or user action (guards S1-S13).
# v5.91 — 2026-11-04 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE (paired with blueprint_core v1.31,
#   audit_canonical v2.36, final_assembly v1.13, Framework_MockReview v2.0.0 (internal brief),
#   Framework_MockDeliver v1.25.0, Framework_DeliveryFooter v1.39.0, NEW STEP_CONTRACTS.json +
#   LAW_REGISTRY STEP-CONTRACT-LAW). Release 2026.11.03 broke the Step 7 user contract for
#   every exam project (incident 2026-11-04, SSC GD Tier 1, TestCreate P2, 50 reasoning MCQs):
#   (1) Final Assembly ENDED at AWAITING_REVIEW and handed the owner a review packet to run in
#   a new chat, a verdict file to carry back and a --resume to type; (2) A-TEMPLATE fell back
#   to a cap of 2 repeats per template on every project without measured caps — infeasible
#   for any real paper (a reasoning family has 8 ask types) — so 35 of 50 items were stamped
#   UNRESOLVED and the paper NOT CERTIFIED. OWNER DECISIONS 2026-11-04, binding:
#   D0 — OD-5 RESTATED: the independent review is mandatory and runs INSIDE the run; it is
#     never a user step, never ends Step 7, never creates a user-visible file. OD-9 RESTATED:
#     NOT CERTIFIED only from an ACTIVE, MEASURED gate. D1 — no sub-agent in the runtime (or a
#     part fails twice): same-session cold review, disclosed; NOT_RUN only if even that fails
#     (A-REVIEW WARN). D2 — the MockReview / TestReview triggers are retired; Framework_
#     MockReview is the internal reviewer brief, routed with this step. D3 — no third file:
#     the repo auditor and an amended blueprint are never delivered (informational footer
#     lines). D4 — reviewer isolation by instruction accepted. D5 — Deliver re-certifies a
#     paper whose only UNRESOLVED findings come from dormant controls. D6 — STEP-CONTRACT-LAW.
#   CHANGES: S13-2F no longer ends the step; S13-2G is an IN-SESSION review (phase 1 packet
#   under /home/claude only; phase 2 one fresh sub-agent per <= 30-item part, a passage group
#   never split; phase 3 automatic bind / repair / round 2) and continues to S13-3 .. S13-8 in
#   the same response; S4-12 continues REVIEW_RUNNING / REVIEW_REPAIR / legacy AWAITING_REVIEW
#   internally on "continue" (a legacy verdict file is found by CONTENT); S13-2F stamps
#   ladder.terminal_sweep (the only R4 exemption A-TEMPLATE honours); S13-6 has NO conditional
#   additions; S13-7 clears this run's leftovers from outputs (fa.outputs_to_clear) before the
#   checklist; S13-8 judges fa.delivery_scope. Auditor: A-TEMPLATE counts per (subtopic,
#   fingerprint) against that subtopic's MEASURED cap, never a default (unmeasured -> not
#   checked; nothing measured -> DORMANT; infeasible -> reported, never FAIL); a readiness
#   record showing G-TEMPLATE not PASS makes the FINGERPRINT caps DORMANT (every other gate
#   is unchanged from 2026.11.03); S13-2F clears 2026.11.03 default-cap stamps; per-batch
#   audits report the same level as the pre-commit sweep. Contract (STEP_CONTRACTS.json):
#   the final batch's response ends with EXACTLY [ExamCode]_[slug]_Create.docx +
#   [ExamCode]_registry.json; the only user action is "continue" between batches.
# v5.90 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (paired with blueprint_core
#   v1.30 Cluster QQ, corpus_io v1.18, figural_core v5.90, figure_types v1.2, analyse_engine
#   v1.2, audit_canonical v2.35, final_assembly v1.12, Framework_MockTestAnalyse v2.59,
#   Framework_PYQExplain v2.26, Framework_Blueprint v1.63.0, Framework_ScopedBlueprint v1.13.0,
#   Framework_MockDeliver v1.24.0, Framework_DeliveryFooter v1.38.0, NEW Framework_MockReview
#   v1.0.0). Estate-wide, exam-agnostic; the CSIR-NET Organic Test 01 paper (40 items, all keys
#   right, quality far below the real paper) is the incident, not the scope. OWNER DECISIONS
#   2026-11-03, binding: OD-1 NEVER A STOP — a missing quality input is PRINTED (S3-2e
#   readiness block) and RECORDED, nothing more; OD-2 entity reuse hard for molecules /
#   values, text calibrated (R3.8); OD-3 naming the tested reaction / drawn substrate banned
#   unless the cell's PYQ rate >= 10 %; OD-4 the EXISTING difficulty tolerance and R5
#   amend-in-place mechanism are kept — only WHO MEASURES changes (judge + content floor,
#   never the author's counts); OD-5 INDEPENDENT REVIEW mandatory on every paper, two-session
#   protocol (S13-2G AWAITING_REVIEW -> MockReview in a fresh chat -> --resume repairs);
#   OD-6 shape FLOORS AND CAPS; OD-7 longest-key 1.5x hard, suspended only by MEASURED PYQ
#   rate; OD-8 layout / drawing style out of scope; OD-9 a finding that survives R5 ->
#   quality_status UNRESOLVED, paper NOT CERTIFIED, Deliver refuses without
#   --accept-uncertified (never a stop); OD-10 new gates HARD only for papers whose
#   producer_release >= 2026.11.03 (older papers AMBER), bp_refresh is additive; OD-11
#   exemplar bank is a DELIVERED RUN FILE, absent -> judge DORMANT; OD-12 the 60 % Hard
#   target stays; OD-13 G-MEDIAREUSE at commit + validator law; OD-14 Step-9 difficulty_gate
#   stays MOCK-only (the Create-side judge runs on scoped papers); Q-A G-STEREODECL yes.
#   WHAT CHANGES: S2-2 R3/R4/R5 now NAME their engine functions (they were prose with no code
#   behind them); S3-2e QUALITY READINESS; S3-12d SHAPE PLAN; S7 authoring records
#   (stereo_declared per structure, distractor_mechanisms + pathway MANDATORY, entities[],
#   named_entities, stem_agents, class_word, stated_formula, scheme_annotations, trailing /
#   asked placeholders, shape, fingerprint, pattern_key) and CHECK 3c's judge now reads the
#   EXEMPLAR BANK through bc.build_judge_input (author fields stripped); S10-8 render-time
#   G-OPTDISTINCT / G-STEREODECL; S4-11 gains eleven must-PASS quality items; §Q8b-LADDER
#   gains sub-rungs R2s / R2o; S13-2F stamps quality_status and writes certificate schema 2;
#   S13-2G REVIEW HANDOFF + --resume; S13-4 producer_release; footer DEGRADED / uncertified.
#   RELEASE REVIEW (2026-11-03, cold read — every item verified in code): (1) S13-2G phases
#   1 and 3 RELOAD batch_state from disk (a --resume session never ran S3-16); phase 3
#   persists review_defects / uncertified_items; round 2 always carries the WHOLE paper
#   and is the last round (< 2). (2) S7-QUALITY `shape` is the BARE ask type (the plan /
#   target key); `scheme_grammar` is its own field; stem_text / option_texts /
#   figure_files are recorded so the review packet is self-contained. (3) S3-12d reads a
#   FROZEN plan on resume and records G-SHAPEMIX STALE on the readiness record when this
#   paper has no targets (bc.readiness_mark); S3-16 persists quality_readiness + shape_plan
#   (no bare batch_state write before the initialiser). (4) S13-2F's _qq_gates includes the
#   paper-level item gates (A-SHAPEMIX / A-TEMPLATE / A-QUALITYSTATUS); the auditor itself
#   is precommit-tolerant of unstamped items and reconciles UNRESOLVED-only FAILs to WARN
#   (OD-9), so a NOT CERTIFIED paper never dead-ends at sweep 4 or at S13-4c. (5) S13-4c
#   passes --key and --fig-manifest (the certified sweep's own inputs) and commit_registry
#   receives quality_readiness. (6) S2-2 R1 / R2 name their engines (MS-26 i).
# v5.89 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (paired with figural_core
#   v5.89, corpus_io v1.17, blueprint_core v1.29, figure_types v1.1, analyse_engine v1.1,
#   audit_canonical v2.34, final_assembly v1.11, Framework_ScopedBlueprint v1.12.0,
#   Framework_Blueprint v1.62.0, Framework_MockTestAnalyse v2.58.0, Framework_PYQExplain v2.25,
#   Framework_MockTestExplain v1.52.0, Framework_DeliveryFooter v1.37.0). Estate-wide and
#   exam-agnostic; the CSIR Organic paper is the incident, not the scope. Owner decisions
#   2026-11-02: one release; O1 monochrome structures; O2 MARK-IFF-NAMED; O3 '+30% harder'
#   kept as the default, applied to the SCOPE mix positionally; O4 never drop / ladder; O5
#   NOT adopted — the label-then-picture SHAPE is kept and bound by keep_with_next instead;
#   O6 PYQ structure transcription; O7 audit with the repo copy when the project has none;
#   plus difficulty anchored for EVERY exam (independent blind rating against the exam's
#   own past questions), style measured for EVERY figure type, content measure as a floor.
#   (1) S3-2S: drawing style from FIGURE_STYLE_PROFILE (Step 5) -> print-true native
#   structure tokens TOK per role; S10-7C C1/C8/C9 rewritten (monochrome default, natural
#   size, one bond length, abbreviations only as the exam abbreviates, highlight bands
#   retired). (2) Q7b.8 amended (chemistry exempt) + Q7b.8' MARK-IFF-NAMED (G-FIGMARK).
#   (3) S10-8 KEEP INVARIANT: every option label kept with its picture (gap report: 25 of 108
#   labels stranded, in 25 of 27 questions; re-measured 19 of 108 before, 0 after, LibreOffice PDF). (4) §Q8b-LADDER: every
#   item defect is repaired in place (R1-R5); 49 quality run-stops converted ([HS:LADDER]);
#   every remaining "HARD STOP" carries [HS:INFRA] / [HS:INPUT] / [HS:PROSE]; G-ALTGROUP /
#   G-GROUPMANDATE / G-MINCOUNT repair instead of exit; the text fallback (R4) is used only
#   when the paper keeps its Axis-1 budget (else R4'). (5) S13-2F pre-commit item sweep +
#   certificate; S13-4c confirms (A-CERT); AMBER advisories no longer stop a run. (6) S3-1
#   P3: no project auditor -> the verified repo copy audits and is delivered. (7) S3-2D:
#   the difficulty schedule is recomputed from its provenance and the in-run blueprint is
#   amended + delivered (P2). (8) CHECK 3c: independent blind rating + content floor decide
#   the band; A-CONTENTLEVEL. (9) ask-type apportionment (F8). Full text: GAP document.
# v5.88 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (paired with
#   figure_types v1.0, corpus_io v1.16, paper_pipeline v5.40, final_assembly v1.10,
#   audit_canonical v2.33, blueprint_core v1.28, Framework_ScopedBlueprint v1.11.0,
#   Framework_Blueprint v1.61.0). Estate-wide; the reference exam (CSIR_NET_CHEMICALSCIENCES)
#   is the incident, not the scope. Measured: a delivered scoped paper with 36 figural
#   questions shipped exit_0/SHIP with every problem figure a lone molecule where the real
#   paper draws a reaction SCHEME (20 of 24 figural organic questions on 07-Jun-2023), and
#   with NO figure record in the registry; across the registry 385 questions were labelled
#   'reaction_scheme' while 287 of them held a STRUCTURE semantic object and 44 'REACTION'
#   objects held no reaction SMILES at all. Three root causes, three laws (LAW_REGISTRY.json):
#   F1 FIGURE-TYPE-COVERAGE — a vocabulary bound to a capability. figure_types.FIGURE_TYPES
#      binds every object_type to a render class, a semantic kind and a renderer. S7-NEW-B
#      dispatches a figure BY ITS REGISTRY ROW; "never record a type whose row was not the
#      one that rendered the figure". REACTION figures render through the NEW compositor
#      corpus_io.render_scheme (substrate → arrow carrying reagents/conditions → product or
#      placeholder; G1–G10 grammar) — the kind that S7-NEW-B2 mandated to a single-molecule
#      renderer that rejected it. NEW S3-17c FIGURE-TYPE SESSION PRE-FLIGHT (HS-17): this
#      paper's dominant types must be renderable BY THIS SESSION before Q.1 (rdkit absent →
#      one operator action, the pip line — never a traceback at Q.14). S10-7 Q5 states that
#      reagent/condition text over an arrow is INTRINSIC figure content.
#   F2 FIGURE-RECORD-INTEGRITY — the record agrees with itself. object_type is recorded for
#      EVERY rendered figure (S7-NEW-B; final_assembly refuses a commit without it); a
#      REACTION canonical must contain '>>' (paper_pipeline v5.40); NEW gate G-FIGTYPE-KIND
#      (S4-11) / A-FIGTYPE-KIND (auditor): label ↔ semantic kind ↔ FigureSpec class must name
#      one registry row — a mismatch is a FAIL, a false record; S4-7 STEP B passes
#      --fig-manifest so the gate is armed per batch, not only at S13-4c.
#   F3 MANIFEST-COMMIT — the record is committed because it EXISTS. S13-4 no longer gates
#      the rc/di/figural manifest on passage/di/figural_present (final_assembly v1.10 commits
#      on existence and records any flag disagreement in registry.paper_flags); S3-2a
#      HS-15a is SELF-CORRECTING (a false flag beside FIGURAL allocations is set True in
#      session, printed, and S3-18 / S4-5 CHECK 5 then run); S13-4c REQUIRES armed
#      A-FIGPROFILE and A-FIGTYPE-KIND lines on a figural paper (dormant = HARD STOP [HS:PROSE], the
#      A-QINDEX precedent); S13-REGCHECK runs fa.annotate_legacy_figure_records (forward-
#      only migration — legacy records are annotated, never rewritten, and the footer
#      discloses them).
# v5.87 — 2026-10-27 — GAP-2026-10-27-SCOPED-STIMULUS-SECTIONS (spec only; no engine change).
#   S3-12b's SAFETY-LOCK validation passed section_names = the SELECTED blueprint's
#   sections. The stimulus profile is exam-wide, so on a SCOPED paper (SUBJ/TOPIC/
#   SUBTOPIC) of a multi-section exam every set type belonging to another section was
#   reported "not a section of this exam" and Step 7 HARD STOPPED [HS:PROSE] before Q.1 — with a
#   remedy (re-run PYQExtract --stimulus-profile) that could never clear it. Measured:
#   SSC_CGL_TIER1 `TestCreate P1 --level subject --scope "English Comprehension"`
#   stopped on gir.analogy / gir.classification / qa.statistics_data_interpretation.
#   FIX: section_names is now the exam's section set, taken from the Step-5 subtopic
#   manifest (MANIFEST_IDS[*].section, already loaded and required at S3-8) united with
#   the blueprint's own sections. A renamed section is still caught. Set composition is
#   unchanged: bc.compose_stimulus_groups already uses only the types of the section
#   being placed. Mock papers: identical behaviour.
# v5.86 — 2026-10-09 — GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC (paired with audit_canonical
#   v2.31, final_assembly v1.8, MockTestExplain v1.51.1). The registry is SHARED by every
#   series (MOCK / SUBJ / TOPIC / SUBTOPIC) and every paper size; several places assumed every
#   paper was the size and series of the one being built. Measured: the first 40-Q scoped
#   paper (CSIR_NET_MATHEMATICAL_SCIENCES SUBJ:UNIT 1:01) built after 20 explained 120-Q mocks
#   HARD STOPPED [HS:PROSE] at S13-2 on A-DGATE — MOCK:M13's legal DISCLOSED verdict (bands = 120) was
#   checked against this paper's 40. Fixed in the engines, for every exam and paper type:
#   (1) A-DGATE checks each difficulty_gate record against ITS OWN paper's size;
#   (2) A-DPROFILE certifies the exam-level difficulty profile on its own terms beside a
#   SCOPED blueprint (it failed every scoped paper of an exam holding a profile, batch 1);
#   (3) A-DUP compares a not-yet-committed paper with ALL registry stems (it hid the
#   previous paper's last stems on every batch run and at S13-2); (4) rc/di/figural
#   manifests are written (S13-4) and read (auditor, Step 9) by paper_id, never the bare
#   ordinal; (5) a RESUMED scoped series (ordinal 1 = paper :11) no longer erases paper :01
#   from papers_completed / question_index / session_log at S13-4, nor is it flagged as a
#   duplicate at S13-REGCHECK; (6) a --profile path to an absent (optional) profile no
#   longer crashes the auditor; (7) the FINAL batch's STEP B (whole paper, no --through-q)
#   no longer FAILs A-QINDEX before S13-4 has written the index (dormant until the paper is
#   committed; the S13-4c tripwire now refuses a dormant A-QINDEX). Spec changes here: S3-1 the per-exam auditor is refreshed
#   from the verified clone whenever it DIFFERS from audit_canonical.py (the v5.85 marker
#   test is satisfied by every pre-v5.86 copy, so a fix would never reach a project); S3-2
#   records BP_SRC_PATH, the file the chosen blueprint came from, and S4-7 STEP B / S13-4c
#   pass it as --blueprint (both hard-coded the MOCK blueprint, so a scoped paper was
#   audited against the mock's size, sections and subtopics). Mock-only behaviour unchanged.
# v5.85 — 2026-09-21 — GAP-2026-09-21-LINKED-PLACEMENT (paired with MockTestAnalyse v2.57.2,
#   blueprint_core Cluster SG, audit_canonical v2.30, final_assembly v1.7). Question SETS
#   (RC passage, cloze paragraph, DI table, puzzle) are now placed as ONE block of
#   consecutive questions with ONE shared stimulus. Before this release every exam
#   scattered them (measured: SSC_CGL_TIER2 Mock 13 printed one RC passage at nine
#   positions and asked cloze blanks 5,3,...,1) because the only set path read a
#   manifest field Step 5 never writes. S3-12b: a NEW paper reads
#   [ExamCode]_stimulus_profile.json (written by PYQExtract --stimulus-profile or by final synthesis);
#   SAFETY LOCK — no profile, HARD STOP [HS:PROSE] before Q.1; bc.compose_stimulus_groups splits the
#   blueprint's EXISTING allocation into sets (never a re-allocation) and
#   bc.place_with_stimulus_groups places each set where the past papers place it (D-B);
#   the plan is frozen in batch_state['stimulus_groups'] with the profile SNAPSHOT it was
#   built from (audits read the snapshot, which also carries the paper's own blueprint
#   entry — right for scoped papers). A paper already in progress — plan persisted
#   without that key, OR questions authored in its first unfinished batch — finishes on
#   the legacy path, byte-for-byte. A set-placed paper whose batch_state lost its plan
#   is rebuilt deterministically and PROVEN against every authored question (HARD STOP [HS:PROSE]
#   on any disagreement).
#   NEW S7-STIMGROUP (R-STIMGROUP + stim_register): one stimulus per set, reused
#   verbatim across batch boundaries; cloze blanks asked in order. S7-NEW-A writes
#   concept_map[q].stimulus_group_id on set-placed papers only. Audit invocations pass
#   --stimulus-profile (the snapshot); a stale project auditor is replaced for the run by the verified
#   audit_canonical.py; S13-4c refuses a set-placed paper whose A-BLOCK line is absent
#   or dormant. New checklist item G-BLOCK.
# v5.84 — 2026-09-14 — GAP-2026-09-14-REGISTRY-SOURCE (REGISTRY-SOURCE-LAW; owner decision
#   2026-09-14; paired with MockTestExplain v1.51.0, MockDeliver v1.22.0, DeliveryFooter,
#   paper_pipeline CLUSTER RS). [ExamCode]_registry.json is REQUIRED by this step but it
#   no longer has to sit in Project Files: it is lawful in EITHER lane — (1) attached to
#   the trigger in chat, (2) Project Files — and S3-1 resolves it through
#   pp.resolve_registry (the ONE implementation Steps 7/9/11 share). Attachment WINS when
#   both lanes hold a file (a difference is PRINTED, never a stop); HARD STOP [HS:PROSE] only when
#   BOTH lanes are empty; exact filename + registry.exam_code == [ExamCode] are validated
#   on the way in; the run PINS the fingerprint it started from (batch_state.registry_pin,
#   S3-16) and S3-1 refuses a DIFFERENT registry on any later turn (pp.registry_source_check
#   — dedup state would be corrupted mid-run). S13-8 takes the handoff fingerprint from the
#   resolved source, not from a hardcoded Files path. Nothing about the writers, dedup,
#   gates, the closed delivery set or any artefact changes — only WHERE the file is read.
#   Enforced by LAW_REGISTRY REGISTRY-SOURCE-LAW + mock_sync_audit MS-20 (no spec may open
#   /mnt/project/[ExamCode]_registry.json directly).
# v5.83 — 2026-09-03 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE C: NEW-content generation (S7-NEWGEN, donor hierarchy, L4 firewall, difficulty layers)
# v5.82 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY: the writing side of the style layer.
#   S3-2b loads {EXAM}_style_profile.json + {EXAM}_pyq_index.json (every failure mode
#   DORMANT with a recorded reason — never a stop, P-4); S3-12c draws a deterministic
#   authoring BRIEF per slot (seed = sha256(exam·paper·corpus_hash·qnum), frozen in
#   batch_state.style_briefs, EC-19); S7-STYLE authors to the brief and measures what was
#   written, with the Q19 RETRY BUDGET (MAX_ATTEMPTS_PER_Q=2, MAX_RETRIES_PER_PAPER=
#   ceil(0.20×total) — 72 generations worst case on a 60-Q paper, measured); S4-11 gains
#   items 45-47 (G-STYLE, G-PYQ-DIST, G-ITEM), all three ADVISORY BY CONSTRUCTION — they
#   record their verdict and can never fail a batch or withhold a paper. Every decision
#   constant lives in blueprint_core; nothing here is a hand table.
# v5.81 — 2026-08-30 — GAP-2026-08-30-FITTER-ASPECT (figural_core; audit_canonical v2.25;
#   this spec Q10.6-Q10.8). THREE DEFECTS, found by rendering every figure family through
#   the deployed v5.80 engine: (1) figural_core.apply_data_window() (v5.55) forced the data
#   window's y/x ratio IN DATA UNITS to equal the axes box aspect on EVERY axes — right for
#   an aspect-locked axes (set_aspect('equal'), imshow structures), wrong for an ordinary
#   'auto' chart: y spanning 70 units against x spanning 4 widened x ~17x and collapsed
#   the bars into a sliver (content fill 4 %, coloured ink 0.06 %). Every unequal-range
#   data chart since 2026-08-19 rendered that way; it went unnoticed because delivered
#   figures were structures and dimensionless plots. FIX: an 'auto' axes takes the window
#   AS GIVEN and scales x and y by their OWN factors; an aspect-locked axes is byte-identical
#   to v5.55. (2) G-FIGFIT compared a clearance the fitter converged to within half a pixel
#   against the floor with 1e-6 tolerance, so 0.04993 in (printed "0.050") failed a 0.050
#   floor on 16 of the 38 delivered Mock02 figures. FIX: FIG_FIT_TOL_IN = half a rendered
#   pixel, the fitter's own criterion. (3) audit_canonical printed verdict lines for 13
#   figure gates and DROPPED the rest: G-FIGFIT / G-FIGCOLLIDE / G-FIGINK (BLOCKING-class)
#   and the five v5.80 colour gates were evaluated and never reported, and the three
#   SET-level gates (G-FIGOPTUNIF / OPTWINDOW / OPTELEM) had never been called at all —
#   their "N conform" lines were vacuous. FIX (v2.25): eleven explicit verdict lines
#   (roster 13 -> 24) and per-question set evaluation. Delivered Mock02 now shows its one
#   real G-FIGINK regression (Q7) that Step 8 had never printed. Zero exam values; no PYQ,
#   Explain, Notes, Deliver, registry, route or trigger touched. figural_core self-test
#   163 -> 171; audit_canonical 312 -> 317; six fitter and five auditor mutants killed.
#   FINAL REVIEW (line-by-line): an 'auto' axis keeps its inversion (depth profiles) and a
#   degenerate window is padded (FA6); a set gate that raises reports under ITS OWN id
#   (G-FIGOPTUNIF, not a mis-sliced name) and option specs without a question number are
#   never pooled into one set (fixtures 56d/56e).
# v5.80 — 2026-08-29 — GAP-2026-08-29-FIGURE-COLOUR-ROLES (estate-wide; exam-agnostic;
#   RENDER-TIME ONLY — Step 7 figures; no PYQ flow, no Explain flow, no Notes flow, no
#   registry schema, no route and no trigger is touched; standing issues are NOT mixed in).
#   PROBLEM (measured 2026-08-29 against a 51-figure externally-produced paper and the
#   delivered IIT JAM CHEMISTRY Mock02): (1) corpus_io.structure_draw_fn drew atoms in
#   rdkit's DEFAULT palette — unpinned across rdkit versions and failing WCAG 3.0:1 on
#   Cl (2.2), S (1.7), F (2.0), P (2.5) — and ignored the `palette` argument Q7b.8/C6
#   mandate, so every hydrocarbon structure (9 of 38 figures) rendered 0.0000% coloured
#   and tripped G-FIGACCENT estate-wide while heteroatom structures passed by accident;
#   (2) the three low-contrast Okabe-Ito hues (orange 2.25, sky 2.31, yellow 1.32) had no
#   rule keeping them out of TEXT and thin strokes, and the four line hues (3.06-3.87)
#   are below the 4.5:1 WCAG 1.4.3 floor that applies to any coloured LABEL;
#   (3) heteroatom colour in an option set can single out the one option that carries
#   the heteroatom — a Q7b.6 colour/correctness correlation nothing gated;
#   (4) a question that interrogates a colour (complex, indicator, flame, precipitate)
#   could be handed a figure showing that colour; (5) nothing capped chromatic series,
#   although every published categorical palette (Okabe-Ito, Petroff 6/8/10, Tol)
#   falls to or below the CVD-separability floor from its 5th hue (Petroff 2021,
#   arXiv:2107.02270, reproduced in CAM02-UCS + Machado simulation 2026-08-29).
#   FIX (figural_core, corpus_io v1.14, this spec Q7b.9-Q7b.14 / S10-7C C7-C9 / S10-6A):
#   the eight Okabe-Ito hues stay the ONLY hues; each now has a ROLE and the role is
#   gated — TEXT tier (same hues darkened to >= 4.5:1, via fc.text_ink), LINE/MARK
#   (>= 3.0:1), FILL-only (dark edge always; touching fills differ by hatch or luma,
#   via fc.fill_style), chromatic SERIES CAP 4, a pinned CVD-safe ATOM_PALETTE, an
#   opaque accent HIGHLIGHT for the interrogated site of a structure, set-wide
#   ELEMENT-COLOUR UNIFORMITY decided automatically by render_option_set(), and a
#   COLOUR-AS-CONTENT guard (fc.colour_is_content -> monochrome render). Five new
#   gates, AMBER/VOID_ITEM, all in NEVER_BLOCKING_ON_COLOUR, all SILENT on a sidecar
#   without colour_profile (EC-V18 posture). The `exam_config.figure_palette`
#   reservation of Q7b.1 is CLOSED: one palette, estate-wide, zero per-exam migration.
#   ZERO-BREAK PROOF: OKABE_ITO, series_defaults(), every threshold and every pre-v5.80
#   gate are byte-identical (figural_core fixture C0); every figure that exists today
#   audits exactly as before; figural_core self-test 124 -> 163, corpus_io 357 -> 362,
#   thirteen figural_core and five corpus_io mutants each killed by a fixture.
#   FORWARD-ONLY: papers rendered from v5.80 onward. Delivered papers are never
#   re-rendered; Mock 1..N of one exam may therefore differ in atom colour until a
#   figure-only re-render is requested (S10-7 Q13).
# v5.79 — 2026-08-28 — GAP-2026-08-28-MULTIPART-STEM-LAYOUT (estate-wide; exam-agnostic;
#   a formatting-only change by operator ruling — no other standing issue is touched).
#   PROBLEM: a stem carrying an enumerated sub-part series (reagent/procedure steps,
#   test lists, statement sets, sentences-to-arrange, assertion–reason pairs) had no
#   layout contract — the series shipped inline in one run-on paragraph, unreadable on
#   one-question-per-screen portals — and sub-part LABELS were unconstrained: a
#   digit-dot sub-part in one spacing EVADES the exam's strict OPTION_LABEL_RE while
#   the exact-spacing form COLLIDES with it (G-NAT-NOOPT / G-OPTLABEL / R4 territory),
#   and S12-NEW-2 flags the near-miss as a malformed option. The safe label set is
#   EXAM-RELATIVE (option schemes span numeric/alpha/roman/custom across the estate)
#   and SPACING-EXACT — exactly what session judgment gets wrong and a spec cannot.
#   FIX, four parts: (1) NEW §10 S10-2b — MULTI-PART STEM LAYOUT CONTRACT: one BOLD
#   continuation paragraph per sub-part; LABEL LAW (a) never a Q-number shape,
#   (b) never THIS exam's own option-label scheme tested SPACING-INSENSITIVELY,
#   (c) bare digit-dot/digit-paren banned under EVERY exam, (d) safe-ladder choice;
#   MSQ/NAT instruction stays INSIDE the Q.N line (R14 anchors unchanged); canonical
#   NAT order Q.N(context+instruction) → sub-parts → closing ask; MATCH excluded
#   (lists stay REAL tables); linked-block sub-parts follow the non-numbered ask.
#   (2) NEW S10-3 helpers add_stem_multipart + _subpart_label_violation — the LABEL
#   LAW raises AT AUTHORING TIME, so a colliding paper cannot be BUILT, independent
#   of every downstream gate. (3) S10-1 gains the MULTI-PART STEMS format rule.
#   (4) S2-2 gains R-SUBPART; S4-11 gains its 44th item G-STEM-SUBPART (Layer-1-only,
#   joining the no-auditor-twin items); normative checklist counts move 43→44.
#   Existing gates G-QNUM-FIRST, G-OPTLABEL, G-NAT-NOOPT, R4, K-INT are UNCHANGED and
#   act as independent backstops. Downstream Steps 9/11 need NO change: RE-3 /
#   verify_fidelity (Step 9) and the byte-identical tagger (Step 11) are pass-through
#   by design; MockDeliver §2 already documents "Q.N [bold stem text] — may span
#   multiple paragraphs". FORWARD-ONLY: papers authored from v5.79 onward; the PYQ
#   flow / Row files are UNTOUCHED by operator scope ruling (PYQPrepare owns that
#   contract, not this spec).
# v5.78 — 2026-08-28 — GAP-2026-08-28-STEP7-SUBJECT-LEARNINGS-SEAM (paired with
#   explain_engine v2.10's resolve_learnings_files, already on this trigger's route).
#   v5.77's widened glob made a non-{EXAM}-prefixed learnings file VISIBLE (a real
#   improvement over silent skipping) but its printed remedy — "rename it
#   {EXAM}_EXPLAIN_LEARNINGS_v<N>.md" — contradicted the same-day Explain-side design
#   (GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ §6.2, operator decision D1): per the Explain specs' S24 contract
#   the non-exam-prefixed *_EXPLAIN_LEARNINGS_v*.md IS the subject library, "one file
#   copied unchanged into every exam project of that subject", and obeying the rename
#   instruction re-plants the per-exam-copy workaround estate-wide (highest-version
#   collision hazard included). Two same-day releases, two philosophies, one file
#   family. FIX: Step 7 resolves by the SAME discovery contract Steps 9 / PYQ-1 use —
#   the SUBJECT file is found by explain_engine.resolve_learnings_files (partition by
#   the {EXAM}_ prefix), while the EXAM side keeps the exact v5.56 family glob
#   {EXAM}_EXPLAIN_LEARNINGS_v*.md untouched — the helper's broader exam partition
#   admits the {EXAM}_PYQ_EXPLAIN_LEARNINGS_v*.md family, whose basenames sort after
#   the shared family, so consuming it here would silently swap families on any
#   project that has run both pipelines (caught in pre-deploy review; never shipped).
#   S3-1 stages the highest exam-family file AND the discovered subject file; S3-3
#   extracts BANNED:/VERIFIED DEFECT: markers from BOTH (subject-library markers were
#   previously unreachable by this step under ANY naming). >= 2 non-exam files →
#   abstain + WARN naming the candidates (never a rename instruction). Legacy
#   {EXAM}_ExplainLearnings.md fallback and its migration warning unchanged. Behaviour
#   note: pre-v5.78 loaded exactly one file (highest exam version); v5.78 loads up to
#   two (highest exam + subject) — marker extraction is additive, so an exam whose
#   subject library carries no markers is byte-identical to pre-v5.78.
# v5.77 — 2026-08-28 — GAP-2026-08-28-PLACEMENT-UNSPECIFIED (paired with
#   blueprint_core Cluster Q — place_subtopics / min_possible_adjacent /
#   audit_placement — and audit_canonical v2.23 A-CLUSTER + --through-q).
#   THE GAP: this spec told every session what the finished paper must look
#   like (R19) and what data it starts from (blueprint allocations) but never
#   specified, implemented, persisted or verified the transformation between
#   them. S3-18's one prose sentence — "subtopics assigned to Q positions in
#   blueprint order" — is guaranteed non-conforming with R19 whenever any
#   subtopic has q_count >= 2 (the normal case); MOCK:M01 noticed and
#   hand-repaired, MOCK:M02 did not and shipped Q.1–Q.3 same-concept_group
#   with a clean "all PASS" gate report, because G-CLUSTER was one of five
#   S4-11 items with no auditor equivalent and STEP B presented the auditor
#   as a substitute for the checklist. FIX, five parts: (1) NEW S3-12b builds
#   the placement plan via bc.place_subtopics (deterministic, seeded by
#   paper_index, concept-group-first, provably floor-optimal; linked-stimulus
#   blocks atomic and R19-exempt inside) and arms a G-CLUSTER PRE-FLIGHT
#   before Q.1 exists; (2) the plan is PERSISTED — batch_state gains
#   subtopic_by_qnum + placement_report, S4-12 resume treats a populated plan
#   as FROZEN (never re-placed; pre-fix papers are audited via
#   bc.audit_placement and reported, never rewritten); (3) S3-13's two
#   `except NameError` silent fallbacks are DELETED — a missing plan is a
#   producer fault and HARD STOP [HS:PROSE]s (an empty set silently put every MSQ/NAT
#   question into the free answer pool and corrupted K-BAL paper-wide);
#   (4) S3-18's blueprint-order sentence is DELETED and replaced by a pointer
#   to the persisted plan; (5) S4-7 STEP B and B-7 change from either/or to
#   BOTH auditor AND checklist (five items have no auditor equivalent), the
#   S4-11 heading drops "used when audit.py absent", the checklist must be
#   PRINTED from the item list (a report with fewer than 43 lines is itself a
#   gate failure), and the auditor invocation is spelled out verbatim with
#   --through-q so intermediate batches print RESULT: PASS instead of six
#   structural FAILs (GAP-2026-08-28-AUDIT-PARTIAL-PAPER). ALSO:
#   S3-3's EXPLAIN_LEARNINGS glob widened to *_EXPLAIN_LEARNINGS_v*.md with a
#   loud WARN on a non-{EXAM} prefix (GAP-2026-08-28-LEARNINGS-PREFIX-GLOB);
#   S3-19 gains a structure-renderer pre-flight HARD STOP [HS:PROSE] and figural_core
#   declares rdkit (GAP-2026-08-28-RDKIT-UNDECLARED); S13-4c passes
#   --rules/--manifest so ship-time A-CLUSTER runs at full concept-group
#   strength. S3-12b's middle branch is the pre-v5.77 UPGRADE PATH: authored
#   questions frozen from the answer_key concept_map, the un-authored
#   remainder placed fresh into each section's remaining contiguous range —
#   adjacency on a resume is ALWAYS a §R13 disclosure and the only resume
#   HARD STOP [HS:PROSE]s are artefact-consistency faults. Allocation is summed from the
#   RAW blueprint entries (S3-2's alloc_ids collapses duplicates by
#   overwrite). Difficulty-plan
#   figural-blindness (GAP-2026-08-28-DIFFICULTY-FIGURAL-BLIND) is NOT in
#   this release — it moves the Axis-1 grant pass and gets its own change.
# v5.76 — 2026-08-27 — REPAIR-RETIRED-2026-08-27 (operator decision; paired with
#   paper_pipeline v5.76, MockTestExplain v1.47.0, MockDeliver v1.18.0, DeliveryFooter v1.29,
#   audit_canonical v2.22, blueprint_core DIFFICULTY_GATE_MAX_REPAIR_ROUNDS 1 → 0). The four
#   *Repair triggers are RETIRED: §S16 (repair mode, batches, pre-repair snapshot,
#   _Create_Repaired.docx, repair_state.json) is DELETED and replaced by a retirement
#   notice; routes.json, SKILL and validate_framework_md.PIPELINE drop the triggers;
#   pp.dg_add_rework_snapshot / dg_stem_hash / dg_verify_repair are deleted from the
#   engine; mock_sync_audit MS-2/MS-15 forbid the names from ever returning. The
#   difficulty gate now DISCLOSES (DISCLOSED/0) instead of blocking (FAILED/0) and no
#   step rewrites a question on its say-so. This step's registry contract is unchanged:
#   it CREATES the gate record at birth and never writes status/counter. No question
#   generation rule changed; artefacts of a fresh MockCreate are byte-identical.
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
#   allows it — after bc.difficulty_feasibility HARD STOPS [HS:PROSE] any count the exam shape
#   cannot honestly hold (with the achievable maximum named). (2) CHECK 3c / G-DIFF:
#   author TO the band via bc.difficulty_authoring_profile, record difficulty_obs from
#   the derivation already performed for the sidecar, and accept only when
#   bc.verify_difficulty_obs(label, obs) agrees — MAX_DIFF_TRIES=6, then a quota-
#   preserving band-swap escape, then HARD STOP [HS:PROSE]; a label an evidence contradicts never
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
```

Section §S16 (REPAIR MODE, v5.69–v5.75) RETIRED and moved here VERBATIM at framework
release 2026.08.27.3 (REPAIR-RETIRED-2026-08-27, operator decision). Not executable;
retained so the defect narrative it carries (GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING,
GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER, GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS,
GAP-2026-08-26-REGISTRY-HANDOFF-SEAM, GAP-2026-08-26-REPAIR-BATCH-LAW) stays in the repo.

````
# ════════════════════════════════════════════════════════════════════════
# §S16 — REPAIR MODE (TestCreateRepair / MockCreateRepair, v5.69 —
#         GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING)
# ════════════════════════════════════════════════════════════════════════

Entry v5.93 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v5.94 supersedes).

```
# v5.93 — 2026-11-06 — GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY (owner decision OD-2026-11-06;
#   paired with NEW Framework_MockTestOrchestrate v1.0.0, NEW SESSION_BUDGET.json, the bootstrap.py
#   read / retention / staging / worker commands and the spec_sections.py read plan). Measured
#   2026-11-06 (SESSION_BUDGET.json _measured): a context that keeps growing is summarised by the
#   platform without notice, after which a session works from a summary of this spec; a tool result
#   of about 40,000 characters or more is diverted to a file the session cannot read back whole.
#   WHAT CHANGES HERE. NEW S1-0R: the read method (bootstrap --read K, at most 300 lines per call),
#   READ-RETENTION at four points, RUN MODE (Step 7 runs ORCHESTRATED: the WORKER MODE delivery
#   proxy and review hand-over are defined in Framework_MockTestOrchestrate.md and bind this spec's
#   present_files sites and S13-2G phase 2) and INPUT STAGING (bootstrap.py --stage-inputs satisfies
#   this spec's /mnt/project and /mnt/user-data/uploads paths on every surface); S1-0's read advice
#   now points to S1-0R. S13-2G phase 2 gains one WORKER MODE paragraph; S4-7 STEP E, S13-8 and
#   S13-9A gain one pointer line each. Superseded entries v5.54.1-v5.92 moved verbatim to
#   SPEC_HISTORY.md (EC-P42). STEP_CONTRACTS override floor raised to 5.93 (owner rule D8).
#   No question-writing rule, gate, artefact, deliverable, end state or user action changed.
```

Entry v5.94 moved at framework release 2026.11.08.1 (GAP-2026-11-07-RE25-HARDENING; v5.95 supersedes).

```
# v5.94 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (owner decisions 2026-11-07 D1 (b),
#   D2 relative, D3, D4, D5, D6, Q1 (c), Q4, Q5 and 2026-11-08 (a); paired with blueprint_core v1.33,
#   MockTestAnalyse v2.61.0, MockReview v2.1.0, analyse_engine v1.4). Measured 2026-11-07: a
#   post-graduate organic paper was scheduled Hard 28 and shipped with the blind reviewer grading it
#   Hard 9; the reviewer's verdict was recorded as a note and never acted on, and nothing counted the
#   delivered paper against the ORIGINAL schedule. WHAT CHANGES HERE (every exam unless marked):
#   NEW S3-8L builds the organic decision-load ruler (L2; organic subtopics only, owner Q4) from the
#   exam's OWN past papers (shares: the Step-5 blind grades of the SAME profile, else the registry
#   cache, else the blueprint's measured shares — printed), freezes it for the series, and derives the
#   pattern cards; S3-15L (from the final plan) fixes the target plan and gives each organic slot a
#   pattern source (never a past question, D6);
#   CHECK 3c gains (b0) (the L2 band is the organic item's content evidence; L1 is informational for
#   it) and ONE generic rule: a slot measured BELOW its band is re-authored (DR1 next pattern source,
#   DR2 band-target brief, inside the one G-DIFF budget) and then CARRIED TO REVIEW at its band
#   (decision 'carried_below') instead of the R5 easier relabel; the band-swap escape also updates the
#   TARGET plan (batch_state 'difficulty_plan_target', count-neutral). S13-2G phase 1 gives the
#   reviewer the concept vocabulary; phase 3 replaces DL-52 with bc.dl_phase3_decision (reviewer band
#   when anchored, the in-batch measured band, the L2 ruler on the lower of author / reviewer
#   concepts): round 1 BELOW -> a repair, round 2 BELOW -> DR3, the only relabel, disclosed. NEW S13-2L
#   counts the paper against the target plan (bc.difficulty_paper_gate). S13-4 caches the blind
#   grades in the registry; S13-6 prints bc.difficulty_layer_lines. Nothing here stops (C1); no
#   certificate effect (C2); no new user action (C4). Entry v5.93 moved to SPEC_HISTORY.md.
```

Entry v5.95 moved at framework release 2026.11.09 (GAP-2026-11-08-DR3-QINDEX-CONFLICT; OD-2026-11-09).

```
# v5.95 — 2026-11-08 — GAP-2026-11-07-RE25-HARDENING (paired with MockTestExplain v1.55.0,
#   PYQExplain v2.30, explain_engine v2.14, corpus_io v1.20). One S7-QUALITY field and one
#   authoring check, nothing else: option_text_smiles (every TEXT option that names a species
#   gets its structure, RC-17 / owner Q10 (a)); the NAME CHECK AT
#   AUTHORING (explain_engine.name_check_item: a stem or text option whose name is not the
#   structure it must be is a defect and the item is regenerated, RC-6). OPSIN is installed
#   once per session by the engine; absent -> NAME_UNRESOLVED recorded, never a stop. Entry v5.94
#   moved to SPEC_HISTORY.md.
```

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
````

Entry v5.59 moved at framework release 2026.08.25.3 (EC-P42; v5.71 supersedes).

```
# v5.59 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paper_pipeline v5.39,
#   final_assembly v5.55, corpus_io v1.12; paired with MockTestExplain v1.37.0 / engine
#   v2.8). A delivered Mock 01 was CREATED with key 2 on a figural question (salicylic
#   acid: carboxyl + phenol) and EXPLAINED with key 1 — Step 9 misread the hand-drawn
#   structure, both its derivations shared the misread, and nothing compared the two
#   steps because the key never leaves Step 7 by design. Two creation-side gaps made
#   that silent: (1) the registry carried no trace of the key Step 7 held, so no
#   downstream step could reconcile against it without seeing plaintext; (2) a
#   chemical structure was drawn by HAND-PLACED bonds (`cd.ring_pts`, `cd.bond`) with
#   NO machine-readable record of what it depicted — figural_manifests.object_types was
#   empty and Step 9's §13-3 manifest cross-check had nothing to compare. FIXES:
#   (a) KEY COMMITMENTS — S13-4 passes the answer_key sidecar to fa.commit_registry
#       (answer_key=…) which writes registry.key_commitments[paper_id] = salted sha256
#       of every canonical answer (mcq '2' · msq '2,3' · NAT grading string). No
#       plaintext enters the registry; Step 9 hashes its OWN derived answers and
#       compares (Explain §7-8). S13-REGCHECK gate G-KEYCOMMIT refuses a commit without
#       them. ZERO new operator deliverables — the registry is already uploaded.
#   (b) SEMANTIC OBJECTS — NEW S7-NEW-B2: every generated figure registers what it
#       DEPICTS (paper_pipeline.validate_semantic_object; kind STRUCTURE / REACTION
#       carries canonical SMILES) in fig_manifest questions[q].semantic_objects; S13-4
#       commits them to figural_manifests[].semantic_objects. A STRUCTURE figure is
#       RENDERED FROM ITS SMILES through corpus_io.structure_draw_fn inside
#       figural_core.render_figure (verified: passes the v5.57 fit census and G-FIGINK
#       unchanged) — the image and its registration are ONE artefact, so a figure can
#       no longer disagree with its own identity. Hand-placed bonds for a STRUCTURE are
#       a G-FIGSEM defect. EC-V18: a registry without either field is read unchanged.
```

Entry v5.66 moved at framework release 2026.08.24.4 (EC-P42; v5.68 supersedes).

```
# v5.66 — 2026-08-23 — GAP-2026-08-23-ECFG-LABEL-PARITY. The exam_config
#   option_label_format tier — the FIRST tier of the v5.65 chain — was consumed
#   VERBATIM: never passed through pp.resolve_option_label, never family-checked
#   against what the auditor will classify. Two failures, both MEASURED on a
#   synthetic exam against the live auditor: (1) a cross-family override
#   (section_rules '1/2/3/4', exam_config alpha) renders (A)(B)(C)(D) per the
#   documented override while audit_canonical.gate_options classifies family from
#   section_rules ONLY (its L400 cat_c read; exam_config is never read by the
#   auditor) — A-OPTLABEL 'bad label family' FAILED every question, exit 1, no CP
#   repair: the exact GAP-2026-08-03-LABELFMT class v5.37 killed on the
#   section_rules tier, still alive on the override tier. (2) a notation-form
#   override ('A/B/C/D' instead of a template) carries no '{text}' placeholder,
#   so the G-OPTLABEL regex builder and option rendering both operate on a
#   non-template string. FIX (§3 S3-2 config block): the override now goes through
#   the SAME resolver as the section_rules tier, its render family is derived from
#   the resolved template's own token (option_label_family misclassifies template
#   strings — the pass-through branch is NOT trusted for parity), and it is
#   asserted equal to the family the auditor will classify: _resolved_family when
#   section_rules declares a label, else 'num' (the auditor's own L400 default —
#   an override with NO section_rules label is still audited against '1/2/3/4').
#   Mismatch or unknown token = HARD STOP at PRE-GENERATION naming the conflict.
#   Same-family punctuation overrides ('(1)' vs '1.') remain fully supported and
#   byte-identical. DORMANT for every exam_config that omits option_label_format
#   (the IIT_JAM_CHEMISTRY reference config omits it). No engine changes. No
#   artefact moves.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockTestCreate.md.

```
# v5.54.0 — 2026-08-12 — THREE DEFERRED DESIGN GAPS CLOSED (scoped 1-by-1)
#   Closes, as individually scoped fixes, the three gaps earlier hardening releases flagged
#   and deliberately deferred (each documented at its flag site + in the audit records):
#   1. GAP-2026-08-12-S13-4B-SCOPED-PATH (spec-only). S13-4b's dossier md5-binding and
#      S13-4c's re-sweep command hardcoded f'{EXAM}_Mock{N}_Create.docx'. DOUBLY wrong:
#      pp.paper_slug zero-pads ("Mock03"), so the literal missed EVERY single-digit mock's
#      actual file (FileNotFoundError at S13-4b for mocks 1-9), and a scoped paper's slug
#      ("SUBJ_Physics_01") never matched at all. Fixed: the docx path is derived from
#      pp.paper_slug(paper_id) — the ONE filename-stem rule — at both sites. The dossier's
#      OWN filename keeps its M[N] form (writer, S13-7 checker, DeliveryFooter and
#      audit_canonical --dossier help all agree on it; outputs/ holds one paper per
#      session, so it cannot collide).
#   2. GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING (engine, final_assembly.py).
#      question_index/session_log deduped by exact paper_id while G-COMMIT-COMPLETE looked
#      up by mock number — a paper_id corrected mid-session then re-committed left a stale
#      same-number sibling no gate could see. Fixed on BOTH sides: commit_registry's
#      dedupe key widened to SAME-SERIES + SAME-NUMBER (one series holds exactly one paper
#      per number; a same-number entry in a DIFFERENT series — MOCK:M01 alongside
#      SUBJ:Physics:01 — legitimately coexists and is never touched), papers_completed
#      drops the renamed same-series/same-number predecessor (unparseable numbers left
#      alone, never guessed at), and regcheck() gains a stale-sibling DETECTOR
#      (G-COMMIT-COMPLETE/DUP): ≥2 same-series entries for one number HARD-STOPS when it
#      is THIS mock's slot, warns for historical mocks — the same fails/warns split as
#      G-COMMIT-COMPLETE itself.
#   3. GAP-2026-08-12-AXISPAPER-PERSISTENCE (spec + engine). S7-AXIS wrote per-paper
#      Axis-1/Axis-3 snapshots onto an in-memory registry object nothing ever dumped —
#      the v5.49 mock-keyed history never reached disk. Fixed: S7-AXIS now only
#      ACCUMULATES the per-section snapshots (axis1_paper_counts / NEW axis3_paper_counts,
#      dead reg writes removed), and S13-4 threads both into commit_registry's new
#      optional axis1_snapshots/axis3_snapshots params, persisted as
#      reg['axis1_paper'][str(N)] / reg['axis3_paper'][str(N)] — replace-by-mock,
#      idempotent, deep-copied, the axis2_window_counts precedent exactly. Read at S13-4
#      via globals().get (an exam with no axis feature never runs S7-AXIS, so the
#      accumulators are legitimately unbound there — that means "nothing to persist",
#      never a NameError). Absent/empty ⇒ no write ⇒ feature-inert exams byte-identical.
#   final_assembly.py self-test: 79 → 96 fixtures (17 new, every new load-bearing branch
#   mutation-verified). No schema change: axis1_paper/axis3_paper already existed in the
#   documented v5.49 shape — this release makes the documented write actually happen.
# v5.53.2 — 2026-08-12 — SPEC-INLINE NAME-FLOW AUDIT (GAP-2026-08-12-SPEC-INLINE-NAME-AUDIT)
#   The v5.53.1 audit proved the one blind spot in the whole verification chain: spec-inline
#   ```python blocks are syntax-checked (validate_framework_md.py Check B) but never
#   name-flow-analysed (Check AJ covers .py engines only), which is how the
#   batches_completed NameError survived 7+ releases. This release closes the CLASS, not
#   just the instance: new tracked repo-level auditor `spec_name_audit.py` v1.0 simulates
#   sequential (notebook-cell) execution of every ```python block in every Framework_*.md
#   and flags any name read before any block binds it. Calibrated against the known bug
#   shape (its self-test embeds the batches_completed fixture: buggy shape MUST flag, fixed
#   shape MUST pass; 16/16, mutation-verified). CI now runs it in baseline-ratchet mode
#   (spec_name_audit_baseline.json freezes the triaged pre-existing findings — illustrative
#   fragments, prose-contract inputs, trigger-provided names; any NEW finding fails CI).
#   Rolling this file back to its v5.53.0 state makes the ratchet fail on exactly the 4
#   real bugs — proof the tool would have caught all of them automatically.
#   ITS FIRST RUN AGAINST THIS FILE FOUND 3 MORE REAL BUGS, ALL FIXED HERE:
#   1. GAP-2026-08-12-S3-17B-BC-UNBOUND — S3-17b (§3, session start; added v5.50/v5.51)
#      reads `bc.axis1_mock_feasibility(...)`, but this file's only
#      `import blueprint_core as bc` lived at §7 S7-NEW-B, which executes LATER. NameError
#      in strict execution order. Fixed: explicit import at the top of the S3-17b block.
#   2. GAP-2026-08-12-S7-AXIS-COUNTS-UNINIT — S7-AXIS's snapshot loop assigns
#      `axis1_paper_counts[sec_name] = snap` and S7-NEW-B reads it, but nothing anywhere
#      initialised the dict. NameError in strict execution order. Fixed:
#      `axis1_paper_counts = {}` at its producer.
#   3. G-ALTGROUP / G-GROUPMANDATE / G-MINCOUNT (§12) called `sys.exit(...)` with `sys`
#      never imported by any block in this file. Fixed: `raise SystemExit(...)` — needs no
#      import and is this file's own house style (20 existing gates already use it).
#   ALSO EXPLICITLY FLAGGED, NOT FIXED (GAP-2026-08-12-AXISPAPER-PERSISTENCE, deferred —
#   design change, not a hardening): S7-AXIS's `reg['axis1_paper']`/`reg['axis3_paper']`
#   writes mutate the in-memory §3 `reg` object that no block ever json.dumps, so in
#   strict execution order they never reach the delivered registry. No engine consumes
#   either field today (verified by grep), so nothing mis-audits; the fix (threading the
#   snapshots through final_assembly.commit_registry(), mirroring axis2_window_counts) is
#   recommended as its own scoped release. Documented inline at S7-AXIS.
# v5.53.1 — 2026-08-12 — FINAL ASSEMBLY ENGINE HARDENING (post-extraction 0-bug audit)
#   A dedicated final adversarial audit (3 independent passes: byte-fidelity diff of
#   final_assembly.py against the pre-extraction spec-inline code it replaced, spec-inline
#   wiring/variable-scope sync check, and adversarial edge-case/mutation hunting) found and
#   fixed 5 real defects surfaced by v5.53.0's Row 0 extraction — 1 CRITICAL (would have
#   crashed EVERY Final Assembly run) and 4 crash-on-malformed-input hardening gaps:
#   1. GAP-2026-08-12-S13-4-UNDEFINED-BATCHES-COMPLETED (CRITICAL). S13-4's call into
#      fa.commit_registry() referenced a bare `batches_completed` name that was NEVER bound
#      anywhere in this file (only `bs['batches_completed']`/`batch_state['batches_completed']`
#      dict keys exist, scoped inside S3-16/S4-8a). This exact NameError was latent in the
#      PRE-EXTRACTION spec-inline code too (v5.52.0 and earlier — confirmed via `git show` on
#      the parent commit), invisible to every verification pass to date because nothing in the
#      chain (gen_manifest/bootstrap/validate_framework_md/check_triggers/self-tests) actually
#      EXECUTES this specific inline block end-to-end. Found by a dedicated wiring-audit pass
#      that traced every variable's binding site by line number, then confirmed live via a
#      real exec() of the extracted S13-4/S13-REGCHECK/S13-QINDEX/S13-7 blocks in sequence
#      against a fixture filesystem. Fixed by reloading batch_state.json fresh at S13-4 (same
#      defensive-reload pattern already used for progress.json/registry.json there), rather
#      than relying on a per-batch local (`bs`) that isn't guaranteed still bound this late.
#   2-4. final_assembly.py regcheck() hardening: a non-numeric msq_meta.total_options no
#      longer raises ValueError (the pre-extraction code's try/except protected this
#      conversion; splitting file-load from schema-gate moved it outside that protection —
#      an extraction-introduced regression, now fixed with its own guard); a malformed
#      (non-dict) concept_map entry no longer raises AttributeError (degrades to "not
#      numerical" rather than crashing); a pre-existing wrong-typed `options_by_q` (e.g. a
#      hand-patched registry) no longer raises TypeError (force-reset to the correct
#      container type, same self-heal spirit as the _REQUIRED_TOP fields). All three are
#      pre-existing crash risks the old spec-inline code also had (same bare-indexing
#      patterns existed before extraction) — hardened now because this function's own
#      docstring promises it never raises, and doing so costs nothing on well-formed input
#      (100% of real production data): all pre-existing self-test assertions are unchanged.
#   5. final_assembly.py predelivery_checklist() hardening: broadened its `except
#      FileNotFoundError` to `except OSError`, so a real filesystem's NotADirectoryError
#      (a file sits where the outputs directory should be) or PermissionError (restricted
#      ACL) degrade to "nothing staged" (checks then fail honestly) instead of crashing.
#   6 new self-test fixtures added for items 2-5, each mutation-verified (neutered the fix,
#   confirmed the self-test catches it, restored) — final_assembly.py --self-test: 79/79.
#   NOT FIXED, EXPLICITLY DEFERRED (a design gap in G-COMMIT-COMPLETE itself, pre-dating
#   this extraction, inherited unchanged from release .10 — out of Row 0's charter to
#   redesign): GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING. question_index/session_log
#   dedupe by paper_id while G-COMMIT-COMPLETE's cross-ledger check keys by mock number; if a
#   mock's paper_id is ever changed and the SAME mock N is committed twice under two
#   different paper_id values (only reachable via an unusual operational error — editing
#   blueprint.json's mocks[].paper_id mid-session then re-running Final Assembly for that
#   mock), the stale entry is never detected or removed. Recommended as its own scoped fix,
#   same as the already-flagged GAP-2026-08-12-S13-4B-SCOPED-PATH.
# v5.53.0 — 2026-08-12 — FINAL ASSEMBLY ENGINE EXTRACTION (Row 0)
#   Closes Finding 0 of the Mock-10 root-cause gap analysis (GAP-2026-08-12-FINAL-ASSEMBLY-
#   ENGINE) — the last open row of the §13 priority table (v5.52.0's SCOPING NOTE flagged it
#   as remaining). §13's S13-4 (registry update protocol), S13-REGCHECK (schema-completeness
#   gate + G-COMMIT-COMPLETE), S13-QINDEX (G-QINDEX certification), and S13-7 (7-point
#   pre-delivery checklist) had zero engine-file backing — pure spec prose a session had to
#   re-type or faithfully re-derive on every single mock, unlike every other load-bearing
#   step in this pipeline (blueprint_core.py / paper_pipeline.py / audit_canonical.py). All
#   four now call into `final_assembly.py`: routed (MockCreate/TestCreate), tracked
#   (gen_manifest.py), self-tested (71/71 fixtures, mutation-tested), and CI-gated
#   (.github/workflows/validate.yml). Semantics are byte-faithful to the prior spec-inline
#   logic — same hard-stop trigger conditions, same wording — with 4 deliberate, disclosed
#   deviations documented in final_assembly.py's own module docstring: every function is
#   PURE (no file I/O, no input mutation); all four return a {'ok', 'fails', ...} result dict
#   instead of raising SystemExit directly (the spec-inline caller raises); qindex_certify()
#   delegates to paper_pipeline.py's pre-existing, already parity-tested
#   validate_question_index() rather than adding a fifth independent copy of G-QINDEX's six
#   checks; and three ledgers (session_log, mocks_completed/papers_completed, rc_manifests/
#   di_manifests/figural_manifests) are now properly idempotent (replace-by-key) where the
#   spec-inline code was append-only. S13-4b/S13-4c (the Tier-A dossier + dossier-fed
#   re-sweep) are deliberately left spec-inline — a different concern (external subprocess
#   invocation), not registry/gate logic.
# v5.52.0 — 2026-08-12 — MANDATORY concept_map CAPTURE + REGISTRY COMMIT COMPLETENESS
#   Closes the last two open rows of the Mock-10 root-cause gap analysis's §13 priority
#   table: row 3 (concept_map/difficulty authoring instruction missing from the consumer
#   spec) and row 5 (partial registry commits, the Mock 4 failure mode).
#   ROW 3 — GAP-2026-08-12-S10-CONCEPTMAP-MANDATE. §S7-NEW-A's write_q_to_sidecar()
#   previously defaulted subtopic_id/difficulty to None, so a call site that forgot them
#   silently persisted `null` — exactly what shipped Mock 10 with difficulty:null on all
#   60 questions, undetected until (if ever) G-QINDEX ran at Final Assembly. Both
#   parameters are now keyword-only with NO default: omitting either is a TypeError at
#   the point of authoring, not a silent null propagated to Final Assembly. New §S10-0
#   states the mandate explicitly in THIS spec's own per-question-authoring section
#   (previously the obligation was documented only in Framework_Blueprint.md §S7-6, the
#   producer's contract, and in §S7-NEW-A's docstring — never as an explicit instruction
#   at S10, where the per-question authoring work actually happens).
#   ROW 5 — GAP-2026-08-12-S13-COMMIT-COMPLETE. New G-COMMIT-COMPLETE gate in
#   S13-REGCHECK cross-checks mocks_completed/session_log/question_index against each
#   other for every mock: a session_log entry AND a question_index entry with a non-null
#   paper_id must both exist. THIS mock's own commit is a HARD STOP if incomplete (a
#   fresh partial write must never reach delivery); a PRE-EXISTING partial commit from an
#   earlier mock is a WARN (repairing historical data is out of scope — same precedent as
#   GAP-2026-08-12-AXISPAPER-HISTORY: fixable going forward, not retroactively). S13-4
#   also gained an explicit ATOMICITY MANDATE comment immediately above its one terminal
#   json.dump, so a future transcription of that block cannot silently regress into
#   incremental (and therefore partially-crashable) writes.
#   SCOPING NOTE: Finding 0 (extracting S13-4/S13-REGCHECK/S13-QINDEX/S13-7 into a real
#   final_assembly.py engine file) remains open — both fixes above are implemented
#   in-place, within the existing spec-inline pattern S13-4/S13-REGCHECK/S13-QINDEX
#   already use, exactly as S13-QINDEX itself does. They do not require, and are not
#   blocked by, the full engine-file extraction.
# v5.51.0 — 2026-08-12 — AXIS-3 PRE-FLIGHT FEASIBILITY (advisory, before Batch 1)
#   (GAP-2026-08-12-AXIS3-PREFLIGHT). Closes the Axis-3 half v5.50 (below) deliberately
#   withheld rather than ship un-verified: a naive subtopic-capability feasibility check
#   for Axis-3 (mechanism MCQ/MSQ/NAT) would be WRONG on any exam whose marking_scheme
#   declares more than one distinct question_type anywhere, because v5.30's POSITION-
#   BASED QUESTION TYPE DISPATCH (`_resolve_answer_axes`, §3 S3-2) means every question's
#   mechanism on such an exam is decided by Q-POSITION (defaulting to MCQ outside any
#   declared range) — in EVERY section, not only the ones GAP-2026-08-12-AXIS3-MECHLOCK's
#   axis3_mechanism_lock marks locked, since `_position_based_typing` is a GLOBAL,
#   exam-wide flag, not a per-section one. A subtopic-capability check applied
#   unconditionally would therefore be not merely useless but ACTIVELY MISLEADING —
#   capable of reporting a shortfall for a mechanism that position dispatch guarantees
#   regardless of which subtopics were allocated.
#   FIX: new `blueprint_core.axis3_mock_feasibility(target, alloc_counts, manifest_ids,
#   position_based_typing)` — `position_based_typing` is a REQUIRED parameter (no
#   default) and the function returns `{}` UNCONDITIONALLY whenever it is True, so the
#   check degrades to a harmless no-op — never a wrong answer — on any exam where
#   subtopic capability is not what actually decides the mechanism. §3 S3-17b (below,
#   extended in place, not duplicated) now computes both axis1_preflight_shortfalls AND
#   axis3_preflight_shortfalls in the SAME per-mock, per-section loop, reusing the SAME
#   `_position_based_typing` variable S3-2 already computes for real drafting dispatch —
#   never a recomputed copy that could drift from what Batch 1 will actually do.
#   S3-18's summary gains a second, parallel AXIS-3 PRE-FLIGHT ADVISORY block, printed
#   only when non-empty — ADVISORY ONLY, never a HALT, identical contract to Axis-1's.
#   blueprint_core.py self-test: 384/384 -> 391/391 (7 new fixtures, including a fixture
#   that feeds an OBVIOUS subtopic-capability shortfall under position_based_typing=True
#   and asserts the function still returns {} — the exact correctness trap this release
#   exists to avoid — mutation-verified twice: once neutering the whole function body,
#   once neutering ONLY the position_based_typing gate while leaving the rest intact,
#   confirming that specific gate is independently load-bearing, not merely coincidental
#   to some other assertion).
# v5.50.0 — 2026-08-12 — AXIS-1 PRE-FLIGHT FEASIBILITY (advisory, before Batch 1)
#   (GAP-2026-08-12-AXIS-PREFLIGHT). Companion release to Framework_Blueprint v1.48's
#   GAP-2026-08-12-AXIS3-MECHLOCK, closing the second half of the Mock-10 root-cause gap
#   analysis's §13 priority table (row 2): "A-AXIS1/A-AXIS3 invisible before Final
#   Assembly." `blueprint_core.axis1_feasibility` (existing, B1/blueprint-build time)
#   answers "does this SECTION have any PYQ subtopic capable of each targeted format,
#   ever" — necessary but not sufficient, since it runs once, before any mock's specific
#   allocation exists. A mock can pass that section-wide check and still be drafted from
#   a subset of subtopics that under-represents the format-capable ones THIS mock needed,
#   purely from how the window's rotation/quota split landed for this specific mock — a
#   structural shortfall invisible until Final Assembly's A-AXIS1 gate audits the
#   finished 60-question paper, by which point fixing it means rewriting already-drafted
#   questions (the exact, expensive discovery-order failure this closes).
#   NEW §3 S3-17b (after the mandatory-subtopic pre-check, before the session-start
#   summary): once this mock's subtopic_allocations are finalised (S3-2/S3-8, well
#   before Batch 1 drafts anything), composes this mock's own Axis-1 target (substituting
#   axis1_target_series[this mock] for the rotating FIGURAL count) and checks it via new
#   `blueprint_core.axis1_mock_feasibility(target, alloc_counts, MANIFEST_IDS)` against
#   the mock's ACTUAL allocation. S3-18's summary prints an AXIS-1 PRE-FLIGHT ADVISORY
#   block naming any short section/format/target/max-achievable — ADVISORY ONLY, never a
#   HALT (mirrors axis1_feasibility's own established contract: "Subtopic is hard #1";
#   Axis-1 is a steered, audited-within-tolerance consequence of allocation, never
#   force-blocking on it). Absent-safe: no axis_schedule, or a section whose status isn't
#   'ok', is silently skipped — byte-identical to every exam that predates this.
#   SCOPE — AXIS-1 ONLY, deliberately, this release. Axis-3 (mechanism MCQ/MSQ/NAT) is
#   NOT included: v5.30's POSITION-BASED QUESTION TYPE DISPATCH (`_resolve_answer_axes`,
#   §3 S3-2) means a mechanism-locked exam's question mechanism is decided by Q-POSITION,
#   not by the allocated subtopic's own answer_cardinality/answer_type — a naive
#   subtopic-capability check would misleadingly report a shortfall for exactly the
#   sections GAP-2026-08-12-AXIS3-MECHLOCK's axis3_mechanism_lock marks 'full'-locked,
#   where the target is ALWAYS achievable by construction. A correct Axis-3 pre-flight
#   needs to branch on axis3_target_source first and is left for its own dedicated,
#   separately-verified change rather than risking a false-positive advisory shipping
#   alongside this one. blueprint_core.py self-test: 377/377 -> 384/384 (7 new fixtures,
#   mutation-verified: neutering the check to "always feasible" makes the shortfall-
#   detection tests fail, confirming they are load-bearing, not decorative;
#   axis1_feasibility itself, and its one existing caller, are byte-identical/untouched).
# v5.49.0 — 2026-08-12 — QUOTA CHECK MOVED INTO THE ENGINE + AXIS-PAPER HISTORY
#   Two independent fixes, found together during a forensic gap analysis of a
#   single exam's 15-mock corpus (four mocks carrying live A-AXIS1 violations;
#   one mock's question_index difficulty shipping null; a fifth mock's
#   axis1_paper/axis3_paper history already unrecoverable).
#   (1) GAP-2026-08-12-QINDEX-QUOTA-ENFORCEMENT — G-QINDEX check 6 (the
#       difficulty distribution EQUALS difficulty_schedule[N] EXACTLY,
#       Contract_QuestionMetadataIndex v1.0) was the one check
#       GAP-2026-08-10-QINDEX-FK-ENFORCEMENT did NOT move into the engine —
#       checks 1-5 (FK/coverage/label validity) did. A session could pass
#       checks 1-5 with a canonical-labelled but wrong-QUOTA distribution (an
#       ungoverned free assessment, or — the mock that motivated this — every
#       difficulty simply left null before S13-4 ever wrote them, since check
#       5 alone would have hard-stopped it had S13-QINDEX actually run) and
#       still log a clean, exit-code-durable audit, because A-QINDEX never
#       compared the count. `audit_canonical.gate_qindex` and
#       `paper_pipeline.validate_question_index` (the reference implementation
#       and its per-exam FK-enforcement twin, GAP-2026-08-10-QINDEX-FK-
#       ENFORCEMENT's four-site architecture) now both implement check 6,
#       dormant when an exam declares no `difficulty_schedule`, kept in
#       parity by the existing QINDEX PARITY self-test harness (extended with
#       a quota-parity leg). S13-QINDEX (below) is unchanged prose — it
#       remains the in-session early check; A-QINDEX is now its
#       engine-enforced, exit-code-logged twin for ALL SIX checks, not five.
#   (2) GAP-2026-08-12-AXISPAPER-HISTORY — S13-4's `axis1_paper`/`axis3_paper`
#       commit (below) now writes `reg['axis1_paper'][str(N)][sec_name]`
#       instead of `reg['axis1_paper'][sec_name]` — mock-keyed, mirroring
#       `options_by_q`'s established `[str(N)] = ...` pattern, instead of the
#       section-keyed, mock-overwriting write every OTHER S13-4 field avoided.
#       Purely additive: the field was write-only (grepped, confirmed unread
#       by any spec or engine in this repo), so no consumer's expected shape
#       changes for the current mock; every PRIOR mock's per-paper Axis-1/
#       Axis-3 counts are now retained instead of being overwritten out of
#       existence by the next mock's commit.
# v5.48.0 — 2026-08-10 — QINDEX FK ENFORCEMENT MOVED INTO THE ENGINE
#   (GAP-2026-08-10-QINDEX-FK-ENFORCEMENT). ROOT CAUSE, proven on a 15-mock
#   reference corpus: registry.question_index subtopic_ids are captured at
#   S7-NEW-A and committed at S13-4 by SESSION-EXECUTED code; the only FK check
#   (spec-inline G-QINDEX) is likewise session-executed and its execution is
#   unverifiable. Three of fifteen sessions persisted INVENTED subtopic_ids
#   (semantically plausible paraphrases of blueprint ids — e.g. a re-typed
#   section slug, a synonym leaf) while truthfully logging audit exit_0/SHIP,
#   because audit_canonical.py — the ONLY enforcement whose exit code is
#   durably logged — never validated question_index at all. The bad ids then
#   hard-stopped Step 11's JOIN, four pipeline steps too late. WHAT CHANGED:
#   (1) S13-4: _qi is now built by JOINING concept_map to blueprint.subtopic_list
#       — the committed subtopic_id is the BLUEPRINT'S OWN STRING (copy-by-
#       reference, never the sidecar's re-typed value); an unjoinable id is a
#       HARD STOP naming the Q-numbers; each row also carries section+subtopic
#       display names (activating Step 11's S1-3 (section,subtopic) fallback,
#       dead until now because these fields were never written); the mock entry
#       carries a qindex_cert {blueprint_version, subtopic_set_hash} provenance
#       stamp.
#   (2) S13-4c: the re-sweep now passes --registry --blueprint --mockN, arming
#       the NEW ENGINE GATE A-QINDEX (audit_canonical.py v2026.08.10): entry
#       exists, count/coverage, every id ∈ blueprint, every difficulty ∈ labels.
#       A FAIL is a nonzero exit handled exactly like any S13-2 FAIL —
#       present_files forbidden until clean. A session can no longer ship a bad
#       index while logging a clean audit: the logged exit code IS the gate.
#   (3) S13-QINDEX (G-QINDEX) is retained unchanged as the in-session early
#       check; A-QINDEX is its engine-enforced, exit-code-logged twin.
#   Companion changes: audit_canonical.py (A-QINDEX), paper_pipeline.py
#   (validate_question_index / registry_integrity_check / classify_unresolved /
#   subtopic_set_hash), Framework_MockTestExplain v1.23 (P10 tripwire),
#   Framework_MockDeliver v1.12.0 (ledger check + remediation classifier).
# v5.47.3 — 2026-08-07 — ONE MASK SET, TWO CONSUMERS (review findings on v5.47.2).
#   (1) _yearform's [A-Za-z]+ swallowed single-letter-over-year fractions
#       (N/2000, M/1950, E/2026) — the cure was wider than the March/2026
#       complaint. Repaired to [A-Za-z]{2,} (month names keep masking; every
#       single-letter numerator fires again).
#   (2) STRUCTURAL FIX for the divergence class: the gate's masks lived only in
#       the gate, while needs_omml kept the old narrow UNIT_LABEL_RE (with the
#       \b-before-² bug, no word-pair mask, h|s|min|hr only) — m/s², 3/2 and
#       is/are were gate-silent but needs_omml-True, and needs_omml feeds
#       assert_not_math, which RAISES. There is now ONE shared mask set
#       (_MM_UNIT/_MM_WORDPAIR/_MM_YEARFORM) and ONE masked detector,
#       consumed by BOTH the gate and needs_omml — agreement is structural,
#       not claimed. UNIT_LABEL_RE is retired to a compatibility alias.
#       NAMED ASYMMETRY (deliberate, not divergence): digit/digit (3/2) stays
#       needs_omml-True — rule 3 makes digit fractions mandatory OMML at
#       routing — while the post-build gate is lenient on rendered digit/digit
#       (dates, scores). Same masks, different pattern scope, on purpose.
#   (3) Named behavioural scoping (the second consumer the v5.47.2 changelog
#       failed to name): widening MATH_TRIGGER_RE had widened assert_not_math's
#       build-aborting figural ban too — ordinary normalised-axis labels
#       (σ/σ₀, λ/λ₀, α/β, Δv/Δt) began aborting builds. assert_not_math now
#       tests the ORIGINAL v4.3-scope RASTER_BAN_RE (letters/digits fraction,
#       caret, superscript-on-term, raw LaTeX, √( ) — restoring pre-v5.47.2
#       figural behaviour exactly, while stem/option ROUTING keeps the widened
#       Greek/subscript detector. Whole expressions still never rasterise.
# v5.47.2 — 2026-08-07 — GATE FIXES (review findings 1–3 on v5.47.1):
#   (1) m/s², rad/s² were false positives: ² is a \w character, so the _unit
#       mask's trailing \b never matched after "s" — denominators (and
#       numerators, for cm²/s) now take an optional [²³] before the boundary.
#   (2) Uppercase and most lowercase Greek were missing from the fraction
#       classes: Δv/Δt, α/β, ρ/σ, ℏ/2, Ω/2, Σ/n, v/c passed silently. Both
#       gate classes AND the MATH_TRIGGER_RE fraction branch now carry the
#       full Greek block (\u0391-\u03c9) plus ℏ, so authoring detection and
#       the post-build gate agree.
#   (3) Known accepted noise, recorded so it is not rediscovered: widening the
#       right class to digits admits non-math letter-over-digit ("Paper A/2",
#       "Section B/1"). Word-slash-YEAR ("March/2026") is masked; the rest is
#       low-volume amber-only operator attention by design (warn-and-deliver).
# v5.47.1 — 2026-08-07 — GATE FIX (review finding on v5.47): the letter-fraction
#   residue pattern required a LETTER after the slash, so letter-over-DIGIT
#   fractions (M/3, E/2, v/2) — including this release's own headline example —
#   passed silently. The right-hand class now admits digits; the left-hand class
#   deliberately does not, so digit/digit (3/2), dates (12/3) and masked units/
#   word-pairs stay non-firing. √N (bare digit radicand) remains deliberately
#   non-firing: readable as-is, and t3_mathcomp auto-converts it inside regions.
# v5.47 — 2026-08-07 — TIER-3 MATH (GAP-2026-08-07-MOCK-OMML, remedies MC1–MC3).
#   Measured on IIT_JAM_PHYSICS Mock05 (14/60 questions): letter fractions left
#   linear in stems ("M/3", "a/√n"), subscripts shipped as flat text ("k_B T",
#   "R_in") because MATH_TRIGGER_RE had NO underscore branch and S10-4 had no
#   subscript vocabulary at all, one caret exponent, and — latent — the S10-4
#   frac/sup/sqrt builders accepted RAW text (schema-invalid <m:num>3</m:num>
#   that Word renders as an EMPTY placeholder; the exact GAP-2026-08-07-
#   EXPLAIN-OMML defect, one forgotten _r() away from firing here).
#   Fix: (MC1) builders _r_wrap + XML-escape internally — raw args are now safe;
#   (MC2) S10-4 delegates to the SHARED Tier-3 compiler t3_mathcomp.py (byte-
#   locked to Framework_PYQPrepare §S3-5b): new single funnel render_mock_text()
#   dispatches ⟦MATH:…⟧ regions with the strict-core/forgiving-boundary contract
#   (a bad region degrades to plain unmarked text and is quoted VERBATIM for
#   Ctrl+F — never a halt, never silent); MATH_TRIGGER_RE gains underscore-
#   subscript, ÷ and combining-accent branches; the decision tree names
#   subscripts as built-up math; (MC3) new mock_math_residue_check() post-build
#   gate scans the rendered docx for dialect residue, bare-text fraction parts,
#   empty OMML and region delimiters, reporting in plain operator words —
#   mandatory before delivery, amber-not-halt. routes.json binds t3_mathcomp.py
#   to MockCreate/TestCreate.
# v5.46 — 2026-08-07 — GAP-2026-08-07-FIGACCENT: the S10-6A palette column was
#   normative prose with NO enforcing gate. "1 accent hue permitted" (data_single)
#   and ">=1 accent for the item under interrogation" (schematic) had a Colour-gate
#   column reading "not required", and figural_core's COLOUR_REQUIRED covered
#   data_series only — so an all-black paper (IIT JAM PHYSICS Mock01, 16/16 figures
#   at 0.0000% coloured pixels, the pre-v5.33 "solid black" habit of RC-1) and an
#   accented paper (IIT JAM BIOTECH Mock01, 0.10-1.11%) both passed every gate
#   identically, and cross-exam figure style drifted with session taste. Remedies:
#   (1) Q7b.8 — the accent is now MANDATORY for data_single (owner decision
#   2026-08-07: "permitted" -> mandatory, OKABE_ITO[0] series ink) and for
#   schematic (interrogated item), gated by G-FIGACCENT/A-FIGACCENT, AMBER by
#   construction (fire-0 history does not exist yet; owner directive: colour never
#   halts); floor coloured_fraction >= 0.05%, calibrated on the real corpus
#   (accented minimum 0.105%, all-black 0.0000%, 2x margin, zero false positives)
#   and deliberately NOT gated on dominant_hues (its area cut swallows small
#   accents). (2) The draw_fn authoring contract: accent ink MUST come from the
#   palette argument, never hardcoded black. (3) render_figure() gains an optional
#   palette= parameter — the plumbing Q7b.1 promised; exam_config wiring stays
#   RESERVED. reasoning_glyph monochrome doctrine and EC-V18 legacy tolerance are
#   untouched; ~200 pre-v5.33 exams stay silent under this gate.
# v5.45 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v5.44 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v5.43 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: figures are SCHEDULED, not forced.
#   The render fork decided figural-vs-text per question from a boolean, so a
#   subtopic allocated to every mock drew a figure in every mock whatever its
#   measured frequency, and an irreducible flag let it pass over budget silently.
#   Step 7 now reads Step 6's per-mock figure schedule (bc.schedule_figural_slots).
#   Absent schedule -> v5.41 ranking, so un-remeasured exams are untouched.
# v5.42 — 2026-08-06 — GAP-2026-08-06-DI: DI becomes measurable.
#   DI was the one budgeted Axis-1 stimulus class leaving NO trace anywhere, so
#   A-AXIS1 could only ever report it UNESTABLISHED. It cannot be recovered from the
#   docx: G-MATCH-TABLE mandates a real Word table for every MATCH question, so on a
#   real paper table-presence finds 3 candidates where exactly 1 is DI. Step 7 now
#   records di_manifests (the producer's own record) and asks the Axis-1 budget
#   before building a table stimulus; Step 5 emits di_rate/di_q_count/di_reducible.
#   Absent-safe: no di_manifest -> DI stays unestablished, exactly as before.
# v5.41 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v5.40 — 2026-08-03 — DEFECT FIX: the Tier-A dossier had lost its reader.
#   v5.39 retired Step 8, which was the only consumer that passed `--dossier` to the
#   auditor. The writer (S13-4b) survived; the reader did not. audit_canonical.py still
#   exposes the flag, nothing passed it, and A-NAT-GRADE + A-FIGPROFILE silently went back
#   to re-deriving what Step 7 had already recorded — the regression the dossier exists to
#   prevent. NEW S13-4c re-runs the SAME auditor over the SAME final docx with `--dossier`
#   immediately after S13-4b writes it (it cannot live in S13-2, which runs before the file
#   exists). No new gate, no new hard stop, no new artefact.
#   Also: Step 7 now delivers the dossier explicitly in the Step-7 footer template
#   (Framework_DeliveryFooter v1.12).
#
# v5.39 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   Step 7 now hands the paper straight to Step 9. Every clause that promised a downstream
#   re-verification ("independently re-verified by Step 8 A-HEADER", "audited within
#   tolerance at Step 8", "Step 8 re-derives subtopic_id") has been restated against what
#   actually runs: the SAME canonical A-* catalogue, in audit_canonical.py, executed HERE
#   via [ExamCode]_mock_test_audit.py at S3-10 / S4-11. audit_canonical.py is KEPT and Step
#   6 B3 still generates the per-exam copy.
#   NO RULE WAS ADDED: audit.py remains OPTIONAL to run (S4-11's manual checklist still
#   substitutes when it is absent). What changed is the reporting duty — its absence must
#   now be stated explicitly in the batch report, because with no audit step downstream an
#   absent audit.py means NO machine gate ever runs over the paper.
#   ACCEPTED LOSS, stated once: subtopic_id, the answer key, the axis distribution and the
#   figure conformance verdicts are no longer independently re-derived by a second reader.
#   The Tier-A dossier (S13-4b) is still written; its consumer is now the author.
#
# v5.38 — 2026-08-03 — THE SELF-TEST BANNER REPORTED PASS OVER A FAILED RUN.
#   GAP-2026-08-03-BANNER. Caught at deployment review of v5.37, BEFORE it shipped.
#
#   v5.37 appended its 13 LABELFMT fixtures AFTER the line that prints
#   "SELF-TEST: {p}/{p+f} PASS". Reintroducing v5.37's OWN defect produced:
#         SELF-TEST: 37/37 PASS          <- printed first
#         Traceback ... LabelFormatError
#         exit=1
#   The exit code was correct, so the release gate still failed — but every human
#   reading the banner, and every spec quoting it, saw PASS over broken work. That
#   is the false-clean-banner shape (GAP-2026-07-26-003, "QV-9 PASS and a green Step
#   Complete footer"), reintroduced by the very release that was closing a sync bug.
#   14 assertions were outside the count: the true figure was 51, not 37.
#
#   SECOND, DEEPER DEFECT IN THE HARNESS ITSELF: ck(name, cond) receives an
#   ALREADY-EVALUATED condition, so an exception inside a fixture PROPAGATES and
#   ABORTS the whole self-test — every later fixture silently never runs. The
#   LABELFMT fixtures call resolve_option_label(), which RAISES by design. A hollow
#   branch in the test harness is worse than one in a gate: it hides all the others.
#
#   FIX. The banner is now the LAST thing computed, immediately before the return,
#   and names every failing fixture. New ck_call(name, fn) evaluates a fixture that
#   may raise and COUNTS A RAISE AS A FAILURE. Verified: clean run prints 51/51;
#   with v5.37's defect reintroduced it prints 46/51 with all five failures named
#   and no green banner anywhere.
#
#   PERMANENT CONTROL: validate_framework_md CHECK AQ — in any engine with a
#   self-test, no ck(/ck_call(/check( may appear after the banner print. Mechanical,
#   exact, and binds engines not yet written. Negative-tested.
#
# v5.37 — 2026-08-03 — OPTION LABEL RESOLUTION WAS RE-IMPLEMENTED, AND THE TWO
#   IMPLEMENTATIONS DISAGREED. GAP-2026-08-03-LABELFMT.
#
#   Found by a line-by-line Step-7/Step-8 sync audit, not by a failing run — it is
#   LATENT, and fires the first time any exam declares roman option labels.
#
#   THE DEFECT. This step turned the section_rules option_label_format notation
#   into a render template by testing the LEADING TOKEN'S CASING. It had no roman
#   branch and no else-branch:
#     'i/ii/iii/iv'      -> .islower() is True for 'i' -> ({alpha_lower})
#                        -> RENDERS (a)(b)(c)(d), while Step 8's
#                           option_label_family reads the same string as 'roman'.
#                           A-OPTLABEL then FAILS EVERY QUESTION, exit 1, Step 8
#                           refuses to certify, and NO CP repair can fix it because
#                           the paper matches THIS STEP'S OWN contract. Confirmed
#                           end-to-end on a rendered paper.
#     'I/II/III/IV'      -> identical failure via .isupper().
#     '(1)/(2)/(3)/(4)'  -> matched no branch, so the NOTATION ITSELF became the
#                           render template — a template with no {text} placeholder,
#                           i.e. no substitution at all.
#     '[A]/[B]/[C]/[D]'  -> silently became '(A)'.
#     circled digits     -> silently became '1.'  (Python .isdigit() is True for them).
#
#   FIX. Resolution moves to paper_pipeline.resolve_option_label(), which is routed
#   by BOTH MockCreate and TestCreate, so one function is reachable from both
#   steps and the pair cannot drift again. Roman is RENDERED, not aliased ({roman_upper}
#   / {roman_lower} tokens, also taught to the G-OPTLABEL prefix regex). The resolver
#   ASSERTS that the family this step renders equals the family Step 8 classifies and
#   RAISES LabelFormatError otherwise, so 'i/j/k/l' (renders alpha, classifies roman)
#   and '[A]/[B]/[C]/[D]' (renders alpha, classifies num) are REFUSED AT
#   PRE-GENERATION rather than producing a paper that could never certify. An
#   unrenderable notation hard-stops instead of guessing — the same posture as
#   pick_blueprint (PickError) and derive_nat_grading, and for the same reason: a
#   guessed label reaches the delivered paper.
#
#   VERIFIED BY ROUND TRIP: for all NINE supported notations, output rendered as
#   this step renders it passes Step 8's A-OPTLABEL / A-OPTORDER / A-OPTUNIQUE.
#   paper_pipeline self-test 22 -> 37. No existing notation changes behaviour.
#
# v5.36 — 2026-08-01 — GAP-2026-08-01-DELIVERY-SET-DRIFT: STEP 7 HARD-STOPPED AT
#   PRE-DELIVERY ON EVERY EXAM. v5.35 added the Tier-A dossier as a THIRD delivered
#   file (S13-4b) and did not widen S13-7 check 6, which asserted
#   `staged == {docx_name, reg_name}` — a hardcoded set of two. The third file made
#   the comparison false, S13-7 raised SystemExit, and Step 7 could not deliver.
#   Step 7 had been the one step in this pipeline that never failed; an improvement
#   made for Step 8's benefit broke it, and it would have failed on the FIRST run
#   after deployment.
#
#   WHY NOTHING CAUGHT IT. All six auditors reported zero findings, twice, plus a
#   fresh-clone deployment simulation — and they still would. NO CHECK ANYWHERE
#   cross-verifies the Step-7 closed deliverable set against what Step 7 actually
#   stages. validate_framework_md's cardinality check AK covers the 19 .py files of
#   the B3 bundle, a different contract. The delivery set was stated in prose at
#   four sites and asserted in code at one, with nothing binding them together —
#   the same "rule with no machine check behind it" class this corpus keeps
#   rediscovering, this time across a STEP BOUNDARY rather than inside one file.
#
#   THE FIX. S13-7 check 6 now DERIVES the expected set from what was written
#   (docx + registry always; dossier when S13-4b produced one) instead of
#   hardcoding a count, so a producer change and its gate cannot disagree by
#   construction. R-DELIVER, G-DELIVERY-SET and the §13 prose are corrected in
#   lockstep, and a new cross-file check (validate_framework_md CHECK AL) fails
#   the build if any site states a delivery-set cardinality the others do not.
#   Absent-safe: a pre-v5.35 mock writes no dossier and the set is exactly 2,
#   byte-identical to v5.34 behaviour.
# v5.35.1 — 2026-08-01 — self-test count refresh only (105/105 -> 107/107).
# v5.35 — 2026-08-01 — TIER A: emit [ExamCode]_M[N]_audit_dossier.json for
#   Step 8 (S13-4b). Facts only, never judgments; MD5-bound to the paper.
# v5.34.3 — 2026-08-01 — self-test count refresh only (89/89 -> 107/107, D2+D4).
# v5.34.2 — 2026-08-01 — self-test count refresh only (78/78 -> 107/107, C1).
# v5.34.1 — 2026-08-01 — self-test count refresh only (73/73 -> 107/107, B3).
# v5.34 — 2026-08-01 — FIGURESPEC TRANSPORT TO STEP 8
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT D2). One additive field at S13-4; zero
#   change to any render, any question, any gate, any deliverable.
#
#   WHAT WAS WRONG. v5.33 renders every figure through figural_core, and
#   render_figure() MUTATES the FigureSpec with what actually happened —
#   png_px, png_dpi, placed_in, placement_scale, font_pt_native — after reading
#   the saved artefact back. write_spec_sidecar() then drops that record beside
#   the PNG as q{N}_*.figspec.json. Step 8's thirteen figure-conformance
#   gates (v2.11 + A-FIGACCENT, v5.46) are arithmetic over the PNG AND ITS SIDECAR.
#
#   But the sidecars live in THIS session's working directory, which is internal
#   and is never delivered (S0-1 / R-DELIVER lists the closed set: the docx, the
#   registry, and — from v5.35 — the Tier-A audit dossier when S13-4b wrote one). So Step 8 saw spec == {} on every figure, fc.is_legacy() read
#   every v5.33 render as pre-v5.33 output, and EC-V18 leniency was applied to
#   papers that were not legacy at all. The gates could not fail on a real
#   regression because they never had the record to compare against.
#
#   THE FIX. S13-4 writes the sidecars into
#   registry.figural_manifests[].figure_specs, keyed by the canonical PNG name
#   S10-8 already stamps on each drawing (_name_last_drawing ->
#   "q{N}_problem.png" / "q{N}_opt{i}.png"), which is the same base
#   write_spec_sidecar() names the sidecar after. The registry is the sanctioned
#   channel for precisely this: it is the one artefact Step 8 receives, and it
#   is the precedent object_types/subtopic_ids set at v5.31 for the identical
#   reason. Absent-safe both ways — a session that rendered no figural_core
#   figure writes no sidecar, the field is {}, and Step 8 reads legacy, i.e.
#   exactly the pre-v5.34 behaviour. Nothing is written to the docx and nothing
#   new is delivered; B3/R-DELIVER cardinality is untouched.
#
# v5.33.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   1267 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestCreate'. The current companion block, the
#   v5.33 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v5.33 — 2026-07-29 — FIGURE COLOUR, LABEL LEGIBILITY AND PLACEMENT SCALE
#   (GAP-2026-07-29-FIG-R2 + VERIFY-2026-07-29-FIG-R2).
#   Measured across 208 delivered drawings in four exhibits: 0 of 55 IIT JAM figures
#   contained a single coloured pixel; placement scale was 0.500 EXACTLY on 24 of 24
#   option canvases; on-page labels ran to a median of 6.7 pt; 0 of 208 drawings
#   carried alt text. The three GATE papers, believed correct, measured 115 of 153
#   figures below a 9 pt floor — they were not a working reference, only a quieter
#   failure, and their colour came from session code that bypassed this spec entirely
#   (three distinct document-assembly paths across four exhibits).
#   FOUR root causes, not one:
#     RC-1 S10-7 Q7 MANDATED "solid black". The monochrome output was CONFORMANT.
#          The implementation was faithful; this spec was the defect.
#     RC-2 FIG_NATIVE_HEADROOM=2.0 supersampled the canvas and was never compensated
#          in the font size, while placement width came from a CONFIGURATION constant
#          rather than the saved artefact. p_page = p_native x S, and the spec
#          controlled neither S nor p_page. A 10 pt label landed at 5 pt.
#     RC-3 Nothing required colour to be redundant with a second visual channel, so
#          greyscale printing and colour-blind readers were served by luck.
#     RC-4 (found by VERIFY, absent from the gap) render_figural_image() sets
#          ax.axis("off") in BOTH branches, and the corpus contained no set_xlabel,
#          no set_ylabel, no legend, no rcParams and no fontsize anywhere. It is an
#          abstract-geometry GLYPH renderer and was being used for scientific data
#          figures, which it structurally cannot label. S8-5, the section that would
#          hold the data-figure path, was an empty title; insert_chart_image(), the
#          function that would call it, was referenced and never defined.
#   Fix: (1) new engine figural_core.py — the data-figure renderer the framework never
#   had, beside (not replacing) the geometry-glyph path. (2) S10-6A FIGURE CLASS
#   taxonomy; class is declared, never defaulted. (3) S10-7 Q2/Q3/Q7 rewritten, Q7b and
#   Q9 added. (4) S10-8 places from the FigureSpec and stamps alt text. (5) S8-5 filled.
#   DISPLAY WIDTH IS A LAYOUT DECISION AND STAYS FIXED; the render is solved to fit it.
#   The inverse rule (place every figure at its native size) was measured and REJECTED:
#   it inflates figure area 1.84x and makes a four-option MCQ need 10.4 in of option
#   stack against a ~9.0 in page text height, orphaning options from their stem.
#   FIG_NATIVE_HEADROOM is retired to 1.0 and bbox_inches="tight" is banned on this
#   path; constrained_layout gives the same margins with a deterministic size, so
#   S == 1.0 by construction rather than by luck.
#   G-FIGLABEL is ARITHMETIC over recorded render-time font metrics, NOT pixel
#   connected components: verified counter-example — three renders at an identical
#   10 pt request and identical saved width, and the one whose axis titles carried
#   "µmol photons m⁻² s⁻¹" and "Net CO₂ assimilation" measured 8.5 pt while
#   short-label renders measured above the floor. A pixel gate is biased against
#   exactly the scientific notation Q9.4 mandates.
#
```

## Framework_MockTestExplain.md

Entries v1.41.0–v1.53.1 moved at framework releases 2026.11.06 and 2026.11.07 (EC-P42; v1.54.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.53.1 — 2026-11-06 — GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY (handshake review of the
#   Step 7 -> Step 9 hand-over, run on a real paper). (1) P1: the engine self-test is run IN
#   the verified clone (`cd /tmp/fw && python3 explain_engine.py --self-test`). The old
#   wording copied explain_engine.py ALONE to /home/claude and ran it there; the engine
#   imports t3_mathcomp.py from its own folder, so that copy could not start
#   (ModuleNotFoundError) and P1 turns any self-test failure into a HALT. (2) S0-1 and S1-1
#   name the Step 7 deliverable by its real file name, [ExamCode]_[paper_slug]_Create.docx
#   (STEP_CONTRACTS.json; the P1 discovery already used it). No rule, gate, artefact or
#   deliverable of Step 9 changes.
#
# v1.53.0 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY (paired with blueprint_core
#   v1.32, paper_pipeline v5.40, audit_canonical v2.37, MockTestCreate v5.92, DeliveryFooter
#   v1.40.0). §7A-M: (1) the gate runs for EVERY paper — the MOCK-ONLY dormancy
#   ('scoped_paper') is lifted; a scoped paper (born DORMANT/scoped_paper) is evaluated and
#   written ONLY PASSED or DISCLOSED (guard S9); (2) WINDOW RULE w2
#   (bc.DIFFICULTY_GATE_BAND_WINDOWS_W2 = authoring bands; allowance over ASSESSED items,
#   'harder' disagreements only) is SELECTED by bc.difficulty_gate_window_rule from the
#   paper's own obs (r2 / level record = born under this release) — never typed; every
#   older paper stays on w1 byte-for-byte (guard G8); the writer stamps window_rule and the
#   coverage (assessed_frac / assessed_count / gated_count; gate_rule stays 'windows');
#   (3) the re-derivation obs copies rubric_rule from question_index, records
#   inferential_steps and derivation_confidence, and is scored by
#   bc.difficulty_score_from_obs under its own rule (a positional difficulty_score call
#   would re-score an r2 item under r1); a level item's measure is its clamped level band
#   with scores_by_q[q] = None for that item only; (4) `_score9 or None` is corrected to
#   `None if _score9 is None else _score9` (a valid 0 was "not measurable"); (5) coverage
#   under 80 % assessed (including 0) writes the verdict as computed and the footer prints
#   `Step 9: k/n assessed` — a "not assessed" DISCLOSED is never written. No new stop.
# v1.52.0 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (paired with
#   explain_engine v2.12, figural_core v5.89, corpus_io v1.17, MockTestCreate v5.89).
#   Explanation structures are drawn print-true at the paper's problem tokens with the
#   decisive site as a mark (no highlight band). MANDATE D: only a fidelity breach stops
#   (INFRA); every other self-audit finding is repaired in place ([HS:LADDER]).
# v1.51.2 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (paired
#   with corpus_io v1.16 / explain_engine canonical_structure twin, final_assembly v1.9,
#   MockTestCreate v5.88). PATCH, S13-2b only: (1) a REACTION object now canonicalises —
#   explain_engine.canonical_structure accepts reaction SMILES (reactants>agents>products),
#   so the registered scheme is reconciled per role like a STRUCTURE; (2) a question whose
#   registry record carries record_integrity (the S13-REGCHECK legacy annotation —
#   label/kind mismatch or a REACTION without '>>') is reconciled against the TRANSCRIPTION
#   ALONE with the annotation printed once (edge case E16): the registered object is known
#   to be a false or degenerate record and must not be used as a cross-check. No gate,
#   set or engine change here.
# v1.51.1 — 2026-10-09 — GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC (paired with
#   MockTestCreate v5.86, final_assembly v1.8, audit_canonical v2.31). registry
#   rc_manifests[] / di_manifests[] / figural_manifests[] are shared by EVERY series
#   (MOCK, SUBJ, TOPIC, SUBTOPIC) and, before final_assembly v1.8, were keyed only by the
#   bare ordinal "mock": N — so MOCK:M01 and SUBJ:X:01 (both N=1) overwrote each other.
#   Every entry Step 7 now commits carries "paper_id". P2 / P3 select THIS paper's entry
#   by paper_id == PAPER_ID; an entry with no paper_id is a LEGACY entry and belongs to
#   MOCK:M<mock> only; an entry is NEVER matched by the bare ordinal. No entry for this
#   paper = no manifest (the PAPER is the authority either way — unchanged).
# v1.51.0 — 2026-09-14 — GAP-2026-09-14-REGISTRY-SOURCE (REGISTRY-SOURCE-LAW; owner decision
#   2026-09-14; paired with MockTestCreate v5.84, MockDeliver v1.22.0, DeliveryFooter,
#   paper_pipeline CLUSTER RS). [ExamCode]_registry.json is REQUIRED by this step but no
#   longer has to sit in Project Files: it is lawful in EITHER lane — (1) attached to the
#   trigger in chat beside the _Create.docx, (2) Project Files. S19-0a resolves it through
#   pp.resolve_registry (the ONE implementation Steps 7/9/11 share): attachment WINS when
#   both lanes hold a file (a difference is PRINTED, never a stop); HARD STOP [HS:PROSE] only when
#   BOTH are empty; exact filename + registry.exam_code == [ExamCode] validated. The run
#   PINS the fingerprint it started from ({EXAMCODE}_registry_pin.json beside REG_WORK) and
#   every later turn's S19-0a refuses a DIFFERENT registry (pp.registry_source_check).
#   P10's FK tripwire reads the resolved source (REG_SRC['registry']) instead of a
#   hardcoded Files path; S19-0b's handoff fingerprint is REG_SRC['fingerprint']. S0-1
#   item 2 and the §19-4 badge prose name both lanes. Writers (Cluster DG), the closed
#   delivery set, the Replace badge, MS-14 and every artefact are unchanged — only WHERE
#   the file is read. Enforced by LAW_REGISTRY REGISTRY-SOURCE-LAW + mock_sync_audit MS-20.
# v1.50.0 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY: §7A-S STYLE RE-MEASURE (advisory). Step 9 recomputes
#   style_obs from the DELIVERED bytes and records mismatches against Step 7's record;
#   three dormancy reasons (profile_dormant, hash_mismatch, pre_v582_paper). Single-writer:
#   Step 9 writes style_gate.remeasure[paper_id] and nothing else in that container. The
#   P-series takes the authored distractor type as its default diagnosis, re-derives
#   independently (RE-6), and RECORDS BOTH on disagreement — never edits the question.
# v1.49.0 — 2026-08-30 — GAP-2026-08-30-EXPLAIN-COLOUR-BINDING (paired with explain_engine
#   v2.11, Framework_PYQExplain v2.21, routes.json: figural_core.py + corpus_io.py routed to
#   MockExplain / TestExplain / PYQExplain; SHARED_RULES_VERSION 1.5 → 1.6). Explanation
#   figures had NO colour contract — rdkit's default atom palette and matplotlib's
#   Category-10 defaults — so a question (Step 7 v5.80, pinned palette) and its explanation
#   disagreed on what an oxygen atom looks like, and a PYQ solution drew a third way.
#   S6A-6 COLOUR binds every renderer to figural_core (the palette owner) through the same
#   calls Step 7 uses (explain_engine.structure_draw -> corpus_io.structure_draw_fn, fc.text_ink,
#   fc.fill_style); P1 renderer
#   preflight import-tests those two engines and records it. Step-7 answer-leak rules
#   (monochrome colour-content, option-set uniformity, no-chrome) are explicitly NOT
#   transferred — an explanation shows what it explains. Additive: §6A-1..§6A-5, every
#   §6A-5 mechanic and every non-visual question are byte-unchanged; existing explanation
#   figures are never re-rendered.
# v1.48.0 — 2026-08-28 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ (paired with
#   explain_engine v2.10, Framework_PYQExplain v2.19, audit_seam v1.3,
#   validate_framework_md v3.2). Three CATEGORY-C config keys this spec read were
#   produced by NOTHING anywhere in the framework, so their absent-paths ran on every
#   exam forever: representation_renderers (every STRUCTURE_GRAPH / LEVEL_DIAGRAM /
#   DATA_PLOT / CONFORMER verdict degraded per §6A-4 — the §6A-1b structure-answer
#   presumption was defeated on every exam, every time), subject_code (the
#   [Subject]_EXPLAIN_LEARNINGS_v*.md library was unlocatable — its documented fallback
#   blueprint.subject is a key blueprint.json has never carried — so §24's subject
#   library and §7-7's curated neighbours had never loaded on any exam), and
#   exam_conventions (§S8-2's EXAM_CONVENTION machinery had no configured input).
#   FIX, exam-independent by construction, zero regeneration: (A) the requirement →
#   library → §6A-5 identifier binding is FRAMEWORK-OWNED and now lives in
#   explain_engine.REPRESENTATION_RENDERERS (§6A-6) — it states what the framework can
#   draw, not a property of any exam; WHETHER a question uses a renderer stays a
#   per-question §6A-1 decision, so non-scientific exams are byte-unchanged. (B)
#   subject_code is RETIRED; the subject library is found by DISCOVERY
#   (explain_engine.resolve_learnings_files — §24 places exactly ONE non-exam-prefixed
#   *_EXPLAIN_LEARNINGS_v*.md per project, so its presence IS the evidence; >= 2 →
#   abstain + WARN naming all candidates). (C) exam_conventions is RETIRED; §S8-2
#   reads conventions from the subject library only, "never assumed" preserved. No
#   section_rules.md schema change, no analyse_engine change, no exam regenerated.
#   Gate for the class: validate_framework_md Check V (SECTION_RULES CONFIG-KEY
#   CONTRACT) + audit_seam v1.3 prose-read widening.
# v1.47.0 — 2026-08-27 — REPAIR-RETIRED-2026-08-27 (operator decision; paired with
#   paper_pipeline v5.76, MockTestCreate v5.76, MockDeliver v1.18.0, DeliveryFooter v1.29,
#   audit_canonical v2.22). MINOR: a trigger and a section are removed. The four *Repair
#   triggers are RETIRED and §7A-R (TestExplainRepair / MockExplainRepair) is DELETED —
#   replaced by a retirement notice. THE DIFFICULTY GATE NOW DISCLOSES, IT NEVER BLOCKS:
#   §7A-M writes status='DISCLOSED' (rounds=0) where it wrote 'FAILED', prints a
#   ⚠️ PROCEED WITH DISCLOSURE box whose next step is the Deliver trigger
#   (pp.dg_next_step), and Step 11 delivers the paper with the §FOOTER-DG measured-
#   difficulty line. 'FAILED' is a retired status: pp.dg_write_verdict refuses it and
#   pp.dg_preflight heals a pre-v1.47.0 FAILED record to DISCLOSED/0 with a disclosed
#   migration line. PASSED/1 and DISCLOSED/1 (written by the retired repair step) stay
#   legal and deliverable as LEGACY repaired papers; a re-run of this step on one carries
#   the spent count (ROUND-MONOTONIC unchanged). S2-1: a _Create_Repaired*.docx upload is
#   a HARD STOP [HS:PROSE] on every trigger (rename a legacy repaired paper to _Create.docx; P3's
#   stem hash-match against registry.stem_texts proves identity). S19-0b: the repair-run
#   stop and HANDOFF_STEP's repair values are removed. PENDING is the ONLY blocking gate
#   state and its remedy is this step. No explanation rule changed.
# v1.46.3 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (prose only): §7A-M's level-anchor
#   text names the difficulty profile's calibration examples (bc.dp_calibration) in place of
#   section_rules' retired PYQ_DIFFICULTY_CALIBRATION. No rule, gate or engine change.
# v1.46.2 — 2026-08-26 — GAP-2026-08-26-REPAIR-BATCH-LAW (MockTestCreate v5.74; prose only).
#   S2-1 / §7A-R R2: a [ExamCode]_[slug]_Create_Repaired_PARTIAL_[k]of[K].docx (Step 7-R's
#   mid-batch cumulative paper) is REFUSED with "finish every repair batch — attach
#   _Create_Repaired.docx"; only the final _Create_Repaired.docx is a valid R2 input.
# v1.46.1 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM follow-up (prose only; paired
#   with paper_pipeline v5.74). REPAIRED-PAPER FILENAME. §7A-R attaches the TestCreateRepair
#   output, [ExamCode]_[paper_slug]_Create_Repaired.docx, and R2 says "parse (P3
#   machinery)" — but S2-1 and P1 named ONLY the _Create.docx form when parsing the paper
#   slug from the upload, so a literal repair run would refuse its own input (the v1.24
#   "_Complete" class, one filename later). S2-1 / P1 / §7A-R R2 now accept BOTH forms
#   and derive the slug by stripping whichever suffix is present; the repaired form is
#   accepted ONLY on a *Repair trigger, and a fresh TestExplain on a _Repaired.docx is a
#   HARD STOP [HS:PROSE] (a re-judge after a repair runs on the same repaired paper via
#   TestExplainRepair, never as a fresh explain). Found by the release's own
#   filename-chain re-verification. ALSO: S19-0 is split — S19-0a (session start at P1:
#   binds `reg`, the project fingerprint and persist_registry BEFORE §7A-M's preflight can
#   write) and S19-0b (delivery decision) — v1.46.0 defined all of it in the delivery
#   fence, so `reg`/persist_registry were unbound when §7A-M first needed them. No gate,
#   band or block rule changes.
# v1.46.0 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestCreate
#   v5.73, MockDeliver v1.16.0, DeliveryFooter v1.27, paper_pipeline v5.74 Cluster RH,
#   explain_engine v2.9, final_assembly v5.60; LAW_REGISTRY REGISTRY-HANDOFF-LAW,
#   mock_sync_audit MS-14). P0, every exam. §7A-M (v1.42.0+) writes the difficulty-gate
#   verdict into registry.json and calls the registry "the ONLY channel to Step 11" —
#   while S0-2, MANDATE D, S19-1 check 5 (`outputs == {Explanation.docx}`, a HARD STOP [HS:PROSE]),
#   §21 item 12 and DeliveryFooter §3 all still carried the pre-v1.42 "registry is frozen,
#   never delivered" rule, and the "S19 write" §7A-M relied on was defined nowhere. Under
#   a literal run the verdict lived only in /home/claude, the project copy stayed
#   (PENDING, 0) and Step 11 refused the paper on EVERY exam; §7A-R had no delivery
#   contract at all. Measured on the reference project: the registry reached the project
#   only because a session broke its own S19-1 gate. FIX: (1) NEW S19-0 — the registry
#   working copy, the ONE persist point every §7A-M / §7A-R write names, and the handoff
#   decision pp.handoff_set('TestExplain', …) driven by pp.registry_changed (a fingerprint
#   of the project copy vs the working copy) — never by prose. (2) S19-1 check 5 asserts
#   outputs == that closed set (pp.verify_handoff_outputs); S19-2 presents exactly it; the
#   final batch delivers Explanation.docx + registry.json (Replace in Project Files) +
#   the NEW report docx. (3) OPERATOR DECISION 2026-08-26: the §20 END-OF-MOCK REPORT is
#   ALSO written as [ExamCode]_[paper_slug]_Explain_Report.docx (explain_engine.
#   build_report_docx, MANDATE 0 enforced at the writer) and delivered at the final batch;
#   it is INERT downstream — Step 11 reads only registry.json + the Explanation docx —
#   so no next step requires it. (4) §7A-R gains its delivery contract: same Explanation
#   filename (spliced), registry.json (Replace), report docx (repair edition), F2 footer.
#   (5) S0-1/S0-2, MANDATE D, S2-2, §21-12 rewritten to the law; every "frozen / NOT
#   delivered" sentence is gone (MS-14 bans the wording corpus-wide). Every DG gate,
#   window, band and block rule is unchanged.
# v1.45.1 — 2026-08-26 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS follow-up (paired with
#   paper_pipeline v5.73, audit_canonical v2.20). §7A-M: a fresh round-0 verdict retires a
#   pre-repair stem snapshot taken for a different rework set (pp.dg_write_verdict), so the
#   mandated re-judge of a retired-rule paper cannot leave a stale snapshot that would fail
#   A-DGATE at delivery or make §7A-R R3 accuse a correct repair file. Prose + engine only.
# v1.45.0 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS (operator decision 2026-08-25;
#   paired with blueprint_core Cluster E2 split + E2d, paper_pipeline v5.72, MockTestCreate
#   v5.72, MockDeliver v1.15.0, DeliveryFooter v1.26). §7A-M's disagreement test moves from
#   band-label EQUALITY to per-band ACCEPTANCE WINDOWS on the raw rubric score, read from
#   bc.DIFFICULTY_GATE_BAND_WINDOWS by band POSITION (exam-agnostic): bottom band NOT gated;
#   middle agrees at 2–6 inclusive; top agrees at ≥5. bc.DIFFICULTY_GATE_MAX_DISAGREE_FRAC
#   0.30 → 0.35 (floor computed exactly). Step 9 records measured_score_by_q (bc.difficulty_
#   score) beside measured_by_q and passes windows + rework_directions ('harder'/'easier')
#   to pp.dg_write_verdict, which stamps gate_rule='windows'. A FAILED record WITHOUT that
#   stamp (v1.42.0–v1.44.0 rule) is re-judged by re-running this step — §7A-R R1, Step 7
#   §S16 P1 and pp.dg_next_step all route it there; it is never repaired. Verdict boxes and
#   footer show the bottom band as "(not gated)". Single-writer/state-machine contract of
#   v1.44.0 unchanged. Engine self-tests: blueprint_core 559 → 585, paper_pipeline 144 → 159.
# v1.44.0 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with
#   paper_pipeline v5.71 Cluster DG, final_assembly v5.58, MockTestCreate v5.71,
#   MockDeliver v1.14.0, DeliveryFooter v1.25, audit_canonical v2.19 A-DGATE).
#   P0 DEADLOCK. registry.difficulty_gate[paper_id] was read by four steps and written
#   by three (final_assembly, §7A-M, §7A-R) as hand-built dicts across two specs and
#   one engine, with no owner, no legal-state table, no write guard, no auditor and
#   no recovery path. A TestCreateRepair session set repair_rounds_used=1 on a
#   still-FAILED record; §7A-R R1 read the counter alone ("round used → TestDeliver"),
#   Step 11 read the status alone (FAILED → CreateRepair), TestCreateRepair refused
#   ("consumed") — no exit; a finished 60-question paper + explanation run lost. Two
#   more defects of the same class fired with NO repair: every SCOPED paper was born
#   PENDING while §7A-M is MOCK-ONLY, and a DORMANT gate wrote nothing — both left
#   PENDING forever, which Step 11 refuses. FIX: (1) the record is behind ONE writer,
#   pp Cluster DG — dg_stamp_pending / dg_write_verdict / dg_add_rework_snapshot —
#   each validating the (status, rounds) pair against the six generated legal states;
#   (FAILED,1) is now UNWRITABLE. (2) The legal state machine and DG-INVARIANT
#   (FAILED ⇒ 0) are declared in §7A-M. (3) Every preflight opens with
#   pp.dg_preflight, which heals a corrupt record deterministically WITH a mandatory
#   chat + footer disclosure and refuses an unknown status. (4) §7A-R branches on the
#   state PAIR and every next-step string is pp.dg_next_step — the function Step 11
#   prints from — so advice can never name a step that refuses. (5) DORMANT is a
#   WRITTEN verdict with a reason (incl. scoped_paper); a scoped paper is born DORMANT.
#   (6) The re-gate write is atomic/terminal/idempotent, logs a session_log entry, and
#   is round-monotonic (a full re-explain cannot grant a second round). (7) R3 uses
#   pp.dg_verify_repair against the pre-repair snapshot via the one shared digest
#   pp.dg_stem_hash; the contradictory stem_texts clause is gone. (8) audit_canonical
#   A-DGATE certifies every record; §S16-3 also snapshots every question so R3 proves
#   nothing unflagged changed; `python3 final_assembly.py --dg-fleet-scan ROOT
#   [--apply]` heals the ~200 existing registries with a .bak and a migrations trail.
#   Superseded v1.40.0 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
# v1.43.0 — 2026-08-24 — CHG-2026-08-24-NO-COVERAGE-BANNER (operator decision; paired with
#   PYQExplain v2.17, SHARED_RULES_VERSION 1.4 → 1.5; NO engine change). The S12-4
#   document-level coverage banner ("COVERAGE: Batch k of K …" / "COVERAGE: Complete -
#   all [Q_TOTAL] questions explained.") is RETIRED from every delivered Explanation
#   docx — interim AND final. Step 9 no longer calls explain_engine.set_coverage_banner();
#   the delivered file's first non-blank body paragraph is Q.1. Two facts decided it:
#   (1) the operator does not want a coverage line in the delivered document, and
#   (2) Framework_MockDeliver S4-2 treats ANY non-blank paragraph before Q.1 as an
#   upstream regression — detect_header_paras() strips it and raises a REGRESSION ALARM
#   — so the final banner S12-4 mandated was exactly what Step 11 flagged. The §18-1
#   checklist item is inverted (zero banner paragraphs; first non-blank paragraph is
#   Q.1) so a stale-session banner can never ship. Coverage is still stated in chat
#   (S19-3 progress line, F1/F2 footer) and asserted per batch (S4-5 guard 3) — nothing
#   about coverage CHECKING changes, only the in-file announcement. Engine untouched:
#   set_coverage_banner()/strip_solutions() and the BANNER-* fixtures stay (the
#   function is simply never called; BANNER-REMOVABLE already licensed dropping it).
# v1.42.0 — 2026-08-24 — GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING (paired with MockTestCreate v5.69,
#   MockDeliver v1.13.0, blueprint_core Cluster E2d, audit_canonical check 9,
#   final_assembly PENDING stamp). §7A-M promoted from advisory to BLOCKING:
#   band disagreement >30% (floor) blocks delivery and writes a rework order;
#   new §7A-R repair mode (TestExplainRepair / MockExplainRepair) patches only
#   the reworked questions, re-gates, and after the single permitted round
#   resolves to PASSED or DISCLOSED — never a stop, never silent.
# v1.41.0 — 2026-08-24 — GAP-2026-08-24-STEP9-AUDIT-R3 (executable dry run; paired
#   with final_assembly v5.56, audit_canonical v2.16, MockTestCreate v5.67). A harness
#   drove ten synthetic exams through the REAL Step-7 writers and then Step 9's P1→P3→
#   P10→S4-2→S4-4→§7-8→§18→S19-1 in spec order, then Step 11's preflight. Two defects
#   no reading could see: (1) OPTIONS-BY-Q SERIES COLLISION — P3 read
#   registry.options_by_q[str(N)], a paper-ORDINAL key that a scoped paper of the same
#   ordinal overwrites on the shared registry (measured: Mock 1 hard-stopped at
#   parse_paper after SUBJ:PHYS:01 was committed). P3 now reads the paper_id key first
#   (final_assembly v5.56 authority), str(N) second with a WARN. (2) SIBLING-EXAM GLOB —
#   P1 and P10 loaded every [ExamCode]*_blueprint.json and only checked exam_code AFTER
#   pp.pick_blueprint; with EXAM_A and EXAM_AB in one project pick_blueprint raised first
#   with a misleading "remove duplicate blueprints", and P10's own next(...) would have
#   silently taken EXAM_AB's file (sorts first). Both now filter exam_code == [ExamCode]
#   BEFORE selecting. Also §15-2 now names the engine's record fields for both provenance
#   modes (the harness's first MODE B block was refused for a field the spec never named).
#   Superseded v1.39.0 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
```

Section §7A-R (REPAIR MODE, v1.42.0–v1.46.3) RETIRED and moved here VERBATIM at framework
release 2026.08.27.3 (REPAIR-RETIRED-2026-08-27, operator decision). Not executable.

````
Entry v1.54.0 moved at framework release 2026.11.08.1 (GAP-2026-11-07-RE25-HARDENING; v1.55.0 supersedes).

```
# v1.54.0 — 2026-11-07 — GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS (RE-25 CHEM-STRUCTURE
#   STANDARD; paired with PYQExplain v2.28, explain_engine v2.13, corpus_io v1.19, figural_core
#   v5.91, SHARED_RULES_VERSION 1.7, the repo-shipped CHEMISTRY_EXPLAIN_LEARNINGS_v1.md).
#   Incident: CSIR NET Chemical Sciences 18-Jul-2026 — 120 questions, 34 structure questions,
#   ZERO explanation figures, 11 chemistry defects, every key right: the router said PROSE,
#   the renderer drew one molecule, figures could land only in DEDUCTION, nothing compared
#   the derived product with the keyed option, the chemistry library had never loaded.
#   NEW RE-25 (decided per question from CONTENT — never a subject, topic or exam name, §6A-7
#   T1-T3, ask shapes A1-A12): every step drawn inside DEDUCTION with curly arrows (E-03
#   proved), every wrong option drawn under its own heading (E-05), every figure layout-gated
#   and auto-retried (E-04), reviewed once in-turn (E-09), reconciled with the options (E-06
#   c-e, E-07), stereo descriptors re-derived (E-06 f), per-step balance (E-06 g), pipeline
#   vocabulary banned (E-08). NEW §6A-7..§6A-12, §7-0d / §7-0e, §24 S24-7; amended §5-1 /
#   §5-3, §6-1, §6A-1 / 1b / 2 / 3b / 5 / 6, §7-2, §8-3 / §8-5, §15-2, §18-1, §R3, §21.
#   option_smiles come from the registry; a key that is not the derived product is a Step 7
#   defect under §17-3 (EC-39), never a NEAREST-OPTION disclosure.
#   No new section heading; a NOT_APPLICABLE question takes no new obligation and renders
#   byte-identically (GAP Section 10.1; engine fixture AT-4 b).
```

## §7A-R — REPAIR MODE (TestExplainRepair / MockExplainRepair, v1.42.0; v1.44.0 — STATE-PAIR PREFLIGHT, ATOMIC RE-GATE; v1.45.0 — WINDOWED RE-GATE)

  TRIGGER: `TestExplainRepair P[N]` or `MockExplainRepair M[N]`.
  ATTACH:  (1) the REPAIRED question paper docx (TestCreateRepair output) and
           (2) the PREVIOUS explanation docx (this step's earlier output).
  PREFLIGHT (HARD STOP on any failure — these protect the operator from
  repairing the wrong thing, so they stay hard even under the no-stop rule,
  which governs the VERDICT, not malformed input):
    ORDER IS FIXED: R0 → R1 → R2 → R3. Registry legality is checked BEFORE
    anything about the operator's files, because a corrupt registry makes
    every downstream verdict meaningless and its remedy has nothing to do
    with the attachments.
    R0  rec, disclosure = pp.dg_preflight(reg, paper_id, where='§7A-R R0')
        An ILLEGAL (status, repair_rounds_used) pair is NOT "a round already
        used" — it is a CORRUPT REGISTRY, healed here per DG-INVARIANT (a
        FAILED record's counter is reset to 0: the round is provably
        unconsumed). If disclosure is not None: print disclosure['line']
        verbatim in chat, persist the registry (S19-0 write), and CONTINUE. A DGIllegalState
        (unknown status) is a HARD STOP: print its message verbatim. Never
        route the operator onward on an illegal record — the historical
        failure was exactly that (FAILED + 1 → "go to TestDeliver" → Step 11
        hard-stops on FAILED → TestCreateRepair refuses "consumed" → no exit).
    R1  BRANCH ON THE STATE PAIR pp.dg_state(rec), never on one field. Every
        next-step string is pp.dg_next_step(reg, paper_id, N, mock=<Mock*
        trigger>) — the SAME function Step 11 prints from — never restated:
          absent            → "This is a legacy paper (no gate record) —
                               nothing to repair. Next step: " + next_step
          ('PENDING',   0)  → "Run TestExplain P[N] first — the gate has not
                               run. Next step: " + next_step
          ('FAILED',    0)  → if pp.dg_is_windowed(rec): PROCEED (the one and
                               only repair round). Else (v1.45.0 — the record
                               was judged FAILED under the retired band-
                               equality rule, GAP-2026-08-25-DIFFICULTY-GATE-
                               WINDOWS): "This paper was judged under the old
                               difficulty rule — nothing is repaired on its
                               say-so. Next step: " + next_step (which is the
                               Explain trigger: re-run it so the verdict is
                               re-judged under the windows). HARD STOP.
          ('PASSED',    0)  → "Nothing to repair — next step: " + next_step
          ('PASSED',    1)  → "Already repaired and passed — next step: " + next_step
          ('DISCLOSED', 1)  → "The one repair round is already used — next
                               step: " + next_step + " (delivers with disclosure)."
          ('DORMANT',   0)  → "This paper's gate is dormant ([dormant_reason])
                               — nothing to repair. Next step: " + next_step
        (No other pair can reach R1: R0 healed or refused it.)
    R2  Both attachments present and parse (P3 machinery): the
        [ExamCode]_[paper_slug]_Create_Repaired.docx paper (S2-1 / P1 accept this
        form on this trigger — v1.46.1) and the previous
        [ExamCode]_[paper_slug]_Explanation.docx; both must carry the SAME
        paper_slug as the trigger's paper N (P10/0 identity gate) or HARD STOP.
    R3  Stem diff against the PRE-REPAIR SNAPSHOT ONLY, via the shared digest:
          v = pp.dg_verify_repair(rec, {q: <first-paragraph text of q in the
                                         REPAIRED paper, raw — see
                                         pp.dg_stem_hash> for q in 1..N})
        v['missing_snapshot'] → HARD STOP: "The repaired paper was produced
          without §S16-3's snapshot — re-run TestCreateRepair P[N]." Never
          fall back to registry.stem_texts (TestCreateRepair has already
          overwritten it with the post-repair stems, and it is a flat
          append-only list across all papers with no defined per-paper
          offset).
        v['ok'] is False → HARD STOP naming v['changed_unlisted'] ("changed
          questions the gate did not flag: Q…" — detectable only when the
          §S16-3 snapshot carries baseline_stem_hashes for every question;
          v['extras_verifiable'] says whether it does; a pre-v5.71 snapshot
          without it verifies the flagged questions only, and the run says
          so in §R10) and/or v['unchanged_listed']
          ("failed to change a flagged question: Q… — if ALL of rework_qs is
          listed here you attached the PRE-repair paper by mistake"). It is
          the wrong file.
        pp.dg_stem_hash is the ONE digest (sha256 of the raw first paragraph
        including the "Q.<n>" label, no normalisation); §S16-3 computes the
        snapshot with the same function. Neither side implements its own.
  RUN: execute §4–§18 for the rework_qs ONLY (batching rules apply to that
    subset); splice the regenerated per-question blocks into the previous
    explanation docx, replacing the superseded blocks in place (block = the
    question's full §2 structure); leave every other block byte-identical.
  RE-GATE: rebuild scores_by_q AND measured_by_q for the untouched qs from
    the record's measured_score_by_q / measured_by_q (the engine accepts the
    record's str keys) and update BOTH for the repaired qs only; re-run
    bc.evaluate_difficulty_gate(labels_by_q, measured_by_q, difficulty_labels,
    scores_by_q=scores_by_q) over the FULL maps with the engine defaults;
    then ONE write, via the single writer:
      pp.dg_write_verdict(reg, paper_id,
          status='PASSED' if gate['verdict'] == 'PASS' else 'DISCLOSED',
          rounds=1, threshold=gate['threshold'], bands=<as §7A-M>,
          measured_by_q=measured_by_q, rework_qs=gate['rework_qs'],
          scores_by_q=scores_by_q,
          rework_directions=gate['rework_directions'],
          windows=gate['windows'])
    (on DISCLOSED, rework_qs / rework_directions document what remains out of
     window; no further repair command is printed.)
    ATOMIC, TERMINAL, IDEMPOTENT (v1.44.0). The counter and the status are
    written ONCE, TOGETHER, at the END of a successful re-gate, by that call.
    NEVER increment repair_rounds_used on ENTRY, never in a separate write,
    never by hand — an entry-time increment that crashes before the re-gate
    reproduces the deadlocked (FAILED, 1) pair by a second route, and
    pp.dg_write_verdict refuses that pair outright. A run that crashes
    mid-repair therefore leaves (FAILED, 0) untouched and is simply RE-RUN:
    safe, because TestCreateRepair's rework_stem_hashes snapshot is the
    PRE-repair evidence and is carried forward unchanged by every re-gate.
    SESSION LOG — in the SAME registry write, append the evidence trail:
      reg.setdefault('session_log', []).append({
          'step': 'TestExplainRepair' (or 'MockExplainRepair'),
          'paper_id': paper_id, 'round': 1, 'verdict': gate['verdict'],
          'qs': rec['rework_qs']   (the PRE-repair list read at R0 — NOT
                                    the re-gate's new rework_qs),
          'timestamp': <utc-now>,
          'spec': 'Framework_MockTestExplain v1.44.0 §7A-R'})
    Recovery does NOT depend on this entry (DG-INVARIANT makes the record
    self-diagnosing); without it no later audit can reconstruct what ran.
    Resulting status:
      PASS → 'PASSED'   — print the PASSED box (§7A-M shape).
      FAIL → 'DISCLOSED' — the one round is spent; NO further loop and NO stop
             (operator decision). Print:
      ════════════════════════════════════════════════════════════
        DIFFICULTY GATE: ⚠️ PROCEED WITH DISCLOSURE
      ════════════════════════════════════════════════════════════
        After 1 repair round: [bottom] [n] (not gated) · [middle]
        [b]/[m] in window · [top] [c]/[h] in window. The paper MAY
        be delivered; the delivery footer will state these measured
        counts so no reader is misled.
        Next step:  TestDeliver P[N]
      ════════════════════════════════════════════════════════════
    (the "Next step" line is pp.dg_next_step(...) verbatim; on a DISCLOSED
     record it is guaranteed to be the Deliver trigger, which Step 11 accepts.)
  DELIVERABLES (v1.46.0 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM; this section had NO
    delivery contract through v1.45.1, so the re-gate verdict stayed in /home/claude and
    Step 11 kept reading (FAILED, 0) from the project). The CLOSED SET, one present_files
    call, F2 footer, is pp.handoff_set('TestExplainRepair', …, final=True) — run S19-0b →
    S19-1 → S19-2 → S19-4 exactly as a final batch, with FINAL_BATCH = True and
    HANDOFF_STEP = 'TestExplainRepair' (or 'MockExplainRepair'):
      1. [ExamCode]_[paper_slug]_Explanation.docx — the previous explanation docx with
         the rework_qs blocks replaced in place, SAME filename (Step 11's S1-2 gate
         accepts exactly this name)                                → Use locally
      2. [ExamCode]_registry.json — carries the re-gate verdict (PASSED/1 or DISCLOSED/1)
         + the session_log entry                                   → Replace in Project Files
      3. [ExamCode]_[paper_slug]_Explain_Report.docx — the §20 report regenerated as the
         REPAIR EDITION (§R1 states "repair round 1"; §R3 lists the rework_qs re-explained;
         every other section reports the whole paper as it now stands) → Use locally
    The re-gate is ONE write (above); pp.registry_changed is therefore True on every
    successful repair run, and a run whose registry is unchanged has NOT re-gated — S19-0
    HARD-STOPS it rather than deliver a stale verdict (S19-0b).
````

Entry v1.40.0 moved at framework release 2026.08.25.3 (EC-P42; v1.44.0 supersedes).

```
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
```

Entry v1.39.0 moved at framework release 2026.08.24.3 (EC-P42; v1.41.0 supersedes).

```
# v1.39.0 — 2026-08-22 — GAP-2026-08-22-STEP9-READ-SET (EC-P42; deploy follow-up #2
#   of 2026.08.21.2). New S0-3: FINAL vs NON-FINAL session class with a GENERATED
#   read set — a NON-FINAL batch session skips §20 (end-of-mock report), §22 (its
#   §R9 disclosure input) and APPENDIX A; escalation to a full read is mandatory and
#   one-way before §20 runs. §20–§24, APPENDIX A and FOOTER banners promoted from
#   '# ' to '## ' so spec_sections.py can address their spans (IDs unchanged; no
#   consumer reads header levels — verified by corpus grep). Ranges live in
#   SPEC_SECTIONS.json (has_read_set), hash-tracked, never hand-copied. The
#   MockExplain/TestExplain route is now budget-covered by design, not by headroom.
```

Entry v1.38.0 moved at framework release 2026.08.24.1 (EC-P42 discipline; v1.40.0 supersedes).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.38.0 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (MOCK-ONLY; pairs
#   MockTestCreate v5.60). New §7A-M: Step 9 re-scores every question on the shared
#   rubric (blueprint_core.assess_difficulty) at THIS exam's level and reports
#   agreement with Step 7's labels (dashboard + §R10). Report-only; sticker wins.
#   Resolves the §7A divergence note (same RUBRIC, different mechanisms; PYQExplain
#   v2.16). No shared §4–§18 rule modified; SHARED_RULES stays 1.4. Superseded
#   v1.37.0 entry moved verbatim to SPEC_HISTORY.md (EC-P42, 2026.08.20.9 discipline).
```

Entry v1.37.0 and two in-section narrations moved at framework release 2026.08.21.3
(EC-P42 route budget — MockExplain/TestExplain crossed 250,000 B; SPEC-BUDGET gate).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.37.0 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paired with
#   PYQExplain v2.15, engine v2.8, MockTestCreate v5.59, paper_pipeline v5.39,
#   final_assembly v5.55). The first v1.36.0 paper passed every §18 gate and (1)
#   PUBLISHED A WRONG KEY on a figural item (structure misread; Step 7, holding the
#   opposite key, was by design never consulted); (2) carried 24 hedged WHY WRONG /
#   PITFALL lines, nine with FALSE arithmetic — §15-2's "a real path always exists"
#   forced invention; (3) 0 NARROWED over 60 AXIOMs while the loaded library named
#   the overgeneralised families; (4) every prose formula ASCII. ROOT CAUSE: gates
#   proved a protocol was DECLARED, not DONE. FIXES: §7-8 KEY RECONCILIATION (hash
#   commitments, resolved IN-RUN); §13-2b SEMANTIC-OBJECT RECONCILIATION; §15-2
#   REWRITTEN (two modes, engine RECOMPUTES, hedges banned, no quota); §7-7 step 3
#   MECHANICAL (Triggers + tripwire); §8-0c TYPOGRAPHY; §6A-1b-ii; §17 REWRITTEN
#   (never halt); RE-1/13/16 amended, RE-23/24 new; §18/§20/§21/§24 hooks.
#   SHARED_RULES 1.3→1.4.
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockTestExplain.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14, and again at 2026.08.19.1 (v1.25.0–v1.34.0 — the
#   MockExplain/TestExplain route had crossed the EC-P42 SPEC-BUDGET threshold)
#   (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.```

In-section narration moved from §24 (operational summary retained in-spec):

```
#   v1.21.0 — THE AUTOMATIC PRODUCER IS GONE. Step 10 was this loop's producer: it distilled
#   the defects it had to FIX into reusable AL-rules so the same mistake was not authored
#   again. With Step 10 retired, NOTHING generates AL-rules automatically any more. This
#   section remains as the CONSUMER half only: any AL-rule file already accumulated stays
#   valid and is still loaded and obeyed, and new rules may be added BY HAND by the author.
#   The schema below is frozen so existing files keep parsing; there is no producer half to
#   keep pinned to it.
#
```

In-section narration moved from the Appendix (operational facts retained in-spec):

```
#   WHY THE LISTING WAS REMOVED (v1.12): through v1.11 the full engine was reproduced
#   verbatim in this Appendix AND in the (now retired) ExplainAudit spec's Appendix A "for
#   self-containment" — but a reproduced copy and the standalone can silently DESYNC, and
#   the v1.8/v1.9 changelog records that this ALREADY happened once (the embedded copy
#   lagged the standalone's step-number + code fixes). A single canonical copy removes
#   that failure mode — the same multi-copy-drift fix the retired audit steps applied
#   to their auditors. The framework linter (validate_framework_md.py) runs
#   explain_engine.py's `--self-test` directly.
#
```


# v1.36.0 — 2026-08-20 — GAP-2026-08-20-TRANSFER-SAFE-EXPLANATIONS (paired with
#   PYQExplain v2.14, engine v2.7). A DELIVERED 60-question paper passed every §18
#   gate with every answer correct and still carried ~17 sentences TRUE FOR THE ITEM,
#   FALSE FOR ITS NEAREST NEIGHBOUR ("electron-withdrawing → meta" vs halogens; "one
#   carbon richer"; "stable carbonylate = 18e"; "always a meso form"; "cannot … at
#   all"), plus "The seductive half is …" on 10/10 MSQ blocks — mandated by §15-3's
#   own wording. Answer-level gates are blind to this. ROOT CAUSE as in v1.35.0:
#   §8-0b / §14-3b / §8-2 ADVISED what only a gate enforces; §6A tested PRESENCE, not
#   ALIGNMENT. FIXES (domain-neutral): NEW §7-7 TRANSFER-SAFETY PROTOCOL (scope →
#   type → neighbour test → repair by MECHANISM → recorded transfer_record); §8-2
#   epistemic type; §8-3 minimum components (subject data); §8-0b a GATE (kept
#   absolutes declared; plain quantifiers NOT gated — 80% false positives measured);
#   §14-1 three-part + §14-5 four fields; §15-3 MSQ rewritten, old wording WITHDRAWN,
#   psychology phrases engine-banned; NEW §6A-1c ALIGNMENT, §6A-3b tripwire,
#   CONFORMER (F3); §24 SUBJECT-level learnings file + §24-5 codes; §5/§18/§R3/§21
#   hooks; engine fixes F2. SHARED_RULES 1.2→1.3. Student format LOCKED.

Moved from the file header at framework release 2026.08.15.14; entries
v1.25.0–v1.34.0 moved VERBATIM at framework release 2026.08.19.1, and
v1.35.0 at framework release 2026.08.20.9 (both times the
MockExplain/TestExplain route had reached the EC-P42 SPEC-BUDGET
threshold — 287 B of headroom remained at the second move).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.35.0 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-EXECUTION-INTEGRITY (paired with
#   PYQExplain v2.13, engine v2.6). Four defects, one root cause, found by auditing a
#   DELIVERED 60-question paper: each traced to a rule that ADVISED what only a gate
#   can enforce — prompt policy treated as enforcement.
#   D1 — INTERNAL ERROR-TAXONOMY TOKENS RENDERED TO STUDENTS. Every WHY WRONG entry in
#   the reference paper opened with the raw snake_case token ('regiochemistry_error:
#   the para phenol ...'; 40 option entries + 20 NAT pitfalls). CAUSE: §9/§15-2 asked
#   the first line to "name an error type" and nothing separated the internal name
#   from the rendered sentence — the §9 taxonomy is itself snake_case, so obeying the
#   rule literally printed machine metadata into a learner document. FIX: the §9
#   diagnosis is METADATA — still mandatory, recorded per wrong option/pitfall in
#   progress state — and the visible line states the same content in natural language.
#   Engine v2.6 raises at write time on any taxonomy token in student-facing text AND
#   re-scans the rendered bytes at verify time, so the leak cannot ship by either path.
#   D2 — ROUTING WITHOUT EMISSION. The same paper carried 46 question-region images
#   and TWO explanation figures, on a structure-heavy paper whose section_rules
#   declared renderers; structure-decisive DEDUCTIONs ended at "the structure drawn in
#   Option N". The §6A router classified and the renderer shipped prose — the defect
#   §6A exists to remove, standing because verdict and emission were never tied
#   together. FIX: NEW §6A-1b (structure-answer presumption: when the verified answer
#   IS a structure, STRUCTURE_GRAPH is presumed and PROSE requires a recorded
#   justification naming where the prose carries each decisive feature); §6A-3 now
#   passes the verdict INTO the block and engine v2.6 enforces coherence — a visual
#   verdict with zero figures raises at construction; a §6A-4 degrade records the
#   DEGRADED requirement, never the original.
#   D3 — SPEED HACK ON 56 OF 60. §14's omit-by-default held per question and nothing
#   measured the AGGREGATE, so inclusion pressure won 93% of the paper, several
#   "hacks" restating the DEDUCTION (a §14-1 part-1 failure each). FIX: NEW §14-5 —
#   eligibility recorded per question (distinct/faster/scoped), the inclusion RATE
#   reported in §R3, and a batch at 100% inclusion re-runs the §14-1 test per question
#   before §18. A TRIPWIRE, never a quota: a genuinely shortcut-rich batch survives
#   its re-audit unchanged.
#   D4 — TWO REASONING DISCIPLINES WITH NO RULE. (a) A correct final answer can carry
#   mutually incompatible intermediate claims — derive-twice compares ANSWERS, §7-5
#   audits the final VALUE, neither reads the reasoning: NEW §7-6 decisive-claim
#   consistency — an explanation whose claims cannot all be true is invalid even when
#   the answer matches; repair returns to §7-1, never to patched prose. (b) Counting
#   questions were OPENED from a closed-form ceiling before the elements it assumes
#   independent were inventoried: NEW §7-0c enumeration-before-formula. Both stated
#   domain-neutrally per the v1.33.0 convention; the incident's domain appears only as
#   a labelled illustration. RE-6d added; RE-13 restated (diagnosis internal, rendered
#   naturally); §5-1/§5-2/§5-3, §18, §R3 and §21 carry the matching hooks.
#   ALSO (engine v2.6, found while writing its fixtures): the v2.3 figure-validation
#   loop sat AFTER the NAT branch's return, so a NAT block's figures were NEVER
#   validated at construction — moved above the type split (NAT-FIG-VALIDATED locks
#   it); an anomaly block now rejects figures as student content; an AXIOM naming an
#   option label raises (§8-2 — binding is the DEDUCTION's job).
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
# v1.34.0 — 2026-08-19 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT (paired with
#   PYQExplain v2.12, engine v2.5). SPEC-ONLY here; the paired ENGINE release fixes a
#   separate, unrelated label defect found the same way (see explain_engine v2.5).
#   THE DEFECT. section_rules declares `option_label_format` in TWO places — the
#   CATEGORY C header and every per-SECTION block — and P5 compared NEITHER. It checked
#   option COUNT, question TYPE and Q_TOTAL, and it checked opt_re against label_scheme,
#   but the declared label FORMAT was never compared against itself. A real exam config
#   was found carrying `(A)/(B)/(C)/(D)` in the header and `1/2/3/4` in all FOUR of its
#   section blocks. The run did not halt. It silently took the header, and every option
#   in the paper was printed with the wrong label.
#   WHY IT IS SILENT AND TOTAL. The two values come from DIFFERENT generators: the header
#   is written from OBSERVED PYQ papers, the per-section values from per-section
#   synthesis. Re-running the PYQ analysis can change the header alone and leave every
#   section untouched. Nothing else in the run looks wrong — counts match, types match,
#   the paper renders cleanly — so there is no second symptom to notice.
#   THE FIX. P5 now compares the header against EVERY section and the sections against
#   each other, and HALTs on any disagreement, printing every declared value with its
#   location. Resolution by precedence is explicitly forbidden: "Surface, do not guess"
#   already governed this step and the missing comparison was the only reason it could.
#   SCOPE, NOT OVERCLAIMED. Labels are PRINTED by the generation step; this step reads
#   them. Halting here cannot un-print an already-generated paper — it stops an
#   explanation run from cementing wrong labels and sends the author to fix the config
#   and regenerate. The same comparison belongs upstream in generation; that this one is
#   downstream is a reason to surface loudly, never a reason to resolve silently.
# v1.33.0 — 2026-08-19 — GAP-2026-08-19-DOMAIN-LEAK-IN-UNIVERSAL-RULES (paired with
#   PYQExplain v2.11). SPEC-ONLY, no engine change, NO rule weakened — every obligation
#   added in v1.31.0/v1.32.0 still binds. What changes is that four of them were written
#   in ONE domain's vocabulary while sitting in an EXAM-AGNOSTIC spec that serves every
#   exam in the corpus.
#   THE DEFECT. §7-0a listed conditions as "solvent · pH · catalyst · ligand · WORK-UP";
#   §7-0b listed assumptions as "ideal-gas · activity ~ concentration · spin-only";
#   §7-5 made "temperature in KELVIN" and "STOICHIOMETRY — the mole ratio comes from the
#   BALANCED relation" MANDATORY checks; §8-0a banned "bond angles, spectral positions,
#   industrial temperatures". Read by an aptitude, language or reasoning paper, those are
#   not merely irrelevant — §7-5 in particular demanded checks that CANNOT be satisfied or
#   even understood, so a conformant paper in another domain could not pass its own
#   checklist. That breaches the EXAM-AGNOSTIC GUARANTEE at the top of this file.
#   THE FIX, following the convention the corpus already uses elsewhere ("config triggers;
#   default NOT/EXCEPT/INCORRECT/FALSE"): the RULE is stated in domain-neutral terms, the
#   LIST is marked ILLUSTRATIVE and read from the exam's own material, and every §7-5
#   check is explicitly CONDITIONAL ON APPLICABILITY — a check whose subject the question
#   does not contain is NOT APPLICABLE and is NOT a failure. Domain examples are retained
#   deliberately, because a rule with no worked instance is hard to apply, but each is now
#   labelled as one domain illustrating a universal shape.
#   WHY IT HAPPENED, recorded so it is not repeated: these four rules were written from a
#   chemistry incident, and the incident's vocabulary travelled into the rule. Every
#   earlier release in this series was audited for exam-independence by absence of exam
#   NAMES and counts — a test that these passed, because a domain leak carries neither.
# v1.32.0 — 2026-08-19 — GAP-2026-08-19-CONDITIONAL-CORRECTNESS (paired with PYQExplain
#   v2.10). SPEC-ONLY, no engine change. Four rules covering the same underlying failure:
#   an answer that is RIGHT IN GENERAL and WRONG HERE, because a condition, an
#   assumption, a unit or a scope was never made explicit. Derive-twice does not catch
#   this class — both routes can share the same silent premise.
#   D1 — §7-0a CONDITION CAPTURE. Nothing required the SOLVER to read back the conditions
#   a remembered result depends on. §9's `wrong_condition` names this failure in a
#   DISTRACTOR only, which is a different obligation — the same error-type-standing-in-
#   for-a-rule confusion that let two defects survive an earlier audit. Reference case:
#   ozonolysis, where the WORK-UP alone decides between an aldehyde and a carboxylic acid.
#   D2 — §7-0b ASSUMPTION LEDGER. Ideal gas, activity ~ concentration, small-x, spin-only,
#   298 K, standard state. Three cases; only an assumption that MATERIALLY changes the
#   answer reaches the reader, and it may never contradict the stem.
#   D3 — §7-5 NUMERICAL VERIFICATION. Derive-twice catches a DIFFERENT-answer error, never
#   a CONSISTENT one: both routes can share one unit slip, one log base, one power of ten.
#   Seven orthogonal checks — units, conversions/kelvin, magnitude, log base, sign,
#   stoichiometry, precision — run on the final value. A failure returns to §7-1, never to
#   a patched number.
#   D4 — §14-3b SHORTCUT VALIDITY DOMAIN. §14 tested whether a shortcut was DISTINCT and
#   FASTER, never whether it was SCOPED. A SPEED HACK is the line a student memorises, so
#   an unscoped one is the most damaging sentence in the block. Distinct from §8-0b:
#   "a bulky base usually gives the less substituted alkene" is calibrated (passes §8-0b)
#   and still unscoped (fails §14-3b) because it never says WHEN to reach for it.
# v1.31.0 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-CONTENT-DISCIPLINE (paired with
#   PYQExplain v2.9, engine v2.4). Three defects that were IDENTIFIED at the start of
#   this work, survived every release since, and were nearly closed out unfixed: an
#   internal audit reported them CLOSED on loose keyword matches that hit adjacent
#   text. A test that can only pass is not a test.
#   D1 — NO RULE AGAINST INVENTED PRECISION. A delivered explanation asserted a major
#   product forms "in about 70 percent yield" — a figure the stem never supplied, the
#   syllabus never fixes, and no step derived. Nothing in this spec forbade it. The
#   earlier audit passed this on §9's `overgeneralised_rule`, which is a DISTRACTOR
#   error type describing how a wrong OPTION fails — it says nothing about what the
#   explanation itself may assert. NEW §8-0a: every number traces to the stem, a
#   syllabus constant, or a shown derivation; nothing else may be written.
#   D2 — NO RULE AGAINST ABSOLUTE LANGUAGE. The same explanation said a bulky base
#   "cannot approach" the hindered hydrogens. It demonstrably can; it is disfavoured,
#   and the question turns entirely on the competition between two ACCESSIBLE
#   pathways — so the absolute destroyed the reasoning being taught. Zero rules
#   existed. NEW §8-0b: absolutes are reserved for claims absolute in the subject's
#   own terms; tendencies take calibrated language.
#   D3 — THE ARTEFACT DID NOT DECLARE ITS OWN STATE. Coverage was announced only in
#   the chat progress line (§S19-3), so the FILE said nothing. A legitimate mid-run
#   Batch-1 artefact carrying 10 of 60 explanations is byte-indistinguishable from a
#   finished paper once it leaves the conversation — and in the reference incident it
#   was reviewed as finished, the review's central complaint being the 50 questions
#   the batch had not yet reached. NEW §12-4 + engine v2.4 set_coverage_banner().
#   ENGINE SUPPORT WAS REQUIRED FOR D3, AND THAT WAS VERIFIED BEFORE THE RULE WAS
#   WRITTEN: with a banner present, verify_fidelity still PASSES (it sits outside
#   every question region) but strip_solutions leaves it, so the questions-only copy
#   diverges from the Step-7 source and the §12-3 re-audit FAILS. Engine v2.4 strips
#   it; five self-tests lock presence, gate-neutrality, stripping, idempotence and
#   removal (83/83).
# v1.30.0 — 2026-08-19 — GAP-2026-08-19-STALE-PIN-SWEEP (paired with PYQExplain v2.8).
#   SPEC-ONLY, no engine change. A CLASS SWEEP, not four incidents: v1.29.0 de-pinned
#   the §R1 report line and stopped, leaving the SAME defect standing in every other
#   place a count was written into prose. GAP-2026-08-13-STALE-SELFTEST-PIN fixed the
#   P1 gate in v1.25.0 and left the class standing too — this is the third time this
#   shape has been fixed instance-by-instance, so it is fixed by RULE here (§21-0).
#   D1 — §21 DEFINITION OF DONE HARD-PINNED THE ENGINE COUNT. Item 1 read "engine
#   --self-test 62/62" under a heading that says "ANY violation = do NOT deliver". The
#   engine prints 78/78. On a literal reading the Definition of Done could NEVER be
#   satisfied — the exact failure mode of GAP-2026-08-13-STALE-SELFTEST-PIN, in the one
#   place that fix never reached. Converted to floor form.
#   D2 — THE P2 DASHBOARD TEMPLATE PRESCRIBED PRINTING "[62/62 PASS]". A template is
#   an instruction: it told every session to print a count that has been wrong since the
#   engine grew past 62 fixtures. Now prints what the engine actually reported.
#   D3 — THE P2 DASHBOARD HEADER SAID "MockExplain v1.20" at spec v1.29.0. Now reads
#   the version from this file's own header.
#   D4 — STALE FACTUAL COUNT. P1's explanatory note asserted "it prints 64/64 today";
#   it prints 78/78. Any such assertion is stale the moment a fixture is added, so the
#   count is removed rather than corrected.
#   NEW §21-0 states the rule the three previous fixes each implied but never wrote
#   down, so the next fixture addition cannot reopen this.
# v1.29.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-FIGURAL-DOMAIN-BLINDNESS. SPEC-ONLY:
#   no engine change, no artefact-shape change. Four defects found by auditing what
#   v1.27.0/v1.28.0 did NOT touch. The router fixed what an explanation EMITS; these
#   fix how a question is READ and how the run REPORTS itself.
#   D1 — §13 SPOKE ONLY REASONING-PUZZLE. S13-1/S13-4 named "mirror/water image, paper
#   folding, cube net, space orientation" and defined the figural AXIOM as "the visual
#   rule (rotation / reflection / element add-remove / count / net-folding)". That is the
#   SSC/CAT non-verbal vocabulary. It is CORRECT for those exams and USELESS for a drawn
#   molecular structure, an MO diagram or a titration curve: a session reading §13 for a
#   chemistry stem was told to look for rotation and folding. §13 is now split into a
#   SHARED gate (detect/extract/view — unchanged, it was always domain-neutral) and TWO
#   named FAMILIES, transformation-puzzle and scientific-diagram, with the reading
#   protocol each actually needs. No exam loses anything: the puzzle family is the old
#   text preserved verbatim in substance.
#   D2 — §6 HAD NO CLASS FOR STRUCTURAL OR DERIVATIONAL REASONING. S6-1 classed by
#   exam shape (vocab / grammar / formal-logic / figural) so a Claisen rearrangement
#   landed in C-FIGURAL and a multi-step derivation in C-COMPUTATIONAL. Class decides
#   which SECTION LEADS — a different job from §6A, which decides what is EMITTED — so
#   the gap was not covered by the router. C-STRUCTURAL and C-DERIVATIONAL added.
#   D3 — §6A-3 PROMISED A REPORT LINE §20 DID NOT DEFINE. §6A-3 states "The §20 report
#   states the distribution" while §R3 listed no such field: a dangling cross-reference
#   that would be satisfied by nobody. §R3 now carries the representation distribution
#   and the degrade ledger.
#   D4 — §R1 PROVENANCE WAS STALE. It printed "spec v1.13 · engine 62/62" against a
#   spec at v1.28.0 and an engine at 78/78. NOT a halt risk — the GATES were converted
#   to FLOOR form in v1.25.0 (GAP-2026-08-13-STALE-SELFTEST-PIN) and remain floor-form
#   here — but a provenance line that misreports its own versions defeats the purpose of
#   provenance. §R1 now reads both values from what actually ran, pinning neither.
# v1.28.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-REPRESENTATION-EMISSION (figures LIVE).
#   MINOR bump, paired with explain_engine v2.3. v1.27.0 shipped the §6A router
#   RECORD-ONLY, deliberately: verdicts first, emission after review. This release
#   turns emission ON. What lands:
#   1. ExplanationBlock gains `figures` (list[RepresentationFigure]); each figure
#      carries the §6A-5 validation record and FAILS AT CONSTRUCTION on any breach
#      (no record, match False, inconsistent identifiers, missing file, width
#      outside 0.5..7.0 in). A figure is proved, not trusted.
#   2. Render path: figures interleave with DEDUCTION sentences at their
#      after_step position as CENTRED, TEXT-FREE picture paragraphs. The no-text
#      invariant is load-bearing: the strict reader keeps an explanation
#      paragraph only when it has display text or math source, so figure
#      paragraphs are INVISIBLE to parse_solution_blocks and the round-trip is
#      unchanged by design (self-test FIG-READER-INVISIBLE). There is NO caption
#      paragraph — the surrounding DEDUCTION prose describes the figure (§6A-1
#      already requires the prose to be readable without it).
#   3. verify_explanations gains the FIGURE-LANDING check: a block that declares
#      N figures must render EXACTLY N drawing paragraphs in its explanation
#      region. A silent skip (e.g. a legacy caller without doc_part) is a
#      BLOCKING FAIL — §6A-4's degrade-LOUDLY rule applied to the render path
#      itself (self-test FIG-SILENT-SKIP-CAUGHT).
#   4. verify_fidelity needs NO change and gets none: question-region signatures
#      exclude the explanation region, source-media MD5s are one-directional, and
#      new image parts register real rIds so the dangling-rId check (A3) passes.
#      Locked by FIG-E2E-GATES on a figural sample paper (stem images present),
#      proving stem drawings and explanation drawings are never conflated.
#   5. §6A-6 (NEW) defines the renderer execution contract: renderers are
#      declared per-exam in section_rules CATEGORY C, executed by the session at
#      solve time, and every artefact ships with its validation record. No new
#      engine file, no routes.json change: rendering is session-executed spec
#      work (the Step-7 figural precedent), and t3_mathcomp.py stays untouched.
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
# v1.24.0 — 2026-08-13 — CROSS-STEP SYNC AUDIT FIXES (Steps 5→11 handshake audit)
#   Two desyncs found by a dedicated 3-pass producer↔consumer audit of the whole
#   Step 5 → TestDeliver chain, both fixed in this file:
#   1. GAP-2026-08-13-STALE-CREATE-COMPLETE-NAME — S2-1's trigger contract (FRESH
#      prerequisite line + the HALT rule) still demanded a "Create_Complete" docx,
#      a filename RETIRED at v1.21.0 that no step produces (this file's own header
#      says so; Step 7 delivers [ExamCode]_[paper_slug]_Create.docx). Read literally,
#      the HALT rule could never be satisfied — a session would refuse the valid
#      _Create.docx upload forever. Both sites (and the S19-1 comment) now name
#      _Create.docx. The operative P1 discovery always did.
#   2. GAP-2026-08-13-EXPLAIN-N-SLUG-GATE — new P10/0: trigger-N ↔ uploaded-docx
#      identity gate, the SAME assertion Step 11 (MockDeliver S1-2) already makes
#      and Step 9 did NOT. P1 selects the BLUEPRINT by the uploaded docx's slug, but
#      N comes from the trigger — and on a RESUMED SCOPED SERIES the blueprint's
#      `mock` field is an ORDINAL (1..count) while the paper_id carries the OFFSET
#      series number (ScopedBlueprint S2-4 paper_start), so a mistyped P[N] could
#      silently bind a DIFFERENT paper's options_by_q/question_index to the uploaded
#      paper and publish a mislabeled Explanation. P10/0 hard-stops on
#      pp.paper_slug(trigger-N's paper_id) != the uploaded filename's slug.
# v1.23 — 2026-08-10 — P10 REGISTRY-FK TRIPWIRE (GAP-2026-08-10-QINDEX-FK-
#   ENFORCEMENT). New mandatory preflight P10: before ANY solving, validate this
#   mock's registry.question_index against the blueprint (entry exists; count/
#   coverage; every subtopic_id byte-exact in subtopic_list; every difficulty in
#   difficulty_labels) AND check the registry's ledger↔index agreement. WHY HERE:
#   three reference Step-7 sessions committed invented subtopic_ids that only
#   detonated at Step 11's JOIN — after the full Explain effort had been spent —
#   and one paper's question_index was silently LOST by a later registry write
#   while the completion ledger still claimed it done. P10 catches both classes
#   BEFORE Explain effort is spent: a defective index for THIS mock is a HARD
#   STOP with per-Q findings (remedy: fix at Step 7 / patch the registry
#   upstream, never inside Step 9); ledger gaps for OTHER papers are a loud WARN
#   (they do not block this mock, but must be surfaced the first time any step
#   sees them, not at those papers' deliveries). Companion to MockTestCreate
#   v5.48.0 (S13-4 copy-by-reference + A-QINDEX) and MockDeliver v1.12.0.
# v1.22 — 2026-08-10 — SHARED-ENGINE MATH-INTEGRITY GATE (GAP-2026-08-10-EXPLAIN-
#   MATH-DEGRADE-SILENT, mirrored from Framework_PYQExplain v2.4). The shared
#   explain_engine.py now compiles every ⟦MATH:…⟧ region inside ExplanationBlock.
#   validate() and RAISES at construction on a Tier-3 grammar reject, so a region
#   can no longer degrade to raw plain text at render. Because verify_explanations
#   REPORTS such degrades through its RETURN value (ok, problems) — it does NOT
#   raise — §18-1's verify_explanations line is now an explicit BLOCKING CONTRACT
#   (assert ok is True AND problems == [] AND T3_STATS['failed'] empty). This
#   pipeline authors math with the explicit helpers and bans LaTeX in prose (§11),
#   so ⟦MATH:…⟧ regions are rare here, but the shared-engine gate and the §18
#   contract apply. Engine self-test unchanged (62/62). Touched: §S5-2, §S18-1,
#   header + END sentinel. Ships with the regenerated MANIFEST (engine sha changed).
# v1.21.1 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED and explain_audit_gate.py
#   REMOVED from the framework. Updated the two notes that said the gate module still
#   survives / is still routed "for PYQExplainAudit" (no longer true). No rule change.
# v1.21.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   Step 9 now reads the Step-7 paper directly ([ExamCode]_Mock[N]_Create.docx) — the
#   rectified _Create_Complete.docx no longer exists because no step produces it. Every
#   claim of upstream certification, every escalation target, and every "Step 10 proves
#   truth" clause is restated against what actually survives: Step 7's own gates upstream,
#   and this step's §12 fidelity verification + §19 pre-delivery checklist downstream.
#   ACCEPTED LOSS, stated once and not hidden: no independent re-derivation of any answer
#   and no independent completion gate exist after this step. Step 9's self-checks are now
#   TERMINAL for explanation correctness. The §24 learnings loop loses its producer and is
#   demoted to an optional, manually-authored input.
#
# v1.20.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   401 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestExplain'. The current companion block, the
#   v1.20 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v1.20 — 2026-07-20 — FINAL QA FIX: EXAM_CODE CROSS-VALIDATION (twin of Framework_
#   MockTestCreate v5.29, found during the same full line-by-line adversarial re-audit).
#   P1's [ExamCode]*_blueprint.json glob is a PREFIX match — added an explicit
#   bp['exam_code'] == [ExamCode] check immediately after pp.pick_blueprint returns,
#   HALTING on mismatch instead of silently trusting the glob.
#
```

## Framework_NotesAudit.md

Entries v3.5.0–v3.8.0 moved at framework release 2026.11.06 (EC-P42; v3.9.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_NotesAudit.md.

```
# v3.8.0 — 2026-09-23 — GAP-2026-09-23-FLAT-MATH-NOTATION (owner decisions O-1..O-12 of
#   the 2026-09-23 review; notes_core v2.13, notes_docx v1.8, notes_audit v2.10,
#   Framework_NotesCreate v2.10.0 §6 F-3(b)–(e)). THE DEFECT: §5 G-2c gated a literal
#   token list from one domain (8 enzyme-kinetics words, pKa, 16 Unicode characters) so
#   2^9, a^m, x**2, H_2O, \frac, 1e-3, ⁿ, ₄, ¾ ALL passed — AND, since notes_core v2.5
#   (2026-08-13) joined runs without a separator, a CORRECTLY styled V+sub max, K+sub m,
#   pK+sub a FAILED. G-2b saw only the substring "^(" in raw oMath XML. Nothing enforced
#   F-3(b) at construction, so NA was the first and only line, and it was blind in both
#   directions. THE FIX: G-2c is notes_core.scan_flat_math_tokens(docx, exemptions) —
#   RUN-AWARE (w:vertAlign on the run's own w:rPr decides script vs plain), evaluating
#   notes_core.FLAT_MATH_RULES through the SAME notes_core.flat_math_findings that
#   notes_docx.validate_model runs at construction: one authority, two layers. G-2b
#   reads oMath m:t TEXT and flags every "^", "**", "_" and the complete Unicode
#   inventory. G-3 never counts an F-3 finding (they carry the "block i.j" prefix G-3
#   used to classify as anatomy). terminal_regate forwards exemptions to G-2c and G-3
#   and reports G-2c meta.advisories (uppercase juxtaposed forms, CO2 + H2O — advisory,
#   never a failure). A G-2c remediation recipe per rule id is added. Every finding
#   names its rule id ("[caret]", "[script_hyphen]" …) and its remedy; script-run
#   findings are reported ONE PER OFFENDING RUN with context, so N defects are N
#   locatable findings. Text + gate + engine change.
# v3.7.1 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2; DeliveryFooter v1.35
#   rule R6 / section 9). Delivery site gains the PHASE 1 print of its closed set (S10-1/§3 set unchanged), PHASE 2 echo of the RETURNED paths and PHASE 3 result-built footer. Text only; no set, gate or engine change; never a halt.
# v3.7.0 — 2026-09-01 — G-14 RECALL CONTRACT (GAP-2026-09-01-RECALL-CONTRACT; owner
#   decisions of the 2026-09-01 design session; notes_audit v2.9, notes_core v2.12,
#   notes_docx v1.7, Framework_NotesCreate v2.9.0 §4 B7a). THE DEFECT: the Recall Check
#   was the only section in the document with no content contract — G-5 gated its
#   FORMAT and G-10 its counter, and this spec then FROZE whatever count NC chose (§2A
#   "FORBIDDEN — changing the NUMBER"). THE FIX: §5 G-14 (notes_audit.gate_recall_contract)
#   gates the shipped Recall set against the SAME bank-derived target NC authored to
#   (notes_core.recall_target_for — the G-12/G-13 idiom, one authority, no drift) plus
#   the author's per-item declarations read from the registry unit record
#   (recall_contract, NC §9A) — the document cannot carry them (§7 / W-4), so the
#   registry is their only home, exactly as it is draft_ref's. HARD: coverage (one core
#   Recall per concept), attested types, the figure-reading item, EARLIER-only
#   cumulative items at the engine's count, the near-miss item, the concept-combining
#   item where the exam or the unit's breadth demands it (R-12), interleaved order,
#   no clone of a worked Example, and DIFFICULTY ON THE EXAM'S OWN SCALE (owner O-4): each
#   band == notes_core.recall_expected_band (the ONE resolver over the disclosed evidence
#   ladder) AND == the shared rubric's band for the recorded derivation
#   (notes_core.recall_verify_difficulty — the same check Step 7's G-DIFF and A-QINDEX 8
#   run), and the set's mix within the exam's measured paper-level mix when the
#   difficulty profile is present. ADVISORY: Trap-Box provenance, rubric fall-throughs,
#   basis distribution. DORMANT (reported): a registry unit with no recall_contract
#   record — a draft built before NC v2.9.0 — the G-13 grandfathering idiom; a
#   pre-upgrade unit re-run here yields identical gates otherwise. §2A: a G-14 hard
#   finding joins G-12/G-13 as a licence for a net ADD of Recall items; one-for-one
#   replacement remains the default. The rendered Recall box is unchanged (owner O-2/O-3).
# v3.6.0 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3; notes_audit v2.8,
#   notes_core v2.11, Framework_NotesCreate v2.8.0 §6 F-4a). §1's v3.0.0 re-render clause
#   named figural_core, which is NOT routed to NA — the clause was non-executable. It now
#   names the F-4a recipe (notes_core), and states the one rule that protects §8's
#   idempotence: COLOUR NON-CONFORMANCE IS NEVER A RE-RENDER TRIGGER. G-7a carries a
#   figure-palette ADVISORY in meta (notes_audit.figure_palette_meta) — information for the
#   next draft, never a finding, never ok=False. Additive; an AUDITED_PASS unit re-run after
#   v3.6.0 still yields zero corrections and identical bytes.
# v3.5.0 — 2026-08-15 — G-12 FORMAT CONTRACT (figure vs text balance; owner
#   decisions of the 2026-08-15 design session, approved proposal; pairs
#   with Framework_NotesCreate v2.7.0 §4 B3a; notes_core >= v2.10,
#   notes_audit >= v2.7). §5 G-12 extended — deliberately NO new gate id
#   (format coverage IS coverage; the same reasoning that folded the
#   distractor-autopsy rules into G-5, keeping notes_audit.GATES and this
#   spec in one-to-one agreement). HARD: figure evidence in the unit's
#   slice (format_mix, notes_core v2.10) -> at least one concept section
#   pairs a rendered figure with a worked Example, detected purely from
#   block order — no new model field, no builder change, W-3 and §0B P-4
#   untouched; the B8 mind map never satisfies it. ADVISORY:
#   figure_concept_tags (where the evidence sits, for §2A placement
#   judgement) and figure_example_pairs. Lead-format emphasis (FMT-2) is
#   §2A authoring judgement, never a block. Quarantined and
#   UNRESOLVED-image figure questions still count (v3.3.1 discipline).
#   Remediation: the standing §2A net-ADD licence on a G-12 hard finding —
#   NA adds the figure and the Example that reads it. Rollout follows the
#   G-12 precedent: applies at each unit's next audit; a target without
#   format_mix skips the check (additive, never retroactive).
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesAudit.md.

```
# v3.4.2 — 2026-08-14 — ADVERSARIAL-REVIEW FIXES (independent fresh-eyes
#   review + 400-trial property fuzz of the integration feature; pairs with
#   notes_core v2.9, notes_audit v2.6, Framework_NotesCreate v2.6.2,
#   Framework_NotesBlueprint v3.1.1). Five fixes on this side:
#     (1) §5 G-11 still said "ALL of the unit's bank questions" — the exact
#         pre-v3.4.1 boundary v3.4.1 replaced; the terminal re-solve runs
#         over the §2 CERTIFICATION SET (the same count-drift class as the
#         MockTestAnalyse PART-B miss, caught one release later this time).
#     (2) FILING MOVES ONLY ON FULLY-RESOLVED EVIDENCE (notes_core v2.9): a
#         fused question moves off its header only when EVERY fusion-set
#         member is a registry unit in the order map. An out-of-syllabus
#         header's question can no longer leak INTO a certifiable unit's
#         set, and a typo'd partner no longer under-files — the question
#         stays at its header and the defect is REPORTED.
#     (3) §5 G-13: UNRESOLVED evidence is ADVISORY (never a Combines demand
#         naming an unresolvable subtopic); the Combines match now uses
#         notes_core.display_norm — the subtopic_key component norm — so
#         & / and / dash / NFKC drift between paper-header bytes and
#         manifest names cannot produce a false blocking finding; the
#         containment-residual ("Waves" inside "Matter Waves") is STATED,
#         with the §2 inbound solve as the semantic net.
#     (4) §2: DEFERRED disclosure gains the ORPHANED-FILING check — when the
#         manifest is present, a deferred question whose filing unit's sid
#         has left the manifest is disclosed as certification-pending, never
#         silently dropped from the exam's coverage.
#     (5) §9 chat line: unresolved-evidence and orphaned-filing disclosures.
# v3.4.1 — 2026-08-14 — THE AUDIT BOUNDARY FOLLOWS FILING (line-by-line
#   certification sweep of the v3.4.0 feature; pairs with notes_core v2.8,
#   Framework_NotesCreate v2.6.1). Found by tracing ONE fused question
#   through NB -> NC -> NA: v3.4.0 filed the fused question's TEACHING at
#   the latest partner (G-13) but §2's closed-book solve still read the
#   HEADER slice — so the EARLIER unit was asked to solve a question whose
#   ingredients its own notes must not teach (backward-only, NC I-4): a
#   guaranteed PARTIAL/NOT with no licensed remedy, looping toward a
#   quarantine the question does not deserve. Meanwhile the FILING unit —
#   whose integration section exists exactly to make that question solvable
#   — never solved it closed-book at all: the certification instrument
#   missed the very questions the feature exists for. §2 now audits the
#   unit's CERTIFICATION SET, notes_core.audit_questions_for: the header
#   slice MINUS fused questions DEFERRED to a later partner PLUS fused
#   questions INBOUND from earlier slices — the filing decision is the SAME
#   shared authority G-13's target uses, so where a fusion is taught and
#   where it is solved can never disagree. IDENTICAL to the old slice for
#   grandfathered banks: no change for any existing exam. Second fix, same
#   sweep: unit_order was prose-only and built independently by NC and NA —
#   the author/gate drift class. notes_core.unit_order_from_registry is now
#   the ONE builder (ordinals = the persisted unit_code digits, NB §1A
#   A-3); NC I-5 and §2 here both call it, neither hand-builds a map.
#   coverage_target_for DELIBERATELY still reads the header slice (the
#   v3.3.1 discipline: the contract reads the BANK's evidence; only the
#   solve boundary follows filing). Deferred and inbound questions are
#   DISCLOSED in the §9 chat line.
# v3.4.0 — 2026-08-14 — G-13 INTEGRATION (in-subtopic Integration sections;
#   owner decisions of the 2026-08-14 design session; pairs with
#   Framework_NotesCreate v2.6.0 §4 B4a, Framework_NotesBlueprint v3.1.0 §3B
#   B-1; notes_core >= v2.7, notes_audit >= v2.5). New gate G-13
#   (notes_audit.gate_integration) against the unit's bank-derived
#   INTEGRATION CONTRACT (notes_core.integration_target_for — latest-partner
#   filing over the persisted teaching order, so the fusion is always taught
#   where the student has met every ingredient). HARD when the bank attests
#   a fusion for THIS unit: an integration section (a concept block whose
#   FIRST bullet is the Combines declaration — the same
#   derived-from-content discipline as every number in the document; no new
#   model field, W-3 and §0B P-4 untouched) must name every partner, sit
#   after every core concept, and carry >= 1 worked Example. DORMANT, never
#   blocking: no target (bank-less caller) and the GRANDFATHERED case — a
#   bank with no integration_partners anywhere predates notes-pyq-bank/1.2
#   and could not attest a fusion; both are reported, and the grandfathered
#   dormancy is a legitimate live-NA outcome (unlike G-12's). ADVISORY:
#   unattested integration sections (SME bridge-justified, D-6). REMEDIATION
#   ROUTING (§2A/§4): a G-13 finding is a PARTNER-HOMING gap — NA EXTENDS or
#   ADDS the integration section (net-ADD licensed exactly like G-12's);
#   it NEVER quarantines the fused question, because quarantine says "this
#   stem is corrupt or mis-filed", not "the notes lack the partner bridge".
#   G-11 runs G-13 with every other gate over the bytes that ship.
# v3.3.1 — 2026-08-14 — QUARANTINE x COVERAGE EDGE STATED (line-by-line
#   certification sweep). §5 G-12 now states explicitly what the engine
#   already does: a QUARANTINED question (§4 L-4) still counts toward the
#   coverage contract. coverage_target_for reads the BANK slice, and
#   quarantine lives in the report, never in the bank — so quarantining a
#   unit's only numeric item does not waive the numeric-Example requirement.
#   That is deliberate: quarantine says "this one stem is corrupt or
#   mis-filed", not "the syllabus stopped testing this type" — NA teaches the
#   type from a FRESH scenario (§2A licenses the add on the G-12 finding).
#   Prose only; no engine, gate or behaviour change.
# v3.3.0 — 2026-08-13 — G-12 COVERAGE (Phase 2, Recommendations 3+4; pairs with
#   Framework_NotesCreate v2.5.0 §4 B3a; notes_core >= v2.6, notes_audit >=
#   v2.4). New BLOCKING gate G-12 (notes_audit.gate_coverage) against the
#   unit's bank-derived coverage contract (notes_core.coverage_target_for):
#   every question type the unit's OWN bank attests has >= 1 worked Example,
#   and Examples span the required number of DISTINCT concept sections. The
#   contract is deliberately CONCEPT SPREAD, never an example COUNT (owner
#   decision, 2026-08-13): a count is satisfiable by clones of one scenario,
#   which add pages and teach nothing new. An Example's concept is DERIVED
#   from block order (nearest preceding concept block) — no new model field,
#   no rendering change, W-3 untouched. Two ADVISORY signals ride in the
#   gate's meta and never block: a bank-attested figure need with no concept
#   figure in the model, and duplicate_suspects (a concept section carrying
#   more than one Example of one type). Scenario diversity within a concept
#   is §2A judgement, not regex: an Example teaching a scenario an existing
#   Example already covers adds no coverage — NA REPLACES it with an
#   uncovered scenario, never keeps both. Without a target G-12 reports
#   DORMANT (the G-7a discipline). The spread clamp is
#   notes_core.COVERAGE_CONCEPT_CEILING — the engine constant is the single
#   authority; this spec deliberately restates no number.
# v3.2.0 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE ENFORCEMENT
#   (Point 1; pairs with Framework_NotesCreate v2.4.0 §4 B3, notes_docx v1.3,
#   notes_audit v2.3). G-5 (question format) now re-asserts, on the SHIPPED
#   model, the two new B3 elements: every Example carries a one-line Educational
#   Objective and one distractor-autopsy line per WRONG option (MCQ 3; MSQ
#   4 − #correct; NAT >= 1 trap value), and a Recall carries NEITHER. This is
#   deliberately folded into the EXISTING gate G-5 rather than a new identifier,
#   so notes_audit.GATES and this spec stay in one-to-one agreement (the S-2
#   sync check). notes_docx.validate_model gates the same contract at
#   construction, so the two layers agree exactly as they do for D-1. The new
#   text is document-facing and is scanned by G-4 like the rest of the file
#   (Framework_NotesCreate §7). §2A's editable model now includes the why_wrong
#   and objective fields — bounded improvement may sharpen a rationale or the
#   Objective, but may not delete either (validate_model + G-5 would fail).
# v3.1.0 — 2026-08-13 — LOSSLESS PARSE + TEXT AUTHORITY + ANCHORED G-9
#   (GAP-2026-08-12-NAPARSE; owner decisions OD-1 and OD-2 of 2026-08-13).
#   Four defects, all root-caused to test fixtures built from the simplest
#   shape rather than the production shape; every one had a green self-test.
#     (1) §2A's cycle now passes exam_code and tier into notes_docx.parse —
#         F-6 bans them from the document, so the registry unit record is the
#         only place they can come from (D-1b: without this, strict build
#         raised for EVERY unit of EVERY exam). New write property W-4.
#     (2) §0B gains P-4 PARSE FIDELITY: validate_model over the parsed draft
#         HARD-STOPS before any solving if the parser lost anything the
#         builder wrote (the permanent guard for the whole lossy-parse class;
#         D-1 lost every pure-OMML option and re-typed MCQ items NAT).
#     (3) §5 G-10 names notes_core.document_text as the ONLY text extractor —
#         a bare tag strip welded "Answer: 1" to "2.10 MIND MAP" and failed
#         correct documents on the standard tail anatomy (D-2).
#     (4) §5 G-9 scans PROSE, never model JSON (D-3), scope pinned to
#         stem/options/explanation with SPEED HACK excluded (OD-1), and runs
#         DOMAIN-ANCHORED (OD-2 Design A): only syllabus-evidenced orphans
#         report, so a clean unit yields ZERO findings and the gate is
#         readable again.
#   Companions rise to notes_core >= v2.5, notes_docx >= v1.2,
#   notes_audit >= v2.2.
# v3.0.0 — 2026-08-12 — NA BECOMES A WRITER (BREAKING; GAP-2026-08-12-NADOCX
#   patch P2 of 2; owner decisions of the 2026-08-12 design session).
#   Through v2.0.6 NA was a read-only certifier: it produced verdicts and
#   routed every defect BACK to NC (§4 L-2), and §7 stated the audited file was
#   "the SAME file ND ships — delivery never edits content". NA now VERIFIES,
#   CORRECTS, IMPROVES and EMITS the student-facing document itself. The seven
#   changes that follow, and why each one is load-bearing:
#     (1) INPUT BY ATTACHMENT (§0A). The unit .docx arrives attached to the
#         trigger message, never from Project Files. The bank, blueprint and
#         registry stay in Project Files. Attachment removes the implicit
#         guarantee that the file audited is the file NC produced, so §0B adds
#         three HARD-STOP preflights — filename identity, exam-code
#         cross-check, and sha256 against the registry's draft_ref.
#     (2) REBUILD, NEVER PATCH XML (§2A). NA parses the draft to a
#         notes_docx content model, edits the MODEL, and rebuilds through the
#         SHARED builder. notes_docx.py exists because construction was prose
#         until 2026-08-12: a writing NA hand-rolling paragraphs would have
#         been a second implementation of the §6A colour map, the cascade, box
#         styling, spacers, F-7 and the OMML conventions — the exact "one
#         contract, two implementations" class the 2026-08-10 sweep closed.
#     (3) KEY CORRECTION (§3A), superseding v2.0.0 owner decision 4a for the
#         correction path. Where the notes-derived answer disagrees with the
#         stored key, NA teaches the CORRECT method and answer instead of
#         bending the notes to a wrong key. Two tiers: a bank that contradicts
#         ITSELF is corrected silently; a bank that is internally consistent
#         is still corrected but the correction is DISCLOSED in the chat.
#         Without the tier split every disagreement would resolve in NA's
#         favour and the ground-truth check would be decorative.
#     (4) FOURTH VERDICT SOLVABLE_KEY_CORRECTED, counting toward the pass, so
#         a corrected unit certifies without weakening the vacuous-pass floor.
#     (5) NO .md REPORT (§6). The evidence moves into notes_registry.json as
#         audit_summary. The report OBJECT stays: pass_for_unit operates on it
#         and IS the vacuous-pass floor, so dropping the object would delete
#         the certification rather than just the file.
#     (6) NEW GATES (§5): G-7a visual layout (DORMANT without a renderer),
#         G-7b OMML/figure line-rule geometry, G-8 answer integrity, G-9
#         orphan terms, G-10 counter integrity, and G-11 the TERMINAL RE-GATE
#         that certifies the BYTES THAT SHIP rather than the pre-patch draft.
#     (7) ALWAYS DELIVER (§4/§9). NA emits exactly one file, always named by
#         notes_core.notes_final_filename, in every outcome. A question that
#         survives the loop is QUARANTINED, not shipped as a warning: nothing
#         inside the document ever marks a defect (F-6/§7 unchanged).
#   Companions: notes_core >= v2.4, notes_docx >= v1.1, notes_audit >= v2.0.
# v2.0.6 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §7's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename".
# v2.0.5 — 2026-08-10 — TAXONOMY SYNC (registry keyed by the Step-5 sid).
# v2.0.4 — 2026-08-10 — CROSS-CHAT HANDOFF + STALE-REF FIX.
# v2.0.3 — 2026-08-10 — POST-DEPLOY REVIEW (bank join recomputed from stored
#   fields).
# v2.0.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 2 (vacuous-pass floor wired).
# v2.0.0 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES.
# v1.1.0 — 2026-08-08 — REFINEMENT GATES (G-4, G-5, G-6).
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_NotesBlueprint.md

Entries v3.1.1–v3.3.2 moved at framework release 2026.11.06 (EC-P42; v3.3.3 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_NotesBlueprint.md.

```
# v3.3.2 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2; DeliveryFooter v1.35
#   rule R6 / section 9). Delivery site gains the PHASE 1 print of its closed set (S10-1/§3 set unchanged), PHASE 2 echo of the RETURNED paths and PHASE 3 result-built footer. Text only; no set, gate or engine change; never a halt.
# v3.3.1 — 2026-09-05 — GAP-2026-09-05-SYLLABUS-FILENAME-TOLERANCE: S-1
#   note — the shared resolver accepts filename dates as YYYY-MM or YYYYMM
#   (project Files strips the hyphen) and normalizes to YYYY-MM; NB
#   inherits this and the new HS-ST12 date-collision stop automatically
#   (single implementation, no NB-side change).
# v3.3.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE A
#   (Declaration & Detection). Version renumbered from the GAP's planned
#   v3.2.0 to v3.3.0 per the rev 4.6 rebase: the GAP was written against
#   corpus 2026.08.31.2, and GAP-2026-09-01-RECALL-CONTRACT already shipped
#   v3.2.0 in 2026.09.01.1. §2 S-1 gains CURRENT-FILE RESOLUTION: when the
#   exam's exam_config.syllabus_transition block reports an ACTIVE transition,
#   the syllabus NB parses is ALWAYS the resolved CURRENT file
#   ([ExamCode]_Syllabus_<EF>.<ext> — census corpus_io.syllabus_file_census +
#   decision blueprint_core.resolve_syllabus_sources); SUPERSEDED files are
#   never parsed by NB. INACTIVE + >= 2 syllabus-named files => HS-ST2 (R3,
#   the R26 reactive discovery). NB joins the §3.7 drift guard (declaration
#   fields only, blueprint_core.transition_drift => HS-ST10) and the §3.10
#   staleness contract (blueprint_core.check_syllabus_staleness => HS-ST7;
#   legacy artefacts exempt). §1 scope note: DELETED topics of a superseded
#   syllabus version never enter notes — structurally, because the CURRENT
#   syllabus is the master filter (§1.1) and NB now provably parses CURRENT.
#   A keys-absent exam with <= 1 syllabus-named file is byte-identical to
#   v3.2.0 (§7 P1).
# v3.2.0 — 2026-09-01 — REGISTRY CARRY-OVER HAS AN ENGINE (GAP-2026-09-01-RECALL-CONTRACT;
#   notes_core v2.12). §7 promised "existing unit states preserved" on a re-run, but
#   O-3 writes the registry through notes_core.registry_init, which sets every unit
#   BLUEPRINTED with draft_ref / final_ref / audit_summary None — the promise had no
#   engine behind it, and the new per-unit recall_contract (Framework_NotesCreate
#   v2.9.0 §9A, the ONLY place NotesAudit G-14 can read NC's declarations) would have
#   been silently reset too. §7 now names notes_core.registry_carry_over(reg, prior_reg)
#   — the ONE carry-over list (notes_core.REGISTRY_CARRY_FIELDS: state, notes_version,
#   audit, artifacts, history, draft_ref, final_ref, audit_summary, recall_contract),
#   deep-copied onto matching sid keys; new sids stay BLUEPRINTED; orphans are
#   reported (§7), never re-created. Additive: a first-ever NB run has no prior
#   registry and behaves byte-identically.
# v3.1.1 — 2026-08-14 — TAG SWEEP + PARTNER RESOLUTION + ORPHANED-FILING
#   (independent fresh-eyes review + 400-trial property fuzz; pairs with
#   notes_core v2.9, Framework_NotesCreate v2.6.2, Framework_NotesAudit
#   v3.4.2). Three fixes: (1) v3.1.0 claimed tags "enter naturally at the
#   next §7 refresh" — false for UNCHANGED papers, which §7's no-op merge
#   never re-reads: one tagged new paper made the contract live bank-wide
#   while legacy fused questions could never gain tags. §7 gains the TAG
#   SWEEP: once the bank is live (or on operator request), an NB re-run
#   MAY review untagged questions of papers already in the bank and add
#   integration_partners in place — an additive edit to NB's OWN artifact,
#   every added tag listed in the chat summary, bank_ref re-emitted after
#   the write so every downstream staleness link stays correct. Until a
#   question is tagged it simply stays in its header unit's certification
#   set (the pre-feature boundary) — safe, but taught without its bridge;
#   the sweep is how the feature reaches old evidence. The ingest report
#   now counts tags ("integration tags: N questions / M papers") so a
#   half-tagged bank is visible, never silent. (2) §3B B-1: partners
#   SHOULD resolve to manifest subtopics; notes_core v2.9 files a fused
#   question AWAY from its header ONLY when every fusion-set member
#   resolves to a registry unit — a typo'd or excluded partner keeps the
#   question at its header and surfaces as a downstream unresolved
#   advisory whose FIX IS HERE (correct the tag on the next NB run).
#   (3) §7 ORPHANED report extended: fused questions whose FILING home is
#   an orphaned sid are listed by bank_id — a deferred question must never
#   silently lose its certification home (NA §2 discloses the same from
#   its side). Companions: notes_core >= v2.9.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesBlueprint.md.

```
# v3.1.0 — 2026-08-14 — INTEGRATION EVIDENCE IN THE BANK (owner decisions of
#   the 2026-08-14 design session; pairs with Framework_NotesCreate v2.6.0
#   §4 B4a and Framework_NotesAudit v3.4.0 §5 G-13; notes_core >= v2.7).
#   Real exams fuse 2-3 subtopics in one question; the bank now RECORDS that
#   evidence where it is seen — at ingest. §3B B-1 gains the OPTIONAL
#   integration_partners field (schema notes-pyq-bank/1.2, additive; 1.0/1.1
#   banks still load): the OTHER subtopics a question genuinely fuses, each
#   in the canonical Subject::Topic::Sub Topic Name scope form (the same
#   form the resolve convention teaches everywhere). Claude-as-SME tags it
#   while reading the question — the header subtopic stays AUTHORITATIVE
#   and untouched (§1.3; NB still never reclassifies); a partner is evidence
#   ABOUT the question, not a re-filing OF it. bank_add_question validates:
#   scope form only, own subtopic never a partner. WHERE the fusion is
#   taught is not NB's decision: notes_core.integration_target_for files
#   every fused question at the LATEST member of its fusion set in the
#   persisted teaching order (backward-only by construction — NC §4 B4a
#   authors to it, NA G-13 gates it). GRANDFATHERING: a bank with no
#   integration_partners anywhere (written before 1.2) makes the contract
#   DORMANT downstream — no re-ingest is forced; the next §7 bank refresh
#   or new-paper append is the natural moment tags enter. No other field,
#   count, role, tier or output changes.
# v3.0.3 — 2026-08-12 — REGISTRY 2.1 SYNC (GAP-2026-08-12-NADOCX patch P3 of 3).
#   NB creates the registry, and notes_core v2.4's registry_init now EMITS
#   notes-registry/2.1 — additively: the 2.0 keys are untouched, 1.x/2.0 still
#   load, and 2.1 adds the per-unit draft_ref (written by NC section 9A),
#   final_ref and audit_summary (written by NA section 6). This spec still
#   cited 2.0 in its companion block and in O-3, so the step that CREATES the
#   artifact named an older schema than the engine it calls — the drift the
#   SPEC-LOCK block exists to catch, one release after the flip. Corrected
#   here, together with the PIPELINE POSITION line, which described NA as
#   "audit + loop" and no longer matched Framework_NotesAudit v3.0.0, where NA
#   also corrects, rebuilds and emits the unit's _Final.docx. Companion:
#   notes_core >= v2.4. No behaviour change: notes_blueprint.py is untouched
#   and notes-blueprint/2.0 is unchanged.
# v3.0.2 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts; pairs
#   with Framework_NotesCreate v2.2.1 and notes_core v2.1 SPEC-LOCK). §1A A-3
#   now names notes_core.unit_code as the FORMATTER of the numeric code (the
#   {EXAM}_S{s}_T{t}_ST{nn} pattern shown anywhere in this spec is the human
#   rendering; the engine is the single authority, spec-lock-pinned). §5's tier
#   bands and the §4 vocabularies are likewise spec-lock-pinned in notes_core.
# v3.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW RESOLVE (three notes from the v3.0.0
#   deployment verification).
#   (1) "133/133 unverifiable from the repo": the manifest is a PROJECT artifact,
#       so that validation is now a standing, REPRODUCIBLE preflight instead of a
#       changelog claim: notes_blueprint.verify_manifest — CLI
#       `python3 notes_blueprint.py --verify-manifest <path> [exam_code]` —
#       loads the manifest (exam_code gate), asserts unique unit_codes + gapless
#       ST numbering, sweeps ALL THREE resolution tiers across every subtopic,
#       and checks filename uniqueness. §1A A-1 now runs it as the session
#       preflight. Re-run against the live IIT_JAM_BIOTECHNOLOGY manifest at
#       resolve time: 133 subtopics, 133/133 sid + scope + bare-name, VERDICT
#       PASS — and anyone with the project file can re-verify with one command.
#       Companion: notes_blueprint >= v2.1 (additive; v2.0 surface unchanged).
#   (2) "breaking for mid-pipeline projects": intentional, now stated as the
#       explicit MIGRATION block after §7 — one NB re-run per project, bank
#       untouched (A-0 resumes; nothing re-downloads), and the previously
#       UNSPECIFIED state carry-over across the key change (1.x unit_code keys ->
#       sid keys) is specified: each 1.x unit's name resolves to its sid via
#       notes_core.resolve_unit; states/notes_version/artifacts carry over;
#       ambiguous/none resolutions are listed for the owner, never guessed.
#   (3) "NB hard-stops without the Step-5 manifest": intentional and now stated
#       plainly in the PREREQUISITE — Step 5 (PYQExtract) must have run for the
#       exam BEFORE Notes; that ordering IS the single-vocabulary architecture.
#       An exam that ran Notes before Step 5 completes Step 5 first, then takes
#       the MIGRATION path.
# v3.0.0 — 2026-08-10 — TAXONOMY CONSUMER (breaking; owner decision: ONE subtopic
#   vocabulary across Test Creation and Notes Creation). The Step-5
#   [ExamCode]_subtopic_manifest.json (the same file MockBlueprint consumes, whose
#   human view is [ExamCode]_taxonomy.xlsx) is now the SINGLE SOURCE OF TRUTH for
#   Notes unit identity. Step 5 itself is UNTOUCHED — Notes only consumes.
#     (1) NEW §1A applies the Mock pipeline's Cross-Step Subtopic Contract
#         (Framework_Blueprint RULES 1/2/2a) to Notes verbatim: every unit carries
#         its manifest sid VERBATIM; resolution failure is a HARD STOP whose fix is
#         upstream (re-run Step 5); NB NEVER mints, sequences, or fallback-creates
#         an id — on ANY path, including evidence-added.
#     (2) Unit names, section and topic are the manifest's EXACT BYTES; the
#         syllabus's role shrinks to what §1.1 always said — the MASTER FILTER
#         (in/out of scope, roles, tiers) — never a naming authority. §2 S-1
#         rewritten; the summary gains a SYLLABUS-MATCH report.
#     (3) The registry and blueprint are KEYED BY sid (schemas notes-registry/2.0
#         — 2.1 as of notes_core v2.4, additive — and notes-blueprint/2.0). The numeric unit_code {EXAM}_S{s}_T{t}_ST{nn}
#         survives as a DERIVED PRESENTATION attribute (B1 title number, F-1
#         filename): numbers come from manifest row order via
#         notes_core.assign_numbering and, once assigned, are PERSISTED — a Step-5
#         re-run that inserts/reorders subtopics never renumbers an existing unit;
#         new sids append with next numbers. The F-1 slug is notes_core.sid_slug
#         (the sid's final component), so a delivered filename is visibly
#         traceable to its taxonomy.xlsx row.
#     (4) taxonomy_ref {path, sha256, subtopics, generated} over the manifest
#         bytes is emitted beside bank_ref (notes_core.taxonomy_ref_for) and
#         stored in blueprint + registry; verify_taxonomy_ref is the staleness
#         link (NC §1.2 checks it; a changed manifest flips units STALE, §7).
#     (5) Engine: notes_blueprint.build_blueprint_v2 (manifest-consuming) replaces
#         build_blueprint in this spec's flow (the v1 builder remains in the
#         engine for legacy reads only). Companions: notes_core >= v2.0,
#         notes_blueprint >= v2.0. Engineering-session validation against the
#         live IIT_JAM_BIOTECHNOLOGY manifest (a project artifact, not in this
#         repo) is reproducible via the v3.0.1 --verify-manifest preflight.
#     (6) NEW §7 rules: manifest-hash staleness, ORPHANED (a delivered unit whose
#         sid left the manifest is reported, never deleted), and the BANK-MATCH
#         report (bank triples that fail to norm-match any manifest triple —
#         expected empty; nonzero exposes an upstream sorting anomaly).
# v2.0.5 — 2026-08-10 — DELIVERY-FOOTER CONTRACT HONORED. v2.0.4 added
#   present_files at every BATCH STOP but rendered no footer — a violation of
#   Framework_DeliveryFooter §4-0 R1 ("a present_files call is always followed by
#   the footer"), and the Notes pipeline had no §3 registry entry. A-7 now renders
#   F1 (batch bar) after each non-final batch and F2 (4-cell NOTES bar, Next: NC)
#   after the final delivery, per Framework_DeliveryFooter v1.18 (which now carries
#   the NB/NC/NA/ND §3 entries, the NOTES bar, and the Notes §6 chain).
# v2.0.4 — 2026-08-10 — POST-DEPLOY REVIEW. (B) O-2 no longer claims a "bank"
#   provenance value the engine never writes — unit provenance is
#   "syllabus"/"evidence-added"; only the pyq_count is bank-DERIVED, now stated as
#   such. (D) the bank checkpoint is written to /mnt/user-data/outputs AND
#   presented (present_files) at every BATCH STOP, and A-7 option B now tells the
#   operator to DOWNLOAD that presented bank and re-upload it to project knowledge
#   before a fresh-chat resume (the previous "already in project Files" was false —
#   write_bank targets the working dir). A-0 makes the resume load explicit.
#   Companion: notes_core >= v1.8 (stored subtopic_key is informational; reads
#   recompute — a bank written by an older notes_core still joins correctly).
# v2.0.3 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   notes_core.subtopic_key now reuses syllabus_provenance.norm per component so
#   bank counts join blueprint units across syllabus-vs-header label drift
#   (& vs and, dash/unicode/slash-spacing). Prevents a real subtopic silently
#   getting pyq_count=0 and the wrong tier. Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route. §1.3 updated.
# v2.0.2 — 2026-08-10 — BATCH STOP law added to §3A (owner-selected cadence).
#   The eager ingest now processes papers 3 at a time and PAUSES for user
#   confirmation after each batch (A-7), mirroring PYQExtract /
#   Framework_MockTestAnalyse: BATCH_SIZE = 3 is non-negotiable, and the response
#   ENDS after each batch so the run never auto-advances in one turn. The A-6 bank
#   checkpoint makes the pause resume-safe (reply 'continue', or re-trigger NB in
#   a fresh chat — it resumes from the paper_keys already in the bank). Spec-only
#   change; no engine surface moved.
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIXES. (1) bank_ref is now actually
#   EMITTED: NB builds the blueprint with bank_ref=notes_blueprint.bank_ref_for(
#   bank_path) after writing the bank, so §6 O-2's staleness link is real and NC
#   §1.2 can detect a blueprint/bank mismatch (notes_core.verify_bank_ref).
#   (3) §3A-1 enumeration is reworded to the CLASS T bridge: Claude runs the
#   paginated + recursive Google Drive:search_files walk IN ITS OWN TURN and
#   passes collect_corpus_files a PLAIN-LOOKUP resolver over the materialised
#   listing — never the tool marker (the defect audit_callgraph C6 exists to
#   catch). §3A-3 download uses the same resolver idiom explicitly.
# v2.0.0 — 2026-08-10 — INGEST BASE (breaking role change). NB is now the base
#   of the Notes architecture: it performs the EAGER full-corpus ingest of every
#   sorted-PYQ paper and emits a verified notes_pyq_bank.json (questions +
#   options + verbatim correct_answers + verbatim explanations + a stem/solution
#   figure split) that NC and NA consume READ-ONLY. Neither NC nor NA re-reads
#   Drive again. Consequences of the six owner decisions locked 2026-08-10:
#     (1) Drive images are read via corpus_io (the proven PYQExtract path):
#         enumerate -> screen -> batch-of-3 download -> image extract -> vision
#         read. No FIGURE_PENDING stem-only fallback for the normal run.
#     (2/3) exam_date comes from the (stable) filename via
#         notes_core.parse_exam_date_from_filename; nothing in the body carries it.
#     (4) answers + explanations are read from the doc VERBATIM and never
#         re-derived; NA runs permanently in ground-truth mode; KEY_FLAG dropped.
#     (5) subtopic-wise pyq_count + recent-3-year counts are DERIVED from the
#         bank (notes_core.derive_taxonomy_counts); the separate PYQ Analysis doc
#         is no longer a prerequisite (optional cross-check only, §2 S-3).
#     (6) image reads succeed (files < 10 MB); NB does NOT hard-stop on a per-
#         image gate finding — it reports it. Only a corrupt ZIP or a truncated
#         download (size mismatch) stops the affected paper, which then routes to
#         the upload lane.
# v1.1.0 — 2026-08-08 — REFINEMENT SUPPORT: allowed_question_types, explicit unit
#   ordering (seq_in_topic), per-unit prose_ban_exemptions; registry schema 1.1.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Design locked + validated on the IIT JAM
#   BT Enzyme Kinetics proof-of-concept (37/37 PYQ solvability). SourceMap folded in.
```

## Framework_NotesCreate.md

Entries v2.7.2–v2.10.0 moved at framework release 2026.11.06 (EC-P42; v2.11.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_NotesCreate.md.

```
# v2.10.0 — 2026-09-23 — GAP-2026-09-23-FLAT-MATH-NOTATION (owner decisions O-1..O-12 of
#   the 2026-09-23 review; notes_core v2.13, notes_docx v1.8, notes_audit v2.10,
#   Framework_NotesAudit v3.8.0 §5 G-2b/G-2c/G-3). THE DEFECT: §6 F-3(b) defined "flat
#   math token" only by a biochemistry EXAMPLE LIST, the engine implemented that list
#   literally, and the gate meant to stop flat notation (G-2c) could neither see a
#   caret (2^9, a^m, a^(m−n) shipped with every gate green in the SSC_CGL_TIER2 Number
#   Systems draft) nor tolerate a correctly styled symbol (V+sub max FAILED since
#   notes_core v2.5, 2026-08-13). Nothing enforced F-3(b) at construction, the golden
#   fixtures themselves violated it, and an ASCII hyphen inside a superscript run
#   rendered as an invisible dash ("a-2" for a⁻²). THE FIX: F-3(b) is now a NORMATIVE
#   definition backed by ONE machine authority, notes_core.FLAT_MATH_RULES, evaluated
#   RUN-AWARE by notes_core.flat_math_findings at CONSTRUCTION (notes_docx.validate_model,
#   §4A) and at AUDIT (NA G-2c) — a styled token is never a finding, a flat token always
#   is. New F-3(c) names the only accepted authoring forms, F-3(d) the per-unit
#   exemption path (G-2c:<rule_id> labels in prose_ban_exemptions, declared by NB),
#   F-3(e) that headings and figure/mind-map labels are notation-free (they are plain
#   strings and can never carry a script run, so notation there is unfixable at audit).
#   Rules: caret, double_star, underscore_script, latex_residue, e_notation,
#   unicode_script (complete inventory), script_hyphen, domain_token, unit_power
#   (cm2, m3, m/s2 — named by F-3(b) since v2.x, never implemented), juxtaposed_power
#   (x2 + y2 — lowercase, operator within 3 chars). notes_docx v1.8 also refuses every
#   unbraced sign/bracket script in a math run (a^-2, a^(m-n) mis-rendered silently).
#   Km/h is no longer mistaken for the Michaelis constant. Text + gate + engine change.
# v2.9.1 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2; DeliveryFooter v1.35
#   rule R6 / section 9). Delivery site gains the PHASE 1 print of its closed set (S10-1/§3 set unchanged), PHASE 2 echo of the RETURNED paths and PHASE 3 result-built footer. Text only; no set, gate or engine change; never a halt.
# v2.9.0 — 2026-09-01 — GAP-2026-09-01-RECALL-CONTRACT (owner decisions of the
#   2026-09-01 design session; notes_core v2.12, notes_docx v1.7, notes_audit v2.9,
#   Framework_NotesAudit v3.7.0 §5 G-14). THE DEFECT: §4 B7 fixed the Recall Check's
#   FORMAT and nothing anywhere defined its CONTENT — how many questions, which
#   concepts, what order, how hard, where the distractors come from. The count was
#   SME judgement here and then FROZEN by NA (§4 there, "FORBIDDEN — changing the
#   NUMBER"). The one section built for the student to self-test was the only
#   section with no contract — the declared-property-without-a-definition class of
#   GAP-2026-08-21-DIFFICULTY-STICKER-LABELS. THE FIX: §4 B7a, a bank-derived
#   contract in the coverage_target_for idiom (third instance after B3a and B4a):
#   notes_core.recall_target_for is the single authority NC authors to and G-14
#   gates, so author and gate cannot drift. SPREAD NOT COUNT (owner, 2026-08-13,
#   applied to Recall): one core Recall per concept section; every attested type;
#   a figure-reading item iff the slice attests figures; cumulative items ONLY
#   from EARLIER subtopics (unit_order — I-4 backward-only by construction); >= 1
#   near-miss discrimination item; >= 1 concept-COMBINING item where the exam or
#   the unit's breadth demands it (R-12); interleaved order; NO clone of a worked
#   Example; distractors from the Trap Box. DIFFICULTY ON THE EXAM'S OWN SCALE
#   (owner O-4): the SAME rubric Step 7 labels mock questions with and PYQExplain
#   profiles real PYQs with (blueprint_core, now routed here through notes_core
#   wrappers), the SAME [ExamCode]_difficulty_profile.json, the SAME
#   author-to-band / verify / re-verify discipline. A missing or partial profile
#   NEVER blocks a unit (owner O-5): the band stands on the nearest rung of a
#   disclosed evidence ladder. WHAT DID NOT CHANGE (owner O-2/O-3): the rendered
#   Recall box is byte-identical — Answer immediately after the options (the IFAS
#   portal hides it), no explanation, no key table, no attempt log, no confidence
#   tick (portal features). The contract lives in UNPRINTED model fields and in
#   the registry unit record (§9A recall_contract). ADDITIVE: every existing unit
#   keeps its Recall Check; G-14 is DORMANT on a registry unit with no record.
# v2.8.0 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3 of the figure-colour
#   programme; notes_core v2.11, notes_audit v2.8, Framework_NotesAudit v3.6.0). F-4
#   figures and the B8 mind map had NO render recipe — no palette, no dpi, no size — so
#   every notes figure was drawn from the model's judgement of the moment. §6 F-4a is the
#   recipe: the SAME constants Step 7 / Step 9 draw with, PINNED in notes_core.FIGURE_PALETTE
#   (a copy locked equal to figural_core by the SPEC-LOCK tripwire and a CI cross-check;
#   figural_core is NOT routed here and its mock gates never run on notes). What does NOT
#   transfer from the mock flow is stated in F-4a: notes TEACH, so colour-as-content is
#   ALLOWED, in-image labels stay REQUIRED (F-4), and no answer-leak rule applies. Additive:
#   every existing notes unit keeps its figures; only units drafted from v2.8.0 use F-4a.
# v2.7.2 — 2026-08-15 — THE SPACING RHYTHM (owner refinement of v2.7.1 in
#   the same release wave; notes_docx v1.5). v2.7.1 stopped tables from
#   touching; the owner's review of the rebuilt document showed the rhythm
#   still cramped — tables hugging the bullet text above them and section
#   bars starting with no visible break. The §4 tail rule is now the full
#   SPACING RHYTHM: one deterministic post-assembly pass sizes every
#   vertical gap by context (larger before L1/L2 bars, medium between
#   tables, small between text and a table, either direction); the engine
#   constants are the single authority. All per-case spacing emission is
#   gone from the builder's block loop, so the rhythm holds for every
#   block combination by construction. Model, parse(), W-3 byte-identity:
#   unchanged. Companion: notes_docx >= v1.5.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesCreate.md.

```
# v2.7.1 — 2026-08-15 — UNIVERSAL SPACING INVARIANT
#   (GAP-2026-08-15-ADJACENT-TABLES; field report from the first live NC
#   run: heading bars, data tables and boxes rendered FUSED, zero gap —
#   Word merges directly adjacent tables and nearly every element of these
#   notes is a table). The §4 spacer rule was the box-after-box special
#   case; notes_docx v1.4 now guarantees the GENERAL invariant — no two
#   tables are ever adjacent anywhere in the body, enforced by a
#   post-assembly pass so it holds for every block combination, current
#   and future, by construction. Model, anatomy, colours, numbering,
#   parse(): all unchanged; W-3 byte-identity preserved. Existing drafts
#   gain the spacing on their next rebuild (NA §0B P-4b reads the byte
#   difference as the documented builder-upgrade diagnostic, never a
#   stop). Companion: notes_docx >= v1.4.
# v2.7.0 — 2026-08-15 — THE FORMAT CONTRACT (figure vs text balance; owner
#   decisions of the 2026-08-15 design session, approved proposal; pairs
#   with Framework_NotesAudit v3.5.0 §5 G-12; notes_core >= v2.10,
#   notes_audit >= v2.7). Reading a figure (V–I curve, ray diagram,
#   potential well, phase diagram) is a SEPARATE skill from knowing the
#   theory — a subtopic with perfect prose and zero figure practice is a
#   gap wherever the exam asks figure-based questions. §4 B3a gains the
#   FORMAT CONTRACT, derived entirely from evidence every bank already
#   carries (the per-question figure flag + concept tags — no new field,
#   no re-ingest): FMT-1 both formats attested -> both taught, with >= 1
#   concept section PAIRING a rendered figure with an Example that reads
#   it (HARD, G-12-enforced); FMT-2 frequency shapes EMPHASIS — the lead
#   Example follows each concept's dominant format — never exclusion and
#   never count-mirroring (spread-not-count, applied to formats); FMT-3 no
#   evidence, no demand — a zero-figure slice never forces a figure. The
#   old unit-level requires_figure ADVISORY is superseded by FMT-1's hard
#   pairing where figure evidence exists (the advisory itself still rides
#   in G-12 meta). Anatomy, colours, density, builder: all UNCHANGED —
#   figures render through the existing F-4 rules. Rollout follows the
#   G-12 precedent: applies at each unit's next audit; no grandfathering
#   flag exists or is needed.
# v2.6.2 — 2026-08-14 — ADVERSARIAL-REVIEW FIXES (independent fresh-eyes
#   review + 400-trial property fuzz; pairs with notes_core v2.9,
#   notes_audit v2.6, Framework_NotesAudit v3.4.2, Framework_NotesBlueprint
#   v3.1.1). Six fixes: (1) new I-7 — a TIER-3 unit CAN be a fusion host:
#   the inbound fused questions ARE the evidence, so it ships its TIER-3
#   anatomy PLUS the demanded integration section(s), the only Examples in
#   such a unit; G-13 demands them, G-12 (header-slice contract) never
#   double-demands. (2) I-1 placement stated for units without B5 (before
#   B6; the mechanical check is unchanged). (3) I-6: EVIDENCE OUTRANKS the
#   1-2-partner style bound — an attested 3-partner fusion at a mid-topic
#   unit gets its section there; the bound shapes unattested SME sections
#   only (the old wording deadlocked against a G-13 demand). (4) I-2:
#   duplicate partner names are Topic-qualified (NB E-16). (5) PIPELINE
#   POSITION synced to NA v3.0.0 (was "audit + convergence loop" — the
#   same stale line NB v3.0.3 fixed on its side). (6) PREREQUISITE: the
#   "returned by NA for full regeneration" path died with NA §4 L-2
#   (regeneration is NA-internal); the real NA->NC return is the missing-
#   draft_ref preflight. Companions: notes_core >= v2.9.
# v2.6.1 — 2026-08-14 — ONE ORDER-MAP BUILDER (line-by-line certification
#   sweep of the v2.6.0 feature; pairs with notes_core v2.8 and
#   Framework_NotesAudit v3.4.1). v2.6.0's I-5 said "unit_order maps
#   subtopic_key -> the registry's persisted ordinal" in PROSE and left NC
#   and NA to each build the map — the author/gate drift class this
#   framework exists to kill (two builders, one contract). I-5 now names
#   notes_core.unit_order_from_registry as the ONE builder (ordinals = the
#   persisted unit_code digits, NB §1A A-3); NA §2 and G-13 call the same
#   function, so filing can never disagree between author and gate. Wording
#   only on this side; the engine change and the companion audit-boundary
#   fix (a fused question is SOLVED where it is TAUGHT) live in notes_core
#   v2.8 / Framework_NotesAudit v3.4.1.
# v2.6.0 — 2026-08-14 — IN-SUBTOPIC INTEGRATION SECTIONS (owner decisions of
#   the 2026-08-14 design session; approved on the DC/AC Circuits placement
#   demo; pairs with Framework_NotesBlueprint v3.1.0 §3B B-1,
#   Framework_NotesAudit v3.4.0 §5 G-13; notes_core >= v2.7, notes_audit >=
#   v2.5). Real exams fuse 2-3 subtopics in ONE question; the IFAS portal
#   links one page per subtopic (owner constraint), so the fusion is taught
#   IN-SUBTOPIC: new §4 B4a — an INTEGRATION SECTION closing the concept
#   stack, after every core concept's KEY POINTS and immediately before the
#   TRAP BOX. It is an ORDINARY concept section (same block type, own example
#   stack, own KEY POINTS; numbering, colours, gates all already apply — no
#   builder change of any kind) marked ONLY by its first bullet: the Combines
#   declaration. Rules I-1..I-6: placement (end of stack), the Combines
#   declaration + bridge bullets, backward-only partners (persisted teaching
#   order — students have met every ingredient), evidence-driven authoring
#   against notes_core.integration_target_for (latest-partner filing —
#   the SAME contract NA's G-13 gates, so author and gate can never
#   disagree), the last-subtopic capstone bound, and the no-earlier-partner
#   edge (no integration section). B8's mind map stays SUBTOPIC-ONLY —
#   merged concepts never enter it (owner decision). Anatomy is otherwise
#   UNCHANGED; TIER-3 unchanged; §7 bans apply to integration prose in full.
# v2.5.1 — 2026-08-14 — STALE ANATOMY REFERENCE (line-by-line certification
#   sweep). §2.1 called the fresh-numbered practice questions "§4 B4/B7" — a
#   leftover from a pre-v2.0.0 block layout. Under the CURRENT §4 anatomy B4
#   is the KEY POINTS box; the practice questions are B3 (Examples) and B7
#   (Recall Check). Reference corrected to "§4 B3/B7". Wording only; no
#   behaviour, gate or engine change.
# v2.5.0 — 2026-08-13 — COVERAGE CONTRACT AUTHORING (Phase 2, Recommendations
#   3+4; pairs with Framework_NotesAudit v3.3.0 §5 G-12; notes_core >= v2.6).
#   New §4 B3a: before drafting Examples, NC computes the unit's coverage
#   contract with notes_core.coverage_target_for over the unit's bank slice
#   and AUTHORS TO IT — at least one worked Example for every question type
#   the unit's own PYQs attest, and Examples spread across at least the
#   required number of DISTINCT concept sections. The contract is CONCEPT
#   SPREAD, deliberately NOT an example count (owner decision, 2026-08-13):
#   more Examples on one scenario add pages, not coverage — an additional
#   Example is justified only by an uncovered concept, scenario or type.
#   NotesAudit G-12 gates the SAME bank-derived contract on the shipped
#   file, so author and gate can never disagree. An empty bank slice means
#   no contract (TIER-3 "no examples where no evidence" unchanged). No model,
#   anatomy, colour or rendering change of any kind — B3a constrains WHERE
#   Examples go and WHICH types they teach, not how they are built.
# v2.4.0 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE (Point 1;
#   pairs with Framework_NotesAudit v3.2.0 and notes_docx v1.3). Every worked
#   Example (B3) now ends with TWO new elements, and a Recall (B7) carries
#   NEITHER:
#     (1) A per-option "why the other options fail" block — ONE line per WRONG
#         option, naming the specific error that produces it (MCQ: 3 lines;
#         MSQ: 4 − #correct; NAT: this becomes a "trap values" block of >= 1
#         line, each a wrong number and the mistake that yields it). The
#         builder stores these in the example block's why_wrong field.
#     (2) A one-line Educational Objective — the transferable takeaway — stored
#         in the objective field.
#   These are built THROUGH notes_docx.build like everything else (§4A):
#   notes_docx.validate_model enforces the exact per-option count and the
#   presence of the Objective at construction, and Framework_NotesAudit G-5
#   re-asserts both on the shipped file, so a missing rationale can never reach
#   a delivered document. The autopsy header renders in the TRAP red and the
#   Objective label in the L2 teal — both EXISTING §6A colours, so no new
#   colour is introduced. The new text is document-facing prose and is subject
#   to §7 in full (no question-type names, no years, no PYQ token). Anatomy,
#   density, math and numbering (§4A–§6A otherwise) are UNCHANGED.
# v2.3.1 — 2026-08-13 — OPTION CONTRACT MADE EXPLICIT (GAP-2026-08-12-NAPARSE
#   D-1). §4 B3 now states that the "N. " option marker is the ONLY
#   guaranteed plain text (w:t) on an option line: the option's CONTENT may
#   be entirely OMML, so any reader of a built document must never require
#   w:t content beyond the marker. Framework_NotesAudit §0B P-4 enforces it.
# v2.3.0 — 2026-08-12 — SHARED BUILDER + DRAFT PROVENANCE (GAP-2026-08-12-NADOCX
#   patch P2 of 2; pairs with Framework_NotesAudit v3.0.0).
#     (1) CONSTRUCTION IS NOW AN ENGINE. NC builds the .docx by calling
#         notes_docx.build(model, path) — never by hand-rolling paragraphs.
#         Until 2026-08-12 document construction lived only in this spec's
#         prose, so NC's run-time code was the sole implementation of the
#         section 6A colour map, the decimal cascade, box styling, spacer
#         paragraphs, rule F-7 and the OMML conventions. NA now writes
#         documents too (v3.0.0), and two implementations of one contract is
#         the defect class the 2026-08-10 sweep closed for filenames. New
#         section 4A states the content model and the derived-numbering rule.
#     (2) NUMBERS ARE NO LONGER WRITTEN BY NC. Every "n.k", "n.k.m",
#         "Example j" and "Recall j" is DERIVED from block order by
#         notes_docx.outline_of at render time. Section 6A's renumber rule is
#         satisfied structurally: there is no stored number that can go stale.
#     (3) DRAFT PROVENANCE (new section 9A). NC records
#         notes_core.docx_ref_for(draft) into the registry unit as draft_ref
#         (schema notes-registry/2.1). NA now receives its input as a CHAT
#         ATTACHMENT rather than from Project Files, so nothing else would
#         prove the file audited is the file NC produced. draft_ref is the
#         evidence for NA section 0B P-3.
#     (4) HANDOFF CHANGED (section 9). The draft is NO LONGER uploaded to
#         Project Files. Its footer badge is "Use locally" and the Next
#         callout instructs the operator to ATTACH it to the NA chat. The
#         registry is still uploaded, because NA reads it from Project Files.
#     (5) t3_mathcomp.py is now ROUTED to NC. F-3(a) has always required its
#         conventions, but the engine was never on NC's route — a real gap
#         found while wiring the shared builder.
#   Companions: notes_core >= v2.3, notes_docx >= v1.0. Anatomy, density,
#   format rules and content bans (sections 4-7) are otherwise UNCHANGED.
# v2.2.1 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). A
#   deployment review found F-1 restating the filename recipe in prose while
#   notes_core.notes_filename sanitises non-alphanumeric runs in {Slug} to "_"
#   — one contract, two implementations. F-1 now names the ENGINE as the single
#   authority, states the sanitisation, and requires NC to derive the draft
#   filename by CALLING notes_core.notes_filename — never by re-implementing
#   the pattern. The same sweep marked §5 and §6A as spec-lock-pinned (the
#   notes_core v2.1 SPEC-LOCK self-test pins every literal these sections
#   restate) and replaced §9's informal "[ExamCode]_<unit>.docx" with "the
#   unit's F-1 filename". Companion: notes_core >= v2.1. No behaviour change.
# v2.2.0 — 2026-08-10 — TAXONOMY-SYNCED OPERATOR INPUT (Framework_NotesBlueprint
#   v3.0.0). Units are identified by the Step-5 manifest sid (the registry key);
#   the OPERATOR identifies a unit by copying a cell from
#   [ExamCode]_taxonomy.xlsx — the SAME convention that workbook's "How to use"
#   sheet already teaches for Step 6. NEW §0: three-tier resolution via
#   notes_core.resolve_unit — (1) Sub Topic Id (column D), (2)
#   Subject::Topic::Sub Topic Name scope (columns A::B::C), (3) bare Sub Topic
#   Name (column C), norm-matched so case/dash/&/spacing variants resolve; a
#   multi-hit bare name STOPS and lists the candidates with their Topics for the
#   operator to choose; zero hits STOP with nearest-name suggestions — NEVER a
#   fuzzy auto-pick. §1.2 additionally verifies taxonomy_ref
#   (notes_core.verify_taxonomy_ref): a manifest changed since the blueprint was
#   built STOPS the unit back to NB, exactly like the stale-bank stop. F-1's
#   {Slug} is the sid's final component (notes_core.sid_slug), so every
#   delivered filename traces visibly to its taxonomy.xlsx row. Companion:
#   notes_core >= v2.0. B1's "n" and F-1's numbers come from the unit's
#   PERSISTED unit_code/seq_in_topic (NB §1A A-3) — they never churn on a
#   taxonomy re-run. All v2.1.x behaviour otherwise unchanged.
# v2.1.5 — 2026-08-10 — §8 wording aligned with §9/DeliveryFooter §3. Each
#   multi-unit request is separate PER-UNIT RUNS, each a complete step ending F2
#   (§9); the continue-confirmation is BETWEEN runs, not batches within one (NC
#   has no intra-run batching — that F1 pattern is NB's). §8 retitled RUNS AND
#   STATE and cross-references §9. Wording only; no behaviour change.
# v2.1.4 — 2026-08-10 — CROSS-CHAT HANDOFF SPECIFIED. NC runs in its own chat, so
#   its draft .docx must reach NA (a fresh chat) the same way NB's bank reaches NC.
#   New §9: NC present_files the draft + the updated registry and renders the F2
#   footer (4-cell NOTES bar "2 of 4"; Next → NA), so the handoff persists and the
#   next-step pointer actually prints. Pairs with Framework_DeliveryFooter v1.19.
# v2.1.3 — 2026-08-10 — POST-DEPLOY REVIEW. bank_questions_for now joins by
#   RECOMPUTING the subtopic key from stored fields (drift class closed), so an
#   older bank still reads correctly. Companion: notes_core >= v1.8.
# v2.1.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   bank_questions_for now joins via the hardened notes_core.subtopic_key
#   (syllabus_provenance.norm). Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route.
# v2.1.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 1 (bank staleness stop wired).
#   §1.2's "signals a stale bank" stop now has evidence: NC reads the blueprint's
#   bank_ref and calls notes_core.verify_bank_ref(bank_path, bank_ref) before
#   drafting; a sha256 mismatch (blueprint built from a different bank than the
#   one on disk) or a missing bank_ref STOPS the unit back to NB. Companion bump
#   to notes_core >= v1.6.
# v2.1.0 — 2026-08-10 — BANK CONSUMER (Framework_NotesBlueprint v2.0.0). NC no
#   longer reads Drive or builds its own PYQ bank. It LOADS the bank NB produced
#   (notes_pyq_bank.json), filters it to the unit's subtopic
#   (notes_core.bank_questions_for), and drafts from those records. The FIGURE
#   flag is the bank's stem_figures; the correct_answer and explanation are read
#   from the bank as SME grounding (never reproduced verbatim — §3 paraphrase
#   rule unchanged). §1 rewritten accordingly; all v2.0.0 anatomy/format/gates
#   (§4-§8) are unchanged.
# v2.0.0 — 2026-08-08 — REFINEMENT RELEASE (breaking anatomy change). Encodes the
#   12-item refinement set locked in the 2026-08-08 review session and approved
#   on the Enzyme Kinetics golden sample: title-only header; plain concept
#   headings; frequency tags removed from the document; "Example N" boxes with
#   the fixed stem/options/Answer/Explanation template; question types
#   constrained to the exam's own type set; hierarchical cascade numbering;
#   level-locked colour map; figure labels inside the image with no captions
#   and no exam vocabulary; no editorial lead-ins; no exam-type words, years,
#   or PYQ references anywhere in delivered text; EXAM LENS block removed;
#   RECALL CHECK re-defined as exam-format questions; structural-OMML +
#   styled-script math standard document-wide including diagrams.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_NotesDeliver.md

Entry v1.2.0 moved at framework release 2026.11.06 (EC-P42; v1.2.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_NotesDeliver.md.

```
# v1.2.0 — 2026-08-12 — CONSUMES NA's _Final (GAP-2026-08-12-NADOCX patch P2 of
#   2; pairs with Framework_NotesAudit v3.0.0).
#     (1) ND's input is now the unit's _Final.docx from NA
#         (notes_core.notes_final_filename), attached or filed per section 1.0,
#         and its output is notes_core.notes_deliver_filename —
#         {unit_code}_{Slug}_Deliver.docx. Three filename authorities now
#         exist (draft / _Final / _Deliver) and each is an ENGINE CALL; no step
#         spells a pattern.
#     (2) THE AUDIT REPORT IS GONE. NA no longer writes [ExamCode]_<unit>_
#         Audit.md; the evidence lives in notes_registry.json as the unit's
#         audit_summary (schema notes-registry/2.1). ND's delivery line reads
#         its verdict counts from there.
#     (3) PORTAL FORMATTING IS DEFERRED (owner decision, 2026-08-12). ND
#         currently ships the audited bytes UNCHANGED. When portal formatting
#         is specified it will make ND a SECOND WRITER downstream of the
#         certified bytes, so it will need its own terminal re-gate — and any
#         LibreOffice-based conversion will silently destroy every equation
#         (section 3). Recorded here so the requirement is not rediscovered
#         late.
#   Companions: notes_core >= v2.3.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesDeliver.md.

```
# v1.1.3 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §1.0's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename" —
#   Framework_NotesCreate F-1 (notes_core.notes_filename) is the single
#   authority for notes filenames (§1.1 already deferred to F-1). Pairs with
#   Framework_NotesCreate v2.2.1. Nothing else changed.
# v1.1.2 — 2026-08-10 — TAXONOMY SYNC (Framework_NotesBlueprint v3.0.0). The
#   registry key is the Step-5 manifest sid; an operator unit reference is
#   resolved per Framework_NotesCreate section 0 (notes_core.resolve_unit — same
#   taxonomy.xlsx convention). The §1.3 delivery line identifies the unit as
#   <Sub Topic Name> (<sid>) alongside unit_code/notes_version. Companion:
#   notes_core >= v2.0. Nothing else changed.
# v1.1.1 — 2026-08-10 — CROSS-CHAT READ + REGISTRY. Made the fresh-chat handoff
#   explicit: ND READS the audited .docx + _Audit.md + notes_registry.json from
#   Project Files (NA uploaded them), and re-presents the updated registry
#   (unit → DELIVERED) alongside the delivery so the state persists. Pairs with
#   Framework_NotesAudit v2.0.4 / Framework_DeliveryFooter v1.19.
# v1.1.0 — 2026-08-10 — POST-DEPLOY REVIEW. (1) ND is the delivery step but never
#   said to present_files its artifacts and rendered no footer — so on mobile the
#   delivered files were unreachable and the Framework_DeliveryFooter contract was
#   unmet. §1 now present_files the notes .docx + audit report and renders the F2
#   step-complete footer (4-cell NOTES bar "4 of 4"; Framework_DeliveryFooter
#   v1.18 §3 ND entry). (2) Removed stale references the NA v2.0.0 changes left
#   behind: KEY_FLAG is retired (NA owner decision 4a) and answer-mode "M-2" is
#   gone (NA runs permanent ground-truth mode). Companion: notes_core >= v1.0.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_PYQApprove.md

Entries v1.0–v1.3.0 moved at framework release 2026.11.06 (EC-P42; v1.3.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQApprove.md.

````
# v1.3.0 — 2026-09-14 — GAP-2026-09-14-SCAN-ORPHAN-AT-SOURCE (companion; the fix lives
#   in PYQScan v1.6.0). S4-0 passes manual_corrections= to build_approval_record
#   (reconcile_taxonomy v1.5): when the operator edited classifications.json or
#   scan_progress.json OUTSIDE the pipeline before this run (the SSC_CGL_TIER1 INV-5
#   orphan was hand-repaired and the resulting CLEAN record carried no trace), the
#   edits are declared and recorded verbatim in approval_record.json. INV-5
#   conservation_check is unchanged — it is now the BACKSTOP of the zero-orphan gate
#   PYQScan runs at source (verify_no_orphans, GATE 5), the same relationship C6 has
#   to PYQDraft's pre-delivery gate. A conservation HOLD on a v1.6.0 scan therefore
#   names a scan that bypassed its own gate, not a scan-time classification defect.
# v1.2.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: crosswalk approval + R30 + G-1
# v1.1.0 — 2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION. (A1) C6's spec
#   text cites reconcile_taxonomy.check_topic_density — BOTH forms (subject
#   density + the NEW per-topic cap, finding class TOPIC_OVER_AGGREGATION_TOPIC),
#   the syllabus-anchored denominator, the excluded/anchored scoping, the
#   per-topic finding detail — and gains the THREE-CASE reclassification rule
#   (pre-release generation / DECLARED_AMBER / stale current-generation input).
#   (A3) the S4-0 INPUTS list extends to qcount_anchored_topics, item excluded
#   states, amber_status (draft + scan _meta), telemetry and spec_generation,
#   all passed through; the invocation gains grandfather() (E4/S3) and
#   resolve_declared_amber() (E7) between reconcile and adjudicate. (A2) Branch
#   B prints the per-topic crowded list with counts and the re-derive-directive
#   sentence — the operator action stays exactly one step. Branch A gains the
#   DECLARED_AMBER lines. C6 is now the BACKSTOP of a check that PYQDraft's
#   pre-delivery gate already ran at source.
# v1.0.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 1 prose mention to no-paren form (write_analysis_doc).
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
````

## Framework_PYQCompress.md

Entries v1.1.1–v2.1 moved at framework release 2026.11.06 (EC-P42; v2.1.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQCompress.md.

```
# v2.1 — 2026-09-14 — GAP-2026-09-14-COMPRESS-NAME-IDENTITY (owner ruling 2026-09-14).
#   THE OUTPUT FILENAME IS THE INPUT FILENAME, BYTE-FOR-BYTE. The v2.0.0 canonical-name
#   rule (blueprint_core.canonical_output_name: ExamCode_DD-Mon-YYYY[_ShiftN].docx, Shift 1
#   suffix dropped, _IMAG junk stripped, hyphen removed from Shift-N) is RETIRED for this
#   step. Measured against the Step 1 contract (PYQPrepare §6, [ExamCode]_DD-Mon-YYYY
#   [_<session_keyword>-<N>].docx): the deriver RENAMED every Shift-1 Row file
#   (…_Shift-1.docx -> ….docx) and every Shift-N one (…_Shift-2 -> …_Shift2), so a
#   compressed paper re-entered Drive under a second identity — the exact double-count
#   §2 was written to prevent. Under the identity rule the output overwrites its input in
#   place, always. §2 rewritten; §4 compress_one writes to OUT_DIR/<input name>; CHECK 4
#   asserts basename(output) == input name; the batch collision gate keys on the input
#   name (EC-C14: two spellings of one paper now yield two outputs — de-duplication is
#   the enumeration gate's job, never this step's); §6/§11/§12 operator guidance is
#   replace-in-place. Engine: blueprint_core.canonical_output_name / NAME_JUNK_TOKENS
#   DELETED in the same release — this spec was their only caller, audit_callgraph C4
#   forbids a dead export, and they had no self-test fixture (661/661 unchanged). Paper
#   identity (blueprint_core.canonical_paper_key) is untouched. All compression,
#   parity, survival and no-growth logic unchanged.
# v2.0.1 — 2026-08-30 — GAP-2026-08-30-LINEART-CLASSIFIER (corpus_io v1.15; no rule of
#   this spec changes). EC-C6's line-art test was "<= 256 distinct colours" — measured
#   2026-08-30, EVERY anti-aliased rendered figure (structures 553-1,705 colours, charts
#   268-1,504) failed it and routed to JPEG unless it carried alpha, while a smooth
#   gradient (exactly 256 colours) passed as line art. corpus_io._is_line_art() is now
#   STRUCTURAL (corpus_io._is_line_art): line art when flat_fraction (pixels whose four
#   neighbours are exactly equal; renders 0.78-0.98, photographs and scans 0.00) >=
#   LINE_ART_FLAT_FRAC 0.60 OR mode_fraction (share of the single most common exact colour
#   — a render's background; renders 0.39-0.99, photographs / scans / gradients <= 0.005)
#   >= LINE_ART_MODE_FRAC 0.25. Either alone decides; the second catches a smoothly
#   interpolated heat map whose axis text would ring under JPEG. Deterministic, bounded,
#   NEAREST-resampled (explicit — Pillow's default filter changed across versions and a
#   smoothing filter blurs the flatness being measured), numpy-less fallback to the old
#   rule. EC-C5 (alpha wins) and EC-C7 (JPEG source wins) are unchanged.
# v2.0.0 — 2026-08-25 — GAP-2026-08-18-PYQCOMPRESS-UNDERCOMPRESSION. Two load-bearing
#   changes, measured on a 22-paper live corpus before adoption:
#   (1) MAX COMPRESSION. The governor no longer walks TIER_LADDER stopping at the
#       first tier that fits the budget — that design meant an under-budget file was
#       NEVER downscaled even with images embedded at 600–900 effective DPI in a 1–2
#       inch display box (every pre-2015 scanned paper). PYQCompress now calls
#       corpus_io.optimize_docx(mode='max'): ONE pass at blueprint_core.MAX_TIER
#       (q82 / 300 DPI at display size — above the q80/200 T4 floor) with PNG output
#       palette-quantized (pngquant → optipng when installed, PIL FASTOCTREE
#       fallback; alpha-capable on every path). Measured: 90%+ reduction on pre-2015
#       scans (19.8 MB → 1.1 MB), 40–60% on 2021+ papers already at display
#       resolution. Ladder callers (PYQSort S7-6) unchanged. corpus_io v1.13,
#       blueprint_core MAX_TIER / PNG_QUANT_*.
#   (2) CANONICAL OUTPUT NAME. §2's byte-identical-filename rule is REPLACED by
#       blueprint_core.canonical_output_name: ExamCode_DD-Mon-YYYY[_ShiftN].docx.
#       Shift 1 emits NO suffix; junk tokens (NAME_JUNK_TOKENS, e.g. _IMAG) are
#       stripped; document-class decorations after the date (…_Sorted_Q1-Q100)
#       survive verbatim. Unparseable name = HARD STOP, never a guess. The operator
#       instruction changes from replace-in-place to upload-canonical-AND-trash-the-
#       misnamed-original (§2, §6) — the two names are DIFFERENT identities.
# v1.1.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   9 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQCompress'. The current companion block, the
#   v1.1 entry, and all structural notes remain in-file. Body byte-untouched.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCompress.md.

```
#   v1.1 — 2026-07-25 — SIZE GATE REMOVED. Every attached file is now compressed
#          regardless of size (corpus_io v1.0.3 `always=True`); previously anything at or
#          under SIZE_BUDGET was reported T0 and skipped. The operator selects what to
#          compress by selecting what to attach. SIZE_BUDGET is unchanged and still
#          governs the LADDER TARGET and the MARGINAL/BLOCKED verdicts — it is no longer
#          an eligibility test. New EC-C1b covers the file that cannot be improved:
#          corpus_io restores the original bytes and it is reported but not delivered,
#          which stops CHECK 5 from hard-stopping the run on an already-optimal document.
```

## Framework_PYQCore.md

Entries v1.5.1–v1.8 moved at framework release 2026.11.06 (EC-P42; v1.9 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQCore.md.

````
# v1.8 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE A
#   (Declaration & Detection; rebased to 2026.09.01.1 per rev 4.6). S1-2
#   --taxonomy mode gains the SYLLABUS FILE CENSUS contract and NEW S1-2a
#   defines it for every PYQ step: candidate syllabus / sample-paper files
#   (corpus_io.syllabus_file_census / sample_paper_census), the T2 outcomes at
#   the shared-core level (INACTIVE + >= 2 syllabus-named files => HS-ST2, the
#   R26 reactive discovery; ACTIVE requires BOTH syllabus documents as project
#   FILES — a chat-only or pasted-image syllabus is HS-ST3, because a re-run
#   must be reproducible), the §3.7 per-step drift guard (census +
#   bc.resolve_transition re-run, DECLARATION fields compared only via
#   bc.transition_drift => HS-ST10) and the §3.10 staleness contract
#   (taxonomy_draft syllabus_sha256; consumers bc.check_syllabus_staleness =>
#   HS-ST7; legacy artefacts without the field exempt). Engine: blueprint_core
#   Cluster SYLLABUS ERA + corpus_io Cluster SYL are the ONLY implementations
#   — this core cites, never restates. A keys-absent exam holding <= 1
#   syllabus-named file is byte-identical to 2026.09.01.1 (§7 P1).
# v1.7 — 2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION. The GATE-AT-SOURCE
#   LAW is added (registered in LAW_REGISTRY.json) and S2-3 is brought under it:
#   (C1) the S2-3 "PROOF OF CORRECT TOPIC COUNT" self-check — stranded on the
#   pre-v1.1 absolute rule while the engine moved to density, the RULEBOOK DRIFT
#   that HELD RPSC_ZOOLOGY — now CITES reconcile_taxonomy.check_topic_density
#   (both forms; constants live ONLY in the engine); (C2) the GROUPING rule
#   gains the per-topic cap with the EC-P20 tie-break, and the Arithmetic worked
#   example is REVISED per DECISION D8 (an example contradicting a blocking rule
#   is the two-rulebook disease inside one file); (C3) Q-count-anchored topics
#   are recorded and OUT of the over-aggregation domain (archetype A2 conflict
#   dissolved); (C4) exclusions are RECORDED, never silently omitted (D3:
#   automatic, recorded); (C5-C7) the draft-time ratio / name-shape / catch-all
#   HARD STOPs on Claude's OWN output become bounded self-correction, the name
#   gate enforces min(80, bc.MAX_HEADING_LEN) at write time, and STEP 3 gains
#   the normative PRE-DELIVERY GATE (D3 order) with the FLAGGED-DELIVERY (AMBER)
#   exit; §12 Phase 0a DoD gains the matching checklist lines. Superseded texts
#   moved VERBATIM to SPEC_HISTORY.md (2026.08.15.14 discipline).
# v1.6 — 2026-08-23 — GAP-2026-08-23-SESSIONLESS-DEDUP-BLINDSPOT, companion
#   wording per the LAW-PROPAGATION LAW (rule lives in Framework_PYQCount v1.6).
#   S5-1's same-paper duplicate gate is re-keyed from (date, session) — whose
#   regex required a session token PYQSort's session-less and _to_ filename forms
#   never carry, leaving their re-sort duplicates silently double-counted — to
#   the filename STEM before `_Sorted_` (dated stems only). EC-P30 and the §12
#   Phase-B checklist now describe the stem key. No other rule changed.
# v1.5.2 — 2026-08-22 — GAP-2026-08-22-SCANROUTE-HEADROOM (editorial; no rule
#   changed). Superseded v1.5 entry moved VERBATIM to SPEC_HISTORY.md (the
#   2026.08.15.14 discipline) — PYQScan-route SPEC-BUDGET headroom, flagged
#   +809 B by the 2026.08.21.4 deploy review. Directory and standing notes stay.
# v1.5.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: admission call -> tagged fence; 8 prose mentions to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
````

Entry v1.5 moved at framework release 2026.08.22.2 (EC-P42 — PYQScan-route
headroom, flagged +809 B by the 2026.08.21.4 deploy review). Current-version
entry remains in Framework_PYQCore.md.

```
# v1.5 — 2026-08-16 — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION (SESSION-BUDGET LAW).
#   §9 gains four edge cases. The reference incident is IIT_JAM_MATHEMATICS PYQExtract:
#   two consecutive sessions, 54 tool calls, ZERO of 22 papers processed, because three
#   independent stalls each sufficient on their own were present at once.
#   EC-P40 (the probe is a SPENDER, not a free classifier — a CLASS T acquisition
#   performed BEFORE the partition must be subtracted from the budget, and is charged
#   even when it fails, because the bytes arrived either way). EC-P41 (a PARTIAL
#   listing is worse than an empty one — EC-P39 catches zero and nothing caught
#   21-of-22; the transcription from connector response to DRIVE_LISTING_CACHE is the
#   highest-risk step in the acquisition path and must be asserted against an
#   independently declared count, with a HARD STOP). EC-P42 (SPECIFICATION-READ COST is
#   a session resource — the framework priced payload characters and paper pacing but
#   never priced reading its own specification, which on Step 5 is 556,834 B / ~139,208
#   tok / >=36 view calls BEFORE any work). EC-P43 (the DIRECT EGRESS LANE — when the
#   container can reach Drive and the folder is link-shared, python fetches the bytes
#   itself and EC-P36's double charge disappears entirely; proven per exam on a real
#   paper, never assumed, never fatal on failure).
#   EC-P36/EC-P37 are unchanged and remain correct: they describe the connector lane,
#   which stays the fallback whenever the direct lane is unavailable.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCore.md.

```
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
```

## Framework_PYQCount.md

Entries v1.5–v1.7 moved at framework release 2026.11.06 (EC-P42; v1.7.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQCount.md.

````
# v1.7 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: per-era counts, n_new, HS-ST9
# v1.6 — 2026-08-23 — GAP-2026-08-23-SESSIONLESS-DEDUP-BLINDSPOT. S5-1's same-paper
#   duplicate gate keyed on (date, session) and its regex REQUIRED the session token,
#   while PYQSort's own filename contract legitimately emits SESSION-LESS names
#   ([ExamCode]_DD-Mon-YYYY_Sorted_Q1-QN.docx) whenever a paper carries no session
#   number, plus a _to_ multi-date form this gate explicitly skipped. For both, a
#   re-sorted duplicate pair (..._Sorted_Q1-Q100.docx beside ..._Sorted_Q1-Q99.docx —
#   this gate's own motivating example, written WITHOUT a session token) matched
#   NOTHING: canonical identity cannot collapse differing Q-ranges, Task 1 and S5-4
#   count both copies consistently so Task 2 balances, and the counts inflate
#   SILENTLY — the class EC-P30 names the most dangerous. Verified by execution on a
#   two-copy fixture: session-ful pair caught, session-less pair invisible. The key
#   is now the filename STEM before `_Sorted_` (dated stems only), covering
#   session-ful, session-less and _to_ forms with zero false positives; the undated
#   Multi_ last-resort form stays out of scope (two genuinely different undated
#   papers could share it) and is already visible as a year=None inventory row
#   (EC-P8). Companion wording updated in Framework_PYQCore.md EC-P30 + §12 per the
#   LAW-PROPAGATION LAW. No engine change; no other rule touched.
# v1.5.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 9 prose mentions to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.5 — 2026-08-16 — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, propagated per the
#   LAW-PROPAGATION LAW. Step 4 did not suffer the reference incident — it is
#   single-session, so its probe cost amortises to zero and its spec is far under the
#   SPEC-BUDGET threshold — but three of the four laws that incident produced govern any
#   step performing a CLASS T acquisition before a partition, and a law that is applied
#   in one file and not its sibling is how the PYQAnalyse->PYQCount split shipped an
#   unfixed defect "content byte-identical" in the first place.
#   (a) EC-P43 DIRECT EGRESS LANE added as A0, tried before the connector probe.
#   (b) EC-P40 the probe is a SPENDER: plan_transport passes consumed= explicitly.
#       Step 4 fetches the probe paper again in the same run, so the value is 0 and the
#       reason is stated at the call site rather than left as an absent argument that
#       audit_callgraph C10 cannot distinguish from an oversight.
#   (c) EC-P41 the listing is written and ASSERTED by corpus_io.write_drive_listing.
#   (d) P4f divergence DECLARED: 'SMALLEST by fileSize' is correct HERE and wrong in
#       Step 5. mock_sync_audit MS-13 requires both files to name the divergence.
````

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCount.md.

```
# v1.4 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (sibling fix, applied
#   here per the LAW-PROPAGATION LAW rather than waiting for Step 4 to fail). THE BRIDGE
#   showed a flat `list_fn` that ignores its folder_id argument. corpus_io.collect_corpus_files
#   RECURSES into sub-folders, so on a year-subfoldered Drive folder that resolver returns
#   the same entries for the sub-folder and the walk raises DuplicatePaperError — a HARD
#   STOP blaming the operator's Drive for a defect in this contract. The cache is now
#   keyed by folder id; a bare {'files': [...]} cache is still accepted, scoped to the
#   root. Found by reading the engine while fixing Step 5, not by a failing run: a flat
#   corpus never triggers it.
# v1.3 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (EXECUTION-BOUNDARY
#   LAW). S5-4 step 1 injected the bare name `gdrive_download_file` into
#   corpus_io.fetch_drive_docx. That name was defined NOWHERE — no spec, no engine, no
#   builtin — so executed literally it raised NameError, every paper fell through
#   TransportFallback to the upload lane, and the Drive lane was unreachable on EVERY
#   run of EVERY exam. Measured on IIT_JAM_MATHEMATICS (22 papers, all under
#   DRIVE_CAP): 0 of 22 acquired, Task 1 unconfirmable, 22 manual uploads demanded.
#   This is GAP-2026-07-26-003 applied to the PYQ counting path: the identical fix
#   shipped in MockTestAnalyse v2.37 on 2026-07-26 and was never propagated here, and
#   the 2026-07-31 split from PYQAnalyse v2.29 then copied the defect forward "content
#   byte-identical" into a file that never mentions the GAP id. §5 now opens with a
#   CLASS T transport declaration and THE BRIDGE, in a ```python fence so the CI can
#   read it; S5-4 step 1 injects a bound resolver. New S5-0 CHANNEL PROBE measures the
#   connector's delivery form on ONE paper before Task 1 — the "results always spill to
#   disk" invariant is MEASURED FALSE (one 40,488-byte .docx spilled in one deployment
#   and returned inline in another), so it is now probed, never assumed, and never
#   inferred from a directory listing. S5-8's "3 tool calls per session" is corrected
#   to 3 PHASES: it omitted the N connector calls that ARE the acquisition.
#   audit_callgraph gains C7 (text pass — an AST-only pass cannot see this call site,
#   which lives in an untagged, non-parseable fence) and C8.
# v1.2 — 2026-08-15 — GAP-2026-08-15-BAREQ (R-3). The S5-1 mandatory gate and
#   count_sorted_file() carried an inline r'^Q\.?\s*\d+' justified by an ASSUMPTION about
#   PYQSort's output ("always outputs Q.<N> format") where a DELEGATION belongs, and
#   nothing enforced the assumption. That dialect matched strings the engine's table did
#   not — a bare "Q.4" among them — so on IIT_JAM_MATHEMATICS 12-Feb-2017 this step
#   counted 60 for a file Step 5 extracted as 56, attributing four questions to whatever
#   subtopic happened to precede them. Both sites now call bc.detect_question_start();
#   audit_deep's new INLINE-QREGEX check fails the build if a private copy returns.
# v1.1 — 2026-08-05 — GAP-2026-08-05-001 (textless content is content). S5-2 now takes
#   the BLOCK-level lookahead bc.sorted_body_lookahead(doc) and the per-FILE colour probe
#   bc.heading_colour_available(paras); S5-4b CAUSE 1 split into 1a (gate absent) and 1b
#   (gate present but DEFEATED), because 1a's remedy asked the operator to verify two
#   already-true facts and re-run, which reproduced the halt forever.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
```

## Framework_PYQDeliver.md

Entries v1.12–v1.13.1 moved at framework release 2026.11.06 (EC-P42; v1.13.2 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQDeliver.md.

```
# v1.13.1 — 2026-08-27 — doc sync: S2-3b and EC-18 no longer name the retired
#   map_difficulty_level. Prose only.
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
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQDeliver.md.

```
# v1.11 — 2026-08-10 — DOC-CONSISTENCY: completes the v1.9 single-artifact sweep.
#   v1.9 retired the render-source and made the delivered file the ONE artifact, and
#   its changelog claimed it touched "§11 (done + invariants)" and the §7 "both
#   artifacts" prose — but three LIVE lines were missed and still asserted the retired
#   two-artifact model: the §7 C18 one-line summary ("on BOTH artifacts"), §11
#   Definition-of-done item 11 ("machine-verified by C18 on both artifacts"), and the
#   §11 hard invariant ("Both artifacts are schema-valid ..."). The gate_c18 code and
#   the §7 body prose already validate exactly ONE delivered artifact, so behaviour was
#   always correct; only these summary/invariant/done lines contradicted them, and no
#   check catches prose drift. FIX: all three now name "the delivered artifact"
#   (singular). No behaviour, gate, or delivered-byte change — documentation only.
#   Surfaced in the 2026.08.10.1 deployment review; not introduced by v1.10.
#   Touched: §7 C18 summary line, §11 done item 11, §11 hard invariant, END sentinel.
# v1.10 — 2026-08-10 — PYQ REGISTRY IS NO LONGER A PROJECT-FILES DELIVERABLE.
#   ROOT CAUSE of the reported cross-session gap: the registry
#   ([ExamCode]_pyq_registry.json) was the ONLY PYQ-4 artifact whose usefulness
#   depended on the operator MANUALLY uploading it back into the exam project's
#   Files section (old S8-3) — /home/claude and outputs are chat-scoped and
#   /mnt/project is read-only to the engine, so nothing else could persist it.
#   Across the ~200-exam corpus that manual step was skipped routinely, so the NEXT
#   paper's PYQ-4 ran in a fresh chat, found no registry, and — per the old §12
#   case 11 — reset the corpus tally and dropped the duplicate-delivery guard
#   SILENTLY. FIX: the registry is DEMOTED from a required Project-Files deliverable
#   to an OPTIONAL, LOCAL-ONLY, absence-tolerant continuity aid. It is (1) NEVER
#   badged Upload/Replace and NEVER presented as a file to manage in Project Files;
#   (2) READ ONLY IF the operator voluntarily attaches one — absence is the normal,
#   silent, expected state, never a WARN and never a nag; (3) CORRECTNESS-INDEPENDENT
#   — producing the tagged portal file and passing C1–C18 never depends on it, and
#   Definition-of-done no longer lists a registry update as a hard item; (4)
#   BEST-EFFORT — when a prior registry IS attached PYQ-4 still updates it, may emit a
#   LOCAL-ONLY copy, and the duplicate-delivery guard still fires; when none is
#   attached the §R6 line reports current-paper-only totals neutrally. CONSEQUENCE:
#   cross-chat corpus tracking becomes OPT-IN (attach the prior registry) instead of
#   mandatory-upload; the portal deliverable is unchanged. Mirrors Framework_
#   DeliveryFooter v1.16, which places *_pyq_registry.json in LOCAL_ONLY so the badge
#   engine can never route it to Project Files on any step, for any exam. Touched:
#   §0 outputs, §1 step 6, §3 step 3, §8 (open/S8-2/S8-3), §9 (items 2/6), §10 §R6,
#   §11 done item 9, §12 cases 4 & 11, §13 S13-2 table, END sentinel.
# v1.9 — 2026-08-09 — DELIVERED FILE NOW PRESERVES NATIVE OMML — the OMML→Unicode
#   linearization (Rule 19) is RETIRED from the delivery path. ROOT CAUSE of the
#   reported defect: §4-S4-2 named the RENDER-SOURCE artifact (every `<m:oMath>`
#   flattened to a one-line Unicode text run by S6-1/Rule 19) as the delivered
#   `_PYQ_Final.docx`. That silently DESTROYED all structured math — fractions,
#   radicals, integrals/sums, matrices, sub/superscripts — in the portal file
#   (measured on IIT JAM Physics 15-Feb-2026: 856 native `<m:oMath>` in the input,
#   0 in the delivered file). The two-artifact design was justified (S4-1 Fact 1)
#   by python-docx round-trip corruption — but PYQ-4 edits raw document.xml
#   (unzip→XML→zip, §3) and NEVER round-trips through python-docx, so OMML already
#   survives the pipeline byte-perfect: the INTEGRITY artifact proves it (gate C5:
#   integrity OMML count == source). FIX: the INTEGRITY artifact (native OMML, tag
#   blocks inserted, date/session tags removed, NO render transforms) is now THE
#   delivered file. Rule 19 linearization is retired; the render-source is no longer
#   built or delivered. The delivered file is therefore byte-identical to the input
#   except for the two pipeline-mandated edits (§4A date-tag removal + §5 tag-block
#   insertion). CONSEQUENCE: the render-only transforms Rule 21 (non-ASCII safe-font)
#   and Rule 22 (underline recolor) no longer apply to the delivered file — content
#   fidelity supersedes those portal-cosmetic transforms. Math preservation is now
#   gated: C5 (unchanged) guards the delivered OMML count == source, and C11 is
#   INVERTED from "zero OMML in render-source" to "delivered OMML count == source;
#   zero linearization." Mirrors MockDeliver v1.11.0, which fixes the identical
#   defect the same way. Touched: ZERO-MUTATION RULE, §0 outputs, §3, §4 (S4-1/S4-2),
#   §6 (retired), §7 (C11 inverted; C14/C15 repurposed; "both artifacts" prose),
#   §10 §R4/§R5, §11 (done + invariants), §12 case 7, §13 S13-1/S13-2, Appendix A.
# v1.8 — 2026-08-09 — QUESTION TYPE IS NOW POSITION-BASED (three-tier), closing the
#   section-determined-MSQ portal defect for real. SUPERSEDES the aborted v1.7 (never
#   deployed). v1.7 tried to fix this by CONSUMING a `qtype` map it claimed PYQExplain
#   had committed into pyq_explain_progress.json — but PYQExplain (§S7A-4) writes only
#   _meta / q_to_classification / options_by_q / q_to_difficulty; there was no qtype key
#   in the delivered sidecar, so v1.7's Tier 1 never fired and every question fell back to
#   the same structural rule that returned 0 MSQ where 10 were expected. The v1.7 root-cause
#   sentence ("PYQ-4 re-derived a type PYQExplain had already committed into the JSON") was
#   simply false. TRUE ROOT CAUSE: Question Type was being read from section_rules
#   `answer_cardinality`, a SUBTOPIC-scoped corpus statistic that cannot express
#   SECTION-determined MSQ — on IIT JAM Physics 15-Feb-2026 every Section-B subtopic reads
#   'single', so all 10 MSQ (Q31-40) mis-tagged as MCQ. FIX (mirrors the proven MockDeliver
#   v1.7 precedent): S2-2 is now a three-tier resolver whose Tier 1 resolves Question Type
#   POSITION-BASED from exam_config.marking_scheme[].question_type whenever marking_scheme
#   carries more than one distinct question_type — the exam's OFFICIAL, section-scoped
#   type-by-position, a field PYQ-4 already loads (§0 item 2). Tier 2 consumes PYQExplain's
#   now-genuinely-delivered qtype (v2.3+); Tier 3 is the pre-v1.7 structural rule for
#   single-type / subtopic-based exams. Deterministic; on IIT JAM Physics this yields
#   exactly 30 MCQ / 10 MSQ / 20 NAT. Touched: §0 item 2 (third use) + item 8, §1 step 5,
#   S2-1 row 4, S2-2 (rewritten), §10 §R1, S13-2 table. Paired with PYQExplain v2.3, which
#   fixes P4 the same way and delivers qtype as a fourth map.
# v1.6.2 — 2026-08-09 — PYQExplain v2.2.1 delivers the sidecar under the paper-identity stem
#   [ExamCode]_[date]_[session]_pyq_explain_progress.json. §1/§0 now derive the expected sidecar
#   name from the attached docx and load THAT — closing the same-Q_TOTAL collision where the
#   §2-5 coverage gate (1..Q_TOTAL) would pass a wrong-paper map. Legacy bare names → WARN.
# v1.6.1 — 2026-08-09 — PYQExplain v2.2 now DELIVERS pyq_explain_progress.json to outputs.
#   Clarified §1/§0 that the sidecar (q_to_classification + options_by_q + q_to_difficulty)
#   is attached alongside the _PYQ_Explanation.docx. No behaviour change — sourcing unchanged.
# v1.6 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. PYQ-4 now takes PYQ-1's
#   _PYQ_Explanation.docx as its STANDARD input (a legacy _Complete.docx is still
#   accepted, unchanged, but is no longer produced), and reads pyq_explain_progress.json
#   as the primary sidecar for q_to_classification / options_by_q / q_to_difficulty.
#   COMPLEXITY Tier 1 (q_to_difficulty) is now PRODUCER-ONLY: PYQ-2's independent
#   validation (§10A) is gone, so PYQ-4 consumes PYQ-1's assessed values directly after
#   the same membership check (S2-3a). No gate, transform, or delivered byte changes.
#   Edits retire the PYQ-2 input preference and cross-references. Touched: PIPELINE
#   POSITION, §0/§1 input + sidecar priority, S2-3a note, §4A, §5-3, §7 C18 note,
#   §10 §R7, §12 edge cases.
# v1.5.2 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   197 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQDeliver'. The current companion block, the
#   v1.5.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.5.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.2.1, several versions behind the header, so the last line of the file
#   contradicted the first. Documentation only — not one line of behaviour changes. It went
#   unnoticed because BOTH integrity tools were structurally blind to it:
#   validate_framework_md.py Check C recognised only the '# END OF <name> vN' sentinel form
#   and skipped the comparison entirely for the '**End of <name>.md (vN)**' form used here,
#   while audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
```

## Framework_PYQDraft.md

Entries v1.0–v1.3.1 moved at framework release 2026.11.06 (EC-P42; v1.3.2 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQDraft.md.

````
# v1.3.1 — 2026-09-05 — GAP-2026-09-05-SYLLABUS-FILENAME-TOLERANCE: §3.4
#   NAMING date stamp accepts YYYY-MM and YYYYMM (R-a — claude.ai project
#   Files strips '-' from uploaded filenames; verified 2026-09-05 with
#   byte-identical CSIR NET Life Science files under both names);
#   bc.parse_syllabus_filename now RETURNS the normalized YYYY-MM always.
#   NEW HS-ST12 (R-b, P-1): any two files sharing one normalized date stop
#   as a date collision — T2 row 7 (>=2 match EF => HS-ST5) retires into
#   it. HS-ST3/4/5 templates reworded to state both forms (R-d). Register
#   is now HS_ST1..HS_ST12. R-e: §3.7 drift identity for syllabus files is
#   the sha256 — current_file and superseded NAMES are display-only and
#   never drift-compared (superseded compare as a sorted sha256 set); a
#   platform rename of an unchanged file is never drift, changed bytes
#   still stop as HS-ST10. Legacy INACTIVE/single-file paths untouched.
# v1.3.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: S2-0b crosswalk DRAFT
# v1.2.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE A
#   (Declaration & Detection; rebased to corpus 2026.09.01.1 per rev 4.6). NEW
#   S2-0a SYLLABUS-TRANSITION RESOLUTION: two OPTIONAL Overview keys (Syllabus
#   Changed / New Syllabus Effective From) drive the R1 activation predicate
#   (engine: blueprint_core Cluster SYLLABUS ERA — resolve_transition,
#   coerce_effective_from with Excel date coercion per R4); file census +
#   CURRENT/SUPERSEDED resolution (corpus_io syllabus_file_census /
#   sample_paper_census + bc.resolve_syllabus_sources, Truth Table T2);
#   HS-ST1..HS-ST6 wired at 2a from the engine's §3.11 register; §3.6 traces
#   (one console line, the §3.5 exam_config block, one DeliveryFooter line —
#   T1 rows 4/5/7 only); §3.9 dial registry (bc.resolve_dials — factory values
#   engine-pinned, invalid override => factory + trace, never a stop); §3.5 A1
#   'Zero History Approved' key (bc.parse_zero_history_approved — R29 keeps
#   PYQDraft the sole exam_config writer); duplicate-key WARN + near-miss key
#   listing (bc.overview_duplicate_keys / bc.near_miss_keys). S2-4 taxonomy
#   draft gains syllabus_sha256 (§3.10 staleness lock — hash of the taxonomy's
#   source file: CURRENT in active mode; the single file otherwise; absent for
#   legacy chat-pasted input). S2-5 schema gains the OPTIONAL
#   syllabus_transition block (ABSENT for keys-absent exams — §7 P1
#   byte-identity; SOLE WRITER PYQDraft, immutable until re-run, R29). An exam
#   with both keys absent and <= 1 syllabus-named file is byte-identical to
#   2026.09.01.1 (P1); the crosswalk DRAFT (§4.2) ships with Release B.
# v1.1.0 — 2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION. (D1) NEW S2-0
#   INTAKE RULE: a HELD approval record's re_derive_directive is consumed as
#   HARD constraints (the memoryless-re-run loop hazard closed); a CLEAN /
#   CLEAN_ADJUDICATED record demands explicit operator confirmation before
#   re-deriving a LOCKED taxonomy (contract-protection, Type-2 class); a prior
#   AMBER draft's unresolved list constrains the re-run. (C9) DUPLICATE-SUBJECT
#   SEATBELT at S2-1 and save_taxonomy_draft — Type-2, one-touch message, never
#   merges (the dict-key overwrite silent-data-loss class). (D2) S2-1/S2-3e wire
#   dedup, exclusions and subject flags to syllabus_provenance E5; build_items
#   now returns (items, errors, dedup_report). (C8) S2-3f: budget raised to the
#   law's SELF_CORRECTION_MAX_ROUNDS, retries are constraint-carrying, and
#   exhaustion exits AMBER with a finding-keyed amber_status + auto-declared
#   OTHER deviations + data-preserving structural residue (validate_provenance
#   MUST still pass) — never the pre-v1.1.0 "re-run and report" dead end (moved
#   verbatim to SPEC_HISTORY.md). (D2/D3) S2-4 schema gains excluded items,
#   qcount_anchored_topics, subject_flags (skeletal/open_ended), dedup_report,
#   telemetry, amber_status and spec_generation; S2-6 prints the AMBER residue
#   when one exists.
# v1.0.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 2 prose mentions to no-paren form (syllabus_provenance).
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
````

## Framework_PYQExplain.md

Entries v2.15–v2.27 moved at framework releases 2026.11.06 and 2026.11.07 (EC-P42; v2.28 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQExplain.md.

```
# v2.27 — 2026-11-05 — GAP-2026-11-05-DIFFICULTY-FIDELITY (paired with blueprint_core
#   v1.32, audit_canonical v2.37, figure_types v1.3, figural_vision zoom_tiles,
#   MockTestAnalyse v2.60.0, Blueprint v1.64.0, ScopedBlueprint v1.14.0, MockTestCreate
#   v5.92, MockTestExplain v1.53.0). What a band MEANS is measured from this exam's own
#   past papers and bound to the question's content. §7A: every difficulty_obs carries
#   `rubric_rule` 'r2' and `inferential_steps` counted by the ONE rule
#   (bc.INFERENTIAL_STEP_RULE, quoted verbatim in S7A-2 and in Create CHECK 3c);
#   `deduction_steps` stays the paragraph count for explanation validation; the score is
#   bc.difficulty_score_from_obs(obs) — never a positional difficulty_score call; a
#   flagged derivation no longer changes the band (DL-16) and is resolved in-run
#   (§7-1 / RE-16 / §18-2: derived answer, web-verified tie-break; owner D4 — no human
#   hand-off; owner F2 — no official answer key is ever an input). S7A-6 passes
#   exam_config.marking_scheme so each profile record carries `marks` (DL-10).
#   §13A-3 P2a (drawn chemistry only): the graphics-team Row images are the figure
#   source (owner F1); every structure and scheme is transcribed VISIBLE-ONLY into
#   content_objects, every option image per role option:<k> into option_smiles, text-
#   named species into SMILES (content_source 'text'), an arrow+conditions math region
#   with a reagent-lexicon hit into a text-form REACTION (DL-04), the stem's ask_format
#   (statement / match / sequence / assertion_reason / combination / direct, DL-22) and
#   reagents_seen (the read-time method lexicon, §4.6) are recorded, zoom tiles
#   (figural_vision.zoom_tiles, 300 dpi) are used for wedges and small groups, and the
#   engine sets transcription_confidence 'partial' on an atom / ring / stereocentre count
#   mismatch after one re-view (never VOID, S10). §13A-3 P7 (after the derived answer):
#   answer_smiles and option_closeness. Every new field is hand-off only (never in
#   ExplanationBlock.validate(), never MANDATE D); the S19-1 output set is unchanged;
#   nothing here stops. Profile records are written record_version 2 under DP_SCHEMA 1
#   (guard S4); older records keep their r1 verdicts (guard G1).
# v2.26 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (paired with
#   figure_types v1.2, analyse_engine v1.2, blueprint_core v1.30, MockTestAnalyse v2.59.0).
#   §13A-3 Phase B records, per EVERY PYQ item (text and figural, every subject), the
#   tags the new Create / audit gates and Step 5's measurements read: figural_ask_type now
#   from the PER-FAMILY vocabulary figure_types.ASK_TYPES[family] (the chemistry family
#   gained multiple_products / outcome_ratio / two_part / quantitative_calculation — the
#   four shapes the real CSIR-NET paper uses and Test 01 lacked), drawn_names (the names
#   the stem uses for drawn species — Step 5's shown_entity_named_rate),
#   near_isomer_set (are the wrong options near-isomers of the key — R6.2 distractor mix),
#   distractor_mechanisms per wrong option (bc.MECHANISM_VOCABULARY[family]), and
#   concept (the taxonomy concept id), named_concepts (the AXIOM's named reactions /
#   rules — Step 5's tested-concept lexicon, R4.2) and stereo_decl. The profile keeps
#   per-item vectors, bands and tags (bc.DP_CONTENT_KEYS carries every one of them);
#   Step 5 joins its own stems to these records by stem text and writes the QUALITY
#   block and the EXEMPLAR BANK from them (OD-11). Schema additive; nothing here stops.
# v2.25 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (paired with
#   blueprint_core v1.29, figure_types v1.1, MockTestAnalyse v2.58.0, MockTestCreate
#   v5.89). §13A-3 Phase B also records, per figural question, a CONTENT RECORD
#   (/home/claude/pyq_content_objects.json): chemistry species as SMILES / scheme specs,
#   the answer SMILES, content_confidence, abbreviations exactly as printed and the
#   site-mark device; and for every figural question of any subject the ask type /
#   representation / scheme-grammar tags (closed vocabularies, figure_types). S7A-6
#   joins it to the scored observations; bc.dp_add_paper carries the optional keys and
#   COMPUTES content_vector. Profile schema unchanged (additive keys). Step 5 aggregates
#   the tags; Create builds the content-complexity floor from the vectors.
# v2.24 — 2026-09-14 — GAP-2026-09-14-DELIVERY-ECHO (DeliveryFooter v1.34 §9 / R6; paired
#   with MockTestAnalyse v2.57.1, PYQScan v1.6.1). Reference incident: the FINAL batch
#   shipped only the Explanation docx and left pyq_explain_progress.json +
#   difficulty_profile.json unattached while the F2 footer listed all three. S19-1
#   already proved all three were ON DISK (check 5: outputs == expected); the loss was
#   at the CALL — present_files is CLASS T (`pass`), S19-2 built `deliverables` in
#   python and never printed it, so the model performed the call from memory and the
#   "one docx per present_files" habit of batches 1..K-1 won on batch K. S19-2 now
#   prints the closed set through print_delivery_set() (PHASE 1) in the tool output
#   immediately before ONE present_files call, and names a dormant profile as
#   NOT DELIVERED THIS RUN so an absent file is never read as a forgotten one; S19-4
#   binds the footer to the present_files RESULT (R6). Reports only — no new stop,
#   no engine change, S19-1 unchanged.
# v2.23 — 2026-09-14 — GAP-2026-09-14-ROWFILE-NAME-TWO-FORMS (paired with PYQPrepare v2.2).
#   §22: a vision-transcribed Row file is identified by core_properties.category
#   ("PYQPrepare-Source-Trust:"), not by a "__vision-unverified" filename suffix — the
#   suffix no longer exists. Prose only; no rule, gate or code path changed.
# v2.22 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: OOS questions explained normally (R20)
# v2.21 — 2026-08-30 — GAP-2026-08-30-EXPLAIN-COLOUR-BINDING (explain_engine v2.11,
#   MockTestExplain v1.49.0, routes.json +figural_core/+corpus_io; SHARED_RULES 1.5 → 1.6).
#   S6A-6 COLOUR: explanation figures draw with figural_core's constants via
#   explain_engine.structure_draw / fc.text_ink / fc.fill_style. Additive; no re-render.
# v2.20 — 2026-08-29 — GAP-2026-08-29-PROFILE-UNSCORED-QUESTIONS (paired with blueprint_core
#   Cluster DP dp_add_paper paper_positions/unscored_reasons, Blueprint v1.58.0 S7-0,
#   audit_canonical v2.24). Two explained 60-question papers were EXCLUDED from an exam's
#   difficulty profile because 1–2 questions carried no derived answer (a VOID_ITEM figure,
#   a defective Row-file option set): the writer counted OBSERVATIONS against
#   total_questions and read the shortfall as a pattern change. It was not — the paper had
#   every position. S7A-6 now passes the handoff's `qtype` map keys as the paper's
#   POSITIONS (the pattern test runs on those) and the new S7A-4 `difficulty_unscored`
#   map {q: reason} for every position without an observation; such a question is
#   recorded UNSCORED in the profile with its reason and left out of the arithmetic — it
#   never excludes its paper and can never bias a mix (a gap shrinks the sample). Only a
#   paper whose positions differ from the current pattern is excluded. §R13 states
#   "added (scored/held; unscored Q list)". Exam-agnostic; no per-exam change.
# v2.19 — 2026-08-28 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ (paired with
#   explain_engine v2.10, Framework_MockTestExplain v1.48.0, audit_seam v1.3,
#   validate_framework_md v3.2). Three CATEGORY-C config keys this spec read were
#   produced by NOTHING anywhere in the framework, so their absent-paths ran on every
#   exam forever: representation_renderers (every STRUCTURE_GRAPH / LEVEL_DIAGRAM /
#   DATA_PLOT / CONFORMER verdict degraded per §6A-4), subject_code (the
#   [Subject]_EXPLAIN_LEARNINGS_v*.md subject library was unlocatable and had never
#   loaded on any exam — worsened here by P1's load list never naming the subject
#   file at all), and exam_conventions (§S8-2's EXAM_CONVENTION machinery had no
#   configured input). FIX, exam-independent, zero regeneration: (A) the requirement →
#   library → §6A-5 identifier binding is FRAMEWORK-OWNED in
#   explain_engine.REPRESENTATION_RENDERERS (§6A-6); WHETHER a question uses a
#   renderer stays a per-question §6A-1 decision, so non-scientific exams are
#   byte-unchanged. (B) subject_code RETIRED; the subject library is found by
#   DISCOVERY (explain_engine.resolve_learnings_files; >= 2 non-exam files → abstain +
#   WARN) and P1 now loads it. (C) exam_conventions RETIRED; §S8-2 reads conventions
#   from the subject library only, "never assumed" preserved. Also corrects §S6A-2's
#   stale "last three" (CONFORMER made it four, v2.14). P7 dashboard gains a
#   "Renderer preflight" line and names the loaded subject file. No section_rules.md
#   schema change, no analyse_engine change, no exam regenerated. Gate for the class:
#   validate_framework_md Check V + audit_seam v1.3.
# v2.18 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with blueprint_core Cluster DP,
#   Blueprint §S7-0, MockTestAnalyse E-9 retirement, PYQDeliver Tier-2 retirement, ScopedBlueprint
#   §1-3/§5). §7A-3 records the raw rubric SCORE (bc.difficulty_score) and the observation
#   record; S7A-4 writes q_to_difficulty_score + difficulty_obs beside q_to_difficulty; NEW
#   S7A-6 writes [ExamCode]_difficulty_profile.json on the final batch through the single
#   writer bc.dp_add_paper (pattern-changed papers recorded as excluded, never a stop);
#   S19-1 check 8, S19-2 deliverable, §R13 report line. PYQ-side rule unchanged (measurement,
#   no target); SHARED_RULES_VERSION unchanged (no RE-*/MANDATE/§4-§18 rule changed).
# v2.17 — 2026-08-24 — CHG-2026-08-24-NO-COVERAGE-BANNER (operator decision; paired with
#   MockTestExplain v1.43.0; SHARED_RULES_VERSION 1.4 → 1.5; NO engine change). The
#   S12-4 document-level coverage banner ("COVERAGE: …") is RETIRED from every delivered
#   _PYQ_Explanation.docx — interim AND final. PYQ-1 no longer calls
#   explain_engine.set_coverage_banner(); the delivered file's first non-blank body
#   paragraph is Q.1. Same reasons as the mock side: the operator does not want a
#   coverage line in the delivered document, and the downstream deliver step
#   (Framework_PYQDeliver, detect_header_paras — same as MockDeliver S4-2) strips any
#   non-blank pre-Q.1 paragraph and raises a regression alarm on it. A new §18-1 item
#   asserts zero banner paragraphs before present_files. Coverage is still stated in
#   chat (S19-3, F1/F2 footer) and asserted per batch (S4-5 guard 3) — only the in-file
#   announcement is gone. Engine untouched (BANNER-* fixtures retained, function unused).
# v2.16 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (note-only; §7A
#   itself unchanged). The v1.1 DELIBERATE DIVERGENCE note's deferred mock-side
#   difficulty treatment is RESOLVED under the adopted contract: both pipelines
#   share the rubric (bc.assess_difficulty); mock side enforces it at authoring
#   (MockTestCreate v5.60 G-DIFF), audits it mechanically (audit_canonical v2.15),
#   and re-measures advisorily at Step 9 (TestExplain §7A-M). No shared §4-§18
#   rule changed; SHARED_RULES_VERSION stays 1.4.
# v2.15 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paired with
#   MockTestExplain v1.37.0, engine v2.8). Same defect class, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.37.0 for the
#   incident record (a delivered paper with a wrong published key on a misread
#   structure, 24 hedged / nine arithmetically false WHY WRONG lines, a curated
#   library loaded and never consulted, ASCII formulae throughout). PYQ-side: §13-2b
#   SEMANTIC-OBJECT transcription folds into the §13A pre-transcription pass (a
#   STRUCTURE is transcribed to SMILES and rdkit-sanitised; no registered object
#   exists for a PYQ, so the transcription stands alone); §15-2 REWRITTEN (two
#   provenance modes, engine RECOMPUTES, hedges banned, old wording WITHDRAWN, no
#   pitfall quota); §7-7 step 3 MECHANICAL (Triggers + tripwire); §8-0c FORMULA
#   TYPOGRAPHY; §6A-1b-ii; RE-13 amended, RE-24 new; §18/§21/§24 hooks. §7-8 KEY
#   RECONCILIATION is MOCK-ONLY (a PYQ has no Step-7 commitment; D4 unchanged).
#   SHARED_RULES_VERSION 1.3 → 1.4.
```

# v2.14 — 2026-08-20 — GAP-2026-08-20-TRANSFER-SAFE-EXPLANATIONS (paired with
#   MockTestExplain v1.36.0, engine v2.7). Same defect class, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.36.0 for the full
#   incident record (a delivered 60-question paper, answer-correct on every item,
#   carrying ~17 sentences true for the item and false for its nearest neighbour).
#   NEW §7-7 transfer-safety protocol (scope → type → neighbour test → repair by
#   mechanism → recorded transfer_record); §8-2 epistemic type + scope-in-sentence;
#   §8-3 topic minimum-concept components (subject data); §8-0b is now an engine
#   gate (undeclared universal raises; kept absolutes declared); §14-1 three-part
#   (TRANSFER-SAFE), §14-5 four-field record; §15-3 MSQ wording WITHDRAWN and
#   rewritten (learner-psychology boilerplate banned by the engine); NEW §6A-1c
#   representation alignment + §6A-3b distribution tripwire; CONFORMER verdict;
#   §24 loads the SUBJECT-level [Subject]_EXPLAIN_LEARNINGS_v*.md (same schema,
#   same parser; precedence exam > subject > spec) + §24-5 defect codes; §5-1/
#   §5-2/§5-3, §18, §R3, §21 hooks. Student-facing format unchanged and LOCKED.
#   SHARED_RULES_VERSION 1.2 → 1.3.
# v2.13 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-EXECUTION-INTEGRITY (paired with
#   MockTestExplain v1.35.0, engine v2.6). Same four defects, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.35.0 for the full
#   incident record (a delivered 60-question paper, audited).
#   D1 — the §9 error type becomes INTERNAL metadata: still mandatory, recorded per
#   wrong option / pitfall in progress state, and the visible line delivers the same
#   diagnosis in natural language — never the snake_case token. Engine v2.6 raises at
#   write time on any taxonomy token in student-facing text and re-scans the rendered
#   bytes at verify time.
#   D2 — NEW §6A-1b structure-answer presumption + verdict↔emission coherence: when
#   the verified answer IS a structure, STRUCTURE_GRAPH is presumed and PROSE needs a
#   recorded justification; §6A-3 passes the verdict INTO the block (engine v2.6
#   representation_verdict) and a visual verdict with zero figures raises; a §6A-4
#   degrade records the DEGRADED requirement. PYQ-SPECIFIC: VOID_ITEM WINS — §6A-2b
#   forbids any generated figure for a VOID_ITEM, so the presumption is void for it
#   by construction.
#   D3 — NEW §14-5: SPEED-HACK eligibility recorded per question, the inclusion RATE
#   reported in §R3, and an all-hack batch re-runs the §14-1 test before §18 — a
#   tripwire, never a quota (reference incident: a hack on 56 of 60 questions).
#   D4 — NEW §7-0c enumeration-before-formula and §7-6 decisive-claim consistency
#   (a right answer with contradictory reasoning is invalid; repair returns to §7-1,
#   never to patched prose). Both domain-neutral per the v2.11 convention.
#   RE-6d added; RE-13 restated in both files; SHARED_RULES_VERSION 1.1 → 1.2.
#   ALSO: the stale "currently 64/64" aside in MANDATE A is removed — the §21-0
#   class (an exact count asserted in prose is wrong from the next fixture on; the
#   engine prints a higher count today and the gate is floor-form anyway).
#   ENGINE FINDINGS (v2.6, from writing its fixtures): the v2.3/v2.7 figure-validation
#   loop sat AFTER the NAT branch's return, so NAT figures were never validated at
#   construction — moved above the type split; anomaly blocks now reject figures as
#   student content; an AXIOM naming an option label raises (§8-2).
# v2.12 — 2026-08-19 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT (paired with
#   MockTestExplain v1.34.0, engine v2.5). SPEC-ONLY. P6's conflict check compared
#   Q_TOTAL, option count, question type and opt_re-vs-label_scheme, but never compared
#   the DECLARED `option_label_format` values against each other — and section_rules
#   declares that value once in the CATEGORY C header and once per SECTION block, from
#   two different generators. A header/section disagreement therefore passed silently and
#   every option carried the wrong label. P6 now compares all declarations and HALTs on
#   any disagreement, printing each value with its location. See MockTestExplain v1.34.0
#   for the full incident record.
# v2.11 — 2026-08-19 — GAP-2026-08-19-DOMAIN-LEAK-IN-UNIVERSAL-RULES (paired with
#   MockTestExplain v1.33.0). SPEC-ONLY, no engine change, no rule weakened. The four
#   rules added in v2.9/v2.10 were written in one domain's vocabulary inside an
#   exam-agnostic spec: §7-0a/§7-0b listed domain-specific conditions and assumptions as
#   though universal, §7-5 made domain-specific checks MANDATORY, and §8-0a banned
#   domain-specific quantities. Rules are now stated neutrally, lists are ILLUSTRATIVE and
#   read from the exam's own material, and every §7-5 check is CONDITIONAL ON
#   APPLICABILITY. See MockTestExplain v1.33.0 for the full record.
# v2.10 — 2026-08-19 — GAP-2026-08-19-CONDITIONAL-CORRECTNESS (paired with
#   MockTestExplain v1.32.0). SPEC-ONLY. Same four rules, so both explanation paths hold
#   one standard; see MockTestExplain v1.32.0 for the full incident record.
#   §7-0a CONDITION CAPTURE · §7-0b ASSUMPTION LEDGER · §7-5 NUMERICAL VERIFICATION ·
#   §14-3b SHORTCUT VALIDITY DOMAIN.
#   PYQ SHARPENS §7-0a: these are REAL past papers, so a condition the stem supplies was
#   put there by the examining body to DISCRIMINATE. A stated condition that changed
#   nothing in the derivation is strong evidence the question was misread.
# v2.9 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-CONTENT-DISCIPLINE (paired with
#   MockTestExplain v1.31.0, engine v2.4). Same three defects, same fixes, so the two
#   explanation paths hold one standard. See MockTestExplain v1.31.0 for the full
#   incident record.
#   D1 — NEW §8-0a SUPPORTED VALUES ONLY: every number traces to the stem, a syllabus
#   constant, or a shown derivation. PYQ SHARPENS THIS: these are REAL past papers, so
#   an invented yield or constant does not merely mislead — it misrepresents what the
#   examining body actually asked and what it supplied.
#   D2 — NEW §8-0b CALIBRATED LANGUAGE: absolutes reserved for claims absolute in the
#   subject's own terms; tendencies take calibrated terms.
#   D3 — NEW §12-4 INTERIM COVERAGE BANNER via engine v2.4 set_coverage_banner(), so a
#   mid-run artefact declares its own state wherever it travels. strip_solutions()
#   removes it, keeping the questions-only copy byte-equal to the Row file source.
# v2.8 — 2026-08-19 — GAP-2026-08-19-STALE-PIN-SWEEP (paired with MockTestExplain v1.30.0).
#   SPEC-ONLY, no engine change. Same CLASS as the paired release: an exact self-test
#   count written into prose is correct only until the next fixture is added, and this
#   file carried two such sites after v2.7 de-pinned only the §R1 report line.
#   D1 — §21 DEFINITION OF DONE HARD-PINNED THE ENGINE COUNT. Item 1 read "engine
#   62/62" while the engine prints 78/78 — the failure mode of
#   GAP-2026-08-13-STALE-SELFTEST-PIN, in the place that fix (v2.5, which converted the
#   P0 gate) never reached. Converted to floor form.
#   D2 — THE ENGINE-CAPABILITY REFERENCE WAS INTERNALLY INCONSISTENT. Two adjacent
#   lines described the same engine's two self-tests in two different conventions:
#   `--self-test` pinned "62/62 PASS" while `--self-test-audit` correctly used the
#   floor form "N >= 10". Both now use floor form.
#   NEW §21-0 states the rule as a RULE, matching MockTestExplain §21-0 verbatim in
#   substance, so the two explanation specs cannot drift apart on it.
# v2.7 — 2026-08-19 — GAP-2026-08-19-PYQEXPLAIN-NO-REPRESENTATION-ROUTER. SPEC-ONLY:
#   no engine change. PYQ-1 shares explain_engine.py with TestExplain, so since engine
#   v2.2/v2.3 it has SILENTLY INHERITED the Tier-3 notation guard and the figure-emission
#   surface (RepresentationFigure / ExplanationBlock.figures) — capability with nothing
#   directing its use. Result: every PYQ document stayed prose-only while the Mock path
#   gained schemes, orbital diagrams and rendered equations. This release closes that.
#   NOTE ON SCOPE — §11 IS ALREADY CORRECT HERE AND IS NOT TOUCHED. PYQ-1's S11-1 has
#   always documented the ⟦MATH:…⟧ grammar properly and has always said "guards are
#   region-aware: \\frac inside a region is legal; the _BANNED_LATEX list applies to prose
#   outside regions only". The §11 defect fixed in MockTestExplain v1.27.0 never existed
#   in this file. Verbalised arithmetic is therefore NOT a documented-cause defect here;
#   §6A-2's EQUATION requirement simply makes the existing rule explicit at routing time.
#   D1 — NO REPRESENTATION ROUTER. New §6A, adapted to PYQ (NOT copied): PROSE is the
#   default and a visual is EARNED on the §14 two-part test; renderers are declared per
#   exam in section_rules; degrade is loud. Two PYQ-specific rules that do not exist in
#   the Mock spec: (a) the router runs AFTER §13A transcription, so a figural question is
#   routed from what was actually SEEN, never from the stem text; (b) a VOID_ITEM figure
#   FORBIDS a generated STRUCTURE_GRAPH for that question — no answer is published for a
#   VOID_ITEM at all (§13A-5), so drawing a structure for one would be manufacturing
#   content from an untranscribable source, the precise thing RE-11 forbids.
#   D2 — §6 HAD NO STRUCTURAL OR DERIVATIONAL CLASS. C-STRUCTURAL and C-DERIVATIONAL
#   added; C-FIGURAL made family-aware.
#   D3 — §13 WAS BLIND TO SCIENTIFIC FIGURES. S13-4 defined the figural AXIOM as "the
#   visual rule" — the reasoning-puzzle vocabulary. Split into §13-4a
#   (transformation-puzzle, preserved) and §13-4b (scientific-diagram). PYQ papers are
#   REAL past papers, so this is the more consequential half of the split here: a JAM or
#   GATE stem figure is essentially always a scientific diagram.
#   D4 — §9 forced science distractors into aptitude labels; eight scientific error types
#   added.
#   D5 — §R1 PROVENANCE WAS STALE ("spec v1.1 · engine 62/62" against v2.6 / 78/78) and
#   §R3 had no representation line. Both fixed; the GATES stay floor-form (P0, v2.5).
# v2.6 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: a name is added to this file's executable surface. NO ARTEFACT CHANGES.
#   This spec CALLED present_files() from compiling python while DEFINING it nowhere —
#   a guaranteed NameError the moment that path executes as python. Five such call
#   sites stood across four specs; spec_name_audit_baseline.json had accepted
#   `present_files` as a known-unbound name in all four, which is why the ratchet
#   reported OK for weeks. SAME SHAPE as D2 of
#   GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed the instance and left the
#   class standing. FIX: a CLASS: T stub is declared in this file, matching the
#   corpus's per-file house pattern for CLASS T markers.
# v2.5 — 2026-08-13 — GAP-2026-08-13-STALE-SELFTEST-PIN: the MANDATE-A engine gate pinned
#   the literal "SELF-TEST: 62/62 PASS" while explain_engine.py prints 64/64 — a HALT on
#   every session with a healthy engine. Converted to the FLOOR form (N/N PASS, N >= 62),
#   the AUTH_GATE_FLOOR pattern; same for the --self-test-audit reader pin (>= 10).
# [ExamCode] project | PYQ-1 (PYQExplain) | Exam-agnostic
#
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take a PYQ Row file (.docx, Step 1 output) from Google Drive, INDEPENDENTLY
#   DERIVE the answer to every question, and INTERLEAVE a perfect, highest-standard
#   explanation after each question — without altering one byte of the original paper.
#   Emit [ExamCode]_[date]_[session]_PYQ_Explanation.docx: a 100%-explained, zero-
#   defect learner-facing solution document for that exam sitting.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION (PYQ Explanation Pipeline)
# ════════════════════════════════════════════════════════════════════════
#   PHASE 1 — Already completed (shared with Mock/Test pipeline):
#     Step 1  PYQPrepare    → Row file (Q.1-Q.N, original exam order) → Google Drive
#     Step 2  PYQDraft/Scan/Approve → taxonomy, exam_config.json → project
#     Step 3  PYQSort       → Sorted PYQ docs → Google Drive
#     Step 5  PYQExtract    → section_rules.md + subtopic_manifest.json → project
#
#   PHASE 2 — PYQ Explanation (this pipeline):
#     PYQ-1  PYQExplain      → [ExamCode]_[date]_[session]_PYQ_Explanation.docx  ← THIS STEP
#     PYQ-3  PYQFormat       → [ExamCode]_[date]_[session]_PYQ_Formatted.docx  (student)
#     PYQ-4  PYQDeliver      → [ExamCode]_[date]_[session]_PYQ_Final.docx       (portal)
#     (PYQ-2 PYQExplainAudit was RETIRED in v2.1. PYQ-3 and PYQ-4 are INDEPENDENT —
#     both take PYQ-1's _PYQ_Explanation.docx directly, neither depends on the other.)
#
#   PYQ-1 runs in the [ExamCode] project (exam-specific). It runs AFTER Steps 1-5
#   have produced section_rules.md, subtopic_manifest.json, and exam_config.json.
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. No section name, no subtopic,
#   no question count, no time/marks figure, no option count, no option label, no
#   language, no figural type, no block label is hardcoded. Every such value is READ
#   at runtime from:
#     • question/option counts, Q total → Row file scan + exam_config.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets,
#       OMML_required, option label format, language, block labels/markers, figural
#       object/transformation types, escape tokens, passage word ranges
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, subtopic names
#       → subtopic_manifest.json
#   Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT, CSIR, Banking, RRB, state
#   PSC, or any exam with valid Step 1-5 outputs.
#

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQExplain.md.

```
# v2.4 — 2026-08-10 — AUTHORING-TIME TIER-3 COMPILE GATE (GAP-2026-08-10-EXPLAIN-
#   MATH-DEGRADE-SILENT). Root cause, measured on a real 60-Q paper: every formula
#   was authored as a ⟦MATH:…⟧ region, but many used LaTeX outside the Tier-3
#   grammar (\tfrac/\dfrac, \varepsilon, \vec r / \sqrt3 unbraced, \frac12,
#   \left…\right, \begin{pmatrix}). t3_compile rejected them; per the no-halt render
#   contract add_math_text DEGRADED each to plain text and RECORDED it in
#   T3_STATS['failed'] — shipping raw LaTeX in the document. It was not caught
#   because verify_explanations() REPORTS the degrade ledger through its RETURN
#   value (ok, problems), not by raising, and the §18 self-audit consumed only
#   whether the call raised. TWO GaPS, BOTH now closed, exam-agnostically:
#   (E1 — the permanent fix) ExplanationBlock.validate() now COMPILES every
#   ⟦MATH:…⟧ region via t3_compile and RAISES a ValueError on MathCompileError, so
#   a malformed region fails at CONSTRUCTION and can never reach the renderer.
#   validate() is the one universal chokepoint (every block, every step, BOTH
#   pipelines, all exams, one explain_engine.py under MANDATE A) and it RAISES, so
#   no producer harness can bypass it — mirrors the NAT fail-at-construction posture.
#   (E2 — defence in depth) §18 gains an explicit BLOCKING contract + literal
#   S18-1a HARD-STOP that asserts ok is True AND problems == [] AND T3_STATS
#   ['failed'] is empty, converting the RETURNED ledger into a delivery-blocking
#   condition. Engine self-test unchanged (62/62). Touched: §S5-2, §S11-1, new
#   §S11-1a, §S18-1, new §S18-1a, header + END sentinel + SHARED_RULES_VERSION.
#   ENGINE CHANGE (explain_engine.py): validate()'s per-sentence guard compiles
#   regions and raises; ships with this release (MANIFEST regenerated).
# v2.3 — 2026-08-09 — QUESTION TYPE RESOLVED POSITION-BASED + qtype DELIVERED as a
#   fourth sidecar map. Until v2.2.1, P4 resolved Question Type ONLY from
#   section_rules answer_cardinality (a subtopic-scoped corpus statistic), and the
#   delivered pyq_explain_progress.json carried only three maps — no qtype. On
#   section-determined-MSQ exams (IIT JAM, GATE, …) every subtopic in the MSQ section
#   reads 'single', so P4 built those questions as MCQ and PYQ-4 had no per-question
#   type to consume. P4 now has a Tier 1 that, when exam_config.marking_scheme carries
#   >1 distinct question_type, resolves type POSITION-BASED from marking_scheme[].q_range
#   (mirroring MockDeliver v1.7) — the "set explicitly" mechanism §5-1 names — falling
#   back to the prior structural rule for single-type/subtopic-based exams. The resolved
#   qtype is now RECORDED and DELIVERED (§S7A-4) as the fourth map and coverage-gated at
#   S19-1 check 7. qtype is a structural type, MANDATE-0-safe. Consumed by PYQDeliver v1.8
#   Tier 2. Touched: P4, §S7A-4, §S0-2, §19 S19-1, header + END sentinel.
# v2.2.1 — 2026-08-09 — Fix two v2.2 deployment findings on the handoff delivery.
#   (1) The handoff shipped under a BARE name (pyq_explain_progress.json) with no paper
#   identity, so two papers' sidecars (same exam, different session) collided by filename
#   and the wrong classification map could silently tag a portal. It is now delivered under
#   the SAME [ExamCode]_[date]_[session] stem as the docx, and PYQ-3/PYQ-4 load the
#   identity-matched name derived from the attached docx. (2) S19-1's shutil.copy ran before
#   the checklist and would raise an uncaught FileNotFoundError if the source were missing,
#   making check 6 unreachable; the copy is now guarded so a missing handoff lands as a clean
#   S19-1 HARD STOP. Touched: S0-2, S19-1, S19-2.
# v2.2 — 2026-08-09 — pyq_explain_progress.json PROMOTED to a delivered artifact.
#   Since PYQ-2 retired (v2.1), this JSON is the SOLE metadata source for PYQ-3/PYQ-4,
#   which run in a fresh chat where /home/claude is gone — yet PYQ-1 previously kept it
#   internal, so the user had no way to carry it forward. It is now delivered to
#   /mnt/user-data/outputs on the FINAL batch (100% coverage, all maps complete) as a
#   first-class pipeline handoff. It carries only classification / option-counts /
#   difficulty (NO answer keys — those stay in the never-delivered pyq_answer_keys.json),
#   so it is MANDATE-0-safe. Touched: S0-2, S19-1 (gate now permits the one handoff on
#   the final batch), S19-2 (present_files ships it).
# v2.1 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED from the PYQ pipeline (operator
#   decision). PYQ-1 is now the SOLE producer AND the FINAL self-certifier: its §18
#   self-audit is the only certification this document receives, there is no downstream
#   independent re-derivation or completion gate, and the official-answer-key cross-check
#   (formerly PYQ-2 D4) no longer exists anywhere. Correctness now rests entirely on
#   producer discipline (§7 derive-twice, RE-18 web-verify, §13/§13A view-every-image)
#   plus the engine's write-time shape guarantees. PYQ-3 (PYQFormat) and PYQ-4 (PYQDeliver)
#   now consume PYQ-1's _PYQ_Explanation.docx directly, with pyq_explain_progress.json as
#   the SOLE metadata source. No algorithm, engine, ExplanationBlock field, gate, or
#   delivered byte changes; the edits retire references to the removed auditor and the
#   (now open) learnings feedback loop. Touched: PIPELINE POSITION, CORE PRINCIPLE,
#   §7A recording note, §14 S14-4, §16, §17-3, §18-2, §20 §R8/§R11, §24, Appendix A.
# v2.0 — 2026-08-07 — TIER-3 STRUCTURED MATH (GAP-2026-08-07-EXPLAIN-OMML, remedies E1–E4).
#   Measured on IIT_JAM_PHYSICS 15-Feb-2026 explanations (60 Q, 56 affected):
#   (a) the v1 OMML builders interpolated RAW text into m:num/m:den — schema-invalid
#   XML every Word engine renders as an EMPTY ▯/▯ placeholder, while the verifier's
#   itertext() reader happily read the bare text, so 12 destroyed fractions shipped
#   under green checks (verifier had been loosened to match the producer's bug);
#   (b) the §11 guard understood only digit/digit slashes, so generation evaded it
#   with an ASCII dialect — 234 "÷" fractions, V_B underscores, x^b carets, √( ),
#   combining-character A̅/E⃗ accents — all guard-invisible, all typographically wrong;
#   (c) inherited upstream loss (pre-v2.0 Row files with missing symbols) was
#   faithfully laundered, because the fidelity check compares output to its own input.
#   Fix (all in explain_engine.py — MockTestExplain Step 9 inherits via MANDATE A):
#   E1 builders _r()-wrap + XML-escape all content; verifier check 5 now REJECTS
#   bare-text num/den (the loosened reader is reverted and locked the other way);
#   E2 add_math_text v2.0 dispatches ⟦MATH:…⟧ regions through the SHARED Tier-3
#   compiler (new repo module t3_mathcomp.py, byte-identical to PYQPrepare §S3-5b,
#   drift-locked in the engine self-test) with the same no-halt/no-markup graceful
#   degradation and verbatim Ctrl+F quoting; E3 guard_sentence bans the dialect
#   (÷, ^, _x, √(, combining accents) with the region spelling as the named remedy,
#   and is region-aware (\frac etc. are legal INSIDE regions); E4 new
#   source_math_health() input check names upstream loss in plain words ("re-run
#   Step 1 v2.0 first") before any explanation is generated. Verifier gains Tier-3
#   structural integrity, rendered-dialect residue, and a region ledger + degrade
#   report. Self-test 10 → 24 audit checks incl. a negative-proofed drift lock.
# v1.2.1 — 2026-08-03 — REGRESSION REPAIR (one line; zero rule change).
#   v1.2 was authored from a base predating 2026.08.03.5 and reintroduced a pointer to
#   Framework_MockTestCreateAudit.md, a spec deleted in that release. Restated as
#   audit_canonical.py, which is where the A-NAT-GRADE implementation actually lives.
#   Every §13A figural pre-transcription rule, the P2a preflight, the VOID_ITEM/AMBER
#   routing and the §R12 reporting shape introduced by v1.2 are UNTOUCHED.
#
# v1.2 — 2026-08-03 — §13A FIGURAL PRE-TRANSCRIPTION PASS (new capability).
#   Figural images are VIEWED ONCE, at P2a, and persisted as TEXT. Every batch
#   then reads the transcription instead of re-viewing the image.
#
#   THE DEFECT THIS REPAIRS. `view` is CLASS T (CLAUDE.md EXECUTION-BOUNDARY
#   LAW) and an image held in context is not durable. PYQ-1 previously viewed
#   each figure lazily, inside whichever batch contained it — so the LAST
#   figural batch asked the image channel for a fresh render after a clone, a
#   bootstrap, two specs read in full (RULE 2), and five prior batches. Measured
#   in one session on pixel-verified non-blank files: early views returned
#   perceptible content, later views on the SAME files returned empty payloads,
#   and a retry did not recover. The failure then surfaced as a HALT inside
#   Batch 1 rather than at preflight, and §13 offered no sanctioned path
#   onward — the CERTIFIED-DEGRADED (VISION) route in DeliveryFooter §5 Q0b was
#   scoped to Step 8 only.
#
#   THREE PROPERTIES, ALL NEW. (a) Vision is spent at the EARLIEST executable
#   moment, when context is lightest. (b) What was seen becomes durable text on
#   disk, so a figure is viewed exactly once per paper no matter how long the
#   run or how many resumes it survives. (c) A dead image channel is detected at
#   P2a in seconds, by measurement, instead of as a mid-batch halt.
#
#   IT NEVER HALTS. CLAUDE.md: "A CLASS T failure must be LOUD, and must NOT
#   halt." An untranscribable figure makes its question VOID_ITEM and the run
#   AMBER; the paper still completes, still delivers every other question, and
#   still ships. BLOCKING is never emitted for a vision condition. This aligns
#   PYQ-1 with the corpus rule that no rendering/observation condition may stop
#   a paper, and DeliveryFooter v1.11 extends Q0b to carry the amber.
#
#   RE-11 IS NOT WEAKENED — IT IS MOVED EARLIER AND MADE AUDITABLE. A figural
#   answer is still derived only from what was actually seen. What changes is
#   that "what was seen" is now a recorded artefact a later step can inspect,
#   rather than a claim about a context window nobody can re-examine. A question
#   whose figure was never legibly seen now yields NO published answer, where
#   before it yielded a halt (best case) or an unfalsifiable assertion (worst).
#
#   Zero changes to explain_engine.py (62/62 unchanged), the ExplanationBlock
#   model, the delivered document, §12 byte-identity, or any existing gate.
#   New engine: figural_vision.py (pure stdlib, Phase A/C only — it models no
#   tool call and contains no CLASS T stub).
#
# v1.1.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   29 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQExplain'. The current companion block, the
#   v1.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.1 — 2026-07-24 — §7A PER-QUESTION DIFFICULTY ASSESSMENT (new capability).
#   PYQ-1 becomes the SINGLE PRODUCER of per-question difficulty for the PYQ
#   pipeline. It emits `q_to_difficulty` into pyq_explain_progress.json; PYQ-2
#   validates it; PYQ-4 consumes it as Tier 1 of its §2-3 resolver.
#
#   WHY HERE AND NOWHERE ELSE. Difficulty for a PYQ paper is a MEASUREMENT, not a
#   choice: the exam body already wrote the questions, so the label must follow the
#   content. Only a step that READS AND SOLVES a question can measure what it
#   demands — and PYQ-1 is the only step in this pipeline that does. PYQ-4 tags
#   from a document it never solves, which is why its Tier 2 keyword scorer
#   (E-9) collapsed an entire IIT JAM Biotechnology paper to one label: 60 of 60
#   questions "Easy", with E-9's computation axis at its floor for all 60. No
#   keyword list fixes that, because a keyword list is exam-SPECIFIC and this
#   framework serves ~200 exams.
#
#   NO NEW COGNITIVE WORK. §7A does not analyse anything. Every input it reads is
#   an observation PYQ-1 has ALREADY made by the time it runs: the §6 class, the
#   DEDUCTION step count it just built, the AXIOM principle count it just wrote,
#   whether the §14 SPEED HACK gate passed, whether §7's two methods agreed, the
#   §10a negative-phrasing scan, and the §5-1 qtype. The assessment is a pure
#   function of those observations, evaluated by blueprint_core.assess_difficulty.
#
#   DETERMINISM CONTRACT. The scoring function is pure and deterministic: identical
#   observations always yield the identical label. The observations themselves come
#   from model derivation, so a FRESH PYQ-1 run on the same paper may observe a
#   different step count and produce a different label. That is bounded and
#   acceptable because the value is WRITTEN ONCE to the progress JSON and every
#   downstream reader performs a pure lookup — PYQ-4 §S2-3d's guarantee that "no
#   model judgment participates in tag resolution at PYQ-4 time" stays literally
#   true. (v2.1: PYQ-2's independent check on this value is retired — the difficulty
#   label is now producer-only.)
#
#   Zero changes to explain_engine.py. Zero changes to the ExplanationBlock model,
#   the delivered document, or any existing gate. The assessment is metadata only
#   and is NEVER rendered into the paper.
#
```

Entry v2.28 moved at framework release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; v2.29 supersedes).

```
# v2.28 — 2026-11-07 — GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS (RE-25 CHEM-STRUCTURE
#   STANDARD; paired with MockTestExplain v1.54.0, explain_engine v2.13, corpus_io v1.19, figural_core
#   v5.91, SHARED_RULES_VERSION 1.7, the repo-shipped CHEMISTRY_EXPLAIN_LEARNINGS_v1.md).
#   Incident: CSIR NET Chemical Sciences 18-Jul-2026 — 120 questions, 34 structure questions,
#   ZERO explanation figures, 11 chemistry defects, every key right: the router said PROSE,
#   the renderer drew one molecule, figures could land only in DEDUCTION, nothing compared
#   the derived product with the keyed option, the chemistry library had never loaded.
#   NEW RE-25 (decided per question from CONTENT — never a subject, topic or exam name, §6A-7
#   T1-T3, ask shapes A1-A12): every step drawn inside DEDUCTION with curly arrows (E-03
#   proved), every wrong option drawn under its own heading (E-05), every figure layout-gated
#   and auto-retried (E-04), reviewed once in-turn (E-09), reconciled with the options (E-06
#   c-e, E-07), stereo descriptors re-derived (E-06 f), per-step balance (E-06 g), pipeline
#   vocabulary banned (E-08). NEW §6A-7..§6A-12, §7-0d / §7-0e, §24 S24-7; amended §5-1 /
#   §5-3, §6-1, §6A-1 / 1b / 2 / 3b / 5 / 6, §7-2, §8-3 / §8-5, §15-2, §18-1, §R3, §21.
#   §13A-3 guard S10 is amended (option_smiles / answer_smiles become validate() inputs on an
#   APPLIES question, DL-18 mandatory there) and §17-3 gains the NEAREST-OPTION outcome
#   (the derived product matches no printed option: full chemistry, nearest option bound,
#   difference disclosed in the last DEDUCTION paragraph, OPTION-DRAWING-DEFECT recorded).
#   No new section heading; a NOT_APPLICABLE question takes no new obligation and renders
#   byte-identically (GAP Section 10.1; engine fixture AT-4 b).
```

Entry v2.29 moved at framework release 2026.11.08.1 (GAP-2026-11-07-RE25-HARDENING; v2.30 supersedes).

```
# v2.29 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (paired with blueprint_core v1.33,
#   MockTestCreate v5.94). FORWARD-ONLY, one field rule: §13A-3 "named_concepts" of an ORGANIC
#   question is written with the CANONICAL label of bc.l2_vocabulary() wherever the AXIOM's concept
#   is in that controlled vocabulary (the vocabulary the organic decision-load ruler scores, owner
#   D4); a concept outside it is written as printed. Profiles written earlier are NOT re-run:
#   bc.l2_concept_match maps the printed names onto the same labels, and the ruler discloses its
#   concept coverage. No other field, phase, gate or output changes.
```

## Framework_PYQFormat.md

Entry v1.6.0 moved at framework release 2026.11.06 (EC-P42; v1.6.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQFormat.md.

```
# v1.6.0 — 2026-09-03 — GAP-2026-09-03-PAGE-BORDER: a full-page border frames EVERY page of
#   the formatted document. NEW §6A defines the border (pgBorders: single 0.75pt line,
#   #1F3864, 24pt from the PAGE edge, all four sides, display attribute ABSENT = all pages
#   by the OOXML standard itself); S13-2 step 7 wires it into EVERY sectPr; S13-8 carries
#   PGBORDERS_ORDER, apply_page_border(), the edge-case-23 margin WARN and
#   selftest_page_border(); S8-3 rule 5 verifies presence + exact attributes (HARD STOP);
#   §12 edge cases 22–24 (pre-existing border REPLACED per O-3; narrow margins WARN per
#   O-4; multi-section = every sectPr); Appendix A PAGE_BORDER_* tokens. Owner rulings
#   O-1..O-4 (2026-09-03): scope PYQFormat ONLY; constants locked; replace; WARN-not-HALT.
#   Chrome-only change: pgBorders is a section property, never a body element — S8-4..S8-8
#   are unaffected by construction; proven on a real 76-page artefact (official validator:
#   0 new errors vs baseline; a naive-position mutant is REJECTED by the S8-9 gate).
```

Moved from the file header at framework release 2026.08.15.14; v1.5.2 entry moved at 2026.09.03.3.
Current-version entry remains in Framework_PYQFormat.md.

```
# v1.5.2 — 2026-08-09 — PYQExplain v2.2.1 delivers the sidecar under the paper-identity stem
#   [ExamCode]_[date]_[session]_pyq_explain_progress.json. §1/§0 now derive the expected sidecar
#   name from the attached docx and load THAT (prevents a colliding sidecar from another paper
#   silently supplying the classification map). Legacy bare names accepted with a WARN.
# v1.5.1 — 2026-08-09 — PYQExplain v2.2 now DELIVERS pyq_explain_progress.json to outputs.
#   Clarified §1/§0 that the sidecar is attached alongside the _PYQ_Explanation.docx (both
#   are PYQExplain deliverables). No behaviour change — the sourcing priority is unchanged.
# v1.5 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. PYQ-3 now takes PYQ-1's
#   _PYQ_Explanation.docx as its STANDARD input (a legacy _Complete.docx is still
#   accepted, unchanged, but is no longer produced). q_to_classification is read from
#   pyq_explain_progress.json as the primary sidecar. No runtime behaviour changes —
#   PYQ-3 never audited; it formats whatever it is given. Edits retire the "certified by
#   PYQ-2" framing (the input is now producer-certified by PYQ-1's self-audit, not independently
#   audited) and the PYQ-2 cross-references. Touched: PURPOSE, ZERO-MUTATION rationale,
#   §0/§1 input contract + map priority, §4, S7-2, §9/§10 notes, §12 edge cases.
# v1.4.2 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   173 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQFormat'. The current companion block, the
#   v1.4.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.4.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.3, several versions behind the header, so the last line of the file contradicted
#   the first. Documentation only — not one line of behaviour changes. It went unnoticed
#   because BOTH integrity tools were structurally blind to it: validate_framework_md.py
#   Check C recognised only the '# END OF <name> vN' sentinel form and skipped the
#   comparison entirely for the '**End of <name>.md (vN)**' form used here, while
#   audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
```

## Framework_PYQPrepare.md

Entries v2.1–v2.2 moved at framework release 2026.11.06 (EC-P42; v2.2.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQPrepare.md.

````
# v2.2 — 2026-09-14 — GAP-2026-09-14-ROWFILE-NAME-TWO-FORMS (owner ruling 2026-09-14).
#   §6 now defines EXACTLY two legal output filenames — [ExamCode]_DD-Mon-YYYY_<session
#   _keyword>-<N>.docx and [ExamCode]_DD-Mon-YYYY.docx — with no variant for any
#   condition. The v1.7 "__vision-unverified" suffix for FORMAT C1 / C-HYBRID Row files
#   is REMOVED (§6, §7, S1-13 build note, §9 CALL B4 variant). All logic is retained:
#   mark_vision_transcribed() still sets core_properties.category unconditionally in the
#   S1-13 path, the §7 "human verification required" delivery note is unchanged, and
#   §10's provenance ripple is unchanged. CHECK 14 re-anchored: it compared the
#   core-property against the filename suffix; with the suffix gone it now compares the
#   core-property against the caller's claim — validate_row_file(source_trust=), the
#   value mark_vision_transcribed() returned (None on the text path). That parameter
#   existed since v1.7 and was never read; it is now the second signal, which is stronger
#   than the filename was (two signals written by one code path at one moment could
#   only ever agree); CHECK 14 also compares the trust VALUE (VISION-TRANSCRIBED vs
#   MIXED), which the suffix never could. Consumer side: PYQExplain v2.23 (Limitations
#   section) identifies vision-transcribed Row files by the core-property. Row files
#   already delivered with the suffix remain valid. No engine change; no downstream glob
#   or reader ever matched the suffix.
# v2.1.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: two-view invariant -> tagged fence; 10 prose mentions to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v2.1 — 2026-08-15 — GAP-2026-08-15-BAREQ (producer side). S1-4 contract rewritten: a
#   bare "Q.N" stem — OMML-only, figure-only, or empty/corrupt — is a LAWFUL normalised
#   form with a named reason, and "repairing" it by injecting filler ("Solve:") is now
#   PROHIBITED: filler is not in the source, survives into Step 5's extraction and into
#   every mock derived from the item, and corrupts the corpus it appears to fix.
#   CHECK 1/2/12/15/21 delegate to bc.detect_question_start() — they carried a PRIVATE
#   regex r'^Q\.\d+' that needed no trailing content, so Step 1 certified "Q-count = 60,
#   sequential OK" on a file Step 3 read as 56 and delivered it green. CHECK 13 calls
#   bc.is_bare_q_label(): it already had the right regex gated on the wrong payload test
#   (NEXT paragraph for a drawing, never the SAME paragraph for an equation) and now
#   reports OMML-only, figure-only and truly-empty stems separately. S2-4 sanitise() and
#   CHECK 7 widen to the zero-width class (U+200B/200C/200D/2060/FEFF), which str.strip()
#   does not remove and \s does not match, so "Q.4<ZWSP>" defeats every table entry while
#   looking correct on screen. NEW CHECK 22 (WARN, 21 -> 22): producer/consumer
#   Q-detection agreement — the <w:t>-only view vs the <w:t>+<m:t> view of the SAME
#   document, the one construction a shared blind spot cannot satisfy.
````

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQPrepare.md.

```
# v2.0 — 2026-08-07 — TIER-3 STRUCTURED MATH (GAP-2026-08-07-OMML, remedies M1/M2/M4/M5).
#   Root cause (measured on IIT_JAM_MATHEMATICS 15-Feb-2026, 60 questions): S1-13
#   emitted FLAT Unicode transcription, destroying 2-D math structure at capture
#   time; Tier-2 regex reconstruction then recovered only digit fractions and √N.
#   Result classes: letter-fraction flattening, ^/_ artefacts, inline big-operator
#   limits, cases/matrix structures PARAPHRASED into prose (Q.11/14/17/33/34/36/
#   37/49/52/56), hybrid-font islands, and the bare-label OMML option conflict.
#   Fix: (M1) S1-13 now REQUIRES ⟦MATH:…⟧ LaTeX-lite regions for all structural
#   math and BANS paraphrasing matrices/vectors/cases into prose, with declared
#   STRUCT_FLAGS; (M2) new S3-5b deterministic LaTeX-lite→OMML compiler (fractions,
#   radicals, scripts, n-ary with true operands, limLow, cases, matrices, sPre,
#   stretchy delimiters, accents, \binom, Greek/symbol map; STRICT CORE with a
#   FORGIVING BOUNDARY — a region the compiler rejects never halts the run and
#   never ships silently: it is delivered as ordinary plain text — no colour,
#   no highlight — and CHECK 20 quotes it verbatim for Ctrl+F, with the remedy
#   in plain operator words, under an F1 AMBER footer);
#   render_text_with_math() v2.0 dispatches Tier-3 regions first and
#   keeps the v1.5 legacy path byte-compatible for plain segments; (M3, in
#   corpus_io Cluster I) text_of() = w:t + m:t canonical accessor; CHECK 9 v2
#   accepts bare "N." labels whose payload is <m:oMath> (producer mirror of S-1);
#   (M4) CHECK 19 structure-residue, CHECK 20 region round-trip, CHECK 21 declared-
#   structure fidelity — 18 -> 21 checks; (M5) S4-1: OMML runs keep the Word math
#   font (Cambria Math italic), EXEMPT from the Arial rule.
#   Verified: 60-question rebuild, 142/142 regions compiled, 21/21 checks, page-
#   for-page structural render match against the source PDF.
# v1.14.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   317 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQPrepare'. The current companion block, the
#   v1.14 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.14 — 2026-07-29 — DI TABLE STRUCTURE, BLOCK COMPOSITION AND CELL CONTENT
#           (GAP-2026-07-29-TBL). This spec could say what a table CONTAINS and never
#           what a table IS. S1-12 CATEGORY 2 transcribed "a list of rows" and S4-3
#           wrote cell.text into a rectangular add_table(), so a grouped header had
#           exactly one representable form: squared into a grid and padded with empty
#           strings. Measured on SSC_CGL_Tier1 09-Sep-2024 Shift 1 — Q.52 and Q.61 each
#           lost a 4-column header span and a 2-row label span and gained 4 stray empty
#           cells, while Q.74 passed because ITS header is flat. That is why the gap
#           survived to v1.13: the worked example in S1-12 and in EC-P20b is flat too,
#           so a model that cannot express a span was never once exercised against one.
#           The delivered Row file carried 0 gridSpan and 0 vMerge elements and passed
#           16/16 checks with a green F2 footer, because no check in this framework has
#           ever compared a built table with its source.
#           SECOND DEFECT, SAME FAMILY: S1-7 and S4-2 emitted one table PER OPTION, and
#           two adjacent w:tbl siblings are FUSED into a single table by every Word
#           engine. Measured: 19 tables as written came back from a Word-engine
#           round-trip as 7. It is invisible in the emitted file — python-docx reports
#           19 — which is why it went unnoticed for the life of the spec.
#           Fix: (1) new S1-8a TABLE STRUCTURE CONTRACT — the TableSpec model, anchor
#           cells with cs/rs, padding BANNED; a blank cell is now distinguishable from
#           padding STRUCTURALLY rather than by heuristic.
#           (2) S4-3 build_di_table DELEGATED to corpus_io (Cluster I) — HTML-style
#           occupancy placement, cell.merge() strictly AFTER text placement (merge
#           CONCATENATES: 'A'+'B' -> 'A\nB'), per-cell column widths, centred default.
#           Two builders modelled one concept and both were flat; one model, one owner.
#           (3) S1-6 and S1-11 scope EXTENDED to table cells — cells now render through
#           render_text_with_math, so a fraction, a superscript or an underlined term
#           inside a DI table is no longer silently flattened. That is the v1.3-v1.6
#           math defect, relocated into tables and unaddressed until now.
#           (4) new S1-8b BLOCK COMPOSITION — no two adjacent block tables; a figure-
#           option SET is ONE table with one row per option, which is also the better
#           match for the ALL-or-NONE rule in S1-7.
#           (5) new S2-2 CALL A2b — text-layer tables are DETECTED and transcribed
#           instead of being parsed as stem prose. S1-12 fires only on embedded images,
#           so a vector-drawn DI table in a FORMAT A source never entered the table
#           protocol at all.
#           (6) new CHECK 17 (geometry equality, declared vs built), CHECK 17b (padding
#           signature, legacy path only), CHECK 18 (no adjacent block tables).
#           16 -> 18 checks.
#           (7) new EC-P24 (table structure, 8 sub-scenarios) and EC-P25 (adjacent
#           block tables). EC-P14 and EC-P20b rewritten; "preserve source data exactly"
#           governed VALUES and was silently read as covering STRUCTURE.
#           (8) an unrepresentable structure is REPORTED, never silently normalised —
#           the EC-V8 / EC-P22 principle extended from images to tables.
#           REQUIRES corpus_io with Cluster I table structure (normalise_table_spec,
#           place_cells, build_di_table, read_table_spec, adjacent_table_pairs) AND the
#           anchor-only _table_rows. Shipping the writer without the reader turns lost
#           geometry into DUPLICATED header text in every consumer: python-docx
#           row.cells returns one entry per GRID COLUMN and repeats the anchor for every
#           covered position. The two halves ship together.
```

## Framework_PYQScan.md

Entries v1.3.1–v1.6.0 moved at framework release 2026.11.06 (EC-P42; v1.6.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQScan.md.

````
# v1.6.0 — 2026-09-14 — GAP-2026-09-14-SCAN-ORPHAN-AT-SOURCE. A classified row
#   could be ORPHANED — its (section, topic, subtopic) absent from
#   scan_progress['taxonomy'] — with no log, no stop, until PYQApprove INV-5 held
#   the run (SSC_CGL_TIER1 Q.13 "Ranking and Position": a rejected new-TOPIC
#   candidate whose already-persisted row was never reconciled; S3-6 Step 5b's
#   fallback no-op'd because the Topic key did not exist, so `available` was []).
#   Six independent orphan sources closed under ONE rulebook:
#   (1) S3-3 step 3b — a rejected discovery candidate is reconciled INTO its
#       persisted row in the same step, ledgered in _meta.rejected_discoveries and
#       REPLAYED on a normalized/near match (same candidate, same answer, every
#       batch and session — INV-6's replay principle applied at scan time).
#   (2) rows carry discovery_status (accepted | resolved_existing; absent = first-
#       pass match; pre-v1.6.0 rows read as legacy). The phantom is_new_discovery
#       field — named in 2f, present in no schema, example, docstring or real row —
#       is retired.
#   (3) SENTINEL RULE — bc.OUT_OF_PATTERN and a retired marker-mode module are
#       ROUTING values, never a persisted `section`; the row carries the resolved
#       path's real section plus pattern_era (the field PYQSort v1.9 carries).
#       PYQApprove has no sentinel handling and HOLDS on such a row.
#   (4) verify_no_orphans() — ONE function, THREE call sites (per paper after 3b;
#       S3-6 before split detection and after reclassify; before every
#       check_convergence call, whose new GATE 5 reads its stamp — S3-6 runs ONCE,
#       so batches scanned after it had no net at all). It compares through
#       reconcile_taxonomy.normalize_label exactly as INV-5 does: a STRING VARIANT
#       is CANONICALISED, never re-filed (Step 5b's and reclassify's raw == sent
#       "letter series" to available[0] — a mis-file INV-5 would have accepted as
#       live); a true orphan is resolved by the S3-3 ladder (Rule 1/Rule 5 inside
#       the topic; the step-3 Q1-Q3 test across the section, ledger-first;
#       promotion through gate_scan_name + add_to_taxonomy). Every repair is in
#       _meta.orphan_repairs; the scan never dead-stops on its own output
#       (GATE-AT-SOURCE rule 2).
#   (5) S3-6 — assign_to_refined_subtopic output is validated ∈ new_subtopics
#       (round-bounded re-derivation, then the ladder — never new_subs[0]); a MERGE
#       is a split record with new_subtopics=[kept]; repair runs before aggregation
#       so Step 4 can never KeyError on a phantom bucket.
#   (6) COMPLETENESS invariant set(classifications) == set(papers_scanned_list) —
#       nothing bound the two files until now, so S3-6 and every gate could judge a
#       PARTIAL row set and PYQApprove could receive two generations. Type-2 input
#       stop naming the file to re-upload; runs on load, before S3-6 and before
#       convergence.
#   (7) the CONVERGED branches and S3-6 now persist classifications.json as well as
#       scan_progress.json — v1.5.0 saved only the latter after refinement, so a split
#       at convergence delivered rows still naming the removed old_subtopic (a
#       fresh-exam INV-5 HOLD with no scan-time cause at all).
#   schema_version stays "2.0" (load_scan_progress and PYQApprove §4 both reject
#   any other value); every new field is additive and read with .get; for a scan
#   with no orphan and no variant, classifications.json and the taxonomy are
#   byte-identical and scan_progress._meta gains only the orphan_gate stamp and
#   two empty ledgers. INV-5 at PYQApprove is unchanged and remains the backstop.
# v1.5.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: crosswalk suppression at scan
# v1.4.0 — 2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION. (F1) S3-1 gains
#   the GENERATION-AWARE TRIPWIRE: a draft carrying spec_generation is re-checked
#   with reconcile_taxonomy.check_topic_density on load — an unmatched finding
#   means the file in project Files is not the file PYQDraft's gate passed
#   (Type-2 stale-input stop naming the file to replace); a draft WITHOUT
#   spec_generation predates the release and gets the one-touch "re-run
#   PYQDraft before scanning" Type-2 stop. S3-6 completion additionally writes
#   post-refinement subtopic totals + ratio into scan_progress._meta
#   (informational telemetry — PYQApprove C4 stays the enforcement point).
#   (F2) scan-created names are GATED AT SOURCE: S3-3 discovery and S3-6 splits
#   run the S2-3 name gates (question shape, catch-all patterns, the
#   min(80, bc.MAX_HEADING_LEN) length bound), plus the C5 near-duplicate check
#   against the receiving Topic's existing subtopics and, for discovered
#   TOPICS, a collision check against syllabus-anchored topic names —
#   self-correcting within the law's rounds; exhaustion writes a finding-keyed
#   amber_status into scan_progress._meta (merged with the draft's at
#   PYQApprove via engine E7).
# v1.3.3 — 2026-08-22 — GAP-1A-STEP7-UNBOUND-NAMES Release B. MIN_PATTERN_SIZE
#   (and its documented pair MIN_QUESTIONS_FOR_SPLIT) hoisted from
#   run_refinement_pass()'s locals to module scope in the same fence:
#   check_dimensional_splits() reads MIN_PATTERN_SIZE and is a module-level
#   function, so EVERY call raised NameError — the refinement pass has never
#   completed on any corpus that reached it with >=15 questions in a subtopic
#   (the GAP-2026-08-16 D5 shape). Values unchanged (15 / 3); behaviour of a
#   successful pass identical. Baseline entry deleted. Release: 2026.08.22.4.
# v1.3.2 — 2026-08-22 — GAP-2026-08-22-SCANROUTE-HEADROOM (editorial; no rule
#   changed). Superseded v1.3 entry moved VERBATIM to SPEC_HISTORY.md (the
#   2026.08.15.14 discipline) — PYQScan-route SPEC-BUDGET headroom, flagged
#   +809 B by the 2026.08.21.4 deploy review. Directory and standing notes stay.
# v1.3.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: era-classification block -> tagged def resolve_era; 1 prose mention to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
````

Entry v1.3 moved at framework release 2026.08.22.2 (EC-P42 — PYQScan-route
headroom, flagged +809 B by the 2026.08.21.4 deploy review). Current-version
entry remains in Framework_PYQScan.md.

```
# v1.3 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: adds a CLASS: T stub for present_files(). NO ARTEFACT CHANGES.
#   It was CALLED from compiling python here while DEFINED nowhere — a guaranteed
#   NameError; spec_name_audit_baseline.json had accepted it as known-unbound in all
#   four affected specs, so the ratchet reported OK.
#   FULL NARRATIVE: SPEC_HISTORY.md + CHANGELOG.md 2026.08.16.2.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQScan.md.

```
# v1.2 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (D5).
#   collect_row_files() was `files = []` … `pass  # Drive MCP calls` … `return files`:
#   it returned an EMPTY LIST unconditionally, on every run of every exam, and its own
#   comment cited "the same pattern as Step 5's S1-2 Drive path" — inheriting a pattern
#   that was itself dead. Invisible to C6 twice over: the `pass` shares its body with
#   other statements so it is not a pass-bodied stub, and it carried no CLASS tag. The
#   listing now delegates to corpus_io.collect_corpus_files over a PHASE A cache keyed
#   by folder id, and an empty result HARD STOPS with a transport diagnosis (EC-P39)
#   instead of silently reporting a Row-file-less exam.
# v1.1 — 2026-08-15 — GAP-2026-08-15-BAREQ. S3-2 Q_PATTERNS mirrors the engine's widened
#   four-entry table (entries 3/4 = BARE-LABEL forms), updated atomically with
#   blueprint_core, PYQSort S3-1 and MockTestAnalyse E-2. S3-2 now PERSISTS q_count and
#   q_count_method into every drive_file_inventory[] entry: the "MANDATORY GATE" computed
#   a check-verified per-file count, displayed it and DISCARDED it, so the one number that
#   would have caught this defect in two seconds (56 parsed vs 60 classified on
#   IIT_JAM_MATHEMATICS 12-Feb-2017) existed, was correct, and was thrown away. NEW S3-3
#   step 1b: assert len(classifications[paper]) == inventory[paper].q_count — HARD STOP on
#   mismatch, WARN when the count came from a filename or the field is absent.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
```

## Framework_PYQSort.md

Entries v1.20.0–v1.21.0 moved at framework release 2026.11.06 (EC-P42; v1.21.1 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_PYQSort.md.

````
# v1.21.0 — 2026-09-02 — GAP-2026-09-01-SYLLABUS-TRANSITION rev 4.5, RELEASE B: syllabus era + OOS labeling
# v1.20.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 2 code islands -> tagged fences (inferred_headings, question_views); 5 prose mentions to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.20.0 — 2026-08-15 — GAP-2026-08-15-BAREQ. S3-1 Q_PATTERNS mirrors the engine's
#   widened four-entry table (entries 3/4 = BARE-LABEL forms). A stem whose whole payload
#   is <m:oMath> reads through p.text as "Q.N", entries 1/2 require whitespace AFTER the
#   digits, and extract_questions() therefore filed the stem, its four options and its
#   date label as BODY of the preceding question: 4 of 60 lost on IIT_JAM_MATHEMATICS
#   12-Feb-2017 with all ten checks GREEN (CHECK 2 counts input and output with the same
#   blind detector; CHECK 5 passes because this step RENUMBERS; CHECK 3 passes because
#   the emitter rebuilds one date label per DETECTED question). NEW S1-3b: reconcile the
#   parsed count against scan_progress.json drive_file_inventory[].q_count — HARD STOP on
#   disagreement, WARN when the field is absent so pre-remedy projects are not stranded.
#   NEW CHECK 12 (HARD FAIL): the question-side twin of CHECK 11 — the <w:t> view and the
#   <w:t>+<m:t> view of the delivered file must agree on every question start. §8 heading
#   corrected from a stale "10 checks" (CHECK 11 was already live) to 12.
````

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQSort.md.

```
# v1.19.0 — 2026-08-05 — GAP-2026-08-05-001. CHECK 11 DOWNSTREAM-PARSE ROUND TRIP added
#   (HARD FAIL, D3/SG-5): PYQSort now re-reads its own delivered file with the DOWNSTREAM
#   predicate and asserts inferred headings == emitted headings, plus the heading-colour
#   styling assertion (SG-10). S6-2 LEVEL 3 parser line amended (SG-9): it mandated
#   11pt Bold Navy #003366 and then told the parser "default -> level 3", i.e. to ignore
#   the marker the same clause guarantees — the root cause of all three heading defects.
# v1.18.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   307 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQSort'. The current companion block, the
#   v1.18 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.18 — 2026-07-27 — THE ORIGINAL EXAM POSITION SURVIVES SORTING (GAP-2026-07-27-E).
#           Step 3 renumbers questions into TAXONOMY order. That is correct and stays —
#           but it destroyed the EXAM position, and nothing downstream could recover it.
#           Step 5's MSQ detector had only the instruction phrase left to work from and
#           measured 24 MSQ across 1,719 questions on an exam whose marking scheme
#           reserves Q31-40 for MSQ (~10/paper, so ~120 in the current era alone).
#           Section B was therefore under-represented corpus-wide, Step 6 under-allocated
#           it and Step 7 under-produced MSQ — surfacing two steps later as unexplained
#           Section B feasibility pressure in MockBlueprint.
#
#           This is the class of defect that CANNOT be fixed where it is observed. The
#           information does not exist by the time Step 5 runs, so Step 5 had nothing to
#           be smarter about. The fix belongs at the point of destruction.
#
#           CHANGE: the date label — rebuilt on every emit, never cloned, and already
#           parsed by Step 5 — now carries a trailing " Q<N>" holding the original
#           position. No new artefact, no new parser, no schema migration.
#             * build_date_label_re(): the Q-part is OPTIONAL, so every sorted file
#               produced before v1.18 still parses BYTE-IDENTICALLY. No exam is forced
#               to re-sort; each gains positional typing when next sorted.
#             * parse_original_q_num(): new. Kept SEPARATE from parse_date_label(),
#               whose 4-tuple return is the sort key and is consumed positionally in
#               several places — widening it would be a silent breaking change.
#             * stamp_original_q_num(): new, IDEMPOTENT, so a re-emit cannot produce
#               "[... Q37 Q37]".
#             * Both DELEGATE to corpus_io Cluster Q (>= v1.9). Step 3 WRITES this stamp
#               and Step 5 READS it — precisely the two-spec shape that produced the
#               is_option drift v1.17 had to unwind, where each file's docstring asserted
#               alignment with the other and both were wrong. One definition in the
#               engine; drift impossible by construction, not asserted by comment.
#           A None result means UNKNOWN — a pre-v1.18 file, or a position no band
#           covers — and callers must never read it as position 0.
#
```

## Framework_ScopedBlueprint.md

Entries v1.8.0–v1.13.0 moved at framework release 2026.11.06 (EC-P42; v1.14.0 supersedes;
GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY — the preamble of every spec is now read by every session, so every header byte is paid).
Current-version entry remains in Framework_ScopedBlueprint.md.

```
# v1.13.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY G05 + OD-10 (paired with
#   blueprint_core v1.30, MockTestCreate v5.90, MockTestAnalyse v2.59.0). (1) S8-2d SHAPE
#   TARGETS: shape_target_per_paper[paper] = bc.shape_targets(shape shares, Q, paper index)
#   — FLOOR for every shape with share x Q >= 1, CAP = round(share x Q) + 2 (owner OD-6 c),
#   series rotation below that — from the in-scope subtopics' QUALITY blocks
#   (bc.quality_block_for_subtopic; first cascade level holding >= bc.SHAPE_MIN_POOL items);
#   {} (dormant, printed) when section_rules carries no QUALITY block. (2) --refresh
#   (bp_refresh, OD-10 a): with an EXISTING blueprint attached, writes ONLY the new fields
#   (shape_target_per_paper, schema_version, producer) for papers AFTER the last registered
#   one and never touches allocations or schedules of registered papers — a series in
#   progress keeps its continuity. (3) blueprint.schema_version = 2.
# v1.12.0 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY L2 + F8 (paired with
#   blueprint_core v1.29, MockTestCreate v5.89). Measured defect: every paper of a delivered
#   Organic scoped series was scheduled 2/14/24 — the exam's PAPER-level mix (not the
#   scope's) run through '+30% harder' and then read in ALPHABETICAL key order (Easy, Hard,
#   Medium); this spec had no 'harder' form and no dict->tuple rule, so a session improvised.
#   §5 S5-P (new, runs whenever a difficulty profile exists): EVERY form is computed by ONE
#   engine call, bc.scoped_difficulty_schedule, on the SCOPE's measured mix
#   (bc.dp_scope_mix: equal-weight over window cycles, empty cycles skipped, cascade
#   scope -> topic -> section -> paper below 20 questions), converted ONLY by bc.mix_to_smh
#   (positional, exam_config.difficulty_labels order). Forms: 'harder' (DEFAULT — owner
#   decision O3, same default as the mock Blueprint since v1.58), 'exam' (now the SCOPE's
#   mix, no longer the paper's), 'S:M:H', 'progressive'. The blueprint records
#   difficulty_source (A-DPROFILE schema + builder + profile hash) so Create S3-2D and the
#   auditor's A-DIFFSRC recompute it. CSIR Organic: 1 Easy / 23 Medium / 16 Hard per 40.
#   No profile -> the v1.5 envelope ramp (§5 Branch A) unchanged. S8-2c (new):
#   fig_ask_target_per_mock from section_rules figural_ask_type_counts (bc.fig_ask_series).
# v1.11.0 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (LAW F1.4 +
#   LAW F3.2; paired with blueprint_core v1.28, figure_types v1.0, final_assembly v1.10,
#   Framework_MockTestCreate v5.88, Framework_Blueprint v1.61.0). TWO DEFECTS, both estate-wide.
#   (1) S8-4 INHERITED the five producer flags (passage/figural/di/multi/nat_present) from
#   exam_config with default False. No step writes those keys, so every scoped blueprint in
#   the estate was born `figural_present: false` — on the reference exam beside 17–18 FIGURAL
#   allocations per paper. Step 7 S13-4 and final_assembly.commit_registry gated the figure
#   record on that flag, so 6 of 21 scoped papers committed NO figure record (no object_types,
#   no figure_specs, no semantic_objects): every figure gate went dormant and every paper
#   audited exit_0/SHIP. FIX: the flags are DERIVED from the scoped allocation through ONE
#   engine rule shared with the mock Blueprint, bc.derive_presence_flags (formats of the
#   allocated subtopics; answer_cardinality / answer_type of the allocated subtopics; the
#   scoped marking_scheme per the S6-MS precedent). exam_config is never consulted for these
#   five keys again; mock_sync_audit MS-22 forbids the idiom from returning.
#   (2) No step asked whether a DOMINANT figure type could be rendered: §6 checked format
#   feasibility (is the section figural-capable?) never TYPE feasibility. NEW S4-5 KIND-
#   COVERAGE PRE-FLIGHT (bc.kind_coverage_preflight over figure_types.FIGURE_TYPES): a
#   dominant type the registry marks UNSUPPORTED (a photograph, a micrograph) HARD STOPs
#   naming subtopic + type, unless exam_config.figure_fallback_policy == 'text_disclosed', in
#   which case the subtopic is allocated TEXT for the series and blueprint.figural_fallbacks
#   records it for the footer; an UNREGISTERED type is an advisory (it renders as a GENERIC
#   schematic; the auditor reports it AMBER) — ~200 legacy exams are never halted by a
#   vocabulary gap. blueprint.figure_type_coverage records the verdict. S8-6 asserts the
#   derived flags; DoD gains item 13.
# v1.10.1 — 2026-09-15 — GAP-2026-09-14-DELIVERY-ECHO Release B (2026.09.15.2; DeliveryFooter v1.35
#   rule R6 / section 9). Delivery site gains the PHASE 1 print of its closed set (S10-1/§3 set unchanged), PHASE 2 echo of the RETURNED paths and PHASE 3 result-built footer. Text only; no set, gate or engine change; never a halt. New DoD item 12 (this spec never named its present_files call).
# v1.10.0 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with blueprint_core Cluster DP,
#   PYQExplain v2.18, MockTestAnalyse v2.55). §1-3 loads the optional difficulty profile
#   (bc.dp_check_profile) instead of section_rules' retired PYQ_DIFFICULTY_CALIBRATION; S5-1
#   observed_levels() reads bc.dp_calibration (rubric-measured bands per subtopic; positional
#   alias to Simple/Medium/Hard); new '--difficulty exam' fixed-uniform form uses the profile's
#   paper-level mix. Default ramp and the S5-2 cascade unchanged. FIX: §1-3 resolves
#   [ExamCode]_exam_config.json (the corpus convention) before the bare name — the bare-only
#   read hard-stopped on every prefixed project.
# v1.9.0 — 2026-08-23 — GAP-2026-08-23-AXIS-ADVISORY-TRUTH (mock S9-12 parity;
#   paired with blueprint_core axis_truth_check + Framework_Blueprint v1.54.0).
#   §6-3 now cross-examines the derived axis_schedule's advisories
#   (axis1_unreachable_formats, guarantee_feasibility) against the in-scope
#   manifest via a first-principles recomputation BEFORE the schedule is stored,
#   and HARD STOPS on any contradiction — a corrupted instrument must not be
#   persisted into blueprint.json, where every downstream reader inherits it
#   silently. Genuine format shortfalls remain flag-and-continue advisories.
# v1.8.1 — 2026-08-23 — GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE follow-through
#   (comment-only; no rule, gate, or output changes). The §6-3 rationale for
#   scoped_manifest_ids still described the PRE-FIX engine ("the engine ... filters ids
#   by manifest[sid]['section'] == section_name") — false since the engine fix shipped
#   with Framework_Blueprint v1.49.0, and exactly the mental model that produces the
#   next instance of the defect class. Rewritten: the view is a retained defensive
#   no-op under the engine's pre-scoped contract, and the raw-join "simplification" is
#   named as the thing the new ENGINE-SECTIONJOIN audit fails the build on.
# v1.8.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   Pipeline listing updated to 6S -> 7 -> 9 -> 11; the one "audited downstream at Step 8"
#   claim is restated against Step 7's audit.py. No allocation rule, gate, or output of
#   this spec changes. ACCEPTED LOSS: a scoped paper now receives no independent audit at
#   any point — Step 7's own gates are terminal for it.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_ScopedBlueprint.md.

```
# v1.7.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   105 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_ScopedBlueprint'. The current companion block, the
#   v1.7 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v1.7 — 2026-07-21 — HARDENING PASS on v1.6 (line-by-line adversarial re-audit, 2 passes,
#   found and fixed 3 real issues before any downstream reliance):
#   (1) ENVELOPE COMPUTATION WAS NOT ACTUALLY GATED — S5-1's prose claimed "S5-1/S5-2 are
#       SKIPPED entirely" under override_mode, but the v1.6 code had `ENVELOPE =
#       scope_envelope()` as an unconditional top-level statement — true only in the sense
#       that Branch B's math never READS ENVELOPE, not that it's never COMPUTED. Fixed:
#       `ENVELOPE = scope_envelope() if not override_mode else None` (S5-2), and merged the
#       former S5-3a/S5-3b into a single S5-3 with an explicit `if override_mode: ... else:
#       ...` — mirroring the mock's own proven S7-5 unified-branch pattern exactly, so there
#       is zero ambiguity about which branch runs and ENVELOPE is never touched in Branch B.
#   (2) STALE DUPLICATE CLAIM IN §10 DoD ITEM 11 — a second, independent occurrence of
#       "difficulty ... from the Step-5 outputs" (absolute, pre-v1.6 wording) survived in the
#       Definition-of-Done checklist even after the same claim was corrected in the
#       EXAM-AGNOSTIC GUARANTEE paragraph at the top of the file. Fixed: item 11 now states
#       difficulty may come from Step-5 outputs OR the trigger override, matching the header.
#   (3) NO CATCH-ALL FOR MALFORMED --difficulty VALUES — S1-1 defined 'progressive', a valid
#       S:M:H ratio, and "neither given", but not a value that is neither (typo, wrong count
#       of numbers, non-numeric). Added an explicit ERROR path naming the accepted formats.
#   Verified: validate_framework_md.py 0 issues (24/24 AST-clean); both S5-3 branches
#   extracted and literally executed against 5 edge cases (uniform override, full-bypass
#   100:0:0, N=1, non-divisible Q rounding, N=200 uniformity, plus a Branch-A ramp regression
#   and single-level-envelope degenerate case) — all assertions held, zero errors. Full
#   before/after SHA256 diff of all 21 OTHER tracked files in the corpus confirmed untouched.
#
```

---

# END OF SPEC_HISTORY v1.0

## Framework_PYQCore.md — texts superseded by v1.7 (GAP-2026-08-30-TYPE1-HALT-ELIMINATION, 2026-08-30)

### S2-3 PROOF OF CORRECT TOPIC COUNT (v1.6 form — the stranded pre-v1.1 absolute rule; RPSC_ZOOLOGY root cause 1)
```
  PROOF OF CORRECT TOPIC COUNT (self-check):
    After Topic derivation, count the Topics per section.
    If a section has ≤ 4 Topics but the syllabus listed 10+ items → Topics
    are over-aggregated. Re-derive. The syllabus items ARE the Topics.
```

### S2-3 GROUPING Arithmetic example (v1.6 form — superseded per DECISION D8: the example produced exactly the 11-items-one-Topic shape the density check rejects)
```
    Example: "Percentage, Ratio, Average, Interest, P&L, Discount,
             Partnership, Mixture, SDT, Time & Work, Pipes & Cisterns"
             → Topic "Arithmetic" with each item as a subtopic.
```

### S2-3 CATCH-ALL PROHIBITION SELF-CHECK (v1.6 form — HARD STOP on Claude's own output, retired per GATE-AT-SOURCE LAW rule 2)
```
    SELF-CHECK: after completing Topic derivation for a section,
    scan all Topic names against the banned patterns. If ANY match
    → HARD STOP. Re-derive those items as individual Topics.
```

### S2-3 NAME-SHAPE SELF-CHECK HARD branch (v1.6 form — same retirement)
```
          if verdict == 'HARD':
              HARD STOP: f"Name-shape violation: '{name[:60]}' — {reason}. "
                         f"Re-extract this item as a proper taxonomy label, not a question."
```

### question_shape_verdict length branch (v1.6 form — bare 80 bound, superseded by min(80, bc.MAX_HEADING_LEN))
```
    if len(n) > 80:
        return ('HARD', f'{len(n)} chars — far longer than any taxonomy label')
```

### STEP 3 ratio guardrail (v1.6 form — dead-stop, retired per GATE-AT-SOURCE LAW rule 2)
```
      ratio > 3.0  → HARD STOP. Print:
        "Taxonomy inflation ratio = [X]× exceeds 3.0× guardrail.
         Over-fragmentation will cause classification failures.
         Re-derive taxonomy with fewer splits."
```

### STEP 3 CATCH-ALL NAME CHECK (v1.6 form — same retirement)
```
    CATCH-ALL NAME CHECK (mandatory):
      Scan ALL Topic and Subtopic names against the banned patterns
      from the CATCH-ALL PROHIBITION rule (above). If ANY match →
      HARD STOP. Re-derive those items as individual named Topics/Subtopics.
      This check runs AFTER all other quality gates.
```

### §12 Phase 0a DoD ratio line (v1.6 form)
```
  ☐ Ratio guardrail passed: total_subtopics / syllabus_entries ≤ 3.0×
```

## Framework_PYQDraft.md — texts superseded by v1.1.0 (GAP-2026-08-30-TYPE1-HALT-ELIMINATION, 2026-08-30)

### S2-3f attempts + operator message (v1.0.1 form — the two-attempt "re-run and report" dead end; halts #7/#8's root, retired per GATE-AT-SOURCE LAW rule 4 in favor of the 3-round constraint-carrying loop with AMBER exhaustion)
```
  ATTEMPT 2 — if it still fails, re-derive that subject's mapping from S2-3.

  AFTER 2 FAILED ATTEMPTS — stop. Do NOT loop, do NOT save a partial draft,
  and do NOT surface the exception. Print the operator message below.

OPERATOR MESSAGE (plain language, closed set — this is the ONLY form in which
this failure may reach the operator):

  "Step 2a could not complete. The syllabus mapping has an issue I could not
   resolve automatically.

   WHAT HAPPENED:
     [one plain line per error, max 5, jargon removed]

   This is a taxonomy build issue, not something you did, and not something
   you need to evaluate.

   YOUR NEXT ACTION (1 step):
   1. Re-run: PYQDraft [ExamCode]
      If it fails again, report the WHAT HAPPENED lines above."

  No traceback. No field names. No stack. No request to judge anything.
```


## Framework_PYQDraft.md — texts superseded by v1.3.1 (GAP-2026-09-05-SYLLABUS-FILENAME-TOLERANCE, 2026-09-05)

### §3.4 NAMING same-date sentence (v1.3.0 form — HS-ST5 owned the ambiguous same-date case; retired per ruling P-1 in favor of the HS-ST12 date-collision stop)
```
and extension must all be present exactly, or HS-ST4; two files carrying
the SAME date in different letter case are still HS-ST5 (ambiguous).
```

### T2 row 7 (v1.3.0 form)
```
  7 | ACTIVE   | >= 2 dated, >= 2 match   | * HS-ST5 (ambiguous CURRENT)
```

## Framework_PYQCore.md — texts superseded by v1.9 (same GAP)

### §3.11 register range citation (v1.8 form)
```
§3.11 register (blueprint_core HS_ST1..HS_ST11 — cited, never restated).
```


## blueprint_core.py — text superseded by R-e within release 2026.09.05.1 (same GAP)

### TRANSITION_DECLARATION_FIELDS (pre-R-e form — names drift-compared)
```
TRANSITION_DECLARATION_FIELDS = (
    'status', 'effective_from', 'reason', 'keys_seen', 'current_file',
    'current_sha256', 'superseded', 'dials', 'zero_history_approved')
```


## Framework_PYQScan.md — texts superseded by v1.6.0 (GAP-2026-09-14-SCAN-ORPHAN-AT-SOURCE, 2026-09-14)

### S3-6 run_refinement_pass Step 5b (v1.5.0 form — the silent no-op; SSC_CGL_TIER1 root cause)
```
    # 5b. Verify no orphaned classifications (v1.7)
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            sub = c['subtopic']
            sec = c['section']
            top = c['topic']
            if sub not in taxonomy.get(sec, {}).get(top, []):
                # Orphaned classification — reclassify missed this question
                # Force-assign to first new subtopic as fallback
                available = taxonomy.get(sec, {}).get(top, [])
                if available:
                    c['subtopic'] = available[0]  # fallback assignment
```

### S3-3 step 2f (v1.5.0 form — the phantom is_new_discovery field)
```
     f. Store classification in [ExamCode]_classifications.json:
        {q_num, section, topic, subtopic, is_new_discovery,
         question_task, question_format, question_direction, thematic_domain}
```

### S3-6 reclassify_after_refinement match + assignment (v1.5.0 form — raw ==, unvalidated output)
```
                if (c['section'] == sec and c['topic'] == top
                        and c['subtopic'] == old_sub):
                    # Claude re-examines the question's metadata and assigns
                    # to the best-fit new subtopic
                    c['subtopic'] = assign_to_refined_subtopic(
                        c, new_subs
                    )
```

## Framework_MockTestOrchestrate.md

Entry v1.0.0 moved at framework release 2026.11.09 (GAP-2026-11-08-DR3-QINDEX-CONFLICT; OD-2026-11-09).

```
# v1.0.0 — 2026-11-06 — GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY (owner decision OD-2026-11-06;
#   paired with Framework_MockTestCreate v5.93 S1-0R, SESSION_BUDGET.json and the bootstrap.py read /
#   retention / staging / worker commands). NEW. How a Step 7 run (MockCreate / TestCreate) is executed
#   so that the specification that writes the paper stays in the context that writes it: the user's
#   chat orchestrates, worker sub-agents execute Framework_MockTestCreate.md, and every read is proved
#   present (READ-RETENTION). No question-writing rule, gate, artefact, deliverable, end state or user
#   action is defined or changed here.
```
