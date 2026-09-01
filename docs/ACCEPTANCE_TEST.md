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


# Acceptance — GAP-2026-09-01-RECALL-CONTRACT (run in ONE real exam project before rollout)

- A-1 Six-concept unit with one integration section, ≥ 1 earlier subtopic →
  7 core + 3 cumulative Recalls; no consecutive same-identity pair; ≥ 1
  near-miss; NA G-14 PASS.
- A-2 First subtopic of a topic → 0 cumulative items; G-14 PASS.
- A-3 TIER-3 unit, difficulty profile absent → B7 ships; every band on the
  topic/neutral rung; footer discloses "profile absent — exam-wide mix check
  dormant"; no hard stop.
- A-4 Concept with 4 Medium + 1 Hard PYQs → core Recall labelled Medium and
  `recall_verify_difficulty` agrees; the near-miss on that concept is Hard.
- A-5 A Recall stem that names the method the anchor PYQ made the student
  recognise scores below its band → rewritten (≤ 6 tries) or that item HARD
  STOPS; it never ships relabelled.
- A-6 A Recall whose scenario clones an Example → validate_model FAIL at NC.
- A-7 A unit drafted before NC v2.9.0 re-run at NA → G-14 DORMANT (reason: no
  recall_contract record); every other gate identical to v3.6.0.
- A-8 Profile present; the set's band mix off the exam's paper-level mix by 2
  items in one band → G-14 FAIL naming the band; off by 1 → PASS.
- A-9 A unit with >= 2 concept sections, or any Hard PYQ, whose Recalls all
  record axiom_concepts = 1 → validate_model FAIL at NC (section trigger) /
  G-14 FAIL at NA (either trigger); one Recall recording >= 2 → PASS.
