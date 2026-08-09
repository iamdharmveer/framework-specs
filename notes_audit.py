"""
notes_audit.py v1.1 — Engine for Notes Step NA (Framework_NotesAudit).

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
import json, os, re, zipfile
from datetime import datetime, timezone

VERDICTS = ("SOLVABLE", "PARTIAL", "NOT")
REPORT_SCHEMA = "notes-audit-report/1.0"
MAX_PATCHES_PER_QUESTION = 3     # spec §4 L-2
MAX_REGENERATIONS = 3            # spec §4 L-3


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_report(unit_code, notes_version, mode):
    assert mode in ("question_only", "ground_truth")
    return {"schema": REPORT_SCHEMA, "unit_code": unit_code,
            "notes_version": notes_version, "mode": mode, "started": _now(),
            "items": {}, "patch_log": [], "regenerations": 0,
            "figure_pending": [], "key_flags": [], "gates": {}}


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
def extract_media(docx_path, out_dir):
    """Unzip word/media/* to out_dir; returns extracted paths in zip order."""
    os.makedirs(out_dir, exist_ok=True)
    out = []
    with zipfile.ZipFile(docx_path) as z:
        for n in z.namelist():
            if n.startswith("word/media/"):
                tgt = os.path.join(out_dir, os.path.basename(n))
                with open(tgt, "wb") as f:
                    f.write(z.read(n))
                out.append(tgt)
    return out


def bind_figures(docx_path, anchors):
    """Positional binding (spec §1): anchors = ordered list of (qid, regex)
    where regex matches the question's date-tag in document.xml text. Each
    w:drawing between anchor i and anchor i+1 binds to anchors[i].qid.
    Returns {qid: [media_rIds]} for Claude to pair with extract_media order
    via the relationships file."""
    xml = zipfile.ZipFile(docx_path).read("word/document.xml").decode("utf-8")
    spans = []
    for qid, pat in anchors:
        m = re.search(pat, xml)
        if m:
            spans.append((m.start(), qid))
    spans.sort()
    bound = {qid: [] for _, qid in spans}
    for dm in re.finditer(r"<w:drawing>.*?r:embed=\"(rId\d+)\".*?</w:drawing>", xml, re.S):
        owner = None
        for start, qid in spans:
            if start <= dm.start():
                owner = qid
            else:
                break
        if owner:
            bound[owner].append(dm.group(1))
    return bound


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
    r = new_report("U", "0.1", "question_only")
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
    r2 = new_report("U", "0.1", "question_only")
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

    # bind_figures positional binding on a minimal fixture
    import zipfile, tempfile
    dx = os.path.join(tempfile.gettempdir(), "na_selftest_fig.docx")
    xml = ('<w:document><w:p><w:r><w:t>[10-Feb-2013 Q32]</w:t></w:r></w:p>'
           '<w:p><w:drawing><a:blip r:embed="rId9"/></w:drawing></w:p>'
           '<w:p><w:r><w:t>[10-Feb-2013 Q34]</w:t></w:r></w:p>'
           '<w:p><w:drawing><a:blip r:embed="rId12"/></w:drawing></w:p></w:document>')
    with zipfile.ZipFile(dx, "w") as z:
        z.writestr("word/document.xml", xml)
        z.writestr("word/media/image1.png", b"x")
    bound = bind_figures(dx, [("EK-021", "\\[10-Feb-2013 Q32\\]"),
                              ("EK-022", "\\[10-Feb-2013 Q34\\]")])
    check("figure binding by position",
          bound == {"EK-021": ["rId9"], "EK-022": ["rId12"]})
    check("media extraction", len(extract_media(dx, tempfile.mkdtemp())) == 1)

    print(f"notes_audit self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_audit.py — Notes Step NA engine. Run with --self-test.")
