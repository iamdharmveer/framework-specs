# DEPLOY NOTES — release 2026.12.03 (Phase 1C: lean safety fallback + model wording) over release 2026.12.02
Deploy ONLY AFTER release 2026.12.02 (Phase 1A + 1B) is in production, and ideally after its reference run.
Upload EVERY file below in ONE commit, flat (no folders); push main, then main:production. A partial upload fails
bootstrap for every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
Before uploading: production must be exactly the 2026.12.02 bundle (`cat VERSION` -> 2026.12.02 and
`sha256sum -c` of the 2026.12.02 SHA256SUMS.txt passes on it). If anything else changed, stop — rebuild 1C on it.

WHAT IT DOES (no gate, RUN-BLOCK, engine, job count, round, ladder, model, read set or deliverable changes):
- LEAN SAFETY FALLBACK (Orchestrate O2-3 v1.16.0, bootstrap --lean-failure): a review job started as the plugin's
  lean type that fails for a non-limit reason is reported; at the 2nd such failure in a run the lean types are dropped
  for that run and every later job runs as the normal (general-purpose) reviewer — what ran before 2026.11.19. The
  RUN REPORT then shows "USAGE lean reviewers: DROPPED this run after 2 failures (last: ...)". A broken plugin can no
  longer pause a paper on every message.
- WORDING (Create v8.10): four lines that said "another model" now say "a fresh context" (Opus-only since 2026.11.30).
- HISTORY: Create entry v8.9 and Orchestrate entries v1.10.1 .. v1.15.0 moved verbatim to SPEC_HISTORY.md.
- READ: a worker reads ~1,000 tokens LESS than on 2026.12.02 (FINAL ~325,764 tokens); the SPEC-READ-GROWTH baseline
  for MockCreate / TestCreate is lowered to the new size (794,337 B).

UPLOAD LIST (12 files):
CHANGELOG.md                       (2026.12.03 entry)
DEPLOY_NOTES.md                    (this file)
Framework_MockTestCreate.md        (v8.10 — wording only)
Framework_MockTestOrchestrate.md   (v1.16.0 — O2-3 lean safety fallback; O2-11 lean_fallback event)
MANIFEST.json                      (regenerated)
SESSION_BUDGET.json                (read_growth_baseline_bytes MockCreate / TestCreate lowered)
SHA256SUMS.txt                     (checksums of this upload)
SPEC_HISTORY.md                    (moved entries)
SPEC_MANIFEST.json                 (regenerated)
SPEC_SECTIONS.json                 (regenerated)
VERSION                            (2026.12.03)
bootstrap.py                       (--lean-failure; lean_fallback in USAGE; self-test 105/105)

SEPARATELY (not GitHub): a small correction to your mock-test-framework skill (SKILL.md rule 2a: the old PYQExtract
token figure is marked as the August 2026 incident and points to what bootstrap prints) — approve it on the card in
chat. The framework does not depend on it.

VERIFY BEFORE PUSH (on the commit):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.12.03, 60/60 VERIFIED
  4. python3 bootstrap.py --self-test                                   -> 105/105
  5. python3 run_ci_gates.py --skip Install                             -> every step PASS
  6. sha256sum -c SHA256SUMS.txt                                        -> every file OK

AFTER DEPLOY: nothing per exam. Papers already running keep the rules they started with; new runs use 1C.
How to see it working: in a run where the plugin loads, the RUN REPORT shows no "lean reviewers: DROPPED" line; if it
ever shows one, the plugin is broken on that surface — uninstall it, and tell Claude the error text it names.

ROLLBACK: re-deploy the 2026.12.02 files together.
