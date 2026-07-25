"""
Syllabus Provenance Builder — Framework_PYQAnalyse S2-3e (Issue C fix)

TWO defects addressed:
  C   EMISSION BURDEN — 9 fields x N items emitted by prose-following.
      Fix: emit 4 fields, DERIVE the other 5 deterministically.
  C-1 DELIMITER AMBIGUITY — paths were '/'-joined strings, but real subject
      names contain '/' (e.g. "Microbial/Plant/Animal Biotech"). Any
      string-encoded path is unparseable in general.
      Fix: paths are LISTS OF COMPONENTS. Never parsed, never split.
"""
import re, unicodedata

DASHES = dict.fromkeys(map(ord, "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"), "-")
PATH_ARITY = 3          # Subject / Topic / Subtopic
VALID_RULES = {"TOPIC_INTEGRITY_TEST", "SPLIT", "MERGE", "OTHER"}


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

def build_items(emissions, group_topic_map=None, start=1):
    """
    emissions: [{'path':[...], 'text':str, 'to':[[...]], 'why':str|None}]
    Returns (items, errors). Derives 5 of the 9 fields deterministically.
    """
    errors = []
    gmap = {}
    for g in (group_topic_map or []):
        key = (norm(g.get("subject")), norm(g.get("group")))
        gmap[key] = {tuple(norm_path(t)) for t in (g.get("mapped_topics") or [])}

    items = []
    for n, e in enumerate(emissions or [], start):
        iid = f"SYL-{n:03d}"                       # DERIVED: never mis-emitted
        path = e.get("path") or []
        if not isinstance(path, (list, tuple)) or not path:
            errors.append(f"{iid}: 'path' must be a non-empty list of headings")
            continue
        subject = path[0]                          # DERIVED
        group = path[1] if len(path) > 1 else None # DERIVED
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
        items.append({
            "id": iid,
            "subject": subject,
            "syllabus_path": list(path),
            "syllabus_group": group,
            "raw_text": str(e.get("text") or "").strip(),
            "enumerated": bool(e.get("enumerated", True)),
            "source_ref": e.get("source_ref"),
            "mapped_paths": clean,
            "deviation": deviation,
        })
        if not items[-1]["raw_text"]:
            errors.append(f"{iid}: 'text' is empty")
    return items, errors


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
        if not it.get("mapped_paths"):
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
