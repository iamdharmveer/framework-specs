---
name: mock-test-framework
description: Central source of truth for the exam mock-test framework. Use this whenever the user triggers a framework step — PYQPrepare, PYQDraft, PYQScan, PYQApprove, PYQSort, PYQCount, PYQExtract, PYQExplain, PYQFormat, PYQDeliver, MockBlueprint, ScopedBlueprint, MockCreate, TestCreate, MockExplain, TestExplain, MockDeliver, TestDeliver, PYQCompress, NotesBlueprint, NotesCreate, NotesAudit, or NotesDeliver — or asks to generate, audit, explain, tag, deliver, or shrink an oversized mock/PYQ document, or to blueprint, draft, audit, or deliver exam study notes. It pulls the latest verified specs from the central GitHub repo, verifies their integrity, and runs the requested step from the complete spec. Do not generate any mock-test output from memory.
---

# Mock Test Framework — Source of Truth

SPECS ARE PROJECT-FIRST (2026.08.03.8). If a `Framework_*.md` is present in the exam
project's Files section, THAT copy is authoritative for this run. GitHub supplies only the
specs the project does not carry. Precedence is PER FILE — a project may override one spec
and inherit the rest.
CONTRACT FLOOR (2026.11.04): a project copy of a spec named in STEP_CONTRACTS.json
`override_floor` whose version is BELOW its floor is NOT loaded — the verified repo copy is
used and Step 0 prints `[STALE — NOT LOADED]` (never a stop). It protects the Step 7 user
contract (two files, review in-session) from an outdated project copy.

ENGINES ARE REPO-ONLY. All 18 routed engine scripts, plus the 9 tracked-but-never-routed
scripts (validate_framework_md.py the CI validator; audit_canonical.py the canonical auditor
that Step 6 copies to each exam and Step 7 runs as its self-audit; spec_source.py the
resolver; run_ci_gates.py the CI-parity gate runner; regression_pyq_fixtures.py the
cross-exam regression suite; handshake_audit.py the cross-step handshake audit
(GAP-2026-11-03); and the three baseline auditors spec_name_audit.py, mock_sync_audit.py and
notes_sync_audit.py), come ONLY from the verified clone. `/mnt/project` is never placed on `sys.path`,
so a `.py` sitting in a project's Files section is never imported and editing one has no
effect. `routes.json` and `MANIFEST.json` are likewise repo-only.

WHAT PROJECT-FIRST COSTS — read this once, it is not a formality. `bootstrap.py` verifies
sha256, version header, END-sentinel and exact line count against `MANIFEST.json`, which
describes the REPO. A project-supplied spec has no manifest entry, so byte-integrity
verification is IMPOSSIBLE for it — not skipped, impossible. `spec_source.py` checks what
can be checked without a reference (non-empty, UTF-8, well-formed header, header/filename
agreement, sentinel present per the repo's own convention, header/sentinel version
agreement) and HARD-STOPS on failure. Passing proves the file is WELL-FORMED. It never
proves it is correct, current, or in step with the repo engines it drives. A project spec
that is simply old is perfectly well-formed and will be used.

NEVER work from memory. That rule is unchanged and absolute.

## STEP 0 — Load and verify the framework (run this bash FIRST, before every step)

```bash
set -e
FW=/tmp/fw && rm -rf "$FW"
PRIMARY=https://github.com/iamdharmveer/framework-specs.git
# NOTE: no DR yet — same URL as PRIMARY; set a distinct mirror before relying on failover.
MIRROR=https://github.com/iamdharmveer/framework-specs.git
n=0
until git clone --depth 1 --branch production "$PRIMARY" "$FW" 2>/dev/null; do
  n=$((n+1)); [ "$n" -ge 3 ] && break; sleep $((2**n)); done
if [ ! -d "$FW/.git" ]; then
  [ "$MIRROR" = "$PRIMARY" ] && { echo "HARD STOP: primary unreachable and no DR mirror configured (MIRROR == PRIMARY). DO NOT proceed from memory."; exit 1; }
  git clone --depth 1 --branch production "$MIRROR" "$FW" 2>/dev/null \
    || { echo "HARD STOP: framework repo unreachable (primary + mirror). DO NOT proceed from memory."; exit 1; }
fi
cd "$FW" && python3 bootstrap.py \
  || { echo "HARD STOP: framework verification failed. DO NOT proceed."; exit 1; }
# Figure rendering + conformance gates (Framework v5.33 / Audit v2.11).
# matplotlib is REQUIRED to render a figure; pillow and numpy are required for
# the pixel gates; scipy and fonttools are optional. Absence never halts an
# audit — every gate degrades to DORMANT-but-reported — but a Create step
# CANNOT draw a figure without matplotlib, so install it here rather than
# discover it as a traceback mid-paper.
pip install matplotlib pillow numpy scipy fonttools rdkit scikit-image --break-system-packages -q 2>/dev/null \
  || echo "WARN: figure dependencies incomplete — run figural_core.preflight() and expect DORMANT figure gates."
python3 -c "import figural_core as fc, json; print('FIGURE PREFLIGHT:', json.dumps(fc.preflight()['available']))" 2>/dev/null || true
# ── PROJECT-FIRST SPEC RESOLUTION (2026.08.03.8) ────────────────────────────
# Owner rule: a Framework_*.md present in the exam project's Files section WINS.
# GitHub supplies only the specs the project does not carry. Precedence is PER FILE.
# Engines are NEVER taken from the project; /mnt/project is never on sys.path.
python3 spec_source.py --resolve --repo-dir "$FW" --project-dir /mnt/project \
        --overlay-dir /tmp/fw_effective \
  || { echo "HARD STOP: a project spec is malformed or truncated. Fix or remove it in the project Files section. DO NOT proceed."; exit 1; }
cd /tmp/fw_effective
```

STEP 0b — INPUT STAGING. If the `python3 bootstrap.py` output above printed `SURFACE:`, run
`cd /tmp/fw && python3 bootstrap.py --stage-inputs --trigger <Step>` (the step the user asked
for) and follow what it prints (the project-document
procedure, then `python3 bootstrap.py --stage-status` until it prints STAGING COMPLETE), then re-run
the resolve line:
`python3 spec_source.py --resolve --repo-dir /tmp/fw --project-dir /mnt/project --overlay-dir /tmp/fw_effective && cd /tmp/fw_effective`

## RULES

1. If Step 0 prints "HARD STOP" or exits non-zero, STOP — generate nothing.
2. After it succeeds, open the spec in /tmp/fw_effective (the resolved corpus: the verified
   clone with any project specs laid over it) that matches the step the user asked for
   (e.g. "MockDeliver M1" -> Framework_MockDeliver.md; PYQDraft/PYQScan/PYQApprove/PYQCount each load their step file PLUS Framework_PYQCore.md) and READ IT IN FULL — the read-in-full rule applies to .md SPEC files ONLY; .py ENGINE files in the route are EXECUTED via `import` inside the spec's code blocks and must NOT be read into context — every line to
   its "# END OF ..." sentinel. Some specs are thousands of lines (Blueprint ~6400) — read
   all pages, never a partial. Trimmed, summarised or partial WORKING COPIES of a spec are
   PROHIBITED (GAP-2026-11-02 P1); `python3 bootstrap.py --trigger <Step> --receipt` prints
   the exact bytes the run is held to, and the delivery footer repeats them.

2a. RUN `python3 bootstrap.py --trigger <Step> --progress <the step's own progress file, if it
   exists>` FIRST. The progress file: PYQExtract — [ExamCode]_analysis_progress.json; MockBlueprint —
   [ExamCode]_blueprint.json; MockCreate / TestCreate — /home/claude/[ExamCode]_M[N]_batch_state.json;
   MockExplain / TestExplain — that step's own state file (Framework_MockTestExplain.md S0-3). It prints the entry files split by role AND the PRE-WORK READ
   BUDGET — lines, bytes, tokens, calls — AND the SESSION CLASS. Do not start reading
   before you have seen that block. GAP-2026-08-16-STEP5-SESSION-EXHAUSTION: this rule
   was a hard, unbounded obligation that nothing anywhere priced, and on PYQExtract it
   costs 556,834 B / ~139,208 tok / >=36 view calls BEFORE any work. In the reference
   incident 40 of a session's 50 tool calls went to satisfying this rule and ZERO of 22
   papers were processed. Framework_PYQCore EC-P42.

2b. READ SPECS ONLY WITH `python3 bootstrap.py --trigger <Step> [--progress <file>] --read K`
   for K = 1..N, one call each, in order (bootstrap prints N; each call serves at most 300 lines).
   Measured 2026-11-06 (SESSION_BUDGET.json): a tool result of about 40,000 characters or more is
   diverted to a file the session cannot read back whole. Never read a spec with a sed range above
   300 lines or with `view`, and never open a tool-output file the harness diverted.

2c. SESSION CLASS decides the READ SET, and only for a spec that declares one
   (SPEC_SECTIONS.json says which; today that is Framework_MockTestAnalyse.md). Any spec
   with no declared read set is read IN FULL — the default is always the whole file.
     FINAL      -> read everything, no exception. This session may write the final
                   artefacts, and synthesising from a reduced read is exactly the
                   "paraphrased spec" failure the corpus has regressed on before.
     NON-FINAL  -> read the ranges bootstrap prints. Sections a non-final session can
                   never execute are skipped. Measured: 529,438 -> 257,723 B.
   ESCALATION IS MANDATORY AND ONE-WAY. If a session begins NON-FINAL and discovers
   mid-run that it has cleared the corpus, it MUST read the omitted sections BEFORE
   synthesis. It may never write a final artefact from a reduced read. FINAL never
   downgrades. Line ranges come from SPEC_SECTIONS.json, which is GENERATED from each
   spec's own headers and verified by bootstrap — never hand-copied into a chat.
2d. READ-RETENTION (GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY). Every read ends with READ-ANCHOR
   codes. Prove the read from memory with `python3 bootstrap.py --retention "<nn>=<code> ..."` after
   the read and wherever the step's spec requires it (Step 7: Framework_MockTestCreate.md S1-0R);
   never open `.read_state`. RETENTION: FAIL means the spec is no longer in context: read it again,
   then continue from the state on disk.
2e. STEP 7 RUNS ORCHESTRATED (owner decision OD-2026-11-06). For MockCreate / TestCreate this chat
   reads ONLY Framework_MockTestOrchestrate.md
   (`python3 bootstrap.py --trigger <Step> --role orchestrator --read K`) and follows it: worker sub-agents read and execute the full Step 7
   specification, and starting them is authorised by the owner — do not ask the user. Rule 2's
   read-in-full binds each worker, and this chat only when that spec sends it to DIRECT MODE.
3. Read blueprint.json / registry.json / per-exam files from /mnt/project (the project's
   own files; staged by bootstrap --stage-inputs on surfaces that do not mount it), exactly as
   the specs describe.
4. Before presenting any output, confirm /tmp/fw/.verified exists AND that the
   "SPEC SOURCE:" provenance report from Step 0 was printed. If it listed any
   [PROJECT-UNVERIFIED] spec, the delivery footer MUST disclose that (Framework_DeliveryFooter
   §2A) — naming each project-sourced spec. A run on project specs still completes and still
   delivers; it is never silently presented as fully verified.
4b. An [ORPHAN — NOT LOADED] line means the project holds a spec no trigger routes (e.g. a
   spec for a retired step). It is ignored, never executed. Tell the user it can be deleted.
5. **In-protocol vision is not "working from memory."** The "never from
   memory" rule bans inventing question CONTENT from your own knowledge. It
   does NOT ban spec-sanctioned reading of the SOURCE. When a spec protocol
   (e.g. PYQPrepare S1-12 Image Inspection, or S1-13 Scanned-Source Vision
   Transcription) directs you to view an extracted image or a rasterised scan
   page and transcribe it, that transcription IS the executed protocol —
   perform it and proceed. A FORMAT C1/C-HYBRID scan therefore does NOT hard
   stop; only FORMAT C0 (illegible) halts.
