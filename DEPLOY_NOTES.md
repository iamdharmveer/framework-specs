# DEPLOY NOTES — release 2026.11.02 (GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY)
Over verified production aa50912 (2026.11.01); commit once, push main, push main:production.
Upload EVERY file below (30 files) in ONE commit. A partial upload fails bootstrap for every exam
(MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

Engines:  figural_core.py (-> v5.89)            corpus_io.py (v1.16 -> v1.17)
          blueprint_core.py (v1.28 -> v1.29)    figure_types.py (v1.0 -> v1.1)
          analyse_engine.py (v1.0 -> v1.1)      audit_canonical.py (v2.33 -> v2.34)
          final_assembly.py (v1.10 -> v1.11)    explain_engine.py (-> v2.12)
          paper_pipeline.py (handoff_set extra_upload)
          bootstrap.py (+ --receipt)            validate_framework_md.py (v3.3 HS-CLASS check)
Specs:    Framework_MockTestCreate.md (v5.88 -> v5.89)      Framework_ScopedBlueprint.md (v1.11.0 -> v1.12.0)
          Framework_Blueprint.md (v1.61.0 -> v1.62.0)      Framework_MockTestAnalyse.md (v2.57.3 -> v2.58.0)
          Framework_PYQExplain.md (v2.24 -> v2.25)          Framework_MockTestExplain.md (-> v1.52.0)
          Framework_DeliveryFooter.md (v1.36.0 -> v1.37.0) Framework_MockDeliver.md (HARD STOP class tags only)
Governance: routes.json (figure_types.py -> PYQExplain), audit_seam.py (ALLOW +1),
          SKILL.md + mocktestframework_SKILL.md (pip + scikit-image; read-receipt rule),
          .github/workflows/validate.yml (pip + scipy scikit-image)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together):  MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py                    -> [OK] FRAMEWORK 2026.11.02 VERIFIED
  python3 bootstrap.py --trigger TestCreate --receipt  -> one READ RECEIPT line per routed spec
  python3 run_ci_gates.py --skip Install  -> ALL GREEN (verified in the release environment before packaging)

Owner action outside the repo: the installed claude.ai skill's Step-0 pip line must add
`scikit-image` (same line as in SKILL.md). Step 5 uses it to MEASURE the exam's chemistry
drawing style from the PYQ pictures; without it nothing is measured, every paper draws with
the framework defaults (black-and-white, 10 pt) and the footer says "drawing style from
framework defaults". (The native drawing itself needs only rdkit.)

Per exam (once per exam, in this order):
  1. Re-run PYQExplain on the PYQ papers. Its delivered [ExamCode]_difficulty_profile.json
     now carries, per figural question, the content record (chemistry transcribed to SMILES
     -> content vectors for the content-complexity floor) and the ask-type / representation
     tags. Replace the profile in Project Files. (Ask-type tags travel in the difficulty
     profile, which is written only for exams with a 3-band difficulty vocabulary.)
  2. THEN re-run Step 5 (PYQExtract / MockTestAnalyse) with the PYQ docx files in the
     project, so section_rules.md gains the FIGURE_STYLE_PROFILE line and the ask /
     representation counts (read from the profile of step 1). Upload the new
     section_rules.md.
  3. Regenerate the scoped blueprints (ScopedBlueprint P[N] ...) and the mock blueprint
     (MockBlueprint) and upload them — they now carry difficulty_source and
     fig_ask_target_per_mock. An old SCOPED blueprint still runs UNCHANGED (its schedule
     cannot be recomputed — it records no provenance) with the footer line "difficulty
     schedule unverified"; regenerating it is the step that fixes the scoped schedule.
     The same holds for a full-mock blueprint built before Blueprint v1.57 (no
     difficulty_source). A blueprint built by this release that a run amends (S3-2D
     recompute, ladder R5) is delivered back with "Upload to Project Files" — upload that one.
  4. If the project has NO [ExamCode]_mock_test_audit.py, TestCreate uses the repo copy and
     delivers it — upload it to the project.
  Skipping 1-2 does not stop a run: DEFAULT_STYLE_PROFILE (black-and-white, 10 pt) is used and
  the footer discloses it; the content floor is skipped with a printed note.
  A project that OVERRIDES any changed spec in its Files section opts out of that spec's part
  of this fix (CLAUDE.md project-first); remove or update the override.
