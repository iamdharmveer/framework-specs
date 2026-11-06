# DEPLOY NOTES — release 2026.11.06 (GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY)
Over verified production 030fa56 (2026.11.05); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (44 files = every file that differs from production; 2 are NEW):
CHANGELOG.md
CLAUDE.md
DEPLOY_NOTES.md
Framework_Blueprint.md
Framework_DeliveryFooter.md
Framework_MockDeliver.md
Framework_MockReview.md
Framework_MockTestAnalyse.md
Framework_MockTestCreate.md
Framework_MockTestExplain.md
Framework_MockTestOrchestrate.md        (NEW)
Framework_NotesAudit.md
Framework_NotesBlueprint.md
Framework_NotesCreate.md
Framework_NotesDeliver.md
Framework_PYQApprove.md
Framework_PYQCompress.md
Framework_PYQCore.md
Framework_PYQCount.md
Framework_PYQDeliver.md
Framework_PYQDraft.md
Framework_PYQExplain.md
Framework_PYQFormat.md
Framework_PYQPrepare.md
Framework_PYQScan.md
Framework_PYQSort.md
Framework_ScopedBlueprint.md
LAW_REGISTRY.json
MANIFEST.json
SESSION_BUDGET.json                     (NEW)
SHA256SUMS.txt
SKILL.md
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
STEP_CONTRACTS.json
VERSION
audit_specs_ext.py
bootstrap.py
gen_manifest.py
mocktestframework_SKILL.md
routes.json
spec_sections.py
spec_source.py

(Framework_MockTestExplain is v1.53.1: one Step 9 intake instruction corrected, see CHANGELOG.
20 of the specs change only by the history move — superseded header entries moved verbatim to
SPEC_HISTORY.md, no version change.)

RE-INSTALL THE SKILL IN EVERY ACCOUNT: upload the new SKILL.md as the mock-test-framework skill in each Claude account that runs exams.
NEW STEP 0 STEP: when bootstrap prints SURFACE (no /mnt/project), the chat runs `python3 bootstrap.py --stage-inputs` and follows it before reading any spec.

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.06 VERIFIED — 59/59
  python3 bootstrap.py --self-test         -> SELF-TEST: 68/68 PASS
  python3 spec_sections.py --self-test     -> SELF-TEST: 33/33 PASS
  python3 audit_specs_ext.py Framework_*.md *.py   -> 0 issues (SPEC-CAPACITY included)
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 79 ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues across 25 file(s)
  python3 audit_sync.py                    -> findings: 0
  sha256sum -c SHA256SUMS.txt              -> every line OK
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

No trigger, deliverable, end state, badge or user action changes (STEP_CONTRACTS deliverables /
end states / user actions unchanged; MS-27 green).

WHAT THE OPERATOR SEES (every exam — no per-exam action required):
  * TestCreate / MockCreate: the chat prints `STEP 7 MODE: WORKER` and works through helper
    sub-agents; each batch still ends with the cumulative docx and "Type 'continue'", and the
    paper still ends with exactly the Create docx + the registry. The chat stays short.
  * Every step: specs are read in numbered chunks and the session proves it still holds them.
    If a model cannot hold the Step 7 specification, the run stops with MODEL-CAPACITY and asks
    for a larger-context model; the paper resumes from its saved state on "continue".
  * Surfaces without /mnt/project: Step 0 prints SURFACE and stages the project's files first.
