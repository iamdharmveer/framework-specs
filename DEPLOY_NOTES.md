# DEPLOY NOTES — release 2026.11.09 (GAP-2026-11-08-DR3-QINDEX — never a hard stop, never NOT CERTIFIED, every exam)
Over verified production 642c024 (2026.11.08.1, the RE-25 hardening release); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (21 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.44.0 — SLOT-CHAIN LINES, amber classes)
Framework_MockDeliver.md                (v1.28.0 — 3f''' SLOT-CHAIN LINES; --accept-uncertified legacy only)
Framework_MockTestCreate.md             (v5.96 — S13-2F sweep_route, S13-2G delta / panel, NEW S13-2L, NEW S13-2R)
Framework_MockTestOrchestrate.md        (v1.1.0 — O2-8 resume; review mode in the part folder name)
LAW_REGISTRY.json                       (+LABEL-BASIS-LAW, +REVIEW-COVERAGE-LAW)
MANIFEST.json
SHA256SUMS.txt
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
STEP_CONTRACTS.json                     (override floors raised; Deliver user_actions note)
VERSION                                 (2026.11.09)
audit_canonical.py                      (v2.39)
audit_sync.py                           (LABEL-VERIFIER / REVIEW-COVERAGE / LADDER-COVERAGE)
blueprint_core.py                       (v1.34 — label verifier, slot chains, review coverage, sweep route)
final_assembly.py                       (v1.15 — commits slot_chain for DISCLOSED items)
handshake_audit.py                      (189 checks)
notes_core.py                           (v2.15 — recall uses the one label verifier)
paper_pipeline.py                       (check-6 count mirror)

No trigger, deliverable or end state changes. SKILL.md is unchanged — no skill re-install is needed.
Framework_MockReview.md is deliberately unchanged.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx --break-system-packages
  sha256sum -c SHA256SUMS.txt              -> every line OK
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.09 VERIFIED
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1195/1195 PASS
  python3 audit_canonical.py --self-test   -> SELF-TEST: 612/612 PASS
  python3 final_assembly.py --self-test    -> SELF-TEST: 180/180 PASS
  python3 paper_pipeline.py --self-test    -> SELF-TEST: 257/257 PASS
  python3 notes_core.py --self-test        -> 314 passed, 0 failed
  python3 audit_sync.py --self-test        -> 46 passed, 0 failed
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 189 ok, 0 FAIL
  python3 audit_mutation.py --quiet --max-survivors 0
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES:
  * A question that measures easier than its slot is reworked and replaced (13 reviewed attempts at
    most), then swapped with a partner in the right band, then paired with an upgraded partner.
    Only if all of that fails is the slot's label kept at the schedule — and the question is named on
    an AMBER footer line ("schedule-forced"). The difficulty schedule is always delivered exactly.
  * A disputed answer key goes to a switched reviewer, then a 3-reviewer panel, then a re-key, then a
    majority (AMBER line). UNRESOLVED is never stamped; every paper is CERTIFIED.
  * A session that cannot start reviewer sub-agents still finishes: its same-session reviews count for
    coverage (disclosed, as before), and a disputed key that only a same-session review agrees with moves on
    through its chain to a panel / majority instead of waiting forever.
  * A question that keeps measuring HARDER than its slot keeps its scheduled label (footer "Difficulty held at
    slot: …") — the requested schedule is delivered exactly (owner decision 2026-11-10).
  * A broken tool is self-healed twice; a paper-level gate is reassembled; after 6 sweeps the
    remaining finding becomes an AMBER line instead of a stop.
  * A run that stopped under 2026.11.08.x resumes from its saved files: say "TestCreate" again in the
    same conversation (Orchestrate O2-8 re-runs Step 0 and migrates the paper onto chains).

DISCLOSED LIMITS (this release):
  * The only remaining stop is an environment that is still broken after two self-heals (e.g. the
    python-docx install itself fails). It names the tool and resumes on the next "TestCreate".
  * Forced labels, majority keys and disclosed quality items are delivered CERTIFIED but always
    listed on AMBER footer lines — never silent.
  * A resume of an old stopped run needs the container to still hold its working files; a fresh
    container starts the paper again.
