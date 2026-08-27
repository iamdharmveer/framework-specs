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
     di_manifests / figural_manifests (replace-by-mock-number — these
     entries carry no paper_id field, only "mock": N). This directly
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

__all__ = [
    "commit_registry",
    "regcheck",
    "qindex_certify",
    "predelivery_checklist",
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


def commit_registry(registry, pending, bp, N, *, paper_id, batches_completed,
                     axis2_window_counts, passage_present, di_present,
                     figural_present, concept_map,
                     passage_linked_qs=(), cloze_linked_qs=(),
                     di_manifest=None, fig_manifest=None, figure_specs=None,
                     axis1_snapshots=None, axis3_snapshots=None,
                     framework_repo_commit=None, spec_source_report=None,
                     timestamp=None, answer_key=None):
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

    # ── RC / DI / figural manifests — replace-by-mock (deviation 4) ─────────
    if passage_present:
        rc = [e for e in reg.setdefault('rc_manifests', []) if e.get('mock') != N]
        rc.append({
            "mock": N,
            "passage_linked": sorted(set(passage_linked_qs)),
            "cloze_linked": sorted(set(cloze_linked_qs)),
        })
        reg['rc_manifests'] = rc

    if di_present and di_manifest is not None:
        di = [e for e in reg.setdefault('di_manifests', []) if e.get('mock') != N]
        di.append({
            "mock": N,
            "di_qs": sorted(int(q) for q in di_manifest.get('questions', {})),
            "subtopic_ids": {str(q): v.get('subtopic_id')
                             for q, v in di_manifest.get('questions', {}).items()
                             if v.get('subtopic_id')},
            "table_shapes": {str(q): v.get('table_shape')
                             for q, v in di_manifest.get('questions', {}).items()
                             if v.get('table_shape')},
        })
        reg['di_manifests'] = di

    if figural_present and fig_manifest is not None:
        fg = [e for e in reg.setdefault('figural_manifests', []) if e.get('mock') != N]
        fg.append({
            "mock": N,
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
            "semantic_objects": _validated_semantic_objects(fig_manifest),
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
            "difficulty_obs": concept_map[qn].get("difficulty_obs")}
           for qn in sorted(concept_map, key=int)]
    _qindex_cert = {"blueprint_version": bp.get("blueprint_version"),
                    "subtopic_set_hash": hashlib.sha256("\n".join(sorted(
                        s.get("subtopic_id") or "" for s in bp.get("subtopic_list", [])
                    )).encode("utf-8")).hexdigest()[:16]}
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
    _new_prefix = _series_prefix(paper_id)

    def _stale_sibling(e):
        if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == paper_id:
            return True                      # the pre-v5.54 exact-id rule
        return (e.get('mock') == N
                and _series_prefix(e.get('paper_id')) == _new_prefix)

    reg.setdefault('question_index', [])
    reg['question_index'] = [e for e in reg['question_index'] if not _stale_sibling(e)]
    reg['question_index'].append({"mock": N, "paper_id": paper_id,
                                  "qindex_cert": _qindex_cert, "questions": _qi})

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
    papers_completed[:] = [p for p in papers_completed
                           if p == paper_id
                           or _series_prefix(p) != _new_prefix
                           or _paper_number_or_none(p) != N]
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


def _validated_semantic_objects(fig_manifest):
    """v5.55 — {q: [semantic objects]} from fig_manifest questions[q].semantic_objects,
    each shape-validated (paper_pipeline.validate_semantic_object) and, for a
    STRUCTURE/REACTION, canonicalised through rdkit when available so the
    registry carries the canonical form. Raises ValueError on a malformed object
    — a figure whose identity cannot be stated is not committed."""
    import paper_pipeline as _pp
    out = {}
    for q, v in (fig_manifest or {}).get('questions', {}).items():
        objs = v.get('semantic_objects') or []
        if not objs:
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
    sl_mocks = {e.get('mock') for e in reg.get('session_log', [])
                if _series_prefix(e.get('paper_id')) == series_prefix}
    qi_by_mock = {e.get('mock'): e for e in reg.get('question_index', [])
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


def _duplicate_commit_problems(reg, m):
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
    that claim the same slot."""
    problems = []
    for ledger in ('question_index', 'session_log'):
        by_prefix = Counter(_series_prefix(e.get('paper_id'))
                            for e in reg.get(ledger, []) if e.get('mock') == m)
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

    this_mock_problems = _commit_problems(reg, N, series_prefix=_this_prefix)
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
    this_mock_dups = _duplicate_commit_problems(reg, N)
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

    warnings = [f"mock {m}: {', '.join(_commit_problems(reg, m))}"
               for m in reg.get('mocks_completed', [])
               if m != N and _commit_problems(reg, m)]
    warnings += [f"mock {m}: {', '.join(_duplicate_commit_problems(reg, m))}"
                 for m in reg.get('mocks_completed', [])
                 if m != N and _duplicate_commit_problems(reg, m)]

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
# S13-7 — predelivery_checklist()
# ══════════════════════════════════════════════════════════════════════════
def predelivery_checklist(outputs_dir, *, docx_name, reg_name, dossier_name=None,
                          regcheck_ok, qindex_ok, listdir=None, exists=None):
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
    leaked = [f for f in staged if any(m in f for m in internal)]
    if dossier_name and dossier_name in staged and dossier_name not in leaked:
        leaked.append(dossier_name)
    checks.append(("5 no internal sidecars in outputs", len(leaked) == 0))
    expected_set = {docx_name, reg_name}
    checks.append((f"6 outputs == exactly the {len(expected_set)} deliverables",
                  staged == expected_set))
    checks.append(("7 question_index certified (G-QINDEX)", bool(qindex_ok)))

    fails = [name for name, ok in checks if not ok]
    return {'ok': not fails, 'checks': checks, 'fails': fails}


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

    files_extra = files_ok | {'stray_file.txt'}
    ld6, ex6 = fake_fs(files_extra)
    chk_6 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld6, exists=ex6)
    check('predelivery_check6_extra_file', chk_6['checks'][5][1] is False)

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
                                'subtopic_id': 'ex.a',
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
