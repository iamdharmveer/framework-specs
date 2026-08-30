"""
notes_sync_audit.py v1.1 — CROSS-STEP SYNC AUDITOR for the Notes pipeline.

v1.1 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3). S-4's colour
    authority widens from LEVEL_COLORS/BOX_COLORS (document colours) to ALSO
    include notes_core.FIGURE_PALETTE (figure colours: Okabe-Ito hues, TEXT
    tier, fills, highlight) — NotesCreate §6 F-4a names figure hexes, and a
    hex the spec names must have an engine authority, which these now do.
    Fixture: a figure hex passes; a hex in neither map still fires.

v1.0 — 2026-08-12 — GAP-2026-08-12-NOTESYNC.

    WHY THIS EXISTS.  notes_core v2.1's SPEC-LOCK closed the "one contract, two
    implementations" defect class for Framework_NotesCreate — and said so
    plainly in its own changelog: "Coverage is deliberately narrow —
    NotesCreate only, the three literals above; NB section 5's tier bands and
    the NA/ND restatements are NOT yet spec-read and can still drift
    prose-side."  Every defect the 2026-08-12 end-to-end audit found lived in
    exactly that uncovered space: stale companion-version blocks in NC and ND,
    NB citing registry schema 2.0 while the engine it calls emitted 2.1, a G-10
    regex that failed correct documents, a density gate that counted nothing.
    Four of the five were found by a human reading files, which is not a
    control — it does not run in CI, it does not run on the next patch, and it
    does not run at 2 a.m. six months from now.

    This module turns that reading into a REPRODUCIBLE GATE.  It holds no
    opinions of its own: every check compares one authority against another
    (spec prose vs engine constant, spec vs spec, spec vs routes.json) and
    reports where they disagree.  It is deliberately NOT routed to any trigger
    — like validate_framework_md.py and audit_seam.py it is a repo-level
    auditor, run by CI and by the owner:

        python3 notes_sync_audit.py            # human report, exit 1 on FAIL
        python3 notes_sync_audit.py --json     # machine-readable
        python3 notes_sync_audit.py --self-test

    WHAT IT CANNOT DO, stated so nobody over-trusts it: it checks AGREEMENT
    between artifacts, not correctness of what they agree on.  Four specs and
    an engine can be unanimously wrong about pedagogy, exam scope or whether a
    gate is worth having, and every check here will pass.  It catches drift.
    It does not catch a bad idea implemented consistently.

CHECKS
    S-1  Every notes_*.<symbol> a spec names exists in that engine.
    S-2  Gate identifiers in the NA spec and notes_audit.GATES agree.
    S-3  Every schema string an engine EMITS is cited by a spec, and every
         schema a spec cites is known to an engine.
    S-4  Engine constants restated in spec prose match the engine (extends the
         notes_core SPEC-LOCK reverse half from NC alone to all four specs).
    S-5  MINIMUM COMPANION VERSIONS name every engine the spec calls, and
         claim a version no higher than the engine actually is.
    S-6  Cross-step handshake: every artifact a step declares as an output is
         declared as an input by the step that consumes it.
    S-7  Vocabularies (states, verdicts, tiers, roles, question types) used in
         spec prose are members of the engine's vocabulary.
    S-8  Filename recipes are not re-spelled in prose except where the spec
         explicitly defers to the engine authority.
    S-9  Routing parity: engines a Notes spec calls are routed to its trigger,
         and engines routed to the trigger are named by the spec.
"""
import importlib
import json
import os
import re
import sys

SPECS = {"NB": "Framework_NotesBlueprint.md",
         "NC": "Framework_NotesCreate.md",
         "NA": "Framework_NotesAudit.md",
         "ND": "Framework_NotesDeliver.md"}
TRIGGERS = {"NB": "NotesBlueprint", "NC": "NotesCreate",
            "NA": "NotesAudit", "ND": "NotesDeliver"}
ENGINE_NAMES = ("notes_core", "notes_docx", "notes_audit", "notes_blueprint")

# "notes_blueprint.json" is an ARTIFACT, not a call to notes_blueprint.py.
# Without this the auditor reports every spec that names the blueprint file as
# calling an engine it does not call — a false positive that would train the
# reader to ignore the report, which is the worst thing an auditor can do.
NON_SYMBOL_SUFFIXES = {"py", "json", "md", "docx", "xlsx", "pdf"}
_SYMREF = re.compile(r"\b(notes_core|notes_docx|notes_audit|notes_blueprint)"
                     r"\.([a-zA-Z_][a-zA-Z0-9_]*)\b")


def _symbol_refs(s):
    """(module, symbol) pairs a spec genuinely references."""
    for m in _SYMREF.finditer(s):
        if m.group(2) not in NON_SYMBOL_SUFFIXES:
            yield m.group(1), m.group(2)

# Artifacts that move between steps. producer -> consumers.
# This table is the auditor's ONLY hand-maintained input; S-6 checks the specs
# against it in both directions, so an artifact added to the pipeline without
# updating both ends fails here.
HANDSHAKE = [
    ("notes_pyq_bank.json", "NB", ("NC", "NA")),
    ("notes_blueprint.json", "NB", ("NC", "NA")),
    ("notes_registry.json", "NB", ("NC", "NA", "ND")),
    ("draft_ref", "NC", ("NA",)),
    ("final_ref", "NA", ("ND",)),
    ("audit_summary", "NA", ("ND",)),
    ("taxonomy_ref", "NB", ("NC", "NA")),
    ("bank_ref", "NB", ("NC", "NA")),
]


_load_seq = [0]


def _load(root):
    """Load the engines FROM THE GIVEN ROOT, bypassing the import cache.

    importlib.import_module returns whatever is already in sys.modules, so
    auditing a second repository in the same process silently re-used the
    FIRST repository's engines — the audit would report on files it never
    read. It made every engine-side change invisible, which is exactly the
    failure this module exists to catch, in this module. Each call now loads
    under a unique synthetic package name from an explicit file path.

    MEASURED, not assumed: reverting this function wholesale to the original
    (import_module with no cache eviction) IS caught by the self-test's
    engine-side fixtures. Removing any ONE of the three mechanisms — the
    explicit file-path loader, the cache eviction, or root-at-the-front of
    sys.path — is NOT caught, because each is independently sufficient to
    load the right file. That redundancy is deliberate and is recorded here
    so a later reader does not delete two of them on the evidence that
    deleting one changed nothing.
    """
    import importlib.util
    _load_seq[0] += 1
    tag = f"_nsa{_load_seq[0]}_"
    root = os.path.abspath(root)
    saved_path = list(sys.path)
    saved_mods = {n: sys.modules.get(n) for n in ENGINE_NAMES}
    sys.path.insert(0, root)
    try:
        for n in ENGINE_NAMES:
            sys.modules.pop(n, None)
        mods = {}
        for n in ENGINE_NAMES:
            spec = importlib.util.spec_from_file_location(
                tag + n, os.path.join(root, n + ".py"))
            mod = importlib.util.module_from_spec(spec)
            sys.modules[tag + n] = mod
            sys.modules[n] = mod          # so siblings resolve to THIS copy
            spec.loader.exec_module(mod)
            mods[n] = mod
        return mods
    finally:
        sys.path[:] = saved_path
        for n, old_mod in saved_mods.items():
            if old_mod is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = old_mod


def _read(root, name):
    with open(os.path.join(root, name), encoding="utf-8") as f:
        return f.read()


def _ver_tuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def audit(root="."):
    """Run every check. Returns (ok, findings, stats)."""
    findings = []
    stats = {}

    def fail(check, msg):
        findings.append({"check": check, "detail": msg})

    mods = _load(os.path.abspath(root))
    text = {k: _read(root, f) for k, f in SPECS.items()}
    joined = "\n".join(text.values())
    nc_, nd_, na_, nb_ = (mods["notes_core"], mods["notes_docx"],
                          mods["notes_audit"], mods["notes_blueprint"])

    # ---- S-1 spec -> engine symbol resolution ---------------------------
    n = 0
    for k, s in text.items():
        for mod, fn in _symbol_refs(s):
            n += 1
            if not hasattr(mods[mod], fn):
                fail("S-1", f"{k} names {mod}.{fn}, which does not exist "
                            f"in the engine")
    stats["S-1_symbols_checked"] = n

    # ---- S-2 gate identifiers -------------------------------------------
    # [a-z]? not [ab]? — G-2c exists, and a regex that cannot express the
    # identifier it is auditing reports the gate as undocumented.
    spec_gates = set(re.findall(r"\bG-\d+[a-z]?\b", text["NA"]))
    eng_gates = set(na_.GATES)
    # "G-2" is the umbrella the spec uses for G-2a/b/c; accept it iff all three
    # sub-gates exist in the engine.
    umbrella = {"G-2"} if {"G-2a", "G-2b", "G-2c"} <= eng_gates else set()
    for g in sorted(spec_gates - eng_gates - umbrella):
        fail("S-2", f"NA spec names gate {g} but notes_audit.GATES does not "
                    f"list it — the engine's gate registry is the authority "
                    f"for what a report can contain")
    for g in sorted(eng_gates - spec_gates):
        fail("S-2", f"notes_audit.GATES lists {g} but the NA spec never "
                    f"describes it — a gate nobody specified")
    stats["S-2_gates"] = len(eng_gates)

    # ---- S-3 schema citations -------------------------------------------
    emitted = {nc_.REGISTRY_SCHEMA, nc_.BLUEPRINT_SCHEMA, nc_.PYQ_BANK_SCHEMA,
               nd_.SCHEMA, na_.REPORT_SCHEMA}
    known = (set(nc_.REGISTRY_SCHEMAS_ACCEPTED)
             | set(nc_.BLUEPRINT_SCHEMAS_ACCEPTED)
             | set(nc_.PYQ_BANK_SCHEMAS_ACCEPTED)
             | set(nd_.MODEL_SCHEMAS_ACCEPTED) | emitted)
    cited = set(re.findall(r"notes-[a-z\-]+/\d+\.\d+", joined))
    for sch in sorted(cited - known):
        fail("S-3", f"specs cite schema {sch!r}, which no engine accepts or "
                    f"emits")
    for sch in sorted(emitted - cited):
        fail("S-3", f"an engine EMITS schema {sch!r} but no Notes spec cites "
                    f"it — a version bump would be invisible spec-side")
    stats["S-3_schemas_emitted"] = len(emitted)

    # ---- S-4 constants restated in prose --------------------------------
    # Extends the notes_core SPEC-LOCK reverse half (NC only) to all four.
    checked = 0
    for tier, (lo, hi) in nc_.TIER_PAGE_BANDS.items():
        for k, s in text.items():
            for m in re.finditer(re.escape(tier)
                                 + r"[^\n]*?(\d+)\s*[-\u2013]\s*(\d+)\s*"
                                   r"(?:pp\b|pages\b)", s):
                checked += 1
                if (int(m.group(1)), int(m.group(2))) != (lo, hi):
                    fail("S-4", f"{k} states {tier} page band "
                                f"{m.group(1)}-{m.group(2)} but "
                                f"notes_core.TIER_PAGE_BANDS says {lo}-{hi}")
    for k, s in text.items():
        for m in re.finditer(r"HARD CAP\s+(\d+)", s):
            checked += 1
            if int(m.group(1)) != nc_.BULLET_HARD_CAP_WORDS:
                fail("S-4", f"{k} states bullet HARD CAP {m.group(1)} but "
                            f"notes_core.BULLET_HARD_CAP_WORDS is "
                            f"{nc_.BULLET_HARD_CAP_WORDS}")
    engine_hex = set(nc_.LEVEL_COLORS.values())
    for fg, bg in nc_.BOX_COLORS.values():
        engine_hex |= {fg, bg}
    # v1.1 — figure colours (NC §6 F-4a) have their own engine authority.
    fp = getattr(nc_, "FIGURE_PALETTE", {}) or {}
    for hx in (list(fp.get("okabe_ito", ())) + list(fp.get("fills", ()))
               + list(fp.get("text_tier", {}).values()) + [fp.get("highlight", "")]):
        if isinstance(hx, str) and hx.startswith("#") and len(hx) == 7:
            engine_hex.add(hx[1:].upper())
    for k, s in text.items():
        for hexv in set(re.findall(r"\b[0-9A-F]{6}\b", s)):
            checked += 1
            if hexv not in engine_hex:
                fail("S-4", f"{k} names colour {hexv} which is not in "
                            f"notes_core.LEVEL_COLORS/BOX_COLORS")
    for k, s in text.items():
        for m in re.finditer(r"MAX_PATCHES_PER_QUESTION \((\d+)\)", s):
            checked += 1
            if int(m.group(1)) != na_.MAX_PATCHES_PER_QUESTION:
                fail("S-4", f"{k} states MAX_PATCHES_PER_QUESTION "
                            f"{m.group(1)}, engine says "
                            f"{na_.MAX_PATCHES_PER_QUESTION}")
        for m in re.finditer(r"MAX_REGENERATIONS \((\d+)\)", s):
            checked += 1
            if int(m.group(1)) != na_.MAX_REGENERATIONS:
                fail("S-4", f"{k} states MAX_REGENERATIONS {m.group(1)}, "
                            f"engine says {na_.MAX_REGENERATIONS}")
    stats["S-4_constants_checked"] = checked

    # ---- S-5 companion version claims -----------------------------------
    actual = {}
    for n_ in ENGINE_NAMES:
        head = (getattr(mods[n_], "__doc__") or "").strip().splitlines()[0]
        m = re.search(r"v(\d+(?:\.\d+)*)", head)
        actual[n_ + ".py"] = m.group(1) if m else None
    for k, s in text.items():
        blk = re.search(r"MINIMUM COMPANION VERSIONS:(.*?)"
                        r"(?:\n#\s*\n|\n# PURPOSE)", s, re.S)
        if not blk:
            fail("S-5", f"{k} has no MINIMUM COMPANION VERSIONS block")
            continue
        claims = {m.group(1): m.group(2)
                  for m in re.finditer(r"(notes_\w+\.py)\s*>=\s*v?"
                                       r"([\d.]+)", blk.group(1))}
        called = {mod + ".py" for mod, _ in _symbol_refs(s)}
        for eng in sorted(called - set(claims)):
            fail("S-5", f"{k} calls {eng} but does not name it in MINIMUM "
                        f"COMPANION VERSIONS")
        for eng, want in claims.items():
            if actual.get(eng) is None:
                continue
            if _ver_tuple(want) > _ver_tuple(actual[eng]):
                fail("S-5", f"{k} requires {eng} >= v{want} but the engine "
                            f"is only v{actual[eng]}")
    stats["S-5_engines"] = len(actual)

    # ---- S-6 cross-step handshake ---------------------------------------
    for artifact, producer, consumers in HANDSHAKE:
        if artifact not in text[producer]:
            fail("S-6", f"{producer} is the producer of {artifact!r} but "
                        f"never names it")
        for c in consumers:
            if artifact not in text[c]:
                fail("S-6", f"{c} consumes {artifact!r} (produced by "
                            f"{producer}) but never names it")
    stats["S-6_artifacts"] = len(HANDSHAKE)

    # ---- S-7 vocabularies ------------------------------------------------
    vocab = {"state": set(nc_.STATES), "verdict": set(na_.VERDICTS),
             "tier": set(nc_.TIERS), "role": set(nc_.ROLES),
             "qtype": set(nc_.CANONICAL_TYPES)}
    # Engine CONSTANT names (PYQ_BANK_SCHEMA, LEVEL_COLORS, ...) share prefixes
    # with vocabulary members and must not be mistaken for them.
    engine_attrs = set()
    for mod in mods.values():
        engine_attrs |= {a for a in dir(mod) if a.isupper()}
    for k, s in text.items():
        for tok in set(re.findall(r"\b[A-Z][A-Z_]{4,}\b", s)):
            if tok in engine_attrs:
                continue
            for kind, allowed in vocab.items():
                near = {v for v in allowed
                        if v.split("_")[0] == tok.split("_")[0]}
                if near and tok not in allowed and "_" in tok:
                    fail("S-7", f"{k} uses {tok!r}, which looks like a "
                                f"{kind} but is not one of {sorted(near)}")
    stats["S-7_vocabularies"] = len(vocab)

    # ---- S-8 filename recipes not re-spelled ----------------------------
    for k, s in text.items():
        for m in re.finditer(r"\{EXAM\}_S\{s\}_T\{t\}_ST\{nn\}[^\s]*", s):
            window = s[max(0, m.start() - 400):m.end() + 400]
            # Deferral is shown by naming the engine authority anywhere in
            # the window, or by flagging the text as a human rendering /
            # derived attribute rather than a recipe.
            if not re.search(r"single authority|the ENGINE is|human rendering"
                             r"|DERIVED PRESENTATION|notes_core\.\w+",
                             window):
                fail("S-8", f"{k} spells the filename pattern at offset "
                            f"{m.start()} without deferring to the engine "
                            f"authority")
    stats["S-8"] = "checked"

    # ---- S-9 routing parity ----------------------------------------------
    routes = json.load(open(os.path.join(root, "routes.json"),
                            encoding="utf-8"))
    for k, trig in TRIGGERS.items():
        routed = {r for r in routes.get(trig, []) if r.endswith(".py")}
        called = {mod + ".py" for mod, _ in _symbol_refs(text[k])}
        for eng in sorted(called - routed):
            fail("S-9", f"{k} calls {eng} but it is not routed to "
                        f"trigger {trig}")
    stats["S-9_triggers"] = len(TRIGGERS)

    return (not findings, findings, stats)


def report(root=".", as_json=False):
    ok, findings, stats = audit(root)
    if as_json:
        print(json.dumps({"ok": ok, "findings": findings, "stats": stats},
                         indent=2))
        return ok
    print("=" * 62)
    print("NOTES CROSS-STEP SYNC AUDIT — 4 specs vs 4 engines")
    print("=" * 62)
    for k, v in stats.items():
        print(f"  {k:28} {v}")
    print("-" * 62)
    if ok:
        print("RESULT: OK — 0 findings. Specs and engines agree.")
    else:
        by = {}
        for f in findings:
            by.setdefault(f["check"], []).append(f["detail"])
        for c in sorted(by):
            print(f"  [{c}] {len(by[c])} finding(s):")
            for d in by[c]:
                print(f"      - {d}")
        print("-" * 62)
        print(f"RESULT: {len(findings)} FINDING(S).")
    return ok


def self_test():
    """Fixtures that MUTATE a spec copy and assert the auditor notices.

    An auditor whose own tests only prove it passes a clean repo proves
    nothing: it would still pass if every check were `return True`. Each
    fixture below breaks exactly one contract and asserts the matching check
    fires.
    """
    import shutil
    import tempfile
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    root = os.path.dirname(os.path.abspath(__file__))
    ok, findings, stats = audit(root)
    check("the live repo passes the sync audit", ok)
    if not ok:
        for f in findings:
            fails.append(f"live finding [{f['check']}] {f['detail'][:70]}")

    def mutated(spec_key, old, new, count=1):
        """Break exactly one contract in a COPY of the repo and re-audit.

        count=0 replaces EVERY occurrence. That matters for S-6: an artifact
        named three times in a spec is not removed by replacing the first
        mention, and a fixture that leaves the contract intact passes for the
        wrong reason — it proves the mutation was too weak, not that the check
        works.
        """
        d = tempfile.mkdtemp()
        for f in os.listdir(root):
            if f.endswith((".py", ".md", ".json")):
                shutil.copy(os.path.join(root, f), d)
        p = os.path.join(d, SPECS[spec_key])
        s = open(p, encoding="utf-8").read()
        assert old in s, f"anchor not found: {old[:40]}"
        s = s.replace(old, new) if count == 0 else s.replace(old, new, count)
        open(p, "w", encoding="utf-8").write(s)
        return audit(d)

    def mutated_engine(engine, old, new, count=0):
        """Break a contract on the ENGINE side instead of the spec side.

        S-2 and S-3 are two-directional (spec names something the engine lacks,
        AND engine has something no spec names). Spec-side fixtures alone
        exercise one branch each, so disabling the other branch survived —
        which is precisely the "test that cannot fail" this auditor exists to
        prevent, found in the auditor itself.
        """
        d = tempfile.mkdtemp()
        for f in os.listdir(root):
            if f.endswith((".py", ".md", ".json")):
                shutil.copy(os.path.join(root, f), d)
        p = os.path.join(d, engine)
        s = open(p, encoding="utf-8").read()
        assert old in s, f"anchor not found: {old[:40]}"
        s = s.replace(old, new) if count == 0 else s.replace(old, new, count)
        open(p, "w", encoding="utf-8").write(s)
        return audit(d)

    def fires(check_id, res, contains=None):
        """A fixture must pin the BRANCH, not just the check id.

        S-2, S-3, S-5 and S-6 each have two directions. Asserting only
        `check == "S-3"` passes when either branch fires, so disabling one of
        them still looked tested. `contains` pins which sentence was emitted.
        """
        return any(f["check"] == check_id
                   and (contains is None or contains in f["detail"])
                   for f in res[1])

    check("S-1 fires on a spec naming a non-existent engine symbol",
          fires("S-1", mutated("NA", "notes_audit.terminal_regate",
                               "notes_audit.terminal_regate_typo")))
    check("S-4 fires on a drifted bullet HARD CAP in prose",
          fires("S-4", mutated("NC", "HARD CAP 25", "HARD CAP 40")))
    check("S-4 fires on a colour that is not in the engine map",
          fires("S-4", mutated("NC", "1F4E79", "1F4E7A")))
    # v1.1 — a FIGURE hex (F-4a) is authorised by FIGURE_PALETTE; a hex in
    # neither map still fires even inside the F-4a clause.
    check("S-4 accepts a figure-palette hex named by NC §6 F-4a",
          not fires("S-4", mutated("NC", "C25604", "C25604"), contains="C25604"))
    check("S-4 still fires on a figure hex outside FIGURE_PALETTE",
          fires("S-4", mutated("NC", "C25604", "C25605"), contains="C25605"))
    check("S-5 fires on a companion version higher than the engine",
          fires("S-5", mutated("NA", "notes_core.py  >= v2.10",
                               "notes_core.py  >= v9.9")))
    check("S-6 fires when a consumer stops naming a handed-over artifact",
          fires("S-6", mutated("ND", "final_ref", "REMOVED_REF", count=0)))
    check("S-2 fires when the NA spec stops describing a registered gate",
          fires("S-2", mutated("NA", "G-7b", "G-7z", count=0)))
    check("S-3 fires when a cited schema is unknown to every engine",
          fires("S-3", mutated("NA", "notes-registry/2.1",
                               "notes-registry/9.9", count=0)))
    check("S-9 fires when a spec calls an engine not routed to its trigger",
          fires("S-9", mutated("ND", "notes_core.notes_deliver_filename",
                               "notes_blueprint.verify_manifest", count=0)))
    check("S-2 fires the OTHER way: a gate the spec names is missing from "
          "notes_audit.GATES",
          fires("S-2", mutated_engine(
              "notes_audit.py",
              '"G-7a", "G-7b", "G-8", "G-9", "G-10", "G-11", "G-12", "G-13")',
              '"G-7a", "G-8", "G-9", "G-10", "G-11", "G-12", "G-13")',
              count=1)))
    check("S-3 fires the OTHER way: an engine emits a schema no spec cites",
          fires("S-3", mutated_engine(
              "notes_audit.py",
              'REPORT_SCHEMA = "notes-audit-report/2.0"   # v2.0',
              'REPORT_SCHEMA = "notes-audit-report/7.7"   # v2.0', count=1)))
    check("S-2 fires the OTHER way: notes_audit.GATES lists a gate no spec "
          "describes",
          fires("S-2", mutated_engine(
              "notes_audit.py", '"G-12", "G-13")',
              '"G-12", "G-13", "G-99")',
              count=1), contains="never describes"))
    check("S-3 fires on an EMITTED schema that no spec cites",
          fires("S-3", mutated_engine(
              "notes_audit.py",
              'REPORT_SCHEMA = "notes-audit-report/2.0"   # v2.0',
              'REPORT_SCHEMA = "notes-audit-report/7.7"   # v2.0', count=1),
              contains="EMITS schema"))
    check("S-5 fires when a spec calls an engine its companion block omits",
          fires("S-5", mutated("ND", "notes_core.notes_deliver_filename",
                               "notes_blueprint.verify_manifest", count=0),
                contains="does not name it"))
    check("S-6 fires when the PRODUCER stops naming its own artifact",
          fires("S-6", mutated("NB", "taxonomy_ref", "tref", count=0),
                contains="is the producer"))
    check("the import cache cannot leak one repo's engines into another "
          "audit (the auditor's own defect: import_module returns whatever "
          "is already loaded)",
          fires("S-2", mutated_engine(
              "notes_audit.py", '"G-12", "G-13")',
              '"G-12", "G-13", "G-98")',
              count=1), contains="G-98"))
    check("a clean copy of the repo still passes (no false positive from the "
          "harness itself)", mutated("NA", "G-7b", "G-7b")[0])

    print(f"notes_sync_audit self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    sys.exit(0 if report(os.path.dirname(os.path.abspath(__file__)) or ".",
                         as_json="--json" in sys.argv) else 1)
