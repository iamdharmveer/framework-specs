# Deploy: GAP-2026-08-28-STEP7-SUBJECT-LEARNINGS-SEAM — release 2026.08.28.3

**Files to commit (7):** `Framework_MockTestCreate.md` (v5.78), `VERSION`,
`CHANGELOG.md`, `DEPLOY_NOTES.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`,
`SPEC_SECTIONS.json`. One spec section changed (S3-1 staging + S3-3 load): the SUBJECT
file is resolved by the 2026.08.28.2 discovery helper (explain_engine.py is already
on the TestCreate/MockCreate route); the EXAM side keeps the exact v5.56 family glob
untouched. No engine changed. See CHANGELOG 2026.08.28.3.

**Operator change (all ~200 exams): NONE.** The v5.77 "rename it {EXAM}_..." WARN is
gone; a project's subject library is discovered and staged automatically. New visible
line: "S3-3 — learnings loaded for authoring bans: <files> (<n> marker(s))".

**Estate action after deploy: none.** No artefact changes shape. Any exam whose
subject library carries no BANNED:/VERIFIED DEFECT: markers authors byte-identically
to v5.77 (measured on the reporting project: 0 markers). Projects that already
created an exam-prefixed COPY of their subject library should delete the copy (same
guidance as 2026.08.28.2 — the S24 highest-version collision hazard).

**Acceptance evidence:** full validator batch 0 issues across 23 specs (incl. the new
S3 code blocks under Checks B/F/H and check_aj); Check V 0 findings; audit_seam 0
findings / 25 self-test; audit_deep, audit_sync, audit_callgraph, audit_specs_ext,
mock_sync_audit, spec_name_audit baseline, check_triggers all green; behavioral
simulation of the new path verified on four project shapes (exam-only, subject-only,
exam+subject, ambiguous-abstain).

**Note for operators reading pre-2026.08.28.2 end-of-mock reports:** carried standing
items claiming "representation_renderers absent from section_rules ... needs an
upstream PYQExtract change" are STALE — that read was retired by 2026.08.28.2; nothing
consumes the key. Disregard, and drop the item from the next report.

**Rollback:** revert the commit. Resolution returns to the v5.77 glob + rename WARN;
nothing else is affected.

---

# Deploy: GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ — release 2026.08.28.2

**Files to commit (11):** `explain_engine.py` (v2.10), `Framework_MockTestExplain.md`
(v1.48.0), `Framework_PYQExplain.md` (v2.19), `audit_seam.py` (v1.3),
`validate_framework_md.py` (v3.2), `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json` (both Explain specs grew,
so their section line spans moved; all three manifests machine-regenerated with the
repo's own generators, never hand-edited). See CHANGELOG 2026.08.28.2.

**NOT touched — this is the release's central property:** `analyse_engine.py` and
`write_section_rules()` are byte-identical; `Framework_MockTestAnalyse.md` §14 is
unchanged; **no `section_rules.md` anywhere in the estate changes and no exam is
regenerated.** Every exam — including mid-series exams that cannot safely
re-synthesise — is fixed on its next TestExplain / MockExplain / PYQExplain run after
the repo updates.

**Operator change (all ~200 exams): NONE.** Renderer bindings are framework-owned
(explain_engine.REPRESENTATION_RENDERERS); the subject learnings library is found by
discovery. New visible lines only: the P2/P7 dashboards' "Renderer preflight" entry
now reports per-requirement availability from the constant, and "Learnings loaded"
names the subject file and its rule count (or none / AMBIGUOUS(n)).

**Estate action after deploy: one per-project cleanup where the workaround exists.**
Any project that copied its subject library to an exam-prefixed name as a workaround
(e.g. `IIT_JAM_CHEMISTRY_EXPLAIN_LEARNINGS_v2.md` duplicating
`CHEMISTRY_EXPLAIN_LEARNINGS_v2.md`) must DELETE the duplicate after this release:
under §24's highest-version-wins rule the exam-prefixed v2 outranks the genuine
exam-level v1, so subject content would masquerade as exam content.

**Acceptance evidence (measured on this release):** Check V — 3 ORPHAN-CONFIG-READ
findings on the pre-fix corpus, 0 on this corpus, 9/9 self-test fixtures (incl. gate-
fires-on-reintroduction and abstain-on-producer-rename); audit_seam v1.3 — same
3 findings pre-fix, 0 post-fix, 25/25 self-test; explain_engine 179/179 (V30 fixtures
fail the build if REPRESENTATION_RENDERERS loses a requirement or its §6A-5 shape);
full validator batch 0 issues across 23 specs; audit_deep / audit_sync /
audit_callgraph / mock_sync_audit / notes_sync_audit / spec_name_audit baseline /
check_triggers / audit_specs_ext all green.

**Non-scientific exams:** byte-identical behaviour — §6A-1's router never reaches a
visual verdict there; the constant is inert by construction (criterion 9).

**Rollback:** revert the commit. No artefact of any step changed shape; the fix's
effects appear only at the next Explain run.

---

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
