#!/usr/bin/env python3
"""
LOAD-AND-VERIFY GATE  (runs inside a freshly-cloned framework repo)

Verifies the ENTIRE framework (every file in MANIFEST.json) on every run:
PRESENT + BYTE-EXACT (sha256) + expected VERSION (.md header) + WHOLE
(.md END-sentinel + exact line count). Because the whole framework is verified,
an imperfect routes.json can never cause a missing/partial dependency at runtime.

Contract:
  - Exit 0 AND write .verified  -> only when EVERY tracked file passes.
  - Exit 1 (HARD STOP)          -> on ANY failure. Caller MUST NOT proceed
                                   from memory / project knowledge.

--trigger is optional and advisory: if given and known, the gate prints which
spec(s) are that step's entry point to read IN FULL. Verification always covers
all files regardless of trigger.

Usage:
    python3 bootstrap.py                     # verify whole framework
    python3 bootstrap.py --trigger MockDeliver
"""
import argparse, hashlib, json, os, sys

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def fail(msg):
    print(f"[HARD STOP] {msg}")
    print("Do NOT generate anything from memory or project knowledge. Stop here.")
    sys.exit(1)

def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [ln.rstrip("\n") for ln in f]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trigger", default=None, help="optional step trigger, e.g. MockDeliver")
    ap.add_argument("--manifest", default="MANIFEST.json")
    args = ap.parse_args()

    if not os.path.exists(args.manifest):
        fail("MANIFEST.json missing from clone (partial/failed clone?)")
    try:
        M = json.load(open(args.manifest, encoding="utf-8"))
    except Exception as e:
        fail(f"MANIFEST.json is not valid JSON: {e}")

    files_meta = M.get("files", {})
    routes = M.get("routes", {})
    fw_version = M.get("framework_version", "?")
    if not files_meta:
        fail("MANIFEST.json has no files listed")

    verified = []
    for fname, meta in sorted(files_meta.items()):
        if not os.path.exists(fname):
            fail(f"{fname}: file absent in clone (partial clone / deleted file)")
        actual = sha256(fname)
        if actual != meta["sha256"]:
            fail(f"{fname}: sha256 MISMATCH\n  expected {meta['sha256']}\n  actual   {actual}")
        lines = read_lines(fname)
        if len(lines) != meta["lines"]:
            fail(f"{fname}: line count {len(lines)} != manifest {meta['lines']}")
        if fname.endswith(".md"):
            if not lines or lines[0].rstrip() != meta["version_header"].rstrip():
                fail(f"{fname}: version header mismatch\n  expected '{meta['version_header']}'\n  actual   '{(lines[0] if lines else '')}'")
            nonblank = [l for l in lines if l.strip() != ""]
            if not nonblank or nonblank[-1] != meta["end_sentinel"]:
                fail(f"{fname}: END sentinel not last line -> possible truncation. "
                     f"Expected: '{meta['end_sentinel']}'")
        verified.append(fname)

    token = {"framework_version": fw_version, "files": verified,
             "read_rule": "Read each .md IN FULL to its END-sentinel line; line counts are exact."}
    with open(".verified", "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)

    print(f"[OK] FRAMEWORK {fw_version} VERIFIED — {len(verified)}/{len(files_meta)} files, "
          f"all checksums/versions/whole-file checks PASS")

    if args.trigger:
        entry = routes.get(args.trigger)
        if entry:
            print(f"Entry-point spec(s) for '{args.trigger}' — read IN FULL: {entry}")
        else:
            print(f"[note] trigger '{args.trigger}' not in advisory routes; "
                  f"read the spec whose header matches your step. All files are verified & present.")
    print(".verified written. Read the needed spec(s) in full, then execute the step.")

if __name__ == "__main__":
    main()
