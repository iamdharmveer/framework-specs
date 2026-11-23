# DEPLOY NOTES — release 2026.11.29 (GAP-2026-11-22 MATH-LENIENT / MATH-READ / FAMILY-LEVERS) over release 2026.11.28
Built on production 09c320d (release 2026.11.28). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for every exam
(MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production has any content change beyond 09c320d when you deploy (git diff 09c320d production not empty), stop —
the bundle must be rebuilt on the new production commit.

UPLOAD LIST (the files that differ from 2026.11.28, plus DEPLOY_NOTES.md and SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                  (this file)
Framework_MockTestAnalyse.md     (v2.66.0 — readable past-paper equations for non-chemistry exams; STRUCT-LOSS line)
Framework_MockTestCreate.md      (v8.8 — lenient maths render, A-RAWTEX WARN, G-MATH-COMPILE soft, EC-15 keeps the
                                  planned format, apply_lever in the rewrite brief)
Framework_MockTestExplain.md     (v1.56.0 — a maths spelling never stops Step 9; repaired regions listed AMBER)
Framework_PYQExplain.md          (v2.34 — same, PYQ-1)
Framework_PYQPrepare.md          (v2.3.0 — S3-5b compiler v2.2, byte-identical with t3_mathcomp.py)
LAW_REGISTRY.json                (LAW-NF-4 amended: per-family lever lists)
MANIFEST.json                    (regenerated)
SHA256SUMS.txt                   (checksums of this upload)
SPEC_MANIFEST.json               (regenerated)
SPEC_SECTIONS.json               (regenerated)
STEP_CONTRACTS.json              (floors: Create 8.8, PYQExplain 2.34, MockTestExplain 1.56.0, MockTestAnalyse 2.66.0,
                                  PYQPrepare 2.3.0)
VERSION                          (2026.11.29)
analyse_engine.py                (v1.8 — pyq_omml / auto_pyq_reader / STRUCT-LOSS; stamps v2.66)
audit_canonical.py               (A-AXIS2 compares one format vocabulary for recognised non-chemistry subjects)
blueprint_core.py                (omml_read, math_linear reads what the candidate sees, subject_family, family levers,
                                  G-MATH-COMPILE, install_t3; self-test 1635)
explain_engine.py                (v2.16 — lenient render, validate() records instead of raising; self-test 448)
final_assembly.py                (installs the compiler for blueprint_core; fa_release stamp; A3 reading lenient;
                                  subject for the rewrite step; self-test 267)
notes_docx.py                    (lenient render — a notes build never crashes on a maths spelling)
spec_name_audit_baseline.json    (PYQPrepare forward reference t3_compile -> t3_compile_lenient)
t3_mathcomp.py                   (v2.2 — t3_compile_lenient, t3_normalize, t3_plain, t3_repair_lines)

NOT CHANGED: Framework_Blueprint.md, Framework_ScopedBlueprint.md, the difficulty ladder (40/35/25 cuts), the
"+30% harder" preset and the CONFIRM override. SKILL / TRIGGERS / ROUTES unchanged.

AFTER DEPLOY — ONCE PER NON-CHEMISTRY EXAM (no change to how a paper runs):
  1. Run Step 5 (PYQExtract) for the exam: past-question equations are re-read with the new reader (a STRUCT-LOSS line
     is printed per paper), the ladder refits through the existing pyq_sha rule (unchanged packets keep their
     orderings).
  2. Upload the new [ExamCode]_difficulty_ladder.json (and the Step 5 run files it delivers) to the project, replacing
     the old ones. Start with CSIR NET Mathematical Sciences.
  Chemistry-only exams need nothing. The project "RC - Maths" is over its knowledge limit (2,074,221 / 2,000,000
  bytes): remove CSIR_NET_MATHEMATICAL_SCIENCES_PYQ_Analysis.docx and _PYQ_Frequency.xlsx from project knowledge first.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.11.29, 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.28 files (production 09c320d) together. A ladder refit on readable text stays valid
on rollback (the ladder file format is unchanged); a rolled-back Step 5 re-reads equations the old way.
