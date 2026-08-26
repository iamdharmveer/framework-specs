# Deploy: REGISTRY-HANDOFF-LAW — release 2026.08.26.3

**Fixes:** `GAP-2026-08-26-REGISTRY-HANDOFF-SEAM` — four mock-track steps write
`[ExamCode]_registry.json` and only one delivered it; MockTestExplain's own delivery
gate HARD-STOPPED on a staged registry while §7A-M called the registry "the ONLY
channel to Step 11". Every gated paper on every exam was undeliverable by a literal
run; the repair pair dead-looped on a snapshot that never reached the project.

**Exam-independent:** the handoff decision is a fingerprint (`pp.registry_changed`)
fed to `pp.handoff_set`; no exam value, step name in prose, or per-step sentence
decides it. Enforced by LAW_REGISTRY.json REGISTRY-HANDOFF-LAW + mock_sync_audit
MS-14, so the "frozen registry" wording cannot return in any spec.

**Operator decisions folded in (2026-08-26):** the Step-7 audit dossier is internal
(not delivered); the Step-9 END-OF-MOCK REPORT is also delivered as
`[ExamCode]_[slug]_Explain_Report.docx` (inert downstream).

---

## Files to commit to GitHub (branch: production — via main)

| File | Required | Why |
| --- | --- | --- |
| `Framework_MockTestExplain.md` (v1.46.0) | **Yes** | S19-0, closed handoff set, §7A-R delivery contract, §20-R |
| `Framework_MockTestCreate.md` (v5.73) | **Yes** | §S16-3 delivery contract; dossier internal |
| `Framework_DeliveryFooter.md` (v1.27) | **Yes** | STEP 7-R / 9-R blocks, badges, §8 law |
| `Framework_MockDeliver.md` (v1.16.0) | **Yes** | §8 closed set, S1-2 remedy |
| `paper_pipeline.py` (v5.74) | **Yes** | Cluster RH |
| `explain_engine.py` (v2.9) | **Yes** | report docx builder |
| `final_assembly.py` (v5.60) | **Yes** | dossier internal in predelivery_checklist |
| `mock_sync_audit.py` | **Yes** | MS-14 |
| `audit_sync.py` | **Yes** | `registry_writer_call` detect rule + fixture |
| `LAW_REGISTRY.json` | **Yes** | REGISTRY-HANDOFF-LAW |
| `SPEC_HISTORY.md` | **Yes** | DeliveryFooter v1.24–v1.26 entries relocated (EC-P42) — tracked by MANIFEST |
| `VERSION`, `CHANGELOG.md`, `CLAUDE.md`, `DEPLOY_NOTES.md` | **Yes** | release + guardrail |
| `MANIFEST.json`, `SPEC_MANIFEST.json`, `SPEC_SECTIONS.json` | **Yes** | regenerated — CI diffs them |

> Do **not** hand-edit the three manifests. If you change any file after downloading,
> re-run `python3 gen_manifest.py && python3 build_spec_manifest.py && python3 spec_sections.py`.

## Gates run on this bundle (local, verbatim from validate.yml)
Manifest / SPEC_MANIFEST / SPEC_SECTIONS current · bootstrap 52/52 · markdown validator 0 issues
(23 files) · triggers consistent · notes sync + notes self-tests · final_assembly 122/122 ·
spec-name ratchet OK · mock_sync_audit 14/14 checks (self-test 46/46) · audit_deep ·
audit_callgraph 0 findings · audit_sync 0 findings (self-test incl. the new law fixture) ·
audit_specs_ext 0 issues (SPEC-BUDGET satisfied: DeliveryFooter trimmed via EC-P42 so the
PYQPrepare route stays under 250,000 B) · audit_seam · audit_mutation: audit_canonical 44/44,
mock_sync_audit 34/34, transport_core — all 100% killed · every engine self-test green.
NOT re-run here (unchanged engine, ~4 min): the analyse_engine pipeline mutation audit.

## Deploy steps
1. Replace the files above in your `main` checkout; `git push origin main`;
   `git push origin main:production`.
2. CI (`validate.yml`) runs the full gate list; `python3 run_ci_gates.py --skip Install`
   reproduces it locally.

## What the operator does differently from now on
After **TestCreate, TestExplain (final batch), TestCreateRepair, TestExplainRepair** the
footer shows `[ExamCode]_registry.json → Replace in Project Files`. Replace it before
the next step. TestDeliver reads only the project copy and now says so in plain words
if the replace was skipped.
