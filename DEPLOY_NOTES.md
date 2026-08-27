# Deploy: REPAIR-RETIRED-2026-08-27 — release 2026.08.27.3

**Files to commit (18):** `paper_pipeline.py` (v5.76), `blueprint_core.py`, `audit_canonical.py`
(v2.22), `final_assembly.py`, `mock_sync_audit.py` (MS-15), `validate_framework_md.py`,
`routes.json`, `SKILL.md`, `mocktestframework_SKILL.md`, `Framework_MockTestCreate.md` (v5.76),
`Framework_MockTestExplain.md` (v1.47.0), `Framework_MockDeliver.md` (v1.18.0),
`Framework_DeliveryFooter.md` (v1.29), `SPEC_HISTORY.md`, `VERSION`, `CHANGELOG.md`,
`DEPLOY_NOTES.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`. See CHANGELOG
2026.08.27.3.

**Operator change (all ~200 exams):** the four triggers `TestCreateRepair`, `MockCreateRepair`,
`TestExplainRepair`, `MockExplainRepair` no longer exist. The difficulty gate at Step 9 still
measures every paper, but it now DISCLOSES instead of blocking: after `TestExplain P[N]` the
next step is ALWAYS `TestDeliver P[N]` (or the Mock alias). A paper whose gate was not met is
delivered with one extra footer line stating the measured band counts. PENDING (Step 9 never
ran, or its registry was not replaced in Project Files) is the only thing Step 11 still refuses.

**Estate action after deploy (once, per project):** any registry still carrying a FAILED
gate record heals automatically the next time TestExplain or TestDeliver reads it (the heal is
printed in chat and in the footer). To heal every project in one pass instead:
`python3 final_assembly.py --dg-fleet-scan <root-with-project-dirs> --apply`.
Papers already repaired by the retired steps (PASSED/1, DISCLOSED/1) are untouched and deliver.
A previously repaired paper whose file is named `…_Create_Repaired.docx` must be renamed to
`…_Create.docx` before it is attached to TestExplain again (S2-1 refuses the retired name).

**Rollback:** revert the commit. No artefact of any step changed shape; the 12-artefact Step 5
golden set (IIT_JAM_MATHEMATICS + IIT_JAM_CHEMISTRY) was byte-identical before and after.
