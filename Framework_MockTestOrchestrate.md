# Framework_MockTestOrchestrate v1.3.0
# v1.3.0 — 2026-11-11 — GAP-2026-11-11-BATCH-VERIFICATION (owner 2026-11-11; paired with Framework_MockTestCreate
#   v6.1, blueprint_core v2.1 Cluster BV, bootstrap GRADE_REQUEST / ROTATE). Every question is measured by fresh
#   blind graders and solvers INSIDE ITS OWN BATCH: NEW worker state GRADE_REQUEST and orchestrator message
#   GRADE RETURNED (O2-3, O3-9) — the in-batch controls of O-GRADE now have a path (v1.2.0 named them but no
#   worker could request them, so the first fresh measurement happened at Final Assembly). NEW state ROTATE: a
#   worker short of room saves and is replaced by a fresh worker on the same message — never a HARD STOP for
#   room. Entry v1.2.0 moved to SPEC_HISTORY.md.

## O0-1 — Why this spec exists

The Step 7 route (Framework_MockTestCreate.md, Framework_MockReview.md, Framework_DeliveryFooter.md,
this spec) is read before the first question is written; `audit_specs_ext` SPEC-CAPACITY computes its
size from SESSION_BUDGET.json `bytes_per_token` (currently about 400,000 tokens for a FINAL read).
SESSION_BUDGET.json `_measured` records what a session holds: a large model held the whole route and
answered every read-back check; a context that keeps growing is summarised by the platform without
notice (compaction), after which the session works from a summary of the specification, not from its
text. Two controls follow: (1) READ-RETENTION — every read is proved
present at fixed points (O3-3); (2) WORKER MODE — the paper is written by worker sub-agents whose size
the orchestrator sees and replaces before compaction; the user's chat stays small for any paper size
and the run finishes in the chat where it started (owner requirement R-ONE, OD-2026-11-06).

## O0-2 — Scope, precedence and names

Framework_MockTestCreate.md (MTC) remains the law of Step 7: every question-writing rule, gate,
artefact, deliverable, end state and user action is MTC's and STEP_CONTRACTS.json's. This spec decides
only who executes MTC and how its text is read. MTC S1-0R hands three sites to this spec: the read
method (O3-2, O3-3), the delivery proxy (O3-4) and the review hand-over (O3-6). Everywhere else MTC wins.
Names: <T> = the trigger (MockCreate or TestCreate). <E> = the exam code and <N> = the paper number, as
in MTC's file names ([ExamCode], [N]). BATCH STATE = /home/claude/<E>_M<N>_batch_state.json. CHAT
BLOCK FILE = /home/claude/<E>_M<N>_chat_block.md. CHECKPOINT = the folder
/home/claude/<E>_M<N>_checkpoint. SESSION_BUDGET.json = the file in /tmp/fw_effective.
ORCHESTRATOR = the user's chat in WORKER MODE. WORKER = a sub-agent that is the Step 7 session of MTC.

## O1-1 — Which mode this chat is in (decided once per run)

Decide after Step 0 passed and, when bootstrap printed SURFACE, after
`python3 bootstrap.py --stage-status` printed STAGING COMPLETE:
- WORKER MODE: this chat has a tool that starts a sub-agent in a fresh context (for example a tool
  named Agent or Task). This chat is the ORCHESTRATOR (PART A). Starting worker and reviewer
  sub-agents for Step 7 is authorised by the owner (OD-2026-11-06) as part of the standing instruction
  behind every MockCreate / TestCreate trigger. Do not ask the user.
- DIRECT MODE: this chat has no such tool, or the tool refuses or fails to start the first worker of
  the run. This chat is the Step 7 session itself (O5-1).
Print one line in chat: `STEP 7 MODE: WORKER` or `STEP 7 MODE: DIRECT (<reason>)`; when the first
worker cannot be started, print the DIRECT line with the tool's reason. DIRECT MODE lasts to run end.

## O2-1 — PART A: ORCHESTRATOR LAW — what the orchestrator reads and does

The orchestrator reads this spec only:
`python3 bootstrap.py --trigger <T> --role orchestrator --read K` for K = 1..N, one call each, in
order, then proves it from memory with
`python3 bootstrap.py --retention "<nn>=<code> ..." --role orchestrator`.
At the start of every response to a user message it re-proves that read with the same command; on
FAIL, or when bootstrap answers that there is no current orchestrator read, it reads this spec again
(one `--role orchestrator --read K` series, K = 1..N) and proves it before doing anything else —
nothing is lost: its state is the worker reports on disk.
A RUN is one paper: it starts with a MockCreate / TestCreate trigger message and ends with
PAPER_DELIVERED or a printed HARD STOP. Step 0 runs ONCE per run. A later user message of the same
run (a continue trigger included) never runs Step 0 again: rebuilding /tmp/fw_effective deletes the
read state the current worker proves its read against. The exceptions are O2-7 and O2-8.
Besides that it reads only bootstrap output, SESSION_BUDGET.json and worker reports. It never reads
Framework_MockTestCreate.md, Framework_MockReview.md or Framework_DeliveryFooter.md; never opens the
paper, a sidecar, the registry, the BATCH STATE, a review folder or a verdict file; never authors,
repairs or checks a question; never prints question content (MTC MANDATE 0 binds the whole run).
Before the first worker, in this order: Step 0 passed in this chat; STAGING COMPLETE was printed when
bootstrap printed SURFACE; this spec was read in full and its retention check printed `RETENTION: PASS`.

## O2-2 — Starting a worker

Prompt = the verbatim output of
`python3 bootstrap.py --worker-prompt --trigger-text "<TRIGGER>"`
where <TRIGGER> is the user's message that started this run, verbatim, as one shell argument.
- Until a worker of this run has reported BATCH_DELIVERED, every worker (the first one and any
  replacement for it) gets this prompt as printed and no message: its prompt carries the trigger.
- After that, every new worker gets the prompt printed with `--continue` added and, after a blank
  line at the end of the prompt, the ORCHESTRATOR MESSAGE it is to handle (the message the replaced
  worker was handling, or the new one).
ORCHESTRATOR MESSAGES (closed set; each is sent exactly as written):
- `continue — delivery confirmed` — the user typed a continue trigger after BATCH_DELIVERED (O2-6).
- `FINAL ASSEMBLY` — after FINAL_BATCH_BUILT.
- `REVIEW RETURNED` followed by one line per part (O2-3).
- `GRADE RETURNED` followed by one line per job folder (O2-3, v1.3.0).
- `USER MESSAGE: <the user's message, verbatim>` (O2-6).
Model: the first entry of SESSION_BUDGET.json `worker_models` that the tool accepts and that O2-3 has
not ruled out for this run; a tool with no model choice uses its default. One worker at a time, in the foreground when the tool offers it; wait
until it finishes. A message to an existing worker is sent with the tool that resumes a sub-agent
(for example one named SendMessage).

## O2-3 — Acting on a worker report

A worker's turn ends with the single line `WORKER DONE <STATE> batch K of M`. Read <E> and <N> once
per run from the newest file name listed by `ls -t /home/claude/*_worker_report.json`
(`<E>_M<N>_worker_report.json`). Then run
`python3 bootstrap.py --worker-report show --exam <E> --paper <N>`
(when its output ends with a `MORE:` line the CHAT BLOCK has several parts: run the same command
with `--part 2`, `--part 3`, ... until no `MORE:` line follows; the CHAT BLOCK is those parts joined
in order). The first line bootstrap prints (`WORKER REPORT <E> M<N> — STATE <STATE> — batch K of M`)
must carry the same STATE, K and M as the worker's final line; a difference means the report on disk
is an earlier turn's and is handled as a turn that ended without that line (below). Act on STATE:
- BATCH_DELIVERED — when FILES TO DELIVER lists files, deliver them in ONE call of this chat's
  file-delivery tool (present_files, or the name this surface gives it), in the listed order. Then
  print the CHAT BLOCK verbatim as the last element of the response and END the response.
- FINAL_BATCH_BUILT — when FILES TO DELIVER lists files, deliver them in ONE call. Print nothing and
  do not end the response: send `FINAL ASSEMBLY` at once (O2-5 picks the worker). This is MTC's one
  auto-advance (S4-9); the user sees one response.
- REVIEW_REQUEST — for each directory in REVIEW PARTS start one reviewer sub-agent whose prompt is the
  content of `<part_dir>/REVIEWER_BRIEF.txt` (print it with `cat`; the only file under /home/claude
  the orchestrator opens) and nothing else. Start several at once when the tool allows it, otherwise
  one after another; foreground; model as in O2-2. Each reviewer returns one line; a reviewer that
  errors or returns nothing counts as `REVIEW FAILED <error text>`. Retry no reviewer: the worker
  decides retries (O3-6). Then send the worker `REVIEW RETURNED` followed by one line per part:
  `<part_dir> <the reviewer's line>`.
- PAPER_DELIVERED — deliver the listed files in ONE call, in the listed order; print the CHAT BLOCK
  verbatim; END. The run is complete.
- GRADE_REQUEST (v1.3.0) — the worker is writing a batch and needs its fresh blind graders / solvers (MTC
  S4-7 STEP A2). For each directory in GRADE JOBS start one sub-agent whose prompt is the content of
  `<job_dir>/JOB_BRIEF.txt` (print it with `cat`) and nothing else — never the paper, the plan or a band. Start
  them all at once when the tool allows it (they are independent), otherwise one after another; foreground;
  model as in O2-2 (a different model from the worker when the platform offers one). Each returns one line; an
  error or no answer counts as `JOB FAILED <error text>` (a job folder ending in vision_<i>_<k> is a fresh vision read
  of one rendered figure; its brief says so). Retry none: the worker decides. Then send
  `GRADE RETURNED` followed by one line per job: `<job_dir> <the sub-agent's line>` — to the SAME worker when
  O2-5 allows it, otherwise to a fresh worker (the batch's state is on disk). Print nothing; do not end the
  response: the batch is not delivered until the worker reports BATCH_DELIVERED.
- ROTATE (v1.3.0) — the worker's room is short and its progress is saved. Start a fresh worker (O2-2,
  `--continue`) with the ORCHESTRATOR MESSAGE the rotating worker was handling. Print nothing; never a stop. A
  worker that reports ROTATE twice in a row with the same `PROGRESS:` line (bootstrap prints the BATCH STATE's
  sha256 for a ROTATE report — no progress between them) is handled as RETENTION_FAIL.
- RETENTION_FAIL — retire that worker (never message it again) and start a fresh worker (O2-2) with
  the message the retired worker was handling. When two fresh workers in a row report RETENTION_FAIL,
  that model is ruled out for this run: continue with the next entry of `worker_models` (O2-2). When
  no entry is left (or the tool offers no model choice), print this line and END:
  `HARD STOP [HS:INFRA] MODEL-CAPACITY — no model available to the workers can hold the Step 7 specification (SESSION_BUDGET.json worker_models). Run this paper in an account whose sub-agents can use one of those models. Nothing was lost: on continue the paper resumes from its saved state.`
- HARD_STOP — deliver nothing; print the CHAT BLOCK verbatim; END.
When the turn ends without that line, or `--worker-report show` exits non-zero: send the same worker
once the sentence `Write your worker report now.` (a repair request, not an ORCHESTRATOR MESSAGE); if
that fails, start a fresh worker (O2-2) with the ORCHESTRATOR MESSAGE the failed worker was handling;
if that fails too, print this line and END:
`HARD STOP [HS:INFRA] WORKER-FAILED — <what bootstrap printed>`

## O2-4 — Delivery failure

When the delivery tool has not returned a listed file after one retry of the same call, print the CHAT
BLOCK with one added line `❌ NOT DELIVERED — <file name> (<reason>)` directly above the footer's
first band line, and never claim that file was delivered. The file stays in /mnt/user-data/outputs;
on the user's next message, deliver the undelivered file(s) again in ONE call before anything else.
Framework_DeliveryFooter.md is the law for footers; the worker composed the footer.

## O2-5 — Reusing a worker or starting a fresh one (decided by numbers)

`FINAL ASSEMBLY` and `REVIEW RETURNED` always go to a fresh worker (O2-2): Final Assembly, a repair
round and the sweep after it need more room than a worker that has already written batches has left.
`GRADE RETURNED` goes to the worker that requested it while conditions 1, 2 and 4 below hold (it holds the
batch); otherwise to a fresh worker, which resumes the batch from disk (O3-9).
`continue — delivery confirmed` and `USER MESSAGE: ...` are sent to the current worker only when ALL
of these hold:
1. the tool can still resume it;
2. W + R <= SESSION_BUDGET.json `rotate_tokens`, where W = the total tokens the platform last reported
   for this worker and R = `work_unit_tokens`; when the platform reports no token count, this
   condition is instead: it has completed at most 1 batch;
3. it has completed fewer than `max_batches_per_worker` batches (a batch counts when one of its
   reports shows a K higher than the K of the report before it);
4. its last report is not RETENTION_FAIL or HARD_STOP.
Otherwise start a fresh worker (O2-2) with the message: the paper's state is on disk and the worker
resumes it (O3-7).

## O2-6 — The user's messages

The accepted continue triggers are MTC S4-6's, compared case-insensitively after trimming: "continue",
"go", "next", "continue.", "go ahead", "next batch", "proceed".
- A continue trigger when the last worker report is BATCH_DELIVERED: send
  `continue — delivery confirmed` (O2-5).
- After PAPER_DELIVERED the run is over. First re-deliver any file O2-4 still owes. Then: a message
  that is itself a MockCreate / TestCreate trigger starts a NEW run (Step 0, O1-1, O2-1, a first
  worker); to any other message answer in one sentence that Step 7 is complete for this paper,
  start no worker, generate nothing (MTC S4-6). The same holds after a printed HARD STOP that this
  spec says ends the run (WORKDIR-LOST, O2-7).
- A continue trigger when the last worker report is HARD_STOP: O2-8.
- Any other message, a continue trigger in any other situation included: send
  `USER MESSAGE: <the message, verbatim>` (O2-5). The worker applies MTC S4-6 to it.
The orchestrator never starts a batch without a continue trigger (Batch Stop Law, MTC S4-4 B-5).
It prints only: the O1-1 mode line; at most one progress line while a worker runs; a CHAT BLOCK
verbatim; the O2-4 line; the O2-6 sentence; its own HARD STOP [HS:PROSE] lines. Nothing follows a
printed CHAT BLOCK.

## O2-7 — Working files removed by the platform

After a long idle period the platform may replace the container while this chat holds a paper in
progress. When a bootstrap command fails because /tmp/fw_effective is missing, run
`ls /home/claude/*_batch_state.json` (existence only; never open the file):
- a BATCH STATE is listed — only the framework folder was lost. Run Step 0 and input staging again in
  this chat (O2-1), then start a fresh worker (`--continue`) with the message being handled.
- none is listed — the paper's working files are gone, the answer-key sidecar among them, and MTC
  S4-12 has no rebuild for that file (its step 4 loads it; a worker started now would begin the
  paper again from question 1 without saying so). v1.2.0 (G-14 row 11): the orchestrator RESTARTS THE PAPER
  AUTOMATICALLY — it re-runs Step 0 and input staging, starts a fresh worker with the ORIGINAL trigger, and
  prints once: `WORKDIR-LOST — the platform removed this paper's working files; the paper is being written
  again from question 1 automatically (batches delivered earlier are superseded).` No user step; never a stop.

## O2-8 — A run parked at a HARD STOP; a newer framework release (v1.1.0, OD-2026-11-09)

When the last worker report is HARD_STOP and the user sends a continue trigger:
1. Compare the production commit with the one this run verified:
   `git ls-remote https://github.com/iamdharmveer/framework-specs.git production` and
   `git -C /tmp/fw rev-parse HEAD` (read only; never a push).
2. DIFFERENT commit — a release was deployed after the stop. Run Step 0 and input staging again in this
   chat (they never touch /home/claude/<EXAM>_M<N>_* — the paper's working files are kept), read and
   prove this spec again (O2-1), then start a fresh worker with `--continue` and
   `USER MESSAGE: continue`. Its MTC S4-12 runs the state migration (bc.migrate_paper_state) first and
   continues the paper from where it stopped; nothing is written again from question 1.
3. SAME commit — start a fresh `--continue` worker with `USER MESSAGE: continue` (the stop may have been
   an INFRA-HEAL the previous worker could not finish). A stop it raises again ends the run.
A missing /tmp/fw or /tmp/fw_effective is O2-7, which comes first.

## O3-1 — PART B: WORKER LAW — ground rules

The worker is the Step 7 session of MTC: all of MTC applies, plus O3-1 to O3-8. Never run Step 0,
never clone, never delete or change /tmp/fw or /tmp/fw_effective; the working directory is
/tmp/fw_effective. Inputs are staged: project files in /mnt/project, chat attachments in
/mnt/user-data/uploads. Never start a sub-agent, never call a file-delivery tool, never wait for the
user: the worker's only reader is the orchestrator.
In every worker, reused or fresh, the ORCHESTRATOR MESSAGE `continue — delivery confirmed` IS the
user's continue trigger for MTC S4-6 and S4-5 CHECK 4, and `USER MESSAGE: <m>` is the user's message
<m> for S4-6.
A worker started with `--continue` that finds no BATCH STATE in /home/claude writes nothing: it
reports RESTART (WORKDIR-LOST) and the orchestrator restarts the paper automatically (O2-7, v1.2.0).

## O3-2 — Reading the route

Read with `python3 bootstrap.py --trigger <T> --progress <BATCH STATE> --read K` for K = 1..N, one
call each, in order (omit `--progress` while the BATCH STATE does not exist). bootstrap decides the
session class and the read set by MTC S1-0. Never read a spec with a sed range above 300 lines, never
read a spec any other way, never open a tool-output file the harness diverted.

## O3-3 — READ-RETENTION (binding in both modes)

Prove a read with `python3 bootstrap.py --retention "<nn>=<code> ..." --when <W>`, giving every
READ-ANCHOR code of that read from memory. Never open `.read_state`; never search earlier output for a
code. `RETENTION: PASS` is required at four points:
- (a) `--when after-read`: right after the read, before anything else;
- (b) `--when before-batch`: before authoring a batch (MTC S4-7 STEP A) or a correction (S4-6);
- (c) `--when after-batch`: after the batch's gates and report (S4-7 STEP B to D), before S4-7
  STEP E records the batch as delivered; for a correction, after S4-6 has applied and re-gated it,
  before its re-delivery;
- (d) `--when before-final`: before MTC Final Assembly (S13), for the session read and, when O3-5
  escalated, for the escalation read (add `--escalate`).
A FAIL at (a), (b) or (d): nothing was authored. WORKER MODE: report RETENTION_FAIL. DIRECT MODE: read
again (O3-2) in this chat, prove (a), continue.

A FAIL at (c): the batch (or correction) was authored without the specification in context; it is not
delivered, not recorded as completed, and is redone after a new read. NEW IN THIS SPEC — MTC S4-12 has no branch for
a batch authored but not recorded (its steps 3-4 keep the cumulative docx and answer key, which would
still hold that batch's questions while the BATCH STATE names it as current_batch). Therefore:
- WORK FILES = the regular files directly in /home/claude whose name starts with `<E>_` or matches
  `q*_*.png` or `q*_*.figspec.json` (MTC's figure files), except the CHAT BLOCK FILE and
  `<E>_M<N>_worker_report.json`; OUTPUT FILES = the regular files in /mnt/user-data/outputs whose
  name starts with `<E>_`.
- CHECKPOINT: right after (b) passes, empty the CHECKPOINT, then copy every WORK FILE into its
  `home/` and every OUTPUT FILE into its `outputs/`. Delete the CHECKPOINT as soon as the unit of
  work is safe: for a batch, after S4-7 STEP E has updated the BATCH STATE; for a correction, right
  after (c) passes.
- RESTORE: copy every file in `home/` and `outputs/` back over its origin; remove every WORK FILE
  that is not in `home/` and every OUTPUT FILE that is not in `outputs/`; delete the CHECKPOINT.
  The unit of work the CHECKPOINT was made for is then redone from the ORCHESTRATOR MESSAGE the
  session holds (O3-7): `continue — delivery confirmed` writes the batch again from S4-5 (the user's
  continue for it was already given), `USER MESSAGE: <m>` applies the correction again.
- A session that finds the CHECKPOINT after its own (a) PASS performs RESTORE before anything else
  (a CHECKPOINT that exists at a turn's start always marks an unfinished unit: a retention failure
  or a worker that stopped mid-way). WORKER MODE: the failing worker reports RETENTION_FAIL and the
  next worker restores. DIRECT MODE: read again, prove (a), restore, redo.

## O3-4 — DELIVERY PROXY (WORKER MODE)

Where MTC calls present_files (S4-7 STEP E, the S4-6 correction re-delivery, S13-8), the worker does
not deliver. The files stay where MTC put them in /mnt/user-data/outputs, and the worker carries on
with every step MTC orders after a successful call (state updates, the STOP line, S13-9's terminal
state and handoff block, the S13-9A footer per Framework_DeliveryFooter.md with a row for each listed
file) as if the call had returned every listed file.

Everything MTC tells the session to print in chat during the turn is written, in order, to the CHAT
BLOCK FILE instead, and nothing else is written there (output of MTC's code blocks is tool output,
not chat). The worker empties the CHAT BLOCK FILE at the start of every turn, except a turn started
by `FINAL ASSEMBLY` or `REVIEW RETURNED`, which appends. The chat prints are:
- session start: the S3-18 summary and batch plan, ending with its continue line;
- a non-final batch: the S4-5 CHECK 5 figural lines (only when CHECK 5 prints them); the S4-7 STEP D
  report, carrying every S4-11 item line (S4-11 EMISSION LAW) and the audit STDOUT; the S4-7 STEP E
  STOP line; the S13-9A F1 footer. S4-8 prints nothing in chat;
- the final batch and Final Assembly: the S4-5 CHECK 5 lines; the S4-7 STEP D report; the S4-9 line
  `=== Final batch complete. Running Final Assembly... ===`; the S13-9 handoff block; the S13-9A
  footer of the type Framework_DeliveryFooter.md selects (it places the REGISTRY HANDOFF lines S13-8
  prints from `pp.handoff_footer_lines`). The final batch has no STOP line and no F1 footer (S4-7
  STEP F, S4-9, S13-9A);
- a user message: what S4-6 prints for it, and the S4-12 step 5 resume summary when S4-12 runs
  steps 5-6 (O3-7);
- a HARD STOP [HS:PROSE]: its full text (O3-8).

Then run
`python3 bootstrap.py --worker-report write --exam <E> --paper <N> --state <STATE> --batch <K> --of <M> --files "<paths>" --chat-file /home/claude/<E>_M<N>_chat_block.md`
adding `--review-parts "<dir1>,<dir2>"` for REVIEW_REQUEST and GRADE_REQUEST (the job folders). <paths> = the full paths MTC's present_files
call of this turn would have passed, in its order, comma-separated; `""` when the turn has no such
call. K = the number of batch ids in batches_completed; M = the number of batches in batch_plan (both
0 before S3-16 writes the plan). The worker's final message is the one line
`WORKER DONE <STATE> batch K of M`. STATE, by where the turn ends:
- BATCH_DELIVERED: MTC ends the response after a batch (S4-7 STEP F), after the session start
  (S3-18), after a user message (S4-6) or after the S4-12 resume summary;
- FINAL_BATCH_BUILT: the final batch reached S4-9 (O3-5);
- REVIEW_REQUEST: S13-2G phase 2 is reached (O3-6);
- GRADE_REQUEST: S4-7 STEP A2 printed JOBS OUT (O3-9; v1.3.0);
- ROTATE: the worker's remaining room is below SESSION_BUDGET.json `work_unit_tokens` (or it cannot tell and has
  finished at least one batch since its start) — its state is saved; never a HARD STOP for room (v1.3.0);
- PAPER_DELIVERED: S13-9 and its footer are written;
- RETENTION_FAIL: O3-3; HARD_STOP: O3-8.

## O3-5 — One MTC response per turn; Final Assembly

A worker turn is one MTC response, cut at four points: when the final batch reaches S4-9
(FINAL_BATCH_BUILT), when S13-2G phase 2 is reached (REVIEW_REQUEST), when S4-7 STEP A2 prints JOBS OUT
(GRADE_REQUEST, v1.3.0) and when the worker's room is short (ROTATE, v1.3.0). At FINAL_BATCH_BUILT the final
batch has gone through S4-7 STEP A to E and S4-8: its questions are in the cumulative docx
`[ExamCode]_[paper_slug]_Q1to[last_q].docx` in /mnt/user-data/outputs; their answers are in the
answer-key sidecar (written per question, S4-8a ORDERING); progress.json is written when the batch had
PASSAGE questions (S4-8b); the figural manifest is updated (STEP C); the BATCH STATE lists the final
batch in batches_completed, has current_batch incremented and the ledgers refreshed (S4-8a). The
registry holds no committed question_index entry for this paper and batch_state.state is not set. On
`FINAL ASSEMBLY` goes to a fresh worker (O2-5), which reaches S13 through S4-12's FINAL ASSEMBLY
INTERRUPTED BEFORE THE REVIEW rule (S13-2 / S13-2F onward); in DIRECT MODE the session proceeds into
S13 as S4-9 says.

Before Final Assembly, a worker whose read was NON-FINAL performs MTC S1-0's one-way escalation:
`python3 bootstrap.py --trigger <T> --progress <BATCH STATE> --read K --escalate` for K = 1..N, then
`python3 bootstrap.py --retention "<nn>=<code> ..." --escalate --when before-final`.

## O3-6 — Independent review hand-over (MTC S13-2G phase 2, WORKER MODE)

When S13-2G phase 1 has written REVIEW_DIR/queue.json (a worker cannot start sub-agents):
1. For each part to review (at first: every part in queue.json), write `<dir>/REVIEWER_BRIEF.txt`
   holding the REVIEWER BRIEF of S13-2G phase 2 — the lines after
   `# REVIEWER BRIEF (verbatim; fill <PART_DIR>):` to the end of that block, each without its leading
   `#` and the spaces after it — with every `<PART_DIR>` replaced by the part's 'dir'. Report
   REVIEW_REQUEST with `--review-parts` = those directories, and stop.
2. On `REVIEW RETURNED`: in queue.json, for each returned part, set 'reviewer' = 'sub-agent', add 1
   to 'attempts', and set 'error' = the returned line when it does not start with `REVIEW DONE`. Then
   apply S13-2G phase 2 step 2 (CHECK) to every part: a part whose returned line does not start
   with `REVIEW DONE`, or whose verdicts.json is missing or does not parse, gets its one retry when
   'attempts' is 1 (report REVIEW_REQUEST again for exactly those
   parts) and the same-session fallback of step 3 when 'attempts' is 2. Then phase 3, in this turn.
Steps 3 to 5 of phase 2, the round-2 review after REVIEW_REPAIR and S4-12's REVIEW_RUNNING branch are
unchanged. In DIRECT MODE S13-2G runs as written.
v1.1.0: the review MODE is carried by the folder name the worker reports with `--review-parts` (the
orchestrator never opens queue.json): a folder whose name ends in `_switch` (an adjudication) or `_panel`
(a panel copy), or a folder named `switched` (a D0 re-review — the worker copies the part's
review_packet.json and *_Create.docx into '<dir>/switched/', writes the brief there with <PART_DIR> =
'<dir>/switched' and reports that folder; MTC S13-2G phase 2 step 3b) gets its reviewer on a DIFFERENT
model than the round's other reviewers — the next of SESSION_BUDGET.json worker_models; with one model
only, a fresh context. Every other folder is reviewed as before. Delta rounds use REVIEW_DIR names
.../delta<k>/part<n>[_switch|_panel]; nothing else differs.

## O3-9 — In-batch grading hand-over (MTC S4-7 STEP A2, WORKER MODE; v1.3.0)

A worker cannot start sub-agents, so the fresh blind graders and solvers of the batch it is writing go to the
orchestrator: MTC S4-7 STEP A2 writes one job folder per (question, role) with packet.json and JOB_BRIEF.txt
(blueprint_core.bv_jobs — the packet carries nothing that names the slot's band, the plan or the solution) and
reports GRADE_REQUEST with `--review-parts` = those folders (bootstrap prints them as GRADE JOBS). On
`GRADE RETURNED` the worker (the same one, or a fresh `--continue` worker after S4-12's BATCH IN VERIFICATION
branch) reads each `<job_dir>/result.json` (blueprint_core.bv_read_result), records the grades with their packet
sha256 and context 'fresh', and applies blueprint_core.bv_decide per question: pass, tiebreak (one more grader
job), ONE rewrite, or settle. Tiebreak and regrade jobs are a further GRADE_REQUEST in the same batch (at most
blueprint_core.BV_MAX_ROUNDS per batch). A job that returned nothing gets one new job in the next round; a
question that still has fewer than two grades after BV_MAX_ROUNDS is the NO-MODEL environment failure of MTC
S0-OP-10. Only when every question of the batch is settled does the worker run STEP B and report BATCH_DELIVERED.
In DIRECT MODE the session starts these jobs itself when it can start a sub-agent; otherwise NO-MODEL.

## O3-7 — A worker that starts from disk (`--continue`)

After (a) passes, the worker performs RESTORE when the CHECKPOINT exists (O3-3). Then, in every case,
it runs MTC's session start (S3-1 loads what S4-12 step 0 relies on) and S4-12. NEW IN THIS SPEC — S4-12's batch recovery ends with the resume summary
and STOP (steps 5-6), which would ask the user again for a message already given. So a worker that
holds an ORCHESTRATOR MESSAGE ends S4-12's batch recovery after step 4c and applies MTC S4-6 to its
message: `continue — delivery confirmed` is a continue trigger (it satisfies S4-5 CHECK 4);
`USER MESSAGE: <m>` is <m>; `GRADE RETURNED ...` is handled by S4-12's BATCH IN VERIFICATION branch
(O3-9). S4-12's other branches are unchanged: with `FINAL ASSEMBLY` it enters S13
by its FINAL ASSEMBLY INTERRUPTED BEFORE THE REVIEW rule (O3-5); with `REVIEW RETURNED` the worker
first performs O3-6 step 2, which runs inside S4-12's REVIEW_RUNNING branch.

## O3-8 — HARD STOP inside a worker; MANDATE 0 [HS:PROSE]

A HARD STOP [HS:PROSE] raised anywhere (MTC, bootstrap, an engine) ends the turn: its full text goes
to the CHAT BLOCK FILE and the worker reports HARD_STOP. RETENTION_FAIL needs no chat block. MTC
MANDATE 0 covers the CHAT BLOCK FILE, the worker report and the final line: no question content.
v1.1.0 (MTC MANDATE 0b): an "INFRA-HEAL [HS:LADDER]", "SLOT-CHAIN [HS:LADDER]", "DELTA [HS:LADDER]" or
"REVIEW-VOID [HS:LADDER]" is NOT a stop — the worker performs what it names and continues in the same
turn. A worker never reports HARD_STOP for a stop the executed block did not raise at that point.

## O4-1 — Budgets (SESSION_BUDGET.json; never copy a value into a run)

```text
key                      used by                    meaning
bytes_per_token          bootstrap, SPEC-CAPACITY   spec bytes per token (currently 2.3)
read_chunk_max_lines     bootstrap --read           lines per read call (currently 300)
read_chunk_max_bytes     bootstrap --read           bytes per read call (currently 28000)
context_baseline_tokens  SPEC-CAPACITY              a sub-agent's context before any read
compaction_floor_tokens  SPEC-CAPACITY              lowest measured silent-compaction point
rotate_tokens            O2-5                       a worker is replaced before this size
work_unit_tokens         O2-5, SPEC-CAPACITY        room one batch or correction needs
read_cap_tokens          SPEC-CAPACITY              rotate - baseline - work unit: the route cap
worker_models            O2-2                       worker and reviewer model preference order
max_batches_per_worker   O2-5                       batches before a worker is replaced
orchestrated             bootstrap --trigger        triggers that run under this spec
```
Values change only with a re-measurement recorded in CHANGELOG.md (SESSION_BUDGET.json `_change_rule`).

## O5-1 — DIRECT MODE

This chat is the Step 7 session. Read the whole route with
`python3 bootstrap.py --trigger <T> --progress <BATCH STATE> --read K` (O3-2); prove (a) to (d)
(O3-3: on a FAIL read again in this chat — the paper's state is on disk — then continue; a FAIL at (c)
uses RESTORE); escalate as O3-5 says; execute MTC as written: the session delivers its own files with
present_files and S13-2G runs as written. O3-1, O3-4, O3-6 and O3-7 do not apply. The limit, stated
plainly: a long paper is read again each time retention fails. When a completed read fails (a) twice
in a row in this chat, print this line and END:
`HARD STOP [HS:INFRA] MODEL-CAPACITY — this chat's model cannot hold the Step 7 specification. Select a larger-context model for this chat and type continue. Nothing was lost: the paper resumes from its saved state.`

## O6-1 — PART F (v1.2.0): FRESH-CONTEXT WORKERS (GAP-2026-11-10; Create S0-OP-5 / S0-OP-8 / S13-2R)

A control that must be INDEPENDENT of the author is never run in the author's context. The orchestrator (or,
in DIRECT MODE, a sub-agent the session starts) runs it in a FRESH context that receives ONLY the packet the
engine builds, and returns ONLY the fields named here. Each result records context 'fresh' and the packet's
sha256 (blueprint_core.dl_set_label_basis_strict refuses a grade without them).
- O-GRADE — per item, INSIDE ITS BATCH (v1.3.0: requested with GRADE_REQUEST, O3-9): two blind GRADERS (packet = blueprint_core.build_judge_input(item, <ruler anchors
  with content>); never the band, plan, obs, solution or the author's counts) -> {band, decisions, rationale};
  two blind SOLVERS (packet = stem + options only) -> {answer, confidence, assumptions[]}. Graders and solvers
  are four separate fresh contexts; a switched model is used when the platform offers one. v1.3.0: a split
  between the two graders gets ONE more grader (blueprint_core.bv_decide 'tiebreak'), never a rewrite.
- O-VISION — per rendered organic figure: a fresh vision pass that never saw the SMILES transcribes the image
  -> {smiles, stereo_mode}; 2 independent reads when the answer depends on stereo, else 1
  (figural_vision.readback_compare decides the match).
- O-REFILL — Create S13-2R 'refill_session' / 'last_resort_generate': a fresh worker resumes from saved state
  and writes the entry's K candidates for the open slot only (composer + library on), each through O-GRADE and
  O-VISION; at most blueprint_core.C_REFILL_SESSIONS refill sessions per paper (batch_state counter).
- O-BACKFILL — Create S0-OP-0: PYQExplain §13A-3B on the records listed, in fresh workers; each upgraded record
  is saved into /home/claude/<E>_op_profile.json as it completes (a resumed run continues from it). When every
  listed record is done the orchestrator re-runs Create S0-OP-0 and S0-OP-2 (ruler rebuilt) before Q1.
- O-AUTHOR — the author worker of an organic slot reads blueprint_core.author_brief (<= C_BRIEF_MAX_PAGES
  pages) plus the engine call list instead of the full Create spec (G-13); the orchestrator keeps the full spec.
A platform that can start neither a sub-agent nor a worker cannot produce a fresh control: that is the
NO-MODEL environment failure — save state, print one plain instruction, resume when it returns; a same-context
result is never recorded as 'fresh' and nothing is delivered uncertified.

## O6-2 — Faults that outlive their self-heals (v1.2.0, G-14 row 7)

An INFRA fault still present after blueprint_core.INFRA_HEAL_MAX heals in one worker is retried in a FRESH
worker (at most 3 fresh workers per stop site). A fault that persists on the verified clone is a release
defect: the paper continues on the PREVIOUS verified production release (Step 0 with that commit) and a P0
framework incident naming the stop site is recorded in difficulty_state['incidents']. A worker report that is
missing, stale or for the wrong part is answered with a fresh worker that resumes the saved state.

# END OF Framework_MockTestOrchestrate v1.3.0
