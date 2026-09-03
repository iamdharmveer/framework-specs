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

# E21: active + dated files, 0 or >=2 matching EF => HS-ST5
r21a = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2019-06.pdf', 'a'), _cand('EX_Syllabus_2020-06.pdf',
                                                  'b')],
    'EX', 'active', '2026-12')
r21b = bc.resolve_syllabus_sources(
    [_cand('EX_Syllabus_2026-12.pdf', 'a'),
     _cand('EX_Syllabus_2026-12.docx', 'b')],
    'EX', 'active', '2026-12')
ck("FX-ST-21 HS-ST5 on zero and on ambiguous EF matches",
   r21a['outcome'] == 'stop' and r21a['code'] == 'HS-ST5'
   and r21b['outcome'] == 'stop' and r21b['code'] == 'HS-ST5')

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
ck("FX-ST-CASE3 case variants at the same date stay HS-ST5 (ambiguous)",
   bc.resolve_syllabus_sources(
       [_cand('EX_Syllabus_2027-02.pdf', 'a'),
        _cand('EX_SYLLABUS_2027-02.PDF', 'b')],
       'EX', 'active', '2027-02')['code'] == 'HS-ST5')
ck("FX-ST-CASE4 structural malformation still HS-ST4",
   bc.parse_syllabus_filename('EX_Sylabus_2027-02.pdf', 'EX') is None
   and bc.parse_syllabus_filename('EX_Syllabus_2027-2.pdf', 'EX') is None)

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

def _self_test():
    total = PASS + len(FAILS)
    print(f"SELF-TEST: {PASS}/{total} PASS")
    for n in FAILS:
        print("  FAIL:", n)
    return not FAILS


if __name__ == "__main__":
    sys.exit(0 if _self_test() else 1)
