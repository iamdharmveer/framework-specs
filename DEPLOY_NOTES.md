# DEPLOY NOTES — release 2026.11.24 (GAP-2026-11-18-DIFFICULTY-AND-CORRECTNESS v4.1) over release 2026.11.23
Built on production d29dc50 (release 2026.11.23). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly d29dc50 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (21 files = the files that differ from 2026.11.23 + DEPLOY_NOTES.md + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                         (this file)
Framework_Blueprint.md                  (v1.66.0 — FG-4 advisory line; status untouched)
Framework_DeliveryFooter.md             (v1.53.0 — §2R slot ledger / swap / paper level / E1 / figure lines; 3 question lines)
Framework_MockTestAnalyse.md            (v2.64.0 — S11-1d before S11-1c; grades from the ladder; ask_form / statement_forms)
Framework_MockTestCreate.md             (v8.3 — S3-12e ladder shares; S3-16 figure plan + stem form + E1; S4-7.1 packet;
                                         S13-2L.0 one pure band swap; figure manifest with plan)
Framework_PYQExplain.md                 (v2.33 — §13A-4 names incomplete option_text records)
Framework_ScopedBlueprint.md            (v1.16.0 — FG-4 advisory line; status assert untouched)
LAW_REGISTRY.json                       (NEW LAW-R31-1 / LAW-R31-2 / LAW-R31-3)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.3, Analyse 2.64.0, Footer 1.53.0, Blueprint 1.66.0,
                                         Scoped 1.16.0, PYQExplain 2.33)
VERSION                                 (2026.11.24)
analyse_engine.py                       (OMML options, tables, complete ladder rows, packet reuse, stem-form lines; 313 checks)
audit_canonical.py                      (A-AXIS1 counts recorded figure shortfalls at their planned format; 675 checks)
blueprint_core.py                       (Cluster R3.1 — pooled placement, swap, claims, plans, ladder grades; 1550 checks)
corpus_io.py                            (formula subscripts on arrow / caption text; 595 checks)
figural_core.py                         (plotted data on the figure record; 241 checks)
final_assembly.py                       (per-reviewer anchors, claims, bv_s3_plans, figure fallback, footer lines; 238 checks)

SKILL CHANGE: none. TRIGGERS: unchanged.

AFTER DEPLOY:
  1. Nothing to change in any of the ~200 projects. Spec copies in a project's Files below the new floors
     (Create 8.3, Analyse 2.64.0, DeliveryFooter 1.53.0, Blueprint 1.66.0, ScopedBlueprint 1.16.0, PYQExplain 2.33)
     are not loaded — remove them to silence the [STALE — NOT LOADED] line.
  2. Difficulty ladder: the first PYQExtract (Step 5) run of an exam after this release refits its ladder ONCE
     (ladder release < 2026.11.24): options with formulas, tables and figure files now reach the rankers. Packets
     whose text did not change are reused (no re-ranking). Until that run, Create uses the old ladder and says so.
  3. section_rules gains ask_form / statement_forms lines on the next Step 5 run; until then those two controls are
     dormant (printed), never a stop.
  4. A paper already in progress resumes unchanged (its plans are frozen in batch_state); the figure plan is built by
     the engine fallback for it when absent.
  5. Live bench (owner ruling RL-6): run CSIR Chemistry plus 3 exams and share the registries; the footer prints
     DIFFICULTY SLOTS, PAPER LEVEL and FIGURES lines for checking.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.23 bundle (production d29dc50).
