"""
reconcile_taxonomy.py v1.3 — Taxonomy Reconciliation Engine, Framework_PYQAnalyse S4-0

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

ENGINE_VERSION = "reconcile_taxonomy.py v1.3"
SCHEMA_VERSION = "1.3"

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
              name_canonicalizations=None, syllabus_style=None,
              mode="FULL", locked_taxonomy=None, ledger=None):
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
        for it in syllabus_items:
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
                      findings=len(findings) - n0)

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
    items_by_subject = {}
    for it in syllabus_items:
        items_by_subject.setdefault(normalize_label(it.get("subject")), []).append(it)
    if "C6" in run:
        n0 = len(findings)
        matched = 0
        for nk, sec in tax_sections.items():
            n_topics = len(scan_taxonomy.get(sec, {}) or {})
            n_items = len(items_by_subject.get(nk, []))
            if n_items:
                matched += 1
            density = n_items / max(n_topics, 1)
            if n_items >= OVER_AGG_MIN_ITEMS and density >= OVER_AGG_ITEMS_PER_TOPIC:
                findings.append({
                    "id": fingerprint("TOPIC_OVER_AGGREGATION", sec),
                    "class": "TOPIC_OVER_AGGREGATION", "tier": 2, "item": sec, "pyq_count": 0,
                    "detail": f"{n_topics} topic(s) for {n_items} syllabus items "
                              f"= {density:.1f} items/topic "
                              f"(>= {OVER_AGG_ITEMS_PER_TOPIC}) — over-aggregated.",
                })
        # Vacuity guard: syllabus items exist but none attached to any taxonomy
        # section => the subject keys never met and C6 measured nothing.
        ledger.record("C6", domain=matched if syllabus_items else len(tax_sections),
                      inputs_present=bool(tax_sections) and bool(syllabus_items),
                      findings=len(findings) - n0)

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
                          final_taxonomy=None):
    """
    mode    : "FULL" | "DEGRADED" — MUST match the mode reconcile() ran under.
    ledger  : the CheckLedger reconcile() attested into. FAIL-SAFE: None means
              nothing can be proven to have run, so every expected check is
              missing and the status is HELD. Unknown is never CLEAN.
    blocked : materialise()'s unmaterialisable actions (INV-9).
    """
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; expected one of {MODES}")

    hard = [a for a in adjudications if a["action"] == "RE_DERIVE"] + \
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
        "status": status,
        "mode": mode,
        "engine": "S4-0 reconcile_taxonomy",
        "engine_version": ENGINE_VERSION,
        "checks": checks,
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
    small_items = [{"id": f"S{i}", "subject": "Bio", "raw_text": "t",
                    "mapped_paths": [["Bio", "T1", "a"]]} for i in range(12)]
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
    ck("T13a schema 1.3", rec["schema_version"] == "1.3")

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
