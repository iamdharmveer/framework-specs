#!/usr/bin/env python3
"""
spec_source.py — PROJECT-FIRST SPEC RESOLUTION (2026.08.03.8)

THE RULE, set by the framework owner:
    If a Framework_*.md spec is present in the exam project's Files section
    (/mnt/project), THAT copy is used. GitHub is consulted ONLY for specs the
    project does not carry.

Precedence is PER FILE, not per route: a project may override one spec and
inherit the rest.

WHAT THIS COSTS, STATED HERE BECAUSE IT MUST NOT BE DISCOVERED LATER
-------------------------------------------------------------------
bootstrap.py's guarantee — present + sha256 byte-exact + version header +
END-sentinel + exact line count, hard-stopping on any failure — rests entirely
on MANIFEST.json, which is generated from the repo and describes the repo. A
spec sitting in a project's Files section has no manifest entry, so there is
NOTHING to compare it against. Byte-integrity verification is therefore
IMPOSSIBLE for project-sourced specs, not merely skipped.

Generating a manifest from the project copies does not recover it: a manifest
built by hashing the same files it certifies verifies them against themselves
and reports VERIFIED for any content whatsoever.

So this module does not pretend. It splits the corpus into two provenance
classes and is loud about which is which:

    REPO-VERIFIED     — full bootstrap.py guarantee, unchanged.
    PROJECT-UNVERIFIED — integrity UNKNOWN. Only self-consistency checks are
                         possible (below), and passing them proves the file is
                         well-formed, NEVER that it is correct or current.

WHAT IS STILL CHECKED ON A PROJECT SPEC (self-consistency only)
---------------------------------------------------------------
  P1 non-empty and UTF-8 decodable
  P2 first line is a version header of the form '# Framework_<Name> v<ver>'
  P3 the header name matches the filename (Framework_X.md declares Framework_X)
  P4 an END-sentinel for THIS spec exists somewhere in the file, IF the repo copy
     of the same spec has one (truncation is the failure mode a project upload
     most plausibly has). The convention is CALIBRATED against the repo rather
     than assumed: measured across the live corpus, only 16 of 20 specs end ON
     their sentinel (Framework_MockTestCreate.md carries 78 further non-blank
     lines of appendix after it), and Framework_DeliveryFooter.md has no sentinel
     at all. A hardcoded "sentinel must be the last line" rule would reject four
     genuine specs, so it is not used.
  P5 header version and END-sentinel version agree, when the sentinel carries one
Failing any of P1-P5 is a HARD STOP for that spec — a malformed override is
worse than no override, because the run would half-apply it.

WHAT CANNOT BE CHECKED, EVER, FOR A PROJECT SPEC
------------------------------------------------
  - that it is not stale (an old spec is perfectly well-formed)
  - that it agrees with the repo engines it drives (routes.json pins spec and
    engine together; an overridden spec breaks that pin)
  - that it has not been edited, truncated mid-file but re-sentinelled, or
    tampered with
  - that its cross-spec references resolve (RA-*/MANDATE anchors, §-refs)

ENGINES ARE NEVER TAKEN FROM THE PROJECT
-----------------------------------------
Only .md SPECS participate. Every .py engine still comes from the verified
clone, and /mnt/project is still never placed on sys.path (CLAUDE.md). This is
deliberate: engines are imported, so a project engine copy would need a path
change that the corpus forbids and that grep-verifies as absent.

ROUTES COME FROM THE REPO
--------------------------
routes.json is repo-sourced, so ONLY specs named in a route are ever loaded. A
project holding a spec for a RETIRED step (e.g. Framework_MockTestCreateAudit.md,
deleted in 2026.08.03.5) has no trigger pointing at it and is never loaded. It is
reported as ORPHAN so it can be cleaned up, not silently executed.

USAGE
    python3 spec_source.py --resolve            # build overlay, print provenance
    python3 spec_source.py --resolve --trigger PYQScan
    python3 spec_source.py --self-test
"""
import argparse, hashlib, json, os, re, shutil, sys

PROJECT_DIR = "/mnt/project"
OVERLAY_DIR = "/tmp/fw_effective"
PROVENANCE_FILE = ".spec_provenance.json"
SPEC_RE = re.compile(r"^Framework_[A-Za-z0-9_]+\.md$")
HEADER_RE = re.compile(r"^#\s*(Framework_[A-Za-z0-9_]+)\s+v([0-9][0-9A-Za-z._-]*)")
SENTINEL_RE = re.compile(r"(?:END OF|End of)\s+(Framework_[A-Za-z0-9_]+)"
                         r"(?:\.md)?\s*\(?v?([0-9][0-9A-Za-z._-]*)?")


class SpecDefect(Exception):
    """A project-sourced spec failed a self-consistency check (P1-P5)."""


def _read(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    if not raw.strip():
        raise SpecDefect("P1 file is empty")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SpecDefect("P1 not valid UTF-8: %s" % exc)


def _has_sentinel(text, name):
    """Return the sentinel version for `name` if a sentinel is present, else None."""
    for ln in reversed([l.rstrip() for l in text.split("\n") if l.strip()]):
        m = SENTINEL_RE.search(ln)
        if m and m.group(1) == name:
            return m.group(2) or ""
    return None


def check_project_spec(path, text=None, repo_dir=None):
    """Run P1-P5 on a project-sourced spec. Returns (name, header_ver).

    Raises SpecDefect on any failure. Passing proves WELL-FORMEDNESS ONLY —
    never correctness, never currency, never agreement with the engines.

    `repo_dir` calibrates P4: the sentinel is required only when the repo copy of
    the same spec carries one. Without it, P4 requires a sentinel whenever the
    file contains the string at all (best effort) and is otherwise skipped.
    """
    text = _read(path) if text is None else text
    lines = text.split("\n")
    fname = os.path.basename(path)

    m = HEADER_RE.match(lines[0].strip())
    if not m:
        raise SpecDefect("P2 first line is not a '# Framework_<Name> v<ver>' header: "
                         "%r" % lines[0][:80])
    name, hver = m.group(1), m.group(2)

    if fname != name + ".md":
        raise SpecDefect("P3 header declares %s but the file is named %s — a renamed or "
                         "mis-saved spec would be loaded for the wrong step" % (name, fname))

    nonblank = [ln.rstrip() for ln in lines if ln.strip()]
    if not nonblank:
        raise SpecDefect("P1 file has no non-blank lines")

    sver = _has_sentinel(text, name)

    # Does the repo convention for THIS spec include a sentinel?
    repo_expects = None
    if repo_dir:
        rp = os.path.join(repo_dir, fname)
        if os.path.exists(rp):
            repo_expects = _has_sentinel(_read(rp), name) is not None

    if sver is None:
        # A sentinel naming ANOTHER spec is always wrong: it means the file was
        # assembled from the wrong source, whatever the repo convention is.
        for ln in reversed(nonblank[-40:]):
            m2 = SENTINEL_RE.search(ln)
            if m2 and m2.group(1) != name:
                raise SpecDefect("P4 END sentinel names %s but the header declares %s — "
                                 "this file was assembled from the wrong source"
                                 % (m2.group(1), name))
        if repo_expects:
            raise SpecDefect("P4 no 'END OF %s' sentinel found, but the repo copy has one "
                             "-> the upload is almost certainly TRUNCATED. Last line: %r"
                             % (name, nonblank[-1][:80]))
        if repo_expects is None:
            raise SpecDefect("P4 no 'END OF %s' sentinel found and there is no repo copy to "
                             "calibrate against — cannot rule out truncation" % name)
        return name, hver                      # repo copy has none either: conforming
    if sver and sver != hver:
        raise SpecDefect("P5 header says v%s but the END sentinel says v%s — the file is "
                         "internally inconsistent (a partial edit or a bad merge)"
                         % (hver, sver))
    return name, hver


def discover(project_dir=PROJECT_DIR):
    """Return sorted Framework_*.md basenames present in the project Files section."""
    if not os.path.isdir(project_dir):
        return []
    return sorted(f for f in os.listdir(project_dir) if SPEC_RE.match(f))


def resolve(repo_dir, project_dir=PROJECT_DIR, overlay_dir=OVERLAY_DIR, routes=None):
    """Build the effective corpus: repo clone, with project specs laid over it.

    Returns a provenance report dict. Raises SpecDefect if a project spec is
    malformed (P1-P5) — a half-applied override is worse than none.
    """
    if os.path.isdir(overlay_dir):
        shutil.rmtree(overlay_dir)
    shutil.copytree(repo_dir, overlay_dir,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", ".verified"))

    routed = set()
    if routes is None:
        rp = os.path.join(repo_dir, "routes.json")
        routes = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
    for entry in routes.values():
        routed.update(f for f in entry if f.endswith(".md"))

    overridden, orphan, repo_only = [], [], []
    for fname in discover(project_dir):
        src = os.path.join(project_dir, fname)
        name, ver = check_project_spec(src, repo_dir=repo_dir)   # raises on P1-P5 failure
        if routed and fname not in routed:
            orphan.append({"file": fname, "version": ver})
            continue                                  # never loaded: no route names it
        shutil.copyfile(src, os.path.join(overlay_dir, fname))
        entry = {"file": fname, "version": ver,
                 "sha256": hashlib.sha256(open(src, "rb").read()).hexdigest()}
        rp = os.path.join(repo_dir, fname)
        entry["repo_version"] = (_read(rp).split("\n")[0].strip()
                                 if os.path.exists(rp) else None)
        overridden.append(entry)

    ov = {e["file"] for e in overridden}
    repo_only = sorted(f for f in os.listdir(repo_dir)
                       if SPEC_RE.match(f) and f not in ov)
    rep = {"overlay_dir": overlay_dir,
           "project_unverified": overridden,
           "repo_verified": repo_only,
           "orphan_project_specs": orphan}

    # Write the provenance record INTO the overlay.
    #
    # WHY THIS EXISTS. shutil.copytree above copies bootstrap.py and MANIFEST.json into
    # the overlay alongside the overridden spec. MANIFEST.json describes the REPO, so an
    # override cannot match it by definition — and SKILL RULE 2 tells the operator to run
    # `bootstrap.py --trigger <Step>` from the overlay. Without this record bootstrap
    # reports the override as `sha256 MISMATCH` and prints "Do NOT generate anything...
    # Stop here." — a HALT, for EVERY trigger, contradicting SKILL rule 4 and
    # Framework_DeliveryFooter §2A, both of which promise a project-first run never halts.
    # The record lets bootstrap distinguish "this file was deliberately overridden" from
    # "this file is corrupt", and report the first without halting.
    #
    # It is NOT a verification bypass. bootstrap still checks each listed file against the
    # sha recorded HERE, so tampering with the overlay AFTER resolution is still caught.
    # What is impossible is checking it against the repo — there is no reference.
    #
    # ONLY .md SPECS may appear. An engine can never be excused from manifest verification.
    prov = {"schema": 1,
            "generated_by": "spec_source.py --resolve",
            "project_dir": project_dir,
            "project_unverified": [{"file": e["file"], "sha256": e["sha256"],
                                    "version": e["version"]} for e in overridden],
            "orphan_project_specs": [o["file"] for o in orphan]}
    assert all(f["file"].endswith(".md") for f in prov["project_unverified"]), \
        "provenance may only excuse .md specs — never an engine"
    with open(os.path.join(overlay_dir, PROVENANCE_FILE), "w", encoding="utf-8") as fh:
        json.dump(prov, fh, indent=2)
    rep["provenance_file"] = os.path.join(overlay_dir, PROVENANCE_FILE)
    return rep


def format_report(rep, trigger=None):
    out = []
    n = len(rep["project_unverified"])
    if n == 0:
        out.append("SPEC SOURCE: 100%% REPO-VERIFIED — no Framework_*.md in %s. "
                   "bootstrap.py's guarantee holds in full." % PROJECT_DIR)
    else:
        out.append("SPEC SOURCE: PROJECT-FIRST ACTIVE — %d spec(s) taken from the project "
                   "Files section and NOT byte-verified." % n)
        out.append("  Integrity of these files is UNKNOWN. P1-P5 well-formedness passed; "
                   "that proves the file is not truncated or malformed, NEVER that it is "
                   "correct, current, or in step with the repo engines it drives.")
        for e in rep["project_unverified"]:
            out.append("  [PROJECT-UNVERIFIED] %s %s   (repo has: %s)"
                       % (e["file"], "v" + e["version"], e["repo_version"] or "no repo copy"))
    for o in rep["orphan_project_specs"]:
        out.append("  [ORPHAN — NOT LOADED] %s: no trigger routes this spec. It is ignored. "
                   "If it belongs to a retired step, delete it from project Files." % o["file"])
    out.append("  REPO-VERIFIED specs: %d" % len(rep["repo_verified"]))
    out.append("  Engines: ALWAYS from the verified clone. /mnt/project is never on sys.path.")
    if trigger:
        out.append("  Trigger: %s" % trigger)
    return "\n".join(out)


# ── self-test (fixture-based: each check must CATCH a planted defect and PASS a clean file)
def _self_test():
    import tempfile
    passed = failed = 0

    def ok(label, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  FAIL: %s" % label)

    d = tempfile.mkdtemp()

    def write(fname, body):
        p = os.path.join(d, fname)
        open(p, "w", encoding="utf-8").write(body)
        return p

    good = ("# Framework_Demo v1.2\n# body\n\n# END OF Framework_Demo v1.2\n")
    p = write("Framework_Demo.md", good)
    try:
        name, ver = check_project_spec(p)
        ok("clean spec passes", name == "Framework_Demo" and ver == "1.2")
    except SpecDefect as e:
        ok("clean spec passes (%s)" % e, False)

    def catches(label, fname, body, needle):
        pp = write(fname, body)
        try:
            check_project_spec(pp)
            ok(label, False)
        except SpecDefect as exc:
            ok(label, needle in str(exc))

    catches("P1 catches empty", "Framework_E.md", "   \n", "P1")
    catches("P2 catches missing header", "Framework_H.md",
            "not a header\n# END OF Framework_H v1\n", "P2")
    catches("P3 catches name/filename mismatch", "Framework_Wrong.md",
            "# Framework_Other v1\n# END OF Framework_Other v1\n", "P3")
    catches("P4 catches truncation (no repo to calibrate)", "Framework_T.md",
            "# Framework_T v1\nbody with no sentinel\n", "P4")
    catches("P4 catches sentinel naming another spec", "Framework_N.md",
            "# Framework_N v1\n# END OF Framework_Z v1\n", "P4")

    # P4 is CALIBRATED, not hardcoded. Measured on the live corpus: 4 of 20 specs do
    # not end on their sentinel and one carries none at all, so both shapes must pass.
    cal = tempfile.mkdtemp()
    open(os.path.join(cal, "Framework_Tail.md"), "w", encoding="utf-8").write(
        "# Framework_Tail v1\n# END OF Framework_Tail v1\n# =====\n")
    pt = write("Framework_Tail.md", "# Framework_Tail v1\n# END OF Framework_Tail v1\n# =====\n")
    try:
        check_project_spec(pt, repo_dir=cal); ok("sentinel followed by a divider passes", True)
    except SpecDefect as e:
        ok("sentinel followed by a divider passes (%s)" % e, False)

    open(os.path.join(cal, "Framework_None.md"), "w", encoding="utf-8").write(
        "# Framework_None v1\nbody\n```\n")
    pn = write("Framework_None.md", "# Framework_None v1\nbody\n```\n")
    try:
        check_project_spec(pn, repo_dir=cal)
        ok("spec whose repo copy has no sentinel passes", True)
    except SpecDefect as e:
        ok("spec whose repo copy has no sentinel passes (%s)" % e, False)

    # ...but if the repo copy DOES carry one, its absence is truncation.
    ptr = write("Framework_Tail2.md", "# Framework_Tail v1\nbody only\n")
    os.rename(ptr, os.path.join(d, "Framework_Tail.md"))
    try:
        check_project_spec(os.path.join(d, "Framework_Tail.md"), repo_dir=cal)
        ok("missing sentinel caught when repo has one", False)
    except SpecDefect as e:
        ok("missing sentinel caught when repo has one", "P4" in str(e))
    catches("P5 catches header/sentinel version skew", "Framework_V.md",
            "# Framework_V v1.2\n# END OF Framework_V v1.3\n", "P5")

    # sentinel without a version is tolerated (several live specs are written that way)
    pv = write("Framework_S.md", "# Framework_S v9.9\n# END OF Framework_S\n")
    try:
        check_project_spec(pv)
        ok("versionless sentinel tolerated", True)
    except SpecDefect:
        ok("versionless sentinel tolerated", False)

    # discover() only picks up Framework_*.md
    write("registry.json", "{}")
    write("notes.md", "x")
    found = discover(d)
    ok("discover returns only Framework_*.md",
       found and all(SPEC_RE.match(f) for f in found)
       and "registry.json" not in found and "notes.md" not in found)
    ok("discover output is sorted", found == sorted(found))
    ok("discover on missing dir returns []", discover(os.path.join(d, "nope")) == [])

    # orphan routing: a project spec no route names is NOT loaded
    repo = tempfile.mkdtemp()
    open(os.path.join(repo, "Framework_Demo.md"), "w", encoding="utf-8").write(good)
    json.dump({"T": ["Framework_Demo.md"]},
              open(os.path.join(repo, "routes.json"), "w", encoding="utf-8"))
    proj = tempfile.mkdtemp()
    open(os.path.join(proj, "Framework_Demo.md"), "w", encoding="utf-8").write(
        "# Framework_Demo v9.9\n# END OF Framework_Demo v9.9\n")
    open(os.path.join(proj, "Framework_Retired.md"), "w", encoding="utf-8").write(
        "# Framework_Retired v2\n# END OF Framework_Retired v2\n")
    rep = resolve(repo, proj, os.path.join(d, "eff"))
    ok("project spec overrides repo",
       [e["file"] for e in rep["project_unverified"]] == ["Framework_Demo.md"])
    ok("overridden version is the project's",
       rep["project_unverified"][0]["version"] == "9.9")
    ok("unrouted project spec is ORPHAN, not loaded",
       [o["file"] for o in rep["orphan_project_specs"]] == ["Framework_Retired.md"])
    ok("overlay carries the project copy",
       "v9.9" in open(os.path.join(d, "eff", "Framework_Demo.md"), encoding="utf-8").read())
    ok("orphan not written into overlay",
       not os.path.exists(os.path.join(d, "eff", "Framework_Retired.md")))
    ok("report names the unverified file",
       "PROJECT-UNVERIFIED" in format_report(rep))
    # provenance record — the artefact that stops bootstrap reporting an override as
    # corruption. Regression guard for the 2026.08.03.8 release blocker.
    prov_p = os.path.join(d, "eff", PROVENANCE_FILE)
    ok("provenance file written into the overlay", os.path.exists(prov_p))
    pv = json.load(open(prov_p, encoding="utf-8"))
    ok("provenance lists the overridden spec",
       [e["file"] for e in pv["project_unverified"]] == ["Framework_Demo.md"])
    ok("provenance records the on-disk sha of the override",
       pv["project_unverified"][0]["sha256"] ==
       hashlib.sha256(open(os.path.join(proj, "Framework_Demo.md"), "rb").read()).hexdigest())
    ok("provenance never lists a .py engine",
       all(e["file"].endswith(".md") for e in pv["project_unverified"]))
    ok("provenance records orphans separately",
       pv["orphan_project_specs"] == ["Framework_Retired.md"])

    rep2 = resolve(repo, os.path.join(d, "empty-nope"), os.path.join(d, "eff2"))
    ok("no project specs -> fully repo-verified",
       rep2["project_unverified"] == [] and "100% REPO-VERIFIED" in format_report(rep2))
    pv2 = json.load(open(os.path.join(d, "eff2", PROVENANCE_FILE), encoding="utf-8"))
    ok("provenance written even with no overrides (empty list, not absent)",
       pv2["project_unverified"] == [])

    print("SELF-TEST: %d/%d PASS" % (passed, passed + failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--project-dir", default=PROJECT_DIR)
    ap.add_argument("--overlay-dir", default=OVERLAY_DIR)
    ap.add_argument("--trigger", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        sys.exit(_self_test())
    if not a.resolve:
        ap.error("nothing to do: pass --resolve or --self-test")
    try:
        rep = resolve(a.repo_dir, a.project_dir, a.overlay_dir)
    except SpecDefect as exc:
        print("[HARD STOP] project spec failed a well-formedness check: %s" % exc)
        print("Fix or remove the file in the project Files section. Do NOT proceed.")
        sys.exit(1)
    print(json.dumps(rep, indent=2) if a.json else format_report(rep, a.trigger))
    sys.exit(0)


if __name__ == "__main__":
    main()
