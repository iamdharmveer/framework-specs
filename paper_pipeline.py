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
    # while Step 8 classified the family as 'roman' — A-OPTLABEL then FAILED every
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

    # THE SYNC INVARIANT: Step 7's render family must equal Step 8's classification
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
# template Step 7 emits with AND the label family Step 8 audits against.
#
# WHY IT LIVES HERE. Before v5.37 the two steps derived this INDEPENDENTLY:
# Step 7 by testing the leading token's CASING inside a spec code block, Step 8 by
# a regex family classifier in audit_canonical. They disagreed, and the disagreement
# was a guaranteed halt:
#     section_rules 'i/ii/iii/iv'
#        Step 7  -> .islower() is True for 'i'  -> ({alpha_lower}) -> renders (a)(b)(c)(d)
#        Step 8  -> option_label_family        -> 'roman'
#        result  -> A-OPTLABEL FAIL on EVERY question, exit 1, MANDATE D blocks
#                   delivery, and NO CP repair can fix it because the paper matches
#                   Step 7's own contract. Measured end-to-end.
# paper_pipeline is routed by BOTH TestCreate and TestCreateAudit, so one function
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
            f"delivered paper and Step 8 then fails every question against the "
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
    # In both cases Step 8 would fail every question on a paper that obeys Step 7.
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
            f"render it as {_tok_family!r} labels (e.g. {template!r}) while Step 8's "
            f"option_label_family classifies it as {_audit_family!r}. Step 8 would "
            f"then FAIL A-OPTLABEL on every question of a paper that obeys Step 7, "
            f"with no repair possible. Declare an unambiguous notation "
            f"('1/2/3/4', 'A/B/C/D', 'a/b/c/d', 'i/ii/iii/iv', 'I/II/III/IV', or "
            f"those in round brackets) — this is NEVER guessed at.")
    return (template, _tok_family)


if __name__ == '__main__':
    import sys
    sys.exit(0 if _self_test() else 1)
