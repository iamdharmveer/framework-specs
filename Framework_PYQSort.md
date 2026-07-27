# Framework_PYQSort v1.18 — Universal PYQ Sorter
# [ExamCode] project | Step 3 (PYQSort) | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS (v1.14):
#   corpus_io.py          >= v1.4   — load_taxonomy() is S1-0b/S1-2's ONLY entry
#                                     point: source selection, read and identity
#                                     assertion in one call
#   (superseded note) v1.3  — Cluster K read_analysis_doc() is S1-2's ONLY
#                                     reader, assert_taxonomy_lock() is S1-0b's ONLY
#                                     comparison, and v1.2 INGEST FORMS are what make
#                                     the project-Files copy readable at all
#   (superseded note) v1.1  — Cluster K read_analysis_doc() is S1-2's ONLY
#                                     reader. Under v1.0.x this spec does not run.
#   reconcile_taxonomy.py >= v1.2   — S1-0b compares taxonomy_fingerprint, which the
#                                     record only carries from schema 1.2 onward. An
#                                     older record HARD STOPS with a named message.
#   blueprint_core.py     — parse_taxonomy_level / MAX_HEADING_LEN / taxonomy_fingerprint
#
# PURPOSE:
#   Take one Row file (.docx, output of Step 1 PYQ Prepare) and re-sort every
#   question into a new .docx grouped hierarchically by Subject → Topic →
#   Subtopic, ordered within each subtopic by date descending, session ascending.
#   The sorted output is the input format that Step 5 (PYQExtract) expects.
#
# REPLACES:
#   TestSeriesSort Tier 1 v10 (SSC CGL Tier 1 specific)
#   TestSeriesSort Tier 2 v3  (SSC CGL Tier 2 specific)
#   This framework is exam-agnostic — same spec for ALL exams.
#
# PIPELINE POSITION:
#   Step 1 PYQ Prepare  → raw exam dump to Row file (.docx)
#   Step 2a PYQ Draft   → syllabus + taxonomy_draft.json + exam_config.json
#   Step 2b PYQ Scan    → discover subtopics from PYQ content
#   Step 2c PYQ Approve → approved Analysis docs + exam_config.json
#   Step 3 PYQ Sort     → THIS SPEC (1 Row file → 1 Sorted PYQ)
#   Step 4 PYQ Count    → fill PYQ counts in Analysis docs (Phase B of PYQAnalyse)
#   Step 5 PYQ Extract  → Sorted PYQ → section_rules.md + manifest + Frequency xlsx
#   Step 6 Mock Blueprint → Analysis docs + Frequency xlsx → blueprint.json
#   Steps 7–11          → Mock test creation pipeline
#
# PREREQUISITE:
#   1. Step 1 must have produced the Row file from raw exam dump.
#   2. Step 2c PYQApprove must have produced approved Analysis docs + exam_config.json.
#   3. Both Analysis docs and exam_config.json must be in [ExamCode] project Files.
#      Project knowledge stores the .docx as extracted TEXT under its .docx name.
#      That is SUPPORTED and EXPECTED — corpus_io >= v1.2 reads either form and
#      reports which one at S1-3. No operator action, and do NOT attach the
#      Analysis doc to chat as well: the project copy wins and the attachment is
#      silently ignored (EC-S20).
#
# INPUTS:
#   1. One Row file (.docx) — uploaded to chat
#   2. Approved Analysis docs — in project knowledge (loaded automatically)
#   3. [ExamCode]_exam_config.json — in project knowledge (loaded automatically)
#
# OUTPUT:
#   One Sorted PYQ .docx file — delivered via present_files.
#   (1 file, nothing else. Deliverable set is CLOSED — see §9 delivery contract.)
#   User downloads → uploads to Google Drive PYQ folder.
#   v1.12: the output is SIZE-GOVERNED to blueprint_core.SIZE_BUDGET (9 MiB, a 10%
#   margin under the 10 MiB Drive connector download cap) and its image count is
#   GATED against the Row file. The Sorted file is what Steps 4 and 5 fetch back out
#   of Drive, so an ungoverned Sorted file is the thing that blocks them — see S7-6.
#
#   DO NOT DELIVER:
#     ✗ sort_pipeline.py (execution script — stays in /home/claude/)
#     ✗ Any intermediate or working .docx files
#     ✗ Any JSON, .txt, or log files generated during sorting
#     ✗ Input Row file (this is an INPUT, not an output)
#
# TRIGGER FORMAT:
#   Step 3: PYQSort
#   Trigger matching is case-insensitive.
#   ExamCode read from exam_config.json in project knowledge (set during Step 2a PYQDraft).
#
# RUNS IN: [ExamCode] project (exam-specific, where Analysis docs are uploaded)
#
# EXECUTION MODEL: Single script, 4 tool calls maximum. No "Continue" needed.
#   1. create_file  → write complete sort_pipeline.py
#   2. bash_tool    → run it (parse + classify + sort + emit + validate)
#   3. bash_tool    → verify Q-count, heading counts, date-label count
#   4. present_files → deliver
#
# EXAM-AGNOSTIC GUARANTEE:
#   Zero hardcoded exam values. All section names, topic names, subtopic names,
#   subject order, section boundaries, session keyword, page size, question types
#   → read from Analysis docs + exam_config.json.
#   Same spec runs for SSC CGL (4 sections, Q-range, Shift), SSC Tier 2 (5 sections,
#   markers, Shift), GATE (1 section, no session, NAT questions), Banking (Slot),
#   UPSC (Paper), RRB (Phase), or any exam.
#
# STEP 1 FORMAT CONTRACT:
#   PYQSort assumes Row files are produced by Step 1 (PYQ Prepare) in a
#   STANDARDISED format. Step 1 is the normalisation layer — it converts
#   exam-specific raw dumps into this universal format:
#     Date labels:  [DD-Mon-YYYY <session_keyword> <N>] (with session)
#                   [DD-Mon-YYYY] (without session — single-session exams)
#                   session_keyword comes from exam_config.json
#                   Session part is OPTIONAL — Step 1 omits it when not provided
#                   Month abbreviations: always 3-char English (Jan, Feb, ...)
#     Q-numbering:  Q.<N> format (continuous or per-module)
#     Options:      one of the 5 OPT_PATTERNS formats, or none for NAT questions
#   If a Row file violates this contract, PYQSort raises a clear error pointing
#   to Step 1 as the fix location — not a PYQSort bug.
#
# VERSION HISTORY:
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
#   v1.17 — 2026-07-26 — is_option DELEGATED; IMAGE OPTIONS NO LONGER UNDERCOUNTED
#            (audit_deep [XSPEC-DRIFT]). This file carried its own is_option() whose
#            docstring claimed "Aligned with Step 5's is_option() — same 5 patterns."
#            MockTestAnalyse v2.34/v2.35 added the image-option path and this copy was
#            left behind, so the claim became false and the same defect stayed live
#            HERE. It was not cosmetic: _count_options_in_body() and the option
#            re-indent pass both use the predicate, so an IMAGE OPTION — a bare "1."
#            whose content is a picture — was neither counted nor indented. Measured
#            on IIT_JAM_BIOTECHNOLOGY 2022: 156 options counted against 160 actual.
#            corpus_io >= v1.6 now owns OPT_PATTERNS / BARE_OPT_PATTERNS /
#            para_has_image / is_option; this spec delegates. BOTH call sites now pass
#            the paragraph element — delegating without passing it compiles cleanly
#            and keeps the undercount, which is the trap in this fix.
#   v1.16 — 2026-07-26 — THE TAXONOMY IS LOADED ONCE, FROM JSON WHERE AVAILABLE.
#          reconcile_taxonomy >= v1.3 records the approved taxonomy inside
#          approval_record.json — a file the platform stores byte-for-byte — beside
#          the fingerprint that validates it. corpus_io.load_taxonomy() prefers that
#          and falls back to the Analysis doc for pre-1.3 records, so on the
#          preferred path this step reads no Word document at all and EC-S20 cannot
#          arise. Exams approved earlier are unaffected and need no re-run.
#          S1-0b and S1-2 collapse to ONE call. The pair they replace — a read
#          followed by a separate lock assertion — was written in both sections,
#          which meant the artefact was read TWICE in one step and the two reads
#          could disagree. S1-0b makes the call because it is the first consumer;
#          S1-2 reuses the object and hard stops if it is missing.
#          S1-3 reports source alongside ingest form. EC-S21 records the new path
#          and, explicitly, that a pre-1.3 record is NOT a fault. DoD 23 updated.
#   v1.15 — 2026-07-26 — INGEST FORMS SURFACED + S1-0b DELEGATED (GAP-2026-07-25-003).
#          Documentation and delegation only; no behaviour in this spec changes that
#          corpus_io >= v1.3 does not already provide.
#          (a) EC-S20 records what the runtime actually receives: the Analysis doc is
#              stored in project Files as extracted TEXT under its .docx name, and
#              that is the PRIMARY form at Steps 3-6, not a degraded one. It also
#              records the two things that are NOT tolerated — a '|' in any taxonomy
#              name, which the text form splits into a silently truncated name whose
#              declared totals still agree, and an unrecognised extraction grammar.
#          (b) S1-3 REPORTS the ingest form. Same discipline as S1-0's one line on
#              success: when the platform's grammar eventually changes, this line is
#              the first evidence of it.
#          (c) S1-0b no longer writes the fingerprint comparison itself. It was the
#              first place to make that claim and, for one release, the only one;
#              Steps 4, 5 and 6 now make it too, so the rule lives once in
#              corpus_io.assert_taxonomy_lock() and every step calls it. Four
#              transcriptions of one comparison is how GAP-2026-07-25-002's four
#              readers happened. The claim, the messages and the operator actions are
#              unchanged — only their location is.
#          (d) §13 gains the rule the whole gap reduces to: NEVER infer a container
#              format from a file extension.
#   v1.14 — 2026-07-25 — ANALYSIS-DOC READER DELEGATED + S1-0b CONTENT CROSS-CHECK
#          (GAP-2026-07-25-002). S1-2 carried its own reader and it was wrong twice over.
#          DEFECT A (loud): the discovery glob '*_PYQ_Analysis_*.docx' required a trailing
#          '_' that PYQAnalyse v2.6 removed 19 days and 7 releases ago — it matched every
#          filename the framework no longer produces and none of the one it does, so PYQSort
#          hard-stopped telling the operator to upload a file already correctly in place.
#          DEFECT B (silent, P0): a `if not section_name` latch delimited SUBJECTS BY FILE
#          BOUNDARY, which is exactly what the merge to a single doc removed. Measured on the
#          first real exam: 1 subject parsed where the doc declares 6, all 131 subtopics filed
#          under one subject, 5 topic_idx collision groups, correct totals throughout. Every
#          sorted file would have carried "Subject: General Biology" above Physics questions.
#          A was the ONLY control preventing B from shipping, and it was protecting by
#          accident: fixing the glob alone converts a loud stop into silent corpus-wide
#          corruption. They are fixed together, and by deletion rather than by repair —
#          the reader now lives in corpus_io Cluster K, the single reader/writer/verifier for
#          this artefact, with heading recognition delegated to
#          blueprint_core.parse_taxonomy_level(). Two consequences beyond the reported bug:
#          (a) all six level-1 label forms (Subject/Domain/Section/Part/Area) and all six
#          level-2 forms (Topic/Chapter/Unit/Module/Block) now work here, where the old
#          hardcoded matcher saw one of each; (b) the reader HARD STOPS when its parse
#          disagrees with the totals the document declares about itself, so a future variant
#          of B cannot be silent. NEW S1-0b closes the other half: S1-0 proved the lock was
#          earned, never that the loaded taxonomy IS the locked one — Defect B passed S1-0
#          cleanly. S1-0b compares blueprint_core.taxonomy_fingerprint() against the
#          approval record's. topic_idx becomes positional within the subject, which is what
#          §S6-2 always specified; the old label-derived form could not survive a merged doc,
#          where "Topic N:" restarts at 1 for every subject.
#   v1.13 — 2026-07-25 — S1-0 TAXONOMY LOCK VERIFICATION added (GAP-2026-07-25-001,
#          Layer 4). approval_record.json was produced at Step 2c and read by NOTHING —
#          the string did not appear in this spec or in any other downstream spec. A lock
#          nothing verifies is a receipt, and it is why a silent S4-0 check-skip could
#          travel five steps undetected. PYQSort now HARD STOPS when the record is absent,
#          when status is not CLEAN/CLEAN_ADJUDICATED, or when the record cannot prove its
#          checks ran (pre-1.1 schema, or non-empty checks.missing / checks.vacuous /
#          unmaterialisable). Re-running PYQApprove is RECONCILIATION, never re-derivation.
#   v1.12.2 — 2026-07-25 — Q_PATTERNS TABLE RECONCILED WITH THE ENGINE. The local table listed
#           five patterns while the delegated bc.detect_question_start implements two, and the
#           audit_deep TABLE-PARITY check this spec cited as its guarantee could not see the
#           difference: its extraction regex stopped at the first "]", which sits inside
#           r'^Question\s+(\d+)\s*[:.]'. The table is documentary — declared, never read — so
#           behaviour is unchanged; what changes is that the documentation no longer invites a
#           catastrophic "fix". Widening the engine to five patterns would make every option
#           line match: a 100-question paper parses as 500 (verified).
#   v1.12.1 — 2026-07-25 — MINIMUM COMPANION VERSION CORRECTED. The v1.12 entry named
#           "corpus_io v1.0" as its twin. That is wrong in a way that matters: S7-6 calls
#           assert_docx_parity with allow_resample=False for tier T1, and in corpus_io v1.0
#           that raises a FALSE IntegrityError whenever the governor renames a media part —
#           which is the ordinary path for a photographic PNG, since the jpeg route rewrites
#           image1.png as image1.jpeg. Proven by execution: identical 1400x1000 dimensions
#           before and after, corpus_io v1.0 HARD STOPs, corpus_io v1.0.1 passes. Pairing
#           v1.12 with corpus_io v1.0 therefore gives a governor that fails closed on exactly
#           the papers it exists to shrink. The minimum companion is corpus_io v1.0.1, whose
#           parity fix was found while verifying this very spec. Documentation only — not one
#           line of behaviour changes here.
#   v1.12 — 2026-07-25 — IMAGE SURVIVAL GATE + SIZE GOVERNOR ON WRITE (DEFECT J, DEFECT M).
#           Twin of Framework_MockTestAnalyse v2.29 / corpus_io v1.0.1 (see v1.12.1 — the
#           original entry said v1.0, which is the one release this spec does NOT work with).
#           Step 3 is where images
#           are RE-EMBEDDED — the riskiest image operation in the PYQ pipeline, and the one
#           §13 has warned about since v1.0 in its own words: "images silently vanish. No
#           error, just empty space." Verified by grep across all 31 tracked files: NO
#           image-count check of any kind existed in this file. Framework_PYQFormat has
#           enforced exact input==output image equality (S8-6) since v1.1 for the same class
#           of risk; the step that actually performs the risky operation had nothing.
#           (1) DEFECT J — re_embed_images() matched only <a:blip r:embed> (DrawingML).
#               Legacy VML <v:imagedata r:id> — emitted by older Word, several PDF converters
#               and pasted OLE/equation objects — was never re-pointed, so exactly the
#               failure the §13 warning describes occurred for every VML image, silently.
#               Verified: 'imagedata' appeared 0 times in this file, in
#               Framework_MockTestAnalyse.md and in Framework_PYQPrepare.md. S7-1 now
#               re-points BOTH mechanisms.
#           (2) DEFECT M — NEW S7-7 image survival gate, modelled on PYQFormat S8-6 with the
#               same exact-equality discipline (not a tolerance) and surfaced as CHECK 10.
#               Body image references in the delivered file MUST equal the `intended` count
#               from the S7-5 census. Mismatch is a HARD STOP naming the missing media parts.
#           (3) NEW S7-5 pre-flight + input image census. The pre-flight runs on the PATH
#               before python-docx opens the Row file, because a relationship pointing at a
#               missing media part makes python-docx raise a bare zipfile KeyError while
#               CONSTRUCTING the Document — any check placed after Document(path) is
#               unreachable, and the operator gets a library traceback instead of a sentence
#               naming the defect and the step that owns it. Found by adversarial test, not
#               by reading. The census then establishes the expected count before any work,
#               partitions every body child into CARRIED (a question's stem or body element)
#               and NOT CARRIED, and REPORTS the not-carried ones with their count and text
#               prefix. Images before Q.1, or inside a date-label paragraph the emitter
#               rebuilds from scratch, are correctly not carried — but dropping them SILENTLY
#               would either hide a real loss or trip the new gate for a benign reason. The
#               expected count is derived from the parse, not from a Q-number regex, so it
#               cannot disagree with what the emitter actually carries.
#           (4) NEW S7-6 size governor on write. Step 3 is the first step to hold real image
#               bytes, and its output is what Steps 4 and 5 fetch back OUT of Drive through a
#               connector that refuses downloads above 10 MiB. An ungoverned Sorted file is
#               therefore the thing that blocks Step 4/5 later, three-quarters of the way
#               through a batch run (the reported 2026-07-24 incident: 6 of 7 pending papers
#               above the cap, discovered at batch 6). The governor runs on write, under
#               corpus_io.assert_docx_parity — 17 invariants including the text SHA256, the
#               OMML count and per-image pixel dimensions, because a governor that quietly
#               dropped a figure would still produce a smaller file that opens cleanly in Word.
#           (5) Ladder floor exceeded (still over budget at T4) → DELIVER + WARN + FLAG, never
#               HALT. A legitimately huge paper must not block its own delivery; the operator
#               is told the file will need the upload lane at Step 4/5.
#           (6) Counting is DELEGATED to corpus_io.count_image_refs (Cluster I) — blip AND
#               VML, every story part, never doc.inline_shapes (which sees only inline body
#               drawings and so under-counts silently). A local re-implementation here is
#               forbidden: a count that can run low is worse than no count, because it makes
#               a broken document look verified.
#           (7) §9 write path made explicit for the first time: save → census → govern →
#               parity → CHECK 1..10 → copy to FINAL_OUT. Still 4 tool calls.
#           (8) EC-S16..EC-S19 (VML images · governor floor · non-carried images · dangling
#               relationship in the Row file).
#           ROUTING: routes.json must route corpus_io.py to PYQSort. NOT OPTIONAL — this spec
#           imports it.
#   v1.11 — 2026-07-23 — detect_question_start DELEGATED to blueprint_core (Cluster G).
#           Twin of Framework_PYQPrepare v1.8 / MockTestAnalyse v2.28. No behaviour change —
#           the engine form is byte-identical to the copy removed here.
#   v1.10 — 2026-07-23 — ANTI-DRIFT: OUT_OF_PATTERN now comes from the ENGINE
#           (blueprint_core.OUT_OF_PATTERN) instead of being declared locally. v1.9 declared
#           the literal here while Framework_PYQAnalyse RULE 4 referenced it by name under a
#           DIFFERENT trigger, with no shared definition and no route carrying one — two
#           independent copies of a single literal, which is precisely the drift the
#           framework's anti-drift principle forbids. routes.json now routes blueprint_core.py
#           to PYQSort (and to PYQDraft/PYQScan/PYQApprove/PYQCount/PYQExtract for the same
#           reason). No behavioural change: the value is identical.
#   v1.9 — 2026-07-23 — OUT-OF-PATTERN QUESTIONS NO LONGER SILENTLY LOST
#           (GAP-2026-07-23-001, PYQ-side twin of Framework_Blueprint v1.36).
#           ROOT CAUSE: exam_config describes the CURRENT exam pattern, but a PYQ corpus
#           routinely spans several patterns. get_section_by_q_range() returned None for any
#           Q-number outside every configured section range; the None was written straight
#           into the question record at S3-2, and a corpus-wide grep confirms NO guard for it
#           existed anywhere. Those questions then failed every (section, topic, subtopic)
#           lookup. On a 100-question legacy paper sorted against a 60-question current
#           config that is a silent 40% data loss on one file, with no operator-visible
#           signal of any kind. This is the same unstated assumption — "PYQ structure equals
#           current structure" — that produced the Blueprint axis-unit and coverage-gate
#           defects fixed in Framework_Blueprint v1.36.
#           (1) S2-2 get_section_by_q_range(): returns the OUT_OF_PATTERN module constant
#               instead of None. NEVER returns None. The sentinel is a fixed literal, not an
#               exam-derived string, so it cannot collide with any exam's section names.
#           (2) S3-2 extract_questions(): every question record gains pattern_era, valued
#               'current' or 'out_of_pattern'. Structural provenance only — never a content
#               judgement.
#           (3) S4-3 classify_question(): OUT_OF_PATTERN questions are classified against the
#               FULL taxonomy instead of one section's slice. This is a NARROW, SENTINEL-GATED
#               exception to RULE 4 ("section from structure, not content"): RULE 4 exists so a
#               maths question sitting in the Reasoning section stays in Reasoning, which
#               presupposes a structural section EXISTS. These have none, so RULE 4 has nothing
#               to say and applying it anyway yields an empty candidate list — exactly how the
#               questions were lost. The exception is gated on the sentinel, never on a failed
#               match, so a question that HAS a real section can never fall through to it.
#           (4) NEW report_pattern_era(): prints observed vs configured Q-count, the
#               out-of-pattern count and Q-range, and the mix consequence. Reports only —
#               never mutates, never decides, never halts. Silent when the paper matches the
#               current pattern exactly, so the 200-exam common case is unchanged.
#           (5) EC-S1b: the mirror of EC-S1 (papers LARGER than the current pattern).
#           WHAT THIS DELIBERATELY DOES NOT DO: it does not exclude out-of-pattern questions
#           from frequency. Counts are already safe (Framework_Blueprint §4-2 uses r_avg as a
#           PROPORTION against a sec_qs budget, so a different-size paper cannot inflate or
#           shrink allocation), but subject/subtopic MIX is still inherited from whichever
#           eras the corpus contains. Era-scoped frequency requires era-tagging through the
#           Step-5 manifest and Frequency xlsx and is a separate change.
#   v1.8 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           Framework_PYQPrepare v1.0 allows session to be omitted from date labels.
#           (1) build_date_label_re(): session_keyword+number now optional in regex.
#               Old: ^\[DD-Mon-YYYY\s+<keyword>\s+\d+\]$
#               New: ^\[DD-Mon-YYYY(?:\s+<keyword>\s+(\d+))?\]$
#           (2) parse_date_label(): session defaults to 1 when not present in label.
#           (3) CHECK 3: accepts both [DD-Mon-YYYY] and [DD-Mon-YYYY <keyword> N].
#           (4) EC-S10: error message updated to show both date label formats.
#           (5) EC-S15: updated — Step 1 now omits session entirely for single-session
#               exams (no default session=1). parse_date_label defaults to 1.
#           (6) Header + bottom STEP 1 FORMAT CONTRACT updated for optional session.
#           (7) make_output_filename(): handles session-less date labels.
#           Cross-step sync: Framework_PYQPrepare v1.0 §1 S1-3 (date label contract).
#   v1.7 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3 in §12 DoD POST-DELIVERY block.
#           Zero logic change.
#   v1.6 — 2026-07-06 — CLOSED DELIVERABLE SET CONTRACT.
#           Added closed-set delivery contract to match cross-framework standard
#           (PYQAnalyse §10, MockCreate S13-6). Header OUTPUT now says "(1 file,
#           nothing else)" with explicit DO-NOT-DELIVER list. §9 execution model
#           has a DELIVERABLE SET CONTRACT block with pre-delivery check (exactly
#           1 file, correct path, all validations passed). §12 DoD item 18 added.
#           Low structural risk (single-file deterministic script output), but
#           formalised for consistency after SSC CGL Tier 2 PYQAnalyse failure
#           (unauthorized taxonomy_draft_v2.json delivery) exposed the gap pattern.
#
#   v1.5 — 2026-07-06 — EXAM_CONFIG V2.5 SCHEMA COMPATIBILITY.
#           Step 2a v2.5 expanded exam_config.json with marking_scheme[], level, medium,
#           max_attempt, and question_types. PYQSort does NOT consume these new fields
#           (sorting depends on taxonomy + Q-ranges + session_keyword, not marks or level).
#           Change: S1-3 file inventory printout updated to reflect new schema fields
#           for transparency (shows marking ranges count, level, medium if present).
#           sections[] now includes max_attempt in the loaded schema — PYQSort ignores it
#           (sorting is independent of attempt limits). Zero code logic changes.
#
#   v1.4 — 2026-07-03 — EXAM-AGNOSTIC AUDIT (6 rigidity fixes).
#          (1) DATE_LABEL_RE: replaced hardcoded "Shift" with session_keyword
#              read from exam_config.json. Supports Shift/Slot/Phase/Paper/
#              Session/Morning/Afternoon or any custom keyword. parse_date_label()
#              and Check 3 validation both use the configurable pattern.
#          (2) Check 4 NAT-awareness: exams with NAT questions (answer_type=
#              numerical) have questions with ZERO options. Check 4 now counts
#              only MCQ questions (total − NAT count) for the options threshold.
#              NAT questions are identified by having 0 option paragraphs in
#              their body_elems.
#          (3) Page size: replaced hardcoded US Letter (8.5×11") with page_size
#              from exam_config.json. Default is A4 (8.27×11.69") — the standard
#              for Indian competitive exams. US Letter available via config.
#          (4) EC-S10 softened: missing date label still raises ValueError (it IS
#              a parse failure), but the error message now names Step 1 as the
#              fix location and documents the Step 1 format contract.
#          (5) Sort key shift field documented: for single-session exams, Step 1
#              synthesises session=1, making field 7 a no-op tiebreak. This is
#              correct behaviour, not dead weight.
#          (6) PROOF section expanded: added GATE (1 section, NAT, no session),
#              Banking (multi-slot), UPSC (multi-paper) as covered exam patterns.
#              Added Step 1 format contract as explicit prerequisite.
#   v1.3 — 2026-07-03 — DEEP-RESEARCH AUDIT (14 fixes).
#          (1) Q_PATTERNS drift: patterns 1-2 used `\s` instead of `\s+`,
#              misaligned with Step 5 E-2. Fixed to `\s+` for contract parity.
#          (2) OPT_RE replaced: single `r'^[1-5]\.\s'` replaced with full
#              5-pattern OPT_PATTERNS matching Step 5 E-3 / PYQAnalyse exactly.
#              is_option() function aligned.
#          (3) Taxonomy table parser rewritten: cur_topic_for_table was declared
#              but never used — all subtopics were attributed to the LAST topic.
#              Fixed: table rows now properly track their parent topic via
#              section-topic detection within each table.
#          (4) load_exam_config circular dependency: function required exam_code
#              to find the file containing exam_code. Fixed: glob search for
#              any *_exam_config.json in /mnt/project/.
#          (5) Pipeline position updated: "TestSeriesRow" → "Step 1 PYQ Prepare",
#              Step 4 PYQCount added between PYQSort and PYQExtract, full 11-step
#              pipeline listed.
#          (6) make_output_filename: multi-date case now computes actual earliest
#              and latest dates instead of generic "Multi" placeholder.
#          (7) renumber_stem: extended to handle all Q_PATTERNS formats (Q.N,
#              QN., Question N:, N., (N)) not just Q.N.
#          (8) Month regex aligned: DATE_LABEL_RE changed from `{3,}` to `{3}`
#              to match Check 3 validation exactly.
#          (9) subtopic_idx reset per topic in taxonomy table parser.
#          (10) Check 4 options count: changed from hardcoded 4 to exam_config.
#          (11) Footer version marker added.
#          (12) Section detection fallback: marker_mode mismatch changed from
#               warn-and-fallback to HARD STOP.
#          (13) S3-1 comment corrected.
#          (14) §11 Exam-Agnostic Guarantee updated.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (1 fix). S6-2 sub-section heading still
#          said "STEP 0 E-1 COMPATIBLE" — missed by v1.1 audit. Corrected to
#          "STEP 5 E-1 COMPATIBLE". No code logic changed.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (1 fix). 4 "Step 0" references corrected
#          to "Step 5" (PYQExtract). Step 0 was the old internal name; the
#          canonical pipeline position is Step 5. No code logic changed.
#   v1.0 — Initial release. Derived from TestSeriesSort Tier 1 v10 + Tier 2 v3.
#          Exam-agnostic taxonomy loading. Dual section-detection mode (markers + Q-range).
#          Heading format contract with Step 5 E-1 parser. 13 edge cases.
#          All pipeline mechanics inherited: insert_para, image re-embedding,
#          OMML walker, date label iron rule, 9-check validator.

---

## §1 — SESSION START

### S1-0 — TAXONOMY LOCK VERIFICATION (v1.13 — MANDATORY, runs FIRST)

```
PYQSort and everything after it (PYQCount -> PYQExtract -> MockBlueprint ->
MockCreate) are built on ONE assumption: the taxonomy is LOCKED and the lock was
EARNED. That assumption was never verified anywhere.

Before v1.13, [ExamCode]_approval_record.json was produced at Step 2c, uploaded to
project Files, and then read by NOTHING. The string "approval_record" did not appear
in this spec, in Framework_Blueprint.md, in Framework_PYQDeliver.md, or in
Framework_DeliveryFooter.md. A lock that nothing verifies is not a lock — it is a
receipt. GAP-2026-07-25-001 travelled from Step 2c through five downstream steps
with zero detection points precisely because no such point existed.

  approval = glob('*_approval_record.json') in project Files

  HARD STOP — "no record" (the lock was never established):
    If no approval_record.json is present:
      "Taxonomy lock not verified — [ExamCode]_approval_record.json is missing
       from project Files.
       PYQSort classifies every question against a taxonomy that Step 2c is
       responsible for reconciling and locking. Without that record there is no
       evidence the reconciliation ran at all.
       NEXT ACTION: run PYQApprove and upload all 3 deliverables."
      DO NOT sort. DO NOT proceed on the Analysis doc alone — the doc shows what
      the taxonomy IS, never whether it was checked.

  HARD STOP — "status" (the lock was refused):
    If record['status'] not in ('CLEAN', 'CLEAN_ADJUDICATED'):
      HELD     -> a construction defect was found and the taxonomy was NOT locked.
      DEGRADED -> a mode-B run; it never locks and never reaches Branch A.
      "Taxonomy is not locked — approval_record status is [status].
       NEXT ACTION: resolve the S4-0 findings, then re-run PYQApprove."

  HARD STOP — "unattested" (the lock cannot be shown to have been earned):
    If record.get('schema_version') is absent or < '1.1'
       OR record['checks']['missing'] is non-empty      (INV-7)
       OR record['checks']['vacuous'] is non-empty      (INV-8)
       OR record.get('unmaterialisable')                (INV-9):
      "Taxonomy lock cannot be verified — the approval record does not prove its
       checks ran.
         schema        : [schema_version or 'pre-1.1 (no attestation)']
         missing       : [checks.missing]
         vacuous       : [checks.vacuous]
         unmaterialisable: [unmaterialisable]
       A pre-1.1 record proves nothing about which checks executed: under the
       engine that produced it, C5/C6/C7 could be skipped entirely and the record
       would still read CLEAN.
       NEXT ACTION: re-run PYQApprove with reconcile_taxonomy.py >= v1.1. This is
       RECONCILIATION, not re-derivation — it reads taxonomy_draft.json and writes
       only approval_record.json, and CANNOT change a locked taxonomy.
       Do NOT re-run PYQDraft."

  PROCEED only when: record exists, status is CLEAN or CLEAN_ADJUDICATED, schema
  >= 1.1, and missing / vacuous / unmaterialisable are all empty.

  Print one line on success, so the verification is visible rather than assumed:
    "Taxonomy lock verified: [status], checks C1-C7 executed, engine [engine_version]."
```

### S1-0b — TAXONOMY CONTENT CROSS-CHECK (v1.14 — MANDATORY, runs with S1-0)

```
S1-0 proves the lock was EARNED. It does not prove that the taxonomy PYQSort is
about to sort against is the taxonomy that was LOCKED. Those are different claims,
and GAP-2026-07-25-002 Defect B satisfied the first while violating the second:
the record read CLEAN, every attestation passed, and the reader had flattened six
subjects into one.

v1.15 — THE COMPARISON IS NO LONGER WRITTEN HERE. S1-0b was the first place to make
this claim and, for one release, the only one. It is now made at Steps 4, 5 and 6 as
well, so the rule lives in corpus_io as assert_taxonomy_lock() and every step calls
it. Four transcriptions of one comparison is how the four Analysis-doc readers of
GAP-2026-07-25-002 happened; the fix for that was deletion, and so is this one. The
claim, the message and the operator action are unchanged — only their location is.
```

```python
import corpus_io

# ONE call. It selects the taxonomy source, verifies identity, and returns the
# shape S1-2 has always returned. S1-2 reuses this object; it does NOT load again.
ANALYSIS_DOC = corpus_io.load_taxonomy(record=approval_record, step='PYQSort')
```

```
  v1.16 — WHERE THE TAXONOMY COMES FROM. load_taxonomy() prefers the approval
  record's own "taxonomy" key (reconcile_taxonomy >= v1.3, schema >= 1.3) and falls
  back to the Analysis doc for records written before that. The record is JSON,
  which the platform stores byte-for-byte, so on the preferred path no Word document
  is read at all and no extraction grammar is involved. The record VALIDATES ITSELF
  — the fingerprint it carries was computed from the taxonomy it carries — so the
  identity claim below is made on either path, from one implementation.
    source='approval_record' -> ingest_form='json'  (preferred; nothing to parse)
    source='analysis_doc'    -> ingest_form='text' | 'ooxml'  (pre-1.3 records)
  Exams approved before schema 1.3 keep working unchanged and need no re-run. When
  one IS re-run through PYQApprove — reconciliation only — it moves to the preferred
  path automatically.

  load_taxonomy() HARD STOPS on exactly two identity conditions, both of which used
  to be spelled out here:

    "no fingerprint" — the record carries no 'taxonomy_fingerprint' key, i.e. it
      predates the contract (reconcile_taxonomy.py v1.2). The message names the
      re-run as RECONCILIATION, not re-derivation: it reads taxonomy_draft.json and
      rewrites only approval_record.json, and CANNOT change a locked taxonomy. Do
      NOT re-run PYQDraft.

    "mismatch" — fp_locked != doc['fingerprint']. Either the Analysis doc was edited
      after PYQApprove, or a different exam's doc is in this project. The message
      names both the restore path and, if the taxonomy genuinely changed, the
      requirement to re-sort every paper already sorted under the old one.

  Either way: DO NOT sort.

  It additionally HARD STOPS when a record that CARRIES a taxonomy does not agree
  with itself — the fingerprint it records is not the fingerprint of the taxonomy it
  records, or the declared taxonomy_counts do not match what the taxonomy assembles
  to, or a name is repeated. A repeated name matters more than it looks: it would
  collapse on assembly and the fingerprint would NOT notice, because it is computed
  over the same duplicated triples and therefore agrees with itself.

  `record=` is passed because S1-0 has already loaded and attested the record.
  Omitting it would make load_taxonomy() discover the record a second time — a second
  read of a file this step has already validated, and one more place for the two
  reads to disagree. Steps 4-6 omit it because they have no equivalent of S1-0.

  The fingerprint is computed over slugify()-normalised triples
  (blueprint_core.taxonomy_fingerprint), so it is invariant to exactly the cosmetic
  variance the subtopic_id contract already tolerates and sensitive to everything
  else. Byte-identity of display names is a separate guarantee, enforced at Step 4
  by PYQAnalyse Task 2.5.

  WHY THIS IS NOT REDUNDANT WITH THE READER'S OWN SELF-CHECK. Cluster K asserts the
  doc agrees with ITSELF; S1-0b asserts the doc is the one that was APPROVED. A doc
  that is internally perfect but belongs to a different run passes the first and
  fails the second.

  Print one line on success:
    "Taxonomy content verified: [K] subjects / [N] subtopics, fingerprint matches
     the lock."
```

### S1-1 — Trigger parsing

```
Trigger: PYQSort
Trigger matching is case-insensitive.

Parse:
  ExamCode : read from exam_config.json in project knowledge.
             The file is discovered by glob (*_exam_config.json), NOT by
             constructing a filename from an already-known exam code.
             If no exam_config found → HARD STOP:
               "No exam_config.json found.
                Run PYQDraft [ExamCode] first, then upload
                Analysis docs + exam_config.json to this project."
```

### S1-2 — Load taxonomy from Analysis docs

```python
import json, os, re, copy, glob, shutil
from collections import Counter
from docx import Document

# ── MODULES (both routed to PYQSort in routes.json) ──────────────────────────
#   blueprint_core  ENGINE    — pure decisions, standard library only (Clusters G, H)
#   corpus_io       I/O SHELL — image integrity + size governor (Clusters I, J)
# The split is deliberate: Steps 6-11 import blueprint_core purely for allocation
# arithmetic, so putting PIL or python-docx in it would make the allocation core
# unimportable wherever those packages are absent — the P0 recorded in
# Framework_MockTestAnalyse v2.26, where a failed `import blueprint_core` aborted
# Step 5 for EVERY exam. corpus_io is the one home for impure corpus plumbing.
import corpus_io                 # v1.12 — S7-5 census, S7-6 governor, S7-7 survival gate
                                 # v1.14 — Cluster K: THE Analysis-doc reader (S1-2)

def load_exam_config():
    """
    Load exam_config.json from project knowledge via glob search.
    No exam_code needed — discovers any *_exam_config.json file.
    Returns (exam_code, config_dict) or raises SystemExit.
    """
    matches = sorted(glob.glob('/mnt/project/*_exam_config.json'))
    if not matches:
        raise SystemExit(
            "HARD STOP: No *_exam_config.json found in project knowledge.\n"
            "Run PYQDraft [ExamCode] first, then upload\n"
            "Analysis docs + exam_config.json to this project.")
    if len(matches) > 1:
        raise SystemExit(
            f"HARD STOP: Multiple exam_config.json files found: {matches}\n"
            "Only one exam should be configured per project.")
    config = json.load(open(matches[0], encoding='utf-8'))
    exam_code = config.get('exam_code', os.path.basename(matches[0]).split('_exam_config')[0])
    return exam_code, config

def load_taxonomy_from_analysis_docs():
    """Load the COMPLETE taxonomy from the approved Analysis doc.

    v1.14 (GAP-2026-07-25-002) — DELEGATED. This function used to carry its own
    reader, and that reader was wrong in two independent ways:

      DEFECT A (loud)   its glob required a trailing '_' after "Analysis", so it
                        matched the per-subject filenames PYQAnalyse retired at
                        v2.6 and NO filename it has produced since. Zero files
                        found; hard stop; the message told the operator to upload
                        a file that was already correctly present.
      DEFECT B (silent) it delimited SUBJECTS BY FILE BOUNDARY — a
                        `if not section_name` latch pinned the first "Subject:"
                        heading and discarded every later one. On the first real
                        exam it returned 1 subject where the doc declares 6, filed
                        all 131 subtopics under "General Biology", and produced
                        five topic_idx collision groups. Counts were right, so
                        nothing looked wrong.

    Defect A was the only thing preventing Defect B from reaching production. It
    was protecting by accident, which is why the obvious one-character glob fix
    would have been strictly worse than shipping nothing.

    The reader now lives in corpus_io Cluster K — ONE reader, ONE writer, ONE
    verifier for this artefact, with heading recognition delegated a level further
    to blueprint_core.parse_taxonomy_level() so every label form the engine knows
    works here automatically. corpus_io.read_analysis_doc() also HARD STOPS when
    the taxonomy it parses disagrees with the totals the document declares about
    itself, which is what makes this class of mis-parse loud rather than silent.

    Return shape is UNCHANGED, so every downstream consumer in this spec is
    untouched:
      { section_name: { 'subject_order': int,
                        'topics': { topic_name: {
                            'topic_idx': int,
                            'subtopics': { subtopic_name: {'subtopic_idx': int} } } } } }
    plus the ordered list of (subject, topic, subtopic) triples.

    NOTE ON topic_idx — it is now POSITIONAL WITHIN THE SUBJECT, which is what
    §S6-2 has always specified ("position of topic within its section's Analysis
    doc"). The old code derived it from the printed "Topic N:" label, which
    restarts at 1 for every subject in a merged doc.

    v1.16 — S1-0b ALREADY LOADED IT. corpus_io.load_taxonomy() performs the source
    selection, the read and the identity assertion in one call, and S1-0b makes that
    call because it is the first consumer. Loading again here would read the same
    artefact twice in one step and give the two reads a chance to disagree.
    """
    if ANALYSIS_DOC is None:                # only when S1-0b was somehow skipped
        raise SystemExit(
            "HARD STOP: S1-2 reached with no taxonomy loaded. S1-0b is MANDATORY and "
            "runs first — it is what loads and verifies the taxonomy.")
    return ANALYSIS_DOC['taxonomy'], ANALYSIS_DOC['triples']
```

### S1-3 — File inventory

```
List ALL received files:
  "Received files:
   • [filename].docx  (Row file, [size])

   Project knowledge loaded:
   • Taxonomy: [total] subtopics across [M] subjects
     source: [approval_record / analysis_doc]   <- v1.16, from doc['source']
     ingest form: [json / text / ooxml]         <- v1.15, from doc['ingest_form']
   • exam_config.json ([ExamCode], [total_questions] questions, [sections] sections)

   Section detection mode: [marker_mode / Q-range]
   Session keyword: [session_keyword] (from exam_config)
   Page size: [page_size] (from exam_config)
   Level: [level] (from exam_config, if present)
   Medium: [medium] (from exam_config, if present)
   Marking ranges: [N] range(s) (from exam_config, if present)"

REPORT the source and the ingest form; never warn about either and never ask the
operator to act on them. source='approval_record' with ingest_form='json' is the
preferred state; source='analysis_doc' with ingest_form='text' is NORMAL for any
exam approved before reconcile_taxonomy v1.3 — see EC-S20 and EC-S21. It is printed for the same reason
S1-0 prints its one line on success: a verification nobody can see is a
verification nobody can trust, and when the platform's extraction grammar
eventually changes this line is the first evidence of it.

If Row file missing → "Upload 1 Row file (.docx) and re-trigger PYQSort."
If Analysis docs missing → HARD STOP (see S1-2).
If exam_config missing → HARD STOP (see S1-1).
```

---

## §2 — SECTION DETECTION

### S2-1 — Auto-detect mode

```python
def detect_section_mode(doc, exam_config):
    """
    Auto-detect whether the Row file uses module separators or Q-number ranges.
    Check first 20 paragraphs for === separators.
    """
    for i, para in enumerate(doc.paragraphs[:20]):
        text = para.text.strip()
        if re.match(r'^===\s+.+\s+===$', text):
            return 'marker'

    # No markers found — use Q-range from exam_config
    if exam_config.get('marker_mode', False):
        # Config says markers expected but none found — HARD STOP
        raise SystemExit(
            "HARD STOP: exam_config says marker_mode=true but no === separators\n"
            "found in the first 20 paragraphs of the Row file.\n"
            "Either the wrong file was uploaded, or the Row file format is corrupted.\n"
            "Check the file and re-upload.")
    return 'q_range'
```

### S2-2 — Q-range section assignment

```python
# SENTINEL — the section label used when a Q-number falls outside every configured section
# range. v1.10: imported from the ENGINE instead of being re-declared here. Framework_PYQAnalyse
# routes questions to the same sentinel under a DIFFERENT trigger, so two spec-local copies of
# one literal was a drift waiting to happen. One definition, both importers.
import blueprint_core as bc          # ENGINE (routed for PYQSort in routes.json)
OUT_OF_PATTERN = bc.OUT_OF_PATTERN


def get_section_by_q_range(q_num, exam_config):
    """
    Determine section from Q-number using exam_config section boundaries.
    Returns a section name, or OUT_OF_PATTERN if the Q-number is outside every range.

    v1.9 — NEVER RETURNS None (was: returned None, silently).
      WHY THIS CHANGED. exam_config describes the CURRENT exam pattern. A PYQ paper from a
      previous pattern era can carry Q-numbers beyond it — e.g. a 100-question legacy paper
      sorted against a 60-question current config leaves Q.61-Q.100 matching no section.
      The old None return was stored straight into the question record with no guard
      anywhere in the corpus, so those questions silently failed every downstream
      (section, topic, subtopic) lookup: a 40% data loss on that paper, invisible to the
      operator. This is the same defect class as the Blueprint coverage gate's asymmetry
      (Framework_Blueprint v1.36 §2 S2-3) — the pipeline assumed PYQ structure always
      matches current structure.
      An explicit sentinel keeps the questions ADDRESSABLE rather than dropping them: they
      still reach taxonomy discovery (the whole reason legacy papers are retained is the
      variety of concepts and question shapes they expose), while never being mistaken for
      a real section of the current pattern.
    """
    for sec in exam_config['sections']:
        q_start, q_end = sec['q_range']
        if q_start <= q_num <= q_end:
            return sec['name']
    return OUT_OF_PATTERN
```

### S2-3 — Marker section assignment

```python
def parse_module_separator(text):
    """
    Parse === Subject Name === separator.
    Returns subject name or None.
    """
    m = re.match(r'^===\s+(.+?)\s+===$', text.strip())
    return m.group(1).strip() if m else None
```

---

## §3 — PARSER (Row File Reading)

### S3-1 — Question extraction

```python
# Q-number detection patterns — ALIGNED WITH Step 5 E-2 (MUST stay in sync)
Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1
    r'^Q(\d+)\.\s+',               # Q1.  Q25.
]

# DELEGATED to the engine (blueprint_core Cluster G). Four specs parse Q-numbers from the
# same documents and must agree exactly; a local copy in any one of them is drift waiting to
# happen. This table mirrors the engine's canonical table EXACTLY and is verified by
# audit_deep.py TABLE-PARITY.
#
# WHY ONLY TWO PATTERNS — DO NOT ADD MORE (2026-07-25).
# Three further forms exist in RAW exam sources — "Question 1:", bare "1." and "(1)" — and
# Step 1 detects them via its own SOURCE_Q_PATTERNS. They are deliberately ABSENT here and
# must never be restored. After Step 1 every document is NORMALISED: questions read "Q.N"
# and OPTIONS read "N. text". The bare-number pattern therefore matches every option line.
# Verified by execution on a canonical two-question fixture: the two-pattern table finds 2
# question starts; the five-pattern table finds 10. A 100-question paper would parse as 500.
# Until 2026-07-25 these tables carried all five entries while the engine implemented two,
# and audit_deep TABLE-PARITY could not see it: its extraction regex stopped at the first
# ']', which occurs inside r'^Question\s+(\d+)\s*[:.]', so it compared a silently truncated
# two-entry slice against the engine's two and always passed.
detect_question_start = bc.detect_question_start

# ═══════════════════════════════════════════════════════════════════
# DATE LABEL DETECTION — CONFIGURABLE SESSION KEYWORD
# ═══════════════════════════════════════════════════════════════════
#
# The session keyword (Shift, Slot, Phase, Paper, Session, etc.) is read
# from exam_config.json at runtime. Step 1 (PYQ Prepare) produces date labels
# using the SAME keyword. The regex is built dynamically.
#
# exam_config.json field:
#   "session_keyword": "Shift"      (SSC CGL, SSC CHSL, SSC MTS)
#   "session_keyword": "Slot"       (IBPS PO, IBPS Clerk, SBI PO)
#   "session_keyword": "Phase"      (RRB NTPC, RRB Group D)
#   "session_keyword": "Paper"      (UPSC CSE, UPSC CAPF)
#   "session_keyword": "Session"    (GATE, CAT)
#   "session_keyword": "Shift"      (default if not specified)
#
# For single-session exams (GATE, UPSC single-paper):
#   Step 1 omits session entirely: [DD-Mon-YYYY]
#   parse_date_label() defaults session to 1 — sort key field 7 is a no-op.
# ═══════════════════════════════════════════════════════════════════

def build_date_label_re(session_keyword):
    """
    Build date label regex dynamically from exam_config session_keyword.
    Session part is OPTIONAL — matches both [DD-Mon-YYYY] and
    [DD-Mon-YYYY <keyword> N] formats.

    v1.18 (GAP-2026-07-27-E) — the label now optionally carries the ORIGINAL question
    number as a trailing " Q<N>". The group is OPTIONAL, so every sorted file produced
    before v1.18 still parses byte-identically and no re-sort is forced.

    WHY HERE. Step 3 renumbers questions into taxonomy order, which DESTROYS the exam
    position. Step 5's MSQ detector then has only the instruction phrase to go on, and
    measured 24 MSQ across 1,719 questions on an exam whose marking scheme reserves
    Q31-40 for MSQ (~10/paper, so ~120 in the current era alone). Step 5 cannot recover
    what Step 3 discarded — so Step 3 must stop discarding it. The date label is the
    right carrier because it is rebuilt (never cloned) on every emit and Step 5 already
    parses it, so no new artefact and no new parser are introduced.
    """
    return re.compile(
        r'^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})'
        r'(?:\s+' + re.escape(session_keyword) + r'\s+(\d+))?'
        r'(?:\s+Q(\d+))?'
        r'\]$'
    )


# ── ORIGINAL EXAM POSITION — DELEGATED (v1.18, Cluster Q) ────────────────────
# GAP-2026-07-27-E. Step 3 WRITES this stamp and Step 5 READS it. A format defined in
# two specs is exactly the shape that produced the is_option drift v1.17 had to unwind:
# each file's docstring asserted alignment with the other, and both claims were false.
# corpus_io >= v1.9 owns the single definition; both specs bind to it by assignment, so
# a divergence is not merely discouraged, it is unrepresentable.
#
# The stamped field is OPTIONAL. A label written before v1.18 parses to None, which
# means UNKNOWN and must never be read as position 0. No exam is forced to re-sort.
parse_original_q_num = corpus_io.parse_original_q_num
stamp_original_q_num = corpus_io.stamp_original_q_num   # v1.18 — DELEGATED (Cluster Q)

MONTH_MAP = {
    'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12
}

def parse_date_label(text, date_label_re):
    """
    Parse [DD-Mon-YYYY <session_keyword> X] or [DD-Mon-YYYY] →
    (year, month, day, session) or None.
    Session defaults to 1 when not present in the label.
    """
    m = date_label_re.match(text.strip())
    if not m: return None
    day = int(m.group(1))
    month = MONTH_MAP.get(m.group(2)[:3].lower(), 0)
    year = int(m.group(3))
    session = int(m.group(4)) if m.group(4) else 1
    return (year, month, day, session)

# Option detection — ALIGNED WITH Step 5 E-3 / PYQAnalyse (MUST stay in sync)
# The (.+) suffix requires actual option text after the label, preventing bare
# labels like "1. " from being treated as options.
# ── OPTION PREDICATE — DELEGATED (v1.17, audit_deep [XSPEC-DRIFT]) ────────────
# This file previously defined its own is_option() with the docstring "Aligned with
# Step 5's is_option() — same 5 patterns." That claim became FALSE when
# MockTestAnalyse v2.34/v2.35 added the image-option path, and the consequence was
# real here: _count_options_in_body() and the option re-indent pass both use this
# predicate, so an image option ("1." with a picture and no text) was NOT COUNTED and
# NOT INDENTED. Measured on IIT_JAM_BIOTECHNOLOGY 2022: 156 counted vs 160 actual.
# corpus_io >= v1.6 owns the single definition. Both call sites below pass the
# paragraph element — delegating WITHOUT passing it compiles but keeps the undercount.
OPT_PATTERNS = corpus_io.OPT_PATTERNS
is_option    = corpus_io.is_option
```

### S3-2 — Full extraction algorithm

```python
def extract_questions(doc, section_mode, exam_config, date_label_re):
    """
    Walk the Row file, extract question blocks.
    Each question = {
      'q_num': int (original),
      'section': str,
      'date_label': str,   # e.g. '[12-Sep-2025 Shift 1]'
      'date_parsed': (year, month, day, session),
      'stem_elem': <w:p> element (deep-copyable),
      'body_elems': [<w:p> or <w:tbl> elements],
      'module': str or None (for marker mode),
      'has_options': bool   # False for NAT questions
    }
    """
    session_keyword = exam_config.get('session_keyword', 'Shift')
    questions = []
    current_module = None
    current_date_label = None
    current_q = None
    body = doc.element.body

    for child in body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            text = child.text or ''
            # Reconstruct full text from all <w:t> elements
            NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            runs_text = ''.join(
                t.text for t in child.iter(f'{{{NS}}}t') if t.text
            )
            text = runs_text.strip()

            # Check for module separator (marker mode)
            if section_mode == 'marker':
                mod = parse_module_separator(text)
                if mod:
                    current_module = mod
                    continue

            # Check for date label
            dl = parse_date_label(text, date_label_re)
            if dl:
                current_date_label = text.strip()
                continue

            # Check for question start
            q_num = detect_question_start(text)
            if q_num is not None:
                # Save previous question (and compute has_options)
                if current_q:
                    current_q['has_options'] = _count_options_in_body(current_q['body_elems']) > 0
                    questions.append(current_q)

                # Determine section
                if section_mode == 'marker':
                    section = current_module
                else:
                    section = get_section_by_q_range(q_num, exam_config)

                current_q = {
                    'q_num': q_num,
                    'section': section,
                    # v1.9 — structural provenance, NOT a content judgement. 'out_of_pattern'
                    # means this Q-number lies beyond every range in the current exam_config,
                    # i.e. the paper predates (or postdates) the current pattern. Carried so
                    # the operator can see era mixing instead of inferring it from a silent gap.
                    'pattern_era': ('out_of_pattern' if section == OUT_OF_PATTERN
                                    else 'current'),
                    'date_label': current_date_label or '',
                    'date_parsed': parse_date_label(current_date_label, date_label_re) if current_date_label else None,
                    'stem_elem': child,
                    'body_elems': [],
                    'module': current_module,
                    'has_options': True  # default, recomputed when next Q starts
                }

                if not current_date_label:
                    raise ValueError(
                        f"Q.{q_num} has no date label. "
                        f"Step 1 (PYQ Prepare) must emit a date label before every "
                        f"question in format: [DD-Mon-YYYY] or [DD-Mon-YYYY {session_keyword} N]. "
                        f"Fix the Row file in Step 1, then re-upload."
                    )
                continue

            # Not a separator, not a date, not a Q start → body element
            if current_q is not None:
                current_q['body_elems'].append(child)

        elif tag == 'tbl':
            # Table element → part of current question body
            if current_q is not None:
                current_q['body_elems'].append(child)

    # Save last question
    if current_q:
        current_q['has_options'] = _count_options_in_body(current_q['body_elems']) > 0
        questions.append(current_q)

    report_pattern_era(questions, exam_config, section_mode)
    return questions


def report_pattern_era(questions, exam_config, section_mode):
    """v1.9 — Surface pattern-era mixing to the operator. NEVER silent.

    A PYQ corpus routinely spans more than one exam pattern. That is DESIRABLE for taxonomy
    and question-variety purposes — the reason legacy papers are kept is precisely that they
    expose concepts, phrasings, difficulties and formats the current-era papers do not.
    What is NOT acceptable is the pipeline discovering the mismatch and saying nothing.

    Before v1.9 every Q-number beyond the configured ranges got section=None, was stored
    unguarded, and then failed every downstream (section, topic, subtopic) lookup. On a
    100-question legacy paper sorted against a 60-question current config that is a silent
    40% data loss on a single file, with no line of output to indicate it happened.

    This function does not decide anything and never mutates. It reports, so the operator
    holds the corpus-scope decision. Exam-agnostic: reads only exam_config and the observed
    Q-numbers, and hardcodes no exam, section, count or year.
    """
    if section_mode == 'marker':
        return                      # marker mode carries its own structure; ranges unused
    total_cfg = sum(s['q_count'] for s in exam_config['sections'])
    oop = [q for q in questions if q.get('pattern_era') == 'out_of_pattern']
    observed = len(questions)
    if not oop and observed == total_cfg:
        return                      # paper matches the current pattern exactly — nothing to say

    print("PATTERN-ERA REPORT")
    print(f"  Questions in this paper        : {observed}")
    print(f"  Questions in current exam_config: {total_cfg}")
    if observed != total_cfg:
        direction = 'LARGER' if observed > total_cfg else 'SMALLER'
        print(f"  -> This paper is {direction} than the current pattern "
              f"({observed} vs {total_cfg}).")
    if oop:
        nums = sorted(q['q_num'] for q in oop)
        rng = f"Q.{nums[0]}-Q.{nums[-1]}" if len(nums) > 1 else f"Q.{nums[0]}"
        print(f"  Out-of-pattern questions      : {len(oop)} ({rng})")
        print(f"  These fall outside every section range in exam_config. They are NOT")
        print(f"  dropped: each is classified against the FULL taxonomy so its concept")
        print(f"  still reaches the corpus. They carry pattern_era='out_of_pattern'.")
    print("  CONSEQUENCES — counts are safe, MIX is not:")
    print("    Allocation cannot be inflated or shrunk by a different-size paper "
          "(Framework_Blueprint §4-2 uses r_avg as a PROPORTION against a sec_qs budget).")
    print("    Subject/subtopic MIX and format mix are inherited from whichever eras the")
    print("    corpus contains. Recency weighting (§3, last 2 valid years x2) dampens this")
    print("    but does not remove it when old-era years outnumber current-era ones.")
    print("  DECIDE: keep the full corpus (maximum question variety, era-blended mix), or")
    print("  restrict the corpus to current-pattern papers (faithful mix, less variety).")

def _count_options_in_body(body_elems):
    """Count option paragraphs in a question's body elements."""
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    count = 0
    for elem in body_elems:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        text = ''.join(t.text for t in elem.iter(f'{{{NS}}}t') if t.text)
        # elem is passed so an IMAGE OPTION (bare "1." + picture) is counted.
        if is_option(text.strip(), elem):
            count += 1
    return count
```

### S3-3 — OMML text extraction (for classification)

```python
MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

def omml_to_text(omath_elem):
    """
    Recursive OMML → linear text renderer for classification.
    Walks <m:f>, <m:sSup>, <m:sSub>, <m:rad>, <m:d>, <m:nary>, <m:eqArr>, <m:r>, <m:t>.
    """
    def recurse(el):
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag == 'r':
            t = el.find(f'{{{MATH_NS}}}t')
            return (t.text or '') if t is not None else ''
        elif tag == 'f':
            n = el.find(f'{{{MATH_NS}}}num')
            d = el.find(f'{{{MATH_NS}}}den')
            return f'({recurse(n)})/({recurse(d)})' if n is not None and d is not None else '?/?'
        elif tag == 'sSup':
            b = el.find(f'{{{MATH_NS}}}e')
            s = el.find(f'{{{MATH_NS}}}sup')
            return f'{recurse(b)}^{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'sSub':
            b = el.find(f'{{{MATH_NS}}}e')
            s = el.find(f'{{{MATH_NS}}}sub')
            return f'{recurse(b)}_{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'rad':
            deg = el.find(f'{{{MATH_NS}}}deg')
            e = el.find(f'{{{MATH_NS}}}e')
            return f'√({recurse(e)})' if e is not None else '√?'
        elif tag == 'd':
            e = el.find(f'{{{MATH_NS}}}e')
            return f'({recurse(e)})' if e is not None else '(?)'
        else:
            return ''.join(recurse(c) for c in el)
    return recurse(omath_elem)

def get_full_stem_text(stem_elem, body_elems):
    """
    Extract complete stem text including OMML formulas.
    Used for classification — not for output (output preserves original XML).
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    parts = []

    for elem in [stem_elem] + body_elems[:3]:  # stem + first 3 body elems
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        for child in elem:
            ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if ctag == 'r':
                t = child.find(f'{{{NS}}}t')
                if t is not None and t.text:
                    parts.append(t.text)
            elif 'oMath' in child.tag:
                parts.append(omml_to_text(child))

    return ' '.join(parts).strip()
```

---

## §4 — CLASSIFICATION PROTOCOL

### S4-1 — Pre-build classification table

```
Before writing sort_pipeline.py, Claude builds a complete classification table
for ALL questions in the Row file:

  Q.N | Stem summary | Section | Topic | Subtopic

This table is the SINGLE SOURCE OF TRUTH. The CLASSIF dictionary in code
must be copied from this table exactly — never rewritten from memory.

Classification uses:
  1. Universal rules from §4-2 (Rule 1–6)
  2. Taxonomy from approved Analysis docs (loaded in §1-2)
  3. OMML-rendered stem text (from §3-3)
  4. Section assignment (from §2)
```

### S4-2 — Universal classification rules

```
RULE 1 — TOPICAL HOME WINS OVER SOLVE METHOD
  Pick the subtopic whose DOMAIN matches what the question is ABOUT,
  not what technique is USED to solve it.

  Canonical precedents (apply to ALL exams):
    Bank deposits earning interest       → Interest subtopic (not Percentage)
    Discount on marked price + profit    → Discount subtopic (not Profit & Loss)
    Two trains crossing                  → Trains/Speed subtopic (not generic SDT)
    Pipes filling a tank                 → Pipes subtopic (not Time & Work)
    Mixture at different prices          → Mixture subtopic (not Ratio)
    Compound interest multi-period       → CI subtopic (not Percentage)
    Polynomial remainder via factor      → Algebra subtopic (not Number System)
    Full multi-row DI table              → DI/Statistics subtopic
    Small 2-4 row reference table        → classify by arithmetic operation

RULE 2 — THE VERB AT THE END OF THE STEM DECIDES
    "find the ratio"       → Ratio subtopic
    "find the percentage"  → Percentage subtopic
    "find the average"     → Average subtopic
    "find the value of [trig]" → Trigonometry subtopic

RULE 3 — OMML-AWARE CLASSIFICATION IS MANDATORY
    Render OMML math before classifying. Never guess from garbled text.

RULE 4 — SECTION FROM STRUCTURE, NOT CONTENT
    marker_mode → section from === separator
    Q-range mode → section from Q-number range in exam_config
    A maths question in the Reasoning section STAYS in Reasoning.

RULE 5 — CLOSEST FIT FOR UNCLASSIFIABLE QUESTIONS
    If no subtopic fits perfectly → closest match. No flag. Decide and move on.

RULE 6 — IMAGE/FIGURAL QUESTIONS
    Image-only stem → section's spatial/figural subtopic.
    If no figural subtopic exists → most general subtopic in section.
```

### S4-3 — Taxonomy matching algorithm

```python
def classify_question(stem_text, section, taxonomy, options_text=''):
    """
    Classify a question into (topic, subtopic) within its section.
    Uses stem_text (OMML-rendered), section (from structure), and taxonomy.

    Returns: (topic_name, subtopic_name)

    Classification approach:
    1. Get all topics + subtopics for this section from taxonomy
    2. Match stem keywords against subtopic names and known patterns
    3. Apply Rules 1-6 for disambiguation
    4. If no match → closest fit (Rule 5)
    """
    # v1.9 — OUT-OF-PATTERN QUESTIONS (narrow, explicit exception to RULE 4).
    # RULE 4 ("section from structure, not content") exists so that a maths question sitting
    # in the Reasoning section STAYS in Reasoning. That rationale presupposes the question
    # HAS a structural section. A question from a previous pattern era whose Q-number lies
    # beyond every configured range has none, so RULE 4 has nothing to say about it and
    # applying it anyway yields an empty candidate list — which is how these questions were
    # silently lost before v1.9.
    # For these, and ONLY these, classify against the FULL taxonomy (every section's topics).
    # The taxonomy is exam-wide and era-independent, so a genuine exam question always has a
    # home in it. This exception must not widen: it is gated on the sentinel, never on a
    # failed match, so a question that has a real section can never fall through to it.
    if section == OUT_OF_PATTERN:
        candidates = []
        for sec_name, sec_data in taxonomy.items():
            for topic, topic_data in sec_data.get('topics', {}).items():
                for subtopic in topic_data['subtopics']:
                    candidates.append((topic, subtopic))
    else:
        section_taxonomy = taxonomy.get(section, {}).get('topics', {})

        # Build a flat list of (topic, subtopic) candidates
        candidates = []
        for topic, topic_data in section_taxonomy.items():
            for subtopic in topic_data['subtopics']:
                candidates.append((topic, subtopic))

    # Claude classifies the question against these candidates
    # using stem analysis + Rules 1-6
    # Returns the best (topic, subtopic) match
    pass  # Claude's classification judgment applied here
```

### S4-4 — CLASSIF dictionary format

```python
# For Q-range mode (single Q-number namespace):
CLASSIF = {
    1:  ('General Intelligence & Reasoning', 'Analogy', 'General Word Analogy'),
    2:  ('General Intelligence & Reasoning', 'Analogy', 'General Word Analogy'),
    3:  ('General Intelligence & Reasoning', 'Series', 'Letter Group / Cluster Series'),
    # ...
    100: ('English Comprehension', 'Cloze Test', 'Vocabulary-Based Cloze (Appropriate Word)'),
}

# For marker mode (Q-numbers restart per module):
# Key = (module_name, q_num) — 2-tuple for single-paper inputs
# Key = (module_name, date_label, q_num) — 3-tuple for multi-paper inputs
CLASSIF = {
    ('Mathematical Abilities', 1): ('Mathematical Abilities', 'Number Systems', 'Simplification (BODMAS)'),
    ('Mathematical Abilities', 2): ('Mathematical Abilities', 'Fundamental Arithmetical Operations', 'Percentage'),
    # ...
}
```

---

## §5 — SORT ORDER

```
Every question has a sort key composed of 8 fields, compared left-to-right:

  (subject_idx, topic_idx, subtopic_idx, −year, −month, −day, +session, +orig_q_num)

Field definitions:
  subject_idx   : from exam_config.sections[].subject_order (or taxonomy load order)
  topic_idx     : position of topic within its section's Analysis doc
  subtopic_idx  : position of subtopic within its topic's table in Analysis doc
  −year         : from date label                              DESC (newest first)
  −month        : parsed month (Jan=1 … Dec=12)                DESC
  −day          : parsed day-of-month                          DESC
  +session      : parsed session number (Shift/Slot/Phase/etc) ASC (Session 1 before 2)
  +orig_q_num   : original Q-number from Row file              ASC (deterministic tiebreak)

For marker mode: orig_q_num is the per-module Q-number.
For single-session exams: session is always 1 (no-op tiebreak, correct by design).
```

```python
def make_sort_key(q, taxonomy, exam_config):
    """Build 8-field sort key for a classified question."""
    section = q['classified_section']
    topic = q['classified_topic']
    subtopic = q['classified_subtopic']

    sec_data = taxonomy.get(section, {})
    subject_idx = sec_data.get('subject_order', 99)

    topic_data = sec_data.get('topics', {}).get(topic, {})
    topic_idx = topic_data.get('topic_idx', 99)

    subtopic_data = topic_data.get('subtopics', {}).get(subtopic, {})
    subtopic_idx = subtopic_data.get('subtopic_idx', 99)

    dp = q.get('date_parsed')
    if dp:
        year, month, day, session = dp
    else:
        year, month, day, session = 0, 0, 0, 0

    return (
        subject_idx,
        topic_idx,
        subtopic_idx,
        -year,      # DESC
        -month,     # DESC
        -day,       # DESC
        session,    # ASC
        q['q_num']  # ASC
    )
```

---

## §6 — OUTPUT FILE STRUCTURE

### S6-1 — Filename pattern

```python
def make_output_filename(exam_code, questions, session_keyword):
    """
    Build output filename from exam code and date range in questions.
    Single date: [ExamCode]_DD-Mon-YYYY_<session_keyword>-N_Sorted_Q1-QN.docx
    Multi date:  [ExamCode]_DD-Mon-YYYY_to_DD-Mon-YYYY_Sorted_Q1-QN.docx
    """
    dates = set()
    date_label_re = build_date_label_re(session_keyword)
    for q in questions:
        if q.get('date_label'):
            dates.add(q['date_label'])

    total = len(questions)
    if len(dates) == 1:
        dl = list(dates)[0].strip('[]')
        parts = dl.split()
        date_str = parts[0]
        if len(parts) >= 3 and session_keyword in dl:
            session_num = parts[-1]
            return f'{exam_code}_{date_str}_{session_keyword}-{session_num}_Sorted_Q1-Q{total}.docx'
        else:
            return f'{exam_code}_{date_str}_Sorted_Q1-Q{total}.docx'
    else:
        # Multi-date: compute earliest and latest from parsed dates
        parsed = []
        for d in dates:
            p = parse_date_label(d, date_label_re)
            if p:
                parsed.append((p, d.strip('[]')))
        if parsed:
            parsed.sort()
            earliest_str = parsed[0][1].split()[0]   # DD-Mon-YYYY portion
            latest_str = parsed[-1][1].split()[0]
            return f'{exam_code}_{earliest_str}_to_{latest_str}_Sorted_Q1-Q{total}.docx'
        return f'{exam_code}_Multi_Sorted_Q1-Q{total}.docx'
```

### S6-2 — Heading format (STEP 5 E-1 COMPATIBLE — NON-NEGOTIABLE)

```
══════════════════════════════════════════════════════════════════
HEADING FORMAT — EXACT CONTRACT WITH Step 5 parse_taxonomy_level()
══════════════════════════════════════════════════════════════════

LEVEL 1 (Section/Subject):
  Text:    "Subject: <Section Name>"
  Styling: 14pt Bold Navy #003366
  Parser:  re.match(r'Subject:|Domain:', text) → level 1

LEVEL 2 (Topic):
  Text:    "Topic <N>: <Topic Name>"
  N:       1-indexed ABSOLUTE position from Analysis doc (gaps OK, no renumber)
  Styling: 12pt Bold Black #000000
  Parser:  re.match(r'Topic\s+\d+:', text) → level 2

LEVEL 3 (Subtopic):
  Text:    "<Subtopic Name>"  (no prefix)
  Name:    EXACT string from Analysis doc, .strip()-ed
  Styling: 11pt Bold Navy #003366
  Parser:  default → level 3

NOTE: Step 5's parser also supports "Chapter N" as a level 2 heading for
non-SSC exams. PYQSort always EMITS "Topic N:" format. The "Chapter N"
path exists only for backwards compatibility in downstream parsers.

DATE LABEL:
  Text:    "[DD-Mon-YYYY <session_keyword> X]"
  Examples: "[12-Sep-2025 Shift 1]"   (SSC)
            "[15-Jan-2025 Slot 2]"    (Banking)
            "[02-Feb-2025 Session 1]" (GATE)
  Styling: 11pt Bold Navy #003366, Right-aligned
  Always REBUILT from scratch (never cloned from source)
  Always emitted immediately above Q.N stem — zero paragraphs between

ALL headings built as raw OOXML via make_heading_para() + insert_para().
NEVER use doc.add_paragraph() — it breaks when mixed with insert_para().
NEVER set explicit LEFT alignment on headings — leave as None (unset).
```

### S6-3 — OOXML helper functions

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ═══════════════════════════════════════════════════════════════════
# PAGE SIZE — CONFIGURABLE VIA EXAM_CONFIG
# ═══════════════════════════════════════════════════════════════════
#
# exam_config.json field:
#   "page_size": "A4"           (default — 210mm × 297mm — Indian standard)
#   "page_size": "Letter"       (8.5" × 11" — US standard)
#
# All Indian competitive exams default to A4. Override via exam_config only.
# ═══════════════════════════════════════════════════════════════════

PAGE_SIZES = {
    'A4':     (8.27, 11.69),    # 210mm × 297mm — Indian standard
    'Letter': (8.5,  11.0),     # US Letter
}

def get_page_dimensions(exam_config):
    """Return (width_inches, height_inches) from exam_config page_size."""
    size_name = exam_config.get('page_size', 'A4')
    return PAGE_SIZES.get(size_name, PAGE_SIZES['A4'])

def insert_para(doc, elem):
    """Insert element into body BEFORE sectPr so it stays in document flow."""
    body = doc.element.body
    sectPr = body.find(qn('w:sectPr'))
    if sectPr is not None:
        body.insert(list(body).index(sectPr), elem)
    else:
        body.append(elem)

def make_heading_para(text, size_pt, bold, color_hex, space_before_pt, space_after_pt):
    """Build heading as raw OOXML — never use doc.add_paragraph()."""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before_pt * 20)))
    spacing.set(qn('w:after'),  str(int(space_after_pt  * 20)))
    pPr.append(spacing)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial'); rFonts.set(qn('w:hAnsi'), 'Arial')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz');   sz.set(qn('w:val'), str(int(size_pt * 2)))
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), str(int(size_pt * 2)))
    rPr.append(sz); rPr.append(szCs)
    if bold:
        rPr.append(OxmlElement('w:b')); rPr.append(OxmlElement('w:bCs'))
    clr = OxmlElement('w:color'); clr.set(qn('w:val'), color_hex)
    rPr.append(clr)
    r.append(rPr)
    t = OxmlElement('w:t'); t.text = text; r.append(t)
    p.append(r)
    return p

def make_date_label_para(date_str):
    """Build date label as raw OOXML — always rebuilt, never cloned."""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'right')
    pPr.append(jc)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial'); rFonts.set(qn('w:hAnsi'), 'Arial')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz');   sz.set(qn('w:val'), '22')
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), '22')
    rPr.append(sz); rPr.append(szCs)
    rPr.append(OxmlElement('w:b')); rPr.append(OxmlElement('w:bCs'))
    clr = OxmlElement('w:color'); clr.set(qn('w:val'), '003366')
    rPr.append(clr)
    r.append(rPr)
    t = OxmlElement('w:t'); t.text = date_str; r.append(t)
    p.append(r)
    return p

def make_blank_para():
    """One empty paragraph for inter-question spacing."""
    return OxmlElement('w:p')

def renumber_stem(stem_elem, new_q_num):
    """
    Replace the original Q-number with new_q_num in the stem's first <w:t>.
    Handles all Q_PATTERNS formats:
      Q.N, QN., Question N:, N., (N)
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    RENUMBER_PATTERNS = [
        (r'^(Q\.?\s*)\d+',        r'\g<1>' + str(new_q_num)),    # Q.N / QN
        (r'^(Question\s+)\d+',    r'\g<1>' + str(new_q_num)),    # Question N
        (r'^(\()\d+(\))',         r'\g<1>' + str(new_q_num) + r'\2'),  # (N)
        (r'^(\d+)(\.\s)',         str(new_q_num) + r'\2'),        # N.
    ]
    for t in stem_elem.iter(f'{{{NS}}}t'):
        if not t.text:
            continue
        for pat, repl in RENUMBER_PATTERNS:
            if re.match(pat, t.text):
                t.text = re.sub(pat, repl, t.text, count=1)
                return
```

### S6-4 — Emit loop (IRON RULE — non-negotiable order)

```python
def emit_sorted(out_doc, sorted_questions, taxonomy, src_doc, exam_config):
    """
    Emit all questions in sorted order with Subject/Topic/Subtopic headings.
    """
    from docx.shared import Inches

    # Set page dimensions from exam_config (default A4)
    page_w, page_h = get_page_dimensions(exam_config)
    sec = out_doc.sections[0]
    sec.page_width  = Inches(page_w)
    sec.page_height = Inches(page_h)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)

    prev_section = prev_topic = prev_subtopic = None
    new_q_num = 0

    for q in sorted_questions:
        section = q['classified_section']
        topic = q['classified_topic']
        subtopic = q['classified_subtopic']

        # Emit Subject heading on section change
        if section != prev_section:
            h = make_heading_para(f'Subject: {section}', 14, True, '003366', 24, 6)
            insert_para(out_doc, h)
            prev_section = section
            prev_topic = None
            prev_subtopic = None

        # Emit Topic heading on topic change
        if topic != prev_topic:
            topic_idx = taxonomy[section]['topics'][topic]['topic_idx'] + 1
            h = make_heading_para(f'Topic {topic_idx}: {topic}', 12, True, '000000', 12, 4)
            insert_para(out_doc, h)
            prev_topic = topic
            prev_subtopic = None

        # Emit Subtopic heading on subtopic change
        if subtopic != prev_subtopic:
            h = make_heading_para(subtopic, 11, True, '003366', 8, 2)
            insert_para(out_doc, h)
            prev_subtopic = subtopic

        # ⛔ IRON RULE — EMIT ORDER IS MANDATORY, NO DEVIATION
        new_q_num += 1

        # Step A — Date label (MANDATORY, always first)
        # v1.18 (GAP-2026-07-27-E): carries the ORIGINAL exam position. new_q_num above
        # is the TAXONOMY position; q['q_num'] is where the question actually sat in the
        # paper. Sorting destroys the latter, and Step 5 needs it to recognise a
        # section-banded question type (MSQ at Q31-40) that carries no instruction
        # phrase of its own. Stamping is idempotent and the field is optional, so
        # pre-v1.18 sorted files remain valid and no re-sort is forced.
        dl = make_date_label_para(stamp_original_q_num(q['date_label'], q.get('q_num')))
        insert_para(out_doc, dl)

        # Step B — Cloned stem (renumbered Q.N)
        stem = copy.deepcopy(q['stem_elem'])
        renumber_stem(stem, new_q_num)
        re_embed_images(stem, src_doc, out_doc)
        insert_para(out_doc, stem)

        # Step C — Cloned body elements (options, tables, images)
        # Strip trailing blank paragraphs first
        body = list(q['body_elems'])
        while body and not (body[-1].text or '').strip():
            ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            has_content = any(True for _ in body[-1].iter(f'{{{ns}}}t'))
            has_table = body[-1].tag.endswith('}tbl') if '}' in body[-1].tag else body[-1].tag == 'tbl'
            if not has_content and not has_table:
                body.pop()
            else:
                break

        for elem in body:
            cloned = copy.deepcopy(elem)
            re_embed_images(cloned, src_doc, out_doc)
            insert_para(out_doc, cloned)

        # Step D — Exactly one blank line
        insert_para(out_doc, make_blank_para())
```

---

## §7 — PIPELINE MECHANICS

### S7-1 — Image re-embedding

```python
def re_embed_images(elem, src_doc, out_doc):
    """
    Re-embed all images in an element with fresh relationship IDs.
    Without this, images silently vanish in the output document.

    v1.12 — DEFECT J: BOTH image mechanisms are now re-pointed.

      <a:blip r:embed>    DrawingML. Covers inline drawings AND floating ones
                          (<wp:anchor>), because both carry a blip.
      <v:imagedata r:id>  Legacy VML. Emitted by older Word versions, by several
                          PDF converters, and by pasted OLE / equation objects.

    Until v1.12 only the first was handled. A VML image's relationship was never
    re-pointed in the output document, which is precisely the failure the §13
    warning describes — "images silently vanish. No error, just empty space." No
    exception, no log line, and the question then reads as TEXT for the rest of the
    pipeline. Verified: the string 'imagedata' appeared 0 times in this file.

    elem.iter() descends into tables, so images inside table cells — the normal
    layout for match-the-following items, multi-panel figures and option grids —
    are re-embedded like any other. (This is the same trap that produced DEFECT I
    in Framework_MockTestAnalyse, where the walk used doc.paragraphs, which in
    python-docx does NOT descend into tables. This function was already correct;
    do not "simplify" it to a paragraph walk.)

    S7-7 is what makes any future regression here self-detecting rather than silent.
    """
    DRAW_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    VML_NS = 'urn:schemas-microsoft-com:vml'

    def _repoint(node, attr):
        old_rid = node.get(attr)
        if old_rid and old_rid in src_doc.part.rels:
            src_rel = src_doc.part.rels[old_rid]
            new_rid = out_doc.part.relate_to(
                src_rel.target_part, src_rel.reltype
            )
            node.set(attr, new_rid)

    for blip in elem.iter(f'{{{DRAW_NS}}}blip'):
        _repoint(blip, f'{{{REL_NS}}}embed')

    for imagedata in elem.iter(f'{{{VML_NS}}}imagedata'):
        _repoint(imagedata, f'{{{REL_NS}}}id')
```

The attribute names differ between the two mechanisms — `r:embed` on `<a:blip>`,
`r:id` on `<v:imagedata>` — which is why the re-point is factored into a helper
rather than duplicated. Both are matched here exactly as `corpus_io.count_image_refs`
matches them, so the S7-7 gate counts precisely what this function is responsible
for carrying. If the two ever diverge, the gate fails closed (HARD STOP) rather
than passing on a document with a missing figure.

### S7-2 — Orphan option auto-repair

```python
def repair_orphan_options(body_elems):
    """
    At emit time: if an option paragraph has no indent, force Pt(18) left indent.
    Accepts 4 forms: (a) Pt(18) indent, (b) table cell, (c) inline drawing,
    (d) OMML formula.
    Uses corpus_io.is_option() — THE shared predicate. Image options included.
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    for elem in body_elems:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        text = ''.join(t.text for t in elem.iter(f'{{{NS}}}t') if t.text)
        # elem is passed so an IMAGE OPTION is indented like any other option.
        if not is_option(text.strip(), elem):
            continue
        # Check if already indented
        pPr = elem.find(f'{{{NS}}}pPr')
        if pPr is not None:
            ind = pPr.find(f'{{{NS}}}ind')
            if ind is not None and ind.get(qn('w:left')):
                continue
        # Force indent
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            elem.insert(0, pPr)
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), '360')  # Pt(18) = 360 twips (1 pt = 20 twips)
        pPr.append(ind)
```

### S7-3 — Non-Latin script preservation

```
Non-Latin text (Hindi/Devanagari, regional scripts) is preserved by
copy.deepcopy() of source XML elements. No font forcing on non-Latin runs.

Acceptable non-Latin fonts:
  Nirmala UI, Mangal, Devanagari Sangam MN, SimSun, SimHei,
  Microsoft YaHei, MS Mincho, MS Gothic, Malgun Gothic, Yu Gothic

Check 1 (validation) accepts these fonts on runs where ord(c) > 0x024F.
```

### S7-4 — Comprehension passage handling

```
RC and Cloze passages: the Row file repeats the full passage above each
sub-question. Preserve this structure exactly — do not deduplicate.
After sorting, sub-questions from the same passage remain consecutive
(same date+session → same sort key cluster).
```

### S7-5 — Input image census (v1.12)

```
WHY THIS EXISTS. Step 3 re-embeds every image with a fresh relationship ID —
the single riskiest image operation in the PYQ pipeline. §13 has warned since
v1.0 that a failure here means "images silently vanish. No error, just empty
space." Until v1.12 there was no detector at the point where that happens:
verified by grep, this file contained no image-count check of any kind, while
Framework_PYQFormat has enforced exact input==output equality (S8-6) since v1.1
for the same class of risk.

The census runs AFTER extract_questions() and BEFORE emit_sorted(). It fixes the
number the output must contain, and it does so from the PARSE — the actual list
of elements the emitter will carry — not from a Q-number regex applied to the
document a second time. A second, independent walk could disagree with the first
and would then either invent a loss or conceal one.
```

```python
def count_elem_image_refs(elem):
    """Count image references inside ONE already-parsed body element.

    Package-level counting is corpus_io.count_image_refs (Cluster I) and MUST NOT be
    re-implemented anywhere. This helper answers a different question: how many
    references live inside a single lxml element the parser is holding in memory —
    a DOM-level operation on an object corpus_io never sees, since corpus_io works on
    packages and paths.

    It matches the SAME two mechanisms as corpus_io.count_image_refs, deliberately:
      <a:blip r:embed>    DrawingML — inline and floating (<wp:anchor>)
      <v:imagedata r:id>  legacy VML
    If the two ever diverged, S7-7 would report a loss that never happened, or —
    far worse — pass a document that really had lost a figure.

    elem.iter() descends into tables. doc.inline_shapes is NEVER used anywhere in
    this spec: it sees only inline body drawings, so it cannot see anchored figures,
    VML objects or anything inside a table cell. A count that can silently run low is
    worse than no count at all, because it makes a broken document look verified.
    """
    A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    V_NS = 'urn:schemas-microsoft-com:vml'
    n = 0
    for blip in elem.iter(f'{{{A_NS}}}blip'):
        if blip.get(f'{{{R_NS}}}embed'):
            n += 1
    for imagedata in elem.iter(f'{{{V_NS}}}imagedata'):
        if imagedata.get(f'{{{R_NS}}}id'):
            n += 1
    return n


def assert_row_file_images_readable(input_path):
    """PRE-FLIGHT — runs on the PATH, BEFORE python-docx opens the Row file.

    ORDER IS LOAD-BEARING, and this was found the hard way. If a relationship points at
    a media part that is not in the package, python-docx raises a bare

        KeyError: "There is no item named 'word/media/image1.png' in the archive"

    from inside zipfile while CONSTRUCTING the Document — so any check placed after
    Document(path) can never run, and the operator gets an opaque traceback from a
    library instead of a sentence naming the defect and the step that owns it.
    Checking the package first is the only position where the named diagnostic is
    reachable.

    Both faults are invisible without a check: Word renders empty space and
    python-docx raises nothing at the point of use.
    """
    _, _, unresolved = corpus_io.count_image_refs(input_path)
    if unresolved:
        raise SystemExit(
            "HARD STOP: the Row file references image(s) that no relationship resolves:\n  "
            + "\n  ".join(f'{part} -> {rid}' for part, rid in unresolved[:5])
            + "\n\nThese images cannot be re-embedded because there is nothing to point at. "
              "This is a Step 1 (PYQ Prepare) packaging defect, not a PYQSort bug — rebuild "
              "the Row file and re-upload. Sorting it anyway would deliver a document with "
              "blank space where the figures belong.")

    dangling = corpus_io.dangling_media_targets(input_path)
    if dangling:
        raise SystemExit(
            f"HARD STOP: the Row file has {len(dangling)} relationship(s) pointing at a "
            f"media part that does not exist in the package: {dangling[:5]}\n"
            "python-docx cannot even open this file — it raises a bare KeyError from "
            "zipfile. Fix in Step 1 (PYQ Prepare) and re-upload.")


def image_census(input_path, src_doc, questions):
    """Establish what the sorted output MUST contain, before anything is emitted.

    Partitions every child of the Row file's body into exactly two buckets:
      CARRIED      — it is some question's stem_elem or one of its body_elems, so
                     emit_sorted() will deep-copy it into the output
      NOT CARRIED  — everything else: content before Q.1, the date-label paragraphs
                     the emitter rebuilds from scratch, module separators
    Images in the second bucket are correctly not carried. Dropping them SILENTLY is
    not correct: it would either hide a genuine loss or trip S7-7 for an entirely
    benign reason. They are reported with their reference count and text prefix.
    (Same discipline as the 'preamble' bucket in corpus_io.map_images_to_questions;
    the equivalent silent drop was DEFECT L in Framework_MockTestAnalyse.)

    PRECONDITION: assert_row_file_images_readable(input_path) has already passed, so
    every reference resolves. The accounting identity below depends on it.
    """
    total_refs, in_parts, unresolved = corpus_io.count_image_refs(input_path)
    body_refs, _, _ = corpus_io.count_image_refs(input_path, body_only=True)

    if unresolved:                      # defence in depth — pre-flight should have caught it
        raise SystemExit(
            "HARD STOP: unresolved image reference(s) reached the census: "
            f"{unresolved[:5]}\nassert_row_file_images_readable() was not run first.")

    carried_ids = set()
    for q in questions:
        carried_ids.add(id(q['stem_elem']))
        for elem in q['body_elems']:
            carried_ids.add(id(elem))

    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    intended = 0
    not_carried = []
    for child in src_doc.element.body:
        n = count_elem_image_refs(child)
        if not n:
            continue
        if id(child) in carried_ids:
            intended += n
        else:
            txt = ''.join(t.text or '' for t in child.iter(f'{{{NS}}}t')).strip()
            not_carried.append({'refs': n, 'text': txt[:60] or '<no text>'})

    accounted = intended + sum(x['refs'] for x in not_carried)
    if accounted != body_refs:
        raise SystemExit(
            "HARD STOP: image accounting does not close.\n"
            f"  body references (package) : {body_refs}\n"
            f"  carried by the parse      : {intended}\n"
            f"  not carried               : {accounted - intended}\n"
            "Every image in the document body must fall into exactly one of those two "
            "buckets. A shortfall means the parser is holding elements that are not "
            "children of the body, or an image lives in a container this walk does not "
            "reach — either way the expected count would be wrong and S7-7 would be "
            "checking against a fiction. Do not proceed.")

    census = {
        'total_refs': total_refs,
        'body_refs': body_refs,
        'header_footer_refs': total_refs - body_refs,
        'intended': intended,
        'not_carried': not_carried,
        'media_parts': len(in_parts),
    }
    report_image_census(census)
    return census


def report_image_census(census):
    """Print the census. NEVER silent about an image that will not be carried."""
    if not census['total_refs']:
        return                      # text-only paper — nothing to say
    print(f"  images: {census['body_refs']} body reference(s) across "
          f"{census['media_parts']} media part(s) — {census['intended']} will be carried "
          f"into the sorted output")
    if census['header_footer_refs']:
        print(f"  note: {census['header_footer_refs']} header/footer/footnote image(s) in "
              "the Row file. These are page furniture, not question figures; the sorted "
              "document is built fresh and does not carry them.")
    for item in census['not_carried']:
        print(f"  WARN: {item['refs']} image reference(s) NOT carried — the element belongs "
              f"to no question: \"{item['text']}\"")
```

### S7-6 — Size governor on write (v1.12)

```
WHY STEP 3 GOVERNS SIZE. Step 3 is the first step in the pipeline to hold real
image bytes: Step 1 emits only 300×200 red placeholder PNGs, and Step 2b works
from text. The Sorted file it produces is uploaded to the Drive PYQ folder and is
then FETCHED BACK by Step 4 (PYQCount) and Step 5 (PYQExtract) through a
connector that refuses any download above 10 MiB. An ungoverned Sorted file is
therefore the thing that blocks Steps 4 and 5 later — and it blocks them
mid-batch, which is exactly the 2026-07-24 incident: 6 of 7 pending papers above
the cap, discovered at batch 6 of a run.

Governing here is Layer 1 PREVENTION. The upload lane in Steps 4/5 and the
PYQCompress trigger are Layer 2 remediation for files that already exist.

CONSTANTS ARE THE ENGINE'S, NOT THIS SPEC'S:
  blueprint_core.DRIVE_CAP    10,485,760  connector refuses above this (measured)
  blueprint_core.SIZE_BUDGET   9,437,184  governor target — 10% margin under the cap
  blueprint_core.TIER_LADDER   T1..T4     deterministic; T4 is the floor
Never restate a threshold in this file. One definition, every importer.

FLOOR EXCEEDED IS NOT A HALT. If the ladder reaches T4 (q80 / 200 DPI at display
size) and the file is still over budget, the file is DELIVERED with a WARN and a
flag. Going below the floor would damage the figures, and a legitimately huge
paper must not block its own delivery. The consequence is stated to the operator,
not hidden: Steps 4/5 will fall back to the upload lane for that paper.
```

```python
def write_sorted_document(out_doc, raw_out, out_file, census):
    """Save, size-govern, and prove nothing was lost. Returns the write report.

    ORDER IS LOAD-BEARING — govern FIRST, gate SECOND (S7-7). The gate has to run on
    the bytes that are actually delivered, so that governor-induced loss is inside its
    scope rather than outside it.
    """
    out_doc.save(raw_out)
    raw_size = os.path.getsize(raw_out)

    ok, report, log = corpus_io.optimize_docx(raw_out, out_file, budget=bc.SIZE_BUDGET)

    if report['tier'] == 'T0':
        # optimize_docx returns WITHOUT writing dst when the source is already under
        # budget — nothing was re-encoded, so there is no destination file to deliver.
        # Materialising it is the caller's job. Missing this detail is a
        # FileNotFoundError at present_files on the ORDINARY path (most papers are
        # already small), which is why it is spelled out rather than left to the reader.
        shutil.copy2(raw_out, out_file)
        parity = 'SKIP — already under budget, bytes untouched'
    else:
        # 17 invariants (verified by execution against corpus_io.docx_invariants, not
        # quoted from the change plan, which says 19) including the extracted-text SHA256,
        # the OMML equation count and per-image pixel dimensions. Byte size and "it opens
        # in Word" are NOT evidence of correctness: a governor that quietly dropped a
        # figure produces a smaller file that opens perfectly. allow_resample is True only
        # for the tiers that downscale by design (T2..T4); T1 re-encodes quality only and
        # must preserve every pixel dimension.
        corpus_io.assert_docx_parity(
            raw_out, out_file,
            allow_resample=report['tier'] not in ('T0', 'T1'))
        parity = 'PASS'

    final_size = os.path.getsize(out_file)
    print(f"  size: {raw_size:,} -> {final_size:,} bytes "
          f"(tier {report['tier']}, budget {bc.SIZE_BUDGET:,}) — parity {parity}")
    for base, before, after, how in log:
        if after != before:
            print(f"    {base}: {before:,} -> {after:,} ({how})")

    over_cap = final_size > bc.DRIVE_CAP
    over_budget = final_size > bc.SIZE_BUDGET

    if over_cap:
        print(f"  ⚠️  WARN: sorted file is {final_size:,} bytes, above the "
              f"{bc.DRIVE_CAP:,}-byte Drive download cap. The governor reached its floor "
              f"(tier {report['tier']}) and stopped — going lower would damage the "
              "figures. DELIVERED ANYWAY: a legitimately large paper must not block its "
              "own delivery.\n"
              "      Consequence: Step 4 (PYQCount) and Step 5 (PYQExtract) cannot FETCH "
              "this paper from Drive — corpus_io.fetch_drive_docx will raise "
              "TransportFallback and it will be requested by chat upload instead. Nothing "
              "is lost; that run simply takes the upload lane for this file.")
    elif over_budget:
        print(f"  WARN: sorted file is {final_size:,} bytes — under the "
              f"{bc.DRIVE_CAP:,}-byte cap, so Drive fetch still works, but above the "
              f"{bc.SIZE_BUDGET:,}-byte budget, so the 10% safety margin is gone.")

    return {'raw_bytes': raw_size, 'final_bytes': final_size, 'tier': report['tier'],
            'parity': parity, 'under_budget': not over_budget,
            'fetchable_from_drive': not over_cap, 'floor_exceeded': not ok}
```

### S7-7 — Image survival gate (v1.12) — HARD STOP

```
DEFECT M. Modelled on Framework_PYQFormat S8-6, with the same discipline: EXACT
input==output equality, never a tolerance. Surfaced to the operator as CHECK 10.

Runs LAST, on the delivered file, AFTER the governor (S7-6) — so it covers loss
from re-embedding, loss from the emit loop, and loss caused by the governor
itself, in one assertion. corpus_io.assert_docx_parity already checks the
governor's own work; per the anti-drift principle the pipeline asserts the
end-to-end property independently rather than trusting a module's self-report.

The expected value is census['intended'] from S7-5 — the images belonging to
questions that the emitter carried. Images legitimately not carried were already
reported by the census and are NOT folded into the expectation, so a benign drop
can never be mistaken for survival and a real loss can never hide behind one.
```

```python
def assert_image_survival(input_path, out_file, census):
    """CHECK 10 — the delivered file must carry every image its questions had.

    A shortfall here is the failure this spec has warned about since v1.0 and never
    detected: the document opens cleanly, the text is complete, the question reads
    normally — and a figure is simply gone. Downstream, Step 5 then classifies that
    question TEXT instead of FIGURAL and the format distribution that drives Step 7
    generation is quietly wrong. There is no later gate that would notice.
    """
    out_body, out_parts, unresolved = corpus_io.count_image_refs(out_file, body_only=True)

    if unresolved:
        raise SystemExit(
            "HARD STOP — IMAGE SURVIVAL (CHECK 10 / S7-7): the sorted output has "
            f"{len(unresolved)} image reference(s) that resolve to no relationship: "
            f"{unresolved[:5]}\n"
            "re_embed_images() did not re-point them. Word renders these as empty space.")

    dangling = corpus_io.dangling_media_targets(out_file)
    if dangling:
        raise SystemExit(
            "HARD STOP — IMAGE SURVIVAL (CHECK 10 / S7-7): the sorted output has "
            f"{len(dangling)} relationship(s) pointing at a media part that is not in the "
            f"package: {dangling[:5]}")

    if out_body != census['intended']:
        in_parts = corpus_io.count_image_refs(input_path, body_only=True)[1]

        def _stem(p):
            # The governor may rename a part (.png -> .jpeg) when it re-encodes, so parts
            # are compared by name without extension. Comparing full targets would report
            # every re-encoded image as missing.
            return os.path.splitext(os.path.basename(p))[0]

        missing = sorted({_stem(p) for p in in_parts} - {_stem(p) for p in out_parts})
        raise SystemExit(
            "HARD STOP — IMAGE SURVIVAL (CHECK 10 / S7-7).\n"
            f"  expected {census['intended']} body image reference(s), found {out_body}\n"
            + (f"  media part(s) in the Row file but absent from the output: {missing[:5]}\n"
               if missing else "")
            + "  Usual causes, in order of likelihood:\n"
              "    1. an image mechanism re_embed_images() does not re-point (S7-1 handles\n"
              "       <a:blip r:embed> and <v:imagedata r:id> — a third would need adding\n"
              "       there AND in corpus_io.count_image_refs, never in only one)\n"
              "    2. an element dropped from body_elems by the parser (S3-2)\n"
              "    3. the governor lost a part — impossible without assert_docx_parity\n"
              "       also failing, so check that it actually ran (S7-6)\n"
              "  Do not deliver. A missing figure is invisible downstream: the question\n"
              "  simply reads as text and Step 5 classifies it TEXT instead of FIGURAL.")

    print(f"  CHECK 10 image survival: PASS "
          f"({out_body}/{census['intended']} body image reference(s) carried)")
    return out_body
```

---

## §8 — VALIDATION (10 checks — iterate until ALL PASSED)

```
Every Sorted file must pass all 10 checks before delivery.
session_keyword is read from exam_config.json for Check 3.
CHECK 10 (v1.12) runs on the FINAL, size-governed file — see the §9 write path.

CHECK 1 — BODY FONT & TIER SIZES
  All body runs effectively Arial 11pt (with font-inheritance and non-Latin fallback).
  Subject 14pt. Topic 12pt. Subtopic 11pt.
  DI table cells exempted (preserve source font size, typically 9pt).

CHECK 2 — Q-COUNT PARITY
  Input Q-count == Output Q-count strictly. Every question exactly once.
  For marker mode: count per module (Q.1 appears once per module), sum modules.

CHECK 3 — DATE LABEL: PRESENCE, POSITION, FORMAT & STYLING
  HARD FAIL if date-label count ≠ Q-count.
  Every label matches the DYNAMIC pattern built from session_keyword.
  Session part is OPTIONAL — both formats are valid:
    WITH session:    ^\[\d{1,2}-[A-Za-z]{3}-\d{4}\s+<session_keyword>\s+\d+\]$
    WITHOUT session: ^\[\d{1,2}-[A-Za-z]{3}-\d{4}\]$
  The build_date_label_re() regex handles both via optional group.
  Examples:
    SSC:     [18-Jan-2025 Shift 1]
    Banking: [14-Oct-2023 Slot 3]
    GATE:    [09-Feb-2025]          (no session — single-session exam)
    UPSC:    [02-Jun-2024]          (no session)
  Styling: Arial 11pt bold navy #003366, non-italic, right-aligned.
  Position: each label immediately precedes its Q.N stem — zero paragraphs between.

CHECK 4 — OPTIONS INDENTED (NAT-aware)
  For MCQ questions (has_options=True):
    ≥ options_count × mcq_count option paragraphs
    (options_count from exam_config, typically 4 or 5)
  For NAT questions (has_options=False):
    0 option paragraphs expected — exempted from this check.
  mcq_count = total Q-count − nat_count.
  Uses corpus_io.is_option() — THE shared predicate. Image options included.
  Accept: (a) Pt(18) indent, (b) table cell, (c) inline drawing, (d) OMML formula.

CHECK 5 — SEQUENTIAL NUMBERING
  Q-lines read Q.1, Q.2 … Q.N in body order. No gaps, no duplicates.

CHECK 6 — SUBTOPIC GROUPING
  Subtopic heading count == number of distinct (Subject, Topic, Subtopic) triples used.
  Every heading under correct parent Topic and Subject.
  Same subtopic name under different Topics is valid (not a violation).

CHECK 7 — TAXONOMY MEMBERSHIP
  Every Subject, Topic, Subtopic heading text exists verbatim in the Analysis docs.

CHECK 8 — SORT ORDER
  Sequence matches (subject_idx ASC, topic_idx ASC, subtopic_idx ASC,
  year DESC, month DESC, day DESC, session ASC, orig_q_num ASC).

CHECK 9 — NO METADATA LEAKAGE
  No paragraphs matching Answer:, Explanation:, Solution:, Question ID,
  Chosen Option, Correct Answer, Section:, === (module separators).

CHECK 10 — IMAGE SURVIVAL (v1.12)
  Body image references in the delivered file == census['intended'] from S7-5.
  EXACT equality, never a tolerance — the same discipline as PYQFormat S8-6.
  Mismatch → HARD STOP naming the missing media parts (S7-7).
  Also HARD STOP on any unresolved rId or dangling media relationship in the
  output: both render as empty space rather than raising anything.
  Counting is delegated to corpus_io.count_image_refs — <a:blip r:embed> AND
  <v:imagedata r:id>, across every story part. doc.inline_shapes is NEVER used:
  it cannot see anchored, VML, table-cell or header images, so it under-counts
  silently and would make a broken document look verified.
  Runs on the FINAL file, AFTER the S7-6 governor, so governor-induced loss is
  inside its scope. Images legitimately not carried (before Q.1, or inside a
  date-label paragraph the emitter rebuilds) were reported by the S7-5 census
  and are NOT folded into the expected count.
  This is the only check that runs on the package rather than the DOM.
```

---

## §9 — EXECUTION MODEL

```
SINGLE SCRIPT, 4 TOOL CALLS, NO "CONTINUE":

  CALL 1 — create_file: Write complete sort_pipeline.py containing:
    1. Taxonomy dictionary (loaded from Analysis docs)
    2. CLASSIF dictionary (from pre-build classification table)
    3. Parser (Row file → question blocks), preceded by the S7-5 pre-flight
    4. Image census (S7-5) — runs after the parse, before the emit
    5. Sorter (8-field sort key)
    6. Emitter (headings + questions via insert_para)
    7. Write path: save → size governor (S7-6) → parity assert
    8. Validator (all 10 checks, CHECK 10 = image survival S7-7)
    9. Delivery (shutil.copy2 to /mnt/user-data/outputs/)

  CALL 2 — bash_tool: Run sort_pipeline.py
    → Parse + census + classify + sort + emit + govern + validate + deliver

  CALL 3 — bash_tool: Verify output
    → Q-count, heading counts, date-label count, image count vs census

WRITE PATH (v1.12 — ORDER IS LOAD-BEARING):

  assert_row_file_images_readable(INPUT_DOC)      # S7-5 PRE-FLIGHT — before Document()
  src_doc   = Document(INPUT_DOC)
  questions = extract_questions(src_doc, ...)      # S3-2
  census    = image_census(INPUT_DOC, src_doc, questions)   # S7-5, fixes the expectation
  emit_sorted(out_doc, sorted_questions, ...)      # S6-4
  write     = write_sorted_document(out_doc, RAW_OUT, OUT_FILE, census)  # S7-6 govern+parity
  run CHECK 1..9 on OUT_FILE
  assert_image_survival(INPUT_DOC, OUT_FILE, census)        # S7-7 = CHECK 10
  shutil.copy2(OUT_FILE, FINAL_OUT)
  present_files(FINAL_OUT)

  The governor runs BEFORE validation so that every check — including CHECK 10 —
  runs on the bytes actually delivered. Validating the pre-governor file and then
  shipping a different one would leave the governor's own work unverified by
  anything except its internal parity assert.
  This adds NO tool calls: the governor is a function call inside CALL 2.

  CALL 4 — present_files: Deliver sorted .docx

DELIVERABLE SET CONTRACT (CLOSED):
  The present_files call MUST contain EXACTLY 1 file:
    [ExamCode]_<date-range>_Sorted_Q1-Q<N>.docx
  and NOTHING ELSE. This is an exhaustive, closed list.

  DO NOT include in present_files:
    ✗ sort_pipeline.py (execution script)
    ✗ Any working .docx from /home/claude/work/
    ✗ Any JSON, log, or intermediate files
    ✗ The input Row file

  PRE-DELIVERY CHECK: Before calling present_files, verify:
    1. Exactly 1 file path in the argument list
    2. File is the FINAL_OUT path (/mnt/user-data/outputs/...)
    3. All 10 validation checks PASSED on this file
    4. FINAL_OUT is a copy of the GOVERNED file (OUT_FILE), never of RAW_OUT

If script fails: fix and re-run within the 4-call budget.
If validation fails: iterate until PASSED, then deliver.

MANDATORY CLASSIF CROSS-CHECK:
  After writing the CLASSIF dict in sort_pipeline.py, verify every entry
  against the pre-build classification table before executing. Any mismatch →
  fix the code before running. Never rewrite from memory — copy exactly.

INPUT/OUTPUT PATHS:
  INPUT_DOC  = "/mnt/user-data/uploads/<Row-filename>.docx"
  RAW_OUT    = "/home/claude/work/<Sorted-filename>.raw.docx"   (v1.12 — pre-governor)
  OUT_FILE   = "/home/claude/work/<Sorted-filename>.docx"       (governed + validated)
  FINAL_OUT  = "/mnt/user-data/outputs/<Sorted-filename>.docx"

  RAW_OUT is what out_doc.save() writes and is the LEFT side of the parity assert.
  It is a working file: never validated, never delivered, never copied to outputs.
```

---

## §10 — EDGE CASES

```
EC-S1: ROW FILE WITH FEWER QUESTIONS THAN EXPECTED
  Some papers may have <100 questions (partial paper, missing section).
  Process whatever is present. Q-count validation targets the actual count,
  not the expected count from exam_config.

EC-S1b: ROW FILE WITH MORE QUESTIONS THAN THE CURRENT PATTERN (v1.9)
  The mirror of EC-S1, and the more dangerous direction because the surplus
  questions have no configured home. A previous-era paper can exceed the current
  exam_config total — e.g. a 100-question legacy paper against a 60-question
  current pattern leaves Q.61-Q.100 outside every section range.
  Before v1.9 get_section_by_q_range returned None for these, the None was stored
  unguarded, and the questions silently failed every downstream taxonomy lookup:
  a 40% data loss on that file with no operator-visible signal.
  Resolution: they receive the OUT_OF_PATTERN sentinel (never None), are classified
  against the FULL taxonomy rather than a single section's slice (the narrow, gated
  exception to RULE 4 in §4 — RULE 4 presupposes a structural section exists, and
  these have none), carry pattern_era='out_of_pattern', and are reported by
  report_pattern_era() with their Q-range and the mix consequence.
  This is NOT an error condition. A corpus spanning several exam patterns is the
  normal, intended state — the variety of question types and concepts in old papers
  is the reason they are retained. Only the SILENCE was the defect.
  See also: Framework_PYQAnalyse EC-P9 (same case at scan time) and
  Framework_Blueprint v1.36 §2 S2-3 (same case at allocation time).

EC-S2: MODULE SEPARATOR NOT MATCHING SECTION NAME
  Marker mode: === Subject === text might not exactly match Analysis doc section name.
  Resolution: fuzzy match against taxonomy section names. If ambiguous → classify
  based on question content within that module.

EC-S3: DUPLICATE Q-NUMBERS (marker mode)
  Tier 2 style: Q.1 appears once per module. Parser tracks current_module to
  disambiguate. CLASSIF key = (module_name, q_num).

EC-S4: MULTI-PAPER ROW FILES
  Row file combines questions from multiple dates. Filename uses date range.
  CLASSIF key = (module_name, date_label, q_num) to avoid collisions.
  Detect: if all date labels identical → 2-tuple key; else → 3-tuple key.

EC-S5: IMAGE-ONLY QUESTIONS
  Question stem is an image with no text. Classification uses figural fallback
  subtopic for the section. Image re-embedded via re_embed_images().

EC-S6: OMML FORMULA IN OPTIONS
  Options contain <m:oMath> elements. Accept as valid option form (Check 4 form d).
  Preserve verbatim via deep-copy.

EC-S7: ASSERTION-REASON LONG OPTIONS
  Options like "Both A and R are true and R is the correct explanation of A"
  are valid plain-text options despite length. Do not treat as stem continuation.

EC-S8: MULTI-PARAGRAPH STEMS
  Statement I / Statement II blocks span multiple bold paragraphs after Q.N.
  Detection: bold + not-date + not-option + not-next-Q → stem continuation.
  Include in body_elems in source order.

EC-S9: DI TABLE PRESERVATION
  Tables preserved with original font size (typically 9pt). Do NOT upscale.
  Check 1 exempts table cells from the Arial 11pt requirement.

EC-S10: MISSING DATE LABEL
  If parser finds Q.N without a preceding date label → raise ValueError.
  Error message names Step 1 (PYQ Prepare) as the fix location:
    "Q.{N} has no date label. Step 1 must emit a date label before every
     question in format: [DD-Mon-YYYY] or [DD-Mon-YYYY {session_keyword} N]."
  Step 1 FORMAT CONTRACT: every Row file must have a date label above every
  question. Session part is optional — omitted for single-session exams.

EC-S11: NON-LATIN SCRIPTS (Hindi/Devanagari)
  Preserved by deep-copy. Font fallback accepted in Check 1.
  Classification uses English portion of bilingual stems.

EC-S12: TOPIC NUMBER GAPS
  If paper has questions from Topic 1 and Topic 3 but not Topic 2, headings read
  "Topic 1: ..." and "Topic 3: ..." — gaps in numbering are CORRECT. Do NOT
  renumber topics to close gaps. Topic N uses ABSOLUTE 1-indexed position from
  Analysis doc.

EC-S13: BLANK LINES BETWEEN QUESTIONS
  Strip trailing blank paragraphs from source question block. Emit exactly ONE
  fresh blank paragraph after each question via make_blank_para() + insert_para().
  Do NOT clone source blank — always emit fresh.

EC-S14: NAT QUESTIONS (NO OPTIONS)
  GATE, banking, and some other exams have Numerical Answer Type questions with
  ZERO selectable options — only a stem. These are valid questions.
  Parser sets has_options=False. Check 4 exempts them from options count.
  Classification, sorting, heading emission, and date labels are identical to MCQ.
  The body_elems for NAT questions may include an answer-entry instruction
  paragraph (e.g. "Enter your answer as an integer") — preserve verbatim.

EC-S15: SINGLE-SESSION EXAMS
  GATE, UPSC, state PSC exams have one session per date.
  Step 1 omits session from date label entirely: [DD-Mon-YYYY].
  parse_date_label() defaults session to 1. Sort key field 7 becomes
  a no-op tiebreak. This is correct by design — no special handling
  needed in PYQSort.

EC-S16: LEGACY VML IMAGES (v1.12)
  Older Word versions, several PDF converters, and pasted OLE / equation objects
  emit <v:pict><v:imagedata r:id="..."> instead of DrawingML <a:blip r:embed>.
  Before v1.12 re_embed_images() matched only the blip form, so a VML image's
  relationship was never re-pointed and the image vanished from the output with
  no error — exactly the failure §13 warns about. S7-1 now re-points both, and
  S7-5/S7-7 count both, so the same class of miss is a HARD STOP rather than an
  empty rectangle. A Row file may contain both mechanisms at once; this is normal
  and needs no operator action.

EC-S17: SORTED OUTPUT STILL OVER BUDGET AT THE LADDER FLOOR (v1.12)
  An image-dense paper can exceed blueprint_core.SIZE_BUDGET even after the
  governor reaches tier T4 (q80 / 200 DPI at display size). T4 is the FLOOR —
  encoding below it damages the figures the whole pipeline exists to preserve.
  Resolution: DELIVER + WARN + FLAG. Never HALT. The file is valid and complete;
  it is only awkward to transport. The WARN states the consequence explicitly —
  Steps 4/5 cannot fetch it from Drive and will request it by chat upload
  (corpus_io.fetch_drive_docx raises TransportFallback, which is a routing signal,
  not an error). Blocking delivery here would trade a transport inconvenience for
  actual data loss.

EC-S18: IMAGES THAT BELONG TO NO QUESTION (v1.12)
  A Row file may carry a logo, a paper-header graphic, or an instruction figure
  before Q.1, or an image in a header/footer part. These are page furniture, not
  question figures, and the sorted document — built fresh — does not carry them.
  That is correct. What is NOT acceptable is dropping them silently: it would
  either mask a real loss or fail S7-7 for a benign reason. S7-5 partitions them
  into the not-carried bucket and REPORTS each one with its reference count and
  text prefix, and excludes them from census['intended'].
  If the operator recognises a genuine question figure in that report, the fix is
  in Step 1 (PYQ Prepare) — the image is sitting above the Q.N line that owns it.

EC-S19: UNRESOLVED OR DANGLING IMAGE RELATIONSHIP IN THE ROW FILE (v1.12)
  An rId with no matching relationship, or a relationship whose media part is not
  in the package. Both are Step 1 packaging defects and both are invisible without
  a check: Word renders empty space and python-docx raises nothing.
  Resolution: HARD STOP at the S7-5 PRE-FLIGHT, on the PATH, before python-docx is
  allowed to open the file — naming the offending part and rId and pointing at Step 1
  as the fix location.
  The position is not cosmetic. A missing media part makes python-docx raise a bare
  KeyError from zipfile while CONSTRUCTING the Document, so a check placed after
  Document(path) can never run and the operator sees a library traceback instead of a
  sentence naming the defect. Verified by construction.
  Sorting it anyway would deliver a document that looks complete and is not.

EC-S20: ANALYSIS DOC READ AS PLATFORM-EXTRACTED TEXT (v1.15 / GAP-2026-07-25-003)
  The Analysis doc lives in the project's Files section, uploaded once after
  PYQApprove (Step 2c). The Claude Projects platform stores an uploaded .docx there
  as extracted Markdown TEXT, KEEPING the original filename and .docx extension.
  Measured on the first real exam: the chat attachment is a 40,882-byte OOXML
  package; the same file in project Files is 12,911 bytes of Markdown.
  This text form is therefore the PRIMARY and NORMAL runtime input at Steps 3, 4, 5
  and 6 — not a fallback and not a degraded mode.
  Resolution: corpus_io >= v1.2 detects the ingest form by CONTENT (never by
  extension — the .pdf in the same project is a Zip page-bundle under its .pdf name,
  so the extension is not evidence of the container) and scans the text form with
  _scan_text(), which emits the identical structure as the OOXML scanner.
  verify_analysis_doc() still asserts all three self-declarations, and S1-0b still
  asserts the fingerprint against the lock — the text form is admitted THROUGH both
  gates, never around them.
  NO OPERATOR ACTION. Do NOT attach the Analysis doc to chat: discover_analysis_doc()
  de-duplicates by name and the project copy wins, so an attachment under the
  canonical name is silently ignored and one under a different name raises "2
  Analysis docs found". Do not warn about the ingest form; report it in the S1-3
  inventory and continue.
  ONLY an UNRECOGNISED form halts, and it halts loudly and by name — never with a
  library traceback and never as a best-effort parse.
  TWO THINGS THAT ARE NOT TOLERATED, both of which would otherwise be silent:
    • a '|' anywhere in a subject, topic or subtopic name. In the text form '|' is
      the cell separator, so the name is split, the remainder is swallowed as the
      count column, and the declared totals STILL AGREE — D1, D2 and D3 all pass on
      a truncated name. corpus_io hard stops on any table whose rows differ in cell
      count, and write_analysis_doc() refuses to emit such a name at Step 2c.
    • an extraction grammar this version does not recognise. The parse yields no
      subject heading and the reader stops naming the grammar change explicitly.
      Report it as a GAP-2026-07-25-003 follow-up; do NOT work around it.

EC-S21: TAXONOMY SOURCED FROM THE APPROVAL RECORD (v1.16)
  reconcile_taxonomy >= v1.3 records the approved taxonomy INSIDE
  [ExamCode]_approval_record.json, beside the fingerprint that validates it. That
  file is JSON, which the platform stores byte-for-byte, so on this path no Word
  document is read and no extraction grammar is involved at all — EC-S20 simply
  cannot arise. Display names are exact rather than merely slug-equivalent, which
  the fingerprint alone could never guarantee.
  load_taxonomy() prefers it automatically. Nothing to configure.
  PRE-1.3 RECORDS ARE NOT A FAULT. Every exam approved before this carries a
  fingerprint and no taxonomy; those take the Analysis-doc path, fully gated, and
  need no re-run. S1-3 reports which path was taken. An exam moves to the preferred
  path the next time it goes through PYQApprove, which is RECONCILIATION — it reads
  taxonomy_draft.json, rewrites only the record, and cannot change a locked taxonomy.
  WHAT STILL HALTS: a record that carries a taxonomy and does not agree with itself.
  Fingerprint vs taxonomy, declared counts vs assembled counts, or a repeated name —
  the last of which the fingerprint cannot catch, since it is computed over the same
  duplicated triples and so agrees with itself. Never half-believed; always named.
```

---

## §11 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  Trigger parsing and file inventory
  Section detection (auto: markers vs Q-range)
  Question extraction (Q patterns, date label patterns, option patterns)
  Date label parsing (dynamic regex from session_keyword)
  Option detection (5-pattern OPT_PATTERNS aligned with Step 5 E-3)
  NAT question handling (has_options flag, Check 4 exemption)
  OMML renderer
  Classification rules 1-6
  Sort key (8 fields)
  Heading format (Step 5 E-1 contract)
  Page size selection (from exam_config, default A4)
  All OOXML helpers (insert_para, make_heading_para, make_date_label_para, etc.)
  Image re-embedding (DrawingML blip AND legacy VML imagedata)
  Input image census and the not-carried report (S7-5)
  Size governor on write + parity assert (S7-6) — thresholds from the engine
  Image survival gate (S7-7 / CHECK 10)
  Orphan option repair (using 5-pattern is_option)
  Non-Latin script preservation
  10-check validator (with configurable session_keyword and NAT-awareness)
  4-call execution model
  All 20 edge cases (EC-S1 … EC-S19, plus EC-S1b)

EXAM-SPECIFIC (loaded at runtime from project files):
  Taxonomy (from Analysis docs)
  Section names, topic names, subtopic names (from Analysis docs)
  Subject order (from exam_config.json)
  Section boundaries / marker mode (from exam_config.json)
  Session keyword: Shift/Slot/Phase/Paper/Session (from exam_config.json)
  Page size: A4/Letter (from exam_config.json)
  Options count per question (from exam_config.json)
  Question types: MCQ/NAT/MSQ (from exam_config.json)
  Classification precedents (from question content + universal rules)

PROOF:
  SSC CGL Tier 1: 4 sections, Q-range mode, Shift, 100 Q/paper, all MCQ
  SSC CGL Tier 2: 5 sections, marker mode, Shift, 150 Q/paper, all MCQ
  GATE CS:        1 section,  Q-range mode, Session, 65 Q/paper, MCQ+NAT
  IBPS PO:        5 sections, marker mode, Slot, 100 Q/paper, all MCQ
  UPSC CSE:       2 papers,   Q-range mode, Paper, 100 Q/paper, all MCQ
  Same spec handles all — zero exam-specific code in framework.

STEP 1 FORMAT CONTRACT (prerequisite):
  Step 1 (PYQ Prepare) normalises all exam-specific raw formats into:
    Date labels:  [DD-Mon-YYYY <session_keyword> <N>] (with session)
                  [DD-Mon-YYYY] (without session — single-session exams)
                  Session part is OPTIONAL. PYQSort handles both forms.
    Q-numbering:  Q.<N> (continuous — Step 1 always renumbers continuously)
    Options:      Canonical "N. text" format, or none for NAT
    Month names:  3-char English abbreviations (Jan, Feb, ...)
  PYQSort trusts this contract. Violations are Step 1 bugs, not PYQSort bugs.
```

---

## §12 — DEFINITION OF DONE

```
☐ 1.  All Analysis docs loaded from project knowledge
☐ 2.  exam_config.json loaded and validated
☐ 3.  Session keyword and page size read from exam_config
☐ 4.  Section detection mode determined (markers or Q-range)
☐ 5.  Row file parsed — all questions extracted with date labels
☐ 6.  NAT questions identified (has_options=False)
☐ 7.  OMML rendered for all math-containing stems
☐ 8.  Pre-build classification table completed for all questions
☐ 9.  CLASSIF dictionary matches pre-build table exactly
☐ 10. sort_pipeline.py written with all 9 components
☐ 11. Script executed successfully
☐ 12. All 10 validation checks PASSED
☐ 13. Output Q-count == Input Q-count
☐ 14. All headings present in taxonomy (Check 7)
☐ 15. Sort order verified (Check 8)
☐ 16. No metadata leakage (Check 9)
☐ 17. S7-5 pre-flight run BEFORE Document() opened; census run BEFORE the emit,
       and every not-carried image reported
☐ 18. Size governor run on write; parity asserted or legitimately SKIPped (S7-6)
☐ 19. Image survival gate PASSED on the FINAL governed file (S7-7 / Check 10)
☐ 20. If the governor floor was exceeded: file DELIVERED, WARN shown, upload-lane
       consequence stated to the operator — never halted (EC-S17)
☐ 21. Sorted .docx delivered via present_files
☐ 22. Deliverable set closed: EXACTLY 1 file in present_files call
       (no scripts, no intermediates, no input files, no RAW_OUT)
☐ 23. Taxonomy SOURCE and ingest form identified and REPORTED in the S1-3
       inventory, and the taxonomy loaded through corpus_io.load_taxonomy() —
       never by prose, never by a bare Document(path) open, never loaded twice
       in one step (EC-S20, EC-S21)

POST-DELIVERY:
  User downloads sorted .docx → uploads to Google Drive PYQ folder.
  After ALL papers sorted: run Step 4 PYQCount PYQ: <<Drive link>> to fill
  PYQ counts into Analysis docs.
  v1.12 — if S7-6 flagged the file as above the Drive download cap, say so in the
  handover as well as in the run output. The file still belongs in the Drive folder
  (that is where the corpus lives and where enumeration finds it); Steps 4/5 will
  simply request that one paper by chat upload instead of fetching it. An operator
  who is told this once does not spend a batch run diagnosing it.

POST-DELIVERY FOOTER (MANDATORY after present_files):
  Render the standardized visual delivery footer as the LAST element in the response.
  Follow Framework_DeliveryFooter.md for footer type (F2 step-complete — always for
  PYQSort since it has no batches), file badge (Use locally), and next-step reference.
```

---

## §13 — CRITICAL WARNINGS

```
⚠️ NEVER infer a container format from a file extension.
   A file named .docx in /mnt/project/ is extracted TEXT, not an OOXML package;
   a file named .pdf there is a Zip page-bundle. The platform preserves the NAME
   through every transform, so the name is evidence of nothing. Detect from
   CONTENT. This is what made GAP-2026-07-25-003 a P0 across every exam, and it is
   why the "no file found" diagnostic that anticipated it could never fire: the
   file was never missing, only transformed.

⚠️ NEVER use body.append() — ALWAYS use insert_para()
   body.append() places content after <w:sectPr>, making it invisible.
   This is the #1 most dangerous bug. Every element (headings, date labels,
   stems, options, tables, blanks) MUST use insert_para().

⚠️ NEVER use doc.add_paragraph() for any content
   It conflicts with insert_para() when mixed. Build ALL elements as raw
   OOXML via OxmlElement.

⚠️ ALWAYS use Inches() for page dimensions
   Raw integers (12240, 15840) are DXA values, not EMU. They produce
   a corrupt document with hundreds of micro-pages.

⚠️ ALWAYS re-embed images with fresh rIds — BOTH mechanisms
   Without re_embed_images(), images silently vanish. No error, just empty
   space where the image should be.
   v1.12: this applies to <a:blip r:embed> (DrawingML) AND <v:imagedata r:id>
   (legacy VML). Handling only the first is what DEFECT J was: every VML image
   produced exactly the failure this warning describes, for years, silently.
   If a third mechanism is ever found, it must be added to S7-1 AND to
   corpus_io.count_image_refs in the same change — never to only one, or the
   gate will certify a document it can no longer see all of.

⚠️ NEVER count images with doc.inline_shapes
   It sees only inline body drawings. Anchored figures, VML objects, images
   inside table cells and header/footer images are all invisible to it, so it
   under-counts SILENTLY. A count that can run low is worse than no count at
   all — it makes a broken document look verified. Count via
   corpus_io.count_image_refs, which reads the package XML.

⚠️ NEVER re-implement a corpus_io function in this spec
   Image counting, extraction, mapping, the governor and the parity assert live
   in corpus_io (Clusters I/J); the thresholds and the tier ladder live in
   blueprint_core (Cluster H). Steps 1, 3, 4, 5 and PYQCompress all consume
   them. A local copy produces ZERO drift signal until the two copies disagree,
   which is precisely the failure that required MockTestAnalyse v2.27 and
   PYQAnalyse v2.20. Call it, or write a thin forwarding adapter — nothing else.

⚠️ NEVER deliver RAW_OUT, and never validate the pre-governor file
   RAW_OUT is the left side of the parity assert and nothing else. Checks 1-10
   run on the governed OUT_FILE, which is what FINAL_OUT is copied from. Shipping
   bytes that were never validated is the whole class of bug S7-6/S7-7 exist to
   close.

⚠️ NEVER set explicit LEFT alignment on headings
   Leave alignment as None (unset). Explicit LEFT adds a <w:jc> element
   that should not be there.

⚠️ ALWAYS rebuild date labels from scratch
   Never clone source date label paragraphs. Always use make_date_label_para()
   to ensure consistent styling regardless of source formatting.

⚠️ NEVER skip the date label emit
   If q['date_label'] is empty → raise ValueError. Fix Step 1.
   A missing date label is a Step 1 format violation, not a valid state to skip.

⚠️ Q_PATTERNS and OPT_PATTERNS MUST stay aligned with Step 5 E-2 / E-3
   Any change to pattern lists here MUST be mirrored in Framework_MockTestAnalyse.md
   and Framework_PYQAnalyse.md. Contract violation breaks the entire pipeline.

⚠️ NEVER hardcode exam-specific values (Shift, US Letter, 4 options, etc.)
   ALL exam-varying values come from exam_config.json. If you find yourself
   writing a literal "Shift" or "4" in the code, you are violating the
   exam-agnostic guarantee.
```

---

# END OF Framework_PYQSort v1.18
