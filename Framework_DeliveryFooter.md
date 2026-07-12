# Framework_DeliveryFooter v1.6 — Universal Delivery Footer Contract
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
#   v1.6 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#          Per-step registry (§3) + LOCAL_ONLY badge globs (§2) updated to the new
#          deliverable names: Step 7 Complete→Create, Step 8 Complete→Create_Complete,
#          Step 9 Solutions→Explanation, Step 10 Solutions_Audited→Explanation_Complete,
#          Step 11 Tagged→Final. The single Mock*_Complete.docx glob is SPLIT into two
#          distinct patterns (Mock*_Create.docx + Mock*_Create_Complete.docx) since Step 7
#          and Step 8 outputs are now distinct files. Glob cross-match + badge logic
#          re-tested: each delivered file matches exactly one pattern. The v1.2 changelog
#          entries below are preserved as history and intentionally keep the old names.
#   v1.5 — 2026-07-09 — RENDERING CONTRACT REBUILT (widget dependency removed).
#          ROOT CAUSE of the intermittent footer failures seen across the pipeline:
#          §4 mandated rendering via the LOCAL show_widget / visualizer MCP server.
#          Whenever that local server was down, not loaded, timed out, or simply
#          unreachable (a teammate on a different machine, mobile, web, or a
#          scheduled run), the footer silently degraded to improvised text — an
#          ASCII banner one time, bullets another, a monospace block a third — which
#          reads as "broken." Same spec, different result per run = an external
#          dependency, not a logic bug. Proof: identical steps rendered clean in some
#          sessions and broke in others; one session even printed "the local
#          visualizer MCP server timed out."
#          FIX: §4 is now a PURE-MARKDOWN contract requiring ZERO external tools.
#          It renders byte-identical on every surface and every team member's machine.
#          (1) §4 fully rewritten: Markdown templates replace all HTML/widget structure.
#          (2) State COLOR THEME via Unicode emoji bands — GREEN (complete) /
#              AMBER (in progress) — renders identically everywhere (no CSS).
#          (3) §4-0 rules: canonical Markdown is MANDATORY; show_widget/visualizer is
#              FORBIDDEN; improvised fallbacks (ASCII banners, monospace footers,
#              ad-hoc lists) are FORBIDDEN. The template is the only permitted output.
#          (4) §4-4 added: deterministic progress bars (no guessing at position).
#          (5) §1 VISUAL IDENTITY blocks are SUPERSEDED by §4 (pointer note added at
#              the top of §1). §1 WHEN-TO-SHOW and CRITICAL RULES logic unchanged.
#          (6) Badge WORDING unchanged (§2). Optional scan icons added: 📤 Upload /
#              🔁 Replace / 📁 Use locally.
#   v1.4 — 2026-07-07 — STEP 1 REGISTRY ADDITION.
#          Framework_PYQPrepare v1.0 now exists — Step 1 is no longer manual/external.
#          (1) Replaced NOTE ON STEP 1 exclusion block with full Step 1 registry entry
#              (Row file, F2 step-complete, "Use locally" badge, next = Step 2a).
#          (2) Added Row file pattern to LOCAL_ONLY in §2 badge logic.
#          (3) Added "After Step 1 → Step 2a" to §6 next-step reference table.
#   v1.3 — 2026-07-07 — AUTOMATED CROSS-CHECK (1 context-dependent badge bug fixed).
#          Custom Python audit script tested all 39 file×context combinations against
#          LOCAL_ONLY patterns. Found 1 conflict: analysis_progress.json was in LOCAL_ONLY
#          but Step 5 mid-step delivery needs Upload/Replace (for session resume). The
#          file has DUAL behavior: mid-step=project Files, final=local. Moved to a new
#          CONTEXT-DEPENDENT section in the pseudocode with explicit documentation.
#   v1.2 — 2026-07-07 — DEEP SOURCE-SPEC CROSS-CHECK (5 filename/deliverable bugs fixed).
#          Every step's deliverables verified line-by-line against its source spec.
#          (1) Step 7 per-batch filename: Mock[N]_Batch[B].docx → Mock[N]_Q1to[K].docx
#              (cumulative whole-paper, per Framework_MockTestCreate S4-10).
#          (2) Step 8 filename: Mock[N]_Rectified.docx → Mock[N]_Complete.docx
#              (same filename as Step 7 — replaces input, per MockTestCreateAudit S0-2).
#          (3) Step 8 missing conditional deliverable: Mock[N]_audit_changelog.md added
#              (delivered ONLY when ≥1 question regenerated, per S0-2).
#          (4) Step 9 per-batch: Mock[N]_Solutions_Batch[B].docx removed — spec delivers
#              the SAME Mock[N]_Solutions.docx each batch (whole-paper incremental, per
#              MockTestExplain S19-2 + RE-8). Mid-step and final = same file.
#          (5) §2 LOCAL_ONLY: fixed patterns to match actual filenames — removed
#              Rectified/Solutions_Batch (don't exist), added Q1to*/audit_changelog.
#   v1.1 — 2026-07-07 — EXHAUSTIVE AUDIT (12 bugs fixed).
#          (1) Step 6 B3: added mock_test_audit.py as 6th deliverable (Blueprint v1.20).
#          (2) Step 2b/5 first-batch badge: fixed "Replace" → dynamic Upload/Replace.
#          (3) Step 4: added count_progress.json session-break interim deliverable.
#          (4) Step 2c NEXT STEP: removed wrong "parallel" claim (Step 4 depends on Step 3).
#          (5) Step 3 NEXT STEP: removed nonsensical "(if not already done)" qualifier.
#          (6) §2 LOCAL_ONLY: added all mock paper file patterns.
#          (7) Step 1 PYQPrepare: added exclusion note.
#          (8) Step 5 final: analysis_progress.json + analysis_summary.md → Use locally
#              (per PYQAnalyse handoff: "KEEP LOCALLY").
#          (9) §5: added session-break edge case (F1 variant for forced context-limit breaks).
#          (10) §6 reference table: synced with §3 fixes.
#   v1.0 — 2026-07-07 — Initial release. Two footer types defined.
#          Per-step deliverable registry with action badges.
#          Decision logic for mid-step vs step-complete.

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
    - Step 5 PYQExtract: after final batch + auto-synthesis + all 5 files
    - Step 6 MockBlueprint: after B3 final delivery of all 6 files
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

B3 FINAL DELIVERABLES (6 files — per Blueprint v1.20):
  [ExamCode]_blueprint.xlsx          → Use locally (xlsx not readable by Claude)
  [ExamCode]_blueprint.json          → Replace in Project Files
  [ExamCode]_registry.json           → Upload to Project Files
  [ExamCode]_ExplainLearnings.md     → Upload to Project Files
  [ExamCode]_ExplainAuditLearnings.md → Upload to Project Files
  [ExamCode]_mock_test_audit.py      → Upload to Project Files (Step 7 optional, Step 8 mandatory)

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
