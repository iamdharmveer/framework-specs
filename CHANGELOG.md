# Changelog

## 2026.07.31.4
- bootstrap.py advisory REWORDED (context-cost defect, found during the corpus_io.py length
  analysis): `--trigger` printed one line — "Entry-point spec(s) ... read IN FULL:" — listing
  the WHOLE route, engines included. Followed literally, a PYQCount session would read 2,641
  spec lines PLUS 9,316 engine lines (corpus_io 4,399 + blueprint_core 3,226 +
  reconcile_taxonomy 1,248 + syllabus_provenance 443) into context; engines are executed, not
  read, so all 9,316 of those lines were dead weight. The advisory now prints two lists:
  .md specs "READ IN FULL" and .py engines "EXECUTE via import; do NOT read into context".
  Verification contract untouched (same checks, same exit codes, same .verified token);
  nothing machine-parses the advisory line (verified by corpus grep). Matching one-line
  clarification in mocktestframework_SKILL.md rule 2 and in the installed-skill SKILL.md
  shipped alongside.
- corpus_io.py itself: analysed and deliberately UNCHANGED. Its 4,399 lines cost sessions
  nothing (engines are executed, never required reading); it is the consolidation artifact
  for previously-drifting copies (Cluster K readers, is_option), so splitting it would
  reopen that defect class; its docstrings/comments are consumed by audit_callgraph
  (parameter contracts), audit_specs_ext V-SYNC (sync rules) and encode GAP-numbered defect
  history, so trimming them risks three auditors for zero runtime gain. Health verified: no
  dead public functions (5 external-orphan suspects each have 2-5 internal call sites),
  no layering violation (blueprint_core imports stdlib only), callgraph 0 findings.
- LATENT COUNT DEFECT FIXED (both SKILL copies): release 2026.07.31.2 set the skill's
  engine count to 9 (tracked scripts), but CHECK AA and audit_sync count engines ROUTED
  in routes.json = 8 — validate_framework_md.py is tracked but deliberately never routed
  (it is the CI validator). Any SKILL.md claiming 9 placed where AA reads it fires
  'claims 9 engine scripts; routes.json routes 8'. Both copies now state 8 with the 9th
  script explicitly accounted in the same sentence, so the count matches the checkers'
  definition while preserving the .2 entry's fact.
- MANIFEST.json regenerated for the VERSION stamp (bootstrap.py and skill files are not
  hash-tracked; specs and engines all unchanged — 31 hashes identical to 2026.07.31.3).

## 2026.07.31.3
- Framework_PYQCore v1.0.2: post-deployment deep sync audit found one ownership ambiguity —
  the scaffolding host-note header '## §2-HOSTED — ...' matched the '^## §N' section-header
  pattern, making §2 resolve to two files (Draft owns §2; Core hosts S2-3). Header renamed to
  'HOSTED SECTION S2-3 (from §2 ...)'; §-ownership now unique per file. Scaffolding-only,
  hosted v2.29 content re-verified byte-identical. SPEC_MANIFEST.json: Core entry updated in
  place, 40-file wide baseline preserved. MANIFEST.json regenerated.
- Sync audit result at seal (production 2026.07.31.2 + this fix): bootstrap 31/31; validator
  0 repo issues (sole finding is the environment-side stale installed skill, already tracked);
  check_triggers 24 consistent; audit_sync clear of ERA-SYNC; audit_deep 0; audit_callgraph 0;
  audit_specs_ext 0 across 39 files (full invocation with engines — specs-only invocation
  emits 4 [V-SCOPE] scope warnings by design, not findings). Independent cross-step audit:
  9/9 v2.29 slices byte-identical each in exactly one file; §1-§12 single-owner; 12/12
  artifact producer/consumer placements correct; 4/4 pipeline handoffs in the right files;
  S2-3 single-sourced; companion minimums single-sourced; stub unrouted; 4/4 routes correct.

## 2026.07.31.2
- Seals commit 3bbc36c (Framework_PYQCore v1.0.1 — the ERA-SYNC engine-sourcing line), which
  landed after VERSION had already been stamped 2026.07.31.1. Its substance is described in
  the 2026.07.31.1 entry below; this block exists so the version history and the shipped
  commits stay in step, and to CORRECT three claims in that entry which do not match what
  actually went live:
  - SKILL.md engine count shipped as **9**, not "7→8". figural_core.py became the 9th engine
    in release 2026.07.29.2 and was missing from the count; the uploaded file still said 8.
  - CLAUDE.md was not merely "generalised": the stale bootstrap figure is now stated
    explicitly as **31/31 — 22 Framework_*.md + 9 engines** (was 25/25 — 17 + 8), and the
    SPEC_MANIFEST baseline as **40 files** (was 33).
  - SPEC_MANIFEST.json shipped at **40 files (22 specs + 18 engines/auditors/tooling)**, not
    the 22-file specs-only form the generator emitted. Narrowing it would have dropped the
    second integrity baseline for all 9 engines, the 4 audit scripts and routes.json, which
    contradicts CLAUDE.md's definition of it as "the wider workbench baseline — including the
    audit and tooling scripts".
- Release-manager note: the split was deployed via `main` → `main:production` fast-forward.
  DEPLOY_INSTRUCTIONS.md §D directed `git checkout production` + `git push origin production`,
  which the standing guardrail forbids; the instruction was not followed.
- Verification at seal: bootstrap 31/31, validate_framework_md 0 issues across 22 files,
  check_triggers consistent (24), audit_deep 0, audit_callgraph 0, audit_specs_ext 0 across
  25 files, audit_sync clear of [ERA-SYNC]. MANIFEST.json regenerated independently and found
  byte-identical to the one shipped with the split — 31 file hashes and 24 routes agreeing
  across two separate generations.
- Still open (owner action): the installed project skill at
  /mnt/skills/user/mock-test-framework/SKILL.md must be replaced with the repo copy, or
  audit_sync/CHECK AA keeps reporting the stale 17-spec claim.

## 2026.07.31.1
- Framework_PYQAnalyse v2.29 SPLIT into 5 files with ZERO rule/functionality change
  (owner request: per-step context load; the 6,988-line monolith destabilised chat sessions).
  New architecture: Framework_PYQDraft.md (§2), Framework_PYQScan.md (§3),
  Framework_PYQApprove.md (§4), Framework_PYQCount.md (§5), Framework_PYQCore.md
  (§1 + hosted S2-3 + §6–§12 shared contracts + companion-version minimums). All §/S/EC IDs
  preserved byte-identically; a completeness gate proved every v2.29 body line appears in
  exactly one new file. S2-3 is hosted in Core because PYQScan S3-6 Refinement executes its
  machinery (Domain Check, Q1/Q2/Q3 decision tree, 6 Pattern Dimensions) — §11 already
  declared it universal; single-sourcing it prevents the cross-file drift class of
  GAP-2026-07-25-002 / the triple is_option() defect.
- Framework_PYQAnalyse.md becomes a v3.0 stub (section map) so historical citations resolve.
- routes.json: PYQDraft/PYQScan/PYQApprove/PYQCount now load their step file +
  Framework_PYQCore.md; engine lists unchanged (CHECK AH green).
- Per-session spec read drops from 6,988 lines to 2,240–3,260 (−53% to −68%).
- The v2.0–v2.29 per-file changelog (1,248 lines) moved out of the runtime file into the
  ARCHIVE section at the bottom of this CHANGELOG. A token sweep verified every technical
  identifier in the deleted history is either present in the split body or was already
  history-only in the v2.29 body (nothing lost).
- Framework_PYQCore.md v1.0.1: audit_sync [ERA-SYNC] fired post-split because S2-3's
  prose mentions of OUT_OF_PATTERN landed in Core while the executable bc.OUT_OF_PATTERN
  call sites landed in Framework_PYQScan.md. Added an engine-sourcing comment to the
  S2-3 host note (scaffolding only; hosted v2.29 content remains byte-identical).
  All four audit scripts now report 0 findings.
- Housekeeping: mocktestframework_SKILL.md spec count 17→22 (and engine count 7→8, matching
  routes.json); CLAUDE.md stale "25 files" phrasing generalised; SPEC_MANIFEST.json and
  MANIFEST.json regenerated. Verified: bootstrap 31/31, validate_framework_md 0 issues
  across 22 files, check_triggers consistent. NOTE: the installed project skill
  (/mnt/skills/user/mock-test-framework/SKILL.md) must be replaced with the updated SKILL.md
  shipped with this release, or audit_sync/CHECK AA will keep reporting the stale 17-spec claim.

## 2026.07.29.3
- figural_core: RUNTIME DEPENDENCIES DECLARED, CHECKED AND NEVER FATAL IN AN AUDIT. Closes the
  hard-dependency note recorded in 2026.07.29.2. Step 0 installs python-docx and nothing else,
  and no spec declared a dependency list before v5.33, so the engine's extra needs would have
  been discovered as a traceback in a live exam session.
- Split by role, following "Silence is the defect; a halt is not the remedy": RENDER (Create)
  genuinely requires matplotlib, so render_figure() now raises FiguralError G-FIGDEP carrying
  the pip command instead of a bare ImportError from three frames down; AUDIT degrades every
  gate to DORMANT-but-reported, routed to AMBER by triage(). A gate that raises is worse than a
  gate that is absent, because it takes the whole audit down — and an audit that dies takes
  ~200 projects with it.
- New surface: DEPENDENCIES (matplotlib, PIL, numpy, scipy, fontTools with each one's role),
  PIP_INSTALL, and preflight() so a missing package is a stated precondition rather than a
  traceback. Guards IMPORT the module and catch failure rather than asking find_spec whether it
  is on the path — a package can be installed and still fail to load (numpy without BLAS,
  Pillow without its shared libs), and presence-checking leaves exactly the traceback the guard
  exists to prevent. dominant_hues()/coloured_fraction() now return None (not []) when pixel
  tooling is unavailable, so a caller can tell "no hues found" from "could not look".
- Self-test 56 -> 79. The absence fixtures block imports through sys.meta_path rather than a
  builtins.__import__ hook: an earlier version patched __import__ only, so nothing was ever
  blocked and all six cases passed against unguarded code — a test that proved nothing.
- Framework_MockTestCreate v5.33 documents the dependency surface (docs-only; version unchanged
  as behaviour is unaltered). MANIFEST.json + SPEC_MANIFEST.json regenerated.
- bootstrap 26/26, validator 0 issues, audit_deep 0, audit_callgraph 0, audit_specs_ext 0
  across 20 files; blueprint_core 266/266, corpus_io 303/303, figural_core 79/79.

## 2026.07.29.2
- GAP-2026-07-29-FIG-R2 + VERIFY-2026-07-29-FIG-R2 (figure colour, label legibility and
  placement scale). Measured across 208 delivered drawings in four exhibits: 0 of 55 IIT JAM
  figures contained a single coloured pixel; placement scale was 0.500 EXACTLY on 24 of 24
  option canvases; on-page labels ran to a median of 6.7 pt; 0 of 208 drawings carried alt
  text. The three GATE papers believed correct measured 115 of 153 figures below a 9 pt floor —
  not a working reference, only a quieter failure. Four root causes, not one, including RC-1
  (S10-7 Q7 MANDATED "solid black", so the monochrome output was CONFORMANT) and RC-4 (the
  corpus had exactly ONE figure helper, an abstract-geometry GLYPH renderer with no set_xlabel,
  no legend, no rcParams anywhere, being used to draw scientific data figures it structurally
  cannot label).
- NEW ENGINE (the 9th): figural_core.py — shared figure renderer + 12 conformance gates.
  The scale contract is now S == 1.0 BY CONSTRUCTION rather than by luck: display width is a
  LAYOUT decision, the render is solved to fit it, FIG_NATIVE_HEADROOM is retired to 1.0 (it
  was the sole source of the halving) and bbox_inches="tight" is banned (it made saved width a
  function of the figure's own content, so S wandered 0.495..0.666 across 27 canvas sizes).
  Okabe-Ito palette with REDUNDANT encoding (colour is never the sole carrier of meaning),
  pinned/normative CVD arithmetic, and a FigureSpec sidecar that makes a figure auditable
  without vision. Self-test 56/56 with day-one fixtures D1/D2/D5 that fail on the shipped
  defects. Tracked by gen_manifest (bootstrap 25 -> 26) and routed to the four
  Create/CreateAudit triggers.
- Severity model encodes the framework's own doctrine: no image-COLOUR condition may ever halt
  a run (AMBER — report loudly, force the amber footer, always complete); an answer-cue leak
  voids the ITEM not the run (VOID_ITEM); BLOCKING is reserved for renderer-contract
  REGRESSION on v5.33+ output, with EC-V18 downgrading it to AMBER for legacy output that has
  no sidecar, so all ~200 existing exams keep auditing. A gate that throws is worse than a gate
  that is absent — every gate tolerates a partial or empty spec and never raises.
- Specs: MockTestCreate v5.32 -> v5.33 (renders through the engine); MockTestCreateAudit
  v2.10 -> v2.11 (twelve new deterministic Part-A gates, correcting v2.10's over-generalisation
  that "auditing recorded intent, not pixels" applies to every figure property — it is true of
  SEMANTICS and false of colour presence, hue separation, scale and label size).
- HARD DEPENDENCY: figural_core's render path imports matplotlib UNGUARDED, so the four
  Create/CreateAudit triggers now require it at runtime (scipy and fontTools are used too but
  degrade gracefully). Confirm it is present in exam sessions.
- bootstrap 26/26, validator 0 issues, audit_deep 0, audit_callgraph 0, audit_specs_ext 0
  across 20 files; blueprint_core 266/266, corpus_io 303/303, figural_core 56/56.
  MANIFEST.json + SPEC_MANIFEST.json regenerated (35 files).

## 2026.07.29.1
- Debt closure — the three follow-ups recorded in the 2026.07.29 seal are closed, and no
  open debts remain.
- corpus_io v1.10 -> v1.11: (1) the ~300-line Cluster I table-structure addition is now
  RECORDED in its own changelog entry (third un-bumped occurrence, fixed); (2) Cluster I
  gains its missing fixtures — a gridSpan/vMerge table driven through _table_rows and
  read_table_spec (a fixture the old row.cells implementation fails) plus a flat-table
  identity check; (3) the long-open is_option/para_has_image fixtures land (bare-marker
  image options + OPT_PATTERNS cases, open since 2026.07.26.2). Self-test 273 -> 303.
- audit_specs_ext: V-SYNC now recognises a DELEGATION ADAPTER (a copy whose whole body
  calls or aliases the canonical engine copy) and skips it — parity holds by construction,
  and byte-comparing it false-fired on every adapter since the GAP-2026-07-25-002
  consolidation. Peer-window made bidirectional (a forward-only window silently compared
  nothing; verified by targeted mutation). First fully clean audit_specs_ext run across the
  corpus + engines: 0 issues across 19 files.
- All checkers green simultaneously: bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0, audit_specs_ext 0; blueprint_core 266/266, corpus_io 303/303.
  MANIFEST.json + SPEC_MANIFEST.json updated.

## 2026.07.29
- GAP-2026-07-29-TBL (table STRUCTURE survives the pipeline, both halves). The corpus could
  say what a table CONTAINS but never what a table IS: Step 1 S4-3 wrote cell.text into a
  rectangular add_table() and Step 7 S8-4 modelled a DI table as (headers, rows) — so a grouped
  header (a cell spanning four columns over a label spanning two rows) had exactly one
  representable form: squared into a grid and padded with empty strings. Measured on
  SSC_CGL_Tier1 09-Sep-2024 Shift 1: Q.52 and Q.61 each lost a 4-column header span and a
  2-row label span and gained 4 stray empty cells; the delivered Row file carried 0 gridSpan
  and 0 vMerge elements and passed 16/16 checks with a green footer, because no check had ever
  compared a built table with its source. Second defect, same family: one-table-PER-OPTION
  emission — adjacent w:tbl siblings are FUSED by every Word engine (19 tables written came
  back as 7 from a round-trip).
- corpus_io — new Cluster I (table structure): _table_rows rewritten to walk w:tr/w:tc with
  vMerge/gridSpan so a merged header is one anchor cell, never a repeat (flat-table output
  unchanged); new read_table_spec() + TableSpec builder as the ONE table model both steps use;
  legacy {'headers','rows'} DI payload accepted forever (no registry migration); font_name
  parameterised (Row-file contract stays Arial, Step 7 passes its FONT_NAME). Self-test 273/273.
- Specs: PYQPrepare v1.13 -> v1.14 (DI table structure, block composition, cell content —
  part 1); MockTestCreate v5.31 -> v5.32 (S8-4 rebuilt on Cluster I — part 2; two flat builders
  under one concept emit no drift signal until they disagree, so the model now lives once in
  the engine). routes.json: corpus_io.py routed to the Create steps. MANIFEST.json +
  SPEC_MANIFEST.json updated; bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0.
- Follow-ups (recorded, owner-accepted): Cluster I self-test fixture (a gridSpan/vMerge table
  that FAILS on the old row.cells implementation + flat-table byte-identity check) and a
  corpus_io version bump/changelog for the Cluster I addition; is_option fixture still open.

## 2026.07.27
- GAP-2026-07-27 (six defects found by six sessions on one corpus — IIT_JAM_BIOTECHNOLOGY,
  22 papers / 1,719 Qs; five sessions rediscovered the same vision defect and each invented a
  different workaround, while the one session that executed the python fences VERBATIM found a
  P0 no paraphrasing session hit). MockTestAnalyse v2.38 -> v2.39 carries the fixes, including:
  A — taxonomy Source-2 concatenated instead of merging (P0); B — build_vision_queue()
  overwrote its fixed-name outputs and was called per paper (P0), so a 22-paper run retained
  only the last paper's queue; D — XLSX-F9 compared a corpus total to a per-paper denominator
  (P1); E — MSQ under-detection originating in Step 3 (P2).
- GAP-2026-07-27-B (the B fix, both halves): corpus_io v1.8 -> v1.10 — build_vision_queue()
  is now IDEMPOTENT: it reads the existing vision_queue.json and unions prior items with the
  incoming batch, so re-runs and resumed sessions no longer destroy earlier papers' work;
  tag_width is pinned as a floor so surviving tags stay stable, and a genuine hash-collision
  re-tag is reported (tag_generation_changed), never silent. v1.10 adds `fresh=` so run-scoped
  callers (Step 1) can opt out of the union. Release-gate note: the first upload of this wave
  (v1.9) FAILED its own self-test 240/249 — the union broke nine CLUSTER V fixtures sharing
  one workdir — and was STOPPED at the gate; v1.10 isolates each fixture in its own workdir
  and adds positive union coverage. Self-test 273/273.
- PYQPrepare v1.12 -> v1.13 (caller-side half): VISION_WORKDIR was used at three call sites
  without being defined, so Step 1 silently inherited Step 5's workdir — hidden while
  corpus_io overwrote, surfaced by the union. Now defined, distinct per step, and fresh.
- GAP-2026-07-27-E: PYQSort v1.17 -> v1.18 — the ORIGINAL exam position now survives sorting.
  Step 3's taxonomy renumbering destroyed the exam position; Step 5's MSQ detector had only the
  instruction phrase left and measured 24 MSQ across 1,719 questions on an exam whose scheme
  reserves Q31-40 for MSQ (~120 expected), under-representing Section B corpus-wide.
- MANIFEST.json + SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0 issues,
  audit_deep 0, audit_callgraph (incl. C6) 0; blueprint_core 266/266, corpus_io 273/273.

## 2026.07.26.3
- GAP-2026-07-26-003 (EXECUTION-BOUNDARY LAW — a tool call cannot happen inside a running
  Python process). analyse_image_claude() and the vision-probe family were pass-bodied CLASS T
  stubs that a Python loop called and consumed, so vision was unreachable on every run of every
  exam and the literal code raised AttributeError — production silently executed a substituted
  body. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers / 1719 Qs): the four vision fields present
  on 0 of 1719 questions, 153/153 figural questions vision_unavailable, 45/45 FIGURAL subtopics
  shipping an empty object-type profile — with QV-9 PASS and a green Step-Complete footer.
- Fix — vision made reachable via MATERIALISE-THEN-INJECT (Phase A python emits a work queue,
  Phase B the model performs the view() tool calls in-turn as prose, Phase C python consumes the
  results): MockTestAnalyse v2.36 -> v2.38 (vision reachable, then probe family retired),
  PYQPrepare v1.10 -> v1.12 (S1-12 reachable, callback halt replaced), corpus_io v1.6 -> v1.8
  (Cluster V vision Phase A / observation I/O, then probe family deleted). A CLASS T failure is
  now LOUD but does NOT halt.
- GAP-2026-07-26-003 D2 (a measurement with no consumer is not a feature): Step 5 had measured
  each subtopic's real figure profile since v2.29, but Step 7 read only image_role — the semantic
  half was written and consumed by nothing for six minor versions. MockTestCreate v5.30 -> v5.31
  now reads the figure profile; MockTestCreateAudit v2.9.2 -> v2.10 adds gate A-FIGPROFILE.
- DeliveryFooter v1.7 -> v1.8: new §5 Q0 quality gate — any FAIL from a step's own checks forces
  an AMBER footer with the failing check and remedy named, instead of a green Step-Complete. WARN
  does not force amber. Reports, does not halt.
- Tooling / protocol: audit_callgraph gains C6 (model-agency-stub / EXECUTION-BOUNDARY LAW, scans
  every fence not just python-labelled ones); PYQAnalyse tagged its two judgment stubs # CLASS: J;
  CLAUDE.md adds the EXECUTION-BOUNDARY LAW and measurement-consumer guardrails. blueprint_core
  self-test 266/266, corpus_io 249/249; bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0.

## 2026.07.26.2
- GAP-2026-07-26-002 closed (image-option integrity + intra-spec wiring). Three parts:
- (1) is_option consolidated to ONE engine predicate (audit_deep [XSPEC-DRIFT]). v2.34/v2.35
  made is_option() image-option-aware in MockTestAnalyse only; the same-named copies in PYQSort
  and PYQAnalyse kept the text-only form while their docstrings still claimed alignment. Not
  cosmetic: PYQSort USES its copy to count options, so the defect fixed in Step 5 was live in
  Step 1 — measured on IIT_JAM_BIOTECHNOLOGY 2022, 156 options counted against 160 actual. Fix:
  corpus_io v1.5 -> v1.6 now owns is_option + BARE_OPT_PATTERNS + para_has_image as the single
  shared predicate; MockTestAnalyse v2.35 -> v2.36, PYQAnalyse v2.28 -> v2.29, PYQSort v1.16 ->
  v1.17 all delegate (is_option = corpus_io.is_option), and PYQSort passes the paragraph element
  at both call sites so image options are actually counted.
- (2) IMG-6 probe protocol hardened (PYQPrepare v1.9.1 -> v1.10). The v1.6 protocol was
  single-attempt/single-token and recorded nothing, while score_vision_probe() returned False on
  an empty string — so "I did not look" was indistinguishable from a blind session and produced a
  false session-terminating halt in Step 5 on first production use. Now 3 attempts, 3 distinct
  tokens, observation mandatory.
- (3) New auditor audit_callgraph.py (intra-spec call-graph): asserts every documented-required
  parameter is supplied at each call site, every multi-return function has one shape, and every
  public engine function is reached from executable spec code (not prose). Now tracked in
  SPEC_MANIFEST (33 -> 34 files). blueprint_core self-test 184/184; corpus_io 228/228.
- Follow-ups (recorded): add an is_option self-test fixture to corpus_io (bare-marker + OPT_PATTERNS
  cases); update audit_specs_ext's stale V-SYNC that false-fires on the delegation adapters.

## 2026.07.26.1
- GAP-2026-07-26-001 (a multi-paragraph stem is not a heading): PYQSort EC-S8 emits stems
  whose continuation lines are bold, not-date, not-option, not-next-question — character for
  character the level-3 taxonomy-heading predicate in `blueprint_core.is_taxonomy_heading()`.
  Level 3 is the only taxonomy level with no textual prefix, so boldness was its sole positive
  signal; the moment the producer emitted bold body text, a stem continuation and a subtopic
  heading became the same object. Two classes, one predicate, on opposite sides of the repo,
  never compared.
- Fix: `is_taxonomy_heading()` now takes the next paragraph's text (`is_taxonomy_heading(para,
  is_option, next_text)`) so a line followed by more stem body is no longer classified as a
  heading; MockTestAnalyse S3-2 passes `next_text` at both extraction loops — an older engine
  raises `TypeError` rather than silently truncating stems.
- Impact this closed was the silent half: Step 4's phantom-triple gate HARD STOPs loudly, but
  the extractor half kept question counts right (QV parity held, every gate passed) while
  truncating stems at the figure and orphaning every option after it — corruption that flowed
  into section_rules.md, the manifest, the Frequency xlsx, and on into Step 6 allocation and
  Step 7 generation. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers / 1719 questions): 20
  spurious headings across 10 papers, 128 counted triples vs 126 real, 2 phantom triples.
- Specs: Framework_MockTestAnalyse v2.32 -> v2.33, Framework_PYQAnalyse v2.27 -> v2.28.
  Engine: blueprint_core.py (self-test 178/178) — heading predicate gains the `next_text`
  parameter. MANIFEST.json + SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0
  issues across 17 files.

## 2026.07.26
- GAP-2026-07-25-003 (taxonomy read consolidated to ONE reader + lock gate reaches every
  consumer): the last hand-written and prose readers of the approved taxonomy are removed.
  Every step now loads through `corpus_io.load_taxonomy()` and asserts identity through
  `corpus_io.assert_taxonomy_lock()` — one implementation, called everywhere, instead of the
  four-plus transcriptions that produced GAP-2026-07-25-002. The read and the lock assertion,
  previously two calls (and in some steps two independent reads of the same artefact), collapse
  to a single call at each site.
- Preferred source moves from the Analysis Word document to `approval_record.json`: where the
  record carries the taxonomy (reconcile_taxonomy >= v1.3) the consuming steps parse no Word
  document at all; pre-1.3 records fall back to the doc, fully gated, and need no re-run.
- Specs: Framework_Blueprint v1.39 -> v1.41 (S2-2 asserts the lock, then loads through
  load_taxonomy — Step 6 was the worst place for a silently-wrong taxonomy); Framework_MockTestAnalyse
  v2.30 -> v2.32 (both Step-5 readers gated then load through load_taxonomy; a second latent
  defect in `_extract_taxonomy_tuples_from_*` fixed while wiring the gate); Framework_PYQAnalyse
  v2.24 -> v2.27 (Task 2.5 was the last hand-parser — read/write through Cluster K, lock delegated
  to the shared gate, then load through load_taxonomy); Framework_PYQSort v1.14 -> v1.16 (taxonomy
  loaded once from JSON where available; S1-0b/S1-2 collapse to one call; ingest form surfaced,
  EC-S20/S21 recorded).
- Engines: reconcile_taxonomy.py (self-test 69/69) records the approved taxonomy inside
  approval_record.json beside its validating fingerprint; corpus_io.py -> v1.4 (self-test 226/226)
  owns `load_taxonomy()` + `assert_taxonomy_lock()` as the single reader/gate. MANIFEST.json +
  SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0 issues across 17 files.

## 2026.07.25.2
- GAP-2026-07-25-002 (Analysis-doc reader delegation): MockTestAnalyse v2.29.1 -> v2.30
  delegates both Analysis-doc readers (score_difficulty / determine_strip_mode) to
  blueprint_core Cluster E — the byte-identical second copy is replaced by a thin adapter,
  so one definition is called from both places. Blueprint v1.38 -> v1.39 (S2-2 reader
  delegated), PYQAnalyse v2.23 -> v2.24 (S4-2 de-stubbed, taxonomy attested, name-length
  gate), PYQSort v1.13 -> v1.14 (reader delegated + S1-0b content cross-check).
- Engines: blueprint_core (164/164), corpus_io (138/138), reconcile_taxonomy (59/59),
  validate_framework_md.py — +batch checks AF (deliverable-filename contract) and AG
  (shared-artefact readers); Check Z widened to the engine's whole public surface.
- routes.json: engine routing broadened across the PYQ steps. CLAUDE.md: guardrails added —
  deliverable rename/cardinality is a cross-step contract change; a shared artefact has ONE
  reader; producer-enforced bounds. MANIFEST.json + SPEC_MANIFEST.json regenerated.

## 2026.07.25.1
- GAP-2026-07-25-001 (S4-0 silent check-skip): reconcile_taxonomy.py v1.0 -> v1.1 — the
  early `return` inside C4's style-aware branch that disabled C5/C6/C7 for every
  syllabus_style exam is removed; reconcile() is now SINGLE-EXIT. Adds CheckLedger
  (INV-7 completeness, INV-8 measured-domain), materialise() (INV-9 no-derivation,
  INV-10 resolvable-target), DEGRADED mode, C6 scale-relative, C4 normalized subject
  match; self-test 54/54. PYQAnalyse v2.22.1 -> v2.23 (S4-0 check-completeness
  architecture). PYQSort v1.12.2 -> v1.13 and DeliveryFooter v1.6 -> v1.7 wire the
  [ExamCode]_approval_record.json contract (produced at Step 2c, consumed at PYQSort entry).
  validate_framework_md.py +Check AC (aggregator single-exit) so the drift cannot return;
  routes.json routes reconcile_taxonomy.py to PYQApprove.
- CLAUDE.md release-manager protocol updated: corpus-level checks AA-AE are part of the
  gate; "a red check is never advisory"; corrected engine-load model (engines load from
  the repo clone, /mnt/project is data-only, no per-project provisioning). SPEC_MANIFEST.json
  33-file workbench baseline regenerated to match production.

## 2026.07.25
- NEW audit_sync.py — cross-step synchronisation auditor (engine-API, trigger/route/SKILL
  parity, version xrefs, filename chain, blueprint.json schema). Untracked dev tool.
- PYQAnalyse v2.16 -> v2.22.1 + 3 NEW engines: corpus_io.py (Drive acquisition / image
  integrity / size governor), reconcile_taxonomy.py (S4-0), syllabus_provenance.py (S2-3e);
  blueprint_core.py +Clusters F-J (pattern-era, taxonomy parse, acquisition, image-gate,
  size governor; self-test 57 -> 164). Tracked set 21 -> 24.
- Corpus-transport migration wave: NEW spec PYQCompress v1.0 (Layer-2 doc size remediation;
  new trigger, tracked set -> 25); Blueprint v1.35 -> v1.38, MockTestAnalyse v2.24.10 ->
  v2.29.1, MockTestExplainAudit -> v1.16.1, PYQPrepare -> v1.9.1, PYQSort -> v1.12.2,
  PYQExplain -> v1.1, PYQExplainAudit -> v1.1.1, PYQFormat -> v1.4.1, PYQDeliver -> v1.5.1
  (delegate engine-owned functions to blueprint_core/corpus_io; remove local copies).
  validate_framework_md.py +5 checks (V-DRIVEGUARD/W-ENUMSIZE/X-DURABILITY/Y-IMGGATE/
  Z-DELEGATION). NEW audit_deep.py (deep drift/delegation/table-parity auditor).
- PYQCompress v1.0 -> v1.1 + corpus_io v1.0.1 -> v1.0.3 (v1.0.2 media-stem-collision fix
  [silent figure loss]; v1.0.3 optimize_docx always= param). Shipped as an atomic pair.

## 2026.07.23.1
- blueprint_core.py +Cluster E — score_difficulty / determine_strip_mode /
  map_difficulty_level, the canonical shared difficulty scorer for Step 5 and PYQ-4.
  Self-test 33 -> 57 PASS; byte-identical to MockTestAnalyse E-9/E-10 (V-SYNC verified).
- NEW audit_specs_ext.py — supplementary corpus auditor (V-SYNC cross-file parity,
  W-DECISION decision-ID integrity, X-NUMBER list contiguity, Y-CONFIG field-contract,
  Z-VERSION full 3-part compare). Untracked dev tool; 0 issues across the corpus.
- Framework_PYQDeliver.md v1.0 -> v1.2.1: date/session tag removal (§4A), three-tier
  deterministic Complexity resolver via blueprint_core Cluster E (D11 supersedes D4),
  adversarial audit fixes (marks_default declared, JSON int-key normalization,
  difficulty_labels fallback). RELEASE-MANAGER FIX: converted blueprint_core.py sourcing
  from /mnt/project-only to dual-path (/tmp/fw first, else /mnt/project) so GitHub-connected
  projects no longer HARD STOP. routes.json: PYQDeliver now lists blueprint_core.py.
- Framework_MockTestAnalyse.md v2.24.9 -> v2.24.10: annotation-only (E-9/E-10 canonical
  copy moved to blueprint_core Cluster E; zero logic change).
- routes.json reformatted to the generator's pretty-printed emit style (no functional change).

## 2026.07.23
- Framework_PYQFormat.md v1.0 -> v1.3 (PYQ-3, self-contained formatter):
  v1.1 removes the per-question date/session tag paragraphs (only sanctioned deletion);
  v1.2 restyles explanation tag headers into colored bands + marker-glyph swaps
  (⬛->📘/🧮, ❌->⚠️), machine-verified by a full text-stream integrity check (S8-8);
  v1.3 promotes the exam header + IFAS footer to real page header/footer parts that
  repeat on every page, and updates the footer tagline. Trigger/step unchanged; no
  framework engine; bootstrap stays 21/21.

## 2026.07.22
- NEW PYQ Explanation Pipeline — 4 specs: PYQExplain (PYQ-1), PYQExplainAudit (PYQ-2),
  PYQFormat (PYQ-3), PYQDeliver (PYQ-4). Wired into routes.json / PIPELINE / skill
  (19 -> 23 triggers); tracked set 17 -> 21 (bootstrap now 21/21). PYQ-1/PYQ-2 reuse
  explain_engine.py (+ explain_audit_gate.py for PYQ-2); PYQ-3/PYQ-4 are self-contained
  (write their own format_pipeline.py / pyq_deliver_pipeline.py, no framework engine).
- validate_framework_md.py — S2-EXPLAINGATE now fires on an actual gate invocation
  (`explain_audit_gate.py --`) or the AUDIT-COMPLETION-GATE output, not on a bare name-drop,
  so specs that only DISCLAIM the gate (PYQ-1 delegation note; PYQ-3/PYQ-4 NOT-REQUIRED
  lists) no longer false-positive. Genuine gate-users (Step 10 / PYQ-2) still fully checked.
- GAP-2026-07-22-001 section<->subject mapping chain (shipped atomically):
  MockTestCreate v5.29 -> v5.30 (position-based question-type dispatch, §6);
  MockTestCreateAudit v2.9.1 -> v2.9.2 (position-based question-type in audit);
  MockTestAnalyse v2.24.8 -> v2.24.9 (BUG 1 — sections[].subjects);
  Blueprint v1.34 -> v1.35 (BUGS 2-4 — section<->subject mapping);
  ScopedBlueprint BLUEPRINT_SCHEMA_VERSION 1.23 -> 1.35 (schema sync to Blueprint);
  DeliveryFooter Step 5 deliverable-count doc fix (5 -> 6 files).
- routes.json — PYQ explanation triggers reordered to end (no functional change; syncs the
  repo to the generator's emit order).

## 2026.07.21
- NEW engine paper_pipeline.py — shared naming/numbering/registry plumbing for Steps 6-11
  (self-test 37/37; added to tracked set -> bootstrap now 17/17). Added 5 Test* trigger aliases
  (TestCreate/TestCreateAudit/TestExplain/TestExplainAudit/TestDeliver -> 19 triggers), wired into
  routes.json / PIPELINE / skill.
- Specs: MockTestCreate v5.29, MockTestCreateAudit v2.9.1, MockTestExplain v1.20, MockTestExplainAudit
  refresh; Blueprint v1.32 -> v1.34; MockTestAnalyse v2.24.7 -> v2.24.8; PYQAnalyse v2.15 -> v2.16;
  MockDeliver v1.8 -> v1.9; ScopedBlueprint v1.5 -> v1.7.
- Added manifest_to_taxonomy_xlsx.py (untracked helper: subtopic_manifest.json -> taxonomy Excel).

## 2026.07.20
- explain_engine.py core self-test 44/44 -> 62/62 (audit stays 10/10). MockTestExplain -> v1.18 and
  MockTestExplainAudit P0 corrected to 62-of-62, so Step 9/10 pre-flight demands exactly what the
  engine prints. Deployed as a version-matched bundle (engine + both Explain specs).
- MockTestCreate v5.24 -> v5.27; MockTestCreateAudit v2.7.6 -> v2.8.1; MockTestExplain v1.15 -> v1.18;
  MockTestExplainAudit v1.8 refresh; MockDeliver v1.7 -> v1.8.

## 2026.07.18.1
- Framework_MockDeliver.md v1.6 -> v1.7.

## 2026.07.18
- validate_framework_md.py -> v2.8: adds Check T (cross-file token contract) and Check U (JSON
  producer/consumer field contract); generalises cross-file RA/MANDATE anchor resolution; drops
  the "equivalent"-exemption now that the MANDATE 8/9 prose is root-fixed in the specs.
  Re-added 'ScopedBlueprint': '6S' to the PIPELINE dict.
- Framework_MockTestCreate.md, Framework_MockTestAnalyse.md, Framework_PYQAnalyse.md,
  Framework_MockTestCreateAudit.md updated (MANDATE 8/9 "equivalent" prose removed at source).

## 2026.07.17.1
- Dual-path engine sourcing: Blueprint (Step 6), ScopedBlueprint (Step 6S), MockTestExplain
  (Step 9), MockTestExplainAudit (Step 10) now load their engines (blueprint_core.py /
  explain_engine.py / explain_audit_gate.py) from the framework clone (/tmp/fw) with fallback
  to the project Files (/mnt/project). GitHub-connected projects no longer need the engines
  uploaded to their Files; direct-upload projects continue to work.
- Framework_Blueprint.md v1.31 -> v1.32 (dual-path gate now in the spec source);
  Framework_MockTestAnalyse.md v2.24.5 -> v2.24.6; Framework_MockTestCreateAudit.md v2.7.3 -> v2.7.4.

## 2026.07.17
- NEW spec Framework_ScopedBlueprint.md v1.5 (Step 6S — scoped subject/topic/subtopic test
  blueprints). Wired into routes.json / PIPELINE / skill (14 triggers).
- NEW shared engine blueprint_core.py (added to the tracked set; self-test 33/33). Bootstrap
  count is now 16/16. Framework_Blueprint.md v1.27 -> v1.31 (allocation math extracted into
  blueprint_core.py). NOTE: blueprint_core.py must be uploaded to each project's /mnt/project/
  or Step 6/6S HARD STOPs (operational, outside this repo).
- Framework_MockTestAnalyse.md v2.24.2 -> v2.24.5.
- Framework_MockTestCreate.md v5.20 -> v5.23; Framework_MockTestCreateAudit.md v2.7.2 -> v2.7.3;
  Framework_MockDeliver.md v1.5 -> v1.6.
- Framework_MockTestExplain.md v1.14 -> v1.15; Framework_MockTestExplainAudit.md v1.8 refresh.

## 2026.07.14
- Framework_PYQPrepare.md: v1.6 -> v1.7.
- Added mocktestframework_SKILL.md — canonical account-level skill (STEP 0 load-and-verify
  bootstrap; trigger list synced to the live 13-trigger routing). Added an explicit no-DR-mirror
  guard that hard-stops when MIRROR == PRIMARY instead of silently re-cloning the same URL.
- Added check_triggers.py — enforces that the skill trigger list, routes.json, and the validator
  PIPELINE dict stay in sync; wired into CI (validate.yml) so drift fails the build.
- Deprecated docs/CUSTOM_INSTRUCTIONS.md to a pointer at the skill (single source of truth).

## 2026.07.12
- Deliverable filename rename across the delivery contract and the Create/Explain/Deliver
  specs: Step 7 -> Create, Step 8 -> Create_Complete, Step 9 -> Explanation,
  Step 10 -> Explanation_Complete, Step 11 -> Final.
- Specs updated to: MockTestAnalyse v2.24.2, MockTestCreate v5.20, MockTestCreateAudit v2.7.2,
  DeliveryFooter v1.6, MockTestExplain v1.14, MockTestExplainAudit v1.8 (content refresh),
  MockDeliver v1.5.
- validate_framework_md.py: permanently exempt "MANDATE/RA N equivalent" descriptive phrasing
  from the anchor checks (O-MANDATE/N-RA false-positive fix; genuine dangling refs still caught).
- MockDeliver: fixed stray internal "End of v1.3" marker.
- Added CLAUDE.md documenting the release-manager protocol (approved_framework, seal_release,
  guardrails) so future sessions inherit it.

## 2026.07.11
- Framework_MockTestAnalyse.md: v2.24 -> v2.24.1
- Framework_Blueprint.md: v1.27 content refresh
- Framework_MockDeliver.md: v1.3 -> v1.4
- Framework_MockTestExplain.md: v1.12 -> v1.13
- Framework_MockTestExplainAudit.md: v1.7 -> v1.8
- explain_engine.py: FIGURE-section tests replaced with FIGURAL-NO-FIGURE-SECTION regression lock (self-test 44/44, audit 10/10)
- routes.json: 10 -> 13 triggers (Framework_DeliveryFooter.md on all routes; Blueprint renamed to MockBlueprint; new PYQDraft/PYQScan/PYQApprove; engine deps on explain routes)
- tooling: validate_framework_md.py hardened (word-boundary stale markers, corpus-wide MANDATE/RA anchor resolution, accepts "vX changes:" changelog format); CI gates validator on Framework_*.md and installs python-docx; .verified gitignored; auto-manifest workflow removed

## 2026.07.10
- Initial release of the version-pinned, integrity-verified framework repo.
- 11 .md specs + 3 .py engines/gates under load-and-verify gate (bootstrap.py).


# ═══ ARCHIVE — Framework_PYQAnalyse v2.29 pre-split header & changelog (moved 2026-07-31; verbatim) ═══

# Framework_PYQAnalyse v2.29 — Universal PYQ Analysis & Taxonomy Builder
#
# MINIMUM COMPANION VERSIONS (v2.28):
#   corpus_io.py          >= v1.4   — load_taxonomy() IS Task 2.5's loader and gate;
#                                     Cluster K write_analysis_doc() IS S4-2,
#                                     read_analysis_doc() IS Task 2.5's reader and
#                                     assert_taxonomy_lock() IS its identity gate, and
#                                     read_analysis_doc() IS Task 2.5's reader. v1.2
#                                     adds INGEST FORMS: the Analysis doc is stored in
#                                     project Files as extracted TEXT, so under v1.1
#                                     Phase B cannot read it at all (GAP-2026-07-25-003).
#   reconcile_taxonomy.py >= v1.3   — S4-0 passes final_taxonomy=, and v1.3 RECORDS it
#                                     so Steps 3-6 need no Word document at all; older
#                                     builds accept
#                                     no such argument and raise TypeError.
#   blueprint_core.py     — MAX_HEADING_LEN for the S4-0 name gate; and the
#                           GAP-2026-07-26-001 build carrying next_nonempty_texts()
#                           and is_taxonomy_heading(para, is_option, next_text).
#                           S5-2 PASSES next_text; on an older engine that raises
#                           TypeError rather than silently miscounting.
#
# v2.29 — 2026-07-26 — is_option DELEGATED (audit_deep [XSPEC-DRIFT]).
#   This file defined its own is_option() with a docstring claiming alignment with
#   Step 5. No executable call site was found for it here, so the copy could not
#   misbehave — but it was drift bait, and it went stale the moment MockTestAnalyse
#   v2.34/v2.35 added the image-option path. Delegated to corpus_io >= v1.6 rather
#   than deleted, so a future call site in this spec inherits the correct predicate
#   instead of silently reintroducing the text-only one.
#
# v2.28 — 2026-07-26 — GAP-2026-07-26-001: A MULTI-PARAGRAPH STEM IS NOT A HEADING.
#          PYQSort EC-S8 defines a stem continuation as "bold + not-date + not-option
#          + not-next-Q". blueprint_core.is_taxonomy_heading() defined a taxonomy
#          heading as the same four conditions. Two different objects, one predicate,
#          on opposite sides of the same repository, never compared. Level 3 is the
#          only taxonomy level with no textual prefix, so bold was its only positive
#          signal — and the moment the producer began emitting bold body text the two
#          classes became the same object.
#          MEASURED, IIT_JAM_BIOTECHNOLOGY, 22 papers / 1719 questions: 20 spurious
#          headings across 10 papers; 128 counted triples against 126 real ones; 2
#          phantom triples; Task 2.5 HARD STOP. The question total and the orphan
#          count were both CORRECT throughout (1719 / 0) — nothing was lost, only
#          mis-filed — which is why Task 2.5 was the only gate that could catch it.
#          FIX (S5-2): count_sorted_file() builds bc.next_nonempty_texts() once per
#          document and passes next_text. A bare level-3 heading is genuine only when
#          the next non-empty paragraph is a DATE LABEL — guaranteed exam-agnostically
#          by PYQSort S6-2, CHECK 3 and EC-S10. Levels 1 and 2 are exempt (prefixed,
#          self-identifying). Verified on the full corpus: 1244/1244 genuine headings
#          preserved, all 20 spurious ones rejected, 1719 questions and 0 orphans
#          unchanged, triples 128 -> 126, phantoms 2 -> 0.
#          ALSO §6: added the QUESTION (multi-paragraph) class. Its absence WAS the
#          defect — §6 described a question as a single paragraph while EC-S8 emitted
#          several, and everything downstream inherited the wrong one.
#          ALSO S5-4b: Task 2.5 now TRIAGES phantoms into misread-stem vs genuine
#          name-mismatch. It previously asserted one cause and offered only the
#          name-mismatch remedies; against a misread stem "re-sort" is a no-op that
#          reproduces the file byte for byte, and "update the Analysis doc" writes a
#          question stem into the locked taxonomy — the exact defect D6-1 blocks.
#          The operator had no valid exit and the run halted permanently.
#
# v2.27 — 2026-07-26 — TASK 2.5 LOADS THROUGH load_taxonomy(). The read and the
#          identity assertion were two calls; they are now one, and the taxonomy is
#          taken from approval_record.json where the record carries it
#          (reconcile_taxonomy >= v1.3) rather than from a Word document. Pre-1.3
#          records fall back to the doc, fully gated, and need no re-run.
#          Companion rises to corpus_io.py >= v1.4.
#
# v2.26 — 2026-07-26 — TASK 2.5's LOCK CHECK DELEGATED TO THE SHARED GATE.
#          v2.25 gave Step 4 a fingerprint identity gate by writing the comparison
#          into the spec. Steps 5 and 6 then needed the same claim, so it now lives
#          once in corpus_io.assert_taxonomy_lock() and Task 2.5 calls it like
#          everyone else. No behaviour change: same two hard stops, same messages,
#          same operator actions — one implementation instead of four. Companion
#          requirement rises to corpus_io.py >= v1.3.
#
# v2.25 — 2026-07-26 — PHASE B READS AND WRITES THROUGH CLUSTER K (GAP-2026-07-25-003).
#          Step 4 was the LAST hand-parser of the Analysis doc. GAP-2026-07-25-002
#          consolidated four independent readers into corpus_io Cluster K, but the fifth
#          reader was PROSE — S5-4b Task 2.5 instructed Claude to extract section names
#          from a header line, topic names from master-summary cells and subtopic names
#          from per-topic cells, by hand. Prose is invisible to validate_framework_md
#          CHECK AG, which only inspects ```python blocks, so the consolidation could not
#          see it and it survived. Two consequences, both now fixed:
#            (1) Step 4 fails on GAP-2026-07-25-003 at its OWN call site. The Cluster K
#                ingest-form fix does not reach a reader that never called Cluster K, so
#                Phase B would have halted one step after PYQSort started working.
#            (2) Task 2.5's whole purpose is BYTE-IDENTICAL name agreement between the
#                Analysis doc and count_sorted_file(). Two hand-written extractions of the
#                same names is precisely how they drift. Both sides now derive names from
#                blueprint_core.parse_taxonomy_level() through one reader.
#          S5-5 Task 3 changes shape for the same reason. It described EDITING the doc in
#          place — replacing "—" cells and re-totalling. That is impossible now: the
#          runtime receives extracted text, which has no cells to edit, and /mnt/project/
#          is read-only. Task 3 becomes PARSE -> MERGE COUNTS -> REGENERATE through
#          write_analysis_doc(counts=), which the module has accepted since v1.1. This is
#          strictly stronger than the old rule: the writer computes the subtopic cell, the
#          per-topic TOTAL, the master-summary Total PYQs, the GRAND TOTAL and the header
#          total from ONE counts map, so the four levels cannot disagree by construction
#          rather than by checking. Verified end to end on the first real exam: 6/26/131,
#          all four levels equal, zero cells left as "—", fingerprint unchanged.
#          NEW GATE — Task 2.5 now asserts the Analysis doc against the approval record's
#          taxonomy_fingerprint before using it, the same cross-check PYQSort S1-0b makes.
#          Step 4 had NO identity gate: it verified that the doc agreed with ITSELF and
#          never that it was the doc that was APPROVED, so a superseded Analysis doc left
#          in project Files would have been counted into silently.
#
# v2.24 — 2026-07-25 — S4-2 DE-STUBBED + TAXONOMY ATTESTED + NAME-LENGTH GATE
#         (GAP-2026-07-25-002). Three changes, one theme: this step produces the artefact
#         the rest of the pipeline is built on, and it neither defined it nor attested it.
#         (1) S4-2 generate_merged_analysis_doc() was `pass`, deferring to "the npm docx
#             package per SKILL.md". The Analysis doc therefore had NO definition anywhere,
#             so its four consumers each guessed at a different structure and three guessed
#             wrong. It now delegates to corpus_io.write_analysis_doc() — THE writer, paired
#             with THE reader, asserted against each other by round-trip over a GENERATED
#             matrix of exam shapes (corpus_io --self-test). The framework serves ~200 exams
#             and cannot be validated against 200 real corpora; that matrix is the claim.
#         (2) S4-0 now passes final_taxonomy to build_approval_record(), which records a
#             taxonomy_fingerprint (reconcile_taxonomy v1.2, schema 1.2). Until now the
#             record proved the reconciliation RAN and said nothing about WHAT it locked, so
#             PYQSort could verify the lock was earned and still sort against a different
#             taxonomy — which is precisely what happened. Verified at PYQSort S1-0b.
#         (3) S4-0 HARD STOPS before locking when any subject/topic/subtopic name reaches
#             blueprint_core.MAX_HEADING_LEN. That bound governs whether text is recognised
#             as a heading in the sorted files and was enforced NOWHERE upstream: proven by
#             execution, a 131-character subtopic name written here survived PYQSort and then
#             silently stopped being a heading at Steps 4 and 5, with its questions
#             attributed to the PRECEDING subtopic — zero orphans, INV-5 conservation still
#             passing, because nothing was lost, only mis-filed. Raised 100 -> 300 and now a
#             named constant the producer and the consumer share.
#         Also corrects the v2.6 entry's false downstream-compatibility claim in place.
# v2.23 — 2026-07-25 — S4-0 CHECK-COMPLETENESS ARCHITECTURE (GAP-2026-07-25-001).
#         reconcile() returned from INSIDE C4's style-aware branch, so C5 (near-duplicate),
#         C6 (over-aggregation) and C7 (anchoring) never ran for ANY exam carrying a
#         syllabus_style record — i.e. every PYQDraft >= v2.17 exam, which is the default
#         path, not an edge case. The record then reported CLEAN with an empty anchoring
#         block and AUTO-LOCKED the taxonomy. A missing finding is worse than a crash: it
#         is indistinguishable from a passing check.
#         (1) TIER 0 table: C7 DOCUMENTED for the first time (its four classes were emitted
#             by the engine and REQUIRED by the S4-4 gate template while appearing in no
#             spec at all); C4's two mutually exclusive forms and their real thresholds
#             stated; list declared EXHAUSTIVE, CLOSED and INDEPENDENT; single-exit engine
#             contract stated.
#         (2) INV-7 CHECK_COMPLETENESS, INV-8 CHECK_MEASURED, INV-9 NO_DERIVATION_AT_S4_0
#             added. INV-8 exists because execution attestation alone is NOT sufficient —
#             C4 matched subjects with raw `==` while every other comparison normalized, so
#             a subject differing only in case or spacing passed C1 and then silently zeroed
#             C4's measurement domain. The check "ran" and measured nothing.
#         (3) INV-9: ADD_SECTION / ADD_SUBTOPIC (safe defaults for SUBJECT_MISSING and
#             ITEM_UNMAPPED — the data-loss class) were never materialised AND never held
#             the run, so a syllabus subject could be dropped while the taxonomy auto-locked
#             CLEAN_ADJUDICATED. They now HOLD for PYQDraft re-derivation.
#         (4) EXECUTION block: verdicts, final_taxonomy and quarantined_paths DEFINED; the
#             missing MATERIALISE step specified; ROUTING directive added.
#         (5) R1 mode B: check list corrected to C3 + C5 + INV-5. C4 is provenance-DEPENDENT
#             (both forms divide by a syllabus-derived base), so with no provenance the
#             divisor collapses to 1 and every DEGRADED run would be falsely HELD.
#             locked_taxonomy is now REQUIRED.
#         (6) C6 made SCALE-RELATIVE (items-per-topic density). The absolute rule encoded one
#             exam's scale and false-fired on legitimately small exams; because its safe
#             default is RE_DERIVE, a false fire is a hard block.
#         (7) S4-4 Branch A: ratio line is now FORM-AWARE; checks executed/skipped printed.
#         (8) S4-1 SUBJECT ORDERING: alphabetical fallback replaced by taxonomy order —
#             sections[] are OTS labels (S2-2a SECTION != SUBJECT), so the intersection is
#             empty for every non-marker_mode exam and the "rare" fallback was the norm.
#         (9) §12 Phase 0c: "EXACTLY 2 files" -> 3; stale benchmark-count line replaced;
#             INV-7/8/9 gate items added.
#        (11) INV-10 RESOLVABLE_TARGET added. materialise() matched destructive verdicts
#             against the finding's `item`, which is a path only for PATH_EXTRA — and
#             PATH_EXTRA is resolved at Tier 1 and never reaches a destructive verdict.
#             Every destructively-adjudicable class carries a description, subject name or
#             raw syllabus text, so DROP/SUPPRESS/MERGE_INTO removed nothing while the
#             record asserted the path was dropped. The taxonomy was never harmed; the
#             RECORD lied. Unresolvable destructive actions now block and HOLD.
#        (10) S4-4 Branch A: PRIOR DECISIONS line added. INV-6 replay was already
#             recorded in the JSON (prior_record_attested, engine_version) but printed
#             nowhere, so a verdict reused from an older engine was invisible to the
#             operator, whose only interface to a run is the gate text. Same shape as
#             the write-only approval_record this release closes at PYQSort S1-0.
#         Enforced statically by validate_framework_md.py Checks AC (aggregator single-exit),
#         AD (emitted finding-class documented) and AE (normalization conformance).
# v2.22.1 — 2026-07-25 — PRE-SCAN GATE Q_PATTERNS CORRECTED. The inline copy in the Step 2b
#         confirmation gate listed five patterns "from Step 5 E-2" and was used to COUNT
#         questions per file. Counting a normalised Row file with the bare-number pattern counts
#         every option as a question — the gate would have reported roughly five times the true
#         total and the operator would have confirmed it. Corrected to the engine's two.
# v2.22 — 2026-07-25 — DEFECT C AT STEP 2b + v2.21 RATIONALE CORRECTION.
#         (1) Step 2b (PYQScan) carried the SAME batch-level durability defect that v2.21
#             fixed at Step 4. S3-5's per-paper loop calls scan_paper(), appends to
#             papers_scanned_list, increments papers_scanned, records years_covered and
#             adds every newly discovered subtopic to the taxonomy — all in memory — while
#             save_scan_progress ran only AFTER the loop. An exception on paper 3 therefore
#             discarded papers 1 and 2 together with their discoveries, and the progress
#             file showed them as never scanned. Found by validate_framework_md.py v3.0
#             Check X (per-item durability), not by reading: the same shape had been fixed
#             twice already and still went unnoticed here, which is the entire argument for
#             encoding a defect as a check rather than as a memory.
#             Fix: save_scan_progress + save_classifications inside the per-paper loop.
#             Convergence is untouched — consecutive_empty_batches is a per-BATCH,
#             complete-batches-only counter, and EC-P26 already specifies that a partial
#             batch persists its papers without affecting it. BATCH_SIZE unchanged.
#         (2) CORRECTION to v2.21. That entry justified the Step 4 fix with "the failure
#             mode is a silent undercount". It is not. Counts and files_processed_list are
#             written by the same save, so a skipped save loses both and the resume simply
#             recounts those files — the total comes out right, and S5-4a would catch it if
#             it did not. The real costs are lost work, a progress file that understates
#             what was done, and a latent double-count if the accumulator and the
#             processed-list are ever persisted at different moments. The fix stands; the
#             stated reason was overclaimed and is corrected in S5-4. An inflated rationale
#             invites a future reader to check it, disbelieve it, and discount the rule.
#
# v2.21 — 2026-07-25 — STEP 4 CORPUS TRANSPORT (DEFECTS A, B, C, N + O at Step 4).
#         Twin of Framework_MockTestAnalyse v2.29 / Framework_PYQSort v1.12 / corpus_io v1.0.1.
#         Step 4 (PYQCount) and Step 5 (PYQExtract) fetch the SAME corpus from the SAME Drive
#         folder through the SAME connector, and Step 4 carried every one of the defects that
#         took Step 5 down on 2026-07-24 — it had simply not been run far enough to hit them.
#         (1) DEFECT C (CRITICAL) — count_progress.json was saved AFTER each batch, not after
#             each file (S5-4 item 7). process → accumulate → save is the only thing that
#             persists a file's counts, so ANY exception inside the loop skipped the save and
#             discarded every file already counted in that batch, with no trace: the progress
#             file shows them as never processed and a resume silently recounts them. At
#             BATCH_SIZE_COUNTS = 5 that is up to FOUR papers of work lost per failure. This
#             is the same defect that made the Step 5 incident destructive. (v2.21 stated the
#             consequence as "a silent undercount"; v2.22 corrects that — see below.)
#             Fix: save inside the per-file loop, immediately after each file is counted. The
#             batch-level save REMAINS as a redundant flush. BATCH_SIZE_COUNTS = 5 is
#             UNCHANGED — batching is the user-facing pacing unit, never the durability unit.
#         (2) DEFECT A — enumeration discarded fileSize. The Drive listing carries it inline,
#             already in the response, and S5-1 read only the name. With size unknown there is
#             no pre-flight partition, so a paper above the connector's 10 MiB cap cannot be
#             known to be unfetchable until the download is attempted — which in the reported
#             incident happened at batch 6 of a clean-looking run. Enumeration now records
#             {id, name, mimeType, fileSize, parentId, source} and screens every entry:
#             native Google Docs, Drive shortcuts and legacy .doc are REJECTED WITH A REASON
#             instead of vanishing, and a paper with no reported size is rejected rather than
#             silently processed.
#         (3) DEFECT B (CRITICAL) — the download was unguarded. Verified across the corpus:
#             ZERO try/except existed around any Drive call anywhere. Every fetch now goes
#             through corpus_io.fetch_drive_docx; every failure — size, permission, network,
#             malformed payload, unknown — raises TransportFallback and routes that paper to
#             the UPLOAD LANE. A transport failure is NEVER fatal to the run. This is what
#             makes Step 4 survive a future change to the connector's cap: correctness rests
#             on the fallback being taken, not on the predicted partition being right.
#         (4) DEFECT N — the retrieval envelope is documented for the first time. For any real
#             paper the connector's result exceeds context and spills to
#             /mnt/user-data/tool_results/*.json; that file is a LIST whose [0]['text'] is
#             itself a JSON STRING which parses to {id, title, mimeType, content} with content
#             base64. Every previous execution rediscovered this by trial and error with a
#             different improvisation each time — non-determinism in the hot path. One
#             implementation now: corpus_io.decode_drive_payload, followed by a byte-count and
#             PK magic assertion, because a payload truncated at a ZIP member boundary still
#             opens as a valid archive while presenting fewer questions.
#         (5) DEFECT O at Step 4 — the duplicate rule actively selected the unfetchable file.
#             S5-1 kept the LARGER of two sorted files for the same date+session on the
#             reasoning that it was "more likely to have images intact". Under a 10 MiB
#             download cap that rule picks precisely the copy that cannot be fetched, and
#             under Phase B's zero-tolerance standard picking EITHER copy silently is wrong:
#             a re-sorted paper and its superseded predecessor differ in content, so the
#             choice changes the counts. Both duplicate classes are now HARD STOPs naming
#             both files — canonical identity (X.docx vs "X (1).docx") via Cluster H at
#             enumeration, and same date+session with different Q-ranges at the filter stage.
#             Image survival is no longer a reason to prefer the larger file: PYQSort v1.12
#             CHECK 10 gates it at the point of production.
#         (6) 4-batches-per-chat arithmetic stated up front (S5-7). The binding constraint on
#             the upload lane is the platform's 20-files-per-chat limit, not the batch size:
#             at BATCH_SIZE_COUNTS = 5 that is exactly 4 batches / 20 papers per chat. Derived
#             from bc.upload_batch_plan, never restated as a literal.
#         (7) Step 2b banner (S3-2): the absence of images and OMML during the scan is BY
#             DESIGN and is NOT the defect class fixed in Steps 3/5. Added because a reader
#             arriving from the v2.29 image-integrity work would otherwise reasonably conclude
#             Step 2b was broken too and "fix" it. S3-2, EC-P24 and EC-P25 are UNCHANGED.
#         (8) New edge cases EC-P31..EC-P34. §11 and §12 updated.
#         NOT CHANGED: BATCH_SIZE_COUNTS (5), the S5-1a Task 1 confirmation gate, the S5-4a
#         zero-tolerance accuracy gate, Task 2.5, Task 3, the sorted-filename filter, and every
#         Phase 0a / 0b / 0c behaviour other than the S3-2 banner.
#         ROUTING: routes.json must route corpus_io.py to PYQCount. NOT OPTIONAL.
#
# v2.20 — 2026-07-23 — PHASE-B HEADING PARSER DRIFT CLOSED (line-by-line audit finding).
#   parse_taxonomy_level() and is_taxonomy_heading() each carried a comment demanding they
#   stay IDENTICAL to Step 5's, and EC-P14 named the exact failure mode and remedy. Both had
#   nevertheless drifted: Framework_MockTestAnalyse v2.16 (RIGID-4) expanded the heading
#   table from 3 patterns to 12+ (Section:/Part:/Area:, Unit/Module/Block, colon-style
#   topics, case-insensitive) and this file was never mirrored, and the two
#   is_taxonomy_heading copies used DIFFERENT question-exclusion regexes.
#   IMPACT: for any exam not using the Subject:/Topic N: convention, Step 5 read a heading as
#   level 1/2 while Step 4 fell through to level 3 and counted it as a SUBTOPIC — wrong
#   per-subtopic counts, caught (if at all) only by Step 6's BV-0A cross-check.
#   FIX: both now delegate to blueprint_core Cluster G. The engine form is Step 5's superset,
#   proven by test_cluster_g.py to classify every heading the old copy handled identically
#   while additionally levelling the forms it silently mis-filed. A comment asking two files
#   to stay in step is not a mechanism; one definition is.
#
# v2.19 — 2026-07-23 — ERA LOGIC UNIFIED INTO THE ENGINE + MARKER-MODE COVERAGE
#   (audit follow-up to v2.18; fixes defects introduced BY v2.18).
#   (1) ANTI-DRIFT. v2.18 transcribed the era-classification chain into S3-2a step 3b as
#       prose while blueprint_core carried its own implementation, and routes.json routed
#       no engine to PYQScan — two independent definitions of "current era" with nothing
#       keeping them in step. The v2.25 Step-5 changelog even CLAIMED they were shared;
#       they were not. Step 3b now CALLS bc.classify_paper_era / bc.exam_config_bounds /
#       bc.type_resolver_from_config, and routes.json routes blueprint_core.py to
#       PYQDraft/PYQScan/PYQApprove/PYQSort/PYQCount/PYQExtract. Same for the
#       OUT_OF_PATTERN literal, which now lives in the engine only.
#   (2) NEW ERA 'retyped' (EC-P9b). Era was defined by SIZE alone, so an exam that keeps its
#       question count but changes its question TYPES — all-MCQ becoming MCQ/MSQ/NAT — was
#       classified 'current' and blended into the mix and the axis-3 distribution. Across
#       ~200 exams that is at least as common as a count change, so size-only classification
#       was missing the majority case. Backward compatible: with no marking_scheme, or with
#       no detected types, no comparison runs and the v2.18 chain applies unchanged.
#   (3) MARKER-MODE ERA DETECTION (EC-P9c). marker_mode exams had NO era detection at all —
#       the Q-number chain cannot run without Q-ranges. Step 3b now compares observed module
#       names against exam_config.sections[].name and reports retired modules instead of
#       letting EC-S2 fuzzy matching silently absorb them into a surviving section.
#
# v2.18 — 2026-07-23 — PATTERN-ERA AWARENESS AT SCAN TIME (GAP-2026-07-23-001;
#   PYQ-side twin of Framework_PYQSort v1.9 and Framework_Blueprint v1.36).
#   ROOT CAUSE (shared by all three specs): exam_config describes the CURRENT exam
#   pattern, but a PYQ corpus routinely spans several patterns. Nothing in the pipeline
#   recorded, reported, or handled that. RULE 4 said "section from Q-number range in
#   exam_config" with no branch for a Q-number outside every range, and EC-P9 documented
#   only the SHORTER direction ("later sections may have 0 questions"). The LONGER
#   direction — a previous-era paper with MORE questions than the current pattern — was
#   undocumented corpus-wide, and it is the dangerous one: surplus Q-numbers match no
#   range at all, so they were assigned None and then failed every (section, topic,
#   subtopic) lookup downstream. A 100-question legacy paper scanned against a
#   60-question current config lost 40 questions silently.
#   (1) RULE 4 (§8) — new OUT-OF-RANGE branch. Q-numbers outside every configured range
#       take the OUT_OF_PATTERN sentinel (the same constant as Framework_PYQSort v1.9
#       S2-2) and are classified against the FULL taxonomy instead of one section's slice.
#       This is the ONE relaxation of the rule's "not content" half, and only because the
#       rule's premise fails: it presupposes a structural section EXISTS. Gated on the
#       sentinel, never on a failed match, so a question that has a section cannot reach
#       it. pattern_era='out_of_pattern' is recorded on the classification.
#   (2) EC-P9 — the missing mirror documented: papers LARGER than the current pattern.
#   (3) S3-3 step (c) — the out-of-range route made explicit at the classification site
#       rather than only in the rules section.
#   (4) S3-2a PRE-SCAN GATE — new step 3b computes each paper's pattern era
#       (current / larger / smaller / unverified) from exam_config and the observed
#       Q-numbers ALONE; new Pattern Era column; new step 5b notice printed ONLY when the
#       corpus spans more than one era. A single-era corpus — the common case across the
#       ~200 exams — sees no behavioural or output change whatsoever.
#   DESIGN INTENT: both eras are scanned and both feed the taxonomy. Older papers are
#   retained precisely because the variety of concepts, phrasings, difficulties and
#   formats they expose is what makes generated questions good, and a subtopic observed
#   across many eras is better characterised than one observed twice. The defect was
#   never that old papers were included — it was that the pipeline noticed the structural
#   mismatch and said nothing.
#   SCOPE BOUNDARY (stated so it is not mistaken for solved): question COUNTS are safe —
#   Framework_Blueprint §4-2 consumes r_avg as a PROPORTION against a sec_qs budget from
#   exam_config, so a different-size paper can neither inflate nor shrink allocation.
#   Subject/subtopic MIX and format mix remain era-blended; §3 recency weighting dampens
#   but does not remove this. Era-scoped frequency would require era-tagging through the
#   Step-5 manifest and the Frequency xlsx and is deliberately NOT attempted here.
#   The pre-scan notice reports the exposure so the operator holds that decision.
#
# v2.17 — 2026-07-23 — PYQAPPROVE OPERATOR-SAFE APPROVAL GATE (root-cause fix).
#   INCLUDES (Issue C + C-1):
#     C-1 CRITICAL — DELIMITER AMBIGUITY. Paths were '/'-joined strings, but
#         real subject names contain '/' (live example: IIT JAM Biotechnology's
#         "Microbial/Plant/Animal Biotech"). Every anchor check produced a FALSE
#         FAILURE on that exam. FIX: paths are LISTS OF COMPONENTS, compared as
#         tuples, never split or joined for comparison. Delimiter-free by design.
#     C   EMISSION BURDEN. S2-1/S2-3 had to emit 9 fields x N items by prose-
#         following (~1800 values for a 200-item syllabus). FIX: emit 4 fields
#         (path, text, to, why); DERIVE the other 5 (id, subject,
#         syllabus_group, enumerated, deviation) in syllabus_provenance.py.
#         A derived field cannot be emitted wrong.
#     CIRCULARITY GATE. group_topic_map must be DECLARED from syllabus
#         structure; a map derived from the mappings it checks makes anchoring
#         vacuous. Found by testing 11 real syllabi (all passed spuriously).
#     4-LEVEL COLLAPSE. Syllabi whose depth exceeds Subject>Topic>Subtopic
#         (NEET Chemistry: CHEMISTRY > PHYSICAL CHEMISTRY > SOLUTIONS > item)
#         MUST record the collapse as a declared deviation. Verified: NEET
#         correctly build-blocks until the collapse decision is recorded.
#     §7 CANONICALIZATION. A destination matching the taxonomy only after
#         normalization is snapped to the taxonomy's EXACT spelling, so
#         byte-identity holds downstream instead of failing at Step 5/6.
#   PROBLEM: S4-4 posed four ACADEMIC questions ("are subtopics faithful to the
#   syllabus?", "is anything MISSING/EXTRA?") to an operator who is non-technical
#   and non-academic by role definition. The gate was therefore unanswerable at
#   the point of use, yielding either a rubber-stamp (gate protects nothing) or a
#   stall (no escalation path). Approval theatre, not approval.
#
#   ROOT CAUSE (found during this fix, deeper than S4-4): S2-4 persisted the
#   DERIVED taxonomy but NEVER persisted the extracted syllabus items. At
#   PYQApprove time no machine-readable ground truth existed, so the four
#   questions COULD NOT be answered by machine — they had to be delegated to a
#   human. The gate was a symptom; the missing provenance record was the defect.
#
#   FIX (4 changes):
#     (1) S2-4 — taxonomy_draft.json now persists syllabus_subjects[] (verbatim
#         S2-1 subject names) and syllabus_items[] (id, subject, raw_text,
#         enumerated, source_ref, mapped_paths[]). This is the provenance record
#         that makes Tier 0 possible. Backward compatible: absent => legacy mode.
#     (2) NEW S4-0 — TAXONOMY RECONCILIATION ENGINE (reconcile_taxonomy.py).
#         Deterministic 3-tier resolution replacing the human quiz:
#           Tier 0  machine reconciliation  (C1..C6, no judgment)
#           Tier 1  codified auto-policy    (PATH_EXTRA by PYQ evidence)
#           Tier 2  evidence-bound adjudication, REPLAYED from approval_record
#     (3) S4-4 REWRITTEN — emits a VERDICT + receipt, not a questionnaire.
#         CLEAN / CLEAN_ADJUDICATED => auto-lock, operator only uploads files.
#         HELD => named finding routed for adjudication. Operator never performs
#         academic judgment in any branch.
#     (4) S4-3 / S10-1 / S10-2 — approve-mode closed set 2 -> 3 files
#         (+ [ExamCode]_approval_record.json, the audit + replay ledger).
#
#   TIER 1 POLICY (confirmed): out-of-syllabus but PYQ-backed subtopics are
#   AUTO-RETAINED. Rationale is the framework's own anti-data-loss rule (S2-3
#   MPPSC Botany evidence) plus S3-6, which already gates every scan-added
#   subtopic at MIN_PATTERN_SIZE >= 3 PYQs — so such subtopics are PYQ-evidenced
#   BY CONSTRUCTION before they ever reach PYQApprove.
#
#   DETERMINISM GUARANTEE: Tier 2 adjudication is constrained by six hard
#   invariants that an adjudicating verdict CANNOT override. Unsafe or
#   unevidenced verdicts are rewritten to the safe default rather than rejected,
#   so a bad adjudication degrades to data-preserving, never to data loss:
#     INV-1 NO_SUPPRESS_SYLLABUS      never remove a syllabus-enumerated item
#     INV-2 NO_DROP_PYQ_BACKED        never drop a path with >= 3 PYQs
#     INV-3 LOW_CONFIDENCE_SAFE_DEFAULT
#     INV-4 EVIDENCE_REQUIRED         destructive verdict needs a syllabus quote
#     INV-5 CONSERVATION              no classified question may be orphaned
#     INV-6 REPLAY_DETERMINISM        prior verdicts replayed, never re-decided
#   INV-6 is what makes the gate reproducible across sessions and model
#   instances — it closes the framework's known "spec-as-prose is
#   non-deterministic" failure class at the adjudication boundary.
#
#   Verified: 24/24 adversarial unit tests (test_reconcile.py) incl. attempts to
#   drop syllabus items, drop PYQ-backed paths, adjudicate with no evidence, and
#   adjudicate under silence; plus end-to-end IIT JAM BT simulation reproducing
#   the reported case (both scan-discovered subtopics auto-retained, 0
#   escalations, conservation pass, status CLEAN).
#
# v2.16 — 2026-07-20 — PYQ CORPUS DRIVE-ONLY STANDARDIZATION, STEP 2b/PYQScan (twin fix:
#   Framework_MockTestAnalyse.md Step 5/PYQExtract v2.24.8). Found during a project-level
#   audit: three pipeline steps that all handle the SAME document class (Row/Sorted PYQ
#   .docx corpus files) disagreed on whether Google Drive was required — Step 4 (PYQCount,
#   this file) always mandated Drive with no fallback; this step (Step 2b/PYQScan) allowed
#   an uploads-only fallback; Step 5 (PYQExtract) allowed the broadest fallback (project/
#   uploads). STANDARDIZED to Step 4's existing Drive-only rule (confirmed with
#   Radheshyam) — Row files must be in Google Drive for --scan mode now, same as
#   --counts mode always required. WHAT CHANGED:
#     Header, S1-1 trigger parsing, S1-2 mode validation, S1-2 file inventory — PYQ:
#       <<Drive link>> is now REQUIRED for --scan mode; absent → HARD STOP (was: silent
#       fallback to /mnt/user-data/uploads/).
#     collect_row_files() (§3 S3-2) — removed the 'uploads' source branch entirely;
#       now takes drive_folder_id as a required argument and raises SystemExit if
#       absent, instead of silently scanning uploads/.
#   --taxonomy mode (Exam Syllabus/Pattern docs) and --approve mode (scan_progress.json)
#   are UNAFFECTED — those are a different document class (small config/state files),
#   not the PYQ corpus, and remain project/uploads-eligible per existing architecture.
#   Does not touch taxonomy-building logic, batch processing, or gate/mandate checks.
#   Verified: validate_framework_md.py (0 issues, AST-clean).
#
# v2.15 — 2026-07-18 — LOCAL-COPY CORRUPTION REPAIR (B-PYAST false positive; zero content/
#   logic change). This project's local Files-section copy of this spec had silently DROPPED
#   2 markdown code-fence lines somewhere between §D6-3 (the "pass" / NOTE comment ending the
#   dimensional-split-detection block) and §D6-4/D6-5 (the split-governance-guards block) —
#   a closing ``` after the v2.13 NOTE comment, and an opening ```python before
#   reclassify_after_refinement(). Missing fences caused validate_framework_md.py to parse
#   two separate, independently-valid Python blocks as one contiguous block, producing a
#   false "invalid syntax (line 188 of block)" AST error at the boundary. Verified via direct
#   byte-for-byte diff against the canonical framework-specs GitHub repo (production branch,
#   commit 74d395f) that the CANONICAL source was never affected — this was local-copy
#   corruption only, likely introduced during an earlier Files-section upload/sync, not a
#   spec defect. Fix: restored both fence lines exactly as they exist upstream. Confirmed
#   post-fix: this file is now byte-identical to the canonical GitHub copy in its entirety
#   (diff clean, matching line count). No prose, code, gate, or rule content changed.
#
# v2.14 changes: FORMAT AUTHORITY RECONCILIATION (register D6-11). S3-3b reconcile_format()
#   makes the authoritative full-parse format (PYQSort Phase A) supersede the lightweight
#   scan's provisional OMML-obscured/figure-inferred tokens, so a mis-scanned math/figural
#   item no longer drives the wrong Format/CONCEPT_GROUP/class downstream. reconcile_stats()
#   flags a >20% correction rate for review. Verified by fmt_harness (16/16).
#
# v2.13 changes: SPLIT GOVERNANCE GUARDS (register D6-4/D6-5). Deterministic helpers that
#   enforce the previously prose-only split rules: split_children_valid() flags near-duplicate
#   split children (over-split) so they are merged back (high-precision: singular/plural, paren-
#   variants, exact dups; borderline pairs left to Q3/QV-13 to avoid false merges); merge_record()
#   captures distinct forms merged into one subtopic (under-split) so Step 7 scenario_key still
#   separates them. Verified by split_harness (14/14).
#
# v2.12 changes: NAME-QUALITY GATES (register D6-1/D6-2).
#   (1) NAME-SHAPE VALIDATION: HARD STOP on question-shaped subtopic/topic names
#       (ends with '?', >80 chars, or interrogative-initial) — stops a raw PYQ question
#       being captured as a subtopic and then allocated/generated (occurred in the SSC CGL
#       run). High-precision: 0 false positives on 31 real labels.
#   (2) canon_name(): NFC + dash/whitespace/case folding for COMPARING/COUNTING names, so
#       trivial drift never phantom-splits a subtopic (complements Task 2.5). Display keeps
#       the original name. Verified by name_harness (46/46).
# [ExamCode] project | Steps 2a/2b/2c + 4 (PYQDraft/PYQScan/PYQApprove/PYQCount) | Exam-agnostic
#
# PURPOSE:
#   Build the authoritative 3-level taxonomy (Subject > Topic > Subtopic) and
#   produce a single merged Analysis Word Document for any competitive exam.
#   This Analysis doc is a mandatory input to Step 6 (MockBlueprint). The taxonomy also serves
#   as the classification reference for PYQSort (Framework_PYQSort.md).
#
# PIPELINE POSITION:
#   Step 1  PYQ Prepare  → raw PYQ .docx to Row file
#   PYQAnalyse           → THIS SPEC (taxonomy + Analysis doc)
#   Step 3  PYQSort      → 1 Row file → 1 Sorted PYQ (uses approved Analysis doc as taxonomy)
#   Step 5  PYQExtract   → Sorted PYQ → section_rules.md + manifest + Frequency .xlsx
#   Step 6  MockBlueprint → Analysis doc + Frequency xlsx → blueprint.json
#   Steps 7–11           → Mock test creation pipeline
#
#   PYQAnalyse has 4 modes that run at different points in the pipeline:
#     --taxonomy + --scan + --approve  run BEFORE PYQSort (build & lock taxonomy)
#     --counts                         runs AFTER  PYQSort (fill PYQ counts)
#
# PREREQUISITE:
#   Step 1 (PYQ Prepare) must have already converted raw exam dumps into standardized
#   Row files (.docx with Q.1–Q.N, date labels [DD-Mon-YYYY <session_keyword> X] or
#   [DD-Mon-YYYY] when session is not applicable, no answers/explanations/metadata).
#   Session part in date labels is OPTIONAL — single-session exams omit it.
#   PYQAnalyse and PYQSort both expect Row file format.
#   If Row files don't exist: run Step 1 PYQ Prepare first.
#
# INPUTS (by mode):
#   --taxonomy : Exam Syllabus (ANY format: image/PDF/.docx/plain text)
#                Exam Pattern  (ANY format: image/PDF/.docx/.xlsx/plain text)
#                  PREFERRED: .xlsx with 3 standardized tabs (Overview/Sections/Range)
#                  See S2-2 for xlsx parser specification.
#   --scan     : Row files (.docx) — from Google Drive (required, v2.16)
#                scan_progress.json (for resume across sessions)
#   --approve  : scan_progress.json (completed scan)
#   --counts   : Sorted PYQ files from Google Drive (output of PYQSort)
#
# OUTPUTS (by mode — CLOSED SETS, see §10 S10-1 for full contract):
#   --taxonomy : [ExamCode]_taxonomy_draft.json + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --scan     : [ExamCode]_scan_progress.json + [ExamCode]_classifications.json
#                (2 files, nothing else — taxonomy lives INSIDE scan_progress.json)
#   --approve  : [ExamCode]_PYQ_Analysis.docx + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --counts   : [ExamCode]_PYQ_Analysis.docx (UPDATED with PYQ counts)
#                (1 file, nothing else — count_progress.json is internal)
#
#   DELIVERABLE SET IS CLOSED: each mode delivers EXACTLY the files listed
#   and NOTHING ELSE. See §10 S10-1 for DO-NOT-DELIVER lists per mode
#   and S10-2 for the pre-delivery checklist. Creating unauthorized files
#   is a spec violation (same class as anti-editorializing violations).
#
# TRIGGER FORMAT:
#   Step 2a: PYQDraft [ExamCode]          (ExamCode provided ONLY here, saved in exam_config.json)
#   Step 2b: PYQScan                      (reads ExamCode from exam_config.json)
#   Step 2b: PYQScan PYQ: <<Google Drive folder link>>  (required, v2.16 — Drive source for Row files)
#   Step 2c: PYQApprove                   (reads ExamCode from exam_config.json)
#   Step 4:  PYQCount PYQ: <<Google Drive folder link>>  (reads ExamCode from exam_config.json)
#
#   Trigger matching is case-insensitive.
#   ExamCode: alphanumeric + underscore only (e.g. SSC_CGL_TIER1, GATE_CS).
#   ExamCode is typed ONCE in Step 2a, then auto-read from exam_config.json in all later steps.
#
# PROJECT SETUP:
#   ALL modes run in [ExamCode] project (exam-specific).
#   After --approve: Analysis doc + exam_config.json are already in project.
#   After --counts: user downloads updated Analysis doc → input for Step 5 + Step 6.
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   All section names, topic names, subtopic names → derived from syllabus + PYQ.
#   Same spec runs for SSC CGL (4 sections), GATE CS (1 section), or any exam.
#
# VERSION HISTORY:
#   v2.11 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           PREREQUISITE section updated: date labels can be [DD-Mon-YYYY] without
#           session (single-session exams). Framework_PYQPrepare v1.1 makes session
#           optional in the trigger. PYQAnalyse date detection (\d{1,2} day pattern)
#           already handles both forms — this is a documentation-only fix.
#   v2.10 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S10-4: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. All 4 modes (--taxonomy, --scan,
#           --approve, --counts) now render the standardized visual footer after
#           every present_files call. Zero logic change.
#   v2.9 — 2026-07-06 — BATCH STOP LAW + DELIVERABLE SET CONTRACT (1 new section, 2 rewrites, 10 fixes).
#           ROOT CAUSE 1 — BATCH STOP LAW: SSC CGL Tier 2 PYQScan — Claude
#           auto-advanced from Batch 1 to Batch 2 in the same response without
#           waiting for user's "continue" trigger. 7 structural gaps identified
#           by comparing how MockCreate enforces the same rule (MANDATE 1) vs
#           how PYQAnalyse expressed it (item 7 in Anti-Editorializing Rule).
#
#           ROOT CAUSE 2 — DELIVERABLE SET: SSC CGL Tier 2 PYQScan — Claude
#           delivered an unauthorized taxonomy_draft_v2.json alongside the
#           spec-defined scan outputs. The spec had no CLOSED DELIVERABLE SET
#           contract — outputs were listed in the header but nothing said
#           "these files and NOTHING ELSE." 4 structural gaps identified by
#           comparing how MockCreate enforces delivery (S13-6 closed set,
#           S13-7 pre-delivery checklist, R-DELIVER rule) vs PYQAnalyse
#           (one-liner in header, no DO-NOT-DELIVER, no pre-delivery gate).
#
#           BATCH STOP LAW CHANGES:
#           (1) NEW S3-4a — BATCH STOP LAW: dedicated mandate-level section
#               with failure history, continue trigger contract, small-corpus
#               clarification, final-batch exception, and forbidden behaviors.
#               Same architectural weight as MockCreate's MANDATE 1 / B-1..B-8.
#           (2) S3-4 convergence gate docstring: "CONTINUE scanning without
#               discussion" rewritten to explicitly say "STOP THE RESPONSE and
#               wait for user's continue trigger — without discussion means
#               do not editorialize, NOT auto-advance." This single line was
#               the primary cause of the failure — Claude read it as an
#               instruction to auto-advance silently.
#           (3) S3-5 run_scan() batch gate: expanded from 2-line comment to
#               6-line block with "Write nothing more. Generate nothing more."
#               and cross-reference to S3-4a + MockCreate MANDATE 1 STEP 6.
#           (4) S3-4 Anti-Editorializing items 7-8: added explicit note that
#               the response ENDS after printing items 1-7 (S3-4a reference).
#           (5) §12 DoD: batch gate checklist item expanded with S3-4a reference
#               and explicit "including small corpora" qualifier.
#           (6) S3-4a STEP 3 + S3-5 run_scan(): added present_files call for
#               scan_progress.json + classifications.json after each non-final
#               batch. Previously files were saved to disk silently with no
#               download link — user could not grab progress for session resume.
#               Matches MockTestAnalyse S8-3 pattern (summary → present_files
#               → continue prompt). Continue prompt is always the LAST line.
#
#           CROSS-FRAMEWORK NOTE: Phase B counting (S5-7/S5-8) uses a Python
#           script execution model where all batches run in one script call —
#           the Batch Stop Law does NOT apply to script-executed batches (the
#           script handles its own save-after-each-batch logic). The law applies
#           to interactive chat-based batch processing only (Phase 0b scan).
#           MockTestAnalyse (PYQExtract) has its own batch gate via Options A/B
#           pattern — verify that framework separately.
#
#           DELIVERABLE SET CONTRACT CHANGES:
#           (7) §10 REWRITTEN — DELIVERABLE SET CONTRACT: closed deliverable
#               sets for all 4 modes (--taxonomy, --scan, --approve, --counts).
#               Each mode defines EXACTLY which files to deliver and an explicit
#               DO-NOT-DELIVER list of internal/intermediate files. Pre-delivery
#               checklist (S10-2) blocks present_files until the call contains
#               EXACTLY the expected files and nothing else.
#               Mirrors MockCreate's S13-6 (closed set), S13-7 (pre-delivery
#               checklist), and R-DELIVER (named rule).
#               LIVE FAILURE: SSC CGL Tier 2 --scan delivered an unauthorized
#               taxonomy_draft_v2.json because no "NOTHING ELSE" qualifier
#               existed and no DO-NOT-DELIVER list blocked extra files.
#           (8) Header OUTPUTS section: updated with "(N files, nothing else)"
#               qualifiers and cross-reference to §10. classifications.json
#               now explicitly listed (was changelog-only since v1.7 C2).
#           (9) S2-6, S3-5, S3-7, S4-3, S5-5, S5-8: delivery instructions
#               updated to reference S10-1 closed set and S10-2 pre-delivery
#               checklist.
#           (10) §12 DoD: all 4 phases updated with closed-set verification
#               items and pre-delivery checklist pass requirement.
#
#   v2.8 — 2026-07-06 — SYLLABUS-ENUMERATED ITEMS MUST BECOME SUBTOPICS.
#           ROOT CAUSE: Comparative analysis of framework-generated (68 subtopics) vs
#           PYQ-grounded (209 subtopics) Analysis docs for SSC CGL Tier 1 revealed a
#           3× subtopic gap. The merge-over-split bias (v2.4) was too aggressive —
#           Claude interpreted it as "if the Topic name covers it, don't create
#           subtopics", producing 1:1 Topic=Subtopic mappings (e.g., "Geometry" → 1
#           subtopic "Geometry" despite the syllabus explicitly listing Triangles,
#           Circles, Polygons as separate items). This is data loss, not conservative
#           merging.
#
#           CHANGE 1 — S2-3 CORE PRINCIPLE: Added CRITICAL SCOPE OF MERGE BIAS
#             clarification. The merge bias applies ONLY to AI-invented splits, NOT
#             to items the syllabus itself explicitly enumerates. Suppressing
#             syllabus-enumerated items is data loss. Added SSC CGL Tier 1 counter-
#             evidence alongside the MPPSC Botany evidence.
#           CHANGE 2 — S2-3 Step 1 GROUPING RULE: Added GROUPED ITEMS ARE SUBTOPICS
#             mandatory rule. When multiple syllabus items are grouped into one Topic,
#             every grouped item MUST become a named subtopic. Includes 3 failure
#             examples (Geometry, Trigonometry, Polity) with correct vs wrong output.
#           CHANGE 3 — S2-3 Step 1 GROUPING RULE: Added 1:1 TOPIC=SUBTOPIC DETECTOR
#             self-check. After subtopic derivation, any Topic with exactly 1 subtopic
#             of the same name is flagged for re-derivation (unless the syllabus
#             genuinely lists it as a single atomic concept).
#           CHANGE 4 — §12 DoD Phase 0a: Added 1:1 Topic=Subtopic check item.
#
#   v2.7 — 2026-07-06 — CATCH-ALL / RESIDUAL TOPIC PROHIBITION.
#           ROOT CAUSE: Live execution on SSC CGL Tier 2 produced "Topic 17: Other
#           Sub-topics" containing Blood Relations, Seating Arrangement, Syllogism,
#           Dice and Cubes, Ranking and Ordering, Logical Sequence — all distinct
#           question types that should be separate Topics. Claude ran out of patience
#           while processing a long syllabus and dumped remaining items into a residual
#           bin, violating the Topic Integrity Test.
#
#           CHANGE 1 — S2-3 Step 1: Added CATCH-ALL / RESIDUAL TOPIC PROHIBITION
#             rule with explicit banned patterns (case-insensitive substring match):
#             "other", "miscellaneous", "misc", "remaining", "additional",
#             "general topics", "catch-all", "residual". Includes failure example
#             from SSC CGL Tier 2 and mandatory self-check after Topic derivation.
#           CHANGE 2 — S2-3 EXCLUSION RULES: Added matching prohibition at Subtopic
#             level — same banned patterns apply to Subtopic names.
#           CHANGE 3 — S2-3 QUALITY GATE: Added CATCH-ALL NAME CHECK as a mandatory
#             gate that runs after all other quality gates. HARD STOP if any
#             Topic or Subtopic name matches a banned pattern.
#           CHANGE 4 — §12 DoD Phase 0a: Added catch-all name check item.
#
#   v2.6 — 2026-07-06 — MERGED ANALYSIS DOC (single file replaces per-subject files).
#           ROOT CAUSE: Phase 0c produced one .docx per subject (e.g. 4 files for SSC
#           CGL Tier 1). This created unnecessary file management overhead: N+1 files
#           to upload, track, and version; risk of missing one subject's doc during
#           upload; partial-update risk during Phase B; and the "missing ONE subject"
#           fallback (S10-6 in downstream Blueprint) that was fragile. Every downstream
#           parser (PYQSort, Step 5, Step 6) already identifies sections by CONTENT
#           (the "Subject: [Name]" header inside the doc), not by filename — so the
#           per-file split had no technical justification.
#
#           CHANGE 1 — S4-1: Output is now a single [ExamCode]_PYQ_Analysis.docx
#             containing ALL subjects, separated by page breaks. Internal structure
#             per subject is unchanged (header block, master summary table, per-topic
#             subtopic tables, footer). File management drops from N+1 to 2 files
#             (1 Analysis doc + 1 exam_config.json).
#           CHANGE 2 — S4-2: generate_analysis_doc() → generate_merged_analysis_doc()
#             accepts full taxonomy dict, iterates all subjects with page breaks.
#           CHANGE 3 — S4-4: Approval gate message updated for single-file output.
#             Lists sections within the doc instead of separate filenames.
#           CHANGE 4 — S5-4b/S5-5/S5-8: Phase B references updated from plural
#             "Analysis docs" to singular "Analysis doc" — same parsing logic, single
#             file load/save instead of per-file iteration.
#           CHANGE 5 — S10-3/S10-4: Delivery sections updated for single file.
#           CHANGE 6 — §7 Name Consistency: "Analysis docs" → "Analysis doc".
#           CHANGE 7 — §12 DoD Phase 0c: "One Analysis .docx per subject" →
#             "Single merged Analysis .docx with all subjects".
#           CHANGE 8 — S1-2 --counts mode, EC-P1, EC-P29: plural → singular.
#
#           DOWNSTREAM CONSUMERS — CORRECTED 2026-07-25 (GAP-2026-07-25-002).
#           The original v2.6 entry claimed: "All downstream consumers (PYQSort,
#           Step 5, Step 6) require NO spec changes — they already parse by content
#           pattern, not file boundary. The downstream specs use glob patterns or
#           direct file load; both work with a single file. Cross-step contract
#           unchanged." Every clause of that was wrong, and it stood for 19 days
#           and 7 PYQSort releases.
#             "parse by content pattern, not file boundary" conflated two things.
#           PYQSort parsed taxonomy LEVELS by content pattern — true, and presumably
#           what was checked — but it DISCOVERED the file by filename glob and
#           DELIMITED SUBJECTS BY FILE BOUNDARY, which is exactly what this change
#           removed. The analysis inspected the parser's inner loop, never its outer.
#             "both work with a single file" reasoned only about CARDINALITY. v2.6
#           changed two independent axes: cardinality (N -> 1) AND the filename. A
#           glob does work with a single file; it does not work with a RENAMED file.
#             "Cross-step contract unchanged" — a deliverable's filename IS the
#           cross-step contract. It changed.
#           ACTUAL IMPACT, measured 2026-07-25 against the first exam's live doc:
#             PYQSort  BROKEN ON BOTH AXES. Its glob matched zero files (loud), and
#                      its parser flattened 6 subjects into 1 (silent). Fixed v1.14.
#             Step 5   BROKEN, but not by this change — both of its Analysis-doc
#                      readers returned ZERO subtopics from any real doc and always
#                      had. Fixed in MockTestAnalyse v2.30.
#             Step 6   read the doc as prose: format-tolerant but non-deterministic.
#                      Fixed in Blueprint v1.39.
#           RULE: a deliverable RENAME, or a CARDINALITY change, is a cross-step
#           contract change. Every consumer's discovery pattern must be re-tested
#           against the new literal name AND every consumer's parser re-tested
#           against the new file SHAPE. A changelog assertion of downstream
#           compatibility is not evidence. Enforced by Check AF.
#
#   v2.5 — 2026-07-06 — STANDARDIZED EXAM PATTERN XLSX + EXAM_CONFIG SCHEMA OVERHAUL.
#           ROOT CAUSE: Exam pattern was read via AI interpretation of image/PDF/docx —
#           ambiguous, non-deterministic, and unable to capture per-range marking schemes
#           (e.g., CSIR NET Part C: 4 marks/Q vs Part A/B: 2 marks/Q), attempt limits
#           (e.g., CSIR NET: attempt 15/20 in Part A), or academic level. Validated
#           against 7 exam patterns: SSC CGL T1/T2, MPSC Botany, CSIR NET Life Science,
#           CSIR NET Mathematical Science, GATE Biotechnology, IIT JAM Chemistry.
#
#           CHANGE 1 — S1-2 + S2-2: XLSX AS PREFERRED INPUT FORMAT:
#             Exam pattern now accepted as .xlsx with 3 standardized tabs:
#               Tab 1 "Overview": key-value pairs (Total Questions, Medium, Question Type,
#                 Total Marks, Duration, Level)
#               Tab 2 "Sections": table (Section, Total Question, Question Starts,
#                 Question Ends, Max Attempt)
#               Tab 3 "Range": table (Question Range, Question Type, Correct Marks,
#                 Negative Marks)
#             Deterministic parser replaces AI interpretation. Legacy image/PDF/docx
#             path preserved as backward-compatible fallback.
#
#           CHANGE 2 — S2-2: 10 STRUCTURAL VALIDATIONS ON XLSX:
#             V1: Σ(Total Question) == Total Questions (Overview)
#             V2: Q_Ends − Q_Starts + 1 == Total Question (per section)
#             V3: Section Q-ranges contiguous and non-overlapping
#             V4: Range tab tiles Q.1 through Total Questions completely
#             V5: All Negative Marks ≤ 0
#             V6: Σ(Max Attempt × correct_marks) == Total Marks
#             V7: 0 < Max Attempt ≤ Total Question (per section)
#             V8: Overview Question Type set == Range tab distinct types
#             V9: All Correct Marks > 0
#             V10: Total Questions > 0, Duration > 0
#             Any failure → HARD STOP with specific error.
#
#           CHANGE 3 — S2-2: SECTION ≠ SUBJECT CLARIFICATION:
#             Section names from Sections tab are OTS (Online Test Series) display labels
#             only. They do NOT define Subject names for the taxonomy. The syllabus
#             (provided separately) defines Subjects, Topics, and Subtopics. A single
#             Subject can span multiple sections (e.g., CSIR NET: "Cell Biology" questions
#             appear in both Part B and Part C). The framework must never conflate
#             Section with Subject.
#
#           CHANGE 4 — S2-5: EXAM_CONFIG.JSON SCHEMA OVERHAUL:
#             Removed: marks_per_question (single int), negative_marking (single float).
#             Added: medium (str), question_types (list), level (str),
#               marking_scheme[] (per-range: q_range, question_type, correct_marks,
#               negative_marks), max_attempt (per section).
#             Per-range marking replaces global scalars — handles CSIR NET (2m vs 4m),
#             GATE (1m vs 2m, MCQ vs MSQ vs NAT per range), IIT JAM (MCQ/MSQ/NAT
#             sections with mixed marks). Float marks supported (CSIR NET Math: 4.75).
#
#           CHANGE 5 — S2-6 DELIVERY MESSAGE: includes new fields.
#           CHANGE 6 — §12 DoD: updated for xlsx validation + new schema fields.
#
#   v2.4 — 2026-07-05 — TAXONOMY DEPTH ARCHITECTURE OVERHAUL (S2-3 rewrite).
#           ROOT CAUSE: v1.5's "when in doubt, SPLIT" + mandatory 6 pattern dimensions
#           produced 336 subtopics for MPPSC Botany (81 syllabus entries → 4.1× inflation).
#           PYQ classification then failed on 38% of questions (93/150 mapped). Root cause
#           traced via comparative analysis of 13 exam syllabi: SSC CGL T1/T2, CAT, MPPSC
#           Botany, CSIR NET Life Sci, GATE CS, GATE Biotech, IIT JAM Physics, UGC NET
#           History, CUET PG Math, CUET UG Political Sci, NEET, CTET Paper 1.
#
#           CORE PRINCIPLE — UNIQUE DOMAIN PROPERTY:
#             Every subtopic must uniquely claim a concept set that no other subtopic also
#             claims. Given any PYQ question, exactly ONE subtopic must be the unambiguous
#             best match. Over-splitting violates this by creating near-duplicate bins that
#             confuse the classifier. Over-merging preserves it (loses granularity but
#             classifies 100% of questions). Default bias: MERGE over SPLIT.
#
#           CHANGE 1 — S2-3 COMPLETE REWRITE:
#             Replaced "6 mandatory pattern dimensions applied to every Topic" with a
#             3-question per-entry decision tree (Q1: explicit identifier? Q2: internal
#             sub-structure? Q3: Unique Domain Check). The 6 dimensions are retained as
#             an OPTIONAL tool for undivided-block entries only, not a mandatory universal
#             procedure. Subtopic derivation default reversed from "SPLIT" to "follow
#             syllabus structure faithfully."
#           CHANGE 2 — EXCLUSION RULES:
#             Vocabulary lists, glossary terms, named reactions, individual organisms,
#             historical terms, and enumerated scope items within colon-descriptors are
#             explicitly excluded from becoming subtopics.
#           CHANGE 3 — SANITY CHECKS:
#             Added ratio guardrail (flag at 2.0×, hard-stop at 3.0×), near-duplicate
#             detection (>75% name similarity), keyword overlap check (<30%), and
#             total-coverage verification (every syllabus concept → exactly 1 subtopic).
#           CHANGE 4 — QUALITY GATE REWRITE:
#             Replaced fixed benchmark (150–250 subtopics) with ratio-based guardrail
#             that scales to any exam size.
#           CHANGE 5 — §3-6 REFINEMENT PASS DEFAULT BIAS:
#             Changed from "split broad subtopics" to "merge confused subtopics first,
#             split only with ≥15 Qs evidence + Q3 Unique Domain Check pass."
#           CHANGE 6 — §11 and §12 UPDATED:
#             Exam-agnostic guarantee and DoD updated to reflect new taxonomy rules.
#
#           Validated against 13 exams: all produce ratio ≤ 2.6×. The MPPSC Botany
#           disaster (4.1×) would be prevented (ratio = 1.0× under new rules).
#   v2.3 — 2026-07-05 — PHASE 0b CONSISTENCY FIXES (3 issues).
#           (1) MEDIUM — S3-2 vs S3-7 CONTRADICTION: S3-2 said "no re-listing
#               on resume" but S3-7 (v2.2) said "RE-LIST". FIXED: S3-2 cached
#               inventory section now defers to S3-7 for resume behaviour.
#               First-session caching unchanged; resume re-lists per S3-7.
#           (2) LOW-MEDIUM — ANTI-EDITORIALIZING RULE UPDATED (S3-4): the
#               "NOTHING ELSE" allowed list now explicitly includes v2.2's
#               per-section Q distribution and classification quality output.
#               Without this, Claude could interpret v2.2 additions as violating
#               the anti-editorializing rule.
#           (3) LOW — total_available META UPDATE (S3-5): run_scan now writes
#               total_available to progress['_meta']['total_available'] before
#               first batch. Without this, saved scan_progress.json permanently
#               showed total_available=0 (the init default), breaking convergence
#               gates on resume if they read from _meta instead of parameter.
#   v2.2 — 2026-07-05 — PHASE 0b DEEP-AUDIT (4 gap fixes).
#           (1) HIGH — POST-CONVERGENCE SUMMARY (S3-5 updated): before printing
#               "Run: PYQApprove", display a comprehensive summary: original
#               taxonomy size vs final (after scan + refinement), net discovery
#               (+N new, +M from splits, -K removed), classification quality
#               (normal vs OMML-obscured vs figure-inferred percentages),
#               per-section snapshot (section → topics → subtopics), and papers
#               scanned per year. User needs full visibility before locking.
#           (2) MEDIUM — CLASSIFICATION QUALITY TRACKING (S3-5 batch-end updated):
#               after each batch, show per-section Q-count AND quality breakdown
#               (normal / OMML-obscured / figure-inferred counts). Surfaces
#               degraded classification rates early — if 40%+ are OMML-obscured,
#               the scan might miss patterns.
#           (3) LOW-MEDIUM — BATCH-END PER-SECTION Q-COUNT (S3-5 batch-end
#               updated): show per-section classified Q distribution after each
#               batch. Catches section detection failures (wrong marker_mode or
#               Q-range config) within the first batch, not after 60+ papers.
#           (4) LOW-MEDIUM — RESUME DRIVE RE-VERIFICATION (S3-7 updated): resume
#               sessions now re-list Drive files and re-run S3-2a pre-scan gate
#               instead of relying on cached inventory. Catches files added or
#               removed between sessions. Aligned with Phase B's S5-7 pattern.
#           §12 Phase 0b DoD updated: 3 new items.
#   v2.1 — 2026-07-05 — PRE-SCAN CONFIRMATION GATE (1 addition).
#           (1) NEW S3-2a — PRE-SCAN CONFIRMATION GATE: after collecting and
#               ordering all Row files (S3-2) but before any batch scanning
#               (S3-3/S3-5), display a year-wise paper inventory table with
#               per-paper Q counts (verified by parsing or from filename
#               pattern). Wait for explicit user confirmation before proceeding.
#               Proves Claude can see every file and every question. Matches
#               the Step 4 (PYQCount) Task 1 pattern (S5-1a) for consistency.
#               §12 Phase 0b DoD updated with 2 new items.
#   v2.0 — 2026-07-05 — PHASE B FINAL DEEP-AUDIT (7 fixes).
#           (1) HIGH — CHILD POINTER RESET (S5-2): count_sorted_file() now
#               resets cur_top + cur_sub when a new Section heading is found,
#               and resets cur_sub when a new Topic heading is found. Matches
#               Step 5 E-1 pseudocode (current_path[:level-1] + [content]).
#               Without this, a question after a Topic heading but before its
#               first Subtopic would silently inherit the wrong subtopic from
#               the previous topic — invisible to all Task gates.
#           (2) HIGH — TASK 1 Q-COUNTING METHOD (S5-1a): now explicitly
#               specifies: use python-docx paragraph iteration with the SAME
#               Q-pattern (r'^Q\.?\s*\d+') as count_sorted_file(). Also
#               documents the PYQSort renumber_stem dependency (sorted files
#               always output Q.<N> format). Also specifies per-file Q-count
#               storage for Task 2 diagnostic.
#           (3) BUG — TASK 2 FLOW REFERENCE (S5-4a): "Proceed to S5-5" fixed
#               to "Proceed to S5-4b (Task 2.5)." Was skipping the taxonomy
#               name cross-check in the documented flow.
#           (4) HIGH — TASK 2.5 EXTRACTION METHOD (S5-4b): now specifies exact
#               rules for extracting (section, topic, subtopic) triples from
#               Analysis doc tables. Section name from doc header (strip
#               "[ExamCode] — " prefix). Topic name from master table cells
#               (strip "Topic N: " prefix via parse_taxonomy_level). Subtopic
#               name from per-topic table cells (raw text .strip()). Ensures
#               extracted names match parse_taxonomy_level() output.
#           (5) MEDIUM — TASK 2 PER-FILE DIAGNOSTIC (S5-4, S5-4a): batch
#               counting now tracks per_file_attributed[filename] = sum of
#               attributed counts. When Task 2 fails, compares against Task 1
#               per-file Q-counts to identify exactly which files have
#               discrepancies and by how many.
#           (6) MEDIUM — PHASE B EXECUTION MODEL (new S5-8): specifies Python
#               script-based execution via count_pipeline.py. Script processes
#               files in batches, writes results to JSON, runs all gates.
#               3-tool-call model: create_file → bash_tool → present_files.
#           (7) LOW — DEDUP REGEX MULTI-DATE FIX (S5-1): multi-date filenames
#               (containing "_to_") are now excluded from dedup — they represent
#               unique combined papers by definition.
#   v1.9 — 2026-07-05 — PHASE B DEEP-AUDIT (6 gap fixes).
#           (1) CRITICAL — TAXONOMY NAME CROSS-CHECK (new S5-4b, TASK 2.5):
#               after Task 2 passes, cross-check every counted (section, topic,
#               subtopic) triple against the Analysis doc taxonomy. Flag phantom
#               triples (counted but not in doc) and orphan subtopics (in doc but
#               not counted). Prevents silent count loss from name mismatches
#               (trailing spaces, dash variants, case differences). HARD STOP
#               if any phantom triples found.
#           (2) HIGH — ORPHAN QUESTION TRACKING (S5-2 updated): count_sorted_file()
#               now tracks orphan questions (Q found before any Subject/Subtopic
#               heading) separately. Returns orphan list with file, Q number, and
#               reason. Task 2 failure message includes orphan diagnostic.
#           (3) MEDIUM — SORTED FILE FILTERING (S5-1 updated): Drive listing now
#               filters for files matching sorted filename pattern (*_Sorted_*.docx).
#               Non-sorted .docx files (Row files, other docs) are skipped with
#               a logged warning. Prevents double-counting.
#           (4) MEDIUM — DUPLICATE SORTED FILE DETECTION (S5-1 updated): same-date
#               same-session dedup applied to sorted files. If two sorted files
#               share the same date+session, keep the larger file, skip the
#               smaller. Log the skip. Prevents inflated counts.
#           (5) MEDIUM — PHASE B SESSION MANAGEMENT (new S5-7): explicit session
#               protocol for large corpora. Resume via re-trigger with same Drive
#               link. count_progress.json tracks processed files for skip-on-resume.
#               Task 1 re-runs on resume (re-confirms full inventory).
#           (6) LOW-MEDIUM — ZERO-COUNT SUBTOPICS (S5-5 updated): explicit rule
#               that 0 is a valid count written as "0". No subtopic may remain
#               "—" after Phase B. Subtopics with 0 PYQs get "0" not "—".
#           New edge cases: EC-P27 (phantom triple), EC-P28 (orphan Q in sorted
#           file), EC-P29 (non-sorted file in Drive folder), EC-P30 (duplicate
#           sorted file).
#           §12 Phase B DoD updated: 6 new items.
#   v1.8 — 2026-07-05 — PHASE B QUALITY GATES + BATCH SIZE (4 tasks, 5 changes).
#           (1) TASK 1 — PRE-COUNT CONFIRMATION GATE (new S5-1a): after reading
#               all sorted PYQ files from Drive, display year-wise paper inventory
#               with per-paper Q counts before any subtopic counting begins. Wait
#               for explicit user confirmation. Proves all files and all questions
#               are visible.
#           (2) TASK 2 — POST-COUNT ACCURACY GATE (new S5-4a): after all batch
#               counting is complete, display full Subject > Topic > Subtopic
#               breakdown with counts. Grand total must exactly equal the confirmed
#               total from Task 1. If mismatch (even 1 Q) → re-scan and fix before
#               proceeding. Zero tolerance.
#           (3) TASK 3 — DOC-WRITING ACCURACY GUARANTEE (S5-5 expanded): every
#               number inserted into Analysis docs must be arithmetically verified
#               at 4 levels: subtopic cells, topic TOTAL rows, master summary table,
#               header line. Cross-check: header == GRAND TOTAL == sum(topic totals)
#               == sum(subtopic counts). Any mismatch → fix before delivering.
#           (4) TASK 4 — BATCH SIZE REDUCED: BATCH_SIZE_COUNTS changed from 15 → 5.
#               S5-1 prose updated from "batch 10-15 files" → "batch up to 5 files".
#               §11 batch model updated.
#           (5) §12 Phase B DoD updated: 4 new Task gates added.
#   v1.7 — 2026-07-04 — RUNTIME GAP FIXES (32 issues from live execution).
#           Source: PYQAnalyse_Gap_Analysis_v1.md — live execution against
#           SSC CGL Tier 1 (200 papers, 7 years) exposed 32 gaps in 9 categories.
#           3 CRITICAL, 7 HIGH, 12 MEDIUM, 10 LOW — all fixed.
#
#           CATEGORY A — CONVERGENCE ENFORCEMENT (6 fixes):
#           (A1) CRITICAL: Anti-editorializing rule for JSON — Claude added
#                convergence_recommendation, scan_analysis fields to progress JSON.
#                FIX: BANNED JSON FIELDS list + schema-only enforcement.
#           (A2) CRITICAL: Anti-editorializing rule for chat — Claude argued
#                "taxonomy is functionally stable" alongside FAIL gate statuses.
#                FIX: Mandatory batch-end message template + BANNED PHRASES list.
#           (A3) MEDIUM: Gate 3 counter cited before Gate 2 met. FIX: counter is
#                informational noise before Gate 2 — documented.
#           (A4) HIGH: Strongest language only in code comments. FIX: prose-level
#                MANDATE block added before S3-4 code block.
#           (A5) MEDIUM: No papers-per-session expectation. FIX: 4-5 batches/session
#                target added to new S3-7 session management.
#           (A6) LOW: offer_early_exit name primes exit-thinking. FIX: renamed to
#                report_gate_status.
#
#           CATEGORY B — BATCH PROCESSING (4 fixes):
#           (B1) HIGH: Partial batches (1-2 papers) counted as complete. FIX:
#                BATCH INTEGRITY RULE — partial batch does not increment/reset counter.
#           (B2) MEDIUM: No explicit increment/reset code. FIX: explicit code with
#                "2 empty + 1 discovery = RESET" annotation.
#           (B3) MEDIUM: No response budget guidance. FIX: response budget section
#                with fallback to 2-paper batches.
#           (B4) HIGH: File reading method unspecified — Drive read_file_content
#                strips OMML/images. FIX: Drive reading method spec with OMML/figural
#                fallback classification rules.
#
#           CATEGORY C — CLASSIFICATION QUALITY (5 fixes):
#           (C1) CRITICAL: Per-question classifications not stored — only paper
#                summaries. FIX: per-Q storage mandate + separate classifications
#                file for large corpora.
#           (C2) HIGH: scan_progress.json too large (6000+ records). FIX: split
#                classifications into [ExamCode]_classifications.json.
#           (C3) MEDIUM: No new-discovery validation protocol. FIX: 3-question
#                validation gate before adding new subtopic.
#           (C4) MEDIUM: Figural questions classified blind during scan. FIX:
#                text-clue inference rules + EC-P24.
#           (C5) LOW: No per-section Q-count validation. FIX: post-paper validation
#                with informational warnings.
#
#           CATEGORY D — TAXONOMY & SCHEMA (3 fixes):
#           (D1) MEDIUM: Taxonomy authority chain unclear. FIX: explicit chain
#                documented (taxonomy_draft → scan_progress → PYQApprove).
#           (D2) HIGH: Full taxonomy not stored — only deltas. FIX: scan_progress
#                ['taxonomy'] must be COMPLETE (original + discoveries).
#           (D3) LOW: No schema version enforcement. FIX: version check in
#                load_scan_progress with error message.
#
#           CATEGORY E — REFINEMENT PASS (4 fixes):
#           (E1) HIGH: Refinement data impractical at scale. FIX: per-subtopic
#                sequential execution model with 50-Q sampling.
#           (E2) MEDIUM: Post-refinement gate re-check ambiguous. FIX: EC-P19
#                updated — Gate 2 not re-checked, only Gate 3.
#           (E3) MEDIUM: check_dimensional_splits unimplemented. FIX: structured
#                Counter-based algorithm with concrete example.
#           (E4) LOW: No refinement output verification. FIX: orphan check.
#
#           CATEGORY F — SESSION MANAGEMENT (3 fixes):
#           (F1) HIGH: No session management for large corpora. FIX: new S3-7
#                session management section with protocol and formula.
#           (F2) LOW: Drive listing not cached. FIX: drive_file_inventory in
#                scan_progress.json.
#           (F3) LOW: No Drive rate limit handling. FIX: retry-once + save guidance.
#
#           CATEGORY G — PAPER SELECTION (2 fixes):
#           (G1) MEDIUM: Cherry-picking small files. FIX: date-asc/shift-asc
#                ordering within each year — no reordering by size.
#           (G2) LOW: Newest-year-first bias undocumented. FIX: design note added.
#
#           CATEGORY H — CROSS-STEP CONTRACT (2 fixes):
#           (H1) MEDIUM: PYQApprove required fields unspecified. FIX: explicit
#                field list added to S4-1.
#           (H2) LOW: taxonomy_draft → scan_progress copy not explicit. FIX:
#                source_taxonomy tracking in init + authority chain docs.
#
#           CATEGORY I — MISSING EDGE CASES (3 fixes):
#           (I1-I3) LOW: EC-P21 (mixed file types), EC-P22 (duplicate filenames),
#                EC-P23 (Drive folder structure variants).
#
#           Additional edge cases from other categories:
#           EC-P24 (figural scan misclassification), EC-P25 (OMML-obscured scan),
#           EC-P26 (partial batch on context limit).
#
#           Structural changes:
#           - S3-7 is now Session Management (new). Old S3-7 → S3-8.
#           - report_gate_status replaces report_gate_status.
#           - §11 updated: 26 edge cases.
#           - §12 DoD updated for session management and classification storage.
#   v1.6 — 2026-07-04 — CROSS-STEP SYNC + EXAM-AGNOSTIC FIX (6 bugs).
#           (1) MISSING FOOTER: no "END OF" marker — every other framework file has
#               one. FIXED: added.
#           (2) EXAM-SPECIFIC JSON EXAMPLE (S2-5): exam_config schema used hardcoded
#               SSC CGL Tier 1 values (exam_code, exam_name, 4 SSC section names with
#               specific q_ranges). FIXED: replaced with [ExamCode]/[Section N Name]
#               placeholders matching the exam-agnostic pattern of other framework files.
#           (3) 'TestSeriesRow' STALE NAME (3 refs in header): Step 1 PYQ Prepare was
#               still referenced by its old name. v1.2 fixed TestSeriesSort→PYQSort but
#               missed TestSeriesRow. FIXED: "Step 1 PYQ Prepare" / "Step 1 (PYQ Prepare)".
#           (4) PIPELINE POSITION MISSING STEP NUMBERS: PYQExtract and MockBlueprint
#               listed without canonical step numbers. FIXED: "Step 5 PYQExtract",
#               "Step 6 MockBlueprint", "Step 3 PYQSort".
#           (5) exam_config SCHEMA MISSING 3 FIELDS: session_keyword, page_size,
#               options_count — all consumed by PYQSort (v1.3/v1.4) but not defined in
#               the schema that creates exam_config.json. PYQSort used silent defaults
#               (Shift, A4, 4) which worked but weren't documented as the contract.
#               FIXED: all 3 added to S2-5 schema with field definitions + defaults.
#           (6) PREREQUISITE section hardcoded "Shift" in date label format description.
#               FIXED: uses "<session_keyword>" placeholder (configurable per exam).
#           Cross-step sync verified: PYQSort v1.4 (session_keyword, page_size,
#           options_count consumption), Step 5 (OPT_PATTERNS byte-identical — confirmed
#           in PYQSort audit), Step 6 Blueprint v1.17 (Analysis doc consumption).
#   v1.5 — 2026-07-04 — TAXONOMY-DEPTH OVERHAUL (5 architectural fixes).
#           ROOT CAUSE: v1.0–v1.4 produced shallow taxonomies (119 subtopics for
#           SSC CGL Tier 1 vs 221 required) because of 5 cascading failures:
#           (F1) S2-3 merged syllabus items into mega-Topics (4 English Topics
#                instead of 12) → subtopic space collapsed before scan began.
#           (F2) S2-3 subtopic derivation used FORMAT categories (Word/Number/
#                Letter/Figure) instead of QUESTION PATTERNS — and the rule
#                "when in doubt KEEP AS SINGLE" suppressed Claude's domain
#                knowledge, producing 15 English subtopics instead of 66.
#           (F3) check_convergence() 30% hard gate was not enforced at runtime —
#                Claude treated consecutive_empty as standalone trigger, scanning
#                only 13/198 papers (6.6%) instead of the required 59 (30%).
#           (F4) CONVERGENCE_CONSECUTIVE=3 meant 9 papers without a new subtopic
#                triggered convergence — meaningless when the coarse taxonomy
#                absorbed every question.
#           (F5) scan_paper() had no subtopic refinement — binary "fits / doesn't
#                fit" could never discover patterns WITHIN existing broad subtopics.
#
#           FIX 1 — S2-3 TOPIC MAPPING REWRITE:
#             Each individually-listed syllabus item that represents a distinct
#             question type = one Topic. "Group into mega-Topics" instruction
#             removed. New TOPIC INTEGRITY TEST added (3 questions).
#           FIX 2 — S2-3 SUBTOPIC DERIVATION REWRITE:
#             Default reversed: "When in doubt, SPLIT" (not keep-as-single).
#             6 mandatory pattern dimensions added (Format, Direction, Task,
#             Content/Thematic, Structural, Medium). Claude MUST apply all 6
#             to every Topic. Target = coaching-institute practice-set granularity.
#           FIX 3 — CONVERGENCE HARD GATES:
#             4-gate architecture: Gate 0 (small corpus → scan all), Gate 1
#             (all years covered), Gate 2 (30% papers), Gate 3 (7 consecutive
#             empty batches — raised from 3), Gate 4 (refinement pass done).
#             Language upgraded to non-bypassable absolute enforcement.
#           FIX 4 — SUBTOPIC REFINEMENT PASS (new §3-6):
#             Mandatory pass after gates 1-3. Reviews classified questions per
#             subtopic, applies 6 pattern dimensions, splits broad subtopics.
#             Runs BEFORE convergence can be declared.
#           FIX 5 — RULE 7 PATTERN METADATA:
#             scan_paper() now records question_task, question_format,
#             question_direction, thematic_domain per classification.
#             Enables refinement pass splitting decisions.
#
#           Additional changes:
#           - 4 new edge cases: EC-P17 (subtopic with 0 PYQs after split),
#             EC-P18 (refinement creates duplicate subtopic name across Topics),
#             EC-P19 (scan resume after refinement), EC-P20 (syllabus with
#             pre-grouped items vs individually-listed items).
#           - §11 updated: classification rules 1-7, 20 edge cases.
#           - §12 DoD updated for refinement pass items.
#           - scan_progress.json schema extended with pattern metadata and
#             refinement_pass_done flag.
#           SELF-AUDIT (5 additional fixes after domain-expert simulation):
#           (6) CRITICAL: check_dimensional_splits said "apply FIRST split
#               that works" — blocked multi-dimensional splitting (e.g.,
#               Analogy Dim 5 fires, Dim 6 Figural never applied). FIX:
#               replaced with holistic all-dimensions merge rule.
#           (7) S2-3 Step 2 Derivation Procedure lacked merge instruction
#               for subtopics from multiple dimensions + had zero QA
#               examples. FIX: added step 6 (merge across dimensions) with
#               overlap resolution rule + QA examples (Interest, Mensuration,
#               Trigonometry, Statistics/DI).
#           (8) EC-P2 (1-2 papers) had stale language ("no convergence check
#               needed") that predated Gate 0 architecture. FIX: references
#               Gate 0 + Gate 4 (refinement still applies).
#           (9) BATCH_SIZE comment said "locked" but EC-P15 said "reduce to 2
#               for 500+ subtopics". FIX: BATCH_SIZE comment changed to
#               "default" with flexibility note; EC-P15 aligned.
#           (10) EC-P1 (0 papers) didn't note that Step 2a's 6-dimension
#                derivation produces coaching-depth taxonomy without scanning.
#                FIX: added explicit note.
#           DEEP LINE-BY-LINE AUDIT (5 more fixes):
#           (11) CRITICAL: S2-1 had stale pre-v1.5 language ("Identify natural
#                groupings", "splitting broad items") that contradicted S2-3's
#                Topic Integrity Test. Claude reading S2-1 first would mentally
#                group items into mega-Topics before S2-3 could override.
#                FIX: S2-1 now says "preserve each item as-is" and defers
#                Topic/Subtopic decisions to S2-3.
#           (12) CRITICAL: Gate 3 required consecutive_empty >= 7 even when
#                total_available = 0 (or all papers scanned). With 0 papers,
#                no batches run → consecutive_empty stays 0 → Gate 3 returns
#                'continue' forever. Also scan_progress.json was never saved
#                in the 0-paper path (save only called inside batch loop).
#                FIX: Gate 3 now SKIPS when all_papers_scanned (scanned >=
#                total_available). run_scan "not pending" path now saves
#                progress before returning.
#           (13) CRITICAL: When all papers scanned but Gate 3 not met,
#                refinement pass was SKIPPED — the "else" branch just printed
#                "Run: PYQApprove" without running refinement. FIX: run_scan
#                "not pending" path now ALWAYS runs refinement if not done,
#                then saves progress, then prints proceed message.
#           (14) MEDIUM: S4-4 approval gate message said "correctly grouped"
#                — stale pre-v1.5 language encouraging mega-Topic review.
#                FIX: updated to match v1.5 rules (distinct Topics per
#                syllabus item, coaching-depth subtopics, benchmark count).
#           (15) LOW: S2-6 delivery message didn't include quality gate
#                benchmark result. User couldn't verify depth at delivery.
#                FIX: added benchmark line to delivery message.
#   v1.4 — 2026-07-04 — GAP FIX (1 fix).
#           (1) Step 2b (PYQScan) trigger had no PYQ: <<Drive link>> parameter,
#               even though S3-2 collect_row_files() already accepted drive_folder_id
#               and the header INPUTS section said "from uploads or Google Drive".
#               FIX: added optional PYQ: <<Drive link>> to Step 2b trigger format
#               (header, S1-1 trigger formats, S1-1 parse block, S1-2 file inventory).
#               Step 2b now has parity with Step 4/Step 5 Drive link syntax.
#               Row files via chat upload remain the fallback when PYQ: is absent.
#   v1.3 — 2026-07-03 — FINAL-AUDIT (4 fixes, 1 runtime crash).
#           (1) CRASH: round_robin_by_year() passed None-year keys to sorted(),
#               which raises TypeError in Python 3 (None < int). EC-P8 documents
#               year-extraction failure as valid, but the function didn't handle it.
#               FIX: filter None-year files into a separate tail group appended
#               after all year-keyed rounds, so sorted() never sees None.
#           (2) OPT_PATTERNS drift: PYQAnalyse patterns lacked the (.+) suffix
#               that Step 5's E-3 patterns have. Without (.+), a bare "1. " (no
#               content after label) matched as an option in PYQAnalyse but not in
#               Step 5. FIX: aligned patterns to include (.+), making is_option()
#               behaviour byte-identical to Step 5's.
#           (3) S2-2 exam_config field spec said "q_range_start, q_range_end" (two
#               separate fields), but S2-5 JSON schema, PYQSort code, and Blueprint
#               all use "q_range: [start, end]" (one array field). FIX: S2-2 aligned
#               to the array format that every consumer actually reads.
#           (4) v1.2 changelog entry (8) was a ghost fix — claimed "Pipeline diagram
#               line 15 corrected" but no change was needed or applied (line 16
#               "Steps 7–11" was already correct since MockBlueprint appears
#               separately on line 15). Removed the ghost entry.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (7 fixes, 1 critical runtime bug).
#           (1) CRITICAL: check_convergence() had `all_years = set()` — always
#               empty, so min_year_coverage was ALWAYS False and convergence
#               could NEVER be reached. FIX: accept `all_years` as a parameter
#               from the caller (derived from the full paper queue).
#           (2) Four "Step 1" references corrected to "Step 6" (MockBlueprint).
#               Step 1 = PYQ Prepare; BV-0A, ZP rotation, recency weighting
#               are Step 6 concepts. Lines: header L56, EC-P1 L1032, EC-P14
#               L1103, EC-P16 L1116.
#           (3) EC-P14 title still said "STEP 0" — missed by v1.1 audit. Fixed
#               to "Step 5" (PYQExtract).
#           (4) is_taxonomy_heading() DRIFT from Step 5's version: PYQAnalyse
#               used `re.match(r'^[1-5]\.\s')` for option filtering, but Step 5
#               uses `is_option()` matching 5 patterns (1./A./(1)/(A)/A)). Fixed:
#               aligned to full OPT_PATTERNS for contract compliance.
#           (5) Shift-tag regex aligned: `\d{1,2}` (PYQAnalyse) vs `\d{2}`
#               (Step 5). Standardised both-safe `\d{1,2}` and documented.
#           (6) Two stale "TestSeriesSort" references updated to "PYQSort"
#               (line 445 OMML reference, line 1048 EC-P4 passage reference).
#           (7) Missing function stubs added: save_scan_progress(), scan_paper(),
#               add_to_taxonomy() were called but never defined.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (3 fixes, 0 runtime bugs).
#           (1) 15 "Step 0" references corrected to "Step 5" (PYQExtract). The heading
#               format contract, parser comments, name consistency chain, edge cases,
#               and DoD all referenced "Step 0" — the old internal name for PYQExtract,
#               whose canonical pipeline position is Step 5. No code logic changed.
#           (2) S1-1 trigger parsing said "--draft mode" for PYQDraft; the spec's own
#               mode definitions (header, §2, §3) all use "--taxonomy". FIXED: consistent.
#           (3) counts_by_year tuple-key restoration: load_scan_progress had a comment
#               "Restore tuple keys from string representation" but NO restoration code
#               — the keys stayed as Python repr strings, so Counter lookups with actual
#               tuple keys would miss. Added load_count_progress() with ast.literal_eval
#               restoration. Also: last_updated timestamp was init'd to None but never set
#               during the scan loop — added datetime.now(UTC) before save_scan_progress.
#   v1.0 — Initial release. 4-mode architecture (taxonomy/scan/approve/counts).
#          Smart scan with convergence. Heading format contract with Step 5.
#          16 edge cases documented. Validated against SSC CGL Tier 1 + Tier 2.

