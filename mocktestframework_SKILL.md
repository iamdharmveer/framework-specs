---
name: mock-test-framework
description: Central source of truth for the exam mock-test framework. Use this whenever the user triggers a framework step — PYQPrepare, PYQDraft, PYQScan, PYQApprove, PYQSort, PYQCount, PYQExtract, PYQExplain, PYQExplainAudit, PYQFormat, PYQDeliver, MockBlueprint, ScopedBlueprint, MockCreate, TestCreate, MockCreateAudit, TestCreateAudit, MockExplain, TestExplain, MockExplainAudit, TestExplainAudit, MockDeliver, or TestDeliver — or asks to generate, audit, explain, tag, or deliver a mock test paper. It pulls the latest verified specs from the central GitHub repo, verifies their integrity, and runs the requested step from the complete spec. Do not generate any mock-test output from memory.
---

# Mock Test Framework — Source of Truth

The 16 framework specs and 5 engine scripts live ONLY in the central GitHub repo below,
never in project knowledge. NEVER work from memory or from any Framework_*.md that may
appear in project knowledge. Always pull and verify the latest specs first.

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
```

## RULES

1. If Step 0 prints "HARD STOP" or exits non-zero, STOP — generate nothing.
2. After it succeeds, open the spec in /tmp/fw that matches the step the user asked for
   (e.g. "MockDeliver M1" -> Framework_MockDeliver.md) and READ IT IN FULL — every line to
   its "# END OF ..." sentinel. Some specs are thousands of lines (Blueprint ~6400) — read
   all pages, never a partial.
3. Read blueprint.json / registry.json / per-exam files from /mnt/project (the project's
   own files), exactly as the specs describe.
4. Before presenting any output, confirm /tmp/fw/.verified exists.
5. **In-protocol vision is not "working from memory."** The "never from
   memory" rule bans inventing question CONTENT from your own knowledge. It
   does NOT ban spec-sanctioned reading of the SOURCE. When a spec protocol
   (e.g. PYQPrepare S1-12 Image Inspection, or S1-13 Scanned-Source Vision
   Transcription) directs you to view an extracted image or a rasterised scan
   page and transcribe it, that transcription IS the executed protocol —
   perform it and proceed. A FORMAT C1/C-HYBRID scan therefore does NOT hard
   stop; only FORMAT C0 (illegible) halts.
