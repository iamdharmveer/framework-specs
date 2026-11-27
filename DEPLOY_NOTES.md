# DEPLOY NOTES — release 2026.12.05 (GAP-2026-11-27-ATTACHMENT-INPUT-LANE, INPUT-SOURCE-LAW) over release 2026.12.04
Deploy ONLY over release 2026.12.04 (production HEAD 2483723). Upload EVERY file below in ONE commit, flat (no folders);
push main, then main:production. A partial upload fails bootstrap for every exam (MANIFEST.json / SPEC_MANIFEST.json /
SPEC_SECTIONS.json hash every engine and spec).
Before uploading: production must be exactly the 2026.12.04 bundle (`cat VERSION` -> 2026.12.04). If anything else
changed, stop — the bundle must be rebuilt on it.

WHAT IT DOES (no new deliverable, end state, loop, review round or sub-agent):
- Every step reads its exam inputs from ONE folder, /tmp/fw_inputs, built by the new engine input_tray.py: everything in
  Project Files PLUS every file attached to the trigger in chat (the random 8-character upload prefix removed).
- A file in both places: the chat attachment is used (the step says the two differ). The same file attached twice: the
  newest is used. A broken attached file (empty, not valid JSON, ...) is never used, and the Files copy is never used
  in its place — the step stops and names it.
- Every missing input is named in ONE stop (before: one stop per file). A renamed browser copy ('X (1).json') is named.
- Spec files are unchanged: GitHub, or a Framework_*.md in Project Files, as before. An attached spec is ignored.
- Also fixed: TestDeliver could not read the paper name from a prefixed upload; ScopedBlueprint's old-registry migration
  wrote into the read-only Files folder.
- Guard: mock_sync_audit MS-28 fails the build if any spec or engine ever reads an input from Project Files only again.
- READ: each step's spec read grows by at most +1,427 B (~620 tokens); every route stays inside the 2,300 B tolerance.

OPERATOR: inputs may be in Project Files OR attached in chat, for all 23 steps. A new chat needs its attachments again.
Test steps read: TestCreate — section_rules.md, subtopic_manifest.json, blueprint.json, registry.json,
stimulus_profile.json (new paper), exam_config.json (+ optional difficulty_profile, style_profile, pyq_index,
exemplar_bank, difficulty_ladder, fig_manifest, mock_test_audit.py, EXPLAIN_LEARNINGS_v1.md); TestExplain — the Create
.docx, section_rules.md, blueprint.json, subtopic_manifest.json, registry.json (+ EXPLAIN_LEARNINGS_v1.md,
exam_config.json); TestDeliver — the Explanation .docx, blueprint.json, registry.json.

IN-PROGRESS PAPERS: resume with `continue`. Nothing about a paper already started changes.

UPLOAD LIST (40 files):
CHANGELOG.md                       (2026.12.05 entry)
CLAUDE.md                          (INPUT-SOURCE LAW; counts 61 / 62)
DEPLOY_NOTES.md                    (this file)
Framework_Blueprint.md             (v1.66.1)
Framework_DeliveryFooter.md        (v1.58.1)
Framework_MockDeliver.md           (v1.29.0)
Framework_MockTestAnalyse.md       (v2.67.1)
Framework_MockTestCreate.md        (v8.12)
Framework_MockTestExplain.md       (v1.57.0)
Framework_MockTestOrchestrate.md   (v1.16.1)
Framework_NotesCreate.md           (v2.11.1)
Framework_PYQDeliver.md            (v1.13.3)
Framework_PYQExplain.md            (v2.35)
Framework_PYQFormat.md             (v1.6.2)
Framework_PYQScan.md               (v1.6.2)
Framework_PYQSort.md               (v1.21.2)
Framework_ScopedBlueprint.md       (v1.17.0)
LAW_REGISTRY.json                  (NEW INPUT-SOURCE-LAW; REGISTRY-SOURCE-LAW lane 1 text)
MANIFEST.json                      (regenerated)
SESSION_BUDGET.json                (project_inputs: Test/MockExplain, Test/MockDeliver added)
SHA256SUMS.txt                     (this bundle)
SKILL.md                           (Step 0 builds the input folder; rule 3; 20 routed engines)
SPEC_HISTORY.md                    (Create entry v8.11 moved)
SPEC_MANIFEST.json                 (regenerated; input_tray.py entry)
SPEC_SECTIONS.json                 (regenerated)
VERSION                            (2026.12.05)
analyse_engine.py                  (input folder first in two exact-name lookups)
audit_canonical.py                 (P10 fixture follows the folder)
audit_specs_ext.py                 (SPEC-CAPACITY counts input-folder reads)
audit_sync.py                      (detect rule input_source_read)
corpus_io.py                       (default lanes: Files + input folder)
final_assembly.py                  (blueprint / ladder from the folder)
frequency_xlsx.py                  (exam_config: folder first)
gen_manifest.py                    (tracks input_tray.py)
handshake_audit.py                 (relocates the folder onto the fixture project)
input_tray.py                      (NEW — v1.0)
mock_sync_audit.py                 (NEW MS-28 INPUT-SOURCE; MS-20 widened)
mocktestframework_SKILL.md         (same as SKILL.md)
paper_pipeline.py                  (registry lane 1 = the folder's attachment view)
routes.json                        (input_tray.py routed to all 23 triggers)

AFTER DEPLOY: fresh clone of production; `cat VERSION` -> 2026.12.05; `sha256sum -c SHA256SUMS.txt` passes;
`python3 bootstrap.py` exits 0 (61/61). Replace the installed Claude Skill's SKILL.md with this SKILL.md (optional for
the fix — every step builds the folder itself — but it makes Step 0 print the input report). Then the live bench:
MockCreate M2 for CSIR_NET_CHEMICALSCIENCES with the inputs attached in chat.
