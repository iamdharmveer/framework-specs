#!/usr/bin/env python3
"""
LOAD-AND-VERIFY GATE  (runs inside a freshly-cloned framework repo)

Verifies the ENTIRE framework (every file in MANIFEST.json) on every run:
PRESENT + BYTE-EXACT (sha256) + expected VERSION (.md header) + WHOLE
(.md END-sentinel + exact line count). Because the whole framework is verified,
an imperfect routes.json can never cause a missing/partial dependency at runtime.

Contract:
  - Exit 0 AND write .verified  -> only when EVERY tracked file passes.
  - Exit 1 (HARD STOP)          -> on ANY failure. Caller MUST NOT proceed
                                   from memory / project knowledge.

PROJECT-FIRST OVERRIDES (2026.08.03.9)
  Specs are project-first: a Framework_*.md in the exam project's Files section
  overrides the repo copy (see spec_source.py). The resolved corpus in
  /tmp/fw_effective therefore contains specs that CANNOT match MANIFEST.json —
  the manifest describes the repo, and an override is by definition different.

  SKILL RULE 2 runs `bootstrap.py --trigger <Step>` from that overlay. Before
  2026.08.03.9 this reported the override as `sha256 MISMATCH` and hard-stopped
  for EVERY trigger, not just the overridden one, printing an instruction to
  abandon the run — contradicting SKILL rule 4 and Framework_DeliveryFooter §2A,
  which both promise a project-first run never halts.

  So: if a `.spec_provenance.json` written by spec_source.py sits beside the
  manifest, files it lists are reported as PROJECT-UNVERIFIED instead of
  MISMATCH, and do not halt.

  THIS IS NOT A BYPASS.
    - A listed file is still hashed, and must match the sha the RESOLVER
      recorded. Tampering with the overlay after resolution still HARD-STOPS.
    - Only `.md` specs may be listed. An engine can never be excused.
    - A file NOT listed that fails any check still HARD-STOPS, unchanged.
    - The completion banner says VERIFIED only when nothing was overridden;
      otherwise it says PARTIALLY VERIFIED and names every unverified spec.
  What is impossible, and is not attempted, is verifying an override against
  the repo: there is no reference to verify it against.

--trigger is optional and advisory: if given and known, the gate prints the
step's entry files SPLIT BY ROLE — .md specs are to be READ IN FULL; .py engines
are to be EXECUTED via `import` inside the spec's code blocks and must NOT be
read into context (an engine can be thousands of lines; reading it wastes the
session's context for zero benefit — the split exists because a route lists
BOTH kinds and the old single-line advisory said "read IN FULL" for all of
them). Verification always covers all files regardless of trigger.

--receipt (2026.11.02, GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY P1) with --trigger prints
one READ RECEIPT line per routed .md spec — {spec, lines, sha256, end_sentinel} — into the
run log. Reading a spec in full is the framework's own rule; a session once worked from
"trimmed working copies" and nothing recorded it. The receipt makes the spec a run was
held to VISIBLE (the delivery footer repeats it); it cannot make skipped reading impossible.

READ CAPACITY (2026.11.06, GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY). Measured 2026-11-06 on
the Claude cloud-session surface: a bash result of >= ~40,000 chars is diverted to a file the
session cannot read back whole; 300 lines / ~20 KB came back inline 43 times in a row; specs
cost 2.3 B/tok, not 4; a sub-agent holding the 870 KB Step 7 spec compacted SILENTLY at
~790,000 tok. So reading is served here, not improvised: `--read K` prints one chunk of
<= 300 lines / <= 28,000 B (spec_sections.chunk_plan) with READ-ANCHOR codes on chunk 1, every
8th and the last, and `--retention` checks that the session can still reproduce them — the
only observable sign that the spec is still in its context. The surface also has no
/mnt/project and stores attachments under /mnt/user-data/attachments: `--stage-inputs`,
`--stage-project-docs`, `--stage-doc` and `--stage-status` put the inputs where the specs read them. `--worker-report`
and `--worker-prompt` are the orchestrator/worker hand-off for Step 7 (OD-2026-11-06).
State lives in <cwd>/.read_state/. Paths are overridable for hermetic tests: FW_PROJECT_DIR,
FW_UPLOADS_DIR, FW_ATTACH_DIR, FW_HOME.

Usage:
    python3 bootstrap.py                     # verify whole framework
    python3 bootstrap.py --trigger MockDeliver
    python3 bootstrap.py --trigger MockCreate --receipt
    python3 bootstrap.py --trigger TestCreate --progress P --read K     # K = 1..N
    python3 bootstrap.py --retention "01=ABCDEFG 02=..." [--when after-read]
    python3 bootstrap.py --stage-inputs | --stage-project-docs | --stage-status | --stage-doc NAME --from PATH|--typed
    python3 bootstrap.py --self-test
"""
import argparse, hashlib, json, math, os, re, secrets, shutil, sys, time

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def fail(msg):
    print(f"[HARD STOP] {msg}")
    print("Do NOT generate anything from memory or project knowledge. Stop here.")
    sys.exit(1)

def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [ln.rstrip("\n") for ln in f]

def ensure_compression_tools(trigger):
    """Best-effort provisioning of pngquant + optipng for TMAX (mode='max') runs.

    v2026.08.25 (GAP-2026-08-18-PYQCOMPRESS-UNDERCOMPRESSION, follow-up). The
    Framework_PYQCompress v2.0.0 governor palette-quantizes PNG output through
    corpus_io._quantize_png, which is strongest with the pngquant and optipng
    binaries and degrades gracefully to PIL FASTOCTREE without them (~10-20%
    weaker on PNG-heavy papers). The execution container resets every session,
    so the binaries must be provisioned at bootstrap or they are never there.

    THIS IS PROVISIONING, NOT VERIFICATION. It runs only AFTER the verify gate
    has passed, it is scoped to compression triggers so every other step pays
    zero wall time, and NO outcome here can change the gate's exit code or the
    .verified contract — a failed install is a quality note, never a halt,
    because the engine's PIL fallback keeps PYQCompress fully functional.
    """
    if trigger is not None and 'compress' not in trigger.lower():
        return                      # not a compression session — silent, zero cost
    import shutil as _sh
    import subprocess as _sp
    try:
        missing = [t for t in ('pngquant', 'optipng') if not _sh.which(t)]
        if not missing:
            print("[tools] pngquant + optipng present — TMAX runs at full strength")
            return
        r = _sp.run(['apt-get', 'install', '-y', '-qq'] + missing,
                    capture_output=True, timeout=180)
        if r.returncode != 0:
            _sp.run(['apt-get', 'update', '-qq'], capture_output=True, timeout=180)
            r = _sp.run(['apt-get', 'install', '-y', '-qq'] + missing,
                        capture_output=True, timeout=180)
        still = [t for t in ('pngquant', 'optipng') if not _sh.which(t)]
        if not still:
            print(f"[tools] installed {' + '.join(missing)} — TMAX runs at full strength")
        else:
            print(f"[tools] could not install {' + '.join(still)} — PYQCompress will "
                  f"run on the PIL fallback (correct output, ~10-20% weaker PNG "
                  f"compression). NOT a failure; the run proceeds.")
    except Exception as e:
        print(f"[tools] provisioning skipped ({type(e).__name__}) — PYQCompress will "
              f"run on the PIL fallback. NOT a failure; the run proceeds.")


def _session_class(progress_path, files_meta, trigger=None):
    # v2026.08.22.2 (GAP-2026-08-22-STEP9-READ-SET): Step 9's S0-3 law differs from
    # Step 5's §S8-0b on the UNKNOWN case — a fresh mock has no frozen batch plan
    # yet, and reading too little there can let a reduced read reach the end-of-mock
    # writer, so unknown -> FINAL for MockExplain/TestExplain. Step 5's fresh-corpus
    # NON-FINAL rule is unchanged.
    if trigger in ('MockExplain', 'TestExplain') and (
            not progress_path or not os.path.exists(progress_path)):
        return 'FINAL'
    # v2026.08.22.5 (GAP-1B-STEP7-READ-SET): Step 7's S1-0 law is the S0-3 shape,
    # not the §S8-0b shape — a fresh mock has no frozen batch plan yet (S3-16 builds
    # batch_state.json), and reading too little there can let a reduced read reach
    # the Final-Assembly writers, so unknown -> FINAL. With a batch_state.json the
    # plan itself decides: the session is FINAL iff the batch it will deliver is the
    # plan's last (current entry is_final, or remaining batches <= 1). A malformed
    # or schema-alien file is a corrupt state, not a fresh one -> FINAL.
    # v2026.08.22.7 (STEP6-READ-SET): Step 6's S0-READSET law. The progress
    # artefact IS blueprint.json — no file means B1 (read everything, it consumes
    # every input section AND delivers the skeleton per §14/§15); mocks complete
    # means B3 (read everything, it writes every closing output); in between is a
    # B2 batch, which works entirely from blueprint.json state -> NON-FINAL.
    # Malformed or schema-alien -> FINAL (corrupt state, not a fresh one).
    # v2026.08.23 (GAP-2026-08-23-PYQSCAN-SPECBUDGET): one-shot triggers. PYQDraft
    # and PYQApprove have no batch loop — their only session closes the books, and
    # under the generic fresh-corpus rule below (no progress file -> NON-FINAL) that
    # session would skip Framework_PYQCore.md's newly FINAL-only §11/§12 on the very
    # run that must consult them. One-shot => FINAL, unconditionally. The batched
    # PYQ routes are already safe both ways: a fresh PYQScan/PYQCount session is
    # genuinely NON-FINAL, and any session holding a scan/count progress file falls
    # to the schema-alien branch of the generic parser -> FINAL, the safe default.
    if trigger in ('PYQDraft', 'PYQApprove'):
        return 'FINAL'
    if trigger == 'MockBlueprint':
        if not progress_path or not os.path.exists(progress_path):
            return 'FINAL'
        try:
            bp = json.load(open(progress_path, encoding='utf-8'))
            n_done = len(bp['mocks'])
            n_total = int(bp['total_mocks'])
            if n_total > 0 and n_done < n_total:
                return 'NON-FINAL'
            return 'FINAL'
        except Exception:
            return 'FINAL'
    if trigger in ('MockCreate', 'TestCreate'):
        if not progress_path or not os.path.exists(progress_path):
            return 'FINAL'
        try:
            bs = json.load(open(progress_path, encoding='utf-8'))
            plan = bs['batch_plan']
            done = set(bs.get('batches_completed') or [])
            cur = bs.get('current_batch')
            remaining = [b for b in plan if b.get('batch_id') not in done]
            cur_entry = next((b for b in plan if b.get('batch_id') == cur), None)
            if len(remaining) <= 1 or (cur_entry or {}).get('is_final'):
                return 'FINAL'
            return 'NON-FINAL'
        except Exception:
            return 'FINAL'
    """FINAL vs NON-FINAL — Framework_MockTestAnalyse §S8-0b, Framework_PYQCore EC-P42.

    THE AXIS IS NOT FRESH vs RESUME. A session executes the same code whether it is
    session 1 or session 5; what decides which sections it reaches is whether it will
    CLOSE THE BOOKS. Routing on fresh/resume would leave session 1 of every one of the
    ~200 exams exactly as broken as the reference incident.

    Unknown -> FINAL. The default must be the SAFE one: reading too much costs a
    session, reading too little can let a reduced read reach a writer.
    """
    if not progress_path or not os.path.exists(progress_path):
        # FRESH CORPUS. GAP-2026-08-16, deployment review: this returned "FINAL", and
        # the model correctly followed the printed class — so session 1 of the very
        # first live run did a FULL read (552,313 B) when §S8-0b calls for the
        # NON-FINAL set. Measured on IIT_JAM_MATHEMATICS: both batches logged
        # spec_read_mode "full". The read-set fix did not engage on the session it was
        # designed for. It caused no harm only because the direct lane (EC-P43) had
        # removed all context pressure; on a connector-lane deployment session 1 would
        # be back at the original stall.
        # §S8-0b L6782 is the authority and says: "When no progress file exists the
        # corpus has not been enumerated yet, so the count is unknown; decide the class
        # immediately after PHASE A/A1b, which is the first moment it is knowable, and
        # read the NON-FINAL set until then." bootstrap now prints that instead of
        # contradicting it. The safe default is preserved where it belongs — an
        # UNREADABLE or malformed progress file still returns FINAL, because that is a
        # corrupt state rather than a fresh one.
        return "NON-FINAL"
    try:
        prog = json.load(open(progress_path, encoding="utf-8"))
    except Exception:
        # Unreadable/malformed progress file: FINAL. Reading too much costs a session;
        # reading too little can let a reduced read reach a writer.
        return "FINAL"
    meta = prog.get("_meta") or {}
    done = len(meta.get("papers_processed") or [])
    transport = meta.get("_transport") or {}
    # Tolerate the pre-v2.51.0 key for one release (EC-P38: a pre-patch progress file
    # is VALID INPUT and is never discarded).
    planned = transport.get("papers_planned", transport.get("papers_admitted")) or []
    deferred = transport.get("deferred_context") or []
    total = meta.get("total_papers") or (done + len(planned) + len(deferred))
    remaining = max(0, total - done)
    return "NON-FINAL" if remaining > 3 else "FINAL"


# ── GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY ────────────────────────────────────────
# Production paths; each is overridable by environment so --self-test never touches them.
def _dir(var, default):
    return os.environ.get(var, default)

def project_dir():
    return _dir("FW_PROJECT_DIR", "/mnt/project")

def uploads_dir():
    return _dir("FW_UPLOADS_DIR", "/mnt/user-data/uploads")

def attach_dir():
    return _dir("FW_ATTACH_DIR", "/mnt/user-data/attachments")

def home_dir():
    return _dir("FW_HOME", "/home/claude")

def outputs_dir():
    return _dir("FW_OUTPUTS", "/mnt/user-data/outputs")


# ── 2026.11.12 (GAP-2026-11-12-HANDOVER-CHECKPOINT): the O3-3 CHECKPOINT as ONE deterministic command. A planned
# handover (GRADE_REQUEST, ROTATE) REFRESHES it to the current progress (`make`), so the next worker's RESTORE
# brings back exactly that progress — the batch in work survives; only a FAILED worker's unproven work is undone.
def _ckpt_work_files(exam, paper):
    import fnmatch
    h = home_dir()
    keep = (f"{exam}_M{paper}_chat_block.md", f"{exam}_M{paper}_worker_report.json")
    out = []
    if os.path.isdir(h):
        for n in sorted(os.listdir(h)):
            p = os.path.join(h, n)
            if os.path.isfile(p) and n not in keep and (n.startswith(f"{exam}_") or fnmatch.fnmatch(n, "q*_*.png")
                                                        or fnmatch.fnmatch(n, "q*_*.figspec.json")):
                out.append(n)
    return out


def _ckpt_output_files(exam):
    o = outputs_dir()
    return sorted(n for n in os.listdir(o) if os.path.isfile(os.path.join(o, n)) and n.startswith(f"{exam}_")) \
        if os.path.isdir(o) else []


def checkpoint_cmd(a):
    import shutil
    if not a.exam or not a.paper:
        return _refuse("--checkpoint needs --exam and --paper")
    ck = os.path.join(home_dir(), f"{a.exam}_M{a.paper}_checkpoint")
    if a.checkpoint == "make":
        if os.path.isdir(ck):
            shutil.rmtree(ck)
        os.makedirs(os.path.join(ck, "home"))
        os.makedirs(os.path.join(ck, "outputs"))
        w, o = _ckpt_work_files(a.exam, a.paper), _ckpt_output_files(a.exam)
        for n in w:
            shutil.copy2(os.path.join(home_dir(), n), os.path.join(ck, "home", n))
        for n in o:
            shutil.copy2(os.path.join(outputs_dir(), n), os.path.join(ck, "outputs", n))
        print(f"CHECKPOINT MADE: {len(w)} work file(s), {len(o)} output file(s) — {ck}")
        return 0
    if a.checkpoint == "restore":
        if not os.path.isdir(ck):
            print("CHECKPOINT: none — nothing to restore")
            return 0
        hw, ho = set(os.listdir(os.path.join(ck, "home"))), set(os.listdir(os.path.join(ck, "outputs")))
        for n in _ckpt_work_files(a.exam, a.paper):
            if n not in hw:
                os.remove(os.path.join(home_dir(), n))
        for n in _ckpt_output_files(a.exam):
            if n not in ho:
                os.remove(os.path.join(outputs_dir(), n))
        for n in hw:
            shutil.copy2(os.path.join(ck, "home", n), os.path.join(home_dir(), n))
        os.makedirs(outputs_dir(), exist_ok=True)
        for n in ho:
            shutil.copy2(os.path.join(ck, "outputs", n), os.path.join(outputs_dir(), n))
        shutil.rmtree(ck)
        print(f"CHECKPOINT RESTORED: {len(hw)} work file(s), {len(ho)} output file(s); checkpoint deleted")
        return 0
    if a.checkpoint == "drop":
        if os.path.isdir(ck):
            shutil.rmtree(ck)
        print("CHECKPOINT DROPPED")
        return 0
    print("CHECKPOINT: " + ("present" if os.path.isdir(ck) else "none"))
    return 0

READ_STATE_DIR = ".read_state"
STAGED_RECORD = ".staged.json"
# Fallback when SESSION_BUDGET.json is absent: the 2026-11-06 measurement (215,068 B of
# spec = 89,041 tok, 2.41 B/tok; 2.3 is the conservative divisor).
DEFAULT_BYTES_PER_TOKEN = 2.3
# Anchors: consonants only, so a code is never a word the model could "recall" by
# guessing; on chunk 1, every 8th chunk and the last, so a lost stretch of the read is
# caught wherever it falls.
ANCHOR_ALPHABET = "BCDFGHJKLMNPQRSTVWXZ"
ANCHOR_LEN = 7
ANCHOR_EVERY = 8
RETENTION_WHEN = ("after-read", "before-batch", "after-batch", "before-final", "handover")
# 2026.11.11 (GAP-2026-11-11-BATCH-VERIFICATION): GRADE_REQUEST — the worker hands the fresh blind grader /
# solver jobs of the batch it is writing to the orchestrator (a worker cannot start sub-agents), BEFORE the
# batch is delivered; ROTATE — the worker's room is short: its progress is on disk and a FRESH worker continues
# the same message (never a stop).
WORKER_STATES = ("BATCH_DELIVERED", "FINAL_BATCH_BUILT", "REVIEW_REQUEST", "GRADE_REQUEST", "ROTATE",
                 "PAPER_DELIVERED", "RETENTION_FAIL", "HARD_STOP")
WORKER_STATES_NEED_PARTS = ("REVIEW_REQUEST", "GRADE_REQUEST")
WORKER_STATES_NEED_BLOCK = ("BATCH_DELIVERED", "PAPER_DELIVERED", "HARD_STOP")
# The orchestrator prints the chat block with --worker-report show. Raised at integration
# (2026-11-06) from 400 / 30,000: the Final-Assembly response (S4-7 STEP D checklist + audit
# STDOUT + S13-9 handoff + footer) can exceed 400 lines. A tool result above ~40,000 chars is
# diverted by the harness to a file the session cannot read back whole (measured 2026-11-06),
# so `show` serves the block in PARTS of at most CHAT_BLOCK_PART_BYTES (whole lines):
# `--part P`, default 1. Every part is a normal inline result.
CHAT_BLOCK_MAX_LINES = 800
CHAT_BLOCK_MAX_BYTES = 60000
CHAT_BLOCK_PART_BYTES = 24000


def _block_parts(block):
    """Split a chat block into consecutive parts of whole lines, each <= CHAT_BLOCK_PART_BYTES
    (a single longer line is its own part). Joining the parts gives the block back exactly."""
    lines = block.splitlines(keepends=True)
    parts, cur, size = [], [], 0
    for ln in lines:
        b = len(ln.encode("utf-8"))
        if cur and size + b > CHAT_BLOCK_PART_BYTES:
            parts.append("".join(cur)); cur, size = [], 0
        cur.append(ln); size += b
    if cur or not parts:
        parts.append("".join(cur))
    return parts

# D-4: the FINAL line named Step 5's writer (section_rules.md) for EVERY trigger, so a
# Step 7 session was told it "may write section_rules.md" and nothing about Final Assembly.
FINAL_READ_MESSAGES = {
    "MockCreate": "This session may run Final Assembly and commit the registry.",
    "TestCreate": "This session may run Final Assembly and commit the registry.",
    "MockBlueprint": "This session may write the closing outputs.",
    "MockExplain": "This session may write the end-of-mock report.",
    "TestExplain": "This session may write the end-of-mock report.",
    "PYQExtract": "This session may write section_rules.md.",
}
FINAL_READ_DEFAULT = "This session may write final artefacts."

D2_TEXT = """PROJECT FILES ARE NOT MOUNTED ON THIS SURFACE. Stage them into {proj} now:
1. List the project's documents with the Projects tool (project_info).
2. Call project_read once for each document the step needs. Copy nothing by hand and do not
   re-type anything. (A .docx or .pdf held in the project is returned as extracted text only
   and cannot be staged: when the step needs that file itself, ask the user to attach it.)
3. Run  python3 bootstrap.py --stage-project-docs
   It takes every document you just read from this chat's own tool-result record and writes
   it byte for byte into {proj} (a document the tool saved as `local_file` is copied).
4. Only for a document step 3 lists under NOT STAGED:
   - the result gave `local_file`:  python3 bootstrap.py --stage-doc "<name>" --from "<local_file>"
   - the result was inline text: write that text, character for character, to
     {proj}/<name> with your file-writing tool, then
       python3 bootstrap.py --stage-doc "<name>" --typed
5. A document the user ATTACHED to this chat is already staged (listed above as STAGED
   ATTACHMENT) and wins over the project copy: do nothing for it.
6. Run  python3 bootstrap.py --stage-status  and continue only when it prints STAGING COMPLETE.
Sub-agents cannot read the project: staging is done in THIS chat, once per chat."""

# The worker prompt. Its commands, states and messages are Framework_MockTestOrchestrate.md's
# (O2-2, O3-1 to O3-8) word for word; keep the two in step. Under 60 lines.
WORKER_PROMPT = """You are a Step 7 WORKER (owner decision OD-2026-11-06): the Step 7 session of
Framework_MockTestCreate.md (MTC). You are governed by MTC AND by Framework_MockTestOrchestrate.md
PART B (O3-1 to O3-8); both are in your read. The user's trigger, verbatim:
  {trigger_text}
<T> = the trigger's step word (MockCreate or TestCreate); <E> = the exam code; <N> = the paper
number. BATCH STATE = {home}/<E>_M<N>_batch_state.json.
CHAT BLOCK FILE = {home}/<E>_M<N>_chat_block.md.

GROUND RULES (O3-1). Step 0 is ALREADY DONE: the verified, resolved framework is in
/tmp/fw_effective; work there (cd /tmp/fw_effective). Do NOT clone, do NOT re-run Step 0, do NOT
delete /tmp/fw or /tmp/fw_effective. Inputs are staged: project files in {proj}, chat
attachments in {up}. Never start a sub-agent, never call a file-delivery tool, never wait for
the user: your only reader is the orchestrator.

ORCHESTRATOR MESSAGE (O2-2). A worker that replaces another one receives, after a blank line at
the end of this prompt, the ORCHESTRATOR MESSAGE the replaced worker was handling; later messages
arrive as new messages to you. The first worker of a run receives no message: its prompt carries
the trigger. The messages (closed set, sent exactly as written):
  continue — delivery confirmed
  FINAL ASSEMBLY
  REVIEW RETURNED   (followed by one line per part: <part_dir> <the reviewer's line>)
  GRADE RETURNED    (followed by one line per job folder: <job_dir> <the reviewer's line>)
  USER MESSAGE: <the user's message, verbatim>
In every worker `continue — delivery confirmed` IS the user's continue trigger (MTC S4-6, S4-5
CHECK 4) and `USER MESSAGE: <m>` is the user's message <m> for S4-6 (O3-1).

READ (O3-2). For K = 1..N, one call each, in order:
  python3 bootstrap.py --trigger <T> --progress <BATCH STATE> --read K
(omit --progress while the BATCH STATE does not exist). Never read a spec any other way, never
with a sed range above 300 lines, never open a tool-output file the harness diverted.
PYTHON (MTC S1-0R): session start `python3 bootstrap.py --session-start --exam <E> --paper <N> <trigger options>`;
any other block: save it as /home/claude/fwrun/<x>.py, run `python3 bootstrap.py --run-block <file> --exam <E> --paper <N>`.
RETENTION (O3-3). Prove the read from memory (never open .read_state):
  python3 bootstrap.py --retention "<nn>=<code> ..." --when <W>
W = after-read (a), before-batch (b), after-batch (c), before-final (d; add --escalate for the
escalation read of O3-5), handover (before a GRADE_REQUEST or ROTATE report). CHECKPOINT (O3-3), always with the command
  python3 bootstrap.py --checkpoint make|restore|drop --exam <E> --paper <N>
`make` right after (b) passes; `drop` when the batch is recorded (S4-7 STEP E) or the correction has passed (c).
A PLANNED HANDOVER — GRADE_REQUEST or ROTATE — first proves retention (--when handover), then runs `make`
again (the checkpoint now holds the progress so far: the next worker's restore keeps the batch in work), then
reports. A FAIL at any point: report RETENTION_FAIL and stop (the next worker restores the CHECKPOINT: the work
since the last make, made without the spec in context, is undone).
{body}
END EVERY TURN (O3-4): write MTC's chat prints of this turn to the CHAT BLOCK FILE, then run
  python3 bootstrap.py --worker-report write --exam <E> --paper <N> --state <STATE> --batch <K> --of <M> --files "<paths>" --chat-file {home}/<E>_M<N>_chat_block.md
adding --review-parts "<dir1>,<dir2>" for REVIEW_REQUEST and GRADE_REQUEST (the job folders); --files ""
when the turn has no present_files call. STATE is one of BATCH_DELIVERED, FINAL_BATCH_BUILT,
REVIEW_REQUEST, GRADE_REQUEST, ROTATE, PAPER_DELIVERED, RETENTION_FAIL, HARD_STOP. When your remaining
room is short, save state and report ROTATE — never a HARD STOP for room. Your final message is the one line:
  WORKER DONE <STATE> batch K of M"""

WORKER_FIRST = """THIS TURN (first worker of the run): read (O3-2), prove (a), then execute MTC for ONE
response (O3-5): the session start, or one batch; a turn is cut only at FINAL_BATCH_BUILT,
REVIEW_REQUEST, GRADE_REQUEST and ROTATE. Prove (b) before authoring and (c) before S4-7 STEP E records the batch."""

WORKER_CONTINUE = """THIS TURN (--continue: the paper is in progress on disk): read (O3-2) and prove (a) first.
If {home}/<E>_M<N>_batch_state.json does not exist, write nothing and report HARD_STOP with the
WORKDIR-LOST chat block of O3-1. Otherwise O3-7: RESTORE first with `--checkpoint restore` (O3-3; a no-op when there is none; after a
planned handover it restores exactly the saved progress);
then, in every case, MTC's session start and S4-12, handling the ORCHESTRATOR MESSAGE at the end of
this prompt exactly as O3-7 says: for `continue — delivery confirmed` and `USER MESSAGE: ...`
S4-12's batch recovery ends after step 4c (no resume summary, no STOP) and MTC S4-6 is applied to
the message; `FINAL ASSEMBLY` enters S13 by S4-12's FINAL ASSEMBLY INTERRUPTED BEFORE THE REVIEW
rule; `REVIEW RETURNED` is O3-6 step 2 inside S4-12's REVIEW_RUNNING branch; `GRADE RETURNED` is S4-12's
BATCH IN VERIFICATION branch (append its lines to returned.txt, run S4-7 STEP A2 again; O3-9). Prove (b) and
(c) as in O3-3; a worker continuing a batch in verification runs `--checkpoint make` right after (a)."""


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _session_budget():
    return _load_json("SESSION_BUDGET.json") or {}


def _sha12(path):
    return sha256(path)[:12]


def _spec_sections():
    import spec_sections
    return spec_sections


def _routed_specs(trigger):
    M = _load_json("MANIFEST.json") or {}
    return [f for f in (M.get("routes") or {}).get(trigger) or [] if f.endswith(".md")]


def _plans(sec, specs, klass):
    """{spec: [(start, end), ...]} read chunks for `klass`, or None for a spec the map
    does not describe (absent, or its sha differs: a stale map is never chunked)."""
    ss, out = _spec_sections(), {}
    for f in specs:
        try:
            out[f] = ss.chunk_plan(sec, f, klass)
        except (KeyError, ValueError, OSError):
            out[f] = None
    return out


def _attachments():
    """Regular, non-dot files under FW_ATTACH_DIR, recursively — ONE path per attachment
    name: when the user attached the same name more than once, the newest copy wins (an
    older copy is never staged over it and never re-raises the SURFACE notice)."""
    newest = {}
    for root, dirs, files in os.walk(attach_dir()):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(files):
            if f.startswith("."):
                continue
            p = os.path.join(root, f)
            if not os.path.isfile(p):
                continue
            name = _attachment_name(p)
            if name not in newest or os.path.getmtime(p) >= os.path.getmtime(newest[name]):
                newest[name] = p
    return sorted(newest.values())


def _attachment_name(path):
    # Measured 2026-11-06: chat attachments land as <session>/<8 hex>-<name>.
    return re.sub(r"^[0-9a-f]{8}-", "", os.path.basename(path))


def _unstaged_attachments():
    up = uploads_dir()
    return [p for p in _attachments()
            if not os.path.isfile(os.path.join(up, _attachment_name(p)))
            or sha256(os.path.join(up, _attachment_name(p))) != sha256(p)]


def surface_notice(trigger=None):
    """D1. Printed after a successful verify; never a stop."""
    if not os.path.isdir(project_dir()) or _unstaged_attachments():
        print("SURFACE: project files are not mounted on this surface (no /mnt/project) and/or "
              "attachments are\nstored under /mnt/user-data/attachments. RUN NOW, before "
              "reading any spec:\n  python3 bootstrap.py --stage-inputs --trigger "
              + (trigger or "<Step>   (the step the user asked for, e.g. TestCreate)"))


def _staged_record(proj):
    """The staging record of `proj`: a dict ({} when there is none yet), or None when the
    file exists but does not parse — a corrupt record must never be read as "nothing was
    attached" (the attachment-wins rule depends on it)."""
    path = os.path.join(proj, STAGED_RECORD)
    if not os.path.exists(path):
        return {}
    rec = _load_json(path)
    return rec if isinstance(rec, dict) else None


def _held(proj):
    """The staged files of `proj`: regular entries whose name does not start with a dot."""
    return sorted(f for f in (os.listdir(proj) if os.path.isdir(proj) else [])
                  if not f.startswith("."))


def _plain_name(name):
    """True for a bare file name — never a path, never '.', '..' or empty."""
    return bool(name) and name not in (".", "..") and os.path.basename(name) == name \
        and "/" not in name and "\\" not in name


def _copy_replacing(src, dst):
    """Byte copy; a read-only target is unlinked first (re-staging must never wedge)."""
    if os.path.exists(dst) and not os.access(dst, os.W_OK):
        os.unlink(dst)
    shutil.copyfile(src, dst)


def stage_inputs(trigger=None):
    proj, up = project_dir(), uploads_dir()
    os.makedirs(proj, exist_ok=True)
    os.makedirs(up, exist_ok=True)
    if _staged_record(proj) is None:
        # Corrupt record: drop it. Every attachment is recorded again just below.
        os.unlink(os.path.join(proj, STAGED_RECORD))
        print("NOTICE: the staging record was unreadable and has been rebuilt.")
    bad = []
    for src in _attachments():
        name = _attachment_name(src)
        dst = os.path.join(up, name)
        try:
            if not os.path.isfile(dst) or sha256(dst) != sha256(src):
                _copy_replacing(src, dst)
            print(f"STAGED ATTACHMENT {name} {os.path.getsize(dst)} B sha256 {_sha12(dst)}")
            # An attached file WINS over the project copy (the registry lane rule, applied to
            # every input): it is also placed in the project dir, byte for byte, so no step
            # needs the Projects tool for a file the user attached.
            if stage_doc(name, dst, False, mode="attachment", quiet=True) != 0:
                bad.append(name)
        except OSError as e:
            print(f"NOTICE: could not stage attachment {name} ({type(e).__name__}: {e}); "
                  f"continuing.")
    if bad:
        print(f"STAGING STOPPED: the attached file(s) {', '.join(bad)} failed the check printed "
              f"above. Ask the user to attach a correct copy; do not continue.")
        return 2
    held = _held(proj)
    rec = _staged_record(proj) or {}
    if all(rec.get(f, {}).get("mode") == "attachment" for f in held):
        print(D2_TEXT.format(proj=proj, up=up))
        pats = (_session_budget().get("project_inputs") or {}).get(trigger or "")
        if pats:
            print(f"THIS STEP ({trigger}) reads only these project documents — call "
                  f"project_read only for names matching:\n  " + "  ".join(pats)
                  + "\n  and skip any of them already listed above as STAGED ATTACHMENT.")
        else:
            print("Skip any document already listed above as STAGED ATTACHMENT. (Run "
                  "--stage-inputs with --trigger <Step> to see which documents the step reads.)")
    if any(f.startswith("Framework_") and f.endswith(".md") for f in held):
        print(f"NEXT: python3 spec_source.py --resolve --repo-dir /tmp/fw --project-dir {proj} "
              f"--overlay-dir /tmp/fw_effective && cd /tmp/fw_effective")
    else:
        print("NEXT: continue with rule 2a (bootstrap.py --trigger <Step>)")
    return 0


def _stage_invalid(name, reason):
    print(f"HARD STOP [HS:INPUT] STAGE-INVALID {name}: {reason} — re-read the document and "
          f"write it again.")
    return 2


def transcript_glob():
    return os.environ.get("FW_TRANSCRIPT_GLOB") or os.path.join(
        os.path.expanduser("~"), ".claude", "projects", "*", "*.jsonl")


def _project_read_results(obj):
    """Yield every Projects-tool `project_read` result found anywhere inside one transcript
    record: a JSON string {"method":"project_read","path":...,"content"|"local_file":...}."""
    if isinstance(obj, str):
        s = obj.lstrip()
        if s.startswith("{") and '"project_read"' in s[:80]:
            try:
                d = json.loads(s)
            except ValueError:
                return
            if isinstance(d, dict) and d.get("method") == "project_read" and d.get("path"):
                yield d
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _project_read_results(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _project_read_results(v)


def stage_project_docs():
    """GAP-2026-11-06 (measured): on a surface with no /mnt/project the Projects tool returns a
    document either as `local_file` (large) or INLINE in the tool result (seen up to 111,528
    chars). Re-typing an inline document is slow and can alter it. The session's own
    tool-result record on disk holds each result exactly, so the documents are staged from
    it byte for byte. The newest result per document wins. No record -> NOT STAGED (the
    session falls back to --stage-doc)."""
    import glob as _glob
    found = {}
    files = sorted(_glob.glob(transcript_glob()), key=os.path.getmtime)
    for f in files:
        try:
            fh = open(f, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                if "project_read" not in line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                for d in _project_read_results(rec):
                    found[d["path"]] = d
    if not found:
        print(f"NOT STAGED: no project_read result was found in this chat's tool-result "
              f"record ({transcript_glob()}). Use --stage-doc for each document (see "
              f"--stage-inputs).")
        return 2
    proj = project_dir()
    os.makedirs(proj, exist_ok=True)
    bad = []
    staged_rec = _staged_record(proj)
    if staged_rec is None:
        print("HARD STOP [HS:INPUT] STAGE-RECORD — the staging record is unreadable. Run "
              "python3 bootstrap.py --stage-inputs (it rebuilds the record), then this "
              "command again.")
        return 2
    for name in sorted(found):
        d = found[name]
        base = os.path.basename(name)
        if not _plain_name(base):
            print(f"NOT STAGED {name!r}: not a file name.")
            bad.append(repr(name))
            continue
        if staged_rec.get(base, {}).get("mode") == "attachment":
            print(f"KEPT ATTACHMENT {base} (the file attached to this chat wins over the "
                  f"project copy)")
            continue
        is_blob = d.get("file_kind") == "blob" and d.get("local_file")
        if not is_blob and base.lower().endswith((".docx", ".pdf", ".xlsx", ".pptx")):
            print(f"SKIPPED {base} (only its extracted text is available; when the step needs "
                  f"the file itself, ask the user to attach it)")
            continue
        if isinstance(d.get("content"), str) and not is_blob:
            tmp = os.path.join(proj, f".incoming_{secrets.token_hex(4)}")
            try:
                with open(tmp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(d["content"])
                rc = stage_doc(base, tmp, False, mode="project-record")
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
        elif d.get("local_file") and os.path.isfile(d["local_file"]):
            rc = stage_doc(base, d["local_file"], False, mode="file")
        else:
            print(f"NOT STAGED {base}: its local_file is gone — call project_read for it again.")
            rc = 2
        if rc != 0:
            bad.append(base)
    if bad:
        print(f"NOT STAGED: {', '.join(bad)}")
        return 2
    return 0


def stage_doc(name, src, typed, mode=None, quiet=False):
    proj = project_dir()
    if not _plain_name(name):
        return _stage_invalid(name, "the name must be a plain file name, not a path")
    dst = os.path.join(proj, name)
    if os.path.isdir(dst):
        return _stage_invalid(name, f"{dst} is a directory")
    forced = mode
    if typed:
        mode = "typed"
        if not os.path.isfile(dst):
            return _stage_invalid(name, f"not found in {proj} — write it there first")
    else:
        if not src or not os.path.isfile(src):
            return _stage_invalid(name, f"source {src!r} not found")
        up = os.path.realpath(uploads_dir())
        mode = forced or ("attachment" if os.path.realpath(src).startswith(up + os.sep)
                          else "file")
    check = dst if typed else src
    data = open(check, "rb").read()
    if not data.strip():
        return _stage_invalid(name, "file is empty")
    if name.endswith(".json"):
        try:
            json.loads(data.decode("utf-8"))
        except ValueError as e:
            return _stage_invalid(name, f"not valid JSON ({e})")
    if name.endswith(".py"):
        try:
            compile(data, name, "exec")
        except (SyntaxError, ValueError) as e:
            return _stage_invalid(name, f"does not compile ({e})")
    os.makedirs(proj, exist_ok=True)
    if not typed:
        _copy_replacing(src, dst)
    rec_path = os.path.join(proj, STAGED_RECORD)
    rec = _staged_record(proj) or {}
    rec[name] = {"name": name, "mode": mode, "bytes": os.path.getsize(dst),
                 "sha256": sha256(dst)}
    with open(rec_path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
    if not quiet:
        print(f"STAGED {mode} {name} {os.path.getsize(dst)} B sha256 {_sha12(dst)}")
    return 0


def stage_status():
    proj = project_dir()
    held = _held(proj)
    if not held:
        print(f"HARD STOP [HS:INPUT] STAGING-EMPTY — {proj} holds no file. Run "
              f"python3 bootstrap.py --stage-inputs and follow it.")
        return 2
    rec = _staged_record(proj) or {}
    for f in held:
        print(f"  {f}  ({rec.get(f, {}).get('mode', 'present')})")
    typed = sum(1 for f in held if rec.get(f, {}).get("mode") == "typed")
    print(f"STAGING COMPLETE — {len(held)} file(s) in {proj} ({typed} typed from inline "
          f"project text)")
    return 0


# ── READ / RETENTION ──────────────────────────────────────────────────────────────
def _state_path(read_id):
    return os.path.join(READ_STATE_DIR, f"{read_id}.json")


def _pointer(role, escalate):
    return os.path.join(READ_STATE_DIR, f"current_{role}" + ("_escalate" if escalate else ""))


def _load_read(role, escalate, read_id):
    rid = read_id
    if not rid and os.path.exists(_pointer(role, escalate)):
        rid = open(_pointer(role, escalate), encoding="utf-8").read().strip()
    return _load_json(_state_path(rid)) if rid else None


def _save_read(st):
    with open(_state_path(st["read_id"]), "w", encoding="utf-8") as fh:
        json.dump(st, fh, indent=2)


def _anchor_ks(n):
    return sorted({1, n} | {k for k in range(ANCHOR_EVERY, n, ANCHOR_EVERY)})


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _reread_cmd(st):
    cmd = f"python3 bootstrap.py --trigger {st['trigger']}"
    if st.get("progress"):
        cmd += f" --progress {st['progress']}"
    if st["role"] != "session":
        cmd += f" --role {st['role']}"
    return cmd + " --read 1" + (" --escalate" if st.get("escalate") else "")


def _new_read(args, role):
    """K=1: decide the class exactly as the budget block does, plan the chunks, mint the
    anchors and persist the read. Returns (state, None) or (None, exit_code)."""
    budget = _session_budget()
    sec = _load_json("SPEC_SECTIONS.json") or {}
    ss = _spec_sections()
    if role == "orchestrator":
        orch = ((budget.get("orchestrated") or {}).get(args.trigger) or {}).get("orchestrator_spec")
        if not orch:
            print(f"READ: trigger '{args.trigger}' is not orchestrated (SESSION_BUDGET.json); "
                  f"use the session read.")
            return None, 2
        specs, klass = [orch], "FINAL"
    else:
        specs = _routed_specs(args.trigger)
        klass = _session_class(args.progress, {}, trigger=args.trigger)
    if args.escalate:
        # One-way escalation: the class that matters is the one the session READ with,
        # not today's — by Final Assembly the plan says FINAL and would hide the omission.
        prior = _load_read("session", False, None)
        if not prior or prior.get("trigger") != args.trigger:
            print(f"ESCALATION: there is no session read for '{args.trigger}' to escalate — "
                  f"run the session read first (--read 1 without --escalate).")
            return None, 2
        klass = prior["class"]
        sfiles = sec.get("files") or {}

        def _merged(rs):
            out = []
            for a, b in sorted(tuple(r) for r in rs):
                if out and a <= out[-1][1] + 1:
                    out[-1][1] = max(out[-1][1], b)
                else:
                    out.append([a, b])
            return [tuple(r) for r in out]
        plans = {}
        for f in specs:
            info = sfiles.get(f)
            if not info or not os.path.exists(f) or sha256(f) != info.get("sha256"):
                plans[f] = None
                continue
            rs = (_merged(info.get("final_only_ranges") or [])
                  if klass == "NON-FINAL" and info.get("has_read_set") else [])
            plans[f] = ss.chunk_ranges(f, rs)
    else:
        plans = _plans(sec, specs, klass)
    stale = [f for f in specs if plans[f] is None]
    if stale:
        fail(f"SPEC_SECTIONS.json does not describe {stale} as they are on disk. Re-run "
             f"python3 bootstrap.py (and spec_source.py --resolve in an overlay).")
    chunks = [{"file": f, "start": a, "end": b,
               "sha256": hashlib.sha256(ss.chunk_text(f, a, b).encode("utf-8")).hexdigest()}
              for f in specs for a, b in plans[f]]
    if not chunks:
        if args.escalate:
            print("ESCALATION: nothing to read — this session read everything.")
            return None, 0
        print(f"READ: trigger '{args.trigger}' routes no spec.")
        return None, 2
    for k, c in enumerate(chunks, 1):
        c["k"] = k
    n = len(chunks)
    anchors = {f"{i:02d}": "".join(secrets.choice(ANCHOR_ALPHABET) for _ in range(ANCHOR_LEN))
               for i, _ in enumerate(_anchor_ks(n), 1)}
    st = {"read_id": args.read_id or secrets.token_hex(4), "trigger": args.trigger,
          "role": role, "class": klass, "escalate": bool(args.escalate),
          "progress": args.progress, "files": {f: sha256(f) for f in specs},
          "chunks": chunks, "anchor_chunks": _anchor_ks(n), "anchors": anchors,
          "served": [], "started": _now(), "finished": None, "checks": []}
    os.makedirs(READ_STATE_DIR, exist_ok=True)
    _save_read(st)
    with open(_pointer(role, args.escalate), "w", encoding="utf-8") as fh:
        fh.write(st["read_id"])
    return st, None


def cmd_read(args):
    if not args.trigger:
        print("READ: --read needs --trigger.")
        return 2
    if not os.path.exists(".verified"):
        fail("no .verified in this directory — run  python3 bootstrap.py --trigger "
             f"{args.trigger}  first; reads are served from the verified corpus only.")
    role = args.role
    if args.read == 1:
        st, rc = _new_read(args, role)
        if st is None:
            return rc
    else:
        st = _load_read(role, args.escalate, args.read_id)
        if st is None or st["trigger"] != args.trigger:
            print(f"READ: no current {role} read for '{args.trigger}' — start with --read 1.")
            return 2
    n, k = len(st["chunks"]), args.read
    if not 1 <= k <= n:
        print(f"READ: unknown chunk {k} — this read has chunks 1..{n}.")
        return 2
    expected = (st["served"][-1] + 1) if st["served"] else 1
    if k != expected and k not in st["served"]:
        print(f"WARNING READ ORDER: expected chunk {expected}")
    c = st["chunks"][k - 1]
    body = _spec_sections().chunk_text(c["file"], c["start"], c["end"])
    if hashlib.sha256(body.encode("utf-8")).hexdigest() != c["sha256"]:
        fail(f"{c['file']} lines {c['start']}-{c['end']} changed since this read began. "
             f"Re-read from chunk 1: {_reread_cmd(st)}")
    sys.stdout.write(f"=== READ {st['read_id']} · chunk {k} of {n} · {c['file']} lines "
                     f"{c['start']}-{c['end']} ===\n")
    sys.stdout.write(body if body.endswith("\n") else body + "\n")
    print(f"=== END chunk {k} of {n} ===")
    if k in st["anchor_chunks"]:
        nn = f"{st['anchor_chunks'].index(k) + 1:02d}"
        print(f"<<READ-ANCHOR {nn} {st['anchors'][nn]} — remember this code; you will be "
              f"asked for it>>")
    if k not in st["served"]:
        st["served"].append(k)
    if k == n:
        st["finished"] = _now()
        tot = sum(len(_spec_sections().chunk_text(x["file"], x["start"], x["end"])
                      .encode("utf-8")) for x in st["chunks"])
        role_flag = "" if role == "session" else f" --role {role}"
        esc_flag = " --escalate" if st["escalate"] else ""
        print(f"READ COMPLETE {st['read_id']}: {n} chunks, {tot} B. Now run:\n"
              f"  python3 bootstrap.py --retention \"<nn>=<code> ...\"{role_flag}{esc_flag}   "
              f"(all {len(st['anchors'])} anchors, from memory)")
    _save_read(st)
    return 0


def cmd_retention(args):
    st = _load_read(args.role, args.escalate, args.read_id)
    if st is None:
        print(f"RETENTION: no current {args.role} read — start one with --read 1.")
        return 2
    pairs = re.findall(r"(?<![0-9A-Z])(\d{2})=([A-Z]+)", args.retention.upper())
    given = {}
    for nn, code in pairs:
        # The same anchor given twice with different codes is a guess, not a recall.
        given[nn] = code if given.get(nn, code) == code else None
    wrong = sum(1 for nn, code in st["anchors"].items() if given.get(nn) != code)
    unread = len([c for c in st["chunks"] if c["k"] not in st["served"]])
    ok = wrong == 0 and unread == 0
    st["checks"].append({"when": args.when, "ts": _now(), "result": "PASS" if ok else "FAIL"})
    _save_read(st)
    m, n = len(st["anchors"]), len(st["chunks"])
    if ok:
        print(f"RETENTION: PASS {st['read_id']} ({m}/{m} anchors, {n}/{n} chunks) [{args.when}]")
        return 0
    never = f", {unread} chunk(s) never read" if unread else ""
    print(f"RETENTION: FAIL {st['read_id']} — {wrong} anchor(s) wrong or missing{never}. The "
          f"spec text is no longer (or was never fully) in this context. Re-read: "
          f"{_reread_cmd(st)} ... then continue from disk state (S4-12).")
    return 3


def cmd_read_receipts(args):
    st = _load_read(args.role, args.escalate, args.read_id)
    if st is None:
        print(f"READ RECEIPT: no current {args.role} read.")
        return 2
    res = [c["result"] for c in st["checks"]]
    ret = ("none" if not res else "FAIL" if res[-1] == "FAIL"
           else f"PASS {res.count('PASS')}×")
    for f in st["files"]:
        mine = [c for c in st["chunks"] if c["file"] == f]
        if not mine:
            continue
        spans = []
        for c in mine:
            if spans and c["start"] == spans[-1][1] + 1:
                spans[-1][1] = c["end"]
            else:
                spans.append([c["start"], c["end"]])
        print(f"READ RECEIPT {f} lines {','.join(f'{a}-{b}' for a, b in spans)} chunks "
              f"{mine[0]['k']}-{mine[-1]['k']} sha256 {st['files'][f][:12]} read_id "
              f"{st['read_id']} retention {ret}")
    return 0


# ── WORKER HAND-OFF (OD-2026-11-06) ───────────────────────────────────────────────
def _report_path(exam, paper):
    return os.path.join(home_dir(), f"{exam}_M{paper}_worker_report.json")


def _refuse(msg):
    print(f"WORKER REPORT REFUSED: {msg}")
    return 2


def _split_paths(text):
    """Comma-separated file paths. A file NAME may itself hold a comma (a paper slug built
    from a section name such as "Reasoning, General Intelligence"): pieces are joined back
    with their comma for as long as the joined text is not yet an existing file, so such a
    path is never cut in two. Paths that do not exist come back as their plain pieces."""
    pieces = [p for p in text.split(",")]
    out, i = [], 0
    while i < len(pieces):
        joined, j = pieces[i], i
        while not os.path.isfile(joined.strip()) and j + 1 < len(pieces):
            j += 1
            joined += "," + pieces[j]
        if os.path.isfile(joined.strip()):
            out.append(joined.strip()); i = j + 1
        else:
            if pieces[i].strip():
                out.append(pieces[i].strip())
            i += 1
    return out


def worker_report_write(a):
    if a.state not in WORKER_STATES:
        return _refuse(f"state {a.state!r} is not one of {', '.join(WORKER_STATES)}")
    absent = [n for n in ("exam", "paper", "batch", "of") if getattr(a, n) in (None, "")]
    if absent:
        return _refuse("missing " + ", ".join("--" + n for n in absent))
    paths = [os.path.abspath(p) for p in _split_paths(a.files or "")]
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        return _refuse(f"listed file(s) do not exist: {missing}")
    if a.chat_file and not os.path.isfile(a.chat_file):
        return _refuse(f"chat file {a.chat_file!r} does not exist")
    block = open(a.chat_file, encoding="utf-8", newline="").read() if a.chat_file else ""
    parts_given = [d.strip() for d in (a.review_parts or "").split(",") if d.strip()]
    if a.state in WORKER_STATES_NEED_PARTS and not parts_given:
        return _refuse(f"state {a.state} needs --review-parts")
    no_dir = [d for d in parts_given if not os.path.isdir(d)]
    if no_dir:
        return _refuse(f"review part folder(s) do not exist: {no_dir}")
    if len(block.splitlines()) > CHAT_BLOCK_MAX_LINES or len(block.encode("utf-8")) > CHAT_BLOCK_MAX_BYTES:
        return _refuse(f"chat block exceeds {CHAT_BLOCK_MAX_LINES} lines or "
                       f"{CHAT_BLOCK_MAX_BYTES:,} B")
    if not block.strip() and a.state in WORKER_STATES_NEED_BLOCK:
        return _refuse(f"chat block is empty; state {a.state} must carry one")
    rep = {"exam": a.exam, "paper": a.paper, "state": a.state, "batch": a.batch, "of": a.of,
           "files": [{"path": p, "exists": True, "bytes": os.path.getsize(p),
                      "sha256": sha256(p)} for p in paths],
           "chat_block": block,
           "review_parts": parts_given,
           "tokens_note": a.tokens_note, "written": _now()}
    if a.state == "ROTATE":
        # 2026.11.11: the orchestrator never opens the BATCH STATE — bootstrap records its sha so two ROTATE
        # reports with no progress between them are visible (O2-3: handled as RETENTION_FAIL, never a loop)
        _bsp = os.path.join(home_dir(), f"{a.exam}_M{a.paper}_batch_state.json")
        rep["progress_sha"] = sha256(_bsp) if os.path.isfile(_bsp) else "none"
    os.makedirs(home_dir(), exist_ok=True)
    with open(_report_path(a.exam, a.paper), "w", encoding="utf-8", newline="") as fh:
        json.dump(rep, fh, indent=2, ensure_ascii=False)
    print(f"WORKER REPORT written: {_report_path(a.exam, a.paper)} — {a.state} batch "
          f"{a.batch} of {a.of}")
    return 0


def worker_report_show(a):
    path = _report_path(a.exam, a.paper)
    if a.exam in (None, "") or a.paper in (None, ""):
        print("HARD STOP [HS:INFRA] WORKER-REPORT-MISSING — --exam and --paper are required.")
        return 2
    rep = _load_json(path)
    newest = max((os.path.getmtime(f["path"]) for f in (rep or {}).get("files", [])
                  if os.path.exists(f["path"])), default=0)
    if rep is None or os.path.getmtime(path) < newest:
        print(f"HARD STOP [HS:INFRA] WORKER-REPORT-MISSING — {path} is absent or older than "
              f"a file it lists. The worker did not finish its turn; do not deliver.")
        return 2
    changed = [f["path"] for f in rep["files"]
               if not os.path.isfile(f["path"]) or sha256(f["path"]) != f["sha256"]]
    if changed:
        print(f"HARD STOP [HS:INFRA] WORKER-REPORT-STALE — file(s) the report lists are "
              f"missing or no longer the ones it recorded: {changed}. Do not deliver.")
        return 2
    print(f"WORKER REPORT {rep['exam']} M{rep['paper']} — STATE {rep['state']} — batch "
          f"{rep['batch']} of {rep['of']}")
    print("FILES TO DELIVER (in this order):")
    for f in rep["files"]:
        print(f"  {f['path']}  ({f['bytes']} B)")
    if rep["state"] == "REVIEW_REQUEST":
        print(f"REVIEW PARTS: {', '.join(rep['review_parts'])}")
    if rep["state"] == "GRADE_REQUEST":
        print(f"GRADE JOBS: {', '.join(rep['review_parts'])}")
    if rep["state"] == "ROTATE":
        print(f"PROGRESS: {rep.get('progress_sha', 'none')}")
    block = rep["chat_block"]
    if not block.endswith("\n"):
        block += "\n"
    parts = _block_parts(block)
    want = getattr(a, "part", None) or 1
    if want < 1 or want > len(parts):
        print(f"HARD STOP [HS:INFRA] WORKER-REPORT-PART — part {want} does not exist "
              f"(this chat block has {len(parts)} part(s)).")
        return 2
    print(f"----- CHAT BLOCK part {want} of {len(parts)} (print verbatim, nothing added, "
          f"nothing removed) -----")
    sys.stdout.write(parts[want - 1])
    print(f"----- END CHAT BLOCK part {want} of {len(parts)} -----")
    if want < len(parts):
        print(f"MORE: run the same command with --part {want + 1} and print that part "
              f"directly after this one, as one continuous block.")
    return 0


def worker_prompt(trigger_text, cont):
    print(WORKER_PROMPT.format(trigger_text=trigger_text, proj=project_dir(), up=uploads_dir(),
                               home=home_dir(),
                               body=(WORKER_CONTINUE.format(home=home_dir()) if cont
                                     else WORKER_FIRST)))
    return 0


PROGRESS_HELP = ("the step's progress file — decides SESSION CLASS and the read plan. "
                 "PYQExtract: [ExamCode]_analysis_progress.json; MockBlueprint: "
                 "[ExamCode]_blueprint.json; MockCreate/TestCreate: "
                 "/home/claude/[ExamCode]_M[N]_batch_state.json; MockExplain/TestExplain: "
                 "that step's state file")


def orchestrated_notice(trigger):
    """D5: the orchestrated notice for a trigger listed in SESSION_BUDGET.orchestrated, else
    None. Printed FIRST in the --trigger block and again as the LAST lines of the output
    (an older installed SKILL reads the end of the block)."""
    orch = ((_session_budget().get("orchestrated") or {}).get(trigger) or {}).get(
        "orchestrator_spec")
    if not orch:
        return None
    sec = _load_json("SPEC_SECTIONS.json") or {}
    n_orch = len((_plans(sec, [orch], "FINAL")[orch]) or [])
    return (f"STEP 7 RUNS ORCHESTRATED (owner decision OD-2026-11-06). In THIS chat read ONLY\n"
            f"{orch}:  python3 bootstrap.py --trigger {trigger} --role orchestrator "
            f"--read 1 ...  (K = 1..{n_orch})\n"
            f"and follow it. Do NOT read the other Step 7 specs in this chat unless that spec "
            f"sends you to DIRECT MODE.")


def budget_block(args, specs, files_meta):
    """--trigger advisory: what the session must read, priced on the measured basis."""
    # ── GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / Fix A1 ─────────────────
    # DISCLOSE THE COST BEFORE IT IS PAID. SKILL Rule 2 is a hard, unbounded
    # obligation and nothing anywhere priced it. This is a DISCLOSURE BLOCK, NOT A
    # GATE — same precedent as Framework_DeliveryFooter §2A. It never blocks a run.
    # 2026-11-06 (GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY): tokens are bytes/2.3 (was
    # bytes/4, ~40% low) and "read calls" are the chunks --read serves (the old
    # 150,000-char bash call is diverted to an unreadable file on the cloud surface).
    sec = _load_json("SPEC_SECTIONS.json") or {}
    sfiles = sec.get("files", {})
    budget = _session_budget()
    bpt = float(budget.get("bytes_per_token") or DEFAULT_BYTES_PER_TOKEN)
    klass = _session_class(args.progress, files_meta, trigger=args.trigger)
    notice = orchestrated_notice(args.trigger)
    if notice:
        print("\n" + notice)
    plans = _plans(sec, specs, klass)
    print(f"\nEntry-point spec(s) for '{args.trigger}' — READ IN FULL "
          f"(subject to SESSION CLASS below):")
    tot_l = tot_b = tot_t = tot_calls = 0
    for f in specs:
        meta, info = files_meta.get(f, {}), sfiles.get(f, {})
        ln = info.get("lines") or meta.get("lines") or 0
        by = info.get("bytes") or meta.get("bytes") or 0
        use_b = (info.get("reduced_bytes", by)
                 if klass == "NON-FINAL" and info.get("has_read_set") else info.get("final_read_bytes", by))
        calls = len(plans[f]) if plans[f] is not None else -(-use_b // 28000)
        tok = math.ceil(use_b / bpt)
        tot_l += ln; tot_b += use_b; tot_t += tok; tot_calls += calls
        tag = ""
        if klass == "NON-FINAL" and info.get("has_read_set"):
            tag = f"  [reduced from {by:,} B — {len(info.get('final_only_titles', []))} section(s) skipped]"
        if plans[f] is None:
            tag += "  [SPEC_SECTIONS.json does not describe this file]"
        print(f"  {f:<34} {ln:>6} lines  {use_b:>9,} B  ~{tok:>8,} tok"
              f"  ~{calls} read call(s){tag}")
    print(f"  {'-' * 96}")
    print(f"  {'PRE-WORK READ BUDGET':<34} {tot_l:>6} lines  {tot_b:>9,} B  "
          f"~{tot_t:>8,} tok  ~{tot_calls} read call(s)")
    print(f"  SESSION CLASS: {klass}")
    if (klass == "NON-FINAL" and not args.progress
            and args.trigger not in ("MockExplain", "TestExplain",
                                     "MockCreate", "TestCreate",
                                     "MockBlueprint")):
        print("    FRESH CORPUS — the paper count is not knowable until PHASE A/A1b.")
        print("    Read the NON-FINAL set now and re-decide the class there (§S8-0b).")
        print("    If A1b shows papers_remaining <= BATCH_SIZE, escalate to a FULL read")
        print("    BEFORE run_synthesise(). Escalation is MANDATORY and ONE-WAY.")
    elif klass == "NON-FINAL" and args.trigger in ("MockCreate", "TestCreate"):
        print("    Reduced read is permitted: the batch this session delivers is not the last of")
        print("    the frozen batch plan, so it never reaches Final Assembly (MTC S1-0).")
        print("    ESCALATION IS MANDATORY AND ONE-WAY (MTC S1-0) — before Final Assembly read the")
        print("    omitted Final-Assembly sections with  --read K --escalate  (below), then prove them")
        print("    with  --retention ... --escalate --when before-final.")
    elif klass == "NON-FINAL":
        print("    Reduced read is permitted: this session cannot clear the corpus, so it")
        print("    never reaches synthesis, QV, the summary or the schema/xlsx writers.")
        print("    ESCALATION IS MANDATORY AND ONE-WAY — if this session turns out to be")
        print("    final, read the omitted sections BEFORE run_synthesise(). §S8-0b.")
    else:
        print("    FULL READ REQUIRED — no exception. "
              + FINAL_READ_MESSAGES.get(args.trigger, FINAL_READ_DEFAULT))
    if klass == "NON-FINAL":
        print(f"    Escalation read (the omitted sections only):  python3 bootstrap.py "
              f"--trigger {args.trigger} --read K --escalate")
    prog = f" --progress {args.progress}" if args.progress else ""
    print(f"READ METHOD (measured 2026-11-06): read with  python3 bootstrap.py --trigger "
          f"{args.trigger}{prog} --read K\n"
          f"for K = 1..{tot_calls}, one call each, in order. Do NOT read specs with sed ranges "
          f"above 300 lines, and never\n"
          f"open a tool-output file the harness diverted. Then prove retention:  --retention "
          f"(the last chunk prints the exact command).")


def _regenerated_map_ok(fname):
    """A SPEC_SECTIONS.json that spec_source.py rebuilt for a project override is
    accepted only if it is EXACTLY what spec_sections derives from the files on disk
    now — re-derived here, never trusted from the record alone."""
    ss = _spec_sections()
    return open(fname, encoding="utf-8").read() == ss.render(ss.build("."))



# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
# PYTHON SESSION OF A STEP 7 PAPER (release 2026.11.13 — GAP-2026-11-13-RUN-NOT-READ; MTC S1-0R PYTHON SESSION)
#   python3 bootstrap.py --session-start --exam <E> --paper <N> [--level L] [--subject S] [--topic T] [--resume]
#   python3 bootstrap.py --run-block <file.py> --exam <E> --paper <N>
# Framework_MockTestCreate.md runs its python blocks in ONE namespace per paper; a shell starts a fresh python for
# every call, so a worker had to read every block (the session-start code of section 3 and the helper libraries of
# sections 6-11: ~235 KB, ~102,000 tokens) and type it out again in each new worker. The namespace is now kept on
# disk (/home/claude/<E>_M<N>_session_ns.pkl — a WORK FILE, so the O3-3 CHECKPOINT carries it). --session-start
# runs, in file order, every block whose first line is the ENGINE-RUN marker, from the verified spec (those block
# bodies are never served by --read: spec_sections.engine_ranges). --run-block runs one block the session wrote in
# the same namespace. Values are pickled one by one (a value that cannot be is LISTED on the next load, never lost
# silently); functions / classes are rebuilt from the logged source of the defs; modules are re-imported by name.
# A block's SystemExit (the spec's stop lines) prints its message and exits with its code; any other exception
# prints the spec line and the traceback and exits 1. Lives here (not in a new file) so it is verified with
# bootstrap itself and the skill's script inventory is unchanged.
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
import ast as _ns_ast
import pickle as _ns_pickle
import textwrap as _ns_textwrap
import traceback as _ns_traceback
import types as _ns_types

NS_VERSION = '1.0'
NS_ENGINE_MARK = '# ENGINE-RUN'
NS_SPEC_DEFAULT = 'Framework_MockTestCreate.md'
NS_NAME = 'fw_ns_session'
_NS_SKIP = {'__builtins__', '__name__', '__doc__', '__loader__', '__spec__', '__package__', '__file__',
         '__cached__', '__annotations__'}


def ns_home_dir():
    return os.environ.get('FW_HOME', '/home/claude')


def ns_path(exam, paper):
    return os.path.join(ns_home_dir(), f'{exam}_M{paper}_session_ns.pkl')


def ns_engine_blocks(spec_path=NS_SPEC_DEFAULT):
    """[(line, source)] — every ```python block whose first body line starts with ENGINE_MARK, dedented, in file
    order. `line` is the 1-based line of the opening fence. Pure (reads the file only)."""
    with open(spec_path, encoding='utf-8') as fh:
        lines = fh.read().split('\n')
    out, cur = [], None
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if cur is None:
            if s.startswith('```python'):
                cur = (i, [])
            continue
        if s.startswith('```'):
            body = cur[1]
            first = next((b for b in body if b.strip()), '')
            if first.strip().startswith(NS_ENGINE_MARK):
                out.append((cur[0], _ns_textwrap.dedent('\n'.join(body))))
            cur = None
            continue
        cur[1].append(ln)
    return out


def _ns_defs_source(src):
    """The top-level import / def / class statements of `src`, as source, in order (what a reload re-executes)."""
    try:
        tree = _ns_ast.parse(src)
    except SyntaxError:
        return []
    out = []
    for node in tree.body:
        if isinstance(node, (_ns_ast.Import, _ns_ast.ImportFrom, _ns_ast.FunctionDef, _ns_ast.AsyncFunctionDef, _ns_ast.ClassDef)):
            seg = _ns_ast.get_source_segment(src, node)
            if seg:
                if getattr(node, 'decorator_list', None):
                    deco = '\n'.join('@' + _ns_ast.get_source_segment(src, d) for d in node.decorator_list)
                    seg = deco + '\n' + seg
                out.append(seg)
    return out


def ns_new():
    """A fresh session namespace — the __dict__ of a module registered as NS_NAME, so an instance of a class a
    block defined pickles by reference and loads again once the class is re-defined."""
    mod = _ns_types.ModuleType(NS_NAME)
    sys.modules[NS_NAME] = mod
    ns = mod.__dict__
    ns['__builtins__'] = __builtins__
    return ns


def ns_load(exam, paper, out=print):
    """The saved namespace of the paper (a fresh one when none is saved). Never raises."""
    ns = ns_new()
    p = ns_path(exam, paper)
    if not os.path.exists(p):
        return ns, {'defs': [], 'lost': []}
    try:
        with open(p, 'rb') as fh:
            rec = _ns_pickle.load(fh)
    except Exception as ex:                                   # noqa: BLE001
        out(f'FW-NS: the saved session {os.path.basename(p)} does not load ({type(ex).__name__}: {ex}) — '
            f'starting a fresh namespace; run --session-start again.')
        return ns, {'defs': [], 'lost': []}
    for k, modname in (rec.get('modules') or {}).items():
        try:
            ns[k] = __import__(modname, fromlist=['_'])
        except Exception:                                     # noqa: BLE001
            pass
    # two passes: a def whose default argument names a saved value, and a saved instance of a class a block
    # defined, each need the other first — defs, values, then whatever failed of both, once more
    failed_defs, failed_vals = [], []
    for src in rec.get('defs') or []:
        try:
            exec(compile(src, '<session reload>', 'exec'), ns)
        except Exception:                                     # noqa: BLE001
            failed_defs.append(src)
    for k, blob in (rec.get('values') or {}).items():
        try:
            ns[k] = _ns_pickle.loads(blob)
        except Exception:                                     # noqa: BLE001
            failed_vals.append((k, blob))
    for src in failed_defs:
        try:
            exec(compile(src, '<session reload>', 'exec'), ns)
        except Exception:                                     # noqa: BLE001
            pass
    for k, blob in failed_vals:
        try:
            ns[k] = _ns_pickle.loads(blob)
        except Exception:                                     # noqa: BLE001
            rec.setdefault('lost', []).append(k)
    if rec.get('lost'):
        out(f"FW-NS: not restored (could not be saved): {sorted(set(rec['lost']))} — a block that needs one of them "
            f"rebuilds it from the paper's files.")
    return ns, {'defs': list(rec.get('defs') or []), 'lost': list(rec.get('lost') or [])}


def _ns_dedupe_defs(defs):
    """The definition log without repeats: the LAST occurrence of an identical source is kept (its position is
    where it was last run, so a later re-definition still wins)."""
    seen, out = set(), []
    for src in reversed(list(defs or [])):
        if src in seen:
            continue
        seen.add(src)
        out.append(src)
    return list(reversed(out))


def ns_save(ns, meta, exam, paper):
    """Persist `ns` (values pickled one by one; functions / classes as their logged source). Returns the names
    that could not be saved. Never raises."""
    values, modules, lost = {}, {}, []
    for k, v in list(ns.items()):
        if k in _NS_SKIP:
            continue
        if isinstance(v, _ns_types.ModuleType):
            modules[k] = v.__name__
            continue
        if isinstance(v, (_ns_types.FunctionType, type)) and getattr(v, '__module__', None) == NS_NAME \
                and getattr(v, '__name__', None) == k:
            continue                                         # rebuilt from the logged source (an alias is pickled
            #                                                  by reference below; a lambda is listed as not saved)
        if isinstance(v, (_ns_types.BuiltinFunctionType, _ns_types.FunctionType, type)) and getattr(v, '__module__', None) \
                not in (None, NS_NAME):
            mod = getattr(v, '__module__', None)
            try:
                if getattr(sys.modules.get(mod), getattr(v, '__name__', ''), None) is v:
                    values[k] = _ns_pickle.dumps(v)
                    continue
            except Exception:                                 # noqa: BLE001
                pass
        try:
            values[k] = _ns_pickle.dumps(v)
        except Exception:                                     # noqa: BLE001
            lost.append(k)
    rec = {'version': NS_VERSION, 'values': values, 'modules': modules, 'defs': _ns_dedupe_defs(meta.get('defs')),
           'lost': lost}
    p = ns_path(exam, paper)
    tmp = p + '.tmp'
    try:
        with open(tmp, 'wb') as fh:
            _ns_pickle.dump(rec, fh)
        os.replace(tmp, p)
    except OSError as ex:
        print(f'FW-NS: could not save the session ({ex}).')
    return lost


def _ns_exec_block(src, label, ns, meta):
    """Run one block in ns, logging its defs. Returns None, or ('exit', code) / ('error', text)."""
    meta.setdefault('defs', []).extend(_ns_defs_source(src))
    try:
        exec(compile(src, label, 'exec'), ns)
    except SystemExit as ex:
        return ('exit', ex.code)
    except Exception:                                         # noqa: BLE001
        return ('error', _ns_traceback.format_exc())
    return None


def ns_session_start(exam, paper, level=None, subject=None, topic=None, resume=False, grader_model=None,
                  spec_path=NS_SPEC_DEFAULT, out=print):
    """Run every ENGINE-RUN block of the spec, in file order, in the paper's namespace. Returns (rc, ns)."""
    ns, meta = ns_load(exam, paper, out=out)
    # the definitions earlier blocks made stay (a helper a non-engine block defined is still there for the next
    # worker); the engine blocks' definitions are logged again after them, so the verified text wins
    ns.update({'EXAM': exam, 'N': int(paper), 'RESUME_TRIGGER': bool(resume)})
    # the trigger's scope: a later session start that omits an option keeps the value the paper started with
    # (a continuing worker never turns a subject test into a full mock by leaving --level out)
    for _k, _v in (('LEVEL', level), ('SCOPE_SUBJECT', subject), ('SCOPE_TOPIC', topic)):
        if _v is not None or _k not in ns:
            ns[_k] = _v
    if grader_model:
        ns['GRADER_MODEL_ID'] = grader_model
    blocks = ns_engine_blocks(spec_path)
    if not blocks:
        out(f'FW-NS: {spec_path} has no ENGINE-RUN block — nothing to run (read the spec as before).')
        return 2, ns
    for line, src in blocks:
        src = src.replace('"[ExamCode]"', repr(exam)).replace("'[ExamCode]'", repr(exam))
        if 'RESUME = False' in src and resume:
            src = src.replace('RESUME = False', 'RESUME = True', 1)
        res = _ns_exec_block(src, f'<{os.path.basename(spec_path)}:{line}>', ns, meta)
        if res is not None:
            lost = ns_save(ns, meta, exam, paper)
            if res[0] == 'exit':
                if res[1] not in (None, 0):
                    out(str(res[1]))
                out(f'FW-NS: session start stopped in the block at {os.path.basename(spec_path)} line {line}.')
                return (res[1] if isinstance(res[1], int) else 1) or 0, ns
            out(res[1])
            out(f'FW-NS: the block at {os.path.basename(spec_path)} line {line} raised — session start stopped; '
                f'the error above is the report.')
            return 1, ns
    lost = ns_save(ns, meta, exam, paper)
    out(f'FW-NS SESSION READY {exam} M{paper}: {len(blocks)} engine blocks run'
        + (f'; not saved: {sorted(lost)}' if lost else '') + '.')
    return 0, ns


def ns_run_file(path, exam, paper, out=print):
    """Run one block file in the paper's namespace and save it. Returns (rc, ns)."""
    ns, meta = ns_load(exam, paper, out=out)
    try:
        with open(path, encoding='utf-8') as fh:
            src = fh.read()
    except OSError as ex:
        out(f'FW-NS: cannot read {path} ({ex}).')
        return 2, ns
    res = _ns_exec_block(src, f'<{os.path.basename(path)}>', ns, meta)
    lost = ns_save(ns, meta, exam, paper)
    if res is None:
        return 0, ns
    if res[0] == 'exit':
        if res[1] not in (None, 0):
            out(str(res[1]))
        return (res[1] if isinstance(res[1], int) else 1) or 0, ns
    out(res[1])
    return 1, ns


def ns_self_test():
    import tempfile
    ok, bad = [], []

    def check(name, cond):
        (ok if cond else bad).append(name)
    with tempfile.TemporaryDirectory() as d:
        os.environ['FW_HOME'] = d
        spec = os.path.join(d, 'S.md')
        open(spec, 'w', encoding='utf-8').write(
            '# S\n\n  ```python\n  # ENGINE-RUN S3-1\n  import json, re\n  EXAM = "[ExamCode]"\n  RESUME = False\n'
            '  LEDGER = globals().get("LEDGER", set())\n  def helper(x):\n      return f"{EXAM}:{x}:{len(LEDGER)}"\n'
            '  PAT = re.compile("a+")\n  class Box:\n      def __init__(self, v):\n          self.v = v\n'
            '  ```\n\n  ```python\n  not_engine = 1\n  ```\n\n  ```python\n  # ENGINE-RUN S10-3\n'
            '  def fmt(s):\n      return helper(s).upper()\n  ```\n')
        bl = ns_engine_blocks(spec)
        check('engine_blocks_marked_only_in_order', [b[0] for b in bl] == [3, 21] and 'not_engine' not in str(bl))
        rc, ns = ns_session_start('EX', 1, level='subject', resume=True, spec_path=spec, out=lambda *a: None)
        check('session_start_binds_and_runs', rc == 0 and ns['EXAM'] == 'EX' and ns['RESUME'] is True
              and ns['fmt']('q') == 'EX:Q:0' and ns['N'] == 1 and ns['LEVEL'] == 'subject')
        blk = os.path.join(d, 'b.py')
        open(blk, 'w').write('LEDGER.add("k1")\nB = Box(3)\nVAL = helper("z")\nimport math\nR = math.sqrt(16)\n')
        rc2, ns2 = ns_run_file(blk, 'EX', 1, out=lambda *a: None)
        msgs = []
        open(blk, 'w').write('OUT = (fmt("w"), sorted(LEDGER), VAL, R, PAT.match("aa") is not None, math.pi > 3)\n')
        rc3, ns3 = ns_run_file(blk, 'EX', 1, out=msgs.append)
        check('state_survives_processes', rc2 == 0 and rc3 == 0
              and ns3['OUT'] == ('EX:W:1', ['k1'], 'EX:z:1', 4.0, True, True) and ns3['B'].v == 3)
        open(blk, 'w').write('GEN = (i for i in range(3))\n')
        ns_run_file(blk, 'EX', 1, out=lambda *a: None)
        m3b = []
        ns3b, _ = ns_load('EX', 1, out=m3b.append)
        check('unpicklable_is_listed_never_silent', any("'GEN'" in m for m in m3b) and 'GEN' not in ns3b)
        open(blk, 'w').write('raise SystemExit("HARD STOP [HS:INPUT]: x missing")\n')
        m4 = []
        rc4, _ = ns_run_file(blk, 'EX', 1, out=m4.append)
        check('hard_stop_surfaces_message_and_code', rc4 == 1 and any('HARD STOP' in m for m in m4))
        open(blk, 'w').write('1/0\n')
        m5 = []
        rc5, _ = ns_run_file(blk, 'EX', 1, out=m5.append)
        check('error_reports_traceback', rc5 == 1 and any('ZeroDivisionError' in m for m in m5))
        open(blk, 'w').write('OUT2 = sorted(LEDGER)\n')
        rc6, ns6 = ns_run_file(blk, 'EX', 1, out=lambda *a: None)
        check('state_kept_after_a_failed_block', rc6 == 0 and ns6['OUT2'] == ['k1'])
        open(blk, 'w').write('DEFAULT_SEP = "|"\ndef joiner(a, b, sep=DEFAULT_SEP):\n    return a + sep + b\n')
        ns_run_file(blk, 'EX', 1, out=lambda *a: None)
        rc7, ns7 = ns_session_start('EX', 1, spec_path=spec, out=lambda *a: None)
        open(blk, 'w').write('J = joiner("a", "b")\nALIAS = joiner\nLAM = lambda x: x\n')
        rc7b, ns7b = ns_run_file(blk, 'EX', 1, out=lambda *a: None)
        check('block_helpers_survive_a_session_start_and_defaults_reload', rc7b == 0 and ns7b['J'] == 'a|b')
        m7 = []
        ns7c, _ = ns_load('EX', 1, out=m7.append)
        check('alias_kept_lambda_listed', ns7c['ALIAS']('x', 'y') == 'x|y' and any("'LAM'" in m for m in m7))
        check('session_start_again_keeps_state_idempotent', rc7 == 0 and sorted(ns7['LEDGER']) == ['k1']
              and ns7['RESUME'] is False and ns7['LEVEL'] == 'subject')
        open(os.path.join(d, 'EX_M1_session_ns.pkl'), 'wb').write(b'garbage')
        m8 = []
        ns8, _ = ns_load('EX', 1, out=m8.append)
        check('corrupt_session_is_reported_and_fresh', any('does not load' in m for m in m8) and 'LEDGER' not in ns8)
        open(spec, 'w').write('# S\n```python\nx = 1\n```\n')
        rc9, _ = ns_session_start('EX', 2, spec_path=spec, out=lambda *a: None)
        check('no_engine_block_is_reported', rc9 == 2)
        os.environ.pop('FW_HOME', None)
    return ok, bad




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trigger", default=None, help="optional step trigger, e.g. MockDeliver")
    ap.add_argument("--progress", default=None, help=PROGRESS_HELP)
    ap.add_argument("--manifest", default="MANIFEST.json")
    ap.add_argument("--receipt", action="store_true",
                    help="with --trigger: print a READ RECEIPT per routed spec (P1)")
    ap.add_argument("--read", type=int, default=None, metavar="K",
                    help="with --trigger: serve read chunk K (K=1 starts a new read)")
    ap.add_argument("--role", choices=("session", "orchestrator"), default="session")
    ap.add_argument("--read-id", default=None)
    ap.add_argument("--escalate", action="store_true",
                    help="read / check the sections the NON-FINAL read skipped")
    ap.add_argument("--retention", default=None, metavar='"01=CODE 02=CODE ..."')
    ap.add_argument("--when", choices=RETENTION_WHEN, default="after-read")
    ap.add_argument("--read-receipts", action="store_true")
    ap.add_argument("--stage-inputs", action="store_true")
    ap.add_argument("--make-cache", default=None, metavar="OUT.zip",
                    help="2026.11.10 (G-14): write a project-cacheable copy of THIS verified release (every "
                         "MANIFEST file + MANIFEST.json); SKILL Step 0 uses it only when primary and mirror fail")
    ap.add_argument("--stage-doc", default=None, metavar="NAME")
    ap.add_argument("--from", dest="from_path", default=None, metavar="PATH")
    ap.add_argument("--typed", action="store_true")
    ap.add_argument("--stage-status", action="store_true")
    ap.add_argument("--stage-project-docs", action="store_true")
    ap.add_argument("--worker-report", choices=("write", "show"), default=None)
    ap.add_argument("--checkpoint", choices=("make", "restore", "drop", "status"), default=None,
                    help="2026.11.12: the O3-3 CHECKPOINT (make = refresh to the current progress)")
    ap.add_argument("--part", type=int, default=1,
                    help="--worker-report show: which part of the chat block (default 1)")
    ap.add_argument("--exam", default=None)
    ap.add_argument("--paper", default=None)
    ap.add_argument("--state", default=None)
    ap.add_argument("--batch", default=None)
    ap.add_argument("--of", default=None)
    ap.add_argument("--files", default=None)
    ap.add_argument("--chat-file", default=None)
    ap.add_argument("--review-parts", default=None)
    ap.add_argument("--tokens-note", default=None)
    ap.add_argument("--worker-prompt", action="store_true")
    ap.add_argument("--trigger-text", default="")
    ap.add_argument("--continue", dest="cont", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    # 2026.11.13 — the python session of a Step 7 paper (MTC S1-0R PYTHON SESSION)
    ap.add_argument("--session-start", action="store_true",
                    help="2026.11.13: run every ENGINE-RUN block of the verified spec in the paper's namespace")
    ap.add_argument("--run-block", default=None, metavar="FILE",
                    help="2026.11.13: run one block file in the paper's namespace (kept on disk)")
    ap.add_argument("--level", default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--topic", default=None)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--grader-model", default=None)
    ap.add_argument("--spec", default=None, metavar="FILE")
    args = ap.parse_args()
    if args.make_cache:
        # 2026.11.10 (G-14 row 1): the project-cached verified release — every top-level file of this clone (what a
        # git clone gives: specs, engines, bootstrap, manifests; never .git / caches); Step 0 extracts it and this
        # same bootstrap re-verifies every hash against the MANIFEST.json inside it
        import zipfile as _zf
        _here = os.path.dirname(os.path.abspath(__file__))
        _man = json.load(open(os.path.join(_here, args.manifest), encoding="utf-8"))
        _names = sorted(n for n in os.listdir(_here) if os.path.isfile(os.path.join(_here, n))
                        and not n.startswith('.') and not n.endswith('.pyc'))
        with _zf.ZipFile(args.make_cache, "w", _zf.ZIP_DEFLATED) as _z:
            for _n in _names:
                _p = os.path.join(_here, _n)
                if os.path.isfile(_p):
                    _z.write(_p, _n)
        print(f"CACHE written: {args.make_cache} ({len(_names)} files, release {_man.get('framework_version')})")
        sys.exit(0)

    # Sub-commands that are not the verification gate; each returns its exit code.
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    if args.stage_inputs:
        sys.exit(stage_inputs(args.trigger))
    if args.stage_doc:
        sys.exit(stage_doc(args.stage_doc, args.from_path, args.typed))
    if args.stage_project_docs:
        sys.exit(stage_project_docs())
    if args.stage_status:
        sys.exit(stage_status())
    if args.checkpoint:
        sys.exit(checkpoint_cmd(args))
    if args.session_start or args.run_block:
        if not args.exam or not args.paper or not str(args.paper).isdigit():
            print("FW-NS: --exam <ExamCode> and --paper <N> are required.")
            sys.exit(2)
        if args.session_start:
            sys.exit(ns_session_start(args.exam, int(args.paper), args.level, args.subject, args.topic, args.resume,
                                      args.grader_model, spec_path=args.spec or NS_SPEC_DEFAULT)[0])
        sys.exit(ns_run_file(args.run_block, args.exam, int(args.paper))[0])
    if args.worker_report == "write":
        sys.exit(worker_report_write(args))
    if args.worker_report == "show":
        sys.exit(worker_report_show(args))
    if args.worker_prompt:
        sys.exit(worker_prompt(args.trigger_text, args.cont))
    if args.retention is not None:
        sys.exit(cmd_retention(args))
    if args.read_receipts:
        sys.exit(cmd_read_receipts(args))
    if args.read is not None:
        sys.exit(cmd_read(args))

    # A verify that fails must not leave an earlier pass behind: --read is served only
    # where .verified exists.
    if os.path.exists(".verified"):
        os.remove(".verified")
    if not os.path.exists(args.manifest):
        fail("MANIFEST.json missing from clone (partial/failed clone?)")
    try:
        M = json.load(open(args.manifest, encoding="utf-8"))
    except Exception as e:
        fail(f"MANIFEST.json is not valid JSON: {e}")

    prov_path = os.path.join(os.path.dirname(os.path.abspath(args.manifest)),
                             ".spec_provenance.json")
    prov, overrides, regen = None, {}, {}
    if os.path.exists(prov_path):
        try:
            prov = json.load(open(prov_path, encoding="utf-8"))
        except Exception as e:
            fail(f".spec_provenance.json is not valid JSON: {e}")
        for entry in prov.get("project_unverified", []):
            fname = entry.get("file", "")
            if not fname.endswith(".md"):
                fail(f".spec_provenance.json lists a non-spec file '{fname}'. Only "
                     f".md specs may be project-sourced; an engine is never excused "
                     f"from manifest verification.")
            if not entry.get("sha256"):
                fail(f".spec_provenance.json entry for '{fname}' has no sha256 — the "
                     f"record is unusable and cannot excuse the file.")
            overrides[fname] = entry["sha256"]
        # GAP-2026-11-06 D-5: with a project spec laid over the repo, spec_source.py
        # rebuilds SPEC_SECTIONS.json so the read ranges describe the file actually read.
        # Only that one generated map may be listed, and it is re-derived below.
        for entry in prov.get("regenerated", []):
            if entry.get("file") != "SPEC_SECTIONS.json" or not entry.get("sha256"):
                fail(f".spec_provenance.json lists '{entry.get('file')}' as regenerated. Only "
                     f"SPEC_SECTIONS.json (with its sha256) may be; nothing else is excused.")
            regen[entry["file"]] = entry["sha256"]

    files_meta = M.get("files", {})
    routes = M.get("routes", {})
    fw_version = M.get("framework_version", "?")
    if not files_meta:
        fail("MANIFEST.json has no files listed")

    verified, unverified, regenerated = [], [], []
    for fname, meta in sorted(files_meta.items()):
        if not os.path.exists(fname):
            fail(f"{fname}: file absent in clone (partial clone / deleted file)")
        actual = sha256(fname)
        if fname in overrides:
            # Deliberately overridden by the project. No repo reference exists, so
            # manifest comparison is meaningless — but the file must still be the one
            # the resolver inspected and approved (P1-P5).
            if actual != overrides[fname]:
                fail(f"{fname}: listed as a project override, but its sha256 does not "
                     f"match the resolver's record\n  resolver saw {overrides[fname]}"
                     f"\n  on disk now  {actual}\n"
                     f"The overlay was modified after resolution. Re-run "
                     f"spec_source.py --resolve.")
            unverified.append(fname)
            continue
        if fname in regen:
            if actual != regen[fname] or not _regenerated_map_ok(fname):
                fail(f"{fname}: listed as regenerated by spec_source.py, but it is not the "
                     f"map the effective specs on disk derive. Re-run spec_source.py --resolve.")
            regenerated.append(fname)
            continue
        if actual != meta["sha256"]:
            fail(f"{fname}: sha256 MISMATCH\n  expected {meta['sha256']}\n  actual   {actual}")
        lines = read_lines(fname)
        if len(lines) != meta["lines"]:
            fail(f"{fname}: line count {len(lines)} != manifest {meta['lines']}")
        if fname.endswith(".md"):
            if not lines or lines[0].rstrip() != meta["version_header"].rstrip():
                fail(f"{fname}: version header mismatch\n  expected '{meta['version_header']}'\n  actual   '{(lines[0] if lines else '')}'")
            nonblank = [l for l in lines if l.strip() != ""]
            if not nonblank or nonblank[-1] != meta["end_sentinel"]:
                fail(f"{fname}: END sentinel not last line -> possible truncation. "
                     f"Expected: '{meta['end_sentinel']}'")
        verified.append(fname)

    token = {"framework_version": fw_version, "files": verified,
             "project_unverified": unverified,
             "read_rule": "Read each .md IN FULL to its END-sentinel line; line counts are exact."}
    if regenerated:
        token["regenerated"] = regenerated
    with open(".verified", "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)

    if unverified:
        print(f"[OK] FRAMEWORK {fw_version} PARTIALLY VERIFIED — "
              f"{len(verified)}/{len(files_meta)} files pass all checksum/version/whole-file "
              f"checks; {len(unverified)} spec(s) are PROJECT-UNVERIFIED and cannot be "
              f"checked against the manifest:")
        for fname in unverified:
            print(f"  [PROJECT-UNVERIFIED] {fname} — sourced from the project Files "
                  f"section. Integrity unknown; it may be stale or out of step with the "
                  f"repo engines. Disclose in the delivery footer (§2A).")
        for fname in regenerated:
            print(f"  [REGENERATED] {fname} — rebuilt by spec_source.py from the effective "
                  f"specs and re-derived here: it describes the files actually read.")
        print("This is NOT a failure and does NOT halt the run (SKILL rule 4, "
              "Framework_DeliveryFooter §2A).")
    else:
        print(f"[OK] FRAMEWORK {fw_version} VERIFIED — {len(verified)}/{len(files_meta)} files, "
              f"all checksums/versions/whole-file checks PASS")
    surface_notice(args.trigger)

    if args.trigger:
        entry = routes.get(args.trigger)
        if entry:
            specs = [f for f in entry if f.endswith(".md")]
            engines = [f for f in entry if f.endswith(".py")]
            budget_block(args, specs, files_meta)
            if engines:
                print(f"Routed engine(s) for '{args.trigger}' — EXECUTE via `import` inside the "
                      f"spec's code blocks; do NOT read these into context: {engines}")
            if args.receipt:
                # P1 (GAP-2026-11-02): the exact spec bytes this run is held to.
                for f in specs:
                    if not os.path.exists(f):
                        continue
                    _ls = read_lines(f)
                    _nb = [l for l in _ls if l.strip() != ""]
                    print("READ RECEIPT " + json.dumps(
                        {"spec": f, "lines": len(_ls), "sha256": sha256(f),
                         "end_sentinel": (_nb[-1] if _nb else ""),
                         # the spec's own "# END OF <spec> vX" line (None when it has none):
                         # a reader that reached it has read the whole spec body
                         "end_marker": next((l for l in reversed(_nb)
                                             if l.startswith("# END OF")), None)},
                        ensure_ascii=False))
                print("READ RULE: trimmed, summarised or partial working copies of a spec "
                      "are PROHIBITED; a run that declares one records finding A-READ in its "
                      "delivery footer.")
        else:
            print(f"[note] trigger '{args.trigger}' not in advisory routes; "
                  f"read the spec whose header matches your step. All files are verified & present.")
    ensure_compression_tools(args.trigger)
    print(".verified written. Read the needed spec(s) (.md) in full; engines (.py) are "
          "executed, not read.")
    notice = orchestrated_notice(args.trigger) if args.trigger else None
    if notice:
        print("\n" + notice)


def self_test():
    """Hermetic (D11): a tiny fixture corpus in a temp dir — its own routes.json,
    SPEC_SECTIONS.json built by spec_sections, SESSION_BUDGET.json and a MANIFEST.json
    from gen_manifest.py — and FW_* overrides pointing at temp dirs, so nothing under
    /mnt or /home/claude and no network is touched. Every sub-command runs as a
    subprocess exactly as a session runs it."""
    import subprocess, tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import spec_sections as ss
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    tmp = tempfile.mkdtemp(prefix="bootstrap_st_")
    env = dict(os.environ, FW_PROJECT_DIR=os.path.join(tmp, "project"),
               FW_UPLOADS_DIR=os.path.join(tmp, "uploads"),
               FW_ATTACH_DIR=os.path.join(tmp, "attach"), FW_HOME=os.path.join(tmp, "home"))

    def run(cwd, *argv):
        r = subprocess.run([sys.executable, os.path.join(here, "bootstrap.py")] + list(argv),
                           cwd=cwd, env=env, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    # ── fixture corpus: a Step 7 spec named as the real one so its read set applies ──
    fx = os.path.join(tmp, "repo")
    os.makedirs(fx)
    mtc = ["# Framework_MockTestCreate v9.0", "# v9.0 — 2026-11-06 — fixture",
           "# MANDATE 0 — NO QUESTION CONTENT IN CHAT", "# MANDATE 1 — BATCH STOP LAW",
           "## S1-0 — SESSION CLASS", "class law",
           "## S4-1 — BATCH LAW"] + [f"batch rule line {i:05d}" for i in range(4300)] + [
           "## S13-1 — Final Assembly trigger", "fa",
           "## S13-2F — PRE-COMMIT ITEM SWEEP", "sweep",
           "## S13-2G — INDEPENDENT REVIEW", "review",
           "## S13-9A — Post-delivery footer", "footer law",
           "## S17-2 — Downstream handoff", "handoff", "# ═══════",
           "# §18 — AUDIT GATE GLOSSARY", "glossary law",
           "# END OF Framework_MockTestCreate v9.0", ""]
    files = {"Framework_MockTestCreate.md": "\n".join(mtc),
             "Framework_MockTestOrchestrate.md":
                 "# Framework_MockTestOrchestrate v1.0.0\n# v1.0.0 — 2026-11-06 — fixture\n"
                 "## O0-1 — orchestrator law\nPART A\n# END OF Framework_MockTestOrchestrate v1.0.0\n",
             "Framework_Footer.md": "# Framework_Footer v1.0\n## F-1 — footer\nfooter\n"
                                    "# END OF Framework_Footer v1.0\n"}
    for name, text in files.items():
        with open(os.path.join(fx, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    route = ["Framework_MockTestCreate.md", "Framework_MockTestOrchestrate.md",
             "Framework_Footer.md"]
    with open(os.path.join(fx, "routes.json"), "w", encoding="utf-8") as fh:
        json.dump({"TestCreate": route, "PYQScan": ["Framework_Footer.md"],
                   "PYQDraft": ["Framework_Footer.md"]}, fh)
    with open(os.path.join(fx, "SESSION_BUDGET.json"), "w", encoding="utf-8") as fh:
        json.dump({"bytes_per_token": 2.3, "orchestrated": {"TestCreate": {
            "orchestrator_spec": "Framework_MockTestOrchestrate.md"}}}, fh)
    with open(os.path.join(fx, "SPEC_SECTIONS.json"), "w", encoding="utf-8") as fh:
        fh.write(ss.render(ss.build(fx)))
    subprocess.run([sys.executable, os.path.join(here, "gen_manifest.py")], cwd=fx, env=env,
                   capture_output=True, check=True)
    sec = json.load(open(os.path.join(fx, "SPEC_SECTIONS.json"), encoding="utf-8"))
    bs_path = os.path.join(fx, "batch_state.json")
    with open(bs_path, "w", encoding="utf-8") as fh:
        json.dump({"batch_plan": [{"batch_id": "B1"}, {"batch_id": "B2"}, {"batch_id": "B3"}],
                   "batches_completed": [], "current_batch": "B1"}, fh)

    # D1 + D5: verify passes; surface notice when the project dir is absent; budget block
    rc, out = run(fx, "--trigger", "TestCreate")
    final_n = sum(len(ss.chunk_plan(sec, f, "FINAL", fx)) for f in route)
    check("verify passes on the fixture corpus", rc == 0 and "VERIFIED" in out)
    check("D1 surface notice when the project dir is absent",
          "SURFACE: project files are not mounted" in out and "--stage-inputs" in out)
    check("D5 orchestrated notice precedes the budget block",
          "STEP 7 RUNS ORCHESTRATED (owner decision OD-2026-11-06)" in out
          and out.index("STEP 7 RUNS ORCHESTRATED") < out.index("PRE-WORK READ BUDGET"))
    check("D5 Step 7 FINAL wording and measured read method",
          "FULL READ REQUIRED — no exception. This session may run Final Assembly and commit "
          "the registry." in out and "READ METHOD (measured 2026-11-06)" in out
          and f"for K = 1..{final_n}," in out and "188,024" not in out
          and "section_rules.md" not in out)
    check("D5 orchestrated notice is also the LAST lines of the output",
          out.rstrip().endswith("sends you to DIRECT MODE.")
          and out.count("STEP 7 RUNS ORCHESTRATED") == 2)
    with open(os.path.join(fx, "bs_adv.json"), "w", encoding="utf-8") as fh:
        json.dump({"batch_plan": [{"batch_id": "B1"}, {"batch_id": "B2"}],
                   "batches_completed": [], "current_batch": "B1"}, fh)
    rc, out = run(fx, "--trigger", "TestCreate", "--progress", "bs_adv.json")
    check("D5 Step 7 NON-FINAL advisory names the escalation read, not Step 5's writer",
          rc == 0 and "SESSION CLASS: NON-FINAL" in out and "run_synthesise" not in out
          and "--read K --escalate" in out and "Final Assembly (MTC S1-0)" in out)
    os.remove(os.path.join(fx, "bs_adv.json"))
    rc, out = run(fx, "--trigger", "PYQDraft")
    check("D5 generic FINAL wording never names a Step 5 writer",
          "FULL READ REQUIRED — no exception. This session may write final artefacts." in out
          and "section_rules" not in out and "STEP 7 RUNS ORCHESTRATED" not in out)

    # D6/D7: FINAL session read, chunk by chunk
    def read_all(*extra, n=None):
        outs, k = [], 1
        while True:
            rc, out = run(fx, "--trigger", "TestCreate", "--read", str(k), *extra)
            if rc != 0:
                return outs, rc, out
            outs.append(out)
            m = re.search(r"chunk \d+ of (\d+)", out)
            if k == int(m.group(1)) or k == n:
                return outs, 0, out
            k += 1

    def bodies(outs):
        return "".join(re.search(r"===\n(.*)=== END chunk", o, re.S).group(1) for o in outs)

    def state(role="session", esc=False):
        p = os.path.join(fx, READ_STATE_DIR, f"current_{role}" + ("_escalate" if esc else ""))
        rid = open(p, encoding="utf-8").read().strip()
        return json.load(open(os.path.join(fx, READ_STATE_DIR, rid + ".json"), encoding="utf-8"))

    def codes(st):
        return " ".join(f"{nn}={c}" for nn, c in st["anchors"].items())

    outs, rc, last = read_all()
    st = state()
    whole = "".join(open(os.path.join(fx, f), encoding="utf-8").read() for f in route)
    check("FINAL read serves every routed spec whole, byte for byte",
          rc == 0 and len(outs) == final_n and bodies(outs) == whole)
    check("every chunk within 300 lines and 28,000 B",
          all(c["end"] - c["start"] + 1 <= 300 for c in st["chunks"])
          and all(len(re.search(r"===\n(.*)=== END", o, re.S).group(1).encode()) <= 28000
                  for o in outs))
    akt = [k for k, o in enumerate(outs, 1) if "<<READ-ANCHOR" in o]
    check("anchors on chunk 1, every 8th and the last",
          final_n > 16 and akt == sorted({1, final_n} | set(range(8, final_n, 8)))
          and outs[0].rstrip().endswith("you will be asked for it>>"))
    check("READ COMPLETE after the last chunk names the retention command",
          "READ COMPLETE" in last and "--retention" in last)
    rc, out = run(fx, "--retention", codes(st))
    check("retention PASS with every anchor", rc == 0 and "RETENTION: PASS" in out)
    bad = codes(st).replace(st["anchors"]["01"], "BBBBBBB")
    rc, out = run(fx, "--retention", bad, "--when", "before-batch")
    check("retention FAIL (exit 3) on one wrong code, never printing the codes",
          rc == 3 and "1 anchor(s) wrong or missing" in out
          and all(c not in out for c in st["anchors"].values()))
    rc, out = run(fx, "--read-receipts")
    check("read receipts name lines, chunks, sha and retention",
          "READ RECEIPT Framework_MockTestCreate.md lines 1-" in out
          and f"retention FAIL" in out and st["read_id"] in out)
    rc, out = run(fx, "--trigger", "TestCreate", "--read", "1")
    rc2, out2 = run(fx, "--trigger", "TestCreate", "--read", "3")
    check("an out-of-order chunk is served with a READ ORDER warning",
          rc2 == 0 and "READ ORDER: expected chunk 2" in out2)
    rc, out = run(fx, "--retention", codes(state()))
    check("retention FAIL when a chunk was never read",
          rc == 3 and "chunk(s) never read" in out)
    rc, out = run(fx, "--trigger", "TestCreate", "--read", "999")
    check("unknown chunk exits 2", rc == 2)

    # NON-FINAL read: exactly the plan; preamble + banner read; S13-2F/2G not; escalation
    outs, rc, _ = read_all("--progress", bs_path)
    nf = state()
    lines = open(os.path.join(fx, "Framework_MockTestCreate.md"), encoding="utf-8").read().split("\n")
    served = {(c["file"], j) for c in nf["chunks"] for j in range(c["start"], c["end"] + 1)}
    plan = {(f, j) for f in route for a, b in ss.read_plan(sec, f, "NON-FINAL")
            for j in range(a, b + 1)}
    text = bodies(outs)
    check("NON-FINAL read covers exactly read_plan(NON-FINAL)",
          rc == 0 and nf["class"] == "NON-FINAL" and served == plan)
    check("NON-FINAL read serves the MANDATES and the §18 banner, not S13-2F/2G",
          "# MANDATE 0" in text and "# MANDATE 1" in text and "# §18 — AUDIT" in text
          and "## S13-2F" not in text and "## S13-2G" not in text and "footer law" in text)
    outs_e, rc, _ = read_all("--progress", bs_path, "--escalate")
    esc = state(esc=True)
    eserved = {(c["file"], j) for c in esc["chunks"] for j in range(c["start"], c["end"] + 1)}
    check("escalation serves exactly the complement, as its own read",
          rc == 0 and esc["read_id"] != nf["read_id"] and not (eserved & served)
          and eserved | served == {(f, j) for f in route for j in range(1, sec["files"][f]["lines"] + 1)}
          and "## S13-2F" in bodies(outs_e) and "# MANDATE 0" not in bodies(outs_e))
    rc, out = run(fx, "--retention", codes(esc), "--escalate", "--when", "before-final")
    check("escalation retention checks the escalation read",
          rc == 0 and esc["read_id"] in out and "[before-final]" in out)
    os.remove(bs_path)
    for f in os.listdir(os.path.join(fx, READ_STATE_DIR)):
        if f.startswith("current_session"):
            os.remove(os.path.join(fx, READ_STATE_DIR, f))
    rc, out = run(fx, "--trigger", "TestCreate", "--read", "1", "--escalate")
    check("escalation without a session read is refused (exit 2), never 'nothing to read'",
          rc == 2 and "no session read" in out and "nothing to read" not in out)
    run(fx, "--trigger", "TestCreate", "--read", "1")
    rc, out = run(fx, "--trigger", "TestCreate", "--read", "1", "--escalate")
    check("escalation from a FINAL session reads nothing",
          rc == 0 and "ESCALATION: nothing to read" in out)

    # orchestrator role: only the orchestrator spec, whole
    outs, rc, _ = read_all("--role", "orchestrator")
    check("orchestrator role reads only the orchestrator spec",
          rc == 0 and bodies(outs) == files["Framework_MockTestOrchestrate.md"]
          and {c["file"] for c in state("orchestrator")["chunks"]}
          == {"Framework_MockTestOrchestrate.md"})
    o_st = state("orchestrator")
    rc, out = run(fx, "--retention", codes(o_st), "--role", "orchestrator")
    check("orchestrator retention without --trigger checks the orchestrator read",
          rc == 0 and f"RETENTION: PASS {o_st['read_id']}" in out)
    rc, out = run(fx, "--retention", "01=BBBBBBB", "--role", "orchestrator")
    check("orchestrator retention FAIL names the orchestrator re-read",
          rc == 3 and "--role orchestrator --read 1" in out)
    rc, out = run(fx, "--trigger", "PYQScan", "--role", "orchestrator", "--read", "1")
    check("orchestrator role refuses a trigger that is not orchestrated", rc == 2)

    # D2-D4 staging
    att = os.path.join(tmp, "attach", "sess1")
    os.makedirs(att)
    with open(os.path.join(att, "0a1b2c3d-My_Notes.json"), "w", encoding="utf-8") as fh:
        fh.write('{"a": 1}')
    up = env["FW_UPLOADS_DIR"]
    os.makedirs(up)
    with open(os.path.join(up, "My_Notes.json"), "w", encoding="utf-8") as fh:
        fh.write("stale")
    os.chmod(os.path.join(up, "My_Notes.json"), 0o444)
    rc, out = run(fx, "--stage-inputs")
    check("stage-inputs strips the 8-hex prefix and replaces a read-only target",
          rc == 0 and "STAGED ATTACHMENT My_Notes.json 8 B" in out
          and open(os.path.join(up, "My_Notes.json"), encoding="utf-8").read() == '{"a": 1}')
    check("stage-inputs prints the project-doc procedure while the project dir is empty",
          "PROJECT FILES ARE NOT MOUNTED ON THIS SURFACE" in out
          and "NEXT: continue with rule 2a" in out)
    rc, out = run(fx, "--trigger", "TestCreate")
    check("D1 notice is silent once the project dir exists and attachments are staged",
          rc == 0 and "SURFACE:" not in out)
    proj = env["FW_PROJECT_DIR"]
    src = os.path.join(tmp, "Framework_X.md")
    with open(src, "w", encoding="utf-8") as fh:
        fh.write("# Framework_X v1\n")
    rc, out = run(fx, "--stage-doc", "Framework_X.md", "--from", src)
    check("stage-doc --from copies and records mode file",
          rc == 0 and out.startswith("STAGED file Framework_X.md 17 B sha256 "))
    rc, out = run(fx, "--stage-doc", "My_Notes.json", "--from", os.path.join(up, "My_Notes.json"))
    check("stage-doc from the uploads dir records mode attachment",
          rc == 0 and out.startswith("STAGED attachment My_Notes.json"))
    with open(os.path.join(proj, "cfg.json"), "w", encoding="utf-8") as fh:
        fh.write('{"ok": true}')
    rc, out = run(fx, "--stage-doc", "cfg.json", "--typed")
    check("stage-doc --typed validates in place", rc == 0 and out.startswith("STAGED typed cfg.json"))
    txd = os.path.join(fx, "tx"); os.makedirs(txd, exist_ok=True)
    big_doc = '{\n  "exam_code": "EX",\n  "v": "' + "é—x" * 9000 + '"\n}'
    lf = os.path.join(fx, "lf.txt")
    with open(lf, "w", encoding="utf-8") as fh:
        fh.write("# rules\nline two\n")
    recs = [
        {"type": "user", "message": {"content": [{"type": "tool_result", "content": [
            {"type": "text", "text": json.dumps({"method": "project_read", "path": "EX_old.json",
                                                 "content": '{"v": 1}'})}]}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "content": json.dumps(
            {"method": "project_read", "path": "EX_big.json", "content": big_doc})}]}},
        {"toolUseResult": json.dumps({"method": "project_read", "path": "EX_old.json",
                                      "content": '{"v": 2}'})},
        {"x": json.dumps({"method": "project_read", "path": "EX_rules.md", "local_file": lf,
                          "size_bytes": 18})},
        {"x": json.dumps({"method": "project_read", "path": "EX Syllabus.docx",
                          "content": "text"})},
        {"x": json.dumps({"method": "project_read", "path": "EX_bad.json", "content": "{nope"})},
    ]
    with open(os.path.join(txd, "s.jsonl"), "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r) + "\n")
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "*.jsonl")
    rc, out = run(fx, "--stage-project-docs")
    pj = env["FW_PROJECT_DIR"]
    check("stage-project-docs stages inline results byte-exact, newest wins, copies local_file, "
          "skips document uploads and reports an invalid one (exit 2)",
          rc == 2 and open(os.path.join(pj, "EX_big.json"), encoding="utf-8").read() == big_doc
          and open(os.path.join(pj, "EX_old.json")).read() == '{"v": 2}'
          and open(os.path.join(pj, "EX_rules.md")).read() == "# rules\nline two\n"
          and "SKIPPED EX Syllabus.docx" in out and "NOT STAGED: EX_bad.json" in out
          and "STAGED project-record EX_big.json" in out
          and not os.path.exists(os.path.join(pj, "EX Syllabus.docx")))
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "none", "*.jsonl")
    rc, out = run(fx, "--stage-project-docs")
    check("stage-project-docs without any record says NOT STAGED (exit 2)",
          rc == 2 and out.startswith("NOT STAGED: no project_read result"))
    for _n in ("EX_big.json", "EX_old.json", "EX_rules.md"):
        os.unlink(os.path.join(pj, _n))
    _rp = os.path.join(pj, STAGED_RECORD)
    _r = _load_json(_rp) or {}
    for _n in ("EX_big.json", "EX_old.json", "EX_rules.md"):
        _r.pop(_n, None)
    with open(_rp, "w", encoding="utf-8") as fh:
        json.dump(_r, fh, indent=2)
    with open(os.path.join(proj, "bad.json"), "w", encoding="utf-8") as fh:
        fh.write('{"ok": tru')
    rc, out = run(fx, "--stage-doc", "bad.json", "--typed")
    check("stage-doc refuses invalid JSON (exit 2, HS:INPUT)",
          rc == 2 and "HARD STOP [HS:INPUT] STAGE-INVALID bad.json: not valid JSON" in out)
    with open(os.path.join(proj, "eng.py"), "w", encoding="utf-8") as fh:
        fh.write("def f(:\n")
    rc, out = run(fx, "--stage-doc", "eng.py", "--typed")
    check("stage-doc refuses python that does not compile", rc == 2 and "does not compile" in out)
    rc, out = run(fx, "--stage-inputs")
    check("stage-inputs points at spec_source once a project spec is staged",
          "NEXT: python3 spec_source.py --resolve" in out and "PROJECT FILES ARE NOT" not in out)
    rc, out = run(fx, "--stage-status")
    check("stage-status reports STAGING COMPLETE with the typed count",
          rc == 0 and "STAGING COMPLETE — 5 file(s)" in out and "(1 typed" in out)
    env["FW_PROJECT_DIR"] = os.path.join(tmp, "empty_project")
    rc, out = run(fx, "--stage-status")
    check("stage-status on an empty project dir is STAGING-EMPTY (exit 2)",
          rc == 2 and "HARD STOP [HS:INPUT] STAGING-EMPTY" in out)
    env["FW_PROJECT_DIR"] = proj

    # Edge cases (final review 2026-11-06), in their own directories.
    keep = {k: env[k] for k in ("FW_PROJECT_DIR", "FW_UPLOADS_DIR", "FW_ATTACH_DIR")}
    e_att = os.path.join(tmp, "e_attach")
    env.update(FW_PROJECT_DIR=os.path.join(tmp, "e_project"),
               FW_UPLOADS_DIR=os.path.join(tmp, "e_uploads"), FW_ATTACH_DIR=e_att)
    os.makedirs(os.path.join(e_att, "s1")); os.makedirs(os.path.join(e_att, "s2"))
    _old = os.path.join(e_att, "s2", "ffffffff-EX_registry.json")
    _new = os.path.join(e_att, "s1", "00000000-EX_registry.json")
    with open(_old, "w", encoding="utf-8") as fh:
        fh.write('{"v": "old"}')
    with open(_new, "w", encoding="utf-8") as fh:
        fh.write('{"v": "new"}')
    os.utime(_old, (time.time() - 500, time.time() - 500))
    rc, out = run(fx, "--stage-inputs", "--trigger", "TestCreate")
    rcv, outv = run(fx, "--trigger", "PYQDraft")
    check("the newest attachment of a name wins, lands in uploads and project, and the "
          "SURFACE notice goes silent",
          rc == 0 and out.count("STAGED ATTACHMENT EX_registry.json") == 1
          and open(os.path.join(env["FW_UPLOADS_DIR"], "EX_registry.json")).read() == '{"v": "new"}'
          and open(os.path.join(env["FW_PROJECT_DIR"], "EX_registry.json")).read() == '{"v": "new"}'
          and "SURFACE:" not in outv)
    _blob = os.path.join(tmp, "blob.bin")
    with open(_blob, "wb") as fh:
        fh.write(b"PK\x03\x04\x00\xff binary")
    with open(os.path.join(txd, "e.jsonl"), "w", encoding="utf-8") as fh:
        for r in ({"x": json.dumps({"method": "project_read", "path": "EX_registry.json",
                                    "content": '{"v": "project"}'})},
                  {"x": json.dumps({"method": "project_read", "path": "EX Pattern.xlsx",
                                    "file_kind": "blob", "local_file": _blob})}):
            fh.write(json.dumps(r) + "\n")
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "e.jsonl")
    rc, out = run(fx, "--stage-project-docs")
    check("stage-project-docs never replaces an attached file and stages a blob byte for byte",
          rc == 0 and "KEPT ATTACHMENT EX_registry.json" in out
          and open(os.path.join(env["FW_PROJECT_DIR"], "EX_registry.json")).read() == '{"v": "new"}'
          and open(os.path.join(env["FW_PROJECT_DIR"], "EX Pattern.xlsx"), "rb").read()
          == open(_blob, "rb").read())
    with open(os.path.join(e_att, "s1", "11111111-EX_cfg.json"), "w", encoding="utf-8") as fh:
        fh.write('{"cut": ')
    rc, out = run(fx, "--stage-inputs")
    check("an attached JSON that does not parse stops staging (exit 2)",
          rc == 2 and "STAGE-INVALID EX_cfg.json" in out and "STAGING STOPPED" in out
          and "NEXT:" not in out)
    env.update(keep)
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "none", "*.jsonl")

    # Blind-review fixes (2026-11-06).
    rc, out = run(fx, "--stage-doc", "../escape.md", "--from", src)
    check("stage-doc refuses a name that is a path",
          rc == 2 and "plain file name" in out
          and not os.path.exists(os.path.join(os.path.dirname(proj), "escape.md")))
    with open(os.path.join(txd, "p.jsonl"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"x": json.dumps({"method": "project_read", "path": "dir/",
                                              "content": "T"})}) + "\n")
        fh.write(json.dumps({"x": json.dumps({"method": "project_read", "path": "EX_ok.md",
                                              "content": "ok\n"})}) + "\n")
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "p.jsonl")
    rc, out = run(fx, "--stage-project-docs")
    check("stage-project-docs survives a path that is not a file name and leaves no temp file",
          rc == 2 and "not a file name" in out and "STAGED project-record EX_ok.md" in out
          and not [f for f in os.listdir(proj) if f.startswith(".incoming_")])
    with open(os.path.join(proj, STAGED_RECORD), "w", encoding="utf-8") as fh:
        fh.write("{oops")
    rc, out = run(fx, "--stage-project-docs")
    rc2, out2 = run(fx, "--stage-inputs")
    check("a corrupt staging record stops project staging and is rebuilt by stage-inputs",
          rc == 2 and "STAGE-RECORD" in out and rc2 == 0 and "has been rebuilt" in out2
          and (_load_json(os.path.join(proj, STAGED_RECORD)) or {}).get(
              "My_Notes.json", {}).get("mode") == "attachment")
    os.remove(os.path.join(proj, "EX_ok.md"))
    env["FW_TRANSCRIPT_GLOB"] = os.path.join(txd, "none", "*.jsonl")
    run(fx, "--trigger", "TestCreate")
    with open(os.path.join(fx, "Framework_Footer.md"), "a", encoding="utf-8") as fh:
        fh.write("x\n")
    rc, out = run(fx, "--trigger", "TestCreate")
    rc2, out2 = run(fx, "--trigger", "TestCreate", "--read", "1")
    check("a failed verify removes .verified, so no read is served afterwards",
          rc == 1 and rc2 == 1 and "no .verified" in out2
          and not os.path.exists(os.path.join(fx, ".verified")))
    with open(os.path.join(fx, "Framework_Footer.md"), "w", encoding="utf-8") as fh:
        fh.write(files["Framework_Footer.md"])
    run(fx, "--trigger", "TestCreate")
    orch_st = None
    run(fx, "--trigger", "TestCreate", "--role", "orchestrator", "--read", "1")
    orch_st = json.load(open(os.path.join(fx, READ_STATE_DIR, open(os.path.join(
        fx, READ_STATE_DIR, "current_orchestrator")).read().strip() + ".json")))
    _a1 = orch_st["anchors"]["01"]
    rc, out = run(fx, "--role", "orchestrator", "--retention", "1" + "01=" + _a1)
    rc2, out2 = run(fx, "--role", "orchestrator", "--retention", "01=BBBBBBB 01=" + _a1)
    rc3, out3 = run(fx, "--role", "orchestrator", "--retention", "01=" + _a1)
    check("retention ignores a code glued to other digits and refuses two different codes "
          "for one anchor", rc == 3 and rc2 == 3 and rc3 == 0)

    # A reader that closes the pipe early never produces a traceback, and the command
    # still does its work (here: .verified is written).
    if os.path.exists(os.path.join(fx, ".verified")):
        os.remove(os.path.join(fx, ".verified"))
    rp = subprocess.run(f'"{sys.executable}" "{os.path.join(here, "bootstrap.py")}" '
                        f'--trigger TestCreate | head -1', shell=True, cwd=fx, env=env,
                        capture_output=True, text=True)
    check("output cut by `| head` gives no traceback and the verify still completes",
          "Traceback" not in rp.stderr and "BrokenPipe" not in rp.stderr
          and rp.stdout.startswith("[OK] FRAMEWORK")
          and os.path.exists(os.path.join(fx, ".verified")))

    # D9/D10 worker hand-off
    chat = os.path.join(tmp, "chat.txt")
    with open(chat, "w", encoding="utf-8") as fh:
        fh.write("Batch 1 delivered.\n")
    common = ["--worker-report", "write", "--exam", "EX", "--paper", "2", "--batch", "1",
              "--of", "4", "--chat-file", chat]
    rc, out = run(fx, *common, "--state", "BATCH_DELIVERED", "--files", src + ",/nope/x.docx")
    check("worker-report refuses a listed file that does not exist", rc == 2)
    rc, out = run(fx, *common, "--state", "DONE", "--files", src)
    check("worker-report refuses a state outside the closed set", rc == 2)
    comma = os.path.join(tmp, "EX_SUBJ_Reasoning, General Intelligence_01_Q1to10.docx")
    with open(comma, "w", encoding="utf-8") as fh:
        fh.write("docx")
    rc, out = run(fx, "--worker-report", "write", "--exam", "EXC", "--paper", "1", "--batch",
                  "1", "--of", "2", "--chat-file", chat, "--state", "BATCH_DELIVERED",
                  "--files", comma + ", " + src)
    rcs, outs = run(fx, "--worker-report", "show", "--exam", "EXC", "--paper", "1")
    check("worker-report keeps a file name that holds a comma whole",
          rc == 0 and rcs == 0 and f"  {comma}  (4 B)" in outs and f"  {src}  (17 B)" in outs)
    big = os.path.join(tmp, "big.txt")
    with open(big, "w", encoding="utf-8") as fh:
        fh.write("x\n" * 801)
    rc, out = run(fx, *(common[:-1] + [big]), "--state", "BATCH_DELIVERED", "--files", src)
    with open(big, "w", encoding="utf-8") as fh:
        fh.write("x\n" * 800)
    rc2, out2 = run(fx, "--worker-report", "write", "--exam", "EX800", "--paper", "1",
                    "--batch", "1", "--of", "1", "--chat-file", big,
                    "--state", "BATCH_DELIVERED", "--files", src)
    with open(big, "w", encoding="utf-8") as fh:
        fh.write(("y" * 99 + "\n") * 600 + "z\n")
    rc3, out3 = run(fx, *(common[:-1] + [big]), "--state", "BATCH_DELIVERED", "--files", src)
    check("worker-report refuses a chat block over 800 lines or 60,000 B and accepts exactly 800",
          rc == 2 and rc2 == 0 and rc3 == 2)
    rc_all = [run(fx, "--worker-report", "write", "--exam", "EXF", "--paper", "1", "--batch",
                  "0", "--of", "0", "--chat-file", chat, "--state", s_, "--files", "",
                  *(["--review-parts", tmp] if s_ in WORKER_STATES_NEED_PARTS else []))[0]
              for s_ in WORKER_STATES]
    rc_m = run(fx, "--worker-report", "write", "--state", "BATCH_DELIVERED", "--files", "",
               "--chat-file", chat)[0]
    rc_r = run(fx, "--worker-report", "write", "--exam", "EXF", "--paper", "1", "--batch", "5",
               "--of", "5", "--chat-file", chat, "--state", "REVIEW_REQUEST", "--files", "")[0]
    rc_g = run(fx, "--worker-report", "write", "--exam", "EXF", "--paper", "1", "--batch", "2",
               "--of", "5", "--chat-file", chat, "--state", "GRADE_REQUEST", "--files", "")[0]
    check("worker-report refuses missing --exam/--paper/--batch/--of and a REVIEW_REQUEST / GRADE_REQUEST "
          "without job folders", rc_m == 2 and rc_r == 2 and rc_g == 2)
    rc_g2, _ = run(fx, "--worker-report", "write", "--exam", "EXF", "--paper", "1", "--batch", "2",
                   "--of", "5", "--chat-file", chat, "--state", "GRADE_REQUEST", "--files", "",
                   "--review-parts", tmp)
    rc_gs, out_gs = run(fx, "--worker-report", "show", "--exam", "EXF", "--paper", "1")
    check("worker-report GRADE_REQUEST shows its job folders",
          rc_g2 == 0 and rc_gs == 0 and ("GRADE JOBS: " + tmp) in out_gs)
    rc_rt, _ = run(fx, "--worker-report", "write", "--exam", "EXF", "--paper", "1", "--batch", "2",
                   "--of", "5", "--chat-file", chat, "--state", "ROTATE", "--files", "")
    rc_rs, out_rs = run(fx, "--worker-report", "show", "--exam", "EXF", "--paper", "1")
    check("worker-report ROTATE prints the BATCH STATE progress sha", rc_rt == 0 and rc_rs == 0 and "PROGRESS: " in out_rs)
    # 2026.11.12 GAP-2026-11-12-HANDOVER-CHECKPOINT: a planned handover refreshes the checkpoint — the next
    # worker's restore keeps the batch in work; a failed worker's work since the last make is undone
    _h = env["FW_HOME"]
    env["FW_OUTPUTS"] = os.path.join(tmp, "outputs")
    os.makedirs(_h, exist_ok=True); os.makedirs(env["FW_OUTPUTS"], exist_ok=True)
    def _w(n, t):
        open(os.path.join(_h, n), "w").write(t)
    _w("CKX_M1_answer_key.json", "pre-batch"); _w("CKX_M1_batch_state.json", "b0")
    rc_c1, _ = run(fx, "--checkpoint", "make", "--exam", "CKX", "--paper", "1")             # (b) passed
    _w("CKX_M1_answer_key.json", "10 questions + grades"); _w("CKX_M1_batch_state.json", "b1-verifying")
    _w("q3_problem.png", "fig")
    rc_c2, _ = run(fx, "--checkpoint", "make", "--exam", "CKX", "--paper", "1")             # planned handover
    rc_c3, out_c3 = run(fx, "--checkpoint", "restore", "--exam", "CKX", "--paper", "1")     # the fresh worker
    kept = open(os.path.join(_h, "CKX_M1_answer_key.json")).read() == "10 questions + grades" \
        and os.path.exists(os.path.join(_h, "q3_problem.png"))
    rc_c4, _ = run(fx, "--checkpoint", "make", "--exam", "CKX", "--paper", "1")
    _w("CKX_M1_answer_key.json", "unproven work"); _w("CKX_stray.json", "x")
    rc_c5, _ = run(fx, "--checkpoint", "restore", "--exam", "CKX", "--paper", "1")         # after a RETENTION_FAIL
    undone = open(os.path.join(_h, "CKX_M1_answer_key.json")).read() == "10 questions + grades" \
        and not os.path.exists(os.path.join(_h, "CKX_stray.json"))
    rc_c6, out_c6 = run(fx, "--checkpoint", "status", "--exam", "CKX", "--paper", "1")
    check("checkpoint: a planned handover keeps the batch in work; a failed worker's unproven work is undone",
          (rc_c1, rc_c2, rc_c3, rc_c4, rc_c5, rc_c6) == (0, 0, 0, 0, 0, 0) and kept and undone
          and "RESTORED" in out_c3 and "none" in out_c6)
    rc_h, out_h = run(fx, "--retention", "01=XXXX", "--when", "handover")
    check("retention accepts --when handover", "invalid choice" not in out_h and "RETENTION" in out_h)
    check("worker-report accepts --files \"\" (no files) for every state",
          rc_all == [0] * len(WORKER_STATES))
    empty = os.path.join(tmp, "empty.txt")
    open(empty, "w").close()
    rc, out = run(fx, *(common[:-1] + [empty]), "--state", "PAPER_DELIVERED", "--files", src)
    check("worker-report refuses an empty chat block for PAPER_DELIVERED", rc == 2)
    rc, out = run(fx, "--worker-report", "show", "--exam", "EX", "--paper", "2")
    check("worker-report show without a report is WORKER-REPORT-MISSING (exit 2)",
          rc == 2 and "HARD STOP [HS:INFRA] WORKER-REPORT-MISSING" in out)
    rc, out = run(fx, *common, "--state", "BATCH_DELIVERED", "--files", src)
    rc2, out2 = run(fx, "--worker-report", "show", "--exam", "EX", "--paper", "2")
    check("worker-report show prints the files and the chat block verbatim",
          rc == 0 and rc2 == 0
          and out2.startswith("WORKER REPORT EX M2 — STATE BATCH_DELIVERED — batch 1 of 4")
          and f"  {src}  (17 B)" in out2
          and "-----\nBatch 1 delivered.\n----- END CHAT BLOCK part 1 of 1 -----" in out2)
    os.utime(src, (time.time() + 60, time.time() + 60))
    rc, out = run(fx, "--worker-report", "show", "--exam", "EX", "--paper", "2")
    check("worker-report show refuses a report older than a file it lists", rc == 2)
    gone = os.path.join(tmp, "gone.docx")
    with open(gone, "w", encoding="utf-8") as fh:
        fh.write("v1")
    run(fx, "--worker-report", "write", "--exam", "EXG", "--paper", "1", "--batch", "1", "--of",
        "2", "--chat-file", chat, "--state", "BATCH_DELIVERED", "--files", gone)
    os.utime(gone, (time.time() - 100, time.time() - 100))
    with open(gone, "w", encoding="utf-8") as fh:
        fh.write("v2")
    os.utime(gone, (time.time() - 100, time.time() - 100))
    rc, out = run(fx, "--worker-report", "show", "--exam", "EXG", "--paper", "1")
    os.remove(gone)
    rc2, out2 = run(fx, "--worker-report", "show", "--exam", "EXG", "--paper", "1")
    check("worker-report show refuses a listed file that changed or is gone (WORKER-REPORT-STALE)",
          rc == 2 and "WORKER-REPORT-STALE" in out and rc2 == 2 and "WORKER-REPORT-STALE" in out2)
    big = os.path.join(fx, "big_block.md")
    with open(big, "w", encoding="utf-8") as fh:
        fh.write("".join(f"line {i:04d} " + "x" * 90 + "\n" for i in range(500)))
    run(fx, "--worker-report", "write", "--exam", "EXP", "--paper", "1", "--batch", "1",
        "--of", "2", "--state", "BATCH_DELIVERED", "--files", "", "--chat-file", big)
    got, k, n_parts, ok_sz = "", 1, None, True
    while True:
        rc, out = run(fx, "--worker-report", "show", "--exam", "EXP", "--paper", "1",
                      "--part", str(k))
        m = re.search(r"----- CHAT BLOCK part (\d+) of (\d+)", out)
        if rc != 0 or not m:
            break
        n_parts = int(m.group(2))
        body = out.split(" -----\n", 1)[1].split("----- END CHAT BLOCK part", 1)[0]
        got += body
        ok_sz = ok_sz and len(out) < 40000
        if k >= n_parts:
            break
        k += 1
    check("worker-report show serves a large chat block in inline-sized parts that join exactly",
          n_parts is not None and n_parts > 1 and ok_sz and got == open(big, encoding="utf-8").read())
    rc, out = run(fx, "--worker-report", "show", "--exam", "EXP", "--paper", "1", "--part", "99")
    check("worker-report show refuses a part that does not exist", rc == 2)
    rc, out = run(fx, "--worker-prompt", "--trigger-text", "TestCreate EX M2")
    check("worker prompt carries the trigger and the fixed worker rules",
          rc == 0 and "TestCreate EX M2" in out and "do NOT re-run Step 0" in out
          and "do NOT\ndelete /tmp/fw" in out and "--worker-report write" in out
          and out.rstrip().endswith("WORKER DONE <STATE> batch K of M")
          and len(out.splitlines()) < 64)   # 2026.11.13: +2 lines (the PYTHON SESSION rule)
    check("worker prompt names Orchestrate PART B, the read, retention and O2-2 messages",
          "Framework_MockTestOrchestrate.md\nPART B (O3-1 to O3-8)" in out
          and "python3 bootstrap.py --trigger <T> --progress <BATCH STATE> --read K" in out
          and 'python3 bootstrap.py --retention "<nn>=<code> ..." --when <W>' in out
          and "after a blank line at\nthe end of this prompt" in out
          and all(m in out for m in ("continue — delivery confirmed", "FINAL ASSEMBLY",
                                     "REVIEW RETURNED", "USER MESSAGE: <the user's message, verbatim>")))
    rc, out = run(fx, "--worker-prompt", "--trigger-text", "TestCreate EX M2", "--continue")
    check("--continue prompt makes a fresh worker read, restore and apply S4-6",
          rc == 0 and "read (O3-2) and prove (a) first" in out and "RESTORE" in out
          and "S4-6" in out and len(out.splitlines()) < 64)   # 2026.11.13: +2 lines (PYTHON SESSION)

    # E: an overlay with a project spec carries a regenerated map that verifies
    import spec_source
    shutil.copy(os.path.join(here, "spec_sections.py"), fx)
    pj = os.path.join(tmp, "pj")
    os.makedirs(pj)
    with open(os.path.join(pj, "Framework_Footer.md"), "w", encoding="utf-8") as fh:
        fh.write("# Framework_Footer v1.1\n## F-1 — footer\nnew footer\nmore\n"
                 "# END OF Framework_Footer v1.1\n")
    ov = os.path.join(tmp, "overlay")
    spec_source.resolve(fx, pj, ov)
    rc, out = run(ov, "--trigger", "TestCreate")
    check("overlay with a regenerated map verifies (PARTIALLY, REGENERATED listed)",
          rc == 0 and "[REGENERATED] SPEC_SECTIONS.json" in out)
    with open(os.path.join(ov, "SPEC_SECTIONS.json"), "a", encoding="utf-8") as fh:
        fh.write(" ")
    rc, out = run(ov, "--trigger", "TestCreate")
    check("a tampered regenerated map is a HARD STOP", rc == 1 and "HARD STOP" in out)

    # session class unchanged for the existing cases
    def sc(trigger, obj):
        p = None
        if obj is not None:
            p = os.path.join(tmp, "prog.json")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(obj if isinstance(obj, str) else json.dumps(obj))
        return _session_class(p, {}, trigger=trigger)
    plan3 = [{"batch_id": b} for b in ("B1", "B2", "B3")]
    table = [
        ("MockExplain", None, "FINAL"), ("TestExplain", None, "FINAL"),
        ("PYQDraft", None, "FINAL"), ("PYQApprove", None, "FINAL"),
        ("MockBlueprint", None, "FINAL"),
        ("MockBlueprint", {"mocks": [1], "total_mocks": 3}, "NON-FINAL"),
        ("MockBlueprint", {"mocks": [1, 2, 3], "total_mocks": 3}, "FINAL"),
        ("MockBlueprint", "{bad", "FINAL"),
        ("TestCreate", None, "FINAL"),
        ("MockCreate", {"batch_plan": plan3, "batches_completed": [], "current_batch": "B1"},
         "NON-FINAL"),
        ("MockCreate", {"batch_plan": plan3, "batches_completed": ["B1", "B2"],
                        "current_batch": "B3"}, "FINAL"),
        ("MockCreate", {"batch_plan": [{"batch_id": "B1"}, {"batch_id": "B2", "is_final": True},
                                       {"batch_id": "B3"}],
                        "batches_completed": ["B1"], "current_batch": "B2"}, "FINAL"),
        ("MockCreate", {"no_plan": 1}, "FINAL"),
        ("PYQExtract", None, "NON-FINAL"),
        ("PYQExtract", {"_meta": {"papers_processed": [1], "total_papers": 10}}, "NON-FINAL"),
        ("PYQExtract", {"_meta": {"papers_processed": [1, 2], "total_papers": 5}}, "FINAL"),
        ("PYQExtract", "{bad", "FINAL"),
    ]
    got = [(t, sc(t, o)) for t, o, _ in table]
    check("session class unchanged for every existing case",
          got == [(t, want) for t, _, want in table])

    shutil.rmtree(tmp, ignore_errors=True)
    # 2026.11.13 — the python session (--session-start / --run-block)
    _ns_ok, _ns_bad = ns_self_test()
    for _n in _ns_ok:
        check("NS " + _n, True)
    for _n in _ns_bad:
        check("NS " + _n, False)
    rc_ns = subprocess.run([sys.executable, os.path.abspath(__file__), "--session-start", "--exam", "EX"],
                           capture_output=True, text=True).returncode
    check("NS --session-start without --paper is refused (exit 2)", rc_ns == 2)
    print(f"SELF-TEST: {passed}/{passed + len(fails)} PASS")
    if fails:
        print("FAILED: " + "; ".join(fails))
    return not fails


class _PipeSafe:
    """A reader that closes the pipe early (`bootstrap.py ... | head -5`) must not turn a
    finished or half-finished command into a Python traceback: the work goes on, the rest of
    the output is dropped."""
    def __init__(self, stream):
        self._s = stream

    def _drop(self):
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), self._s.fileno())
        except (OSError, ValueError):
            pass

    def write(self, text):
        try:
            return self._s.write(text)
        except BrokenPipeError:
            self._drop()
            return len(text)

    def flush(self):
        try:
            self._s.flush()
        except BrokenPipeError:
            self._drop()

    def __getattr__(self, name):
        return getattr(self._s, name)


if __name__ == "__main__":
    sys.stdout = _PipeSafe(sys.stdout)
    try:
        main()
    finally:
        sys.stdout.flush()
