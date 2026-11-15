# DEPLOY NOTES — release 2026.11.19 (GAP-2026-11-15-RUN-ANALYSIS) over release 2026.11.17
This bundle REPLACES the 2026.11.18 bundle: do not deploy 2026.11.18, because everything in it is included here.
Deploy release 2026.11.17 (framework_release_2026.11.17_on_eaf40a9.zip) FIRST; this bundle is built on it
(local commit 8491f6b). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly 2026.11.17 when you deploy (any other commit on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (18 files = the 17 files that differ from 2026.11.17 + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_MockTestCreate.md             (v7.3 — STEP A2 PRE-REVIEW; one figure-proof rule; --auto-continue; + 7.2)
Framework_MockTestOrchestrate.md        (v1.10.0 — lean reviewer agents; one-line prompts; earlier standby)
LAW_REGISTRY.json                       (LAW-BC-2, LAW-BC-3, LAW-BC-6 amended)
MANIFEST.json                           (regenerated)
SESSION_BUDGET.json                     (review_qs_per_job_fallback = 10)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (Create v7.1 / v7.2 and Orchestrate v1.9.0 entries moved)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 7.3, Orchestrate 1.10.0)
VERSION                                 (2026.11.19)
audit_canonical.py                      (v2.43 — amber_findings per question)
audit_sync.py                           (ENGINE-STATUS-SYNC, from 2026.11.18)
blueprint_core.py                       (v2.9 — whole-proof settle; earlier-paper offsets; planned ask type)
bootstrap.py                            (--install-agents, --lean-agents; timing window fix)
final_assembly.py                       (v1.24 — pre-review; layout proof; lean job size)

SKILL CHANGE: none. EXAM PROJECTS: nothing to change; papers in progress continue unchanged.
TRIGGER: unchanged. Optional: add `--auto-continue` to a TestCreate / MockCreate message to start each next
batch without waiting for "continue" (the paper is still delivered after every batch).

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> N/N VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> 23/23 PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK
