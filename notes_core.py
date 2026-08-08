"""
notes_core.py v1.0 — Shared engine for the Notes pipeline (Steps NB/NC/NA/ND).

v1.0 — 2026-08-08 — INITIAL RELEASE. Registry schema + transitions, syllabus
    hashing, unit-code naming, role/tier tables (Framework_NotesBlueprint
    §4/§5), density-gate constants and checks (Framework_NotesCreate §5,
    machine-gated in NotesAudit §5 G-1), and the OMML structural assertion
    (NotesAudit §5 G-2 — LibreOffice preview blindness rule).
"""
import hashlib, json, os, re, zipfile
from datetime import datetime, timezone

# ---------------------------------------------------------------- constants
ROLES = ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
STATES = ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
TIERS = ("TIER-1", "TIER-2", "TIER-3")

# Density gate (Framework_NotesCreate §5)
BULLET_TARGET_WORDS = 20
BULLET_HARD_CAP_WORDS = 25
TIER_PAGE_BANDS = {"TIER-1": (6, 15), "TIER-2": (4, 8), "TIER-3": (2, 5)}

REGISTRY_SCHEMA = "notes-registry/1.0"
BLUEPRINT_SCHEMA = "notes-blueprint/1.0"

_NSMATH = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- identity
def syllabus_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def unit_code(exam_code, s_no, t_no, st_no):
    return f"{exam_code}_S{int(s_no)}_T{int(t_no)}_ST{int(st_no):02d}"


def notes_filename(exam_code, s_no, t_no, st_no, slug):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", slug).strip("_")
    return f"{unit_code(exam_code, s_no, t_no, st_no)}_{slug}.docx"


# ---------------------------------------------------------------- roles/tiers
def assign_role(in_syllabus, pyq_count, is_bridge, recent3_count):
    """Framework_NotesBlueprint §1.2 + §4. Returns role or None (=excluded)."""
    if is_bridge:
        return "BRIDGE"
    if in_syllabus:
        return "PYQ_WEIGHTED" if pyq_count >= 3 else "COVERAGE"
    return "EVIDENCE_ADDED" if recent3_count >= 2 else None


def assign_tier(role, pyq_count):
    """Framework_NotesBlueprint §5."""
    if role == "PYQ_WEIGHTED":
        return "TIER-1" if pyq_count >= 15 else "TIER-2"
    if role == "EVIDENCE_ADDED":
        return "TIER-2"
    return "TIER-3"


# ---------------------------------------------------------------- registry
def registry_init(exam_code, syllabus_hash, level, units):
    reg = {
        "schema": REGISTRY_SCHEMA,
        "exam_code": exam_code,
        "syllabus_sha256": syllabus_hash,
        "exam_level": level,
        "created": _now(),
        "updated": _now(),
        "units": {},
    }
    for u in units:
        reg["units"][u["unit_code"]] = {
            "name": u["name"],
            "role": u["role"],
            "tier": u["tier"],
            "pyq_count": u.get("pyq_count", 0),
            "provenance": u.get("provenance", "syllabus"),
            "state": "BLUEPRINTED",
            "stale": False,
            "notes_version": None,
            "audit": None,
            "artifacts": {},
            "history": [{"at": _now(), "event": "BLUEPRINTED"}],
        }
    return reg


def registry_load(path):
    reg = json.load(open(path, encoding="utf-8"))
    if reg.get("schema") != REGISTRY_SCHEMA:
        raise ValueError(f"registry schema mismatch: {reg.get('schema')}")
    return reg


def registry_save(reg, path):
    reg["updated"] = _now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def transition(reg, unit_code_, new_state, **extra):
    order = {s: i for i, s in enumerate(STATES)}
    u = reg["units"][unit_code_]
    cur = u["state"]
    ok = (
        new_state in STATES
        and (order[new_state] == order[cur] + 1
             or (cur == "DELIVERED" and new_state == "AUDITED_PASS")   # ND §4 reopen
             or (cur == "AUDITED_PASS" and new_state == "DRAFTED"))    # NA §4 L-2 regen
    )
    if not ok:
        raise ValueError(f"illegal transition {cur} -> {new_state} for {unit_code_}")
    u["state"] = new_state
    u.update(extra)
    u["history"].append({"at": _now(), "event": new_state, **extra})
    return u


# ---------------------------------------------------------------- density gate
def _docx_xml(path):
    return zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")


def bullet_word_counts(docx_path):
    """Word count of every bulleted paragraph (numPr-carrying w:p)."""
    xml = _docx_xml(docx_path)
    counts = []
    for para in re.findall(r"<w:p\b.*?</w:p>", xml, re.S):
        if "<w:numPr>" not in para:
            continue
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S))
        words = len(re.findall(r"\S+", text))
        if words:
            counts.append(words)
    return counts


def density_gate(docx_path, tier, page_count):
    """Returns (passed: bool, findings: list[str]). page_count comes from the
    caller's render step (soffice) — this module never renders."""
    findings = []
    for w in bullet_word_counts(docx_path):
        if w > BULLET_HARD_CAP_WORDS:
            findings.append(f"bullet exceeds hard cap: {w} words")
    lo, hi = TIER_PAGE_BANDS[tier]
    if not (lo <= page_count <= hi):
        findings.append(f"page count {page_count} outside {tier} band {lo}-{hi}")
    return (not findings, findings)


# ---------------------------------------------------------------- OMML gate
def assert_omml(docx_path, expected_min, required_tokens=()):
    """NotesAudit §5 G-2: verify equations STRUCTURALLY. LibreOffice PDF
    previews drop OMML silently — never use them for equation checks."""
    xml = _docx_xml(docx_path)
    maths = re.findall(r"<m:oMath>.*?</m:oMath>", xml, re.S)
    if len(maths) < expected_min:
        raise AssertionError(f"OMML count {len(maths)} < expected {expected_min}")
    joined = "\n".join(maths)
    missing = [tok for tok in required_tokens if tok not in joined]
    if missing:
        raise AssertionError(f"OMML tokens missing: {missing}")
    return len(maths)
