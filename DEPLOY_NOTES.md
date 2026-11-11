# DEPLOY NOTES — release 2026.11.10 (GAP-2026-11-10-ORGANIC-QUESTION-PARITY + GAP-2026-11-10-DIFFICULTY-INTEGRITY — every label measured, every exam)
Over verified production bbc6c14 (2026.11.09); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (26 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.45.0 — §LADDER-OP: schedule as applied, last-resort AMBER line)
Framework_MockTestCreate.md             (v6.0 — NEW S0-OP; S3 stops -> repairs; CHECK 3c fresh graders; S13-2L/2R SC2; S13-2P)
Framework_MockTestOrchestrate.md        (v1.2.0 — O6 fresh-context workers; WORKDIR-LOST auto-restart)
Framework_PYQExplain.md                 (v2.31 — schema 3 Phase B, fail-closed Phase C, §13A-3B BACKFILL)
LAW_REGISTRY.json                       (+LAW-ORG-1..12; 5 laws amended)
MANIFEST.json
SHA256SUMS.txt
SKILL.md                                (Step 0: DR mirror + project cache failover)
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
VERSION                                 (2026.11.10)
analyse_engine.py                       (v1.5)
audit_canonical.py                      (v2.40)
audit_sync.py                           (organic_parity_rule, STOP-NEEDS-REPAIR)
blueprint_core.py                       (v2.0 — Cluster OP)
bootstrap.py                            (--make-cache)
corpus_io.py                            (v1.21 — geometry gates, templates, figure proofs)
figural_core.py                         (v5.97 — native geometry gate, G-ORGPROOF)
figural_vision.py                       (v3 — fail closed, readback_compare)
figure_types.py                         (v1.3 — proven projection renderers, 13 convention tags)
final_assembly.py                       (v1.16 — framework_release stamp, parity / proof gates)
handshake_audit.py                      (186 checks)
mocktestframework_SKILL.md              (same Step 0 change as SKILL.md)

SKILL CHANGE: SKILL.md Step 0 changed. Re-install / re-sync the mock-test-framework skill in every Claude account
that runs the framework (the synced skill copy is what a session executes first).

OPTIONAL (owner, any time; never required for a run):
  * FRAMEWORK_MIRROR.txt in an exam project = one line, the HTTPS URL of a distinct mirror (mirror.yml pushes
    production there when MIRROR_URL / MIRROR_PAT secrets are set). Without it Step 0 skips the mirror.
  * framework_cache.zip in an exam project = `python3 bootstrap.py --make-cache framework_cache.zip` on a verified
    clone; used only when GitHub and the mirror are both unreachable; bootstrap re-verifies every hash.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx scikit-image openpyxl --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> VERIFIED
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1303/1303 PASS
  python3 audit_canonical.py --self-test   -> SELF-TEST: 618/618 PASS
  python3 final_assembly.py --self-test    -> SELF-TEST: 184/184 PASS
  python3 corpus_io.py --self-test         -> SELF-TEST: 594/594 PASS
  python3 figural_core.py --self-test      -> SELF-TEST: 240/240 PASS
  python3 figure_types.py --self-test      -> SELF-TEST: 985/985 PASS
  python3 figural_vision.py --self-test    -> SELF-TEST: 53/53 PASS
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 186 ok, 0 FAIL
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES:
  * The first TestCreate / MockCreate of each exam after this release first BACK-FILLS that exam's PYQ records to
    schema 3 (re-reads the page images already in the project, two fresh blind grades per record) in automatic
    worker sessions, then builds the exam's difficulty ruler. No user step; it takes longer once per exam.
  * Every question label is set by two fresh blind graders + the band recipe agreeing on the band. A question that
    grades easier or harder is rewritten or replaced — never relabelled, swapped, held or forced.
  * Every key is checked by two fresh blind solvers; a disputed key is replaced, never certified by majority.
  * If a slot still cannot reach its band after every repair, the reserve and 5 fresh refill sessions, it is filled
    with a fully verified question at the nearest band, shown on ONE AMBER footer line ("last resort — requested
    Hard, delivered Medium") and a P0 incident is recorded. The target rate is 0.
  * Organic figures (bridged rings in perspective, chairs, Newman, Fischer, Haworth) are drawn and proven; a figure
    that cannot be proven is never delivered.
  * A requested schedule never stops a run; percentages / wrong sums are normalised and printed once.

DISCLOSED LIMITS (this release):
  * Exam-input and infrastructure stop sites OTHER than the difficulty path (a missing blueprint / manifest, an
    exam-code mismatch, an undrawable figure type, a corrupt saved state) keep their existing stop text; the
    orchestrator now retries INFRA faults in fresh workers and then on the previous verified release (O6-2).
  * organic_library.json (the cross-exam library) is not shipped: thin-history exams use the built-in level recipes
    (blueprint_core.LEVEL_DEFAULT_RECIPES) until a maintainer builds the library with blueprint_core.organic_library_build.
  * Fresh blind graders / solvers / vision reads need sub-agents or Orchestrate workers; a surface with neither is the
    NO-MODEL environment failure (state saved, resumes) — it never certifies on same-context grades.
  * Cage compounds (prismane, cubane) cannot be drawn in 2-D without a crossing bond; G-BONDCROSS refuses them, so such
    a slot is written with another structure (never drawn wrongly).
  * The first TestCreate of each exam back-fills every PYQ record once (CSIR NET Chemical Sciences: 358 records); the
    upgraded records are kept in registry.json['pyq_backfill'], so later papers never repeat it.
  * An organic format / convention floor that no conversion can fill is disclosed on the footer ("Organic parity: FAIL —
    short ..."), never hidden and never a stop.
  * A structure figure that still has no proof record after two replacements is disclosed on an AMBER line (bounded).
  * If the grading / review environment cannot produce independent results (graders never agree over 6 last-resort
    rounds, or every review returns NOT_RUN), the run saves state and prints NO-MODEL — type continue once sub-agents /
    Orchestrate workers are available.
