"""
reconcile_taxonomy.py v1.4 — Taxonomy Reconciliation Engine, Framework_PYQAnalyse S4-0

v1.4 — 2026-08-30 — GAP-2026-08-30-TYPE1-HALT-ELIMINATION. SCHEMA_VERSION 1.3 -> 1.4.
    GATE-AT-SOURCE release: the over-aggregation check becomes a SINGLE public
    function with three call sites, and PYQApprove's checks become a backstop.

    E1  check_topic_density() EXPORTED — one implementation, called by PYQDraft
        (pre-delivery gate), PYQScan (S3-1 tripwire) and C6 (backstop). BOTH forms:
        (a) subject-density (constants unchanged) and (b) NEW per-topic form —
        TOPIC_OVER_AGGREGATION_TOPIC fires when one topic's mapped enumerated-item
        count reaches OVER_AGG_PER_TOPIC_CAP (closes the UGC-History 4.0-average
        blind spot: 1x20 + 15x1 averages 2.2 and passes, 20-in-one is caught).
        DENOMINATOR FIX: density divides by SYLLABUS-ANCHORED topics only (topics
        reachable from mapped_paths); scan-discovered topics are reported, never
        counted (kills the dilution that masked RPSC's true 6.0 as 5.25).
        FINDING DETAIL: every over-cap topic is named with its item count, and
        crowded_topics rides on the finding for the E3 directive.
        SCOPING: excluded items and qcount_anchored topics are OUT of the
        measurement domain; the scoping counts are attested in the C6 ledger note.
    E2  C2 skips items with a declared `excluded` state; excluded_counts attested.
    E3  build_approval_record() writes re_derive_directive on HELD: findings,
        crowded_topics, machine constraints, rejected_fingerprint. Consumed by
        PYQDraft S2-0 intake — the Approve->Draft loop is now convergent.
    E4  GRANDFATHERING + grandfather(): a prior record without spec_generation
        identifies a pre-release lock; NEW_FINDING_CLASSES findings are rewritten
        to Tier 0 informational, so an INV-6 mode-C replay can never newly HELD
        the back catalog on a check class that did not exist when it locked.
    E6  reconcile() input-shape guards: classifications must be dict-of-paper->list
        (the flattened-list defect observed live), scan_taxonomy dict-of-dict-of-list,
        ledger a CheckLedger or None. Violations raise with the CORRECT shape stated.
    E7  DECLARED_AMBER + resolve_declared_amber(): findings matching a draft/scan
        amber_status residue are resolved Tier 0 BEFORE adjudication (auto_resolved,
        by=DECLARED_AMBER) — reported, never HELD, and NEVER in the INV-6 replay
        ledger, so a later non-AMBER re-run judges a recurring finding FRESH.
    Self-test: T8a fixture updated (items now spread across its 3 topics — the
    denominator fix makes the old all-in-one-topic shape CORRECTLY fire); T15-T21
    added for E1-E7. SAFE_DEFAULT gains TOPIC_OVER_AGGREGATION_TOPIC -> RE_DERIVE.

v1.3 — 2026-07-26 — THE RECORD CARRIES THE TAXONOMY, NOT JUST ITS HASH.
    SCHEMA_VERSION 1.2 -> 1.3. GAP-2026-07-25-003 follow-up, and the change that ends
    the defect class rather than handling it.

    v1.2 made the record prove WHAT was locked. It proved it with a fingerprint —
    which establishes identity and cannot restore content. So Steps 3, 4, 5 and 6
    still had to recover the taxonomy by PARSING A WORD DOCUMENT, and when the
    platform's storage of that document turned out to be extracted text rather than
    an OOXML package, all four steps failed on every exam simultaneously.

    build_approval_record() has always received final_taxonomy in exactly the
    {section: {topic: [subtopic]}} shape those steps need, and discarded it. It now
    records it under "taxonomy": {"sections": ...}. Three consequences:
      • the record is SELF-SUFFICIENT — the taxonomy and the fingerprint that
        validates it live in one file, so a consumer needs no second artefact and no
        new trust;
      • that file is JSON, which the platform stores BYTE-FOR-BYTE (measured: .py,
        .json and .md pass through unchanged; .docx becomes Markdown text and .pdf
        becomes a Zip page-bundle, both under their original names);
      • display names come from JSON rather than from a text-extraction round trip,
        so they are exact rather than merely slug-equivalent — which matters, because
        the fingerprint is slug-normalised BY DESIGN and cannot detect a display-byte
        change on its own.
    Order is preserved throughout: subject order sets subject_order and topic order
    sets topic_idx, which is positional.

    Additive and backward-compatible. Older records simply lack the key, and the
    reader falls back to the Analysis doc for them, so no exam approved before this
    version needs re-running.

v1.2 — 2026-07-25 — TAXONOMY ATTESTATION (GAP-2026-07-25-002). SCHEMA_VERSION 1.1 -> 1.2.
    build_approval_record() gains final_taxonomy= and, when given one, records
    taxonomy_fingerprint + taxonomy_counts. Until now this record proved the
    reconciliation RAN — status, mode, ledger, conservation — and said nothing about WHAT
    it locked, so PYQSort could verify the lock was earned and still sort against an
    entirely different taxonomy. That is not hypothetical: a reader that flattened six
    subjects into one passed every check in this record cleanly. Verified downstream at
    PYQSort S1-0b.
    FAIL-SAFE: with no taxonomy supplied the keys are OMITTED, never computed over an
    empty dict. A fingerprint of nothing is a well-formed value that would report a
    content MISMATCH and point the operator at the Analysis doc, which is not where the
    fault would be. An absent key instead names the real cause — a caller that does not
    yet pass final_taxonomy. Unknown is never attested.
    NEW HARD DEPENDENCY: blueprint_core (for taxonomy_fingerprint / slugify). Both ship
    in the same clone and blueprint_core is standard-library only, so this adds no
    package requirement — but this engine LOCKS taxonomies, so the dependency is stated
    rather than left to be discovered.
Exam-agnostic. Zero hardcoded exam/section/subtopic names.

Converts the PYQApprove human quiz into a deterministic 3-tier verdict:
  Tier 0 — machine reconciliation (no judgment)
  Tier 1 — codified auto-policy (no judgment)
  Tier 2 — evidence-bound adjudication, replayed from prior record

CHANGELOG
  v1.1  GAP-2026-07-25-001 remediation.
        P0 (D-1)  reconcile() returned from inside C4's style-aware branch, so
                  C5/C6/C7 never ran for any exam carrying syllabus_style — i.e.
                  every PYQDraft >= v2.17 exam. C4's two forms are mutually
                  exclusive BY DESIGN; that exclusivity is now if/else and
                  reconcile() has a SINGLE EXIT.
        P0 (N-9)  ADD_SECTION / ADD_SUBTOPIC (the safe defaults for
                  SUBJECT_MISSING and ITEM_UNMAPPED — the data-loss class) were
                  never materialised and never held the run, so a taxonomy could
                  auto-lock while missing a syllabus subject. S4-0 reconciles and
                  MUST NOT derive, so these now HOLD the run (INV-9).
        P1 (N-1)  C4's style-aware subject match used raw `==` — the only
                  comparison in reconcile() not going through normalize_label(),
                  contrary to S4-0's own "all comparison is via normalize_label"
                  rule. Case/spacing/dash drift between the syllabus-sourced
                  style keys and the scan-sourced taxonomy sections silently
                  zeroed C4's measurement domain.
        P1 (N-2)  INV-8 CHECK_MEASURED: execution attestation alone is not
                  sufficient — a check can run, attest, and measure nothing.
                  Each check now attests its MEASUREMENT DOMAIN; a domain of 0
                  over non-empty inputs is VACUOUS and holds the run.
        P1 (INV-7) CHECK_COMPLETENESS: reconcile() records every check it
                  completes; build_approval_record() forces HELD and names the
                  missing IDs when it cannot prove completion. Fail-safe: a
                  caller that does not attest gets HELD, never CLEAN.
        P1 (D-2)  mode ("FULL" | "DEGRADED") added; DEGRADED emits
                  status="DEGRADED" and requires locked_taxonomy.
        P1 (D-3)  C4 is provenance-DEPENDENT and is a declared skip in DEGRADED.
                  Both forms divide by a syllabus-derived base; with no
                  provenance the divisor collapses to 1 and every DEGRADED run
                  would be falsely HELD on RATIO_HARDSTOP.
        P1 (D-7)  materialise() added — the only step permitted to change the
                  taxonomy, and it may only apply adjudicated actions.
        P2 (N-4)  C6 over-aggregation made SCALE-RELATIVE. The absolute rule
                  (<=4 topics AND >=10 items) false-fired on legitimately small
                  exams — 1 subject / 3 topics / 12 items was held as
                  over-aggregated. Now measured as items-per-topic density.
        P2 (D-4)  The record reports the thresholds ACTUALLY applied, per form.
        P2 (N-5)  A syllabus_style present with syllabus_provenance unimportable
                  silently downgraded C4 from 0.85/1.0 prose thresholds to
                  2.0/3.0 legacy. That downgrade is now attested and holds.
        P2 (N-7)  Replay records whether the prior record was itself attested
                  and produced by the same engine version. INV-6 replay is
                  preserved verbatim; it is now labelled, not silently trusted.
        Record schema 1.0 -> 1.1: adds mode, engine_version, checks{}, thresholds
                  per form, prior_record_attested.
        P1 (INV-10) materialise() matched destructive actions against
                  entry['item'], which is a path string ONLY for PATH_EXTRA —
                  and PATH_EXTRA never reaches a destructive action, being
                  resolved at Tier 1. Every destructively-adjudicable class
                  carries a description, subject name or raw syllabus text, so
                  DROP / SUPPRESS / MERGE_INTO silently removed nothing while
                  the record asserted the path was dropped. The taxonomy was
                  never harmed; the RECORD lied. Unresolvable destructive
                  actions now block and HOLD the run.
        --self-test added.
  v1.0  Initial release (Framework_PYQAnalyse v2.17).
"""
import json, re, hashlib, unicodedata
from blueprint_core import taxonomy_fingerprint   # v1.2 — THE canonical fingerprint
from difflib import SequenceMatcher

ENGINE_VERSION = "reconcile_taxonomy.py v1.4"
SCHEMA_VERSION = "1.4"

# GAP-2026-08-30-TYPE1-HALT-ELIMINATION — generation stamp. Written by
# save_taxonomy_draft (S2-4) into taxonomy_draft.json and by
# build_approval_record() into approval_record.json. Its ABSENCE in an artifact
# is load-bearing: it is what identifies a pre-release artifact for the A1
# three-case rule, the F1 tripwire mode select, and E4/S3 grandfathering.
SPEC_GENERATION = "2026-08-30-TYPE1"

# Finding classes INTRODUCED by the 2026-08-30 release. Against a taxonomy
# locked before it (prior record lacks spec_generation), these are Tier 0
# informational (E4/S3) — a routine mode-C replay can never newly HELD on them.
NEW_FINDING_CLASSES = frozenset({"TOPIC_OVER_AGGREGATION_TOPIC"})

# GATE-AT-SOURCE LAW bound (§6.1.4): every self-correction gate runs at most
# this many constraint-carrying rounds, then exits AMBER — never a dead stop.
SELF_CORRECTION_MAX_ROUNDS = 3

MIN_PATTERN_SIZE = 3      # MUST match S3-6 refinement threshold
RATIO_WARN       = 2.0    # S2-3 guardrail (LEGACY C4 form only)
RATIO_HARDSTOP   = 3.0    # S2-3 guardrail (LEGACY C4 form only)
DUP_SIMILARITY   = 0.75   # S4-4 near-duplicate threshold

# C6 over-aggregation (v1.1, N-4). The v1.0 rule was ABSOLUTE — "<=4 topics AND
# >=10 items" — which is a statement about ONE exam's scale applied to a fleet of
# ~200 exams of wildly different syllabus sizes. It false-fired on legitimately
# small exams (1 subject / 3 topics / 12 items) and, because the safe default for
# TOPIC_OVER_AGGREGATION is RE_DERIVE, a false fire is a HARD BLOCK.
# The defect the check exists for is DENSITY: a syllabus crushed into too few
# topics. S2-3 states the target shape directly — "the syllabus items ARE the
# Topics" — so density is the scale-free measure of departure from it.
OVER_AGG_ITEMS_PER_TOPIC = 5.0   # >= this many syllabus items per topic => crushed
OVER_AGG_MIN_ITEMS       = 10    # floor: never judge density on a tiny syllabus
# v1.4 (E1b, DECISION D1): PER-TOPIC cap — one topic absorbing this many mapped
# enumerated items is over-aggregated regardless of the subject AVERAGE. The
# average cannot catch mixed shapes (1 topic x 20 items + 15 x 1 = 2.2 average);
# the per-topic form can. Same number as the density threshold: one number, one
# meaning. Topics flagged qcount_anchored (archetype A2) are OUT of this domain.
OVER_AGG_PER_TOPIC_CAP   = 5

# ── Check registry (INV-7 / INV-8) ───────────────────────────────────
# ONE source of truth for which checks exist and which are expected per mode.
CHECK_IDS = ("C1", "C2", "C3", "C4", "C5", "C6", "C7")
EXPECTED_CHECKS = {
    "FULL":     set(CHECK_IDS),
    # DEGRADED runs against a LOCKED taxonomy with no S2-3e provenance record.
    # C1/C2/C6/C7 need that record. C4 needs it too (D-3): both forms divide by a
    # syllabus-derived base, so with no provenance the divisor is 1 and every real
    # exam trips RATIO_HARDSTOP. A check guaranteed to fire is not a check.
    "DEGRADED": {"C3", "C5"},
}
DECLARED_SKIPS = {
    "FULL":     set(),
    "DEGRADED": {"C1", "C2", "C4", "C6", "C7"},
}
MODES = tuple(EXPECTED_CHECKS)


class CheckLedger:
    """
    INV-7 + INV-8 attestation sink.

    Records, per check: whether it executed, whether its inputs were present, and
    the size of the MEASUREMENT DOMAIN it actually iterated over.

    The distinction that matters:
      inputs absent, domain 0  -> INAPPLICABLE. Legitimate. Nothing to measure.
      inputs present, domain 0 -> VACUOUS. The check ran and measured NOTHING.
                                  Indistinguishable from a pass in its output, so
                                  it must be indistinguishable from a FAILURE in
                                  its status. This is the N-1 class: a name-match
                                  that silently misses makes a live check inert.
    """

    def __init__(self):
        self.entries = {}

    def record(self, check_id, *, domain, inputs_present, findings=0,
               form=None, note=None):
        self.entries[check_id] = {
            "executed": True,
            "inputs_present": bool(inputs_present),
            "domain": int(domain),
            "findings": int(findings),
            "vacuous": bool(inputs_present) and int(domain) == 0,
            "form": form,
            "note": note,
        }

    def executed(self):
        return {k for k, v in self.entries.items() if v["executed"]}

    def vacuous(self):
        return {k for k, v in self.entries.items() if v["vacuous"]}

    def form(self, check_id):
        return (self.entries.get(check_id) or {}).get("form")

    def as_dict(self, mode):
        expected = EXPECTED_CHECKS[mode]
        executed = self.executed()
        return {
            "expected":         sorted(expected),
            "executed":         sorted(executed),
            "declared_skipped": sorted(DECLARED_SKIPS[mode]),
            "missing":          sorted(expected - executed),
            "vacuous":          sorted(self.vacuous() & expected),
            "c4_form":          self.form("C4"),
            "detail":           {k: self.entries[k] for k in sorted(self.entries)},
        }

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
# E1 (GAP-2026-08-30-TYPE1-HALT-ELIMINATION) — THE over-aggregation check.
# ONE implementation, THREE call sites: PYQDraft pre-delivery gate, PYQScan
# S3-1 tripwire, and C6 below (backstop). Specs CITE this function and the
# constants above; they never restate the values (GATE-AT-SOURCE LAW rule 3).
# ══════════════════════════════════════════════════════════════════
def _item_excluded(it, excluded_ids):
    return bool(it.get("excluded")) or (it.get("id") in excluded_ids)


def check_topic_density(syllabus_items, taxonomy, *,
                        qcount_anchored=frozenset(), excluded_ids=frozenset()):
    """
    BOTH forms of the over-aggregation check, scale-free and scoped.

      SUBJECT form  — TOPIC_OVER_AGGREGATION when a subject has
                      >= OVER_AGG_MIN_ITEMS eligible items AND
                      >= OVER_AGG_ITEMS_PER_TOPIC items per anchored topic.
      PER-TOPIC form — TOPIC_OVER_AGGREGATION_TOPIC when any single
                      non-anchored topic's mapped eligible-item count
                      reaches OVER_AGG_PER_TOPIC_CAP. Needs mapped_paths,
                      so it measures nothing pre-mapping (C1 sequencing:
                      the subject form alone runs after S2-3 Step 1; BOTH
                      forms run at the pre-delivery gate and at S4-0).

    DENOMINATOR (E1c): topics reachable from the items' mapped_paths are
    SYLLABUS-ANCHORED and form the density denominator. Topics present in
    the taxonomy but reached by NO item are scan-discovered (or empty) and
    are reported separately, never counted — scan discovery can no longer
    dilute draft over-aggregation (RPSC: 6.0 true density, not 5.25).
    When NO item of a subject carries any mapped_paths (the pre-mapping
    call from S2-3 Step 1), ALL of that subject's topics anchor.

    SCOPING (E1e): items with a declared exclusion (item['excluded'] set,
    or id in excluded_ids) and topics named in qcount_anchored are OUT of
    the measurement domain. Scoping counts ride on each finding's
    `scoping` key so the C6 ledger note can attest them (INV-8 extension).

    Returns a list of findings in the reconcile() finding shape. Findings
    additionally carry `crowded_topics`: [{topic, item_count}] — consumed
    by build_approval_record()'s re_derive_directive (E3).
    """
    findings = []
    anchored_norm = {normalize_label(t) for t in (qcount_anchored or ())}
    excluded_ids = frozenset(excluded_ids or ())

    items_by_subject = {}
    for it in (syllabus_items or []):
        items_by_subject.setdefault(normalize_label(it.get("subject")), []).append(it)

    for sec, topics in (taxonomy or {}).items():
        nk = normalize_label(sec)
        subj_items = items_by_subject.get(nk, [])
        if not subj_items:
            continue
        eligible = [it for it in subj_items if not _item_excluded(it, excluded_ids)]
        n_excluded = len(subj_items) - len(eligible)

        topic_norm = {normalize_label(t): t for t in (topics or {})}
        # mapped eligible-item count per topic (path component [1] is the Topic)
        per_topic = {}
        any_mapped = False
        for it in eligible:
            seen_topics = set()
            for p in (it.get("mapped_paths") or []):
                comps = p if isinstance(p, (list, tuple)) else None
                if comps is None or len(comps) < 2:
                    continue
                any_mapped = True
                tkey = normalize_label(comps[1])
                if tkey in seen_topics:
                    continue          # one item counts once per topic
                seen_topics.add(tkey)
                per_topic[tkey] = per_topic.get(tkey, 0) + 1

        if any_mapped:
            anchored = [t for t in topic_norm if t in per_topic
                        and t not in anchored_norm]
            n_scan_discovered = sum(1 for t in topic_norm
                                    if t not in per_topic and t not in anchored_norm)
        else:                          # pre-mapping call (S2-3 Step 1)
            anchored = [t for t in topic_norm if t not in anchored_norm]
            n_scan_discovered = 0
        n_anchored_exempt = sum(1 for t in topic_norm if t in anchored_norm)

        # numerator: eligible items NOT wholly absorbed by qcount-anchored topics
        def _only_anchored(it):
            tks = {normalize_label(p[1]) for p in (it.get("mapped_paths") or [])
                   if isinstance(p, (list, tuple)) and len(p) >= 2}
            return bool(tks) and tks <= anchored_norm
        measured_items = [it for it in eligible if not _only_anchored(it)]

        crowded = sorted(
            # .get(t, t): a mapped path can name a topic ABSENT from the
            # taxonomy (a C3/C5 destination defect). C6 must still measure and
            # report — never crash on it — so the normalized name stands in
            # for the missing display name; C5 flags the ghost itself.
            ({"topic": topic_norm.get(t, t), "item_count": c}
             for t, c in per_topic.items()
             if t not in anchored_norm and c >= OVER_AGG_PER_TOPIC_CAP),
            key=lambda x: -x["item_count"])
        scoping = {"excluded_items": n_excluded,
                   "qcount_anchored_topics": n_anchored_exempt,
                   "scan_discovered_topics": n_scan_discovered}

        n_items = len(measured_items)
        density = n_items / max(len(anchored), 1)
        if n_items >= OVER_AGG_MIN_ITEMS and density >= OVER_AGG_ITEMS_PER_TOPIC:
            crowd_txt = ("; crowded: " + "; ".join(
                f"{c['topic']}: {c['item_count']} items" for c in crowded)
                if crowded else "")
            disc_txt = (f" ({n_scan_discovered} scan-discovered topic(s) excluded "
                        f"from the denominator)" if n_scan_discovered else "")
            findings.append({
                "id": fingerprint("TOPIC_OVER_AGGREGATION", sec),
                "class": "TOPIC_OVER_AGGREGATION", "tier": 2, "item": sec,
                "pyq_count": 0,
                "detail": f"{len(anchored)} syllabus-anchored topic(s) for "
                          f"{n_items} syllabus items = {density:.1f} items/topic "
                          f"(>= {OVER_AGG_ITEMS_PER_TOPIC}) — over-aggregated"
                          f"{disc_txt}{crowd_txt}.",
                "crowded_topics": crowded, "scoping": scoping,
            })
        for c in crowded:
            findings.append({
                "id": fingerprint("TOPIC_OVER_AGGREGATION_TOPIC",
                                  f"{sec}|{c['topic']}"),
                "class": "TOPIC_OVER_AGGREGATION_TOPIC", "tier": 2,
                "item": f"{sec} > {c['topic']}", "pyq_count": 0,
                "detail": f"topic absorbs {c['item_count']} mapped syllabus items "
                          f"(cap {OVER_AGG_PER_TOPIC_CAP}) — split it: the items "
                          f"ARE the Topics (EC-P20).",
                "crowded_topics": [c], "scoping": scoping,
            })
    return findings


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
    "TOPIC_OVER_AGGREGATION_TOPIC": "RE_DERIVE",
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
              name_canonicalizations=None, syllabus_style=None,
              mode="FULL", locked_taxonomy=None, ledger=None,
              qcount_anchored_topics=None):
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
    mode                 : "FULL" (R1 modes A and C) | "DEGRADED" (R1 mode B).
    locked_taxonomy      : REQUIRED in DEGRADED mode — the taxonomy parsed from
                           the already-locked Analysis doc. Without it C3 has no
                           reference and reports EVERY path as PATH_EXTRA.
    ledger               : CheckLedger. INV-7/INV-8 attestation sink. A caller
                           that passes None gets a record that cannot prove any
                           check ran, and build_approval_record() will HOLD it.

    ENGINE CONTRACT — SINGLE EXIT. This function returns in exactly one place.
    An early return inside any check's branch silently disables every check
    positioned below it (GAP-2026-07-25-001). Checks are INDEPENDENT: the branch
    one check takes MUST NOT affect whether another check runs.
    """
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; expected one of {MODES}")
    if mode == "DEGRADED" and locked_taxonomy is None:
        raise ValueError(
            "DEGRADED mode requires locked_taxonomy — the taxonomy parsed from "
            "the locked Analysis doc. Without it C3 has no reference and every "
            "taxonomy path is reported as PATH_EXTRA.")
    # ── E6 (v1.4) INPUT-SHAPE GUARDS — corrective, not diagnostic-only ────
    # Each message STATES the correct shape, because the observed live defect
    # (halt #10) was a session passing classifications as a flattened list and
    # then reading an opaque engine error it could not act on.
    if classifications is not None and not isinstance(classifications, dict):
        raise TypeError(
            "classifications must be a DICT keyed by paper filename, each value "
            "a LIST of classification rows: {paper: [{q_num, section, topic, "
            "subtopic, ...}, ...]}. A flattened list of rows is the exact shape "
            "this guard rejects — rebuild it as {paper_filename: rows} from "
            "[ExamCode]_classifications.json (S3-8 stores it in that shape).")
    if isinstance(classifications, dict):
        for _pk, _pv in classifications.items():
            if not isinstance(_pv, list):
                raise TypeError(
                    f"classifications[{_pk!r}] must be a LIST of classification "
                    f"rows (got {type(_pv).__name__}). Correct shape: "
                    f"{{paper_filename: [rows]}}.")
    if scan_taxonomy is not None and not isinstance(scan_taxonomy, dict):
        raise TypeError(
            "scan_taxonomy must be {section: {topic: [subtopic, ...]}} — the "
            "dict stored at scan_progress.json['taxonomy'] (S3-8).")
    if isinstance(scan_taxonomy, dict):
        for _sk, _sv in scan_taxonomy.items():
            if not isinstance(_sv, dict):
                raise TypeError(
                    f"scan_taxonomy[{_sk!r}] must be a DICT of topics (got "
                    f"{type(_sv).__name__}). Correct shape: "
                    f"{{section: {{topic: [subtopic, ...]}}}}.")
    if ledger is not None and not isinstance(ledger, CheckLedger):
        raise TypeError(
            f"ledger must be a CheckLedger (or None for the fail-safe HELD "
            f"path), got {type(ledger).__name__}. Construct CheckLedger() and "
            f"pass it so INV-7/INV-8 can attest what ran.")
    if ledger is None:
        ledger = CheckLedger()          # local sink; caller proved nothing
    run = EXPECTED_CHECKS[mode]

    syllabus_items = syllabus_items or []
    findings = []
    pyq = count_pyqs_by_path(classifications)
    tax_paths = enumerate_paths(scan_taxonomy)
    tax_norm = {normalize_label(path_str(*p)): p for p in tax_paths}
    tax_sections = {normalize_label(s): s for s in (scan_taxonomy or {})}

    if syllabus_subjects:
        syl_subjects = {normalize_label(x): x for x in syllabus_subjects if x}
    else:
        syl_subjects = {normalize_label(i["subject"]): i["subject"]
                        for i in syllabus_items if i.get("subject")}

    # ── C1: subject coverage ──────────────────────────────────
    if "C1" in run:
        n0 = len(findings)
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
        ledger.record("C1",
                      domain=len(syl_subjects) + len(tax_sections),
                      inputs_present=bool(syl_subjects or tax_sections),
                      findings=len(findings) - n0)

    # ── C2: syllabus item mapping (MISSING = data loss class) ──
    claimed = set()
    for it in syllabus_items:
        for p in (it.get("mapped_paths") or []):
            claimed.add(normalize_label(p))
    if "C2" in run:
        n0 = len(findings)
        excluded_counts = {}
        for it in syllabus_items:
            exc = it.get("excluded")
            if exc:
                # E2 (v1.4): a recorded exclusion is a DECLARED state, not data
                # loss — C2 skips it and the counts are attested below. An item
                # both excluded AND mapped is a build error validate_provenance
                # surfaces at Draft (E5); it is never silently resolved here.
                cls = (exc.get("class") if isinstance(exc, dict) else str(exc)) or "?"
                excluded_counts[cls] = excluded_counts.get(cls, 0) + 1
                continue
            if not (it.get("mapped_paths") or []):
                findings.append({
                    "id": fingerprint("ITEM_UNMAPPED", f"{it.get('subject')}|{it.get('raw_text')}"),
                    "class": "ITEM_UNMAPPED", "tier": 2, "item": it.get("raw_text"),
                    "subject": it.get("subject"), "syllabus_id": it.get("id"),
                    "enumerated": bool(it.get("enumerated", True)), "pyq_count": 0,
                    "detail": "Syllabus item has no corresponding taxonomy path.",
                })
        ledger.record("C2", domain=len(syllabus_items),
                      inputs_present=bool(syllabus_items),
                      findings=len(findings) - n0,
                      note={"excluded_counts": excluded_counts}
                           if excluded_counts else None)

    # ── C3: extra taxonomy paths (scan discoveries) ───────────
    # DEGRADED: measured against the LOCKED doc taxonomy, not against syllabus
    # provenance (which does not exist for a mode-B exam).
    if "C3" in run:
        n0 = len(findings)
        if mode == "DEGRADED":
            reference = {normalize_label(path_str(*p))
                         for p in enumerate_paths(locked_taxonomy)}
            ref_present = bool(reference)
        else:
            reference = claimed
            ref_present = bool(syllabus_items)
        for nk, (sec, top, sub) in tax_norm.items():
            if nk not in reference:
                findings.append({
                    "id": fingerprint("PATH_EXTRA", path_str(sec, top, sub)),
                    "class": "PATH_EXTRA", "tier": 1, "item": path_str(sec, top, sub),
                    "subtopic": sub, "pyq_count": pyq.get(nk, 0),
                    "detail": "Taxonomy path not traceable to any syllabus item."
                              if mode == "FULL" else
                              "Taxonomy path absent from the locked Analysis doc.",
                })
        ledger.record("C3", domain=len(tax_paths),
                      inputs_present=bool(tax_paths) and ref_present,
                      findings=len(findings) - n0)

    # ── C4: ratio guardrail — TWO MUTUALLY EXCLUSIVE FORMS ────
    # STYLE_AWARE when usable provenance exists, else LEGACY. Exactly one runs.
    # The exclusivity is `if/else` — expressing it as `return` (v1.0) terminated
    # the whole function and silently disabled C5, C6 and C7 (GAP-2026-07-25-001).
    if "C4" in run:
        n0 = len(findings)
        ratio_verdict = None
        import_failed = False
        if syllabus_style:
            try:
                from syllabus_provenance import ratio_verdict
            except ImportError:
                ratio_verdict = None
                import_failed = True

        if syllabus_style and ratio_verdict:
            # N-1: match on the NORMALIZED name. syllabus_style is keyed by the
            # SYLLABUS-sourced subject (S2-1); tax_paths[0] is the SCAN-sourced
            # section name (S3-8). These are independently sourced strings that
            # C1 already compares normalized, so a subject differing only by
            # case/spacing/dash passes C1 and then — under raw `==` — silently
            # zeroed this check's measurement domain.
            paths_by_subject = {}
            for p in tax_paths:
                paths_by_subject.setdefault(normalize_label(p[0]), []).append(p)
            measured = 0
            for subj, st in syllabus_style.items():
                key = normalize_label(subj)
                if key not in paths_by_subject:
                    continue          # subject carries no taxonomy path; C1 covers it
                measured += 1
                n = len(paths_by_subject[key])
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
            ledger.record("C4", domain=measured,
                          inputs_present=bool(syllabus_style) and bool(tax_paths),
                          findings=len(findings) - n0, form="STYLE_AWARE")
        else:
            n_sub = len(tax_paths)
            n_syl = max(len(syllabus_items), 1)
            ratio = n_sub / n_syl
            if ratio >= RATIO_HARDSTOP:
                findings.append({
                    "id": fingerprint("RATIO_HARDSTOP", f"{n_sub}/{n_syl}"),
                    "class": "RATIO_HARDSTOP",
                    "tier": 2, "item": f"{n_sub}/{n_syl} = {ratio:.2f}x", "pyq_count": 0,
                    "detail": f"Taxonomy inflation >= {RATIO_HARDSTOP}x.",
                })
            elif ratio >= RATIO_WARN:
                findings.append({
                    "id": fingerprint("RATIO_WARN", f"{n_sub}/{n_syl}"), "class": "RATIO_WARN",
                    "tier": 0, "item": f"{n_sub}/{n_syl} = {ratio:.2f}x", "pyq_count": 0,
                    "detail": f"Taxonomy inflation >= {RATIO_WARN}x (informational).",
                })
            # N-5: provenance exists but could not be loaded => this run measured
            # a PROSE syllabus at ENUMERATED thresholds. Attest the downgrade;
            # build_approval_record() holds on it rather than reporting a verdict
            # derived from thresholds the exam was never meant to be judged by.
            ledger.record("C4", domain=1 if tax_paths else 0,
                          inputs_present=bool(tax_paths),
                          findings=len(findings) - n0,
                          form="LEGACY_IMPORT_FALLBACK" if import_failed else "LEGACY",
                          note=("syllabus_style present but syllabus_provenance "
                                "could not be imported — style thresholds NOT applied"
                                if import_failed else None))

    # ── C5: near-duplicate subtopics within same topic ────────
    by_topic = {}
    for sec, top, sub in tax_paths:
        by_topic.setdefault((sec, top), []).append(sub)
    if "C5" in run:
        n0 = len(findings)
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
        # Domain is TOPICS EXAMINED, not pairs found. A taxonomy whose topics each
        # hold one subtopic legitimately yields zero pairs; that is a pass, not a
        # vacuum. The vacuum this guards against is "iterated over nothing".
        ledger.record("C5", domain=len(by_topic), inputs_present=bool(tax_paths),
                      findings=len(findings) - n0)

    # ── C6: topic over-aggregation (MPPSC/SSC class defect) ───
    # v1.4 (E1): DELEGATES to check_topic_density() — the SAME function
    # PYQDraft's pre-delivery gate and PYQScan's S3-1 tripwire call. One
    # implementation, three call sites. C6 is the BACKSTOP: post-release it
    # should never fire on a current-generation draft (A1 three-case rule).
    items_by_subject = {}
    for it in syllabus_items:
        items_by_subject.setdefault(normalize_label(it.get("subject")), []).append(it)
    if "C6" in run:
        n0 = len(findings)
        matched = sum(1 for nk in tax_sections if items_by_subject.get(nk))
        f6 = check_topic_density(
            syllabus_items, scan_taxonomy,
            qcount_anchored=frozenset(qcount_anchored_topics or ()),
            excluded_ids=frozenset())
        findings.extend(f6)
        # E1e scoping attestation (INV-8 domain extension): the note carries
        # the measurement-domain scoping so the record can prove WHAT was
        # exempt, not merely that the check ran.
        _scope = next((f.get("scoping") for f in f6 if f.get("scoping")), None)
        if _scope is None and qcount_anchored_topics:
            _scope = {"qcount_anchored_topics": len(qcount_anchored_topics)}
        # Vacuity guard: syllabus items exist but none attached to any taxonomy
        # section => the subject keys never met and C6 measured nothing.
        ledger.record("C6", domain=matched if syllabus_items else len(tax_sections),
                      inputs_present=bool(tax_sections) and bool(syllabus_items),
                      findings=len(findings) - n0, note=_scope)

    # ── C7: anchoring coverage (v2.17 — surfaces S2-4 anchoring state) ──
    # These are INFORMATIONAL (tier 0). They do not block. They exist so the
    # approval record shows WHERE placement could not be verified, instead of
    # that gap being silently invisible at the gate. C7 is what makes the S4-4
    # Branch A anchoring lines producible at all.
    if "C7" in run:
        n0 = len(findings)
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
        if group_topic_map and not any(i.get("syllabus_group") for i in syllabus_items):
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
        # C7's inputs are the S2-4 anchoring record. When S2-4 supplied nothing to
        # anchor (no unanchorable subjects, no deviations, no map, no corrections)
        # the check is INAPPLICABLE, not vacuous — it is still ATTESTED, which is
        # precisely the distinction v1.1 exists to make.
        _c7_inputs = bool(unanchorable_subjects or declared_deviations
                          or group_topic_map or name_canonicalizations)
        ledger.record("C7",
                      domain=(len(unanchorable_subjects or [])
                              + len(declared_deviations or [])
                              + len(name_canonicalizations or [])
                              + (1 if group_topic_map else 0)),
                      inputs_present=_c7_inputs,
                      findings=len(findings) - n0)

    # SINGLE EXIT (engine contract). Do not add a return above this line.
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
# E4 — GRANDFATHERING (§6.4-S3 mechanics)
# ══════════════════════════════════════════════════════════════════
def grandfather(findings, prior_record):
    """
    Run BETWEEN reconcile() and apply_tier1() (S4-0 invocation, A3).

    A prior approval record that lacks `spec_generation` was written before
    this release — the taxonomy it locked predates the per-topic form and the
    exclusion scoping. Findings of NEW_FINDING_CLASSES against it are rewritten
    to Tier 0 informational: reported, never escalated, never HELD. Without
    this, the release CREATES Type-1 halts on the back catalog during routine
    INV-6 mode-C replays — the verified failure mode S3 exists to prevent.

    No prior record (a new exam) or a current-generation prior record: findings
    pass through unchanged — the new checks enforce in full.
    """
    if not prior_record or prior_record.get("spec_generation"):
        return list(findings)
    out = []
    for f in findings:
        if f.get("class") in NEW_FINDING_CLASSES and f.get("tier") == 2:
            out.append({**f, "tier": 0, "grandfathered": True,
                        "detail": (f.get("detail") or "") +
                        " [GRANDFATHERED: taxonomy locked pre-release — this "
                        "finding class did not exist then; informational only "
                        "(E4/S3), never HELD.]"})
        else:
            out.append(f)
    return out


# ══════════════════════════════════════════════════════════════════
# E7 — DECLARED_AMBER resolution (BEFORE adjudication, outside replay)
# ══════════════════════════════════════════════════════════════════
def _amber_residues(amber_status):
    """(class, normalize_label(item)) set from one amber_status or a list."""
    residues = set()
    blocks = amber_status if isinstance(amber_status, (list, tuple)) \
        else [amber_status] if amber_status else []
    for blk in blocks:
        for u in (blk or {}).get("unresolved", []):
            residues.add((u.get("class"), normalize_label(u.get("item"))))
    return residues


def resolve_declared_amber(escalated, amber_status):
    """
    Returns (declared, remaining).

    A finding whose (class, normalized item) matches a residue DECLARED in the
    draft's or scan's amber_status is resolved Tier 0 as DECLARED_AMBER —
    reported in the record and the S4-4 gate text, never escalated to Tier 2,
    never HELD. The declared entries belong in `resolved` (auto_resolved),
    which the INV-6 replay ledger NEVER reads: DECLARED_AMBER resolutions are
    condition-dependent, keyed to the CURRENT artifact's declaration. On a
    later mode-C run against a re-derived, non-AMBER draft the same-fingerprint
    finding is judged FRESH — replaying the waiver would silently pass a
    now-undeclared defect, INV-6's defect class inverted.
    """
    residues = _amber_residues(amber_status)
    declared, remaining = [], []
    for f in escalated:
        keys = {(f.get("class"), normalize_label(str(f.get("item") or "")))}
        if f.get("subject"):
            keys.add((f.get("class"), normalize_label(f.get("subject"))))
        if f.get("syllabus_id"):
            keys.add((f.get("class"), normalize_label(f.get("syllabus_id"))))
        if residues & keys:
            declared.append({**f, "tier": 0, "action": "NOTE",
                             "by": "DECLARED_AMBER",
                             "reason": "carried imperfection, declared at gate "
                                       "exhaustion (AMBER) — Tier 0, reported, "
                                       "never adjudicated, never replayed (E7)"})
        else:
            remaining.append(f)
    return declared, remaining


# ══════════════════════════════════════════════════════════════════
# TIER 2 — evidence-bound adjudication with replay
# ══════════════════════════════════════════════════════════════════
def adjudicate(escalated, verdicts, prior_record=None, amber_status=None):
    """
    verdicts: {finding_id: {action, confidence, syllabus_quote, syllabus_present, rationale}}
    prior_record: previously persisted approval_record -> replayed verbatim (INV-6).
    amber_status: DEFENSIVE second filter (E7). The invocation routes declared
      residues through resolve_declared_amber() BEFORE this stage; passing the
      same amber_status here guarantees a declared residue can never be
      adjudicated (and so never enter the replay ledger) even if a caller
      skipped the resolve step. Matched findings are dropped from this stage —
      build_approval_record(amber_status=...) still reports them.
    """
    if amber_status:
        _, escalated = resolve_declared_amber(escalated, amber_status)
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


# ══════════════════════════════════════════════════════════════════
# MATERIALISATION — the ONLY step permitted to change the taxonomy
# ══════════════════════════════════════════════════════════════════
# INV-9 NO_DERIVATION_AT_S4_0 (v1.1, N-9)
#   S4-0 RECONCILES. It must never DERIVE. Deriving is PYQDraft's job, and a
#   taxonomy is a CONTRACT with every downstream artifact built on it.
#   ADD_SECTION and ADD_SUBTOPIC are the safe defaults for SUBJECT_MISSING and
#   ITEM_UNMAPPED (the data-loss class). Applying them would require S4-0 to
#   INVENT taxonomy structure — where would the new section's topics come from?
#   In v1.0 they were neither applied nor held, so a syllabus subject could be
#   dropped and the taxonomy still auto-locked as CLEAN_ADJUDICATED.
#   v1.1 resolves this in the only safe direction: they HOLD the run.
# INV-10 RESOLVABLE_TARGET (v1.1)
#   A destructive action must name a LIVE taxonomy path. If it does not, it
#   cannot be applied — and it must not be silently discarded either, because
#   the adjudication record would then assert a removal that never happened.
#   Unresolvable destructive actions are blocked and HOLD the run.
UNMATERIALISABLE = {"ADD_SECTION", "ADD_SUBTOPIC"}
REMOVING         = {"DROP", "SUPPRESS", "MERGE_INTO"}


def materialise(scan_taxonomy, resolved, adjudications):
    """
    Apply ONLY adjudicated actions to scan_taxonomy.
    Returns (final_taxonomy, quarantined_paths, blocked).

      RETAIN / RETAIN_BOTH / NOTE      -> keep (no mutation)
      QUARANTINE                       -> path STAYS LIVE in the taxonomy (D2,
                                          v2.17: a review flag, not a deletion)
                                          and is recorded in quarantined_paths
      DROP / SUPPRESS / MERGE_INTO     -> remove the path (only reachable when
                                          every hard invariant permitted it)
      RE_DERIVE                        -> no mutation; the run is HELD
      ADD_SECTION / ADD_SUBTOPIC       -> no mutation; recorded in `blocked`,
                                          which HOLDS the run (INV-9)

    With no Tier 2 actions, final_taxonomy is scan_taxonomy unchanged.
    """
    final = {sec: {top: list(subs or []) for top, subs in (topics or {}).items()}
             for sec, topics in (scan_taxonomy or {}).items()}
    quarantined, blocked = [], []
    live = {normalize_label(path_str(*p)) for p in enumerate_paths(scan_taxonomy)}
    remove = set()

    for entry in list(resolved) + list(adjudications):
        action = entry.get("action")
        item = entry.get("item")
        if action == "QUARANTINE":
            quarantined.append(item)
        elif action in REMOVING:
            # INV-10 RESOLVABLE_TARGET. A destructive action must name a LIVE
            # taxonomy path. `item` is a path string ONLY for PATH_EXTRA — and
            # PATH_EXTRA is resolved at Tier 1 (RETAIN / QUARANTINE) and never
            # reaches a destructive action. Every class that CAN be adjudicated
            # destructively carries a description, a subject name, or raw
            # syllabus text instead. Matching those against a path yields no
            # hit, so an unguarded removal SILENTLY does nothing while the
            # record asserts the path was dropped.
            # The taxonomy is unharmed either way, but the record would LIE, and
            # a record that misstates what happened is the failure this release
            # exists to remove. Unresolvable => blocked => HELD.
            key = normalize_label(str(item))
            if key in live:
                remove.add(key)
            else:
                blocked.append({
                    "class": entry.get("class"), "item": item, "action": action,
                    "reason": "destructive action does not resolve to a live taxonomy "
                              "path; it cannot be applied and MUST NOT be recorded as "
                              "applied (INV-10)"})
        elif action in UNMATERIALISABLE:
            blocked.append({
                "class": entry.get("class"), "item": item, "action": action,
                "reason": "would require S4-0 to DERIVE new taxonomy structure "
                          "(INV-9); re-run PYQDraft"})

    if remove:
        for sec, topics in list(final.items()):
            for top, subs in list(topics.items()):
                final[sec][top] = [s for s in subs
                                   if normalize_label(path_str(sec, top, s)) not in remove]
    return final, quarantined, blocked


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


def build_approval_record(exam_code, findings, resolved, adjudications, conservation,
                          mode="FULL", ledger=None, blocked=None, prior_record=None,
                          final_taxonomy=None, amber_status=None,
                          subject_flags=None, dedup_report=None, telemetry=None):
    """
    mode    : "FULL" | "DEGRADED" — MUST match the mode reconcile() ran under.
    ledger  : the CheckLedger reconcile() attested into. FAIL-SAFE: None means
              nothing can be proven to have run, so every expected check is
              missing and the status is HELD. Unknown is never CLEAN.
    blocked : materialise()'s unmaterialisable actions (INV-9).
    amber_status : the draft's (and, merged, the scan's) declared AMBER residue
              (E7/S1). Recorded verbatim; matching adjudications are guarded
              out of hard[] defensively; the declared_amber summary is derived
              from `resolved` entries with by == DECLARED_AMBER.
    subject_flags / dedup_report / telemetry : the draft's E5/S2 provenance
              blocks (§6.5 handshake map — Approve is their consumer of
              record). Recorded verbatim; skeletal subjects additionally
              yield the density_unjudged note. Absence semantics: {} / [] /
              [] — no flags, no merges, no auto-corrections.
    v1.4: stamps spec_generation (E4); writes re_derive_directive on HELD (E3).
    """
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; expected one of {MODES}")

    # E4 DEFENSE: against a pre-release lock, a NEW-class adjudication must
    # never hold — grandfather() upstream makes these Tier 0, but a caller
    # that skipped it must still not newly HELD the back catalog.
    _pre_release_lock = bool(prior_record) and not prior_record.get("spec_generation")
    # E7 DEFENSE: a declared amber residue must never hold, whatever path
    # brought its adjudication here.
    _residues = _amber_residues(amber_status)

    def _holds(a):
        if a["action"] != "RE_DERIVE":
            return False
        if _pre_release_lock and a.get("class") in NEW_FINDING_CLASSES:
            return False
        if _residues and (a.get("class"),
                          normalize_label(str(a.get("item") or ""))) in _residues:
            return False
        return True

    hard = [a for a in adjudications if _holds(a)] + \
           [f for f in findings if f["class"] == "RATIO_HARDSTOP"]

    # D3 (v2.17): INV-5 must GATE the verdict. A failed conservation check
    # previously left status CLEAN, making the invariant decorative.
    if conservation and not conservation.get("pass", True):
        hard = hard + [{"item": "INV-5 CONSERVATION FAILED — "
                                f"{conservation.get('orphaned_questions', 0)} question(s) orphaned",
                        "action": "RE_DERIVE"}]

    # INV-9 NO_DERIVATION_AT_S4_0 (N-9): an adjudicated action S4-0 cannot apply
    # without inventing taxonomy structure must never be silently discarded.
    for b in (blocked or []):
        inv = "INV-10" if "does not resolve" in (b.get("reason") or "") else "INV-9"
        hard = hard + [{"item": f"{inv} UNAPPLIED_ACTION — {b.get('class')}: {b.get('item')} "
                                f"was adjudicated {b.get('action')} but could not be applied. "
                                f"{b.get('reason', '')}",
                        "action": "RE_DERIVE"}]

    # INV-7 CHECK_COMPLETENESS + INV-8 CHECK_MEASURED.
    checks = (ledger or CheckLedger()).as_dict(mode)
    if checks["missing"]:
        hard = hard + [{"item": "INV-7 INCOMPLETE_RECONCILIATION — expected check(s) "
                                f"did not execute: {', '.join(checks['missing'])}",
                        "action": "RE_DERIVE"}]
    if checks["vacuous"]:
        hard = hard + [{"item": "INV-8 VACUOUS_CHECK — check(s) executed but measured "
                                f"nothing over non-empty inputs: {', '.join(checks['vacuous'])}. "
                                "A check that measures nothing cannot be distinguished "
                                "from one that passed.",
                        "action": "RE_DERIVE"}]
    if checks["c4_form"] == "LEGACY_IMPORT_FALLBACK":
        hard = hard + [{"item": "INV-8 DEGRADED_MEASUREMENT — syllabus_style was present "
                                "but syllabus_provenance could not be imported, so C4 "
                                "applied LEGACY thresholds to an exam that must be "
                                "judged on style-aware thresholds.",
                        "action": "RE_DERIVE"}]

    if hard:
        status = "HELD"
    elif mode == "DEGRADED":
        status = "DEGRADED"            # a degraded record MUST NOT report CLEAN
    elif adjudications:
        status = "CLEAN_ADJUDICATED"   # Tier 2 ran, all safely resolved, taxonomy locked
    else:
        status = "CLEAN"

    # D-4: report the thresholds ACTUALLY applied, per the C4 form that ran.
    thresholds = {"MIN_PATTERN_SIZE": MIN_PATTERN_SIZE, "DUP_SIMILARITY": DUP_SIMILARITY,
                  "OVER_AGG_ITEMS_PER_TOPIC": OVER_AGG_ITEMS_PER_TOPIC,
                  "OVER_AGG_MIN_ITEMS": OVER_AGG_MIN_ITEMS}
    if checks["c4_form"] == "STYLE_AWARE":
        try:
            from syllabus_provenance import (RATIO_ENUM_WARN, RATIO_ENUM_STOP,
                                             RATIO_PROSE_WARN, RATIO_PROSE_STOP)
            thresholds["C4"] = {
                "form": "STYLE_AWARE",
                "ENUMERATED": {"warn": RATIO_ENUM_WARN, "hardstop": RATIO_ENUM_STOP,
                               "basis": "entries"},
                "PROSE": {"warn": RATIO_PROSE_WARN, "hardstop": RATIO_PROSE_STOP,
                          "basis": "atomic concepts"},
            }
        except ImportError:
            thresholds["C4"] = {"form": "STYLE_AWARE", "detail": "provenance unavailable"}
    elif checks["c4_form"]:
        thresholds["C4"] = {"form": checks["c4_form"], "warn": RATIO_WARN,
                            "hardstop": RATIO_HARDSTOP, "basis": "syllabus items"}

    # N-7: replay is preserved verbatim (INV-6) but is now LABELLED, not trusted.
    prior_attested = None
    if prior_record is not None:
        prior_attested = bool(prior_record.get("checks", {}).get("executed"))

    # v1.2 (GAP-2026-07-25-002): ATTEST THE TAXONOMY THAT WAS LOCKED.
    # Until now this record proved the reconciliation RAN — status, mode, ledger,
    # conservation — and said nothing about WHAT it locked. PYQSort could therefore
    # verify the lock was earned and still sort against a completely different
    # taxonomy, which is precisely what Defect B did: it flattened six subjects into
    # one and passed every check in this record cleanly. A lock that does not name
    # its subject is a receipt for an unnamed thing.
    # Computed over slugify()-normalised triples so it is invariant to the cosmetic
    # variance the subtopic_id contract already tolerates, and sensitive to
    # everything else. Verified downstream at PYQSort S1-0b.
    #
    # FAIL-SAFE, NOT FAIL-CONVENIENT: when no taxonomy is supplied the key is
    # OMITTED, never emitted over an empty dict. A fingerprint of nothing is a
    # well-formed value that would match nothing, so PYQSort S1-0b would report a
    # content MISMATCH — pointing the operator at the Analysis doc, which is not
    # where the fault is. An absent key instead triggers S1-0b's "no fingerprint"
    # branch, which names the real cause: the record was built by a caller that
    # does not yet pass final_taxonomy. Unknown is never attested.
    _record = {
        "exam_code": exam_code,
        "schema_version": SCHEMA_VERSION,
        # E4: the generation stamp. Its ABSENCE in a prior record is what
        # identifies a pre-release lock (grandfathering, F1 tripwire, A1).
        "spec_generation": SPEC_GENERATION,
        "status": status,
        "mode": mode,
        "engine": "S4-0 reconcile_taxonomy",
        "engine_version": ENGINE_VERSION,
        "checks": checks,
        # E7/S1: the declared residue, verbatim, and the Tier-0 resolutions it
        # produced. declared_amber entries live in auto_resolved (below) — NOT
        # in adjudications — so INV-6 replay can never resurrect a waiver.
        "amber_status": amber_status,
        "declared_amber": [r for r in (resolved or [])
                           if r.get("by") == "DECLARED_AMBER"],
        # §6.5 handshake — the draft's provenance blocks, carried into the
        # record verbatim (the S4 operator-audit habit reads them HERE).
        "subject_flags": subject_flags or {},
        "dedup_report": dedup_report or [],
        "telemetry": telemetry or [],
        # E5/D5: skeletal subjects have too few entries to judge density and
        # too much content to be small — the record SAYS so (Tier-0 note)
        # instead of the shape looking silently anomalous downstream.
        "density_unjudged": sorted(
            s for s, fl in (subject_flags or {}).items()
            if isinstance(fl, dict) and fl.get("skeletal")),
        "prior_record_attested": prior_attested,
        "thresholds": thresholds,
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
        "unmaterialisable": list(blocked or []),
        "conservation": conservation,
    }
    if final_taxonomy:
        _triples = [(sec, top, sub)
                    for sec, tops in final_taxonomy.items()
                    for top, subs in tops.items()
                    for sub in subs]
        _record["taxonomy_fingerprint"] = taxonomy_fingerprint(_triples)
        _record["taxonomy_counts"] = {
            "subjects": len(final_taxonomy),
            "topics": sum(len(t) for t in final_taxonomy.values()),
            "subtopics": len(_triples)}
        # v1.3 — THE APPROVED TAXONOMY ITSELF, not merely its hash.
        #
        # This function has always RECEIVED final_taxonomy in exactly the shape four
        # downstream steps need, derived a fingerprint from it, and then thrown it
        # away — leaving Steps 3, 4, 5 and 6 to reconstruct the same structure by
        # parsing a Word document. That reconstruction is what GAP-2026-07-25-003
        # severed on every exam at once, because the platform stores an uploaded
        # .docx in project knowledge as extracted TEXT under its .docx name.
        #
        # A hash proves identity and cannot restore content. Persisting the taxonomy
        # makes the record self-sufficient: JSON is byte-preserved by the platform
        # (unlike .docx and .pdf), the fingerprint recorded beside it validates it
        # with no new trust, and syllabus_provenance.read_taxonomy_draft() already
        # reads this exact {"sections": {sec: {top: [sub]}}} shape. The Analysis doc
        # becomes what it should always have been: a HUMAN deliverable.
        #
        # ORDER IS LOAD-BEARING and is preserved. Subject order sets subject_order
        # and within-subject topic order sets topic_idx, which is POSITIONAL. dicts
        # and json.dump both preserve insertion order, so the order written here is
        # the order every consumer sees.
        #
        # Emitted only when final_taxonomy is supplied — the same fail-safe rule as
        # the fingerprint above. An absent key means "this record was built by a
        # caller that does not pass final_taxonomy", never "the taxonomy is empty".
        _record["taxonomy"] = {
            "sections": {sec: {top: list(subs) for top, subs in tops.items()}
                         for sec, tops in final_taxonomy.items()}}

    # ── E3 (v1.4): RE-DERIVE DIRECTIVE — machine-readable, HELD only ──────
    # Branch B's "re-run PYQDraft" was memoryless: each step runs in a fresh
    # chat, so the re-run could plausibly reproduce the rejected shape (the
    # RPSC infinite-loop hazard). The directive names WHICH topics are
    # crowded, states each constraint, and pins the rejected fingerprint;
    # PYQDraft S2-0 consumes it as HARD constraints (D1a) — that consumption
    # is what makes the Approve->Draft loop convergent across sessions.
    if status == "HELD":
        _crowded, _seen = [], set()
        for f in findings:
            for c in (f.get("crowded_topics") or []):
                k = normalize_label(c.get("topic"))
                if k not in _seen:
                    _seen.add(k)
                    _crowded.append({"topic": c.get("topic"),
                                     "item_count": c.get("item_count")})
        _tier2 = [{"id": f.get("id"), "class": f.get("class"),
                   "item": f.get("item"), "detail": f.get("detail")}
                  for f in findings if f.get("tier") == 2]
        _constraints = [
            f"topic '{c['topic']}' must be split — its {c['item_count']} "
            f"syllabus items ARE the Topics (EC-P20)"
            for c in _crowded]
        for h in hard:
            it = str(h.get("item") or "")
            if it and not any(c["topic"] and c["topic"] in it for c in _crowded):
                _constraints.append(f"resolve: {it}")
        _record["re_derive_directive"] = {
            "findings": _tier2,
            "crowded_topics": _crowded,
            "constraints": _constraints,
            "rejected_fingerprint": _record.get("taxonomy_fingerprint"),
        }
    return _record


# ══════════════════════════════════════════════════════════════════
# SELF-TEST
# ══════════════════════════════════════════════════════════════════
def _self_test():
    ok, fail = 0, []

    def ck(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    def full(items, tax, **kw):
        led = CheckLedger()
        f = reconcile(items, tax, kw.pop("cls", {}), {}, ledger=led, **kw)
        return f, led

    def classes(f):
        return {x["class"] for x in f}

    # ---- fixtures -------------------------------------------------
    DUP_TAX = {"A": {"T": ["Node One — Form and Use", "Node Two — Form and Use"]}}
    DUP_ITEMS = [{"id": "S1", "subject": "A", "raw_text": "x",
                  "mapped_paths": [["A", "T", "Node One — Form and Use"],
                                   ["A", "T", "Node Two — Form and Use"]]}]
    STYLE = {"A": {"style": "PROSE", "entries": 1, "atomic": 6}}

    # ---- T1: THE REGRESSION (D-1). Fails by construction on v1.0. ----
    f, led = full(DUP_ITEMS, DUP_TAX, syllabus_subjects=["A"],
                  unanchorable_subjects=["A"], syllabus_style=STYLE)
    ck("T1a C5 runs under style-aware C4", "NEAR_DUPLICATE" in classes(f))
    ck("T1b C7 runs under style-aware C4", "UNANCHORABLE_SUBJECT" in classes(f))
    ck("T1c all FULL checks attested", led.as_dict("FULL")["missing"] == [])
    ck("T1d C4 form recorded STYLE_AWARE", led.form("C4") == "STYLE_AWARE")

    # ---- T2: legacy path still complete ----
    f, led = full(DUP_ITEMS, DUP_TAX, syllabus_subjects=["A"],
                  unanchorable_subjects=["A"], syllabus_style=None)
    ck("T2a C5 runs on legacy C4", "NEAR_DUPLICATE" in classes(f))
    ck("T2b C7 runs on legacy C4", "UNANCHORABLE_SUBJECT" in classes(f))
    ck("T2c C4 form recorded LEGACY", led.form("C4") == "LEGACY")
    ck("T2d no checks missing", led.as_dict("FULL")["missing"] == [])

    # ---- T3: the two C4 forms are mutually exclusive ----
    ck("T3 exactly one C4 form per run", led.form("C4") in ("LEGACY", "STYLE_AWARE"))

    # ---- T4 (N-1): normalized subject match ----
    TAX4 = {"General Biology": {"T": ["s%d" % i for i in range(50)]}}
    IT4 = [{"id": "S1", "subject": "General Biology", "raw_text": "x", "mapped_paths": []}]
    for label, key in (("exact", "General Biology"),
                       ("case", "GENERAL BIOLOGY"),
                       ("spacing", "General  Biology")):
        f, led = full(IT4, TAX4, syllabus_subjects=["General Biology"],
                      syllabus_style={key: {"style": "PROSE", "entries": 0, "atomic": 5}})
        ck(f"T4 C4 measures under {label} variance", led.entries["C4"]["domain"] == 1)
        ck(f"T4 C4 not vacuous under {label}", not led.entries["C4"]["vacuous"])

    # ---- T5 (INV-8): a genuinely unmatchable style key is VACUOUS -> HELD ----
    f, led = full(IT4, TAX4, syllabus_subjects=["General Biology"],
                  syllabus_style={"Chemistry": {"style": "PROSE", "entries": 0, "atomic": 5}})
    ck("T5a C4 vacuous when no style key matches", "C4" in led.vacuous())
    rec = build_approval_record("X", f, [], [], {"pass": True}, mode="FULL", ledger=led)
    ck("T5b vacuous check forces HELD", rec["status"] == "HELD")
    ck("T5c vacuous check is named", any("INV-8" in r for r in rec["summary"]["held_reasons"]))

    # ---- T6 (INV-7): fail-safe when caller does not attest ----
    rec = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL", ledger=None)
    ck("T6a no attestation -> HELD", rec["status"] == "HELD")
    ck("T6b missing checks named", rec["checks"]["missing"] == sorted(CHECK_IDS))

    # ---- T7 (N-9 / INV-9): ADD_* holds instead of silently dropping ----
    items7 = [{"id": "S1", "subject": "Chemistry", "raw_text": "Organic", "mapped_paths": []},
              {"id": "S2", "subject": "Bio", "raw_text": "Cells",
               "mapped_paths": [["Bio", "T", "Cells"]]}]
    tax7 = {"Bio": {"T": ["Cells"]}}
    f, led = full(items7, tax7, syllabus_subjects=["Bio", "Chemistry"])
    res, esc = apply_tier1(f)
    adj = adjudicate(esc, {}, None)
    fin, quar, blocked = materialise(tax7, res, adj)
    rec = build_approval_record("X", f, res, adj, conservation_check({}, fin, quar),
                                mode="FULL", ledger=led, blocked=blocked)
    ck("T7a SUBJECT_MISSING detected", "SUBJECT_MISSING" in classes(f))
    ck("T7b ITEM_UNMAPPED detected", "ITEM_UNMAPPED" in classes(f))
    ck("T7c ADD_* reported unmaterialisable", len(blocked) == 2)
    ck("T7d run is HELD, not CLEAN_ADJUDICATED", rec["status"] == "HELD")
    ck("T7e INV-9 named in held_reasons",
       any("INV-9" in r for r in rec["summary"]["held_reasons"]))
    ck("T7f taxonomy NOT mutated", fin == {"Bio": {"T": ["Cells"]}})

    # ---- T8 (N-4): C6 scale-relative ----
    # v1.4 fixture update (E1c): the old shape mapped all 12 items into ONE of
    # the three topics, which the corrected denominator now CORRECTLY fires on
    # (T2/T3 were reachable by no item — they diluted the pre-v1.4 measure).
    # The small-exam protection being proven is a small syllabus SPREAD across
    # its topics: 12 items over 3 anchored topics = 4.0 < 5.0, and 4 < cap.
    small_items = [{"id": f"S{i}", "subject": "Bio", "raw_text": "t",
                    "mapped_paths": [["Bio", f"T{i % 3 + 1}", "a"]]}
                   for i in range(12)]
    small_tax = {"Bio": {"T1": ["a"], "T2": ["b"], "T3": ["c"]}}
    f, led = full(small_items, small_tax, syllabus_subjects=["Bio"])
    ck("T8a small exam not over-aggregated", "TOPIC_OVER_AGGREGATION" not in classes(f))
    crushed_items = [{"id": f"S{i}", "subject": "Bio", "raw_text": "t",
                      "mapped_paths": [["Bio", "T1", "a"]]} for i in range(40)]
    f2, _ = full(crushed_items, {"Bio": {"T1": ["a"], "T2": ["b"]}}, syllabus_subjects=["Bio"])
    ck("T8b crushed syllabus IS over-aggregated", "TOPIC_OVER_AGGREGATION" in classes(f2))

    # ---- T9 (D-2/D-3): DEGRADED mode ----
    locked = {"A": {"T": ["Node One — Form and Use", "Node Two — Form and Use"]}}
    led = CheckLedger()
    f = reconcile([], DUP_TAX, {}, {}, mode="DEGRADED", locked_taxonomy=locked, ledger=led)
    d = led.as_dict("DEGRADED")
    ck("T9a DEGRADED runs C3+C5 only", set(d["executed"]) == {"C3", "C5"})
    ck("T9b DEGRADED declares C1/C2/C4/C6/C7 skipped",
       set(d["declared_skipped"]) == {"C1", "C2", "C4", "C6", "C7"})
    ck("T9c DEGRADED emits no RATIO_HARDSTOP (D-3)", "RATIO_HARDSTOP" not in classes(f))
    ck("T9d DEGRADED emits no SUBJECT_EXTRA storm", "SUBJECT_EXTRA" not in classes(f))
    ck("T9e C3 measured vs locked taxonomy", "PATH_EXTRA" not in classes(f))
    rec = build_approval_record("X", f, [], [], {"pass": True}, mode="DEGRADED", ledger=led)
    ck("T9f status is DEGRADED", rec["status"] == "DEGRADED")
    ck("T9g DEGRADED is never CLEAN", rec["status"] != "CLEAN")
    try:
        reconcile([], DUP_TAX, {}, {}, mode="DEGRADED", ledger=CheckLedger())
        ck("T9h missing locked_taxonomy raises", False)
    except ValueError:
        ck("T9h missing locked_taxonomy raises", True)

    # ---- T10: unknown mode rejected ----
    try:
        reconcile([], {}, {}, {}, mode="TYPO", ledger=CheckLedger())
        ck("T10 unknown mode raises", False)
    except ValueError:
        ck("T10 unknown mode raises", True)

    # ---- T11: determinism + INV-6 replay ----
    a, _ = full(DUP_ITEMS, DUP_TAX, syllabus_subjects=["A"], syllabus_style=STYLE)
    b, _ = full(DUP_ITEMS, DUP_TAX, syllabus_subjects=["A"], syllabus_style=STYLE)
    ck("T11a finding IDs stable", [x["id"] for x in a] == [x["id"] for x in b])
    prior = {"adjudications": [{"id": x["id"], "class": x["class"], "item": x["item"],
                                "action": "RETAIN_BOTH"}
                               for x in a if x["class"] == "NEAR_DUPLICATE"],
             "checks": {"executed": list(CHECK_IDS)}}
    _, esc = apply_tier1(a)
    adj = adjudicate(esc, {}, prior)
    ck("T11b prior verdicts replayed", all(x.get("replayed") for x in adj if x["id"] in
                                           {p["id"] for p in prior["adjudications"]}))
    rec = build_approval_record("X", a, [], adj, {"pass": True}, mode="FULL",
                                ledger=CheckLedger() if False else _full_ledger(),
                                prior_record=prior)
    ck("T11c prior record attestation recorded", rec["prior_record_attested"] is True)
    rec2 = build_approval_record("X", a, [], adj, {"pass": True}, mode="FULL",
                                 ledger=_full_ledger(), prior_record={"adjudications": []})
    ck("T11d unattested prior flagged", rec2["prior_record_attested"] is False)

    # ---- T14 (INV-10): destructive action that resolves to no live path ----
    tax14 = {"A": {"T": ["Alpha Beta Gamma", "Alpha Beta Gamme"]}}
    led14 = CheckLedger()
    f14 = reconcile([], tax14, {}, {}, syllabus_subjects=["A"], ledger=led14)
    nd = [x for x in f14 if x["class"] == "NEAR_DUPLICATE"]
    ck("T14a NEAR_DUPLICATE detected", bool(nd))
    adj14 = adjudicate(nd, {nd[0]["id"]: {"action": "DROP", "confidence": "HIGH",
                                          "syllabus_quote": "q"}}, None)
    ck("T14b DROP survives the hard invariants", adj14[0]["action"] == "DROP")
    fin14, q14, bl14 = materialise(tax14, [], adj14)
    ck("T14c unresolvable DROP is BLOCKED, not silently dropped", len(bl14) == 1)
    ck("T14d taxonomy left intact", fin14 == tax14)
    rec14 = build_approval_record("X", f14, [], adj14, {"pass": True},
                                  mode="FULL", ledger=_full_ledger(), blocked=bl14)
    ck("T14e unapplied action forces HELD", rec14["status"] == "HELD")
    ck("T14f INV-10 named in held_reasons",
       any("INV-10" in r for r in rec14["summary"]["held_reasons"]))
    # a RESOLVABLE destructive action must still work
    resolvable = [{"class": "PATH_EXTRA", "item": "A/T/Alpha Beta Gamma", "action": "DROP"}]
    fin15, _, bl15 = materialise(tax14, [], resolvable)
    ck("T14g resolvable DROP still removes the path",
       fin15["A"]["T"] == ["Alpha Beta Gamme"] and bl15 == [])

    # ---- T12: invariants must not regress ----
    fx = {"class": "PATH_EXTRA", "pyq_count": 5}
    act, notes = enforce_invariants(fx, {"action": "DROP", "confidence": "HIGH",
                                         "syllabus_quote": "q"})
    ck("T12a INV-2 protects PYQ-backed path", act == "RETAIN")
    act, _ = enforce_invariants({"class": "NEAR_DUPLICATE", "pyq_count": 0},
                                {"action": "DROP", "confidence": "LOW",
                                 "syllabus_quote": "q"})
    ck("T12b INV-3 low confidence -> safe default", act == "RETAIN_BOTH")

    # ---- T13: schema / stamping ----
    rec = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                ledger=_full_ledger())
    ck("T13a schema 1.4", rec["schema_version"] == "1.4")

    # ---- T15 (E1b): per-topic form closes the mixed-shape blind spot ----
    # 1 topic x 20 items + 15 topics x 1 item: average 35/16 = 2.2 PASSES the
    # subject form; the 20-in-one topic is caught per-topic.
    mixed_items = ([{"id": f"M{i}", "subject": "His", "raw_text": "t",
                     "mapped_paths": [["His", "Big", f"s{i}"]]} for i in range(20)]
                   + [{"id": f"N{i}", "subject": "His", "raw_text": "t",
                       "mapped_paths": [["His", f"P{i}", "x"]]} for i in range(15)])
    mixed_tax = {"His": {"Big": [f"s{i}" for i in range(20)],
                         **{f"P{i}": ["x"] for i in range(15)}}}
    f15 = check_topic_density(mixed_items, mixed_tax)
    c15 = {x["class"] for x in f15}
    ck("T15a subject average passes on the mixed shape",
       "TOPIC_OVER_AGGREGATION" not in c15)
    ck("T15b per-topic form catches 20-in-one",
       "TOPIC_OVER_AGGREGATION_TOPIC" in c15)
    ck("T15c the crowded topic is NAMED with its count",
       any(x.get("crowded_topics") == [{"topic": "Big", "item_count": 20}]
           for x in f15))

    # ---- T16 (E1c): denominator counts syllabus-anchored topics only ----
    # RPSC shape: 42 items mapped across 7 topics; 1 scan-discovered topic
    # holds no mapped item. True density 42/7 = 6.0, not 42/8 = 5.25.
    r_items = [{"id": f"R{i}", "subject": "Zoo", "raw_text": "t",
                "mapped_paths": [["Zoo", f"T{i % 7}", "x"]]} for i in range(42)]
    r_tax = {"Zoo": {**{f"T{i}": ["x"] for i in range(7)}, "EcoScan": ["y"]}}
    f16 = check_topic_density(r_items, r_tax)
    subj16 = [x for x in f16 if x["class"] == "TOPIC_OVER_AGGREGATION"]
    ck("T16a scan-discovered topic excluded from the denominator (6.0 fires)",
       bool(subj16) and "= 6.0 items/topic" in subj16[0]["detail"])
    ck("T16b the exclusion is reported",
       subj16 and subj16[0]["scoping"]["scan_discovered_topics"] == 1)

    # ---- T17 (E1e): scoping — anchored topics and excluded items are OUT ----
    f17 = check_topic_density(mixed_items, mixed_tax, qcount_anchored={"Big"})
    ck("T17a qcount-anchored topic exempt from the per-topic cap",
       not any(x["class"] == "TOPIC_OVER_AGGREGATION_TOPIC" for x in f17))
    x_items = [{"id": f"X{i}", "subject": "His", "raw_text": "t", "excluded":
                {"class": "VOCABULARY_LIST", "reason": "glossary"},
                "mapped_paths": []} for i in range(100)]
    # 100 excluded + 15 spread items: honored exclusion -> 15/15 = 1.0 passes;
    # a broken exclusion would measure 115/15 = 7.7 and fire.
    f17b = check_topic_density(x_items + mixed_items[20:], mixed_tax)
    subj17 = [x for x in f17b if x["class"] == "TOPIC_OVER_AGGREGATION"]
    ck("T17b excluded items out of the subject-density numerator", not subj17)
    # E2: C2 skips excluded items and attests the counts
    led17 = CheckLedger()
    f17c = reconcile(x_items, {"His": {"T": ["x"]}}, {}, {},
                     syllabus_subjects=["His"], ledger=led17)
    ck("T17c C2 emits no ITEM_UNMAPPED for declared exclusions",
       "ITEM_UNMAPPED" not in {x["class"] for x in f17c})
    ck("T17d excluded_counts attested in the C2 ledger note",
       (led17.entries["C2"]["note"] or {}).get("excluded_counts")
       == {"VOCABULARY_LIST": 100})

    # ---- T18 (E3): HELD record carries the re-derive directive ----
    crushed = [{"id": f"C{i}", "subject": "Zoo", "raw_text": "t",
                "mapped_paths": [["Zoo", "T1", "x"]]} for i in range(40)]
    ctax = {"Zoo": {"T1": ["x"], "T2": ["y"]}}
    led18 = CheckLedger()
    f18 = reconcile(crushed, ctax, {}, {}, syllabus_subjects=["Zoo"], ledger=led18)
    r18, e18 = apply_tier1(f18)
    a18 = adjudicate(e18, {}, None)
    rec18 = build_approval_record("X", f18, r18, a18, {"pass": True},
                                  mode="FULL", ledger=led18, final_taxonomy=ctax)
    ck("T18a crushed run is HELD", rec18["status"] == "HELD")
    d18 = rec18.get("re_derive_directive") or {}
    ck("T18b directive names the crowded topic with its count",
       {"topic": "T1", "item_count": 40} in d18.get("crowded_topics", []))
    ck("T18c directive carries actionable constraints",
       any("must be split" in c for c in d18.get("constraints", [])))
    ck("T18d directive pins the rejected fingerprint",
       d18.get("rejected_fingerprint") == rec18.get("taxonomy_fingerprint"))
    ck("T18e no directive on a clean record",
       "re_derive_directive" not in build_approval_record(
           "X", [], [], [], {"pass": True}, mode="FULL", ledger=_full_ledger()))

    # ---- T19 (E4): grandfathering — pre-release lock never newly HELD ----
    old_rec = {"adjudications": [], "checks": {"executed": list(CHECK_IDS)}}
    gf = grandfather(f15, old_rec)          # prior record LACKS spec_generation
    ck("T19a new-class finding rewritten to Tier 0",
       all(x["tier"] == 0 for x in gf
           if x["class"] in NEW_FINDING_CLASSES))
    ck("T19b other findings untouched",
       [x for x in gf if x["class"] not in NEW_FINDING_CLASSES]
       == [x for x in f15 if x["class"] not in NEW_FINDING_CLASSES])
    cur_rec = {"adjudications": [], "spec_generation": SPEC_GENERATION}
    ck("T19c current-generation prior record: no grandfathering",
       grandfather(f15, cur_rec) == list(f15))
    # defensive path: a NEW-class RE_DERIVE adjudication against a pre-release
    # lock must not hold even when grandfather() was skipped
    bad_adj = [{"id": "z", "class": "TOPIC_OVER_AGGREGATION_TOPIC",
                "item": "His > Big", "action": "RE_DERIVE", "by": "TIER2"}]
    rec19 = build_approval_record("X", [], [], bad_adj, {"pass": True},
                                  mode="FULL", ledger=_full_ledger(),
                                  prior_record=old_rec)
    ck("T19d defensive: pre-release lock + new-class RE_DERIVE != HELD",
       rec19["status"] != "HELD")

    # ---- T20 (E6): input-shape guards are corrective ----
    try:
        reconcile([], {}, [{"q_num": 1}], {}, ledger=CheckLedger())
        ck("T20a flattened classifications rejected", False)
    except TypeError as exc:
        ck("T20a flattened classifications rejected",
           "dict" in str(exc).lower() and "paper" in str(exc).lower())
    try:
        reconcile([], {}, {"p1": {"q": 1}}, {}, ledger=CheckLedger())
        ck("T20b non-list paper value rejected", False)
    except TypeError as exc:
        ck("T20b non-list paper value rejected", "LIST" in str(exc))
    try:
        reconcile([], {"A": ["not-a-dict"]}, {}, {}, ledger=CheckLedger())
        ck("T20c malformed scan_taxonomy rejected", False)
    except TypeError as exc:
        ck("T20c malformed scan_taxonomy rejected", "topic" in str(exc).lower())
    try:
        reconcile([], {}, {}, {}, ledger="not-a-ledger")
        ck("T20d non-CheckLedger ledger rejected", False)
    except TypeError as exc:
        ck("T20d non-CheckLedger ledger rejected", "CheckLedger" in str(exc))

    # ---- T21 (E7): DECLARED_AMBER — Tier 0, reported, never replayed ----
    # S1 SHAPE: each unresolved entry carries the finding CLASS the residue
    # will produce at Approve and its normalized identity — the draft declares
    # EVERY class its residue yields (subject form AND per-topic form here).
    amber = {"gate": "density", "rounds": 3,
             "unresolved": [{"class": "TOPIC_OVER_AGGREGATION", "item": "Zoo",
                             "detail": "unsplittable under q-count conflict"},
                            {"class": "TOPIC_OVER_AGGREGATION_TOPIC",
                             "item": "Zoo > T1",
                             "detail": "unsplittable under q-count conflict"}]}
    r21, e21 = apply_tier1(f18)             # f18 escalates TOPIC_OVER_AGGREGATION
    d21, e21b = resolve_declared_amber(e21, amber)
    ck("T21a declared residue resolved out of Tier 2",
       any(x["by"] == "DECLARED_AMBER" for x in d21)
       and not any(x["class"] == "TOPIC_OVER_AGGREGATION" for x in e21b))
    a21 = adjudicate(e21b, {}, None)
    rec21 = build_approval_record("X", f18, r21 + d21, a21, {"pass": True},
                                  mode="FULL", ledger=led18,
                                  final_taxonomy=ctax, amber_status=amber)
    ck("T21b AMBER-declared run locks (not HELD)",
       rec21["status"] in ("CLEAN", "CLEAN_ADJUDICATED"))
    ck("T21c declared_amber reported in the record",
       rec21["declared_amber"] and rec21["amber_status"] == amber)
    ck("T21d declared entries NEVER enter the replay ledger",
       not any(a.get("by") == "DECLARED_AMBER" for a in rec21["adjudications"]))
    # NON-REPLAY: a later mode-C run with a NON-amber draft, using rec21 as the
    # prior record, must judge the recurring finding FRESH — and hold on it.
    a21f = adjudicate(e21, {}, rec21)       # no amber_status this time
    rec21f = build_approval_record("X", f18, r21, a21f, {"pass": True},
                                   mode="FULL", ledger=led18,
                                   final_taxonomy=ctax)
    ck("T21e recurring finding judged FRESH on a non-AMBER re-run (HELD)",
       rec21f["status"] == "HELD"
       and not any(a.get("replayed") for a in a21f))
    # defensive: adjudicate(amber_status=...) alone also never adjudicates it
    a21d = adjudicate(e21, {}, None, amber_status=amber)
    ck("T21f adjudicate's defensive filter drops declared residues",
       not any(x["class"] == "TOPIC_OVER_AGGREGATION" for x in a21d))

    # ---- T22 (v1.4 hardening): ghost destination topic must not crash C6 ----
    ghost_items = ([{"id": f"G{i}", "subject": "S", "raw_text": "t",
                     "mapped_paths": [["S", "Ghost Topic", f"x{i}"]]}
                    for i in range(6)]
                   + [{"id": f"H{i}", "subject": "S", "raw_text": "t",
                       "mapped_paths": [["S", "Real", f"y{i}"]]}
                      for i in range(6)])
    ghost_tax = {"S": {"Real": [f"y{i}" for i in range(6)]}}
    try:
        f22 = check_topic_density(ghost_items, ghost_tax)
        ck("T22a ghost topic measured, not crashed",
           any(c["topic"] == "ghost topic" and c["item_count"] == 6
               for x in f22 for c in (x.get("crowded_topics") or [])))
    except Exception:
        ck("T22a ghost topic measured, not crashed", False)

    # ---- T23 (§6.5 handshake): provenance blocks carried into the record ----
    fl23 = {"GK": {"skeletal": True, "open_ended": True},
            "Zoo": {"skeletal": False, "open_ended": False}}
    dr23 = [{"kept": "SYL-001", "kept_text": "x", "merged_from": ["X"],
             "reason": "exact duplicate (canon-identical)"}]
    tl23 = [{"check": "density", "round": 1, "action": "split",
             "before": "1 topic", "after": "3 topics"}]
    rec23 = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                  ledger=_full_ledger(), subject_flags=fl23,
                                  dedup_report=dr23, telemetry=tl23)
    ck("T23a subject_flags / dedup_report / telemetry recorded verbatim",
       rec23["subject_flags"] == fl23 and rec23["dedup_report"] == dr23
       and rec23["telemetry"] == tl23)
    ck("T23b skeletal subject yields the density_unjudged note",
       rec23["density_unjudged"] == ["GK"])
    rec23b = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                   ledger=_full_ledger())
    ck("T23c absence semantics: {} / [] / [] / no note",
       rec23b["subject_flags"] == {} and rec23b["dedup_report"] == []
       and rec23b["telemetry"] == [] and rec23b["density_unjudged"] == [])

    # ---- T13-TAX: the record CARRIES the taxonomy (v1.3, GAP-2026-07-25-003) ----
    # A fingerprint establishes identity and cannot restore content. Until v1.3 four
    # steps recovered this structure by parsing a Word document, which is what broke
    # on every exam at once when the platform stored that document as text.
    _tx = {"General Biology": {"Cell Biology": ["Membrane", "Nucleus"],
                               "Genetics": ["Linkage"]},
           "Physics": {"Mechanics": ["Kinematics"]}}
    _rt = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                ledger=_full_ledger(), final_taxonomy=_tx)
    ck("T13-TAX taxonomy is recorded", "taxonomy" in _rt)
    ck("T13-TAX recorded under 'sections', the read_taxonomy_draft shape",
       set(_rt["taxonomy"]) == {"sections"})
    ck("T13-TAX round-trips through JSON unchanged",
       json.loads(json.dumps(_rt["taxonomy"]))["sections"] == _tx)
    ck("T13-TAX subject ORDER preserved (drives subject_order)",
       list(json.loads(json.dumps(_rt["taxonomy"]))["sections"])
       == ["General Biology", "Physics"])
    ck("T13-TAX topic ORDER preserved within a subject (drives positional topic_idx)",
       list(json.loads(json.dumps(_rt["taxonomy"]))["sections"]["General Biology"])
       == ["Cell Biology", "Genetics"])
    ck("T13-TAX subtopic ORDER preserved",
       _rt["taxonomy"]["sections"]["General Biology"]["Cell Biology"]
       == ["Membrane", "Nucleus"])
    ck("T13-TAX counts agree with the recorded taxonomy",
       _rt["taxonomy_counts"] == {"subjects": 2, "topics": 3, "subtopics": 4})
    _rtt = [(a, b, c) for a, t in _rt["taxonomy"]["sections"].items()
            for b, xs in t.items() for c in xs]
    ck("T13-TAX the recorded fingerprint validates the recorded taxonomy",
       taxonomy_fingerprint(_rtt) == _rt["taxonomy_fingerprint"])
    ck("T13-TAX taxonomy is OMITTED when no final_taxonomy is supplied",
       "taxonomy" not in build_approval_record("X", [], [], [], {"pass": True},
                                               mode="FULL", ledger=_full_ledger()))
    ck("T13-TAX the writer does not alias the caller's dict",
       (_tx["Physics"]["Mechanics"].append("SCRIBBLE") or True)
       and _rt["taxonomy"]["sections"]["Physics"]["Mechanics"] == ["Kinematics"])

    # ---- T13-FP: taxonomy attestation (v1.2, GAP-2026-07-25-002) ----
    # A record that does not name the taxonomy it locked cannot be matched against
    # the doc PYQSort loads; that gap is what let Defect B pass the lock gate.
    _tx = {"Physics": {"Mechanics": ["Kinematics", "Newton Laws"]},
           "Chemistry": {"Bonding": ["Ionic"]}}
    _r1 = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                ledger=_full_ledger(), final_taxonomy=_tx)
    ck("T13-FP1 fingerprint present", bool(_r1.get("taxonomy_fingerprint")))
    ck("T13-FP2 counts attested",
       _r1["taxonomy_counts"] == {"subjects": 2, "topics": 2, "subtopics": 3})
    _tx2 = {"Physics": {"Mechanics": ["Kinematics"]},
            "Chemistry": {"Bonding": ["Ionic"]}}
    _r2 = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                ledger=_full_ledger(), final_taxonomy=_tx2)
    ck("T13-FP3 a changed taxonomy changes the fingerprint",
       _r1["taxonomy_fingerprint"] != _r2["taxonomy_fingerprint"])
    # SUBJECT FLATTENING must change it — this is the exact Defect B shape, and a
    # fingerprint that survived it would attest nothing.
    _flat = {"Physics": {"Mechanics": ["Kinematics", "Newton Laws"],
                         "Bonding": ["Ionic"]}}
    _r3 = build_approval_record("X", [], [], [], {"pass": True}, mode="FULL",
                                ledger=_full_ledger(), final_taxonomy=_flat)
    ck("T13-FP4 subject flattening changes the fingerprint",
       _r1["taxonomy_fingerprint"] != _r3["taxonomy_fingerprint"])
    ck("T13-FP5 cosmetic variance does NOT change it",
       _r1["taxonomy_fingerprint"] == build_approval_record(
           "X", [], [], [], {"pass": True}, mode="FULL", ledger=_full_ledger(),
           final_taxonomy={"physics": {"Mechanics ": ["Kinematics", "Newton  Laws"]},
                           "CHEMISTRY": {"Bonding": ["Ionic"]}}
       )["taxonomy_fingerprint"])
    ck("T13b engine version stamped", rec["engine_version"] == ENGINE_VERSION)
    ck("T13c mode stamped", rec["mode"] == "FULL")
    ck("T13d clean run is CLEAN", rec["status"] == "CLEAN")

    print(f"SELF-TEST: {ok}/{ok + len(fail)} PASS")
    for n in fail:
        print("  FAIL:", n)
    return not fail


def _full_ledger():
    """A ledger attesting every FULL check ran over a non-empty domain."""
    led = CheckLedger()
    for c in CHECK_IDS:
        led.record(c, domain=1, inputs_present=True,
                   form="STYLE_AWARE" if c == "C4" else None)
    return led


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if _self_test() else 1)
    print(__doc__.strip().splitlines()[0])
