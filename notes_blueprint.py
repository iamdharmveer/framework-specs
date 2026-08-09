"""
notes_blueprint.py v1.2 — Engine for Notes Step NB (Framework_NotesBlueprint).

v1.2 — 2026-08-08 — DEPLOYMENT-REVIEW FIXES. The EVIDENCE_ADDED path no
    longer crashes: a folded-in analysis-only subtopic requires explicit
    placement (s_no/t_no/st_no) supplied by the blueprint author, validated
    with a clear error naming the unit instead of a KeyError; its slug
    defaults from its name; and it joins its topic's seq_in_topic counter so
    outline numbering stays gapless. Excluded rows still need no placement.
    self_test() added per CLAUDE.md engine rule with a fixture that fails on
    the rectified defect.

v1.1 — 2026-08-08 — REFINEMENT SUPPORT. extract_allowed_types() reads the
    Range tab Type column through notes_core.normalize_types (HARD STOP on an
    empty set); build_blueprint() accepts and emits allowed_question_types,
    computes per-unit seq_in_topic from list order, and passes through
    optional prose_ban_exemptions; the registry is initialised with the
    allowed type set.

v1.0 — 2026-08-08 — INITIAL RELEASE. Exam Pattern xlsx reader (Overview /
    Sections / Range / optional Sources tabs), Option-B evidence-expansion
    filter, blueprint writer, exclusion report. Syllabus/PYQ-Analysis parsing
    is Claude-driven per spec §2; this engine validates and assembles.
"""
import json, os
from datetime import datetime, timezone
import notes_core


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_exam_pattern(xlsx_path):
    """Returns dict with overview / sections / ranges / sources. HARD STOP if
    the Overview Level field is absent (spec §2 S-2)."""
    from openpyxl import load_workbook
    wb = load_workbook(xlsx_path, data_only=True)
    out = {"overview": {}, "sections": [], "ranges": [], "sources": []}
    for row in wb["Overview"].iter_rows(values_only=True):
        if row and row[0] is not None:
            out["overview"][str(row[0]).strip()] = row[1]
    if not any(k.lower().startswith("level") for k in out["overview"]):
        raise SystemExit("HARD STOP: Exam Pattern Overview has no Level field")
    for name, key in (("Sections", "sections"), ("Range", "ranges")):
        if name in wb.sheetnames:
            rows = list(wb[name].iter_rows(values_only=True))
            hdr = [str(h).strip() for h in rows[0]]
            out[key] = [dict(zip(hdr, r)) for r in rows[1:] if any(r)]
    if "Sources" in wb.sheetnames:
        rows = list(wb["Sources"].iter_rows(values_only=True))
        hdr = [str(h).strip().lower() for h in rows[0]]
        out["sources"] = [dict(zip(hdr, r)) for r in rows[1:] if any(r)]
    return out


def extract_allowed_types(pattern):
    """Ordered unique canonical types from the Range tab. HARD STOP if empty
    (Framework_NotesBlueprint §6 O-1)."""
    col = [r.get("Type") for r in pattern.get("ranges", [])]
    types = notes_core.normalize_types(col)
    if not types:
        raise SystemExit("HARD STOP: no recognisable question types in the "
                         "Exam Pattern Range tab")
    return types


def resolve_sources(chat_link, pattern_sources, project_files):
    """Spec §3 priority: chat link > Sources tab > project Files."""
    if chat_link:
        return {"mode": "chat", "entries": [{"label": "chat", "url": chat_link}]}
    if pattern_sources:
        return {"mode": "xlsx-sources-tab", "entries": pattern_sources}
    docx = [f for f in project_files if f.lower().endswith(".docx")]
    return {"mode": "project-files", "entries": [{"label": f} for f in docx]}


def build_blueprint(exam_code, level, syllabus_hash, sources, unit_rows,
                    analysis_only_rows, allowed_question_types=None):
    """unit_rows: in-syllabus rows {s_no,t_no,st_no,name,slug,pyq_count,
    is_bridge,bridge_reason?,provenance}. analysis_only_rows: PYQ-analysis
    subtopics absent from syllabus {name,pyq_count,recent3_count}; a row
    that folds in (Option B satisfied) MUST also carry its placement
    {s_no,t_no,st_no} and may carry slug and prose_ban_exemptions."""
    units, excluded = [], []
    _topic_seq = {}
    for r in unit_rows:
        key = (r["s_no"], r["t_no"])
        _topic_seq[key] = _topic_seq.get(key, 0) + 1
        r = dict(r, _seq=_topic_seq[key])
        role = notes_core.assign_role(True, r["pyq_count"], r.get("is_bridge", False), 0)
        units.append({
            "unit_code": notes_core.unit_code(exam_code, r["s_no"], r["t_no"], r["st_no"]),
            "name": r["name"], "slug": r["slug"], "role": role,
            "tier": notes_core.assign_tier(role, r["pyq_count"]),
            "pyq_count": r["pyq_count"],
            "provenance": r.get("provenance", "syllabus"),
            "bridge_reason": r.get("bridge_reason"),
            "seq_in_topic": r["_seq"],
            "prose_ban_exemptions": r.get("prose_ban_exemptions", []),
        })
    for r in analysis_only_rows:
        role = notes_core.assign_role(False, r["pyq_count"], False, r["recent3_count"])
        if role is None:
            excluded.append({"name": r["name"], "pyq_count": r["pyq_count"],
                             "recent3_count": r["recent3_count"],
                             "reason": "out-of-syllabus, <2 PYQs in latest 3 years"})
        else:
            missing = [k for k in ("s_no", "t_no", "st_no") if r.get(k) is None]
            if missing:
                raise ValueError(
                    "EVIDENCE_ADDED unit %r folds into the blueprint and "
                    "needs placement: missing %s" % (r["name"], ", ".join(missing)))
            key = (r["s_no"], r["t_no"])
            _topic_seq[key] = _topic_seq.get(key, 0) + 1
            units.append({
                "unit_code": notes_core.unit_code(exam_code, r["s_no"], r["t_no"], r["st_no"]),
                "name": r["name"], "slug": r.get("slug") or r["name"], "role": role,
                "tier": notes_core.assign_tier(role, r["pyq_count"]),
                "pyq_count": r["pyq_count"], "provenance": "evidence-added",
                "seq_in_topic": _topic_seq[key],
                "prose_ban_exemptions": r.get("prose_ban_exemptions", []),
            })
    return {
        "schema": notes_core.BLUEPRINT_SCHEMA,
        "exam_code": exam_code, "level": level,
        "allowed_question_types": allowed_question_types or [],
        "syllabus_sha256": syllabus_hash, "generated": _now(),
        "sources": sources, "units": units, "excluded": excluded,
    }


def write_blueprint_and_registry(bp, out_dir="."):
    bp_path = os.path.join(out_dir, "notes_blueprint.json")
    with open(bp_path, "w", encoding="utf-8") as f:
        json.dump(bp, f, indent=2, ensure_ascii=False); f.write("\n")
    reg = notes_core.registry_init(bp["exam_code"], bp["syllabus_sha256"],
                                   bp["level"], bp["units"])
    reg["allowed_question_types"] = bp.get("allowed_question_types") or None
    reg_path = os.path.join(out_dir, "notes_registry.json")
    notes_core.registry_save(reg, reg_path)
    return bp_path, reg_path


# ---------------------------------------------------------------- self-test
def self_test():
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    rows = [dict(s_no=1, t_no=2, st_no=8, name="EK", slug="EK", pyq_count=37),
            dict(s_no=1, t_no=2, st_no=9, name="B", slug="B", pyq_count=4)]

    # Defect fixture: EVIDENCE_ADDED path crashed with KeyError (the shipped bug)
    ev = [dict(name="Oscillations", pyq_count=18, recent3_count=3,
               s_no=6, t_no=1, st_no=4)]
    try:
        bp = build_blueprint("EX", "Grad", "h", {"mode": "chat", "entries": []},
                             rows, ev, allowed_question_types=["MCQ"])
        u = [x for x in bp["units"] if x["provenance"] == "evidence-added"]
        check("evidence path builds", len(u) == 1
              and u[0]["unit_code"] == "EX_S6_T1_ST04"
              and u[0]["slug"] == "Oscillations"
              and u[0]["seq_in_topic"] == 1
              and u[0]["role"] == "EVIDENCE_ADDED")
    except KeyError:
        check("evidence path builds", False)

    try:
        build_blueprint("EX", "G", "h", {"mode": "chat", "entries": []}, rows,
                        [dict(name="Orphan", pyq_count=5, recent3_count=2)])
        check("missing placement raises ValueError", False)
    except ValueError as e:
        check("missing placement raises ValueError", "Orphan" in str(e))
    except KeyError:
        check("missing placement raises ValueError", False)

    bp = build_blueprint("EX", "G", "h", {"mode": "chat", "entries": []}, rows,
                         [dict(name="Weak", pyq_count=1, recent3_count=1)])
    check("excluded row needs no placement",
          bp["excluded"] and bp["excluded"][0]["name"] == "Weak")

    bp = build_blueprint("EX", "G", "h", {"mode": "chat", "entries": []}, rows,
                         [dict(name="Joined", pyq_count=6, recent3_count=2,
                               s_no=1, t_no=2, st_no=10)])
    seqs = {u["name"]: u["seq_in_topic"] for u in bp["units"]}
    check("evidence unit continues topic sequence",
          seqs == {"EK": 1, "B": 2, "Joined": 3})

    check("types extracted",
          extract_allowed_types({"ranges": [{"Type": "MCQ"}, {"Type": "NAT"}]})
          == ["MCQ", "NAT"])
    for bad in ([{"Kind": "MCQ"}], []):
        try:
            extract_allowed_types({"ranges": bad})
            check("empty type set hard-stops", False)
        except SystemExit:
            check("empty type set hard-stops", True)

    print(f"notes_blueprint self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_blueprint.py — Notes Step NB engine. Run with --self-test.")
