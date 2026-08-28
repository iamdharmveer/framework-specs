# Deploy: GAP-2026-08-28-PLACEMENT-UNSPECIFIED — release 2026.08.28.1

**Files to commit (12):** `blueprint_core.py` (+Cluster Q), `audit_canonical.py` (v2.23),
`figural_core.py` (+rdkit), `Framework_MockTestCreate.md` (v5.77), `SKILL.md`,
`mocktestframework_SKILL.md`, `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`. See CHANGELOG 2026.08.28.1.

**Operator change (all ~200 exams): NONE.** The placement plan is built, gated,
persisted and audited automatically. `TestCreate P[N]` / `continue` behave exactly as
before from the operator's seat; the only new visible lines are S3-12b NOTICEs (when a
blueprint makes some adjacency mathematically unavoidable, with the MockBlueprint
remedy named) and per-batch audit output that now reads `RESULT: PASS` on healthy
intermediate batches instead of six structural FAILs.

**Estate action after deploy: none required.** Delivered papers are untouched.
Mid-flight papers (batches_completed non-empty) resume on a FROZEN plan: a pre-fix
paper's AUTHORED questions are frozen from the answer_key concept_map, the un-authored
remainder of each section is placed fresh into its remaining contiguous range, and the
whole map is audited with `bc.audit_placement` — old blueprint-order violations are
DISCLOSED as a §R13 limitation, never re-placed; the only resume HARD STOPs are
artefact-consistency faults (answer_key vs batch_state vs blueprint disagreeing). Optionally, re-running the auditor
with `--registry` over an existing project reports historical A-CLUSTER findings on
completed papers; those are information about what shipped, not a regression
(recommendation: treat retroactive findings as WARN-grade context only).

**The regression test for the whole gap:** A-CLUSTER FAILs the shipped
`IIT_JAM_CHEMISTRY_Mock02_Q1to20.docx` answer-key shape (names Q.2 and Q.3, quotes the
achievable floor 0) and PASSes the shipped hand-repaired `MOCK:M01` registry (one
truthful WARN: Section B's subject run of 4 — a secondary objective, not an R19 rule).

**Known deferrals:** GAP-2026-08-28-DIFFICULTY-FIGURAL-BLIND (moves the Axis-1 grant
pass; own release) and the `\mathrm` S3-5b grammar-table note (doc-only, loud failure,
lives in Framework_PYQPrepare).

**Rollback:** revert the commit. No artefact of any step changed shape; a fresh paper
generated pre- and post-fix differs ONLY in question ordering within sections (the
entire point), and `continue`/resume on the same version is byte-deterministic.
