"""
paper_pipeline.py — shared plumbing for the test-generation pipeline (Step 6 blueprints and
Steps 7-11 generation). ONE implementation of each shared rule, imported by every step, so the
steps can never drift out of sync. All functions are pure (data in, data out); no file I/O, no
spec logic — only the resolution / naming / guard / numbering rules.

Concerns:
  1. paper_slug(paper_id)                 — the single filename-stem rule for every test type
  2. paper_prefix(paper_id)               — the scope-identity prefix (registry join / numbering)
  3. next_offset(registry, prefix)        — cross-slot numbering continuation (mock AND scoped)
  4. pick_blueprint(bps, ...)             — resolve WHICH blueprint to use (selector or docx)
  6. apply_mock_offset(blueprint, registry) — cross-slot mock renumbering (relabel post-pass)
  7. registry_guard(new, existing)        — refuse to overwrite a populated registry
  8. list_papers(blueprints, registry)    — TestList helper: inventory every paper + status
 10. canonical_answer / seal_key_commitments / verify_key_commitments / resolve_commitment
                                          — v5.39 KEY COMMITMENTS (GAP-2026-08-21-EXPLANATION-
                                            PROVENANCE): Step 7 commits a salted hash of every
                                            canonical answer into registry.key_commitments; Step 9
                                            re-derives, hashes its OWN answers and compares. Step 9
                                            never reads a plaintext key; a mismatch is resolved
                                            in-run by the Explain spec (§17 v1.37.0), never halted.
 12. dg_* (CLUSTER DG)                   — v5.71 DIFFICULTY-GATE RECORD SINGLE WRITER
                                            (GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER):
                                            registry['difficulty_gate'][paper_id] is written
                                            ONLY through dg_stamp_pending / dg_write_verdict /
                                            dg_add_rework_snapshot, every preflight opens with
                                            dg_preflight, every next-step string comes from
                                            dg_next_step, Step 11 decides via
                                            dg_deliver_decision, the footer from dg_footer_lines.
                                            v5.72 (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS):
                                            DG_DEFAULT_THRESHOLD 0.30 → 0.35; verdicts carry the
                                            gate's windows / measured_score_by_q / rework_directions
                                            and are stamped gate_rule='windows' (dg_is_windowed);
                                            a FAILED record from the retired band-equality rule is
                                            routed to TestExplain (re-judge), never repaired;
                                            §FOOTER-DG shows an ungated band as "(not gated)".
                                            v5.73 (2026-08-26, windows follow-up): a FRESH
                                            round-0 verdict retires a pre-repair stem snapshot
                                            whose rework set differs from the new verdict's
                                            (superseded_snapshots) — a stale snapshot would make
                                            §7A-R R3 accuse a correct repair and fail A-DGATE 5;
                                            kept when the set is identical or the round is carried.
 11. validate_semantic_object / semantic_objects_agree
                                          — v5.39 FIGURE SEMANTIC OBJECTS: every generated figure
                                            registers what it DEPICTS in machine-readable form
                                            (kind STRUCTURE carries a canonical SMILES). The rdkit-
                                            backed canonicaliser and the SMILES renderer live in
                                            corpus_io.py (Create route) and explain_engine.py
                                            (Explain route) and are INJECTED here — thin-core stays
                                            stdlib-only (CHECK AB).

Design invariants this enforces:
  * paper_id is globally unique and scope-qualified → no collision across types or slots.
  * paper_slug is deterministic AND unique AND match-reversible (docx name → blueprint paper).
  * numbering continues from the registry for every series type → slot-safe.
  * a populated registry can never be silently replaced by an empty one.
"""



# ── exceptions (clear, actionable stops) ─────────────────────────────────────────
class PickError(Exception):
    """Raised when the right blueprint cannot be unambiguously chosen."""


class RegistryWipeError(Exception):
    """Raised when an operation would overwrite a populated registry with an empty one."""


# ── 1. paper_slug — the ONE filename-stem rule (all four test types) ──────────────
def paper_slug(paper_id):
    """paper_id -> clean, zero-padded, single-underscore filename stem.

      MOCK:M01                     -> Mock01
      SUBJ:Physics:01              -> SUBJ_Physics_01
      TOPIC:Physics::Mechanics:01  -> TOPIC_Physics_Mechanics_01   (note: single underscore)
      SUBTOPIC:ST0042:01           -> SUBTOPIC_ST0042_01

    Deterministic (same paper_id -> same slug) and unique (paper_id is unique), so Steps 8-11 can
    match an uploaded docx back to its blueprint paper by comparing slugs.
    """
    if paper_id.startswith('MOCK:M'):
        return f"Mock{int(paper_id[len('MOCK:M'):]):02d}"
    prefix, num = paper_id.rsplit(':', 1)
    scopetag = prefix.replace('::', '_').replace(':', '_')      # '::' first, then remaining ':'
    return f"{scopetag}_{int(num):02d}"


def paper_prefix(paper_id):
    """The scope-identity prefix (everything but the paper number).
      MOCK:M07 -> 'MOCK'   ·   SUBJ:Physics:03 -> 'SUBJ:Physics'
      TOPIC:Physics::Mechanics:12 -> 'TOPIC:Physics::Mechanics'
    """
    if paper_id.startswith('MOCK:M'):
        return 'MOCK'
    return paper_id.rsplit(':', 1)[0]


def paper_number(paper_id):
    """The integer paper number within its series."""
    if paper_id.startswith('MOCK:M'):
        return int(paper_id[len('MOCK:M'):])
    return int(paper_id.rsplit(':', 1)[1])


# ── 3. cross-slot numbering continuation (mock AND scoped share this) ─────────────
def next_offset(registry, prefix):
    """Highest paper number already recorded for `prefix` in registry.papers_completed
    (falls back to the legacy mocks_completed for a mock-only prefix). New papers start at
    offset+1. Slot-safe: run again after 2 months and it continues, never restarts.

    prefix: 'MOCK' for mocks, else the scope prefix e.g. 'SUBJ:Physics'.
    """
    reg = registry or {}
    papers = list(reg.get('papers_completed', []))
    if prefix == 'MOCK' and not papers:
        # legacy registries recorded mocks in mocks_completed as bare ints or 'MOCK:M..'
        papers = [f"MOCK:M{int(m):02d}" if str(m).isdigit() else str(m)
                  for m in reg.get('mocks_completed', [])]
    nums = [paper_number(p) for p in papers if paper_prefix(p) == prefix]
    return max(nums) if nums else 0


# ── 4. pick_blueprint — resolve WHICH blueprint to use ───────────────────────────
def _bp_scope(bp):
    """(level, subject, topic) identity of a blueprint. Mock has no scope block."""
    sc = bp.get('scope')
    if not sc:
        return ('mock', None, None)
    return (sc.get('level'), sc.get('subject'), sc.get('topic'))


def _bp_slugs(bp):
    """Set of paper_slugs the blueprint contains (for docx matching)."""
    return {paper_slug(mk['paper_id']) for mk in bp.get('mocks', []) if mk.get('paper_id')}


def _bp_label(bp):
    """Human label for error messages."""
    lvl, sub, top = _bp_scope(bp)
    if lvl == 'mock':
        return 'mock'
    if lvl == 'subject':
        return f'subject "{sub}"'
    if lvl == 'topic':
        return f'topic "{sub}::{top}"'
    return f'{lvl} "{(bp.get("scope") or {}).get("scope_label", sub)}"'


def pick_blueprint(blueprints, level=None, scope_subject=None, scope_topic=None, docx_slug=None):
    """Choose the one blueprint to use from those present in the project.

    blueprints : list of loaded blueprint dicts.
    Resolution order:
      (a) docx_slug given (Steps 8-11)  -> the blueprint containing that paper_slug.
      (b) level/scope given (Step 7)    -> match by scope metadata (level 'mock' -> no scope block).
      (c) neither                       -> the single blueprint if exactly one; else PickError.
    Raises PickError with an actionable message on 0 / ambiguous / mismatch.
    """
    if not blueprints:
        raise PickError("No blueprint found — run MockBlueprint or ScopedBlueprint first.")

    # (a) uploaded docx drives it
    if docx_slug is not None:
        hits = [bp for bp in blueprints if docx_slug in _bp_slugs(bp)]
        if len(hits) == 1:
            chosen = hits[0]
            if level is not None and _bp_scope(chosen)[0] != level:      # optional cross-check
                raise PickError(
                    f"The uploaded paper is a {_bp_label(chosen)} paper, but you said --level {level}.")
            return chosen
        if not hits:
            raise PickError(
                f"The uploaded paper '{docx_slug}' matches no blueprint here — wrong file, "
                "or its blueprint isn't in the project.")
        raise PickError(f"'{docx_slug}' matches {len(hits)} blueprints (should be impossible; "
                        "remove duplicate blueprints).")

    # (b) explicit selector
    if level is not None:
        def matches(bp):
            lvl, sub, top = _bp_scope(bp)
            if lvl != level:
                return False
            if level in ('subject', 'topic') and sub != scope_subject:
                return False
            if level == 'topic' and top != scope_topic:
                return False
            return True
        hits = [bp for bp in blueprints if matches(bp)]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            want = level if level == 'mock' else f'{level} {scope_subject or ""}' \
                   + (f'::{scope_topic}' if scope_topic else '')
            raise PickError(f"No blueprint for {want.strip()} — run its blueprint step first.")
        raise PickError(f"{len(hits)} blueprints match that scope — remove the older one.")

    # (c) no selector: single-active default
    if len(blueprints) == 1:
        return blueprints[0]
    labels = ', '.join(sorted(_bp_label(bp) for bp in blueprints))
    raise PickError(f"Multiple blueprints present ({labels}). Add --level/--scope to pick one, "
                    "or keep only the one you're generating.")


# ── 6. apply_mock_offset — cross-slot mock renumbering (relabel post-pass) ────────
def apply_mock_offset(blueprint, registry):
    """Relabel a freshly-built MOCK blueprint so its papers CONTINUE from the registry instead
    of restarting at M01 — the mock analogue of the scoped `paper_start`. Pure post-pass on the
    finished dict: the allocation math (built on internal 1..N) is never touched, only the output
    labels. When there are no prior mocks (offset == 0) the blueprint is returned UNCHANGED, so an
    exam's first mock series is byte-identical to before.

    Offsets: mocks[].mock, mocks[].paper_id, and difficulty_schedule[].mock (the auditor looks up
    difficulty by mock number, so it must move too). Records blueprint['mock_offset'] for audit.
    Idempotent-guarded: refuses to double-apply (a blueprint already carrying mock_offset).
    """
    if blueprint.get('mock_offset'):
        raise ValueError("mock offset already applied to this blueprint (double-apply guard).")
    offset = next_offset(registry, 'MOCK')
    if not offset:
        return blueprint                                    # first series → byte-identical
    for mk in blueprint.get('mocks', []):
        mk['mock'] = mk['mock'] + offset
        mk['paper_id'] = f"MOCK:M{mk['mock']:02d}"
    for d in blueprint.get('difficulty_schedule', []):
        d['mock'] = d['mock'] + offset
    blueprint['mock_offset'] = offset
    return blueprint


# ── 7. registry_guard — never wipe a populated registry ──────────────────────────
def registry_guard(new_registry, existing_registry):
    """Return new_registry, unless it would overwrite a populated existing registry with an
    empty one — then raise RegistryWipeError. This makes the cross-slot history impossible to
    destroy by accident (e.g. re-running MockBlueprint and using its blank template)."""
    ex = existing_registry or {}
    nw = new_registry or {}
    ex_has = bool(ex.get('papers_completed') or ex.get('mocks_completed'))
    nw_has = bool(nw.get('papers_completed') or nw.get('mocks_completed'))
    if ex_has and not nw_has:
        raise RegistryWipeError(
            "Refusing to overwrite the populated registry with an empty one. The registry is the "
            "permanent record (dedup + paper ledger) — keep the existing "
            "[ExamCode]_registry.json; do not replace it with a blank template.")
    return new_registry


# ── 8. list_papers — TestList helper: inventory every paper across blueprints + registry ──
def list_papers(blueprints, registry=None):
    """Build a flat, exam-agnostic inventory of every paper defined across the given
    blueprints, cross-referenced against the registry's completion ledger. Powers the
    TestList helper trigger — a non-technical operator's "what exists, what's done" view
    across mock AND every scoped tier, without reading raw JSON.

    Returns a list of dicts, one per paper (blueprints in the order given, each
    blueprint's mocks[] in its original order):
      {
        'paper_id':   the paper's identity string (e.g. 'MOCK:M03', 'SUBJ:Physics:01')
        'paper_slug': paper_slug(paper_id) — the filename stem Steps 7-11 use
        'level':      'mock' | 'subject' | 'topic' | <scoped level>
        'label':      human label, e.g. 'mock', 'subject "Physics"', 'topic "Physics::Mechanics"'
        'number':     the paper's number within its own series (paper_number(paper_id))
        'completed':  True if paper_id is in registry.papers_completed (or, for a mock,
                      the legacy registry.mocks_completed), else False
      }
    Pure (no file I/O). registry=None means nothing is marked complete (e.g. before any
    generation has run).
    """
    reg = registry or {}
    completed_ids = set(reg.get('papers_completed', []))
    # legacy fallback: pre-C1 registries recorded mocks in mocks_completed as bare ints
    # or 'MOCK:M..' strings — same normalisation next_offset() applies.
    for m in reg.get('mocks_completed', []):
        completed_ids.add(f"MOCK:M{int(m):02d}" if str(m).isdigit() else str(m))

    out = []
    for bp in blueprints:
        level, _, _ = _bp_scope(bp)
        label = _bp_label(bp)
        for mk in bp.get('mocks', []):
            pid = mk.get('paper_id')
            if not pid:
                continue
            out.append({
                'paper_id': pid,
                'paper_slug': paper_slug(pid),
                'level': level,
                'label': label,
                'number': paper_number(pid),
                'completed': pid in completed_ids,
            })
    return out


# ── self-test ────────────────────────────────────────────────────────────────────
def _self_test():
    p, f = 0, 0

    _failed = []

    def ck(name, cond):
        nonlocal p, f
        if cond:
            p += 1
        else:
            f += 1
            _failed.append(name)

    def ck_call(name, fn):
        """v5.38 — evaluate a fixture that MAY RAISE and count a raise as a
        FAILURE. `ck(name, expr)` receives an ALREADY-EVALUATED condition, so an
        exception inside expr propagates and ABORTS the whole self-test — every
        later fixture silently never runs. That is a hollow branch in the test
        harness itself, which is the defect class this corpus keeps closing."""
        try:
            ck(name, bool(fn()))
        except Exception as _e:
            ck(f'{name} [raised {type(_e).__name__}]', False)
            print(f"  FAIL {name}")

    # slug rule, all four types + zero-pad + single underscore
    ck('slug_mock', paper_slug('MOCK:M01') == 'Mock01')
    ck('slug_mock_pad', paper_slug('MOCK:M07') == 'Mock07' and paper_slug('MOCK:M10') == 'Mock10')
    ck('slug_subject', paper_slug('SUBJ:Physics:01') == 'SUBJ_Physics_01')
    ck('slug_topic_single_us', paper_slug('TOPIC:Physics::Mechanics:01') == 'TOPIC_Physics_Mechanics_01')
    ck('slug_subtopic', paper_slug('SUBTOPIC:ST0042:03') == 'SUBTOPIC_ST0042_03')
    # prefix / number
    ck('prefix_mock', paper_prefix('MOCK:M05') == 'MOCK' and paper_number('MOCK:M05') == 5)
    ck('prefix_topic', paper_prefix('TOPIC:Physics::Mechanics:12') == 'TOPIC:Physics::Mechanics'
       and paper_number('TOPIC:Physics::Mechanics:12') == 12)
    # numbering continuation (the slot-safety core)
    reg = {'papers_completed': ['MOCK:M01', 'MOCK:M10', 'SUBJ:Physics:15', 'SUBJ:Physics:03']}
    ck('offset_mock', next_offset(reg, 'MOCK') == 10)
    ck('offset_subject', next_offset(reg, 'SUBJ:Physics') == 15)
    ck('offset_fresh', next_offset({}, 'MOCK') == 0 and next_offset(None, 'SUBJ:Chemistry') == 0)
    ck('offset_legacy', next_offset({'mocks_completed': [1, 2, 3]}, 'MOCK') == 3)
    # registry guard
    try:
        registry_guard({'papers_completed': []}, {'papers_completed': ['MOCK:M01']})
        ck('guard_blocks_wipe', False)
    except RegistryWipeError:
        ck('guard_blocks_wipe', True)
    ck('guard_allows_fresh', registry_guard({'papers_completed': []}, {}) == {'papers_completed': []})
    ck('guard_allows_append',
       registry_guard({'papers_completed': ['a', 'b']}, {'papers_completed': ['a']})
       == {'papers_completed': ['a', 'b']})

    # apply_mock_offset — byte-identity at 0, continuation at >0, double-apply guard
    import copy
    fresh_bp = {'mocks': [{'mock': i, 'paper_id': f'MOCK:M{i:02d}', 'sections': [i]} for i in range(1, 4)],
                'difficulty_schedule': [{'mock': i, 'simple': i} for i in range(1, 4)]}
    bp0 = apply_mock_offset(copy.deepcopy(fresh_bp), {'papers_completed': []})
    ck('offset0_byte_identical', bp0 == fresh_bp and 'mock_offset' not in bp0)
    bp10 = apply_mock_offset(copy.deepcopy(fresh_bp),
                             {'papers_completed': [f'MOCK:M{i:02d}' for i in range(1, 11)]})
    ck('offset10_mocks', [mk['mock'] for mk in bp10['mocks']] == [11, 12, 13])
    ck('offset10_paper_ids', [mk['paper_id'] for mk in bp10['mocks']]
       == ['MOCK:M11', 'MOCK:M12', 'MOCK:M13'])
    ck('offset10_difficulty', [d['mock'] for d in bp10['difficulty_schedule']] == [11, 12, 13])
    ck('offset10_sections_untouched', [mk['sections'] for mk in bp10['mocks']] == [[1], [2], [3]])
    ck('offset10_records', bp10['mock_offset'] == 10)
    try:
        apply_mock_offset(bp10, {'papers_completed': ['MOCK:M40']})
        ck('offset_double_guard', False)
    except ValueError:
        ck('offset_double_guard', True)

    # pick_blueprint — build sample blueprints
    mock_bp = {'mocks': [{'paper_id': 'MOCK:M01'}, {'paper_id': 'MOCK:M02'}]}
    phys_bp = {'scope': {'level': 'subject', 'subject': 'Physics'},
               'mocks': [{'paper_id': 'SUBJ:Physics:01'}]}
    mech_bp = {'scope': {'level': 'topic', 'subject': 'Physics', 'topic': 'Mechanics'},
               'mocks': [{'paper_id': 'TOPIC:Physics::Mechanics:01'}]}
    ck('pick_single', pick_blueprint([phys_bp]) is phys_bp)
    ck('pick_by_docx', pick_blueprint([mock_bp, phys_bp, mech_bp],
                                      docx_slug='TOPIC_Physics_Mechanics_01') is mech_bp)
    ck('pick_by_selector', pick_blueprint([mock_bp, phys_bp, mech_bp],
                                          level='subject', scope_subject='Physics') is phys_bp)
    ck('pick_mock_selector', pick_blueprint([mock_bp, phys_bp], level='mock') is mock_bp)
    for args, exc in [
        (dict(blueprints=[]), PickError),                                   # 0 blueprints
        (dict(blueprints=[mock_bp, phys_bp]), PickError),                   # ambiguous, no selector
        (dict(blueprints=[phys_bp], docx_slug='SUBJ_Chemistry_01'), PickError),  # docx no match
        (dict(blueprints=[phys_bp], level='topic', scope_subject='X', scope_topic='Y'), PickError),
    ]:
        try:
            pick_blueprint(**args)
            ck(f'pick_raises_{exc.__name__}', False)
        except PickError:
            ck('pick_raises', True)
    # docx/selector conflict cross-check
    try:
        pick_blueprint([mech_bp], docx_slug='TOPIC_Physics_Mechanics_01', level='subject')
        ck('pick_conflict', False)
    except PickError:
        ck('pick_conflict', True)

    # list_papers — TestList helper
    lp_mock_bp = {'mocks': [{'mock': 1, 'paper_id': 'MOCK:M01'}, {'mock': 2, 'paper_id': 'MOCK:M02'}]}
    lp_phys_bp = {'scope': {'level': 'subject', 'subject': 'Physics'},
                  'mocks': [{'mock': 1, 'paper_id': 'SUBJ:Physics:01'}]}
    lp_reg = {'papers_completed': ['MOCK:M01']}
    inv = list_papers([lp_mock_bp, lp_phys_bp], lp_reg)
    ck('list_papers_count', len(inv) == 3)
    ck('list_papers_slugs', {p['paper_slug'] for p in inv} == {'Mock01', 'Mock02', 'SUBJ_Physics_01'})
    ck('list_papers_levels', {p['paper_id']: p['level'] for p in inv}
       == {'MOCK:M01': 'mock', 'MOCK:M02': 'mock', 'SUBJ:Physics:01': 'subject'})
    ck('list_papers_completed', {p['paper_id']: p['completed'] for p in inv}
       == {'MOCK:M01': True, 'MOCK:M02': False, 'SUBJ:Physics:01': False})
    ck('list_papers_numbers', {p['paper_id']: p['number'] for p in inv}
       == {'MOCK:M01': 1, 'MOCK:M02': 2, 'SUBJ:Physics:01': 1})
    # legacy mocks_completed fallback
    inv_legacy = list_papers([lp_mock_bp], {'mocks_completed': [1]})
    ck('list_papers_legacy_completed', next(p['completed'] for p in inv_legacy if p['paper_id'] == 'MOCK:M01'))
    # no registry -> nothing completed
    inv_none = list_papers([lp_mock_bp])
    ck('list_papers_no_registry', all(not p['completed'] for p in inv_none))


    # ── v5.37 GAP-2026-08-03-LABELFMT — OPTION LABEL RESOLUTION ────────────────
    def _render(tpl, i):
        _rom = ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x')
        return (tpl.replace('{i}', str(i))
                   .replace('{alpha_upper}', chr(64 + i)).replace('{alpha_lower}', chr(96 + i))
                   .replace('{roman_upper}', _rom[i - 1].upper())
                   .replace('{roman_lower}', _rom[i - 1])
                   .replace('{text}', 'X'))

    # THE DEFECT THIS CLOSES: before v5.37, 'i/ii/iii/iv' rendered (a)(b)(c)(d)
    # because Step 7 tested the leading token's CASING and had no roman branch,
    # while the auditor classified the family as 'roman' — A-OPTLABEL then FAILED every
    # question, exit 1, MANDATE D blocked delivery, and no CP repair could fix a
    # paper that matched Step 7's own contract. Measured end-to-end.
    ck_call('LABELFMT-roman-lower-renders-roman',
            lambda: _render(resolve_option_label('i/ii/iii/iv')[0], 1).startswith('i.'))
    ck_call('LABELFMT-roman-upper-renders-roman',
            lambda: _render(resolve_option_label('I/II/III/IV')[0], 2).startswith('II.'))
    ck_call('LABELFMT-roman-bracketed-preserved',
            lambda: _render(resolve_option_label('(i)/(ii)/(iii)/(iv)')[0], 2).startswith('(ii)'))

    # UNCHANGED FOR EVERY EXISTING NOTATION — ~200 exams depend on this.
    ck_call('LABELFMT-numeric-unchanged',
            lambda: _render(resolve_option_label('1/2/3/4')[0], 3).startswith('3.'))
    ck_call('LABELFMT-alpha-unchanged',
            lambda: _render(resolve_option_label('A/B/C/D')[0], 2).startswith('B.'))
    ck_call('LABELFMT-bracketing-preserved',
            lambda: _render(resolve_option_label('(1)/(2)/(3)/(4)')[0], 1).startswith('(1)'))
    ck_call('LABELFMT-empty-defaults-numeric',
            lambda: resolve_option_label('')[0] == '{i}.  {text}')

    # THE SYNC INVARIANT: Step 7's render family must equal the auditor's classification
    # for EVERY notation that resolves, or the pair can silently drift again.
    _SUPPORTED = ('1/2/3/4', 'A/B/C/D', 'a/b/c/d', 'i/ii/iii/iv', 'I/II/III/IV',
                  '(1)/(2)/(3)/(4)', '(A)/(B)/(C)/(D)', '(i)/(ii)/(iii)/(iv)',
                  '1)/2)/3)/4)', '')
    ck_call('LABELFMT-render-family-matches-audit-family-for-all-supported',
            lambda: all(resolve_option_label(_x)[1] == option_label_family(_x)
                        for _x in _SUPPORTED))

    # AMBIGUITY IS REFUSED, NEVER GUESSED. 'i/j/k/l' renders alpha but classifies
    # roman; '[A]/...' renders alpha but classifies num (the classifier strips
    # ()., not []). Either would reproduce the defect under a new notation.
    for _amb in ('i/j/k/l', '[A]/[B]/[C]/[D]'):
        try:
            resolve_option_label(_amb)
            ck(f'LABELFMT-ambiguous-{_amb}-refused', False)
        except LabelFormatError:
            ck(f'LABELFMT-ambiguous-{_amb}-refused', True)

    # UNRENDERABLE NOTATION HARD-STOPS rather than degrading. Pre-v5.37,
    # '(1)/(2)/(3)/(4)' became the template VERBATIM (no {text} => no substitution)
    # and '\u2460/...' silently became '1.' (Python .isdigit() is True for circled
    # digits). Guessing contradicts pick_blueprint/derive_nat_grading posture.
    for _bad in ('\u2460/\u2461/\u2462/\u2463', 'nonsense', 'xx/yy/zz'):
        try:
            resolve_option_label(_bad)
            ck(f'LABELFMT-unrenderable-{_bad[:12]}-refused', False)
        except LabelFormatError:
            ck(f'LABELFMT-unrenderable-{_bad[:12]}-refused', True)

    # NEVER emits a template without a substitution point — the pre-v5.37 failure.
    ck_call('LABELFMT-template-always-has-text-placeholder',
            lambda: all('{text}' in resolve_option_label(_x)[0] for _x in _SUPPORTED))

    # ── GAP-2026-08-10-QINDEX-FK-ENFORCEMENT — the four §9 helpers ────────────
    # These shipped with NO fixture at all: the release's own note recorded
    # "51/51 PASS", the pre-change count, so four new functions gating three
    # steps were added without moving the suite by one. The behavioural runs
    # against the defective corpus were done by hand and cannot re-run. What
    # follows is those runs, made permanent.
    _QBP = {'total_questions': 2, 'mocks': [{'mock': 1, 'paper_id': 'MOCK:M01'}],
            'subtopic_list': [{'subtopic_id': 'PHY.MECH.NEWTON'},
                              {'subtopic_id': 'PHY.MECH.WORK'}],
            'difficulty_labels': ['Easy', 'Medium', 'Hard']}
    _QCLEAN = [{'q': 1, 'subtopic_id': 'PHY.MECH.NEWTON', 'difficulty': 'Easy'},
               {'q': 2, 'subtopic_id': 'PHY.MECH.WORK', 'difficulty': 'Hard'}]

    def _qreg(qs):
        return {'question_index': [{'paper_id': 'MOCK:M01', 'questions': qs}]}

    def _qok(qs):
        return validate_question_index(_qreg(qs), _QBP, mock_n=1)[0]

    ck('QINDEX-clean-certifies', _qok(_QCLEAN))
    # THE DEFECT: three reference sessions persisted a PARAPHRASED subtopic_id
    # (the blueprint string retyped rather than copied) and logged clean audits.
    ck('QINDEX-invented-id-fails',
       not _qok([_QCLEAN[0], {'q': 2, 'subtopic_id': 'Physics.Mechanics.Work',
                              'difficulty': 'Hard'}]))
    ck_call('QINDEX-invented-id-names-the-question',
            lambda: validate_question_index(
                _qreg([_QCLEAN[0], {'q': 2, 'subtopic_id': 'Physics.Mechanics.Work',
                                    'difficulty': 'Hard'}]),
                _QBP, mock_n=1)[1]['bad_ids'] == {2: 'Physics.Mechanics.Work'})
    ck('QINDEX-short-count-fails', not _qok(_QCLEAN[:1]))
    ck('QINDEX-duplicate-q-fails',
       not _qok([_QCLEAN[0], {'q': 1, 'subtopic_id': 'PHY.MECH.WORK',
                              'difficulty': 'Hard'}]))
    ck('QINDEX-bad-difficulty-fails',
       not _qok([_QCLEAN[0], {'q': 2, 'subtopic_id': 'PHY.MECH.WORK',
                              'difficulty': 'Tough'}]))

    # ── GAP-2026-08-12-QINDEX-QUOTA-ENFORCEMENT — check 6 ────────────────────
    # THE DEFECT THIS CLOSES: checks 1-5 (above) were moved into the engine at
    # GAP-2026-08-10-QINDEX-FK-ENFORCEMENT; the exact-quota check (schedule-first
    # assignment, Contract_QuestionMetadataIndex v1.0) was left session-executed-
    # only. A session can satisfy checks 1-5 with a canonical-labelled but wrong-
    # QUOTA distribution (e.g. a free assessment never constrained to the
    # schedule) and still log a clean, exit-code-durable audit. Ships WITH a
    # fixture from day one, unlike the four helpers this extends (shipped with
    # none, per the note above).
    _QBP6 = dict(_QBP, difficulty_schedule=[{'mock': 1, 'simple': 1, 'hard': 1}])
    ck('QINDEX-quota-exact-match-certifies',
       validate_question_index(_qreg(_QCLEAN), _QBP6, mock_n=1)[0])
    ck('QINDEX-quota-mismatch-fails',
       not validate_question_index(
           _qreg([{'q': 1, 'subtopic_id': 'PHY.MECH.NEWTON', 'difficulty': 'Medium'},
                  {'q': 2, 'subtopic_id': 'PHY.MECH.WORK', 'difficulty': 'Medium'}]),
           _QBP6, mock_n=1)[0])
    ck_call('QINDEX-quota-mismatch-names-got-and-want',
            lambda: 'schedule quota' in validate_question_index(
                _qreg([{'q': 1, 'subtopic_id': 'PHY.MECH.NEWTON', 'difficulty': 'Medium'},
                       {'q': 2, 'subtopic_id': 'PHY.MECH.WORK', 'difficulty': 'Medium'}]),
                _QBP6, mock_n=1)[1]['fails'][0])
    ck('QINDEX-quota-dormant-when-exam-has-no-schedule',
       # _QBP (no difficulty_schedule key) must still certify a clean set —
       # check 6 must never be invented for an exam that never declared one.
       _qok(_QCLEAN))
    ck('QINDEX-quota-fails-when-schedule-exists-but-not-for-this-mock',
       not validate_question_index(_qreg(_QCLEAN),
           dict(_QBP, difficulty_schedule=[{'mock': 99, 'simple': 2}]), mock_n=1)[0])

    # the 4th defective mock: a later registry write dropped the whole entry
    ck_call('QINDEX-lost-entry-fails-and-flags-entry_missing',
            lambda: (lambda r: r[0] is False and r[1]['entry_missing'] is True)(
                validate_question_index({'question_index': []}, _QBP, mock_n=1)))
    ck('QINDEX-needs-a-paper-selector',
       not validate_question_index(_qreg(_QCLEAN), _QBP)[0])

    # registry_integrity_check — ledger claims complete, index data gone (Class A)
    ck_call('QINDEX-integrity-names-the-lost-paper',
            lambda: registry_integrity_check(
                {'papers_completed': ['MOCK:M01', 'MOCK:M12'],
                 'question_index': [{'paper_id': 'MOCK:M01', 'questions': []}]})
            == (False, {'missing_index': ['MOCK:M12'], 'orphan_index': []}))
    ck_call('QINDEX-integrity-orphan-is-advisory-not-fatal',
            lambda: (lambda r: r[0] is True and r[1]['orphan_index'] == ['MOCK:M09'])(
                registry_integrity_check(
                    {'papers_completed': [],
                     'question_index': [{'paper_id': 'MOCK:M09', 'questions': []}]})))
    ck_call('QINDEX-integrity-legacy-mocks_completed-counted',
            lambda: registry_integrity_check(
                {'mocks_completed': [3], 'question_index': []})[1]['missing_index']
            == ['MOCK:M03'])

    # classify_unresolved — W1 deterministic / D human / W2 confirm
    _CBP = {'subtopic_list': [{'subtopic_id': 'PHY.MECH.WORK'},
                              {'subtopic_id': 'CHEM.THERMO.WORK'},
                              {'subtopic_id': 'PHY.MECH.NEWTON'}]}
    _cls = classify_unresolved({1: 'Physics.Mechanics.NEWTON', 2: 'X.Y.WORK',
                                3: 'PHY.MECH.ENERGYY'}, _CBP)
    ck('QINDEX-classify-W1-unique-leaf',
       _cls[1]['cls'] == 'W1' and _cls[1]['targets'] == ['PHY.MECH.NEWTON'])
    ck('QINDEX-classify-D-ambiguous-leaf',
       _cls[2]['cls'] == 'D' and len(_cls[2]['targets']) == 2)
    ck('QINDEX-classify-W2-reworded-leaf', _cls[3]['cls'] == 'W2')

    # subtopic_set_hash — a SET stamp: order must not matter, membership must
    ck('QINDEX-hash-order-independent',
       subtopic_set_hash(_QBP)
       == subtopic_set_hash({'subtopic_list': list(reversed(_QBP['subtopic_list']))}))
    ck('QINDEX-hash-changes-on-membership',
       subtopic_set_hash(_QBP)
       != subtopic_set_hash({'subtopic_list': [{'subtopic_id': 'PHY.MECH.NEWTON'}]}))

    # QINDEX PARITY lives in audit_canonical's suite ONLY, not here. The pair
    # gate_qindex <-> validate_question_index must be asserted equal, but
    # paper_pipeline is a THIN CORE (CHECK AB): stdlib imports only, so it may
    # never import the auditor. This is the same asymmetry LABEL-PARITY already
    # uses — the auditor imports the core, never the reverse. One red suite on
    # divergence is the requirement; two would cost thin-core purity.

    # ── v5.39 KEY COMMITMENTS + SEMANTIC OBJECTS ─────────────────────────────
    ck('KEY-canonical-mcq', canonical_answer('mcq', 2) == '2')
    ck('KEY-canonical-msq-sorted', canonical_answer('msq', [3, 1]) == '1,3'
       and canonical_answer('msq', {2, 3}) == '2,3')
    ck('KEY-canonical-nat-string', canonical_answer('nat', '3.09') == '3.09'
       and canonical_answer('nat', '0') == '0')
    _kc = seal_key_commitments('MOCK:M01', {1: '2', 47: '2', 45: '3.09'},
                               salts={1: 'aa', 47: 'bb', 45: 'cc'})
    ck('KEY-seal-shape', _kc['schema'] == 1 and set(_kc['entries']) == {'1', '47', '45'}
       and len(_kc['entries']['1']['h']) == 64)
    ck('KEY-seal-deterministic', _kc == seal_key_commitments('MOCK:M01', {1: '2', 47: '2', 45: '3.09'},
                                                             salts={1: 'aa', 47: 'bb', 45: 'cc'}))
    ck('KEY-seal-salted', seal_key_commitments('MOCK:M01', {1: '2'})['entries']['1']['h']
       != seal_key_commitments('MOCK:M01', {1: '2'})['entries']['1']['h'])
    _vr = verify_key_commitments(_kc, {1: '2', 47: '1', 45: '3.09', 60: '18'}, 'MOCK:M01')
    ck('KEY-verify-split', _vr == {'matched': [1, 45], 'mismatched': [47], 'missing': [60]})
    ck('KEY-verify-paper-bound', verify_key_commitments(_kc, {1: '2'}, 'MOCK:M02')['mismatched'] == [1])
    ck('KEY-resolve-probe', resolve_commitment(_kc, 47, ['1', '2', '3', '4'], 'MOCK:M01') == '2'
       and resolve_commitment(_kc, 47, ['1', '3'], 'MOCK:M01') is None
       and resolve_commitment(_kc, 99, ['1'], 'MOCK:M01') is None)
    ck('KEY-verify-empty', verify_key_commitments({}, {1: '2'}, 'MOCK:M01') ==
       {'matched': [], 'mismatched': [], 'missing': [1]})
    _so = {'role': 'problem', 'kind': 'STRUCTURE', 'name': 'salicylic acid',
           'canonical': 'OC(=O)c1ccccc1O', 'descriptor': {'acidic_sites': 2}}
    def ck_raises(name, fn):
        try:
            fn(); ck(name, False)
        except ValueError:
            ck(name, True)
    ck('SEM-valid', validate_semantic_object(_so))
    ck_raises('SEM-structure-needs-canonical',
            lambda: validate_semantic_object(dict(_so, canonical='')))
    ck_raises('SEM-bad-role', lambda: validate_semantic_object(dict(_so, role='figure 1')))
    ck_raises('SEM-bad-kind', lambda: validate_semantic_object(dict(_so, kind='PICTURE')))
    ck('SEM-option-role', validate_semantic_object(dict(_so, role='option:3')))
    ck('SEM-agree-string', semantic_objects_agree(_so, dict(_so))[0]
       and not semantic_objects_agree(_so, dict(_so, canonical='O=C(C)c1ccccc1O'))[0])
    _fake = lambda sm: ({'OC(=O)c1ccccc1O': 'X', 'Oc1ccccc1C(O)=O': 'X',
                         'O=C(C)c1ccccc1O': 'Y'}.get(sm), 'ok')
    ck('SEM-agree-injected-canon',
       semantic_objects_agree(_so, dict(_so, canonical='Oc1ccccc1C(O)=O'), canon=_fake)[0]
       and not semantic_objects_agree(_so, dict(_so, canonical='O=C(C)c1ccccc1O'), canon=_fake)[0])
    ck('SEM-agree-descriptor', semantic_objects_agree(
        {'kind': 'NEWMAN', 'descriptor': {'dihedral': 0}}, {'kind': 'NEWMAN', 'descriptor': {'dihedral': 0}})[0]
       and not semantic_objects_agree({'kind': 'NEWMAN', 'descriptor': {'dihedral': 0}},
                                      {'kind': 'NEWMAN', 'descriptor': {'dihedral': 60}})[0])

    # ══════════════════════════════════════════════════════════════════════
    # CLUSTER DG — v5.71 GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER
    #   Every fixture below fails on the defect it was written for; the mutation
    #   auditor requires it. DG-REFUSE-FAILED-1 is the exact incident.
    def ck_dg_raises(name, fn):
        try:
            fn(); ck(name, False)
        except DGIllegalState:
            ck(name, True)
        except Exception as _e:                                    # noqa: BLE001
            ck(f'{name} [raised {type(_e).__name__}]', False)
    # legal table: generated, six states at max_rounds=1, E18 shape at 2
    ck('DG-LEGAL-SIX', sorted(DG_LEGAL_STATES) == [('DISCLOSED', 1), ('DORMANT', 0),
       ('FAILED', 0), ('PASSED', 0), ('PASSED', 1), ('PENDING', 0)])
    ck('DG-LEGAL-E18-generated', sorted(_dg_legal_states(2)) == [('DISCLOSED', 2),
       ('DORMANT', 0), ('FAILED', 0), ('FAILED', 1), ('PASSED', 0), ('PASSED', 1),
       ('PASSED', 2), ('PENDING', 0)])
    # (bc constant parity is asserted in audit_canonical --self-test, which imports
    #  both engines; the thin core may not import blueprint_core — CHECK AB.)
    # the three writers round-trip every legal pair
    _R = {}
    ck('DG-STAMP-mock-PENDING', dg_state(dg_stamp_pending(_R, 'MOCK:M01')) == ('PENDING', 0))
    ck('DG-STAMP-scoped-DORMANT', dg_state(dg_stamp_pending(_R, 'SUBJ:Physics:01')) == ('DORMANT', 0)
       and _R['difficulty_gate']['SUBJ:Physics:01']['dormant_reason'] == 'scoped_paper')
    ck('DG-SCOPED-DELIVERABLE', dg_deliver_decision(_R, 'SUBJ:Physics:01', 1, mock=False)['deliver'])
    ck('DG-ISOLATION', dg_read(_R, 'MOCK:M01') == {'schema': DG_SCHEMA, 'status': 'PENDING',
       'threshold': DG_DEFAULT_THRESHOLD, 'repair_rounds_used': 0})
    # GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS: verdicts carry the gate's windows; a
    # FAILED verdict needs windows + a direction for every rework q.
    _W = [None, [2, 6], [5, None]]
    _bands = {'Easy': {'total': 6, 'gated': False, 'window': None, 'assessed': 0, 'agree': 0,
                       'disagree': 0, 'allowed': 2, 'over_limit': False},
              'Hard': {'total': 6, 'gated': True, 'window': [5, None], 'assessed': 6, 'agree': 1,
                       'disagree': 5, 'allowed': 2, 'over_limit': True}}
    _DIRS = {4: 'harder', 1: 'easier'}
    ck('DG-LEGAL-FAILED-0', dg_state(dg_write_verdict(_R, 'MOCK:M01', status='FAILED', rounds=0,
       bands=_bands, measured_by_q={1: 'Easy', 2: None}, rework_qs=[4, 1],
       scores_by_q={1: 7, 2: None, 4: '3'}, rework_directions=_DIRS, windows=_W)) == ('FAILED', 0)
       and _R['difficulty_gate']['MOCK:M01']['rework_qs'] == [1, 4]
       and _R['difficulty_gate']['MOCK:M01']['measured_by_q'] == {'1': 'Easy'}
       and _R['difficulty_gate']['MOCK:M01']['measured_score_by_q'] == {'1': 7, '4': 3}
       and _R['difficulty_gate']['MOCK:M01']['rework_directions'] == {'4': 'harder', '1': 'easier'}
       and _R['difficulty_gate']['MOCK:M01']['windows'] == _W
       and _R['difficulty_gate']['MOCK:M01']['gate_rule'] == DG_RULE_WINDOWS
       and dg_is_windowed(dg_read(_R, 'MOCK:M01')))
    ck_dg_raises('DG-WIN-REFUSE-FAILED-no-windows', lambda: dg_write_verdict({}, 'MOCK:M09', status='FAILED',
                 rounds=0, bands=_bands, rework_qs=[4], rework_directions={4: 'harder'}))
    ck_dg_raises('DG-WIN-REFUSE-FAILED-no-directions', lambda: dg_write_verdict({}, 'MOCK:M09', status='FAILED',
                 rounds=0, bands=_bands, rework_qs=[4], windows=_W))
    ck_dg_raises('DG-WIN-REFUSE-partial-directions', lambda: dg_write_verdict({}, 'MOCK:M09', status='FAILED',
                 rounds=0, bands=_bands, rework_qs=[4, 1], rework_directions={4: 'harder'}, windows=_W))
    ck_dg_raises('DG-WIN-REFUSE-bad-direction', lambda: dg_write_verdict({}, 'MOCK:M09', status='FAILED',
                 rounds=0, bands=_bands, rework_qs=[4], rework_directions={4: 'up'}, windows=_W))
    ck_dg_raises('DG-WIN-REFUSE-bad-windows-shape', lambda: dg_write_verdict({}, 'MOCK:M09', status='PASSED',
                 rounds=0, windows=[None, [2, 6]]))
    ck_dg_raises('DG-WIN-REFUSE-bad-window-entry', lambda: dg_write_verdict({}, 'MOCK:M09', status='PASSED',
                 rounds=0, windows=[None, 5, [5, None]]))
    ck_dg_raises('DG-WIN-REFUSE-non-int-score', lambda: dg_write_verdict({}, 'MOCK:M09', status='PASSED',
                 rounds=0, windows=_W, scores_by_q={1: 'x'}))
    ck_dg_raises('DG-WIN-REFUSE-fractional-score', lambda: dg_write_verdict({}, 'MOCK:M09', status='PASSED',
                 rounds=0, windows=_W, scores_by_q={1: 5.5}))
    ck('DG-WIN-score-coercion', dg_write_verdict({}, 'MOCK:M09', status='PASSED', rounds=0, windows=_W,
       scores_by_q={1: 5.0, 2: '4', 3: None, 4: True})['measured_score_by_q'] == {'1': 5, '2': 4})
    ck('DG-WIN-CONSTANTS-pinned', DG_RULE_WINDOWS == 'windows'          # literal already on disk in every windowed record
       and abs(DG_DEFAULT_THRESHOLD - 0.35) < 1e-12)                       # operator decision 2026-08-25
    ck('DG-WIN-threshold-recorded', dg_write_verdict({}, 'MOCK:M09', status='PASSED', rounds=0, windows=_W,
       threshold=0.4)['threshold'] == 0.4
       and dg_write_verdict({}, 'MOCK:M09', status='PASSED', rounds=0, windows=_W)['threshold'] == DG_DEFAULT_THRESHOLD)
    ck('DG-WIN-PASSED-stamped', dg_is_windowed(dg_write_verdict({}, 'MOCK:M09', status='PASSED', rounds=0, windows=_W))
       and not dg_is_windowed(dg_write_verdict({}, 'MOCK:M09', status='PASSED', rounds=0))
       and not dg_is_windowed(None) and not dg_is_windowed({'status': 'PENDING'}))
    # a FAILED record from the retired rule: re-judge, never repair, never deliver
    _OLD = {'difficulty_gate': {'MOCK:M07': {'schema': 2, 'status': 'FAILED', 'repair_rounds_used': 0,
                                            'rework_qs': [2, 5], 'bands': {'Hard': {'total': 2}}}}}
    ck('DG-WIN-OLD-FAILED-next-is-explain', dg_next_step(_OLD, 'MOCK:M07', 7, mock=True).startswith('MockExplain M7')
       and 'CreateRepair' not in dg_next_step(_OLD, 'MOCK:M07', 7, mock=True)
       and dg_deliver_decision(_OLD, 'MOCK:M07', 7, mock=True)['deliver'] is False
       and 'retired' in dg_deliver_decision(_OLD, 'MOCK:M07', 7, mock=True)['reason'])
    ck_dg_raises('DG-WIN-OLD-FAILED-snapshot-refused', lambda: dg_add_rework_snapshot(_OLD, 'MOCK:M07', {2: 'a', 5: 'b'}))
    ck('DG-WIN-OLD-FAILED-still-legal-state', dg_is_legal(dg_read(_OLD, 'MOCK:M07'))
       and dg_preflight(_OLD, 'MOCK:M07', 'test')[1] is None)
    # a fresh round-0 verdict over a FAILED/0 that already has a snapshot: the snapshot
    # survives ONLY if the rework set is identical; otherwise it is retired (never stale)
    _RS = {'difficulty_gate': {'MOCK:M08': {'status': 'FAILED', 'repair_rounds_used': 0, 'rework_qs': [1, 4],
           'gate_rule': DG_RULE_WINDOWS, 'rework_stem_hashes': {'1': 'a', '4': 'b'}, 'baseline_stem_hashes': {'2': 'c'}}}}
    _same = dg_write_verdict(dict(_RS), 'MOCK:M08', status='FAILED', rounds=0, bands=_bands, windows=_W,
                             rework_qs=[4, 1], rework_directions={1: 'harder', 4: 'harder'})
    ck('DG-SNAPSHOT-KEPT-same-rework-set', _same['rework_stem_hashes'] == {'1': 'a', '4': 'b'}
       and 'superseded_snapshots' not in _same)
    _rejudged = dg_write_verdict({'difficulty_gate': {'MOCK:M08': dict(_RS['difficulty_gate']['MOCK:M08'])}},
                                 'MOCK:M08', status='PASSED', rounds=0, bands=_bands, windows=_W, rework_qs=[])
    ck('DG-SNAPSHOT-RETIRED-on-rejudge', 'rework_stem_hashes' not in _rejudged and 'baseline_stem_hashes' not in _rejudged
       and _rejudged['superseded_snapshots'][0]['rework_qs'] == ['1', '4'])
    _diff = dg_write_verdict({'difficulty_gate': {'MOCK:M08': dict(_RS['difficulty_gate']['MOCK:M08'])}},
                             'MOCK:M08', status='FAILED', rounds=0, bands=_bands, windows=_W,
                             rework_qs=[1], rework_directions={1: 'harder'})
    ck('DG-SNAPSHOT-RETIRED-different-set-then-fresh-snapshot', 'rework_stem_hashes' not in _diff
       and dg_add_rework_snapshot({'difficulty_gate': {'MOCK:M08': _diff}}, 'MOCK:M08', {1: 'z'}) == {'1': 'z'})
    _spent = {'difficulty_gate': {'MOCK:M08': {'status': 'DISCLOSED', 'repair_rounds_used': 1, 'rework_qs': [1],
              'gate_rule': DG_RULE_WINDOWS, 'rework_stem_hashes': {'1': 'a', '4': 'b'}}}}
    _carry = dg_write_verdict(_spent, 'MOCK:M08', status='PASSED', rounds=0, windows=_W, rework_qs=[])
    ck('DG-SNAPSHOT-KEPT-on-carried-round', _carry['rework_stem_hashes'] == {'1': 'a', '4': 'b'}
       and dg_state(_carry) == ('PASSED', 1))
    # THE INCIDENT: repair_rounds_used=1 with status FAILED must be UNWRITABLE
    ck_dg_raises('DG-REFUSE-FAILED-1', lambda: dg_write_verdict({}, 'MOCK:M09', status='FAILED', rounds=1))
    ck_dg_raises('DG-REFUSE-PENDING-1', lambda: dg_write_verdict({}, 'MOCK:M09', status='PENDING', rounds=1))
    ck_dg_raises('DG-REFUSE-DISCLOSED-0', lambda: dg_write_verdict({}, 'MOCK:M09', status='DISCLOSED', rounds=0))
    ck_dg_raises('DG-REFUSE-DORMANT-1', lambda: dg_write_verdict({}, 'MOCK:M09', status='DORMANT', rounds=1, dormant_reason='scoped_paper'))
    ck_dg_raises('DG-DORMANT-REASON', lambda: dg_write_verdict({}, 'MOCK:M09', status='DORMANT', rounds=0))
    ck_dg_raises('DG-REFUSE-UNKNOWN-STATUS', lambda: dg_write_verdict({}, 'MOCK:M09', status='OK', rounds=0))
    # snapshot: FAILED-only, write-once, no leak into status/counter
    ck_dg_raises('DG-SNAPSHOT-STATE', lambda: dg_add_rework_snapshot(_R, 'SUBJ:Physics:01', {1: 'x'}))
    ck_dg_raises('DG-SNAPSHOT-NO-RECORD', lambda: dg_add_rework_snapshot(_R, 'MOCK:M77', {1: 'x'}))
    _h1 = dg_add_rework_snapshot(_R, 'MOCK:M01', {1: dg_stem_hash('Q.1 old'), 4: dg_stem_hash('Q.4 old')})
    _h2 = dg_add_rework_snapshot(_R, 'MOCK:M01', {1: 'REPAIRED-HASH', 4: 'REPAIRED-HASH'})
    ck('DG-SNAPSHOT-ONCE', _h1 == _h2 == _R['difficulty_gate']['MOCK:M01']['rework_stem_hashes']
       and _h1['1'] == dg_stem_hash('Q.1 old'))
    ck('DG-SNAPSHOT-NOLEAK', dg_state(dg_read(_R, 'MOCK:M01')) == ('FAILED', 0))
    ck('DG-STEMHASH-PIN', dg_stem_hash('Q.1 x') == '378388b8f9cac200910e0f8ebbc73c6e13525760da0e5b6fc8bea75ddcaa9917'
       and dg_stem_hash('Q.1 x') != dg_stem_hash('Q.1 x '))   # pinned digest locks the algorithm
    # R3 as one call: exact set, extras, missing, no snapshot
    ck('DG-R3-exact', dg_verify_repair(dg_read(_R, 'MOCK:M01'), {1: 'Q.1 new', 4: 'Q.4 new'})['ok'])
    _r3 = dg_verify_repair(dg_read(_R, 'MOCK:M01'), {1: 'Q.1 old', 4: 'Q.4 new'})
    ck('DG-R3-unchanged-listed-named', not _r3['ok'] and _r3['unchanged_listed'] == [1])
    ck('DG-R3-missing-snapshot', dg_verify_repair({'rework_qs': [1]}, {1: 'x'})['missing_snapshot'])
    # E20/E23: extras outside rework_qs are only detectable with the all-question baseline
    _RB = {'difficulty_gate': {'MOCK:M01': {'status': 'FAILED', 'repair_rounds_used': 0, 'rework_qs': [1],
                                            'gate_rule': DG_RULE_WINDOWS}}}
    dg_add_rework_snapshot(_RB, 'MOCK:M01', {1: dg_stem_hash('Q.1 old')},
                           all_stem_hashes={1: dg_stem_hash('Q.1 old'), 2: dg_stem_hash('Q.2 old')})
    _rb = dg_read(_RB, 'MOCK:M01')
    _e20 = dg_verify_repair(_rb, {1: 'Q.1 new', 2: 'Q.2 TAMPERED'})
    ck('DG-R3-changed-unlisted-named', not _e20['ok'] and _e20['changed_unlisted'] == [2] and _e20['extras_verifiable'])
    ck('DG-R3-baseline-exact-ok', dg_verify_repair(_rb, {1: 'Q.1 new', 2: 'Q.2 old'})['ok'])
    _e23 = dg_verify_repair(_rb, {1: 'Q.1 old', 2: 'Q.2 old'})
    ck('DG-R3-pre-repair-paper-attached', not _e23['ok'] and _e23['unchanged_listed'] == [1])
    ck('DG-R3-baseline-write-once', dg_add_rework_snapshot(_RB, 'MOCK:M01', {1: 'x'}, all_stem_hashes={1: 'x', 2: 'x'})
       == {'1': dg_stem_hash('Q.1 old')} and _rb['baseline_stem_hashes']['2'] == dg_stem_hash('Q.2 old'))
    ck('DG-R3-baseline-carried-by-regate', 'baseline_stem_hashes' in
       dg_write_verdict(_RB, 'MOCK:M01', status='PASSED', rounds=1))
    # crash-safety (G-6): a §7A-R that dies before dg_write_verdict leaves (FAILED,0); re-run succeeds
    _crash = {'difficulty_gate': {'MOCK:M01': dict(dg_read(_R, 'MOCK:M01'))}}
    ck('DG-CRASH-SAFE', dg_state(dg_read(_crash, 'MOCK:M01')) == ('FAILED', 0)
       and dg_preflight(_crash, 'MOCK:M01', 'test')[1] is None)
    # the re-gate: atomic, carries the snapshot and migrations forward
    _R2 = {'difficulty_gate': {'MOCK:M01': dict(dg_read(_R, 'MOCK:M01'), migrations=[{'gap': 'X'}])}}
    _v = dg_write_verdict(_R2, 'MOCK:M01', status='DISCLOSED', rounds=1, bands=_bands)
    ck('DG-LEGAL-DISCLOSED-1', dg_state(_v) == ('DISCLOSED', 1) and 'rework_stem_hashes' in _v
       and _v['migrations'] == [{'gap': 'X'}] and _v['schema'] == DG_SCHEMA)
    ck('DG-LEGAL-PASSED-1', dg_state(dg_write_verdict({'difficulty_gate': {'MOCK:M01': dict(dg_read(_R, 'MOCK:M01'))}},
       'MOCK:M01', status='PASSED', rounds=1)) == ('PASSED', 1))
    ck('DG-LEGAL-PASSED-0', dg_state(dg_write_verdict({}, 'MOCK:M02', status='PASSED', rounds=0)) == ('PASSED', 0))
    ck('DG-LEGAL-DORMANT-0', dg_state(dg_write_verdict({}, 'MOCK:M02', status='DORMANT', rounds=0,
       dormant_reason='vocabulary_not_3_band')) == ('DORMANT', 0))
    # ROUND-MONOTONIC (E16): a full re-explain cannot grant a second round
    _R3 = {'difficulty_gate': {'MOCK:M01': dict(_v)}}
    _re = dg_write_verdict(_R3, 'MOCK:M01', status='FAILED', rounds=0, bands=_bands, windows=_W,
                           rework_qs=[4], rework_directions={4: 'harder'})
    ck('DG-ROUND-MONOTONIC', dg_state(_re) == ('DISCLOSED', 1) and _re.get('rounds_carried_from') == 1)
    ck('DG-DORMANT-never-erases-terminal', dg_state(dg_write_verdict({'difficulty_gate': {'MOCK:M01': dict(_v)}},
       'MOCK:M01', status='DORMANT', rounds=0, dormant_reason='blueprint_core_unavailable')) == ('DISCLOSED', 1))
    ck('DG-ROUND-MONOTONIC-pass', dg_state(dg_write_verdict({'difficulty_gate': {'MOCK:M01': dict(_v)}},
       'MOCK:M01', status='PASSED', rounds=0)) == ('PASSED', 1))
    # migration: the LIVE incident record heals to (FAILED,0), disclosed, idempotent
    _live = {'difficulty_gate': {'MOCK:M01': {'schema': 1, 'status': 'FAILED', 'threshold': 0.3,
             'repair_rounds_used': 1, 'bands': _bands, 'rework_qs': [1, 2, 4],
             'timestamp': '2026-08-25T11:20:12+00:00', 'rework_stem_hashes': {'1': 'a', '2': 'b', '4': 'c'}}}}
    ck_dg_raises('DG-ASSERT-ILLEGAL-raises', lambda: dg_assert_legal(_live, 'MOCK:M01', 'test'))
    ck_dg_raises('DG-NEXTSTEP-ILLEGAL-raises', lambda: dg_next_step(_live, 'MOCK:M01', 1, mock=False))
    _rec, _disc = dg_preflight(_live, 'MOCK:M01', 'test')
    ck('DG-MIGRATE-F1', dg_state(_rec) == ('FAILED', 0) and _disc is not None
       and _disc['from'] == 1 and _disc['to'] == 0 and 'HEALED' in _disc['line']
       and _rec['migrations'][0]['gap'] == DG_GAP_ID and _rec['schema'] == DG_SCHEMA
       and _rec['rework_stem_hashes'] == {'1': 'a', '2': 'b', '4': 'c'})
    ck('DG-MIGRATE-IDEMPOTENT', dg_migrate(_live, 'MOCK:M01') is None and len(_rec['migrations']) == 1)
    ck('DG-MIGRATE-DISCLOSED-0', dg_migrate({'difficulty_gate': {'X': {'status': 'DISCLOSED', 'repair_rounds_used': 0}}}, 'X')['to'] == 1)
    ck('DG-MIGRATE-PASSED-clamp', dg_migrate({'difficulty_gate': {'X': {'status': 'PASSED', 'repair_rounds_used': 3}}}, 'X')['to'] == 1)
    ck('DG-MIGRATE-PENDING-1', dg_migrate({'difficulty_gate': {'X': {'status': 'PENDING', 'repair_rounds_used': 1}}}, 'X')['to'] == 0)
    ck('DG-MIGRATE-DORMANT-1', dg_migrate({'difficulty_gate': {'X': {'status': 'DORMANT', 'repair_rounds_used': 2, 'dormant_reason': 'scoped_paper'}}}, 'X')['to'] == 0)
    ck_dg_raises('DG-MIGRATE-UNKNOWN', lambda: dg_migrate({'difficulty_gate': {'X': {'status': 'BOGUS'}}}, 'X'))
    ck('DG-LEGACY-none', dg_preflight({}, 'MOCK:M01', 'test') == (None, None)
       and dg_next_step({}, 'MOCK:M01', 1, mock=True) == 'MockDeliver M1'
       and dg_deliver_decision({}, 'MOCK:M01', 1, mock=True)['deliver'])
    ck('DG-E17-missing-counter', dg_is_legal({'status': 'PASSED'}))
    # NEXT-STEP AGREES WITH STEP 11 (the mechanical G-3 guard): for every legal state
    # the step dg_next_step names is one whose own preflight accepts that state.
    # (windowed rule: TestExplain also accepts a FAILED record judged under the
    #  retired rule — it re-judges it; TestCreateRepair accepts only a windowed FAILED.)
    def _accepts(step, st, windowed):
        return {'Deliver': st in DG_DELIVERABLE,
                'Explain': st == 'PENDING' or (st == 'FAILED' and not windowed),
                'CreateRepair': st == 'FAILED' and windowed}[step]
    _agree = True
    for (_st, _rn) in DG_LEGAL_STATES:
      for _win in (True, False):
        _reg = {'difficulty_gate': {'MOCK:M05': {'status': _st, 'repair_rounds_used': _rn,
                'rework_qs': [3], 'dormant_reason': 'scoped_paper',
                **({'gate_rule': DG_RULE_WINDOWS} if _win else {})}}}
        _cmd = dg_next_step(_reg, 'MOCK:M05', 5, mock=False)
        _step = _cmd.split()[0].replace('Test', '')
        _agree &= _accepts(_step, _st, _win)
        _dec = dg_deliver_decision(_reg, 'MOCK:M05', 5, mock=False)
        _agree &= (_dec['deliver'] == (_st in DG_DELIVERABLE))
        _agree &= (_dec['next_step'] is None) == _dec['deliver']
    ck('DG-NEXTSTEP-AGREE', _agree)
    ck('DG-NEXTSTEP-FAILED-lists-qs', dg_next_step({'difficulty_gate': {'MOCK:M05': {'status': 'FAILED',
       'repair_rounds_used': 0, 'rework_qs': [3, 8], 'gate_rule': DG_RULE_WINDOWS}}}, 'MOCK:M05', 5, mock=True)
       == 'MockCreateRepair M5 Q3 Q8\n   then: MockExplainRepair M5')
    # footer: shape is a function of status; migrations always disclosed
    ck('DG-FOOTER-DISCLOSED-pre-window', dg_footer_lines(_v)[0]
       == 'Measured difficulty: Easy 0/6 · Hard 1/6 confirmed after 1 repair round.'
       and len(dg_footer_lines(_v)) == 2)          # + the carried migration line
    _vw = dg_write_verdict({'difficulty_gate': {'MOCK:M01': dict(dg_read(_R, 'MOCK:M01'))}}, 'MOCK:M01',
                           status='DISCLOSED', rounds=1, bands=_bands, windows=_W)
    ck('DG-FOOTER-DISCLOSED-windowed', dg_footer_lines(_vw)
       == ['Measured difficulty: Easy 6 (not gated) · Hard 1/6 in window confirmed after 1 repair round.'])
    ck('DG-FOOTER-DISCLOSED-windowed-missing-gated-key', 'in window' in dg_footer_lines(
       {'status': 'DISCLOSED', 'repair_rounds_used': 1, 'gate_rule': DG_RULE_WINDOWS,
        'bands': {'Medium': {'total': 3, 'agree': 2}}})[0])
    ck('DG-FOOTER-DORMANT', dg_footer_lines(dg_read(_R, 'SUBJ:Physics:01'))
       == ['Difficulty gate: not applicable to this paper (scoped_paper) — labels are as planned at Step 7.'])
    ck('DG-FOOTER-PASSED-none', dg_footer_lines({'status': 'PASSED', 'repair_rounds_used': 0}) == [])
    ck('DG-FOOTER-MIGRATION', any('healed' in ln for ln in dg_footer_lines(_rec)))
    ck('DG-FOOTER-PENDING-no-bands-KeyError', dg_footer_lines({'status': 'PENDING'}) == [])
    # fleet heal: report vs apply, scoped PENDING cohort, escalation never touched
    _fleet = {'difficulty_gate': {
        'MOCK:M01': {'status': 'FAILED', 'repair_rounds_used': 1, 'rework_qs': [1]},
        'MOCK:M02': {'status': 'PENDING', 'repair_rounds_used': 0},
        'SUBJ:Chem:01': {'status': 'PENDING', 'repair_rounds_used': 0},
        'SUBJ:Chem:02': {'status': 'PENDING', 'repair_rounds_used': 1},
        'MOCK:M03': {'status': 'WEIRD', 'repair_rounds_used': 0}}}
    _rep = dg_fleet_heal(_fleet, apply=False)
    ck('DG-FLEET-REPORT', [x[0] for x in _rep['illegal']] == ['MOCK:M01', 'SUBJ:Chem:02'] and _rep['pending'] == ['MOCK:M02']
       and _rep['stuck_scoped'] == ['SUBJ:Chem:01'] and [x[0] for x in _rep['escalate']] == ['MOCK:M03']
       and not _rep['changed'] and dg_state(_fleet['difficulty_gate']['MOCK:M01']) == ('FAILED', 1))
    _app = dg_fleet_heal(_fleet, apply=True)
    ck('DG-FLEET-APPLY', _app['changed'] and sorted(_app['healed']) == ['MOCK:M01', 'SUBJ:Chem:01', 'SUBJ:Chem:02']
       and dg_state(_fleet['difficulty_gate']['SUBJ:Chem:02']) == ('DORMANT', 0)
       and dg_fleet_heal(_fleet, apply=False)['illegal'] == [] and dg_fleet_heal(_fleet, apply=False)['stuck_scoped'] == []
       and dg_state(_fleet['difficulty_gate']['MOCK:M01']) == ('FAILED', 0)
       and dg_state(_fleet['difficulty_gate']['SUBJ:Chem:01']) == ('DORMANT', 0)
       and _fleet['difficulty_gate']['MOCK:M03']['status'] == 'WEIRD'
       and dg_state(_fleet['difficulty_gate']['MOCK:M02']) == ('PENDING', 0))

    # v5.38 (GAP-2026-08-03-BANNER) — THE BANNER IS THE LAST THING COMPUTED.
    # It previously sat mid-function, so the 13 LABELFMT fixtures appended after
    # it ran OUTSIDE the count: reintroducing THIS release's own defect printed a
    # green "SELF-TEST: 37/37 PASS" directly above the traceback of the fixture
    # written to catch it. The exit code was right, but every human and every spec
    # quoting the banner reads PASS over broken work — the false-clean-banner shape
    # (GAP-2026-07-26-003). A banner printed before the last check is a lie by
    # construction, regardless of what the checks say.
    print(f"SELF-TEST: {p}/{p + f} PASS"
          + ("" if not f else f"  ({f} FAILED: " + ", ".join(_failed) + ")"))
    return f == 0


class LabelFormatError(Exception):
    """Raised when section_rules declares an option_label_format this framework
    cannot render. NEVER guessed at (v5.37) — see resolve_option_label."""


# ── OPTION LABEL RESOLUTION (v5.37, GAP-2026-08-03-LABELFMT) ────────────────────
# SINGLE SOURCE OF TRUTH for turning the section_rules `option_label_format`
# notation ('1/2/3/4', 'A/B/C/D', 'i/ii/iii/iv', ...) into BOTH the render
# template Step 7 emits with AND the label family the auditor audits against.
#
# WHY IT LIVES HERE. Before v5.37 the two steps derived this INDEPENDENTLY:
# Step 7 by testing the leading token's CASING inside a spec code block, the auditor by
# a regex family classifier in audit_canonical. They disagreed, and the disagreement
# was a guaranteed halt:
#     section_rules 'i/ii/iii/iv'
#        Step 7  -> .islower() is True for 'i'  -> ({alpha_lower}) -> renders (a)(b)(c)(d)
#        auditor -> option_label_family        -> 'roman'
#        result  -> A-OPTLABEL FAIL on EVERY question, exit 1, MANDATE D blocks
#                   delivery, and NO CP repair can fix it because the paper matches
#                   Step 7's own contract. Measured end-to-end.
# paper_pipeline is routed by BOTH MockCreate and TestCreate, so one function
# here is reachable from both and the pair cannot drift again.
#
# ROMAN IS SUPPORTED, NOT REFUSED. Refusing would trade a mid-audit halt for a
# pre-generation halt; supporting it makes the declared format actually work.
#
# UNRECOGNISED NOTATION HARD-STOPS. The old code had no else-branch, so
# '(1)/(2)/(3)/(4)' fell through and became the render template VERBATIM — a
# template with no {text} placeholder, i.e. no substitution at all. '[A]/[B]/[C]/[D]'
# silently became '(A)', and '①/②/③/④' silently became '1.' (Python's .isdigit() is
# True for circled digits). Guessing here contradicts the framework's own posture
# everywhere else (pick_blueprint raises PickError; derive_nat_grading raises on an
# ambiguous range) and the guess reaches the delivered paper.

_ROMAN = ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x')


def option_label_family(fmt):
    """The audit-side family for a section_rules option_label_format.

    Byte-compatible with audit_canonical.option_label_family — asserted by a
    differential fixture in BOTH self-tests, so a change to either is caught.
    """
    import re                      # local: paper_pipeline is a THIN CORE (CHECK AB)
    first = (fmt or '1/2/3/4').split('/')[0].strip().strip('()').strip('.').strip(')')
    if first.isdigit():
        return 'num'
    if re.fullmatch(r'[ivxIVX]+', first):
        return 'roman'
    if len(first) == 1 and first.isalpha():
        return 'alpha'
    return 'num'


def resolve_option_label(fmt):
    """(render_template, family) for a section_rules option_label_format.

    Raises LabelFormatError on any notation this framework cannot render, rather
    than degrading to a template that silently produces the wrong labels.
    """
    if not fmt:
        return ('{i}.  {text}', 'num')
    fmt = str(fmt).strip()
    if '{' in fmt:                      # already a render template — pass through
        return (fmt, option_label_family(fmt))
    if '/' not in fmt:
        raise LabelFormatError(
            f"option_label_format {fmt!r} is not a recognised notation. Expected a "
            f"'/'-separated sample of the first labels, e.g. '1/2/3/4', 'A/B/C/D', "
            f"'a/b/c/d', 'i/ii/iii/iv' or 'I/II/III/IV'.")
    toks = [t.strip() for t in fmt.split('/') if t.strip()]
    first = toks[0]
    bare = first.strip('()[].)')
    # ROMAN FIRST: 'i' is BOTH a single alpha character and a roman numeral, so the
    # single-letter test below would swallow it. Disambiguated on the SEQUENCE, not
    # the first token alone — 'i/ii/iii/iv' is roman, 'i/j/k/l' is alpha.
    lowered = [t.strip('()[].)').lower() for t in toks]
    if len(lowered) >= 2 and all(t in _ROMAN for t in lowered[:2]) \
            and lowered[:2] == list(_ROMAN[:2]):
        tok = '{roman_upper}' if bare.isupper() else '{roman_lower}'
    elif bare.isdigit() and bare.isascii():
        tok = '{i}'
    elif len(bare) == 1 and bare.isalpha() and bare.isascii():
        tok = '{alpha_upper}' if bare.isupper() else '{alpha_lower}'
    else:
        raise LabelFormatError(
            f"option_label_format {fmt!r} declares labels this framework cannot "
            f"render (first token {first!r}). Supported: decimal digits, a single "
            f"ASCII letter, or roman numerals. Add explicit support before using it "
            f"— it is NEVER guessed at, because a guessed label reaches the "
            f"delivered paper and the auditor then fails every question against the "
            f"format section_rules actually declared.")
    # preserve the declared bracketing/punctuation around the token
    lead = first[:len(first) - len(first.lstrip('(['))]
    trail = first[len(first.rstrip(').]')):]
    if not lead and not trail:
        trail = '.'
    template = f'{lead}{tok}{trail}  {{text}}'
    # ── THE SYNC INVARIANT (v5.37) ────────────────────────────────────────────
    # STEP 7 MUST NEVER EMIT LABELS WHOSE FAMILY STEP 8 WILL CLASSIFY DIFFERENTLY.
    # Resolution and classification are two different computations, so agreement
    # is ASSERTED here rather than assumed. Two real notations fail it and would
    # otherwise reproduce GAP-2026-08-03-LABELFMT under a new name:
    #   'i/j/k/l'          -> renders a,b,c,d (the SEQUENCE is alpha, not roman)
    #                         but the classifier reads the first token 'i' as roman
    #   '[A]/[B]/[C]/[D]'  -> renders [A],[B] (alpha) but the classifier strips only
    #                         ()., not [], so it reads 'num'
    # In both cases the auditor would fail every question on a paper that obeys Step 7.
    # Refusing at PRE-GENERATION is not the halt class this framework fights: it
    # happens before Q1, names the exact conflict, and prevents a paper that could
    # never certify. A guessed label, by contrast, reaches the delivered document.
    _tok_family = {'{i}': 'num',
                   '{alpha_upper}': 'alpha', '{alpha_lower}': 'alpha',
                   '{roman_upper}': 'roman', '{roman_lower}': 'roman'}[tok]
    _audit_family = option_label_family(fmt)
    if _tok_family != _audit_family:
        raise LabelFormatError(
            f"option_label_format {fmt!r} is AMBIGUOUS ACROSS STEPS: Step 7 would "
            f"render it as {_tok_family!r} labels (e.g. {template!r}) while the auditor's "
            f"option_label_family classifies it as {_audit_family!r}. The auditor would "
            f"then FAIL A-OPTLABEL on every question of a paper that obeys Step 7, "
            f"with no repair possible. Declare an unambiguous notation "
            f"('1/2/3/4', 'A/B/C/D', 'a/b/c/d', 'i/ii/iii/iv', 'I/II/III/IV', or "
            f"those in round brackets) — this is NEVER guessed at.")
    return (template, _tok_family)


# ── 10. KEY COMMITMENTS (v5.39, GAP-2026-08-21-EXPLANATION-PROVENANCE) ────────────
KEY_COMMITMENT_SCHEMA = 1

def canonical_answer(qtype, value):
    """The ONE string both steps hash. mcq -> '2'; msq -> '2,3' (sorted, comma,
    no spaces); nat -> the portal grading string exactly as derive_nat_grading
    produced it ('484', '3.09', '0.414-0.416') — never a float repr."""
    if qtype == 'msq':
        vals = value if isinstance(value, (list, tuple, set, frozenset)) else [value]
        return ','.join(str(int(v)) for v in sorted(int(x) for x in vals))
    if qtype == 'nat':
        return str(value).strip()
    return str(int(value)) if not isinstance(value, str) else value.strip()

def key_commitment(paper_id, q, canonical, salt):
    import hashlib
    return hashlib.sha256(f'{paper_id}|{int(q)}|{salt}|{canonical}'.encode('utf-8')).hexdigest()

def seal_key_commitments(paper_id, answers, salts=None):
    """answers: {q: canonical_answer_string}. Returns the registry block
    {'schema': 1, 'alg': 'sha256', 'entries': {str(q): {'salt': hex, 'h': hex}}}.
    Deterministic when salts are supplied (tests); random 16-byte salts otherwise."""
    import secrets
    entries = {}
    for q, canon in answers.items():
        salt = (salts or {}).get(q, (salts or {}).get(str(q))) or secrets.token_hex(16)
        entries[str(int(q))] = {'salt': salt, 'h': key_commitment(paper_id, q, str(canon), salt)}
    return {'schema': KEY_COMMITMENT_SCHEMA, 'alg': 'sha256', 'entries': entries}

def verify_key_commitments(commitments, derived, paper_id):
    """derived: {q: canonical_answer_string} from the EXPLAINING step. Returns
    {'matched': [q], 'mismatched': [q], 'missing': [q]} (missing = derived but
    never committed). Pure; never raises on a mismatch."""
    ents = (commitments or {}).get('entries', {})
    out = {'matched': [], 'mismatched': [], 'missing': []}
    for q in sorted(int(x) for x in derived):
        e = ents.get(str(q))
        if not e:
            out['missing'].append(q); continue
        if key_commitment(paper_id, q, str(derived[q] if q in derived else derived[str(q)]),
                          e['salt']) == e['h']:
            out['matched'].append(q)
        else:
            out['mismatched'].append(q)
    return out

def resolve_commitment(commitments, q, candidates, paper_id):
    """The in-run resolution probe: which of `candidates` (canonical strings) the
    committed hash for q accepts, or None. Used ONLY after a mismatch, to learn
    what Step 7 intended without a plaintext key ever existing."""
    e = (commitments or {}).get('entries', {}).get(str(int(q)))
    if not e:
        return None
    for c in candidates or []:
        if key_commitment(paper_id, q, str(c), e['salt']) == e['h']:
            return str(c)
    return None

# ── 11. FIGURE SEMANTIC OBJECTS (v5.39) ──────────────────────────────────────────
SEMANTIC_KINDS = ('STRUCTURE', 'REACTION', 'NEWMAN', 'FISCHER', 'MO_DIAGRAM',
                  'ORBITAL_BOXES', 'COORDINATION', 'PLOT', 'TABLE', 'GEOMETRY', 'GENERIC')
SEMANTIC_ROLE_RE = None

def validate_semantic_object(obj, ctx=''):
    """Shape-validate one semantic object:
      {role: 'problem' | 'problem:<i>' | 'option:<label>', kind: SEMANTIC_KINDS,
       name: str (human-readable identity), canonical: str|None, descriptor: dict}
    kind STRUCTURE/REACTION MUST carry canonical (SMILES; reaction SMILES for
    REACTION). Raises ValueError on breach."""
    import re as _re
    if not isinstance(obj, dict):
        raise ValueError(f'{ctx}: semantic object is not a dict')
    role = str(obj.get('role', ''))
    if not _re.match(r'^(problem(:\d+)?|option:\S+)$', role):
        raise ValueError(f'{ctx}: semantic object role {role!r} must be problem, '
                         f'problem:<i> or option:<label>')
    kind = obj.get('kind')
    if kind not in SEMANTIC_KINDS:
        raise ValueError(f'{ctx}: semantic object kind {kind!r} not in {SEMANTIC_KINDS}')
    if not str(obj.get('name', '')).strip():
        raise ValueError(f'{ctx}: semantic object needs name (what the figure depicts)')
    if kind in ('STRUCTURE', 'REACTION') and not str(obj.get('canonical', '')).strip():
        raise ValueError(f'{ctx}: semantic object kind {kind} needs canonical (SMILES / '
                         f'reaction SMILES) — a structure with no machine-readable '
                         f'identity cannot be reconciled by the explaining step')
    if not isinstance(obj.get('descriptor', {}), dict):
        raise ValueError(f'{ctx}: semantic object descriptor must be a dict')
    return True

def semantic_objects_agree(a, b, canon=None):
    """Identity test between two semantic objects (or two canonical strings).
    `canon` is an injected canonicaliser (smiles) -> (canonical|None, reason) —
    corpus_io.canonical_structure on the Create route, explain_engine.
    canonical_structure on the Explain route; paper_pipeline itself stays
    thin-core (CHECK AB) and, with canon=None, compares strings. Non-structure
    kinds compare their descriptor dicts. Returns (agree: bool, detail: str)."""
    ca = a.get('canonical') if isinstance(a, dict) else a
    cb = b.get('canonical') if isinstance(b, dict) else b
    ka = a.get('kind') if isinstance(a, dict) else 'STRUCTURE'
    if ka in ('STRUCTURE', 'REACTION') or not isinstance(a, dict):
        if canon is not None:
            na, ra = canon(ca); nb, rb = canon(cb)
            if na is not None and nb is not None:
                return na == nb, f'canonical {na!r} vs {nb!r}'
            if ra != 'rdkit_unavailable' or rb != 'rdkit_unavailable':
                return False, f'{ra}; {rb}'
        return str(ca).strip() == str(cb).strip(), 'string compare'
    da = (a or {}).get('descriptor', {}); db = (b or {}).get('descriptor', {})
    return da == db, 'descriptor compare'

# ── 9. question_index FK validation + registry ledger integrity (v2026.08.10 —
#       GAP-2026-08-10-QINDEX-FK-ENFORCEMENT). Pure: data in, data out.
#
#   ARCHITECTURE — ONE CONTRACT, FOUR INDEPENDENT IMPLEMENTATIONS (corrected
#   2026.08.10.5; the original header here claimed "ONE implementation,
#   imported by Step 7 … Step 9 … Step 11", which was FALSE — none of those
#   steps import these helpers, and believing it would make an editor change
#   this file and assume every step followed). The FK/coverage/difficulty
#   contract is enforced at four sites, each DELIBERATELY self-contained:
#     1. THIS FILE — the REFERENCE implementation. Consumers: standalone
#        tooling, one-time corpus sweeps, and the agreement fixtures in
#        audit_canonical's self-test. Not imported by any step spec.
#     2. audit_canonical.gate_qindex (A-QINDEX) — self-contained ON PURPOSE:
#        it ships as a per-exam Step-6 copy that must carry zero new imports.
#        This is the enforcement of record (exit-code-logged at S13-4c).
#     3. Framework_MockTestExplain P10 — spec-inline preflight, self-contained
#        so the tripwire needs nothing importable at that point in a session.
#     4. Framework_MockDeliver S1-2/S1-3 — spec-inline; S1-3's remediation
#        classifier mirrors classify_unresolved below (same leaf rule, same
#        difflib cutoff=0.5).
#   Independence is the point: an inline gate can be skipped by a defective
#   session, but a shared import cannot substitute for it at sites 2-4 (per-
#   exam copies and spec-inline blocks cannot depend on this module being on
#   the path). The drift risk of four copies is held down by the A-QINDEX
#   self-test agreement matrix, which EXECUTES all four and compares them:
#   this module vs gate_qindex vs the P10 block extracted from
#   Framework_MockTestExplain vs the S1-3 classifier extracted from
#   Framework_MockDeliver (classes AND candidate lists, so the difflib
#   cutoff is pinned too). Added 2026.08.10.5 — until then the matrix
#   compared sites 1 and 2 only, and site 3 had already shipped one release
#   MISSING its q-set coverage check while sites 1-2 rejected the same
#   registry. ANY change to the contract must touch ALL FOUR sites above and
#   keep that matrix green — this list is the map, and the matrix is what
#   makes the map load-bearing rather than advisory. ─────────────────────────
def subtopic_set_hash(blueprint):
    """Stable hash of the blueprint's subtopic_id set (provenance stamp)."""
    import hashlib
    ids = sorted(s.get('subtopic_id') or '' for s in blueprint.get('subtopic_list', []))
    return hashlib.sha256('\n'.join(ids).encode('utf-8')).hexdigest()[:16]


def validate_question_index(registry, blueprint, mock_n=None, paper_id=None):
    """FK-validate one paper's question_index against the blueprint.
    Returns (ok: bool, report: dict). report['fails'] lists every violation;
    report['bad_ids'] maps q -> offending subtopic_id for classifier use.
    Never raises; callers decide HARD STOP vs WARN."""
    fails, bad_ids = [], {}
    if paper_id is None:
        if mock_n is None:
            return False, {'fails': ['validate_question_index: need mock_n or paper_id'],
                           'bad_ids': {}}
        _tp = next((mk for mk in blueprint.get('mocks', [])
                    if mk.get('mock') == mock_n), None)
        paper_id = (_tp or {}).get('paper_id', f"MOCK:M{int(mock_n):02d}")
    entry = next((e for e in registry.get('question_index', [])
                  if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == paper_id), None)
    if entry is None:
        return False, {'fails': [f'A-QINDEX/1: no question_index entry for {paper_id}'],
                       'bad_ids': {}, 'paper_id': paper_id, 'entry_missing': True}
    qs = entry.get('questions', [])
    tq = blueprint.get('total_questions')
    if tq is not None and len(qs) != tq:
        fails.append(f'A-QINDEX/2: {len(qs)} entries != total_questions {tq}')
    qn = [x.get('q') for x in qs]
    if tq is not None and (qn != sorted(qn) or len(set(qn)) != len(qn)
                           or set(qn) != set(range(1, tq + 1))):
        fails.append(f'A-QINDEX/3: q set != 1..{tq} (sorted/unique/complete)')
    sub_ids = {s.get('subtopic_id') for s in blueprint.get('subtopic_list', [])}
    for x in qs:
        sid = x.get('subtopic_id')
        if sid not in sub_ids:
            bad_ids[int(x.get('q', -1))] = sid
    if bad_ids:
        fails.append('A-QINDEX/4: subtopic_id(s) not in blueprint.subtopic_list: '
                     + '; '.join(f"Q{q}={bad_ids[q]!r}" for q in sorted(bad_ids)))
    canon = blueprint.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])
    bad_d = sorted({x.get('difficulty') for x in qs if x.get('difficulty') not in canon})
    if bad_d:
        fails.append(f'A-QINDEX/5: difficulty value(s) not in {canon}: {bad_d}')
    # ── GAP-2026-08-12-QINDEX-QUOTA-ENFORCEMENT ──────────────────────────────
    # check 6: the SCHEDULE-FIRST quota (difficulty_schedule[mock_n], Contract_
    # QuestionMetadataIndex v1.0) must be met EXACTLY, not merely with canonical
    # labels. Checks 1-5 moved into the engine at GAP-2026-08-10-QINDEX-FK-
    # ENFORCEMENT; check 6 was left session-executed-only, so a session could
    # pass checks 1-5 with a genuinely non-compliant distribution (e.g. every
    # difficulty null, or a free assessment that never matched the schedule)
    # and still log a clean, exit-code-durable audit, because nothing durably
    # logged ever compared the count. Dormant (not evaluated, never invented)
    # when this exam does not declare difficulty_schedule at all; if it does
    # but has no entry for THIS mock, that is itself a fail — a real gap in a
    # feature the exam opted into, not silence.
    sched_list = blueprint.get('difficulty_schedule')
    if sched_list and mock_n is not None:
        sched = next((d for d in sched_list if d.get('mock') == mock_n), None)
        if sched is None:
            fails.append(f'A-QINDEX/6: exam declares difficulty_schedule but has no '
                         f'entry for mock {mock_n}')
        else:
            alias3 = ({'simple': canon[0], 'medium': canon[1], 'hard': canon[2]}
                      if len(canon) == 3
                      else {'simple': 'Easy', 'medium': 'Medium', 'hard': 'Hard'})
            want = {}
            for k, v in sched.items():
                if k in ('mock', 'band') or not isinstance(v, int):
                    continue
                lab = alias3.get(k, k)
                want[lab] = want.get(lab, 0) + v
            want = {lab: want.get(lab, 0) for lab in canon}
            got = {lab: 0 for lab in canon}
            for x in qs:
                d = x.get('difficulty')
                if d in got:
                    got[d] += 1
            if got != want:
                fails.append(f'A-QINDEX/6: difficulty distribution {got} != '
                             f'schedule quota {want}')
    return (not fails), {'fails': fails, 'bad_ids': bad_ids, 'paper_id': paper_id,
                         'entry_missing': False}


def registry_integrity_check(registry):
    """Ledger <-> index agreement (closes the lost-question_index class, e.g. a
    completed mock whose per-question data was dropped by a later write).
    Invariant: every paper the ledgers claim complete has a question_index
    entry, and every question_index entry is claimed complete.
    Returns (ok, report) with report['missing_index'] / report['orphan_index']."""
    claimed = set(registry.get('papers_completed') or [])
    for m in registry.get('mocks_completed') or []:
        try:
            claimed.add(f"MOCK:M{int(m):02d}")
        except (TypeError, ValueError):
            pass
    have = {e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}")
            for e in registry.get('question_index', [])}
    missing = sorted(claimed - have)   # completed but data lost  -> Class A
    orphan  = sorted(have - claimed)   # data present, never claimed complete
    ok = not missing                    # orphans are advisory, never fatal
    return ok, {'missing_index': missing, 'orphan_index': orphan}


def classify_unresolved(bad_ids, blueprint):
    """Classify stale registry subtopic_ids for remediation (Step 11 S1-3).
    bad_ids: {q: stale_id}. Returns {q: {'stale', 'cls', 'targets'}} where cls is
      'W1' stale leaf exists on exactly ONE current subtopic  -> deterministic patch
      'W2' leaf reworded (no verbatim leaf)                   -> confirm candidates
      'D'  leaf exists on MULTIPLE current subtopics          -> human decision
    Pure; suggestion only — callers must never auto-apply W2/D."""
    import difflib
    by_leaf = {}
    all_ids = []
    for s in blueprint.get('subtopic_list', []):
        sid = s.get('subtopic_id') or ''
        all_ids.append(sid)
        by_leaf.setdefault(sid.rsplit('.', 1)[-1], []).append(sid)
    out = {}
    for q, stale in bad_ids.items():
        leaf = (stale or '').rsplit('.', 1)[-1]
        tgts = by_leaf.get(leaf, [])
        if len(tgts) == 1:
            out[q] = {'stale': stale, 'cls': 'W1', 'targets': tgts}
        elif len(tgts) > 1:
            out[q] = {'stale': stale, 'cls': 'D', 'targets': sorted(tgts)}
        else:
            cand = difflib.get_close_matches(stale or '', all_ids, n=3, cutoff=0.5)
            out[q] = {'stale': stale, 'cls': 'W2', 'targets': cand}
    return out




# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER DG — DIFFICULTY-GATE RECORD, SINGLE WRITER
#            (v5.71 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER)
#
# registry['difficulty_gate'][paper_id] is cross-step, machine-read state: written at
# Step 7 (birth), Step 9 (§7A-M gate, §7A-R re-gate) and Step 7-repair (§S16-3
# snapshot), READ by Step 7-repair, Step 9, Step 9-repair and Step 11. Before this
# cluster the ownership rule existed only as one clause of English prose
# (MockTestCreate §S16-3: "UNTOUCHED except adding rework_stem_hashes") with no guard
# behind it. A TestCreateRepair session set repair_rounds_used = 1 while status was
# still 'FAILED' — a pair no step can produce on purpose — and the four triggers that
# read the record refused the same paper with no exit (a completed 60-question paper
# and its full explanation run were unrecoverable without a manual registry edit).
#
# FROM HERE NO SPEC MAY WRITE THIS RECORD BY HAND. Every mutation goes through the
# three permitted writers below, each of which validates the resulting
# (status, repair_rounds_used) pair against DG_LEGAL_STATES before returning. Same
# posture as bc.DATE_TAG_RE / cur_date_label (Framework_DeliveryFooter §2): one
# writer, mechanically enforced. paper_pipeline is the ONLY engine on all six routes
# (TestCreate · TestCreateRepair · TestExplain · TestExplainRepair · TestDeliver and
# their Mock* aliases), which is why the cluster lives here and not in blueprint_core.
#
# LEGAL STATE MACHINE (the contract no spec declared before v5.71):
#     S0  (absent)        legacy paper, pre-gate           Step 11: DELIVER
#     S1  PENDING   / 0   born; gate has not run           Step 11: HARD STOP → TestExplain
#     S2  PASSED    / 0   gate passed first time           Step 11: DELIVER
#     S3  FAILED    / 0   gate failed; ONE repair round    Step 11: HARD STOP → CreateRepair → ExplainRepair
#     S4  PASSED    / 1   repaired; re-gate passed         Step 11: DELIVER
#     S5  DISCLOSED / 1   repaired; re-gate failed         Step 11: DELIVER + §FOOTER-DG line
#     S6  DORMANT   / 0   gate not applicable              Step 11: DELIVER + dormancy line
#
# DG-INVARIANT. A COMPLETED repair round resolves status away from FAILED (to PASSED
# or DISCLOSED) in the SAME atomic write that sets repair_rounds_used = 1. Therefore
# status == 'FAILED' ⇒ repair_rounds_used MUST be 0; any other value proves the
# counter was written out of contract and the round is UNCONSUMED. This is what makes
# dg_migrate deterministic: the record alone fixes itself, no history needed.
#
# ROUND-MONOTONIC. repair_rounds_used never decreases through a legal writer. A full
# §7A-M re-gate on a paper whose round is already spent (a TestExplain re-run after a
# repair) cannot hand the paper a second round: a FAIL verdict on a spent round
# resolves to DISCLOSED/1, never FAILED/0. See dg_write_verdict.
#
# Pure: mutates the dict handed in, performs no I/O (thin-core, CHECK AB). The
# fleet-scan CLI (`python3 final_assembly.py --dg-fleet-scan ROOT [--apply]`) lives in the
# I/O shell and calls dg_fleet_heal below on each loaded registry.
# ═══════════════════════════════════════════════════════════════════════════════


DG_SCHEMA = 2                    # v2 = legal states declared; v1 records auto-upgrade
DG_MAX_REPAIR_ROUNDS = 1         # MIRRORS bc.DIFFICULTY_GATE_MAX_REPAIR_ROUNDS (self-test asserts parity)
DG_DEFAULT_THRESHOLD = 0.35      # MIRRORS bc.DIFFICULTY_GATE_MAX_DISAGREE_FRAC  (self-test asserts parity)
                                 # 0.30 → 0.35: operator decision 2026-08-25 (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS)
DG_RULE_WINDOWS = 'windows'      # rec['gate_rule'] written by every verdict under the windowed rule;
                                 # a FAILED record WITHOUT it was judged by the retired band-equality
                                 # rule and is re-judged (TestExplain), never repaired — dg_is_windowed

DG_DELIVERABLE = frozenset({'PASSED', 'DISCLOSED', 'DORMANT'})   # Step 11 may proceed
DG_BLOCKING    = frozenset({'PENDING', 'FAILED'})                # Step 11 hard-stops
DG_STATUSES    = DG_DELIVERABLE | DG_BLOCKING

DG_DORMANT_REASONS = ('no_difficulty_labels', 'vocabulary_not_3_band',
                      'blueprint_core_unavailable', 'scoped_paper')

DG_GAP_ID = 'GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER'


def _dg_legal_states(max_rounds):
    """The legal (status, rounds) table, GENERATED from the round limit so raising
    bc.DIFFICULTY_GATE_MAX_REPAIR_ROUNDS later needs no table edit (edge case E18).
    Rules: PENDING/FAILED/DORMANT admit only 0; DISCLOSED admits only max_rounds
    (the round budget is exhausted by definition); PASSED admits 0..max_rounds."""
    legal = {('PENDING', 0): 'final_assembly.commit_registry (birth)',
             ('DORMANT', 0): 'final_assembly (scoped) / Step 9 §7A-M (dormant gate)'}
    for r in range(0, max_rounds + 1):
        who = 'Step 9 Framework_MockTestExplain §7A-M' if r == 0 else 'Step 9 Framework_MockTestExplain §7A-R'
        legal[('PASSED', r)] = who
        if r < max_rounds:                    # FAILED with a round still available
            legal[('FAILED', r)] = who
    legal[('DISCLOSED', max_rounds)] = 'Step 9 Framework_MockTestExplain §7A-R'
    return legal


DG_LEGAL_STATES = _dg_legal_states(DG_MAX_REPAIR_ROUNDS)


class DGIllegalState(ValueError):
    """A difficulty_gate record is not a legal (status, repair_rounds_used) pair, or a
    writer was asked to produce one. The message carries the operator-facing remedy."""


def _dg_now():
    import datetime                 # local: paper_pipeline is a THIN CORE (CHECK AB)
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# ── read / validate ──────────────────────────────────────────────────────────────
def dg_read(reg, paper_id):
    """The record for paper_id, or None for a LEGACY (pre-gate) paper."""
    return (reg.get('difficulty_gate') or {}).get(paper_id)


def dg_state(rec):
    """(status, rounds) as a normalised tuple. A missing/None counter reads as 0."""
    try:
        n = int(rec.get('repair_rounds_used') or 0)
    except (TypeError, ValueError):
        n = -1                               # non-integer counter is illegal by construction
    return (rec.get('status'), n)


def dg_is_legal(rec):
    return dg_state(rec) in DG_LEGAL_STATES


def dg_diagnose_illegal(rec):
    """Deterministic one-field repair for a corrupt record, resting on DG-INVARIANT.
    Returns {'field','from','to','explanation','remedy'}; 'to' is None when the record
    is uninterpretable (unknown status) — such a record is NEVER auto-repaired."""
    st, n = dg_state(rec)
    if st == 'FAILED' and not (0 <= n < DG_MAX_REPAIR_ROUNDS):
        to = DG_MAX_REPAIR_ROUNDS - 1
        return {'field': 'repair_rounds_used', 'from': n, 'to': to,
                'explanation': (f"status is 'FAILED', which proves the final repair round never "
                                f"COMPLETED (a completed final round writes PASSED or DISCLOSED "
                                f"atomically with the counter). The counter was written "
                                f"out of contract; a repair round is UNCONSUMED."),
                'remedy': f"set repair_rounds_used to {to} — the repair round is intact."}
    if st in ('PENDING', 'DORMANT') and n != 0:
        return {'field': 'repair_rounds_used', 'from': n, 'to': 0,
                'explanation': (f"status is {st!r}: the gate never ran (PENDING) or does not "
                                f"apply (DORMANT), so no repair round can have been used."),
                'remedy': "set repair_rounds_used to 0."}
    if st == 'DISCLOSED' and n != DG_MAX_REPAIR_ROUNDS:
        return {'field': 'repair_rounds_used', 'from': n, 'to': DG_MAX_REPAIR_ROUNDS,
                'explanation': (f"status DISCLOSED is only reachable after the "
                                f"{DG_MAX_REPAIR_ROUNDS} permitted repair round(s)."),
                'remedy': f"set repair_rounds_used to {DG_MAX_REPAIR_ROUNDS}."}
    if st == 'PASSED' and not (0 <= n <= DG_MAX_REPAIR_ROUNDS):
        return {'field': 'repair_rounds_used', 'from': n, 'to': DG_MAX_REPAIR_ROUNDS,
                'explanation': f"PASSED admits 0..{DG_MAX_REPAIR_ROUNDS} only.",
                'remedy': f"clamp repair_rounds_used to {DG_MAX_REPAIR_ROUNDS}."}
    return {'field': 'status', 'from': st, 'to': None,
            'explanation': f"status {st!r} is not one of {sorted(DG_STATUSES)}.",
            'remedy': ("NO AUTOMATIC REPAIR — an unknown status cannot be interpreted. "
                       "Escalate: the registry was written by an out-of-contract tool "
                       "or a newer framework release.")}


def dg_assert_legal(reg, paper_id, where):
    """Strict form: returns the record (None for legacy) or raises DGIllegalState with
    the exact one-field remedy. Use dg_preflight for the healing form every step
    preflight calls; this is for auditors and tests."""
    rec = dg_read(reg, paper_id)
    if rec is None or dg_is_legal(rec):
        return rec
    st, n = dg_state(rec)
    fix = dg_diagnose_illegal(rec)
    raise DGIllegalState(
        f"HARD STOP ({where}): difficulty_gate[{paper_id}] is in an ILLEGAL state "
        f"status={st!r} repair_rounds_used={n}. No step in the framework can produce "
        f"this pair ({DG_GAP_ID}). {fix['explanation']} REMEDY: {fix['remedy']}")


def dg_migrate(reg, paper_id):
    """Idempotent, in-place heal of a legacy/corrupt record. Returns a disclosure dict
    (None if nothing needed healing) that the caller MUST surface in chat and that the
    delivery footer prints (dg_footer_lines reads rec['migrations']). NEVER silent: a
    healed registry that looks identical to a clean one is the failure mode this gap is
    about. An unknown status RAISES — it is never guessed at."""
    rec = dg_read(reg, paper_id)
    if rec is None:
        return None
    if dg_is_legal(rec):
        if rec.get('schema') != DG_SCHEMA:
            rec['schema'] = DG_SCHEMA         # v1 → v2 shape upgrade only; values untouched
        return None
    fix = dg_diagnose_illegal(rec)
    if fix['to'] is None:
        raise DGIllegalState(f"difficulty_gate[{paper_id}]: {fix['explanation']} {fix['remedy']}")
    before = dg_state(rec)
    rec[fix['field']] = fix['to']
    rec['schema'] = DG_SCHEMA
    entry = {'gap': DG_GAP_ID, 'field': fix['field'], 'from': fix['from'],
             'to': fix['to'], 'at': _dg_now()}
    rec.setdefault('migrations', []).append(entry)
    if not dg_is_legal(rec):
        raise DGIllegalState(f"dg_migrate produced an illegal state for {paper_id}: "
                             f"{dg_state(rec)} (was {before})")
    return {'paper_id': paper_id, 'field': fix['field'], 'from': fix['from'],
            'to': fix['to'], 'explanation': fix['explanation'], 'remedy': fix['remedy'],
            'line': (f"⚠ REGISTRY HEALED ({DG_GAP_ID}): difficulty_gate[{paper_id}]."
                     f"{fix['field']} {fix['from']} → {fix['to']}. {fix['explanation']}")}


def dg_preflight(reg, paper_id, where):
    """THE FIRST CALL of every preflight that reads the record (MockTestCreate §S16-1
    P0, MockTestExplain §7A-M / §7A-R R0, MockDeliver S1-2 3b). Heals a corrupt record
    per DG-INVARIANT with mandatory disclosure (operator decision D3 of the gap: the
    repair is provably unique and the operator is non-technical), refuses an
    uninterpretable one. Returns (rec_or_None, disclosure_or_None). The caller MUST
    print disclosure['line'] when it is not None and MUST persist the registry."""
    disclosure = dg_migrate(reg, paper_id)          # raises on unknown status
    rec = dg_assert_legal(reg, paper_id, where)     # cannot raise after a successful migrate
    return rec, disclosure


# ── the three permitted writers ──────────────────────────────────────────────────
def dg_stamp_pending(reg, paper_id, threshold=DG_DEFAULT_THRESHOLD):
    """final_assembly.commit_registry ONLY, at paper commit. The ONLY place a record is
    CREATED. A MOCK paper is born PENDING (Step 11 refuses it until Step 9's gate has
    run). A SCOPED paper (any non-MOCK paper_id) is born DORMANT/scoped_paper: §7A-M is
    MOCK-ONLY by title, so a scoped paper stamped PENDING could never be resolved and
    could never be delivered (gap defect G-4 — measured on every scoped paper in every
    project). Writing the terminal verdict at birth makes a scoped paper deliverable
    even if a Step-9 session never touches the record. A fresh commit REPLACES any
    prior record for the same paper_id: a regenerated paper is a new paper, and a
    stale rework_stem_hashes snapshot from a previous cycle would falsely accuse it."""
    scoped = paper_prefix(paper_id) != 'MOCK'
    rec = {'schema': DG_SCHEMA,
           'status': 'DORMANT' if scoped else 'PENDING',
           'threshold': threshold, 'repair_rounds_used': 0}
    if scoped:
        rec['dormant_reason'] = 'scoped_paper'
        rec['timestamp'] = _dg_now()
    assert dg_is_legal(rec)
    reg.setdefault('difficulty_gate', {})[paper_id] = rec
    return rec


def dg_is_windowed(rec):
    """True when a record's verdict was produced under the windowed rule
    (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS): rec['gate_rule'] == DG_RULE_WINDOWS,
    stamped by dg_write_verdict. PENDING/DORMANT/legacy/absent → False (nothing to
    repair anyway). A FAILED record that is NOT windowed carries a rework list the
    operator retired; dg_next_step routes it to TestExplain, dg_add_rework_snapshot
    refuses it."""
    return isinstance(rec, dict) and rec.get('gate_rule') == DG_RULE_WINDOWS


def dg_write_verdict(reg, paper_id, *, status, rounds, threshold=None, bands=None,
                     measured_by_q=None, rework_qs=None, dormant_reason=None,
                     scores_by_q=None, rework_directions=None, windows=None):
    """Step 9 ONLY (§7A-M first gate: rounds=0; §7A-R re-gate: rounds=1). The ONLY
    writer of `status` and `repair_rounds_used` after birth, and it writes them
    TOGETHER — which is what makes (FAILED, 1) unreachable and DG-INVARIANT true.

    TERMINAL AND ATOMIC (gap defect G-6): call ONCE, at the END of a successful gate
    or re-gate, never on entry. A crashed repair therefore leaves (FAILED, 0) and is
    simply re-run; rework_stem_hashes is carried forward untouched, so §7A-R R3 still
    validates against the pre-repair snapshot.

    ROUND-MONOTONIC (edge case E16): a §7A-M re-run (rounds=0) on a record whose round
    is already spent keeps the spent count, and a FAIL on a spent round resolves to
    DISCLOSED — a paper can never be handed a second repair round by re-running the
    full explain. The carry is recorded in rec['rounds_carried_from'].

    WINDOWED RULE (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS): pass the gate result's
    scores_by_q (raw rubric scores → 'measured_score_by_q'), rework_directions
    ({q: 'harder'|'easier'} → Step 7 §S16 reads which way to rewrite) and windows
    (gate['windows'], the per-position acceptance windows the verdict was judged
    by). A PASSED/FAILED/DISCLOSED verdict carrying `windows` is stamped
    rec['gate_rule'] = DG_RULE_WINDOWS; a FAILED verdict WITHOUT windows is refused
    (the band-equality rule is retired — no new record may be written under it).
    rework_directions must cover every rework q (a partial map is a caller bug).

    Raises DGIllegalState rather than write an illegal pair. NEVER build this dict by
    hand in a spec."""
    if status not in DG_STATUSES:
        raise DGIllegalState(f"unknown difficulty_gate status {status!r} for {paper_id}; "
                             f"legal: {sorted(DG_STATUSES)}")
    if status == 'DORMANT' and dormant_reason not in DG_DORMANT_REASONS:
        raise DGIllegalState(f"DORMANT requires dormant_reason from {DG_DORMANT_REASONS}, "
                             f"got {dormant_reason!r}")
    prev = dg_read(reg, paper_id) or {}
    prev_rounds = dg_state(prev)[1] if prev else 0
    rounds = int(rounds)
    carried = None
    if status == 'DORMANT' and prev_rounds >= DG_MAX_REPAIR_ROUNDS and dg_is_legal(prev):
        # A post-repair terminal verdict (PASSED/1, DISCLOSED/1) is a quality finding;
        # a later dormant re-run (e.g. blueprint_core missing in that session) must
        # not erase it. Idempotent no-op — the record is returned unchanged.
        return prev
    if prev_rounds > rounds and status in ('PASSED', 'FAILED'):
        carried, rounds = prev_rounds, prev_rounds
        if status == 'FAILED' and rounds >= DG_MAX_REPAIR_ROUNDS:
            status = 'DISCLOSED'
    if (status, rounds) not in DG_LEGAL_STATES:
        raise DGIllegalState(
            f"refusing to write illegal difficulty_gate state ({status!r}, {rounds}) "
            f"for {paper_id}. Legal: {sorted(DG_LEGAL_STATES)}")
    rec = {'schema': DG_SCHEMA, 'status': status,
           'threshold': (prev.get('threshold', DG_DEFAULT_THRESHOLD)
                         if threshold is None else threshold),
           'repair_rounds_used': rounds}
    if dormant_reason:
        rec['dormant_reason'] = dormant_reason
    if bands is not None:
        rec['bands'] = bands
    if measured_by_q is not None:
        rec['measured_by_q'] = {str(q): m for q, m in measured_by_q.items() if m is not None}
    if rework_qs is not None:
        rec['rework_qs'] = sorted(int(q) for q in rework_qs)
    if status in ('PASSED', 'FAILED', 'DISCLOSED'):
        if windows is None:
            if status == 'FAILED':
                raise DGIllegalState(
                    f"refusing to write a FAILED difficulty_gate verdict for {paper_id} "
                    f"without `windows`: the band-equality rule is retired "
                    f"(GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS); pass gate['windows'] "
                    f"from bc.evaluate_difficulty_gate")
        else:
            if (not isinstance(windows, (list, tuple)) or len(windows) != 3
                    or any(w is not None and (not isinstance(w, (list, tuple)) or len(w) != 2)
                           for w in windows)):
                raise DGIllegalState(f"windows must be the gate's 3-entry list of None|[lo, hi], "
                                     f"got {windows!r}")
            rec['windows'] = [None if w is None else [w[0], w[1]] for w in windows]
            rec['gate_rule'] = DG_RULE_WINDOWS
    if scores_by_q is not None:
        _scores = {}
        for q, v in scores_by_q.items():
            if v is None or isinstance(v, bool):
                continue                          # None = not measurable; bool is never a score
            try:
                _iv = int(v)
                if isinstance(v, float) and v != _iv:
                    raise ValueError
            except (TypeError, ValueError, OverflowError):
                raise DGIllegalState(f"measured score for Q{q} is not an integer: {v!r}")
            _scores[str(q)] = _iv
        rec['measured_score_by_q'] = _scores
    if rework_directions is not None:
        _dirs = {str(q): d for q, d in rework_directions.items()}
        _bad = sorted(q for q, d in _dirs.items() if d not in ('harder', 'easier'))
        if _bad:
            raise DGIllegalState(f"rework_directions must be 'harder'|'easier'; bad: {_bad}")
        _missing = sorted(set(str(q) for q in rec.get('rework_qs') or []) - set(_dirs))
        if _missing:
            raise DGIllegalState(f"rework_directions missing for rework_qs {_missing}")
        rec['rework_directions'] = _dirs
    elif status == 'FAILED' and rec.get('rework_qs'):
        raise DGIllegalState(f"FAILED verdict for {paper_id} needs rework_directions for "
                             f"{rec['rework_qs']} (windowed rule)")
    rec['timestamp'] = _dg_now()
    if carried is not None:
        rec['rounds_carried_from'] = carried
    # Step-7-repair evidence and the audit trail survive every re-gate ...
    for keep in ('rework_stem_hashes', 'baseline_stem_hashes', 'migrations'):
        if keep in prev:
            rec[keep] = prev[keep]
    # ... EXCEPT that a FRESH round-0 verdict (a full §7A-M re-run, or the re-judge
    # of a retired-rule record — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS) starts a
    # new repair lineage. A pre-repair stem snapshot taken for the OLD rework set
    # would (a) make §7A-R R3 falsely accuse a correct repair file of touching the
    # wrong questions and (b) fail A-DGATE check 5 (snapshot keys ≠ rework_qs). It
    # is kept only when the new verdict names EXACTLY the same rework set (the same
    # order continues); otherwise it is retired to rec['superseded_snapshots'] and
    # a later TestCreateRepair takes a fresh one. Never on a carried (spent) round:
    # the repair evidence for that round stays intact.
    if (carried is None and rounds == 0 and status in ('PASSED', 'FAILED')
            and prev.get('rework_stem_hashes')):
        _snap_keys = set(str(q) for q in prev['rework_stem_hashes'])
        _new_keys = set(str(q) for q in (rec.get('rework_qs') or []))
        if _snap_keys != _new_keys:
            rec.pop('rework_stem_hashes', None)
            rec.pop('baseline_stem_hashes', None)
            rec['superseded_snapshots'] = list(prev.get('superseded_snapshots') or []) + [
                {'rework_qs': sorted(_snap_keys, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else 0, x)),
                 'retired_at': _dg_now(), 'reason': 'fresh_round0_verdict_with_different_rework_set'}]
    reg.setdefault('difficulty_gate', {})[paper_id] = rec
    return rec


def dg_add_rework_snapshot(reg, paper_id, stem_hashes, all_stem_hashes=None):
    """TestCreateRepair (MockTestCreate §S16-3) ONLY. Adds the PRE-repair stem
    snapshot and NOTHING else — status and repair_rounds_used are byte-untouched.
    WRITE-ONCE (gap defect G-8): a second call is a no-op returning the original,
    because a re-run of TestCreateRepair would otherwise hash the ALREADY-REPAIRED
    stems, destroy the evidence and make §7A-R R3 falsely accuse a correct file.
    Refuses unless the record is exactly (FAILED, 0): a snapshot on any other state
    means a repair is being attempted where none is owed."""
    rec = dg_read(reg, paper_id)
    if rec is None:
        raise DGIllegalState(f"no difficulty_gate record for {paper_id} — run TestExplain first "
                             f"(or this is a legacy paper; deliver as usual)")
    if dg_state(rec)[0] != 'FAILED' or not dg_is_legal(rec):
        raise DGIllegalState(f"rework snapshot may only be written on a legal FAILED record; "
                             f"{paper_id} is {dg_state(rec)}")
    if not dg_is_windowed(rec):
        raise DGIllegalState(
            f"{paper_id} was judged FAILED under the retired band-equality rule "
            f"(GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS); its rework list is not an order. "
            f"Run TestExplain / MockExplain on this paper so the verdict is re-judged "
            f"under the acceptance windows, then return here only if it still fails.")
    if rec.get('rework_stem_hashes'):
        return rec['rework_stem_hashes']                       # write-once no-op
    rec['rework_stem_hashes'] = {str(q): h for q, h in stem_hashes.items()}
    if all_stem_hashes:
        # PRE-repair digest of EVERY question (write-once, same call). This is what
        # lets §7A-R R3 detect a question changed OUTSIDE rework_qs (gap case E20) —
        # rework_stem_hashes alone can only prove the flagged ones changed.
        rec['baseline_stem_hashes'] = {str(q): h for q, h in all_stem_hashes.items()}
    return rec['rework_stem_hashes']


# ── the shared stem digest (gap defect G-9): ONE implementation, both sides call it ──
def dg_stem_hash(stem_paragraph_text):
    """sha256 of the RAW first paragraph of a question region.
    EXACT DEFINITION — TestCreateRepair (§S16-3) and TestExplainRepair (§7A-R R3) both
    call THIS function, never their own:
      • text = concatenation of every <w:t> descendant of the question's FIRST <w:p>,
        in document order;
      • the "Q.<n>" label is INCLUDED;
      • NO whitespace normalisation, NO case folding, NO stripping;
      • UTF-8 bytes, lowercase hex digest.
    Verified 32/32 against the live IIT_JAM_CHEMISTRY Mock 1 snapshot (0/32 for every
    normalised variant). The self-test pins the digest of a fixed string so the
    algorithm cannot drift across releases."""
    import hashlib                  # local: thin core (CHECK AB)
    return hashlib.sha256(stem_paragraph_text.encode('utf-8')).hexdigest()


def dg_verify_repair(rec, repaired_stem_texts_by_q):
    """§7A-R R3 as one call. repaired_stem_texts_by_q: {q: first-paragraph text of the
    REPAIRED paper}. Returns {'ok', 'changed', 'unchanged_listed', 'changed_unlisted',
    'missing_snapshot'}; ok is True iff the changed set == rework_qs exactly. Compares
    ONLY against rec['rework_stem_hashes'] (the pre-repair snapshot) — never against
    registry.stem_texts, which TestCreateRepair has already overwritten."""
    snap = rec.get('rework_stem_hashes') or {}
    rework = sorted(int(q) for q in rec.get('rework_qs') or [])
    if not snap:
        return {'ok': False, 'changed': [], 'unchanged_listed': rework,
                'changed_unlisted': [], 'missing_snapshot': True,
                'extras_verifiable': False}
    # baseline (every question) when the snapshot carries it; rework-only otherwise
    base = dict(rec.get('baseline_stem_hashes') or {})
    base.update(snap)
    changed = sorted(int(q) for q, t in repaired_stem_texts_by_q.items()
                     if str(q) in base and dg_stem_hash(t) != base[str(q)])
    unchanged_listed = sorted(q for q in rework if q not in changed)
    changed_unlisted = sorted(q for q in changed if q not in rework)
    return {'ok': not unchanged_listed and not changed_unlisted and bool(rework),
            'changed': changed, 'unchanged_listed': unchanged_listed,
            'changed_unlisted': changed_unlisted, 'missing_snapshot': False,
            'extras_verifiable': bool(rec.get('baseline_stem_hashes'))}


# ── the single source for next-step advice (gap defect G-3) ─────────────────────
def dg_next_step(reg, paper_id, n, *, mock):
    """The ONE place a next-step command is derived. Every spec that prints a next
    command calls this instead of restating the rule, so §7A-R can never again send an
    operator to a step that is guaranteed to refuse. Reads the SAME record Step 11
    reads. Raises on an illegal record — call dg_preflight first."""
    t, p = ('Mock', 'M') if mock else ('Test', 'P')
    rec = dg_read(reg, paper_id)
    if rec is None:
        return f"{t}Deliver {p}{n}"
    if not dg_is_legal(rec):
        raise DGIllegalState(f"dg_next_step called on an illegal record for {paper_id} "
                             f"{dg_state(rec)} — call dg_preflight first")
    st, _ = dg_state(rec)
    if st in DG_DELIVERABLE:
        return f"{t}Deliver {p}{n}"
    if st == 'PENDING':
        return f"{t}Explain {p}{n}   (attach the question paper)"
    if not dg_is_windowed(rec):
        # FAILED under the retired band-equality rule: re-judge, never repair
        return (f"{t}Explain {p}{n}   (attach the question paper — this paper was judged "
                f"under the old difficulty rule; the verdict is re-judged under the windows)")
    qs = ' '.join(f"Q{q}" for q in rec.get('rework_qs') or [])
    return (f"{t}CreateRepair {p}{n} {qs}".rstrip()
            + f"\n   then: {t}ExplainRepair {p}{n}")


def dg_deliver_decision(reg, paper_id, n, *, mock):
    """MockDeliver S1-2 3b as one call. Returns {'deliver': bool, 'state', 'reason',
    'next_step', 'footer_lines'} from a record that MUST already be legal (call
    dg_preflight first). The gate reads ONLY the registry — never the chat."""
    rec = dg_read(reg, paper_id)
    if rec is None:
        return {'deliver': True, 'state': None, 'reason': 'LEGACY paper (pre-gate) — '
                'deliver exactly as before (operator decision 2026-08-24)',
                'next_step': None, 'footer_lines': []}
    st, r = dg_state(rec)
    if (st, r) not in DG_LEGAL_STATES:
        raise DGIllegalState(f"dg_deliver_decision on an illegal record {dg_state(rec)} "
                             f"for {paper_id} — call dg_preflight first")
    if st in DG_DELIVERABLE:
        return {'deliver': True, 'state': (st, r), 'reason': f'{st}/{r}',
                'next_step': None, 'footer_lines': dg_footer_lines(rec)}
    return {'deliver': False, 'state': (st, r),
            'reason': ('Step 9 never ran its gate' if st == 'PENDING'
                       else 'difficulty gate FAILED — repair round available' if dg_is_windowed(rec)
                       else 'difficulty gate FAILED under the retired band-equality rule — '
                            're-run the explain step to re-judge'),
            'next_step': dg_next_step(reg, paper_id, n, mock=mock), 'footer_lines': []}


def dg_footer_lines(rec):
    """§FOOTER-DG: the ONLY source of the difficulty-gate footer lines (Framework_
    DeliveryFooter §FOOTER-DG). Shape is a function of status (schema 2):
      DISCLOSED   → measured band counts after the repair round (from bands)
      DORMANT     → not-applicable line with the reason
      any + migrations → one healed-registry disclosure line per migration
    PASSED emits no gate line. Returns a list (possibly empty)."""
    if rec is None:
        return []
    lines = []
    st, r = dg_state(rec)
    if st == 'DISCLOSED':
        bands = rec.get('bands') or {}
        # windowed rule: an ungated band (gated False) prints its size and "(not gated)";
        # a gated band prints agree/total "in window". Pre-window records keep the
        # plain fraction they were written under.
        parts = []
        for lab, b in bands.items():
            b = b or {}
            if dg_is_windowed(rec):
                if b.get('gated') is False:
                    parts.append(f"{lab} {b.get('total', '?')} (not gated)")
                else:
                    parts.append(f"{lab} {b.get('agree', '?')}/{b.get('total', '?')} in window")
            else:
                parts.append(f"{lab} {b.get('agree', '?')}/{b.get('total', '?')}")
        lines.append("Measured difficulty: " + " · ".join(parts)
                     + f" confirmed after {r} repair round{'s' if r != 1 else ''}.")
    elif st == 'DORMANT':
        lines.append(f"Difficulty gate: not applicable to this paper "
                     f"({rec.get('dormant_reason', 'unspecified')}) — labels are as planned at Step 7.")
    for m in rec.get('migrations') or []:
        lines.append(f"Difficulty-gate record healed ({m.get('gap', DG_GAP_ID)}): "
                     f"{m.get('field')} {m.get('from')} → {m.get('to')} on {m.get('at', '?')[:10]}.")
    return lines


# ── fleet recovery (gap §9) — pure core; the I/O wrapper lives in __main__ ────────
def dg_fleet_heal(reg, *, apply):
    """Scan one registry dict. Returns {'illegal': [...], 'healed': [...],
    'stuck_scoped': [...], 'pending': [...], 'escalate': [...], 'changed': bool}.
    With apply=True, heals in place via dg_migrate (disclosed in rec['migrations'])
    and converts a PENDING scoped paper to DORMANT/scoped_paper (cohort B of the gap).
    Unknown statuses are reported under 'escalate' and never touched."""
    out = {'illegal': [], 'healed': [], 'stuck_scoped': [], 'pending': [],
           'escalate': [], 'changed': False}
    for pid, rec in list((reg.get('difficulty_gate') or {}).items()):
        st, n = dg_state(rec)
        if (st, n) not in DG_LEGAL_STATES:
            fix = dg_diagnose_illegal(rec)
            if fix['to'] is None:
                out['escalate'].append((pid, st, n))
                continue
            out['illegal'].append((pid, st, n, fix['field'], fix['from'], fix['to']))
            if apply:
                dg_migrate(reg, pid)
                out['healed'].append(pid)
                out['changed'] = True
                st, n = dg_state(rec)              # fall through: a healed scoped PENDING is still stuck
            else:
                continue
        if st == 'PENDING':
            if paper_prefix(pid) != 'MOCK':
                out['stuck_scoped'].append(pid)
                if apply:
                    prev_keys = {k: v for k, v in rec.items()
                                 if k in ('rework_stem_hashes', 'baseline_stem_hashes', 'migrations')}
                    rec.clear()
                    rec.update({'schema': DG_SCHEMA, 'status': 'DORMANT',
                                'threshold': DG_DEFAULT_THRESHOLD, 'repair_rounds_used': 0,
                                'dormant_reason': 'scoped_paper', 'timestamp': _dg_now()})
                    rec.update(prev_keys)
                    rec.setdefault('migrations', []).append(
                        {'gap': DG_GAP_ID, 'field': 'status', 'from': 'PENDING',
                         'to': 'DORMANT/scoped_paper', 'at': _dg_now()})
                    if pid not in out['healed']:
                        out['healed'].append(pid)
                    out['changed'] = True
            else:
                out['pending'].append(pid)
    return out


if __name__ == '__main__':
    import sys
    sys.exit(0 if _self_test() else 1)
