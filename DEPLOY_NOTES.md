# DEPLOY NOTES — release 2026.12.04 (GAP-2026-11-26-RENDER-PARITY, Release 1 "print integrity") over release 2026.12.03
Deploy ONLY over release 2026.12.03 (production HEAD 2f2bda4). Upload EVERY file below in ONE commit, flat (no folders);
push main, then main:production. A partial upload fails bootstrap for every exam (MANIFEST.json / SPEC_MANIFEST.json /
SPEC_SECTIONS.json hash every engine and spec).
Before uploading: production must be exactly the 2026.12.03 bundle (`cat VERSION` -> 2026.12.03). If anything else
changed, stop — the bundle must be rebuilt on it.

WHAT IT DOES (no new hard stop, loop, review round, sub-agent, deliverable or end state):
- ONE RECORD, ONE PRINTER: a stem with a labelled series (statements, conditions, data lines) is recorded structured
  (bc.stem_record); every question is printed from its record by render_from_record (Create S10-8A). Picture questions
  now print their statement lines (after the picture by default; before it where Step 5 measured that), labels under
  pictured items ('I', 'II'), and pictures inside List-I cells. A question printed the old way prints byte-identically.
- ONE CHECK (G-RENDER-PARITY): STEP B writes the printed blocks (--item-texts); STEP A2 sends a block that does not show
  its reviewed record back to the writer BEFORE any reviewer is paid; STEP A3 inserts a reviewed sentence that is still
  missing (after the picture, before the options) and discloses it — the paper is always answerable.
- DISCLOSURE: the new lines appear in the chat delivery footer and in the registry's chain footer — never on the paper.
  Delivery is still exactly two files (owner ruling 2026-11-26).
- STEP 5: section_rules gains 'stem_lines_position' per section (measured; absent on old section_rules = after the
  picture). Re-running Step 5 is NOT required; do it when convenient to switch an exam to its measured position
  (CSIR Life Sciences measured: before the picture).
- READ: the TestCreate / MockCreate worker read grows +1,710 B (~740 tokens), inside the 2,300 B tolerance.

IN-PROGRESS PAPERS: resume with `continue`. Questions already bound keep their binding and are never repaired; only
questions not yet bound get the new check.

UPLOAD LIST (22 files):
CHANGELOG.md                       (2026.12.04 entry)
DEPLOY_NOTES.md                    (this file)
Framework_DeliveryFooter.md        (v1.58.0 — G-RENDER-PARITY footer lines)
Framework_MockTestAnalyse.md       (v2.67.0 — stem_lines_position; stamps v2.67)
Framework_MockTestCreate.md        (v8.11)
LAW_REGISTRY.json                  (NEW LAW-PRINT-1; LAW-BC-5 / LAW-BC-7 amended)
MANIFEST.json                      (regenerated)
SHA256SUMS.txt                     (this bundle)
SKILL.md                           (engine inventory: 19 routed / 8 never-routed)
SPEC_HISTORY.md                    (Create entry v8.10 moved)
SPEC_MANIFEST.json                 (regenerated)
SPEC_SECTIONS.json                 (regenerated)
VERSION                            (2026.12.04)
analyse_engine.py                  (v1.9)
audit_canonical.py                 (v2.48)
audit_sync.py                      (RPAR-SYNC)
blueprint_core.py                  (v2.14)
corpus_io.py                       (v1.22)
final_assembly.py                  (v1.30.0)
handshake_audit.py                 (H5-RPAR, H-RPAR)
mocktestframework_SKILL.md         (same inventory line as SKILL.md)
routes.json                        (audit_canonical.py routed to MockCreate / TestCreate — final_assembly imports it)

AFTER DEPLOY: fresh clone of production; `cat VERSION` -> 2026.12.04; `sha256sum -c SHA256SUMS.txt` passes;
`python3 bootstrap.py` exits 0. Then the live bench: TestCreate CSIR_NET_CHEMICAL_SCIENCES Organic Chemistry 01, and
one exam with figure statement sets in another subject.
