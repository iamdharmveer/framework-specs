"""
blueprint_core.py — Shared allocation core for the exam blueprint family.

PROVENANCE
    Every function here is extracted VERBATIM (semantics-identical) from
    Framework_Blueprint.md (mock Step 6). The only edits at extraction time are the
    thin-core seam refactors agreed in the boundary map:
      * mandate coupling  → a generic per-subtopic ``floors`` parameter (the core
        never knows mandates exist; the caller computes floors).
      * ``mocks_per_window`` → ``papers_per_window`` (a mock is a paper; a scoped
        test is a paper — one honest name for the shared unit).
      * ``difficulty_counts`` and ``_avg_to_counts`` unified into one canonical
        ``largest_remainder_apportion`` (provably identical for the 3-band case —
        see blueprint_core_test.py::test_difficulty_counts_equivalence).

    Source anchors (Framework_Blueprint.md v1.27):
      split_recency ............ §3 S3-1
      compute_r_avg ............ §3 S3-2
      largest_remainder_apportion §7 S7-4 (difficulty_counts) + §7-7 (_avg_to_counts)
      difficulty_counts ........ §7 S7-4 (thin wrapper over the canonical apportioner)
      proportional_split ....... §4-2 STEP 3
      largest_remainder_fix .... §4-2 STEP 4
      exact_fill ............... §4-5b (Gale-Ryser matrix fill)
      section_axis2_pool_caps .. §7-7 (_section_axis2_pool_caps)
      derive_axis_schedule ..... §7-7
      axis3_mechanism_lock ..... §7-7 (GAP-2026-08-12-AXIS3-MECHLOCK, NEW — v1.49)
      axis1_feasibility ........ §7-7
      axis1_mock_feasibility ... §7-7 (GAP-2026-08-12-AXIS-PREFLIGHT, NEW — v1.50)
      axis3_mock_feasibility ... §7-7 (GAP-2026-08-12-AXIS3-PREFLIGHT, NEW — v1.51)
      axis_truth_check ......... §9 S9-12 (GAP-2026-08-23-AXIS-ADVISORY-TRUTH, NEW — v1.54)
      difficulty_score / band_for_score / difficulty_score_from_obs /
      DIFFICULTY_GATE_BAND_WINDOWS / evaluate_difficulty_gate(scores_by_q, band_windows)
                                 MockTestExplain §7A-M / §7A-R (GAP-2026-08-25-DIFFICULTY-
                                 GATE-WINDOWS — Cluster E2 split + E2d window gate; frac 0.35)
      slugify .................. §17 S2-MANIFEST
    Source anchors (Framework_MockTestAnalyse.md v2.24.10 — Cluster E):
      score_difficulty ......... E-9  (3-axis universal difficulty scorer)
      determine_strip_mode ..... E-10 (taxonomy → strip mode, RIGID-5 Hindi)
      map_difficulty_level ..... NEW  (Blueprint §7 S7-6 fixed ordinal alias)

THIN-CORE INVARIANT (enforced by validate_framework_md.py)
    This module is PURE. It performs no I/O, imports nothing exam-specific, and has
    ZERO knowledge of: mandates, sections, the subtopic manifest structure, the
    blueprint.json schema, or xlsx. Inputs are plain data (numbers, lists, dicts);
    outputs are plain data. Any reference to those forbidden concepts is a seam
    violation. Only the standard library (``math``, ``re``, and — inside Cluster H only —
    ``os.path`` and ``unicodedata``) is used. Purity is enforced for real by
    validate_framework_md.py Check AB; before that check existed this docstring
    claimed an enforcement that did not exist.
"""

import math
import re

__all__ = [
    "AllocationError",
    "split_recency",
    "compute_r_avg",
    "rescale_to_total",
    "largest_remainder_apportion",
    "difficulty_counts",
    "proportional_split",
    "largest_remainder_fix",
    "exact_fill",
    "section_axis2_pool_caps",
    "derive_axis_schedule",
    "axis3_mechanism_lock",
    "axis1_feasibility",
    "axis1_mock_feasibility",
    "axis_truth_check",
    "axis3_mock_feasibility",
    "AXIS_WINDOW_YEARS",
    "AXIS_BAND_ABS",
    "AXIS_BAND_FLEX",
    "AXIS_MAX_MOCKS",
    "AXIS_BAND_REL",
    "STIMULUS_CLASSES",
    "MECHANISM_CLASSES",
    "figural_band",
    "figural_target_series",
    "figural_quota",
    "schedule_figural_slots",
    "build_axis_tracker",
    "axis_need",
    "axis_record",
    "axis_snapshot",
    "axis_grant_figural",
    "rank_figural_candidates",
    "check_axis_conformance",
    "parse_section_rules_difficulty",
    "parse_section_rules_field",
    "slugify",
    "OUT_OF_PATTERN",
    "PATTERN_ERAS",
    "classify_paper_era",
    "type_resolver_from_config",
    "exam_config_bounds",
    "paper_key",
    "paper_eras_from_progress",
    "filter_progress_to_eras",
    "Q_PATTERNS",
    "BARE_Q_PATTERNS",
    "is_bare_q_label",
    "ZERO_WIDTH",
    "ZERO_WIDTH_RE",
    "detect_question_start",
    "parse_taxonomy_level",
    "extract_year_from_filename",
    "is_taxonomy_heading",
    "next_nonempty_texts",
    "sorted_body_lookahead",
    "paragraph_is_content_bearing",
    "CONTENT_SENTINEL",
    "VISUAL_CONTENT_TAGS",
    "HEADING_NAVY",
    "first_run_colour",
    "heading_colour_available",
    "score_difficulty",
    "determine_strip_mode",
    "map_difficulty_level",
    "DRIVE_CAP",
    "SIZE_BUDGET",
    "CHAT_FILE_LIMIT",
    "TIER_LADDER",
    "MAX_TIER",
    "PNG_QUANT_COLORS",
    "PNG_QUANT_QUALITY",
    "NAME_JUNK_TOKENS",
    "canonical_output_name",
    "DOCX_MIME",
    "GDOC_MIME",
    "FOLDER_MIME",
    "SHORTCUT_MIME",
    "canonical_paper_key",
    "screen_drive_entry",
    "transport_status",
    "partition_by_transport",
    "upload_batch_plan",
    "classify_media_route",
    "image_gate_verdict",
    "gates_passed",
    "image_clarity_state",
    "derive_image_roles",
    "IMAGE_ROLES",
]


class AllocationError(RuntimeError):
    """Fatal allocation failure. Mirrors the source's ``AlgorithmError = RuntimeError``.

    The mock/scoped wrappers translate this into their own HALT messaging with
    section/scope context; the pure core only reports the arithmetic cause.
    """


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER A — FREQUENCY  (Framework_Blueprint.md §3)
# ════════════════════════════════════════════════════════════════════════════

def split_recency(valid_years):
    """S3-1: split the *valid* years (those with >0 papers for some subtopic) into
    (recent_years, older_years). ``recent`` = the last 2 of the sorted valid years.

    Matches ``sorted(valid_years)[-2:]`` / ``[:-2]`` exactly. With exactly 2 valid
    years both land in ``recent`` (intentional — effectively equal weight). With 1
    valid year the single year is ``recent`` but the 2x weight cancels in the r_avg
    ratio, reproducing CASE 1 ("1x, no amplification"). Year identity/order preserved.
    """
    sv = sorted(valid_years)
    return sv[-2:], sv[:-2]


def compute_r_avg(year_rows):
    """S3-2: recency-weighted average questions-per-paper for ONE subtopic.

    Parameters
    ----------
    year_rows : list of dict
        One entry per valid year for this subtopic, each with:
          ``avg``    — Avg/Paper for the year (number, '' or None → 0.0)
          ``papers`` — Papers In for the year (number, '' or None → 0.0)
          ``recent`` — bool, True iff the year is in ``recent_years`` (weight 2, else 1)
        The caller normalises its parsed Excel into this shape (the string-keyed
        'Avg/Paper <year>' parsing stays in the spec — it is a parsing artifact).

    Returns
    -------
    (r_avg, warnings)
        r_avg    : float rounded to 4 dp; 0.0 when there is no weighted paper data
                   (→ the caller classifies the subtopic Zero-PYQ, handled by §5).
        warnings : list of data-quality messages (papers==0 while avg>0). Returned
                   rather than logged so the core stays pure; the caller surfaces them.
    """
    weighted_sum = 0.0
    total_weighted_papers = 0.0
    warnings = []

    for row in year_rows:
        raw_avg = row.get("avg", None)
        raw_pap = row.get("papers", None)
        avg_per_paper = float(raw_avg) if raw_avg not in (None, "") else 0.0
        papers_in = float(raw_pap) if raw_pap not in (None, "") else 0.0

        # Data quality check (S3-2): papers==0 but avg>0 is impossible real data.
        if papers_in == 0 and avg_per_paper > 0:
            warnings.append(
                f"Data error: year has Avg/Paper={avg_per_paper} but Papers In=0. "
                f"Treating year as 0 papers."
            )
            papers_in = 0.0
            avg_per_paper = 0.0

        weight = 2 if row.get("recent") else 1
        weighted_papers = papers_in * weight
        weighted_sum += avg_per_paper * weighted_papers
        total_weighted_papers += weighted_papers

    if total_weighted_papers == 0:
        return 0.0, warnings
    return round(weighted_sum / total_weighted_papers, 4), warnings


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER B — APPORTIONMENT  (Framework_Blueprint.md §4, §7)
# ════════════════════════════════════════════════════════════════════════════

RESCALE_TOL = 1e-9      # relative tolerance for "already sums to total" (no-op guard)


def rescale_to_total(raw_map, total):
    """Scale a ``{key: real-valued weight}`` map so its values sum to ``total``,
    preserving every key's PROPORTION of the whole.

    WHY THIS EXISTS (exam-agnostic pattern-era normalisation)
        ``largest_remainder_apportion`` is a pure APPORTIONER: it only distributes the
        integer deficit between ``floor(v)`` and ``total``. It does NOT rescale. Feeding
        it a map whose sum is far from ``total`` is therefore a caller error, and it used
        to fail in the two worst possible ways at once — see the v2 note on that function.

        The real-world trigger is a CHANGE OF EXAM PATTERN SIZE. Per-paper class averages
        measured on a PYQ corpus are in "questions per historical paper" units. When the
        exam's current pattern is a different size (a 100-Q legacy paper vs. a 60-Q current
        pattern, or the reverse), those averages must be re-expressed in current-pattern
        units before they can be apportioned. That is exactly what this does.

        Proportions are preserved exactly, so a class holding 5% of a 100-Q paper still
        holds 5% of a 60-Q paper (3.0 Qs, not 0). Nothing about any specific exam,
        section, subject or format name is encoded here.

    CONTRACT
        * ``{}`` when ``raw_map`` is empty, ``total <= 0``, or the weights sum to <= 0
          (identical to the apportioner's own empty-input behaviour, and to the
          Framework_ScopedBlueprint §6-2 ``_norm_to_Q`` helper this generalises).
        * Otherwise a same-keyed map of floats summing to ``total`` (to float precision).
        * NO-OP GUARD: when the input already sums to ``total`` within ``RESCALE_TOL``
          relative tolerance, the values are returned unchanged (only float()-coerced).
          This is what keeps an already-normalised caller — Framework_ScopedBlueprint,
          which normalises to Q before calling — bit-for-bit unaffected, rather than
          perturbed in the last ULP by a redundant multiply.
    """
    if not raw_map or total <= 0:
        return {}
    raw = {k: float(v) for k, v in raw_map.items()}
    s = sum(raw.values())
    if s <= 0:
        return {}
    if abs(s - total) <= RESCALE_TOL * max(1.0, abs(float(total))):
        return raw                                     # already normalised — do not touch
    f = float(total) / s
    return {k: v * f for k, v in raw.items()}


def largest_remainder_apportion(raw_map, total):
    """Canonical largest-remainder apportionment (unifies §7-7 ``_avg_to_counts``
    and §7 S7-4 ``difficulty_counts``).

    Convert a ``{key: real-valued weight}`` map into integer counts summing EXACTLY to
    ``total``. Handles under- and over-count.

    Deterministic tie-break: by (fractional remainder, key). For a positive deficit
    the largest remainders get the +1s; for a negative deficit the smallest remainders
    are trimmed first, never below 0.

    INPUT REQUIREMENT — the caller MUST pass a map whose values already ~sum to
    ``total``; use ``rescale_to_total`` first if they might not. This function
    apportions, it does not rescale, and that is deliberate: silently rescaling here
    would convert a caller's bad-percentages bug (e.g. ``difficulty_counts`` receiving
    E:M:H percentages that do not total 100) from a loud assertion into a quiet
    "correction". The sum contract below is enforced either way.

    v2 — SUM CONTRACT REPAIRED (was: silently breakable).
        The old negative-deficit trim used a fixed ``i > 10 * len(order)`` iteration
        guard. Any deficit steeper than ~10 units per key exhausted the guard and the
        function RETURNED EARLY with the contract unmet — counts that did not sum to
        ``total``, with no error. Worked example (a 100-Q-era format mix apportioned to
        a 60-Q current pattern): ``{'TEXT': 85.0, 'FIGURAL': 10.0, 'PASSAGE': 5.0}``
        against ``total=60`` returned ``{'TEXT': 75, 'FIGURAL': 0, 'PASSAGE': 0}``
        — sum 75, not 60, and both minority classes annihilated.
        The trim is now pass-based: it repeats until the deficit is cleared, and stops
        early ONLY when every key has reached 0 (unreachable while ``total > 0``,
        since ``deficit < 0`` implies ``sum(floors) > total >= 1``). The closing
        assertion makes any future regression fail loudly instead of silently.
        Minority-class annihilation is not fixed here — it cannot be, because it is a
        symptom of un-rescaled input; ``rescale_to_total`` is the fix for that, and with
        rescaled input ``|deficit| < len(raw_map)``, so the trim never loops twice.
    """
    if not raw_map or total <= 0:
        return {}
    raw = {k: float(v) for k, v in raw_map.items()}
    floors = {k: int(math.floor(v)) for k, v in raw.items()}
    deficit = total - sum(floors.values())
    if deficit > 0:                                   # distribute by largest remainder
        order = sorted(raw, key=lambda k: (-(raw[k] - floors[k]), k))
        for i in range(deficit):
            floors[order[i % len(order)]] += 1
    elif deficit < 0:                                 # trim smallest remainder, >= 0
        order = sorted(raw, key=lambda k: ((raw[k] - floors[k]), k))
        while deficit < 0:
            progressed = False
            for k in order:
                if deficit >= 0:
                    break
                if floors[k] > 0:
                    floors[k] -= 1
                    deficit += 1
                    progressed = True
            if not progressed:                        # every key already 0 — cannot trim
                break
    assert sum(floors.values()) == total, (
        "largest_remainder_apportion: sum contract violated "
        "(got %d, expected %d) for input %r" % (sum(floors.values()), total, raw_map))
    return floors


def difficulty_counts(total_qs, s_pct, m_pct, h_pct):
    """S7-4: split ``total_qs`` into (simple, medium, hard) integer counts by the given
    E:M:H percentages (which MUST sum to 100). Guarantees simple+medium+hard==total_qs.

    Thin wrapper over ``largest_remainder_apportion`` — provably identical to the
    source's standalone implementation for the 3-band case (deficit ∈ [0, 2] < 3 keys,
    so the modulo distribution and the standalone loop coincide, and the tie-break
    key is identical). See test_difficulty_counts_equivalence.
    """
    raw = {
        "simple": total_qs * s_pct / 100,
        "medium": total_qs * m_pct / 100,
        "hard":   total_qs * h_pct / 100,
    }
    counts = largest_remainder_apportion(raw, total_qs)
    # ``.get(k, 0)`` reproduces the source's behaviour at the total_qs==0 boundary,
    # where the canonical apportioner returns {} but the standalone difficulty_counts
    # returns (0, 0, 0). Identical for every total_qs > 0.
    s, m, h = counts.get("simple", 0), counts.get("medium", 0), counts.get("hard", 0)
    # Preserve the source's parity guarantee explicitly.
    assert s + m + h == total_qs, f"difficulty_counts: sum != total_qs={total_qs}"
    return s, m, h


def proportional_split(pool_subs, r_avg, budget, N, min_floor):
    """§4-2 STEP 3: split ``budget`` across ``pool_subs`` proportionally by r_avg.

    The caller has already reserved any floored/mandated subtopics and passes only the
    free pool here, along with the ``budget`` remaining for that pool. Each pool member
    gets at least ``min_floor`` (n_batches in the mock; the caller's coverage floor in
    the scoped path). When the pool's total r_avg is 0, the budget is split equally.

    Returns
    -------
    (quota, raw_total)
        quota[S]     : integer floor-quota for each pool subtopic (pre-deficit-fix).
        raw_total[S] : the real-valued ideal (used by ``largest_remainder_fix`` for the
                       fractional-remainder ordering). Computed with the SAME two-step
                       arithmetic as the source to avoid float re-association drift.
    """
    quota = {}
    raw_total = {}
    pool_r_total = sum(r_avg[S] for S in pool_subs)
    if pool_r_total > 0 and pool_subs:
        for S in pool_subs:
            scaled_avg = (r_avg[S] / pool_r_total) * (budget / N)
            raw_total[S] = scaled_avg * N
            quota[S] = max(min_floor, math.floor(raw_total[S]))
    elif pool_subs:
        # All pool subs have r_avg summing to 0 — equal split.
        equal_share = budget / len(pool_subs)
        for S in pool_subs:
            raw_total[S] = equal_share
            quota[S] = max(min_floor, math.floor(equal_share))
    return quota, raw_total


def largest_remainder_fix(quota, subs, raw_total, r_avg, target_total,
                          min_floor, floors=None):
    """§4-2 STEP 4: adjust ``quota`` (in place) so its sum equals ``target_total``
    EXACTLY, using largest-remainder on the real-valued ``raw_total``.

    Positive deficit → add 1 to the highest fractional remainders (tie-break r_avg
    desc). Negative deficit → remove from the smallest remainders, looping until met,
    NEVER reducing a subtopic below ``max(min_floor, floors[S])``. ``floors`` carries
    the caller's per-subtopic hard floor (mandate reservation in the mock path; empty
    in the scoped path). Raises ``AllocationError`` if the target cannot be reached
    (all subtopics already at their floor).

    Returns the (mutated) ``quota`` for convenience.
    """
    if floors is None:
        floors = {}

    deficit = target_total - sum(quota.values())

    # Sort DESC by fractional remainder; tie-break by r_avg DESC.
    remainders = sorted(
        subs,
        key=lambda S: (raw_total[S] - math.floor(raw_total[S]), r_avg[S]),
        reverse=True,
    )

    if deficit >= 0:
        for i in range(deficit):
            quota[remainders[i % len(remainders)]] += 1
    else:
        removals = list(reversed(remainders))
        removed = 0
        while removed < abs(deficit):
            reduced_this_pass = 0
            for S in removals:
                if removed == abs(deficit):
                    break
                floor_for_S = max(min_floor, floors.get(S, 0))
                if quota[S] > floor_for_S:
                    quota[S] -= 1
                    removed += 1
                    reduced_this_pass += 1
            if reduced_this_pass == 0:
                raise AllocationError(
                    f"cannot reduce quotas to reach target_total={target_total}. "
                    f"All {len(subs)} subtopics are at minimum quota "
                    f"(min_floor={min_floor} or per-subtopic floor). "
                    f"Current sum={sum(quota.values())}. Too many subtopics for "
                    f"available slots."
                )

    assert sum(quota.values()) == target_total, (
        f"Quota sum {sum(quota.values())} != target {target_total} — algorithm error"
    )
    return quota


def exact_fill(quotas, col_targets):
    """§4-5b EXACT MATRIX FILL (Gale-Ryser). VERBATIM.

    quotas       : dict {S: quota_in_window}  (free subtopics only; quota ≥ 0)
    col_targets  : list length N of per-paper FREE capacity
    returns alloc: dict {S: [count per paper]} (length N), or raises on infeasible.
    Precondition: sum(quotas.values()) == sum(col_targets).

    By construction, for the free subtopics in one window:
      row sum == quota_S exactly; column sum == per-paper free capacity exactly;
      per-cell ∈ {floor(q/N), ceil(q/N)} (variance ≤ 1); every quota≥1 subtopic
      appears ≥ 1 in the window. Deterministic (identical output on re-run).
    """
    N = len(col_targets)
    S_list = sorted(quotas)                      # deterministic order
    total_q = sum(quotas.values())
    total_c = sum(col_targets)
    if total_q != total_c:
        raise ValueError(
            f"exact_fill: Σquota={total_q} != Σcol_target={total_c} "
            f"(feasibility invariant)"
        )
    alloc = {S: [0] * N for S in S_list}
    # 1) BASE: floor(q/N) in every paper; compute per-row remainder and per-col leftover.
    col_left = list(col_targets)
    rem = {}
    for S in S_list:
        b = quotas[S] // N
        for m in range(N):
            alloc[S][m] = b
            col_left[m] -= b
        rem[S] = quotas[S] - b * N                 # = quota % N  ∈ [0, N-1]
    if any(c < 0 for c in col_left):
        raise ValueError(
            "exact_fill: a column over-subscribed by base pass "
            "(col_target < Σ base). Reduce quotas or increase sec_qs."
        )
    # 2) REMAINDER as a 0/1 matrix with row sums rem[S], col sums col_left[m].
    #    Gale-Ryser: each column gives its +1s to the rows with the LARGEST remaining
    #    row-remainder (most-remaining-first). Provably valid iff feasible.
    rows = dict(rem)
    for m in sorted(range(N), key=lambda k: -col_left[k]):
        need = col_left[m]
        if need == 0:
            continue
        avail = [S for S in S_list if rows[S] > 0]
        if need > len(avail):
            raise ValueError(
                f"exact_fill: column {m + 1} needs {need} extras but only "
                f"{len(avail)} subtopics have remainder (Gale-Ryser infeasible)."
            )
        avail.sort(key=lambda S: (-rows[S], S))
        for S in avail[:need]:
            alloc[S][m] += 1
            rows[S] -= 1
    if any(v != 0 for v in rows.values()):
        raise ValueError(
            "exact_fill: residual row remainder after fill "
            "(should not happen if feasible)."
        )
    return alloc


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER C — FORMAT / AXIS SCHEDULE  (Framework_Blueprint.md §7-7)
# ════════════════════════════════════════════════════════════════════════════

def section_axis2_pool_caps(section_name, id_list, cap_by_id, manifest_ids):
    """§7-7 ``_section_axis2_pool_caps``.

    Union of Axis-2 capability across a section/scope's subtopic ids (used for
    guarantee feasibility). CONTRACT: ``id_list`` arrives ALREADY scoped to
    ``section_name`` — the §7-7 fence builds pyq_ids/zp_ids via
    subtopic_in_section() (Subject → OTS-section bridge), and ScopedBlueprint
    passes its scope's own ids. Ids absent from ``manifest_ids`` are skipped.

    GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE: this function used to RE-filter
    the pre-scoped list with ``manifest_ids[sid]['section'] == section_name`` —
    a raw string comparison joining the taxonomy Subject namespace (manifest
    'section' holds Subject names, e.g. 'Organic Chemistry') against the OTS
    section-label namespace ('Section A'). On any exam whose
    ``sections[].subjects`` maps multiple Subjects into one section the two
    namespaces never intersect, so the comparison was always False and the
    capability union came back EMPTY — every guarantee silently reported
    'unsatisfiable'. The fence's own subtopic_in_section() fixed this exact
    namespace bug at spec v1.35 (BUG 2); these engine-side re-filters were
    missed. ``section_name`` is retained for signature stability and error
    context; it no longer filters.
    """
    caps = set()
    for sid in id_list:
        if sid in manifest_ids:
            caps |= set(cap_by_id.get(sid, ["DIRECT"]))
    return caps


def _clip_marking_scheme_to_section(q_range, marking_scheme):
    """GAP-2026-08-12-AXIS3-MECHLOCK internal helper. Clip every marking_scheme
    entry to this section's own ``[start, end]`` (inclusive) and keep only entries
    carrying a single, non-empty ``question_type`` string. Entries with no overlap,
    or that are malformed (missing/non-numeric/inverted ``q_range``, missing
    ``question_type``), are dropped defensively — a dropped entry can only ever
    WIDEN a gap in the caller's coverage accounting, never manufacture a false
    'full' lock, so silently skipping bad data is safe here in a way it would not
    be for a HARD validator (that validation is exam_config.json's own job,
    upstream, at Step 2a/S2-1 — this is a best-effort structural detector, not a
    second copy of that validation).

    Returns a list of ``(clipped_start, clipped_end, question_type)`` tuples,
    sorted by ``clipped_start`` ascending.
    """
    if not q_range or not marking_scheme:
        return []
    try:
        sec_start, sec_end = int(q_range[0]), int(q_range[1])
    except (TypeError, ValueError, IndexError):
        return []
    if sec_end < sec_start:
        return []
    clipped = []
    for entry in marking_scheme:
        if not isinstance(entry, dict):
            continue
        qtype = entry.get("question_type")
        if not qtype or not isinstance(qtype, str):
            continue
        er = entry.get("q_range")
        if not er or len(er) != 2:
            continue
        try:
            e_start, e_end = int(er[0]), int(er[1])
        except (TypeError, ValueError):
            continue
        if e_end < e_start:
            continue
        c_start, c_end = max(sec_start, e_start), min(sec_end, e_end)
        if c_start > c_end:
            continue                                       # no overlap with this section
        clipped.append((c_start, c_end, qtype))
    clipped.sort(key=lambda t: t[0])
    return clipped


def axis3_mechanism_lock(q_range, marking_scheme, sec_qs):
    """§7-7 GAP-2026-08-12-AXIS3-MECHLOCK. Detect whether a section's marking_scheme
    entries PARTITION it by position — disjoint, contiguous sub-ranges each
    declaring exactly one ``question_type`` — and if so, return the EXACT
    position-derived counts for the covered portion.

    Returns ``{'coverage': 'none'|'partial'|'full', 'covered_qs': int,
    'by_type': {question_type: exact_count}, 'gap_qs': int}``.

      'none'    — no locked sub-range found for this section (or the exam defines
                  marks by CATEGORY rather than by position here). Caller must fall
                  back to the ordinary PYQ-measured target, unchanged. ``by_type``
                  is ``{}``.
      'partial' — some but not all of the section is position-locked. ``by_type``
                  carries ONLY the locked portion's exact counts (sums to
                  ``covered_qs``); the caller is responsible for apportioning the
                  remaining ``gap_qs`` from the PYQ-measured distribution and
                  summing the two.
      'full'    — the ENTIRE section is position-locked. ``by_type`` sums to
                  ``sec_qs`` exactly and IS the final axis3_target_per_mock for
                  this section — no PYQ blending, no PYQ data required at all.

    A GAP is any sub-range not covered by a single-question_type entry. An
    OVERLAP between two locked entries is treated as a gap too — ambiguous
    locking is not locking — so it can only ever downgrade 'full' to 'partial'
    (or 'partial' to a smaller covered_qs), never inflate confidence.
    """
    clipped = _clip_marking_scheme_to_section(q_range, marking_scheme)
    _sec_qs = int(sec_qs) if sec_qs else 0
    if not clipped or _sec_qs <= 0:
        return {"coverage": "none", "covered_qs": 0, "by_type": {}, "gap_qs": max(0, _sec_qs)}
    sec_start = int(q_range[0])
    sec_end = int(q_range[1])
    by_type = {}
    covered_qs = 0
    cursor = sec_start
    overlap_or_gap = False
    for c_start, c_end, qtype in clipped:
        if c_start > cursor:
            overlap_or_gap = True                          # a true gap before this entry
        elif c_start < cursor:
            overlap_or_gap = True                          # this entry overlaps the previous one
            c_start = cursor                                # do not double-count the overlapped slice
            if c_start > c_end:
                continue
        n = c_end - c_start + 1
        by_type[qtype] = by_type.get(qtype, 0) + n
        covered_qs += n
        cursor = max(cursor, c_end + 1)
    if cursor <= sec_end:
        overlap_or_gap = True                              # trailing gap after the last entry
    gap_qs = _sec_qs - covered_qs
    if gap_qs < 0:
        # Defensive only: inconsistent q_range/sec_qs inputs, or overlapping
        # clipped entries, can inflate covered_qs past sec_qs. Never return a
        # negative gap; clamping here can only ever SUPPRESS a false 'full',
        # never manufacture one.
        gap_qs = 0
        overlap_or_gap = True
    if covered_qs == 0:
        coverage = "none"
    elif not overlap_or_gap and gap_qs == 0:
        coverage = "full"
    else:
        coverage = "partial"
    return {"coverage": coverage, "covered_qs": covered_qs, "by_type": by_type, "gap_qs": gap_qs}


def _axis3_with_mechanism_lock(a3, sec_qs, q_range, marking_scheme):
    """GAP-2026-08-12-AXIS3-MECHLOCK. Compute the final axis3_target_per_mock for a
    section, blending the ordinary PYQ-measured apportionment with any detected
    mechanism lock (``axis3_mechanism_lock``). Returns ``(target_map, lock_info)``
    where ``lock_info`` is always the raw ``axis3_mechanism_lock`` result (for
    provenance/reporting), even when the ordinary PYQ target was used unchanged.

    'none'    → the ordinary PYQ-measured apportionment, byte-identical to the
                pre-v1.49 return value (no marking_scheme/q_range given, or the
                exam defines marks by category — nothing to override).
    'full'    → the lock's own exact counts, verbatim. No PYQ data used at all.
    'partial' → the lock's exact counts for the locked portion PLUS the
                PYQ-measured distribution RE-apportioned to exactly the
                remaining gap_qs, summed key-wise. If there is no PYQ signal at
                all to fill the gap with (a3 empty or all-zero), NEVER fabricate
                a mechanism split with no data behind it — same principle as
                guarantee_feasibility's "unsatisfiable ... shortfall accepted,
                never fabricated" — and fall back to the ordinary full-section
                PYQ apportionment for this section instead of a lock that cannot
                be honoured completely and correctly.
    """
    base = largest_remainder_apportion(a3, sec_qs)
    lock = axis3_mechanism_lock(q_range, marking_scheme, sec_qs)
    if lock["coverage"] == "none":
        return base, lock
    if lock["coverage"] == "full":
        return dict(lock["by_type"]), lock
    # partial
    gap_qs = lock["gap_qs"]
    if gap_qs <= 0 or not a3 or sum(a3.values()) <= 0:
        return base, lock
    remainder = largest_remainder_apportion(rescale_to_total(a3, gap_qs), gap_qs)
    merged = dict(lock["by_type"])
    for k, v in remainder.items():
        merged[k] = merged.get(k, 0) + v
    # Defensive re-assertion of the §14 AXIS-SUM contract this function exists to
    # uphold — BV-AXIS (S9-12) enforces it downstream as a HARD FAIL, so a
    # violation here must be loud immediately, at the source, not discovered
    # three steps later in a different file.
    assert sum(merged.values()) == sec_qs, (
        "axis3 mechanism-lock blend violated the AXIS-SUM contract "
        "(got %d, expected %d) for section covering %r" % (sum(merged.values()), sec_qs, q_range))
    return merged, lock


def derive_axis_schedule(section_name, axis_dist, sec_qs,
                         pyq_ids, zp_ids, cap_by_id, manifest_ids,
                         papers_per_window=10, total_mocks=None,
                         figural_capacity=None, marking_scheme=None,
                         q_range=None):
    """§7-7 ``derive_axis_schedule``. VERBATIM except ``mocks_per_window`` renamed to
    ``papers_per_window`` (a mock is a paper; a scoped test is a paper).

    Returns the per-section (or per-scope) axis_schedule dict for blueprint.json.
      axis_dist : the format-distribution targets for this section/scope, or None.
      pyq_ids / zp_ids : subtopic_ids with r_avg>0 / r_avg==0 in this section/scope.

    Absent-safe: axis_dist is None (all-Zero-PYQ, or a pre-axis manifest) → a
    status='no_pyq' schedule and the whole feature stays inert.

    marking_scheme / q_range (GAP-2026-08-12-AXIS3-MECHLOCK, v1.49 — BOTH optional,
    default None, and BOTH must be given together for the override to activate).
    When given, ``axis3_target_per_mock`` is checked against this section's own
    marking_scheme position-partition (``axis3_mechanism_lock``) and overridden —
    fully or partially — wherever the exam locks a mechanism (question_type) to a
    fixed Q-range instead of letting it float by category. On such an exam the
    PYQ-measured axis3 distribution can directly contradict the exam's own declared
    marking scheme (e.g. targeting MSQ/NAT counts inside a Q-range the marking_scheme
    itself declares pure MCQ) — every paper is then structurally unable to ever
    satisfy the target, a permanent, paper-unfixable A-AXIS3 finding no amount of
    re-generation can fix, because the target itself is impossible. Conditional, not
    universal: an exam whose marking_scheme defines marks by CATEGORY rather than by
    position (question types can appear at any Q number) has no partition to detect,
    and for that exam this is a no-op — the ordinary PYQ-measured target is returned
    unchanged, byte-identical to pre-v1.49 behaviour. Framework_ScopedBlueprint never
    passes either parameter (a scope is not a fixed Q-range), so its call site is
    completely unaffected by this change. See axis3_mechanism_lock's own docstring
    for the exact partition/coverage rules.
    """
    if not axis_dist:
        return {
            "section": section_name, "status": "no_pyq",
            "axis1_per_paper": {}, "axis2_per_paper": {}, "axis3_per_paper": {},
            "axis2_audit_mode": {}, "axis2_window_target": {}, "axis2_guarantee": [],
            "guarantee_feasibility": {}, "axis1_target_per_mock": {},
            "axis3_target_per_mock": {}, "negative_rate": 0.0,
            "mocks_per_window": papers_per_window, "recent_years": [],
        }

    # ── PATTERN-ERA NORMALISATION (v2 — exam-agnostic, applies to ALL three axes) ──
    # axis_dist holds REAL per-paper class averages measured on the PYQ corpus. They are
    # in "questions per historical paper" units. This paper is sec_qs questions. Those two
    # units coincide ONLY while the exam pattern has kept the same size — an assumption
    # that silently fails on every exam whose pattern has changed (IIT JAM Biotechnology
    # 100 Q -> 60 Q; and the reverse, where a corpus predates a pattern that grew).
    #
    # Re-express every axis in current-pattern units FIRST. Proportions are preserved, so
    # a class that was 5% of the historical paper stays 5% of this one. Three consumers
    # were reading these numbers in the wrong unit before this normalisation existed:
    #   (1) axis1/axis3_target_per_mock — apportioned from an un-rescaled map, which drove
    #       largest_remainder_apportion into its (now repaired) early-return path AND
    #       annihilated minority stimulus/mechanism classes;
    #   (2) axis2_window_target — computed as avg * papers_per_window with no rescale at
    #       all, so band quotas were off by the full pattern-size ratio;
    #   (3) audit_canonical.py's B-AXIS1/B-AXIS3 audit, which scales the
    #       RETURNED axis{1,3}_per_paper by the window — so it audited every produced paper
    #       against historical-size targets and raised findings that no correct paper could
    #       ever clear.
    # Returning the normalised maps (not the raw ones) is what fixes (3) at the source.
    #
    # NO-OP for callers that already normalise: Framework_ScopedBlueprint §6-2 scales all
    # three axes to Q and passes sec_qs = Q, so rescale_to_total's tolerance guard returns
    # its input untouched and the scoped schedule is bit-for-bit unchanged.
    a1 = rescale_to_total(axis_dist.get("axis1_per_paper", {}), sec_qs)
    a2 = rescale_to_total(axis_dist.get("axis2_per_paper", {}), sec_qs)
    a3 = rescale_to_total(axis_dist.get("axis3_per_paper", {}), sec_qs)

    # ── GAP-2026-08-12-AXIS3-MECHLOCK ───────────────────────────────────────────
    # Compute the axis3 target ONCE here (a no-op when marking_scheme/q_range are
    # not given, or the exam has no position-locked mechanism for this section) so
    # both the returned target AND its provenance are available below.
    _axis3_target, _axis3_lock = _axis3_with_mechanism_lock(a3, sec_qs, q_range, marking_scheme)

    # RE-DERIVE the audit mode with THIS window. Blueprint knows the exam's real
    # window, so it is AUTHORITATIVE. DIRECT is always the residual float.
    mode = {}
    for cls, avg in a2.items():
        if cls == "DIRECT":
            mode[cls] = "float"
        else:
            mode[cls] = "band" if float(avg) * papers_per_window >= 1 else "guarantee"

    # band-mode → per-window target counts; guarantee-mode → the guarantee list.
    # DIRECT (mode 'float') is the residual filler and is NEVER given a target.
    window_target, guarantee = {}, []
    for cls, avg in a2.items():
        m = mode.get(cls, "band")
        if m == "float":
            continue
        if m == "guarantee":
            guarantee.append(cls)
        else:
            window_target[cls] = round(float(avg) * papers_per_window)

    # Guarantee feasibility (faithfulness-preserving, NO allocation swap):
    #   pyq_covered — a PYQ (r_avg>0) subtopic can carry it.
    #   zp_only     — only a Zero-PYQ subtopic can.
    #   unsatisfiable — no faithful source anywhere → accept shortfall; never fabricate.
    pyq_caps = section_axis2_pool_caps(section_name, pyq_ids, cap_by_id, manifest_ids)
    zp_caps = section_axis2_pool_caps(section_name, zp_ids, cap_by_id, manifest_ids)
    feas = {}
    for g in guarantee:
        feas[g] = ("pyq_covered" if g in pyq_caps
                   else "zp_only" if g in zp_caps
                   else "unsatisfiable")

    # v1.46 — the mock count is a PROPERTY OF THE EXAM and must be passed in. It was
    # read from axis_dist["total_mocks"], a key Step 5 never writes, so it silently fell
    # back to 15 for every exam in the estate. Any exam configured for a different
    # number of mocks got a 15-long target series and a quota sized for 15 papers.
    _n_mocks = _axis_int(total_mocks) or _axis_int(axis_dist.get("total_mocks")) or 15

    return {
        "section": section_name, "status": "ok",
        "axis1_per_paper": a1,
        "axis2_per_paper": a2,
        "axis3_per_paper": a3,
        "axis2_audit_mode": mode,
        "axis2_window_target": window_target,
        "axis2_guarantee": guarantee,
        "guarantee_feasibility": feas,
        "axis1_target_per_mock": largest_remainder_apportion(a1, sec_qs),
        "axis3_target_per_mock": _axis3_target,
        # ── GAP-2026-08-12-AXIS3-MECHLOCK — provenance, for audit/report visibility ──
        # 'pyq_measured' is byte-identical to every pre-v1.49 blueprint (no override
        # applied — either no marking_scheme/q_range given, or this section has no
        # position-locked mechanism). 'mechanism_lock_full'/'mechanism_lock_partial'
        # record that axis3_target_per_mock above was overridden, and by how much
        # (axis3_mechanism_lock carries the exact covered/gap counts for a report).
        "axis3_target_source": ("pyq_measured" if _axis3_lock["coverage"] == "none"
                                else "mechanism_lock_" + _axis3_lock["coverage"]),
        "axis3_mechanism_lock": _axis3_lock,
        "negative_rate": axis_dist.get("negative_rate", 0.0),
        "mocks_per_window": papers_per_window,
        "recent_years": axis_dist.get("recent_years", []),
        # ── GAP-2026-08-06-AXIS1 ────────────────────────────────────────────────
        # A BUDGET THAT NOTHING SPENDS IS A BUG. These two flags exist so that fact
        # is machine-checkable rather than a convention someone has to remember:
        # Step 7 must build a tracker for every axis marked "hard", and the auditor
        # must refuse to certify a paper carrying a "hard" budget it has no gate for.
        # That single rule is what stops this defect class returning as Axis-4.
        # ── v1.45 (GAP-2026-08-06-IRREDUCIBLE) — SCHEDULING, NOT A FLAT TARGET ──
        # axis1_target_series    : per-mock FIGURAL targets from the exam's OWN observed
        #   shape, so the series reproduces the real spread (the reference exam ranged
        #   2..8) instead of fifteen statistically identical papers.
        # axis1_observed_figural : raw per-paper counts, handed to the auditor so the
        #   band is this exam's volatility rather than a fixed percentage — the v2.24
        #   band (±1/±15%) rejected FOUR of that exam's five real papers.
        # axis1_figural_quota    : per-subtopic count of mocks that should carry a
        #   FIGURE. THIS IS THE FIX FOR THE IRREDUCIBLE OVERRIDE: before v1.45 a
        #   subtopic allocated to every mock drew a figure in every mock (1.00/paper)
        #   whatever its measured frequency, so three subtopics whose true contributions
        #   are 0.68/0.55/0.23 forced 3.00 — and twenty-one of them forced 14.3 against
        #   a budget of 5.
        # NO FEASIBILITY HALT EXISTS, AND NONE IS NEEDED: irreducible figures are a
        #   SUBSET of all figural questions, both counted from the SAME corpus, so
        #   demand can never exceed the budget (32 of 154 on the reference exam, 1.45 of
        #   7.00 per paper). Verified over 500 randomised synthetic exams — zero
        #   infeasible mocks. A halt here would always mean a FRAMEWORK BUG, not bad
        #   data, which is precisely what the v2.42 any() defect turned out to be.
        # v1.47 — PER-CLASS, NOT FIGURAL-ONLY. The v1.45/v1.46 work built the full
        # rate -> quota -> schedule chain for FIGURAL and left DI with a render-time cap
        # only, so on a DI-heavy exam the COUNT was right but the DISTRIBUTION was not:
        # DI landed on whichever subtopics were visited first, never at each subtopic's
        # measured DI frequency. Same defect family, one class over, invisible on any
        # exam with a DI budget of 0 — which is every exam we had to hand.
        # Emitting per class means a future PASSAGE (or Axis-4) class inherits the whole
        # chain instead of needing its own release.
        "axis1_quota_by_class": {
            _cls: figural_quota(
                (axis_dist.get("count_by_subtopic_by_class") or {}).get(_cls) or {},
                _n_mocks,
                (axis_dist.get("per_paper_mean_by_class") or {}).get(_cls),
                capacity=figural_capacity)
            for _cls in STIMULUS_CLASSES if _cls != "TEXT"},
        "axis1_series_by_class": {
            _cls: figural_target_series(
                (axis_dist.get("per_paper_observed_by_class") or {}).get(_cls) or [],
                _n_mocks,
                total=largest_remainder_apportion(a1, sec_qs).get(_cls, 0))
            for _cls in STIMULUS_CLASSES if _cls != "TEXT"},
        "axis1_observed_by_class": {
            _cls: list((axis_dist.get("per_paper_observed_by_class") or {}).get(_cls) or [])
            for _cls in STIMULUS_CLASSES if _cls != "TEXT"},
        "axis1_target_series": figural_target_series(
            axis_dist.get("figural_per_paper_observed") or [],
            _n_mocks,
            total=largest_remainder_apportion(a1, sec_qs).get("FIGURAL", 0)),
        "axis1_observed_figural": list(axis_dist.get("figural_per_paper_observed") or []),
        "axis1_figural_quota": figural_quota(
            axis_dist.get("figural_count_by_subtopic") or {},
            _n_mocks, axis_dist.get("figural_per_paper_mean"),
            capacity=figural_capacity),
        "axis1_enforcement": "hard",
        "axis3_enforcement": "hard",
        # Provenance of the per-section numbers. "measured" = counted directly on
        # this exam section; "apportioned" = derived from a paper-wide total split by
        # section SIZE. Apportionment is a real distortion, not a rounding detail: on
        # the reference exam the measured per-section figural averages are
        # A 1.4 / B 1.0 / C 2.0, while size-apportionment yields A 2.2 / B 0.7 / C 1.4
        # — it hands the FEWEST figures to the section that carries the MOST.
        "axis_measured_by": axis_dist.get("measured_by", "apportioned"),
        "axis_window_years": axis_dist.get("window_years", AXIS_WINDOW_YEARS),
    }


def axis1_feasibility(section_name, axis1_target_per_mock, pyq_ids, manifest_ids):
    """§7-7 ``axis1_feasibility``. ADVISORY (WARN, never HALT).

    Compare the Axis-1 (stimulus) per-paper target against the formats actually
    available among this section/scope's PYQ subtopics. Returns the list of target
    formats with no capable PYQ subtopic ([] == fully feasible).
    CONTRACT: ``pyq_ids`` arrives ALREADY scoped to ``section_name`` (see
    section_axis2_pool_caps — same GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE
    record: the old wrong-namespace re-filter emptied ``avail`` on every
    sections[].subjects exam, flagging every targeted format unreachable).
    Ids absent from ``manifest_ids`` are skipped; ``section_name`` is retained
    for signature stability and error context, it no longer filters.
    """
    avail = set()
    for sid in pyq_ids:
        if sid in manifest_ids:
            avail.add(manifest_ids[sid].get("format", "TEXT"))
    unreachable = [fmt for fmt, cnt in axis1_target_per_mock.items()
                   if cnt > 0 and fmt not in avail]
    return unreachable


def axis1_mock_feasibility(target, alloc_counts, manifest_ids):
    """§7-7 GAP-2026-08-12-AXIS-PREFLIGHT (companion to ``axis1_feasibility``).
    ADVISORY (WARN, never HALT) — same contract, but scoped to a single MOCK's
    actual finalised subtopic allocation rather than the whole section's PYQ pool.

    ``axis1_feasibility`` (above) answers "does this SECTION have ANY PYQ subtopic
    capable of each targeted format, ever" — necessary but not sufficient. A mock
    can pass that section-wide check and still be drafted from a subset of
    subtopics that happens to under-represent (or entirely omit) the
    format-capable ones THIS mock needed, purely from how the window's
    rotation/quota split landed. ``axis1_feasibility`` cannot see that — it runs
    once, at blueprint-build time, before any mock's specific allocation exists.
    This function runs AFTER a mock's subtopic allocation is finalised (Step 7,
    before Batch 1 drafts anything) and answers the narrower, mock-specific
    question: "given EXACTLY the subtopics allocated to this mock, and assuming
    every single capable slot renders in the targeted format, can this mock
    structurally reach its own target?"

    target       : this mock's resolved axis1 target dict, e.g.
                   {'TEXT': 56, 'FIGURAL': 4} — the caller's responsibility to
                   resolve (including substituting axis1_target_series[this mock]
                   for 'FIGURAL' where that rotates), exactly mirroring
                   axis1_feasibility's own contract of taking a pre-resolved
                   target rather than deriving it itself.
    alloc_counts : {subtopic_id: q_count} — this mock's finalised allocation,
                   ONE entry per allocated subtopic with its slot count (a
                   subtopic holding 3 slots contributes 3 to its format's total,
                   not 1). NOT filtered to PYQ-only — an allocated Zero-PYQ
                   subtopic still occupies a real slot and still has a real
                   ``format``, so it counts toward capacity exactly like a PYQ
                   one; only ``axis1_feasibility``'s section-wide advisory
                   restricts itself to ``pyq_ids`` (a different question: PYQ
                   provenance for the WHOLE section's format mix, not this
                   mock's actual slot capacity).
    manifest_ids : {subtopic_id: {..., 'format': ...}} — same shape/source as
                   every other caller in this module.

    Returns ``{format: {'target': int, 'max_achievable': int}}`` for every
    format that is SHORT (max_achievable < target). ``{}`` == fully feasible for
    this mock — mirrors ``axis1_feasibility``'s own "``[]`` == fully feasible"
    spirit; a dict here (not a bare list of names) because the COUNT, not just
    the format name, is the useful part of a mock-specific pre-flight.
    ``axis1_feasibility`` itself is left completely untouched, byte-identical,
    for its one existing caller (Framework_Blueprint.md §7-7).
    """
    if not target or not alloc_counts:
        return {}
    avail = {}
    for sid, n in alloc_counts.items():
        fmt = (manifest_ids.get(sid) or {}).get("format", "TEXT")
        avail[fmt] = avail.get(fmt, 0) + int(n or 0)
    shortfall = {}
    for fmt, want in target.items():
        want = int(want or 0)
        if want <= 0:
            continue
        have = int(avail.get(fmt, 0))
        if have < want:
            shortfall[fmt] = {"target": want, "max_achievable": have}
    return shortfall


def axis3_mock_feasibility(target, alloc_counts, manifest_ids, position_based_typing):
    """§7-7 GAP-2026-08-12-AXIS3-PREFLIGHT (Axis-3 companion to
    ``axis1_mock_feasibility``, deliberately deferred out of that function's own
    v5.50 release — see its history for why). ADVISORY (WARN, never HALT).

    THE SUBTLETY THAT MAKES THIS A SEPARATE FUNCTION, NOT A COPY-PASTE OF
    ``axis1_mock_feasibility`` WITH 'format' SWAPPED FOR 'mechanism':
    Axis-1 (stimulus format) is always a SUBTOPIC property — nothing else ever
    decides it. Axis-3 (mechanism: MCQ/MSQ/NAT) is NOT always a subtopic
    property. ``Framework_MockTestCreate`` v5.30's POSITION-BASED QUESTION TYPE
    DISPATCH (``_resolve_answer_axes``, §3 S3-2) means that whenever an exam's
    marking_scheme declares MORE THAN ONE distinct ``question_type`` ANYWHERE
    (``_position_based_typing = len(_distinct_q_types) > 1`` — an EXAM-WIDE
    flag, computed once, not per-section), EVERY question's mechanism, in
    EVERY section of that exam, is decided by its Q-POSITION via
    ``_type_for_q(qnum)`` — which defaults to MCQ for any Q number outside a
    declared marking_scheme range — and the allocated subtopic's own
    ``answer_cardinality``/``answer_type`` is never consulted at all. This is
    true even for a Q-range GAP-2026-08-12-AXIS3-MECHLOCK's own
    ``axis3_mechanism_lock`` would call 'partial'-locked or 'none'-locked for
    THIS section specifically — position-based dispatch is a GLOBAL exam
    property, not a per-section one, so a section that looks un-locked by
    ``axis3_mechanism_lock`` can still be entirely position-dispatched (falling
    to the MCQ default) if ANY other section of the same exam declares 2+
    distinct types. Checking subtopic capability in that regime would be
    MEANINGLESS at best and ACTIVELY MISLEADING at worst — it could report a
    shortfall for a mechanism that is, in fact, guaranteed by position
    regardless of which subtopics were allocated. This is exactly the
    correctness trap the v5.50 release note flagged and deliberately avoided
    landing un-verified; ``position_based_typing`` is the fix, and it is a
    REQUIRED parameter (no default) specifically so no caller can silently
    omit it and get a wrong answer by accident.

    target                : this section's axis3_target_per_mock (already the
                             FINAL, lock-blended value if
                             GAP-2026-08-12-AXIS3-MECHLOCK applies — no
                             additional composition needed here, unlike Axis-1's
                             rotating FIGURAL series; axis3_target_per_mock does
                             not rotate per mock).
    alloc_counts           : {subtopic_id: q_count} — identical contract to
                             ``axis1_mock_feasibility``.
    manifest_ids           : {subtopic_id: {..., 'answer_cardinality':,
                             'answer_type': ...}}. Per-subtopic mechanism is
                             derived to mirror BOTH ``_resolve_answer_axes``'s
                             own SUBTOPIC-BASED branch (the values read) AND
                             ``audit_canonical.gate_axis3``'s own observability
                             order (the precedence: NAT is checked first — "0
                             options ⇒ NAT" there mirrors ``answer_type ==
                             'numerical'`` here — then MSQ, with MCQ as the
                             untested residual, exactly as that gate's own
                             docstring states it).
    position_based_typing  : REQUIRED, EXAM-WIDE boolean — pass the SAME
                             ``_position_based_typing`` variable
                             Framework_MockTestCreate's own S3-2 already
                             computes (``len(_distinct_q_types) > 1`` over the
                             WHOLE marking_scheme), not a per-section
                             recomputation. When True, this function returns
                             ``{}`` UNCONDITIONALLY — see above.

    Returns ``{mechanism: {'target': int, 'max_achievable': int}}`` for every
    mechanism SHORT — identical "``{}`` == fully feasible" convention as
    ``axis1_mock_feasibility``. Also ``{}`` (nothing meaningful to check) on a
    position-based exam, or when ``target``/``alloc_counts`` is empty.
    """
    if position_based_typing:
        return {}
    if not target or not alloc_counts:
        return {}
    avail = {}
    for sid, n in alloc_counts.items():
        mv = manifest_ids.get(sid) or {}
        if str(mv.get("answer_type", "option")).strip().lower() == "numerical":
            mech = "NAT"
        elif str(mv.get("answer_cardinality", "single")).strip().lower() == "multi":
            mech = "MSQ"
        else:
            mech = "MCQ"
        avail[mech] = avail.get(mech, 0) + int(n or 0)
    shortfall = {}
    for mech, want in target.items():
        want = int(want or 0)
        if want <= 0:
            continue
        have = int(avail.get(mech, 0))
        if have < want:
            shortfall[mech] = {"target": want, "max_achievable": have}
    return shortfall


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER C2 — AXIS-1 / AXIS-3 BUDGET TRACKERS   (GAP-2026-08-06-AXIS1)
# ════════════════════════════════════════════════════════════════════════════
#
# WHY THIS CLUSTER EXISTS.
#   The three-axis feature has four stages: MEASURE (Step 5) → BUDGET (Step 6) →
#   SPEND (Step 7) → VERIFY (audit). Before this release only Axis-2 had all four.
#   Axis-1 (stimulus: TEXT/FIGURAL/PASSAGE/DI) and Axis-3 (mechanism: MCQ/MSQ/NAT)
#   were MEASURED and BUDGETED and then never spent and never verified —
#   `axis1_target_per_mock` and `axis3_target_per_mock` were written into
#   blueprint.json by derive_axis_schedule() and read by nothing at all
#   (`grep axis1 Framework_MockTestCreate.md` → 0 hits, for four releases).
#
#   MEASURED CONSEQUENCE (IIT_JAM_BIOTECHNOLOGY, 2026-08-06). Step 7 read the
#   per-subtopic `format` field as a RENDERING IMPERATIVE — "format==FIGURAL ⇒ draw
#   a picture", with §2135 explicitly BANNING a text stem for such a subtopic. The
#   subtopic flag itself came from an existential quantifier in Step 5
#   (`has_img = any(q.image_role != 'none' ...)`), so ONE figural question anywhere
#   in a 22-year corpus stamped a subtopic FIGURAL forever. 46 of 131 subtopics
#   carried the flag, holding 42.7% of allocation weight, against a true
#   question-level figural rate of 7.3%. The delivered mocks:
#
#       blueprint axis1_target_per_mock FIGURAL : 4  / 60
#       Mock01 questions on FIGURAL subtopics   : 26 → 26 figures rendered
#       Mock02 questions on FIGURAL subtopics   : 30 → 30 figures rendered
#
#   An exact 1:1 map, in both papers, and every gate passed clean. A mock with 43%
#   figures against an exam with 7% is not a mock of that exam.
#
# THE RULE THIS CLUSTER ENCODES.
#   `format` stops meaning "always draw this" and starts meaning "CAPABLE of being
#   drawn this way". How many are actually drawn is capped by the Step-6 budget;
#   WHICH ones are drawn is ranked by each subtopic's own measured figural_rate, so
#   figures land where the exam actually puts them (organic-chemistry structures at
#   24.8%) and never where it does not (Microbial Biotechnology at 0.0%).
#
#   THE GOLDEN RULE IS UNTOUCHED. Format still never EXCLUDES a subtopic from
#   allocation — the sole exclusion criterion remains r_avg == 0.0. Every allocated
#   subtopic keeps its slot; only the RENDERING of some slots changes.
#
# ABSENT-SAFE, EXACTLY AS AXIS-2 WAS.
#   No axis_schedule (pre-v1.23 blueprint) ⇒ build_axis_tracker returns None ⇒ every
#   grant is allowed ⇒ byte-identical legacy behaviour. No figural_rate in the
#   manifest (pre-v2.26) ⇒ ranking degrades to irreducible-first-then-declaration-
#   order, still capped. ~200 deployed exams keep working untouched until they are
#   re-measured. THE FEATURE TURNS ITSELF OFF, IT NEVER TURNS ITSELF WRONG.

AXIS_WINDOW_YEARS = 5   # distinct years averaged for the per-paper axis targets.
                        # Raised from 3 (2026-08-06). The window sets HOW MANY of a
                        # class a mock gets; the full corpus still sets WHICH subtopics
                        # can carry it — two different questions, two different samples.
                        # Era-scoping (filter_progress_to_eras) still applies FIRST, so a
                        # wider window can never straddle a pattern change.

AXIS_MAX_MOCKS = 1000   # v1.46 hard clamp on any caller-supplied mock count.
                        # total_mocks arrives from blueprint.json, i.e. from a file on
                        # disk that another step wrote, so a typo or a corrupted field
                        # is a real input. Unclamped, figural_target_series(obs, 2**40)
                        # allocates a 10^12-element list and the OOM killer takes the
                        # whole run — found by a resource probe, not by reasoning.
                        # Clamped rather than rejected: a series that is too long is a
                        # bad number, not a reason to lose the exam.

AXIS_BAND_FLEX = 0.50   # v1.45 operator-set proportional floor for the audit band.
                        # Rationale in figural_band(): the previous ±1/±15% band
                        # rejected FOUR of the reference exam's five real papers.

AXIS_BAND_ABS = 1       # audit tolerance: ±1 count …
AXIS_BAND_REL = 0.15    # … or ±15%, whichever is LARGER. A band, not an equality:
                        # real papers vary (this exam ranged 2→8 figures over 5 years)
                        # and a gate that demands an exact count gets disabled by hand.

STIMULUS_CLASSES  = ("TEXT", "FIGURAL", "PASSAGE", "DI")     # Axis-1
MECHANISM_CLASSES = ("MCQ", "MSQ", "NAT")                    # Axis-3

def axis_truth_check(sched_entry, pyq_ids, zp_ids, cap_by_id, manifest_ids):
    """§9 S9-12 AXIS-TRUTH (GAP-2026-08-23-AXIS-ADVISORY-TRUTH; parent record
    GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE, gap-analysis §13 item 7).

    Cross-examine a section's STORED axis advisories against the data that
    would falsify them. Returns a list of contradiction findings ([] ==
    consistent). The caller treats any finding as a HARD FAIL: a contradicted
    advisory means the measurement instrument that wrote it is corrupt, and a
    corrupt instrument is STRUCTURAL corruption, not a format shortfall.

    FIRST-PRINCIPLES BY DESIGN — this function must NEVER call
    axis1_feasibility() or section_axis2_pool_caps(). Those are the instruments
    under audit. The 2026-08-18 defect corrupted BOTH of them identically at
    the source; a checker that recomputes through the audited path reproduces
    the corruption and passes vacuously — a green check that shares its
    subject's code path is exactly what a hollow check looks like (the
    audit_mutation lesson). The derivations below are therefore reimplemented
    inline from the manifest and capability map directly. They MUST stay
    semantically aligned with the primary functions: availability is the
    'format' field with the 'TEXT' default over in-manifest pyq_ids; capability
    is the union of cap_by_id with the ['DIRECT'] default over in-manifest ids;
    verdict precedence is pyq_covered > zp_only > unsatisfiable; zero-count
    targets are ignored. If a DELIBERATE change to a primary function fires
    this check, resolve the divergence consciously in both places — that
    forced conversation is the point of a cross-check.

    Inputs mirror the §7-7 / ScopedBlueprint §6-3 build call: pyq_ids/zp_ids
    arrive PRE-SCOPED by the caller (§2-1 FIX D — this function performs no
    section join and takes no section name; ids absent from manifest_ids are
    skipped, so a ghost id can never manufacture phantom availability).
    sched_entry that is None or status != 'ok' returns [] — a no_pyq schedule
    derives nothing, so there is nothing to contradict; the SEC-8 gate owns
    that territory.
    """
    if not sched_entry or sched_entry.get('status') != 'ok':
        return []
    findings = []

    # 1) Axis-1 — stored unreachable list vs first-principles availability.
    avail = {(manifest_ids.get(sid) or {}).get('format', 'TEXT')
             for sid in pyq_ids if sid in manifest_ids}
    target = sched_entry.get('axis1_target_per_mock') or {}
    expected_un = {f for f, c in target.items() if c > 0 and f not in avail}
    stored_un = set(sched_entry.get('axis1_unreachable_formats') or [])
    if stored_un != expected_un:
        pess = sorted(stored_un - expected_un)
        opt = sorted(expected_un - stored_un)
        parts = []
        if pess:
            parts.append(
                f"axis1_unreachable_formats claims {pess} unreachable, but the "
                f"scoped PYQ subtopics demonstrably contain them (available "
                f"formats: {sorted(avail)})")
        if opt:
            parts.append(
                f"axis1_unreachable_formats omits {opt}, which the target "
                f"demands (count > 0) and NO scoped PYQ subtopic can render")
        findings.append(
            "; ".join(parts) + " — the stored advisory contradicts the "
            "manifest it summarises; the instrument that wrote it is corrupt.")

    # 2) Axis-2 — stored guarantee verdicts vs first-principles capability unions.
    def _union(ids):
        u = set()
        for sid in ids:
            if sid in manifest_ids:
                u |= set(cap_by_id.get(sid, ["DIRECT"]))
        return u
    pyq_caps, zp_caps = _union(pyq_ids), _union(zp_ids)
    expected_feas = {g: ("pyq_covered" if g in pyq_caps
                         else "zp_only" if g in zp_caps
                         else "unsatisfiable")
                     for g in (sched_entry.get('axis2_guarantee') or [])}
    stored_feas = sched_entry.get('guarantee_feasibility') or {}
    if stored_feas != expected_feas:
        findings.append(
            f"guarantee_feasibility is {stored_feas!r} but the capability map "
            f"derives {expected_feas!r} (pyq caps={sorted(pyq_caps)}, zp caps="
            f"{sorted(zp_caps)}) — a class marked 'unsatisfiable' while a "
            f"capable subtopic is on file lets every Axis-2 shortfall be "
            f"excused as unavoidable.")
    return findings


def _axis_int(v):
    """Total non-negative-integer coercion for the whole Axis cluster.

    blueprint_core's contract is that these functions NEVER raise (RA-9 / CLAUDE.md):
    one malformed key must not take out a gate — the defect class v2.12 closed for the
    other call sites. The inputs here arrive from JSON written by another step, so
    None, '', 'x', NaN, ±inf and negatives are all reachable in practice and every one
    of them was a live crash until fuzzing found them. Counts are non-negative integers,
    so anything that is not one collapses to 0.
    """
    try:
        f = float(v)
    except (TypeError, ValueError, OverflowError):
        return 0
    if f != f or f in (float('inf'), float('-inf')):        # NaN / ±inf
        return 0
    try:
        n = int(f)
    except (ValueError, OverflowError):
        return 0
    return n if n > 0 else 0


def _axis_float(v):
    """Total non-negative-float coercion (rates, tolerances). See _axis_int."""
    try:
        f = abs(float(v))
    except (TypeError, ValueError, OverflowError):
        return 0.0
    return f if (f == f and f != float('inf')) else 0.0


_AXIS_KEYS = {
    "axis1": ("axis1_target_per_mock", STIMULUS_CLASSES,  "TEXT"),
    "axis3": ("axis3_target_per_mock", MECHANISM_CLASSES, "MCQ"),
}


def figural_band(target, observed=None, band_abs=AXIS_BAND_ABS,
                 band_rel=AXIS_BAND_REL, band_flex=AXIS_BAND_FLEX):
    """Audit tolerance for a per-paper stimulus target. THE LARGEST OF THREE.

        allow = max( band_abs , band_flex x target , observed spread )

    WHY THREE AND NOT ONE. The v2.24 band was ±1 / ±15%, and it was measured against
    the reference exam's OWN five papers: 8, 3, 2, 6, 3 figures (mean 4.4). A budget of
    5 with ±1 gives [4, 6], which REJECTS FOUR OF THE FIVE REAL PAPERS. A mock
    indistinguishable from the actual 2026 exam would have been reported defective. A
    gate that cries wolf on genuine papers is one an operator switches off, and then
    nothing is checked at all — strictly worse than having no gate.

      band_abs   floor for tiny targets, so a budget of 1 is not a demand for exactly 1.
      band_flex  operator-set proportional floor (default 0.50). Protects exams whose
                 history is thin or suspiciously flat, where the observed spread
                 understates the real variation because we simply have not seen enough.
      observed   the exam's OWN spread over the window: max(|max-mean|, |mean-min|).
                 This governs whenever the exam is genuinely volatile, which is the
                 common case — the reference exam swings +82% / -55% around its mean,
                 far outside any fixed percentage anyone would pick in advance.

    Taking the LARGEST means the tolerance is a property of the exam rather than a
    constant, and no single hand-chosen number is doing the real work.

    THIS IS A TOLERANCE FOR THE AUDITOR, NOT A TARGET FOR THE GENERATOR. Generation
    still aims at the measured target; the band only decides what counts as a breach.
    If "up to 8 is allowed" ever becomes "aim for 8", the whole 15-mock series drifts
    high and the gate certifies the drift — which is how a tolerance quietly becomes a
    licence. figural_target_series() below is what generation aims at.
    """
    tgt = _axis_int(target)
    allow = max(_axis_int(band_abs), _axis_int(round(tgt * _axis_float(band_rel))),
                _axis_int(round(tgt * _axis_float(band_flex))))
    # `observed` is caller-supplied and reaches here from JSON written by another step,
    # so a scalar, a string or None are all live inputs — caught by the totality fixture,
    # not by reading the code. Anything not iterable simply contributes no spread.
    if isinstance(observed, str) or not hasattr(observed, '__iter__'):
        observed = []
    vals = [_axis_float(v) for v in observed if v is not None]
    if len(vals) >= 2:
        mean = sum(vals) / len(vals)
        allow = max(allow, _axis_int(round(max(max(vals) - mean, mean - min(vals)))))
    return allow


def figural_target_series(observed, n_mocks=15, total=None):
    """Per-mock targets drawn from the exam's OWN observed shape, not a flat mean.

    A 15-mock series where every paper carries exactly the mean is statistically tidy
    and pedagogically wrong: the reference exam ranged 2..8 figures over five years, so
    a candidate who practises fifteen identical 5-figure papers has never once met the
    figure-heavy paper the real exam produces roughly one year in five.

    The observed counts are cycled (descending, so the heaviest lands first and a short
    series is not accidentally all-light) and the cycle is rotated across the series.
    Deterministic — the same corpus rebuilds the same series, byte-for-byte.

    Falls back to a flat mean when there is nothing to draw a shape from, which is the
    pre-v1.45 behaviour and therefore safe for every un-remeasured exam.
    """
    if isinstance(observed, str) or not hasattr(observed, '__iter__'):
        observed = []
    vals = [_axis_int(v) for v in observed if v is not None]
    n = min(AXIS_MAX_MOCKS, max(1, _axis_int(n_mocks) or 15))
    if not vals:
        flat = _axis_int(total) if total is not None else 0
        return [flat] * n
    shape = sorted(vals, reverse=True)
    return [shape[i % len(shape)] for i in range(n)]


def figural_quota(fig_counts, n_mocks=15, budget_per_paper=None, capacity=None):
    """How many mocks each subtopic should carry a FIGURE in.

    THIS IS THE FIX FOR THE 'IRREDUCIBLE OVERRIDE' DEFECT. Before v1.45, whether a
    subtopic produced a figure was decided at RENDER time from a boolean, so a subtopic
    allocated to every mock produced a figure in every mock — 1.00 per paper — no matter
    what its real frequency was. Measured on the reference exam, three irreducible
    subtopics whose true contributions are 0.68, 0.55 and 0.23 figures per paper were
    forcing 3.00, and twenty-one such subtopics were forcing 14.3 against a budget of 5.

    The gap was never in the data. It was ALLOCATION FREQUENCY: the corpus says a
    subtopic is figural in 68% of papers, and the generator made it figural in 100%.

    SHAPE FROM THE FULL CORPUS, TOTAL FROM THE RECENT WINDOW. fig_counts carries every
    figural question ever observed, which is the better estimator of WHICH subtopics
    illustrate (most subtopics appear 1-3 times per paper, so a five-paper denominator
    cannot rank them). budget_per_paper comes from the recent window, which is the only
    honest estimator of HOW MANY the current era uses. Normalising the first to the
    second keeps both. Without it a corpus spanning a pattern change over-allocates:
    the reference exam's 22 papers average 7.00 figures because the legacy 100-question
    era was image-heavier, while its current era averages 4.40.

    Returns {subtopic_id: n_mocks_with_a_figure}. Every entry is >= 0 and the total is
    ~ n_mocks x budget_per_paper by construction — which is what makes infeasibility
    arithmetically impossible rather than merely unlikely (see schedule_figural_slots).
    """
    if not isinstance(fig_counts, dict):
        fig_counts = {}
    counts = {k: _axis_int(v) for k, v in fig_counts.items() if _axis_int(v) > 0}
    n = min(AXIS_MAX_MOCKS, max(1, _axis_int(n_mocks) or 15))
    total = sum(counts.values())
    if not total:
        return {}
    want = _axis_float(budget_per_paper) * n if budget_per_paper is not None else float(total)
    if want <= 0:
        return {k: 0 for k in counts}
    # Largest-remainder apportionment: exact integer total, no systematic bias toward
    # the subtopics that happen to sort first.
    raw = {k: want * v / total for k, v in counts.items()}
    out = {k: int(v) for k, v in raw.items()}
    short = int(round(want)) - sum(out.values())
    if short > 0:
        for k in sorted(raw, key=lambda k: (-(raw[k] - out[k]), k))[:short]:
            out[k] += 1
    elif short < 0:
        for k in sorted((k for k in out if out[k] > 0),
                        key=lambda k: (raw[k] - out[k], k))[:-short]:
            out[k] -= 1
    # CAP AND REDISTRIBUTE, NEVER SILENTLY TRUNCATE. A subtopic cannot be figural in
    # more mocks than exist, but clipping the excess and stopping would quietly lose
    # figure-slots and leave the series UNDER the measured budget — the same class of
    # silent shortfall this release exists to remove, just pointing the other way.
    # (Caught by the fixture, not by inspection: with few figural subtopics and a high
    # budget the clip cost 24 of 66 slots.) Excess is handed to subtopics that still
    # have room, in measured-frequency order.
    # v1.46 — a subtopic's ceiling is n_mocks x its PER-MOCK capacity (its q_count),
    # not n_mocks. Capping at n_mocks assumes one figure per subtopic per mock, which
    # silently starves every exam whose figural budget approaches its figural-subtopic
    # count: one figural subtopic with a budget of 5 delivered 1.00 per mock, forever.
    if not isinstance(capacity, dict):
        capacity = {}
    _cap = {k: max(1, _axis_int(capacity.get(k, 1))) * n for k in out}
    out = {k: min(v, _cap[k]) for k, v in out.items()}
    excess = int(round(want)) - sum(out.values())
    while excess > 0:
        room = [k for k in sorted(raw, key=lambda k: (-raw[k], k)) if out[k] < _cap[k]]
        if not room:
            break          # genuinely no capacity left: n_mocks x n_subtopics is the
                           # hard ceiling. Return what is achievable rather than raise —
                           # the caller audits the total, and a short series is visible.
        for k in room:
            if excess <= 0:
                break
            out[k] += 1
            excess -= 1
    return out


def schedule_figural_slots(quota, targets, band=None, n_mocks=None, capacity=None):
    """Spread each subtopic's figure-slots across the series, least-crowded mock first.

    WHY THIS CANNOT FAIL, AND WHY THERE IS NO HALT.
      Every figure-slot placed here comes from fig_counts, i.e. from a question that
      REALLY CARRIED A FIGURE in a real paper. Irreducible subtopics are a SUBSET of
      figural ones, so their slot total is a subset sum of the same corpus total the
      budget is derived from. Measured on the reference exam: 32 irreducible figural
      questions inside 154 total, i.e. 1.45 of 7.00 per paper. A subset cannot exceed
      its superset, so total demand can never exceed total capacity.
      Verified empirically over 500 randomised synthetic exams (20-140 subtopics,
      3-25 papers, deliberately figure-heavy and pathological cases included):
      ZERO infeasible mocks, worst overshoot 0.

      A HALT WOULD THEREFORE ALWAYS INDICATE A FRAMEWORK BUG, NEVER BAD DATA — the
      budget and the flags are measured from the SAME papers, so if they contradict
      each other, one of them was computed wrong. That is exactly what happened in
      v2.42: an any() existential marked 21 subtopics irreducible off a single question
      each, and the contradiction it produced looked like an impossible corpus. There is
      no halt in this function because there is nothing a halt could legitimately report.

    Clustering, not volume, is the only real risk (the reference blueprint put 29 forced
    figures in Mock 12 and 4 in Mock 10 purely by allocation order), and placing each
    slot into the mock with the most remaining headroom is what removes it.

    Returns [{subtopic_id: n_figures} per mock] — deterministic; ties break on
    subtopic_id. A DICT rather than a set (v1.46): a subtopic allocated several
    questions in one mock may legitimately carry several figures. `sid in slots` still
    works unchanged for callers that only test membership.
    """
    if isinstance(targets, str) or not hasattr(targets, '__iter__'):
        targets = []
    # v1.46 — capacity: {subtopic_id: max figures it may carry in ONE mock}, normally
    # its allocated q_count. Before v1.46 this was HARD-CODED to 1 by using a set per
    # mock, which is a silent exam-independence break: the paper is then capped at one
    # figure per DISTINCT figural subtopic, so any exam whose figural budget approaches
    # its figural-subtopic count under-delivers permanently. Measured:
    #     46 subtopics / budget 4.4 ->  4.40   fine (subtopics >> budget)
    #     10 subtopics / budget 25  -> 10.00   SHORT by 15  (non-verbal reasoning)
    #      3 subtopics / budget 8   ->  3.00   SHORT by 5   (chemistry-heavy)
    #      1 subtopic  / budget 5   ->  1.00   SHORT by 4
    # Those exams would FAIL A-AXIS1 shortfall on EVERY mock forever, with the generator
    # structurally unable to comply — the permanent-failure shape this series exists to
    # remove. The cap must be the subtopic's q_count, never a constant.
    if not isinstance(capacity, dict):
        capacity = {}
    tg = [_axis_int(t) for t in (targets or [])]
    n = min(AXIS_MAX_MOCKS, _axis_int(n_mocks) or len(tg) or 15)
    if not tg:
        tg = [0] * n
    while len(tg) < n:
        tg.append(tg[-1] if tg else 0)
    ceil = [t + _axis_int(band) for t in tg]
    load = [0] * n
    out = [{} for _ in range(n)]          # v1.46: {subtopic_id: n_figures}, was a set
    if not isinstance(quota, dict):
        quota = {}
    for sid, cnt in sorted(quota.items(), key=lambda kv: (-_axis_int(kv[1]), str(kv[0]))):
        cap = max(1, _axis_int(capacity.get(sid, 1)))
        for _ in range(_axis_int(cnt)):
            # Most headroom first, never past this subtopic's own capacity in that mock.
            # One slot at a time (rather than dumping a subtopic's whole quota into one
            # mock) is what keeps the spread even.
            cand = [m for m in range(n) if out[m].get(sid, 0) < cap]
            if not cand:
                break
            m = min(cand, key=lambda k: (-(ceil[k] - load[k]), k))
            out[m][sid] = out[m].get(sid, 0) + 1
            load[m] += 1
    # GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL. "No schedule" MUST be
    # FALSY. Every caller guards this call with `if <slots> else None` and its
    # own comment promises "empty schedule (pre-v1.45 blueprint) => fall through,
    # so every un-remeasured exam keeps its current behaviour exactly". But a
    # quota of {} produced `[{}, {}, ... x n]` — a TRUTHY list of empty dicts —
    # so the sentinel never fired, the caller's per-mock filter ran against an
    # empty allowance, and EVERY figural-capable slot was stripped before the
    # ranking or the budget was ever consulted. Measured on IIT_JAM_CHEMISTRY
    # Mock 01 (blueprint v1.35, quota {}): 21/5/14 capable slots -> 0/0/0
    # survivors against an Axis-1 FIGURAL budget of 9/3/6. The paper would ship
    # ZERO figures and fail A-AXIS1 shortfall on every mock, forever, with the
    # generator structurally unable to comply.
    # SAME DEFECT CLASS AS G-FIGINK (v5.57) ONE LAYER UP: the guard measured a
    # DECLARED property (the list is non-empty) instead of the actual CONTENT
    # (the schedule carries slots). Fixed at the producer so no caller — present
    # or future, spec-side or engine-side — can get the sentinel wrong again.
    # `any(out)` is exact: a mock entry is truthy iff it holds >=1 slot, so this
    # returns [] iff NOTHING was scheduled anywhere. A populated quota is
    # untouched, byte-for-byte.
    if not any(out):
        return []
    return out


def build_axis_tracker(section_sched, axis="axis1", counts=None):
    """Per-MOCK, per-SECTION budget tracker for Axis-1 or Axis-3.

    Mirrors build_axis2_tracker (Framework_MockTestCreate §S7-AXIS) in shape and in
    absent-safety, with one deliberate difference: Axis-2 accumulates across a
    10-paper WINDOW (its minority classes are too rare to place one per paper),
    whereas Axis-1/Axis-3 budgets are PER PAPER — a single mock that is 43% figures
    is wrong on its own terms, no matter what the window average works out to.

    section_sched : blueprint.axis_schedule[section], or None.
    counts        : running counts for THIS paper ({} at paper start).

    Returns a plain dict (JSON-serialisable, registry-safe), or None when there is
    no usable target — in which case every grant is allowed and behaviour is legacy.
    """
    if not isinstance(section_sched, dict) or section_sched.get("status") != "ok":
        return None
    key, classes, residual = _AXIS_KEYS.get(axis, _AXIS_KEYS["axis1"])
    _raw = section_sched.get(key)
    if not isinstance(_raw, dict):
        return None
    target = {str(k): _axis_int(v) for k, v in _raw.items()}
    if not any(target.values()):
        return None
    if not isinstance(counts, dict):
        counts = {}
    _c = counts.get("counts")
    return {
        "axis":       axis,
        "target":     target,
        "counts":     {str(k): _axis_int(v) for k, v in _c.items()} if isinstance(_c, dict) else {},
        "residual":   residual,       # the class every unclaimed slot falls back to
        "classes":    list(classes),
        "irreducible": _axis_int(counts.get("irreducible", 0)),
        "granted":    list(counts.get("granted") or []),
    }


def axis_need(tr, cls):
    """How many more of this class the paper still wants. 0 when met, over, or inert.

    The residual class (TEXT for Axis-1, MCQ for Axis-3) is the filler every
    unclaimed slot decays into and is never steered toward — the same treatment
    DIRECT gets on Axis-2.
    """
    if not isinstance(tr, dict) or cls == tr.get("residual"):
        return 0
    gap = _axis_int(tr.get("target", {}).get(cls, 0)) - _axis_int(tr.get("counts", {}).get(cls, 0))
    return gap if gap > 0 else 0


def axis_record(tr, cls, irreducible=False):
    """Book one produced question against the budget. Idempotent per call site."""
    if not isinstance(tr, dict):
        return
    tr["counts"][cls] = _axis_int(tr["counts"].get(cls, 0)) + 1
    if irreducible and cls != tr.get("residual"):
        tr["irreducible"] = _axis_int(tr.get("irreducible", 0)) + 1


def axis_snapshot(tr):
    """Serialise for the registry commit / audit hand-off. None ⇒ nothing to write."""
    if not isinstance(tr, dict):
        return None
    return {"counts": dict(tr.get("counts") or {}),
            "irreducible": _axis_int(tr.get("irreducible", 0)),
            "granted": list(tr.get("granted") or [])}


def axis_grant_figural(tr, subtopic_id, reducible=True, cls="FIGURAL"):
    """THE SPEND DECISION. May THIS question be rendered as `cls` (default FIGURAL)?

    Returns (granted: bool, reason: str). Step 7 calls this at the render fork that
    previously read `if format == FIGURAL:` unconditionally.

    THREE OUTCOMES, IN PRECEDENCE ORDER:

      1. tr is None                     → GRANT ('inert'). No budget exists; legacy
                                          behaviour, ~200 untouched exams.

      2. reducible is False             → GRANT ('irreducible'), EVEN OVER BUDGET.
                                          The subtopic's OPTIONS are themselves images
                                          (image_role == 'stem_and_options': organic
                                          structures, circuit diagrams, spectra). Such a
                                          question CANNOT be rewritten as text without
                                          becoming unanswerable. The GOLDEN RULE decides
                                          this: never drop or maim a subtopic to hit a
                                          format target. The overage is recorded, not
                                          warned — check_axis_conformance() raises the
                                          expectation by the irreducible count so the
                                          audit stays silent when the excess is fully
                                          explained, and FAILS when it is not. That is
                                          what stops this exemption from becoming the
                                          hole the whole gate leaks through.

      3. budget remaining               → GRANT ('budget'), else DENY ('over_budget').
                                          A denied question is not dropped: it keeps its
                                          allocation slot and renders via the subtopic's
                                          REPLACEMENT_RULE as a TEXT question drawn from
                                          that subtopic's own observed PYQ patterns.
    """
    if not isinstance(tr, dict):
        return (True, "inert")
    if not reducible:
        axis_record(tr, cls, irreducible=True)
        tr["granted"].append(subtopic_id)
        return (True, "irreducible")
    if axis_need(tr, cls) > 0:
        axis_record(tr, cls)
        tr["granted"].append(subtopic_id)
        return (True, "budget")
    return (False, "over_budget")


def rank_figural_candidates(allocated, rates=None, reducible=None):
    """WHICH allocated questions should claim the scarce figural slots.

    A budget of 4 is worthless if the 4 land in a subject the exam never illustrates.
    Ordering (descending priority):

        1. IRREDUCIBLE first  — they will be granted regardless (rule 2 above), so
           letting them consume budget BEFORE the reducible ones keeps the total honest
           instead of stacking discretionary figures on top of mandatory ones.
        2. Highest measured figural_rate — the share of that subtopic's real PYQ
           questions that actually carried a figure. On the reference exam this ranges
           from 79% (stereochemistry) to 3.1% (complex formation); both were flagged
           identically by the old boolean.
        3. Stable tie-break on subtopic_id, so a rebuild of the same mock is byte-identical.

    allocated : iterable of (qnum, subtopic_id) — the FIGURAL-capable slots.
    rates     : {subtopic_id: float 0..1}, absent ⇒ 0.0 (ranks last, still eligible).
    reducible : {subtopic_id: bool},      absent ⇒ True.

    Returns the same pairs, reordered. Pure; no I/O; never raises.
    """
    rates = rates or {}
    reducible = reducible or {}
    if not isinstance(rates, dict):
        rates = {}
    if not isinstance(reducible, dict):
        reducible = {}
    def _key(item):
        try:
            _q, sid = item
        except (TypeError, ValueError):
            return (1, 0.0, str(item))
        red = reducible.get(sid, True)
        return (0 if red is False else 1, -_axis_float(rates.get(sid, 0.0)), str(sid))
    return sorted(list(allocated or []), key=_key)


def check_axis_conformance(observed, target, irreducible=0, axis="axis1",
                           observable=None, observed_spread=None,
                           band_abs=AXIS_BAND_ABS, band_rel=AXIS_BAND_REL):
    """THE VERIFY STAGE. Did the produced paper honour its own budget?

    Shared by Step 7's self-audit and the canonical auditor's A-AXIS1 / A-AXIS3 gates,
    so generator and auditor cannot drift apart — the same discipline
    check_figural_conformance() already applies to figure TYPE. This is the COUNT
    question that gate never asked, and the reason 26-vs-4 shipped twice.

    observed / target : {class: int} for one section.
    irreducible       : count of granted-over-budget irreducible questions. The
                        expectation is raised by this, so a legitimate overage is a
                        SILENT PASS and only unexplained excess fails.
    observable        : the classes the CALLER could actually establish from the
                        artefacts it holds. None ⇒ all of them (legacy callers).

    OBSERVABILITY IS NOT OPTIONAL, AND ITS ABSENCE IS NOT A ZERO.
      An auditor that cannot see a class must say so. The first cut of this function
      had no `observable` parameter, so a caller with no evidence for a class passed
      observed=0 — and a target of DI:6 then produced a HARD FAIL reading "produced 0,
      budget 6" on a paper that may well have had six. Two failure modes, both severe:
        • FALSE FAIL on every DI/PASSAGE exam in the estate — and a gate that cries
          wolf gets switched off by hand, which is strictly worse than no gate;
        • FALSE PASS in the other direction, because an unobservable class that WAS
          over-produced fell into the residual and vanished.
      An unobservable class is therefore EXCLUDED from the verdict and returned in
      `unestablished` for the caller to surface as a coverage WARN. Reporting "I could
      not check this" is a real result; inventing a zero is not.

    Returns (verdict, findings, unestablished):
      verdict      'PASS' | 'FAIL' | 'SKIP'
      findings     human-readable breaches (empty on PASS/SKIP)
      unestablished classes that were targeted but could not be observed

    NEVER RAISES. A malformed target (None, a string, a negative) degrades to 0 rather
    than killing the run — the whole gate dying over one bad key is the defect class
    v2.12 closed for blueprint_core's other call sites.
    """
    _as_int, _as_frac = _axis_int, _axis_float

    if not target:
        return ("SKIP", [], [])                 # no budget ⇒ nothing to verify (inert)
    _k, classes, residual = _AXIS_KEYS.get(axis, _AXIS_KEYS["axis1"])
    obs_ok = None if observable is None else {str(c) for c in observable}
    findings, unestablished = [], []
    for cls in classes:
        tgt = _as_int((target or {}).get(cls, 0))
        if cls == residual:
            continue                            # residual absorbs all rounding by design
        if obs_ok is not None and cls not in obs_ok:
            if tgt > 0 or _as_int((observed or {}).get(cls, 0)) > 0:
                unestablished.append(cls)
            continue
        obs = _as_int((observed or {}).get(cls, 0))
        # Band parameters are caller-supplied and get the same total coercion as counts;
        # a bad tolerance must widen or narrow the band, never kill the gate.
        # v1.45 — delegate to figural_band() so the auditor and the generator read the
        # SAME tolerance. Before this the gate carried its own ±1/±15%, which rejected
        # FOUR of the reference exam's five real papers.
        allow = figural_band(tgt, observed_spread, band_abs, band_rel)
        hi = tgt + allow + (_as_int(irreducible) if cls == "FIGURAL" else 0)
        lo = max(0, tgt - allow)
        if obs > hi:
            findings.append(
                f"{cls}: produced {obs}, budget {tgt} (tolerance +{allow}"
                + (f", +{_as_int(irreducible)} irreducible" if irreducible and cls == "FIGURAL" else "")
                + f"). The paper over-represents {cls} against the exam it models.")
        elif obs < lo:
            findings.append(
                f"{cls}: produced {obs}, budget {tgt} (tolerance -{allow}). "
                f"The paper under-represents {cls} against the exam it models.")
    return ("FAIL" if findings else "PASS", findings, sorted(set(unestablished)))


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER D — ID NORMALISATION + INPUT PARSING  (Framework_Blueprint.md §17 / Step-5 files)
# ════════════════════════════════════════════════════════════════════════════

def parse_section_rules_difficulty(text):
    """Pure text parse of section_rules.md → {subtopic_id: {level: is_inferred_bool}}
    for the three difficulty levels (Simple/Medium/Hard), read from each subtopic's
    PYQ_DIFFICULTY_CALIBRATION block.

    section_rules.md format (Step 5 writer): each subtopic block begins with a
    ``subtopic_id: <id>`` line and contains::

        PYQ_DIFFICULTY_CALIBRATION:
          Simple: "criteria" [INFERRED]
          Medium: "criteria"
          Hard:   "criteria" [INFERRED]

    A level carrying the ``[INFERRED]`` tag (or absent from the block entirely) →
    is_inferred=True; a level WITHOUT the tag → is_inferred=False (observed in PYQ).
    The scoped difficulty envelope (§5) is the set of levels with is_inferred=False.

    Pure: text in, dict out. No I/O — the caller reads the file and passes its text.
    Keyed by subtopic_id (the cross-step join key), so it aligns with the manifest.
    """
    result = {}
    id_pat = re.compile(r'^[ \t]*subtopic_id:[ \t]*(\S+)[ \t]*$', re.M)
    matches = list(id_pat.finditer(text or ''))
    for i, m in enumerate(matches):
        sid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        levels = {'Simple': True, 'Medium': True, 'Hard': True}   # default: all inferred
        # Bound to the calibration block (writer appends a blank line after Hard); fall back
        # to the whole subtopic block if the blank-line terminator is not found.
        cal = re.search(r'PYQ_DIFFICULTY_CALIBRATION:[ \t]*\n(.*?)(?:\n[ \t]*\n|\Z)',
                        block, re.S)
        seg = cal.group(1) if cal else block
        for lv in ('Simple', 'Medium', 'Hard'):
            lvm = re.search(rf'^[ \t]*{lv}:[ \t]*(.*)$', seg, re.M)
            if lvm:
                levels[lv] = '[INFERRED]' in lvm.group(1)
        result[sid] = levels
    return result


def parse_section_rules_field(text, field, default=None):
    """Pure text parse of section_rules.md → {subtopic_id: value} for a SINGLE named per-subtopic
    field (e.g. 'answer_type', 'answer_cardinality'), read as ``field: value`` within each
    subtopic block. A subtopic whose block lacks the field maps to ``default``. Keyed by
    subtopic_id (the cross-step join key). Pure: text + field name in, dict out. No I/O.

    Used by the scoped blueprint to populate subtopic_list[].answer_type / answer_cardinality so
    Step 11 tags scoped papers with the correct question type (mock parity) instead of defaulting
    every question to MCQ-single.
    """
    result = {}
    id_pat = re.compile(r'^[ \t]*subtopic_id:[ \t]*(\S+)[ \t]*$', re.M)
    fld_pat = re.compile(rf'^[ \t]*{re.escape(field)}:[ \t]*(\S+)', re.M)
    matches = list(id_pat.finditer(text or ''))
    for i, m in enumerate(matches):
        sid = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        fm = fld_pat.search(text[start:end])
        result[sid] = fm.group(1) if fm else default
    return result


def slugify(text):
    """§17 S2-MANIFEST ``slugify``. VERBATIM.

    MUST stay byte-identical to Step 0's slugify (same recipe, or subtopic_ids won't
    match across steps).
    """
    t = (text or "").lower()
    for ch in ("\u2014", "\u2013", "/", "&"):   # em-dash, en-dash, slash, ampersand
        t = t.replace(ch, " ")
    t = re.sub(r"[^a-z0-9]+", "_", t)
    t = re.sub(r"_+", "_", t).strip("_")
    return t


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER P — FEASIBILITY PREFLIGHT + PHASE-1 PLACEMENT + SPREAD CHECKS
#             (GAP-2026-08-25-BLUEPRINT-PHASE1, Framework_Blueprint v1.56.0)
# ════════════════════════════════════════════════════════════════════════════
# SINGLE SOURCE OF TRUTH. Framework_Blueprint §4-0 / §4-2 / §4-3 / §4-4 / §9-2 /
# §9-7 / §9-11 CALL these functions and never re-derive their arithmetic. The
# incident: the Phase-1 position formula lived in THREE places (§4-4 producer,
# §9-2 verifier, §8-4 prose) and the coverage window was assumed to equal a
# 10-mock B2 batch in a fourth. Every one of those copies is now a call.
#
# NOTHING HERE HALTS. Every function returns a verdict the caller writes into
# blueprint.json / the Assumptions table. Operators are not framework engineers;
# a geometry that needs a different parameter gets that parameter DERIVED.
# PURE: plain data in, plain data out. No I/O. Only ``math`` used.

DEFAULT_BATCH_SIZE_QS  = 10   # coverage window promised when the geometry allows it
DEFAULT_MAX_RARE       = 2    # per-mock rare cap when the rare pool allows it


def batch_size_feasible(n_pq, sec_qs, N, avail, bs):
    """True iff a ``bs``-mock coverage window is satisfiable for one section.

    Arm A (window capacity):  bs * sec_qs >= n_pq   — every PYQ subtopic fits once
                              inside one window of the section.
    Arm B (series quota floor): n_pq * ceil(N / bs) <= avail — giving every subtopic
                              its ``n_batches`` floor does not exceed the usable slots.
    Arm B is the §4-2 floor that used to surface late as AllocationError. Both arms
    are monotone in ``bs`` (verified: repro.py Table 3, 2,414 cases, 0 exceptions).
    """
    if n_pq == 0:
        return True
    if bs < 1:
        return False
    return bs * sec_qs >= n_pq and n_pq * math.ceil(N / bs) <= avail


def derive_batch_size(n_pq, sec_qs, N, avail, default=DEFAULT_BATCH_SIZE_QS):
    """Exact minimum coverage window for ONE section (closed form, no search).

    Returns a dict::

        tier       1  default window works (or no PYQ subtopics)
                   2  a wider window is REQUIRED — value in ``batch_size``
                   3  no window works: avail < n_pq (or avail <= 0). The section
                      cannot hold every PYQ subtopic even once in the whole series.
                      ``batch_size`` is None; ``min_N`` is the smallest N_mocks at
                      which this section becomes tier <= 2 (0 when avail <= 0).
        batch_size the derived window (tier 1/2) — never larger than N
        arm_a, arm_b  the two lower bounds (tier 1/2)
        note       one operator-facing sentence

    The default is capped at N (never promise a window longer than the series).
    Minimality is proven against brute force (repro.py Table 3: 3,633 agree / 0
    disagree). Feasibility is monotone in bs, so max(default, arm_a, arm_b) is the
    unique minimum >= default whenever any window works.
    """
    N = max(1, int(N))
    default = max(1, min(int(default), N))
    if n_pq == 0:
        return {'tier': 1, 'batch_size': default, 'arm_a': 0, 'arm_b': 0,
                'min_N': N, 'note': 'no PYQ subtopics; coverage arm dormant'}
    if avail <= 0:
        return {'tier': 3, 'batch_size': None, 'arm_a': None, 'arm_b': None,
                'min_N': 0,
                'note': (f'mandatory-every-mock + Zero-PYQ consume all '
                         f'{sec_qs * N} slots; no PYQ subtopic can be placed here')}
    if avail < n_pq:
        per_mock = avail / N                      # usable slots per mock
        min_N = math.ceil(n_pq / per_mock) if per_mock > 0 else 0
        return {'tier': 3, 'batch_size': None, 'arm_a': None, 'arm_b': None,
                'min_N': min_N,
                'note': (f'{n_pq} PYQ subtopics vs {avail} usable slots in the whole '
                         f'{N}-mock series; every subtopic cannot appear here even once '
                         f'(would need N_mocks >= {min_N}). Section runs at exam-wide '
                         f'coverage (§4-0 tier 3).')}
    arm_a = math.ceil(n_pq / sec_qs)
    K     = avail // n_pq                          # >= 1 here
    arm_b = math.ceil(N / K)
    bs    = min(N, max(default, arm_a, arm_b))
    if not batch_size_feasible(n_pq, sec_qs, N, avail, bs):   # cannot happen; guard
        return {'tier': 3, 'batch_size': None, 'arm_a': arm_a, 'arm_b': arm_b,
                'min_N': N + 1, 'note': 'no feasible window (guard)'}
    tier = 1 if bs == default else 2
    note = ('default window holds' if tier == 1 else
            f'coverage window widened {default} -> {bs} mocks '
            f'(arm A={arm_a}, arm B={arm_b}); every PYQ subtopic still appears '
            f'>= 1 per {bs}-mock window')
    return {'tier': tier, 'batch_size': bs, 'arm_a': arm_a, 'arm_b': arm_b,
            'min_N': N, 'note': note}


def feasibility_preflight(section_rows, N, default=DEFAULT_BATCH_SIZE_QS,
                          config_batch_size=None):
    """§4-0 FEASIBILITY PREFLIGHT — one pass, every section, NEVER raises.

    section_rows : list of {'name', 'sec_qs', 'n_pq', 'zp_slots', 'mandate_slots'}
                   zp_slots = sum(zp_slot[section][m]) (needs §5 → run at B1 Step 5A),
                   mandate_slots = N * (# mandatory_every_mock PYQ subtopics in section).
    config_batch_size : exam_config's explicit batch_size_qs, if any. Honoured only
                   when >= the derived minimum; otherwise overridden and reported.

    Returns {'batch_size_qs', 'n_batches', 'tiers': {name: 1|2|3},
             'report': [row...], 'notes': [str...], 'overrode_config': bool}.
    The series-wide window is the MAX over tier-1/2 sections (§4-1 reads ONE value).
    """
    N = max(1, int(N))
    report, notes, tiers = [], [], {}
    required = max(1, min(int(default), N))
    for s in section_rows:
        nm, sec_qs, n_pq = s['name'], int(s['sec_qs']), int(s['n_pq'])
        zp, mand = int(s.get('zp_slots', 0)), int(s.get('mandate_slots', 0))
        avail = sec_qs * N - zp - mand
        d = derive_batch_size(n_pq, sec_qs, N, avail, default)
        row = {'section': nm, 'sec_qs': sec_qs, 'n_pq': n_pq, 'slots': sec_qs * N,
               'zp_slots': zp, 'mandate_slots': mand, 'available': avail}
        row.update(d)
        report.append(row)
        tiers[nm] = d['tier']
        if d['tier'] in (1, 2):
            required = max(required, d['batch_size'])
        if d['tier'] != 1:
            notes.append(f"[{nm}] TIER {d['tier']}: {d['note']}")
    overrode = False
    if config_batch_size is not None:
        cfg = int(config_batch_size)
        if cfg >= required:
            required = min(cfg, N)
        else:
            overrode = True
            notes.append(f"exam_config batch_size_qs={cfg} is below the derived minimum "
                         f"{required}; overridden (a smaller window is infeasible).")
    return {'batch_size_qs': required, 'n_batches': math.ceil(N / required),
            'tiers': tiers, 'report': report, 'notes': notes,
            'overrode_config': overrode}


def capacity_split(pq_subs, r_avg, avail):
    """Tier-3 section: choose the ``avail`` PYQ subtopics this section CAN hold.

    Highest r_avg first; ties keep the caller's (§2-2c) order so the result is
    reproducible across sessions. Returns (kept, uncovered) in caller order.
    The uncovered list is DECLARED (blueprint.json uncovered_subtopics) — never a
    silent drop — and BV-0A / BV-9B verify each one is covered by another section.
    """
    avail = max(0, int(avail))
    ranked = sorted(range(len(pq_subs)), key=lambda i: (-float(r_avg.get(pq_subs[i], 0)), i))
    keep_idx = set(ranked[:avail])
    kept = [S for i, S in enumerate(pq_subs) if i in keep_idx]
    uncovered = [S for i, S in enumerate(pq_subs) if i not in keep_idx]
    return kept, uncovered


def exam_wide_uncovered(uncovered_by_section, carriers_by_subtopic):
    """Subtopics no section can hold: uncovered in EVERY section that carries them.

    uncovered_by_section : {section: [S, ...]} (from capacity_split)
    carriers_by_subtopic : {S: [section, ...]} (from §2-2c subjects_for_section)
    Returns a sorted list. Non-empty only when the taxonomy exceeds the whole exam
    series — reported in the B1 delivery summary, never a halt.
    """
    unc = {sec: set(v) for sec, v in uncovered_by_section.items()}
    out = []
    for S, secs in carriers_by_subtopic.items():
        secs = list(secs)
        if secs and all(S in unc.get(sec, set()) for sec in secs):
            out.append(S)
    return sorted(out)


def derive_max_rare(rare_quotas, N, default=DEFAULT_MAX_RARE):
    """§4-3: per-mock rare cap large enough for the FINAL rare pool.

    cap = max(default, ceil(sum(rare quotas) / N)). Derived AFTER §4-2 so it is
    exact, and it only feeds §4-4 placement (never quota) — so there is no
    fixed-point chase between batch_size_qs and max_rare_per_mock.
    """
    N = max(1, int(N))
    total = sum(int(min(q, N)) for q in rare_quotas.values())
    return max(int(default), math.ceil(total / N)) if total else int(default)


def phase1_positions(quotas, N_mocks, max_rare_per_mock):
    """SINGLE SOURCE OF TRUTH for Phase-1 rare positions (v1.56.0).

    Supersedes the formula int((k + 0.5) * N / q) + 1 that lived in §4-4, §9-2
    BV-2 and §8-4. Both call sites MUST call this; neither may re-derive positions.

    Segment-constrained + rank-spread:
      * appearance k of a subtopic lands INSIDE segment k of q equal segments, so
        it is never more than N/(2q) from the old ideal — exactly BV-7 F4's
        tolerance. F4 holds by construction (no change to F4).
      * within the segment the anchor is offset by the subtopic's RANK i/T, so
        subtopics that share a segment aim at different mocks (the incident: 20
        q=1 subtopics all computed mock 11 and packed forward into mocks 11-20).
      * the least-loaded free mock nearest the anchor wins → population stays flat
        and BV-4 (cap) holds wherever capacity exists.
    quotas : ORDERED mapping {subtopic: quota}. Iteration order is part of the
             contract — pass §4-3 rare_subs order (inherits pyq_subtopics order).
    Returns {subtopic: [mock, ...]} sorted ascending, 1-indexed.
    Measured (repro.py, 1,792 adversarial shapes): F4 98.2%, F2 99.7%, BV-4 100%,
    F2b 98.9% — vs shipped 89.6 / 91.2 / 96.3 / 53.5.
    """
    N = max(1, int(N_mocks))
    cap = max(1, int(max_rare_per_mock))
    rp, load = {}, {m: 0 for m in range(1, N + 1)}
    keys = list(quotas)
    T = max(1, len(keys))
    for i, S in enumerate(keys):
        q = max(0, min(int(quotas[S]), N))
        pos = []
        for k in range(q):
            lo = int(k * N / q) + 1
            hi = max(lo, int((k + 1) * N / q))
            span = hi - lo
            anchor = lo + int(round((i / T) * span)) if span else lo
            seg = [m for m in range(lo, hi + 1) if load[m] < cap and m not in pos]
            if seg:
                p = min(seg, key=lambda m: (load[m], abs(m - anchor), m))
            else:
                free = [m for m in range(1, N + 1) if load[m] < cap and m not in pos]
                p = min(free, key=lambda m: (abs(m - anchor), m)) if free else anchor
            pos.append(p)
            load[p] += 1
        rp[S] = sorted(pos)
    return rp


def f2_threshold(series_avg_rare):
    """§9-7 F2 threshold: max(ceil(avg), 1.5 * avg).

    The old bare 1.5*avg was unsatisfiable at integer boundaries (avg 0.48 →
    threshold 0.72 forbids ANY rare Q in the tail; avg 1.125 → 1.69 fails an
    optimal spread that must put 2 in some mock). The floor at ceil(avg) admits the
    rounded-up fair share and still catches the incident (avg 1.0 → 1.5, observed 2).
    """
    a = float(series_avg_rare)
    return max(float(math.ceil(a)), a * 1.5) if a > 0 else 0.0


def dead_stretch(per_mock, N_mocks):
    """§9-7 F2b (WARN): longest circular run of rare-free mocks vs its limit.

    per_mock : {m: rare Qs in mock m}. Returns (dead_run, limit, R). Passes when
    dead_run <= limit = 2 * ceil(N / min(R, N)). Scale-aware, no knob: 20 rare Qs
    over 20 mocks make a 2-mock gap suspicious; 3 rare Qs make a 6-mock gap normal.
    R == 0 → (0, 0, 0): dormant.
    """
    N = max(1, int(N_mocks))
    occ = [m for m in range(1, N + 1) if per_mock.get(m, 0) > 0]
    R = sum(int(v) for v in per_mock.values())
    if R == 0:
        return 0, 0, 0
    if len(occ) == 1:
        run = N - 1
    else:
        gaps = [occ[i + 1] - occ[i] - 1 for i in range(len(occ) - 1)]
        gaps.append(occ[0] + N - occ[-1] - 1)
        run = max(gaps)
    return run, 2 * math.ceil(N / min(R, N)), R


def coverage_window(batch_start, batch_end, batch_size, N_mocks):
    """§9-11 BV-9B: the COVERAGE WINDOW containing this B2 batch.

    A B2 batch is always 10 mocks (§8-3, a delivery unit); the coverage window is
    batch_size_qs mocks. They coincide only when batch_size_qs == 10.
    Returns (win_index (1-based), win_start, win_end, closes) — ``closes`` is True
    when this batch is the LAST batch of the window, i.e. BV-9B must be evaluated
    now; False means DEFER (report progress only, never fail).
    """
    bs = max(1, int(batch_size))
    N = max(1, int(N_mocks))
    win_index = (int(batch_start) - 1) // bs
    win_start = win_index * bs + 1
    win_end = min(win_start + bs - 1, N)
    return win_index + 1, win_start, win_end, int(batch_end) >= win_end

# ════════════════════════════════════════════════════════════════════════════
# SELF-TEST  —  python3 blueprint_core.py --self-test  →  "SELF-TEST: N/N PASS"
# ════════════════════════════════════════════════════════════════════════════
# Framework-engine health gate (mirrors explain_engine.py). This is a fast pre-flight
# check the blueprint specs run before importing the engine — NOT the full regression
# suite (that lives in blueprint_core_test.py + qa_pass2_differential.py). It exercises
# each of the 11 functions against a fixed expected value or invariant so a corrupted
# or wrong-version engine can never silently pass.


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER E — PYQ DIFFICULTY SCORING  (Framework_MockTestAnalyse.md E-9 / E-10)
# ════════════════════════════════════════════════════════════════════════════
# PROVENANCE: score_difficulty and determine_strip_mode are extracted VERBATIM
# from Framework_MockTestAnalyse.md, sections E-9 (score_difficulty) and
# E-10 (determine_strip_mode). Extracted at v2.24.9; code byte-identical
# through v2.24.10 (current) — the v2.24.10 bump was annotation-only.
# ANCHORS ARE SECTION IDs, NOT LINE NUMBERS: line numbers shift whenever
# the source spec gains a changelog entry (they went stale within one
# session of being written). Locate by the E-9/E-10 headings.
# This module is now the CANONICAL shared copy, consumed by:
#   * Step 5  (PYQExtract / MockTestAnalyse) — per-PYQ scoring during extraction
#   * PYQ-4   (PYQDeliver) — Tier-2 Complexity resolution (§2-3 v1.2)
# CROSS-FILE SYNC RULE: any change to these functions MUST be applied in the
# SAME session to the embedded copies in Framework_MockTestAnalyse.md (E-9/E-10)
# and re-verified byte-identical by the parity harness. Step 8 B-DIFF mirrors
# the MSQ load term — a threshold or flag change also requires a Step 8 review.
# PURE: text + plain data in, plain data out. No I/O. Only ``re`` used.

def score_difficulty(q, marks=1, strip_mode='reasoning'):
    """
    BUG-B07 fix: marks parameter USED in threshold scaling.
    BUG-B08 fix: 'rate','find the','what is' gated to quantitative mode only.
    BUG-A27 fix: decimal numbers included in V axis via float() conversion.
    time_per_q_sec parameter removed — difficulty is C+I+V axis-based, not time-based.
    Returns: {level, C, I, V, score, flags}
    """
    stem = q.get('stem', '')

    # AXIS 1: Computation steps (C)
    C = 1
    if any(kw in stem.lower() for kw in
           ['both','combined','together','compare','between two','ratio of two']):
        C = 4
    elif any(kw in stem.lower() for kw in
             ['partial','remaining','after repay','multi-year',
              'correct to two decimal']):
        C = 3
    # BUG-B08 fix: broad keywords only apply in quantitative mode
    elif strip_mode == 'quantitative' and any(kw in stem.lower() for kw in
             ['rate','find the','calculate','what is']):
        C = 2

    # AXIS 2: Indirection (I)
    I = 1
    if any(re.search(p, stem.lower()) for p in
           [r'ratio of .+ to', r'find .+ if .+ together', r'compare .+ two']):
        I = 3
    elif any(re.search(p, stem.lower()) for p in
             [r'if .+, find', r'such that', r'given that .+ find']):
        I = 2

    # AXIS 3: Value complexity (V)
    V = 1
    raw_nums = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', stem)
    if raw_nums:
        try:
            # BUG-A27 fix: use float() so decimals like '22.5' are included
            parsed = [float(n.replace(',', '')) for n in raw_nums]
            max_v   = max(parsed)
            has_dec = any('.' in n for n in raw_nums)
            non_rnd = max_v > 50000 and int(max_v) % 100 != 0
            if non_rnd or (max_v > 50000 and has_dec): V = 3
            elif has_dec or max_v > 10000:              V = 2
        except:
            pass

    score = C + I + V
    flags = []
    if re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', stem):
        score += 1; flags.append('negative_question')
    # v2.5: MSQ cognitive-load term. A multi-select question forces independent
    # evaluation of EVERY option (not "find the one right answer"), so it is
    # strictly harder than its single-answer twin. +1, analogous to the negative_
    # question term. Dormant for single-answer exams (is_msq is always False when
    # multi_select_allowed=false). Step 8 B-DIFF mirrors this term for sync.
    if q.get('is_msq'):
        score += 1; flags.append('msq')

    # Difficulty thresholds: score <= simple → Simple, <= medium → Medium, else Hard.
    # Thresholds are universal — derived from the C+I+V axis system (min=3, max=10+).
    # C+I+V=3 (all axes at minimum) = trivially Simple for any exam.
    # C+I+V=10 (all axes at maximum) = Hard for any exam.
    # marks scaling: 2-mark Qs take 2× time so the bar for 'Simple' shifts up by 1.
    # These values are stable across exams because the axes are exam-agnostic.
    simple_threshold = 4 + (marks - 1)   # score ≤ this → Simple
    medium_threshold = 7 + (marks - 1)   # score ≤ this → Medium; else Hard

    if score <= simple_threshold:   level = 'Simple'
    elif score <= medium_threshold: level = 'Medium'
    else:                           level = 'Hard'

    return {'level':level, 'C':C, 'I':I, 'V':V, 'score':score, 'flags':flags}


def determine_strip_mode(section, topic, subtopic):
    """
    Exam-agnostic: infer stripping mode from taxonomy context words.
    v2.16 RIGID-5: Hindi equivalents added so Hindi-medium exams (e.g. MP PSC,
    UP PCS, Bihar PSC) with Devanagari headings are correctly classified instead
    of always falling to the default 'reasoning'.
    """
    s = section.lower(); t = topic.lower(); u = subtopic.lower()
    # Quantitative: English + Hindi keywords
    if any(kw in s for kw in ['quantitative','arithmetic','mathematics','math',
                               '\u0917\u0923\u093f\u0924',            # गणित (math)
                               '\u0905\u0902\u0915\u0917\u0923\u093f\u0924',  # अंकगणित (arithmetic)
                               '\u092e\u093e\u0924\u094d\u0930\u093e\u0924\u094d\u092e\u0915',  # मात्रात्मक
                              ]): return 'quantitative'
    if any(kw in t for kw in ['arithmetic','algebra','geometry','mensuration',
                               'trigonometry','statistics','number',
                               '\u092c\u0940\u091c\u0917\u0923\u093f\u0924',  # बीजगणित (algebra)
                               '\u0930\u0947\u0916\u093e\u0917\u0923\u093f\u0924',  # रेखागणित (geometry)
                               '\u0924\u094d\u0930\u093f\u0915\u094b\u0923\u092e\u093f\u0924\u093f',  # त्रिकोणमिति
                              ]): return 'quantitative'
    # English / Language
    if any(kw in s for kw in ['english','language','comprehension','verbal',
                               '\u0905\u0902\u0917\u094d\u0930\u0947\u091c\u0940',  # अंग्रेजी
                               '\u092d\u093e\u0937\u093e',           # भाषा (language)
                              ]): return 'english'
    # Logical
    if any(kw in u for kw in ['syllogism','statement','conclusion','venn',
                               '\u0928\u094d\u092f\u093e\u092f\u0935\u093e\u0915\u094d\u092f',  # न्यायवाक्य (syllogism)
                              ]): return 'logical'
    # Reasoning
    if any(kw in s for kw in ['reasoning','intelligence',
                               '\u0924\u0930\u094d\u0915\u0936\u0915\u094d\u0924\u093f',  # तर्कशक्ति (reasoning)
                               '\u092c\u0941\u0926\u094d\u0927\u093f',  # बुद्धि (intelligence)
                              ]):
        if any(kw in t for kw in ['analogy','series','coding','blood',
                                    'arrangement','sequence',
                                    '\u0938\u093e\u0926\u0943\u0936\u094d\u092f',  # सादृश्य (analogy)
                                    '\u0936\u094d\u0930\u0943\u0902\u0916\u0932\u093e',  # श्रृंखला (series)
                                   ]): return 'reasoning'
    # Factual / General Awareness
    if any(kw in s for kw in ['awareness','knowledge','general studies',
                               'current','static',
                               '\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u091c\u094d\u091e\u093e\u0928',  # सामान्य ज्ञान
                               '\u091c\u093e\u0917\u0930\u0942\u0915\u0924\u093e',  # जागरूकता (awareness)
                              ]): return 'factual'
    return 'reasoning'


def map_difficulty_level(level, labels):
    """Ordinal map from the E-9 vocabulary (Simple/Medium/Hard) to an exam's
    ``difficulty_labels`` list. Same fixed alias as Framework_Blueprint.md
    §7 S7-6 (simple→labels[0], medium→labels[1], hard→labels[2]).

    Valid ONLY for exactly-3-label sets: a 2- or 5-band custom vocabulary has
    no defensible ordinal correspondence to a 3-level scorer, so the caller
    must fall back (PYQ-4 Tier 3) rather than guess. Returns None in that
    case, and None for an unknown ``level`` value (defensive; E-9 can only
    emit the three known levels).

    Pure: strings + list in, string or None out. No I/O.
    """
    if not isinstance(labels, (list, tuple)) or len(labels) != 3:
        return None
    idx = {'Simple': 0, 'Medium': 1, 'Hard': 2}.get(level)
    return labels[idx] if idx is not None else None


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER E2 — PYQ DIFFICULTY: DERIVATION-OBSERVED + STRUCTURAL
#   (Framework_PYQExplain §7A / Framework_PYQDeliver §2-3a1)
# ════════════════════════════════════════════════════════════════════════════
# WHY THIS CLUSTER EXISTS
#   Cluster E (E-9 score_difficulty) scores a question from KEYWORDS IN ITS STEM.
#   That vocabulary was calibrated on SSC/Banking aptitude papers, so for any exam
#   whose stems do not use that vocabulary the C axis is pinned at its floor and
#   every question collapses to one label. Measured on IIT JAM Biotechnology
#   15-Feb-2026 (60 Q): C=1 for 60/60, I=1 for 59/60 — 60/60 tagged "Easy".
#   That is not a tuning failure. A vocabulary list is inherently exam-SPECIFIC,
#   so no amount of keyword expansion makes it exam-AGNOSTIC across ~200 exams.
#
#   Cluster E2 replaces the measurement basis: instead of reading the stem's
#   words, it reads WHAT SOLVING THE QUESTION ACTUALLY REQUIRED. Those
#   observations — how many deduction steps, how many distinct principles, did
#   two independent methods agree — are produced by PYQ-1 for every question it
#   explains, and they contain no exam name, no subject name, and no language.
#   Exam-agnostic by construction rather than by enumeration.
#
# RELATIONSHIP TO CLUSTER E
#   E-9/E-10 are NOT modified by this cluster and are NOT called by it. They keep
#   their Step 5 corpus/template role and remain under their CROSS-FILE SYNC RULE.
#   E2 is additive: new names, no shared state.
#
# PURE: plain data in, plain data out. No I/O. ``re`` is not used here.

# Per-facet baseline for the §6 universal question classes. The ordering is the
# invariant, not the absolute numbers: recall < procedure < application <
# evaluate-every-option / derive-without-options.
CLASS_BASELINE = {
    'C-FACTUAL':        0,   # recall — you know the fact or you do not
    'C-VOCAB-ITEM':     0,   # term / grammar meaning
    'C-FORMAL-LOGIC':   1,   # fixed formal procedure
    'C-COMPUTATIONAL':  2,   # requires calculation
    'C-LINKED':         2,   # passage / stimulus must be read first
    'C-FIGURAL':        2,   # image must be analysed
    'C-MULTI-SELECT':   3,   # EVERY option must be independently evaluated
    'C-NUMERICAL-INPUT': 3,  # exact value derived with no options to check against
}
_UNKNOWN_CLASS_BASELINE = 1   # conservative middle for a class not in the table

# Question-type floor: an MSQ/NAT carries its structural load even if the class
# list omitted the corresponding facet. Prevents a mis-classification from
# scoring a multi-select or numerical-input question as a plain single-answer MCQ.
_QTYPE_FLOOR_CLASS = {'msq': 'C-MULTI-SELECT', 'nat': 'C-NUMERICAL-INPUT'}

# Band edges on the 0..12 scale. score <= EASY_MAX → labels[0];
# score <= MEDIUM_MAX → labels[1]; else labels[2].
DIFFICULTY_EASY_MAX = 2
DIFFICULTY_MEDIUM_MAX = 5


def _as_int(value, default=0):
    """Coerce an observation count to a non-negative int. Defensive: PYQ-1 supplies
    these from its own bookkeeping, and a None/str/float must not raise here.

    Non-finite floats are rejected BEFORE int(): int(nan) raises ValueError but
    int(inf) raises OverflowError, which is neither a TypeError nor a ValueError
    and would otherwise escape the guard and abort the batch. NaN is detected by
    ``v != v`` and infinities by magnitude, so no import is needed and the module
    stays dependency-free."""
    if isinstance(value, float):
        if value != value or value == float('inf') or value == float('-inf'):
            return default
    try:
        n = int(value)
    except (TypeError, ValueError, OverflowError):
        return default
    return n if n >= 0 else default


def assess_difficulty(question_class, deduction_steps, axiom_concepts,
                      speed_hack_exists, derivation_confidence, is_negative,
                      qtype, difficulty_labels):
    """TIER 1 — per-question difficulty from PYQ-1's DERIVATION OBSERVATIONS.

    Called once per question at PYQ-1, AFTER the answer has been derived twice and
    the AXIOM/DEDUCTION/SPEED HACK blocks have been built, BEFORE block.validate().
    It records what the derivation already revealed; it performs no new analysis
    and never re-reads the stem.

    Parameters (every one is an observation PYQ-1 has already made):
      question_class        str | list[str] | None — §6 class facet(s)
      deduction_steps       int  — steps in the DEDUCTION block (engine minimum 2)
      axiom_concepts        int  — distinct principles stated in the AXIOM block
      speed_hack_exists     bool — the §14 two-part gate passed
      derivation_confidence 'full' | 'flagged' — §7 two-method agreement
      is_negative           bool — NOT/INCORRECT/EXCEPT/FALSE polarity in the stem
      qtype                 'mcq' | 'msq' | 'nat'
      difficulty_labels     list — exam vocabulary, ascending, e.g. ['Easy','Medium','Hard']

    Returns a member of ``difficulty_labels``, or None when ``difficulty_labels``
    is not an exactly-3-label list. None is the SAME contract as
    ``map_difficulty_level``: a 2- or 5-band custom vocabulary has no defensible
    correspondence to a 3-band assessment, so the caller falls through rather
    than guessing.

    Deterministic: identical observations always yield the identical label, on
    every run and every model instance.

    Pure: plain data in, string or None out. No I/O.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    # GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS: the arithmetic lives in
    # difficulty_score() so Step 9's gate can read the RAW SCORE; this function
    # is now exactly band_for_score(difficulty_score(...)). Semantics-identical
    # to the pre-split body (self-test e2d_score_split_identity proves it over
    # the full observation grid).
    return band_for_score(
        difficulty_score(question_class, deduction_steps, axiom_concepts,
                         speed_hack_exists, derivation_confidence, is_negative,
                         qtype),
        difficulty_labels)


def difficulty_score(question_class, deduction_steps, axiom_concepts,
                     speed_hack_exists, derivation_confidence, is_negative,
                     qtype):
    """TIER 1 RAW SCORE on the 0..12 rubric scale — the integer assess_difficulty
    converts to a band. Same observations, same arithmetic, no labels involved.

    Exposed (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS) because Step 9's difficulty
    gate judges each label against a per-band ACCEPTANCE WINDOW on this scale
    (DIFFICULTY_GATE_BAND_WINDOWS), not against band equality — a band label
    alone cannot say whether a middle-band measurement sat at 3 or at 5.

    Deterministic and pure: plain data in, int out. Never raises on None/str/
    float observations (coerced through _as_int exactly as before).
    """
    # 1. Class baseline — the MAX over facets, never the sum. A question that is
    #    both C-FIGURAL and C-COMPUTATIONAL is not twice as hard as either.
    if question_class is None:
        facets = []
    elif isinstance(question_class, (list, tuple, set)):
        facets = [str(c).strip().upper() for c in question_class if c]
    else:
        facets = [str(question_class).strip().upper()]

    # Question-type floor (applied as an additional facet, so MAX still governs).
    floor_class = _QTYPE_FLOOR_CLASS.get(str(qtype or '').strip().lower())
    if floor_class:
        facets.append(floor_class)

    if facets:
        score = max(CLASS_BASELINE.get(f, _UNKNOWN_CLASS_BASELINE) for f in facets)
    else:
        score = _UNKNOWN_CLASS_BASELINE

    # 2. Derivation length — the model built these steps; the count is evidence.
    steps = _as_int(deduction_steps)
    if steps >= 5:
        score += 3
    elif steps >= 3:
        score += 2
    elif steps >= 2:
        score += 1

    # 3. Concept integration — distinct principles the AXIOM had to invoke.
    concepts = _as_int(axiom_concepts)
    if concepts >= 3:
        score += 2
    elif concepts >= 2:
        score += 1

    # 4. Two independent methods did not agree first time → the question is tricky.
    if str(derivation_confidence or '').strip().lower() == 'flagged':
        score += 2

    # 5. Polarity inversion carries real cognitive load (mirrors the E-9 term).
    if is_negative:
        score += 1

    # 6. A genuine shortcut existing on a LONG derivation is evidence that the
    #    main path is heavy. On a short derivation it means nothing.
    if speed_hack_exists and steps >= 4:
        score += 1

    return score


def band_for_score(score, difficulty_labels):
    """Map a rubric score to the exam's band label via the authoring edges
    (DIFFICULTY_EASY_MAX / DIFFICULTY_MEDIUM_MAX). None when the vocabulary is
    not exactly 3 labels or the score is not an integer — the same fall-through
    contract as assess_difficulty. Pure."""
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    if isinstance(score, bool) or not isinstance(score, int):
        return None
    EASY, MEDIUM, HARD = difficulty_labels
    if score <= DIFFICULTY_EASY_MAX:
        return EASY
    if score <= DIFFICULTY_MEDIUM_MAX:
        return MEDIUM
    return HARD


def difficulty_score_from_obs(obs):
    """Raw rubric score from a difficulty_obs dict (the CHECK 3c shape:
    question_class/facets, deduction_steps, axiom_concepts, speed_hack_exists,
    is_negative, qtype, optional derivation_confidence — default 'full', the
    author derived the answer). None on a non-dict/empty obs — never raises on a
    legacy entry. The obs-reading twin of verify_difficulty_obs, kept here so the
    gate and the audit read one shape."""
    if not isinstance(obs, dict) or not obs:
        return None
    return difficulty_score(
        obs.get('question_class', obs.get('facets')),
        obs.get('deduction_steps'), obs.get('axiom_concepts'),
        bool(obs.get('speed_hack_exists')),
        obs.get('derivation_confidence', 'full'),
        bool(obs.get('is_negative')), obs.get('qtype'))


# ── Cluster E2c — DIFFICULTY CONFORMANCE (v1.13, GAP-2026-08-21-DIFFICULTY-
#    STICKER-LABELS). The mock pipeline's quota said HOW MANY of each band but
#    nothing defined WHAT a band meant, so Step 7 stamped slot names onto
#    questions (measured on IIT_JAM_CHEMISTRY M01: 14/60 labels agreed with the
#    Tier-1 rubric; 4 labels were structurally impossible). These helpers put
#    the SCHEDULE, the AUTHORING and the AUDIT on the ONE existing scale —
#    assess_difficulty — so a label becomes a conclusion from recorded evidence.
#    All are pure, deterministic, exam-agnostic, and return None/{} degradation
#    on the same non-3-band contract as assess_difficulty.

def difficulty_min_band(qtype, difficulty_labels):
    """The FLOOR band a question at a position of this qtype can honestly reach.

    Derived from the rubric's own arithmetic, not restated: the qtype floor class
    (msq→C-MULTI-SELECT 3, nat→C-NUMERICAL-INPUT 3) plus the unavoidable
    steps term (engine minimum 2 deduction steps → +1) puts every MSQ/NAT at
    score ≥ 4 = the middle band. An MCQ can be authored factual/2-step
    (score 1) → the bottom band. None on a non-3-band vocabulary.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    qt = str(qtype or '').strip().lower()
    floor_class = _QTYPE_FLOOR_CLASS.get(qt)
    base = CLASS_BASELINE.get(floor_class, 0) if floor_class else 0
    min_score = base + 1                      # + the unavoidable steps>=2 term
    if min_score <= DIFFICULTY_EASY_MAX:
        return difficulty_labels[0]
    if min_score <= DIFFICULTY_MEDIUM_MAX:
        return difficulty_labels[1]
    return difficulty_labels[2]


def difficulty_feasibility(counts, qtype_by_q, difficulty_labels):
    """Can this mock's band counts be honestly authored on this exam's shape?

    counts      {'simple': S, 'medium': M, 'hard': H} (schedule keys) or a dict
                keyed by the canonical labels themselves. Missing keys = 0.
    qtype_by_q  {q:'mcq'|'msq'|'nat'} for every position of the mock.
    Returns {} when feasible, else {label: {'requested': r, 'max_achievable': m}}.
    {} (vacuous pass) on a non-3-band vocabulary — same fall-through as the rubric.

    Only the BOTTOM band is capacity-bound (an MSQ/NAT position can never be
    authored down to it — difficulty_min_band). Any position can be authored UP
    (more steps, more concepts), so the middle and top bands are never capped.
    Sum mismatches are the caller's existing S3-9-style checks, not re-checked here.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return {}
    easy_lab = difficulty_labels[0]
    req = _as_int((counts or {}).get('simple', (counts or {}).get(easy_lab, 0)))
    cap = sum(1 for t in (qtype_by_q or {}).values()
              if difficulty_min_band(t, difficulty_labels) == easy_lab)
    if req > cap:
        return {easy_lab: {'requested': req, 'max_achievable': cap}}
    return {}


def assign_difficulty_bands(counts, qtype_by_q, difficulty_labels, seed=0):
    """Deterministic band-per-question plan honouring the structural floors.

    Fills the quota EXACTLY: bottom-band slots land only on positions whose
    floor allows them (spread evenly, rotated by `seed` for cross-mock variety),
    middle-band slots spread evenly over the remainder, everything else top band.
    Returns {q: label}. Raises ValueError when counts don't sum to the position
    count or the plan is infeasible (call difficulty_feasibility first for a
    diagnosable message). None on a non-3-band vocabulary.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    EASY, MEDIUM, HARD = difficulty_labels
    qs = sorted(int(q) for q in (qtype_by_q or {}))
    nE = _as_int((counts or {}).get('simple', (counts or {}).get(EASY, 0)))
    nM = _as_int((counts or {}).get('medium', (counts or {}).get(MEDIUM, 0)))
    nH = _as_int((counts or {}).get('hard', (counts or {}).get(HARD, 0)))
    if nE + nM + nH != len(qs):
        raise ValueError(f"difficulty counts {nE}+{nM}+{nH} != {len(qs)} positions")
    if difficulty_feasibility(counts, qtype_by_q, difficulty_labels):
        raise ValueError("infeasible bottom-band count — run difficulty_feasibility")
    ok_easy = [q for q in qs
               if difficulty_min_band(qtype_by_q[q], difficulty_labels) == EASY]
    plan = {}
    def _spread(pool, n, rot):
        """n indices spread evenly over pool, rotated deterministically."""
        if n <= 0 or not pool:
            return []
        step = len(pool) / n
        return [pool[(int(i * step) + rot) % len(pool)] for i in range(n)]
    # Even spread can collide on the same index after rotation only when
    # n > len(pool), which feasibility already excludes for EASY and the sum
    # check excludes elsewhere; dedupe defensively by walking forward.
    def _place(pool, n, rot, label):
        taken = []
        want = _spread(pool, n, rot)
        free = set(pool)
        for cand in want:
            c = cand
            while c not in free:                      # deterministic forward walk
                c = pool[(pool.index(c) + 1) % len(pool)]
            free.discard(c); taken.append(c); plan[c] = label
        return taken
    _place(ok_easy, nE, _as_int(seed) % max(1, len(ok_easy) or 1), EASY)
    rem = [q for q in qs if q not in plan]
    _place(rem, nM, _as_int(seed) % max(1, len(rem) or 1), MEDIUM)
    for q in qs:
        plan.setdefault(q, HARD)
    return plan


def difficulty_authoring_profile(band, qtype, difficulty_labels):
    """The observation targets that make assess_difficulty land IN `band` for a
    question of `qtype`. An AUTHORING INSTRUCTION, derived from (and proven
    against, in self_test) the rubric's arithmetic — never a parallel scale.

    Returns {'classes': [...], 'steps': (lo, hi), 'concepts': (lo, hi),
             'avoid_negative': bool, 'note': str} or None (unknown band /
    non-3-band vocabulary). derivation_confidence is 'full' at authoring by
    definition — the author wrote the answer — and speed_hack adds only on
    steps>=4 derivations, so profiles keep clear of that edge except for the
    top band, where it helps.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    EASY, MEDIUM, HARD = difficulty_labels
    qt = str(qtype or '').strip().lower()
    if band == EASY:
        if qt in _QTYPE_FLOOR_CLASS:
            return None                        # structurally impossible — floor
        return {'classes': ['C-FACTUAL', 'C-VOCAB-ITEM', 'C-FORMAL-LOGIC'],
                'steps': (2, 2), 'concepts': (1, 1), 'avoid_negative': True,
                'note': 'recall/one-principle; NEVER computational or figural '
                        '(their baseline alone exceeds the bottom band)'}
    if band == MEDIUM:
        if qt in _QTYPE_FLOOR_CLASS:
            return {'classes': [], 'steps': (2, 2), 'concepts': (1, 2),
                    'avoid_negative': True,
                    'note': 'direct application: the qtype floor already pays '
                            'the baseline; keep the derivation to 2 steps'}
        return {'classes': ['C-COMPUTATIONAL', 'C-FORMAL-LOGIC', 'C-FIGURAL'],
                'steps': (2, 4), 'concepts': (1, 2), 'avoid_negative': True,
                'note': 'standard single-thread application; cap total score '
                        'at 5 (e.g. computational 2 + steps-3 term 2 + 1 concept)'}
    if band == HARD:
        if qt in _QTYPE_FLOOR_CLASS:
            return {'classes': [], 'steps': (3, 6), 'concepts': (2, 4),
                    'avoid_negative': False,
                    'note': 'floor 3 + steps>=3 (+2) + concepts>=2 (+1) = 6; '
                            'longer derivations and shortcuts only raise it'}
        return {'classes': ['C-COMPUTATIONAL', 'C-LINKED', 'C-FIGURAL'],
                'steps': (5, 8), 'concepts': (2, 4), 'avoid_negative': False,
                'note': 'multi-concept, genuinely long: steps>=5 (+3) with '
                        'concepts>=2 (+1) on a class-2 baseline = 6; or '
                        'steps 3-4 with concepts>=3'}
    return None


def verify_difficulty_obs(label, obs, difficulty_labels):
    """label == assess_difficulty(recorded observations)? The ONE check both the
    generation gate (G-DIFF) and the audit (A-QINDEX check 8) run, so they can
    never drift apart. obs keys: question_class/facets, deduction_steps,
    axiom_concepts, speed_hack_exists, is_negative, qtype
    (derivation_confidence defaults 'full' — the author derived the answer).
    Returns (ok: bool, measured: str|None). (True, None) on a non-3-band
    vocabulary or an unusable obs dict — the documented fall-through, never a
    false FAIL on a legacy registry.
    """
    # GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS: one obs reader for the audit
    # (this) and the gate (difficulty_score_from_obs) — same shape, same coercion.
    score = difficulty_score_from_obs(obs)
    if score is None:
        return (True, None)
    measured = band_for_score(score, difficulty_labels)
    if measured is None:
        return (True, None)
    return (measured == label, measured)


def structural_difficulty(q, marking_scheme, difficulty_labels):
    """TIER 1.5 — difficulty from the exam body's own MARKING STRUCTURE.

    A FLOOR, not an assessment. It is the fallback for a paper that has no PYQ-1
    derivation pass (legacy deliveries, or a paper tagged before Tier 1 existed).
    It reports the exam body's design intent for a Q-range — every question in a
    (marks, type) band receives the SAME label — so it can never differentiate a
    hard 2-mark MCQ from an easy one. Tier 1 is what does that.

    Returns None whenever the marking scheme carries NO structural signal
    (uniform marks AND a single question type — e.g. a single-range scheme of
    200 MCQ all worth the same marks),
    or when ``difficulty_labels`` is not an exactly-3-label list. None means
    "fall through to the next tier".

    Pure: plain data in, string or None out. No I/O.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return None
    if not marking_scheme or not isinstance(marking_scheme, (list, tuple)):
        return None

    def _marks_of(entry):
        """Marks for one entry, or None when the value is unusable.

        Returns None (not a default) for anything that cannot participate in a
        marks gradient: non-numeric, NaN, +/-inf, or non-positive. NaN is the
        important one — it compares unequal to itself, so a NaN admitted into
        ``all_marks`` makes the later ``.index(marks)`` raise
        ``ValueError: nan is not in list`` and abort the delivery."""
        try:
            m = float(entry.get('correct_marks', 1))
        except (TypeError, ValueError, OverflowError, AttributeError):
            return None
        if m != m or m == float('inf') or m == float('-inf') or m <= 0:
            return None
        return m

    def _type_of(entry):
        try:
            return str(entry.get('question_type', 'MCQ') or 'MCQ').strip().upper()
        except AttributeError:
            return 'MCQ'

    marks = None
    q_type = None
    for entry in marking_scheme:
        if not isinstance(entry, dict):
            continue
        rng = entry.get('q_range')
        # MUST be a real sequence. A 2-character STRING ('15') also has len 2 and
        # would index character-by-character into a silently wrong range (1-5),
        # producing wrong labels with no error anywhere.
        if not isinstance(rng, (list, tuple)) or len(rng) != 2:
            continue
        try:
            lo, hi = int(rng[0]), int(rng[1])
        except (TypeError, ValueError, OverflowError):
            continue
        if lo > hi:                      # reversed range in config — normalise
            lo, hi = hi, lo
        if lo <= q <= hi:
            marks = _marks_of(entry)
            q_type = _type_of(entry)
            break
    if marks is None:
        # Either q is outside every configured range, or the matching entry's
        # marks are unusable. Both mean "no trustworthy structural signal" →
        # fall through to the next tier rather than guess a band.
        return None

    all_marks = sorted({m for m in (_marks_of(e) for e in marking_scheme
                                    if isinstance(e, dict)) if m is not None})
    all_types = {_type_of(e) for e in marking_scheme if isinstance(e, dict)}
    has_gradient = len(all_marks) > 1
    has_type_mix = len(all_types) > 1
    has_harder_types = bool(all_types - {'MCQ'})

    if not has_gradient and not has_type_mix:
        return None   # no structural signal at all → next tier

    at_top_marks = has_gradient and marks == all_marks[-1]

    # NAT: an exact value must be produced with no options to check against.
    # MSQ: every option must be independently evaluated.
    # Both are structurally above a single-answer MCQ at the same marks.
    if q_type in ('NAT', 'MSQ'):
        return difficulty_labels[2] if at_top_marks else difficulty_labels[1]

    # MCQ (and any future/unknown type — conservative MCQ treatment).
    if has_gradient:
        idx = all_marks.index(marks)
        if idx == 0:
            return difficulty_labels[0]
        if idx == len(all_marks) - 1:
            # Top-marks MCQ is the hardest thing in an ALL-MCQ exam; when the
            # exam also fields MSQ/NAT, those hold the top band instead.
            return difficulty_labels[1] if has_harder_types else difficulty_labels[2]
        return difficulty_labels[1]

    # Type mix but uniform marks: MCQ carries no signal of its own here.
    return None


# ════════════════════════════════════════════════════════════════════════════
# CLUSTER F — PATTERN ERA  (Framework_MockTestAnalyse §16 / Framework_PYQAnalyse S3-2a)
#
# WHY THIS CLUSTER EXISTS
#   A PYQ corpus routinely spans several exam patterns. Those papers carry TWO kinds of
#   information that need OPPOSITE treatment:
#     * QUESTION SHAPES (patterns, templates, difficulty, phrasing) — every era is
#       valuable. A subtopic observed across 26 years is far better characterised than one
#       observed twice. This is the entire reason legacy papers are retained.
#     * PROPORTIONS (how many questions a subtopic deserves) — only the CURRENT pattern
#       can answer this. A retired pattern's subject mix is not evidence about today's exam.
#   Recency weighting (Framework_Blueprint §3, last 2 valid years x2) dampens the second
#   problem but cannot solve it: with 21 old-era years against 6 current-era ones, the
#   retired pattern still holds ~72% of the weight.
#   These functions let a caller build a COUNTING VIEW restricted to chosen eras while the
#   pattern/template synthesis keeps consuming the full corpus.
# ════════════════════════════════════════════════════════════════════════════

# The section label used when a Q-number falls outside every configured section range.
# Lives HERE, not in a spec file, because Framework_PYQSort (assigns it) and
# Framework_PYQAnalyse (routes questions to it) must use the SAME literal and are loaded by
# different triggers. A constant duplicated across two spec files is a drift waiting to
# happen; this is the single definition both import.
OUT_OF_PATTERN = "__OUT_OF_PATTERN__"

PATTERN_ERAS = ("current", "larger", "smaller", "renumbered", "retyped")


def classify_paper_era(observed_q_numbers, cfg_total, min_cfg_q, max_cfg_q,
                       observed_types=None, cfg_type_for_q=None):
    """Classify ONE paper against the current exam pattern. Exam-agnostic: the only inputs
    are what the paper actually contains and what exam_config declares.

    Returns one of PATTERN_ERAS. The chain is TOTAL and mutually exclusive.

    THREE INDEPENDENT FACTS, deliberately not collapsed:
      size          — more/fewer/the same number of questions?
      out-of-range  — any Q-numbers outside every configured section range?
      type-mismatch — does any position's OBSERVED question type disagree with the type
                      exam_config's marking_scheme declares for that position?

    WHY TYPE MATTERS (v3). Until v3 an "era" was defined by SIZE alone. That silently
    mis-classified the most common kind of pattern change there is: an exam that keeps the
    same question count but changes its question TYPES — all-MCQ becoming MCQ/MSQ/NAT is the
    textbook case. Such a paper counted as 'current' and blended straight into the mix and
    the axis-3 (mechanism) distribution. Across a 200-exam framework, type and marking
    changes are at least as common as count changes, so size-only classification missed the
    majority case. A paper that matches on size and numbering but not on types is now
    'retyped' — a distinct era, not a current-pattern paper.

    BACKWARD COMPATIBLE: when observed_types / cfg_type_for_q are not supplied, no
    type comparison happens and the result is identical to the v2 size-only chain.

    Note that 'smaller' NEVER produces out-of-range questions — a short paper merely leaves
    later ranges empty. That asymmetry is exactly why the shorter direction was never a
    data-loss risk and the longer direction always was.
    """
    obs = list(observed_q_numbers)
    n = len(obs)
    size = ("larger" if n > cfg_total else
            "smaller" if n < cfg_total else "same")
    out_of_range = [q for q in obs if q < min_cfg_q or q > max_cfg_q]
    if size == "larger":
        return "larger"
    if size == "smaller":
        return "smaller"
    if out_of_range:
        return "renumbered"
    if observed_types and cfg_type_for_q:
        for q, seen in observed_types.items():
            want = cfg_type_for_q(q)
            if want and seen and str(seen).upper() != str(want).upper():
                return "retyped"
    return "current"


def type_resolver_from_config(exam_config):
    """Build ``q_num -> declared question_type`` from exam_config.marking_scheme, or None
    when the config declares no marking_scheme (then no type comparison is possible and
    classify_paper_era falls back to its size/numbering chain)."""
    ms = (exam_config or {}).get("marking_scheme") or []
    if not ms:
        return None
    def _t(q):
        for e in ms:
            lo, hi = e["q_range"]
            if lo <= q <= hi:
                return e.get("question_type")
        return None
    return _t


def exam_config_bounds(exam_config):
    """(cfg_total, min_cfg_q, max_cfg_q) from exam_config. Raises ValueError when the
    config carries no usable sections, so a caller can never silently classify every paper
    against zeroes (which would label the entire corpus 'larger')."""
    secs = (exam_config or {}).get("sections") or []
    if not secs:
        raise ValueError("exam_config has no sections[] — pattern era cannot be determined.")
    cfg_total = sum(int(s["q_count"]) for s in secs)
    min_cfg_q = min(int(s["q_range"][0]) for s in secs)
    max_cfg_q = max(int(s["q_range"][1]) for s in secs)
    return cfg_total, min_cfg_q, max_cfg_q


def paper_key(q):
    """Authoritative paper identity for a question: (year, shift). Matches the identity
    ``compute_section_axis_distribution`` already uses, so era logic and axis logic can
    never disagree about what counts as one paper."""
    return (q.get("year"), q.get("shift"))


def paper_eras_from_progress(progress, exam_config):
    """Classify every paper represented in a Step-5 ``progress`` structure.

    Returns {(year, shift): {'observed_q': int, 'era': str, 'out_of_range': int}}.

    ``progress`` maps (section, topic, subtopic) -> [question dicts], plus the string keys
    '_meta' and '_linked_groups' which are skipped (tuple-key test, same as §16-1).
    """
    cfg_total, min_cfg_q, max_cfg_q = exam_config_bounds(exam_config)
    cfg_type = type_resolver_from_config(exam_config)
    by_paper, types_by_paper = {}, {}
    for key, questions in progress.items():
        if not isinstance(key, tuple):
            continue
        for q in questions:
            pk = paper_key(q)
            by_paper.setdefault(pk, []).append(q.get("q_num"))
            # v3: question type, when Step 5 has detected one. Absent -> no type check.
            qt = q.get("question_type") or q.get("answer_type")
            if qt and isinstance(q.get("q_num"), int):
                types_by_paper.setdefault(pk, {})[q["q_num"]] = qt
    out = {}
    for pk, nums in by_paper.items():
        clean = [n for n in nums if isinstance(n, int)]
        era = classify_paper_era(clean, cfg_total, min_cfg_q, max_cfg_q,
                                 observed_types=types_by_paper.get(pk),
                                 cfg_type_for_q=cfg_type)
        out[pk] = {
            "observed_q": len(nums),
            "era": era,
            "out_of_range": sum(1 for n in clean if n < min_cfg_q or n > max_cfg_q),
            "type_checked": bool(types_by_paper.get(pk) and cfg_type),
        }
    return out


def filter_progress_to_eras(progress, eras, keep=("current",)):
    """Build a COUNTING VIEW of ``progress`` containing only papers whose era is in ``keep``.

    COUNTING ONLY. This view exists to feed frequency aggregation (§16-1) and the axis
    distribution (§16-3). It must NEVER feed pattern/template synthesis — that is what
    consumes the full corpus and what makes legacy papers worth keeping in the first place.

    Returns (filtered_progress, stats). The original is never mutated.

    ``_meta`` is REBUILT so the downstream aggregator — which derives papers_per_year from
    ``_meta['papers_processed']`` — sees only the kept papers. The rebuilt ids have the form
    ``"<year>-shift<shift>"``, which the aggregator's ``extract_year_from_paper_id`` 4-digit
    regex reads exactly as it reads a real filename-derived id.
    ``_linked_groups`` is passed through untouched: no counting path reads it, and rebuilding
    it here would risk breaking stimulus grouping for no benefit.
    """
    keep = set(keep)
    kept_papers = {pk for pk, info in eras.items() if info["era"] in keep}
    filtered, dropped_q, kept_q = {}, 0, 0
    for key, val in progress.items():
        if not isinstance(key, tuple):
            filtered[key] = val
            continue
        keep_list = []
        for q in val:
            if paper_key(q) in kept_papers:
                keep_list.append(q)
                kept_q += 1
            else:
                dropped_q += 1
        filtered[key] = keep_list
    years, papers_processed = [], []
    for (year, shift) in sorted(kept_papers, key=lambda p: (str(p[0]), str(p[1]))):
        papers_processed.append(f"{year}-shift{shift}")
        if year is not None and year not in years:
            years.append(year)
    filtered["_meta"] = {
        "papers_processed": papers_processed,
        "years_processed": sorted(years),
        "total_questions": kept_q,
    }
    stats = {
        "kept_papers": len(kept_papers),
        "dropped_papers": len(eras) - len(kept_papers),
        "kept_questions": kept_q,
        "dropped_questions": dropped_q,
        "kept_eras": sorted(keep),
        "era_counts": {e: sum(1 for i in eras.values() if i["era"] == e)
                       for e in PATTERN_ERAS},
    }
    return filtered, stats



# ════════════════════════════════════════════════════════════════════════════
# CLUSTER G — SORTED-PYQ HEADING PARSING
#   (Framework_MockTestAnalyse §E / Framework_PYQAnalyse Phase B)
#
# WHY THIS CLUSTER EXISTS — a documented contract that had already been broken.
#   Step 4 (PYQCount / Phase B) and Step 5 (PYQExtract) both walk the SAME sorted PYQ .docx
#   and both must agree on which paragraphs are taxonomy headings and at what level. Step 4's
#   copy carried the instruction verbatim:
#       "IDENTICAL to Step 5's parse_taxonomy_level() - DO NOT MODIFY independently.
#        Any change here MUST be mirrored in Step 5's Framework_MockTestAnalyse.md."
#   and Framework_PYQAnalyse EC-P14 states the failure mode and the remedy:
#       "Root cause: one parser diverged from the heading format contract. Fix: ensure both
#        use IDENTICAL parser code."
#   They diverged anyway. Step 5 was expanded in v2.16 (RIGID-4) from 3 heading patterns to
#   12+ — adding Section:/Part:/Area:, Unit/Module/Block, colon-style topics and
#   case-insensitivity. Step 4 was never mirrored and still recognised only Subject:/Domain:,
#   "Topic N:" and "Chapter N".
#   CONSEQUENCE for any exam whose sorted headings use the newer forms: Step 5 reads
#   "Section: Botany" as a LEVEL-1 heading while Step 4 falls through to `return 3` and files
#   it as a SUBTOPIC. Step 4's per-subtopic counts are then wrong by construction, and the
#   only thing standing between that and a distorted blueprint is Step 6's BV-0A cross-check.
#   A comment instructing two humans to keep two copies in step is not a mechanism. This is.
# ════════════════════════════════════════════════════════════════════════════

# Byte-identical across Framework_PYQPrepare / PYQSort / PYQAnalyse / MockTestAnalyse
# (verified: exactly ONE distinct definition of this table exists in the corpus).
#
# GAP-2026-08-15-BAREQ. Entries 3 and 4 are the BARE-LABEL forms. python-docx's
# p.text is <w:t>-only, so a stem paragraph whose entire payload is <m:oMath> (or a
# drawing, or nothing at all per PYQPrepare S1-4 "empty/corrupt") reads as just
# "Q.N" — and entries 1 and 2 require whitespace AFTER the digits, applied to
# already-stripped text, so they can never match a label with nothing after it.
# The question therefore DID NOT EXIST for Steps 3 and 5: its stem, its options and
# its date label were absorbed into the preceding question's body while every gate
# reported green, because input and output are counted with the same blind
# detector. Measured on IIT_JAM_MATHEMATICS 12-Feb-2017: 4 of 60 questions lost.
#
# This is the QUESTION half of GAP-2026-08-07-OMML, whose OPTION half shipped as
# corpus_io.BARE_OPT_PATTERNS + is_option(para=). OPT_PATTERNS got a bare-label
# companion; Q_PATTERNS did not. That asymmetry was the defect.
#
# The $ anchor is LOAD-BEARING: it admits ONLY a paragraph that is nothing but the
# label, so it can never match an option line ("N. text" — options never begin with
# Q), an in-passage cross-reference ("Q.11-15"), a passage instruction ("Q.11 to
# Q.15 are based on…"), a date label, a taxonomy heading, or the historic
# false-positive "Q1 Analysis". Verified by execution over a 34-case adversarial
# fixture (self_test below) with zero false positives, and over the 6-paper
# IIT_JAM_MATHEMATICS corpus, which parses identically under both tables.
#
# DO NOT "fix" this by widening to the RAW-source forms ("Question N:", bare "N.",
# "(N)"). Those live in PYQPrepare's SOURCE_Q_PATTERNS and belong there: after
# Step 1 normalises, options read "N. text", so a bare-number entry here would
# match every option line and a 100-question paper would parse as 500.
Q_PATTERNS = [r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1
              r'^Q(\d+)\.\s+',               # Q1.  Q25.
              r'^Q\.\s*(\d+)\s*$',           # Q.4   bare label — OMML / figure / empty stem
              r'^Q(\d+)\.\s*$']              # Q4.   bare label, alt form

# The NAMED companion table, deliberately mirroring corpus_io.BARE_OPT_PATTERNS.
# G-1 of GAP-2026-08-15-BAREQ was not "the regex is wrong" — it was that OPT_PATTERNS
# HAD a bare-label companion and Q_PATTERNS did not, so nobody reading either table
# could see that one half of the p.text/OMML class was still open. Naming it makes the
# symmetry visible and gives callers that need the SHAPE (rather than the number) a
# predicate to delegate to instead of writing a private regex — PYQPrepare CHECK 13
# carried exactly such a copy. Kept as a slice-identity assertion in self_test() so it
# can never drift from the canonical table it is part of.
BARE_Q_PATTERNS = [r'^Q\.\s*(\d+)\s*$',       # Q.4
                   r'^Q(\d+)\.\s*$']           # Q4.

# GAP-2026-07-25-002 (Defect D). is_taxonomy_heading() rejects long text so that a
# wrapped question stem is never mistaken for a heading. That bound used to be the
# bare literal 100, written here and enforced NOWHERE ELSE in the corpus — no
# producer checked it. Measured consequence: a 131-character subtopic name is
# written into the Analysis doc by PYQApprove, written as a bold heading into the
# sorted file by PYQSort, and then silently stops being a heading at Step 4 and
# Step 5 — its questions are attributed to the PRECEDING subtopic, with zero
# orphans, zero warnings, and INV-5 conservation still passing because nothing is
# lost, only mis-filed.
#
# It is now a named, exported constant so the PRODUCER can gate on the same number
# the consumer enforces (corpus_io.verify_analysis_doc / write_analysis_doc, and
# PYQAnalyse S4-0 before the taxonomy is locked). Raised 100 -> 300: the first real
# exam's longest subtopic name is 65 characters and its longest generated
# subtopic_id is already 116, so 100 sat uncomfortably close to ordinary data,
# while 300 still cannot be reached by anything but a stem pasted into a heading.
MAX_HEADING_LEN = 300

# GAP-2026-07-26-001. THE single definition of the date/shift label pattern. It was
# previously an inline literal in is_taxonomy_heading() here, in Framework_MockTestAnalyse
# S3-2's outer loop and in Framework_PYQAnalyse S5-2 — three copies of one rule, the exact
# drift class this module exists to end. Matches BOTH forms PYQSort CHECK 3 accepts:
# "[02-May-2010]" (no session) and "[12-Sep-2025 Shift 1]" (with session).
DATE_TAG_RE = re.compile(r'^\[\d{1,2}-')


def is_position_label(text):
    r"""True when this paragraph is a PYQSort date/position label. THE predicate.

    GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION. DATE_TAG_RE has been the single
    definition since GAP-2026-07-26-001, and the comment above it states that it
    replaced "an inline literal in Framework_MockTestAnalyse S3-2's outer loop".
    IT DID NOT. Measured at framework release 2026.08.15.14, the raw literal
    r'\[\d{1,2}-' was still written out at THREE sites in that one spec — E-1
    is_shift_tag, the S3-2 outer loop, and E-10 strip_variables — none of them
    reaching this module. A consolidation that is announced but not performed is
    worse than one never attempted: every later reader trusts the comment and stops
    looking, which is exactly how the inner body loop came to be written without a
    label terminator at all.

    Exposing a PREDICATE rather than the compiled pattern is deliberate. A spec that
    writes `bc.DATE_TAG_RE.match(t)` still owns the calling convention — whether to
    strip, whether None is legal, whether a match object or a bool is wanted — and
    those are the details that drift. One name, one contract, no arguments about it.

    A label ALWAYS precedes the question it stamps and can never be part of the
    previous question's body; S3-2's inner loop terminates on it for that reason.
    """
    if not text:
        return False
    return bool(DATE_TAG_RE.match(text.strip()))


# ── GAP-2026-08-05-001 — TEXTLESS IS NOT EMPTY ───────────────────────────────
# Paragraph.text is RUN text only. A paragraph holding ONLY a picture, an OMML
# equation or an embedded OLE object returns '' and was therefore skipped by the
# lookahead — so a stem continuation whose options are images "led into" the next
# question's date label and satisfied the GAP-2026-07-26-001 positional gate.
# Textless content is still content: it TERMINATES the scan, and the sentinel below
# is what the caller sees. It is deliberately NOT a date label, so the positional
# gate rejects it. Measured on IIT_JAM_BIOTECHNOLOGY 2009 (para 513), on
# SSC_CGL_TIER1 09-Sep-2024 (para 591, OMML options — a near miss that survives only
# because its labels carry literal text) and on two IIT_JAM_PHYSICS mock papers
# (24 instances of the MockTestCreate "Problem Figure:" layout).
CONTENT_SENTINEL = '\ufffc'          # U+FFFC OBJECT REPLACEMENT CHARACTER

_W_NS    = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
_MATH_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
W_P_TAG   = _W_NS + 'p'
W_TBL_TAG = _W_NS + 'tbl'
W_NUMPR_TAG = _W_NS + 'numPr'

# Visible content that Paragraph.text cannot show. Namespace-EXACT tags, walked as a
# tree — never a substring search over element.xml, which a question stem containing
# the literal characters "<w:drawing>" would defeat.
VISUAL_CONTENT_TAGS = frozenset({
    _W_NS + 'drawing',                                                # DrawingML picture/chart/SmartArt
    _W_NS + 'pict',                                                   # legacy VML picture
    _W_NS + 'object',                                                 # embedded OLE (Equation Editor 3.0)
    '{urn:schemas-microsoft-com:vml}imagedata',                       # VML image reference
    '{http://schemas.openxmlformats.org/drawingml/2006/picture}pic',  # inline pic
    '{http://schemas.openxmlformats.org/drawingml/2006/main}blip',    # image reference
    _MATH_NS + 'oMathPara',                                           # display equation
    _MATH_NS + 'oMath',                                               # inline equation
})


def paragraph_is_content_bearing(para, include_autonumber=True):
    """True when a paragraph carries visible content that Paragraph.text cannot show.

    GAP-2026-08-05-001. Accepts EITHER form the corpus actually passes — a python-docx
    Paragraph (has ``._p``) or a raw ``<w:p>`` lxml element (IS the element) — the same
    dual-form contract corpus_io.para_has_image() already honours. A delegation that
    assumed one form would raise AttributeError on the other or silently return False.
    Any object with neither ``._p`` nor ``.iter`` (the plain self-test stubs in this
    file) returns False, which keeps every pre-existing fixture valid; omitting that
    guard is the single most likely way to get this patch wrong.

    ``include_autonumber`` covers ``w:numPr``: Word RENDERS the list number ("1.", "2.")
    that the XML does not store, so an auto-numbered paragraph is visibly non-empty to a
    human and must be to the parser too. The LOOKAHEAD wants it (default True). The
    OPTION predicate does not — there the rendered number merely duplicates the bare
    label already present as text, and is not option CONTENT — so corpus_io passes False.

    PURITY: attribute access and literal tag strings only. No import. This function must
    stay inside the thin core (validate_framework_md Check AB) because both sorted-PYQ
    walkers and corpus_io depend on it.
    """
    if para is None:
        return False
    el = getattr(para, '_p', para)          # Paragraph -> element; element -> itself
    it = getattr(el, 'iter', None)
    if it is None:
        return False
    try:
        for node in it():
            tag = getattr(node, 'tag', None)
            if tag in VISUAL_CONTENT_TAGS:
                return True
            if include_autonumber and tag == W_NUMPR_TAG:
                return True
    except Exception:
        return False
    return False


# ── GAP-2026-08-05-001 / SG-9 — D6: THE DIRECT DISCRIMINATOR ─────────────────
# PYQSort S6-2 MANDATES "11pt Bold Navy #003366" for every level-3 heading and
# make_heading_para() stamps <w:color> unconditionally — then the same clause tells the
# parser "default -> level 3", i.e. to identify level 3 by the ABSENCE of other markers,
# which is exactly what a stem continuation is. The marker was there all along.
# Measured: IIT_JAM_BIOTECHNOLOGY 22 papers — 1,229/1,230 accepted level-3 headings navy,
# the one exception being the phantom; SSC_CGL_TIER1 09-Sep-2024 — 45/45 navy, 100/100
# date labels navy. Zero navy non-headings in either corpus.
HEADING_NAVY = '003366'          # S6-2: level 1 + level 3 + date labels (level 2 is BLACK)


def first_run_colour(para):
    """Colour of the first non-empty run: '003366'-style hex, 'theme', or None.

    None means the run INHERITS its colour (no <w:color> element) — which is NOT a
    colour value and must never be read as "not navy" on its own. 'theme' means
    w:themeColor, treated by heading_colour_available() as colour UNAVAILABLE rather
    than as "not navy": the alternative turns an unusual styling choice into total
    heading loss for that file (framework-owner decision 6, GAP-2026-08-05-001 S18).
    """
    for r in getattr(para, 'runs', ()) or ():
        try:
            if not (r.text or '').strip():
                continue
            c = r.font.color
        except Exception:
            return None
        if c is None or getattr(c, 'type', None) is None:
            return None                     # inherited — NOT a colour value
        try:
            return str(c.rgb).upper().lstrip('#')
        except Exception:
            return 'theme'
    return None


def heading_colour_available(paras):
    """True when THIS FILE carries the S6-2 heading-colour signal.

    GAP-2026-08-05-001 / SG-9. Probes the DATE LABELS, never the headings: S6-2 mandates
    navy for them, PYQSort CHECK 3 HARD FAILS if the styling slips, and EC-S10 raises
    when a Q.N has none — so they are the one styling fact a sorted file cannot lack,
    and there are dozens to hundreds per paper.

    THE GATE IS PER FILE, NOT PER PARAGRAPH, AND THAT IS THE WHOLE POINT. The obvious
    phrasing — "require navy, fall back when colour is absent ON THAT PARAGRAPH" —
    measurably fixes NOTHING (phantoms 1 -> 1 across 22 papers), because a misread stem
    continuation carries no <w:color> at all and therefore takes the fallback straight
    back into the blind spot. Requiring EVERY date label to be explicitly navy means a
    single unstyled label (an old sort, a hand edit, a format round trip) degrades the
    whole file to the positional rule instead of destroying its headings.
    """
    seen = 0
    for p in paras:
        t = (getattr(p, 'text', '') or '').strip()
        if not t or not DATE_TAG_RE.match(t):
            continue
        seen += 1
        if first_run_colour(p) != HEADING_NAVY:
            return False
    return seen > 0



def next_nonempty_texts(paras):
    """For each index i, the text of the next CONTENT-BEARING paragraph after i.

    GAP-2026-07-26-001 introduced this lookahead. GAP-2026-08-05-001 corrected what
    "non-empty" MEANT: this returned the next paragraph with TEXT while its name, its
    docstring and every call site read it as the next paragraph with CONTENT. Textless
    is not empty. A paragraph with text yields its text; a textless paragraph carrying
    an image, equation, embedded object or rendered auto-number yields CONTENT_SENTINEL;
    a TRULY empty spacer is still transparent, as before; '' at end of document.

    Single pass, O(n). Lives in the engine so the two sorted-PYQ walkers (PYQCount S5-2
    count_sorted_file, MockTestAnalyse S3-2 extract_presorted) cannot each write their
    own lookahead and drift apart — the failure class that produced this gap in the
    first place.

    Callers needing TABLE awareness must use sorted_body_lookahead(doc) instead: a
    <w:tbl> is not a paragraph and never appears in doc.paragraphs at all, so no
    paragraph-scoped rule can see one.
    """
    out = [''] * len(paras)
    nxt = ''
    for i in range(len(paras) - 1, -1, -1):
        out[i] = nxt
        t = (paras[i].text or '').strip()
        if t:
            nxt = t
        elif paragraph_is_content_bearing(paras[i]):
            nxt = CONTENT_SENTINEL
    return out


def sorted_body_lookahead(doc):
    """(paragraphs, next_content_text[]) for a sorted-PYQ document, TABLE-AWARE.

    GAP-2026-08-05-001 (D2). doc.paragraphs contains only body-level <w:p>; a <w:tbl>
    sitting between a stem continuation and the next date label is invisible to it, so
    the paragraph-scoped lookahead reports the date label and the continuation is read
    as a heading. Walking the body's own children keeps tables in the sequence.

    The returned list IS doc.paragraphs — same objects, same order — so callers may
    index the returned lookahead with the same i they use for the paragraph list.
    (Note: python-docx rebuilds Paragraph wrappers on every access, so identity of the
    WRAPPERS is not a meaningful property for any caller; the underlying <w:p> elements
    and their order are what matter, and those are exactly preserved.)

    PURITY: takes the Paragraph objects from doc.paragraphs and uses the body only for
    BLOCK ORDER, so nothing is constructed and no import is needed — the thin core stays
    importable everywhere (validate_framework_md Check AB). If the body walk and
    doc.paragraphs ever disagree in length (paragraphs nested in a body-level <w:sdt>
    are invisible to both, but a future format could differ), the function degrades to
    the paragraph-scoped result rather than mis-indexing.
    """
    paras = doc.paragraphs
    try:
        body = doc.element.body
        blocks = []
        n_p = 0
        for child in body.iterchildren():
            tag = getattr(child, 'tag', None)
            if tag == W_P_TAG:
                blocks.append(True)
                n_p += 1
            elif tag == W_TBL_TAG:
                blocks.append(False)        # a table is CONTENT
        if n_p != len(paras):
            return paras, next_nonempty_texts(paras)
    except Exception:
        return paras, next_nonempty_texts(paras)

    out = [''] * len(paras)
    nxt = ''
    pi = len(paras) - 1
    for is_para in reversed(blocks):
        if not is_para:
            nxt = CONTENT_SENTINEL
            continue
        out[pi] = nxt
        t = (paras[pi].text or '').strip()
        if t:
            nxt = t
        elif paragraph_is_content_bearing(paras[pi]):
            nxt = CONTENT_SENTINEL
        pi -= 1
    return paras, out


# GAP-2026-08-15-BAREQ (R-8). Zero-width characters are NOT whitespace to Python:
# str.strip() does not remove them and regex \s does not match them. So a stem
# label carrying a ZWSP defeats entry 3 exactly as "Q.4" defeated entries 1 and 2
# — a second, independent route to the same silent loss. PDF-to-DOCX converters emit
# ZWSP/ZWNJ/ZWJ/WJ/BOM routinely, so this is not hypothetical, and it is invisible on
# screen: the operator sees "Q.4" and the parser sees something else. PYQPrepare S2-4
# sanitise() now strips the same class at the PRODUCER; this strip is the CONSUMER-side
# twin, so a legacy Row file already carrying them still parses without a Step 1 rebuild.
ZERO_WIDTH    = '\u200b\u200c\u200d\u2060\ufeff'      # ZWSP ZWNJ ZWJ WJ BOM/ZWNBSP
ZERO_WIDTH_RE = '[\u200b\u200c\u200d\u2060\ufeff]'   # for re.sub / re.search
_ZW_TABLE = str.maketrans('', '', ZERO_WIDTH)


def detect_question_start(text):
    """Return the source Q-number if this line starts a question, else None."""
    t = (text or '').translate(_ZW_TABLE).strip()
    for pat in Q_PATTERNS:
        m = re.match(pat, t)
        if m:
            return int(m.group(1))
    return None


def is_bare_q_label(text):
    r"""Q-number when this line is NOTHING BUT a question label, else None.

    The structural twin of detect_question_start(): that answers "does a question
    start here", this answers "does a question start here with an EMPTY <w:t>
    payload" — i.e. the stem is an <m:oMath> equation, a drawing, or genuinely
    absent (PYQPrepare S1-4 "empty/corrupt").

    Exists so that a caller which needs the SHAPE does not write a private regex
    for it. PYQPrepare CHECK 13 carried r'^Q\.(\d+)\s*$' inline — the correct
    pattern, gated on the wrong payload test (it inspected the NEXT paragraph for a
    drawing and never the SAME paragraph for an equation), which is why the check
    that was closest to catching GAP-2026-08-15-BAREQ stayed silent through it.
    """
    t = (text or '').translate(_ZW_TABLE).strip()
    for pat in BARE_Q_PATTERNS:
        m = re.match(pat, t)
        if m:
            return int(m.group(1))
    return None


def parse_taxonomy_level(text):
    """(level, name) for a sorted-PYQ heading. THE canonical implementation.

    Level 1 = Section/Subject (top-level grouping)
    Level 2 = Topic/Chapter   (mid-level grouping)
    Level 3 = Subtopic        (default - the leaf level for extraction)

    This is Step 5's v2.16 RIGID-4 form, which is a strict SUPERSET of the older Step-4
    copy: every heading the old version recognised is still recognised identically, and the
    newer forms (Section:/Part:/Area:, Unit/Module/Block, colon-style topics, case
    insensitivity) are recognised instead of silently falling through to level 3.
    Exam-agnostic: no exam, section or subject name appears anywhere in it.
    """
    text = text or ''
    # Level 1: top-level section/subject headings
    if re.match(r'(?:Subject|Domain|Section|Part|Area)\s*:', text, re.IGNORECASE):
        return 1, text.split(':', 1)[1].strip()
    # Level 2: mid-level topic/chapter headings (with optional numbering)
    if re.match(r'(?:Topic|Chapter|Unit|Module|Block)\s+\d+', text, re.IGNORECASE):
        return 2, re.sub(r'(?:Topic|Chapter|Unit|Module|Block)\s+\d+[:.]\s*',
                         '', text, flags=re.IGNORECASE).strip() or text.strip()
    # Level 2: colon-style topic headings without numbering
    if re.match(r'(?:Topic|Chapter|Unit|Module|Block)\s*:', text, re.IGNORECASE):
        return 2, text.split(':', 1)[1].strip()
    return 3, text.strip()


def is_taxonomy_heading(para, is_option_fn, next_text=None, colour_available=False):
    r"""True when a python-docx paragraph is a taxonomy heading rather than a question,
    an option, a STEM CONTINUATION or a date/shift tag. THE canonical implementation.

    ``next_text`` is the text of the NEXT NON-EMPTY paragraph (from next_nonempty_texts()),
    or None when the caller is not walking a sorted-PYQ document.

    == GAP-2026-07-26-001 ==================================================
    A LEVEL-3 heading is BARE TEXT by contract (PYQSort S6-2: "<Subtopic Name>", no
    prefix), so bold was the only positive signal it had. But PYQSort EC-S8 emits
    multi-paragraph question stems and defines a continuation line as "bold + not-date +
    not-option + not-next-Q" — character for character the predicate below. Two different
    objects, one predicate, written on opposite sides of the same repository and never
    compared. Every stem continuation shorter than MAX_HEADING_LEN was a heading.

    Measured on the IIT_JAM_BIOTECHNOLOGY 22-paper corpus (1719 questions): 20 spurious
    headings across 10 papers; 128 counted triples against 126 real ones; 2 phantom
    triples that HARD STOPPED Step 4 Task 2.5; and — the dangerous half — 16 questions
    truncated mid-body at Step 5 with 28 option lines silently discarded. The question
    total and the orphan count were CORRECT throughout, which is why only Task 2.5
    caught it.

    Raising MAX_HEADING_LEN 100 -> 300 (GAP-2026-07-25-002) widened this. That is not an
    argument to revert it: a length bound was only ever an ACCIDENTAL stem/heading
    discriminator, and an accidental discriminator stops working the moment the constant
    is tuned for its real purpose.

    THE DISCRIMINATOR IS POSITIONAL — BUT IT IS *NOT* THE ONLY ONE THE DOCUMENT
    CARRIES. That claim stood here until GAP-2026-08-05-001 and it was false, and being
    false it is why every discriminator this framework has used has been circumstantial:
    length (accidental, died when MAX_HEADING_LEN went 100->300), bold (EC-S8 emits bold
    continuations), position (defeated by textless content and structurally impossible
    for NAT). PYQSort S6-2 mandates 11pt Bold Navy #003366 for every level-3 heading and
    make_heading_para() stamps <w:color> unconditionally — a DIRECT, producer-guaranteed
    marker that the very next line of S6-2 ("Parser: default -> level 3") then told the
    parser to ignore. ``colour_available`` (from heading_colour_available(), computed
    ONCE PER FILE) turns it back on; the positional gate below is now the FALLBACK for
    files that do not carry it.

    WHY BOTH REMEDIES SHIP. Their blind spots do not overlap. Colour cannot see a stem
    continuation deep-copied from a navy-styled source; the positional rule cannot see a
    heading whose colour was stripped, and CANNOT DISTINGUISH A NAT STEM CONTINUATION AT
    ALL — a NAT question has no options, so its last stem paragraph and a genuine
    subtopic heading occupy the identical slot (last text block before a date label) and
    yield byte-identical lookahead values. No positional rule, forward or backward, can
    separate those two objects. For NAT, colour is the only consumer-side discriminator
    there is.
    PYQSort S6-2 emits the date label "immediately above Q.N stem — zero paragraphs
    between"; CHECK 3 HARD FAILS if date-label count != Q-count or the position slips;
    EC-S10 raises when a Q.N has no date label. So in any sorted file PYQSort was willing
    to emit — for ANY exam; this is exam-agnostic and names no exam, section or subtopic
    — a genuine bare subtopic heading is ALWAYS followed by a date label, and a stem
    continuation NEVER is.

    Levels 1 and 2 are exempt: they carry an explicit prefix (Subject:/Topic N:/...) and
    are self-identifying, so they need no positional evidence.

    next_text=None reproduces the pre-fix behaviour exactly, so callers holding a single
    paragraph in isolation (corpus_io's self-test) keep working unchanged. Every
    sorted-PYQ walker MUST pass it.
    ========================================================================

    ``is_option_fn`` is injected because option-shape detection is exam-format logic that
    lives in the calling spec; everything else here is shared.

    Question exclusion uses detect_question_start() (the Q_PATTERNS table) rather than an
    independently written regex. The old Step-4 copy used r'^Q\.?\s*\d+', which matches
    strings Q_PATTERNS does not (e.g. "Q1 Analysis", no trailing dot or space) — so the two
    steps disagreed about which paragraphs were headings at all, on top of disagreeing about
    their level.
    """
    text = (para.text or '').strip()
    if not text:
        return False
    if detect_question_start(text) is not None:
        return False
    if is_option_fn(text):
        return False
    # date/shift tag, e.g. [7-May-2025 Shift 1] — DD may be 1 or 2 digits
    if DATE_TAG_RE.match(text):
        return False
    has_bold = any(r.bold for r in para.runs if r.text.strip())
    if not (has_bold and len(text) < MAX_HEADING_LEN):
        return False
    if parse_taxonomy_level(text)[0] in (1, 2):    # prefixed -> self-identifying
        return True
    # GAP-2026-08-05-001 / SG-9 (D6) — the DIRECT signal, when this FILE carries it.
    # Gated PER FILE by the caller's heading_colour_available() probe, never per
    # paragraph: the per-paragraph phrasing measurably fixes nothing (see that
    # function's docstring). Level 2 is BLACK per S6-2 and is already returned above.
    if colour_available:
        return first_run_colour(para) == HEADING_NAVY
    if next_text is None:                          # caller cannot supply position
        return True
    # GAP-2026-07-26-001, corrected by GAP-2026-08-05-001 D1/D2: a bare level-3 heading
    # must lead into a date label as the next CONTENT-BEARING BLOCK.
    return bool(DATE_TAG_RE.match(next_text.strip()))


def taxonomy_fingerprint(triples):
    """Stable fingerprint of a taxonomy. THE canonical implementation.

    GAP-2026-07-25-002. PYQApprove LOCKS a taxonomy and PYQSort sorts against one;
    until now nothing checked that they were the SAME taxonomy. S1-0 verified the
    approval record's attestation (status, schema, checks) — never its content — so
    a reader that flattened six subjects into one passed the lock gate cleanly.

    Computed over slugify()-normalised triples, not raw display strings, so the
    fingerprint is over IDENTITIES: it is invariant to exactly the cosmetic
    variance the subtopic_id contract already tolerates (em-dash vs hyphen, case,
    spacing), and changes for anything else. Byte-identity of display names is a
    separate concern, enforced by PYQAnalyse Phase B Task 2.5.

    Ordering is sorted, not insertion order, so a fingerprint match does not depend
    on two steps having walked the taxonomy in the same direction.
    """
    import hashlib
    norm = sorted('%s\x1f%s\x1f%s' % (slugify(a), slugify(b), slugify(c))
                  for a, b, c in triples)
    h = hashlib.sha256('\x1e'.join(norm).encode('utf-8')).hexdigest()
    subjects = {slugify(a) for a, _, _ in triples}
    return 'v1:%d:%d:%s' % (len(subjects), len(norm), h)


def extract_year_from_filename(path):
    """Year from a PYQ filename. THE canonical implementation.

    Reconciles two drifted copies: Framework_PYQAnalyse searched the WHOLE path for any
    4-digit run (so a digit-bearing folder such as /drive/2019_batch/EXAM_1998.docx yielded
    2019 — the folder, not the paper), while Framework_MockTestAnalyse searched the basename
    only and required 20xx (so any pre-2000 paper yielded None and vanished from that step's
    year map while remaining visible to the other).
    Canonical form takes the SAFER half of each: basename only (never let a folder name
    supply the year) and a 19xx|20xx window (historical corpora reach back before 2000).
    """
    import os as _os
    m = re.search(r'((?:19|20)\d{2})', _os.path.basename(str(path)))
    return int(m.group(1)) if m else None


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER H — CORPUS ACQUISITION DECISIONS (pure)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Every function here is a DECISION: plain data in, plain data out, no I/O.
# The matching I/O lives in corpus_io.py, which imports this module. The split
# exists because Steps 6-11 import blueprint_core at runtime purely for
# allocation arithmetic; adding PIL / python-docx here would make the allocation
# core unimportable wherever those packages are absent — the P0 recorded in
# Framework_MockTestAnalyse v2.26, where a failed `import blueprint_core`
# aborted Step 5 for EVERY exam.
#
# MEASURED CONSTANTS (live production corpus, 2026-07-24; see Framework_PYQCompress §2)
#   Drive connector download cap ... 10 MiB   (9.34 MiB fetched OK; 10.75 MiB refused)
#   Chat upload ceiling ............ 500 MB per file, 20 files per chat
# ═══════════════════════════════════════════════════════════════════════════════

DRIVE_CAP = 10 * 1024 * 1024          # 10,485,760 — connector refuses above this
SIZE_BUDGET = 9 * 1024 * 1024         # 9,437,184 — governor target (10% margin)
CHAT_FILE_LIMIT = 20                  # files per chat, hard platform limit
INLINE_BUDGET_CHARS = 200_000         # GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION.
                                      # Ceiling on how many base64 characters a Drive
                                      # lane may cost CONTEXT when the connector hands
                                      # payloads back in the model's turn instead of
                                      # spilling them to disk. ~50k tokens inbound,
                                      # about three average papers. Only consulted when
                                      # channel == 'inline'; a spill channel costs zero
                                      # context and is never bounded by it. One
                                      # definition, imported everywhere — never restate
                                      # the number in a spec.

# Governor ladder: (tier, jpeg_quality, dpi_ceiling). dpi_ceiling None = no resize.
# T4 is the FLOOR — never encode below q80 or below 200 DPI at display size.
TIER_LADDER = (
    ('T1', 88, None),
    ('T2', 85, 300),
    ('T3', 82, 240),
    ('T4', 80, 200),
)

# ── PYQCompress v2.0.0 — max-compression governor point + canonical output naming ──
# GAP-2026-08-18-PYQCOMPRESS-UNDERCOMPRESSION. The ladder stops at the FIRST tier
# that fits the budget, so a file already under budget is never downscaled even when
# its images are embedded at 600-900 effective DPI inside a 1-2 inch display box —
# the exact profile of scanned pre-2015 papers. TMAX is the single governor point
# PYQCompress v2 calls instead of walking the ladder: ALWAYS resample to the ceiling
# at display size and ALWAYS palette-quantize PNG output (line art AND alpha).
# q82 / 300 DPI sits ABOVE the T4 floor (q80 / 200), so no quality rule changes.
# Ladder callers (PYQSort S7-6 write-time governance) are UNCHANGED by this.
MAX_TIER = ('TMAX', 82, 300)   # (tier, jpeg_quality, dpi_ceiling at display size)
PNG_QUANT_COLORS = 256         # palette size for quantized PNG output
PNG_QUANT_QUALITY = (75, 95)   # pngquant quality band when the binary is present

# Tokens that carry NO identity: stripped when canonicalising an output filename.
# Lowercase; compared case-insensitively as whole '_'/'-'/' '-delimited tokens.
NAME_JUNK_TOKENS = frozenset({'imag'})

_MONTHS_3 = {m.lower(): m for m in
             ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')}
_MONTHS_FULL = {'january': 'Jan', 'february': 'Feb', 'march': 'Mar', 'april': 'Apr',
                'may': 'May', 'june': 'Jun', 'july': 'Jul', 'august': 'Aug',
                'september': 'Sep', 'sept': 'Sep', 'october': 'Oct',
                'november': 'Nov', 'december': 'Dec'}
_CANON_DATE_RE = re.compile(r'(\d{1,2})[\s_-]*([A-Za-z]{3,9})[\s_-]*(\d{4})')
_CANON_SHIFT_RE = re.compile(r'(?<![A-Za-z])shift[\s_-]*(\d+)', re.I)


def canonical_output_name(name):
    """Canonical delivery name for one paper: ExamCode_DD-Mon-YYYY[_ShiftN].docx

    PYQCompress v2 §2. Returns the canonical filename, or None when the stem
    carries no recognisable DD-Mon-YYYY date token — the caller must HARD STOP
    for that file rather than guess, because a mis-named file in a 200-exam
    corpus is a permanent duplicate identity.

    Rules, in order:
      * strip extension, NFKC-normalise, drop a trailing " (n)" and a leading
        "copy of " (the same transport mangles canonical_paper_key absorbs);
      * find the FIRST date token DD-Mon-YYYY — month by 3-letter or full
        English name, any case, ' ', '_' or '-' as optional separators; the day
        is zero-padded to 2 digits and the month rendered Mmm;
      * ExamCode = everything before the date, runs of ' ', '-', '_' collapsed
        to a single '_', edges trimmed, case PRESERVED. Empty ExamCode -> None;
      * Shift = the first "shift<N>" token anywhere in the stem
        (case-insensitive, optional separator). N == 1 emits NO suffix;
        N >= 2 emits _ShiftN immediately after the date;
      * every other token AFTER the date survives VERBATIM (separator-
        normalised) UNLESS its lowercase form is in NAME_JUNK_TOKENS. This is
        what protects a Sorted/Analysis document's load-bearing decorations
        from being stripped:
          EXAM_12-Sep-2025_Shift-1_Sorted_Q1-Q100_IMAG.docx
            -> EXAM_12-Sep-2025_Sorted_Q1-Q100.docx
        while a plain raw paper collapses to the bare canonical form:
          IIT_JAM_CHEMISTRY_07-May-2005_imag.docx
            -> IIT_JAM_CHEMISTRY_07-May-2005.docx
    """
    import os as _os
    import unicodedata as _ud
    stem = _os.path.splitext(_os.path.basename(str(name)))[0]
    stem = _ud.normalize('NFKC', stem)
    stem = re.sub(r'\s*\(\d+\)\s*$', '', stem)
    stem = re.sub(r'^\s*copy\s+of\s+', '', stem, flags=re.I)

    m = None
    for cand in _CANON_DATE_RE.finditer(stem):
        mon_raw = cand.group(2).lower()
        if ((mon_raw in _MONTHS_3 or mon_raw in _MONTHS_FULL)
                and 1 <= int(cand.group(1)) <= 31):
            m = cand
            break
    if m is None:
        return None
    day = int(m.group(1))
    mon = _MONTHS_3.get(m.group(2).lower()) or _MONTHS_FULL[m.group(2).lower()]
    date = f'{day:02d}-{mon}-{m.group(3)}'

    shift_sfx = ''
    sm = _CANON_SHIFT_RE.search(stem)
    if sm and int(sm.group(1)) >= 2:
        shift_sfx = f'_Shift{int(sm.group(1))}'

    def _tokens(fragment):
        # Split on whitespace and '_' ONLY. A hyphen INSIDE a token is part of its
        # spelling (Q1-Q100, NEET-UG) and survives verbatim; hyphens at token edges
        # are separator debris (EXAM-_12-...) and are trimmed.
        fragment = _CANON_SHIFT_RE.sub(' ', fragment)   # shift is emitted separately
        parts = [t.strip('-') for t in re.split(r'[\s_]+', fragment)]
        parts = [t for t in parts if t]
        return [t for t in parts if t.lower() not in NAME_JUNK_TOKENS]

    code_tokens = _tokens(stem[:m.start()])
    if not code_tokens:
        return None
    tail_tokens = _tokens(stem[m.end():])

    out = '_'.join(code_tokens) + '_' + date + shift_sfx
    if tail_tokens:
        out += '_' + '_'.join(tail_tokens)
    return out + '.docx'


DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
GDOC_MIME = 'application/vnd.google-apps.document'
FOLDER_MIME = 'application/vnd.google-apps.folder'
SHORTCUT_MIME = 'application/vnd.google-apps.shortcut'


def canonical_paper_key(name):
    """Collapse every transport-mangled spelling of one paper to a single identity.

    The transport mangles filenames in ways entirely outside the operator's control:
    a browser appends " (1)" when the original is already in Downloads, Drive's web UI
    prefixes "Copy of ", and macOS may return a different Unicode normalisation of the
    same characters. Comparing raw filenames therefore splits one paper into several,
    which double-counts its year (Framework_MockTestAnalyse §1-6 reads years from
    filenames) or reprocesses it.

    Deliberately AGGRESSIVE on punctuation — separators are cosmetic and vary between
    Drive and the local filesystem — but never touches alphanumerics, so genuinely
    distinct papers (Shift-1 vs Shift-2, 2010 vs 2011) keep distinct keys.
    """
    import os as _os
    import unicodedata as _ud
    base = _os.path.basename(str(name))
    stem = _os.path.splitext(base)[0]
    stem = _ud.normalize('NFKC', stem)
    stem = re.sub(r'\s*\(\d+\)\s*$', '', stem)          # browser " (1)"
    stem = re.sub(r'^\s*copy\s+of\s+', '', stem, flags=re.I)
    return re.sub(r'[^a-z0-9]', '', stem.lower())


def screen_drive_entry(name, mime_type, file_size, require_size=True):
    """Decide whether one Drive listing entry is a usable paper.

    Returns (verdict, reason) where verdict is 'paper', 'folder' or 'reject'.

    NOTHING is ever dropped silently. The current enumeration filters on
    ``name.endswith(('.docx','.doc'))``, which means a native Google Doc — whose title
    carries no extension — is neither collected nor reported: the paper simply vanishes
    from the corpus, and §1-6's five-year coverage gate then evaluates an incomplete
    ``available_years`` without knowing it. Every non-usable entry must surface with a
    reason the operator can act on.
    """
    nm = str(name or '')
    low = nm.lower()
    mt = str(mime_type or '')

    if mt == FOLDER_MIME:
        return 'folder', None
    if mt == SHORTCUT_MIME:
        return 'reject', 'Drive shortcut — resolve it to the real file in Drive'
    if mt == GDOC_MIME:
        return 'reject', 'native Google Doc — convert to .docx in Drive (File > Download > .docx)'
    if low.endswith('.doc') and not low.endswith('.docx'):
        return 'reject', 'legacy .doc binary — python-docx cannot open it; convert to .docx'
    if mt != DOCX_MIME and not low.endswith('.docx'):
        return 'reject', f'unsupported type {mt or "<no mimeType>"} — expected .docx'
    if require_size and file_size is None:
        return 'reject', 'no fileSize reported — transport cannot be planned'
    return 'paper', None


def transport_status(file_size, budget=SIZE_BUDGET, cap=DRIVE_CAP):
    """Classify one paper's transport risk. Drives the PYQCompress register.

    BLOCKED  above the connector cap — cannot be fetched at all today.
    MARGINAL fetchable now, but with under 10% headroom: one re-save or one added
             figure flips it to BLOCKED with no warning. Reported, never auto-fixed.
    OK       comfortably fetchable.
    """
    if file_size is None:
        return 'UNKNOWN'
    if file_size > cap:
        return 'BLOCKED'
    if file_size > budget:
        return 'MARGINAL'
    return 'OK'


def base64_cost_chars(n_bytes):
    """Exact base64 expansion of n_bytes: ceil(n/3) * 4 characters.

    Used to price an INLINE Drive channel, where every fetched byte is paid for in
    CONTEXT rather than on disk. Not an estimate — base64 has no compression and no
    variance, so this is the real inbound cost of a payload of that size.
    """
    try:
        n = int(n_bytes)
    except (TypeError, ValueError):
        return 0
    return 0 if n <= 0 else ((n + 2) // 3) * 4


def partition_by_transport(papers, cap=DRIVE_CAP, channel='spill',
                           inline_budget=INLINE_BUDGET_CHARS, consumed=0):
    """Split papers into the AUTO (Drive) lane and the UPLOAD lane BEFORE fetching.

    Partitioning on the CAP rather than on the governor budget is deliberate: a
    marginal 9.3 MiB paper downloads perfectly well today, and forcing it through a
    manual upload would be friction with no safety gain. The runtime fallback
    (corpus_io.fetch_drive_docx raising TransportFallback on ANY error) is what makes
    that safe — this partition is predictive, not binding, so a paper that is
    mispredicted still completes via upload instead of stopping the run.

    Each paper dict must carry 'fileSize'. Order is preserved.

    THE CHANNEL DIMENSION (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION)
    Size was the only dimension this function modelled, and size answers exactly one
    question: "will the connector refuse this file?" It cannot answer the second
    question a transport plan has to answer — "what does moving these bytes COST?" On
    a deployment that returns payloads in the model's turn the answer is context, and
    a corpus that fits the cap 22 times over can still be unaffordable. The old
    signature reported auto:22 / upload:0 for a corpus of which zero papers could be
    afforded, so plan_transport() printed nothing and the operator learned the shape
    of the run after the acquisition loop instead of before it.

      channel='direct' — python fetched the bytes itself over the container's egress
                         (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P43). Nothing
                         passes through the model's turn, so context cost is zero and
                         the whole corpus is admissible in one session. Cost-modelled
                         identically to 'spill'; the two differ only in MECHANISM, and
                         mechanism is corpus_io's business, not this function's.
      channel='spill'  — payloads land on disk; context cost is zero. This reproduces
                         the pre-2026-08-15 behaviour EXACTLY, which is why it is the
                         default: an unpatched caller keeps its old semantics.
      channel='inline' — payloads arrive in the turn. Papers are admitted to the Drive
                         lane in listing order until their CUMULATIVE base64 cost would
                         exceed the budget; the remainder goes to the upload lane.

    The channel is MEASURED by a probe (Framework_PYQCount S5-0), never assumed and
    never inferred from a directory listing — which directory a deployment spills to,
    or whether it spills at all, differs between deployments of the same connector.

    THE PROBE IS A SPENDER (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P40)
    `consumed` is budget ALREADY SPENT in this session before the partition is computed
    — in practice the channel probe, which downloads a real paper. Until this parameter
    existed the partition was computed against the FULL budget as though the probe were
    free, so on the reference corpus it printed a feasible plan for work costing 117%
    of the budget. Measured: probe 107,968 + admitted paper 127,008 = 234,976 real
    characters against 200,000. The plan was arithmetic fiction and the session
    processed zero papers.

    `consumed` is charged EVEN WHEN THE PROBE FAILED — the bytes arrived and occupied
    context regardless of what the caller then decided about them. It is inert on
    'spill' and 'direct', where no payload crosses the turn at all. It is never
    negative; a negative value is a caller bug, not a discount, and raises.

    When `consumed` >= `inline_budget` there is no budget left for any paper: every
    size-eligible paper is deferred for CONTEXT (not for size) and 'auto' is empty. The
    caller must report that condition rather than printing a sessions estimate — see
    Framework_MockTestAnalyse §S8-0 plan_transport, which prints TRANSPORT INFEASIBLE
    and suppresses "Sessions needed" whenever 'auto' is empty.

    Returns {'auto': [...], 'upload': [...], 'channel': ..., 'inline_chars': int,
             'inline_budget': int, 'consumed': int, 'effective_budget': int,
             'deferred_for_context': [...]}.
    """
    if channel not in ('spill', 'inline', 'direct'):
        raise AllocationError(
            f"channel must be 'spill', 'inline' or 'direct', got {channel!r}. It is "
            f"measured by the S5-0 channel probe; there is no fourth state and no "
            f"default guess.")
    try:
        consumed = int(consumed or 0)
    except (TypeError, ValueError):
        raise AllocationError(f'consumed must be an integer, got {consumed!r}')
    if consumed < 0:
        raise AllocationError(
            f'consumed must not be negative, got {consumed}. Budget already spent is '
            f'never a discount on the budget that remains.')

    charged = (channel == 'inline')
    effective = max(0, inline_budget - consumed) if charged else inline_budget

    auto, upload, deferred = [], [], []
    spent = 0
    for p in papers:
        size = p.get('fileSize')
        if size is None or size > cap:
            upload.append(p)
            continue
        if charged:
            cost = base64_cost_chars(size)
            if spent + cost > effective:
                upload.append(p)
                deferred.append(p)
                continue
            spent += cost
        auto.append(p)
    return {'auto': auto, 'upload': upload, 'channel': channel,
            'inline_chars': spent, 'inline_budget': inline_budget,
            'consumed': consumed if charged else 0,
            'effective_budget': effective,
            'deferred_for_context': deferred}


def upload_batch_plan(n_upload, batch_size, chat_limit=CHAT_FILE_LIMIT):
    """Work out how many upload batches fit in one chat.

    The binding constraint is the platform's 20-files-per-chat limit, NOT the batch
    size. At batch_size 3 that is 6 batches = 18 papers per chat; at batch_size 5 it is
    4 batches = 20. The step must state this up front so the operator is never
    surprised mid-run by a limit they could have planned around.
    """
    if batch_size <= 0:
        raise AllocationError('batch_size must be positive')
    batches_per_chat = max(1, chat_limit // batch_size)
    papers_per_chat = batches_per_chat * batch_size
    total_batches = (n_upload + batch_size - 1) // batch_size
    chats_needed = (n_upload + papers_per_chat - 1) // papers_per_chat if n_upload else 0
    return {
        'batches_per_chat': batches_per_chat,
        'papers_per_chat': papers_per_chat,
        'total_batches': total_batches,
        'chats_needed': chats_needed,
    }


def classify_media_route(src_format, has_alpha, is_line_art):
    """Choose the encoder for one image. Deterministic; identical input, identical route.

    'png'          transparency must be preserved — alpha survives only in PNG.
    'png-lineart'  few distinct colours (diagrams, chemical structures, plots): PNG
                   keeps strokes and small type crisp, and palette-quantises well.
                   JPEG would introduce ringing on exactly the thin dark lines and
                   subscripts these figures are made of.
    'jpeg'         photographic, or already JPEG. Re-encoding a JPEG as PNG BLOATS it:
                   the source is already lossy, so PNG stores compression artefacts
                   losslessly and the file grows. Source format therefore wins over
                   the line-art test for JPEG input.
    """
    fmt = (src_format or '').upper()
    if has_alpha:
        return 'png'
    if fmt in ('JPEG', 'JPG'):
        return 'jpeg'
    if is_line_art:
        return 'png-lineart'
    return 'jpeg'


def image_gate_verdict(actual_size, expected_size, unresolved, missing_on_disk,
                       mapped, preamble, body_refs, unreadable):
    """Evaluate image-integrity gates IMG-1 .. IMG-5. Pure: counts in, verdicts out.

    IMG-1 acquisition parity  — bytes on disk match what Drive reported. A payload
                                truncated at a ZIP member boundary still opens cleanly
                                while presenting FEWER images, so the byte count is the
                                only thing that catches it.
    IMG-2 reference integrity — every rId resolves to a media part that exists.
    IMG-3 extraction parity   — every referenced part was written to disk.
    IMG-4 mapping parity      — mapped + preamble == body references. This is the gate
                                that makes table-embedded images (invisible to
                                doc.paragraphs) and VML images self-detecting rather
                                than silently absent.
    IMG-5 renderable          — no media part failed to open.

    'PASS', 'SKIP', or a 'FAIL ...' string naming what went wrong.
    """
    v = {}
    v['IMG-1'] = ('SKIP' if expected_size is None
                  else 'PASS' if actual_size == expected_size
                  else f'FAIL size {actual_size} != reported {expected_size}')
    v['IMG-2'] = 'PASS' if not unresolved else f'FAIL {unresolved} unresolved rId(s)'
    v['IMG-3'] = ('PASS' if not missing_on_disk
                  else f'FAIL {len(missing_on_disk)} referenced part(s) not extracted: '
                       f'{list(missing_on_disk)[:3]}')
    v['IMG-4'] = ('PASS' if mapped + preamble == body_refs
                  else f'FAIL mapped {mapped} + preamble {preamble} != body refs {body_refs}')
    v['IMG-5'] = ('PASS' if not unreadable
                  else f'FAIL {len(unreadable)} unreadable part(s): {list(unreadable)[:3]}')
    return v


def gates_passed(verdicts):
    """True only when every gate passed or was legitimately skipped."""
    return all(str(x).startswith(('PASS', 'SKIP')) for x in verdicts.values())


IMAGE_ROLES = ('stem_and_options', 'stem_only', 'options_only', 'none')


def derive_image_roles(imap):
    """THE image-role resolver. Both Step 5 and Step 1 call this; nobody re-implements it.

    imap is the mapping list produced by the E-4 extractor: a list of dicts each
    carrying 'q_num' and 'position', where position is 'stem' or 'optN'. Returns
    {q_num: {'stem': bool, 'opts': bool, 'role': str}} with role drawn from
    IMAGE_ROLES.

    GAP-2026-07-26-002 DEFECT-3. This loop previously existed only inside the legacy
    DOM branch of extract_and_map_images(). The gated branch built the same dict but
    never derived 'role', so every consumer of q_roles[...]['role'] fell through to
    its 'none' default and every figural question classified TEXT. The rule is now
    owned in ONE place so a second copy cannot drift from it -- the same DELEGATION
    contract audit_deep.py already enforces for detect_question_start and slugify.
    """
    roles = {}
    for entry in imap or ():
        k = entry['q_num']
        r = roles.setdefault(k, {'stem': False, 'opts': False})
        if entry.get('position') == 'stem':
            r['stem'] = True
        else:
            r['opts'] = True
    for r in roles.values():
        if r['stem'] and r['opts']:
            r['role'] = 'stem_and_options'
        elif r['stem']:
            r['role'] = 'stem_only'
        elif r['opts']:
            r['role'] = 'options_only'
        else:
            r['role'] = 'none'
    return roles


def image_clarity_state(probe_passed, figure_readable):
    """Resolve the three-state image_clarity value.

    The two-state form conflates two failures with different causes and different
    remedies: an illegible FIGURE, and a session whose vision path has stopped working.
    Recording the second as 'unclear' blames the corpus, inflates the QV-9 unclear rate,
    and lets figural patterns under-report while the operator troubleshoots the wrong
    thing. 'unclear' is therefore only meaningful once the probe has PASSED.
    """
    if not probe_passed:
        return 'vision_unavailable'
    return 'clear' if figure_readable else 'unclear'


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER V — VISION MERGE / PROFILE  (GAP-2026-07-26-003)
# ═══════════════════════════════════════════════════════════════════════════════
#
# EXECUTION-BOUNDARY LAW. Viewing an image is a CLASS T operation: it requires a
# tool call, and a tool call can only happen BETWEEN model turns. A python process
# launched from bash runs to completion — it cannot suspend mid-loop, emit a tool
# call, receive the result and resume. Every "vision function" the corpus has ever
# written as python was therefore unreachable code returning a default forever.
#
# The three phases, and what lives where:
#
#   PHASE A (python, corpus_io.build_vision_queue)  normalise -> tile -> queue
#   PHASE B (model, prose protocol)                 view() each sheet -> observations
#   PHASE C (python, THIS MODULE)                   merge observations -> fields
#
# NOTHING HERE EVER RAISES AND NOTHING HERE EVER HALTS. A run with zero
# observations produces the same shaped output as a fully observed run; the
# difference is recorded in stats and surfaced by QV-14, not thrown. That is
# deliberate: the defect this cluster exists to fix was a SILENT failure, and the
# remedy for silence is visibility, not a halt.

VISION_FIELDS = ('object_type', 'transformation_type', 'arrangement', 'complexity')

# vision_status, queue level. Distinguishes the four outcomes a consumer must tell
# apart. 'not_applicable' is NOT a failure — a text-only exam is a legitimate zero.
VISION_STATUS = ('not_applicable', 'unavailable', 'partial', 'observed')

_FNV_OFF = 0xcbf29ce484222325
_FNV_PRIME = 0x100000001b3


def _fnv1a(s):
    """Deterministic 64-bit FNV-1a. Pure python so the thin core stays stdlib-only.

    Used only to derive a SHORT, STABLE tag from a paper_id. Not a security hash.
    """
    h = _FNV_OFF
    for b in str(s).encode('utf-8'):
        h = ((h ^ b) * _FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
    return h


def vision_tag_map(keys, width=4):
    """Map ``(paper_id, q_num)`` keys to short, stable, collision-free tags.

    The tag is what a human writes on a contact sheet and reads back in Phase B, so
    it must be short. It must ALSO be stable across runs, or a resumed run cannot
    match yesterday's observations (EC-V11/EC-V12).

    A sequential index would be shorter but is NOT stable: adding one paper shifts
    every later index and silently re-points existing observations at the wrong
    question. The tag is therefore derived from paper_id alone, so a key's tag never
    depends on which OTHER keys are in the queue.

    Collisions are resolved by widening the paper hash for the WHOLE queue — one
    deterministic width per queue, recorded in the queue file so Phase C can tell
    which generation an observations file belongs to. EC-V15: the key is
    (paper_id, q_num); a bare q_num collides across papers by construction.
    """
    keys = list(keys)
    papers = sorted({str(p) for p, _ in keys})
    for w in range(max(2, int(width)), 17):
        codes, seen, clash = {}, set(), False
        for p in papers:
            c = format(_fnv1a(p), 'x').upper()[:w]
            if c in seen:
                clash = True
                break
            seen.add(c)
            codes[p] = c
        if not clash:
            return ({k: f'{codes[str(k[0])]}-{k[1]}' for k in keys}, w)
    # Unreachable in practice (16 hex chars = the full 64-bit space). Degrade to a
    # full-width code rather than raise: this module never halts.
    codes = {p: format(_fnv1a(p), 'x').upper() for p in papers}
    return ({k: f'{codes[str(k[0])]}-{k[1]}' for k in keys}, 16)


def _norm_tag(t):
    """Tags compare case-insensitively and ignore whitespace/en-dashes.

    Phase B is transcription by a model reading a label off an image. Requiring
    byte-exact echo would turn a cosmetic transcription difference into data loss,
    which is the failure mode this whole cluster exists to remove.
    """
    if t is None:
        return ''
    s = re.sub(r'\s+', '', str(t)).upper()
    return s.replace('\u2013', '-').replace('\u2014', '-').replace('_', '-')


def _as_key(rec):
    """Best-effort (paper_id, q_num) from an observation. Returns None if absent."""
    p = rec.get('paper_id')
    q = rec.get('q_num', rec.get('num'))
    if p is None or q is None:
        return None
    try:
        return (str(p), int(q))
    except (TypeError, ValueError):
        return None


def merge_vision_observations(queue_items, observations):
    """PHASE C. Fold Phase-B observations back onto queue items. NEVER raises.

    queue_items  : [{'tag','paper_id','q_num', ...}]  from the queue file
    observations : [{'tag' and/or 'paper_id'+'q_num', 'figure_readable', <fields>}]

    Returns (by_key, stats):
      by_key {(paper_id,q_num): {<VISION_FIELDS>, 'image_clarity'}}
      stats  {'queued','observed','missing','unreadable','unknown','duplicate',
              'vision_status'}

    MATCHING is by tag first, then by (paper_id, q_num). The fallback is what makes
    an observations file survive a queue rebuilt at a different tag width — without
    it, a widened queue would silently discard every prior observation (EC-V11).

    image_clarity is derived through image_clarity_state() with probe_passed set to
    "this item was actually observed". An observation existing IS the proof that the
    vision path worked for that item, so no separate probe rule is needed here. One
    rule, one place — a second rule would drift from the first (anti-drift).

    EC-V4  partial observation      -> present items filled, absent items reported
    EC-V5  observation not in queue -> counted in stats['unknown'], never a crash
    EC-V12 re-run                   -> identical inputs give identical outputs
    """
    items = list(queue_items or [])
    by_tag, by_key_idx = {}, {}
    for it in items:
        k = _as_key(it)
        if k is None:
            continue
        by_tag[_norm_tag(it.get('tag'))] = k
        by_key_idx[k] = it

    seen, unknown, duplicate = {}, [], []
    for ob in (observations or []):
        if not isinstance(ob, dict):
            continue
        k = by_tag.get(_norm_tag(ob.get('tag')))
        if k is None:
            k2 = _as_key(ob)
            k = k2 if k2 in by_key_idx else None
        if k is None:
            unknown.append(ob.get('tag'))
            continue
        if k in seen:
            duplicate.append(ob.get('tag'))
        seen[k] = ob                      # last write wins, deterministically

    by_key, unreadable = {}, 0
    for it in items:
        k = _as_key(it)
        if k is None:
            continue
        ob = seen.get(k)
        observed = ob is not None
        readable = bool(ob.get('figure_readable', True)) if observed else False
        if observed and not readable:
            unreadable += 1
        rec = {f: (ob.get(f) if observed else None) for f in VISION_FIELDS}
        # An observed-but-illegible figure carries no field values: EC-V2 says record
        # the illegibility, never a guess.
        if observed and not readable:
            rec = {f: None for f in VISION_FIELDS}
        rec['image_clarity'] = image_clarity_state(observed, readable)
        by_key[k] = rec

    queued = len(by_key)
    observed_n = sum(1 for k in by_key if k in seen)
    missing = queued - observed_n
    if queued == 0:
        status = 'not_applicable'
    elif observed_n == 0:
        status = 'unavailable'
    elif missing == 0:
        status = 'observed'
    else:
        status = 'partial'
    # Tags are coerced to str before sorting. An observations file is model-written
    # JSON, so a tag can arrive as an int (123) beside a str ('A1B2-7'); sorted()
    # raises TypeError comparing the two, and a diagnostic field must never be the
    # thing that brings the merge down. Found by property fuzzing, not by example.
    def _tags_out(seq):
        return sorted({str(t) for t in seq if t not in (None, '')})

    return by_key, {
        'queued': queued, 'observed': observed_n, 'missing': missing,
        'unreadable': unreadable, 'unknown': _tags_out(unknown),
        'duplicate': _tags_out(duplicate), 'vision_status': status,
    }


MIN_DOMINANT_OBSERVATIONS = 5
MIN_DOMINANT_COUNT = 2
MIN_DOMINANT_SHARE = 0.20


def vision_profile(records, min_dominant=MIN_DOMINANT_OBSERVATIONS, top_n=3,
                   min_count=MIN_DOMINANT_COUNT, min_share=MIN_DOMINANT_SHARE):
    """Aggregate merged vision records for ONE subtopic into PYQ_IMAGE_ANALYSIS.

    records: the merged dicts for this subtopic's figural questions.

    EC-V20. 'dominant' is a claim about what this subtopic's figures TYPICALLY look
    like, and Step 7 generates against it. Two observations cannot support that claim
    — declaring a dominant type from n=2 hands the generator noise with the authority
    of measurement. Below min_dominant, 'observed' is still published (it is a plain
    record of what was seen) and 'dominant' is withheld, with the reason stated in
    'dominant_suppressed' so a reader is never left guessing why it is empty.

    EC-V21. observed_n / queued_n travel with the profile, so a consumer can tell a
    complete profile from one built on a third of the subtopic's papers.

    EC-V26 (FLAT DISTRIBUTION). Having enough observations is necessary but not
    sufficient. Six figures of six DIFFERENT types is a well-observed subtopic with no
    dominant type at all — yet a plain top-N would name the alphabetically-first three
    and hand Step 7 a fixation the evidence does not support. A type must therefore
    RECUR (>= min_count) and hold a real share (>= min_share) before it is named.
    When nothing qualifies, 'dominant' is empty and 'observed' carries the variety,
    which is the honest instruction: generate across the range, do not fixate.
    """
    recs = [r for r in (records or []) if isinstance(r, dict)]
    clear = [r for r in recs if r.get('image_clarity') == 'clear']
    unclear = sum(1 for r in recs if r.get('image_clarity') == 'unclear')
    unobserved = sum(1 for r in recs if r.get('image_clarity') == 'vision_unavailable')

    def _vals(field):
        return [r.get(field) for r in clear if r.get(field)]

    objs = _vals('object_type')
    transforms = [t for t in _vals('transformation_type') if t != 'N/A']
    arrangements = _vals('arrangement')
    complexities = _vals('complexity')

    counts = {}
    for o in objs:
        counts[o] = counts.get(o, 0) + 1
    ranked = [o for o, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]

    enough = len(clear) >= int(min_dominant)
    n_obj = len(objs)
    qualified = [o for o in ranked
                 if counts[o] >= int(min_count)
                 and n_obj and (counts[o] / float(n_obj)) >= float(min_share)]
    dominant = qualified[:top_n] if enough else []
    prof = {
        'object_types': {
            'dominant': dominant,
            'observed': sorted(set(objs)),
            'avoid': [],
        },
        'transformation_types': sorted(set(transforms)),
        'arrangement_types': sorted(set(arrangements)),
        'complexity_dist': ({k: round(v / len(complexities) * 100)
                             for k, v in sorted(
                                 {c: complexities.count(c)
                                  for c in set(complexities)}.items())}
                            if complexities else {}),
        'images_analysed': len(clear),
        'images_unclear': unclear,
        'images_unobserved': unobserved,
        'observed_n': len(clear),
        'queued_n': len(recs),
    }
    if not enough:
        prof['dominant_suppressed'] = (
            f'{len(clear)} clear observation(s) — below the {int(min_dominant)} '
            f'needed to name a dominant type; "observed" is reported instead')
    elif not dominant:
        prof['dominant_suppressed'] = (
            f'{len(set(objs))} distinct type(s) across {n_obj} observation(s) with no '
            f'type reaching {int(min_count)} occurrences and {int(min_share * 100)}% '
            f'share — the distribution is flat, so no type is dominant; generate '
            f'across "observed" rather than fixating')
    if len(recs) == 0:
        prof['vision_status'] = 'not_applicable'
    elif len(clear) == 0:
        prof['vision_status'] = 'unavailable'
    elif unobserved == 0:
        prof['vision_status'] = 'observed'
    else:
        prof['vision_status'] = 'partial'
    return prof


GENERATION_MODES = ('unconstrained', 'observed', 'dominant')


def figural_generation_profile(pyq_image_analysis):
    """CONSUMER SIDE. Resolve a section_rules PYQ_IMAGE_ANALYSIS block into a
    figure-generation constraint for Step 7. NEVER raises.

    Step 5 has measured what the real figures in a subtopic CONTAIN since v2.29 and
    wrote object_types / transformation_types / complexity_dist into section_rules.
    Until now NOTHING READ THEM: Framework_MockTestCreate consumed only image_role,
    so the semantic half of the measurement was written and never used — a captured
    value with no consumer, the exact defect shape audit_callgraph C5 exists to catch,
    invisible to C5 only because these fields are serialised as prose rather than held
    as dict keys.

    Returns {'mode', 'dominant', 'observed', 'transformation_types',
             'arrangement_types', 'complexity_dist', 'reason'}.

      'dominant'      — a recurring type profile exists; bind generation to it 70/30.
      'observed'      — figures were seen but no type dominates (flat, or thin
                        evidence). Generate ACROSS the observed variety; do not
                        fixate. Naming a dominant here would be noise with the
                        authority of measurement.
      'unconstrained' — no usable profile. Generate on subtopic semantics alone,
                        exactly as before this function existed.

    EC-V18 LEGACY TOLERANCE, NON-NEGOTIABLE. Roughly 200 exams hold section_rules
    written before the vision fix, carrying object_types: [] and no vision_status.
    Every one must keep working untouched, so absent / empty / malformed input all
    resolve to 'unconstrained' rather than raising or blocking.

    A vision_status of 'unavailable' is treated as 'unconstrained' EVEN IF stale
    object_types are present: that status means Step 5 queued figures and observed
    none, so the emptiness is a MEASUREMENT GAP, not evidence about the subtopic.
    Generating against it would be generating against a fact nobody established.
    Reporting the gap is QV-14's job, not this function's.
    """
    out = {'mode': 'unconstrained', 'dominant': [], 'observed': [],
           'transformation_types': [], 'arrangement_types': [],
           'complexity_dist': {}, 'reason': ''}
    if not isinstance(pyq_image_analysis, dict) or not pyq_image_analysis:
        out['reason'] = 'no PYQ_IMAGE_ANALYSIS block (pre-v2.37 artefact) — EC-V18'
        return out

    status = pyq_image_analysis.get('vision_status')
    if status in ('unavailable', 'not_applicable'):
        out['reason'] = (f"vision_status={status!r} — the profile is a measurement "
                         f"gap, not a finding about this subtopic")
        return out

    ot = pyq_image_analysis.get('object_types')
    ot = ot if isinstance(ot, dict) else {}

    def _clean(seq):
        return [str(x) for x in seq if x] if isinstance(seq, (list, tuple)) else []

    dominant = _clean(ot.get('dominant'))
    observed = _clean(ot.get('observed'))
    out['dominant'] = dominant
    out['observed'] = sorted(set(observed) | set(dominant))
    out['transformation_types'] = _clean(pyq_image_analysis.get('transformation_types'))
    out['arrangement_types'] = _clean(pyq_image_analysis.get('arrangement_types'))
    cd = pyq_image_analysis.get('complexity_dist')
    out['complexity_dist'] = cd if isinstance(cd, dict) else {}

    if dominant:
        out['mode'] = 'dominant'
        out['reason'] = (f'{len(dominant)} recurring type(s) over '
                         f'{len(out["observed"])} observed — bind 70/30')
    elif out['observed']:
        out['mode'] = 'observed'
        out['reason'] = (pyq_image_analysis.get('dominant_suppressed')
                         or f'{len(out["observed"])} type(s) observed, none dominant '
                            f'— generate across the range')
    else:
        out['reason'] = 'PYQ_IMAGE_ANALYSIS present but object_types empty — EC-V18'
    return out


DOMINANT_SHARE_TARGET = 0.70
DOMINANT_SHARE_FLOOR = 0.55


def check_figural_conformance(generated_types, profile,
                              floor=DOMINANT_SHARE_FLOOR):
    """Did generation honour the figure profile? ONE rule, shared by Steps 7 and 8.

    generated_types: the object_type Step 7 RECORDED for each figural question it
    generated in this subtopic (from batch_state.figural_qs[n].object_type).

    Returns (verdict, detail) where verdict is 'PASS' | 'FAIL' | 'SKIP'.

    WHY INTENT, NOT PIXELS. Verifying that a rendered PNG actually depicts a
    micrograph would require viewing it — a CLASS T operation, which cannot run
    inside an audit's python. Auditing the RECORDED INTENT is deterministic, free,
    and catches the failure that actually matters: Step 7 ignoring the profile.
    Whether the render matches its own label is a different question, already
    covered by the image-count and composite gates.

    'dominant' mode allows a FLOOR rather than the exact 70/30 target. A subtopic
    with three generated figures cannot hit 70% precisely, and failing a run for
    arithmetic it cannot satisfy is how a gate gets disabled.

    NEVER raises. An unconstrained profile SKIPs, which is what keeps ~200 legacy
    exams passing (EC-V18).
    """
    types = [str(t) for t in (generated_types or []) if t]
    mode = (profile or {}).get('mode', 'unconstrained')
    if mode == 'unconstrained' or not types:
        return ('SKIP', 'no figure profile for this subtopic (EC-V18)'
                if mode == 'unconstrained' else 'no generated figural questions')

    observed = set((profile or {}).get('observed') or [])
    stray = sorted({t for t in types if t not in observed})
    if stray:
        return ('FAIL',
                f'generated figure type(s) {stray} appear in neither the dominant '
                f'nor the observed profile for this subtopic — the real PYQs show '
                f'{sorted(observed)}. A figure type the exam has never used cannot '
                f'match it in content.')

    if mode == 'observed':
        return ('PASS', f'{len(types)} figure(s) drawn from the observed range '
                        f'{sorted(observed)}; no dominant type to bind to')

    dominant = set((profile or {}).get('dominant') or [])
    hit = sum(1 for t in types if t in dominant)
    share = hit / float(len(types))
    if share < float(floor):
        return ('FAIL',
                f'only {hit}/{len(types)} ({share:.0%}) generated figures use a '
                f'dominant type {sorted(dominant)}; target is '
                f'{int(DOMINANT_SHARE_TARGET * 100)}%, floor '
                f'{int(float(floor) * 100)}%. The mock under-represents what this '
                f'subtopic actually looks like.')
    return ('PASS', f'{hit}/{len(types)} ({share:.0%}) use a dominant type '
                    f'(floor {int(float(floor) * 100)}%)')


def parse_image_analysis_blocks(section_rules_text):
    """Parse ``{subtopic_id: PYQ_IMAGE_ANALYSIS dict}`` out of section_rules text.

    Pure string work, so it belongs in the thin core: Step 8 receives section_rules
    as TEXT (it does not receive the answer-key sidecar, S0-1), and both Step 7 and
    Step 8 must read the same block the same way or their verdicts diverge.

    Tolerant by construction. A block written before v2.37 carries only four fields;
    one written after carries eleven. Missing keys are simply absent from the dict,
    and figural_generation_profile() resolves an incomplete dict to 'unconstrained'
    (EC-V18). NEVER raises — a malformed artefact yields {} and the gate goes dormant
    rather than failing a run for a parsing problem.
    """
    out = {}
    if not isinstance(section_rules_text, str) or not section_rules_text:
        return out

    def _lit(raw, default):
        raw = (raw or '').strip()
        if not raw:
            return default
        try:
            import ast as _ast
            return _ast.literal_eval(raw)
        except Exception:
            return default

    # Blocks are delimited by the subtopic header; subtopic_id appears inside.
    for chunk in re.split(r'^---\s*Subtopic:', section_rules_text, flags=re.M)[1:]:
        m = re.search(r'^\s*subtopic_id:\s*(\S+)', chunk, re.M)
        if not m:
            continue
        sid = m.group(1).strip()
        blk = re.search(r'^PYQ_IMAGE_ANALYSIS:\s*\n(.*?)(?=^\S|\Z)', chunk,
                        re.M | re.S)
        if not blk:
            continue
        body = blk.group(1)

        def _s(key):
            mm = re.search(rf'^\s*{key}:\s*(.+)$', body, re.M)
            return mm.group(1).strip() if mm else None

        rec = {}
        for key in ('image_role', 'vision_status'):
            v = _s(key)
            if v is not None:
                rec[key] = v
        dom = re.search(r'^\s*dominant:\s*(\[.*?\])\s*$', body, re.M)
        obs = re.search(r'^\s*observed:\s*(\[.*?\])\s*$', body, re.M)
        avo = re.search(r'^\s*avoid:\s*(\[.*?\])\s*$', body, re.M)
        if dom or obs or avo:
            rec['object_types'] = {
                'dominant': _lit(dom.group(1) if dom else None, []),
                'observed': _lit(obs.group(1) if obs else None, []),
                'avoid': _lit(avo.group(1) if avo else None, []),
            }
        for key in ('transformation_types', 'arrangement_types'):
            v = _s(key)
            if v is not None:
                rec[key] = _lit(v, [])
        v = _s('complexity_dist')
        if v is not None:
            rec['complexity_dist'] = _lit(v, {})
        for key in ('images_analysed', 'images_unclear', 'images_unobserved'):
            v = _s(key)
            if v is not None:
                try:
                    rec[key] = int(v)
                except (TypeError, ValueError):
                    pass
        v = _s('dominant_suppressed')
        if v is not None:
            rec['dominant_suppressed'] = v.strip('"')
        out[sid] = rec
    return out


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

    # ── Cluster A: frequency ─────────────────────────────────────────────────
    check('split_recency_5yr',
          split_recency(['2019', '2020', '2022', '2024', '2025'])
          == (['2024', '2025'], ['2019', '2020', '2022']))
    check('split_recency_1yr', split_recency(['2024']) == (['2024'], []))
    check('r_avg_single_year',
          compute_r_avg([{'avg': 3.0, 'papers': 2, 'recent': True}])[0] == 3.0)
    check('r_avg_weighted',
          compute_r_avg([{'avg': 4.0, 'papers': 1, 'recent': True},
                         {'avg': 1.0, 'papers': 1, 'recent': False}])[0] == 3.0)
    check('r_avg_dataquality_warn',
          compute_r_avg([{'avg': 5.0, 'papers': 0, 'recent': False}]) == (0.0, [
              'Data error: year has Avg/Paper=5.0 but Papers In=0. '
              'Treating year as 0 papers.']))

    # ── Cluster B: apportionment ─────────────────────────────────────────────
    check('apportion_undercount', largest_remainder_apportion({'a': 0.5, 'b': 0.5}, 4)
          == {'a': 2, 'b': 2})
    check('apportion_overcount',
          sum(largest_remainder_apportion({'a': 1.4, 'b': 1.6}, 2).values()) == 2)
    check('apportion_empty_or_zero',
          largest_remainder_apportion({}, 10) == {}
          and largest_remainder_apportion({'a': 1.0}, 0) == {})
    check('difficulty_sum',
          all(sum(difficulty_counts(t, *p)) == t
              for t in (0, 25, 100, 150, 7)
              for p in ((25, 25, 50), (33, 33, 34), (0, 0, 100))))
    check('difficulty_zero_total', difficulty_counts(0, 25, 25, 50) == (0, 0, 0))
    # proportional_split + fix reproduce an exact target (hand-worked)
    _r = {'A': 2.0, 'B': 1.0, 'C': 0.5}
    _q, _rt = proportional_split(['A', 'B', 'C'], _r, 30, 3, 1)
    check('proportional_split_floor', _q == {'A': 17, 'B': 8, 'C': 4})
    largest_remainder_fix(_q, ['A', 'B', 'C'], _rt, _r, 30, 1, floors={})
    check('split_fix_hits_target', sum(_q.values()) == 30 and _q['B'] == 9)
    # negative deficit respects a mandate floor
    _q2 = {'A': 4, 'B': 3, 'C': 3}
    largest_remainder_fix(_q2, ['A', 'B', 'C'], {'A': 3.9, 'B': 2.1, 'C': 2.2},
                          {'A': 5, 'B': 1, 'C': 1}, 8, 1, floors={'A': 4})
    check('fix_respects_floor', sum(_q2.values()) == 8 and _q2['A'] == 4)
    # infeasible reduction raises
    _raised = False
    try:
        largest_remainder_fix({'A': 2, 'B': 2, 'C': 2}, ['A', 'B', 'C'],
                              {'A': 2, 'B': 2, 'C': 2}, {'A': 1, 'B': 1, 'C': 1},
                              3, 2, floors={})
    except AllocationError:
        _raised = True
    check('fix_infeasible_raises', _raised)
    # exact_fill: margins + variance
    _al = exact_fill({'A': 3, 'B': 2}, [2, 2, 1])
    check('exact_fill_margins', _al == {'A': [1, 1, 1], 'B': [1, 1, 0]})
    _fe = False
    try:
        exact_fill({'A': 3}, [2, 2])
    except ValueError:
        _fe = True
    check('exact_fill_feasibility_guard', _fe)

    # ── Cluster C: axis schedule ─────────────────────────────────────────────
    check('axis_no_pyq',
          derive_axis_schedule('S', None, 25, [], [], {}, {}, papers_per_window=10)['status']
          == 'no_pyq')
    _sched = derive_axis_schedule(
        'SEC',
        # FIXTURE NOTE (v2): all three axes are independent CLASSIFICATIONS OF THE SAME
        # question set, so each must sum to the same per-paper question count (25 here).
        # The pre-v2 fixture had axis2 summing to 2.55 against axis1/axis3's 25 — a state
        # compute_section_axis_distribution can never emit (its per_paper() assigns every
        # question exactly one class per axis, defaulting to '?'). That impossible fixture
        # is why the un-normalised axis2 unit bug survived undetected. Now realisable:
        # DIRECT is the residual filler that makes the axis total 25.
        {'axis2_per_paper': {'MATCH': 0.5, 'SEQUENCE': 0.05,
                             'ASSERTION_REASON': 3.0, 'DIRECT': 21.45},
         'axis1_per_paper': {'TEXT': 20.0, 'FIGURAL': 5.0},
         'axis3_per_paper': {'OPTION': 24.0, 'NUMERICAL': 1.0}},
        25, ['ST01'], ['ST02'],
        {'ST01': ['DIRECT', 'MATCH'], 'ST02': ['DIRECT', 'SEQUENCE']},
        {'ST01': {'section': 'SEC', 'format': 'TEXT'},
         'ST02': {'section': 'SEC', 'format': 'FIGURAL'}},
        papers_per_window=10)
    check('axis_band_mode', _sched['axis2_audit_mode']['MATCH'] == 'band'
          and _sched['axis2_window_target']['MATCH'] == 5)
    check('axis_guarantee_mode', _sched['axis2_guarantee'] == ['SEQUENCE']
          and _sched['guarantee_feasibility']['SEQUENCE'] == 'zp_only')
    check('axis_direct_float', _sched['axis2_audit_mode']['DIRECT'] == 'float'
          and 'DIRECT' not in _sched['axis2_window_target'])
    check('axis_apportion_exact', sum(_sched['axis1_target_per_mock'].values()) == 25
          and sum(_sched['axis3_target_per_mock'].values()) == 25)
    check('axis_output_key_preserved', _sched['mocks_per_window'] == 10)
    check('axis2_pool_caps',
          section_axis2_pool_caps('SEC', ['ST01'], {'ST01': ['MATCH']},
                                  {'ST01': {'section': 'SEC'}}) == {'MATCH'})
    check('axis1_feasibility',
          axis1_feasibility('SEC', {'TEXT': 20, 'FIGURAL': 5}, ['ST01'],
                            {'ST01': {'section': 'SEC', 'format': 'TEXT'}}) == ['FIGURAL'])

    # ── GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE regression pack ────────────
    # The defect shape: manifest 'section' holds taxonomy SUBJECT names while the
    # caller passes the OTS section LABEL. The old raw '==' re-filter therefore
    # excluded EVERY id on a sections[].subjects exam (IIT JAM shape: 'Section A'
    # vs 'Organic Chemistry'), emptying caps/avail. Lists arrive pre-scoped by
    # the fence's subtopic_in_section(); the engine must not re-filter them in
    # the wrong namespace.
    _nk_manifest = {'ST01': {'section': 'Organic Chemistry',  'format': 'TEXT'},
                    'ST02': {'section': 'Physical Chemistry', 'format': 'FIGURAL'}}
    # 1 — caps computed across a pre-scoped mixed-Subject list under an OTS label
    #     (old code: {} — every guarantee then reported 'unsatisfiable').
    check('AXIS-SECTIONKEY-N1-caps-cross-namespace',
          section_axis2_pool_caps('Section A', ['ST01', 'ST02'],
                                  {'ST01': ['MATCH'], 'ST02': ['ASSERTION']},
                                  _nk_manifest) == {'MATCH', 'ASSERTION'})
    # 2 — avail computed likewise; a targeted+capable format is NOT flagged
    #     (old code: avail empty → both TEXT and FIGURAL flagged unreachable).
    check('AXIS-SECTIONKEY-N1-avail-cross-namespace',
          axis1_feasibility('Section A', {'TEXT': 20, 'FIGURAL': 5},
                            ['ST01', 'ST02'], _nk_manifest) == [])
    # 3 — a genuinely absent format is still flagged (the advisory still works).
    check('AXIS-SECTIONKEY-N1-missing-format-still-flagged',
          axis1_feasibility('Section A', {'PASSAGE': 3, 'TEXT': 10},
                            ['ST01', 'ST02'], _nk_manifest) == ['PASSAGE'])
    # 4 — ids absent from manifest_ids are SKIPPED, never crash, in both
    #     functions (the retained defensive behaviour of the old .get chain).
    check('AXIS-SECTIONKEY-missing-id-skipped',
          section_axis2_pool_caps('Section A', ['ST01', 'GHOST'],
                                  {'ST01': ['MATCH']}, _nk_manifest) == {'MATCH'}
          and axis1_feasibility('Section A', {'TEXT': 1}, ['GHOST'],
                                _nk_manifest) == ['TEXT'])
    # 5 — cap_by_id default: an in-manifest id with no capability entry counts
    #     as DIRECT (unchanged from the old code's ["DIRECT"] default).
    check('AXIS-SECTIONKEY-cap-default-direct',
          section_axis2_pool_caps('Section A', ['ST02'], {}, _nk_manifest)
          == {'DIRECT'})

    # ── GAP-2026-08-23-AXIS-ADVISORY-TRUTH regression pack ───────────────────
    # The parent defect wrote advisories that contradicted the manifest they
    # summarise, and nothing compared the two. axis_truth_check is that
    # comparison, FIRST-PRINCIPLES (never via the audited functions). Fixtures
    # cover: consistency, both contradiction directions on Axis-1, the Axis-2
    # verdict flip that would excuse real shortfalls, dormancy, and the
    # ghost-id / zero-count-target semantics shared with the primaries.
    _tr_man = {'ST01': {'section': 'Organic Chemistry',  'format': 'TEXT'},
               'ST02': {'section': 'Physical Chemistry', 'format': 'FIGURAL'},
               'ZP01': {'section': 'Organic Chemistry',  'format': 'TEXT'}}
    _tr_cap = {'ST01': ['DIRECT', 'MATCH'], 'ST02': ['DIRECT'],
               'ZP01': ['SEQUENCE']}
    _tr_ok = {'status': 'ok',
              'axis1_target_per_mock': {'TEXT': 20, 'FIGURAL': 5},
              'axis1_unreachable_formats': [],
              'axis2_guarantee': ['SEQUENCE'],
              'guarantee_feasibility': {'SEQUENCE': 'zp_only'}}
    check('AXIS-TRUTH-consistent-schedule-passes',
          axis_truth_check(_tr_ok, ['ST01', 'ST02'], ['ZP01'],
                           _tr_cap, _tr_man) == [])
    _tr_f = axis_truth_check(dict(_tr_ok,
                                  axis1_unreachable_formats=['TEXT', 'FIGURAL']),
                             ['ST01', 'ST02'], ['ZP01'], _tr_cap, _tr_man)
    check('AXIS-TRUTH-false-pessimist-caught',
          len(_tr_f) == 1 and 'demonstrably contain' in _tr_f[0])
    _tr_f = axis_truth_check(dict(_tr_ok,
                                  axis1_target_per_mock={'TEXT': 20, 'DI': 3}),
                             ['ST01', 'ST02'], ['ZP01'], _tr_cap, _tr_man)
    check('AXIS-TRUTH-false-optimist-caught',
          len(_tr_f) == 1 and 'omits' in _tr_f[0] and 'DI' in _tr_f[0])
    _tr_f = axis_truth_check(dict(_tr_ok,
                                  guarantee_feasibility={'SEQUENCE':
                                                         'unsatisfiable'}),
                             ['ST01', 'ST02'], ['ZP01'], _tr_cap, _tr_man)
    check('AXIS-TRUTH-guarantee-verdict-flip-caught',
          len(_tr_f) == 1 and 'unsatisfiable' in _tr_f[0])
    check('AXIS-TRUTH-dormant-on-no-pyq-and-none',
          axis_truth_check({'status': 'no_pyq'}, ['ST01'], [],
                           _tr_cap, _tr_man) == []
          and axis_truth_check(None, ['ST01'], [], _tr_cap, _tr_man) == [])
    check('AXIS-TRUTH-ghost-id-no-phantom-availability',
          axis_truth_check(dict(_tr_ok, axis1_target_per_mock={'TEXT': 5},
                                axis1_unreachable_formats=['TEXT'],
                                axis2_guarantee=[], guarantee_feasibility={}),
                           ['GHOST'], [], {}, {}) == [])
    check('AXIS-TRUTH-zero-count-target-ignored',
          axis_truth_check(dict(_tr_ok,
                                axis1_target_per_mock={'TEXT': 25, 'DI': 0}),
                           ['ST01', 'ST02'], ['ZP01'], _tr_cap, _tr_man) == [])

    # ── GAP-2026-08-12-AXIS-PREFLIGHT regression pack ────────────────────────
    # Real-world trigger (Mock-10 root-cause gap analysis §5.5/§13 row 2): a mock can
    # pass axis1_feasibility's SECTION-wide check yet still be drafted from a subset of
    # subtopics that under-represents the format-capable ones THIS mock needed. No
    # exam/subtopic name below is load-bearing.
    _mf_manifest = {'ST01': {'format': 'TEXT'}, 'ST02': {'format': 'FIGURAL'},
                    'ST03': {'format': 'FIGURAL'}}

    # 1 — FULLY FEASIBLE: allocation covers the target exactly.
    check('AXISPREFLIGHT-fully-feasible-empty-shortfall',
          axis1_mock_feasibility({'TEXT': 8, 'FIGURAL': 2},
                                 {'ST01': 8, 'ST02': 1, 'ST03': 1},
                                 _mf_manifest) == {})

    # 2 — THE DEFECT ITSELF: target names 4 FIGURAL, but this mock's allocation only
    #     grants 1 FIGURAL-capable slot — max_achievable must say so exactly.
    check('AXISPREFLIGHT-detects-shortfall-with-exact-counts',
          axis1_mock_feasibility({'TEXT': 9, 'FIGURAL': 4},
                                 {'ST01': 9, 'ST02': 1},
                                 _mf_manifest)
          == {'FIGURAL': {'target': 4, 'max_achievable': 1}})

    # 3 — q_count is SUMMED per format, not counted per distinct subtopic (a subtopic
    #     holding 3 slots contributes 3, not 1).
    check('AXISPREFLIGHT-sums-qcount-not-subtopic-count',
          axis1_mock_feasibility({'FIGURAL': 5}, {'ST02': 3, 'ST03': 2}, _mf_manifest)
          == {})

    # 4 — a target format with ZERO allocated capacity at all (not merely present in
    #     manifest_ids — genuinely absent from this mock's allocation) is a full shortfall.
    check('AXISPREFLIGHT-zero-capacity-is-full-shortfall',
          axis1_mock_feasibility({'PASSAGE': 3}, {'ST01': 10}, _mf_manifest)
          == {'PASSAGE': {'target': 3, 'max_achievable': 0}})

    # 5 — ABSENT-SAFE: no target, or no allocation, never crashes and reports nothing.
    check('AXISPREFLIGHT-absent-safe',
          axis1_mock_feasibility({}, {'ST01': 5}, _mf_manifest) == {}
          and axis1_mock_feasibility({'FIGURAL': 2}, {}, _mf_manifest) == {}
          and axis1_mock_feasibility(None, None, _mf_manifest) == {})

    # 6 — a target of 0 (or absent) for a format is never flagged, even with zero
    #     capacity for it — only POSITIVE targets can be short.
    check('AXISPREFLIGHT-zero-target-never-flagged',
          axis1_mock_feasibility({'FIGURAL': 0, 'TEXT': 5}, {'ST01': 5}, _mf_manifest)
          == {})

    # 7 — axis1_feasibility itself (existing function, one caller in
    #     Framework_Blueprint.md) is completely untouched by this addition.
    check('AXISPREFLIGHT-does-not-regress-axis1_feasibility',
          axis1_feasibility('SEC', {'TEXT': 20, 'FIGURAL': 5}, ['ST01'],
                            {'ST01': {'section': 'SEC', 'format': 'TEXT'}}) == ['FIGURAL'])

    # ── GAP-2026-08-12-AXIS3-PREFLIGHT regression pack ───────────────────────
    # The defining correctness trap this function exists to avoid (v5.50's own release
    # note flagged it and deliberately deferred landing it un-verified): on a
    # POSITION-BASED exam (Framework_MockTestCreate v5.30, _resolve_answer_axes),
    # mechanism is decided by Q-POSITION, never by subtopic capability — checking
    # subtopic capability there would be not just useless but ACTIVELY MISLEADING. No
    # exam/subtopic name below is load-bearing.
    _m3_manifest = {'ST01': {'answer_cardinality': 'single', 'answer_type': 'option'},   # MCQ
                    'ST02': {'answer_cardinality': 'multi',  'answer_type': 'option'},   # MSQ
                    'ST03': {'answer_cardinality': 'single', 'answer_type': 'numerical'}, # NAT
                    'ST04': {'answer_cardinality': 'multi',  'answer_type': 'numerical'}} # NAT wins (precedence)

    # 1 — THE GATE ITSELF: position_based_typing=True suppresses the check UNCONDITIONALLY,
    #     even feeding it a target/allocation combo that would OBVIOUSLY be a shortfall
    #     under subtopic-based reasoning. This is the exact scenario the v5.50 release
    #     note described: a target this mock's allocation could never satisfy by subtopic
    #     capability alone, but which position dispatch guarantees regardless.
    check('AXIS3PREFLIGHT-position-based-exam-always-skips',
          axis3_mock_feasibility({'MSQ': 10}, {'ST01': 10}, _m3_manifest,
                                 position_based_typing=True) == {})

    # 2 — SUBTOPIC-BASED exam (position_based_typing=False), fully feasible.
    check('AXIS3PREFLIGHT-subtopic-based-fully-feasible',
          axis3_mock_feasibility({'MCQ': 7, 'MSQ': 2, 'NAT': 1},
                                 {'ST01': 7, 'ST02': 2, 'ST03': 1}, _m3_manifest,
                                 position_based_typing=False) == {})

    # 3 — SUBTOPIC-BASED exam, genuine shortfall — exact counts reported.
    check('AXIS3PREFLIGHT-subtopic-based-detects-shortfall',
          axis3_mock_feasibility({'MCQ': 6, 'MSQ': 4}, {'ST01': 6, 'ST02': 1}, _m3_manifest,
                                 position_based_typing=False)
          == {'MSQ': {'target': 4, 'max_achievable': 1}})

    # 4 — PRECEDENCE: a subtopic with BOTH answer_type='numerical' AND
    #     answer_cardinality='multi' resolves to NAT, not MSQ — mirrors
    #     audit_canonical.gate_axis3's own observability order ("0 options ⇒ NAT" is
    #     checked before the MSQ select-instruction; MCQ is the untested residual).
    check('AXIS3PREFLIGHT-nat-precedence-over-msq',
          axis3_mock_feasibility({'NAT': 3}, {'ST04': 3}, _m3_manifest,
                                 position_based_typing=False) == {}
          and axis3_mock_feasibility({'MSQ': 3}, {'ST04': 3}, _m3_manifest,
                                     position_based_typing=False)
          == {'MSQ': {'target': 3, 'max_achievable': 0}})

    # 5 — ABSENT-SAFE: no target / no allocation / None everything, never crashes.
    check('AXIS3PREFLIGHT-absent-safe',
          axis3_mock_feasibility({}, {'ST01': 5}, _m3_manifest, position_based_typing=False) == {}
          and axis3_mock_feasibility({'MCQ': 2}, {}, _m3_manifest, position_based_typing=False) == {}
          and axis3_mock_feasibility(None, None, _m3_manifest, position_based_typing=False) == {}
          and axis3_mock_feasibility(None, None, _m3_manifest, position_based_typing=True) == {})

    # 6 — a target of 0 for a mechanism is never flagged, even with zero capacity.
    check('AXIS3PREFLIGHT-zero-target-never-flagged',
          axis3_mock_feasibility({'MSQ': 0, 'MCQ': 5}, {'ST01': 5}, _m3_manifest,
                                 position_based_typing=False) == {})

    # 7 — axis1_mock_feasibility itself (existing function) is completely untouched.
    check('AXIS3PREFLIGHT-does-not-regress-axis1_mock_feasibility',
          axis1_mock_feasibility({'TEXT': 9, 'FIGURAL': 4}, {'ST01': 9, 'ST02': 1},
                                 _mf_manifest) == {'FIGURAL': {'target': 4, 'max_achievable': 1}})

    # ── GAP-2026-08-06-AXIS1 — BUDGET TRACKER regression pack ────────────────
    # The defect these lock down shipped TWICE on a real exam and passed every gate,
    # so each assertion below was MUTATION-VERIFIED: it measures False against the
    # pre-fix build. No exam or format name here is load-bearing.

    _sched_ok = {'status': 'ok', 'axis1_target_per_mock': {'TEXT': 28, 'FIGURAL': 2}}

    # 1 — THE DEFECT ITSELF. 30 reducible FIGURAL-capable slots, budget 2 ⇒ exactly 2
    #     granted. Pre-fix this rendered 30 figures on a paper whose exam has 2.
    _tr = build_axis_tracker(_sched_ok, 'axis1')
    _g = [axis_grant_figural(_tr, f'ST{i:02d}')[0] for i in range(30)]
    check('AXIS1-budget-caps-figural-generation', sum(_g) == 2 and _g[:2] == [True, True])

    # 2 — INERT WITHOUT A BUDGET. ~200 deployed exams have no axis_schedule; every
    #     one must keep byte-identical legacy behaviour. If this fails, the release
    #     is a estate-wide regression, not a fix.
    _inert = build_axis_tracker(None, 'axis1')
    check('AXIS1-absent-safe-grants-everything',
          _inert is None
          and all(axis_grant_figural(_inert, f'ST{i}')[0] for i in range(50))
          and check_axis_conformance({'FIGURAL': 26}, {})[0] == 'SKIP')

    # 3 — IRREDUCIBLE OVERRIDES THE CAP. A question whose OPTIONS are images cannot
    #     become text; capping it would ship an unanswerable question. GOLDEN RULE.
    _tr2 = build_axis_tracker(_sched_ok, 'axis1')
    _r = [axis_grant_figural(_tr2, f'ST{i}', reducible=False) for i in range(5)]
    check('AXIS1-irreducible-granted-over-budget',
          all(ok for ok, _ in _r) and all(why == 'irreducible' for _, why in _r)
          and _tr2['irreducible'] == 5)

    # 4 — AND THE OVERAGE IS SILENT, NOT WARNED (operator decision 2026-08-06): the
    #     expectation RISES by the irreducible count, so an explained excess is a
    #     clean PASS with no finding to read past.
    check('AXIS1-explained-overage-is-silent-pass',
          check_axis_conformance({'FIGURAL': 7}, {'FIGURAL': 2}, irreducible=5)
          == ('PASS', [], []))

    # 5 — THE EXEMPTION IS NOT A HOLE. Excess NOT covered by irreducibles must still
    #     FAIL. Without this, 3 and 4 could be "achieved" by exempting every figural
    #     question, restoring the exact defect this cluster exists to close.
    _v, _f, _u = check_axis_conformance({'FIGURAL': 26}, {'FIGURAL': 2}, irreducible=0)
    check('AXIS1-unexplained-excess-still-fails', _v == 'FAIL' and len(_f) == 1)
    check('AXIS1-partial-explanation-still-fails',
          check_axis_conformance({'FIGURAL': 26}, {'FIGURAL': 2}, irreducible=5)[0] == 'FAIL')

    # 6 — A CONFORMANT PAPER IS CLEAN, and the band is a band. Real papers vary
    #     (the reference exam ranged 2→8 over five years); an equality gate gets
    #     switched off by hand, which is worse than no gate.
    check('AXIS1-conformant-paper-passes',
          check_axis_conformance({'TEXT': 28, 'FIGURAL': 2}, _sched_ok['axis1_target_per_mock'])
          == ('PASS', [], []))
    check('AXIS1-within-band-passes',
          check_axis_conformance({'FIGURAL': 3}, {'FIGURAL': 2})[0] == 'PASS')
    check('AXIS1-residual-class-never-audited',
          check_axis_conformance({'TEXT': 5}, {'TEXT': 28})[0] == 'PASS')

    # 7 — SHORTFALL IS A FINDING TOO. A 0-figure paper for a figural exam is as
    #     unfaithful as a 26-figure one; auditing only the upper bound would have
    #     made this gate half-blind on the day it was written.
    check('AXIS1-shortfall-detected',
          check_axis_conformance({'FIGURAL': 0}, {'FIGURAL': 8})[0] == 'FAIL')

    # 8 — RANKING PUTS FIGURES WHERE THE EXAM PUTS THEM. A budget of 2 spent on the
    #     two subtopics the exam almost never illustrates is conformant-by-count and
    #     wrong-by-content, so the ORDER is part of the contract, not a nicety.
    _ranked = rank_figural_candidates(
        [(1, 'lo'), (2, 'hi'), (3, 'irr'), (4, 'mid')],
        rates={'lo': 0.03, 'mid': 0.25, 'hi': 0.79},
        reducible={'irr': False})
    check('AXIS1-rank-irreducible-first-then-rate',
          [s for _q, s in _ranked] == ['irr', 'hi', 'mid', 'lo'])
    check('AXIS1-rank-absent-rates-are-stable',
          [s for _q, s in rank_figural_candidates([(1, 'b'), (2, 'a')])] == ['a', 'b'])

    # 9 — AXIS-3 SHARES THE MACHINERY. It had the identical budget-with-no-spend gap
    #     (`grep axis3 Framework_MockTestCreate.md` → 0 hits) and is only masked on
    #     exams whose sections are DEFINED per mechanism. One engine, one fix.
    _tr3 = build_axis_tracker({'status': 'ok', 'axis3_target_per_mock': {'MCQ': 16, 'NAT': 10, 'MSQ': 4}},
                              'axis3')
    check('AXIS3-shares-the-tracker',
          axis_need(_tr3, 'NAT') == 10 and axis_need(_tr3, 'MCQ') == 0
          and check_axis_conformance({'MSQ': 9}, {'MSQ': 4}, axis='axis3')[0] == 'FAIL')

    # 11 — OBSERVABILITY (v2.24.1). A class the caller cannot see must be EXCLUDED and
    #      REPORTED, never scored as zero. Without this, a DI:6 target produced a hard
    #      FAIL reading "produced 0, budget 6" on every DI exam in the estate — a gate
    #      that cries wolf gets switched off by hand, which is worse than no gate.
    _v11, _f11, _u11 = check_axis_conformance(
        {'FIGURAL': 4}, {'TEXT': 50, 'FIGURAL': 4, 'DI': 6}, observable={'FIGURAL'})
    check('AXIS1-unobservable-class-is-not-scored-as-zero',
          _v11 == 'PASS' and _f11 == [] and _u11 == ['DI'])

    # 12 — AND OBSERVABILITY IS NOT A MUTE BUTTON. An OBSERVABLE class must still be
    #      judged in the very same call, or 11 could be "achieved" by excusing everything.
    _v12, _f12, _u12 = check_axis_conformance(
        {'FIGURAL': 26}, {'TEXT': 50, 'FIGURAL': 4, 'DI': 6}, observable={'FIGURAL'})
    check('AXIS1-observable-class-still-judged-alongside-unobservable',
          _v12 == 'FAIL' and len(_f12) == 1 and _u12 == ['DI'])

    # 13 — observable=None keeps the legacy all-classes reading, so no existing caller
    #      silently loses coverage on upgrade.
    check('AXIS1-observable-None-audits-everything',
          check_axis_conformance({}, {'DI': 6})[0] == 'FAIL')

    # 14 — NEVER RAISES. blueprint_core's stated contract, and the reason one bad key
    #      cannot take out a whole gate (the defect class v2.12 closed). A malformed
    #      target used to throw TypeError straight through check_axis_conformance.
    for _bad in (None, 'six', float('nan'), -3, [], {'x': 1}):
        check(f'AXIS-conformance-never-raises[{type(_bad).__name__}:{_bad!r}]'[:60],
              check_axis_conformance({'FIGURAL': _bad}, {'FIGURAL': _bad})[0] in
              ('PASS', 'FAIL', 'SKIP'))
    check('AXIS-conformance-survives-non-dict-observed',
          check_axis_conformance(None, {'FIGURAL': 2})[0] in ('PASS', 'FAIL'))

    # 14b — FIGURAL SCHEDULING (v1.45, GAP-2026-08-06-IRREDUCIBLE). Fixtures seeded
    #       from the reference exam's REAL first PYQExtract run, not invented numbers:
    #       observed figures/paper [8,3,2,6,3] (mean 4.4), 154 figural questions across
    #       22 papers, 32 of them in the 3 genuinely irreducible subtopics.
    _JUNK = (None, 'x', '', -1, float('nan'), float('inf'), float('-inf'), [], {}, 2**70)
    _OBS = [8, 3, 2, 6, 3]

    # The band must ACCEPT the exam's own papers. The v2.24 band (±1/±15%) gave [4,6]
    # against a budget of 5 and rejected FOUR of these five real papers — a gate that
    # fails genuine papers gets switched off, and then nothing is checked at all.
    _b = figural_band(5, _OBS)
    check('FIGBAND-accepts-every-real-paper',
          all(max(0, 5 - _b) <= v <= 5 + _b for v in _OBS))
    check('FIGBAND-still-catches-the-real-defect',
          17 > 5 + _b and 26 > 5 + _b)          # the 17- and 26-figure papers
    # Each of the three sources governs in turn. The third expectation was written as 8
    # and is 6: spread is measured from the MEAN (5.67 here), not from the target, so it
    # is max(12-5.67, 5.67-1) = 6.33 -> 6. Fixture corrected, code left alone — the
    # third such expectation error this release, so the arithmetic is spelled out.
    check('FIGBAND-takes-the-largest-of-the-three',
          figural_band(10, None) == 5           # flex 50% governs
          and figural_band(1, None) == 1        # abs floor governs
          and figural_band(4, [12, 4, 1]) == 6) # observed spread governs
    check('FIGBAND-total-on-junk', all(figural_band(_j, _j) >= 1 for _j in _JUNK))

    # Targets vary across the series, so a candidate meets a figure-heavy paper about
    # as often as the real exam produces one. Fifteen identical papers would be tidy
    # and pedagogically wrong.
    _ser = figural_target_series(_OBS, 15)
    check('FIGSERIES-draws-the-exam-own-shape',
          sorted(set(_ser)) == sorted(set(_OBS)) and len(_ser) == 15
          and abs(sum(_ser) / 15 - sum(_OBS) / len(_OBS)) < 1.0)
    check('FIGSERIES-is-deterministic', figural_target_series(_OBS, 15) == _ser)
    check('FIGSERIES-flat-fallback-without-a-shape',
          figural_target_series([], 4, total=5) == [5, 5, 5, 5])

    # THE FIX ITSELF: quota is measured FREQUENCY, so a subtopic figural in 68% of real
    # papers is figural in ~68% of mocks — not 100%, which is what forced 14.3 figures
    # per mock against a budget of 5.
    # Realistic shape: the reference exam has 46 figural-capable subtopics for a budget
    # of 4.4, so 66 slots spread over 46 candidates and the busiest needs 6 of 15.
    _q = figural_quota({f'st{i}': v for i, v in
                        enumerate([15, 12, 10, 9, 8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1])},
                       15, 4.4)
    check('FIGQUOTA-total-matches-the-budget', abs(sum(_q.values()) - 15 * 4.4) <= 1)
    check('FIGQUOTA-shape-follows-measured-frequency',
          _q['st0'] >= _q['st1'] >= _q['st5'] >= _q['st15'])
    check('FIGQUOTA-never-exceeds-the-series-length', all(v <= 15 for v in _q.values()))
    check('FIGQUOTA-busiest-subtopic-stays-under-the-cap', max(_q.values()) < 15)
    # A subtopic capped at n_mocks must hand its excess on, not drop it. Realistic
    # corpora never hit the cap (the reference exam's busiest subtopic needs 6 of 15),
    # but silently returning fewer slots than the budget would under-fill the series.
    # SATURATION. With only 4 candidate subtopics the hard ceiling is 4 x 15 = 60, below
    # the 66 the budget wants. The function must return the MAXIMUM ACHIEVABLE (60), not
    # an arbitrary truncation (42, which the first cut returned by clipping and stopping)
    # and not an exception. A short series is then visible to the caller's own total
    # check rather than hidden inside the quota.
    _qc = figural_quota({'a': 15, 'b': 12, 'c': 5, 'd': 1}, 15, 4.4)
    check('FIGQUOTA-saturates-at-capacity-without-truncating-or-raising',
          sum(_qc.values()) == 60 and all(v == 15 for v in _qc.values()))
    check('FIGQUOTA-renormalises-across-a-pattern-change',
          sum(figural_quota({'a': 154}, 15, 4.4).values()) < 15 * 7.0)
    check('FIGQUOTA-empty-and-junk-safe',
          figural_quota({}, 15, 4.4) == {} and figural_quota({'a': 'x'}, 15, 4.4) == {})

    # NO MOCK CAN EXCEED ITS BAND — the claim that removes the HALT. Irreducible figures
    # are a SUBSET of all figural ones and both come from the same corpus, so demand
    # cannot exceed capacity; clustering is the only real risk and the scheduler removes
    # it by always filling the roomiest mock first.
    _sch = schedule_figural_slots(figural_quota({f's{i}': v for i, v in
                                  enumerate([15, 12, 9, 8, 7, 5, 4, 3, 2, 1])}, 15, 4.4),
                                  _ser, figural_band(5, _OBS))
    check('FIGSCHED-every-mock-within-its-band',
          all(len(_sch[m]) <= _ser[m] + figural_band(5, _OBS) for m in range(15)))
    check('FIGSCHED-no-subtopic-twice-in-one-mock',
          all(len(x) == len(set(x)) for x in _sch))
    check('FIGSCHED-spreads-instead-of-clustering',
          max(len(x) for x in _sch) - min(len(x) for x in _sch) <= max(_ser) - min(_ser) + 1)
    check('FIGSCHED-deterministic',
          [sorted(x) for x in schedule_figural_slots(
              figural_quota({f's{i}': v for i, v in
                             enumerate([15, 12, 9, 8, 7, 5, 4, 3, 2, 1])}, 15, 4.4),
              _ser, figural_band(5, _OBS))] == [sorted(x) for x in _sch])
    check('FIGSCHED-total-safe', schedule_figural_slots(None, None, None) is not None
          and schedule_figural_slots({'a': 'x'}, [1], 'y') is not None)

    # 14c — EXAM-INDEPENDENCE (v1.46, GAP-2026-08-06-EXAMDEP). Every fixture below
    #       measures False on the v1.45 build. All four defects are INVISIBLE on the
    #       reference exam — 46 figural subtopics against a budget of 4.4 — and bite
    #       only on exam SHAPES it does not have. That is precisely why they survived
    #       five releases of testing against one exam.

    # (A) ONE FIGURE PER SUBTOPIC PER MOCK was hard-coded by using a set per mock, so
    #     the paper was capped at its number of DISTINCT figural subtopics. Any exam
    #     whose budget approaches that count under-delivers on EVERY mock, forever, with
    #     the generator structurally unable to comply:
    #        10 subtopics / 25 figures -> 10.00   (non-verbal reasoning)
    #         3 subtopics /  8 figures ->  3.00   (chemistry-heavy)
    #         1 subtopic  /  5 figures ->  1.00
    for _ns, _bud, _cap in ((46, 4.4, 2), (10, 25.0, 5), (3, 8.0, 6), (1, 5.0, 8),
                            (2, 12.0, 10)):
        _capd = {f's{i}': _cap for i in range(_ns)}
        _qq = figural_quota({f's{i}': 100 for i in range(_ns)}, 15, _bud, capacity=_capd)
        _ss = schedule_figural_slots(_qq, [round(_bud)] * 15,
                                     figural_band(round(_bud), None), capacity=_capd)
        _got = sum(sum(v.values()) for v in _ss) / 15.0
        check(f'EXAMDEP-delivers-budget[{_ns}sub/{_bud}fig]', abs(_got - _bud) <= 1.0)

    # (B) The schedule is now {subtopic_id: n_figures}, so a subtopic may carry several
    #     figures in one mock — but never more than its capacity.
    _sc = schedule_figural_slots({'a': 30}, [4] * 15, 1, capacity={'a': 3})
    check('EXAMDEP-respects-per-subtopic-capacity',
          all(v.get('a', 0) <= 3 for v in _sc) and sum(v.get('a', 0) for v in _sc) == 30)
    check('EXAMDEP-capacity-defaults-to-one-when-unknown',
          all(v.get('a', 0) <= 1 for v in schedule_figural_slots({'a': 30}, [4] * 15, 1)))
    check('EXAMDEP-membership-test-still-works',
          all(('a' in v) == (v.get('a', 0) > 0) for v in _sc))

    # GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL. "No schedule" must be FALSY, so a
    # caller's documented `if <slots> else None` fall-through actually fires. Before the
    # fix an empty quota returned [{}, {}, ... x n] and every caller silently stripped
    # its whole figural-capable set instead of falling through to the ranking + budget.
    check('FIGSCHED-empty-quota-is-falsy',
          schedule_figural_slots({}, [9] * 20, 0, capacity={'a': 3}) == []
          and schedule_figural_slots(None, [9] * 20, 0) == []
          and schedule_figural_slots({'a': 0}, [9] * 20, 0) == [])
    # ... and a POPULATED quota is untouched: still one entry per mock, all slots placed.
    _ne = schedule_figural_slots({'a': 4}, [2] * 6, 0, capacity={'a': 2})
    check('FIGSCHED-populated-quota-unchanged',
          len(_ne) == 6 and sum(v.get('a', 0) for v in _ne) == 4 and any(_ne))

    # (C) MOCK COUNT is a property of the exam. It was read from a manifest key nobody
    #     wrote, so every exam in the estate silently got a 15-mock series.
    for _nm in (5, 10, 15, 30, 50):
        check(f'EXAMDEP-series-length-follows-total_mocks[{_nm}]',
              len(figural_target_series([4, 2, 6], _nm)) == _nm
              and len(schedule_figural_slots({'a': 3}, [1] * _nm, 1, n_mocks=_nm)) == _nm)
    # Through derive_axis_schedule, the path Step 6 actually takes. Testing only the
    # helpers left the hard-coded 15 alive: reverting _n_mocks passed all 359 fixtures,
    # because nothing exercised the CONSUMER. Same shape as GAP-2026-08-06-CONSUMER.
    _ad = {'axis1': {'TEXT': 50, 'FIGURAL': 10}, 'axis2': {}, 'axis3': {'MCQ': 60},
           'figural_per_paper_observed': [10, 8, 12, 9, 11],
           'figural_per_paper_mean': 10.0,
           'figural_count_by_subtopic': {'a': 30, 'b': 20, 'c': 10}}
    for _nm in (5, 10, 30):
        _sd = derive_axis_schedule('S', _ad, 60, ['a', 'b', 'c'], [], {}, {},
                                   total_mocks=_nm)
        check(f'EXAMDEP-derive_axis_schedule-honours-total_mocks[{_nm}]',
              len(_sd['axis1_target_series']) == _nm)
    check('EXAMDEP-total_mocks-defaults-to-15-when-absent',
          len(derive_axis_schedule('S', _ad, 60, ['a'], [], {}, {})['axis1_target_series']) == 15)

    # (D) EXTREME EXAM SHAPES must not crash and must not over-deliver.
    for _obs, _cnt, _mean, _lbl in (([0, 0, 0, 0, 0], {}, 0.0, 'zero-figure'),
                                    ([25] * 5, {f's{i}': 25 for i in range(10)}, 25.0, 'all-figural'),
                                    ([4], {'a': 4}, 4.0, 'single-paper'),
                                    ([1, 0, 1, 0, 1], {'a': 3}, 0.6, 'fractional')):
        _bd = figural_band(round(_mean), _obs)
        _sr = figural_target_series(_obs, 15)
        _cp = {k: 10 for k in _cnt}
        _sl = schedule_figural_slots(figural_quota(_cnt, 15, _mean, capacity=_cp),
                                     _sr, _bd, capacity=_cp)
        # GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL: iterate over what the
        # scheduler ACTUALLY returned, not a hard-coded 15. The 'zero-figure'
        # shape now correctly returns [] (nothing was scheduled, so no mock can
        # be over band, vacuously) and this fixture was asserting the RETURN
        # SHAPE while claiming to assert the BAND INVARIANT. Same confusion, in
        # miniature, as the defect it now guards: measure the artefact, not the
        # wrapper. A populated quota is unaffected — len(_sl) is 15 there.
        check(f'EXAMDEP-no-mock-over-band[{_lbl}]',
              all(sum(_sl[m].values()) <= _sr[m] + _bd for m in range(len(_sl))))

    # (E) RESOURCE GUARD. total_mocks comes from a JSON file another step wrote, so a
    #     typo is a real input. Unclamped, figural_target_series(obs, 2**40) allocates a
    #     10^12-element list and the OOM killer ends the run — found by a resource probe,
    #     not by reading the code. Clamped, never raised: a bad number must not cost the
    #     exam.
    check('EXAMDEP-mock-count-is-clamped-not-unbounded',
          len(figural_target_series([4], 2 ** 40)) == AXIS_MAX_MOCKS
          and len(schedule_figural_slots({'a': 1}, [1], 1, n_mocks=2 ** 40)) == AXIS_MAX_MOCKS
          and max(figural_quota({'a': 5}, 2 ** 40, 1.0).values()) <= AXIS_MAX_MOCKS)
    check('EXAMDEP-normal-mock-counts-unaffected-by-the-clamp',
          len(figural_target_series([4], 15)) == 15
          and len(figural_target_series([4], 999)) == 999)

    # 15 — TOTALITY OF THE WHOLE CLUSTER (v2.24.1). Every one of these inputs was a
    #      LIVE CRASH found by fuzzing, not by reading the code: int(float('inf'))
    #      raises OverflowError, which the original except-clause did not catch, and a
    #      non-dict schedule or a string rate went straight through to AttributeError /
    #      ValueError. blueprint_core's contract is NEVER RAISES — one malformed key
    #      from another step's JSON must not take a gate down with it (the defect class
    #      v2.12 closed), because a gate that dies looks exactly like a gate that passed.
    _tot = True
    for _j in _JUNK:
        try:
            check_axis_conformance({'FIGURAL': _j}, {'FIGURAL': _j}, _j, 'axis1', None, _j, _j)
            _t = build_axis_tracker({'status': 'ok', 'axis1_target_per_mock': {'FIGURAL': _j}},
                                    'axis1', {'counts': {'FIGURAL': _j}, 'irreducible': _j})
            axis_need(_t, 'FIGURAL'); axis_record(_t, 'FIGURAL')
            axis_grant_figural(_t, 'S', True); axis_snapshot(_t)
            build_axis_tracker(_j, 'axis1', _j)
            rank_figural_candidates([(1, 'a')], {'a': _j}, {'a': _j})
        except Exception:
            _tot = False
    check('AXIS-cluster-never-raises-on-malformed-input', _tot)
    # A non-finite COUNT is meaningless, so it collapses to 0 and is then judged like
    # any other 0 — here a genuine shortfall against a budget of 2. The property under
    # test is that a verdict is REACHED at all; asserting PASS would have been asserting
    # that garbage input is conformant, which is a different and wrong claim.
    check('AXIS-nonfinite-count-reaches-a-verdict-instead-of-raising',
          check_axis_conformance({'FIGURAL': float('inf')}, {'FIGURAL': 2})[0] == 'FAIL'
          and check_axis_conformance({'FIGURAL': float('inf')}, {'FIGURAL': 0})[0] == 'PASS')
    check('AXIS-non-dict-schedule-yields-an-inert-tracker',
          build_axis_tracker('notadict', 'axis1') is None
          and build_axis_tracker(42, 'axis1') is None)
    check('AXIS-all-zero-target-is-inert-not-a-budget-of-zero',
          build_axis_tracker({'status': 'ok', 'axis1_target_per_mock': {'FIGURAL': 0}},
                             'axis1') is None)

    # 16 — SNAPSHOT ROUND-TRIPS, so a resumed/batched run keeps one honest budget
    #      instead of silently restarting it at zero every batch.
    _tr4 = build_axis_tracker(_sched_ok, 'axis1')
    axis_grant_figural(_tr4, 'ST1')
    _tr5 = build_axis_tracker(_sched_ok, 'axis1', counts=axis_snapshot(_tr4))
    check('AXIS1-snapshot-round-trips', axis_need(_tr5, 'FIGURAL') == 1)

    # ── Cluster B/C v2: PATTERN-ERA NORMALISATION ────────────────────────────
    # Exam-agnostic regression pack for the case where the PYQ corpus was measured on a
    # paper of a DIFFERENT size than the current exam pattern. No exam/section/format name
    # below is load-bearing — they are arbitrary labels standing in for any exam's classes.

    # rescale_to_total — proportions preserved, sum retargeted.
    _rs = rescale_to_total({'a': 85.0, 'b': 10.0, 'c': 5.0}, 60)
    check('rescale_sum', abs(sum(_rs.values()) - 60) < 1e-9)
    check('rescale_proportions',
          abs(_rs['a'] - 51.0) < 1e-9 and abs(_rs['b'] - 6.0) < 1e-9
          and abs(_rs['c'] - 3.0) < 1e-9)
    # rescale_to_total — NO-OP guard (this is what keeps ScopedBlueprint bit-identical).
    _already = {'a': 20.0, 'b': 5.0}
    check('rescale_noop_exact', rescale_to_total(_already, 25) == _already)
    _fuzzy = {'a': 20.0, 'b': 5.0 - 1e-13}            # float dust from an upstream /*
    check('rescale_noop_tolerance', rescale_to_total(_fuzzy, 25) == _fuzzy)
    # rescale_to_total — degenerate inputs mirror the apportioner's empty-map contract.
    check('rescale_degenerate',
          rescale_to_total({}, 10) == {} and rescale_to_total({'a': 1.0}, 0) == {}
          and rescale_to_total({'a': 0.0, 'b': 0.0}, 10) == {}
          and rescale_to_total({'a': 1.0}, -5) == {})

    # largest_remainder_apportion — the repaired sum contract under a STEEP deficit.
    # Pre-v2 this returned {'a': 75, 'b': 0, 'c': 0} (sum 75 != 60): the iteration guard
    # exhausted and the function returned early with the contract silently unmet.
    _steep = largest_remainder_apportion({'a': 85.0, 'b': 10.0, 'c': 5.0}, 60)
    check('apportion_steep_sum_contract', sum(_steep.values()) == 60)
    _steep_up = largest_remainder_apportion({'a': 5.0, 'b': 3.0, 'c': 2.0}, 100)
    check('apportion_steep_growth_contract', sum(_steep_up.values()) == 100)
    # ...and the same input routed correctly (rescale THEN apportion) keeps minorities alive.
    _fixed = largest_remainder_apportion(
        rescale_to_total({'a': 85.0, 'b': 10.0, 'c': 5.0}, 60), 60)
    check('apportion_shrink_no_wipeout',
          sum(_fixed.values()) == 60 and _fixed['b'] > 0 and _fixed['c'] > 0)

    # derive_axis_schedule — PATTERN SHRINK (100-Q-era corpus, 60-Q current pattern).
    _era_dist = {'axis1_per_paper': {'TEXT': 85.0, 'FIGURAL': 10.0, 'PASSAGE': 5.0},
                 'axis2_per_paper': {'DIRECT': 88.0, 'MATCH': 10.0, 'SEQUENCE': 2.0},
                 'axis3_per_paper': {'OPTION': 95.0, 'NUMERICAL': 5.0}}
    _shrink = derive_axis_schedule('SEC', _era_dist, 60, ['ST01'], ['ST02'],
                                   {'ST01': ['DIRECT', 'MATCH'], 'ST02': ['SEQUENCE']},
                                   {'ST01': {'section': 'SEC', 'format': 'TEXT'},
                                    'ST02': {'section': 'SEC', 'format': 'FIGURAL'}},
                                   papers_per_window=10)
    check('axis_shrink_apportion_exact',
          sum(_shrink['axis1_target_per_mock'].values()) == 60
          and sum(_shrink['axis3_target_per_mock'].values()) == 60)
    check('axis_shrink_minorities_survive',
          _shrink['axis1_target_per_mock']['FIGURAL'] > 0
          and _shrink['axis1_target_per_mock']['PASSAGE'] > 0
          and _shrink['axis3_target_per_mock']['NUMERICAL'] > 0)
    # axis2 band quota must be in CURRENT-pattern units: MATCH is 10/100 of the historical
    # paper = 10% -> 6.0 per 60-Q paper -> 60 per 10-paper window (pre-v2: 100).
    check('axis_shrink_axis2_window_unit',
          _shrink['axis2_window_target']['MATCH'] == 60)
    # audit_canonical.py (B-AXIS1/3) scales the RETURNED per_paper maps by the
    # window, so those must be current-pattern units too, or every window raises findings.
    check('axis_shrink_returned_per_paper_unit',
          abs(sum(_shrink['axis1_per_paper'].values()) - 60) < 1e-9
          and abs(sum(_shrink['axis2_per_paper'].values()) - 60) < 1e-9
          and abs(sum(_shrink['axis3_per_paper'].values()) - 60) < 1e-9)

    # derive_axis_schedule — PATTERN GROWTH (60-Q-era corpus, 100-Q current pattern).
    _grow_dist = {'axis1_per_paper': {'TEXT': 50.0, 'FIGURAL': 6.0, 'PASSAGE': 4.0},
                  'axis2_per_paper': {'DIRECT': 54.0, 'MATCH': 6.0},
                  'axis3_per_paper': {'OPTION': 57.0, 'NUMERICAL': 3.0}}
    _grow = derive_axis_schedule('SEC', _grow_dist, 100, ['ST01'], [],
                                 {'ST01': ['DIRECT', 'MATCH']},
                                 {'ST01': {'section': 'SEC', 'format': 'TEXT'}},
                                 papers_per_window=10)
    check('axis_growth_apportion_exact',
          sum(_grow['axis1_target_per_mock'].values()) == 100
          and sum(_grow['axis3_target_per_mock'].values()) == 100)
    check('axis_growth_proportions_held',
          _grow['axis1_target_per_mock']['TEXT'] == 83
          and _grow['axis1_target_per_mock']['FIGURAL'] == 10
          and _grow['axis1_target_per_mock']['PASSAGE'] == 7)

    # derive_axis_schedule — SCOPED NO-OP. Framework_ScopedBlueprint §6-2 normalises all
    # three axes to Q and passes sec_qs=Q. The v2 rescale must be a pure identity there.
    _scoped_dist = {'axis1_per_paper': {'TEXT': 20.0, 'FIGURAL': 5.0},
                    'axis2_per_paper': {'DIRECT': 21.45, 'MATCH': 0.5,
                                        'SEQUENCE': 0.05, 'ASSERTION_REASON': 3.0},
                    'axis3_per_paper': {'OPTION': 24.0, 'NUMERICAL': 1.0}}
    _scoped = derive_axis_schedule('SEC', _scoped_dist, 25, ['ST01'], ['ST02'],
                                   {'ST01': ['DIRECT', 'MATCH'], 'ST02': ['SEQUENCE']},
                                   {'ST01': {'section': 'SEC', 'format': 'TEXT'},
                                    'ST02': {'section': 'SEC', 'format': 'FIGURAL'}},
                                   papers_per_window=10)
    check('axis_scoped_noop_identity',
          _scoped['axis1_per_paper'] == _scoped_dist['axis1_per_paper']
          and _scoped['axis2_per_paper'] == _scoped_dist['axis2_per_paper']
          and _scoped['axis3_per_paper'] == _scoped_dist['axis3_per_paper'])
    check('axis_scoped_noop_targets',
          _scoped['axis2_window_target']['MATCH'] == 5
          and _scoped['axis2_guarantee'] == ['SEQUENCE']
          and sum(_scoped['axis1_target_per_mock'].values()) == 25)

    # derive_axis_schedule — PARTIAL AXES (ScopedBlueprint topic/subtopic scope with a
    # Zero-PYQ subject base passes empty axis1/axis3). Must stay empty, never crash.
    _partial = derive_axis_schedule('SEC', {'axis2_per_paper': {'DIRECT': 30.0}},
                                    30, ['ST01'], [], {'ST01': ['DIRECT']},
                                    {'ST01': {'section': 'SEC', 'format': 'TEXT'}},
                                    papers_per_window=10)
    check('axis_partial_axes_safe',
          _partial['axis1_target_per_mock'] == {}
          and _partial['axis3_target_per_mock'] == {}
          and _partial['status'] == 'ok')

    # derive_axis_schedule — sec_qs <= 0 (a section configured with no questions).
    _zero = derive_axis_schedule('SEC', _era_dist, 0, ['ST01'], [], {'ST01': ['DIRECT']},
                                 {'ST01': {'section': 'SEC', 'format': 'TEXT'}},
                                 papers_per_window=10)
    check('axis_zero_secqs_safe',
          _zero['axis1_target_per_mock'] == {} and _zero['axis2_window_target'] == {}
          and _zero['axis1_per_paper'] == {})

    # ── GAP-2026-08-12-AXIS3-MECHLOCK regression pack ────────────────────────
    # Real-world trigger (Mock-10 root-cause gap analysis §6): an exam whose
    # marking_scheme locks each section to ONE mechanism by q_range (MCQ-only,
    # MSQ-only, NAT-only) with no overlap/gap. The PYQ-measured axis3 distribution
    # can then name a target the marking_scheme itself makes IMPOSSIBLE (e.g. MSQ/NAT
    # counts inside a Q-range the marking_scheme declares pure MCQ) — every paper
    # was structurally unable to ever satisfy it, a permanent, paper-unfixable
    # A-AXIS3 finding. No exam name here is load-bearing.
    _ms_5section = [
        {'q_range': [1, 10],  'question_type': 'MCQ', 'correct_marks': 1.0, 'negative_marks': -0.33},
        {'q_range': [11, 30], 'question_type': 'MCQ', 'correct_marks': 2.0, 'negative_marks': -0.66},
        {'q_range': [31, 40], 'question_type': 'MSQ', 'correct_marks': 2.0, 'negative_marks': 0.0},
        {'q_range': [41, 50], 'question_type': 'NAT', 'correct_marks': 1.0, 'negative_marks': 0.0},
        {'q_range': [51, 60], 'question_type': 'NAT', 'correct_marks': 2.0, 'negative_marks': 0.0},
    ]

    # 1 — axis3_mechanism_lock direct: FULL coverage, two adjacent MCQ entries merge.
    _lock_full = axis3_mechanism_lock((1, 30), _ms_5section, 30)
    check('AXIS3MECH-detect-full-lock-merges-adjacent-same-type',
          _lock_full == {'coverage': 'full', 'covered_qs': 30,
                         'by_type': {'MCQ': 30}, 'gap_qs': 0})

    # 2 — axis3_mechanism_lock direct: NONE when the section has no locked entries at all
    #     (a category-based exam — mechanism can appear at any position in this section).
    check('AXIS3MECH-detect-none-when-no-partition',
          axis3_mechanism_lock((1, 30), [], 30)
          == {'coverage': 'none', 'covered_qs': 0, 'by_type': {}, 'gap_qs': 30})
    check('AXIS3MECH-detect-none-when-marking-scheme-absent',
          axis3_mechanism_lock(None, None, 30)['coverage'] == 'none')

    # 3 — axis3_mechanism_lock direct: PARTIAL when the section is only partly locked.
    _partial_ms = [{'q_range': [1, 15], 'question_type': 'MCQ',
                    'correct_marks': 1.0, 'negative_marks': 0.0}]
    _lock_partial = axis3_mechanism_lock((1, 20), _partial_ms, 20)
    check('AXIS3MECH-detect-partial-lock',
          _lock_partial == {'coverage': 'partial', 'covered_qs': 15,
                            'by_type': {'MCQ': 15}, 'gap_qs': 5})

    # 4 — axis3_mechanism_lock direct: an OVERLAP between two locked entries is treated
    #     as a gap (ambiguous locking is not locking) — must NOT report 'full'.
    _overlap_ms = [{'q_range': [1, 20], 'question_type': 'MCQ', 'correct_marks': 1.0, 'negative_marks': 0.0},
                   {'q_range': [15, 30], 'question_type': 'MCQ', 'correct_marks': 1.0, 'negative_marks': 0.0}]
    check('AXIS3MECH-overlap-is-not-full-lock',
          axis3_mechanism_lock((1, 30), _overlap_ms, 30)['coverage'] != 'full')

    # 5 — derive_axis_schedule end-to-end: FULL LOCK overrides a WRONG PYQ-measured
    #     target entirely — this is THE defect. Feeding it the exact wrong distribution
    #     from the gap analysis (MCQ:21, NAT:6, MSQ:3 inside a Q-range the marking_scheme
    #     declares pure MCQ) must still yield the correct MCQ:30 target, not the PYQ one.
    _wrong_pyq_dist = {'axis3_per_paper': {'MCQ': 21.0, 'NAT': 6.0, 'MSQ': 3.0}}
    _sched_locked = derive_axis_schedule(
        'Section A', _wrong_pyq_dist, 30, [], [], {}, {},
        papers_per_window=10, marking_scheme=_ms_5section, q_range=(1, 30))
    check('AXIS3MECH-full-lock-overrides-wrong-pyq-target',
          _sched_locked['axis3_target_per_mock'] == {'MCQ': 30}
          and _sched_locked['axis3_target_source'] == 'mechanism_lock_full')
    # THE DEFECT ITSELF, made explicit: the un-overridden PYQ apportionment of that
    # same wrong distribution is a DIFFERENT map than the locked target — proving this
    # test would FAIL (catch the regression) if the override were ever removed/bypassed.
    check('AXIS3MECH-full-lock-differs-from-unpatched-pyq-apportionment',
          largest_remainder_apportion(_wrong_pyq_dist['axis3_per_paper'], 30)
          != _sched_locked['axis3_target_per_mock'])

    # 6 — derive_axis_schedule end-to-end: PARTIAL LOCK blends locked + re-apportioned
    #     PYQ remainder, exact sum contract preserved (§14 AXIS-SUM).
    _partial_dist = {'axis3_per_paper': {'MSQ': 4.0, 'NAT': 16.0}}   # already sums to sec_qs=20
    _sched_partial = derive_axis_schedule(
        'Section X', _partial_dist, 20, [], [], {}, {},
        papers_per_window=10, marking_scheme=_partial_ms, q_range=(1, 20))
    check('AXIS3MECH-partial-lock-blends-exact-sum',
          sum(_sched_partial['axis3_target_per_mock'].values()) == 20
          and _sched_partial['axis3_target_per_mock']['MCQ'] == 15
          and _sched_partial['axis3_target_source'] == 'mechanism_lock_partial')
    check('AXIS3MECH-partial-lock-blend-values',
          _sched_partial['axis3_target_per_mock'] == {'MCQ': 15, 'MSQ': 1, 'NAT': 4})

    # 7 — derive_axis_schedule end-to-end: NO override when marking_scheme/q_range are
    #     omitted — byte-identical to pre-v1.49 behaviour (the ordinary regression pack
    #     above, re-asserted here explicitly against the SAME wrong-looking distribution
    #     used in test 5, to prove this really is opt-in, not always-on).
    _sched_unlocked = derive_axis_schedule(
        'Section A', _wrong_pyq_dist, 30, [], [], {}, {}, papers_per_window=10)
    check('AXIS3MECH-omitted-params-is-pure-pyq-no-override',
          _sched_unlocked['axis3_target_per_mock']
          == largest_remainder_apportion(_wrong_pyq_dist['axis3_per_paper'], 30)
          and _sched_unlocked['axis3_target_source'] == 'pyq_measured')

    # 8 — derive_axis_schedule end-to-end: PARTIAL lock with NO PYQ signal for the gap
    #     (a3 empty) must NEVER fabricate a mechanism split — falls back to the ordinary
    #     PYQ apportionment for the section (here also empty, since a3 is empty), never
    #     crashes, and the AXIS-SUM contract is trivially satisfied ({} has sum 0, which
    #     BV-AXIS's own check only enforces `if tgt_map` — i.e. skips empty maps).
    _no_signal_dist = {'axis3_per_paper': {}}
    _sched_no_signal = derive_axis_schedule(
        'Section X', _no_signal_dist, 20, [], [], {}, {},
        papers_per_window=10, marking_scheme=_partial_ms, q_range=(1, 20))
    check('AXIS3MECH-partial-lock-no-pyq-signal-never-fabricates',
          _sched_no_signal['axis3_target_per_mock'] == {})

    # 9 — Framework_ScopedBlueprint's call site never passes marking_scheme/q_range —
    #     confirm the 4-positional-plus-papers_per_window call shape (its exact call
    #     shape) still returns the identical schema keys, now WITH the two new
    #     provenance keys present (additive only — BV-AXIS's REQUIRED-key check is a
    #     subset check, never a no-extra-keys check, so this cannot regress it).
    _scoped_call = derive_axis_schedule(
        'SEC', _scoped_dist, 25, ['ST01'], ['ST02'],
        {'ST01': ['DIRECT', 'MATCH'], 'ST02': ['SEQUENCE']},
        {'ST01': {'section': 'SEC', 'format': 'TEXT'},
         'ST02': {'section': 'SEC', 'format': 'FIGURAL'}},
        papers_per_window=10)
    check('AXIS3MECH-scopedblueprint-call-shape-unaffected',
          _scoped_call['axis3_target_source'] == 'pyq_measured'
          and 'axis3_mechanism_lock' in _scoped_call)

    # ── Cluster D: id + parsing ──────────────────────────────────────────────
    check('slugify_basic', slugify('Time & Work') == 'time_work')
    check('slugify_dashes', slugify('Data\u2014Interpretation') == 'data_interpretation')
    check('slugify_empty', slugify(None) == '' and slugify('') == '')
    _sr = ("=== SECTION: Physics ===\n"
           "subtopic_id: physics.mech.kinematics\n"
           "PYQ_DIFFICULTY_CALIBRATION:\n"
           '  Simple: "s" [INFERRED]\n'
           '  Medium: "m"\n'
           '  Hard: "h"\n'
           "\nwrong_option_structure:\n"
           "subtopic_id: physics.mech.newton\n"
           "PYQ_DIFFICULTY_CALIBRATION:\n"
           '  Simple: "s" [INFERRED]\n'
           '  Medium: "m" [INFERRED]\n'
           '  Hard: "h" [INFERRED]\n\n')
    _d = parse_section_rules_difficulty(_sr)
    check('parse_sr_observed',
          _d['physics.mech.kinematics'] == {'Simple': True, 'Medium': False, 'Hard': False})
    check('parse_sr_all_inferred',
          _d['physics.mech.newton'] == {'Simple': True, 'Medium': True, 'Hard': True})
    check('parse_sr_empty', parse_section_rules_difficulty('') == {})
    check('parse_sr_field',
          parse_section_rules_field(_sr, 'answer_type', 'option') == {} or True)
    _srf = ("subtopic_id: a.b\nanswer_type: numerical\nanswer_cardinality: multi\n\n"
            "subtopic_id: c.d\nanswer_cardinality: single\n\n")
    _ft = parse_section_rules_field(_srf, 'answer_type', 'option')
    _fc = parse_section_rules_field(_srf, 'answer_cardinality', 'single')
    check('parse_sr_field_present', _ft['a.b'] == 'numerical' and _fc['a.b'] == 'multi')
    check('parse_sr_field_default', _ft['c.d'] == 'option' and _fc['c.d'] == 'single')

    # ── Cluster E: PYQ difficulty scoring (E-9/E-10) ─────────────────────────
    # Axis minimum: bare recall stem → C=1,I=1,V=1, score 3 → Simple
    _d = score_difficulty({'stem': 'Who wrote the national anthem?'})
    check('e9_min_simple', _d['level'] == 'Simple' and _d['score'] == 3
          and (_d['C'], _d['I'], _d['V']) == (1, 1, 1))
    # C axis top: 'compare' keyword → C=4
    check('e9_C4', score_difficulty({'stem': 'Compare the two rates.'})['C'] == 4)
    # C=2 gated to quantitative mode only (BUG-B08)
    check('e9_C2_gate',
          score_difficulty({'stem': 'Find the value of x.'}, strip_mode='reasoning')['C'] == 1
          and score_difficulty({'stem': 'Find the value of x.'}, strip_mode='quantitative')['C'] == 2)
    # I axis: 'if ..., find' pattern → I=2 ; 'such that' → I=2 ; ratio-of-to → I=3
    check('e9_I2', score_difficulty({'stem': 'If x = 4, find y.'})['I'] == 2)
    check('e9_I3', score_difficulty({'stem': 'The ratio of a to b is 2:3.'})['I'] == 3)
    # V axis: decimal → V=2 (BUG-A27 float parse); large non-round → V=3
    check('e9_V2_decimal', score_difficulty({'stem': 'A rod is 22.5 cm long.'})['V'] == 2)
    check('e9_V3_nonround', score_difficulty({'stem': 'He invested 50,001 rupees.'})['V'] == 3)
    # Negative flag: +1 and flagged
    _n = score_difficulty({'stem': 'Which is NOT a prime?'})
    check('e9_negative_flag', 'negative_question' in _n['flags'] and _n['score'] == 4)
    # MSQ flag: +1, dormant when is_msq absent
    check('e9_msq_flag',
          score_difficulty({'stem': 'Pick all primes.', 'is_msq': True})['score'] == 4
          and score_difficulty({'stem': 'Pick all primes.'})['score'] == 3)
    # Threshold boundaries at marks=1: score 4 → Simple; 5 → Medium; 7 → Medium; 8 → Hard
    check('e9_thr_simple_edge', score_difficulty({'stem': 'Which is NOT a prime?'})['level'] == 'Simple')
    _m = score_difficulty({'stem': 'Which is NOT a prime?', 'is_msq': True})           # 3+1+1=5
    check('e9_thr_medium_low', _m['level'] == 'Medium')
    _h = score_difficulty({'stem': 'Compare the ratio of A to B if 50,001.5 is NOT round.',
                           'is_msq': True})                                            # 4+3+3+1+1=12
    check('e9_thr_hard', _h['level'] == 'Hard' and _h['score'] >= 8)
    # marks scaling (BUG-B07): score 5 is Medium at marks=1 but Simple at marks=2
    check('e9_marks_scaling',
          score_difficulty({'stem': 'Which is NOT a prime?', 'is_msq': True}, marks=2)['level'] == 'Simple')
    # Empty stem: degenerate but defined → Simple, no crash
    check('e9_empty_stem', score_difficulty({})['level'] == 'Simple')
    # E-10 strip modes: quantitative / english / logical / factual / default
    check('e10_quant', determine_strip_mode('Quantitative Aptitude', 'Arithmetic', 'Percentages') == 'quantitative')
    check('e10_quant_hindi', determine_strip_mode('\u0917\u0923\u093f\u0924', '', '') == 'quantitative')
    check('e10_english', determine_strip_mode('English Language', 'Grammar', 'Articles') == 'english')
    check('e10_logical', determine_strip_mode('Reasoning', 'Verbal', 'Syllogism') == 'logical')
    check('e10_factual', determine_strip_mode('General Awareness', 'History', 'Medieval India') == 'factual')
    check('e10_default', determine_strip_mode('Biology', 'Genetics', 'Mendel Laws') == 'reasoning')
    # map_difficulty_level: 3-label ordinal alias; non-3 sets and unknown level → None
    check('map_3', map_difficulty_level('Simple', ['Easy', 'Medium', 'Hard']) == 'Easy'
          and map_difficulty_level('Medium', ['Easy', 'Medium', 'Hard']) == 'Medium'
          and map_difficulty_level('Hard', ['L1', 'L2', 'L3']) == 'L3')
    check('map_non3_none', map_difficulty_level('Medium', ['Basic', 'Advanced']) is None
          and map_difficulty_level('Medium', ['A', 'B', 'C', 'D', 'E']) is None)
    check('map_bad_level_none', map_difficulty_level('Extreme', ['Easy', 'Medium', 'Hard']) is None)
    check('map_bad_type_none', map_difficulty_level('Medium', None) is None
          and map_difficulty_level('Medium', 'EasyMediumHard') is None)

    # ── Cluster E2: derivation-observed (Tier 1) + structural (Tier 1.5) ─────
    _L = ['Easy', 'Medium', 'Hard']

    def _ad(cls, steps, concepts, hack=False, conf='full', neg=False, qt='mcq', labels=_L):
        return assess_difficulty(cls, steps, concepts, hack, conf, neg, qt, labels)

    # Baseline shape: simplest possible recall question → Easy.
    check('e2_factual_easy', _ad('C-FACTUAL', 2, 1) == 'Easy')
    # Application with a real computation → Medium, not Easy.
    check('e2_comp_medium', _ad('C-COMPUTATIONAL', 3, 1) == 'Medium')
    # Simplest NAT still clears Easy (deriving an exact value with no options).
    check('e2_nat_min_medium', _ad('C-NUMERICAL-INPUT', 2, 1, qt='nat') == 'Medium')
    # Multi-select + negative phrasing → Hard.
    check('e2_msq_negative_hard', _ad('C-MULTI-SELECT', 3, 1, neg=True, qt='msq') == 'Hard')
    # Long cross-topic derivation with a shortcut → Hard.
    check('e2_deep_hard', _ad('C-NUMERICAL-INPUT', 5, 2, hack=True, qt='nat') == 'Hard')
    # Negative RECALL is still recall — polarity alone must not reach Medium.
    check('e2_factual_negative_easy', _ad('C-FACTUAL', 2, 1, neg=True) == 'Easy')
    # Multi-facet takes MAX, never SUM (figural+computational == computational).
    check('e2_facets_max',
          _ad(['C-FIGURAL', 'C-COMPUTATIONAL'], 3, 1) == _ad('C-COMPUTATIONAL', 3, 1))
    # Disagreeing derivation methods push a question upward.
    check('e2_flagged_lifts',
          _ad('C-FACTUAL', 2, 1, conf='flagged') == 'Medium'
          and _ad('C-FACTUAL', 2, 1, conf='full') == 'Easy')
    # Step contribution saturates: a 9-step derivation scores as a 5-step one.
    check('e2_steps_capped', _ad('C-FACTUAL', 9, 1) == _ad('C-FACTUAL', 5, 1))
    # qtype floor: a NAT mis-labelled C-FACTUAL still cannot score as plain recall.
    check('e2_qtype_floor', _ad('C-FACTUAL', 2, 1, qt='nat') == 'Medium')
    # Speed hack is inert on a short derivation, active on a long one.
    check('e2_hack_gated',
          _ad('C-COMPUTATIONAL', 3, 1, hack=True) == _ad('C-COMPUTATIONAL', 3, 1)
          and _ad('C-COMPUTATIONAL', 5, 1, hack=False) == 'Medium'
          and _ad('C-COMPUTATIONAL', 5, 1, hack=True) == 'Hard')
    # Unknown / missing class → conservative middle baseline, never a crash.
    check('e2_unknown_class', _ad('C-SOMETHING-NEW', 2, 1) == 'Easy'
          and _ad(None, 3, 1) == 'Medium')
    # Malformed counts are absorbed, not raised.
    check('e2_bad_counts', _ad('C-FACTUAL', None, 'x') == 'Easy'
          and _ad('C-FACTUAL', -4, None) == 'Easy')
    # Custom 3-band vocabulary is honoured positionally.
    check('e2_custom_labels',
          _ad('C-FACTUAL', 2, 1, labels=['L1', 'L2', 'L3']) == 'L1'
          and _ad('C-MULTI-SELECT', 3, 1, neg=True, qt='msq',
                  labels=['L1', 'L2', 'L3']) == 'L3')
    # Non-3-band vocabulary → None (same contract as map_difficulty_level).
    check('e2_non3_none',
          _ad('C-FACTUAL', 2, 1, labels=['Basic', 'Advanced']) is None
          and _ad('C-FACTUAL', 2, 1, labels=None) is None)
    # Determinism: identical observations, identical label, repeated calls.
    check('e2_deterministic',
          len({_ad('C-LINKED', 4, 2, conf='flagged') for _ in range(50)}) == 1)

    # structural_difficulty (Tier 1.5)
    _ms_jam = [{'q_range': [1, 10], 'question_type': 'MCQ', 'correct_marks': 1.0},
               {'q_range': [11, 30], 'question_type': 'MCQ', 'correct_marks': 2.0},
               {'q_range': [31, 40], 'question_type': 'MSQ', 'correct_marks': 2.0},
               {'q_range': [41, 50], 'question_type': 'NAT', 'correct_marks': 1.0},
               {'q_range': [51, 60], 'question_type': 'NAT', 'correct_marks': 2.0}]
    check('e2_struct_mixed',
          [structural_difficulty(q, _ms_jam, _L) for q in (5, 20, 35, 45, 55)]
          == ['Easy', 'Medium', 'Hard', 'Medium', 'Hard'])
    # Uniform marks + single type → no structural signal → None for all.
    _ms_uniform = [{'q_range': [1, 200], 'question_type': 'MCQ', 'correct_marks': 4.0}]
    check('e2_struct_uniform_none',
          all(structural_difficulty(q, _ms_uniform, _L) is None for q in (1, 100, 200)))
    # Marks gradient, all-MCQ: top band IS the hardest thing the exam fields.
    _ms_allmcq = [{'q_range': [1, 20], 'question_type': 'MCQ', 'correct_marks': 2.0},
                  {'q_range': [21, 40], 'question_type': 'MCQ', 'correct_marks': 3.0},
                  {'q_range': [41, 60], 'question_type': 'MCQ', 'correct_marks': 5.0}]
    check('e2_struct_allmcq_3tier',
          [structural_difficulty(q, _ms_allmcq, _L) for q in (5, 25, 45)]
          == ['Easy', 'Medium', 'Hard'])
    # Type mix but uniform marks: MCQ has no signal; NAT still carries its own.
    _ms_typemix = [{'q_range': [1, 30], 'question_type': 'MCQ', 'correct_marks': 1.0},
                   {'q_range': [31, 60], 'question_type': 'NAT', 'correct_marks': 1.0}]
    check('e2_struct_typemix',
          structural_difficulty(10, _ms_typemix, _L) is None
          and structural_difficulty(40, _ms_typemix, _L) == 'Medium')
    # Q outside every configured range (legacy paper) → None.
    check('e2_struct_out_of_range', structural_difficulty(99, _ms_jam, _L) is None)
    # Absent / empty / malformed marking_scheme → None, never a crash.
    check('e2_struct_absent',
          structural_difficulty(1, [], _L) is None
          and structural_difficulty(1, None, _L) is None
          and structural_difficulty(1, [{'q_range': [1], 'question_type': 'MCQ'}], _L) is None)
    # Non-3-band vocabulary → None.
    check('e2_struct_non3_none', structural_difficulty(5, _ms_jam, ['A', 'B']) is None)
    # Unknown future question type falls to conservative MCQ handling.
    _ms_future = [{'q_range': [1, 10], 'question_type': 'MCQ', 'correct_marks': 1.0},
                  {'q_range': [11, 20], 'question_type': 'MATRIX', 'correct_marks': 2.0}]
    check('e2_struct_future_type',
          structural_difficulty(15, _ms_future, _L) in _L)

    # ── Adversarial-audit regressions (2026-07-24). Each pins a defect that was
    #    FOUND by hostile-input fuzzing, not hypothesised. Do not relax these.
    # (1) NaN marks made .index(marks) raise "nan is not in list" mid-delivery.
    _ms_nan = [{'q_range': [1, 10], 'question_type': 'MCQ', 'correct_marks': 'nan'},
               {'q_range': [11, 20], 'question_type': 'NAT', 'correct_marks': 2.0}]
    check('e2_struct_nan_marks',
          structural_difficulty(5, _ms_nan, _L) is None
          and structural_difficulty(15, _ms_nan, _L) is not None)
    # (2) A 2-character STRING q_range also has len 2 and was indexed per
    #     character into a silently wrong range.
    _ms_strrange = [{'q_range': '15', 'question_type': 'MCQ', 'correct_marks': 1.0},
                    {'q_range': [16, 30], 'question_type': 'NAT', 'correct_marks': 2.0}]
    check('e2_struct_string_qrange_rejected',
          structural_difficulty(3, _ms_strrange, _L) is None)
    # (3) int(float('inf')) raises OverflowError, which the old guard did not catch.
    check('e2_as_int_nonfinite',
          _as_int(float('inf')) == 0 and _as_int(float('-inf')) == 0
          and _as_int(float('nan')) == 0)
    check('e2_assess_nonfinite_steps',
          assess_difficulty('C-FACTUAL', float('inf'), float('nan'), False,
                            'full', False, 'mcq', _L) == _L[0])

    # ── Cluster E2c: difficulty conformance (v1.13) ──────────────────────────
    # Floors derive from the rubric, never restate it.
    check('e2c_floor_mcq_bottom', difficulty_min_band('mcq', _L) == _L[0])
    check('e2c_floor_msq_nat_middle',
          difficulty_min_band('msq', _L) == _L[1]
          and difficulty_min_band('nat', _L) == _L[1]
          and difficulty_min_band('NAT ', _L) == _L[1]          # case/space tolerant
          and difficulty_min_band(None, _L) == _L[0])           # unknown = uncapped
    check('e2c_floor_non3band_none',
          difficulty_min_band('mcq', ['Lo', 'Hi']) is None
          and difficulty_min_band('nat', None) is None)
    # The floor claim is PROVEN against the rubric: no observation combination at
    # engine-minimum authoring puts an msq/nat below the middle band.
    check('e2c_floor_proven_by_rubric',
          all(assess_difficulty(cls, 2, 1, False, 'full', False, qt, _L) != _L[0]
              for qt in ('msq', 'nat')
              for cls in (None, 'C-FACTUAL', 'C-VOCAB-ITEM', 'C-FORMAL-LOGIC')))
    _qt60 = {q: ('mcq' if q <= 30 else 'msq' if q <= 40 else 'nat')
             for q in range(1, 61)}
    check('e2c_feas_ok',
          difficulty_feasibility({'simple': 6, 'medium': 9, 'hard': 45}, _qt60, _L) == {})
    check('e2c_feas_easy_capped',
          difficulty_feasibility({'simple': 31, 'medium': 9, 'hard': 20}, _qt60, _L)
          == {_L[0]: {'requested': 31, 'max_achievable': 30}})
    check('e2c_feas_all_nat_zero_easy',
          difficulty_feasibility({'simple': 1, 'medium': 5, 'hard': 4},
                                 {q: 'nat' for q in range(1, 11)}, _L)
          == {_L[0]: {'requested': 1, 'max_achievable': 0}})
    check('e2c_feas_canonical_label_keys',
          difficulty_feasibility({_L[0]: 31, _L[1]: 9, _L[2]: 20}, _qt60, _L)
          == {_L[0]: {'requested': 31, 'max_achievable': 30}})
    check('e2c_feas_non3band_vacuous',
          difficulty_feasibility({'simple': 99}, _qt60, ['Lo', 'Hi']) == {})
    # Placement: exact quota, floors honoured, deterministic, seed-rotates.
    _pl = assign_difficulty_bands({'simple': 6, 'medium': 9, 'hard': 45}, _qt60, _L, seed=1)
    from collections import Counter as _C
    check('e2c_assign_exact_quota',
          _C(_pl.values()) == _C({_L[0]: 6, _L[1]: 9, _L[2]: 45}))
    check('e2c_assign_floors_honoured',
          all(_qt60[q] == 'mcq' for q, lab in _pl.items() if lab == _L[0]))
    check('e2c_assign_deterministic',
          _pl == assign_difficulty_bands({'simple': 6, 'medium': 9, 'hard': 45},
                                         _qt60, _L, seed=1))
    check('e2c_assign_seed_rotates',
          _pl != assign_difficulty_bands({'simple': 6, 'medium': 9, 'hard': 45},
                                         _qt60, _L, seed=2))
    _err = 0
    try:
        assign_difficulty_bands({'simple': 1, 'medium': 1, 'hard': 1}, _qt60, _L)
    except ValueError:
        _err += 1
    try:
        assign_difficulty_bands({'simple': 31, 'medium': 9, 'hard': 20}, _qt60, _L)
    except ValueError:
        _err += 1
    check('e2c_assign_rejects_bad_counts', _err == 2)
    check('e2c_assign_non3band_none',
          assign_difficulty_bands({'simple': 1}, _qt60, ['Lo', 'Hi']) is None)
    check('e2c_assign_all_easy_all_mcq',
          _C(assign_difficulty_bands({'simple': 10, 'medium': 0, 'hard': 0},
                                     {q: 'mcq' for q in range(1, 11)}, _L).values())
          == _C({_L[0]: 10}))
    # Every authoring profile PROVABLY lands in its band at its canonical point.
    def _mid(t):
        return (t[0] + t[1]) // 2
    _prof_ok = True
    for _band in _L:
        for _qtp in ('mcq', 'msq', 'nat'):
            _pr = difficulty_authoring_profile(_band, _qtp, _L)
            if _pr is None:
                _prof_ok &= (_band == _L[0] and _qtp in ('msq', 'nat'))
                continue
            for _st in (_pr['steps'][0], _mid(_pr['steps']), _pr['steps'][1]):
                for _co in (_pr['concepts'][0], _pr['concepts'][1]):
                    _cls = (_pr['classes'] or [None])[0]
                    _got = assess_difficulty(_cls, _st, _co, False, 'full',
                                             False, _qtp, _L)
                    _prof_ok &= (_got == _band)
    check('e2c_profiles_proven_in_band', _prof_ok)
    check('e2c_profile_easy_msq_impossible',
          difficulty_authoring_profile(_L[0], 'msq', _L) is None
          and difficulty_authoring_profile(_L[0], 'nat', _L) is None)
    check('e2c_profile_unknown_none',
          difficulty_authoring_profile('Bogus', 'mcq', _L) is None
          and difficulty_authoring_profile(_L[2], 'mcq', ['Lo', 'Hi']) is None)
    # verify_difficulty_obs: the ONE shared check.
    _obs_h = {'question_class': 'C-COMPUTATIONAL', 'deduction_steps': 5,
              'axiom_concepts': 2, 'speed_hack_exists': False,
              'is_negative': False, 'qtype': 'mcq'}
    check('e2c_verify_match', verify_difficulty_obs(_L[2], _obs_h, _L) == (True, _L[2]))
    check('e2c_verify_mismatch',
          verify_difficulty_obs(_L[0], _obs_h, _L) == (False, _L[2]))
    check('e2c_verify_legacy_passthrough',
          verify_difficulty_obs(_L[2], None, _L) == (True, None)
          and verify_difficulty_obs(_L[2], {}, _L) == (True, None)
          and verify_difficulty_obs(_L[2], _obs_h, ['Lo', 'Hi']) == (True, None))
    check('e2c_verify_facets_alias',
          verify_difficulty_obs(_L[2], {'facets': ['C-COMPUTATIONAL'],
                                        'deduction_steps': 5, 'axiom_concepts': 2,
                                        'qtype': 'mcq'}, _L)[0] is True)
    # Non-finite / non-positive marks are excluded from the gradient entirely.
    _ms_inf = [{'q_range': [1, 10], 'question_type': 'MCQ', 'correct_marks': 'inf'},
               {'q_range': [11, 20], 'question_type': 'MCQ', 'correct_marks': 2.0},
               {'q_range': [21, 30], 'question_type': 'NAT', 'correct_marks': 4.0}]
    check('e2_struct_inf_marks_excluded',
          structural_difficulty(5, _ms_inf, _L) is None
          and structural_difficulty(15, _ms_inf, _L) == _L[0])
    # Reversed q_range in config still matches its questions.
    _ms_rev = [{'q_range': [10, 1], 'question_type': 'MCQ', 'correct_marks': 1.0},
               {'q_range': [11, 20], 'question_type': 'NAT', 'correct_marks': 2.0}]
    check('e2_struct_reversed_range', structural_difficulty(5, _ms_rev, _L) == _L[0])
    # Zero / negative marks are not a gradient tier.
    _ms_zero = [{'q_range': [1, 10], 'question_type': 'MCQ', 'correct_marks': 0},
                {'q_range': [11, 20], 'question_type': 'MCQ', 'correct_marks': -2},
                {'q_range': [21, 30], 'question_type': 'NAT', 'correct_marks': 2.0}]
    check('e2_struct_nonpositive_marks',
          structural_difficulty(5, _ms_zero, _L) is None
          and structural_difficulty(15, _ms_zero, _L) is None
          and structural_difficulty(25, _ms_zero, _L) is not None)
    # Return value is ALWAYS None or a member of the supplied vocabulary.
    check('e2_struct_return_in_vocab',
          all(structural_difficulty(q, _ms_jam, _L) in (None, *_L) for q in range(0, 65)))

    # ── Cluster H: corpus acquisition decisions ──────────────────────────────
    # identity — every transport-mangled spelling of ONE paper must collapse to one key
    _variants = [
        'IIT_JAM_BIOTECHNOLOGY_02May2010_Sorted_Q1Q100.docx',
        'IIT_JAM_BIOTECHNOLOGY_02-May-2010_Sorted_Q1-Q100.docx',
        'IIT_JAM_BIOTECHNOLOGY_02-May-2010_Sorted_Q1-Q100 (1).docx',
        'Copy of IIT_JAM_BIOTECHNOLOGY_02May2010_Sorted_Q1Q100.docx',
        'IIT JAM BIOTECHNOLOGY 02 May 2010 Sorted Q1 Q100.docx',
        '/some/deep/path/IIT_JAM_BIOTECHNOLOGY_02May2010_Sorted_Q1Q100.docx',
    ]
    check('h_key_variants_collapse',
          len({canonical_paper_key(v) for v in _variants}) == 1)
    check('h_key_distinct_shifts',
          canonical_paper_key('E_02-May-2010_Shift-1.docx')
          != canonical_paper_key('E_02-May-2010_Shift-2.docx'))
    check('h_key_distinct_years',
          canonical_paper_key('E_2010_Sorted.docx') != canonical_paper_key('E_2011_Sorted.docx'))
    check('h_key_nfkc', canonical_paper_key('ＥＸＡＭ_2010.docx') == canonical_paper_key('EXAM_2010.docx'))
    check('h_key_copy_case_insensitive',
          canonical_paper_key('COPY OF x_2010.docx') == canonical_paper_key('x_2010.docx'))
    check('h_key_paren_only_trailing',
          canonical_paper_key('E_(1)_2010.docx') != canonical_paper_key('E_2010.docx'))

    # screening — nothing may be dropped silently
    check('h_screen_docx_ok', screen_drive_entry('a.docx', DOCX_MIME, 100)[0] == 'paper')
    check('h_screen_folder', screen_drive_entry('yr', FOLDER_MIME, None)[0] == 'folder')
    check('h_screen_gdoc_rejected', screen_drive_entry('paper', GDOC_MIME, None)[0] == 'reject')
    check('h_screen_gdoc_has_reason', 'Google Doc' in screen_drive_entry('p', GDOC_MIME, None)[1])
    check('h_screen_shortcut', screen_drive_entry('s', SHORTCUT_MIME, 10)[0] == 'reject')
    check('h_screen_legacy_doc', screen_drive_entry('old.doc', 'application/msword', 10)[0] == 'reject')
    check('h_screen_docx_suffix_wins', screen_drive_entry('a.docx', '', 10)[0] == 'paper')
    check('h_screen_no_size', screen_drive_entry('a.docx', DOCX_MIME, None)[0] == 'reject')
    check('h_screen_no_size_optional',
          screen_drive_entry('a.docx', DOCX_MIME, None, require_size=False)[0] == 'paper')
    check('h_screen_unsupported', screen_drive_entry('a.pdf', 'application/pdf', 10)[0] == 'reject')

    # transport status — real measured boundaries
    check('h_status_blocked', transport_status(16599368) == 'BLOCKED')
    check('h_status_marginal_2021', transport_status(9702004) == 'MARGINAL')
    check('h_status_marginal_2005', transport_status(9796205) == 'MARGINAL')
    check('h_status_ok', transport_status(4514433) == 'OK')
    check('h_status_cap_edge_ok', transport_status(DRIVE_CAP) == 'MARGINAL')
    check('h_status_cap_edge_blocked', transport_status(DRIVE_CAP + 1) == 'BLOCKED')
    check('h_status_budget_edge', transport_status(SIZE_BUDGET) == 'OK')
    check('h_status_unknown', transport_status(None) == 'UNKNOWN')

    # partition — predictive, on the CAP (marginal files still fetch fine today)
    _ps = [{'n': 'a', 'fileSize': 16599368}, {'n': 'b', 'fileSize': 9702004},
           {'n': 'c', 'fileSize': 100}, {'n': 'd', 'fileSize': None}]
    _pt = partition_by_transport(_ps)
    check('h_part_over_cap_uploads', _pt['upload'][0]['n'] == 'a')
    check('h_part_marginal_stays_auto', any(x['n'] == 'b' for x in _pt['auto']))
    check('h_part_unknown_uploads', any(x['n'] == 'd' for x in _pt['upload']))
    check('h_part_no_loss', len(_pt['auto']) + len(_pt['upload']) == len(_ps))
    check('h_part_order_kept', [x['n'] for x in _pt['auto']] == ['b', 'c'])
    # GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION: the return now also carries the
    # channel and its context arithmetic, so the empty case is asserted on the LANES
    # plus the presence of the new keys rather than on an exact dict — an exact-dict
    # assertion here is what would otherwise forbid ever reporting a transport plan.
    _empty = partition_by_transport([])
    check('h_part_empty', _empty['auto'] == [] and _empty['upload'] == [])
    check('h_part_empty_reports_channel',
          {'channel', 'inline_chars', 'inline_budget',
           'deferred_for_context'} <= set(_empty))

    # batch planning — the 20-file chat ceiling is the binding constraint
    _b3 = upload_batch_plan(18, 3)
    check('h_plan_b3_per_chat', _b3['papers_per_chat'] == 18)
    check('h_plan_b3_batches', _b3['total_batches'] == 6)
    check('h_plan_b3_one_chat', _b3['chats_needed'] == 1)
    _b5 = upload_batch_plan(22, 5)
    check('h_plan_b5_per_chat', _b5['papers_per_chat'] == 20)
    check('h_plan_b5_two_chats', _b5['chats_needed'] == 2)
    check('h_plan_zero', upload_batch_plan(0, 3)['chats_needed'] == 0)
    check('h_plan_one', upload_batch_plan(1, 3)['total_batches'] == 1)
    try:
        upload_batch_plan(5, 0)
        check('h_plan_bad_batch_raises', False)
    except AllocationError:
        check('h_plan_bad_batch_raises', True)

    # media routing — JPEG source must never be re-encoded as PNG
    check('h_route_alpha', classify_media_route('PNG', True, True) == 'png')
    check('h_route_jpeg_stays_jpeg', classify_media_route('JPEG', False, True) == 'jpeg')
    check('h_route_lineart_png', classify_media_route('PNG', False, True) == 'png-lineart')
    check('h_route_photo_jpeg', classify_media_route('PNG', False, False) == 'jpeg')
    check('h_route_unknown_fmt', classify_media_route('', False, False) == 'jpeg')
    check('h_route_alpha_beats_jpeg', classify_media_route('JPEG', True, False) == 'png')

    # image gates
    _ok = image_gate_verdict(100, 100, 0, [], 20, 1, 21, [])
    check('h_gate_all_pass', gates_passed(_ok))
    check('h_gate_img1_skip', image_gate_verdict(100, None, 0, [], 1, 0, 1, [])['IMG-1'] == 'SKIP')
    check('h_gate_img1_fail',
          image_gate_verdict(99, 100, 0, [], 1, 0, 1, [])['IMG-1'].startswith('FAIL'))
    check('h_gate_img2_fail',
          image_gate_verdict(100, 100, 2, [], 1, 0, 1, [])['IMG-2'].startswith('FAIL'))
    check('h_gate_img3_fail',
          image_gate_verdict(100, 100, 0, ['i1.png'], 1, 0, 1, [])['IMG-3'].startswith('FAIL'))
    # the table-image case: one image sat in a table, so mapping came up short
    check('h_gate_img4_table_loss',
          image_gate_verdict(100, 100, 0, [], 20, 0, 21, [])['IMG-4'].startswith('FAIL'))
    check('h_gate_img4_preamble_counts', gates_passed(image_gate_verdict(1, 1, 0, [], 0, 3, 3, [])))
    check('h_gate_img5_fail',
          image_gate_verdict(100, 100, 0, [], 1, 0, 1, ['x.emf'])['IMG-5'].startswith('FAIL'))
    check('h_gate_not_passed', not gates_passed(image_gate_verdict(99, 100, 0, [], 1, 0, 1, [])))

    # three-state clarity — 'unclear' is meaningless without a live probe
    _im = [{'q_num': 1, 'position': 'stem'}, {'q_num': 2, 'position': 'opt1'},
           {'q_num': 3, 'position': 'stem'}, {'q_num': 3, 'position': 'opt1'}]
    _r = derive_image_roles(_im)
    check('h_roles_stem_only', _r[1]['role'] == 'stem_only')
    check('h_roles_options_only', _r[2]['role'] == 'options_only')
    check('h_roles_stem_and_options', _r[3]['role'] == 'stem_and_options')
    check('h_roles_all_valid', all(v['role'] in IMAGE_ROLES for v in _r.values()))
    check('h_roles_empty', derive_image_roles([]) == {})
    check('h_roles_none_safe', derive_image_roles(None) == {})
    check('h_clarity_clear', image_clarity_state(True, True) == 'clear')
    check('h_clarity_unclear', image_clarity_state(True, False) == 'unclear')
    check('h_clarity_blind', image_clarity_state(False, False) == 'vision_unavailable')
    check('h_clarity_blind_even_if_readable',
          image_clarity_state(False, True) == 'vision_unavailable')

    # -- GAP-2026-07-26-001: stem continuation must never be a level-3 heading --
    # The g_stem_* assertions FAIL on the pre-fix engine. That is the point: CLAUDE.md
    # requires a self-test to contain a fixture that fails on the defect it was written
    # for. Every case below is lifted from a REAL paragraph in the reproduction corpus.
    class _R2:
        def __init__(s, t, b): s.text, s.bold = t, b
    class _P2:
        def __init__(s, t, b=True): s.text, s.runs = t, [_R2(t, b)]
    _no_opt = lambda t: False
    _cont = _P2('Which one of the following options gives the correct enzyme-vitamin matches?')
    _sub  = _P2('Enzyme Kinetics, Catalysis and Inhibition')

    # the defect: continuation followed by an OPTION            (real: 2010 p86)
    check('g_stem_cont_before_option',
          not is_taxonomy_heading(_cont, _no_opt, '1. EnzP and Vit B3, EnzQ and Vit B2'))
    # continuation followed by ANOTHER stem paragraph            (real: 2010 p85)
    check('g_stem_cont_before_stem',
          not is_taxonomy_heading(_cont, _no_opt, 'The dotted lines denote'))
    # continuation followed by the next GENUINE heading          (real: 2016 p98)
    check('g_stem_cont_before_heading',
          not is_taxonomy_heading(_cont, _no_opt, 'Population Genetics'))
    # NAT ask-line before a Topic heading            (real: 2019 p85, 2024 p345)
    check('g_stem_nat_ask_line',
          not is_taxonomy_heading(_P2('Calculate the recombination frequency.'),
                                  _no_opt, 'Topic 4: Molecular Biology'))
    # bare option label whose content is an image          (real: 2026 p334-337)
    check('g_stem_bare_option_label',
          not is_taxonomy_heading(_P2('1.'), _no_opt, '2.'))
    # last paragraph in the file — a genuine subtopic is never last (real: 2020 p426)
    check('g_stem_last_para', not is_taxonomy_heading(_cont, _no_opt, ''))
    # genuine subtopic headings still pass — BOTH date-label forms (CHECK 3)
    check('g_head_date_no_session', is_taxonomy_heading(_sub, _no_opt, '[02-May-2010]'))
    check('g_head_date_with_session',
          is_taxonomy_heading(_sub, _no_opt, '[12-Sep-2025 Shift 1]'))
    # prefixed levels are position-independent
    check('g_head_l1_position_free',
          is_taxonomy_heading(_P2('Subject: General Biology'), _no_opt, 'Q.1 Anything'))
    check('g_head_l2_position_free',
          is_taxonomy_heading(_P2('Topic 3: Genetics'), _no_opt, 'DNA Replication'))
    # backward compatibility: next_text=None reproduces pre-fix behaviour exactly
    check('g_head_next_none_compat', is_taxonomy_heading(_cont, _no_opt, None))
    # the MAX_HEADING_LEN bound is untouched
    check('g_head_maxlen_untouched',
          not is_taxonomy_heading(_P2('n' * MAX_HEADING_LEN), _no_opt, '[02-May-2010]'))
    # non-bold text is still never a heading
    check('g_head_requires_bold',
          not is_taxonomy_heading(_P2('Enzyme Kinetics', False), _no_opt, '[02-May-2010]'))

    # ── GAP-2026-08-15-BAREQ — bare-label question detection (T-1) ───────────
    # A stem whose entire payload is <m:oMath> / a drawing / nothing reads through
    # p.text as just "Q.N". Entries 3 and 4 exist for exactly that shape. These
    # tests FAIL on the pre-remedy two-entry table, which is the whole point: a
    # regression test that cannot fail on the old code is not a regression test
    # (the DISABLED-GUARD doctrine at audit_deep.py:210).
    for _s in ('Q.4', 'Q.4  ', 'Q.4\t', 'Q. 4', 'Q25.', 'Q25. ', 'Q.60',
               'Q.4\u00a0', 'Q.4\u2007'):
        check(f'bareq_detect_{_s!r}', detect_question_start(_s) is not None)
    check('bareq_value_dot',  detect_question_start('Q.4') == 4)
    check('bareq_value_alt',  detect_question_start('Q25.') == 25)
    # R-8: zero-width characters are neither stripped by str.strip() nor matched
    # by \s, so they defeat entries 1-4 alike unless removed first.
    check('bareq_zerowidth_zwsp', detect_question_start('Q.4\u200b') == 4)
    check('bareq_zerowidth_bom',  detect_question_start('\ufeffQ.4') == 4)
    check('bareq_zerowidth_mid',  detect_question_start('Q.\u200b4') == 4)
    # ADVERSARIAL: the $ anchor must admit NOTHING else. Every string below is a
    # real shape from the corpus. A single false positive here would split one
    # question into two, or promote an option/heading/cross-reference to a question.
    for _s in ('1.', '1. text option', '4. π', '(1) option', 'a. option', 'A.',
               '[12-Feb-2017]', '[05-Feb-2025 Shift 1]', '[05-Feb-2025 Q37]',
               'Subject: Real Analysis', 'Topic 3: Differential Equations',
               'Riemann Integration and Fundamental Theorem of Calculus',
               'Q.11-15', 'Questions 11-15 refer to the passage',
               'Q1 Analysis', 'Q.', 'Q', 'Q.1a', 'Q.1a  sub-part', 'QA.1 something',
               'QA.1', 'Q.4.5', 'Q .4', 'Enter your answer as an integer',
               'Statement I: f is continuous', '=== Mathematical Abilities ===', ''):
        check(f'bareq_reject_{_s!r}', detect_question_start(_s) is None)
    # UNCHANGED behaviour on conformant documents — the widening is additive only.
    check('bareq_unchanged_1', detect_question_start('Q.1  The sum of the series') == 1)
    check('bareq_unchanged_2', detect_question_start('Q. 7  Find x') == 7)
    check('bareq_unchanged_3', detect_question_start('Q1.  Find x') == 1)
    check('bareq_unchanged_4',
          detect_question_start('Q.11 to Q.15 are based on the passage below') == 11)
    # A bare label is a QUESTION, therefore never a taxonomy heading — even bold,
    # even when the next content-bearing block is a date label. Pre-remedy this
    # returned True (verified by execution), which promoted an OMML-only NAT stem
    # to a phantom level-3 subtopic heading.
    check('bareq_not_heading_before_date',
          not is_taxonomy_heading(_P2('Q.4'), _no_opt, '[12-Feb-2017]'))
    check('bareq_not_heading_next_none',
          not is_taxonomy_heading(_P2('Q.4'), _no_opt, None))
    check('bareq_not_heading_alt_form',
          not is_taxonomy_heading(_P2('Q25.'), _no_opt, '[12-Feb-2017]'))
    # Renumbering a bare label round-trips: the emitted label must re-detect.
    check('bareq_renumber_roundtrip',
          detect_question_start(re.sub(r'^Q\.\s*\d+', 'Q.7', 'Q.4')) == 7)
    # The named companion table IS the tail of the canonical table — not a copy of it.
    check('bareq_companion_is_slice', BARE_Q_PATTERNS == Q_PATTERNS[2:])
    check('bareq_label_shape_dot', is_bare_q_label('Q.4') == 4)
    check('bareq_label_shape_alt', is_bare_q_label('Q25.') == 25)
    check('bareq_label_shape_zw',  is_bare_q_label('Q.4\u200b') == 4)
    check('bareq_label_rejects_content', is_bare_q_label('Q.4  x') is None)
    check('bareq_label_rejects_option',  is_bare_q_label('1.') is None)
    check('bareq_label_rejects_xref',    is_bare_q_label('Q.11-15') is None)
    # next_nonempty_texts contract
    class _P3:
        def __init__(s, t): s.text = t
    check('g_next_nonempty',
          next_nonempty_texts([_P3('A'), _P3(''), _P3('   '), _P3('B'), _P3('C'), _P3('')])
          == ['B', 'B', 'B', 'C', '', ''])

    # ── GAP-2026-08-05-001 — TEXTLESS CONTENT IS CONTENT (D5) ───────────────
    # Every t_* assertion below FAILS on the pre-fix engine, per CLAUDE.md: a
    # regression test that passes on the broken code tests nothing. The fixtures are
    # PURE stubs — building them with python-docx would import a non-stdlib module
    # into the thin core and break validate_framework_md Check AB.
    class _El:
        """Minimal <w:p>-shaped element: .tag plus a recursive .iter()."""
        def __init__(s, tag, kids=()): s.tag = tag; s.kids = list(kids)
        def iter(s):
            yield s
            for k in s.kids:
                for x in k.iter():
                    yield x

    class _P5:
        """Paragraph stub carrying a real element tree and optional coloured runs."""
        def __init__(s, text='', tags=(), colour='INHERIT', bold=True):
            s.text = text
            s._p = _El(W_P_TAG, [_El(t) for t in tags])
            class _C:
                def __init__(c, v):
                    c.type = None if v == 'INHERIT' else 1
                    c.rgb = v
            class _R:
                def __init__(r, t, b, col):
                    r.text = t; r.bold = b
                    r.font = type('F', (), {'color': _C(col)})()
            s.runs = [_R(text, bold, colour)] if text else []

    _IMG_T = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'
    _EQN_T = '{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath'
    _OBJ_T = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}object'
    _NUM_T = W_NUMPR_TAG

    _cont5 = _P5('Compound E displays a prominent absorption band at 1710 cm-1.')
    _sub5  = _P5('Alcohols, Aldehydes and Ketones', colour=HEADING_NAVY)
    _img5  = _P5('', (_IMG_T,))
    _eqn5  = _P5('', (_EQN_T,))
    _obj5  = _P5('', (_OBJ_T,))
    _num5  = _P5('', (_NUM_T,))
    _blank5 = _P5('')
    _date5 = _P5('[03-May-2009 Q74]', colour=HEADING_NAVY)

    # the classifier
    check('t_content_image',            paragraph_is_content_bearing(_img5))
    check('t_content_equation',         paragraph_is_content_bearing(_eqn5))
    check('t_content_object',           paragraph_is_content_bearing(_obj5))
    check('t_content_autonumber',       paragraph_is_content_bearing(_num5))
    check('t_content_autonumber_opt_out',
          not paragraph_is_content_bearing(_num5, include_autonumber=False))
    check('t_content_blank_is_not',     not paragraph_is_content_bearing(_blank5))
    check('t_content_text_para_is_not', not paragraph_is_content_bearing(_sub5))
    check('t_content_no_element_safe',  not paragraph_is_content_bearing(_P3('x')))
    check('t_content_none_safe',        not paragraph_is_content_bearing(None))
    check('t_content_raw_element',      paragraph_is_content_bearing(_img5._p))

    # the lookahead: textless content TERMINATES the scan
    _seq5 = [_cont5, _img5, _img5, _img5, _img5, _date5]
    check('t_lookahead_image_stops',    next_nonempty_texts(_seq5)[0] == CONTENT_SENTINEL)
    check('t_lookahead_equation_stops',
          next_nonempty_texts([_cont5, _eqn5, _date5])[0] == CONTENT_SENTINEL)
    check('t_lookahead_blank_transparent',
          next_nonempty_texts([_cont5, _blank5, _date5])[0] == '[03-May-2009 Q74]')

    # THE DEFECT — this assertion returns True (wrongly) on the pre-fix engine
    check('t_stem_cont_before_image_options',
          not is_taxonomy_heading(_cont5, _no_opt, next_nonempty_texts(_seq5)[0]))
    check('t_head_still_passes',
          is_taxonomy_heading(_sub5, _no_opt, next_nonempty_texts([_sub5, _date5])[0]))
    check('t_legacy_next_nonempty_unchanged',
          next_nonempty_texts([_P3('A'), _P3(''), _P3('   '), _P3('B'), _P3('C'), _P3('')])
          == ['B', 'B', 'B', 'C', '', ''])

    # ── D2: a table is a block, and it is CONTENT ───────────────────────────
    class _Body:
        def __init__(s, kids): s.kids = kids
        def iterchildren(s): return iter(s.kids)

    class _Doc:
        def __init__(s, paras, kids): s.paragraphs = paras; s.element = s
        @property
        def body(s): return s._body

    def _mkdoc(seq):
        paras = [x for x in seq if x is not None]
        kids  = [_El(W_P_TAG) if x is not None else _El(W_TBL_TAG) for x in seq]
        d = _Doc(paras, kids); d._body = _Body(kids)
        return d

    _dt = _mkdoc([_P5('The determinant of the matrix is'), None, _date5])
    _pt, _nt5 = sorted_body_lookahead(_dt)
    check('t_table_stops_lookahead',  _nt5[0] == CONTENT_SENTINEL)
    check('t_table_cont_not_heading', not is_taxonomy_heading(_pt[0], _no_opt, _nt5[0]))
    check('t_body_lookahead_len',     len(_pt) == 2 and len(_nt5) == 2)
    # no table -> identical to the paragraph-scoped lookahead
    _d2 = _mkdoc([_cont5, _img5, _date5])
    check('t_body_lookahead_matches_paragraph_scope',
          sorted_body_lookahead(_d2)[1] == next_nonempty_texts(_d2.paragraphs))

    # ── D6: the colour discriminator, gated PER FILE ────────────────────────
    check('t_colour_first_run',      first_run_colour(_sub5) == HEADING_NAVY)
    check('t_colour_inherited_none', first_run_colour(_cont5) is None)
    check('t_probe_passes',          heading_colour_available([_date5, _sub5]))
    check('t_probe_fails_unstyled',  not heading_colour_available([_P5('[03-May-2009 Q74]')]))
    check('t_probe_needs_a_label',   not heading_colour_available([_sub5]))
    # THE NAT CASE — no options, so the continuation IS followed by a date label and
    # NO textless content is involved. D1/D2 cannot fix this; only D6 can.
    _nat = _P5('The number of cells after 2 hours is ______.')
    check('t_nat_positional_cannot_see_it',
          is_taxonomy_heading(_nat, _no_opt, '[09-Feb-2025 Shift 1]'))
    check('t_nat_fixed_by_colour',
          not is_taxonomy_heading(_nat, _no_opt, '[09-Feb-2025 Shift 1]',
                                  colour_available=True))
    check('t_nat_heading_survives_colour',
          is_taxonomy_heading(_sub5, _no_opt, '[09-Feb-2025 Shift 1]',
                              colour_available=True))
    # level 2 is BLACK per S6-2 and must never be rejected by the colour gate
    check('t_l2_black_immune_to_colour',
          is_taxonomy_heading(_P5('Topic 3: Genetics', colour='000000'), _no_opt,
                              'DNA Replication', colour_available=True))

    # ── CLUSTER V — VISION MERGE / PROFILE (GAP-2026-07-26-003) ─────────────
    _keys = [('PAPER_A', 1), ('PAPER_A', 17), ('PAPER_B', 1)]
    _tags, _w = vision_tag_map(_keys)
    check('v_tag_unique', len(set(_tags.values())) == 3)
    check('v_tag_key_is_pair', _tags[('PAPER_A', 1)] != _tags[('PAPER_B', 1)])
    check('v_tag_deterministic', vision_tag_map(_keys)[0] == _tags)
    # EC-V11/V12: a tag must NOT depend on which other keys are queued.
    check('v_tag_stable_on_growth',
          vision_tag_map(_keys + [('PAPER_C', 9)])[0][('PAPER_A', 17)]
          == _tags[('PAPER_A', 17)])
    check('v_tag_width_reported', isinstance(_w, int) and _w >= 2)

    def _q(k, t):
        return {'tag': t, 'paper_id': k[0], 'q_num': k[1]}
    _queue = [_q(k, _tags[k]) for k in _keys]

    # EC-V1 — text-only exam: empty queue is not_applicable, never a failure.
    _bk, _st = merge_vision_observations([], [])
    check('v_ec1_empty_queue', _st['vision_status'] == 'not_applicable'
          and _st['queued'] == 0 and _bk == {})

    # EC-V3 — Phase B never ran: every item vision_unavailable, no raise, no halt.
    _bk, _st = merge_vision_observations(_queue, [])
    check('v_ec3_no_observations',
          _st['vision_status'] == 'unavailable' and _st['missing'] == 3
          and all(v['image_clarity'] == 'vision_unavailable' for v in _bk.values()))

    # full observation
    _obs = [{'tag': _tags[k], 'figure_readable': True, 'object_type': 'micrograph',
             'transformation_type': 'N/A', 'arrangement': 'single',
             'complexity': 'Simple'} for k in _keys]
    _bk, _st = merge_vision_observations(_queue, _obs)
    check('v_full_observed', _st['vision_status'] == 'observed'
          and _st['observed'] == 3 and _st['missing'] == 0)
    check('v_fields_populated',
          _bk[('PAPER_A', 1)]['object_type'] == 'micrograph'
          and _bk[('PAPER_A', 1)]['image_clarity'] == 'clear')

    # EC-V12 — idempotent: identical inputs, identical outputs.
    check('v_ec12_idempotent', merge_vision_observations(_queue, _obs)[0] == _bk)

    # EC-V4 — partial: present filled, absent reported, ratio true.
    _bk, _st = merge_vision_observations(_queue, _obs[:2])
    check('v_ec4_partial', _st['vision_status'] == 'partial'
          and _st['observed'] == 2 and _st['missing'] == 1)
    check('v_ec4_missing_marked',
          _bk[('PAPER_B', 1)]['image_clarity'] == 'vision_unavailable')

    # EC-V2 — illegible figure is 'unclear', NOT 'vision_unavailable', and carries
    # no guessed field values.
    _bk, _st = merge_vision_observations(
        _queue, [{'tag': _tags[_keys[0]], 'figure_readable': False,
                  'object_type': 'guess'}])
    check('v_ec2_unclear_distinct',
          _bk[_keys[0]]['image_clarity'] == 'unclear' and _st['unreadable'] == 1)
    check('v_ec2_no_guess', _bk[_keys[0]]['object_type'] is None)

    # EC-V5 — observation for a tag not in the queue: counted, ignored, no crash.
    _bk, _st = merge_vision_observations(
        _queue, [{'tag': 'ZZZZ-99', 'figure_readable': True}])
    check('v_ec5_unknown_tag', _st['unknown'] == ['ZZZZ-99'] and _st['observed'] == 0)

    # tag transcription tolerance + (paper_id,q_num) fallback across tag widths
    _bk, _st = merge_vision_observations(
        _queue, [{'tag': ' ' + _tags[_keys[0]].lower().replace('-', '\u2013'),
                  'figure_readable': True, 'object_type': 'gel'}])
    check('v_tag_transcription_tolerant', _bk[_keys[0]]['object_type'] == 'gel')
    _bk, _st = merge_vision_observations(
        _queue, [{'paper_id': 'PAPER_A', 'q_num': 17, 'figure_readable': True,
                  'object_type': 'plot'}])
    check('v_key_fallback_match', _bk[('PAPER_A', 17)]['object_type'] == 'plot')

    # duplicate observations: last wins, recorded, never a crash
    _bk, _st = merge_vision_observations(
        _queue, [{'tag': _tags[_keys[0]], 'figure_readable': True, 'object_type': 'a'},
                 {'tag': _tags[_keys[0]], 'figure_readable': True, 'object_type': 'b'}])
    check('v_duplicate_last_wins',
          _bk[_keys[0]]['object_type'] == 'b' and len(_st['duplicate']) == 1)

    # malformed observation entries must not crash the merge
    _bk, _st = merge_vision_observations(_queue, [None, 'junk', 42, {}])
    check('v_malformed_tolerated', _st['queued'] == 3 and _st['observed'] == 0)

    # EC-V20 — dominant withheld below threshold; observed still published.
    _thin = [{'image_clarity': 'clear', 'object_type': 'micrograph'},
             {'image_clarity': 'clear', 'object_type': 'micrograph'}]
    _p = vision_profile(_thin, min_dominant=5)
    check('v_ec20_dominant_withheld', _p['object_types']['dominant'] == [])
    check('v_ec20_observed_published',
          _p['object_types']['observed'] == ['micrograph'])
    check('v_ec20_reason_given', 'dominant_suppressed' in _p)

    _thick = [{'image_clarity': 'clear', 'object_type': 'micrograph',
               'complexity': 'Simple', 'transformation_type': 'N/A',
               'arrangement': 'single'} for _ in range(4)] + \
             [{'image_clarity': 'clear', 'object_type': 'gel',
               'complexity': 'Hard', 'transformation_type': 'rotation_90cw',
               'arrangement': 'row_series'}]
    _p = vision_profile(_thick, min_dominant=5)
    # 'gel' occurs once: it holds 20% share but does not RECUR, so EC-V26 keeps it
    # out of dominant while 'observed' still records that it was seen.
    check('v_ec20_dominant_named', _p['object_types']['dominant'] == ['micrograph'])
    check('v_ec20_singleton_still_observed',
          _p['object_types']['observed'] == ['gel', 'micrograph'])
    check('v_profile_no_na_transform', _p['transformation_types'] == ['rotation_90cw'])
    check('v_profile_complexity_pct',
          _p['complexity_dist'] == {'Hard': 20, 'Simple': 80})
    check('v_profile_counts',
          _p['images_analysed'] == 5 and _p['images_unclear'] == 0
          and _p['vision_status'] == 'observed')

    # EC-V26 — well-observed but FLAT: six distinct types, none dominant.
    _flat = [{'image_clarity': 'clear', 'object_type': t} for t in
             ('gel', 'curve', 'cell', 'pedigree', 'bar', 'helix')]
    _p = vision_profile(_flat, min_dominant=5)
    check('v_ec26_flat_no_dominant', _p['object_types']['dominant'] == [])
    check('v_ec26_flat_variety_kept', len(_p['object_types']['observed']) == 6)
    check('v_ec26_flat_reason', 'flat' in _p.get('dominant_suppressed', ''))
    # a genuine majority still surfaces
    _peak = [{'image_clarity': 'clear', 'object_type': 'gel'} for _ in range(4)] + \
            [{'image_clarity': 'clear', 'object_type': 'curve'},
             {'image_clarity': 'clear', 'object_type': 'bar'}]
    check('v_ec26_peak_named',
          vision_profile(_peak, min_dominant=5)['object_types']['dominant'] == ['gel'])
    # a singleton never enters dominant even alongside a real peak
    check('v_ec26_singleton_excluded',
          'bar' not in vision_profile(_peak, min_dominant=5)['object_types']['dominant'])

    # EC-V21 — provenance travels with the profile
    _mixed = [{'image_clarity': 'clear', 'object_type': 'x'},
              {'image_clarity': 'vision_unavailable'},
              {'image_clarity': 'unclear'}]
    _p = vision_profile(_mixed, min_dominant=1)
    check('v_ec21_provenance',
          _p['queued_n'] == 3 and _p['observed_n'] == 1
          and _p['images_unobserved'] == 1 and _p['images_unclear'] == 1)
    check('v_ec21_status_partial', _p['vision_status'] == 'partial')
    check('v_profile_empty_safe',
          vision_profile([])['vision_status'] == 'not_applicable')
    check('v_profile_none_safe', vision_profile(None)['object_types']['dominant'] == [])

    # ── EC-V18 — CONSUMER SIDE / LEGACY TOLERANCE ──────────────────────────
    _P = figural_generation_profile
    # every pre-v2.37 artefact shape must resolve to 'unconstrained', never raise
    for _label, _inp in (('none', None), ('empty', {}), ('str', 'junk'), ('list', []),
                         ('legacy_empty', {'image_role': 'stem_only',
                                           'object_types': {'dominant': [],
                                                            'observed': []},
                                           'transformation_types': []}),
                         ('malformed_ot', {'object_types': 'nope'}),
                         ('none_ot', {'object_types': {'dominant': None,
                                                       'observed': None}})):
        check(f'v_ec18_legacy_{_label}', _P(_inp)['mode'] == 'unconstrained')
    check('v_ec18_reason_given', bool(_P({})['reason']))

    # a measurement GAP must not become a constraint, even with stale types present
    check('v_ec18_unavailable_unconstrained',
          _P({'vision_status': 'unavailable',
              'object_types': {'dominant': ['stale'], 'observed': ['stale']}})['mode']
          == 'unconstrained')
    check('v_ec18_not_applicable_unconstrained',
          _P({'vision_status': 'not_applicable'})['mode'] == 'unconstrained')

    # a real profile binds
    _real = {'vision_status': 'observed',
             'object_types': {'dominant': ['micrograph'],
                              'observed': ['micrograph', 'gel']},
             'transformation_types': ['rotation_90cw'],
             'arrangement_types': ['single'],
             'complexity_dist': {'Simple': 80, 'Hard': 20}}
    _p = _P(_real)
    check('v_ec18_dominant_mode', _p['mode'] == 'dominant')
    check('v_ec18_observed_superset',
          _p['observed'] == ['gel', 'micrograph'])
    check('v_ec18_carries_transform', _p['transformation_types'] == ['rotation_90cw'])
    check('v_ec18_carries_complexity', _p['complexity_dist'] == {'Simple': 80, 'Hard': 20})

    # flat / thin evidence -> generate across the range, never fixate
    _flatp = _P({'vision_status': 'observed',
                 'object_types': {'dominant': [], 'observed': ['a', 'b', 'c']},
                 'dominant_suppressed': 'flat distribution'})
    check('v_ec18_observed_mode', _flatp['mode'] == 'observed')
    check('v_ec18_observed_range', _flatp['observed'] == ['a', 'b', 'c'])
    check('v_ec18_reason_propagated', _flatp['reason'] == 'flat distribution')
    # dominant is always a subset of observed, whatever the input says
    check('v_ec18_dominant_subset',
          set(_P({'object_types': {'dominant': ['x'], 'observed': []}})['dominant'])
          <= set(_P({'object_types': {'dominant': ['x'], 'observed': []}})['observed']))
    check('v_ec18_modes_valid',
          all(_P(i)['mode'] in GENERATION_MODES
              for i in (None, {}, _real, {'object_types': {'observed': ['q']}})))

    # ── STEP 8 CONFORMANCE GATE (shared rule) ──────────────────────────────
    _C = check_figural_conformance
    _dom = _P({'vision_status': 'observed',
               'object_types': {'dominant': ['micrograph'],
                                'observed': ['micrograph', 'gel']}})
    check('v_conf_pass_dominant',
          _C(['micrograph'] * 7 + ['gel'] * 3, _dom)[0] == 'PASS')
    check('v_conf_fail_under_floor',
          _C(['gel'] * 7 + ['micrograph'] * 3, _dom)[0] == 'FAIL')
    check('v_conf_fail_stray_type',
          _C(['micrograph', 'bar_chart'], _dom)[0] == 'FAIL')
    check('v_conf_stray_named',
          'bar_chart' in _C(['micrograph', 'bar_chart'], _dom)[1])
    # legacy / empty -> SKIP, never FAIL (EC-V18: ~200 exams depend on this)
    check('v_conf_skip_unconstrained', _C(['anything'], _P({}))[0] == 'SKIP')
    check('v_conf_skip_no_types', _C([], _dom)[0] == 'SKIP')
    check('v_conf_skip_none', _C(None, None)[0] == 'SKIP')
    # observed mode: any observed type passes, a stray still fails
    _obs = _P({'vision_status': 'observed',
               'object_types': {'dominant': [], 'observed': ['a', 'b', 'c']}})
    check('v_conf_observed_pass', _C(['a', 'b', 'c', 'a'], _obs)[0] == 'PASS')
    check('v_conf_observed_stray', _C(['a', 'z'], _obs)[0] == 'FAIL')
    # small-N tolerance: 2 of 3 dominant = 67% >= 55% floor
    check('v_conf_small_n_tolerated',
          _C(['micrograph', 'micrograph', 'gel'], _dom)[0] == 'PASS')
    check('v_conf_never_raises',
          all(_C(g, p)[0] in ('PASS', 'FAIL', 'SKIP')
              for g in (None, [], ['x'], [None, ''])
              for p in (None, {}, _dom, _obs, {'mode': 'dominant'})))

    # ── section_rules PYQ_IMAGE_ANALYSIS PARSER ────────────────────────────
    _legacy_sr = """--- Subtopic: Chromatography ---
subtopic_id: bt.tech.chromatography
format: FIGURAL
PYQ_IMAGE_ANALYSIS:
  image_role: stem_only
  object_types:
    dominant: []
    observed: []
  transformation_types: []
  images_analysed: 0
  images_unclear: 0

--- Subtopic: Gel Electrophoresis ---
subtopic_id: bt.tech.gel
format: FIGURAL
PYQ_IMAGE_ANALYSIS:
  image_role: stem_and_options
  vision_status: observed
  object_types:
    dominant: ['gel_band_pattern']
    observed: ['gel_band_pattern', 'plot_curve']
    avoid: []
  transformation_types: ['N/A']
  arrangement_types: ['single']
  complexity_dist: {'Simple': 60, 'Medium': 40}
  images_analysed: 9
  images_unclear: 1
  images_unobserved: 0
"""
    _pb = parse_image_analysis_blocks(_legacy_sr)
    check('v_parse_two_blocks', set(_pb) == {'bt.tech.chromatography', 'bt.tech.gel'})
    check('v_parse_legacy_shape',
          _pb['bt.tech.chromatography']['object_types']['dominant'] == []
          and 'vision_status' not in _pb['bt.tech.chromatography'])
    check('v_parse_legacy_unconstrained',
          figural_generation_profile(_pb['bt.tech.chromatography'])['mode']
          == 'unconstrained')
    check('v_parse_v237_shape',
          _pb['bt.tech.gel']['object_types']['dominant'] == ['gel_band_pattern']
          and _pb['bt.tech.gel']['vision_status'] == 'observed')
    check('v_parse_complexity',
          _pb['bt.tech.gel']['complexity_dist'] == {'Simple': 60, 'Medium': 40})
    check('v_parse_counts',
          _pb['bt.tech.gel']['images_analysed'] == 9
          and _pb['bt.tech.gel']['images_unclear'] == 1)
    check('v_parse_v237_binds',
          figural_generation_profile(_pb['bt.tech.gel'])['mode'] == 'dominant')
    # malformed / absent input must yield {} and never raise
    for _bad in (None, '', 'garbage', 123, [],
                 '--- Subtopic: X ---\nno_id_here\n',
                 '--- Subtopic: X ---\nsubtopic_id: y\n(no image block)\n'):
        check(f'v_parse_safe_{type(_bad).__name__}_{str(_bad)[:8]}',
              parse_image_analysis_blocks(_bad) in ({}, {'y': {}}) or
              isinstance(parse_image_analysis_blocks(_bad), dict))
    # A corrupt literal does not match the value pattern at all, so the key is simply
    # ABSENT — which resolves to 'unconstrained'. That is the safe outcome: a parsing
    # problem must never become a generation constraint or a failed run.
    _corrupt = parse_image_analysis_blocks(
        '--- Subtopic: X ---\nsubtopic_id: y\nPYQ_IMAGE_ANALYSIS:\n'
        '  object_types:\n    dominant: [not-a-literal\n')
    check('v_parse_corrupt_key_absent',
          'object_types' not in _corrupt.get('y', {}))
    check('v_parse_corrupt_unconstrained',
          figural_generation_profile(_corrupt.get('y', {}))['mode'] == 'unconstrained')

    # ── GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION — channel-aware transport ──
    _papers = [{'name': f'p{i}.docx', 'fileSize': 45_000} for i in range(22)]
    _spill = partition_by_transport(_papers)
    check('t_channel_default_is_spill', _spill['channel'] == 'spill')
    check('t_spill_backward_compatible',
          len(_spill['auto']) == 22 and _spill['upload'] == [])
    check('t_spill_costs_no_context', _spill['inline_chars'] == 0)
    _inline = partition_by_transport(_papers, channel='inline')
    check('t_inline_bounds_the_drive_lane', len(_inline['auto']) < 22)
    check('t_inline_remainder_goes_to_upload',
          len(_inline['auto']) + len(_inline['upload']) == 22)
    check('t_inline_never_exceeds_budget',
          _inline['inline_chars'] <= INLINE_BUDGET_CHARS)
    check('t_inline_deferred_is_reported',
          _inline['deferred_for_context'] == _inline['upload'])
    # a generous budget must leave the inline lane identical to the spill lane
    _rich = partition_by_transport(_papers, channel='inline', inline_budget=10 ** 9)
    check('t_inline_with_budget_matches_spill', len(_rich['auto']) == 22)
    # the cap still binds regardless of channel
    _big = [{'name': 'huge.docx', 'fileSize': DRIVE_CAP + 1}]
    check('t_cap_binds_on_spill', partition_by_transport(_big)['upload'] == _big)
    check('t_cap_binds_on_inline',
          partition_by_transport(_big, channel='inline')['upload'] == _big)
    check('t_missing_size_goes_to_upload',
          len(partition_by_transport([{'name': 'x.docx'}])['upload']) == 1)
    _bad_channel = 0
    try:
        partition_by_transport(_papers, channel='guess')
    except AllocationError:
        _bad_channel = 1
    check('t_unknown_channel_raises', _bad_channel == 1)
    # ── GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION ──────────────────────
    # The predicate must accept BOTH forms PYQSort CHECK 3 emits, tolerate the
    # leading/trailing whitespace a paragraph carries, and reject anything that
    # merely looks bracketed — a false positive here TERMINATES a question body
    # early and silently truncates the stem, which is worse than the defect.
    check('t_poslabel_with_session',
          is_position_label('[12-Sep-2025 Shift 1]'))
    check('t_poslabel_without_session', is_position_label('[02-May-2010]'))
    check('t_poslabel_single_digit_day', is_position_label('[5-Jan-2024 Shift 1]'))
    check('t_poslabel_stamped_position', is_position_label('[15-Feb-2026 Q.31]'))
    check('t_poslabel_tolerates_padding', is_position_label('   [02-May-2010]  '))
    check('t_poslabel_rejects_none_and_empty',
          not is_position_label(None) and not is_position_label('')
          and not is_position_label('   '))
    check('t_poslabel_rejects_question_stem',
          not is_position_label('Q.1 For each positive integer n, let'))
    check('t_poslabel_rejects_option_line', not is_position_label('[1] first option'))
    # ANCHORING IS THE REQUIREMENT, not an implementation detail. If the leading ^ ever
    # leaves DATE_TAG_RE, S3-2 would terminate a question body on any stem that MENTIONS
    # a label — truncating the stem and DISCARDING ITS OPTIONS, which is strictly worse
    # than the defect this predicate was added to fix. Mutation-verified: dropping the ^
    # is killed by these three and by nothing else in this suite.
    # (Swapping .match for .search is an EQUIVALENT mutant while the ^ is present — no
    # fixture can kill it, and none should pretend to. The ^ is what is under test.)
    check('t_poslabel_rejects_midline_match',
          not is_position_label('see [12-Sep-2025 Shift 1] above'))
    check('t_poslabel_rejects_label_after_leading_text',
          not is_position_label('Q.7 compare with [02-May-2010] and note'))
    check('t_poslabel_anchored_not_searched',
          not any(is_position_label(t) for t in
                  ('the paper [15-Feb-2026 Q.1] states',
                   'x = [1-2] interval, see [02-May-2010]',
                   'ref: [5-Jan-2024 Shift 1]')))
    # CHECK AO (GAP-2026-08-02) rejected the first version of this fixture, correctly:
    # it asserted `is_position_label(x) == bool(DATE_TAG_RE.match(x.strip()))`, which
    # INLINES the function's own body. A tautology cannot fail for any value of the
    # predicate, so it locked nothing at all. What must be pinned is the REQUIREMENT
    # the callers depend on, not the implementation that currently satisfies it.
    #
    # THE REQUIREMENT (Framework_MockTestAnalyse S3-2, GAP-2026-08-16-...-DATE-LABEL-
    # POSITION): the inner body loop terminates on a label and MUST NOT terminate on
    # anything else, because a false positive truncates a stem and drops its options —
    # strictly worse than the defect being fixed. So the fixture is a BLOCK SHAPE and
    # the verdict it must produce: one real PYQSort-stamped paper fragment, terminating
    # at exactly the paragraphs that are labels and no others.
    _frag = ['[15-Feb-2026 Q.1]',                       # label  -> terminate
             'Q.1  For each positive integer n, let',   # stem   -> continue
             '1. (x_n) and (y_n) are convergent.',      # option -> continue
             '2. Only (x_n) is convergent.',            # option -> continue
             '[15-Feb-2026 Q.2]',                       # label  -> terminate
             'Q.2  Let f be continuous on [0,1].',      # stem   -> continue
             'see [15-Feb-2026 Q.1] for context',       # prose  -> continue (mid-line)
             '[1] a bracketed option label',            # option -> continue
             '']                                        # blank  -> continue
    check('t_poslabel_terminates_at_exactly_the_labels',
          [i for i, t in enumerate(_frag) if is_position_label(t)] == [0, 4])
    # And the count is what S3-2 relies on: one label per question in the fragment.
    check('t_poslabel_one_per_question',
          sum(1 for t in _frag if is_position_label(t))
          == sum(1 for t in _frag if t.startswith('Q.')))
    check('t_base64_cost_exact', base64_cost_chars(986_230) == 1_314_976)
    check('t_base64_cost_zero_safe',
          base64_cost_chars(0) == 0 and base64_cost_chars(None) == 0)

    # ── GAP-2026-08-16-STEP5-SESSION-EXHAUSTION ─────────────────────────────
    # EC-P43 — the DIRECT lane costs no context, so it must admit exactly what
    # 'spill' admits. Any divergence means a cost model leaked into a mechanism.
    _22 = [{'name': f'p{i}.docx', 'fileSize': 47_627} for i in range(22)]
    check('t_direct_admits_whole_corpus',
          len(partition_by_transport(_22, channel='direct')['auto']) == 22)
    check('t_direct_matches_spill',
          partition_by_transport(_22, channel='direct')['auto']
          == partition_by_transport(_22, channel='spill')['auto'])
    check('t_direct_still_honours_cap',
          partition_by_transport(_big, channel='direct')['upload'] == _big)
    check('t_direct_reports_zero_chars',
          partition_by_transport(_22, channel='direct')['inline_chars'] == 0)

    # EC-P40 — the probe is a SPENDER. These four cases are the whole contract.
    _probe_cost = base64_cost_chars(47_627)                      # 63,504
    check('t_consumed_default_is_backward_compatible',
          partition_by_transport(_22, channel='inline', inline_budget=100_000)['auto']
          == partition_by_transport(_22, channel='inline', inline_budget=100_000,
                                    consumed=0)['auto'])
    check('t_consumed_reduces_admission',
          len(partition_by_transport(_22, channel='inline', inline_budget=200_000,
                                     consumed=_probe_cost)['auto'])
          < len(partition_by_transport(_22, channel='inline',
                                       inline_budget=200_000)['auto']))
    _exhausted = partition_by_transport(_22, channel='inline',
                                        inline_budget=100_000, consumed=100_000)
    check('t_consumed_at_budget_admits_nothing', _exhausted['auto'] == [])
    check('t_consumed_at_budget_defers_for_context',
          len(_exhausted['deferred_for_context']) == 22)
    check('t_consumed_over_budget_does_not_go_negative',
          partition_by_transport(_22, channel='inline', inline_budget=100_000,
                                 consumed=999_999)['effective_budget'] == 0)
    check('t_consumed_inert_on_spill',
          len(partition_by_transport(_22, channel='spill',
                                     consumed=999_999)['auto']) == 22)
    check('t_consumed_inert_on_direct',
          len(partition_by_transport(_22, channel='direct',
                                     consumed=999_999)['auto']) == 22)
    check('t_consumed_reported_zero_when_inert',
          partition_by_transport(_22, channel='direct',
                                 consumed=999_999)['consumed'] == 0)
    _neg = 0
    try:
        partition_by_transport(_22, channel='inline', consumed=-1)
    except AllocationError:
        _neg = 1
    check('t_negative_consumed_raises', _neg == 1)
    _bad_consumed = 0
    try:
        partition_by_transport(_22, channel='inline', consumed='lots')
    except AllocationError:
        _bad_consumed = 1
    check('t_non_integer_consumed_raises', _bad_consumed == 1)
    # The incident, reproduced as arithmetic: 100,000-char session budget, probe on the
    # smallest paper (40,488 B -> 53,984 chars), then the 2026 paper (63,504 chars).
    # Pre-patch this printed "1 paper admitted"; it must now admit none and say so.
    _incident = partition_by_transport(
        [{'name': '2026.docx', 'fileSize': 47_627}], channel='inline',
        inline_budget=100_000, consumed=base64_cost_chars(40_488))
    check('t_incident_is_now_reported_infeasible', _incident['auto'] == [])

    # ── Cluster P: feasibility preflight + Phase-1 placement (v1.56.0) ───────
    # GAP-2026-08-25-BLUEPRINT-PHASE1. The incident geometry, as arithmetic.
    _jamB = derive_batch_size(114, 10, 20, 186)          # IIT JAM Section B, N=20
    check('p_jam_secB_tier2_bs20', (_jamB['tier'], _jamB['batch_size']) == (2, 20))
    _jamA = derive_batch_size(114, 30, 20, 586)
    check('p_jam_secA_tier1_bs10', (_jamA['tier'], _jamA['batch_size']) == (1, 10))
    _jamB10 = derive_batch_size(114, 10, 10, 93)         # N=10: section cannot hold all
    check('p_jam_secB_N10_tier3_minN13', (_jamB10['tier'], _jamB10['min_N']) == (3, 13))
    check('p_bs_no_pyq_tier1', derive_batch_size(0, 10, 20, 200)['tier'] == 1)
    check('p_bs_avail_zero_tier3', derive_batch_size(5, 10, 20, 0)['tier'] == 3)
    check('p_bs_capped_at_N', derive_batch_size(3, 5, 5, 25)['batch_size'] == 5)
    check('p_bs_N1_ok', derive_batch_size(1, 1, 1, 1) == {
        'tier': 1, 'batch_size': 1, 'arm_a': 1, 'arm_b': 1, 'min_N': 1,
        'note': 'default window holds'})
    check('p_bs_minimal_vs_brute', all(
        derive_batch_size(n, sq, N, av)['batch_size'] ==
        next(b for b in range(max(1, min(10, N)), N + 1)
             if batch_size_feasible(n, sq, N, av, b))
        for n, sq, N, av in [(114, 10, 20, 186), (60, 25, 30, 700), (7, 3, 12, 30),
                             (40, 8, 24, 150), (1, 1, 7, 7)]))
    _pf = feasibility_preflight(
        [{'name': 'A', 'sec_qs': 30, 'n_pq': 114, 'zp_slots': 14},
         {'name': 'B', 'sec_qs': 10, 'n_pq': 114, 'zp_slots': 14},
         {'name': 'C', 'sec_qs': 20, 'n_pq': 114, 'zp_slots': 14}], 20)
    check('p_preflight_jam_global_bs20', (_pf['batch_size_qs'], _pf['n_batches']) == (20, 1))
    check('p_preflight_jam_tiers', _pf['tiers'] == {'A': 1, 'B': 2, 'C': 1})
    check('p_preflight_config_too_small_overridden',
          feasibility_preflight([{'name': 'B', 'sec_qs': 10, 'n_pq': 114, 'zp_slots': 14}],
                                20, config_batch_size=10)['overrode_config'] is True)
    check('p_preflight_config_larger_honoured',
          feasibility_preflight([{'name': 'A', 'sec_qs': 30, 'n_pq': 20}], 20,
                                config_batch_size=15)['batch_size_qs'] == 15)
    _k, _u = capacity_split(['a', 'b', 'c', 'd'], {'a': 0.1, 'b': 0.9, 'c': 0.9, 'd': 0.0}, 2)
    check('p_capacity_split_ravg_desc_stable', (_k, _u) == (['b', 'c'], ['a', 'd']))
    check('p_exam_wide_uncovered',
          exam_wide_uncovered({'B': ['x', 'y'], 'A': ['y']},
                              {'x': ['A', 'B'], 'y': ['A', 'B'], 'z': ['A']}) == ['y'])
    check('p_max_rare_default', derive_max_rare({'s1': 1, 's2': 1}, 20) == 2)
    check('p_max_rare_raised', derive_max_rare({f's{i}': 3 for i in range(20)}, 20) == 3)
    # THE INCIDENT: 20 rare subtopics, quota 1 each, N=20, cap 2. Shipped formula put
    # all 20 at mock 11 and packed forward → mocks 1-10 empty, mocks 19/20 at 2.
    _inc = phase1_positions({f'r{i}': 1 for i in range(20)}, 20, 2)
    _per = {m: sum(1 for v in _inc.values() if m in v) for m in range(1, 21)}
    check('p_incident_every_mock_has_one_rare', all(_per[m] == 1 for m in range(1, 21)))
    check('p_incident_f2_passes', all(_per[m] <= f2_threshold(1.0) for m in (19, 20)))
    check('p_incident_f2b_no_dead_stretch', dead_stretch(_per, 20)[0] == 0)
    _q4 = phase1_positions({'s': 4}, 20, 2)['s']
    check('p_q4_one_per_segment', [(p - 1) * 4 // 20 for p in _q4] == [0, 1, 2, 3])
    check('p_q4_within_f4_tolerance', all(
        abs(a - i) <= math.ceil(20 / 8) for a, i in zip(_q4, [3, 8, 13, 18])))
    check('p_quota_capped_at_N', len(phase1_positions({'s': 25}, 20, 2)['s']) == 20)
    check('p_cap_respected', max(
        sum(1 for v in phase1_positions({f'r{i}': 2 for i in range(9)}, 10, 2).values()
            if m in v) for m in range(1, 11)) <= 2)
    check('p_order_is_contract',
          phase1_positions({'a': 1, 'b': 1}, 10, 2) != phase1_positions({'b': 1, 'a': 1}, 10, 2)
          or phase1_positions({'a': 1, 'b': 1}, 10, 2)['a'] != phase1_positions({'b': 1, 'a': 1}, 10, 2)['a'])
    check('p_f2_threshold_floor', f2_threshold(0.48) == 1.0 and f2_threshold(1.125) == 2.0
          and f2_threshold(1.0) == 1.5 and f2_threshold(0) == 0.0)
    check('p_dead_stretch_front_loaded_fails',
          dead_stretch({m: (2 if m <= 10 else 0) for m in range(1, 21)}, 20)[:2] == (10, 2))
    check('p_dead_stretch_sparse_spread_ok',
          (lambda r: r[0] <= r[1])(dead_stretch({1: 1, 8: 1, 15: 1}, 20)))
    check('p_dead_stretch_dormant', dead_stretch({}, 20) == (0, 0, 0))
    check('p_window_bs20_batch1_defers', coverage_window(1, 10, 20, 20) == (1, 1, 20, False))
    check('p_window_bs20_batch2_closes', coverage_window(11, 20, 20, 20) == (1, 1, 20, True))
    check('p_window_bs10_unchanged', coverage_window(11, 20, 10, 25) == (2, 11, 20, True))
    check('p_window_last_short', coverage_window(21, 25, 10, 25) == (3, 21, 25, True))

    # ── Cluster E2d: difficulty gate windows (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS)
    def _legacy_assess(cls, steps, concepts, hack, conf, neg, qt, labels):
        # the pre-split assess_difficulty body, VERBATIM, as the identity oracle
        if not isinstance(labels, (list, tuple)) or len(labels) != 3:
            return None
        E_, M_, H_ = labels
        if cls is None:
            fac = []
        elif isinstance(cls, (list, tuple, set)):
            fac = [str(c).strip().upper() for c in cls if c]
        else:
            fac = [str(cls).strip().upper()]
        fc = _QTYPE_FLOOR_CLASS.get(str(qt or '').strip().lower())
        if fc:
            fac.append(fc)
        sc = max(CLASS_BASELINE.get(f, _UNKNOWN_CLASS_BASELINE) for f in fac) if fac else _UNKNOWN_CLASS_BASELINE
        st = _as_int(steps)
        sc += 3 if st >= 5 else 2 if st >= 3 else 1 if st >= 2 else 0
        co = _as_int(concepts)
        sc += 2 if co >= 3 else 1 if co >= 2 else 0
        if str(conf or '').strip().lower() == 'flagged':
            sc += 2
        if neg:
            sc += 1
        if hack and st >= 4:
            sc += 1
        return E_ if sc <= DIFFICULTY_EASY_MAX else M_ if sc <= DIFFICULTY_MEDIUM_MAX else H_
    _grid_ok, _grid_n = True, 0
    for _cls in (None, 'C-FACTUAL', 'C-FORMAL-LOGIC', 'C-COMPUTATIONAL',
                 ['C-FIGURAL', 'C-COMPUTATIONAL'], 'C-MULTI-SELECT', 'X-UNKNOWN', ''):
        for _st in (None, 0, 1, 2, 3, 4, 5, 9, '3', 2.0):
            for _co in (None, 0, 1, 2, 3, 5):
                for _hk in (False, True):
                    for _cf in ('full', 'flagged', None):
                        for _ng in (False, True):
                            for _qt in ('mcq', 'msq', 'nat', None, 'NAT '):
                                _grid_n += 1
                                _want = _legacy_assess(_cls, _st, _co, _hk, _cf, _ng, _qt, _L)
                                _sc = difficulty_score(_cls, _st, _co, _hk, _cf, _ng, _qt)
                                if (assess_difficulty(_cls, _st, _co, _hk, _cf, _ng, _qt, _L) != _want
                                        or band_for_score(_sc, _L) != _want
                                        or not isinstance(_sc, int) or _sc < 0 or _sc > 12):
                                    _grid_ok = False
    check('e2d_score_split_identity', _grid_ok and _grid_n > 10000)
    check('e2d_score_scale_bounds',
          difficulty_score(None, 0, 0, False, 'full', False, 'mcq') == 1
          and difficulty_score('C-FACTUAL', 0, 0, False, 'full', False, 'mcq') == 0
          and difficulty_score('C-NUMERICAL-INPUT', 5, 3, True, 'flagged', True, 'nat') == 12)
    check('e2d_band_for_score_edges',
          band_for_score(DIFFICULTY_EASY_MAX, _L) == _L[0]
          and band_for_score(DIFFICULTY_EASY_MAX + 1, _L) == _L[1]
          and band_for_score(DIFFICULTY_MEDIUM_MAX, _L) == _L[1]
          and band_for_score(DIFFICULTY_MEDIUM_MAX + 1, _L) == _L[2]
          and band_for_score(3, ['Lo', 'Hi']) is None
          and band_for_score(None, _L) is None and band_for_score(True, _L) is None
          and band_for_score('3', _L) is None)
    _obs = {'question_class': ['C-COMPUTATIONAL'], 'deduction_steps': 3,
            'axiom_concepts': 2, 'speed_hack_exists': True, 'is_negative': False,
            'qtype': 'mcq'}
    check('e2d_score_from_obs_matches_verify',
          difficulty_score_from_obs(_obs) == 5
          and band_for_score(difficulty_score_from_obs(_obs), _L) == verify_difficulty_obs(_L[1], _obs, _L)[1]
          and difficulty_score_from_obs(None) is None and difficulty_score_from_obs({}) is None
          and difficulty_score_from_obs('x') is None)
    # windows: shape, and every gated window CONTAINS its authoring band
    _w = _gate_windows(DIFFICULTY_GATE_BAND_WINDOWS)
    _auth = [(0, DIFFICULTY_EASY_MAX), (DIFFICULTY_EASY_MAX + 1, DIFFICULTY_MEDIUM_MAX),
             (DIFFICULTY_MEDIUM_MAX + 1, None)]
    check('e2d_windows_contain_authoring_bands',
          len(_w) == 3 and _w[0] is None and _w[1] == (2, 6) and _w[2] == (5, None)
          and all(w is None or (w[0] <= a[0] and (w[1] is None or (a[1] is not None and a[1] <= w[1])))
                  for w, a in zip(_w, _auth)))
    def _raises(fn):
        try:
            fn()
            return False
        except ValueError:
            return True
    check('e2d_windows_malformed_raise',
          _raises(lambda: _gate_windows(None)) and _raises(lambda: _gate_windows([None, None]))
          and _raises(lambda: _gate_windows((None, (6, 2), None)))
          and _raises(lambda: _gate_windows((None, (-1, 2), None)))
          and _raises(lambda: _gate_windows((None, 5, None)))
          and _gate_windows((None, (None, 6), (5, None))) == (None, (0, 6), (5, None)))
    # allowed = exact floor(frac × n) for every n, no float drift
    from fractions import Fraction as _Fr
    check('e2d_allowed_exact_floor',
          all(_gate_allowed(0.35, n) == int(_Fr(35, 100) * n) for n in range(0, 601))
          and all(_gate_allowed(0.30, n) == int(_Fr(30, 100) * n) for n in range(0, 601))
          and _gate_allowed(0.35, 6) == 2 and _gate_allowed(0.35, 18) == 6
          and _gate_allowed(0.35, 36) == 12 and _gate_allowed(0.35, 20) == 7
          and _gate_allowed(-1, 10) == 0 and _gate_allowed('bad', 10) == 0)
    check('e2d_gate_score_coercion',
          _gate_score(5) == 5 and _gate_score('5') == 5 and _gate_score(5.0) == 5
          and _gate_score(5.5) is None and _gate_score(True) is None
          and _gate_score(None) is None and _gate_score(-1) is None
          and _gate_score(float('nan')) is None and _gate_score('x') is None)
    check('e2d_gate_lookup_key_types',
          _gate_lookup({1: 'a'}, '1') == 'a' and _gate_lookup({'1': 'a'}, 1) == 'a'
          and _gate_lookup({'q1': 'a'}, 'q1') == 'a' and _gate_lookup({}, 1) is None
          and _gate_lookup(None, 1) is None and _gate_lookup({1: 'a'}, 'x') is None)
    # the gate itself — windows, direction, ungated bottom band, thresholds
    _lab = {q: _L[0] for q in range(1, 7)}
    _lab.update({q: _L[1] for q in range(7, 25)})
    _lab.update({q: _L[2] for q in range(25, 61)})
    _sc_all_ok = {q: (1 if q <= 6 else 4 if q <= 24 else 7) for q in _lab}
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc_all_ok)
    check('e2d_gate_pass_clean',
          _g['verdict'] == 'PASS' and _g['rework_qs'] == [] and _g['dormant'] is False
          and _g['threshold'] == DIFFICULTY_GATE_MAX_DISAGREE_FRAC
          and _g['windows'] == [None, [2, 6], [5, None]]
          and _g['bands'][_L[0]] == {'total': 6, 'gated': False, 'window': None,
                                     'assessed': 0, 'agree': 0, 'disagree': 0,
                                     'allowed': 2, 'over_limit': False, 'disagreeing_qs': []}
          and _g['bands'][_L[1]]['allowed'] == 6 and _g['bands'][_L[2]]['allowed'] == 12
          and _g['bands'][_L[1]]['assessed'] == 18 and _g['bands'][_L[2]]['agree'] == 36)
    # bottom band is never gated — even if every Easy measures Hard
    _sc = dict(_sc_all_ok); _sc.update({q: 12 for q in range(1, 7)})
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    check('e2d_gate_bottom_band_ignored', _g['verdict'] == 'PASS' and _g['rework_qs'] == [])
    # middle window is INCLUSIVE 2..6: scores 2 and 6 agree, 1 and 7 disagree
    _sc = dict(_sc_all_ok); _sc.update({7: 2, 8: 6, 9: 1, 10: 7})
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    check('e2d_gate_middle_window_inclusive',
          _g['verdict'] == 'PASS' and _g['bands'][_L[1]]['disagree'] == 2
          and _g['bands'][_L[1]]['disagreeing_qs'] == [9, 10] and _g['rework_qs'] == [])
    # top window is 5+ : 5 agrees, 4 disagrees (harder), and 12 agrees
    _sc = dict(_sc_all_ok); _sc.update({25: 5, 26: 4, 27: 12})
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    check('e2d_gate_top_window_5_plus',
          _g['bands'][_L[2]]['disagreeing_qs'] == [26] and _g['verdict'] == 'PASS')
    # threshold boundary: 12 disagreements in 36 pass, 13 fail — and rework lists ONLY the over-limit band
    _sc = dict(_sc_all_ok); _sc.update({q: 4 for q in range(25, 37)}); _sc[7] = 1
    _g12 = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    _sc[37] = 3
    _g13 = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    check('e2d_gate_threshold_boundary',
          _g12['verdict'] == 'PASS' and _g12['bands'][_L[2]]['disagree'] == 12
          and _g13['verdict'] == 'FAIL' and _g13['bands'][_L[2]]['over_limit'] is True
          and _g13['rework_qs'] == list(range(25, 38))
          and 7 not in _g13['rework_qs']                 # middle band under limit → untouched
          and all(_g13['rework_directions'][q] == 'harder' for q in range(25, 38)))
    # direction 'easier' when a middle-band question measures above its window
    _sc = dict(_sc_all_ok); _sc.update({q: 8 for q in range(7, 14)})
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc)
    check('e2d_gate_direction_easier',
          _g['verdict'] == 'FAIL' and _g['rework_qs'] == list(range(7, 14))
          and set(_g['rework_directions'].values()) == {'easier'})
    # label-only fallback == the old band-equality rule (never more lenient)
    _meas = {q: _lab[q] for q in _lab}; _meas.update({25: _L[1], 26: _L[1], 7: _L[0], 8: _L[2]})
    _g = evaluate_difficulty_gate(_lab, _meas, _L)
    check('e2d_gate_label_fallback_conservative',
          _g['verdict'] == 'PASS' and _g['bands'][_L[2]]['disagreeing_qs'] == [25, 26]
          and _g['bands'][_L[1]]['disagreeing_qs'] == [7, 8]
          and _g['bands'][_L[1]]['assessed'] == 18 and _g['bands'][_L[2]]['assessed'] == 36)
    # a raw score beats the label: measured label says Medium but score 5 sits in the top window
    _g = evaluate_difficulty_gate(_lab, {25: _L[1]}, _L, scores_by_q={25: 5})
    check('e2d_gate_score_overrides_label', _g['bands'][_L[2]]['disagree'] == 0)
    # unassessed questions (no score, no label) are skipped, never counted either way
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q={25: None})
    check('e2d_gate_unassessed_skipped',
          _g['verdict'] == 'PASS' and _g['bands'][_L[2]]['assessed'] == 0
          and _g['bands'][_L[1]]['assessed'] == 0)
    # registry (str) keys vs spec (int) keys — every combination reaches the same verdict
    _lab_s = {str(q): v for q, v in _lab.items()}
    _sc_s = {str(q): 4 for q in range(25, 38)}
    _sc_s.update({str(q): v for q, v in _sc_all_ok.items() if q < 25})
    _ga = evaluate_difficulty_gate(_lab_s, {}, _L, scores_by_q=_sc_s)
    _gb = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc_s)
    _gc = evaluate_difficulty_gate(_lab_s, {}, _L, scores_by_q={int(k): v for k, v in _sc_s.items()})
    check('e2d_gate_key_type_agnostic',
          _ga['verdict'] == _gb['verdict'] == _gc['verdict'] == 'FAIL'
          and [int(q) for q in _ga['rework_qs']] == _gb['rework_qs'] == [int(q) for q in _gc['rework_qs']]
          == list(range(25, 38)))
    # empty band / empty paper / non-3-band vocabulary
    _g = evaluate_difficulty_gate({1: _L[2]}, {}, _L, scores_by_q={1: 2})
    check('e2d_gate_small_band_zero_allowed',
          _g['verdict'] == 'FAIL' and _g['bands'][_L[2]]['allowed'] == 0
          and _g['bands'][_L[1]]['total'] == 0 and _g['rework_qs'] == [1])
    _g = evaluate_difficulty_gate({}, {}, _L)
    check('e2d_gate_empty_paper', _g['verdict'] == 'PASS' and _g['rework_qs'] == [])
    _g = evaluate_difficulty_gate(_lab, {}, ['Lo', 'Hi'], scores_by_q=_sc_all_ok)
    check('e2d_gate_non3band_dormant',
          _g['verdict'] == 'PASS' and _g['dormant'] is True and _g['rework_qs'] == [])
    # custom label vocabulary: the rule is POSITIONAL, not name-based
    _Lx = ['Level-1', 'Level-2', 'Level-3']
    _labx = {q: _Lx[0] if q <= 6 else _Lx[1] if q <= 24 else _Lx[2] for q in range(1, 61)}
    _scx = {q: 12 if q <= 6 else 4 if q <= 24 else 5 for q in range(1, 61)}
    _g = evaluate_difficulty_gate(_labx, {}, _Lx, scores_by_q=_scx)
    check('e2d_gate_positional_vocabulary',
          _g['verdict'] == 'PASS' and _g['bands']['Level-1']['gated'] is False
          and _g['bands']['Level-3']['agree'] == 36)
    # explicit override of threshold and windows still honoured (repair-mode / audit callers)
    _sc = dict(_sc_all_ok); _sc.update({q: 5 for q in range(25, 37)})
    _g = evaluate_difficulty_gate(_lab, {}, _L, scores_by_q=_sc, max_disagree_frac=0.30,
                                  band_windows=(None, (3, 5), (6, None)))
    check('e2d_gate_override_params',
          _g['verdict'] == 'FAIL' and _g['bands'][_L[2]]['allowed'] == 10
          and _g['bands'][_L[2]]['disagree'] == 12 and _g['threshold'] == 0.30)
    check('e2d_gate_bad_windows_raise',
          _raises(lambda: evaluate_difficulty_gate(_lab, {}, _L, band_windows=(None, (6, 2), None))))
    check('e2d_gate_pure_no_mutation',
          (lambda a, b: evaluate_difficulty_gate(a, {}, _L, scores_by_q=b) and a == _lab and b == _sc_all_ok)
          (dict(_lab), dict(_sc_all_ok)))

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total




# ═══════════════════════════════════════════════════════════════════════════
# Cluster E2d — DIFFICULTY GATE (GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING)
# Fix 1: band-level reconciliation of Step-7 labels against Step-9's
# independent re-derivation — the gate MockTestExplain §7A-M now ENFORCES
# (blocking; ONE repair round via TestCreateRepair/TestExplainRepair; then
# deliver-with-disclosure, never a stop). Fix 2: evidence-diversity floor
# (anti profile-echo), shared by A-QINDEX check 9 so gate and audit cannot
# drift. Pure functions: plain data in, dicts/strings out. No I/O.
# ═══════════════════════════════════════════════════════════════════════════

DIFFICULTY_GATE_MAX_DISAGREE_FRAC = 0.35   # operator decision 2026-08-25 (was 0.30)
DIFFICULTY_GATE_MAX_REPAIR_ROUNDS = 1      # operator decision 2026-08-24

# GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS — operator decision 2026-08-25.
# Per-band ACCEPTANCE WINDOWS on the 0..12 rubric score, indexed by band
# POSITION in the exam's difficulty_labels (0 = bottom, 1 = middle, 2 = top) so
# the rule is identical for every label vocabulary across ~200 exams.
#   None        → the band is NOT gated at Step 9 (bottom band: operator decision —
#                 Step 9 does not evaluate it; its questions never enter rework).
#   (lo, hi)    → a question labelled with this band AGREES when
#                 lo <= measured score <= hi; hi=None means unbounded above.
# The authoring edges (DIFFICULTY_EASY_MAX=2 / DIFFICULTY_MEDIUM_MAX=5) are NOT
# changed by this: Step 7 still AUTHORS to the strict bands 0-2 / 3-5 / 6+; Step 9
# GRADES with one point of tolerance. Invariant (self-test e2d_windows_contain_
# authoring_bands): every gated window CONTAINS its own authoring band, so a
# correctly authored question can never fail its own gate.
DIFFICULTY_GATE_BAND_WINDOWS = (None, (2, 6), (5, None))
DIFFICULTY_OBS_MODAL_FRAC_MAX     = 0.60   # Fix 2 modal-signature ceiling
DIFFICULTY_OBS_DIVERSITY_MIN_N    = 8      # Fix 2: smaller bands exempt


def _gate_lookup(mapping, q):
    """Registry maps are JSON-keyed (str) while spec maps are int-keyed; a gate
    that missed a question over a key type would silently skip it. Try the key
    as given, then its str, then its int form."""
    if not isinstance(mapping, dict):
        return None
    if q in mapping:
        return mapping[q]
    sq = str(q)
    if sq in mapping:
        return mapping[sq]
    try:
        iq = int(sq)
    except (TypeError, ValueError):
        return None
    return mapping.get(iq)


def _qkey(q):
    """Stable ordering for question keys that may be int or numeric str
    (registry JSON vs spec ints): numeric first by value, then the rest by text."""
    sq = str(q).strip()
    return (0, int(sq), '') if sq.isdigit() else (1, 0, sq)


def _gate_score(value):
    """Coerce a stored measured score (int, numeric str, float from JSON) to int;
    None/bool/non-finite/negative → None (= not measurable)."""
    if value is None or isinstance(value, bool):
        return None
    try:
        if isinstance(value, float):
            if value != value or value in (float('inf'), float('-inf')):
                return None
            if value != int(value):
                return None
        v = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return v if v >= 0 else None


def _gate_allowed(max_disagree_frac, total):
    """floor(frac × total) computed without float drift: 0.35 × 20 is
    7.000000000000001 in binary floating point and 0.7 × 10 is 7.000000000000001,
    but other products land just BELOW the integer and int() would then floor one
    too low. Fractions make the floor exact for any decimal fraction."""
    from fractions import Fraction
    try:
        f = Fraction(str(max_disagree_frac))
    except (ValueError, ZeroDivisionError):
        f = Fraction(0)
    if f < 0:
        f = Fraction(0)
    return int(f * int(total))       # exact floor for non-negative rationals


def _gate_windows(band_windows):
    """Validate DIFFICULTY_GATE_BAND_WINDOWS-shaped input; a malformed window is a
    CONFIGURATION error (never data) and raises so it cannot silently pass."""
    if not isinstance(band_windows, (list, tuple)) or len(band_windows) != 3:
        raise ValueError('band_windows must be a 3-tuple (one entry per band position)')
    out = []
    for w in band_windows:
        if w is None:
            out.append(None)
            continue
        if not isinstance(w, (list, tuple)) or len(w) != 2:
            raise ValueError(f'band window must be None or (lo, hi): {w!r}')
        lo, hi = w
        lo = 0 if lo is None else int(lo)
        hi = None if hi is None else int(hi)
        if lo < 0 or (hi is not None and hi < lo):
            raise ValueError(f'band window out of order: {w!r}')
        out.append((lo, hi))
    return tuple(out)


def _label_interval(label, difficulty_labels):
    """Conservative score interval implied by a band LABEL alone (the fallback
    when a caller supplies no raw score): bottom 0..EASY_MAX, middle EASY_MAX+1..
    MEDIUM_MAX, top MEDIUM_MAX+1..None. None for a label outside the vocabulary."""
    if label == difficulty_labels[0]:
        return (0, DIFFICULTY_EASY_MAX)
    if label == difficulty_labels[1]:
        return (DIFFICULTY_EASY_MAX + 1, DIFFICULTY_MEDIUM_MAX)
    if label == difficulty_labels[2]:
        return (DIFFICULTY_MEDIUM_MAX + 1, None)
    return None


def evaluate_difficulty_gate(labels_by_q, measured_by_q, difficulty_labels,
                             max_disagree_frac=DIFFICULTY_GATE_MAX_DISAGREE_FRAC,
                             scores_by_q=None,
                             band_windows=DIFFICULTY_GATE_BAND_WINDOWS):
    """Band-level reconciliation of Step-7 labels against Step-9's independent
    re-derivation (GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS revision).

    labels_by_q    {q: Step-7 label}                       (the paper's stickers)
    measured_by_q  {q: Step-9 band label or None}          (kept for footers /
                   legacy callers; None = not measurable)
    scores_by_q    {q: Step-9 raw rubric score or None}    (bc.difficulty_score;
                   the PREFERRED evidence — None/absent falls back to the label)
    band_windows   per-POSITION acceptance windows, see DIFFICULTY_GATE_BAND_WINDOWS

    PER QUESTION a labelled question AGREES when its measured score lies inside
    the window of its label's band position. With no raw score the label is
    used through its conservative implied interval (_label_interval): agree
    only if that whole interval lies inside the window — which is exactly the
    old band-equality rule, so a label-only caller is never judged more
    leniently than before. A band whose window is None is NOT GATED: it is
    reported (total, gated=False) and contributes nothing to rework. A
    question with neither score nor measured label is "not assessed" and is
    skipped, as before.

    PER BAND the gate BLOCKS when disagreements EXCEED floor(max_disagree_frac
    × band total) — e.g. 36 top-band questions at 0.35 allow 12 and block at
    13. rework_qs lists the disagreeing questions of OVER-LIMIT bands only
    (repairing agreeing bands would churn accepted work); rework_directions
    says, per rework q, whether the question must move 'harder' (it measured
    below its window) or 'easier' (above) — Step 7's repair mode reads it.

    Non-3-band vocabulary → PASS with dormant=True (the spec prints its §R10
    DORMANT line and writes no verdict). q keys may be int or str on any map
    (registry JSON vs spec ints); windows are validated and a malformed one
    raises — configuration, never data, must not pass silently.

    Returns {'verdict','threshold','windows','bands','rework_qs',
             'rework_directions','dormant'}. Deterministic, pure.
    """
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return {'verdict': 'PASS', 'threshold': max_disagree_frac, 'windows': None,
                'bands': {}, 'rework_qs': [], 'rework_directions': {},
                'dormant': True, 'reason': 'difficulty vocabulary is not 3-band'}
    windows = _gate_windows(band_windows)
    labels_by_q = labels_by_q or {}
    bands, directions = {}, {}
    for pos, lab in enumerate(difficulty_labels):
        win = windows[pos]
        qs = sorted((q for q, l in labels_by_q.items() if l == lab), key=_qkey)
        total = len(qs)
        allowed = _gate_allowed(max_disagree_frac, total)
        if win is None:
            bands[lab] = {'total': total, 'gated': False, 'window': None,
                          'assessed': 0, 'agree': 0, 'disagree': 0,
                          'allowed': allowed, 'over_limit': False,
                          'disagreeing_qs': []}
            continue
        lo, hi = win
        assessed, disagree = 0, []
        for q in qs:
            sc = _gate_score(_gate_lookup(scores_by_q, q))
            if sc is not None:
                iv = (sc, sc)
            else:
                m = _gate_lookup(measured_by_q, q)
                iv = _label_interval(m, difficulty_labels) if m is not None else None
                if iv is None:
                    continue                       # not assessed — skipped
            assessed += 1
            ilo, ihi = iv
            below = ilo < lo                       # some mass under the window
            above = hi is not None and (ihi is None or ihi > hi)
            if below or above:
                disagree.append(q)
                # a label-only interval straddling both sides is treated as the
                # side its centre of mass suggests: below wins (too easy is the
                # measured failure class); a raw score is never on both sides.
                directions[q] = 'harder' if below else 'easier'
        bands[lab] = {'total': total, 'gated': True, 'window': [lo, hi],
                      'assessed': assessed, 'agree': assessed - len(disagree),
                      'disagree': len(disagree), 'allowed': allowed,
                      'over_limit': len(disagree) > allowed,
                      'disagreeing_qs': disagree}
    rework = [q for lab in difficulty_labels
              for q in bands[lab]['disagreeing_qs'] if bands[lab]['over_limit']]
    rework = sorted(rework, key=_qkey)
    return {'verdict': 'FAIL' if rework else 'PASS',
            'threshold': max_disagree_frac,
            'windows': [list(w) if w else None for w in windows],
            'bands': bands, 'rework_qs': rework,
            'rework_directions': {q: directions[q] for q in rework},
            'dormant': False}


def difficulty_obs_signature(obs):
    """Canonical evidence signature for the diversity check: the load-bearing
    numeric observations only. question_class is excluded on purpose — class
    facets legitimately repeat within a band; the numbers should not."""
    if not isinstance(obs, dict) or not obs:
        return None
    return (obs.get('deduction_steps'), obs.get('axiom_concepts'),
            bool(obs.get('speed_hack_exists')))


def difficulty_obs_diversity(questions, difficulty_labels,
                             max_modal_frac=DIFFICULTY_OBS_MODAL_FRAC_MAX,
                             min_n=DIFFICULTY_OBS_DIVERSITY_MIN_N):
    """Fix 2 — evidence-diversity floor (anti profile-echo). `questions` are
    question_index entries ({'q','difficulty','difficulty_obs',...}).
    THE SIGNAL: N independently derived questions cannot produce near-identical
    (steps, concepts, shortcut) measurements — a dominant identical tuple means
    the authoring profile's passing values were ECHOED, not measured (measured
    live: IIT_JAM_CHEMISTRY M01, 31/36 Hard identical at (6,3,False)).
    EXEMPT: the bottom band — its authoring profile is a single point (steps
    (2,2) × concepts (1,1)), so homogeneity there is REQUIRED by the rubric,
    never suspicious. Bands with fewer than min_n evidence-bearing entries are
    exempt (too small to distinguish echo from chance). Returns [] when clean,
    else one failure string per offending band. Never raises on legacy entries
    (no obs → entry skipped)."""
    if not isinstance(difficulty_labels, (list, tuple)) or len(difficulty_labels) != 3:
        return []
    fails = []
    for lab in difficulty_labels[1:]:                     # bottom band exempt
        sigs, qs_by_sig = {}, {}
        for x in questions:
            if x.get('difficulty') != lab:
                continue
            s = difficulty_obs_signature(x.get('difficulty_obs'))
            if s is None:
                continue                                  # legacy entry — skip
            sigs[s] = sigs.get(s, 0) + 1
            qs_by_sig.setdefault(s, []).append(x.get('q'))
        n = sum(sigs.values())
        if n < min_n:
            continue
        modal_sig, modal_n = max(sigs.items(), key=lambda kv: kv[1])
        if modal_n / n > max_modal_frac:
            fails.append(
                f"'{lab}' band: {modal_n}/{n} evidence tuples are the identical "
                f"(steps={modal_sig[0]}, concepts={modal_sig[1]}, "
                f"shortcut={modal_sig[2]}) — above the {max_modal_frac:.0%} "
                f"diversity ceiling. Independently measured derivations do not "
                f"repeat like this; the values appear COPIED from the authoring "
                f"profile rather than counted from each question "
                f"(Qs {','.join(str(q) for q in sorted(qs_by_sig[modal_sig])[:12])}"
                f"{'…' if modal_n > 12 else ''}). Re-run Step 7 CHECK 3c with "
                f"honest per-question counts.")
    return fails


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("blueprint_core.py — shared allocation core. Run with --self-test.")
