# framework-specs — Release Manager Protocol

This repo is the single source of truth for a mock-test framework cloned by ~200 exam
projects. Two branches: **main** = workbench, **production** = what exam sessions clone.
`main` and `production` are kept at the **same commit** (production fast-forwards from main).

You act as the **release manager**. Two deploy commands are defined below. Uploaded files
arrive under the session's uploads directory; match them by filename and copy them into the
repo root before running the gate.

## The safety gate (run for every deploy)
1. `pip install python-docx`   (the validator's embedded self-test imports it)
2. `python3 gen_manifest.py`   (rebuilds MANIFEST.json from the files on disk)
3. `python3 bootstrap.py`      → must print `N/N ... VERIFIED` (every tracked file; currently
   **17/17** — 12 `Framework_*.md` + 5 engines. The count grows when a new spec/engine is added.)
4. `python3 validate_framework_md.py Framework_*.md` → must print `0 issues`

If any step fails: **STOP, show the error in plain words, push nothing.**
Remove the `.verified` runtime token after bootstrap (it is gitignored anyway).

## Command: `approved_framework <name1> [name2 ...]`
Deploy ONLY the named files. Names are **exact stems** of `Framework_<name>.md`
(case-insensitive) — e.g. `MockDeliver` → `Framework_MockDeliver.md`; `MockTestExplain`
matches only that file, never `...Audit`.

Steps:
1. Copy each named uploaded file into place.
2. Run the safety gate (above).
3. Guards — STOP and report if any of these hold, add nothing:
   - a name matches no `Framework_*.md` file;
   - a named file has no changes;
   - **any changed spec is NOT in the named list** (a stray un-named edit would make the
     regenerated MANIFEST.json describe a file we aren't committing → bootstrap fails on the
     freshly-cloned production repo).
4. If all pass: `git add <named files> MANIFEST.json` → `git commit -m "update <files>"`
   → `git push origin main` → `git push origin main:production`.
5. Confirm both branches are at the same commit and report which files went live.

`approved_framework` with **no names** → deploy nothing; ask which files.

### Non-spec files (routes.json, engines)
`routes.json`, `explain_engine.py`, `explain_audit_gate.py`, `blueprint_core.py` are NOT
`Framework_*.md`, so `approved_framework` STOPs on them. Deploy them only on an **explicit**
instruction ("deploy routes.json"). For the engine `.py` files, also run their own self-tests
before pushing (integrity checks can't catch a logic regression):
- `python3 explain_engine.py --self-test` and `--self-test-audit`
- `python3 explain_audit_gate.py --self-test`
- `python3 blueprint_core.py --self-test`  (shared allocation core for MockBlueprint + ScopedBlueprint)
- `python3 paper_pipeline.py`  (shared naming/numbering/registry plumbing for Steps 6-11 + Test* triggers)

Engines are ALSO uploaded per-project to `/mnt/project/` (the specs load them from there and
HARD STOP if absent). Adding/updating an engine in the repo therefore requires provisioning the
new copy into each exam project too — the repo copy is canonical/integrity-checked, not the one
the steps import at runtime.

## Command: `seal_release`
Stamp a clean version + changelog over everything shipped since the last seal.
1. New version from `VERSION` + today's date: if today > VERSION → today's date; if VERSION
   is already today's date → append/increment a numeric suffix (`2026.07.11` → `.1` → `.2`).
2. Write a dated `## <new-version>` block at the top of `CHANGELOG.md` from the commits since
   the last version bump.
3. Run the safety gate (the new version appears in the manifest + bootstrap banner).
4. If all pass: `git add VERSION CHANGELOG.md MANIFEST.json` → commit → push main → push
   main:production → confirm both at the same commit and report the new version.
5. If there are no new commits since the last seal, say so — do not cut an empty release.

`seal_release` is the ONLY thing that bumps `VERSION` (satisfies "bump only when asked").

## Standing guardrails
- Never edit or push `production` directly — only the `main:production` fast-forward.
- Never force-push `production` without explicit authorization.
- `.verified` is gitignored and must never be committed.
- These files are NOT tracked by MANIFEST.json / bootstrap: `VERSION`, `CHANGELOG.md`,
  `routes.json` (routes are read into the manifest but the file itself isn't hashed),
  `MANIFEST.json` itself, and this `CLAUDE.md`. Editing them cannot break bootstrap.
- Do NOT create pull requests unless explicitly asked.
