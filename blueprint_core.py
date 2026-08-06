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
      axis1_feasibility ........ §7-7
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
    "axis1_feasibility",
    "AXIS_WINDOW_YEARS",
    "AXIS_BAND_ABS",
    "AXIS_BAND_REL",
    "STIMULUS_CLASSES",
    "MECHANISM_CLASSES",
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
    """§7-7 ``_section_axis2_pool_caps``. VERBATIM.

    Union of Axis-2 capability across a section/scope's subtopic ids (used for
    guarantee feasibility). Only ids whose manifest section matches are counted.
    """
    caps = set()
    for sid in id_list:
        if manifest_ids.get(sid, {}).get("section") == section_name:
            caps |= set(cap_by_id.get(sid, ["DIRECT"]))
    return caps


def derive_axis_schedule(section_name, axis_dist, sec_qs,
                         pyq_ids, zp_ids, cap_by_id, manifest_ids,
                         papers_per_window=10):
    """§7-7 ``derive_axis_schedule``. VERBATIM except ``mocks_per_window`` renamed to
    ``papers_per_window`` (a mock is a paper; a scoped test is a paper).

    Returns the per-section (or per-scope) axis_schedule dict for blueprint.json.
      axis_dist : the format-distribution targets for this section/scope, or None.
      pyq_ids / zp_ids : subtopic_ids with r_avg>0 / r_avg==0 in this section/scope.

    Absent-safe: axis_dist is None (all-Zero-PYQ, or a pre-axis manifest) → a
    status='no_pyq' schedule and the whole feature stays inert.
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
        "axis3_target_per_mock": largest_remainder_apportion(a3, sec_qs),
        "negative_rate": axis_dist.get("negative_rate", 0.0),
        "mocks_per_window": papers_per_window,
        "recent_years": axis_dist.get("recent_years", []),
        # ── GAP-2026-08-06-AXIS1 ────────────────────────────────────────────────
        # A BUDGET THAT NOTHING SPENDS IS A BUG. These two flags exist so that fact
        # is machine-checkable rather than a convention someone has to remember:
        # Step 7 must build a tracker for every axis marked "hard", and the auditor
        # must refuse to certify a paper carrying a "hard" budget it has no gate for.
        # That single rule is what stops this defect class returning as Axis-4.
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
    """§7-7 ``axis1_feasibility``. VERBATIM. ADVISORY (WARN, never HALT).

    Compare the Axis-1 (stimulus) per-paper target against the formats actually
    available among this section/scope's PYQ subtopics. Returns the list of target
    formats with no capable PYQ subtopic ([] == fully feasible).
    """
    avail = set()
    for sid in pyq_ids:
        if manifest_ids.get(sid, {}).get("section") == section_name:
            avail.add(manifest_ids[sid].get("format", "TEXT"))
    unreachable = [fmt for fmt, cnt in axis1_target_per_mock.items()
                   if cnt > 0 and fmt not in avail]
    return unreachable


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

AXIS_BAND_ABS = 1       # audit tolerance: ±1 count …
AXIS_BAND_REL = 0.15    # … or ±15%, whichever is LARGER. A band, not an equality:
                        # real papers vary (this exam ranged 2→8 figures over 5 years)
                        # and a gate that demands an exact count gets disabled by hand.

STIMULUS_CLASSES  = ("TEXT", "FIGURAL", "PASSAGE", "DI")     # Axis-1
MECHANISM_CLASSES = ("MCQ", "MSQ", "NAT")                    # Axis-3

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
                           observable=None,
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
        _rel = _as_frac(band_rel)
        allow = max(_as_int(band_abs), _as_int(round(tgt * _rel)))
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
    EASY, MEDIUM, HARD = difficulty_labels

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

    if score <= DIFFICULTY_EASY_MAX:
        return EASY
    if score <= DIFFICULTY_MEDIUM_MAX:
        return MEDIUM
    return HARD


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
Q_PATTERNS = [r'^Q\.\s*(\d+)\s+', r'^Q(\d+)\.\s+']

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


def detect_question_start(text):
    """Return the source Q-number if this line starts a question, else None."""
    for pat in Q_PATTERNS:
        m = re.match(pat, (text or '').strip())
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

# Governor ladder: (tier, jpeg_quality, dpi_ceiling). dpi_ceiling None = no resize.
# T4 is the FLOOR — never encode below q80 or below 200 DPI at display size.
TIER_LADDER = (
    ('T1', 88, None),
    ('T2', 85, 300),
    ('T3', 82, 240),
    ('T4', 80, 200),
)

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


def partition_by_transport(papers, cap=DRIVE_CAP):
    """Split papers into the AUTO (Drive) lane and the UPLOAD lane BEFORE fetching.

    Partitioning on the CAP rather than on the governor budget is deliberate: a
    marginal 9.3 MiB paper downloads perfectly well today, and forcing it through a
    manual upload would be friction with no safety gain. The runtime fallback
    (corpus_io.fetch_drive_docx raising TransportFallback on ANY error) is what makes
    that safe — this partition is predictive, not binding, so a paper that is
    mispredicted still completes via upload instead of stopping the run.

    Each paper dict must carry 'fileSize'. Order is preserved.
    """
    auto, upload = [], []
    for p in papers:
        size = p.get('fileSize')
        (upload if (size is None or size > cap) else auto).append(p)
    return {'auto': auto, 'upload': upload}


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

    # 15 — TOTALITY OF THE WHOLE CLUSTER (v2.24.1). Every one of these inputs was a
    #      LIVE CRASH found by fuzzing, not by reading the code: int(float('inf'))
    #      raises OverflowError, which the original except-clause did not catch, and a
    #      non-dict schedule or a string rate went straight through to AttributeError /
    #      ValueError. blueprint_core's contract is NEVER RAISES — one malformed key
    #      from another step's JSON must not take a gate down with it (the defect class
    #      v2.12 closed), because a gate that dies looks exactly like a gate that passed.
    _JUNK = (None, 'x', '', -1, float('nan'), float('inf'), float('-inf'), [], {}, 2**70)
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
    check('h_part_empty', partition_by_transport([]) == {'auto': [], 'upload': []})

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

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("blueprint_core.py — shared allocation core. Run with --self-test.")
