# Framework_NotesBlueprint v2.0.5 — Notes Pipeline Step NB (Ingest Base + Blueprint + Bank)
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
# [ExamCode] project | Notes Step NB | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py      >= v1.8 — PYQ_BANK_SCHEMA, bank_*() builders/validators,
#                                subtopic_key, derive_taxonomy_counts,
#                                parse_exam_date_from_filename, normalize_answer,
#                                nat_precision_from_stem/nat_within_tolerance,
#                                msq_match, verify_bank_ref, plus registry/gates.
#   notes_blueprint.py >= v1.4 — assemble_bank, write_bank, counts_from_bank,
#                                bank_ref_for, blueprint writer (bank_ref emitted).
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
#   Notes Step NA (NotesAudit)     -> ground-truth solvability audit + loop, reads bank
#   Notes Step ND (NotesDeliver)   -> delivery + registry DELIVERED
#
# PREREQUISITE:
#   [ExamCode] project Files MUST contain: (a) official syllabus (pdf/docx, ANY
#   official layout; §2 parsing), (b) Exam Pattern xlsx (Overview / Sections /
#   Range tabs; Overview MUST carry a Level field). Sorted PYQ papers are located
#   via §3 and ingested via §3A. A PYQ Analysis doc is OPTIONAL (cross-check only).

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
   the paper header differ only in punctuation or unicode.

## §2 — INPUT PARSING (syllabus + pattern; Claude-driven per S-1/S-2)
S-1 Syllabus: accept pdf or docx in any official layout. Extract the
    Subject->Topic->Subtopic hierarchy; where a syllabus lists prose topics with
    no explicit subtopics, the bank's own subtopic set for that topic is adopted
    (provenance per unit "syllabus" | "analysis-adopted" — here "bank-adopted").
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
S-4 syllabus_sha256 over the raw syllabus bytes is written to the registry. Any
    later hash change marks all units STALE for incremental re-run (§7).

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
      correct_answer, explanation, stem_figures, solution_figures, concept_tags.
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
O-1 notes_pyq_bank.json — schema notes_core.PYQ_BANK_SCHEMA (>= notes-pyq-bank/1.1;
    a 1.0 bank still loads and migrates). The full corpus: papers[] (with per-paper
    image_report) and questions[] (§3B fields). The stored subtopic_key is
    informational only — NC/NA and count derivation RECOMPUTE it from each
    question's subject/topic/subtopic, so a bank written by an older notes_core
    still joins correctly. This is a project artifact, not a framework file; NC and
    NA read it read-only.
O-2 notes_blueprint.json — notes_core.BLUEPRINT_SCHEMA (>= notes-blueprint/1.2);
    exam_code, level, allowed_question_types, sources, and bank_ref. bank_ref is
    EMITTED by building the blueprint with
    bank_ref=notes_blueprint.bank_ref_for(bank_path) AFTER the bank is written —
    {path, sha256, questions, generated} over the bank bytes on disk — so any
    later change to notes_pyq_bank.json is detectable (notes_core.verify_bank_ref;
    read by NC §1.2). Also the exclusion report and the full unit table
    (unit_code, names, role, pyq_count, tier, provenance, seq_in_topic, optional
    prose_ban_exemptions). Unit provenance is "syllabus" or "evidence-added" (the
    values build_blueprint writes); pyq_count is DERIVED from the bank (§3B B-6),
    not carried on a provenance field.
O-3 notes_registry.json — notes_core.registry_init; every unit -> BLUEPRINTED.
O-4 Chat summary — the INGEST REPORT is emitted at EACH BATCH STOP (A-7) for that
    batch's 3 papers; after the LAST batch a FULL summary adds unit counts by
    role/tier + the exclusion report, plus totals: papers ingested (Drive lane vs
    upload lane), questions banked, per-type split, images read, any IMG-gate
    findings, any UNRESOLVED stem figures, any filename with no parseable date,
    and (if an Analysis doc was present) the cross-check result. Version numbers
    appear in CHAT ONLY, never inside delivered documents.

## §7 — INCREMENTAL RE-RUNS
Unchanged syllabus_sha256 AND unchanged corpus (same paper_key set + sizes) is a
no-op merge: existing unit states preserved; genuinely new units enter BLUEPRINTED.
A NEW or CHANGED paper is (re)ingested and appended to the bank (its questions get
fresh bank_ids); counts and Option-B evidence are recomputed. A changed syllabus
hash marks every unit STALE=true (state preserved) and the summary lists the diff.
The §3A-6 checkpoint means an interrupted ingest resumes from the last completed
batch — reply 'continue' in-session, or re-trigger NotesBlueprint in a fresh chat
(A-7 option B) and it picks up the paper_keys not yet in the bank. Nothing is
deleted automatically.

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

---

# END OF Framework_NotesBlueprint v2.0.5
