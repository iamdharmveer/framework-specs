# DEPLOY NOTES — release 2026.11.05 (GAP-2026-11-05-DIFFICULTY-FIDELITY)
Over verified production 8ff6aa5 (2026.11.04); commit once, push main, push main:production.
Upload EVERY file below (29 files, none new, none removed) in ONE commit. A partial upload fails
bootstrap for every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every
engine and spec).

Engines:  blueprint_core.py (v1.31 -> v1.32)      audit_canonical.py (v2.36 -> v2.37)
          analyse_engine.py (v1.2 -> v1.3)         figure_types.py (v1.2 -> v1.3)
          figural_vision.py (+zoom_tiles, +transcription_confidence)
          paper_pipeline.py (dg_write_verdict window_rule / coverage, v5.40 note)
          final_assembly.py (v1.13 -> v1.14)       notes_core.py (v2.13 -> v2.14)
          notes_audit.py (v2.10 -> v2.11)
Auditors: handshake_audit.py (H3 Blueprint §7-9 / ScopedBlueprint S8-2e, H4 S3-12e; 79 checks)
Specs:    Framework_PYQExplain.md (v2.26 -> v2.27)          Framework_MockTestAnalyse.md (v2.59.0 -> v2.60.0)
          Framework_Blueprint.md (v1.63.0 -> v1.64.0)      Framework_ScopedBlueprint.md (v1.13.0 -> v1.14.0)
          Framework_MockTestCreate.md (v5.91 -> v5.92)     Framework_MockReview.md (v2.0.0 -> v2.0.1)
          Framework_MockTestExplain.md (v1.52.0 -> v1.53.0) Framework_MockDeliver.md (v1.25.0 -> v1.26.0)
          Framework_DeliveryFooter.md (v1.39.0 -> v1.40.0)  Framework_NotesCreate.md (v2.10.0 -> v2.11.0)
          Framework_NotesAudit.md (v3.8.0 -> v3.9.0)
Governance: STEP_CONTRACTS.json (override floors raised — owner D8 A), CLAUDE.md UNCHANGED
          (FRAMEWORK COUNTS still 57 / 60 / 23), LAW_REGISTRY.json UNCHANGED, routes.json UNCHANGED
Release:  VERSION (2026.11.05), CHANGELOG.md, DEPLOY_NOTES.md, SHA256SUMS.txt
Generated (must ship together):  MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json
Frozen (owner P1 — verified byte-identical before and after, hash in the bundle's FREEZE line):
          Framework_PYQPrepare.md (sha256 e0047ba1…), corpus_io.py, explain_engine.py,
          t3_mathcomp.py, every blueprint_core / corpus_io symbol PYQPrepare names (52 symbols),
          DeliveryFooter §1, §2, §4-§7 and the §3 STEP 1 block.

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.05 VERIFIED — 57/57
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 79 ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues across 24 file(s)
  python3 mock_sync_audit.py               -> OK — all checks agree
  python3 notes_sync_audit.py              -> OK — 0 findings
  python3 audit_sync.py                    -> findings: 0
  python3 audit_callgraph.py               -> 0 findings
  python3 blueprint_core.py --self-test    -> 991/991
  python3 audit_canonical.py --self-test   -> 577/577
  python3 analyse_engine.py --self-test    -> 304 passed
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

Owner action outside the repo: NONE. No trigger, deliverable, end state, badge or user action
changes (STEP_CONTRACTS deliverables / end states unchanged; MS-27 green).

WHAT THE OPERATOR SEES (every exam — no per-exam action required):
  * TestCreate / MockCreate: the same two files. New INFO lines may appear before delivery and
    in the footer: `DIFFICULTY UNVERIFIED — <reason>` (a control that could not measure says so),
    `Hard target missed: k item(s) ...` (D3-R5 a), the profile coverage line, `level model: small
    pool n=...` (D10 B). They are informational. NOT CERTIFIED still comes only from an ACTIVE,
    measured gate (OD-9); none of the four new auditor gates can produce it (WARN only).
  * TestExplain / MockExplain: §7A-M now runs on scoped papers too; `Step 9: k/n assessed` is
    printed below 80 % coverage (verdict unchanged).
  * PYQExplain: new runs score under rubric r2 (inferential MOVES); an exam whose profile was
    built under r1 keeps its stored bands — readers re-score under the rule each record carries.
    Nothing has to be re-run. §13A P2a is VISIBLE-ONLY (zoom tiles) and records option SMILES.
  * MockTestAnalyse: QUALITY gains figure_complexity_pct / closeness_pct / ask_format_shares,
    each stamped `rule.<key>: q2` (an auditor FAIL resting on such a key degrades to WARN, G5).

PER-EXAM EFFECT (gap doc §12):
  * Chemistry-bearing exams (CSIR NET Chemical Sciences, GATE CY, IIT JAM CY, CUET PG CY, BARC,
    PSC chemistry, ... — any exam whose PYQ figures carry structures): RECOMMENDED, never required
    (owner D1-PRE B): re-run PYQExplain on every window paper from the graphics-team Row docx
    (F1), then MockTestAnalyse, then MockBlueprint / ScopedBlueprint --refresh. Until then the
    Level Model is DORMANT for that exam (fewer than LEVEL_MIN_POOL = 12 content-full records)
    and every paper carrying drawn chemistry gets the AMBER `DIFFICULTY UNVERIFIED` line.
  * Text-only exams: readiness reports G-DIFF-FLOOR N/A (no transcribed content, no remedy
    asked); rubric r2 applies to new PYQExplain runs; no AMBER line, nothing to re-run.
  * Re-running PYQExplain mid-series changes the profile; S3-2D recomputes later schedules of a
    scoped series (existing behaviour, recorded in difficulty_amendments).

KNOWN LIMITS (recorded, not defects):
  * figure_types.lookup's 'structure' regex fallback maps unregistered names such as
    data_structure / tree_structure to the chemistry family; the chem-family defaults (DL-50,
    Create S3-2S CHEM_FIGURE_SUBTOPICS) read the DOMINANT registered object types, so a CS /
    biology subtopic is affected only if its section_rules carries such a raw name.
  * Owner D9: the non-chemistry figure families (biology, data, physics_graph, geometry,
    reasoning) keep rubric r2 + the independent judge; their Level Model is a follow-up GAP.
  * Acceptance pool = 30 organic items from two papers (P2a by the model, visible-only); the
    cuts move with the measured share of each exam's own window by design (D1-CUTS A).
