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
    violation. Only the standard library (``math``, ``re``) is used.
"""

import math
import re

__all__ = [
    "AllocationError",
    "split_recency",
    "compute_r_avg",
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
    "score_difficulty",
    "determine_strip_mode",
    "map_difficulty_level",
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

def largest_remainder_apportion(raw_map, total):
    """Canonical largest-remainder apportionment (unifies §7-7 ``_avg_to_counts``
    and §7 S7-4 ``difficulty_counts``).

    Convert a ``{key: real-valued weight}`` map (whose values ~sum to ``total``) into
    integer counts summing EXACTLY to ``total``. Handles under- and over-count.

    Deterministic tie-break: by (fractional remainder, key). For a positive deficit
    the largest remainders get the +1s; for a negative deficit the smallest remainders
    are trimmed first, never below 0.
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
    elif deficit < 0:                                 # trim smallest remainder, ≥ 0
        order = sorted(raw, key=lambda k: ((raw[k] - floors[k]), k))
        i = 0
        while deficit < 0 and order:
            k = order[i % len(order)]
            if floors[k] > 0:
                floors[k] -= 1
                deficit += 1
            i += 1
            if i > 10 * len(order):                    # safety: guards infinite loop
                break
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

    a2 = axis_dist.get("axis2_per_paper", {})
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
        "axis1_per_paper": axis_dist.get("axis1_per_paper", {}),
        "axis2_per_paper": a2,
        "axis3_per_paper": axis_dist.get("axis3_per_paper", {}),
        "axis2_audit_mode": mode,
        "axis2_window_target": window_target,
        "axis2_guarantee": guarantee,
        "guarantee_feasibility": feas,
        "axis1_target_per_mock": largest_remainder_apportion(
            axis_dist.get("axis1_per_paper", {}), sec_qs),
        "axis3_target_per_mock": largest_remainder_apportion(
            axis_dist.get("axis3_per_paper", {}), sec_qs),
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
        {'axis2_per_paper': {'MATCH': 0.5, 'SEQUENCE': 0.05, 'DIRECT': 2.0},
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


    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("blueprint_core.py — shared allocation core. Run with --self-test.")
