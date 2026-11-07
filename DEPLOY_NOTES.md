# DEPLOY NOTES — release 2026.11.07 (GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS — RE-25 CHEM-STRUCTURE)
Over verified production 50c2690 (2026.11.06); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (20 files = every file that differs from production; 1 is NEW):
CHANGELOG.md
CHEMISTRY_EXPLAIN_LEARNINGS_v1.md       (NEW — the chemistry subject library, tracked + routed)
CLAUDE.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.41.0)
Framework_MockTestExplain.md            (v1.54.0)
Framework_PYQExplain.md                 (v2.28)
LAW_REGISTRY.json
MANIFEST.json
SHA256SUMS.txt
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
VERSION
audit_sync.py
corpus_io.py                            (v1.19)
explain_engine.py                       (v2.13)
figural_core.py                         (v5.91)
gen_manifest.py
routes.json

No trigger, deliverable, end state, badge or user action changes (STEP_CONTRACTS.json unchanged;
check_triggers 23/23; MS-27 green). SKILL.md is unchanged — no skill re-install is needed.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.07 VERIFIED — 60/60
  python3 bootstrap.py --self-test         -> SELF-TEST: N/N PASS
  python3 spec_sections.py --self-test     -> SELF-TEST: N/N PASS
  python3 explain_engine.py --self-test    -> SELF-TEST: N/N PASS (the CHS-* fixtures are in it)
  python3 explain_engine.py --self-test-audit -> AUDIT-SELF-TEST: N/N PASS
  python3 corpus_io.py --self-test         -> SELF-TEST: N/N PASS (the chs_* fixtures render Q.73)
  python3 figural_core.py --self-test      -> SELF-TEST: N/N PASS
  python3 audit_specs_ext.py Framework_*.md *.py   -> 0 issues (SPEC-CAPACITY included)
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: N ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues across 25 file(s)
  python3 audit_sync.py                    -> findings: 0  (CHEM-STRUCTURE-LAW governs both explain specs)
  sha256sum -c SHA256SUMS.txt              -> every line OK
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

WHAT THE OPERATOR SEES (every exam — no per-exam action required):
  * PYQExplain / TestExplain / MockExplain on a paper WITH chemistry-structure questions: each
    such question (decided from its content, never from the exam or topic name) is explained with
    drawn, proved, step-by-step figures — one per step inside DEDUCTION, one under each wrong
    Option / pitfall value, at most one under SPEED HACK. No new section headings. The chat views
    one contact sheet of figures per batch (the recorded E-09 review) and §R3 prints the
    CHEM-STRUCTURE ledger. A printed option that differs from the derived product is disclosed in
    the last DEDUCTION paragraph (PYQ) or raised as a Step 7 defect (mock).
  * Every other question and every exam with no chemistry content: unchanged, byte-identical.
  * No new hard stop. rdkit missing → one install retry, then those questions are recorded
    APPLIES-UNRENDERABLE and the footer goes amber via the existing "renderer degraded (…)" line;
    re-solve loops are bounded (3 attempts); the paper always delivers and §R3 lists every degrade.
  * Re-explain priority chemistry papers (start with CSIR NET Chemical Sciences 18-Jul-2026) so
    their difficulty-profile records are replaced idempotently (S7A-6).
