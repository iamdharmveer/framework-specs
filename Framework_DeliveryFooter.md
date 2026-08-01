# Framework_DeliveryFooter v1.9 — Universal Delivery Footer Contract
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
    - Step 5 PYQExtract: after final batch + auto-synthesis + all 6 files
    - Step 6 MockBlueprint: after B3 final delivery of all 8 files
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
           Step 7 re-delivering updated registry.json after each batch.

BADGE 3 — "Use locally"               (icon: 📁)
  When   : File is NOT meant to be uploaded to project Files.
  Example: blueprint.xlsx (not readable by Claude in project knowledge).
           Sorted PYQ .docx (goes to Google Drive, not project Files).
           PYQ_Frequency.xlsx (reference only).
```

### Badge determination logic

```python
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
        'Mock*_Create_Complete.docx', # Step 8 rectified (distinct filename)
        'Mock*_audit_changelog.md', # Step 8 conditional (only if Qs regenerated)
        'Mock*_Explanation.docx',     # Step 9 solutions (same file each batch)
        'Mock*_Explanation_Complete.docx', # Step 10 audited solutions
        'Mock*_Final.docx',        # Step 11 tagged final deliverable
        'analysis_summary.md',      # Step 5 final — human review audit trail
    }

    # CONTEXT-DEPENDENT FILES (not in LOCAL_ONLY — badge varies by delivery context):
    #   analysis_progress.json:
    #     Step 5 mid-step delivery → Upload/Replace in Project Files (session resume)
    #     Step 5 final delivery    → Use locally (keep for future re-runs)
    #   Claude determines the correct badge from §3 registry per step + context.
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
═══════════════════════════════════════════════════════════════════════
STEP 1 — PYQPrepare
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 per exam paper (single response, no batches)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_DD-Mon-YYYY[_<session>].docx  → Use locally
    (User uploads to [ExamCode] project Files or Google Drive PYQ folder)

NEXT STEP  : Step 2a: PYQDraft
NOTE       : Step 1 runs once per raw exam paper. If multiple papers exist,
             user triggers Step 1 separately for each. After ALL papers are
             converted to Row files, proceed to Step 2a.

═══════════════════════════════════════════════════════════════════════
BADGE NOTE — FIRST-BATCH vs SUBSEQUENT-BATCH
═══════════════════════════════════════════════════════════════════════
For batch-based steps (2b, 5, 6, 7, 9), the badge for a file depends
on whether it already exists in project Files at the time of delivery.
  - First batch delivering a file  → "Upload to Project Files"
  - Subsequent batches (same file) → "Replace in Project Files"
The badges shown below represent the TYPICAL case. Claude determines
the actual badge at runtime using the §2 logic (check if file exists).

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

FINAL DELIVERABLES (5 files):
  [ExamCode]_section_rules.md        → Upload to Project Files
  [ExamCode]_subtopic_manifest.json  → Upload to Project Files
  [ExamCode]_PYQ_Frequency.xlsx      → Use locally (Step 6 input — user provides when needed)
  [ExamCode]_analysis_progress.json  → Use locally (keep for future re-runs if adding papers)
  [ExamCode]_analysis_summary.md     → Use locally (human review audit trail)

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

B3 FINAL DELIVERABLES (8 files — per Blueprint v1.42 / CreateAudit v2.12):
  [ExamCode]_blueprint.xlsx          → Use locally (xlsx not readable by Claude)
  [ExamCode]_blueprint.json          → Replace in Project Files
  [ExamCode]_registry.json           → Upload to Project Files
  [ExamCode]_ExplainLearnings.md     → Upload to Project Files
  [ExamCode]_ExplainAuditLearnings.md → Upload to Project Files
  [ExamCode]_mock_test_audit.py      → Upload to Project Files (Step 7 optional, Step 8 mandatory)
  blueprint_core.py                  → Upload to Project Files (BARE name — Step 8 A-FIGPROFILE)
  figural_core.py                    → Upload to Project Files (BARE name — Step 8's 12 A-FIG* gates)

  NOTE (v2.12): the last two keep their BARE names — no [ExamCode]_ prefix. They are
  imported as Python modules; renaming breaks `import blueprint_core` and silently
  reduces Step-8 coverage (the affected gates then report WARN skips instead of
  running). The audit still completes either way — no engine condition halts a run.

NEXT STEP  : Step 7: MockCreate M1

═══════════════════════════════════════════════════════════════════════
STEP 7 — MockCreate
═══════════════════════════════════════════════════════════════════════
PARTS      : Multiple batches per mock + final assembly
FOOTER TYPE: F1 (mid-step) after each non-final batch
             F2 (step-complete) after final assembly

MID-STEP DELIVERABLES (per batch — cumulative whole-paper):
  [ExamCode]_Mock[N]_Q1to[K].docx    → Use locally
  (K = last Q number in this batch; filename grows: Q1to10, Q1to20, ...)

FINAL DELIVERABLES:
  [ExamCode]_Mock[N]_Create.docx   → Use locally
  [ExamCode]_registry.json           → Replace in Project Files

NEXT STEP  : Step 8: MockCreateAudit M[N]

═══════════════════════════════════════════════════════════════════════
STEP 8 — MockCreateAudit
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_Mock[N]_Create_Complete.docx   → Use locally
    (DISTINCT filename — reads Mock[N]_Create.docx, writes Mock[N]_Create_Complete.docx)
  [ExamCode]_registry.json           → Replace in Project Files
    (re-synced from rectified paper)

CONDITIONAL DELIVERABLE (only when ≥1 question was regenerated):
  [ExamCode]_Mock[N]_audit_changelog.md → Use locally
    (author-only BEFORE→AFTER diff; NOT produced if zero regenerations)

NEXT STEP  : Step 9: MockExplain M[N]

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

FINAL DELIVERABLES (same file, now fully explained):
  [ExamCode]_Mock[N]_Explanation.docx  → Use locally

NOTE: registry.json is NOT delivered by Step 9 (frozen/read-only).

NEXT STEP  : Step 10: MockExplainAudit M[N]

═══════════════════════════════════════════════════════════════════════
STEP 10 — MockExplainAudit
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_Mock[N]_Explanation_Complete.docx → Use locally

NEXT STEP  : Step 11: MockDeliver M[N]

═══════════════════════════════════════════════════════════════════════
STEP 11 — MockDeliver
═══════════════════════════════════════════════════════════════════════
PARTS      : 1 (single response)
FOOTER TYPE: F2 (step-complete) — always

DELIVERABLES:
  [ExamCode]_Mock[N]_Final.docx     → Use locally

NEXT STEP  : Pipeline complete for this mock.
             For next mock: Step 7: MockCreate M[N+1]
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
> ### 🏁 Pipeline complete for [ExamCode] Mock [N]
> Next mock: **Step 7 — MockCreate M[N+1]** in a new chat. Thank you!
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
  Example — Step 3 : 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜  3 of 11
  Example — Step 8 : 🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜  8 of 11

BATCH BAR (F1 only): exactly 12 cells.
  filled = round(12 × X / Y). Render `filled` × 🟨 + (12 − filled) × ⬜.
  Label: "[X] of [Y]". If Y (total batches) is unknown, OMIT the bar line.
  Example — batch 1 of 3 : 🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜  1 of 3
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

      NO  → continue to Q1.

      WHY THIS EXISTS. A step could previously report a FAIL and still render
      "Step Complete" in green. That is exactly what shipped the reference run:
      153/153 figural questions unobserved, 45/45 FIGURAL subtopics with an empty
      object-type profile, QV-9 PASS, and a green F2 footer. Green is a claim
      that the artefact is fit to hand downstream; a FAIL means it is not.

      THIS IS NOT A HALT. The step still COMPLETES, still delivers every file, and
      the operator may still proceed. Amber reports; it does not block. The whole
      point of the fix is that a failure is VISIBLE, not that work stops.

      A WARN does NOT force amber — WARN is advisory and the distinction has to
      stay meaningful, or every run turns amber and the signal is lost again.

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
After Step 7   → Step 8: MockCreateAudit M[N]
After Step 8   → Step 9: MockExplain M[N]
After Step 9   → Step 10: MockExplainAudit M[N]
After Step 10  → Step 11: MockDeliver M[N]
After Step 11  → Pipeline complete for Mock [N].
                 Next mock: Step 7: MockCreate M[N+1]
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
