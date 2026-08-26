# Framework_DeliveryFooter v1.28 — Universal Delivery Footer (F1/F2) Contract
# v1.28 — 2026-08-26 — GAP-2026-08-26-REPAIR-BATCH-LAW (MockTestCreate v5.74): STEP 7-R
#   batched — F1 per non-final batch with _Create_Repaired_PARTIAL_[k]of[K].docx
#   (registry withheld), F2 at the final batch. LOCAL_ONLY gains the PARTIAL pattern.
# v1.27 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (MockTestCreate v5.73,
#   MockTestExplain v1.46.0, MockDeliver v1.16.0, paper_pipeline v5.74). NEW §8
#   REGISTRY-HANDOFF-LAW; §3 Step 7 drops the dossier, Step 9 final delivers registry
#   (Replace) + Explain_Report.docx, NEW STEP 7-R / 9-R, Step 11 delivers a healed
#   registry; §6 repair path. Full text: SPEC_HISTORY.md.
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_DeliveryFooter.md" — superseded
#   entries are moved there VERBATIM (EC-P42): this file rides on every route, so every
#   header byte is paid by every session. The CURRENT entry stays above (Z-VERSION).
---

## §1 — FOOTER TYPES

> NOTE (v1.5): The "VISUAL IDENTITY" blocks in this section describe the RETIRED
> widget rendering and are kept only for historical context. The AUTHORITATIVE
> rendering is now §4 (pure Markdown, green/amber emoji color themes, zero external
> tools). Read §1 for WHEN-TO-SHOW and CRITICAL RULES; ignore its widget CSS/icon
> lines and follow §4 for how the footer actually looks.

Two visually distinct footer types. They MUST look different enough that
any team member can distinguish them at a glance without reading text.
(In §4 this is achieved by a GREEN emoji band + ✅ for complete vs an AMBER
emoji band + ⏳ for in-progress.)

### F1 — Mid-step footer (amber/warning)

```
WHEN TO SHOW:
  The step has MORE parts/batches remaining after this delivery.
  Examples:
    - Step 2b PYQScan: after each non-final batch
    - Step 5 PYQExtract: after each non-final batch
    - Step 6 MockBlueprint: after B1 or any B2 batch (B3 not yet done)
    - Step 7 MockCreate: after each non-final batch

VISUAL IDENTITY (superseded by §4 — see note above):
  - Theme        : AMBER (🟨 band, ⏳ header icon)
  - Header text  : "Step [N] · [StepName] — In progress"
  - Bottom strip : "Type continue to generate batch [X+1]. Step not yet complete."

CRITICAL RULES:
  - NEVER say "Start a new chat" — continuation happens in the same chat.
  - NEVER show the "Execute next step" line.
  - If the exact total parts is unknown (e.g., PYQScan where total batches
    depend on corpus size), use: "Step [N] in progress — batch [X] complete"
    without the "of [Y]" part (and omit the batch progress bar).
```

### F2 — Step-complete footer (green/success)

```
WHEN TO SHOW:
  The step is FULLY complete — all parts/batches done, all files delivered.
  This is the absolute final delivery of the entire step.
  Examples:
    - Step 2a PYQDraft: after delivering taxonomy_draft + exam_config
    - Step 3 PYQSort: after delivering the sorted docx
    - Step 5 PYQExtract: after final batch + auto-synthesis + the full final set (S11-3)
    - Step 6 MockBlueprint: after B3 final delivery of all 5 files
    - Step 11 MockDeliver: after delivering the tagged docx

VISUAL IDENTITY (superseded by §4 — see note above):
  - Theme        : GREEN (🟩 band, ✅ header icon)
  - Header text  : "Step [N] · [StepName] — Complete"
  - Bottom strip : "Execute next step: Step [N+1]: [StepName] in a new chat. Thank you!"

SPECIAL CASE — Steps 5 and 6 are parallel:
  Step 5 complete → next callout points to "Step 6: MockBlueprint (if not already complete)".
  Step 6 complete → next callout points to "Step 7: MockCreate M1 (ensure Step 5 outputs
                     are also in project Files)".

SPECIAL CASE — Step 11 (last step):
  Next callout becomes "Pipeline complete for [ExamCode] Mock [N]" (see §4-1 Step 11 variant).
```

---

## §2 — ACTION BADGES

Each deliverable file gets one of three action badges. The badge is
determined by checking whether the file already exists in the project's
Files section at the time of delivery.

### Badge types

```
BADGE 1 — "Upload to Project Files"   (icon: 📤)
  When   : File does NOT exist in project Files yet.
  Example: First-time PYQDraft delivering exam_config.json.

BADGE 2 — "Replace in Project Files"  (icon: 🔁)
  When   : File ALREADY exists in project Files (prior run or prior part).
  Example: Step 4 PYQCount re-delivering updated PYQ_Analysis.docx.
           Step 6 B2 re-delivering updated blueprint.json (B1 version exists).
           Step 7 / 7-R / 9 / 9-R re-delivering the updated registry.json
           (REGISTRY-HANDOFF-LAW, §8 — every step that changes it).

BADGE 3 — "Use locally"               (icon: 📁)
  When   : File is NOT meant to be uploaded to project Files.
  Example: blueprint.xlsx (not readable by Claude in project knowledge).
           Sorted PYQ .docx (goes to Google Drive, not project Files).
           PYQ_Frequency.xlsx (reference only).
```

### Badge determination logic

```python
# ── present_files — THE SINGLE DECLARATION ───────────────────────────────────
# GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3). This file is on every route, so the
# CLASS T delivery primitive is declared here ONCE and every spec inherits it. It had
# been CALLED from compiling python at five sites in four specs and DEFINED nowhere
# (a guaranteed NameError); audit_callgraph C12 fails the build on a new one. Full
# narrative: SPEC_HISTORY.md / CHANGELOG.md 2026.08.16.2.

def present_files(paths):
    """CLASS: T — the chat file-delivery tool. NOT executable python.

    GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), class sweep. Declared per-spec,
    matching this corpus's CLASS T house pattern (gdrive_search is declared in both
    Framework_MockTestAnalyse.md and Framework_PYQCount.md). The F1/F2 contract is
    owned by Framework_DeliveryFooter.md. The model performs the call in its own
    turn; nothing returns to python and no call site may consume a result (C6).
    """
    pass  # CLASS: T — performed by the model between turns, never from python


# Pseudocode — Claude evaluates this mentally before rendering footer

def get_badge(filename, step, is_first_run):
    """
    Returns: 'upload' | 'replace' | 'local'
    """
    # Files that NEVER go to project Files
    LOCAL_ONLY = {
        '*_[0-9]*-*-[0-9]*.docx',  # Step 1 Row files (go to Drive or project Files manually)
        'blueprint.xlsx',           # xlsx not readable by Claude
        'PYQ_Frequency.xlsx',       # reference spreadsheet
        'Sorted_*.docx',            # goes to Google Drive PYQ folder
        'Mock*_Q1to*.docx',         # Step 7 per-batch cumulative paper
        'Mock*_Create.docx',        # Step 7 final
        'Mock*_Explanation.docx',     # Step 9 solutions (same file each batch)
        # LEGACY (v1.13; Steps 8/10 retired) — kept so a file already on disk still badges local.
        'Mock*_Create_Complete.docx',      # was Step 8 rectified
        'Mock*_audit_changelog.md',        # was Step 8 conditional
        'Mock*_Explanation_Complete.docx', # was Step 10 audited solutions
        'Mock*_Final.docx',        # Step 11 tagged final deliverable
        # v1.21 (GAP-2026-08-13-FOOTER-SCOPED-PATTERNS): suffix patterns cover scoped slugs
        # (SUBJ_*/TOPIC_*/SUBTOPIC_*) that the Mock* patterns above never matched.
        '*_Q1to*.docx',             # Step 7 per-batch cumulative (any slug)
        '*_Create.docx',            # Step 7 final (any slug)
        '*_Explanation.docx',       # Step 9 solutions (any slug)
        '*_Final.docx',             # Step 11 tagged final (any slug)
        '*_audit_dossier.json',     # Step 7 dossier — INTERNAL since v1.27 (kept for old files)
        '*_Create_Repaired.docx',   # Step 7-R repaired paper (any slug) — v1.27
        '*_Create_Repaired_PARTIAL_*.docx',  # Step 7-R mid-batch cumulative paper — v1.28
        '*_Explain_Report.docx',    # Step 9 / 9-R END-OF-MOCK REPORT docx (any slug) — v1.27
        '*_taxonomy.xlsx',          # Step 5 id companion (xlsx — not Claude-readable)
        'analysis_summary.md',      # Step 5 final — human review audit trail
        '*pyq_registry.json',       # PYQ-4 corpus tracker — LOCAL-ONLY (v1.16/v1.17: bare name
                                    # too; Framework_PYQDeliver v1.10 never uploads it)
    }

    # CONTEXT-DEPENDENT (not in LOCAL_ONLY — badge per §3 registry + context):
    #   analysis_progress.json: Step 5 mid-step → Upload/Replace; final → Use locally.
    #   notes_pyq_bank.json (NB): mid-batch checkpoint → Upload/Replace (fresh-chat
    #     resume, A-7 option B) or Use locally (in-session); final → Upload (NC/NA consume it).
    if any(filename.endswith(pat.replace('*', '')) or
           fnmatch(filename, f'*{pat}') for pat in LOCAL_ONLY):
        return 'local'

    # Files that go to project Files
    # If file already exists in project (from prior step/part/run) → replace
    # If file is new → upload
    if file_exists_in_project(filename):
        return 'replace'
    else:
        return 'upload'
```

---

## §3 — PER-STEP DELIVERABLE REGISTRY

Complete mapping of every step's deliverables, their footer type, and
the next step to reference. [ExamCode] is the exam prefix throughout.

```
§2A — SPEC PROVENANCE DISCLOSURE (v1.14 — MANDATORY, every footer)
═══════════════════════════════════════════════════════════════════════
Specs are PROJECT-FIRST (2026.08.03.8): a project-Files Framework_*.md overrides the
repo copy and CANNOT be byte-verified (MANIFEST.json describes the repo).

Step 0 prints a "SPEC SOURCE:" report. Carry its verdict into every footer:

  All specs repo-sourced →
      SPECS      : repo-verified (bootstrap 100%)

  Any spec project-sourced →
      SPECS      : PROJECT-OVERRIDE — N spec(s) unverified
                   [names every project-sourced spec and its version]
                   Integrity not verifiable; these may be stale or out of step
                   with the repo engines.

THIS NEVER HALTS AND NEVER CHANGES SEVERITY: a DISCLOSURE line, not a gate (no
AMBER, no VOID_ITEM/BLOCKING, no F1/F2 change). It only prevents a run on an
unverified spec from being presented as fully verified.

An [ORPHAN — NOT LOADED] line = a project spec no trigger routes; ignored — say it can be deleted.

═══════════════════════════════════════════════════════════════════════
STEP 1 — PYQPrepare
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 per exam paper (single response, no batches)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_DD-Mon-YYYY[_<session>].docx  → Use locally
    (User uploads to [ExamCode] project Files or Google Drive PYQ folder)

NEXT STEP  : Step 2a: PYQDraft
NOTE       : Step 1 runs once per raw paper (trigger separately for each); go to
             Step 2a after ALL papers are converted.

═══════════════════════════════════════════════════════════════════════
BADGE NOTE — FIRST-BATCH vs SUBSEQUENT-BATCH
═══════════════════════════════════════════════════════════════════════
For batch-based steps (2b, 5, 6, 7, 9): first batch delivering a file →
"Upload to Project Files"; subsequent batches → "Replace in Project Files".
Badges below are the TYPICAL case; the actual badge follows §2 at runtime.

═══════════════════════════════════════════════════════════════════════
STEP 2a — PYQDraft [ExamCode]
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response, no batches)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_taxonomy_draft.json     → Upload to Project Files
  [ExamCode]_exam_config.json        → Upload to Project Files

NEXT STEP  : Step 2b: PYQScan

═══════════════════════════════════════════════════════════════════════
STEP 2b — PYQScan
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches (corpus-dependent)
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after final batch + convergence

MID-STEP DELIVERABLES (per batch):
  [ExamCode]_scan_progress.json      → Upload (1st batch) / Replace (subsequent)
  [ExamCode]_classifications.json    → Upload (1st batch) / Replace (subsequent)

FINAL DELIVERABLES (same files, final versions):
  [ExamCode]_scan_progress.json      → Replace in Project Files
  [ExamCode]_classifications.json    → Replace in Project Files

NEXT STEP  : Step 2c: PYQApprove

═══════════════════════════════════════════════════════════════════════
STEP 2c — PYQApprove
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_PYQ_Analysis.docx       → Upload to Project Files
  [ExamCode]_exam_config.json        → Replace in Project Files
  [ExamCode]_approval_record.json    → Upload to Project Files

  approval_record.json is NOT a report — it is the taxonomy LOCK and a
  load-bearing artifact. Later PYQApprove runs replay its verdicts (INV-6),
  and PYQSort refuses to run without it (Framework_PYQSort S0-0). Omitting it
  from this registry is what allowed it to go undelivered from PYQAnalyse
  v2.17 to v2.22.1.

NEXT STEP  : Step 3: PYQSort

═══════════════════════════════════════════════════════════════════════
STEP 3 — PYQSort
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 per Row file (single response, no batches)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_<date>_Sorted_Q1-Q<N>.docx  → Use locally
    (User uploads to Google Drive PYQ folder)

NEXT STEP  : Step 4: PYQCount
NOTE       : Step 3 runs once per Row file. If multiple Row files exist,
             user triggers Step 3 separately for each. After ALL Row files
             are sorted, proceed to Step 4.

═══════════════════════════════════════════════════════════════════════
STEP 4 — PYQCount
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (script-based, single response)
FOOTER TYPE: F2 (step-complete) — always
             F1 (session-break) if context limit forces mid-count break

COMPLETION DELIVERABLES:
  [ExamCode]_PYQ_Analysis.docx       → Replace in Project Files

SESSION-BREAK INTERIM DELIVERABLE (context limit only):
  [ExamCode]_count_progress.json     → Upload to Project Files
  (Session persistence file. Delivered ONLY at forced session breaks,
   NEVER at completion. User uploads to project for resume in new chat.)

NEXT STEP  : Step 5: PYQExtract

═══════════════════════════════════════════════════════════════════════
STEP 5 — PYQExtract
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches (3 papers per batch)
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after final batch + auto-synthesis

MID-STEP DELIVERABLES (per batch):
  [ExamCode]_analysis_progress.json  → Upload (1st batch) / Replace (subsequent)

FINAL DELIVERABLES (5 mandatory + 2 conditional — exam_config.json when
generated, taxonomy.xlsx when written; the two-tier set MockTestAnalyse S11-3
enforces. v1.23 heading; the v1.21 note below is historical — v1.21,
GAP-2026-08-13-DELIVERY-COUNT-DRIFT mirrored from MockTestAnalyse v2.47: this
list said "5 files", predating BOTH the v2.24.9 exam_config addition and the
v2.24 taxonomy companion, so exam_config had no badge and taxonomy.xlsx fell
through to an Upload badge for an xlsx this spec itself calls unreadable):
  [ExamCode]_section_rules.md        → Upload to Project Files
  [ExamCode]_subtopic_manifest.json  → Upload to Project Files
  [ExamCode]_PYQ_Frequency.xlsx      → Use locally (Step 6 input — user provides when needed)
  [ExamCode]_exam_config.json        → Replace in Project Files (subjects[] added by S-SECMAP;
                                       delivered only when generated)
  [ExamCode]_analysis_progress.json  → Use locally (keep for future re-runs if adding papers)
  [ExamCode]_analysis_summary.md     → Use locally (human review audit trail)
  [ExamCode]_taxonomy.xlsx           → Use locally (human-readable id companion; when written)

NEXT STEP  : Step 6: MockBlueprint (parallel with Step 5 — see §1 F2 special case)

═══════════════════════════════════════════════════════════════════════
STEP 6 — MockBlueprint
═══════════════════════════════════════════════════════════════════════
PARTS      : B1 + B2×ceil(N/10) + B3 (3+ batches)
FOOTER TYPE: F1 (mid-step) after B1 and each B2 batch
             F2 (step-complete) after B3

B1 DELIVERABLES:
  [ExamCode]_blueprint.xlsx          → Use locally
  [ExamCode]_blueprint.json          → Upload to Project Files

B2 DELIVERABLES (per batch):
  [ExamCode]_blueprint.json          → Replace in Project Files

B3 FINAL DELIVERABLES (5 files — per Blueprint v1.43.0):
  [ExamCode]_blueprint.xlsx          → Use locally (xlsx not readable by Claude)
  [ExamCode]_blueprint.json          → Replace in Project Files
  [ExamCode]_registry.json           → Upload to Project Files
  [ExamCode]_EXPLAIN_LEARNINGS_v1.md → Upload to Project Files
    (v1.23: was listed as [ExamCode]_ExplainLearnings.md — a name Blueprint
     v1.50.0 no longer emits because it matched no consumer's glob; Steps 7
     and 9 load [ExamCode]_EXPLAIN_LEARNINGS_v*.md.)
  [ExamCode]_mock_test_audit.py      → Upload to Project Files (run by Step 7)

  NOTE (v2.12.1): the repo engines blueprint_core.py / figural_core.py are NOT
  delivered here and must NOT be uploaded per-exam. Step 7 copies both from the
  Step-0 verified clone into its own working directory. Engines live only in the
  central repo (CLAUDE.md); a per-project copy is a second, unverified source that
  can silently go stale. If an engine is ever unavailable the dependent gates
  report an explicit WARN skip — no engine condition halts a run.

NEXT STEP  : Step 7: MockCreate M1

═══════════════════════════════════════════════════════════════════════
STEP 6S — ScopedBlueprint (v1.24 — the scoped-paper twin of Step 6)
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 per scope (single response, no batches)
FOOTER TYPE: F2 (step-complete) — always. Pipeline bar: MAIN number 6 (6 of 11).

DELIVERABLES ([SCOPETAG] = SUBJ_* / TOPIC_* / SUBTOPIC_*, as Framework_ScopedBlueprint
              defines it in its EMIT section):
  [ExamCode]_[SCOPETAG]_blueprint.json → Upload to Project Files
  [ExamCode]_[SCOPETAG]_blueprint.xlsx → Use locally (xlsx not readable by Claude)
  [ExamCode]_registry.json             → Upload to Project Files — ONLY when S8-7
                                         seeded a fresh registry (no registry existed);
                                         an existing registry is left untouched here
                                         (Step 6S does not change it — §8 law).

NEXT STEP  : Step 7: TestCreate P1 --level <subject|topic|subtopic> --scope <…>
             (ensure Step 5 outputs are also in project Files)

═══════════════════════════════════════════════════════════════════════
STEP 7 — MockCreate
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches per mock + final assembly
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after final assembly

MID-STEP DELIVERABLES (per batch — cumulative whole-paper):
  [ExamCode]_Mock[N]_Q1to[K].docx    → Use locally
  (K = last Q number in this batch; filename grows: Q1to10, Q1to20, ...)

FINAL DELIVERABLES (EXACTLY two — MockTestCreate S13-6, v5.73):
  [ExamCode]_Mock[N]_Create.docx   → Use locally
  [ExamCode]_registry.json           → Replace in Project Files
  (v1.27: [ExamCode]_M[N]_audit_dossier.json is INTERNAL — written to /home/claude,
   never delivered. Operator decision 2026-08-26.)

NEXT STEP  : Step 9: MockExplain M[N]   (mock paper)
             Step 9: TestExplain P[N]   (scoped paper — v1.24; the M alias HARD-STOPs
                                         on a scoped docx, MockTestExplain S2-1)

  (v1.13 — Step 8 is RETIRED; never print it as a next step.)

═══════════════════════════════════════════════════════════════════════
STEP 7-R — TestCreateRepair / MockCreateRepair  (v1.27 — MockTestCreate §S16; batched v1.28)
═══════════════════════════════════════════════════════════════════════
PARTS      : one batch (≤ 10 rework qs) per response — MockTestCreate S16-1b
FOOTER TYPE: F1 (mid-step) after each non-final repair batch
             F2 (step-complete) at the final batch

MID-STEP DELIVERABLES (per non-final batch — cumulative, whole paper):
  [ExamCode]_[paper_slug]_Create_Repaired_PARTIAL_[k]of[K].docx → Use locally
  (registry WITHHELD until the final batch — S16-3; Step 9-R refuses the PARTIAL name)

FINAL DELIVERABLES (CLOSED SET = pp.handoff_set('TestCreateRepair', …)):
  [ExamCode]_[paper_slug]_Create_Repaired.docx → Use locally
  [ExamCode]_registry.json                    → Replace in Project Files (carries the
                                                 pre-repair snapshot §7A-R R3 needs)

NEXT STEP  : Step 9-R: TestExplainRepair P[N] · MockExplainRepair M[N]  (attach the
             repaired paper + the previous Explanation docx)

═══════════════════════════════════════════════════════════════════════
STEP 9 — MockExplain
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches (batch size from spec)
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after final batch

DELIVERY MODEL: Whole-paper incremental (RE-8). Each batch delivers the
  SAME file — explained-so-far + untouched remainder. NOT separate batch files.

MID-STEP DELIVERABLES (per batch — same file, incrementally filled):
  [ExamCode]_Mock[N]_Explanation.docx  → Use locally

FINAL DELIVERABLES (CLOSED SET = pp.handoff_set('TestExplain', …, final=True);
MockTestExplain S19-0, v1.46.0):
  [ExamCode]_Mock[N]_Explanation.docx     → Use locally   (now fully explained)
  [ExamCode]_registry.json                → Replace in Project Files — whenever the run
                                            changed it (every §7A-M verdict/healing; the ONLY
                                            channel to Step 11). Legacy: unchanged → not delivered.
  [ExamCode]_Mock[N]_Explain_Report.docx  → Use locally   (END-OF-MOCK REPORT docx,
                                            MockTestExplain S20-R; inert downstream)

NEXT STEP  : Step 11: MockDeliver M[N]  (mock paper) — only on "✅ CLEARED FOR DELIVERY";
             on ❌ FAILED → Step 7-R (the box prints both commands, pp.dg_next_step)
             Step 11: TestDeliver P[N]  (scoped paper — v1.24; MockDeliver S1-2 gates
                                         the uploaded slug against the paper_slug)

  (v1.13 — Step 10 is RETIRED; v1.15 — PYQExplainAudit (PYQ-2) too. Never print
   either as a next step.)

═══════════════════════════════════════════════════════════════════════
STEP 9-R — TestExplainRepair / MockExplainRepair  (v1.27 — MockTestExplain §7A-R)
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 or more batches over the rework_qs only (batching rules apply)
FOOTER TYPE: F2 (step-complete) — after the re-gate

DELIVERABLES (CLOSED SET = pp.handoff_set('TestExplainRepair', …, final=True)):
  [ExamCode]_[paper_slug]_Explanation.docx    → Use locally   (rework blocks spliced;
                                                 SAME filename Step 11 accepts)
  [ExamCode]_registry.json                    → Replace in Project Files (re-gate verdict)
  [ExamCode]_[paper_slug]_Explain_Report.docx → Use locally   (REPAIR EDITION)

NEXT STEP  : Step 11: TestDeliver P[N] · MockDeliver M[N]  (pp.dg_next_step)

═══════════════════════════════════════════════════════════════════════
STEP 11 — MockDeliver
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_Mock[N]_Final.docx     → Use locally
  [ExamCode]_registry.json          → Replace in Project Files — ONLY when S1-2 3b
                                       healed the record (pp.registry_changed, MockDeliver §8)

NEXT STEP  : Pipeline complete for this paper ([paper_slug]).
             Next mock paper   : Step 7: MockCreate M[N+1]
             Next scoped paper : Step 7: TestCreate P[N+1] (same --level/--scope), or
                                 the series is complete when N == the scoped
                                 blueprint's paper count (v1.24)

§FOOTER-DG — DIFFICULTY-GATE DISCLOSURE LINES (v1.25 — GAP-2026-08-25-DIFFICULTY-
GATE-ROUND-COUNTER; referenced by MockDeliver since v1.13.0, defined here for the
first time). Immediately after the Deliverables table of the Step 11 F2 footer,
print EVERY string returned by
    pp.dg_footer_lines(pp.dg_read(reg, paper_id))
one per line, each prefixed "ℹ️ ". The engine is the ONLY source of these lines —
never compose them by hand. The set it returns, by record state:
    PASSED (0 or 1 rounds)  → nothing
    DISCLOSED / 1           → "Measured difficulty: [bottom] n (not gated) · [middle]
                               b/m in window · [top] c/h in window confirmed after 1
                               repair round." (v1.26 windowed record; a pre-window
                               record prints plain a/n fractions)
    DORMANT / 0             → "Difficulty gate: not applicable to this paper
                               ([dormant_reason]) — labels are as planned at Step 7."
    any record with a
    migrations[] trail      → one "Difficulty-gate record healed (GAP-…): <field>
                               a → b on <date>." line PER migration
A legacy paper (no record) prints nothing. A HEALED registry is ALWAYS disclosed:
a registry healed by pp.dg_preflight must never look identical to one that was
always clean (MockTestExplain §6A-4: silent degradation is the worse failure).

═══════════════════════════════════════════════════════════════════════
NOTES PIPELINE (NB / NC / NA / ND)
═══════════════════════════════════════════════════════════════════════
A SEPARATE pipeline. Its F2 footers use the 4-cell NOTES bar (§4-4), never the
11-cell Mock/PYQ bar. Each step runs in its OWN chat (framework idiom). v1.20:
the JSON artifacts (bank, blueprint, registry) persist through Project Files as
before, but the notes .docx moves between NC -> NA -> ND as a CHAT ATTACHMENT —
so its badge is "Use locally" and the Next callout tells the operator to attach
it. All four steps still present files and render a footer. The registry (notes_registry.json)
is re-presented by every step that changes a unit's state (DRAFTED → AUDITED_PASS
→ DELIVERED).

═══════════════════════════════════════════════════════════════════════
NB — NotesBlueprint
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches of 3 papers (BATCH STOP after each — NB §3A A-7)
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after the final batch + blueprint/registry

MID-BATCH DELIVERABLES (per batch — same file, append-only checkpoint):
  notes_pyq_bank.json                → Upload/Replace in Project Files for a
    fresh-chat resume (A-7 option B); Use locally if continuing in-session
    (option A). Context-dependent — see the get_badge note in §2.

FINAL DELIVERABLES:
  notes_pyq_bank.json                → Upload to Project Files (NC/NA read it)
  notes_blueprint.json               → Upload to Project Files
  notes_registry.json                → Upload to Project Files

NEXT STEP  : NC: NotesCreate (one subtopic at a time)

═══════════════════════════════════════════════════════════════════════
NC — NotesCreate
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 subtopic per run (single response)
FOOTER TYPE: F2 (step-complete) — the subtopic draft is done

DELIVERABLES:
  [ExamCode]_<unit>.docx (draft)     → Use locally, then ATTACH to the NA chat
    (v1.20: the draft is NOT filed — Framework_NotesAudit §0A takes it as a
     chat attachment, and §0B verifies it against the registry's draft_ref)
  notes_registry.json                → Replace in Project Files (unit → DRAFTED,
    carrying draft_ref)

NEXT STEP  : NA: NotesAudit (in a NEW chat, with the draft ATTACHED)

═══════════════════════════════════════════════════════════════════════
NA — NotesAudit
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 unit per run; convergence loop until pass (internal)
FOOTER TYPE: F2 (step-complete) on AUDITED_PASS
             F1 AMBER (quality-gate variant) if the §4 loop exits at the L-3
             non-convergence diagnostic

DELIVERABLES (NA emits exactly one document in EVERY outcome — v1.20):
  [ExamCode]_<unit>_Final.docx       → Use locally, then ATTACH to the ND chat
    (notes_core.notes_final_filename; no _Audit.md exists any more — the
     evidence is the unit's audit_summary inside the registry)
  notes_registry.json                → Replace in Project Files (unit →
    AUDITED_PASS, carrying final_ref and audit_summary)

NEXT STEP  : ND: NotesDeliver (in a NEW chat, with the _Final ATTACHED)

═══════════════════════════════════════════════════════════════════════
ND — NotesDeliver
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 unit per run (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_<unit>_Deliver.docx     → Use locally (IFAS portal — Word-native;
    notes_core.notes_deliver_filename)
  notes_registry.json                → Replace in Project Files (unit → DELIVERED)

NEXT STEP  : NC: NotesCreate (next subtopic), or Notes pipeline complete when all
             blueprinted units are DELIVERED.
```

---

## §4 — RENDERING CONTRACT

The delivery footer is a fixed Markdown block. It requires NO external tool,
MCP server, visualizer, or widget. It renders identically on every surface
(desktop, laptop, web, mobile) and for every team member, because it uses only
universal Markdown + Unicode. The footer is the LAST element in the response,
after the present_files call and any in-chat delivery report.

COLOR THEME (state-coded, via Unicode emoji — renders identically everywhere):
  F2 step-complete → GREEN theme : 🟩 band, ✅ header icon, 🟩 progress fill.
  F1 mid-step      → AMBER theme : 🟨 band, ⏳ header icon, 🟨 progress fill.

### §4-0 — Rendering rules (MANDATORY)

```
R1. The Markdown template below IS the contract. Always emit it, exactly, as
    the LAST element of the response after present_files. It is never skipped
    and never optional.
R2. FORBIDDEN: show_widget, the visualizer, or any rendering MCP. Never call
    one, never ToolSearch for one. The footer needs nothing external. This is
    the whole point of v1.5 — the old widget path was the cause of every
    intermittent "broken footer" report.
R3. FORBIDDEN: improvising any other footer format — no ASCII banners
    (=== ... ===), no monospace code-block footers, no ad-hoc bullet lists.
    If unsure, reproduce the template verbatim.
R4. State color is MANDATORY and must match the footer type:
    complete = GREEN (🟩 / ✅), in-progress = AMBER (🟨 / ⏳). Never mix themes.
R5. Filenames in `inline code`; one NUMBERED table row per deliverable; the
    Action column carries the §2 badge text VERBATIM, prefixed with its icon
    (📤 Upload to Project Files / 🔁 Replace in Project Files / 📁 Use locally).
```

### §4-1 — F2 step-complete footer (GREEN) — Markdown template

The literal structure to emit (substitute [bracketed] values; keep everything else):

```
🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

## ✅ Step [N] · [StepName] — Complete

`[ExamCode]`  ·  all deliverables ready

**📦 Deliverables**

| # | File | Action |
| :---: | :--- | :--- |
| 1 | `[ExamCode]_<file1>.<ext>` | [icon] [badge] |
| 2 | `[ExamCode]_<file2>.<ext>` | [icon] [badge] |

> ### → Next: Step [N+1] — [NextStepName]
> Start in a **new chat**. [one short line on what the next step does]
>
> `Pipeline  [11-cell 🟩/⬜ bar]  [N] of 11`

Thank you! 🎯

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
```

STEP 11 (last step) — replace the Next callout block with:

```
> ### 🏁 Pipeline complete for [ExamCode] [paper_slug]
> Next paper: **Step 7 — MockCreate M[N+1]** (mock) / **TestCreate P[N+1]** (scoped series,
> or "series complete" at its last paper) in a new chat. Thank you!
>
> `Pipeline  🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩  11 of 11`
```

### §4-2 — F1 mid-step footer (AMBER) — Markdown template

```
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨

## ⏳ Step [N] · [StepName] — In progress

`[ExamCode]`  ·  batch [X] of [Y] complete

**📦 Delivered this batch**

| # | File | Action |
| :---: | :--- | :--- |
| 1 | `[ExamCode]_<file>.<ext>` | [icon] [badge] |

> ### 🔄 Type `continue` to generate batch [X+1]
> Stay in **this chat** — step not yet complete.
>
> `Batch  [12-cell 🟨/⬜ bar]  [X] of [Y]`

🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
```

UNKNOWN TOTAL (e.g. PYQScan) — the metadata line becomes
"`[ExamCode]`  ·  batch [X] complete", and the batch progress-bar line is OMITTED.

SESSION-BREAK VARIANT (context-limit forced break) — replace the callout block with:

```
> ### ⚠️ Upload files to Project Files, then resume in a new chat
> Step not yet complete.
```

### §4-3 — Action badge text + icon

```
📤  Upload to Project Files   — file is new to project Files
🔁  Replace in Project Files  — file already exists in project Files
📁  Use locally               — file not uploaded to project Files

Badge SELECTION logic is unchanged — see §2. Wording is EXACT (do not reword);
the icon is a fixed prefix per badge.
```

### §4-4 — Progress bars (deterministic — no guessing)

```
PIPELINE BAR (F2 only): exactly 11 cells.
  filled = the step's MAIN number. Steps 2a / 2b / 2c all count as 2.
  Render `filled` × 🟩 followed by (11 − filled) × ⬜. Label: "[N] of 11".
  The bar stays at 11 cells (v1.13): retiring Steps 8 and 10 did NOT renumber the
  pipeline, so Step 9 is still 9 of 11 and Step 11 is still 11 of 11. Numbers 8 and
  10 simply never occur as a step's MAIN number any more.
  Example — Step 3 : 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜  3 of 11
  Example — Step 9 : 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜  9 of 11

BATCH BAR (F1 only): exactly 12 cells.
  filled = round(12 × X / Y). Render `filled` × 🟨 + (12 − filled) × ⬜.
  Label: "[X] of [Y]". If Y (total batches) is unknown, OMIT the bar line.
  Example — batch 1 of 3 : 🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜  1 of 3

NOTES PIPELINE BAR (F2 only — Notes steps NB/NC/NA/ND): exactly 4 cells.
  Used INSTEAD of the 11-cell bar in EVERY Notes-step F2 footer (the 11-cell
  Mock/PYQ bar never applies to Notes). filled = NB→1, NC→2, NA→3, ND→4. Render
  `filled` × 🟩 + (4 − filled) × ⬜. Label: "[n] of 4" with the step code in the
  header ("Step NB · NotesBlueprint"). NB's NON-FINAL batches stay F1 with the
  12-cell BATCH bar above; NB's final delivery, NC, NA and ND each use this 4-cell
  bar.
  Example — NB final : 🟩⬜⬜⬜  1 of 4
  Example — NC       : 🟩🟩⬜⬜  2 of 4
  Example — NA       : 🟩🟩🟩⬜  3 of 4
  Example — ND       : 🟩🟩🟩🟩  4 of 4
```

---

## §5 — DECISION FLOWCHART

```
After every present_files call, Claude evaluates:

  Q0: Did this step's own quality checks report any FAIL?
      (v1.8, GAP-2026-07-26-003. Step 5 run_qv QV-1..QV-14, Step 8 audit gates,
       or an unobserved-image count from Step 1 S1-12.)

      YES → Render F1 (AMBER), even when every batch is finished, and name the
            failing check and its remedy in the footer body.
            DO NOT render F2. Then END response.

      NO  → Q0b (v1.12): did the run that produced this paper report
            COMPLETION-GATE: DEGRADED (vision) — OR did PYQExplain (PYQ-1) record
            any VOID_ITEM in its §13A figural pre-transcription pass?
            (Step 7 reports the first since Step 8 retired; the second is
            Framework_PYQExplain §13A-5. Same condition: an image measured un-viewable.)

            YES → Render F1 (AMBER). The paper IS certified and IS delivered, but a
                  measured vision outage meant some figures were machine-checked and
                  never eyeballed. Name it exactly:
                  "CERTIFIED-DEGRADED (VISION) — <v> of <i> image artefact(s) were not
                   viewed (P3.5 probe FAILED). Figure arithmetic, tables and OMML were
                   fully checked; legibility and figure/stem match were NOT visually
                   confirmed. Remedy: re-run Step 7 on a session with a working view
                   tool." Then END response.
                  For PYQ-1 the same footer NAMES the voided questions instead:
                  "CERTIFIED-DEGRADED (VISION) — <v> of <i> figural artefact(s) could
                   not be transcribed (§13A). Question(s) <list> carry NO derived
                   answer; every other question is fully explained.
                   Remedy: re-run PYQExplain on a session with a working view tool."
                  Naming is mandatory (the reviewer must be told where to look).
                  A degraded certificate must NEVER render green.

            NO  → continue to Q1.

      WHY THIS EXISTS. A step could report a FAIL and still render green — the
      reference run shipped 153/153 figural questions unobserved under a green F2.
      THIS IS NOT A HALT: the step completes and delivers; amber reports, never
      blocks. A WARN does NOT force amber (advisory — keep the distinction meaningful).

  Q1: Is this step's work FULLY complete?
      (All batches done, all parts done, final synthesis done if applicable)

      YES → Render F2 (GREEN step-complete footer, §4-1)
            Include ALL final deliverable files with correct badges.
            Include the "→ Next" callout with correct next step name.
            END response after footer.

      NO  → Render F1 (AMBER mid-step footer, §4-2)
            Include ONLY the files delivered in THIS present_files call.
            Include the "Type continue" callout.
            END response after footer.

  EDGE CASE — Session-break delivery (context limit exhaustion):
      This is a special F1 case. The step is not at a normal batch boundary
      — Claude is forced to stop mid-work. Footer uses F1 (AMBER) with the
      session-break callout variant (see §4-2). Files delivered are
      session-persistence files (e.g., count_progress.json).

  EDGE CASE — Step complete but a check FAILED (v1.8):
      F1 AMBER with the QUALITY-GATE callout variant. Wording states the step is
      complete, names the failing check, and gives the remedy. For a vision gap
      the remedy is always: re-run PHASE B ONLY — the queue and contact sheets are
      already on disk, Phases A and C need not repeat, and Phase B is idempotent.
      NEVER phrase this as "the step failed"; the step ran, the artefact is
      incomplete, and both facts belong in the footer.

  NEVER render both footers in the same response.
  NEVER omit the footer after a present_files call.
  NEVER render the footer WITHOUT a preceding present_files call.
  NEVER call show_widget / the visualizer (§4-0 R2).
  The footer is always the LAST element in the response.
```

---

## §6 — NEXT-STEP REFERENCE TABLE

```
After Step 1   → Step 2a: PYQDraft (after ALL papers converted to Row files)
After Step 2a  → Step 2b: PYQScan
After Step 2b  → Step 2c: PYQApprove
After Step 2c  → Step 3: PYQSort (sort all Row files, then Step 4)
After Step 3   → Step 4: PYQCount
After Step 4   → Step 5: PYQExtract
After Step 5   → Step 6: MockBlueprint (if not already done)
After Step 6   → Step 7: MockCreate M1
After Step 6S  → Step 7: TestCreate P1 --level … --scope …          (v1.24)
After Step 7   → Step 9: MockExplain M[N] · TestExplain P[N] (scoped)   (Step 8 retired — 2026.08.03.5)
After Step 9   → Step 11: MockDeliver M[N] · TestDeliver P[N] (scoped) (Step 10 retired — 2026.08.03.5)
                 … when the §7A-M verdict is ✅ PASSED / DORMANT. On ❌ FAILED (v1.27):
After Step 9 ❌ → Step 7-R: TestCreateRepair P[N] Q… · MockCreateRepair M[N] Q…
After Step 7-R → Step 9-R: TestExplainRepair P[N] · MockExplainRepair M[N]
After Step 9-R → Step 11: TestDeliver P[N] · MockDeliver M[N]   (PASSED/1 or DISCLOSED/1)
After Step 11  → Pipeline complete for [paper_slug].
                 Next: Step 7: MockCreate M[N+1] (mock) · TestCreate P[N+1] (scoped series)

NOTES PIPELINE (separate):
After NB       → NC: NotesCreate (one subtopic at a time)
After NC       → NA: NotesAudit
After NA       → ND: NotesDeliver (NA is self-contained from v3.0.0: it
                 corrects, rebuilds and always emits one _Final.docx)
After ND       → NC: NotesCreate (next subtopic), or Notes pipeline complete when
                 all blueprinted units are DELIVERED.
```

---

## §7 — EXAM-AGNOSTIC GUARANTEE

```
This spec contains zero hardcoded exam values.
All filenames use [ExamCode] prefix — resolved at runtime.
All deliverable lists are read from the step's own spec (§3 registry).
The footer needs zero external tools, so it renders identically on any
machine, any surface, for any team member — SSC CGL, GATE, NEET, UPSC,
CAT, MPSC, or any exam.
```

---

## §8 — REGISTRY-HANDOFF-LAW (v1.27 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM)

```
THE LAW. A step that CHANGES [ExamCode]_registry.json DELIVERS it, badge "Replace in
Project Files", in the SAME present_files call as its primary artefact. The next step
reads ONLY the project copy; an undelivered change is a change the pipeline never sees.

WRITERS (paper_pipeline.RH_REGISTRY_WRITING_STEPS): Test/MockCreate (Final Assembly),
Test/MockCreateRepair (§S16-3), Test/MockExplain (§7A-M), Test/MockExplainRepair (§7A-R).
READER: Test/MockDeliver (delivers the registry only when its preflight healed it).

DECIDED BY pp.registry_changed(project fingerprint, working copy) → pp.handoff_set(step, …)
— the CLOSED set and badge per file. The footer prints pp.handoff_footer_lines(HANDOFF)
VERBATIM, then HANDOFF['lines']. Never composed by hand, never decided by prose.

WHY A LAW. Four steps wrote the registry, one delivered it, every gated paper was
undeliverable. MS-14 bans the old wording; LAW_REGISTRY.json REGISTRY-HANDOFF-LAW.
```
