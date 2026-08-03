# framework-specs — Release Manager Protocol

This repo is the single source of truth for a mock-test framework cloned by ~200 exam
projects. Two branches: **main** = workbench, **production** = what exam sessions clone.
`main` and `production` are kept at the **same commit** (production fast-forwards from main).

You act as the **release manager**. Two deploy commands are defined below. Uploaded files
arrive under the session's uploads directory; match them by filename and copy them into the
repo root before running the gate.

## The safety gate (run for every deploy)
1. `pip install python-docx`   (the validator's embedded self-test imports it)
2. `python3 gen_manifest.py`   (rebuilds MANIFEST.json from the files on disk)
3. `python3 bootstrap.py`      → must print `N/N ... VERIFIED` (every tracked file; currently
   **32/32** — 20 `Framework_*.md` + 12 engines. The count moves when a spec/engine is added or
   retired; Steps 8 and 10 were retired in 2026.08.03.5, taking 2 specs with them, and
   `figural_vision.py` was added in 2026.08.03.6.)
4. `python3 validate_framework_md.py Framework_*.md` → must print `0 issues`
   This includes the CORPUS-level checks (AA routes/skill sync, AB thin-core purity,
   AC aggregator single-exit, AD emitted-class documented, AE normalization conformance).
   They are part of the gate, not commentary appended after it. The BATCH-level
   checks (T, U, AF deliverable-filename contract, AG shared-artefact readers) are part
   of it too.

(`MANIFEST.json`/`bootstrap.py` track the framework files a session clones (count = MANIFEST.json "files"). `SPEC_MANIFEST.json`
is the separate, wider workbench baseline — currently 42 files, including the audit and
tooling scripts. It has NO generator in the repo: the release manager refreshes the changed
entries from disk at deploy time, after checking the entry-builder reproduces every
unchanged entry byte-for-byte. Both must be clean.
Its entry convention was aligned to gen_manifest's in 2026.08.03.5: `lines` is
`len(text.splitlines())` (NOT `split('\n')`, which is one higher), `end_sentinel` is the last
non-empty line `.rstrip()`ed with leading indentation PRESERVED, and `.py`/`.json` entries now
carry `version_header`/`end_sentinel` too. Rebuilding with the pre-08.03.5 convention rewrites
every entry.)

If any step fails: **STOP, show the error in plain words, push nothing.**

**A red check is never advisory.** `validate_framework_md.py` must print `0 issues` before any
push. If a check is judged wrong, FIX OR REMOVE THE CHECK in its own commit with a stated
reason — never ship past it, and never treat a corpus-level check as lower priority than a
per-file one. (GAP-2026-07-25-001: Check AA had been reporting `reconcile_taxonomy.py` as
unrouted, and release `2026.07.25` shipped anyway. The P0 that release carried — a `return`
that silently disabled three taxonomy checks for every current-generation exam — was found by
a live run, not by the gate that was already red about the same file. A check that can be
shipped past is decoration.)
Remove the `.verified` runtime token after bootstrap (it is gitignored anyway).

## Command: `approved_framework <name1> [name2 ...]`
Deploy ONLY the named files. Names are **exact stems** of `Framework_<name>.md`
(case-insensitive) — e.g. `MockDeliver` → `Framework_MockDeliver.md`; `MockTestExplain`
matches only that file, never `...Audit`.

Steps:
1. Copy each named uploaded file into place.
2. Run the safety gate (above).
3. Guards — STOP and report if any of these hold, add nothing:
   - a name matches no `Framework_*.md` file;
   - a named file has no changes;
   - **any changed spec is NOT in the named list** (a stray un-named edit would make the
     regenerated MANIFEST.json describe a file we aren't committing → bootstrap fails on the
     freshly-cloned production repo).
4. If all pass: `git add <named files> MANIFEST.json` → `git commit -m "update <files>"`
   → `git push origin main` → `git push origin main:production`.
5. Confirm both branches are at the same commit and report which files went live.

`approved_framework` with **no names** → deploy nothing; ask which files.

### Non-spec files (routes.json, engines, validator)
`routes.json`, `validate_framework_md.py` and every engine `.py` are NOT `Framework_*.md`, so
`approved_framework` STOPs on them. Deploy them only on an **explicit** instruction
("deploy reconcile_taxonomy.py, routes.json"). For the engine `.py` files, also run their own
self-tests before pushing (integrity checks can't catch a logic regression — checksums prove
the bytes are the intended bytes, never that the code is reachable):
- `python3 explain_engine.py --self-test` and `--self-test-audit`
- `python3 explain_audit_gate.py --self-test`
- `python3 blueprint_core.py --self-test`  (shared allocation core for MockBlueprint + ScopedBlueprint)
- `python3 paper_pipeline.py`  (shared naming/numbering/registry plumbing for Steps 6-11 + Test* triggers)
- `python3 reconcile_taxonomy.py --self-test`  (S4-0 — its output LOCKS a taxonomy)
- `python3 corpus_io.py --self-test`  (corpus I/O shell)
- `python3 figural_vision.py --self-test`  (Phase A/C of PYQExplain §13A figural pre-transcription)

An engine whose output locks or gates an artifact MUST have a self-test, and that self-test
MUST contain a fixture that fails on the defect it was written for. A regression test that
passes on the broken code tests nothing.

#### Where engines actually load from — the repo, not the project
`mocktestframework_SKILL.md` Step 0 clones the repo to `$FW` and does `cd "$FW"` before
anything runs, so the clone is the working directory and a bare `import reconcile_taxonomy`
resolves there. **No spec and no engine ever places `/mnt/project` on `sys.path`** (verified by
grep across the whole corpus), and `mocktestframework_SKILL.md` states the rule directly: the
specs and engine scripts live ONLY in the central repo.

`/mnt/project` holds the exam's DATA — `blueprint.json`, `registry.json`, `taxonomy_draft.json`,
`approval_record.json`, per-exam config and output documents. It is not an import source.

Therefore: **a fix pushed to `production` reaches all ~200 exam projects on their next clone.**
No per-project engine provisioning is required, and none should be performed — a `.py` copy
sitting in an exam's Files section is never imported, so editing one produces no effect while
looking like a fix. (Pre-2026-07-25 this file claimed the opposite: that specs load engines from
`/mnt/project` and hard-stop if absent, and that the repo copy is "not the one the steps import
at runtime". That was false in both directions and, acted upon, would have turned every engine
fix into a 200-project manual migration with no way to tell whether it had taken.)

##### The one mechanical exception: standalone scripts (2026-08-01)
The rule above is correct, and it rests on `cd "$FW"` putting the clone on `sys.path`. That
holds **only for code Python reads from stdin** — spec-inline `python3 - <<EOF` gets
`sys.path[0] == ''`, which resolves to the cwd, i.e. `$FW`. Every ordinary engine consumer
works this way.

It does **not** hold for a standalone `.py` executed by path. Python sets `sys.path[0]` to the
**script's own directory**, never the cwd, so `python3 /home/claude/X.py` puts `/home/claude`
on the path and leaves `$FW` off it *even when the cwd is `$FW`*. Verified empirically in both
directions.

Two consumers run that way, and both already handle it the same correct way — by **copying the
engine out of `$FW` into their own working directory**:

- `Framework_Blueprint.md` §S1-2b copies `blueprint_core.py` from `/tmp/fw` before Step 1 runs.
- `Framework_MockTestCreate.md` copies `blueprint_core.py` + `figural_core.py` from
  `$FW` before running `[ExamCode]_mock_test_audit.py` (v2.12.1; moved here from the
  retired Step 8 on 2026-08-03).

This is not a counter-example to the rule — it preserves it. The copy is taken from the fresh,
bootstrap-verified clone at session time, so the engine is current by construction and a
production push still reaches every exam on its next clone. What remains forbidden is sourcing
that copy from `/mnt/project`, which would create a second, unverified per-exam copy that can
silently go stale.

**Missing this exception is what produced GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING**: the
auditor's `A-FIGPROFILE` gate was written to delegate to `blueprint_core`, the delegation was
recorded in its comments and call sites, and the import was never added — because in the
environment the change was reviewed in, a bare import appeared to resolve.

## Command: `seal_release`
Stamp a clean version + changelog over everything shipped since the last seal.
1. New version from `VERSION` + today's date: if today > VERSION → today's date; if VERSION
   is already today's date → append/increment a numeric suffix (`2026.07.11` → `.1` → `.2`).
2. Write a dated `## <new-version>` block at the top of `CHANGELOG.md` from the commits since
   the last version bump.
3. Run the safety gate (the new version appears in the manifest + bootstrap banner).
4. If all pass: `git add VERSION CHANGELOG.md MANIFEST.json` → commit → push main → push
   main:production → confirm both at the same commit and report the new version.
5. If there are no new commits since the last seal, say so — do not cut an empty release.

`seal_release` is the ONLY thing that bumps `VERSION` (satisfies "bump only when asked").

## Standing guardrails
- **EXECUTION-BOUNDARY LAW — a tool call cannot happen inside a running Python process.**
  Every operation in a spec is exactly one of:

  | Class | Definition | May Python execute it? |
  | :-- | :-- | :-- |
  | **DETERMINISTIC** | parsing, regex, counting, file I/O, arithmetic | yes |
  | **CLASS J** | model judgment over data ALREADY in context | yes, as a reasoning step |
  | **CLASS T** | requires a TOOL CALL — `view`, MCP connector, web fetch | **no** |

  A CLASS T operation **MUST NOT** be called from inside a Python execution block, and
  **MUST NOT** be modelled as a Python function, callback, or parameter. A tool call can
  only occur BETWEEN model turns; a Python process launched from bash runs to completion
  and cannot suspend mid-loop, emit a tool call, receive the result, and resume. Python
  that "calls" a tool is unreachable code returning a default forever, on every run.

  CLASS T uses **MATERIALISE-THEN-INJECT**:

      PHASE A (python)  prepare inputs, emit a WORK QUEUE to disk
      PHASE B (model)   perform the tool calls IN-TURN, write results to disk
      PHASE C (python)  consume the results and continue deterministically

  Phase B is **prose in a plain, unlabelled fence — never a ```python block**. The urge
  to "implement" a Phase B section is the bug, not the fix.

  Every model-agency stub carries `# CLASS: J` or `# CLASS: T`. Enforced by
  `audit_callgraph.py` check **C6**, which scans EVERY fence rather than only
  python-labelled ones — the two Drive stubs that carried this defect for months lived
  in an unlabelled prose fence and were invisible to every static tool in the corpus.

  **A CLASS T failure must be LOUD, and must NOT halt.** These are separate properties
  and the corpus conflated them. Drive and vision had the IDENTICAL defect; Drive was
  worked around for months and vision was not, purely because a Drive failure blocks
  visibly (no papers, no output) while a vision failure leaves an empty field. The
  variable was never the pattern — it was the OBSERVABILITY of the failure. So Phase C
  must never raise, never halt, and always complete; the gap is reported by a FAIL-severity
  check and an amber footer. Silence is the defect; a halt is not the remedy.

  (GAP-2026-07-26-003: `analyse_image_claude()` was a `pass` stub whose return value the
  calling loop immediately consumed — it raised `AttributeError` if executed literally, so
  every production run silently executed some SUBSTITUTED body. Measured on a 22-paper
  corpus: the four vision fields present on **0 of 1719** questions, 153/153 figural
  questions `vision_unavailable`, 45/45 FIGURAL subtopics shipping an empty profile,
  QV-9 PASS, and a green "Step Complete" footer.)
- **A measurement with no consumer is not a feature.** If a step computes a value, some
  step must READ it, and that reader must be named in the same commit. Step 5 measured
  object types, transformations, arrangements and complexity for every figure from v2.29
  onward; Step 7 read only `image_role`, so the semantic half was written and consumed by
  nothing for six minor versions. Check C5 exists for exactly this shape and could not see
  it, because the fields were serialised into `section_rules.md` as prose rather than held
  as dict keys — so C5's "written but never read" test never applied. When a value crosses
  an artefact boundary as TEXT, C5 is blind and the reader must be verified by hand.
- **A deliverable RENAME or CARDINALITY change is a cross-step contract change, never a
  docs-only edit.** Changing any `[ExamCode]_<n>.<ext>` — its name, or how many of them
  there are — requires, in the SAME commit:
  (a) every consumer's discovery pattern re-tested against the new literal name;
  (b) every consumer's PARSER re-tested against the new file SHAPE — a cardinality change
      (N files → 1) breaks parsers that never mention the filename at all;
  (c) Check AF and Check AG green.
  A changelog assertion that downstream consumers are unaffected is not evidence.
  (GAP-2026-07-25-002: PYQAnalyse v2.6 changed both axes and its changelog asserted
  "Cross-step contract unchanged". PYQSort's glob then matched zero files for 19 days,
  and behind that loud failure sat a silent one — its parser delimited subjects by file
  boundary, the exact thing v2.6 removed. Fixing the glob alone would have converted a
  hard stop into silent corpus-wide corruption.)
- **A shared artefact has ONE reader.** If two steps parse the same file, the parser
  belongs in an engine and both steps call it. Four readers of the Analysis doc existed
  simultaneously; three were wrong, and the corpus reported 0 issues throughout.
  Enforced by Check AG and by Check Z, which now owns the ENGINE'S WHOLE public surface
  (it used to start at the `CLUSTER H` marker and so guarded 10 of 40 names — the 30 it
  missed included every taxonomy-parsing function in the framework).
- **A bound that only the consumer enforces is not enforced.** If a value must satisfy a
  constraint to survive downstream, gate it at the PRODUCER. `MAX_HEADING_LEN` lived as a
  bare `100` inside `is_taxonomy_heading()` and nothing upstream checked it, so an
  over-length subtopic name was written, locked, sorted, and then silently stopped being
  a heading — its questions attributed to the preceding subtopic, with zero orphans and
  conservation still passing.
- Never edit or push `production` directly — only the `main:production` fast-forward.
- Never force-push `production` without explicit authorization.
- `.verified` is gitignored and must never be committed.
- These files are NOT tracked by MANIFEST.json / bootstrap: `VERSION`, `CHANGELOG.md`,
  `routes.json` (routes are read into the manifest but the file itself isn't hashed),
  `MANIFEST.json` itself, and this `CLAUDE.md`. Editing them cannot break bootstrap.
- Do NOT create pull requests unless explicitly asked.
