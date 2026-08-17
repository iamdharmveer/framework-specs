# Framework_MockTestAnalyse v2.53.3 — Universal PYQ Pattern Extraction Engine
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
# [ExamCode] project | Step 5 (PYQExtract) | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS (v2.51.0):
#   blueprint_core.py     >= the build carrying partition_by_transport(consumed=)
#                           and channel='direct'. Against an older engine the
#                           consumed= keyword raises TypeError at the plan call —
#                           loud and immediate, which is the correct direction to
#                           fail for a missing dependency.
#   corpus_io.py          >= the build carrying probe_direct_egress(),
#                           fetch_drive_direct() and write_drive_listing().
#                           Absent => AttributeError at PHASE A/A0, before any
#                           paper is touched and before anything is written.
#   Framework_PYQCore.md  >= v1.5 (EC-P40, EC-P41, EC-P42, EC-P43).
#   corpus_io.py          >= v1.9  — MUST carry (a) an IDEMPOTENT build_vision_queue()
#                           that unions with the on-disk queue, and (b) Cluster Q:
#                           parse_original_q_num(), stamp_original_q_num(),
#                           question_type_for_position().
#                           v1.9 is a HARD floor, not a preference. This spec hoists the
#                           Phase A call to the batch boundary; against a v1.8 engine the
#                           hoist still loses every prior SESSION's sheets, because
#                           overwrite-on-write is the engine-side half of the same defect.
#                           Cluster Q absent => AttributeError at the first question,
#                           which is the correct direction to fail for a MISSING
#                           DEPENDENCY (loud, immediate) as against a positional-typing
#                           GAP, which degrades to v2.38 behaviour and never halts.
#   Framework_PYQSort.md  >= v1.18 — writes the original exam position into the date
#                           label. NOT a hard floor: a pre-v1.18 sorted file parses
#                           unchanged and yields positional_type=None, so MSQ detection
#                           falls back to v2.5 instruction-phrase behaviour exactly. No
#                           exam is forced to re-sort; each gains positional typing when
#                           its papers are next sorted.
#
# ═══════════════════════════════════════════════════════════════════════════
# STEP NUMBER NOTE — CANONICAL PIPELINE MAPPING
# This file is Step 5 (PYQExtract) in the canonical 11-step pipeline.
# The changelogs for v2.0-v2.14 (now in SPEC_HISTORY.md) used an internal
# "Step 0/1/2..." shorthand:
#   internal "Step 0" = canonical Step 5  (PYQExtract, THIS file)
#   internal "Step 1" = canonical Step 6  (MockBlueprint)
#   internal "Step 2" = canonical Step 7  (MockCreate)
#   internal "Step 3" = RETIRED (was canonical Step 8, MockCreateAudit — 2026.08.03.5)
#   internal "Step 4" = canonical Step 9  (MockExplain)
#   internal "Step 5" = RETIRED (was canonical Step 10, MockExplainAudit — 2026.08.03.5)
#   internal "Step 6" = canonical Step 11 (MockDeliver)
# Changelogs are preserved as-is (historical). All ACTIVE code, docstrings,
# handoff messages, and documentation now use canonical step numbers exclusively.
# ═══════════════════════════════════════════════════════════════════════════
#
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockTestAnalyse.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.
---

## §1 — SESSION START

No config file required. All parameters are auto-detected from the Exam Pattern
document and PYQ papers. The only inputs are documents the user already has.

### S1-1 — Trigger parsing and ExamCode detection

```
Trigger: PYQExtract  PYQ: <<link>>  [--mode]  [--frequency-scope all|current-era]
Trigger matching is case-insensitive.

ExamCode: alphanumeric + underscore only (e.g. SSC_CGL_TIER1, GATE_CS, IBPS_PO).
  If ExamCode contains invalid chars: flag and ask to correct.

PYQ parameter (REQUIRED for paper-processing modes — v2.24.8, standardized with
Step 4/Step 2b; not needed for --status or --synthesise, which don't read the
PYQ corpus):
  Format : PYQ: <<Google Drive folder URL>>
  Parsing: pyq_drive_folder_id = corpus_io.parse_drive_folder_id(<the PYQ value>)
           THE parser. Do NOT re-implement the regex here — a local copy is the
           drift pattern v2.27/v2.28 removed elsewhere, and the engine version also
           accepts a bare folder id and the /u/N/ account-scoped URL form, which the
           inline regex silently failed on. Returns None when the value is neither.
  Example: PYQ: https://drive.google.com/drive/folders/[YOUR_FOLDER_ID]
             → pyq_drive_folder_id = '[YOUR_FOLDER_ID]'

  If PYQ parameter present    → use Google Drive as source (S1-2 Drive path)
  If PYQ parameter absent AND mode is auto (none) → HARD STOP: "PYQExtract
    requires PYQ: <<Google Drive folder link>>. The local project/uploads
    fallback for PYQ corpus files was removed (v2.24.8)."
  If PYQ parameter absent AND mode is --status/--synthesise → fine, proceed
    (these modes don't re-scan the PYQ corpus).
  If link format unrecognised → flag: "Cannot extract folder ID from link.
                                       Expected: https://drive.google.com/drive/folders/ID"

Mode flags:
  (none)           -> auto-mode: scan Drive folder (PYQ: required), process pending papers
  --status         -> print progress dashboard, then HALT
  --synthesise ALL -> re-synthesise from existing progress.json, skip paper processing
  --synthesise [S] -> synthesise named section only
```

```python

# Parse mode from trigger (extract flag after ExamCode and optional PYQ: param)
# mode is set here and used throughout session-start logic below.
# Examples:
#   "PYQExtract"                        → mode = None
#   "PYQExtract --status"               → mode = '--status'
#   "PYQExtract --synthesise ALL"       → mode = '--synthesise ALL'
#   "PYQExtract PYQ: <<link>>"          → mode = None
mode = None   # set from trigger parsing above; None = auto-mode

# v2.50.0 — bind the other two trigger-parsing outputs explicitly, in the same idiom
# as `mode` above. They were always used below and never bound in inspectable code:
# before the S1-1 fence was split (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION) this
# whole block was invisible to every static check, so nothing could say so.
trigger_text = ''    # the raw trigger line, set from trigger parsing above
exam_config  = None  # loaded from [ExamCode]_exam_config.json below; None = absent

import json, os, re, ast, glob
import blueprint_core as bc      # Cluster H — pure acquisition/image decisions
import corpus_io                 # I/O shell — Drive fetch, image integrity, governor
from collections import Counter
from difflib import SequenceMatcher
import math
from functools import reduce

# ── v2.16 RIGID-1: SESSION KEYWORD FROM exam_config.json ─────────────────────
# The session keyword (Shift/Slot/Phase/Paper/Session) varies by exam.
# PYQSort already reads it from exam_config.json; this file MUST do the same.
# Used to build all shift/session detection regexes dynamically.
# Fallback: 'Shift' when exam_config.json absent or field missing.
#
# exam_config.json examples:
#   "session_keyword": "Shift"     (SSC CGL, SSC CHSL, SSC MTS)
#   "session_keyword": "Slot"      (IBPS PO, IBPS Clerk, SBI PO)
#   "session_keyword": "Phase"     (RRB NTPC, RRB Group D)
#   "session_keyword": "Paper"     (UPSC CSE, UPSC CAPF)
#   "session_keyword": "Session"   (GATE, CAT)

def _read_session_keyword():
    """Read session_keyword from exam_config.json. Fallback: 'Shift'.
    v2.16 SYNC FIX: PYQAnalyse saves the file as {ExamCode}_exam_config.json (with
    prefix), and PYQSort discovers it via glob('*_exam_config.json'). This function
    MUST use the same glob pattern — a fixed path like 'exam_config.json' would miss
    the prefixed file and silently fall through to the 'Shift' default."""
    import glob as _glob
    # Search order: project knowledge (primary), then uploads (fallback)
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        matches = sorted(_glob.glob(os.path.join(search_dir, '*exam_config.json')))
        for cfg_path in matches:
            try:
                with open(cfg_path, encoding='utf-8') as f:
                    cfg = json.load(f)
                return cfg.get('session_keyword', 'Shift')
            except Exception:
                continue
    return 'Shift'

session_keyword = _read_session_keyword()

# ── v2.18: GENERAL EXAM CONFIG READER ──────────────────────────────────────
# Reads marking_scheme[], level, medium, question_types from exam_config.json.
# These are the new fields added by Step 2a v2.5 (standardized xlsx exam pattern).
# Derives marks_per_q (dict, MAX per type) and negative_marking (scalar, mode)
# from marking_scheme[] for backward compatibility with existing PARAMETER code.
# All values have safe defaults when exam_config.json is absent (legacy path).

def _read_exam_config_fields():
    """Read all new exam_config fields. Returns dict with safe defaults.
    Uses same glob pattern as _read_session_keyword for discovery."""
    import glob as _glob
    from collections import Counter as _Counter
    defaults = {
        'marking_scheme': [],
        'level': 'unknown',
        'medium': 'unknown',
        'question_types': ['MCQ'],
        'total_questions': None,
        'time_minutes': None,
    }
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        matches = sorted(_glob.glob(os.path.join(search_dir, '*exam_config.json')))
        for cfg_path in matches:
            try:
                with open(cfg_path, encoding='utf-8') as f:
                    cfg = json.load(f)
                return {
                    'marking_scheme':  cfg.get('marking_scheme', []),
                    'level':           cfg.get('level', 'unknown'),
                    'medium':          cfg.get('medium', 'unknown'),
                    'question_types':  cfg.get('question_types', ['MCQ']),
                    'total_questions': cfg.get('total_questions'),
                    'time_minutes':    cfg.get('time_minutes'),
                }
            except Exception:
                continue
    return defaults

def _derive_marks_per_q(marking_scheme):
    """Derive marks_per_q dict from marking_scheme[].
    Groups ranges by question_type, takes MAX correct_marks per type.
    Returns dict e.g. {'MCQ': 2} or {'MCQ': 2, 'MSQ': 2, 'NAT': 2}.
    Returns {'MCQ': 1} if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return {'MCQ': 1}
    by_type = {}
    for ms in marking_scheme:
        qt = ms.get('question_type', 'MCQ')
        cm = ms.get('correct_marks', 1)
        by_type.setdefault(qt, []).append(cm)
    return {qt: max(marks_list) for qt, marks_list in by_type.items()}

def _derive_negative_marking(marking_scheme):
    """Derive scalar negative_marking from marking_scheme[].
    Returns the most common (mode) negative_marks value across all ranges.
    Returns 0 if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return 0
    from collections import Counter as _Counter
    vals = [ms.get('negative_marks', 0) for ms in marking_scheme]
    return _Counter(vals).most_common(1)[0][0]

def _derive_negative_marking_by_type(marking_scheme):
    """Derive per-type negative_marking dict from marking_scheme[].
    For each question_type, takes MIN (most negative) across all ranges of that type.
    Returns dict e.g. {'MCQ': -0.5, 'MSQ': 0, 'NAT': 0}.
    Returns {} if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return {}
    by_type = {}
    for ms in marking_scheme:
        qt = ms.get('question_type', 'MCQ')
        nm = ms.get('negative_marks', 0)
        by_type.setdefault(qt, []).append(nm)
    return {qt: min(neg_list) for qt, neg_list in by_type.items()}

# Read all fields at session start
_ecfg = _read_exam_config_fields()
marking_scheme = _ecfg['marking_scheme']
level          = _ecfg['level']
medium         = _ecfg['medium']

# Derive backward-compatible PARAMETER values from marking_scheme
# These feed into S1-3 parameter detection as PRIMARY values.
# Legacy AI detection from Exam Pattern doc / PYQ becomes VALIDATION ONLY.
if marking_scheme:
    # exam_config.json present with marking_scheme → authoritative
    _marks_from_config  = _derive_marks_per_q(marking_scheme)
    _neg_from_config    = _derive_negative_marking(marking_scheme)
    _negbt_from_config  = _derive_negative_marking_by_type(marking_scheme)
else:
    # exam_config absent or legacy → PARAMETER detection fills these later
    _marks_from_config  = None
    _neg_from_config    = None
    _negbt_from_config  = None
# ─────────────────────────────────────────────────────────────────────────────

def build_session_re(keyword):
    """Build dynamic regex for session/shift detection from the configurable keyword.
    Matches: <keyword><optional separator><digits>
    e.g. Shift-1, Slot_2, Phase 3, Session1, Paper-1"""
    return re.compile(re.escape(keyword) + r'[-_\s]?(\d+)', re.IGNORECASE)

SESSION_RE = build_session_re(session_keyword)
# ─────────────────────────────────────────────────────────────────────────────
# ── GOOGLE DRIVE — CLASS T TRANSPORT ─────────────────────────────────────────
#
# v2.37 (GAP-2026-07-26-003). These were `pass`-bodied stubs, and line ~6533 passed
# gdrive_download_file DIRECTLY into corpus_io.fetch_drive_docx as its download_fn.
# Executed literally that returns None, decode_drive_payload raises TransportFallback,
# and EVERY paper routes to the upload lane on EVERY run — measured: all 22 papers of
# the reference corpus are under the 10 MiB cap, so none is rejected early and all 22
# would be demanded as manual uploads.
#
# Drive appeared to "work" only because that failure is LOUD: a run with no papers
# produces no output, so the operator or the model is forced to substitute real MCP
# calls out of band. Vision's identical defect was SILENT, so nothing forced anything.
# THE VARIABLE WAS NEVER THE PATTERN — IT WAS THE OBSERVABILITY OF THE FAILURE.
# Both are CLASS T; both now state their contract explicitly.
#
# CLASS: T — these are NOT python functions. They are the NAME of a tool call the
# model performs IN ITS OWN TURN, before run_batch_loop() starts. The model calls the
# Google Drive MCP tool, and the result — a spill-file PATH or an inline payload,
# whichever that deployment produces — is INJECTED into python as a resolver.
# corpus_io.decode_drive_payload() accepts BOTH, plus bytes, a dict, a list, an inner
# JSON string and bare base64, exactly so the bridge never has to know which came
# back; that is the materialise-then-inject bridge, and it is the same bridge S4-2
# uses for vision.
#
# GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION — INVARIANT CORRECTION. This block used to
# assert that the result "for any file of consequence is spilled to a JSON file on
# disk rather than returned inline". MEASURED FALSE on 2026-08-15: one 40,488-byte
# sorted paper spilled to a file in one deployment and came back inline in another,
# and the two spill directories were not the same directory. Delivery form is a
# property of the DEPLOYMENT, not of the file size. Never assume it and never test for
# it by listing a directory — Framework_PYQCount S5-0 measures it on one paper, and
# PYQCore EC-P35/EC-P36 carry the consequences.

def gdrive_search(query, page_size=100, page_token=None):
    """CLASS: T — Google Drive MCP 'search_files'. NOT executable python.

    The model calls Google Drive:search_files(query=..., pageSize=..., pageToken=...)
    in its own turn and materialises the listing before any python runs.
    query format: "parentId = 'FOLDER_ID'". Returns [{id, title, mimeType, fileSize}].
    """
    pass  # CLASS: T — performed by the model between turns, never from python


def gdrive_download_file(file_id, local_path):
    """CLASS: T — Google Drive MCP 'download_file_content'. NOT executable python.

    The model calls Google Drive:download_file_content(fileId=file_id) in its own
    turn. The result is EITHER a spill-file path OR an inline payload — which one is a
    property of the DEPLOYMENT, not of the file size, and it is MEASURED (see
    Framework_PYQCount S5-0), never assumed. Record whatever came back; the resolver
    carries it unchanged and decode_drive_payload accepts both.
    """
    pass  # CLASS: T — performed by the model between turns, never from python


def present_files(paths):
    """CLASS: T — the chat file-delivery tool. NOT executable python.

    GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), DEFECT-CLASS SWEEP.
    §8 calls this twice — once per batch in the status block, once in
    deliver_final — and it was DEFINED nowhere. Five call sites across four specs
    (this file twice, Framework_PYQScan.md run_scan, Framework_PYQExplain.md
    S19-2, Framework_MockTestExplain.md S19-2), each a guaranteed NameError the
    moment that path executes as python.

    SAME SHAPE as D2 of GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, where
    collect_drive_docx_recursive() called the CLASS T marker gdrive_search() from
    python. That gap fixed the INSTANCE and left the CLASS standing for another
    eleven days. P3 rather than P1 only because deliver_final runs AFTER all five
    artefacts are on disk: the run loses its delivery, not its work.

    DECLARED PER-SPEC, deliberately: this corpus's CLASS T house pattern is
    per-file self-containment — gdrive_search and gdrive_download_file are each
    declared in BOTH this file and Framework_PYQCount.md. A pass-bodied marker has
    no logic to drift, and per-file declaration is what keeps spec_name_audit, a
    per-file auditor, able to see the binding at all. The F1/F2 footer contract for
    this primitive remains owned by Framework_DeliveryFooter.md.

    The model performs the call in its own turn, after python returns. Nothing is
    returned to python and NO call site may consume a result (C6).
    """
    pass  # CLASS: T — performed by the model between turns, never from python


# ── THE BRIDGE (this IS the pattern every CLASS T operation must follow) ──────
#
# PHASE A (model, before python):
#     For each paper to fetch, call Google Drive:download_file_content(fileId=...).
#     Note where each result landed — inline payload or spill-file path.
#
# PHASE B (python): pass a RESOLVER that returns the already-materialised payload.
#     A resolver is a plain dict lookup over results that ALREADY EXIST. It performs
#     no tool call, so it is ordinary reachable python:
#
#         drive_payloads = {file_id: payload_or_spill_path, ...}   # from Phase A
#         resolver = lambda fid: drive_payloads[fid]
#         local_path = corpus_io.fetch_drive_docx(resolver, paper_ref, dest_dir)
#
#     NEVER pass gdrive_download_file itself. It is a CLASS T marker, not a callable;
#     passing it is precisely the defect this section documents, and audit_callgraph
#     C6 fails the build if any call site consumes a CLASS T stub's return value.
# ─────────────────────────────────────────────────────────────────────────────


# v2.26 — parse --frequency-scope. Without this the frequency_scope parameter on
# generate_frequency_xlsx()/write_subtopic_manifest() was UNREACHABLE: it existed, defaulted
# to 'all', and no trigger could ever set it. Both callers below must be passed the parsed
# value together with exam_config.
frequency_scope = 'all'
_m_fs = re.search(r'--frequency-scope\s+(all|current-era)', trigger_text or '')
if _m_fs:
    frequency_scope = _m_fs.group(1)
if frequency_scope == 'current-era' and not exam_config:
    raise SystemExit(
        "HARD STOP: --frequency-scope current-era requires exam_config.json. Pattern era is "
        "defined by comparison against the CURRENT pattern; without it no paper's era is "
        "knowable. Supply exam_config.json or drop the flag.")

# Parse ExamCode and PYQ link from trigger
# pyq_drive_folder_id = None  if no PYQ parameter given
# pyq_drive_folder_id = 'ID'  if PYQ: link given and parsed successfully
```

### S1-2 — File inventory

```python
pyq_doc_paths      = []   # list of {source, id, name} for Drive OR {source, path, name} local
exam_pattern_paths = []
analysis_doc_paths = []

# ── GOOGLE DRIVE PATH (when PYQ: link provided in trigger) ────────────────

# v2.35: DELEGATED (audit_callgraph C4). This was a local reimplementation of the
# Drive-URL regex that corpus_io already owns. Two copies of one rule is the drift
# pattern v2.27/v2.28 removed for detect_question_start and slugify. The engine
# version is also strictly more capable: it accepts a BARE folder id and the
# /u/N/ account-scoped URL form, both of which this local copy returned None for —
# a user pasting either got "no PYQ folder" with no explanation.
# (the delegation itself is bound below, beside the listing contract it belongs to)

# ── PHASE A / PHASE B — DRIVE LISTING (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION)
#
# v2.50.0 DELETED collect_drive_docx_recursive(), a 90-line hand-rolled walker that
# carried three defects at once and was invisible to every static check in the repo:
#
#   D1  it read `results.get('items', [])`. The connector returns {'files': [...]}.
#       There is no 'items' key. Measured against the live envelope: the engine
#       returns 22 papers, that line returns []. And an empty corpus is NOT loud in
#       this step — the no-PYQ branch below used to rewrite mode to '--synthesise
#       ALL', so a broken listing became "this exam has no past papers" and Step 5
#       shipped a complete green deliverable of zero-PYQ scaffolds. Steps 6 and 7
#       then generated every question from training knowledge for an exam with 22
#       years of real papers in Drive. THIS STEP CAN PRODUCE A WRONG ANSWER; Step 4
#       could only stall. EC-P39 now forbids that fall-through.
#   D2  it called gdrive_search() — a CLASS T marker — from inside python and
#       consumed the result. Executed literally that is None.get('items'), i.e. an
#       AttributeError caught by the wrapper below and reported as a Drive outage.
#   D4  it had no channel probe, no transport plan and no context budget.
#
# ONE definition of the walk exists, in corpus_io. It paginates to exhaustion,
# recurses newest-first, screens every entry through bc.screen_drive_entry, raises
# DuplicatePaperError on canonical-identity collisions and normalises 'files'/'items'
# /bare-list plus the 'title'/'name' spellings. Never re-implement it here.
DRIVE_LISTING_CACHE = '/home/claude/pyq_drive_listing.json'
DRIVE_WORKDIR       = '/home/claude/pyq_temp'

extract_folder_id = corpus_io.parse_drive_folder_id


def make_drive_list_fn(listing_cache, root_folder_id):
    """PHASE B resolver over the PHASE A listing cache. Performs NO tool call.

    PHASE A (model, in its own turns, BEFORE any python):
        Google Drive:search_files(query="parentId = '<folder_id>'", pageSize=100)
        Paginate to exhaustion and MERGE every page into one {'files': [...]} per
        folder. Recurse into every sub-folder the response reports and cache each
        one under its OWN id. Write the result to DRIVE_LISTING_CACHE verbatim —
        do not reshape the records; normalise_drive_listing owns every shape.

    Cache format — either of:
        {"<folder_id>": {"files": [...]}, "<sub_id>": {"files": [...]}}   # keyed
        {"files": [...]}                                                  # flat root

    WHY KEYED, AND WHY THE FLAT FORM IS SCOPED TO THE ROOT. collect_corpus_files
    recurses: it calls list_fn again with each sub-folder's id. A resolver that
    ignores folder_id and returns the whole cache every time hands the walker the
    SAME entries for the sub-folder, so the sub-folder re-appears inside itself and
    the paper is seen twice — which surfaces as `DuplicatePaperError: two files
    resolve to the same paper identity`, a HARD STOP that blames the operator's Drive
    for a defect in this contract. Measured 2026-08-15 on a one-folder/one-paper
    fixture. The flat form is therefore answered for the ROOT id only; any other id
    resolves to an empty page, which ends the walk cleanly.
    """
    with open(listing_cache, encoding='utf-8') as fh:
        cached = json.load(fh)
    if isinstance(cached, dict) and 'files' in cached:
        cached = {root_folder_id: cached}          # flat cache: root folder only

    def list_fn(folder_id, page_token=None):
        if page_token:
            return {'files': []}                   # PHASE A merged every page already
        return cached.get(folder_id, {'files': []})

    return list_fn


def collect_pyq_papers(folder_id, listing_cache=DRIVE_LISTING_CACHE):
    """Enumerate the PYQ corpus. Returns (papers, rejects) in DRIVE LISTING ORDER.

    Ordering note, and it is load-bearing: this returns listing order, NOT recency
    order. sort_papers_recency_first() owns recency, and on an inline channel the
    transport partition MUST run after that sort — see S8-0 and EC-X21.

    Rejects are ATTACHED, never discarded (v2.29 rule, unchanged). A paper that
    disappears from the corpus with no error is a missing year that nobody notices.
    """
    list_fn = make_drive_list_fn(listing_cache, folder_id)
    papers, rejects = corpus_io.collect_corpus_files(list_fn, folder_id)
    collect_pyq_papers.last_rejects = rejects
    return papers, rejects


_needs_pyq_corpus = not (mode == '--status' or (mode or '').startswith('--synthesise'))

if _needs_pyq_corpus:
    if not pyq_drive_folder_id:
        raise SystemExit(
            "HARD STOP: PYQExtract requires PYQ: <<Google Drive folder link>>. PYQ "
            "papers must be in Google Drive — the local project/uploads fallback for "
            "PYQ .docx corpus files was removed (v2.24.8) to standardize with Step 4 "
            "(PYQCount) and Step 2b (PYQScan). Exam pattern and Analysis documents may "
            "still be provided via project knowledge or chat upload (see below) — only "
            "the PYQ paper corpus itself now requires Drive.")

    try:
        pyq_doc_paths, pyq_rejects = collect_pyq_papers(pyq_drive_folder_id)
        print(f"Google Drive: found {len(pyq_doc_paths)} PYQ .docx file(s)")
        print(f"  Folder ID: {pyq_drive_folder_id}")
        for _r in pyq_rejects:
            print(f"  REJECTED: {_r.get('name')} — {_r.get('reason')}")
    except Exception as e:
        raise SystemExit(
            f"HARD STOP: Google Drive error while listing the PYQ folder: {e}\n"
            f"Fix the Drive link/permissions and retry — there is no local fallback "
            f"for PYQ corpus files (v2.24.8, standardized with Step 4/Step 2b).")
elif pyq_drive_folder_id:
    # v2.24.8: --status / --synthesise don't strictly need the PYQ corpus, but if a
    # PYQ: link was given anyway, honor it — harmless, and useful for --status to
    # report accurate Drive counts. Non-fatal on error since these modes don't
    # depend on it.
    try:
        pyq_doc_paths, pyq_rejects = collect_pyq_papers(pyq_drive_folder_id)
    except Exception as e:
        print(f"NOTE: Google Drive error while listing PYQ folder "
              f"(non-fatal for {mode!r}): {e}")

# ── Exam pattern + Analysis docs always from project/uploads ─────────────
# (these are small files — no Drive needed for them; unaffected by the v2.24.8
#  PYQ-corpus Drive-only standardization — only the raw PYQ .docx corpus was
#  tightened, not these small state/reference documents)

for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
    for f in glob.glob(os.path.join(search_dir, '*')):
        bn  = os.path.basename(f).lower()
        ext = os.path.splitext(bn)[1]
        if 'analysis' in bn or 'analyse' in bn:
            if ext in ('.docx', '.doc') and f not in [x.get('path') for x in analysis_doc_paths]:
                analysis_doc_paths.append({'source': 'local', 'path': f})
        elif any(kw in bn for kw in ('pattern', 'exam_pattern', 'notification')):
            if ext in ('.docx', '.doc', '.pdf', '.jpg', '.jpeg', '.png'):
                if f not in [x.get('path') for x in exam_pattern_paths]:
                    exam_pattern_paths.append({'source': 'local', 'path': f})
        elif ext in ('.jpg', '.jpeg', '.png', '.pdf') and not exam_pattern_paths:
            # v2.24.8: preserved from the old PYQ-corpus fallback loop — a loose
            # image/PDF with no pattern/notification keyword in its name is still
            # accepted as the Exam Pattern doc if nothing else has matched yet.
            # Unrelated to the PYQ-corpus Drive-only change; kept unchanged.
            if f not in [x.get('path') for x in exam_pattern_paths]:
                exam_pattern_paths.append({'source': 'local', 'path': f})

# ── Status print ──────────────────────────────────────────────────────────

analysis_docs_present = bool(analysis_doc_paths)
exam_pattern_present  = bool(exam_pattern_paths)
pyq_available         = bool(pyq_doc_paths)

print(f"Files found:")
print(f"  PYQ papers    : {len(pyq_doc_paths)}  (source: Google Drive)")
print(f"  Exam pattern  : {len(exam_pattern_paths)}")
print(f"  Analysis docs : {len(analysis_doc_paths)}")

# ── EC-P39 — AN EMPTY LISTING IS NOT A ZERO-PYQ EXAM ─────────────────────
# GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. Until v2.50.0 this block rewrote
# mode to '--synthesise ALL' whenever the listing came back empty. That made a
# BROKEN LISTING indistinguishable from a PYQ-less exam — and the listing WAS
# broken (D1, the 'items' key), so the step proceeded to synthesis and shipped a
# complete, green, F2-footered deliverable in which every subtopic was a zero-PYQ
# scaffold. Step 6 blueprinted it and Step 7 generated every question from
# training knowledge, for an exam with 22 years of papers in the Drive folder the
# operator had just supplied.
#
# The operator supplying a PYQ link IS the assertion that papers exist. Zero
# usable papers from a supplied link is therefore a TRANSPORT diagnosis, never a
# corpus fact. A genuinely PYQ-less exam is requested EXPLICITLY with
# '--synthesise ALL'; it is never inferred.
if not pyq_available and not (mode or '').startswith('--synthesise') and mode != '--status':
    raise SystemExit(
        "HARD STOP — the PYQ Drive folder yielded ZERO usable papers (EC-P39).\n"
        f"  folder id      : {pyq_drive_folder_id}\n"
        f"  entries seen   : {len(pyq_doc_paths) + len(pyq_rejects)}\n"
        f"  rejected       : {len(pyq_rejects)}"
        + ("".join(f"\n                     - {r.get('name')}: {r.get('reason')}"
                   for r in pyq_rejects) if pyq_rejects else "")
        + "\n\nThis is NOT treated as a PYQ-less exam and Step 5 will NOT fall through to\n"
          "synthesis: doing so silently produces a deliverable of zero-PYQ scaffolds that\n"
          "Steps 6 and 7 then build an entire paper from training knowledge alone.\n\n"
          "Check, in order:\n"
          "  1. PHASE A ran and DRIVE_LISTING_CACHE holds every page of every folder;\n"
          "  2. the Drive link points at the folder holding the sorted .docx papers;\n"
          "  3. the rejects above — a native Google Doc or legacy .doc is not usable.\n"
          "If this exam GENUINELY has no PYQ corpus, say so explicitly:\n"
          "  PYQExtract --synthesise ALL")

# Load prior progress
progress = load_progress(exam_code)
n_done   = len(progress.get('_meta', {}).get('papers_processed', []))
if n_done:
    n_subs = len([k for k in progress if isinstance(k, tuple)])
    print(f"Resuming: {n_done} papers already processed. {n_subs} subtopics with data.")
```

**Key design decisions:**

- Folder structure is irrelevant — flat, year-subfolders, any nesting → all handled.
- Folder name is irrelevant — "Exam PYQ 2025", "My Papers", "PYQ Docs" → doesn't matter.
- Drive account is irrelevant — any shared folder link works as long as Claude has read access.
- ExamCode and Drive folder are decoupled — same ExamCode can point to different Drive folders
  across different runs (e.g., switching from your Drive to a colleague's Drive).
- Only .docx and .doc files are collected — other file types in the folder are ignored.

### S1-3 — Auto-detect all parameters from Exam Pattern + PYQ papers

No config file. All parameters are derived automatically.

**Sampling rule for PYQ-based detection:**
Where detection reads from PYQ papers, use a sample of one paper per year
from the most recent 3 available years (or all years if fewer than 3 exist).
This ensures detections reflect current exam style, not a single paper's quirks.

```python
# EXECUTION ORDER NOTE:
# All helper functions (sort_papers_recency_first from §8-S8-2,
# extract_year_from_filename from §3-S3-1) are defined in their respective sections.
# Claude loads and defines ALL functions from §2 through §8 before executing any
# session-start logic. This is a spec-reading convention: sections define functions,
# session execution happens after all definitions are loaded.
#
# all_sorted_papers built here using fully-loaded sort function:
all_sorted_papers = sort_papers_recency_first(pyq_doc_paths)  # sort once, use everywhere
```

```python
def get_detection_sample(all_sorted_papers):
    """
    Returns one paper per year from the most recent 3 years.
    all_sorted_papers: already sorted recency-first by sort_papers_recency_first().
    Picks the FIRST paper from each year (= most recent shift of that year).

    Examples:
      [N] papers across multiple years → picks most-recent-year session-1 per year (up to 3 years)
      8 papers from 2021 only     → picks 2021 session-1 (only 1 year available)
      Papers from 2024 and 2025   → picks both (2 years — use all available)
    """
    seen_years = {}
    for paper in all_sorted_papers:
        year = extract_year_from_filename(paper['name'])
        if year and year not in seen_years:
            seen_years[year] = paper
        if len(seen_years) == 3:
            break
    # Return in recency order (most recent year first)
    return [seen_years[y] for y in sorted(seen_years, reverse=True)]

# detection_sample: 1-3 papers, one per most recent year, used for P3/P5/P7/P8
detection_sample = get_detection_sample(all_sorted_papers)
detection_years  = [extract_year_from_filename(p['name']) for p in detection_sample]
print(f"Detection sample: {len(detection_sample)} paper(s) from years {detection_years}")
```

```
PARAMETER 1: time_per_question_sec
  Source: exam_config.json (primary — v2.18) or Exam Pattern document (legacy fallback).
  From exam_config: time_per_q_sec = time_minutes × 60 / total_questions.
  From Exam Pattern doc (legacy): same formula, AI-interpreted duration and Q count.
  Examples (values discovered at runtime from each exam's config):
    SSC CGL T1 (60 min / 100 Qs)     → 36 sec/Q
    GATE Biotech (180 min / 65 Qs)   → 166 sec/Q
    CSIR NET LS (180 min / 145 Qs)   → 74 sec/Q
    IIT JAM Chem (180 min / 60 Qs)   → 180 sec/Q
  If exam_config absent AND exam pattern not uploaded: default 60 sec/Q, document assumption.
  If pattern shows sectional time limits: use shortest section time/Qs
  (most constrained section sets the difficulty pace).

PARAMETER 2: negative_marking
  Source: exam_config.json marking_scheme[] (primary — v2.18) or Exam Pattern doc (legacy).
  From exam_config (v2.18): derive scalar and per-type from marking_scheme[]:
    scalar negative_marking = most common negative_marks across all ranges.
    negative_marking_by_type = for each question_type, take the MIN (most negative)
      value across all ranges of that type. Example:
        GATE marking_scheme: MCQ ranges have -0.33 and -0.66 → {'MCQ': -0.66}.
        MSQ ranges have 0.0 → {'MSQ': 0}. NAT ranges have 0.0 → {'NAT': 0}.
    If all ranges have the same negative_marks → scalar = that value.
    If mixed → scalar = most common value (mode); per-type dict captures full detail.
  From Exam Pattern doc (legacy fallback):
    Detection: scan for '-0.25', '-0.5', '-1', '1/3 mark', 'no negative', 'zero penalty'.
    '-1/4' / '-0.25' / '0.25 marks deducted'  → negative_marking = -0.25
    '-1/3' / '0.33 marks deducted'             → negative_marking = -0.33
    '-1/2' / '-0.5' / '0.5 marks deducted'    → negative_marking = -0.5
    '-1 mark' / 'full mark deducted'           → negative_marking = -1.0
    'no negative marking' / 'zero penalty'     → negative_marking = 0
    Not found in exam pattern                   → negative_marking = 0 (safe default)
  Use: stored in _meta and written to EXAM_STRUCTURE header in section_rules.md.
  NOT used in per-question difficulty scoring (extraction is marking-scheme agnostic).
  Step 7 reads it to know whether wrong answers reduce score (affects strategy).

  v2.5 PER-TYPE MARKING (MSQ contract; dormant until consumed by Step 9 (MockExplain)):
    negative_marking_by_type  dict  Source: Exam Pattern doc. Per question-type penalty,
      e.g. {'MCQ': -0.5, 'MSQ': 0}. MSQ commonly carries NO negative marking even when
      MCQ does. If the pattern gives only a single global value, replicate it for each
      q_type. If MSQ not present → omit the MSQ key. Default {} (fall back to the scalar
      negative_marking above).
    partial_credit  bool  Source: Exam Pattern doc. True if MSQ awards partial marks for a
      partially-correct set (e.g. "+1 per correct option, capped"); False = all-or-nothing.
      Default False. Captured now; consumed by Step 9 (MockExplain) scoring, not Step 5.
    These are detection-only at Step 5 and have NO effect when multi_select_allowed=false.

PARAMETER 3: language
  Source: exam_config.json medium field (primary — v2.18) + detection_sample (validation).
  v2.18 PRIORITY RULE: if exam_config.json contains a 'medium' field (e.g., "English"),
    use it as the authoritative language value:
      "English"    → language = 'english'
      "Hindi"      → language = 'hindi'
      "Bilingual"  → language = 'bilingual'
      other value  → language = medium.lower()
    PYQ auto-detection (below) then VALIDATES: if PYQ-detected language differs from
    the exam_config value, log a WARNING but keep the exam_config value. The exam_config
    xlsx is the authoritative source; PYQ detection catches edge cases.
    If exam_config absent or medium='unknown': fall through to PYQ detection as primary.
  PYQ detection method: for each sample paper, scan all paragraph text of first 30 questions.
          Count ASCII chars vs Indic-script Unicode chars across ALL scripts.
          Compute ratio across ALL sampled questions combined (not per paper).

  v2.16 RIGID-2: expanded from Devanagari-only to ALL major Indic scripts.
  INDIC_RANGES (Unicode block → script):
    U+0900–U+097F  Devanagari  (Hindi, Marathi, Sanskrit, Nepali)
    U+0980–U+09FF  Bengali     (Bengali, Assamese)
    U+0A00–U+0A7F  Gurmukhi    (Punjabi)
    U+0A80–U+0AFF  Gujarati
    U+0B00–U+0B7F  Odia
    U+0B80–U+0BFF  Tamil
    U+0C00–U+0C7F  Telugu
    U+0C80–U+0CFF  Kannada
    U+0D00–U+0D7F  Malayalam

  Detection (exam-agnostic — works for 100+ exams across all Indian languages):
    1. Count: ascii_count, devanagari_count, other_indic_count (all non-Devanagari
       Indic scripts combined), total_alpha.
    2. Compute ratios: ascii_pct, devanagari_pct, other_indic_pct.
    3. Decision:
       If >90% ASCII                           → language = 'english'
       If devanagari_pct > 20% AND other_indic_pct < 5%  → language = 'hindi'
       If other_indic_pct > 20%                → language = 'regional'
         (the specific script is stored in _meta['detected_script'] for downstream use)
       If 10-90% ASCII with any Indic > 10%    → language = 'bilingual'
       Otherwise                               → language = 'english' (safe default)

  The 'regional' value is new in v2.16. Step 7 treats 'regional' the same as
  'hindi' for generation purposes (use training knowledge for the script).
  Rationale: a single paper could be atypical; sampling 3 years gives a
  stable detection even if one year's paper had unusual formatting.

PARAMETER 4: no-PYQ behaviour (mode decision, not a tunable parameter)
  If no PYQ .docx files found → auto-redirect to --synthesise ALL.
  All subtopics written as confidence='absent'. Step 7 uses training knowledge.
  Valid and expected state — not an error.
  If PYQ files present → always presorted; extract_presorted() is sole path.

PARAMETER 5: question_types
  Source: exam_config.json question_types[] (primary — v2.18) + detection_sample (validation).
  From exam_config (v2.18): read question_types list directly. Already validated at
    Step 2a (V8 ensures Overview types match Range tab types). Maps to q_types:
      "MCQ" → 'MCQ'.  "MSQ" → 'MSQ'.  "NAT" → 'integer'.
    multi_select_allowed = ('MSQ' in question_types).
    nat_allowed = ('NAT' in question_types).
  From Exam Pattern doc (legacy fallback):
    MCQ     : default unless pattern says otherwise.
    MSQ     : "Multiple Select" / "select all that apply" / "MSQ" /
              "one or more options may be correct" → add 'MSQ'.
    Integer : "Numerical Answer Type" / "NAT" / "integer type" /
              "enter the answer" → add 'integer'.
  Validation from detection_sample (BOTH paths):
    Scan first 50 questions across ALL sample papers combined.
    If any question has no option labels (stem only, no 1/2/3/4 or A/B/C/D)
    → integer type confirmed (even if not in exam_config/pattern).
    If exam_config AND exam pattern both absent: use PYQ-observed types only. Default ['MCQ'].

PARAMETER 6: marks_per_question
  Source: exam_config.json marking_scheme[] (primary — v2.18) or Exam Pattern doc (legacy).
  From exam_config (v2.18): derive marks_per_q dict from marking_scheme[]:
    Group ranges by question_type. For each type, take MAX correct_marks across ranges.
    Examples:
      SSC CGL T1: 1 range, all MCQ 2m      → {'MCQ': 2}
      CSIR NET LS: 3 ranges, MCQ at 2m/4m  → {'MCQ': 4}   (max)
      GATE BT: MCQ 1m/2m, MSQ 1m/2m, NAT 1m/2m → {'MCQ': 2, 'MSQ': 2, 'NAT': 2}
      CSIR NET Math: MCQ 2m/3m, MSQ 4.75m  → {'MCQ': 3, 'MSQ': 4.75}
    WHY MAX: In sorted PYQ files, original Q-number positions are lost (PYQSort
    renumbers). We cannot look up which marking_scheme range a PYQ question came
    from. Using MAX per type is conservative — it shifts difficulty thresholds up,
    preventing under-classification of high-mark questions as "Simple".
    Step 7 (which generates new questions at known Q positions) uses the full
    marking_scheme[] for exact per-range marks lookup.
  From Exam Pattern doc (legacy fallback):
    "All questions carry 1 mark" / "1 mark each"                → {'MCQ': 1}
    "1 mark for 1-mark / 2 marks for 2-mark questions"          → {'1-mark':1,'2-mark':2}
    "Each correct answer: 2 marks"                              → {'MCQ': 2}
    No marking scheme found → default {'MCQ': 1}, document assumption.
  Affects difficulty threshold scaling in E-9 (higher-mark Qs get higher thresholds).

PARAMETER 7: options_count + option_label_format
  Source: detection_sample (1-3 papers, one per most recent year).
  Method: collect first 30 questions from EACH sample paper. For each question,
          count how many option labels (1./2./3./4. or A./B./C./D.) were found.
          This is a raw count of observed labels — NOT filtered by options_count
          (which is unknown at this stage — we are computing it here).
  Decision (majority vote across all questions combined, ~90 questions):
    If ≥90% of questions have exactly 4 option labels → options_count = 4
    If ≥90% of questions have exactly 3 option labels → options_count = 3
    If mixed or ambiguous                             → options_count = 4 (safe default)
    Note: questions with 0 option labels are skipped (image-only options or NAT).
  Rationale: sampling 3 years catches any format change mid-series.

  option_label_format (v2.15 BUG-D07 — was documented but never implemented):
    ALSO detect the LABEL STYLE from the same sample questions:
      If majority of option lines start with "1." / "2." / "3." / "4."   → '1/2/3/4'
      If majority start with "(1)" / "(2)" / "(3)" / "(4)"              → '(1)/(2)/(3)/(4)'
      If majority start with "A." / "B." / "C." / "D."                  → 'A/B/C/D'
      If majority start with "(A)" / "(B)" / "(C)" / "(D)"              → '(A)/(B)/(C)/(D)'
      If majority start with "(a)" / "(b)" / "(c)" / "(d)"              → '(a)/(b)/(c)/(d)'
      If majority start with "A)" / "B)" / "C)" / "D)"                  → 'A)/B)/C)/D)'
    Default: '1/2/3/4'.
    This is the option LABEL style (how labels are printed), NOT option FORMAT type
    (single_value/sentence_label etc. which describes content shape).
    Stored in _meta and written to EXAM_STRUCTURE. Per-section override derived
    from per-question option_label stored during extraction.

PARAMETER 8: multi_select_allowed
  Source: Exam Pattern document (primary) + detection_sample (confirmation).
  From exam pattern: "Multiple Correct Answers" / "MSQ" / "Select all" → True.
  From detection_sample:
    Scan ALL questions across ALL sample papers (not just first 20).
    If any stem contains "select ALL correct" / "one or more correct"
    / "which of the following are correct" → True.
  Default: False. Only True for exams explicitly supporting MSQ (e.g. GATE).
  Rationale: MSQ questions are rare but consequential — scanning 3 years of
  papers gives much higher confidence than scanning a single paper.

PARAMETER 9: msq_k_mode / msq_k  [v2.5 MSQ contract; only when multi_select_allowed=True]
  Source: Exam Pattern document ONLY.
  WHY NOT FROM PYQ: extraction is answer-key agnostic and PYQ papers carry no key,
  so the NUMBER of correct options (k) is unextractable from PYQ. It must come from
  the exam pattern. Step 5 can detect THAT a question is MSQ (from option shape +
  stem), but not k. This is a documented, intentional limitation.
  Detection from exam pattern:
    "select TWO" / "exactly two correct" / "choose 2"   → msq_k_mode='fixed', msq_k=2
    "select THREE" / "exactly three correct"            → msq_k_mode='fixed', msq_k=3
    "one or more correct" / "select all that apply"     → msq_k_mode='variable', msq_k=None
    Not specified but multi_select_allowed=True          → msq_k_mode='variable' (default)
  Constraint passed to Step 7: correct set S ⊆ {1..options_count} with
    1 ≤ |S| ≤ options_count−1 (variable), or |S| = msq_k (fixed). k=0 and k=n forbidden.
  Default when multi_select_allowed=False: msq_k_mode='n/a' (path inert).

PARAMETER 10: msq_allow_aota  [v2.5 MSQ contract, D5; only meaningful when multi_select_allowed=True]
  Source: Exam Pattern document; default False.
  Policy flag controlling whether an "All of the above" option is permitted under
  multi-select. Under MSQ, AOTA is self-contradictory (it cannot coexist with
  individually selectable correct options), so it is REJECTED by default. An exam whose
  pattern explicitly sanctions AOTA-style options in multi-select sets this True.
  Detection from exam pattern:
    explicit "All of the above permitted / allowed in multi-select" → msq_allow_aota=True
    anything else (incl. silent)                                    → msq_allow_aota=False
  Written into EXAM_STRUCTURE so Step 7 (R-MSQ-ESCAPE / G-MSQ-SET) and Step 3
  (A-MSQ-KEY) read it directly from section_rules. "None of these" is unaffected — it
  stays an ordinary selectable option in either case. Default when
  multi_select_allowed=False: False (path inert).
  msq_instruction / msq_instruction_hi  [v2.9 — parametric, localised; D8]:
    The candidate-facing select-instruction Step 7 places inside the Q.N stem line (R14)
    for a multi-select question, e.g. "(One or more options may be correct)" / "(Select
    TWO)", and Step 8 (A-MSQ-INSTR) verifies. The EXACT MSQ analogue of nat_instruction
    (PARAMETER 11) — referenced there as the model. Parenthesised so it reads as an in-stem
    instruction. Default text supplied below; an exam may override from its pattern, and the
    _hi variant carries the Hindi/bilingual phrasing (per PARAMETER 3). Before v2.9 no
    producer emitted this and Step 7/8 silently used a hardcoded fallback (a contract-sync
    gap closed here); now authoritative + overridable, symmetric with NAT.
      Default: msq_instruction    = '(One or more options may be correct)'
               msq_instruction_hi = '(एक या अधिक विकल्प सही हो सकते हैं)'
      If msq_k_mode=='fixed' with msq_k=K, an exam may instead phrase it "(Select K)" /
      localized. Default when multi_select_allowed=False: defaults still written but inert.

PARAMETER 11: nat_allowed + NAT config  [v2.8 NAT contract; only when nat_allowed=True]
  Source: Exam Pattern document (primary) + detection_sample (confirmation).
  nat_allowed (the capability gate — analogous to multi_select_allowed for MSQ):
    Derived primarily from PARAMETER 5 q_types: nat_allowed = ('integer' in q_types).
    Reinforced from exam pattern: "Numerical Answer Type" / "NAT" / "fill in the value"
    / "enter the answer" present → True. From detection_sample: any question with ZERO
    selectable options (no text option labels AND no option-images — image_role is none or
    stem_only, never options_only/stem_and_options) confirms NAT.
    Default: False. Only True for exams that explicitly use numerical-entry questions
    (e.g. GATE, JEE). When False, the entire NAT path is inert (answer_type is always
    'option', so non-NAT exams are behaviourally identical to v2.7).
  WHY NOT k-style PYQ extraction: as with msq_k, the ACCEPTED VALUE and its TOLERANCE are
    answer-key information; PYQ papers carry no key, so a NAT question's value/tolerance are
    unextractable from PYQ. Step 5 detects THAT a subtopic is numerical (0-option shape),
    but the answer model below must come from the exam pattern. Documented limitation.
  nat_answer_type ∈ {integer, real}  [only when nat_allowed=True]:
    From exam pattern:
      "answer is an integer" / "integer type" / "no decimals"        → 'integer'
      "up to N decimal places" / "rounded to" / "real value" / "±"   → 'real'
      nat_allowed but unspecified                                    → 'real' (default;
        GATE-style NAT commonly permits a decimal value with a tolerance band)
    integer ⇒ exact match (no tolerance band); real ⇒ value within nat_tolerance.
  nat_tolerance  [only when nat_answer_type=='real']:
    From exam pattern ONLY (e.g. "± 0.01", "accept 46.5 to 47.5", "2 decimal places").
    Encoded as an absolute delta (float) or a percentage string ("1%"). Becomes Step 9's
    ca_range=(value−tol, value+tol). Default when unspecified: '0' (treat as exact to the
    displayed precision — never invent a tolerance). integer ⇒ always '0'.
  nat_instruction  [parametric, localised]:
    The candidate-facing instruction Step 7 places inside the Q.N stem line (R14), e.g.
    "Enter your answer as a numerical value." (Hindi/bilingual per PARAMETER 3). Default
    text supplied; an exam may override from its pattern. Mirrors the MSQ instruction.
  NAT marking: per-type penalty lives in negative_marking_by_type (PARAMETER 2) under the
    'NAT' key (NAT is usually 0 negative marking). Additive — no new field. Default absent
    ⇒ falls back to the generic negative_marking.
```

Auto-detection confirmation printed before processing:

```
"=== Auto-detected parameters ===
 Session keyword  : [session_keyword] (from: exam_config.json | default 'Shift')
 Detection sample : [year1] [session_keyword]-[N], [year2] [session_keyword]-[N], ...
                    ([N] paper(s) sampled from [N] most recent year(s))
 Time/Q           : [N] sec  (from: [exam pattern | default 60])
 Language         : [english | hindi | regional | bilingual]  (from: 3-year PYQ sample)
 Q-types          : [MCQ | MCQ+MSQ | MCQ+integer]  (from: [exam pattern | PYQ | default])
 Marks/Q          : [dict]  (from: [exam pattern | default {'MCQ':1}])
 Options/Q        : [N]  (observed from: [N] papers across [N] years)
 Multi-select     : [yes | no]  (from: [exam pattern | PYQ sample | default no])
 MSQ k-mode       : [fixed k=N | variable | n/a]  (printed only when multi-select=yes)
 MSQ AOTA         : [allowed | rejected (default)]  (printed only when multi-select=yes)
 MSQ marking      : [neg-by-type | partial=yes/no]  (printed only when multi-select=yes)
 NAT type         : [integer | real (default) | n/a]  (printed only when nat-allowed=yes)
 NAT tolerance    : [± value | exact]  (printed only when nat-allowed=yes)
 Note: presorted = always true (all PYQ files pre-sorted by subtopic heading)
================================="
```

If any detection is ambiguous across sampled papers (e.g., options_count=4 in 2025
but options_count=3 in 2023), Claude reports the conflict explicitly:
  "options_count conflict across years: 2025=4, 2023=3 → using 4 (most recent year wins)"
Most-recent-year always wins for conflicting detections.
Claude does NOT ask the user to resolve conflicts — it decides and proceeds.

### S1-3a — Config-derived parameter overrides (NEW v2.18)

When exam_config.json is present with marking_scheme[] (Step 2a v2.5+), the
config-derived values OVERRIDE AI-detected values for PARAMETERs 1, 2, 3, 5, 6.
AI detection from PYQ becomes validation only (warn on conflict, config wins).

```python
# v2.18: Override AI-detected parameters with exam_config values when available.
# _ecfg, marking_scheme, level, medium, _marks_from_config, _neg_from_config,
# _negbt_from_config are all set at session start (above _read_exam_config_fields).
# Gate: marking_scheme non-empty means exam_config v2.5 is present → authoritative.
# When marking_scheme is empty, exam_config is absent or legacy → no override.

# PARAMETER 1: time_per_q_sec — prefer exam_config.time_minutes / total_questions
if _ecfg.get('time_minutes') and _ecfg.get('total_questions'):
    config_time_per_q = round(_ecfg['time_minutes'] * 60 / _ecfg['total_questions'])
    if time_per_q != config_time_per_q:
        print(f"NOTE: time_per_q overridden by exam_config: {time_per_q} → {config_time_per_q}")
    time_per_q = config_time_per_q

# PARAMETER 2: negative_marking — prefer marking_scheme-derived value
if _neg_from_config is not None:
    if negative_marking != _neg_from_config:
        print(f"NOTE: negative_marking overridden by exam_config: {negative_marking} → {_neg_from_config}")
    negative_marking = _neg_from_config
if _negbt_from_config is not None:
    negative_marking_by_type = _negbt_from_config

# PARAMETER 3: language — prefer medium from exam_config
if medium and medium.lower() != 'unknown':
    config_lang = medium.lower()
    if config_lang in ('english', 'hindi', 'bilingual'):
        if language != config_lang:
            print(f"NOTE: language overridden by exam_config medium: {language} → {config_lang}")
        language = config_lang

# PARAMETER 5: question_types — prefer exam_config.question_types
# Gate on marking_scheme to distinguish v2.5 exam_config (authoritative) from
# legacy/absent exam_config (default ['MCQ'] — should NOT suppress PYQ detection).
# When exam_config v2.5 says ['MCQ'] only, it is AUTHORITATIVE — PYQ-detected NAT/MSQ
# must be ignored (the exam genuinely has only MCQ). A warning is logged so the user
# can correct the exam_config xlsx if the PYQ detection was correct.
if marking_scheme and _ecfg.get('question_types'):
    config_q_types = set()
    for qt in _ecfg['question_types']:
        if qt == 'NAT':
            config_q_types.add('integer')
        else:
            config_q_types.add(qt)
    if set(q_types) != config_q_types:
        print(f"WARN: q_types overridden by exam_config: PYQ detected {q_types}, "
              f"exam_config says {sorted(config_q_types)}. If PYQ detection was correct, "
              f"update the exam pattern xlsx Question Type field.")
    q_types = sorted(config_q_types)
    multi_select = 'MSQ' in _ecfg['question_types']
    # nat_allowed must also be updated (consumed by S1-3b and downstream)
    nat_allowed_override = 'NAT' in _ecfg['question_types']

# PARAMETER 6: marks_per_q — prefer marking_scheme-derived MAX per type
if _marks_from_config is not None:
    if marks_per_q != _marks_from_config:
        print(f"NOTE: marks_per_q overridden by exam_config: {marks_per_q} → {_marks_from_config}")
    marks_per_q = _marks_from_config
```

### S1-3b — Store auto-detected params in _meta (NEW v2.3)

After S1-3 completes detection, store all detected params in `progress['_meta']`.
These are later retrieved by `run_synthesise` and passed to `write_section_rules`
as `exam_meta` so the EXAM_STRUCTURE header block can be written to section_rules.md.

```python
# Store auto-detected exam parameters in progress _meta immediately after S1-3.
# Keys must match what write_section_rules() expects in exam_meta dict.
progress.setdefault('_meta', {}).update({
    'time_per_q_sec'       : time_per_q,          # int (seconds)
    'language'             : language,             # 'english'|'hindi'|'regional'|'bilingual'
    'session_keyword'      : session_keyword,      # v2.16 RIGID-1: 'Shift'|'Slot'|'Phase'|etc.
    'q_types'              : list(q_types),        # e.g. ['MCQ'] or ['MCQ','MSQ']
    'marks_per_q'          : marks_per_q,          # dict e.g. {'MCQ':1} (derived from marking_scheme)
    'negative_marking'     : negative_marking,     # float e.g. -0.5 or 0 (summary scalar)
    'options_count'        : options_count,        # int e.g. 4
    'multi_select_allowed' : multi_select,         # bool
    # v2.18: new fields from exam_config.json (Step 2a v2.5 contract).
    # marking_scheme is the per-range source of truth; marks_per_q and negative_marking
    # above are derived summaries for backward compatibility.
    'marking_scheme'       : marking_scheme,       # list of {q_range, question_type, correct_marks, negative_marks}
    'level'                : level,                # 'Graduation'|'Post Graduation'|etc.
    'medium'               : medium,               # 'English'|'Hindi'|'Bilingual'|etc.
    # v2.5 MSQ contract (dormant unless multi_select_allowed). PARAMETER 9 + per-type marking.
    'msq_k_mode'              : msq_k_mode,         # 'fixed'|'variable'|'n/a'
    'msq_k'                   : msq_k,              # int|None
    'msq_allow_aota'          : msq_allow_aota,     # v2.5 D5: bool (default False) — permit
                                                   #   "All of the above" under MSQ
    # v2.9 (contract-sync fix): localized MSQ select-instruction, the MSQ analogue of
    # nat_instruction. Parametric, localised; default supplied, an exam may override from
    # its pattern. Consumed by Step 7/8 from section_rules. _hi = Hindi/bilingual variant.
    'msq_instruction'         : msq_instruction,    # localised; default '(One or more options may be correct)'
    'msq_instruction_hi'      : msq_instruction_hi, # Hindi/bilingual variant
    'negative_marking_by_type': negative_marking_by_type,  # dict e.g. {'MCQ':-0.5,'MSQ':0}
    'partial_credit'          : partial_credit,    # bool
    # v2.8 NAT contract (dormant unless nat_allowed). PARAMETER 11. nat_allowed gates the
    # per-subtopic answer_type detection; the answer model comes from the exam pattern.
    'nat_allowed'             : ('integer' in q_types),   # bool — capability gate
    'nat_answer_type'         : nat_answer_type,   # 'integer'|'real' (default 'real')
    'nat_tolerance'           : nat_tolerance,     # abs float or '%' string; '0' = exact
    'nat_instruction'         : nat_instruction,   # parametric, localised (PARAMETER 3)
    # v2.15 BUG-D07: option_label_format now auto-detected from PYQ option lines
    # during PARAMETER 7 detection. The label style ('1/2/3/4' vs 'A/B/C/D') is
    # distinct from option FORMAT type ('single_value'). Stored here; written to
    # EXAM_STRUCTURE. Per-section override derived during synthesis from per-question
    # option_label fields stored during extraction.
    'option_label_format'     : option_label_format,  # '1/2/3/4' | 'A/B/C/D' | etc.
})
# Note: papers_analysed, questions_analysed, years_covered are updated
# incrementally in _meta['papers_processed'] and _meta['total_questions']
# and _meta['years_processed'] during each paper processing call.
```

### S1-3c — §1-6 Minimum year coverage check (runs at session start)

```python
# Run immediately after file inventory (S1-2) — before any paper processing.
# Determines coverage_mode, recent_5_years, available_years for this session.
# These three variables are passed to run_batch_loop() and run_synthesise().
#
# ★ CRITICAL: 5-year minimum is MANDATORY when PYQ papers are available.
# ★ This check cannot be bypassed by any user instruction or argument.

def compute_coverage_mode(pyq_doc_paths):
    """
    §1-6 check: compute minimum year coverage requirements for this exam.
    Returns: (coverage_mode, recent_5_years, available_years)
    MANDATORY: cover as many recent years as available, with a minimum of
min_pyq_years (default: 5, read from project configuration or trigger parameter).
If fewer years are available (new exam, limited PYQ history): process ALL available years.
The 5-year default is a quality floor — not a rigid rule that blocks generation when fewer exist.
    """
    # Extract years from all available paper filenames, filter out None
    all_years_raw  = [extract_year_from_filename(p['name']) for p in pyq_doc_paths]
    all_years_clean = sorted(set(y for y in all_years_raw if y is not None), reverse=True)

    if not all_years_clean:
        # No year detectable from filenames (e.g. "GATE_Paper_Set1.docx")
        # Cannot enforce year-based coverage. Use a passthrough mode.
        print("WARN: No years detectable from PYQ filenames. Year coverage check disabled.")
        return 'no_year_info', [], []

    available_years  = all_years_clean                    # descending: [2025, 2024, 2023, ...]
    n_required_years = min(5, len(available_years))      # cap at actual number of years available
    recent_5_years   = available_years[:n_required_years] # most recent N years (up to 5)
    coverage_mode    = 'mandatory_5yr'                    # single mode — always 5 years

    print(f"★ MANDATORY 5-YEAR COVERAGE RULE ACTIVE ★")
    print(f"Coverage mode  : {coverage_mode}")
    print(f"Available years: {available_years}")
    print(f"Required years : {recent_5_years} ({n_required_years} year(s) must be processed)")
    return coverage_mode, recent_5_years, available_years

# Scenario B (no PYQ): skip coverage check entirely
if pyq_available:
    coverage_mode, recent_5_years, available_years = compute_coverage_mode(pyq_doc_paths)
else:
    # Scenario B — no PYQ files. §1-6 does not apply (see §1-6 note).
    coverage_mode, recent_5_years, available_years = 'no_pyq', [], []
```

### S1-4 — Load subtopic taxonomy

```
CROSS-STEP SUBTOPIC NAME RULE (applies to Step 5 and Step 6 both):
  Step 5 (PYQExtract) and Step 6 (MockBlueprint) both read subtopic
  names from the SAME Analysis Word docs. Both steps MUST use the EXACT names
  as written in the Analysis doc — the names seed the SAME taxonomy triples
  both steps derive subtopic_ids from, so a divergent spelling here mints a
  DIVERGENT id downstream, and ids are the only join key that matters.
  v2.47 (GAP-2026-08-13-STALE-NAME-MATCH-RULE — cross-step sync audit): this
  rule previously claimed "Step 7 matches subtopics by EXACT name between
  section_rules.md and blueprint.json" and prescribed re-running BOTH Step 5
  AND Step 6 on any rename. That has been FALSE since MockTestCreate v3.4:
  Step 7 joins on subtopic_id ONLY (its SUBTOPIC_ID CONTRACT section: "v3.4
  removes string-matching entirely... The display name is decorative;
  nothing matches on it") —
  exactly what this file's own §15 SUBTOPIC_ID CONTRACT says (Step 5 mints,
  Step 6 consumes, Step 7 joins by id). A display-name-only correction that
  does NOT change the derived slug/id needs NO re-runs; a correction that
  DOES change the triple (and therefore the id) still requires re-running
  Step 5 AND Step 6 together, because a manifest/blueprint id mismatch is a
  Step-7 HARD STOP (HS-9/HS-11), never a silent no-allocation.
```

```python
def extract_taxonomy_from_analysis_doc(doc_path, taxonomy, renames=None):
    """Populate taxonomy {section: [{'topic','subtopic'}]} from the Analysis doc.

    v2.30 (GAP-2026-07-25-002) — DELEGATED. The previous implementation returned
    ZERO subtopics from a real Analysis doc, on every exam, and had done so since
    it was written. Two independent reasons, both verified by executing it against
    the first exam's live doc:
      (1) it iterated doc.paragraphs, while EVERY subtopic in the Analysis doc
          lives in a TABLE;
      (2) it keyed hierarchy off Word Heading 1/2/3 styles and left_indent, and the
          generator emits neither — para.style is None for every paragraph of a
          real doc, so those branches are unreachable.
    It also carried the same `not cur_sec` first-value latch as the P0 in
    Framework_PYQSort S1-2, and on a styled doc reported 12 phantom sections by
    reading the title line AND the "Subject:" line as level 1.
    Net effect: Source 2 of the v2.20 taxonomy sync — the safety net that mints ids
    for zero-PYQ subtopics — has never contributed a single tuple.

    corpus_io Cluster K is now THE reader for this artefact. Signature and
    in-place-mutation contract are unchanged, so callers are untouched.

    v2.31 — THE LOCK GATE. Reading the doc proved it agreed with ITSELF and never
    that it was the doc PYQApprove APPROVED. Step 5 mints the subtopic_ids every
    later step matches on, so a superseded Analysis doc here does not degrade the
    run — it silently renames the vocabulary of the whole pipeline.

    v2.39 — THE MERGE IS NOW A MERGE (GAP-2026-07-27-A). What stood here was a bare
    .append() into a bucket that Source 1 had already filled, so the stated contract
    — "merged, Analysis docs win for names" — held in NEITHER half: it concatenated
    rather than merged, and it never won a name because it never replaced anything.
    Measured on IIT_JAM_BIOTECHNOLOGY: section_rules.md carried 260 subtopic blocks
    for 134 distinct ids; 126 ids were emitted TWICE (the 8 singletons are zero-PYQ
    scaffolds, which enter through the guarded path). mint_subtopic_ids() cannot
    recover, because its `_2` disambiguator fires only when the KEY differs:
        while sid in seen and seen[sid] != key:   # identical key -> never entered
    so both copies took the same id and QV-13 correctly refused the run.

    The 126 duplicate blocks were verified byte-identical, so no downstream artefact
    carried WRONG data — but the step could not pass its own DoD, and section_rules.md
    shipped at twice its true size.

    RENAME CONTRACT (decision (a), 2026-07-27). The doc wins the topic name, AND the
    rename is propagated to the progress keys by the caller. This is not optional
    bookkeeping: run_synthesise looks questions up with
        key = (section, e['topic'], e['subtopic'])
    so a topic renamed HERE and not re-keyed THERE turns every PYQ-evidenced subtopic
    whose topic the doc spells differently into a silent zero-PYQ scaffold — all its
    evidence dropped, no error raised. That would convert a loud, correctly-detected
    QV-13 failure into exactly the silent data loss this gap wave exists to remove.
    Renames are therefore RECORDED here and APPLIED to progress by the caller, in the
    same pass, via apply_taxonomy_renames().
    """
    import corpus_io
    actual_path = doc_path['path'] if isinstance(doc_path, dict) else doc_path
    try:
        doc = corpus_io.load_taxonomy(path=actual_path, step='PYQExtract')
    except corpus_io.AnalysisDocError as ex:
        raise RuntimeError(str(ex))
    for section, topic, subtopic in doc['triples']:
        bucket = taxonomy.setdefault(section, [])
        hit = next((e for e in bucket if e['subtopic'] == subtopic), None)
        if hit is None:
            bucket.append({'topic': topic, 'subtopic': subtopic})
        elif hit['topic'] != topic:
            # Doc wins the name. Record so the caller can re-key progress.
            if renames is not None:
                renames.append((section, hit['topic'], topic, subtopic))
            hit['topic'] = topic


def apply_taxonomy_renames(progress, renames):
    """Re-key progress so a topic rename accepted from the Analysis doc keeps its data.

    v2.39 (GAP-2026-07-27-A, decision (a)). extract_taxonomy_from_analysis_doc lets the
    Analysis doc win the topic name. The progress dict is keyed by the OLD name, and
    run_synthesise's lookup key includes topic — so without this pass the rename
    silently orphans every question under the renamed topic.

    Merges rather than clobbers when both keys exist (two source topics collapsing onto
    one doc topic is legitimate), and is a no-op when renames is empty, which is the
    overwhelmingly common case.

    Returns a log of what moved, for the audit trail.
    """
    log = []
    for section, old_topic, new_topic, subtopic in (renames or []):
        old_key = (section, old_topic, subtopic)
        new_key = (section, new_topic, subtopic)
        if old_key == new_key or old_key not in progress:
            continue
        moved = progress.pop(old_key)
        if new_key in progress:
            progress[new_key].extend(moved)
            log.append(f"  RENAME+MERGE: {old_key} -> {new_key} ({len(moved)} Qs merged)")
        else:
            progress[new_key] = moved
            log.append(f"  RENAME: {old_key} -> {new_key} ({len(moved)} Qs carried)")
    return log


def _dedupe_analysis_docs(paths):
    """Collapse the SAME Analysis doc reached by two routes into one entry.

    v2.39 (GAP-2026-07-27-A, edge cases 1 and 2). The synthesis glob searches BOTH
    /mnt/project/ and /mnt/user-data/uploads/, and the documented operator workflow is
    "download the output, re-upload it to project knowledge" — so the same doc routinely
    sits in both, which multiplies every overlapping subtopic a THIRD time. A superseded
    copy saved as "..._PYQ_Analysis (1).docx" multiplies it again.

    Identity is realpath first (same file, two routes), then SHA-256 of content (two
    routes, two inodes, same bytes). Distinct content is NOT collapsed here — two
    genuinely different Analysis docs are an operator error that the v2.31 lock gate
    must adjudicate, not something this function may silently pick a winner for.
    """
    import hashlib
    seen_real, seen_hash, keep = set(), set(), []
    for p in sorted(paths):
        try:
            rp = os.path.realpath(p)
            if rp in seen_real:
                continue
            with open(p, 'rb') as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            if h in seen_hash:
                continue
            seen_real.add(rp); seen_hash.add(h); keep.append(p)
        except OSError:
            continue
    return keep

taxonomy = {}
if analysis_docs_present:
    # v2.39 (GAP-2026-07-27-A). SECOND call site of the same defect. The gap report
    # cited only run_synthesise; this one multiplies identically and prints the result
    # to the operator as the verified subtopic count in the S1-5 summary — so before
    # v2.39 the number the operator was asked to trust was itself inflated.
    # _dedupe_analysis_docs collapses the same doc reached by two routes; the merge
    # inside extract_taxonomy_from_analysis_doc collapses the rest.
    for doc_path in _dedupe_analysis_docs(analysis_doc_paths):
        extract_taxonomy_from_analysis_doc(doc_path, taxonomy)
    total = sum(len(v) for v in taxonomy.values())
    print(f"Taxonomy: {total} subtopics, {len(taxonomy)} sections")
elif pyq_available:
    # Presorted PYQ papers carry their own taxonomy headings.
    # Taxonomy will be built incrementally from docx headings during E-1.
    print("Taxonomy built from PYQ docx headings during extraction")
else:
    # No PYQ and no Analysis docs: cannot build taxonomy.
    # Synthesis will produce empty section_rules.md — warn user.
    print("WARN: No Analysis docs and no PYQ files found.\n"
          "section_rules.md will be empty. Upload Analysis docs to get absent entries.")
```

### S1-5 — Verification summary

```
"=== PYQExtract: [ExamCode] ===
 Mode            : [auto|synthesise|status]
 PYQ source      : [Google Drive (folder: [ID]) | project/uploads]
 PYQ files       : [N] total  ([N] done, [N] pending)
 Session keyword : [session_keyword] (from: exam_config.json | default 'Shift')
 Detection sample: [year1] [session_keyword]-[N], [year2] [session_keyword]-[N], ...
 Exam pattern    : [found | not found — time/Q defaulted to 60 sec]
 Analysis docs   : [N] docx
 ── Auto-detected ──────────────────────────────────────
 Time/Q          : [N] sec  (from: [exam pattern | default 60])
 Language        : [english|hindi|regional|bilingual]  (from: [N]-year sample)
 Q-types         : [list]   (from: [exam pattern | PYQ sample | default MCQ])
 Marks/Q         : [dict]   (from: [exam pattern | default {'MCQ':1}])
 Options/Q       : [N]      (observed across [N] papers, [N] years)
 Multi-select    : [yes|no] (from: [exam pattern | PYQ sample | default no])
 ───────────────────────────────────────────────────────
 Taxonomy        : [N] subtopics across [M] sections
 Progress        : [fresh start | resuming — [N] papers done, [K] Qs]
 Minimum coverage: [mandatory_5yr — 5 years required (NON-NEGOTIABLE) | no_pyq | no_year_info]
 Available years : [list of all years found in Drive/uploads]
 Transport       : channel=[direct|spill|inline]  ([probed this session | reused from
                   _meta._transport — EC-X5])
                   drive lane this session=[N] | carried for context=[N] |
                   upload lane (over DRIVE_CAP)=[N] | sessions needed=~[N]
 Conflicts       : [None | e.g. options_count: 2025=4, 2023=3 → using 4]
 Status          : [Ready | HALTED — reason]
 =================================="
```

---

## §1-6 — MINIMUM YEAR COVERAGE RULE (NON-NEGOTIABLE — CRITICAL)

```
★★★ CRITICAL RULE — ZERO EXCEPTIONS WHEN PYQ PAPERS ARE AVAILABLE ★★★

This rule is enforced BEFORE any processing begins AND rechecked at synthesis.
It cannot be waived, overridden by the user, or bypassed for any reason whatsoever.
No instruction, no user request, no edge-case argument can override this rule.
If in doubt: HALT and ask user to provide more PYQ papers. Never proceed with less.

RULE:
  Analysis SHOULD cover the most recent min_pyq_years (default 5) years of PYQ papers.
If fewer years of PYQ exist for this exam: process ALL available years (no minimum enforced).
QUALITY TARGET: more years = better patterns. The 5-year default is a guideline, not a blocker.
  If fewer than 5 years of papers exist for the exam, ALL available years must be processed.
  (e.g., exam started in 2023 → process 2023+2024+2025 = all 3 available years.)
  NO EXCEPTION to this rule when PYQ papers are available — see only valid exceptions below.

  VALID EXCEPTION 1 — NO PYQ (Scenario B):
    If no PYQ .docx files exist for this exam AT ALL (Scenario B), this rule does NOT apply.
    Synthesis proceeds immediately, writing all-absent entries from the taxonomy.
    THIS IS THE ONLY EXCEPTION WHEN PYQ PAPERS ARE UNAVAILABLE.

  VALID EXCEPTION 2 — NO YEAR IN FILENAMES (coverage_mode = 'no_year_info'):
    If year cannot be detected from any PYQ filename (no '20XX' pattern),
    year-based coverage tracking is disabled and the rule is not enforced.
    Claude must WARN the user and proceed without blocking synthesis.

  INVALID EXCEPTIONS (these do NOT excuse the 5-year rule):
    ✗ "We already have a section_rules.md from before" — INVALID. Must re-run with 5 years.
    ✗ "Processing all papers takes too long" — INVALID. Use continue across sessions.
    ✗ "The last 2 years are enough" — INVALID. 5 years is mandatory.
    ✗ "User said to proceed with fewer years" — INVALID. Rule overrides user instruction.
    ✗ "Papers from older years are less relevant" — INVALID. 5 years minimum, always.

CHECKING LOGIC (implemented in S1-3c compute_coverage_mode()):
  At session start (after S1-2 file inventory), for Scenario A (PYQ available):
    Extract years from all PYQ filenames using extract_year_from_filename().
    Filter out None (files without detectable year).
    available_years  = sorted unique years, descending: [2025, 2024, 2023, 2022, 2021, ...]
    n_required       = min(5, len(available_years))   # cap: can't require >what exists
    recent_5_years   = available_years[:n_required]   # most recent N years (up to 5)
    coverage_mode    = 'mandatory_5yr'                # single mode — always 5 years

  Displayed in S1-5 verification summary.

ENFORCEMENT AT SYNTHESIS (implemented in run_synthesise()):
  processed_years = set of years in progress['_meta']['years_processed']
  n_required      = min(5, len(available_years))

  if coverage_mode == 'mandatory_5yr':
    missing = [y for y in recent_5_years if y not in processed_years]
    if len(processed_years) < n_required or missing:
      → HALT — SYNTHESIS BLOCKED (see run_synthesise enforcement code in S8-4)

  if coverage_mode in ('no_pyq', 'no_year_info') → proceed without check.

  HALT means: do not write section_rules.md. Print the block message below.
  Do NOT silently proceed with insufficient data.
  Do NOT ask user if they want to proceed anyway — this is non-negotiable.

BLOCK MESSAGE (printed when halted):
  "★ SYNTHESIS BLOCKED: 5-YEAR COVERAGE RULE NOT MET ★
   Required : {n_required} most recent year(s): {recent_5_years[:n_required]}
   Processed: {processed_years}
   Missing  : {sorted(missing, reverse=True)}
   ACTION   : Process papers from the missing year(s) before synthesising.
              This rule cannot be waived. No exception applies here."
```

---

## §2 — UNIVERSAL EXTRACTION ENGINE: E-1 THROUGH E-11

These 11 rules apply identically to every exam.
Operations are universal. Outputs differ because PYQ content differs.

### E-1 — Hierarchy reading

PYQ papers are always presorted — bold taxonomy headings organize every
question into Subject → Topic → Subtopic before it appears.
There is no Mode B. If PYQ is not available for an exam, no .docx files
are uploaded and Step 5 skips extraction entirely, writing absent entries
from the taxonomy during --synthesise (see S1-2 no-PYQ path).

```
Helpers:

  def is_shift_tag(text):
      # Matches date-format shift tags like [09-Sep-2024 Shift 1] or [5-Jan-2024 Shift 1]
      # v2.52.0 (GAP-2026-08-16-...-DATE-LABEL-POSITION): delegates to the engine.
      # This was the THIRD copy of r'\[\d{1,2}-' in this one file. Three hand-kept
      # copies of one rule is the drift class bc.DATE_TAG_RE was created to end, and
      # a "v2.16 SYNC" comment aligning two of them by hand is the evidence that it
      # had already cost a release once.
      return bc.is_position_label(text)

  def parse_shift(text):
      # v2.16 RIGID-1: uses SESSION_RE (built from exam_config.json session_keyword)
      # instead of hardcoded 'Shift'. Works for Shift/Slot/Phase/Paper/Session.
      m = SESSION_RE.search(text)
      return f'S{m.group(1)}' if m else 'S1'

  # parse_taxonomy_level() defined in S3-2.
  # detect_question_start() defined in E-2.

Algorithm (pseudocode — full implementation in S3-2 extract_presorted()):
  current_path  = []    # [section, topic, subtopic]
  current_shift = 'S1'
  paras, nxt = bc.sorted_body_lookahead(doc)     # GAP-2026-07-26-001 + -08-05-001
  colour_ok  = bc.heading_colour_available(paras)   # D6 — once per FILE
  for i, paragraph in enumerate(paras):
      text = paragraph.text.strip()
      if not text: continue
      if is_taxonomy_heading(paragraph, nxt[i], colour_ok):
          level, content = parse_taxonomy_level(text)
          current_path = current_path[:level-1] + [content]
      elif is_shift_tag(text):
          current_shift = parse_shift(text)
      else:
          q_num = detect_question_start(text)
          if q_num is not None:
              tag_question(q_num, current_path, current_shift)

  is_taxonomy_heading() and parse_taxonomy_level() are defined in S3-2.
```

### E-2 — Question detection

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   Q_PATTERNS, detect_question_start
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    detect_question_start,
)
```

### E-3 — Option detection

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   OPT_PATTERNS, BARE_OPT_PATTERNS, para_has_image, is_option, clean_option_text
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    is_option, clean_option_text,
)
```

### E-4 — Image extraction and mapping

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   extract_and_map_images
#
# CONTRACT RETAINED HERE (the engine holds the code; this is what it must satisfy):
# image extraction/mapping is NOT complete without its accounting. An image present in
# the document and absent from the mapping produces a WRONG CLASSIFICATION, never an
# error — nothing raises and no gate trips, so the count assertion is the only thing
# that can notice. The mapping returned by extract_and_map_images() is therefore
# checked by corpus_io's count_image_refs / verify_images / image_gate_verdict and by
# blueprint_core's gates_passed / assert_image_survival before any classification is
# trusted (validator check Y-IMGGATE).
#
# WHY THIS PARAGRAPH IS HERE AND NOT IN THE AUDITOR. Y-IMGGATE is a TEXT-PRESENCE check
# on this spec, and moving the code took the accounting names out of the file, so the
# gate fired on a spec that had got safer. The tempting fix — widen the auditor to
# search every .py routed to the same trigger — was BUILT, MUTATION-TESTED AND
# REJECTED: corpus_io.py and blueprint_core.py both already contain those names, so it
# would have made Y-IMGGATE vacuous for nearly every spec in the estate. Retaining the
# contract in the spec keeps the check at exactly its original strength. Verified: strip
# these names from this file and Y-IMGGATE fires.
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    extract_and_map_images,
)
```

IMAGE ROLES:
- `stem_and_options` -> format=FIGURAL, option_format=image_only (image options — e.g. shape matching)
- `stem_only`        -> format=FIGURAL, text options (image in stem only)
- `options_only`     -> format=FIGURAL, stem is text
- `none`             -> text-only question

### E-5 — OMML formula extraction

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   MATH_NS, omml_to_linear, enrich_paragraph_with_omml
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    enrich_paragraph_with_omml,
)
```

### E-6 — NOTE/instruction block detection

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   NOTE_PAT, extract_note_block, classify_note_frequency, canonical_note_text
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    extract_note_block, classify_note_frequency, canonical_note_text,
)
```

### E-7 — Linked group detection

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   detect_linked_groups, extract_stimulus, classify_stimulus
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    detect_linked_groups,
)
```

### E-8 — Option format classification (12 types)

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   classify_option_format, subtopic_option_format
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    classify_option_format, subtopic_option_format,
)
```

### E-9 — Difficulty scoring (3-axis universal system)

> **CROSS-FILE SYNC RULE (v2.24.10):** the canonical shared copy of
> `score_difficulty` lives in `blueprint_core.py` Cluster E (consumed by
> PYQDeliver v1.2 Tier 2). Any edit here MUST be mirrored there (and vice
> versa) in the same session, byte-identical. Step 8 B-DIFF mirrors the MSQ
> load term — threshold/flag changes also require a Step 8 review.

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   score_difficulty
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    score_difficulty,
)
```

### E-10 — Template generation (subject-aware variable stripping)

> **CROSS-FILE SYNC RULE (v2.24.10):** `determine_strip_mode` below also has
> its canonical shared copy in `blueprint_core.py` Cluster E. Same mirroring
> obligation as E-9.

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   determine_strip_mode, strip_variables, generate_templates
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    determine_strip_mode, generate_templates,
)
```

APPROACH NAMING (add after generate_templates):
- quantitative: state formula ("Apply SI = PRT/100; find [variable] from [given]")
- reasoning:    state logic ("Decode substitution; apply same rule to target pair")
- factual:      state recall type ("Identify person/place from contextual clues")
- english:      state rule ("Select semantically correct word for blank position")
- logical:      "Evaluate statement-conclusion pairs using syllogism rules"

### E-11 — Wrong option structure classification (11 types)

```python
# IMPLEMENTATION EXTRACTED from §2 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   classify_wrong_option_structure, _classify_one_set
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    classify_wrong_option_structure,
)
```

---

## §3 — DOCUMENT PROCESSING PIPELINE

### S3-1 — Per-paper pipeline

```python
# IMPLEMENTATION EXTRACTED from §3 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   extract_shift_from_filename, process_pyq_paper
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
from analyse_engine import (
    extract_shift_from_filename, process_pyq_paper,
)
```


### S3-1c — IMG-6 VISION LIVENESS PROBE (v2.34, mandatory)

WHEN: once at the start of EVERY batch, BEFORE any figural classification.

WHY: figural classification depends on Claude actually seeing the figure. That
capability can stop working mid-session. Without a probe the pipeline cannot
distinguish "this figure is illegible" (a property of the IMAGE) from "I cannot see
anything" (a property of the SESSION), and records the second as the first — blaming
the corpus, inflating QV-9, and under-reporting FIGURAL patterns while the operator
troubleshoots the wrong thing.

v2.34 (GAP-2026-07-26-002 PART A). The v2.29 protocol was PROSE wired into no
executable block, single-attempt, single-token, with no requirement to record what was
read — and corpus_io.score_vision_probe() returned False for an empty string. A
non-observation was therefore indistinguishable from a genuine blind session, and
produced a false, session-terminating halt on essentially its first production use.
Three changes: the protocol is now a FUNCTION, it retries with THREE DISTINCT tokens,
and it NEVER HALTS — a failed probe records 'vision_unavailable' and processing
continues, because the three-state image_clarity value exists precisely so those
questions can be re-run later without discarding the rest of the batch.

DELETED IN v2.37 (GAP-2026-07-26-003). `run_img6_probe(read_probe)` took a CALLBACK
that was supposed to perform a `view()`. A callback cannot perform a tool call from
inside a running python process, so the parameter defaulted to a function returning
`''`, `score_vision_probe` raised ProbeObservationMissing on all three attempts, and
the probe returned False on EVERY run of EVERY exam. That False then marked all 153
figural questions in the reference corpus `vision_unavailable` — a "session is blind"
verdict produced by a session whose vision was fine.

**The probe is no longer needed, and a separate probe would now be a SECOND rule that
can drift from the first.** Phase B observes real figures. If ANY observation comes
back, vision demonstrably works; if NONE does, it demonstrably does not. Liveness is
therefore DERIVED from the merge, not measured separately:

```python
# IMPLEMENTATION EXTRACTED from §3 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   vision_liveness
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
import analyse_engine as _ae  # engine-internal only; no name bound here
```

`corpus_io.make_vision_probe()` / `score_vision_probe()` / `normalise_for_view()` are
DELETED in corpus_io v1.8, together with ProbeObservationMissing and VisionUnavailable.
Once no spec path called them, audit_callgraph C4 correctly reported them as
public-but-unreached, and leaving them would have made C4 report findings forever —
"a check that can be shipped past is decoration". Liveness now comes from observation
coverage, and normalisation lives inside build_vision_queue, so the empty-callback
failure mode is structurally impossible rather than merely documented against.

ON `unavailable`:
  Do NOT halt. Do NOT stop the batch. Every figural question records
  image_clarity='vision_unavailable', QV-9 excludes them, **QV-14 FAILs**, and the
  step footer renders F1 amber instead of F2 green. Tell the user which papers were
  affected and that a fresh session can re-run PHASE B ALONE — the queue and the
  contact sheets are already on disk, so Phases A and C need not repeat (EC-V3).

COST: 0 extra view() calls. Liveness comes free with the work.

### S3-1d — QV-13 IMAGE INTEGRITY REPORT (v2.29)

```
Written into analysis_progress.json per paper so the audit trail survives an Option-B
session restart:

  image_integrity: {
    gates       : {IMG-1..IMG-5 verdicts},
    probe       : 'pass' | 'fail',
    refs_body   : N,   mapped : N,   preamble : N,   header_footer : N,
    vector      : N,   unreadable : N,
    questions_with_images : N
  }

FLAGS (reported, not silent):
  * any gate FAIL                      -> HARD STOP (raised at extract time)
  * preamble > 0                       -> note: images before Q.1, not question figures
  * vector > 0                         -> note: EMF/WMF present, rasterised before view()
  * probe == 'fail'                    -> batch halted, session restart required
  * figural_consistency mismatches     -> see IMG-5b below

IMG-5b — FIGURAL CROSS-CHECK. After classification:
  corpus_io.figural_consistency(mapping, q_formats, overrides=<INHERENTLY-VISUAL log>)
catches two faults with one assertion:
  * a question WITH an image not classified FIGURAL  -> image lost, or classifier missed it
  * a question classified FIGURAL with NO image      -> misclassification, unless it is an
    explicitly logged INHERENTLY-VISUAL override
Both are reported with question numbers. Neither is silently accepted.
```

#### IMG-5b — FIGURAL CROSS-CHECK (executable, v2.35)

```python
# IMPLEMENTATION EXTRACTED from §3 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   run_img5b
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
import analyse_engine as _ae  # engine-internal only; no name bound here
```

### S3-2 — Presorted extraction (the only extraction mode)

```python
# IMPLEMENTATION EXTRACTED from §3 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   is_taxonomy_heading, parse_taxonomy_level, extract_year_from_filename, detect_blank_position, _MSQ_INSTR_RE, _COMBO_OPT_RE, _is_statement_combination, detect_is_msq, _detect_option_label_style, extract_presorted
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
from analyse_engine import (
    extract_year_from_filename,
)
```

---

## §4 — VISION ANALYSIS FOR FIGURAL QUESTIONS

Claude performs all vision analysis automatically using the `view` tool.
The user is never asked to describe images. This is Claude's responsibility.

### S4-1 — When to run

After E-4 maps images to questions, identify which questions need vision:

```python
# IMPLEMENTATION EXTRACTED from §4 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   get_vision_candidates
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    get_vision_candidates,
)
```

### S4-2 — Vision analysis: the THREE-PHASE contract (v2.37)

`analyse_image_claude()` USED TO LIVE HERE and has been DELETED. It was a
`pass`-bodied function that a python loop called and whose return value the same
loop immediately consumed. That is not a bug in one function — it is a category
error, and the corpus now has a rule for it:

> **EXECUTION-BOUNDARY LAW.** Every operation is DETERMINISTIC (python may run it),
> CLASS J (model judgment over data already in context), or CLASS T (requires a
> TOOL CALL — `view`, MCP, fetch). **A CLASS T operation MUST NOT be called from
> inside a python execution block and MUST NOT be modelled as a python function,
> callback or parameter.** A tool call can only occur BETWEEN model turns; python
> that "calls" a tool is unreachable code returning a default forever, silently.
> CLASS T uses MATERIALISE-THEN-INJECT: Phase A python prepares a work queue on
> disk, Phase B the model performs the tool calls in its own turn and writes the
> results to disk, Phase C python consumes them.

Viewing a figure is CLASS T. The three phases:

| Phase | Runs as | Owner | Output |
| :-- | :-- | :-- | :-- |
| **A** S4-2a | python | `corpus_io.build_vision_queue()` | `vision_queue.json` + contact sheets |
| **B** S4-2b | **model, in-turn** | the prose protocol below | `vision_observations.json` |
| **C** S4-2c | python | `bc.merge_vision_observations()` | the five vision fields |

**NO PHASE HALTS.** If Phase B never runs, Phase C still runs, every figural
question records `image_clarity='vision_unavailable'`, `vision_status` says
`unavailable`, QV-14 reports FAIL and the footer renders amber. The run COMPLETES.
The defect this replaces was silent, and the remedy for silence is visibility — not
a halt.

### S4-2a — PHASE A (python): queue the work

Called from `process_pyq_paper()` (§3 S3-1). Pure python: normalise → compose →
tile → write. It never views anything.

```python
# IMPLEMENTATION EXTRACTED from §4 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   VISION_WORKDIR, VISION_PER_SHEET
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    VISION_WORKDIR, VISION_PER_SHEET,
)
```

Contract (all enforced by `corpus_io.self_test()`):

- every queued item appears on **exactly one** sheet, and that sheet exists
- tags are stable across re-tiling and across adding papers (EC-V11/V12)
- a question's panels share one cell (EC-V6)
- an unopenable vector/corrupt part is queued and flagged, never dropped (EC-V8)
- Pillow absent degrades to one view per figure, never a silent skip (EC-V9)
- two records for one `(paper_id, q_num)` collapse to one tagged cell (EC-V27)

### S4-2b — PHASE B (MODEL, IN-TURN): view the sheets

> **This block is PROSE ON PURPOSE. Its fence is deliberately UNLABELLED and must
> never be changed to a python fence.** The moment it becomes a function, it becomes unreachable again and
> this entire defect returns. If a future editor feels the urge to "implement" this
> section, that urge is the bug.

```
FOR EACH sheet listed in vision_queue.json['sheets']:

  1. view(<VISION_WORKDIR>/<sheet>)

  2. The sheet is a grid of cells. Every cell carries a BLACK LABEL BAR at its top
     showing that cell's TAG (e.g. "2B73-14"). Read the tag from the bar, not from
     position — a re-tile changes position and never changes the tag.

  3. For EVERY cell on the sheet, record ONE object:

       {"tag": "<tag exactly as printed>",
        "figure_readable": true|false,
        "object_type": "...",            # what KIND of object the figure shows
        "transformation_type": "...",    # rule across a series; "N/A" if single
        "arrangement": "...",            # row_series | matrix | pair_analogy | single
        "complexity": "Simple|Medium|Hard"}

     * figure_readable=false when THIS FIGURE is too small/blurry/corrupted to
       classify. Record it and leave the other fields out. DO NOT GUESS — a guess
       is worse than a recorded gap, because a gap is visible and a guess is not.
     * A cell labelled [UNRENDERABLE] carries no image: record figure_readable=false.
     * object_type is drawn from what the corpus actually contains. It is NOT a
       closed list and NOT exam-specific — name what is there, in lower_snake_case,
       and use the SAME name for the same kind of thing across sheets.

  4. Write every observation to <VISION_WORKDIR>/vision_observations.json via
     corpus_io.write_vision_observations(), as {"observations": [ ... ]}.

OMITTING A CELL IS A PROCEDURAL ERROR, NOT A SESSION VERDICT. Phase C counts an
omitted cell as unobserved and QV-14 reports the true ratio. Re-running Phase B is
idempotent and safe (EC-V4/EC-V12) — observations are matched by tag, so a second
pass simply fills the gaps. Phases A and C need not repeat (EC-V3).

IF THE SHEETS DO NOT RENDER AT ALL, vision is unavailable in this session. DO NOT
HALT and DO NOT invent observations. Write an empty observations list, let Phase C
mark every figure vision_unavailable, and let QV-14 report it. The remedy is a
fresh session re-running PHASE B ONLY — the queue and sheets are already on disk.
```

### S4-2c — PHASE C (python): merge observations back

```python
# IMPLEMENTATION EXTRACTED from §4 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   apply_vision_observations
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    apply_vision_observations,
)
```


### S4-3 — Integration into paper processing pipeline

Vision is NOT an inline step inside `process_pyq_paper()` and cannot be one — see
S4-2. What runs per paper is PHASE A only.

Key points:
- `get_vision_candidates(questions, q_roles, image_map)` filters to qualifying Qs
  and returns ALL of each question's stem images (EC-V6)
- `corpus_io.build_vision_queue(...)` (Phase A) writes contact sheets + the queue.
  It views nothing and populates no vision field.
- **PHASE B runs at the batch boundary** the run already stops at under the S8-1
  BATCH STOP law. Nothing new interrupts a run and no halt is introduced.
- `apply_vision_observations(progress)` (Phase C, S4-2c) is the ONLY writer of
  `object_type`, `transformation`, `arrangement`, `complexity` and `image_clarity`.
- Until Phase C runs those fields are ABSENT, not `None` and not guessed.
- Re-running Phase B is idempotent; Phases A and C need not repeat (EC-V3/EC-V4).

### S4-4 — Aggregate per subtopic (unchanged logic, fully automated)

```python
# IMPLEMENTATION EXTRACTED from §4 (2026-08-17, v2.53.2) to the repo engine file
#   analyse_engine.py   —   aggregate_figural
# Moved VERBATIM: the block that lived here through v2.53.1 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified, exactly as frequency_xlsx.py has been since §16 moved at
# v2.39.2. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — it is not a .md and SKILL
# Rule 2 does not route it, so it costs a session nothing to use.
from analyse_engine import (
    aggregate_figural,
)
```

---

## §5 — SYNTHESIS ENGINE

### S5-1 — Pre-synthesis check

```python
# IMPLEMENTATION EXTRACTED from §5 (2026-08-17, v2.53.3) to the repo engine file
#
# ── EMITTED-STAMP CONTRACT (retained here; the engine holds the assignments) ──
# The engine emits these three literals into every artefact, and they MUST track this
# file's header major.minor:
#     FRAMEWORK_STAMP         = 'Framework_MockTestAnalyse v2.53'
#     GENERATED_BY_STAMP      = 'Generated by Framework_MockTestAnalyse v2.53'
#     FRAMEWORK_VERSION_STAMP = 'framework_version: v2.53'
# CROSS-FILE SYNC RULE: bumping this file's MAJOR.MINOR requires the same bump in
# analyse_engine.py. A PATCH bump (v2.53.2 -> v2.53.3) does not, which is exactly why
# the extraction batches are PATCH releases.
#
# WHY THESE LITERALS STAY IN THE SPEC. mock_sync_audit MS-3 is a PRESENCE check over
# this file's fences, and moving the assignments into the engine took the literals out
# of the file — MS-3 then reported that it could match nothing, which its own comment
# names as the disarmed state ("reports success while checking nothing"). The fix is
# the one MS-3 asks for: keep one literal per pattern. Widening MS-3 to search the
# routed engines was NOT done, for the same reason it was not done for Y-IMGGATE in
# B2 — a presence check that follows code into large shared engines goes vacuous.
# A CALL-SITE check may follow the code; a PRESENCE check may not.
#   analyse_engine.py   —   pre_synthesis_check
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
import analyse_engine as _ae  # engine-internal only; no name bound here
```

### S5-2 — Per-subtopic synthesis

```python
# IMPLEMENTATION EXTRACTED from §5 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   AXIS2_CLASSES, STEM_FORMAT_TO_AXIS2, FAMILY_AXIS2_MENU, _TABLE_WORD_RE, _looks_like_table_stimulus, classify_axis1, classify_axis3, _opts_are_combination_labels, _MATCH_PAIR_RE, _MATCH_PAIR_SUB, _MATCH_OPT_RE, _label_family, _opts_are_match_pairs, classify_axis2, tag_axes, _FAMILY_KEYWORDS, resolve_presentation_family_s5, axis2_capability, compute_section_axis_distribution, FIGURAL_IRREDUCIBLE_RATE, synthesise_subtopic, _detect_recycled_stimuli, _absent_entry, build_diff_criteria, infer_approach, extract_number_ranges, extract_context_pool, extract_passage_structure
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
from analyse_engine import (
    synthesise_subtopic,
)
```

### S5-3 — Write section_rules.md

```python
# IMPLEMENTATION EXTRACTED from §5 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   _compute_structural_changes, canon_text, _has_word, _HI_MAP, _translit_hint, _VERBAL_SECTION_HINTS, _is_verbal, _OVERRIDES, _MERGE_LOG, load_mechanic_overrides, io_open_utf8, _FAMILY_MAP, _QUALIFIERS, _QUALIFIABLE, _ALL_FAMILY_NAMES, _TEMPLATE_SET, _identity_base, _redundant, _extract_qualifiers, _allowed_template_sets, derive_mechanic, mint_subtopic_ids, apply_subtopic_merges, stamp_mechanic_axes, _derive_axes, _derive_concept_group, _derive_question_mechanic, _derive_form_key, _derive_collision_domain, FRAMEWORK_STAMP, GENERATED_BY_STAMP, FRAMEWORK_VERSION_STAMP, write_section_rules, slugify, _PREFIX_STOPWORDS, section_prefix, build_section_prefix_map, _as_mandate_int, _mandate_from_note, make_subtopic_id, _ZP_VISUAL_KEYWORDS, infer_zero_pyq_axes, apply_zero_pyq_format_inference, make_zero_pyq_scaffold_entry, taxonomy_sync_entries, _extract_taxonomy_tuples_from_analysis_doc, write_taxonomy_xlsx, write_subtopic_manifest, rebuild_subtopic_manifest_from_section_rules, format_entry
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
from analyse_engine import (
    mint_subtopic_ids, apply_subtopic_merges, stamp_mechanic_axes,
    write_section_rules, apply_zero_pyq_format_inference, taxonomy_sync_entries,
    write_subtopic_manifest,
)
```

---

## §6 — QUALITY VERIFICATION (QV-1 through QV-16)

```python
# IMPLEMENTATION EXTRACTED from §6 (2026-08-17, v2.53.3) to the repo engine file
#   analyse_engine.py   —   run_qv, print_qv
# Moved VERBATIM: the block that lived here through v2.53.2 is byte-identical to
# the corresponding region of the engine. Hash-tracked in MANIFEST.json and
# bootstrap-verified. THIS SECTION RETAINS THE CONTRACT; THE ENGINE HOLDS THE CODE.
# The engine is IMPORTED AND EXECUTED, NEVER READ — not a .md, so SKILL Rule 2
# does not route it and it costs a session nothing to use.
from analyse_engine import (
    run_qv, print_qv,
)
```

---

## §7 — EDGE CASES (EC-1 through EC-15)

```
EC-1:  INCOMPLETE OPTIONS (<options_count extracted)
  1. E-5 OMML: may have formula in option slot.
  2. E-4 q_roles: may be image-only option.
  3. Still <N: q_incomplete=True, exclude from template extraction.

EC-2:  STEM CONTENT AFTER OPTIONS
  Apply E-6 to detect NOTE. If NOTE: record. If not: discard and log.

EC-3:  IMAGE ROLE CLASSIFICATION
  stem_and_options -> format=FIGURAL, option_format=image_only
  stem_only        -> format=FIGURAL, text options
  Determined from E-4 q_roles. S4-3 computes dominant_role from data.

EC-4:  SHARED DI TABLE VS INDEPENDENT TABLES
  E-7 Method 1: shared table (>=90% match) -> linked group (linked_group_size=N).
  Own table: not linked (linked_group_size=0). Both valid.

EC-5:  HINDI / REGIONAL LANGUAGE
  E-6: NOTE_PAT uses non-raw string with actual \u escapes (fixed BUG-A14 related).
  E-10: factual mode skips proper-noun stripping (capitalisation unreliable).

EC-6:  MARKS VARIATION (multi-mark exams — e.g., 1-mark and 2-mark questions)
  Triggered when: exam has questions carrying different marks (read from _meta marks_per_q dict).
  score_difficulty called with marks=q_marks.
  Difficulty thresholds scale: simple_threshold = 4 + (marks-1).
  Exam-agnostic: marks_per_q read from section_rules.md EXAM_STRUCTURE block.
  No exam names hardcoded — any exam with multi-mark Qs triggers this edge case.

EC-7:  MULTI-SELECT QUESTIONS (MSQ)  [v2.5 — dormant unless multi_select_allowed]
  q['is_msq']=True detected in presorted mode via detect_is_msq() (option-shape
  aware — see EC-A). Synthesis aggregates per-question is_msq into a per-SUBTOPIC
  answer_cardinality ∈ {single, multi} (CATEGORY B) — the Step 7 dispatch unit — plus
  msq_freq%. A subtopic is treated as uniformly single- or multi-answer
  (whole-subtopic mode), so the downstream per-mock allocation schema is unchanged.
  Step 7 GENERATES MSQ for multi subtopics per the answer_cardinality contract (it no
  longer skips them). k-mode/k and per-type marking come from the Exam Pattern doc
  (PYQ has no key → k is unextractable), carried in EXAM_STRUCTURE. When
  multi_select_allowed=false, is_msq is always False and this whole path is inert.

EC-A:  STATEMENT-COMBINATION MCQ vs MSQ (false-positive guard) [v2.5]
  ROOT CAUSE of the v2.4 mis-tag: the old is_msq regex matched "Which is/are
  correct?" — but EC-9 statement-combination questions use that exact phrasing and
  are SINGLE-answer (you pick one combo option). The forgery-resistant signal is
  OPTION SHAPE: if the options are predominantly combination-labels (Only N /
  Both N and M / Neither…nor / "N and M" / None of / All of the above), the
  question is a statement-combination MCQ and is NEVER MSQ, regardless of stem
  wording. detect_is_msq() requires a genuine multi-select instruction AND
  non-combo options. Validated empirically against real docx fixtures (a genuine
  statement MSQ with ordinary options stays MSQ; a combo-label MCQ stays MCQ).

EC-8:  ASSERTION-REASON FORMAT
  Template: "Assertion (A): _STMT_ Reason (R): _STMT_"
  wrong_option_structure: fixed_set. fixed_option_texts recorded exactly.

EC-9:  STATEMENT-COMBINATION FORMAT
  Template: "Consider the following statements: 1. _STMT_ 2. _STMT_ Which is/are correct?"
  Note: spaces (not \n) because stems are space-joined from paragraphs.
  E-11: options classified as sentence_label.

EC-10: NON-REPRINTED PASSAGE (proximity detection)
  Detect during extraction: paragraph >100 words before run of short-stem Qs.
  Link following Qs to that passage group.

EC-11: FILL-IN-BLANK STEMS
  blank_pos recorded. Template preserves _BLANK_. Wrong option: same_category.

EC-12: NEGATIVE QUESTIONS (NOT/INCORRECT/EXCEPT/FALSE/WRONG)
  is_negative=True. score +1. negative_question_freq% recorded for Step 7.

EC-13: MATCHING TYPE QUESTIONS
  Template: "Match _ITEM_ with _ITEM_"
  option_format: value_pair_quad.

EC-14: YEAR-WISE PATTERN DRIFT
  deprecated=True (set in generate_templates) if pattern absent from last 2 years.
  confidence='observed_recent' if ONLY in last 2 years.
  Step 7 EC-14: observed_recent weight x1.5; deprecated weight x0.1.

EC-15: CROSS-SUBJECT QUESTIONS
  Trust the docx taxonomy heading — it is always authoritative in presorted papers.
  When a question's content spans multiple subtopics (e.g. arithmetic + DI),
  the heading under which it appears is the correct classification.
  Step 7 ignores any secondary subtopic signal.

EC-16: THREE-AXIS CLASSIFICATION (v2.23 — see AXIS CLASSIFIER v1.0)
  Every question is tagged on THREE orthogonal axes by the shared classifier
  (tag_axes): Axis-1 stimulus (TEXT|FIGURAL|PASSAGE|DI), Axis-2 stem structure
  (the exclusive 8-class ladder), Axis-3 mechanism (MCQ|MSQ|NAT); negative polarity
  is an orthogonal flag (is_negative), never an Axis-2 class.
  EXCLUSIVITY: first-match-wins; LINKED is a GATE decided by linked_group_id (shared
  stimulus), not phrasing — so an assertion-reason inside a passage is LINKED. SEQUENCE
  is ordered ABOVE STATEMENT (the operation is arranging). DIRECT is the residual.
  OVERLAP EXAMPLES resolved deterministically: "which pair is NOT matched" → MATCH +
  is_negative; "arrange the following statements" → SEQUENCE (not STATEMENT); a passage's
  A-R sub-question → LINKED (not ASSERTION_REASON).
  This classifier is the SINGLE SOURCE OF TRUTH — Step 8 re-tags GENERATED questions with
  the identical functions so the PYQ target and the generated output are comparable.
```

---

## §8 — BATCH EXECUTION AND SESSION FLOW

### S8-0 — TRANSPORT PREFLIGHT (runs ONCE per session, BEFORE the first batch)

```
GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. Step 5 had no channel probe, no
transport plan, no context budget and no persistence of the transport verdict —
while being the one step in the framework that is inherently multi-session.

GAP-2026-08-16-STEP5-SESSION-EXHAUSTION rewrites the ORDER of this phase. The
v2.50.0 order listed the folder, probed the SMALLEST paper, then partitioned. All
three of those steps were wrong in a way that only shows up together: the probe
paper was not in the admitted set so its payload was discarded, the probe was
never charged against the budget so the printed plan was arithmetic fiction, and
the listing cache was hand-transcribed with nothing comparing it to what Drive
returned. Measured: session 1 spent 107,968 real characters — 54% of the entire
budget — to classify a channel, and processed zero papers.

CHANNEL PRECEDENCE IS direct -> spill -> inline. Framework_PYQCore EC-P43.

PHASE A — MODEL TURNS. CLASS T unless stated. In order:

  A0. DIRECT EGRESS PROBE — PYTHON, NOT A TOOL CALL, AND IT COMES FIRST.
      Call corpus_io.probe_direct_egress(candidate, work_dir) on the first
      recency-sorted paper under bc.DRIVE_CAP (see A1b — the sort runs before
      this). If it returns ok, the channel is 'direct': python fetched the bytes
      itself, nothing crossed the turn, EC-P36's double charge does not exist,
      `consumed` is 0, and EVERY paper under the cap is admissible in one session.
      The probe NEVER raises; ok=False is an ordinary state, not an incident.

      Two preconditions must both hold and NEITHER may be assumed: container
      egress reaches drive.google.com, and the folder's General access is
      "Anyone with the link". When either is absent the run falls through to A2
      and behaves exactly as it did before this lane existed. An exam whose
      folder is not link-shared is not a broken exam.

      SKIP A0 when _meta._transport.channel is already recorded (EC-X5) and when
      mode is --status or --synthesise (EC-X14).

  A1. Google Drive:search_files(query="parentId = '<folder_id>'", pageSize=100)
      Paginate to exhaustion; recurse into every sub-folder the response reports.
      Keep EVERY raw page exactly as the connector returned it — do not reshape,
      do not merge by hand, do not drop fields you think are unused.

      Then, IN PYTHON, hand every page to
        corpus_io.write_drive_listing(pages, DRIVE_LISTING_CACHE, folder_id,
                                      observed_count=<the count YOU read off the
                                      connector response>)
      `observed_count` is the whole point of the gate: it is an INDEPENDENT number
      you declare, so the comparison is capable of failing. A short listing HARD
      STOPS (EC-P41) — it is worse than an empty one, because EC-P39 catches zero
      and nothing at all caught 21-of-22 before this release. Never cache only
      page 1: a lost tail is a missing year that §1-6 cannot see (EC-X16), and it
      is now a hard stop rather than a silent loss.

      The function also REPORTS the year span and any interior gaps. Print it.
      It never stops on a gap — an exam may genuinely not have been held in a
      year, and only the operator can tell that apart from a listing defect — but
      it must be on screen BEFORE paper 1, while acting on it is still cheap.

  A1b. collect_corpus_files -> sort_papers_recency_first. THE SORT RUNS BEFORE THE
      PARTITION, ALWAYS (EC-X21, P4d). Measured: partitioning the raw listing
      order admitted 2017/2021/2014; partitioning after the sort admitted
      2026/2025/2024. On an inline channel the difference can leave §1-6's
      required latest-five-years permanently unreached while the operator watches
      papers arrive successfully.

  A2. CONNECTOR CHANNEL PROBE — reached ONLY when A0 returned ok=False.
      Download exactly ONE paper: `admitted[0]`, the FIRST RECENCY-SORTED PAPER
      THE PLAN WILL FETCH ANYWAY (P4f below). Not the smallest.
      Then OBSERVE YOUR OWN TURN: did the tool hand back a REFERENCE TO A FILE,
      or the BYTES THEMSELVES? That is `arrived_inline`. It is a fact about what
      you received, not an inference.

      NEVER classify by listing a directory to see whether a spill file appeared.
      EC-P35 forbids it and the reason is measured: the spill directory differs
      between deployments of the SAME connector, and one deployment has no such
      directory at all. A path-hardcoding probe reports 'inline' on a working
      spill channel and sends a fully fetchable corpus to manual upload, on every
      exam, forever — silently. That is worse than the defect the probe exists to
      catch.

      SKIP the probe entirely when _meta._transport.channel is already recorded
      (EC-X5), and when mode is --status or --synthesise (EC-X14) — those modes
      read no papers and must not pay a probe's context.

  A3. Download every REMAINING paper this SESSION's plan admits (see
      plan_transport below). The probe payload is ALREADY one of them — pass it
      into drive_payloads with the rest. Record, per file, WHATEVER CAME BACK — a
      spill path in any directory, or an inline payload. Do not normalise,
      relocate or unwrap it: corpus_io owns every shape the connector emits, and a
      spec-side extraction is a second definition that will drift (EC-X11,
      EC-X12).

PHASE B — PYTHON. Inject resolvers over results that ALREADY EXIST. No CLASS T
tool call occurs below this line. (A0 is python and is therefore not a tool call
at all; it is listed in PHASE A because it decides the channel, and the channel
must be decided before anything is planned.)
```

```python
# ── S8-0 TRANSPORT PREFLIGHT ─────────────────────────────────────────────────
# GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. Ported in CONTRACT from
# Framework_PYQCount S5-0, with four Step-5-specific deviations (P4a–P4e below)
# that exist because Step 4 is a SINGLE-session script step and Step 5 is a
# MULTI-session batched step. Porting S5-0 verbatim would be wrong here.

SESSION_INLINE_BUDGET = bc.INLINE_BUDGET_CHARS // 2
# P4c / EC-P36 — CHARGE THE PAYLOAD TWICE ON AN INLINE CHANNEL.
# bc.INLINE_BUDGET_CHARS prices INBOUND characters only: partition_by_transport
# sums bc.base64_cost_chars against it. On an inline channel Step 5 pays that cost
# a SECOND time, because the model receives the base64 in the tool result and must
# then RE-EMIT it into a python block for stage_drive_payload to decode.
# THIS DESCRIBES THE CONNECTOR LANE ONLY, AND IT IS NO LONGER THE ONLY LANE. Until
# EC-P43 the statement here read "there is no third route — the container's egress
# allowlist contains no Google domain". That was true of the deployment measured on
# 2026-08-15 and is NOT a property of the framework: the allowlist is configurable.
# When it reaches drive.google.com and the folder is link-shared, PHASE A/A0 fetches
# the bytes in python, nothing crosses the turn, and neither this halving nor the
# EC-P36 double charge applies. The halving below stays correct and mandatory
# WHENEVER the channel is 'inline'; it is inert on 'direct' and on 'spill'.
# Halving here rather than changing bc.INLINE_BUDGET_CHARS is deliberate: the
# shared constant is Step 4's too, and mutating it would silently re-partition a
# step this GAP does not touch. This is a DERIVED value, never a literal — the
# threshold still has exactly one definition, exactly as DRIVE_CAP does.


def acquire_listing(pages, cache_path, folder_id, observed_count):
    """PHASE A / A1 — persist DRIVE_LISTING_CACHE through the engine, and ASSERT it.

    `pages` is every RAW connector page for this folder, unmodified. `observed_count`
    is the total the model declares from the connector response — an INDEPENDENT
    number, which is the only reason the comparison is capable of failing.

    A short listing HARD STOPS (ListingIntegrityError, EC-P41). It is deliberately not
    a TransportFallback: a fallback means "try another lane", and there is no other
    lane for a corpus that cannot be enumerated correctly. EC-P39 already caught zero;
    nothing caught 21-of-22, and 21-of-22 is the dangerous one because §1-6 reports
    success on whatever survived and the missing year stays invisible for the life of
    the exam.

    The year span and any interior gaps are REPORTED, never stopped on — an exam may
    genuinely not have been held in a year and only the operator can tell that apart
    from a listing defect. Printing it here puts it on screen before paper 1.
    """
    report = corpus_io.write_drive_listing(pages, cache_path, folder_id, observed_count)
    print(f"\n  DRIVE LISTING  ({report['count']} record(s) cached, asserted against "
          f"{observed_count} declared)")
    if report['year_span']:
        print(f"    Year span         : {report['year_span'][0]}-{report['year_span'][1]}")
    if report['missing_years']:
        print(f"    ! Interior gaps   : {report['missing_years']} — REPORT ONLY. An exam "
              f"may not have been held in a year; confirm before Task 1.")
    else:
        print("    Interior gaps     : none")
    return report


def probe_transport(candidate, work_dir, recorded=None):
    """PHASE A / A0 -> A2 — decide the channel. DIRECT FIRST, then the connector.

    Returns (verdict_or_None, probe_consumed). A None verdict means the direct lane
    was unavailable and the caller must run the connector probe (A2) on admitted[0].

    EC-P43. The direct lane is PROVEN on a real paper and never predicted;
    corpus_io.probe_direct_egress never raises, because an unshared folder or a
    deployment without Google egress is an ORDINARY state and an exception here would
    turn a routine fallback into a halted run.

    EC-X5 / EC-P38 — a recorded verdict is REUSED, never re-probed, and `consumed` is
    then 0. Re-probing costs one paper's context every session for a fact that is a
    property of the deployment.
    """
    if recorded and recorded.get('channel'):
        print(f"\n  TRANSPORT VERDICT REUSED — channel "
              f"{recorded['channel'].upper()} (EC-X5); no probe this session.")
        return recorded, 0
    direct = corpus_io.probe_direct_egress(candidate, work_dir)
    if direct['ok']:
        print(f"\n  S8-0 A0 DIRECT EGRESS PROBE — {candidate['name']}")
        print(f"    Verified bytes on disk : {direct['path']}")
        print( "    Channel                : DIRECT — python fetched the bytes itself; "
               "nothing crossed the turn, so the whole corpus is admissible (EC-P43)")
        return {'channel': 'direct', 'probe_paper': candidate['name'],
                'probe_local_path': direct['path']}, 0
    print(f"\n  S8-0 A0 DIRECT EGRESS PROBE — unavailable: {direct['reason']}")
    print( "    Falling back to the connector lane. This is an ordinary state, not a "
           "failure: the run proceeds exactly as it did before EC-P43 existed.")
    return None, 0


def probe_drive_channel(probe_paper, probe_payload, arrived_inline, work_dir):
    """Classify the CONNECTOR Drive channel from ONE real download, and PROVE it decodes.

    REACHED ONLY WHEN THE DIRECT LANE IS UNAVAILABLE (PHASE A / A0, EC-P43). When
    corpus_io.probe_direct_egress succeeded the channel is 'direct', this function is
    never called, and probe_consumed is 0 — python holds verified bytes and nothing
    crossed the turn.

    `probe_paper` is admitted[0], NOT the smallest paper — see plan_transport's P4f.

    Identical contract to Framework_PYQCount S5-0. `arrived_inline` is the model's
    OBSERVATION about its own turn (PHASE A step A2), never a filesystem test.

    The probe PROVES the lane rather than predicting it: the payload is staged
    through the same engine path the whole run will use, so a channel that
    classifies cleanly but cannot produce verified bytes fails here, at paper 1,
    instead of at paper 12. Any TransportFallback propagates to the caller, which
    routes the corpus to the upload lane per EC-P35 / EC-X20.
    """
    local_path = corpus_io.stage_drive_payload(probe_payload, probe_paper, work_dir)
    channel = 'inline' if arrived_inline else 'spill'
    print(f"\n  S8-0 CHANNEL PROBE — {probe_paper['name']} "
          f"({probe_paper['fileSize']:,} bytes)")
    print(f"    Verified bytes on disk : {local_path}")
    print(f"    Channel                : {channel.upper()}"
          + ("  — payloads arrive in context; the Drive lane is bounded by context"
             if channel == 'inline' else
             "   — payloads land on disk; the Drive lane costs no context"))
    return {'channel': channel, 'probe_paper': probe_paper['name'],
            'probe_local_path': local_path}


def plan_transport(pending_recency_sorted, channel, session_budget, batch_size,
                   probe_consumed=0):
    """Decide what THIS SESSION fetches. Print it BEFORE the first batch.

    P4f — PROBE PAPER SELECTION DIVERGES FROM STEP 4, ON PURPOSE.
    Framework_PYQCount S5-0 probes the SMALLEST paper. That is correct THERE: Step 4 is
    single-session and fetches the whole corpus in the same run, so the probe cost is
    amortised to zero. Step 5 is batched across ~8 sessions and its admitted set is
    recency-first, so the smallest paper is almost never the one being fetched — its
    payload is decoded, proven, and thrown away.
    Measured on IIT_JAM_MATHEMATICS: probing the smallest (10-Feb-2013, 40,488 B) spent
    107,968 real characters, 54% of INLINE_BUDGET_CHARS, on a paper the admitted set
    does not contain, and session 1 processed ZERO papers. Probing admitted[0]
    (15-Feb-2026, 47,627 B) proves the lane AND delivers paper 1 for the same
    characters, so probe_consumed is 0 — the payload is not waste, it is paper 1.
    v2.50.0 inherited "SMALLEST" verbatim when S8-0 was ported in CONTRACT from S5-0;
    the four documented deviations P4a-P4e covered budget, persistence, halving,
    partition ordering and the PYQCompress text, and probe-paper selection was never
    reviewed. mock_sync_audit MS-13 now fails the build for a spec that carries a
    channel probe without declaring its probe-paper rule and any divergence.

    P4g / EC-P40 — THE PROBE IS A SPENDER, NOT A FREE CLASSIFIER.
    `probe_consumed` is budget ALREADY SPENT in this session before this partition is
    computed. Before it existed the partition was computed against the FULL budget as
    though the probe were free: probe 107,968 + admitted paper 127,008 = 234,976 real
    characters against a 200,000 ceiling, and this function printed "1 paper(s) fetch
    automatically". Values:
        probe ran this session, connector lane  -> bc.base64_cost_chars(probe fileSize)
        probe reused from _meta._transport      -> 0            (EC-X5 / EC-P38)
        probe re-run on resume                  -> charged in THAT session (EC-P38)
        probe raised TransportFallback          -> STILL CHARGED — the bytes arrived
        channel 'spill' or 'direct'             -> 0, and the parameter is inert
        probe IS admitted[0] (P4f)              -> 0, the payload is paper 1
    audit_callgraph C10 fails the build for a partition call preceded by a CLASS T
    acquisition without a non-defaulted consumed=.

    P4d / EC-X21 — THE INPUT MUST ALREADY BE RECENCY-SORTED. bc.partition_by_transport
    admits papers in the order it receives them until the budget would be exceeded,
    and corpus_io.collect_corpus_files returns DRIVE LISTING order. Measured on the
    22-paper IIT_JAM_MATHEMATICS corpus, same papers, same budget, only the order
    changed:
        partitioned BEFORE the recency sort -> 2017, 2021, 2014   (185,892 chars)
        partitioned AFTER  the recency sort -> 2026, 2025, 2024   (189,156 chars)
    That is not cosmetic. S8-1's whole processing-order rationale is that an early
    stop must leave section_rules.md reflecting the MOST RECENT patterns, and §1-6
    requires the latest five years. Partitioning the raw listing order on an inline
    channel can leave the §1-6 required set permanently unreached while the operator
    watches papers arrive successfully. Always sort first.

    P4a — ON AN INLINE CHANNEL STEP 5 DOES NOT ROUTE THE CORPUS TO UPLOAD.
    EC-P35's Step-4 resolution is "route the WHOLE corpus to the upload lane",
    which is right for a step that must finish in one session and wrong here.
    Step 5 already has BATCH_SIZE 3, a mandatory BATCH STOP and a documented
    Option B (download analysis_progress.json, open a fresh chat) — AND A FRESH
    CHAT RESETS THE CONTEXT BUDGET. So the budget is applied PER SESSION and the
    remainder is carried to the next session, not demanded as manual uploads. The
    upload lane stays the fallback for a paper that cannot fit even one session's
    budget, or that exceeds bc.DRIVE_CAP.

    `batch_size` is passed in rather than read from the module-level BATCH_SIZE, which
    S8-1 defines AFTER this section. A forward reference would be a name this spec's own
    checkers cannot resolve, and this GAP is about instructions the CI cannot read.
    Callers pass BATCH_SIZE; it still has exactly one definition, in S8-1.
    """
    part = bc.partition_by_transport(pending_recency_sorted, channel=channel,
                                     inline_budget=session_budget,
                                     consumed=probe_consumed)
    admitted, carried = part['auto'], part['deferred_for_context']
    oversize = [p for p in part['upload'] if (p.get('fileSize') or 0) > bc.DRIVE_CAP]
    print(f"\n  TRANSPORT PLAN  (channel: {part['channel']})")
    if part['channel'] == 'inline':
        # FIRST LINE, ALWAYS. The plan is not readable without knowing what was spent
        # before it was computed, and a probe reported after the admission count reads
        # as trivia rather than as the reason the count is what it is.
        print(f"    Probe consumed      : {part['consumed']:,} of {session_budget:,} "
              f"chars this session — EC-P40, EC-P36 double charge applies")
    print(f"    Pending this corpus : {len(pending_recency_sorted)} paper(s)")
    print(f"    Drive lane, session : {len(admitted)} paper(s) fetch automatically")
    if part['channel'] == 'direct':
        print(f"    Context cost        : 0 — python fetched the bytes itself over "
              f"container egress; nothing crossed the turn (EC-P43)")
    if part['channel'] == 'inline':
        print(f"    Context cost        : {part['inline_chars']:,} of "
              f"{part['effective_budget']:,} chars remaining after the probe "
              f"(bc.INLINE_BUDGET_CHARS // 2 — charged twice, EC-P36)")
        print(f"    Carried to later    : {len(carried)} paper(s) deferred FOR CONTEXT, "
              f"not for size — EC-P36/EC-X9")
    if part['channel'] == 'inline' and not admitted:
        # FIX F / G-9. `Sessions needed: ~0` while 22 papers pend is not merely wrong,
        # it is inverted in meaning, and the v2.39 changelog records what that does:
        # "a gate that cannot fire correctly trains operators to ignore gates."
        _cheapest = min(pending_recency_sorted,
                        key=lambda q: q.get('fileSize') or 0, default=None)
        print("\n  ! TRANSPORT INFEASIBLE THIS SESSION (EC-P37 upload-lane fallback)")
        print(f"    Session budget      : {session_budget:,} chars")
        print(f"    Already consumed    : {part['consumed']:,} chars")
        print(f"    Remaining           : {part['effective_budget']:,} chars")
        if _cheapest is not None:
            print(f"    Cheapest pending    : {_cheapest.get('name')} "
                  f"({bc.base64_cost_chars(_cheapest.get('fileSize')):,} chars)")
        print("    No paper fits this session's remaining budget. Per EC-P37 the upload")
        print("    lane is the fallback for a paper that cannot fit even ONE session.")
        print("    PYQCompress is NOT the remedy — these papers are far under DRIVE_CAP.")
        print("    If this is a fresh chat and the number above is still zero, the direct")
        print("    egress lane (EC-P43) is the fix: share the Drive folder as 'Anyone")
        print("    with the link' and allow drive.google.com in the container egress.")
    elif part['channel'] == 'inline':
        sessions = -(-len(pending_recency_sorted) // max(1, len(admitted)))
        print(f"    Sessions needed     : ~{sessions} — continue via Option B in a "
              f"FRESH chat, which resets the budget (EC-P37). These papers are NOT "
              f"manual uploads.")
    if oversize:
        plan = bc.upload_batch_plan(len(oversize), batch_size)
        print(f"    Upload lane         : {len(oversize)} paper(s) exceed the "
              f"{bc.DRIVE_CAP:,}-byte connector cap — chat accepts "
              f"{bc.CHAT_FILE_LIMIT} files per conversation, so "
              f"{plan['chats_needed']} chat session(s).")
        print(f"    Permanent fix for those: run PYQCompress on them once and replace "
              f"them in Drive.")
    # P4e — PYQCompress is the remedy for SIZE and for nothing else. On this GAP the
    # papers are 40-49 KB against a 10 MiB cap, 213x under; recommending compression
    # for a channel or context deferral sends the operator to do work that cannot
    # help. Never print it under EC-P35/EC-P36 deferrals.
    return part


def acquire_paper(paper_ref, drive_payloads, resolver, work_dir, needs_upload):
    """S8-1 batch-loop acquisition. Returns a local path, or None -> upload lane.

    THIS IS THE ACQUISITION CONTRACT AND IT LIVES IN A ```python FENCE ON PURPOSE.
    Every AST check in the repo skips a fence that does not compile; the CLASS T
    stubs of this very file sat in one until v2.50.0, which is why C6 reported zero
    findings against two live violations for the whole life of the defect.

    `resolver` performs no tool call — it is a lookup over payloads PHASE A already
    materialised — so this function raises no NameError and cannot reach the
    connector. Every failure arrives as TransportFallback and degrades to the upload
    lane; a transport failure is NEVER fatal to the run.
    """
    if paper_ref['source'] != 'gdrive':
        return paper_ref['path']
    try:
        return corpus_io.fetch_drive_docx(resolver, paper_ref, work_dir)
    except corpus_io.TransportFallback as exc:
        print(f"    ! Drive fetch unavailable — {exc}")
        print(f"    → routing to upload lane: {paper_ref['name']}")
        needs_upload.append(paper_ref)
        return None


def read_transport_verdict(progress):
    """EC-X5 / EC-X7 — reuse a recorded channel; probe only when there is none.

    Returns the recorded verdict dict, or None when this is a fresh corpus or a
    pre-patch progress file. A pre-patch file is VALID INPUT and is never discarded:
    the absent key simply means "probe as if fresh, then record".
    """
    return (progress.get('_meta') or {}).get('_transport')


def record_transport(progress, verdict, admitted, carried, oversize):
    """P4b — persist the verdict in _meta so a resumed session cannot re-decide.

    Step 5 is 8 sessions minimum on a 22-paper corpus. Without this, every session
    re-decides transport from scratch and re-probes, paying one paper's context each
    time. _meta is already serialised by save_progress and load_progress already
    selects the most-advanced copy by _meta.papers_processed, so this needs no new
    handling anywhere.
    """
    meta = progress.setdefault('_meta', {})
    prev = meta.get('_transport') or {}
    if prev.get('channel') and prev['channel'] != verdict['channel']:
        # EC-P38 / EC-X6 — a transition is legitimate (a resumed session may be on a
        # different deployment) but it is NEVER silent.
        print(f"  ! TRANSPORT CHANNEL CHANGED: {prev['channel']} -> "
              f"{verdict['channel']}. Recorded; continuing.")
    prev_log = prev.get('session_log') or []
    meta['_transport'] = {
        'channel': verdict['channel'],
        'probe_paper': verdict.get('probe_paper'),
        'session_budget': SESSION_INLINE_BUDGET,
        # G-8. RENAMED from 'papers_admitted' in v2.51.0. This field is written BEFORE
        # the acquisition loop runs, so it is a PLAN and never a result — in the
        # reference incident it recorded the 2026 paper as 'admitted' although that
        # paper was never fetched. No corruption followed, because run_batch_loop skips
        # on _meta.papers_processed which save_progress writes per paper, but a forecast
        # named as a fact is a trap for the next reader and for every gap investigation.
        'papers_planned': [p['id'] for p in admitted],
        # Readers MUST tolerate the old key for one release (EC-P38: a pre-patch
        # progress file is VALID INPUT and is never discarded). Read it as
        #     planned = t.get('papers_planned', t.get('papers_admitted', []))
        'deferred_context': [p['id'] for p in carried],
        'deferred_size': [p['id'] for p in oversize],
        'session_log': prev_log,
    }
    return meta['_transport']


def log_session(progress, session_index, spec_read_mode, probe_run, chars_consumed,
                papers_fetched, papers_processed, ended_at):
    """Append what this session ACTUALLY did. Additive; a pre-patch file stays valid.

    GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / G-8. Nothing recorded whether the probe
    ran, how many characters were really consumed, whether the spec was read in full or
    reduced, or whether the session ended at a batch boundary or at exhaustion. A
    resumed session — and every future gap investigation — was blind to all of it, which
    is why reconstructing the reference incident required the chat transcript rather
    than the artefact the step itself produces.

    `ended_at` is one of: 'batch_boundary', 'corpus_complete', 'session_exhausted'.
    """
    import datetime as _dt
    t = progress.setdefault('_meta', {}).setdefault('_transport', {})
    t.setdefault('session_log', []).append({
        'session_index': session_index,
        'started_utc': _dt.datetime.now(_dt.timezone.utc).isoformat(),
        'spec_read_mode': spec_read_mode,        # 'full' | 'reduced'  (see §S8-0b)
        'probe_run': bool(probe_run),
        'chars_consumed': int(chars_consumed or 0),
        'papers_fetched': list(papers_fetched or []),
        'papers_processed': list(papers_processed or []),
        'ended_at': ended_at,
    })
    return t['session_log']
```

### S8-0b — SESSION CLASS AND READ SET (runs at STEP 0, before any spec is read)

```
GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / G-1, G-4. Framework_PYQCore EC-P42.

THE DEFECT THIS CLOSES. SKILL Rule 2 mandates reading every routed .md IN FULL before
any work. For trigger PYQExtract that is this file (8,850 lines / 504,240 B) plus
Framework_DeliveryFooter.md (929 / 52,594): 556,834 B, ~139,208 tokens, >=36 view
calls, MANDATORY, every session. In the reference incident 40 of session 1's 50 tool
calls and 63% of the context window were spent before the first paper was touched, and
the step stalled immediately before its first productive operation. Over a 22-session
run that is ~3.06M tokens spent re-reading a file that is byte-identical every time and
whose sha256 bootstrap.py has already verified.

THE AXIS IS FINAL vs NON-FINAL. IT IS NOT FRESH vs RESUME.
A session executes the same code whether it is session 1 or session 5. What decides
which sections it reaches is whether it will CLOSE THE BOOKS. Routing on FRESH/RESUME
would leave session 1 of every one of the ~200 exams exactly as broken as the incident.

  NON-FINAL  papers_remaining > BATCH_SIZE
             This session mathematically cannot clear the corpus, so it can never
             enter run_synthesise(), §1-6's coverage check, QV, the summary format or
             the schema/xlsx writers.
             READ: §1 (S1-1, S1-2 and the resume load only), §2, §3, §4, §7, §8, §11
                   + Framework_DeliveryFooter §2, §2A, §3, §4, §5
             DO NOT READ: the header changelog block, §1-6, §5, §6, §9, §10, §12–§16
             Measured read set: 232,228 B, ~58,000 tok — 47% of the file.

  FINAL      papers_remaining <= BATCH_SIZE, OR mode is --synthesise ALL,
             --synthesise [S], or --status
             READ EVERYTHING. NO EXCEPTION.
             Synthesis, QV and every writer run in this session, and a reduced read of
             them is exactly the "paraphrased spec" failure the v2.39 changelog
             documents: five sessions paraphrased the spec and silently repaired bugs;
             the one session that executed the fences verbatim found a P0 no other
             session hit.

ESCALATION IS MANDATORY AND ONE-WAY.
A session that begins NON-FINAL and discovers mid-run that it has cleared the corpus
MUST read §1-6, §5, §6, §10, §12–§16 BEFORE run_synthesise() is entered. It may never
synthesise, never run QV, and never write section_rules.md from a reduced read. There
is no reverse direction: FINAL never downgrades to NON-FINAL.

HOW TO DECIDE IT — AT STEP 0, BEFORE READING ANYTHING.
The count comes from the progress file, which is small and is not a spec:
    papers_remaining = len(all corpus papers) - len(_meta.papers_processed)
`bootstrap.py --trigger PYQExtract --progress <analysis_progress.json>` prints the
class, the byte/token/call cost of each read set, and the exact line ranges. When no
progress file exists the corpus has not been enumerated yet, so the count is unknown;
decide the class immediately after PHASE A / A1b, which is the first moment it is
knowable, and read the NON-FINAL set until then.
A stale project copy of analysis_progress.json is the v2.39 GAP-H scenario: decide from
the copy load_progress() actually selects (most advanced by papers_processed), never
the first one found.

HOW TO READ IT — THE STRIDE MATTERS AS MUCH AS THE SET.
Measured in this container: the view tool truncates output above ~16,000 characters
INCLUDING explicitly ranged reads — the incident's first call, view [1,700], returned
"< truncated lines 120-581 >" and cost three further calls to cover one 700-line
window. A bash heredoc returned 188,024 characters intact in a single call.
Read spec ranges with `sed -n 'START,ENDp' <file>` in bash. The NON-FINAL set is ~2
calls; the FINAL set is ~4. The same content through view is 32-36. Context cost is
identical either way — only the CALL COUNT changes, and tool calls are the resource
that ran out first in the reference incident.

Line ranges are GENERATED into SPEC_SECTIONS.json from this file's own '## §' and
'### S' headers and hash-tracked in MANIFEST.json. They are NEVER hand-maintained here:
a hand-copied line number is a second definition of the file's own structure and will
drift on the first edit that adds a paragraph.

WHAT THIS SECTION DOES NOT DO. It does not shrink the defect narrative, which stays in
the repo unchanged — the v2.39 record proves it is load-bearing for editors. It moves
the EDITORIAL record off the EXECUTION path; it does not delete it. It also does not
change one byte of what any session WRITES: the artefacts are identical, so no exam
re-runs any step because of this section.
```

### S8-1 — Batch design

```
★★★ CRITICAL RULE — BATCH SIZE = 3 IS A CEILING, NOT A FLOOR ★★★

BATCH_SIZE = 3  # MAXIMUM papers per batch — NON-NEGOTIABLE AS A MAXIMUM.
                # Cannot be raised by any instruction.

Processing MORE than 3 papers without pausing for user confirmation is STRICTLY
PROHIBITED — unchanged. Analysing all files in one go without batching is STRICTLY
PROHIBITED. No user instruction, no efficiency argument, no time pressure overrides
that ceiling.

Processing FEWER than 3 is NORMAL AND IS NOT A VIOLATION. The batch is

    batch = min(BATCH_SIZE, len(admitted_this_session))

GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / G-6. This paragraph is new because the old
wording read as a FLOOR ("Processing 3 papers together in one go is MANDATORY",
"MANDATORY AFTER EVERY BATCH OF 3") while Framework_PYQCore EC-P37 had already settled
the opposite and said so explicitly. A model or an operator reading only this file
concluded that a 1-paper batch was a spec violation, and then either stalled asking for
clarification or "fixed" it by widening the context budget — which EC-P37 forbids in
terms, because it trades a longer run for a mid-batch context stall that the per-paper
save survives but the operator cannot interpret.

WHY A SESSION CAN ADMIT FEWER THAN 3 (Framework_PYQCore EC-P36/EC-P37):
  channel 'direct' — payloads never cross the turn. Batch is 3 again. This is the
                     normal case once the direct egress lane is available (EC-P43).
  channel 'spill'  — payloads land on disk. Batch is 3 again.
  channel 'inline' — the Drive lane is bounded by CONTEXT, not by DRIVE_CAP. Measured
                     on IIT_JAM_MATHEMATICS one 45-50 KB paper costs ~63,500 inbound
                     characters and is charged twice, so a session commonly admits ONE
                     paper. The run simply takes more sessions. That is the designed
                     behaviour, not a degraded one.
A final batch of 1 or 2 remaining papers has always been legal and is unchanged.
`admitted == []` is not a batch at all — §S8-0's TRANSPORT INFEASIBLE block reports it
and the session ends without processing, having spent nothing it cannot account for.

Why this rule is critical:
  1. Each batch delivers an incremental analysis_progress.json — user has a safe restore point.
  2. User can review progress after every 3 papers and catch errors early.
  3. Prevents session timeouts from losing all work on large paper sets
   (large exams with many years × shifts can easily exceed 100 papers).
  4. Ensures the user is always in control and can stop/resume at any point.

MANDATORY AFTER EVERY BATCH (of 1, 2 or 3 — the list below is unchanged):
  1. Save updated progress to analysis_progress.json
  2. Deliver analysis_progress.json as downloadable chat file (present_files)
  3. Print batch summary (papers processed, cumulative count, subtopic coverage)
  4. Show Options A/B (say "continue" OR download+upload+fresh chat)
  5. WAIT for user confirmation — do NOT auto-proceed under any circumstances

ACCEPTED CONTINUE SIGNALS: "continue" / "go" / "next" / "ok" / "proceed" / "yes"
PROHIBITED: auto-proceeding without user confirmation, even if user said "process all" earlier.
  If user says "process all X papers at once" → REFUSE. Reply:
    "Processing all papers at once is strictly prohibited. I will process 3 papers per batch
     and ask for your confirmation after each batch. This ensures progress is saved safely
     and you stay in control. Say 'continue' after each batch to proceed."

Processing order: latest year first → latest date within year first → session ascending.
  e.g. latest year's session 1 → session 2 → session 3 → prior date session 1 → ...
                    → prior year → ... → earliest year last
  (session = Shift/Slot/Phase/Paper/Session per exam_config.json session_keyword)
Rationale: if processing stops early, section_rules.md reflects the most recent
  exam patterns — exactly what Step 7 needs to generate up-to-date questions.

After ALL papers are processed (last batch):
  1. Save final progress
  2. Enforce minimum year coverage check (§1-6) — HALT if not met
  3. Auto-run synthesis immediately
  4. Run QV-1 through QV-16 (plus QV-5b)
  5. Deliver section_rules.md + analysis_progress.json + analysis_summary.md
     as downloadable chat files via present_files (no Drive upload)
  6. No separate session needed

Session flow:
  Session 1: STEP 0 decides the SESSION CLASS and the READ SET before any spec is read
             (§S8-0b) → PHASE A (S8-0), IN THIS ORDER:
               A1  the MODEL lists the Drive folder in its own turns, keeps every RAW
                   page, then acquire_listing() writes and ASSERTS the cache against an
                   independently declared observed_count (HARD STOP on a short listing,
                   EC-P41) and prints the year span and any gaps
               A1b collect_corpus_files() → sort_papers_recency_first()
                   THE SORT COMES BEFORE THE PROBE. It did not in v2.50.0, and it must
                   now: under P4f the probe paper IS admitted[0], which does not exist
                   until the recency sort has run. EC-X21 already required the sort
                   before the PARTITION; P4f moves the same requirement earlier still.
               A0  probe_transport() → corpus_io.probe_direct_egress() on the first
                   recency-sorted paper under DRIVE_CAP. Success → channel 'direct',
                   probe_consumed 0, nothing crossed the turn, whole corpus admissible
                   (EC-P43). Failure is an ORDINARY state and falls through to A2.
                   Skipped entirely when _meta._transport.channel is recorded (EC-X5)
                   or the mode is --status / --synthesise (EC-X14).
               A2  connector CHANNEL PROBE — only if A0 failed — on admitted[0], NOT
                   the smallest (P4f) → probe_drive_channel() PROVES it decodes
               A3  plan_transport(..., probe_consumed=...) PRINTS the plan. The probe
                   is a SPENDER and is charged even when it failed (EC-P40). When
                   nothing is admitted it prints TRANSPORT INFEASIBLE and NEVER a
                   sessions estimate computed from an empty set.
               A4  the MODEL downloads the REMAINING admitted payloads — the probe
                   payload is already paper 1 — and passes them ALL to run_batch_loop
                   as drive_payloads
             → processes min(BATCH_SIZE, len(admitted)) papers, latest year first.
               That is commonly ONE paper on an inline channel and exactly 3 on a
               'direct' or 'spill' channel: BATCH_SIZE is a CEILING, not a floor
               (S8-1, EC-P37). A 1-paper batch is NOT a spec violation.
             → record_transport() persists the verdict → log_session() records what
               this session ACTUALLY consumed → delivers progress.json → Options A/B

             The download step is NOT optional and NOT implicit. Until v2.50.0 this
             line read simply "reads Drive folder → sorts → processes", with no step
             in which payloads were materialised — so run_batch_loop's drive_payloads
             parameter had no producer anywhere in the spec, defaulted to {}, and the
             entire corpus routed to manual upload on every run of every exam.
  Session 2 option A: user says "continue" in same session → processes #4-6 → shows Options A/B
  Session 2 option B: user downloads progress.json from chat → uploads to [ExamCode]
             project knowledge (replacing prior version) → opens fresh chat →
             types: PYQExtract PYQ: <<same Drive link>> → processes #4-6
  ...
  Session N: processes last batch → §1-6 coverage check → synthesises → delivers final outputs
```

### S8-2 — Main execution loop

```python
BATCH_SIZE = 3

def sort_papers_recency_first(paper_list):
    """
    Sort PYQ papers: latest year first, then latest date within year first,
    then session number ascending within same date (session 1 before session 2).

    Extracts year and date from filename using the common naming convention:
      [ExamCode]_DD-Mon-YYYY_<session_keyword>-N.docx
    session_keyword is read from exam_config.json (Shift/Slot/Phase/Paper/Session).

    For filenames without a recognizable date: sorted last, alphabetically.

    Examples (sorted order, using session_keyword='Shift'):
      [ExamCode]_26-Sep-2025_Shift-1 → year=2025, date=2025-09-26, session=1 (first)
      [ExamCode]_26-Sep-2025_Shift-2 → year=2025, date=2025-09-26, session=2
      [ExamCode]_12-Sep-2025_Shift-1 → year=2025, date=2025-09-12, session=1
    Examples (using session_keyword='Slot'):
      [ExamCode]_09-Sep-2024_Slot-1  → year=2024, date=2024-09-09, session=1
      [ExamCode]_13-Aug-2021_Slot-2  → year=2021, date=2021-08-13, session=2
    """
    MONTH_MAP = {
        'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
        'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12
    }

    def sort_key(paper):
        name = paper['name']
        # Match: DD-Mon-YYYY and Shift-N
        date_m  = re.search(r'(\d{2})-([A-Za-z]{3})-(\d{4})', name)
        # v2.16 RIGID-1: uses SESSION_RE (dynamic from exam_config.json session_keyword)
        shift_m = SESSION_RE.search(name)

        if date_m:
            day   = int(date_m.group(1))
            month = MONTH_MAP.get(date_m.group(2).lower(), 0)
            year  = int(date_m.group(3))
        else:
            # No date found — try year-only
            year_m = re.search(r'(20\d{2})', name)
            year  = int(year_m.group(1)) if year_m else 0
            month = 0
            day   = 0

        shift = int(shift_m.group(1)) if shift_m else 99

        # Sort key: year DESC, month DESC, day DESC, shift ASC
        # Negate year/month/day for descending; shift stays ascending
        return (-year, -month, -day, shift)

    return sorted(paper_list, key=sort_key)


def deliver_batch_summary(batch, progress, batch_num, papers_done, total_all, exam_code):
    """Print per-batch delivery summary to chat. Called after EVERY batch.

    The batch is min(BATCH_SIZE, len(admitted_this_session)) — commonly ONE on an
    inline channel (S8-1, EC-P37). Never assume three.
    """
    meta       = progress.get('_meta', {})
    total_qs   = meta.get('total_questions', 0)
    n_observed = sum(1 for k,v in progress.items() if isinstance(k,tuple) and len(v)>=3)
    n_inferred = sum(1 for k,v in progress.items() if isinstance(k,tuple) and 1<=len(v)<3)
    n_omml_fail = sum(1 for k,qs in progress.items()
                      if isinstance(k,tuple)
                      for q in qs if q.get('omml_failed'))
    n_unclear   = sum(1 for k,qs in progress.items()
                      if isinstance(k,tuple)
                      for q in qs if q.get('image_clarity')=='unclear')

    print(f"\n=== Batch {batch_num} complete ===")
    for p in batch:
        name = p['name']
        yr   = extract_year_from_filename(name) or '?'
        sh   = extract_shift_from_filename(name, session_re=SESSION_RE)
        print(f"  ✓ {name} | {yr} {sh}")
    print(f"\n Cumulative : {papers_done} / {total_all} papers")
    print(f" Subtopics  : {n_observed} observed | {n_inferred} sparse")
    print(f" Total Qs   : {total_qs}")
    if n_omml_fail: print(f" OMML issues: {n_omml_fail} questions with failed OMML")
    if n_unclear:   print(f" Unclear imgs: {n_unclear} figural images unclear")
    print("========================")
    # Deliver progress.json as downloadable chat file after every batch
    progress_path = f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json'
    present_files([progress_path])
    # present_files makes the file downloadable in chat (Claude tool).

def run_batch_loop(pyq_doc_paths, exam_code, time_per_q, marks_per_q,
                   options_count, multi_select, progress,
                   coverage_mode='mandatory_5yr', recent_5_years=None,
                   available_years=None, drive_payloads=None):
    """
    Core loop: process papers in batches of BATCH_SIZE (always 3 — non-negotiable).
    pyq_doc_paths: list of dicts — {source: 'gdrive'|'local', id/path, name}
    Papers already in progress._meta.papers_processed are skipped.
    Processing order: latest year first, then latest date, then shift ascending.
    coverage_mode, recent_5_years, available_years: passed from §1-6 check.
    ★ NEVER process more than BATCH_SIZE papers without pausing for user confirmation.
    """
    import os

    # v2.37 CLASS T BRIDGE. drive_payloads is {file_id: payload_or_spill_path},
    # materialised by the MODEL before this function is called (see the GOOGLE DRIVE
    # section). The resolver performs NO tool call — it looks up a result that already
    # exists, so it is ordinary reachable python.
    #
    # A missing entry raises TransportFallback, which corpus_io already routes to the
    # UPLOAD LANE. That is the correct degradation and it is LOUD: the operator is
    # asked for the paper by name. Nothing halts.
    #
    # v2.50.0 (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION). This line used to read
    # `drive_payloads = drive_payloads or {}`. That default is the whole defect: the
    # parameter had NO PRODUCER anywhere in this spec — S8-1's session flow never
    # mentioned it, PHASE A was described only in a prose comment with no named
    # contract, and there is no call site to supply it — so it could only ever be {},
    # drive_resolver raised TransportFallback for EVERY paper, and the ENTIRE corpus
    # routed to manual upload on EVERY run of EVERY exam. An empty container behind a
    # correctly-injected resolver is invisible to C6 and to C7 alike; C9 now fails the
    # build for it.
    #
    # Fail loudly instead, exactly as v2.39 does for the vision_pending accumulator a
    # few hundred lines up — same failure shape, same remedy, same wording.
    if drive_payloads is None:
        raise RuntimeError(
            "run_batch_loop: drive_payloads not supplied. PHASE A (S8-0) must "
            "materialise the payload for every paper this session's transport plan "
            "admits, and pass them in as {file_id: payload_or_spill_path}. Defaulting "
            "to {} would silently route the entire corpus to the manual upload lane — "
            "the exact failure GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION removes. "
            "Pass {} EXPLICITLY if this session is intentionally upload-only.")

    def drive_resolver(file_id):
        if file_id not in drive_payloads:
            raise corpus_io.TransportFallback(
                f'no materialised Drive payload for {file_id} — the model must call '
                f'Google Drive:download_file_content in its own turn BEFORE '
                f'run_batch_loop() and pass the results in as drive_payloads')
        return drive_payloads[file_id]

    done_ids = set(progress.get('_meta', {}).get('papers_processed', []))

    # Sort ALL papers recency-first, then filter out already-done ones
    # Sorting before filtering preserves the correct order for pending papers
    all_sorted = sort_papers_recency_first(pyq_doc_paths)
    pending    = [p for p in all_sorted if make_paper_id(p['name']) not in done_ids]

    total_done = len(done_ids)
    total_all  = total_done + len(pending)

    if not pending:
        print(f"All {total_all} paper(s) already processed. Running synthesis.")
        run_synthesise(exam_code, progress,
                       coverage_mode=coverage_mode,
                       recent_5_years=recent_5_years,
                       available_years=available_years)
        return

    print(f"Papers done: {total_done} / {total_all}. Pending this session: {len(pending)}")

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_start : batch_start + BATCH_SIZE]
        batch_num = (total_done // BATCH_SIZE) + (batch_start // BATCH_SIZE) + 1

        print(f"\n=== Batch {batch_num}: processing {len(batch)} paper(s) ===")

        # v2.37: the IMG-6 callback probe is GONE (S3-1c). It could not work: a
        # callback cannot make a tool call from inside python, so it defaulted to
        # returning '' and reported EVERY session blind. Liveness is now DERIVED from
        # Phase C, which costs nothing extra and cannot drift from the thing it
        # measures. Phase A runs per paper below; Phase B + C run at the batch
        # boundary this loop already stops at, so no new interruption is introduced.

        needs_upload = []          # papers this batch could not be fetched from Drive

        # v2.39 (GAP-2026-07-27-B). Phase A candidates accumulate ACROSS the batch and
        # the queue is built ONCE, below, immediately before Phase B. Building it
        # per paper overwrote vision_queue.json and vision_sheet_NNN.png — both fixed
        # filenames — so only the batch's last paper ever reached Phase B.
        vision_pending = []

        for paper_ref in batch:
            paper_id  = make_paper_id(paper_ref['name'])
            print(f"  Processing: {paper_ref['name']}")

            # ── Fetch (v2.29; v2.50.0 delegates to the S8-0 contract) ────────
            # NEVER call the connector unguarded, and never from python at all.
            # acquire_paper() is defined in S8-0 in a ```python fence the CI can
            # parse — v2.49.1 carried this code inline here and an equivalent copy of
            # it lived in a fence that did not compile, so no static check in the repo
            # could read the step's single most load-bearing instruction.
            # EVERY failure — size, permission, network, malformed envelope, unknown —
            # degrades to the UPLOAD LANE. Correctness depends on the fallback being
            # taken, not on the predicted partition being right.
            local_path = acquire_paper(paper_ref, drive_payloads, drive_resolver,
                                       DRIVE_WORKDIR, needs_upload)
            if local_path is None:
                continue

            process_pyq_paper(local_path, paper_id, exam_code,
                               time_per_q, marks_per_q, options_count,
                               multi_select, progress,
                               expected_size=paper_ref.get('fileSize'),
                               vision_pending=vision_pending, session_re=SESSION_RE)

            # ── Persist after EVERY paper (v2.29) ────────────────────────────
            # The durability unit is the PAPER, not the batch. Previously save_progress
            # ran only after the inner loop finished, so an exception on paper 3 skipped
            # it entirely and papers 1 and 2 — already processed in memory — were
            # discarded with no trace, showing as never-processed in the progress file.
            # BATCH_SIZE stays 3: batching is the user-facing PACING unit and is
            # unchanged. This makes a partial batch safe to resume.
            save_progress(progress, exam_code)

        # ── Upload lane (v2.29) ─────────────────────────────────────────────
        # Ask for exactly the papers Drive could not supply. Requested BY NAME so the
        # user never has to guess, and matched back by canonical identity because the
        # browser appends " (1)" whenever the original is already in their Downloads
        # folder — which happens on every remediation round trip.
        if needs_upload:
            plan = bc.upload_batch_plan(len(needs_upload), BATCH_SIZE)
            print(f"\n  {len(needs_upload)} paper(s) in this batch exceed the "
                  f"{bc.DRIVE_CAP:,}-byte Drive download cap and must be uploaded to chat:")
            for p in needs_upload:
                sz = p.get('fileSize')
                print(f"    - {p['name']}" + (f"  ({sz:,} bytes)" if sz else ""))
            print(f"  Chat accepts {bc.CHAT_FILE_LIMIT} files per conversation "
                  f"({plan['papers_per_chat']} papers across {plan['batches_per_chat']} "
                  f"batches at BATCH_SIZE={BATCH_SIZE}).")
            print(f"  Permanent fix: run  PYQCompress  on these papers once and replace "
                  f"them in Drive — they then fetch automatically for every future run "
                  f"of Steps 2b, 4 and 5.")
            expected = [bc.canonical_paper_key(p['name']) for p in needs_upload]
            found = corpus_io.resolve_uploaded_papers(expected)
            for p in needs_upload:
                key = bc.canonical_paper_key(p['name'])
                if key not in found['matched']:
                    continue
                # Upload lane: the Drive-reported fileSize describes the Drive copy,
                # not the uploaded one, so IMG-1 measures the file actually on disk.
                _up = found['matched'][key]
                process_pyq_paper(_up, make_paper_id(p['name']),
                                  exam_code, time_per_q, marks_per_q, options_count,
                                  multi_select, progress,
                                  expected_size=os.path.getsize(_up),
                                  vision_pending=vision_pending, session_re=SESSION_RE)
                save_progress(progress, exam_code)        # per-paper, as above
            if found['unexpected']:
                print(f"  ! Ignored {len(found['unexpected'])} unexpected upload(s) — "
                      f"only the papers named above are processed.")
            still_missing = [p['name'] for p in needs_upload
                             if bc.canonical_paper_key(p['name']) not in found['matched']]
            if still_missing:
                print(f"  Awaiting upload: {', '.join(still_missing)}")

        # ══ PHASE B + PHASE C — the batch boundary (v2.37, GAP-2026-07-26-003) ══
        # This is where the CLASS T work happens, and it happens HERE because the run
        # already stops here under the BATCH STOP law below. No new interruption is
        # introduced and nothing halts.
        #
        # PHASE B is performed BY THE MODEL, IN THIS TURN, following the prose protocol
        # in S4-2b: view() each contact sheet in VISION_WORKDIR, record one observation
        # per labelled cell, and write them with corpus_io.write_vision_observations().
        # It is NOT a function call and must never be written as one.
        #
        # PHASE C then folds whatever came back onto the questions. If Phase B was
        # skipped, produced nothing, or produced a malformed file, this still runs, the
        # figures record 'vision_unavailable', QV-14 FAILs and the footer goes amber.
        # The run COMPLETES either way.
        #
        # ── PHASE A, ONCE PER BATCH (v2.39, GAP-2026-07-27-B) ───────────────────
        # build_vision_queue() is idempotent as of corpus_io v1.9: it unions the items
        # passed here with any queue already on disk, keyed by (paper_id, q_num), so a
        # RESUMED session does not orphan the sheets a prior session already wrote.
        # Both halves of the fix are required — hoisting alone still loses prior
        # sessions, and idempotence alone still loses papers 1..N-1 within one batch.
        vision_queue = corpus_io.build_vision_queue(
            vision_pending, VISION_WORKDIR, per_sheet=VISION_PER_SHEET)
        n_vision = len(vision_queue['items'])
        if n_vision:
            print(f"    PHASE A: {n_vision} figural question(s) queued across "
                  f"{vision_queue['stats']['sheets']} contact sheet(s) in {VISION_WORKDIR}")
            print(f"      ({len(vision_pending)} accumulated this batch; the queue is a "
                  f"union with any items already on disk)")
            if vision_queue['stats']['unrenderable']:
                print(f"    note: {vision_queue['stats']['unrenderable']} figure(s) could not "
                      f"be rasterised (vector/corrupt) — queued and reported, never dropped")
            if vision_queue['degraded']:
                print("    note: Pillow absent — degraded to one view() per figure (EC-V9)")
            if vision_queue['stats'].get('tag_generation_changed'):
                # EC-V12. A paper_id hash collision widened the tag code for the WHOLE
                # queue, so every tag changed and any observation written under the
                # previous generation can no longer be matched by Phase C. Loud, because
                # the alternative is Phase C reporting already-viewed figures as simply
                # unobserved and the operator re-viewing sheets that were already done.
                print(f"    ! TAG GENERATION CHANGED "
                      f"(width {vision_queue['stats'].get('prior_tag_width')} -> "
                      f"{vision_queue['tag_width']}). A paper_id hash collision forced "
                      f"a re-tag of the whole queue.")
                print(f"      Observations recorded under the previous generation cannot "
                      f"be matched and will report as unobserved. Re-run PHASE B over "
                      f"every sheet in {VISION_WORKDIR}; QV-14 reports the true coverage.")

        vision_stats = apply_vision_observations(progress)
        progress.setdefault('_meta', {})['vision'] = vision_stats
        if vision_stats['vision_status'] == 'unavailable' and vision_stats['queued']:
            print(f"    ! VISION UNAVAILABLE — {vision_stats['queued']} figure(s) queued, "
                  f"0 observed. Processing CONTINUES and the run will complete.")
            print(f"      QV-14 will FAIL and the step footer will render amber.")
            print(f"      Remedy: a fresh session re-running PHASE B ONLY — the queue "
                  f"and sheets are already on disk at {VISION_WORKDIR}.")
        elif vision_stats['vision_status'] == 'partial':
            print(f"    ! {vision_stats['missing']} queued figure(s) were not observed. "
                  f"Re-running Phase B is idempotent and fills only the gaps.")

        # Save and deliver after each batch (redundant flush — the per-paper saves above
        # are the durability guarantee; this keeps the delivery contract unchanged)
        progress_path    = save_progress(progress, exam_code)
        papers_now_done  = len(progress.get('_meta',{}).get('papers_processed',[]))
        papers_remaining = total_all - papers_now_done

        deliver_batch_summary(batch, progress, batch_num, papers_now_done, total_all, exam_code)

        if papers_remaining == 0:
            print(f"\nAll {total_all} papers complete. Running synthesis now...")
            run_synthesise(exam_code, progress,
                           coverage_mode=coverage_mode,
                           recent_5_years=recent_5_years,
                           available_years=available_years)
            return

        # More papers remain — pause for user.
        # The for loop STOPS here after each batch (break).
        # Next batch only runs if user says 'continue' in same session,
        # OR user uploads progress.json and starts a fresh chat.
        print(f"\n{papers_remaining} paper(s) remaining.")
        print(f"Options:")
        print(f"  A) Say 'continue' to process the next batch now in this same session.")
        print(f"  B) Download analysis_progress.json above, then upload it to")
        print(f"     [ExamCode] project knowledge (replace prior version),")
        print(f"     open a fresh chat, and type:")
        print(f"     PYQExtract {exam_code}  PYQ: <<same Drive link>>")
        print(f"  Both options are valid. Progress is in memory — option A needs no upload.")

        # ══ BATCH STOP -- END THE RESPONSE ═══════════════════════
        # *** Write nothing more. Generate nothing more. ***
        # This is the same class of rule as PYQAnalyse S3-4a and
        # MockCreate MANDATE 1 STEP 6.
        # CROSS-FRAMEWORK FAILURE: PYQAnalyse SSC CGL Tier 2 --
        # Claude auto-advanced from Batch 1 to Batch 2 in the same
        # response because no "END THE RESPONSE" prose existed.
        # The Python `break` stops the loop but does NOT stop Claude
        # from writing content after the loop. This prose block does.
        break  # STOP after each batch — do not auto-proceed to next batch

def make_paper_id(filename):
    """Stable unique ID from filename (without extension)."""
    return os.path.splitext(os.path.basename(filename))[0]
```

### S8-3 — Batch delivery format

```
After each batch, Claude prints in chat. The ✓ list is VARIABLE-LENGTH — ONE line per
paper ACTUALLY processed, which is min(BATCH_SIZE, len(admitted_this_session)) and is
commonly 1 on an inline channel (S8-1, EC-P37). Three lines are the ceiling, never a
quota, and padding the list to three is a fabrication.

"=== Batch [N] complete ===
 Papers processed this batch:
   ✓ [filename_1] | [Y] S[N] | [N] Qs | [N] groups | [N] figural imgs
   [... one ✓ line per paper processed, 1 to BATCH_SIZE of them ...]

 Batch size this session: [N] of ceiling [BATCH_SIZE] (channel=[direct|spill|inline])
 Cumulative progress : [done] / [total] papers
 Subtopics with data: [N] observed | [N] inferred | [N] absent
 Total Qs accumulated: [N]

 Transport this batch: channel=[direct|spill|inline]
   fetched from Drive : [N]
   uploaded to chat   : [N]
   probe consumed     : [N] chars   (inline channel only — EC-P40)
   budget consumed    : [N] / [effective budget after probe] chars   (inline only)
   spec read mode     : [full|reduced]   (§S8-0b session class)

 Data quality snapshot:
   OMML issues   : [N] questions with failed OMML nodes (if any)
   Unclear images: [N] figural images too small/blurry to classify (if any)
 ========================"

Then present_files: [ExamCode]_analysis_progress.json
  (EXACTLY 1 file — S11-3 per-batch closed set. No other files.)

If more papers remain:
  (See S11-1 PART C for exact continue prompt text.)
  Options: say "continue" in same session, OR download progress.json and resume in fresh chat.
  Wait for user: "continue" / "go" / "next" are all valid.
  Claude does NOT auto-proceed — user confirms before each batch.
  *** After printing Options A/B: END THE RESPONSE. Write nothing more. ***

If this was the last batch:
  → auto-synthesise (see S8-4). No separate session needed.
```

### S8-4 — Auto-synthesise on completion (no separate final session)

```python

def write_analysis_summary(entries, progress, exam_code):
    """Write human-review audit trail to analysis_summary.md."""
    from datetime import datetime
    meta    = progress.get('_meta', {})
    n_pap   = len(meta.get('papers_processed',[]))
    n_qs    = meta.get('total_questions',0)
    years   = sorted(meta.get('years_processed',[]))
    out     = f'/mnt/user-data/outputs/{exam_code}_analysis_summary.md'

    lines = [
        f'# {exam_code} Analysis Summary',
        f'Generated: {datetime.now().isoformat()[:19]} | Papers: {n_pap} | Questions: {n_qs} | Years: {years}',
        '',
        '## HUMAN REVIEW REQUIRED',
        '',
        '### Inferred patterns (1-2 occurrences — verify):',
    ]
    for e in entries:
        for p in e.get('PYQ_STEM_PATTERNS',[]):
            if p.get('confidence')=='inferred':
                lines.append(f'  {e["subtopic"]} {p["id"]}: "{p["template"][:60]}" '
                             f'(seen {p["raw_count"]} times, years: {p.get("years",[])})')

    lines += ['', '### Deprecated patterns (absent from last 2 years):']
    for e in entries:
        for p in e.get('PYQ_STEM_PATTERNS',[]):
            if p.get('deprecated'):
                lines.append(f'  {e["subtopic"]} {p["id"]}: "{p["template"][:60]}" '
                             f'(last seen: {max(p.get("years",[0]))})')

    lines += ['', '### Absent subtopics (Zero-PYQ — no PYQ data — Step 7 uses training knowledge):',
              '### SYNC NOTE: Step 6 (Framework_Blueprint) calls these "Zero-PYQ" subtopics.',
              '### r_avg = 0.0 for all entries below. Step 6 places them in zero_pyq_rotation{}.']
    for e in entries:
        if e.get('observed_count',0)==0:
            lines.append(f'  {e["subtopic"]}')

    lines += ['', '### Figural vision analysis summary:']
    for e in entries:
        ia = e.get('PYQ_IMAGE_ANALYSIS')
        if ia:
            lines.append(f'  {e["subtopic"]}: {ia.get("images_analysed",0)} analysed, '
                        f'{ia.get("images_unclear",0)} unclear')

    lines += ['', '## STATISTICS',
              f'Total subtopics: {len(entries)}',
              f'Observed (>=3 Qs): {sum(1 for e in entries if e["observed_count"]>=3)}',
              f'Sparse   (1-2 Qs): {sum(1 for e in entries if 1<=e["observed_count"]<3)}',
              f'Absent   (0 Qs)  : {sum(1 for e in entries if e["observed_count"]==0)}',
              '',
              '### Top 10 subtopics by observed_count:']
    for e in sorted(entries, key=lambda x:-x['observed_count'])[:10]:
        lines.append(f'  {e["subtopic"]}: {e["observed_count"]} Qs')

    with open(out,'w',encoding='utf-8') as f: f.write('\n'.join(lines))
    print(f'Written: {out}')
    return out

def run_synthesise(exam_code, progress, coverage_mode='mandatory_5yr',
                    recent_5_years=None, available_years=None):
    """
    Called automatically when all papers are processed.
    Runs synthesis, QV checks, generates section_rules.md and summary.
    User never needs to type --synthesise separately.

    Enforces mandatory 5-year coverage rule (§1-6) before proceeding.
    coverage_mode   : 'mandatory_5yr' (standard) | 'no_pyq' | 'no_year_info'
    recent_5_years  : list of the most recent N years available (N = min(5, available))
    available_years : full sorted list of all years in Drive/uploads
    """
    # §1-6 MANDATORY 5-YEAR COVERAGE ENFORCEMENT
    processed_years = sorted(set(progress.get('_meta', {}).get('years_processed', [])),
                             reverse=True)

    # If called via --synthesise ALL (recent_5_years=None), reconstruct from progress.
    # We cannot re-scan Drive here (no pyq_doc_paths available), so derive
    # available_years from what was actually processed.
    _recent_5 = recent_5_years
    _avail    = available_years
    if coverage_mode == 'mandatory_5yr' and _recent_5 is None:
        # Reconstruct: assume available years == processed years (conservative)
        _avail    = sorted(processed_years, reverse=True)
        _recent_5 = _avail[:5]

    # Skip check for Scenario B (no PYQ) or no-year-info mode
    if coverage_mode in ('no_pyq', 'no_year_info'):
        pass  # No coverage check needed — proceed to synthesis
    elif coverage_mode == 'mandatory_5yr':
        n_required = min(5, len(_avail)) if _avail else 0
        missing = [y for y in (_recent_5 or []) if y not in processed_years]
        if len(processed_years) < n_required or missing:
            print("\n★ SYNTHESIS BLOCKED: 5-YEAR COVERAGE RULE NOT MET ★")
            print(f"  Required : {n_required} most recent year(s): {(_recent_5 or [])[:n_required]}")
            print(f"  Processed: {processed_years}")
            if missing: print(f"  Missing  : {sorted(missing, reverse=True)}")
            print("  ACTION   : Process papers from the missing year(s) before synthesising.")
            print("             This rule cannot be waived. No exception applies here.")
            return   # HALT — do not write section_rules.md

    print("\n=== Auto-synthesis starting ===")
    print("Building taxonomy from accumulated PYQ data...")

    # Build taxonomy from two sources (merged, Analysis docs win for names):
    # Source 1: progress keys (always available — built during extraction)
    taxonomy = {}
    for key in progress:
        if isinstance(key, tuple) and len(key) == 3:
            section, topic, subtopic = key
            taxonomy.setdefault(section, [])
            if not any(e['subtopic'] == subtopic for e in taxonomy[section]):
                taxonomy[section].append({'topic': topic, 'subtopic': subtopic})

    # Source 2: Analysis docs (if present in project/uploads — adds absent subtopics
    # that have no PYQ data, ensuring QV-1 can detect missing coverage correctly)
    #
    # v2.39 (GAP-2026-07-27-A). Three defects lived in these six lines:
    #   1. the append was unguarded  -> 126 of 134 ids emitted twice, QV-13 FAIL;
    #   2. the glob spans BOTH directories, and the documented operator workflow puts
    #      the same doc in both -> a THIRD copy of every overlapping subtopic;
    #   3. `except Exception: pass` swallowed the RuntimeError that the v2.31 lock gate
    #      raises for a SUPERSEDED Analysis doc. The gate was armed at line ~2200 and
    #      disarmed six lines later, so the one failure it exists to prevent — silently
    #      renaming the vocabulary of the whole pipeline — passed through unreported.
    renames = []
    _cand = []
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, '*.docx')):
            bn = os.path.basename(f).lower()
            if 'analysis' in bn or 'analyse' in bn:
                _cand.append(f)
    for f in _dedupe_analysis_docs(_cand):
        try:
            extract_taxonomy_from_analysis_doc(f, taxonomy, renames=renames)
        except RuntimeError:
            # v2.31 LOCK GATE — this doc is not the one PYQApprove approved.
            # MUST NOT be swallowed: Step 5 mints the subtopic_ids every later step
            # matches on, so proceeding renames the pipeline's vocabulary silently.
            raise
        except Exception as ex:
            # Any OTHER read failure stays non-fatal, as before — but is now VISIBLE.
            print(f"  WARN: Analysis doc unreadable, skipped: {os.path.basename(f)} — {ex}")

    # v2.39 decision (a): the doc won the topic name above; carry the rename into the
    # progress keys BEFORE the synthesis loop, whose lookup key includes topic. Without
    # this, a renamed topic orphans every question under it — silently.
    for line in apply_taxonomy_renames(progress, renames):
        print(line)
    if renames:
        print(f"Taxonomy renames applied from Analysis doc: {len(renames)}")

    # Synthesise every subtopic
    all_entries = []
    # v2.8: nat_allowed (PARAMETER 11) gates the NAT detection axis. Read once from _meta
    # (default False ⇒ answer_type always 'option' ⇒ non-NAT exams behave exactly as v2.7).
    _nat_allowed = bool(progress.get('_meta', {}).get('nat_allowed', False))
    for section, entries in taxonomy.items():
        for e in entries:
            key       = (section, e['topic'], e['subtopic'])
            questions = progress.get(key, [])
            figural   = None
            if any(q.get('image_role','none') != 'none' for q in questions):
                figural = aggregate_figural(questions, {})
            entry = synthesise_subtopic(section, e['topic'], e['subtopic'],
                                         questions, progress, figural_data=figural,
                                         nat_allowed=_nat_allowed)
            all_entries.append(entry)

    # ── v2.20 TAXONOMY SYNC (Fix A): ensure manifest covers COMPLETE vocabulary ──
    # After PYQ-based entries are built, synchronise with the exam's approved
    # taxonomy. Any taxonomy-defined subtopic NOT already in all_entries gets a
    # zero-PYQ scaffold entry appended. This makes the manifest COMPLETE by
    # construction — Step 6 can never encounter an unresolvable subtopic.
    print("\n--- Taxonomy sync (v2.20) ---")
    zero_pyq_scaffolds, sync_log = taxonomy_sync_entries(all_entries, exam_code)
    if zero_pyq_scaffolds:
        all_entries.extend(zero_pyq_scaffolds)
        # Also add to taxonomy dict so QV-1 coverage sees them
        for scaffold in zero_pyq_scaffolds:
            sec = scaffold['section']
            taxonomy.setdefault(sec, [])
            if not any(e['subtopic'] == scaffold['subtopic'] for e in taxonomy[sec]):
                taxonomy[sec].append({'topic': scaffold['topic'],
                                      'subtopic': scaffold['subtopic']})
    for line in sync_log:
        print(line)
    print(f"Taxonomy sync: {len(zero_pyq_scaffolds)} zero-PYQ scaffold entries added.")
    print(f"Total subtopics after sync: {len(all_entries)}")
    print("--- End taxonomy sync ---\n")

    # v2.24.5: AUTOMATIC zero-PYQ format inference. Runs on the full entry set (PYQ + scaffolds)
    # so same-topic siblings are visible; refines ONLY zero-PYQ entries in place (name keyword →
    # FIGURAL; unanimous sibling format inherited; ≥2/3 NAT/MSQ inherited) before ids/stamp/QV/
    # writers see them. No prompt — every change is logged for the audit trail.
    apply_zero_pyq_format_inference(all_entries)

    # ── v2.24.1 DERIVE-ONCE PIPELINE (§8-4 order): mint id → merges → stamp → QV ──
    # (subtopic_merges is keyed by subtopic_id, so ids MUST be minted before merging.)
    # subtopic_id is minted HERE (moved out of write_section_rules) so QV-13 and every
    # writer read the SAME id and the SAME stamped mechanic axes. stamp_mechanic_axes()
    # asserts form_key uniqueness before anything is written — a shared form_key can no
    # longer reach Step 6 as a silent, two-steps-later HALT.
    _stamp_meta = {'section_prefix_overrides':
                   (progress.get('_meta', {}) or {}).get('section_prefix_overrides', {})}
    # ── QV-13b (v2.39, GAP-2026-07-27-A) — DUPLICATE TAXONOMY KEY, PRE-MINT ─────
    # Runs BEFORE minting, deliberately. After minting, a duplicated (section, topic,
    # subtopic) surfaces as an opaque subtopic_id collision in QV-13, which sent six
    # sessions looking at mint_subtopic_ids() — the one function that was behaving
    # correctly. Attributing the failure to the MERGE, at the point the merge is still
    # visible, is the difference between a six-line fix and a six-session hunt.
    # HARD STOP: every id minted downstream keys the whole pipeline, and a duplicate
    # key means two entries are competing to define one subtopic.
    _keys = [(e['section'], e['topic'], e['subtopic']) for e in all_entries]
    if len(_keys) != len(set(_keys)):
        import collections as _c
        _dupes = [k for k, n in _c.Counter(_keys).items() if n > 1]
        print(f"\n★ QV-13b HARD STOP: {len(_dupes)} duplicate (section, topic, subtopic) "
              f"key(s) in the entry set, {len(_keys)} entries for {len(set(_keys))} "
              f"distinct subtopics.")
        print("  CAUSE: the taxonomy was CONCATENATED rather than MERGED — Source 1 "
              "(progress keys) and Source 2 (Analysis doc) each contributed the same "
              "subtopic, or one Analysis doc was read twice from two directories.")
        for k in _dupes[:5]:
            print(f"    {k}")
        if len(_dupes) > 5:
            print(f"    ... and {len(_dupes) - 5} more")
        print("  This is NOT a mint_subtopic_ids() fault. Do not renumber ids to "
              "work around it.")
        raise SystemExit("QV-13b: duplicate taxonomy keys — synthesis aborted before minting.")

    mint_subtopic_ids(all_entries, _stamp_meta)                    # ids first (merges join on them)
    all_entries = apply_subtopic_merges(all_entries, exam_code)    # D7 (no-op if none declared)
    stamp_mechanic_axes(all_entries, exam_code, _stamp_meta)

    # QV checks
    qv_results  = run_qv(all_entries, taxonomy, progress)
    qv_ok       = print_qv(qv_results)

    # ── S-SECMAP: DERIVE SECTION↔SUBJECT MAPPING AND UPDATE EXAM_CONFIG ──────
    # v2.24.9 GAP FIX (BUG 1 of 4). After classification completes, derive which
    # taxonomy Subjects appear in which OTS sections and write the mapping as
    # sections[].subjects in exam_config.json. This enables Step 6's resolver
    # (S2-1b) to handle cross-subject exams (e.g. IIT JAM, CSIR NET) where a
    # single Subject spans multiple OTS sections. Without this, S2-1b falls to
    # SEC-4 HARD STOP on any exam where section names ≠ manifest Subject names
    # AND there are multiple OTS sections.
    #
    # 3-stage rule:
    #   STAGE 1 (OBSERVE): for each (section, subject) pair in classified PYQ data,
    #     record which subjects appeared in which Q-ranges (sections).
    #   STAGE 2 (AUGMENT): cross-subject sections (≥2 subjects) pool all subjects
    #     and assign the union to every cross-subject section — covers sampling gaps.
    #   STAGE 3 (FALLBACK): any taxonomy subject not mapped to ANY section by Stage 1
    #     → assign to cross-subject sections (or all sections if none are cross-subject).
    #
    # Properties:
    #   100% automatic (zero user prompts).
    #   100% from PYQ evidence (zero heuristics).
    #   Zero behavior change for 1:1 exams (single-element subject lists).
    #   Exam-independent (no hardcoded names/types/structure).

    _ecfg_path = None
    for _sd in ['/mnt/project/', '/mnt/user-data/uploads/']:
        _matches = sorted(glob.glob(os.path.join(_sd, '*exam_config.json')))
        if _matches:
            _ecfg_path = _matches[0]
            break

    if _ecfg_path:
        import json as _json
        with open(_ecfg_path, encoding='utf-8') as _f:
            _ecfg = _json.load(_f)
        _sections = _ecfg.get('sections', [])
        _taxonomy_subjects = sorted({e['section'] for e in all_entries if e.get('section')})

        # STAGE 1: OBSERVE — which subjects appear in which section Q-ranges
        _sec_subjects = {s['name']: set() for s in _sections}
        for _paper_id, _paper_classifs in progress.items():
            if not isinstance(_paper_classifs, list):
                continue   # skip _meta and other non-list keys
            for _q in _paper_classifs:
                if not isinstance(_q, dict) or 'q_num' not in _q:
                    continue
                for _s in _sections:
                    _qr = _s.get('q_range', [0, 0])
                    if _qr[0] <= _q['q_num'] <= _qr[1]:
                        if _q.get('section'):
                            _sec_subjects[_s['name']].add(_q['section'])
                        break

        # STAGE 2: AUGMENT — cross-subject sections get union of all cross-subject pools
        _cross_secs = [_s['name'] for _s in _sections if len(_sec_subjects.get(_s['name'], set())) >= 2]
        if _cross_secs:
            _pool = set()
            for _cs in _cross_secs:
                _pool |= _sec_subjects[_cs]
            for _cs in _cross_secs:
                _sec_subjects[_cs] = set(_pool)

        # STAGE 3: FALLBACK — unmapped taxonomy subjects → cross-subject sections (or all)
        _mapped = set()
        for _v in _sec_subjects.values():
            _mapped |= _v
        _unmapped = set(_taxonomy_subjects) - _mapped
        if _unmapped:
            _targets = _cross_secs if _cross_secs else [_s['name'] for _s in _sections]
            for _t in _targets:
                _sec_subjects[_t] |= _unmapped

        # Write subjects[] to each section in exam_config
        for _s in _sections:
            _s['subjects'] = sorted(_sec_subjects.get(_s['name'], set()))

        # Write updated exam_config.json to outputs
        _out_ecfg = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
        with open(_out_ecfg, 'w', encoding='utf-8') as _f:
            _json.dump(_ecfg, _f, ensure_ascii=False, indent=2)

        print(f"\n--- S-SECMAP (v2.24.9) ---")
        for _s in _sections:
            print(f"  {_s['name']}: subjects = {_s.get('subjects', [])}")
        print(f"  → exam_config.json updated with subjects[] per section.")
        print(f"--- End S-SECMAP ---\n")
    else:
        print("\n⚠ S-SECMAP: exam_config.json not found — subjects[] not derived.")
        print("  Step 6 resolver will use fallback rules (SEC-1/SEC-3/SEC-4).\n")

    # Build exam_meta from progress._meta for EXAM_STRUCTURE header (NEW v2.3)
    from datetime import datetime
    meta_raw  = progress.get('_meta', {})
    exam_meta = {
        'papers_analysed'      : len(meta_raw.get('papers_processed', [])),
        'questions_analysed'   : meta_raw.get('total_questions', 0),
        'years_covered'        : sorted(meta_raw.get('years_processed', [])),
        'generation_date'      : datetime.now().isoformat()[:10],
        'time_per_q_sec'       : meta_raw.get('time_per_q_sec', 'unknown'),
        'language'             : meta_raw.get('language', 'unknown'),
        'q_types'              : meta_raw.get('q_types', ['MCQ']),
        'marks_per_q'          : meta_raw.get('marks_per_q', {'MCQ': 1}),
        'negative_marking'     : meta_raw.get('negative_marking', 0),
        'options_count'        : meta_raw.get('options_count', 4),
        'multi_select_allowed' : meta_raw.get('multi_select_allowed', False),
        # v2.18: new fields from exam_config.json (Step 2a v2.5 contract).
        'marking_scheme'       : meta_raw.get('marking_scheme', []),
        'level'                : meta_raw.get('level', 'unknown'),
        'medium'               : meta_raw.get('medium', 'unknown'),
        # v2.5 MSQ contract fields (default-safe: inert when multi_select_allowed=false)
        'msq_k_mode'               : meta_raw.get('msq_k_mode', 'n/a'),
        'msq_k'                    : meta_raw.get('msq_k', None),
        'msq_allow_aota'           : meta_raw.get('msq_allow_aota', False),  # v2.6 D5
        # v2.9 contract-sync: localized MSQ select-instruction (MSQ analogue of nat_instruction)
        'msq_instruction'          : meta_raw.get('msq_instruction',
                                                  '(One or more options may be correct)'),
        'msq_instruction_hi'       : meta_raw.get('msq_instruction_hi',
                                                  '(एक या अधिक विकल्प सही हो सकते हैं)'),
        'negative_marking_by_type' : meta_raw.get('negative_marking_by_type', {}),
        'partial_credit'           : meta_raw.get('partial_credit', False),
        # v2.8 NAT contract fields (default-safe: inert when nat_allowed=false)
        'nat_allowed'              : meta_raw.get('nat_allowed', False),
        'nat_answer_type'          : meta_raw.get('nat_answer_type', 'real'),
        'nat_tolerance'            : meta_raw.get('nat_tolerance', '0'),
        'nat_instruction'          : meta_raw.get('nat_instruction',
                                                  'Enter your answer as a numerical value.'),
        # v2.15 BUG-D07: option_label_format now auto-detected and stored
        'option_label_format'      : meta_raw.get('option_label_format', '1/2/3/4'),
    }

    # Write outputs
    rules_path    = write_section_rules(all_entries, exam_code, exam_meta=exam_meta,
                                         progress=progress)   # v2.15 BUG-D03: progress for label agg
    manifest_path = write_subtopic_manifest(all_entries, exam_code, exam_meta=exam_meta,
                                             progress=progress)   # v2.23: per-section axis dist
    summary_path  = write_analysis_summary(all_entries, progress, exam_code)
    # v2.15 BUG-D01 fix: generate_frequency_xlsx() was defined in §16 but NEVER called.
    # v2.24.6 FIX B: pass all_entries (PYQ + Zero-PYQ scaffolds, post taxonomy-sync +
    # zero-PYQ format inference) so the xlsx is taxonomy-complete and Format-parity-
    # guaranteed with the manifest — was `progress` only (PYQ-observed subtopics only).
    # v2.39.2: implementation lives in the repo engine frequency_xlsx.py (§16).
    import frequency_xlsx as fx
    xlsx_path     = fx.generate_frequency_xlsx(progress, exam_code, all_entries=all_entries)

    # Final delivery
    deliver_final(exam_code, rules_path, summary_path, qv_results, progress,
                  manifest_path=manifest_path, xlsx_path=xlsx_path)

def deliver_final(exam_code, rules_path, summary_path, qv_results, progress,
                  manifest_path=None, xlsx_path=None):
    """
    Final delivery: section_rules.md, subtopic_manifest.json, PYQ_Frequency.xlsx,
    analysis_progress.json, analysis_summary.md — all 5 outputs in one response.
    v2.15 BUG-D02: xlsx_path added (was missing — xlsx never delivered).
    """
    # Save final progress
    progress_path = save_progress(progress, exam_code)

    meta        = progress.get('_meta', {})
    n_papers    = len(meta.get('papers_processed', []))
    n_questions = meta.get('total_questions', 0)
    years       = sorted(meta.get('years_processed', []))

    print(f"\n{'='*55}")
    print(f"Step 5 (PYQExtract) COMPLETE — {exam_code}")
    print(f"Papers : {n_papers} | Questions: {n_questions} | Years: {years}")
    print(f"{'='*55}")

    # Deliver all outputs as downloadable chat files.
    # NO Drive upload. User downloads from chat and uploads manually to project.
    # Order matters — section_rules.md first (most important).

    # Present all files as downloadable chat attachments
    # v2.15 BUG-D02 fix: xlsx_path included in delivery (was missing).
    # v2.24.9 S-SECMAP: exam_config.json added (carries subjects[] for Step 6 resolver).
    # Order: section_rules (most important) → manifest → xlsx → exam_config → progress → summary
    delivery = [rules_path]
    if manifest_path: delivery.append(manifest_path)
    if xlsx_path:     delivery.append(xlsx_path)
    # v2.24.9: include updated exam_config.json (with subjects[]) if it was generated
    _ecfg_out = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
    import os as _os2
    if _os2.path.exists(_ecfg_out):
        delivery.append(_ecfg_out)
    # v2.24: the human-readable taxonomy companion (Subject/Topic/Sub-topic + id), written by
    # write_subtopic_manifest → write_taxonomy_xlsx. Deterministic path; include if it exists.
    import os as _os
    _tax_path = f'/mnt/user-data/outputs/{exam_code}_taxonomy.xlsx'
    if _os.path.exists(_tax_path): delivery.append(_tax_path)
    delivery += [progress_path, summary_path]
    present_files(delivery)
    # present_files is the Claude tool that makes files downloadable in chat.
    # User downloads section_rules.md AND subtopic_manifest.json and uploads
    # BOTH to their [ExamCode] Claude project Files/Knowledge section.
    # subtopic_manifest.json is the cross-step contract — Step 6 and Step 7 both require it.
    # PYQ_Frequency.xlsx is kept locally for Step 6 input.

    # Print handoff message (matches S11-2 PART C format exactly)
    print(f"\nStep 5 (PYQExtract) complete for {exam_code}.")
    print(f"Papers: {n_papers} | Questions: {n_questions} | Years: {years}")
    print("")
    print("ACTION REQUIRED — upload to [ExamCode] Claude project:")
    print(f"  [1] Download {exam_code}_section_rules.md from the file above")
    print(f"  [2] Go to your {exam_code} Claude project → Files (or Knowledge) section")
    print(f"  [3] Upload the downloaded section_rules.md file there")
    print("  (Step 7 reads it directly from the project Files section)")
    print("")
    print("KEEP LOCALLY (downloaded to your computer):")
    print(f"  analysis_progress.json — needed if you add more PYQ papers later")
    print(f"  analysis_summary.md    — review WARNs if any")
    print("")
    print("NEXT:")
    print("  Step 5 complete.")
    print("  If Step 6 (MockBlueprint) also complete: start MockCreate M1.")
    print(f"  If Step 6 pending: run MockBlueprint [N].")
```

### S8-5 — Resume logic (between sessions)

```python
# At session start (S1-2), after loading progress:
done_ids = set(progress.get('_meta',{}).get('papers_processed',[]))

# is_already_processed() used to skip any paper whose ID is in done_ids.
# Filenames must be stable across sessions — do not rename PYQ files.
# Paper ID = filename without extension (make_paper_id).

def is_already_processed(paper_id, progress):
    return paper_id in progress.get('_meta',{}).get('papers_processed',[])

# If ALL uploaded papers are already in done_ids → auto-synthesise immediately.
# User never needs to explicitly type --synthesise.
```

### S8-7 — Progress JSON schema (reference)

```json
{
  "_meta": {
    "exam_code"       : "[ExamCode]",
    "schema_version"  : "2.3",
    "last_updated"    : "[ISO-datetime]",
    "papers_processed": ["[ExamCode]_2024_Shift1", "[ExamCode]_2024_Shift2"],
    "years_processed" : [2019, 2020, 2021, 2022, 2023, 2024],
    "total_questions" : 0,

    "_transport": {
      "channel"          : "direct | spill | inline",
      "probe_paper"      : "[ExamCode]_15-Feb-2026_Sorted_Q1-Q60.docx",
      "session_budget"   : 100000,
      "papers_planned"   : ["[file_id]"],
      "deferred_context" : ["[file_id]"],
      "deferred_size"    : [],
      "session_log"      : [
        { "session_index"    : 1,
          "started_utc"      : "[ISO-8601 UTC]",
          "spec_read_mode"   : "full | reduced",
          "probe_run"        : true,
          "chars_consumed"   : 0,
          "papers_fetched"   : ["[file_id]"],
          "papers_processed" : ["[paper_key]"],
          "ended_at"         : "batch_boundary | corpus_complete | session_exhausted" }
      ]
    }
    // v2.51.0 — 'papers_admitted' was RENAMED 'papers_planned': record_transport writes
    // it BEFORE the acquisition loop, so it is a FORECAST and never a result. Readers
    // MUST tolerate the old key for one release (EC-P38 — a pre-patch progress file is
    // VALID INPUT and is never discarded):
    //     planned = t.get('papers_planned', t.get('papers_admitted', []))
    // 'session_log' is purely additive; its absence means "written before v2.51.0".
  },
  "('[Section Name]', '[Topic]', '[Subtopic]')": [
    {
      "num":1, "stem":"clean stem text", "stem_raw":"original stem with NOTE",
      "options":["option1","option2","option3","option4"],
      "section":"[Section Name]",
      "topic":"[Topic]", "subtopic":"[Subtopic]",
      "year":2024, "shift":"S1", "paper_id":"[ExamCode]_2024_Shift1",
      "has_note":true, "note_text":"(NOTE: Operations on whole numbers only...)",
      "blank_pos":"none", "is_negative":false, "is_msq":false,
      "image_role":"none", "omml_present":false, "omml_failed":false,
      "object_type":null, "transformation":null, "arrangement":null,
      "complexity":null, "image_clarity":null,
      "difficulty":{"level":"Medium","C":2,"I":1,"V":1,"score":4,"flags":[]},
      "option_format":"single_value", "linked_group_id":null
    }
  ],
  "_linked_groups": {
    "G1": {"group_id":"G1","q_numbers":[90,91,92,93,94],
           "stimulus_type":"passage","word_count":120}
  }
}
```

### S8-8 — Save and load functions

```python
def save_progress(progress, exam_code):
    """Serialize tuple keys to strings for JSON compatibility. Updates last_updated timestamp."""
    from datetime import datetime, timezone
    if isinstance(progress.get('_meta'), dict):
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
    data = {str(k) if isinstance(k, tuple) else k: v for k, v in progress.items()}
    path = f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json'
    with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def load_progress(exam_code):
    """Load progress, preferring the MOST ADVANCED copy rather than the first found.

    v2.39 (GAP-2026-07-27-H, raised P3 -> P1 on operator evidence).

    The old order returned the FIRST existing path, with /mnt/project/ first and
    /mnt/user-data/outputs/ — where the live session writes — LAST. Within a run the
    current state is in outputs while a stale copy sits in project knowledge, so any
    mid-run reload silently reverted to the stale one. This is not an edge case: the
    documented operator workflow is "download the output, re-upload it to project
    knowledge", which makes stale-project-copy the NORMAL state between sessions. One
    session lost a completed 3-paper batch this way and had to reprocess it.

    Ordering by directory cannot express the real rule, because which directory is
    freshest depends on whether this is a cold start or a mid-run reload — something
    this function cannot know. So it does not guess: it reads every candidate and takes
    the one that has processed the most papers, which is correct in BOTH cases and needs
    no mode flag. Divergence is reported, never silent.

    Ties break toward the earlier path (project knowledge), preserving pre-v2.39
    behaviour when the copies are equally advanced.
    """
    candidates = []
    for search_path in [
        f'/mnt/project/{exam_code}_analysis_progress.json',
        f'/mnt/user-data/uploads/{exam_code}_analysis_progress.json',
        f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json',  # live session state
    ]:
        if not os.path.exists(search_path):
            continue
        try:
            with open(search_path, encoding='utf-8') as f: raw = json.load(f)
        except Exception as ex:
            print(f"  WARN: progress file unreadable, skipped: {search_path} — {ex}")
            continue
        progress = {}
        for k, v in raw.items():
            try:    key = ast.literal_eval(k)
            except: key = k
            progress[key] = v
        n_done = len((progress.get('_meta', {}) or {}).get('papers_processed', []))
        candidates.append((n_done, search_path, progress))

    if candidates:
        best = max(candidates, key=lambda c: c[0])       # max() keeps the FIRST maximum
        if len({c[0] for c in candidates}) > 1:
            print("  ! Divergent progress files found — taking the most advanced:")
            for n_done, path, _ in candidates:
                mark = '  <= USING' if path == best[1] else ''
                print(f"      {n_done:3d} paper(s)  {path}{mark}")
            print("    (v2.39: selection is by papers_processed, not directory order. "
                  "Delete or refresh the stale copy to silence this.)")
        return best[2]
    return {'_meta': {'papers_processed': [], 'total_questions': 0,
                       'years_processed': [], 'exam_code': exam_code},
            '_linked_groups': {}}
```

### S8-9 — When --synthesise flag is still useful

```
The --synthesise flag remains available but is never required in normal flow.

Use cases where it IS still useful:
  (a) User added new PYQ papers after section_rules.md was already generated.
      Upload new papers → new session auto-processes them → auto-synthesises.
      Result: section_rules.md is refreshed with improved patterns.

  (b) User wants to re-synthesise without adding new papers (e.g., after
      manually fixing progress.json data):
        PYQExtract --synthesise ALL
      NOTE: Year coverage check still applies when --synthesise ALL is called.
      run_synthesise() reconstructs available_years from progress['_meta']['years_processed']
      and blocks synthesis if minimum coverage is not already in the progress data.

  (c) User wants to synthesise a single section to preview:
        PYQExtract --synthesise "[Section Name]"

In case (a), the flow is:
  Upload new .docx files → new session → processes only the new papers
  (existing papers already in progress.json are skipped) → auto-synthesises
  → delivers updated section_rules.md as downloadable chat file.
  Download it → replace old section_rules.md in [ExamCode] project Files/Knowledge.
  Existing mocks unaffected. Future mocks use improved patterns.
```

---

## §9 — STATUS DASHBOARD

When `--status`:
```
"=== PYQExtract Status: [ExamCode] ===
 Time/Q: [N]sec | lang:[x] | Q-types:[list] | marks:[dict]
 Papers: [N] | Years: [list] | Total Qs: [N]
 Figural images analysed: [N] ([N_unclear] unclear)

 Coverage by section:
   [Section 1]: [N]/[total] subtopics  [####....] [%]%
   [Section 2]: [N]/[total] subtopics  [########] 100%

 Data quality:
   observed  (>=3 Qs): [N] subtopics
   inferred  (1-2 Qs): [N] subtopics
   absent    (0 Qs)  : [N] subtopics

 section_rules.md: [Generated [date] | Not yet generated]
 Next: Process more papers  OR  Run --synthesise ALL
 ============================================="
```

---

## §10 — ANALYSIS SUMMARY FORMAT

```
# [ExamCode] Analysis Summary
Generated: [datetime] | Papers: [N] | Questions: [N] | Years: [list]

## HUMAN REVIEW REQUIRED

### Inferred patterns (1-2 occurrences — verify):
  [Subtopic] P[N]: "[template]" (seen [N] times, years: [Y])

### Deprecated patterns (absent from last 2 years):
  [Subtopic] P[N]: "[template]" (last seen: [Y])

### Figural object types (Claude's vision analysis — review if needed):
  [Subtopic]: [N] images analysed, [N] unclear
  Detected dominant objects: [list]
  Transformation types: [list]
  (QV-9 flags if unclear rate > 20% — those subtopics may need more PYQ data)

### Absent subtopics (no PYQ data — Step 2 uses training knowledge):
  [list]

### Option format changes across years:
  [Subtopic]: [old_fmt] in [years] -> [new_fmt] in [recent years]

## SUGGESTED AUDIT_CONFIG UPDATES
  passage_min_words: [observed min]
  vocab_topic_names: [vocabulary subtopics found]

## STATISTICS
[Section coverage table]
[Top 10 subtopics by observed_count]
```

---

## §11 — DELIVERY FORMAT

### S11-1 — Mid-batch delivery (after each batch, more papers remain)

```
PART A — Batch summary in chat:
  "=== Batch [N] complete ===
   ✓ [filename_1] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs
   ✓ [filename_2] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs
   ✓ [filename_3] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs

   Cumulative : [done] / [total] papers | [N] total Qs
   Subtopics  : [N] observed | [N] sparse | [N] absent
   Unclear imgs: [N] (QV-9 will flag if >20% per subtopic)
   =================================="

PART B — present_files:
  1. [ExamCode]_analysis_progress.json   <- downloadable from chat

PART C — Continue prompt:
  "[N] paper(s) remaining.
   Options:
   A) Say 'continue' to process the next batch now in this same session.
   B) Download analysis_progress.json above → upload to [ExamCode] project
      knowledge (replace prior version) → open fresh chat → type:
        PYQExtract PYQ: <<same Drive link>>
   Both are valid. Progress is in memory so option A needs no upload."

   Note: User can say 'continue' / 'go' / 'next' — all accepted.
   Claude does NOT auto-proceed — user confirms before each batch.
```

### S11-2 — Final delivery (last batch processed → auto-synthesis complete)

```
This happens automatically at the end of the last batch.
No separate session, no --synthesise command needed.

PART A — QV results in chat:
  "=== Quality Verification ===
   v QV-1  Coverage        : PASS — [N] subtopics covered
   v QV-2  Freq sums       : PASS — all = 100%
   ! QV-3  Difficulty      : WARN — [N] subtopics missing Hard level
   v QV-4  Option format   : PASS
   v QV-5  Wrong options   : PASS
   v QV-6  Confidence      : PASS
   v QV-7  Templates       : PASS
   v QV-8  OMML recovery   : PASS
   ! QV-9  Image clarity   : WARN — [N] unclear images (< 20% threshold)
   v QV-10 Passage groups  : PASS
   v QV-11 Recency         : PASS
   v QV-12 Dedup           : PASS
   ==========================="

PART B — present_files (all in one call, in the order the final_delivery code
emits: rules → manifest → xlsx → exam_config → taxonomy → progress → summary):

  MANDATORY — every run:
    1. [ExamCode]_section_rules.md        <- PRIMARY: download → upload to [ExamCode] project
    2. [ExamCode]_subtopic_manifest.json  <- download → upload to [ExamCode] project
    3. [ExamCode]_PYQ_Frequency.xlsx      <- download → keep for Step 6 input

  WHEN IT EXISTS — which is every normal run:
    4. [ExamCode]_exam_config.json        <- download → REPLACE in [ExamCode] project
                                             (v2.24.9: carries subjects[] for Step 6 resolver;
                                              absent only when S-SECMAP warned and continued)
    5. [ExamCode]_taxonomy.xlsx           <- download → human-readable taxonomy companion
                                             (absent only when openpyxl was unavailable)

  MANDATORY — every run (emitted last):
    6. [ExamCode]_analysis_progress.json  <- download → keep locally
    7. [ExamCode]_analysis_summary.md     <- download → review if WARNs exist

  All files above are delivered as downloadable chat attachments — 7 on a normal run,
  5 in the degraded case where both conditional files are absent. This list is the same
  two-tier contract S11-3 and the pre-delivery checklist enforce; do not restate it as a
  fixed count (v2.48.2 — the "All 6" wording here survived v2.47.1 and v2.48.1 and was
  the site the field-reported silent drop came from).
  NOTHING is uploaded to Google Drive.

PART C — Handoff message:
  "Step 5 (PYQExtract) complete for [ExamCode].
   Papers: [N] | Questions: [N] | Years: [list]

   ACTION REQUIRED — upload to [ExamCode] Claude project:
     [tick] Download [ExamCode]_section_rules.md from the file above
     [tick] Download [ExamCode]_subtopic_manifest.json from the file above
     [tick] Download [ExamCode]_exam_config.json from the file above
           (v2.24.9: now carries subjects[] per section for Step 6 resolver)
     [tick] Go to your [ExamCode] Claude project → Files (or Knowledge) section
     [tick] Upload all 3 files (replace any existing versions)

   KEEP FOR STEP 6:
     [ExamCode]_PYQ_Frequency.xlsx — Step 6 input (Frequency Excel)

   KEEP LOCALLY (downloaded to your computer):
     analysis_progress.json  — needed if you add more PYQ papers later
     analysis_summary.md     — review WARNs if any

   To add new PYQ papers later:
     1. Add new .docx files to your Google Drive PYQ folder
     2. Run: PYQExtract PYQ: <<same Drive link>>
     3. New papers auto-detected → processed → auto-synthesis → refreshed outputs
     4. Download all output files from chat (the S11-3 final set: 5 mandatory,
        plus exam_config.json and taxonomy.xlsx when present)
     5. Replace old files in [ExamCode] project Files/Knowledge section
     Existing mocks: unaffected. Future mocks: use improved patterns.

   NEXT:
     Step 5 complete.
     If Step 6 (MockBlueprint) also complete: start MockCreate M1.
     If Step 6 pending: run MockBlueprint [N]."
```

### S11-3 — DELIVERABLE SET CONTRACT (CLOSED)

```
═══════════════════════════════════════════════════════════════════════
DELIVERABLE SET CONTRACT — EXHAUSTIVE AND CLOSED
═══════════════════════════════════════════════════════════════════════

Each delivery point delivers EXACTLY the files listed and NOTHING ELSE.
This is an exhaustive, closed list — not a minimum. Creating or
delivering any unauthorized file is a spec violation.

────────────────────────────────────────────────────────────────────
PER-BATCH DELIVERY (after each batch — 1 to BATCH_SIZE papers — more remain)
────────────────────────────────────────────────────────────────────
DELIVER (single present_files call):
  1. [ExamCode]_analysis_progress.json

DO NOT DELIVER:
  ✗ section_rules.md (not yet generated — synthesis hasn't run)
  ✗ subtopic_manifest.json (not yet generated)
  ✗ PYQ_Frequency.xlsx (not yet generated)
  ✗ analysis_summary.md (not yet generated)
  ✗ Any intermediate or working files

────────────────────────────────────────────────────────────────────
FINAL DELIVERY (last batch → auto-synthesis → QV checks complete)
────────────────────────────────────────────────────────────────────
DELIVER in ONE present_files call, in the order the delivery code emits
(v2.48.2: numbering now follows the code's emission order — rules → manifest →
xlsx → exam_config → taxonomy → progress → summary — so this list, S11-2
PART B, and the delivery code are literally identical; v2.48.1's renumbering
put the conditional tier AFTER progress/summary, a third order in play.
v2.48.1: the list shows the SAME two tiers the pre-delivery checklist below
enforces — v2.47.1 moved exam_config.json to the conditional tier but this
list still called it one of "the 6 mandatory files"):
  MANDATORY — every run:
    1. [ExamCode]_section_rules.md
    2. [ExamCode]_subtopic_manifest.json
    3. [ExamCode]_PYQ_Frequency.xlsx
  WHEN IT EXISTS — which is every normal run:
    4. [ExamCode]_exam_config.json   (absent only when S-SECMAP warned and continued)
    5. [ExamCode]_taxonomy.xlsx      (absent only when openpyxl was unavailable)
  MANDATORY — every run (emitted last):
    6. [ExamCode]_analysis_progress.json
    7. [ExamCode]_analysis_summary.md

DO NOT DELIVER:
  ✗ Input PYQ .docx files (these are INPUTS)
  ✗ Any intermediate scripts or pipeline files
  ✗ Any temporary JSON, working, or debug files
  ✗ Any renamed or versioned variants of the above files

PRE-DELIVERY CHECKLIST (before every present_files call):
  delivering = set of files about to be passed to present_files
  expected   = per-batch: {analysis_progress.json}
               final:     {section_rules.md, subtopic_manifest.json,
                           PYQ_Frequency.xlsx,
                           analysis_progress.json, analysis_summary.md}
               final, additionally WHEN IT EXISTS: {exam_config.json, taxonomy.xlsx}
               (v2.47.1: exam_config.json moved to the conditional tier — the
                delivery code appends it only if generated, and S-SECMAP
                explicitly tolerates a missing exam_config with a WARN and
                continues; listing it unconditionally meant Check 1 below
                FORBADE delivery on exactly the runs S-SECMAP had already
                blessed — the inverse of the taxonomy.xlsx veto v2.47 fixed.)
               (v2.47, GAP-2026-08-13-DELIVERY-COUNT-DRIFT: the delivery code
                has appended taxonomy.xlsx conditionally since v2.24 — written
                on every normal run, skipped only when openpyxl is missing —
                but this expected set did not list it, so Check 2 below would
                veto the code's own 7-file delivery. DERIVED from what was
                actually written, the same v5.36 lesson Step 7's S13-7 learned.)
  Check 1: All expected files present in delivery — assert not (expected - delivering)
  Check 2: No unexpected files in delivery — assert not (delivering - expected)
  Check 3: No internal files leaked — no banned patterns in filenames
  Only after all checks pass → call present_files
  A FAILED CHECK IS A FINDING, NEVER A TRIM (v2.48.1). If any check fires,
  STOP and report the exact differing filenames in chat as a spec/code drift
  discrepancy — do NOT silently drop the extra file or pad the missing one
  and proceed. Observed in the field: a run holding a generated
  taxonomy.xlsx back to satisfy a stale six-file reading of this contract,
  with no mention in chat; the operator learned the file existed only by
  asking. The contract polices drift; silence hides it.
═══════════════════════════════════════════════════════════════════════
```

### S11-4 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.

Step 5 uses BOTH footer types:
  - F1 (amber) after each non-final batch (delivers analysis_progress.json)
  - F2 (green) after final batch + auto-synthesis (delivers the full final set — S11-3)
```

---

## §12 — INTEGRATION WITH STEP 7 (MockCreate)

### S12-1 — How Step 7 reads section_rules.md

```
Step 7 S1-2d loads:
  section_rules_text = open('/mnt/project/[ExamCode]_section_rules.md',
                             encoding='utf-8').read()

Per question generated (Step 7 MockCreate, section 17, S17-3):

  STEP 1 -- stem template:
    Locate: '--- Subtopic: [re.escape(S)] ---' in section_rules_text.
    Parse: PYQ_STEM_PATTERNS block (P1, P2, ... until next '---' or '=== SECTION:').
    Stop markers: '--- Subtopic:' (next subtopic) or '=== SECTION:' (next section).
    Select P_k by weighted random (weights=frequency%).
    Deprecated patterns: multiply weight by 0.1.
    observed_recent patterns: multiply weight by 1.5.

  STEP 2 -- difficulty calibration:
    Parse PYQ_DIFFICULTY_CALIBRATION block for assigned level.
    Apply criteria literally.

  STEP 3 -- context:
    Parse PYQ_CONTEXT_POOL.dominant. Select from this list (>50% of time).
    Never select from avoid list.

  STEP 4 -- numbers:
    Parse PYQ_NUMBER_RANGES. Generate values within min/max, aligned to multiples_of.

  STEP 5 -- wrong options:
    Read wrong_option_structure.type. Apply:
    fixed_set      -> use fixed_option_texts exactly
    shared_pool    -> rotate from shared_pool_words
    adjacent_values -> 3 near-miss calculations
    alliterative   -> 3 options sharing first letter
    same_category  -> 3 real entities from same class
    anagram        -> 3 rearrangements of answer
    sentence_label -> "Only X" / "Both X and Y" combinations
    image_only     -> no text options generated

  STEP 6 -- NOTE block:
    Read note_block for selected pattern.
    mandatory   -> always append note_text to stem
    conditional -> append with 60% probability
    rare        -> append with 20% probability
    BUG-B13 fix: rare handling added above.
    never       -> do not add NOTE

  STEP 7 -- figural:
    Read PYQ_IMAGE_ANALYSIS.image_role (actual role from E-4, not hardcoded).
    Read object_types.dominant (70%) or observed (30%).
```

### S12-2 — Update protocol

```
NEVER edit section_rules.md directly. Regenerate only.

When new PYQ papers arrive:
  1. Add new .docx files to your Google Drive PYQ folder (same folder used in original trigger).
  2. Run: PYQExtract PYQ: <<same Drive link>>
     → Skips already-processed papers automatically.
     → Processes only new papers (in batches of up to BATCH_SIZE; see S8-1 — it is a ceiling).
     → Auto-synthesises when all new papers are done.
     → Delivers refreshed section_rules.md.
  3. Download the updated section_rules.md from chat.
  4. Replace section_rules.md in [ExamCode] project Files/Knowledge section.

Impact:
  blueprint.json: unchanged | registry.json: unchanged
  Existing mocks: unaffected | Future mocks: use improved patterns
```

---

## §13 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  All 11 extraction rules (E-1 through E-11) with all bug fixes
  section_rules.md field names and schema
  Difficulty scoring (3 axes + marks scaling + v2.5 MSQ load term)
  QV-1 through QV-16 checks (plus QV-5b for fixed_set validation)
  EC-1 through EC-15 edge cases (plus EC-A statement-combination MSQ guard, v2.5)
  Progress JSON schema and delivery format

EXAM-DISCOVERED (zero hardcoding):
  Subtopic names, stem templates, approaches
  answer_cardinality (single/multi) + msq_freq + msq_k_mode/k + per-type marking (v2.5,
    discovered from PYQ option shape + Exam Pattern; nothing exam-specific hardcoded)
  Option formats (which of 12 types), wrong option structures
  Difficulty calibration criteria, number ranges, context pools
  NOTE block texts and frequencies
  Figural object types and transformations
  Passage structures and topic domains

PROOF:
  SSC CGL:   221 subtopics | 1/2/3/4 options | NOTE blocks for Analogy
  GATE CS:   ~40 subtopics | (A)/(B)/(C)/(D) | no NOTE blocks
  NEET Bio:  ~90 subtopics | (1)/(2)/(3)/(4) | statement format heavy
  UPSC CSAT: ~30 subtopics | (a)/(b)/(c)/(d) | Assertion-Reason frequent
```

---

## §14 — SECTION_RULES.MD SCHEMA REFERENCE

```
CATEGORY C (file-level header — written once at top of section_rules.md):
  *** DOC-ALIAS ONLY *** — "CATEGORY C" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '=== EXAM_STRUCTURE ==='.
  A consumer spec MUST test for '=== EXAM_STRUCTURE ===' (or read specific key: value
  lines via a regex like cat_c() does) — NEVER regex-match the phrase "CATEGORY" or
  "CATEGORY C" against file content; that string is never written to disk. (See
  A-INTEGRITY-FALSEPOS-01 / the CreateAudit v2.7.5 changelog entry (CHANGELOG.md) for the
  exact defect this caused when violated.)
  NEW v2.3 — auto-detected at runtime, never hardcoded.
  Written by write_section_rules() under '=== EXAM_STRUCTURE ==='.

  exam_code                str   [ExamCode] from trigger.
  total_papers_analysed    int   Number of PYQ .docx files processed.
  total_questions_analysed int   Total PYQ questions accumulated across all papers.
  years_covered            list  All years for which PYQ papers were processed.
  generation_date          str   ISO date of synthesis run.
  time_per_q_sec           int   Seconds per question (auto-detected from exam pattern).
  language                 str   english | hindi | regional | bilingual (auto-detected from PYQ).
  medium                   str   v2.18. Exam language from exam_config.json Overview tab.
                                 "English", "Hindi", "Bilingual", etc. Authoritative source —
                                 language field above is PYQ-detected validation. xlsx wins
                                 on conflict. Consumed by Steps 7, 9, 11.
  level                    str   v2.18. Academic level from exam_config.json Overview tab.
                                 "Graduation", "Post Graduation", "Under Graduation", "School".
                                 Step 7 uses for question complexity calibration.
                                 Step 9 uses for explanation depth.
  q_types                  list  e.g. ['MCQ'] or ['MCQ','MSQ'] (auto-detected).
  marks_per_q              dict  e.g. {'MCQ':1} or {'MCQ':2,'MSQ':2} (auto-detected).
                                 v2.18: derived from marking_scheme[] — MAX per question_type.
                                 Summary scalar for backward compat; see marking_scheme for
                                 full per-range detail.
  negative_marking         float e.g. -0.5 or 0 (auto-detected).
                                 v2.18: derived from marking_scheme[] — most common value.
                                 Summary scalar; see marking_scheme for per-range detail.
  marking_scheme           list  v2.18. Full per-range scoring rules from exam_config.json.
                                 Each entry: {q_range: [start,end], question_type: str,
                                 correct_marks: float, negative_marks: float}.
                                 Steps 7/8/9 use this for exact per-Q-position marks lookup
                                 (e.g., CSIR NET Q.72 in Part C → 4 marks, Q.25 in Part B → 2).
                                 Empty list [] when exam_config absent (legacy fallback).
  options_count            int   Options per question e.g. 4 (auto-detected).
  multi_select_allowed     bool  True for exams with MSQ (auto-detected).
  msq_k_mode               str   v2.5. fixed | variable | n/a (from Exam Pattern; n/a when
                                 multi_select_allowed=false). Step 7 uses to bound |S|.
  msq_k                    int   v2.5. Correct-option count for fixed mode (else none).
  msq_allow_aota           bool  v2.6 (D5). True permits "All of the above" as an option
                                 under MSQ (default False — AOTA is self-contradictory in
                                 multi-select). Step 7 (R-MSQ-ESCAPE/G-MSQ-SET) and Step 8
                                 (A-MSQ-KEY) read it directly from section_rules.
  msq_instruction          str   v2.9. Localized MSQ select-instruction (the MSQ analogue of
                                 nat_instruction). Default '(One or more options may be
                                 correct)'. Step 7 (msq_instruction_for) and Step 8
                                 (msq_instruction_phrases / A-MSQ-INSTR) read it from
                                 section_rules; overridable per exam. Inert when
                                 multi_select_allowed=false.
  msq_instruction_hi       str   v2.9. Hindi/bilingual variant of msq_instruction. Default
                                 '(एक या अधिक विकल्प सही हो सकते हैं)'.
  negative_marking_by_type dict  v2.5. e.g. {'MCQ':-0.5,'MSQ':0}. Per-type penalty; MSQ
                                 commonly 0. Consumed by Step 9 scoring. {} = use scalar.
  partial_credit           bool  v2.5. True if MSQ awards partial marks (else all-or-nothing).
                                 Consumed by Step 9; dormant at Step 5.
  difficulty_labels        list  v2.12. Canonical, exam-overridable difficulty vocabulary used
                                 as the stored/rendered Complexity value in the per-question
                                 registry.question_index (Step 6 seeds, Step 7 fills, Step 8
                                 certifies, Step 6 renders). Default ['Easy','Medium','Hard'].
                                 Alias to the two internal spellings — Step-0 calibration
                                 Simple/Medium/Hard and Step-1 schedule counts simple/medium/hard
                                 — is fixed: simple→Easy, medium→Medium, hard→Hard. Consumed by
                                 Step 6 (carry-through to blueprint.json) and the G-QINDEX
                                 difficulty check. An exam may override (e.g. a 2- or 5-band set).
  nat_allowed              bool  v2.8 (PARAMETER 11). Capability gate (analogous to
                                 multi_select_allowed): true iff the exam uses numerical-entry
                                 questions. Gates the per-subtopic answer_type detection.
                                 Default false ⇒ NAT path fully inert.
  nat_present              bool  v2.8. Rollup of THIS analysis — true iff any subtopic
                                 resolved to answer_type=='numerical'. Step 6 also derives
                                 this from per-subtopic answer_type (mirrors multi_present).
  nat_answer_type          str   v2.8. integer | real (default real when nat_allowed). integer
                                 ⇒ exact match; real ⇒ value within nat_tolerance. From exam
                                 pattern only (answer-key info; unextractable from PYQ).
  nat_tolerance            str   v2.8. Accepted band for real NAT — abs delta (float) or '%'
                                 string. '0' = exact to displayed precision (default; never
                                 invented). Becomes Step 9 ca_range. integer ⇒ always '0'.
  nat_instruction          str   v2.8. Parametric candidate-facing instruction Step 7 places
                                 in the Q.N stem (R14), localised per PARAMETER 3. Default
                                 "Enter your answer as a numerical value."
  total_sections           int   Number of distinct sections in section_rules.md.
  framework_version        str   Framework_MockTestAnalyse version used.

  (Also written: STRUCTURAL_CHANGES_BY_YEAR block — observable year-over-year
   structural changes derived from PYQ data by _compute_structural_changes().)

CATEGORY A (per section header — one block per section):
  *** DOC-ALIAS ONLY *** — "CATEGORY A" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '=== SECTION: <n> ===' (per
  section, where <n> is the section number). Never regex-match the phrase "CATEGORY A"
  against file content — test for the '=== SECTION:' marker instead.
  option_label_format  str   Most common option label in section: "1/2/3/4"|"A/B/C/D" etc.
  figural_banned       bool  NEW v2.3. True when ALL FIGURAL subtopics in this section
                             have observed_count=0 or all patterns deprecated.
                             Computed from data — NOT hardcoded per exam.
                             Step 7 uses this to skip FIGURAL generation for this section.
  sub_types_observed   list  Exact SubTopic heading strings from PYQ docx.
  axis_distribution    block v2.23. Per-section 3-year format-distribution TARGET (per-paper
                             averages) — the CATEGORY-A output of compute_section_axis_distribution().
                             Sub-fields: recent_years, n_papers_recent, mocks_per_window,
                             negative_rate, axis1_per_paper {TEXT|FIGURAL|PASSAGE|DI: avg},
                             axis2_per_paper {8-class: avg}, axis3_per_paper {MCQ|MSQ|NAT: avg},
                             axis2_audit_mode {class: band|guarantee|float}. band iff
                             avg×mocks_per_window ≥ 1; else guarantee (periodic ≥1/window);
                             DIRECT always float (residual, never audited). Step 6 enforces
                             axis1/axis3 + LINKED at allocation; Step 7 enforces the other 7
                             Axis-2 classes at generation; Step 8 audits. Omitted for all-Zero-PYQ
                             sections. Also mirrored into subtopic_manifest.json axis_distribution{}.

CATEGORY B (per subtopic entry — one block per subtopic):
  *** DOC-ALIAS ONLY *** — "CATEGORY B" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '--- Subtopic: <name> ---'
  (per subtopic). Never regex-match the phrase "CATEGORY B" against file content — test
  for the '--- Subtopic:' marker instead.
  subtopic               str   Exact subtopic name.
  section                str   Parent section.
  topic                  str   Parent topic.
  observed_count         int   Total PYQ questions across all papers.
  format                 str   TEXT | FIGURAL | PASSAGE | DI
  option_format_primary  str   Most common option format across all years.
                               (BUG-B15/C04 fix v2.3: written as 4 separate fields)
  option_format_recent   str   Option format in most recent year only.
  option_format_changed_recently  bool  True if recent != primary.
  option_format_all_observed      list  All distinct option format types seen.
  OMML_required          bool  True if subtopic has OMML math formulas in PYQ.
  negative_question_freq int   % of Qs using NOT/INCORRECT/EXCEPT/WRONG.
  observed_axis2         dict  v2.23. {AXIS2_CLASS: count} — this subtopic's PYQ-observed
                               Axis-2 (STEM STRUCTURE) distribution, from the shared classifier.
  presentation_family    str   v2.23. Family key (vocab_single_word|one_word_substitution|
                               idiom_phrase|fact_recall|None) seeding axis2_capability;
                               mirrors Step 7 resolve_presentation_family (Step 7 authoritative).
  axis2_capability       list  v2.23. Axis-2 forms this subtopic may FAITHFULLY take =
                               observed ∪ family-menu ∪ {DIRECT} (+LINKED iff format PASSAGE/DI,
                               LINKED being stimulus-locked). Step 6 uses it for rare-format
                               reachability; Step 7 renders ONLY within it (fabrication banned).
  answer_type            str   v2.8. option | numerical — the NAT axis (orthogonal to
                               answer_cardinality). 'numerical' (NAT: no options, typed
                               value) when nat_allowed AND >50% of observed Qs have zero
                               selectable options (no text options AND no option-images:
                               image_role none|stem_only, never options_only|stem_and_options
                               — so a figural NAT with a problem diagram still counts, but a
                               figural MCQ with image-options does not). Always 'option' when
                               nat_allowed=false. A 'numerical' subtopic's cardinality is moot.
  nat_freq               int   v2.8. % of observed Qs in this subtopic detected as NAT.
  answer_cardinality            str   v2.5. single | multi — the Step 7 DISPATCH unit. 'multi'
                               when >50% of observed Qs are MSQ (whole-subtopic mode, so
                               the per-mock allocation schema needs no answer-mode split).
                               Always 'single' when multi_select_allowed=false.
  msq_freq               int   v2.5. % of observed Qs in this subtopic detected as MSQ.
  fill_in_blank          str   none | start | middle | end
  linked_group_size      int   0=independent; N=average Qs per stimulus group.
  max_per_paper          int   NEW v2.3. Max Qs of this subtopic in any single paper.
                               Step 7 uses as L3 uniqueness ceiling — never exceed this.
  typical_per_paper      int   NEW v2.3. Modal/average Qs per paper for this subtopic.
  stem_word_count        dict  {min:int, max:int, typical:int}
  sub_type_label         str   Exact SubTopic heading for Step 7 dispatch.

  PYQ_STEM_PATTERNS      list  Sorted by weighted frequency DESC:
    id           str   P1, P2, P3, ...
    template     str   Structural skeleton with _VAR_ placeholders.
    approach     str   Cognitive operation in plain language.
    frequency    int   Weighted frequency% (all patterns per subtopic sum to 100).
    raw_count    int   Actual PYQ Qs matching this pattern.
                       NEW v2.3: now written to file (BUG-C02 fix).
    years        list  Calendar years this pattern was observed in.
                       NEW v2.3: now written to file (BUG-C02 fix). QV-11 uses it.
    confidence   str   observed (>=3) | observed_recent | inferred (1-2) | absent (0)
    deprecated   bool  True if pattern absent from last 2 years of data. (BUG-A20 fix)
    note_block   str   mandatory | conditional | rare | never
    note_text    str   Canonical NOTE text (if mandatory or conditional).

  PYQ_DIFFICULTY_CALIBRATION  (BUG-B09+C01 fix: is_inferred written to file v2.3):
    Simple  str   criteria="..." [INFERRED] tag if is_inferred=True
    Medium  str   criteria="..." [INFERRED] tag if is_inferred=True
    Hard    str   criteria="..." [INFERRED] tag if is_inferred=True

  wrong_option_structure dict:
    type                str  One of 11 E-11 types (including image_only). (BUG-B12 fix)
    description         str  What this means for Step 7 generation.
    fixed_option_texts  list REQUIRED when type=fixed_set. (BUG-C07 fix: QV-5b enforces)
    shared_pool_words   list Only when type=shared_pool.

  PYQ_NUMBER_RANGES  dict  {var: {min, max, multiples_of, notes}}
    (omit entirely if not quantitative)

  PYQ_CONTEXT_POOL   dict  {dominant:[str], common:[str], rare:[str], avoid:[str]}
    Optional additional fields when recycled stimuli detected (NEW v2.3):
    recycled_datasets  list  Short descriptors of stimuli seen in >=2 papers.
                             Step 7 must NOT reproduce these stimuli verbatim.
    ban_recycled       bool  True when recycled_datasets is non-empty.
    (omit entirely if not quantitative and no recycled stimuli)

  PYQ_IMAGE_ANALYSIS dict  (omit entirely if format != FIGURAL):
    image_role           str  stem_only | options_only | stem_and_options
                              Computed from E-4 q_roles, not hardcoded. (BUG-B11 fix)
    object_types         dict {dominant:[str], observed:[str], avoid:[str]}
    transformation_types list Observed transformation types.
    complexity_dist      dict {Simple:%, Medium:%, Hard:%}
    images_analysed      int
    images_unclear       int

  PYQ_PASSAGE_STRUCTURE dict  (omit entirely if format != PASSAGE):
    sub_format              str  RC | Cloze (no leading space — BUG-A10 fix)
    word_range              dict {min:int, max:int}
    paragraph_count         dict {typical:int}  (BUG-C05 fix v2.3: now written)
    topic_domains_observed  list Passage topic categories seen in PYQ.
                                 (BUG-C05 fix v2.3: now written)
    topic_domains_avoid     list Passage topics seen too recently — avoid repeating.
    q_type_distribution     dict {inference:%, direct:%, vocab:%, grammar:%}
```

---

## DEFINITION OF DONE — Step 5 (PYQExtract)

Step 5 is complete when ALL of the following hold:

```
[0] Minimum year coverage rule (§1-6) satisfied:
      MANDATORY: papers from at least 5 most recent years processed (non-negotiable).
      If exam has fewer than 5 years of PYQ: ALL available years processed.
      Exception only: Scenario B (no PYQ at all) or no_year_info mode.
      (Synthesis is automatically blocked if this is not met — §1-6 enforcement.)

[1] All available PYQ docx files processed (all years required by [0], all shifts).
[2] analysis_progress.json is current — all papers reflected in accumulated data.
[3] Auto-synthesis ran successfully at end of last batch — no manual --synthesise needed.
    (If synthesis failed: re-run PYQExtract --synthesise ALL)
[4] QV-1 through QV-12 (plus QV-5b): all results are PASS or WARN (zero FAIL checks).
[5] WARN items reviewed by user and accepted or corrected.
[6] section_rules.md loads without error in Step 7 S1-2d:
      section_rules_text = open('/mnt/project/[ExamCode]_section_rules.md',
                                 encoding='utf-8').read()
    Verify: file non-empty; all '=== SECTION:' and '--- Subtopic:' blocks present.
[7] analysis_summary.md human-review items resolved or accepted.
[8] User downloaded [ExamCode]_section_rules.md from the chat file delivery
    and uploaded it to the [ExamCode] Claude project → Files / Knowledge section.
    (NOT Drive. Claude project Files section only.)
[9] User confirmed: Step 6 (MockBlueprint) is also complete.
[13] [ExamCode]_PYQ_Frequency.xlsx generated with correct sheet count (4 + sections_count).
[14] XLSX-F1 through XLSX-F9 validation: all PASS (§16 §EXT-9).
[15] Master Data sheet row count matches total unique subtopics in progress.json.
[16] Year columns in xlsx match _meta.years_processed exactly.
[17] User downloaded [ExamCode]_PYQ_Frequency.xlsx — kept for Step 6 input.
[18] Per-batch deliverable set closed: EXACTLY 1 file per batch (S11-3)
[19] Final deliverable set closed: the 5 mandatory files, + exam_config.json and
     taxonomy.xlsx when written (=7 on a normal run) — per S11-3's derived
     expected set, two tiers exactly as S11-3 now prints them (v2.48.1; the
     "6 mandatory" wording predated v2.47.1's exam_config tier move).
     (v2.47: this item said
     "EXACTLY 5" — stale twice over: it predated both the v2.24.9 exam_config addition
     [6th] and the v2.24 taxonomy.xlsx companion [conditional 7th], and disagreed with
     S11-3's own "all 6" list. GAP-2026-08-13-DELIVERY-COUNT-DRIFT.)
[20] Pre-delivery checklist (S11-3) passed before every present_files call
[21] No unauthorized files in any present_files call
[22] Taxonomy sync ran: run_synthesise printed "Taxonomy sync:" summary line
     showing count of zero-PYQ scaffold entries added (may be 0 if all
     taxonomy subtopics were already PYQ-observed — that is correct).
[23] Completeness invariant holds: manifest subtopic count >= taxonomy subtopic
     count. A manifest with FEWER subtopics than the taxonomy means taxonomy
     sync failed or was skipped — re-run Step 5 to fix.
[24] S8-0 TRANSPORT PREFLIGHT ran (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION):
     the channel was PROBED on one paper or REUSED from _meta._transport — never
     assumed and never inferred from a directory listing (EC-P35); the transport
     plan was PRINTED BEFORE the first batch; _meta._transport is populated in
     analysis_progress.json; and the inline partition ran AFTER
     sort_papers_recency_first(), so the admitted set is the most recent N papers
     (EC-X21). A run whose deliverables exist but whose _meta._transport is absent
     was produced by a pre-v2.50.0 path and its Drive lane cannot be trusted.
[25] The corpus was NOT silently emptied: pyq_doc_paths is non-empty, or the run
     HARD STOPPED per EC-P39. Step 5 never rewrites mode to '--synthesise ALL'
     because a listing came back empty — that path produced complete, green
     deliverables of zero-PYQ scaffolds for exams with a full Drive corpus.

MockCreate M1 MUST NOT start until [8] AND [9] both hold.
```


# ════════════════════════════════════════════════════════════════════════
# §15 — SUBTOPIC_ID CONTRACT (v2.4 — the cross-step vocabulary authority)
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS EXISTS:
#   Before v2.4, Step 5 (Analyse) and Step 6 (Blueprint) each independently
#   derived subtopic names from the same Analysis docs, then Step 7 (Create)
#   tried to rejoin them by EXACT STRING MATCH. Two independent derivations do
#   not produce identical strings — each step silently corrected/merged/re-
#   clustered names its own way. On SSC CGL Tier 1 this produced ~70% name
#   mismatch (144 of 208 blueprint names had no section_rules match), causing
#   Step 7 to fail its subtopic join and its mandatory-subtopic checks.
#
# THE CONTRACT (three roles):
#   MINTER  (Step 5, THIS framework): assigns every subtopic a stable subtopic_id
#           and publishes the authoritative id↔name registry
#           ([ExamCode]_subtopic_manifest.json). Step 5 is the ONLY minter.
#   CONSUMER+ENFORCER (Step 6, Framework_Blueprint): READS the manifest, refers
#           to subtopics by subtopic_id, and enforces the mandate/alternation
#           data carried in the manifest at blueprint-build time.
#   JOINER  (Step 7, Framework_MockCreate): joins blueprint.json ↔
#           section_rules.md ON subtopic_id. No string matching.
#
# THE id RECIPE (deterministic, exam-agnostic — see slugify / make_subtopic_id):
#   subtopic_id = <section_prefix>.<topic_slug>.<subtopic_slug>
#   - slugify: lowercase; — – / & → space; non-alnum → _; collapse/strip _.
#   - Same (section, topic, subtopic) ALWAYS yields the same id, on every exam.
#   - Collisions de-duplicated with numeric suffix (_2, _3, …) by the manifest writer.
#   - INDEPENDENT of concept_group. concept_group is for DOUBT-3 intra-mock
#     uniqueness (a different concern); subtopic_id is purely the cross-step join key.
#
# WHAT IS LOAD-BEARING vs DECORATIVE:
#   - subtopic_id  = LOAD-BEARING. Never reworded. The machine joins on this.
#   - display name (the "--- Subtopic: X ---" heading) = DECORATIVE. May be
#     reworded freely WITHOUT breaking the pipeline, because nothing joins on it.
#
# MANDATE DATA IS STRUCTURED, NOT PROSE:
#   The manifest carries, per subtopic:
#     mandates.mandatory_every_mock   (bool)
#     mandates.alternation_group      (str|null — members must NOT co-occur in a mock)
#     mandates.min_per_series_window  (int|null)
#   plus top-level convenience lists: mandatory_every_mock[], alternation_groups{}.
#   To declare a subtopic mandatory: author its NOTE with an explicit
#   "MANDATORY ... every mock" / "MANDATORY per mock" marker (Step 5 extracts it).
#   To declare an alternation pair: set alternation_group on both members
#   (e.g. both Simple Interest and Compound Interest → alternation_group: "ci_si").
#   Downstream steps read these as DATA; they never re-parse prose to rediscover them.
#
# COMPLETENESS REQUIREMENT (v2.20 — closes the closed-world assumption gap):
#   The manifest must cover the ENTIRE exam taxonomy, not just the PYQ-observed
#   subset. A PYQ-only manifest is a PARTIAL vocabulary that will break when the
#   blueprint (Step 6) includes syllabus-only subtopics.
#
#   INVARIANT:  len(manifest_subtopics) >= len(taxonomy_subtopics)
#
#   The manifest may have MORE entries than the taxonomy (PYQ-discovered subtopics
#   finer than taxonomy granularity — e.g., taxonomy says "Geometry" but PYQs
#   revealed "Triangles", "Circles", "Coordinate Geometry"). That is correct.
#   The manifest must NEVER have FEWER taxonomy-defined subtopics.
#
#   HOW IT HOLDS: run_synthesise() calls taxonomy_sync_entries() (§15-1) AFTER
#   building PYQ-based entries and BEFORE writing section_rules + manifest.
#   Taxonomy sync adds scaffold entries for every taxonomy subtopic absent from
#   the PYQ-derived set. The manifest is therefore COMPLETE by construction.
#
#   WHY THE PRE-v2.20 SPEC MISSED THIS: the contract assumed a CLOSED-WORLD
#   model where every subtopic the blueprint needs would have been observed in
#   PYQs and therefore minted by Step 5. The OPEN-WORLD reality is that exams
#   routinely have syllabus-defined subtopics with zero PYQ history (new syllabus
#   additions, rarely-tested topics, partial PYQ availability). This is the
#   COMMON CASE — not an edge case.
#
# FUTURE-PROOFING (why this can't drift again, across 100 exams):
#   1. Ids are minted ONCE, by ONE step, from a fixed recipe.
#   2. Downstream steps copy ids verbatim or FAIL LOUD (no silent fallback).
#   3. Step 6 and Step 7 each run a CONTRACT GATE at startup: every subtopic_id
#      they reference MUST exist in the manifest; an unknown id = HARD STOP naming
#      the offending id. A name that drifts can no longer silently disappear.
#   4. The recipe and contract contain zero exam-specific values.
#   5. Taxonomy sync (v2.20) ensures the manifest covers the COMPLETE vocabulary.
#      Step 6 NEVER self-mints an id — it HARD STOPS if any subtopic is missing.
#
# DEFINITION OF DONE additions (v2.4):
#   [10] [ExamCode]_subtopic_manifest.json written and delivered via present_files.
#   [11] Every --- Subtopic: --- block has a subtopic_id as its first field.
#   [12] User uploaded subtopic_manifest.json to the project Files section
#        alongside section_rules.md (Step 6 and Step 7 both require it).
#
# DEFINITION OF DONE additions (v2.20):
#   [22] Taxonomy sync ran: run_synthesise printed "Taxonomy sync:" summary line.
#   [23] Completeness invariant holds: manifest subtopic count >= taxonomy subtopic count.
# DEFINITION OF DONE additions (v2.24.6 — FIX B/C):
#   [24] Frequency Excel completeness invariant holds (master_data_completeness_test):
#        set(master_data_subtopic_ids) == set(manifest_subtopic_ids) —
#        aggregate_frequency_data(progress, all_entries=...) printed no
#        "master_data_completeness_test would FAIL" WARN.
#   [25] Excel Format == manifest Format for every subtopic (excel_manifest_format_parity_test)
#        — guaranteed by construction when all_entries is passed (both read entry['format']
#        from the same dict).
#   [26] DI/PASSAGE detection uses the structural _looks_like_table_stimulus() helper
#        (di_heuristic_false_positive_test) — word-boundary + pipe-row signal, not a bare
#        substring match; "vegetable"/"acceptable"/stray single pipes no longer false-positive.
# ════════════════════════════════════════════════════════════════════════
#
# ════════════════════════════════════════════════════════════════════════
# §15-1 — TAXONOMY SYNC PROTOCOL (v2.20 — zero-PYQ manifest completeness)
# ════════════════════════════════════════════════════════════════════════
#
# WHAT: After PYQ-based synthesis produces the entry list, synchronise it
#   with the exam's approved taxonomy. For every taxonomy-defined subtopic
#   NOT already in the PYQ-derived entries, create a scaffold entry with
#   zero-PYQ defaults. These scaffolds flow through the normal
#   write_section_rules() and write_subtopic_manifest() paths, AND (v2.24.6
#   FIX B) through generate_frequency_xlsx() via the all_entries parameter —
#   so the Frequency Excel is now ALSO complete by construction, not just
#   section_rules.md and the manifest. Previously the Excel was derived from
#   `progress` only (PYQ-observed keys), so Zero-PYQ scaffolds could never
#   appear in it regardless of how complete the manifest itself was.
#
# WHEN: Called by run_synthesise() AFTER the PYQ-based entry loop and
#   BEFORE QV checks, write_section_rules(), and write_subtopic_manifest().
#
# IMPLEMENTATION: taxonomy_sync_entries() + make_zero_pyq_scaffold_entry()
#   (defined in §5 code after make_subtopic_id). Full docstrings and edge
#   case handling (EC-ZP-1 through EC-ZP-10) are in those function bodies.
#
# TAXONOMY SOURCES (priority order — UNION, not primary/fallback):
#   1. [ExamCode]_taxonomy_draft.json (Step 2a output — PRIMARY, contains
#      ALL syllabus subtopics including zero-PYQ ones)
#   2. Approved Analysis doc [ExamCode]_PYQ_Analysis.docx (Step 2c output —
#      ADDITIONAL, covers PYQ-discovered subtopics not in taxonomy_draft)
#   Both sources are loaded and unioned. If neither is found, sync SKIPS
#   with a logged warning.
#
# SCAFFOLD ENTRY SHAPE: a complete entry dict with all format_entry() fields,
#   observed_count=0, confidence='absent', generic P1 stem pattern, zero
#   difficulty calibration, and a NOTE identifying it as syllabus-only.
#   See make_zero_pyq_scaffold_entry() for the full field list.
#
# POST-SYNC STATE:
#   all_entries[] contains BOTH PYQ-derived entries AND zero-PYQ scaffolds.
#   write_section_rules() iterates all_entries → scaffold blocks appear in
#   section_rules.md alongside PYQ-derived blocks.
#   write_subtopic_manifest() iterates all_entries → scaffold subtopics
#   get proper slugified subtopic_ids in the manifest.
#   The manifest is COMPLETE by construction. Step 6 can never encounter
#   an unresolvable subtopic.
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §16 — FREQUENCY XLSX OUTPUT (v2.13 — PYQ frequency analysis spreadsheet)
# ════════════════════════════════════════════════════════════════════════
#
# PURPOSE:
#   Generate [ExamCode]_PYQ_Frequency.xlsx during the synthesis phase.
#   This xlsx is a mandatory input to Step 6 (MockBlueprint).
#   All data sourced from analysis_progress.json — no new extraction needed.
#
# DOWNSTREAM CONSUMER:
#   Step 1 reads: Subject, Topic, Sub-Topic, Format, year-wise Qs, Avg/Paper,
#   Consistency, Trend, Importance, Must Prepare.
#
# INTEGRATION:
#   Called automatically at end of run_synthesise(), after section_rules.md
#   and subtopic_manifest.json are written. Added to present_files delivery.

---

## §16-1 — DATA AGGREGATION FROM PROGRESS JSON

```python
# §16-1 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   aggregate_frequency_data(), extract_year_from_paper_id()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-2 — DERIVED METRICS COMPUTATION

```python
# §16-2 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   compute_derived_metrics(), compute_ranks()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-3 — XLSX SHEET SPECIFICATIONS

```
The Frequency xlsx has the following sheets:

SHEET 1: "Summary Dashboard"
  - Title with exam code, year range, paper count, question count
  - Year-wise overview table (papers, Qs, avg Qs/paper, per-section breakdown)
  - Top 25 most-asked subtopics (combined Qs, avg/paper, consistency, trend, importance)
  - Must Prepare section, New-in-latest-year section, Never-appeared section
  - Importance tag legend

SHEET 2: "Master Data (N Years)"
  - Full row per subtopic: Subject, Topic, Sub-Topic, Format
  - Year-wise Qs columns, Combined Qs
  - Year-wise Avg/Paper columns, Combined Avg/Paper
  - Year-wise Papers-In columns, Combined Papers-In
  - % of Subject, Importance, Consistency, Trend, Must Prepare, Rank in Topic

SHEET 3: "Topic Analysis"
  - One row per topic (aggregated from subtopics)
  - Year-wise Qs, Combined, Avg/Paper, % of Subject, Sub-Topic count

SHEET 4: "Trend Analysis & Charts"
  - Top 20 subtopics by combined avg/paper
  - Year-wise avg/paper values for charting

SHEET 5+: One sheet per section
  - Per-subtopic data within that section
  - Topic, Sub-Topic, Format, year-wise Qs, Combined, Avg, Consistency, Trend, etc.
```

---

## §16-4 — XLSX GENERATION CODE

```python
# §16-4 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   generate_frequency_xlsx()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-5 — SHEET WRITER: SUMMARY DASHBOARD

```python
# §16-5 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   write_summary_dashboard()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-6 — SHEET WRITER: MASTER DATA

```python
# §16-6 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   write_master_data()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-7 — SHEET WRITER: TOPIC ANALYSIS

```python
# §16-7 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   write_topic_analysis()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-8 — SHEET WRITER: TREND ANALYSIS & PER-SECTION

```python
# §16-8 IMPLEMENTATION EXTRACTED (2026-07-31, v2.39.2) to the repo engine file
#   frequency_xlsx.py   —   write_trend_analysis(), write_section_sheet()
# Hash-tracked + bootstrap-verified; byte-identical to the block that lived here
# through v2.39.1. This section retains the CONTRACT; the engine holds the code.
import frequency_xlsx as fx
```

---

## §16-9 — XLSX VALIDATION

```
Before delivering the xlsx, verify ALL 9 items:

  XLSX-F1: Workbook has correct sheet count: 4 + sections_count
  XLSX-F2: Master Data row count = total unique (section, topic, subtopic) keys
  XLSX-F3: Year columns match _meta.years_processed exactly
  XLSX-F4: Combined Qs = sum of all year Qs (verified per row)
  XLSX-F5: papers_per_year values match _meta.papers_processed count per year
  XLSX-F6: Consistency value = count of years where Qs > 0 (per row)
  XLSX-F7: No division-by-zero errors (papers_per_year=0 handled)
  XLSX-F8: Per-section sheet subtopic count = Master Data count for that section
  XLSX-F9: sum(all subtopic Combined Qs) vs exam_config.total_questions:
           if mismatch > 5% → WARN (classification gaps exist)
           if mismatch > 25% → HARD WARN (downstream blueprint will be inaccurate)
           Note: XLSX-F9 requires exam_config.json. If absent, skip with note.
```

---

## §16-10 — FREQUENCY XLSX EDGE CASES

```
EC-F1: EXAM WITH ONLY 1 YEAR OF DATA
  Trend = "Insufficient Data". Single year column. Structure unchanged.

EC-F2: SUBTOPIC WITH 0 QUESTIONS ACROSS ALL YEARS
  Appears in Master Data with all zeroes. Consistency=0. Trend="No Data".
  Importance="Low". These are taxonomy subtopics with no PYQ observed (Zero-PYQ
  scaffolds). v2.24.6 FIX B: now reachable-by-construction — aggregate_frequency_data
  seeds every all_entries subtopic (PYQ + Zero-PYQ) BEFORE scanning progress, so this
  row exists even though it has no progress[] key. Was previously UNREACHABLE via the
  taxonomy-sync path (progress-only iteration structurally excluded Zero-PYQ scaffolds) —
  this note was aspirational until v2.24.6 closed the gap (see Framework_Blueprint FIX A/B).

EC-F3: VERY LARGE NUMBER OF YEARS (10+)
  Columns grow linearly. No structural issue.

EC-F4: SECTION NAME TOO LONG FOR SHEET TAB
  Truncate: section[:31].replace('/', ' '). Excel 31-char limit.

EC-F5: PAPERS_PER_YEAR = 0 FOR A YEAR
  Avg/Paper = 0 for that year (division guarded).

EC-F6: FORMAT DETECTION UNCERTAINTY (v2.24.6 FIX B — REVISED)
  When all_entries is supplied (the standard run_synthesise path), Format is taken
  directly from entry['format'] — the SAME 4-way TEXT/FIGURAL/PASSAGE/DI value
  synthesise_subtopic computed and write_subtopic_manifest() writes to the manifest.
  There is no separate "detection uncertainty" in this path: Excel Format == manifest
  Format by construction, not by chance. TEXT-as-default only applies in the backward-
  compat path (all_entries=None) or for a genuinely absent/malformed value.
  Step 6 (Framework_Blueprint v1.32+) no longer reads Format from this xlsx at all —
  the manifest is authoritative there; this Excel Format column is advisory-only
  (cross-check, ref Blueprint §6 S6-1b).
```

# ════════════════════════════════════════════════════════════════════════

# END OF Framework_MockTestAnalyse v2.53.3
