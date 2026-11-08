# Framework_DeliveryFooter v1.42.0 — Universal Delivery Footer (F1/F2) Contract
# v1.42.0 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (paired with blueprint_core v1.33,
#   MockTestCreate v5.94, MockDeliver v1.27.0). §FOOTER-FT gains the DIFFICULTY LAYER LINES —
#   bc.difficulty_layer_lines over the paper's recorded difficulty_state.paper_gate / l2_model:
#   delivered vs target counts, DR3 items (accepted below their slot after full repair, disclosed),
#   unmeasured slots, the organic ruler's state and the source of its shares. "ℹ️ "-prefixed,
#   disclosure only; a paper without the records prints nothing (byte-identical).
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
           Step 7 / 9 re-delivering the updated registry.json
           (REGISTRY-HANDOFF-LAW, §8 — every step that changes it).
           v1.33: for [ExamCode]_registry.json the operator may EITHER replace it
           in Project Files OR attach the delivered file to the next step's
           trigger (REGISTRY-SOURCE-LAW — the attachment wins). Badge unchanged.

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
        '*_Explain_Report.docx',    # Step 9 END-OF-MOCK REPORT docx (any slug) — v1.27
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

FINAL DELIVERABLES (8 mandatory + 2 conditional — exam_config.json when
generated, taxonomy.xlsx when written; the two-tier set MockTestAnalyse S11-3
enforces, listed here in the S11-3 emission order. v1.34 heading — this block
had stopped at 5 mandatory and never gained the v2.56 style_profile.json /
pyq_index.json pair (GAP-2026-09-14-DELIVERY-ECHO, registry-drift half). The
v1.21 note is historical — v1.21, GAP-2026-08-13-DELIVERY-COUNT-DRIFT mirrored
from MockTestAnalyse v2.47: this list said "5 files", predating BOTH the v2.24.9
exam_config addition and the v2.24 taxonomy companion, so exam_config had no
badge and taxonomy.xlsx fell through to an Upload badge for an xlsx this spec
itself calls unreadable):
  [ExamCode]_section_rules.md        → Upload to Project Files
  [ExamCode]_subtopic_manifest.json  → Upload to Project Files
  [ExamCode]_PYQ_Frequency.xlsx      → Use locally (Step 6 input — user provides when needed)
  [ExamCode]_style_profile.json      → Upload to Project Files (v2.56; DORMANT is a written
                                       status, never a missing file)
  [ExamCode]_pyq_index.json          → Upload to Project Files (v2.56; same corpus_hash as
                                       the profile — replace the pair together)
  [ExamCode]_stimulus_profile.json   → Upload to Project Files (v1.35.1; Step 7 keeps
                                       question sets together with it; required before
                                       any new mock/test)
  [ExamCode]_exam_config.json        → Replace in Project Files (subjects[] added by S-SECMAP;
                                       delivered only when generated)
  [ExamCode]_taxonomy.xlsx           → Use locally (human-readable id companion; when written)
  [ExamCode]_analysis_progress.json  → Use locally (keep for future re-runs if adding papers)
  [ExamCode]_analysis_summary.md     → Use locally (human review audit trail)

MODE `PYQExtract --stimulus-profile` (v1.35.1 — existing exams, run once; F2):
  [ExamCode]_stimulus_profile.json   → Upload to Project Files (the ONLY file delivered)
  NEXT: the next NEW MockCreate/TestCreate paper uses it.

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

FINAL DELIVERABLES (EXACTLY two — MockTestCreate S13-6, v5.73; v1.39.0 — always exactly
these two, STEP_CONTRACTS.json; no conditional additions, no review packet):
  [ExamCode]_Mock[N]_Create.docx   → Use locally
                                     (scoped paper: [ExamCode]_[slug]_Create.docx)
  [ExamCode]_registry.json           → Replace in Project Files
                                       (or attach it to the Step 9 trigger — v1.33 §8)
  (v1.27: [ExamCode]_M[N]_audit_dossier.json is INTERNAL — written to /home/claude,
   never delivered. Operator decision 2026-08-26.)
  (v1.39.0: the independent review runs INSIDE Step 7 (MockTestCreate S13-2G) — it is never a
   user step and produces no user-visible file. An in-run blueprint amendment or a stale /
   missing project auditor copy is disclosed by one INFORMATIONAL §LADDER line — never a
   file to upload.)

NEXT STEP  : Step 9: MockExplain M[N] (mock paper) /
             Step 9: TestExplain P[N] (scoped paper — v1.24; the M alias HARD-STOPs on a
             scoped docx, MockTestExplain S2-1)

  (v1.13 — Step 8 is RETIRED; never print it as a next step.)

(STEP 7R — MockReview / TestReview — RETIRED in v1.39.0, owner decision D2 (a): the
 independent review runs inside Step 7 (MockTestCreate S13-2G); never print 7R, a review
 packet or a verdict file as a deliverable or a next step.)

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
                                            channel to Step 11 — which reads it from Project
                                            Files OR attached to its trigger, v1.33 §8).
                                            Legacy: unchanged → not delivered.
  [ExamCode]_Mock[N]_Explain_Report.docx  → Use locally   (END-OF-MOCK REPORT docx,
                                            MockTestExplain S20-R; inert downstream)

NEXT STEP  : Step 11: MockDeliver M[N]  (mock paper) — on ✅ PASSED, ⚠️ DISCLOSED or
             DORMANT alike (v1.29: the gate discloses, it never blocks; the box
             prints the Deliver trigger, pp.dg_next_step)
             Step 11: TestDeliver P[N]  (scoped paper — v1.24; MockDeliver S1-2 gates
                                         the uploaded slug against the paper_slug)

  (v1.13 — Step 10 is RETIRED; v1.15 — PYQExplainAudit (PYQ-2) too. Never print
   either as a next step.)

═══════════════════════════════════════════════════════════════════════
STEP 11 — MockDeliver
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_Mock[N]_Final.docx     → Use locally
  [ExamCode]_registry.json          → Replace in Project Files — ONLY when the run changed
                                       it: S1-2 3b healed the record, or (v1.38.0) S1-2 3f
                                       recorded accepted_uncertified (pp.registry_changed,
                                       MockDeliver §8; or attach it to the next step's
                                       trigger — v1.33 §8)

NEXT STEP  : Pipeline complete for this paper ([paper_slug]).
             Next mock paper   : Step 7: MockCreate M[N+1]
             Next scoped paper : Step 7: TestCreate P[N+1] (same --level/--scope), or
                                 the series is complete when N == the scoped
                                 blueprint's paper count (v1.24)

═══════════════════════════════════════════════════════════════════════
PYQ EXPLANATION TRACK — PYQ-1 / PYQ-3 / PYQ-4 / L2 (v1.34 — this track had NO
block here; each spec's own delivery section was the only source. Sets below
are transcribed from each spec's own delivery section — PYQExplain S19-2,
PYQFormat, PYQDeliver, PYQCompress — and change ONLY when those change. PYQ-2
is retired.)
═══════════════════════════════════════════════════════════════════════
PYQ-1 — PYQExplain
PARTS      : Multiple batches (question ranges)
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after the final batch (100% coverage)

MID-STEP DELIVERABLES (every batch, cumulative docx):
  [ExamCode]_[date]_[session]_PYQ_Explanation.docx → Use locally

FINAL DELIVERABLES (final batch — the docx PLUS the two files below; the batch
habit of "one docx per present_files" does NOT apply to the final batch):
  [ExamCode]_[date]_[session]_PYQ_Explanation.docx        → Use locally (PYQ-3 / PYQ-4 input)
  [ExamCode]_[date]_[session]_pyq_explain_progress.json   → Use locally (PYQ-3 / PYQ-4
                                                             q_to_classification source —
                                                             attach it WITH the docx)
  [ExamCode]_difficulty_profile.json                       → Replace in Project Files
                                                             (Upload on the first run; NOT
                                                             delivered when S7A-6 reports
                                                             PROFILE_STATUS dormant — the
                                                             footer then prints the dormant
                                                             line — R6 (d))

NEXT STEP  : PYQ-3: PYQFormat (student-facing document) · PYQ-4: PYQDeliver (portal)
             — both take the PYQ-1 docx + progress json directly, in a new chat.
             v1.37.0 (GAP-2026-11-02 handshake): after the LAST PYQ paper of the exam
             is explained and its difficulty_profile.json replaced in Project Files,
             re-run Step 5: PYQExtract --synthesise ALL, with the Sorted PYQ .docx
             files attached to that chat or in Project Files (Step 5 also re-measures the
             drawing style from them; without them the style falls back to defaults) —
             Step 5 reads the profile's
             per-question ask / representation / scheme-grammar tags and abbreviation
             evidence into section_rules.md (Steps 6 / 6S / 7 read them from there).
             Print this line on the PYQ-1 F2 footer whenever the profile was delivered.

PYQ-3 — PYQFormat
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always
DELIVERABLES:
  [ExamCode]_[date]_[session]_PYQ_Formatted.docx          → Use locally
NEXT STEP  : Student-facing document — ready for distribution. Portal delivery is
             PYQ-4: PYQDeliver (from the PYQ-1 output, not this file).

PYQ-4 — PYQDeliver
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always
DELIVERABLES:
  [ExamCode]_[date]_[session]_PYQ_Final.docx              → Use locally
  [ExamCode]_pyq_registry.json                             → Use locally — LOCAL-ONLY, and
                                                             ONLY when a prior copy was
                                                             attached to the trigger; on the
                                                             normal run no registry row appears
NEXT STEP  : PYQ pipeline complete for [ExamCode] [date] [session].
             Next paper: PYQ-1: PYQExplain in a new chat.

L2 — PYQCompress
PARTS      : 1 (single response, one or more input files)
FOOTER TYPE: F2 (step-complete) — always
DELIVERABLES:
  one .docx per input, named IDENTICALLY to that input (COMPRESS-NAME-IDENTITY,
  2026.09.14.1)                                            → Use locally
NEXT STEP  : Replace the file(s) in Drive. No pipeline step follows.

PIPELINE BAR for this track: NONE — the 11-cell Mock/PYQ bar and the 4-cell Notes
bar both stay OFF; omit the `Pipeline …` line and keep the Next callout.

§FOOTER-DG — DIFFICULTY-GATE DISCLOSURE LINES (v1.25 — GAP-2026-08-25-DIFFICULTY-
GATE-ROUND-COUNTER; referenced by MockDeliver since v1.13.0, defined here for the
first time). Immediately after the Deliverables table of the Step 11 F2 footer,
print EVERY string returned by
    pp.dg_footer_lines(pp.dg_read(reg, paper_id))
one per line, each prefixed "ℹ️ ". The engine is the ONLY source of these lines —
never compose them by hand. The set it returns, by record state:
    PASSED (0 or 1 rounds)  → nothing
    DISCLOSED / 0           → "Measured difficulty: [bottom] n (not gated) · [middle]
                               b/m in window · [top] c/h in window — the difficulty
                               gate was not met; labels are as planned at Step 7."
                               (v1.29 — the gate discloses, it never blocks; a
                               pre-window record prints plain a/n fractions)
    DISCLOSED / 1           → "Measured difficulty: … confirmed after 1 repair round
                               (legacy repair — the repair steps are retired)."
                               (a LEGACY paper the retired repair step re-gated)
    DORMANT / 0             → "Difficulty gate: not applicable to this paper
                               ([dormant_reason]) — labels are as planned at Step 7."
    any record with a
    migrations[] trail      → one "Difficulty-gate record healed (GAP-…): <field>
                               a → b on <date>." line PER migration
A legacy paper (no record) prints nothing. A HEALED registry is ALWAYS disclosed:
a registry healed by pp.dg_preflight must never look identical to one that was
always clean (MockTestExplain §6A-4: silent degradation is the worse failure).

§FOOTER-FT — FIGURE-RECORD DISCLOSURE LINES (v1.36.0 — GAP-2026-11-01-FIGURE-TYPE-
COVERAGE-AND-RECORD-INTEGRITY LAW F1.4/F3). Immediately after the §FOOTER-STYLE line
of the Step 11 F2 footer — the ONE site that delivers a student-facing paper (Step 7
and Step 9 deliver internal artefacts whose F2 footers carry no paper disclosure
lines) — print EVERY string returned by
    pp.figure_footer_lines(registry, blueprint, paper_id)
(the step's resolved registry dict and the blueprint it selected for this paper), one per
line, each prefixed "ℹ️ ". The engine is the ONLY source of these lines —
never compose them by hand. The set it returns:
    blueprint.figural_fallbacks (text_disclosed)
                            → "Figure fallback: <subtopic_id> rendered as TEXT in this
                               series — its dominant figure type(s) [...] are not
                               renderable (policy text_disclosed)."  (one per subtopic)
    registry.paper_flags[pid] declared False / derived True
                            → "Figure record: blueprint declared <flag>=false but this
                               paper carries that content — the record was committed
                               (MANIFEST-COMMIT-LAW); regenerate the blueprint so the
                               flag is derived."
    paper_flags[pid].figure_record == 'absent_legacy'
                            → "Figure record ABSENT (legacy paper): figures were drawn
                               but no per-question record reached the registry, so
                               figure-profile and type↔kind conformance were NOT
                               AUDITED for this paper."
    figural_manifests[pid].record_integrity (S13-REGCHECK migration)
                            → "Legacy figure record: N question(s) annotated (<counts
                               by kind>) — authored before the figure-record laws; not
                               re-rendered, not re-audited."
    record_integrity == 'legacy_unlabelled' (Step 7 S4-12 4c — a paper resumed across
    the v5.88 fix)          → "Figure record: N question(s) authored before the
                               figure-record laws and completed after them carry no
                               figure type — their type↔kind conformance was NOT
                               AUDITED."
    blueprint.figure_type_coverage.advisories
                            → "Figure types: N subtopic(s) have a dominant figure type
                               not in the figure-type registry — rendered as generic
                               schematics; type↔kind conformance not verifiable for them."
A clean, current paper prints NOTHING (the legacy estate's footers stay byte-identical,
§7 P1). No per-question detail, no gate verdict, no SMILES ever reaches the delivered
document; the annotations themselves live in the registry (internal).

DIFFICULTY DISCLOSURE LINES (v1.40.0 — GAP-2026-11-05-DIFFICULTY-FIDELITY Part D; owner
decisions D3-R5 (a), D10 (B)). In the SAME place, immediately after the figure-record
lines, print EVERY string returned by
    bc.difficulty_unverified_lines(readiness, level_model, n_level_items,
                                   judge_dormant_qs, hard_missed, step9_assessed, coverage)
one per line, each prefixed "⚠️ " — the arguments are the paper's recorded
registry.question_index[].quality_readiness / difficulty_state (Step 7 S13-6 writes the
same lines from the same engine function into its own footer; Step 11 reprints them from
the record). The engine is the ONLY source of these lines — never compose them by hand.
The set it returns:
    level model dormant while the paper carries drawn chemistry
                            → "DIFFICULTY UNVERIFIED — N chemistry item(s) written
                               without an active level model (<reason>)"
    level model active on a small pool (owner D10 B)
                            → "level model: small pool n=<k> (< 20); bands are
                               indicative (owner D10 B)"
    independent rating dormant on items
                            → "DIFFICULTY UNVERIFIED — independent rating dormant on
                               Q…, Q… (no exemplar with content)"
    Hard slots accepted below Hard at ladder R5 (D3-R5 (a))
                            → "Hard target missed: k item(s) accepted at their measured
                               band after 6 regeneration tries (schedule amended, D3-R5)"
    Step 9 coverage under 80 % (DL-53; also pp.dg_footer_lines for the record)
                            → "Step 9: k/n assessed"
    profile written under mixed rubric rules (DL-20)
                            → "profile coverage: … — mixed rubric rules; re-run PYQExplain
                               on all window papers together (recommended, never required)"
A paper whose every difficulty control measured prints NOTHING. The Complexity tag on
the paper stays the canonical label (MockDeliver [HS:INPUT] on a non-canonical label is
untouched, guard G9); "unverified" appears ONLY in these footer lines. These lines are
DISCLOSURE: they never change a verdict, never make a paper NOT CERTIFIED (OD-9) and
never stop a step.

DIFFICULTY LAYER LINES (v1.42.0 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER; owner decisions
D1 (b), Q1 (c)). Immediately after the DIFFICULTY DISCLOSURE LINES print EVERY string
returned by
    bc.difficulty_layer_lines(paper_gate, l2_model, n_l2_items, shares_source)
one per line, each prefixed "ℹ️ " — the arguments are the paper's recorded
registry.question_index[].difficulty_state.paper_gate / .l2_model (Step 7 S13-2L / S3-8L),
the number of its items on the ruler's organic subtopics, and l2_model.grades_source (Step 7
S13-6 prints the same lines from the same engine function; Step 11 reprints them from the
record). The engine is the ONLY source of these lines — never compose them by hand:
    always, when a paper gate was recorded
                            → "Difficulty vs schedule: Easy a / Medium b / Hard c
                               (schedule Easy x / Medium y / Hard z)"
    items accepted below their slot after DR1 / DR2 and two review rounds
                            → "Difficulty fallback (DR3): k item(s) accepted below their
                               slot after full repair — Q…"
    slots no independent control could measure
                            → "Difficulty unmeasured: k slot(s) had no independent band — Q…"
    the organic ruler (an organic paper only)
                            → "Organic difficulty ruler (L2, relative): pool n=…, shares
                               from …, concept coverage …" (+ " — ADVISORY …" below the
                               coverage floor) or "… dormant — <reason>; bands from the
                               independent controls"
A paper without these records prints NOTHING. They are DISCLOSURE: no verdict changes, no
NOT CERTIFIED (OD-9), never a stop.

§FOOTER-STYLE — STYLE-PROFILE STATUS LINE (v1.30 — GAP-2026-08-29-STYLE-FIDELITY
§6.7). Immediately after the §FOOTER-DG lines of the Step 11 F2 footer, print
EVERY string returned by
    pp.style_footer_line(style_meta)
one per line, each prefixed "ℹ️ ", where `style_meta` is the Step-7 record
{status, schema, corpus_hash, reason}. The engine is the ONLY source of this
line — never compose it by hand. The set it returns:
    ACTIVE   → "STYLE PROFILE: ACTIVE (schema 1, corpus <hash8>)"
    DORMANT  → "STYLE PROFILE: DORMANT — <reason>"
    no record (pre-v5.82 paper) → nothing

EXACTLY ONE LINE, AND NOTHING ELSE (P-11 / ruling Q15). No per-question detail,
no similarity figure, no nearest-PYQ id, no G-STYLE / G-PYQ-DIST / G-ITEM
verdict ever reaches the delivered document — a candidate reading the paper
learns that a style profile was in force, not how any individual question
scored against it. Every one of those records lives in the audit dossier and
the registry (`style_gate`), which are internal artefacts and never staged.
The engine drops unknown keys by construction, so passing a richer dict cannot
widen the footer.

§FOOTER-SYL — SYLLABUS-DECLARATION DISCLOSURE LINE (v1.31 — GAP-2026-09-01
§3.6(c)/R15/R19, Release A). On EVERY footer — F1 and F2, every step, both
pipelines — of an exam whose exam_config carries a syllabus_transition block
in a TRACED-INACTIVE state (T1 rows 4/5/7: declaration keys present but
activation failed), print EVERY string returned by
    bc.syllabus_footer_lines(st)
one per line, each prefixed "ℹ️ ", where `st` is the
exam_config.syllabus_transition block (blueprint_core Cluster SYLLABUS ERA;
sole writer of the block: PYQDraft, R29). The engine is the ONLY source of
these lines — never compose them by hand. The set it returns (Release A):
    traced-inactive → "Syllabus declaration present but inactive: <reason>"
    keys absent / silently inactive (no block, or SC=No with no EF) → nothing
      (§7 P1: the legacy estate's footers are byte-identical; R25)
    active → nothing YET — the §5.9 ACTIVE-mode lines (blend label with
      n_new always printed, coverage X/Y, style donors, R22 converged flip)
      arrive with Release C and will extend the SAME engine function; no
      hand-composed interim line may be printed for an active exam.
An inactive-trace line is DISCLOSURE of a half-declared state, not an error
banner: the run completed normally (R4 — inactive is never invisible, never
fatal). Exactly the engine's lines and nothing else (the §FOOTER-STYLE
single-line discipline applies identically here).

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


§FOOTER-SYL-ACTIVE (v1.32 — GAP-2026-09-01 §5.9; completes §FOOTER-SYL)

For an ACTIVE transition, every F1/F2 footer renders the line(s) from
bc.transition_footer_lines(block, n_new, coverage_text, style_donor,
dials) — pre-converged: "SYLLABUS TRANSITION — weights from equal-share
prior blended with {n_new} measured sitting(s) (n_new={n}); NEW-content
style from {donor}; coverage {X}/{Y}."; converged (n_new >= D-6):
"SYLLABUS TRANSITION — weights effectively measured (n_new={n})." The
label never changes behaviour; n_new is always printed. MockDeliver hands
this step the inputs (count-manifest n_new, BV-COVERAGE text, style-donor
note). The Release-A traced-inactive line (bc.syllabus_footer_lines) is
unchanged; the two surfaces are disjoint by status.

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
R6. DELIVERY-ECHO (v1.34 — GAP-2026-09-14-DELIVERY-ECHO; full contract in §9).
    present_files is performed by the model, so its RESULT is the only proof a
    file shipped. The footer is built from that result, never from intent:
    (a) call present_files ONCE with EVERY path the step's tool output printed
        under "DELIVERY SET"; (b) read the paths the tool RETURNED; (c) any
        printed path not returned → call present_files again with exactly the
        missing paths, BEFORE writing the footer; (d) one table row per RETURNED
        path, plus one ❌ row per path still not returned; (e) the F2 header line
        is "[k] of [n] delivered" from those counts. NEVER a halt (owner
        decision 2026-09-14): a file that could not be attached is a named row,
        never a silent omission and never a stop.
```

### §4-1 — F2 step-complete footer (GREEN) — Markdown template

The literal structure to emit (substitute [bracketed] values; keep everything else):

```
🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

## ✅ Step [N] · [StepName] — Complete

`[ExamCode]`  ·  [k] of [n] delivered

**📦 Deliverables**

| # | File | Action |
| :---: | :--- | :--- |
| 1 | `[ExamCode]_<file1>.<ext>` | [icon] [badge] |
| 2 | `[ExamCode]_<file2>.<ext>` | [icon] [badge] |
| 3 | `[ExamCode]_<file3>.<ext>` | ❌ NOT DELIVERED — [reason] |

> ### → Next: Step [N+1] — [NextStepName]
> Start in a **new chat**. [one short line on what the next step does]
>
> `Pipeline  [11-cell 🟩/⬜ bar]  [N] of 11`

Thank you! 🎯

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
```

v1.34 (R6): `[k] of [n] delivered` — k = paths present_files RETURNED, n = paths the
tool output printed under DELIVERY SET; k == n on a clean run. Row 3's form
`❌ NOT DELIVERED — [reason]` exists ONLY for a printed path the tool never returned
after the R6 (c) retry; on a clean run no such row is emitted. Any "NOT DELIVERED
THIS RUN" line the step printed (a dormant profile, an ungenerated conditional
artefact) is repeated beneath the table, each prefixed "ℹ️ ".

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

      Q0c (v1.37.0, Steps 7 and 9; v1.41.0 — also PYQExplain, RE-25 lines only): does
            the run carry any AMBER-CLASS §LADDER line —
            a certificate amber_note, a terminal-rung repair ("Q<n> repaired at …"),
            "systemic: …", a difficulty or allocation amendment, "difficulty schedule
            unverified…" (EXCEPT its "(no difficulty profile in the project)" variant,
            which is INFORMATIONAL), "renderer degraded (…)", "Q<n> explanation degraded
            (…)" (Step 9), or "A-READ: …"? The auditor reports
            AMBER figure advisories as WARN lines (no exit 1 — Q8b "ALWAYS complete");
            the certificate is what carries them here.
            YES → Render F1 (AMBER) and print every §LADDER line. The paper IS
                  certified and IS delivered.
            NO  → print the INFORMATIONAL §LADDER lines (if any) and continue to Q1.

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

## §LADDER — REPAIR-LADDER, DRAWING AND LEVEL DISCLOSURE (v1.37.0 — GAP-2026-11-02)

```
Step 7 prints, one per line, every line that applies. AMBER-CLASS lines (prefix "⚠️ ")
force F1 through Q0c; INFORMATIONAL lines (prefix "ℹ️ ") never change the footer colour:
  • "Q<n> repaired at <R4|R4'|R5> (<finding>)" — every item that reached a TERMINAL rung
    (R1-R3 repairs are recorded in registry.question_index[].ladder, not printed).
  • "systemic: <finding>" — >= 3 items of this paper reached a terminal rung for it.
  • "difficulty schedule amended: mock <k> <section> <from> -> <to>" — one line per
    bp['difficulty_amendments'] entry whose reason is NOT 'recomputed' (every R5
    accept-at-measured; the entry carries no question number — the question is named by
    its "Q<n> repaired at R5" line above).
  • "allocation amended: <from_subtopic> -> <to_subtopic>" — every R5 reassignment.
  • "difficulty schedule recomputed from its provenance (mock <k>: <from> -> <to>)" — one
    line per difficulty_amendments entry with reason 'recomputed' (S3-2D).
  • DIFF_SRC_NOTE: "difficulty schedule unverified[ — outside the expected range]" —
    AMBER-CLASS (the blueprint can be regenerated with provenance); its variant
    "difficulty schedule unverified (no difficulty profile in the project)" —
    INFORMATIONAL (no profile exists to verify against: a 2-/4-band vocabulary, or an
    exam that has not run PYQExplain — nothing the run could have done differently).
  • STYLE_NOTES "renderer degraded (…)" — AMBER-CLASS.
  • STYLE_NOTES "drawing style from framework defaults" / "drawing style measured;
    structure print sizes from framework defaults (…)" / "level control: rubric +
    independent rating only (content-complexity model dormant)" — INFORMATIONAL.
  • every certificate amber_note (AMBER figure advisory), verbatim.
  • v1.39.0 (D3 a): "blueprint amended in this run (…) — informational; nothing to upload" /
    "project auditor copy is missing or older than the verified repo auditor — this run used
    the verified repo auditor; informational, nothing to upload" (MockTestCreate S13-6
    INFO_LINES_S136) — INFORMATIONAL. Never an upload instruction, never a third file.
  • "spec read: <spec> <lines> lines sha <first 12 of sha256>" — one per READ RECEIPT
    (MockTestCreate S3-1, bootstrap --receipt) — INFORMATIONAL; "A-READ: <what>" when the
    run declared a trimmed / summarised / partial working copy of a spec (prohibited) —
    AMBER-CLASS.
  • Step 9 (Framework_MockTestExplain self-audit terminal rung): "Q<n> explanation degraded (<item>)" —
    AMBER-CLASS, one per disclosed block.
  • v1.41.0 — RE-25 CHEM-STRUCTURE (GAP-2026-11-06; MockTestExplain v1.54.0 AND PYQExplain
    v2.28 — PYQExplain prints these lines too, through the same Q0c):
      - "renderer degraded (RE-25: rdkit unavailable, <N> questions)" — AMBER-CLASS (the
        existing STYLE_NOTES "renderer degraded (…)" class).
      - "Q<n> explanation degraded (RE-25: <reason>)" — AMBER-CLASS; a question that hit
        the three-attempt bound (EC-41) or a figure the layout fallback could not pass.
      - "document size <X> MB (RE-25 figures)" — INFORMATIONAL; printed when a delivered
        docx exceeds 25 MB (EC-37). Never a stop, never an upload instruction.
  • v1.38.0 (GAP-2026-11-03) QUALITY LINES, Step 7 / Step 11:
      - QUALITY_FOOTER_LINE (S3-2e; bc.degraded_footer_line): "DEGRADED QUALITY — dormant
        controls: <ids> (inputs missing or stale; OD-1: run continued)" — AMBER-CLASS; or
        "Quality controls: all ACTIVE." — INFORMATIONAL.
      - "NOT CERTIFIED — uncertified items: Q<a>, Q<b> (<finding ids>)" — AMBER-CLASS; one
        line when certificate.uncertified_items is non-empty (OD-9). Step 11 adds
        "delivered with --accept-uncertified (owner)" — INFORMATIONAL — when it was.
      - v1.39.0 (D0): "independent review: round <k>, <n> item(s) repaired" — INFORMATIONAL
        (batch_state.review_summary); "+ (same-session review — no sub-agent in this
        runtime)" appended when review_summary.reviewer lists 'same-session' (D1) —
        INFORMATIONAL; "independent review not run on Q<a>, Q<b> (<reason>)" when
        review_summary.not_run is non-empty — AMBER-CLASS. Never a user instruction: the
        review is never handed to the user and there is no review packet or --resume.
      - Step 11 (MockDeliver v1.25.0, D5 a): "re-certified Q<a>, … — their only finding was a
        2026.11.03 A-TEMPLATE stamp (default cap / paper-wide count)" (RECERTIFIED_ITEMS) —
        INFORMATIONAL.
      - "shape plan: <shape> infeasible in this paper (no capable slot)" — INFORMATIONAL.
      - "bench card: see A-PYQBENCH in the audit report" — INFORMATIONAL.
  Every line not marked INFORMATIONAL above is AMBER-CLASS. A clean paper (no repair past
  R3, no amendment, measured or no figures, verified schedule) renders green.
These lines are DISCLOSURE: nothing here stops, voids or re-runs anything.
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
After PYQ-1    → (after the exam's LAST PYQ paper) Step 5: PYQExtract --synthesise ALL
                 again, with the Sorted PYQ .docx files attached or in Project Files, so
                 section_rules.md carries the profile's ask-type / representation
                 / abbreviation evidence (v1.37.0); then Step 6 / 6S as usual
After Step 6   → Step 7: MockCreate M1
After Step 6S  → Step 7: TestCreate P1 --level … --scope …          (v1.24)
After Step 7   → Step 9: MockExplain M[N] · TestExplain P[N] (scoped)   (Step 8 retired — 2026.08.03.5)
After Step 9   → Step 11: MockDeliver M[N] · TestDeliver P[N] (scoped) (Step 10 retired — 2026.08.03.5)
                 … ALWAYS: PASSED, DISCLOSED (gate not met — delivered with the
                 §FOOTER-DG line) or DORMANT. (v1.29: the Step 7-R / 9-R repair
                 steps are retired — 2026-08-27.)
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
reads the delivered registry from Project Files OR attached to its own trigger
(REGISTRY-SOURCE-LAW, v1.33 — pp.resolve_registry; the attachment wins when both
exist); an undelivered change is a change the pipeline never sees.

REGISTRY-SOURCE-LAW (v1.33 — GAP-2026-09-14-REGISTRY-SOURCE, owner decision 2026-09-14).
Every step that REQUIRES [ExamCode]_registry.json (Test/MockCreate, Test/MockExplain,
Test/MockDeliver) resolves it ONLY through pp.resolve_registry from two lawful lanes —
the chat attachment (/mnt/user-data/uploads) and Project Files (/mnt/project). The
attachment wins when both hold a file (a difference is printed, never a stop); HARD
STOP only when both are absent; exact filename + exam_code are validated; a run pins
the fingerprint it started from and refuses a different registry on a later turn.
This law changes WHERE the file is read and nothing else: the badge text above, the
writers, the closed set and every artefact are as before. Enforced by
LAW_REGISTRY.json REGISTRY-SOURCE-LAW and mock_sync_audit MS-20.

WRITERS (paper_pipeline.RH_REGISTRY_WRITING_STEPS): Test/MockCreate (Final Assembly),
Test/MockExplain (§7A-M). (v1.29: the retired repair steps are no longer writers.)
READER: Test/MockDeliver (delivers the registry only when its preflight healed it).

DECIDED BY pp.registry_changed(project fingerprint, working copy) → pp.handoff_set(step, …)
— the CLOSED set and badge per file. The footer prints pp.handoff_footer_lines(HANDOFF)
VERBATIM, then HANDOFF['lines']. Never composed by hand, never decided by prose.

WHY A LAW. Four steps wrote the registry, one delivered it, every gated paper was
undeliverable. MS-14 bans the old wording; LAW_REGISTRY.json REGISTRY-HANDOFF-LAW.
```

---

## §9 — DELIVERY-ECHO (v1.34 — GAP-2026-09-14-DELIVERY-ECHO)

```
THE RULE. Every step delivers its closed set through ONE present_files call whose
argument is COPIED from the tool output, and proves the delivery from the call's
RESULT. Applies to EVERY present_files call in EVERY spec (both pipelines, every
batch, final or not). Owner decision 2026-09-14: this rule NEVER halts a step.

WHY. present_files is CLASS T — the python `def present_files(paths): pass` does
nothing; the model performs the real call in its own turn. Through v1.33 the
model performed it from memory: the closed set was built in python and never
printed (PYQExplain S19-2, PYQExtract deliver_final, PYQScan S3-5), and no step
read what the call returned. On a final batch the set grows (docx → docx + json +
profile) while the tool output looked exactly like every earlier batch, so the
"one docx per present_files" habit won and the footer — composed from intent —
listed files that were never attached. Steps 7/9/11 were immune because
pp.handoff_footer_lines prints the set into the tool output first; this section
generalises that pattern and adds the missing half: reading the result.

CONTRACT — three phases around the single call:

  PHASE 1 — PRINT (python, before the call). The step's delivery code prints,
    immediately before the call and as the last lines of its own output:
        DELIVERY SET (n files) — pass EXACTLY these paths to present_files, ONE call:
          /mnt/user-data/outputs/<file 1>
          …
    and, for every path in the set that does not exist on disk:
        DELIVERY WARN: <file> not staged on disk — delivering the rest; it becomes a
        NOT DELIVERED row (R6 (d))
    A missing file is REPORTED, never asserted (no SystemExit, no raise): the
    step ships what exists and the footer names what did not (R6 (d)). Any file the
    step deliberately withholds this run (a dormant profile, an unchanged
    registry, a conditional artefact that was not generated) is printed on its
    own "NOT DELIVERED THIS RUN: <file> — <reason>" line so that an absent file
    is never mistaken for a forgotten one.

  PHASE 2 — CALL + ECHO (model). Call present_files ONCE with the printed paths.
    Read the RETURNED paths (basenames). Compare to the printed set:
      every printed path returned      → proceed to PHASE 3.
      some printed path not returned   → call present_files AGAIN with exactly
                                         the missing paths, then re-compare. At
                                         most one retry; whatever is still not
                                         returned is a ❌ row in PHASE 3.
    A retry is a delivery, not a fault: it needs no apology line and no re-run.

  PHASE 3 — FOOTER (model). Build the footer from RETURNED paths only:
      one numbered row per returned path, badge from §3;
      one "❌ NOT DELIVERED — <reason>" row per printed path never returned
        (reason = the PHASE 1 WARN text, or "present_files did not return it");
      F2 header line: "`[ExamCode]`  ·  [k] of [n] delivered" (k returned, n
        printed). k == n on a clean run. k < n is disclosure, not a stop.
      The NOT-DELIVERED-THIS-RUN lines of PHASE 1 are repeated beneath the table,
        each prefixed "ℹ️ ", so the operator sees WHY the row is absent.

WHAT THIS IS NOT. It is not a gate: nothing here can halt a step, and it adds no
auditor. Steps 7/9/11 keep pp.handoff_set / pp.verify_handoff_outputs unchanged —
their HARD STOP on outputs != closed set is pre-existing and is NOT propagated to
any other step. Engines are untouched (owner decision).

STEP COVERAGE. Release A (2026.09.15.1): this contract + the three steps where the
set is built in python and was never printed — PYQExplain S19-2, PYQExtract
S8-4 deliver_final + per-batch site, PYQScan S3-5 (each carries its own copy of
the helper below). Release B (2026.09.15.2): the fourteen prose-only delivery
sites — Steps 1, 2a, 2c, 3, 4, 6, 6S, PYQ-3, PYQ-4, L2, NB, NC, NA, ND — each
carry a DELIVERY-ECHO block naming their closed set and pointing at the canonical
helper below. Every present_files call in the framework is now covered.
```

CANONICAL HELPER — copy this fence verbatim into the last python cell before the
present_files call (the Release A specs carry their own identical copy):

```python
def print_delivery_set(paths, withheld=()):
    """DELIVERY-ECHO PHASE 1 — Framework_DeliveryFooter §9 / R6 (v1.34).
    Prints the CLOSED set the model must pass to ONE present_files call, warns on
    any path absent from disk, and names every file deliberately withheld this run.
    Reports only — never raises (owner decision 2026-09-14: this never halts).
    Byte-identical copy in every spec that builds a delivery set in python
    (PYQScan / PYQExplain / MockTestAnalyse) — audit_deep XSPEC-DRIFT keeps it so."""
    import os as _os
    print(f"\nDELIVERY SET ({len(paths)} files) — pass EXACTLY these paths to "
          f"present_files, ONE call:")
    for _p in paths:
        print(f"  {_p}")
        if not _os.path.exists(_p):
            print(f"DELIVERY WARN: {_os.path.basename(_p)} not staged on disk — "
                  f"delivering the rest; it becomes a NOT DELIVERED row (R6-d)")
    for _name, _why in withheld:
        print(f"NOT DELIVERED THIS RUN: {_name} — {_why}")
```
