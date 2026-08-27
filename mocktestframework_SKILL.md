---
name: mock-test-framework
description: Central source of truth for the exam mock-test framework. Use this whenever the user triggers a framework step — PYQPrepare, PYQDraft, PYQScan, PYQApprove, PYQSort, PYQCount, PYQExtract, PYQExplain, PYQFormat, PYQDeliver, MockBlueprint, ScopedBlueprint, MockCreate, TestCreate, MockExplain, TestExplain, MockDeliver, TestDeliver, PYQCompress, NotesBlueprint, NotesCreate, NotesAudit, or NotesDeliver — or asks to generate, audit, explain, tag, deliver, or shrink an oversized mock/PYQ document, or to blueprint, draft, audit, or deliver exam study notes. It pulls the latest verified specs from the central GitHub repo, verifies their integrity, and runs the requested step from the complete spec. Do not generate any mock-test output from memory.
---

# Mock Test Framework — Source of Truth

SPECS ARE PROJECT-FIRST (2026.08.03.8). If a `Framework_*.md` is present in the exam
project's Files section, THAT copy is authoritative for this run. GitHub supplies only the
specs the project does not carry. Precedence is PER FILE — a project may override one spec
and inherit the rest.

ENGINES ARE REPO-ONLY. All 17 routed engine scripts, plus the 6 tracked-but-never-routed
scripts (validate_framework_md.py the CI validator; audit_canonical.py the canonical auditor
that Step 6 copies to each exam and Step 7 runs as its self-audit; spec_source.py the
resolver; and the three baseline auditors spec_name_audit.py, mock_sync_audit.py and
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
pip install matplotlib pillow numpy scipy fonttools --break-system-packages -q 2>/dev/null \
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

## RULES

1. If Step 0 prints "HARD STOP" or exits non-zero, STOP — generate nothing.
2. After it succeeds, open the spec in /tmp/fw_effective (the resolved corpus: the verified
   clone with any project specs laid over it) that matches the step the user asked for
   (e.g. "MockDeliver M1" -> Framework_MockDeliver.md; PYQDraft/PYQScan/PYQApprove/PYQCount each load their step file PLUS Framework_PYQCore.md) and READ IT IN FULL — the read-in-full rule applies to .md SPEC files ONLY; .py ENGINE files in the route are EXECUTED via `import` inside the spec's code blocks and must NOT be read into context — every line to
   its "# END OF ..." sentinel. Some specs are thousands of lines (Blueprint ~6400) — read
   all pages, never a partial.

2a. RUN `python3 bootstrap.py --trigger <Step> --progress <the exam's *_analysis_progress.json,
   if one exists>` FIRST. It prints the entry files split by role AND the PRE-WORK READ
   BUDGET — lines, bytes, tokens, calls — AND the SESSION CLASS. Do not start reading
   before you have seen that block. GAP-2026-08-16-STEP5-SESSION-EXHAUSTION: this rule
   was a hard, unbounded obligation that nothing anywhere priced, and on PYQExtract it
   costs 556,834 B / ~139,208 tok / >=36 view calls BEFORE any work. In the reference
   incident 40 of a session's 50 tool calls went to satisfying this rule and ZERO of 22
   papers were processed. Framework_PYQCore EC-P42.

2b. READ WITH `sed -n 'START,ENDp' <file>` IN BASH, NOT WITH `view`. Measured in the
   container: `view` truncates output above ~16,000 characters INCLUDING explicitly
   ranged reads — a view [1,700] on a 57-bytes/line spec returns "< truncated lines
   120-581 >" and costs three more calls to cover one window — while a bash heredoc
   returned 188,024 characters intact in a single call. Same context cost, ~10x fewer
   tool calls, and tool calls are a resource that runs out. Read in sequential,
   non-overlapping ranges and never re-read a range you already hold.

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
3. Read blueprint.json / registry.json / per-exam files from /mnt/project (the project's
   own files), exactly as the specs describe.
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
