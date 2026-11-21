# DEPLOY NOTES — release 2026.11.27 (GAP-2026-11-21-MATH-TYPESET + GAP-2026-11-21-FIGURE-NEED) over release 2026.11.26.1
Built on production 9575e8a55d4751e3ad3c26e4d6ebf4e71eb29a88 (release 2026.11.26.1) and verified on production c7c6a47
(4 later commits added and removed SYNC_TEST.md only — tree byte-identical to 9575e8a). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production has any content change beyond c7c6a47 when you deploy (git diff c7c6a47 production not empty), stop and
send me the production commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (19 files = the 17 files that differ from 2026.11.26.1 + DEPLOY_NOTES.md + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                         (this file)
Framework_DeliveryFooter.md             (v1.56.0 — §LADDER-BC: "maths written as text", "the figure restates the stem";
                                         §LADDER-NF: the A-TYPESET composition line)
Framework_MockReview.md                 (v2.4.0 — S2-2R: D-FIG-DECORATIVE, minor, only in jobs with a non-chemistry figure;
                                         300 lines — one reviewer read)
Framework_MockTestAnalyse.md            (v2.65.0 — synthesis measures MATH_TYPESET_PROFILE per SUBJECT; stamps v2.65)
Framework_MockTestCreate.md             (v8.6 — S3-16 plan print; S4-7.1 notation line; S4-11 two soft items; OPTION A
                                         FIGURE PURPOSE / FIGURE STYLE; S7-QUALITY stem_src / option_src; S10-3 builders
                                         route ⟦MATH:…⟧ regions; S10-4 render_mock_text font + display; decision-tree
                                         rule 8; GENERATION ROUTING; rule 5 / rule 8 amendments; S12-NEW-31 / -32)
LAW_REGISTRY.json                       (LAW-TYPESET-1, LAW-FIG-NEED-1)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (MockReview v2.3.1 entry moved here verbatim — SPEC-CAPACITY: one 300-line read)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.6, MockTestAnalyse 2.65.0, MockReview 2.4.0, DeliveryFooter 1.56.0)
VERSION                                 (2026.11.27)
analyse_engine.py                       (v1.7 — math_typeset_rows_from_docx / math_typeset_profiles /
                                         math_typeset_chem_subjects; write_section_rules writes the profile lines; 317)
audit_canonical.py                      (v2.46 — A-TYPESET, WARN only; 693)
blueprint_core.py                       (v2.12 — Cluster P1: six arms, linear form, per-subject plan, chemistry boundary,
                                         fig_need, soft gates G-MATH-TYPESET / G-FIG-NEED, D-FIG-DECORATIVE, notation
                                         line, A-TYPESET maths; standard library only; 1625)
figural_core.py                         (v5.98 — text_labels record; strict-subject line art + italic labels; plain alt; 245)
final_assembly.py                       (v1.28.0 — plan frozen at S3-16; gate context; AMBER lines at settle; FIG brief
                                         choice; chemistry types from figure_types; t3 drift lock; 254)

SKILL CHANGE: none. TRIGGERS: unchanged. ROUTES: unchanged.

AFTER DEPLOY:
  1. Every exam: nothing to do for the figure fix (G-FIG-NEED, plain alt text) and the region routing — they reach every
     project on its next Step 0. Spec copies in a project's Files below the new floors are not loaded — remove them
     to silence the [STALE — NOT LOADED] line.
  2. Maths typesetting is MEASURED per exam: run `PYQExtract <EXAM> --synthesise ALL` once with the exam's Sorted PYQ
     .docx files attached to the chat (or in Project Files). section_rules.md then carries one MATH_TYPESET_PROFILE
     line per subject; upload the new section_rules.md to the project as usual. Until then every subject is 'off'
     (today's maths behaviour). Chemistry subjects always measure off and stay unchanged.
     CSIR NET Mathematical Sciences, measured on 02-Mar-2025 / 18-Dec-2025 / 17-Jul-2026: Mathematical Sciences
     strict (84% of 300 questions typeset, all six arms), General Aptitude off.
     Without a Step 5 run, the owner may add by hand to section_rules.md (subject or paper-part names both work):
         MATH_TYPESET_MODE: Mathematical Sciences = strict
  3. A paper in progress resumes unchanged (its batch_state has no 'math_typeset'); new papers pick the plan up at S3-16.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.11.27, 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.26.1 files (production 9575e8a). The new section_rules lines are ignored by 9575e8a
(its parsers read only the prefixes they know); text_labels / stem_src / option_src / math_typeset are unknown keys to it.
