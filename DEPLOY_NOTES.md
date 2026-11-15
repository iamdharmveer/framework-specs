# DEPLOY NOTES — release 2026.11.20 (GAP-2026-11-15-RUN-ANALYSIS, second pass) over release 2026.11.19
Deploy release 2026.11.19 (framework_release_2026.11.19.zip, the bundle being deployed now) FIRST; this bundle is
built on it. Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly 2026.11.19 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (15 files = the 14 files that differ from 2026.11.19 + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.51.1 — the S13-2P figure-proof line catalogued)
Framework_MockTestCreate.md             (v7.3.1 — auto-continue start-up fix; list_columns; B-5 exception)
Framework_MockTestOrchestrate.md        (v1.10.1 — lean-agents recorded before the first worker; standby fix)
LAW_REGISTRY.json                       (LAW-BC-5 amended — full reviewer packets)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (Create v7.3, Orchestrate v1.10.0, Footer v1.51.0 entries moved)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 7.3.1, Orchestrate 1.10.1)
VERSION                                 (2026.11.20)
bootstrap.py                            (--auto-continue accepted; repeated window opener ignored)
final_assembly.py                       (v1.24.1 — stimulus in reviewer packets; narrower pre-review)

SKILL CHANGE: none. EXAM PROJECTS: nothing to change; papers in progress continue unchanged.
TRIGGER: unchanged. Optional: add `--auto-continue` to a TestCreate / MockCreate message to start each next
batch without waiting for "continue" (the paper is still delivered after every batch). On 2026.11.19 alone this flag
stops the run at session start: deploy 2026.11.20 before using it.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> N/N VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> 23/23 PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK
