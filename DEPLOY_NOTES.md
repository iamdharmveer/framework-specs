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
