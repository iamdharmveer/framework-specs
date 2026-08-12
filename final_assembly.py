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
def commit_registry(registry, pending, bp, N, *, paper_id, batches_completed,
                     axis2_window_counts, passage_present, di_present,
                     figural_present, concept_map,
                     passage_linked_qs=(), cloze_linked_qs=(),
                     di_manifest=None, fig_manifest=None, figure_specs=None,
                     framework_repo_commit=None, spec_source_report=None,
                     timestamp=None):
    """Registry update protocol (v2.0 GAP-03 + GAP-04 fix; v5.48.0 QINDEX-FK
    enforcement; v5.52 idempotency — see module docstring deviation 4).

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
        })
        reg['figural_manifests'] = fg

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
            "difficulty": concept_map[qn].get("difficulty")}
           for qn in sorted(concept_map, key=int)]
    _qindex_cert = {"blueprint_version": bp.get("blueprint_version"),
                    "subtopic_set_hash": hashlib.sha256("\n".join(sorted(
                        s.get("subtopic_id") or "" for s in bp.get("subtopic_list", [])
                    )).encode("utf-8")).hexdigest()[:16]}
    if framework_repo_commit is not None:
        _qindex_cert["framework_repo_commit"] = framework_repo_commit
    if spec_source_report is not None:
        _qindex_cert["spec_source_report"] = spec_source_report

    reg.setdefault('question_index', [])
    reg['question_index'] = [e for e in reg['question_index']
                             if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") != paper_id]
    reg['question_index'].append({"mock": N, "paper_id": paper_id,
                                  "qindex_cert": _qindex_cert, "questions": _qi})

    # ── Ledgers — idempotent (deviation 4) ───────────────────────────────────
    mocks_completed = reg.setdefault('mocks_completed', [])
    if N not in mocks_completed:
        mocks_completed.append(N)
    papers_completed = reg.setdefault('papers_completed', [])
    if paper_id not in papers_completed:
        papers_completed.append(paper_id)

    session_log = [e for e in reg.setdefault('session_log', [])
                   if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") != paper_id]
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

    return {'ok': True, 'fails': [], 'registry': reg, 'paper_id': paper_id}


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


def _commit_problems(reg, m):
    """G-COMMIT-COMPLETE per-mock cross-ledger check (GAP-2026-08-12-
    S13-COMMIT-COMPLETE). A mock is complete iff it has a session_log entry
    AND a question_index entry carrying a non-null paper_id."""
    sl_mocks = {e.get('mock') for e in reg.get('session_log', [])}
    qi_by_mock = {e.get('mock'): e for e in reg.get('question_index', [])}
    problems = []
    if m not in sl_mocks:
        problems.append('no session_log entry')
    qie = qi_by_mock.get(m)
    if qie is None:
        problems.append('no question_index entry')
    elif not qie.get('paper_id'):
        problems.append('question_index entry has no paper_id')
    return problems


def regcheck(registry, bp, *, N, concept_map=None, msq_meta=None):
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

    this_mock_problems = _commit_problems(reg, N)
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

    warnings = [f"mock {m}: {', '.join(_commit_problems(reg, m))}"
               for m in reg.get('mocks_completed', [])
               if m != N and _commit_problems(reg, m)]

    # options_by_q (v4.7, ND6) — derived from concept_map/msq_meta the caller
    # already read (with the SAME try/except fallback the spec-inline code
    # has around the answer_key.json load — see §13 in the spec).
    ocount = int(msq_meta.get("total_options", 4))
    obq = {q: (0 if concept_map[q].get("answer_type") == "numerical" else ocount)
           for q in concept_map}
    reg.setdefault('options_by_q', {})[str(N)] = obq

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
    except FileNotFoundError:
        staged = set()

    checks = []
    checks.append(("1 final docx in outputs", _exists(docx_path)))
    checks.append(("2 registry.json in outputs", _exists(reg_path)))
    checks.append(("3 registry schema complete", bool(regcheck_ok)))
    bad_ak = [f for f in staged if 'answer' in f.lower()]
    checks.append(("4 no answer-key file in outputs", len(bad_ak) == 0))
    internal = ['_answer_key.json', '_fig_manifest.json', '_batch_state.json', '_progress.json']
    leaked = [f for f in staged if any(m in f for m in internal)]
    checks.append(("5 no internal sidecars in outputs", len(leaked) == 0))
    expected_set = {docx_name, reg_name}
    if dossier_name and dossier_name in staged:
        expected_set.add(dossier_name)
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
    check('regcheck_section_names_written',
         rc_clean['registry']['section_names'] == ['Section A'])
    check('regcheck_does_not_mutate_input', clean_reg['section_names'] == [])

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

    # dossier-present-vs-absent variant of check 6
    files_dossier = files_ok | {'EX_M1_audit_dossier.json'}
    ld8, ex8 = fake_fs(files_dossier)
    chk_8 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json',
                                  dossier_name='EX_M1_audit_dossier.json',
                                  regcheck_ok=True, qindex_ok=True, listdir=ld8, exists=ex8)
    check('predelivery_check6_dossier_present_and_expected', chk_8['ok'] is True)

    # missing outputs_dir entirely does not crash (§ Angle 6 of the design's
    # adversarial review — first-run-before-makedirs case)
    def raising_listdir(_d):
        raise FileNotFoundError()
    check_raises_never('predelivery_missing_outputs_dir_does_not_crash',
                       lambda: predelivery_checklist('/does/not/exist',
                           docx_name='x', reg_name='y', regcheck_ok=True, qindex_ok=True,
                           listdir=raising_listdir, exists=lambda p: False)['ok'] is False)

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("final_assembly.py — Step 7 Final Assembly engine. Run with --self-test.")
