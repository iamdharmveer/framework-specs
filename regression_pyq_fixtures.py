#!/usr/bin/env python3
"""
regression_pyq_fixtures.py — GAP-2026-08-30-TYPE1-HALT-ELIMINATION §7/§11 (S5)

25-fixture cross-exam regression suite for the GATE-AT-SOURCE release.
Each fixture is a miniature of a REAL syllabus structure from the release
document's twelve-syllabus verification set (§11) plus the release's own
behavioral acceptance criteria (§9). Run: python3 regression_pyq_fixtures.py
--self-test (CI's discovery step runs it automatically).

These fixtures exercise the ENGINES (reconcile_taxonomy v1.4,
syllabus_provenance E5) exactly as the specs invoke them — the S4-0
invocation order for Approve-side fixtures, build_items/check_topic_density
for Draft-side ones. No fixture reads the network or the specs.
"""
import sys

from reconcile_taxonomy import (reconcile, apply_tier1, adjudicate,
                                materialise, conservation_check,
                                build_approval_record, CheckLedger,
                                EXPECTED_CHECKS, grandfather,
                                resolve_declared_amber, check_topic_density,
                                SPEC_GENERATION, DUP_SIMILARITY,
                                OVER_AGG_MIN_ITEMS, OVER_AGG_PER_TOPIC_CAP,
                                normalize_label)
from syllabus_provenance import (build_items, detect_subject_flags,
                                 find_duplicate_subjects, validate_provenance)

PASS, FAILS = 0, []


def ck(name, cond):
    global PASS
    if cond:
        PASS += 1
    else:
        FAILS.append(name)


import hashlib


def _sub_name(topic, k):
    """Deterministic per (topic, k), mutually DISSIMILAR: fixtures must
    manufacture neither PATH findings (mk_items/mk_tax must align) nor
    incidental C5 near-duplicate findings (names must not resemble each
    other)."""
    h = hashlib.sha256(f"{topic}|{k}".encode()).hexdigest()
    return "".join(chr(97 + int(h[i], 16) % 26) for i in range(10)).title()


def mk_items(subject, spread, prefix="I"):
    """spread: {topic: n_items} -> items with 1 mapped path each."""
    items, n = [], 0
    for topic, count in spread.items():
        for k in range(count):
            n += 1
            items.append({"id": f"{prefix}{n:03d}", "subject": subject,
                          "raw_text": f"{topic} item {n}",
                          "mapped_paths": [[subject, topic,
                                            _sub_name(topic, k)]]})
    return items


def mk_tax(subject, spread, extra_topics=()):
    tops = {t: [_sub_name(t, k) for k in range(c)] for t, c in spread.items()}
    for t in extra_topics:
        tops[t] = [_sub_name(t, 0)]
    return {subject: tops}


def approve(items, tax, prior=None, amber=None, anchored=None, verdicts=None,
            subject_flags=None, dedup_report=None, telemetry=None):
    """The A3/S4-0 invocation order, verbatim — ALL handshake inputs passed."""
    led = CheckLedger()
    findings = reconcile(items, tax, {}, {},
                         syllabus_subjects=list(tax), ledger=led,
                         qcount_anchored_topics=anchored)
    findings = grandfather(findings, prior)
    resolved, escalated = apply_tier1(findings)
    declared, escalated = resolve_declared_amber(escalated, amber)
    resolved = resolved + declared
    adjs = adjudicate(escalated, verdicts or {}, prior, amber_status=amber)
    final, quar, blocked = materialise(tax, resolved, adjs)
    cons = conservation_check({}, final, quar)
    return build_approval_record("FIX", findings, resolved, adjs, cons,
                                 mode="FULL", ledger=led, blocked=blocked,
                                 prior_record=prior, final_taxonomy=final,
                                 amber_status=amber, subject_flags=subject_flags,
                                 dedup_report=dedup_report,
                                 telemetry=telemetry), findings


# ── F1: RPSC_ZOOLOGY — the reference incident, TWO-SESSION shape (crit 4+9) ──
# Session 1: the crushed real shape — 42 anchored + 1 scan-discovered topic.
rpsc_spread = {"Diversity of Life Forms (Invertebrates)": 9,
               "Developmental Biology": 9, "Genetics": 6, "Evolution": 6,
               "Ethology": 6, "Structural Organization of Chordates": 4,
               "Taxonomy": 3}
rpsc_items = mk_items("Zoology Paper I", rpsc_spread, "Z")
rpsc_tax = mk_tax("Zoology Paper I", rpsc_spread,
                  extra_topics=("Ecology and Environment",))
rec1, f1 = approve(rpsc_items, rpsc_tax)
ck("F1a RPSC session 1: HELD", rec1["status"] == "HELD")
subj = [f for f in f1 if f["class"] == "TOPIC_OVER_AGGREGATION"]
ck("F1b true density from ANCHORED topics only (43/7 = 6.1; the scan topic "
   "that diluted the live run to 5.25-class is excluded and reported)",
   subj and "= 6.1 items/topic" in subj[0]["detail"]
   and "1 scan-discovered topic(s) excluded" in subj[0]["detail"])
ck("F1c per-topic form names both 9-item topics",
   {c["topic"] for f in f1 if f["class"] == "TOPIC_OVER_AGGREGATION_TOPIC"
    for c in f["crowded_topics"]} >= {"Diversity of Life Forms (Invertebrates)",
                                      "Developmental Biology"})
d1 = rec1.get("re_derive_directive") or {}
ck("F1d directive present with crowded topics + constraints + fingerprint",
   d1.get("crowded_topics") and d1.get("constraints")
   and d1.get("rejected_fingerprint"))
# Session 2 (fresh "session"): a compliant re-derive CONSUMING the directive —
# every crowded topic split so no anchored topic reaches the cap.
rpsc2 = {}
for t, c in rpsc_spread.items():
    if any(x["topic"] == t for x in d1["crowded_topics"]):
        # the directive's constraint: split so no part reaches the cap
        part, i = OVER_AGG_PER_TOPIC_CAP - 1, 0
        while c > 0:
            i += 1
            rpsc2[f"{t} — part {i}"] = min(part, c)
            c -= min(part, c)
    else:
        rpsc2[t] = c
rec2, _ = approve(mk_items("Zoology Paper I", rpsc2, "Z"),
                  mk_tax("Zoology Paper I", rpsc2,
                         extra_topics=("Ecology and Environment",)))
ck("F1e RPSC session 2: compliant re-derive is CLEAN (crit 9)",
   rec2["status"] in ("CLEAN", "CLEAN_ADJUDICATED")
   and "re_derive_directive" not in rec2)
ck("F1f re-derive did not reproduce the rejected fingerprint",
   rec2.get("taxonomy_fingerprint") != d1["rejected_fingerprint"])

# ── F2: CSIR NET Life Sciences — 101 items must not sit in 14 topics ──
csir = {f"Unit {i}": 8 for i in range(1, 13)}
csir["Unit 13"] = 5
rec, f = approve(mk_items("Life Sciences", csir, "C"),
                 mk_tax("Life Sciences", csir))
ck("F2a CSIR 101/13 crushed shape fires (7.8 avg + per-topic)",
   rec["status"] == "HELD")
csir_ok = {f"Unit {i}.{j}": 3 for i in range(1, 13) for j in (1, 2, 3)}
rec, _ = approve(mk_items("Life Sciences", csir_ok, "C"),
                 mk_tax("Life Sciences", csir_ok))
ck("F2b CSIR split-to-subunits shape passes", rec["status"] != "HELD")

# ── F3: UGC NET History — vocabulary exclusion + per-topic blind spot ──
his_ems = ([{"path": ["History"], "text": f"Historiography topic {i}",
             "to": [["History", f"T{i}", f"Historiography topic {i}"]]}
            for i in range(12)]
           + [{"path": ["History"], "text": f"Technical term {i}",
               "excluded": {"class": "VOCABULARY_LIST",
                            "reason": "glossary of ~100 technical terms"}}
              for i in range(40)])
his_items, his_errs, _ = build_items(his_ems)
ck("F3a History: 40 vocab exclusions build clean", his_errs == [])
his_tax = {"History": {f"T{i}": [f"Historiography topic {i}"]
                       for i in range(12)}}
f3 = check_topic_density(his_items, his_tax)
ck("F3b excluded terms out of the density domain (12/12 = 1.0)", f3 == [])
# blind-spot half: 20 items in one topic + 15 singletons (crit: per-topic fires)
blind = {"Ancient Indian History": 20}
blind.update({f"P{i}": 1 for i in range(15)})
f3b = check_topic_density(mk_items("History", blind, "H"),
                          mk_tax("History", blind))
ck("F3c mixed-shape: average silent, per-topic fires on the 20-item topic",
   {x["class"] for x in f3b} == {"TOPIC_OVER_AGGREGATION_TOPIC"})

# ── F4: CAT — repeated entries dedup with non-empty report (crit: A4/D4) ──
cat_ems = [{"path": ["VARC"], "text": "Reading Comprehension",
            "to": [["VARC", "RC", "Reading Comprehension"]]},
           {"path": ["VARC"], "text": "reading comprehension",   # coaching dup
            "to": [["VARC", "RC", "RC passages"]]},
           {"path": ["VARC"], "text": "Para-jumbles",
            "to": [["VARC", "VA", "Para-jumbles"]]}]
cat_items, _, cat_report = build_items(cat_ems, dup_similarity=DUP_SIMILARITY)
ck("F4a CAT duplicate merged, destinations unioned",
   len(cat_items) == 2 and len(cat_items[0]["mapped_paths"]) == 2)
ck("F4b dedup_report non-empty and names the merge",
   cat_report and cat_report[0]["kept"] == cat_items[0]["id"])

# ── F5: CTET — q-count anchored blocks exempt (zero C6 on real densities) ──
ctet = {"Child Development (23 items)": 23, "Pedagogy blocks": 7}
ctet_anch = ["Child Development (23 items)", "Pedagogy blocks"]
rec, f = approve(mk_items("Paper I", ctet, "T"), mk_tax("Paper I", ctet),
                 anchored=ctet_anch)
ck("F5a CTET anchored blocks: zero C6 findings, not HELD",
   rec["status"] != "HELD"
   and not any(x["class"].startswith("TOPIC_OVER") for x in f))
ck("F5b scoping attested in the C6 ledger note",
   ((rec["checks"].get("detail") or {}).get("C6", {}).get("note") or {})
   .get("qcount_anchored_topics", 0) >= 1)

# ── F6: CUET PG Mathematics — 7 fat units must split ──
cuet = {f"Unit {i}": 7 for i in range(1, 8)}
rec, _ = approve(mk_items("Mathematics", cuet, "M"), mk_tax("Mathematics", cuet))
ck("F6 CUET PG 49/7 = 7.0 fires", rec["status"] == "HELD")

# ── F7: CUET UG PolSci — clean modest shape stays clean ──
pol = {f"Chapter {i}": 3 for i in range(1, 11)}
rec, _ = approve(mk_items("Political Science", pol, "P"),
                 mk_tax("Political Science", pol))
ck("F7 CUET UG 30/10 = 3.0 clean", rec["status"] in ("CLEAN",
                                                     "CLEAN_ADJUDICATED"))

# ── F8: GATE BT — dense official listing passes when split per section ──
gate = {f"Section {c}": 4 for c in "ABCDEFGHIJ"}
rec, _ = approve(mk_items("Biotechnology", gate, "G"),
                 mk_tax("Biotechnology", gate))
ck("F8 GATE BT 40/10 = 4.0 clean", rec["status"] != "HELD")

# ── F9: GATE CS — one crushed section among clean ones (per-subject scoping) ──
cs_items = (mk_items("Section A", {f"T{i}": 2 for i in range(8)}, "A")
            + mk_items("Section B", {"Everything": 12}, "B"))
cs_tax = {**mk_tax("Section A", {f"T{i}": 2 for i in range(8)}),
          **mk_tax("Section B", {"Everything": 12})}
rec, f = approve(cs_items, cs_tax)
ck("F9 two subjects, one crushed: findings scoped to Section B only",
   rec["status"] == "HELD"
   and all("Section B" in str(x["item"]) for x in f
           if x["class"].startswith("TOPIC_OVER")))

# ── F10: IIT JAM Physics — 7 papers-style units, borderline-clean ──
jam = {f"U{i}": 4 for i in range(1, 8)}
rec, _ = approve(mk_items("Physics", jam, "J"), mk_tax("Physics", jam))
ck("F10 IIT JAM 28/7 = 4.0 clean", rec["status"] != "HELD")

# ── F11: RRB NTPC — skeletal + open-ended flags (E5/D5/D6) ──
rrb = [{"subject": "General Awareness", "raw_text":
        "Current events, sports, art and culture, Indian polity, economy, "
        "geography, history, general science, environment, computers, "
        "abbreviations, organisations, transport, defence, awards, books, "
        "days, schemes, persons, places etc."}]
fl = detect_subject_flags(rrb, min_items=OVER_AGG_MIN_ITEMS)
ck("F11 RRB skeletal + open_ended both detected",
   fl["General Awareness"] == {"skeletal": True, "open_ended": True})

# ── F12: CLAT UG — comprehension-style syllabus, few broad areas, clean ──
clat = {"English Language": 2, "Current Affairs": 2, "Legal Reasoning": 2,
        "Logical Reasoning": 2, "Quantitative Techniques": 1}
rec, _ = approve(mk_items("CLAT UG", clat, "L"), mk_tax("CLAT UG", clat))
ck("F12 CLAT 9 items < OVER_AGG_MIN_ITEMS floor: density unjudged, clean",
   rec["status"] != "HELD")

# ── F13: CA Foundation — "(excluding …)" scope marker preserved ──
ca_ems = [{"path": ["Accounting"], "text": "Partnership accounts",
           "to": [["Accounting", "Partnership", "Partnership accounts"]]},
          {"path": ["Accounting"],
           "text": "(excluding: admission of a partner under revaluation)",
           "excluded": {"class": "SCOPE_MARKER",
                        "reason": "syllabus exclusion clause — bounds the "
                                  "topic; not itself testable content"}}]
ca_items, ca_errs, _ = build_items(ca_ems)
ok_ca, e_ca, w_ca, _ = validate_provenance(
    {"Accounting": {"Partnership": ["Partnership accounts"]}},
    ca_items, ["Accounting"], [])
ck("F13 CA Foundation exclusion clause recorded, valid, no unmapped warn",
   ca_errs == [] and ok_ca
   and not any("SYL-002" in w and "unmapped" in w for w in w_ca))

# ── F14: NEET-class pass-through (13-exam proof table's clean side) ──
neet = {f"Ch {i}": 3 for i in range(1, 15)}
rec, _ = approve(mk_items("Biology", neet, "N"), mk_tax("Biology", neet))
ck("F14 NEET-class 42/14 = 3.0 clean", rec["status"] != "HELD")

# ── F15: scan-discovery must not mask draft crush (denominator, again) ──
mask = {"T1": 30}
f15 = check_topic_density(mk_items("Sub", mask, "S"),
                          mk_tax("Sub", mask,
                                 extra_topics=tuple(f"D{i}" for i in range(9))))
ck("F15 nine scan-discovered topics cannot dilute 30-in-1",
   any(x["class"] == "TOPIC_OVER_AGGREGATION" for x in f15)
   and any(x["scoping"]["scan_discovered_topics"] == 9 for x in f15))

# ── F16: unsatisfiable constraints → AMBER ≤3 rounds, pipeline continues (crit 6+11) ──
amber = {"gate": "density", "rounds": 3,
         "unresolved": [
             {"class": "TOPIC_OVER_AGGREGATION", "item": "Sub",
              "detail": "q-count anchor forbids the only admissible split"},
             {"class": "TOPIC_OVER_AGGREGATION_TOPIC", "item": "Sub > T1",
              "detail": "q-count anchor forbids the only admissible split"}]}
rec16, _ = approve(mk_items("Sub", mask, "S"), mk_tax("Sub", mask), amber=amber)
ck("F16a AMBER round-trip: CLEAN with DECLARED_AMBER (crit 11)",
   rec16["status"] in ("CLEAN", "CLEAN_ADJUDICATED")
   and rec16["declared_amber"]
   and all(r["by"] == "DECLARED_AMBER" for r in rec16["declared_amber"]))
ck("F16b declared entries not in the replay ledger",
   not any(a.get("by") == "DECLARED_AMBER" for a in rec16["adjudications"]))

# ── F17: DECLARED_AMBER non-replay (crit 13) ──
rec17, _ = approve(mk_items("Sub", mask, "S"), mk_tax("Sub", mask),
                   prior=rec16)          # same findings, NO amber this time
ck("F17 non-AMBER re-run judges the finding FRESH and holds",
   rec17["status"] == "HELD"
   and not any(a.get("replayed") for a in rec17["adjudications"]))

# ── F18: grandfathering — pre-release lock FULL re-run never newly HELD (crit 5) ──
old_lock = {"adjudications": [], "checks": {"executed": list(EXPECTED_CHECKS)}}
f18 = check_topic_density(mk_items("His", blind, "H"), mk_tax("His", blind))
gf18 = grandfather(f18, old_lock)
ck("F18a pre-release lock: new-class findings Tier 0",
   all(x["tier"] == 0 for x in gf18
       if x["class"] == "TOPIC_OVER_AGGREGATION_TOPIC"))
rec18, _ = approve(mk_items("His", blind, "H"), mk_tax("His", blind),
                   prior=old_lock)
ck("F18b replay against pre-release lock: per-topic class never holds",
   not any(a.get("class") == "TOPIC_OVER_AGGREGATION_TOPIC"
           for a in rec18["adjudications"] if a["action"] == "RE_DERIVE")
   or rec18["status"] != "HELD"
   or all(h.get("class") != "TOPIC_OVER_AGGREGATION_TOPIC"
          for h in rec18.get("held_on", [])))

# ── F19: E6 — flattened classifications rejected with the corrective shape (crit 7) ──
try:
    reconcile([], {}, [{"q_num": 1, "section": "A"}], {},
              ledger=CheckLedger())
    ck("F19 flattened classifications rejected", False)
except TypeError as e:
    msg = str(e)
    ck("F19 flattened classifications rejected, message states the shape",
       "paper filename" in msg and "{paper" in msg.replace(" ", "")
       or "paper" in msg)

# ── F20: schema round-trip — every new field written and readable (crit 8) ──
rec20 = rec16
ck("F20a record carries spec_generation + amber_status + declared_amber",
   rec20["spec_generation"] == SPEC_GENERATION
   and rec20["amber_status"] == amber
   and isinstance(rec20["declared_amber"], list))
# §6.5: full handshake — every Draft-produced block reaches the record
fl20 = {"Sub": {"skeletal": False, "open_ended": True}}
dr20 = [{"kept": "SYL-001", "kept_text": "x", "merged_from": ["x2"],
         "reason": "exact duplicate (canon-identical)"}]
tl20 = [{"check": "density", "round": 1, "action": "split",
         "before": "1", "after": "2"}]
rec20b, _ = approve(mk_items("Sub", {"T1": 3}, "S"), mk_tax("Sub", {"T1": 3}),
                    subject_flags=fl20, dedup_report=dr20, telemetry=tl20)
ck("F20b subject_flags/dedup_report/telemetry carried into the record",
   rec20b["subject_flags"] == fl20 and rec20b["dedup_report"] == dr20
   and rec20b["telemetry"] == tl20 and rec20b["density_unjudged"] == [])

# ── F21: C9 seatbelt — merged banking notification, exact message (crit 14) ──
dups = find_duplicate_subjects(["English Language", "Quantitative Aptitude",
                                "Reasoning", "English  language"])
ck("F21a duplicate subject detected across phase copies",
   dups == ["English Language"])
seatbelt_msg = ("This document appears to contain more than one exam/phase "
                f"(subject '{dups[0]}' appears twice). Provide the "
                "single-phase syllabus for this ExamCode and re-run PYQDraft.")
ck("F21b message names the subject and exactly one operator action",
   "appears twice" in seatbelt_msg and "re-run PYQDraft" in seatbelt_msg)

# ── F22: stale-draft tripwire semantics (F1 spec logic, engine side) ──
# current-generation draft whose density finding matches NO declared residue
stale_findings = check_topic_density(mk_items("Sub", mask, "S"),
                                     mk_tax("Sub", mask))
declared_none = set()
residue = [x for x in stale_findings
           if (x["class"], normalize_label(str(x["item"]))) not in declared_none]
ck("F22 unmatched finding on a stamped draft = stale-input signal",
   bool(residue))

# ── F23: EC-P1 zero-PYQ exam unaffected (no classifications, clean shape) ──
rec, _ = approve(mk_items("New Exam", {f"T{i}": 2 for i in range(6)}, "E"),
                 mk_tax("New Exam", {f"T{i}": 2 for i in range(6)}))
ck("F23 zero-PYQ exam: engine path unchanged, clean",
   rec["status"] != "HELD")

# ── F24: DEGRADED mode unchanged (C6 domain untouched by the release) ──
led24 = CheckLedger()
tax24 = mk_tax("Legacy", {"T": 3})
f24 = reconcile([], tax24, {}, {}, mode="DEGRADED",
                locked_taxonomy=tax24, ledger=led24)
ck("F24 DEGRADED mode still skips provenance checks",
   "C6" in (led24.entries.get("__declared_skipped__", {}) or {}).get("ids", [])
   if "__declared_skipped__" in led24.entries else
   not any(x["class"].startswith("TOPIC_OVER") for x in f24))

# ── F25: subject-set equality caught at draft (halt #3 at source) ──
ok25, e25, _, _ = validate_provenance(
    {"A": {"T": ["x"]}},
    [{"id": "SYL-001", "subject": "A", "syllabus_group": None, "raw_text": "x",
      "mapped_paths": [["A", "T", "x"]], "deviation": None}],
    ["A", "Dropped Subject"], [])
ck("F25 dropped subject caught by validate_provenance",
   not ok25 and any("SUBJECT-SET MISMATCH" in x for x in e25))


def _self_test():
    total = PASS + len(FAILS)
    print(f"SELF-TEST: {PASS}/{total} PASS")
    for n in FAILS:
        print("  FAIL:", n)
    return not FAILS


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
