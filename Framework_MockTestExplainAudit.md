# Framework_MockTestExplainAudit.md
# [ExamCode] project | Step 10 (MockExplainAudit) | Universal Mock Test Explanation Auditor

**Step 10 — MockExplainAudit**
**The independent auditor and rectifier of explanation documents produced by Step 9.**

Version: v1.7
Status: Active
Engine: `explain_engine.py` (shared universal engine; core `--self-test` 47/47, extended reader suite `--self-test-audit` 10/10) + `explain_audit_gate.py` (ledger completion gate; `--self-test` 8/8)

---

## VERSION HISTORY

**v1.7** — 2026-07-08 — MECHANICAL COMPLETION GATE (close the explanation false-clean chain).
ROOT-CAUSE PARALLEL: the same false-clean chain fixed for Step 8 in
Framework_MockTestCreateAudit.md v2.6 was latent here. Step 10 already NAMED the right
guarantees — the per-question evidence gate (§17 mechanism 2), the zero-sampling coverage
assertion (§17 mechanism 3), and the pre-delivery scope assertion (§18) — but those were
PROSE the model self-attests, and the engine's `verify_fidelity` / `verify_structure` /
`verify_explanations` check the DOCUMENT, never the audit ledger + evidence sidecars. So a
collapsed or partial Phase-2 run could self-declare clean and ship a bad explanation /
answer-key set.
FIX — a runnable, exam-agnostic COMPLETION GATE, `explain_audit_gate.py`, is now REQUIRED at
Phase 3 (§20) before `present_files`. It reads the Step-10 audit ledger
(`audit_progress.json`, §18) + its evidence sidecars and asserts CA1–CA7 (all HARD;
evidence-bound):
  CA1 every planned batch closed (a skipped/collapsed Phase 2 fails here — MANDATE B);
  CA2 coverage exact 1..total_questions (no gap, no look-ahead);
  CA3 every verdict CLEAN/FIXED (no open ESCALATED/UNVERIFIED);
  CA4 every answer independently re-derived with ≥1 route (RXA-1);
  CA5 figural Q grounded in a viewed image whose file EXISTS (RXA-8 / §11);
  CA6 factual/vocab Q web-sourced with the source file present (RXA-12 / §9);
  CA7 reproduce-check evidence present for every Q (RXA-9 / §8.7).
Evidence-binding (mirrors Step 8 FIX F): every named evidence file must EXIST and be
non-empty, so a fabricated ledger cannot pass without the work that produces the files.
Also: RXA-0 PRECEDENCE (no preference reduces coverage or weakens the gate); RXA-7 split
into RXA-7a EXHAUSTIVENESS (the WHAT, mode-independent) and RXA-7b PACING (the WHEN,
waivable); an AUTONOMOUS-mode paragraph (§18) that waives the inter-batch PAUSE only, never
the review; §3 P0, §4 PHASE 3, §17/§18, §20, §22 wired. The gate is a SEPARATE module (it
reads the JSON ledger, not the docx, so it does not touch the engine's read/write path —
MANDATE A — and needs no python-docx). Appendix A now POINTS to the canonical runnable
`explain_engine.py` + `explain_audit_gate.py` (single source of truth) instead of
re-embedding the engine listing. Engine self-tests unchanged (47/47 + 10/10); new gate 8/8.

**v1.6** — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
Added post-delivery footer rendering reference to Framework_DeliveryFooter.md v1.3
in the delivery section (after item 4 in the delivery protocol). F2 (step-complete)
footer rendered after the single present_files call and end-of-mock report. Zero logic change.

**v1.5** — 2026-07-04 — ENGINE CODE FIXES (3 bugs) + EXAM-AGNOSTIC HARDENING (4 fixes).
Coordinated with Step 9 v1.9. Embedded engine Appendix A updated:
PART A — 3 code fixes claimed in v1.8 of MockTestExplain but never applied:
(1) parse_solution_blocks CA detection → case-insensitive. (2) _is_subheader →
configurable terminators. (3) parse_learnings superseded → explicit field check.
PART B — EXAM-AGNOSTIC HARDENING:
(4) _BANNED_BLOCKS (SSC-specific 'REMEMBER'/'EXAM CONNECTION') → configurable via
EngineConfig.banned_blocks. (5) _BANNED_TEMPLATE, _BANNED_FAKECITE (English-only) →
configurable via EngineConfig.banned_templates/banned_fakecites. (6) _META_RE
(English metacommentary) → configurable via EngineConfig.metacommentary_re.
(7) option_label() → bounds checks for custom-list and alpha schemes.
guard_sentence() + verify_explanations() read from cfg when available.
Engine self-test: 47/47 + 10/10. No spec-text or logic change.

**v1.4** — 2026-07-04 — CANONICAL STEP-NUMBER ALIGNMENT + CROSS-REFERENCE FIXES (10 bugs).
(1) TITLE/FILENAME MISMATCH: header said "Framework_MockExplainAudit.md" but filename
    is Framework_MockTestExplainAudit.md. FIXED: title now matches filename.
(2) ~100 CANONICAL STEP-NUMBER VIOLATIONS: entire body used old internal phase
    numbering (Step 0/1/2/3/4/5/6) while header used canonical 11-step pipeline.
    FIXED: all body references now use canonical numbers: old Step 0 → Step 5
    (PYQExtract), old Step 1 → Step 6 (MockBlueprint), old Step 2 → Step 7
    (MockCreate), old Step 3 → Step 8 (MockCreateAudit), old Step 4 → Step 9
    (MockExplain), old Step 5 → Step 10 (MockExplainAudit = THIS), old Step 6 →
    Step 11 (MockDeliver). Version history preserved unchanged.
(3) PIPELINE POSITION used old numbering (Step 0–6) and non-existent step name
    "MockTestSort". FIXED: canonical Step 5–11; "MockTestSort" → "MockDeliver"
    with correct output filename.
(4) §8.9 CROSS-REFERENCE DOESN'T EXIST (2 occurrences): §13 and §25 referenced
    "§8.9" but the common-pitfalls audit is §8.8 (S5-9) and the reproduce-check
    is §8.7 (S5-8). FIXED: "§8.9" → "§8.8" and "§8.7/§8.8".
(5) §8.5 FRACTION CROSS-REFERENCE WRONG in §22 definition-of-done: "(§8.5, §7)"
    but §8.5 is speed-hack; FRACTION-INLINE is defined under §8.4 (deduction
    audit). FIXED: "(§8.4, §7)".
(6) DEFECT CLASSIFICATION TABLE (§15) missing markdown header separator row.
    FIXED: added |---| separator.
(7) EMBEDDED ENGINE STEP NUMBERS: Appendix A engine comments used old step
    numbers (~15 occurrences). FIXED: all aligned to canonical.
(8) EMBEDDED ENGINE FILENAME: engine comment referenced "Framework_MockExplain.md"
    instead of "Framework_MockTestExplain.md". FIXED.
(9) END-OF-FILE MARKER: "End of Framework_MockExplainAudit.md" missing "Test".
    FIXED.
(10) "Step 8's RA-*" and "Step 9's rule families" in D4: step references in
     design-decision text updated to canonical.
Cross-step contract verified against: Step 9 v1.8 (canonical numbering, delivery
contract, §24/RE-22 consumer); Step 8 v1.9 (canonical numbering); Step 11 v1.0
(pipeline position, input contract). No logic change; engine untouched; self-test
stays 47/47 + 10/10.

**v1.3** — 2026-07-03 — DEEP-AUDIT (3 version/count fixes).
(1) Header `Version:` was v1.1 but the latest changelog entry is v1.2 — never bumped.
    Fixed: v1.3.
(2) Self-test core count stale at 44/44 in two prose locations (MANDATE A and P0); the
    engine is now 47/47 (Step 9 v1.6 added FIGURE-HDR tests). Fixed: 47/47.
(3) MANDATE A reader suite count stale at "5 of 5"; it's been 10/10 since v1.1. Fixed.
No logic change; engine untouched.

**v1.2** — Question metadata index — defensive read-only touch (cross-step index extension, Step-5 half). Step 5 never reads or writes `registry.question_index`: it is a Step-3-certified, frozen field bound for Step 6, and Step 5 writes only its own audit sidecars, never the registry. §0 records the frozen/read-only status and the escalation-consistency path — when Step 5 escalates a *paper* defect (§16) and Step 2/3 regenerate it, Step 3 re-runs and re-syncs the index from the rectified paper, so the index tracks the corrected paper without Step 5 touching it. No output bytes change; the shared engine and both self-tests (`--self-test` 47/47, `--self-test-audit` 10/10) are untouched. Governed by Contract_QuestionMetadataIndex v1.0.

**v1.1** — Closes the learnings loop (D3) and pins its producer↔consumer contract. Step 4 now consumes the emitted `[ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md` at its P1 and applies every applicable rule while authoring (Step 4 §24 / RE-22). §24 here is tightened to the PINNED AL-rule schema and the ≥2-occurrence promotion threshold that Step 4's consumer expects, so the two halves cannot silently desync. The shared engine gains `parse_learnings` (the reader both steps use for the learnings file); it is additive, the core `--self-test` stays 44/44, and the extended `--self-test-audit` suite is now 10/10 (reader round-trips + OMML-fraction and fraction-NAT regressions + learnings-parse round-trip). A final adversarial-QA pass also fixed three OMML-blindness defects in `verify_explanations` / the reader that made a NAT with a fraction answer or fraction pitfall value unshippable — segmentation, binding and coverage read `p.text`, which excludes OMML — and switched sub-header detection to the writer’s spacing rather than a text heuristic. Zero rendered bytes change; no audit logic changed.

**v1.0** — First release. Establishes Step 5 as the independent explanation auditor: it re-derives every answer from scratch, re-runs the machine verifiers itself rather than trusting Step 4's self-report, deep-audits every explanation section against three lanes (correctness, sufficiency, proportion), and rectifies defects surgically while the reasoning context is fresh. Rationale for the six architecture decisions that shaped this release is recorded below so future edits inherit the reasoning, not just the rule.

- **D1 — no inherited answer key.** Step 4 delivers only the Solutions document; it publishes no answer-key sidecar (Step 4 D1, closed-delivery contract). Step 5 therefore re-derives every answer independently and writes its own `[ExamCode]_Mock[N]_audit_answer_keys.json`. This mirrors how Step 3 relates to Step 2: the auditor never trusts the producer's key, it reconstructs one. See MANDATE A and §9.
- **D2 — the reader lives in the engine.** Reading a rendered Solutions document back into structured blocks is not a text-scrape: the block headers, the option word, the correct-answer label, the accepted-range label and the option-label scheme are all configuration-driven glyphs, not literals. A reader that hardcoded them would be exam-bound. The reader (`parse_solution_blocks`) is therefore an engine function driven by the same `EngineConfig` that Step 4 wrote with, making it the exact inverse of the writer. See §7, §16, Appendix A.
- **D3 — learnings loop is emit-now, wire-later.** Step 5 emits `[ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md` capturing every recurring defect class it fixed. Step 4 consumes that file at its P1 and applies its rules while authoring (Step 4 §24 / RE-22, wired in v1.1); the producer schema here is pinned to that consumer. See §24.
- **D4 — rule-family prefix RXA.** Audit rules are numbered RXA-1, RXA-2, … (Rules, eXplanation Audit), keeping them distinct from Step 3's RA-* and Step 4's rule families.
- **D5 — output filename.** The rectified document is `[ExamCode]_Mock[N]_Solutions_Audited.docx`. The input `[ExamCode]_Mock[N]_Solutions.docx` is never modified in place. See §0, §20.
- **D6 — per-batch rectification.** Defects are fixed in the same response that finds them, while the derivation is fresh, then the document is rebuilt and re-verified before the batch closes. Fix-later batching is a decay vector and is forbidden. See §16, §17.
- **Engine fraction-extraction fix (discovered during Step 5 bring-up).** While proving the reader, the round-trip surfaced a latent defect in the shared engine: `frac()` stores a fraction's digits as the direct text of the `m:num`/`m:den` elements, but `verify_explanations` read them only through `m:t` descendants, so every genuine digit/digit fraction was falsely reported as a malformed OMML fraction. Because Step 4's own §18 self-audit calls `verify_explanations`, any explanation containing a real stacked fraction could not pass that gate — which explains why quantitative explanations in practice avoid OMML fractions entirely. The root-cause fix reads the full text content via `itertext()` (handling both the direct-text and the wrapped `m:r`/`m:t` forms); it changes no rendered bytes and leaves the core self-test at 44/44. The fix is locked by a regression test in the reader round-trip suite (`RT-FRAC-VERIFY`). See §7 and Appendix A.

---

## PURPOSE

Step 9 (MockExplain) writes one explanation per question into an append-only Word document. Step 10 is the independent quality gate on that output. It exists because a producer cannot be its own final auditor: Step 9's construction-time guards and its §18 self-audit prove that each explanation is *well-formed*, but they cannot prove that each explanation is *correct*, *sufficient*, and *proportionate*, because those judgements require re-deriving the answer from first principles without reference to what Step 9 concluded. Step 10 supplies exactly that independent judgement, and then rectifies — root-cause, in place, verified — every defect it finds.

Step 10 audits and rectifies explanation content. It does not audit the question paper: a defect in a stem, an option, a figure, or an answer key that traces to the *question itself* (not to its explanation) is out of Step 10's rectification scope and is escalated to Step 7/Step 8 (§16). Step 10 owns the explanation; the pipeline owns the paper.

---

## PIPELINE POSITION

```text
Step 5   PYQExtract       -> section_rules.md
Step 6   MockBlueprint    -> blueprint.json, subtopic_manifest.json
Step 7   MockCreate       -> [ExamCode]_Mock[N].docx, registry.json
Step 8   MockCreateAudit  -> rectified paper, re-synced registry
Step 9   MockExplain      -> [ExamCode]_Mock[N]_Solutions.docx
Step 10  MockExplainAudit -> [ExamCode]_Mock[N]_Solutions_Audited.docx   <-- THIS STEP
Step 11  MockDeliver      -> [ExamCode]_Mock[N]_Tagged.docx
```

Step 10 consumes the Step 9 Solutions document and the frozen paper artifacts, and produces an audited Solutions document plus its audit sidecars. It is the last gate before the explanation product is considered final.

---

## EXAM-AGNOSTIC GUARANTEE

This specification hardcodes **no** exam value. Section names, section counts, question totals, per-section option counts, option-label schemes (numeric, upper/lower alpha, lower roman), languages, sentence terminators, question sub-types, block-header glyphs and every label are read at run time from the frozen configuration:

- `blueprint.json` (Step 6) — sections, per-section question ranges, option contracts, question-type contracts (mcq / msq / nat).
- `section_rules.md` (Step 5) — labels, markers, language parameters, msq/nat instructions, the accepted-range label.
- `registry.json` (Step 7/8) — the per-question option count and type manifest, and the figural manifest.
- `[ExamCode]_Mock[N]_Solutions.docx` (Step 9) — the explanation content under audit.

Any place a reader might expect an exam-specific value, this document instead names the configuration field it is read from. SSC CGL Tier 1 is used only as a worked reference instance; not one of its values is embedded here. A hardcoded exam value anywhere in this file is a defect regardless of whether the policy behind it is correct.

---

# MANDATE 0 — No explanation content is authored in the chat transcript

Every audit judgement, every re-derivation, and every rectified sentence is reasoned about and then committed **through the engine into the document**. The chat transcript carries status, defect logs, verdicts and the end-of-mock report — never the body of an explanation. This preserves the single source of truth (the document) and prevents a fix that "exists" only in chat from being mistaken for a fix that shipped. The end-of-mock report (§21) is the one place Step 10 speaks at length in chat, and it is deliberately free of authored explanation prose. The audit ledger + evidence sidecars (§18) live on disk and are never printed (they may carry answer-bearing content).

# MANDATE A — The engine is the only read and write path

Step 10 never parses the Solutions document by ad-hoc text matching and never writes explanation paragraphs by hand. It reads through `parse_solution_blocks` and writes through `build_interleaved_docx`, both driven by the `EngineConfig` reconstructed from the frozen configuration. The engine is the same universal `explain_engine.py` Step 9 uses, now carrying the Step 10 reader (Appendix A). Pre-flight (§3) refuses to start unless the engine's core self-test passes cleanly at 47 of 47 and the reader round-trip passes cleanly at 10 of 10. Re-deriving answers independently (D1) means Step 10 builds its own key and never reads a key sidecar, because none is delivered. NOTE (v1.7): the ledger completion gate (`explain_audit_gate.py`, §18/§20) is a SEPARATE module — it reads the JSON audit ledger + evidence sidecars, never the docx, so it does not touch the engine's read/write path and needs no python-docx; it is a distinct enforcement layer, not a second write path.

# MANDATE B — Batch or halt; one batch per response

Step 10 audits and rectifies in batches whose boundaries are frozen before the run begins (§18). A batch is at most `EXPLAIN_AUDIT_BATCH_SIZE` questions (default 10), and the only permitted exception to that ceiling is keeping an atomic linked group whole (§13). Exactly one batch is completed per response; the response then halts and waits for an explicit continue (interactive mode; autonomous mode waives the pause only — §18). Auditing the whole mock in a single response is not a stretch goal — it is a malfunction signal, because it defeats the fresh-context guarantee that keeps late-batch judgement as sharp as early-batch judgement (§17). The pre-delivery scope assertion (§18) makes a single-response full run mechanically unshippable, and v1.7 makes it a COMMAND RESULT: the Phase-3 completion gate (`explain_audit_gate.py`, §20) FAILS (CA1/CA2) unless every planned batch is closed and every question reviewed — a collapsed Phase 2 cannot certify.

# MANDATE D — Deliver once, only when certified clean

The audited document is presented exactly once, after every batch has closed clean and the final whole-document re-verification passes (§20). A batch closes only when its rectifications are rebuilt into the document and the document re-passes `verify_fidelity`, `verify_structure` and `verify_explanations` for the whole paper (not merely the batch). If any check fails, the batch is not closed and nothing is delivered.

**v1.7 — "certified clean" is now a COMMAND RESULT, not a self-judgment.** Before `present_files`, Step 10 runs the mechanical COMPLETION GATE:

```
python3 explain_audit_gate.py --audit-progress [ExamCode]_Mock[N]_audit_progress.json
    → MUST print  AUDIT-COMPLETION-GATE: PASS
```

It validates the audit ledger (§18) + the on-disk evidence sidecars against CA1–CA7: every planned batch closed (CA1), every question reviewed with no look-ahead (CA2), every verdict CLEAN/FIXED (CA3), every answer independently re-derived (CA4), every figural Q grounded in a viewed image whose file exists (CA5), every factual/vocab Q web-sourced with the source file present (CA6), and a reproduce-check evidence file for every Q (CA7). A self-declared "clean" is NOT acceptance — the gate is. This makes a collapsed or partial Phase-2 run mechanically unshippable (CA1/CA2 fail), closing the same false-clean chain fixed for Step 8 (Framework_MockTestCreateAudit.md v2.6 / S5-1A). Evidence-binding: every named evidence file must EXIST and be non-empty, so a fabricated ledger cannot pass without the work that produces the files.

---

# §0 — Input / output contract

**Inputs (all read-only to Step 10):**

- `[ExamCode]_Mock[N]_Solutions.docx` — the Step 9 explanation document under audit. Never modified in place.
- `[ExamCode]_Mock[N].docx` — the frozen question paper (Step 7/8). Used to reconstruct the question region and to re-seed the rebuild so question regions stay byte-identical.
- `blueprint.json`, `section_rules.md`, `registry.json`, `subtopic_manifest.json` — the frozen configuration (CATEGORY C). Source of every exam-specific value. **`registry.question_index` (Step 8-certified) is FROZEN and read-only here** (Contract_QuestionMetadataIndex v1.0): Step 10 never reads it as a source and never writes the registry at all — it writes only its own audit sidecars (below). A paper defect that Step 10 escalates and that Step 7/8 regenerate causes Step 8 to re-run and re-sync `question_index` from the rectified paper, so the index stays consistent with the corrected paper without Step 10 ever touching it.

**Outputs (written by Step 10):**

- `[ExamCode]_Mock[N]_Solutions_Audited.docx` — the rectified Solutions document (D5). Byte-identical to the input wherever no defect was found; every defective explanation section replaced with a correct, sufficient, proportionate one.
- `[ExamCode]_Mock[N]_audit_answer_keys.json` — Step 10's independently re-derived answer key (D1), with per-question derivation confidence and evidence pointers.
- `[ExamCode]_Mock[N]_audit_defect_log.json` — every defect found, its code, lane, severity, verdict, and the before/after of the fix.
- `[ExamCode]_Mock[N]_audit_progress.json` — the frozen batch plan and the resume-safe progress ledger (§18). **v1.7: this is the load-bearing ledger the completion gate validates (CA1–CA7).**
- `[ExamCode]_Mock[N]_audit_web_sources.json` — every external source consulted during factual re-verification, with the claim it supports (§9).
- `[ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md` — recurring defect classes, for the Step 9 feedback loop (§24).

**The audited document must satisfy, at delivery:** every question region byte-identical to the paper; every explanation present, well-formed, correct, sufficient and proportionate; every fraction real OMML; every figural explanation grounded in a viewed image; every one of Step 10's verdicts backed by recorded evidence; and the completion gate printing AUDIT-COMPLETION-GATE: PASS (§20).

---

# §1 — Pipeline position and sources of truth

Step 10 trusts the **paper** and the **configuration** as ground truth for structure, and trusts **nothing** from Step 9 about correctness. Concretely:

- **Structure of the paper** (question numbering, option counts, types, figural manifest) is authoritative from `registry.json` and the paper document. Step 10 does not re-litigate it; if the paper and the Solutions document disagree on structure, the paper wins and the discrepancy is a defect in the Solutions document (§7).
- **Correctness of every answer** is re-derived by Step 10 from the stem and options alone (§9). Step 9's chosen answer is treated as a claim to be checked, never as an input to the check. This is the single most important independence property: if Step 10 lets Step 9's answer anchor its own derivation, the audit collapses into agreement bias and catches nothing.
- **Sufficiency and proportion** of every explanation are judged against the lanes in §5, independently of Step 9's density self-assessment.

Where this document and any earlier step's document disagree about a label, marker, count or type, the frozen configuration is the tie-breaker, because that is what the engine was and is driven by.

---

# §2 — Trigger and mock resolution

Step 10 begins on the instruction form:

```text
MockExplainAudit M[N]
```

Resolution sequence:

1. Resolve `[ExamCode]` to its project configuration (`blueprint.json`, `section_rules.md`, `registry.json`, `subtopic_manifest.json`). If any is missing, halt: Step 10 cannot reconstruct the `EngineConfig` and therefore cannot read the document faithfully.
2. Resolve `M[N]` to `[ExamCode]_Mock[N]_Solutions.docx` and `[ExamCode]_Mock[N].docx`. If the Solutions document is absent, halt (nothing to audit). If the paper is absent, halt (cannot re-seed the rebuild or re-verify fidelity).
3. Reconstruct the `EngineConfig` exactly as Step 9 built it: question regex, option regex, per-question option map (including 0 for nat), label scheme, language terminators, labels and markers — all from configuration. A mis-reconstructed config makes the reader mis-segment the document; §3 P4 proves the reconstruction before any audit begins.
4. If an `audit_progress.json` for this mock already exists, resume from its ledger (§18); otherwise freeze a new batch plan.

---

# §3 — Pre-flight (P0–P9)

Pre-flight runs once at the start of a run (or resume) and gates everything after it. Any failed pre-flight check halts Step 10 with a specific reason; no batch is audited until all pass.

## P0 — Engine present and honest
Run `explain_engine.py --self-test` and require a clean 47-of-47 core pass. Run `explain_engine.py --self-test-audit` and require a clean 10-of-10 extended reader suite. **v1.7: also run `explain_audit_gate.py --self-test` and require a clean `COMPLETION-SELF-TEST: 8/8 PASS` — a completion gate that fails its own fixtures is not a working gate (parallel to Step 8 P1 hardened), and Phase 3 relies on it.** The engine self-tests prove the exact write→read→rebuild inverse holds for mcq, msq and nat, across numeric, alpha and roman label schemes, with OMML fractions and figure notes; that a genuine fraction survives `verify_explanations` (the fraction-extraction regression); and that `parse_learnings` reads a learnings file back into the pinned rule schema (the loop the producer feeds — §24). Without all three green, Step 10 halts.

## P1 — Configuration loads and is complete
Every configuration field the `EngineConfig` needs resolves to a concrete value. No default is silently substituted for a missing exam fact.

## P2 — Paper and Solutions documents open
Both documents open, and `parse_paper` on the paper validates ascending-contiguous questions from 1 with the expected per-question option counts. A paper that fails `parse_paper` is a Step-7/8 defect and is escalated, not audited around.

## P3 — Config reconstruction matches the document
`parse_solution_blocks` reads the Solutions document without raising. Every question in the paper has exactly one explanation region (a correct-answer line) in the Solutions document; any missing or extra region is recorded as a structural defect for §7 and does not, by itself, halt the run.

## P4 — Round-trip self-check on this document
Reconstruct all blocks with `parse_solution_blocks`, rebuild against the paper with `build_interleaved_docx`, and confirm the rebuild passes `verify_fidelity` (question regions byte-identical) and `verify_explanations` (structure intact). This proves the reconstructed `EngineConfig` matches how the document was written *before* any auditing relies on that reconstruction. A failure here means the config is wrong or the document was hand-edited outside the engine; either halts the run.

## P5 — Figural manifest resolves
Every question the registry marks figural, and every question whose Solutions region carries a figure note, is collected into the figural set (union; §11). Every image the paper references resolves to a media part (no dangling relationship). A figural question whose image cannot be resolved halts the run for that batch when reached (§11).

## P6 — Batch plan freezes
Derive the batch plan from the blueprint section ranges (§18), write it to `audit_progress.json`, and never recompute it mid-run. Atomic linked groups are identified now so no batch boundary splits one.

## P7 — Web reachability sample
Confirm the external-verification path is usable (a single reachability probe). Factual re-verification (§9) requires it; if the environment forbids web access, Step 10 records every factual claim it could not externally confirm as `FACT-UNVERIFIABLE` rather than silently trusting Step 9.

## P8 — Output targets writable
The output document path and every sidecar path are writable, and the input Solutions document is confirmed read-only to this process (it is never the write target; D5). The evidence directory (`audit_progress.evidence_dir`) is created for the run's viewed-image / web-source / reproduce-check artefacts (§18).

## P9 — Prior-run reconciliation
If resuming, the ledger's claimed-closed batches are re-verified against the current audited document (a closed batch must still pass whole-document verification). A closed batch that no longer verifies is reopened.

---

# §4 — Audit architecture

Step 10 runs in three phases. Phase 1 is a single whole-document machine pass. Phase 2 is the batched, per-question deep audit with per-batch rectification. Phase 3 is certification and single delivery.

```text
PHASE 1  (once, whole document)
  Independent machine re-verification (§7): re-run verify_fidelity,
  verify_structure, verify_explanations HERE, in Step 10, rather than
  trusting Step 9's §18 self-report. Record every machine-level defect.

PHASE 2  (batched; one batch per response interactively / sequential in
          autonomous mode; MANDATE B)
  For each frozen batch, in order:
    a. Re-derive every answer in the batch from scratch (§9).
    b. Deep-audit every explanation section across the three lanes (§5,§8).
    c. Run the cross-cutting scans that need batch context (§14).
    d. Classify every defect (§15); rectify FIXABLE defects now (§16);
       escalate BLOCKER-class question defects (§16).
    e. Rebuild the document and re-verify the WHOLE paper (MANDATE D).
    f. Write each question's complete, evidence-backed ledger entry (§18);
       advance the ledger by exactly this slice; halt (interactive) or
       proceed to the next batch (autonomous — pacing waiver only, §18).

PHASE 3  (once, after the last batch closes clean)
  1. COMPLETION GATE: explain_audit_gate.py --audit-progress ..._audit_progress.json
     -> MUST print AUDIT-COMPLETION-GATE: PASS (CA1-CA7). A non-PASS forbids
     delivery (MANDATE D).
  2. Final whole-document re-verification (verify_fidelity/structure/explanations).
  3. Sidecar finalization, the end-of-mock report (§21), and the single delivery (§20).
```

**The continue contract.** After a batch closes, Step 10 states the batch just certified, the next batch's question range, and waits (interactive). It does not pre-audit the next batch. It does not summarize work it has not done. A response that closes batch *k* and also reports on batch *k+1* has violated MANDATE B and the scope assertion (§18) will have raised before delivery. In autonomous mode the pause is waived (batches run sequentially) but the per-question review, evidence writes, and the Phase-3 completion gate are unchanged (§18 / RXA-7a).

---

# §5 — The three audit lanes and the restraint principle

Every explanation section is judged in three lanes. A section passes only if it clears all three.

**Lane 1 — Correctness.** Is the explanation true, and does it justify the *right* answer? A correctness defect is a BLOCKER: the explanation teaches a falsehood or defends a wrong option/value. Correctness is established by independent re-derivation (§9), never by agreement with Step 9. Lane-1 defects include a wrong correct-answer, a wrong multi-select set, a wrong numerical value or range, an axiom that states a false principle, a deduction step that does not follow, and a wrong-option rationale that misidentifies why the option is wrong.

**Lane 2 — Sufficiency.** Does the explanation teach *why*, not merely *what*? A sufficiency defect is FIXABLE: the explanation reaches the right answer but leaves a learner unable to reproduce the reasoning — a deduction that leaps over the load-bearing step, a wrong-option note that only asserts the option is wrong without naming the specific error a student would make, a missing common-pitfalls entry on a numerical answer, an axiom that names no principle. Sufficiency is the teaching floor; §8 gives the per-section tests.

**Lane 3 — Proportion.** Is the explanation *to the point* — dense enough to teach, short enough to respect the reader? A proportion defect is FIXABLE and cuts **both** ways. Under-proportion is a density-floor failure: a one-line hand-wave where the class demands a worked derivation. Over-proportion is bloat: restating the stem, re-deriving what was already shown, padding with generic study advice, or repeating an option's rationale across sections. Lane 3 is where the auditor's own discipline matters most (see the restraint principle).

**The restraint principle.** An auditor's instinct is to add. That instinct is wrong more often than it is right. The density floor exists to guarantee teaching, not to license expansion; the proportion lane exists equally to *cut*. Every rectification must be the **minimal** change that clears all three lanes: fix the false step, supply the missing why, cut the bloat — and stop. A rectified explanation should, on average, be **shorter or the same length** as the original, not longer. Adding correct-but-unnecessary sentences to a section that already passed is itself a Lane-3 defect the auditor is introducing. When in doubt between two correct fixes, choose the shorter. This principle governs §16; a rectification that grows a clean section is rejected in re-verification review.

---

# §6 — Universal question classes and per-class checklists

Step 10 audits against the same ten universal question **classes** the whole pipeline shares (Step 9 §6-1). A class is a mode of reasoning, not an exam section: the same class check applies whether the question sits in a quantitative section of one exam or a technical section of another. This is what makes the audit exam-agnostic — the checking wisdom attaches to the class, and the class is inferred from the question's structure and the registry type, never from the section name.

The ten classes and the correctness question each one forces the auditor to answer:

- **C-COMPUTATIONAL** — a value is computed. Re-derive the value by an independent route (§9); does the axiom state the correct formula for this sub-class, and does every deduction step survive arithmetic re-execution?
- **C-FORMAL-LOGIC** — a rule is executed (syllogism, inequality chain, blood-relation, assertion-reason, coding-decoding). Re-run the rule; does the conclusion follow under the rule's own semantics, and is the negative-stem polarity handled correctly?
- **C-FACTUAL** — a fact is asserted (static knowledge, current affairs, domain facts). Externally re-verify the fact (§9); is it true as of the paper's reference frame, and is it uniquely the correct option?
- **C-VOCAB-ITEM** — a lexical judgement (synonym, antonym, idiom, one-word). Re-verify the sense; does the chosen option match the intended sense and not merely a near-neighbour?
- **C-GRAMMAR** — a grammatical judgement (error-spotting, fill-in, transformation). Re-apply the grammatical rule; is the correct option the one the rule selects, and does the wrong-option note name the specific rule each distractor violates?
- **C-LINKED** — a shared-stimulus set (reading comprehension, data-interpretation, a shared-premise cluster). Answer from the stimulus alone; is every answer entailed by the stimulus, and is the explanation free of outside knowledge the stimulus does not supply?
- **C-FIGURAL** — the stem or an option is an image (§11). View the image; does the explanation describe what is actually shown, and is the correct option the unique satisfier of the figural rule?
- **C-MATRIX/MATCH** — a matrix, matching or arrangement. Re-solve the assignment; is the mapping complete and consistent, and does the deduction bind every matched pair?
- **C-MULTI-SELECT** — a multi-select question (msq). Re-derive the full correct **set**; is the set exactly right (no missing correct option, no included wrong option), and does the last deduction step bind every selected option?
- **C-NUMERICAL-INPUT** — a numerical-answer question (nat). Re-derive the value; is it within the accepted range, does the last deduction step contain the value, and does each common-pitfall reconstruct to a plausible wrong value a real method would produce?

A question may carry more than one class (a computational reading-comprehension sub-question is both C-LINKED and C-COMPUTATIONAL); the audit applies every class that fits. Class is inferred, per question, from: registry type (mcq/msq/nat), presence of a figure (registry figural manifest ∪ figure note), a shared stimulus (linked-group manifest), and the reasoning the stem demands. The inferred classes are recorded on the ledger entry (§18) so the completion gate can require the class's evidence (figural→viewed image, factual/vocab→web source). §8.0 runs the universal checks; the per-class question above is answered inside §8's per-section audit.

---

# §7 — Phase 1: independent machine re-verification

Step 9's §18 self-audit runs `verify_fidelity`, `verify_structure` and `verify_explanations` and reports the result. Step 10 does **not** read that report. It re-runs the same three verifiers itself, on the delivered document, because a self-report is exactly the artifact an independent auditor must reconstruct rather than trust. Running them here also catches anything that changed between Step 9's self-audit and delivery, and anything Step 9's configuration reconstruction got subtly wrong.

Phase 1, in order:

1. `parse_solution_blocks(solutions, cfg)` → the reconstructed block set. A raise here is a structural defect (the document does not match the config the audit was told to use) and halts.
2. `verify_fidelity(solutions, paper, cfg)` → confirm every question region in the Solutions document is byte-identical to the paper: stem and option text, OMML `m:t` sequence, drawing counts, table grids, media MD5s, and that every image relationship resolves. Any failure is a fidelity defect (§15); it means Step 9 altered the paper while interleaving, which is a BLOCKER.
3. `verify_structure(solutions, blocks, cfg)` → confirm every expected question is explained exactly once, no explanation looks ahead beyond its own question, and every block re-validates structurally.
4. `verify_explanations(solutions, blocks, cfg)` → the independent post-render re-audit: header order, the answer-binding last deduction step (option / set / value, type-aware), wrong-section coverage, one sentence per prose paragraph, zero banned glyphs / metacommentary / templates / fake citations / banned blocks, zero inline or vulgar fractions, and document-wide OMML fraction well-formedness (numerator and denominator non-empty, no consecutive-year artifact). **This is the verifier the engine fraction-extraction fix corrects**: before the fix, a genuine digit/digit fraction was falsely reported malformed here; after it, real fractions pass and only truly empty fractions fail.

Phase 1 defects are recorded, not fixed in place: a fidelity or structure failure means the document's spine is wrong, and spine defects that trace to the paper escalate to Step 7/8 while spine defects that trace to the interleave are rebuilt wholesale before Phase 2 begins. Phase 1 must be clean (or its defects escalated) before per-question auditing starts, because Phase 2 relies on the reconstructed blocks being faithful.

Note the division of labour that v1.7 makes explicit: the three engine verifiers prove the **document** is well-formed and faithful; the completion gate (§18/§20) proves the **audit** was performed — every question reviewed with complete, evidence-bound records. Both are required to certify; neither substitutes for the other.

---

# §8 — Phase 2: per-question deep audit

For every question in the current batch, Step 10 runs the universal checks (§8.0) and then the per-section deep audit (§8.1–§8.7). Every check maps to a lane (§5) and, on failure, to a defect code (§15). Every question opens its ledger entry (§18) at the start of its audit and closes it — with its verdict, inferred classes, derivation routes, and evidence-file paths — only when every applicable check has run; a question left open (no verdict) fails the completion gate (CA3).

## S5-1 — §8.0 universal per-question checks

Applied to every question regardless of class:

- **Type-container match.** The registry type (mcq/msq/nat) matches the rendered container: mcq has a single-option correct-answer line and a why-wrong section keyed by the non-selected options; msq has a multi-option correct-answer line and a why-wrong section keyed by the non-selected options; nat has a value (and optional accepted range) correct-answer line and a common-pitfalls section. A mismatch is `TYPE-CONTAINER-MISMATCH` (BLOCKER): the explanation is built for the wrong question type.
- **Answer re-derivation.** The answer is re-derived from scratch (§9) and compared to the rendered correct answer. Disagreement is a Lane-1 BLOCKER: `CA-WRONG` (mcq), `MSQ-SET-WRONG` (msq), `NAT-VALUE-WRONG` or `NAT-RANGE-WRONG` (nat). The re-derivation and its route(s) are recorded on the ledger entry (CA4).
- **Answer-binding.** The last deduction step binds the answer the explanation itself claims — the selected option(s) by option-word-and-label, or the value for nat. A binding gap is `DEDUCTION-BIND-FAIL` (Lane-1/2).
- **Header order and presence.** Correct-answer line, then (figure note if figural), then axiom, then deduction, then optional speed hack, then why-wrong (mcq/msq) or common-pitfalls (nat). A disorder or a missing mandatory section is a structural defect (`SECTION-ORDER` / `SECTION-MISSING`).
- **Prose hygiene.** Every prose paragraph is exactly one sentence, free of banned glyphs, metacommentary, template filler, fake citations and banned blocks, with no inline or vulgar fraction. These are caught mechanically by `verify_explanations`; §8.0 confirms they are clean after any rectification too.

## S5-2 — §8.1 Correct-answer line audit

The correct-answer line is the explanation's headline claim. Re-derive independently (§9) and confirm the line names the right option, the right set, or the right value/range. For nat, confirm the displayed value and the accepted range are consistent with the re-derived value (the re-derived value lies inside the displayed range, and the range is not absurdly wide or inverted). A correct-answer line that disagrees with the re-derivation is the highest-severity defect Step 10 can find and gates the whole question's rectification: fix the answer first, because axiom, deduction and wrong-option notes all cascade from it (§16 coupling).

## S5-3 — §8.2 Figure-note audit (figural questions)

For every figural question (§11), the figure note must describe what the viewed image actually shows and must not smuggle in the answer as an unearned assertion. A figure note that mis-describes the image, or that is absent on a figural question whose reasoning needs it, is a defect (`FIGURE-NOTE-WRONG` / `FIGURE-NOTE-MISSING`). This audit is impossible without viewing the image; §11 makes the view mandatory and records it as evidence (the viewed-image path on the ledger entry — CA5).

## S5-4 — §8.3 AXIOM audit

The axiom must state the *principle* the question tests — the formula, rule, definition or property from which the answer follows — and must state it correctly. Two failure modes:

- **False axiom** (Lane-1 BLOCKER, `AXIOM-WRONG`): the stated principle is untrue or is the wrong principle for this question.
- **Restated stem** (Lane-2/3, `AXIOM-RESTATE`): the axiom repeats the question instead of naming a principle, teaching nothing. The test: could a student apply this axiom to a *different* question of the same class? If it only describes this question, it is a restatement, not an axiom.

## S5-5 — §8.4 DEDUCTION audit

The deduction must carry the reader from the axiom to the answer in steps that each follow, with the load-bearing step shown, and must end by binding the answer. Failure modes:

- **Broken step** (Lane-1 BLOCKER, `DEDUCTION-STEP-WRONG`): a step does not follow — an arithmetic error, an invalid rule application, a non-sequitur.
- **Leap** (Lane-2, `DEDUCTION-LEAP`): the step that actually determines the answer is skipped or compressed to the point a learner cannot reproduce it. The test: remove Step 9's chosen answer from view; can the deduction alone regenerate it? If a reader must already know the answer to follow the step, it leaps.
- **Binding gap** (Lane-1/2, `DEDUCTION-BIND-FAIL`): the last step does not bind the claimed option(s)/value.
- **Fraction rendering** (Lane-1, `FRACTION-INLINE`): any fraction in the deduction must be real OMML, never inline text. This is the section most affected by the engine fraction-extraction fix — with it, a rectified deduction can carry a genuine stacked fraction and still pass `verify_explanations`.

## S5-6 — §8.5 SPEED HACK audit

Audited for both existence and honesty; the full inclusion logic is §10. In summary: if a speed hack is present it must be a genuinely faster, genuinely distinct method that actually reaches the answer (a restated long method dressed as a shortcut is `FAKE-SPEED-HACK`, Lane-1/2); if a speed hack is absent but the question's class and content make one clearly warranted, its absence is `MISSING-SPEED-HACK` (Lane-2). The auditor determines "warranted" from its own second derivation (§10), not from whether Step 9 chose to include one.

## S5-7 — §8.6 WHY WRONG audit (mcq / msq)

The why-wrong section must, for each non-selected option, name the **specific** error that makes it wrong — the exact mistake a student would make to land on it — not merely assert that it is wrong. Failure modes:

- **What-not-why** (Lane-2, `WHY-NOT-WHAT`): the note says the option is wrong without naming the error. Template filler ("this option is incorrect") is the degenerate case and is also caught mechanically.
- **Wrong diagnosis** (Lane-1, `WHY-WRONG-DIAG`): the note names an error, but that error does not actually produce this option. The reproduce-check (§8.7) is the test.
- **Coverage gap** (structural, `WHY-WRONG-COVERAGE`): the keys are not exactly the non-selected options. Caught by `verify_explanations`; re-confirmed after any rectification.
- **Lead-class mismatch** (Lane-2/3, `LEAD-CLASS-MISMATCH`): the diagnosis is framed in a register alien to the question's class (a computational slip described as a vocabulary confusion, or vice versa), which misleads more than it teaches.

## S5-8 — §8.7 The reproduce-check (wrong-option and pitfall honesty)

For every wrong-option note (mcq/msq) and every common-pitfall (nat), Step 10 executes the *claimed* error and confirms it reproduces the *specific* distractor or wrong value. If the note says an option results from swapping two values, Step 10 performs that swap and checks the result equals that option; if the pitfall says forgetting to divide leaves a value, Step 10 checks that value is the one named. A claimed error that does not reproduce its target is a Lane-1 defect (`WHY-WRONG-DIAG` / `PITFALL-DIAG-WRONG`): the explanation teaches a diagnosis that is itself false. This is the sharpest wrong-option test in the pipeline and it is impossible to fake, because it is arithmetic, not assertion. The reproduce-check result is written to the evidence directory and its path recorded on the ledger entry (CA7).

## S5-9 — §8.8 COMMON PITFALLS audit (nat)

nat questions have no options to reject, so their teaching of error lives in common-pitfalls. Each pitfall must name a value a real (wrong) method would produce and the method that produces it (subject to the reproduce-check, §8.7). Failure modes: `COMMON-PITFALLS-MISSING` (nat with no pitfalls — Lane-2, a nat with zero pitfalls teaches no error), `COMMON-PITFALLS-THIN` (a single trivial pitfall where the question's method admits several distinct, instructive slips), and `PITFALL-DIAG-WRONG` (a pitfall whose method does not produce its stated value).

---

# §9 — Independent answer derivation

Correctness in Step 10 rests entirely on re-deriving each answer without reference to Step 9's conclusion. The derivation protocol is class-aware and evidence-producing.

**Derive-twice, then reconcile.** For every question, Step 10 derives the answer by two independent routes where the class admits two (a computational value by direct calculation and by estimation or dimensional check; a factual claim by two independent sources; a logical conclusion by forward and by elimination). The two routes must agree. If they agree, the answer is held with high confidence. If they disagree, Step 10 derives a third route and takes the two-of-three consensus, recording a `DERIVATION-CONFIDENCE` note. If no consensus emerges, the question is escalated (§16): Step 10 will not certify an answer it cannot itself establish, and it will not defer to Step 9 to break its own tie. The derivation routes are recorded on the ledger entry (`answer_derived` + `derivation_routes`), which the completion gate requires (CA4).

**Per-class derivation:**

- **C-COMPUTATIONAL / C-NUMERICAL-INPUT** — compute the value independently; cross-check by a second method (estimation, unit analysis, back-substitution). Re-execute every deduction step's arithmetic.
- **C-FORMAL-LOGIC / C-MATRIX/MATCH** — re-run the rule or re-solve the assignment from the premises; verify by elimination.
- **C-FACTUAL / C-VOCAB-ITEM** — externally re-verify against authoritative sources (§ web protocol below). Record each source and the exact claim it supports in `audit_web_sources.json` AND save the source under the evidence directory, its path on the ledger entry (CA6).
- **C-GRAMMAR** — re-apply the grammatical rule; confirm the correct option is the unique rule-satisfier.
- **C-LINKED** — answer strictly from the shared stimulus; confirm entailment and flag any step that requires outside knowledge (`LINKED-OUTSIDE-STIMULUS`).
- **C-FIGURAL** — view the image (§11) and derive the figural rule from what is shown; confirm the correct option uniquely satisfies it.
- **C-MULTI-SELECT** — derive the complete correct set, testing every option for inclusion independently; the set is right only if every inclusion and every exclusion is independently justified.

**Web-verification protocol.** Factual and lexical claims are confirmed against authoritative, current sources; the paper's reference frame (its intended "as of" date, from configuration) governs time-sensitive facts. Each consulted source is recorded with the specific claim it supports AND saved to the evidence directory. A claim that cannot be externally confirmed is marked `FACT-UNVERIFIABLE` rather than trusted; Step 10 never certifies a fact it could not verify, and never invents a citation to cover a gap (a fabricated citation is itself a defect the audit exists to prevent).

**The view is mandatory for figural questions.** No figural answer is derived, and no figural explanation is audited, without the image having been viewed and recorded (§11). A figural verdict on an unviewed image is not evidence; it is a guess, and Step 10 does not ship guesses. The completion gate (CA5) enforces this mechanically: a figural question with no viewed-image evidence file cannot certify.

---

# §10 — SPEED HACK inclusion audit

A speed hack is an optional faster method. Whether one *should* be present is a judgement Step 10 makes independently, and then it audits the actual state against that judgement — a two-by-two:

```text
                        speed hack SHOULD exist        speed hack should NOT exist
speed hack IS present   audit it for honesty (§8.5)    FAKE-SPEED-HACK if it is not
                        -> genuine & faster -> pass    genuinely faster/distinct
speed hack is ABSENT    MISSING-SPEED-HACK (Lane-2)    correct -> pass
```

**Determining "should exist" — the two-part test.** Step 10 forms its own shortcut candidate during derivation (§9) and asks:

1. **Distinct method** — is the candidate a genuinely different route to the answer, not a re-description of the main deduction? A "shortcut" that is the long method with words removed is not distinct.
2. **Genuinely faster** — does the candidate reach the answer in materially fewer steps or less computation for a test-taker under time pressure?

A speed hack should exist only if both hold. If Step 10's own candidate fails either test, then absence is correct and presence would be `FAKE-SPEED-HACK`.

**Class-weighted search intensity.** The effort Step 10 spends looking for a warranted shortcut scales with class:

- **Computational / numerical-input** — search hard; these classes most often admit a genuine shortcut (a ratio trick, a symmetry, a smart substitution), so a missing one is most often a real Lane-2 defect.
- **Factual / vocab** — there is rarely a "faster" way to know a fact; here a *present* speed hack is the suspicious case (usually `FAKE-SPEED-HACK`), and absence is almost always correct.
- **Linked / reading-comprehension** — a shortcut is usually redundant with the stimulus scan; presence is often bloat (Lane-3), absence usually correct.
- **Formal-logic / matrix** — sometimes a shortcut exists (a parity check, an elimination order); search moderately.

The point is that Step 10 does not treat "has a speed hack" or "has no speed hack" as inherently good or bad; it treats the *match between the class's shortcut-availability and the document's state* as the thing to audit.

---

# §11 — Figural deep audit

Figural questions are the pipeline's highest-risk explanations because their correctness cannot be judged from text alone.

**Union detection.** The figural set is the union of (a) questions the registry figural manifest marks figural and (b) questions whose Solutions region carries a figure note. Where the two disagree, the paper (registry ∪ actually-rendered image) wins: a question with an image in the paper is figural even if the registry missed it, and a question with a figure note is figural even if the manifest is silent. This union also catches questions whose **options** are images, not only questions whose **stem** is an image.

**The view is mandatory and recorded.** For every question in the figural set, Step 10 views every image involved — stem image and each option image — before deriving or auditing. Each view is saved to the evidence directory and its path recorded on the ledger entry (which images, viewed). An empty evidence record on a figural question is a **hard stop** for that batch and a completion-gate failure (CA5): Step 10 will not certify or rectify a figural explanation it has not visually grounded (§17 makes the empty record mechanically detectable).

**What the view establishes:**

- The correct option is the **unique** satisfier of the figural rule read from the image — not merely *a* satisfier. If two options satisfy the rule as drawn, the question has a defect that escalates to Step 7/8 (a figural question with a non-unique answer is a paper defect, not an explanation defect).
- The figure note describes what is actually shown (§8.2).
- The axiom, deduction and wrong-option notes are consistent with the image; a figural fix cascades through all of them (§16 coupling), because a corrected reading of the image can change every downstream section.

**Rendering constraints Step 10 preserves.** Figural options render as single-column vertical stacks (never a two-by-two or composite panel), decomposed into discrete per-option images at full resolution. Step 10 never re-renders or reflows figural content; it audits the explanation around the frozen figures, and its rebuild re-seeds the figures byte-identically from the paper (verified by `verify_fidelity`).

---

# §12 — Error-type taxonomy

Wrong-option notes and common-pitfalls are strongest when the named error is drawn from a shared vocabulary of how students actually err. Step 10 audits each diagnosis against this taxonomy (shared with Step 9 §9) and, via the reproduce-check (§8.7), confirms the named type actually produces the target:

- **value_swap** — two quantities exchanged.
- **sign_error** — a sign or direction flipped.
- **unit_error** — a unit or scale mishandled.
- **off_by_one** — a boundary or count off by one.
- **partial_truth** — true of part, asserted of the whole.
- **process_confusion** — the right idea, the wrong procedure.
- **reversed_relationship** — a dependency read backwards.
- **name_swap** — the right description attached to the wrong entity.
- **formula_error** — a wrong or mis-recalled formula.
- **rounding_trap** — a premature or wrong rounding.
- **polarity_flip** — a negative-stem or antonym polarity inverted.

A diagnosis that names a type but fails the reproduce-check is `WHY-WRONG-DIAG` / `PITFALL-DIAG-WRONG`. A diagnosis that names no type and no specific error is `WHY-NOT-WHAT`. The taxonomy is a checking aid, not a template: Step 10 does not force a note into a taxonomy word; it confirms the note's *actual* named error is specific and reproduces its target.

---

# §13 — Special-case audit protocols

- **Negative-stem questions.** When the stem asks for the option that is NOT true / is incorrect / is the exception, the correct-answer is the one that fails the property, and every wrong-option note must explain why that option *satisfies* the property (the polarity is inverted relative to a positive stem). Step 10 re-reads the stem polarity from the text, independently of Step 9, and confirms the whole explanation is written to the correct polarity; a polarity inversion is `polarity_flip` at the question level and is a Lane-1 BLOCKER.
- **Composite / multi-part options** ("both A and B", "all of the above", "none"). Step 10 evaluates each atomic component independently and confirms the composite verdict follows from the components; a composite whose explanation asserts the whole without resolving the parts is a Lane-2 defect.
- **Multi-select (msq).** The correct **set** is re-derived element-by-element (§9). The last deduction step must bind every selected option; the why-wrong section must cover exactly the non-selected options; and — the msq-specific trap — an option that is *partially* correct but not fully must be excluded and its note must explain the partial-truth (`partial_truth`). `MSQ-SET-WRONG` covers both a missing correct option and an included wrong one.
- **Numerical-input (nat).** The value is re-derived and checked against the accepted range; the last deduction step must contain the value; common-pitfalls replace why-wrong and are held to §8.8. The nat-specific traps are an accepted range that excludes the true value (`NAT-RANGE-WRONG`) and a value stated to a precision the method does not support (`rounding_trap`).
- **Linked groups.** A shared-stimulus group is audited as a unit and never split across a batch boundary (MANDATE B, §18). Every answer must be entailed by the stimulus; a step that needs outside knowledge the stimulus does not supply is `LINKED-OUTSIDE-STIMULUS`. A defect in the shared stimulus itself (not in a sub-question's explanation) escalates to Step 7/8 and is fixed once for the whole group.

---

# §14 — Cross-cutting scans

Some defects are invisible one question at a time and only appear across a batch or the whole paper. Step 10 runs these scans with batch context (and the paper-wide ones in Phase 3):

- **Second-correct-answer scan.** For each mcq, confirm no non-selected option is *also* fully correct under the stem; a genuine second correct answer is a paper defect (escalate to Step 7/8), but the scan lives here because it is Step 10's independent re-derivation that surfaces it.
- **Distractor-provenance scan.** Across a question's wrong-option notes, confirm each distractor is explained by a *distinct* error (not three options all blamed on the same slip), so the set of notes teaches the full error surface. A collapse to one repeated error is `LEAD-CLASS-MISMATCH` or a coverage-quality defect.
- **Inter-question leakage scan.** Confirm no explanation references another question's content, answer or numbering — each explanation must stand alone.
- **Factual-dedup scan.** Across the paper, confirm two different factual/vocab questions do not resolve to the same underlying fact with contradictory explanations (`FACTUAL-DEDUP-FAIL`).
- **Speed-hack genuineness scan.** Apply §10 across the batch so the present/absent judgement is consistent within a class.
- **Derivation-confidence scan.** Collect every `DERIVATION-CONFIDENCE` note; any question Step 10 could not confidently derive is surfaced in the report and, if unresolved, escalated.
- **Anomaly-justification scan.** If the Solutions document carries any internal anomaly signal, confirm it is justified; an unjustified anomaly escalates (Step 10 does not render anomalies — it resolves or escalates them).

---

# §15 — Defect classification

Every defect carries a code, the lane it belongs to (§5), a severity, and a disposition (fix here, or escalate). Severity **BLOCKER** means the explanation is false or defends a wrong answer; **FIXABLE** means the explanation is correct but insufficient or disproportionate. Disposition **FIX** means Step 10 rectifies it in the explanation (§16); **ESCALATE** means the root cause is in the question, not the explanation, and goes to Step 7/8.

| Code | Lane | Severity | Disposition |
|------|------|----------|-------------|
| CA-WRONG | Correctness | BLOCKER | FIX |
| MSQ-SET-WRONG | Correctness | BLOCKER | FIX |
| NAT-VALUE-WRONG | Correctness | BLOCKER | FIX |
| NAT-RANGE-WRONG | Correctness | BLOCKER | FIX |
| TYPE-CONTAINER-MISMATCH | Correctness | BLOCKER | FIX |
| AXIOM-WRONG | Correctness | BLOCKER | FIX |
| DEDUCTION-STEP-WRONG | Correctness | BLOCKER | FIX |
| DEDUCTION-BIND-FAIL | Correctness | BLOCKER | FIX |
| WHY-WRONG-DIAG | Correctness | BLOCKER | FIX |
| PITFALL-DIAG-WRONG | Correctness | BLOCKER | FIX |
| FIGURE-NOTE-WRONG | Correctness | BLOCKER | FIX |
| FRACTION-INLINE | Correctness | BLOCKER | FIX |
| FIDELITY-BREACH | Correctness | BLOCKER | ESCALATE |
| SECOND-CORRECT-ANSWER | Correctness | BLOCKER | ESCALATE |
| FIGURAL-NON-UNIQUE | Correctness | BLOCKER | ESCALATE |
| FACT-UNVERIFIABLE | Correctness | BLOCKER | ESCALATE |
| AXIOM-RESTATE | Sufficiency | FIXABLE | FIX |
| DEDUCTION-LEAP | Sufficiency | FIXABLE | FIX |
| WHY-NOT-WHAT | Sufficiency | FIXABLE | FIX |
| LEAD-CLASS-MISMATCH | Sufficiency | FIXABLE | FIX |
| WHY-WRONG-COVERAGE | Sufficiency | FIXABLE | FIX |
| COMMON-PITFALLS-MISSING | Sufficiency | FIXABLE | FIX |
| COMMON-PITFALLS-THIN | Sufficiency | FIXABLE | FIX |
| FIGURE-NOTE-MISSING | Sufficiency | FIXABLE | FIX |
| MISSING-SPEED-HACK | Sufficiency | FIXABLE | FIX |
| FAKE-SPEED-HACK | Sufficiency | FIXABLE | FIX |
| LINKED-OUTSIDE-STIMULUS | Sufficiency | FIXABLE | FIX |
| DENSITY-FLOOR-FAIL | Proportion | FIXABLE | FIX |
| BLOAT | Proportion | FIXABLE | FIX |
| SECTION-ORDER | Structure | FIXABLE | FIX |
| SECTION-MISSING | Structure | FIXABLE | FIX |
| FACTUAL-DEDUP-FAIL | Correctness | BLOCKER | ESCALATE |
| DERIVATION-CONFIDENCE | Correctness | BLOCKER | ESCALATE |

Disposition is a default, not a reflex: a BLOCKER whose root cause is the explanation is fixed; a BLOCKER whose root cause is the question is escalated. `CA-WRONG` with a correct paper key means the explanation defended the wrong option and Step 10 rewrites the explanation to the correct option; `CA-WRONG` where re-derivation shows the *paper key itself* is wrong is a question defect and escalates. §16 draws that boundary precisely.

---

# §16 — Rectification engine

Rectification is surgical, root-cause, verified, and minimal (the restraint principle, §5). It runs per batch, immediately after the batch's defects are classified, while the derivation is fresh (D6).

**The escalation boundary — explanation vs question.** Step 10 rectifies **explanation** text. It never edits a stem, an option, a figure or the paper's answer key. The test for every BLOCKER: *does the correct explanation exist for this question as printed?*

- If yes — the answer is derivable and correct, but the explanation got it wrong, insufficient or disproportionate — Step 10 rewrites the explanation (FIX).
- If no — the question itself is broken (two correct options, no correct option, a non-unique figural answer, a stem/option/key defect, an unverifiable fact) — Step 10 does not paper over it with prose. It records the defect and escalates to Step 7/8 (ESCALATE), because an eloquent explanation of a broken question is worse than none: it hides the breakage.

**The per-batch fix protocol:**

```text
For the current batch (context fresh from §8/§9 derivation):
  1. Order defects: answer-level first (CA/MSQ/NAT), then axiom, then
     deduction, then speed-hack, then wrong-option/pitfalls. Answer-level
     fixes cascade, so they are applied before the sections that depend on them.
  2. For each FIX defect, author the MINIMAL corrected section(s):
       - reconstruct the block with parse_solution_blocks (already in hand
         from §7);
       - replace only the defective section's sentences with corrected ones,
         leaving every clean section untouched (clean OMML, clean prose, clean
         figures are never re-authored);
       - honour coupling (below): if the answer changed, re-derive and rewrite
         every section that depends on it.
  3. For each ESCALATE defect, write the escalation record (question, code,
     evidence, the Step-7/Step-8 action needed) and leave the explanation
     unshipped for that question (the batch cannot close with an open BLOCKER).
  4. Rebuild: build_interleaved_docx(paper, corrected_blocks, audited_out, cfg)
     re-seeds every question region byte-identically from the paper and appends
     the corrected explanations.
  5. Re-verify the WHOLE document (MANDATE D): verify_fidelity, verify_structure,
     verify_explanations must all pass for the entire paper, not just the batch.
  6. Restraint review: confirm no rectified section grew a clean section and
     that each fixed section is shorter-or-equal on average (§5). A fix that
     bloats is reverted and re-authored tighter.
  7. Re-run parse_solution_blocks on the rebuilt document and confirm the fixed
     blocks now re-derive clean (the fix actually took).
  8. Write the question's ledger entry (§18): verdict FIXED, inferred classes,
     derivation routes, and the evidence-file paths (viewed image / web source /
     reproduce-check) — the record the completion gate reads (CA3-CA7).
```

**Coupling rules (cascade).** Sections are not independent; a fix in one forces a re-audit of those below it:

- **Answer changed** (CA/MSQ/NAT) → re-derive and rewrite axiom (must justify the new answer), deduction (must bind the new answer), speed-hack (must reach the new answer), and every wrong-option/pitfall note (the previously-correct option is now a distractor and needs a note; the previously-wrong-now-correct option loses its note).
- **Axiom changed** → re-audit deduction (it must follow from the new axiom).
- **Figure reading changed** (§11) → re-audit axiom, deduction and wrong-option notes (all read from the image).
- **Deduction step changed** → re-audit the binding and any wrong-option note whose reproduce-check depended on the changed arithmetic.

**Why full-rebuild is safe for OMML.** The engine is the only writer of explanation prose, and it emits OMML only as digit/digit fractions (`add_math_text`); the reader maps those back to `num/den` losslessly and raises on any other OMML, so a clean section round-trips exactly and a rebuilt document carries genuine stacked fractions that pass `verify_explanations` (post the fraction-extraction fix, §7). Clean sections are reconstructed and re-emitted identically; only defective sections carry new prose, and that new prose passes through the same guards Step 9 used.

---

# §17 — Quality-consistency (anti-decay) architecture

The failure mode this section defends against is *silent late-run decay*: an auditor that judges question 5 with full rigour and question 95 with a tired shrug, shipping a document that is audited in name only past the halfway point. Five mechanisms, layered, make decay either impossible or immediately detectable.

1. **Batching for fresh context (MANDATE B).** One batch per response means every batch is judged with the same context budget as the first. Late questions are not audited at the end of a long, degraded context; they are audited at the start of their own response. This protects the *quality* of the work that is done.

2. **A mechanical per-question evidence gate.** Every question writes an evidence record before it can be certified: the re-derived answer and its route(s), the web sources (for factual/vocab), the viewed images (for figural), the reproduce-check results (for wrong-option/pitfall). An empty required field is a detectable hole: a figural question with no viewed image, a factual question with no source, a wrong-option note with no reproduce-check result cannot be marked clean. **v1.7: this is enforced mechanically at Phase 3 by `explain_audit_gate.py` (CA4–CA7) reading the §18 ledger + evidence files — not by self-attestation.** This protects against work being *skipped*.

3. **Zero-sampling coverage assertion.** Step 10 never audits a sample. The ledger asserts that every question in every closed batch has a complete evidence record; a batch cannot close with any question un-evidenced. Coverage is all-or-nothing per batch, and the batches tile the paper exactly. **v1.7: the completion gate makes this a command result — CA1 (every planned batch closed) + CA2 (coverage exact 1..total_questions) fail a collapsed or partial run.**

4. **Whole-document re-verification every batch (MANDATE D).** After each batch, the *entire* document is re-verified, not just the batch. This catches any regression a batch's rebuild introduced elsewhere and means the document is provably clean-so-far at every checkpoint, not merely clean-in-the-last-slice.

5. **Resume-safe disk state.** The ledger, defect log, answer keys, web sources and the evidence directory are on disk (§18), so an interrupted run resumes exactly where it stopped with full evidence intact — no re-audit from memory, no silent gap where a crash landed.

**Gates catch skipped work; batching protects done work.** The distinction matters: mechanisms 2–4 make it impossible to *skip* a question or a check without detection (now mechanically, via the completion gate); mechanism 1 makes the work that *is* done as good on the last batch as the first. Both are necessary; neither alone suffices.

---

# §18 — Batch architecture and state files

**The frozen batch plan.** At pre-flight P6, Step 10 derives the batch plan from the blueprint's per-section question ranges and freezes it to `audit_progress.json`. The plan tiles the whole paper into ordered batches of at most `EXPLAIN_AUDIT_BATCH_SIZE` (default 10) questions. The ceiling has exactly one exception: an atomic linked group that would be split by a boundary is kept whole in one batch even if that pushes the batch over the ceiling (§13). The plan is derived once and never recomputed; recomputing mid-run is how a resumed run silently re-tiles and drops or double-audits questions.

**One batch per response (MANDATE B / RXA-7b).** Each response completes exactly one batch: derive, audit, rectify, rebuild, re-verify, write the ledger entries, advance the ledger, halt. The batch size is a ceiling, not a quota — a batch may be smaller (a short trailing section, or a linked group handled alone), but it is never larger except for the linked-group case.

**AUTONOMOUS (headless) mode — PACING WAIVER ONLY (RXA-7b).** When the user or a project-memory preference requests non-interactive / end-to-end / "don't pause" execution, the inter-batch pause is waived and Batches 1..K run SEQUENTIALLY within the one session; the per-batch structure (derive, audit, rectify, rebuild, re-verify, write ledger entries, advance) is UNCHANGED, and every question still gets its complete, evidence-backed ledger entry (RXA-7a — the WHAT is never waived, RXA-0). Phase 3 still runs the completion gate. A run that finishes "fast" by collapsing Phase 2 is a MANDATE B violation, not a valid autonomous run — CA1/CA2 fail it. Autonomous mode changes WHEN work is reported, never WHETHER it is done.

**The pre-delivery scope assertion.** Before a response ends, Step 10 asserts that the progress ledger advanced by *exactly* the current batch's slice — the same set of question numbers the frozen plan assigned to this batch (interactive: one batch; autonomous: the ledger still advances one batch at a time internally). If the ledger advanced by more (a look-ahead into the next batch) or by less (an incomplete batch), the assertion raises and nothing is delivered. At Phase 3 the completion gate re-checks this globally (CA1/CA2): to certify, every planned batch must be closed and the questions must be exactly 1..total_questions — a single-response full run that skipped the per-question review cannot pass.

**The ledger schema (load-bearing — validated by `explain_audit_gate.py`).**

```text
audit_progress.json:
  { mock, total_questions, evidence_dir,
    batch_plan:      [[q, ...], ...],         # frozen tiling of 1..total_questions
    batches_closed:  [batch_index, ...],      # advanced by exactly one per response
    questions: { "<q>": {
        verdict: CLEAN | FIXED | ESCALATED | UNVERIFIED,
        classes: [ C-COMPUTATIONAL, C-FIGURAL, C-FACTUAL, ... ],   # inferred (§6)
        answer_derived: bool, derivation_routes: [ ... ],          # §9 (>=1)
        viewed_images:    [ evidence path, ... ],   # figural (RXA-8 / §11)   -> CA5
        web_sources:      [ evidence path, ... ],   # factual/vocab (RXA-12 / §9) -> CA6
        reproduce_checks: [ evidence path, ... ],   # wrong-option/pitfall (§8.7) -> CA7
    } } }
```

Every evidence path resolves to an EXISTING, non-empty file under `evidence_dir` — the completion gate checks the FILES, not just booleans (a stamp with no backing file is treated as un-audited, RXA-16). The completion gate (CA1–CA7) is the machine reading of §17 mechanisms 2 and 3 and this scope assertion.

**State files (all on disk, resume-safe):**

- `audit_progress.json` — the frozen batch plan and the ledger (which batches closed, which questions evidenced, the next batch's range). The resume anchor AND the completion-gate input.
- `audit_answer_keys.json` — Step 10's independently re-derived answers, per question, with derivation route(s) and confidence (D1).
- `audit_defect_log.json` — every defect: code, lane, severity, disposition, the before/after of each fix, and each escalation record.
- `audit_web_sources.json` — every external source and the exact claim it supports (§9).
- `evidence_dir/` — the saved viewed-image montages, web-source captures, and reproduce-check traces the ledger paths point at.

The evidence record for a question (mechanism 2 of §17) is the union of that question's ledger fields plus the files they name; "complete" means every field the question's classes require is populated AND its file exists — exactly what `explain_audit_gate.py` asserts.

---

# §19 — Verdict decision table

Per question, after §8–§14, Step 10 assigns one verdict:

```text
CLEAN        every lane passes; evidence record complete; no defect.
             -> no change to the document for this question.

FIXED        one or more FIX defects found and rectified in this batch;
             the rebuilt document re-verifies; the fixed sections re-derive
             clean; restraint review passed.
             -> corrected explanation shipped in the audited document.

ESCALATED    at least one ESCALATE defect (the question, not the explanation,
             is broken); escalation record written; explanation left unshipped
             for this question until Step 7/8 resolves the paper defect.
             -> batch cannot close CLEAN/FIXED while this is open; the run
             surfaces the escalation and halts the affected question.

UNVERIFIED   Step 10 could not confidently derive the answer (no derivation
             consensus, or a fact it could not verify); recorded as
             DERIVATION-CONFIDENCE / FACT-UNVERIFIABLE and escalated.
             -> never certified; Step 10 does not ship an answer it cannot
             itself establish.
```

A batch closes only when every question in it is CLEAN or FIXED. Any ESCALATED or UNVERIFIED question holds the batch open and is surfaced in the report (§21) for resolution before Step 10 can certify the mock. The completion gate (CA3) refuses to certify while any question is ESCALATED/UNVERIFIED.

---

# §20 — Delivery

Delivery happens once (MANDATE D), in Phase 3, after the last batch closes clean:

1. **COMPLETION GATE (v1.7): `explain_audit_gate.py --audit-progress [ExamCode]_Mock[N]_audit_progress.json` → MUST print `AUDIT-COMPLETION-GATE: PASS` (CA1–CA7).** A non-PASS forbids delivery (MANDATE D) and names the failing assertion + question numbers; the run resolves it (re-open the batch / supply the missing evidence / resolve the escalation) and re-runs the gate.
2. Final whole-document re-verification: `verify_fidelity`, `verify_structure`, `verify_explanations` pass for the entire paper.
3. Every question is CLEAN or FIXED; no ESCALATED/UNVERIFIED question remains open (any that do are resolved via Step 7/8 and re-audited, or the mock is returned as not-yet-certifiable with the open list).
4. Sidecars finalized: `audit_answer_keys.json`, `audit_defect_log.json`, `audit_web_sources.json`, `audit_progress.json` (marked complete), and `EXPLAIN_AUDIT_LEARNINGS_v1.md` (§24).
5. Present `[ExamCode]_Mock[N]_Solutions_Audited.docx` exactly once, with the end-of-mock report (§21). The input Solutions document is never presented as the output and is never modified (D5).

Nothing is presented before the completion gate prints PASS and every batch has closed clean; a partial audited document is not a deliverable.

**Post-delivery footer (MANDATORY after present_files):**
After the present_files call and end-of-mock report (§21), render the standardized visual
delivery footer as the LAST element in the response. Follow Framework_DeliveryFooter.md
for footer type (F2 step-complete — always for Step 10 since it delivers once), file badge
(Use locally for Solutions_Audited.docx), and next-step reference.

---

# §21 — End-of-mock report

The report is the one place Step 10 speaks at length in chat, and it carries status and evidence, never authored explanation prose (MANDATE 0). It is structured as numbered report sections so it is skimmable and complete:

- **§R1 — Scope.** Exam, mock, question count, batch plan, questions audited.
- **§R2 — Machine verification.** Phase-1 results, the final whole-document verification results, and the completion-gate result (`AUDIT-COMPLETION-GATE: PASS`, CA1–CA7).
- **§R3 — Verdict summary.** Counts of CLEAN / FIXED / ESCALATED / UNVERIFIED.
- **§R4 — Defects fixed.** Per code, how many, with a representative before/after described (not the full prose — the transcript is not the document).
- **§R5 — Escalations.** Every ESCALATE/UNVERIFIED question, its code, the evidence, and the Step-7/Step-8 action required.
- **§R6 — Derivation confidence.** Any question derived at less than full confidence, and how it was resolved.
- **§R7 — Coverage assertion.** The evidence-completeness statement: every question in every closed batch fully evidenced (§17), backed by the completion gate (CA2/CA4–CA7).
- **§R8 — Learnings.** The recurring defect classes emitted to the learnings file (§24).

The report asserts, in plain terms, that the audited document is certified clean (the gate printed PASS), or names precisely what prevents certification (the failing CA-assertion + questions).

---

# §22 — Definition of done and hard invariants

Step 10 is done for a mock only when **all** of the following hold:

1. Pre-flight P0–P9 passed (engine honest 47/47 + 10/10; completion gate honest 8/8; config complete, round-trip clean).
2. Every question audited in a frozen batch; zero questions sampled or skipped; every closed batch fully evidenced (§17).
3. Every answer independently re-derived (D1); no answer taken from Step 9; no key sidecar read (none exists).
4. Every explanation section cleared all three lanes (§5), or was rectified until it did, or its question was escalated.
5. Every figural explanation grounded in a viewed image with a recorded evidence entry (§11); no figural verdict on an unviewed image.
6. Every wrong-option note and pitfall passed the reproduce-check (§8.7).
7. Every fraction is real OMML; no inline or vulgar fraction survives (§8.4, §7).
8. The audited document passes `verify_fidelity`, `verify_structure`, `verify_explanations` for the whole paper at final verification (MANDATE D).
9. Every rectification was minimal and root-cause; no clean section was bloated (the restraint principle, §5).
10. The document is exam-agnostic clean: no exam-specific value entered any audit judgement; every exam fact came from configuration.
11. Delivered once (MANDATE D), with all sidecars and the end-of-mock report (§20, §21).
12. **The completion gate printed `AUDIT-COMPLETION-GATE: PASS` (CA1–CA7) before `present_files` (MANDATE D). A self-declared clean never certifies; a collapsed or partial Phase-2 run fails CA1/CA2 and cannot ship.**

**Hard invariants (never violated):**

- The input Solutions document is never modified in place; the output is a new file (D5).
- The paper (stem, options, figures, answer key) is never edited by Step 10; question defects escalate (§16).
- No explanation content is authored in the chat transcript (MANDATE 0).
- The engine is the only read/write path for the docx (MANDATE A); no hand-parsing, no hand-writing. The completion gate reads only the JSON ledger + evidence files, never the docx.
- One batch per response interactively; the scope assertion holds; autonomy waives the pause only (MANDATE B, §18, RXA-7).
- Nothing is delivered until the whole document verifies clean AND the completion gate prints PASS (MANDATE D).

---

# §23 — Known limitations and scope

- **Step 10 audits explanations, not papers.** A defect in the question itself is escalated, not fixed here (§16). Step 10 makes paper defects *visible and precise*; Step 7/8 fixes them.
- **Web verification depends on source availability.** A fact no authoritative current source confirms is marked `FACT-UNVERIFIABLE` and escalated, not guessed (§9). Step 10's factual confidence is bounded by what can be verified, by design.
- **Figural judgement depends on the view.** Step 10's figural audit is only as good as the image it viewed; an unviewable image halts the affected question (§11) rather than being audited blind.
- **The learnings loop is closed as of v1.1.** Step 10 emits the learnings file and Step 9 consumes it at P1 (Step 9 §24 / RE-22); the producer schema (§24) is pinned to the consumer. Promotion is threshold-gated (≥2 occurrences), so a one-off defect is logged but does not yet become a standing rule.
- **The reader assumes engine-written explanations.** `parse_solution_blocks` supports exactly the OMML the engine emits (digit/digit fractions) and raises on anything else, rather than guessing. A Solutions document hand-edited outside the engine may not round-trip; P4 detects this and halts.
- **Completion-gate residual (v1.7).** The gate verifies that each class-required evidence file EXISTS and is non-empty — it cannot prove the model reasoned correctly INSIDE that evidence (that a saved source supports the fact, that a viewed montage was truly scrutinised). Evidence-binding shrinks the residual to "the model would have to produce every montage, saved source and reproduce-check trace — i.e. perform the audit — in order to fake having performed it," the structural ceiling of an LLM-driven audit (parallel to Framework_MockTestCreateAudit.md §19).

---

# §24 — The learnings feedback loop

Step 10 emits and maintains `[ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md`: the accumulating record of recurring explanation defects, fed back into Step 9 so the same mistake is not authored again. The loop is **closed** — Step 9 loads this file at its P1 and applies every applicable rule while authoring (Step 9 §24 / RE-22). Because a silent producer↔consumer desync is precisely the failure this project guards against, the emission schema below is **pinned** to Step 9's consumer contract (Step 9 §24 S24-1); if either side changes, both change in the same pass.

**The promotion threshold.** At the end of a mock's audit, for every defect code Step 10 fixed **two or more times** in that mock, it writes or updates one rule. A single occurrence is recorded in the defect log (§18) but does not yet earn a standing rule — the threshold keeps the file signal, not noise.

**The pinned AL-rule schema.** Each rule is a markdown block headed `## AL-<id> — TITLE` carrying exactly these fields, which Step 9's `parse_learnings` extracts verbatim: **Defect code** (the universal-taxonomy code — the routing key, never a section name), **First seen** (Mock N, Q#), **Occurrences** (`k of m` in the promoting mock), **Pattern** (what went wrong and why it recurs), **Prevention rule** (the obeyable authoring change), and **Verification** (the one-line self-check). Rules are grouped in the file for human readability, but the machine contract keys off the defect code, so the loop is exam-agnostic.

**Accumulate, never delete.** Rules accumulate across mocks. A rule is retired only by an explicit `Supersedes: AL-<id>` annotation on a newer rule; silent deletion is forbidden (it would reopen a closed defect). The filename version advances only on an incompatible schema change; Step 9 loads the highest version present.

---

# §25 — T2 coverage map

Step 10 generalizes the proven SSC-CGL-Tier-2 explanation-audit reference (`T2_MockExplainAudit`) into an exam-agnostic form. This map records where every part of the reference lands, so the migration is provably complete rather than asserted complete. The principle: keep the reference's checking *wisdom*, attach it to universal classes and configuration instead of to SSC section names and the answer-key input.

**Carried over essentially unchanged (already exam-independent):**

- The reference's Part A / Part B / Part C structure → §7 (machine re-verification) / §8 (per-question deep audit) / §14 (cross-cutting scans).
- Its universal checks (re-derive independently, three-way binding, back-substitute wrong options, axiom-not-restatement, deduction arithmetic, wrong-option reproduce-check, negative-stem polarity, banned template/metacommentary/fake-citation) → §8.0, §8.4–§8.8, §13.
- Its cross-cutting scans (second-correct-answer, negative-stem polarity, composite-options, speed-hack genuineness, inter-question leakage, derivation-confidence resolution, anomaly justification) → §14.
- Its per-batch fix protocol (display, rebuild the block, re-verify, proceed; corrected document grows incrementally) → §16.
- Its hard invariants and state-file model → §18, §22.

**Generalized (exam-specific → configuration-driven):**

- Fixed SSC sections and counts and the fixed batch schedule → derived from `blueprint.json` section ranges (§18); nothing hardcoded.
- The reference's per-section sub-type checklists (its dozens of section-specific checks) → collapsed onto the ten universal classes (§6); each sub-type check is re-expressed as the class check it always was (a compound-interest check and a discount check are both C-COMPUTATIONAL axiom-correctness; an assertion-reason check and an inequality check are both C-FORMAL-LOGIC rule-execution).
- Exam-specific defect codes → generic codes: the reference's separate general-awareness and computer-section wrong-answer codes → `CA-WRONG` with class context; its two unverifiable-fact codes → `FACT-UNVERIFIABLE`; its reading-comprehension-outside-knowledge code → `LINKED-OUTSIDE-STIMULUS`; its computer-section dedup code → `FACTUAL-DEDUP-FAIL`.
- Its exam-specific rule tags (option-scrambling, inter-question leakage, one-rule-per-distractor, vocabulary/grammar dedup) → configuration-driven cross-cutting scans (§14) and the distractor-provenance scan.

**Added (the reference predates msq/nat; it was single-answer only):**

- Multi-select: `MSQ-SET-WRONG`, the set re-derivation and full-set binding (§13, §6 C-MULTI-SELECT).
- Numerical-input: `NAT-VALUE-WRONG`, `NAT-RANGE-WRONG`, `COMMON-PITFALLS-MISSING`, `COMMON-PITFALLS-THIN`, the pitfall reproduce-check (§8.7/§8.8, §13).
- Type-container matching across three types: `TYPE-CONTAINER-MISMATCH` (§8.0).
- The explicit sufficiency and proportion lanes and their codes: `WHY-NOT-WHAT`, `DEDUCTION-LEAP`, `LEAD-CLASS-MISMATCH`, `BLOAT`, `DENSITY-FLOOR-FAIL`, and the restraint principle (§5).
- The mechanical completion gate (v1.7): `explain_audit_gate.py` / CA1–CA7 — the reference certified by self-attestation; Step 10 certifies by a command over an evidence-bound ledger (§18/§20).

**Dropped (deliberately, by design):**

- The `answer_keys.json` input. The reference required Step 8's key as input; Step 9 delivers no key, so Step 10 re-derives independently and builds its own (D1). This is a cleaner independence property, not a lost capability.
- In-document anomaly rendering. The reference rendered anomalies into the document; Step 10 resolves or escalates them (§14) and renders none, because an explanation document should not carry unresolved anomaly annotations to a student.

Every reference defect code and every reference sub-type check has a home above: carried, generalized, or added-alongside; the only two deliberate drops are the key input and anomaly rendering, both replaced by a stronger mechanism.

---

# AUDIT RULES (RXA)

The rules below are the enforceable contract; the sections above are their rationale. Each rule is terse by design.

```text
  RXA-0  PRECEDENCE. No user preference, project-memory note, or autonomy /
         "don't-pause" instruction may reduce audit COVERAGE (RXA-7a) or weaken the
         COMPLETION GATE (MANDATE D / §20). Such instructions may ONLY change PACING
         (RXA-7b — skip the inter-batch pauses) and report verbosity. When a
         preference appears to conflict with a HARD rule, the HARD rule wins and the
         preference is applied to pacing/reporting only.
  RXA-1  Re-derive every answer independently (§9); never read Step 9's answer as
         input to the derivation, and never read a key sidecar (none is delivered).
  RXA-2  Re-run verify_fidelity, verify_structure, verify_explanations in Step 10
         (§7); never trust Step 9's §18 self-report.
  RXA-3  Read only through parse_solution_blocks and write only through
         build_interleaved_docx, both driven by the reconstructed EngineConfig
         (MANDATE A). No hand-parsing, no hand-writing. (The completion gate reads the
         JSON ledger + evidence files only, never the docx — it is not a write path.)
  RXA-4  Judge every section in all three lanes — correctness, sufficiency,
         proportion (§5). A section passes only if it clears all three.
  RXA-5  Every rectification is minimal and root-cause (the restraint principle);
         never bloat a clean section; prefer the shorter of two correct fixes.
  RXA-6  Fix in the same batch that finds the defect, while context is fresh (D6);
         rebuild and re-verify the whole document before the batch closes.
  RXA-7a EXHAUSTIVENESS (the WHAT). Every question is audited across all three lanes
         and leaves a COMPLETE, evidence-backed ledger entry (§18); zero sampling.
         Holds in EVERY mode; no preference may waive it (RXA-0). Mechanically
         enforced by the Phase-3 completion gate (CA2/CA3 + the CA4–CA7 evidence checks).
  RXA-7b PACING (the WHEN). Interactively, one batch = one response, each ending on an
         explicit continue; the pre-delivery scope assertion (§18) confirms the ledger
         advanced by exactly this slice. In AUTONOMOUS mode (§18) the pause is waived and
         batches run sequentially in one session — RXA-7a still holds for every question.
  RXA-8  View every figural image before deriving or auditing it (§11); an empty
         viewed-image record is a hard stop for the batch and a completion-gate failure (CA5).
  RXA-9  Run the reproduce-check on every wrong-option note and pitfall (§8.7); a
         diagnosis that does not reproduce its target is a Lane-1 defect; its result is
         recorded as evidence (CA7).
  RXA-10 Every fraction is real OMML (§8.5); no inline or vulgar fraction ships.
  RXA-11 Rectify explanations only; escalate question defects to Step 7/8 (§16).
         Never write an eloquent explanation of a broken question.
  RXA-12 Verify a fact against authoritative current sources or mark it
         FACT-UNVERIFIABLE (§9); never invent a citation; save the source as evidence (CA6).
  RXA-13 Determine speed-hack "should-exist" from Step 10's own second derivation
         (§10), not from whether Step 9 included one.
  RXA-14 Keep atomic linked groups whole across batch boundaries (§13, §18).
  RXA-15 No exam-specific value enters any audit judgement; every exam fact is
         read from configuration (exam-agnostic guarantee).
  RXA-16 Every question carries a complete evidence record — each named evidence file
         EXISTING and non-empty — before it is certified (§17/§18); an empty required
         field or a missing file blocks the batch and fails the completion gate.
  RXA-17 Deliver once, whole-document-clean AND completion-gate PASS (MANDATE D); a
         partial audited document is not a deliverable.
  RXA-18 Emit the learnings file every run (§24); wiring Step 9 to consume it is a
         flagged follow-up, not a silent assumption.
  RXA-19 Certification is a COMMAND RESULT, not a self-judgment: Phase 3 runs
         explain_audit_gate.py --audit-progress and it MUST print
         AUDIT-COMPLETION-GATE: PASS before present_files (MANDATE D / §20).
```

---

# APPENDIX A — The universal engine + the completion gate (single source of truth)

Step 10 runs two canonical, exam-agnostic Python artifacts. To avoid the multi-copy drift that enabled the Step-8 false-clean (see Framework_MockTestCreateAudit.md v2.6 / §21), the runnable code is NOT re-embedded here; it lives in ONE place each and this section points to it:

- **`explain_engine.py`** — the universal explanation engine (the ONLY docx read/write path, MANDATE A). It carries `EngineConfig`, `ExplanationBlock`, `add_math_text`, `parse_paper`, `build_interleaved_docx`, `verify_fidelity`, `verify_structure`, `verify_explanations`, `strip_solutions`, the Step-10 reader `parse_solution_blocks`, and `parse_learnings`. Self-tests: `--self-test` → `SELF-TEST: 47/47 PASS` (core), `--self-test-audit` → `AUDIT-SELF-TEST: 10/10 PASS` (reader round-trip). Pre-flight P0 requires both green. This is the same file Step 9 uses.

- **`explain_audit_gate.py`** — the mechanical Phase-3 COMPLETION GATE (v1.7). It reads `audit_progress.json` (§18) + the evidence sidecars and asserts CA1–CA7 (evidence-bound). It touches no docx and needs no python-docx. Self-test: `--self-test` → `COMPLETION-SELF-TEST: 8/8 PASS` (fixtures: clean-pass, skipped-Phase-2 [CA1+CA2], partial-review [CA2], open-verdict [CA3], unviewed-figure [CA5], missing-evidence-file [CA5], unsourced-fact [CA6], not-derived [CA4]). Pre-flight P0 requires it green; Phase 3 (§20) requires `AUDIT-COMPLETION-GATE: PASS`.

  Invocation at Phase 3:
  ```
  python3 explain_audit_gate.py --audit-progress [ExamCode]_Mock[N]_audit_progress.json
      → AUDIT-COMPLETION-GATE: PASS   (else exit 1, delivery forbidden — MANDATE D)
  ```

Both files are delivered alongside this spec and uploaded to the [ExamCode] project. The framework linter (`validate_framework_md.py`) runs each file's `--self-test`. Never patch either by hand — regenerate from the canonical source. (Historical note: through v1.6 the engine listing was reproduced verbatim in this Appendix "for self-containment"; v1.7 replaces that with this pointer to end the multi-copy drift, exactly as Step 8 v2.6 did for its auditor.)

---

**End of Framework_MockTestExplainAudit.md (v1.7)**
