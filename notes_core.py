"""
notes_core.py v1.4 — Shared engine for the Notes pipeline (Steps NB/NC/NA/ND).

v1.4 — 2026-08-08 — THIRD-WAVE CLOSURE; file rewritten whole (no incremental
    patches) after edit-scar corruption. Reviewer designs adopted verbatim:
    (1) Year detection: determiner cue "the" removed (the "the 1700 peak" /
    "the 1857 revolt" shapes are indistinguishable; the cue-less year is the
    reviewer-accepted documented miss) plus a UNIT-SUFFIX VETO — a candidate
    with a unit token (cm, nm, K, g/mol, rpm, Hz, degree-C, mol, Pa, ppm, eV,
    ... incl. cm-1 spellings; bare "s" deliberately absent, it collides with
    the 1990s suffix) within a short following window is a measurement. The
    IR spellings 1600-1800 cm-1 and 1650, 1700, 1750 cm-1 scan clean.
    (2) Flat-token measurement suppression is Km-ONLY (the sole real unit
    collision, kilometre) and contextual: digit-preceded Km followed by
    punctuation/digit/direction/preposition is a distance; "the 2 Kd values",
    "Table 3 Km column", "compare 4 Vmax estimates" flag as symbol mentions.
    (3) The scan_omml_structural self-test fixture uses a defect-carrying
    ATTRIBUTED oMath region and asserts non-empty (previous fixture was
    vacuous). (4) Both reviewer tables are permanent fixtures.

v1.3 — 2026-08-08 — Second wave: positive-evidence years; case-insensitive
    lexicon (NAT exact-case by design); blueprint schema 1.1 + migration;
    first (too-broad) measurement suppression.
v1.2 — 2026-08-08 — density_gate unknown-tier finding; attribute-tolerant
    oMath matching; self_test() added per CLAUDE.md engine rule.
v1.1 — 2026-08-08 — Refinement gates: colour map, PROSE_BAN, math scans,
    type canonicalisation, registry 1.1 migration.
v1.0 — 2026-08-08 — Initial release.
"""
import hashlib, json, os, re, zipfile
from datetime import datetime, timezone

# ---------------------------------------------------------------- constants
ROLES = ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
STATES = ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
TIERS = ("TIER-1", "TIER-2", "TIER-3")

BULLET_TARGET_WORDS = 20
BULLET_HARD_CAP_WORDS = 25
TIER_PAGE_BANDS = {"TIER-1": (6, 15), "TIER-2": (4, 8), "TIER-3": (2, 5)}

REGISTRY_SCHEMA = "notes-registry/1.1"
REGISTRY_SCHEMAS_ACCEPTED = ("notes-registry/1.0", "notes-registry/1.1")
BLUEPRINT_SCHEMA = "notes-blueprint/1.1"
BLUEPRINT_SCHEMAS_ACCEPTED = ("notes-blueprint/1.0", "notes-blueprint/1.1")

LEVEL_COLORS = {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                "table_header": "44546A"}
BOX_COLORS = {"example": ("2E75B6", "E8F1FA"), "recall": ("2E75B6", "E8F1FA"),
              "key_points": ("2E7D32", "E4F2E4"), "trap": ("C62828", "FBE4E4")}

CANONICAL_TYPES = ("MCQ", "MSQ", "NAT")


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
    """Framework_NotesBlueprint rules. Returns role or None (=excluded)."""
    if is_bridge:
        return "BRIDGE"
    if in_syllabus:
        return "PYQ_WEIGHTED" if pyq_count >= 3 else "COVERAGE"
    return "EVIDENCE_ADDED" if recent3_count >= 2 else None


def assign_tier(role, pyq_count):
    if role == "PYQ_WEIGHTED":
        return "TIER-1" if pyq_count >= 15 else "TIER-2"
    if role == "EVIDENCE_ADDED":
        return "TIER-2"
    return "TIER-3"


def normalize_types(raw_values):
    """Range-tab Type values -> ordered unique canonical set."""
    out = []
    for v in raw_values:
        c = re.sub(r"[^A-Z]", "", str(v or "").upper())
        for k in CANONICAL_TYPES:
            if k in c and k not in out:
                out.append(k)
    return out


# ---------------------------------------------------------------- registry
def registry_init(exam_code, syllabus_hash, level, units):
    reg = {"schema": REGISTRY_SCHEMA, "exam_code": exam_code,
           "syllabus_sha256": syllabus_hash, "exam_level": level,
           "allowed_question_types": None,
           "created": _now(), "updated": _now(), "units": {}}
    for u in units:
        reg["units"][u["unit_code"]] = {
            "name": u["name"], "role": u["role"], "tier": u["tier"],
            "pyq_count": u.get("pyq_count", 0),
            "provenance": u.get("provenance", "syllabus"),
            "seq_in_topic": u.get("seq_in_topic"),
            "prose_ban_exemptions": u.get("prose_ban_exemptions", []),
            "state": "BLUEPRINTED", "stale": False, "notes_version": None,
            "audit": None, "artifacts": {},
            "history": [{"at": _now(), "event": "BLUEPRINTED"}]}
    return reg


def registry_load(path):
    reg = json.load(open(path, encoding="utf-8"))
    if reg.get("schema") not in REGISTRY_SCHEMAS_ACCEPTED:
        raise ValueError(f"registry schema mismatch: {reg.get('schema')}")
    if reg["schema"] != REGISTRY_SCHEMA:
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
    ok = (new_state in STATES
          and (order[new_state] == order[cur] + 1
               or (cur == "DELIVERED" and new_state == "AUDITED_PASS")
               or (cur == "AUDITED_PASS" and new_state == "DRAFTED")))
    if not ok:
        raise ValueError(f"illegal transition {cur} -> {new_state} for {unit_code_}")
    u["state"] = new_state
    u.update(extra)
    u["history"].append({"at": _now(), "event": new_state, **extra})
    return u


def load_blueprint(path):
    """Accept blueprint schema 1.0 or 1.1; migrate 1.0 in place so consumers
    can rely on the 1.1 shape (symmetric with registry_load)."""
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


# ---------------------------------------------------------------- docx text
def _docx_xml(path):
    return zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")


def _document_text(docx_path):
    xml = _docx_xml(docx_path)
    return " ".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", xml, re.S))


# ---------------------------------------------------------------- density
def bullet_word_counts(docx_path):
    xml = _docx_xml(docx_path)
    counts = []
    for para in re.findall(r"<w:p\b.*?</w:p>", xml, re.S):
        if "<w:numPr>" not in para:
            continue
        text = "".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", para, re.S))
        words = len(re.findall(r"\S+", text))
        if words:
            counts.append(words)
    return counts


def density_gate(docx_path, tier, page_count):
    """NA gate G-1. Unknown tier is a finding, never a crash."""
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


# ---------------------------------------------------------------- prose bans
# Word-like patterns are case-insensitive. NAT is exact-case BY DESIGN:
# lowercase "nat" is a plausible fragment of ordinary text.
PROSE_BAN = [
    (r"(?<![A-Za-z])NAT(?![A-Za-z])", "question-type name NAT", 0),
    (r"(?<![A-Za-z])MCQ(?![A-Za-z])", "question-type name MCQ", re.I),
    (r"(?<![A-Za-z])MSQ(?![A-Za-z])", "question-type name MSQ", re.I),
    (r"(?<![A-Za-z])PYQ", "PYQ token", re.I),
    (r"EXAM\s+LENS", "retired block name", re.I),
    ("[\u2605\u2606]", "star glyph", 0),
    (r"(?m)(?:^|[>\s])Q:\s", "Q: stem prefix", re.I),
    (r"modelled\s+on", "example anchor phrase", re.I),
    (r"examiner", "editorial lead-in", re.I),
]

# Positive-evidence year detection. _YR is 1600-2099. Determiner "the" is
# deliberately NOT a cue ("the 1700 peak" vs "the 1857 revolt" are the same
# shape); the cue-less year is the reviewer-accepted documented miss.
_YR = r"(?:1[6-9]\d\d|20\d\d)"
YEAR_EVIDENCE = [
    r"(?i)(?<![A-Za-z0-9])(?:in|by|since|from|until|till|during|circa|year|"
    r"early|late|mid|pre|post)\s+" + _YR + r"(?!\d)",
    _YR + r"(?:s|\s+(?:AD|CE|BCE|BC))(?![A-Za-z0-9])",
    _YR + r"\s*,\s*" + _YR,
    _YR + r"\s*[\u2013\u2014-]\s*" + _YR,
    _YR + r"\s+Q\d",
]

# Unit-suffix veto: a year-candidate with a unit token in the following
# window is a measurement. Bare "s" deliberately absent (1990s collision).
_UNIT_WINDOW = 26
_UNIT_RE = re.compile(
    "(?<![A-Za-z])"
    "(?:cm|mm|nm|\u00b5m|um|km|kg|mg|\u00b5g|g/mol|mol|K|\u00b0C|\u00b0F"
    "|Hz|kHz|MHz|GHz|rpm|Pa|kPa|MPa|ppm|eV|kJ|kcal|cal|mL|\u00b5L|L|g|min|h)"
    "(?:-1)?(?![A-Za-z])")


def _year_hit(text):
    for p in YEAR_EVIDENCE:
        for m in re.finditer(p, text):
            window = text[m.start():m.end() + _UNIT_WINDOW]
            if not _UNIT_RE.search(window):
                return True
    return False


def scan_prose_bans(docx_path, exemptions=()):
    """NA gate G-4. Returns findings (empty == pass)."""
    text = _document_text(docx_path)
    findings = []
    for pat, label, flags in PROSE_BAN:
        if label in exemptions:
            continue
        if re.search(pat, text, flags):
            findings.append(label)
    if "year reference" not in exemptions and _year_hit(text):
        findings.append("year reference")
    return findings


# ---------------------------------------------------------------- math gates
_SCRIPT_CHARS = ("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078"
                 "\u2079\u207b\u2080\u2081\u2082\u2083\u00bd")
MATH_TOKEN_RES = [r"(?<![A-Za-z])" + t + r"(?![A-Za-z])" for t in
                  ("Vmax", "Km", "Ki", "Kd", "Keq", "kcat", "kd", "Et")] + \
                 [r"pKa(?![A-Za-z])", "[" + _SCRIPT_CHARS + "]"]

_KM_DIST_FOLLOW = re.compile(
    r"^\s*(?:$|[.,;:)\]]|\d|north|south|east|west|away|apart|ahead|along|"
    r"across|downstream|upstream|offshore|long|wide|deep|high|per|from|to|"
    r"in|at|of|off|on|over|beyond|before|behind)", re.I)


def scan_flat_math_tokens(docx_path):
    """NA gate G-2c: no un-styled math token in any plain text run.
    Suppression is Km-ONLY (kilometre collision) and contextual:
    digit-preceded Km followed by punctuation/digit/direction/preposition is
    a distance. Digit-preceded Kd/Vmax/etc. remain symbol mentions."""
    text = _document_text(docx_path)
    findings = []
    for p in MATH_TOKEN_RES:
        for m in re.finditer(p, text):
            pre = text[max(0, m.start() - 2):m.start()]
            post = text[m.end():m.end() + 14]
            if ("Km" in p and re.search(r"\d\s?$", pre)
                    and _KM_DIST_FOLLOW.search(post)):
                continue
            findings.append("flat math token: " + p)
            break
    return findings


def scan_omml_structural(docx_path):
    """NA gate G-2b: no textual exponents or unicode script chars inside any
    oMath region. Attribute-tolerant tag matching."""
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


def assert_omml(docx_path, expected_min, required_tokens=()):
    """NA gate G-2a: verify equations STRUCTURALLY (XML), never via
    LibreOffice previews (LO drops OMML silently). Attribute-tolerant."""
    xml = _docx_xml(docx_path)
    maths = re.findall(r"<m:oMath\b[^>]*>.*?</m:oMath>", xml, re.S)
    if len(maths) < expected_min:
        raise AssertionError(f"OMML count {len(maths)} < expected {expected_min}")
    joined = "\n".join(maths)
    missing = [tok for tok in required_tokens if tok not in joined]
    if missing:
        raise AssertionError(f"OMML tokens missing: {missing}")
    return len(maths)


# ---------------------------------------------------------------- self-test
def self_test():
    import tempfile
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

    # density: unknown tier is a finding (v1.2 defect fixture); band edges
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

    # oMath: attributed tag counted (v1.2) AND attributed defect caught (v1.4
    # — the previously vacuous fixture, reviewer-prescribed)
    fp = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(fp, "w") as z:
        z.writestr("word/document.xml",
                   '<w:document><m:oMath xmlns:m="http://x"><m:r><m:t>V</m:t>'
                   "</m:r></m:oMath></w:document>")
    try:
        check("attributed oMath counted", assert_omml(fp, 1) == 1)
    except AssertionError:
        check("attributed oMath counted", False)
    fp2 = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(fp2, "w") as z:
        z.writestr("word/document.xml",
                   '<w:document><w:p><w:r><w:t>prose</w:t></w:r></w:p>'
                   '<m:oMath xmlns:m="http://x"><m:r><m:t>x^(2)</m:t></m:r>'
                   "</m:oMath></w:document>")
    check("attributed oMath defect caught",
          scan_omml_structural(fp2) == ["textual exponent inside oMath"])

    # prose bans: wave-1 basics
    check("prose ban: year", scan_prose_bans(mini_docx("in 1857 it began"))
          == ["year reference"])
    check("prose ban: exemption",
          scan_prose_bans(mini_docx("in 1857 it began"),
                          exemptions=("year reference",)) == [])
    check("prose ban: boundaries safe",
          scan_prose_bans(mini_docx("NATO NATure signature Nature Q3")) == [])
    check("prose ban: attrs ignored",
          scan_prose_bans(mini_docx("clean", '<w:gridCol w:w="1700"/>')) == [])

    # reviewer tables (waves 2+3) verbatim: must all be CLEAN
    for sci in ("absorption at 1650 cm\u207b\u00b9", "a load of 1700 held",
                "melting near 1750", "molar mass 1800 g/mol",
                "rotates 2000 per second", "range 1600 to saturation",
                "the 1650 cm-1 band", "at the 1700 peak",
                "from 1600 to 1800 cm-1", "range 1600-1800 cm-1",
                "band 1600, 1700 and 1750 cm-1",
                "bands at 1650, 1700, 1750 cm\u207b\u00b9",
                "range 1600\u20131800 cm\u207b\u00b9"):
        check("no year on: " + sci, scan_prose_bans(mini_docx(sci)) == [])
    for yr in ("in 2014 the pattern", "since 2006 it recurs",
               "seen 2006, 2009, 2014", "span 2005\u20132026",
               "the 1990s trend", "asked 2013 Q32"):
        check("year on: " + yr,
              scan_prose_bans(mini_docx(yr)) == ["year reference"])
    check("documented miss: the 1857 revolt",
          scan_prose_bans(mini_docx("the 1857 revolt")) == [])

    # case-insensitivity (wave-2 reverts bind); NAT exact-case trade-off
    for t2 in ("The Examiner expects", "EXAMINER note", "pyq bank", "Pyq",
               "exam lens returns", "Modelled On a pattern", "mcq set",
               "q: hello"):
        check("case-insensitive ban: " + t2,
              scan_prose_bans(mini_docx(t2)) != [])
    check("NAT stays exact-case (documented trade-off)",
          scan_prose_bans(mini_docx("a nat fragment")) == [])

    # reviewer table (wave 3): measurement vs symbol-mention
    for clean in ("distance 5 Km north", "walked 5 Km in the field",
                  "a 12 Km, then rest"):
        check("measurement clean: " + clean,
              scan_flat_math_tokens(mini_docx(clean)) == [])
    for flg in ("the 2 Kd values", "Table 3 Km column",
                "compare 4 Vmax estimates", "the Km of this enzyme"):
        check("symbol mention flags: " + flg,
              scan_flat_math_tokens(mini_docx(flg)) != [])
    check("split runs clean",
          scan_flat_math_tokens(mini_docx("V and max apart")) == [])

    # registry + blueprint migrations, transitions, roles/tiers
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
    bp10 = {"schema": "notes-blueprint/1.0", "exam_code": "X", "level": "G",
            "syllabus_sha256": "h", "generated": "g", "sources": {},
            "units": [{"unit_code": "X_S1_T1_ST01", "name": "n", "slug": "n",
                       "role": "COVERAGE", "tier": "TIER-3", "pyq_count": 0,
                       "provenance": "syllabus"}], "excluded": []}
    fp3 = tempfile.mktemp(suffix=".json")
    _json.dump(bp10, open(fp3, "w"))
    bp = load_blueprint(fp3)
    check("blueprint 1.0 migrates to 1.1", bp["schema"] == BLUEPRINT_SCHEMA
          and bp["allowed_question_types"] == []
          and bp["units"][0]["prose_ban_exemptions"] == [])
    _json.dump(dict(bp10, schema="notes-blueprint/0.9"), open(fp3, "w"))
    try:
        load_blueprint(fp3)
        check("unknown blueprint schema rejected", False)
    except ValueError:
        check("unknown blueprint schema rejected", True)
    check("role: evidence rule", assign_role(False, 5, False, 1) is None
          and assign_role(False, 5, False, 2) == "EVIDENCE_ADDED")
    check("tier: thresholds", assign_tier("PYQ_WEIGHTED", 15) == "TIER-1"
          and assign_tier("PYQ_WEIGHTED", 14) == "TIER-2")
    check("types normalized",
          normalize_types(["MCQ", "mcq (Single)", "NAT x"]) == ["MCQ", "NAT"])
    LC = LEVEL_COLORS
    check("colour map distinct",
          len({LC["L1"], LC["L2"], LC["L3"], LC["table_header"]}) == 4)
    check("example/recall boxes identical",
          BOX_COLORS["example"] == BOX_COLORS["recall"])

    print(f"notes_core self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_core.py — shared Notes pipeline core. Run with --self-test.")
