# Release notes — figural pre-transcription (PYQExplain v1.2)

Paste this as the `## <version>` block when you run `seal_release`.
It is deliberately NOT written into `CHANGELOG.md` here: `seal_release` is the
only thing that bumps `VERSION`, and audit_sync compares the changelog's top
entry against `VERSION`. Pre-writing the entry turns that check red.

---

**PYQ-1 lost figural vision partway through long runs and HALTED instead of
degrading — the one place the corpus did not apply its own CLASS T rule.**

**The defect.** `view` is CLASS T (CLAUDE.md EXECUTION-BOUNDARY LAW): it can
only happen between model turns, and an image held in context is not durable.
PYQExplain viewed each figure lazily, at solve time, inside whichever batch
contained it — so the last figural batch asked the image channel for a fresh
render after a clone, a bootstrap, two specs read in full (skill RULE 2), and
every prior batch. Measured in one session on pixel-verified non-blank files:
early views returned perceptible content, later views on the SAME files
returned empty payloads, and a retry did not recover.

Two failures followed. The channel was asked for the same image repeatedly, at
the point of greatest context pressure; and when it failed, §13 had no
sanctioned path onward, so PYQ-1 halted. On a 60-question reference paper with
figures in five of six batches, a session-level tool fault blocked the whole
paper. CLAUDE.md already states that a CLASS T failure must be LOUD and must
NOT halt; vision was the one place that rule was not applied.

**The fix.** New §13A FIGURAL PRE-TRANSCRIPTION PASS at the new preflight step
P2a, in MATERIALISE-THEN-INJECT form. Phase A extracts and role-binds every
figure and emits a work queue; Phase B (prose, never a code block) views each
one in-turn; Phase C verifies and persists. What was seen becomes TEXT on disk
(`pyq_figural_vision.json`), so a figure is viewed exactly ONCE per paper no
matter how long the run or how many resumes it survives, and vision is spent at
the moment context is lightest. Role binding is READ FROM THE DOCUMENT — a
drawing in a paragraph whose text opens with an option label binds to that
option — never inferred from extraction order.

Verification is by measurement, not assumption: OK / MISSING / EMPTY / THIN /
STALE. THIN catches a payload that arrived but says too little to derive from;
STALE catches a transcription written against a different image.

**It never halts.** A shortfall makes the affected question VOID_ITEM and the
run AMBER. BLOCKING is never emitted for a vision condition. A VOID_ITEM takes
the §17-3 anomaly shape, so batch coverage stays exact and the S4-5 guard 3
assertion still holds. Reported in the new §R12, never §R7 — an untranscribable
figure is a session defect with a known remedy, not a fact about the exam paper.

**RE-11 is not weakened.** A figural answer is still derived only from what was
actually seen; "what was seen" is now an auditable artefact rather than an
unfalsifiable claim. A question whose figure was never legibly seen publishes NO
answer, where before it produced a halt at best.

**Also fixed (pre-existing, unrelated).** `mocktestframework_SKILL.md` was not
updated by release 2026.08.03.5 and still claimed 22 specs / 9 engines plus the
pre-retirement auditor wording, while `SKILL.md` had moved to 20. The two skill
files are byte-identical again.

**Files.** New `figural_vision.py` (pure stdlib; Phase A/C only — it models no
tool call and contains no CLASS T stub; SELF-TEST 30/30, with fixtures that fail
on the blank-payload defect it was written for). `Framework_PYQExplain.md`
v1.1.1 → v1.2. `Framework_DeliveryFooter.md` v1.11 → v1.12 (Q0b gains PYQ-1 as a
second producer; F1/F2 shape, Q0, Q1 and all severity routing untouched).
`routes.json` (one line), `gen_manifest.py` TRACKED_PY, `SKILL.md` +
`mocktestframework_SKILL.md` engine count 9 → 10. Bootstrap 31/31 → 32/32.

Zero changes to `explain_engine.py` (62/62 and 10/10 unchanged), the
ExplanationBlock model, the delivered document, §12 byte-identity, or any
existing gate.

---

## Deploy order

Base: `2026.08.03.5`. Every file below is an explicit non-spec deploy except the
two `Framework_*.md`, so `approved_framework` alone will not carry them.

1. Copy all 8 files into the repo root.
2. `python3 gen_manifest.py` → expect `32 files, 20 triggers`.
3. `python3 bootstrap.py` → expect `32/32 ... VERIFIED`.
4. `python3 validate_framework_md.py Framework_*.md` → expect `0 issues`.
5. `python3 figural_vision.py --self-test` → expect `SELF-TEST: 30/30 PASS`.
6. `python3 explain_engine.py --self-test` → expect `62/62` (unchanged).
7. Commit and fast-forward `main:production`.
8. **Reinstall the skill** from the repo's `SKILL.md` /
   `mocktestframework_SKILL.md`. The installed copy at
   `/mnt/skills/user/mock-test-framework/SKILL.md` is stale — it predates the
   Steps 8/10 retirement and still claims 22 specs and names four retired
   triggers. Until it is refreshed, `audit_sync` reports SKILL-INVENTORY
   findings that are about the installed copy, not the repo.
9. `seal_release`, using the block above.
