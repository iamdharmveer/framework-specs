# DEPLOY NOTES — release 2026.11.08.1 (GAP-2026-11-07-RE25-HARDENING — world-class organic explanations, zero silent defects, every exam)
Over verified production 02c3dba (2026.11.08, the difficulty release); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (16 files = every file that differs from production; none is new):
CHANGELOG.md
CHEMISTRY_EXPLAIN_LEARNINGS_v1.md       (v1.1 — Contradicts field, EX-CHEM-15b / 18..28)
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.43.0)
Framework_MockTestCreate.md             (v5.95)
Framework_MockTestExplain.md            (v1.55.0 — NEW §6A-13)
Framework_PYQExplain.md                 (v2.30 — NEW §6A-13)
MANIFEST.json
SHA256SUMS.txt
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
STEP_CONTRACTS.json                     (override floors raised; no contract changed)
VERSION                                 (2026.11.08.1)
corpus_io.py                            (v1.20)
explain_engine.py                       (v2.14)

No trigger, deliverable, end state, badge or user action changes (STEP_CONTRACTS.json contracts
unchanged — only the override floors rise, so a stale project copy of a changed spec is NOT loaded;
check_triggers 23/23). SKILL.md is unchanged — no skill re-install is needed: OPSIN (py2opsin) is
installed by the engine itself, once per container session, the first time a chemistry name must be
read; if Java or the install is unavailable the run continues with one AMBER footer line.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.08.1 VERIFIED
  python3 explain_engine.py --self-test    -> SELF-TEST: 448/448 PASS with OPSIN (py2opsin + Java);
                                              446/446 PASS without it (the GitHub runner) — 2 name
                                              fixtures need OPSIN to resolve systematic names
  python3 explain_engine.py --self-test-audit -> AUDIT-SELF-TEST: 26/26 PASS
  python3 corpus_io.py --self-test         -> SELF-TEST: 575/575 PASS (v120_* included)
  python3 validate_framework_md.py Framework_*.md   -> 0 issues
  python3 audit_sync.py                    -> findings: 0
  sha256sum -c SHA256SUMS.txt              -> every line OK
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

WHAT THE OPERATOR SEES (every exam with organic content — no per-exam action required):
  * TestExplain / MockExplain / PYQExplain: chair, Newman, Fischer, Haworth, R/S-priority and
    transition-state drawings where the question needs them; cage molecules (camphor, pinene,
    adamantane, tropane, morphinan, spiroketals) are drawn; text-only organic questions ("Treatment
    of cyclohexanone with MeMgBr gives …") get structures too, read from the printed question
    itself; no "SN₂"; a wrong stem name is reported (mock: regenerate the item; PYQ: one fixed
    disclosure sentence), never explained away. Questions that fail a check are re-solved (at most
    three times); anything still open is listed by question in §R3 with an AMBER footer line.
  * TestCreate / MockCreate: one new field on each item's quality record (structures for text
    options) and a name check at authoring — a stem that asserts a wrongly-numbered product is
    regenerated in the batch (a comparison stem naming the isomers it asks about is never flagged).
  * Non-chemistry exams and non-chemistry questions: nothing changes (no name lookup, no OPSIN
    install, no footer line — probed on history, English, physics, maths, biology, Hindi).
  * No new hard stop, no certificate effect, no new user action.

DISCLOSED LIMITS (this release):
  * FMO lobe diagrams (Woodward–Hoffmann) are not built (owner Q5 (a)).
  * CIP priority numbers are printed only when the engine's digraph reproduces rdkit's CIP label
    (76/77 centres in the release test set); the residue (deep fused quaternary centres) is a
    recorded per-figure degrade, never a wrong number on a page.
  * Explanation figures are laid out by Step 7's own layout engine and aligned step to step; they are
    not placed on the PRINTED coordinates of a mock's options, because no pipeline stores those
    coordinates (a registry carrying them would outgrow the project's 2 MB knowledge limit; this
    project already uses 1.67 MB). The engine supports printed placement for any future source
    of the exact printed MolBlock.
  * A chair / Newman / Fischer / Haworth figure is refused when the structure leaves a stereocentre
    unspecified (it would show an arbitrary configuration); the question is re-solved with the
    configured structure (a racemate is drawn as one enantiomer captioned rac).
  * Map-number leaks are closed at the renderer (labels print only when declared); a deliberately
    declared wrong locant on a non-fused skeleton is caught only by the labels-sentence legend
    check and the E-09 review.
