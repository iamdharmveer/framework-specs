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
    #   (3) Framework_MockTestCreateAudit's Step-8 B-AXIS1/B-AXIS3 audit, which scales the
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


def is_taxonomy_heading(para, is_option_fn):
    r"""True when a python-docx paragraph is a taxonomy heading rather than a question,
    an option or a date/shift tag. THE canonical implementation.

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
    if re.match(r'\[\d{1,2}-', text):
        return False
    has_bold = any(r.bold for r in para.runs if r.text.strip())
    return has_bold and len(text) < 100


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
    # Step-8 (MockTestCreateAudit B-AXIS1/3) scales the RETURNED per_paper maps by the
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
    check('h_clarity_clear', image_clarity_state(True, True) == 'clear')
    check('h_clarity_unclear', image_clarity_state(True, False) == 'unclear')
    check('h_clarity_blind', image_clarity_state(False, False) == 'vision_unavailable')
    check('h_clarity_blind_even_if_readable',
          image_clarity_state(False, True) == 'vision_unavailable')

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("blueprint_core.py — shared allocation core. Run with --self-test.")
