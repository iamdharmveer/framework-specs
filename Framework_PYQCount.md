# Framework_PYQCount v1.5.1 — PYQ Step 4 — Phase B Count Filling (§5)
# v1.5.1 — 2026-08-21 — GAP-2026-08-21-C8-FENCE-BURNDOWN (editorial; no rule
#   changed). audit_callgraph C8 reported engine calls in untagged fences — 30
#   across the corpus, invisible behind an 8-line display cap. This file: 9 prose mentions to no-paren form.
#   Call mentions in prose now use the documented no-paren form; genuine code is in
#   tagged ```python fences, AST-inspectable by C1-C8, all names bound (def-wrapped).
# v1.5 — 2026-08-16 — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, propagated per the
#   LAW-PROPAGATION LAW. Step 4 did not suffer the reference incident — it is
#   single-session, so its probe cost amortises to zero and its spec is far under the
#   SPEC-BUDGET threshold — but three of the four laws that incident produced govern any
#   step performing a CLASS T acquisition before a partition, and a law that is applied
#   in one file and not its sibling is how the PYQAnalyse->PYQCount split shipped an
#   unfixed defect "content byte-identical" in the first place.
#   (a) EC-P43 DIRECT EGRESS LANE added as A0, tried before the connector probe.
#   (b) EC-P40 the probe is a SPENDER: plan_transport passes consumed= explicitly.
#       Step 4 fetches the probe paper again in the same run, so the value is 0 and the
#       reason is stated at the call site rather than left as an absent argument that
#       audit_callgraph C10 cannot distinguish from an oversight.
#   (c) EC-P41 the listing is written and ASSERTED by corpus_io.write_drive_listing.
#   (d) P4f divergence DECLARED: 'SMALLEST by fileSize' is correct HERE and wrong in
#       Step 5. mock_sync_audit MS-13 requires both files to name the divergence.
## CROSS-FILE SECTION DIRECTORY — all §/S/EC IDs unchanged from Framework_PYQAnalyse v2.29
#### §1 — SESSION START → Framework_PYQCore.md
#### §2 — PHASE 0a: TAXONOMY BUILDING (PYQDraft) → Framework_PYQDraft.md
####      (S2-3 Draft taxonomy generation is HOSTED in Framework_PYQCore.md — universal
####       machinery per §11, executed by both S2-3 [PYQDraft] and S3-6 Refinement [PYQScan])
#### §3 — PHASE 0b: SMART SCAN (PYQScan) → Framework_PYQScan.md
#### §4 — PHASE 0c: ANALYSIS DOC & APPROVAL (PYQApprove) → Framework_PYQApprove.md
#### §5 — PHASE B: COUNT FILLING (PYQCount) → Framework_PYQCount.md
#### §6 — HEADING FORMAT CONTRACT → Framework_PYQCore.md
#### §7 — NAME CONSISTENCY CONTRACT → Framework_PYQCore.md
#### §8 — CLASSIFICATION RULES → Framework_PYQCore.md
#### §9 — EDGE CASES → Framework_PYQCore.md
#### §10 — DELIVERABLE SET CONTRACT → Framework_PYQCore.md
#### §11 — EXAM-AGNOSTIC GUARANTEE → Framework_PYQCore.md
#### §12 — DEFINITION OF DONE → Framework_PYQCore.md
#### Every trigger loads its step file + Framework_PYQCore.md (routes.json). History: CHANGELOG.md
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_PYQCount.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

---

## §5 — PHASE B: COUNT FILLING (after all sorting done)

### S5-1 — Read sorted PYQ files from Drive

```
Trigger: PYQCount PYQ: <<Drive link>>

Phase B reads ALL sorted PYQ files from the Drive folder.
These are the output of PYQSort — one sorted .docx per original Row file.

Processing model: batch up to 5 files at a time (BATCH_SIZE_COUNTS = 5).
Accumulate counts in a count_progress.json across batches.

═══════════════════════════════════════════════════════════════════════
v2.21 — ACQUISITION IS DELEGATED TO CLUSTER H / corpus_io
═══════════════════════════════════════════════════════════════════════
Step 4 and Step 5 read the SAME corpus from the SAME folder through the SAME
connector. They must not hold two independent enumerations — that is the drift
the framework forbids, and it is how Step 4 came to carry every defect that
took Step 5 down on 2026-07-24 while looking untouched.

  blueprint_core (Cluster H)  DECIDES  — screening rules, identity, partition
  corpus_io                   PERFORMS — listing, pagination, fetch, decode

Never restate a threshold here. DRIVE_CAP, SIZE_BUDGET and CHAT_FILE_LIMIT
have one definition and every step imports it.
```

### S5-0 — GOOGLE DRIVE TRANSPORT: CLASS T DECLARATION, THE BRIDGE, CHANNEL PROBE

```python
# ── GOOGLE DRIVE — CLASS T TRANSPORT ─────────────────────────────────────────
#
# GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. Until v1.3, S5-4 step 1 read:
#
#       local_path = corpus_io.fetch_drive_docx(
#           gdrive_download_file, paper, '/home/claude/pyq_counts')
#
# and `gdrive_download_file` was defined in NO spec, NO engine and NO builtin. The
# name appeared exactly once in this file — at that call site. Executed literally it
# raises NameError; fetch_drive_docx converts that to TransportFallback; every paper
# routes to the upload lane; Task 1 reports "0 of N papers read" and cannot confirm.
# The Drive lane was therefore unreachable on EVERY run of EVERY exam, for 20 days,
# with audit_callgraph reporting 0 findings the whole time.
#
# The failure is LOUD, so no wrong number was ever produced — this cost availability,
# not correctness. That is the ONLY reason it was survivable. Do not treat loudness as
# a mitigation: MockTestAnalyse v2.37 records the identical defect in the identical
# shape, and the observability of the failure was the only variable between them.
#
# CLASS: T — these are NOT python functions. They are the NAME of a tool call the
# model performs IN ITS OWN TURN, before count_pipeline.py runs. A tool call cannot
# happen inside a running python process (CLAUDE.md, EXECUTION-BOUNDARY LAW). That is
# a law about EXECUTION and it is unconditional: LISTING a folder is a connector
# operation and can never be done from python, whatever the allowlist says.
# The separate claim that "there is not even a network fallback" was measured on one
# deployment and is NOT a framework property — EC-P43 adds a DOWNLOAD path in python
# for link-shared files when egress permits it. Downloading and listing are different
# operations: A0 may fetch bytes, A1 must still use the connector. A "just fetch it
# from python" proposal for the LISTING is still refused, on the execution-boundary
# ground above rather than on an allowlist that can change.

def gdrive_search(query, page_size=100, page_token=None):
    """CLASS: T — Google Drive MCP 'search_files'. NOT executable python.

    The model calls Google Drive:search_files(query="parentId = 'FOLDER_ID'",
    pageSize=..., pageToken=...) in its own turn and materialises the listing before
    any python runs. Returns [{id, title, mimeType, fileSize}]. Paginate to exhaustion
    — a folder larger than one page silently loses its tail otherwise.
    """
    pass  # CLASS: T — performed by the model between turns, never from python


def gdrive_download_file(file_id, local_path):
    """CLASS: T — Google Drive MCP 'download_file_content'. NOT executable python.

    The model calls Google Drive:download_file_content(fileId=file_id) in its own
    turn. The result is EITHER a spill-file path OR an inline payload. WHICH ONE IS A
    PROPERTY OF THE DEPLOYMENT, NOT OF THE FILE SIZE, and S5-0's probe measures it.
    """
    pass  # CLASS: T — performed by the model between turns, never from python


# ── THE BRIDGE — the pattern EVERY CLASS T operation must follow ─────────────
#
# PHASE A (model, in its own turns, BEFORE any python):
#     listing = gdrive_search("parentId = '<folder_id>'")   -> cache verbatim to disk
#     probe   = gdrive_download_file(<smallest paper>)      -> S5-0 channel probe
#     then, for each DRIVE-lane paper: gdrive_download_file(...)
#     Record, per file, WHATEVER CAME BACK — a spill path or an inline payload.
#     Do not normalise them, do not convert one into the other, and do not care which
#     it is: corpus_io.decode_drive_payload accepts bytes, a spill path in ANY
#     directory, a dict, a list, an inner JSON string, or bare base64.
#
# PHASE B (python): inject RESOLVERS — plain lookups over results that ALREADY EXIST.
# A resolver performs no tool call, so it is ordinary, reachable, testable python:
#
#     cache          = json.load(open(LISTING_CACHE))           # from PHASE A
#     list_fn        = lambda fid, page_token=None: (
#                          {'files': []} if page_token
#                          else cache.get(fid, {'files': []}))
#
#     v1.4 — THE CACHE IS KEYED BY FOLDER ID. v1.3 wrote a flat lambda that ignored
#     `fid` and returned the whole listing on every call. collect_corpus_files
#     RECURSES: it calls list_fn again with each sub-folder's id, so a flat resolver
#     hands the walker the SAME entries for the sub-folder, the sub-folder re-appears
#     inside itself, and the paper is seen twice — surfacing as
#     `DuplicatePaperError: two files resolve to the same paper identity`, a HARD STOP
#     that blames the operator's Drive for a defect in this contract. Measured on a
#     one-folder/one-paper fixture. A flat corpus never triggered it, which is exactly
#     why it had to be found by reading the engine rather than by running the step.
#     PHASE A therefore caches {folder_id: {'files': [...]}}, merging every page of a
#     folder into one entry. A bare {'files': [...]} cache is still accepted for a FLAT
#     folder, answered for the ROOT id only; any other id resolves to an empty page,
#     which ends the walk cleanly.
#     drive_payloads = {file_id: path_or_payload, ...}          # from PHASE A
#     resolver       = lambda fid: drive_payloads[fid]
#     local_path     = corpus_io.fetch_drive_docx(resolver, paper, WORK_DIR)
#
# When PHASE A already holds the payload there is no callable to own at all, and
# inventing one is what produced this GAP. Use the direct route instead:
#
#     local_path = corpus_io.stage_drive_payload(drive_payloads[paper['id']],
#                                                paper, WORK_DIR)
#
# NEVER pass gdrive_search or gdrive_download_file themselves. They are CLASS T
# markers, not callables. audit_callgraph C6 fails the build if a CLASS T stub's
# return value is consumed; C7 fails the build if an injection point receives a name
# that is not bound in this spec — including from an untagged fence, which is where
# this defect lived and why an AST-only check could not see it.
# ─────────────────────────────────────────────────────────────────────────────
```

```python
# ── S5-0 CHANNEL PROBE — MEASURE THE CHANNEL, NEVER ASSUME IT ────────────────
# Runs AFTER S5-1 enumeration and BEFORE S5-1a Task 1. Costs exactly ONE paper.
import blueprint_core as bc      # Cluster H — pure acquisition decisions
import corpus_io                 # I/O shell — Drive listing, guarded fetch, decode

def probe_drive_channel(probe_paper, probe_payload, arrived_inline, work_dir):
    """Classify the Drive channel from ONE real download, and PROVE it decodes.

    WHY THIS EXISTS. Until v1.3 the corpus asserted, in three places, that "for any
    real paper the connector's result EXCEEDS CONTEXT and spills to a JSON file on
    disk". Measured 2026-08-15 on a single 40,488-byte sorted paper: one deployment
    spilled it to a file, a second returned it inline with no spill file anywhere, and
    the two spill directories were not the same directory. The invariant was false in
    the only sense that matters — it was believed, and it was not checked.

    WHAT IS CLASSIFIED, AND WHAT IS NOT. The channel does NOT select a mechanism: the
    resolver already carries whatever PHASE A received, and decode_drive_payload
    already accepts every shape either channel produces. The channel selects a COST
    MODEL and nothing else:

        'spill'  — the payload landed on disk. Context cost is ZERO. Drive lane.
        'inline' — the payload arrived in the model's turn. Every paper costs
                   ceil(bytes/3)*4 characters of context inbound, and again to
                   persist. The lane is then bounded by CONTEXT, not by DRIVE_CAP.

    HOW IT IS CLASSIFIED. `arrived_inline` is an OBSERVATION the model makes about its
    own turn: did the tool hand back a reference to a file, or the bytes themselves?
    That is a fact, not an inference. NEVER classify by listing a directory and
    checking whether a spill file appeared in it: the spill directory is chosen by the
    deployment, one deployment's directory does not exist in another, and a probe that
    hardcodes a path reports 'inline' on a perfectly working spill channel — which
    would route an entire fetchable corpus to manual upload on every exam. That is a
    worse outcome than the defect this GAP fixes, and it is the reason this function
    takes an observation rather than performing a filesystem test.

    The probe also PROVES the lane rather than predicting it: the payload is staged
    through the same engine path the corpus will use, so a channel that classifies
    cleanly but cannot produce verified bytes fails here, at paper 1, instead of at
    paper 12. Any TransportFallback propagates to the caller, which routes the whole
    corpus to the upload lane per EC-P35.
    """
    local_path = corpus_io.stage_drive_payload(probe_payload, probe_paper, work_dir)
    channel = 'inline' if arrived_inline else 'spill'
    print(f"\n  S5-0 CHANNEL PROBE — {probe_paper['name']} "
          f"({probe_paper['fileSize']:,} bytes)")
    print(f"    Verified bytes on disk : {local_path}")
    print(f"    Channel                : {channel.upper()}"
          + ("  — payloads arrive in context; the Drive lane is bounded by context"
             if channel == 'inline' else
             "   — payloads land on disk; the Drive lane costs no context"))
    return {'channel': channel, 'probe_paper': probe_paper['name'],
            'probe_local_path': local_path}


def plan_transport(sorted_papers, channel):
    """Split the corpus into the Drive lane and the upload lane BEFORE fetching.

    Predictive, not binding: the runtime fallback in S5-4 is what guarantees
    correctness. A paper mispredicted here still completes, via upload.

    `channel` comes from probe_drive_channel and has no default. A default would be a
    guess about the deployment, and guessing is the entire defect class this GAP
    closes. Print the plan even when nothing is deferred — before v1.3 the block was
    printed only `if part['upload']`, so a corpus that could not be fetched at all
    told the operator NOTHING before Task 1, defeating the stated purpose of S5-1.
    """
    # EC-P40 / audit_callgraph C10 — the probe is a SPENDER and the argument is
    # ALWAYS passed explicitly, never left to the default. Here the value is 0 and the
    # reason is specific to this step: Step 4 is single-session and fetches the probe
    # paper again in the same run, so its cost is amortised rather than lost. Omitting
    # the argument would be indistinguishable from the Step-5 oversight this law
    # exists to prevent, which is why C10 requires it to be written out.
    part = bc.partition_by_transport(sorted_papers, channel=channel, consumed=0)
    print(f"\n  TRANSPORT PLAN  (channel: {part['channel']})")
    print(f"    Drive lane  : {len(part['auto'])} paper(s) fetch automatically")
    print(f"    Upload lane : {len(part['upload'])} paper(s) must be uploaded to chat")
    if part['channel'] == 'inline':
        print(f"    Context cost: {part['inline_chars']:,} base64 chars admitted of a "
              f"{part['inline_budget']:,} budget "
              f"(bc.INLINE_BUDGET_CHARS); {len(part['deferred_for_context'])} paper(s) "
              f"deferred to the upload lane for CONTEXT, not for size — EC-P36.")
    if part['upload']:
        plan = bc.upload_batch_plan(len(part['upload']), BATCH_SIZE_COUNTS)
        print(f"    Chat accepts {bc.CHAT_FILE_LIMIT} files per conversation — "
              f"{plan['papers_per_chat']} papers across {plan['batches_per_chat']} "
              f"batches at BATCH_SIZE_COUNTS={BATCH_SIZE_COUNTS}, "
              f"so {plan['chats_needed']} chat session(s) for the upload lane.")
        oversize = [p for p in part['upload']
                    if (p.get('fileSize') or 0) > bc.DRIVE_CAP]
        if oversize:
            print(f"    Permanent fix for the {len(oversize)} OVERSIZED paper(s): run "
                  f"PYQCompress on them once and replace them in Drive — they then "
                  f"fetch automatically for Steps 2b, 4 and 5. PYQCompress does NOT "
                  f"help papers deferred for channel or context reasons (EC-P35/P36): "
                  f"the constraint there is the channel, not the file size.")
    return part


def acquire_paper(paper, drive_payloads, resolver, work_dir, needs_upload):
    """S5-4 step 1. Return a local path, or None when the paper needs an upload.

    THIS IS THE ACQUISITION CONTRACT, AND IT LIVES IN A ```python FENCE ON PURPOSE.
    Until v1.3 it lived as indented pseudo-code inside an UNTAGGED, non-parseable
    fence, mixed with prose and box-drawing rules. Every AST-based check in the repo —
    audit_callgraph C1-C6, audit_deep, validate_framework_md — skips such a block
    entirely. The single most load-bearing instruction in Step 4, how the bytes are
    obtained, was therefore the one instruction the CI was structurally unable to
    read, and a call to an undefined name survived there for 20 days across a full
    corpus audit that reported 0 findings.

      A contract the CI cannot read is a contract the CI cannot enforce.
      Executable contracts belong in ```python fences. audit_callgraph C8 enforces
      this for every injection point.

    NEVER call the connector from here. `resolver` is a plain lookup over payloads
    PHASE A already materialised, so this function performs no tool call and raises no
    NameError. Every failure — size, permission, malformed envelope, truncation,
    unknown — arrives as TransportFallback and degrades to the upload lane. A
    transport failure is NEVER fatal to the run.
    """
    if paper['id'] in drive_payloads:
        try:
            return corpus_io.fetch_drive_docx(resolver, paper, work_dir)
        except corpus_io.TransportFallback as exc:
            print(f"    ! Drive fetch unavailable — {exc}")
            print(f"    → routing to upload lane: {paper['name']}")
            needs_upload.append(paper)
            return None
    if paper.get('path'):
        return paper['path']
    needs_upload.append(paper)
    return None
```

```python
import blueprint_core as bc      # Cluster H — pure acquisition decisions
import corpus_io                 # I/O shell — Drive listing, guarded fetch, decode

SORTED_RE = re.compile(r'_Sorted_Q\d+-Q\d+\.docx$', re.I)


def collect_sorted_papers(folder_id, list_fn):
    """Enumerate the Drive folder, keep only sorted PYQ files, plan transport.

    v2.21 — replaces a name-only listing that captured neither size nor mimeType.

    WHAT THE OLD FILTER MISSED, ALL SILENTLY:
      * fileSize — carried inline in the listing response and simply thrown away,
        so no pre-flight partition was possible and a paper above the connector's
        cap surfaced only when the download was attempted, deep inside the batch
        loop. Capturing it costs ZERO extra API calls.
      * a native Google Doc's title has no .docx suffix, so it matched nothing and
        was neither collected NOR reported — the paper vanished from the count.
      * legacy .doc was indistinguishable from .docx by suffix alone in the old
        pattern's intent; python-docx cannot open it, deferring a certain failure.
      * two files resolving to one paper identity ("X.docx" and "X (1).docx", which
        a browser creates on every remediation round trip) were counted TWICE.
    corpus_io.collect_corpus_files handles all four, paginates to exhaustion, and
    raises DuplicatePaperError rather than choosing between two identities.
    """
    papers, rejects = corpus_io.collect_corpus_files(list_fn, folder_id)

    # ── sorted-file filter (unchanged intent, EC-P29) ───────────────────────
    # The PYQ folder legitimately also holds Row files, the Analysis doc and other
    # documents. Only PYQSort output may be counted.
    sorted_papers, non_sorted = [], []
    for p in papers:
        (sorted_papers if SORTED_RE.search(p['name']) else non_sorted).append(p)

    for p in non_sorted:
        print(f"  Skipped non-sorted file: {p['name']}")
    for r in rejects:
        print(f"  REJECTED: {r['name']} — {r['reason']}")

    if not sorted_papers:
        raise SystemExit(
            "No sorted PYQ files found in Drive folder.\n"
            "Sorted files must match pattern: *_Sorted_Q1-QN.docx\n"
            + (f"{len(rejects)} entry(ies) were rejected — see the reasons above; "
               "one of them may be the corpus." if rejects else ""))

    return sorted_papers, non_sorted, rejects


def assert_no_session_duplicates(sorted_papers, session_keyword):
    """HARD STOP when two sorted files describe the same date + session.

    v2.21 — REPLACES "keep the LARGER file (more likely to have images intact)".

    That rule is now wrong twice over:
      1. Under the 10 MiB connector cap it selects precisely the copy that CANNOT
         be fetched, converting a cosmetic duplicate into a blocked paper.
      2. Phase B's standard is zero tolerance — S5-4a permits not one question
         missing or extra. A re-sorted paper and the superseded copy it replaced
         differ in content, so choosing between them silently CHANGES THE COUNTS.
         Choosing by size chooses by accident.
    The image-integrity reasoning behind the old tiebreak is also obsolete:
    PYQSort v1.12 CHECK 10 gates image survival where the file is produced, so a
    sorted file that lost a figure cannot be delivered in the first place.

    Canonical-identity duplicates ("X.docx" vs "X (1).docx") are caught earlier,
    at enumeration, by corpus_io.collect_corpus_files. This catches the case
    canonical identity cannot see: the same paper sorted twice under genuinely
    different names, e.g. _Sorted_Q1-Q100.docx and _Sorted_Q1-Q99.docx.
    """
    # Multi-date files ("_to_") represent unique combined papers — excluded, as before.
    pattern = re.compile(
        r'(\d{1,2}-[A-Za-z]{3}-\d{4})_.*?' + re.escape(session_keyword) + r'-(\d+)_Sorted_',
        re.I)
    groups = {}
    for p in sorted_papers:
        if '_to_' in p['name']:
            continue
        m = pattern.search(p['name'])
        if not m:
            continue                      # no parsable date+session — nothing to compare
        groups.setdefault((m.group(1).lower(), m.group(2)), []).append(p)

    clashes = {k: v for k, v in groups.items() if len(v) > 1}
    if clashes:
        lines = []
        for (date, sess), files in sorted(clashes.items()):
            lines.append(f"  {date} {session_keyword} {sess}:")
            for f in files:
                sz = f.get('fileSize')
                lines.append(f"    - {f['name']}" + (f"  ({sz:,} bytes)" if sz else ""))
        raise SystemExit(
            "HARD STOP — two sorted files describe the same paper:\n"
            + "\n".join(lines)
            + "\n\nDelete the superseded copy from Drive and re-run. This is NOT resolved "
              "automatically: the two files differ in content, so counting either one is a "
              "decision about the numbers, and Phase B tolerates no error at all. Keeping "
              "the larger file — the pre-v2.21 rule — would also pick the copy least likely "
              "to fit under the "
            + f"{bc.DRIVE_CAP:,}-byte Drive download cap.")


# plan_transport() is DEFINED IN S5-0 above, with the channel parameter the probe
# supplies. v1.2 defined it here with a size-only signature and printed the plan only
# `if part['upload']`, so an unfetchable corpus printed NOTHING before Task 1. Do not
# reintroduce a second definition: two transport planners is the drift this file's own
# v2.21 note forbids for enumeration, and it applies identically here.
```

```
FILE FILTERING (prevent non-sorted files from contaminating counts):
  1. Enumerate via corpus_io.collect_corpus_files (recursive, paginated, per EC-P23).
  2. Keep ONLY files matching r'_Sorted_Q\d+-Q\d+\.docx$'.
     Non-matching .docx files are SKIPPED with a warning:
       "Skipped non-sorted file: [filename]"
     This prevents Row files, the Analysis doc, or other .docx files in the
     same Drive folder from being processed.
  3. Every REJECTED entry (native Google Doc, shortcut, legacy .doc, no size)
     is printed with its reason. Nothing is ever dropped silently — a paper that
     disappears without an error is a year of the corpus that nobody notices.
  4. If 0 sorted files found → "No sorted PYQ files found in Drive folder.
     Sorted files must match pattern: *_Sorted_Q1-QN.docx"

DUPLICATE DETECTION (prevent inflated or wrong counts) — v2.21, both HARD STOP:
  a. CANONICAL IDENTITY — "X.docx" and "X (1).docx", or the same paper in two
     subfolders. Caught at enumeration by corpus_io.collect_corpus_files, which
     raises DuplicatePaperError naming both files.
  b. SAME DATE + SESSION, different filenames — e.g. a paper re-sorted after a
     correction, leaving _Sorted_Q1-Q100.docx beside _Sorted_Q1-Q99.docx.
     Caught by assert_no_session_duplicates(), which names both and stops.
     Multi-date files (filename contains "_to_") are excluded from this check —
     they represent unique combined papers, as before.
  Neither is resolved automatically. See EC-P30 for the reasoning.
```

### S5-1a — TASK 1: Pre-Count Confirmation Gate

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before ANY subtopic counting begins.
═══════════════════════════════════════════════════════════════════════

After listing all sorted PYQ files from Drive (S5-1), but BEFORE running
the batch counting loop (S5-4):

  1. Read EVERY sorted PYQ file from Drive using python-docx (same method
     as count_sorted_file in S5-2 — paragraph iteration, NOT Drive
     read_file_content which may strip content).
  2. For each file: count total questions using the SAME detector as
     count_sorted_file(), which is the ENGINE detector:
       bc.detect_question_start on para.text is not None
     GAP-2026-08-15-BAREQ (R-3). This step used to carry a private regex
     r'^Q\.?\s*\d+' justified by "PYQSort always outputs Q.<N> format" — an
     ASSUMPTION about another step's output where a DELEGATION belongs, and one
     nothing enforced. It matched strings the engine's table did not (notably a
     bare "Q.4", and "Q1 Analysis"), so Step 4 and Step 5 disagreed about which
     paragraphs were questions AT ALL. On the discovery paper that divergence is
     measurable in the wrong direction too: the permissive regex COUNTED the four
     absorbed bare labels while Step 5 could not extract them, so Step 4 reported
     60 for a file Step 5 read as 56 and attributed the four to whatever subtopic
     happened to precede them.
     Store per-file count: task1_per_file[filename] = q_count
  3. Extract year from filename (S5-3 logic)
  4. Display a YEAR-WISE PAPER INVENTORY table:

     | Year | Paper File | Q Count |
     |------|-----------|---------|
     | 2025 | [ExamCode]_12-Sep-2025_Shift-1_Sorted_Q1-Q100.docx | 100 |
     | 2025 | [ExamCode]_13-Sep-2025_Shift-2_Sorted_Q1-Q100.docx | 100 |
     | ...  | ...       | ...     |
     | TOTAL | [N] papers | [T] questions |

  5. Print:
     "TASK 1 — PRE-COUNT CONFIRMATION
      Papers found: [N]
      Total questions across all papers: [T]

      ★ CONFIRMATION REQUIRED ★
      Verify these numbers match your expectation.
      Once confirmed, I will proceed with subtopic-level counting.
      If anything looks wrong, tell me and I will re-scan."

  6. WAIT for explicit user confirmation. Do NOT proceed to S5-4 until
     confirmed. The confirmed total [T] becomes the ACCURACY TARGET
     for Task 2.

PURPOSE: proves that Claude can see every file and every question
inside each file without fail. Catches Drive access issues, missing
files, or parsing failures BEFORE counting effort is wasted.
```

### S5-2 — Heading parser (Step 5 E-1 compatible)

```python
# CRITICAL — HEADING FORMAT CONTRACT
# This parser MUST use the SAME patterns as Step 5's parse_taxonomy_level().
# If these diverge, Phase B counts won't match Step 5's Frequency xlsx.

# v2.20 — DELEGATED TO THE ENGINE. This function previously carried the instruction
# "IDENTICAL to Step 5's parse_taxonomy_level() - DO NOT MODIFY independently", and the two
# copies had ALREADY drifted: Step 5 was expanded in v2.16 (RIGID-4) from 3 heading patterns
# to 12+ while this copy was never mirrored. Any exam whose sorted headings use Section:,
# Part:, Area:, Unit N, Module N, Block N or a colon-style Topic had those headings read as
# LEVEL 1/2 by Step 5 and as SUBTOPICS (level-3 fallthrough) by Step 4 — wrong per-subtopic
# counts by construction, with only Step 6's BV-0A cross-check downstream of it.
# EC-P14's remedy ("ensure both use IDENTICAL parser code") is now enforced structurally
# instead of by a comment asking two files to stay in step.
parse_taxonomy_level = bc.parse_taxonomy_level

# Option patterns — MUST match Step 5's E-3 OPT_PATTERNS exactly.
# Capture groups are present for parity; is_option() only checks match/no-match.
# The (.+) suffix is critical: it requires actual option text after the label,
# preventing bare labels like "1. " from being treated as options.
# ── OPTION PREDICATE — DELEGATED (v2.29, audit_deep [XSPEC-DRIFT]) ────────────
# This file defined its own is_option() with a docstring claiming alignment with
# Step 5. No executable call site was found for it here, so the copy was pure drift
# bait: it could not misbehave, but it WOULD have gone stale unnoticed — and did,
# the moment MockTestAnalyse v2.34/v2.35 added the image-option path.
# Delegated rather than deleted so that any future call site in this spec inherits
# the correct behaviour instead of silently reintroducing the text-only predicate.
OPT_PATTERNS = corpus_io.OPT_PATTERNS
is_option    = corpus_io.is_option

# v2.20 — DELEGATED TO THE ENGINE (same drift class as parse_taxonomy_level above).
# The local copy excluded questions with its own regex r'^Q\.?\s*\d+' while Step 5 used the
# shared Q_PATTERNS table via detect_question_start(). Those two match DIFFERENT strings
# (e.g. "Q1 Analysis" matches the local regex but is not a Q_PATTERNS question start), so the
# two steps disagreed about which paragraphs were headings AT ALL, not merely about level.
# 2026-08-15 (GAP-2026-08-15-BAREQ, R-3): the LAST two inline copies of that regex, in the
# S5-1 mandatory gate and in count_sorted_file() below, are now gone as well. Q-detection in
# this spec happens in exactly one way — bc.detect_question_start() — and audit_deep's
# INLINE-QREGEX check fails the build if a private copy is ever reintroduced.
def is_taxonomy_heading(para, next_text=None, colour_available=False):
    return bc.is_taxonomy_heading(para, is_option, next_text, colour_available)

# GAP-2026-07-26-001 — PASSING next_text IS MANDATORY HERE.
# A LEVEL-3 heading is bare text by contract (PYQSort S6-2), so bold was its only
# positive signal — and PYQSort EC-S8 emits multi-paragraph stems whose continuation
# lines are ALSO bold, not dates, not options and not question starts. Without the
# positional argument every such line became a subtopic, and every question after it
# was counted under a question stem. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers,
# 1719 questions): 20 spurious headings, 128 counted triples against 126 real ones,
# 2 phantom triples, Task 2.5 HARD STOP with no valid remedy — re-sorting reproduces
# the file byte for byte, and amending the taxonomy would have written a question
# stem into the LOCKED taxonomy, which D6-1 exists to prevent. See S5-4b step 4a.
def count_sorted_file(docx_path):
    """
    Walk a sorted PYQ .docx, count questions per (section, topic, subtopic).
    Returns: (counts, orphans)
      counts:  {(section, topic, subtopic): count}
      orphans: [(q_num, reason)]  — questions that couldn't be attributed
    """
    from docx import Document
    doc = Document(docx_path)
    counts = Counter()
    orphans = []
    cur_sec = cur_top = cur_sub = ''

    # GAP-2026-07-26-001 + GAP-2026-08-05-001. sorted_body_lookahead() is BLOCK-level:
    # a <w:tbl> is not a paragraph and never appears in doc.paragraphs, and a paragraph
    # holding only an image / equation / embedded object has NO text, so the old
    # paragraph-and-text-scoped lookahead skipped both and reported the NEXT QUESTION'S
    # date label — making a bold stem continuation satisfy the level-3 heading test.
    paras, nxt = bc.sorted_body_lookahead(doc)
    # D6 — the DIRECT discriminator, probed ONCE PER FILE from the date labels (S6-2
    # mandates them navy #003366; CHECK 3 enforces it). Never probe per paragraph: a
    # misread continuation carries no <w:color> at all, so a per-paragraph fallback
    # returns straight to the blind spot and measurably fixes nothing.
    colour_ok = bc.heading_colour_available(paras)
    for i, para in enumerate(paras):
        text = para.text.strip()
        if not text: continue
        if is_taxonomy_heading(para, nxt[i], colour_ok):
            lv, content = parse_taxonomy_level(text)
            # CRITICAL — reset child pointers when parent changes.
            # Matches Step 5 E-1: current_path[:level-1] + [content]
            # Without this, a Q after a new Topic heading but before its
            # first Subtopic heading would silently inherit the WRONG
            # subtopic from the previous topic.
            if lv == 1:
                cur_sec = content; cur_top = ''; cur_sub = ''
            elif lv == 2:
                cur_top = content; cur_sub = ''
            else:
                cur_sub = content
        elif bc.detect_question_start(text) is not None:
            # GAP-2026-08-15-BAREQ (R-3) — engine detector, never a local copy.
            q_num = bc.detect_question_start(text)
            if not cur_sec:
                orphans.append((q_num, 'no_section_context'))
            elif not cur_sub:
                orphans.append((q_num, 'no_subtopic_context'))
            else:
                counts[(cur_sec, cur_top, cur_sub)] += 1

    return counts, orphans
```

### S5-3 — Year extraction from sorted files

```python
def extract_year_from_sorted_filename(filename):
    """
    Sorted PYQ filenames follow patterns:
      [ExamCode]_DD-Mon-YYYY_Shift-N_Sorted_Q1-QN.docx
      [ExamCode]_DD-Mon-YYYY_to_DD-Mon-YYYY_Sorted_Q1-QN.docx
    Extract the primary year.
    """
    m = re.search(r'(\d{1,2})-([A-Za-z]{3})-(\d{4})', filename)
    return int(m.group(3)) if m else None
```

### S5-4 — Batch counting loop

```
BATCH_SIZE_COUNTS = 5  # max 5 papers per batch — UNCHANGED in v2.21

═══════════════════════════════════════════════════════════════════════
v2.21 — THE DURABILITY UNIT IS THE FILE, NOT THE BATCH (DEFECT C)
═══════════════════════════════════════════════════════════════════════
Before v2.21 this loop saved count_progress.json once per BATCH (old item 7).
Counting mutates the accumulators in memory; the save is the only thing that
persists them. Any exception inside the loop — a transport failure, a malformed
document, a context stop — skipped the save entirely, so every file already
counted in that batch was discarded with NO trace. count_progress.json shows
them as never processed, and the resume path recounts them from scratch.

At BATCH_SIZE_COUNTS = 5 that is up to FOUR papers of work lost per failure.

WHAT THE CONSEQUENCE ACTUALLY IS (v2.22 correction). v2.21 described this as "a
silent undercount". That was wrong, and the correction matters because an
overstated rationale is the kind of thing a future reader checks, disbelieves,
and then discounts the whole rule over. Counts and _meta.files_processed_list
are persisted by the SAME save, so a skipped save loses both together: the
resume path finds those files absent from the list and recounts them, and the
total comes out right. S5-4a would catch it if it did not.
The real costs are two:
  * up to four papers of counting work discarded per failure, and a progress
    file that reports fewer files done than were actually processed;
  * a double-count IF the accumulator and the processed-list are ever persisted
    at different moments — which is precisely what happens the first time
    someone "optimises" one of the two writes without noticing they are a pair.
Saving per file makes them atomic, so the second risk cannot be introduced by a
later edit. That is the durable reason for the fix, and it does not need the
overstatement.

BATCH_SIZE_COUNTS stays 5. Batching is the user-facing PACING unit and is not
the durability unit. The batch-level save REMAINS as a redundant flush.
═══════════════════════════════════════════════════════════════════════

For each batch of sorted PYQ files (up to 5 per batch):

  For each file in the batch:
    1. ACQUIRE the file — call acquire_paper(), DEFINED IN S5-0 as python.
       If it returns None the paper went to the upload lane; skip to the next file.

       v2.21 — never call the connector unguarded.
       v1.3  — and never call it FROM PYTHON AT ALL. `resolver` and `drive_payloads`
       come from THE BRIDGE in S5-0: PHASE A materialised every DRIVE-lane payload
       before this loop starts, so acquisition here is a dict lookup and a decode,
       not a tool call. Papers S5-0 assigned to the upload lane are never attempted.

       This step used to carry its own inline copy of the acquisition code, in this
       untagged prose fence, and that copy passed the undefined name
       `gdrive_download_file` — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. The code
       now has ONE definition, in a fence the CI can parse. Do not paste a second copy
       back into this block: an acquisition contract that lives in prose is invisible
       to every static check in the repo, which is exactly how the defect survived a
       corpus-wide audit that reported zero findings.

       EVERY failure — size, permission, network, malformed envelope, unknown —
       raises TransportFallback and degrades to the upload lane. A transport
       failure is NEVER fatal to the run. Verified before v2.21: ZERO try/except
       existed around any Drive call in the entire corpus, so one oversized paper
       terminated everything.
       fetch_drive_docx also asserts byte count == reported fileSize and the
       PK\x03\x04 magic. A payload truncated at a ZIP member boundary still opens
       as a valid archive while presenting FEWER QUESTIONS — the byte count is
       the only thing that catches an undercount caused by transport.

    2. Read the file → count_sorted_file() → (per-subtopic counts, orphans)
    3. Track per-file attributed count:
         per_file_attributed[filename] = sum(counts.values())
       This is compared against task1_per_file[filename] in Task 2 diagnostic.
    4. If orphans non-empty for this file → log:
         "WARNING: [filename] has [N] orphan questions: Q[x] (reason), ..."
       Accumulate in all_orphans[(filename, q_num)] = reason
    5. Extract year from filename
    6. Accumulate: counts_by_year[(section, topic, subtopic)][year] += count
    7. Track papers_per_year[year] += 1
    8. Append filename to _meta.files_processed_list
    9. SAVE count_progress.json — NOW, inside this loop, for THIS file.
       Not after the batch. This is the whole of the DEFECT C fix and it makes a
       partial batch safe to resume.

  After the file loop, if needs_upload is non-empty:
    Request exactly those papers BY NAME, then match the uploads back by
    CANONICAL identity via corpus_io.resolve_uploaded_papers — never by exact
    filename (the browser appends " (1)" whenever the original is already in the
    operator's Downloads folder, which happens on every remediation round trip)
    and never by recency (uploads ACCUMULATE across turns, so by batch 3 the
    directory still holds batches 1 and 2 and they would be silently recounted).
    Count each matched upload and SAVE after each one, exactly as above.
    Report unexpected uploads; never process them.
    Papers still missing are reported and remain pending — not skipped, not
    counted as done.

  Then save count_progress.json again (redundant batch flush — harmless, and it
  keeps the batch delivery contract unchanged).

After all files processed:
  If all_orphans is non-empty:
    Print "⚠ [N] orphan questions found across [M] files.
           These questions appear before any Subject/Subtopic heading
           and cannot be attributed to a taxonomy triple.
           This is a PYQSort bug — sorted files must have taxonomy
           headings before every question block."
    List all orphans with file + Q number + reason.
    HARD STOP — do not proceed until orphans are resolved.
  If all_orphans is empty:
    Run Task 2 accuracy gate (S5-4a).

NOTE ON TASK 1 (S5-1a) — it reads every file too, and takes the identical
acquisition path. A paper that must come through the upload lane is requested
ONCE, at Task 1, and the local copy is reused for counting; it is not requested
again in S5-4. The Task 1 inventory reports which lane each paper took, so the
operator learns the transport shape of the corpus before any counting begins,
not at batch 6.
```

### S5-4a — TASK 2: Post-Count Accuracy Gate

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before touching the Analysis doc.
Zero tolerance: not even 1 question may be missing or extra.
═══════════════════════════════════════════════════════════════════════

After all batches in S5-4 are complete, but BEFORE updating the Analysis doc
(S5-5):

  1. Compute grand_total = sum of ALL subtopic counts across all
     (section, topic, subtopic) triples.

  2. Compare grand_total against the CONFIRMED total from Task 1 (S5-1a).

  3. Display a FULL HIERARCHICAL BREAKDOWN:

     SUBJECT: [Section 1 Name]
       Topic 1: [Topic Name] — [topic_total] Qs
         [Subtopic A] — [count]
         [Subtopic B] — [count]
         ...
         Topic Total: [sum]
       Topic 2: [Topic Name] — [topic_total] Qs
         ...
       Section Total: [section_total]

     SUBJECT: [Section 2 Name]
       ...

     ═══════════════════════════════
     GRAND TOTAL: [grand_total] Qs
     TASK 1 CONFIRMED TOTAL: [T] Qs
     MATCH: ✓ / ✗
     ═══════════════════════════════

  4. ACCURACY CHECK:
     IF grand_total == confirmed_total (Task 1):
       Print "TASK 2 PASSED — all [T] questions accounted for."
       Proceed to S5-4b (Task 2.5).
     ELSE:
       Print "TASK 2 FAILED — mismatch: counted [grand_total], expected [T].
              Difference: [delta] questions."

       PER-FILE DIAGNOSTIC:
       Compare task1_per_file[filename] (Task 1 raw Q-count) against
       per_file_attributed[filename] (S5-4 heading-attributed count)
       for every file. Display files where the counts differ:
         | File | Task 1 Qs | Attributed Qs | Diff |
         | [filename1] | 100 | 98 | -2 |
         | ...
       This pinpoints exactly WHICH files have the gap and by how many.
       Common causes: heading parser missed a question (malformed heading
       above it), or orphan questions were present (should have been
       caught by orphan gate, but verify).

       Re-scan the identified files. Fix the root cause.
       Repeat until grand_total == confirmed_total.
       Do NOT proceed to S5-4b until match is exact.

PURPOSE: guarantees 100% accuracy — every question counted by Task 1
is classified into exactly one (section, topic, subtopic) triple.
No question silently dropped by the heading parser.
```

### S5-4b — TASK 2.5: Taxonomy Name Cross-Check

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before writing ANY count to the Analysis doc.
Prevents silent count loss from name mismatches.
═══════════════════════════════════════════════════════════════════════

After Task 2 passes, but BEFORE S5-5 (doc writing):

  1. LOAD THE TAXONOMY THROUGH THE ONE READER. Never by hand.

     v2.25 (GAP-2026-07-25-003) — THE ANALYSIS DOC IS READ BY corpus_io, NOT BY PROSE.
```

```python
import corpus_io                        # ENGINE (routed to PYQCount)

# v2.27 — ONE call: it selects the taxonomy source, reads it, and asserts identity
# against the approval record. Prefers the record's own "taxonomy" key
# (reconcile_taxonomy >= v1.3) and falls back to the Analysis doc for pre-1.3
# records, so exams approved earlier keep working and need no re-run.
doc = corpus_io.load_taxonomy(step='PYQCount')
taxonomy_triples = set(doc['triples'])   # (section, topic, subtopic), names already
                                         # normalised by parse_taxonomy_level()

# ── IDENTITY GATE (v2.25) — the doc must be the one that was APPROVED ─────────
# Cluster K asserts the doc agrees with ITSELF (its three self-declarations). It
# cannot assert that this is the taxonomy PYQApprove LOCKED. Those are different
# claims, and until v2.25 Step 4 made only the first — so a superseded Analysis
# doc left in project Files would have been counted into, silently, and every
# downstream step would have inherited the wrong vocabulary. Same cross-check as
# Framework_PYQSort S1-0b, same failure text.
# v2.27 — the identity assertion happens INSIDE load_taxonomy() above; there is no
# separate gate call and no separate read. It discovers
# [ExamCode]_approval_record.json, hard stops when the record carries no
# taxonomy_fingerprint (re-run PYQApprove — RECONCILIATION, not re-derivation), hard
# stops when the fingerprint differs from the loaded taxonomy's, and — when the
# record carries a taxonomy — hard stops when the record does not agree with itself.
record = corpus_io.read_approval_record(doc['exam_code'])

print("Taxonomy identity verified: fingerprint matches the approval record.")
print("Taxonomy source: %s (%s)" % (doc['source'], doc['ingest_form']))
```

```
     WHY THIS REPLACED THE OLD EXTRACTION METHOD. Task 2.5's entire purpose is
     BYTE-IDENTICAL agreement between the names in the Analysis doc and the names
     count_sorted_file() produces. The old text described extracting section names
     from the "[ExamCode] — [Section]" header line, topic names by stripping
     "Topic N: " with a local regex, and subtopic names from raw cells — a SECOND
     hand-written implementation of parse_taxonomy_level(). Two implementations of
     one rule is exactly how the names drift, and drift is the failure this gate
     exists to catch. Both sides now come from ONE reader delegating to ONE
     heading parser, so the invariant holds by construction.

     It is also what makes Step 4 work at all. The Analysis doc lives in the
     project's Files section, where the platform stores it as extracted TEXT under
     its .docx name. corpus_io v1.2 detects the ingest form from CONTENT and scans
     either form to the identical structure; a hand parser, or a bare
     Document(path) open, sees a text file and fails (GAP-2026-07-25-003).
     NO OPERATOR ACTION — do not attach the Analysis doc to chat. Report the
     ingest form in the inventory; never warn about it.

  2. Build two sets:
       counted_triples  = set of all (section, topic, subtopic) from counting
       taxonomy_triples = doc['triples'] (loaded above)

  3. Compute:
       phantom_triples = counted_triples - taxonomy_triples
         (counted in sorted files but NOT in the Analysis doc)
       uncounted_subtopics = taxonomy_triples - counted_triples
         (in the Analysis doc but have zero counted questions)

  4. PHANTOM TRIPLE CHECK:
     IF phantom_triples is non-empty:
       Print "TASK 2.5 FAILED — [N] phantom triples found.
              These subtopics were counted in sorted PYQ files but do NOT
              exist in the Analysis doc.

              Phantom triples:"
       For each phantom: print (section, topic, subtopic) with count.
       Also print the CLOSEST MATCH from taxonomy_triples (fuzzy match).

     4a. TRIAGE FIRST — THERE ARE TWO CAUSES AND THEY NEED OPPOSITE FIXES.
         Run question_shape_verdict() (§S3 D6-1) on each phantom SUBTOPIC name and
         check whether the phantom text reads as prose lifted from a question.

         CAUSE 1 — MISREAD QUESTION STEM (GAP-2026-07-26-001).
           Signals: verdict is HARD or WARN; the name ends in '?', begins with an
           interrogative, is a bare option label ("1."), or reads as a sentence
           fragment; and NO close fuzzy match exists in the taxonomy.
           This is NOT a name mismatch. A bold stem-continuation paragraph was read
           as a subtopic heading. The sorted file is CORRECT; the parser was wrong.
           DO NOT re-sort — PYQSort reproduces the identical file, so this is a
             no-op and the run halts again in exactly the same place.
           DO NOT add the phantom to the Analysis doc — that writes a question stem
             into the LOCKED taxonomy, precisely the defect D6-1 exists to block.
             Step 6 would then allocate it and Step 7 would be asked to generate
             questions FOR a question.
           Those two prohibitions hold under 1a AND 1b below. Split the cause first.

           CAUSE 1a — THE POSITIONAL GATE IS ABSENT OR NOT PASSED.
             FIX: confirm count_sorted_file() (§S5-2) calls is_taxonomy_heading() WITH
             next_text, and that blueprint_core.py carries the GAP-2026-07-26-001
             positional gate (it exposes next_nonempty_texts()). Re-run PYQCount.

           CAUSE 1b — THE GATE IS PRESENT AND WAS DEFEATED (GAP-2026-08-05-001).
             If the two conditions in 1a are ALREADY TRUE, 1a's remedy is a dead end:
             it asks the operator to verify two already-true facts and re-run, which
             reproduces the identical halt forever. That is the exact failure the
             "WHY THE TRIAGE EXISTS" note below was written to prevent, and it
             happened again — this time one layer down. Diagnose instead:

             (i)  Locate the phantom text in the sorted paper. Inspect every BLOCK
                  between it and the NEXT date label. If all of them are TEXTLESS —
                  an image-only paragraph (<w:drawing>/<w:pict>), an equation-only
                  paragraph (<m:oMath>), an embedded object (<w:object>), an
                  auto-numbered paragraph whose "1." is rendered by Word and absent
                  from the XML, or a TABLE (which is not a paragraph at all) — this
                  is GAP-2026-08-05-001. The engine must carry paragraph_is_content_
                  bearing() and sorted_body_lookahead(); if it does not, upgrade it.
             (ii) If the question is NAT, there may be NO intervening blocks at all.
                  A NAT question has no options, so its last stem paragraph and a
                  genuine subtopic heading occupy the IDENTICAL slot — the last text
                  block before a date label — and no positional rule can separate
                  them. This case is fixed ONLY by D6: confirm the walker computes
                  bc.heading_colour_available on paras once per file and passes it.
             (iii) If the engine already carries both and the phantom persists,
                  escalate to the framework project WITH THE PAPER ATTACHED. Do not
                  work around it locally.

             NO RE-SORT IS REQUIRED under 1b. The sorted bytes were always correct;
             only the reading was wrong. Re-run Step 4 alone (and Step 5 if it had
             already completed — see Framework_MockTestAnalyse QV-1a/QV-15).

           A NOTE THAT SAVES TRIAGE TIME. The mis-attributed question is the one
           AFTER the misread paragraph, not the one containing it: the continuation
           sets cur_sub, so its OWN question was already counted correctly and the
           NEXT question is displaced. An operator reading the phantom text and
           looking for the question it came from will inspect the wrong question.

         CAUSE 2 — GENUINE NAME MISMATCH.
           Signals: verdict is OK; a close fuzzy match EXISTS in the taxonomy,
           differing only by trailing space, dash variant or case.
           FIX, either:
             Option A: re-sort the affected papers (PYQSort used the wrong name)
             Option B: correct the Analysis doc taxonomy (the doc carries the typo)
           The names MUST match exactly before counts are written.

       HARD STOP — do not proceed to S5-5 until the cause is identified and fixed.

     WHY THE TRIAGE EXISTS. Until GAP-2026-07-26-001 this gate asserted a single
     cause — "likely a name mismatch" — and offered only the two Cause-2 remedies.
     Against a misread stem, Option A is a no-op that reproduces the file byte for
     byte and Option B is destructive. An operator following the message as written
     had no valid exit, and the run halted permanently. A gate that DETECTS correctly
     but MISDIAGNOSES is worse than one that never fires: it spends the operator's
     trust, and then it spends their taxonomy.

  5. UNCOUNTED SUBTOPICS (informational, not a stop):
     IF uncounted_subtopics is non-empty:
       Print "INFO: [N] subtopics in the Analysis doc have 0 PYQ counts.
              These will be written as '0' in the doc (not left as '—')."
       List them. This is expected for Zero-PYQ subtopics (EC-P17).

PURPOSE: catches the most dangerous silent failure in Phase B — a name
mismatch that causes counts to vanish. Task 2 total-match passes because
the question IS counted, just under a wrong name. Without this cross-check,
some subtopics get inflated counts and others get 0, and the error is
invisible until Step 6's BV-0A (too late).
```

### S5-5 — TASK 3: Regenerate the Analysis doc with counts (arithmetic guarantee)

```
═══════════════════════════════════════════════════════════════════════
MANDATORY — every number in the Analysis doc must be arithmetically
perfect at ALL 4 levels. Not even 1 question mismatch tolerated.
═══════════════════════════════════════════════════════════════════════

v2.25 (GAP-2026-07-25-003) — PARSE -> MERGE -> REGENERATE, never edit in place.

This task used to say "replace every '—' PYQ Count cell" and re-total upward.
That is not performable any more, for two independent reasons:
  • the runtime receives the Analysis doc as platform-extracted TEXT, which has
    no cells to edit — there is no OOXML package on the path at all;
  • /mnt/project/ is READ-ONLY, so even the OOXML form could not be edited where
    it sits.
The doc is therefore rebuilt from the taxonomy Task 2.5 already loaded plus the
Task-2 verified counts, through corpus_io.write_analysis_doc (counts=...), which has
accepted a counts map since v1.1.

This is STRICTLY STRONGER than the rule it replaces. The writer derives the
subtopic cell, the per-topic TOTAL row, the master-summary "Total PYQs" cell, the
GRAND TOTAL and the header total from ONE counts map in one pass. The four levels
therefore cannot disagree BY CONSTRUCTION, where before they agreed only if every
hand edit and every re-total was performed correctly on every subject. The
cross-check below no longer hunts for arithmetic drift inside the document; it
asserts the one thing construction cannot guarantee — that the map itself totals
to what Task 1 confirmed.
```

```python
# ── TASK 3 — runs only after Task 2.5 passes, in the same script ──────────────
# `doc` and `counted` come from Task 2.5. Nothing is re-read and nothing is re-parsed.

if not counted:
    raise SystemExit(
        "HARD STOP: the counts map is empty. write_analysis_doc() treats an empty "
        "map as 'no counts supplied' and would emit an em-dash in every cell, "
        "silently producing a Phase-A document under a Phase-B filename.\n"
        "NEXT ACTION: confirm count_progress.json loaded and that Task 2 passed.")

# ZERO-COUNT RULE, satisfied by construction: the writer emits
# counts.get(triple, 0), so a taxonomy subtopic with no counted questions receives
# an explicit 0 and never an em-dash. "—" means "not yet counted"; "0" means
# "counted, none found", and Step 6 depends on the distinction (EC-P17).
for triple in taxonomy_triples:
    counted.setdefault(triple, 0)

# Cluster K's reader returns the RICH taxonomy shape; the writer takes the plain
# one. Convert order-preservingly — subject order and within-subject topic order
# are load-bearing (topic_idx is positional).
tax = {s: {t: list(v['subtopics']) for t, v in d['topics'].items()}
       for s, d in doc['taxonomy'].items()}

out_path = corpus_io.write_analysis_doc(
    tax, doc['exam_code'],
    subject_order=doc['subjects'],
    out_dir='/mnt/user-data/outputs',
    counts=counted)

# ── CROSS-CHECK — the one thing construction cannot assert ────────────────────
if sum(counted.values()) != confirmed_total:          # confirmed_total from Task 1
    raise SystemExit(
        "HARD STOP: Σ counts = %d but Task 1 confirmed %d. The regenerated doc "
        "would report a total the corpus does not support. Do NOT deliver."
        % (sum(counted.values()), confirmed_total))

# ── STRUCTURAL VERIFICATION — read the artefact back, never trust the write ───
back = corpus_io.read_analysis_doc(out_path)
if back['fingerprint'] != doc['fingerprint']:
    raise SystemExit(
        "HARD STOP: regeneration changed the taxonomy. The Analysis doc must carry "
        "the SAME taxonomy after Phase B as before it — Phase B writes counts, "
        "never structure.\n"
        "  before : %s\n"
        "  after  : %s" % (doc['fingerprint'], back['fingerprint']))

print("Task 3 OK — %d subtopics, sum = %d, fingerprint unchanged, ingest form in: %s"
      % (len(taxonomy_triples), sum(counted.values()), doc['ingest_form']))
```

```
THE FOUR LEVELS, and where each is now guaranteed:

  LEVEL 1 — SUBTOPIC CELLS       counts.get((section, topic, subtopic), 0)
  LEVEL 2 — PER-TOPIC TOTAL ROW  Σ over that topic's subtopics
  LEVEL 3 — MASTER SUMMARY       per-topic Σ, and GRAND TOTAL = Σ over the subject
  LEVEL 4 — HEADER "Total:"      Σ over the subject
All five figures are computed from `counted` inside write_analysis_doc(), in one
pass, from the same expression. There is no path by which they can disagree.
Verified on the first real exam: 6 subjects / 26 topics / 131 subtopics, header
totals == GRAND TOTALs == Σ counted, zero cells left as "—".

WHAT STILL REQUIRES A CHECK, and is checked above:
  • Σ counted == Task 1's confirmed total          — the map vs the corpus
  • fingerprint unchanged across regeneration      — counts written, not structure
  • counts map non-empty                           — an empty map is silently Phase A

WHAT THE READER CANNOT CHECK (recorded, not hidden): read_analysis_doc() returns
the taxonomy and its structural counts, never the per-subtopic PYQ counts — it
does not read the count column. So the regenerated NUMBERS cannot be re-verified
through Cluster K. They do not need to be, because they were never transcribed:
they are written from the same map this task asserts against Task 1. Do NOT add a
hand parser to re-read them; that is the fifth reader this version removed.

COUNTS MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 1 file.
    1. [ExamCode]_PYQ_Analysis.docx  (REGENERATED, with PYQ counts)
  No other files. count_progress.json is INTERNAL — do NOT deliver
  at completion. (It IS delivered at session breaks for resume only.)
  Run S10-2 pre-delivery checklist before present_files.

  The operator uploads it to the project's Files section, replacing the Phase-A
  copy. The platform will store it as extracted text under the same .docx name;
  that is expected and supported (GAP-2026-07-25-003). No operator action.
```

### S5-6 — Count progress JSON schema

```json
{
  "_meta": {
    "exam_code": "[ExamCode]",
    "phase": "B_counts",
    "files_processed": 150,
    "total_files": 200,
    "confirmed_total": 20000,
    "files_processed_list": [
      "[ExamCode]_12-Sep-2025_Shift-1_Sorted_Q1-Q100.docx",
      "[ExamCode]_13-Sep-2025_Shift-2_Sorted_Q1-Q100.docx"
    ]
  },
  "counts_by_year": {
    "('[Section 1 Name]', '[Topic A]', '[Subtopic A1]')": {
      "2019": 14, "2020": 9, "2021": 8, "2022": 50, "2023": 70,
      "2024": 46, "2025": 32
    }
  },
  "papers_per_year": {
    "2019": 19, "2020": 16, "2021": 8, "2022": 40,
    "2023": 39, "2024": 36, "2025": 46
  },
  "all_orphans": {},
  "_transport": {
    "upload_lane": ["[ExamCode]_10-Mar-2010_Shift-1_Sorted_Q1-Q100.docx"],
    "rejected": [
      {"name": "2007 paper", "reason": "native Google Doc — convert to .docx in Drive"}
    ],
    "fetch_failures": {
      "[ExamCode]_10-Mar-2010_Shift-1_Sorted_Q1-Q100.docx":
        "<the TransportFallback message, verbatim — it names the actual byte
          count and the cap read from blueprint_core.DRIVE_CAP at run time.
          Never write a cap literal here: a stale number copied from an example
          is exactly the drift one definition per constant exists to prevent>"
    }
  }
}
```

```
v2.21 — _transport is written by the SAME per-file save as the counts, so a
resumed session knows which papers Drive could not supply and re-requests only
those. Without it the resume path re-attempts every oversized paper, fails
again, and the operator re-uploads files that were already counted.
_transport is DIAGNOSTIC. It never affects a count and never gates Task 2 —
a paper counted via the upload lane is indistinguishable from one fetched
from Drive in counts_by_year, which is the point.
```

### S5-7 — Phase B session management

```
═══════════════════════════════════════════════════════════════════════
SESSION MANAGEMENT — for large corpora spanning multiple sessions
═══════════════════════════════════════════════════════════════════════

Phase B with 200+ papers at 5/batch = 40+ batches may span multiple
chat sessions due to context limits. Protocol:

FIRST SESSION:
  1. S5-1: list + filter + dedup Drive files
  2. S5-1a: Task 1 inventory → user confirmation
  3. S5-4: batch counting (5/batch) until context limit reached
  4. Save count_progress.json with:
     - _meta.files_processed, _meta.total_files
     - _meta.confirmed_total (the Task 1 confirmed number)
     - _meta.files_processed_list (filenames already counted)
     - accumulated counts_by_year and papers_per_year
  5. Print session handoff message:
     "Phase B session paused. Progress: [N]/[T] files processed.
      count_progress.json saved.
      To resume: download count_progress.json → upload to [ExamCode]
      project → trigger: PYQCount PYQ: <<same Drive link>>"

RESUME SESSION:
  1. Trigger: PYQCount PYQ: <<Drive link>>
  2. Detect count_progress.json in project knowledge.
  3. Load progress: restore counts_by_year, papers_per_year, confirmed_total.
  4. Re-list Drive files (S5-1 filtering + dedup).
  5. RE-RUN Task 1 (S5-1a): display full inventory again. User re-confirms.
     This catches any files added/removed between sessions.
     If confirmed_total differs from previous session → warn user and
     ask which total to use as accuracy target.
  6. Skip already-processed files (check against files_processed_list).
  7. Continue batch counting from where it left off.

COMPLETION:
  When all files processed:
  8. Run Task 2 (S5-4a), Task 2.5 (S5-4b), Task 3 (S5-5) in sequence.
  9. Deliver the updated Analysis doc.

TARGET: 8-10 batches per session (40-50 papers). Adjust based on
context usage — counting is lighter than classification, so more
batches fit per session than Phase 0b.

═══════════════════════════════════════════════════════════════════════
UPLOAD-LANE ARITHMETIC (v2.21) — STATE IT BEFORE THE RUN, NOT AT BATCH 6
═══════════════════════════════════════════════════════════════════════
The Drive lane is limited by CONTEXT (8-10 batches above). The upload lane is
limited by something else entirely, and it binds much sooner: the platform
accepts blueprint_core.CHAT_FILE_LIMIT files per conversation.

  bc.upload_batch_plan with (n_upload, BATCH_SIZE_COUNTS) returns
    batches_per_chat = CHAT_FILE_LIMIT // BATCH_SIZE_COUNTS = 20 // 5 = 4
    papers_per_chat  = 4 x 5 = 20
    chats_needed     = ceil(n_upload / 20)

So a corpus with 30 oversized papers needs TWO chat sessions for the upload
lane regardless of how much context is left — a fact the operator can plan
around only if they are told at S5-1, which is why plan_transport() prints it
before Task 1 rather than discovering it mid-run.

Never write 4 or 20 as a literal here. Both are derived from the engine, so a
change to CHAT_FILE_LIMIT or to BATCH_SIZE_COUNTS reaches every step at once.
The permanent fix for the upload lane is PYQCompress: compress those papers
once, replace them in Drive, and Steps 2b, 4 and 5 all fetch them normally
from then on.
```

### S5-8 — Phase B execution model

```
═══════════════════════════════════════════════════════════════════════
EXECUTION MODEL — 3 PHASES.  Tool calls = 3 + 1 listing + 1 probe + N drive papers
═══════════════════════════════════════════════════════════════════════

v1.3 (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION) corrects "3 tool calls per session".
That accounting was wrong for any Drive-lane run: it counted create_file, bash_tool
and delivery, and omitted the N connector calls the model must make IN ITS OWN TURNS
to acquire the papers. Those calls are the dominant cost of the step and the entire
subject of this GAP. Stating the cheap half as the whole cost is precisely what let an
unreachable acquisition step look like a solved problem for 20 days.

  PHASE A — MODEL TURNS (acquisition; CLASS T, never python)
    A0. DIRECT EGRESS PROBE — PYTHON, NOT A TOOL CALL, AND IT COMES FIRST.
        corpus_io.probe_direct_egress with (candidate, work_dir). If it returns ok the
        channel is 'direct': python fetched the bytes itself, nothing crossed the
        turn, there is no context cost and the whole corpus is admissible. It NEVER
        raises — ok=False is an ordinary state (folder not link-shared, or container
        egress excludes Google) and the run falls through to A2 unchanged.
        Framework_PYQCore EC-P43.
    A1. Google Drive:search_files(query="parentId = '<folder_id>'", pageSize=100)
        → paginate to exhaustion → keep every raw page → then, IN PYTHON,
        corpus_io.write_drive_listing with (pages, cache_path, folder_id, observed_count)
        where observed_count is the count YOU read off the connector response. It is
        an INDEPENDENT number, so the comparison can fail. A short listing HARD STOPS
        (EC-P41): EC-P39 catches zero and nothing caught 21-of-22. The records are
        cached VERBATIM — write_drive_listing never reshapes them.
    A2. S5-0 CHANNEL PROBE — reached ONLY when A0 returned ok=False.
        Download exactly ONE paper, the SMALLEST by fileSize.

        P4f DIVERGENCE, DECLARED. 'Smallest' is correct HERE and WRONG in Step 5.
        Step 4 is single-session and fetches the whole corpus in the same run, so the
        probe paper is fetched again anyway and the probe cost amortises to zero.
        Framework_MockTestAnalyse §S8-0 is batched across ~8 sessions with a
        recency-first admitted set, so the smallest paper is almost never fetched and
        its payload is discarded — measured, 107,968 characters and 54% of the budget
        for zero papers. It therefore probes admitted[0] instead. Neither file may
        change its rule without changing this paragraph in both; mock_sync_audit MS-13
        fails the build for a probe whose paper-selection rule is undeclared.

        Observe whether the result came back as a reference to a file or as bytes in
        the turn, then run probe_drive_channel(...) to PROVE it decodes and verifies.
    A3. Branch on the S5-0 verdict, and print plan_transport() BEFORE Task 1:
          channel 'spill'                            → Drive lane, no context cost.
          channel 'inline', within INLINE_BUDGET_CHARS → Drive lane.
          channel 'inline', over budget              → the overflow goes to the
                upload lane with bc.upload_batch_plan arithmetic stated up front.
    A4. Download every remaining DRIVE-lane paper. Record, per file, WHATEVER came
        back — a spill path or an inline payload. Do not normalise them.
  PHASE B — create_file: count_pipeline.py, injecting `list_fn` and `resolver`
        (plain lookups over the PHASE A results). No connector call appears in it.
  PHASE C — bash_tool: run it. Then Task 1 → user confirmation → counting.

"3 tool calls" describes PHASES B and C only. Record the probe verdict in
count_progress.json._transport.channel so a resumed session neither re-probes nor
silently switches lanes mid-corpus.


Phase B counting is a mechanical operation (heading parsing + Q-pattern
matching) — NOT a judgment task. It MUST be executed via Python script,
not manual paragraph-by-paragraph Claude reading in chat.

PER-SESSION EXECUTION:

  CALL 1 — create_file: Write count_pipeline.py containing:
    1. Drive enumeration via corpus_io.collect_corpus_files (S5-1) — captures
       fileSize and mimeType, paginates, screens and reports every reject
    2. Sorted-file filter + both duplicate HARD STOPs (S5-1), then
       plan_transport(papers, channel) — which calls bc.partition_by_transport
       with the S5-0 verdict and bc.upload_batch_plan
    3. Task 1: acquire each file via corpus_io.fetch_drive_docx with the PHASE A
       RESOLVER (guarded; TransportFallback -> upload lane), or via
       corpus_io.stage_drive_payload when PHASE A already holds the payload;
       parse with python-docx, count Q-patterns, build inventory table
    4. Heading parser functions (parse_taxonomy_level, is_taxonomy_heading,
       is_option, count_sorted_file — from S5-2, byte-identical)
    5. Batch counting loop (5/batch, accumulate counts_by_year)
    6. Orphan tracking and per-file attributed counts
    7. Save count_progress.json after EVERY FILE (S5-4) — the batch-level save
       remains only as a redundant flush
    8. Print Task 1 inventory table for user confirmation

  CALL 2 — bash_tool: Run count_pipeline.py
    → Downloads files, counts, saves progress, prints inventory

  CALL 3 — (after user confirms Task 1)
    Either: continue counting (next session's CALL 1 if more files)
    Or:     run Task 2 + Task 2.5 + Task 3 gates and deliver

  For the FINAL session (all files counted):
    CALL 1 — create_file: Write count_finalize.py containing:
      1. Load count_progress.json
      2. Task 2: compute grand total, display breakdown, compare
      3. Task 2.5 (S5-4b): corpus_io.load_taxonomy — ONE call that selects the
         taxonomy source, reads it and asserts identity against
         approval_record.json. Never a hand parser, never a bare Document(path)
         open, and never a separate gate call. Then the phantom / uncounted set
         comparison
      4. Task 3 (S5-5): merge counts onto the loaded taxonomy and REGENERATE via
         corpus_io.write_analysis_doc with (..., counts=), then read the result back and
         assert the fingerprint is unchanged. Do NOT edit the doc in place — the
         runtime receives extracted text and /mnt/project/ is read-only
      5. The regenerated .docx is written to /mnt/user-data/outputs/ by
         write_analysis_doc()'s own out_dir; nothing else saves it
    CALL 2 — bash_tool: Run count_finalize.py
    CALL 3 — present_files: Deliver the regenerated Analysis doc
             (EXACTLY 1 file — S10-1 --counts closed set.
              count_progress.json is NOT delivered at completion.
              Run S10-2 pre-delivery checklist before present_files.)

NOTE: Task 1 inventory display happens in chat (printed by the script).
User confirmation is a chat response. The script pauses after Task 1
output — Task 2/2.5/3 run only after user confirms and all files are
processed.

DEPENDENCY: python-docx must be installed (pip install python-docx
--break-system-packages). Google Drive MCP tools must be connected.
corpus_io.py and blueprint_core.py must be routed to PYQCount in routes.json.

DEPENDENCY (v1.3): `gdrive_search` and `gdrive_download_file` are CLASS T markers
performed by the MODEL. Never import them, never pass them, never call them from
python. python-docx and both engines are ordinary imports; the connector is not.

═══════════════════════════════════════════════════════════════════════
THE DRIVE RETRIEVAL ENVELOPE (v2.21, DEFECT N) — DOCUMENTED, NOT REDISCOVERED
═══════════════════════════════════════════════════════════════════════
The one-line "download via Drive MCP" concealed a three-stage contract that
every previous execution rediscovered by trial and error, with a different
improvisation each time. That is non-determinism in the hot path, and it is
exactly the kind of interpretive gap the framework replaces with a function.

The connector's result is EITHER a spill-file path OR an inline payload. WHICH ONE
IS A PROPERTY OF THE DEPLOYMENT, NOT OF THE FILE SIZE, and S5-0 MEASURES it.

v1.2 and earlier asserted here that "for any real paper the result EXCEEDS CONTEXT and
spills to a file under /mnt/user-data/tool_results/*.json". Measured 2026-08-15 on one
40,488-byte sorted paper: one deployment spilled it to a file, a second returned it
inline and created no spill file at all, and the two spill directories were different
directories. Never hardcode a spill directory and never test for one — a probe that
does reports 'inline' on a working spill channel and sends a fetchable corpus to
manual upload on every exam.

The shapes the payload can take, all of which decode_drive_payload accepts:

  1. raw bytes
  2. a spill-file path — in ANY directory the deployment chooses
  3. a LIST whose element [0]['text'] is itself a JSON STRING
  4. a dict {id, title, mimeType, content}, where content is base64
  5. that inner JSON string on its own
  6. bare base64 (accepted from the GAP-2026-08-15 release onward)

ONE implementation handles every shape — raw bytes, a spill path, the parsed
list or dict, or the inner JSON string:

    raw = corpus_io.decode_drive_payload applied to the payload

and corpus_io.fetch_drive_docx wraps decode with the two assertions that make
truncation detectable:

    len(raw) == the fileSize the listing reported
    raw starts with PK\x03\x04

The byte count is not belt-and-braces. A payload truncated at a ZIP member
boundary still opens as a VALID archive presenting FEWER QUESTIONS, so the
document parses cleanly, the count comes out low, and nothing anywhere reports
an error. Under Phase B's zero-tolerance standard that is the worst possible
failure: a wrong number that looks right.

Never hand-roll this decode in a generated count_pipeline.py.
```

---


---

# END OF Framework_PYQCount v1.5.1
