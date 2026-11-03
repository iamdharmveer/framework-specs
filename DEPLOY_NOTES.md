# DEPLOY NOTES — release 2026.11.03 (GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY)
Over verified production 766e8c6 (2026.11.02); commit once, push main, push main:production.
Upload EVERY file below (31 files, two NEW) in ONE commit. A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

Engines:  blueprint_core.py (v1.29 -> v1.30, Cluster QQ)   corpus_io.py (v1.17 -> v1.18)
          figural_core.py (v5.89 -> v5.90)                  figure_types.py (v1.1 -> v1.2)
          analyse_engine.py (v1.1 -> v1.2)                  audit_canonical.py (v2.34 -> v2.35)
          final_assembly.py (v1.11 -> v1.12)
Auditors: mock_sync_audit.py (+MS-26)                       audit_sync.py (+quality_gate_producer)
          validate_framework_md.py (PIPELINE +MockReview/TestReview = 7R)
          handshake_audit.py (NEW — cross-step handshake audit; tracked, CI-discovered)
          gen_manifest.py (tracks handshake_audit.py)
Specs:    Framework_MockTestCreate.md (v5.89 -> v5.90)      Framework_MockReview.md (NEW v1.0.0)
          Framework_MockDeliver.md (v1.23.0 -> v1.24.0)     Framework_DeliveryFooter.md (v1.37.0 -> v1.38.0)
          Framework_MockTestAnalyse.md (v2.58.0 -> v2.59.0) Framework_PYQExplain.md (v2.25 -> v2.26)
          Framework_Blueprint.md (v1.62.0 -> v1.63.0)       Framework_ScopedBlueprint.md (v1.12.0 -> v1.13.0)
Governance: routes.json (+MockReview, +TestReview; blueprint_core.py -> MockDeliver/TestDeliver),
          SKILL.md + mocktestframework_SKILL.md (trigger list), LAW_REGISTRY.json (+QUALITY-GATE-LAW),
          CLAUDE.md (FRAMEWORK COUNTS 56 / 60 / 25)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together):  MANIFEST.json, SPEC_MANIFEST.json (+Framework_MockReview.md entry), SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 25
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.03 VERIFIED — 56/56
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 52 ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues across 24 file(s)
  python3 mock_sync_audit.py               -> OK — all checks agree (MS-26 included)
  python3 audit_sync.py                    -> findings: 0
  python3 run_ci_gates.py --skip Install   -> ALL GREEN
  (The full CI run exceeds 30 minutes on a single-core runner because of the engine self-tests;
   the gates were verified individually in the release environment — see the release report.)

Owner action outside the repo: the installed claude.ai skill's description/trigger list must add
`MockReview, TestReview` (same line as in SKILL.md). Nothing else outside the repo changes.

NEW STEP in the Create workflow (every paper, every exam — owner OD-5 a):
  TestCreate / MockCreate now ENDS at "STATE: AWAITING_REVIEW" and delivers
  [ExamCode]_[slug]_review_packet.zip. That is the normal end of the step, not a stop.
    1. Open a NEW chat in the same project, attach ONLY the packet, run `MockReview`
       (or `TestReview`). It delivers [ExamCode]_[slug]_review_verdicts.json.
    2. Back in the AUTHOR's chat, attach the verdict file AND [ExamCode]_registry.json and run
       `TestCreate --resume` (or `MockCreate --resume`). It binds the verdicts, repairs every
       flagged item through the ladder, re-sweeps, and commits. One more review round at most;
       an item still disputed after round 2 is UNRESOLVED and the paper is NOT CERTIFIED.
  A NOT CERTIFIED paper: Explain runs as before; `MockDeliver M[N]` / `TestDeliver P[N]` REFUSES
  it with the item list (a printed verdict that ends the step before any rendering) — re-run the
  same trigger with `--accept-uncertified` to deliver it; the footer says so and the registry
  records who accepted and when (registry.accepted_uncertified; the registry is delivered).

Per exam (once per exam, in this order; nothing here halts a run if skipped — each control prints
"DORMANT" and records it in quality_readiness, and the footer says DEGRADED QUALITY):
  1. Re-run PYQExplain on the PYQ papers (profile v2.26: per-item ask_type / named_concepts /
     concept / drawn_names / near_isomer_set / distractor_mechanisms / stereo_decl join the
     content record). Replace [ExamCode]_difficulty_profile.json in Project Files. THIS IS THE
     SOURCE of Step 5's lexicon, rates and exemplar bank — without it they read 'unmeasured'
     and the bank is empty (printed, never a halt).
  2. THEN re-run Step 5 (PYQExtract / MockTestAnalyse v2.59.0) with the PYQ docx files in the
     project. section_rules.md gains one QUALITY block per subtopic (shape shares, named-concept
     rate, common entities, text-leak calibration) and the EXAM_QUALITY block; the step ALSO
     delivers [ExamCode]_exemplar_bank.json (real PYQ items per difficulty band) in its own
     present_files call. Upload section_rules.md to Project Files. The exemplar bank is a RUN
     FILE (OD-11): attach it to every TestCreate / MockCreate run beside the registry (Create
     also accepts it from Project Files); absent, the difficulty judge is dormant (printed),
     never a halt.
  3. Refresh the blueprints: `ScopedBlueprint --refresh` for every scoped series in progress and
     `MockBlueprint --refresh` for the mock series — with the existing blueprint (and the registry)
     attached. Only shape_target_per_paper / schema_version / producer are written, for papers
     AFTER the last registered one; registered papers are untouched. Upload the refreshed
     blueprint. A blueprint without shape targets still runs: S3-12d prints "shape plan DORMANT".
  4. If the project has an old [ExamCode]_mock_test_audit.py, TestCreate uses the verified repo
     auditor (v2.35) and delivers it — upload it to the project (15 new gates; certificate
     schema 2).
  A paper produced BEFORE this release is AMBER on every new gate (EC-V18), never a FAIL; its
  Deliver is unchanged (no certificate -> legacy).
  A project that OVERRIDES any changed spec in its Files section opts out of that spec's part of
  this fix (CLAUDE.md project-first); remove or update the override.
