"""
notes_core.py v2.3 — Shared engine for the Notes pipeline (Steps NB/NC/NA/ND).

v2.3 — 2026-08-12 — REGISTRY SCHEMA 2.1 (GAP-2026-08-12-NADOCX patch P2 of 2).
    P1 landed the 2.1 SHAPE while still emitting 2.0, because an engine that
    emits a schema string its own specs do not cite is exactly the drift the
    SPEC-LOCK block catches. P2 moves the specs, so the emitted schema moves
    with them:
      REGISTRY_SCHEMA -> "notes-registry/2.1". Unit records now carry
      draft_ref (written by NC), final_ref (written by NA) and audit_summary
      (NA's registry-embedded replacement for the .md audit report). 1.x and
      2.0 registries still load, gaining the three fields as None — the P1
      read-side default is unchanged, so nothing needs migrating.
    No other surface changed.

v2.2 — 2026-08-12 — NOTESAUDIT-AS-WRITER FOUNDATION (GAP-2026-08-12-NADOCX,
    patch P1 of 2). PURELY ADDITIVE: no existing function changes behaviour,
    no emitted schema string moves, so P1 deploys and verifies on its own and
    every current NB/NC/NA/ND run is byte-for-byte unaffected. P2 (the
    Framework_NotesAudit v3.0.0 rewrite and its companion specs) is what
    switches these on.
      (1) TWO NEW FILENAME AUTHORITIES beside notes_filename, same recipe and
          same sanitisation, so no step ever spells a filename itself:
            notes_final_filename   -> {unit_code}_{Slug}_Final.docx   (NA)
            notes_deliver_filename -> {unit_code}_{Slug}_Deliver.docx (ND)
          All three are spec-lock-pinned. A step that needs a name CALLS one.
      (2) docx_ref_for / verify_docx_ref — the bank_ref/taxonomy_ref staleness
          idiom applied to a .docx: {filename, sha256, bytes, generated}.
          NotesAudit now receives its input as a CHAT ATTACHMENT rather than
          from Project Files, so there is no longer any implicit guarantee
          that the file audited is the file NotesCreate produced. This is the
          evidence for that check. verify_docx_ref reports filename mismatch
          and sha256 mismatch SEPARATELY, because the two mean different
          things: the first is usually the wrong unit attached, the second a
          hand-edit between steps.
      (3) "notes-registry/2.1" is ACCEPTED but NOT yet emitted (REGISTRY_SCHEMA
          stays 2.0 until P2 moves the specs with it — an engine that emitted a
          schema the specs do not cite would be exactly the drift this file's
          SPEC-LOCK exists to prevent). registry_load additionally defaults the
          2.1 per-unit fields draft_ref / final_ref / audit_summary, so a 2.0
          registry read by a P2 step already has the shape.
    Companion: notes_docx.py >= v1.0 (the shared builder; construction left
    prose and became an engine in the same patch).

v2.1 — 2026-08-10 — SPEC-LOCK TRIPWIRE (defect-class closure). A deployment
    review found Framework_NotesCreate F-1 restating the filename recipe in
    prose while notes_filename sanitises non-alphanumerics to "_" — one
    contract, two implementations. The CLASS is any spec restating an
    engine-owned literal. Resolution: (a) the specs now name the engine as the
    SINGLE AUTHORITY at every such spot; (b) this file gains a SPEC-LOCK
    self-test block in TWO halves.
      FORWARD half — pins each spec-restated literal to its documented value:
        LEVEL_COLORS/BOX_COLORS (NC §6A), density constants + tier page bands
        (NC §5 / NB §5), schema strings, ROLES/STATES/TIERS vocabularies, the
        unit_code format and the notes_filename recipe INCLUDING its
        sanitisation. Fires when the ENGINE moves.
      REVERSE half — reads Framework_NotesCreate.md and compares the prose
        itself (F-1's deferral + sanitisation statement, the §6A colour
        literals, §5 D-1's word counts). Fires when the SPEC moves.
    The reverse half is the one that closes THIS defect: the engine was
    already correct and the prose was stale, so every forward pin passes
    verbatim against the pre-v2.2.1 text. Coverage is deliberately narrow —
    NotesCreate only, the three literals above; NB §5's tier bands and the
    NA/ND restatements are NOT yet spec-read and can still drift prose-side.
    No functional surface changed; all v2.0 self-tests retained verbatim.

v2.0 — 2026-08-10 — TAXONOMY CONSUMER (Framework_NotesBlueprint v3.0.0; owner
    decision: ONE subtopic vocabulary across Test Creation and Notes Creation).
    The Step-5 [ExamCode]_subtopic_manifest.json is now the single source of
    truth for Notes unit identity, mirroring the Mock pipeline's Cross-Step
    Subtopic Contract (Framework_Blueprint RULES 1/2/2a). New here:
      (1) load_subtopic_manifest() — loads + structurally validates the manifest
          and HARD-STOPS (ValueError) on an exam_code mismatch (wrong exam's
          manifest in Files can never be consumed silently).
      (2) taxonomy_ref_for() / verify_taxonomy_ref() — the same staleness idiom
          as bank_ref: {path, sha256, subtopics, generated} over the manifest
          bytes, so a re-uploaded manifest is detectable and flips units STALE.
      (3) assign_numbering(manifest, prior) — derives S/T/ST numbers from
          manifest row order, PRESERVING any prior assignment verbatim (persisted
          numbering: a Step-5 re-run that inserts or reorders subtopics never
          renumbers already-assigned units; new sids append with next numbers).
      (4) resolve_unit() — the three-tier operator-input resolution shared by
          NC/NA/ND: exact Sub Topic Id -> 'Subject::Topic::Sub Topic Name'
          scope (norm per component) -> bare Sub Topic Name (norm). Unique hit
          proceeds; multiple hits return 'ambiguous' with the candidates; zero
          hits return 'none' with nearest-name suggestions. Never fuzzy-picks.
      (5) sid_slug() — the sid's final component, used as the F-1 filename slug.
      (6) REGISTRY_SCHEMA -> notes-registry/2.0 and BLUEPRINT_SCHEMA ->
          notes-blueprint/2.0: units are KEYED BY sid (registry_init keys by
          u['sid'] when present, else legacy u['unit_code']); unit records carry
          sid, section, topic, unit_code, slug; the registry carries
          taxonomy_ref. 1.x registries/blueprints still load (read-only
          migration: sid defaults None; a real migration is a re-blueprint).
    All v1.8 self-tests retained verbatim; v2.0 adds its own.

v1.8 — 2026-08-10 — POST-DEPLOY REVIEW (drift class closed + doc fixes).
    (A) subtopic_key is a DERIVED field that was also STORED in every bank
    question, and the readers compared a fresh key against the stored one — so the
    v1.7 normalization change meant a bank written by v1.6 returned 0 questions for
    any subtopic containing '&' or an en-dash. Root fix: bank_questions_for and
    derive_taxonomy_counts now RECOMPUTE the key from each question's
    subject/topic/subtopic and never trust the stored value, which ends the drift
    class for this and any future subtopic_key change. The stored key is now
    informational only. PYQ_BANK_SCHEMA -> notes-pyq-bank/1.1 (accepts 1.0 and
    1.1); bank_load migrates a 1.0 bank by refreshing its stored keys so an
    inspected bank is self-consistent. (C) load_blueprint docstring corrected to
    say it accepts 1.0/1.1/1.2 and migrates to the 1.2 shape (the code already
    did). No public signature changed; all v1.7 self-tests retained.

v1.7 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
    subtopic_key now REUSES syllabus_provenance.norm per path component — the same
    canonical form the rest of the framework's taxonomy joins use (NFKC, dash
    unification, & -> and, '/' kept as data) — and additionally collapses spaces
    around '/'. Previously it only lowercased + collapsed whitespace, so a subtopic
    written "Microbial & Plant Biotech" in the syllabus and "Microbial and Plant
    Biotech" on the paper header produced DIFFERENT keys; the bank count never
    joined the blueprint unit, which silently got pyq_count=0 and the wrong tier.
    Measured before the fix: 4 of 5 realistic label variants missed the join.
    No public signature changed; downstream (bank_add_question stores the key,
    derive_taxonomy_counts / bank_questions_for read it) is unaffected beyond
    producing correct joins. All v1.6 self-tests retained.

v1.6 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 1 (bank_ref staleness link). The
    blueprint now carries a real bank_ref so a blueprint built from bank vN can
    never be silently paired with bank vM. BLUEPRINT_SCHEMA -> notes-blueprint/1.2
    (load_blueprint migrates 1.0/1.1 by defaulting bank_ref=None); new
    verify_bank_ref(bank_path, bank_ref) recomputes the bank's sha256 and returns
    (ok, detail) so NC §1.2's "stale bank" stop finally has the evidence to fire.
    file_sha256() is exposed (syllabus_sha256 kept as an alias). No other v1.5
    surface changed.

v1.5 — 2026-08-10 — NOTES-INGEST BASE (Framework_NotesBlueprint v2.0.0). NB is
    now the eager full-corpus ingest step: it reads every sorted-PYQ paper from
    Drive via corpus_io and emits a verified notes_pyq_bank.json that NC and NA
    consume read-only. New here: (1) PYQ_BANK_SCHEMA + bank_new/bank_add_paper/
    bank_add_question/bank_validate/bank_save/bank_load with per-question fields
    incl. verbatim correct_answer + explanation and a stem_figures/
    solution_figures split; (2) subtopic_key() and derive_taxonomy_counts(),
    which compute subtopic-wise pyq_count + recent-3-year counts DIRECTLY from
    the bank so the separate PYQ Analysis doc is no longer a prerequisite
    (owner decision 5i); (3) parse_exam_date_from_filename() — the filename is
    authoritative for exam date (owner decision 2/3); (4) ground-truth answer
    matching: normalize_answer(), nat_precision_from_stem(),
    nat_within_tolerance() (rounding-precision, owner decision 4b) and
    msq_match() (unordered set). Nothing in the v1.4 gate/registry surface
    changed; all v1.4 self-tests are retained verbatim.

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
import syllabus_provenance
from datetime import datetime, timezone

# ---------------------------------------------------------------- constants
ROLES = ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
STATES = ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
TIERS = ("TIER-1", "TIER-2", "TIER-3")

BULLET_TARGET_WORDS = 20
BULLET_HARD_CAP_WORDS = 25
TIER_PAGE_BANDS = {"TIER-1": (6, 15), "TIER-2": (4, 8), "TIER-3": (2, 5)}

# v2.3: the specs now cite 2.1 (Framework_NotesAudit v3.0.0 /
# Framework_NotesCreate v2.3.0), so the engine emits it. P1 deliberately held
# this back for one release: an engine emitting a schema string its own specs
# do not name is precisely the drift the SPEC-LOCK block at the foot of this
# file exists to catch.
REGISTRY_SCHEMA = "notes-registry/2.1"
REGISTRY_SCHEMAS_ACCEPTED = ("notes-registry/1.0", "notes-registry/1.1",
                             "notes-registry/2.0", "notes-registry/2.1")
BLUEPRINT_SCHEMA = "notes-blueprint/2.0"
BLUEPRINT_SCHEMAS_ACCEPTED = ("notes-blueprint/1.0", "notes-blueprint/1.1",
                              "notes-blueprint/1.2", "notes-blueprint/2.0")

LEVEL_COLORS = {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                "table_header": "44546A"}
BOX_COLORS = {"example": ("2E75B6", "E8F1FA"), "recall": ("2E75B6", "E8F1FA"),
              "key_points": ("2E7D32", "E4F2E4"), "trap": ("C62828", "FBE4E4")}

CANONICAL_TYPES = ("MCQ", "MSQ", "NAT")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- identity
def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# syllabus_sha256 kept as a named alias for existing call sites / clarity.
syllabus_sha256 = file_sha256


def unit_code(exam_code, s_no, t_no, st_no):
    return f"{exam_code}_S{int(s_no)}_T{int(t_no)}_ST{int(st_no):02d}"


def _notes_stem(exam_code, s_no, t_no, st_no, slug):
    """The one place the {unit_code}_{Slug} stem is formed. Every filename
    authority below derives from it, so the sanitisation rule cannot drift
    between the draft, the audited file and the delivered file."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", slug).strip("_")
    return f"{unit_code(exam_code, s_no, t_no, st_no)}_{slug}"


def notes_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesCreate F-1 — the NC DRAFT filename."""
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + ".docx"


def notes_final_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesAudit — the AUDITED, student-ready filename.

    v2.2. NA emits one file in every outcome and it always carries this name,
    so an operator on a phone can never confuse NC's draft with NA's certified
    output. The stem is shared with notes_filename, so the two can never
    disagree about sanitisation.
    """
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + "_Final.docx"


def notes_deliver_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesDeliver — the portal-formatted delivery filename."""
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + "_Deliver.docx"


def docx_ref_for(path):
    """A staleness/provenance ref over a .docx, mirroring bank_ref and
    taxonomy_ref. Stored by NC as draft_ref and by NA as final_ref."""
    return {"filename": os.path.basename(path),
            "sha256": file_sha256(path),
            "bytes": os.path.getsize(path),
            "generated": _now()}


def verify_docx_ref(path, ref, expected_filename=None):
    """Returns (ok, kind, detail). kind is one of:
        "ok" | "missing_ref" | "not_found" | "filename" | "sha256"

    The kinds are reported SEPARATELY on purpose. A filename mismatch almost
    always means the wrong unit's file was attached to the trigger — a
    different defect, with a different remedy, from a sha256 mismatch, which
    means the right file was attached but its bytes changed since the
    producing step wrote it (a hand-edit in between).
    """
    if expected_filename and os.path.basename(path) != expected_filename:
        return (False, "filename",
                f"attached file is {os.path.basename(path)!r} but this unit's "
                f"filename is {expected_filename!r} — the wrong unit's "
                f"document appears to be attached.")
    if not ref or not ref.get("sha256"):
        return (False, "missing_ref",
                "no reference recorded for this document by the producing "
                "step — re-run it so the reference exists.")
    if not os.path.exists(path):
        return (False, "not_found", f"file not found at {path}.")
    actual = file_sha256(path)
    if actual != ref["sha256"]:
        return (False, "sha256",
                f"the recorded document is sha256 {ref['sha256'][:12]}… but "
                f"the file present is {actual[:12]}… — it was modified after "
                f"the producing step wrote it.")
    return (True, "ok", "document matches the recorded reference.")


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
def registry_init(exam_code, syllabus_hash, level, units, taxonomy_ref=None):
    """v2.0: units are KEYED BY sid (the verbatim Step-5 Sub Topic Id) when the
    unit carries one; a legacy unit without a sid keys by unit_code so 1.x-shaped
    callers still work. Unit records carry the manifest triple (section, topic,
    name==display_name verbatim) plus the DERIVED unit_code and slug; the
    registry carries taxonomy_ref (verify_taxonomy_ref staleness link)."""
    reg = {"schema": REGISTRY_SCHEMA, "exam_code": exam_code,
           "syllabus_sha256": syllabus_hash, "exam_level": level,
           "allowed_question_types": None, "taxonomy_ref": taxonomy_ref,
           "created": _now(), "updated": _now(), "units": {}}
    for u in units:
        key = u.get("sid") or u["unit_code"]
        reg["units"][key] = {
            "sid": u.get("sid"), "name": u["name"],
            "section": u.get("section"), "topic": u.get("topic"),
            "unit_code": u.get("unit_code"), "slug": u.get("slug"),
            "role": u["role"], "tier": u["tier"],
            "pyq_count": u.get("pyq_count", 0),
            "provenance": u.get("provenance", "syllabus"),
            "seq_in_topic": u.get("seq_in_topic"),
            "prose_ban_exemptions": u.get("prose_ban_exemptions", []),
            "state": "BLUEPRINTED", "stale": False, "notes_version": None,
            "audit": None, "artifacts": {},
            # v2.3 (notes-registry/2.1)
            "draft_ref": None, "final_ref": None, "audit_summary": None,
            "history": [{"at": _now(), "event": "BLUEPRINTED"}]}
    return reg


def registry_load(path):
    """Accept registry schema 1.0/1.1/2.0; migrate older ones IN PLACE to the
    2.0 shape (read-only migration: a 1.x unit gains sid=None and keeps its
    unit_code key — sid-keyed identity requires a re-blueprint at NB, which is
    cheap because the ingested bank is untouched)."""
    reg = json.load(open(path, encoding="utf-8"))
    if reg.get("schema") not in REGISTRY_SCHEMAS_ACCEPTED:
        raise ValueError(f"registry schema mismatch: {reg.get('schema')}")
    if reg["schema"] not in (REGISTRY_SCHEMA, "notes-registry/2.1"):
        reg["schema"] = REGISTRY_SCHEMA
        reg.setdefault("allowed_question_types", None)
        reg.setdefault("taxonomy_ref", None)
        for key, u in reg.get("units", {}).items():
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
            u.setdefault("sid", None)
            u.setdefault("section", None)
            u.setdefault("topic", None)
            u.setdefault("slug", None)
            u.setdefault("unit_code", key)
    # v2.2 (additive, applied to EVERY accepted schema): the 2.1 per-unit
    # fields are defaulted on load, so a P2 step reads a uniform shape whether
    # the registry on disk was written by a 1.x, 2.0 or 2.1 producer.
    for u in reg.get("units", {}).values():
        u.setdefault("draft_ref", None)
        u.setdefault("final_ref", None)
        u.setdefault("audit_summary", None)
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
    """Accept blueprint schema 1.0/1.1/1.2/2.0; migrate older ones in place so
    consumers can rely on the 2.0 shape (symmetric with registry_load): a 1.x
    unit gains sid/section/topic = None and taxonomy_ref = None."""
    bp = json.load(open(path, encoding="utf-8"))
    if bp.get("schema") not in BLUEPRINT_SCHEMAS_ACCEPTED:
        raise ValueError(f"blueprint schema mismatch: {bp.get('schema')}")
    if bp["schema"] != BLUEPRINT_SCHEMA:
        bp["schema"] = BLUEPRINT_SCHEMA
        bp.setdefault("allowed_question_types", [])
        bp.setdefault("bank_ref", None)
        bp.setdefault("taxonomy_ref", None)
        for u in bp.get("units", []):
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
            u.setdefault("sid", None)
            u.setdefault("section", None)
            u.setdefault("topic", None)
    return bp


def verify_bank_ref(bank_path, bank_ref):
    """Fix 1 (deployment review): the staleness link NC §1.2 needs. Returns
    (ok, detail). A blueprint with no bank_ref predates the bank and must be
    rebuilt at NB. A bank_ref whose sha256 does not match the bank on disk means
    the blueprint was built from a DIFFERENT bank than the one present — the
    exact silent-mismatch this catches."""
    if not bank_ref or not bank_ref.get("sha256"):
        return (False, "blueprint carries no bank_ref — rebuild it at NB (the "
                       "blueprint predates the current bank).")
    if not os.path.exists(bank_path):
        return (False, f"notes_pyq_bank.json not found at {bank_path}.")
    actual = file_sha256(bank_path)
    if actual != bank_ref["sha256"]:
        return (False, "STALE BANK: the blueprint was built from bank sha256 "
                f"{bank_ref['sha256'][:12]}… but notes_pyq_bank.json is now "
                f"{actual[:12]}…. Re-run NB so blueprint and bank agree.")
    return (True, "bank_ref matches the bank on disk.")


# ================================================================ TAXONOMY
# v2.0 — the Step-5 subtopic manifest is the SINGLE SOURCE OF TRUTH for the
# Notes unit vocabulary (owner decision 2026-08-10; mirrors the Mock pipeline's
# Cross-Step Subtopic Contract). Notes NEVER mints a subtopic id. Step 5 is
# untouched: everything below CONSUMES [ExamCode]_subtopic_manifest.json.

def load_subtopic_manifest(path, expected_exam_code=None):
    """Load + structurally validate the Step-5 manifest. HARD STOP (ValueError)
    on: unreadable/shapeless file, empty subtopics, an entry missing
    display_name/section/topic, or an exam_code mismatch (the wrong exam's
    manifest in project Files must never be consumed silently). The Step-5 id
    recipe is NOT re-validated here — the recipe is Step 5's contract and may
    evolve; Notes treats each sid as an opaque verbatim key."""
    m = json.load(open(path, encoding="utf-8"))
    subs = m.get("subtopics")
    if not isinstance(subs, dict) or not subs:
        raise ValueError(f"subtopic manifest at {path} has no 'subtopics' map")
    for sid, v in subs.items():
        if not sid or not isinstance(sid, str):
            raise ValueError(f"subtopic manifest has an empty/non-string id: {sid!r}")
        missing = [k for k in ("display_name", "section", "topic")
                   if not (isinstance(v, dict) and v.get(k))]
        if missing:
            raise ValueError(f"manifest entry {sid!r} missing {missing}")
    mc = m.get("exam_code")
    if expected_exam_code and mc != expected_exam_code:
        raise ValueError(
            "HARD STOP: manifest exam_code %r does not match this project's "
            "exam_code %r — the wrong exam's %s is in project Files."
            % (mc, expected_exam_code, os.path.basename(str(path))))
    return m


def taxonomy_ref_for(manifest_path):
    """The {path, sha256, subtopics, generated} reference embedded in the
    blueprint + registry — the same staleness idiom as bank_ref. sha256 is over
    the manifest bytes on disk, so a re-uploaded/re-generated manifest is
    detectable (verify_taxonomy_ref) and flips units STALE at NB §7."""
    m = load_subtopic_manifest(manifest_path)
    return {"path": manifest_path, "sha256": file_sha256(manifest_path),
            "subtopics": len(m["subtopics"]), "generated": _now()}


def verify_taxonomy_ref(manifest_path, taxonomy_ref):
    """Mirror of verify_bank_ref for the subtopic manifest. Returns (ok, detail).
    A blueprint/registry with no taxonomy_ref predates the taxonomy-consumer
    architecture and must be rebuilt at NB. A sha256 mismatch means the manifest
    on disk is not the one the blueprint was built from."""
    if not taxonomy_ref or not taxonomy_ref.get("sha256"):
        return (False, "no taxonomy_ref — rebuild at NB (the blueprint predates "
                       "the taxonomy-consumer architecture).")
    if not os.path.exists(manifest_path):
        return (False, f"subtopic manifest not found at {manifest_path}.")
    actual = file_sha256(manifest_path)
    if actual != taxonomy_ref["sha256"]:
        return (False, "STALE TAXONOMY: the blueprint was built from manifest "
                f"sha256 {taxonomy_ref['sha256'][:12]}… but the manifest on disk "
                f"is {actual[:12]}…. Re-run NB so blueprint and taxonomy agree.")
    return (True, "taxonomy_ref matches the manifest on disk.")


def sid_slug(sid):
    """The sid's final dot-component — the filesystem-safe subtopic slug used
    as the F-1 filename slug (S/T/ST numbers already encode section + topic)."""
    return str(sid).rsplit(".", 1)[-1]


def assign_numbering(manifest, prior=None):
    """Derive per-sid S/T/ST numbers from MANIFEST ROW ORDER, preserving any
    prior assignment VERBATIM (persisted numbering, owner decision 2026-08-10):
    a Step-5 re-run that inserts or reorders subtopics never renumbers an
    already-assigned unit — delivered filenames and printed title numbers stay
    stable. New sections/topics/subtopics take the next free number in their
    scope. prior: {sid: {"s_no","t_no","st_no"}} (a prior registry's map; sids
    no longer in the manifest keep their numbers and are the caller's ORPHANED
    report). Returns {sid: {"s_no","t_no","st_no"}} covering the union."""
    subs = manifest["subtopics"]
    out = {}
    sec_no, top_no, st_used = {}, {}, {}
    for sid, num in (prior or {}).items():
        s, t, st = int(num["s_no"]), int(num["t_no"]), int(num["st_no"])
        out[sid] = {"s_no": s, "t_no": t, "st_no": st}
        v = subs.get(sid)
        if v:                       # anchor the section/topic numbers it proves
            sec_no.setdefault(v["section"], s)
            top_no.setdefault((v["section"], v["topic"]), t)
        st_used[(s, t)] = max(st_used.get((s, t), 0), st)
    next_sec = max(sec_no.values(), default=0)
    next_top = {}
    for (sec, _t), t in top_no.items():
        next_top[sec] = max(next_top.get(sec, 0), t)
    for sid, v in subs.items():     # manifest insertion order == taxonomy order
        if sid in out:
            continue
        sec, top = v["section"], v["topic"]
        if sec not in sec_no:
            next_sec += 1
            sec_no[sec] = next_sec
        s = sec_no[sec]
        if (sec, top) not in top_no:
            next_top[sec] = next_top.get(sec, 0) + 1
            top_no[(sec, top)] = next_top[sec]
        t = top_no[(sec, top)]
        st_used[(s, t)] = st_used.get((s, t), 0) + 1
        out[sid] = {"s_no": s, "t_no": t, "st_no": st_used[(s, t)]}
    return out


def resolve_unit(units_by_sid, operator_input):
    """Three-tier operator-input resolution (shared by NC/NA/ND; the operator
    copies a cell from [ExamCode]_taxonomy.xlsx — Sub Topic Id, a
    'Subject::Topic::Sub Topic Name' scope, or the bare Sub Topic Name).
    units_by_sid: {sid: {..., 'name'/'display_name', 'section', 'topic'}}.
    Returns {'status': 'ok'|'ambiguous'|'none', 'sid', 'via', 'matches',
    'suggestions', 'detail'}. NEVER fuzzy-picks: multiple bare-name hits are
    returned for the operator to choose; zero hits return nearest-name
    suggestions and stop."""
    def _name(u):
        return u.get("display_name") or u.get("name") or ""
    n = syllabus_provenance.norm
    t = str(operator_input or "").strip().strip('"').strip("'").strip()
    if not t:
        return {"status": "none", "sid": None, "via": None, "matches": [],
                "suggestions": [], "detail": "empty unit reference"}
    if t in units_by_sid:
        return {"status": "ok", "sid": t, "via": "sid", "matches": [t],
                "suggestions": [], "detail": "exact Sub Topic Id"}
    if "::" in t:
        parts = [p.strip() for p in t.split("::")]
        if len(parts) != 3:
            return {"status": "none", "sid": None, "via": "scope", "matches": [],
                    "suggestions": [],
                    "detail": "a scope must be Subject::Topic::Sub Topic Name "
                              "(3 parts) — got %d part(s)" % len(parts)}
        want = tuple(n(p) for p in parts)
        hits = [sid for sid, u in units_by_sid.items()
                if (n(u.get("section")), n(u.get("topic")), n(_name(u))) == want]
        if len(hits) == 1:
            return {"status": "ok", "sid": hits[0], "via": "scope",
                    "matches": hits, "suggestions": [], "detail": "scope match"}
        return {"status": "ambiguous" if hits else "none", "sid": None,
                "via": "scope", "matches": hits, "suggestions": [],
                "detail": "scope matched %d unit(s)" % len(hits)}
    want = n(t)
    hits = [sid for sid, u in units_by_sid.items() if n(_name(u)) == want]
    if len(hits) == 1:
        return {"status": "ok", "sid": hits[0], "via": "name", "matches": hits,
                "suggestions": [], "detail": "unique Sub Topic Name"}
    if hits:
        return {"status": "ambiguous", "sid": None, "via": "name",
                "matches": hits, "suggestions": [],
                "detail": "Sub Topic Name matches %d units — re-trigger with "
                          "the Subject::Topic::Sub Topic Name scope or the "
                          "Sub Topic Id" % len(hits)}
    sugg = [sid for sid, u in units_by_sid.items()
            if want and (want in n(_name(u)) or n(_name(u)) in want)][:5]
    return {"status": "none", "sid": None, "via": "name", "matches": [],
            "suggestions": sugg,
            "detail": "no unit named %r — copy the exact Sub Topic Name (or "
                      "Sub Topic Id) from [ExamCode]_taxonomy.xlsx" % t}


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


# ================================================================ PYQ BANK
# The bank is NB's ingest artifact (notes_pyq_bank.json). It is a PROJECT
# artifact, not a framework file — its SCHEMA lives here so it is bootstrap-
# verified and unit-testable. NC filters it per subtopic; NA solves against
# its verbatim correct_answer. Both consume it read-only; neither re-reads Drive.
PYQ_BANK_SCHEMA = "notes-pyq-bank/1.1"
PYQ_BANK_SCHEMAS_ACCEPTED = ("notes-pyq-bank/1.0", "notes-pyq-bank/1.1")

BANK_REQUIRED_FIELDS = ("bank_id", "paper_key", "exam_date", "exam_year",
                        "q_no", "type", "subject", "topic", "subtopic", "stem")

_MONTHS = {m: i for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"), 1)}


def parse_exam_date_from_filename(name):
    """Exam date from a sorted-PYQ filename (owner decision 2/3: the filename is
    authoritative and stable). Returns (iso 'YYYY-MM-DD', year int,
    label 'DD-Mon-YYYY') or None. Tolerant of prefixes/suffixes, 'Copy of',
    '(1)', and DD-Mon-YYYY / DDMonYYYY / Mon-YYYY / YYYY-only shapes."""
    stem = re.sub(r"\.(?:docx|doc)$", "", os.path.basename(str(name)), flags=re.I)
    m = re.search(r"(?<!\d)(\d{1,2})[\-_ ]?([A-Za-z]{3,9})[\-_ ]?((?:19|20)\d\d)",
                  stem)
    if m and _MONTHS.get(m.group(2)[:3].lower()):
        d, mon, y = int(m.group(1)), _MONTHS[m.group(2)[:3].lower()], int(m.group(3))
        if 1 <= d <= 31:
            return (f"{y:04d}-{mon:02d}-{d:02d}", y,
                    f"{d:02d}-{m.group(2)[:3].title()}-{y}")
    m = re.search(r"(?<![A-Za-z])([A-Za-z]{3,9})[\-_ ]?((?:19|20)\d\d)", stem)
    if m and _MONTHS.get(m.group(1)[:3].lower()):
        mon, y = _MONTHS[m.group(1)[:3].lower()], int(m.group(2))
        return (f"{y:04d}-{mon:02d}-01", y, f"{m.group(1)[:3].title()}-{y}")
    m = re.search(r"(?<!\d)((?:19|20)\d\d)(?!\d)", stem)
    if m:
        y = int(m.group(1))
        return (f"{y:04d}-01-01", y, str(y))
    return None


def subtopic_key(subject, topic, subtopic):
    """Canonical subtopic identity so bank counts and blueprint units join even
    when the syllabus and the paper header differ only in punctuation or unicode.
    Reuses syllabus_provenance.norm per component (NFKC, dash unification,
    & -> and, casefold, '/' kept as data) — the same normalization the rest of the
    framework's taxonomy joins use — and additionally collapses spaces around '/'
    so 'Optics/Polarization' and 'Optics / Polarization' resolve identically."""
    def n(x):
        return re.sub(r"\s*/\s*", "/", syllabus_provenance.norm(x))
    return f"{n(subject)}|||{n(topic)}|||{n(subtopic)}"


def normalize_answer(qtype, raw):
    """Normalise a doc-declared answer by type (never re-derived; owner
    decision 4). MCQ -> option string ('2'); MSQ -> sorted int list ([1, 3]);
    NAT -> float."""
    t = (qtype or "").upper()
    s = str("" if raw is None else raw).strip()
    if t == "MSQ":
        return sorted({int(x) for x in re.findall(r"\d+", s)})
    if t == "NAT":
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        return float(m.group(0)) if m else None
    m = re.search(r"\d+", s)
    return m.group(0) if m else s


def nat_precision_from_stem(stem):
    """Decimal places a NAT stem asks for (NC B3 requires NAT stems to state
    rounding). Defaults to 2. 'nearest integer' -> 0."""
    s = stem or ""
    if re.search(r"nearest\s+(?:integer|whole)", s, re.I):
        return 0
    m = re.search(r"(?:to|up\s*to|correct\s+to|round(?:ed)?\s+to)\s+(\d+)\s*"
                  r"(?:decimal|dp|place)", s, re.I) \
        or re.search(r"(\d+)\s*decimal\s*place", s, re.I)
    return int(m.group(1)) if m else 2


def nat_within_tolerance(computed, target, precision_decimals=2):
    """Ground-truth NAT match (owner decision 4b): equal after rounding BOTH to
    the stem's stated precision. None on either side is never a match."""
    if computed is None or target is None:
        return False
    p = int(precision_decimals)
    return round(float(computed), p) == round(float(target), p)


def msq_match(computed, target):
    """MSQ ground-truth match: unordered set equality."""
    def norm(x):
        if isinstance(x, (list, tuple, set)):
            return {int(i) for i in x}
        return {int(i) for i in re.findall(r"\d+", str(x))}
    return norm(computed) == norm(target)


def bank_new(exam_code):
    return {"schema": PYQ_BANK_SCHEMA, "exam_code": exam_code,
            "created": _now(), "updated": _now(),
            "papers": [], "questions": []}


def bank_add_paper(bank, paper_key, exam_date, exam_year, filename,
                   n_questions, image_report=None):
    bank["papers"].append({
        "paper_key": paper_key, "exam_date": exam_date,
        "exam_year": int(exam_year), "filename": filename,
        "questions": int(n_questions), "image_report": image_report or {}})


def bank_add_question(bank, rec):
    """Append one validated question. rec keys: the BANK_REQUIRED_FIELDS plus
    optional complexity, options, correct_answer, explanation (verbatim),
    stem_figures, solution_figures, concept_tags. stem_figures present ->
    figure flag True (NC FIGURE dependency; owner decision 3 split)."""
    missing = [k for k in BANK_REQUIRED_FIELDS if rec.get(k) in (None, "")]
    if missing:
        raise ValueError(f"bank question {rec.get('bank_id')!r} missing {missing}")
    t = str(rec["type"]).upper()
    if t not in CANONICAL_TYPES:
        raise ValueError(f"bank question {rec['bank_id']!r} non-canonical type "
                         f"{rec['type']!r}")
    q = {"bank_id": rec["bank_id"], "paper_key": rec["paper_key"],
         "exam_date": rec["exam_date"], "exam_year": int(rec["exam_year"]),
         "q_no": rec["q_no"], "type": t, "complexity": rec.get("complexity"),
         "subject": rec["subject"], "topic": rec["topic"],
         "subtopic": rec["subtopic"],
         "subtopic_key": subtopic_key(rec["subject"], rec["topic"], rec["subtopic"]),
         "stem": rec["stem"], "options": list(rec.get("options", [])),
         "correct_answer": rec.get("correct_answer"),
         "explanation": rec.get("explanation", ""),
         "stem_figures": list(rec.get("stem_figures", [])),
         "solution_figures": list(rec.get("solution_figures", [])),
         "figure": bool(rec.get("stem_figures")),
         "concept_tags": list(rec.get("concept_tags", []))}
    bank["questions"].append(q)
    return q


def bank_validate(bank):
    if bank.get("schema") not in PYQ_BANK_SCHEMAS_ACCEPTED:
        raise ValueError(f"bank schema mismatch: {bank.get('schema')}")
    ids = [q["bank_id"] for q in bank.get("questions", [])]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"duplicate bank_id(s): {dupes}")
    for q in bank.get("questions", []):
        if str(q.get("type")).upper() not in CANONICAL_TYPES:
            raise ValueError(f"bank_id {q.get('bank_id')!r} bad type {q.get('type')!r}")
    return True


def bank_save(bank, path):
    bank["updated"] = _now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)
    return path


def bank_load(path):
    bank = json.load(open(path, encoding="utf-8"))
    bank_validate(bank)
    # Migrate a pre-1.1 bank: subtopic_key is DERIVED, and older banks stored it
    # under a weaker normalization. Refresh the stored key from the authoritative
    # subject/topic/subtopic so an inspected bank is self-consistent, and stamp the
    # schema. Reads recompute the key regardless (bank_questions_for /
    # derive_taxonomy_counts), so this migration is cosmetic — the drift class is
    # already closed; it just keeps the stored field honest.
    if bank.get("schema") != PYQ_BANK_SCHEMA:
        for q in bank.get("questions", []):
            q["subtopic_key"] = subtopic_key(q.get("subject"), q.get("topic"),
                                             q.get("subtopic"))
        bank["schema"] = PYQ_BANK_SCHEMA
    return bank


def bank_questions_for(bank, subject, topic, subtopic):
    """Every bank question under one subtopic (NC §1 unit filter). Identity is
    RECOMPUTED from each question's stored subject/topic/subtopic — the stored
    subtopic_key is never trusted — so a bank written by an older notes_core with
    a different subtopic_key normalization still joins correctly."""
    k = subtopic_key(subject, topic, subtopic)
    return [q for q in bank["questions"]
            if subtopic_key(q["subject"], q["topic"], q["subtopic"]) == k]


def derive_taxonomy_counts(bank, latest_years=3):
    """Owner decision 5(i): subtopic-wise pyq_count and recent-N-year counts
    computed DIRECTLY from the ingested bank — the separate PYQ Analysis doc is
    no longer required. 'recent3' counts questions whose exam_year is among the
    top `latest_years` DISTINCT exam years present in the corpus (so a corpus
    that stops in 2024 still has a well-defined recent window). Returns
    {subtopic_key: {subject, topic, subtopic, pyq_count, recent3_count,
    per_year{year:count}}}."""
    years = sorted({q["exam_year"] for q in bank["questions"]}, reverse=True)
    recent = set(years[:max(0, int(latest_years))])
    out = {}
    for q in bank["questions"]:
        # Recompute the key from stored fields — never trust the stored
        # subtopic_key — so counts are correct even on a bank written by an older
        # notes_core (drift class closed, v1.8).
        e = out.setdefault(subtopic_key(q["subject"], q["topic"], q["subtopic"]),
                           {"subject": q["subject"], "topic": q["topic"],
                            "subtopic": q["subtopic"], "pyq_count": 0,
                            "recent3_count": 0, "per_year": {}})
        e["pyq_count"] += 1
        e["per_year"][q["exam_year"]] = e["per_year"].get(q["exam_year"], 0) + 1
        if q["exam_year"] in recent:
            e["recent3_count"] += 1
    return out


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
    check("blueprint 1.0 migrates to 1.2", bp["schema"] == BLUEPRINT_SCHEMA
          and bp["allowed_question_types"] == []
          and bp["bank_ref"] is None
          and bp["units"][0]["prose_ban_exemptions"] == [])
    _json.dump(dict(bp10, schema="notes-blueprint/0.9"), open(fp3, "w"))
    try:
        load_blueprint(fp3)
        check("unknown blueprint schema rejected", False)
    except ValueError:
        check("unknown blueprint schema rejected", True)

    # bank_ref staleness link (fix 1)
    bpath = tempfile.mktemp(suffix=".json")
    bnk = bank_new("EX"); bank_save(bnk, bpath)
    ref = {"path": bpath, "sha256": file_sha256(bpath), "questions": 0}
    check("verify_bank_ref matches", verify_bank_ref(bpath, ref)[0] is True)
    with open(bpath, "a", encoding="utf-8") as _f:
        _f.write(" ")   # mutate the bank on disk
    check("verify_bank_ref detects a stale bank",
          verify_bank_ref(bpath, ref)[0] is False)
    check("verify_bank_ref flags a missing ref",
          verify_bank_ref(bpath, None)[0] is False)
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

    # ---- v1.5 ingest base -------------------------------------------------
    # filename date parsing (the live physics name + variants + fallbacks)
    check("date: DD-Mon-YYYY",
          parse_exam_date_from_filename(
              "IIT_JAM_PHYSICS_15-Feb-2026_PYQ_Final.docx")
          == ("2026-02-15", 2026, "15-Feb-2026"))
    check("date: compact DDMonYYYY + Copy of + (1)",
          parse_exam_date_from_filename(
              "Copy of IIT_JAM_BIOTECHNOLOGY_02May2010_Sorted (1).docx")[:2]
          == ("2010-05-02", 2010))
    check("date: Mon-YYYY fallback",
          parse_exam_date_from_filename("EXAM_Feb-2019.docx")[:2]
          == ("2019-02-01", 2019))
    check("date: YYYY-only fallback",
          parse_exam_date_from_filename("EXAM_2005_sorted.docx")[1] == 2005)
    check("date: none when absent",
          parse_exam_date_from_filename("no_date_here.docx") is None)

    # answer normalisation + ground-truth matching
    check("norm MCQ", normalize_answer("MCQ", "2") == "2")
    check("norm MSQ set", normalize_answer("MSQ", "1, 3, 4") == [1, 3, 4])
    check("norm NAT float", normalize_answer("NAT", "-8") == -8.0
          and normalize_answer("NAT", "274.4") == 274.4)
    check("nat precision from stem",
          nat_precision_from_stem("... answer to 2 decimal places.") == 2
          and nat_precision_from_stem("... to the nearest integer.") == 0
          and nat_precision_from_stem("no hint") == 2)
    check("nat tolerance match",
          nat_within_tolerance(0.4149, 0.41, 2) is True
          and nat_within_tolerance(0.418, 0.41, 2) is False
          and nat_within_tolerance(None, 0.41, 2) is False)
    check("msq unordered match",
          msq_match([3, 1], [1, 3]) is True
          and msq_match("1, 3", {1, 3}) is True
          and msq_match([1, 2], [1, 3]) is False)

    # bank build/validate/counts + subtopic join + recent-window
    b = bank_new("IITJAM_PH")
    bank_add_paper(b, "k2026", "2026-02-15", 2026, "..2026..docx", 2)
    bank_add_paper(b, "k2013", "2013-02-10", 2013, "..2013..docx", 1)
    bank_add_question(b, dict(bank_id="PH-1", paper_key="k2026",
        exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
        subject="Physics", topic="Optics", subtopic="Polarization",
        stem="s1", correct_answer="2", stem_figures=["m1.png"]))
    bank_add_question(b, dict(bank_id="PH-2", paper_key="k2026",
        exam_date="2026-02-15", exam_year=2026, q_no=2, type="NAT",
        subject="Physics", topic="Optics", subtopic="Polarization",
        stem="s2", correct_answer="0.41"))
    bank_add_question(b, dict(bank_id="PH-3", paper_key="k2013",
        exam_date="2013-02-10", exam_year=2013, q_no=5, type="MSQ",
        subject="Physics", topic="Thermo", subtopic="Carnot", stem="s3",
        correct_answer="1,3"))
    check("bank validates", bank_validate(b) is True)
    check("figure flag from stem_figures",
          b["questions"][0]["figure"] is True
          and b["questions"][1]["figure"] is False)
    counts = derive_taxonomy_counts(b, latest_years=1)
    pol = counts[subtopic_key("Physics", "Optics", "Polarization")]
    car = counts[subtopic_key("Physics", "Thermo", "Carnot")]
    check("counts: subtopic pyq_count", pol["pyq_count"] == 2 and car["pyq_count"] == 1)
    check("counts: recent window = top-1 year (2026)",
          pol["recent3_count"] == 2 and car["recent3_count"] == 0)
    check("subtopic filter", len(bank_questions_for(b, "Physics", "optics",
          " Polarization ")) == 2)

    # v1.7: subtopic_key joins across syllabus-vs-header label drift (fix 3)
    def _joins(a, bb):
        return subtopic_key("S", "T", a) == subtopic_key("S", "T", bb)
    check("join: & vs and", _joins("Microbial & Plant Biotech",
                                   "Microbial and Plant Biotech"))
    check("join: en-dash vs hyphen", _joins("Enzyme Kinetics \u2013 Basics",
                                            "Enzyme Kinetics - Basics"))
    check("join: fullwidth NFKC", _joins("\uff2e\uff2d\uff32 Spectroscopy",
                                         "NMR Spectroscopy"))
    check("join: slash spacing", _joins("Optics/Polarization",
                                        "Optics / Polarization"))
    check("join: still distinguishes real differences",
          not _joins("Carnot Cycle", "Otto Cycle"))

    # v1.8: reads recompute the key, so a bank whose STORED keys are stale (as a
    # v1.6-written bank's would be) still joins correctly and counts correctly.
    b2 = bank_new("EX")
    bank_add_paper(b2, "p", "2026-02-15", 2026, "x_15-Feb-2026.docx", 2)
    bank_add_question(b2, dict(bank_id="X1", paper_key="p", exam_date="2026-02-15",
        exam_year=2026, q_no=1, type="MCQ", subject="Bio", topic="Enz",
        subtopic="Microbial & Plant Biotech", stem="a", correct_answer="1"))
    bank_add_question(b2, dict(bank_id="X2", paper_key="p", exam_date="2026-02-15",
        exam_year=2026, q_no=2, type="MCQ", subject="Bio", topic="Enz",
        subtopic="Microbial and Plant Biotech", stem="b", correct_answer="2"))
    # Simulate a stale/legacy stored key (what a weaker normaliser would have left)
    b2["questions"][0]["subtopic_key"] = "bio|||enz|||microbial & plant biotech"
    b2["questions"][1]["subtopic_key"] = "bio|||enz|||microbial and plant biotech"
    got = bank_questions_for(b2, "Bio", "Enz", "Microbial and Plant Biotech")
    check("reader ignores stale stored key (join by recompute)", len(got) == 2)
    cnts = derive_taxonomy_counts(b2)
    check("counts ignore stale stored key", len(cnts) == 1
          and list(cnts.values())[0]["pyq_count"] == 2)

    # schema acceptance + migration
    check("bank_validate accepts 1.0 and 1.1",
          bank_validate({"schema": "notes-pyq-bank/1.0", "questions": []}) is True
          and bank_validate({"schema": "notes-pyq-bank/1.1", "questions": []}) is True)
    try:
        bank_validate({"schema": "notes-pyq-bank/0.9", "questions": []})
        check("bank_validate rejects unknown schema", False)
    except ValueError:
        check("bank_validate rejects unknown schema", True)
    b2["schema"] = "notes-pyq-bank/1.0"
    b2["questions"][0]["subtopic_key"] = "STALE"
    _bp = tempfile.mktemp(suffix=".json"); bank_save(b2, _bp)
    reloaded = bank_load(_bp)
    check("bank_load migrates 1.0 -> current + refreshes stored key",
          reloaded["schema"] == PYQ_BANK_SCHEMA
          and reloaded["questions"][0]["subtopic_key"]
          == subtopic_key("Bio", "Enz", "Microbial & Plant Biotech"))
    try:
        bank_add_question(b, dict(bank_id="X", paper_key="k", exam_date="d",
            exam_year=2000, q_no=9, type="FOO", subject="s", topic="t",
            subtopic="st", stem="x"))
        check("non-canonical type rejected", False)
    except ValueError:
        check("non-canonical type rejected", True)
    try:
        bank_add_question(b, dict(bank_id="PH-1", paper_key="k2026",
            exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
            subject="Physics", topic="Optics", subtopic="Polarization", stem="d"))
        bank_validate(b)
        check("duplicate bank_id rejected", False)
    except ValueError:
        check("duplicate bank_id rejected", True)

    # ---- v2.0 taxonomy consumer ------------------------------------------
    _man = {"exam_code": "EXBT", "subtopics": {
        "gb.cell.membranes": {"display_name": "Membrane Structure and Function",
                              "section": "General Biology", "topic": "Cell"},
        "gb.cell.signalling": {"display_name": "Cell Signalling - Endocrine and "
                               "Paracrine Pathways",
                               "section": "General Biology", "topic": "Cell"},
        "gb.genetics.linkage": {"display_name": "Linkage and Mapping",
                                "section": "General Biology",
                                "topic": "Genetics"},
        "ch.bonding.vsepr": {"display_name": "VSEPR Theory",
                             "section": "Chemistry (10+2+3 level)",
                             "topic": "Bonding"}}}
    mp = tempfile.mktemp(suffix=".json")
    _json.dump(_man, open(mp, "w", encoding="utf-8"))
    check("manifest loads with matching exam_code",
          load_subtopic_manifest(mp, "EXBT")["exam_code"] == "EXBT")
    try:
        load_subtopic_manifest(mp, "OTHER_EXAM")
        check("manifest exam_code mismatch hard-stops", False)
    except ValueError as e:
        check("manifest exam_code mismatch hard-stops", "OTHER_EXAM" in str(e))
    bad = tempfile.mktemp(suffix=".json")
    _json.dump({"exam_code": "EXBT", "subtopics": {"x": {"section": "S"}}},
               open(bad, "w"))
    try:
        load_subtopic_manifest(bad)
        check("manifest entry missing fields hard-stops", False)
    except ValueError:
        check("manifest entry missing fields hard-stops", True)

    ref2 = taxonomy_ref_for(mp)
    check("taxonomy_ref_for yields sha+count",
          len(ref2["sha256"]) == 64 and ref2["subtopics"] == 4)
    check("verify_taxonomy_ref matches", verify_taxonomy_ref(mp, ref2)[0] is True)
    with open(mp, "a", encoding="utf-8") as _f:
        _f.write(" ")
    check("verify_taxonomy_ref detects a changed manifest",
          verify_taxonomy_ref(mp, ref2)[0] is False)
    check("verify_taxonomy_ref flags a missing ref",
          verify_taxonomy_ref(mp, None)[0] is False)

    check("sid_slug takes final component",
          sid_slug("gb.cell.membranes") == "membranes"
          and sid_slug("plainslug") == "plainslug")

    num = assign_numbering(_man)
    check("numbering from manifest order",
          num["gb.cell.membranes"] == {"s_no": 1, "t_no": 1, "st_no": 1}
          and num["gb.cell.signalling"] == {"s_no": 1, "t_no": 1, "st_no": 2}
          and num["gb.genetics.linkage"] == {"s_no": 1, "t_no": 2, "st_no": 1}
          and num["ch.bonding.vsepr"] == {"s_no": 2, "t_no": 1, "st_no": 1})
    # persistence: an INSERTED subtopic must not renumber existing units, and a
    # sid removed from the manifest keeps its number (caller's ORPHANED report)
    _man2 = {"exam_code": "EXBT", "subtopics": {}}
    _man2["subtopics"]["gb.cell.transport"] = {
        "display_name": "Membrane Transport", "section": "General Biology",
        "topic": "Cell"}                       # inserted FIRST in row order
    for k, v in _man["subtopics"].items():
        if k != "gb.genetics.linkage":         # linkage removed upstream
            _man2["subtopics"][k] = v
    num2 = assign_numbering(_man2, prior=num)
    check("prior numbering preserved verbatim",
          all(num2[k] == num[k] for k in num))
    check("inserted sid appends, never renumbers",
          num2["gb.cell.transport"] == {"s_no": 1, "t_no": 1, "st_no": 3})
    check("removed sid keeps its number (orphan)",
          num2["gb.genetics.linkage"] == num["gb.genetics.linkage"])
    # collision safety under the harshest re-run: an ENTIRE prior section is
    # orphaned and a NEW section arrives. Even if the numeric s is reused, the
    # (s,t,st) TRIPLE can never collide, because st_used is seeded from EVERY
    # prior assignment (unconditionally), so new STs continue after orphans.
    _man3 = {"exam_code": "EXBT", "subtopics": {
        k: v for k, v in _man["subtopics"].items() if not k.startswith("ch.")}}
    _man3["subtopics"]["ph.mech.kinematics"] = {
        "display_name": "Kinematics", "section": "Physics", "topic": "Mechanics"}
    num3 = assign_numbering(_man3, prior=num)
    trips = [(v["s_no"], v["t_no"], v["st_no"]) for v in num3.values()]
    check("orphaned-section re-run: all (s,t,st) triples unique",
          len(trips) == len(set(trips)))
    check("orphaned section keeps numbers; new section STs never collide",
          num3["ch.bonding.vsepr"] == num["ch.bonding.vsepr"]
          and num3["ph.mech.kinematics"]["st_no"]
          > num["ch.bonding.vsepr"]["st_no"] - 1)

    units_ix = {sid: dict(_man["subtopics"][sid],
                          name=_man["subtopics"][sid]["display_name"])
                for sid in _man["subtopics"]}
    r = resolve_unit(units_ix, "gb.cell.membranes")
    check("resolve: exact sid", r["status"] == "ok" and r["via"] == "sid")
    r = resolve_unit(units_ix, "General Biology::Cell::Membrane Structure and Function")
    check("resolve: 3-part scope", r["status"] == "ok"
          and r["sid"] == "gb.cell.membranes")
    r = resolve_unit(units_ix, "membrane structure & function")
    check("resolve: bare name, norm (& vs and, case)",
          r["status"] == "ok" and r["sid"] == "gb.cell.membranes")
    r = resolve_unit(units_ix,
                     "Cell Signalling \u2013 Endocrine and Paracrine Pathways")
    check("resolve: bare name, en-dash vs hyphen",
          r["status"] == "ok" and r["sid"] == "gb.cell.signalling")
    dup = dict(units_ix)
    dup["ch.misc.linkage"] = {"display_name": "Linkage and Mapping",
                              "section": "Chemistry (10+2+3 level)",
                              "topic": "Misc", "name": "Linkage and Mapping"}
    r = resolve_unit(dup, "Linkage and Mapping")
    check("resolve: duplicate bare name -> ambiguous with both candidates",
          r["status"] == "ambiguous" and sorted(r["matches"])
          == ["ch.misc.linkage", "gb.genetics.linkage"])
    r = resolve_unit(dup, "Chemistry (10+2+3 level)::Misc::Linkage and Mapping")
    check("resolve: scope disambiguates the duplicate",
          r["status"] == "ok" and r["sid"] == "ch.misc.linkage")
    r = resolve_unit(units_ix, "Membrane")
    check("resolve: typo/partial -> none with suggestions, never auto-picked",
          r["status"] == "none" and "gb.cell.membranes" in r["suggestions"])
    r = resolve_unit(units_ix, "Cell::Membrane Structure and Function")
    check("resolve: 2-part scope refused with guidance",
          r["status"] == "none" and "3 parts" in r["detail"])

    # registry v2: sid keying + taxonomy_ref carried + 1.x load unaffected
    reg2 = registry_init("EXBT", "h", "G", [
        {"sid": "gb.cell.membranes", "unit_code": "EXBT_S1_T1_ST01",
         "name": "Membrane Structure and Function", "section": "General Biology",
         "topic": "Cell", "slug": "membranes", "role": "PYQ_WEIGHTED",
         "tier": "TIER-2", "pyq_count": 5}], taxonomy_ref=ref2)
    check("registry v2 keys by sid and carries taxonomy_ref",
          "gb.cell.membranes" in reg2["units"]
          and reg2["units"]["gb.cell.membranes"]["unit_code"] == "EXBT_S1_T1_ST01"
          and reg2["taxonomy_ref"]["sha256"] == ref2["sha256"])
    check("1.x registry load gains v2 defaults",
          reg["units"]["U"]["sid"] is None
          and reg["units"]["U"]["unit_code"] == "U")
    check("blueprint 1.0 migrate gains taxonomy_ref default",
          bp["taxonomy_ref"] is None and bp["units"][0]["sid"] is None)

    # ---- v2.1 SPEC-LOCK (defect-class tripwire) --------------------------
    # FORWARD half: every literal a Framework_Notes* spec restates in prose is
    # PINNED here to its documented value, so a moving ENGINE constant fails the
    # self-test. These pins compare the engine to a literal in this same file —
    # they say nothing about what the spec text actually reads, which is why the
    # REVERSE half below exists and is what closes the defect this was written
    # for. Neither half alone catches "one contract, two implementations".
    check("spec-lock: NC §6A level colours",
          LEVEL_COLORS == {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                           "table_header": "44546A"})
    check("spec-lock: NC §6A box colours",
          BOX_COLORS == {"example": ("2E75B6", "E8F1FA"),
                         "recall": ("2E75B6", "E8F1FA"),
                         "key_points": ("2E7D32", "E4F2E4"),
                         "trap": ("C62828", "FBE4E4")})
    check("spec-lock: NC §5 density constants",
          BULLET_TARGET_WORDS == 20 and BULLET_HARD_CAP_WORDS == 25)
    check("spec-lock: NB §5 / NC §5 tier page bands",
          TIER_PAGE_BANDS == {"TIER-1": (6, 15), "TIER-2": (4, 8),
                              "TIER-3": (2, 5)})
    check("spec-lock: schema strings as the specs cite them",
          REGISTRY_SCHEMA == "notes-registry/2.1"
          and BLUEPRINT_SCHEMA == "notes-blueprint/2.0"
          and PYQ_BANK_SCHEMA == "notes-pyq-bank/1.1")
    check("spec-lock: NB §4 / registry vocabularies",
          ROLES == ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
          and STATES == ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
          and TIERS == ("TIER-1", "TIER-2", "TIER-3")
          and CANONICAL_TYPES == ("MCQ", "MSQ", "NAT"))
    check("spec-lock: NB §1A A-3 unit_code format",
          unit_code("EX", 1, 2, 3) == "EX_S1_T2_ST03")
    check("spec-lock: NC F-1 filename recipe INCLUDING sanitisation "
          "(the engine is the single authority; deployment-review fixture)",
          notes_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers.docx"
          and notes_filename("EX", 1, 2, 3, "membrane_structure")
          == "EX_S1_T2_ST03_membrane_structure.docx"
          and notes_filename("EX", 1, 2, 3, sid_slug("gb.cell.membranes"))
          == "EX_S1_T2_ST03_membranes.docx")

    # ---- v2.2 SPEC-LOCK: the three filename authorities ------------------
    # All three share one stem, so sanitisation cannot drift between the
    # draft, the audited file and the delivered file.
    check("spec-lock: NA _Final filename authority",
          notes_final_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers_Final.docx")
    check("spec-lock: ND _Deliver filename authority",
          notes_deliver_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers_Deliver.docx")
    check("spec-lock: all three filenames share one sanitised stem",
          notes_filename("EX", 1, 2, 3, "a-b&c")[:-len(".docx")]
          == notes_final_filename("EX", 1, 2, 3, "a-b&c")[:-len("_Final.docx")]
          == notes_deliver_filename("EX", 1, 2, 3,
                                    "a-b&c")[:-len("_Deliver.docx")])
    check("spec-lock: the three filenames are mutually distinct",
          len({notes_filename("EX", 1, 2, 3, "x"),
               notes_final_filename("EX", 1, 2, 3, "x"),
               notes_deliver_filename("EX", 1, 2, 3, "x")}) == 3)

    # ---- v2.2: docx_ref_for / verify_docx_ref ----------------------------
    _fp = tempfile.mktemp(suffix=".docx")
    with open(_fp, "wb") as _f:
        _f.write(b"original bytes")
    _ref = docx_ref_for(_fp)
    check("docx_ref_for captures filename, sha256 and size",
          _ref["filename"] == os.path.basename(_fp)
          and len(_ref["sha256"]) == 64 and _ref["bytes"] == 14)
    check("verify_docx_ref: unmodified file verifies",
          verify_docx_ref(_fp, _ref)[0] is True)
    with open(_fp, "wb") as _f:
        _f.write(b"tampered bytes!")
    _ok, _kind, _ = verify_docx_ref(_fp, _ref)
    check("verify_docx_ref: a modified file fails as 'sha256'",
          _ok is False and _kind == "sha256")
    _ok, _kind, _ = verify_docx_ref(_fp, _ref,
                                    expected_filename="OTHER_UNIT.docx")
    check("verify_docx_ref: wrong unit attached fails as 'filename' — a "
          "DIFFERENT defect from a hand-edit, so it is reported separately",
          _ok is False and _kind == "filename")
    check("verify_docx_ref: absent ref fails as 'missing_ref'",
          verify_docx_ref(_fp, None)[1] == "missing_ref")
    check("verify_docx_ref: absent file fails as 'not_found'",
          verify_docx_ref(tempfile.mktemp(suffix=".docx"), _ref)[1]
          == "not_found")

    # ---- v2.2: registry schema forward-compatibility ---------------------
    check("registry: 2.1 is now EMITTED, and 1.x/2.0 still load",
          REGISTRY_SCHEMA == "notes-registry/2.1"
          and {"notes-registry/1.0", "notes-registry/2.0"}
          <= set(REGISTRY_SCHEMAS_ACCEPTED))
    check("registry_init emits the 2.1 per-unit fields",
          all(k in registry_init("EX", "h", "PG",
                                 [{"sid": "s", "name": "N", "role": "COVERAGE",
                                   "tier": "TIER-3",
                                   "unit_code": "EX_S1_T1_ST01"}]
                                 )["units"]["s"]
              for k in ("draft_ref", "final_ref", "audit_summary")))
    _rp = tempfile.mktemp(suffix=".json")
    _reg = registry_init("EX", "h", "PG",
                         [{"sid": "a.b.c", "name": "N", "role": "COVERAGE",
                           "tier": "TIER-3", "unit_code": "EX_S1_T1_ST01"}])
    registry_save(_reg, _rp)
    _loaded = registry_load(_rp)
    check("registry_load defaults the 2.1 per-unit fields on any schema",
          all(k in _loaded["units"]["a.b.c"]
              for k in ("draft_ref", "final_ref", "audit_summary")))
    check("registry_load leaves the 2.1 defaults empty (additive, not lossy)",
          _loaded["units"]["a.b.c"]["draft_ref"] is None
          and _loaded["units"]["a.b.c"]["audit_summary"] is None)

    # ---- SPEC-LOCK, REVERSE HALF (the drift direction that produced the bug)
    # The pins above compare the engine to a literal in THIS file, so they fire
    # only when the ENGINE moves. The defect they were written for ran the other
    # way: the engine was right and Framework_NotesCreate's prose was stale, and
    # every pin above passes verbatim against that stale text (verified). So the
    # spec text itself is read and compared, the same way explain_engine's
    # T3-DRIFT-LOCK reads Framework_PYQPrepare §S3-5b. Missing spec = loud crash,
    # never a silent pass — also as in T3-DRIFT-LOCK.
    _spec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "Framework_NotesCreate.md"), encoding="utf-8").read()
    _f1 = _spec.split("F-1 Naming:", 1)[1].split("F-2 ", 1)[0]
    check("spec-lock/reverse: NC F-1 defers to the engine and states the "
          "sanitisation (fails on the pre-v2.2.1 prose recipe)",
          "notes_core.notes_filename" in _f1
          and "non-alphanumeric" in _f1 and "sanitis" in _f1)
    _cmap = _spec.split("Colour map (constants", 1)[1].split(
        "No other colour", 1)[0]
    _engine_hex = set(LEVEL_COLORS.values())
    for _fg, _bg in BOX_COLORS.values():
        _engine_hex |= {_fg, _bg}
    check("spec-lock/reverse: NC §6A colour literals == LEVEL_COLORS/BOX_COLORS",
          set(re.findall(r"\b[0-9A-F]{6}\b", _cmap)) == _engine_hex)
    _d5 = _spec.split("D-1 Bullet length:", 1)[1].split("\n", 1)[0]
    check("spec-lock/reverse: NC §5 D-1 word counts == the engine constants",
          [int(x) for x in re.findall(r"\d+", _d5)]
          == [BULLET_TARGET_WORDS, BULLET_HARD_CAP_WORDS])

    print(f"notes_core self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_core.py — shared Notes pipeline core. Run with --self-test.")
