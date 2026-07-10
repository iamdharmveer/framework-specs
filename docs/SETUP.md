# SETUP — stand up the public framework repo (one time)

## A. Create the repo and push
1. Create a new **public** GitHub repo: `framework-specs` (empty, no README).
2. On your machine, in a folder containing this scaffold PLUS your 14 real files
   (11 Framework_*.md + validate_framework_md.py + explain_audit_gate.py + explain_engine.py):

    git init -b main
    git add .
    python3 gen_manifest.py          # builds MANIFEST.json from the real files
    git add MANIFEST.json
    git commit -m "Framework v2026.07.10"
    git remote add origin https://github.com/iamdharmveer/framework-specs.git
    git push -u origin main

3. Create the release branch that exam sessions clone:

    git branch production
    git push -u origin production

## B. Protect production (tamper resistance)
On GitHub → Settings → Branches → add a rule for `production`:
- Require a pull request before merging
- Require status checks: `validate-framework`
- Do not allow force pushes / deletions
- (Optional, strongest) Require signed commits

## C. DR mirror (chosen: build from day one)
1. Create a second **public** repo on a different host (e.g. GitLab) `framework-specs`.
2. In GitHub repo → Settings → Secrets and variables → Actions, add:
   - `MIRROR_URL` = https://gitlab.com/<YOU>/framework-specs.git
   - `MIRROR_PAT` = a write token for the mirror host
3. `mirror.yml` then auto-pushes `production` to the mirror on every release.

## D. Per exam project (repeat, but trivial)
- Keep ONLY the per-exam JSON/artifacts in the project Files section
  (`<Exam>_blueprint.json`, `<Exam>_registry.json`, etc.). Remove any Framework_*.md.
- Paste the block from docs/CUSTOM_INSTRUCTIONS.md into Custom Instructions,
  setting TRIGGER per step (or keep a per-step version).

## E. Before rollout
Run docs/ACCEPTANCE_TEST.md inside ONE real exam project. Proceed to all 200 only
if it prints EGRESS OK + MOUNT OK + green VERIFIED.

# RELEASE / ROLLBACK runbook
- Edit specs on `main` → PR → CI green → merge.
- RELEASE: fast-forward `production` to the validated `main` commit and tag it:
      git checkout production && git merge --ff-only main
      git tag v$(cat VERSION) && git push origin production --tags
  Propagates to all 200 exams atomically on their next run.
- ROLLBACK: move production back one tag:
      git checkout production && git reset --hard v<previous> && git push -f origin production
