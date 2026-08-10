# Deploy: Math-Integrity Gate — release 2026.08.10.3

**Fixes:** `GAP-2026-08-10-EXPLAIN-MATH-DEGRADE-SILENT` — a `⟦MATH:…⟧` region that
did not compile degraded to raw LaTeX at render and shipped, because the failure
was reported only through `verify_explanations()`'s **return value** (not a raise)
and a self-audit consumed only whether the call raised.

**Exam-independent:** the fix is pure Tier-3 grammar / verifier plumbing. No exam,
subject, or value appears anywhere in the change. It protects all ~200 exams and
**both** pipelines (PYQExplain and MockTestExplain) because both drive the same
`explain_engine.py` (MANDATE A).

---

## What changed

1. **`explain_engine.py` — the permanent mechanical fix (load-bearing).**
   `ExplanationBlock.validate()` now compiles every `⟦MATH:…⟧` region through
   `t3_compile` and **raises `ValueError`** on any `MathCompileError`. A malformed
   region fails at *construction*, before any docx exists, so it can never reach
   the renderer or degrade. `validate()` is the one universal chokepoint (called on
   every block, every step, both pipelines, all exams) and it raises — no producer
   harness can bypass it. Only `⟦MATH:…⟧` is compiled; `⟦M:<base64>⟧` preserve
   tokens are untouched. Engine self-test unchanged: **62/62 PASS**.

2. **`Framework_PYQExplain.md` → v2.4** — documents the authoring-time gate
   (§S5-2, §S11-1, new §S11-1a) and adds an explicit **BLOCKING** contract plus a
   literal HARD-STOP gate (§S18-1, new §S18-1a): a run must assert
   `ok is True AND problems == [] AND T3_STATS['failed']` is empty; a non-empty
   degrade ledger forbids `present_files`. Header + END sentinel bumped to v2.4;
   `SHARED_RULES_VERSION` → 1.1.

3. **`Framework_MockTestExplain.md` → v1.22** — mirrors the §18 BLOCKING contract
   and the shared-engine gate note (§S5-2). (This pipeline authors math via the
   explicit helpers and bans LaTeX, so regions are rare here, but the gate and the
   contract apply.)

4. **`VERSION` → `2026.08.10.3`** and **`MANIFEST.json` regenerated** (engine +
   both specs changed their sha256/headers/sentinels).

5. **`SPEC_MANIFEST.json` regenerated** — optional (not read by CI or bootstrap),
   included only to keep the repo fully consistent.

---

## Files to commit to GitHub (branch: production)

| File | Required | Why |
| --- | --- | --- |
| `explain_engine.py` | **Yes** | the fix |
| `Framework_PYQExplain.md` | **Yes** | contract + gate |
| `Framework_MockTestExplain.md` | **Yes** | mirror + parity |
| `VERSION` | **Yes** | release bump |
| `MANIFEST.json` | **Yes** | CI runs `gen_manifest.py` + `git diff --exit-code MANIFEST.json`; a stale manifest fails the build |
| `SPEC_MANIFEST.json` | Optional | repo consistency only |

> Do **not** hand-edit `MANIFEST.json`. It is machine-generated. If you change any
> file after downloading, re-run `python3 gen_manifest.py` and commit the result.

---

## Deploy steps

1. Replace the six files above in your `production` checkout with the ones in this
   folder.
2. Sanity-check locally (this is exactly what CI runs):
   ```bash
   python3 gen_manifest.py
   git diff --exit-code MANIFEST.json      # must show NO diff
   python3 bootstrap.py                     # must print: 39/39 files ... PASS
   python3 validate_framework_md.py Framework_*.md   # 0 issues
   python3 check_triggers.py                # TRIGGERS CONSISTENT
   python3 explain_engine.py --self-test    # SELF-TEST: 62/62 PASS
   ```
3. Commit and push to `production`.

## CI expectation (`.github/workflows/validate.yml`)
`gen_manifest.py` → `git diff --exit-code MANIFEST.json` → `bootstrap.py` →
`validate_framework_md.py Framework_*.md` → `check_triggers.py`. All pass with this set.

## Rollback
Restore the previous `explain_engine.py`, `Framework_PYQExplain.md`,
`Framework_MockTestExplain.md`, `VERSION`, and `MANIFEST.json`
(release 2026.08.10.2), then re-run `gen_manifest.py` and commit.

## How to confirm the fix is live (post-deploy, any exam)
Constructing an `ExplanationBlock` whose `⟦MATH:…⟧` region uses out-of-grammar
LaTeX (e.g. `\tfrac`, `\varepsilon`, `\vec r` unbraced) now raises `ValueError`
at `.validate()` — before any document is built — instead of degrading silently
at render.
