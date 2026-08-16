#!/usr/bin/env python3
"""
MANIFEST GENERATOR — run by CI (and locally) to (re)build MANIFEST.json from the
actual files on disk. The manifest is ALWAYS machine-generated, never hand-edited,
so it can never drift from the files it describes.

Tracked framework files = every Framework_*.md plus the tracked *.py engines/gates.
Per-trigger routing (incl. cross-file dependencies) is read from routes.json.

CI usage (see .github/workflows/validate.yml):
    python3 gen_manifest.py
    git diff --exit-code MANIFEST.json   # fails the build if committed manifest is stale
"""
import hashlib, json, os, sys

TRACKED_PY = ["validate_framework_md.py", "explain_engine.py",
              "t3_mathcomp.py",
              "blueprint_core.py", "paper_pipeline.py", "final_assembly.py",
              "corpus_io.py", "reconcile_taxonomy.py", "syllabus_provenance.py",
              "figural_core.py", "figural_vision.py", "audit_canonical.py",
              "spec_source.py", "spec_name_audit.py", "mock_sync_audit.py",
              "frequency_xlsx.py",
              "notes_core.py", "notes_blueprint.py", "notes_audit.py",
              "notes_docx.py", "notes_sync_audit.py"]

# GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (P7). The law-propagation registry is DATA
# the CI enforces, so it needs the same byte-integrity guarantee as an engine: an
# untracked registry can be gutted to `{"laws":{}}` and every law it enforces goes
# quiet with nothing to notice. bootstrap.py applies header/sentinel checks only to
# .md files, so a .json entry is verified by sha256 + line count, which is exactly
# what is wanted here.
# GAP-2026-08-16-STEP5-SESSION-EXHAUSTION (Fix A). SPEC_SECTIONS.json is the read-set
# map §S8-0b routes on. It holds LINE NUMBERS ONLY and never spec content, so it is a
# read aid and not a second source of truth — but a STALE map is worse than no map: it
# sends a reduced read at ranges that no longer bound the sections they name. Tracking
# it by sha256 means bootstrap.py fails the build the moment a spec is edited without
# regenerating it, which is before anybody can read a wrong range.
TRACKED_JSON = ["LAW_REGISTRY.json", "SPEC_SECTIONS.json"]

def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def head(p):
    with open(p, encoding="utf-8") as f:
        return f.readline().rstrip("\n")

def end_sentinel(p):
    nonblank = [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() != ""]
    return nonblank[-1] if nonblank else ""

def linecount(p):
    with open(p, encoding="utf-8", newline="") as f:
        return sum(1 for _ in f)

def main():
    # Regenerate the section map FIRST. If this ran after hashing, a run of
    # gen_manifest.py would record the sha256 of the PREVIOUS map and the manifest
    # would be born stale — the exact drift class this file exists to make impossible.
    if os.path.exists("spec_sections.py"):
        import subprocess
        subprocess.run([sys.executable, "spec_sections.py"], check=True,
                       stdout=subprocess.DEVNULL)
    if not os.path.exists("routes.json"):
        print("ERROR: routes.json not found", file=sys.stderr); sys.exit(2)
    routes = json.load(open("routes.json", encoding="utf-8"))
    routes = {k:v for k,v in routes.items() if not k.startswith('_')}
    fw_version = open("VERSION", encoding="utf-8").read().strip() if os.path.exists("VERSION") else "0.0.0"

    tracked = sorted(f for f in os.listdir(".") if f.endswith(".md") and f.startswith("Framework_"))
    tracked += [p for p in TRACKED_PY if os.path.exists(p)]
    tracked += [p for p in TRACKED_JSON if os.path.exists(p)]

    files = {}
    for f in tracked:
        files[f] = {
            "sha256": sha256(f),
            "version_header": head(f),
            "end_sentinel": end_sentinel(f),
            "lines": linecount(f),
            "bytes": os.path.getsize(f),
        }

    # integrity: every file named in routes must be a tracked, hashed file
    missing = sorted({fn for fs in routes.values() for fn in fs} - set(files))
    if missing:
        print(f"ERROR: routes.json references files not present/tracked: {missing}", file=sys.stderr)
        sys.exit(2)

    manifest = {
        "framework_version": fw_version,
        "generated_by": "gen_manifest.py",
        "routes": routes,
        "files": files,
    }
    with open("MANIFEST.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print(f"MANIFEST.json written: v{fw_version}, {len(files)} files, {len(routes)} triggers")

if __name__ == "__main__":
    main()
