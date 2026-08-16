# Framework_NotesBlueprint v3.1.1 — Notes Pipeline Step NB (Ingest Base + Blueprint + Bank)
# v3.1.1 — 2026-08-14 — TAG SWEEP + PARTNER RESOLUTION + ORPHANED-FILING
#   (independent fresh-eyes review + 400-trial property fuzz; pairs with
#   notes_core v2.9, Framework_NotesCreate v2.6.2, Framework_NotesAudit
#   v3.4.2). Three fixes: (1) v3.1.0 claimed tags "enter naturally at the
#   next §7 refresh" — false for UNCHANGED papers, which §7's no-op merge
#   never re-reads: one tagged new paper made the contract live bank-wide
#   while legacy fused questions could never gain tags. §7 gains the TAG
#   SWEEP: once the bank is live (or on operator request), an NB re-run
#   MAY review untagged questions of papers already in the bank and add
#   integration_partners in place — an additive edit to NB's OWN artifact,
#   every added tag listed in the chat summary, bank_ref re-emitted after
#   the write so every downstream staleness link stays correct. Until a
#   question is tagged it simply stays in its header unit's certification
#   set (the pre-feature boundary) — safe, but taught without its bridge;
#   the sweep is how the feature reaches old evidence. The ingest report
#   now counts tags ("integration tags: N questions / M papers") so a
#   half-tagged bank is visible, never silent. (2) §3B B-1: partners
#   SHOULD resolve to manifest subtopics; notes_core v2.9 files a fused
#   question AWAY from its header ONLY when every fusion-set member
#   resolves to a registry unit — a typo'd or excluded partner keeps the
#   question at its header and surfaces as a downstream unresolved
#   advisory whose FIX IS HERE (correct the tag on the next NB run).
#   (3) §7 ORPHANED report extended: fused questions whose FILING home is
#   an orphaned sid are listed by bank_id — a deferred question must never
#   silently lose its certification home (NA §2 discloses the same from
#   its side). Companions: notes_core >= v2.9.
# [ExamCode] project | Notes Step NB | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py >= v2.9 — fully-resolved filing + unresolved reporting
#                           (v2.9; the §7 TAG SWEEP / ORPHANED-FILING side);
#                           notes-pyq-bank/1.2: bank_add_question accepts and
#                           validates the optional integration_partners field
#                           (§3B B-1); integration_target_for is the
#                           downstream filing authority. Additive — a 1.0/1.1
#                           bank still loads and migrates. Also (v2.4):
#                           registry_init EMITS notes-registry/2.1 (additive:
#                           adds draft_ref / final_ref / audit_summary per
#                           unit). NB creates the registry, so it must be the
#                           version that writes the 2.1 shape; a 2.0 registry
#                           would reach NC without the fields section 9A sets.
#                           notes-blueprint/2.0 is UNCHANGED. Also:
#   notes_core.py      >= v2.0 — load_subtopic_manifest, taxonomy_ref_for /
#                                verify_taxonomy_ref, assign_numbering,
#                                resolve_unit, sid_slug, sid-keyed registry
#                                (notes-registry/2.0, notes-blueprint/2.0); plus
#                                PYQ_BANK_SCHEMA, bank_*() builders/validators,
#                                subtopic_key, derive_taxonomy_counts,
#                                parse_exam_date_from_filename, normalize_answer,
#                                nat_precision_from_stem/nat_within_tolerance,
#                                msq_match, verify_bank_ref, registry/gates.
#   notes_blueprint.py >= v2.1 — build_blueprint_v2 (manifest consumer),
#                                verify_manifest (reproducible §1A preflight),
#                                assemble_bank, write_bank, counts_from_bank,
#                                bank_ref_for, registry writer (taxonomy_ref).
#   corpus_io.py       >= v1.11 — Drive enumerate/download/decode/verify, image
#                                extract + map_images_to_questions + vision queue.
#   blueprint_core.py  (repo, bootstrap-verified) — DRIVE_CAP, screen_drive_entry,
#                                canonical_paper_key, transport partitioning.
#
# PURPOSE:
#   (a) Ingest the ENTIRE sorted-PYQ corpus once and build notes_pyq_bank.json.
#   (b) Build notes_blueprint.json (unit list with role tags + depth tiers) using
#       counts derived from the bank.
#   (c) Initialise notes_registry.json (every unit -> BLUEPRINTED).
#   This is the ONLY step that reads syllabus, Exam Pattern xlsx and the sorted
#   papers directly. Every later step consumes the bank + blueprint.
#
# PIPELINE POSITION (Notes pipeline — independent of the Mock pipeline):
#   Notes Step NB (NotesBlueprint) -> THIS SPEC (bank + blueprint + registry)
#   Notes Step NC (NotesCreate)    -> 1 subtopic -> 1 notes .docx (draft), reads bank
#   Notes Step NA (NotesAudit)     -> ground-truth solvability audit; from
#                                     Framework_NotesAudit v3.0.0 NA also
#                                     CORRECTS and REBUILDS the notes and emits
#                                     the unit's _Final.docx. Reads the bank;
#                                     never writes it (NA section 3A)
#   Notes Step ND (NotesDeliver)   -> portal formatting + registry DELIVERED
#
# PREREQUISITE:
#   [ExamCode] project Files MUST contain: (a) [ExamCode]_subtopic_manifest.json —
#   the Step-5 (PYQExtract) deliverable; missing = HARD STOP naming the file.
#   Step 5 MUST therefore have run for this exam BEFORE any Notes step — that
#   ordering IS the single-vocabulary architecture (v3.0.1 note 3). An exam that
#   ran Notes before Step 5 completes Step 5 first, then follows MIGRATION
#   (after §7). (The manifest's human view [ExamCode]_taxonomy.xlsx is the
#   operator's picking list and is NOT read by NB.) (b) official syllabus (pdf/docx, ANY official layout;
#   §2 parsing), (c) Exam Pattern xlsx (Overview / Sections / Range tabs;
#   Overview MUST carry a Level field). Sorted PYQ papers are located via §3 and
#   ingested via §3A. A PYQ Analysis doc is OPTIONAL (cross-check only).
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_NotesBlueprint.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

## §1 — SCOPE RULES (locked)
1. CURRENT syllabus is the MASTER FILTER. Out-of-syllabus PYQ subtopics are
   excluded and listed in the blueprint's exclusion report.
2. EVIDENCE EXPANSION (Option B): a bank subtopic absent from the syllabus is
   folded in with role EVIDENCE_ADDED iff it has >= 2 PYQs within the LATEST 3
   exam years (recent3_count, derived from the bank). Otherwise excluded (reported).
3. The Subject->Topic->Subtopic header stamped on each question IN THE SORTED
   PAPER is AUTHORITATIVE. NB never reclassifies a question. subtopic identity is
   canonicalised via notes_core.subtopic_key — which reuses syllabus_provenance.norm
   (NFKC, dash unification, & -> and, '/' as data, spaces-around-'/' collapsed) so
   bank counts and blueprint units join on the same key even when the syllabus and
   the paper header differ only in punctuation or unicode. Since v3.0.0 this norm
   join is a SAFETY NET, not a load-bearing joint: unit names ARE the manifest
   names, which are the same taxonomy PYQSort stamped the headers from, so exact
   agreement is the expectation and any residual drift is REPORTED (§7 BANK-MATCH).

## §1A — TAXONOMY CONSUMER CONTRACT (v3.0.0; mirrors Framework_Blueprint
##        RULES 1/2/2a — Step 5 is the single source of truth; Step 5 UNTOUCHED)
A-1 READ THE MANIFEST. NB MUST notes_core.load_subtopic_manifest(
    "[ExamCode]_subtopic_manifest.json", exam_code) at session start. The loader
    HARD-STOPS on a structurally invalid manifest and on an exam_code mismatch
    (the wrong exam's manifest in Files is never consumed silently). NB then
    runs the PREFLIGHT notes_blueprint.verify_manifest(path, exam_code) and
    includes its report line in the chat summary; a FAIL verdict is a HARD STOP
    naming the failing check (reproducible by the owner:
    `python3 notes_blueprint.py --verify-manifest <path> [exam_code]`). Every unit
    NB places into the blueprint carries the manifest sid (Sub Topic Id)
    VERBATIM plus the manifest's display_name / section / topic EXACT BYTES.
A-2 RESOLVE, NEVER MINT. The syllabus scope-match (§2 S-1) resolves each
    manifest subtopic IN or OUT of syllabus; the bank's subtopics resolve to
    manifest triples by construction (§1.3). Any subtopic that cannot resolve to
    a manifest sid — from the syllabus, the bank, or ANY path including
    evidence-added — is a HARD STOP: "re-run Step 5 (PYQExtract) so the manifest
    includes it, then re-run NB." There is NO code path that creates a unit
    without a manifest sid (notes_blueprint.build_blueprint_v2 enforces this).
    SPECIFICALLY BANNED, exactly as in the Mock pipeline: sequential/self-minted
    ids, display-name-derived ids, and any fallback id of any shape.
A-3 DERIVED NUMBERING, PERSISTED. The numeric unit_code is a PRESENTATION
    attribute: numbers derive from manifest row order
    (notes_core.assign_numbering) and are FORMATTED by notes_core.unit_code —
    the single authority for the {EXAM}_S{s}_T{t}_ST{nn} pattern
    (spec-lock-pinned). Once assigned it is persisted in
    the registry and NEVER changes for that sid — a Step-5 re-run that inserts
    or reorders subtopics appends numbers for new sids only. Identity is the
    sid; the number is for the B1 title, F-1 filename and human reading.
A-4 STALENESS LINK. taxonomy_ref = notes_core.taxonomy_ref_for(manifest_path)
    is emitted into blueprint + registry beside bank_ref. Any later manifest
    change is detectable (notes_core.verify_taxonomy_ref; NC §1.2 checks it;
    §7 flips units STALE).

## §2 — INPUT PARSING (syllabus + pattern; Claude-driven per S-1/S-2)
S-1 Syllabus: accept pdf or docx in any official layout. Its role is SCOPE
    MATCHING ONLY (v3.0.0) — the manifest owns names and identity (§1A). Claude
    extracts the syllabus's Subject->Topic->Subtopic rows and norm-matches each
    manifest subtopic against them (syllabus_provenance.norm per component,
    full-tuple first, then name-within-matching-parents) to decide IN or OUT of
    syllabus. Where a syllabus lists prose topics with no explicit subtopics,
    every manifest subtopic under the matched topic is IN (provenance stays
    "syllabus"). The chat summary carries a SYLLABUS-MATCH report: every
    manifest subtopic that failed to match any syllabus row (these face the
    Option-B test as out-of-syllabus) AND every syllabus row that matched no
    manifest subtopic (these are A-2 HARD-STOP candidates for the owner: the
    manifest must be the superset — the fix is a Step-5 re-run, never a
    Notes-side mint).
S-2 Exam Pattern xlsx via notes_blueprint.read_exam_pattern: Overview (Total
    Questions, Types, Marks, Duration, Level), Sections and Range. Level drives
    depth calibration (§5). Missing Level = HARD STOP. allowed_question_types is
    the ordered unique set from the Range tab via extract_allowed_types (HARD STOP
    if empty); it is cross-checked against the types actually present in the bank
    and any type in the bank but absent from the Range set is reported, not dropped.
S-3 PYQ Analysis doc is NO LONGER required (owner decision 5i). Counts come from
    the bank (§3B). If an Analysis doc IS present in Files, NB runs an OPTIONAL
    cross-check (bank-derived subtopic counts vs the doc) and reports any
    divergence in the chat summary; a divergence never blocks the run and the
    bank is authoritative.
S-4 syllabus_sha256 over the raw syllabus bytes AND taxonomy_ref over the
    manifest bytes (§1A A-4) are written to the registry. A later change to
    EITHER hash marks all units STALE for incremental re-run (§7).

## §3 — SORTED-PYQ SOURCE RESOLUTION (SourceMap, folded in)
Priority order (notes_blueprint.resolve_sources):
  1. A Drive folder link given in the triggering chat message (chat wins).
  2. A Sources tab in the Exam Pattern xlsx (columns: label, url).
  3. Sorted PYQ .docx files present directly in project Files.
The resolved source list is written into notes_blueprint.json.sources.

## §3A — CORPUS INGEST (eager; corpus_io; owner decisions 1 & 6)
This is the same proven engine PYQExtract runs. Drive MCP calls are CLASS T
(Claude runs them in its own turn) and are injected into corpus_io as resolvers.
  A-0 RESUME LOAD. before enumerating, look for notes_pyq_bank.json in project
      Files (a prior run's checkpoint the operator re-uploaded, A-7 option B). If
      present, notes_core.bank_load it and treat every paper_key in its papers[]
      as DONE — those papers are skipped in A-3..A-6 and never re-downloaded. If
      absent, start a fresh bank (notes_core.bank_new).
  A-1 ENUMERATE (CLASS T bridge). resolve the folder id
      (corpus_io.parse_drive_folder_id). collect_corpus_files paginates a folder
      to exhaustion and recurses into sub-folders, so each listing call's
      page_token and each sub-folder id are known only from the PREVIOUS result —
      they cannot be pre-materialised in a single shot the way downloads can.
      Claude therefore performs the Google Drive:search_files walk IN ITS OWN
      TURN, iteratively: list the root, follow nextPageToken to the end, descend
      into every sub-folder discovered, until nothing remains, accumulating a map
      keyed by (folder_id, page_token) -> raw listing response. ONLY THEN is
      collect_corpus_files driven, with a list_fn that is a PLAIN LOOKUP over that
      already-materialised map — e.g. `list_fn = lambda fid, page_token=None:
      listings[(fid, page_token)]`. NEVER pass the Google Drive:search_files
      marker itself: that is precisely the CLASS T defect the
      Framework_MockTestAnalyse CLASS T bridge documents, and audit_callgraph C6
      fails the build on a call site that consumes a CLASS T stub's return value.
      Each entry is screened by blueprint_core.screen_drive_entry (native Google
      Doc / legacy .doc / non-.docx REJECTED with a fix message); a duplicate
      paper key (canonical_paper_key) raises DuplicatePaperError naming both files.
  A-2 PARTITION BY TRANSPORT. blueprint_core.partition_by_transport splits papers
      by DRIVE_CAP (10 MB): at-or-under-cap -> Drive lane; over-cap -> upload lane
      (chat upload / GitHub). Owner note: papers are < 10 MB, so the Drive lane is
      the norm; the upload lane remains available and is never an error.
  A-3 BATCH-OF-3 DOWNLOAD (CLASS T bridge). process papers in batches of 3. In
      Claude's OWN turn, call Google Drive:download_file_content for each paper of
      the batch and note where each result landed (inline payload or spill-file
      path), building drive_payloads = {file_id: payload_or_spill_path}. Then pass
      corpus_io.fetch_drive_docx a RESOLVER that is a plain lookup over that map
      (`resolver = lambda fid: drive_payloads[fid]`) — never the
      download_file_content marker. fetch_drive_docx -> decode_drive_payload
      (unwraps the spill-file/JSON/base64 envelope) -> verify_downloaded_bytes
      (PK magic + EXACT size match; a truncated download raises TransportFallback).
      A missing entry / TransportFallback routes THAT paper to the upload lane; it
      never aborts the batch (owner decision 6).
  A-4 IMAGE READ (per paper). corpus_io.extract_images + map_images_to_questions
      (body.iter(), so images in tables / VML <v:imagedata> / option grids are
      seen; pre-Q.1 images bucket to PREAMBLE, never dropped). verify_images runs
      the IMG gates and REPORTS findings (they do not hard-stop). Build the vision
      queue (corpus_io.build_vision_queue, 6/sheet) and READ each sheet — this is
      spec-sanctioned in-protocol vision (§8.3), not "working from memory".
  A-5 PER-QUESTION RECORD. anchor questions with the corpus_io Q pattern
      (^\s*Q\.?\s*(\d+); handles "Q.1" and "Q 1", full-number capture). For each
      question read from the paper build a bank record (§3B fields).
  A-6 CHECKPOINT. after every batch of 3, write the partial bank with
      notes_blueprint.write_bank(bank, "/mnt/user-data/outputs") (append-only) and
      present_files it, so notes_pyq_bank.json is DOWNLOADABLE (write_bank targets
      a directory; without present_files the operator cannot reach it for a
      fresh-chat resume). This is the resume artifact referenced by A-0 and A-7.
  A-7 BATCH STOP (mirrors PYQExtract / Framework_MockTestAnalyse; NON-NEGOTIABLE).
      BATCH_SIZE = 3 is fixed. Processing more than 3 papers without pausing for
      user confirmation is STRICTLY PROHIBITED; analysing the whole folder in one
      go is STRICTLY PROHIBITED; no user instruction, efficiency argument, or time
      pressure overrides this. After each batch of 3 (A-3..A-6):
        (i)   present_files the batch checkpoint (notes_pyq_bank.json) so it is
              downloadable, then emit that batch's mini INGEST REPORT — papers
              ingested (Drive vs upload lane), questions banked + per-type split,
              integration tags added this batch (bank_id + partners; v3.1.1),
              images read, any IMG-gate finding, any UNRESOLVED stem figure, any
              undated filename;
        (ii)  RENDER THE DELIVERY FOOTER as the LAST element of the response —
              the present_files call in (i) obligates it (Framework_DeliveryFooter
              §4-0 R1; §3 NB entry). For a non-final batch use F1 (amber, §4-2)
              with the 12-cell BATCH bar "batch X of Y": the template's 'continue'
              callout IS resume option A (reply 'continue' — the bank is still in
              the working dir); the SESSION-BREAK variant IS resume option B
              (download the presented bank, re-upload to [ExamCode] project
              knowledge, open a fresh chat, re-trigger NotesBlueprint — A-0
              resumes from the paper_keys already in the bank, re-downloading
              nothing);
        (iii) END THE RESPONSE — nothing after the footer, and start no new batch
              in the same turn. The A-6 checkpoint makes the pause safe; the
              Python loop boundary alone does NOT stop generation — this prose
              rule does (same class of rule as the Framework_MockTestAnalyse BATCH
              STOP law, added there after a run auto-advanced batch 1 -> batch 2 in
              one response because no END-THE-RESPONSE rule existed).
      After the LAST batch: run the corpus-level work (§3B counts, roles/tiers),
      write blueprint + registry, present_files the final set (notes_pyq_bank.json
      + notes_blueprint.json + notes_registry.json), and render F2 (green, §4-1)
      with the 4-cell NOTES pipeline bar "1 of 4" (header "Step NB · NotesBlueprint")
      and Next: NC — NotesCreate. That final F2 is the ONLY F2 in NB; every earlier
      batch stop is F1. Until the last batch, only the incremental bank (O-1) exists.

## §3B — BANK BUILD, FIGURE SPLIT, ANSWER CAPTURE, COUNT DERIVATION
B-1 PER-QUESTION FIELDS (notes_core.bank_add_question):
      bank_id (stable: "<paper_key>-Q<qno>"), paper_key, exam_date, exam_year,
      q_no, type (the doc's "Question Type:" label, canonicalised to MCQ/MSQ/NAT),
      complexity (the doc's "Complexity:" value; stored, informs §5 register),
      subject/topic/subtopic (the per-question header, authoritative),
      stem (full text WITH its OMML math preserved), options (MCQ/MSQ; empty for NAT),
      correct_answer, explanation, stem_figures, solution_figures, concept_tags,
      and (v3.1.0, OPTIONAL) integration_partners — when solving the question
      genuinely REQUIRES another subtopic's content (not merely mentions its
      vocabulary), Claude-as-SME lists that OTHER subtopic in the canonical
      Subject::Topic::Sub Topic Name scope form; typically 1-2 partners, only
      where the fusion is real. The header subtopic remains AUTHORITATIVE and
      is never a partner (bank_add_question raises on the own subtopic and on
      any non-scope-form entry). The field is EVIDENCE about the question —
      never a re-filing of it (§1.3 stands: NB never reclassifies). WHERE the
      fusion is taught is decided downstream by
      notes_core.integration_target_for (latest-partner filing over the
      persisted teaching order; NC §4 B4a authors to it, NA G-13 gates it) —
      NB only records what it sees. A bank with no integration_partners
      anywhere (pre-1.2) leaves the downstream contract DORMANT
      (grandfathered); tags enter via NEW/CHANGED papers and via the §7 TAG
      SWEEP (v3.1.1) — an unchanged paper's questions gain tags ONLY through
      the sweep, never silently. RESOLUTION (v3.1.1): every partner SHOULD
      name a manifest subtopic; the scope-form check here is syntactic only,
      and notes_core v2.9 moves a fused question off its header ONLY when
      every fusion-set member resolves to a registry unit — a typo'd or
      excluded partner keeps the question at its header, surfaces downstream
      as an unresolved advisory (NA §5 G-13 / §9), and is FIXED HERE by
      correcting the tag on the next NB run.
B-2 EXAM DATE (owner decision 2/3): notes_core.parse_exam_date_from_filename on
      the paper filename supplies exam_date + exam_year for every question in that
      paper. A filename with no parseable date is REPORTED (that paper's questions
      cannot join the recent-3 window) and the operator is asked to rename it to the
      canonical "..._DD-Mon-YYYY_..." form; the run still ingests it (year unknown).
B-3 ANSWER (owner decision 4, read verbatim, never re-derived):
      correct_answer is normalise per type (notes_core.normalize_answer): MCQ ->
      option token ("2"); MSQ -> sorted int set ([1, 3]); NAT -> float. The doc's
      value is authoritative; NB does not recompute it.
B-4 EXPLANATION: the doc's explanation (e.g. the 4-block AXIOM/DEDUCTION/SPEED
      HACK/WHY WRONG) is stored VERBATIM in the bank (internal only). It is used by
      NA as ground truth and by NC as SME grounding, and is NEVER reproduced in a
      delivered notes document (NC §3 paraphrase rule is unchanged).
B-5 FIGURE SPLIT (owner decision 3): within a question, images positioned BEFORE
      the "Correct Answer:" line are stem_figures (solve-critical); images AFTER it
      are solution_figures (part of the key). Only stem_figures set the FIGURE
      dependency NC/NA care about. A stem figure whose media did not resolve is
      recorded as "UNRESOLVED:<rId>" (rare; NA parks it, never hard-stops — §6/§9).
B-6 COUNTS (owner decision 5i): notes_blueprint.counts_from_bank ->
      notes_core.derive_taxonomy_counts yields, per subtopic_key, pyq_count and
      recent3_count (top-3 distinct exam years in the corpus) and per_year. These
      feed the blueprint's unit pyq_count and the Option-B recent3_count. The bank
      is the single source of truth for weighting.
B-7 VALIDATE: notes_core.bank_validate before the bank is written final —
      duplicate bank_id or non-canonical type raises; a corrupt bank never reaches
      NC/NA.

## §4 — ROLE TAGS (locked vocabulary)
  PYQ_WEIGHTED   — in-syllabus, pyq_count >= 3.
  BRIDGE         — prerequisite unit; full notes even at 0 PYQs. Declared by the
                   blueprint author (Claude-as-SME) with a one-line justification.
  EVIDENCE_ADDED — folded in via §1.2 (recent3_count >= 2).
  COVERAGE       — in-syllabus, pyq_count 0-2, not BRIDGE; leaner treatment.
Role assignment is notes_core.assign_role; tiers notes_core.assign_tier.

## §5 — DEPTH TIERS
  TIER-1: PYQ_WEIGHTED with pyq_count >= 15 ......... full anatomy, 6-15 pp.
  TIER-2: PYQ_WEIGHTED 3-14, or EVIDENCE_ADDED ...... full anatomy, 4-8 pp.
  TIER-3: BRIDGE or COVERAGE ........................ blocks 1-4 + 8-10, 2-5 pp.
Level (from S-2) calibrates register and assumed prerequisites within a tier; it
never changes the tier boundaries. Complexity (B-1) may nuance the register but
never the tier.

## §6 — OUTPUTS
O-1 notes_pyq_bank.json — schema notes_core.PYQ_BANK_SCHEMA (notes-pyq-bank/1.2
    as of notes_core v2.7 — additive: 1.2 adds the optional per-question
    integration_partners field of §3B B-1; a 1.0 or 1.1 bank still loads and
    migrates). The full corpus: papers[] (with per-paper
    image_report) and questions[] (§3B fields). The stored subtopic_key is
    informational only — NC/NA and count derivation RECOMPUTE it from each
    question's subject/topic/subtopic, so a bank written by an older notes_core
    still joins correctly. This is a project artifact, not a framework file; NC and
    NA read it read-only.
O-2 notes_blueprint.json — notes_core.BLUEPRINT_SCHEMA (notes-blueprint/2.0;
    1.x still loads read-only); exam_code, level, allowed_question_types,
    sources, bank_ref AND taxonomy_ref. bank_ref is EMITTED by building the
    blueprint with bank_ref=notes_blueprint.bank_ref_for(bank_path) AFTER the
    bank is written — {path, sha256, questions, generated} over the bank bytes on
    disk — so any later change to notes_pyq_bank.json is detectable
    (notes_core.verify_bank_ref; read by NC §1.2). taxonomy_ref is the same idiom
    over the manifest (§1A A-4; notes_core.verify_taxonomy_ref). Built via
    notes_blueprint.build_blueprint_v2. Also the exclusion report (each row with
    its sid + manifest names) and the full unit table: sid, unit_code, name
    (manifest display_name verbatim), section, topic, slug (notes_core.sid_slug),
    role, pyq_count, tier, provenance, seq_in_topic, optional
    prose_ban_exemptions. Unit provenance is "syllabus" or "evidence-added";
    pyq_count is DERIVED from the bank (§3B B-6), not carried on a provenance
    field.
O-3 notes_registry.json — notes_core.registry_init (notes-registry/2.1 as of
    notes_core v2.4 — the 2.0 keys are unchanged and 2.0/1.x still load; 2.1
    adds the per-unit draft_ref / final_ref / audit_summary that NC section 9A
    and NA section 6 populate downstream; units
    KEYED BY sid; taxonomy_ref stored); every unit -> BLUEPRINTED.
O-4 Chat summary — the INGEST REPORT is emitted at EACH BATCH STOP (A-7) for that
    batch's 3 papers; after the LAST batch a FULL summary adds unit counts by
    role/tier + the exclusion report, plus totals: papers ingested (Drive lane vs
    upload lane), questions banked, per-type split, images read, any IMG-gate
    findings, any UNRESOLVED stem figures, any filename with no parseable date,
    and (if an Analysis doc was present) the cross-check result — PLUS (v3.0.0)
    the SYLLABUS-MATCH report (§2 S-1), the BANK-MATCH report (§7), and any
    ORPHANED units (§7). Version numbers appear in CHAT ONLY, never inside
    delivered documents.

## §7 — INCREMENTAL RE-RUNS
Unchanged syllabus_sha256 AND unchanged taxonomy_ref.sha256 AND unchanged corpus
(same paper_key set + sizes) is a no-op merge: existing unit states preserved;
genuinely new units enter BLUEPRINTED. A NEW or CHANGED paper is (re)ingested and
appended to the bank (its questions get fresh bank_ids); counts and Option-B
evidence are recomputed. A changed syllabus hash OR a changed manifest hash marks
every unit STALE=true (state preserved) and the summary lists the diff; unit
identity is the sid, so a re-run against a changed manifest PRESERVES every
existing unit's sid key, numbering (§1A A-3 — assign_numbering is fed the prior
registry's numbers) and state. New manifest sids enter BLUEPRINTED with appended
numbers. ORPHANED: a registry sid no longer present in the manifest is REPORTED
(with its state) and NEVER deleted — the owner decides; a renamed subtopic
upstream arrives as remove+add (slug-derived sids), which the report makes
visible side by side. ORPHANED-FILING (v3.1.1): the ORPHANED report also
lists, by bank_id, every fused question whose integration FILING home is an
orphaned sid — computed with the public authority, per orphaned unit:
notes_core.integration_target_for(bank, section, topic, name,
unit_order_from_registry(registry)), whose fusions[].bank_ids are exactly
the questions filed there. Those PYQs' certification home is leaving the
taxonomy, and
the owner's orphan decision must account for them (NA §2 discloses the same
pending state on every audit until it clears). TAG SWEEP (v3.1.1): once the
bank carries ANY integration_partners (live) — or whenever the operator
asks for integration tagging — an NB re-run MAY review the untagged
questions of papers ALREADY in the bank and add integration_partners where
the fusion is real (Claude-as-SME, same bar as B-1: the question genuinely
REQUIRES the partner's content). This is an additive edit to NB's own
artifact: every added tag is listed in the chat summary (bank_id +
partners), nothing else in the record changes, bank_validate re-runs, and
bank_ref is re-emitted over the new bank bytes so NC/NA staleness links
stay correct. Without the sweep an unchanged paper's questions can NEVER
gain tags (§7 re-reads only new/changed papers) — they stay safely in
their header unit's certification set, taught without their bridge. BANK-MATCH: after ingest, every bank (subject, topic,
subtopic) triple is norm-matched against the manifest triples; failures are
listed (expected ZERO — the sorted headers came from this same taxonomy; a
nonzero list exposes an upstream sorting anomaly to fix at PYQSort/Step 5, never
by a Notes-side rename). The §3A-6 checkpoint means an interrupted ingest resumes
from the last completed batch — reply 'continue' in-session, or re-trigger
NotesBlueprint in a fresh chat (A-7 option B) and it picks up the paper_keys not
yet in the bank. Nothing is deleted automatically.

## MIGRATION (v3.0.0 -> sid-keyed; one-time per pre-v3 Notes project)
A project with 1.x notes_blueprint.json / notes_registry.json is mid-pipeline on
unit_code keys. Those artifacts still LOAD read-only (sid=None), but NC/NA/ND
resolution and the taxonomy_ref check route to NB — by design. The remedy is ONE
NB re-run: the ingested bank is untouched and A-0 resumes from it (nothing is
re-downloaded), so the cost is the counts + blueprint + registry rebuild only.
STATE CARRY-OVER across the key change is explicit: for each 1.x unit, resolve
its name against the new sid-keyed units via notes_core.resolve_unit; on a
unique hit, carry state, notes_version, audit, artifacts and history onto the
sid-keyed unit (numbering comes from the new assignment — a pre-v3 unit_code was
syllabus-positional and is NOT preserved as numbering prior); an ambiguous or
failed resolution is LISTED in the chat summary for the owner to map manually —
never guessed. Delivered .docx files keep their old filenames until their unit
is next redelivered; the registry's artifacts map records both.

## §8 — HARD RULES CARRIED FROM THE FRAMEWORK CORE
1. NEVER work from memory for exam-varying values: counts, ranges, marks, Level,
   answers and figures come from the parsed inputs / ingested bank only.
2. Specs are PROJECT-FIRST; engines (incl. corpus_io, blueprint_core, notes_*) are
   REPO-ONLY (bootstrap-verified). notes_pyq_bank.json is a project artifact.
3. IN-PROTOCOL VISION IS NOT MEMORY. The §3A-4 vision read of extracted image
   sheets, and reading the sorted paper's stems / options / answers / explanations,
   ARE the executed protocol. The memory ban targets INVENTING question content or
   answer keys; it does not ban spec-sanctioned reading of the SOURCE. Answers and
   explanations are read VERBATIM and never re-derived (owner decision 4).
4. NB does not hard-stop on a per-image gate finding or an over-cap paper (owner
   decision 6): it reports and, where needed, routes the paper to the upload lane.
   The only hard stops are: missing Level (S-2), an empty allowed-type set (S-2),
   a corrupt ZIP archive (extract_images IntegrityError — nothing to read), and a
   malformed bank (bank_validate).

## §9 — EDGE CASES (must all be covered)
E-1  Native Google Doc / legacy .doc / non-.docx on Drive -> screened out at
     enumeration with a "convert to .docx" message; not ingested.
E-2  Duplicate paper (same canonical_paper_key, e.g. "Copy of ..." / "... (1)") ->
     rejected at enumeration naming both; operator removes one.
E-3  Over-cap (> 10 MB) paper -> upload lane, not an error (owner note: won't occur).
E-4  Truncated download (bytes != Drive-reported size) -> TransportFallback -> that
     paper to the upload lane; never a silent image loss.
E-5  Images in tables / option grids / VML <v:imagedata> / header-footer / pre-Q.1
     -> all handled by map_images_to_questions (body.iter + PREAMBLE bucket).
E-6  A question with BOTH a stem figure and explanation figures -> split at the
     "Correct Answer:" line (B-5); only the stem figure sets the FIGURE dependency.
E-7  NAT answer with a sign/decimal ("-8", "274.4") -> normalise to float (B-3);
     NA matches at the stem's stated rounding precision (owner decision 4b).
E-8  MSQ answer "1, 3, 4" (spaced) -> sorted int set; NA matches unordered.
E-9  Filename with no parseable date -> reported; questions ingested with unknown
     year (excluded from the recent-3 window) until the file is renamed.
E-10 Subtopic label present in the paper but absent from the syllabus -> Option-B
     evidence test (§1.2); folds in as EVIDENCE_ADDED or is excluded + reported.
E-11 A stem figure whose media rId does not resolve -> "UNRESOLVED:..."; NA parks
     the question in figure_pending, never hard-stops (owner decision 6).
E-12 An optional PYQ Analysis doc disagreeing with bank counts -> reported; the
     bank is authoritative (owner decision 5i).
E-13 Wrong exam's manifest in project Files -> load_subtopic_manifest exam_code
     HARD STOP before any work (§1A A-1).
E-14 Syllabus subtopic with no manifest match -> SYLLABUS-MATCH report + A-2
     HARD-STOP path: re-run Step 5 so the manifest (the superset) includes it.
     NB never mints an id for it.
E-15 Manifest subtopic removed by a Step-5 re-run while its unit is DRAFTED/
     DELIVERED -> ORPHANED report (§7), state + numbering preserved, nothing
     deleted; the owner decides.
E-16 Two subtopics with the SAME display name under different topics -> distinct
     sids (full-tuple identity); the bare-name operator path returns both as
     'ambiguous' for the operator to choose (notes_core.resolve_unit — Framework_NotesCreate section 0);
     the scope form Subject::Topic::Sub Topic Name resolves uniquely.

---

# END OF Framework_NotesBlueprint v3.1.1
