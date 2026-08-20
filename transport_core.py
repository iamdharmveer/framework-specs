#!/usr/bin/env python3
"""
transport_core.py — Step 5 (PYQExtract) DRIVE ACQUISITION AND TRANSPORT PLANNING.

WAVE 2 PART C, BATCH 9. Extracted VERBATIM from Framework_MockTestAnalyse.md's §S8-0
TRANSPORT PREFLIGHT fence (2026-08-20, v2.53.5). This file is IMPORTED AND EXECUTED,
NEVER READ — it is not routed by SKILL Rule 2 and costs a session nothing.

WHY THIS EXTRACTION HAPPENED WHEN IT DID
────────────────────────────────────────
This code was invisible. Four auditors extracted fenced python with a non-greedy regex
that ended its capture at the FIRST ``` in the body; this fence carries a triple
backtick inside a docstring, so it was cut mid-string, failed to parse, and was
discarded by each caller's `except SyntaxError: continue`. Nothing failed — the tools
simply never read it, and code that is never read produces no findings, so every report
said `findings: 0` over the whole Drive transport contract.

Release 2026.08.20.2 replaced those regexes with a line scanner and the block became
visible for the first time (measured: 261/264 fences parsed before, 263/263 after).
This release moves it where it can be TESTED as well as read: 8 functions, ZERO
top-level session flow, one derived constant. The same definition/flow split that
governed batches 2, 3 and 5 applies unchanged.

WHAT IS AND IS NOT HERE
───────────────────────
NOT here, deliberately: `gdrive_search` and `gdrive_download_file`. Those are CLASS T
markers — operations the MODEL performs in its own turn, not python. They stay in the
spec, where the reader can see that they are not callable code. Every function below
takes the RESULT of a CLASS T operation as an argument (`pages`, `probe_payload`,
`drive_payloads`, `resolver`), which is precisely why the block is extractable at all:
no function here performs a tool call, and none can.

THE STEP 4 DIVERGENCE IS DECLARED, NOT ACCIDENTAL
─────────────────────────────────────────────────
Framework_PYQCount §S5-0 defines its own `probe_drive_channel`, `plan_transport` and
`acquire_paper`. They differ from these on purpose — Step 4 is single-session, Step 5 is
batched across ~8 sessions — and the divergence is recorded, with a reason and a pinned
fingerprint for both sides, in XSPEC_DIVERGENCE_BASELINE.json. Moving this copy into an
engine does not dissolve that record: audit_deep's baseline check reads engine
definitions as well as spec fences, so the pin survives the extraction. If it did not,
this refactor would have quietly retired the only check watching those three pairs.

Companion floors: blueprint_core (partition_by_transport with consumed=,
base64_cost_chars, upload_batch_plan, INLINE_BUDGET_CHARS), corpus_io
(write_drive_listing, probe_direct_egress, fetch_drive_docx, stage_drive_payload,
collect_corpus_files, TransportFallback, ListingIntegrityError).

Run `python3 transport_core.py --self-test` for the fixtures.
"""
import json
import os
import re
import sys

import blueprint_core as bc
import corpus_io

__all__ = ['SESSION_INLINE_BUDGET', 'acquire_listing', 'probe_transport',
           'probe_drive_channel', 'plan_transport', 'acquire_paper',
           'read_transport_verdict', 'record_transport', 'log_session']


# ═══ FROM Framework_MockTestAnalyse.md §S8-0, fence L2645-2990 (v2.53.5) — VERBATIM ═══
# ── S8-0 TRANSPORT PREFLIGHT ─────────────────────────────────────────────────
# GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. Ported in CONTRACT from
# Framework_PYQCount S5-0, with four Step-5-specific deviations (P4a–P4e below)
# that exist because Step 4 is a SINGLE-session script step and Step 5 is a
# MULTI-session batched step. Porting S5-0 verbatim would be wrong here.

SESSION_INLINE_BUDGET = bc.INLINE_BUDGET_CHARS // 2
# P4c / EC-P36 — CHARGE THE PAYLOAD TWICE ON AN INLINE CHANNEL.
# bc.INLINE_BUDGET_CHARS prices INBOUND characters only: partition_by_transport
# sums bc.base64_cost_chars against it. On an inline channel Step 5 pays that cost
# a SECOND time, because the model receives the base64 in the tool result and must
# then RE-EMIT it into a python block for stage_drive_payload to decode.
# THIS DESCRIBES THE CONNECTOR LANE ONLY, AND IT IS NO LONGER THE ONLY LANE. Until
# EC-P43 the statement here read "there is no third route — the container's egress
# allowlist contains no Google domain". That was true of the deployment measured on
# 2026-08-15 and is NOT a property of the framework: the allowlist is configurable.
# When it reaches drive.google.com and the folder is link-shared, PHASE A/A0 fetches
# the bytes in python, nothing crosses the turn, and neither this halving nor the
# EC-P36 double charge applies. The halving below stays correct and mandatory
# WHENEVER the channel is 'inline'; it is inert on 'direct' and on 'spill'.
# Halving here rather than changing bc.INLINE_BUDGET_CHARS is deliberate: the
# shared constant is Step 4's too, and mutating it would silently re-partition a
# step this GAP does not touch. This is a DERIVED value, never a literal — the
# threshold still has exactly one definition, exactly as DRIVE_CAP does.


def acquire_listing(pages, cache_path, folder_id, observed_count):
    """PHASE A / A1 — persist DRIVE_LISTING_CACHE through the engine, and ASSERT it.

    `pages` is every RAW connector page for this folder, unmodified. `observed_count`
    is the total the model declares from the connector response — an INDEPENDENT
    number, which is the only reason the comparison is capable of failing.

    A short listing HARD STOPS (ListingIntegrityError, EC-P41). It is deliberately not
    a TransportFallback: a fallback means "try another lane", and there is no other
    lane for a corpus that cannot be enumerated correctly. EC-P39 already caught zero;
    nothing caught 21-of-22, and 21-of-22 is the dangerous one because §1-6 reports
    success on whatever survived and the missing year stays invisible for the life of
    the exam.

    The year span and any interior gaps are REPORTED, never stopped on — an exam may
    genuinely not have been held in a year and only the operator can tell that apart
    from a listing defect. Printing it here puts it on screen before paper 1.
    """
    report = corpus_io.write_drive_listing(pages, cache_path, folder_id, observed_count)
    print(f"\n  DRIVE LISTING  ({report['count']} record(s) cached, asserted against "
          f"{observed_count} declared)")
    if report['year_span']:
        print(f"    Year span         : {report['year_span'][0]}-{report['year_span'][1]}")
    if report['missing_years']:
        print(f"    ! Interior gaps   : {report['missing_years']} — REPORT ONLY. An exam "
              f"may not have been held in a year; confirm before Task 1.")
    else:
        print("    Interior gaps     : none")
    return report


def probe_transport(candidate, work_dir, recorded=None):
    """PHASE A / A0 -> A2 — decide the channel. DIRECT FIRST, then the connector.

    Returns (verdict_or_None, probe_consumed). A None verdict means the direct lane
    was unavailable and the caller must run the connector probe (A2) on admitted[0].

    EC-P43. The direct lane is PROVEN on a real paper and never predicted;
    corpus_io.probe_direct_egress never raises, because an unshared folder or a
    deployment without Google egress is an ORDINARY state and an exception here would
    turn a routine fallback into a halted run.

    EC-X5 / EC-P38 — a recorded verdict is REUSED, never re-probed, and `consumed` is
    then 0. Re-probing costs one paper's context every session for a fact that is a
    property of the deployment.
    """
    if recorded and recorded.get('channel'):
        print(f"\n  TRANSPORT VERDICT REUSED — channel "
              f"{recorded['channel'].upper()} (EC-X5); no probe this session.")
        return recorded, 0
    direct = corpus_io.probe_direct_egress(candidate, work_dir)
    if direct['ok']:
        print(f"\n  S8-0 A0 DIRECT EGRESS PROBE — {candidate['name']}")
        print(f"    Verified bytes on disk : {direct['path']}")
        print( "    Channel                : DIRECT — python fetched the bytes itself; "
               "nothing crossed the turn, so the whole corpus is admissible (EC-P43)")
        return {'channel': 'direct', 'probe_paper': candidate['name'],
                'probe_local_path': direct['path']}, 0
    print(f"\n  S8-0 A0 DIRECT EGRESS PROBE — unavailable: {direct['reason']}")
    print( "    Falling back to the connector lane. This is an ordinary state, not a "
           "failure: the run proceeds exactly as it did before EC-P43 existed.")
    return None, 0


def probe_drive_channel(probe_paper, probe_payload, arrived_inline, work_dir):
    """Classify the CONNECTOR Drive channel from ONE real download, and PROVE it decodes.

    REACHED ONLY WHEN THE DIRECT LANE IS UNAVAILABLE (PHASE A / A0, EC-P43). When
    corpus_io.probe_direct_egress succeeded the channel is 'direct', this function is
    never called, and probe_consumed is 0 — python holds verified bytes and nothing
    crossed the turn.

    `probe_paper` is admitted[0], NOT the smallest paper — see plan_transport's P4f.

    Identical contract to Framework_PYQCount S5-0. `arrived_inline` is the model's
    OBSERVATION about its own turn (PHASE A step A2), never a filesystem test.

    The probe PROVES the lane rather than predicting it: the payload is staged
    through the same engine path the whole run will use, so a channel that
    classifies cleanly but cannot produce verified bytes fails here, at paper 1,
    instead of at paper 12. Any TransportFallback propagates to the caller, which
    routes the corpus to the upload lane per EC-P35 / EC-X20.
    """
    local_path = corpus_io.stage_drive_payload(probe_payload, probe_paper, work_dir)
    channel = 'inline' if arrived_inline else 'spill'
    print(f"\n  S8-0 CHANNEL PROBE — {probe_paper['name']} "
          f"({probe_paper['fileSize']:,} bytes)")
    print(f"    Verified bytes on disk : {local_path}")
    print(f"    Channel                : {channel.upper()}"
          + ("  — payloads arrive in context; the Drive lane is bounded by context"
             if channel == 'inline' else
             "   — payloads land on disk; the Drive lane costs no context"))
    return {'channel': channel, 'probe_paper': probe_paper['name'],
            'probe_local_path': local_path}


def plan_transport(pending_recency_sorted, channel, session_budget, batch_size,
                   probe_consumed=0):
    """Decide what THIS SESSION fetches. Print it BEFORE the first batch.

    P4f — PROBE PAPER SELECTION DIVERGES FROM STEP 4, ON PURPOSE.
    Framework_PYQCount S5-0 probes the SMALLEST paper. That is correct THERE: Step 4 is
    single-session and fetches the whole corpus in the same run, so the probe cost is
    amortised to zero. Step 5 is batched across ~8 sessions and its admitted set is
    recency-first, so the smallest paper is almost never the one being fetched — its
    payload is decoded, proven, and thrown away.
    Measured on IIT_JAM_MATHEMATICS: probing the smallest (10-Feb-2013, 40,488 B) spent
    107,968 real characters, 54% of INLINE_BUDGET_CHARS, on a paper the admitted set
    does not contain, and session 1 processed ZERO papers. Probing admitted[0]
    (15-Feb-2026, 47,627 B) proves the lane AND delivers paper 1 for the same
    characters, so probe_consumed is 0 — the payload is not waste, it is paper 1.
    v2.50.0 inherited "SMALLEST" verbatim when S8-0 was ported in CONTRACT from S5-0;
    the four documented deviations P4a-P4e covered budget, persistence, halving,
    partition ordering and the PYQCompress text, and probe-paper selection was never
    reviewed. mock_sync_audit MS-13 now fails the build for a spec that carries a
    channel probe without declaring its probe-paper rule and any divergence.

    P4g / EC-P40 — THE PROBE IS A SPENDER, NOT A FREE CLASSIFIER.
    `probe_consumed` is budget ALREADY SPENT in this session before this partition is
    computed. Before it existed the partition was computed against the FULL budget as
    though the probe were free: probe 107,968 + admitted paper 127,008 = 234,976 real
    characters against a 200,000 ceiling, and this function printed "1 paper(s) fetch
    automatically". Values:
        probe ran this session, connector lane  -> bc.base64_cost_chars(probe fileSize)
        probe reused from _meta._transport      -> 0            (EC-X5 / EC-P38)
        probe re-run on resume                  -> charged in THAT session (EC-P38)
        probe raised TransportFallback          -> STILL CHARGED — the bytes arrived
        channel 'spill' or 'direct'             -> 0, and the parameter is inert
        probe IS admitted[0] (P4f)              -> 0, the payload is paper 1
    audit_callgraph C10 fails the build for a partition call preceded by a CLASS T
    acquisition without a non-defaulted consumed=.

    P4d / EC-X21 — THE INPUT MUST ALREADY BE RECENCY-SORTED. bc.partition_by_transport
    admits papers in the order it receives them until the budget would be exceeded,
    and corpus_io.collect_corpus_files returns DRIVE LISTING order. Measured on the
    22-paper IIT_JAM_MATHEMATICS corpus, same papers, same budget, only the order
    changed:
        partitioned BEFORE the recency sort -> 2017, 2021, 2014   (185,892 chars)
        partitioned AFTER  the recency sort -> 2026, 2025, 2024   (189,156 chars)
    That is not cosmetic. S8-1's whole processing-order rationale is that an early
    stop must leave section_rules.md reflecting the MOST RECENT patterns, and §1-6
    requires the latest five years. Partitioning the raw listing order on an inline
    channel can leave the §1-6 required set permanently unreached while the operator
    watches papers arrive successfully. Always sort first.

    P4a — ON AN INLINE CHANNEL STEP 5 DOES NOT ROUTE THE CORPUS TO UPLOAD.
    EC-P35's Step-4 resolution is "route the WHOLE corpus to the upload lane",
    which is right for a step that must finish in one session and wrong here.
    Step 5 already has BATCH_SIZE 3, a mandatory BATCH STOP and a documented
    Option B (download analysis_progress.json, open a fresh chat) — AND A FRESH
    CHAT RESETS THE CONTEXT BUDGET. So the budget is applied PER SESSION and the
    remainder is carried to the next session, not demanded as manual uploads. The
    upload lane stays the fallback for a paper that cannot fit even one session's
    budget, or that exceeds bc.DRIVE_CAP.

    `batch_size` is passed in rather than read from the module-level BATCH_SIZE, which
    S8-1 defines AFTER this section. A forward reference would be a name this spec's own
    checkers cannot resolve, and this GAP is about instructions the CI cannot read.
    Callers pass BATCH_SIZE; it still has exactly one definition, in S8-1.
    """
    part = bc.partition_by_transport(pending_recency_sorted, channel=channel,
                                     inline_budget=session_budget,
                                     consumed=probe_consumed)
    admitted, carried = part['auto'], part['deferred_for_context']
    oversize = [p for p in part['upload'] if (p.get('fileSize') or 0) > bc.DRIVE_CAP]
    print(f"\n  TRANSPORT PLAN  (channel: {part['channel']})")
    if part['channel'] == 'inline':
        # FIRST LINE, ALWAYS. The plan is not readable without knowing what was spent
        # before it was computed, and a probe reported after the admission count reads
        # as trivia rather than as the reason the count is what it is.
        print(f"    Probe consumed      : {part['consumed']:,} of {session_budget:,} "
              f"chars this session — EC-P40, EC-P36 double charge applies")
    print(f"    Pending this corpus : {len(pending_recency_sorted)} paper(s)")
    print(f"    Drive lane, session : {len(admitted)} paper(s) fetch automatically")
    if part['channel'] == 'direct':
        print(f"    Context cost        : 0 — python fetched the bytes itself over "
              f"container egress; nothing crossed the turn (EC-P43)")
    if part['channel'] == 'inline':
        print(f"    Context cost        : {part['inline_chars']:,} of "
              f"{part['effective_budget']:,} chars remaining after the probe "
              f"(bc.INLINE_BUDGET_CHARS // 2 — charged twice, EC-P36)")
        print(f"    Carried to later    : {len(carried)} paper(s) deferred FOR CONTEXT, "
              f"not for size — EC-P36/EC-X9")
    if part['channel'] == 'inline' and not admitted:
        # FIX F / G-9. `Sessions needed: ~0` while 22 papers pend is not merely wrong,
        # it is inverted in meaning, and the v2.39 changelog records what that does:
        # "a gate that cannot fire correctly trains operators to ignore gates."
        _cheapest = min(pending_recency_sorted,
                        key=lambda q: q.get('fileSize') or 0, default=None)
        print("\n  ! TRANSPORT INFEASIBLE THIS SESSION (EC-P37 upload-lane fallback)")
        print(f"    Session budget      : {session_budget:,} chars")
        print(f"    Already consumed    : {part['consumed']:,} chars")
        print(f"    Remaining           : {part['effective_budget']:,} chars")
        if _cheapest is not None:
            print(f"    Cheapest pending    : {_cheapest.get('name')} "
                  f"({bc.base64_cost_chars(_cheapest.get('fileSize')):,} chars)")
        print("    No paper fits this session's remaining budget. Per EC-P37 the upload")
        print("    lane is the fallback for a paper that cannot fit even ONE session.")
        print("    PYQCompress is NOT the remedy — these papers are far under DRIVE_CAP.")
        print("    If this is a fresh chat and the number above is still zero, the direct")
        print("    egress lane (EC-P43) is the fix: share the Drive folder as 'Anyone")
        print("    with the link' and allow drive.google.com in the container egress.")
    elif part['channel'] == 'inline':
        sessions = -(-len(pending_recency_sorted) // max(1, len(admitted)))
        print(f"    Sessions needed     : ~{sessions} — continue via Option B in a "
              f"FRESH chat, which resets the budget (EC-P37). These papers are NOT "
              f"manual uploads.")
    if oversize:
        plan = bc.upload_batch_plan(len(oversize), batch_size)
        print(f"    Upload lane         : {len(oversize)} paper(s) exceed the "
              f"{bc.DRIVE_CAP:,}-byte connector cap — chat accepts "
              f"{bc.CHAT_FILE_LIMIT} files per conversation, so "
              f"{plan['chats_needed']} chat session(s).")
        print(f"    Permanent fix for those: run PYQCompress on them once and replace "
              f"them in Drive.")
    # P4e — PYQCompress is the remedy for SIZE and for nothing else. On this GAP the
    # papers are 40-49 KB against a 10 MiB cap, 213x under; recommending compression
    # for a channel or context deferral sends the operator to do work that cannot
    # help. Never print it under EC-P35/EC-P36 deferrals.
    return part


def acquire_paper(paper_ref, drive_payloads, resolver, work_dir, needs_upload):
    """S8-1 batch-loop acquisition. Returns a local path, or None -> upload lane.

    THIS IS THE ACQUISITION CONTRACT AND IT LIVES IN A ```python FENCE ON PURPOSE.
    Every AST check in the repo skips a fence that does not compile; the CLASS T
    stubs of this very file sat in one until v2.50.0, which is why C6 reported zero
    findings against two live violations for the whole life of the defect.

    `resolver` performs no tool call — it is a lookup over payloads PHASE A already
    materialised — so this function raises no NameError and cannot reach the
    connector. Every failure arrives as TransportFallback and degrades to the upload
    lane; a transport failure is NEVER fatal to the run.
    """
    if paper_ref['source'] != 'gdrive':
        return paper_ref['path']
    try:
        return corpus_io.fetch_drive_docx(resolver, paper_ref, work_dir)
    except corpus_io.TransportFallback as exc:
        print(f"    ! Drive fetch unavailable — {exc}")
        print(f"    → routing to upload lane: {paper_ref['name']}")
        needs_upload.append(paper_ref)
        return None


def read_transport_verdict(progress):
    """EC-X5 / EC-X7 — reuse a recorded channel; probe only when there is none.

    Returns the recorded verdict dict, or None when this is a fresh corpus or a
    pre-patch progress file. A pre-patch file is VALID INPUT and is never discarded:
    the absent key simply means "probe as if fresh, then record".
    """
    return (progress.get('_meta') or {}).get('_transport')


def record_transport(progress, verdict, admitted, carried, oversize):
    """P4b — persist the verdict in _meta so a resumed session cannot re-decide.

    Step 5 is 8 sessions minimum on a 22-paper corpus. Without this, every session
    re-decides transport from scratch and re-probes, paying one paper's context each
    time. _meta is already serialised by save_progress and load_progress already
    selects the most-advanced copy by _meta.papers_processed, so this needs no new
    handling anywhere.
    """
    meta = progress.setdefault('_meta', {})
    prev = meta.get('_transport') or {}
    if prev.get('channel') and prev['channel'] != verdict['channel']:
        # EC-P38 / EC-X6 — a transition is legitimate (a resumed session may be on a
        # different deployment) but it is NEVER silent.
        print(f"  ! TRANSPORT CHANNEL CHANGED: {prev['channel']} -> "
              f"{verdict['channel']}. Recorded; continuing.")
    prev_log = prev.get('session_log') or []
    meta['_transport'] = {
        'channel': verdict['channel'],
        'probe_paper': verdict.get('probe_paper'),
        'session_budget': SESSION_INLINE_BUDGET,
        # G-8. RENAMED from 'papers_admitted' in v2.51.0. This field is written BEFORE
        # the acquisition loop runs, so it is a PLAN and never a result — in the
        # reference incident it recorded the 2026 paper as 'admitted' although that
        # paper was never fetched. No corruption followed, because run_batch_loop skips
        # on _meta.papers_processed which save_progress writes per paper, but a forecast
        # named as a fact is a trap for the next reader and for every gap investigation.
        'papers_planned': [p['id'] for p in admitted],
        # Readers MUST tolerate the old key for one release (EC-P38: a pre-patch
        # progress file is VALID INPUT and is never discarded). Read it as
        #     planned = t.get('papers_planned', t.get('papers_admitted', []))
        'deferred_context': [p['id'] for p in carried],
        'deferred_size': [p['id'] for p in oversize],
        'session_log': prev_log,
    }
    return meta['_transport']


def log_session(progress, session_index, spec_read_mode, probe_run, chars_consumed,
                papers_fetched, papers_processed, ended_at):
    """Append what this session ACTUALLY did. Additive; a pre-patch file stays valid.

    GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / G-8. Nothing recorded whether the probe
    ran, how many characters were really consumed, whether the spec was read in full or
    reduced, or whether the session ended at a batch boundary or at exhaustion. A
    resumed session — and every future gap investigation — was blind to all of it, which
    is why reconstructing the reference incident required the chat transcript rather
    than the artefact the step itself produces.

    `ended_at` is one of: 'batch_boundary', 'corpus_complete', 'session_exhausted'.
    """
    import datetime as _dt
    t = progress.setdefault('_meta', {}).setdefault('_transport', {})
    t.setdefault('session_log', []).append({
        'session_index': session_index,
        'started_utc': _dt.datetime.now(_dt.timezone.utc).isoformat(),
        'spec_read_mode': spec_read_mode,        # 'full' | 'reduced'  (see §S8-0b)
        'probe_run': bool(probe_run),
        'chars_consumed': int(chars_consumed or 0),
        'papers_fetched': list(papers_fetched or []),
        'papers_processed': list(papers_processed or []),
        'ended_at': ended_at,
    })
    return t['session_log']


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════
# WHY THESE FIXTURES DID NOT EXIST BEFORE. This block lived in a spec fence that four
# auditors could not parse, so nothing read it and nothing could test it. It is the
# acquisition path for every one of ~200 exams, and its failure modes are the quiet
# kind: a short listing that looks like a small corpus, a probe charged as free, a
# partition computed in listing order instead of recency order. None of those raise.
#
# EVERY FIXTURE BELOW INJECTS ITS DEPENDENCIES BY SWAPPING MODULE GLOBALS, never by
# touching the filesystem or the network. GAP-2026-08-17-B4-ENV-SKEW: a fixture that
# needs a writable /mnt or a live connector is a fixture that SKIPS in CI, and a
# skipped assertion is indistinguishable from a passing one in the printed result.
# ═══════════════════════════════════════════════════════════════════════════════

class _FakeCIO:
    """Stand-in for corpus_io. Records calls; raises exactly what is asked of it."""

    TransportFallback = corpus_io.TransportFallback
    ListingIntegrityError = corpus_io.ListingIntegrityError

    def __init__(self, **behaviour):
        self.b = behaviour
        self.calls = []

    def write_drive_listing(self, pages, path, folder_id, observed_count):
        self.calls.append(('write_drive_listing', folder_id, observed_count))
        if 'listing_raises' in self.b:
            raise self.b['listing_raises']
        return self.b.get('listing', {'count': observed_count, 'year_span': None,
                                      'missing_years': []})

    def probe_direct_egress(self, paper, dest_dir, getter=None):
        self.calls.append(('probe_direct_egress', paper.get('name')))
        return self.b.get('direct', {'ok': False, 'reason': 'not shared'})

    def stage_drive_payload(self, payload, paper, dest_dir):
        self.calls.append(('stage_drive_payload', paper.get('name')))
        if 'stage_raises' in self.b:
            raise self.b['stage_raises']
        return self.b.get('staged_path', '/tmp/zz_probe.docx')

    def fetch_drive_docx(self, download_fn, paper, dest_dir):
        self.calls.append(('fetch_drive_docx', paper.get('name')))
        if 'fetch_raises' in self.b:
            raise self.b['fetch_raises']
        return self.b.get('fetched_path', '/tmp/zz_paper.docx')


def _quiet(fn, *a, **k):
    """Run fn capturing stdout; return (result, printed_text)."""
    import io as _io
    import contextlib as _cl
    buf = _io.StringIO()
    with _cl.redirect_stdout(buf):
        out = fn(*a, **k)
    return out, buf.getvalue()


def self_test():
    passed, fails = 0, []

    def check(name, ok):
        nonlocal passed
        if ok:
            passed += 1
        else:
            fails.append(name)

    def with_cio(fake, fn, *a, **k):
        real = globals()['corpus_io']
        globals()['corpus_io'] = fake
        try:
            return _quiet(fn, *a, **k)
        finally:
            globals()['corpus_io'] = real

    P = [{'id': 'p26', 'name': '2026 paper.docx', 'fileSize': 47_627, 'source': 'gdrive'},
         {'id': 'p25', 'name': '2025 paper.docx', 'fileSize': 45_000, 'source': 'gdrive'},
         {'id': 'p24', 'name': '2024 paper.docx', 'fileSize': 44_000, 'source': 'gdrive'},
         {'id': 'p13', 'name': '2013 paper.docx', 'fileSize': 40_488, 'source': 'gdrive'}]

    # ── acquire_listing (EC-P41) ─────────────────────────────────────────────
    # The listing is the ONLY enumeration of the corpus. EC-P39 already caught zero;
    # nothing caught 21-of-22, and 21-of-22 is the dangerous one because every later
    # step reports success over whatever survived.
    _f = _FakeCIO(listing={'count': 22, 'year_span': (2005, 2026),
                           'missing_years': [2011, 2019]})
    rep, out = with_cio(_f, acquire_listing, [{'files': []}], '/tmp/zz.json', 'FID', 22)
    check('listing_report_is_returned_verbatim', rep['count'] == 22)
    check('listing_year_span_is_printed', '2005-2026' in out)
    check('listing_interior_gaps_are_reported_not_stopped_on',
          '[2011, 2019]' in out and 'REPORT ONLY' in out)
    _f2 = _FakeCIO(listing={'count': 22, 'year_span': (2005, 2026), 'missing_years': []})
    _, out2 = with_cio(_f2, acquire_listing, [{'files': []}], '/tmp/zz.json', 'FID', 22)
    check('listing_no_gaps_says_so_explicitly', 'Interior gaps     : none' in out2)
    # A SHORT LISTING IS A HARD STOP, never a fallback: there is no other lane for a
    # corpus that cannot be enumerated. This asserts the exception PROPAGATES — a
    # `try/except` added here later would silently restore the 21-of-22 defect.
    _f3 = _FakeCIO(listing_raises=corpus_io.ListingIntegrityError('21 of 22'))
    try:
        with_cio(_f3, acquire_listing, [{'files': []}], '/tmp/zz.json', 'FID', 22)
        check('short_listing_hard_stops', False)
    except corpus_io.ListingIntegrityError:
        check('short_listing_hard_stops', True)
    except Exception:
        check('short_listing_hard_stops', False)

    # ── probe_transport: direct lane first, recorded verdict reused ──────────
    # EC-X5/EC-P38: re-probing costs one paper's context EVERY session for a fact that
    # is a property of the deployment. The reuse path must not call the connector.
    _f4 = _FakeCIO()
    (v, consumed), out = with_cio(_f4, probe_transport, P[0], '/tmp',
                                  {'channel': 'spill', 'probe_paper': 'x'})
    check('recorded_verdict_is_reused', v['channel'] == 'spill' and consumed == 0)
    check('reused_verdict_performs_no_probe', _f4.calls == [])
    check('reuse_is_announced_with_its_reason', 'EC-X5' in out)

    _f5 = _FakeCIO(direct={'ok': True, 'path': '/tmp/direct.docx'})
    (v5, c5), out5 = with_cio(_f5, probe_transport, P[0], '/tmp', None)
    check('direct_lane_wins_when_available', v5['channel'] == 'direct' and c5 == 0)
    check('direct_lane_records_the_probe_paper', v5['probe_paper'] == P[0]['name'])
    check('direct_lane_states_zero_turn_cost', 'nothing crossed the turn' in out5)

    _f6 = _FakeCIO(direct={'ok': False, 'reason': 'folder not link-shared'})
    (v6, c6), out6 = with_cio(_f6, probe_transport, P[0], '/tmp', None)
    check('direct_unavailable_returns_None_verdict', v6 is None and c6 == 0)
    # An unshared folder is ORDINARY. Printing it as a failure is how an operator
    # abandons a run that was about to work.
    check('direct_unavailable_is_framed_as_ordinary',
          'ordinary state, not a' in out6 and 'folder not link-shared' in out6)

    # ── probe_drive_channel: an OBSERVATION, never a filesystem test ─────────
    _f7 = _FakeCIO(staged_path='/tmp/probe.docx')
    v7, _ = with_cio(_f7, probe_drive_channel, P[0], b'payload', True, '/tmp')
    check('arrived_inline_true_classifies_inline', v7['channel'] == 'inline')
    v8, _ = with_cio(_FakeCIO(staged_path='/tmp/probe.docx'),
                     probe_drive_channel, P[0], b'payload', False, '/tmp')
    check('arrived_inline_false_classifies_spill', v8['channel'] == 'spill')
    # The probe PROVES the lane. A channel that classifies cleanly but cannot produce
    # verified bytes must fail at paper 1, not at paper 12.
    _f9 = _FakeCIO(stage_raises=corpus_io.TransportFallback('cannot decode'))
    try:
        with_cio(_f9, probe_drive_channel, P[0], b'x', True, '/tmp')
        check('probe_failure_propagates_to_the_caller', False)
    except corpus_io.TransportFallback:
        check('probe_failure_propagates_to_the_caller', True)
    except Exception:
        check('probe_failure_propagates_to_the_caller', False)

    # ── plan_transport ───────────────────────────────────────────────────────
    # P4g / EC-P40 — THE PROBE IS A SPENDER. Before probe_consumed existed the
    # partition was computed against the full budget as though the probe were free:
    # 107,968 + 127,008 = 234,976 real chars against a 200,000 ceiling, printed as
    # "1 paper(s) fetch automatically". Same corpus, same budget, only the charge
    # differs — so this pair isolates exactly that argument.
    free_plan, _ = _quiet(plan_transport, P, 'inline', 200_000, 3, 0)
    charged_plan, out_c = _quiet(plan_transport, P, 'inline', 200_000, 3, 107_968)
    check('probe_consumed_reduces_the_admitted_set',
          len(charged_plan['auto']) < len(free_plan['auto']))
    check('probe_charge_is_reported_first_and_named',
          'Probe consumed' in out_c and 'EC-P40' in out_c)
    check('probe_charge_reaches_the_partition',
          charged_plan['consumed'] == 107_968)

    # P4d / EC-X21 — the input must ALREADY be recency-sorted. partition_by_transport
    # admits in the order it receives, so listing order silently admits the wrong years
    # while the operator watches papers arrive successfully.
    reversed_plan, _ = _quiet(plan_transport, P[::-1], 'inline', 120_000, 3, 0)
    sorted_plan, _ = _quiet(plan_transport, P, 'inline', 120_000, 3, 0)
    check('partition_follows_input_order_so_callers_must_sort',
          [p['id'] for p in sorted_plan['auto']]
          != [p['id'] for p in reversed_plan['auto']])
    check('recency_first_input_admits_the_newest_papers',
          sorted_plan['auto'][0]['id'] == 'p26')

    # EC-P43 — on the direct lane the corpus is not context-bound at all.
    direct_plan, out_d = _quiet(plan_transport, P, 'direct', 200_000, 3, 0)
    check('direct_channel_admits_the_whole_corpus', len(direct_plan['auto']) == len(P))
    check('direct_channel_reports_zero_context_cost', 'Context cost        : 0' in out_d)

    # FIX F / G-9 — "Sessions needed: ~0" while papers pend is inverted in meaning, and
    # a gate that cannot fire correctly trains operators to ignore gates.
    _, out_inf = _quiet(plan_transport, P, 'inline', 200_000, 3, 199_000)
    check('infeasible_session_says_so_instead_of_zero_sessions',
          'TRANSPORT INFEASIBLE THIS SESSION' in out_inf
          and 'Sessions needed' not in out_inf)
    check('infeasible_session_names_the_cheapest_pending_paper',
          '2013 paper.docx' in out_inf)
    # P4e — PYQCompress is the remedy for SIZE and nothing else. These papers are 213x
    # under the cap; sending the operator to compress them is work that cannot help.
    check('infeasible_session_does_not_recommend_compression',
          'PYQCompress is NOT the remedy' in out_inf)
    check('infeasible_session_points_at_the_direct_lane', 'EC-P43' in out_inf)

    # The upload lane is for SIZE. bc.DRIVE_CAP is the boundary, and it must be the
    # boundary that is tested rather than a number copied next to it.
    big = P + [{'id': 'huge', 'name': 'huge.docx', 'source': 'gdrive',
                'fileSize': bc.DRIVE_CAP + 1}]
    _, out_big = _quiet(plan_transport, big, 'spill', 200_000, 3, 0)
    check('oversize_paper_routes_to_the_upload_lane', 'Upload lane' in out_big)
    check('oversize_advice_is_compression', 'run PYQCompress on them once' in out_big)

    # ── acquire_paper ────────────────────────────────────────────────────────
    check('local_paper_bypasses_the_connector_entirely',
          acquire_paper({'source': 'local', 'path': '/tmp/local.docx',
                         'name': 'l'}, {}, None, '/tmp', []) == '/tmp/local.docx')
    _fa = _FakeCIO(fetched_path='/tmp/got.docx')
    got, _ = with_cio(_fa, acquire_paper, dict(P[0]), {}, object(), '/tmp', [])
    check('gdrive_paper_is_fetched_through_the_engine', got == '/tmp/got.docx')
    # A transport failure is NEVER fatal — it degrades to the upload lane, and the
    # paper must land in needs_upload or it is silently dropped from the corpus.
    _needs = []
    _fb = _FakeCIO(fetch_raises=corpus_io.TransportFallback('403'))
    res, out_f = with_cio(_fb, acquire_paper, dict(P[0]), {}, object(), '/tmp', _needs)
    check('fetch_failure_returns_None_not_an_exception', res is None)
    check('failed_paper_is_added_to_the_upload_lane',
          [p['id'] for p in _needs] == ['p26'])
    check('fetch_failure_is_announced', 'routing to upload lane' in out_f)

    # ── read_transport_verdict — a pre-patch progress file is VALID INPUT ────
    check('absent_meta_reads_as_no_verdict', read_transport_verdict({}) is None)
    check('pre_patch_meta_reads_as_no_verdict',
          read_transport_verdict({'_meta': {'papers_processed': 3}}) is None)
    check('null_meta_does_not_raise',
          read_transport_verdict({'_meta': None}) is None)
    check('recorded_verdict_round_trips',
          read_transport_verdict(
              {'_meta': {'_transport': {'channel': 'direct'}}})['channel'] == 'direct')

    # ── record_transport ─────────────────────────────────────────────────────
    # G-8. The field was RENAMED from papers_admitted to papers_planned because it is
    # written BEFORE the acquisition loop: in the reference incident it recorded the
    # 2026 paper as 'admitted' although that paper was never fetched. A forecast named
    # as a fact is a trap for every later gap investigation.
    prog = {}
    t, _ = _quiet(record_transport, prog, {'channel': 'inline', 'probe_paper': 'x'},
                  P[:2], P[2:3], P[3:])
    check('verdict_is_persisted_under_meta_transport',
          prog['_meta']['_transport'] is t)
    check('forecast_is_named_papers_planned_not_admitted',
          t['papers_planned'] == ['p26', 'p25'] and 'papers_admitted' not in t)
    check('deferrals_are_split_by_REASON_context_vs_size',
          t['deferred_context'] == ['p24'] and t['deferred_size'] == ['p13'])
    check('session_budget_is_recorded_with_the_verdict',
          t['session_budget'] == SESSION_INLINE_BUDGET)
    # EC-P38 / EC-X6 — a channel transition is legitimate (a resumed session may be on
    # a different deployment) but it is NEVER silent.
    _, out_sw = _quiet(record_transport, prog, {'channel': 'direct'}, [], [], [])
    check('channel_transition_is_announced', 'TRANSPORT CHANNEL CHANGED' in out_sw)
    check('same_channel_is_not_announced',
          'TRANSPORT CHANNEL CHANGED' not in
          _quiet(record_transport, prog, {'channel': 'direct'}, [], [], [])[1])

    # ── log_session — the record that made the reference incident reconstructable ──
    prog2 = {}
    _quiet(record_transport, prog2, {'channel': 'inline'}, [], [], [])
    log, _ = _quiet(log_session, prog2, 1, 'full', True, 107_968, ['p26'], [], 'session_exhausted')
    check('session_log_records_one_entry', len(log) == 1)
    check('session_log_captures_what_was_blind_before',
          log[0]['spec_read_mode'] == 'full' and log[0]['probe_run'] is True
          and log[0]['chars_consumed'] == 107_968
          and log[0]['ended_at'] == 'session_exhausted')
    log2, _ = _quiet(log_session, prog2, 2, 'reduced', False, 0, [], ['p26'], 'batch_boundary')
    check('session_log_appends_and_never_overwrites',
          len(log2) == 2 and log2[0]['session_index'] == 1)
    # record_transport runs at the START of every session and must not wipe the log a
    # previous session wrote — that is the whole point of persisting it.
    _quiet(record_transport, prog2, {'channel': 'inline'}, [], [], [])
    check('record_transport_preserves_a_prior_session_log',
          len(prog2['_meta']['_transport']['session_log']) == 2)

    # ── META-ASSERTION ───────────────────────────────────────────────────────
    # A conditional assertion that silently skips is indistinguishable, in the printed
    # result, from one that passed (GAP-2026-08-17-B4-ENV-SKEW). A count is the
    # cheapest oracle for "did anything vanish?".
    EXPECTED_CHECKS = 48
    total = passed + len(fails)
    if total != EXPECTED_CHECKS:
        fails.append(f'suite_ran_every_check (ran {total}, expected {EXPECTED_CHECKS} — '
                     f'an assertion was SKIPPED or added without updating '
                     f'EXPECTED_CHECKS; a skipped check is not a passing one)')
    else:
        passed += 1

    print(f'transport_core self-test: {passed} passed, {len(fails)} failed'
          + ('  — ' + '; '.join(fails) if fails else ''))
    return not fails


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print('transport_core.py — Step 5 Drive acquisition engine. Run with --self-test.')
