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
                    'key_smiles', 'starting_smiles', 'reagents', 'answer_kind', 'task_template')
# v1.17 (GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY): the per-item non-organic fidelity records
QINDEX_NF_FIELDS = ('subject', 'part', 'mip', 'given_in_stem', 'measured_axis2', 'text_fingerprint', 'stem_text',
                    'option_texts', 'manifest_hash')
QINDEX_V589_FIELDS = ('difficulty_check', 'figural_ask_type', 'representations',
                      'scheme_grammar', 'marked_sites', 'ladder',
                      'slot_chain')            # v1.15: a DISCLOSED item's exhausted chain (S13-4c re-derives it)
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

def bv_batch_step(exam, n, ruler=None, manifest=None, bank=None, op_profile=None, home='/home/claude', echo=True):
    """THE in-batch verification step of Create S4-7 STEP A2 (S0-BV), for the CURRENT batch of paper <exam> M<n>.
    Idempotent and resume-safe: (1) collects every outstanding fresh job whose sub-agent returned REVIEW DONE (v1.18:
    one reviewer job per (round, k) solves, grades and reads the figures of every question of the batch; a per-role
    job of release 2026.11.11 — GRADE / SOLVE / VISION DONE — is still collected) (lines in
    <home>/<exam>_M<n>_bv/returned.txt: '<job_dir> <reply line>'); (2) runs the within-paper checks
    (bc.intra_paper_duplicates / bc.key_leak_check over every question up to this batch — a hit on a question of this batch
    is its one rewrite); (3) decides every question of the batch (bc.bv_apply) and keeps the verification state in
    batch_state['bv']['items'] (write_q_to_sidecar replaces a sidecar entry — the one-rewrite limit survives it);
    (4) writes the fresh jobs still needed (job folder = packet.json + JOB_BRIEF.txt). Returns {'status':
    'jobs_out'|'rewrite'|'done', 'jobs': [dirs], 'rewrite': [q], 'settled', 'disclosed', 'key_chain', 'open', 'lines'}
    and prints the lines (echo). v1.19: never raises for a missing reviewer — a question still without fresh
    results after bc.BV_MAX_ROUNDS job rounds is carried unlabelled to S13-2L (batch_state['bv']['unmeasured'])."""
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
    _ans_bv = _kd_bv.get('answers') or {}
    _labs_bv = list(_bs_bv.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
    _bp_bv = (_bs_bv.get('batch_plan') or [])[int(_bs_bv.get('current_batch', 1)) - 1]
    _qs_bv = [str(q) for q in range(int(_bp_bv['q_start']), int(_bp_bv['q_end']) + 1) if str(q) in _cm_bv]
    _tgt_bv = {str(k): v for k, v in (_bs_bv.get('difficulty_plan_target') or _bs_bv.get('difficulty_plan') or {}).items()}
    _ru_bv = ruler or {}
    _man_bv = manifest or {}
    _bank_bv = bank or {}
    _root_bv = os.path.join(home, f'{exam}_M{n}_bv')
    os.makedirs(_root_bv, exist_ok=True)
    _st_bv = _bs_bv.setdefault('bv', {})
    if _st_bv.get('batch') != _bp_bv['batch_id']:
        _keep_items = dict(_st_bv.get('items') or {})          # every earlier batch's verification record
        _st_bv.clear()
        _st_bv.update({'batch': _bp_bv['batch_id'], 'round': 0, 'jobs': [], 'status': 'open', 'items': _keep_items})
    _ret_bv = {}
    if os.path.exists(os.path.join(_root_bv, 'returned.txt')):
        for _ln in open(os.path.join(_root_bv, 'returned.txt'), encoding='utf-8'):
            _pp = _ln.strip().split(' ', 1)
            if len(_pp) == 2:
                _ret_bv[_pp[0]] = _pp[1]
    try:
        import figural_vision as _fv_bv
        import corpus_io as _ci_bv
        _vcmp_bv, _vprf_bv = _fv_bv.readback_compare, _ci_bv.organic_figure_proof
    except Exception:                                   # noqa: BLE001 — dormant: S13-2L's figure-proof chain covers it
        _vcmp_bv, _vprf_bv = None, None
    # 1. COLLECT every outstanding job whose fresh sub-agent returned DONE
    _res_bv = {}
    for _j in _st_bv.get('jobs') or []:
        _rp = os.path.join(_j['dir'], 'result.json')
        _line = str(_ret_bv.get(_j['dir'], ''))
        if str(_j.get('role', '')).startswith('reviewer_'):
            # v1.18 (2026.11.12): ONE reviewer job per (round, k) for every question of the batch
            if _line.startswith('REVIEW DONE') and os.path.exists(_rp):
                try:
                    _rv = json.load(open(_rp, encoding='utf-8'))
                except (OSError, ValueError):
                    _rv = None
                _k = int(str(_j['role']).rsplit('_', 1)[-1])
                _split = bc.bv_split_reviewer_result(_k, _rv, _labs_bv, _j.get('qs'), _j['sha256'],
                                                     {q: (_cm_bv.get(q) or {}).get('figure_dicts') for q in (_j.get('qs') or [])})
                for _q2, _rr in _split.items():
                    _res_bv.setdefault(_q2, {}).update(_rr)
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
    # S0-NF-6 IN THE BATCH: a question of this batch that repeats an earlier question's template, or that
    # takes part in an answer leak (the later of the two), is rewritten as its ONE rewrite (bc.bv_apply findings)
    _all_bv = []
    for _qa, _ea in _cm_bv.items():
        if not isinstance(_ea, dict) or not str(_qa).isdigit() or int(_qa) > int(_bp_bv['q_end']):
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
    _pyq_bv = ([r.get('stem_snippet') for r in bc.pyq_guard_pool(op_profile)
                if isinstance(r, dict) and r.get('stem_snippet')] if op_profile else [])
    for _a, _b, _v in bc.key_leak_check(_all_bv, _pyq_bv):
        _cand = [x for x in (str(_a), str(_b)) if x in _qs_bv]
        if _cand:
            _x = max(_cand, key=int)
            _o = str(_b) if _x == str(_a) else str(_a)
            _fnd_bv.setdefault(_x, []).append(f'answer leak with Q{_o} ({_v}) — change the data so the value is not given')
    # 2. DECIDE every question of the batch (bc.bv_apply) and 3. WRITE the jobs still needed
    _acts_bv, _new_jobs, _needs_bv = {}, [], {}
    _jr_bv = int(_st_bv.get('round', 0))               # job rounds issued so far for this batch
    for _q in _qs_bv:
        _e = dict(_cm_bv[_q])
        # the verification state lives in batch_state (write_q_to_sidecar REPLACES the sidecar entry on a
        # rewrite — the attempt count must survive it, or a question could be rewritten more than once)
        if isinstance((_st_bv.get('items') or {}).get(_q), dict):
            _e['bv'] = _st_bv['items'][_q]
        _e.setdefault('subject', bc.nf_subject_key(_e, _man_bv))
        _e.setdefault('manifest_hash', bc.manifest_hash(_man_bv))
        _e.pop('bc.manifest_hash', None)                # a key mis-written by release 2026.11.11
        _cr = _e.get('ca_range') if isinstance(_e.get('ca_range'), (list, tuple)) and len(_e.get('ca_range')) == 2 else None
        _tol = (abs(float(_cr[1]) - float(_cr[0])) / 2.0) if _cr else None
        # the I/O shell hashes every rendered organic figure (a redraw keeps its file name) and injects the fresh
        # vision comparer and the proof writer (S0-OP-8) — the thin core never reads a file or imports RDKit
        if isinstance(_e.get('figure_dicts'), list):
            _e['figure_dicts'] = [dict(_fd, render_sha=(hashlib.sha256(open(str(_fd['file']), 'rb').read()).hexdigest()
                                                        if _fd.get('file') and os.path.exists(str(_fd['file'])) else None))
                                  if isinstance(_fd, dict) else _fd for _fd in _e['figure_dicts']]
        _r = bc.bv_apply(_e, _tgt_bv.get(_q), _labs_bv, _ru_bv, _ans_bv.get(_q), str(_e.get('qtype') or 'mcq'),
                         _tol, results=_res_bv.get(_q) or {}, findings=_fnd_bv.get(_q),
                         vision_compare=_vcmp_bv, figure_proof=_vprf_bv,
                         asked=(_st_bv.get('asked') or {}).get(_q))
        _cm_bv[_q] = _r['entry']
        _st_bv.setdefault('items', {})[_q] = _r['entry'].get('bv')
        _acts_bv.setdefault(_r['action'], []).append(_q)
        if _r['roles']:
            _needs_bv[_q] = list(_r['roles'])
        if _r['action'] == 'rewrite':
            # the rewritten text is new content: its reviewers have not been asked yet (the ask count is per content)
            (_st_bv.get('asked') or {}).pop(_q, None)
    # 3. WRITE the fresh jobs still needed: at most bc.BV_REVIEWERS reviewer jobs for the WHOLE batch (v1.18)
    if _needs_bv and _jr_bv >= bc.BV_MAX_ROUNDS:
        # v1.19 (2026.11.13, S0-BV BV-11): never a stop — the questions the platform returned no fresh reviewer for
        # stay unlabelled in this batch (STEP A2 DONE lists them; S13-2L measures them at Final Assembly) and the
        # batch goes on
        _st_bv['unmeasured'] = sorted(set(_st_bv.get('unmeasured') or []) | set(_needs_bv), key=int)
        _say(f"STEP A2: no fresh reviewer returned for {sorted(_needs_bv, key=int)} after {bc.BV_MAX_ROUNDS} rounds — "
             f"carried unlabelled to S13-2L (no stop).")
        _needs_bv = {}
    if _needs_bv:
        _bg_bv = bc.bv_band_guide(_ru_bv, _labs_bv)
        _anc_bv = {q: bc.bv_anchors(_bank_bv, _ru_bv, (_cm_bv[q] or {}).get('subtopic_id'),
                                    str((_cm_bv[q] or {}).get('qtype') or 'mcq'), _labs_bv) for q in _needs_bv}
        for _jb in bc.bv_reviewer_jobs(_needs_bv, _cm_bv, _anc_bv, _labs_bv, _bg_bv):
            _d = os.path.join(_root_bv, f"b{_bp_bv['batch_id']}", f"r{_jr_bv + 1}", _jb['role'])
            os.makedirs(_d, exist_ok=True)
            _pk = json.loads(json.dumps(_jb['packet'], default=str))

            def _copy1(_f):
                if _f and os.path.exists(str(_f)):
                    _dst = os.path.join(_d, os.path.basename(str(_f)))
                    shutil.copy(str(_f), _dst)
                    return _dst
                return None
            # every fresh context sees the figures: they are COPIED into its own folder (it may read nothing else)
            for _row in _pk['items']:
                if isinstance(_row.get('item'), dict) and _row['item'].get('figure_files'):
                    _row['item']['figure_files'] = [x for x in (_copy1(f) for f in _row['item']['figure_files']) if x]
                _row['figures_to_read'] = [x for x in (_copy1(f) for f in (_row.get('figures_to_read') or [])) if x]
            # the sha binds the packet AS WRITTEN (its figure paths point into the job's own folder)
            _sha = hashlib.sha256(json.dumps(_pk, sort_keys=True, default=str, ensure_ascii=False).encode('utf-8')).hexdigest()
            json.dump(_pk, open(os.path.join(_d, 'packet.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(os.path.join(_d, 'JOB_BRIEF.txt'), 'w', encoding='utf-8').write(_jb['brief'].replace('<JOB_DIR>', _d))
            _new_jobs.append({'role': _jb['role'], 'qs': _jb['qs'], 'dir': _d, 'sha256': _sha})
            _kk = _jb['role'].rsplit('_', 1)[-1]
            for _q3 in _jb['qs']:
                for _rl in _needs_bv.get(_q3) or []:
                    if _rl.endswith('_' + _kk):
                        _ak = _st_bv.setdefault('asked', {}).setdefault(_q3, {})
                        _ak[_rl] = int(_ak.get(_rl) or 0) + 1
    for _j in _st_bv.get('jobs') or []:
        _j['done'] = True                       # every job is collected once; a missing result is re-issued above
    _st_bv['jobs'] = _new_jobs
    if _new_jobs:
        _st_bv['round'] = _jr_bv + 1
    _ds_bv = _bs_bv.setdefault('difficulty_state', {})
    _disc = _ds_bv.setdefault('bv_disclosed', {})
    _bst = bc.bv_batch_status(_cm_bv, _qs_bv, _tgt_bv, _labs_bv)
    for _q in _bst['disclosed']:
        _disc[_q] = {'requested': _tgt_bv.get(_q), 'delivered': _cm_bv[_q].get('difficulty')}
    _st_bv['status'] = 'jobs_out' if _new_jobs else ('rewrite' if _acts_bv.get('rewrite') else 'done')
    _st_bv['open'] = _bst['open'] if not _new_jobs and not _acts_bv.get('rewrite') else []
    _st_bv['key_chain'] = _bst['key_chain']
    json.dump(_kd_bv, open(_kp_bv, 'w', encoding='utf-8'), indent=2)
    json.dump(_bs_bv, open(_bsp_bv, 'w', encoding='utf-8'), indent=2)
    _say(f"STEP A2 (job round {_st_bv['round']} of at most {bc.BV_MAX_ROUNDS}): " + '; '.join(f"{k} {v}" for k, v in sorted(_acts_bv.items())))
    if _new_jobs:
        _say("STEP A2: JOBS OUT " + ','.join(j['dir'] for j in _new_jobs))
    elif _acts_bv.get('rewrite'):
        _say(f"STEP A2: REWRITE {_acts_bv['rewrite']} — once each, from concept_map[q]['bv']['rewrite_brief'], then this block again")
    else:
        _say(f"STEP A2: DONE — settled {len(_bst['settled'])}/{len(_qs_bv)} "
              f"(at slot {len(_bst['settled']) - len(_bst['disclosed'])}, disclosed {_bst['disclosed'] or 'none'}); "
              f"key to S13-2L {_bst['key_chain'] or 'none'}; unlabelled {_st_bv['open'] or 'none'}")

    return {'status': _st_bv['status'], 'jobs': [j['dir'] for j in _new_jobs], 'rewrite': list(_acts_bv.get('rewrite') or []),
            'settled': _bst['settled'], 'disclosed': _bst['disclosed'], 'key_chain': _bst['key_chain'],
            'open': _st_bv['open'], 'lines': _lines}



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
        check('bv_rewrite_clears_ask_count', len(r1['jobs']) == 3 and r2['status'] == 'rewrite' and r2['rewrite'] == ['1']
              and '1' not in _asked_after_rw and r3['status'] == 'jobs_out' and len(r3['jobs']) == 3)
    # v1.19 (S0-BV BV-11) — no fresh reviewer at all is never a stop: after bc.BV_MAX_ROUNDS empty rounds the
    # question is carried unlabelled and the batch finishes
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2'],
                                           'subtopic_id': 'A.b', 'qtype': 'mcq'}}, 'answers': {'1': 2}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Hard'}}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _seen, _raised, _last = [], None, None
        try:
            for _i in range(bc.BV_MAX_ROUNDS + 2):
                _last = bv_batch_step('EX', 1, home=_h, echo=False)
                _seen.append(_last['status'])
                if _last['status'] == 'done':
                    break
        except Exception as _ex:                                   # noqa: BLE001
            _raised = _ex
        check('bv_no_reviewer_never_a_stop', _raised is None and _last is not None and _last['status'] == 'done'
              and _last['open'] == ['1'] and 1 <= _seen.count('jobs_out') <= bc.BV_MAX_ROUNDS)
        _bsx = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _bsx['bv'].update({'round': bc.BV_MAX_ROUNDS, 'asked': {}, 'status': 'jobs_out', 'jobs': []})
        _bv_js.dump(_bsx, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        try:
            _mx = bv_batch_step('EX', 1, home=_h, echo=False)
        except Exception as _ex:                                   # noqa: BLE001
            _mx = {'status': f'raised {_ex}'}
        check('bv_max_rounds_carries_unlabelled', _mx['status'] == 'done' and _mx.get('open') == ['1']
              and _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))['bv'].get('unmeasured') == ['1'])
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
