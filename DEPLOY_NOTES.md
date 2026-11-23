# DEPLOY NOTES — release 2026.12.02 (Phase 1A + Phase 1B in ONE deployment) over release 2026.11.30
Built on production 12ca1ed (release 2026.11.30). ONE commit carries both phases: upload EVERY file below, flat (no
folders); push main, then main:production. Checked: production 12ca1ed + these files = the release tree exactly,
bootstrap 60/60 VERIFIED, manifests regenerate identically. If production moved past 12ca1ed, stop — rebuild.
CHANGELOG.md carries two entries (2026.12.01 = Phase 1A, 2026.12.02 = Phase 1B); VERSION is 2026.12.02.

PHASE 1A (measurement only): the orchestrator logs every fresh worker (and why), every warm standby (started / used),
the token totals the sub-agent tool reports per worker / reviewer / adjudicator / _switch job, and retention
failures, model limits, NO-MODEL, DIRECT MODE (Orchestrate O2-11). At PAPER_DELIVERED it prints the RUN REPORT
(counts only: question states, key certification, ladder rung, AMBER, bands on plan, USAGE) above the final chat
block; also written to <E>_M<N>_run_report.json. Never a stop.

PHASE 1B:
WHAT PHASE 1B DOES (no rule, gate, RUN-BLOCK, engine call, job, round, ladder, model or deliverable changes):
- G6: a worker / standby / DIRECT-MODE read of Framework_MockTestOrchestrate.md skips PART A (O1-1 .. O2-11, the
  orchestrator's law). The orchestrator still reads it whole. 26,267 B (~11,400 tokens) less per worker read.
- G5: Framework_MockTestCreate v8.9 — superseded version entries v8.8 .. v7.3.1 moved verbatim to SPEC_HISTORY.md
  (10,291 B). The rest of the file is byte-identical.
- Net worker read (TestCreate): FINAL ~340,331 -> ~326,767 tokens; NON-FINAL ~320,529 -> ~306,965 (-4.0%).
- G7: new CI gate SPEC-READ-GROWTH (audit_specs_ext): a release that grows any trigger's read by more than 2,300 B
  (~1,000 tokens) over SESSION_BUDGET.json read_growth_baseline_bytes fails CI unless the baseline is raised in the
  same commit with the reason in CHANGELOG. When a later release CUTS a read, lower that trigger's baseline.
- G2: Orchestrate recognises the lean reviewer / adjudicator types under a plugin prefix (mtc-agents:mtc-reviewer).

UPLOAD LIST (14 files — both phases):
CHANGELOG.md, DEPLOY_NOTES.md, Framework_MockTestCreate.md (v8.9), Framework_MockTestOrchestrate.md (v1.15.0),
MANIFEST.json, SESSION_BUDGET.json (read_growth_* keys), SHA256SUMS.txt, SPEC_HISTORY.md, SPEC_MANIFEST.json,
SPEC_SECTIONS.json, VERSION (2026.12.02), audit_specs_ext.py, bootstrap.py, spec_sections.py

ONE-TIME, OUTSIDE GITHUB — the mtc-agents plugin (mtc-agents.plugin, delivered beside this bundle): open it in the
Claude app and install it. It holds the two lean sub-agents (Opus, Read + Write only). Check on the next run: the
orchestrator records `--lean-agents yes` when it sees them (USAGE / the session start). If it says `no`, nothing
breaks — review jobs run as before; tell Claude, because plugin agents may not reach cloud chats on every surface.

AFTER DEPLOY — the reference run: run CSIR NET Chemical Sciences P1 --level subject --scope "Organic Chemistry" (40
questions). Note the plan Usage % before and after, and keep the RUN REPORT / USAGE lines printed above the final chat
block. Compare the quality numbers (keys, ladder, AMBER, band on plan) with what earlier papers of this exam looked like;
if any is clearly worse, roll back and report it. Because 1A and 1B ship together, this run has no "before the cut"
counterpart: the read cut is small (-4.0%) and changes no rule, so the run is the baseline for Phase 2.

VERIFY BEFORE PUSH (on the commit):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.12.02, 60/60 VERIFIED
  4. python3 bootstrap.py --self-test (104/104); python3 spec_sections.py --self-test (40/40);
     python3 audit_specs_ext.py --self-test (27 passed, 0 failed); python3 audit_specs_ext.py (0 issues)
  5. python3 run_ci_gates.py --skip Install                             -> every step PASS
  6. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.30 files (production 12ca1ed) together. The plugin can be
uninstalled at any time; the framework falls back to the general-purpose type.
