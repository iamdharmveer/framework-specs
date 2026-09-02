# Framework_PYQDraft v1.3.0 — PYQ Step 2a — Taxonomy Building from Syllabus (§2)
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

## §2 — PHASE 0a: TAXONOMY BUILDING FROM SYLLABUS

### S2-0 — INTAKE RULE (v1.1.0, D1 — runs BEFORE S2-1, every PYQDraft session)

```
Before S2-1, check project Files for [ExamCode]_approval_record.json.

(a) Status HELD → read record['re_derive_directive'] and treat the rejected
    fingerprint's shape and EACH constraint as HARD constraints on derivation:
    every topic in directive['crowded_topics'] MUST be split (the items ARE
    the Topics — EC-P20), and the re-derived taxonomy MUST NOT reproduce
    rejected_fingerprint. This consumption is what makes the Approve→Draft
    loop CONVERGENT across fresh sessions — without it a memoryless re-run
    can plausibly reproduce the rejected shape (the RPSC_ZOOLOGY hazard).
    Print, before deriving: "Consuming re-derive directive from
    [ExamCode]_approval_record.json — [N] constraint(s), [M] crowded topic(s)."

(b) Status CLEAN or CLEAN_ADJUDICATED → the taxonomy is LOCKED. PYQDraft MUST
    warn and require EXPLICIT operator confirmation before proceeding, because
    re-deriving a locked taxonomy can silently diverge it from every
    downstream artifact built on it — the exact danger the PYQApprove R1
    scoping rule names. This is a CONTRACT-PROTECTION confirmation (Type-2
    class), not a defect halt. Message (one action):
      "This exam's taxonomy is already LOCKED ([status], [date if present]).
       Re-running PYQDraft re-derives it and can diverge every artifact built
       on it. Reply CONFIRM RE-DERIVE to proceed, or run the next step
       instead."
    On confirmation, proceed; the eventual PYQApprove replays per INV-6/mode C.

(c) No record → proceed normally.

ALSO: if a prior [ExamCode]_taxonomy_draft.json in project Files carries a
non-empty amber_status, its unresolved list is a CONSTRAINT SET for this run —
each residue must be either resolved or consciously re-declared, never
silently dropped.
```

### S2-0a — SYLLABUS-TRANSITION RESOLUTION (v1.2.0 — GAP-2026-09-01 §3; runs
###          WITH the S1-2 file inventory, BEFORE S2-1 syllabus extraction)

```
WHY THIS SECTION EXISTS. The corpus had no concept of a syllabus VERSION:
S2-1 read ONE syllabus document and nothing recorded which, retained a
previous version, or could diff two. This section gives the operator a
DECLARATION channel and gives the framework the census that decides WHICH
file is the syllabus. It changes NO allocation. An exam whose Overview tab
never carries the keys AND holds at most one syllabus-named file behaves
byte-identically to the pre-v1.2.0 corpus (proof P1); the only new behaviour
such a legacy exam can ever see is HS-ST2 when a SECOND syllabus-named file
strays into its project Files (accepted reactive discovery, R26 — the fix is
a 30-second file deletion).

DECLARATION (two OPTIONAL Overview-tab key-value rows; the existing S2-2a
parser `dict(zip(...))` ignores unknown keys, so absence is cost-free):

  Key (exact string after strip)   | Value
  ---------------------------------+-----------------------------------------
  Syllabus Changed                 | "Yes"/"No" — str(v).strip().casefold()
  New Syllabus Effective From      | YYYY-MM — month of the FIRST EXAM
                                   | CONDUCTED under the new syllabus

ACTIVATION (R1, permissive): transition_active <=> SC normalizes to "yes"
AND EF parses to valid YYYY-MM. Every other combination => INACTIVE — the
framework behaves exactly as today. The ONE declaration-VALUE hard stop:
SC = Yes with EF absent/blank/unparseable => HS-ST1 (R2 — a declared change
is never silently discarded). Excel cells that arrive as datetime/date
objects are coerced to YYYY-MM BEFORE validation (R4); an Excel boolean TRUE
in SC is "true" != "yes" => inactive-with-trace, by design. The engine is
the ONLY implementation: bc.resolve_transition (activation + T1 outcome),
bc.coerce_effective_from (EF parse + Excel coercion + sanity range). Key
matching stays exact-string; every warning/stop message and the §3.8
detector list NEAR-MISS keys via bc.near_miss_keys (casefold +
punctuation/whitespace-collapsed — "Syllabus changed?" is reported).
Duplicate occurrence of any Overview key (dict(zip) keeps the LAST) => WARN
"duplicate Overview key '<k>'; last occurrence used" via
bc.overview_duplicate_keys, regardless of activation outcome.

T1 — every declaration combination (SC shown post-normalization):
  # | SC                | EF                        | Outcome
  --+-------------------+---------------------------+------------------------
  1 | absent            | absent                    | INACTIVE, SILENT (the
    |                   |                           | legacy estate; no block,
    |                   |                           | zero output delta; §3.8
    |                   |                           | detector silent per R25)
  2 | "no"              | absent                    | INACTIVE, silent (block
    |                   |                           | written, nothing printed)
  3 | "yes"             | valid YYYY-MM             | ACTIVE -> census rules
  4 | "no"/blank        | valid YYYY-MM             | INACTIVE + TRACE
  5 | other ("y","true",| anything                  | INACTIVE + TRACE
    | "", "maybe"...)   |                           |
  6 | "yes"             | absent/blank/unparseable/ | * HARD STOP HS-ST1 (R2)
    |                   | out-of-sanity-range       |
  7 | absent            | valid YYYY-MM             | INACTIVE + TRACE
  8 | "yes" any case/   | valid                     | ACTIVE (normalization)
    | whitespace        |                           |

CENSUS (corpus_io — runs at S1-2 and cheaply at every step start, §3.7):
  syllabus candidates  = project files whose basename contains "syllabus"
                         (casefold), ext .pdf/.docx/.txt/.png/.jpg/.jpeg
                         (corpus_io.syllabus_file_census)
  sample papers (R14)  = basename contains "samplepaper", same extensions
                         (corpus_io.sample_paper_census); RECORDED only —
                         consumed by Step 5 alone, from Release B/C; absent
                         => silent
R18: English only — no language suffixes; a translated syllabus is simply a
second census hit and stops under T2 row 3.

NAMING (enforced only at >= 2 syllabus files — R1; a single-file project
keeps ANY name, operator ruling):
  [ExamCode]_Syllabus_<YYYY-MM>.<ext>   <YYYY-MM> = first sitting under that
                                        version (bc.parse_syllabus_filename)
The match is CASE-INSENSITIVE end to end (ExamCode, the Syllabus token, the
extension) — the census that nominates the file is already casefold, and a
correctly structured name must never fail on letter case alone (E04/E08
normalization stance). Structure stays strict: prefix, token, dated stamp
and extension must all be present exactly, or HS-ST4; two files carrying
the SAME date in different letter case are still HS-ST5 (ambiguous).

RESOLUTION (ACTIVE): the file whose <YYYY-MM> equals EF is CURRENT; all
others SUPERSEDED. The taxonomy is ALWAYS built from CURRENT; SUPERSEDED
files feed only the Release-B diff. >= 3 dated files (a second historical
change) are legal: exactly one == EF, the rest superseded in date order.
The T2 decision is bc.resolve_syllabus_sources — ONE implementation:

  # | Mode     | Files found              | Outcome
  --+----------+--------------------------+---------------------------------
  1 | INACTIVE | 0                        | As today (S1-2 asks; steps not
    |          |                          | needing it proceed)
  2 | INACTIVE | 1 (any name)             | As today — the estate norm
  3 | INACTIVE | >= 2                     | * HS-ST2 (R3; discovered
    |          |                          | REACTIVELY per R26)
  4 | ACTIVE   | 0 or 1 / chat-only /     | * HS-ST3 (both documents must
    |          | image pasted in chat     | exist as FILES — reproducible)
  5 | ACTIVE   | >= 2, any not dated      | * HS-ST4
  6 | ACTIVE   | >= 2 dated, 0 match EF   | * HS-ST5
  7 | ACTIVE   | >= 2 dated, >= 2 match   | * HS-ST5 (ambiguous CURRENT)
  8 | ACTIVE   | exactly 1 matches EF     | RESOLVED -> hash checks
  9 | ACTIVE   | CURRENT sha256 equals    | * HS-ST6 (same document twice —
    |          | any SUPERSEDED sha256    | the diff would be empty)
 10 | ACTIVE   | resolved, distinct       | PROCEED (materiality decides
    |          | hashes                   | transition vs cosmetic at
    |          |                          | Release B)

HARD STOPS: the exact message templates are the engine's §3.11 register
(bc.HS_ST1 .. bc.HS_ST11 — cited, never restated). PYQDraft raises
SystemExit with the returned message; HS-ST1..HS-ST6 fire HERE. HS-ST7
(staleness) fires at consumers; HS-ST8 (symptom detector, R25-scoped) at
MockBlueprint pre-flight; HS-ST9/HS-ST11 at their Release-B/C call sites.

TRACES (R4, §3.6 — T1 rows 4/5/7 ONLY, and exactly these three surfaces):
  (a) ONE console warning line quoting raw values
      (bc.syllabus_declaration_traces);
  (b) the inactive syllabus_transition block in exam_config (S2-5);
  (c) ONE DeliveryFooter line (bc.syllabus_footer_lines; rendered per
      Framework_DeliveryFooter §FOOTER-SYL).
R19: the footer is the ONLY disclosure surface; nothing on questions,
options, or student-visible layout — ever.

DIAL REGISTRY (R23/R5, §3.9): seven dials, factory values pinned in
bc.TRANSITION_DIALS and ONLY there (ONE-RULEBOOK; §2.1e whitelists exactly
those seven numerals). Optional per-exam Overview override keys:
  D-1 Transition Blend Pseudo-Count      D-5 Transition Coverage Floor
  D-2 Transition Materiality Percent     D-6 Transition Converged Sittings
  D-3 Transition Era Suspect Percent     D-7 Transition Rollup Dominance
  D-4 Transition Detector Floor              Percent
Absent => factory. Present but invalid (non-numeric, out of range) =>
FACTORY + TRACE — never a stop (bc.resolve_dials). Effective values are
recorded in the exam_config block and printed once per run. R21: NO prior
dial and NO prior-override input of any kind exists.

ZERO HISTORY APPROVED (§3.5 A1): a third OPTIONAL Overview key,
`Zero History Approved` — comma-separated subject names matched to taxonomy
subjects casefold (bc.parse_zero_history_approved); unmatched names =>
trace, not stop. This is the operator's answer to HS-ST8 ("add the key,
re-run PYQDraft") and it keeps PYQDraft the SOLE writer of exam_config
(R29): no step ever writes exam_config after 2a.

STALENESS LOCK (§3.10): S2-4 writes syllabus_sha256 — the sha256 of the
taxonomy's SOURCE file (corpus_io.file_sha256 of CURRENT in active mode;
of the single file otherwise; ABSENT for legacy chat-pasted input) — into
taxonomy_draft.json. Consumers (MockBlueprint, MockTestCreate,
ScopedBlueprint, NotesBlueprint) compare it to the resolved current file at
run time via bc.check_syllabus_staleness => mismatch = HS-ST7. Artefacts
WITHOUT the field (legacy) are exempt — no retro-invalidation; the lock
arms on the first PYQDraft re-run under v1.2.0.

DRIFT GUARD (§3.7): every later step that reads exam_config AND project
files re-runs census + bc.resolve_transition on the current xlsx and
compares DECLARATION FIELDS ONLY via bc.transition_drift (R29: legitimate
downstream artefact writes can never register as drift). Divergence (xlsx
edited after 2a — including the R17 EF-postponement path — or syllabus
files added/removed) => HS-ST10 naming both sides and instructing a
PYQDraft re-run. Cost: one sheet read + one glob.

R10 note: a transition never modifies an in-flight mock series; it takes
effect at the next series boundary (new series) — enforced mechanically by
the staleness lock, because the manifest hash changes.
```

```python
# S2-0a EXECUTION (single invocation shape; engines are the implementations)
import datetime
import blueprint_core as bc
import corpus_io as cio


def resolve_syllabus_transition(ov, ov_raw_keys, project_file_paths,
                                exam_code, taxonomy_subjects):
    """Returns (transition_block | None, sources, console_lines).
    ov: the S2-2a Overview dict. ov_raw_keys: first-column values IN ORDER
    (duplicate detection). SOLE WRITER note (R29): the caller places the
    returned block into exam_config['syllabus_transition'] before
    save_exam_config; nothing else ever writes it."""
    console = []
    for k in bc.overview_duplicate_keys(ov_raw_keys):
        console.append(f"WARNING: duplicate Overview key '{k}'; "
                       f"last occurrence used.")
    for miss, canon in bc.near_miss_keys(ov.keys()):
        console.append(f"NOTE: Overview key '{miss}' near-misses '{canon}' "
                       f"and was ignored (key matching is exact).")
    res = bc.resolve_transition(ov, datetime.date.today())   # HS-ST1 inside
    census = cio.census_records(
        cio.syllabus_file_census(project_file_paths))
    cio.sample_paper_census(project_file_paths)              # R14: record only
    sources = bc.resolve_syllabus_sources(
        census, exam_code, res['status'], res.get('effective_from'))
    if sources['outcome'] == 'stop':
        raise SystemExit(sources['message'])                 # HS-ST2..6
    dials, dial_traces = bc.resolve_dials(ov)
    zha, zha_traces = bc.parse_zero_history_approved(ov, taxonomy_subjects)
    block = bc.build_syllabus_transition_block(
        res, sources, dials, dial_traces + zha_traces, zha)
    console += bc.syllabus_declaration_traces(block)         # §3.6(a)
    return block, sources, console
```

### S2-0b — CROSSWALK DRAFT (v1.3.0 — GAP-2026-09-01 §4.1/§4.2; ACTIVE
### mode only — inactive and legacy runs skip this section byte-identically)

After S2-1/S2-2 build the CURRENT taxonomy, and ONLY when the S2-0a block is
ACTIVE, extract the SUPERSEDED syllabus document(s) under the SAME S2-1
extraction rules (one old taxonomy per superseded version — A2), then build
one crosswalk DRAFT per superseded version:

    syllabus_provenance.crosswalk_build(old_tax, new_tax,
        exam_code=..., old_sha256=..., new_sha256=...,
        era_window=..., dials=<S2-0a effective dials>,
        subject_sections=None)   # None = uniform exam (R34: full-set scope)

The draft carries: per-atom node states (RETAINED/MOVED/MERGED/SPLIT/
DELETED — subjects matched by CONTENT similarity, never name, E29/E67;
split-parent subjects score by top-half mean so a unit dividing across two
current homes is never orphaned), NEW atoms, B1 subject-state roll-up
PROPOSALS with atom-fraction evidence (dial D-7, >= at the boundary, E78),
R34 scopes (orphan => empty scope => every atom OOS, E86), R28 materiality
(MOVED/MERGED/SPLIT count zero), and PROVISIONAL per-DELETED-node lexicons
(G-1: finalized only at 2c approval). Low-similarity mappings carry a
'low-similarity: spot-check.' rationale for the 2c human look.

STORAGE (sole writer THIS step, R29; closed deliverable set S10-1
unchanged): the draft list is stored INSIDE exam_config.json at
`syllabus_transition.crosswalks` (one entry per superseded version, each
`approved: False`), and the era-window table at
`syllabus_transition.era_windows` (bc.era_windows). No new files.

### S2-1 — Syllabus extraction

```
Claude reads the Exam Syllabus (any format — image, PDF, .docx, or text).
v1.2.0: in ACTIVE transition mode the document read here is ALWAYS the
S2-0a-resolved CURRENT file — SUPERSEDED files are never extracted at 2a
(they feed only the Release-B diff).
Extract ALL subject/topic items mentioned.

For each subject listed in the syllabus:
  1. Record subject name EXACTLY as syllabus states it
  2. List every individual topic/item mentioned under that subject
  3. Preserve each item as-is — do NOT merge or group items at this stage
     (S2-3's Topic Integrity Test determines final Topic structure)
  4. v2.17 — PRESERVE THE SYLLABUS'S OWN HIERARCHY. If the syllabus places
     items under intermediate headings, RECORD THOSE HEADINGS. Do NOT flatten
     them away.

GRANULARITY — WHAT COUNTS AS ONE ITEM (v2.17, MANDATORY):

  The old wording ("list every individual topic/item") did not define the unit.
  For CSIR Life Sciences that spans 85 (lettered subsections) to ~700
  (individual concepts) — a ~10x swing that FLIPS the S2-3 ratio guardrail
  between WARN and pass on an IDENTICAL taxonomy. Six of eleven real syllabi
  tested are prose-dense, so the ambiguity governs the majority of items.

  TWO LEVELS ARE RECORDED. Do not pick one and discard the other:

    ENTRY  — the smallest unit carrying its OWN heading, bullet, or
             letter/number label. THIS is a syllabus_item.
             CSIR "A. Photosynthesis" = 1 entry.
             CTET bullet "Remedial Teaching" = 1 entry.
    ATOMIC — a delimiter-separated concept INSIDE an entry (';' preferred,
             else ','). Recorded as a COUNT ONLY, never as separate items.
             "Light harvesting complexes, mechanisms of electron transport,
              photoprotective mechanisms, CO2 fixation" = 1 entry, 4 atomic.

  Never split an entry into multiple items on a delimiter. Splitting inflates
  the item count, breaks 1:1 coverage checking, and makes counts irreproducible
  across sessions — the exact non-determinism the provenance record exists to
  remove.

  WHY BOTH: the inflation guardrail means different things per syllabus style.
    ENUMERATED (entries ARE concepts — CTET, CAT, UGC glossary):
      measure subtopics / ENTRIES, thresholds 2.0x warn / 3.0x hard stop.
      Preserves the MPPSC Botany calibration (336/81 = 4.1x) the thresholds
      were originally set against — verified still HARD STOPs.
    PROSE (a whole section is one entry — JAM Physics, CUET PG Math, GATE, NEET):
      measure subtopics / ATOMIC, thresholds 0.85x warn / 1.0x hard stop.
      Measured against entries instead, 7 of 11 real syllabi HARD STOP as FALSE
      POSITIVES. For prose the failure is INVERTED: a ratio at or above 1.0 means
      one subtopic per concept, i.e. NO grouping happened — MPPSC restated.

  Style is DETECTED, not chosen: median atomic-per-entry <= 1.5 => ENUMERATED,
  else PROSE. Computed per SUBJECT (a syllabus may mix both). Depends only on
  delimiters present in the text, so it is reproducible across sessions.
  See classify_style() / ratio_verdict() in syllabus_provenance.py.

HIERARCHY PRESERVATION (v2.17 — MANDATORY):

  WHY: a syllabus that reads
        Chemistry > Physical Chemistry > Thermodynamics
  already STATES which group the item belongs to. Flattening it to
  (Chemistry, Thermodynamics) discards that fact and forces S2-3 to
  RE-DERIVE by judgment something the source document supplied as data.
  Re-derived facts cannot be verified against anything; recorded facts can.
  This is the same defect class as discarding the subject would be.

  For every item record:
    syllabus_path  : ordered list of headings ABOVE the item, outermost
                     first, verbatim. e.g. ["Chemistry","Physical Chemistry"]
                     For a flat syllabus this is just ["Chemistry"].
    syllabus_group : the IMMEDIATE parent heading below the subject —
                     syllabus_path[1] if it exists, else None.
                     None means the syllabus supplied NO grouping.

  DO NOT INVENT A GROUP. If the syllabus lists items directly under the
  subject with no intermediate heading, syllabus_group is None. Inventing
  one manufactures false ground truth — strictly worse than recording none,
  because downstream checks would then verify against fiction.

  DEEP HIERARCHIES (Subject > Unit > Chapter > item): record the FULL
  path in syllabus_path. syllabus_group is always the immediate child of
  the subject (syllabus_path[1]). Deeper levels are preserved for audit
  but are NOT used for anchoring — which level maps to a taxonomy Topic
  is exam-specific and cannot be assumed.

  ENUMERATIVE HEADINGS ("Unit I", "Part A", "Module 2") are recorded like
  any other heading. Anchoring never compares heading NAMES to topic names,
  only consistency of mapping, so semantically empty labels work fine.

TERMINOLOGY NOTE — "Subject" vs "Section":
  The SYLLABUS defines Subject names (the top-level taxonomy grouping).
  The EXAM PATTERN defines Section names (the OTS paper structure).
  These are independent — see S2-2a "SECTION ≠ SUBJECT" note.
  The taxonomy uses Subject > Topic > Subtopic throughout.
  In the framework code and JSON, the taxonomy key 'section' historically
  refers to the SUBJECT (from syllabus), not the OTS section (from exam
  pattern). This naming is preserved for backward compatibility with all
  downstream steps (PYQSort, PYQExtract, Blueprint, MockCreate, etc.).

S2-3 determines which items become Topics vs Subtopics using the
Topic Integrity Test and 6 Pattern Dimensions.

═══════════════════════════════════════════════════════════════════
DUPLICATE-SUBJECT SEATBELT (v1.1.0 — C9; TYPE-2 INPUT INTEGRITY,
NOT a defect-halt mechanism and NOT a multi-phase mode)
═══════════════════════════════════════════════════════════════════
SCOPE DECISION (operator guarantee): multi-phase notifications ingested as
one exam, and exams with no prescribed syllabus, are OPERATOR INPUT ERRORS —
the operator guarantees one proper single-phase syllabus per ExamCode. No
multi-phase mode and no syllabus-absent mode exist or may be built; a missing
syllabus keeps S1-2's existing ask-the-operator behavior.

This ONE guard is retained because the failure it prevents is SILENT data
loss, not a halt: the taxonomy dict keys by subject name, so a wrongly
supplied multi-phase document producing two subjects with the same
normalized name would have the second silently OVERWRITE the first — one
phase's subjects vanish with C1 passing on the survivor.

RULE: immediately after extracting syllabus_subjects, and again inside
save_taxonomy_draft (S2-4), run syllabus_provenance.find_duplicate_subjects
on the list. A non-empty return → STOP AS TYPE-2 with exactly one operator
action — never proceed, never merge, never prescribe re-derivation:

  "This document appears to contain more than one exam/phase (subject
   '<name>' appears twice). Provide the single-phase syllabus for this
   ExamCode and re-run PYQDraft."

Entry dedup (E5) operates WITHIN one subject only, so it can never mask this
condition. Under the operator guarantee this seatbelt should never fire; its
existence converts a would-be invisible wrong answer into a one-touch input
correction.

═══════════════════════════════════════════════════════════════════
EMISSION WIRING (v1.1.0 — D2; per-item and per-subject E5 states)
═══════════════════════════════════════════════════════════════════
S2-1/S2-3e emissions gain, wired to syllabus_provenance E5:
  * excluded — per S2-3 EXCLUSION RULES' RECORDING MANDATE, each excluded
    item's emission carries excluded: {class, reason} INSTEAD of 'to'
    (mutually exclusive; the gate enforces it).
  * dedup — build_items merges canon-identical entries per subject, and
    near-identical ones at the C5 threshold (pass
    reconcile_taxonomy.DUP_SIMILARITY as dup_similarity — cite, never
    restate). Its dedup_report is carried into save_taxonomy_draft.
    MULTI-GRANULARITY (archetype A4, DECISION D4): when the same content
    appears at multiple granularities, prefer the most granular listing
    from the most authoritative source region; the official document wins
    on conflict; coaching tables fill gaps; order the authoritative region
    FIRST in the emissions so the mechanical keep-first rule keeps it.
  * qcount_anchored_topics — emitted per S2-3 "WHEN SYLLABUS ASSIGNS
    QUESTION COUNTS" ANCHORING RECORD.
  * subject flags — syllabus_provenance.detect_subject_flags computes
    skeletal / open_ended per subject; the caller passes
    min_items=reconcile_taxonomy.OVER_AGG_MIN_ITEMS (one rulebook — the
    value is cited from the engine, never restated here).
```

### S2-2 — Exam Pattern extraction

Two paths: S2-2a (xlsx — preferred) and S2-2b (legacy — fallback).

#### S2-2a — XLSX parser (deterministic, preferred)

```python
import pandas as pd
from openpyxl import load_workbook

def parse_exam_pattern_xlsx(xlsx_path, exam_code):
    """
    Parse the standardized 3-tab Exam Pattern xlsx.
    Returns exam_config dict ready for save_exam_config().
    Raises SystemExit on any validation failure.
    """
    wb = load_workbook(xlsx_path)
    required_sheets = {'Overview', 'Sections', 'Range'}
    if not required_sheets.issubset(set(wb.sheetnames)):
        missing = required_sheets - set(wb.sheetnames)
        raise SystemExit(
            f"HARD STOP: Exam Pattern xlsx missing required tab(s): {missing}. "
            f"Expected 3 tabs: Overview, Sections, Range.")

    # ── TAB 1: Overview (key-value, no header row) ────────────────────
    df_ov = pd.read_excel(xlsx_path, sheet_name='Overview', header=None)
    ov = dict(zip(df_ov[0].str.strip(), df_ov[1]))
    # Required fields
    for field in ['Total Questions', 'Medium', 'Question Type',
                  'Total Marks', 'Duration', 'Level']:
        if field not in ov:
            raise SystemExit(
                f"HARD STOP: Overview tab missing required field: '{field}'.")
    total_questions = int(ov['Total Questions'])
    total_marks     = float(ov['Total Marks'])
    medium          = str(ov['Medium']).strip()
    # question_types: comma-separated string → sorted list
    question_types  = sorted(set(
        t.strip() for t in str(ov['Question Type']).split(',')
    ))
    # duration: "180 Min" → 180 (expected format: "<number> Min")
    # Extracts all digits from the string. If duration is in hours,
    # the xlsx must convert to minutes before saving (e.g., "180 Min" not "3 Hours").
    dur_str = str(ov['Duration']).strip()
    time_minutes = int(''.join(c for c in dur_str if c.isdigit()))
    level = str(ov['Level']).strip()

    # ── TAB 2: Sections (table with header row) ──────────────────────
    df_sec = pd.read_excel(xlsx_path, sheet_name='Sections')
    required_cols = {'Section', 'Total Question', 'Question Starts',
                     'Question Ends', 'Max Attempt'}
    if not required_cols.issubset(set(df_sec.columns)):
        missing = required_cols - set(df_sec.columns)
        raise SystemExit(
            f"HARD STOP: Sections tab missing required column(s): {missing}.")
    sections = []
    for idx, row in df_sec.iterrows():
        sections.append({
            'name':        str(row['Section']).strip(),
            'q_count':     int(row['Total Question']),
            'q_range':     [int(row['Question Starts']),
                            int(row['Question Ends'])],
            'max_attempt': int(row['Max Attempt']),
            'subject_order': idx
        })

    # ── TAB 3: Range (table with header row) ─────────────────────────
    df_rng = pd.read_excel(xlsx_path, sheet_name='Range')
    required_cols_r = {'Question Range', 'Question Type',
                       'Correct Marks', 'Negative Marks'}
    if not required_cols_r.issubset(set(df_rng.columns)):
        missing = required_cols_r - set(df_rng.columns)
        raise SystemExit(
            f"HARD STOP: Range tab missing required column(s): {missing}.")
    marking_scheme = []
    for _, row in df_rng.iterrows():
        parts = str(row['Question Range']).split('-')
        rs, re_ = int(parts[0].strip()), int(parts[1].strip())
        marking_scheme.append({
            'q_range':        [rs, re_],
            'question_type':  str(row['Question Type']).strip(),
            'correct_marks':  float(row['Correct Marks']),
            'negative_marks': float(row['Negative Marks'])
        })

    # ── 10 STRUCTURAL VALIDATIONS ────────────────────────────────────
    issues = []

    # V1: Section sum = Total Questions
    sec_sum = sum(s['q_count'] for s in sections)
    if sec_sum != total_questions:
        issues.append(
            f"V1: Sum of section Total Question ({sec_sum}) ≠ "
            f"Overview Total Questions ({total_questions}).")

    # V2: Q_Ends − Q_Starts + 1 == Total Question per section
    for s in sections:
        computed = s['q_range'][1] - s['q_range'][0] + 1
        if computed != s['q_count']:
            issues.append(
                f"V2: Section '{s['name']}': Q{s['q_range'][0]}-"
                f"Q{s['q_range'][1]} = {computed} Qs but "
                f"Total Question = {s['q_count']}.")

    # V3: Section Q-ranges contiguous and non-overlapping
    prev_end = 0
    for s in sections:
        if s['q_range'][0] != prev_end + 1:
            issues.append(
                f"V3: Section '{s['name']}' starts at Q{s['q_range'][0]} "
                f"but previous section ended at Q{prev_end}. "
                f"Expected Q{prev_end + 1}.")
        prev_end = s['q_range'][1]
    if prev_end != total_questions:
        issues.append(
            f"V3: Last section ends at Q{prev_end}, not Q{total_questions}.")

    # V4: Range tab tiles Q.1 through Total Questions completely
    prev_end_r = 0
    for ms in marking_scheme:
        if ms['q_range'][0] != prev_end_r + 1:
            issues.append(
                f"V4: Range {ms['q_range']} starts at Q{ms['q_range'][0]} "
                f"but previous range ended at Q{prev_end_r}.")
        prev_end_r = ms['q_range'][1]
    if prev_end_r != total_questions:
        issues.append(
            f"V4: Last range ends at Q{prev_end_r}, not Q{total_questions}.")

    # V5: All Negative Marks ≤ 0
    for ms in marking_scheme:
        if ms['negative_marks'] > 0:
            issues.append(
                f"V5: Range {ms['q_range']} has positive Negative Marks "
                f"({ms['negative_marks']}). Must be ≤ 0.")

    # V6: Σ(Max Attempt × correct_marks) == Total Marks
    # Build per-Q marks lookup, then compute per-section attempt marks
    marks_by_q = {}
    for ms in marking_scheme:
        for q in range(ms['q_range'][0], ms['q_range'][1] + 1):
            marks_by_q[q] = ms['correct_marks']
    attempt_marks_total = 0.0
    for s in sections:
        sec_total = sum(
            marks_by_q.get(q, 0)
            for q in range(s['q_range'][0], s['q_range'][1] + 1)
        )
        if s['q_count'] == s['max_attempt']:
            attempt_marks_total += sec_total
        else:
            # Proportional (uniform marks within section assumed for
            # attempt-limited sections; exact when all ranges within
            # section have the same correct_marks)
            attempt_marks_total += sec_total * s['max_attempt'] / s['q_count']
    if abs(attempt_marks_total - total_marks) > 0.01:
        issues.append(
            f"V6: Attempt marks ({attempt_marks_total:.2f}) ≠ "
            f"Total Marks ({total_marks}). Check Max Attempt values.")

    # V7: max_attempt must be > 0 and ≤ q_count for every section
    for s in sections:
        if s['max_attempt'] <= 0:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']}. "
                f"Must be > 0.")
        if s['max_attempt'] > s['q_count']:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']} > "
                f"q_count={s['q_count']}. Cannot attempt more than total.")

    # V8: question_types from Overview must match distinct types in Range tab
    range_types = sorted(set(ms['question_type'] for ms in marking_scheme))
    if question_types != range_types:
        issues.append(
            f"V8: Overview Question Type {question_types} does not match "
            f"Range tab types {range_types}. Both must list the same set.")

    # V9: correct_marks must be > 0 for every range
    for ms in marking_scheme:
        if ms['correct_marks'] <= 0:
            issues.append(
                f"V9: Range {ms['q_range']} has correct_marks="
                f"{ms['correct_marks']}. Must be > 0.")

    # V10: total_questions and time_minutes must be > 0
    if total_questions <= 0:
        issues.append(f"V10: total_questions={total_questions}. Must be > 0.")
    if time_minutes <= 0:
        issues.append(f"V10: time_minutes={time_minutes}. Must be > 0.")

    if issues:
        msg = "HARD STOP: Exam Pattern xlsx failed validation:\n"
        for i, issue in enumerate(issues, 1):
            msg += f"  {i}. {issue}\n"
        msg += "Fix the xlsx and re-upload."
        raise SystemExit(msg)

    # ── BUILD EXAM_CONFIG ─────────────────────────────────────────────
    exam_config = {
        'exam_code':       exam_code,
        'exam_name':       '',    # filled by Claude from pattern/syllabus context
        'total_questions':  total_questions,
        'total_marks':      total_marks,
        'time_minutes':     time_minutes,
        'medium':           medium,
        'question_types':   question_types,
        'level':            level,
        'marker_mode':      False,   # determined from PYQ structure, not xlsx
        'session_keyword':  'Shift', # default; user may override
        'page_size':        'A4',
        'options_count':    4,       # auto-detected from PYQ at Step 5
        'sections':         sections,
        'marking_scheme':   marking_scheme
    }
    return exam_config
```

```
SECTION ≠ SUBJECT — CRITICAL ARCHITECTURAL NOTE:

  Section names from the Sections tab (e.g., "Part A", "Part B", "Part C" for
  CSIR NET; "General Aptitude", "Biotechnology" for GATE) are ONLINE TEST SERIES
  (OTS) display labels. They define how the test platform presents and organizes
  sections to the student during the exam.

  Section names are NOT Subject names for the taxonomy. The syllabus (provided
  separately in S2-1) defines Subjects, Topics, and Subtopics.

  A single Subject from the syllabus can have questions spanning MULTIPLE sections.
  Example: CSIR NET Life Science — "Cell Biology" questions appear in both Part B
  (Q.21-70, 2 marks) and Part C (Q.71-145, 4 marks).

  Conversely, for exams like SSC CGL, section names happen to align closely with
  subject areas, but the framework still derives subjects from the syllabus — never
  from section names.

  The framework uses section names ONLY for:
    1. Q-range boundaries (which question numbers belong to which section)
    2. Marking scheme linkage (which scoring rules apply to which questions)
    3. Max attempt enforcement (OTS platform concern, not paper generation)
    4. OTS display labels (passed through to the platform as metadata)
```

```
SYLLABUS-TRANSITION DECLARATION KEYS (v1.2.0 — GAP-2026-09-01 §3.1):

  The Overview tab may OPTIONALLY carry up to three further key-value rows —
  `Syllabus Changed`, `New Syllabus Effective From`, `Zero History Approved`
  — plus the seven dial override keys of S2-0a. The parser above needs NO
  change: `ov = dict(zip(...))` ignores unknown keys, so absence is
  cost-free estate-wide; dict(zip) keeps the LAST occurrence of a duplicated
  key, which S2-0a turns into a WARN. All consumption, normalization
  ("YES"/" Yes " activate; Excel datetime EF cells coerce; boolean TRUE is
  NOT "yes"), near-miss reporting and validation live in S2-0a and its
  engine functions — this parser only delivers the raw dict. Verified
  against the driving exam's real file: values stored as text ("YES",
  "2026-12") activate directly.
```

#### S2-2b — Legacy extraction (AI-interpreted, fallback)

```
Used when exam pattern is provided as image, PDF, .docx, or plain text
(not the standardized xlsx). Claude reads the document and extracts:

  exam_code           : from trigger
  sections            : list of {name, q_count, q_range: [start, end],
                         max_attempt (= q_count if not stated)}
  total_questions     : sum of all section q_counts
  total_marks         : from pattern
  time_minutes        : from pattern
  medium              : from pattern (default: "English")
  question_types      : from pattern (default: ["MCQ"])
  level               : from pattern (default: "Graduation")
  marking_scheme      : inferred from pattern — if a single marks value is stated
                         (e.g., "each question carries 2 marks"), produce one entry
                         covering Q.1 through total_questions. If per-section marks
                         are stated, produce one entry per section. If unclear,
                         ask user.
  marker_mode         : true if exam uses section separators in paper,
                        false if sections determined by Q-number range.
                        If unclear → ask user.

  After extraction, run the same 10 validations (V1-V10) as the xlsx path.
  Any failure → flag to user with specific issue and ask to correct.

  The legacy path produces the SAME exam_config schema as the xlsx path.
  All downstream steps consume exam_config.json identically regardless
  of which input path was used.
```


### S2-3 — Draft taxonomy generation  →  HOSTED IN Framework_PYQCore.md
# The full S2-3 section (Topic Integrity Test, per-entry decision tree Q1/Q2/Q3,
# Unique Domain Property, ratio guardrails, 6 Pattern Dimensions Appendix) is
# hosted in Framework_PYQCore.md because PYQScan S3-6 executes the same machinery
# (§11 EXAM-AGNOSTIC GUARANTEE declares it universal). Read it there and execute
# it HERE, at this position, as part of --taxonomy mode. Content unchanged.


### S2-3e — SYLLABUS MAPPING EMISSION (v2.17, MANDATORY — closes S2-3)

```
S2-3 derives the taxonomy from the syllabus. This step RECORDS HOW.

WHY MANDATORY: Step 2c (PYQApprove) reconciles the taxonomy against the
syllabus (S4-0). It can only do that if the derivation recorded which
taxonomy path(s) each syllabus item became. Without this record, PYQApprove
has no ground truth and must fall back to asking a human an academic
question — the exact defect v2.17 exists to remove.

The mapping is a BY-PRODUCT OF DERIVATION, not a reconstruction after the
fact. Claude MUST record each item's destination AT THE MOMENT it places
that item into the taxonomy. Reconstructing the mapping afterwards by
name-matching re-introduces the guesswork this record exists to eliminate.

EMIT, for every syllabus item identified in S2-1:

  {
    "id":             "SYL-001",          # stable, assigned in S2-1 order
    "subject":        "<verbatim S2-1 subject name>",
    "syllabus_path":  ["Chemistry","Physical Chemistry"],   # S2-1, verbatim
    "syllabus_group": "Physical Chemistry",                 # or null if flat
    "raw_text":       "<verbatim syllabus item text>",
    "enumerated":     true,               # explicitly listed in syllabus
    "source_ref":     "<locator: page/line/bullet, best effort>",
    "mapped_paths":   ["Subject/Topic/Subtopic", ...],
    "deviation":      null                # or {"rule": ..., "reason": ...}
  }

ALSO EMIT the group -> topic mapping (one entry per non-null syllabus group):

  group_topic_map: [
    {"subject": "Chemistry",
     "group":   "Physical Chemistry",
     "mapped_topics": ["Chemistry/Physical Chemistry"]}    # 1..N topics
  ]

  This declares, ONCE per group, which taxonomy Topic(s) that syllabus group
  legitimately became. Items are then anchored THROUGH this declaration.

─────────────────────────────────────────────────────────────────────
CONFORM-OR-DECLARE (v2.17 — the topic-placement anchor)
─────────────────────────────────────────────────────────────────────
S2-3 is EXPECTED to override syllabus grouping — the Topic Integrity Test
exists precisely to split badly-grouped syllabus entries (e.g. a single
"Grammar" heading MUST become separate Topics for distinct question types).
So deviation from the syllabus grouping is NORMAL AND OFTEN CORRECT. It is
NOT an error signal, and MUST NOT be auto-flagged as one — doing so would
fire on exactly the cases the framework is designed to produce.

The rule is therefore CONFORM OR DECLARE, never CONFORM OR FAIL:

  CONFORM  — every mapped_path's Topic appears in group_topic_map for that
             item's (subject, group). Nothing further required.

  DECLARE  — the item lands in a Topic outside its group's declared map.
             LEGAL, but the item MUST carry:
               "deviation": {
                 "rule":   "TOPIC_INTEGRITY_TEST" | "SPLIT" | "MERGE" | "OTHER",
                 "reason": "<one line: why this item left its syllabus group>"
               }

  UNDECLARED DEVIATION → HARD ERROR. This is the only failure mode, and it
  is purely structural: no judgment about whether the placement is CORRECT,
  only whether it was DECLARED. Zero false positives by construction.

WHAT THIS DOES AND DOES NOT ACHIEVE (do not overstate):
  DOES     — makes every departure from the syllabus's own structure
             explicit, recorded, and reviewable. Silent misplacement becomes
             impossible: an item cannot quietly drift to another Topic.
  DOES NOT — verify that a declared deviation is CORRECT. A wrong placement
             with a plausible reason still passes. Declaration converts an
             invisible unbounded risk into a small named list; it does not
             eliminate the risk.

FLAT SYLLABI (syllabus_group is null):
  No grouping was supplied, so there is NOTHING to anchor against. The
  correct Topic is not present in ANY input — not the syllabus, not the exam
  pattern, and not the PYQs (the scan classifies by SUBTOPIC, inheriting the
  parent Topic, so a wrong parent produces no classification error). This is
  an INFORMATION limit, not an engineering gap.
  Handling: skip anchoring for that subject and RECORD it as unanchorable in
  the approval record, so the gap is named rather than silent.

MAPPING RULES:
  1. An item that became its OWN Topic maps to EVERY subtopic under that
     Topic (a Topic is realized by its subtopics — the Topic itself is a
     label, not a leaf).
  2. An item GROUPED under a shared Topic maps to the ONE subtopic that
     represents it (per S2-3 GROUPED ITEMS ARE SUBTOPICS).
  3. An item SPLIT across multiple subtopics maps to ALL of them.
  4. Two items MERGED as genuinely synonymous both map to the SAME single
     path. This is legal and is NOT a duplicate.
  5. mapped_paths MUST be [] if the item genuinely has no taxonomy
     representation. NEVER invent a path to make the list non-empty —
     an empty list is a truthful signal that S4-0 will surface as
     ITEM_UNMAPPED. A fabricated mapping hides data loss permanently.
  6. Path strings MUST be byte-identical to the taxonomy keys/values
     (§7 NAME CONSISTENCY CONTRACT). No re-typing; copy from the taxonomy.

Pass syllabus_subjects and syllabus_items to save_taxonomy_draft() (S2-4).
Run syllabus_provenance.validate_provenance BEFORE saving. HARD STOP on failure.
It is the ONLY implementation of these checks — do not re-implement it here.
```

```python
# ─────────────────────────────────────────────────────────────────
# S2-3e VALIDATION — SINGLE IMPLEMENTATION (v2.17)
# ─────────────────────────────────────────────────────────────────
# There is exactly ONE implementation of these checks:
#     syllabus_provenance.validate_provenance()
#
# Two spec-embedded duplicates (verify_syllabus_mapping,
# verify_topic_anchoring) were REMOVED here. They parsed paths as
# '/'-delimited STRINGS while build_items() emits LIST paths, so a
# perfectly valid mapping was reported as an UNDECLARED DEVIATION on
# EVERY item of EVERY exam. Two call sites were live simultaneously,
# each using a different implementation.
#
# ANTI-DRIFT (same force as the §D6 detection-logic rule): validation
# logic MUST NOT exist in two places. A second copy does not stay in
# sync — it silently diverges and then contradicts the first.
#
# All path handling is LIST-based end to end. Nothing splits or joins
# a path for comparison; see norm_path() in syllabus_provenance.py.
# ─────────────────────────────────────────────────────────────────
```



### S2-3e-1 — MINIMAL EMISSION FORMAT (v2.17, Issue C — supersedes hand-built records)

```
DO NOT hand-emit the 9-field item records. Emit FOUR fields per item and let
syllabus_provenance.build_items derive the rest. A field that is DERIVED
cannot be emitted wrong; a field that is TYPED can be.

PER ITEM emit exactly:
  path : ["Chemistry","Physical Chemistry"]      headings ABOVE the item,
                                                 outermost first, verbatim.
                                                 ["Chemistry"] if flat.
  text : "Thermodynamics"                        verbatim item text
  to   : [["Chemistry","Physical Chemistry","Thermodynamics"]]
                                                 destination(s), each a LIST of
                                                 exactly 3 components
  why  : "one line"                              ONLY when a destination leaves
                                                 the item's syllabus group
  rule : TOPIC_INTEGRITY_TEST | SPLIT | MERGE | OTHER   (optional, with `why`)

DERIVED AUTOMATICALLY (never emit these):
  id, subject, syllabus_group, enumerated, deviation{rule,reason}

PATHS ARE LISTS, NEVER STRINGS. This is not stylistic. Real subject names
contain '/' — IIT JAM Biotechnology has "Microbial/Plant/Animal Biotech".
Any '/'-joined path is unparseable in general and produced FALSE ANCHOR
FAILURES on live data. A joined string is REJECTED at build time.

group_topic_map MUST BE DECLARED FROM THE SYLLABUS STRUCTURE — i.e. what each
heading SHOULD become — NOT derived from where items were actually sent.
A DERIVED map makes conform-or-declare CIRCULAR: every item conforms by
construction and the check silently passes any misplacement. This was found by
testing 11 real syllabi: all 11 initially passed anchoring for this reason, not
because the mappings were correct. derive_group_topic_map() therefore refuses to
run without _authorized=True and is for bootstrapping an editable draft ONLY;
validate_provenance(map_is_declared=False) hard-errors.

ALSO emit ONCE (not per item):
  syllabus_style   : classify_style(items) output, per subject. Drives the
                     style-aware C4 inflation check at S4-0. Omitting it makes
                     C4 fall back to the legacy whole-corpus ratio, which
                     false-hard-stops prose syllabi.
  syllabus_total   : integer count of ENTRIES you are about to emit.
                     Compared against what actually arrives — catches silent
                     truncation on long syllabi, the dominant failure mode.
  group_topic_map  : one entry per syllabus group:
                     {"subject":..., "group":..., "mapped_topics":[[subj,topic]]}
                     ~1 line per group (tens), not per item (hundreds).

BATCHING (long syllabi): process in bounded chunks, emitting the running count
after each. Never emit a partial set as if complete — syllabus_total is the
contract that makes truncation detectable rather than silent.
```

```python
# S2-3e EXECUTION (replaces hand-built records) — v1.1.0: dedup + exclusions +
# flags wired (D2); density BOTH forms at the pre-delivery gate (GATE-AT-SOURCE).
from syllabus_provenance import (build_items, canonicalize_paths,
                                 validate_provenance, derive_group_topic_map,
                                 detect_subject_flags, find_duplicate_subjects)
from reconcile_taxonomy import (check_topic_density, DUP_SIMILARITY,
                                OVER_AGG_MIN_ITEMS)

# ANCHORING RECORD input (S2-3 "WHEN SYLLABUS ASSIGNS QUESTION COUNTS"):
# populated DURING S2-3 derivation — one topic name per syllabus-assigned
# question-count boundary; stays [] for syllabi that assign none.
qcount_anchored_topics = []

dups = find_duplicate_subjects(syllabus_subjects)     # C9 seatbelt (Type-2)
if dups:
    raise SystemExit(
        f"This document appears to contain more than one exam/phase "
        f"(subject '{dups[0]}' appears twice). Provide the single-phase "
        f"syllabus for this ExamCode and re-run PYQDraft.")

items, build_errors, dedup_report = build_items(emissions, group_topic_map,
                                                dup_similarity=DUP_SIMILARITY)
if build_errors:
    raise AnchoringGateFailure(build_errors)          # S2-3f self-correction

# §7: snap destinations to the taxonomy's exact spelling BEFORE validation
name_fixes = canonicalize_paths(taxonomy, items)

ok, errors, warnings, unanchorable = validate_provenance(
    taxonomy, items, syllabus_subjects, group_topic_map,
    declared_total=syllabus_total)
if not ok:
    raise AnchoringGateFailure(errors)                # S2-3f self-correction

subject_flags = detect_subject_flags(items, min_items=OVER_AGG_MIN_ITEMS)

# PRE-DELIVERY DENSITY — BOTH forms, the SAME engine function C6 backstops.
# Any finding => self-correct per the GATE-AT-SOURCE LAW: split the NAMED
# topics along their syllabus items and re-check, within the law's rounds;
# telemetry records each round; exhaustion exits AMBER per S2-3f.
density_findings = check_topic_density(
    items, taxonomy, qcount_anchored=frozenset(qcount_anchored_topics),
    excluded_ids=frozenset())

# name_fixes / dedup_report / flags must be PASSED to save_taxonomy_draft —
# none is a global:
#   save_taxonomy_draft(taxonomy, exam_config, exam_code, syllabus_subjects,
#                       items, group_topic_map, name_fixes=name_fixes,
#                       qcount_anchored_topics=qcount_anchored_topics,
#                       subject_flags=subject_flags, dedup_report=dedup_report,
#                       telemetry=telemetry, amber_status=amber_status)
```

### S2-3f — GATE FAILURE HANDLING (v2.17, B-FIX — operator never sees a traceback)

```
The S2-3e gate fires on CLAUDE'S OWN output during Step 2a. The operator did
nothing wrong and can do nothing about it. A Python traceback reaching them is
a spec violation of the same class as asking them an academic question: it
puts an unanswerable artifact in front of someone with no means to act.

ON AnchoringGateFailure — SELF-CORRECT, DO NOT ESCALATE:

  ATTEMPT 1 — read each error and fix the CAUSE, not the symptom:
    "UNDECLARED DEVIATION"      -> the item left its syllabus group. Decide:
                                   is the placement CORRECT?
                                     YES -> add deviation {rule, reason}
                                     NO  -> correct mapped_paths instead
                                   Do NOT reflexively add a declaration to
                                   silence the gate — a declaration on a WRONG
                                   placement launders an error into a record
                                   that looks reviewed. Fix the mapping first.
    "no group_topic_map entry"  -> add the missing group -> topic declaration
    "deviation.rule not in..."  -> use TOPIC_INTEGRITY_TEST | SPLIT | MERGE | OTHER
    "empty reason"              -> write a real one-line reason
    "mapped_path not present"   -> the path is a typo or the taxonomy lacks it
    "hierarchy ... inconsistent"-> re-run S2-1 extraction for that subject:
                                   some items got a group, some did not
    Re-run the gate.

  ATTEMPT 2 — if it still fails, re-derive that subject's mapping from S2-3,
  CONSUMING attempt 1's error list verbatim (constraint-carrying: every retry
  reads the prior attempt's specific errors; blind retries are prohibited, and
  repeating attempt 1's identical fix is prohibited — the law's
  anti-oscillation guard).

  ATTEMPT 3 (v1.1.0 — the budget is the law's
  reconcile_taxonomy.SELF_CORRECTION_MAX_ROUNDS; the pre-v1.1.0 two-attempt
  dead end is in SPEC_HISTORY.md) — same constraint-carrying discipline,
  consuming attempt 2's error list.

  ON EXHAUSTION — AMBER DELIVERY, never a dead-end stop (§6.4-S1 mechanics;
  the record MUST remain structurally valid or downstream C7/S4-0 consumption
  breaks):

    1. Each remaining UNDECLARED DEVIATION is auto-declared with
       rule: OTHER, reason: "AMBER: unresolved after 3 rounds — <original
       error>".
    2. Each remaining STRUCTURAL error (missing group_topic_map entry,
       unresolvable mapped_path) is resolved to its DATA-PRESERVING form:
       empty mapped_paths for the item — the truthful ITEM_UNMAPPED signal —
       NEVER an invented path (MAPPING RULE 5).
    3. The residue list goes into amber_status, FINDING-KEYED (normative
       shape): {gate, rounds: 3, unresolved: [{class, item, detail}, ...]}
       where `class` is the finding class the residue will produce at
       PYQApprove (e.g. TOPIC_OVER_AGGREGATION, TOPIC_OVER_AGGREGATION_TOPIC,
       ITEM_UNMAPPED) and `item` is the normalize_label-normalized identity
       (subject name, topic name, or SYL-id) — the SAME keying
       resolve_declared_amber matches on and fingerprint hashes on. A
       free-text-only residue is unmatchable and therefore a spec violation:
       it converts a declared imperfection back into an undeclared one.
    4. validate_provenance MUST pass on the delivered record. AMBER flags
       imperfection; it never licenses an invalid artifact.
    5. Deliver with the Framework_DeliveryFooter F1 AMBER quality-gate
       footer naming the residue (existing §5 Q0 machinery — no new footer
       type), the unresolved errors named in taxonomy_draft.json telemetry
       AND in the delivery message. PYQApprove resolves the matching
       findings as DECLARED_AMBER Tier 0 (engine E7): the taxonomy still
       locks; the imperfection stays permanently visible.

  A genuinely unsatisfiable constraint set (e.g. a dedup-merge vs
  Q-count-anchor conflict) therefore exits AMBER in ≤3 rounds with telemetry
  naming the conflict, and the PIPELINE CONTINUES.

  No traceback. No field names. No stack. No request to judge anything.

TRANSLATION TABLE (error -> plain line):
  UNDECLARED DEVIATION        -> "A syllabus item was placed under a different
                                  topic than the syllabus lists it under."
  no group_topic_map entry    -> "A syllabus heading has no matching topic."
  mapped_path not present     -> "An item points to a topic that doesn't exist."
  hierarchy ... inconsistent  -> "The syllabus headings were read inconsistently
                                  for one subject."
  deviation rule/reason bad   -> "A recorded change is missing its explanation."
  COUNT MISMATCH              -> "Part of the syllabus was not read — the number
                                  of items does not match what was expected."
  must be a list / joined str -> "A topic location was written in the wrong
                                  format."
  exactly 3 components        -> "A topic location is incomplete."
```

### S2-4 — Taxonomy draft output

```python
import json

class AnchoringGateFailure(Exception):
    """S2-3e gate failure. Caught and self-corrected by Claude (S2-3f).
    Reaches the operator ONLY as the plain-language S2-3f message."""
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__(f"{len(self.errors)} undeclared/invalid mapping(s)")


def save_taxonomy_draft(taxonomy, exam_config, exam_code,
                        syllabus_subjects=None, syllabus_items=None,
                        group_topic_map=None, name_fixes=None,
                        qcount_anchored_topics=None, subject_flags=None,
                        dedup_report=None, telemetry=None, amber_status=None,
                        syllabus_sha256=None):
    """
    v2.17: persists the SYLLABUS PROVENANCE RECORD alongside the derived
    taxonomy. Without it, Step 2c (PYQApprove) has no machine-readable ground
    truth and its reconciliation cannot run (S4-0).

    syllabus_subjects: [str] verbatim subject names exactly as S2-1 recorded.
    syllabus_items:    [{'id','subject','raw_text','enumerated',
                         'source_ref','mapped_paths':[...]}]
      mapped_paths = taxonomy paths ('Section/Topic/Subtopic') realizing this
      item. EMPTY list means the item was dropped -> S4-0 flags ITEM_UNMAPPED.
      Every item S2-3 places into the taxonomy MUST record its path(s) here.
    name_fixes:       output of canonicalize_paths() (§7 spelling corrections).
                      Passed in, NOT a free variable — it is produced by the
                      S2-3e block that runs BEFORE this function.
    group_topic_map:  [{'subject','group','mapped_topics':[...]}] — declares
      which taxonomy Topic(s) each syllabus group legitimately became.
      Required for CONFORM-OR-DECLARE anchoring (S2-3e). Omit ONLY when the
      syllabus supplies no grouping at all (fully flat).
    """
    # C9 SEATBELT (v1.1.0 — Type-2, second enforcement point after S2-1).
    # A duplicate normalized subject would key-collide in `sections` below and
    # silently delete one phase's subjects with C1 passing on the survivor.
    from syllabus_provenance import find_duplicate_subjects
    _dups = find_duplicate_subjects(syllabus_subjects or list(taxonomy))
    if _dups:
        raise SystemExit(
            f"This document appears to contain more than one exam/phase "
            f"(subject '{_dups[0]}' appears twice). Provide the single-phase "
            f"syllabus for this ExamCode and re-run PYQDraft.")

    from reconcile_taxonomy import SPEC_GENERATION
    draft = {
        'exam_code': exam_code,
        'version': 'draft',
        # D2 (v1.1.0): the generation stamp. Written on EVERY current-
        # generation draft; its ABSENCE is what identifies a pre-release
        # draft to the PYQScan F1 tripwire and the PYQApprove A1 three-case
        # rule — omitting it from this producer breaks both consumers.
        'spec_generation': SPEC_GENERATION,
        'source': 'syllabus + exam pattern',
        'syllabus_subjects': syllabus_subjects or [],
        'syllabus_items': syllabus_items or [],
        'group_topic_map': group_topic_map or [],
        # v1.1.0 (D2/E5) — absence semantics per the release handshake map:
        # no anchoring => full C6 domain; flags absent/false => normal
        # judgment; empty dedup_report => no merges; empty telemetry => no
        # auto-corrections fired; amber_status None => no residue declared.
        'qcount_anchored_topics': qcount_anchored_topics or [],
        'subject_flags': subject_flags or {},
        'dedup_report': dedup_report or [],
        'telemetry': telemetry or [],
        'amber_status': amber_status,
        # v1.2.0 (§3.10 STALENESS LOCK): sha256 of the taxonomy's SOURCE
        # file — the S2-0a-resolved CURRENT file in active-transition mode,
        # the single syllabus file otherwise, None for legacy chat-pasted
        # input (a None field is written as null and consumers treat it
        # exactly like an absent field: exempt, no retro-invalidation).
        # Consumers compare via bc.check_syllabus_staleness => HS-ST7.
        'syllabus_sha256': syllabus_sha256,
        'sections': {},
        'exam_config': exam_config
    }
    for section, topics in taxonomy.items():
        draft['sections'][section] = {}
        for topic, subtopics in topics.items():
            draft['sections'][section][topic] = subtopics

    # Count totals
    total_subtopics = sum(
        len(subs) for topics in taxonomy.values()
        for subs in topics.values()
    )
    draft['total_subtopics'] = total_subtopics

    # v2.17 provenance gate — surfaces a broken S2-3 mapping immediately
    # rather than 3 steps later at PYQApprove.
    if syllabus_items:
        unmapped = [i['raw_text'] for i in syllabus_items if not i.get('mapped_paths')]
        if unmapped:
            print(f"WARNING: {len(unmapped)} syllabus item(s) have no mapped_paths "
                  f"— these will be flagged ITEM_UNMAPPED at PYQApprove: {unmapped[:5]}")

        # v2.17 CONFORM-OR-DECLARE gate. Runs HERE so an undeclared topic
        # deviation is caught at Step 2a, not discovered at Step 2c or later.
        ok_a, err_a, warn_a, unanchorable = validate_provenance(
            taxonomy, syllabus_items, syllabus_subjects, group_topic_map,
            declared_total=len(syllabus_items))
        if not ok_a:
            # v2.17 (B-FIX): this gate fires during CLAUDE'S OWN Step 2a work,
            # never as a result of anything the operator did. Claude MUST
            # self-correct per S2-3f and re-run. A raw traceback must NEVER be
            # the operator's first contact with this failure — they cannot act
            # on it, and surfacing it recreates the exact "unanswerable prompt"
            # problem v2.17 exists to remove.
            raise AnchoringGateFailure(err_a)
        draft['unanchorable_subjects'] = unanchorable
        draft['name_canonicalizations'] = list(name_fixes or [])
        draft['syllabus_style'] = classify_style(syllabus_items)
        draft['declared_deviations'] = [
            {'id': i['id'], 'subject': i.get('subject'),
             'group': i.get('syllabus_group'), 'deviation': i['deviation']}
            for i in syllabus_items if i.get('deviation')]
        if unanchorable:
            print(f"NOTE: {len(unanchorable)} subject(s) have a FLAT syllabus — "
                  f"topic placement cannot be anchored for: {unanchorable}")

    path = f'/mnt/user-data/outputs/{exam_code}_taxonomy_draft.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(draft, f, indent=2, ensure_ascii=False)
    return path

# Also save exam_config separately (PYQSort needs this)
def save_exam_config(exam_config, exam_code):
    path = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(exam_config, f, indent=2, ensure_ascii=False)
    return path
```

### S2-5 — Exam config schema

```json
{
  "exam_code": "[ExamCode]",
  "exam_name": "[Exam Full Name]",
  "total_questions": 145,
  "total_marks": 200,
  "time_minutes": 180,
  "medium": "English",
  "question_types": ["MCQ"],
  "level": "Post Graduation",
  "marker_mode": false,
  "session_keyword": "Shift",
  "page_size": "A4",
  "options_count": 4,
  "sections": [
    {
      "name": "[Section 1 Name]",
      "q_count": 20,
      "q_range": [1, 20],
      "max_attempt": 15,
      "subject_order": 0
    },
    {
      "name": "[Section 2 Name]",
      "q_count": 50,
      "q_range": [21, 70],
      "max_attempt": 35,
      "subject_order": 1
    },
    {
      "name": "[Section 3 Name]",
      "q_count": 75,
      "q_range": [71, 145],
      "max_attempt": 25,
      "subject_order": 2
    }
  ],
  "marking_scheme": [
    {
      "q_range": [1, 20],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [21, 70],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [71, 145],
      "question_type": "MCQ",
      "correct_marks": 4,
      "negative_marks": -1.0
    }
  ]
}
```

Field definitions:
  exam_code          : alphanumeric + underscore (from trigger).
  exam_name          : human-readable exam name (from Exam Pattern doc or syllabus).
  total_questions    : sum of all section q_counts.
  total_marks        : maximum marks achievable (accounts for attempt limits).
  time_minutes       : total exam duration in minutes.
  medium             : exam language — "English", "Hindi", "Bilingual", etc.
                       From Overview tab. Step 5 auto-detection validates against this;
                       xlsx value takes priority on conflict.
  question_types     : sorted list of distinct question types across all ranges.
                       e.g., ["MCQ"] or ["MCQ", "MSQ", "NAT"]. Derived from Range tab's
                       Question Type column. Controls which Step 5 extensions activate:
                         ["MCQ"] only → MSQ/NAT dormant.
                         includes "MSQ" → multi_select_allowed = true.
                         includes "NAT" → nat_present = true.
  level              : academic level — "Graduation", "Post Graduation",
                       "Under Graduation", "School". From Overview tab.
                       Step 7 uses for question complexity calibration.
                       Step 9 uses for explanation depth.
  marker_mode        : true if exam uses === separators in PYQ papers, false if
                       sections determined by Q-number range. NOT in xlsx — determined
                       from PYQ structure at scan time; default false.
  session_keyword    : the keyword used in date labels (Shift/Slot/Phase/Paper/Session).
                       NOT in xlsx — read from Exam Pattern context or default "Shift".
                       Step 1 uses this when producing Row files; PYQSort reads it for
                       date parsing.
  page_size          : "A4" (default, Indian standard) or "Letter" (US). PYQSort reads
                       this for output .docx page setup.
  options_count      : default number of options per question (typically 4 or 5).
                       PYQSort reads this for option-count validation. Auto-detected
                       from PYQ at Step 5 (PARAMETER 7).
  sections[]         : per-section structural definitions.
    name             : OTS display label (NOT a Subject name for taxonomy — see S2-2a).
    q_count          : total questions in this section.
    q_range          : [start_inclusive, end_inclusive] Q-number boundaries.
    max_attempt      : max questions student may attempt in this section. The framework
                       generates ALL q_count questions; max_attempt is OTS platform
                       metadata. When max_attempt == q_count, there is no attempt limit.
                       Used ONLY for V6 marks validation:
                       Σ(max_attempt × correct_marks) must equal total_marks.
    subject_order    : 0-based display order.
  marking_scheme[]   : per-range scoring rules. Ordered by q_range start ascending.
    q_range          : [start_inclusive, end_inclusive] — must tile Q.1 through
                       total_questions with no gaps or overlaps (validated by V4).
                       A single section can contain multiple marking_scheme ranges
                       (e.g., GATE Biotechnology: section Q.11-65 has 6 ranges with
                       mixed MCQ/MSQ/NAT and mixed 1-mark/2-mark).
    question_type    : "MCQ", "MSQ", or "NAT" for this range.
    correct_marks    : marks awarded per correct answer. Float (supports 4.75 etc.).
    negative_marks   : penalty per wrong answer. Must be ≤ 0. Float.
                       0 = no negative marking for this range.

  HELPER — get marks/type for a specific question number:
    To find correct_marks for Q.72: scan marking_scheme[] for the entry where
    q_range[0] ≤ 72 ≤ q_range[1] → returns that entry's correct_marks.
    Same for question_type and negative_marks.
    Step 5, 6, 7, 8, 9 use this lookup pattern.

OPTIONAL BLOCK — syllabus_transition (v1.2.0 — GAP-2026-09-01 §3.5; R29):

```json
{
  "syllabus_transition": {
    "status": "active | inactive",
    "effective_from": "2026-12",
    "reason": "SC='Y' not in {Yes,No}; treated as No",
    "keys_seen": { "Syllabus Changed": "Y",
                   "New Syllabus Effective From": null },
    "current_file": "[ExamCode]_Syllabus_2026-12.pdf",
    "current_sha256": "…",
    "superseded": [ { "file": "[ExamCode]_Syllabus_2019-06.pdf",
                      "sha256": "…" } ],
    "dials": { "D-1": 3, "D-2": 5.0 },
    "zero_history_approved": ["<subject>"]
  }
}
```

  Written whenever trace or activation applies; ABSENT for T1 row 1 (both
  keys absent — the deployed-estate path, P1). SOLE WRITER: PYQDraft
  (bc.build_syllabus_transition_block assembles it; S2-0a places it into
  exam_config before save_exam_config). IMMUTABLE until PYQDraft re-runs.
  DECLARATION-DERIVED FIELDS ONLY — n_new lives in the count manifest
  (PYQCount's artefact, Release B) and the rotation cursor in the delivery
  manifest (MockDeliver's artefact, Release C); the §3.7 drift guard
  compares declaration fields only (R29). Field semantics:
    status                : "active" | "inactive" (bc.resolve_transition).
    effective_from        : YYYY-MM; active state only.
    reason / keys_seen    : inactive-trace states only (raw values quoted).
    current_file/_sha256  : active state; the S2-0a-resolved CURRENT file.
    superseded[]          : active state; every other dated syllabus file,
                            date order, with sha256.
    dials                 : effective §3.9 values (factory unless a valid
                            Overview override was given); dial_traces may
                            accompany it when an invalid override fell back.
    zero_history_approved : §3.5 A1 — subjects the operator approved as
                            legitimately zero-history (suppresses HS-ST8).
  Downstream steps read ONLY this block, never the xlsx.

### S2-6 — Delivery and next step

```
TAXONOMY MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 2 files.
    1. [ExamCode]_taxonomy_draft.json
    2. [ExamCode]_exam_config.json
  No other files. Run S10-2 pre-delivery checklist before present_files.

Deliver taxonomy_draft.json and exam_config.json via present_files.

Print:
  "Phase 0a complete.
   Draft taxonomy: [N] sections, [M] topics, [K] subtopics.
   Syllabus entries: [E]. Ratio: [K/E]× (guardrail: ≤ 3.0×).
   Near-duplicate pairs: [D] (must be 0).
   Density: [per subject — items/topic, both forms clean | AMBER residue named]
   Exclusions recorded: [X] ([by class]). Dedup merges: [G]. Flags: [skeletal /
     open_ended subjects, if any]. Q-count-anchored topics: [list | none].
   Auto-corrections (telemetry): [T] recorded.
   [ONLY when amber_status is set — F1 AMBER footer per S2-3f, and:]
   AMBER: delivered with [U] declared unresolved residue(s): [class — item,
     one line each]. PYQApprove will report these as DECLARED_AMBER (Tier 0).

   Exam config:
     Total questions : [total_questions]
     Total marks     : [total_marks]
     Duration        : [time_minutes] min
     Medium          : [medium]
     Question types  : [question_types]
     Level           : [level]
     Sections        : [sections_count] ([section_names])
     Marking ranges  : [marking_scheme_count] range(s)
     Attempt limits  : [Yes/No] ([max_attempt per section if Yes])
     Validations     : V1-V10 PASSED
     Syllabus transition (v1.2.0 — printed ONLY when the S2-5 block exists):
       [active:]   Transition ACTIVE — effective from [EF]; CURRENT
                   [current_file]; [k] superseded file(s); dials [effective
                   values, once per run].
       [inactive-trace:] Syllabus declaration present but inactive: [reason].
       [plus each S2-0a console WARNING/NOTE line — duplicates, near-misses,
        invalid dial overrides, unmatched Zero History Approved names.]

   NEXT: Upload both files to [ExamCode] project knowledge.
         Then run: PYQScan
         (with Row files uploaded or Drive link provided)"
```

---


---

# END OF Framework_PYQDraft v1.3.0
