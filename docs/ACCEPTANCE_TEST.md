# One-time Acceptance Test (run inside ONE real exam project before rollout)

Paste this into an exam-project chat and run it. It confirms the two environment
facts the architecture depends on: GitHub egress, and the project mount.

    # 1) GitHub egress?
    git ls-remote https://github.com/iamdharmveer/framework-specs.git >/dev/null 2>&1 \
      && echo "EGRESS OK" || echo "NO EGRESS — git approach not viable in this sandbox"

    # 2) Project files mounted where the specs expect?
    ls -d /mnt/project >/dev/null 2>&1 \
      && echo "MOUNT OK (/mnt/project present)" || echo "MOUNT MISSING — check where project files are mounted"

    # 3) Full end-to-end dry run of the loader
    FW=/tmp/fwtest && rm -rf "$FW"
    git clone --depth 1 --branch production https://github.com/iamdharmveer/framework-specs.git "$FW" \
      && cd "$FW" && python3 bootstrap.py --trigger MockDeliver

Expected: "EGRESS OK", "MOUNT OK", and a green "[OK] FRAMEWORK ... VERIFIED".
If EGRESS is not OK, tell me — we switch the load mechanism before rolling out.
