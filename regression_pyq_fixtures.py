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



# ═════════════════════════════════════════════════════════════════════════════
# FX-ST — GAP-2026-09-01-SYLLABUS-TRANSITION, RELEASE A (Declaration &
# Detection; rebased to 2026.09.01.1 per rev 4.6). One fixture per §7 edge row
# in Release A scope: E01-E27, E53, E54, plus the E66 declaration-parse half.
# Proof obligations exercised at engine level: P1 (legacy silence), P2
# (inactive != invisible — exactly the three §3.6 traces), P3 (stop coverage:
# trigger + nearest-miss for every Release-A stop), P7 partial (§2.1e
# literal-scan, FX-ST-LS). Release B/C rows get their fixtures with their
# releases; the HS-ST9/HS-ST11/W-EF templates are asserted present (P3
# register completeness) even though their call sites land later.
# ═════════════════════════════════════════════════════════════════════════════
import datetime as _dt

import blueprint_core as bc
import corpus_io as cio

_TODAY = _dt.date(2026, 9, 2)


def _rt(sc=None, ef=None, extra=None):
    ov = {}
    if sc is not None:
        ov['Syllabus Changed'] = sc
    if ef is not None:
        ov['New Syllabus Effective From'] = ef
    if extra:
        ov.update(extra)
    return bc.resolve_transition(ov, _TODAY)


def _stops(fn):
    try:
        fn()
    except SystemExit as ex:
        return str(ex)
    return None


# ── FX-ST-01 / E01 + P1: both keys absent — inactive, SILENT, NO block ──
r01 = _rt()
ck("FX-ST-01 keys absent => inactive, trace False (T1 row 1)",
   r01['status'] == 'inactive' and r01['trace'] is False)
ck("FX-ST-01b P1: no exam_config block, no traces, no footer line",
   bc.build_syllabus_transition_block(r01) is None
   and bc.syllabus_declaration_traces(None) == []
   and bc.syllabus_footer_lines(None) == [])

# ── FX-ST-02 / E02: SC=No, EF absent — inactive, silent (block, no trace) ──
r02 = _rt(sc='No')
b02 = bc.build_syllabus_transition_block(r02)
ck("FX-ST-02 SC=No => inactive; block written; zero §3.6 traces (T1 row 2)",
   r02['status'] == 'inactive' and r02['trace'] is True
   and b02 is not None
   and bc.syllabus_declaration_traces(b02) == []
   and bc.syllabus_footer_lines(b02) == [])

# ── FX-ST-03 / E03: SC=Yes, EF string — ACTIVE ──
r03 = _rt(sc='Yes', ef='2026-12')
ck("FX-ST-03 declaration activates (T1 row 3)",
   r03['status'] == 'active' and r03['effective_from'] == '2026-12')

# ── FX-ST-04 / E04: case/whitespace normalization (T1 row 8) ──
ck("FX-ST-04 SC case/space never matters",
   all(_rt(sc=v, ef='2026-12')['status'] == 'active'
       for v in ('yes', 'YES', ' Yes ', 'yEs')))

# ── FX-ST-05 / E05 + E12: SC=Y/TRUE/blank/Maybe/Excel-True — trace row 5 ──
for v in ('Y', 'TRUE', 'Maybe', '', True):
    r05 = _rt(sc=v)
    b05 = bc.build_syllabus_transition_block(r05)
    ck(f"FX-ST-05 SC={v!r} => inactive + row-5 trace",
       r05['status'] == 'inactive'
       and r05['reason'].startswith("SC='")
       and len(bc.syllabus_declaration_traces(b05)) == 1)

# ── FX-ST-06 / E06: SC=No/blank + EF valid — trace row 4 ──
r06 = _rt(sc='No', ef='2026-12')
ck("FX-ST-06 EF present but SC is not Yes (T1 row 4)",
   r06['status'] == 'inactive'
   and r06['reason'] == "EF present but SC is not Yes")
r06b = _rt(sc='', ef='2026-12')
ck("FX-ST-06b blank SC + valid EF also row 4",
   r06b['reason'] == "EF present but SC is not Yes")

# ── FX-ST-07 / E07: SC absent, EF valid — trace row 7 ──
r07 = _rt(ef='2026-12')
ck("FX-ST-07 EF present but 'Syllabus Changed' absent (T1 row 7)",
   r07['status'] == 'inactive'
   and r07['reason'] == "EF present but 'Syllabus Changed' absent")

# ── P2: rows 4/5/7 produce EXACTLY the three traces and nothing else ──
_p2 = [bc.syllabus_declaration_traces(bc.build_syllabus_transition_block(x))
       for x in (r06, _rt(sc='Maybe'), r07)]
ck("FX-ST-P2 each traced state emits exactly one console line",
   all(len(t) == 1 for t in _p2))
ck("FX-ST-P2b footer line matches §3.6(c) template",
   bc.syllabus_footer_lines(bc.build_syllabus_transition_block(r07))
   == ["Syllabus declaration present but inactive: "
       "EF present but 'Syllabus Changed' absent"])

# ── FX-ST-08 / E08 + nearest-miss (P3): SC=Yes, EF absent/blank => HS-ST1 ──
m08 = _stops(lambda: _rt(sc='Yes'))
ck("FX-ST-08 HS-ST1 fires on missing EF (R2)",
   m08 is not None and m08.startswith("HARD STOP: 'Syllabus Changed' is Yes")
   and 'missing' in m08)
ck("FX-ST-08b nearest miss: SC=No + EF absent does NOT stop",
   _stops(lambda: _rt(sc='No')) is None)
m08c = _stops(lambda: _rt(sc='Yes', ef='   '))
ck("FX-ST-08c blank EF descriptor says blank", m08c and 'blank' in m08c)

# ── FX-ST-09 / E09: unparseable EF forms => HS-ST1 ──
for v in ('Dec 2026', '2026-13', '12-2026'):
    m09 = _stops(lambda v=v: _rt(sc='Yes', ef=v))
    ck(f"FX-ST-09 EF={v!r} => HS-ST1 (unparseable)",
       m09 is not None and 'unparseable' in m09)

# ── FX-ST-10 / E10: Excel datetime coercion => ACTIVE ──
r10 = _rt(sc='Yes', ef=_dt.datetime(2026, 12, 1))
ck("FX-ST-10 Excel datetime coerces to YYYY-MM (R4)",
   r10['status'] == 'active' and r10['effective_from'] == '2026-12')

# ── FX-ST-11 / E11: datetime day != 1 — coerce to month + note ──
v11, n11 = bc.coerce_effective_from(_dt.date(2026, 12, 15), _TODAY)
ck("FX-ST-11 day component ignored with note",
   v11 == '2026-12' and any('day component' in x for x in n11))

# ── FX-ST-12 / E12: Excel boolean TRUE => 'true' != 'yes' => row-5 path ──
r12 = _rt(sc=True, ef='2026-12')
ck("FX-ST-12 boolean SC lands row 5, never active",
   r12['status'] == 'inactive' and r12['reason'].startswith("SC='True'"))

# ── FX-ST-13 / E13: EF year outside sanity range => unparseable => HS-ST1 ──
m13 = _stops(lambda: _rt(sc='Yes', ef='1980-06'))
m13b = _stops(lambda: _rt(sc='Yes', ef='2099-01'))
ck("FX-ST-13 out-of-sanity EF => HS-ST1 both directions",
   m13 is not None and m13b is not None)

# ── FX-ST-14 / E14: EF > today+3 => ACTIVE + sanity note ──
r14 = _rt(sc='Yes', ef=f'{_TODAY.year + 4}-01')
ck("FX-ST-14 far-future EF activates with note",
   r14['status'] == 'active'
   and any('more than 3 years ahead' in n for n in r14['notes']))

# ── FX-ST-15 / E15: duplicate Overview key rows — last wins + WARN ──
ck("FX-ST-15 duplicate key detected",
   bc.overview_duplicate_keys(['Syllabus Changed', 'Medium',
                               ' Syllabus Changed ']) == ['Syllabus Changed'])
ck("FX-ST-15b no false duplicate", bc.overview_duplicate_keys(
   ['Syllabus Changed', 'Medium']) == [])

# ── FX-ST-16 / E16: mistyped key listed as near-miss ──
nm = bc.near_miss_keys(['Syllabus changed?', 'Medium', 'Total Marks'])
ck("FX-ST-16 near-miss listing (casefold + collapse)",
   nm == [('Syllabus changed?', 'Syllabus Changed')])
ck("FX-ST-16b exact key is never a near-miss",
   bc.near_miss_keys(['Syllabus Changed']) == [])

# ── census + T2 (E17-E23) ──
_cf = cio.syllabus_file_census
ck("FX-ST-CEN census matches token+ext, casefold",
   _cf(['EX_Syllabus_2026-12.pdf', 'ex_SYLLABUS_old.PNG', 'Syllabus.exe',
        'notes.docx']) == ['EX_Syllabus_2026-12.pdf', 'ex_SYLLABUS_old.PNG'])
ck("FX-ST-CEN2 samplepaper census (R14)",
   cio.sample_paper_census(['EX_SamplePaper_2026-12.pdf', 'EX_other.pdf'])
   == ['EX_SamplePaper_2026-12.pdf'])


def _cand(name, sha):
    return {'name': name, 'sha256': sha}


# E17: inactive + >=2 files (incl. translation — R18) => HS-ST2
r17 = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2019-06.pdf', 'a'), _cand('EX_Syllabus_HI.pdf', 'b')],
    'EX', 'inactive')
ck("FX-ST-17 HS-ST2 on inactive two-file census (R3/R18)",
   r17['outcome'] == 'stop' and r17['code'] == 'HS-ST2'
   and 'cannot choose which file is the syllabus' in r17['message'])

# E18: inactive + 1 file, arbitrary name => allowed (estate norm)
ck("FX-ST-18 single arbitrary-named file allowed while inactive",
   bc.resolve_syllabus_sources([_cand('my syllabus copy.pdf', 'a')],
                               'EX', 'inactive')['outcome'] == 'as_today')

# E19: active + 0/1 file => HS-ST3
r19 = bc.resolve_syllabus_sources([_cand('EX_Syllabus_2026-12.pdf', 'a')],
                                  'EX', 'active', '2026-12')
ck("FX-ST-19 HS-ST3 when active with < 2 files",
   r19['outcome'] == 'stop' and r19['code'] == 'HS-ST3')

# E20: active + one not dated-format => HS-ST4
r20st = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'a'), _cand('old syllabus.pdf', 'b')],
    'EX', 'active', '2026-12')
ck("FX-ST-20 HS-ST4 names the non-conforming file",
   r20st['outcome'] == 'stop' and r20st['code'] == 'HS-ST4'
   and 'old syllabus.pdf' in r20st['message'])

# E21: active + dated files, 0 matching EF => HS-ST5; >=2 files at ONE
# date => HS-ST12 (P-1: the collision stop owns all same-date duplicates,
# fired BEFORE EF matching — GAP-2026-09-05)
r21a = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2019-06.pdf', 'a'), _cand('EX_Syllabus_2020-06.pdf',
                                                  'b')],
    'EX', 'active', '2026-12')
r21b = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'a'),
     _cand('EX_Syllabus_2026-12.docx', 'b')],
    'EX', 'active', '2026-12')
ck("FX-ST-21 HS-ST5 on zero EF matches; HS-ST12 on a duplicated date",
   r21a['outcome'] == 'stop' and r21a['code'] == 'HS-ST5'
   and r21b['outcome'] == 'stop' and r21b['code'] == 'HS-ST12')

# E22: current sha == a superseded sha => HS-ST6
r22 = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'h1'),
     _cand('EX_Syllabus_2019-06.pdf', 'h1')],
    'EX', 'active', '2026-12')
ck("FX-ST-22 HS-ST6 on byte-identical documents",
   r22['outcome'] == 'stop' and r22['code'] == 'HS-ST6')

# E23: three dated files — legal; one == EF is CURRENT, rest date order
r23 = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'h1'),
     _cand('EX_Syllabus_2019-06.pdf', 'h2'),
     _cand('EX_Syllabus_2013-06.pdf', 'h3')],
    'EX', 'active', '2026-12')
ck("FX-ST-23 second historical change resolves (A2 degenerate-ready)",
   r23['outcome'] == 'resolved'
   and r23['current']['name'] == 'EX_Syllabus_2026-12.pdf'
   and [s['name'] for s in r23['superseded']]
   == ['EX_Syllabus_2013-06.pdf', 'EX_Syllabus_2019-06.pdf'])
ck("FX-ST-23b nearest miss: clean two-file resolution proceeds (T2 row 10)",
   bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_2026-12.pdf', 'h1'),
        _cand('EX_Syllabus_2019-06.pdf', 'h2')],
       'EX', 'active', '2026-12')['outcome'] == 'resolved')

# ── FX-ST-CASE (real-exam verification, GATE_BIOTECHNOLOGY): naming match
# is case-insensitive end to end — census is casefold (§3.4), so a
# census-nominated file must never fail naming on letter case alone ──
ck("FX-ST-CASE1 exam-code case mismatch still resolves",
   bc.resolve_syllabus_sources(
       [_cand('EX_UPPER_Syllabus_2027-02.pdf', 'a'),
        _cand('EX_UPPER_Syllabus_2026-02.pdf', 'b')],
       'ex_upper', 'active', '2027-02')['outcome'] == 'resolved')
ck("FX-ST-CASE2 SYLLABUS-token case still resolves",
   bc.parse_syllabus_filename('EX_SYLLABUS_2027-02.PDF', 'EX') == '2027-02')
ck("FX-ST-CASE3 case variants at the same date are HS-ST12 (P-1)",
   bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_2027-02.pdf', 'a'),
        _cand('EX_SYLLABUS_2027-02.PDF', 'b')],
       'EX', 'active', '2027-02')['code'] == 'HS-ST12')
ck("FX-ST-CASE4 structural malformation still HS-ST4",
   bc.parse_syllabus_filename('EX_Sylabus_2027-02.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_2027-2.pdf', 'EX') is None)

# ── FX-ST-HY (GAP-2026-09-05-SYLLABUS-FILENAME-TOLERANCE): the project
# Files section strips '-' from uploaded names (verified 2026-09-05,
# byte-identical CSIR NET Life Science files under both forms), so the
# date stamp accepts YYYYMM and ALWAYS returns normalized YYYY-MM ──
ck("FX-ST-HY1 hyphenless date accepted and normalized (R-a)",
   bc.parse_syllabus_filename('EX_Syllabus_202612.pdf', 'EX') == '2026-12'
   and bc.parse_syllabus_filename('EX_Syllabus_2026-12.pdf', 'EX')
   == '2026-12')
ck("FX-ST-HY2 malformed stamps still refused (mutation-kill: a mutant "
   "accepting any 6 digits, or 5 digits, or '_' separators must die)",
   bc.parse_syllabus_filename('EX_Syllabus_202613.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_202600.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_20261.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_2026_12.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_2026-1.pdf', 'EX') is None)
# live fixture — the two REAL CSIR project-Files names and true sha256s
_hy_live = bc.resolve_syllabus_sources(
    [_cand('CSIR_NET_LIFESCIENCES_Syllabus_202612.pdf',
           'd4544abd87a6b6565b1a739ad7d342a2becdf8e2d65f8c08720c6672'
           'f963a862'),
     _cand('CSIR_NET_LIFESCIENCES_Syllabus_202606.pdf',
           '548dd26b9434473d57f44688135baf9bee26973ef4569acc08ec0f21'
           '766dccc4')],
    'CSIR_NET_LIFESCIENCES', 'active', '2026-12')
ck("FX-ST-HY3 real CSIR hyphen-stripped names resolve; CURRENT=2026-12",
   _hy_live['outcome'] == 'resolved'
   and _hy_live['current']['name']
   == 'CSIR_NET_LIFESCIENCES_Syllabus_202612.pdf'
   and [x['name'] for x in _hy_live['superseded']]
   == ['CSIR_NET_LIFESCIENCES_Syllabus_202606.pdf'])
ck("FX-ST-HY4 mixed-form date collision, different bytes => HS-ST12 (R-b)",
   bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_2026-12.pdf', 'a'),
        _cand('EX_Syllabus_202612.pdf', 'b')],
       'EX', 'active', '2026-12')['code'] == 'HS-ST12')
_hy5 = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'h1'),
     _cand('EX_Syllabus_202612.pdf', 'h1')],
    'EX', 'active', '2026-12')
ck("FX-ST-HY5 same-date byte-identical pair => HS-ST12 names the sha",
   _hy5['code'] == 'HS-ST12' and 'byte-identical' in _hy5['message']
   and 'h1' in _hy5['message'])
ck("FX-ST-HY6 collision fires even when the duplicated date != EF",
   bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_2026-12.pdf', 'a'),
        _cand('EX_Syllabus_2019-06.pdf', 'b'),
        _cand('EX_Syllabus_201906.pdf', 'c')],
       'EX', 'active', '2026-12')['code'] == 'HS-ST12')
ck("FX-ST-HY7 normalization is idempotent and case-insensitive together",
   bc.parse_syllabus_filename('ex_syllabus_202702.PDF', 'EX') == '2027-02')
_hy8 = bc.resolve_syllabus_sources(
    [{'name': 'EX_Syllabus_2026-12.pdf', 'sha256': None},
     {'name': 'EX_Syllabus_202612.pdf', 'sha256': None}],
    'EX', 'active', '2026-12')
ck("FX-ST-HY8 unknown hashes: HS-ST12 never claims 'differ' (truthfulness)",
   _hy8['code'] == 'HS-ST12' and 'unavailable' in _hy8['message']
   and 'contents differ' not in _hy8['message']
   and 'byte-identical' not in _hy8['message'])

# ── FX-ST-24 / E24: dial overrides — invalid => factory + trace, no stop ──
d24, t24 = bc.resolve_dials({'Transition Blend Pseudo-Count': 'abc',
                             'Transition Detector Floor': -1,
                             'Transition Materiality Percent': '200%'})
ck("FX-ST-24 invalid dials fall back to factory with one trace each",
   d24['D-1'] == bc.TRANSITION_DIALS['D-1']['factory']
   and d24['D-4'] == bc.TRANSITION_DIALS['D-4']['factory']
   and d24['D-2'] == bc.TRANSITION_DIALS['D-2']['factory']
   and len(t24) == 3)
d24b, t24b = bc.resolve_dials({'Transition Blend Pseudo-Count': '5',
                               'Transition Materiality Percent': '7'})
ck("FX-ST-24b valid overrides apply; absent dials stay factory; no trace",
   d24b['D-1'] == 5 and d24b['D-2'] == 7.0
   and d24b['D-6'] == bc.TRANSITION_DIALS['D-6']['factory'] and t24b == [])
_nan = float('nan')
d24d, t24d = bc.resolve_dials({'Transition Blend Pseudo-Count': _nan})
ck("FX-ST-24d blank (NaN) dial cell is ABSENT, not invalid — no trace",
   d24d['D-1'] == bc.TRANSITION_DIALS['D-1']['factory'] and t24d == [])
z66c, zt66c = bc.parse_zero_history_approved(
    {'Zero History Approved': _nan}, ['New Unit'])
ck("FX-ST-66c blank (NaN) Zero History Approved cell is absent — no trace",
   z66c == [] and zt66c == [])
ck("FX-ST-24c seven dials, factory values engine-pinned (R23)",
   sorted(bc.TRANSITION_DIALS) == ['D-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6',
                                   'D-7']
   and [bc.TRANSITION_DIALS[k]['factory'] for k in
        ('D-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7')]
   == [3, 5.0, 40.0, 8, 1, 3, 80.0])

# ── FX-ST-25 / E25: declaration drift => HS-ST10; E62 non-drift ──
_act = _rt(sc='Yes', ef='2026-12')
_src = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'h1'),
     _cand('EX_Syllabus_2019-06.pdf', 'h2')], 'EX', 'active', '2026-12')
_blk = bc.build_syllabus_transition_block(_act, _src, {'D-1': 3}, [], [])
_act2 = _rt(sc='Yes', ef='2027-06')  # R17 EF-postponement edit
_blk2 = bc.build_syllabus_transition_block(_act2, None, {'D-1': 3}, [], [])
d25 = bc.transition_drift(_blk, _blk2)
ck("FX-ST-25 drift detected on an EF edit (R17 path)",
   any(f == 'effective_from' for f, _, __ in d25)
   and bc.HS_ST10('a', 'b').startswith('HARD STOP: declaration drift'))
ck("FX-ST-25b no drift on identical declaration (E62 class: non-declaration "
   "writes can never register)",
   bc.transition_drift(_blk, dict(_blk)) == []
   and bc.transition_drift(None, None) == [])

# ── FX-ST-RE (R-e, GAP-2026-09-05): drift identity is the sha256; names
# are display-only. Mutation-kill: a mutant restoring name comparison
# must die on RE1/RE3; a mutant dropping the sha compare dies on RE2/RE4 ──
_re_stored = {'status': 'active', 'effective_from': '2026-12',
              'current_file': 'CSIR_NET_LIFESCIENCES_Syllabus_2026-12.pdf',
              'current_sha256': 'd45', 'superseded': [
                  {'file': 'CSIR_NET_LIFESCIENCES_Syllabus_2026-06.pdf',
                   'sha256': '548'}]}
_re_fresh = {'status': 'active', 'effective_from': '2026-12',
             'current_file': 'CSIR_NET_LIFESCIENCES_Syllabus_202612.pdf',
             'current_sha256': 'd45', 'superseded': [
                 {'file': 'CSIR_NET_LIFESCIENCES_Syllabus_202606.pdf',
                  'sha256': '548'}]}
ck("FX-ST-RE1 name-form flip of byte-identical files is NOT drift (R-e)",
   bc.transition_drift(_re_stored, _re_fresh) == [])
_re_b2 = dict(_re_fresh); _re_b2['current_sha256'] = 'CHANGED'
ck("FX-ST-RE2 changed CURRENT bytes still drift on current_sha256",
   any(fld == 'current_sha256'
       for fld, _, __ in bc.transition_drift(_re_stored, _re_b2)))
_re_b3 = dict(_re_fresh)
_re_b3['superseded'] = [{'file': 'renamed anyhow.pdf', 'sha256': '548'}]
ck("FX-ST-RE3 superseded rename with same sha set is NOT drift",
   bc.transition_drift(_re_stored, _re_b3) == [])
_re_b4 = dict(_re_fresh)
_re_b4['superseded'] = [{'file': 'x.pdf', 'sha256': 'OTHER'}]
ck("FX-ST-RE4 superseded sha-set change drifts as superseded_sha256_set",
   any(fld == 'superseded_sha256_set'
       for fld, _, __ in bc.transition_drift(_re_stored, _re_b4)))

# ── FX-ST-26 / E26: staleness — HS-ST7 + legacy exemption ──
ck("FX-ST-26 hash mismatch => HS-ST7; legacy artefact exempt; match clean",
   bc.check_syllabus_staleness('taxonomy_draft', 'h_old', 'h_new', '6')
   is not None
   and bc.check_syllabus_staleness('taxonomy_draft', None, 'h_new', '6')
   is None
   and bc.check_syllabus_staleness('taxonomy_draft', 'h', 'h', '6') is None)

# ── FX-ST-27 / E27 + FX-ST-53 / E53 + FX-ST-66 / E66: symptom detector ──
_tr = bc.build_syllabus_transition_block(_rt(sc='Maybe'))
_di = {'D-4': 8}
m27 = bc.symptom_detector(_tr, ['New Unit'], 9, _di,
                          present_overview_keys=['Syllabus changed?'])
ck("FX-ST-27 HS-ST8 fires on keys-present-inactive + zero-history subject",
   m27 is not None and "Subject 'New Unit'" in m27
   and 'ignored' in m27)
ck("FX-ST-27b below detector floor: silent",
   bc.symptom_detector(_tr, ['New Unit'], 7, _di) is None)
ck("FX-ST-53 keys-absent exam: detector fully SILENT (R25; proves P1)",
   bc.symptom_detector(None, ['New Unit'], 30, _di) is None
   and bc.symptom_detector(b02, ['New Unit'], 30, _di) is None)
_tr66 = dict(_tr)
_tr66['zero_history_approved'] = ['New Unit']
ck("FX-ST-66 Zero History Approved suppresses HS-ST8 for that subject",
   bc.symptom_detector(_tr66, ['New Unit'], 9, _di) is None)
z66, zt66 = bc.parse_zero_history_approved(
    {'Zero History Approved': ' new unit , Ghost '}, ['New Unit', 'Old'])
ck("FX-ST-66b A1 parse: casefold match; unmatched name => trace not stop",
   z66 == ['New Unit'] and len(zt66) == 1 and 'Ghost' in zt66[0])

# ── FX-ST-54 / E54: legacy stray-file discovery is HS-ST2, reactive (R26) ──
ck("FX-ST-54 keys-absent + 2 stray files stops reactively with the "
   "self-explanatory message",
   'Remove the extra file(s) or complete the declaration'
   in bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_a.pdf', 'x'), _cand('EX_Syllabus_b.pdf', 'y')],
       'EX', 'inactive')['message'])

# ── P3 register completeness: every §3.11 template exists and renders ──
ck("FX-ST-P3 register HS-ST1..11 + W-EF1/2 all render non-empty",
   all(callable(getattr(bc, n)) for n in
       ['HS_ST%d' % i for i in range(1, 12)] + ['W_EF1', 'W_EF2'])
   and 'ruling R20' in bc.HS_ST9('p', 3, 2, 0)
   and 'subject-partitioned' in bc.HS_ST11('S')
   and 'fully measured mode' in bc.W_EF1('2020-01', '2021-06')
   and 'Verify Effective From' in bc.W_EF2('S', 9, 8))


# ═══ FX-XW — Release B: crosswalk, era, labeling, counts (GAP §4) ═══════════
import syllabus_provenance as _sp

_XO = {'Unit One Old Name': {'T': ['alpha beta gamma delta', 'epsilon zeta eta',
                                   'theta iota kappa']},
       'Split Parent': {'M': ['natural selection and genetic drift',
                              'mechanisms of speciation events',
                              'adaptive radiation and convergence'],
                        'B': ['circadian rhythms biological clocks',
                              'mating systems parental investment']},
       'Orphan Unit': {'X': ['completely unrelated content one',
                             'completely unrelated content two']}}
_XN = {'Unit One New Name': {'T': ['alpha beta gamma delta', 'epsilon zeta eta',
                                   'theta iota kappa']},
       'Evolution Home': {'E': ['natural selection genetic drift and gene flow',
                                'mechanisms of speciation',
                                'adaptive radiation and convergent evolution']},
       'Behaviour Home': {'H': ['sexual selection and mating systems',
                                'parental care'],
                          'P': ['photoperiodism and biological clock']},
       'Brand New Subject': {'N': ['brand new material one',
                                   'brand new material two']}}
_xw = _sp.crosswalk_build(_XO, _XN, exam_code='EXAM_A', old_sha256='O',
                          new_sha256='N',
                          era_window={'from': '2026-12', 'to': None},
                          dials={'D-2': 5.0, 'D-7': 80.0})
_ss = _xw['subject_states']
ck("FX-XW-29 renamed subject matched by CONTENT, never name (E29)",
   _xw['correspondents']['Unit One Old Name'][0][0] == 'Unit One New Name'
   and _ss['Unit One New Name']['state'] != 'NEW')
ck("FX-XW-30 split parent keeps a correspondent (top-half mean, not orphaned)",
   bool(_xw['correspondents']['Split Parent']))
_XSM = _sp.subject_correspondents(
    {'Tiny': {'T': ['plant systematics', 'photosynthesis and metabolism']}},
    {'Home': {'T': ['plant systematics', 'photosynthesis and metabolism']},
     'Other': {'T': ['general principles of metabolism',
                     'structure of biomolecules']}})
ck("FX-XW-30b k-floor: one fluke atom match never mints a correspondent "
   "for a small subject (sectioned-exam hardening)",
   _XSM['Tiny'] == [('Home', 1.0)])
_X1 = _sp.subject_correspondents(
    {'Solo': {'T': ['photosynthesis light reactions']}},
    {'Home': {'T': ['photosynthesis and light reaction']}})
ck("FX-XW-30c n=1 keeps k=1: a single-atom subject's score is its best "
   "match, never halved (kills the min-dropped mutant)",
   _X1['Solo'] and _X1['Solo'][0][0] == 'Home'
   and _X1['Solo'][0][1] > 0.9)
_X3 = _sp.subject_correspondents(
    {'Trio': {'T': ['photosynthesis light reactions',
                    'quantum chromodynamics lattice',
                    'byzantine consensus protocols']}},
    {'Home': {'T': ['photosynthesis and light reaction']}})
ck("FX-XW-30d n=3 keeps k=2 exactly: the top-half window neither shrinks "
   "nor grows (kills the floor-raised mutant)",
   _X3['Trio'] and _X3['Trio'][0][0] == 'Home'
   and abs(_X3['Trio'][0][1] - 0.5872) < 0.01)
ck("FX-XW-70 brand-new subject rolls up NEW at D-7 (B1)",
   _ss['Brand New Subject']['state'] == 'NEW'
   and _ss['Brand New Subject']['frac_new'] == 1.0)
ck("FX-XW-86 orphan subject: scope empty, every atom DELETED (E86)",
   _xw['scope']['Orphan Unit'] == []
   and all(n['state'] == 'DELETED' for n in _xw['nodes']
           if n['old_id'][0] == 'Orphan Unit'))
ck("FX-XW-28 materiality: subject flip forces material (R28)",
   _xw['materiality']['material']
   and _xw['materiality']['subject_new_or_deleted'])
ck("FX-XW-24 draft never approved by construction", _xw['approved'] is False)
_CLK = ('Split Parent', 'B', 'circadian rhythms biological clocks')
_ap = _sp.approve_crosswalk(_xw, 'op', '2026-09-02',
                            state_overrides={_CLK: 'DELETED'}, d7_pct=80.0)
_nbc = next(n for n in _ap['nodes'] if n['old_id'] == _CLK)
ck("FX-XW-88 F-1 retained-term subtraction (plural vs singular) empties",
   'biological clocks' not in _nbc['lexicon'])
ck("FX-XW-91 G-1: lexicons finalized in the SAME approve write",
   _ap['approved'] is True
   and all('lexicon' not in n for n in _ap['nodes']
           if n['state'] != 'DELETED'))
ck("FX-XW-59 R30 records newly-DELETED nodes (E59)",
   tuple(_CLK) in set(map(tuple, _sp.reevaluate_suppressions(
       [], _xw, _ap)['newly_deleted'])))
_ORF = ('Orphan Unit', 'X', 'completely unrelated content one')
_ap2 = _sp.approve_crosswalk(_xw, 'op', '2026-09-02',
                             state_overrides={_ORF: 'MOVED'}, d7_pct=80.0)
ck("FX-XW-58 R30 reinstates when approval un-deletes (E58)",
   len(_sp.reevaluate_suppressions(
       [{'proposal': 'p1', 'matched_deleted_node': _ORF, 'score': 0.9}],
       _xw, _ap2)['reinstate']) == 1)
ck("FX-XW-75 B1 subject override honored and flagged (E75)",
   _sp.approve_crosswalk(_xw, 'op', '2026-09-02',
       subject_state_overrides={'Split Parent': 'SPLIT'},
       d7_pct=80.0)['subject_states']['Split Parent'].get('operator_override')
   is True)

_GO = {'Section Four': {'T': ['material and energy balances',
                              'laws of thermodynamics phase equilibria',
                              'newtonian fluids laminar and turbulent flow']},
       'Section Five': {'T': ['rate law zero and first order kinetics',
                              'thiele modulus effectiveness factor',
                              'media formulation and sterilization']}}
_GN = {'Section Four': {'T': ['rate law zero and first order kinetics',
                              'thiele modulus effectiveness factor',
                              'media formulation and optimization']}}
_gc = _sp.subject_correspondents(_GO, _GN)
ck("FX-XW-67 name-sharing sections do NOT auto-map; content decides (E67)",
   bool(_gc['Section Five']) and _gc['Section Five'][0][0] == 'Section Four'
   and not _gc['Section Four'])
_gx = _sp.crosswalk_build(_GO, _GN, exam_code='EXAM_B', old_sha256='O',
                          new_sha256='N',
                          era_window={'from': '2027-02', 'to': None},
                          dials={'D-2': 5.0, 'D-7': 80.0})
ck("FX-XW-67b old S5 content MOVED/RETAINED into the same-name new home",
   all(n['state'] in ('RETAINED', 'MOVED', 'MERGED') for n in _gx['nodes']
       if n['old_id'][0] == 'Section Five'))
ck("FX-XW-67c merged current side not NEW (Regime-2 shape)",
   _gx['subject_states']['Section Four']['state'] != 'NEW')

_w = bc.era_windows(['2019-06', '2026-06', '2026-12'], '2026-12')
ck("FX-XW-63 era windows: A2 next-boundary form, CURRENT opens at EF",
   _w[-1]['from'] == '2026-12' and _w[-1]['to'] is None
   and _w[0]['to'] == '2026-06'
   and bc.era_version_for('2025-07', _w) == '2019-06'
   and bc.era_version_for('2010-01', _w) == '2019-06')
ck("FX-XW-37 boundary paper IN the EF month is new-era (E37)",
   bc.assign_syllabus_era('2026-12', '2026-12') == 'new'
   and bc.assign_syllabus_era('2026-11', '2026-12') == 'old')
ck("FX-XW-38 W-EF1 fires when EF predates every paper (E38)",
   bc.w_ef1_check('2010-01', '2015-06') is not None
   and bc.w_ef1_check('2026-12', '2015-06') is None)
ck("FX-XW-57 era-suspect at D-3 boundary uses >= (E57)",
   bc.era_suspect_check('P1', 40.0, {'D-3': 40.0}) is not None
   and bc.era_suspect_check('P1', 39.9, {'D-3': 40.0}) is None)
_lbl = bc.map_question_label(('S', 'T', 'St'), 'DELETED', [], 'Succ')
ck("FX-XW-31 OOS: sentinel internal, label = old triple VERBATIM (L-1/R24)",
   _lbl['status'] == bc.OUT_OF_SYLLABUS and _lbl['label'] == ('S', 'T', 'St')
   and _lbl['successor_subject'] == 'Succ')
_lb2 = bc.map_question_label(('S', 'T', 'St'), 'MOVED',
                             [('NS', 'NT', 'NSt')], 'NS')
ck("FX-XW-32 mapped question labeled at its NEW home, legacy kept (L-5/E32)",
   _lb2['status'] == 'normal' and _lb2['label'] == ('NS', 'NT', 'NSt')
   and _lb2['legacy_label'] == ('S', 'T', 'St'))
ck("FX-XW-39 n_new counts SITTINGS at/after EF",
   bc.n_new_sittings(['2026-06', '2026-12', '2026-12', '2027-06'],
                     '2026-12') == 3)
ck("FX-XW-40 HS-ST9 reconciliation: mismatch stops, balance passes",
   bc.reconcile_counts('P', 10, 9, 0) is not None
   and bc.reconcile_counts('P', 10, 9, 1) is None)

_xsrc = open('syllabus_provenance.py').read()
_xcl = _xsrc.split('# CLUSTER XW')[1].split('# END CLUSTER XW')[0]
import re as _re_xw
ck("FX-XW-LS no exam identifier in the XW cluster (2.1e)",
   not _re_xw.search(r'CSIR|GATE_|LIFESCIENCE|BIOTECH', _xcl))
ck("FX-XW-LS2 similarity floors declared once, in range",
   0 < _sp.XW_SUBJECT_SIMILARITY < _sp.XW_MAP_SIMILARITY < 1)


# ═══ FX-AL — Release C: transition allocation & gates (GAP §5) ══════════════
ck("FX-AL-01 §5.1 three-way classification",
   bc.classify_bucket(0.7, False) == 'PYQ'
   and bc.classify_bucket(0, True) == bc.NEW_SYLLABUS
   and bc.classify_bucket(0, False) == bc.ZERO_PYQ_BUCKET)
ck("FX-AL-02 regime per SECTION, independent (R33/B2)",
   bc.section_regime(['NEW', 'RETAINED']) == 1
   and bc.section_regime(['RETAINED', 'MERGED', 'SPLIT']) == 2
   and bc.section_regime(['DELETED']) == 1)
_xf2 = {'nodes': ([{'old_id': ('S4', 'T', 'd%d' % i), 'state': 'DELETED',
                    'new_ids': []} for i in range(8)] +
                  [{'old_id': ('S4', 'T', 's%d' % i), 'state': 'MOVED',
                    'new_ids': [('S2', 'T', 's%d' % i)]} for i in range(2)])}
ck("FX-AL-03 F-2: DELETED atoms stay in the denominator — share evaporates",
   abs(bc.frac_atoms_map(_xf2, 'S4')['S2'] - 0.2) < 1e-9)
ck("FX-AL-04 blend convergence 0/25/40/50% at n_new=0..3, m=3 (Pass-3)",
   all(abs(bc.blend_weight(n, 1.0, 0.0, 3) - e) < 1e-9
       for n, e in [(0, 0.0), (1, 0.25), (2, 0.40), (3, 0.50)]))
ck("FX-AL-05 n_new=0 => weight IS the prior",
   abs(bc.blend_weight(0, 0.9, 0.37, 3) - 0.37) < 1e-9)
_s5014 = bc.series_quota_split(50, 14)
_runs, _mx = 1, 1
for _a, _b in zip(_s5014, _s5014[1:]):
    _runs = _runs + 1 if _a == _b else 1
    _mx = max(_mx, _runs)
ck("FX-AL-06 series split 50/14 INTERLEAVES 3s and 4s (GAP worked example; "
   "no front-loading)",
   sum(_s5014) == 50 and sorted(_s5014, reverse=True) == [4] * 8 + [3] * 6
   and _mx <= 2)
ck("FX-AL-06b footer: unwired n_new=None prints nothing, never crashes",
   bc.transition_footer_lines({'status': 'active'}, None) == [])
_u7 = bc.hier_allocate(12.0, [('K', True, 0), ('L', True, 0)] +
                       [(chr(65 + i), False, 1.0) for i in range(10)])
ck("FX-AL-07 §5.3 mixed parent: driving-exam Unit-7 worked example (1/12)",
   abs(_u7['K'] - 1.0) < 1e-9 and abs(_u7['L'] - 1.0) < 1e-9
   and abs(sum(_u7.values()) - 12.0) < 1e-9)
ck("FX-AL-08 §5.3 degenerations: all-NEW = R6 equal; all-history = measured",
   bc.hier_allocate(6.0, [('a', True, 0), ('b', True, 0)]) ==
   {'a': 3.0, 'b': 3.0}
   and abs(bc.hier_allocate(9.0, [('x', False, 2.0), ('y', False, 1.0)]
                            )['x'] - 6.0) < 1e-9)
_pk, _cov, _tot, _nx = bc.even_spread_schedule(
    ['n%02d' % i for i in range(50)], 44, 0)
ck("FX-AL-09 §5.4 even spread in DOCUMENT order; infeasible reports, "
   "cursor resumes",
   _cov == 44 and _tot == 50 and _nx == 44 and _pk[0] == 'n00'
   and bc.bv_coverage_report(_cov, _tot) ==
   '44 of 50 covered (maximum feasible)'
   and bc.bv_coverage_report(50, 50) is None)
_p2, _c2, _t2, _n2 = bc.even_spread_schedule(
    ['n%02d' % i for i in range(50)], 44, 44)
ck("FX-AL-10 next series resumes at the cursor => full coverage across two",
   _p2[0] == 'n44' and len(set(_pk) | set(_p2)) == 50)
ck("FX-AL-11 A3 cursor staleness: hash mismatch resets with a note, "
   "never stops",
   bc.cursor_read({'position': 7, 'syllabus_sha256': 'A'}, 'B') ==
   (0, bc.cursor_read({'position': 7, 'syllabus_sha256': 'A'}, 'B')[1])
   and bc.cursor_read({'position': 7, 'syllabus_sha256': 'A'}, 'A') ==
   (7, None))
ck("FX-AL-12 BV-UNIT +-1 largest-remainder step per section",
   bc.bv_unit_check({'A': 5, 'B': 5}, {'A': 0.5, 'B': 0.5}, 10) == []
   and bc.bv_unit_check({'A': 8, 'B': 2}, {'A': 0.5, 'B': 0.5}, 10) != [])
ck("FX-AL-13 BV-TOPIC closes the single-subject-section hole (D2)",
   bc.bv_topic_check({'t1': 4, 't2': 4}, {'t1': 4.0, 't2': 4.0}) == []
   and bc.bv_topic_check({'t1': 8, 't2': 0}, {'t1': 4.0, 't2': 4.0}) != [])
ck("FX-AL-14 L4/L5 lexicon screen: own-scope hit, foreign-scope clean",
   _sp.lexicon_screen('on the theory of island biogeography today',
                      [['theory of island biogeography']]) ==
   ['theory of island biogeography']
   and _sp.lexicon_screen('photoperiodism in plants',
                          [['theory of island biogeography']]) == [])
ck("FX-AL-15 §5.9 footer: n_new always printed; converged label at D-6",
   'n_new=1' in bc.transition_footer_lines(
       {'status': 'active'}, 1, coverage_text='44 of 50')[0]
   and 'effectively measured (n_new=3)' in
   bc.transition_footer_lines({'status': 'active'}, 3)[0]
   and bc.transition_footer_lines({'status': 'inactive'}, 5) == [])
ck("FX-AL-16 projected shares renormalize; skipped subjects harmless",
   abs(sum(bc.projected_shares({'S4': 0.1, 'S2': 0.9}, _xf2,
                               ['S2']).values()) - 1.0) < 1e-9)

# ── FX-ST-LS — §2.1e LITERAL-SCAN over the GAP-introduced engine code ──
import ast
import re as _re


def _cluster_source(path, start_marker, end_marker):
    txt = open(path, encoding='utf-8').read()
    i = txt.index(start_marker)
    j = txt.index(end_marker, i)
    return txt[i:j]


_ls_src = _cluster_source(
    'blueprint_core.py',
    '# CLUSTER SYLLABUS ERA — SYLLABUS TRANSITION',
    '# END CLUSTER SYLLABUS ERA')
_ls_src2 = _cluster_source(
    'corpus_io.py',
    '# CLUSTER SYL — SYLLABUS & SAMPLE-PAPER FILE CENSUS',
    '# END CLUSTER SYL')
# Whitelist: the seven §3.9 dial factory defaults, plus structural tokens —
# regex/format constants, the §3.2 sanity years of the GAP's OWN code,
# indices/radixes and the 1 MiB read-chunk shift. NOTHING allocation-shaped
# (no subject counts, no quotas) may appear (R5/§2.1).
_LS_WHITELIST = {3, 5.0, 40.0, 8, 1, 80.0,   # dial factory defaults (§3.9)
                 0, 1, 2, 4, 5, 100, 1990, 12, 20}
_ls_found = set()
for blob in (_ls_src, _ls_src2):
    code = '\n'.join(l for l in blob.split('\n')
                     if not l.lstrip().startswith('#'))
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Constant) and isinstance(node.value,
                                                         (int, float)) \
                and not isinstance(node.value, bool):
            _ls_found.add(node.value)
ck("FX-ST-LS §2.1e: no numeric literal outside the dial-default + "
   "structural whitelist in GAP-introduced engine code",
   _ls_found <= _LS_WHITELIST)
ck("FX-ST-LS2 §2.1e: no exam identifier in the cluster logic",
   not _re.search(r'CSIR|GATE_|GATE B|LIFE_SCIENCE|BIOTECH',
                  _ls_src + _ls_src2))


# ── FX-L2 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER: organic decision-load ruler (Cluster L2)
#    + the every-exam difficulty layer (Cluster DL). FIXTURE: the 95 organic past questions of a
#    real post-graduate chemistry exam (3 cycles, decision fields only — named_concepts, ask_type,
#    stereo_decl, distractor_mechanisms, closeness grades, section, stored band; NO stems, structures
#    or keys), zlib+base64, sha256 pinned. Plus that exam's 40-item organic subject test as authored
#    by release 2026.11.06 (concepts / isomeric-distractor count / stereo declaration per item).
import base64 as _b64, zlib as _zl, hashlib as _hl, json as _js
_L2_FX_SHA = 'a193a247bad2a455b6b053ed96bf31f5f52d0526aa8b410264225b9ea3210d89'
_L2_FX_B64 = (
    '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'
    'CWA='
)
_l2_raw = _zl.decompress(_b64.b64decode(''.join(_L2_FX_B64)))
_L2P = _js.loads(_l2_raw.decode('utf-8'))
_L2T01 = {
    1: (["Hajos\u2013Parrish (L-proline organocatalysis)", "Wieland\u2013Miescher ketone", "selective ketalization"], 1, "none"),
    2: (["quasi-Favorskii (semibenzilic) rearrangement"], 0, "none"),
    3: (["Johnson\u2013Claisen", "1,3-chirality transfer"], 2, "relative"),
    4: (["chemical shift", "n + 1 rule"], 0, "none"),
    5: (["epoxidation", "Wharton"], 0, "none"),
    6: (["conformational analysis", "A-value"], 0, "relative"),
    7: (["E2 anti-periplanar", "conformationally locked"], 1, "relative"),
    8: (["Shapiro"], 0, "none"),
    9: (["Birch", "enol ether hydrolysis"], 1, "none"),
    10: (["chemical shift", "n + 1 rule"], 0, "none"),
    11: (["Sharpless\u2013Caron regioselective epoxide opening"], 0, "relative"),
    12: (["azulene", "nucleophilic addition"], 1, "none"),
    13: (["SN1", "ether cleavage"], 0, "none"),
    14: (["terpinyl cation", "biogenesis"], 0, "none"),
    15: (["Woodward cis-hydroxylation", "acetoxonium"], 0, "none"),
    16: (["H\u00fcckel 4n+2"], 0, "none"),
    17: (["Hofmann elimination", "anti-periplanar"], 0, "relative"),
    18: (["osazone"], 0, "none"),
    19: (["iodolactonization", "E2 anti-periplanar"], 1, "none"),
    20: (["Luche", "chemoselective reduction"], 0, "none"),
    21: (["SN1", "Bredt"], 0, "none"),
    22: (["Cannizzaro"], 0, "none"),
    23: (["Bucherer", "Sandmeyer"], 0, "none"),
    24: (["anti addition", "anti-periplanar"], 0, "relative"),
    25: (["E2 anti-periplanar", "conformationally locked"], 1, "relative"),
    26: (["Beckmann fragmentation"], 0, "none"),
    27: (["hydroboration"], 0, "none"),
    28: (["aromatic Claisen rearrangement"], 0, "none"),
    29: (["Wagner\u2013Meerwein", "ring expansion"], 1, "none"),
    30: (["von Baeyer nomenclature", "CIP rules"], 0, "absolute"),
    31: (["bromohydrin"], 0, "relative"),
    32: (["catalytic hydrogenation", "syn addition"], 0, "relative"),
    33: (["SN2", "Mitsunobu-type inversion"], 0, "absolute"),
    34: (["chemical shift"], 0, "none"),
    35: (["anti addition", "bromination"], 0, "relative"),
    36: (["Sharpless epoxidation"], 0, "absolute"),
    37: (["Mannich", "pyrrole"], 0, "none"),
    38: (["Oppenauer"], 1, "none"),
    39: (["dithiane formation"], 0, "none"),
    40: (["Grignard"], 0, "none"),
}
_L2T01_BANDS = {1: 'Hard', 2: 'Medium', 3: 'Hard', 4: 'Medium', 5: 'Medium', 6: 'Medium', 7: 'Hard', 8: 'Medium', 9: 'Medium', 10: 'Medium', 11: 'Hard', 12: 'Medium', 13: 'Medium', 14: 'Medium', 15: 'Medium', 16: 'Medium', 17: 'Medium', 18: 'Medium', 19: 'Medium', 20: 'Medium', 21: 'Medium', 22: 'Medium', 23: 'Medium', 24: 'Medium', 25: 'Hard', 26: 'Medium', 27: 'Medium', 28: 'Medium', 29: 'Medium', 30: 'Medium', 31: 'Medium', 32: 'Medium', 33: 'Medium', 34: 'Medium', 35: 'Medium', 36: 'Medium', 37: 'Medium', 38: 'Medium', 39: 'Medium', 40: 'Medium'}
_L2LABS = ['Easy', 'Medium', 'Hard']
_l2sids = sorted({r['subtopic_id'] for p in _L2P['papers'].values() for r in p['questions'].values()})
_L2M = bc.l2_model_for_scope(_L2P, _l2sids, _L2LABS, measured_pct={'Easy': 3, 'Medium': 70, 'Hard': 27})


def _l2t01(q):
    nc, cc, sd = _L2T01[q]
    return bc.l2_record({'named_concepts': nc, 'stereo_decl': sd,
                         'distractor_mechanisms': ['regioisomer'] * cc + ['alternative_pathway'] * (3 - cc)}, _L2M)


ck("FX-L2-01 fixture integrity: sha256 pinned, 95 organic records, 3 papers",
   _hl.sha256(_l2_raw).hexdigest() == _L2_FX_SHA and _L2M['n'] == 95 and len(_L2P['papers']) == 3)
ck("FX-L2-02 T11 vocabulary coverage 100 % on the fixture exam; ruler BINDING; nothing unmatched",
   _L2M['vocab_coverage'] == 1.0 and _L2M['binding'] is True and _L2M['unmatched'] == [])
ck("FX-L2-03 D3 symmetry law on real data: reagents (62 %) and scheme steps (73 %) OFF, distractor "
   "relations and stereo ON — fields switch by measured pool coverage, never by assumption",
   _L2M['fields_on'] == {'reagents': False, 'close': True, 'stereo': True, 'steps': False}
   and _L2M['field_coverage']['reagents'] < bc.L2_FIELD_MIN_COVERAGE <= _L2M['field_coverage']['close'])
_l2pyq = {(k, q): bc.l2_record(_L2P['papers'][k]['questions'][q], _L2M) for k, q in _L2M['pool_keys']}
_l2hard = [kq for kq, r in _l2pyq.items() if r['band'] == 'Hard']
ck("FX-L2-04 T2 relative calibration: cuts from the exam's own PYQs at the recorded shares; "
   "Hard share within the tie tolerance (+-5 points) of 27 %",
   _L2M['mode'] == 'relative' and _L2M['cuts_list'][1] == 35.0 and _L2M['cuts_list'][0] < 5.0
   and abs((100 - _L2M['achieved'][1]) - 27) <= 5)
ck("FX-L2-05 T2 invariant: no past question whose highest concept is a standard reaction (load <= 3) is Hard",
   all(r['load'] is not None and r['load'] >= 4 for kq, r in _l2pyq.items() if r['band'] == 'Hard'))
ck("FX-L2-06 T2: the advanced-method PYQs are Hard (Zimmerman-Traxler, Myers, Danheiser, Tsuji-Trost, "
   "Evans, phenonium, aza-Cope-Mannich, carbonyl-ene, Vedejs)",
   all(_l2pyq[kq]['band'] == 'Hard' for kq in [('18-Jul-2026', '71'), ('18-Dec-2025', '114'), ('18-Jul-2026', '73'),
                                                ('28-Jul-2025', '86'), ('18-Jul-2026', '96'), ('18-Jul-2026', '84'),
                                                ('18-Dec-2025', '105'), ('18-Dec-2025', '95'), ('18-Dec-2025', '115')]))
ck("FX-L2-07 T3 the 40 authored items reproduce their pinned bands (regression lock)",
   all(_l2t01(q)['band'] == b for q, b in _L2T01_BANDS.items()) and len(_L2T01_BANDS) == 40)
ck("FX-L2-08 T4 size traps are NOT Hard: Oppenauer of a steroid (Q38), Birch of a steroid (Q9), "
   "PhMgBr on a lactone (Q40), Cannizzaro (Q22), osazone (Q18)",
   all(_l2t01(q)['band'] != 'Hard' for q in (38, 9, 40, 22, 18)))
ck("FX-L2-09 T3 every authored item whose concepts are standard B.Sc. reactions (load <= 3) is not Hard",
   all(_l2t01(q)['band'] != 'Hard' for q in _L2T01 if (_l2t01(q)['load'] or 0) <= 3))
ck("FX-L2-10 T3 organocatalysis / Johnson-Claisen + chirality transfer items are Hard",
   _l2t01(1)['band'] == 'Hard' and _l2t01(3)['band'] == 'Hard')
# D5 — no exam-type shift: a second exam at the same degree level whose papers are shallower gets its
# OWN, lower cuts from the SAME vocabulary; the same item is Hard there and Medium here.
_l2lo_q = {}
_lo_concepts = [['Cannizzaro reaction'], ['aldol reaction'], ['SN2 reaction'], ['Grignard addition'],
                ['Friedel–Crafts acylation'], ['PCC'], ['hydroboration'], ['ozonolysis'], ['Wittig reaction'],
                ['Hückel 4n+2 rule'], ['chemical shift'], ['n + 1 rule'], ['Markovnikov rule'],
                ['Beckmann rearrangement'], ['Diels–Alder'], ['anti addition', 'bromination'],
                ['Baeyer–Villiger oxidation'], ['Birch reduction'], ['Hofmann elimination', 'Zaitsev rule'],
                ['CIP rules', 'meso compound']]
for _i, _c in enumerate(_lo_concepts, 1):
    _l2lo_q[str(_i)] = {'subtopic_id': 'oc.t.s', 'qtype': 'mcq', 'ask_type': 'identify_product', 'named_concepts': _c,
                        'stereo_decl': 'relative' if _i in (16, 20) else 'none',
                        'distractor_mechanisms': ['alternative_pathway'] * 3, 'section': 'P', 'band': 'Medium'}
_L2LO = {'papers': {'LO-2025': {'date': '2025-06-01', 'questions': _l2lo_q}}}
_L2MLO = bc.l2_model_for_scope(_L2LO, ['oc.t.s'], _L2LABS, measured_pct={'Easy': 20, 'Medium': 60, 'Hard': 20})
_l2item = {'named_concepts': ['Birch reduction', 'enol ether hydrolysis'], 'stereo_decl': 'none',
           'distractor_mechanisms': ['alternative_pathway'] * 3}
ck("FX-L2-11 D5: same vocabulary, exam-own cuts — the shallower exam's cuts are lower and the same item "
   "is Hard there, Medium in the deeper exam (difficulty comes from each exam's past papers only)",
   _L2MLO['active'] and _L2MLO['cuts_list'][1] < _L2M['cuts_list'][1]
   and bc.l2_record(_l2item, _L2MLO)['band'] == 'Hard' and bc.l2_record(_l2item, _L2M)['band'] == 'Medium')
_l2fz = bc.l2_model_from_frozen(bc.l2_frozen(_L2M))
ck("FX-L2-12 D2 stability: a frozen model scores every fixture item identically to the live one",
   _l2fz is not None and all(bc.l2_record(_L2P['papers'][k]['questions'][q], _l2fz)['band'] == r['band']
                             for (k, q), r in _l2pyq.items()))
_l2_lopo = [bc.l2_model_for_scope({'papers': {k: v for k, v in _L2P['papers'].items() if k != _d}}, _l2sids, _L2LABS,
                                   measured_pct={'Easy': 3, 'Medium': 70, 'Hard': 27}) for _d in sorted(_L2P['papers'])]
ck("FX-L2-13 D2 stability (measured): leaving out any one past paper leaves the Hard cut where it is "
   "(the symmetric fields remove the swing the prototype showed: 26 -> 33)",
   all(_m['active'] and _m['cuts_list'][1] == _L2M['cuts_list'][1] for _m in _l2_lopo))
_l2fz_json = bc.l2_model_from_frozen(_js.loads(_js.dumps(bc.l2_frozen(_L2M))))
ck("FX-L2-13b D2 stability: the frozen model, after a JSON round trip as a blueprint stores it, scores "
   "every past question exactly as the live model",
   _l2fz_json is not None and _l2fz_json['cuts_list'] == _L2M['cuts_list']
   and all(bc.l2_record(_L2P['papers'][k]['questions'][q], _l2fz_json)['band'] == r['band'] for (k, q), r in _l2pyq.items()))
_l2pk = bc.pyq_grade_packet(dict(_L2P['papers']['18-Jul-2026']['questions']['71'], answer_smiles='CC(O)C(C)C(=O)O',
                                  closeness={'per_option': {'1': {'grade': 3}}}, steps=4, score=6),
                             '18-Jul-2026', 71)
ck("FX-L2-14 Q1 (c) blind PYQ grading packet carries no band, concepts, steps or key",
   not ({'band', 'named_concepts', 'steps', 'score', 'answer_smiles', 'distractor_mechanisms', 'closeness'} & set(_l2pk))
   and 'CC(O)C(C)C(=O)O' not in _js.dumps(_l2pk)
   and _l2pk['key'] == '18-Jul-2026:Q71')
_l2g = {f'{k}:Q{q}': ('Hard' if r['load'] and r['load'] >= 6 else ('Easy' if (r['load'] or 0) <= 1 else 'Medium'))
        for (k, q), r in _l2pyq.items()}
_l2mg = bc.l2_model_for_scope(_L2P, _l2sids, _L2LABS, pyq_grades=_l2g, measured_pct={'Easy': 3, 'Medium': 70, 'Hard': 27})
ck("FX-L2-15 Q1 (c): when blind grades exist for the pool they set the shares (not the rubric's measured_pct)",
   _l2mg['shares_source'] == 'pyq_grades' and _l2mg['shares'] != {'Easy': 3, 'Medium': 70, 'Hard': 27})
_l2_src = _cluster_source('blueprint_core.py', '# CLUSTER DL — DIFFICULTY LAYER', '# END CLUSTER L2')
_l2_code = '\n'.join(l for l in _l2_src.split('\n') if not l.lstrip().startswith('#'))
ck("FX-L2-16 generic by construction: no exam identifier anywhere in Clusters DL / L2 (code, docstrings)",
   not _re.search(r'CSIR|RPSC|GATE_|NEET|JEE|IIT_JAM|_NET_|LIFE_SCIENCE', _l2_src))
ck("FX-L2-17 no hard stop in Clusters DL / L2 (no SystemExit / raise / HARD STOP)",
   not _re.search(r'SystemExit|\braise\b|HARD STOP|\[HS:', _l2_code))


def _self_test():
    total = PASS + len(FAILS)
    print(f"SELF-TEST: {PASS}/{total} PASS")
    for n in FAILS:
        print("  FAIL:", n)
    return not FAILS


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
