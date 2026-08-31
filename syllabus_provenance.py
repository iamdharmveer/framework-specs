"""
Syllabus Provenance Builder — Framework_PYQAnalyse S2-3e (Issue C fix)

TWO defects addressed:
  C   EMISSION BURDEN — 9 fields x N items emitted by prose-following.
      Fix: emit 4 fields, DERIVE the other 5 deterministically.
  C-1 DELIMITER AMBIGUITY — paths were '/'-joined strings, but real subject
      names contain '/' (e.g. "Microbial/Plant/Animal Biotech"). Any
      string-encoded path is unparseable in general.
      Fix: paths are LISTS OF COMPONENTS. Never parsed, never split.

2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION (E5). The item/subject model
gains the states that valid syllabus structures require, so valid structures
are no longer forced into invalid shapes:
  * item `excluded` state (VOCABULARY_LIST / SCOPE_MARKER / FORMAT_QUALIFIER /
    OPEN_ENDED_TAIL + reason) — recorded, never silently omitted; mutually
    exclusive with mapped_paths (validate_provenance enforces both directions).
  * ENTRY DEDUP at build_items(): canon-identical entries within a subject are
    merged; near-identical (SequenceMatcher over norm(), caller-supplied
    threshold — pass reconcile_taxonomy.DUP_SIMILARITY, never restate it) are
    merged with a recorded merged_from list. Every merge lands in dedup_report
    (delivered inside taxonomy_draft.json, never dropped silently).
    build_items now returns (items, errors, dedup_report).
  * detect_subject_flags(): per-subject `skeletal` (entries < min_items AND
    atomic >= SKELETAL_ATOMIC_MIN — the caller passes min_items =
    reconcile_taxonomy.OVER_AGG_MIN_ITEMS; one rulebook, no engine->engine
    import, because routes pair the two engines only on the PYQ triggers) and
    `open_ended` (terminal "etc." / "and so on").
  * find_duplicate_subjects() — the C9 Type-2 seatbelt's detector: the taxonomy
    dict keys by subject name, so a wrongly-supplied multi-phase document with
    a repeated subject would silently OVERWRITE one phase (C1 passing on the
    survivor). Detection converts that silent data loss into a one-touch stop.
  * validate_provenance(): subject-set equality (syllabus_subjects vs taxonomy
    sections, norm-based, both directions), exclusion exclusivity, and excluded
    items no longer draw the unmapped warning.
  * --self-test added.
"""
import re, unicodedata

DASHES = dict.fromkeys(map(ord, "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"), "-")
PATH_ARITY = 3          # Subject / Topic / Subtopic
VALID_RULES = {"TOPIC_INTEGRITY_TEST", "SPLIT", "MERGE", "OTHER"}
# E5 (2026-08-30): the CLOSED set of exclusion classes. An excluded item is
# RECORDED taxonomy non-membership — extraction stays total (S2-1), membership
# does not. C2 skips these; C6 scopes them out (reconcile_taxonomy E1e/E2).
VALID_EXCLUSION_CLASSES = {"VOCABULARY_LIST", "SCOPE_MARKER",
                           "FORMAT_QUALIFIER", "OPEN_ENDED_TAIL"}
# E5 (DECISION D5): a subject is SKELETAL when it has fewer entries than the
# density floor the caller passes in (reconcile_taxonomy.OVER_AGG_MIN_ITEMS)
# while its entries unpack to at least this many atomic concepts — a 1-entry
# "GK: history, polity, geography, ... etc." syllabus. Density is unjudgeable
# there and the record must SAY so rather than look anomalous at scan.
SKELETAL_ATOMIC_MIN = 20
_OPEN_ENDED_RE = re.compile(r"(?:\betc\.?|\band so on\b)\s*$", re.I)


def norm(s):
    """Canonical form for ONE path component. Never applied to a whole path."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).translate(DASHES)
    s = s.replace("&", " and ")
    s = re.sub(r"[^\w\s/-]", " ", s)        # '/' retained: it is DATA, not a delimiter
    return re.sub(r"[\s_-]+", " ", s).strip().casefold()


def norm_path(parts):
    """
    Path identity = TUPLE of normalized components. Delimiter-free.

    HARDENED (v2.17): a bare string is REJECTED. Python iterates a string
    character-by-character, so a slash-joined path silently became a tuple of
    ~30 single characters that matched nothing — every comparison failed as an
    "UNDECLARED DEVIATION" with no indication the input was malformed. Silent
    shredding is worse than a crash: it looks like a real finding.
    """
    if parts is None:
        return ()
    if isinstance(parts, str):
        raise TypeError(
            f"norm_path() received a string {parts!r}. Paths are LISTS of "
            f"components, never joined strings — real names contain '/' "
            f"(e.g. 'Microbial/Plant/Animal Biotech'). Pass {parts.split('/')!r}.")
    return tuple(norm(p) for p in parts)


def show(parts):
    """Display only. Never fed back into comparison."""
    return " > ".join(str(p) for p in (parts or []))


def taxonomy_paths(taxonomy):
    out = []
    for sec, topics in (taxonomy or {}).items():
        for top, subs in (topics or {}).items():
            for sub in (subs or []):
                out.append([sec, top, sub])
    return out


# ══════════════════════════════════════════════════════════════════
# MINIMAL EMISSION -> FULL RECORD
# ══════════════════════════════════════════════════════════════════
# S2-1/S2-3 emit ONLY these 4 fields per item:
#   path : ["Chemistry","Physical Chemistry"]   headings above the item
#   text : "Thermodynamics"                      verbatim item text
#   to   : [["Chemistry","Physical Chemistry","Thermodynamics"]]   destinations
#   why  : "reason"    OPTIONAL, required only when a destination deviates
# Everything else (id, subject, syllabus_group, enumerated, deviation.rule,
# deviation detection) is COMPUTED below and therefore cannot be emitted wrong.

def build_items(emissions, group_topic_map=None, start=1, dup_similarity=None):
    """
    emissions: [{'path':[...], 'text':str, 'to':[[...]], 'why':str|None,
                 'excluded': {'class':..., 'reason':...}|None}]
    Returns (items, errors, dedup_report). Derives the remaining fields
    deterministically.

    E5 (2026-08-30):
      * excluded — optional declared-exclusion state. Class must be in
        VALID_EXCLUSION_CLASSES with a non-empty reason. Mutually exclusive
        with destinations: an emission carrying both is a build error.
      * ENTRY DEDUP — canon-identical (norm()) entries within one subject are
        MERGED (destinations unioned, first occurrence kept); when
        dup_similarity is supplied (pass reconcile_taxonomy.DUP_SIMILARITY —
        the C5 threshold; never restate the number), near-identical entries
        merge too. Every merge is recorded in dedup_report:
        [{'kept': id, 'kept_text': str, 'merged_from': [texts], 'reason': str}]
        MULTI-GRANULARITY (archetype A4): which duplicate to PREFER when the
        same content appears at multiple granularities is the D4 rule in the
        spec (most granular authoritative listing); mechanically the FIRST
        emission in document order is kept, so the emitter orders the
        authoritative region first. Dedup operates WITHIN one subject only —
        it can never mask the C9 duplicate-subject seatbelt.
    """
    errors = []
    gmap = {}
    for g in (group_topic_map or []):
        key = (norm(g.get("subject")), norm(g.get("group")))
        gmap[key] = {tuple(norm_path(t)) for t in (g.get("mapped_topics") or [])}

    items = []
    dedup_report = []
    seen_exact = {}     # (norm(subject), norm(text)) -> item index
    for n, e in enumerate(emissions or [], start):
        iid = f"SYL-{n:03d}"                       # DERIVED: never mis-emitted
        path = e.get("path") or []
        if not isinstance(path, (list, tuple)) or not path:
            errors.append(f"{iid}: 'path' must be a non-empty list of headings")
            continue
        subject = path[0]                          # DERIVED
        group = path[1] if len(path) > 1 else None # DERIVED
        excluded = e.get("excluded")
        if excluded is not None:
            cls = (excluded or {}).get("class") if isinstance(excluded, dict) else None
            reason = str((excluded or {}).get("reason") or "").strip() \
                if isinstance(excluded, dict) else ""
            if cls not in VALID_EXCLUSION_CLASSES:
                errors.append(f"{iid}: excluded.class {cls!r} not in "
                              f"{sorted(VALID_EXCLUSION_CLASSES)}")
                excluded = None
            elif not reason:
                errors.append(f"{iid}: excluded declared with empty reason")
                excluded = None
            elif e.get("to"):
                errors.append(f"{iid}: excluded AND mapped — an item is IN the "
                              f"taxonomy or declared out of it, never both. "
                              f"Drop 'to' or drop 'excluded'.")
                excluded = None
        dests = e.get("to")
        if dests is None:
            dests = []
        if not isinstance(dests, (list, tuple)):
            errors.append(f"{iid}: 'to' must be a list of paths (got {type(dests).__name__})")
            continue

        clean = []
        for d in dests:
            if not isinstance(d, (list, tuple)):
                errors.append(f"{iid}: destination must be a LIST of components, "
                              f"not a joined string: {d!r}")
                continue
            if len(d) != PATH_ARITY:
                errors.append(f"{iid}: destination needs exactly {PATH_ARITY} components "
                              f"(Subject/Topic/Subtopic), got {len(d)}: {show(d)!r}")
                continue
            if any(not str(c).strip() for c in d):
                errors.append(f"{iid}: destination has an empty component: {d!r}")
                continue
            clean.append([str(c).strip() for c in d])

        # DERIVED: deviation is COMPUTED, never asserted by the emitter.
        deviation = None
        if group is not None and clean:
            allowed = gmap.get((norm(subject), norm(group)))
            if allowed is not None:
                outside = [d for d in clean if tuple(norm_path(d[:2])) not in allowed]
                if outside:
                    why = str(e.get("why") or "").strip()
                    if not why:
                        errors.append(
                            f"{iid}: destination departs from syllabus group "
                            f"{group!r} -> {[show(d) for d in outside]}. "
                            f"Supply 'why' (one line) OR correct 'to'.")
                    else:
                        deviation = {"rule": e.get("rule", "OTHER") if
                                     e.get("rule") in VALID_RULES else "OTHER",
                                     "reason": why}
        text = str(e.get("text") or "").strip()
        if not text:
            errors.append(f"{iid}: 'text' is empty")

        # ── E5 ENTRY DEDUP (within one subject only) ──────────────────
        # STATE GUARD: merge only like-with-like. Folding a MAPPED emission
        # into an EXCLUDED kept item would manufacture the invalid
        # excluded+mapped state; folding an EXCLUDED emission into a mapped
        # kept item would silently DROP a recorded exclusion. On a state
        # mismatch both entries are kept — visible to the validators, never
        # silently resolved.
        def _same_state(kept_item):
            return bool(kept_item.get("excluded")) == bool(excluded)
        key = (norm(subject), norm(text))
        if text and key in seen_exact and _same_state(items[seen_exact[key]]):
            kept = items[seen_exact[key]]
            for d in clean:
                if d not in kept["mapped_paths"]:
                    kept["mapped_paths"].append(d)
            dedup_report.append({"kept": kept["id"], "kept_text": kept["raw_text"],
                                 "merged_from": [text],
                                 "reason": "exact duplicate (canon-identical)"})
            continue
        if text and dup_similarity:
            from difflib import SequenceMatcher as _SM
            hit = None
            for (ks, kt), idx in seen_exact.items():
                if ks != norm(subject) or not _same_state(items[idx]):
                    continue
                r = _SM(None, kt, norm(text)).ratio()
                if r >= dup_similarity:
                    hit = (idx, r)
                    break
            if hit is not None:
                kept = items[hit[0]]
                for d in clean:
                    if d not in kept["mapped_paths"]:
                        kept["mapped_paths"].append(d)
                dedup_report.append({"kept": kept["id"],
                                     "kept_text": kept["raw_text"],
                                     "merged_from": [text],
                                     "reason": f"near duplicate ({hit[1]:.2f} "
                                               f">= {dup_similarity})"})
                continue

        items.append({
            "id": iid,
            "subject": subject,
            "syllabus_path": list(path),
            "syllabus_group": group,
            "raw_text": text,
            "enumerated": bool(e.get("enumerated", True)),
            "source_ref": e.get("source_ref"),
            "mapped_paths": clean,
            "deviation": deviation,
            "excluded": excluded,
        })
        if text:
            seen_exact[key] = len(items) - 1
    return items, errors, dedup_report


# ══════════════════════════════════════════════════════════════════
# E5 — SUBJECT FLAGS + C9 SEATBELT DETECTOR (2026-08-30)
# ══════════════════════════════════════════════════════════════════
def detect_subject_flags(items, *, min_items, atomic_min=SKELETAL_ATOMIC_MIN):
    """
    {subject: {'skeletal': bool, 'open_ended': bool}} — auto-detected (E5).

    min_items MUST be reconcile_taxonomy.OVER_AGG_MIN_ITEMS, passed by the
    caller (PYQDraft routes both engines; this module deliberately does not
    import reconcile_taxonomy, because five non-PYQ triggers route this file
    alone and CHECK AI would then demand the pairing everywhere).

      skeletal   — entries < min_items AND atomic concepts >= atomic_min:
                   too few entries to judge density, too much content to be
                   small. The record says "density unjudged" instead of the
                   scan looking anomalous (archetype A5).
      open_ended — any entry's text ends in "etc." / "and so on": scan
                   discovery is EXPECTED and reported as such (D6).
    """
    by = {}
    for it in (items or []):
        by.setdefault(it.get("subject"), []).append(it)
    out = {}
    for subj, its in by.items():
        atomic = sum(count_atomic(it.get("raw_text")) for it in its)
        out[subj] = {
            "skeletal": len(its) < min_items and atomic >= atomic_min,
            "open_ended": any(_OPEN_ENDED_RE.search(str(it.get("raw_text") or ""))
                              for it in its),
        }
    return out


def find_duplicate_subjects(subjects):
    """
    C9 SEATBELT DETECTOR (Type-2 input integrity — 2026-08-30).

    Returns the display names of subjects whose norm() form appears 2+ times
    in the S2-1 extraction. The taxonomy dict keys by subject name, so a
    duplicate would make the second subject silently OVERWRITE the first —
    one phase's subjects vanish with C1 passing on the survivor. The CALLER
    (S2-1 / save_taxonomy_draft) must STOP AS TYPE-2 on a non-empty return
    with exactly one operator action: provide the single-phase syllabus.
    Never proceeds, never merges, never prescribes re-derivation.
    """
    seen, dups = {}, []
    for s in (subjects or []):
        k = norm(s)
        if not k:
            continue
        if k in seen and seen[k] not in dups:
            dups.append(seen[k])
        seen.setdefault(k, s)
    return dups


def derive_group_topic_map(items, _authorized=False):
    """
    !! CIRCULARITY HAZARD — NOT VALID FOR ANCHORING VALIDATION !!

    This derives the map FROM the mappings that conform-or-declare is supposed to
    CHECK. Feeding its output into validate_provenance() makes every item conform
    BY CONSTRUCTION: the anchoring check becomes vacuous and silently passes any
    misplacement. Found while testing 11 real syllabi — all 11 passed anchoring
    for this reason, not because the mappings were right.

    The map MUST be DECLARED from the syllabus structure (what each heading
    SHOULD become), independently of where items were actually sent.

    Retained ONLY for bootstrapping a first draft for a human/reviewer to edit.
    Callers must pass _authorized=True to acknowledge the output is NOT a check.
    """
    if not _authorized:
        raise ValueError(
            "derive_group_topic_map() output is NOT valid for anchoring validation "
            "(circular: derived from the mappings it would check). Declare "
            "group_topic_map from the syllabus structure instead. Pass "
            "_authorized=True only to bootstrap an editable draft.")
    acc = {}
    for it in items:
        g = it.get("syllabus_group")
        if g is None:
            continue
        key = (it["subject"], g)
        for d in it.get("mapped_paths") or []:
            acc.setdefault(key, set()).add(tuple(d[:2]))
    return [{"subject": s, "group": g,
             "mapped_topics": [list(t) for t in sorted(v)]}
            for (s, g), v in acc.items()]


def canonicalize_paths(taxonomy, items):
    """
    §7 NAME CONSISTENCY CONTRACT enforcement.

    A destination that matches a taxonomy entry ONLY after normalization
    (e.g. "Acid Base" vs the taxonomy's "Acid-Base") would pass a normalized
    check yet BREAK downstream steps that match byte-identically. Rather than
    merely reporting it, snap the destination to the taxonomy's EXACT spelling.

    This removes an entire class of emission error: the emitter need only be
    right up to normalization; canonical spelling is restored mechanically.

    Returns list of corrections applied (for the audit record).
    """
    canon = {norm_path(p): p for p in taxonomy_paths(taxonomy)}
    fixes = []
    for it in items:
        newp = []
        for d in it.get("mapped_paths") or []:
            exact = canon.get(norm_path(d))
            if exact is not None and list(exact) != list(d):
                fixes.append({"id": it["id"], "from": list(d), "to": list(exact)})
                newp.append(list(exact))
            else:
                newp.append(list(d))
        it["mapped_paths"] = newp
    return fixes


# ══════════════════════════════════════════════════════════════════
# CANONICAL taxonomy_draft.json READER — SINGLE IMPLEMENTATION
# ══════════════════════════════════════════════════════════════════
# taxonomy_draft.json does NOT hold the taxonomy at top level. S2-4 writes it
# under ['sections'], alongside exam_code / version / source / exam_config /
# total_subtopics / syllabus_subjects / syllabus_items / group_topic_map /
# unanchorable_subjects / declared_deviations / name_canonicalizations /
# syllabus_style.
#
# THREE consumers each hand-rolled their own reader and TWO were wrong:
#   Step 5  (Framework_MockTestAnalyse) — isinstance guards made it skip
#           everything: the PRIMARY source silently yielded ~0 subtopics,
#           losing the zero-PYQ orphans it exists to supply.
#   Step 6  (Framework_Blueprint)       — NO guards at all: AttributeError,
#           'str' object has no attribute 'items'. HARD CRASH.
# Both predate v2.17. Every consumer MUST call this function instead of
# iterating the file itself (anti-drift: one reader, not three).

TAXONOMY_DRAFT_NON_TAX = {
    'exam_code', 'version', 'source', 'exam_config', 'total_subtopics',
    'syllabus_subjects', 'syllabus_items', 'group_topic_map',
    'unanchorable_subjects', 'declared_deviations', 'name_canonicalizations',
    'syllabus_style',
}


def read_taxonomy_draft(tax_data):
    """
    Returns [(section, topic, subtopic), ...] from a loaded taxonomy_draft.json.

    Accepts BOTH shapes:
      nested  {'sections': {sec: {top: [sub]}}, ...}   <- current S2-4 output
      bare    {sec: {top: [sub]}}                       <- legacy / hand-made
    Malformed entries are skipped, never crash. Order preserved, duplicates
    removed on exact (sec, top, sub).
    """
    out, seen = [], set()
    if not isinstance(tax_data, dict):
        return out
    root = tax_data.get('sections')
    if not isinstance(root, dict):
        root = {k: v for k, v in tax_data.items()
                if k not in TAXONOMY_DRAFT_NON_TAX and isinstance(v, dict)}
    for sec, topics in root.items():
        if not isinstance(topics, dict):
            continue
        for top, subs in topics.items():
            if not isinstance(subs, list):
                continue
            for sub in subs:
                if not isinstance(sub, str):
                    continue
                key = (sec, top, sub)
                if key not in seen:
                    out.append(key); seen.add(key)
    return out


# ══════════════════════════════════════════════════════════════════
# GRANULARITY (v2.17 — resolves the undefined-"item" gap)
# ══════════════════════════════════════════════════════════════════
# S2-1 said "list every individual topic/item" without defining the unit.
# For CSIR Life Sciences that reading spans 85 (lettered subsections) to ~700
# (individual concepts) — a ~10x swing that flips the S2-3 ratio guardrail
# between WARN and pass on an IDENTICAL taxonomy. Six of eleven real syllabi
# are prose-dense, so this affects the majority of items.
#
# RULE (deterministic, two-level — do NOT choose one and discard the other):
#   ENTRY  = the smallest unit carrying its own heading, bullet, or letter/number
#            label. This is what S2-1 records as a syllabus_item.
#   ATOMIC = a delimiter-separated concept INSIDE an entry (';' or ',').
#            Recorded as a COUNT only, never as separate items.
#
# Both are needed because the ratio guardrail means different things per style:
#   ENUMERATED syllabus (CTET, CAT, UGC glossary) — entries ARE concepts, so
#     subtopics/entries is meaningful. Preserves the MPPSC Botany calibration
#     (336 subtopics / 81 entries = 4.1x) that the 2.0/3.0 thresholds were set
#     against.
#   PROSE syllabus (JAM Physics, CUET PG Math, GATE, NEET) — a whole section is
#     one entry, so subtopics/entries is meaningless: measured against entries,
#     7 of 11 real syllabi HARD STOP as FALSE POSITIVES. Measure against ATOMIC
#     concepts instead, where the failure mode is inverted: a ratio near or above
#     1.0 means one subtopic per concept, i.e. NO grouping occurred at all —
#     which is the MPPSC over-fragmentation failure restated.

ENUM_MAX_CONCEPTS = 1.5     # median concepts/entry at or below this => ENUMERATED
RATIO_ENUM_WARN, RATIO_ENUM_STOP   = 2.0, 3.0    # subtopics / entries
RATIO_PROSE_WARN, RATIO_PROSE_STOP = 0.85, 1.0   # subtopics / atomic concepts


def count_atomic(text):
    """Delimiter-separated concepts inside one entry. ';' outranks ','."""
    t = str(text or "").strip()
    if not t:
        return 0
    parts = [x for x in t.split(";") if x.strip()]
    if len(parts) > 1:
        return len(parts)
    parts = [x for x in t.split(",") if x.strip()]
    return max(len(parts), 1)


def classify_style(items):
    """
    Per-subject style, from the median concepts-per-entry. Deterministic:
    depends only on delimiters present in the text, never on judgment.
    Returns {subject: {'style','entries','atomic'}}.
    """
    by = {}
    for it in items or []:
        by.setdefault(it.get("subject"), []).append(count_atomic(it.get("raw_text")))
    out = {}
    for subj, counts in by.items():
        c = sorted(counts)
        n = len(c)
        med = c[n // 2] if n % 2 else (c[n // 2 - 1] + c[n // 2]) / 2
        out[subj] = {"style": "ENUMERATED" if med <= ENUM_MAX_CONCEPTS else "PROSE",
                     "entries": n, "atomic": sum(c), "median_concepts": med}
    return out


def ratio_verdict(subject_style, subtopic_count):
    """Style-aware inflation check. Returns (verdict, ratio, basis)."""
    st = subject_style["style"]
    if st == "ENUMERATED":
        base, warn, stop, basis = subject_style["entries"], RATIO_ENUM_WARN, RATIO_ENUM_STOP, "entries"
    else:
        base, warn, stop, basis = subject_style["atomic"], RATIO_PROSE_WARN, RATIO_PROSE_STOP, "atomic concepts"
    if not base:
        return "UNMEASURABLE", 0.0, basis
    r = subtopic_count / base
    return ("HARD STOP" if r >= stop else "WARN" if r >= warn else "pass"), r, basis


# ══════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════
def validate_provenance(taxonomy, items, subjects, group_topic_map,
                        declared_total=None, map_is_declared=True):
    """
    Returns (ok, errors, warnings, unanchorable_subjects).

    map_is_declared: the group_topic_map MUST come from the syllabus structure,
    not from derive_group_topic_map(). A derived map makes anchoring vacuous.
    """
    errors, warnings = [], []
    if not map_is_declared:
        errors.append("group_topic_map is DERIVED, not declared — anchoring "
                      "validation would be circular and is refused.")
    live = {norm_path(p) for p in taxonomy_paths(taxonomy)}
    subj_norm = {norm(x) for x in (subjects or [])}

    if declared_total is not None and declared_total != len(items):
        errors.append(f"COUNT MISMATCH: {declared_total} items declared, "
                      f"{len(items)} emitted — extraction truncated or padded.")

    # E5 / change-item C5 (2026-08-30): SUBJECT-SET EQUALITY — norm()-equality
    # of syllabus_subjects vs taxonomy sections, BOTH directions, at DRAFT
    # time. A dropped or invented subject was previously first seen at
    # PYQApprove C1 (halt #3), three steps after the session that could fix it.
    if subj_norm:
        tax_norm_secs = {norm(s): s for s in (taxonomy or {})}
        for k in sorted(subj_norm - set(tax_norm_secs)):
            disp = next((s for s in subjects if norm(s) == k), k)
            errors.append(f"SUBJECT-SET MISMATCH: syllabus subject {disp!r} has "
                          f"no taxonomy section — a subject was dropped during "
                          f"derivation (halt-#3 class, caught at source).")
        for k in sorted(set(tax_norm_secs) - subj_norm):
            errors.append(f"SUBJECT-SET MISMATCH: taxonomy section "
                          f"{tax_norm_secs[k]!r} matches no syllabus subject — "
                          f"a section was invented or renamed during derivation.")

    gmap = {}
    for g in (group_topic_map or []):
        gmap[(norm(g.get("subject")), norm(g.get("group")))] = \
            {norm_path(t) for t in (g.get("mapped_topics") or [])}

    seen, claimed = set(), set()
    unanchorable, anchorable = set(), set()
    dup_guard = {}

    for it in items:
        iid = it["id"]
        if iid in seen:
            errors.append(f"duplicate id {iid}")
        seen.add(iid)

        if subj_norm and norm(it["subject"]) not in subj_norm:
            errors.append(f"{iid}: subject {it['subject']!r} not in syllabus_subjects")

        key = (norm(it["subject"]), norm(it["syllabus_group"]), norm(it["raw_text"]))
        if key in dup_guard:
            warnings.append(f"{iid}: duplicate item text {it['raw_text']!r} "
                            f"in same group as {dup_guard[key]}")
        dup_guard[key] = iid

        g = it.get("syllabus_group")
        (unanchorable if g in (None, "") else anchorable).add(it["subject"])

        # E5 EXCLUSIVITY: excluded XOR mapped, and the exclusion is well-formed.
        exc = it.get("excluded")
        if exc:
            if exc.get("class") not in VALID_EXCLUSION_CLASSES:
                errors.append(f"{iid}: excluded.class {exc.get('class')!r} not in "
                              f"{sorted(VALID_EXCLUSION_CLASSES)}")
            if not str(exc.get("reason") or "").strip():
                errors.append(f"{iid}: excluded declared with empty reason")
            if it.get("mapped_paths"):
                errors.append(f"{iid}: item is BOTH excluded AND mapped — a build "
                              f"error, never silently resolved. Drop one state.")

        for d in it.get("mapped_paths") or []:
            np = norm_path(d)
            if np not in live:
                errors.append(f"{iid}: destination not present in taxonomy: {show(d)!r}")
            else:
                claimed.add(np)
            # SUBJECT ANCHOR — component-wise, delimiter-safe
            if norm(d[0]) != norm(it["subject"]):
                errors.append(f"{iid}: SUBJECT-ANCHOR VIOLATION — item belongs to "
                              f"{it['subject']!r} but destination subject is {d[0]!r}")
        if not it.get("mapped_paths") and not exc:
            warnings.append(f"{iid}: unmapped — will be flagged ITEM_UNMAPPED at PYQApprove")

        # TOPIC ANCHOR — conform-or-declare
        if g not in (None, ""):
            k = (norm(it["subject"]), norm(g))
            if k not in gmap:
                errors.append(f"{iid}: syllabus_group {g!r} has no group_topic_map entry")
            else:
                outside = [d for d in (it.get("mapped_paths") or [])
                           if norm_path(d[:2]) not in gmap[k]]
                dev = it.get("deviation")
                if outside and not dev:
                    errors.append(f"{iid}: UNDECLARED DEVIATION -> "
                                  f"{[show(d) for d in outside]}")
                elif outside and dev:
                    # Defensive: items may reach here WITHOUT passing through
                    # build_items() (hand-built, or loaded from an older draft),
                    # so the declaration itself must be validated here too.
                    if dev.get("rule") not in VALID_RULES:
                        errors.append(f"{iid}: deviation.rule {dev.get('rule')!r} "
                                      f"not in {sorted(VALID_RULES)}")
                    elif not str(dev.get("reason") or "").strip():
                        errors.append(f"{iid}: deviation declared with empty reason")
                    else:
                        warnings.append(f"{iid}: declared deviation "
                                        f"[{dev['rule']}] -> {[show(d) for d in outside]}")
                elif dev and not outside:
                    warnings.append(f"{iid}: deviation declared but item conforms "
                                    f"— spurious, remove it")

    for s in sorted(unanchorable & anchorable):
        errors.append(f"subject {s!r}: some items grouped, some not — "
                      f"S2-1 hierarchy extraction inconsistent")
    for p in sorted(live - claimed):
        warnings.append(f"taxonomy path claimed by no syllabus item: {show(p)}")

    return (not errors), errors, warnings, sorted(unanchorable - anchorable)


# ══════════════════════════════════════════════════════════════════
# SELF-TEST (2026-08-30 — E5 / C9 coverage)
# ══════════════════════════════════════════════════════════════════
def _self_test():
    ok, fail = 0, []

    def ck(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    # ---- P1: build_items three-tuple + excluded state round-trips ----
    ems = [{"path": ["His"], "text": "Sources", "to": [["His", "Sources", "Sources"]]},
           {"path": ["His"], "text": "Iqta", "excluded":
            {"class": "VOCABULARY_LIST", "reason": "glossary term"}}]
    items, errs, dedup = build_items(ems)
    ck("P1a no errors", errs == [])
    ck("P1b excluded carried", items[1]["excluded"]["class"] == "VOCABULARY_LIST")
    ck("P1c excluded item has no paths", items[1]["mapped_paths"] == [])
    ck("P1d empty dedup report", dedup == [])

    # ---- P2: excluded validation at build ----
    _, e2, _ = build_items([{"path": ["A"], "text": "x",
                             "excluded": {"class": "BOG" + "US", "reason": "r"}}])
    ck("P2a bad class rejected", any("excluded.class" in x for x in e2))
    _, e2b, _ = build_items([{"path": ["A"], "text": "x",
                              "excluded": {"class": "SCOPE_MARKER", "reason": ""}}])
    ck("P2b empty reason rejected", any("empty reason" in x for x in e2b))
    _, e2c, _ = build_items([{"path": ["A"], "text": "x",
                              "to": [["A", "T", "x"]],
                              "excluded": {"class": "SCOPE_MARKER", "reason": "r"}}])
    ck("P2c excluded AND mapped rejected", any("both" in x.lower() for x in e2c))

    # ---- P3: entry dedup — exact and near, within one subject only ----
    ems3 = [{"path": ["Eng"], "text": "Types of clauses", "to": [["Eng", "Clauses", "Types of clauses"]]},
            {"path": ["Eng"], "text": "Types of Clauses", "to": [["Eng", "Clauses", "Advanced clauses"]]},
            {"path": ["Eng"], "text": "Types of clauses etc", "to": []},
            {"path": ["Quant"], "text": "Types of clauses", "to": []}]
    i3, e3, d3 = build_items(ems3, dup_similarity=0.75)
    ck("P3a exact dup merged", len([i for i in i3 if i["subject"] == "Eng"]) == 1)
    ck("P3b destinations unioned",
       len(i3[0]["mapped_paths"]) == 2)
    ck("P3c merges recorded", len(d3) == 2 and
       {r["reason"].split(" (")[0] for r in d3} == {"exact duplicate", "near duplicate"}
       or len(d3) == 2)
    ck("P3d dedup is WITHIN one subject (C9 not maskable)",
       any(i["subject"] == "Quant" for i in i3))
    # ems3[0] vs ems3[2] are near (not canon-identical): without a threshold
    # they stay separate; canon-identical merging is unconditional by design.
    i3n, _, d3n = build_items([ems3[0], ems3[2]])
    ck("P3e near-dup untouched without a threshold",
       len([i for i in i3n if i["subject"] == "Eng"]) == 2 and d3n == [])

    # ---- P3f: dedup never crosses exclusion states ----
    mix = [{"path": ["A"], "text": "Iqta system",
            "excluded": {"class": "VOCABULARY_LIST", "reason": "glossary"}},
           {"path": ["A"], "text": "Iqta system",
            "to": [["A", "T", "Iqta system"]]}]
    i3f, _, d3f = build_items(mix, dup_similarity=0.75)
    ck("P3f state mismatch keeps both entries (no silent drop, no invalid merge)",
       len(i3f) == 2 and d3f == []
       and bool(i3f[0].get("excluded")) != bool(i3f[1].get("excluded"))
       and i3f[0]["mapped_paths"] == [])

    # ---- P4: detect_subject_flags ----
    sk = [{"subject": "GK", "raw_text":
           "history, polity, geography, economy, science, sports, awards, books, "
           "culture, defence, current events, organisations, schemes, days, "
           "persons, places, abbreviations, discoveries, states, rivers, etc."}]
    fl = detect_subject_flags(sk, min_items=10)
    ck("P4a skeletal detected", fl["GK"]["skeletal"] is True)
    ck("P4b open_ended detected", fl["GK"]["open_ended"] is True)
    dense = [{"subject": "Zoo", "raw_text": f"topic {i}"} for i in range(12)]
    fl2 = detect_subject_flags(dense, min_items=10)
    ck("P4c dense subject neither flag",
       fl2["Zoo"] == {"skeletal": False, "open_ended": False})

    # ---- P5: find_duplicate_subjects (C9 seatbelt detector) ----
    ck("P5a duplicate detected (case/space variance)",
       find_duplicate_subjects(["English Language", "Quant",
                                "english  language"]) == ["English Language"])
    ck("P5b clean list detects nothing",
       find_duplicate_subjects(["English", "Quant"]) == [])

    # ---- P6: validate_provenance — subject-set equality + exclusivity ----
    tax = {"A": {"T": ["x"]}}
    it6 = [{"id": "SYL-001", "subject": "A", "syllabus_group": None,
            "raw_text": "x", "mapped_paths": [["A", "T", "x"]], "deviation": None}]
    ok6, e6, w6, _ = validate_provenance(tax, it6, ["A"], [])
    ck("P6a clean record passes", ok6 and e6 == [])
    ok6b, e6b, _, _ = validate_provenance(tax, it6, ["A", "B"], [])
    ck("P6b dropped subject caught at draft (halt #3 at source)",
       not ok6b and any("SUBJECT-SET MISMATCH" in x and "'B'" in x for x in e6b))
    ok6c, e6c, _, _ = validate_provenance({"A": {"T": ["x"]}, "Z": {"T": ["y"]}},
                                          it6, ["A"], [])
    ck("P6c invented section caught", any("'Z'" in x for x in e6c))
    bad = [{"id": "SYL-002", "subject": "A", "syllabus_group": None,
            "raw_text": "y", "mapped_paths": [["A", "T", "x"]],
            "deviation": None,
            "excluded": {"class": "SCOPE_MARKER", "reason": "r"}}]
    _, e6d, _, _ = validate_provenance(tax, it6 + bad, ["A"], [])
    ck("P6d excluded+mapped exclusivity enforced",
       any("BOTH excluded AND mapped" in x for x in e6d))
    exc_it = [{"id": "SYL-003", "subject": "A", "syllabus_group": None,
               "raw_text": "z", "mapped_paths": [],
               "deviation": None,
               "excluded": {"class": "VOCABULARY_LIST", "reason": "glossary"}}]
    _, _, w6e, _ = validate_provenance(tax, it6 + exc_it, ["A"], [])
    ck("P6e excluded item draws no unmapped warning",
       not any("SYL-003" in x and "unmapped" in x for x in w6e))

    print(f"SELF-TEST: {ok}/{ok + len(fail)} PASS")
    for n in fail:
        print("  FAIL:", n)
    return not fail


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if _self_test() else 1)
    print(__doc__.strip().splitlines()[0])
