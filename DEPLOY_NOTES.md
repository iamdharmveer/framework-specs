# Release 2026.08.03.5 — Audit steps removed (Steps 8 and 10)

## Deploy order (single atomic release — do not split)

Copy all 22 files below over your `production` working tree, then DELETE these two:

    Framework_MockTestCreateAudit.md
    Framework_MockTestExplainAudit.md

`check_triggers.py` fails CI on any partial landing, because routes.json,
both SKILL files and validate_framework_md.py's PIPELINE must move together.

## Post-push verification (fresh clone)

    git clone --depth 1 --branch production <repo> /tmp/verify && cd /tmp/verify
    python3 bootstrap.py          # expect: 2026.08.03.5 VERIFIED — 31/31 files
    python3 check_triggers.py     # expect: 20 user-facing triggers
    python3 audit_deep.py         # expect: findings: 0
    python3 audit_sync.py         # expect: 5 findings, ALL from the installed skill (below)

## REQUIRED MANUAL ACTION — the installed skill

`audit_sync.py` reads `/mnt/skills/user/mock-test-framework/SKILL.md`, NOT the repo copy.
Until you reinstall the skill from this release's `mocktestframework_SKILL.md`, every audit
run reports 4 TRIGGER-SYNC + 1 SKILL-INVENTORY findings naming the removed triggers.
The repo copy in this release is already correct.

## Before you push — check nothing is mid-audit

Any paper currently sitting in a `MockCreateAudit ... resume` / `status` or
`MockExplainAudit ... resume` / `status` state becomes unreachable the moment this lands.

## Backward compatibility (deliberate — do not "clean up")

- `Framework_MockDeliver.md` still ACCEPTS `_Explanation_Complete.docx` so papers produced
  by the old Step 10 still deliver. Nothing produces that filename any more.
- Existing `[ExamCode]_ExplainAuditLearnings.md` files stay valid, are still loaded and
  obeyed by Step 9, and may be extended by hand. Blueprint no longer generates new ones.
- Old registries certified by past Step-8 runs remain valid. No migration needed.

## Verification evidence from this build

    bootstrap.py            31/31 VERIFIED (run twice, .verified cleared between)
    check_triggers.py       CONSISTENT — 20 triggers
    audit_deep.py           findings: 0
    audit_callgraph.py      0 findings
    audit_mutation.py       30/30 killed, mutation score 100.0%
    audit_canonical.py      SELF-TEST: 175/175 PASS
    explain_engine.py       SELF-TEST: 62/62 PASS · AUDIT-SELF-TEST: 10/10 PASS
    explain_audit_gate.py   COMPLETION-SELF-TEST: 8/8 PASS
    validate_framework_md.py *.md   26 findings — EXACTLY the production baseline,
                                    zero new findings introduced by this release

## Accepted losses (requested, not oversights)

No step re-derives an answer, re-derives a subtopic_id, re-checks a figure, or runs a
completion gate over a mock or scoped paper. Step 7's gates and Step 9's §18 self-audit
are terminal. audit_canonical.py survives and still runs inside Step 7 (S3-10 / S4-11),
carrying the full A-* catalogue including the twelve A-FIG* figure gates.

## One change NOT made

Step 7's audit.py run was NOT promoted from OPTIONAL to MANDATORY — that is a new hard
stop and was not authorised. Instead a REPORTING duty was added: its absence must be
stated explicitly in the batch report. To promote it, change the S3-10 / S4-11 handling
in Framework_MockTestCreate.md from WARN to HARD STOP.
