"""
Taxonomy Reconciliation Engine — Framework_PYQAnalyse S4-0
Exam-agnostic. Zero hardcoded exam/section/subtopic names.

Converts the PYQApprove human quiz into a deterministic 3-tier verdict:
  Tier 0 — machine reconciliation (no judgment)
  Tier 1 — codified auto-policy (no judgment)
  Tier 2 — evidence-bound adjudication, replayed from prior record
"""
import json, re, hashlib, unicodedata
from difflib import SequenceMatcher

MIN_PATTERN_SIZE = 3      # MUST match S3-6 refinement threshold
RATIO_WARN       = 2.0    # S2-3 guardrail
RATIO_HARDSTOP   = 3.0    # S2-3 guardrail
DUP_SIMILARITY   = 0.75   # S4-4 near-duplicate threshold
OVER_AGG_TOPICS  = 4      # S2-3: <=4 topics with >=10 syllabus items => over-aggregated
OVER_AGG_ITEMS   = 10

DASHES = dict.fromkeys(map(ord, "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"), "-")


def normalize_label(s):
    """Canonical comparison form. Exam-agnostic, lossless of meaning."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).translate(DASHES)
    s = s.replace("&", " and ")
    s = re.sub(r"[^\w\s-]", " ", s)          # drop punctuation, keep word chars/hyphen
    s = re.sub(r"[\s_-]+", " ", s)
    return s.strip().casefold()


def similarity(a, b):
    return SequenceMatcher(None, normalize_label(a), normalize_label(b)).ratio()


def path_str(section, topic, subtopic):
    return f"{section}/{topic}/{subtopic}"


def fingerprint(cls, identity):
    """Stable finding ID — same finding yields same fingerprint across sessions."""
    h = hashlib.sha256(f"{cls}|{normalize_label(identity)}".encode()).hexdigest()
    return f"{cls}:{h[:12]}"


def enumerate_paths(taxonomy):
    """taxonomy: {section: {topic: [subtopic,...]}} -> list of (sec, top, sub)."""
    out = []
    for sec, topics in (taxonomy or {}).items():
        for top, subs in (topics or {}).items():
            for sub in (subs or []):
                out.append((sec, top, sub))
    return out


def count_pyqs_by_path(classifications):
    """classifications: {paper: [{section,topic,subtopic,...}]} -> {normpath: count}."""
    counts = {}
    for _paper, qs in (classifications or {}).items():
        for q in (qs or []):
            key = normalize_label(path_str(q.get("section"), q.get("topic"), q.get("subtopic")))
            counts[key] = counts.get(key, 0) + 1
    return counts


# ══════════════════════════════════════════════════════════════════
# HARD INVARIANTS — not overridable by any adjudication verdict
# ══════════════════════════════════════════════════════════════════
SAFE_DEFAULT = {
    "SUBJECT_MISSING":         "ADD_SECTION",
    "SUBJECT_EXTRA":           "RETAIN",
    "ITEM_UNMAPPED":           "ADD_SUBTOPIC",
    "PATH_EXTRA":              "RETAIN",
    "NEAR_DUPLICATE":          "RETAIN_BOTH",
    "TOPIC_OVER_AGGREGATION":  "RE_DERIVE",
    "RATIO_HARDSTOP":          "RE_DERIVE",
}
# Verdicts that destroy information. Permitted only under strict conditions.
DESTRUCTIVE = {"DROP", "SUPPRESS", "MERGE_INTO", "QUARANTINE"}


def enforce_invariants(finding, verdict):
    """
    Returns (final_verdict, applied_notes[]).
    Rewrites unsafe verdicts to the safe default. Never raises on model error —
    it corrects, so a bad adjudication degrades to safe, not to data loss.
    """
    notes = []
    cls = finding["class"]
    action = verdict.get("action")
    conf = str(verdict.get("confidence", "LOW")).upper()
    quote = (verdict.get("syllabus_quote") or "").strip()
    evid = bool(verdict.get("syllabus_present"))
    safe = SAFE_DEFAULT.get(cls, "RETAIN")

    # INV-4 EVIDENCE_REQUIRED: destructive verdict needs a literal syllabus quote
    if action in DESTRUCTIVE and not quote:
        notes.append("INV-4 EVIDENCE_REQUIRED: no syllabus quote -> safe default")
        action = safe

    # INV-1 NO_SUPPRESS_SYLLABUS: never remove an item the syllabus enumerates
    if action in DESTRUCTIVE and evid:
        notes.append("INV-1 NO_SUPPRESS_SYLLABUS: item is syllabus-enumerated -> safe default")
        action = safe

    # INV-2 NO_DROP_PYQ_BACKED: never drop a path with >= MIN_PATTERN_SIZE PYQs
    if action in DESTRUCTIVE and finding.get("pyq_count", 0) >= MIN_PATTERN_SIZE:
        notes.append(f"INV-2 NO_DROP_PYQ_BACKED: {finding['pyq_count']} PYQs -> safe default")
        action = safe

    # INV-3 LOW_CONFIDENCE_SAFE_DEFAULT
    if conf != "HIGH" and action != safe:
        notes.append("INV-3 LOW_CONFIDENCE_SAFE_DEFAULT -> safe default")
        action = safe

    return action, notes


# ══════════════════════════════════════════════════════════════════
# TIER 0 — deterministic reconciliation
# ══════════════════════════════════════════════════════════════════
def reconcile(syllabus_items, scan_taxonomy, classifications, exam_config,
              syllabus_subjects=None, group_topic_map=None,
              unanchorable_subjects=None, declared_deviations=None,
              name_canonicalizations=None, syllabus_style=None):
    """
    syllabus_items   : [{id, subject, raw_text, enumerated, mapped_paths[]}]
    syllabus_subjects: [str] verbatim subject names from S2-1. If None, derived
                       from items (legacy fallback — may yield false SUBJECT_EXTRA
                       when a subject has no enumerated items).
    scan_taxonomy    : {section: {topic: [subtopic]}}
    group_topic_map      : S2-4 declared syllabus-group -> taxonomy-topic map
    unanchorable_subjects: S2-4 subjects whose syllabus is FLAT (no grouping)
    declared_deviations  : S2-4 items that deliberately left their syllabus group
    name_canonicalizations: S2-4 spelling corrections snapped to taxonomy (§7)
    syllabus_style       : S2-4 per-subject {'style','entries','atomic'} (S2-1e).
                           When present, the C4 inflation check is STYLE-AWARE
                           per subject; without it C4 falls back to the legacy
                           whole-corpus ratio, which FALSE-HARD-STOPS prose
                           syllabi (7 of 11 real syllabi tested).
    """
    findings = []
    pyq = count_pyqs_by_path(classifications)
    tax_paths = enumerate_paths(scan_taxonomy)
    tax_norm = {normalize_label(path_str(*p)): p for p in tax_paths}

    # ── C1: subject coverage ──────────────────────────────────
    if syllabus_subjects:
        syl_subjects = {normalize_label(x): x for x in syllabus_subjects if x}
    else:
        syl_subjects = {normalize_label(i["subject"]): i["subject"]
                        for i in syllabus_items if i.get("subject")}
    tax_sections = {normalize_label(s): s for s in (scan_taxonomy or {})}
    for k, name in syl_subjects.items():
        if k not in tax_sections:
            findings.append({
                "id": fingerprint("SUBJECT_MISSING", name), "class": "SUBJECT_MISSING",
                "tier": 2, "item": name, "pyq_count": 0,
                "detail": "Syllabus subject has no taxonomy section.",
            })
    for k, name in tax_sections.items():
        if k not in syl_subjects:
            n = sum(c for p, c in pyq.items() if p.startswith(normalize_label(name) + "/"))
            findings.append({
                "id": fingerprint("SUBJECT_EXTRA", name), "class": "SUBJECT_EXTRA",
                "tier": 2, "item": name, "pyq_count": n,
                "detail": "Taxonomy section not present in syllabus subjects.",
            })

    # ── C2: syllabus item mapping (MISSING = data loss class) ──
    claimed = set()
    for it in syllabus_items:
        paths = it.get("mapped_paths") or []
        for p in paths:
            claimed.add(normalize_label(p))
        if not paths:
            findings.append({
                "id": fingerprint("ITEM_UNMAPPED", f"{it.get('subject')}|{it.get('raw_text')}"),
                "class": "ITEM_UNMAPPED", "tier": 2, "item": it.get("raw_text"),
                "subject": it.get("subject"), "syllabus_id": it.get("id"),
                "enumerated": bool(it.get("enumerated", True)), "pyq_count": 0,
                "detail": "Syllabus item has no corresponding taxonomy path.",
            })

    # ── C3: extra taxonomy paths (scan discoveries) ───────────
    for nk, (sec, top, sub) in tax_norm.items():
        if nk not in claimed:
            findings.append({
                "id": fingerprint("PATH_EXTRA", path_str(sec, top, sub)),
                "class": "PATH_EXTRA", "tier": 1, "item": path_str(sec, top, sub),
                "subtopic": sub, "pyq_count": pyq.get(nk, 0),
                "detail": "Taxonomy path not traceable to any syllabus item.",
            })

    # ── C4: ratio guardrail (style-aware, v2.17) ──────────────
    if syllabus_style:
        try:
            from syllabus_provenance import ratio_verdict
        except ImportError:
            ratio_verdict = None
        if ratio_verdict:
            for subj, st in syllabus_style.items():
                n = len([p for p in tax_paths if p[0] == subj])
                verdict, r, basis = ratio_verdict(st, n)
                if verdict in ("HARD STOP", "WARN"):
                    cls = "RATIO_HARDSTOP" if verdict == "HARD STOP" else "RATIO_WARN"
                    findings.append({
                        "id": fingerprint(cls, f"{subj}|{n}"), "class": cls,
                        "tier": 2 if verdict == "HARD STOP" else 0,
                        "item": f"{subj}: {n} subtopics / {basis} = {r:.2f}x",
                        "pyq_count": 0,
                        "detail": f"{st['style']} syllabus — inflation measured against {basis}.",
                    })
            findings.sort(key=lambda f: (-f["tier"], f["class"], str(f["item"])))
            return findings

    n_sub = len(tax_paths)
    n_syl = max(len(syllabus_items), 1)
    ratio = n_sub / n_syl
    if ratio >= RATIO_HARDSTOP:
        findings.append({
            "id": fingerprint("RATIO_HARDSTOP", f"{n_sub}/{n_syl}"), "class": "RATIO_HARDSTOP",
            "tier": 2, "item": f"{n_sub}/{n_syl} = {ratio:.2f}x", "pyq_count": 0,
            "detail": f"Taxonomy inflation >= {RATIO_HARDSTOP}x.",
        })
    elif ratio >= RATIO_WARN:
        findings.append({
            "id": fingerprint("RATIO_WARN", f"{n_sub}/{n_syl}"), "class": "RATIO_WARN",
            "tier": 0, "item": f"{n_sub}/{n_syl} = {ratio:.2f}x", "pyq_count": 0,
            "detail": f"Taxonomy inflation >= {RATIO_WARN}x (informational).",
        })

    # ── C5: near-duplicate subtopics within same topic ────────
    by_topic = {}
    for sec, top, sub in tax_paths:
        by_topic.setdefault((sec, top), []).append(sub)
    for (sec, top), subs in by_topic.items():
        for i in range(len(subs)):
            for j in range(i + 1, len(subs)):
                r = similarity(subs[i], subs[j])
                if r > DUP_SIMILARITY:
                    pair = sorted([subs[i], subs[j]], key=normalize_label)
                    findings.append({
                        "id": fingerprint("NEAR_DUPLICATE", f"{sec}|{top}|{pair[0]}|{pair[1]}"),
                        "class": "NEAR_DUPLICATE", "tier": 2,
                        "item": f"{sec}/{top}: '{pair[0]}' ~ '{pair[1]}' ({r:.0%})",
                        "pyq_count": min(
                            pyq.get(normalize_label(path_str(sec, top, pair[0])), 0),
                            pyq.get(normalize_label(path_str(sec, top, pair[1])), 0)),
                        "detail": "Subtopic names exceed similarity threshold.",
                    })

    # ── C6: topic over-aggregation (MPPSC/SSC class defect) ───
    items_by_subject = {}
    for it in syllabus_items:
        items_by_subject.setdefault(normalize_label(it.get("subject")), []).append(it)
    for nk, sec in tax_sections.items():
        n_topics = len(scan_taxonomy.get(sec, {}) or {})
        n_items = len(items_by_subject.get(nk, []))
        if n_topics <= OVER_AGG_TOPICS and n_items >= OVER_AGG_ITEMS:
            findings.append({
                "id": fingerprint("TOPIC_OVER_AGGREGATION", sec),
                "class": "TOPIC_OVER_AGGREGATION", "tier": 2, "item": sec, "pyq_count": 0,
                "detail": f"{n_topics} topics for {n_items} syllabus items — over-aggregated.",
            })

    # ── C7: anchoring coverage (v2.17 — surfaces S2-4 anchoring state) ──
    # These are INFORMATIONAL (tier 0). They do not block. They exist so the
    # approval record shows WHERE placement could not be verified, instead of
    # that gap being silently invisible at the gate.
    for subj in sorted(unanchorable_subjects or []):
        findings.append({
            "id": fingerprint("UNANCHORABLE_SUBJECT", subj),
            "class": "UNANCHORABLE_SUBJECT", "tier": 0, "item": subj, "pyq_count": 0,
            "detail": "Flat syllabus — no grouping supplied, so topic placement "
                      "for this subject cannot be anchored against any input.",
        })
    for dv in (declared_deviations or []):
        ident = f"{dv.get('id')}|{dv.get('group')}"
        rule = (dv.get("deviation") or {}).get("rule", "?")
        reason = (dv.get("deviation") or {}).get("reason", "")
        findings.append({
            "id": fingerprint("DECLARED_DEVIATION", ident),
            "class": "DECLARED_DEVIATION", "tier": 0, "pyq_count": 0,
            "item": f"{dv.get('id')} ({dv.get('subject')} > {dv.get('group')}) [{rule}]",
            "detail": f"Declared departure from syllabus grouping: {reason}",
        })
    # Anchoring declared but never applied => S2-4 emitted a map nobody used.
    if group_topic_map and not any(i.get("syllabus_group") for i in (syllabus_items or [])):
        findings.append({
            "id": fingerprint("ANCHOR_MAP_UNUSED", "group_topic_map"),
            "class": "ANCHOR_MAP_UNUSED", "tier": 0, "item": "group_topic_map",
            "pyq_count": 0,
            "detail": "group_topic_map supplied but no item carries syllabus_group "
                      "— anchoring was declared but not performed.",
        })

    for fx in (name_canonicalizations or []):
        findings.append({
            "id": fingerprint("NAME_CANONICALIZED", str(fx.get("from"))),
            "class": "NAME_CANONICALIZED", "tier": 0, "pyq_count": 0,
            "item": f"{fx.get('id')}: {fx.get('from')} -> {fx.get('to')}",
            "detail": "Destination spelling snapped to the taxonomy's exact form "
                      "to satisfy §7 byte-identity.",
        })

    findings.sort(key=lambda f: (-f["tier"], f["class"], str(f["item"])))
    return findings


# ══════════════════════════════════════════════════════════════════
# TIER 1 — codified auto-policy (no judgment)
# ══════════════════════════════════════════════════════════════════
def apply_tier1(findings):
    """Resolves PATH_EXTRA by evidence. Returns (resolved, escalated)."""
    resolved, escalated = [], []
    for f in findings:
        if f["tier"] == 0:
            resolved.append({**f, "action": "NOTE", "by": "TIER0"})
        elif f["class"] == "PATH_EXTRA":
            if f["pyq_count"] >= MIN_PATTERN_SIZE:
                resolved.append({**f, "action": "RETAIN", "by": "TIER1",
                                 "reason": f"PYQ-evidenced ({f['pyq_count']} questions)"})
            else:
                # D2 (v2.17): QUARANTINE is a REVIEW FLAG, not a deletion.
                # The path REMAINS in the taxonomy so its classified questions
                # stay reachable. Deleting it would orphan them and break INV-5.
                resolved.append({**f, "action": "QUARANTINE", "by": "TIER1",
                                 "retained_in_taxonomy": True,
                                 "reason": f"below MIN_PATTERN_SIZE ({f['pyq_count']}<{MIN_PATTERN_SIZE}) "
                                           f"— retained in taxonomy, flagged for review"})
        else:
            escalated.append(f)
    return resolved, escalated


# ══════════════════════════════════════════════════════════════════
# TIER 2 — evidence-bound adjudication with replay
# ══════════════════════════════════════════════════════════════════
def adjudicate(escalated, verdicts, prior_record=None):
    """
    verdicts: {finding_id: {action, confidence, syllabus_quote, syllabus_present, rationale}}
    prior_record: previously persisted approval_record -> replayed verbatim (INV-6).
    """
    prior = {}
    if prior_record:
        for e in prior_record.get("adjudications", []):
            prior[e["id"]] = e

    out = []
    for f in escalated:
        if f["id"] in prior:                      # INV-6 REPLAY_DETERMINISM
            out.append({**prior[f["id"]], "replayed": True})
            continue
        v = verdicts.get(f["id"], {})
        action, notes = enforce_invariants(f, v)
        out.append({
            "id": f["id"], "class": f["class"], "item": f["item"],
            "pyq_count": f.get("pyq_count", 0),
            "action": action, "by": "TIER2",
            "confidence": str(v.get("confidence", "LOW")).upper(),
            "syllabus_present": bool(v.get("syllabus_present")),
            "syllabus_quote": (v.get("syllabus_quote") or "")[:200],
            "rationale": (v.get("rationale") or "")[:400],
            "invariants_applied": notes,
            "replayed": False,
        })
    return out


def conservation_check(classifications, taxonomy_after, quarantined_paths=()):
    """
    INV-5 CONSERVATION: no classified question may become unreachable.

    D2 fix (v2.17): quarantine is a FLAG, not a deletion — a quarantined path
    holds 1..MIN_PATTERN_SIZE-1 questions BY DEFINITION, so requiring it to hold
    zero was self-contradictory and made INV-5 fail whenever quarantine fired.
    The correct invariant is that quarantined paths remain LIVE in the taxonomy.
    """
    pyq = count_pyqs_by_path(classifications)
    live = {normalize_label(path_str(*p)) for p in enumerate_paths(taxonomy_after)}
    orphaned = {p: c for p, c in pyq.items() if p not in live and c > 0}
    dropped_q = sorted(p for p in quarantined_paths
                       if normalize_label(p) not in live)
    return {
        "total_classified": sum(pyq.values()),
        "orphaned_questions": sum(orphaned.values()),
        "orphaned_paths": sorted(orphaned),
        "quarantined_removed_from_taxonomy": dropped_q,
        "pass": not orphaned and not dropped_q,
    }


def build_approval_record(exam_code, findings, resolved, adjudications, conservation):
    hard = [a for a in adjudications if a["action"] == "RE_DERIVE"] + \
           [f for f in findings if f["class"] == "RATIO_HARDSTOP"]
    # D3 (v2.17): INV-5 must GATE the verdict. A failed conservation check
    # previously left status CLEAN, making the invariant decorative.
    if conservation and not conservation.get("pass", True):
        hard = hard + [{"item": "INV-5 CONSERVATION FAILED — "
                                f"{conservation.get('orphaned_questions', 0)} question(s) orphaned",
                        "action": "RE_DERIVE"}]
    if hard:
        status = "HELD"
    elif adjudications:
        status = "CLEAN_ADJUDICATED"   # Tier 2 ran, all safely resolved, taxonomy locked
    else:
        status = "CLEAN"
    return {
        "exam_code": exam_code,
        "schema_version": "1.0",
        "status": status,
        "engine": "S4-0 reconcile_taxonomy",
        "thresholds": {"MIN_PATTERN_SIZE": MIN_PATTERN_SIZE, "RATIO_WARN": RATIO_WARN,
                       "RATIO_HARDSTOP": RATIO_HARDSTOP, "DUP_SIMILARITY": DUP_SIMILARITY},
        "anchoring": {
            "unanchorable_subjects": [f["item"] for f in findings
                                      if f["class"] == "UNANCHORABLE_SUBJECT"],
            "declared_deviations":   [{"item": f["item"], "detail": f["detail"]}
                                      for f in findings
                                      if f["class"] == "DECLARED_DEVIATION"],
            "anchor_map_unused":     any(f["class"] == "ANCHOR_MAP_UNUSED"
                                         for f in findings),
            "name_canonicalizations": [f["item"] for f in findings
                                       if f["class"] == "NAME_CANONICALIZED"],
        },
        "summary": {
            "findings_total": len(findings),
            "held_reasons": [h.get("item") for h in hard],
            "auto_resolved": len(resolved),
            "adjudicated": len(adjudications),
            "replayed": sum(1 for a in adjudications if a.get("replayed")),
        },
        "auto_resolved": resolved,
        "adjudications": adjudications,
        "conservation": conservation,
    }
