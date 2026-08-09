#!/usr/bin/env python3
"""
SPEC_MANIFEST regenerator — rebuilds SPEC_MANIFEST.json from the LIVE bytes on disk.

Why this exists: gen_manifest.py rebuilds MANIFEST.json (the bootstrap integrity set) but
NOTHING rebuilt SPEC_MANIFEST.json — so its entries silently drifted whenever a tracked
file changed without a hand-edit (the 2026-08-09 PYQ-2 wave shipped seven stale entries:
notes_core/blueprint/audit, routes.json, audit_sync.py, audit_deep.py, validate_framework_md.py).

Behaviour (non-destructive):
  * Tracked set = the keys already in SPEC_MANIFEST.json (this file never invents entries).
  * For each tracked file PRESENT on disk -> recompute sha256/size/lines/version_header/end_sentinel.
  * For each tracked file ABSENT on disk -> keep its existing entry and WARN (it may live
    outside this tree, or it may be a genuine deletion — the human decides).
  * --drop A,B  removes named entries (use for genuinely deleted files).
  * Any top-level keys besides "files" are preserved verbatim.

Usage:
    python3 build_spec_manifest.py                      # refresh in place
    python3 build_spec_manifest.py --drop Framework_PYQExplainAudit.md,explain_audit_gate.py
    python3 build_spec_manifest.py --check             # exit 1 if anything is stale (CI)
"""
import argparse, hashlib, json, os, sys

def sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def version_header(p):
    return open(p, encoding="utf-8").readline().rstrip("\n")

def end_sentinel(p):
    for line in reversed([l.rstrip("\n") for l in open(p, encoding="utf-8")]):
        if line.strip():
            return line
    return ""

def linecount(p):
    return sum(1 for _ in open(p, encoding="utf-8"))

def entry_for(p):
    return {
        "end_sentinel": end_sentinel(p),
        "lines": linecount(p),
        "sha256": sha256(p),
        "size_bytes": os.path.getsize(p),
        "version_header": version_header(p),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="SPEC_MANIFEST.json")
    ap.add_argument("--drop", default="", help="comma-separated filenames to remove")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if any present file is stale")
    args = ap.parse_args()

    doc = json.load(open(args.path, encoding="utf-8"))
    files = dict(doc.get("files", {}))
    drop = {x.strip() for x in args.drop.split(",") if x.strip()}
    for d in drop:
        files.pop(d, None)

    absent, stale, refreshed = [], [], []
    for name in sorted(files):
        if not os.path.exists(name):
            absent.append(name)
            continue
        fresh = entry_for(name)
        if fresh != files[name]:
            stale.append(name)
        files[name] = fresh
        refreshed.append(name)

    if args.check:
        if stale:
            print("SPEC_MANIFEST STALE:", sorted(stale), file=sys.stderr)
            sys.exit(1)
        print(f"SPEC_MANIFEST current — {len(refreshed)} present entries verified, "
              f"{len(absent)} not on disk.")
        sys.exit(0)

    doc["files"] = files
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"SPEC_MANIFEST.json written: {len(files)} entries "
          f"({len(refreshed)} present/refreshed, {len(absent)} kept-absent"
          f"{', ' + str(len(drop)) + ' dropped' if drop else ''}).")
    if stale:
        print("  refreshed stale entries:", sorted(stale))
    if absent:
        print("  WARN kept (not on disk):", sorted(absent))

if __name__ == "__main__":
    main()
