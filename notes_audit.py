"""
notes_audit.py v1.0 — Engine for Notes Step NA (Framework_NotesAudit).

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
    if it["patches"] > MAX_PATCHES_PER_QUESTION:
        return "REGENERATE"          # spec §4 L-2
    return "REAUDIT"


def log_regeneration(report):
    report["regenerations"] += 1
    if report["regenerations"] > MAX_REGENERATIONS:
        return "DIAGNOSTIC"          # spec §4 L-3: data problem, stop looping
    return "CONTINUE"


def is_pass(report):
    """100% SOLVABLE; FIGURE_PENDING items permitted per spec §1."""
    return all(v["verdict"] == "SOLVABLE" for v in report["items"].values())


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
