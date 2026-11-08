# DEPLOY NOTES — release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER — difficulty layer for every exam + organic ruler)
Over verified production 2710d92 (2026.11.07 + two fix commits); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (22 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.42.0)
Framework_MockDeliver.md                (v1.27.0)
Framework_MockReview.md                 (v2.1.0)
Framework_MockTestAnalyse.md            (v2.61.0)
Framework_MockTestCreate.md             (v5.94)
Framework_PYQExplain.md                 (v2.29)
LAW_REGISTRY.json                       (DIFFICULTY-LAYER-LAW)
MANIFEST.json
SHA256SUMS.txt
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
STEP_CONTRACTS.json                     (override floors raised; no contract changed)
VERSION                                 (2026.11.08)
analyse_engine.py                       (v1.4)
audit_canonical.py                      (v2.38)
audit_sync.py                           (detect rule difficulty_layer_rule)
blueprint_core.py                       (v1.33)
handshake_audit.py                      (H-DL, 123 checks)
regression_pyq_fixtures.py              (FX-L2-01..17)

No trigger, deliverable, end state, badge or user action changes (STEP_CONTRACTS.json contracts
unchanged — only the override floors rise, so a stale project copy of a changed spec is not loaded;
check_triggers 23/23). SKILL.md is unchanged — no skill re-install is needed. Step 1 (PYQPrepare)
is unchanged.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.08 VERIFIED
  python3 blueprint_core.py --self-test    -> SELF-TEST: N/N PASS (Cluster DL / L2 included)
  python3 analyse_engine.py --self-test    -> SELF-TEST: N/N PASS
  python3 audit_canonical.py --self-test   -> SELF-TEST: N/N PASS (v238 checks included)
  python3 regression_pyq_fixtures.py       -> SELF-TEST: N/N PASS (FX-L2 included)
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 123 ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues
  python3 audit_sync.py                    -> findings: 0  (DIFFICULTY-LAYER-LAW governs Analyse + Create)
  sha256sum -c SHA256SUMS.txt              -> every line OK
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

WHAT THE OPERATOR SEES (every exam — no per-exam action required):
  * MockTestAnalyse (Step 5): one extra internal phase — the exam's past questions of the window are
    graded blind by fresh graders (S11-1c), then the exemplar bank is delivered as before. Attach
    that bank to TestCreate as before. Nothing new to upload to the project.
  * TestCreate / MockCreate: the start-up summary prints where the difficulty shares came from and,
    on an organic paper, the ruler's state and pattern supply. A question measured easier than its
    slot is rewritten, not relabelled; the review repairs it once more; only then may it be accepted
    lower, and the footer says so ("Difficulty fallback (DR3): …"). The footer also prints the
    delivered band counts against the schedule.
  * Every non-organic subject: the generic layer only (same repair-before-relabel rule and the same
    end count); no ruler, no pattern cards.
  * No new hard stop, no certificate effect, no new user action.

DISCLOSED FOLLOW-UP (owner decision pending, not in this release): the blueprint's band mix is
still written as before; whether Blueprint / ScopedBlueprint should take their shares from the
Step-5 blind grades is the next decision.
