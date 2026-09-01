# Deploy: GAP-2026-09-01-RECALL-CONTRACT — release 2026.09.01.1

**Files to commit (15):** `notes_core.py` (v2.12), `notes_docx.py` (v1.7),
`notes_audit.py` (v2.9), `notes_sync_audit.py` (v1.2),
`Framework_NotesCreate.md` (v2.9.0), `Framework_NotesAudit.md` (v3.7.0),
`Framework_NotesBlueprint.md` (v3.2.0 — §7 carry-over now an engine call),
`routes.json`, `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`docs/ACCEPTANCE_TEST.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`,
`SPEC_SECTIONS.json`. (`SHA256SUMS.txt` lists the release set for a
byte-check after upload.)

Deploy the engines after running each `--self-test` ON THE DEPLOYED BYTES:
notes_core 224, notes_docx 107, notes_audit 169, notes_sync_audit 19,
notes_blueprint 31 (unchanged). Then `python3 bootstrap.py` must print
`FRAMEWORK 2026.09.01.1 VERIFIED — 53/53`.

## Operator change: NONE for a unit already in flight

| Your unit's state | What happens |
|---|---|
| Drafted before this release, audited after it | NA G-14 reports `DORMANT — no recall_contract record`; every other gate is identical to v3.6.0; the unit certifies as before. Disclosed in the §9 chat line. |
| Drafted after this release | NC computes the Recall contract, authors to it, verifies every band on the shared rubric, writes `recall_contract` to the registry unit record; NA G-14 gates the shipped set. The rendered Recall box is byte-identical to before (Answer under the options; nothing new printed). |
| `[ExamCode]_difficulty_profile.json` absent from Files | Per-item bands still resolve from the bank; the exam-wide mix check is dormant; the chat line and footer say `difficulty profile absent — exam-wide mix check dormant`. No stop. |
| Profile present but the subtopic has no scored question in its window | The subtopic rung is skipped; the band resolves on the topic/exam/neutral rung and names it. No stop. |
| NotesBlueprint re-run after units were drafted / audited | `registry_carry_over` keeps state, draft_ref, final_ref, audit_summary and recall_contract on every surviving sid. Before this release a re-run reset them. |

**Routing change:** `blueprint_core.py` is now routed to NotesCreate,
NotesAudit and NotesDeliver because `notes_core` imports it (lazily) for the
shared difficulty rubric. The NotesDeliver route gains the file only so the
verified clone matches the import graph; ND calls none of the new functions.

## What this does NOT do (stated up front)

Difficulty is guaranteed in STRUCTURE — a Recall measures its band on the same
rubric as the real paper — not yet in OUTCOME. Student attempt data from the
portal is the only source of the latter; a later `NotesCalibrate` input can
feed it back. Trap-Box provenance is advisory (free-text). The ceiling and the
cumulative share are engine constants chosen on indirect research evidence and
are meant to be tuned from data, never re-typed into a spec.

---

# Deploy: GAP-2026-08-29-STYLE-FIDELITY (rev 2) — release 2026.08.31.2

**Files to commit (20):** `analyse_engine.py` (v2.56), `blueprint_core.py`,
`corpus_io.py`, `explain_engine.py` (v1.50.0), `paper_pipeline.py`,
`audit_canonical.py` (v2.26), `audit_seam.py` (v1.4), `mock_sync_audit.py`,
`spec_sections.py`, `Framework_MockTestAnalyse.md` (v2.56),
`Framework_MockTestCreate.md` (v5.82), `Framework_MockTestExplain.md` (v1.50.0),
`Framework_Blueprint.md` (v1.59.0), `Framework_MockDeliver.md` (v1.20.0),
`Framework_DeliveryFooter.md` (v1.30), `VERSION`, `CHANGELOG.md`,
`DEPLOY_NOTES.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`.

Deploy the engines after running each `--self-test` ON THE DEPLOYED BYTES:
analyse_engine 196, blueprint_core 651, corpus_io 381, explain_engine 193,
paper_pipeline 185, audit_canonical 336, mock_sync_audit 64, audit_seam 25.

## Operator change: NONE for a project already in flight

Nothing is required of you to deploy this. Every behaviour below is DORMANT
until you choose to regenerate an exam's Step 5.

| Your project's state | What happens |
|---|---|
| Release deployed, exam NOT regenerated | The two new artefacts are absent, so both report `DORMANT: absent`. Every step produces the same bytes as 2026.08.31.1 apart from ONE footer line: `STYLE PROFILE: DORMANT — absent`. Verified by execution (§8.6 proof 1). |
| Step 5 regenerated (3 files uploaded), OLD blueprint kept | Profile and index go ACTIVE. G-STYLE, G-PYQ-DIST and G-ITEM start recording. Axis-2 classes absent from the old schedule (IDENTIFY, SELECT_PLOT, RANK, widened STATEMENT) cannot be allocated and are recorded as `axis2_schedule_predates_profile`. |
| Step 5 AND blueprint regenerated | Fully active for the remaining mocks. Delivered mocks are never rewritten; `registry.papers_completed` is preserved, so the new blueprint schedules only what is left. |

**IIT_JAM_CHEMISTRY specifically:** Mocks 1-4 are delivered and are NOT touched,
re-audited or re-scored. To bring the style layer into Mock 5 onward, re-run
Step 5 for the exam and upload the three refreshed files
(`section_rules.md`, `style_profile.json`, `pyq_index.json`) before TestCreate P5.
If you would rather not, Mock 5 runs exactly as Mock 4 did.

## Known limitation, stated up front

A single-subject MCQ CONTENT exam with no mathematical notation and no NAT/MSQ
answer types — some LAW and COMMERCE papers — is classified `aptitude` and keeps
the v2.55 keyword table. That is precisely its v2.55 behaviour, so nothing
regresses; it simply does not yet gain the measured path. The exams that were
being actively harmed (science, engineering, medical — anything with notation or
NAT/MSQ) are all on the measured path. Widening the class test is a later,
separate change and is NOT smuggled into this release.

## What to watch after regenerating an exam

The S3-18 summary prints `STYLE PROFILE: ACTIVE (n=…, window=…)` or a DORMANT
reason, and `PYQ INDEX: <n> questions`. A `DORMANT: stale_profile` line names
both files and means one regeneration is out of step with the other — it is a
prompt, never a failure. All per-question style records live in the audit
dossier and `registry.style_gate`; NONE of it appears in a candidate's paper.

**Deploy all 20 files TOGETHER — a partial deploy is detected, not silent.**
Verified by extracting the bundle into a clean checkout: copying only the `.py`
and `.md` files while leaving `SPEC_SECTIONS.json` / `VERSION` behind makes
`audit_specs_ext` fail SPEC-BUDGET and `audit_sync` report a REL-SYNC finding
immediately. That is the designed behaviour — the manifests and VERSION are part
of the release, not bookkeeping — but it means a half-copied deploy shows up as
two red auditors rather than as a subtly wrong pipeline. Copy the whole set, then
run the self-tests listed above ON THE DEPLOYED BYTES.

**Rollback:** revert all 20 files together. The release is additive, so a
rollback loses the style layer and nothing else; artefacts left in Project Files
are simply ignored by the older code.

---

# Deploy: GAP-2026-08-30-LINEART-CLASSIFIER — release 2026.08.30.3

**Files to commit (8):** `corpus_io.py` (v1.15), `Framework_PYQCompress.md` (v2.0.1), `VERSION`,
`CHANGELOG.md`, `DEPLOY_NOTES.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`.
Deploy the engine after `python3 corpus_io.py --self-test` (376/376) on the deployed bytes.

**Operator change: NONE.** Behaviour change: from this release a PYQSort / PYQCompress pass keeps
rendered figures as PNG (they were JPEG-encoded unless RGBA). Already-JPEG sources and alpha images
route exactly as before. Delivered documents are not re-processed.

**Rollback:** revert the two content files.

---

# Deploy: GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3) — release 2026.08.30.2

**Files to commit (11):** `notes_core.py` (v2.11), `notes_audit.py` (v2.8), `notes_sync_audit.py`
(v1.1), `Framework_NotesCreate.md` (v2.8.0), `Framework_NotesAudit.md` (v3.6.0), `VERSION`,
`CHANGELOG.md`, `DEPLOY_NOTES.md`, `MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`.
Deploy the engines on this explicit instruction only, after `python3 notes_core.py --self-test`
(194/194), `python3 notes_audit.py --self-test` (140/140) and `python3 notes_sync_audit.py
--self-test` (19/19) pass on the deployed bytes.

**Operator change (all ~200 exams): NONE.** No project file edit. Existing notes units keep
their figures; NA never re-renders for colour; only units drafted from NotesCreate v2.8.0 use F-4a.

**What you will SEE:** NotesCreate figures drawn to the F-4a recipe (pinned palette, 300 dpi);
NA's G-7a line carries a figure_palette advisory (count only) on every unit.

**Rollback:** revert the five content files.

---

# Deploy: GAP-2026-08-30-EXPLAIN-COLOUR-BINDING (P2) — release 2026.08.30.1

**Files to commit (10):** `explain_engine.py` (v2.11), `Framework_MockTestExplain.md` (v1.49.0),
`Framework_PYQExplain.md` (v2.21), `routes.json`, `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`. Deploy the engine on this explicit
instruction only, after `python3 explain_engine.py --self-test` (184/184) on the deployed bytes.

**Operator change (all ~200 exams): NONE.** The per-exam explain_engine copies are inert
(engines run from the verified clone).

**What changes:** from this release, a TestExplain / MockExplain / PYQExplain session renders
every explanation figure with figural_core's constants (pinned atom palette, role palette,
300 dpi) and records `colour_contract()['available']` on the preflight dashboard line.
Nothing else in Step 9 / PYQ-1 changes; delivered solutions are not re-rendered.

**Rollback:** revert the four content files.

---

# Deploy: GAP-2026-08-30-FITTER-ASPECT — release 2026.08.30

**Files to commit (9):** `figural_core.py`, `audit_canonical.py` (v2.25),
`Framework_MockTestCreate.md` (v5.81), `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json`. Deploy the engines only on this
explicit instruction, after `python3 figural_core.py --self-test` (171/171) and
`python3 audit_canonical.py --self-test` (317/317) pass on the deployed bytes.

**Operator change (all ~200 exams): NONE.** No project file, exam_config or section_rules edit.
The per-exam `[ExamCode]_mock_test_audit.py` copies are inert (engines run from the verified
clone); Step 6 of the next Blueprint refreshes them from this audit_canonical as usual.

**What you will SEE from this release on:** (1) data charts fill their frame; (2) Step 8 prints
24 figure-gate lines instead of 13 — expect previously-hidden G-FIGFIT / G-FIGCOLLIDE /
G-FIGINK findings on papers that had them (delivered Mock02: one A-FIGINK FAIL on Q7); the
16 false "0.050 below 0.050" G-FIGFIT findings disappear.

**Rollback:** revert the three files.

---

# Deploy: GAP-2026-08-29-FIGURE-COLOUR-ROLES — release 2026.08.29.1

**Files to commit (9):** `figural_core.py`, `corpus_io.py` (v1.14),
`Framework_MockTestCreate.md` (v5.80), `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json` (its read-set line ranges
moved with the spec edit, so it is regenerated and shipped). Two engines and one spec
changed.
Engines are NOT `Framework_*.md`: deploy them on this explicit instruction only, after
`python3 figural_core.py --self-test` (163/163) and `python3 corpus_io.py --self-test`
(362/362) pass on the deployed bytes.

**Operator change (all ~200 exams): NONE.** No project file, no exam_config, no
section_rules change anywhere. `exam_config.figure_palette` was never wired and is now
formally closed; an exam_config that carries the key is ignored, never an error.

**What a Step 7 run does differently from this release on:** structures draw atoms from
figural_core.ATOM_PALETTE (O #C25604, N #0072B2, halogens #158663, everything else
black) instead of rdkit's default; an option set with divergent heteroatom sets renders
all-black automatically; a stem/option that interrogates a colour renders monochrome;
`fc.text_ink()` / `fc.fill_style()` are the authoring calls for coloured text and fills;
new sidecars carry `colour_profile: 2`. Nothing else in the render, layout, sidecar
schema, registry or footer changes.

**What does NOT change:** every delivered paper; every PYQ step (corpus_io reads the
palette from `sys.modules` and never imports figural_core — validator check AI proves the
declared dependency sets are unchanged); Explain and Notes figures (separate GAPs, P2/P3);
audit_canonical (unchanged — see CHANGELOG "KNOWN, NOT TOUCHED": the new gates are silent
at Step 8 until the figure-gate emission GAP lands).

**Rollback:** revert the three files; a sidecar written at v5.80 carries `colour_profile`
which v5.79 ignores.

---

# Deploy: GAP-2026-08-29-DIFFICULTY-HARDER-PRESET + GAP-2026-08-29-PROFILE-UNSCORED-QUESTIONS — release 2026.08.29

**Files to commit (10):** `blueprint_core.py`, `audit_canonical.py` (v2.24),
`Framework_Blueprint.md` (v1.58.0), `Framework_PYQExplain.md` (v2.20),
`Framework_MockDeliver.md` (v1.19.0), `VERSION`, `CHANGELOG.md`, `DEPLOY_NOTES.md`,
`MANIFEST.json`, `SPEC_MANIFEST.json`. (`SPEC_SECTIONS.json` is regenerated and committed
only if its bytes changed — see the gate output.) Two engines and three specs changed. See
CHANGELOG 2026.08.29.

**Operator change (all ~200 exams): NONE.** No project file, no exam_config, no
section_rules change anywhere. Every existing `[ExamCode]_difficulty_profile.json` and
`blueprint.json` reads unchanged. The two IIT JAM papers excluded under the old rule are
NOT re-ingested by this release; from the next PYQExplain run onward, a paper with
unanswered questions is added with those questions listed as unscored.

**What operators see:** at MockBlueprint S7-0 the table shows two rows per section —
"Exam (measured)" and bold "Ours (+30% harder)" — each cell "pct% (nQ)"; per-sitting rows
carry "scored/held"; the preset's editable lines are printed; OK applies the preset,
EXAM the measured mix. The delivery footer names the preset.

**Deploy order:** commit all files together in one commit. bootstrap.py verifies sha256
against MANIFEST.json at every session's Step 0 — a partial deploy HALTS every future
session at verification. Both manifests were regenerated by the repo's own generators
(gen_manifest.py, build_spec_manifest.py) after the edits. Run the engine self-tests
before pushing: `python3 blueprint_core.py --self-test` (633/633) and
`python3 audit_canonical.py --self-test` (312/312).
