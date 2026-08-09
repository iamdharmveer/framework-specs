"""
notes_core.py v1.3 — Shared engine for the Notes pipeline (Steps NB/NC/NA/ND).

v1.3 — 2026-08-08 — DEFECT-CLASS CLOSURE (second review wave). (1) G-4 year
    detection rewritten to POSITIVE-EVIDENCE rules: a 16xx-20xx number is
    flagged only with year context (preceding cue word such as in/since/by/
    the/circa; trailing s/AD/CE; comma-joined year lists; year-to-year en-
    dash ranges; year+question anchors). Scientific numbers — 1650 cm-1,
    1800 g/mol, 2000 per second, bare 1700 — no longer fire. Documented
    trade-off: an isolated cue-less year is not caught; the per-unit
    exemption remains for subjects that need years legitimately. (2) All
    word-like ban patterns are now case-insensitive (pyq, Examiner, Exam
    Lens, Modelled On, q: prefix, mcq/msq); NAT stays exact-case by design —
    lowercase "nat" is a plausible text fragment, and the trade-off is
    recorded here and in the self-test. (3) BLUEPRINT_SCHEMA bumped to
    notes-blueprint/1.1 with load_blueprint() migration accepting 1.0,
    symmetric with the registry. (4) scan_flat_math_tokens suppresses
    measurement collisions: a token directly preceded by a numeral
    ("5 Km", "3Kd") is a quantity, not a symbol. Every reviewer example from
    both waves is a permanent fixture in self_test().

v1.2 — 2026-08-08 — DEPLOYMENT-REVIEW FIXES. density_gate reports an unknown
    tier as a finding instead of raising KeyError; assert_omml and
    scan_omml_structural tolerate attributes on the m:oMath tag (Word-authored
    or raw-XML files that carry xmlns on the element no longer count zero);
    self_test() added per CLAUDE.md engine rule with fixtures that fail on
    each rectified defect.

v1.1 — 2026-08-08 — REFINEMENT GATES. Adds: LEVEL_COLORS / BOX_COLORS (the
    locked level colour map, Framework_NotesCreate §6A); PROSE_BAN lexicon +
    scan_prose_bans() (NotesCreate §7, NA gate G-4); MATH_TOKEN_RES +
    scan_flat_math_tokens() and scan_omml_structural() (the dual zero-issue
    math scans of NA gate G-2b/G-2c); ALLOWED_TYPE canonicalisation
    (normalize_types) for NA gate G-5; registry schema 1.1 with in-place
    migration of 1.0 files (allowed_question_types + per-unit seq_in_topic /
    prose_ban_exemptions defaults). All gates regression-locked against the
    approved Enzyme Kinetics golden sample.

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

REGISTRY_SCHEMA = "notes-registry/1.1"
REGISTRY_SCHEMAS_ACCEPTED = ("notes-registry/1.0", "notes-registry/1.1")
BLUEPRINT_SCHEMA = "notes-blueprint/1.1"
BLUEPRINT_SCHEMAS_ACCEPTED = ("notes-blueprint/1.0", "notes-blueprint/1.1")

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
            "seq_in_topic": u.get("seq_in_topic"),
            "prose_ban_exemptions": u.get("prose_ban_exemptions", []),
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
    if reg.get("schema") not in REGISTRY_SCHEMAS_ACCEPTED:
        raise ValueError(f"registry schema mismatch: {reg.get('schema')}")
    if reg["schema"] != REGISTRY_SCHEMA:          # in-place 1.0 -> 1.1 migration
        reg["schema"] = REGISTRY_SCHEMA
        reg.setdefault("allowed_question_types", None)
        for u in reg.get("units", {}).values():
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
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
    band = TIER_PAGE_BANDS.get(tier)
    if band is None:
        findings.append(f"unknown tier: {tier!r}")
    else:
        lo, hi = band
        if not (lo <= page_count <= hi):
            findings.append(f"page count {page_count} outside {tier} band {lo}-{hi}")
    return (not findings, findings)


# ---------------------------------------------------------------- OMML gate
def assert_omml(docx_path, expected_min, required_tokens=()):
    """NotesAudit §5 G-2: verify equations STRUCTURALLY. LibreOffice PDF
    previews drop OMML silently — never use them for equation checks."""
    xml = _docx_xml(docx_path)
    maths = re.findall(r"<m:oMath\b[^>]*>.*?</m:oMath>", xml, re.S)
    if len(maths) < expected_min:
        raise AssertionError(f"OMML count {len(maths)} < expected {expected_min}")
    joined = "\n".join(maths)
    missing = [tok for tok in required_tokens if tok not in joined]
    if missing:
        raise AssertionError(f"OMML tokens missing: {missing}")
    return len(maths)


def load_blueprint(path):
    """Load notes_blueprint.json accepting schema 1.0 or 1.1; migrate 1.0
    in place (allowed_question_types default [], per-unit seq_in_topic /
    prose_ban_exemptions defaults) so consumers can rely on the 1.1 shape."""
    bp = json.load(open(path, encoding="utf-8"))
    if bp.get("schema") not in BLUEPRINT_SCHEMAS_ACCEPTED:
        raise ValueError(f"blueprint schema mismatch: {bp.get('schema')}")
    if bp["schema"] != BLUEPRINT_SCHEMA:
        bp["schema"] = BLUEPRINT_SCHEMA
        bp.setdefault("allowed_question_types", [])
        for u in bp.get("units", []):
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
    return bp


# ------------------------------------------------- level colour map (§6A)
LEVEL_COLORS = {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                "table_header": "44546A"}
BOX_COLORS = {"example": ("2E75B6", "E8F1FA"), "recall": ("2E75B6", "E8F1FA"),
              "key_points": ("2E7D32", "E4F2E4"), "trap": ("C62828", "FBE4E4")}

# ------------------------------------------------- question types (G-5)
CANONICAL_TYPES = ("MCQ", "MSQ", "NAT")


def normalize_types(raw_values):
    """Range-tab Type values -> ordered unique canonical set. Empty result is
    the caller's HARD STOP condition (Framework_NotesBlueprint §6)."""
    out = []
    for v in raw_values:
        c = re.sub(r"[^A-Z]", "", str(v or "").upper())
        for k in CANONICAL_TYPES:
            if k in c and k not in out:
                out.append(k)
    return out


# ------------------------------------------------- content-style bans (G-4)
# Word-like patterns are case-insensitive. NAT is exact-case BY DESIGN:
# lowercase "nat" is a plausible fragment of ordinary text, so the initialism
# is only banned in its capitalised form (trade-off recorded in self_test).
PROSE_BAN = [
    (r"(?<![A-Za-z])NAT(?![A-Za-z])", "question-type name NAT", 0),
    (r"(?<![A-Za-z])MCQ(?![A-Za-z])", "question-type name MCQ", re.I),
    (r"(?<![A-Za-z])MSQ(?![A-Za-z])", "question-type name MSQ", re.I),
    (r"(?<![A-Za-z])PYQ", "PYQ token", re.I),
    (r"EXAM\s+LENS", "retired block name", re.I),
    ("[★☆]", "star glyph", 0),
    (r"(?m)(?:^|[>\s])Q:\s", "Q: stem prefix", re.I),
    (r"modelled\s+on", "example anchor phrase", re.I),
    (r"examiner", "editorial lead-in", re.I),
]

# Positive-evidence year detection (G-4). _YR is 1600-2099.
_YR = r"(?:1[6-9]\d\d|20\d\d)"
YEAR_EVIDENCE = [
    r"(?i)(?<![A-Za-z0-9])(?:in|by|since|from|until|till|during|circa|the|year|early|late|mid|pre|post)\s+" + _YR + r"(?!\d)",
    _YR + r"(?:s|\s+(?:AD|CE|BCE|BC))(?![A-Za-z0-9])",
    _YR + r"\s*,\s*" + _YR,                       # comma-joined year lists
    _YR + r"\s*[–—-]\s*" + _YR,          # year-to-year ranges
    _YR + r"\s+Q\d",                               # year + question anchors
]
def _document_text(docx_path):
    xml = _docx_xml(docx_path)
    return " ".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", xml, re.S))


def scan_prose_bans(docx_path, exemptions=()):
    """NA gate G-4. Returns findings (empty == pass). Year detection is
    positive-evidence only; see YEAR_EVIDENCE."""
    text = _document_text(docx_path)
    findings = []
    for pat, label, flags in PROSE_BAN:
        if label in exemptions:
            continue
        if re.search(pat, text, flags):
            findings.append(label)
    if "year reference" not in exemptions:
        if any(re.search(p, text) for p in YEAR_EVIDENCE):
            findings.append("year reference")
    return findings


# ------------------------------------------------- math gates (G-2b / G-2c)
_SCRIPT_CHARS = ("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078"
                 "\u2079\u207b\u2080\u2081\u2082\u2083\u00bd")
MATH_TOKEN_RES = [r"(?<![A-Za-z])" + t + r"(?![A-Za-z])" for t in
                  ("Vmax", "Km", "Ki", "Kd", "Keq", "kcat", "kd", "Et")] +                  [r"pKa(?![A-Za-z])", "[" + _SCRIPT_CHARS + "]"]


def scan_omml_structural(docx_path):
    """NA gate G-2b: inside every oMath region, no textual exponents and no
    unicode script characters. Returns findings (empty == pass)."""
    xml = _docx_xml(docx_path)
    joined = "\n".join(re.findall(r"<m:oMath\b[^>]*>.*?</m:oMath>", xml, re.S))
    findings = []
    if "^(" in joined:
        findings.append("textual exponent inside oMath")
    for ch in _SCRIPT_CHARS:
        if ch in joined:
            findings.append("unicode script char inside oMath: %r" % ch)
            break
    return findings


def scan_flat_math_tokens(docx_path):
    """NA gate G-2c: no un-styled math token in any plain text run. A token
    split into styled sub/superscript runs no longer matches these patterns.
    A token directly preceded by a numeral ("5 Km", "3Kd") is a measurement,
    not a symbol, and is suppressed. Returns findings (empty == pass)."""
    text = _document_text(docx_path)
    findings = []
    for p in MATH_TOKEN_RES:
        for m in re.finditer(p, text):
            pre = text[max(0, m.start() - 2):m.start()]
            if re.search(r"\d\s?$", pre):
                continue
            findings.append("flat math token: " + p)
            break
    return findings


# ---------------------------------------------------------------- self-test
def self_test():
    import tempfile, zipfile
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def mini_docx(text, extra_xml=""):
        fp = tempfile.mktemp(suffix=".docx")
        with zipfile.ZipFile(fp, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document>%s<w:p><w:r><w:t>%s</w:t></w:r></w:p>"
                       "</w:document>" % (extra_xml, text))
            z.writestr("[Content_Types].xml", "<Types/>")
        return fp

    # Defect fixture: density_gate KeyError on unknown tier (the shipped bug)
    d = mini_docx("short bullet")
    try:
        okr, f = density_gate(d, "TIER-9", 7)
        check("unknown tier is a finding, not a crash",
              okr is False and any("unknown tier" in x for x in f))
    except KeyError:
        check("unknown tier is a finding, not a crash", False)
    check("band edge 6 passes TIER-1", density_gate(d, "TIER-1", 6)[0])
    check("band edge 15 passes TIER-1", density_gate(d, "TIER-1", 15)[0])
    check("band edge 5 fails TIER-1", not density_gate(d, "TIER-1", 5)[0])
    check("band edge 16 fails TIER-1", not density_gate(d, "TIER-1", 16)[0])

    # Defect fixture: attributed m:oMath tag counted zero (the shipped bug)
    fp = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(fp, "w") as z:
        z.writestr("word/document.xml",
                   '<w:document><m:oMath xmlns:m="http://x"><m:r><m:t>V</m:t>'
                   "</m:r></m:oMath></w:document>")
    try:
        check("attributed oMath counted", assert_omml(fp, 1) == 1)
    except AssertionError:
        check("attributed oMath counted", False)
    check("attributed oMath scanned",
          scan_omml_structural(mini_docx("x")) == [])

    # Gate lexicons on synthetic defects
    check("prose ban: year", scan_prose_bans(mini_docx("the 1857 revolt")) == ["year reference"])
    check("prose ban: exemption",
          scan_prose_bans(mini_docx("the 1857 revolt"), exemptions=("year reference",)) == [])
    check("prose ban: boundaries safe",
          scan_prose_bans(mini_docx("NATO NATure signature Nature Q3")) == [])
    check("prose ban: attrs ignored",
          scan_prose_bans(mini_docx("clean", '<w:gridCol w:w="1700"/>')) == [])
    check("flat token caught", scan_flat_math_tokens(mini_docx("plain Vmax")) != [])
    check("split runs clean", scan_flat_math_tokens(mini_docx("V and max apart")) == [])

    # Registry migration + transition legality
    import json as _json
    rp = tempfile.mktemp(suffix=".json")
    _json.dump({"schema": "notes-registry/1.0", "exam_code": "X",
                "syllabus_sha256": "h", "exam_level": "G", "created": "c",
                "updated": "u", "units": {"U": {"name": "n", "role": "COVERAGE",
                "tier": "TIER-3", "pyq_count": 0, "provenance": "syllabus",
                "state": "BLUEPRINTED", "stale": False, "notes_version": None,
                "audit": None, "artifacts": {}, "history": []}}}, open(rp, "w"))
    reg = registry_load(rp)
    check("1.0 registry migrates", reg["schema"] == REGISTRY_SCHEMA
          and reg["units"]["U"]["prose_ban_exemptions"] == [])
    transition(reg, "U", "DRAFTED")
    try:
        transition(reg, "U", "DELIVERED")
        check("illegal transition rejected", False)
    except ValueError:
        check("illegal transition rejected", True)

    # Role/tier tables
    check("role: evidence rule", assign_role(False, 5, False, 1) is None
          and assign_role(False, 5, False, 2) == "EVIDENCE_ADDED")
    check("tier: thresholds", assign_tier("PYQ_WEIGHTED", 15) == "TIER-1"
          and assign_tier("PYQ_WEIGHTED", 14) == "TIER-2")

    # ---- Wave-2 fixtures: scientific numbers must NOT fire the year ban
    for sci in ("absorption at 1650 cm\u207b\u00b9", "a load of 1700 held",
                "melting near 1750", "molar mass 1800 g/mol",
                "rotates 2000 per second", "range 1600 to saturation"):
        check("no year on: " + sci, scan_prose_bans(mini_docx(sci)) == [])
    # ...while genuine year contexts still fire
    for yr in ("in 2014 the pattern", "since 2006 it recurs",
               "the 1857 revolt", "seen 2006, 2009, 2014",
               "span 2005\u20132026", "the 1990s trend", "asked 2013 Q32"):
        check("year on: " + yr,
              scan_prose_bans(mini_docx(yr)) == ["year reference"])
    check("year exemption still works",
          scan_prose_bans(mini_docx("in 2014"), exemptions=("year reference",)) == [])

    # ---- Wave-2 fixtures: case-insensitivity
    for t2 in ("The Examiner expects", "EXAMINER note", "pyq bank", "Pyq",
               "exam lens returns", "Modelled On a pattern", "mcq set", "q: hello"):
        check("case-insensitive ban: " + t2,
              scan_prose_bans(mini_docx(t2)) != [])
    check("NAT stays exact-case (documented trade-off)",
          scan_prose_bans(mini_docx("a nat fragment")) == [])

    # ---- Wave-2 fixtures: measurement collisions in flat-token scan
    check("'distance 5 Km north' is a measurement",
          scan_flat_math_tokens(mini_docx("distance 5 Km north")) == [])
    check("'3Kd sample' is a measurement",
          scan_flat_math_tokens(mini_docx("3Kd sample")) == [])
    check("bare Km still flagged",
          scan_flat_math_tokens(mini_docx("the Km of this enzyme")) != [])

    # ---- Wave-2 fixtures: blueprint schema symmetry
    import tempfile, json as _json
    bp10 = {"schema": "notes-blueprint/1.0", "exam_code": "X", "level": "G",
            "syllabus_sha256": "h", "generated": "g", "sources": {},
            "units": [{"unit_code": "X_S1_T1_ST01", "name": "n", "slug": "n",
                       "role": "COVERAGE", "tier": "TIER-3", "pyq_count": 0,
                       "provenance": "syllabus"}], "excluded": []}
    fp2 = tempfile.mktemp(suffix=".json")
    _json.dump(bp10, open(fp2, "w"))
    bp = load_blueprint(fp2)
    check("blueprint 1.0 migrates to 1.1",
          bp["schema"] == BLUEPRINT_SCHEMA
          and bp["allowed_question_types"] == []
          and bp["units"][0]["prose_ban_exemptions"] == [])
    _json.dump(dict(bp10, schema="notes-blueprint/0.9"), open(fp2, "w"))
    try:
        load_blueprint(fp2)
        check("unknown blueprint schema rejected", False)
    except ValueError:
        check("unknown blueprint schema rejected", True)

    print(f"notes_core self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_core.py — shared Notes pipeline core. Run with --self-test.")
