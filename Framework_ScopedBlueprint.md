# Framework_ScopedBlueprint v1.5 — Universal Subject / Topic / Sub-Topic Test Blueprint
#
# v1.5 — 2026-07-15 — FEATURE: qualified subtopic scope "Subject::Topic::SubTopic" (§2 S2-1,
#   additive). The subtopic level now accepts three forms — (1) exact subtopic_id, (2) NEW
#   "Subject::Topic::SubTopic" (narrows by section+topic, then matches display_name WITHIN that
#   topic — so a name only has to be unique within its topic, not globally), (3) bare display
#   name if globally unique — all resolving to a single subtopic_id before anything else runs.
#   Zero downstream impact (resolution happens pre-emit). Clear HARD STOPs on wrong part-count,
#   no-match (lists sub-topics under the topic), or intra-topic name collision (lists the ids).
#   Proven by blueprint_scoped_scope_test.py + an e2e qualified-scope run.
#
# v1.4 — 2026-07-15 — CRITICAL FIX #3: emit subtopic_list answer_type + answer_cardinality (nested
#   consumer-contract audit). Step 11's tag JOIN reads subtopic_list[].answer_type /
#   .answer_cardinality (the mock emits them) to tag question type; §8-1 omitted both, so Step 11
#   defaulted every scoped question to MCQ-single — mis-tagging NAT/MSQ subtopics. Fix: §1-3 parses
#   both from section_rules via the new pure engine bc.parse_section_rules_field, and §8-1 emits them
#   per subtopic. Found by diffing NESTED field reads (subtopic_list/section/allocation) against §8
#   emits. Locked by e2e (8/8: NAT/MSQ values survive to subtopic_list). Engine: +parse_section_rules_field
#   (self-test 33/33).
#
# v1.3 — 2026-07-15 — CRITICAL FIX #2: emit batch_size_qs (consumer-contract audit). Steps 7/8 read
#   the axis-2 WINDOW size as bp.get('batch_size_qs', 10); §6 built axis_schedule for a window of
#   batch_size papers, but §8 never emitted batch_size_qs → a non-default --batch_size silently fell
#   back to 10 and mis-audited the axis-2 window. Fix: §8 emits 'batch_size_qs': batch_size. Found by
#   diffing every blueprint field Steps 7-11 READ against what §8 EMITS (the integration seam the
#   in-isolation e2e can't see). Locked by a non-default-batch_size assertion in the e2e (8/8).
#
# v1.2 — 2026-07-15 — CRITICAL FIX: blueprint_version emitted the SCHEMA version, not SCOPED_VERSION.
#   §8 had emitted 'blueprint_version': SCOPED_VERSION ('1.0'); Step 7 gates blueprint_version against
#   MIN_BLUEPRINT_VERSION=(1,7) → _ver_tuple('1.0')=(1,0) < (1,7) HARD-STOPPED every scoped generation.
#   Fix: emit BLUEPRINT_SCHEMA_VERSION='1.23' (the shared blueprint.json schema version the mock also emits;
#   passes the floor); SCOPED_VERSION is preserved as scope.scoped_spec_version. The scoped e2e never
#   caught it (it runs the blueprint, not Step 7's gate) — now locked by an emitted-version floor
#   assertion in blueprint_scoped_emit_test.py (6/6) + blueprint_scoped_e2e_test.py (7/7).
#
# v1.1 — 2026-07-15 — REGISTRY SCHEMA SYNC (seed only; zero logic). The §8-7 fresh-registry seed now
#   includes semantic_usage=[] and exhausted_subtopics={} to MATCH the shared schema written by the
#   generation layer (MockCreate v5.22 B) and the mock Blueprint v1.30 seed. Additive; byte-schema-
#   identical to what Step 7 would self-heal. No allocation/emit/behaviour change.
#
# v1.0 — 2026-07-15 — RELEASE. Feature-complete (§1–§10) and adversarially verified. Two full
#   QA passes (end-to-end trace + line-by-line) found and fixed 11 bugs; 0 remain. Verified by:
#   validate_framework_md.py (0 issues, all AST clean); blueprint_scoped_e2e_test.py 7/7 (EXECUTES
#   the assembled spec against mock inputs — fresh/subject/topic/subtopic runs, duplicate-display-
#   name survival, resumption, old-registry migration, batch_size default, axis-schedule keys, and
#   a static scan asserting NO undefined name in any branch); section harnesses alloc 7/7,
#   difficulty 10/10, format 6/6, emit 5/5, resume 7/7; engine self-test 30/30, core_test 20/20,
#   qa_pass2 6/6; pyflakes-clean embedded Python; every bc.* reference resolves to the engine.
#   Blueprint math is the shared engine blueprint_core.py (identical to Framework_Blueprint v1.28).
#   Remaining (separate deliverables, NOT this spec): the generation layer (Step-7 analog) — shared
#   sharded registry, mock_n→paper_id generalisation of Steps 7–11, (item × angle)/spacing-8
#   uniqueness — governed by the §9 registry contract.
#
# v0.1-qa — 2026-07-15 — ADVERSARIAL QA REMEDIATION (end-to-end, two-pass). The per-section
#   harnesses proved every ALGORITHM but supplied inputs as fixtures, so the spec's own
#   data-loading glue and cross-section keying were never exercised. End-to-end tracing found
#   and fixed 8 bugs: (1-4) exam_config / section_rules / excel / flag were USED but never
#   loaded/defined -> added the loads in §1-3 (section_rules via the new pure engine parser
#   bc.parse_section_rules_difficulty) + the flag helper; (5) DISPLAY-NAME KEYING collapsed
#   subtopics that share a display name within a scope -> re-keyed r_avg/allocation/emit to
#   subtopic_id end-to-end (Excel keyed by the taxonomy triple); (6) paper_start was used in
#   §8 but defined in §9 (after) -> relocated the registry load/gates to §1-4 and the resume
#   offset to §2-4, so paper_id numbering resumes correctly (no collisions); (7) registry load
#   misplaced -> §1-4; (8) engine mandate hardened to always import the freshly-copied engine.
#   Now proven by blueprint_scoped_e2e_test.py (6/6: EXECUTES the assembled spec against mock
#   inputs — fresh/subject/topic/subtopic runs, duplicate-display-name survival, resumption,
#   old-registry migration, AND a static scan asserting NO undefined name in any branch) plus
#   the five section harnesses (alloc 7/7, difficulty 10/10, format 6/6, emit 5/5, resume 7/7).
#   Engine: bc.parse_section_rules_difficulty added (self-test 30/30, core_test 20/20).
#
# v0.1 — 2026-07-15 — INITIAL DRAFT. Built: §1 (session start, engine mandate, trigger,
#   manifest load), §2 (scope selection + synthetic section), §3 (frequency), §4 (scoped
#   allocation: per-batch independent allocation, coverage floor, Zero-PYQ floor, EC-11
#   gate), §5 (difficulty: batch-local envelope-bounded ramp + cascade), §6 (format: hybrid
#   per-scope three-axis signature — SUBJECT scope uses the precomputed subject distribution;
#   TOPIC/SUBTOPIC rescope axis-2 from in-scope observed_axis2 and inherit axis-1/3 from the
#   subject; ALL THREE axes renormalised to Q; zero-PYQ topic→subject→default cascade;
#   section-relabel so the engine's pool-caps/feasibility filter matches in-scope ids).
#   NOTE: bc.largest_remainder_apportion assumes its input sums to ~target (true for the mock,
#   where real per-paper counts ≈ sec_qs); §6 normalises all three axes to Q so the internal
#   apportionment deficit stays ~0 (a real-per-paper input summing >> Q would trip the
#   apportioner's iteration guard and truncate — avoided by normalising, NOT an engine change).
#   Proven: §4 blueprint_scoped_alloc_test.py 7/7; §5 blueprint_scoped_difficulty_test.py
#   10/10; §6 blueprint_scoped_format_test.py 6/6; §7+§8 blueprint_scoped_emit_test.py
#   5/5 (marking tier selection + full blueprint.json schema completeness). Built §7 (marking:
#   modal tier for multi-tier subjects) + §8 (emit: complete blueprint.json in the exact shape
#   Steps 7-11 read, single-section, per-paper paper_id). §9 (resumption: shared-registry
#   load/seed, exam_code + taxonomy-drift + completeness HARD-STOP gates, auto-migration of old
#   mock-only registries [snapshot→migrate→verify→idempotent], per-scope paper_id counter resume,
#   append-only tier-agnostic, + the generation-layer registry CONTRACT) — blueprint_scoped_resume_test.py
#   7/7. ALL §1-§9 BUILT (feature-complete draft). Pending: full adversarial QA, then v0.1 → v1.0.
#
# ═══════════════════════════════════════════════════════════════════════════
# WHAT THIS IS (and is NOT)
#   IS  : an ALLOCATION spec — decides how many questions per in-scope subtopic per
#         paper, across a series of N scoped test papers, plus the difficulty and
#         format targets each paper must hit. Output = blueprint.json (per scope).
#   NOT : a GENERATION spec. Question creation, the shared cross-paper registry, the
#         (item × angle) uniqueness unit, the spacing-gap-8 controlled reuse, and the
#         per-subtopic exhaustion flag are all GENERATION-TIME concerns handled by the
#         Step-7 analog (a later deliverable). This file never writes questions.
# ═══════════════════════════════════════════════════════════════════════════
#
# PIPELINE POSITION:
#   Step 5:  PYQExtract        ← publishes subtopic_manifest.json + section_rules.md
#   Step 6:  MockBlueprint     ← the FULL-EXAM blueprint (Framework_Blueprint.md)
#   Step 6S: ScopedBlueprint   ← THIS SPEC — one scoped series per (level, scope)
#   Step 7:  MockCreate / ScopedCreate  ← SHARED generator (reads blueprint.json)
#   Step 8:  MockCreateAudit
#   Step 9:  MockExplain
#   Step 10: MockExplainAudit
#   Step 11: MockDeliver
#
#   Step 6S is INDEPENDENT of Step 6 (mock) — a project may have mocks, scoped tests,
#   both, or neither, generated in any order (append-only, tier-agnostic — see §9).
#   Step 6S consumes the SAME Step-5 outputs the mock Blueprint does.
#
# ═══════════════════════════════════════════════════════════════════════════
# STEP NUMBER NOTE
#   "Step 6S" is a label of convenience — this spec is a scoped VARIANT of the
#   canonical Step 6. It uses the same B1/B2/B3 phase shorthand where helpful.
# ═══════════════════════════════════════════════════════════════════════════
#
# SOURCES OF TRUTH (load at session start — in priority order):
#   1. This spec (Framework_ScopedBlueprint.md)        — rules + procedures
#   2. blueprint_core.py (SHARED ENGINE)               — all allocation math (S1-2b)
#   3. exam_config.json (from Step 5/2a)               — marking_scheme, medium, level
#   4. [ExamCode]_subtopic_manifest.json (from Step 5) — taxonomy + subtopic_id +
#                                                        per-subtopic axis/format data
#   5. [ExamCode]_section_rules.md (from Step 5)       — per-subtopic PYQ patterns +
#                                                        observed difficulty (for §5/§6)
#   6. Frequency Excel / Analysis docs                 — r_avg inputs (same as mock)
#   7. [ExamCode]_registry.json (prior papers)         — cross-paper dedup (read in §9)
#
# TRIGGER FORMAT:
#   Step 6S: ScopedBlueprint --level <subject|topic|subtopic> --scope "<SCOPE>"
#            --count N --qs_per_paper Q [--batch_size B] [--difficulty progressive]
#
#   Trigger matching is case-insensitive. ExamCode read from exam_config.json.
#   --level      : subject | topic | subtopic (REQUIRED)
#   --scope      : the scope target (REQUIRED). Grammar per §2 S2-1:
#                    subject   → "Subject Name"                (matches manifest section)
#                    topic     → "Subject Name::Topic Name"    (subject-qualified)
#                    subtopic  → the subtopic_id (e.g. ST0042), OR a bare display name if
#                                globally unique, OR "Subject::Topic::SubTopic" (v1.5) which
#                                pins the name within its topic (falls back to the id only if
#                                two sub-topics share the name under that exact topic).
#   --count N    : number of test papers in this scoped series (positive int > 0;
#                  flag if > 200). This is the per-run count you asked for
#                  (e.g. 10 subject tests, 20 topic tests, 15 sub-topic tests).
#   --qs_per_paper Q : questions per paper (positive int > 0). No exam-pattern total
#                  exists for a scoped test, so it MUST be supplied.
#   --batch_size B   : optional (default 10). The batch window; also the coverage
#                  window (every in-scope subtopic appears ≥1 per batch) AND the unit
#                  of the batch-local difficulty ramp (§5). Papers are generated in
#                  batches of B, exactly like the mock B2 loop.
#   --difficulty progressive : optional. Default IS a batch-local easy→hard ramp
#                  (§5); this flag is accepted for symmetry with the mock trigger.
#
#   Examples:
#     ScopedBlueprint --level subject   --scope "Physics"            --count 10 --qs_per_paper 50
#     ScopedBlueprint --level topic     --scope "Physics::Mechanics" --count 20 --qs_per_paper 30
#     ScopedBlueprint --level subtopic  --scope ST0042               --count 15 --qs_per_paper 25
#     ScopedBlueprint --level subtopic  --scope "Physics::Mechanics::Kinematics" --count 15 --qs_per_paper 25
#
# OUTPUT FILES (all with [ExamCode] prefix + scope tag):
#   [ExamCode]_[SCOPETAG]_blueprint.json   — authoritative allocation for this series
#   [ExamCode]_[SCOPETAG]_blueprint.xlsx   — human review
#   (registry.json is SHARED per exam and is updated at GENERATION time, not here.)
#   SCOPETAG = e.g. SUBJ_Physics / TOPIC_Physics_Mechanics / SUBTOPIC_ST0042 (§8).
#
# EXAM-AGNOSTIC GUARANTEE:
#   Zero hardcoded exam values. Scope, counts, and Q/paper are read from the trigger;
#   subtopics, r_avg, formats, and difficulty come from the Step-5 outputs.
#
# ═══════════════════════════════════════════════════════════════════════════

## §1 — SESSION START

Run every step below before writing a single line of B1. No exceptions.

### S1-1 — Trigger parse

```
Parse and validate the trigger:
  ExamCode      : from exam_config.json in the project (as in the mock Blueprint).
  --level       : must be one of {subject, topic, subtopic}. Else → ERROR + re-ask.
  --scope       : required non-empty string. Interpreted per §2 S2-1 by --level.
  --count N     : positive integer > 0. If ≤ 0 / non-integer → ERROR.
                  If > 200 → flag: "count = [N] papers is unusually large. Confirm."
  --qs_per_paper Q : positive integer > 0. If missing → ERROR:
                  "--qs_per_paper is required (a scoped test has no exam-pattern total)."
  --batch_size B : optional, default 10. Positive integer > 0.
  --difficulty  : optional; 'progressive' accepted (default behaviour anyway, §5).

  If --level or --scope or --count or --qs_per_paper is missing → ERROR listing the
  missing flag(s) and the trigger format. Never guess a scope or a count.
```

### S1-2 — File inventory

```
List ALL received / project files immediately after trigger:

  "Received / project files:
   • blueprint_core.py                    (SHARED ENGINE)          [present? ✓/✗]
   • [ExamCode]_subtopic_manifest.json    (Step 5)                 [present? ✓/✗]
   • [ExamCode]_section_rules.md          (Step 5)                 [present? ✓/✗]
   • exam_config.json                     (Step 5/2a)              [present? ✓/✗]
   • Frequency Excel / Analysis docs      (r_avg inputs)           [present? ✓/✗]
   • [ExamCode]_registry.json             (prior papers, optional) [present? ✓/✗]"

Mandatory for Step 6S: blueprint_core.py (S1-2b), subtopic_manifest.json, exam_config.json,
and the r_avg inputs (Frequency Excel or Analysis docs — the same missing-input fallback
chain the mock Blueprint uses). section_rules.md is required for §5 (difficulty envelope)
and §6 (format). If any mandatory input is missing → HARD STOP naming it.
```

### S1-2b — Allocation engine mandate (blueprint_core.py — HARD STOP)

```
# ════════════════════════════════════════════════════════════════════════
# MANDATE — blueprint_core.py IS MANDATORY (HARD STOP)  [identical to mock S1-2b]
# ════════════════════════════════════════════════════════════════════════
#   All allocation MATH in this spec is provided by the SHARED ENGINE
#   blueprint_core.py — the SAME engine the mock Blueprint uses, so scoped and mock
#   allocation can never drift. It is universal (no exam-specific edits, no
#   [ExamCode] prefix; uploaded once, reused in every project). Its correctness is
#   proven by blueprint_core_test.py + qa_pass2_differential.py.
#
#   If blueprint_core.py is absent from the project → HARD STOP. Print:
#     "HARD STOP (ENGINE MANDATE): blueprint_core.py not found in the [ExamCode]
#      project Files. Step 6S cannot allocate without it. It is universal (uploaded
#      once, reused in every project) — upload it, then re-run ScopedBlueprint."
```

```python
import os, shutil, subprocess, sys, re as _re

# 1) PRESENCE GATE
_engine_src = '/mnt/project/blueprint_core.py'
if not os.path.exists(_engine_src):
    raise SystemExit(
        "HARD STOP (ENGINE MANDATE): blueprint_core.py not found in the [ExamCode] "
        "project Files. Step 6S cannot allocate without it. It is universal (uploaded "
        "once, reused in every project) — upload it, then re-run ScopedBlueprint.")

# 2) COPY TO WORKING DIR so `import blueprint_core` resolves the PROJECT's engine (cwd =
#    /home/claude). Prioritise it on sys.path and drop any stale cached import so the copy
#    just made — the project's current engine — is the one that loads.
shutil.copy(_engine_src, '/home/claude/blueprint_core.py')
sys.path.insert(0, '/home/claude')
sys.modules.pop('blueprint_core', None)

# 3) HEALTH GATE — the engine must self-test clean before we trust it.
_st = subprocess.run([sys.executable, '/home/claude/blueprint_core.py', '--self-test'],
                     capture_output=True, text=True, timeout=60)
_out = (_st.stdout + _st.stderr).strip().splitlines()
_last = _out[-1] if _out else ''
if _st.returncode != 0 or not _re.match(r'SELF-TEST: (\d+)/\1 PASS', _last):
    raise SystemExit(
        f"HARD STOP (ENGINE MANDATE): blueprint_core.py --self-test did not pass "
        f"({_last!r}). Re-upload the delivered blueprint_core.py and re-run.")

# 4) IMPORT — every §3/§4/§5/§6 block uses `bc`.
import blueprint_core as bc
```

### S1-3 — Load inputs (exam_config, manifest, section_rules) + the flag helper

```python
import json, os

# Non-fatal diagnostic helper — defined ONCE, used everywhere (§3/§6/§7/§9).
_FLAGS = []
def flag(msg):
    _FLAGS.append(str(msg))
    print(f"[FLAG] {msg}")

# exam_config.json — REQUIRED (drives EXAM, the §7 marking, and the §8 top-level fields).
cfg_path = '/mnt/project/exam_config.json'
if not os.path.exists(cfg_path):
    raise SystemExit("HARD STOP: exam_config.json not found in the project. Step 5/2a must "
                     "publish it before Step 6S. Upload it and re-run ScopedBlueprint.")
exam_config = json.load(open(cfg_path, encoding='utf-8'))
EXAM = exam_config['exam_code']

# subtopic_manifest.json — REQUIRED (taxonomy + per-subtopic axis/format data).
manifest_path = f'/mnt/project/{EXAM}_subtopic_manifest.json'
if not os.path.exists(manifest_path):
    raise SystemExit(f"HARD STOP: {EXAM}_subtopic_manifest.json not found. Step 5 must publish "
                     f"it before Step 6S. Run/re-run Step 5, upload the manifest, then re-run.")
manifest     = json.load(open(manifest_path, encoding='utf-8'))
MANIFEST_IDS = manifest['subtopics']   # subtopic_id -> {display_name, section(=subject), topic,
                                       #                 format, axis2_capability, observed_axis2, ...}

AXIS2_CAP_BY_ID      = {k: v.get('axis2_capability', ['DIRECT']) for k, v in MANIFEST_IDS.items()}
OBSERVED_AXIS2_BY_ID = {k: v.get('observed_axis2', {})           for k, v in MANIFEST_IDS.items()}
FORMAT_BY_ID         = {k: v.get('format', 'TEXT')               for k, v in MANIFEST_IDS.items()}
slugify = bc.slugify   # engine slugify (byte-identical to Step 0 — id matching preserved)

# section_rules.md — REQUIRED for §5 (difficulty envelope). The ENGINE parses its text into
# {subtopic_id: {level: is_inferred}} (pure — no I/O in the engine; the file is read here).
sr_path = f'/mnt/project/{EXAM}_section_rules.md'
if not os.path.exists(sr_path):
    raise SystemExit(f"HARD STOP: {EXAM}_section_rules.md not found. Step 5 must publish it "
                     f"(§5 reads its PYQ_DIFFICULTY_CALIBRATION). Upload it and re-run.")
_sr_text = open(sr_path, encoding='utf-8').read()
SECTION_RULES_DIFF = bc.parse_section_rules_difficulty(_sr_text)
# Per-subtopic question-type dispatch fields (section_rules; mock parity). Step 11 tags scoped
# papers by these, so subtopic_list MUST carry them or every question defaults to MCQ-single.
ANSWER_TYPE = bc.parse_section_rules_field(_sr_text, 'answer_type', 'option')          # option|numerical
ANSWER_CARD = bc.parse_section_rules_field(_sr_text, 'answer_cardinality', 'single')   # single|multi

# NOTE (v0.1): Step 6S does NOT read mandatory_every_mock / alternation_groups / min_counts /
# cadence_windows — those are FULL-EXAM pattern mandates (mock Blueprint only). A scoped test
# has no exam-pattern to replicate, so the mandate engine is intentionally absent here.
```

### S1-4 — Shared registry: load, exam_code gate, migrate, drift + completeness gates

The registry is SHARED per exam (mocks + every scoped tier). It is loaded and gated HERE at
session start because §8's paper_id numbering resumes from it (the per-scope offset is computed
in §2 S2-4, once PAPER_PREFIX exists). The append-only / tier-agnostic semantics and the
generation-layer contract are documented in §9.

```python
import shutil, datetime
SCOPED_SCHEMA = '2.0-scoped'
reg_path = f'/mnt/project/{EXAM}_registry.json'
if os.path.exists(reg_path):
    registry = json.load(open(reg_path, encoding='utf-8'))
    _new_registry = False
else:
    registry = None            # fresh exam — a template is seeded in §8-7
    _new_registry = True

# exam_code gate
if registry is not None and registry.get('exam_code') not in (EXAM, None):
    raise SystemExit(f"HARD STOP: registry exam_code {registry.get('exam_code')!r} != {EXAM!r}. "
                     f"Wrong registry for this exam — do not cross-contaminate dedup state.")

# auto-migration (old mock-only '1.0' → generalised paper_id schema). Format-only; idempotent.
if registry is not None and registry.get('schema_version') != SCOPED_SCHEMA:
    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    shutil.copy(reg_path, f'{reg_path}.pre-migration-{ts}.bak')           # snapshot
    old_mocks = list(registry.get('mocks_completed', []))
    migrated = list(registry.get('papers_completed', []))
    for m in old_mocks:
        pid = f"MOCK:M{int(m):02d}"
        if pid not in migrated:
            migrated.append(pid)
    registry['papers_completed'] = migrated
    for entry in registry.get('question_index', []):
        if 'paper_id' not in entry and 'mock' in entry:
            entry['paper_id'] = f"MOCK:M{int(entry['mock']):02d}"
    registry['schema_version'] = SCOPED_SCHEMA
    assert all(f"MOCK:M{int(m):02d}" in registry['papers_completed'] for m in old_mocks), \
        "registry migration lost a mock paper — aborting (snapshot retained)."
    json.dump(registry, open(reg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    flag(f"Registry migrated 1.0 → {SCOPED_SCHEMA} (snapshot: {reg_path}.pre-migration-{ts}.bak). "
         f"{len(old_mocks)} mock paper(s) tagged with paper_id. Format-only; no question changed.")

# taxonomy-drift + completeness gates (HARD STOP)
if registry is not None:
    prior_ids = {q.get('subtopic_id') for e in registry.get('question_index', [])
                 for q in e.get('questions', []) if q.get('subtopic_id')}
    drifted = sorted(sid for sid in prior_ids if sid not in MANIFEST_IDS)
    if drifted:
        raise SystemExit(
            f"HARD STOP (taxonomy drift): {len(drifted)} subtopic_id(s) in prior papers no longer "
            f"exist in {EXAM}_subtopic_manifest.json (e.g. {drifted[:3]}). The taxonomy changed since "
            f"those papers were generated; adding papers would break strict-global dedup on the moved "
            f"ids. Reconcile the manifest (or re-map the ids) before continuing.")
    indexed = {e.get('paper_id') for e in registry.get('question_index', []) if e.get('paper_id')}
    incomplete = [p for p in registry.get('papers_completed', []) if p not in indexed]
    if incomplete:
        raise SystemExit(
            f"HARD STOP (registry incomplete): {len(incomplete)} paper(s) marked complete but missing "
            f"question_index entries (e.g. {incomplete[:3]}). The registry is stale/partial — dedup "
            f"would be blind to those questions. Restore the correct registry.")
```

## §2 — SCOPE SELECTION

Resolve (--level, --scope) into the exact set of in-scope subtopic_ids, then build the
single synthetic "section" the allocation (§4) and downstream steps operate on. The
taxonomy key `section` means SUBJECT (mock Blueprint §2 note); a subtopic's manifest
entry carries `section` (subject) and `topic`.

### S2-1 — Resolve scope → in-scope subtopic_ids

```python
level = trigger['level']          # 'subject' | 'topic' | 'subtopic'
scope = trigger['scope'].strip()  # raw --scope string

def _entry(sid):        # convenience
    return MANIFEST_IDS[sid]

if level == 'subject':
    # scope = "Subject Name" → every subtopic whose manifest section == scope.
    in_scope_ids = [sid for sid, v in MANIFEST_IDS.items() if v.get('section') == scope]
    scope_subject, scope_topic = scope, None
    if not in_scope_ids:
        _subjects = sorted({v.get('section') for v in MANIFEST_IDS.values()})
        raise SystemExit(
            f"HARD STOP (SCOPE): no subtopics found for subject '{scope}'. "
            f"Known subjects: {_subjects}. Check --scope spelling (exact match).")

elif level == 'topic':
    # scope = "Subject::Topic" — subject-qualified so same-named topics under two
    # subjects never collide (mock Blueprint S2: 'Analogy' under Verbal vs Non-Verbal).
    if '::' not in scope:
        raise SystemExit(
            "HARD STOP (SCOPE): --level topic requires --scope \"Subject::Topic\" "
            "(subject-qualified). Received: " + repr(scope))
    scope_subject, scope_topic = (p.strip() for p in scope.split('::', 1))
    in_scope_ids = [sid for sid, v in MANIFEST_IDS.items()
                    if v.get('section') == scope_subject and v.get('topic') == scope_topic]
    if not in_scope_ids:
        _topics = sorted({v.get('topic') for v in MANIFEST_IDS.values()
                          if v.get('section') == scope_subject})
        raise SystemExit(
            f"HARD STOP (SCOPE): no subtopics for topic '{scope_topic}' under subject "
            f"'{scope_subject}'. Known topics in that subject: {_topics}.")

elif level == 'subtopic':
    # scope anchors on the subtopic_id (the pipeline JOIN key). Three accepted forms, tried in
    # this order — all resolve to a single subtopic_id before anything else runs:
    #   (1) an exact subtopic_id (e.g. ST0042)                    — always unambiguous;
    #   (2) a QUALIFIED name "Subject::Topic::SubTopic" (v1.5)     — narrows by (subject, topic)
    #       first, so a sub-topic name only has to be unique WITHIN its topic;
    #   (3) a bare display name                                    — accepted only if globally UNIQUE.
    # (2) exists because sub-topic display names can repeat across (and even within) topics — so a
    # bare name is often ambiguous, but the qualified form usually pins it without needing the id.
    if scope in MANIFEST_IDS:
        pass                                              # (1) exact subtopic_id
    elif '::' in scope:                                   # (2) qualified Subject::Topic::SubTopic
        _parts = [p.strip() for p in scope.split('::')]
        if len(_parts) != 3:
            raise SystemExit(
                "HARD STOP (SCOPE): a qualified subtopic scope must be "
                "\"Subject::Topic::SubTopic\" (exactly three '::'-separated parts). "
                f"Received {len(_parts)} part(s): {scope!r}")
        _sub, _top, _name = _parts
        _hits = [sid for sid, v in MANIFEST_IDS.items()
                 if v.get('section') == _sub and v.get('topic') == _top
                 and v.get('display_name') == _name]
        if len(_hits) == 1:
            scope = _hits[0]
        elif len(_hits) == 0:
            _names = sorted({v.get('display_name') for v in MANIFEST_IDS.values()
                             if v.get('section') == _sub and v.get('topic') == _top})
            raise SystemExit(
                f"HARD STOP (SCOPE): no sub-topic '{_name}' under '{_sub}::{_top}'. "
                + (f"Sub-topics there: {_names}." if _names
                   else f"No subtopics for topic '{_top}' under subject '{_sub}' "
                        "(check subject/topic spelling — exact match)."))
        else:
            raise SystemExit(
                f"HARD STOP (SCOPE): sub-topic name '{_name}' is AMBIGUOUS under "
                f"'{_sub}::{_top}' ({len(_hits)} share it) — pass the subtopic_id: {sorted(_hits)}.")
    else:                                                 # (3) bare display name (must be global-unique)
        _byname = [sid for sid, v in MANIFEST_IDS.items() if v.get('display_name') == scope]
        if len(_byname) == 1:
            scope = _byname[0]
        else:
            raise SystemExit(
                f"HARD STOP (SCOPE): subtopic '{scope}' is not a manifest subtopic_id"
                + (f" and its display name is AMBIGUOUS ({len(_byname)} matches) — pass the "
                   f"subtopic_id, or qualify it as \"Subject::Topic::SubTopic\"."
                   if len(_byname) > 1
                   else " and no subtopic has that display name. Pass a valid subtopic_id "
                        "(or \"Subject::Topic::SubTopic\")."))
    in_scope_ids = [scope]
    scope_subject = _entry(scope).get('section')
    scope_topic   = _entry(scope).get('topic')

else:
    raise SystemExit(f"HARD STOP (SCOPE): unknown --level '{level}'.")

# Deterministic order: by (topic, display_name) so the synthetic section is stable.
in_scope_ids.sort(key=lambda sid: (str(_entry(sid).get('topic') or ''),
                                   _entry(sid).get('display_name', ''), sid))

print(f"SCOPE: level={level} scope={scope!r} → {len(in_scope_ids)} in-scope subtopic(s).")
```

### S2-2 — Build the single synthetic section

```python
# A scoped test is ONE section. Its subtopics are ordered topic → subtopic (S2-1 sort),
# matching the delivery ordering decision. This mirrors the mock's sections[] entry
# shape so downstream (Steps 7–11) reads it identically — but there is exactly one.
Q = trigger['qs_per_paper']
scope_label = {
    'subject':  scope_subject,
    'topic':    f"{scope_subject} — {scope_topic}",
    'subtopic': _entry(in_scope_ids[0]).get('display_name', in_scope_ids[0]),
}[level]

section = {
    'name':        scope_label,      # OTS display label for this scoped paper
    'q_range':     [1, Q],           # single section spans the whole paper
    'total_qs':    Q,
    'max_attempt': Q,                # no attempt limit for a scoped test
}
sections = [section]                 # exactly one — the whole downstream contract is single-section

# in-scope subtopic display names grouped under this synthetic section (for §3/§4).
in_scope_names = [_entry(sid)['display_name'] for sid in in_scope_ids]  # display only
```

### S2-3 — Scope tag (for filenames + paper_id — full scheme in §8)

```python
def _slug_component(s):
    return slugify(s or '').upper() or 'X'

if level == 'subject':
    SCOPETAG = f"SUBJ_{_slug_component(scope_subject)}"
    PAPER_PREFIX = f"SUBJ:{scope_subject}"
elif level == 'topic':
    SCOPETAG = f"TOPIC_{_slug_component(scope_subject)}_{_slug_component(scope_topic)}"
    PAPER_PREFIX = f"TOPIC:{scope_subject}::{scope_topic}"
else:  # subtopic
    SCOPETAG = f"SUBTOPIC_{in_scope_ids[0]}"
    PAPER_PREFIX = f"SUBTOPIC:{in_scope_ids[0]}"

# paper_id for the k-th NEW paper = f"{PAPER_PREFIX}:{paper_start + k:02d}" (§8), where
# paper_start (S2-4) resumes numbering from any papers of this scope already in the registry.
```

### S2-4 — Per-scope paper_id resume offset (append-only, tier-agnostic)

```python
# Count papers already recorded for THIS scope (its PAPER_PREFIX) in the shared registry
# (loaded in §1-4). New papers CONTINUE the numbering; §8 uses paper_start. Each scope has an
# INDEPENDENT counter (its own prefix) — tiers never share numbering and never block each other.
existing_for_scope = [p for p in (registry.get('papers_completed', []) if registry else [])
                      if p.startswith(PAPER_PREFIX + ':')]
paper_start = len(existing_for_scope)
if paper_start:
    flag(f"Resuming scope {PAPER_PREFIX!r}: {paper_start} paper(s) already recorded; "
         f"new papers numbered {paper_start + 1}..{paper_start + trigger['count']}.")
```

## §3 — FREQUENCY

Compute r_avg per in-scope subtopic — the SAME recency-weighted formula as the mock Blueprint
(bc.compute_r_avg), so scoped and mock frequency can never drift. r_avg drives the §4
proportional split; r_avg == 0 marks a Zero-PYQ subtopic (coverage-floor only, §4).

### S3-1 — Read the Frequency Excel (I/O + structure detection — a Claude step)

Read the Frequency Excel exactly as the mock Blueprint S2-3 does. This is an I/O +
structure-detection step (NOT a pure function — the pure r_avg MATH lives in the engine):

  • Identify the Master Data sheet; read columns by HEADER where present (fallback positional
    A/B/C/D = Subject/Topic/Sub-Topic/Format), plus one 'Avg/Paper [year]' and one
    'Papers In [year]' column per year.
  • Blank Avg/Paper → 0 for that year. Papers In = 0 while Avg/Paper > 0 → data-error flag,
    treat that year as 0 papers (the engine also guards this).
  • Missing year column → 0 papers for that year.

Build the three structures below, KEYED BY THE TAXONOMY TRIPLE (Subject, Topic, Sub-Topic) —
NOT the bare display name — so subtopics that share a display name across topics stay distinct:

```python
# excel_by_key : {(subject, topic, subtopic_display): {year: {'avg': float, 'papers': float}}}
# excel_years  : list of year strings that appear as columns
# valid_years  : years with >0 papers for some subtopic
# (Produced by the Excel read above. If the Frequency Excel is absent, use the mock Blueprint's
#  missing-input fallback — Analysis-doc pooled counts as an r_avg proxy — the identical chain.)
```

### S3-2 — r_avg per subtopic_id (engine)

```python
import blueprint_core as bc
recent_years, older_years = bc.split_recency(valid_years)   # ENGINE (same as mock §3-1)

r_avg = {}
for sid in in_scope_ids:
    e   = MANIFEST_IDS[sid]
    key = (e.get('section'), e.get('topic'), e['display_name'])   # taxonomy triple (disambiguates)
    cells = excel_by_key.get(key, {})
    year_rows = [
        {'avg':    cells.get(y, {}).get('avg'),
         'papers': cells.get(y, {}).get('papers'),
         'recent': y in recent_years}
        for y in excel_years
    ]
    r, _warns = bc.compute_r_avg(year_rows)   # 0.0 → Zero-PYQ (coverage floor in §4)
    r_avg[sid] = r                            # KEYED BY subtopic_id (the canonical key)
    for _w in _warns:
        flag(f"{e['display_name']} [{sid}]: {_w}")   # engine data-quality warnings

# r_avg is keyed by subtopic_id — the canonical key used throughout §4/§6/§8. Duplicate display
# names never collide (the triple Excel key + subtopic_id r_avg keying keep subtopics distinct).
```

## §4 — SCOPED ALLOCATION

Allocate Q questions per paper across the in-scope subtopics for all N papers, r_avg-
weighted, with EVERY in-scope subtopic (PYQ or Zero-PYQ) guaranteed to appear ≥1 in every
batch window. All apportionment is the shared engine (bc). The model is per-BATCH and
independent (mirrors the mock's proven per-window allocation): each batch is a self-
contained mini-allocation, which (a) guarantees coverage even in a small partial last
batch, and (b) makes each batch a clean unit for the batch-local difficulty ramp (§5).

### S4-0 — Parameters

```python
import math
import blueprint_core as bc
Q          = trigger['qs_per_paper']      # questions per paper (S1-1)
N          = trigger['count']             # papers in this series
batch_size = trigger.get('batch_size', 10)  # optional; documented default 10 (S1-1)
n_batches  = math.ceil(N / batch_size)
# papers in each batch (last may be smaller); global paper index k = 1..N
papers_per_batch = [min(batch_size, N - b * batch_size) for b in range(n_batches)]
n_subs = len(in_scope_ids)              # in-scope subtopics (§2); r_avg[...] from §3
```

### S4-1 — Feasibility gate (EC-11 scoped)

```python
# Every in-scope subtopic must appear ≥1 in EVERY batch. The tightest window is the
# SMALLEST batch (the partial last one when N % batch_size != 0): it has
# min_papers × Q slots and must still hold one of each subtopic.
min_papers = min(papers_per_batch)
if n_subs > Q * min_papers:
    raise SystemExit(
        f"HARD STOP (EC-11 scoped): {n_subs} in-scope subtopics > {Q * min_papers} slots "
        f"in the smallest batch ({min_papers} paper(s) x {Q} Q/paper). Cannot guarantee "
        f"every subtopic appears once per batch.\n"
        f"  Options: (a) increase --qs_per_paper; (b) increase --batch_size so no partial "
        f"batch is this small (or make --count a multiple of --batch_size); "
        f"(c) narrow the scope (fewer subtopics).\n"
        f"  Choose one and re-trigger.")
```

### S4-2 — Per-batch allocation

```python
# For each batch: reserve the coverage floor (1 appearance per subtopic), split the rest
# among PYQ subtopics by r_avg, then place per-paper via exact_fill. Zero-PYQ subtopics
# get exactly the floor (guaranteed practice — the 'no surprises' rule); PYQ subtopics get
# floor + r_avg-weighted extra. Structure mirrors the mock §4-2 with Zero-PYQ subtopics
# playing the reserved-floor role that mandates play in the mock.
FLOOR = 1                                   # per-batch coverage floor (each subtopic ≥1)
pyq_subs = [S for S in in_scope_ids if r_avg[S] > 0]
zp_subs  = [S for S in in_scope_ids if r_avg[S] == 0]

paper_alloc = {}          # global paper index k (1..N) -> {subtopic_id: q_count}
k = 0                     # running global paper counter
for b, P_b in enumerate(papers_per_batch):
    batch_target = Q * P_b                  # total slots in this batch

    # ── batch quota per subtopic ────────────────────────────────────────────
    bq, raw_total = {}, {}
    for S in zp_subs:                       # Zero-PYQ: exactly the coverage floor
        bq[S] = FLOOR
        raw_total[S] = float(FLOOR)         # 0 fractional remainder → deficit prefers PYQ
    zp_reserved = sum(bq[S] for S in zp_subs)
    remaining = batch_target - zp_reserved
    if remaining < 0:
        # More Zero-PYQ subtopics than batch slots — same family as EC-11.
        raise SystemExit(
            f"HARD STOP: batch {b + 1} Zero-PYQ floor ({zp_reserved}) exceeds batch slots "
            f"({batch_target}). Increase --qs_per_paper/--batch_size or narrow scope.")
    if pyq_subs:                            # PYQ: r_avg-weighted split of the remainder
        _pool_q, _pool_r = bc.proportional_split(pyq_subs, r_avg, remaining, P_b, FLOOR)
        bq.update(_pool_q)
        raw_total.update(_pool_r)
    # (all-Zero-PYQ scope: no PYQ pool; the deficit fix below spreads `remaining`
    #  evenly across the Zero-PYQ subtopics — all equal raw_total.)

    floors = {S: FLOOR for S in in_scope_ids}
    try:
        bc.largest_remainder_fix(bq, in_scope_ids, raw_total, r_avg,
                                 batch_target, FLOOR, floors=floors)
    except bc.AllocationError as e:
        raise SystemExit(f"HARD STOP (scoped allocation, batch {b + 1}): {e}")
    # INVARIANT: sum(bq) == batch_target; every bq[S] >= 1 (coverage floor).

    # ── per-paper placement within the batch (engine exact_fill) ────────────
    # rows = subtopics (row sum = bq[S]); columns = the P_b papers (col sum = Q each).
    col_targets = [Q] * P_b
    grid = bc.exact_fill(bq, col_targets)   # {S: [count per paper-in-batch]}

    for j in range(P_b):
        k += 1
        paper_alloc[k] = {S: grid[S][j] for S in in_scope_ids if grid[S][j] > 0}
```

### S4-3 — Allocation invariants (assert before proceeding)

```python
# (A) every paper has exactly Q questions
for kk, alloc in paper_alloc.items():
    assert sum(alloc.values()) == Q, f"paper {kk}: {sum(alloc.values())} != Q={Q}"

# (B) batch coverage: every in-scope subtopic appears >=1 in every batch
k = 0
for b, P_b in enumerate(papers_per_batch):
    batch_papers = list(range(k + 1, k + P_b + 1)); k += P_b
    for S in in_scope_ids:
        appearances = sum(paper_alloc[p].get(S, 0) for p in batch_papers)
        assert appearances >= 1, (
            f"COVERAGE FAIL: subtopic '{S}' has {appearances} appearances in batch {b + 1}")

# (C) series totals are frequency-ordered among PYQ subtopics (sanity, not exact):
#     higher r_avg => >= questions in aggregate is NOT asserted per-pair (largest-remainder
#     + per-batch flooring can invert close ties); the per-batch r_avg split is the
#     authoritative fidelity mechanism, audited downstream at Step 8.

# series_total[S] = total questions for subtopic S across all N papers (for §8 blueprint.json)
series_total = {S: sum(paper_alloc[p].get(S, 0) for p in paper_alloc) for S in in_scope_ids}
assert sum(series_total.values()) == Q * N
```

### S4-4 — Subtopic-level scope (degenerate single-subtopic case)

```
When --level subtopic (n_subs == 1): the single subtopic carries the whole paper. S4-2
reduces cleanly — FLOOR reserves 1, the one PYQ (or Zero-PYQ) subtopic absorbs the rest,
exact_fill puts Q in every paper. No special-casing needed; the general path handles it.
(A subtopic test on a Zero-PYQ subtopic is allowed — the deficit fix gives it the full
batch_target; it is practised exactly like any other, from domain knowledge at generation.)
```

## §5 — DIFFICULTY (batch-local, envelope-bounded ramp)

Each batch runs its OWN fresh easy→hard ramp (paper 1 easiest → paper P_b hardest;
saw-tooth across batches is accepted per the locked decision). The ramp is ENVELOPE-
BOUNDED: it only schedules difficulty levels the scope actually exhibits in PYQ, so a
scoped test never drills a difficulty the exam does not use for that scope (which would
be a false-readiness signal). Per-question difficulty is assigned at GENERATION (Step-7
analog) within each subtopic's calibration; §5 sets the per-paper COUNTS as the target
(SCHEDULE-FIRST, exactly like the mock), audited within tolerance downstream.

### S5-1 — Per-subtopic observed difficulty envelope

```python
import blueprint_core as bc
# SECTION_RULES_DIFF (loaded in §1-3 via bc.parse_section_rules_difficulty) is
# {subtopic_id: {level: is_inferred_bool}} for Simple/Medium/Hard.
# is_inferred == False ⇒ that level was OBSERVED in this subtopic's PYQ (its real band).
# is_inferred == True  ⇒ inferred (no PYQ at that level). A Zero-PYQ subtopic (or one absent
#                        from section_rules) has all three inferred → empty observed set →
#                        the inheritance cascade (S5-2) supplies the band.
LEVELS = ['Simple', 'Medium', 'Hard']   # analysis vocabulary; canonical alias Easy/Medium/Hard

def observed_levels(sid):
    calib = SECTION_RULES_DIFF.get(sid, {})              # {level: is_inferred}; {} if absent
    return {lv for lv in LEVELS if calib.get(lv, True) is False}
```

### S5-2 — Scope envelope with inheritance cascade (subtopic → topic → subject → default)

```python
# Envelope = union of observed levels over the in-scope subtopics. If EMPTY (e.g. every
# in-scope subtopic is Zero-PYQ), inherit the union from the parent TOPIC, then SUBJECT,
# then fall back to the full default range. Aggregation is over the WHOLE manifest, not
# just the in-scope set, so a Zero-PYQ subtopic borrows its neighbours' real band.
def _union_levels(ids):
    env = set()
    for sid in ids:
        env |= observed_levels(sid)
    return env

def scope_envelope():
    env = _union_levels(in_scope_ids)
    if env:
        return env
    # all-inferred → cascade. scope_subject / scope_topic from §2 S2-1.
    if scope_topic is not None:
        topic_ids = [sid for sid, v in MANIFEST_IDS.items()
                     if v.get('section') == scope_subject and v.get('topic') == scope_topic]
        env = _union_levels(topic_ids)
        if env:
            return env
    if scope_subject is not None:
        subj_ids = [sid for sid, v in MANIFEST_IDS.items() if v.get('section') == scope_subject]
        env = _union_levels(subj_ids)
        if env:
            return env
    return set(LEVELS)   # default: full Easy/Medium/Hard range

ENVELOPE = scope_envelope()
```

### S5-3 — Batch-local ramp → per-paper difficulty counts

```python
# Default ramp anchors (paper at the easy end vs the hard end of a batch). Overridable;
# these are Simple:Medium:Hard percentages BEFORE envelope masking.
RAMP_EASY_ANCHOR = (50, 30, 20)
RAMP_HARD_ANCHOR = (20, 30, 50)

def paper_emh(t):
    """t in [0,1] (0 = easy end of the batch, 1 = hard end). Linearly interpolate the
    anchors, MASK to the scope envelope (levels not exhibited get 0%), renormalise to 100.
    bc.difficulty_counts then rounds to integer counts summing exactly to Q."""
    interp = [RAMP_EASY_ANCHOR[i] + t * (RAMP_HARD_ANCHOR[i] - RAMP_EASY_ANCHOR[i])
              for i in range(3)]
    masked = [interp[i] if LEVELS[i] in ENVELOPE else 0.0 for i in range(3)]
    s = sum(masked) or 1.0
    pct = [100.0 * m / s for m in masked]
    return pct[0], pct[1], pct[2]

# difficulty_schedule[k] = (simple, medium, hard) integer counts for global paper k.
# Ramp position resets each batch (BATCH-LOCAL): paper j of a P_b-paper batch → t=j/(P_b-1)
# (single-paper batch → t=0.5, the batch midpoint).
difficulty_schedule = {}
k = 0
for b, P_b in enumerate(papers_per_batch):
    for j in range(P_b):
        k += 1
        t = 0.5 if P_b == 1 else j / (P_b - 1)
        s_pct, m_pct, h_pct = paper_emh(t)
        difficulty_schedule[k] = bc.difficulty_counts(Q, s_pct, m_pct, h_pct)
        # (canonical labels: simple→Easy, medium→Medium, hard→Hard — same alias as the mock.)

# INVARIANTS (assert): every paper's counts sum to Q; no paper schedules a level outside
# the envelope; within a batch the Hard count is non-decreasing when Hard ∈ ENVELOPE.
for kk, (s_, m_, h_) in difficulty_schedule.items():
    assert s_ + m_ + h_ == Q
    if 'Simple' not in ENVELOPE: assert s_ == 0
    if 'Medium' not in ENVELOPE: assert m_ == 0
    if 'Hard'   not in ENVELOPE: assert h_ == 0
```

### S5-4 — Degenerate envelopes

```
Single-level envelope (e.g. an inherently-Hard subtopic, ENVELOPE={'Hard'}): every paper
is 100% that level — no ramp is possible or desirable (drilling another difficulty would
be a false signal). Two-level envelopes (e.g. {'Simple','Hard'} with no observed Medium)
ramp between the two present levels, skipping the absent one. The masking in paper_emh
handles all subsets uniformly.
```

## §6 — FORMAT (per-scope three-axis signature)

Build a per-SCOPE three-axis format distribution and turn it into an axis_schedule via the
shared engine (bc.derive_axis_schedule — the SAME function the mock uses). The distribution
respects what data Step 5 actually publishes:

  • Per-SECTION (subject) full 3-axis distribution is precomputed in
    manifest['axis_distribution'][subject] (axis1/axis2/axis3/negative_rate over recent
    years). Per-SUBTOPIC, Step 5 publishes ONLY observed_axis2 (axis-2 counts) — not
    per-subtopic axis-1/axis-3/negative_rate.

  So the design is HYBRID, using the finest granularity available per axis:
  • SUBJECT scope   → use the precomputed subject distribution verbatim (most accurate).
  • TOPIC/SUBTOPIC  → RE-SCOPE axis-2 from the in-scope subtopics' observed_axis2; INHERIT
                       axis-1/axis-3/negative_rate from the parent subject (best available;
                       documented limitation — a future Step-5 enhancement could publish
                       per-subtopic axis-1/axis-3 for finer topic/subtopic fidelity).
  • Zero-PYQ scope  → axis-2 cascade topic→subject→default (DIRECT residual), like §5/§6.

All three axes are re-normalised to the scoped paper size Q (the precomputed distribution
is in REAL-exam-paper terms, whose per-paper question count generally differs from Q).

### S6-1 — Scope axis-2 counts (per-subtopic granularity, with cascade)

```python
import blueprint_core as bc
from collections import Counter

def _agg_observed_axis2(ids):
    c = Counter()
    for sid in ids:
        c.update(OBSERVED_AXIS2_BY_ID.get(sid, {}))
    return dict(c)

def scope_axis2_counts():
    """Aggregate observed_axis2 over the in-scope subtopics; if empty (all Zero-PYQ),
    cascade to the parent TOPIC, then SUBJECT, then default (no axis-2 targets)."""
    c = _agg_observed_axis2(in_scope_ids)
    if c:
        return c
    if scope_topic is not None:
        tids = [s for s, v in MANIFEST_IDS.items()
                if v.get('section') == scope_subject and v.get('topic') == scope_topic]
        c = _agg_observed_axis2(tids)
        if c:
            return c
    if scope_subject is not None:
        sids = [s for s, v in MANIFEST_IDS.items() if v.get('section') == scope_subject]
        c = _agg_observed_axis2(sids)
        if c:
            return c
    return {}      # default: no axis-2 targets → DIRECT residual fills the paper
```

### S6-2 — Scope axis distribution (hybrid base + Q-normalisation of ALL three axes)

```python
AXIS_DIST_BY_SECTION = manifest.get('axis_distribution', {})
subject_base = AXIS_DIST_BY_SECTION.get(scope_subject)   # None if the subject is all-Zero-PYQ

def _norm_to_Q(dist):
    """Preserve class PROPORTIONS but scale to the scoped paper size Q. CRITICAL for all
    three axes: the precomputed distribution is in REAL-per-paper terms (which sum to the
    real section's per-paper question count, generally != Q). bc.derive_axis_schedule
    apportions axis-1/axis-3 to sec_qs=Q internally via a largest-remainder step whose
    safety guard ASSUMES inputs already sum to ~target; feeding it real-per-paper values
    (sum >> Q) would trip that guard and truncate the result. Normalising to Q first keeps
    the apportionment deficit ~0 and the result exact."""
    tot = sum(dist.values())
    return {k: (v / tot) * Q for k, v in dist.items()} if tot > 0 else {}

def _finalize(base_axis1, axis2_source, base_axis3, base_neg, base_years):
    a1 = _norm_to_Q(base_axis1)
    a2 = _norm_to_Q(axis2_source)
    a3 = _norm_to_Q(base_axis3)
    if not (a1 or a2 or a3):
        return None                                  # nothing observed anywhere → no_pyq
    return {'axis1_per_paper': a1, 'axis2_per_paper': a2, 'axis3_per_paper': a3,
            'negative_rate': base_neg, 'recent_years': base_years}

if level == 'subject':
    # Subject scope: precomputed subject distribution, all three axes renormalised to Q.
    scope_axis_dist = (None if subject_base is None else _finalize(
        subject_base.get('axis1_per_paper', {}), subject_base.get('axis2_per_paper', {}),
        subject_base.get('axis3_per_paper', {}), subject_base.get('negative_rate', 0.0),
        subject_base.get('recent_years', [])))
else:
    # Topic/Subtopic scope: axis-2 rescoped to the in-scope subtopics (with cascade);
    # axis-1/axis-3/negative_rate/recent_years inherited from the subject.
    a2_counts = scope_axis2_counts()
    if subject_base is None:
        scope_axis_dist = _finalize({}, a2_counts, {}, 0.0, [])
    else:
        scope_axis_dist = _finalize(
            subject_base.get('axis1_per_paper', {}), a2_counts,
            subject_base.get('axis3_per_paper', {}), subject_base.get('negative_rate', 0.0),
            subject_base.get('recent_years', []))
```

### S6-3 — Derive the axis_schedule (engine)

```python
# PYQ vs Zero-PYQ in-scope ids (r_avg keyed by subtopic_id, §3).
pyq_ids = [sid for sid in in_scope_ids if r_avg[sid] > 0]
zp_ids  = [sid for sid in in_scope_ids if r_avg[sid] == 0]

# The engine's Axis-2 pool-caps and Axis-1 feasibility filter ids by
# manifest[sid]['section'] == section_name. The scoped section is the scope, so relabel the
# in-scope ids' section to scope_label in a LOCAL view (never mutate the real manifest), and
# pass section_name = scope_label so the filter matches every in-scope id (and only those).
scoped_manifest_ids = {sid: {**MANIFEST_IDS[sid], 'section': scope_label} for sid in in_scope_ids}

axis_schedule = bc.derive_axis_schedule(
    scope_label, scope_axis_dist, Q, pyq_ids, zp_ids,
    AXIS2_CAP_BY_ID, scoped_manifest_ids, papers_per_window=batch_size)
#   → status 'no_pyq' when scope_axis_dist is None; otherwise band/guarantee/float modes,
#     window targets, guarantee feasibility (pyq_covered / zp_only / unsatisfiable), and
#     axis1/axis3 targets apportioned to Q. DIRECT is always the residual float.

# Axis-1 advisory (WARN, never HALT): stimulus formats targeted but not present in-scope.
# Add it to the schedule as the 15th key (mock schema S14-3b parity — Step-8 reads it), then
# flag any shortfall for the run report.
unreachable = bc.axis1_feasibility(
    scope_label, axis_schedule.get('axis1_target_per_mock', {}), pyq_ids, scoped_manifest_ids)
axis_schedule['axis1_unreachable_formats'] = unreachable
if unreachable:
    flag(f"Axis-1 formats targeted but absent among in-scope PYQ subtopics: {unreachable} "
         f"(shortfall reported, not forced — subtopic is hard #1).")
```

### S6-4 — Partial-batch caveat + fabrication ban

```
PARTIAL LAST BATCH: papers_per_window = batch_size, but the last batch may be smaller. A
band/guarantee target derived for a FULL window is therefore a tolerance target, not a hard
guarantee, in a short last batch — audited within tolerance downstream (Step-8 analog), never
force-filled.

NEVER FABRICATE: a guarantee-mode class marked 'unsatisfiable' (no in-scope PYQ or Zero-PYQ
subtopic can carry it) is accepted as a shortfall. Generation (Step-7 analog) renders formats
ONLY within each subtopic's axis2_capability — an incapable subtopic is never forced into a
format it cannot faithfully produce.
```

## §7 — MARKING / SECTIONING

A scoped paper is a SINGLE range [1, Q] (one synthetic section, §2, ordered topic→subtopic).
Its marking is inherited from exam_config.marking_scheme[] (per-range
{q_range, question_type, correct_marks, negative_marks}). SUBJECT≠SECTION means a subtopic's
subject does not map 1:1 to an OTS marking range, so the scope's marking is resolved by tier:

  • Single tier (one entry, or all entries share the same marks/type) → use it. (Common case.)
  • Multiple tiers (e.g. a subject spanning 2-mark and 4-mark ranges) → the MODAL tier,
    weighted by how many real questions each tier covers (q_range span), with a flag.
  • Zero-PYQ subtopics inherit the same scope marking (no separate tier).

```python
from collections import Counter

ms = exam_config.get('marking_scheme', [])
if not ms:
    scoped_marking = [{'q_range': [1, Q], 'question_type': 'MCQ',
                       'correct_marks': 1, 'negative_marks': 0}]
    flag("exam_config has no marking_scheme; defaulting to +1 / 0. Verify against the exam.")
else:
    tier_span = Counter()
    for entry in ms:
        rng = entry.get('q_range', [1, 1])
        span = max(1, rng[1] - rng[0] + 1)
        key = (entry.get('correct_marks'), entry.get('negative_marks'),
               entry.get('question_type', 'MCQ'))
        tier_span[key] += span
    (cm, nm, qt), _ = tier_span.most_common(1)[0]        # dominant tier by real-question span
    scoped_marking = [{'q_range': [1, Q], 'question_type': qt,
                       'correct_marks': cm, 'negative_marks': nm}]
    if len(tier_span) > 1:
        flag(f"Exam has {len(tier_span)} marking tiers; this scoped test uses the MODAL tier "
             f"(correct={cm}, negative={nm}, type={qt}). For a subject spanning mark tiers, "
             f"verify this is the intended marking.")
```

## §8 — EMIT (blueprint.json + blueprint.xlsx)

Assemble the SAME blueprint.json schema Steps 7–11 read (the mock Blueprint schema section), specialised to a single
synthetic section and N papers. Every top-level field is inherited from exam_config (never
hardcoded); the allocation blocks come from §3–§7. Plus a `scope{}` block and a per-paper
`paper_id` so the shared generator and registry can tell scoped papers apart.

```python
import json
SCOPED_VERSION = '1.0'   # this SPEC's version (scoped_spec_version below) — NOT blueprint_version.
# blueprint_version is the SHARED blueprint.json SCHEMA version that Steps 7-11 gate on
# (Step 7: MIN_BLUEPRINT_VERSION = (1,7), the subtopic_id contract floor). The scoped blueprint
# emits the SAME blueprint.json schema as the mock (which emits "1.23"), so it MUST emit the same schema
# version — emitting SCOPED_VERSION ('1.0') here would fail Step 7's (1,7) floor and hard-stop
# every scoped generation. Keep this in sync with the mock Blueprint's emitted blueprint_version.
BLUEPRINT_SCHEMA_VERSION = '1.23'

# S8-1 — subtopic_list[] (top-level; r_avg stored ONCE per subtopic, per the mock schema S14-8).
subtopic_list = [{
    'subtopic_id': sid,
    'topic': MANIFEST_IDS[sid].get('topic'),
    'subtopic': MANIFEST_IDS[sid]['display_name'],
    'section': scope_label,
    'r_avg': r_avg[sid],
    'type': 'pyq_based' if r_avg[sid] > 0 else 'zero_pyq',
    'answer_type': ANSWER_TYPE.get(sid, 'option'),            # Step 11 tagging (mock parity)
    'answer_cardinality': ANSWER_CARD.get(sid, 'single'),     # NAT/MSQ fidelity for scoped
} for sid in in_scope_ids]

# S8-2 — difficulty_schedule[] (one entry per PAPER; §5). Length == N; each sums to Q.
difficulty_sched_json = [
    {'mock': k, 'band': 'ScopedRamp', 'simple': s, 'medium': m, 'hard': h}
    for k, (s, m, h) in sorted(difficulty_schedule.items())
]

# S8-3 — mocks[] (one per paper; §4 paper_alloc → subtopic_allocations, only q_count>0 stored).
# paper_alloc is keyed by subtopic_id (§4). paper_id numbering RESUMES from paper_start
# (§2 S2-4: count of existing papers for this scope in the shared registry; 0 for a fresh
# series). Append-only across sessions.
mocks_json = []
for k in range(1, N + 1):
    allocs = []
    for sid, qc in sorted(paper_alloc[k].items()):
        e = MANIFEST_IDS[sid]
        allocs.append({
            'subtopic_id': sid, 'topic': e.get('topic'), 'subtopic': e['display_name'],
            'q_count': qc, 'format': e.get('format', 'TEXT'),
            'type': 'pyq_based' if r_avg[sid] > 0 else 'zero_pyq',
        })
    ssum = sum(a['q_count'] for a in allocs)
    mocks_json.append({
        'mock': k,                                   # kept for Steps 7–11 backward-compat
        'paper_id': f"{PAPER_PREFIX}:{paper_start + k:02d}",   # scoped identity (registry join)
        'sections': [{
            'section_name': scope_label, 'q_range': [1, Q], 'total_qs': Q,
            'subtopic_allocations': allocs,
            'validation': {'sum': ssum, 'expected': Q,
                           'status': 'pass' if ssum == Q else 'FAIL'},
        }],
    })

# S8-4 — assemble the full blueprint (top-level inherited from exam_config).
_default_nat = {'nat_answer_type': 'real', 'nat_tolerance': '0',
                'nat_instruction': 'Enter your answer as a numerical value.'}
_default_msq = {'msq_k_mode': 'n/a', 'msq_k': 'none',
                'msq_instruction': '(One or more options may be correct)',
                'negative_marking_by_type': {}, 'partial_credit': False}

blueprint = {
    'exam_code': EXAM,
    'exam_name': exam_config.get('exam_name', EXAM),
    'blueprint_version': BLUEPRINT_SCHEMA_VERSION,   # shared schema version (mock S14-x; ≥ Step-7 floor 1.7)
    'scope': {'level': level, 'subject': scope_subject, 'topic': scope_topic,
              'scope_label': scope_label, 'scopetag': SCOPETAG, 'paper_prefix': PAPER_PREFIX,
              'scoped_spec_version': SCOPED_VERSION},   # THIS spec's version (not the schema version)
    'n_papers': 1,
    'total_mocks': N,                 # papers in this scoped series
    'total_questions': Q,
    # batch_size_qs is the axis-2 WINDOW size Steps 7/8 read (bp.get('batch_size_qs', 10)); §6
    # built axis_schedule for a window of batch_size papers, so it MUST be emitted here or a
    # non-default --batch_size would silently fall back to 10 and mis-audit the axis-2 window.
    'batch_size_qs': batch_size,
    'total_options': exam_config.get('total_options', 4),
    'option_label': exam_config.get('option_label', '1/2/3/4'),
    'level': exam_config.get('level', ''),
    'medium': exam_config.get('medium', 'English'),
    'marking_scheme': scoped_marking,             # §7
    'passage_present': exam_config.get('passage_present', False),
    'figural_present': exam_config.get('figural_present', False),
    'di_present': exam_config.get('di_present', False),
    'multi_present': exam_config.get('multi_present', False),
    'multi_select_allowed': exam_config.get('multi_select_allowed', False),
    'nat_present': exam_config.get('nat_present', False),
    'nat_allowed': exam_config.get('nat_allowed', False),
    'nat_contract': exam_config.get('nat_contract', _default_nat),
    'q_types': exam_config.get('q_types', "['MCQ']"),
    'msq_contract': exam_config.get('msq_contract', _default_msq),
    'difficulty_labels': exam_config.get('difficulty_labels', ['Easy', 'Medium', 'Hard']),
    'sections': sections,                          # single synthetic section (§2)
    'subtopic_list': subtopic_list,
    'difficulty_schedule': difficulty_sched_json,
    'axis_schedule': {scope_label: axis_schedule},  # §6, keyed by the single section name
    # Zero-PYQ subtopics are covered by the §4 coverage floor (allocated every batch), NOT by
    # the mock's capped rotation — so the rotation list is empty. The KEY is still emitted for
    # every section, per the mock schema S14-4 (a missing section key is blueprint corruption downstream).
    'zero_pyq_rotation': {scope_label: []},
    'mocks': mocks_json,
}

# S8-5 — emit output artifacts.
out_json = f'/mnt/user-data/outputs/{EXAM}_{SCOPETAG}_blueprint.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)
# blueprint.xlsx: a human-review sheet (subtopic × paper q_count grid + difficulty/axis
# summaries), same spirit as the mock's blueprint.xlsx. (Rendering reuses the mock's helper.)
```

### S8-6 — Emit invariants (assert before delivery)

```python
REQUIRED_TOP = ['exam_code', 'exam_name', 'blueprint_version', 'n_papers', 'total_mocks',
                'total_questions', 'total_options', 'option_label', 'level', 'medium',
                'marking_scheme', 'passage_present', 'figural_present', 'di_present',
                'multi_present', 'multi_select_allowed', 'nat_present', 'nat_allowed',
                'nat_contract', 'q_types', 'msq_contract', 'difficulty_labels', 'sections',
                'subtopic_list', 'difficulty_schedule', 'axis_schedule', 'zero_pyq_rotation',
                'mocks']
missing = [k for k in REQUIRED_TOP if k not in blueprint]
assert not missing, f"blueprint.json missing required fields: {missing}"
assert len(blueprint['sections']) == 1
assert len(blueprint['difficulty_schedule']) == N
assert all(e['simple'] + e['medium'] + e['hard'] == Q for e in blueprint['difficulty_schedule'])
assert len(blueprint['mocks']) == N
for m in blueprint['mocks']:
    sec = m['sections'][0]
    assert sec['validation']['status'] == 'pass'
    assert sum(a['q_count'] for a in sec['subtopic_allocations']) == Q
    # every allocation id is a real manifest id (never minted) — RULE 2a parity
    assert all(a['subtopic_id'] in MANIFEST_IDS for a in sec['subtopic_allocations'])
# axis_schedule + zero_pyq_rotation keyed by the single section name
assert set(blueprint['axis_schedule']) == {scope_label}
assert set(blueprint['zero_pyq_rotation']) == {scope_label}
```

### S8-7 — Seed the shared registry template (fresh exam only)

```python
# If §1-4 found no registry (_new_registry True), seed the template the generator will fill.
# An EXISTING registry is NEVER overwritten here — the generator only APPENDS (RS-9 parity:
# the blueprint fixes the schema; generation only adds entries).
if _new_registry:
    seed = {'exam_code': EXAM, 'schema_version': SCOPED_SCHEMA,
            'papers_completed': [], 'question_hashes': [], 'stem_texts': [],
            'semantic_tuples': [], 'semantic_usage': [], 'exhausted_subtopics': {},
            'question_index': [], 'image_phashes': [],
            'image_sources_used': [], 'session_log': [], 'content_tracking': {}}
    json.dump(seed, open(f'/mnt/user-data/outputs/{EXAM}_registry.json', 'w',
                         encoding='utf-8'), ensure_ascii=False, indent=2)
    flag(f"Seeded a fresh shared registry for {EXAM} (schema {SCOPED_SCHEMA}). The generator "
         f"(Step-7 analog) fills it; every tier shares it.")
```

## §9 — RESUMPTION (semantics + generation-layer registry contract)

The registry is SHARED per exam: mocks and every scoped tier read/write the SAME
[ExamCode]_registry.json. That single ledger is what makes uniqueness strict-global — a new
paper dedups against EVERY prior paper of EVERY tier. Resumption is append-only and
TIER-AGNOSTIC: add mocks, subject, topic, or sub-topic papers in any order, any time; there
is no precedence (a later paper simply dedups against everything already recorded).

The MECHANICS run at session start (they are preconditions for the paper_id numbering):
  • §1-4 — load the shared registry; exam_code gate; auto-migrate an old mock-only registry
    to the generalised paper_id schema (snapshot → migrate → verify → idempotent); taxonomy-
    drift and completeness HARD-STOP gates.
  • §2-4 — per-scope paper_id resume offset (paper_start), independent per scope.
  • §8-7 — seed a fresh registry template when none exists (never overwrite an existing one).

### S9-1 — Registry contract for the generation layer (Step-7 analog — parts B/D)

```
The blueprint fixes the shared-registry SCHEMA; generation must honour this contract so
strict-global uniqueness holds across all tiers:

  paper_id tagging   Every appended entry (papers_completed, question_index, session_log)
                     is tagged with paper_id (SUBJ:/TOPIC:/SUBTOPIC:/MOCK:), NOT a bare mock
                     number. question_index entry = {paper_id, questions:[{q, subtopic_id,
                     difficulty}, ...]}.
  strict-global      A new question dedups (question_hashes, semantic_tuples, content_tracking)
                     against ALL prior entries regardless of tier — one shared ledger.
  shard by subtopic  For scale (potentially 100k+ questions/exam) AND correctness, the dedup
                     index is PARTITIONED by subtopic_id: a new Kinematics question is compared
                     only against prior Kinematics entries. Same-margin, cheaper, and matches
                     the natural scope structure.
  content unit       Uniqueness is enforced on (item × angle): the same underlying fact tested
                     through a different angle/presentation is a distinct question.
  exhaustion         For a genuinely narrow FACTUAL subtopic that drains its (item × angle)
                     universe, a fact may be reused — NEVER verbatim, a NEW angle each time,
                     and not within a cumulative cross-tier spacing gap of 8 papers. The
                     per-subtopic exhaustion flag is sticky across ALL tiers including mocks.
                     Never fabricate (the C-FACTUAL gate web-verifies every fact).
  retirement         A deleted paper's items stay retired unless an explicit release op runs
                     (no silent reuse).
```

## §10 — DEFINITION OF DONE (verify before delivering the scoped blueprint)

```
  ☐ 1.  ENGINE MANDATE (S1-2b): blueprint_core.py present, copied to /home/claude, and
         `--self-test` printed "SELF-TEST: N/N PASS" before any allocation ran.
  ☐ 2.  INPUTS loaded (§1-3): exam_config.json, [ExamCode]_subtopic_manifest.json,
         [ExamCode]_section_rules.md — each present or a HARD STOP was raised naming it.
  ☐ 3.  SCOPE resolved (§2): --level/--scope produced ≥1 in-scope subtopic_id; an empty or
         ambiguous scope HARD-STOPPED. All keying is by subtopic_id (never display name).
  ☐ 4.  FREQUENCY (§3): r_avg computed per subtopic_id via bc.compute_r_avg (Excel keyed by
         the taxonomy triple, so duplicate display names stay distinct).
  ☐ 5.  ALLOCATION (§4): EC-11 feasibility passed; every paper has exactly Q questions; every
         in-scope subtopic (PYQ and Zero-PYQ) appears ≥1 in every batch (coverage floor);
         series total == Q×N.
  ☐ 6.  DIFFICULTY (§5): each paper's simple+medium+hard == Q; no level scheduled outside the
         scope envelope; batch-local ramp (Hard non-decreasing within a batch when in-envelope).
  ☐ 7.  FORMAT (§6): axis_schedule built via bc.derive_axis_schedule (subject verbatim;
         topic/subtopic axis-2 rescoped, axis-1/3 inherited; all axes normalised to Q);
         axis1_unreachable_formats present; no fabrication of unsatisfiable formats.
  ☐ 8.  MARKING (§7): single-tier used, or modal-by-span for a multi-tier subject (flagged).
  ☐ 9.  REGISTRY (§1-4/§2-4/§8-7): exam_code gate passed; old registry auto-migrated
         (snapshot retained); taxonomy-drift and completeness gates passed; paper_id numbering
         resumed from paper_start; a fresh registry was seeded only when none existed.
  ☐ 10. EMIT (§8): blueprint.json carries ALL required top-level fields (§8-6 assertion);
         single synthetic section; total_mocks==N; total_questions==Q; every allocation
         subtopic_id is a real manifest id (never minted); each paper's validation.status=='pass'.
  ☐ 11. EXAM-AGNOSTIC: zero hardcoded exam values — scope/counts/Q from the trigger; subtopics,
         r_avg, difficulty, format, marking from the Step-5 outputs + exam_config.
```

# END OF Framework_ScopedBlueprint v1.5 (§1–§10, adversarially verified; qualified subtopic scope)
