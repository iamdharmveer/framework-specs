# Framework_PYQApprove v1.0.1 — PYQ Step 2c — Analysis Doc Generation & Approval (§4)
# v1.0.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 1 prose mention to no-paren form (write_analysis_doc).
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

## §4 — PHASE 0c: ANALYSIS DOC GENERATION (for approval)

### S4-0 — TAXONOMY RECONCILIATION ENGINE (v2.17, MANDATORY before S4-4)

```
PURPOSE
  PYQApprove is executed by an operator who is non-technical and non-academic
  BY ROLE DEFINITION. Any gate that asks that operator an academic question is
  not a gate — it is theatre with two possible outcomes (rubber-stamp or stall).
  S4-0 converts every question the old S4-4 asked a human into a deterministic
  machine verdict, and constrains the residue so tightly that the operator never
  exercises academic judgment in ANY branch.

EXECUTION
  Module: reconcile_taxonomy.py (tracked in SPEC_MANIFEST.json)
  Run AFTER the Analysis doc is generated (S4-1/S4-2), BEFORE the gate (S4-4).

    from reconcile_taxonomy import (reconcile, apply_tier1, adjudicate,
                                    materialise, conservation_check,
                                    build_approval_record, CheckLedger,
                                    EXPECTED_CHECKS)

    # mode: "FULL" for R1 modes A and C, "DEGRADED" for R1 mode B.
    ledger = CheckLedger()      # INV-7/INV-8 attestation sink — MANDATORY.
                                # Omitting it does not produce a lenient run; it
                                # produces a HELD one. That is deliberate.

    findings          = reconcile(syllabus_items, scan_taxonomy, classifications,
                                  exam_config, syllabus_subjects=syllabus_subjects,
                                  group_topic_map=group_topic_map,
                                  unanchorable_subjects=unanchorable_subjects,
                                  declared_deviations=declared_deviations,
                                  name_canonicalizations=name_canonicalizations,
                                  syllabus_style=syllabus_style,
                                  mode=mode, locked_taxonomy=locked_taxonomy,
                                  ledger=ledger)

    resolved, escalated = apply_tier1(findings)

    # verdicts: {finding_id: {action, confidence, syllabus_present,
    #                         syllabus_quote, rationale}} — authored by the STEP
    #   for Tier 2 findings ONLY, from the syllabus text. An absent verdict is
    #   LEGITIMATE and NOT an error: enforce_invariants() applies the class's
    #   SAFE_DEFAULT. Passing {} is the correct, data-preserving baseline. The
    #   operator is NEVER consulted — Tier 2 is not routed to a human.
    adjudications     = adjudicate(escalated, verdicts, prior_record)

    # MATERIALISE — the ONLY step permitted to change the taxonomy, and it may
    # apply ONLY adjudicated actions. Start from scan_taxonomy:
    #   RETAIN / RETAIN_BOTH / NOTE  -> keep (no mutation)
    #   QUARANTINE                   -> path STAYS LIVE in the taxonomy (D2,
    #                                   v2.17: a review flag, not a deletion)
    #                                   and its path string joins quarantined_paths
    #   DROP / SUPPRESS / MERGE_INTO -> remove the path (reachable only when every
    #                                   hard invariant permitted it). The target MUST
    #                                   resolve to a live taxonomy path; if it does
    #                                   not, the action is returned in `blocked` and
    #                                   the run is HELD (INV-10). It is never applied
    #                                   partially and never silently skipped.
    #   RE_DERIVE                    -> no mutation; the run is HELD
    #   ADD_SECTION / ADD_SUBTOPIC   -> no mutation; returned in `blocked`, which
    #                                   HOLDS the run (INV-9). S4-0 must not
    #                                   invent taxonomy structure.
    # With no Tier 2 actions, final_taxonomy is scan_taxonomy unchanged.
    final_taxonomy, quarantined_paths, blocked = materialise(
                                  scan_taxonomy, resolved, adjudications)

    conservation      = conservation_check(classifications, final_taxonomy,
                                           quarantined_paths)
    # v2.24 (GAP-2026-07-25-002): S4-0 must ATTEST THE TAXONOMY IT LOCKS.
    # NAME-LENGTH GATE FIRST. bc.is_taxonomy_heading() stops recognising text at or
    # above MAX_HEADING_LEN as a heading, so a name longer than that survives this
    # step, survives PYQSort, and then silently stops being a heading at Step 4 and
    # Step 5 — its questions are attributed to the PRECEDING subtopic, with zero
    # orphans and INV-5 conservation still passing because nothing is lost, only
    # mis-filed. The bound is enforced HERE, before the lock, because a name that
    # cannot survive the round trip must never be locked into a taxonomy.
    import blueprint_core as bc
    over_length = [(kind, nm)
                   for sec, tops in final_taxonomy.items()
                   for kind, nm in ([('subject', sec)] +
                                    [('topic', t) for t in tops] +
                                    [('subtopic', x) for t in tops for x in tops[t]])
                   if len(nm) >= bc.MAX_HEADING_LEN]
    if over_length:
        raise SystemExit(
            "HARD STOP: %d taxonomy name(s) are at or above the %d-character heading "
            "limit and cannot be locked.\n  %s\n"
            "A name this long stops being recognised as a heading in the sorted PYQ "
            "files, and every question under it is silently attributed to the "
            "preceding subtopic. Shorten these names in the syllabus mapping (S2-3) "
            "and re-run PYQDraft, then PYQScan, then PYQApprove."
            % (len(over_length), bc.MAX_HEADING_LEN,
               '\n  '.join('%s (%d chars): %r' % (k, len(n), n)
                           for k, n in over_length[:5])))

    record            = build_approval_record(exam_code, findings, resolved,
                                              adjudications, conservation,
                                              mode=mode, ledger=ledger,
                                              blocked=blocked,
                                              prior_record=prior_record,
                                              final_taxonomy=final_taxonomy)

ROUTING: routes.json MUST route reconcile_taxonomy.py to PYQApprove. NOT OPTIONAL.
         S4-0 cannot execute without it, and an unrouted mandatory engine is the
         same silent failure class as an unrouted spec. Enforced by Check AA.

INPUTS
  syllabus_subjects  taxonomy_draft.json['syllabus_subjects']   (S2-4, v2.17)
  syllabus_items     taxonomy_draft.json['syllabus_items']      (S2-4, v2.17)
  scan_taxonomy      scan_progress.json['taxonomy']             (S3-8)
  classifications    [ExamCode]_classifications.json            (S3-8)
  group_topic_map        taxonomy_draft.json['group_topic_map']        (S2-4)
  unanchorable_subjects  taxonomy_draft.json['unanchorable_subjects']  (S2-4)
  declared_deviations    taxonomy_draft.json['declared_deviations']    (S2-4)
  name_canonicalizations taxonomy_draft.json['name_canonicalizations'] (S2-4)
  syllabus_style         taxonomy_draft.json['syllabus_style']         (S2-1e)
  prior_record       [ExamCode]_approval_record.json if present (INV-6 replay)

  ALL of the above MUST be passed to reconcile(). An artifact produced at S2-4
  and not consumed here is a silent regression: the anchoring state would be
  recorded at Step 2a and then invisible at the gate where approval happens.

─────────────────────────────────────────────────────────────────────
APPLICABILITY SCOPING (R1 — MANDATORY, read before running S4-0)
─────────────────────────────────────────────────────────────────────
S4-0 requires the S2-3e provenance record. Exams created before v2.17 do not
have one. The scoping rule below exists because the naive response to a
missing record — "re-run PYQDraft" — is DANGEROUS: PYQDraft RE-DERIVES the
taxonomy, and re-deriving a taxonomy that is already LOCKED can silently
diverge it from mock tests already generated against it. A taxonomy is a
CONTRACT with every downstream artifact built on it.

  RULE: S4-0 NEVER triggers re-derivation of a LOCKED taxonomy. Ever.

Determine mode BEFORE running S4-0:

  A) NEW EXAM — no [ExamCode]_PYQ_Analysis.docx in project Files.
     Taxonomy is not yet locked.
     -> syllabus_items present  : FULL MODE. Run S4-0 Tier 0/1/2. Auto-lock.
     -> syllabus_items absent   : HARD STOP —
          "taxonomy_draft.json has no syllabus provenance record (pre-v2.17)
           and this exam has no locked taxonomy. Re-run PYQDraft to
           regenerate it, then re-run PYQApprove."
        Safe here ONLY because nothing is locked and nothing depends on it.

  B) LEGACY EXAM — [ExamCode]_PYQ_Analysis.docx already exists AND no
     [ExamCode]_approval_record.json. Taxonomy is LOCKED under v2.16 rules.
     -> DEGRADED MODE. Do NOT hard stop. Do NOT re-derive. Do NOT auto-lock.
        Call reconcile(..., mode="DEGRADED", locked_taxonomy=<taxonomy parsed
        from the locked Analysis doc>).

        locked_taxonomy is REQUIRED. Without it C3 has no reference and reports
        EVERY taxonomy path as PATH_EXTRA. reconcile() raises ValueError rather
        than run a check against an absent reference.

        RUNS  : C3 (scan taxonomy vs the LOCKED doc taxonomy), C5, INV-5.
        SKIPS : C1, C2, C6, C7 — all require the S2-3e provenance record.
                C4 — ALSO provenance-dependent, contrary to the pre-v2.23
                wording that listed it as runnable here. BOTH C4 forms divide by
                a syllabus-derived base (entries / atomic concepts / item count).
                With no provenance the divisor collapses to max(0,1) = 1 and
                "ratio" degenerates to the raw subtopic count, so every real
                exam trips RATIO_HARDSTOP and every DEGRADED run would be
                falsely HELD. A check guaranteed to fire is not a check.

        Emit approval_record.json with mode="DEGRADED", status="DEGRADED", and
        checks.declared_skipped = [C1, C2, C4, C6, C7]. Then fall through to the
        v2.16 human gate text. A degraded record MUST NOT report status CLEAN —
        CLEAN asserts a full reconciliation that did not occur. A DEGRADED run
        can never reach S4-4 Branch A and never auto-locks.

  C) RE-RUN — [ExamCode]_approval_record.json exists.
     -> FULL MODE with INV-6 replay of all stored verdicts.

  Migration path for a legacy exam (OPTIONAL, operator never initiates):
    A locked exam is migrated to FULL MODE only by deliberately
    reconstructing syllabus_items against the EXISTING locked taxonomy —
    mapping recorded to what IS, never re-derived into what WOULD BE. This
    is a maintenance task, never part of a PYQApprove run.

─────────────────────────────────────────────────────────────────────
TIER 0 — DETERMINISTIC RECONCILIATION (no judgment, no human)
─────────────────────────────────────────────────────────────────────
  C1 SUBJECT_MISSING    syllabus subject with no taxonomy section      -> Tier 2
     SUBJECT_EXTRA      taxonomy section not in syllabus subjects      -> Tier 2
  C2 ITEM_UNMAPPED      syllabus item with empty mapped_paths          -> Tier 2
                        (the data-loss class — MPPSC Botany defect)
  C3 PATH_EXTRA         taxonomy path claimed by no syllabus item      -> Tier 1
                        (DEGRADED mode: path absent from the LOCKED doc)
  C4 RATIO_WARN / RATIO_HARDSTOP — taxonomy inflation. TWO MUTUALLY
     EXCLUSIVE FORMS; exactly one runs per FULL-mode call:
       STYLE_AWARE (default whenever syllabus_style is present and
         syllabus_provenance is importable) — measured PER SUBJECT:
           ENUMERATED  2.0x warn / 3.0x hard stop   (basis = entries)
           PROSE       0.85x warn / 1.0x hard stop  (basis = atomic concepts)
         Subjects are matched to taxonomy sections via normalize_label().
       LEGACY (only when no usable syllabus_style) — whole corpus,
         subtopics / syllabus items, 2.0x warn / 3.0x hard stop.
     The form actually used is RECORDED in approval_record.checks.c4_form,
     and approval_record.thresholds reports the thresholds ACTUALLY applied.
     RATIO_WARN -> Tier 0 (informational). RATIO_HARDSTOP -> Tier 2.
  C5 NEAR_DUPLICATE     >75% name similarity within the same Topic     -> Tier 2
  C6 TOPIC_OVER_AGGREGATION  syllabus crushed into too few topics      -> Tier 2
     Measured as DENSITY, not as absolute counts: fires when a subject has
     >= 10 syllabus items AND >= 5.0 items per topic. The pre-v1.1 absolute
     rule ("<=4 topics AND >=10 items") encoded ONE exam's scale and false-
     fired on legitimately small exams — 1 subject / 3 topics / 12 items was
     held as over-aggregated. Because the safe default for this class is
     RE_DERIVE, a false fire is a HARD BLOCK, so the measure must be
     scale-free across a fleet of ~200 exams of differing syllabus sizes.
     S2-3 states the target shape — "the syllabus items ARE the Topics" —
     so items-per-topic is the direct measure of departure from it.
  C7 ANCHORING COVERAGE (informational, Tier 0 — never blocks):
       UNANCHORABLE_SUBJECT  subject whose syllabus supplied no grouping
       DECLARED_DEVIATION    item that deliberately left its syllabus group
       ANCHOR_MAP_UNUSED     group_topic_map supplied but never applied
       NAME_CANONICALIZED    destination spelling snapped to the taxonomy (§7)
     C7 is what makes the S4-4 Branch A anchoring lines producible. Without
     it the gate prints zeros for state the S2-4 record explicitly declares.

  THIS LIST IS EXHAUSTIVE AND CLOSED. The checks are INDEPENDENT: no check may
  be skipped, short-circuited, or made conditional as a side effect of the
  branch another check takes. C4 choosing between its two forms MUST NOT
  affect C1, C2, C3, C5, C6 or C7. In FULL mode all seven run on every call.
  The engine records which ones completed AND the size of the measurement
  domain each one actually iterated over; build_approval_record() HOLDS the
  run when it cannot prove completion (INV-7) or when a check ran over an
  empty domain despite non-empty inputs (INV-8).

    ENGINE CONTRACT — SINGLE EXIT. reconcile() returns in exactly one place.
    An early return inside any check's branch is a SPEC VIOLATION.
    GAP-2026-07-25-001: a `return` inside C4's style-aware branch silently
    disabled C5, C6 and C7 for every v2.17+ exam and produced a CLEAN record
    that auto-locked the taxonomy. Mutual exclusion between two forms of one
    check is expressed as if/else, never as function termination.
    Enforced statically by validate_framework_md.py Check AC.

  All comparison is via normalize_label(): NFKC, unicode-dash folding,
  '&'->'and', punctuation strip, whitespace collapse, casefold. This prevents
  false MISSING/EXTRA from cosmetic variance (en-dash vs hyphen, trailing
  space, case) — the exact failure class §7 NAME CONSISTENCY CONTRACT governs.

─────────────────────────────────────────────────────────────────────
TIER 1 — CODIFIED AUTO-POLICY (no judgment, no human)
─────────────────────────────────────────────────────────────────────
  PATH_EXTRA with pyq_count >= MIN_PATTERN_SIZE (3)  -> AUTO-RETAIN
  PATH_EXTRA with pyq_count <  MIN_PATTERN_SIZE      -> AUTO-QUARANTINE

  RATIONALE (why this needs no human): S3-6 already gates every scan-added
  subtopic at MIN_PATTERN_SIZE >= 3 PYQs. A subtopic that is out-of-syllabus but
  present at PYQApprove is therefore PYQ-EVIDENCED BY CONSTRUCTION — real past
  questions were classified into it. S2-3's anti-suppression rule (MPPSC Botany:
  suppressing real content is data loss, not conservative merging) settles the
  call. Retention is also the ASYMMETRIC-COST choice: an extra low-count subtopic
  costs a near-zero blueprint allocation; a dropped subtopic is unrecoverable
  downstream. Retention is logged, never asked.

─────────────────────────────────────────────────────────────────────
TIER 2 — EVIDENCE-BOUND ADJUDICATION (never routed to the operator)
─────────────────────────────────────────────────────────────────────
  Only genuine build defects reach Tier 2. Each verdict MUST supply:
    action            closed set per class (see SAFE_DEFAULT)
    confidence        HIGH | LOW
    syllabus_present  bool — is the item in the syllabus?
    syllabus_quote    verbatim syllabus text (required for any destructive action)
    rationale         short justification

  SIX HARD INVARIANTS — a verdict CANNOT override these. An unsafe verdict is
  REWRITTEN to the safe default (not rejected), so a bad adjudication degrades
  to data-preserving, never to data loss:
    INV-1 NO_SUPPRESS_SYLLABUS         never remove a syllabus-enumerated item
    INV-2 NO_DROP_PYQ_BACKED           never drop a path with >= 3 PYQs
    INV-3 LOW_CONFIDENCE_SAFE_DEFAULT  non-HIGH confidence -> safe default
    INV-4 EVIDENCE_REQUIRED            destructive action needs syllabus_quote
    INV-5 CONSERVATION                 no classified question may be orphaned
    INV-6 REPLAY_DETERMINISM           a finding already adjudicated in
                                       approval_record.json is REPLAYED verbatim,
                                       never re-decided

  THREE ATTESTATION INVARIANTS (v2.23 — GAP-2026-07-25-001). The six above
  constrain what a verdict may DO. These constrain what a RECORD may CLAIM:

    INV-7 CHECK_COMPLETENESS   a status other than HELD asserts that every check
                               expected for the run's mode executed. reconcile()
                               records completions; build_approval_record()
                               rewrites the status to HELD and NAMES the missing
                               check IDs when it cannot prove completion.
                               "Did not run" and "ran and found nothing" must
                               never be representable by the same record.
                               FAIL-SAFE: a caller that passes no attestation
                               sink gets every check marked missing -> HELD.
                               Unknown is never CLEAN.

    INV-8 CHECK_MEASURED       execution alone is not proof. A check that ran
                               over an EMPTY measurement domain while its inputs
                               were NON-EMPTY is VACUOUS, and a vacuous check is
                               indistinguishable from a passing one in its
                               output — so it must be indistinguishable from a
                               FAILING one in its status. Each check attests the
                               size of the domain it iterated over. Vacuous ->
                               HELD, naming the check.
                               (The class this closes: C4's style-aware form
                               matched subjects with raw `==` while every other
                               comparison normalized, so a subject differing only
                               in case or spacing passed C1 and then silently
                               zeroed C4. The check "ran". It measured nothing.)
                               Enforced statically by Check AE.

    INV-9 NO_DERIVATION_AT_S4_0  S4-0 RECONCILES; it must never DERIVE. The safe
                               defaults ADD_SECTION (SUBJECT_MISSING) and
                               ADD_SUBTOPIC (ITEM_UNMAPPED) would require S4-0 to
                               INVENT taxonomy structure. They are therefore
                               UNMATERIALISABLE: materialise() records them and
                               the run is HELD for PYQDraft re-derivation.
                               Pre-v1.1 they were neither applied nor held, so a
                               syllabus subject and an unmapped item could both be
                               dropped while the taxonomy auto-locked CLEAN_ADJUDICATED
                               — silent data loss in the exact class C2 exists to catch.

    INV-10 RESOLVABLE_TARGET   a destructive verdict (DROP / SUPPRESS / MERGE_INTO)
                               must name a LIVE taxonomy path. If materialise()
                               cannot resolve it to one, the action is BLOCKED and
                               the run is HELD — never silently discarded.
                               The taxonomy is unharmed by a no-op removal, but the
                               RECORD would assert a removal that never happened,
                               and a record that misstates what occurred is the same
                               failure class as a check that never ran.
                               (Only PATH_EXTRA carries a path as its `item`, and
                               PATH_EXTRA is resolved at Tier 1 and never reaches a
                               destructive verdict — so every destructively-adjudicable
                               class needs this guard, not a hypothetical few.)

  INV-6 is the determinism guarantee. Finding IDs are content fingerprints
  (sha256 of class + normalized identity), so the same finding yields the same
  ID across sessions and model instances. Re-running PYQApprove replays stored
  verdicts instead of re-deriving them — closing the framework's known
  "spec-as-prose is non-deterministic across instances" failure class at the
  adjudication boundary.

  ADJUDICATION IS NOT DELIVERED AS PROSE. It is a structured record persisted to
  [ExamCode]_approval_record.json. Prose commentary about findings is an
  anti-editorializing violation with the same force as S3-4.

─────────────────────────────────────────────────────────────────────
STATUS (three states — Tier 2 activity is never invisible)
─────────────────────────────────────────────────────────────────────
  CLEAN              zero Tier 2 escalations. Auto-lock.
  CLEAN_ADJUDICATED  Tier 2 ran, all resolved safely. Auto-lock, logged.
  HELD               RE_DERIVE, RATIO_HARDSTOP, or FAILED CONSERVATION (INV-5).
                     Taxonomy NOT locked.
  DEGRADED           legacy exam (mode B). Partial checks only, NO auto-lock,
                     falls through to the v2.16 human gate. Never CLEAN.

  A CLEAN result MUST NOT be printed when adjudications occurred — masking
  Tier 2 activity behind CLEAN defeats the audit trail.
```

### S4-1 — Generate merged Analysis doc from taxonomy

```
After Phase 0b scan completes (convergence or full coverage):
  Run: PYQApprove

PYQApprove REQUIRES these fields from scan_progress.json (v1.7):
  _meta.exam_code                    → used in doc title and filename
  _meta.papers_scanned               → informational (approval gate message)
  _meta.refinement_pass_done         → must be True; if False → error
  _meta.schema_version               → must be "2.0"
  taxonomy                           → complete dict (Section > Topic > [Subtopics])
  exam_config                        → section names, Q counts, metadata
If any required field is missing → "scan_progress.json incomplete. Re-run PYQScan."

This generates a SINGLE merged .docx Analysis doc containing ALL subjects:

  [ExamCode]_PYQ_Analysis.docx

INVOCATION (v2.24 — MANDATORY, not illustrative):

  path = generate_merged_analysis_doc(taxonomy, exam_code, section_order)

  Phase B (--counts) passes the filled counts and REGENERATES rather than editing:

  path = generate_merged_analysis_doc(taxonomy, exam_code, section_order,
                                      counts={(subject, topic, subtopic): n, ...})

  S4-2 delegates to corpus_io.write_analysis_doc. Do NOT hand-build this document
  with docx-js or python-docx: it is the artefact four steps parse, it has exactly
  ONE writer, and that writer is paired with the reader by a round-trip assertion in
  corpus_io --self-test. A hand-built doc is unverified by construction.

  Before v2.24 this function was `pass` and nothing in this spec called it, so the
  doc's structure existed only as prose in S4-1 and every consumer guessed. A
  function that is defined and never invoked is the same defect class as a
  deliverable that is produced and never read.

The doc contains one section per subject (taxonomy top-level), separated by
PAGE BREAKS. Internal format per subject matches the IFAS reference:

  ═══ PAGE BREAK before each subject (except the first) ═══

  HEADER:
    "[ExamCode] — [Section Name]"                          (bold, 14pt)
    "Subject: [Section Name]"                              (bold)
    "PYQ Topic & Subtopic-wise Count"                      (bold)
    "Total: — Questions  |  [N] Topics  |  [M] Subtopics" (bold)

  MASTER SUMMARY TABLE:
    | Topic | Total Subtopics | Total PYQs |
    | Topic 1: [Name] | [count] | — |
    | Topic 2: [Name] | [count] | — |
    | ...             |         |   |
    | GRAND TOTAL     | [total] | — |

  PER-TOPIC SECTIONS (one per topic):
    "Topic [N]: [Topic Name]"                              (bold, heading)
    "Total PYQs: —  |  Subtopics: [count]"                (bold)
    | Subtopic | PYQ Count |
    | [Subtopic 1] | — |
    | [Subtopic 2] | — |
    | ...          |   |
    | TOTAL        | — |

  FOOTER:
    "IFAS Edutech  —  [ExamCode] [Section] PYQ Analysis"

  NOTE: All PYQ Count values are "—" (em-dash) at this stage.
        Phase B (--counts) fills them with actual numbers.

SUBJECT ORDERING (v2.23 — corrected):
  1. If any taxonomy subject name matches an exam_config.sections[].name
     (marker_mode exams, where section labels ARE subject names), those
     subjects lead, in section order.
  2. ALL remaining subjects follow in TAXONOMY ORDER — the key order of
     scan_progress.json['taxonomy'], which preserves the syllabus's own
     order as recorded at S2-1.
  Alphabetical ordering is NOT used.
  Rationale: S2-2a's SECTION != SUBJECT rule defines sections[].name as an OTS
  display label, not a subject. For every non-marker_mode exam the intersection
  in step 1 is therefore EMPTY, so the pre-v2.23 "rare" alphabetical fallback
  was in fact the normal path for almost the whole fleet — discarding the
  syllabus order that S2-1 went to the trouble of preserving.
```

### S4-2 — Analysis doc generation script

```python
# Use docx-js (npm) to create .docx file matching reference format.
# See §6 HEADING FORMAT CONTRACT for heading text patterns.
# All subtopic names MUST be .strip()-ed before writing (§7 NAME CONTRACT).

def generate_merged_analysis_doc(taxonomy, exam_code, section_order, counts=None):
    """Generate the SINGLE merged Analysis .docx containing ALL subjects.

    v2.24 (GAP-2026-07-25-002) — DELEGATED. This function was `pass`, with a comment
    deferring to "the npm docx package per SKILL.md". A stub is not a contract: the
    artefact that four downstream steps parse had no definition anywhere, so each
    consumer guessed at a different structure and three of the four guessed wrong.

    corpus_io.write_analysis_doc() is now THE writer, and corpus_io.read_analysis_doc()
    is THE reader. They are asserted against each other by round-trip,
    read(write(taxonomy)) == taxonomy, over a generated matrix of exam shapes in
    corpus_io --self-test: 1/6/30 subjects, every level-1 and level-2 label form,
    duplicate topic names across subjects, duplicate subtopic names across topics,
    punctuation and non-ASCII in names, boundary-length names, single-subtopic
    topics. The framework serves ~200 exams and cannot be validated against 200 real
    corpora; that matrix is the exam-agnostic correctness claim.

    taxonomy      : {subject: {topic: [subtopic, ...]}}  — order preserved
    section_order : ordered subject list (S4-1 SUBJECT ORDERING, v2.23)
    counts        : Phase B only — {(subject, topic, subtopic): int}. Absent means
                    every PYQ Count cell is an em-dash, per S4-1.

    Emits the header block, the master summary table, the per-topic subtopic tables
    and the footer, with a page break before each subject after the first — and, in
    each of those three places, the count declarations the reader asserts its parse
    against. Those redundant declarations are what make a mis-parse LOUD.
    """
    import corpus_io
    return corpus_io.write_analysis_doc(taxonomy, exam_code,
                                        subject_order=section_order, counts=counts)
```

### S4-3 — Exam config delivery

```
APPROVE MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 3 files (v2.17).
    1. [ExamCode]_PYQ_Analysis.docx  (single merged doc)
    2. [ExamCode]_exam_config.json
    3. [ExamCode]_approval_record.json  (S4-0 audit + INV-6 replay ledger)
  No other files. Run S10-2 pre-delivery checklist before present_files.
  scan_progress.json and classifications.json are INPUTS — do NOT forward.

Also deliver [ExamCode]_exam_config.json (from Phase 0a).
This file is needed by PYQSort for section detection in Q-range mode.

Both the Analysis doc and exam_config.json go to [ExamCode] project Files section.
```

### S4-4 — Approval gate (v2.17 — VERDICT, not questionnaire)

```
The gate PRINTS A VERDICT produced by S4-0. It NEVER asks the operator an
academic question. There are exactly two operator-facing branches, and in
neither does the operator exercise academic judgment.

MANDATORY ORDER: S4-1/S4-2 (generate doc) -> S4-0 (reconcile) -> S4-4 (print).
Printing S4-4 without a completed S4-0 record is a spec violation.

─────────────────────────────────────────────────────────────────────
BRANCH A — status CLEAN or CLEAN_ADJUDICATED  => TAXONOMY AUTO-LOCKED
            (mode A/C only — a DEGRADED run can NEVER reach Branch A)
─────────────────────────────────────────────────────────────────────
Print:
  "Phase 0c complete. Taxonomy reconciled and LOCKED.

   RECONCILIATION: [CLEAN | CLEAN_ADJUDICATED]
     Syllabus subjects   : [K] / [K] present as sections
     Syllabus items      : [N] / [N] mapped to taxonomy paths
     Scan-discovered     : [R] retained (PYQ-evidenced), [Q] quarantined (<3 PYQs)
     Taxonomy ratio      : printed in the form the run ACTUALLY used —
                             STYLE_AWARE -> one line per subject:
                               [Subject]: [S] subtopics / [basis] = [ratio]x
                               (limit [warn]x warn / [stop]x stop, [STYLE])
                             LEGACY -> [S]/[N] = [ratio]x (limit [RATIO_HARDSTOP]x)
                           Read the form and the limits from
                           approval_record.thresholds — never assume 2.0/3.0.
                           A style-aware run judges PROSE subjects at 0.85/1.0,
                           and printing a whole-corpus ratio for a per-subject
                           run reports a number the verdict was not derived from.
     Near-duplicates     : [D] pair(s)
     Checks executed     : [C1..C7 list]   (C4 form: [STYLE_AWARE|LEGACY])
     Checks skipped      : [none | list, with the reason]
     Prior decisions     : [none | [N] replayed verbatim from the existing
                           approval_record (INV-6), recorded by [engine_version]]
                           SAY SO ON THIS LINE when prior_record_attested is
                           false, or when the recording engine differs from the
                           one that just ran — e.g.
                             "2 replayed (recorded by reconcile_taxonomy.py v1.1)"
                             "1 replayed (PRIOR RECORD UNATTESTED — pre-1.1 schema)"
                           Reuse is CORRECT: INV-6 exists so two sessions cannot
                           reach different verdicts on the same finding. But reuse
                           must be VISIBLE. The record carries this state already;
                           a flag that lives only in the JSON is read by nobody,
                           because the gate text is the operator's only interface
                           to what a run actually did. Stating it here is what
                           makes an old decision reviewable instead of invisible.
     Question conservation: [T] classified, 0 orphaned
     Topic anchoring     : [P] subject(s) anchored, [U] unanchorable (flat syllabus)
     Declared deviations : [V] recorded
     Name corrections    : [W] destination spelling(s) snapped to taxonomy (§7)
     Syllabus style      : [subject]=[ENUMERATED|PROSE] ([E] entries, [A] concepts)

   Unanchorable subjects (flat syllabus — topic placement NOT verified):
     [Subject]
     ...
   Declared deviations (departures from syllabus grouping, recorded):
     [SYL-id] [Subject > Group] [rule] — [reason]
     ...

   Retained beyond syllabus (auto, PYQ-evidenced):
     [Subject > Topic > Subtopic]  — [n] PYQs
     ...
   Quarantined (below 3-PYQ threshold, recorded in approval_record.json):
     [Subject > Topic > Subtopic]  — [n] PYQs
     ...

   Files:
   • [ExamCode]_PYQ_Analysis.docx
   • [ExamCode]_exam_config.json
   • [ExamCode]_approval_record.json

   YOUR NEXT ACTION (2 steps, no review needed):
   1. Upload all 3 files to the [ExamCode] project Files section
   2. Run: PYQSort   (upload 1 Row file, same project)"

  If [R] == 0 and [Q] == 0, omit both retained/quarantined lists entirely.
  NO approval prompt. NO confirmation request. NO academic question.

─────────────────────────────────────────────────────────────────────
BRANCH B — status HELD  => TAXONOMY NOT LOCKED
─────────────────────────────────────────────────────────────────────
Print:
  "Phase 0c HELD — taxonomy NOT locked. A build defect was detected.

   HELD ON:
     [finding class] — [item]
       [one-line machine detail]
     ...

   This is a taxonomy construction defect, not an operator decision.
   Do NOT upload the Analysis doc. Do NOT run PYQSort.

   YOUR NEXT ACTION (1 step):
   1. Report the HELD line(s) above and re-run: PYQApprove
      (or re-run PYQDraft if the fix requires taxonomy re-derivation)

   Full detail: [ExamCode]_approval_record.json"

  The operator's entire job in Branch B is to RELAY the named finding.
  They are never asked to evaluate, judge, or decide it.

─────────────────────────────────────────────────────────────────────
BRANCH C — status DEGRADED (legacy exam, mode B)  => NO AUTO-LOCK
─────────────────────────────────────────────────────────────────────
Print the partial reconciliation result, NAME the skipped checks (C1/C2/C6),
state that the taxonomy remains under v2.16 rules, then print the v2.16
approval-gate text unchanged. The operator's position is exactly what it was
before v2.17 — no better, no worse, and critically: nothing is re-derived.

Do NOT present a DEGRADED run as verified. Partial checks reported as if
complete is the false-confidence failure this scoping exists to prevent.

─────────────────────────────────────────────────────────────────────
ANTI-EDITORIALIZING (same force as S3-4)
─────────────────────────────────────────────────────────────────────
The gate output is the CLOSED SET above. Do NOT add:
  ✗ any question directed at the operator
  ✗ "please confirm", "please review", "does this look right"
  ✗ commentary, assessment, or recommendation prose about the taxonomy
  ✗ any request to verify syllabus faithfulness, completeness, or coverage
Every such question is answered by S4-0 or it is a defect in S4-0.

POST-LOCK: after Branch A upload, the taxonomy is LOCKED. approval_record.json
must accompany it — later PYQApprove runs REPLAY its verdicts (INV-6). Losing
this file forfeits the determinism guarantee.
```

---


---

# END OF Framework_PYQApprove v1.0.1
