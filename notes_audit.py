"""
notes_audit.py v1.2 — Engine for Notes Step NA (Framework_NotesAudit).

v1.2 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES (Framework_NotesAudit v2.0.0).
    NB now ingests the corpus and stores, per question, the verbatim
    correct_answer, the explanation, and the stem_figures / solution_figures
    split. So NA changes: (1) figure handling — bind_figures() and
    extract_media() are REMOVED; figures are read from the bank question
    (figures_for()), never re-downloaded or re-bound (owner decision 1/6).
    (2) Answer mode — ground_truth is the default and only spec path; NA solves
    from the notes and matches the bank's answer with type-aware helpers
    verdict_against_key() / _mcq / msq (notes_core.msq_match) / nat
    (notes_core.nat_within_tolerance, rounding precision — owner decision 4b).
    (3) KEY_FLAG is DROPPED from the report (owner decision 4a); the doc key is
    authoritative and never re-derived. new_report() no longer carries
    key_flags. is_pass and the §4 convergence counters are unchanged; their
    v1.1 self-tests are retained verbatim.

v1.1 — 2026-08-08 — DEPLOYMENT-REVIEW FIXES. (1) is_pass now has a floor: an
    empty verdict set, or fewer verdicts than the bank's expected count, can
    never certify AUDITED_PASS (vacuous all() defect). (2) Convergence
    counters aligned to spec §4: the 3rd failed patch on a question returns
    REGENERATE (was off by one), and the 3rd regeneration returns DIAGNOSTIC,
    the same >= shape. (3) self_test() added per CLAUDE.md engine rule, with
    fixtures that fail on each rectified defect.

v1.0 — 2026-08-08 — INITIAL RELEASE. Verdict/report schema, convergence-loop
    bookkeeping (patch counter -> regen -> diagnostic per spec §4), figure
    extraction + positional binding (spec §1), and the audit-report writer.
    The closed-book SOLVE itself is Claude-driven; this engine keeps the
    state machine honest.
"""
import json, os, re
from datetime import datetime, timezone
import notes_core

VERDICTS = ("SOLVABLE", "PARTIAL", "NOT")
REPORT_SCHEMA = "notes-audit-report/1.1"   # v1.1: key_flags removed
MAX_PATCHES_PER_QUESTION = 3     # spec §4 L-2
MAX_REGENERATIONS = 3            # spec §4 L-3


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_report(unit_code, notes_version, mode="ground_truth"):
    """Ground-truth is the default and only spec path (owner decision 4): the
    bank carries the authoritative answer, so NA never self-generates one.
    KEY_FLAG is gone. figure_pending stays as an (normally empty) safety list
    for the degenerate case where a bank figure is missing; it is not the
    primary path since NB reads every image (owner decision 6)."""
    assert mode == "ground_truth", "self-answer mode retired (owner decision 4)"
    return {"schema": REPORT_SCHEMA, "unit_code": unit_code,
            "notes_version": notes_version, "mode": mode, "started": _now(),
            "items": {}, "patch_log": [], "regenerations": 0,
            "figure_pending": [], "gates": {}}


def record(report, qid, verdict, notes_location, answer, note=""):
    assert verdict in VERDICTS, verdict
    report["items"][qid] = {"verdict": verdict, "where": notes_location,
                            "answer": answer, "note": note,
                            "patches": report["items"].get(qid, {}).get("patches", 0)}


def log_patch(report, qid, gap, patch_ref):
    it = report["items"][qid]
    it["patches"] += 1
    report["patch_log"].append({"at": _now(), "qid": qid, "gap": gap,
                                "patch": patch_ref})
    if it["patches"] >= MAX_PATCHES_PER_QUESTION:
        return "REGENERATE"          # spec §4 L-2: the 3rd failed patch regenerates
    return "REAUDIT"


def log_regeneration(report):
    report["regenerations"] += 1
    if report["regenerations"] >= MAX_REGENERATIONS:
        return "DIAGNOSTIC"          # spec §4 L-3: data problem, stop looping
    return "CONTINUE"


def is_pass(report, expected_count=None):
    """100% SOLVABLE with a floor: zero audited questions is never a pass,
    and when the bank's expected question count is supplied, fewer verdicts
    than expected is never a pass. FIGURE_PENDING items permitted per §1."""
    items = report["items"]
    if not items:
        return False
    if expected_count is not None and len(items) < int(expected_count):
        return False
    return all(v["verdict"] == "SOLVABLE" for v in items.values())


def write_report(report, path):
    report["finished"] = _now()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False); f.write("\n")
    return path


# ---------------------------------------------------------------- figures
# NB already extracted every image from Drive and bound it to its question,
# splitting stem figures from solution figures at the "Correct Answer:" line
# (owner decision 3). NA does NOT re-open any .docx. It reads the split off the
# bank question. extract_media()/bind_figures() are retired as of v1.2.
def figures_for(bank_question):
    """The stem figures a solver must SEE to answer this question. Solution
    figures are excluded — they are part of the key, not the prompt."""
    return list(bank_question.get("stem_figures", []))


def missing_figures(bank_question):
    """A stem figure the bank flagged but whose media file did not resolve.
    Normally empty (NB reads every image). A non-empty result parks the
    question in report['figure_pending'] rather than hard-stopping the run."""
    return [f for f in bank_question.get("stem_figures", [])
            if str(f).startswith("UNRESOLVED:")]


# ------------------------------------------------------ ground-truth matching
def verdict_against_key(qtype, computed, key, stem=""):
    """Type-aware ground-truth comparison (owner decision 4). Returns
    (matched: bool, detail: str). MCQ: option-token equality. MSQ: unordered
    set (notes_core.msq_match). NAT: rounding-precision tolerance from the stem
    (notes_core.nat_within_tolerance). None computed -> never a match."""
    t = (qtype or "").upper()
    if computed is None:
        return False, "no answer produced from the notes"
    if t == "MSQ":
        ok = notes_core.msq_match(computed, key)
        return ok, f"MSQ set {'==' if ok else '!='} key"
    if t == "NAT":
        p = notes_core.nat_precision_from_stem(stem)
        tgt = notes_core.normalize_answer("NAT", key)
        got = notes_core.normalize_answer("NAT", computed)
        ok = notes_core.nat_within_tolerance(got, tgt, p)
        return ok, f"NAT match at {p} dp ({got} vs {tgt})"
    ok = notes_core.normalize_answer("MCQ", computed) == \
        notes_core.normalize_answer("MCQ", key)
    return ok, f"MCQ option {'==' if ok else '!='} key"


# ---------------------------------------------------------------- self-test
def self_test():
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    # Defect fixture 1: vacuous pass on empty report (the shipped bug)
    r = new_report("U", "0.1", "ground_truth")
    check("empty report is never a pass", is_pass(r) is False)
    record(r, "Q1", "SOLVABLE", "1.1", "a")
    check("one solvable, no floor -> pass", is_pass(r) is True)
    check("floor: 1 of 37 is not a pass", is_pass(r, expected_count=37) is False)
    for i in range(2, 38):
        record(r, f"Q{i}", "SOLVABLE", "1.1", "a")
    check("floor: 37 of 37 passes", is_pass(r, expected_count=37) is True)
    record(r, "Q1", "PARTIAL", "1.1", None)
    check("any PARTIAL blocks pass", is_pass(r, expected_count=37) is False)

    # Defect fixture 2: off-by-one convergence counters (the shipped bug)
    r2 = new_report("U", "0.1", "ground_truth")
    record(r2, "Q1", "PARTIAL", "1.2", None)
    check("patch 1 -> REAUDIT", log_patch(r2, "Q1", "g", "p1") == "REAUDIT")
    check("patch 2 -> REAUDIT", log_patch(r2, "Q1", "g", "p2") == "REAUDIT")
    check("patch 3 -> REGENERATE", log_patch(r2, "Q1", "g", "p3") == "REGENERATE")
    check("regen 1 -> CONTINUE", log_regeneration(r2) == "CONTINUE")
    check("regen 2 -> CONTINUE", log_regeneration(r2) == "CONTINUE")
    check("regen 3 -> DIAGNOSTIC", log_regeneration(r2) == "DIAGNOSTIC")

    # Verdict vocabulary + report write/read round trip
    try:
        record(r2, "QX", "MAYBE", "1.1", None)
        check("invalid verdict rejected", False)
    except AssertionError:
        check("invalid verdict rejected", True)
    import tempfile, os, json as _json
    fp = os.path.join(tempfile.gettempdir(), "na_selftest_report.json")
    write_report(r2, fp)
    check("report round-trips", _json.load(open(fp))["unit_code"] == "U")
    check("report has no key_flags (dropped)", "key_flags" not in r2)

    # v1.2: self-answer mode is retired
    try:
        new_report("U", "0.1", "question_only")
        check("self-answer mode rejected", False)
    except AssertionError:
        check("self-answer mode rejected", True)

    # v1.2: figures read from the bank question (no docx re-open)
    bq = {"stem_figures": ["image3.png", "UNRESOLVED:rId7"],
          "solution_figures": ["image9.png"]}
    check("figures_for returns stem figures only",
          figures_for(bq) == ["image3.png", "UNRESOLVED:rId7"])
    check("missing_figures flags only unresolved",
          missing_figures(bq) == ["UNRESOLVED:rId7"])

    # v1.2: ground-truth verdicts by type (owner decision 4)
    ok, _ = verdict_against_key("MCQ", "2", "2")
    check("MCQ match", ok is True)
    check("MCQ mismatch", verdict_against_key("MCQ", "3", "2")[0] is False)
    check("MSQ unordered match", verdict_against_key("MSQ", [3, 1], "1,3")[0] is True)
    check("MSQ mismatch", verdict_against_key("MSQ", [1, 2], "1,3")[0] is False)
    check("NAT within stem precision",
          verdict_against_key("NAT", 0.4149, "0.41",
                              "give the value to 2 decimal places")[0] is True)
    check("NAT outside precision",
          verdict_against_key("NAT", 0.418, "0.41",
                              "give the value to 2 decimal places")[0] is False)
    check("NAT nearest-integer stem",
          verdict_against_key("NAT", 711.4, "711",
                              "answer to the nearest integer")[0] is True)
    check("no computed answer never matches",
          verdict_against_key("NAT", None, "0.41", "")[0] is False)

    print(f"notes_audit self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_audit.py — Notes Step NA engine. Run with --self-test.")
