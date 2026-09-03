# SPEC_HISTORY v1.0 — per-spec version history, moved off the execution path

GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, Wave 2 (partial). Framework_PYQCore EC-P42
prices SPECIFICATION-READ COST as a session resource. Every routed spec carried its
entire version history in a comment block at the top of the file, so an EXECUTING
session paid for the complete EDITORIAL record before it could do any work — 283,247 B
across the 23 specs, of which 196,024 B is history of releases that have already
shipped.

THE NARRATIVE IS NOT WASTE AND IS NOT DELETED. The v2.39 record is explicit about why:
five sessions paraphrased the spec and silently repaired bugs; the one session that
executed the fences verbatim found a P0 no other session hit. The defect archaeology is
why this corpus stopped regressing. It is moved, byte-for-byte, into this file — which
is tracked in MANIFEST.json and verified by bootstrap.py exactly as a spec is, and is
routed to NO trigger, so it is never read during execution.

WHAT STAYED BEHIND in each spec: line 1 (the version header bootstrap verifies), the
CURRENT version's entry (Z-VERSION requires the highest changelog entry to equal the
header), and every STRUCTURAL block — MINIMUM COMPANION VERSIONS, step-number notes,
and anything else that is operational rather than historical. Only entries for versions
ALREADY SUPERSEDED were moved.

To read the full history of a spec: find its section below. Entries are verbatim,
newest first, exactly as they appeared in the file.

---

## Framework_Blueprint.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_Blueprint.md.

```
# v1.47.0 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v1.46.0 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v1.45.0 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: the exemption became the budget.
#   v2.26 replaced `has_img = any(...)` with a rate and then decided REDUCIBILITY
#   with a fresh any(). One question in a 22-year corpus made a subtopic permanently
#   exempt, and irreducible grants pass even over budget by design. First real
#   PYQExtract run: 21 of 133 subtopics exempt, 14.3 figures/mock against a budget
#   of 5, 13 of 15 mocks over. Reducibility is now rate-based (figural_rate >= 0.50
#   AND option_image_rate >= 0.50) -> 3 subtopics, 1.5 forced, 0 mocks over.
#   Figures are now SCHEDULED at measured frequency rather than forced at render
#   time, the audit band is the exam's own volatility, and per-mock targets follow
#   the exam's observed shape. No feasibility halt exists or is needed.
# v1.44.0 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v1.43.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   B3's deliverable set drops from 6 files to 5: [ExamCode]_ExplainAuditLearnings.md is
#   NO LONGER GENERATED (§13-6), because its only filler — canonical Step 10 — is retired.
#   An ExplainAuditLearnings file already accumulated in an exam project STAYS VALID and is
#   still loaded and obeyed by Step 9; never delete one.
#   §13-7A is KEPT IN FULL: audit_canonical.py remains the single canonical auditor and B3
#   still copies it verbatim to [ExamCode]_mock_test_audit.py. What changed is who runs it —
#   Step 7 only, and optionally, which means an absent audit.py now leaves the paper with no
#   machine gate at any step. Every "audited within tolerance at Step 8" advisory in this
#   file is restated as "audited within tolerance by Step 7's audit.py"; the engine copy
#   duty (blueprint_core.py + figural_core.py from $FW) moves from Step 8 to Step 7.
#   EDITOR CAUTION added at the internal/canonical step map: this file uses "Step 8" for its
#   own B3 sub-steps as well, and those must never be mass-replaced.
#
# v1.42.8 — 2026-08-02 — self-test count refresh only (107/107 -> 139/139).
#   The five LIVE normative sites still quoted "the v2.13 canonical build prints
#   107/107" as the expected auditor count. That was stale twice over (the canonical
#   is v2.21.7 at 139/139) and misattributed the version. Historical changelog lines
#   below are left EXACTLY as written — they record what was true at their release
#   and are not restated. AUTH_GATE_FLOOR stays 35: the count is informational, the
#   floor is the binding condition, and that is now stated at each site so the next
#   count change does not require another sweep.
# v1.42.7 — 2026-08-01 — self-test count refresh only (105/105 -> 107/107).
# v1.42.6 — 2026-08-01 — self-test count refresh only (97/97 -> 107/107).
# v1.42.5 — 2026-08-01 — self-test count refresh only (89/89 -> 107/107, D2+D4 vision
#   fixtures). AUTH_GATE_FLOOR unchanged at 35.
# v1.42.4 — 2026-08-01 — self-test count refresh only (78/78 -> 107/107, C1
#   checkpoint fixtures). AUTH_GATE_FLOOR unchanged at 35.
# v1.42.3 — 2026-08-01 — SELF-TEST COUNT REFRESH ONLY (documentation; zero rule
#   change). audit_canonical.py gained five C5 fact-record fixtures at
#   Framework_MockTestCreateAudit v2.14 (B3), so every §13-7A site stating the
#   expected fixture-based count moves 73/73 -> 107/107. AUTH_GATE_FLOOR stays at
#   35 — the floor gates DEPLOYED copies, and raising it would HARD STOP every
#   un-refreshed exam.
# v1.42.2 — 2026-08-01 — SELF-TEST COUNT REFRESH ONLY (documentation; zero rule
#   change). The canonical auditor B3 ships (audit_canonical.py) gained eleven
#   fixtures at Framework_MockTestCreateAudit v2.13
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT), so every §13-7A site that states the
#   expected fixture-based count moves 61/61 -> 107/107. AUTH_GATE_FLOOR is
#   UNCHANGED at 35 and is deliberately NOT raised: the floor gates the deployed
#   copies, and raising it above their printed count would HARD STOP every
#   un-refreshed exam. A v2.11 copy (51/51), a v2.12 copy (61/61) and a v2.13
#   copy (107/107) all pass the floor, so the estate migrates exam by exam with
#   zero downtime. B3 cardinality (6) and every generation rule are untouched.
# v1.42.1 — 2026-08-01 — B3 STAYS AT 6 OUTPUTS; NO ENGINE PROVISIONING
#   (post-deploy correction). v1.42 raised B3 to 8 by shipping blueprint_core.py +
#   figural_core.py per exam. Wrong remedy: CLAUDE.md states engines live ONLY in
#   the central repo and no per-project provisioning should ever be performed,
#   because a project copy is a second unverified source that can go stale. Step 8
#   P0 now copies both engines from the Step-0 verified clone ($FW) instead — the
#   same pattern §S1-2b already uses for blueprint_core — so the B3 contract
#   returns to 6 and no exam project needs touching. Superseded v1.42 entry:
# v1.42 — 2026-08-01 — B3 SHIPS THE RUNTIME ENGINES (8 outputs, was 6)
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D2/D3). The canonical auditor delegates
#   A-FIGPROFILE to blueprint_core and the 12 A-FIG* gates to figural_core, but
#   NEITHER engine was ever copied into an exam project — not in the B3 output set,
#   not in project knowledge, not named as a Step-8 input anywhere. B3 now copies
#   both VERBATIM under their BARE names (a [ExamCode]_ prefix breaks the module
#   import and silently disables the gates). Also corrected here: the B3 checklist
#   still asserted "--self-test passed (13/13 PASS)", a stale reference to the
#   RETIRED hollow MVP; it now asserts a FIXTURE-BASED N/N with N >= 35.
# v1.41.2 — 2026-07-31 — §13-7A COPY SOURCE now audit_canonical.py (repo engine); the
#   canonical auditor no longer requires opening Framework_MockTestCreateAudit.md
#   mid-session. Behaviour identical (byte-identical script).
# v1.41.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   825 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_Blueprint'. The current companion block, the
#   v1.41 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.41 — 2026-07-26 — S2-2 LOADS THROUGH load_taxonomy(). Read and gate collapse to
#         one call, and the taxonomy comes from approval_record.json where the record
#         carries it rather than from a Word document. Step 6 is the worst place for a
#         wrong taxonomy — the blueprint built from one is internally consistent,
#         passes every BV check and is indistinguishable from a correct one at Steps
#         7-11 — so removing the parse step here removes the largest remaining way to
#         get one. Pre-1.3 records fall back to the doc, gated, and need no re-run.
#         MINIMUM COMPANION: corpus_io.py >= v1.4.
#
```

## Framework_DeliveryFooter.md

Full v1.27 entry (header carries the short form since v1.28 — SPEC-BUDGET on the PYQPrepare route):

```
# v1.27 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestCreate
#   v5.73, MockTestExplain v1.46.0, MockDeliver v1.16.0, paper_pipeline v5.74 Cluster RH,
#   explain_engine v2.9, final_assembly v5.60). NEW §8 REGISTRY-HANDOFF-LAW: a step that
#   CHANGES registry.json DELIVERS it (Replace); badge lines are
#   pp.handoff_footer_lines(HANDOFF) verbatim. §3: Step 7 no longer delivers the audit
#   dossier (internal); Step 9 final delivers registry.json (Replace) +
#   [ExamCode]_[slug]_Explain_Report.docx (the old "registry not delivered" note was wrong
#   since MockTestExplain v1.42.0); NEW blocks STEP 7-R and STEP 9-R; Step 11 delivers a
#   healed registry. §6 gains the repair path. LOCAL_ONLY gains '*_Explain_Report.docx' and
#   '*_Create_Repaired.docx'.
```

Entries v1.24–v1.26 moved at framework release 2026.08.26.3 (EC-P42; v1.27 supersedes;
the PYQPrepare route's pre-work read crossed the SPEC-BUDGET threshold).

```
# v1.26 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS (paper_pipeline v5.72,
#   MockDeliver v1.15.0, MockTestExplain v1.45.0). Prose only. §FOOTER-DG DISCLOSED
#   example shows the windowed shape ("(not gated)" / "in window").
# v1.25 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with
#   paper_pipeline v5.71 Cluster DG, MockDeliver v1.14.0, MockTestExplain v1.44.0).
#   MINOR bump: registry/prose only, NO badge changes, NO artefact changes.
#   * §3 STEP 11 gains §FOOTER-DG, which MockDeliver v1.13.0 referenced but no spec
#     defined: the difficulty-gate disclosure lines are pp.dg_footer_lines(rec) —
#     the measured-band line on DISCLOSED, the not-applicable line on DORMANT, and
#     one healed-registry line per rec['migrations'] entry — so a corrected record
#     is always disclosed in the delivered footer and never composed by hand.
#   Superseded v1.23 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
# v1.24 — 2026-08-24 — GAP-2026-08-24-STEP9-AUDIT-R2: SCOPED-PAPER NEXT-STEP + 6S REGISTRY.
#   MINOR bump: registry/prose only, NO logic changes, NO badge changes, NO artefact
#   changes. Release 2 of the Step-9 audit (R1 = 2026.08.24.1).
#   * §3 STEP 7 / 9 / 11, §4-1 Step-11 variant and §6 named ONLY the mock triggers
#     (MockCreate M / MockExplain M / MockDeliver M) and "Mock [N]". A scoped paper
#     (ScopedBlueprint → TestCreate P[N] → TestExplain P[N] → TestDeliver P[N]) got a
#     footer pointing at a trigger whose --level mock alias would HARD STOP on its
#     scoped docx (MockTestExplain S2-1 / MockDeliver S1-2 slug gates). Every next-step
#     line now names both forms; "Mock [N]" → "[paper_slug]".
#   * §3 had NO entry for Step 6S (ScopedBlueprint), which rides this file on its route
#     and had no deliverable/badge/next-step registry to follow. Added.
#   Superseded v1.22 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
```

Entry v1.23 moved at framework release 2026.08.25.3 (EC-P42; v1.25 supersedes).

```
# v1.23 — 2026-08-23 — REGISTRY SYNC (Step 6 learnings filename; Step 5 tiers).
#   MINOR bump: registry/prose only, NO logic changes, NO artefact changes beyond
#   the filename the Step 6 footer badge table prints.
#   * §3 STEP 6 B3 still listed [ExamCode]_ExplainLearnings.md; Blueprint v1.50.0
#     generates [ExamCode]_EXPLAIN_LEARNINGS_v1.md, because the legacy name
#     matched NO consumer's glob (Steps 7 and 9 load *_EXPLAIN_LEARNINGS_v*.md).
#     The registry now names the file Step 6 actually emits — a footer that
#     badges a filename no step produces sends the operator hunting for it.
#   * §3 STEP 5 FINAL heading said "6 mandatory + taxonomy.xlsx when written",
#     counting exam_config.json as mandatory while its own list line says
#     "delivered only when generated". Restated as the two-tier set that
#     MockTestAnalyse S11-3 and mock_sync_audit MS-11 enforce: 5 mandatory +
#     2 conditional. Fourth recurrence of the delivery-count-drift class; this
#     was the last site still carrying a fixed count.
```

Entry v1.22 moved at framework release 2026.08.24.2 (EC-P42; v1.24 supersedes).

```
# v1.22 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: adds a CLASS: T stub for present_files(). NO ARTEFACT CHANGES.
#   present_files() was CALLED from compiling python here while DEFINED nowhere — a
#   guaranteed NameError; spec_name_audit_baseline.json had accepted it as
#   known-unbound in all four affected specs, so the ratchet reported OK.
#   FULL NARRATIVE: SPEC_HISTORY.md + CHANGELOG.md 2026.08.16.2.
```

Moved from the file header at framework release 2026.08.15.14; entry v1.21
at framework release 2026.08.20.9 — this file rides on ALL 23 routes, so
every byte in its header is paid by every session of every step.
Current-version entry remains in Framework_DeliveryFooter.md.

```
# v1.21 — 2026-08-13 — SYNC AUDIT ROUND 2: footer registry caught up with the steps.
#   (1) GAP-2026-08-13-DELIVERY-COUNT-DRIFT (mirrored): §3's Step-5 final list said "5
#   files" — no badge for exam_config.json (mandatory-when-generated since MockTestAnalyse
#   v2.24.9) and none for taxonomy.xlsx (v2.24), which therefore fell through to an Upload
#   badge for an xlsx this spec itself marks unreadable. List now matches S11-3's derived
#   set. (2) GAP-2026-08-13-FOOTER-SCOPED-PATTERNS: §2 LOCAL_ONLY only knew Mock*_ name
#   forms; scoped papers ({EXAM}_SUBJ_*/TOPIC_*/SUBTOPIC_* slugs) fell through to
#   Upload/Replace. Added slug-agnostic suffix patterns (*_Create.docx, *_Explanation.docx,
#   *_Final.docx, *_Q1to*.docx, *_audit_dossier.json, *_taxonomy.xlsx).
# MockTestFramework | Cross-step | Exam-agnostic
#
# PURPOSE:
#   Define the visual delivery footer that Claude renders after every
#   present_files call in the 11-step pipeline. Two footer types exist:
#   mid-step (amber) and step-complete (green). This file is the single
#   source of truth — all spec files reference it instead of embedding
#   their own footer logic.
#
# SCOPE:
#   Steps 1–11 (all pipeline steps, all exams, all projects).
#   This file is uploaded to the MockTestFramework project AND to each
#   [ExamCode] project so it is available in project knowledge everywhere.
#
# REFERENCED BY:
#   Every Framework_*.md file's delivery section references this spec:
#   "Follow Framework_DeliveryFooter.md for post-delivery footer rendering."
#
# VERSION HISTORY:
#
# v1.20 — 2026-08-12 — NOTES HANDOFF BY ATTACHMENT (GAP-2026-08-12-NADOCX P2;
#   pairs with Framework_NotesAudit v3.0.0 / NotesCreate v2.3.0 / NotesDeliver
#   v1.2.0). The section 3 NC/NA/ND entries change: the notes .docx now moves
#   between steps as a CHAT ATTACHMENT, not through Project Files, so its badge
#   is "Use locally" at every step and the Next callout says to attach it. Only
#   notes_registry.json is still filed — every step reads it from there, and it
#   now carries draft_ref, final_ref and audit_summary (notes-registry/2.1).
#   [ExamCode]_<unit>_Audit.md is REMOVED from ND's and NA's deliverable lists:
#   NA no longer writes one. Filenames are the three engine authorities
#   (notes_filename / notes_final_filename / notes_deliver_filename). The
#   4-cell NOTES bar and every rendering rule are UNCHANGED — ND survives, so
#   the pipeline is still 4 steps.
# v1.19 — 2026-08-10 — NOTES CROSS-CHAT HANDOFF (supersedes v1.18's "NC/NA
#   present nothing"). v1.18 marked NC and NA intermediate, which only holds if
#   all four Notes steps run in ONE session — but the framework idiom is a new
#   chat per step, so NC's draft .docx and NA's audited .docx must persist across
#   chats exactly like NB's bank. NC and NA now PRESENT their handoff artifacts
#   (draft / audited .docx + audit report + the updated registry) and render a
#   footer, so their §6 next-step line actually prints. §3 NC/NA entries rewritten
#   (F2, deliverables, Upload to Project Files); the §4-4 NOTES bar now applies to
#   all four Notes F2 footers (NB=1, NC=2, NA=3, ND=4). Also: notes_pyq_bank.json
#   is NAMED in the get_badge context-dependent note (its mid-batch checkpoint is
#   Upload/Replace for a fresh-chat resume, Use locally for an in-session
#   continue), resolving the §3-vs-get_badge disagreement. Additive to Step 1-11.
# v1.18 — 2026-08-10 — NOTES PIPELINE INTEGRATED. The Notes pipeline
#   (NB/NC/NA/ND) routes this footer but had ZERO §3 registry entries and no
#   pipeline bar, so once NB began calling present_files (NB v2.0.4) it owed a
#   footer it could not render. Added: §3 entries for NB/NC/NA/ND (NB and ND
#   deliver + render a footer; NC/NA are intermediate and present no files, so
#   render none — the contract binds only a present_files call); a 4-cell NOTES
#   PIPELINE BAR in §4-4 for Notes F2 footers (the 11-cell Mock/PYQ bar never
#   applies to Notes); and the Notes chain in §6. Additive only — no Step 1-11
#   entry, badge, severity, F1/F2 shape, or §5 flowchart changed.
# v1.17 — 2026-08-10 — LOCAL_ONLY PATTERN MADE AIRTIGHT. v1.16 added
#   '*_pyq_registry.json', but get_badge() matches via endswith(pat) / fnmatch(*pat),
#   so a BARE 'pyq_registry.json' with no '[ExamCode]_' prefix did NOT match and fell
#   through to the upload/replace branch — the v1.16 "never routed to Project Files"
#   guarantee was narrower than stated (the spec always names the file with a prefix,
#   so it was not reachable in practice, but the guarantee should be exact). FIX: the
#   pattern is now '*pyq_registry.json' (underscore dropped), which matches BOTH the
#   prefixed and bare forms while still excluding the mock '_registry.json',
#   'blueprint.json', and unrelated files (verified: zero false positives). Surfaced in
#   the 2026.08.10.1 deployment review. Badge-only; no severity/F1/F2/flowchart change.
# v1.16 — 2026-08-10 — PYQ REGISTRY IS LOCAL-ONLY (structural badge guarantee).
#   Added '*_pyq_registry.json' to the §2 LOCAL_ONLY set so get_badge() can NEVER
#   route the PYQ corpus tracker to Project Files on any step, for any exam — it
#   always badges 📁 Use locally. Pairs with Framework_PYQDeliver v1.10, which demotes
#   the registry from a required Project-Files deliverable to an OPTIONAL, absence-
#   tolerant, local-only continuity aid (closing the silent cross-session reset that
#   the routinely-skipped manual upload caused across the ~200-exam corpus). BADGE
#   ONLY — no severity routing, no F1/F2 change, no §5 flowchart change; no condition
#   may halt a run, and that is untouched.
# v1.15 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. Updated the PYQ VOID_ITEM /
#   CERTIFIED-DEGRADED (VISION) wording that named PYQ-2 as the reader of the voided-
#   question list (now the human reviewer), and the v1.13 note that called PYQExplainAudit
#   a still-live step (it is now also retired). F1/F2 shape, Q0/Q0b, severity unchanged.
# v1.14 — 2026-08-03 — NEW §2A SPEC PROVENANCE DISCLOSURE (project-first specs).
#   Specs are now PROJECT-FIRST: a Framework_*.md in an exam project's Files section
#   overrides the repo copy and CANNOT be byte-verified. Every footer must now state
#   whether the run used repo-verified specs or project overrides, naming them.
#   DISCLOSURE ONLY — no severity routing, no AMBER/VOID_ITEM/BLOCKING change, no F1/F2
#   change, no §5 flowchart change. No condition may halt a run, and that is untouched.
#
# v1.13 — 2026-08-03 — DEFECT FIX: this file still routed operators to the RETIRED steps.
#   2026.08.03.5 retired canonical Steps 8 and 10 but left §2's step registry intact, so
#   every Step 7 footer printed "NEXT STEP: Step 8: MockCreateAudit M[N]" and every Step 9
#   footer printed "NEXT STEP: Step 10: MockExplainAudit M[N]" — triggers that no longer
#   resolve. This file is routed to ALL triggers, so the defect printed on every delivery.
#   FIXED: the STEP 8 and STEP 10 template blocks are removed, Step 7 -> Step 9 -> Step 11
#   is the printed chain, and the §7 chain map matches. The pipeline bar STAYS at 11 cells.
#   The three retired filenames stay in LOCAL_ONLY so pre-retirement files on disk badge
#   correctly. ZERO CHANGE to §5 Q0b, to the v1.12 PYQ-1 VOID_ITEM producer clause, to any
#   severity routing, or to F1/F2 shape: no colour or vision condition may halt a run.
#
# v1.12 — 2026-08-03 — §5 Q0b GAINS A SECOND PRODUCER: PYQExplain §13A VOID_ITEM.
#   Q0b already fires on a MEASURED vision outage in the mock pipeline. PYQ-1 can
#   now measure the same condition (Framework_PYQExplain v1.2 §13A-5) and had no
#   amber path, so it HALTED instead — the one place the corpus rule 'a CLASS T
#   failure must be LOUD and must NOT halt' (CLAUDE.md) was not applied. Same
#   measured condition, same AMBER, one more producer. The PYQ wording NAMES the
#   voided questions, because an unexplained question that is not named reads as
#   an oversight and the human reviewer must be told where to look (PYQExplain RE-20).
#   Zero change to F1/F2 shape, to Q0, to Q1, or to any severity routing:
#   no colour or vision condition may halt a run, and that stays untouched.
#
# v1.11 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   B3 final deliverables drop 6 -> 5 (ExplainAuditLearnings.md is no longer generated);
#   the engine-copy duty moves from Step 8 to Step 7. The former audit-rule cross-reference
#   is inlined because the spec that defined it no longer exists. No footer rule, severity, or
#   AMBER/VOID_ITEM/BLOCKING routing changes: no colour condition may halt a run, and
#   that is untouched here.
#
# v1.10 — 2026-08-01 — §5 Q0b: CERTIFIED-DEGRADED (VISION) forces F1 AMBER.
#   A paper certified under a MEASURED vision outage (the retired audit-side rule on
#   vision outage, now carried by Step 7's own handling) delivers, but must
#   never render green: some figures were machine-checked and never eyeballed. — Universal Delivery Footer Contract
# v1.9.1 — 2026-08-01 — B3 STAYS AT 6 FILES; ENGINES COME FROM THE CLONE
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING, post-deploy correction). v1.9 briefly
#   raised B3 to 8 by shipping blueprint_core.py + figural_core.py per exam. That was
#   the wrong remedy: CLAUDE.md states engines live ONLY in the central repo and no
#   per-project provisioning should ever be performed, because a project copy is a
#   second unverified source that can go stale. Step 8 P0 now copies both engines
#   from the Step-0 verified clone ($FW) instead — the same pattern Blueprint §S1-2b
#   already uses — so the delivery contract returns to 6 and no exam project needs
#   touching. Superseded v1.9 entry:
# v1.9 — 2026-08-01 — STEP 6 B3 DELIVERABLE LIST 6 -> 8 FILES
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D2/D3). B3 now also delivers
#   blueprint_core.py and figural_core.py under their BARE names. Step 8's auditor
#   delegates A-FIGPROFILE to the former and the 12 A-FIG* gates to the latter, but
#   until v1.9 neither engine ever reached an exam project. Bare names are
#   mandatory: they are imported as Python modules and an [ExamCode]_ prefix breaks
#   the import, silently reducing audit coverage. Absence is never fatal — the
#   dependent gates report an explicit WARN skip and the audit still completes.
# v1.8.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   79 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_DeliveryFooter'. The current companion block, the
#   v1.8 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.8 — 2026-07-26 — §5 QUALITY GATE: A FAILING CHECK FORCES AMBER
#          (GAP-2026-07-26-003). A step could report a FAIL and still render the
#          GREEN "Step Complete" footer, because §5 asked only whether the WORK was
#          finished, never whether the RESULT was sound. That is what shipped the
#          reference run: Step 5 finished all 22 papers with 153/153 figural
#          questions unobserved and 45/45 FIGURAL subtopics carrying an empty
#          object-type profile — and rendered F2 green.
#          New Q0 runs BEFORE Q1: any FAIL from the step's own checks (Step 5
#          QV-1..QV-14, Step 8 audit gates, Step 1 unobserved-image count) renders
#          F1 AMBER with the failing check and its remedy named.
#          WARN does NOT force amber — if it did, every run would turn amber and
#          the signal would be lost again.
#          THIS IS NOT A HALT: the step completes, every file is delivered, and the
#          operator may proceed. Amber REPORTS; it does not block.
```

## Framework_MockDeliver.md

Entry v1.12.1 moved at framework release 2026.08.25.3 (EC-P42; v1.14.0 supersedes).

```
# v1.12.1 — 2026-08-13 — SYNC AUDIT ROUND 2: gate-count prose fix. §2 item 4 said "All 16
#   audit gates" while §6 is headed "all 17 must PASS" and runs C1–C17 (C17 = NAT charset).
#   Prose corrected to 17; no gate logic changed.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockDeliver.md.

```
# v1.12.0 — 2026-08-10 — LEDGER INTEGRITY CHECK + REMEDIATION CLASSIFIER
#   (GAP-2026-08-10-QINDEX-FK-ENFORCEMENT). Two changes, both to the FAILURE
#   side of S1-2/S1-3 — the clean-path JOIN, the tagging pipeline, and every
#   C-gate are byte-untouched.
#   (1) S1-2 step 3 now ALSO runs a whole-registry ledger↔index agreement check:
#       a paper listed in mocks_completed/papers_completed with NO question_index
#       entry is a Class-A finding named as REGISTRY DATA LOSS (the entry was
#       dropped by a later write), with remedy "re-run Step 7" — replacing the
#       misleading suggestion that Step 7 was never run.
#   (2) S1-3 build_tag_lookup now COLLECTS every unresolved question, CLASSIFIES
#       each stale subtopic_id, and hard-stops with a per-question remediation
#       report instead of failing on the first and printing "ensure both files
#       are from the same run" (proven misleading: on the reference corpus both
#       files WERE from the same run — the ids were invented at Step-7 write
#       time). Classes: W1 = stale leaf exists on exactly ONE current subtopic
#       (deterministic registry patch, printed ready-to-apply); W2 = leaf
#       reworded, no verbatim match (candidate targets printed; HUMAN must
#       confirm — never auto-applied); D = leaf matches MULTIPLE subtopics
#       (all candidates printed; human decision). Companion to MockTestCreate
#       v5.48.0 (S13-4 copy-by-reference + engine gate A-QINDEX) and
#       MockTestExplain v1.23 (P10 tripwire), which together make reaching this
#       classifier require multiple independent upstream failures.
# v1.11.0 — 2026-08-09 — DELIVERED FILE NOW PRESERVES NATIVE OMML — the OMML→Unicode
#   linearization (Rule 19) is RETIRED from the delivery path. ROOT CAUSE of the
#   reported math-mutation defect: the "WHY THE RENDER-SOURCE DOCX IS SEPARATE"
#   section + Phase 4/5 named the RENDER-SOURCE docx (every `<m:oMath>` flattened
#   to a one-line Unicode text run by Rule 19) as the final delivered `_Final.docx`.
#   That silently DESTROYED all structured math — fractions, radicals,
#   integrals/sums, matrices, sub/superscripts — in every delivered mock paper.
#   The two-artifact design was justified by python-docx round-trip corruption, but
#   Step 11 edits raw `word/document.xml` (unzip→XML→zip) and NEVER round-trips
#   through python-docx, so OMML already survives byte-perfect: the INTEGRITY
#   artifact proves it (gate C5: integrity OMML count == source). FIX: Phase 4's
#   transforms are retired and Phase 5 now delivers the INTEGRITY artifact (native
#   OMML, tag blocks inserted, headers stripped, NO render transforms) as
#   `_Final.docx`. The delivered file is byte-identical to the Step-9 Solutions
#   input except for the pipeline-mandated tag-block insertion (and the safety-net
#   header strip, which is normally a no-op). CONSEQUENCE: Rule 21 (non-ASCII
#   safe-font) and Rule 22 (underline recolor) no longer apply to the delivered
#   file — content fidelity supersedes those portal-cosmetic transforms. Math
#   preservation is now gated: C5 (unchanged) plus C11 INVERTED from "zero OMML in
#   render-source" to "delivered OMML count == source; zero linearization." Mirrors
#   PYQDeliver v1.9, which fixes the identical defect the same way. Touched:
#   ZERO-MUTATION RULE, the render-source rationale section, DEFINITION OF DONE
#   (items 5/6/8), preflight step 7, Phase 4 (retired), Phase 5 (delivers
#   integrity), §6 gates C11/C14/C15, the delivery report, the assembly checklist,
#   the hard invariants, and Rule 19/21/22 headers (marked RETIRED).
# v1.10.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   No logic change: preflight already accepted the Step-9 [ExamCode]_[paper_slug]_
#   Explanation.docx, and that is now the only input that exists. The _Complete filename
#   is retained in the accept-regex purely so papers produced before this release still
#   deliver. What DID change is every certification claim: tag values are Step-7-written,
#   not Step-8-certified, and the pre-Q.1 SAFETY-NET is now a genuine net rather than a
#   formality, because no A-HEADER gate runs upstream of it. Stated plainly and not
#   hidden: the JOIN is still fully deterministic, but its inputs carry one fewer
#   independent check than they did.
#
# v1.9.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   187 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockDeliver'. The current companion block, the
#   v1.9 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.9 — 2026-07-20 — TEST* TRIGGERS + MULTI-BLUEPRINT SUPPORT (paper_pipeline.py
#       integration). Adds TestDeliver P[N]
#       as the primary trigger (works for mock AND every scoped tier via --level/--scope),
#       keeping MockDeliver M[N] as a working alias (implicitly level='mock'). WHAT CHANGED:
#         §1 S1-1 — new PRIMARY trigger TestDeliver P[N] [--level ...] [--scope ...];
#           MockDeliver M[N] retained as the mock-only alias.
#         §1 S1-2 — Solutions-docx filename acceptance generalised from Mock[N] to
#           [paper_slug] (pp.paper_slug); blueprint verification now refers to the
#           RESOLVED blueprint (§5 Phase 1), not an assumed single file.
#         §5 Phase 1 — STRUCTURAL FIX: the old collision check HARD-STOPPED if more than
#           one *_blueprint.json existed in project knowledge. That is now the NORMAL
#           state once any scoped tier has been generated alongside the mock series, so
#           this was blocking every scoped delivery. Replaced with: load every
#           *_blueprint.json present, derive EXAM from them, parse paper_slug from the
#           UPLOADED docx filename, then pp.pick_blueprint(blueprints, level=LEVEL,
#           docx_slug=paper_slug) selects the ONE blueprint this delivery is for
#           (PickError → HARD STOP, never a guess). registry.json collision check is
#           UNCHANGED (still exactly one registry per project — the shared cross-tier
#           ledger). paper_slug itself is now ALWAYS pp.paper_slug(paper_id) (zero-padded
#           for a mock), replacing the old inline `f'Mock{N}' if ... else .replace(':','_')`
#           — the render pipeline (§5 Phase 1 onward, e.g. render_out_path) already
#           consumed the `paper_slug` variable from prior C3 work, so this fix propagates
#           through unchanged.
#       Shared logic (paper_slug, pick_blueprint) lives ONLY in paper_pipeline.py. Does
#       not touch the C1–C17 gate logic, the NAT portal-grading charset validation, or any
#       render/tagging logic.
#
```

## Framework_MockTestAnalyse.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockTestAnalyse.md.

```
# v2.50.0 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (EXECUTION-
#   BOUNDARY LAW, Step 5). MINOR bump, not a patch: a function signature changes, a
#   section is added, a persisted schema key is added and two DoD items are added.
#   v2.49.1 was a patch release for a comment-only touch and its changelog called this
#   spec "the reference implementation"; nobody then re-read it against the new
#   contract, and its Drive lane was dead the whole time while four auditors reported
#   0 findings. FOUR defects, all measured on IIT_JAM_MATHEMATICS (22 papers):
#     D1 collect_drive_docx_recursive read results.get('items', []). The connector
#        returns {'files': [...]}. Engine: 22 papers; that line: []. And an empty
#        corpus was NOT loud here — the no-PYQ branch rewrote mode to '--synthesise
#        ALL', so a broken listing became "this exam has no past papers" and Step 5
#        shipped a complete, green, F2-footered deliverable of zero-PYQ scaffolds that
#        Steps 6 and 7 then built an entire paper from. Step 4 could only stall; THIS
#        STEP COULD PRODUCE A WRONG ANSWER. Now EC-P39: HARD STOP, never a fall-through.
#     D2 that walker called gdrive_search() — a CLASS T marker — from python and
#        consumed the result. Both call sites deleted; the walk is corpus_io's.
#     D3 run_batch_loop's drive_payloads had NO PRODUCER anywhere in the spec and
#        defaulted to {}, so every paper raised TransportFallback and the whole corpus
#        routed to manual upload. It now fails loudly, mirroring v2.39's vision_pending.
#     D4 no channel probe, no transport plan, no context budget, no persistence — in
#        the one step that is inherently multi-session. New §S8-0 TRANSPORT PREFLIGHT.
#   Step-5-specific deviations from PYQCount S5-0, because Step 4 is single-session and
#   Step 5 is batched: the inline budget is PER SESSION and a fresh chat resets it (so
#   the remainder is carried, never demanded as uploads); the budget is halved because
#   an inline payload is charged twice (inbound + re-emitted); the partition runs AFTER
#   sort_papers_recency_first (measured: listing order admits 2017/2021/2014 instead of
#   2026/2025/2024 and can leave §1-6 unreachable); and PYQCompress is excluded from the
#   remedy text — these papers are 213x UNDER the cap, the constraint is the channel.
#   ROOT CAUSE OF THE CI BLINDNESS: this file's CLASS T stubs sat in an untagged fence
#   spanning 321-603 that fails ast.parse at line 328 on an em-dash IN PROSE.
#   any_python_blocks() yields only compiling fences, so C6 built an empty stub set,
#   returned early, and never reached the two live violations in the fence next door
#   that compiles fine. The fence is now split; C6-PRE fails the build if any governed
#   spec ever hides a CLASS marker in a non-compiling fence again, and C9 fails the
#   build for a correctly-injected resolver whose container has no producer.
# v2.49.1 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (invariant
#   correction only; zero rule/functionality change). The CLASS T transport block
#   asserted that a Drive result "for any file of consequence is spilled to a JSON file
#   on disk rather than returned inline". MEASURED FALSE 2026-08-15: one 40,488-byte
#   sorted paper spilled to a file in one deployment and returned inline in another,
#   and the two spill directories differed. Delivery form is a property of the
#   DEPLOYMENT, not of the file size; both shapes are accepted and the channel is now
#   PROBED in Framework_PYQCount S5-0 (PYQCore EC-P35/EC-P36). This spec's resolver
#   bridge was already correct and is unchanged — it is the reference implementation
#   the PYQ counting path was missing for 20 days.
# v2.49.0 — 2026-08-15 — GAP-2026-08-15-BAREQ (F-1 mirror + F-2 primary).
#   E-2 Q_PATTERNS mirrors the engine's widened four-entry table: entries 3/4 are the
#   BARE-LABEL forms, for a stem paragraph whose whole payload is <m:oMath>, a drawing,
#   or nothing (PYQPrepare S1-4). p.text is <w:t>-only, so such a stem read as "Q.N",
#   entries 1/2 require whitespace AFTER the digits, and the question did not exist for
#   this step. Updated ATOMICALLY with blueprint_core, PYQSort S3-1 and PYQScan S3-2 —
#   engine-only patching turns audit_deep TABLE-PARITY red by design.
#   S3-2 extract_presorted (F-2, INDEPENDENT and broader): stem_parts[0] was built from
#   para.text and never passed through enrich_paragraph_with_omml(), which every
#   CONTINUATION line already used. So a stem paragraph's equation was silently dropped
#   from full_stem / 'stem' / 'stem_raw' / detect_is_msq / detect_blank_position / the
#   negative test / taxonomy keys / PYQ_STEM_PATTERNS and every mock derived from the
#   item. Measured on IIT_JAM_MATHEMATICS 12-Feb-2017: 46 of 60 stems (77%) lost part or
#   all of their maths, and an OMML-only stem extracted as ''. omml_present/omml_ok were
#   likewise seeded from the body loop alone, so QV-8 (OMML recovery) SKIPPED exactly
#   those questions (om == [] -> PASS). Both flags are now seeded from the stem.
# v2.48.2 — 2026-08-14 — S11-2 PART B FIXED FOR REAL + ONE ORDER EVERYWHERE
#   (GAP-2026-08-14-S11-2-PARTB-UNFIXED, primary; GAP-2026-08-14-DELIVERY-ORDER-
#   DRIFT, secondary; release-manager hold on 2026.08.13.6.) v2.48.1 claimed
#   "S11-2's download step now agrees" but S11-2 has TWO delivery sites and the
#   fix landed on PART C (future re-run note) while PART B — the operative
#   present_files list — still said "All 6", exam_config unconditional,
#   taxonomy.xlsx absent. Combined with v2.48.1's own NEVER-TRIM rule that
#   stale list turned into a hard stop on every normal run (taxonomy.xlsx
#   exists → Check 1 fires → STOP). PART B is now the same two-tier contract
#   as S11-3/checklist/QV[19], in the order the delivery code emits (rules →
#   manifest → xlsx → exam_config → taxonomy → progress → summary), and the
#   bare "All 6" count line is deleted — a bare count is what regenerated this
#   defect each time the set changed. S11-3's numbering is reconciled to that
#   same emission order (v2.48.1 had introduced a third order). The NEVER-TRIM
#   rule stays exactly as written — it is what made this visible. PERMANENT
#   GUARD: mock_sync_audit MS-11 now parses the delivery code's unconditional/
#   conditional sets and asserts all five prose sites (PART B, PART C, S11-3,
#   checklist expected, QV[19]) declare the same two sets — self-tested with
#   the v2.48.1 PART B text as the must-flag fixture. Emitted stamps stay
#   v2.48 (major.minor unchanged). Prose fences only; no python fence touched.
# v2.48.1 — 2026-08-14 — DELIVERY TIERS TOLD STRAIGHT + NEVER TRIM SILENTLY
#   (GAP-2026-08-13-DELIVERY-COUNT-DRIFT, residual layer; field report from a
#   live exam project). v2.47.1 moved exam_config.json to the checklist's
#   WHEN-IT-EXISTS tier, but three prose sites still said "the 6 mandatory
#   files" with exam_config listed among them — the same count-drift class one
#   layer down. S11-3's FINAL DELIVERY list now prints the SAME two tiers the
#   checklist enforces (5 mandatory; exam_config.json + taxonomy.xlsx when
#   they exist, which is every normal run); S11-2's download step and QV item
#   [19] now agree. NEW RULE in the pre-delivery checklist: a failed check is
#   a FINDING, never a trim — the run STOPS and reports the differing
#   filenames in chat; observed in the field: a generated taxonomy.xlsx held
#   back to satisfy a stale six-file reading, discovered only when the
#   operator asked. Emitted stamps stay v2.48 (major.minor unchanged).
# v2.48.0 — 2026-08-14 — TAXONOMY ORDER IS TEACHING ORDER
#   (GAP-2026-08-14-TAXONOMY-ORDER; owner decision of 2026-08-14). Two changes,
#   one rule:
#     (1) S5-3 write_taxonomy_xlsx no longer re-sorts rows alphabetically —
#         that resort silently DISCARDED the manifest's curated order, which
#         notes_core.assign_numbering has been freezing into the permanent
#         S/T/ST unit numbers all along (verified against delivered
#         filenames: syllabus order, not alphabet). Rows now emit in MANIFEST
#         ORDER with a new "Upload Order" column (E) and a How-to-use
#         instruction to upload to the portal top-to-bottom. Columns A-D are
#         unchanged in position and meaning, so every downstream "column D"
#         reference (Framework_NotesCreate section 0 among them) still holds.
#         The standalone converter manifest_to_taxonomy_xlsx.py is changed
#         identically in the same release — two writers, one behaviour.
#     (2) S5-3 gains the SUBTOPIC ORDERING RULE above write_subtopic_manifest:
#         first extraction of a NEW exam enters each topic's subtopics in
#         TEACHING order (syllabus order default, SME-adjusted); re-runs
#         APPEND new subtopics at the end of their topic, never mid-list; an
#         exam whose numbering is already persisted is NEVER reordered.
# v2.47.1 — 2026-08-13 — SYNC AUDIT ROUND 2: two more delivery-set fixes.
#   (1) exam_config.json moved from the unconditional to the WHEN-IT-EXISTS tier of
#   S11-3's expected set: the delivery code appends it only if generated and S-SECMAP
#   tolerates its absence with a WARN, so the unconditional listing made Check 1 forbid
#   delivery on runs the spec itself had blessed (the inverse of v2.47's taxonomy fix).
#   (2) write_section_rules' "# Generated by ..." comment stamp still said v2.23 (the
#   parseable framework_version field was fixed at v2.47; the comment was missed).
# v2.47.0 — 2026-08-13 — CROSS-STEP SYNC AUDIT FIXES (Steps 5→11 handshake audit)
#   Three desyncs found by a dedicated 3-pass producer↔consumer audit of the whole
#   Step 5 → TestDeliver chain, all fixed in this file:
#   1. GAP-2026-08-13-STALE-NAME-MATCH-RULE — S1-4's CROSS-STEP SUBTOPIC NAME RULE
#      still claimed "Step 7 matches subtopics by EXACT name" and prescribed re-running
#      Steps 5+6 on any rename. FALSE since MockTestCreate v3.4 (its SUBTOPIC_ID
#      CONTRACT section: joins are by subtopic_id ONLY; the display name is
#      decorative) — and contradicted by this
#      file's own §15 SUBTOPIC_ID CONTRACT. Rewritten to the id-based truth, keeping
#      the one obligation that IS real (a rename that changes the derived id still
#      requires re-running Step 5 AND Step 6 together).
#   2. GAP-2026-08-13-DELIVERY-COUNT-DRIFT — three sites disagreed on the final
#      deliverable count: DoD [19] said "EXACTLY 5" (predating BOTH the v2.24.9
#      exam_config 6th file and the v2.24 taxonomy.xlsx conditional 7th), S11-3's
#      closed list said "all 6", and the delivery code has appended taxonomy.xlsx
#      since v2.24 — so S11-3's own Check 2 ("no unexpected files") would veto the
#      code's own 7-file delivery. All sites now agree: 6 mandatory + taxonomy.xlsx
#      when written (= 7 on a normal run), with the expected set DERIVED from what
#      the code actually writes (the same v5.36 lesson Step 7's S13-7 learned).
#   3. Provenance stamp drift — section_rules framework_version and the manifest
#      generated_by stamps still said v2.22/v2.23. No consumer parses them (verified
#      by grep across Framework_Blueprint/MockTestCreate/blueprint_core/corpus_io —
#      Step 6's v2.22+ gate checks the per-entry `format` FIELD, never the stamp),
#      so severity was cosmetic-only; updated to v2.47 for honest provenance. NOTE:
#      this stamp-drift class has now recurred at least four times (v2.14/v2.15/
#      v2.17 fixed it before) — future version bumps must update these literals.
# v2.46.0 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v2.45.0 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v2.44.0 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: the exemption became the budget.
#   v2.26 replaced `has_img = any(...)` with a rate and then decided REDUCIBILITY
#   with a fresh any(). One question in a 22-year corpus made a subtopic permanently
#   exempt, and irreducible grants pass even over budget by design. First real
#   PYQExtract run: 21 of 133 subtopics exempt, 14.3 figures/mock against a budget
#   of 5, 13 of 15 mocks over. Reducibility is now rate-based (figural_rate >= 0.50
#   AND option_image_rate >= 0.50) -> 3 subtopics, 1.5 forced, 0 mocks over.
#   Figures are now SCHEDULED at measured frequency rather than forced at render
#   time, the audit band is the exam's own volatility, and per-mock targets follow
#   the exam's observed shape. No feasibility halt exists or is needed.
# v2.43.0 — 2026-08-06 — GAP-2026-08-06-DI: DI becomes measurable.
#   DI was the one budgeted Axis-1 stimulus class leaving NO trace anywhere, so
#   A-AXIS1 could only ever report it UNESTABLISHED. It cannot be recovered from the
#   docx: G-MATCH-TABLE mandates a real Word table for every MATCH question, so on a
#   real paper table-presence finds 3 candidates where exactly 1 is DI. Step 7 now
#   records di_manifests (the producer's own record) and asks the Axis-1 budget
#   before building a table stimulus; Step 5 emits di_rate/di_q_count/di_reducible.
#   Absent-safe: no di_manifest -> DI stays unestablished, exactly as before.
# v2.42.0 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v2.41.0 — 2026-08-05 — GAP-2026-08-05-001. S3-2 takes bc.sorted_body_lookahead(doc)
#   and the per-FILE colour probe. QV-1a severity WARN -> FAIL (SG-6): the identical
#   condition was a HARD STOP at Step 4 and a silent green footer here. QV-15 BODY
#   TERMINATION SANITY added (SG-7) with a NAT-specific colour assertion, since an
#   option-count threshold is meaningless for a question that has no options. New counter
#   questions_terminated_by_heading, reported even when 0.
# v2.40.0 — 2026-08-03 — DEFECT FIX: live cross-step contracts still named the retired
#   Step 8. The axis classifier's propagation contract read "MUST PROPAGATE (byte-identical)
#   to Step 8 MockCreateAudit S6-1b" — a binding instruction pointing at a spec deleted in
#   2026.08.03.5. The contract itself is UNCHANGED and still binding; its target is
#   restated as audit_canonical.py, which is where the verbatim classifier copy actually
#   lives and which Step 7 runs. Internal/canonical step map marks slots 3 and 5 RETIRED
#   without renumbering, so unlabelled internal step references keep their meanings.
#
# v2.39.2 — 2026-07-31 — §16 XLSX IMPLEMENTATION EXTRACTED to frequency_xlsx.py (repo
#   engine, hash-tracked). 664 lines of workbook code (aggregation, derived metrics,
#   generation, 5 sheet writers) moved byte-identically; §16 keeps the sheet spec (§16-3),
#   the 9-item validation checklist (§16-9) and the EC-F* edge cases (§16-10), each
#   subsection now naming the engine functions it governs. Call sites use
#   `import frequency_xlsx as fx`. Zero behavioural change.
# v2.39.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   1157 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestAnalyse'. The current companion block, the
#   v2.39 entry, and all structural notes remain in-file. Body byte-untouched.
# v2.39 — 2026-07-27 — GAP-2026-07-27: SIX DEFECTS FOUND BY SIX SESSIONS ON ONE CORPUS.
#     Six independent sessions ran Step 5 on IIT_JAM_BIOTECHNOLOGY (22 papers, 1,719 Qs).
#     FIVE rediscovered the same vision defect and each invented a DIFFERENT workaround;
#     the one session that executed these python fences VERBATIM found a P0 no other
#     session hit. Every earlier session had paraphrased the spec into hand-written
#     modules and, in paraphrasing, silently repaired a bug present here as written.
#     The lesson generalises past these six fixes: THIS SPEC WAS LESS CORRECT THAN ANY
#     IMPLEMENTATION OF IT THAT HAD EVER SHIPPED, and its defects were invisible in
#     exact proportion to how competently it was reimplemented.
#
#     A — TAXONOMY SOURCE-2 CONCATENATED INSTEAD OF MERGING (P0). The Source-2 append
#         was unguarded while Source 1 was guarded, so the stated contract — "merged,
#         Analysis docs win for names" — held in NEITHER half. MEASURED: 260 subtopic
#         blocks for 134 distinct ids; 126 emitted TWICE (the 8 singletons are zero-PYQ
#         scaffolds, which enter through the guarded path). mint_subtopic_ids() could
#         not recover: its `_2` disambiguator fires only when the KEY differs, and these
#         keys were identical, so both copies took one id and QV-13 refused the run.
#         The 126 duplicate blocks were verified BYTE-IDENTICAL — a delivery blocker,
#         not content corruption.
#         FIXED: real merge; renames carried into progress keys by apply_taxonomy_renames()
#         (the lookup key includes topic, so a rename not propagated would silently
#         orphan every question under it); _dedupe_analysis_docs() by realpath + SHA-256,
#         applied at BOTH call sites — the S1-4 one was never reported and inflated the
#         subtopic count shown to the operator; RuntimeError from the v2.31 lock gate no
#         longer swallowed by `except Exception: pass` (the gate was armed and disarmed
#         six lines apart); new QV-13b HARD STOP pre-mint, so the failure is attributed
#         to the MERGE rather than surfacing as an opaque id collision — which is what
#         sent six sessions to inspect the one function behaving correctly.
#
#     B — build_vision_queue() OVERWROTE, AND WAS CALLED PER PAPER (P0). It writes
#         vision_queue.json and vision_sheet_NNN.png, both FIXED names, and never read
#         an existing queue; the sole call site sat inside process_pyq_paper(), writing
#         into a workdir S4-2a defines as one-per-RUN. Only a batch's LAST paper reached
#         Phase B. MEASURED: 153 figural questions across 22 papers, _meta.vision
#         recorded queued=8; batch 7 queued 24 and 3 survived. The stated Phase A
#         invariant was violated in the OPPOSITE direction — sheets existed that no
#         queue referenced.
#         FIXED, both halves: the call is HOISTED to the batch boundary (candidates
#         accumulate in a run-level list; a missing accumulator RAISES rather than
#         silently dropping figures), and corpus_io v1.9 makes the write IDEMPOTENT by
#         unioning with the on-disk queue. Hoisting alone still loses prior sessions;
#         idempotence alone still loses papers 1..N-1 within a batch.
#
#     D — XLSX-F9 COMPARED A CORPUS TOTAL TO A PER-PAPER DENOMINATOR (P1).
#         exam_total_all is one paper's size (60); mapped_total is the corpus sum
#         (1,719). The gate fired on EVERY multi-paper corpus ever run, and printed
#         `60 - 1719` as a count of unclassified questions: "-1659 questions were not
#         classified to any subtopic." Not merely wrong — INVERTED. A gate that cannot
#         fire correctly trains operators to ignore gates.
#         FIXED: denominator is papers_processed x total_questions, taken from
#         counting_progress so --frequency-scope current-era counts only its own papers;
#         a negative shortfall is guarded and reported as a SURPLUS, which is legitimately
#         reachable on an era-mixed corpus.
#
#     E — MSQ UNDER-DETECTION ORIGINATES IN STEP 3 (P2). MEASURED: 24 MSQ across 1,719
#         questions against a marking scheme reserving Q31-40 (~10/paper). Not a weak
#         regex — CROSS-STEP INFORMATION DESTRUCTION: PYQSort renumbers into taxonomy
#         order, so the positions identifying the MSQ band are gone before Step 5 reads
#         the paper. Step 5 cannot recover what Step 3 discarded.
#         FIXED at the source: PYQSort v1.18 stamps the original position into the date
#         label (OPTIONAL field — pre-v1.18 files parse unchanged, no re-sort forced);
#         this spec retains the label instead of skipping it and gains a positional
#         branch. The EC-A option-shape guard keeps HIGHEST precedence, so a paper that
#         deviates from its own declared scheme is not mis-typed. Codec lives in
#         corpus_io Cluster Q — one writer, one reader, one definition — because a
#         format defined in two specs is exactly the drift v2.36 had to unwind.
#         Also persists original_q_num + question_type, arming classify_paper_era()'s
#         type-corroboration branch (GAP-X residual: type_checked was False on all 22
#         reference papers, so era rested on question COUNT alone).
#
#     F — NAT SATURATED AXIS-2 FILL_BLANK (P2). Ladder rule 5 fired on the answer-entry
#         blank every NAT question carries. MEASURED: 218 of 261 NAT (83.5%) against 37
#         of 1,434 MCQ (2.6%) — 32x enrichment tracking the ANSWER MECHANISM, not the
#         question form. Control: across 300 legacy-era questions, which carry almost no
#         NAT, FILL_BLANK moved by exactly 1. The axes are orthogonal so nothing was
#         corrupted, but Section C's Axis-2 profile read ~100% cloze and Step 7 rendering
#         that literally emits NAT stems as fill-in-the-blank.
#         FIXED: rule 5 gated on the question having options. Verified against the live
#         corpus: 255 -> 37, all 218 reclassified are NAT, zero MCQ/MSQ touched.
#
#     H — RESUME PRECEDENCE SILENTLY DISCARDED A BATCH (P3 -> P1 on operator evidence).
#         load_progress() returned the FIRST existing path with /mnt/project/ first and
#         the live session's outputs LAST, so a mid-run reload reverted to stale state.
#         The documented workflow — download the output, re-upload to project knowledge —
#         makes stale-project-copy the NORMAL state, not an edge case; one session lost a
#         completed 3-paper batch this way.
#         FIXED: directory order cannot express the rule, because which copy is freshest
#         depends on cold-start vs mid-run and this function cannot know which. It no
#         longer guesses: it reads every candidate and takes the most advanced by
#         papers_processed — correct in BOTH cases, no mode flag — and REPORTS divergence.
#
#     NOT FIXED HERE, TRACKED: GAP-C (Phase B degradation has no cross-session
#     persistence contract — the queue lives in an ephemeral workdir, so six sessions of
#     observation produced a 46%-complete figural record) and GAP-G (no defined delivery
#     behaviour when the closed six-file set is written but DoD reports FAIL).
#
```

## Framework_MockTestCreate.md

Section §S16 (REPAIR MODE, v5.69–v5.75) RETIRED and moved here VERBATIM at framework
release 2026.08.27.3 (REPAIR-RETIRED-2026-08-27, operator decision). Not executable;
retained so the defect narrative it carries (GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING,
GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER, GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS,
GAP-2026-08-26-REGISTRY-HANDOFF-SEAM, GAP-2026-08-26-REPAIR-BATCH-LAW) stays in the repo.

````
# ════════════════════════════════════════════════════════════════════════
# §S16 — REPAIR MODE (TestCreateRepair / MockCreateRepair, v5.69 —
#         GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING)
# ════════════════════════════════════════════════════════════════════════

## S16-1 — Trigger and preflight

  TRIGGER: `TestCreateRepair P[N] Q4 Q8 Q20 …` or `MockCreateRepair M[N] Q…`
  (Q-list separators: spaces or commas; "Q4"/"4" both accepted).
  CONTINUE: the S4-6 continue triggers ("continue" / "go" / "next" …) between repair
  batches (v5.74 — S16-1b). RESUME: `TestCreateRepair P[N] resume` (re-enter a repair
  mid-way: reload [ExamCode]_M[N]_repair_state.json + the working registry, S16-1b).
  ATTACH: the CURRENT question paper docx for paper N (this step's own
  earlier deliverable). The registry and blueprint come from project
  knowledge as always.

  PREFLIGHT (HARD STOP on any failure — malformed-input stops are exempt
  from the no-stop rule, which governs gate VERDICTS only):
    P0  Load the PROJECT copy of the registry and fingerprint it BEFORE any write
        (v5.73 — S16-3's handoff decision compares against this value):

        ```python
        import os, json, shutil
        import paper_pipeline as pp
        REG_PROJECT = f'/mnt/project/{EXAM}_registry.json'        # what Step 9-R will read
        REG_WORK    = f'/home/claude/{EXAM}_registry.json'        # this repair's working copy
        _reg_fp_loaded = pp.registry_fingerprint(json.load(open(REG_PROJECT, encoding='utf-8')))
        if not os.path.exists(REG_WORK):
            shutil.copy(REG_PROJECT, REG_WORK)                    # first turn of the repair only
        reg = json.load(open(REG_WORK, encoding='utf-8'))         # continue/resume: carries the
                                                                  # S16-1b snapshot + batches done
        rec, disclosure = pp.dg_preflight(reg, paper_id, where='S16-1 P0')
        ```
        (v5.71 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER). Runs FIRST.
        A corrupt (status, repair_rounds_used) pair is healed per
        DG-INVARIANT and disclosure is printed VERBATIM in chat (never
        silent); the registry is persisted with the S16-3 commit. A
        DGIllegalState (unknown status) is a HARD STOP — print its message
        verbatim; never proceed on an illegal record.
    P1  BRANCH ON THE STATE PAIR pp.dg_state(rec), never on one field.
        Absent → "This paper has no gate record — run TestExplain P[N] first
        (or this is a legacy paper; deliver as usual)."
        ('FAILED', 0) → PROCEED only if pp.dg_is_windowed(rec) (v5.72 —
        GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS). A FAILED record WITHOUT the
        'windows' stamp was judged under the retired band-equality rule and
        its rework_qs are NOT an order: HARD STOP with "This paper was judged
        under the old difficulty rule — nothing is rewritten on its say-so.
        Next step: " + pp.dg_next_step(...) (the Explain trigger, which re-
        judges the verdict under the windows). pp.dg_add_rework_snapshot
        refuses such a record too, so the stop cannot be bypassed.
        Any other legal pair → "Nothing to repair — next step: " +
        pp.dg_next_step(reg, paper_id, N, mock=<Mock* trigger>) — the SAME
        function Step 9 and Step 11 print from, so this step can never name a
        next step that refuses. (Legal pairs and the state machine:
        MockTestExplain §7A-M "THE RECORD IS SINGLE-WRITER".)
    P2  THE Q-LIST OF RECORD IS THE REGISTRY'S rework_qs — the operator's
        typed list is a CONFIRMATION, not a selection. Empty typed list →
        use rework_qs verbatim. Typed list ≠ subset of rework_qs → HARD
        STOP naming the extras ("Q7 is not in the rework order — the gate
        flagged only Q…"). Typed list a strict subset → HARD STOP: partial
        repairs would leave the band over-limit by construction; repair all
        of rework_qs in one run.
    P3  The attached paper parses (§P3 machinery) and its stems hash-match
        registry stem_texts for paper N (the operator attached the right
        file and the right version). On a continue/resume turn the paper of
        record is the cumulative repaired docx in /home/claude (S16-1b), not a
        new attachment.

## S16-1b — REPAIR BATCH PLAN + PRE-REPAIR SNAPSHOT (v5.74 — GAP-2026-08-26-REPAIR-BATCH-LAW)

  THE LAW, RESTATED FOR REPAIR. S4-4 B-1..B-7 apply to a repair exactly as to a
  fresh paper: a batch is at most MAX_BATCH_SIZE questions (S4-2's ceiling), ONE batch
  per response, auto-advance BANNED, the next batch only on an S4-6 continue trigger,
  present_files only after the batch passes gate checks. B-8's analogue: the FINAL
  repair batch auto-advances to S16-3 in the same response. A rework list of ≤
  MAX_BATCH_SIZE is one batch and the run is a single response, as it was in v5.73.
  The plan is built ONCE (first turn) and read from the file on every later turn —
  never recomputed, never "the last q + 1".

  ```python
  import os, json
  import paper_pipeline as pp
  MAX_BATCH_SIZE = 10                     # S4-2 ceiling — the same number, by reference
  STATE = f'/home/claude/{EXAM}_M{N}_repair_state.json'
  if not os.path.exists(STATE):           # FIRST TURN — plan + snapshot, once
      # old_stems[q] = the raw first paragraph of q in the ATTACHED paper, "Q.<n>" label
      # included — python-docx paragraph.text, the SAME extraction §7A-R R3 applies to the
      # repaired paper, so both sides of pp.dg_stem_hash see identical bytes.
      import re as _re
      from docx import Document as _Doc
      # The attachment is addressed by its EXACT contract name — never a glob — so a
      # stray _Repaired / _PARTIAL / sibling-paper upload can never be picked up.
      ATTACHED_PAPER = f'/mnt/user-data/uploads/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'
      if not os.path.exists(ATTACHED_PAPER):
          raise SystemExit(f"HARD STOP (S16-1b): {os.path.basename(ATTACHED_PAPER)} is not "
                           f"attached. Attach the CURRENT question paper for paper {N} (not a "
                           f"_Repaired / _PARTIAL file) and re-trigger.")
      _QRE = _re.compile(r'^\s*Q\.?\s*(\d+)\b')
      old_stems = {}
      for _para in _Doc(ATTACHED_PAPER).paragraphs:
          _m = _QRE.match(_para.text)
          if _m and int(_m.group(1)) not in old_stems:
              old_stems[int(_m.group(1))] = _para.text
      if sorted(old_stems) != list(range(1, int(bp['total_questions']) + 1)):
          raise SystemExit(f"HARD STOP (S16-1b): the attached paper yields stems for "
                           f"{len(old_stems)} questions, blueprint says "
                           f"{bp['total_questions']} — the baseline snapshot must cover "
                           f"EVERY question or §7A-R R3 cannot prove the repair touched "
                           f"nothing else. Attach the complete paper.")
      rework_qs = sorted(int(q) for q in rec['rework_qs'])
      if not rework_qs:
          raise SystemExit('HARD STOP (S16-1b): the gate record carries an empty rework_qs — '
                           'nothing to repair; run pp.dg_next_step for the next step.')
      batches = [rework_qs[i:i + MAX_BATCH_SIZE] for i in range(0, len(rework_qs), MAX_BATCH_SIZE)]
      # PRE-REPAIR SNAPSHOT — write-once, BEFORE any stem is regenerated (§7A-R R3 evidence).
      # old_stems[q] = the raw first paragraph of q in the attached paper, "Q.<n>" label
      # included, for EVERY q in 1..total_questions (P3 parsed it).
      pp.dg_add_rework_snapshot(reg, paper_id,
                                {q: pp.dg_stem_hash(old_stems[q]) for q in rework_qs},
                                all_stem_hashes={q: pp.dg_stem_hash(t) for q, t in old_stems.items()})
      json.dump(reg, open(f'/home/claude/{EXAM}_registry.json', 'w', encoding='utf-8'),
                indent=2, ensure_ascii=False)               # working copy only — NOT delivered yet
      repair_state = {'exam_code': EXAM, 'mock_n': N, 'paper_id': paper_id,
                      'rework_qs': rework_qs,
                      'batches': [{'batch_id': i + 1, 'qs': b, 'is_final': i == len(batches) - 1}
                                  for i, b in enumerate(batches)],
                      'batches_completed': [], 'current_batch': 1, 'snapshot_taken': True}
      json.dump(repair_state, open(STATE, 'w', encoding='utf-8'), indent=2)
  repair_state = json.load(open(STATE, encoding='utf-8'))
  # CONTINUE / RESUME GUARDS (B-1 analogue): the working registry must carry the
  # snapshot S16-1b took on the first turn — a working copy lost between turns (fresh
  # container, deleted /home/claude) cannot be re-snapshotted from a half-repaired paper.
  _snap = (reg.get('difficulty_gate', {}).get(paper_id, {}) or {}).get('rework_stem_hashes') or {}
  if set(_snap) != {str(q) for q in repair_state['rework_qs']}:
      raise SystemExit(f"HARD STOP (S16-1b): repair_state.json exists but the working "
                       f"registry has no pre-repair snapshot for {repair_state['rework_qs']}. "
                       f"The working copy was lost mid-repair. Delete "
                       f"{EXAM}_M{N}_repair_state.json, restore the PROJECT registry and "
                       f"the ORIGINAL paper, and re-run TestCreateRepair P{N} from batch 1.")
  if repair_state['current_batch'] > len(repair_state['batches']):
      raise SystemExit(f"HARD STOP (S16-1b): every repair batch is already completed — "
                       f"S16-3 has (or should have) delivered. Next step: "
                       + pp.dg_next_step(reg, paper_id, N, mock=False))
  _b = repair_state['batches'][repair_state['current_batch'] - 1]
  BATCH_QS, REPAIR_FINAL = _b['qs'], _b['is_final']
  K_TOTAL, K_NOW = len(repair_state['batches']), repair_state['current_batch']
  print(f"REPAIR BATCH {K_NOW} of {K_TOTAL}: Q{' Q'.join(map(str, BATCH_QS))}"
        f"{' (final)' if REPAIR_FINAL else ''}")
  ```
  Then S16-2 regenerates ONLY BATCH_QS. After the batch passes the self-audit
  (S4-7 STEP B) the response delivers and ENDS per S16-3.

## S16-2 — Regeneration (the only questions touched are rework_qs)

  For each q in BATCH_QS (v5.74 — this batch's slice of rework_qs; every q in
  rework_qs is reached across the batches), run the FULL S7 single-question flow (scenario →
  CHECK 1/1b/2/3/3c → sidecar) with these bindings:
    band     = difficulty_plan-of-record = question_index[q].difficulty
               (the label does not change; the QUESTION moves to it)
    direction= rec['rework_directions'][str(q)] (v5.72): 'harder' — the
               question measured BELOW its label's window (the common case);
               'easier' — it measured ABOVE it (possible for a middle-band
               question under the windowed rule). Missing for a listed q →
               HARD STOP naming q (a windowed FAILED record always carries
               it — pp.dg_write_verdict refuses to write one without).
               The rewrite must land INSIDE the label's acceptance window
               (bc.DIFFICULTY_GATE_BAND_WINDOWS by band position — middle
               2–6, top ≥5) as measured by CHECK 3c's own obs: assert
               bc.difficulty_score_from_obs(obs) lies in the window before
               committing the slot, else redo the slot. CHECK 3c still
               verifies the authored label against the strict authoring
               bands (G-DIFF) exactly as for a fresh slot.
    subtopic = question_index[q].subtopic_id (slot allocation unchanged —
               quota, axis schedules, figural counts all stay intact)
    qtype    = marking_scheme position type (unchanged)
  CHECK 3c runs with the standing rules PLUS, in repair mode:
    (a) STEM-SUPPLIED RELATION RULE (the reason most 'harder' reworks
        exist): the stem may not donate the governing relation of the asked
        quantity —
        no "Given that ∫…", no quoting the formula whose recall/derivation
        the steps count, no handing over a counted intermediate. If the
        subtopic genuinely requires a supplied constant (physical data),
        supply the CONSTANT, never the RELATION.
    (b) the superseded question's semantic tuple joins the dedup set — the
        repair must be a genuinely different question (harder or easier per
        direction), not a reworded twin.
    (c) an 'easier' rework removes load, never content: drop a concept or a
        derivation stage; do not hand over the governing relation in the
        stem (rule (a) still binds) and do not change the subtopic.
  Dedup, key derivation (§S7-NEW-A/C), figure generation (if the slot is
  FIGURAL) all run exactly as in a normal S7 slot.

## S16-3 — Commit and deliverable

  THE CUMULATIVE PAPER (v5.74): /home/claude/[ExamCode]_[paper_slug]_Create_Repaired.docx —
  created on the first turn as a byte copy of the attached paper, then every batch's
  regenerated questions are spliced into it in place. It persists across turns (S4-8
  cross-batch persistence); the final turn copies it to outputs under the same name.
  MID-BATCH (v5.74 — REPAIR_FINAL is False): after the batch's self-audit, splice the
  regenerated questions into the cumulative repaired paper above, apply the
  per-question registry updates below for THIS batch's qs on the WORKING copy, then
  deliver ONLY the cumulative paper, named
  [ExamCode]_[paper_slug]_Create_Repaired_PARTIAL_[k]of[K].docx (F1 amber footer,
  DeliveryFooter §3 "STEP 7-R"). The registry is WITHHELD mid-batch BY DESIGN — this is
  the one deliberate exception to "changed ⇒ delivered", and it is still the law's
  intent: a registry beside a half-repaired paper would let Step 9-R run on that paper
  (its R3 check would pass for the batches done and fail for the rest as "unchanged
  listed"), so the working copy travels only with the COMPLETE paper. The PARTIAL name
  is one Step 9-R's S2-1 REFUSES, so the same half-paper cannot be attached by mistake.
  Then update repair_state.json (batches_completed += k, current_batch += 1 — B-6),
  print "Repair batch [k] of [K] delivered — Q… rewritten. Type 'continue' for batch
  [k+1]." and END the response (B-4). Nothing below runs on a non-final batch.

  FINAL BATCH (REPAIR_FINAL is True) — everything below, in the same response (B-8):
  S13-4 UPDATE SEMANTICS (surgical — the registry is shared state):
    question_index[q]      → replaced entry (new difficulty_obs from the
                             repair derivation; label unchanged)
    stem_texts / question_hashes / semantic_tuples / semantic_usage
                           → replaced at q's position
    key_commitments[q]     → re-sealed for the new answer (fresh salt)
    options_by_q, figural manifests, image phashes
                           → updated for q only
    difficulty_gate record → ALREADY holds the pre-repair snapshot: S16-1b
                             called pp.dg_add_rework_snapshot ONCE on the
                             first turn, BEFORE any stem was regenerated
                             (v5.74; v5.69–v5.73 took it here, which is
                             equivalent only when the repair is one batch).
                             H(q) = pp.dg_stem_hash(<old first-paragraph text
                             of q, raw, "Q.<n>" label included>); the
                             all-question baseline lets §7A-R R3 prove NO
                             question outside rework_qs was touched. The
                             helper is WRITE-ONCE — a re-run returns the
                             original snapshot and never hashes repaired
                             stems — and refuses unless the record is a legal
                             FAILED state. Assert here that
                             reg['difficulty_gate'][paper_id] carries
                             rework_stem_hashes for every q in rework_qs;
                             if not, HARD STOP: "snapshot missing — re-run
                             TestCreateRepair P[N] from a fresh session".

      ⛔ THIS STEP NEVER WRITES `status` AND NEVER WRITES
         `repair_rounds_used` — not by hand, not "defensively", not to mark
         the round complete. Both belong to Step 9 alone
         (Framework_MockTestExplain §7A-M / §7A-R), which writes them
         TOGETHER in one atomic pp.dg_write_verdict call. Setting
         repair_rounds_used here — however natural it looks next to this
         step's own `'round': 1` session_log entry and its "REPAIR COMPLETE"
         print — produced status=FAILED + rounds=1: a pair no step can
         produce on purpose, which DEADLOCKED TestExplainRepair, TestDeliver
         and TestCreateRepair with no exit and cost a completed 60-question
         paper plus its full explanation run
         (GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER). paper_pipeline
         Cluster DG now enforces this mechanically: pp.dg_add_rework_snapshot
         cannot touch either field, and pp.dg_write_verdict refuses the pair.
         audit_canonical A-DGATE (armed by --registry at the S13-4c
         re-sweep) FAILS the audit on any record outside the six legal
         states.

      NOTE — this step's `'round': 1` session_log entry counts THIS step's
      regeneration runs. It is NOT the difficulty-gate repair-round counter
      and the two are never reconciled with each other.
    Every other question's data: byte-identical. The S13 ledger gains a
    'repair' session_log entry (round 1, qs listed).
  DELIVERABLES (v5.73 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM; the CLOSED SET,
  one present_files call, F2 footer):
    1. [ExamCode]_[paper_slug]_Create_Repaired.docx — the full re-assembled
       question paper (every question, repaired ones spliced in place; same
       slug rule as S13-7, "_Repaired" suffix)                → Use locally
    2. [ExamCode]_registry.json — the registry this step just changed
       (replaced stems/hashes/tuples, re-sealed key_commitments, updated
       question_index[q], and the WRITE-ONCE pre-repair snapshot that §7A-R R3
       verifies against)                                     → Replace in Project Files
  WHY 2 IS NOT OPTIONAL. Through v5.72 this line named ONLY the docx. The
  snapshot then lived in /home/claude, the project registry never received it,
  TestExplainRepair R3 raised missing_snapshot → "re-run TestCreateRepair" →
  whose P3 no longer hash-matched the (already repaired) paper: a dead loop on
  every exam that ever reached a FAILED gate. REGISTRY-HANDOFF-LAW: a step that
  CHANGES registry.json DELIVERS it. The decision is mechanical:

  ```python
  import os, json, shutil
  import paper_pipeline as pp
  # _reg_fp_loaded was taken at S16-1 P0 from the PROJECT copy; `reg` is the working
  # copy that carries the S16-1b snapshot and every batch's updates.
  assert REPAIR_FINAL, 'S16-3 delivery runs on the FINAL repair batch only (S16-1b)'
  out = '/mnt/user-data/outputs'
  repaired_name = f'{EXAM}_{pp.paper_slug(paper_id)}_Create_Repaired.docx'
  reg_name = f'{EXAM}_registry.json'
  json.dump(reg, open(f'/home/claude/{reg_name}', 'w'), indent=2, ensure_ascii=False)
  hs = pp.handoff_set('TestCreateRepair', primary_docx=repaired_name, reg_name=reg_name,
                      registry_changed=pp.registry_changed(_reg_fp_loaded, reg), final=True)
  if not hs['registry_delivered']:
      # S16-3 ALWAYS writes the snapshot; an unchanged registry here is a caller bug.
      raise SystemExit('HARD STOP (S16-3): registry unchanged after a repair commit — '
                       'pp.dg_add_rework_snapshot did not run; nothing is delivered.')
  shutil.copy(f'/home/claude/{reg_name}', f'{out}/{reg_name}')
  v = pp.verify_handoff_outputs(os.listdir(out), hs)
  if not v['ok']:
      raise SystemExit(f"HARD STOP (S16-3): outputs != closed set — missing {v['missing']}, "
                       f"stray {v['stray']}. Fix, then re-run. Do NOT call present_files.")
  print('S16-3: closed set verified —', hs['files'])
  for _line in pp.handoff_footer_lines(hs):
      print(_line)
  ```
  Then present_files([f'{out}/{repaired_name}', f'{out}/{reg_name}']) — ONE call, docx
  first. No dossier, no sidecar, no PARTIAL file (remove any *_Create_Repaired_PARTIAL_*
  from outputs before S16-3's verify — pp.verify_handoff_outputs treats it as stray). The self-audit (S4-7 STEP B)
  runs on the repaired docx exactly as on a fresh paper — including A-QINDEX
  checks 7/8/9 — BEFORE this block.
  PRINT (operator-facing, last lines of the run, then the F2 footer per
  Framework_DeliveryFooter.md "STEP 7-R — TestCreateRepair"):
      ════════════════════════════════════════════════════════════
        REPAIR COMPLETE — [k] questions rewritten toward their labels
        ([k_h] harder · [k_e] easier) across [K] batch(es).
        Delivered (2 files):
          • [ExamCode]_[paper_slug]_Create_Repaired.docx  → Use locally
          • [ExamCode]_registry.json                      → Replace in Project Files
        ⚠ REPLACE registry.json in Project Files NOW — TestExplainRepair
          reads the pre-repair snapshot from the project copy and HARD-STOPS
          (missing_snapshot) if you skip this.
        Next step: copy-paste this, attaching the repaired paper
        + the previous explanation Word file:

           TestExplainRepair P[N]
      ════════════════════════════════════════════════════════════
````

Entry v5.59 moved at framework release 2026.08.25.3 (EC-P42; v5.71 supersedes).

```
# v5.59 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paper_pipeline v5.39,
#   final_assembly v5.55, corpus_io v1.12; paired with MockTestExplain v1.37.0 / engine
#   v2.8). A delivered Mock 01 was CREATED with key 2 on a figural question (salicylic
#   acid: carboxyl + phenol) and EXPLAINED with key 1 — Step 9 misread the hand-drawn
#   structure, both its derivations shared the misread, and nothing compared the two
#   steps because the key never leaves Step 7 by design. Two creation-side gaps made
#   that silent: (1) the registry carried no trace of the key Step 7 held, so no
#   downstream step could reconcile against it without seeing plaintext; (2) a
#   chemical structure was drawn by HAND-PLACED bonds (`cd.ring_pts`, `cd.bond`) with
#   NO machine-readable record of what it depicted — figural_manifests.object_types was
#   empty and Step 9's §13-3 manifest cross-check had nothing to compare. FIXES:
#   (a) KEY COMMITMENTS — S13-4 passes the answer_key sidecar to fa.commit_registry
#       (answer_key=…) which writes registry.key_commitments[paper_id] = salted sha256
#       of every canonical answer (mcq '2' · msq '2,3' · NAT grading string). No
#       plaintext enters the registry; Step 9 hashes its OWN derived answers and
#       compares (Explain §7-8). S13-REGCHECK gate G-KEYCOMMIT refuses a commit without
#       them. ZERO new operator deliverables — the registry is already uploaded.
#   (b) SEMANTIC OBJECTS — NEW S7-NEW-B2: every generated figure registers what it
#       DEPICTS (paper_pipeline.validate_semantic_object; kind STRUCTURE / REACTION
#       carries canonical SMILES) in fig_manifest questions[q].semantic_objects; S13-4
#       commits them to figural_manifests[].semantic_objects. A STRUCTURE figure is
#       RENDERED FROM ITS SMILES through corpus_io.structure_draw_fn inside
#       figural_core.render_figure (verified: passes the v5.57 fit census and G-FIGINK
#       unchanged) — the image and its registration are ONE artefact, so a figure can
#       no longer disagree with its own identity. Hand-placed bonds for a STRUCTURE are
#       a G-FIGSEM defect. EC-V18: a registry without either field is read unchanged.
```

Entry v5.66 moved at framework release 2026.08.24.4 (EC-P42; v5.68 supersedes).

```
# v5.66 — 2026-08-23 — GAP-2026-08-23-ECFG-LABEL-PARITY. The exam_config
#   option_label_format tier — the FIRST tier of the v5.65 chain — was consumed
#   VERBATIM: never passed through pp.resolve_option_label, never family-checked
#   against what the auditor will classify. Two failures, both MEASURED on a
#   synthetic exam against the live auditor: (1) a cross-family override
#   (section_rules '1/2/3/4', exam_config alpha) renders (A)(B)(C)(D) per the
#   documented override while audit_canonical.gate_options classifies family from
#   section_rules ONLY (its L400 cat_c read; exam_config is never read by the
#   auditor) — A-OPTLABEL 'bad label family' FAILED every question, exit 1, no CP
#   repair: the exact GAP-2026-08-03-LABELFMT class v5.37 killed on the
#   section_rules tier, still alive on the override tier. (2) a notation-form
#   override ('A/B/C/D' instead of a template) carries no '{text}' placeholder,
#   so the G-OPTLABEL regex builder and option rendering both operate on a
#   non-template string. FIX (§3 S3-2 config block): the override now goes through
#   the SAME resolver as the section_rules tier, its render family is derived from
#   the resolved template's own token (option_label_family misclassifies template
#   strings — the pass-through branch is NOT trusted for parity), and it is
#   asserted equal to the family the auditor will classify: _resolved_family when
#   section_rules declares a label, else 'num' (the auditor's own L400 default —
#   an override with NO section_rules label is still audited against '1/2/3/4').
#   Mismatch or unknown token = HARD STOP at PRE-GENERATION naming the conflict.
#   Same-family punctuation overrides ('(1)' vs '1.') remain fully supported and
#   byte-identical. DORMANT for every exam_config that omits option_label_format
#   (the IIT_JAM_CHEMISTRY reference config omits it). No engine changes. No
#   artefact moves.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_MockTestCreate.md.

```
# v5.54.0 — 2026-08-12 — THREE DEFERRED DESIGN GAPS CLOSED (scoped 1-by-1)
#   Closes, as individually scoped fixes, the three gaps earlier hardening releases flagged
#   and deliberately deferred (each documented at its flag site + in the audit records):
#   1. GAP-2026-08-12-S13-4B-SCOPED-PATH (spec-only). S13-4b's dossier md5-binding and
#      S13-4c's re-sweep command hardcoded f'{EXAM}_Mock{N}_Create.docx'. DOUBLY wrong:
#      pp.paper_slug zero-pads ("Mock03"), so the literal missed EVERY single-digit mock's
#      actual file (FileNotFoundError at S13-4b for mocks 1-9), and a scoped paper's slug
#      ("SUBJ_Physics_01") never matched at all. Fixed: the docx path is derived from
#      pp.paper_slug(paper_id) — the ONE filename-stem rule — at both sites. The dossier's
#      OWN filename keeps its M[N] form (writer, S13-7 checker, DeliveryFooter and
#      audit_canonical --dossier help all agree on it; outputs/ holds one paper per
#      session, so it cannot collide).
#   2. GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING (engine, final_assembly.py).
#      question_index/session_log deduped by exact paper_id while G-COMMIT-COMPLETE looked
#      up by mock number — a paper_id corrected mid-session then re-committed left a stale
#      same-number sibling no gate could see. Fixed on BOTH sides: commit_registry's
#      dedupe key widened to SAME-SERIES + SAME-NUMBER (one series holds exactly one paper
#      per number; a same-number entry in a DIFFERENT series — MOCK:M01 alongside
#      SUBJ:Physics:01 — legitimately coexists and is never touched), papers_completed
#      drops the renamed same-series/same-number predecessor (unparseable numbers left
#      alone, never guessed at), and regcheck() gains a stale-sibling DETECTOR
#      (G-COMMIT-COMPLETE/DUP): ≥2 same-series entries for one number HARD-STOPS when it
#      is THIS mock's slot, warns for historical mocks — the same fails/warns split as
#      G-COMMIT-COMPLETE itself.
#   3. GAP-2026-08-12-AXISPAPER-PERSISTENCE (spec + engine). S7-AXIS wrote per-paper
#      Axis-1/Axis-3 snapshots onto an in-memory registry object nothing ever dumped —
#      the v5.49 mock-keyed history never reached disk. Fixed: S7-AXIS now only
#      ACCUMULATES the per-section snapshots (axis1_paper_counts / NEW axis3_paper_counts,
#      dead reg writes removed), and S13-4 threads both into commit_registry's new
#      optional axis1_snapshots/axis3_snapshots params, persisted as
#      reg['axis1_paper'][str(N)] / reg['axis3_paper'][str(N)] — replace-by-mock,
#      idempotent, deep-copied, the axis2_window_counts precedent exactly. Read at S13-4
#      via globals().get (an exam with no axis feature never runs S7-AXIS, so the
#      accumulators are legitimately unbound there — that means "nothing to persist",
#      never a NameError). Absent/empty ⇒ no write ⇒ feature-inert exams byte-identical.
#   final_assembly.py self-test: 79 → 96 fixtures (17 new, every new load-bearing branch
#   mutation-verified). No schema change: axis1_paper/axis3_paper already existed in the
#   documented v5.49 shape — this release makes the documented write actually happen.
# v5.53.2 — 2026-08-12 — SPEC-INLINE NAME-FLOW AUDIT (GAP-2026-08-12-SPEC-INLINE-NAME-AUDIT)
#   The v5.53.1 audit proved the one blind spot in the whole verification chain: spec-inline
#   ```python blocks are syntax-checked (validate_framework_md.py Check B) but never
#   name-flow-analysed (Check AJ covers .py engines only), which is how the
#   batches_completed NameError survived 7+ releases. This release closes the CLASS, not
#   just the instance: new tracked repo-level auditor `spec_name_audit.py` v1.0 simulates
#   sequential (notebook-cell) execution of every ```python block in every Framework_*.md
#   and flags any name read before any block binds it. Calibrated against the known bug
#   shape (its self-test embeds the batches_completed fixture: buggy shape MUST flag, fixed
#   shape MUST pass; 16/16, mutation-verified). CI now runs it in baseline-ratchet mode
#   (spec_name_audit_baseline.json freezes the triaged pre-existing findings — illustrative
#   fragments, prose-contract inputs, trigger-provided names; any NEW finding fails CI).
#   Rolling this file back to its v5.53.0 state makes the ratchet fail on exactly the 4
#   real bugs — proof the tool would have caught all of them automatically.
#   ITS FIRST RUN AGAINST THIS FILE FOUND 3 MORE REAL BUGS, ALL FIXED HERE:
#   1. GAP-2026-08-12-S3-17B-BC-UNBOUND — S3-17b (§3, session start; added v5.50/v5.51)
#      reads `bc.axis1_mock_feasibility(...)`, but this file's only
#      `import blueprint_core as bc` lived at §7 S7-NEW-B, which executes LATER. NameError
#      in strict execution order. Fixed: explicit import at the top of the S3-17b block.
#   2. GAP-2026-08-12-S7-AXIS-COUNTS-UNINIT — S7-AXIS's snapshot loop assigns
#      `axis1_paper_counts[sec_name] = snap` and S7-NEW-B reads it, but nothing anywhere
#      initialised the dict. NameError in strict execution order. Fixed:
#      `axis1_paper_counts = {}` at its producer.
#   3. G-ALTGROUP / G-GROUPMANDATE / G-MINCOUNT (§12) called `sys.exit(...)` with `sys`
#      never imported by any block in this file. Fixed: `raise SystemExit(...)` — needs no
#      import and is this file's own house style (20 existing gates already use it).
#   ALSO EXPLICITLY FLAGGED, NOT FIXED (GAP-2026-08-12-AXISPAPER-PERSISTENCE, deferred —
#   design change, not a hardening): S7-AXIS's `reg['axis1_paper']`/`reg['axis3_paper']`
#   writes mutate the in-memory §3 `reg` object that no block ever json.dumps, so in
#   strict execution order they never reach the delivered registry. No engine consumes
#   either field today (verified by grep), so nothing mis-audits; the fix (threading the
#   snapshots through final_assembly.commit_registry(), mirroring axis2_window_counts) is
#   recommended as its own scoped release. Documented inline at S7-AXIS.
# v5.53.1 — 2026-08-12 — FINAL ASSEMBLY ENGINE HARDENING (post-extraction 0-bug audit)
#   A dedicated final adversarial audit (3 independent passes: byte-fidelity diff of
#   final_assembly.py against the pre-extraction spec-inline code it replaced, spec-inline
#   wiring/variable-scope sync check, and adversarial edge-case/mutation hunting) found and
#   fixed 5 real defects surfaced by v5.53.0's Row 0 extraction — 1 CRITICAL (would have
#   crashed EVERY Final Assembly run) and 4 crash-on-malformed-input hardening gaps:
#   1. GAP-2026-08-12-S13-4-UNDEFINED-BATCHES-COMPLETED (CRITICAL). S13-4's call into
#      fa.commit_registry() referenced a bare `batches_completed` name that was NEVER bound
#      anywhere in this file (only `bs['batches_completed']`/`batch_state['batches_completed']`
#      dict keys exist, scoped inside S3-16/S4-8a). This exact NameError was latent in the
#      PRE-EXTRACTION spec-inline code too (v5.52.0 and earlier — confirmed via `git show` on
#      the parent commit), invisible to every verification pass to date because nothing in the
#      chain (gen_manifest/bootstrap/validate_framework_md/check_triggers/self-tests) actually
#      EXECUTES this specific inline block end-to-end. Found by a dedicated wiring-audit pass
#      that traced every variable's binding site by line number, then confirmed live via a
#      real exec() of the extracted S13-4/S13-REGCHECK/S13-QINDEX/S13-7 blocks in sequence
#      against a fixture filesystem. Fixed by reloading batch_state.json fresh at S13-4 (same
#      defensive-reload pattern already used for progress.json/registry.json there), rather
#      than relying on a per-batch local (`bs`) that isn't guaranteed still bound this late.
#   2-4. final_assembly.py regcheck() hardening: a non-numeric msq_meta.total_options no
#      longer raises ValueError (the pre-extraction code's try/except protected this
#      conversion; splitting file-load from schema-gate moved it outside that protection —
#      an extraction-introduced regression, now fixed with its own guard); a malformed
#      (non-dict) concept_map entry no longer raises AttributeError (degrades to "not
#      numerical" rather than crashing); a pre-existing wrong-typed `options_by_q` (e.g. a
#      hand-patched registry) no longer raises TypeError (force-reset to the correct
#      container type, same self-heal spirit as the _REQUIRED_TOP fields). All three are
#      pre-existing crash risks the old spec-inline code also had (same bare-indexing
#      patterns existed before extraction) — hardened now because this function's own
#      docstring promises it never raises, and doing so costs nothing on well-formed input
#      (100% of real production data): all pre-existing self-test assertions are unchanged.
#   5. final_assembly.py predelivery_checklist() hardening: broadened its `except
#      FileNotFoundError` to `except OSError`, so a real filesystem's NotADirectoryError
#      (a file sits where the outputs directory should be) or PermissionError (restricted
#      ACL) degrade to "nothing staged" (checks then fail honestly) instead of crashing.
#   6 new self-test fixtures added for items 2-5, each mutation-verified (neutered the fix,
#   confirmed the self-test catches it, restored) — final_assembly.py --self-test: 79/79.
#   NOT FIXED, EXPLICITLY DEFERRED (a design gap in G-COMMIT-COMPLETE itself, pre-dating
#   this extraction, inherited unchanged from release .10 — out of Row 0's charter to
#   redesign): GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING. question_index/session_log
#   dedupe by paper_id while G-COMMIT-COMPLETE's cross-ledger check keys by mock number; if a
#   mock's paper_id is ever changed and the SAME mock N is committed twice under two
#   different paper_id values (only reachable via an unusual operational error — editing
#   blueprint.json's mocks[].paper_id mid-session then re-running Final Assembly for that
#   mock), the stale entry is never detected or removed. Recommended as its own scoped fix,
#   same as the already-flagged GAP-2026-08-12-S13-4B-SCOPED-PATH.
# v5.53.0 — 2026-08-12 — FINAL ASSEMBLY ENGINE EXTRACTION (Row 0)
#   Closes Finding 0 of the Mock-10 root-cause gap analysis (GAP-2026-08-12-FINAL-ASSEMBLY-
#   ENGINE) — the last open row of the §13 priority table (v5.52.0's SCOPING NOTE flagged it
#   as remaining). §13's S13-4 (registry update protocol), S13-REGCHECK (schema-completeness
#   gate + G-COMMIT-COMPLETE), S13-QINDEX (G-QINDEX certification), and S13-7 (7-point
#   pre-delivery checklist) had zero engine-file backing — pure spec prose a session had to
#   re-type or faithfully re-derive on every single mock, unlike every other load-bearing
#   step in this pipeline (blueprint_core.py / paper_pipeline.py / audit_canonical.py). All
#   four now call into `final_assembly.py`: routed (MockCreate/TestCreate), tracked
#   (gen_manifest.py), self-tested (71/71 fixtures, mutation-tested), and CI-gated
#   (.github/workflows/validate.yml). Semantics are byte-faithful to the prior spec-inline
#   logic — same hard-stop trigger conditions, same wording — with 4 deliberate, disclosed
#   deviations documented in final_assembly.py's own module docstring: every function is
#   PURE (no file I/O, no input mutation); all four return a {'ok', 'fails', ...} result dict
#   instead of raising SystemExit directly (the spec-inline caller raises); qindex_certify()
#   delegates to paper_pipeline.py's pre-existing, already parity-tested
#   validate_question_index() rather than adding a fifth independent copy of G-QINDEX's six
#   checks; and three ledgers (session_log, mocks_completed/papers_completed, rc_manifests/
#   di_manifests/figural_manifests) are now properly idempotent (replace-by-key) where the
#   spec-inline code was append-only. S13-4b/S13-4c (the Tier-A dossier + dossier-fed
#   re-sweep) are deliberately left spec-inline — a different concern (external subprocess
#   invocation), not registry/gate logic.
# v5.52.0 — 2026-08-12 — MANDATORY concept_map CAPTURE + REGISTRY COMMIT COMPLETENESS
#   Closes the last two open rows of the Mock-10 root-cause gap analysis's §13 priority
#   table: row 3 (concept_map/difficulty authoring instruction missing from the consumer
#   spec) and row 5 (partial registry commits, the Mock 4 failure mode).
#   ROW 3 — GAP-2026-08-12-S10-CONCEPTMAP-MANDATE. §S7-NEW-A's write_q_to_sidecar()
#   previously defaulted subtopic_id/difficulty to None, so a call site that forgot them
#   silently persisted `null` — exactly what shipped Mock 10 with difficulty:null on all
#   60 questions, undetected until (if ever) G-QINDEX ran at Final Assembly. Both
#   parameters are now keyword-only with NO default: omitting either is a TypeError at
#   the point of authoring, not a silent null propagated to Final Assembly. New §S10-0
#   states the mandate explicitly in THIS spec's own per-question-authoring section
#   (previously the obligation was documented only in Framework_Blueprint.md §S7-6, the
#   producer's contract, and in §S7-NEW-A's docstring — never as an explicit instruction
#   at S10, where the per-question authoring work actually happens).
#   ROW 5 — GAP-2026-08-12-S13-COMMIT-COMPLETE. New G-COMMIT-COMPLETE gate in
#   S13-REGCHECK cross-checks mocks_completed/session_log/question_index against each
#   other for every mock: a session_log entry AND a question_index entry with a non-null
#   paper_id must both exist. THIS mock's own commit is a HARD STOP if incomplete (a
#   fresh partial write must never reach delivery); a PRE-EXISTING partial commit from an
#   earlier mock is a WARN (repairing historical data is out of scope — same precedent as
#   GAP-2026-08-12-AXISPAPER-HISTORY: fixable going forward, not retroactively). S13-4
#   also gained an explicit ATOMICITY MANDATE comment immediately above its one terminal
#   json.dump, so a future transcription of that block cannot silently regress into
#   incremental (and therefore partially-crashable) writes.
#   SCOPING NOTE: Finding 0 (extracting S13-4/S13-REGCHECK/S13-QINDEX/S13-7 into a real
#   final_assembly.py engine file) remains open — both fixes above are implemented
#   in-place, within the existing spec-inline pattern S13-4/S13-REGCHECK/S13-QINDEX
#   already use, exactly as S13-QINDEX itself does. They do not require, and are not
#   blocked by, the full engine-file extraction.
# v5.51.0 — 2026-08-12 — AXIS-3 PRE-FLIGHT FEASIBILITY (advisory, before Batch 1)
#   (GAP-2026-08-12-AXIS3-PREFLIGHT). Closes the Axis-3 half v5.50 (below) deliberately
#   withheld rather than ship un-verified: a naive subtopic-capability feasibility check
#   for Axis-3 (mechanism MCQ/MSQ/NAT) would be WRONG on any exam whose marking_scheme
#   declares more than one distinct question_type anywhere, because v5.30's POSITION-
#   BASED QUESTION TYPE DISPATCH (`_resolve_answer_axes`, §3 S3-2) means every question's
#   mechanism on such an exam is decided by Q-POSITION (defaulting to MCQ outside any
#   declared range) — in EVERY section, not only the ones GAP-2026-08-12-AXIS3-MECHLOCK's
#   axis3_mechanism_lock marks locked, since `_position_based_typing` is a GLOBAL,
#   exam-wide flag, not a per-section one. A subtopic-capability check applied
#   unconditionally would therefore be not merely useless but ACTIVELY MISLEADING —
#   capable of reporting a shortfall for a mechanism that position dispatch guarantees
#   regardless of which subtopics were allocated.
#   FIX: new `blueprint_core.axis3_mock_feasibility(target, alloc_counts, manifest_ids,
#   position_based_typing)` — `position_based_typing` is a REQUIRED parameter (no
#   default) and the function returns `{}` UNCONDITIONALLY whenever it is True, so the
#   check degrades to a harmless no-op — never a wrong answer — on any exam where
#   subtopic capability is not what actually decides the mechanism. §3 S3-17b (below,
#   extended in place, not duplicated) now computes both axis1_preflight_shortfalls AND
#   axis3_preflight_shortfalls in the SAME per-mock, per-section loop, reusing the SAME
#   `_position_based_typing` variable S3-2 already computes for real drafting dispatch —
#   never a recomputed copy that could drift from what Batch 1 will actually do.
#   S3-18's summary gains a second, parallel AXIS-3 PRE-FLIGHT ADVISORY block, printed
#   only when non-empty — ADVISORY ONLY, never a HALT, identical contract to Axis-1's.
#   blueprint_core.py self-test: 384/384 -> 391/391 (7 new fixtures, including a fixture
#   that feeds an OBVIOUS subtopic-capability shortfall under position_based_typing=True
#   and asserts the function still returns {} — the exact correctness trap this release
#   exists to avoid — mutation-verified twice: once neutering the whole function body,
#   once neutering ONLY the position_based_typing gate while leaving the rest intact,
#   confirming that specific gate is independently load-bearing, not merely coincidental
#   to some other assertion).
# v5.50.0 — 2026-08-12 — AXIS-1 PRE-FLIGHT FEASIBILITY (advisory, before Batch 1)
#   (GAP-2026-08-12-AXIS-PREFLIGHT). Companion release to Framework_Blueprint v1.48's
#   GAP-2026-08-12-AXIS3-MECHLOCK, closing the second half of the Mock-10 root-cause gap
#   analysis's §13 priority table (row 2): "A-AXIS1/A-AXIS3 invisible before Final
#   Assembly." `blueprint_core.axis1_feasibility` (existing, B1/blueprint-build time)
#   answers "does this SECTION have any PYQ subtopic capable of each targeted format,
#   ever" — necessary but not sufficient, since it runs once, before any mock's specific
#   allocation exists. A mock can pass that section-wide check and still be drafted from
#   a subset of subtopics that under-represents the format-capable ones THIS mock needed,
#   purely from how the window's rotation/quota split landed for this specific mock — a
#   structural shortfall invisible until Final Assembly's A-AXIS1 gate audits the
#   finished 60-question paper, by which point fixing it means rewriting already-drafted
#   questions (the exact, expensive discovery-order failure this closes).
#   NEW §3 S3-17b (after the mandatory-subtopic pre-check, before the session-start
#   summary): once this mock's subtopic_allocations are finalised (S3-2/S3-8, well
#   before Batch 1 drafts anything), composes this mock's own Axis-1 target (substituting
#   axis1_target_series[this mock] for the rotating FIGURAL count) and checks it via new
#   `blueprint_core.axis1_mock_feasibility(target, alloc_counts, MANIFEST_IDS)` against
#   the mock's ACTUAL allocation. S3-18's summary prints an AXIS-1 PRE-FLIGHT ADVISORY
#   block naming any short section/format/target/max-achievable — ADVISORY ONLY, never a
#   HALT (mirrors axis1_feasibility's own established contract: "Subtopic is hard #1";
#   Axis-1 is a steered, audited-within-tolerance consequence of allocation, never
#   force-blocking on it). Absent-safe: no axis_schedule, or a section whose status isn't
#   'ok', is silently skipped — byte-identical to every exam that predates this.
#   SCOPE — AXIS-1 ONLY, deliberately, this release. Axis-3 (mechanism MCQ/MSQ/NAT) is
#   NOT included: v5.30's POSITION-BASED QUESTION TYPE DISPATCH (`_resolve_answer_axes`,
#   §3 S3-2) means a mechanism-locked exam's question mechanism is decided by Q-POSITION,
#   not by the allocated subtopic's own answer_cardinality/answer_type — a naive
#   subtopic-capability check would misleadingly report a shortfall for exactly the
#   sections GAP-2026-08-12-AXIS3-MECHLOCK's axis3_mechanism_lock marks 'full'-locked,
#   where the target is ALWAYS achievable by construction. A correct Axis-3 pre-flight
#   needs to branch on axis3_target_source first and is left for its own dedicated,
#   separately-verified change rather than risking a false-positive advisory shipping
#   alongside this one. blueprint_core.py self-test: 377/377 -> 384/384 (7 new fixtures,
#   mutation-verified: neutering the check to "always feasible" makes the shortfall-
#   detection tests fail, confirming they are load-bearing, not decorative;
#   axis1_feasibility itself, and its one existing caller, are byte-identical/untouched).
# v5.49.0 — 2026-08-12 — QUOTA CHECK MOVED INTO THE ENGINE + AXIS-PAPER HISTORY
#   Two independent fixes, found together during a forensic gap analysis of a
#   single exam's 15-mock corpus (four mocks carrying live A-AXIS1 violations;
#   one mock's question_index difficulty shipping null; a fifth mock's
#   axis1_paper/axis3_paper history already unrecoverable).
#   (1) GAP-2026-08-12-QINDEX-QUOTA-ENFORCEMENT — G-QINDEX check 6 (the
#       difficulty distribution EQUALS difficulty_schedule[N] EXACTLY,
#       Contract_QuestionMetadataIndex v1.0) was the one check
#       GAP-2026-08-10-QINDEX-FK-ENFORCEMENT did NOT move into the engine —
#       checks 1-5 (FK/coverage/label validity) did. A session could pass
#       checks 1-5 with a canonical-labelled but wrong-QUOTA distribution (an
#       ungoverned free assessment, or — the mock that motivated this — every
#       difficulty simply left null before S13-4 ever wrote them, since check
#       5 alone would have hard-stopped it had S13-QINDEX actually run) and
#       still log a clean, exit-code-durable audit, because A-QINDEX never
#       compared the count. `audit_canonical.gate_qindex` and
#       `paper_pipeline.validate_question_index` (the reference implementation
#       and its per-exam FK-enforcement twin, GAP-2026-08-10-QINDEX-FK-
#       ENFORCEMENT's four-site architecture) now both implement check 6,
#       dormant when an exam declares no `difficulty_schedule`, kept in
#       parity by the existing QINDEX PARITY self-test harness (extended with
#       a quota-parity leg). S13-QINDEX (below) is unchanged prose — it
#       remains the in-session early check; A-QINDEX is now its
#       engine-enforced, exit-code-logged twin for ALL SIX checks, not five.
#   (2) GAP-2026-08-12-AXISPAPER-HISTORY — S13-4's `axis1_paper`/`axis3_paper`
#       commit (below) now writes `reg['axis1_paper'][str(N)][sec_name]`
#       instead of `reg['axis1_paper'][sec_name]` — mock-keyed, mirroring
#       `options_by_q`'s established `[str(N)] = ...` pattern, instead of the
#       section-keyed, mock-overwriting write every OTHER S13-4 field avoided.
#       Purely additive: the field was write-only (grepped, confirmed unread
#       by any spec or engine in this repo), so no consumer's expected shape
#       changes for the current mock; every PRIOR mock's per-paper Axis-1/
#       Axis-3 counts are now retained instead of being overwritten out of
#       existence by the next mock's commit.
# v5.48.0 — 2026-08-10 — QINDEX FK ENFORCEMENT MOVED INTO THE ENGINE
#   (GAP-2026-08-10-QINDEX-FK-ENFORCEMENT). ROOT CAUSE, proven on a 15-mock
#   reference corpus: registry.question_index subtopic_ids are captured at
#   S7-NEW-A and committed at S13-4 by SESSION-EXECUTED code; the only FK check
#   (spec-inline G-QINDEX) is likewise session-executed and its execution is
#   unverifiable. Three of fifteen sessions persisted INVENTED subtopic_ids
#   (semantically plausible paraphrases of blueprint ids — e.g. a re-typed
#   section slug, a synonym leaf) while truthfully logging audit exit_0/SHIP,
#   because audit_canonical.py — the ONLY enforcement whose exit code is
#   durably logged — never validated question_index at all. The bad ids then
#   hard-stopped Step 11's JOIN, four pipeline steps too late. WHAT CHANGED:
#   (1) S13-4: _qi is now built by JOINING concept_map to blueprint.subtopic_list
#       — the committed subtopic_id is the BLUEPRINT'S OWN STRING (copy-by-
#       reference, never the sidecar's re-typed value); an unjoinable id is a
#       HARD STOP naming the Q-numbers; each row also carries section+subtopic
#       display names (activating Step 11's S1-3 (section,subtopic) fallback,
#       dead until now because these fields were never written); the mock entry
#       carries a qindex_cert {blueprint_version, subtopic_set_hash} provenance
#       stamp.
#   (2) S13-4c: the re-sweep now passes --registry --blueprint --mockN, arming
#       the NEW ENGINE GATE A-QINDEX (audit_canonical.py v2026.08.10): entry
#       exists, count/coverage, every id ∈ blueprint, every difficulty ∈ labels.
#       A FAIL is a nonzero exit handled exactly like any S13-2 FAIL —
#       present_files forbidden until clean. A session can no longer ship a bad
#       index while logging a clean audit: the logged exit code IS the gate.
#   (3) S13-QINDEX (G-QINDEX) is retained unchanged as the in-session early
#       check; A-QINDEX is its engine-enforced, exit-code-logged twin.
#   Companion changes: audit_canonical.py (A-QINDEX), paper_pipeline.py
#   (validate_question_index / registry_integrity_check / classify_unresolved /
#   subtopic_set_hash), Framework_MockTestExplain v1.23 (P10 tripwire),
#   Framework_MockDeliver v1.12.0 (ledger check + remediation classifier).
# v5.47.3 — 2026-08-07 — ONE MASK SET, TWO CONSUMERS (review findings on v5.47.2).
#   (1) _yearform's [A-Za-z]+ swallowed single-letter-over-year fractions
#       (N/2000, M/1950, E/2026) — the cure was wider than the March/2026
#       complaint. Repaired to [A-Za-z]{2,} (month names keep masking; every
#       single-letter numerator fires again).
#   (2) STRUCTURAL FIX for the divergence class: the gate's masks lived only in
#       the gate, while needs_omml kept the old narrow UNIT_LABEL_RE (with the
#       \b-before-² bug, no word-pair mask, h|s|min|hr only) — m/s², 3/2 and
#       is/are were gate-silent but needs_omml-True, and needs_omml feeds
#       assert_not_math, which RAISES. There is now ONE shared mask set
#       (_MM_UNIT/_MM_WORDPAIR/_MM_YEARFORM) and ONE masked detector,
#       consumed by BOTH the gate and needs_omml — agreement is structural,
#       not claimed. UNIT_LABEL_RE is retired to a compatibility alias.
#       NAMED ASYMMETRY (deliberate, not divergence): digit/digit (3/2) stays
#       needs_omml-True — rule 3 makes digit fractions mandatory OMML at
#       routing — while the post-build gate is lenient on rendered digit/digit
#       (dates, scores). Same masks, different pattern scope, on purpose.
#   (3) Named behavioural scoping (the second consumer the v5.47.2 changelog
#       failed to name): widening MATH_TRIGGER_RE had widened assert_not_math's
#       build-aborting figural ban too — ordinary normalised-axis labels
#       (σ/σ₀, λ/λ₀, α/β, Δv/Δt) began aborting builds. assert_not_math now
#       tests the ORIGINAL v4.3-scope RASTER_BAN_RE (letters/digits fraction,
#       caret, superscript-on-term, raw LaTeX, √( ) — restoring pre-v5.47.2
#       figural behaviour exactly, while stem/option ROUTING keeps the widened
#       Greek/subscript detector. Whole expressions still never rasterise.
# v5.47.2 — 2026-08-07 — GATE FIXES (review findings 1–3 on v5.47.1):
#   (1) m/s², rad/s² were false positives: ² is a \w character, so the _unit
#       mask's trailing \b never matched after "s" — denominators (and
#       numerators, for cm²/s) now take an optional [²³] before the boundary.
#   (2) Uppercase and most lowercase Greek were missing from the fraction
#       classes: Δv/Δt, α/β, ρ/σ, ℏ/2, Ω/2, Σ/n, v/c passed silently. Both
#       gate classes AND the MATH_TRIGGER_RE fraction branch now carry the
#       full Greek block (\u0391-\u03c9) plus ℏ, so authoring detection and
#       the post-build gate agree.
#   (3) Known accepted noise, recorded so it is not rediscovered: widening the
#       right class to digits admits non-math letter-over-digit ("Paper A/2",
#       "Section B/1"). Word-slash-YEAR ("March/2026") is masked; the rest is
#       low-volume amber-only operator attention by design (warn-and-deliver).
# v5.47.1 — 2026-08-07 — GATE FIX (review finding on v5.47): the letter-fraction
#   residue pattern required a LETTER after the slash, so letter-over-DIGIT
#   fractions (M/3, E/2, v/2) — including this release's own headline example —
#   passed silently. The right-hand class now admits digits; the left-hand class
#   deliberately does not, so digit/digit (3/2), dates (12/3) and masked units/
#   word-pairs stay non-firing. √N (bare digit radicand) remains deliberately
#   non-firing: readable as-is, and t3_mathcomp auto-converts it inside regions.
# v5.47 — 2026-08-07 — TIER-3 MATH (GAP-2026-08-07-MOCK-OMML, remedies MC1–MC3).
#   Measured on IIT_JAM_PHYSICS Mock05 (14/60 questions): letter fractions left
#   linear in stems ("M/3", "a/√n"), subscripts shipped as flat text ("k_B T",
#   "R_in") because MATH_TRIGGER_RE had NO underscore branch and S10-4 had no
#   subscript vocabulary at all, one caret exponent, and — latent — the S10-4
#   frac/sup/sqrt builders accepted RAW text (schema-invalid <m:num>3</m:num>
#   that Word renders as an EMPTY placeholder; the exact GAP-2026-08-07-
#   EXPLAIN-OMML defect, one forgotten _r() away from firing here).
#   Fix: (MC1) builders _r_wrap + XML-escape internally — raw args are now safe;
#   (MC2) S10-4 delegates to the SHARED Tier-3 compiler t3_mathcomp.py (byte-
#   locked to Framework_PYQPrepare §S3-5b): new single funnel render_mock_text()
#   dispatches ⟦MATH:…⟧ regions with the strict-core/forgiving-boundary contract
#   (a bad region degrades to plain unmarked text and is quoted VERBATIM for
#   Ctrl+F — never a halt, never silent); MATH_TRIGGER_RE gains underscore-
#   subscript, ÷ and combining-accent branches; the decision tree names
#   subscripts as built-up math; (MC3) new mock_math_residue_check() post-build
#   gate scans the rendered docx for dialect residue, bare-text fraction parts,
#   empty OMML and region delimiters, reporting in plain operator words —
#   mandatory before delivery, amber-not-halt. routes.json binds t3_mathcomp.py
#   to MockCreate/TestCreate.
# v5.46 — 2026-08-07 — GAP-2026-08-07-FIGACCENT: the S10-6A palette column was
#   normative prose with NO enforcing gate. "1 accent hue permitted" (data_single)
#   and ">=1 accent for the item under interrogation" (schematic) had a Colour-gate
#   column reading "not required", and figural_core's COLOUR_REQUIRED covered
#   data_series only — so an all-black paper (IIT JAM PHYSICS Mock01, 16/16 figures
#   at 0.0000% coloured pixels, the pre-v5.33 "solid black" habit of RC-1) and an
#   accented paper (IIT JAM BIOTECH Mock01, 0.10-1.11%) both passed every gate
#   identically, and cross-exam figure style drifted with session taste. Remedies:
#   (1) Q7b.8 — the accent is now MANDATORY for data_single (owner decision
#   2026-08-07: "permitted" -> mandatory, OKABE_ITO[0] series ink) and for
#   schematic (interrogated item), gated by G-FIGACCENT/A-FIGACCENT, AMBER by
#   construction (fire-0 history does not exist yet; owner directive: colour never
#   halts); floor coloured_fraction >= 0.05%, calibrated on the real corpus
#   (accented minimum 0.105%, all-black 0.0000%, 2x margin, zero false positives)
#   and deliberately NOT gated on dominant_hues (its area cut swallows small
#   accents). (2) The draw_fn authoring contract: accent ink MUST come from the
#   palette argument, never hardcoded black. (3) render_figure() gains an optional
#   palette= parameter — the plumbing Q7b.1 promised; exam_config wiring stays
#   RESERVED. reasoning_glyph monochrome doctrine and EC-V18 legacy tolerance are
#   untouched; ~200 pre-v5.33 exams stay silent under this gate.
# v5.45 — 2026-08-06 — GAP-2026-08-06-SEAM: DI was not in sync with FIGURAL.
#   The rate->quota->schedule->rank chain was built for FIGURAL only; DI kept a
#   render-time cap and its measured rate was discarded, so on a DI-heavy exam the
#   COUNT was right and the DISTRIBUTION was not. Measurement and scheduling are now
#   keyed BY CLASS, so DI and PASSAGE inherit the whole chain and a future class needs
#   no release. New audit_seam.py cross-checks producer/consumer fields across steps.
# v5.44 — 2026-08-06 — GAP-2026-08-06-EXAMDEP: exam-independence.
#   Six defects invisible on the reference exam (46 figural subtopics vs a budget of
#   4.4) and fatal on shapes it does not have: a hard-coded 1-figure-per-subtopic-per-
#   mock cap (10 subtopics/25 figures delivered 10, forever); total_mocks read from a
#   key nobody wrote, so the whole estate got a 15-mock series; quota keyed by display
#   name when subtopic_id was absent, silently yielding ZERO figures; sorted() over
#   mixed None/int paper keys crashing Step 5; the last DI any() existential; and the
#   subject-merge fallback dropping the new keys.
# v5.43 — 2026-08-06 — GAP-2026-08-06-IRREDUCIBLE: figures are SCHEDULED, not forced.
#   The render fork decided figural-vs-text per question from a boolean, so a
#   subtopic allocated to every mock drew a figure in every mock whatever its
#   measured frequency, and an irreducible flag let it pass over budget silently.
#   Step 7 now reads Step 6's per-mock figure schedule (bc.schedule_figural_slots).
#   Absent schedule -> v5.41 ranking, so un-remeasured exams are untouched.
# v5.42 — 2026-08-06 — GAP-2026-08-06-DI: DI becomes measurable.
#   DI was the one budgeted Axis-1 stimulus class leaving NO trace anywhere, so
#   A-AXIS1 could only ever report it UNESTABLISHED. It cannot be recovered from the
#   docx: G-MATCH-TABLE mandates a real Word table for every MATCH question, so on a
#   real paper table-presence finds 3 candidates where exactly 1 is DI. Step 7 now
#   records di_manifests (the producer's own record) and asks the Axis-1 budget
#   before building a table stimulus; Step 5 emits di_rate/di_q_count/di_reducible.
#   Absent-safe: no di_manifest -> DI stays unestablished, exactly as before.
# v5.41 — 2026-08-06 — GAP-2026-08-06-AXIS1: a budget nothing spent.
#   `format: FIGURAL` was a RENDERING IMPERATIVE with no cap while
#   axis1_target_per_mock — written since blueprint v1.23 — was read by NOTHING.
#   Two delivered mocks carried 26 and 30 figures against a budget of 4, and all
#   24 machine gates certified them clean. Format now means ELIGIBILITY: how many
#   are drawn is capped by the Axis-1 budget, which ones by measured figural_rate.
#   Axis-3 had the identical unspent-budget defect and is fixed in the same release.
#   Standing rule: any axis marked enforcement:"hard" MUST have a spender in Step 7
#   and a gate in the auditor (A-AXIS-UNGATED). Absent-safe; no deployed exam moves
#   until it is re-measured via PYQExtract -> MockBlueprint -> MockCreate.
# v5.40 — 2026-08-03 — DEFECT FIX: the Tier-A dossier had lost its reader.
#   v5.39 retired Step 8, which was the only consumer that passed `--dossier` to the
#   auditor. The writer (S13-4b) survived; the reader did not. audit_canonical.py still
#   exposes the flag, nothing passed it, and A-NAT-GRADE + A-FIGPROFILE silently went back
#   to re-deriving what Step 7 had already recorded — the regression the dossier exists to
#   prevent. NEW S13-4c re-runs the SAME auditor over the SAME final docx with `--dossier`
#   immediately after S13-4b writes it (it cannot live in S13-2, which runs before the file
#   exists). No new gate, no new hard stop, no new artefact.
#   Also: Step 7 now delivers the dossier explicitly in the Step-7 footer template
#   (Framework_DeliveryFooter v1.12).
#
# v5.39 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   Step 7 now hands the paper straight to Step 9. Every clause that promised a downstream
#   re-verification ("independently re-verified by Step 8 A-HEADER", "audited within
#   tolerance at Step 8", "Step 8 re-derives subtopic_id") has been restated against what
#   actually runs: the SAME canonical A-* catalogue, in audit_canonical.py, executed HERE
#   via [ExamCode]_mock_test_audit.py at S3-10 / S4-11. audit_canonical.py is KEPT and Step
#   6 B3 still generates the per-exam copy.
#   NO RULE WAS ADDED: audit.py remains OPTIONAL to run (S4-11's manual checklist still
#   substitutes when it is absent). What changed is the reporting duty — its absence must
#   now be stated explicitly in the batch report, because with no audit step downstream an
#   absent audit.py means NO machine gate ever runs over the paper.
#   ACCEPTED LOSS, stated once: subtopic_id, the answer key, the axis distribution and the
#   figure conformance verdicts are no longer independently re-derived by a second reader.
#   The Tier-A dossier (S13-4b) is still written; its consumer is now the author.
#
# v5.38 — 2026-08-03 — THE SELF-TEST BANNER REPORTED PASS OVER A FAILED RUN.
#   GAP-2026-08-03-BANNER. Caught at deployment review of v5.37, BEFORE it shipped.
#
#   v5.37 appended its 13 LABELFMT fixtures AFTER the line that prints
#   "SELF-TEST: {p}/{p+f} PASS". Reintroducing v5.37's OWN defect produced:
#         SELF-TEST: 37/37 PASS          <- printed first
#         Traceback ... LabelFormatError
#         exit=1
#   The exit code was correct, so the release gate still failed — but every human
#   reading the banner, and every spec quoting it, saw PASS over broken work. That
#   is the false-clean-banner shape (GAP-2026-07-26-003, "QV-9 PASS and a green Step
#   Complete footer"), reintroduced by the very release that was closing a sync bug.
#   14 assertions were outside the count: the true figure was 51, not 37.
#
#   SECOND, DEEPER DEFECT IN THE HARNESS ITSELF: ck(name, cond) receives an
#   ALREADY-EVALUATED condition, so an exception inside a fixture PROPAGATES and
#   ABORTS the whole self-test — every later fixture silently never runs. The
#   LABELFMT fixtures call resolve_option_label(), which RAISES by design. A hollow
#   branch in the test harness is worse than one in a gate: it hides all the others.
#
#   FIX. The banner is now the LAST thing computed, immediately before the return,
#   and names every failing fixture. New ck_call(name, fn) evaluates a fixture that
#   may raise and COUNTS A RAISE AS A FAILURE. Verified: clean run prints 51/51;
#   with v5.37's defect reintroduced it prints 46/51 with all five failures named
#   and no green banner anywhere.
#
#   PERMANENT CONTROL: validate_framework_md CHECK AQ — in any engine with a
#   self-test, no ck(/ck_call(/check( may appear after the banner print. Mechanical,
#   exact, and binds engines not yet written. Negative-tested.
#
# v5.37 — 2026-08-03 — OPTION LABEL RESOLUTION WAS RE-IMPLEMENTED, AND THE TWO
#   IMPLEMENTATIONS DISAGREED. GAP-2026-08-03-LABELFMT.
#
#   Found by a line-by-line Step-7/Step-8 sync audit, not by a failing run — it is
#   LATENT, and fires the first time any exam declares roman option labels.
#
#   THE DEFECT. This step turned the section_rules option_label_format notation
#   into a render template by testing the LEADING TOKEN'S CASING. It had no roman
#   branch and no else-branch:
#     'i/ii/iii/iv'      -> .islower() is True for 'i' -> ({alpha_lower})
#                        -> RENDERS (a)(b)(c)(d), while Step 8's
#                           option_label_family reads the same string as 'roman'.
#                           A-OPTLABEL then FAILS EVERY QUESTION, exit 1, Step 8
#                           refuses to certify, and NO CP repair can fix it because
#                           the paper matches THIS STEP'S OWN contract. Confirmed
#                           end-to-end on a rendered paper.
#     'I/II/III/IV'      -> identical failure via .isupper().
#     '(1)/(2)/(3)/(4)'  -> matched no branch, so the NOTATION ITSELF became the
#                           render template — a template with no {text} placeholder,
#                           i.e. no substitution at all.
#     '[A]/[B]/[C]/[D]'  -> silently became '(A)'.
#     circled digits     -> silently became '1.'  (Python .isdigit() is True for them).
#
#   FIX. Resolution moves to paper_pipeline.resolve_option_label(), which is routed
#   by BOTH MockCreate and TestCreate, so one function is reachable from both
#   steps and the pair cannot drift again. Roman is RENDERED, not aliased ({roman_upper}
#   / {roman_lower} tokens, also taught to the G-OPTLABEL prefix regex). The resolver
#   ASSERTS that the family this step renders equals the family Step 8 classifies and
#   RAISES LabelFormatError otherwise, so 'i/j/k/l' (renders alpha, classifies roman)
#   and '[A]/[B]/[C]/[D]' (renders alpha, classifies num) are REFUSED AT
#   PRE-GENERATION rather than producing a paper that could never certify. An
#   unrenderable notation hard-stops instead of guessing — the same posture as
#   pick_blueprint (PickError) and derive_nat_grading, and for the same reason: a
#   guessed label reaches the delivered paper.
#
#   VERIFIED BY ROUND TRIP: for all NINE supported notations, output rendered as
#   this step renders it passes Step 8's A-OPTLABEL / A-OPTORDER / A-OPTUNIQUE.
#   paper_pipeline self-test 22 -> 37. No existing notation changes behaviour.
#
# v5.36 — 2026-08-01 — GAP-2026-08-01-DELIVERY-SET-DRIFT: STEP 7 HARD-STOPPED AT
#   PRE-DELIVERY ON EVERY EXAM. v5.35 added the Tier-A dossier as a THIRD delivered
#   file (S13-4b) and did not widen S13-7 check 6, which asserted
#   `staged == {docx_name, reg_name}` — a hardcoded set of two. The third file made
#   the comparison false, S13-7 raised SystemExit, and Step 7 could not deliver.
#   Step 7 had been the one step in this pipeline that never failed; an improvement
#   made for Step 8's benefit broke it, and it would have failed on the FIRST run
#   after deployment.
#
#   WHY NOTHING CAUGHT IT. All six auditors reported zero findings, twice, plus a
#   fresh-clone deployment simulation — and they still would. NO CHECK ANYWHERE
#   cross-verifies the Step-7 closed deliverable set against what Step 7 actually
#   stages. validate_framework_md's cardinality check AK covers the 19 .py files of
#   the B3 bundle, a different contract. The delivery set was stated in prose at
#   four sites and asserted in code at one, with nothing binding them together —
#   the same "rule with no machine check behind it" class this corpus keeps
#   rediscovering, this time across a STEP BOUNDARY rather than inside one file.
#
#   THE FIX. S13-7 check 6 now DERIVES the expected set from what was written
#   (docx + registry always; dossier when S13-4b produced one) instead of
#   hardcoding a count, so a producer change and its gate cannot disagree by
#   construction. R-DELIVER, G-DELIVERY-SET and the §13 prose are corrected in
#   lockstep, and a new cross-file check (validate_framework_md CHECK AL) fails
#   the build if any site states a delivery-set cardinality the others do not.
#   Absent-safe: a pre-v5.35 mock writes no dossier and the set is exactly 2,
#   byte-identical to v5.34 behaviour.
# v5.35.1 — 2026-08-01 — self-test count refresh only (105/105 -> 107/107).
# v5.35 — 2026-08-01 — TIER A: emit [ExamCode]_M[N]_audit_dossier.json for
#   Step 8 (S13-4b). Facts only, never judgments; MD5-bound to the paper.
# v5.34.3 — 2026-08-01 — self-test count refresh only (89/89 -> 107/107, D2+D4).
# v5.34.2 — 2026-08-01 — self-test count refresh only (78/78 -> 107/107, C1).
# v5.34.1 — 2026-08-01 — self-test count refresh only (73/73 -> 107/107, B3).
# v5.34 — 2026-08-01 — FIGURESPEC TRANSPORT TO STEP 8
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT D2). One additive field at S13-4; zero
#   change to any render, any question, any gate, any deliverable.
#
#   WHAT WAS WRONG. v5.33 renders every figure through figural_core, and
#   render_figure() MUTATES the FigureSpec with what actually happened —
#   png_px, png_dpi, placed_in, placement_scale, font_pt_native — after reading
#   the saved artefact back. write_spec_sidecar() then drops that record beside
#   the PNG as q{N}_*.figspec.json. Step 8's thirteen figure-conformance
#   gates (v2.11 + A-FIGACCENT, v5.46) are arithmetic over the PNG AND ITS SIDECAR.
#
#   But the sidecars live in THIS session's working directory, which is internal
#   and is never delivered (S0-1 / R-DELIVER lists the closed set: the docx, the
#   registry, and — from v5.35 — the Tier-A audit dossier when S13-4b wrote one). So Step 8 saw spec == {} on every figure, fc.is_legacy() read
#   every v5.33 render as pre-v5.33 output, and EC-V18 leniency was applied to
#   papers that were not legacy at all. The gates could not fail on a real
#   regression because they never had the record to compare against.
#
#   THE FIX. S13-4 writes the sidecars into
#   registry.figural_manifests[].figure_specs, keyed by the canonical PNG name
#   S10-8 already stamps on each drawing (_name_last_drawing ->
#   "q{N}_problem.png" / "q{N}_opt{i}.png"), which is the same base
#   write_spec_sidecar() names the sidecar after. The registry is the sanctioned
#   channel for precisely this: it is the one artefact Step 8 receives, and it
#   is the precedent object_types/subtopic_ids set at v5.31 for the identical
#   reason. Absent-safe both ways — a session that rendered no figural_core
#   figure writes no sidecar, the field is {}, and Step 8 reads legacy, i.e.
#   exactly the pre-v5.34 behaviour. Nothing is written to the docx and nothing
#   new is delivered; B3/R-DELIVER cardinality is untouched.
#
# v5.33.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   1267 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestCreate'. The current companion block, the
#   v5.33 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v5.33 — 2026-07-29 — FIGURE COLOUR, LABEL LEGIBILITY AND PLACEMENT SCALE
#   (GAP-2026-07-29-FIG-R2 + VERIFY-2026-07-29-FIG-R2).
#   Measured across 208 delivered drawings in four exhibits: 0 of 55 IIT JAM figures
#   contained a single coloured pixel; placement scale was 0.500 EXACTLY on 24 of 24
#   option canvases; on-page labels ran to a median of 6.7 pt; 0 of 208 drawings
#   carried alt text. The three GATE papers, believed correct, measured 115 of 153
#   figures below a 9 pt floor — they were not a working reference, only a quieter
#   failure, and their colour came from session code that bypassed this spec entirely
#   (three distinct document-assembly paths across four exhibits).
#   FOUR root causes, not one:
#     RC-1 S10-7 Q7 MANDATED "solid black". The monochrome output was CONFORMANT.
#          The implementation was faithful; this spec was the defect.
#     RC-2 FIG_NATIVE_HEADROOM=2.0 supersampled the canvas and was never compensated
#          in the font size, while placement width came from a CONFIGURATION constant
#          rather than the saved artefact. p_page = p_native x S, and the spec
#          controlled neither S nor p_page. A 10 pt label landed at 5 pt.
#     RC-3 Nothing required colour to be redundant with a second visual channel, so
#          greyscale printing and colour-blind readers were served by luck.
#     RC-4 (found by VERIFY, absent from the gap) render_figural_image() sets
#          ax.axis("off") in BOTH branches, and the corpus contained no set_xlabel,
#          no set_ylabel, no legend, no rcParams and no fontsize anywhere. It is an
#          abstract-geometry GLYPH renderer and was being used for scientific data
#          figures, which it structurally cannot label. S8-5, the section that would
#          hold the data-figure path, was an empty title; insert_chart_image(), the
#          function that would call it, was referenced and never defined.
#   Fix: (1) new engine figural_core.py — the data-figure renderer the framework never
#   had, beside (not replacing) the geometry-glyph path. (2) S10-6A FIGURE CLASS
#   taxonomy; class is declared, never defaulted. (3) S10-7 Q2/Q3/Q7 rewritten, Q7b and
#   Q9 added. (4) S10-8 places from the FigureSpec and stamps alt text. (5) S8-5 filled.
#   DISPLAY WIDTH IS A LAYOUT DECISION AND STAYS FIXED; the render is solved to fit it.
#   The inverse rule (place every figure at its native size) was measured and REJECTED:
#   it inflates figure area 1.84x and makes a four-option MCQ need 10.4 in of option
#   stack against a ~9.0 in page text height, orphaning options from their stem.
#   FIG_NATIVE_HEADROOM is retired to 1.0 and bbox_inches="tight" is banned on this
#   path; constrained_layout gives the same margins with a deterministic size, so
#   S == 1.0 by construction rather than by luck.
#   G-FIGLABEL is ARITHMETIC over recorded render-time font metrics, NOT pixel
#   connected components: verified counter-example — three renders at an identical
#   10 pt request and identical saved width, and the one whose axis titles carried
#   "µmol photons m⁻² s⁻¹" and "Net CO₂ assimilation" measured 8.5 pt while
#   short-label renders measured above the floor. A pixel gate is biased against
#   exactly the scientific notation Q9.4 mandates.
#
```

## Framework_MockTestExplain.md

Section §7A-R (REPAIR MODE, v1.42.0–v1.46.3) RETIRED and moved here VERBATIM at framework
release 2026.08.27.3 (REPAIR-RETIRED-2026-08-27, operator decision). Not executable.

````
## §7A-R — REPAIR MODE (TestExplainRepair / MockExplainRepair, v1.42.0; v1.44.0 — STATE-PAIR PREFLIGHT, ATOMIC RE-GATE; v1.45.0 — WINDOWED RE-GATE)

  TRIGGER: `TestExplainRepair P[N]` or `MockExplainRepair M[N]`.
  ATTACH:  (1) the REPAIRED question paper docx (TestCreateRepair output) and
           (2) the PREVIOUS explanation docx (this step's earlier output).
  PREFLIGHT (HARD STOP on any failure — these protect the operator from
  repairing the wrong thing, so they stay hard even under the no-stop rule,
  which governs the VERDICT, not malformed input):
    ORDER IS FIXED: R0 → R1 → R2 → R3. Registry legality is checked BEFORE
    anything about the operator's files, because a corrupt registry makes
    every downstream verdict meaningless and its remedy has nothing to do
    with the attachments.
    R0  rec, disclosure = pp.dg_preflight(reg, paper_id, where='§7A-R R0')
        An ILLEGAL (status, repair_rounds_used) pair is NOT "a round already
        used" — it is a CORRUPT REGISTRY, healed here per DG-INVARIANT (a
        FAILED record's counter is reset to 0: the round is provably
        unconsumed). If disclosure is not None: print disclosure['line']
        verbatim in chat, persist the registry (S19-0 write), and CONTINUE. A DGIllegalState
        (unknown status) is a HARD STOP: print its message verbatim. Never
        route the operator onward on an illegal record — the historical
        failure was exactly that (FAILED + 1 → "go to TestDeliver" → Step 11
        hard-stops on FAILED → TestCreateRepair refuses "consumed" → no exit).
    R1  BRANCH ON THE STATE PAIR pp.dg_state(rec), never on one field. Every
        next-step string is pp.dg_next_step(reg, paper_id, N, mock=<Mock*
        trigger>) — the SAME function Step 11 prints from — never restated:
          absent            → "This is a legacy paper (no gate record) —
                               nothing to repair. Next step: " + next_step
          ('PENDING',   0)  → "Run TestExplain P[N] first — the gate has not
                               run. Next step: " + next_step
          ('FAILED',    0)  → if pp.dg_is_windowed(rec): PROCEED (the one and
                               only repair round). Else (v1.45.0 — the record
                               was judged FAILED under the retired band-
                               equality rule, GAP-2026-08-25-DIFFICULTY-GATE-
                               WINDOWS): "This paper was judged under the old
                               difficulty rule — nothing is repaired on its
                               say-so. Next step: " + next_step (which is the
                               Explain trigger: re-run it so the verdict is
                               re-judged under the windows). HARD STOP.
          ('PASSED',    0)  → "Nothing to repair — next step: " + next_step
          ('PASSED',    1)  → "Already repaired and passed — next step: " + next_step
          ('DISCLOSED', 1)  → "The one repair round is already used — next
                               step: " + next_step + " (delivers with disclosure)."
          ('DORMANT',   0)  → "This paper's gate is dormant ([dormant_reason])
                               — nothing to repair. Next step: " + next_step
        (No other pair can reach R1: R0 healed or refused it.)
    R2  Both attachments present and parse (P3 machinery): the
        [ExamCode]_[paper_slug]_Create_Repaired.docx paper (S2-1 / P1 accept this
        form on this trigger — v1.46.1) and the previous
        [ExamCode]_[paper_slug]_Explanation.docx; both must carry the SAME
        paper_slug as the trigger's paper N (P10/0 identity gate) or HARD STOP.
    R3  Stem diff against the PRE-REPAIR SNAPSHOT ONLY, via the shared digest:
          v = pp.dg_verify_repair(rec, {q: <first-paragraph text of q in the
                                         REPAIRED paper, raw — see
                                         pp.dg_stem_hash> for q in 1..N})
        v['missing_snapshot'] → HARD STOP: "The repaired paper was produced
          without §S16-3's snapshot — re-run TestCreateRepair P[N]." Never
          fall back to registry.stem_texts (TestCreateRepair has already
          overwritten it with the post-repair stems, and it is a flat
          append-only list across all papers with no defined per-paper
          offset).
        v['ok'] is False → HARD STOP naming v['changed_unlisted'] ("changed
          questions the gate did not flag: Q…" — detectable only when the
          §S16-3 snapshot carries baseline_stem_hashes for every question;
          v['extras_verifiable'] says whether it does; a pre-v5.71 snapshot
          without it verifies the flagged questions only, and the run says
          so in §R10) and/or v['unchanged_listed']
          ("failed to change a flagged question: Q… — if ALL of rework_qs is
          listed here you attached the PRE-repair paper by mistake"). It is
          the wrong file.
        pp.dg_stem_hash is the ONE digest (sha256 of the raw first paragraph
        including the "Q.<n>" label, no normalisation); §S16-3 computes the
        snapshot with the same function. Neither side implements its own.
  RUN: execute §4–§18 for the rework_qs ONLY (batching rules apply to that
    subset); splice the regenerated per-question blocks into the previous
    explanation docx, replacing the superseded blocks in place (block = the
    question's full §2 structure); leave every other block byte-identical.
  RE-GATE: rebuild scores_by_q AND measured_by_q for the untouched qs from
    the record's measured_score_by_q / measured_by_q (the engine accepts the
    record's str keys) and update BOTH for the repaired qs only; re-run
    bc.evaluate_difficulty_gate(labels_by_q, measured_by_q, difficulty_labels,
    scores_by_q=scores_by_q) over the FULL maps with the engine defaults;
    then ONE write, via the single writer:
      pp.dg_write_verdict(reg, paper_id,
          status='PASSED' if gate['verdict'] == 'PASS' else 'DISCLOSED',
          rounds=1, threshold=gate['threshold'], bands=<as §7A-M>,
          measured_by_q=measured_by_q, rework_qs=gate['rework_qs'],
          scores_by_q=scores_by_q,
          rework_directions=gate['rework_directions'],
          windows=gate['windows'])
    (on DISCLOSED, rework_qs / rework_directions document what remains out of
     window; no further repair command is printed.)
    ATOMIC, TERMINAL, IDEMPOTENT (v1.44.0). The counter and the status are
    written ONCE, TOGETHER, at the END of a successful re-gate, by that call.
    NEVER increment repair_rounds_used on ENTRY, never in a separate write,
    never by hand — an entry-time increment that crashes before the re-gate
    reproduces the deadlocked (FAILED, 1) pair by a second route, and
    pp.dg_write_verdict refuses that pair outright. A run that crashes
    mid-repair therefore leaves (FAILED, 0) untouched and is simply RE-RUN:
    safe, because TestCreateRepair's rework_stem_hashes snapshot is the
    PRE-repair evidence and is carried forward unchanged by every re-gate.
    SESSION LOG — in the SAME registry write, append the evidence trail:
      reg.setdefault('session_log', []).append({
          'step': 'TestExplainRepair' (or 'MockExplainRepair'),
          'paper_id': paper_id, 'round': 1, 'verdict': gate['verdict'],
          'qs': rec['rework_qs']   (the PRE-repair list read at R0 — NOT
                                    the re-gate's new rework_qs),
          'timestamp': <utc-now>,
          'spec': 'Framework_MockTestExplain v1.44.0 §7A-R'})
    Recovery does NOT depend on this entry (DG-INVARIANT makes the record
    self-diagnosing); without it no later audit can reconstruct what ran.
    Resulting status:
      PASS → 'PASSED'   — print the PASSED box (§7A-M shape).
      FAIL → 'DISCLOSED' — the one round is spent; NO further loop and NO stop
             (operator decision). Print:
      ════════════════════════════════════════════════════════════
        DIFFICULTY GATE: ⚠️ PROCEED WITH DISCLOSURE
      ════════════════════════════════════════════════════════════
        After 1 repair round: [bottom] [n] (not gated) · [middle]
        [b]/[m] in window · [top] [c]/[h] in window. The paper MAY
        be delivered; the delivery footer will state these measured
        counts so no reader is misled.
        Next step:  TestDeliver P[N]
      ════════════════════════════════════════════════════════════
    (the "Next step" line is pp.dg_next_step(...) verbatim; on a DISCLOSED
     record it is guaranteed to be the Deliver trigger, which Step 11 accepts.)
  DELIVERABLES (v1.46.0 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM; this section had NO
    delivery contract through v1.45.1, so the re-gate verdict stayed in /home/claude and
    Step 11 kept reading (FAILED, 0) from the project). The CLOSED SET, one present_files
    call, F2 footer, is pp.handoff_set('TestExplainRepair', …, final=True) — run S19-0b →
    S19-1 → S19-2 → S19-4 exactly as a final batch, with FINAL_BATCH = True and
    HANDOFF_STEP = 'TestExplainRepair' (or 'MockExplainRepair'):
      1. [ExamCode]_[paper_slug]_Explanation.docx — the previous explanation docx with
         the rework_qs blocks replaced in place, SAME filename (Step 11's S1-2 gate
         accepts exactly this name)                                → Use locally
      2. [ExamCode]_registry.json — carries the re-gate verdict (PASSED/1 or DISCLOSED/1)
         + the session_log entry                                   → Replace in Project Files
      3. [ExamCode]_[paper_slug]_Explain_Report.docx — the §20 report regenerated as the
         REPAIR EDITION (§R1 states "repair round 1"; §R3 lists the rework_qs re-explained;
         every other section reports the whole paper as it now stands) → Use locally
    The re-gate is ONE write (above); pp.registry_changed is therefore True on every
    successful repair run, and a run whose registry is unchanged has NOT re-gated — S19-0
    HARD-STOPS it rather than deliver a stale verdict (S19-0b).
````

Entry v1.40.0 moved at framework release 2026.08.25.3 (EC-P42; v1.44.0 supersedes).

```
# v1.40.0 — 2026-08-24 — GAP-2026-08-24-STEP9-AUDIT-R1 (spec-only; no engine, gate-count,
#   schema or artefact-shape change; zero exam values). Full-line audit of v1.39.0 against
#   the routed engines, Step 7, Step 11 and PYQExplain. THREE run-breaking defects:
#   (1) S19-1 check 4 scanned the Solutions docx ITSELF for the BANNED substrings, so any
#   scoped slug or exam code containing 'state'/'answer'/'key'/'source'/'progress' (e.g.
#   TOPIC_…_SOLID_STATE_01) HARD-STOPPED every delivery — PYQExplain already excluded its
#   expected files; Step 9 now scans present − {sol}. (2) §17-3(b) told Step 9 to write a
#   PLAINTEXT key_corrections.json "which MockDeliver reads": MockDeliver has no reader
#   (it preserves the docx 'Correct Answer:' line verbatim, C17 charset only), the file is
#   banned by S19-1 checks 4 and 5, and it re-created the plaintext key the v1.37.0 hashing
#   design removed. Dropped; RESOLVED_SOURCE now lives in progress.json + §R10 with an
#   operator EX-rule prompt. (3) P3 typed mcq/msq/nat from per-subtopic section_rules only,
#   while Step 7 v5.30 / Step 11 v1.7 / audit_canonical v2.9 switch to POSITION-BASED
#   typing from marking_scheme when it declares >1 question_type — on such an exam every
#   MSQ-range question was typed mcq. P3 now applies the same mode rule.
#   DRIFT (each verified against the live engine): §13-2b named paper_pipeline.
#   canonical_structure (lives in explain_engine; 'rdkit_unavailable' path now specified);
#   MANDATE A / P1 / S0-1 allowed explain_engine.py from /mnt/project (engines are REPO-ONLY,
#   sha256-verified — fallback removed); §16-2 still asserted a live Step 10 (retired
#   v1.21.0); S7-4 claimed byte-identity with two copies that differ in docstrings (logic
#   verified identical on 19 edge inputs — reworded to logic-identical); S0-2 / MANDATE 0 /
#   P2 named the output Mock[N] where S19 uses [paper_slug]; §18-1 cited 'Step8_source' and
#   '(§13)' for the §11 degrade ledger; §6A-3 / §R3 omitted CONFORMER from the visual
#   verdicts the engine enforces; §6A-6 sent renderer preflight to 'P0' (trigger detection)
#   — now an explicit P1 sub-step with its dashboard line, plus the §7A-M line P2 lacked;
#   S19-1 gated on SELF_AUDIT_CLEAN / COVERAGE_OK that nothing set — S4-4 D now sets them;
#   §21 items 16/19/17/18 renumbered. Superseded v1.38.0 entry moved verbatim to
#   SPEC_HISTORY.md (EC-P42).
```

Entry v1.39.0 moved at framework release 2026.08.24.3 (EC-P42; v1.41.0 supersedes).

```
# v1.39.0 — 2026-08-22 — GAP-2026-08-22-STEP9-READ-SET (EC-P42; deploy follow-up #2
#   of 2026.08.21.2). New S0-3: FINAL vs NON-FINAL session class with a GENERATED
#   read set — a NON-FINAL batch session skips §20 (end-of-mock report), §22 (its
#   §R9 disclosure input) and APPENDIX A; escalation to a full read is mandatory and
#   one-way before §20 runs. §20–§24, APPENDIX A and FOOTER banners promoted from
#   '# ' to '## ' so spec_sections.py can address their spans (IDs unchanged; no
#   consumer reads header levels — verified by corpus grep). Ranges live in
#   SPEC_SECTIONS.json (has_read_set), hash-tracked, never hand-copied. The
#   MockExplain/TestExplain route is now budget-covered by design, not by headroom.
```

Entry v1.38.0 moved at framework release 2026.08.24.1 (EC-P42 discipline; v1.40.0 supersedes).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.38.0 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (MOCK-ONLY; pairs
#   MockTestCreate v5.60). New §7A-M: Step 9 re-scores every question on the shared
#   rubric (blueprint_core.assess_difficulty) at THIS exam's level and reports
#   agreement with Step 7's labels (dashboard + §R10). Report-only; sticker wins.
#   Resolves the §7A divergence note (same RUBRIC, different mechanisms; PYQExplain
#   v2.16). No shared §4–§18 rule modified; SHARED_RULES stays 1.4. Superseded
#   v1.37.0 entry moved verbatim to SPEC_HISTORY.md (EC-P42, 2026.08.20.9 discipline).
```

Entry v1.37.0 and two in-section narrations moved at framework release 2026.08.21.3
(EC-P42 route budget — MockExplain/TestExplain crossed 250,000 B; SPEC-BUDGET gate).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.37.0 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paired with
#   PYQExplain v2.15, engine v2.8, MockTestCreate v5.59, paper_pipeline v5.39,
#   final_assembly v5.55). The first v1.36.0 paper passed every §18 gate and (1)
#   PUBLISHED A WRONG KEY on a figural item (structure misread; Step 7, holding the
#   opposite key, was by design never consulted); (2) carried 24 hedged WHY WRONG /
#   PITFALL lines, nine with FALSE arithmetic — §15-2's "a real path always exists"
#   forced invention; (3) 0 NARROWED over 60 AXIOMs while the loaded library named
#   the overgeneralised families; (4) every prose formula ASCII. ROOT CAUSE: gates
#   proved a protocol was DECLARED, not DONE. FIXES: §7-8 KEY RECONCILIATION (hash
#   commitments, resolved IN-RUN); §13-2b SEMANTIC-OBJECT RECONCILIATION; §15-2
#   REWRITTEN (two modes, engine RECOMPUTES, hedges banned, no quota); §7-7 step 3
#   MECHANICAL (Triggers + tripwire); §8-0c TYPOGRAPHY; §6A-1b-ii; §17 REWRITTEN
#   (never halt); RE-1/13/16 amended, RE-23/24 new; §18/§20/§21/§24 hooks.
#   SHARED_RULES 1.3→1.4.
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockTestExplain.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14, and again at 2026.08.19.1 (v1.25.0–v1.34.0 — the
#   MockExplain/TestExplain route had crossed the EC-P42 SPEC-BUDGET threshold)
#   (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.```

In-section narration moved from §24 (operational summary retained in-spec):

```
#   v1.21.0 — THE AUTOMATIC PRODUCER IS GONE. Step 10 was this loop's producer: it distilled
#   the defects it had to FIX into reusable AL-rules so the same mistake was not authored
#   again. With Step 10 retired, NOTHING generates AL-rules automatically any more. This
#   section remains as the CONSUMER half only: any AL-rule file already accumulated stays
#   valid and is still loaded and obeyed, and new rules may be added BY HAND by the author.
#   The schema below is frozen so existing files keep parsing; there is no producer half to
#   keep pinned to it.
#
```

In-section narration moved from the Appendix (operational facts retained in-spec):

```
#   WHY THE LISTING WAS REMOVED (v1.12): through v1.11 the full engine was reproduced
#   verbatim in this Appendix AND in the (now retired) ExplainAudit spec's Appendix A "for
#   self-containment" — but a reproduced copy and the standalone can silently DESYNC, and
#   the v1.8/v1.9 changelog records that this ALREADY happened once (the embedded copy
#   lagged the standalone's step-number + code fixes). A single canonical copy removes
#   that failure mode — the same multi-copy-drift fix the retired audit steps applied
#   to their auditors. The framework linter (validate_framework_md.py) runs
#   explain_engine.py's `--self-test` directly.
#
```


# v1.36.0 — 2026-08-20 — GAP-2026-08-20-TRANSFER-SAFE-EXPLANATIONS (paired with
#   PYQExplain v2.14, engine v2.7). A DELIVERED 60-question paper passed every §18
#   gate with every answer correct and still carried ~17 sentences TRUE FOR THE ITEM,
#   FALSE FOR ITS NEAREST NEIGHBOUR ("electron-withdrawing → meta" vs halogens; "one
#   carbon richer"; "stable carbonylate = 18e"; "always a meso form"; "cannot … at
#   all"), plus "The seductive half is …" on 10/10 MSQ blocks — mandated by §15-3's
#   own wording. Answer-level gates are blind to this. ROOT CAUSE as in v1.35.0:
#   §8-0b / §14-3b / §8-2 ADVISED what only a gate enforces; §6A tested PRESENCE, not
#   ALIGNMENT. FIXES (domain-neutral): NEW §7-7 TRANSFER-SAFETY PROTOCOL (scope →
#   type → neighbour test → repair by MECHANISM → recorded transfer_record); §8-2
#   epistemic type; §8-3 minimum components (subject data); §8-0b a GATE (kept
#   absolutes declared; plain quantifiers NOT gated — 80% false positives measured);
#   §14-1 three-part + §14-5 four fields; §15-3 MSQ rewritten, old wording WITHDRAWN,
#   psychology phrases engine-banned; NEW §6A-1c ALIGNMENT, §6A-3b tripwire,
#   CONFORMER (F3); §24 SUBJECT-level learnings file + §24-5 codes; §5/§18/§R3/§21
#   hooks; engine fixes F2. SHARED_RULES 1.2→1.3. Student format LOCKED.

Moved from the file header at framework release 2026.08.15.14; entries
v1.25.0–v1.34.0 moved VERBATIM at framework release 2026.08.19.1, and
v1.35.0 at framework release 2026.08.20.9 (both times the
MockExplain/TestExplain route had reached the EC-P42 SPEC-BUDGET
threshold — 287 B of headroom remained at the second move).
Current-version entry remains in Framework_MockTestExplain.md.

```
# v1.35.0 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-EXECUTION-INTEGRITY (paired with
#   PYQExplain v2.13, engine v2.6). Four defects, one root cause, found by auditing a
#   DELIVERED 60-question paper: each traced to a rule that ADVISED what only a gate
#   can enforce — prompt policy treated as enforcement.
#   D1 — INTERNAL ERROR-TAXONOMY TOKENS RENDERED TO STUDENTS. Every WHY WRONG entry in
#   the reference paper opened with the raw snake_case token ('regiochemistry_error:
#   the para phenol ...'; 40 option entries + 20 NAT pitfalls). CAUSE: §9/§15-2 asked
#   the first line to "name an error type" and nothing separated the internal name
#   from the rendered sentence — the §9 taxonomy is itself snake_case, so obeying the
#   rule literally printed machine metadata into a learner document. FIX: the §9
#   diagnosis is METADATA — still mandatory, recorded per wrong option/pitfall in
#   progress state — and the visible line states the same content in natural language.
#   Engine v2.6 raises at write time on any taxonomy token in student-facing text AND
#   re-scans the rendered bytes at verify time, so the leak cannot ship by either path.
#   D2 — ROUTING WITHOUT EMISSION. The same paper carried 46 question-region images
#   and TWO explanation figures, on a structure-heavy paper whose section_rules
#   declared renderers; structure-decisive DEDUCTIONs ended at "the structure drawn in
#   Option N". The §6A router classified and the renderer shipped prose — the defect
#   §6A exists to remove, standing because verdict and emission were never tied
#   together. FIX: NEW §6A-1b (structure-answer presumption: when the verified answer
#   IS a structure, STRUCTURE_GRAPH is presumed and PROSE requires a recorded
#   justification naming where the prose carries each decisive feature); §6A-3 now
#   passes the verdict INTO the block and engine v2.6 enforces coherence — a visual
#   verdict with zero figures raises at construction; a §6A-4 degrade records the
#   DEGRADED requirement, never the original.
#   D3 — SPEED HACK ON 56 OF 60. §14's omit-by-default held per question and nothing
#   measured the AGGREGATE, so inclusion pressure won 93% of the paper, several
#   "hacks" restating the DEDUCTION (a §14-1 part-1 failure each). FIX: NEW §14-5 —
#   eligibility recorded per question (distinct/faster/scoped), the inclusion RATE
#   reported in §R3, and a batch at 100% inclusion re-runs the §14-1 test per question
#   before §18. A TRIPWIRE, never a quota: a genuinely shortcut-rich batch survives
#   its re-audit unchanged.
#   D4 — TWO REASONING DISCIPLINES WITH NO RULE. (a) A correct final answer can carry
#   mutually incompatible intermediate claims — derive-twice compares ANSWERS, §7-5
#   audits the final VALUE, neither reads the reasoning: NEW §7-6 decisive-claim
#   consistency — an explanation whose claims cannot all be true is invalid even when
#   the answer matches; repair returns to §7-1, never to patched prose. (b) Counting
#   questions were OPENED from a closed-form ceiling before the elements it assumes
#   independent were inventoried: NEW §7-0c enumeration-before-formula. Both stated
#   domain-neutrally per the v1.33.0 convention; the incident's domain appears only as
#   a labelled illustration. RE-6d added; RE-13 restated (diagnosis internal, rendered
#   naturally); §5-1/§5-2/§5-3, §18, §R3 and §21 carry the matching hooks.
#   ALSO (engine v2.6, found while writing its fixtures): the v2.3 figure-validation
#   loop sat AFTER the NAT branch's return, so a NAT block's figures were NEVER
#   validated at construction — moved above the type split (NAT-FIG-VALIDATED locks
#   it); an anomaly block now rejects figures as student content; an AXIOM naming an
#   option label raises (§8-2 — binding is the DEDUCTION's job).
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the .docx produced by Step 7 and the frozen registry.json,
#   INDEPENDENTLY DERIVE the answer to every Question, and INTERLEAVE a perfect,
#   highest-standard explanation after each question — without altering one byte of
#   the paper. Emit [ExamCode]_Mock[N]_Explanation.docx: a 100%-explained, zero-defect
#   learner-facing solution document, plus an author handoff report.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION
# ════════════════════════════════════════════════════════════════════════
#   Step 5 (PYQExtract)   → [ExamCode]_section_rules.md + _subtopic_manifest.json
#   Step 6 (MockBlueprint) → [ExamCode]_blueprint.json + _registry.json (template)
#   Step 7 (MockCreate)    → [ExamCode]_Mock[N]_Create.docx
#                                  [ExamCode]_registry.json (written at Final Assembly —
#                                  FROZEN for every step after Step 7)
#   THIS STEP — Step 9 (MockExplain) → [ExamCode]_Mock[N]_Explanation.docx (interleaved explanations)
#   C3 (v1.15): in every [ExamCode]_Mock[N]_*.docx name above, "Mock[N]" is the paper_slug of the
#   paper being processed — "Mock[N]" for a mock (byte-identical), else the scoped paper_id with
#   ":"→"_" (e.g. SUBJ_Physics_03), derived from blueprint.mocks[N].paper_id (fallback MOCK:M{N:02d}).
#   Read the input under, and write the output under, that same paper_slug. No registry writes here.
#   Step 11 (MockDeliver)
#
#   Steps 5–11 all run in the [ExamCode] project (exam-specific). Step 9 runs directly
#   after Step 7 and directly before Step 11. There is no audit step on either side:
#   nothing re-derives these answers after this step, so §12 and §19 are terminal.
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. It names no section, no subtopic,
#   no question count, no time/marks figure, no option count, no section family, no
#   language, no figural type, no block label. Every such value is READ at runtime:
#     • question/section counts, q_ranges, options-count, difficulty schedule
#       → blueprint.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets, OMML_required,
#       option label format, language, block labels/markers, figural object/transformation
#       types, escape tokens, passage word ranges
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, mandatory-every-mock list, alternation groups
#       → subtopic_manifest.json
#     • per-mock figural_manifests[] + rc_manifests[] (cross-checks only, never keys)
#       → registry.json
#   SCOPE — what "exam-independent" means here, stated precisely (no over-claim):
#   Step 9 explains OBJECTIVE papers and supports, per question, all three objective
#   answer formats found across these exams:
#     • MCQ — single correct option (the common case; e.g. SSC, IBPS, NEET, CLAT).
#     • MSQ — multiple correct options, scored as a set (e.g. GATE multi-select).
#     • NAT — numerical-answer-type with NO options, optionally with a tolerance
#       range (e.g. GATE / JEE numerical-input questions).
#   It also handles, from config (never hardcoded): per-SECTION option counts (a paper
#   that is 4-option in one section and 5-option in another), alphabetic / roman /
#   custom option labels (A·B·C·D, i·ii·iii, …) as well as numeric, and language-
#   specific sentence terminators (e.g. the Devanagari danda '।'). With valid
#   upstream outputs (Steps 5–7) it therefore covers SSC CGL, GATE (incl. NAT/MSQ), NEET, IBPS,
#   UPSC CSAT, CAT and regional/other-language exams. OUT OF SCOPE by nature: purely
#   DESCRIPTIVE / essay papers (e.g. UPSC Mains), which have no options and no single
#   keyed answer — the objective block model does not apply (see §22). If a value an
#   explanation needs is absent from the source files, the engine falls back to a
#   STRUCTURAL default (English labels, numeric scheme, Latin terminators, the uniform
#   option count) and logs it — it is NEVER hardcoded as an exam fact.
#
# v1.34.0 — 2026-08-19 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT (paired with
#   PYQExplain v2.12, engine v2.5). SPEC-ONLY here; the paired ENGINE release fixes a
#   separate, unrelated label defect found the same way (see explain_engine v2.5).
#   THE DEFECT. section_rules declares `option_label_format` in TWO places — the
#   CATEGORY C header and every per-SECTION block — and P5 compared NEITHER. It checked
#   option COUNT, question TYPE and Q_TOTAL, and it checked opt_re against label_scheme,
#   but the declared label FORMAT was never compared against itself. A real exam config
#   was found carrying `(A)/(B)/(C)/(D)` in the header and `1/2/3/4` in all FOUR of its
#   section blocks. The run did not halt. It silently took the header, and every option
#   in the paper was printed with the wrong label.
#   WHY IT IS SILENT AND TOTAL. The two values come from DIFFERENT generators: the header
#   is written from OBSERVED PYQ papers, the per-section values from per-section
#   synthesis. Re-running the PYQ analysis can change the header alone and leave every
#   section untouched. Nothing else in the run looks wrong — counts match, types match,
#   the paper renders cleanly — so there is no second symptom to notice.
#   THE FIX. P5 now compares the header against EVERY section and the sections against
#   each other, and HALTs on any disagreement, printing every declared value with its
#   location. Resolution by precedence is explicitly forbidden: "Surface, do not guess"
#   already governed this step and the missing comparison was the only reason it could.
#   SCOPE, NOT OVERCLAIMED. Labels are PRINTED by the generation step; this step reads
#   them. Halting here cannot un-print an already-generated paper — it stops an
#   explanation run from cementing wrong labels and sends the author to fix the config
#   and regenerate. The same comparison belongs upstream in generation; that this one is
#   downstream is a reason to surface loudly, never a reason to resolve silently.
# v1.33.0 — 2026-08-19 — GAP-2026-08-19-DOMAIN-LEAK-IN-UNIVERSAL-RULES (paired with
#   PYQExplain v2.11). SPEC-ONLY, no engine change, NO rule weakened — every obligation
#   added in v1.31.0/v1.32.0 still binds. What changes is that four of them were written
#   in ONE domain's vocabulary while sitting in an EXAM-AGNOSTIC spec that serves every
#   exam in the corpus.
#   THE DEFECT. §7-0a listed conditions as "solvent · pH · catalyst · ligand · WORK-UP";
#   §7-0b listed assumptions as "ideal-gas · activity ~ concentration · spin-only";
#   §7-5 made "temperature in KELVIN" and "STOICHIOMETRY — the mole ratio comes from the
#   BALANCED relation" MANDATORY checks; §8-0a banned "bond angles, spectral positions,
#   industrial temperatures". Read by an aptitude, language or reasoning paper, those are
#   not merely irrelevant — §7-5 in particular demanded checks that CANNOT be satisfied or
#   even understood, so a conformant paper in another domain could not pass its own
#   checklist. That breaches the EXAM-AGNOSTIC GUARANTEE at the top of this file.
#   THE FIX, following the convention the corpus already uses elsewhere ("config triggers;
#   default NOT/EXCEPT/INCORRECT/FALSE"): the RULE is stated in domain-neutral terms, the
#   LIST is marked ILLUSTRATIVE and read from the exam's own material, and every §7-5
#   check is explicitly CONDITIONAL ON APPLICABILITY — a check whose subject the question
#   does not contain is NOT APPLICABLE and is NOT a failure. Domain examples are retained
#   deliberately, because a rule with no worked instance is hard to apply, but each is now
#   labelled as one domain illustrating a universal shape.
#   WHY IT HAPPENED, recorded so it is not repeated: these four rules were written from a
#   chemistry incident, and the incident's vocabulary travelled into the rule. Every
#   earlier release in this series was audited for exam-independence by absence of exam
#   NAMES and counts — a test that these passed, because a domain leak carries neither.
# v1.32.0 — 2026-08-19 — GAP-2026-08-19-CONDITIONAL-CORRECTNESS (paired with PYQExplain
#   v2.10). SPEC-ONLY, no engine change. Four rules covering the same underlying failure:
#   an answer that is RIGHT IN GENERAL and WRONG HERE, because a condition, an
#   assumption, a unit or a scope was never made explicit. Derive-twice does not catch
#   this class — both routes can share the same silent premise.
#   D1 — §7-0a CONDITION CAPTURE. Nothing required the SOLVER to read back the conditions
#   a remembered result depends on. §9's `wrong_condition` names this failure in a
#   DISTRACTOR only, which is a different obligation — the same error-type-standing-in-
#   for-a-rule confusion that let two defects survive an earlier audit. Reference case:
#   ozonolysis, where the WORK-UP alone decides between an aldehyde and a carboxylic acid.
#   D2 — §7-0b ASSUMPTION LEDGER. Ideal gas, activity ~ concentration, small-x, spin-only,
#   298 K, standard state. Three cases; only an assumption that MATERIALLY changes the
#   answer reaches the reader, and it may never contradict the stem.
#   D3 — §7-5 NUMERICAL VERIFICATION. Derive-twice catches a DIFFERENT-answer error, never
#   a CONSISTENT one: both routes can share one unit slip, one log base, one power of ten.
#   Seven orthogonal checks — units, conversions/kelvin, magnitude, log base, sign,
#   stoichiometry, precision — run on the final value. A failure returns to §7-1, never to
#   a patched number.
#   D4 — §14-3b SHORTCUT VALIDITY DOMAIN. §14 tested whether a shortcut was DISTINCT and
#   FASTER, never whether it was SCOPED. A SPEED HACK is the line a student memorises, so
#   an unscoped one is the most damaging sentence in the block. Distinct from §8-0b:
#   "a bulky base usually gives the less substituted alkene" is calibrated (passes §8-0b)
#   and still unscoped (fails §14-3b) because it never says WHEN to reach for it.
# v1.31.0 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-CONTENT-DISCIPLINE (paired with
#   PYQExplain v2.9, engine v2.4). Three defects that were IDENTIFIED at the start of
#   this work, survived every release since, and were nearly closed out unfixed: an
#   internal audit reported them CLOSED on loose keyword matches that hit adjacent
#   text. A test that can only pass is not a test.
#   D1 — NO RULE AGAINST INVENTED PRECISION. A delivered explanation asserted a major
#   product forms "in about 70 percent yield" — a figure the stem never supplied, the
#   syllabus never fixes, and no step derived. Nothing in this spec forbade it. The
#   earlier audit passed this on §9's `overgeneralised_rule`, which is a DISTRACTOR
#   error type describing how a wrong OPTION fails — it says nothing about what the
#   explanation itself may assert. NEW §8-0a: every number traces to the stem, a
#   syllabus constant, or a shown derivation; nothing else may be written.
#   D2 — NO RULE AGAINST ABSOLUTE LANGUAGE. The same explanation said a bulky base
#   "cannot approach" the hindered hydrogens. It demonstrably can; it is disfavoured,
#   and the question turns entirely on the competition between two ACCESSIBLE
#   pathways — so the absolute destroyed the reasoning being taught. Zero rules
#   existed. NEW §8-0b: absolutes are reserved for claims absolute in the subject's
#   own terms; tendencies take calibrated language.
#   D3 — THE ARTEFACT DID NOT DECLARE ITS OWN STATE. Coverage was announced only in
#   the chat progress line (§S19-3), so the FILE said nothing. A legitimate mid-run
#   Batch-1 artefact carrying 10 of 60 explanations is byte-indistinguishable from a
#   finished paper once it leaves the conversation — and in the reference incident it
#   was reviewed as finished, the review's central complaint being the 50 questions
#   the batch had not yet reached. NEW §12-4 + engine v2.4 set_coverage_banner().
#   ENGINE SUPPORT WAS REQUIRED FOR D3, AND THAT WAS VERIFIED BEFORE THE RULE WAS
#   WRITTEN: with a banner present, verify_fidelity still PASSES (it sits outside
#   every question region) but strip_solutions leaves it, so the questions-only copy
#   diverges from the Step-7 source and the §12-3 re-audit FAILS. Engine v2.4 strips
#   it; five self-tests lock presence, gate-neutrality, stripping, idempotence and
#   removal (83/83).
# v1.30.0 — 2026-08-19 — GAP-2026-08-19-STALE-PIN-SWEEP (paired with PYQExplain v2.8).
#   SPEC-ONLY, no engine change. A CLASS SWEEP, not four incidents: v1.29.0 de-pinned
#   the §R1 report line and stopped, leaving the SAME defect standing in every other
#   place a count was written into prose. GAP-2026-08-13-STALE-SELFTEST-PIN fixed the
#   P1 gate in v1.25.0 and left the class standing too — this is the third time this
#   shape has been fixed instance-by-instance, so it is fixed by RULE here (§21-0).
#   D1 — §21 DEFINITION OF DONE HARD-PINNED THE ENGINE COUNT. Item 1 read "engine
#   --self-test 62/62" under a heading that says "ANY violation = do NOT deliver". The
#   engine prints 78/78. On a literal reading the Definition of Done could NEVER be
#   satisfied — the exact failure mode of GAP-2026-08-13-STALE-SELFTEST-PIN, in the one
#   place that fix never reached. Converted to floor form.
#   D2 — THE P2 DASHBOARD TEMPLATE PRESCRIBED PRINTING "[62/62 PASS]". A template is
#   an instruction: it told every session to print a count that has been wrong since the
#   engine grew past 62 fixtures. Now prints what the engine actually reported.
#   D3 — THE P2 DASHBOARD HEADER SAID "MockExplain v1.20" at spec v1.29.0. Now reads
#   the version from this file's own header.
#   D4 — STALE FACTUAL COUNT. P1's explanatory note asserted "it prints 64/64 today";
#   it prints 78/78. Any such assertion is stale the moment a fixture is added, so the
#   count is removed rather than corrected.
#   NEW §21-0 states the rule the three previous fixes each implied but never wrote
#   down, so the next fixture addition cannot reopen this.
# v1.29.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-FIGURAL-DOMAIN-BLINDNESS. SPEC-ONLY:
#   no engine change, no artefact-shape change. Four defects found by auditing what
#   v1.27.0/v1.28.0 did NOT touch. The router fixed what an explanation EMITS; these
#   fix how a question is READ and how the run REPORTS itself.
#   D1 — §13 SPOKE ONLY REASONING-PUZZLE. S13-1/S13-4 named "mirror/water image, paper
#   folding, cube net, space orientation" and defined the figural AXIOM as "the visual
#   rule (rotation / reflection / element add-remove / count / net-folding)". That is the
#   SSC/CAT non-verbal vocabulary. It is CORRECT for those exams and USELESS for a drawn
#   molecular structure, an MO diagram or a titration curve: a session reading §13 for a
#   chemistry stem was told to look for rotation and folding. §13 is now split into a
#   SHARED gate (detect/extract/view — unchanged, it was always domain-neutral) and TWO
#   named FAMILIES, transformation-puzzle and scientific-diagram, with the reading
#   protocol each actually needs. No exam loses anything: the puzzle family is the old
#   text preserved verbatim in substance.
#   D2 — §6 HAD NO CLASS FOR STRUCTURAL OR DERIVATIONAL REASONING. S6-1 classed by
#   exam shape (vocab / grammar / formal-logic / figural) so a Claisen rearrangement
#   landed in C-FIGURAL and a multi-step derivation in C-COMPUTATIONAL. Class decides
#   which SECTION LEADS — a different job from §6A, which decides what is EMITTED — so
#   the gap was not covered by the router. C-STRUCTURAL and C-DERIVATIONAL added.
#   D3 — §6A-3 PROMISED A REPORT LINE §20 DID NOT DEFINE. §6A-3 states "The §20 report
#   states the distribution" while §R3 listed no such field: a dangling cross-reference
#   that would be satisfied by nobody. §R3 now carries the representation distribution
#   and the degrade ledger.
#   D4 — §R1 PROVENANCE WAS STALE. It printed "spec v1.13 · engine 62/62" against a
#   spec at v1.28.0 and an engine at 78/78. NOT a halt risk — the GATES were converted
#   to FLOOR form in v1.25.0 (GAP-2026-08-13-STALE-SELFTEST-PIN) and remain floor-form
#   here — but a provenance line that misreports its own versions defeats the purpose of
#   provenance. §R1 now reads both values from what actually ran, pinning neither.
# v1.28.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-REPRESENTATION-EMISSION (figures LIVE).
#   MINOR bump, paired with explain_engine v2.3. v1.27.0 shipped the §6A router
#   RECORD-ONLY, deliberately: verdicts first, emission after review. This release
#   turns emission ON. What lands:
#   1. ExplanationBlock gains `figures` (list[RepresentationFigure]); each figure
#      carries the §6A-5 validation record and FAILS AT CONSTRUCTION on any breach
#      (no record, match False, inconsistent identifiers, missing file, width
#      outside 0.5..7.0 in). A figure is proved, not trusted.
#   2. Render path: figures interleave with DEDUCTION sentences at their
#      after_step position as CENTRED, TEXT-FREE picture paragraphs. The no-text
#      invariant is load-bearing: the strict reader keeps an explanation
#      paragraph only when it has display text or math source, so figure
#      paragraphs are INVISIBLE to parse_solution_blocks and the round-trip is
#      unchanged by design (self-test FIG-READER-INVISIBLE). There is NO caption
#      paragraph — the surrounding DEDUCTION prose describes the figure (§6A-1
#      already requires the prose to be readable without it).
#   3. verify_explanations gains the FIGURE-LANDING check: a block that declares
#      N figures must render EXACTLY N drawing paragraphs in its explanation
#      region. A silent skip (e.g. a legacy caller without doc_part) is a
#      BLOCKING FAIL — §6A-4's degrade-LOUDLY rule applied to the render path
#      itself (self-test FIG-SILENT-SKIP-CAUGHT).
#   4. verify_fidelity needs NO change and gets none: question-region signatures
#      exclude the explanation region, source-media MD5s are one-directional, and
#      new image parts register real rIds so the dangling-rId check (A3) passes.
#      Locked by FIG-E2E-GATES on a figural sample paper (stem images present),
#      proving stem drawings and explanation drawings are never conflated.
#   5. §6A-6 (NEW) defines the renderer execution contract: renderers are
#      declared per-exam in section_rules CATEGORY C, executed by the session at
#      solve time, and every artefact ships with its validation record. No new
#      engine file, no routes.json change: rendering is session-executed spec
#      work (the Step-7 figural precedent), and t3_mathcomp.py stays untouched.
# v1.27.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-MATH-NOTATION + REPRESENTATION ROUTER.
#   MINOR bump: §11 grammar is DOCUMENTED and §9 gains scientific error types; no
#   existing artefact shape changes. TWO defects, one root cause.
#   D1 — §11 BANNED THE SYNTAX ITS OWN COMPILER REQUIRES. S11-1 listed "\\frac",
#   "\\sqrt" and "$…$" as banned LaTeX while t3_compile handles \\frac{}{},
#   \\sqrt{}, K_{sp}, E_{cell}^{0} and \\Delta_{o} CORRECTLY, and S18 recorded the
#   consequence in its own words: "bans LaTeX in prose (§11), so ⟦MATH:⟧ regions
#   are rare here". An executing session therefore read §11, concluded that math
#   notation was forbidden, and VERBALISED arithmetic instead — measured on a
#   60-question chemistry paper: 105 verbalised phrases ("divided by" x18,
#   "square root of" x9, "raised to the power" x3) against 6 OMML nodes in the
#   whole document, every one of them in the two pure-mathematics questions and
#   NONE in any science question. The prose-only texture was the spec working as
#   written, not a generation failure. S11-1 now documents the grammar that
#   actually compiles and confines the LaTeX ban to PROSE, where it belongs.
#   D2 — THE COMPILER VALIDATES GRAMMAR, NEVER NOTATION. guard_sentence exempts
#   ⟦MATH:⟧ bodies from every prose guard on the stated grounds that the compiler
#   checks them. It does not: a bare _ / ^ binds exactly ONE preceding character
#   and unknown words pass through as literal text, so Delta_o rendered "Delt aₒ",
#   K_sp rendered "Kₛp" and sqrt(x) rendered as flat text — SILENTLY, with every
#   gate green. explain_engine v2.2 adds t3_notation_guard (authoring-time, fail-
#   at-construction, remedy named in the message) and the self-test locks it in
#   BOTH directions. t3_mathcomp.py is deliberately NOT touched — it is byte-
#   locked to Framework_PYQPrepare §S3-5b by the self-test drift lock.
#   D3 — REPRESENTATION SELECTION WAS NOT A PIPELINE STAGE. §6 classed questions
#   by exam-shape (vocab/grammar/formal-logic) with no class for structural or
#   derivational reasoning, and ExplanationBlock has no field able to carry a
#   figure, so a structural explanation could only DESCRIBE what a scheme would
#   show. New §6A REPRESENTATION ROUTER makes the choice explicit and — critically
#   — makes PROSE the default that visuals must EARN, on the proven §14 SPEED HACK
#   "omit, never fake" pattern. Emission is staged for the engine work; the router
#   verdict is recorded and reported from this version.
# v1.26.0 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: a name is added to this file's executable surface. NO ARTEFACT CHANGES.
#   This spec CALLED present_files() from compiling python while DEFINING it nowhere —
#   a guaranteed NameError the moment that path executes as python. Five such call
#   sites stood across four specs; spec_name_audit_baseline.json had accepted
#   `present_files` as a known-unbound name in all four, which is why the ratchet
#   reported OK for weeks. SAME SHAPE as D2 of
#   GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed the instance and left the
#   class standing. FIX: a CLASS: T stub is declared in this file, matching the
#   corpus's per-file house pattern for CLASS T markers.
# v1.25.0 — 2026-08-13 — SYNC AUDIT ROUND 2 (fresh-lens re-audit of Steps 5→11)
#   1. GAP-2026-08-13-STALE-SELFTEST-PIN (HALT-class). P1 pinned the engine gate at the
#      literal "SELF-TEST: 62/62 PASS" (3 sites; + "10/10" for --self-test-audit, 2 sites)
#      while explain_engine.py actually prints 64/64 (26/26 audit) — so EVERY Explain
#      session following P1 literally HALTed on a healthy engine. All 5 sites converted to
#      the FLOOR form ("N/N PASS with N >= 62 / >= 10"), the same AUTH_GATE_FLOOR pattern
#      Steps 6/7 already use — integrity is bootstrap.py's sha256 job, not a count pin's.
#   2. GAP-2026-08-13-P10-SCOPED-BLUEPRINT (behavioral). P10 loaded the hardcoded
#      f'{EXAM}_blueprint.json' (the MOCK blueprint) though P1 selects among ALL
#      {EXAM}*_blueprint.json by the uploaded docx's slug — so for a SCOPED paper the
#      v1.24 P10/0 gate compared the scoped docx against the mock blueprint (unconditional
#      false HARD STOP), or crashed if no mock blueprint existed: the gate could never
#      pass for the resumed-scoped papers it was written about. P10 now selects the
#      blueprint containing the paper whose slug matches PAPER_SLUG (P1's own semantics,
#      restated self-contained), and every downstream P10 check (FK, count, difficulty)
#      now validates against the CORRECT blueprint for scoped papers too.
# v1.24.0 — 2026-08-13 — CROSS-STEP SYNC AUDIT FIXES (Steps 5→11 handshake audit)
#   Two desyncs found by a dedicated 3-pass producer↔consumer audit of the whole
#   Step 5 → TestDeliver chain, both fixed in this file:
#   1. GAP-2026-08-13-STALE-CREATE-COMPLETE-NAME — S2-1's trigger contract (FRESH
#      prerequisite line + the HALT rule) still demanded a "Create_Complete" docx,
#      a filename RETIRED at v1.21.0 that no step produces (this file's own header
#      says so; Step 7 delivers [ExamCode]_[paper_slug]_Create.docx). Read literally,
#      the HALT rule could never be satisfied — a session would refuse the valid
#      _Create.docx upload forever. Both sites (and the S19-1 comment) now name
#      _Create.docx. The operative P1 discovery always did.
#   2. GAP-2026-08-13-EXPLAIN-N-SLUG-GATE — new P10/0: trigger-N ↔ uploaded-docx
#      identity gate, the SAME assertion Step 11 (MockDeliver S1-2) already makes
#      and Step 9 did NOT. P1 selects the BLUEPRINT by the uploaded docx's slug, but
#      N comes from the trigger — and on a RESUMED SCOPED SERIES the blueprint's
#      `mock` field is an ORDINAL (1..count) while the paper_id carries the OFFSET
#      series number (ScopedBlueprint S2-4 paper_start), so a mistyped P[N] could
#      silently bind a DIFFERENT paper's options_by_q/question_index to the uploaded
#      paper and publish a mislabeled Explanation. P10/0 hard-stops on
#      pp.paper_slug(trigger-N's paper_id) != the uploaded filename's slug.
# v1.23 — 2026-08-10 — P10 REGISTRY-FK TRIPWIRE (GAP-2026-08-10-QINDEX-FK-
#   ENFORCEMENT). New mandatory preflight P10: before ANY solving, validate this
#   mock's registry.question_index against the blueprint (entry exists; count/
#   coverage; every subtopic_id byte-exact in subtopic_list; every difficulty in
#   difficulty_labels) AND check the registry's ledger↔index agreement. WHY HERE:
#   three reference Step-7 sessions committed invented subtopic_ids that only
#   detonated at Step 11's JOIN — after the full Explain effort had been spent —
#   and one paper's question_index was silently LOST by a later registry write
#   while the completion ledger still claimed it done. P10 catches both classes
#   BEFORE Explain effort is spent: a defective index for THIS mock is a HARD
#   STOP with per-Q findings (remedy: fix at Step 7 / patch the registry
#   upstream, never inside Step 9); ledger gaps for OTHER papers are a loud WARN
#   (they do not block this mock, but must be surfaced the first time any step
#   sees them, not at those papers' deliveries). Companion to MockTestCreate
#   v5.48.0 (S13-4 copy-by-reference + A-QINDEX) and MockDeliver v1.12.0.
# v1.22 — 2026-08-10 — SHARED-ENGINE MATH-INTEGRITY GATE (GAP-2026-08-10-EXPLAIN-
#   MATH-DEGRADE-SILENT, mirrored from Framework_PYQExplain v2.4). The shared
#   explain_engine.py now compiles every ⟦MATH:…⟧ region inside ExplanationBlock.
#   validate() and RAISES at construction on a Tier-3 grammar reject, so a region
#   can no longer degrade to raw plain text at render. Because verify_explanations
#   REPORTS such degrades through its RETURN value (ok, problems) — it does NOT
#   raise — §18-1's verify_explanations line is now an explicit BLOCKING CONTRACT
#   (assert ok is True AND problems == [] AND T3_STATS['failed'] empty). This
#   pipeline authors math with the explicit helpers and bans LaTeX in prose (§11),
#   so ⟦MATH:…⟧ regions are rare here, but the shared-engine gate and the §18
#   contract apply. Engine self-test unchanged (62/62). Touched: §S5-2, §S18-1,
#   header + END sentinel. Ships with the regenerated MANIFEST (engine sha changed).
# v1.21.1 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED and explain_audit_gate.py
#   REMOVED from the framework. Updated the two notes that said the gate module still
#   survives / is still routed "for PYQExplainAudit" (no longer true). No rule change.
# v1.21.0 — 2026-08-03 — AUDIT STEPS REMOVED (Steps 8 and 10 retired framework-wide).
#   Step 9 now reads the Step-7 paper directly ([ExamCode]_Mock[N]_Create.docx) — the
#   rectified _Create_Complete.docx no longer exists because no step produces it. Every
#   claim of upstream certification, every escalation target, and every "Step 10 proves
#   truth" clause is restated against what actually survives: Step 7's own gates upstream,
#   and this step's §12 fidelity verification + §19 pre-delivery checklist downstream.
#   ACCEPTED LOSS, stated once and not hidden: no independent re-derivation of any answer
#   and no independent completion gate exist after this step. Step 9's self-checks are now
#   TERMINAL for explanation correctness. The §24 learnings loop loses its producer and is
#   demoted to an optional, manually-authored input.
#
# v1.20.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   401 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestExplain'. The current companion block, the
#   v1.20 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v1.20 — 2026-07-20 — FINAL QA FIX: EXAM_CODE CROSS-VALIDATION (twin of Framework_
#   MockTestCreate v5.29, found during the same full line-by-line adversarial re-audit).
#   P1's [ExamCode]*_blueprint.json glob is a PREFIX match — added an explicit
#   bp['exam_code'] == [ExamCode] check immediately after pp.pick_blueprint returns,
#   HALTING on mismatch instead of silently trusting the glob.
#
```

## Framework_NotesAudit.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesAudit.md.

```
# v3.4.2 — 2026-08-14 — ADVERSARIAL-REVIEW FIXES (independent fresh-eyes
#   review + 400-trial property fuzz of the integration feature; pairs with
#   notes_core v2.9, notes_audit v2.6, Framework_NotesCreate v2.6.2,
#   Framework_NotesBlueprint v3.1.1). Five fixes on this side:
#     (1) §5 G-11 still said "ALL of the unit's bank questions" — the exact
#         pre-v3.4.1 boundary v3.4.1 replaced; the terminal re-solve runs
#         over the §2 CERTIFICATION SET (the same count-drift class as the
#         MockTestAnalyse PART-B miss, caught one release later this time).
#     (2) FILING MOVES ONLY ON FULLY-RESOLVED EVIDENCE (notes_core v2.9): a
#         fused question moves off its header only when EVERY fusion-set
#         member is a registry unit in the order map. An out-of-syllabus
#         header's question can no longer leak INTO a certifiable unit's
#         set, and a typo'd partner no longer under-files — the question
#         stays at its header and the defect is REPORTED.
#     (3) §5 G-13: UNRESOLVED evidence is ADVISORY (never a Combines demand
#         naming an unresolvable subtopic); the Combines match now uses
#         notes_core.display_norm — the subtopic_key component norm — so
#         & / and / dash / NFKC drift between paper-header bytes and
#         manifest names cannot produce a false blocking finding; the
#         containment-residual ("Waves" inside "Matter Waves") is STATED,
#         with the §2 inbound solve as the semantic net.
#     (4) §2: DEFERRED disclosure gains the ORPHANED-FILING check — when the
#         manifest is present, a deferred question whose filing unit's sid
#         has left the manifest is disclosed as certification-pending, never
#         silently dropped from the exam's coverage.
#     (5) §9 chat line: unresolved-evidence and orphaned-filing disclosures.
# v3.4.1 — 2026-08-14 — THE AUDIT BOUNDARY FOLLOWS FILING (line-by-line
#   certification sweep of the v3.4.0 feature; pairs with notes_core v2.8,
#   Framework_NotesCreate v2.6.1). Found by tracing ONE fused question
#   through NB -> NC -> NA: v3.4.0 filed the fused question's TEACHING at
#   the latest partner (G-13) but §2's closed-book solve still read the
#   HEADER slice — so the EARLIER unit was asked to solve a question whose
#   ingredients its own notes must not teach (backward-only, NC I-4): a
#   guaranteed PARTIAL/NOT with no licensed remedy, looping toward a
#   quarantine the question does not deserve. Meanwhile the FILING unit —
#   whose integration section exists exactly to make that question solvable
#   — never solved it closed-book at all: the certification instrument
#   missed the very questions the feature exists for. §2 now audits the
#   unit's CERTIFICATION SET, notes_core.audit_questions_for: the header
#   slice MINUS fused questions DEFERRED to a later partner PLUS fused
#   questions INBOUND from earlier slices — the filing decision is the SAME
#   shared authority G-13's target uses, so where a fusion is taught and
#   where it is solved can never disagree. IDENTICAL to the old slice for
#   grandfathered banks: no change for any existing exam. Second fix, same
#   sweep: unit_order was prose-only and built independently by NC and NA —
#   the author/gate drift class. notes_core.unit_order_from_registry is now
#   the ONE builder (ordinals = the persisted unit_code digits, NB §1A
#   A-3); NC I-5 and §2 here both call it, neither hand-builds a map.
#   coverage_target_for DELIBERATELY still reads the header slice (the
#   v3.3.1 discipline: the contract reads the BANK's evidence; only the
#   solve boundary follows filing). Deferred and inbound questions are
#   DISCLOSED in the §9 chat line.
# v3.4.0 — 2026-08-14 — G-13 INTEGRATION (in-subtopic Integration sections;
#   owner decisions of the 2026-08-14 design session; pairs with
#   Framework_NotesCreate v2.6.0 §4 B4a, Framework_NotesBlueprint v3.1.0 §3B
#   B-1; notes_core >= v2.7, notes_audit >= v2.5). New gate G-13
#   (notes_audit.gate_integration) against the unit's bank-derived
#   INTEGRATION CONTRACT (notes_core.integration_target_for — latest-partner
#   filing over the persisted teaching order, so the fusion is always taught
#   where the student has met every ingredient). HARD when the bank attests
#   a fusion for THIS unit: an integration section (a concept block whose
#   FIRST bullet is the Combines declaration — the same
#   derived-from-content discipline as every number in the document; no new
#   model field, W-3 and §0B P-4 untouched) must name every partner, sit
#   after every core concept, and carry >= 1 worked Example. DORMANT, never
#   blocking: no target (bank-less caller) and the GRANDFATHERED case — a
#   bank with no integration_partners anywhere predates notes-pyq-bank/1.2
#   and could not attest a fusion; both are reported, and the grandfathered
#   dormancy is a legitimate live-NA outcome (unlike G-12's). ADVISORY:
#   unattested integration sections (SME bridge-justified, D-6). REMEDIATION
#   ROUTING (§2A/§4): a G-13 finding is a PARTNER-HOMING gap — NA EXTENDS or
#   ADDS the integration section (net-ADD licensed exactly like G-12's);
#   it NEVER quarantines the fused question, because quarantine says "this
#   stem is corrupt or mis-filed", not "the notes lack the partner bridge".
#   G-11 runs G-13 with every other gate over the bytes that ship.
# v3.3.1 — 2026-08-14 — QUARANTINE x COVERAGE EDGE STATED (line-by-line
#   certification sweep). §5 G-12 now states explicitly what the engine
#   already does: a QUARANTINED question (§4 L-4) still counts toward the
#   coverage contract. coverage_target_for reads the BANK slice, and
#   quarantine lives in the report, never in the bank — so quarantining a
#   unit's only numeric item does not waive the numeric-Example requirement.
#   That is deliberate: quarantine says "this one stem is corrupt or
#   mis-filed", not "the syllabus stopped testing this type" — NA teaches the
#   type from a FRESH scenario (§2A licenses the add on the G-12 finding).
#   Prose only; no engine, gate or behaviour change.
# v3.3.0 — 2026-08-13 — G-12 COVERAGE (Phase 2, Recommendations 3+4; pairs with
#   Framework_NotesCreate v2.5.0 §4 B3a; notes_core >= v2.6, notes_audit >=
#   v2.4). New BLOCKING gate G-12 (notes_audit.gate_coverage) against the
#   unit's bank-derived coverage contract (notes_core.coverage_target_for):
#   every question type the unit's OWN bank attests has >= 1 worked Example,
#   and Examples span the required number of DISTINCT concept sections. The
#   contract is deliberately CONCEPT SPREAD, never an example COUNT (owner
#   decision, 2026-08-13): a count is satisfiable by clones of one scenario,
#   which add pages and teach nothing new. An Example's concept is DERIVED
#   from block order (nearest preceding concept block) — no new model field,
#   no rendering change, W-3 untouched. Two ADVISORY signals ride in the
#   gate's meta and never block: a bank-attested figure need with no concept
#   figure in the model, and duplicate_suspects (a concept section carrying
#   more than one Example of one type). Scenario diversity within a concept
#   is §2A judgement, not regex: an Example teaching a scenario an existing
#   Example already covers adds no coverage — NA REPLACES it with an
#   uncovered scenario, never keeps both. Without a target G-12 reports
#   DORMANT (the G-7a discipline). The spread clamp is
#   notes_core.COVERAGE_CONCEPT_CEILING — the engine constant is the single
#   authority; this spec deliberately restates no number.
# v3.2.0 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE ENFORCEMENT
#   (Point 1; pairs with Framework_NotesCreate v2.4.0 §4 B3, notes_docx v1.3,
#   notes_audit v2.3). G-5 (question format) now re-asserts, on the SHIPPED
#   model, the two new B3 elements: every Example carries a one-line Educational
#   Objective and one distractor-autopsy line per WRONG option (MCQ 3; MSQ
#   4 − #correct; NAT >= 1 trap value), and a Recall carries NEITHER. This is
#   deliberately folded into the EXISTING gate G-5 rather than a new identifier,
#   so notes_audit.GATES and this spec stay in one-to-one agreement (the S-2
#   sync check). notes_docx.validate_model gates the same contract at
#   construction, so the two layers agree exactly as they do for D-1. The new
#   text is document-facing and is scanned by G-4 like the rest of the file
#   (Framework_NotesCreate §7). §2A's editable model now includes the why_wrong
#   and objective fields — bounded improvement may sharpen a rationale or the
#   Objective, but may not delete either (validate_model + G-5 would fail).
# v3.1.0 — 2026-08-13 — LOSSLESS PARSE + TEXT AUTHORITY + ANCHORED G-9
#   (GAP-2026-08-12-NAPARSE; owner decisions OD-1 and OD-2 of 2026-08-13).
#   Four defects, all root-caused to test fixtures built from the simplest
#   shape rather than the production shape; every one had a green self-test.
#     (1) §2A's cycle now passes exam_code and tier into notes_docx.parse —
#         F-6 bans them from the document, so the registry unit record is the
#         only place they can come from (D-1b: without this, strict build
#         raised for EVERY unit of EVERY exam). New write property W-4.
#     (2) §0B gains P-4 PARSE FIDELITY: validate_model over the parsed draft
#         HARD-STOPS before any solving if the parser lost anything the
#         builder wrote (the permanent guard for the whole lossy-parse class;
#         D-1 lost every pure-OMML option and re-typed MCQ items NAT).
#     (3) §5 G-10 names notes_core.document_text as the ONLY text extractor —
#         a bare tag strip welded "Answer: 1" to "2.10 MIND MAP" and failed
#         correct documents on the standard tail anatomy (D-2).
#     (4) §5 G-9 scans PROSE, never model JSON (D-3), scope pinned to
#         stem/options/explanation with SPEED HACK excluded (OD-1), and runs
#         DOMAIN-ANCHORED (OD-2 Design A): only syllabus-evidenced orphans
#         report, so a clean unit yields ZERO findings and the gate is
#         readable again.
#   Companions rise to notes_core >= v2.5, notes_docx >= v1.2,
#   notes_audit >= v2.2.
# v3.0.0 — 2026-08-12 — NA BECOMES A WRITER (BREAKING; GAP-2026-08-12-NADOCX
#   patch P2 of 2; owner decisions of the 2026-08-12 design session).
#   Through v2.0.6 NA was a read-only certifier: it produced verdicts and
#   routed every defect BACK to NC (§4 L-2), and §7 stated the audited file was
#   "the SAME file ND ships — delivery never edits content". NA now VERIFIES,
#   CORRECTS, IMPROVES and EMITS the student-facing document itself. The seven
#   changes that follow, and why each one is load-bearing:
#     (1) INPUT BY ATTACHMENT (§0A). The unit .docx arrives attached to the
#         trigger message, never from Project Files. The bank, blueprint and
#         registry stay in Project Files. Attachment removes the implicit
#         guarantee that the file audited is the file NC produced, so §0B adds
#         three HARD-STOP preflights — filename identity, exam-code
#         cross-check, and sha256 against the registry's draft_ref.
#     (2) REBUILD, NEVER PATCH XML (§2A). NA parses the draft to a
#         notes_docx content model, edits the MODEL, and rebuilds through the
#         SHARED builder. notes_docx.py exists because construction was prose
#         until 2026-08-12: a writing NA hand-rolling paragraphs would have
#         been a second implementation of the §6A colour map, the cascade, box
#         styling, spacers, F-7 and the OMML conventions — the exact "one
#         contract, two implementations" class the 2026-08-10 sweep closed.
#     (3) KEY CORRECTION (§3A), superseding v2.0.0 owner decision 4a for the
#         correction path. Where the notes-derived answer disagrees with the
#         stored key, NA teaches the CORRECT method and answer instead of
#         bending the notes to a wrong key. Two tiers: a bank that contradicts
#         ITSELF is corrected silently; a bank that is internally consistent
#         is still corrected but the correction is DISCLOSED in the chat.
#         Without the tier split every disagreement would resolve in NA's
#         favour and the ground-truth check would be decorative.
#     (4) FOURTH VERDICT SOLVABLE_KEY_CORRECTED, counting toward the pass, so
#         a corrected unit certifies without weakening the vacuous-pass floor.
#     (5) NO .md REPORT (§6). The evidence moves into notes_registry.json as
#         audit_summary. The report OBJECT stays: pass_for_unit operates on it
#         and IS the vacuous-pass floor, so dropping the object would delete
#         the certification rather than just the file.
#     (6) NEW GATES (§5): G-7a visual layout (DORMANT without a renderer),
#         G-7b OMML/figure line-rule geometry, G-8 answer integrity, G-9
#         orphan terms, G-10 counter integrity, and G-11 the TERMINAL RE-GATE
#         that certifies the BYTES THAT SHIP rather than the pre-patch draft.
#     (7) ALWAYS DELIVER (§4/§9). NA emits exactly one file, always named by
#         notes_core.notes_final_filename, in every outcome. A question that
#         survives the loop is QUARANTINED, not shipped as a warning: nothing
#         inside the document ever marks a defect (F-6/§7 unchanged).
#   Companions: notes_core >= v2.4, notes_docx >= v1.1, notes_audit >= v2.0.
# v2.0.6 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §7's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename".
# v2.0.5 — 2026-08-10 — TAXONOMY SYNC (registry keyed by the Step-5 sid).
# v2.0.4 — 2026-08-10 — CROSS-CHAT HANDOFF + STALE-REF FIX.
# v2.0.3 — 2026-08-10 — POST-DEPLOY REVIEW (bank join recomputed from stored
#   fields).
# v2.0.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 2 (vacuous-pass floor wired).
# v2.0.0 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES.
# v1.1.0 — 2026-08-08 — REFINEMENT GATES (G-4, G-5, G-6).
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_NotesBlueprint.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesBlueprint.md.

```
# v3.1.0 — 2026-08-14 — INTEGRATION EVIDENCE IN THE BANK (owner decisions of
#   the 2026-08-14 design session; pairs with Framework_NotesCreate v2.6.0
#   §4 B4a and Framework_NotesAudit v3.4.0 §5 G-13; notes_core >= v2.7).
#   Real exams fuse 2-3 subtopics in one question; the bank now RECORDS that
#   evidence where it is seen — at ingest. §3B B-1 gains the OPTIONAL
#   integration_partners field (schema notes-pyq-bank/1.2, additive; 1.0/1.1
#   banks still load): the OTHER subtopics a question genuinely fuses, each
#   in the canonical Subject::Topic::Sub Topic Name scope form (the same
#   form the resolve convention teaches everywhere). Claude-as-SME tags it
#   while reading the question — the header subtopic stays AUTHORITATIVE
#   and untouched (§1.3; NB still never reclassifies); a partner is evidence
#   ABOUT the question, not a re-filing OF it. bank_add_question validates:
#   scope form only, own subtopic never a partner. WHERE the fusion is
#   taught is not NB's decision: notes_core.integration_target_for files
#   every fused question at the LATEST member of its fusion set in the
#   persisted teaching order (backward-only by construction — NC §4 B4a
#   authors to it, NA G-13 gates it). GRANDFATHERING: a bank with no
#   integration_partners anywhere (written before 1.2) makes the contract
#   DORMANT downstream — no re-ingest is forced; the next §7 bank refresh
#   or new-paper append is the natural moment tags enter. No other field,
#   count, role, tier or output changes.
# v3.0.3 — 2026-08-12 — REGISTRY 2.1 SYNC (GAP-2026-08-12-NADOCX patch P3 of 3).
#   NB creates the registry, and notes_core v2.4's registry_init now EMITS
#   notes-registry/2.1 — additively: the 2.0 keys are untouched, 1.x/2.0 still
#   load, and 2.1 adds the per-unit draft_ref (written by NC section 9A),
#   final_ref and audit_summary (written by NA section 6). This spec still
#   cited 2.0 in its companion block and in O-3, so the step that CREATES the
#   artifact named an older schema than the engine it calls — the drift the
#   SPEC-LOCK block exists to catch, one release after the flip. Corrected
#   here, together with the PIPELINE POSITION line, which described NA as
#   "audit + loop" and no longer matched Framework_NotesAudit v3.0.0, where NA
#   also corrects, rebuilds and emits the unit's _Final.docx. Companion:
#   notes_core >= v2.4. No behaviour change: notes_blueprint.py is untouched
#   and notes-blueprint/2.0 is unchanged.
# v3.0.2 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts; pairs
#   with Framework_NotesCreate v2.2.1 and notes_core v2.1 SPEC-LOCK). §1A A-3
#   now names notes_core.unit_code as the FORMATTER of the numeric code (the
#   {EXAM}_S{s}_T{t}_ST{nn} pattern shown anywhere in this spec is the human
#   rendering; the engine is the single authority, spec-lock-pinned). §5's tier
#   bands and the §4 vocabularies are likewise spec-lock-pinned in notes_core.
# v3.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW RESOLVE (three notes from the v3.0.0
#   deployment verification).
#   (1) "133/133 unverifiable from the repo": the manifest is a PROJECT artifact,
#       so that validation is now a standing, REPRODUCIBLE preflight instead of a
#       changelog claim: notes_blueprint.verify_manifest — CLI
#       `python3 notes_blueprint.py --verify-manifest <path> [exam_code]` —
#       loads the manifest (exam_code gate), asserts unique unit_codes + gapless
#       ST numbering, sweeps ALL THREE resolution tiers across every subtopic,
#       and checks filename uniqueness. §1A A-1 now runs it as the session
#       preflight. Re-run against the live IIT_JAM_BIOTECHNOLOGY manifest at
#       resolve time: 133 subtopics, 133/133 sid + scope + bare-name, VERDICT
#       PASS — and anyone with the project file can re-verify with one command.
#       Companion: notes_blueprint >= v2.1 (additive; v2.0 surface unchanged).
#   (2) "breaking for mid-pipeline projects": intentional, now stated as the
#       explicit MIGRATION block after §7 — one NB re-run per project, bank
#       untouched (A-0 resumes; nothing re-downloads), and the previously
#       UNSPECIFIED state carry-over across the key change (1.x unit_code keys ->
#       sid keys) is specified: each 1.x unit's name resolves to its sid via
#       notes_core.resolve_unit; states/notes_version/artifacts carry over;
#       ambiguous/none resolutions are listed for the owner, never guessed.
#   (3) "NB hard-stops without the Step-5 manifest": intentional and now stated
#       plainly in the PREREQUISITE — Step 5 (PYQExtract) must have run for the
#       exam BEFORE Notes; that ordering IS the single-vocabulary architecture.
#       An exam that ran Notes before Step 5 completes Step 5 first, then takes
#       the MIGRATION path.
# v3.0.0 — 2026-08-10 — TAXONOMY CONSUMER (breaking; owner decision: ONE subtopic
#   vocabulary across Test Creation and Notes Creation). The Step-5
#   [ExamCode]_subtopic_manifest.json (the same file MockBlueprint consumes, whose
#   human view is [ExamCode]_taxonomy.xlsx) is now the SINGLE SOURCE OF TRUTH for
#   Notes unit identity. Step 5 itself is UNTOUCHED — Notes only consumes.
#     (1) NEW §1A applies the Mock pipeline's Cross-Step Subtopic Contract
#         (Framework_Blueprint RULES 1/2/2a) to Notes verbatim: every unit carries
#         its manifest sid VERBATIM; resolution failure is a HARD STOP whose fix is
#         upstream (re-run Step 5); NB NEVER mints, sequences, or fallback-creates
#         an id — on ANY path, including evidence-added.
#     (2) Unit names, section and topic are the manifest's EXACT BYTES; the
#         syllabus's role shrinks to what §1.1 always said — the MASTER FILTER
#         (in/out of scope, roles, tiers) — never a naming authority. §2 S-1
#         rewritten; the summary gains a SYLLABUS-MATCH report.
#     (3) The registry and blueprint are KEYED BY sid (schemas notes-registry/2.0
#         — 2.1 as of notes_core v2.4, additive — and notes-blueprint/2.0). The numeric unit_code {EXAM}_S{s}_T{t}_ST{nn}
#         survives as a DERIVED PRESENTATION attribute (B1 title number, F-1
#         filename): numbers come from manifest row order via
#         notes_core.assign_numbering and, once assigned, are PERSISTED — a Step-5
#         re-run that inserts/reorders subtopics never renumbers an existing unit;
#         new sids append with next numbers. The F-1 slug is notes_core.sid_slug
#         (the sid's final component), so a delivered filename is visibly
#         traceable to its taxonomy.xlsx row.
#     (4) taxonomy_ref {path, sha256, subtopics, generated} over the manifest
#         bytes is emitted beside bank_ref (notes_core.taxonomy_ref_for) and
#         stored in blueprint + registry; verify_taxonomy_ref is the staleness
#         link (NC §1.2 checks it; a changed manifest flips units STALE, §7).
#     (5) Engine: notes_blueprint.build_blueprint_v2 (manifest-consuming) replaces
#         build_blueprint in this spec's flow (the v1 builder remains in the
#         engine for legacy reads only). Companions: notes_core >= v2.0,
#         notes_blueprint >= v2.0. Engineering-session validation against the
#         live IIT_JAM_BIOTECHNOLOGY manifest (a project artifact, not in this
#         repo) is reproducible via the v3.0.1 --verify-manifest preflight.
#     (6) NEW §7 rules: manifest-hash staleness, ORPHANED (a delivered unit whose
#         sid left the manifest is reported, never deleted), and the BANK-MATCH
#         report (bank triples that fail to norm-match any manifest triple —
#         expected empty; nonzero exposes an upstream sorting anomaly).
# v2.0.5 — 2026-08-10 — DELIVERY-FOOTER CONTRACT HONORED. v2.0.4 added
#   present_files at every BATCH STOP but rendered no footer — a violation of
#   Framework_DeliveryFooter §4-0 R1 ("a present_files call is always followed by
#   the footer"), and the Notes pipeline had no §3 registry entry. A-7 now renders
#   F1 (batch bar) after each non-final batch and F2 (4-cell NOTES bar, Next: NC)
#   after the final delivery, per Framework_DeliveryFooter v1.18 (which now carries
#   the NB/NC/NA/ND §3 entries, the NOTES bar, and the Notes §6 chain).
# v2.0.4 — 2026-08-10 — POST-DEPLOY REVIEW. (B) O-2 no longer claims a "bank"
#   provenance value the engine never writes — unit provenance is
#   "syllabus"/"evidence-added"; only the pyq_count is bank-DERIVED, now stated as
#   such. (D) the bank checkpoint is written to /mnt/user-data/outputs AND
#   presented (present_files) at every BATCH STOP, and A-7 option B now tells the
#   operator to DOWNLOAD that presented bank and re-upload it to project knowledge
#   before a fresh-chat resume (the previous "already in project Files" was false —
#   write_bank targets the working dir). A-0 makes the resume load explicit.
#   Companion: notes_core >= v1.8 (stored subtopic_key is informational; reads
#   recompute — a bank written by an older notes_core still joins correctly).
# v2.0.3 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   notes_core.subtopic_key now reuses syllabus_provenance.norm per component so
#   bank counts join blueprint units across syllabus-vs-header label drift
#   (& vs and, dash/unicode/slash-spacing). Prevents a real subtopic silently
#   getting pyq_count=0 and the wrong tier. Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route. §1.3 updated.
# v2.0.2 — 2026-08-10 — BATCH STOP law added to §3A (owner-selected cadence).
#   The eager ingest now processes papers 3 at a time and PAUSES for user
#   confirmation after each batch (A-7), mirroring PYQExtract /
#   Framework_MockTestAnalyse: BATCH_SIZE = 3 is non-negotiable, and the response
#   ENDS after each batch so the run never auto-advances in one turn. The A-6 bank
#   checkpoint makes the pause resume-safe (reply 'continue', or re-trigger NB in
#   a fresh chat — it resumes from the paper_keys already in the bank). Spec-only
#   change; no engine surface moved.
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIXES. (1) bank_ref is now actually
#   EMITTED: NB builds the blueprint with bank_ref=notes_blueprint.bank_ref_for(
#   bank_path) after writing the bank, so §6 O-2's staleness link is real and NC
#   §1.2 can detect a blueprint/bank mismatch (notes_core.verify_bank_ref).
#   (3) §3A-1 enumeration is reworded to the CLASS T bridge: Claude runs the
#   paginated + recursive Google Drive:search_files walk IN ITS OWN TURN and
#   passes collect_corpus_files a PLAIN-LOOKUP resolver over the materialised
#   listing — never the tool marker (the defect audit_callgraph C6 exists to
#   catch). §3A-3 download uses the same resolver idiom explicitly.
# v2.0.0 — 2026-08-10 — INGEST BASE (breaking role change). NB is now the base
#   of the Notes architecture: it performs the EAGER full-corpus ingest of every
#   sorted-PYQ paper and emits a verified notes_pyq_bank.json (questions +
#   options + verbatim correct_answers + verbatim explanations + a stem/solution
#   figure split) that NC and NA consume READ-ONLY. Neither NC nor NA re-reads
#   Drive again. Consequences of the six owner decisions locked 2026-08-10:
#     (1) Drive images are read via corpus_io (the proven PYQExtract path):
#         enumerate -> screen -> batch-of-3 download -> image extract -> vision
#         read. No FIGURE_PENDING stem-only fallback for the normal run.
#     (2/3) exam_date comes from the (stable) filename via
#         notes_core.parse_exam_date_from_filename; nothing in the body carries it.
#     (4) answers + explanations are read from the doc VERBATIM and never
#         re-derived; NA runs permanently in ground-truth mode; KEY_FLAG dropped.
#     (5) subtopic-wise pyq_count + recent-3-year counts are DERIVED from the
#         bank (notes_core.derive_taxonomy_counts); the separate PYQ Analysis doc
#         is no longer a prerequisite (optional cross-check only, §2 S-3).
#     (6) image reads succeed (files < 10 MB); NB does NOT hard-stop on a per-
#         image gate finding — it reports it. Only a corrupt ZIP or a truncated
#         download (size mismatch) stops the affected paper, which then routes to
#         the upload lane.
# v1.1.0 — 2026-08-08 — REFINEMENT SUPPORT: allowed_question_types, explicit unit
#   ordering (seq_in_topic), per-unit prose_ban_exemptions; registry schema 1.1.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Design locked + validated on the IIT JAM
#   BT Enzyme Kinetics proof-of-concept (37/37 PYQ solvability). SourceMap folded in.
```

## Framework_NotesCreate.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesCreate.md.

```
# v2.7.1 — 2026-08-15 — UNIVERSAL SPACING INVARIANT
#   (GAP-2026-08-15-ADJACENT-TABLES; field report from the first live NC
#   run: heading bars, data tables and boxes rendered FUSED, zero gap —
#   Word merges directly adjacent tables and nearly every element of these
#   notes is a table). The §4 spacer rule was the box-after-box special
#   case; notes_docx v1.4 now guarantees the GENERAL invariant — no two
#   tables are ever adjacent anywhere in the body, enforced by a
#   post-assembly pass so it holds for every block combination, current
#   and future, by construction. Model, anatomy, colours, numbering,
#   parse(): all unchanged; W-3 byte-identity preserved. Existing drafts
#   gain the spacing on their next rebuild (NA §0B P-4b reads the byte
#   difference as the documented builder-upgrade diagnostic, never a
#   stop). Companion: notes_docx >= v1.4.
# v2.7.0 — 2026-08-15 — THE FORMAT CONTRACT (figure vs text balance; owner
#   decisions of the 2026-08-15 design session, approved proposal; pairs
#   with Framework_NotesAudit v3.5.0 §5 G-12; notes_core >= v2.10,
#   notes_audit >= v2.7). Reading a figure (V–I curve, ray diagram,
#   potential well, phase diagram) is a SEPARATE skill from knowing the
#   theory — a subtopic with perfect prose and zero figure practice is a
#   gap wherever the exam asks figure-based questions. §4 B3a gains the
#   FORMAT CONTRACT, derived entirely from evidence every bank already
#   carries (the per-question figure flag + concept tags — no new field,
#   no re-ingest): FMT-1 both formats attested -> both taught, with >= 1
#   concept section PAIRING a rendered figure with an Example that reads
#   it (HARD, G-12-enforced); FMT-2 frequency shapes EMPHASIS — the lead
#   Example follows each concept's dominant format — never exclusion and
#   never count-mirroring (spread-not-count, applied to formats); FMT-3 no
#   evidence, no demand — a zero-figure slice never forces a figure. The
#   old unit-level requires_figure ADVISORY is superseded by FMT-1's hard
#   pairing where figure evidence exists (the advisory itself still rides
#   in G-12 meta). Anatomy, colours, density, builder: all UNCHANGED —
#   figures render through the existing F-4 rules. Rollout follows the
#   G-12 precedent: applies at each unit's next audit; no grandfathering
#   flag exists or is needed.
# v2.6.2 — 2026-08-14 — ADVERSARIAL-REVIEW FIXES (independent fresh-eyes
#   review + 400-trial property fuzz; pairs with notes_core v2.9,
#   notes_audit v2.6, Framework_NotesAudit v3.4.2, Framework_NotesBlueprint
#   v3.1.1). Six fixes: (1) new I-7 — a TIER-3 unit CAN be a fusion host:
#   the inbound fused questions ARE the evidence, so it ships its TIER-3
#   anatomy PLUS the demanded integration section(s), the only Examples in
#   such a unit; G-13 demands them, G-12 (header-slice contract) never
#   double-demands. (2) I-1 placement stated for units without B5 (before
#   B6; the mechanical check is unchanged). (3) I-6: EVIDENCE OUTRANKS the
#   1-2-partner style bound — an attested 3-partner fusion at a mid-topic
#   unit gets its section there; the bound shapes unattested SME sections
#   only (the old wording deadlocked against a G-13 demand). (4) I-2:
#   duplicate partner names are Topic-qualified (NB E-16). (5) PIPELINE
#   POSITION synced to NA v3.0.0 (was "audit + convergence loop" — the
#   same stale line NB v3.0.3 fixed on its side). (6) PREREQUISITE: the
#   "returned by NA for full regeneration" path died with NA §4 L-2
#   (regeneration is NA-internal); the real NA->NC return is the missing-
#   draft_ref preflight. Companions: notes_core >= v2.9.
# v2.6.1 — 2026-08-14 — ONE ORDER-MAP BUILDER (line-by-line certification
#   sweep of the v2.6.0 feature; pairs with notes_core v2.8 and
#   Framework_NotesAudit v3.4.1). v2.6.0's I-5 said "unit_order maps
#   subtopic_key -> the registry's persisted ordinal" in PROSE and left NC
#   and NA to each build the map — the author/gate drift class this
#   framework exists to kill (two builders, one contract). I-5 now names
#   notes_core.unit_order_from_registry as the ONE builder (ordinals = the
#   persisted unit_code digits, NB §1A A-3); NA §2 and G-13 call the same
#   function, so filing can never disagree between author and gate. Wording
#   only on this side; the engine change and the companion audit-boundary
#   fix (a fused question is SOLVED where it is TAUGHT) live in notes_core
#   v2.8 / Framework_NotesAudit v3.4.1.
# v2.6.0 — 2026-08-14 — IN-SUBTOPIC INTEGRATION SECTIONS (owner decisions of
#   the 2026-08-14 design session; approved on the DC/AC Circuits placement
#   demo; pairs with Framework_NotesBlueprint v3.1.0 §3B B-1,
#   Framework_NotesAudit v3.4.0 §5 G-13; notes_core >= v2.7, notes_audit >=
#   v2.5). Real exams fuse 2-3 subtopics in ONE question; the IFAS portal
#   links one page per subtopic (owner constraint), so the fusion is taught
#   IN-SUBTOPIC: new §4 B4a — an INTEGRATION SECTION closing the concept
#   stack, after every core concept's KEY POINTS and immediately before the
#   TRAP BOX. It is an ORDINARY concept section (same block type, own example
#   stack, own KEY POINTS; numbering, colours, gates all already apply — no
#   builder change of any kind) marked ONLY by its first bullet: the Combines
#   declaration. Rules I-1..I-6: placement (end of stack), the Combines
#   declaration + bridge bullets, backward-only partners (persisted teaching
#   order — students have met every ingredient), evidence-driven authoring
#   against notes_core.integration_target_for (latest-partner filing —
#   the SAME contract NA's G-13 gates, so author and gate can never
#   disagree), the last-subtopic capstone bound, and the no-earlier-partner
#   edge (no integration section). B8's mind map stays SUBTOPIC-ONLY —
#   merged concepts never enter it (owner decision). Anatomy is otherwise
#   UNCHANGED; TIER-3 unchanged; §7 bans apply to integration prose in full.
# v2.5.1 — 2026-08-14 — STALE ANATOMY REFERENCE (line-by-line certification
#   sweep). §2.1 called the fresh-numbered practice questions "§4 B4/B7" — a
#   leftover from a pre-v2.0.0 block layout. Under the CURRENT §4 anatomy B4
#   is the KEY POINTS box; the practice questions are B3 (Examples) and B7
#   (Recall Check). Reference corrected to "§4 B3/B7". Wording only; no
#   behaviour, gate or engine change.
# v2.5.0 — 2026-08-13 — COVERAGE CONTRACT AUTHORING (Phase 2, Recommendations
#   3+4; pairs with Framework_NotesAudit v3.3.0 §5 G-12; notes_core >= v2.6).
#   New §4 B3a: before drafting Examples, NC computes the unit's coverage
#   contract with notes_core.coverage_target_for over the unit's bank slice
#   and AUTHORS TO IT — at least one worked Example for every question type
#   the unit's own PYQs attest, and Examples spread across at least the
#   required number of DISTINCT concept sections. The contract is CONCEPT
#   SPREAD, deliberately NOT an example count (owner decision, 2026-08-13):
#   more Examples on one scenario add pages, not coverage — an additional
#   Example is justified only by an uncovered concept, scenario or type.
#   NotesAudit G-12 gates the SAME bank-derived contract on the shipped
#   file, so author and gate can never disagree. An empty bank slice means
#   no contract (TIER-3 "no examples where no evidence" unchanged). No model,
#   anatomy, colour or rendering change of any kind — B3a constrains WHERE
#   Examples go and WHICH types they teach, not how they are built.
# v2.4.0 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE (Point 1;
#   pairs with Framework_NotesAudit v3.2.0 and notes_docx v1.3). Every worked
#   Example (B3) now ends with TWO new elements, and a Recall (B7) carries
#   NEITHER:
#     (1) A per-option "why the other options fail" block — ONE line per WRONG
#         option, naming the specific error that produces it (MCQ: 3 lines;
#         MSQ: 4 − #correct; NAT: this becomes a "trap values" block of >= 1
#         line, each a wrong number and the mistake that yields it). The
#         builder stores these in the example block's why_wrong field.
#     (2) A one-line Educational Objective — the transferable takeaway — stored
#         in the objective field.
#   These are built THROUGH notes_docx.build like everything else (§4A):
#   notes_docx.validate_model enforces the exact per-option count and the
#   presence of the Objective at construction, and Framework_NotesAudit G-5
#   re-asserts both on the shipped file, so a missing rationale can never reach
#   a delivered document. The autopsy header renders in the TRAP red and the
#   Objective label in the L2 teal — both EXISTING §6A colours, so no new
#   colour is introduced. The new text is document-facing prose and is subject
#   to §7 in full (no question-type names, no years, no PYQ token). Anatomy,
#   density, math and numbering (§4A–§6A otherwise) are UNCHANGED.
# v2.3.1 — 2026-08-13 — OPTION CONTRACT MADE EXPLICIT (GAP-2026-08-12-NAPARSE
#   D-1). §4 B3 now states that the "N. " option marker is the ONLY
#   guaranteed plain text (w:t) on an option line: the option's CONTENT may
#   be entirely OMML, so any reader of a built document must never require
#   w:t content beyond the marker. Framework_NotesAudit §0B P-4 enforces it.
# v2.3.0 — 2026-08-12 — SHARED BUILDER + DRAFT PROVENANCE (GAP-2026-08-12-NADOCX
#   patch P2 of 2; pairs with Framework_NotesAudit v3.0.0).
#     (1) CONSTRUCTION IS NOW AN ENGINE. NC builds the .docx by calling
#         notes_docx.build(model, path) — never by hand-rolling paragraphs.
#         Until 2026-08-12 document construction lived only in this spec's
#         prose, so NC's run-time code was the sole implementation of the
#         section 6A colour map, the decimal cascade, box styling, spacer
#         paragraphs, rule F-7 and the OMML conventions. NA now writes
#         documents too (v3.0.0), and two implementations of one contract is
#         the defect class the 2026-08-10 sweep closed for filenames. New
#         section 4A states the content model and the derived-numbering rule.
#     (2) NUMBERS ARE NO LONGER WRITTEN BY NC. Every "n.k", "n.k.m",
#         "Example j" and "Recall j" is DERIVED from block order by
#         notes_docx.outline_of at render time. Section 6A's renumber rule is
#         satisfied structurally: there is no stored number that can go stale.
#     (3) DRAFT PROVENANCE (new section 9A). NC records
#         notes_core.docx_ref_for(draft) into the registry unit as draft_ref
#         (schema notes-registry/2.1). NA now receives its input as a CHAT
#         ATTACHMENT rather than from Project Files, so nothing else would
#         prove the file audited is the file NC produced. draft_ref is the
#         evidence for NA section 0B P-3.
#     (4) HANDOFF CHANGED (section 9). The draft is NO LONGER uploaded to
#         Project Files. Its footer badge is "Use locally" and the Next
#         callout instructs the operator to ATTACH it to the NA chat. The
#         registry is still uploaded, because NA reads it from Project Files.
#     (5) t3_mathcomp.py is now ROUTED to NC. F-3(a) has always required its
#         conventions, but the engine was never on NC's route — a real gap
#         found while wiring the shared builder.
#   Companions: notes_core >= v2.3, notes_docx >= v1.0. Anatomy, density,
#   format rules and content bans (sections 4-7) are otherwise UNCHANGED.
# v2.2.1 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). A
#   deployment review found F-1 restating the filename recipe in prose while
#   notes_core.notes_filename sanitises non-alphanumeric runs in {Slug} to "_"
#   — one contract, two implementations. F-1 now names the ENGINE as the single
#   authority, states the sanitisation, and requires NC to derive the draft
#   filename by CALLING notes_core.notes_filename — never by re-implementing
#   the pattern. The same sweep marked §5 and §6A as spec-lock-pinned (the
#   notes_core v2.1 SPEC-LOCK self-test pins every literal these sections
#   restate) and replaced §9's informal "[ExamCode]_<unit>.docx" with "the
#   unit's F-1 filename". Companion: notes_core >= v2.1. No behaviour change.
# v2.2.0 — 2026-08-10 — TAXONOMY-SYNCED OPERATOR INPUT (Framework_NotesBlueprint
#   v3.0.0). Units are identified by the Step-5 manifest sid (the registry key);
#   the OPERATOR identifies a unit by copying a cell from
#   [ExamCode]_taxonomy.xlsx — the SAME convention that workbook's "How to use"
#   sheet already teaches for Step 6. NEW §0: three-tier resolution via
#   notes_core.resolve_unit — (1) Sub Topic Id (column D), (2)
#   Subject::Topic::Sub Topic Name scope (columns A::B::C), (3) bare Sub Topic
#   Name (column C), norm-matched so case/dash/&/spacing variants resolve; a
#   multi-hit bare name STOPS and lists the candidates with their Topics for the
#   operator to choose; zero hits STOP with nearest-name suggestions — NEVER a
#   fuzzy auto-pick. §1.2 additionally verifies taxonomy_ref
#   (notes_core.verify_taxonomy_ref): a manifest changed since the blueprint was
#   built STOPS the unit back to NB, exactly like the stale-bank stop. F-1's
#   {Slug} is the sid's final component (notes_core.sid_slug), so every
#   delivered filename traces visibly to its taxonomy.xlsx row. Companion:
#   notes_core >= v2.0. B1's "n" and F-1's numbers come from the unit's
#   PERSISTED unit_code/seq_in_topic (NB §1A A-3) — they never churn on a
#   taxonomy re-run. All v2.1.x behaviour otherwise unchanged.
# v2.1.5 — 2026-08-10 — §8 wording aligned with §9/DeliveryFooter §3. Each
#   multi-unit request is separate PER-UNIT RUNS, each a complete step ending F2
#   (§9); the continue-confirmation is BETWEEN runs, not batches within one (NC
#   has no intra-run batching — that F1 pattern is NB's). §8 retitled RUNS AND
#   STATE and cross-references §9. Wording only; no behaviour change.
# v2.1.4 — 2026-08-10 — CROSS-CHAT HANDOFF SPECIFIED. NC runs in its own chat, so
#   its draft .docx must reach NA (a fresh chat) the same way NB's bank reaches NC.
#   New §9: NC present_files the draft + the updated registry and renders the F2
#   footer (4-cell NOTES bar "2 of 4"; Next → NA), so the handoff persists and the
#   next-step pointer actually prints. Pairs with Framework_DeliveryFooter v1.19.
# v2.1.3 — 2026-08-10 — POST-DEPLOY REVIEW. bank_questions_for now joins by
#   RECOMPUTING the subtopic key from stored fields (drift class closed), so an
#   older bank still reads correctly. Companion: notes_core >= v1.8.
# v2.1.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   bank_questions_for now joins via the hardened notes_core.subtopic_key
#   (syllabus_provenance.norm). Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route.
# v2.1.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 1 (bank staleness stop wired).
#   §1.2's "signals a stale bank" stop now has evidence: NC reads the blueprint's
#   bank_ref and calls notes_core.verify_bank_ref(bank_path, bank_ref) before
#   drafting; a sha256 mismatch (blueprint built from a different bank than the
#   one on disk) or a missing bank_ref STOPS the unit back to NB. Companion bump
#   to notes_core >= v1.6.
# v2.1.0 — 2026-08-10 — BANK CONSUMER (Framework_NotesBlueprint v2.0.0). NC no
#   longer reads Drive or builds its own PYQ bank. It LOADS the bank NB produced
#   (notes_pyq_bank.json), filters it to the unit's subtopic
#   (notes_core.bank_questions_for), and drafts from those records. The FIGURE
#   flag is the bank's stem_figures; the correct_answer and explanation are read
#   from the bank as SME grounding (never reproduced verbatim — §3 paraphrase
#   rule unchanged). §1 rewritten accordingly; all v2.0.0 anatomy/format/gates
#   (§4-§8) are unchanged.
# v2.0.0 — 2026-08-08 — REFINEMENT RELEASE (breaking anatomy change). Encodes the
#   12-item refinement set locked in the 2026-08-08 review session and approved
#   on the Enzyme Kinetics golden sample: title-only header; plain concept
#   headings; frequency tags removed from the document; "Example N" boxes with
#   the fixed stem/options/Answer/Explanation template; question types
#   constrained to the exam's own type set; hierarchical cascade numbering;
#   level-locked colour map; figure labels inside the image with no captions
#   and no exam vocabulary; no editorial lead-ins; no exam-type words, years,
#   or PYQ references anywhere in delivered text; EXAM LENS block removed;
#   RECALL CHECK re-defined as exam-format questions; structural-OMML +
#   styled-script math standard document-wide including diagrams.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_NotesDeliver.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_NotesDeliver.md.

```
# v1.1.3 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §1.0's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename" —
#   Framework_NotesCreate F-1 (notes_core.notes_filename) is the single
#   authority for notes filenames (§1.1 already deferred to F-1). Pairs with
#   Framework_NotesCreate v2.2.1. Nothing else changed.
# v1.1.2 — 2026-08-10 — TAXONOMY SYNC (Framework_NotesBlueprint v3.0.0). The
#   registry key is the Step-5 manifest sid; an operator unit reference is
#   resolved per Framework_NotesCreate section 0 (notes_core.resolve_unit — same
#   taxonomy.xlsx convention). The §1.3 delivery line identifies the unit as
#   <Sub Topic Name> (<sid>) alongside unit_code/notes_version. Companion:
#   notes_core >= v2.0. Nothing else changed.
# v1.1.1 — 2026-08-10 — CROSS-CHAT READ + REGISTRY. Made the fresh-chat handoff
#   explicit: ND READS the audited .docx + _Audit.md + notes_registry.json from
#   Project Files (NA uploaded them), and re-presents the updated registry
#   (unit → DELIVERED) alongside the delivery so the state persists. Pairs with
#   Framework_NotesAudit v2.0.4 / Framework_DeliveryFooter v1.19.
# v1.1.0 — 2026-08-10 — POST-DEPLOY REVIEW. (1) ND is the delivery step but never
#   said to present_files its artifacts and rendered no footer — so on mobile the
#   delivered files were unreachable and the Framework_DeliveryFooter contract was
#   unmet. §1 now present_files the notes .docx + audit report and renders the F2
#   step-complete footer (4-cell NOTES bar "4 of 4"; Framework_DeliveryFooter
#   v1.18 §3 ND entry). (2) Removed stale references the NA v2.0.0 changes left
#   behind: KEY_FLAG is retired (NA owner decision 4a) and answer-mode "M-2" is
#   gone (NA runs permanent ground-truth mode). Companion: notes_core >= v1.0.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
```

## Framework_PYQCompress.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCompress.md.

```
#   v1.1 — 2026-07-25 — SIZE GATE REMOVED. Every attached file is now compressed
#          regardless of size (corpus_io v1.0.3 `always=True`); previously anything at or
#          under SIZE_BUDGET was reported T0 and skipped. The operator selects what to
#          compress by selecting what to attach. SIZE_BUDGET is unchanged and still
#          governs the LADDER TARGET and the MARGINAL/BLOCKED verdicts — it is no longer
#          an eligibility test. New EC-C1b covers the file that cannot be improved:
#          corpus_io restores the original bytes and it is reported but not delivered,
#          which stops CHECK 5 from hard-stopping the run on an already-optimal document.
```

## Framework_PYQCore.md

Entry v1.5 moved at framework release 2026.08.22.2 (EC-P42 — PYQScan-route
headroom, flagged +809 B by the 2026.08.21.4 deploy review). Current-version
entry remains in Framework_PYQCore.md.

```
# v1.5 — 2026-08-16 — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION (SESSION-BUDGET LAW).
#   §9 gains four edge cases. The reference incident is IIT_JAM_MATHEMATICS PYQExtract:
#   two consecutive sessions, 54 tool calls, ZERO of 22 papers processed, because three
#   independent stalls each sufficient on their own were present at once.
#   EC-P40 (the probe is a SPENDER, not a free classifier — a CLASS T acquisition
#   performed BEFORE the partition must be subtracted from the budget, and is charged
#   even when it fails, because the bytes arrived either way). EC-P41 (a PARTIAL
#   listing is worse than an empty one — EC-P39 catches zero and nothing caught
#   21-of-22; the transcription from connector response to DRIVE_LISTING_CACHE is the
#   highest-risk step in the acquisition path and must be asserted against an
#   independently declared count, with a HARD STOP). EC-P42 (SPECIFICATION-READ COST is
#   a session resource — the framework priced payload characters and paper pacing but
#   never priced reading its own specification, which on Step 5 is 556,834 B / ~139,208
#   tok / >=36 view calls BEFORE any work). EC-P43 (the DIRECT EGRESS LANE — when the
#   container can reach Drive and the folder is link-shared, python fetches the bytes
#   itself and EC-P36's double charge disappears entirely; proven per exam on a real
#   paper, never assumed, never fatal on failure).
#   EC-P36/EC-P37 are unchanged and remain correct: they describe the connector lane,
#   which stays the fallback whenever the direct lane is unavailable.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCore.md.

```
# v1.4 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. §9 gains EC-P37
#   (inline channel in a batched, multi-session step — the budget is per SESSION, a
#   fresh chat resets it, halve it because an inline payload is charged twice, and
#   partition only AFTER the recency sort), EC-P38 (channel transition on resume —
#   persist and reuse the verdict, re-probe once on a first-acquisition failure, never
#   flip silently) and EC-P39 (an empty listing is a TRANSPORT diagnosis, never a
#   zero-PYQ exam — the one transport defect in the framework that produced a wrong
#   ANSWER rather than a stall). EC-P35/EC-P36 now say explicitly that their
#   single-session resolution does not apply to a batched step.
# v1.3 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. §9 gains EC-P35 (the
#   Drive channel cannot reach the container) and EC-P36 (an inline channel exceeds the
#   context budget). Neither condition is visible to size-based partitioning: measured
#   on IIT_JAM_MATHEMATICS, partition_by_transport returned auto:22 / upload:0 for a
#   corpus of which ZERO papers were actually fetchable, so plan_transport() printed
#   nothing and the operator learned the transport shape of the run AFTER the
#   acquisition loop — the exact discovery EC-P31 and S5-1 exist to prevent. MINIMUM
#   COMPANION VERSIONS now require the engines carrying stage_drive_payload(),
#   bare-base64 decode and channel-aware partitioning.
# v1.2 — 2026-08-15 — GAP-2026-08-15-BAREQ (R-3). Phase-B checklist TASK 1 no longer
#   names a local regex: Q-counting uses bc.detect_question_start(), the same detector
#   Steps 3 and 5 parse with. A checklist that tells the operator to reproduce a private
#   pattern is how a third Q-detection dialect stayed in production.
# v1.1 — 2026-08-05 — GAP-2026-08-05-001. §6 DISCRIMINATOR rewritten: "next non-empty
#   paragraph" -> "next CONTENT-BEARING BLOCK" with the four textless classes enumerated
#   (image, equation, embedded object, TABLE) plus auto-numbering; the false invariant "a
#   stem continuation NEVER is [followed by a date label]" corrected; DISCRIMINATOR 2
#   (colour, per-FILE gate) added; the NAT impossibility stated explicitly. MINIMUM
#   COMPANION VERSIONS now require the GAP-2026-08-05-001 engine and python-docx >= 1.1.0.
# v1.0.2 — 2026-07-31 — HOST-NOTE HEADER DISAMBIGUATED (sync audit, ownership check).
#   The scaffolding header '## §2-HOSTED — ...' matched the '^## §N' section-header
#   pattern, so a tool locating §2 by header could resolve to this file's host note
#   instead of Framework_PYQDraft.md, which owns §2. Renamed to 'HOSTED SECTION S2-3
#   (from §2 ...)' so §-ownership is unique per file: §2 -> Draft; hosted S2-3 content
#   here, unchanged and still byte-identical to v2.29. Scaffolding-only; zero rule change.
# v1.0.1 — 2026-07-31 — ERA-SYNC SOURCING LINE (audit_sync). The split placed S2-3's
#   prose mentions of OUT_OF_PATTERN in this file while the executable bc.OUT_OF_PATTERN
#   call sites landed in Framework_PYQScan.md; audit_sync's per-file rule (any spec naming
#   OUT_OF_PATTERN must source it from the engine) then fired on this file. Added an
#   engine-sourcing comment to the S2-3 host note — scaffolding only, the hosted v2.29
#   content remains byte-identical. Zero rule/functionality change.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
```

## Framework_PYQCount.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQCount.md.

```
# v1.4 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (sibling fix, applied
#   here per the LAW-PROPAGATION LAW rather than waiting for Step 4 to fail). THE BRIDGE
#   showed a flat `list_fn` that ignores its folder_id argument. corpus_io.collect_corpus_files
#   RECURSES into sub-folders, so on a year-subfoldered Drive folder that resolver returns
#   the same entries for the sub-folder and the walk raises DuplicatePaperError — a HARD
#   STOP blaming the operator's Drive for a defect in this contract. The cache is now
#   keyed by folder id; a bare {'files': [...]} cache is still accepted, scoped to the
#   root. Found by reading the engine while fixing Step 5, not by a failing run: a flat
#   corpus never triggers it.
# v1.3 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (EXECUTION-BOUNDARY
#   LAW). S5-4 step 1 injected the bare name `gdrive_download_file` into
#   corpus_io.fetch_drive_docx. That name was defined NOWHERE — no spec, no engine, no
#   builtin — so executed literally it raised NameError, every paper fell through
#   TransportFallback to the upload lane, and the Drive lane was unreachable on EVERY
#   run of EVERY exam. Measured on IIT_JAM_MATHEMATICS (22 papers, all under
#   DRIVE_CAP): 0 of 22 acquired, Task 1 unconfirmable, 22 manual uploads demanded.
#   This is GAP-2026-07-26-003 applied to the PYQ counting path: the identical fix
#   shipped in MockTestAnalyse v2.37 on 2026-07-26 and was never propagated here, and
#   the 2026-07-31 split from PYQAnalyse v2.29 then copied the defect forward "content
#   byte-identical" into a file that never mentions the GAP id. §5 now opens with a
#   CLASS T transport declaration and THE BRIDGE, in a ```python fence so the CI can
#   read it; S5-4 step 1 injects a bound resolver. New S5-0 CHANNEL PROBE measures the
#   connector's delivery form on ONE paper before Task 1 — the "results always spill to
#   disk" invariant is MEASURED FALSE (one 40,488-byte .docx spilled in one deployment
#   and returned inline in another), so it is now probed, never assumed, and never
#   inferred from a directory listing. S5-8's "3 tool calls per session" is corrected
#   to 3 PHASES: it omitted the N connector calls that ARE the acquisition.
#   audit_callgraph gains C7 (text pass — an AST-only pass cannot see this call site,
#   which lives in an untagged, non-parseable fence) and C8.
# v1.2 — 2026-08-15 — GAP-2026-08-15-BAREQ (R-3). The S5-1 mandatory gate and
#   count_sorted_file() carried an inline r'^Q\.?\s*\d+' justified by an ASSUMPTION about
#   PYQSort's output ("always outputs Q.<N> format") where a DELEGATION belongs, and
#   nothing enforced the assumption. That dialect matched strings the engine's table did
#   not — a bare "Q.4" among them — so on IIT_JAM_MATHEMATICS 12-Feb-2017 this step
#   counted 60 for a file Step 5 extracted as 56, attributing four questions to whatever
#   subtopic happened to precede them. Both sites now call bc.detect_question_start();
#   audit_deep's new INLINE-QREGEX check fails the build if a private copy returns.
# v1.1 — 2026-08-05 — GAP-2026-08-05-001 (textless content is content). S5-2 now takes
#   the BLOCK-level lookahead bc.sorted_body_lookahead(doc) and the per-FILE colour probe
#   bc.heading_colour_available(paras); S5-4b CAUSE 1 split into 1a (gate absent) and 1b
#   (gate present but DEFEATED), because 1a's remedy asked the operator to verify two
#   already-true facts and re-run, which reproduced the halt forever.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
```

## Framework_PYQDeliver.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQDeliver.md.

```
# v1.11 — 2026-08-10 — DOC-CONSISTENCY: completes the v1.9 single-artifact sweep.
#   v1.9 retired the render-source and made the delivered file the ONE artifact, and
#   its changelog claimed it touched "§11 (done + invariants)" and the §7 "both
#   artifacts" prose — but three LIVE lines were missed and still asserted the retired
#   two-artifact model: the §7 C18 one-line summary ("on BOTH artifacts"), §11
#   Definition-of-done item 11 ("machine-verified by C18 on both artifacts"), and the
#   §11 hard invariant ("Both artifacts are schema-valid ..."). The gate_c18 code and
#   the §7 body prose already validate exactly ONE delivered artifact, so behaviour was
#   always correct; only these summary/invariant/done lines contradicted them, and no
#   check catches prose drift. FIX: all three now name "the delivered artifact"
#   (singular). No behaviour, gate, or delivered-byte change — documentation only.
#   Surfaced in the 2026.08.10.1 deployment review; not introduced by v1.10.
#   Touched: §7 C18 summary line, §11 done item 11, §11 hard invariant, END sentinel.
# v1.10 — 2026-08-10 — PYQ REGISTRY IS NO LONGER A PROJECT-FILES DELIVERABLE.
#   ROOT CAUSE of the reported cross-session gap: the registry
#   ([ExamCode]_pyq_registry.json) was the ONLY PYQ-4 artifact whose usefulness
#   depended on the operator MANUALLY uploading it back into the exam project's
#   Files section (old S8-3) — /home/claude and outputs are chat-scoped and
#   /mnt/project is read-only to the engine, so nothing else could persist it.
#   Across the ~200-exam corpus that manual step was skipped routinely, so the NEXT
#   paper's PYQ-4 ran in a fresh chat, found no registry, and — per the old §12
#   case 11 — reset the corpus tally and dropped the duplicate-delivery guard
#   SILENTLY. FIX: the registry is DEMOTED from a required Project-Files deliverable
#   to an OPTIONAL, LOCAL-ONLY, absence-tolerant continuity aid. It is (1) NEVER
#   badged Upload/Replace and NEVER presented as a file to manage in Project Files;
#   (2) READ ONLY IF the operator voluntarily attaches one — absence is the normal,
#   silent, expected state, never a WARN and never a nag; (3) CORRECTNESS-INDEPENDENT
#   — producing the tagged portal file and passing C1–C18 never depends on it, and
#   Definition-of-done no longer lists a registry update as a hard item; (4)
#   BEST-EFFORT — when a prior registry IS attached PYQ-4 still updates it, may emit a
#   LOCAL-ONLY copy, and the duplicate-delivery guard still fires; when none is
#   attached the §R6 line reports current-paper-only totals neutrally. CONSEQUENCE:
#   cross-chat corpus tracking becomes OPT-IN (attach the prior registry) instead of
#   mandatory-upload; the portal deliverable is unchanged. Mirrors Framework_
#   DeliveryFooter v1.16, which places *_pyq_registry.json in LOCAL_ONLY so the badge
#   engine can never route it to Project Files on any step, for any exam. Touched:
#   §0 outputs, §1 step 6, §3 step 3, §8 (open/S8-2/S8-3), §9 (items 2/6), §10 §R6,
#   §11 done item 9, §12 cases 4 & 11, §13 S13-2 table, END sentinel.
# v1.9 — 2026-08-09 — DELIVERED FILE NOW PRESERVES NATIVE OMML — the OMML→Unicode
#   linearization (Rule 19) is RETIRED from the delivery path. ROOT CAUSE of the
#   reported defect: §4-S4-2 named the RENDER-SOURCE artifact (every `<m:oMath>`
#   flattened to a one-line Unicode text run by S6-1/Rule 19) as the delivered
#   `_PYQ_Final.docx`. That silently DESTROYED all structured math — fractions,
#   radicals, integrals/sums, matrices, sub/superscripts — in the portal file
#   (measured on IIT JAM Physics 15-Feb-2026: 856 native `<m:oMath>` in the input,
#   0 in the delivered file). The two-artifact design was justified (S4-1 Fact 1)
#   by python-docx round-trip corruption — but PYQ-4 edits raw document.xml
#   (unzip→XML→zip, §3) and NEVER round-trips through python-docx, so OMML already
#   survives the pipeline byte-perfect: the INTEGRITY artifact proves it (gate C5:
#   integrity OMML count == source). FIX: the INTEGRITY artifact (native OMML, tag
#   blocks inserted, date/session tags removed, NO render transforms) is now THE
#   delivered file. Rule 19 linearization is retired; the render-source is no longer
#   built or delivered. The delivered file is therefore byte-identical to the input
#   except for the two pipeline-mandated edits (§4A date-tag removal + §5 tag-block
#   insertion). CONSEQUENCE: the render-only transforms Rule 21 (non-ASCII safe-font)
#   and Rule 22 (underline recolor) no longer apply to the delivered file — content
#   fidelity supersedes those portal-cosmetic transforms. Math preservation is now
#   gated: C5 (unchanged) guards the delivered OMML count == source, and C11 is
#   INVERTED from "zero OMML in render-source" to "delivered OMML count == source;
#   zero linearization." Mirrors MockDeliver v1.11.0, which fixes the identical
#   defect the same way. Touched: ZERO-MUTATION RULE, §0 outputs, §3, §4 (S4-1/S4-2),
#   §6 (retired), §7 (C11 inverted; C14/C15 repurposed; "both artifacts" prose),
#   §10 §R4/§R5, §11 (done + invariants), §12 case 7, §13 S13-1/S13-2, Appendix A.
# v1.8 — 2026-08-09 — QUESTION TYPE IS NOW POSITION-BASED (three-tier), closing the
#   section-determined-MSQ portal defect for real. SUPERSEDES the aborted v1.7 (never
#   deployed). v1.7 tried to fix this by CONSUMING a `qtype` map it claimed PYQExplain
#   had committed into pyq_explain_progress.json — but PYQExplain (§S7A-4) writes only
#   _meta / q_to_classification / options_by_q / q_to_difficulty; there was no qtype key
#   in the delivered sidecar, so v1.7's Tier 1 never fired and every question fell back to
#   the same structural rule that returned 0 MSQ where 10 were expected. The v1.7 root-cause
#   sentence ("PYQ-4 re-derived a type PYQExplain had already committed into the JSON") was
#   simply false. TRUE ROOT CAUSE: Question Type was being read from section_rules
#   `answer_cardinality`, a SUBTOPIC-scoped corpus statistic that cannot express
#   SECTION-determined MSQ — on IIT JAM Physics 15-Feb-2026 every Section-B subtopic reads
#   'single', so all 10 MSQ (Q31-40) mis-tagged as MCQ. FIX (mirrors the proven MockDeliver
#   v1.7 precedent): S2-2 is now a three-tier resolver whose Tier 1 resolves Question Type
#   POSITION-BASED from exam_config.marking_scheme[].question_type whenever marking_scheme
#   carries more than one distinct question_type — the exam's OFFICIAL, section-scoped
#   type-by-position, a field PYQ-4 already loads (§0 item 2). Tier 2 consumes PYQExplain's
#   now-genuinely-delivered qtype (v2.3+); Tier 3 is the pre-v1.7 structural rule for
#   single-type / subtopic-based exams. Deterministic; on IIT JAM Physics this yields
#   exactly 30 MCQ / 10 MSQ / 20 NAT. Touched: §0 item 2 (third use) + item 8, §1 step 5,
#   S2-1 row 4, S2-2 (rewritten), §10 §R1, S13-2 table. Paired with PYQExplain v2.3, which
#   fixes P4 the same way and delivers qtype as a fourth map.
# v1.6.2 — 2026-08-09 — PYQExplain v2.2.1 delivers the sidecar under the paper-identity stem
#   [ExamCode]_[date]_[session]_pyq_explain_progress.json. §1/§0 now derive the expected sidecar
#   name from the attached docx and load THAT — closing the same-Q_TOTAL collision where the
#   §2-5 coverage gate (1..Q_TOTAL) would pass a wrong-paper map. Legacy bare names → WARN.
# v1.6.1 — 2026-08-09 — PYQExplain v2.2 now DELIVERS pyq_explain_progress.json to outputs.
#   Clarified §1/§0 that the sidecar (q_to_classification + options_by_q + q_to_difficulty)
#   is attached alongside the _PYQ_Explanation.docx. No behaviour change — sourcing unchanged.
# v1.6 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. PYQ-4 now takes PYQ-1's
#   _PYQ_Explanation.docx as its STANDARD input (a legacy _Complete.docx is still
#   accepted, unchanged, but is no longer produced), and reads pyq_explain_progress.json
#   as the primary sidecar for q_to_classification / options_by_q / q_to_difficulty.
#   COMPLEXITY Tier 1 (q_to_difficulty) is now PRODUCER-ONLY: PYQ-2's independent
#   validation (§10A) is gone, so PYQ-4 consumes PYQ-1's assessed values directly after
#   the same membership check (S2-3a). No gate, transform, or delivered byte changes.
#   Edits retire the PYQ-2 input preference and cross-references. Touched: PIPELINE
#   POSITION, §0/§1 input + sidecar priority, S2-3a note, §4A, §5-3, §7 C18 note,
#   §10 §R7, §12 edge cases.
# v1.5.2 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   197 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQDeliver'. The current companion block, the
#   v1.5.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.5.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.2.1, several versions behind the header, so the last line of the file
#   contradicted the first. Documentation only — not one line of behaviour changes. It went
#   unnoticed because BOTH integrity tools were structurally blind to it:
#   validate_framework_md.py Check C recognised only the '# END OF <name> vN' sentinel form
#   and skipped the comparison entirely for the '**End of <name>.md (vN)**' form used here,
#   while audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
```

## Framework_PYQExplain.md

# v2.14 — 2026-08-20 — GAP-2026-08-20-TRANSFER-SAFE-EXPLANATIONS (paired with
#   MockTestExplain v1.36.0, engine v2.7). Same defect class, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.36.0 for the full
#   incident record (a delivered 60-question paper, answer-correct on every item,
#   carrying ~17 sentences true for the item and false for its nearest neighbour).
#   NEW §7-7 transfer-safety protocol (scope → type → neighbour test → repair by
#   mechanism → recorded transfer_record); §8-2 epistemic type + scope-in-sentence;
#   §8-3 topic minimum-concept components (subject data); §8-0b is now an engine
#   gate (undeclared universal raises; kept absolutes declared); §14-1 three-part
#   (TRANSFER-SAFE), §14-5 four-field record; §15-3 MSQ wording WITHDRAWN and
#   rewritten (learner-psychology boilerplate banned by the engine); NEW §6A-1c
#   representation alignment + §6A-3b distribution tripwire; CONFORMER verdict;
#   §24 loads the SUBJECT-level [Subject]_EXPLAIN_LEARNINGS_v*.md (same schema,
#   same parser; precedence exam > subject > spec) + §24-5 defect codes; §5-1/
#   §5-2/§5-3, §18, §R3, §21 hooks. Student-facing format unchanged and LOCKED.
#   SHARED_RULES_VERSION 1.2 → 1.3.
# v2.13 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-EXECUTION-INTEGRITY (paired with
#   MockTestExplain v1.35.0, engine v2.6). Same four defects, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.35.0 for the full
#   incident record (a delivered 60-question paper, audited).
#   D1 — the §9 error type becomes INTERNAL metadata: still mandatory, recorded per
#   wrong option / pitfall in progress state, and the visible line delivers the same
#   diagnosis in natural language — never the snake_case token. Engine v2.6 raises at
#   write time on any taxonomy token in student-facing text and re-scans the rendered
#   bytes at verify time.
#   D2 — NEW §6A-1b structure-answer presumption + verdict↔emission coherence: when
#   the verified answer IS a structure, STRUCTURE_GRAPH is presumed and PROSE needs a
#   recorded justification; §6A-3 passes the verdict INTO the block (engine v2.6
#   representation_verdict) and a visual verdict with zero figures raises; a §6A-4
#   degrade records the DEGRADED requirement. PYQ-SPECIFIC: VOID_ITEM WINS — §6A-2b
#   forbids any generated figure for a VOID_ITEM, so the presumption is void for it
#   by construction.
#   D3 — NEW §14-5: SPEED-HACK eligibility recorded per question, the inclusion RATE
#   reported in §R3, and an all-hack batch re-runs the §14-1 test before §18 — a
#   tripwire, never a quota (reference incident: a hack on 56 of 60 questions).
#   D4 — NEW §7-0c enumeration-before-formula and §7-6 decisive-claim consistency
#   (a right answer with contradictory reasoning is invalid; repair returns to §7-1,
#   never to patched prose). Both domain-neutral per the v2.11 convention.
#   RE-6d added; RE-13 restated in both files; SHARED_RULES_VERSION 1.1 → 1.2.
#   ALSO: the stale "currently 64/64" aside in MANDATE A is removed — the §21-0
#   class (an exact count asserted in prose is wrong from the next fixture on; the
#   engine prints a higher count today and the gate is floor-form anyway).
#   ENGINE FINDINGS (v2.6, from writing its fixtures): the v2.3/v2.7 figure-validation
#   loop sat AFTER the NAT branch's return, so NAT figures were never validated at
#   construction — moved above the type split; anomaly blocks now reject figures as
#   student content; an AXIOM naming an option label raises (§8-2).
# v2.12 — 2026-08-19 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT (paired with
#   MockTestExplain v1.34.0, engine v2.5). SPEC-ONLY. P6's conflict check compared
#   Q_TOTAL, option count, question type and opt_re-vs-label_scheme, but never compared
#   the DECLARED `option_label_format` values against each other — and section_rules
#   declares that value once in the CATEGORY C header and once per SECTION block, from
#   two different generators. A header/section disagreement therefore passed silently and
#   every option carried the wrong label. P6 now compares all declarations and HALTs on
#   any disagreement, printing each value with its location. See MockTestExplain v1.34.0
#   for the full incident record.
# v2.11 — 2026-08-19 — GAP-2026-08-19-DOMAIN-LEAK-IN-UNIVERSAL-RULES (paired with
#   MockTestExplain v1.33.0). SPEC-ONLY, no engine change, no rule weakened. The four
#   rules added in v2.9/v2.10 were written in one domain's vocabulary inside an
#   exam-agnostic spec: §7-0a/§7-0b listed domain-specific conditions and assumptions as
#   though universal, §7-5 made domain-specific checks MANDATORY, and §8-0a banned
#   domain-specific quantities. Rules are now stated neutrally, lists are ILLUSTRATIVE and
#   read from the exam's own material, and every §7-5 check is CONDITIONAL ON
#   APPLICABILITY. See MockTestExplain v1.33.0 for the full record.
# v2.10 — 2026-08-19 — GAP-2026-08-19-CONDITIONAL-CORRECTNESS (paired with
#   MockTestExplain v1.32.0). SPEC-ONLY. Same four rules, so both explanation paths hold
#   one standard; see MockTestExplain v1.32.0 for the full incident record.
#   §7-0a CONDITION CAPTURE · §7-0b ASSUMPTION LEDGER · §7-5 NUMERICAL VERIFICATION ·
#   §14-3b SHORTCUT VALIDITY DOMAIN.
#   PYQ SHARPENS §7-0a: these are REAL past papers, so a condition the stem supplies was
#   put there by the examining body to DISCRIMINATE. A stated condition that changed
#   nothing in the derivation is strong evidence the question was misread.
# v2.9 — 2026-08-19 — GAP-2026-08-19-EXPLANATION-CONTENT-DISCIPLINE (paired with
#   MockTestExplain v1.31.0, engine v2.4). Same three defects, same fixes, so the two
#   explanation paths hold one standard. See MockTestExplain v1.31.0 for the full
#   incident record.
#   D1 — NEW §8-0a SUPPORTED VALUES ONLY: every number traces to the stem, a syllabus
#   constant, or a shown derivation. PYQ SHARPENS THIS: these are REAL past papers, so
#   an invented yield or constant does not merely mislead — it misrepresents what the
#   examining body actually asked and what it supplied.
#   D2 — NEW §8-0b CALIBRATED LANGUAGE: absolutes reserved for claims absolute in the
#   subject's own terms; tendencies take calibrated terms.
#   D3 — NEW §12-4 INTERIM COVERAGE BANNER via engine v2.4 set_coverage_banner(), so a
#   mid-run artefact declares its own state wherever it travels. strip_solutions()
#   removes it, keeping the questions-only copy byte-equal to the Row file source.
# v2.8 — 2026-08-19 — GAP-2026-08-19-STALE-PIN-SWEEP (paired with MockTestExplain v1.30.0).
#   SPEC-ONLY, no engine change. Same CLASS as the paired release: an exact self-test
#   count written into prose is correct only until the next fixture is added, and this
#   file carried two such sites after v2.7 de-pinned only the §R1 report line.
#   D1 — §21 DEFINITION OF DONE HARD-PINNED THE ENGINE COUNT. Item 1 read "engine
#   62/62" while the engine prints 78/78 — the failure mode of
#   GAP-2026-08-13-STALE-SELFTEST-PIN, in the place that fix (v2.5, which converted the
#   P0 gate) never reached. Converted to floor form.
#   D2 — THE ENGINE-CAPABILITY REFERENCE WAS INTERNALLY INCONSISTENT. Two adjacent
#   lines described the same engine's two self-tests in two different conventions:
#   `--self-test` pinned "62/62 PASS" while `--self-test-audit` correctly used the
#   floor form "N >= 10". Both now use floor form.
#   NEW §21-0 states the rule as a RULE, matching MockTestExplain §21-0 verbatim in
#   substance, so the two explanation specs cannot drift apart on it.
# v2.7 — 2026-08-19 — GAP-2026-08-19-PYQEXPLAIN-NO-REPRESENTATION-ROUTER. SPEC-ONLY:
#   no engine change. PYQ-1 shares explain_engine.py with TestExplain, so since engine
#   v2.2/v2.3 it has SILENTLY INHERITED the Tier-3 notation guard and the figure-emission
#   surface (RepresentationFigure / ExplanationBlock.figures) — capability with nothing
#   directing its use. Result: every PYQ document stayed prose-only while the Mock path
#   gained schemes, orbital diagrams and rendered equations. This release closes that.
#   NOTE ON SCOPE — §11 IS ALREADY CORRECT HERE AND IS NOT TOUCHED. PYQ-1's S11-1 has
#   always documented the ⟦MATH:…⟧ grammar properly and has always said "guards are
#   region-aware: \\frac inside a region is legal; the _BANNED_LATEX list applies to prose
#   outside regions only". The §11 defect fixed in MockTestExplain v1.27.0 never existed
#   in this file. Verbalised arithmetic is therefore NOT a documented-cause defect here;
#   §6A-2's EQUATION requirement simply makes the existing rule explicit at routing time.
#   D1 — NO REPRESENTATION ROUTER. New §6A, adapted to PYQ (NOT copied): PROSE is the
#   default and a visual is EARNED on the §14 two-part test; renderers are declared per
#   exam in section_rules; degrade is loud. Two PYQ-specific rules that do not exist in
#   the Mock spec: (a) the router runs AFTER §13A transcription, so a figural question is
#   routed from what was actually SEEN, never from the stem text; (b) a VOID_ITEM figure
#   FORBIDS a generated STRUCTURE_GRAPH for that question — no answer is published for a
#   VOID_ITEM at all (§13A-5), so drawing a structure for one would be manufacturing
#   content from an untranscribable source, the precise thing RE-11 forbids.
#   D2 — §6 HAD NO STRUCTURAL OR DERIVATIONAL CLASS. C-STRUCTURAL and C-DERIVATIONAL
#   added; C-FIGURAL made family-aware.
#   D3 — §13 WAS BLIND TO SCIENTIFIC FIGURES. S13-4 defined the figural AXIOM as "the
#   visual rule" — the reasoning-puzzle vocabulary. Split into §13-4a
#   (transformation-puzzle, preserved) and §13-4b (scientific-diagram). PYQ papers are
#   REAL past papers, so this is the more consequential half of the split here: a JAM or
#   GATE stem figure is essentially always a scientific diagram.
#   D4 — §9 forced science distractors into aptitude labels; eight scientific error types
#   added.
#   D5 — §R1 PROVENANCE WAS STALE ("spec v1.1 · engine 62/62" against v2.6 / 78/78) and
#   §R3 had no representation line. Both fixed; the GATES stay floor-form (P0, v2.5).
# v2.6 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: a name is added to this file's executable surface. NO ARTEFACT CHANGES.
#   This spec CALLED present_files() from compiling python while DEFINING it nowhere —
#   a guaranteed NameError the moment that path executes as python. Five such call
#   sites stood across four specs; spec_name_audit_baseline.json had accepted
#   `present_files` as a known-unbound name in all four, which is why the ratchet
#   reported OK for weeks. SAME SHAPE as D2 of
#   GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed the instance and left the
#   class standing. FIX: a CLASS: T stub is declared in this file, matching the
#   corpus's per-file house pattern for CLASS T markers.
# v2.5 — 2026-08-13 — GAP-2026-08-13-STALE-SELFTEST-PIN: the MANDATE-A engine gate pinned
#   the literal "SELF-TEST: 62/62 PASS" while explain_engine.py prints 64/64 — a HALT on
#   every session with a healthy engine. Converted to the FLOOR form (N/N PASS, N >= 62),
#   the AUTH_GATE_FLOOR pattern; same for the --self-test-audit reader pin (>= 10).
# [ExamCode] project | PYQ-1 (PYQExplain) | Exam-agnostic
#
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take a PYQ Row file (.docx, Step 1 output) from Google Drive, INDEPENDENTLY
#   DERIVE the answer to every question, and INTERLEAVE a perfect, highest-standard
#   explanation after each question — without altering one byte of the original paper.
#   Emit [ExamCode]_[date]_[session]_PYQ_Explanation.docx: a 100%-explained, zero-
#   defect learner-facing solution document for that exam sitting.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION (PYQ Explanation Pipeline)
# ════════════════════════════════════════════════════════════════════════
#   PHASE 1 — Already completed (shared with Mock/Test pipeline):
#     Step 1  PYQPrepare    → Row file (Q.1-Q.N, original exam order) → Google Drive
#     Step 2  PYQDraft/Scan/Approve → taxonomy, exam_config.json → project
#     Step 3  PYQSort       → Sorted PYQ docs → Google Drive
#     Step 5  PYQExtract    → section_rules.md + subtopic_manifest.json → project
#
#   PHASE 2 — PYQ Explanation (this pipeline):
#     PYQ-1  PYQExplain      → [ExamCode]_[date]_[session]_PYQ_Explanation.docx  ← THIS STEP
#     PYQ-3  PYQFormat       → [ExamCode]_[date]_[session]_PYQ_Formatted.docx  (student)
#     PYQ-4  PYQDeliver      → [ExamCode]_[date]_[session]_PYQ_Final.docx       (portal)
#     (PYQ-2 PYQExplainAudit was RETIRED in v2.1. PYQ-3 and PYQ-4 are INDEPENDENT —
#     both take PYQ-1's _PYQ_Explanation.docx directly, neither depends on the other.)
#
#   PYQ-1 runs in the [ExamCode] project (exam-specific). It runs AFTER Steps 1-5
#   have produced section_rules.md, subtopic_manifest.json, and exam_config.json.
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. No section name, no subtopic,
#   no question count, no time/marks figure, no option count, no option label, no
#   language, no figural type, no block label is hardcoded. Every such value is READ
#   at runtime from:
#     • question/option counts, Q total → Row file scan + exam_config.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets,
#       OMML_required, option label format, language, block labels/markers, figural
#       object/transformation types, escape tokens, passage word ranges
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, subtopic names
#       → subtopic_manifest.json
#   Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT, CSIR, Banking, RRB, state
#   PSC, or any exam with valid Step 1-5 outputs.
#

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQExplain.md.

```
# v2.4 — 2026-08-10 — AUTHORING-TIME TIER-3 COMPILE GATE (GAP-2026-08-10-EXPLAIN-
#   MATH-DEGRADE-SILENT). Root cause, measured on a real 60-Q paper: every formula
#   was authored as a ⟦MATH:…⟧ region, but many used LaTeX outside the Tier-3
#   grammar (\tfrac/\dfrac, \varepsilon, \vec r / \sqrt3 unbraced, \frac12,
#   \left…\right, \begin{pmatrix}). t3_compile rejected them; per the no-halt render
#   contract add_math_text DEGRADED each to plain text and RECORDED it in
#   T3_STATS['failed'] — shipping raw LaTeX in the document. It was not caught
#   because verify_explanations() REPORTS the degrade ledger through its RETURN
#   value (ok, problems), not by raising, and the §18 self-audit consumed only
#   whether the call raised. TWO GaPS, BOTH now closed, exam-agnostically:
#   (E1 — the permanent fix) ExplanationBlock.validate() now COMPILES every
#   ⟦MATH:…⟧ region via t3_compile and RAISES a ValueError on MathCompileError, so
#   a malformed region fails at CONSTRUCTION and can never reach the renderer.
#   validate() is the one universal chokepoint (every block, every step, BOTH
#   pipelines, all exams, one explain_engine.py under MANDATE A) and it RAISES, so
#   no producer harness can bypass it — mirrors the NAT fail-at-construction posture.
#   (E2 — defence in depth) §18 gains an explicit BLOCKING contract + literal
#   S18-1a HARD-STOP that asserts ok is True AND problems == [] AND T3_STATS
#   ['failed'] is empty, converting the RETURNED ledger into a delivery-blocking
#   condition. Engine self-test unchanged (62/62). Touched: §S5-2, §S11-1, new
#   §S11-1a, §S18-1, new §S18-1a, header + END sentinel + SHARED_RULES_VERSION.
#   ENGINE CHANGE (explain_engine.py): validate()'s per-sentence guard compiles
#   regions and raises; ships with this release (MANIFEST regenerated).
# v2.3 — 2026-08-09 — QUESTION TYPE RESOLVED POSITION-BASED + qtype DELIVERED as a
#   fourth sidecar map. Until v2.2.1, P4 resolved Question Type ONLY from
#   section_rules answer_cardinality (a subtopic-scoped corpus statistic), and the
#   delivered pyq_explain_progress.json carried only three maps — no qtype. On
#   section-determined-MSQ exams (IIT JAM, GATE, …) every subtopic in the MSQ section
#   reads 'single', so P4 built those questions as MCQ and PYQ-4 had no per-question
#   type to consume. P4 now has a Tier 1 that, when exam_config.marking_scheme carries
#   >1 distinct question_type, resolves type POSITION-BASED from marking_scheme[].q_range
#   (mirroring MockDeliver v1.7) — the "set explicitly" mechanism §5-1 names — falling
#   back to the prior structural rule for single-type/subtopic-based exams. The resolved
#   qtype is now RECORDED and DELIVERED (§S7A-4) as the fourth map and coverage-gated at
#   S19-1 check 7. qtype is a structural type, MANDATE-0-safe. Consumed by PYQDeliver v1.8
#   Tier 2. Touched: P4, §S7A-4, §S0-2, §19 S19-1, header + END sentinel.
# v2.2.1 — 2026-08-09 — Fix two v2.2 deployment findings on the handoff delivery.
#   (1) The handoff shipped under a BARE name (pyq_explain_progress.json) with no paper
#   identity, so two papers' sidecars (same exam, different session) collided by filename
#   and the wrong classification map could silently tag a portal. It is now delivered under
#   the SAME [ExamCode]_[date]_[session] stem as the docx, and PYQ-3/PYQ-4 load the
#   identity-matched name derived from the attached docx. (2) S19-1's shutil.copy ran before
#   the checklist and would raise an uncaught FileNotFoundError if the source were missing,
#   making check 6 unreachable; the copy is now guarded so a missing handoff lands as a clean
#   S19-1 HARD STOP. Touched: S0-2, S19-1, S19-2.
# v2.2 — 2026-08-09 — pyq_explain_progress.json PROMOTED to a delivered artifact.
#   Since PYQ-2 retired (v2.1), this JSON is the SOLE metadata source for PYQ-3/PYQ-4,
#   which run in a fresh chat where /home/claude is gone — yet PYQ-1 previously kept it
#   internal, so the user had no way to carry it forward. It is now delivered to
#   /mnt/user-data/outputs on the FINAL batch (100% coverage, all maps complete) as a
#   first-class pipeline handoff. It carries only classification / option-counts /
#   difficulty (NO answer keys — those stay in the never-delivered pyq_answer_keys.json),
#   so it is MANDATE-0-safe. Touched: S0-2, S19-1 (gate now permits the one handoff on
#   the final batch), S19-2 (present_files ships it).
# v2.1 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED from the PYQ pipeline (operator
#   decision). PYQ-1 is now the SOLE producer AND the FINAL self-certifier: its §18
#   self-audit is the only certification this document receives, there is no downstream
#   independent re-derivation or completion gate, and the official-answer-key cross-check
#   (formerly PYQ-2 D4) no longer exists anywhere. Correctness now rests entirely on
#   producer discipline (§7 derive-twice, RE-18 web-verify, §13/§13A view-every-image)
#   plus the engine's write-time shape guarantees. PYQ-3 (PYQFormat) and PYQ-4 (PYQDeliver)
#   now consume PYQ-1's _PYQ_Explanation.docx directly, with pyq_explain_progress.json as
#   the SOLE metadata source. No algorithm, engine, ExplanationBlock field, gate, or
#   delivered byte changes; the edits retire references to the removed auditor and the
#   (now open) learnings feedback loop. Touched: PIPELINE POSITION, CORE PRINCIPLE,
#   §7A recording note, §14 S14-4, §16, §17-3, §18-2, §20 §R8/§R11, §24, Appendix A.
# v2.0 — 2026-08-07 — TIER-3 STRUCTURED MATH (GAP-2026-08-07-EXPLAIN-OMML, remedies E1–E4).
#   Measured on IIT_JAM_PHYSICS 15-Feb-2026 explanations (60 Q, 56 affected):
#   (a) the v1 OMML builders interpolated RAW text into m:num/m:den — schema-invalid
#   XML every Word engine renders as an EMPTY ▯/▯ placeholder, while the verifier's
#   itertext() reader happily read the bare text, so 12 destroyed fractions shipped
#   under green checks (verifier had been loosened to match the producer's bug);
#   (b) the §11 guard understood only digit/digit slashes, so generation evaded it
#   with an ASCII dialect — 234 "÷" fractions, V_B underscores, x^b carets, √( ),
#   combining-character A̅/E⃗ accents — all guard-invisible, all typographically wrong;
#   (c) inherited upstream loss (pre-v2.0 Row files with missing symbols) was
#   faithfully laundered, because the fidelity check compares output to its own input.
#   Fix (all in explain_engine.py — MockTestExplain Step 9 inherits via MANDATE A):
#   E1 builders _r()-wrap + XML-escape all content; verifier check 5 now REJECTS
#   bare-text num/den (the loosened reader is reverted and locked the other way);
#   E2 add_math_text v2.0 dispatches ⟦MATH:…⟧ regions through the SHARED Tier-3
#   compiler (new repo module t3_mathcomp.py, byte-identical to PYQPrepare §S3-5b,
#   drift-locked in the engine self-test) with the same no-halt/no-markup graceful
#   degradation and verbatim Ctrl+F quoting; E3 guard_sentence bans the dialect
#   (÷, ^, _x, √(, combining accents) with the region spelling as the named remedy,
#   and is region-aware (\frac etc. are legal INSIDE regions); E4 new
#   source_math_health() input check names upstream loss in plain words ("re-run
#   Step 1 v2.0 first") before any explanation is generated. Verifier gains Tier-3
#   structural integrity, rendered-dialect residue, and a region ledger + degrade
#   report. Self-test 10 → 24 audit checks incl. a negative-proofed drift lock.
# v1.2.1 — 2026-08-03 — REGRESSION REPAIR (one line; zero rule change).
#   v1.2 was authored from a base predating 2026.08.03.5 and reintroduced a pointer to
#   Framework_MockTestCreateAudit.md, a spec deleted in that release. Restated as
#   audit_canonical.py, which is where the A-NAT-GRADE implementation actually lives.
#   Every §13A figural pre-transcription rule, the P2a preflight, the VOID_ITEM/AMBER
#   routing and the §R12 reporting shape introduced by v1.2 are UNTOUCHED.
#
# v1.2 — 2026-08-03 — §13A FIGURAL PRE-TRANSCRIPTION PASS (new capability).
#   Figural images are VIEWED ONCE, at P2a, and persisted as TEXT. Every batch
#   then reads the transcription instead of re-viewing the image.
#
#   THE DEFECT THIS REPAIRS. `view` is CLASS T (CLAUDE.md EXECUTION-BOUNDARY
#   LAW) and an image held in context is not durable. PYQ-1 previously viewed
#   each figure lazily, inside whichever batch contained it — so the LAST
#   figural batch asked the image channel for a fresh render after a clone, a
#   bootstrap, two specs read in full (RULE 2), and five prior batches. Measured
#   in one session on pixel-verified non-blank files: early views returned
#   perceptible content, later views on the SAME files returned empty payloads,
#   and a retry did not recover. The failure then surfaced as a HALT inside
#   Batch 1 rather than at preflight, and §13 offered no sanctioned path
#   onward — the CERTIFIED-DEGRADED (VISION) route in DeliveryFooter §5 Q0b was
#   scoped to Step 8 only.
#
#   THREE PROPERTIES, ALL NEW. (a) Vision is spent at the EARLIEST executable
#   moment, when context is lightest. (b) What was seen becomes durable text on
#   disk, so a figure is viewed exactly once per paper no matter how long the
#   run or how many resumes it survives. (c) A dead image channel is detected at
#   P2a in seconds, by measurement, instead of as a mid-batch halt.
#
#   IT NEVER HALTS. CLAUDE.md: "A CLASS T failure must be LOUD, and must NOT
#   halt." An untranscribable figure makes its question VOID_ITEM and the run
#   AMBER; the paper still completes, still delivers every other question, and
#   still ships. BLOCKING is never emitted for a vision condition. This aligns
#   PYQ-1 with the corpus rule that no rendering/observation condition may stop
#   a paper, and DeliveryFooter v1.11 extends Q0b to carry the amber.
#
#   RE-11 IS NOT WEAKENED — IT IS MOVED EARLIER AND MADE AUDITABLE. A figural
#   answer is still derived only from what was actually seen. What changes is
#   that "what was seen" is now a recorded artefact a later step can inspect,
#   rather than a claim about a context window nobody can re-examine. A question
#   whose figure was never legibly seen now yields NO published answer, where
#   before it yielded a halt (best case) or an unfalsifiable assertion (worst).
#
#   Zero changes to explain_engine.py (62/62 unchanged), the ExplanationBlock
#   model, the delivered document, §12 byte-identity, or any existing gate.
#   New engine: figural_vision.py (pure stdlib, Phase A/C only — it models no
#   tool call and contains no CLASS T stub).
#
# v1.1.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   29 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQExplain'. The current companion block, the
#   v1.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.1 — 2026-07-24 — §7A PER-QUESTION DIFFICULTY ASSESSMENT (new capability).
#   PYQ-1 becomes the SINGLE PRODUCER of per-question difficulty for the PYQ
#   pipeline. It emits `q_to_difficulty` into pyq_explain_progress.json; PYQ-2
#   validates it; PYQ-4 consumes it as Tier 1 of its §2-3 resolver.
#
#   WHY HERE AND NOWHERE ELSE. Difficulty for a PYQ paper is a MEASUREMENT, not a
#   choice: the exam body already wrote the questions, so the label must follow the
#   content. Only a step that READS AND SOLVES a question can measure what it
#   demands — and PYQ-1 is the only step in this pipeline that does. PYQ-4 tags
#   from a document it never solves, which is why its Tier 2 keyword scorer
#   (E-9) collapsed an entire IIT JAM Biotechnology paper to one label: 60 of 60
#   questions "Easy", with E-9's computation axis at its floor for all 60. No
#   keyword list fixes that, because a keyword list is exam-SPECIFIC and this
#   framework serves ~200 exams.
#
#   NO NEW COGNITIVE WORK. §7A does not analyse anything. Every input it reads is
#   an observation PYQ-1 has ALREADY made by the time it runs: the §6 class, the
#   DEDUCTION step count it just built, the AXIOM principle count it just wrote,
#   whether the §14 SPEED HACK gate passed, whether §7's two methods agreed, the
#   §10a negative-phrasing scan, and the §5-1 qtype. The assessment is a pure
#   function of those observations, evaluated by blueprint_core.assess_difficulty.
#
#   DETERMINISM CONTRACT. The scoring function is pure and deterministic: identical
#   observations always yield the identical label. The observations themselves come
#   from model derivation, so a FRESH PYQ-1 run on the same paper may observe a
#   different step count and produce a different label. That is bounded and
#   acceptable because the value is WRITTEN ONCE to the progress JSON and every
#   downstream reader performs a pure lookup — PYQ-4 §S2-3d's guarantee that "no
#   model judgment participates in tag resolution at PYQ-4 time" stays literally
#   true. (v2.1: PYQ-2's independent check on this value is retired — the difficulty
#   label is now producer-only.)
#
#   Zero changes to explain_engine.py. Zero changes to the ExplanationBlock model,
#   the delivered document, or any existing gate. The assessment is metadata only
#   and is NEVER rendered into the paper.
#
```

## Framework_PYQFormat.md

Moved from the file header at framework release 2026.08.15.14; v1.5.2 entry moved at 2026.09.03.3.
Current-version entry remains in Framework_PYQFormat.md.

```
# v1.5.2 — 2026-08-09 — PYQExplain v2.2.1 delivers the sidecar under the paper-identity stem
#   [ExamCode]_[date]_[session]_pyq_explain_progress.json. §1/§0 now derive the expected sidecar
#   name from the attached docx and load THAT (prevents a colliding sidecar from another paper
#   silently supplying the classification map). Legacy bare names accepted with a WARN.
# v1.5.1 — 2026-08-09 — PYQExplain v2.2 now DELIVERS pyq_explain_progress.json to outputs.
#   Clarified §1/§0 that the sidecar is attached alongside the _PYQ_Explanation.docx (both
#   are PYQExplain deliverables). No behaviour change — the sourcing priority is unchanged.
# v1.5 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. PYQ-3 now takes PYQ-1's
#   _PYQ_Explanation.docx as its STANDARD input (a legacy _Complete.docx is still
#   accepted, unchanged, but is no longer produced). q_to_classification is read from
#   pyq_explain_progress.json as the primary sidecar. No runtime behaviour changes —
#   PYQ-3 never audited; it formats whatever it is given. Edits retire the "certified by
#   PYQ-2" framing (the input is now producer-certified by PYQ-1's self-audit, not independently
#   audited) and the PYQ-2 cross-references. Touched: PURPOSE, ZERO-MUTATION rationale,
#   §0/§1 input contract + map priority, §4, S7-2, §9/§10 notes, §12 edge cases.
# v1.4.2 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   173 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQFormat'. The current companion block, the
#   v1.4.1 entry, and all structural notes remain in-file. Body byte-untouched.
# v1.4.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.3, several versions behind the header, so the last line of the file contradicted
#   the first. Documentation only — not one line of behaviour changes. It went unnoticed
#   because BOTH integrity tools were structurally blind to it: validate_framework_md.py
#   Check C recognised only the '# END OF <name> vN' sentinel form and skipped the
#   comparison entirely for the '**End of <name>.md (vN)**' form used here, while
#   audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
```

## Framework_PYQPrepare.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQPrepare.md.

```
# v2.0 — 2026-08-07 — TIER-3 STRUCTURED MATH (GAP-2026-08-07-OMML, remedies M1/M2/M4/M5).
#   Root cause (measured on IIT_JAM_MATHEMATICS 15-Feb-2026, 60 questions): S1-13
#   emitted FLAT Unicode transcription, destroying 2-D math structure at capture
#   time; Tier-2 regex reconstruction then recovered only digit fractions and √N.
#   Result classes: letter-fraction flattening, ^/_ artefacts, inline big-operator
#   limits, cases/matrix structures PARAPHRASED into prose (Q.11/14/17/33/34/36/
#   37/49/52/56), hybrid-font islands, and the bare-label OMML option conflict.
#   Fix: (M1) S1-13 now REQUIRES ⟦MATH:…⟧ LaTeX-lite regions for all structural
#   math and BANS paraphrasing matrices/vectors/cases into prose, with declared
#   STRUCT_FLAGS; (M2) new S3-5b deterministic LaTeX-lite→OMML compiler (fractions,
#   radicals, scripts, n-ary with true operands, limLow, cases, matrices, sPre,
#   stretchy delimiters, accents, \binom, Greek/symbol map; STRICT CORE with a
#   FORGIVING BOUNDARY — a region the compiler rejects never halts the run and
#   never ships silently: it is delivered as ordinary plain text — no colour,
#   no highlight — and CHECK 20 quotes it verbatim for Ctrl+F, with the remedy
#   in plain operator words, under an F1 AMBER footer);
#   render_text_with_math() v2.0 dispatches Tier-3 regions first and
#   keeps the v1.5 legacy path byte-compatible for plain segments; (M3, in
#   corpus_io Cluster I) text_of() = w:t + m:t canonical accessor; CHECK 9 v2
#   accepts bare "N." labels whose payload is <m:oMath> (producer mirror of S-1);
#   (M4) CHECK 19 structure-residue, CHECK 20 region round-trip, CHECK 21 declared-
#   structure fidelity — 18 -> 21 checks; (M5) S4-1: OMML runs keep the Word math
#   font (Cambria Math italic), EXEMPT from the Arial rule.
#   Verified: 60-question rebuild, 142/142 regions compiled, 21/21 checks, page-
#   for-page structural render match against the source PDF.
# v1.14.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   317 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQPrepare'. The current companion block, the
#   v1.14 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.14 — 2026-07-29 — DI TABLE STRUCTURE, BLOCK COMPOSITION AND CELL CONTENT
#           (GAP-2026-07-29-TBL). This spec could say what a table CONTAINS and never
#           what a table IS. S1-12 CATEGORY 2 transcribed "a list of rows" and S4-3
#           wrote cell.text into a rectangular add_table(), so a grouped header had
#           exactly one representable form: squared into a grid and padded with empty
#           strings. Measured on SSC_CGL_Tier1 09-Sep-2024 Shift 1 — Q.52 and Q.61 each
#           lost a 4-column header span and a 2-row label span and gained 4 stray empty
#           cells, while Q.74 passed because ITS header is flat. That is why the gap
#           survived to v1.13: the worked example in S1-12 and in EC-P20b is flat too,
#           so a model that cannot express a span was never once exercised against one.
#           The delivered Row file carried 0 gridSpan and 0 vMerge elements and passed
#           16/16 checks with a green F2 footer, because no check in this framework has
#           ever compared a built table with its source.
#           SECOND DEFECT, SAME FAMILY: S1-7 and S4-2 emitted one table PER OPTION, and
#           two adjacent w:tbl siblings are FUSED into a single table by every Word
#           engine. Measured: 19 tables as written came back from a Word-engine
#           round-trip as 7. It is invisible in the emitted file — python-docx reports
#           19 — which is why it went unnoticed for the life of the spec.
#           Fix: (1) new S1-8a TABLE STRUCTURE CONTRACT — the TableSpec model, anchor
#           cells with cs/rs, padding BANNED; a blank cell is now distinguishable from
#           padding STRUCTURALLY rather than by heuristic.
#           (2) S4-3 build_di_table DELEGATED to corpus_io (Cluster I) — HTML-style
#           occupancy placement, cell.merge() strictly AFTER text placement (merge
#           CONCATENATES: 'A'+'B' -> 'A\nB'), per-cell column widths, centred default.
#           Two builders modelled one concept and both were flat; one model, one owner.
#           (3) S1-6 and S1-11 scope EXTENDED to table cells — cells now render through
#           render_text_with_math, so a fraction, a superscript or an underlined term
#           inside a DI table is no longer silently flattened. That is the v1.3-v1.6
#           math defect, relocated into tables and unaddressed until now.
#           (4) new S1-8b BLOCK COMPOSITION — no two adjacent block tables; a figure-
#           option SET is ONE table with one row per option, which is also the better
#           match for the ALL-or-NONE rule in S1-7.
#           (5) new S2-2 CALL A2b — text-layer tables are DETECTED and transcribed
#           instead of being parsed as stem prose. S1-12 fires only on embedded images,
#           so a vector-drawn DI table in a FORMAT A source never entered the table
#           protocol at all.
#           (6) new CHECK 17 (geometry equality, declared vs built), CHECK 17b (padding
#           signature, legacy path only), CHECK 18 (no adjacent block tables).
#           16 -> 18 checks.
#           (7) new EC-P24 (table structure, 8 sub-scenarios) and EC-P25 (adjacent
#           block tables). EC-P14 and EC-P20b rewritten; "preserve source data exactly"
#           governed VALUES and was silently read as covering STRUCTURE.
#           (8) an unrepresentable structure is REPORTED, never silently normalised —
#           the EC-V8 / EC-P22 principle extended from images to tables.
#           REQUIRES corpus_io with Cluster I table structure (normalise_table_spec,
#           place_cells, build_di_table, read_table_spec, adjacent_table_pairs) AND the
#           anchor-only _table_rows. Shipping the writer without the reader turns lost
#           geometry into DUPLICATED header text in every consumer: python-docx
#           row.cells returns one entry per GRID COLUMN and repeats the anchor for every
#           covered position. The two halves ship together.
```

## Framework_PYQScan.md

Entry v1.3 moved at framework release 2026.08.22.2 (EC-P42 — PYQScan-route
headroom, flagged +809 B by the 2026.08.21.4 deploy review). Current-version
entry remains in Framework_PYQScan.md.

```
# v1.3 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: adds a CLASS: T stub for present_files(). NO ARTEFACT CHANGES.
#   It was CALLED from compiling python here while DEFINED nowhere — a guaranteed
#   NameError; spec_name_audit_baseline.json had accepted it as known-unbound in all
#   four affected specs, so the ratchet reported OK.
#   FULL NARRATIVE: SPEC_HISTORY.md + CHANGELOG.md 2026.08.16.2.
```

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQScan.md.

```
# v1.2 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (D5).
#   collect_row_files() was `files = []` … `pass  # Drive MCP calls` … `return files`:
#   it returned an EMPTY LIST unconditionally, on every run of every exam, and its own
#   comment cited "the same pattern as Step 5's S1-2 Drive path" — inheriting a pattern
#   that was itself dead. Invisible to C6 twice over: the `pass` shares its body with
#   other statements so it is not a pass-bodied stub, and it carried no CLASS tag. The
#   listing now delegates to corpus_io.collect_corpus_files over a PHASE A cache keyed
#   by folder id, and an empty result HARD STOPS with a transport diagnosis (EC-P39)
#   instead of silently reporting a Row-file-less exam.
# v1.1 — 2026-08-15 — GAP-2026-08-15-BAREQ. S3-2 Q_PATTERNS mirrors the engine's widened
#   four-entry table (entries 3/4 = BARE-LABEL forms), updated atomically with
#   blueprint_core, PYQSort S3-1 and MockTestAnalyse E-2. S3-2 now PERSISTS q_count and
#   q_count_method into every drive_file_inventory[] entry: the "MANDATORY GATE" computed
#   a check-verified per-file count, displayed it and DISCARDED it, so the one number that
#   would have caught this defect in two seconds (56 parsed vs 60 classified on
#   IIT_JAM_MATHEMATICS 12-Feb-2017) existed, was correct, and was thrown away. NEW S3-3
#   step 1b: assert len(classifications[paper]) == inventory[paper].q_count — HARD STOP on
#   mismatch, WARN when the count came from a filename or the field is absent.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
```

## Framework_PYQSort.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_PYQSort.md.

```
# v1.19.0 — 2026-08-05 — GAP-2026-08-05-001. CHECK 11 DOWNSTREAM-PARSE ROUND TRIP added
#   (HARD FAIL, D3/SG-5): PYQSort now re-reads its own delivered file with the DOWNSTREAM
#   predicate and asserts inferred headings == emitted headings, plus the heading-colour
#   styling assertion (SG-10). S6-2 LEVEL 3 parser line amended (SG-9): it mandated
#   11pt Bold Navy #003366 and then told the parser "default -> level 3", i.e. to ignore
#   the marker the same clause guarantees — the root cause of all three heading defects.
# v1.18.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   307 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQSort'. The current companion block, the
#   v1.18 entry, and all structural notes remain in-file. Body byte-untouched.
#   v1.18 — 2026-07-27 — THE ORIGINAL EXAM POSITION SURVIVES SORTING (GAP-2026-07-27-E).
#           Step 3 renumbers questions into TAXONOMY order. That is correct and stays —
#           but it destroyed the EXAM position, and nothing downstream could recover it.
#           Step 5's MSQ detector had only the instruction phrase left to work from and
#           measured 24 MSQ across 1,719 questions on an exam whose marking scheme
#           reserves Q31-40 for MSQ (~10/paper, so ~120 in the current era alone).
#           Section B was therefore under-represented corpus-wide, Step 6 under-allocated
#           it and Step 7 under-produced MSQ — surfacing two steps later as unexplained
#           Section B feasibility pressure in MockBlueprint.
#
#           This is the class of defect that CANNOT be fixed where it is observed. The
#           information does not exist by the time Step 5 runs, so Step 5 had nothing to
#           be smarter about. The fix belongs at the point of destruction.
#
#           CHANGE: the date label — rebuilt on every emit, never cloned, and already
#           parsed by Step 5 — now carries a trailing " Q<N>" holding the original
#           position. No new artefact, no new parser, no schema migration.
#             * build_date_label_re(): the Q-part is OPTIONAL, so every sorted file
#               produced before v1.18 still parses BYTE-IDENTICALLY. No exam is forced
#               to re-sort; each gains positional typing when next sorted.
#             * parse_original_q_num(): new. Kept SEPARATE from parse_date_label(),
#               whose 4-tuple return is the sort key and is consumed positionally in
#               several places — widening it would be a silent breaking change.
#             * stamp_original_q_num(): new, IDEMPOTENT, so a re-emit cannot produce
#               "[... Q37 Q37]".
#             * Both DELEGATE to corpus_io Cluster Q (>= v1.9). Step 3 WRITES this stamp
#               and Step 5 READS it — precisely the two-spec shape that produced the
#               is_option drift v1.17 had to unwind, where each file's docstring asserted
#               alignment with the other and both were wrong. One definition in the
#               engine; drift impossible by construction, not asserted by comment.
#           A None result means UNKNOWN — a pre-v1.18 file, or a position no band
#           covers — and callers must never read it as position 0.
#
```

## Framework_ScopedBlueprint.md

Moved from the file header at framework release 2026.08.15.14.
Current-version entry remains in Framework_ScopedBlueprint.md.

```
# v1.7.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   105 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_ScopedBlueprint'. The current companion block, the
#   v1.7 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v1.7 — 2026-07-21 — HARDENING PASS on v1.6 (line-by-line adversarial re-audit, 2 passes,
#   found and fixed 3 real issues before any downstream reliance):
#   (1) ENVELOPE COMPUTATION WAS NOT ACTUALLY GATED — S5-1's prose claimed "S5-1/S5-2 are
#       SKIPPED entirely" under override_mode, but the v1.6 code had `ENVELOPE =
#       scope_envelope()` as an unconditional top-level statement — true only in the sense
#       that Branch B's math never READS ENVELOPE, not that it's never COMPUTED. Fixed:
#       `ENVELOPE = scope_envelope() if not override_mode else None` (S5-2), and merged the
#       former S5-3a/S5-3b into a single S5-3 with an explicit `if override_mode: ... else:
#       ...` — mirroring the mock's own proven S7-5 unified-branch pattern exactly, so there
#       is zero ambiguity about which branch runs and ENVELOPE is never touched in Branch B.
#   (2) STALE DUPLICATE CLAIM IN §10 DoD ITEM 11 — a second, independent occurrence of
#       "difficulty ... from the Step-5 outputs" (absolute, pre-v1.6 wording) survived in the
#       Definition-of-Done checklist even after the same claim was corrected in the
#       EXAM-AGNOSTIC GUARANTEE paragraph at the top of the file. Fixed: item 11 now states
#       difficulty may come from Step-5 outputs OR the trigger override, matching the header.
#   (3) NO CATCH-ALL FOR MALFORMED --difficulty VALUES — S1-1 defined 'progressive', a valid
#       S:M:H ratio, and "neither given", but not a value that is neither (typo, wrong count
#       of numbers, non-numeric). Added an explicit ERROR path naming the accepted formats.
#   Verified: validate_framework_md.py 0 issues (24/24 AST-clean); both S5-3 branches
#   extracted and literally executed against 5 edge cases (uniform override, full-bypass
#   100:0:0, N=1, non-divisible Q rounding, N=200 uniformity, plus a Branch-A ramp regression
#   and single-level-envelope degenerate case) — all assertions held, zero errors. Full
#   before/after SHA256 diff of all 21 OTHER tracked files in the corpus confirmed untouched.
#
```

---

# END OF SPEC_HISTORY v1.0

## Framework_PYQCore.md — texts superseded by v1.7 (GAP-2026-08-30-TYPE1-HALT-ELIMINATION, 2026-08-30)

### S2-3 PROOF OF CORRECT TOPIC COUNT (v1.6 form — the stranded pre-v1.1 absolute rule; RPSC_ZOOLOGY root cause 1)
```
  PROOF OF CORRECT TOPIC COUNT (self-check):
    After Topic derivation, count the Topics per section.
    If a section has ≤ 4 Topics but the syllabus listed 10+ items → Topics
    are over-aggregated. Re-derive. The syllabus items ARE the Topics.
```

### S2-3 GROUPING Arithmetic example (v1.6 form — superseded per DECISION D8: the example produced exactly the 11-items-one-Topic shape the density check rejects)
```
    Example: "Percentage, Ratio, Average, Interest, P&L, Discount,
             Partnership, Mixture, SDT, Time & Work, Pipes & Cisterns"
             → Topic "Arithmetic" with each item as a subtopic.
```

### S2-3 CATCH-ALL PROHIBITION SELF-CHECK (v1.6 form — HARD STOP on Claude's own output, retired per GATE-AT-SOURCE LAW rule 2)
```
    SELF-CHECK: after completing Topic derivation for a section,
    scan all Topic names against the banned patterns. If ANY match
    → HARD STOP. Re-derive those items as individual Topics.
```

### S2-3 NAME-SHAPE SELF-CHECK HARD branch (v1.6 form — same retirement)
```
          if verdict == 'HARD':
              HARD STOP: f"Name-shape violation: '{name[:60]}' — {reason}. "
                         f"Re-extract this item as a proper taxonomy label, not a question."
```

### question_shape_verdict length branch (v1.6 form — bare 80 bound, superseded by min(80, bc.MAX_HEADING_LEN))
```
    if len(n) > 80:
        return ('HARD', f'{len(n)} chars — far longer than any taxonomy label')
```

### STEP 3 ratio guardrail (v1.6 form — dead-stop, retired per GATE-AT-SOURCE LAW rule 2)
```
      ratio > 3.0  → HARD STOP. Print:
        "Taxonomy inflation ratio = [X]× exceeds 3.0× guardrail.
         Over-fragmentation will cause classification failures.
         Re-derive taxonomy with fewer splits."
```

### STEP 3 CATCH-ALL NAME CHECK (v1.6 form — same retirement)
```
    CATCH-ALL NAME CHECK (mandatory):
      Scan ALL Topic and Subtopic names against the banned patterns
      from the CATCH-ALL PROHIBITION rule (above). If ANY match →
      HARD STOP. Re-derive those items as individual named Topics/Subtopics.
      This check runs AFTER all other quality gates.
```

### §12 Phase 0a DoD ratio line (v1.6 form)
```
  ☐ Ratio guardrail passed: total_subtopics / syllabus_entries ≤ 3.0×
```

## Framework_PYQDraft.md — texts superseded by v1.1.0 (GAP-2026-08-30-TYPE1-HALT-ELIMINATION, 2026-08-30)

### S2-3f attempts + operator message (v1.0.1 form — the two-attempt "re-run and report" dead end; halts #7/#8's root, retired per GATE-AT-SOURCE LAW rule 4 in favor of the 3-round constraint-carrying loop with AMBER exhaustion)
```
  ATTEMPT 2 — if it still fails, re-derive that subject's mapping from S2-3.

  AFTER 2 FAILED ATTEMPTS — stop. Do NOT loop, do NOT save a partial draft,
  and do NOT surface the exception. Print the operator message below.

OPERATOR MESSAGE (plain language, closed set — this is the ONLY form in which
this failure may reach the operator):

  "Step 2a could not complete. The syllabus mapping has an issue I could not
   resolve automatically.

   WHAT HAPPENED:
     [one plain line per error, max 5, jargon removed]

   This is a taxonomy build issue, not something you did, and not something
   you need to evaluate.

   YOUR NEXT ACTION (1 step):
   1. Re-run: PYQDraft [ExamCode]
      If it fails again, report the WHAT HAPPENED lines above."

  No traceback. No field names. No stack. No request to judge anything.
```
