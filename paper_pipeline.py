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

    Offsets: mocks[].mock, mocks[].paper_id, and difficulty_schedule[].mock (Step 8 looks up
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

    def ck(name, cond):
        nonlocal p, f
        if cond:
            p += 1
        else:
            f += 1
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

    print(f"SELF-TEST: {p}/{p + f} PASS" + ("" if not f else f"  ({f} FAILED)"))
    return f == 0


if __name__ == '__main__':
    import sys
    sys.exit(0 if _self_test() else 1)
