# DEPLOY NOTES — release 2026.11.30 (OD-2026-11-23-OPUS-ONLY) over release 2026.11.29
Built on production 23df622 (release 2026.11.29). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for every exam
(MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production has any content change beyond 23df622 when you deploy (git diff 23df622 production not empty), stop —
the bundle must be rebuilt on the new production commit.

WHAT IT DOES: owner instruction 2026-11-23 "never use Fable; always use Opus for any worker or any other task".
Every Step 7 sub-agent (worker, standby, reviewer, adjudicator, _switch re-ask) runs on Opus only. Reviewer and
adjudicator independence stays: fresh context + blind packet (Orchestrate O6-1). No gate, job, round, ladder,
deliverable, end state or user action changed.

UPLOAD LIST (the files that differ from 2026.11.29, plus DEPLOY_NOTES.md and SHA256SUMS.txt; none is new):
CHANGELOG.md                       (2026.11.30 entry)
DEPLOY_NOTES.md                    (this file)
Framework_MockTestOrchestrate.md   (v1.13.0 — O2-2: every sub-agent's model comes from worker_models only; O2-3, O3-6,
                                    O6-1, O4-1 lose "a different model when the platform offers one")
MANIFEST.json                      (regenerated)
SESSION_BUDGET.json                (worker_models ["opus"]; _worker_models note)
SHA256SUMS.txt                     (checksums of this upload)
SPEC_MANIFEST.json                 (regenerated)
SPEC_SECTIONS.json                 (regenerated)
STEP_CONTRACTS.json                (floor: MockTestOrchestrate 1.13.0)
VERSION                            (2026.11.30)
bootstrap.py                       (--install-agents writes `model: opus` into mtc-reviewer / mtc-adjudicator)

NOT CHANGED: Framework_MockTestCreate.md and every engine (its "another model" wording is read only by workers, which
never start sub-agents; the orchestrator takes models from Orchestrate O2-2 alone). SKILL / TRIGGERS / ROUTES unchanged.

AFTER DEPLOY: nothing per exam. Every MockCreate / TestCreate trigger after deploy runs Opus-only. A run already in
progress keeps the Orchestrate text it read at its own Step 0 (Step 0 runs once per run, O2-1); in that run Fable is
used again only if its limit has reset.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.11.30, 60/60 VERIFIED
  4. python3 validate_framework_md.py Framework_*.md                    -> 0 issues
  5. python3 run_ci_gates.py --skip Install                             -> every step PASS
  6. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.29 files (production 23df622) together. Nothing on disk in any exam depends on this
release.
