# Paste-in Custom Instructions (identical for ALL 200 exam projects)

> ⚠️ **DEPRECATED — superseded by `mocktestframework_SKILL.md`.**
> The live path is now the **account-level skill** (claude.ai → Customize → Skills),
> which is the single source of truth for the STEP 0 load-and-verify bootstrap and the
> trigger list. This paste-in block is kept ONLY for environments that cannot use the
> skill. **Do not edit trigger names or bootstrap logic here — change the skill instead;**
> `check_triggers.py` enforces that the skill's trigger list matches `routes.json`.
> (This block is not auto-synced, so treat the skill as authoritative if they differ.)

Paste the block below into each exam project's **Custom Instructions**.
Only the two URLs are constants; everything else is identical everywhere.
Replace <YOU> with your GitHub username and <MIRROR_URL> with your mirror repo.

--------------------------------------------------------------------------------
FRAMEWORK SOURCE OF TRUTH — READ BEFORE EVERY STEP

The 11 framework specs and 3 engine/gate scripts live ONLY in the git repo below.
They are NOT in this project's knowledge. Never generate anything from memory,
chat history, or any Framework_*.md that may appear in project knowledge — the
repo clone is the single source of truth.

STEP 0 — BOOTSTRAP (run this bash FIRST, on every step trigger, before anything else):

    set -e
    FW=/tmp/fw && rm -rf "$FW"
    PRIMARY=https://github.com/iamdharmveer/framework-specs.git
    MIRROR=<MIRROR_URL>
    TRIGGER="PUT_THE_STEP_TRIGGER_HERE"   # e.g. MockDeliver
    n=0
    until git clone --depth 1 --branch production "$PRIMARY" "$FW" 2>/dev/null; do
      n=$((n+1)); [ "$n" -ge 3 ] && break; sleep $((2**n))
    done
    if [ ! -d "$FW/.git" ]; then
      git clone --depth 1 --branch production "$MIRROR" "$FW" 2>/dev/null \
        || { echo "HARD STOP: framework repo unreachable (primary+mirror). DO NOT proceed from memory."; exit 1; }
    fi
    cd "$FW"
    python3 bootstrap.py --trigger "$TRIGGER" \
      || { echo "HARD STOP: framework verification failed. DO NOT proceed."; exit 1; }

RULES:
1. If Step 0 prints "HARD STOP" or exits non-zero, STOP. Do not generate a paper.
2. After Step 0 succeeds, READ each file it lists IN FULL — the whole file, top to
   its "# END OF ..." sentinel line. The printed line count is exact; if your read
   stops before the END sentinel, keep reading the remaining lines. Never work from
   a partial read.
3. Read blueprint.json / registry.json / per-exam artifacts from /mnt/project (the
   project Files section) exactly as the specs describe — those stay in the project.
4. The delivery/audit step must confirm /tmp/fw/.verified exists and matches the
   current trigger before producing or presenting any file.
--------------------------------------------------------------------------------
