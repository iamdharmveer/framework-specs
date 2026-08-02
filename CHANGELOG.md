# Changelog

## 2026.08.02.9
**A-QNFIRST false-failed every conformant figural paper — and the guard that
existed to prevent it modelled the labels and not the pictures.**

Raised from a live `TestCreateAudit` run reporting `Part A — 48 OK · 0 WARN ·
1 FAIL · exit 1`, with A-QNFIRST naming six questions on a paper that was correct.

**The defect.** `gate_qnfirst` anchors on the last option LABEL and treats anything
after it as a stimulus orphaned ahead of the next `Q.<n>`. An IMAGE option is a bare
label paragraph FOLLOWED BY its picture (R-FIGURAL / G-FIGURAL-COMPOSITE: "problem
image + one separate image per option, bound 1:1 to labels"), so the final option's
OWN picture necessarily sits after the last label. Every `stem_and_options` figural
block in the estate was reported as orphaning a stimulus, while A-FIGCOMP, A-OPTN,
A-OPTUNIQUE and A-DOSSIER — the gates that own that structure — all passed the SAME
block. Two gates, one block, contradictory verdicts: the v2.21 A-DOSSIER signature.

**Introduced by the previous release's own fix.** v2.21.7 moved the anchor from
`OPT_RE` to `OPT_LABEL_RE` to close a real false NEGATIVE (figural blocks were being
skipped entirely — 25 of 60 unchecked on a real paper). The fix was correct; nothing
measured what the newly-visible anchor did to the TRAILING scan. A false negative
became a false positive in one move.

**Severity is not cosmetic.** A-QNFIRST is a FAIL, so exit is non-zero and MANDATE D
refuses to certify — and A-QNFIRST is catalogued CP-fixable, so Phase 1 calls
CP-QNFIRST on a block that has nothing to re-emit. The fix does nothing, Part A
re-runs, still red: an unfixable false failure inside a repair loop. That is the
shape of a multi-day audit that never certifies, and it is what the reporting
operator experienced.

**Fix.** The allowance is MEASURED FROM THE BLOCK, never assumed (RA-9): count the
pictures bound to each NON-FINAL option (between consecutive labels) and allow the
same number to trail the final label. A text-option block measures 0 and behaves
exactly as before, so the genuine orphan catch is preserved at full strength.
Verified on real docx fixtures in both directions — a conformant figural block is
clean; a genuine orphan after the last option image still FAILS as an EXTRA image,
a TABLE, or a 60-word passage. Against the v2.21.8 build exactly ONE case flips: no
over-correction.

**Why no fixture saw it.** v2.21.7's guard "a CLEAN figural block stays clean" builds
four BARE LABELS AND NO IMAGES — a shape v2.21.4 declares a finding in its own right.
The guard that existed to prove a conformant figural block stays clean never once
built the shape R-FIGURAL mandates. EIGHTH hollow-branch occurrence.

**The generalised control — CLEAN-SHAPE MATRIX (fixture 5g) + CHECK AP.** The last
four defects share one shape: a block-structural gate written and fixtured against
the TEXT-option rendering, then meeting a different LEGITIMATE rendering in the wild
(v2.21 A-DOSSIER, v2.21.3 A-OPTORDER, v2.21.7 and now v2.21.9 A-QNFIRST). Each was
closed with a per-gate fixture, which requires an author to ANTICIPATE the shape —
and four times running nobody did. CHECK AN and CHECK AO cannot catch it: this gate
used the shared predicate CORRECTLY and its fixture was NOT tautological.
The invariant that needs no anticipation: A CONFORMANT PAPER IS CONFORMANT IN EVERY
RENDERING THE FRAMEWORK MANDATES. Fixture 5g builds a clean paper in each canonical
shape (text options / IMAGE options / enumerated stem), DISCOVERS every `gate_*` by
introspection, runs all of them over each shape, and asserts ZERO FAILs — naming the
offending shape when it trips. Because gates are discovered and not listed, a gate
written next year is covered with nobody remembering to opt it in. Measured: on the
v2.21.8 build 5g reports the A-QNFIRST FAIL on the clean image-option shape. Only
FAIL is asserted; a WARN on a clean shape stays legitimate. CHECK AP fails the BUILD
if 5g is deleted, loses its shape table, drops a mandated shape, or replaces gate
discovery with a hand-maintained list.

Self-test 142 -> 149. Mutation 27/27 killed, 100%, 0 survivors — budget stays 0.
AUTH_GATE_FLOOR stays 35. No paper changes. No Step-7 changes.

Files: `audit_canonical.py`, `validate_framework_md.py`,
`Framework_MockTestCreateAudit.md` (v2.21.8 -> v2.21.9).

## 2026.08.02.8
**A-FIGTEXT-PROSE assumed English — an RA-9 violation that produced a false
assurance on every non-English exam in the estate.**

Found by auditing for **exam-independence** rather than for correctness. That is a
different question from the one every previous release asked, and it found something
none of them could have.

**The defect.** `gate_images` built its figure-reference detector from a **hardcoded
English regex** that also carried reasoning-exam shape nouns
(triangles/squares/circles/angles/regions). Four sibling language inputs —
`msq_instruction_phrases`, `nat_instruction_phrases`, `figural_cue_keywords`,
`escape_reference_phrases` — are all read from `section_rules` per RA-9. This one was
not, and nothing compared them.

**It was a false assurance, not a miss.** On a non-English paper the pattern matched
nothing, so `A-FIGTEXT-PROSE` printed *"no figure-reference prose in zero-image
blocks"* — a clean OK asserting a property of a paper the detector never examined. A
figural subtopic rendered as **prose** (a figure that was never drawn) was
undetectable on every non-English exam while the report claimed conformance.
Measured: a Hindi stem with figure-reference prose and zero images returns **OK** on
v2.21.7, **WARN** (undeclared) or **FAIL** (declared) after.

RA-9 is explicit: *"Hardcode nothing. A missing value → SKIP the dependent check with
a logged reason, never a hardcoded substitute."*

**Fix.** `section_rules figure_reference_phrases` is now read in `load_sources`, the
same shape as its four siblings, and documented as a CATEGORY-C param. The English
set survives **only** as a default that applies when `language == english`. Any other
language with nothing declared makes the gate report **dormant** — a WARN naming the
reason and the remedy — never OK. Fixtures 53k (English unchanged, both directions),
53l (non-English undeclared is dormant, not OK), 53m (non-English with declared
phrases detects normally and stays clean when absent — both halves).

**Scope re-verified for the 200-exam estate.** Every other exam-varying input is read
from source: `language`, `options_count`, `option_label_format`, `font_family`,
`marks_per_q`, `negative_marking`, `marking_scheme`, `level`, `medium`, escape
tokens, MSQ/NAT instruction phrases, figural cues, stimulus cues. The MATCH
detector's `_MT_PAIR_RE`/`_MT_OPT_RE` are **structural** (label-pair shapes), not
lexical, so they are language-independent by construction. `A-SCRIPT` is already
language-conditioned. No exam **name** appears in any engine outside illustrative
comments.

Self-test **139 → 142**. Mutation stays **100% / 0 survivors**. Spec → **v2.21.8**.
`AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7 changes.

## 2026.08.02.7
**The last two OPT_RE consumers closed; the predicate split is now structurally
impossible. Plus a corpus-wide header and count sweep.**

**SEC-1 — real defect, measured.** `gate_qnfirst` anchored on `OPT_RE`, which cannot
see a bare-label image option. On every figural block `last_opt` stayed `-1` and the
`continue` **skipped the whole check**, while the gate still printed `ok` — so the
shortfall was invisible: 25 of 60 blocks unchecked on a real paper. Measured both
ways: an *identical* orphaned lead-in was **caught** after a text block and
**missed** after a figural one. Now on `OPT_LABEL_RE`. Fixture 5a asserts the two
are at parity; 5b guards that a clean figural block stays clean.

**SEC-2 — consistency, stated honestly.** `gate_optref` read `option_paras()`, also
built on `OPT_RE`: on a figural block it reported **one** option where **four** are
rendered. The wrong verdict this enables — a figural stem whose escape option is
itself an image — is rare, and no wrong verdict was observed on the common shapes.
This is hardening, not a demonstrated live bug, and fixture 5c asserts the **count
parity** (always present) rather than a verdict (usually absent).

**Predicate split retired.** With both consumers moved, `option_paras()` had no
callers and `OPT_RE` had no wrapper. Both **deleted**. A second option predicate kept
alive with no caller is drift waiting for an author — the next person needing "the
options of a block" would have found two helpers and picked one. There is now exactly
**one** option-label predicate in the file, so the divergence class behind
`GAP-2026-08-02` is impossible by construction rather than merely absent. `CHECK AN`
still guards reintroduction.

**SEC-3 — message only; the producer is correct.** `A-FIGPROFILE` printed
"pre-v5.31 mock" on modern v5.34+ output. Step 7's writer is right: it deliberately
**omits** `object_types` per question when the profile mode is `unconstrained`, so an
empty map is *expected*, not legacy. The message misattributed it and sent operators
hunting a producer fault that did not exist. Reworded to state both causes and assert
neither.

**D2 (FigureSpec transport) — already closed; no change needed.** Verified against
your live registry: `figure_specs` carries **57** entries on mock 1, written by Step 7
into `registry.figural_manifests[].figure_specs` and read by the auditor. The
carry-forward was stale.

**§16 glossary completed.** Twelve `A-FIG*` gates plus `A-OPTLABEL`, `A-NAT-*`,
`A-MSQ-INSTR`, `A-KBAL`/`A-KPAT` had Step-7 twins but no mapping row. Added — along
with an explicit **STEP-7-ONLY** list (allocation-time and key-dependent gates that
are genuinely not machine-checkable from a delivered docx), so §16's claim that Step 8
re-verifies "every machine-checkable Step-7 contract" is true as written rather than
silently incomplete.

**`Framework_Blueprint.md` → v1.42.8.** Five **live** normative sites still quoted
"the v2.13 canonical build prints 107/107" as the expected auditor count — stale twice
over and version-misattributed. Refreshed to 139/139, each now stating that the count
is informational and `AUTH_GATE_FLOOR` is the binding condition, so the next count
change needs no sweep. Historical changelog lines left exactly as written.

**`Framework_MockTestExplainAudit.md` header repaired (v1.16.1).** Its line 1 read
`# Framework_MockTestExplainAudit.md` — carrying the file extension and **no version
at all**, unlike every other `Framework_*.md`. `MANIFEST.json` recorded that string
verbatim as the `version_header`, so bootstrap compared it to itself and passed, and
`CHECK C`'s header-vs-footer comparison had nothing to compare: the file was
version-pinned to a value containing no version. The version is taken from the file's
**own end-of-file marker** (`v1.16.1`). Worth recording: a first attempt used `v1.15`
from a cross-reference in `Framework_MockDeliver.md`, and **`CHECK C` rejected it**
against the footer — the check this repair restores caught the repair's own error on
the first run. Content untouched.

**`Framework_DeliveryFooter.md`** line-1 title normalised to the corpus convention.

Self-test **136 → 139**. Mutation stays **100% / 0 survivors**. Spec → **v2.21.7**.
`AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7 changes.

## 2026.08.02.6
**Mutation score 100%. Zero survivors. Ratchet lowered to 0 — absolute from here.**

The last seven untested findings closed in one release. Every finding
`audit_canonical.py` can emit is now provably detected by at least one fixture:
deleting **any** of the 27 finding emissions turns the self-test red.

**A-NAT-GRADE (3).** Fixtures 35/36 covered only the mismatch case and the happy
path. Missing `nat_value`, missing `nat_grading_value`, and a re-derivation that
**raises** were all deletable with every test green. This gate guards the exact
string the delivery portal ingests to **auto-grade** a numerical question, so a
silent failure here means **wrong marks**, not a wrong-looking paper — the same
severity class as the v2.21.3 A-OPTORDER anchor defect. Reachability note found
while writing the fixture: an *entirely empty* answers map makes the gate dormant by
design (Step 8 receives no key unless `--key` is supplied), so the reachable defect
is a **partial sidecar** — answers present, this question's value absent. The fixture
asserts that shape.

**A-ZIP (2).** Both failure modes were untested: an rId with **no relationship
entry**, and an rId whose relationship points at a part **not in the archive**. A
docx failing either is structurally broken and its images silently vanish in Word.
Both halves asserted plus the clean case, so neither can be "achieved" by making the
gate fire always.

**A-SECCOUNT (1).** The gate proving each section holds the number of questions its
`q_range` declares had no fixture at all. Matching-count guard included.

**restore_checkpoint (1).** `CK-tamper-refused` covered a member whose *content*
changed (hash mismatch); a member **listed in the manifest but missing from the
archive** had none. A truncated bundle is the likelier real-world corruption
(interrupted upload or copy) and must be refused **before anything is written to
disk**, never resumed onto a half-restored evidence set.

Self-test **130 → 136**. Survivors **7 → 0**; score **74.1% → 100%**. §21 ratchet
budget **lowered to 0** — from this release the gate is absolute: any new finding no
fixture can detect fails the build. No inherited backlog remains.

**Honest scope.** A 100% mutation score means every finding *emission* is covered. It
does **not** mean the gates are correct. A gate can be provably-fires-when-it-should
and still encode the wrong rule — which is exactly what the v2.21.3 (A-OPTORDER
unanchored), v2.21.4 (A-FIGCOMP dead branch, partial figure sets) and v2.21.5 (ND10
figural-NAT) defects were. Those were found by reading the **producer contract**, not
by mutation. Both controls are necessary; neither is sufficient.

Spec → **v2.21.6**. `AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7
changes.

## 2026.08.02.5
**Includes the ND10 figural-NAT correction (spec v2.21.5), caught in review before
deployment.** See the ND10 section at the end of this entry.

**A-FIGCOMP had a dead branch and accepted partial figure sets. Two real defects,
both on the figural path that every image-based paper in the estate travels.**

Found by working the `audit_mutation.py` backlog. `gate_images` carried **seven**
surviving mutants — *every* finding it emits could be deleted outright with all 120
fixtures still green. The gate owning A-FIGCOMP and A-MATHRASTER had no fixture that
could detect it going silent. This is the **third consecutive gate** where closing a
coverage gap exposed a live bug.

**Defect 1 — dead branch.** `if not block_imgs: ... continue` sits *above* the
`stem_only` arm, so `if len(block_imgs) < 1: composite.append('stem_only:0img')`
could never be true — unreachable code. A registry-declared figural question that
rendered **zero images** passed A-FIGCOMP clean (a figure that was never drawn),
unless its stem happened to match the `_fig_ref_re` prose pattern. Detection depended
on the **wording of the stem** rather than on the **absence of the figure**. Fixed by
testing the condition before the `continue`. Membership comes from the **registry set
only**, never from `figural_cue_keywords` — that list holds ordinary MCQ phrases
("which of the", "series", "complete the"), so applying it to zero-image blocks would
false-FAIL a large share of ordinary text questions estate-wide. Fixture 53f locks
both halves.

**Defect 2 — partial figure sets accepted.** Step-7 `G-FIGURAL-COMPOSITE` requires,
for `stem_and_options`, "problem image + one separate image per option" — `oc+1`
images. The check was `if len(block_imgs) == 1`, so a block rendering 2, 3 or 4
images — a problem figure with its **option figures silently undrawn** — passed
clean. Only the degenerate 1-image case was caught. A candidate cannot answer a
question whose option figures were never rendered. Fixed to `len(block_imgs) < oc+1`,
with the count now reported in the finding.

Verified on the real 60-question IIT_JAM_BIOTECHNOLOGY paper (57 drawings): the
flagged question set is **identical** before and after — only the diagnostic detail
is richer. Fixture 53g locks it; 53a guards the canonical set staying clean.

**Fixtures 53a-53h** added (canonical guard, math-token name, non-canonical name
warn, two-images-per-line, figure-reference prose, dead-branch lock, partial-set
lock, options_only short set). `gate_images` now scores **100% (7/7 killed)**.

Self-test **120 → 128**. Engine-wide survivors **14 → 7**, mutation score
**48.1% → 74.1%**. §21 ratchet budget **lowered to 7**. Three gates now at 100%:
`gate_dossier`, `gate_options`, `gate_images`.

Spec → **v2.21.4**. `AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7
changes.

### ND10 correction (spec v2.21.5) — figural-NAT must skip the per-option-image arm

Caught in **review, before deployment**, by a reader checking the change against the
**producer contract** rather than against its own fixtures.

Create.md `R-FIGURAL` v4.7 **FIGURAL-NAT VARIANT (ND10)**: a figural question whose
subtopic is `answer_type=='numerical'` has a problem image (or *series* images) but
**zero option images** — "there are no options to decompose" — and
`G-FIGURAL-COMPOSITE` "must skip its per-option-image arm" for it. ND10 states in
terms that without the variant "a valid figural-NAT would be hard-stopped for missing
option images".

`gate_images` had **never read that signal**. v2.21.3 and earlier already
false-flagged a **single-image** figural-NAT via the `len(block_imgs) == 1` arm — a
pre-existing defect. Tightening that arm to `< oc + 1` (Defect 2 above) **widened**
the same false positive to every 2..oc-image figural-NAT series. It is a WARN, so no
paper hard-stops, but it routes a human to "VIEW + fix in Part B" a paper that is
**correct** — the most expensive kind of wrong answer an auditor can give.

**The signal must be `options_by_q`, not `concept_map`.** The existing
`nat_subtopic_ids` mapping requires `concept_map`, and `load_sources` sets
`concept_map = {}` on any run without a dossier or `--key` — its own comment says
"otherwise empty dict (gate_images falls back to default
image_role='stem_and_options')". So on a plain run the NAT mapping silently does not
fire and the figural-NAT lands in exactly the arm that was tightened. `options_by_q`
travels in the registry (ND6), which Step 8 always receives, and is the same signal
`gate_options` has always read. One shared NAT signal, per S5-2 "one structural
question, one answer".

**Scope:** the per-option-image arm only, in both `stem_and_options` and
`options_only`. ND10 still requires ≥1 problem image, so a figural-NAT rendering
**zero** images remains a finding.

Measured across both builds — N1 single-image figural-NAT: production WARN → **OK**;
N2 three-image series: would have become WARN → **OK**; N3 zero-image figural-NAT:
production OK → **WARN** (correctly detected); N4 the same 3-image block when the
registry does *not* mark it NAT: **WARN** (still caught).

**Fixtures 53i** (both halves — the same 3-image block is OK when the registry marks
it NAT and a finding when it does not, so the fix cannot be "achieved" by disabling
the arm) **and 53j** (zero-image guard). Self-test **128 → 130**. `gate_images` stays
at **100%** (7/7 killed).

## 2026.08.02.4
**A-OPTORDER did not enforce its own documented contract. Options labelled 2,3,4,5
certified clean — and every answer key on such a question is wrong.**

Found by working the `audit_mutation.py` backlog. `gate_options` carried two
surviving mutants (`bad_lab`, `bad_ord`), meaning **A-OPTLABEL and A-OPTORDER — which
police option labelling on every question of every paper in the estate — had no
fixture that could detect them going silent.** Only A-OPTN and A-OPTUNIQUE were
covered. Probing that uncovered space to write the fixtures surfaced a real defect,
which is the whole point of the exercise.

**The defect.** This gate's S5-2 row has always read "options appear in document
order 1..OPTIONS_COUNT". The check was `idxs != list(range(idxs[0], idxs[0] + oc))`,
which accepts **any consecutive run**. A block labelled `2,3,4,5` passed A-OPTORDER
*and* A-OPTLABEL and certified CLEAN. The engine was weaker than its own documented
contract and nothing compared the two — the same producer/consumer divergence class
as `GAP-2026-08-02`, this time between a gate and its own spec row.

**It is not cosmetic.** A-KINT derives the key as an int in `1..OPTIONS_COUNT`. On a
paper labelled 2,3,4,5 the key "option 1" refers to an option that **does not
exist**, and keys 2..oc each point one place off — **every answer for that question
is wrong on the delivered paper**, with no gate objecting. A zero-start set
(`0,1,2,3`) was caught only incidentally, by the separate `0 in idxs` clause.

**Fix.** `idxs != list(range(1, oc + 1))` — anchored at 1, not merely consecutive.
`_idx_of()` normalises all three label families to 1-based (num `1..`, alpha `a=1..`,
roman `i=1..`), so the anchor is family-agnostic and no legitimate
`option_label_format` starts anywhere else. Verified on the real 60-question
IIT_JAM_BIOTECHNOLOGY paper: all four option gates unmoved.

**Fixtures 4a-4e** added — mixed family, family-vs-format mismatch, out-of-order, the
**anchor lock**, and a three-family canonical guard so the fix cannot be "achieved"
by rejecting everything. `gate_options` now scores **100% (4/4 killed)**.

Self-test **115 → 120**. Engine-wide survivors **16 → 14**, mutation score
**40.7% → 48.1%**. §21 ratchet budget **lowered to 14** — it may never be raised.

Spec → **v2.21.3**. `AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7
changes.

## 2026.08.02.3
**Mutation testing made mechanical. Three hollow branches closed in A-DOSSIER —
including half the Tier-A cross-check, unverified since v2.17.**

Answer to "is there a more robust way to prove Step 7 and Step 8 are in sync?"
Yes — and reading the code is not it. This corpus has now shipped **eight** code
paths that no fixture exercises (v2.10, v2.12, v2.13, v2.15, v2.16, v2.20, v2.21,
v2.21.1). Every one was found by a human reading code *after* it shipped, because a
green self-test is exactly what a hollow branch looks like.

**New tool: `audit_mutation.py`** (untracked tooling, alongside `audit_sync.py` et
al — the 33-file tracked count is unchanged). It neutralises each finding emission
in `audit_canonical.py` one at a time and re-runs `--self-test`. A **surviving**
mutant means no fixture can distinguish a gate that reports that defect from one
that does not.

**First run: 19 of 27 findings survived — a mutation score of 29.6%.** Three were
inside `A-DOSSIER` itself, the gate rewritten two releases ago: both set-mismatch
legs (`absent-from-dossier`, `not-in-paper`) and the **entire `subtopic_id`
vs-registry leg** had never been executed by any fixture. Half of the Tier-A
cross-check was unverified while the release that touched it reported 112/112.

Fixtures **92g/92h/92i** close all three. `gate_dossier` now scores **100% (5/5
killed)**. Self-test **112 → 115**. Engine-wide **16 survivors remain, score
40.7%**, all inherited and each itemised by function in §21.

**Ratchet policy (§21):** the survivor count **must not increase** release over
release — `audit_mutation.py --max-survivors 16` is a release gate. A new gate ships
with fixtures that kill its own mutants, or it does not ship. The 16 inherited
survivors retire one release at a time by lowering the budget, never raising it.

`CHECK AO` catches a tautological fixture *shape*; only mutation catches a finding
that is simply never triggered. Both are now required. This is the first control in
the corpus that finds a hollow branch **without anyone suspecting it is there**.

Spec → **v2.21.2**. `AUTH_GATE_FLOOR` stays **35**. No paper changes. No Step-7
changes.

## 2026.08.02.2
Follow-up to `GAP-2026-08-02-DOSSIER-OPTION-PREDICATE`, found by a line-by-line
Step-7 / Step-8 sync audit of the 2026.08.02.1 release itself. **Two findings, one
of them a regression introduced by that release.**

**1. The A-DOSSIER `nat` leg must never be clamped (REGRESSION FIX).** v2.21 changed
the leg to fire only on a COMPLETE rendered option set (`n_opt >= oc`), on the
assumption that a NAT stem may legitimately enumerate. **It may not.**
`Framework_MockTestCreate.md` **R13** (v4.7 NAT EXEMPTION) gives a NAT question ZERO
option paragraphs — "only the bold Q.<N> stem (carrying the nat_instruction per R14)
and the blank separator". R13 admits no third paragraph class, so an enumerated stem
on a NAT block is an R13 *violation*, not a legitimate shape. The assumption was
never checked against the producer spec — the exact error class v2.21 exists to
remove, committed while fixing it.

It opened a real false negative. With `nat_present=False` and the registry marking
the question 0-option, `gate_options` SKIPS the block (`obq == 0`), `gate_nat` is
DORMANT (`nat_present` false), and the clamped `A-DOSSIER` was silent — so an R13
violation passed **all three gates**. v2.20 caught it. That configuration is
precisely a Step-7 internal inconsistency between blueprint and registry, which is
the one condition `A-DOSSIER` exists to detect. Verified across four
`nat_present` × `options_by_q` configurations: 4/4 caught before, 3/4 after v2.21,
4/4 again now. Fixture 92f is inverted and now locks the false negative.

**2. `A-FIGTEXT-PROSE` was an undocumented live gate.** It is emitted by
`gate_images` (v2.4), prints on every Part-A run, and can `_fail()` and block
certification — yet it had **no catalogue row, no sub-code entry and no glossary
line** anywhere in the audit spec. That is the identical documentation gap that left
an operator with nothing to read when `A-DOSSIER` FAILed. Now carries a full S5-2
row and a §16 glossary line mapped to its Step-7 twin `G-FIGTEXT-PROSE`
(Create.md Tier 3).

Self-test stays **112/112**. `AUTH_GATE_FLOOR` stays **35**. **No paper changes.**
Spec → **v2.21.1**.

## 2026.08.02.1
GAP-2026-08-02-DOSSIER-OPTION-PREDICATE — **A-DOSSIER could not see an image
option.** Raised by a live Step-8 `TestCreateAudit P1` run that HALTED PERMANENTLY
with nothing on the paper to repair.

**What was wrong.** `block_option_count()` was built on `OPT_RE`, which requires a
VISIBLE GLYPH after the option label (`[.)]\s+\S`). An IMAGE option is a BARE label
paragraph (`1.`) followed by a picture paragraph — the glyph IS the picture — so
`OPT_RE` counted every image option as ZERO. `A-DOSSIER` therefore FAILed
`qtype-mcq-but-0!=N-options` on every figural question in the estate while `A-OPTN`,
`A-OPTORDER`, `A-OPTUNIQUE` and `A-NAT-NOOPT` all passed on the SAME blocks. Two
gates, one block, contradictory verdicts — that contradiction WAS the defect. The
function's docstring claimed it used "the same OPT_RE the option gates use"; the
option gates do not use `OPT_RE` at all — they use `OPT_LABEL_RE` via
`_label_paras()`. The docstring encoded a BELIEF about a sibling function rather
than a verified fact about it, and no fixture ever compared the two.

**Not figural-only.** `block_option_count()` also had no trailing-set clamp, while
`gate_options()` takes the TRAILING `oc` labels precisely so an enumerated stem
cannot inflate the count. Every STATEMENT / SEQUENCE / MATCH / ASSERTION_REASON stem
that renders an enumerated list — standard on PURE TEXT papers — false-FAILed
`A-DOSSIER` too. The blast radius was the whole estate, not the figural subset.

**It also produced a FALSE PASS.** Because the same zero vacuously satisfied
`if qt == 'nat' and n_opt:`, a question the dossier records as NAT that actually
SHIPS four image options was ACCEPTED SILENTLY. The gate that exists to detect
"Step 7 recorded something other than what it shipped" was BLIND to that exact
condition for every figural question. One predicate, a false FAIL and a false PASS.

**Fix.** `block_option_count(b, oc)` delegates to the option gates' OWN predicate
(`_label_paras`) and their OWN trailing-`oc` clamp. There is now ONE rendered-option
count in the file and every gate reads it. The `nat` leg fires only on a COMPLETE
rendered set (`n_opt >= oc`), so a legitimate NAT question whose STEM enumerates is
not a finding and `A-DOSSIER` is never more opinionated than `A-NAT-NOOPT`, which
OWNS that fact. Verified on a 14-case shape matrix: 14/14 correct after, 8/14 wrong
before (7 false positives, 1 false negative).

**Fixture 92 was a tautology.** It asserted
`block_option_count(b) == sum(1 for p in b.paras if OPT_RE.match(para_text(p)))` —
the right-hand side is a verbatim re-implementation of the left-hand side's body, so
it CANNOT FAIL FOR ANY PREDICATE. It reported green across v2.17–v2.20 on a build
whose dossier gate could not see a single image option. RETIRED and replaced by six
fixtures: 92a–92d and 92f MUTATION-VERIFIED (measured False on the `OPT_RE` build,
True on this one), 92e a permissiveness guard. Every dossier fixture before this
release was built from `_add_q()`, which emits text options only — no dossier
fixture had EVER rendered a non-text option. Self-test 107 → 112.

**Structural counter-measures (so the class cannot recur).** This was the seventh
hollow-branch occurrence the corpus has recorded, so the answer is mechanical, not
vigilance-based. `validate_framework_md.py` gains **CHECK AN** (shared-predicate
parity — an option count must delegate to the one shared collector, never name a
predicate itself) and **CHECK AO** (tautological-fixture detector — a fixture may
not assert `F(x) == <inline of F's own body>`). Both were verified to FAIL on the
pre-fix build and PASS on the post-fix build, which is the acceptance criterion.

**Spec.** `Framework_MockTestCreateAudit.md` → **v2.21**: `A-DOSSIER` added to the
§S5-2 gate catalogue (it could FAIL and block certification while having no
catalogue row at all); new §S5-2 doctrine **ONE STRUCTURAL QUESTION, ONE ANSWER**;
four new §17 operator playbook rows (the discriminator is `A-OPTN` — if it is `ok`
on the same questions, the paper is correct and the gate is wrong); §16 glossary
entry; §21 propagation row mandating a discriminating, mutation-verified fixture per
BLOCK SHAPE for every new gate.

**Estate impact.** NO PAPER CHANGES. Papers produced by Step 7 v5.35+ are correct;
they were only mis-audited. Step 7 requires NO change — `qtype` derivation and the
dossier writer were both verified correct. `AUTH_GATE_FLOOR` STAYS AT 35, so v2.11
(51/51), v2.12 (61/61), v2.13 (107/107) and v2.21 (112/112) copies all coexist and
the estate migrates exam by exam with zero downtime.

## 2026.08.01.11
GAP-2026-08-01-DEAD-PARAMETER — **one third of the dossier identity triple was
never checked.** Found by a line-by-line producer/consumer audit of Steps 7 and 8,
by RUNNING the edge-case matrix rather than reading it.

**What was wrong.** `load_dossier()` has accepted an `exam` argument since v2.17,
and S0-1 item 7b documents the binding as exam_code / mock / paper_md5. The call
site passed `docx_path` and `mockN` and **never passed `exam`** — so the exam_code
leg never executed, and a dossier built for another exam was ACCEPTED. Verified
empirically: the wrong-exam case returned 60 questions before v2.20 and is REFUSED
after.

**Severity, stated honestly.** Unreachable in practice: `paper_md5` is checked, and
a different exam's paper cannot share this paper's hash, so the md5 leg would have
caught it. This was defence-in-depth with one layer unwired, not an open door. But a
documented binding that never executes is the same dead-parameter class this corpus
keeps rediscovering — v2.10 (`bc` bound nowhere), v2.13 (`Block.images` never
populated), v2.17 (`--dossier` never passed) — and the point of a triple is that no
single leg is load-bearing alone.

**Fix.** `load_sources()` passes `exam=blueprint.exam_code`, the authority P2 already
asserts equals the trigger (RS-5). Fixture 90 now checks BOTH that the leg refuses a
wrong exam AND that `load_sources` actually supplies it — because a working check
nobody calls is not a check, which is exactly how this and the v2.17 defect both
survived. Mutation-verified: unwiring the argument fails the fixture.

**FULL STEP-7 / STEP-8 SYNC AUDIT — what else was checked and found clean:**

| Contract | Result |
|---|---|
| Dossier field names (`_FACTS` vs `DOSSIER_FACT_KEYS`) | 10/10 identical, no drift either way |
| Dossier top-level keys (producer vs consumer reads) | complete; nothing read that is not written |
| Registry `figural_manifests` keys | `object_types` / `subtopic_ids` / `figure_specs` written and read; §13 re-sync carries all forward |
| Filenames (docx / registry / dossier) | identical construction on both sides; `paper_slug` shared |
| Variable scope at every injection point | `N` bound at P0 line 1175, used line 1285; `N`/`paper_slug` in scope at S13-4b and S13-7 |
| Version cross-references | all are capability markers ("v5.34+ delivers"), correctly historical |
| Input-count claims | none hardcoded; nothing to drift |
| Edge-case matrix | 10/10 correct (see below) |

**Edge cases re-verified end to end:** happy path ACCEPTED; paper regenerated after
the dossier was written, wrong mock, wrong exam, future schema, smuggled judgment
key, empty questions, truncated file, and absent md5 binding all REFUSED with a
named reason; absent dossier degrades to the legacy WARN and the audit continues.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.19 ->
**v2.20**; `CHANGELOG.md`; `VERSION`; `MANIFEST.json`.

 2026.08.01.10
GAP-2026-08-01-FLAG-NOT-INVOKED — **THE DOSSIER WAS DELIVERED, STAGED, AND NEVER
READ.** A regression introduced by 2026.08.01.7 and shipped through two further
releases.

**What broke.** v2.17 declared the Tier-A dossier as a delivered input (S0-1 item
7b) and `audit_canonical.py` grew a `--dossier` flag to consume it. **No documented
invocation passed the flag.** S5-1 and the Phase-3 command both omitted it, and P0
never staged the file at all. Step 7 would write the dossier, the author would
upload it, and the auditor would ignore it — every benefit silently lost while every
gate reported clean: `A-NAT-GRADE` dormant, `image_role` defaulted, `A-FIGCOMP`
reporting 27 findings where 7 are real.

**This is the exact defect the dossier exists to repair, one layer up.** The original
finding was: Step 7 writes `concept_map`, `audit_canonical.py` has a `--key`
consumer, and nothing connects them. v2.17 fixed that and immediately recreated it —
spec declares the input, engine exposes the flag, no invocation wires them.

**Why nothing caught it.** Every auditor passed, twice, across three releases. The
wiring existed only as an assumption. It surfaced because the paper's author asked,
in plain language, what `--dossier` meant.

**The fix.**

- **P0 stages the dossier** when present, and prints which branch it took — so the
  operator sees "staged" or "not found" rather than inferring.
- **S5-1 and the Phase-3 invocation both pass `--dossier`** when P0 staged one. The
  Phase-3 run is the one that CERTIFIES; a dossier consumed in Phase 1 and dropped
  there would certify against different facts than were audited.
- **New `validate_framework_md.py` CORPUS CHECK AM — CLI FLAG INVOCATION PARITY.**
  Fails the build whenever a spec declares an input, an engine exposes a flag for
  it, and no documented invocation passes it. Also fails the inverse: a flag with no
  declared input is either dead code or an undocumented dependency.

**Verified:** AM reports 0 issues on the corrected corpus, and flags the defect when
the `--dossier` lines are stripped from the invocations.

**Operator signal:** `A-DOSSIER` prints its consumed/not-consumed verdict on every
run. If it says "no Tier-A dossier consumed" while the file exists in
`/home/claude`, the invocation is wrong.

**The lesson, stated plainly because it has now cost three releases:** a wiring
instruction written only in prose is not wiring. Checks AL and AM exist because
single-file auditors cannot see contracts that span a step boundary.

**Files:** `Framework_MockTestCreateAudit.md` v2.18 -> **v2.19**;
`validate_framework_md.py` (CHECK AM); `CHANGELOG.md`; `VERSION`; `MANIFEST.json`.

 2026.08.01.9
GAP-2026-08-01-DELIVERY-SET-DRIFT — **STEP 7 HARD-STOPPED AT PRE-DELIVERY ON EVERY
EXAM.** A regression introduced by 2026.08.01.7, caught before any run.

**What broke.** v5.35 added the Tier-A audit dossier as a THIRD delivered file
(S13-4b) for Step 8's benefit, and did not widen S13-7 check 6, which asserted
`staged == {docx_name, reg_name}` — a hardcoded set of two. The extra file made the
comparison false, S13-7 raised `SystemExit`, and **Step 7 could not deliver at all**,
on every exam and every mock. It would have failed on the first run after deployment.
Step 7 had been the one step in this pipeline that never failed; an improvement made
for Step 8 broke it.

**Why nothing caught it.** All six auditors reported zero findings, twice, plus a
fresh-clone deployment simulation — and they still would have. **Nothing anywhere
cross-verified the Step-7 closed deliverable set.** It was stated in prose at four
sites and asserted in code at one, with nothing binding them together. Check AK
guards the Step-6 B3 bundle, a different contract. This is the familiar "rule stated
in prose with no machine check behind it" class, this time spanning a STEP BOUNDARY
rather than sitting inside one file — which is why every single-file auditor missed
it.

**The fix.**

- S13-7 check 6 now **DERIVES** the expected set from what was actually staged —
  docx + registry always, dossier when S13-4b wrote one — instead of hardcoding a
  count. A producer change and the gate that guards it can no longer disagree by
  construction. Verified across all three cases: 2-file (legacy), 3-file (v5.35+),
  and 3-file-plus-stray (correctly rejected).
- R-DELIVER, G-DELIVERY-SET and the §13 staging prose corrected in lockstep.
- **New `validate_framework_md.py` CORPUS CHECK AL — STEP-7 DELIVERY-SET CONTRACT.**
  Fails the build if any site hardcodes the set or states a stale cardinality.

**CHECK AL found a sixth site on its first run** — `Framework_MockTestCreateAudit.md`
S13 STEP 4, "Stage EXACTLY the two deliverables", which I had missed while fixing
the other five by hand. That is precisely the argument for machine checks over
careful reading. AL also flagged its own spec's version-history prose, which QUOTES
the defective assertion in order to explain it; quoting a defect is not committing
one, so comment lines are excluded.

**Verified:** AL reports 0 issues on the corrected corpus, and 2 issues when the
hardcoded assertion is reintroduced.

**Absent-safe.** A pre-v5.35 mock writes no dossier and the closed set is exactly 2 —
byte-identical to v5.34 behaviour across the estate.

**Files:** `Framework_MockTestCreate.md` v5.35.1 -> **v5.36**;
`Framework_MockTestCreateAudit.md` (S13 STEP 4 wording); `validate_framework_md.py`
(CHECK AL); `CHANGELOG.md`; `VERSION`; `MANIFEST.json`.

 2026.08.01.8
D1 + D3 + D8 — THE THREE DEFECTS CERTAIN TO RECUR. Release 5 of the
session-exhaustion programme. **No gate semantics change and no coverage changes.**
Every item here was verified still-live against the deployed 2026.08.01.7 build.

**D1 — MANDATE 0 was unimplementable, and an operator had already improvised a
waiver.** Inherited verbatim from Step 7, where it is trivially satisfiable because
Step 7 GENERATES content and never reads it back. Step 8 must read it back (§6 S6-0
requires the full stem and every option; S11-1 requires solving all of them), and on
every rendering surface each tool result enters the visible transcript — so
**reading is printing**. Step 8 could neither run Part B lawfully nor satisfy the
mandate while running it; both outcomes fail certification. On a live audit the
operator asked the paper's author to waive MANDATE 0, and that waiver had **no basis
in this spec**. The contradiction is now resolved rather than waived: MANDATE 0
governs **authored prose**, not spec-directed reads — the same distinction SKILL.md
Rule 5 already draws for in-protocol vision. The rule that actually protects the
exam is unchanged and absolute: Claude never RESTATES content in its own prose,
findings, dashboards or reports. Reads must be minimal-surface, incidental leakage
from diagnostic code remains a VIOLATION logged to `session_log.mandate0_incidents[]`,
and P0 emits a one-time SURFACE NOTICE so the author knows the session log will
contain content. On a shared or multi-tenant project the notice instructs a halt —
the only case where Step 8 should stop for MANDATE-0 reasons.

**And MANDATE 0 gets its first machine check, ever.** It declared itself absolute and
had no gate of any kind: S5-1A asserts ledger and evidence; S14-2 scans output
FILENAMES. Nothing inspected what Claude actually wrote, which is precisely how a
violation occurred and went unnoticed. `mandate0_scan()` statically flags the
incidental-print pattern rule 2 forbids — `print(p.text)` is a violation,
`print(len(b.opts))` is correct.

**D3 — Appendix B, introspected not transcribed.** The spec orders the operator to
call engines whose signatures it never stated, while SKILL.md forbids reading a `.py`
into context: no sanctioned discovery path existed. Two mis-calls on a live run cost
two turns and produced a materially wrong finding (6 failing subtopics reported where
the true answer was 2). Appendix B now carries every signature, argument
**provenance**, return type and unstated precondition, and fixture 94 asserts it
against the live engines by introspection so it cannot drift.

**It also corrects the circulating gap report.** That report states
`check_figural_conformance` returns `FAIL` for an unconstrained profile and
prescribes a caller-side skip guard. It returns **`SKIP`** — verified by
introspection and source. Documenting the report's version would have enshrined a
false precondition across 200 exams. The engine already handles it; SKIP is what
keeps ~200 legacy exams passing untouched.

**Also corrected:** the S5-2 A-FIGPROFILE row named
`batch_state.figural_qs[n].object_type` as its input. `batch_state.json` is a Step-7
internal sidecar that S0-1 explicitly does NOT deliver; the auditor has always read
`registry.figural_manifests[].object_types`. The stale row sent an operator hunting
for a file Step 8 can never have.

**D8 — P4 emits the EC-V18 notice BEFORE Phase 1.** A paper with 0 FigureSpec
sidecars is destined for an AMBER footer and a permanent §R13 limitation however well
the audit goes. The author deserves to know before committing hours, not to discover
it mid-audit. Partial coverage reports a RATIO and degrades per figure, never per
paper.

**Regression lock: 105/105 -> 107/107.** Two fixture weaknesses in this release's own
first cut, both found by mutation testing: the Appendix-B check passed vacuously
wherever `blueprint_core` was off the path (`except ImportError` swallowed it
silently), and the MANDATE-0 clean list omitted `print(len(b.opts))` — the exact
boundary the rule draws — so the guard was never exercised and a mutation deleting it
survived. A clean list that avoids the boundary tests nothing.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.17 ->
**v2.18**; `Framework_Blueprint.md` v1.42.6 -> **v1.42.7** and
`Framework_MockTestCreate.md` v5.35 -> **v5.35.1** (count refresh); `CHANGELOG.md`;
`VERSION`; `MANIFEST.json`.

**Remaining, all optimisation:** Tier B (sealed key), scope profiles, D6 partial
certification, and the W-DECISION decision register.

 2026.08.01.7
D7 (NO SILENT TRUNCATION) + TIER A (THE STEP-7 DOSSIER). Release 4 of the
session-exhaustion programme. Shipped together on purpose: fixing truncation alone
would have raised A-FIGCOMP from 12 visible findings to 27 — more honest but more
alarming — when the true cause was a missing `image_role` that Tier A supplies.
Together the diagnostics become honest AND correct: **27 -> 7** on the reference
paper.

**D7 — a findings list may never truncate silently.** Gates printed
`' '.join(sorted(set(x))[:12])`. On a real 60-question paper A-FIGCOMP had 27
findings and printed 12; the other 15 vanished with no trace, in LEXICOGRAPHIC
order (Q3 after Q28). A reviewer reasonably concluded the gate was
non-deterministic and filed it as unreproducible. It was neither — it was
under-reporting, in numeric-blind order. All 41 truncation sites now render through
`_flist()`, which sorts Q-numbers numerically and always states
`[+N MORE NOT SHOWN; T TOTAL]`. New rule RA-3a: a finding that exists and is not
shown is the same false-clean class as a vacuous pass.

**Tier A — repairing a channel that was designed and then severed.** Step 7 already
records every fact Step 8 was re-deriving, and `Framework_MockTestCreate.md` says of
`concept_map`: *"The audit gates read it directly instead of re-deriving."*
`audit_canonical.py` has carried the consumer path since v2.4. S0-1 simply never
delivered the sidecar — producer written, consumer written, pipeline never
connected. Measured on the reference paper: **0 of 60** `concept_map` entries
reached Step 8, `A-NAT-GRADE` printed "dormant" on all ~200 exams, and `image_role`
defaulted for every question.

`[ExamCode]_M[N]_audit_dossier.json` (Step 7 v5.35 S13-4b, Step 8 S0-1 item 7b)
carries per-question `subtopic_id`, `qtype`, `image_role`, `difficulty`,
`stem_precision`, `nat_grading_type/value`, `ca_range` and the MSQ/NAT in-stem
flags. Under one line:

> **HAND OVER FACTS STEP 7 RECORDED. NEVER HAND OVER JUDGMENTS STEP 7 REACHED.**

`load_dossier()` REFUSES any file carrying `answers` / `answer_verified` /
`derived_answer`, refuses an unknown schema, and refuses an `exam_code` / `mock` /
**paper-MD5** mismatch — a dossier describing a different document would let Step 8
audit against facts about another paper. New gate **A-DOSSIER** cross-checks every
fact against the SHIPPED PAPER and the registry; a disagreement is a **FAIL**, never
a silent overwrite in either direction, because it means Step 7 RECORDED something
other than what it SHIPPED. And the rule that keeps the whole thing honest:
**NO GATE MAY PASS ON DOSSIER EVIDENCE ALONE** — the dossier may make a check
cheaper or make a mismatch visible; it may never be the thing that certifies.
RA-1 is amended accordingly: independence over JUDGMENTS is absolute and untouched;
independence over FACTS was amnesia, and it cost a gate.

**Two defects in this release's own first cut, both found by RUNNING it:**

- `gate_dossier` read `b.opts` — **a field that does not exist on `Block`**.
  `getattr()` returned `None`, every mcq cross-check compared 0 against
  OPTIONS_COUNT, and 27 false failures were reported on the reference paper.
  Identical class to `Block.images '# reserved'` (v2.13). `block_option_count()`
  now counts from the document.
- `A-NAT-GRADE`'s dormancy test read `not concept_map`. The moment Tier A populated
  it, the gate woke with no answers and FAILED every NAT question — a correct
  "dormant" turned into a false FAIL. It now tests `not answers`, the honest
  condition, and goes live only with the sealed key channel (Tier B).

**Regression lock: 97/97 -> 105/105, eight guarantees mutation-verified.** Fixtures
86-93 cover suppression/total reporting, numeric ordering, dossier adoption,
disagreement-as-finding, judgment-key refusal, identity binding, absent-safety,
document-counted options, and A-NAT-GRADE dormancy. The A-NAT-GRADE regression was
found UNCOVERED by mutation testing — every other fixture stayed green with the fix
deleted — and fixture 93 closes it.

**Absent-safe across the estate.** No dossier ⇒ A-DOSSIER prints a NAMED reason and
the audit behaves exactly as v2.16. ~200 legacy papers are unaffected.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.16 ->
**v2.17**; `Framework_MockTestCreate.md` v5.34.3 -> **v5.35**;
`Framework_Blueprint.md` v1.42.5 -> **v1.42.6** (count refresh); `CHANGELOG.md`;
`VERSION`; `MANIFEST.json`.

**Remaining:** Tier B (sealed key), then D1/D8/D3, then scope profiles and D6.

## 2026.08.01.6
D2 + D4 — VISION IS A DECLARED, PROBED, DEGRADABLE DEPENDENCY. Release 3 of the
session-exhaustion programme. **This is the defect that actually halted a real
audit.** Coverage is unchanged for every healthy run.

**What happened.** On a live 60-question paper the `view()` path failed
mid-session. 43 images across 27 figural questions became un-stampable, so S5-1A
C6/C7 could never pass, MANDATE D forbade delivery, and the spec defined NO state
for "vision unavailable". The audit was permanently STUCK — not degraded, not
reported, stuck. 16 of 60 questions had been fully certified over two days and
none of it could ship.

**Why that was wrong by this framework's own doctrine.** §5 says "NO DEPENDENCY
CONDITION MAY EVER HALT A RUN"; CLAUDE.md says "Silence is the defect; a halt is
not the remedy." Degradation was granted to `blueprint_core`, to `figural_core`,
to all twelve figure gates and to every colour condition — and denied to the one
dependency whose absence is fatal. RA-4 was doing two jobs with one rule: blocking
a LAZY OPERATOR (right) and blocking an ENVIRONMENT OUTAGE (wrong).

**D2 — a third stamp state, and it is unfakeable.** `'view-unavailable'` joins
`'rendered-and-viewed'` and (absent). The obvious danger is that "I could not see
it" is exactly what a lazy operator would claim, so the state is **never assertable
by choice**: C6 admits it only when `session_log.vision_probe` carries a FAILED
record for that batch AND the montage exists at >= `EVIDENCE_MIN_BYTES`. C6 also
FAILS when vision has RECOVERED and the stamps were not upgraded — a paper that
COULD have been fully audited must not certify degraded. A degraded run prints
`COMPLETION-GATE: DEGRADED (vision)`, exits 0, and ships under an F1 AMBER footer
with a §R13 limitation. Identical treatment to EC-V18 legacy figures, which ~200
exams already deliver under.

**D4 — P3.5 vision probe.** Vision was ambient; now it is declared. The probe
renders three RANDOM glyphs and stores only a SALTED SHA-256 of them, so reading
the sidecar reveals nothing and reporting the glyphs requires actually seeing the
card. **That is what turns vision from an operator claim into a MEASURED fact —
the whole D2 safety argument rests on it.** It runs at pre-flight AND at the start
of every Phase-2 batch, because the incident had Batch 1 healthy and Batch 2 not:
a start-of-session probe alone would have missed it. A probe RENDER failure is an
ENVIRONMENT WARN and explicitly NOT a vision verdict.

**Not touched.** Tables, matrices, charts and OMML are arithmetic, not vision —
unaffected and still fully authoritative. A missing or trivial montage is still
un-audited and still blocks. A key that cannot be derived without sight is a
VOID_ITEM (KEY NOT DERIVABLE), never silently keyed. RA-3, RA-15a, MANDATE B and
every healthy-run verdict are byte-identical to v2.15.

**Regression lock: 89/89 -> 97/97, six guarantees mutation-verified.** Fixtures
78-85: a measured outage certifies DEGRADED at exit 0; the same stamp with no
failed probe FAILS; a RECOVERED probe with un-upgraded stamps FAILS; a trivial
montage still blocks; a MIXED ledger is legal; a healthy run is unchanged; the
probe sidecar leaks no glyph; a render failure is never a vision verdict.
**NO FIXTURE HAD EVER SIMULATED A VISION OUTAGE** — the fifth appearance of the
hollow-branch class (v2.10 `bc` binding, v2.12 A-FIGPROFILE, v2.13 `Block.images`,
v2.15 unknown-schema, now this).

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.15 ->
**v2.16**; `Framework_DeliveryFooter.md` v1.9.1 -> **v1.10** (§5 Q0b);
`Framework_Blueprint.md` v1.42.4 -> **v1.42.5** and `Framework_MockTestCreate.md`
v5.34.2 -> **v5.34.3** (count refresh only); `CHANGELOG.md`; `VERSION`;
`MANIFEST.json`.

**Next in the programme:** the Step-7 -> Step-8 dossier (repairs a channel Step 7's
own spec says should exist — "The audit gates read it directly instead of
re-deriving" — but which S0-1 severs), then D7-corrected silent-truncation removal,
then the sealed key channel.

## 2026.08.01.5
C1 — AN AUDIT CAN NOW SURVIVE A SESSION BOUNDARY. Release 2 of the 4-part
session-exhaustion programme. **Audit coverage is UNCHANGED.**

**The defect, and why it was the real one.** RA-18 declared Step 8 "resume-safe"
and stored every piece of cross-batch state — ledger, batch plan, WIP docx and the
ENTIRE evidence tree — under `/home/claude`. That directory does not survive a
session boundary. So resume worked inside one session and not at all across one,
and the failure was fatal rather than degraded: S5-1A C5/C6 assert that every
stamped evidence file EXISTS, so once the montages and saved fact records were
gone, a perfectly remembered ledger could NEVER certify. A session that exhausted
mid-Phase-2 lost the whole audit, and the retry exhausted the same way. **That
loop — not any individual gate — is why this step kept failing paper after paper.**
2026.08.01.4 (B3) made exhaustion much less likely; C1 makes it survivable, which
is the difference between a step that usually works and one that cannot lose your
work.

**The fix.** At the end of Phase 1 and of every Phase-2 batch, Step 8 writes
`[ExamCode]_M[N]_audit_checkpoint.zip` — `audit_state.json` + the WHOLE evidence
tree + the WIP docx — to the SAME filename each time, so there is exactly one
current bundle to keep track of. On `resume`, new pre-flight step **P0.5C**
verifies and rehydrates the uploaded bundle before any batch runs, rebasing
`evidence_dir` AND every recorded evidence path in the ledger (the previous
container's absolute paths are gone, and C5/C6 resolve through them). Neither
build nor restore is prose: both are commands in `audit_canonical.py`
(`--make-checkpoint` / `--restore-checkpoint`), per §21's rule that only code
certifies.

**Binding is the whole safety argument.** Restore REFUSES — writing NOTHING — on
an unknown schema, an absent/unparseable manifest, ANY member whose sha256
differs, or an `exam_code` / `mock` / `paper_md5` disagreeing with the paper in
hand. A refusal leaves nothing on disk because a half-unpacked checkpoint is the
worst outcome of all: it looks resumable. The paper binding matters most — a
checkpoint restored onto a DIFFERENT document would let Step 8 certify an audit
nobody performed on it, which is strictly worse than losing the audit. Building
without the paper is likewise refused: a bundle with `paper_md5: null` makes the
restore check vacuous.

**MANDATE D gains one explicit carve-out.** The checkpoint is handed to the author
before certification and that is not a breach: MANDATE D forbids shipping an
uncertified PAPER, and the checkpoint is not a product but opaque resume state
containing no certified artefact. The certification delivery remains exactly ONE
`present_files` of the closed set; S14-2 now CLEARS any checkpoint from outputs and
asserts (check 7) that none survives into the delivered set.

**Two defects found by RUNNING it, not by reading it** — the pattern that has
caught every real bug in this programme:

- **Evidence paths were not rebased.** The restored ledger still pointed at the
  dead session's absolute paths, so C5 failed with the files sitting correctly
  restored two directories away. `_rebase_evidence_paths()` now rewrites every
  `saved`/`montage`/`trace` explicitly, and `_resolve_evidence()` gained a
  basename fallback as a safety net.
- **The paper binding was optional.** A shell quoting slip left the docx absent
  during end-to-end testing and the checkpoint was written anyway, cheerfully,
  with `paper_md5: null` and therefore no binding at all. Now refused at both
  ends.

**Regression lock: 78/78 -> 89/89, eight guarantees mutation-verified.** Fixtures
70-77 cover: bundle completeness; **round-trip-then-certify — the source directory
is DESTROYED, the bundle restored into a fresh one, and the REAL completion gate
run, which must PASS**; nested-path rebasing; and refusal of a tampered member, a
wrong paper MD5, a wrong mock/exam, an unbindable bundle, a non-checkpoint
archive, and an UNKNOWN SCHEMA — each leaving nothing on disk. The unknown-schema
guard was found UNCOVERED by mutation testing: it could be deleted with every
other fixture still green, the same hollow-branch class this corpus has now
rediscovered three times. §21 gains test 23.

**Proven end to end on a real delivered paper.** A 60-question IIT JAM
Biotechnology audit with 104 evidence files and batches 1-3 of 6 complete was
checkpointed, its container destroyed, restored in a fresh one, and certified:
`COMPLETION-GATE: PASS (Q reviewed=60/60, facts sourced=60, artefacts stamped=44,
evidence files present=104)`. Bundle size 1.5 MB.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.14 ->
**v2.15**; `Framework_Blueprint.md` v1.42.3 -> **v1.42.4** and
`Framework_MockTestCreate.md` v5.34.1 -> **v5.34.2** (self-test count refresh
only); `CHANGELOG.md`; `VERSION`; `MANIFEST.json`.

**Remaining programme:** A1-A4 overhead cleanup (~27k), then B1 phase-scoped spec
split (~40k).

## 2026.08.01.4
B3 — FACT VERIFICATION KEEPS ITS EVIDENCE, NOT ITS TRANSCRIPT. Release 1 of the
4-part session-exhaustion programme. **Audit coverage is UNCHANGED**; what changes
is where the raw search result lives.

**The problem, measured.** Step 8 was exhausting its session before Phase 3 on
ordinary papers — and that is worse than it sounds, because the evidence directory
lives in `/home/claude` and does NOT survive a session boundary. An exhausted run
therefore loses the whole audit, and the retry exhausts the same way. Measured load
on a 60-question science paper (60 Q, 33 figural, 57 drawings):

| Item | Est. tokens |
|---|---|
| spec reads (`…CreateAudit.md` 72.6k + `…DeliveryFooter.md` 9.1k) | ~82,000 |
| Part A STDOUT x 9 runs (2 + K6 + 1) | ~11,200 |
| 33 per-question montages | ~46,000 |
| **B-FACT** | **~400,000+** |

B-FACT dominates everything else combined. §6 S6-3 requires the keyed fact AND
every option to be web-verified; on ~25 C-FACTUAL questions that is ~125 searches,
and retaining each full result set is what actually ends the session.

**The fix — RA-11 (a)(b)(c).**

- **(a) SAVE-THEN-SHED.** The raw result goes to `evidence/facts/`; ONE verdict line
  (`q17 · VERIFIED · <domain> · <date>`) is carried forward. Context stops being a
  second copy of the evidence.
- **(b) CACHE BY CONCEPT.** `ledger.fact_cache` is consulted BEFORE any search, so a
  claim shared by several questions is verified once and reused by path.
  Re-searching a settled concept is redundant work, not extra rigour.
- **(c) GROUP THE OPTIONS.** Where the options are same-domain claims, one query may
  settle the set and the saved file holds a LIST of per-option records; per-option
  queries remain wherever the grouped result leaves an option unsettled. Every
  option is still verified.

S6-2 now carries the canonical `save_fact()` / `_concept_key()` / `fact_line()`
writers, so the record shape cannot drift from what the gate asserts, and a
malformed record fails LOUDLY at write time rather than silently at C5.

**And the gate moves with it — this is what makes B3 safe.** C5 checked only that
the saved file EXISTED and was >= 1 byte. That was tolerable while the full result
ALSO sat in the reasoning stream, because the evidence was duplicated. It is not
tolerable once the file is the ONLY copy: without a shape check the discipline
degrades silently from "save the result" to "touch a file", and C5 would certify an
audit whose evidence no longer exists anywhere. **C5 now requires the file to PARSE
and to carry a non-blank `query` + `url` + `retrieved_at` + `snippet` in every
record** — exactly the four fields RA-11 has mandated since v2.6 and that no gate
had ever checked. It also accepts one file referenced by many questions and REPORTS
the reuse (`N distinct source file(s) for M reference(s)`), so the cache reads as
reuse and can never be mistaken for a coverage shortfall. FAIL messages name FIELDS
and Q-numbers only, never fact content (MANDATE 0).

**What B3 does not touch:** which facts are checked (all of them), that the check is
LIVE, that it is per-option, that it is evidence-backed, or any of RA-0 / RA-3 /
RA-15a / MANDATE B. No preference may waive coverage and none is waived here.

**Regression lock: 73/73 -> 78/78, all five new behaviours mutation-verified.**
Fixtures 65-69: a well-formed record passes; a 1-byte stub FAILS (this is the file
that CERTIFIED before v2.14); a record missing `retrieved_at` FAILS naming the
field; a blank `url` FAILS exactly like an absent one; a record LIST and a file
shared by two questions both PASS and are reported as cache reuse. Five mutations
run — existence-only C5, presence-instead-of-blank check, list-form rejection,
dedup-reporting removal, unparseable-JSON swallow — each kills exactly its intended
fixture. §21 gains test 22.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.13 ->
**v2.14**; `Framework_Blueprint.md` v1.42.2 -> **v1.42.3** and
`Framework_MockTestCreate.md` v5.34 -> **v5.34.1** (self-test count refresh only);
`CHANGELOG.md`; `VERSION`; `MANIFEST.json`.

**Projected effect:** ~400k -> ~60k on the B-FACT line. Remaining programme: C1
cross-session checkpoint (the fix for losing an audit at a session boundary), then
A1-A4 overhead cleanup, then B1 phase-scoped spec split.

## 2026.08.01.3
GAP-2026-08-01-FIGSPEC-TRANSPORT — the twelve Step-8 figure-conformance gates
ACTUALLY EVALUATE FIGURES. Discovered while verifying the 2026.08.01.1/.2 halt
fix against a real delivered paper: the run completed, the roster was invariant,
and all twelve gates printed `0 figure(s) conform.` on a paper carrying 57
drawings.

**Two independent breaks, either one sufficient.**

- **D1 — `Block.images` was never populated.** Declared `self.images = []
  # reserved` at v1.0 and appended to NOWHERE in the 2,484-line auditor. The
  twelve gates iterate `blk.images`, so `_seen` was 0 on every run, in every
  exam, and every gate passed vacuously.
- **D2 — the FigureSpec sidecars had no transport channel.**
  `src['figure_specs']` was READ at the gate site and WRITTEN nowhere, and
  structurally could not be written: `figural_core.write_spec_sidecar()` drops
  `q{N}_*.figspec.json` beside each PNG in the STEP-7 working directory, which
  is internal and never delivered (S0-1). Even genuine v5.33 output would have
  read as legacy for ever, so EC-V18 leniency applied to papers that were not
  legacy at all.

**Why no gate saw it.** No fixture had ever put an IMAGE IN A BLOCK. All 61
self-tests ran on image-free documents, so an empty `Block.images` was
indistinguishable from correct behaviour and 61/61 PASS coexisted with zero real
coverage. This is the SAME hollow-branch class as 2026.08.01.1 — closed there for
A-FIGPROFILE, left open one gate-family over. It also contradicted the auditor's
own doctrine: v2.12 wrote "0/0 is NOT evidence of conformance (edge case 6)" for
A-FIGPROFILE while twelve gates printed OK over zero evaluated figures.

**The fix.**

- `attach_block_images()` populates `Block.images` before any gate runs, fed by
  `extract_media()` (media parts out of the ZIP onto disk; never raises) and
  `para_images_ext()` (walks each `<w:drawing>` as a UNIT, so a drawing's alt
  text cannot be attributed to its neighbour — A-FIGALT reads `@descr`).
  Table-cell paragraphs are included: a DI chart or a figure/option fusion table
  puts drawings in cells, which a block-level paragraph scan misses entirely.
  `para_images()` is byte-unchanged (six call sites, fixture-locked).
- **TRANSPORT.** Step 7 v5.34 carries the FigureSpec records into
  `registry.figural_manifests[].figure_specs`, keyed by the canonical PNG name
  S10-8 already stamps on the drawing. The registry is the sanctioned channel —
  the precedent `object_types`/`subtopic_ids` set at v5.31, for the identical
  reason: Step 8 receives the registry and receives no sidecar. Additive,
  absent-safe, nothing written to the docx, B3/R-DELIVER cardinality untouched.
- **0 EVALUATED IS NOT EVIDENCE.** Drawings present but unreadable => WARN
  "conformance NOT ESTABLISHED"; no drawings => OK "dormant"; never a vacuous
  "conform". The duplicate SECOND `A-FIGDPI` line the old EC-V18 note emitted is
  folded into each gate's single verdict — unreachable while `_seen` was 0, and
  it would have broken the v2.12 roster-count integrity signal the moment
  figures were actually evaluated.
- **D6 — the §13 re-sync CARRIES FORWARD the figural manifest** instead of
  rebuilding a fresh 3-key dict that silently discarded `object_types`,
  `subtopic_ids`, `figure_specs`, `paper_id` and `visual_verified`. Invisible on
  the audited run; it surfaced on the NEXT one, where a re-audit found
  A-FIGPROFILE dormant and every figure legacy on a paper that was neither. Step
  8 re-derives what it OBSERVES (figural_qs, image hashes) and preserves what
  only Step 7 can know — the same split §13-2b already applies to subtopic_id vs
  difficulty. Specs for a REGENERATED question are dropped by key (S8-4).

**EC-V18 IS A DELIVERY TOLERANCE, NOT ONLY A SEVERITY RELABEL.** Making the gates
non-vacuous surfaced a conflict that could not collide while `_seen` was always
0: AMBER is defined as FAIL severity, and EC-V18 is defined as NON-NEGOTIABLE
that ~200 existing exams "keep auditing AND DELIVERING untouched". A `_fail()`
exits non-zero and MANDATE D requires exit 0 to certify, so emitting FAIL for a
LEGACY-ONLY finding would have converted this coverage fix into an estate-wide
delivery outage on landing — the same trap `AUTH_GATE_FLOOR` exists to avoid.
Resolved in EC-V18's direction, because EC-V18 is the clause that speaks to
delivery: a finding on a figure with NO sidecar is a LOUD WARN (amber footer,
S5-4 ACCEPTED WARN, §R13 limitation, delivery NOT blocked — Step 8 cannot
retro-fit a sidecar onto an already-rendered paper); a finding on a figure that
DOES carry one is a FAIL and blocks certification, exactly as before. Nothing
becomes silent, nothing halts, no existing exam stops shipping.

**Regression lock: 61/61 -> 73/73, every new fixture mutation-verified.**
Fixtures 53-63 cover attachment, per-drawing alt-text attribution, table-cell
drawings, non-vacuity, roster invariance, zero-image dormancy, unreadable-media
coverage WARN, spec-key resolution, and the FAIL/WARN severity split. Nine
mutations were run; each kills exactly its intended fixture. Two matter most:

- The first pass scored **71/71 with the `run_audit` wiring deleted**, because
  every fixture called `attach_block_images()` directly — the identical shape of
  the v2.10 defect (written at the call sites, bound nowhere). Fixture 63 runs
  the REAL `run_audit()` end to end and now fails alone on that mutation.
- **PER-FIGURE FAULT ISOLATION (fixture 64), found empirically during
  end-to-end testing, not by inspection.** The spec now arrives from the
  REGISTRY, i.e. from outside the process, and a partially-recorded one raises:
  `render_figure()` fills `png_px` / `font_pt_native` / `placement_scale` only
  AFTER it reads the artefact back, so a render that died mid-way leaves a shape
  the gates index into. One such figure raised `TypeError` out of
  `g_figlabel()`, `_safe_gate()` converted it to `A-GATEERROR`, and the WHOLE
  `A-IMAGES` gate died — twelve gate lines gone, roster 47 -> 36, the §R15
  invariance 2026.08.01.1 had just restored broken by a single figure. A
  per-item L3 guard now skips only that figure, and the shortfall is stated on
  EVERY gate's own line (`[coverage: N/M evaluated; K skipped]`) so no verdict
  can be read as fuller coverage than it had. This is the same three-layer
  discipline 2026.08.01.1 mandated for `blueprint_core`, applied to
  `figural_core`'s per-item calls.

§21 gains tests 16-20 recording all of this.

**AUTH_GATE_FLOOR STAYS AT 35** — deliberately, and for the third release
running. A v2.11 copy (51/51), a v2.12 copy (61/61) and a v2.13 copy (72/72) all
pass the floor, so the estate migrates exam by exam with zero downtime.

**Files:** `audit_canonical.py`; `Framework_MockTestCreateAudit.md` v2.12.1 ->
**v2.13**; `Framework_MockTestCreate.md` v5.33.1 -> **v5.34**;
`Framework_Blueprint.md` v1.42.1 -> **v1.42.2** (self-test count refresh only);
`CHANGELOG.md`; `VERSION`; `MANIFEST.json`; `SPEC_MANIFEST.json`.

**Verified:** bootstrap 33/33; self-test 73/73; all six auditors clean, twice,
with `rm -f .verified` between runs; Context-1 and Context-2 rosters identical
(47 lines) on a real 60-question, 57-drawing delivered paper, exit 0 preserved.
Positive path proven with an authentic figural_core-rendered FigureSpec injected
into the registry: a planted placement-scale regression FAILs with the correct
diagnostic and exit 1, while the 55 legacy figures in the same paper are counted
separately and explicitly reported as non-blocking.

## 2026.08.01.2
Post-deployment correction to 2026.08.01.1. The engine fix (D1, P6, D3-D7) is
UNCHANGED and remains deployed — `audit_canonical.py`, `routes.json` and the
gate behaviour are byte-identical. What changes is the DISTRIBUTION remedy, and a
CLAUDE.md gap that made the wrong remedy look necessary.

**The wrong remedy.** 2026.08.01.1 solved "the engines never reach the machine that
runs the auditor" by adding both to the Step-6 B3 output set (6 -> 8 files), which
implied uploading them to ~200 exam projects. CLAUDE.md states the opposite rule
and states it correctly: engines live ONLY in the central repo, `/mnt/project` is
DATA and never an import source, and *"a fix pushed to production reaches all ~200
exam projects on their next clone — no per-project engine provisioning is required,
and none should be performed."* A per-exam `.py` copy is a SECOND, UNVERIFIED source
that can silently go stale, reintroducing exactly the generator/auditor drift the
v2.10 delegation to `blueprint_core` exists to prevent.

**Why the exception looked real, and what it actually is.** CLAUDE.md's reasoning is
that Step 0 does `cd "$FW"`, so a bare import resolves in the clone. That is TRUE
for every engine consumer EXCEPT one, and the difference is purely mechanical —
verified empirically in both directions:

- Spec-inline code runs as `python3 - <<EOF`, so `sys.path[0] == ''`, which resolves
  to the cwd, i.e. `$FW`. `import blueprint_core` RESOLVES. This is every ordinary
  consumer.
- The auditor is a standalone file run as `python3 /home/claude/X_mock_test_audit.py`.
  Python sets `sys.path[0]` to the SCRIPT'S OWN DIRECTORY, never the cwd — so
  `/home/claude` goes on the path and `$FW` does NOT, even when the cwd IS `$FW`.
  The import FAILS.

That single unnamed exception is why the A-FIGPROFILE delegation could be written,
reviewed and shipped without its import: in the environment the change was reviewed
in, a bare import appeared to resolve.

**The right remedy.** Step 8 P0 now copies both engines from the Step-0 verified
clone (`$FW`) into `/home/claude` — precisely the pattern `Framework_Blueprint.md`
§S1-2b has always used for `blueprint_core`. The clone is hash-tracked and
bootstrap-verified at Step 0 of every session, so the engines are current BY
CONSTRUCTION, CLAUDE.md's promise holds in full, and **no exam project needs
touching**. If the clone is somehow unavailable, P0 falls back to an upload/project
copy but says explicitly that it is UNVERIFIED and may be stale.

**Consequences:**
- B3 returns to **6 deliverables**. `Framework_Blueprint.md` v1.42 -> **v1.42.1**;
  `Framework_DeliveryFooter.md` v1.9 -> **v1.9.1**;
  `Framework_MockTestCreateAudit.md` v2.12 -> **v2.12.1**.
- `CHECK AK`'s `_AK_B3_EXPECTED` returns to 6, which is exactly what that constant
  is for: one edit, and the check lists every site that must move with it. All
  cardinality sites verified consistent by the check itself.
- **ESTATE ACTION PATH A IS WITHDRAWN.** The ~200 per-exam uploads are unnecessary
  and should NOT be performed. Refreshing an exam's `[ExamCode]_mock_test_audit.py`
  is still worthwhile (it is a genuine per-exam copy, taken at B3), but no engine is
  ever uploaded. Path B (in-session sanctioned repair of a stale auditor copy under
  P0.5 policy (b)) is unaffected and remains the immediate unblock.
- `CLAUDE.md` now NAMES the standalone-script exception under its engine-loading
  section, with both consumers listed and the empirical rule spelled out, so the
  section can no longer be read as licensing an unbound import.
- Third and last dead "copy it from Framework_MockTestCreate.md Appendix A"
  instruction retired (P1 REJECT hard-stop path, CreateAudit:882). That file has
  carried no auditor fence since v2.11.2. All three instances are now gone.

## 2026.08.01.1
GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING — Step 8 (Mock/TestCreateAudit) HALTED
PERMANENTLY with ZERO gate output on any exam whose paper came from Step 7 v5.31+.
Reproduced deterministically on a pristine clone of 4ddfc0c; fix verified by
mutation test (the new CI checks fire on the unfixed tree and are silent on the
fixed one).

**Deployment-hold rectification (pre-push review).** The first cut of this wave was
HELD, correctly. The B3 deliverable cardinality change (6 -> 8) had landed in §13-7
ONLY; eleven other sites still described a 6-file delivery, including §11 S11-3
PART B — the OPERATIVE `present_files` call. A session following the spec would
still have delivered 6 files and neither engine would have reached the exam
project, leaving the whole fix INERT — precisely the state D2/D3 exist to end. Two
of the stale sites were actively harmful rather than merely undercounting: the
S11-3 checklist mandated `[ExamCode]`-prefixed names for ALL files, which for the
two engines is exactly the prefix that BREAKS `import blueprint_core`; and a second
copy of the retired hollow-MVP marker `--self-test passed (13/13 PASS)` survived at
S11-3 (only the §13-7A copy was corrected), telling the operator to CONFIRM the
constant-print signature that P1 is instructed to REJECT as proof of a false-clean.
All twelve sites are now corrected — Blueprint §8 batch overview, §11 S11-3 PART B
+ checklist + PART C handoff, re-generation path, §13 header, §13-1 naming
convention, §13-1 pipeline map, §13-8 header, restart path, footer-type map, §15
checklist; DeliveryFooter §1 F2 (Step 5's own unrelated 6-file line deliberately
untouched); and CreateAudit's MANDATE-A hard-stop text. The §13-1 naming section
previously stated a UNIVERSAL prefix rule that the two new deliverables must
violate; it now names them as the explicit, mandatory exception and says why.
This is CLAUDE.md verbatim: *a deliverable RENAME or CARDINALITY change is a
cross-step contract change, never a docs-only edit* — every consumer re-tested in
the same commit. **CHECK AK now enforces it mechanically** (below), because prose
did not: the miss was invisible to every automated gate in the previous wave.

- **D1 — `bc` referenced but never imported (BLOCKING).** `audit_canonical.py`
  gate `A-FIGPROFILE` READ `bc` at lines 1101/1109/1110 and BOUND it at none. The
  v2.10 change deliberately delegated the conformance verdict to `blueprint_core`
  so the generator and its auditor could not drift — and wrote that delegation
  into the COMMENTS and the CALL SITES, but never added the import. Any registry
  carrying `object_types` raised NameError out of `gate_images()` -> `run_audit()`
  -> `main()`. Because `print_results()` runs only AFTER the last gate, the process
  died before a single line printed: not a failed gate, a failed RUN, blocking
  Phase 1, Phase 2 and the Phase-3 completion gate together. An AST scan confirms
  `bc` was the ONLY unbound name in all 2,194 lines. Now bound with a THREE-LAYER
  guard, because an import guard alone is insufficient — measured, not assumed:
  L1 import (`except Exception`, since a TRUNCATED engine raises SyntaxError and
  `except ImportError` misses it — `blueprint_core.py` is ~168 KB, squarely inside
  the project-knowledge truncation range P0.5 exists for); L2 capability (`hasattr`
  on all three delegated functions, since a STALE engine imports cleanly then
  raises AttributeError at the call site); L3 call site (`try/except`, so a raise
  INSIDE the engine degrades to a reported skip). WARN, not `_ok` (the gate did not
  run; green would be the silent-pass failure the v1.8 quality gate exists to kill)
  and not `_fail` (a missing engine is an ENVIRONMENT condition, not a paper defect
  — EC-V18).
- **P6 — GATE FAULT ISOLATION (`_safe_gate`). The structural fix.** `run_audit`
  called 21 gates in bare sequence, so ANY raise in ANY gate destroyed the entire
  report — including the 30+ gates that had already passed. Binding `bc` fixes THIS
  defect; isolation fixes the DEFECT CLASS. From now on no gate, present or future,
  can abort the run: an unexpected raise becomes a LOUD, NAMED `A-GATEERROR` and
  the remaining gates still execute. Severity is FAIL, not WARN — a gate that
  crashed DID NOT AUDIT THE PAPER, so exit is non-zero and certification is blocked
  while the run still COMPLETES. Exactly CLAUDE.md's rule: a CLASS T failure must be
  LOUD and must NOT halt; silence is the defect, a halt is not the remedy.
- **D2/D3 — neither engine was ever distributed (BLOCKING).** `blueprint_core.py`
  and `figural_core.py` were absent from the Step-6 B3 output set, absent from
  project knowledge, and named as a Step-8 input nowhere in
  `Framework_MockTestCreateAudit.md` (zero occurrences). Fixing D1 alone would have
  converted a loud crash into a quiet no-op. B3 now ships both VERBATIM under their
  BARE names (6 -> 8 outputs); an `[ExamCode]_` prefix breaks `import blueprint_core`
  and silently disables the gates.
- **D3 — eleven figure gates went dark with no output line.** A single self-naming
  `A-FIGSCALE` WARN stood in for all twelve, so `A-FIGALT`, `A-FIGCOLOUR`,
  `A-FIGCVD`, `A-FIGDEGEN` (BLOCKING), `A-FIGDPI`, `A-FIGGLYPH`, `A-FIGLABEL`,
  `A-FIGLABELPX`, `A-FIGMONO` (VOID_ITEM — an answer-cue leak), `A-FIGOPTUNIF` and
  `A-FIGSERIES` vanished from STDOUT entirely; a reader could not tell they had not
  been evaluated. Each now emits its own line. The printed roster is INVARIANT
  across every environment, which restores §R15 reproducibility and makes the gate
  COUNT itself a usable integrity signal. `figural_core`'s guard also widened to
  `except Exception` — a truncated copy raised SyntaxError and killed the run the
  same way D1 did, one engine over.
- **D4 — the 51-fixture self-test could not see any of it.** No fixture ever built
  a registry carrying `figural_manifests[].object_types`, so every fixture took
  A-FIGPROFILE's DORMANT branch and the unbound name was never executed: 51/51 PASS
  on a build that could not survive one real paper. v2.6 hardened the self-test
  against a hollow FILE; this was a hollow BRANCH — the same miss one layer down.
  Ten new fixtures (51 -> 61) execute the PRIMARY branch in every environment the
  estate presents: engine present/absent/truncated/stale/raising, 0-of-0, legacy
  dormant, plus gate-fault isolation and a SELF-HOSTED undefined-name scan that
  runs on every self-test in every exam project.
- **0-of-0 is no longer reported as conformance.** `object_types` present with no
  usable `subtopic_ids` now WARNs rather than claiming `_ok` for coverage it never
  had.
- **D5/D7 — `routes.json` declared the wrong dependency set.** `blueprint_core.py`
  was routed to NEITHER `Mock/TestCreateAudit` (D5) NOR `Mock/TestCreate` (D7 — new,
  not in the gap report: `corpus_io.py` imports it, the identical hole on the
  GENERATOR side). `bootstrap.py --trigger TestCreateAudit` was therefore actively
  telling operators the engine was not needed — the machine-readable root cause.
  All four triggers corrected; full declared-vs-actual parity now clean repo-wide.
- **D6 — no spec handling for "audit.py raises on the real paper."** §17 covered
  `--self-test` failure modes exhaustively but not a traceback on the audit run
  itself, and §12-1 enumerates only CERTIFIED CLEAN or HARD STOP — a Part-A crash is
  neither. P0.5 policy (b) permitted regenerating a *corrupt* script, but this file
  was not corrupt (it ast-parsed, passed 51/51, and was byte-identical to its
  source), so regenerating reproduced the identical defect. Four new §17 rows now
  name this case, `A-GATEERROR`, engine-skip WARNs, and short rosters.
- **Estate refresh (~200 deployed copies).** Fixing the repo does not fix them —
  each project's `[ExamCode]_mock_test_audit.py` is a COPY taken at B3. §21 now
  sanctions BOTH paths: (A) per-exam Step 6 B3 regeneration (permanent, idempotent),
  and (B) in-session sanctioned repair under P0.5 policy (b), a byte-exact restore
  from a hash-tracked source, so any Step-8 run meeting a pre-v2.12 copy completes
  immediately. Until (A) reaches an exam, (B) keeps it running.
- **AUTH_GATE_FLOOR STAYS AT 35** — deliberately NOT raised to 61. The floor gates
  the DEPLOYED copies; raising it above their printed count would HARD STOP every
  un-refreshed exam and convert a coverage improvement into an estate-wide outage.
  At 35 a v2.11 copy (51/51) and a v2.12 copy (61/61) both pass, and the estate
  migrates exam by exam with zero downtime.
- **Three new CI checks in `validate_framework_md.py`, all mutation-tested.**
  CHECK AI (ENGINE <-> ENGINE DEPENDENCY PARITY) — every engine an engine imports
  must be routed alongside it; catches D5/D7 automatically for all future
  delegations, on both the generator and auditor sides. CHECK AJ (UNDEFINED-NAME
  SCAN) — no engine may read a name it never binds; catches the next `bc`-class
  defect in one pass without anyone having to anticipate which gate will have it.
  CHECK AK (B3 DELIVERABLE CARDINALITY) — every site describing the B3 delivery
  must state the same count, and no site may assert the retired hollow-MVP
  self-test signature as a PASS criterion. Verified against the unfixed tree: AJ
  names `bc` at 1101/1109/1110, AI names both Create triggers, AK names all
  thirteen stale cardinality sites plus the surviving `13/13` assertion. All three
  silent on the fixed tree.
- **Dead fallback removed (pre-existing, flagged two waves ago).** MANDATE A's
  hard-stop text and §17's `audit.py missing` row both told the operator to "copy
  it from Framework_MockTestCreate.md Appendix A". That file has carried no auditor
  fence since v2.11.2 and now only points here — so the instruction was dead, and
  it sat on the hard-stop path, i.e. it was what someone read while already
  blocked. Both sites now name `audit_canonical.py` as the live source.
- **Corrected false in-spec claim.** `Framework_MockTestCreateAudit.md:3069` still
  read *"Dependency-light: python-docx + Python stdlib only."* — false since v2.10.
  A maintainer reading it had an explicit in-spec assurance that no repo engine was
  needed, which is how the delegation shipped without its import.
- **Stale MVP artefact removed.** The Blueprint B3 checklist still asserted
  `--self-test passed (13/13 PASS)`, a leftover from the RETIRED hollow MVP; it now
  asserts a FIXTURE-BASED N/N with N >= AUTH_GATE_FLOOR.
- Versions: `Framework_MockTestCreateAudit.md` v2.11.2 -> **v2.12**;
  `Framework_Blueprint.md` v1.41.2 -> **v1.42**; `Framework_DeliveryFooter.md`
  v1.8.1 -> **v1.9**. `audit_canonical.py` self-test 51/51 -> **61/61**.

## 2026.07.31.7
- §16 FREQUENCY-XLSX IMPLEMENTATION EXTRACTED: 664 lines of workbook code (aggregation,
  derived metrics, generation, and the 5 sheet writers) moved byte-identically from
  Framework_MockTestAnalyse.md §16-1/§16-2/§16-4..§16-8 to the new hash-tracked engine
  frequency_xlsx.py. The spec keeps §16's contract — sheet specifications (§16-3), the
  9-item validation checklist (§16-9), the EC-F* frequency edge cases (§16-10) — and each
  extracted subsection now names the engine functions it governs. The synthesis call site
  uses `import frequency_xlsx as fx`. Session read: PYQExtract 9,012 -> 8,389 lines.
  gen_manifest TRACKED_PY += frequency_xlsx.py; routes.json routes it to PYQExtract
  (CHECK AH). Zero behavioural change; spec and engine parse and import clean.
- Both SKILL copies: routed-engine count 8 -> 9 (frequency_xlsx.py is routed); the two
  tracked-but-unrouted scripts (validate_framework_md.py, audit_canonical.py) named explicitly
  so CHECK AA / audit_sync stay green.

## 2026.07.31.6
- CANONICAL AUDITOR EXTRACTED: the 2,194-line fenced mock_test_audit.py source moved
  byte-identically from Framework_MockTestCreateAudit.md Appendix A to the new hash-tracked
  engine file audit_canonical.py (self-test 51/51 verified post-extraction). Appendix A keeps
  the full contract + pointer; Blueprint §13-7A now copies the engine file, ending the
  mid-session cross-spec read of CreateAudit during MockBlueprint Step 8A. Sessions:
  Mock/TestCreateAudit 5,920 -> 3,737 lines (-37%). gen_manifest TRACKED_PY += audit_canonical.py
  (32 files verified). §21 regression lock, MANDATE A, and P1 apply to the engine file unchanged.
- audit_callgraph.py: audit_canonical.py added as a call-site source — its blueprint_core
  calls (check_figural_conformance, parse_image_analysis_blocks) were spec-embedded call
  sites before extraction and remain runtime-reachable; without this, C4 false-fired on both.

## 2026.07.31.5
- HEADER-CHANGELOG RELOCATION, 15 specs, 5,690 lines of history moved verbatim to the
  ARCHIVE sections at the bottom of this file (per-file blocks). Kept in every file:
  line-1 version header (patch-bumped), current MINIMUM COMPANION VERSIONS blocks,
  PURPOSE/SCOPE-style preambles, structural notes/dividers, and the newest entry; archived:
  superseded companion blocks and all older entries. Per-file byte-exact partition proof
  (kept + archived == original header, no gaps/overlaps), body byte-untouched (the only
  tail change is the version-bearing END sentinel bump), token sweep across all 15 archives
  found zero functional tokens lost. Session reads drop: PYQExtract −1,232, MockCreate/
  TestCreate −1,342, MockBlueprint −900, Mock/TestCreateAudit −659, PYQPrepare −392,
  PYQSort −382, and every trigger −79 via the shared DeliveryFooter; corpus total −5,690.
- audit_sync.py: new [REL-SYNC] guard — VERSION file must equal CHANGELOG's top '## ' entry;
  motivated by the 2026.07.31.4 partial deployment where the CHANGELOG entry was missed and
  no checker fired.
- MANIFEST.json + SPEC_MANIFEST.json regenerated (15 spec hashes changed; engines untouched).

## 2026.07.31.4
- bootstrap.py advisory REWORDED (context-cost defect, found during the corpus_io.py length
  analysis): `--trigger` printed one line — "Entry-point spec(s) ... read IN FULL:" — listing
  the WHOLE route, engines included. Followed literally, a PYQCount session would read 2,641
  spec lines PLUS 9,316 engine lines (corpus_io 4,399 + blueprint_core 3,226 +
  reconcile_taxonomy 1,248 + syllabus_provenance 443) into context; engines are executed, not
  read, so all 9,316 of those lines were dead weight. The advisory now prints two lists:
  .md specs "READ IN FULL" and .py engines "EXECUTE via import; do NOT read into context".
  Verification contract untouched (same checks, same exit codes, same .verified token);
  nothing machine-parses the advisory line (verified by corpus grep). Matching one-line
  clarification in mocktestframework_SKILL.md rule 2 and in the installed-skill SKILL.md
  shipped alongside.
- corpus_io.py itself: analysed and deliberately UNCHANGED. Its 4,399 lines cost sessions
  nothing (engines are executed, never required reading); it is the consolidation artifact
  for previously-drifting copies (Cluster K readers, is_option), so splitting it would
  reopen that defect class; its docstrings/comments are consumed by audit_callgraph
  (parameter contracts), audit_specs_ext V-SYNC (sync rules) and encode GAP-numbered defect
  history, so trimming them risks three auditors for zero runtime gain. Health verified: no
  dead public functions (5 external-orphan suspects each have 2-5 internal call sites),
  no layering violation (blueprint_core imports stdlib only), callgraph 0 findings.
- LATENT COUNT DEFECT FIXED (both SKILL copies): release 2026.07.31.2 set the skill's
  engine count to 9 (tracked scripts), but CHECK AA and audit_sync count engines ROUTED
  in routes.json = 8 — validate_framework_md.py is tracked but deliberately never routed
  (it is the CI validator). Any SKILL.md claiming 9 placed where AA reads it fires
  'claims 9 engine scripts; routes.json routes 8'. Both copies now state 8 with the 9th
  script explicitly accounted in the same sentence, so the count matches the checkers'
  definition while preserving the .2 entry's fact.
- MANIFEST.json regenerated for the VERSION stamp (bootstrap.py and skill files are not
  hash-tracked; specs and engines all unchanged — 31 hashes identical to 2026.07.31.3).

## 2026.07.31.3
- Framework_PYQCore v1.0.2: post-deployment deep sync audit found one ownership ambiguity —
  the scaffolding host-note header '## §2-HOSTED — ...' matched the '^## §N' section-header
  pattern, making §2 resolve to two files (Draft owns §2; Core hosts S2-3). Header renamed to
  'HOSTED SECTION S2-3 (from §2 ...)'; §-ownership now unique per file. Scaffolding-only,
  hosted v2.29 content re-verified byte-identical. SPEC_MANIFEST.json: Core entry updated in
  place, 40-file wide baseline preserved. MANIFEST.json regenerated.
- Sync audit result at seal (production 2026.07.31.2 + this fix): bootstrap 31/31; validator
  0 repo issues (sole finding is the environment-side stale installed skill, already tracked);
  check_triggers 24 consistent; audit_sync clear of ERA-SYNC; audit_deep 0; audit_callgraph 0;
  audit_specs_ext 0 across 39 files (full invocation with engines — specs-only invocation
  emits 4 [V-SCOPE] scope warnings by design, not findings). Independent cross-step audit:
  9/9 v2.29 slices byte-identical each in exactly one file; §1-§12 single-owner; 12/12
  artifact producer/consumer placements correct; 4/4 pipeline handoffs in the right files;
  S2-3 single-sourced; companion minimums single-sourced; stub unrouted; 4/4 routes correct.

## 2026.07.31.2
- Seals commit 3bbc36c (Framework_PYQCore v1.0.1 — the ERA-SYNC engine-sourcing line), which
  landed after VERSION had already been stamped 2026.07.31.1. Its substance is described in
  the 2026.07.31.1 entry below; this block exists so the version history and the shipped
  commits stay in step, and to CORRECT three claims in that entry which do not match what
  actually went live:
  - SKILL.md engine count shipped as **9**, not "7→8". figural_core.py became the 9th engine
    in release 2026.07.29.2 and was missing from the count; the uploaded file still said 8.
  - CLAUDE.md was not merely "generalised": the stale bootstrap figure is now stated
    explicitly as **31/31 — 22 Framework_*.md + 9 engines** (was 25/25 — 17 + 8), and the
    SPEC_MANIFEST baseline as **40 files** (was 33).
  - SPEC_MANIFEST.json shipped at **40 files (22 specs + 18 engines/auditors/tooling)**, not
    the 22-file specs-only form the generator emitted. Narrowing it would have dropped the
    second integrity baseline for all 9 engines, the 4 audit scripts and routes.json, which
    contradicts CLAUDE.md's definition of it as "the wider workbench baseline — including the
    audit and tooling scripts".
- Release-manager note: the split was deployed via `main` → `main:production` fast-forward.
  DEPLOY_INSTRUCTIONS.md §D directed `git checkout production` + `git push origin production`,
  which the standing guardrail forbids; the instruction was not followed.
- Verification at seal: bootstrap 31/31, validate_framework_md 0 issues across 22 files,
  check_triggers consistent (24), audit_deep 0, audit_callgraph 0, audit_specs_ext 0 across
  25 files, audit_sync clear of [ERA-SYNC]. MANIFEST.json regenerated independently and found
  byte-identical to the one shipped with the split — 31 file hashes and 24 routes agreeing
  across two separate generations.
- Still open (owner action): the installed project skill at
  /mnt/skills/user/mock-test-framework/SKILL.md must be replaced with the repo copy, or
  audit_sync/CHECK AA keeps reporting the stale 17-spec claim.

## 2026.07.31.1
- Framework_PYQAnalyse v2.29 SPLIT into 5 files with ZERO rule/functionality change
  (owner request: per-step context load; the 6,988-line monolith destabilised chat sessions).
  New architecture: Framework_PYQDraft.md (§2), Framework_PYQScan.md (§3),
  Framework_PYQApprove.md (§4), Framework_PYQCount.md (§5), Framework_PYQCore.md
  (§1 + hosted S2-3 + §6–§12 shared contracts + companion-version minimums). All §/S/EC IDs
  preserved byte-identically; a completeness gate proved every v2.29 body line appears in
  exactly one new file. S2-3 is hosted in Core because PYQScan S3-6 Refinement executes its
  machinery (Domain Check, Q1/Q2/Q3 decision tree, 6 Pattern Dimensions) — §11 already
  declared it universal; single-sourcing it prevents the cross-file drift class of
  GAP-2026-07-25-002 / the triple is_option() defect.
- Framework_PYQAnalyse.md becomes a v3.0 stub (section map) so historical citations resolve.
- routes.json: PYQDraft/PYQScan/PYQApprove/PYQCount now load their step file +
  Framework_PYQCore.md; engine lists unchanged (CHECK AH green).
- Per-session spec read drops from 6,988 lines to 2,240–3,260 (−53% to −68%).
- The v2.0–v2.29 per-file changelog (1,248 lines) moved out of the runtime file into the
  ARCHIVE section at the bottom of this CHANGELOG. A token sweep verified every technical
  identifier in the deleted history is either present in the split body or was already
  history-only in the v2.29 body (nothing lost).
- Framework_PYQCore.md v1.0.1: audit_sync [ERA-SYNC] fired post-split because S2-3's
  prose mentions of OUT_OF_PATTERN landed in Core while the executable bc.OUT_OF_PATTERN
  call sites landed in Framework_PYQScan.md. Added an engine-sourcing comment to the
  S2-3 host note (scaffolding only; hosted v2.29 content remains byte-identical).
  All four audit scripts now report 0 findings.
- Housekeeping: mocktestframework_SKILL.md spec count 17→22 (and engine count 7→8, matching
  routes.json); CLAUDE.md stale "25 files" phrasing generalised; SPEC_MANIFEST.json and
  MANIFEST.json regenerated. Verified: bootstrap 31/31, validate_framework_md 0 issues
  across 22 files, check_triggers consistent. NOTE: the installed project skill
  (/mnt/skills/user/mock-test-framework/SKILL.md) must be replaced with the updated SKILL.md
  shipped with this release, or audit_sync/CHECK AA will keep reporting the stale 17-spec claim.

## 2026.07.29.3
- figural_core: RUNTIME DEPENDENCIES DECLARED, CHECKED AND NEVER FATAL IN AN AUDIT. Closes the
  hard-dependency note recorded in 2026.07.29.2. Step 0 installs python-docx and nothing else,
  and no spec declared a dependency list before v5.33, so the engine's extra needs would have
  been discovered as a traceback in a live exam session.
- Split by role, following "Silence is the defect; a halt is not the remedy": RENDER (Create)
  genuinely requires matplotlib, so render_figure() now raises FiguralError G-FIGDEP carrying
  the pip command instead of a bare ImportError from three frames down; AUDIT degrades every
  gate to DORMANT-but-reported, routed to AMBER by triage(). A gate that raises is worse than a
  gate that is absent, because it takes the whole audit down — and an audit that dies takes
  ~200 projects with it.
- New surface: DEPENDENCIES (matplotlib, PIL, numpy, scipy, fontTools with each one's role),
  PIP_INSTALL, and preflight() so a missing package is a stated precondition rather than a
  traceback. Guards IMPORT the module and catch failure rather than asking find_spec whether it
  is on the path — a package can be installed and still fail to load (numpy without BLAS,
  Pillow without its shared libs), and presence-checking leaves exactly the traceback the guard
  exists to prevent. dominant_hues()/coloured_fraction() now return None (not []) when pixel
  tooling is unavailable, so a caller can tell "no hues found" from "could not look".
- Self-test 56 -> 79. The absence fixtures block imports through sys.meta_path rather than a
  builtins.__import__ hook: an earlier version patched __import__ only, so nothing was ever
  blocked and all six cases passed against unguarded code — a test that proved nothing.
- Framework_MockTestCreate v5.33 documents the dependency surface (docs-only; version unchanged
  as behaviour is unaltered). MANIFEST.json + SPEC_MANIFEST.json regenerated.
- bootstrap 26/26, validator 0 issues, audit_deep 0, audit_callgraph 0, audit_specs_ext 0
  across 20 files; blueprint_core 266/266, corpus_io 303/303, figural_core 79/79.

## 2026.07.29.2
- GAP-2026-07-29-FIG-R2 + VERIFY-2026-07-29-FIG-R2 (figure colour, label legibility and
  placement scale). Measured across 208 delivered drawings in four exhibits: 0 of 55 IIT JAM
  figures contained a single coloured pixel; placement scale was 0.500 EXACTLY on 24 of 24
  option canvases; on-page labels ran to a median of 6.7 pt; 0 of 208 drawings carried alt
  text. The three GATE papers believed correct measured 115 of 153 figures below a 9 pt floor —
  not a working reference, only a quieter failure. Four root causes, not one, including RC-1
  (S10-7 Q7 MANDATED "solid black", so the monochrome output was CONFORMANT) and RC-4 (the
  corpus had exactly ONE figure helper, an abstract-geometry GLYPH renderer with no set_xlabel,
  no legend, no rcParams anywhere, being used to draw scientific data figures it structurally
  cannot label).
- NEW ENGINE (the 9th): figural_core.py — shared figure renderer + 12 conformance gates.
  The scale contract is now S == 1.0 BY CONSTRUCTION rather than by luck: display width is a
  LAYOUT decision, the render is solved to fit it, FIG_NATIVE_HEADROOM is retired to 1.0 (it
  was the sole source of the halving) and bbox_inches="tight" is banned (it made saved width a
  function of the figure's own content, so S wandered 0.495..0.666 across 27 canvas sizes).
  Okabe-Ito palette with REDUNDANT encoding (colour is never the sole carrier of meaning),
  pinned/normative CVD arithmetic, and a FigureSpec sidecar that makes a figure auditable
  without vision. Self-test 56/56 with day-one fixtures D1/D2/D5 that fail on the shipped
  defects. Tracked by gen_manifest (bootstrap 25 -> 26) and routed to the four
  Create/CreateAudit triggers.
- Severity model encodes the framework's own doctrine: no image-COLOUR condition may ever halt
  a run (AMBER — report loudly, force the amber footer, always complete); an answer-cue leak
  voids the ITEM not the run (VOID_ITEM); BLOCKING is reserved for renderer-contract
  REGRESSION on v5.33+ output, with EC-V18 downgrading it to AMBER for legacy output that has
  no sidecar, so all ~200 existing exams keep auditing. A gate that throws is worse than a gate
  that is absent — every gate tolerates a partial or empty spec and never raises.
- Specs: MockTestCreate v5.32 -> v5.33 (renders through the engine); MockTestCreateAudit
  v2.10 -> v2.11 (twelve new deterministic Part-A gates, correcting v2.10's over-generalisation
  that "auditing recorded intent, not pixels" applies to every figure property — it is true of
  SEMANTICS and false of colour presence, hue separation, scale and label size).
- HARD DEPENDENCY: figural_core's render path imports matplotlib UNGUARDED, so the four
  Create/CreateAudit triggers now require it at runtime (scipy and fontTools are used too but
  degrade gracefully). Confirm it is present in exam sessions.
- bootstrap 26/26, validator 0 issues, audit_deep 0, audit_callgraph 0, audit_specs_ext 0
  across 20 files; blueprint_core 266/266, corpus_io 303/303, figural_core 56/56.
  MANIFEST.json + SPEC_MANIFEST.json regenerated (35 files).

## 2026.07.29.1
- Debt closure — the three follow-ups recorded in the 2026.07.29 seal are closed, and no
  open debts remain.
- corpus_io v1.10 -> v1.11: (1) the ~300-line Cluster I table-structure addition is now
  RECORDED in its own changelog entry (third un-bumped occurrence, fixed); (2) Cluster I
  gains its missing fixtures — a gridSpan/vMerge table driven through _table_rows and
  read_table_spec (a fixture the old row.cells implementation fails) plus a flat-table
  identity check; (3) the long-open is_option/para_has_image fixtures land (bare-marker
  image options + OPT_PATTERNS cases, open since 2026.07.26.2). Self-test 273 -> 303.
- audit_specs_ext: V-SYNC now recognises a DELEGATION ADAPTER (a copy whose whole body
  calls or aliases the canonical engine copy) and skips it — parity holds by construction,
  and byte-comparing it false-fired on every adapter since the GAP-2026-07-25-002
  consolidation. Peer-window made bidirectional (a forward-only window silently compared
  nothing; verified by targeted mutation). First fully clean audit_specs_ext run across the
  corpus + engines: 0 issues across 19 files.
- All checkers green simultaneously: bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0, audit_specs_ext 0; blueprint_core 266/266, corpus_io 303/303.
  MANIFEST.json + SPEC_MANIFEST.json updated.

## 2026.07.29
- GAP-2026-07-29-TBL (table STRUCTURE survives the pipeline, both halves). The corpus could
  say what a table CONTAINS but never what a table IS: Step 1 S4-3 wrote cell.text into a
  rectangular add_table() and Step 7 S8-4 modelled a DI table as (headers, rows) — so a grouped
  header (a cell spanning four columns over a label spanning two rows) had exactly one
  representable form: squared into a grid and padded with empty strings. Measured on
  SSC_CGL_Tier1 09-Sep-2024 Shift 1: Q.52 and Q.61 each lost a 4-column header span and a
  2-row label span and gained 4 stray empty cells; the delivered Row file carried 0 gridSpan
  and 0 vMerge elements and passed 16/16 checks with a green footer, because no check had ever
  compared a built table with its source. Second defect, same family: one-table-PER-OPTION
  emission — adjacent w:tbl siblings are FUSED by every Word engine (19 tables written came
  back as 7 from a round-trip).
- corpus_io — new Cluster I (table structure): _table_rows rewritten to walk w:tr/w:tc with
  vMerge/gridSpan so a merged header is one anchor cell, never a repeat (flat-table output
  unchanged); new read_table_spec() + TableSpec builder as the ONE table model both steps use;
  legacy {'headers','rows'} DI payload accepted forever (no registry migration); font_name
  parameterised (Row-file contract stays Arial, Step 7 passes its FONT_NAME). Self-test 273/273.
- Specs: PYQPrepare v1.13 -> v1.14 (DI table structure, block composition, cell content —
  part 1); MockTestCreate v5.31 -> v5.32 (S8-4 rebuilt on Cluster I — part 2; two flat builders
  under one concept emit no drift signal until they disagree, so the model now lives once in
  the engine). routes.json: corpus_io.py routed to the Create steps. MANIFEST.json +
  SPEC_MANIFEST.json updated; bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0.
- Follow-ups (recorded, owner-accepted): Cluster I self-test fixture (a gridSpan/vMerge table
  that FAILS on the old row.cells implementation + flat-table byte-identity check) and a
  corpus_io version bump/changelog for the Cluster I addition; is_option fixture still open.

## 2026.07.27
- GAP-2026-07-27 (six defects found by six sessions on one corpus — IIT_JAM_BIOTECHNOLOGY,
  22 papers / 1,719 Qs; five sessions rediscovered the same vision defect and each invented a
  different workaround, while the one session that executed the python fences VERBATIM found a
  P0 no paraphrasing session hit). MockTestAnalyse v2.38 -> v2.39 carries the fixes, including:
  A — taxonomy Source-2 concatenated instead of merging (P0); B — build_vision_queue()
  overwrote its fixed-name outputs and was called per paper (P0), so a 22-paper run retained
  only the last paper's queue; D — XLSX-F9 compared a corpus total to a per-paper denominator
  (P1); E — MSQ under-detection originating in Step 3 (P2).
- GAP-2026-07-27-B (the B fix, both halves): corpus_io v1.8 -> v1.10 — build_vision_queue()
  is now IDEMPOTENT: it reads the existing vision_queue.json and unions prior items with the
  incoming batch, so re-runs and resumed sessions no longer destroy earlier papers' work;
  tag_width is pinned as a floor so surviving tags stay stable, and a genuine hash-collision
  re-tag is reported (tag_generation_changed), never silent. v1.10 adds `fresh=` so run-scoped
  callers (Step 1) can opt out of the union. Release-gate note: the first upload of this wave
  (v1.9) FAILED its own self-test 240/249 — the union broke nine CLUSTER V fixtures sharing
  one workdir — and was STOPPED at the gate; v1.10 isolates each fixture in its own workdir
  and adds positive union coverage. Self-test 273/273.
- PYQPrepare v1.12 -> v1.13 (caller-side half): VISION_WORKDIR was used at three call sites
  without being defined, so Step 1 silently inherited Step 5's workdir — hidden while
  corpus_io overwrote, surfaced by the union. Now defined, distinct per step, and fresh.
- GAP-2026-07-27-E: PYQSort v1.17 -> v1.18 — the ORIGINAL exam position now survives sorting.
  Step 3's taxonomy renumbering destroyed the exam position; Step 5's MSQ detector had only the
  instruction phrase left and measured 24 MSQ across 1,719 questions on an exam whose scheme
  reserves Q31-40 for MSQ (~120 expected), under-representing Section B corpus-wide.
- MANIFEST.json + SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0 issues,
  audit_deep 0, audit_callgraph (incl. C6) 0; blueprint_core 266/266, corpus_io 273/273.

## 2026.07.26.3
- GAP-2026-07-26-003 (EXECUTION-BOUNDARY LAW — a tool call cannot happen inside a running
  Python process). analyse_image_claude() and the vision-probe family were pass-bodied CLASS T
  stubs that a Python loop called and consumed, so vision was unreachable on every run of every
  exam and the literal code raised AttributeError — production silently executed a substituted
  body. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers / 1719 Qs): the four vision fields present
  on 0 of 1719 questions, 153/153 figural questions vision_unavailable, 45/45 FIGURAL subtopics
  shipping an empty object-type profile — with QV-9 PASS and a green Step-Complete footer.
- Fix — vision made reachable via MATERIALISE-THEN-INJECT (Phase A python emits a work queue,
  Phase B the model performs the view() tool calls in-turn as prose, Phase C python consumes the
  results): MockTestAnalyse v2.36 -> v2.38 (vision reachable, then probe family retired),
  PYQPrepare v1.10 -> v1.12 (S1-12 reachable, callback halt replaced), corpus_io v1.6 -> v1.8
  (Cluster V vision Phase A / observation I/O, then probe family deleted). A CLASS T failure is
  now LOUD but does NOT halt.
- GAP-2026-07-26-003 D2 (a measurement with no consumer is not a feature): Step 5 had measured
  each subtopic's real figure profile since v2.29, but Step 7 read only image_role — the semantic
  half was written and consumed by nothing for six minor versions. MockTestCreate v5.30 -> v5.31
  now reads the figure profile; MockTestCreateAudit v2.9.2 -> v2.10 adds gate A-FIGPROFILE.
- DeliveryFooter v1.7 -> v1.8: new §5 Q0 quality gate — any FAIL from a step's own checks forces
  an AMBER footer with the failing check and remedy named, instead of a green Step-Complete. WARN
  does not force amber. Reports, does not halt.
- Tooling / protocol: audit_callgraph gains C6 (model-agency-stub / EXECUTION-BOUNDARY LAW, scans
  every fence not just python-labelled ones); PYQAnalyse tagged its two judgment stubs # CLASS: J;
  CLAUDE.md adds the EXECUTION-BOUNDARY LAW and measurement-consumer guardrails. blueprint_core
  self-test 266/266, corpus_io 249/249; bootstrap 25/25, validator 0 issues, audit_deep 0,
  audit_callgraph 0.

## 2026.07.26.2
- GAP-2026-07-26-002 closed (image-option integrity + intra-spec wiring). Three parts:
- (1) is_option consolidated to ONE engine predicate (audit_deep [XSPEC-DRIFT]). v2.34/v2.35
  made is_option() image-option-aware in MockTestAnalyse only; the same-named copies in PYQSort
  and PYQAnalyse kept the text-only form while their docstrings still claimed alignment. Not
  cosmetic: PYQSort USES its copy to count options, so the defect fixed in Step 5 was live in
  Step 1 — measured on IIT_JAM_BIOTECHNOLOGY 2022, 156 options counted against 160 actual. Fix:
  corpus_io v1.5 -> v1.6 now owns is_option + BARE_OPT_PATTERNS + para_has_image as the single
  shared predicate; MockTestAnalyse v2.35 -> v2.36, PYQAnalyse v2.28 -> v2.29, PYQSort v1.16 ->
  v1.17 all delegate (is_option = corpus_io.is_option), and PYQSort passes the paragraph element
  at both call sites so image options are actually counted.
- (2) IMG-6 probe protocol hardened (PYQPrepare v1.9.1 -> v1.10). The v1.6 protocol was
  single-attempt/single-token and recorded nothing, while score_vision_probe() returned False on
  an empty string — so "I did not look" was indistinguishable from a blind session and produced a
  false session-terminating halt in Step 5 on first production use. Now 3 attempts, 3 distinct
  tokens, observation mandatory.
- (3) New auditor audit_callgraph.py (intra-spec call-graph): asserts every documented-required
  parameter is supplied at each call site, every multi-return function has one shape, and every
  public engine function is reached from executable spec code (not prose). Now tracked in
  SPEC_MANIFEST (33 -> 34 files). blueprint_core self-test 184/184; corpus_io 228/228.
- Follow-ups (recorded): add an is_option self-test fixture to corpus_io (bare-marker + OPT_PATTERNS
  cases); update audit_specs_ext's stale V-SYNC that false-fires on the delegation adapters.

## 2026.07.26.1
- GAP-2026-07-26-001 (a multi-paragraph stem is not a heading): PYQSort EC-S8 emits stems
  whose continuation lines are bold, not-date, not-option, not-next-question — character for
  character the level-3 taxonomy-heading predicate in `blueprint_core.is_taxonomy_heading()`.
  Level 3 is the only taxonomy level with no textual prefix, so boldness was its sole positive
  signal; the moment the producer emitted bold body text, a stem continuation and a subtopic
  heading became the same object. Two classes, one predicate, on opposite sides of the repo,
  never compared.
- Fix: `is_taxonomy_heading()` now takes the next paragraph's text (`is_taxonomy_heading(para,
  is_option, next_text)`) so a line followed by more stem body is no longer classified as a
  heading; MockTestAnalyse S3-2 passes `next_text` at both extraction loops — an older engine
  raises `TypeError` rather than silently truncating stems.
- Impact this closed was the silent half: Step 4's phantom-triple gate HARD STOPs loudly, but
  the extractor half kept question counts right (QV parity held, every gate passed) while
  truncating stems at the figure and orphaning every option after it — corruption that flowed
  into section_rules.md, the manifest, the Frequency xlsx, and on into Step 6 allocation and
  Step 7 generation. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers / 1719 questions): 20
  spurious headings across 10 papers, 128 counted triples vs 126 real, 2 phantom triples.
- Specs: Framework_MockTestAnalyse v2.32 -> v2.33, Framework_PYQAnalyse v2.27 -> v2.28.
  Engine: blueprint_core.py (self-test 178/178) — heading predicate gains the `next_text`
  parameter. MANIFEST.json + SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0
  issues across 17 files.

## 2026.07.26
- GAP-2026-07-25-003 (taxonomy read consolidated to ONE reader + lock gate reaches every
  consumer): the last hand-written and prose readers of the approved taxonomy are removed.
  Every step now loads through `corpus_io.load_taxonomy()` and asserts identity through
  `corpus_io.assert_taxonomy_lock()` — one implementation, called everywhere, instead of the
  four-plus transcriptions that produced GAP-2026-07-25-002. The read and the lock assertion,
  previously two calls (and in some steps two independent reads of the same artefact), collapse
  to a single call at each site.
- Preferred source moves from the Analysis Word document to `approval_record.json`: where the
  record carries the taxonomy (reconcile_taxonomy >= v1.3) the consuming steps parse no Word
  document at all; pre-1.3 records fall back to the doc, fully gated, and need no re-run.
- Specs: Framework_Blueprint v1.39 -> v1.41 (S2-2 asserts the lock, then loads through
  load_taxonomy — Step 6 was the worst place for a silently-wrong taxonomy); Framework_MockTestAnalyse
  v2.30 -> v2.32 (both Step-5 readers gated then load through load_taxonomy; a second latent
  defect in `_extract_taxonomy_tuples_from_*` fixed while wiring the gate); Framework_PYQAnalyse
  v2.24 -> v2.27 (Task 2.5 was the last hand-parser — read/write through Cluster K, lock delegated
  to the shared gate, then load through load_taxonomy); Framework_PYQSort v1.14 -> v1.16 (taxonomy
  loaded once from JSON where available; S1-0b/S1-2 collapse to one call; ingest form surfaced,
  EC-S20/S21 recorded).
- Engines: reconcile_taxonomy.py (self-test 69/69) records the approved taxonomy inside
  approval_record.json beside its validating fingerprint; corpus_io.py -> v1.4 (self-test 226/226)
  owns `load_taxonomy()` + `assert_taxonomy_lock()` as the single reader/gate. MANIFEST.json +
  SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0 issues across 17 files.

## 2026.07.25.2
- GAP-2026-07-25-002 (Analysis-doc reader delegation): MockTestAnalyse v2.29.1 -> v2.30
  delegates both Analysis-doc readers (score_difficulty / determine_strip_mode) to
  blueprint_core Cluster E — the byte-identical second copy is replaced by a thin adapter,
  so one definition is called from both places. Blueprint v1.38 -> v1.39 (S2-2 reader
  delegated), PYQAnalyse v2.23 -> v2.24 (S4-2 de-stubbed, taxonomy attested, name-length
  gate), PYQSort v1.13 -> v1.14 (reader delegated + S1-0b content cross-check).
- Engines: blueprint_core (164/164), corpus_io (138/138), reconcile_taxonomy (59/59),
  validate_framework_md.py — +batch checks AF (deliverable-filename contract) and AG
  (shared-artefact readers); Check Z widened to the engine's whole public surface.
- routes.json: engine routing broadened across the PYQ steps. CLAUDE.md: guardrails added —
  deliverable rename/cardinality is a cross-step contract change; a shared artefact has ONE
  reader; producer-enforced bounds. MANIFEST.json + SPEC_MANIFEST.json regenerated.

## 2026.07.25.1
- GAP-2026-07-25-001 (S4-0 silent check-skip): reconcile_taxonomy.py v1.0 -> v1.1 — the
  early `return` inside C4's style-aware branch that disabled C5/C6/C7 for every
  syllabus_style exam is removed; reconcile() is now SINGLE-EXIT. Adds CheckLedger
  (INV-7 completeness, INV-8 measured-domain), materialise() (INV-9 no-derivation,
  INV-10 resolvable-target), DEGRADED mode, C6 scale-relative, C4 normalized subject
  match; self-test 54/54. PYQAnalyse v2.22.1 -> v2.23 (S4-0 check-completeness
  architecture). PYQSort v1.12.2 -> v1.13 and DeliveryFooter v1.6 -> v1.7 wire the
  [ExamCode]_approval_record.json contract (produced at Step 2c, consumed at PYQSort entry).
  validate_framework_md.py +Check AC (aggregator single-exit) so the drift cannot return;
  routes.json routes reconcile_taxonomy.py to PYQApprove.
- CLAUDE.md release-manager protocol updated: corpus-level checks AA-AE are part of the
  gate; "a red check is never advisory"; corrected engine-load model (engines load from
  the repo clone, /mnt/project is data-only, no per-project provisioning). SPEC_MANIFEST.json
  33-file workbench baseline regenerated to match production.

## 2026.07.25
- NEW audit_sync.py — cross-step synchronisation auditor (engine-API, trigger/route/SKILL
  parity, version xrefs, filename chain, blueprint.json schema). Untracked dev tool.
- PYQAnalyse v2.16 -> v2.22.1 + 3 NEW engines: corpus_io.py (Drive acquisition / image
  integrity / size governor), reconcile_taxonomy.py (S4-0), syllabus_provenance.py (S2-3e);
  blueprint_core.py +Clusters F-J (pattern-era, taxonomy parse, acquisition, image-gate,
  size governor; self-test 57 -> 164). Tracked set 21 -> 24.
- Corpus-transport migration wave: NEW spec PYQCompress v1.0 (Layer-2 doc size remediation;
  new trigger, tracked set -> 25); Blueprint v1.35 -> v1.38, MockTestAnalyse v2.24.10 ->
  v2.29.1, MockTestExplainAudit -> v1.16.1, PYQPrepare -> v1.9.1, PYQSort -> v1.12.2,
  PYQExplain -> v1.1, PYQExplainAudit -> v1.1.1, PYQFormat -> v1.4.1, PYQDeliver -> v1.5.1
  (delegate engine-owned functions to blueprint_core/corpus_io; remove local copies).
  validate_framework_md.py +5 checks (V-DRIVEGUARD/W-ENUMSIZE/X-DURABILITY/Y-IMGGATE/
  Z-DELEGATION). NEW audit_deep.py (deep drift/delegation/table-parity auditor).
- PYQCompress v1.0 -> v1.1 + corpus_io v1.0.1 -> v1.0.3 (v1.0.2 media-stem-collision fix
  [silent figure loss]; v1.0.3 optimize_docx always= param). Shipped as an atomic pair.

## 2026.07.23.1
- blueprint_core.py +Cluster E — score_difficulty / determine_strip_mode /
  map_difficulty_level, the canonical shared difficulty scorer for Step 5 and PYQ-4.
  Self-test 33 -> 57 PASS; byte-identical to MockTestAnalyse E-9/E-10 (V-SYNC verified).
- NEW audit_specs_ext.py — supplementary corpus auditor (V-SYNC cross-file parity,
  W-DECISION decision-ID integrity, X-NUMBER list contiguity, Y-CONFIG field-contract,
  Z-VERSION full 3-part compare). Untracked dev tool; 0 issues across the corpus.
- Framework_PYQDeliver.md v1.0 -> v1.2.1: date/session tag removal (§4A), three-tier
  deterministic Complexity resolver via blueprint_core Cluster E (D11 supersedes D4),
  adversarial audit fixes (marks_default declared, JSON int-key normalization,
  difficulty_labels fallback). RELEASE-MANAGER FIX: converted blueprint_core.py sourcing
  from /mnt/project-only to dual-path (/tmp/fw first, else /mnt/project) so GitHub-connected
  projects no longer HARD STOP. routes.json: PYQDeliver now lists blueprint_core.py.
- Framework_MockTestAnalyse.md v2.24.9 -> v2.24.10: annotation-only (E-9/E-10 canonical
  copy moved to blueprint_core Cluster E; zero logic change).
- routes.json reformatted to the generator's pretty-printed emit style (no functional change).

## 2026.07.23
- Framework_PYQFormat.md v1.0 -> v1.3 (PYQ-3, self-contained formatter):
  v1.1 removes the per-question date/session tag paragraphs (only sanctioned deletion);
  v1.2 restyles explanation tag headers into colored bands + marker-glyph swaps
  (⬛->📘/🧮, ❌->⚠️), machine-verified by a full text-stream integrity check (S8-8);
  v1.3 promotes the exam header + IFAS footer to real page header/footer parts that
  repeat on every page, and updates the footer tagline. Trigger/step unchanged; no
  framework engine; bootstrap stays 21/21.

## 2026.07.22
- NEW PYQ Explanation Pipeline — 4 specs: PYQExplain (PYQ-1), PYQExplainAudit (PYQ-2),
  PYQFormat (PYQ-3), PYQDeliver (PYQ-4). Wired into routes.json / PIPELINE / skill
  (19 -> 23 triggers); tracked set 17 -> 21 (bootstrap now 21/21). PYQ-1/PYQ-2 reuse
  explain_engine.py (+ explain_audit_gate.py for PYQ-2); PYQ-3/PYQ-4 are self-contained
  (write their own format_pipeline.py / pyq_deliver_pipeline.py, no framework engine).
- validate_framework_md.py — S2-EXPLAINGATE now fires on an actual gate invocation
  (`explain_audit_gate.py --`) or the AUDIT-COMPLETION-GATE output, not on a bare name-drop,
  so specs that only DISCLAIM the gate (PYQ-1 delegation note; PYQ-3/PYQ-4 NOT-REQUIRED
  lists) no longer false-positive. Genuine gate-users (Step 10 / PYQ-2) still fully checked.
- GAP-2026-07-22-001 section<->subject mapping chain (shipped atomically):
  MockTestCreate v5.29 -> v5.30 (position-based question-type dispatch, §6);
  MockTestCreateAudit v2.9.1 -> v2.9.2 (position-based question-type in audit);
  MockTestAnalyse v2.24.8 -> v2.24.9 (BUG 1 — sections[].subjects);
  Blueprint v1.34 -> v1.35 (BUGS 2-4 — section<->subject mapping);
  ScopedBlueprint BLUEPRINT_SCHEMA_VERSION 1.23 -> 1.35 (schema sync to Blueprint);
  DeliveryFooter Step 5 deliverable-count doc fix (5 -> 6 files).
- routes.json — PYQ explanation triggers reordered to end (no functional change; syncs the
  repo to the generator's emit order).

## 2026.07.21
- NEW engine paper_pipeline.py — shared naming/numbering/registry plumbing for Steps 6-11
  (self-test 37/37; added to tracked set -> bootstrap now 17/17). Added 5 Test* trigger aliases
  (TestCreate/TestCreateAudit/TestExplain/TestExplainAudit/TestDeliver -> 19 triggers), wired into
  routes.json / PIPELINE / skill.
- Specs: MockTestCreate v5.29, MockTestCreateAudit v2.9.1, MockTestExplain v1.20, MockTestExplainAudit
  refresh; Blueprint v1.32 -> v1.34; MockTestAnalyse v2.24.7 -> v2.24.8; PYQAnalyse v2.15 -> v2.16;
  MockDeliver v1.8 -> v1.9; ScopedBlueprint v1.5 -> v1.7.
- Added manifest_to_taxonomy_xlsx.py (untracked helper: subtopic_manifest.json -> taxonomy Excel).

## 2026.07.20
- explain_engine.py core self-test 44/44 -> 62/62 (audit stays 10/10). MockTestExplain -> v1.18 and
  MockTestExplainAudit P0 corrected to 62-of-62, so Step 9/10 pre-flight demands exactly what the
  engine prints. Deployed as a version-matched bundle (engine + both Explain specs).
- MockTestCreate v5.24 -> v5.27; MockTestCreateAudit v2.7.6 -> v2.8.1; MockTestExplain v1.15 -> v1.18;
  MockTestExplainAudit v1.8 refresh; MockDeliver v1.7 -> v1.8.

## 2026.07.18.1
- Framework_MockDeliver.md v1.6 -> v1.7.

## 2026.07.18
- validate_framework_md.py -> v2.8: adds Check T (cross-file token contract) and Check U (JSON
  producer/consumer field contract); generalises cross-file RA/MANDATE anchor resolution; drops
  the "equivalent"-exemption now that the MANDATE 8/9 prose is root-fixed in the specs.
  Re-added 'ScopedBlueprint': '6S' to the PIPELINE dict.
- Framework_MockTestCreate.md, Framework_MockTestAnalyse.md, Framework_PYQAnalyse.md,
  Framework_MockTestCreateAudit.md updated (MANDATE 8/9 "equivalent" prose removed at source).

## 2026.07.17.1
- Dual-path engine sourcing: Blueprint (Step 6), ScopedBlueprint (Step 6S), MockTestExplain
  (Step 9), MockTestExplainAudit (Step 10) now load their engines (blueprint_core.py /
  explain_engine.py / explain_audit_gate.py) from the framework clone (/tmp/fw) with fallback
  to the project Files (/mnt/project). GitHub-connected projects no longer need the engines
  uploaded to their Files; direct-upload projects continue to work.
- Framework_Blueprint.md v1.31 -> v1.32 (dual-path gate now in the spec source);
  Framework_MockTestAnalyse.md v2.24.5 -> v2.24.6; Framework_MockTestCreateAudit.md v2.7.3 -> v2.7.4.

## 2026.07.17
- NEW spec Framework_ScopedBlueprint.md v1.5 (Step 6S — scoped subject/topic/subtopic test
  blueprints). Wired into routes.json / PIPELINE / skill (14 triggers).
- NEW shared engine blueprint_core.py (added to the tracked set; self-test 33/33). Bootstrap
  count is now 16/16. Framework_Blueprint.md v1.27 -> v1.31 (allocation math extracted into
  blueprint_core.py). NOTE: blueprint_core.py must be uploaded to each project's /mnt/project/
  or Step 6/6S HARD STOPs (operational, outside this repo).
- Framework_MockTestAnalyse.md v2.24.2 -> v2.24.5.
- Framework_MockTestCreate.md v5.20 -> v5.23; Framework_MockTestCreateAudit.md v2.7.2 -> v2.7.3;
  Framework_MockDeliver.md v1.5 -> v1.6.
- Framework_MockTestExplain.md v1.14 -> v1.15; Framework_MockTestExplainAudit.md v1.8 refresh.

## 2026.07.14
- Framework_PYQPrepare.md: v1.6 -> v1.7.
- Added mocktestframework_SKILL.md — canonical account-level skill (STEP 0 load-and-verify
  bootstrap; trigger list synced to the live 13-trigger routing). Added an explicit no-DR-mirror
  guard that hard-stops when MIRROR == PRIMARY instead of silently re-cloning the same URL.
- Added check_triggers.py — enforces that the skill trigger list, routes.json, and the validator
  PIPELINE dict stay in sync; wired into CI (validate.yml) so drift fails the build.
- Deprecated docs/CUSTOM_INSTRUCTIONS.md to a pointer at the skill (single source of truth).

## 2026.07.12
- Deliverable filename rename across the delivery contract and the Create/Explain/Deliver
  specs: Step 7 -> Create, Step 8 -> Create_Complete, Step 9 -> Explanation,
  Step 10 -> Explanation_Complete, Step 11 -> Final.
- Specs updated to: MockTestAnalyse v2.24.2, MockTestCreate v5.20, MockTestCreateAudit v2.7.2,
  DeliveryFooter v1.6, MockTestExplain v1.14, MockTestExplainAudit v1.8 (content refresh),
  MockDeliver v1.5.
- validate_framework_md.py: permanently exempt "MANDATE/RA N equivalent" descriptive phrasing
  from the anchor checks (O-MANDATE/N-RA false-positive fix; genuine dangling refs still caught).
- MockDeliver: fixed stray internal "End of v1.3" marker.
- Added CLAUDE.md documenting the release-manager protocol (approved_framework, seal_release,
  guardrails) so future sessions inherit it.

## 2026.07.11
- Framework_MockTestAnalyse.md: v2.24 -> v2.24.1
- Framework_Blueprint.md: v1.27 content refresh
- Framework_MockDeliver.md: v1.3 -> v1.4
- Framework_MockTestExplain.md: v1.12 -> v1.13
- Framework_MockTestExplainAudit.md: v1.7 -> v1.8
- explain_engine.py: FIGURE-section tests replaced with FIGURAL-NO-FIGURE-SECTION regression lock (self-test 44/44, audit 10/10)
- routes.json: 10 -> 13 triggers (Framework_DeliveryFooter.md on all routes; Blueprint renamed to MockBlueprint; new PYQDraft/PYQScan/PYQApprove; engine deps on explain routes)
- tooling: validate_framework_md.py hardened (word-boundary stale markers, corpus-wide MANDATE/RA anchor resolution, accepts "vX changes:" changelog format); CI gates validator on Framework_*.md and installs python-docx; .verified gitignored; auto-manifest workflow removed

## 2026.07.10
- Initial release of the version-pinned, integrity-verified framework repo.
- 11 .md specs + 3 .py engines/gates under load-and-verify gate (bootstrap.py).


# ═══ ARCHIVE — Framework_PYQAnalyse v2.29 pre-split header & changelog (moved 2026-07-31; verbatim) ═══

# Framework_PYQAnalyse v2.29 — Universal PYQ Analysis & Taxonomy Builder
#
# MINIMUM COMPANION VERSIONS (v2.28):
#   corpus_io.py          >= v1.4   — load_taxonomy() IS Task 2.5's loader and gate;
#                                     Cluster K write_analysis_doc() IS S4-2,
#                                     read_analysis_doc() IS Task 2.5's reader and
#                                     assert_taxonomy_lock() IS its identity gate, and
#                                     read_analysis_doc() IS Task 2.5's reader. v1.2
#                                     adds INGEST FORMS: the Analysis doc is stored in
#                                     project Files as extracted TEXT, so under v1.1
#                                     Phase B cannot read it at all (GAP-2026-07-25-003).
#   reconcile_taxonomy.py >= v1.3   — S4-0 passes final_taxonomy=, and v1.3 RECORDS it
#                                     so Steps 3-6 need no Word document at all; older
#                                     builds accept
#                                     no such argument and raise TypeError.
#   blueprint_core.py     — MAX_HEADING_LEN for the S4-0 name gate; and the
#                           GAP-2026-07-26-001 build carrying next_nonempty_texts()
#                           and is_taxonomy_heading(para, is_option, next_text).
#                           S5-2 PASSES next_text; on an older engine that raises
#                           TypeError rather than silently miscounting.
#
# v2.29 — 2026-07-26 — is_option DELEGATED (audit_deep [XSPEC-DRIFT]).
#   This file defined its own is_option() with a docstring claiming alignment with
#   Step 5. No executable call site was found for it here, so the copy could not
#   misbehave — but it was drift bait, and it went stale the moment MockTestAnalyse
#   v2.34/v2.35 added the image-option path. Delegated to corpus_io >= v1.6 rather
#   than deleted, so a future call site in this spec inherits the correct predicate
#   instead of silently reintroducing the text-only one.
#
# v2.28 — 2026-07-26 — GAP-2026-07-26-001: A MULTI-PARAGRAPH STEM IS NOT A HEADING.
#          PYQSort EC-S8 defines a stem continuation as "bold + not-date + not-option
#          + not-next-Q". blueprint_core.is_taxonomy_heading() defined a taxonomy
#          heading as the same four conditions. Two different objects, one predicate,
#          on opposite sides of the same repository, never compared. Level 3 is the
#          only taxonomy level with no textual prefix, so bold was its only positive
#          signal — and the moment the producer began emitting bold body text the two
#          classes became the same object.
#          MEASURED, IIT_JAM_BIOTECHNOLOGY, 22 papers / 1719 questions: 20 spurious
#          headings across 10 papers; 128 counted triples against 126 real ones; 2
#          phantom triples; Task 2.5 HARD STOP. The question total and the orphan
#          count were both CORRECT throughout (1719 / 0) — nothing was lost, only
#          mis-filed — which is why Task 2.5 was the only gate that could catch it.
#          FIX (S5-2): count_sorted_file() builds bc.next_nonempty_texts() once per
#          document and passes next_text. A bare level-3 heading is genuine only when
#          the next non-empty paragraph is a DATE LABEL — guaranteed exam-agnostically
#          by PYQSort S6-2, CHECK 3 and EC-S10. Levels 1 and 2 are exempt (prefixed,
#          self-identifying). Verified on the full corpus: 1244/1244 genuine headings
#          preserved, all 20 spurious ones rejected, 1719 questions and 0 orphans
#          unchanged, triples 128 -> 126, phantoms 2 -> 0.
#          ALSO §6: added the QUESTION (multi-paragraph) class. Its absence WAS the
#          defect — §6 described a question as a single paragraph while EC-S8 emitted
#          several, and everything downstream inherited the wrong one.
#          ALSO S5-4b: Task 2.5 now TRIAGES phantoms into misread-stem vs genuine
#          name-mismatch. It previously asserted one cause and offered only the
#          name-mismatch remedies; against a misread stem "re-sort" is a no-op that
#          reproduces the file byte for byte, and "update the Analysis doc" writes a
#          question stem into the locked taxonomy — the exact defect D6-1 blocks.
#          The operator had no valid exit and the run halted permanently.
#
# v2.27 — 2026-07-26 — TASK 2.5 LOADS THROUGH load_taxonomy(). The read and the
#          identity assertion were two calls; they are now one, and the taxonomy is
#          taken from approval_record.json where the record carries it
#          (reconcile_taxonomy >= v1.3) rather than from a Word document. Pre-1.3
#          records fall back to the doc, fully gated, and need no re-run.
#          Companion rises to corpus_io.py >= v1.4.
#
# v2.26 — 2026-07-26 — TASK 2.5's LOCK CHECK DELEGATED TO THE SHARED GATE.
#          v2.25 gave Step 4 a fingerprint identity gate by writing the comparison
#          into the spec. Steps 5 and 6 then needed the same claim, so it now lives
#          once in corpus_io.assert_taxonomy_lock() and Task 2.5 calls it like
#          everyone else. No behaviour change: same two hard stops, same messages,
#          same operator actions — one implementation instead of four. Companion
#          requirement rises to corpus_io.py >= v1.3.
#
# v2.25 — 2026-07-26 — PHASE B READS AND WRITES THROUGH CLUSTER K (GAP-2026-07-25-003).
#          Step 4 was the LAST hand-parser of the Analysis doc. GAP-2026-07-25-002
#          consolidated four independent readers into corpus_io Cluster K, but the fifth
#          reader was PROSE — S5-4b Task 2.5 instructed Claude to extract section names
#          from a header line, topic names from master-summary cells and subtopic names
#          from per-topic cells, by hand. Prose is invisible to validate_framework_md
#          CHECK AG, which only inspects ```python blocks, so the consolidation could not
#          see it and it survived. Two consequences, both now fixed:
#            (1) Step 4 fails on GAP-2026-07-25-003 at its OWN call site. The Cluster K
#                ingest-form fix does not reach a reader that never called Cluster K, so
#                Phase B would have halted one step after PYQSort started working.
#            (2) Task 2.5's whole purpose is BYTE-IDENTICAL name agreement between the
#                Analysis doc and count_sorted_file(). Two hand-written extractions of the
#                same names is precisely how they drift. Both sides now derive names from
#                blueprint_core.parse_taxonomy_level() through one reader.
#          S5-5 Task 3 changes shape for the same reason. It described EDITING the doc in
#          place — replacing "—" cells and re-totalling. That is impossible now: the
#          runtime receives extracted text, which has no cells to edit, and /mnt/project/
#          is read-only. Task 3 becomes PARSE -> MERGE COUNTS -> REGENERATE through
#          write_analysis_doc(counts=), which the module has accepted since v1.1. This is
#          strictly stronger than the old rule: the writer computes the subtopic cell, the
#          per-topic TOTAL, the master-summary Total PYQs, the GRAND TOTAL and the header
#          total from ONE counts map, so the four levels cannot disagree by construction
#          rather than by checking. Verified end to end on the first real exam: 6/26/131,
#          all four levels equal, zero cells left as "—", fingerprint unchanged.
#          NEW GATE — Task 2.5 now asserts the Analysis doc against the approval record's
#          taxonomy_fingerprint before using it, the same cross-check PYQSort S1-0b makes.
#          Step 4 had NO identity gate: it verified that the doc agreed with ITSELF and
#          never that it was the doc that was APPROVED, so a superseded Analysis doc left
#          in project Files would have been counted into silently.
#
# v2.24 — 2026-07-25 — S4-2 DE-STUBBED + TAXONOMY ATTESTED + NAME-LENGTH GATE
#         (GAP-2026-07-25-002). Three changes, one theme: this step produces the artefact
#         the rest of the pipeline is built on, and it neither defined it nor attested it.
#         (1) S4-2 generate_merged_analysis_doc() was `pass`, deferring to "the npm docx
#             package per SKILL.md". The Analysis doc therefore had NO definition anywhere,
#             so its four consumers each guessed at a different structure and three guessed
#             wrong. It now delegates to corpus_io.write_analysis_doc() — THE writer, paired
#             with THE reader, asserted against each other by round-trip over a GENERATED
#             matrix of exam shapes (corpus_io --self-test). The framework serves ~200 exams
#             and cannot be validated against 200 real corpora; that matrix is the claim.
#         (2) S4-0 now passes final_taxonomy to build_approval_record(), which records a
#             taxonomy_fingerprint (reconcile_taxonomy v1.2, schema 1.2). Until now the
#             record proved the reconciliation RAN and said nothing about WHAT it locked, so
#             PYQSort could verify the lock was earned and still sort against a different
#             taxonomy — which is precisely what happened. Verified at PYQSort S1-0b.
#         (3) S4-0 HARD STOPS before locking when any subject/topic/subtopic name reaches
#             blueprint_core.MAX_HEADING_LEN. That bound governs whether text is recognised
#             as a heading in the sorted files and was enforced NOWHERE upstream: proven by
#             execution, a 131-character subtopic name written here survived PYQSort and then
#             silently stopped being a heading at Steps 4 and 5, with its questions
#             attributed to the PRECEDING subtopic — zero orphans, INV-5 conservation still
#             passing, because nothing was lost, only mis-filed. Raised 100 -> 300 and now a
#             named constant the producer and the consumer share.
#         Also corrects the v2.6 entry's false downstream-compatibility claim in place.
# v2.23 — 2026-07-25 — S4-0 CHECK-COMPLETENESS ARCHITECTURE (GAP-2026-07-25-001).
#         reconcile() returned from INSIDE C4's style-aware branch, so C5 (near-duplicate),
#         C6 (over-aggregation) and C7 (anchoring) never ran for ANY exam carrying a
#         syllabus_style record — i.e. every PYQDraft >= v2.17 exam, which is the default
#         path, not an edge case. The record then reported CLEAN with an empty anchoring
#         block and AUTO-LOCKED the taxonomy. A missing finding is worse than a crash: it
#         is indistinguishable from a passing check.
#         (1) TIER 0 table: C7 DOCUMENTED for the first time (its four classes were emitted
#             by the engine and REQUIRED by the S4-4 gate template while appearing in no
#             spec at all); C4's two mutually exclusive forms and their real thresholds
#             stated; list declared EXHAUSTIVE, CLOSED and INDEPENDENT; single-exit engine
#             contract stated.
#         (2) INV-7 CHECK_COMPLETENESS, INV-8 CHECK_MEASURED, INV-9 NO_DERIVATION_AT_S4_0
#             added. INV-8 exists because execution attestation alone is NOT sufficient —
#             C4 matched subjects with raw `==` while every other comparison normalized, so
#             a subject differing only in case or spacing passed C1 and then silently zeroed
#             C4's measurement domain. The check "ran" and measured nothing.
#         (3) INV-9: ADD_SECTION / ADD_SUBTOPIC (safe defaults for SUBJECT_MISSING and
#             ITEM_UNMAPPED — the data-loss class) were never materialised AND never held
#             the run, so a syllabus subject could be dropped while the taxonomy auto-locked
#             CLEAN_ADJUDICATED. They now HOLD for PYQDraft re-derivation.
#         (4) EXECUTION block: verdicts, final_taxonomy and quarantined_paths DEFINED; the
#             missing MATERIALISE step specified; ROUTING directive added.
#         (5) R1 mode B: check list corrected to C3 + C5 + INV-5. C4 is provenance-DEPENDENT
#             (both forms divide by a syllabus-derived base), so with no provenance the
#             divisor collapses to 1 and every DEGRADED run would be falsely HELD.
#             locked_taxonomy is now REQUIRED.
#         (6) C6 made SCALE-RELATIVE (items-per-topic density). The absolute rule encoded one
#             exam's scale and false-fired on legitimately small exams; because its safe
#             default is RE_DERIVE, a false fire is a hard block.
#         (7) S4-4 Branch A: ratio line is now FORM-AWARE; checks executed/skipped printed.
#         (8) S4-1 SUBJECT ORDERING: alphabetical fallback replaced by taxonomy order —
#             sections[] are OTS labels (S2-2a SECTION != SUBJECT), so the intersection is
#             empty for every non-marker_mode exam and the "rare" fallback was the norm.
#         (9) §12 Phase 0c: "EXACTLY 2 files" -> 3; stale benchmark-count line replaced;
#             INV-7/8/9 gate items added.
#        (11) INV-10 RESOLVABLE_TARGET added. materialise() matched destructive verdicts
#             against the finding's `item`, which is a path only for PATH_EXTRA — and
#             PATH_EXTRA is resolved at Tier 1 and never reaches a destructive verdict.
#             Every destructively-adjudicable class carries a description, subject name or
#             raw syllabus text, so DROP/SUPPRESS/MERGE_INTO removed nothing while the
#             record asserted the path was dropped. The taxonomy was never harmed; the
#             RECORD lied. Unresolvable destructive actions now block and HOLD.
#        (10) S4-4 Branch A: PRIOR DECISIONS line added. INV-6 replay was already
#             recorded in the JSON (prior_record_attested, engine_version) but printed
#             nowhere, so a verdict reused from an older engine was invisible to the
#             operator, whose only interface to a run is the gate text. Same shape as
#             the write-only approval_record this release closes at PYQSort S1-0.
#         Enforced statically by validate_framework_md.py Checks AC (aggregator single-exit),
#         AD (emitted finding-class documented) and AE (normalization conformance).
# v2.22.1 — 2026-07-25 — PRE-SCAN GATE Q_PATTERNS CORRECTED. The inline copy in the Step 2b
#         confirmation gate listed five patterns "from Step 5 E-2" and was used to COUNT
#         questions per file. Counting a normalised Row file with the bare-number pattern counts
#         every option as a question — the gate would have reported roughly five times the true
#         total and the operator would have confirmed it. Corrected to the engine's two.
# v2.22 — 2026-07-25 — DEFECT C AT STEP 2b + v2.21 RATIONALE CORRECTION.
#         (1) Step 2b (PYQScan) carried the SAME batch-level durability defect that v2.21
#             fixed at Step 4. S3-5's per-paper loop calls scan_paper(), appends to
#             papers_scanned_list, increments papers_scanned, records years_covered and
#             adds every newly discovered subtopic to the taxonomy — all in memory — while
#             save_scan_progress ran only AFTER the loop. An exception on paper 3 therefore
#             discarded papers 1 and 2 together with their discoveries, and the progress
#             file showed them as never scanned. Found by validate_framework_md.py v3.0
#             Check X (per-item durability), not by reading: the same shape had been fixed
#             twice already and still went unnoticed here, which is the entire argument for
#             encoding a defect as a check rather than as a memory.
#             Fix: save_scan_progress + save_classifications inside the per-paper loop.
#             Convergence is untouched — consecutive_empty_batches is a per-BATCH,
#             complete-batches-only counter, and EC-P26 already specifies that a partial
#             batch persists its papers without affecting it. BATCH_SIZE unchanged.
#         (2) CORRECTION to v2.21. That entry justified the Step 4 fix with "the failure
#             mode is a silent undercount". It is not. Counts and files_processed_list are
#             written by the same save, so a skipped save loses both and the resume simply
#             recounts those files — the total comes out right, and S5-4a would catch it if
#             it did not. The real costs are lost work, a progress file that understates
#             what was done, and a latent double-count if the accumulator and the
#             processed-list are ever persisted at different moments. The fix stands; the
#             stated reason was overclaimed and is corrected in S5-4. An inflated rationale
#             invites a future reader to check it, disbelieve it, and discount the rule.
#
# v2.21 — 2026-07-25 — STEP 4 CORPUS TRANSPORT (DEFECTS A, B, C, N + O at Step 4).
#         Twin of Framework_MockTestAnalyse v2.29 / Framework_PYQSort v1.12 / corpus_io v1.0.1.
#         Step 4 (PYQCount) and Step 5 (PYQExtract) fetch the SAME corpus from the SAME Drive
#         folder through the SAME connector, and Step 4 carried every one of the defects that
#         took Step 5 down on 2026-07-24 — it had simply not been run far enough to hit them.
#         (1) DEFECT C (CRITICAL) — count_progress.json was saved AFTER each batch, not after
#             each file (S5-4 item 7). process → accumulate → save is the only thing that
#             persists a file's counts, so ANY exception inside the loop skipped the save and
#             discarded every file already counted in that batch, with no trace: the progress
#             file shows them as never processed and a resume silently recounts them. At
#             BATCH_SIZE_COUNTS = 5 that is up to FOUR papers of work lost per failure. This
#             is the same defect that made the Step 5 incident destructive. (v2.21 stated the
#             consequence as "a silent undercount"; v2.22 corrects that — see below.)
#             Fix: save inside the per-file loop, immediately after each file is counted. The
#             batch-level save REMAINS as a redundant flush. BATCH_SIZE_COUNTS = 5 is
#             UNCHANGED — batching is the user-facing pacing unit, never the durability unit.
#         (2) DEFECT A — enumeration discarded fileSize. The Drive listing carries it inline,
#             already in the response, and S5-1 read only the name. With size unknown there is
#             no pre-flight partition, so a paper above the connector's 10 MiB cap cannot be
#             known to be unfetchable until the download is attempted — which in the reported
#             incident happened at batch 6 of a clean-looking run. Enumeration now records
#             {id, name, mimeType, fileSize, parentId, source} and screens every entry:
#             native Google Docs, Drive shortcuts and legacy .doc are REJECTED WITH A REASON
#             instead of vanishing, and a paper with no reported size is rejected rather than
#             silently processed.
#         (3) DEFECT B (CRITICAL) — the download was unguarded. Verified across the corpus:
#             ZERO try/except existed around any Drive call anywhere. Every fetch now goes
#             through corpus_io.fetch_drive_docx; every failure — size, permission, network,
#             malformed payload, unknown — raises TransportFallback and routes that paper to
#             the UPLOAD LANE. A transport failure is NEVER fatal to the run. This is what
#             makes Step 4 survive a future change to the connector's cap: correctness rests
#             on the fallback being taken, not on the predicted partition being right.
#         (4) DEFECT N — the retrieval envelope is documented for the first time. For any real
#             paper the connector's result exceeds context and spills to
#             /mnt/user-data/tool_results/*.json; that file is a LIST whose [0]['text'] is
#             itself a JSON STRING which parses to {id, title, mimeType, content} with content
#             base64. Every previous execution rediscovered this by trial and error with a
#             different improvisation each time — non-determinism in the hot path. One
#             implementation now: corpus_io.decode_drive_payload, followed by a byte-count and
#             PK magic assertion, because a payload truncated at a ZIP member boundary still
#             opens as a valid archive while presenting fewer questions.
#         (5) DEFECT O at Step 4 — the duplicate rule actively selected the unfetchable file.
#             S5-1 kept the LARGER of two sorted files for the same date+session on the
#             reasoning that it was "more likely to have images intact". Under a 10 MiB
#             download cap that rule picks precisely the copy that cannot be fetched, and
#             under Phase B's zero-tolerance standard picking EITHER copy silently is wrong:
#             a re-sorted paper and its superseded predecessor differ in content, so the
#             choice changes the counts. Both duplicate classes are now HARD STOPs naming
#             both files — canonical identity (X.docx vs "X (1).docx") via Cluster H at
#             enumeration, and same date+session with different Q-ranges at the filter stage.
#             Image survival is no longer a reason to prefer the larger file: PYQSort v1.12
#             CHECK 10 gates it at the point of production.
#         (6) 4-batches-per-chat arithmetic stated up front (S5-7). The binding constraint on
#             the upload lane is the platform's 20-files-per-chat limit, not the batch size:
#             at BATCH_SIZE_COUNTS = 5 that is exactly 4 batches / 20 papers per chat. Derived
#             from bc.upload_batch_plan, never restated as a literal.
#         (7) Step 2b banner (S3-2): the absence of images and OMML during the scan is BY
#             DESIGN and is NOT the defect class fixed in Steps 3/5. Added because a reader
#             arriving from the v2.29 image-integrity work would otherwise reasonably conclude
#             Step 2b was broken too and "fix" it. S3-2, EC-P24 and EC-P25 are UNCHANGED.
#         (8) New edge cases EC-P31..EC-P34. §11 and §12 updated.
#         NOT CHANGED: BATCH_SIZE_COUNTS (5), the S5-1a Task 1 confirmation gate, the S5-4a
#         zero-tolerance accuracy gate, Task 2.5, Task 3, the sorted-filename filter, and every
#         Phase 0a / 0b / 0c behaviour other than the S3-2 banner.
#         ROUTING: routes.json must route corpus_io.py to PYQCount. NOT OPTIONAL.
#
# v2.20 — 2026-07-23 — PHASE-B HEADING PARSER DRIFT CLOSED (line-by-line audit finding).
#   parse_taxonomy_level() and is_taxonomy_heading() each carried a comment demanding they
#   stay IDENTICAL to Step 5's, and EC-P14 named the exact failure mode and remedy. Both had
#   nevertheless drifted: Framework_MockTestAnalyse v2.16 (RIGID-4) expanded the heading
#   table from 3 patterns to 12+ (Section:/Part:/Area:, Unit/Module/Block, colon-style
#   topics, case-insensitive) and this file was never mirrored, and the two
#   is_taxonomy_heading copies used DIFFERENT question-exclusion regexes.
#   IMPACT: for any exam not using the Subject:/Topic N: convention, Step 5 read a heading as
#   level 1/2 while Step 4 fell through to level 3 and counted it as a SUBTOPIC — wrong
#   per-subtopic counts, caught (if at all) only by Step 6's BV-0A cross-check.
#   FIX: both now delegate to blueprint_core Cluster G. The engine form is Step 5's superset,
#   proven by test_cluster_g.py to classify every heading the old copy handled identically
#   while additionally levelling the forms it silently mis-filed. A comment asking two files
#   to stay in step is not a mechanism; one definition is.
#
# v2.19 — 2026-07-23 — ERA LOGIC UNIFIED INTO THE ENGINE + MARKER-MODE COVERAGE
#   (audit follow-up to v2.18; fixes defects introduced BY v2.18).
#   (1) ANTI-DRIFT. v2.18 transcribed the era-classification chain into S3-2a step 3b as
#       prose while blueprint_core carried its own implementation, and routes.json routed
#       no engine to PYQScan — two independent definitions of "current era" with nothing
#       keeping them in step. The v2.25 Step-5 changelog even CLAIMED they were shared;
#       they were not. Step 3b now CALLS bc.classify_paper_era / bc.exam_config_bounds /
#       bc.type_resolver_from_config, and routes.json routes blueprint_core.py to
#       PYQDraft/PYQScan/PYQApprove/PYQSort/PYQCount/PYQExtract. Same for the
#       OUT_OF_PATTERN literal, which now lives in the engine only.
#   (2) NEW ERA 'retyped' (EC-P9b). Era was defined by SIZE alone, so an exam that keeps its
#       question count but changes its question TYPES — all-MCQ becoming MCQ/MSQ/NAT — was
#       classified 'current' and blended into the mix and the axis-3 distribution. Across
#       ~200 exams that is at least as common as a count change, so size-only classification
#       was missing the majority case. Backward compatible: with no marking_scheme, or with
#       no detected types, no comparison runs and the v2.18 chain applies unchanged.
#   (3) MARKER-MODE ERA DETECTION (EC-P9c). marker_mode exams had NO era detection at all —
#       the Q-number chain cannot run without Q-ranges. Step 3b now compares observed module
#       names against exam_config.sections[].name and reports retired modules instead of
#       letting EC-S2 fuzzy matching silently absorb them into a surviving section.
#
# v2.18 — 2026-07-23 — PATTERN-ERA AWARENESS AT SCAN TIME (GAP-2026-07-23-001;
#   PYQ-side twin of Framework_PYQSort v1.9 and Framework_Blueprint v1.36).
#   ROOT CAUSE (shared by all three specs): exam_config describes the CURRENT exam
#   pattern, but a PYQ corpus routinely spans several patterns. Nothing in the pipeline
#   recorded, reported, or handled that. RULE 4 said "section from Q-number range in
#   exam_config" with no branch for a Q-number outside every range, and EC-P9 documented
#   only the SHORTER direction ("later sections may have 0 questions"). The LONGER
#   direction — a previous-era paper with MORE questions than the current pattern — was
#   undocumented corpus-wide, and it is the dangerous one: surplus Q-numbers match no
#   range at all, so they were assigned None and then failed every (section, topic,
#   subtopic) lookup downstream. A 100-question legacy paper scanned against a
#   60-question current config lost 40 questions silently.
#   (1) RULE 4 (§8) — new OUT-OF-RANGE branch. Q-numbers outside every configured range
#       take the OUT_OF_PATTERN sentinel (the same constant as Framework_PYQSort v1.9
#       S2-2) and are classified against the FULL taxonomy instead of one section's slice.
#       This is the ONE relaxation of the rule's "not content" half, and only because the
#       rule's premise fails: it presupposes a structural section EXISTS. Gated on the
#       sentinel, never on a failed match, so a question that has a section cannot reach
#       it. pattern_era='out_of_pattern' is recorded on the classification.
#   (2) EC-P9 — the missing mirror documented: papers LARGER than the current pattern.
#   (3) S3-3 step (c) — the out-of-range route made explicit at the classification site
#       rather than only in the rules section.
#   (4) S3-2a PRE-SCAN GATE — new step 3b computes each paper's pattern era
#       (current / larger / smaller / unverified) from exam_config and the observed
#       Q-numbers ALONE; new Pattern Era column; new step 5b notice printed ONLY when the
#       corpus spans more than one era. A single-era corpus — the common case across the
#       ~200 exams — sees no behavioural or output change whatsoever.
#   DESIGN INTENT: both eras are scanned and both feed the taxonomy. Older papers are
#   retained precisely because the variety of concepts, phrasings, difficulties and
#   formats they expose is what makes generated questions good, and a subtopic observed
#   across many eras is better characterised than one observed twice. The defect was
#   never that old papers were included — it was that the pipeline noticed the structural
#   mismatch and said nothing.
#   SCOPE BOUNDARY (stated so it is not mistaken for solved): question COUNTS are safe —
#   Framework_Blueprint §4-2 consumes r_avg as a PROPORTION against a sec_qs budget from
#   exam_config, so a different-size paper can neither inflate nor shrink allocation.
#   Subject/subtopic MIX and format mix remain era-blended; §3 recency weighting dampens
#   but does not remove this. Era-scoped frequency would require era-tagging through the
#   Step-5 manifest and the Frequency xlsx and is deliberately NOT attempted here.
#   The pre-scan notice reports the exposure so the operator holds that decision.
#
# v2.17 — 2026-07-23 — PYQAPPROVE OPERATOR-SAFE APPROVAL GATE (root-cause fix).
#   INCLUDES (Issue C + C-1):
#     C-1 CRITICAL — DELIMITER AMBIGUITY. Paths were '/'-joined strings, but
#         real subject names contain '/' (live example: IIT JAM Biotechnology's
#         "Microbial/Plant/Animal Biotech"). Every anchor check produced a FALSE
#         FAILURE on that exam. FIX: paths are LISTS OF COMPONENTS, compared as
#         tuples, never split or joined for comparison. Delimiter-free by design.
#     C   EMISSION BURDEN. S2-1/S2-3 had to emit 9 fields x N items by prose-
#         following (~1800 values for a 200-item syllabus). FIX: emit 4 fields
#         (path, text, to, why); DERIVE the other 5 (id, subject,
#         syllabus_group, enumerated, deviation) in syllabus_provenance.py.
#         A derived field cannot be emitted wrong.
#     CIRCULARITY GATE. group_topic_map must be DECLARED from syllabus
#         structure; a map derived from the mappings it checks makes anchoring
#         vacuous. Found by testing 11 real syllabi (all passed spuriously).
#     4-LEVEL COLLAPSE. Syllabi whose depth exceeds Subject>Topic>Subtopic
#         (NEET Chemistry: CHEMISTRY > PHYSICAL CHEMISTRY > SOLUTIONS > item)
#         MUST record the collapse as a declared deviation. Verified: NEET
#         correctly build-blocks until the collapse decision is recorded.
#     §7 CANONICALIZATION. A destination matching the taxonomy only after
#         normalization is snapped to the taxonomy's EXACT spelling, so
#         byte-identity holds downstream instead of failing at Step 5/6.
#   PROBLEM: S4-4 posed four ACADEMIC questions ("are subtopics faithful to the
#   syllabus?", "is anything MISSING/EXTRA?") to an operator who is non-technical
#   and non-academic by role definition. The gate was therefore unanswerable at
#   the point of use, yielding either a rubber-stamp (gate protects nothing) or a
#   stall (no escalation path). Approval theatre, not approval.
#
#   ROOT CAUSE (found during this fix, deeper than S4-4): S2-4 persisted the
#   DERIVED taxonomy but NEVER persisted the extracted syllabus items. At
#   PYQApprove time no machine-readable ground truth existed, so the four
#   questions COULD NOT be answered by machine — they had to be delegated to a
#   human. The gate was a symptom; the missing provenance record was the defect.
#
#   FIX (4 changes):
#     (1) S2-4 — taxonomy_draft.json now persists syllabus_subjects[] (verbatim
#         S2-1 subject names) and syllabus_items[] (id, subject, raw_text,
#         enumerated, source_ref, mapped_paths[]). This is the provenance record
#         that makes Tier 0 possible. Backward compatible: absent => legacy mode.
#     (2) NEW S4-0 — TAXONOMY RECONCILIATION ENGINE (reconcile_taxonomy.py).
#         Deterministic 3-tier resolution replacing the human quiz:
#           Tier 0  machine reconciliation  (C1..C6, no judgment)
#           Tier 1  codified auto-policy    (PATH_EXTRA by PYQ evidence)
#           Tier 2  evidence-bound adjudication, REPLAYED from approval_record
#     (3) S4-4 REWRITTEN — emits a VERDICT + receipt, not a questionnaire.
#         CLEAN / CLEAN_ADJUDICATED => auto-lock, operator only uploads files.
#         HELD => named finding routed for adjudication. Operator never performs
#         academic judgment in any branch.
#     (4) S4-3 / S10-1 / S10-2 — approve-mode closed set 2 -> 3 files
#         (+ [ExamCode]_approval_record.json, the audit + replay ledger).
#
#   TIER 1 POLICY (confirmed): out-of-syllabus but PYQ-backed subtopics are
#   AUTO-RETAINED. Rationale is the framework's own anti-data-loss rule (S2-3
#   MPPSC Botany evidence) plus S3-6, which already gates every scan-added
#   subtopic at MIN_PATTERN_SIZE >= 3 PYQs — so such subtopics are PYQ-evidenced
#   BY CONSTRUCTION before they ever reach PYQApprove.
#
#   DETERMINISM GUARANTEE: Tier 2 adjudication is constrained by six hard
#   invariants that an adjudicating verdict CANNOT override. Unsafe or
#   unevidenced verdicts are rewritten to the safe default rather than rejected,
#   so a bad adjudication degrades to data-preserving, never to data loss:
#     INV-1 NO_SUPPRESS_SYLLABUS      never remove a syllabus-enumerated item
#     INV-2 NO_DROP_PYQ_BACKED        never drop a path with >= 3 PYQs
#     INV-3 LOW_CONFIDENCE_SAFE_DEFAULT
#     INV-4 EVIDENCE_REQUIRED         destructive verdict needs a syllabus quote
#     INV-5 CONSERVATION              no classified question may be orphaned
#     INV-6 REPLAY_DETERMINISM        prior verdicts replayed, never re-decided
#   INV-6 is what makes the gate reproducible across sessions and model
#   instances — it closes the framework's known "spec-as-prose is
#   non-deterministic" failure class at the adjudication boundary.
#
#   Verified: 24/24 adversarial unit tests (test_reconcile.py) incl. attempts to
#   drop syllabus items, drop PYQ-backed paths, adjudicate with no evidence, and
#   adjudicate under silence; plus end-to-end IIT JAM BT simulation reproducing
#   the reported case (both scan-discovered subtopics auto-retained, 0
#   escalations, conservation pass, status CLEAN).
#
# v2.16 — 2026-07-20 — PYQ CORPUS DRIVE-ONLY STANDARDIZATION, STEP 2b/PYQScan (twin fix:
#   Framework_MockTestAnalyse.md Step 5/PYQExtract v2.24.8). Found during a project-level
#   audit: three pipeline steps that all handle the SAME document class (Row/Sorted PYQ
#   .docx corpus files) disagreed on whether Google Drive was required — Step 4 (PYQCount,
#   this file) always mandated Drive with no fallback; this step (Step 2b/PYQScan) allowed
#   an uploads-only fallback; Step 5 (PYQExtract) allowed the broadest fallback (project/
#   uploads). STANDARDIZED to Step 4's existing Drive-only rule (confirmed with
#   Radheshyam) — Row files must be in Google Drive for --scan mode now, same as
#   --counts mode always required. WHAT CHANGED:
#     Header, S1-1 trigger parsing, S1-2 mode validation, S1-2 file inventory — PYQ:
#       <<Drive link>> is now REQUIRED for --scan mode; absent → HARD STOP (was: silent
#       fallback to /mnt/user-data/uploads/).
#     collect_row_files() (§3 S3-2) — removed the 'uploads' source branch entirely;
#       now takes drive_folder_id as a required argument and raises SystemExit if
#       absent, instead of silently scanning uploads/.
#   --taxonomy mode (Exam Syllabus/Pattern docs) and --approve mode (scan_progress.json)
#   are UNAFFECTED — those are a different document class (small config/state files),
#   not the PYQ corpus, and remain project/uploads-eligible per existing architecture.
#   Does not touch taxonomy-building logic, batch processing, or gate/mandate checks.
#   Verified: validate_framework_md.py (0 issues, AST-clean).
#
# v2.15 — 2026-07-18 — LOCAL-COPY CORRUPTION REPAIR (B-PYAST false positive; zero content/
#   logic change). This project's local Files-section copy of this spec had silently DROPPED
#   2 markdown code-fence lines somewhere between §D6-3 (the "pass" / NOTE comment ending the
#   dimensional-split-detection block) and §D6-4/D6-5 (the split-governance-guards block) —
#   a closing ``` after the v2.13 NOTE comment, and an opening ```python before
#   reclassify_after_refinement(). Missing fences caused validate_framework_md.py to parse
#   two separate, independently-valid Python blocks as one contiguous block, producing a
#   false "invalid syntax (line 188 of block)" AST error at the boundary. Verified via direct
#   byte-for-byte diff against the canonical framework-specs GitHub repo (production branch,
#   commit 74d395f) that the CANONICAL source was never affected — this was local-copy
#   corruption only, likely introduced during an earlier Files-section upload/sync, not a
#   spec defect. Fix: restored both fence lines exactly as they exist upstream. Confirmed
#   post-fix: this file is now byte-identical to the canonical GitHub copy in its entirety
#   (diff clean, matching line count). No prose, code, gate, or rule content changed.
#
# v2.14 changes: FORMAT AUTHORITY RECONCILIATION (register D6-11). S3-3b reconcile_format()
#   makes the authoritative full-parse format (PYQSort Phase A) supersede the lightweight
#   scan's provisional OMML-obscured/figure-inferred tokens, so a mis-scanned math/figural
#   item no longer drives the wrong Format/CONCEPT_GROUP/class downstream. reconcile_stats()
#   flags a >20% correction rate for review. Verified by fmt_harness (16/16).
#
# v2.13 changes: SPLIT GOVERNANCE GUARDS (register D6-4/D6-5). Deterministic helpers that
#   enforce the previously prose-only split rules: split_children_valid() flags near-duplicate
#   split children (over-split) so they are merged back (high-precision: singular/plural, paren-
#   variants, exact dups; borderline pairs left to Q3/QV-13 to avoid false merges); merge_record()
#   captures distinct forms merged into one subtopic (under-split) so Step 7 scenario_key still
#   separates them. Verified by split_harness (14/14).
#
# v2.12 changes: NAME-QUALITY GATES (register D6-1/D6-2).
#   (1) NAME-SHAPE VALIDATION: HARD STOP on question-shaped subtopic/topic names
#       (ends with '?', >80 chars, or interrogative-initial) — stops a raw PYQ question
#       being captured as a subtopic and then allocated/generated (occurred in the SSC CGL
#       run). High-precision: 0 false positives on 31 real labels.
#   (2) canon_name(): NFC + dash/whitespace/case folding for COMPARING/COUNTING names, so
#       trivial drift never phantom-splits a subtopic (complements Task 2.5). Display keeps
#       the original name. Verified by name_harness (46/46).
# [ExamCode] project | Steps 2a/2b/2c + 4 (PYQDraft/PYQScan/PYQApprove/PYQCount) | Exam-agnostic
#
# PURPOSE:
#   Build the authoritative 3-level taxonomy (Subject > Topic > Subtopic) and
#   produce a single merged Analysis Word Document for any competitive exam.
#   This Analysis doc is a mandatory input to Step 6 (MockBlueprint). The taxonomy also serves
#   as the classification reference for PYQSort (Framework_PYQSort.md).
#
# PIPELINE POSITION:
#   Step 1  PYQ Prepare  → raw PYQ .docx to Row file
#   PYQAnalyse           → THIS SPEC (taxonomy + Analysis doc)
#   Step 3  PYQSort      → 1 Row file → 1 Sorted PYQ (uses approved Analysis doc as taxonomy)
#   Step 5  PYQExtract   → Sorted PYQ → section_rules.md + manifest + Frequency .xlsx
#   Step 6  MockBlueprint → Analysis doc + Frequency xlsx → blueprint.json
#   Steps 7–11           → Mock test creation pipeline
#
#   PYQAnalyse has 4 modes that run at different points in the pipeline:
#     --taxonomy + --scan + --approve  run BEFORE PYQSort (build & lock taxonomy)
#     --counts                         runs AFTER  PYQSort (fill PYQ counts)
#
# PREREQUISITE:
#   Step 1 (PYQ Prepare) must have already converted raw exam dumps into standardized
#   Row files (.docx with Q.1–Q.N, date labels [DD-Mon-YYYY <session_keyword> X] or
#   [DD-Mon-YYYY] when session is not applicable, no answers/explanations/metadata).
#   Session part in date labels is OPTIONAL — single-session exams omit it.
#   PYQAnalyse and PYQSort both expect Row file format.
#   If Row files don't exist: run Step 1 PYQ Prepare first.
#
# INPUTS (by mode):
#   --taxonomy : Exam Syllabus (ANY format: image/PDF/.docx/plain text)
#                Exam Pattern  (ANY format: image/PDF/.docx/.xlsx/plain text)
#                  PREFERRED: .xlsx with 3 standardized tabs (Overview/Sections/Range)
#                  See S2-2 for xlsx parser specification.
#   --scan     : Row files (.docx) — from Google Drive (required, v2.16)
#                scan_progress.json (for resume across sessions)
#   --approve  : scan_progress.json (completed scan)
#   --counts   : Sorted PYQ files from Google Drive (output of PYQSort)
#
# OUTPUTS (by mode — CLOSED SETS, see §10 S10-1 for full contract):
#   --taxonomy : [ExamCode]_taxonomy_draft.json + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --scan     : [ExamCode]_scan_progress.json + [ExamCode]_classifications.json
#                (2 files, nothing else — taxonomy lives INSIDE scan_progress.json)
#   --approve  : [ExamCode]_PYQ_Analysis.docx + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --counts   : [ExamCode]_PYQ_Analysis.docx (UPDATED with PYQ counts)
#                (1 file, nothing else — count_progress.json is internal)
#
#   DELIVERABLE SET IS CLOSED: each mode delivers EXACTLY the files listed
#   and NOTHING ELSE. See §10 S10-1 for DO-NOT-DELIVER lists per mode
#   and S10-2 for the pre-delivery checklist. Creating unauthorized files
#   is a spec violation (same class as anti-editorializing violations).
#
# TRIGGER FORMAT:
#   Step 2a: PYQDraft [ExamCode]          (ExamCode provided ONLY here, saved in exam_config.json)
#   Step 2b: PYQScan                      (reads ExamCode from exam_config.json)
#   Step 2b: PYQScan PYQ: <<Google Drive folder link>>  (required, v2.16 — Drive source for Row files)
#   Step 2c: PYQApprove                   (reads ExamCode from exam_config.json)
#   Step 4:  PYQCount PYQ: <<Google Drive folder link>>  (reads ExamCode from exam_config.json)
#
#   Trigger matching is case-insensitive.
#   ExamCode: alphanumeric + underscore only (e.g. SSC_CGL_TIER1, GATE_CS).
#   ExamCode is typed ONCE in Step 2a, then auto-read from exam_config.json in all later steps.
#
# PROJECT SETUP:
#   ALL modes run in [ExamCode] project (exam-specific).
#   After --approve: Analysis doc + exam_config.json are already in project.
#   After --counts: user downloads updated Analysis doc → input for Step 5 + Step 6.
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   All section names, topic names, subtopic names → derived from syllabus + PYQ.
#   Same spec runs for SSC CGL (4 sections), GATE CS (1 section), or any exam.
#
# VERSION HISTORY:
#   v2.11 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           PREREQUISITE section updated: date labels can be [DD-Mon-YYYY] without
#           session (single-session exams). Framework_PYQPrepare v1.1 makes session
#           optional in the trigger. PYQAnalyse date detection (\d{1,2} day pattern)
#           already handles both forms — this is a documentation-only fix.
#   v2.10 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S10-4: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. All 4 modes (--taxonomy, --scan,
#           --approve, --counts) now render the standardized visual footer after
#           every present_files call. Zero logic change.
#   v2.9 — 2026-07-06 — BATCH STOP LAW + DELIVERABLE SET CONTRACT (1 new section, 2 rewrites, 10 fixes).
#           ROOT CAUSE 1 — BATCH STOP LAW: SSC CGL Tier 2 PYQScan — Claude
#           auto-advanced from Batch 1 to Batch 2 in the same response without
#           waiting for user's "continue" trigger. 7 structural gaps identified
#           by comparing how MockCreate enforces the same rule (MANDATE 1) vs
#           how PYQAnalyse expressed it (item 7 in Anti-Editorializing Rule).
#
#           ROOT CAUSE 2 — DELIVERABLE SET: SSC CGL Tier 2 PYQScan — Claude
#           delivered an unauthorized taxonomy_draft_v2.json alongside the
#           spec-defined scan outputs. The spec had no CLOSED DELIVERABLE SET
#           contract — outputs were listed in the header but nothing said
#           "these files and NOTHING ELSE." 4 structural gaps identified by
#           comparing how MockCreate enforces delivery (S13-6 closed set,
#           S13-7 pre-delivery checklist, R-DELIVER rule) vs PYQAnalyse
#           (one-liner in header, no DO-NOT-DELIVER, no pre-delivery gate).
#
#           BATCH STOP LAW CHANGES:
#           (1) NEW S3-4a — BATCH STOP LAW: dedicated mandate-level section
#               with failure history, continue trigger contract, small-corpus
#               clarification, final-batch exception, and forbidden behaviors.
#               Same architectural weight as MockCreate's MANDATE 1 / B-1..B-8.
#           (2) S3-4 convergence gate docstring: "CONTINUE scanning without
#               discussion" rewritten to explicitly say "STOP THE RESPONSE and
#               wait for user's continue trigger — without discussion means
#               do not editorialize, NOT auto-advance." This single line was
#               the primary cause of the failure — Claude read it as an
#               instruction to auto-advance silently.
#           (3) S3-5 run_scan() batch gate: expanded from 2-line comment to
#               6-line block with "Write nothing more. Generate nothing more."
#               and cross-reference to S3-4a + MockCreate MANDATE 1 STEP 6.
#           (4) S3-4 Anti-Editorializing items 7-8: added explicit note that
#               the response ENDS after printing items 1-7 (S3-4a reference).
#           (5) §12 DoD: batch gate checklist item expanded with S3-4a reference
#               and explicit "including small corpora" qualifier.
#           (6) S3-4a STEP 3 + S3-5 run_scan(): added present_files call for
#               scan_progress.json + classifications.json after each non-final
#               batch. Previously files were saved to disk silently with no
#               download link — user could not grab progress for session resume.
#               Matches MockTestAnalyse S8-3 pattern (summary → present_files
#               → continue prompt). Continue prompt is always the LAST line.
#
#           CROSS-FRAMEWORK NOTE: Phase B counting (S5-7/S5-8) uses a Python
#           script execution model where all batches run in one script call —
#           the Batch Stop Law does NOT apply to script-executed batches (the
#           script handles its own save-after-each-batch logic). The law applies
#           to interactive chat-based batch processing only (Phase 0b scan).
#           MockTestAnalyse (PYQExtract) has its own batch gate via Options A/B
#           pattern — verify that framework separately.
#
#           DELIVERABLE SET CONTRACT CHANGES:
#           (7) §10 REWRITTEN — DELIVERABLE SET CONTRACT: closed deliverable
#               sets for all 4 modes (--taxonomy, --scan, --approve, --counts).
#               Each mode defines EXACTLY which files to deliver and an explicit
#               DO-NOT-DELIVER list of internal/intermediate files. Pre-delivery
#               checklist (S10-2) blocks present_files until the call contains
#               EXACTLY the expected files and nothing else.
#               Mirrors MockCreate's S13-6 (closed set), S13-7 (pre-delivery
#               checklist), and R-DELIVER (named rule).
#               LIVE FAILURE: SSC CGL Tier 2 --scan delivered an unauthorized
#               taxonomy_draft_v2.json because no "NOTHING ELSE" qualifier
#               existed and no DO-NOT-DELIVER list blocked extra files.
#           (8) Header OUTPUTS section: updated with "(N files, nothing else)"
#               qualifiers and cross-reference to §10. classifications.json
#               now explicitly listed (was changelog-only since v1.7 C2).
#           (9) S2-6, S3-5, S3-7, S4-3, S5-5, S5-8: delivery instructions
#               updated to reference S10-1 closed set and S10-2 pre-delivery
#               checklist.
#           (10) §12 DoD: all 4 phases updated with closed-set verification
#               items and pre-delivery checklist pass requirement.
#
#   v2.8 — 2026-07-06 — SYLLABUS-ENUMERATED ITEMS MUST BECOME SUBTOPICS.
#           ROOT CAUSE: Comparative analysis of framework-generated (68 subtopics) vs
#           PYQ-grounded (209 subtopics) Analysis docs for SSC CGL Tier 1 revealed a
#           3× subtopic gap. The merge-over-split bias (v2.4) was too aggressive —
#           Claude interpreted it as "if the Topic name covers it, don't create
#           subtopics", producing 1:1 Topic=Subtopic mappings (e.g., "Geometry" → 1
#           subtopic "Geometry" despite the syllabus explicitly listing Triangles,
#           Circles, Polygons as separate items). This is data loss, not conservative
#           merging.
#
#           CHANGE 1 — S2-3 CORE PRINCIPLE: Added CRITICAL SCOPE OF MERGE BIAS
#             clarification. The merge bias applies ONLY to AI-invented splits, NOT
#             to items the syllabus itself explicitly enumerates. Suppressing
#             syllabus-enumerated items is data loss. Added SSC CGL Tier 1 counter-
#             evidence alongside the MPPSC Botany evidence.
#           CHANGE 2 — S2-3 Step 1 GROUPING RULE: Added GROUPED ITEMS ARE SUBTOPICS
#             mandatory rule. When multiple syllabus items are grouped into one Topic,
#             every grouped item MUST become a named subtopic. Includes 3 failure
#             examples (Geometry, Trigonometry, Polity) with correct vs wrong output.
#           CHANGE 3 — S2-3 Step 1 GROUPING RULE: Added 1:1 TOPIC=SUBTOPIC DETECTOR
#             self-check. After subtopic derivation, any Topic with exactly 1 subtopic
#             of the same name is flagged for re-derivation (unless the syllabus
#             genuinely lists it as a single atomic concept).
#           CHANGE 4 — §12 DoD Phase 0a: Added 1:1 Topic=Subtopic check item.
#
#   v2.7 — 2026-07-06 — CATCH-ALL / RESIDUAL TOPIC PROHIBITION.
#           ROOT CAUSE: Live execution on SSC CGL Tier 2 produced "Topic 17: Other
#           Sub-topics" containing Blood Relations, Seating Arrangement, Syllogism,
#           Dice and Cubes, Ranking and Ordering, Logical Sequence — all distinct
#           question types that should be separate Topics. Claude ran out of patience
#           while processing a long syllabus and dumped remaining items into a residual
#           bin, violating the Topic Integrity Test.
#
#           CHANGE 1 — S2-3 Step 1: Added CATCH-ALL / RESIDUAL TOPIC PROHIBITION
#             rule with explicit banned patterns (case-insensitive substring match):
#             "other", "miscellaneous", "misc", "remaining", "additional",
#             "general topics", "catch-all", "residual". Includes failure example
#             from SSC CGL Tier 2 and mandatory self-check after Topic derivation.
#           CHANGE 2 — S2-3 EXCLUSION RULES: Added matching prohibition at Subtopic
#             level — same banned patterns apply to Subtopic names.
#           CHANGE 3 — S2-3 QUALITY GATE: Added CATCH-ALL NAME CHECK as a mandatory
#             gate that runs after all other quality gates. HARD STOP if any
#             Topic or Subtopic name matches a banned pattern.
#           CHANGE 4 — §12 DoD Phase 0a: Added catch-all name check item.
#
#   v2.6 — 2026-07-06 — MERGED ANALYSIS DOC (single file replaces per-subject files).
#           ROOT CAUSE: Phase 0c produced one .docx per subject (e.g. 4 files for SSC
#           CGL Tier 1). This created unnecessary file management overhead: N+1 files
#           to upload, track, and version; risk of missing one subject's doc during
#           upload; partial-update risk during Phase B; and the "missing ONE subject"
#           fallback (S10-6 in downstream Blueprint) that was fragile. Every downstream
#           parser (PYQSort, Step 5, Step 6) already identifies sections by CONTENT
#           (the "Subject: [Name]" header inside the doc), not by filename — so the
#           per-file split had no technical justification.
#
#           CHANGE 1 — S4-1: Output is now a single [ExamCode]_PYQ_Analysis.docx
#             containing ALL subjects, separated by page breaks. Internal structure
#             per subject is unchanged (header block, master summary table, per-topic
#             subtopic tables, footer). File management drops from N+1 to 2 files
#             (1 Analysis doc + 1 exam_config.json).
#           CHANGE 2 — S4-2: generate_analysis_doc() → generate_merged_analysis_doc()
#             accepts full taxonomy dict, iterates all subjects with page breaks.
#           CHANGE 3 — S4-4: Approval gate message updated for single-file output.
#             Lists sections within the doc instead of separate filenames.
#           CHANGE 4 — S5-4b/S5-5/S5-8: Phase B references updated from plural
#             "Analysis docs" to singular "Analysis doc" — same parsing logic, single
#             file load/save instead of per-file iteration.
#           CHANGE 5 — S10-3/S10-4: Delivery sections updated for single file.
#           CHANGE 6 — §7 Name Consistency: "Analysis docs" → "Analysis doc".
#           CHANGE 7 — §12 DoD Phase 0c: "One Analysis .docx per subject" →
#             "Single merged Analysis .docx with all subjects".
#           CHANGE 8 — S1-2 --counts mode, EC-P1, EC-P29: plural → singular.
#
#           DOWNSTREAM CONSUMERS — CORRECTED 2026-07-25 (GAP-2026-07-25-002).
#           The original v2.6 entry claimed: "All downstream consumers (PYQSort,
#           Step 5, Step 6) require NO spec changes — they already parse by content
#           pattern, not file boundary. The downstream specs use glob patterns or
#           direct file load; both work with a single file. Cross-step contract
#           unchanged." Every clause of that was wrong, and it stood for 19 days
#           and 7 PYQSort releases.
#             "parse by content pattern, not file boundary" conflated two things.
#           PYQSort parsed taxonomy LEVELS by content pattern — true, and presumably
#           what was checked — but it DISCOVERED the file by filename glob and
#           DELIMITED SUBJECTS BY FILE BOUNDARY, which is exactly what this change
#           removed. The analysis inspected the parser's inner loop, never its outer.
#             "both work with a single file" reasoned only about CARDINALITY. v2.6
#           changed two independent axes: cardinality (N -> 1) AND the filename. A
#           glob does work with a single file; it does not work with a RENAMED file.
#             "Cross-step contract unchanged" — a deliverable's filename IS the
#           cross-step contract. It changed.
#           ACTUAL IMPACT, measured 2026-07-25 against the first exam's live doc:
#             PYQSort  BROKEN ON BOTH AXES. Its glob matched zero files (loud), and
#                      its parser flattened 6 subjects into 1 (silent). Fixed v1.14.
#             Step 5   BROKEN, but not by this change — both of its Analysis-doc
#                      readers returned ZERO subtopics from any real doc and always
#                      had. Fixed in MockTestAnalyse v2.30.
#             Step 6   read the doc as prose: format-tolerant but non-deterministic.
#                      Fixed in Blueprint v1.39.
#           RULE: a deliverable RENAME, or a CARDINALITY change, is a cross-step
#           contract change. Every consumer's discovery pattern must be re-tested
#           against the new literal name AND every consumer's parser re-tested
#           against the new file SHAPE. A changelog assertion of downstream
#           compatibility is not evidence. Enforced by Check AF.
#
#   v2.5 — 2026-07-06 — STANDARDIZED EXAM PATTERN XLSX + EXAM_CONFIG SCHEMA OVERHAUL.
#           ROOT CAUSE: Exam pattern was read via AI interpretation of image/PDF/docx —
#           ambiguous, non-deterministic, and unable to capture per-range marking schemes
#           (e.g., CSIR NET Part C: 4 marks/Q vs Part A/B: 2 marks/Q), attempt limits
#           (e.g., CSIR NET: attempt 15/20 in Part A), or academic level. Validated
#           against 7 exam patterns: SSC CGL T1/T2, MPSC Botany, CSIR NET Life Science,
#           CSIR NET Mathematical Science, GATE Biotechnology, IIT JAM Chemistry.
#
#           CHANGE 1 — S1-2 + S2-2: XLSX AS PREFERRED INPUT FORMAT:
#             Exam pattern now accepted as .xlsx with 3 standardized tabs:
#               Tab 1 "Overview": key-value pairs (Total Questions, Medium, Question Type,
#                 Total Marks, Duration, Level)
#               Tab 2 "Sections": table (Section, Total Question, Question Starts,
#                 Question Ends, Max Attempt)
#               Tab 3 "Range": table (Question Range, Question Type, Correct Marks,
#                 Negative Marks)
#             Deterministic parser replaces AI interpretation. Legacy image/PDF/docx
#             path preserved as backward-compatible fallback.
#
#           CHANGE 2 — S2-2: 10 STRUCTURAL VALIDATIONS ON XLSX:
#             V1: Σ(Total Question) == Total Questions (Overview)
#             V2: Q_Ends − Q_Starts + 1 == Total Question (per section)
#             V3: Section Q-ranges contiguous and non-overlapping
#             V4: Range tab tiles Q.1 through Total Questions completely
#             V5: All Negative Marks ≤ 0
#             V6: Σ(Max Attempt × correct_marks) == Total Marks
#             V7: 0 < Max Attempt ≤ Total Question (per section)
#             V8: Overview Question Type set == Range tab distinct types
#             V9: All Correct Marks > 0
#             V10: Total Questions > 0, Duration > 0
#             Any failure → HARD STOP with specific error.
#
#           CHANGE 3 — S2-2: SECTION ≠ SUBJECT CLARIFICATION:
#             Section names from Sections tab are OTS (Online Test Series) display labels
#             only. They do NOT define Subject names for the taxonomy. The syllabus
#             (provided separately) defines Subjects, Topics, and Subtopics. A single
#             Subject can span multiple sections (e.g., CSIR NET: "Cell Biology" questions
#             appear in both Part B and Part C). The framework must never conflate
#             Section with Subject.
#
#           CHANGE 4 — S2-5: EXAM_CONFIG.JSON SCHEMA OVERHAUL:
#             Removed: marks_per_question (single int), negative_marking (single float).
#             Added: medium (str), question_types (list), level (str),
#               marking_scheme[] (per-range: q_range, question_type, correct_marks,
#               negative_marks), max_attempt (per section).
#             Per-range marking replaces global scalars — handles CSIR NET (2m vs 4m),
#             GATE (1m vs 2m, MCQ vs MSQ vs NAT per range), IIT JAM (MCQ/MSQ/NAT
#             sections with mixed marks). Float marks supported (CSIR NET Math: 4.75).
#
#           CHANGE 5 — S2-6 DELIVERY MESSAGE: includes new fields.
#           CHANGE 6 — §12 DoD: updated for xlsx validation + new schema fields.
#
#   v2.4 — 2026-07-05 — TAXONOMY DEPTH ARCHITECTURE OVERHAUL (S2-3 rewrite).
#           ROOT CAUSE: v1.5's "when in doubt, SPLIT" + mandatory 6 pattern dimensions
#           produced 336 subtopics for MPPSC Botany (81 syllabus entries → 4.1× inflation).
#           PYQ classification then failed on 38% of questions (93/150 mapped). Root cause
#           traced via comparative analysis of 13 exam syllabi: SSC CGL T1/T2, CAT, MPPSC
#           Botany, CSIR NET Life Sci, GATE CS, GATE Biotech, IIT JAM Physics, UGC NET
#           History, CUET PG Math, CUET UG Political Sci, NEET, CTET Paper 1.
#
#           CORE PRINCIPLE — UNIQUE DOMAIN PROPERTY:
#             Every subtopic must uniquely claim a concept set that no other subtopic also
#             claims. Given any PYQ question, exactly ONE subtopic must be the unambiguous
#             best match. Over-splitting violates this by creating near-duplicate bins that
#             confuse the classifier. Over-merging preserves it (loses granularity but
#             classifies 100% of questions). Default bias: MERGE over SPLIT.
#
#           CHANGE 1 — S2-3 COMPLETE REWRITE:
#             Replaced "6 mandatory pattern dimensions applied to every Topic" with a
#             3-question per-entry decision tree (Q1: explicit identifier? Q2: internal
#             sub-structure? Q3: Unique Domain Check). The 6 dimensions are retained as
#             an OPTIONAL tool for undivided-block entries only, not a mandatory universal
#             procedure. Subtopic derivation default reversed from "SPLIT" to "follow
#             syllabus structure faithfully."
#           CHANGE 2 — EXCLUSION RULES:
#             Vocabulary lists, glossary terms, named reactions, individual organisms,
#             historical terms, and enumerated scope items within colon-descriptors are
#             explicitly excluded from becoming subtopics.
#           CHANGE 3 — SANITY CHECKS:
#             Added ratio guardrail (flag at 2.0×, hard-stop at 3.0×), near-duplicate
#             detection (>75% name similarity), keyword overlap check (<30%), and
#             total-coverage verification (every syllabus concept → exactly 1 subtopic).
#           CHANGE 4 — QUALITY GATE REWRITE:
#             Replaced fixed benchmark (150–250 subtopics) with ratio-based guardrail
#             that scales to any exam size.
#           CHANGE 5 — §3-6 REFINEMENT PASS DEFAULT BIAS:
#             Changed from "split broad subtopics" to "merge confused subtopics first,
#             split only with ≥15 Qs evidence + Q3 Unique Domain Check pass."
#           CHANGE 6 — §11 and §12 UPDATED:
#             Exam-agnostic guarantee and DoD updated to reflect new taxonomy rules.
#
#           Validated against 13 exams: all produce ratio ≤ 2.6×. The MPPSC Botany
#           disaster (4.1×) would be prevented (ratio = 1.0× under new rules).
#   v2.3 — 2026-07-05 — PHASE 0b CONSISTENCY FIXES (3 issues).
#           (1) MEDIUM — S3-2 vs S3-7 CONTRADICTION: S3-2 said "no re-listing
#               on resume" but S3-7 (v2.2) said "RE-LIST". FIXED: S3-2 cached
#               inventory section now defers to S3-7 for resume behaviour.
#               First-session caching unchanged; resume re-lists per S3-7.
#           (2) LOW-MEDIUM — ANTI-EDITORIALIZING RULE UPDATED (S3-4): the
#               "NOTHING ELSE" allowed list now explicitly includes v2.2's
#               per-section Q distribution and classification quality output.
#               Without this, Claude could interpret v2.2 additions as violating
#               the anti-editorializing rule.
#           (3) LOW — total_available META UPDATE (S3-5): run_scan now writes
#               total_available to progress['_meta']['total_available'] before
#               first batch. Without this, saved scan_progress.json permanently
#               showed total_available=0 (the init default), breaking convergence
#               gates on resume if they read from _meta instead of parameter.
#   v2.2 — 2026-07-05 — PHASE 0b DEEP-AUDIT (4 gap fixes).
#           (1) HIGH — POST-CONVERGENCE SUMMARY (S3-5 updated): before printing
#               "Run: PYQApprove", display a comprehensive summary: original
#               taxonomy size vs final (after scan + refinement), net discovery
#               (+N new, +M from splits, -K removed), classification quality
#               (normal vs OMML-obscured vs figure-inferred percentages),
#               per-section snapshot (section → topics → subtopics), and papers
#               scanned per year. User needs full visibility before locking.
#           (2) MEDIUM — CLASSIFICATION QUALITY TRACKING (S3-5 batch-end updated):
#               after each batch, show per-section Q-count AND quality breakdown
#               (normal / OMML-obscured / figure-inferred counts). Surfaces
#               degraded classification rates early — if 40%+ are OMML-obscured,
#               the scan might miss patterns.
#           (3) LOW-MEDIUM — BATCH-END PER-SECTION Q-COUNT (S3-5 batch-end
#               updated): show per-section classified Q distribution after each
#               batch. Catches section detection failures (wrong marker_mode or
#               Q-range config) within the first batch, not after 60+ papers.
#           (4) LOW-MEDIUM — RESUME DRIVE RE-VERIFICATION (S3-7 updated): resume
#               sessions now re-list Drive files and re-run S3-2a pre-scan gate
#               instead of relying on cached inventory. Catches files added or
#               removed between sessions. Aligned with Phase B's S5-7 pattern.
#           §12 Phase 0b DoD updated: 3 new items.
#   v2.1 — 2026-07-05 — PRE-SCAN CONFIRMATION GATE (1 addition).
#           (1) NEW S3-2a — PRE-SCAN CONFIRMATION GATE: after collecting and
#               ordering all Row files (S3-2) but before any batch scanning
#               (S3-3/S3-5), display a year-wise paper inventory table with
#               per-paper Q counts (verified by parsing or from filename
#               pattern). Wait for explicit user confirmation before proceeding.
#               Proves Claude can see every file and every question. Matches
#               the Step 4 (PYQCount) Task 1 pattern (S5-1a) for consistency.
#               §12 Phase 0b DoD updated with 2 new items.
#   v2.0 — 2026-07-05 — PHASE B FINAL DEEP-AUDIT (7 fixes).
#           (1) HIGH — CHILD POINTER RESET (S5-2): count_sorted_file() now
#               resets cur_top + cur_sub when a new Section heading is found,
#               and resets cur_sub when a new Topic heading is found. Matches
#               Step 5 E-1 pseudocode (current_path[:level-1] + [content]).
#               Without this, a question after a Topic heading but before its
#               first Subtopic would silently inherit the wrong subtopic from
#               the previous topic — invisible to all Task gates.
#           (2) HIGH — TASK 1 Q-COUNTING METHOD (S5-1a): now explicitly
#               specifies: use python-docx paragraph iteration with the SAME
#               Q-pattern (r'^Q\.?\s*\d+') as count_sorted_file(). Also
#               documents the PYQSort renumber_stem dependency (sorted files
#               always output Q.<N> format). Also specifies per-file Q-count
#               storage for Task 2 diagnostic.
#           (3) BUG — TASK 2 FLOW REFERENCE (S5-4a): "Proceed to S5-5" fixed
#               to "Proceed to S5-4b (Task 2.5)." Was skipping the taxonomy
#               name cross-check in the documented flow.
#           (4) HIGH — TASK 2.5 EXTRACTION METHOD (S5-4b): now specifies exact
#               rules for extracting (section, topic, subtopic) triples from
#               Analysis doc tables. Section name from doc header (strip
#               "[ExamCode] — " prefix). Topic name from master table cells
#               (strip "Topic N: " prefix via parse_taxonomy_level). Subtopic
#               name from per-topic table cells (raw text .strip()). Ensures
#               extracted names match parse_taxonomy_level() output.
#           (5) MEDIUM — TASK 2 PER-FILE DIAGNOSTIC (S5-4, S5-4a): batch
#               counting now tracks per_file_attributed[filename] = sum of
#               attributed counts. When Task 2 fails, compares against Task 1
#               per-file Q-counts to identify exactly which files have
#               discrepancies and by how many.
#           (6) MEDIUM — PHASE B EXECUTION MODEL (new S5-8): specifies Python
#               script-based execution via count_pipeline.py. Script processes
#               files in batches, writes results to JSON, runs all gates.
#               3-tool-call model: create_file → bash_tool → present_files.
#           (7) LOW — DEDUP REGEX MULTI-DATE FIX (S5-1): multi-date filenames
#               (containing "_to_") are now excluded from dedup — they represent
#               unique combined papers by definition.
#   v1.9 — 2026-07-05 — PHASE B DEEP-AUDIT (6 gap fixes).
#           (1) CRITICAL — TAXONOMY NAME CROSS-CHECK (new S5-4b, TASK 2.5):
#               after Task 2 passes, cross-check every counted (section, topic,
#               subtopic) triple against the Analysis doc taxonomy. Flag phantom
#               triples (counted but not in doc) and orphan subtopics (in doc but
#               not counted). Prevents silent count loss from name mismatches
#               (trailing spaces, dash variants, case differences). HARD STOP
#               if any phantom triples found.
#           (2) HIGH — ORPHAN QUESTION TRACKING (S5-2 updated): count_sorted_file()
#               now tracks orphan questions (Q found before any Subject/Subtopic
#               heading) separately. Returns orphan list with file, Q number, and
#               reason. Task 2 failure message includes orphan diagnostic.
#           (3) MEDIUM — SORTED FILE FILTERING (S5-1 updated): Drive listing now
#               filters for files matching sorted filename pattern (*_Sorted_*.docx).
#               Non-sorted .docx files (Row files, other docs) are skipped with
#               a logged warning. Prevents double-counting.
#           (4) MEDIUM — DUPLICATE SORTED FILE DETECTION (S5-1 updated): same-date
#               same-session dedup applied to sorted files. If two sorted files
#               share the same date+session, keep the larger file, skip the
#               smaller. Log the skip. Prevents inflated counts.
#           (5) MEDIUM — PHASE B SESSION MANAGEMENT (new S5-7): explicit session
#               protocol for large corpora. Resume via re-trigger with same Drive
#               link. count_progress.json tracks processed files for skip-on-resume.
#               Task 1 re-runs on resume (re-confirms full inventory).
#           (6) LOW-MEDIUM — ZERO-COUNT SUBTOPICS (S5-5 updated): explicit rule
#               that 0 is a valid count written as "0". No subtopic may remain
#               "—" after Phase B. Subtopics with 0 PYQs get "0" not "—".
#           New edge cases: EC-P27 (phantom triple), EC-P28 (orphan Q in sorted
#           file), EC-P29 (non-sorted file in Drive folder), EC-P30 (duplicate
#           sorted file).
#           §12 Phase B DoD updated: 6 new items.
#   v1.8 — 2026-07-05 — PHASE B QUALITY GATES + BATCH SIZE (4 tasks, 5 changes).
#           (1) TASK 1 — PRE-COUNT CONFIRMATION GATE (new S5-1a): after reading
#               all sorted PYQ files from Drive, display year-wise paper inventory
#               with per-paper Q counts before any subtopic counting begins. Wait
#               for explicit user confirmation. Proves all files and all questions
#               are visible.
#           (2) TASK 2 — POST-COUNT ACCURACY GATE (new S5-4a): after all batch
#               counting is complete, display full Subject > Topic > Subtopic
#               breakdown with counts. Grand total must exactly equal the confirmed
#               total from Task 1. If mismatch (even 1 Q) → re-scan and fix before
#               proceeding. Zero tolerance.
#           (3) TASK 3 — DOC-WRITING ACCURACY GUARANTEE (S5-5 expanded): every
#               number inserted into Analysis docs must be arithmetically verified
#               at 4 levels: subtopic cells, topic TOTAL rows, master summary table,
#               header line. Cross-check: header == GRAND TOTAL == sum(topic totals)
#               == sum(subtopic counts). Any mismatch → fix before delivering.
#           (4) TASK 4 — BATCH SIZE REDUCED: BATCH_SIZE_COUNTS changed from 15 → 5.
#               S5-1 prose updated from "batch 10-15 files" → "batch up to 5 files".
#               §11 batch model updated.
#           (5) §12 Phase B DoD updated: 4 new Task gates added.
#   v1.7 — 2026-07-04 — RUNTIME GAP FIXES (32 issues from live execution).
#           Source: PYQAnalyse_Gap_Analysis_v1.md — live execution against
#           SSC CGL Tier 1 (200 papers, 7 years) exposed 32 gaps in 9 categories.
#           3 CRITICAL, 7 HIGH, 12 MEDIUM, 10 LOW — all fixed.
#
#           CATEGORY A — CONVERGENCE ENFORCEMENT (6 fixes):
#           (A1) CRITICAL: Anti-editorializing rule for JSON — Claude added
#                convergence_recommendation, scan_analysis fields to progress JSON.
#                FIX: BANNED JSON FIELDS list + schema-only enforcement.
#           (A2) CRITICAL: Anti-editorializing rule for chat — Claude argued
#                "taxonomy is functionally stable" alongside FAIL gate statuses.
#                FIX: Mandatory batch-end message template + BANNED PHRASES list.
#           (A3) MEDIUM: Gate 3 counter cited before Gate 2 met. FIX: counter is
#                informational noise before Gate 2 — documented.
#           (A4) HIGH: Strongest language only in code comments. FIX: prose-level
#                MANDATE block added before S3-4 code block.
#           (A5) MEDIUM: No papers-per-session expectation. FIX: 4-5 batches/session
#                target added to new S3-7 session management.
#           (A6) LOW: offer_early_exit name primes exit-thinking. FIX: renamed to
#                report_gate_status.
#
#           CATEGORY B — BATCH PROCESSING (4 fixes):
#           (B1) HIGH: Partial batches (1-2 papers) counted as complete. FIX:
#                BATCH INTEGRITY RULE — partial batch does not increment/reset counter.
#           (B2) MEDIUM: No explicit increment/reset code. FIX: explicit code with
#                "2 empty + 1 discovery = RESET" annotation.
#           (B3) MEDIUM: No response budget guidance. FIX: response budget section
#                with fallback to 2-paper batches.
#           (B4) HIGH: File reading method unspecified — Drive read_file_content
#                strips OMML/images. FIX: Drive reading method spec with OMML/figural
#                fallback classification rules.
#
#           CATEGORY C — CLASSIFICATION QUALITY (5 fixes):
#           (C1) CRITICAL: Per-question classifications not stored — only paper
#                summaries. FIX: per-Q storage mandate + separate classifications
#                file for large corpora.
#           (C2) HIGH: scan_progress.json too large (6000+ records). FIX: split
#                classifications into [ExamCode]_classifications.json.
#           (C3) MEDIUM: No new-discovery validation protocol. FIX: 3-question
#                validation gate before adding new subtopic.
#           (C4) MEDIUM: Figural questions classified blind during scan. FIX:
#                text-clue inference rules + EC-P24.
#           (C5) LOW: No per-section Q-count validation. FIX: post-paper validation
#                with informational warnings.
#
#           CATEGORY D — TAXONOMY & SCHEMA (3 fixes):
#           (D1) MEDIUM: Taxonomy authority chain unclear. FIX: explicit chain
#                documented (taxonomy_draft → scan_progress → PYQApprove).
#           (D2) HIGH: Full taxonomy not stored — only deltas. FIX: scan_progress
#                ['taxonomy'] must be COMPLETE (original + discoveries).
#           (D3) LOW: No schema version enforcement. FIX: version check in
#                load_scan_progress with error message.
#
#           CATEGORY E — REFINEMENT PASS (4 fixes):
#           (E1) HIGH: Refinement data impractical at scale. FIX: per-subtopic
#                sequential execution model with 50-Q sampling.
#           (E2) MEDIUM: Post-refinement gate re-check ambiguous. FIX: EC-P19
#                updated — Gate 2 not re-checked, only Gate 3.
#           (E3) MEDIUM: check_dimensional_splits unimplemented. FIX: structured
#                Counter-based algorithm with concrete example.
#           (E4) LOW: No refinement output verification. FIX: orphan check.
#
#           CATEGORY F — SESSION MANAGEMENT (3 fixes):
#           (F1) HIGH: No session management for large corpora. FIX: new S3-7
#                session management section with protocol and formula.
#           (F2) LOW: Drive listing not cached. FIX: drive_file_inventory in
#                scan_progress.json.
#           (F3) LOW: No Drive rate limit handling. FIX: retry-once + save guidance.
#
#           CATEGORY G — PAPER SELECTION (2 fixes):
#           (G1) MEDIUM: Cherry-picking small files. FIX: date-asc/shift-asc
#                ordering within each year — no reordering by size.
#           (G2) LOW: Newest-year-first bias undocumented. FIX: design note added.
#
#           CATEGORY H — CROSS-STEP CONTRACT (2 fixes):
#           (H1) MEDIUM: PYQApprove required fields unspecified. FIX: explicit
#                field list added to S4-1.
#           (H2) LOW: taxonomy_draft → scan_progress copy not explicit. FIX:
#                source_taxonomy tracking in init + authority chain docs.
#
#           CATEGORY I — MISSING EDGE CASES (3 fixes):
#           (I1-I3) LOW: EC-P21 (mixed file types), EC-P22 (duplicate filenames),
#                EC-P23 (Drive folder structure variants).
#
#           Additional edge cases from other categories:
#           EC-P24 (figural scan misclassification), EC-P25 (OMML-obscured scan),
#           EC-P26 (partial batch on context limit).
#
#           Structural changes:
#           - S3-7 is now Session Management (new). Old S3-7 → S3-8.
#           - report_gate_status replaces report_gate_status.
#           - §11 updated: 26 edge cases.
#           - §12 DoD updated for session management and classification storage.
#   v1.6 — 2026-07-04 — CROSS-STEP SYNC + EXAM-AGNOSTIC FIX (6 bugs).
#           (1) MISSING FOOTER: no "END OF" marker — every other framework file has
#               one. FIXED: added.
#           (2) EXAM-SPECIFIC JSON EXAMPLE (S2-5): exam_config schema used hardcoded
#               SSC CGL Tier 1 values (exam_code, exam_name, 4 SSC section names with
#               specific q_ranges). FIXED: replaced with [ExamCode]/[Section N Name]
#               placeholders matching the exam-agnostic pattern of other framework files.
#           (3) 'TestSeriesRow' STALE NAME (3 refs in header): Step 1 PYQ Prepare was
#               still referenced by its old name. v1.2 fixed TestSeriesSort→PYQSort but
#               missed TestSeriesRow. FIXED: "Step 1 PYQ Prepare" / "Step 1 (PYQ Prepare)".
#           (4) PIPELINE POSITION MISSING STEP NUMBERS: PYQExtract and MockBlueprint
#               listed without canonical step numbers. FIXED: "Step 5 PYQExtract",
#               "Step 6 MockBlueprint", "Step 3 PYQSort".
#           (5) exam_config SCHEMA MISSING 3 FIELDS: session_keyword, page_size,
#               options_count — all consumed by PYQSort (v1.3/v1.4) but not defined in
#               the schema that creates exam_config.json. PYQSort used silent defaults
#               (Shift, A4, 4) which worked but weren't documented as the contract.
#               FIXED: all 3 added to S2-5 schema with field definitions + defaults.
#           (6) PREREQUISITE section hardcoded "Shift" in date label format description.
#               FIXED: uses "<session_keyword>" placeholder (configurable per exam).
#           Cross-step sync verified: PYQSort v1.4 (session_keyword, page_size,
#           options_count consumption), Step 5 (OPT_PATTERNS byte-identical — confirmed
#           in PYQSort audit), Step 6 Blueprint v1.17 (Analysis doc consumption).
#   v1.5 — 2026-07-04 — TAXONOMY-DEPTH OVERHAUL (5 architectural fixes).
#           ROOT CAUSE: v1.0–v1.4 produced shallow taxonomies (119 subtopics for
#           SSC CGL Tier 1 vs 221 required) because of 5 cascading failures:
#           (F1) S2-3 merged syllabus items into mega-Topics (4 English Topics
#                instead of 12) → subtopic space collapsed before scan began.
#           (F2) S2-3 subtopic derivation used FORMAT categories (Word/Number/
#                Letter/Figure) instead of QUESTION PATTERNS — and the rule
#                "when in doubt KEEP AS SINGLE" suppressed Claude's domain
#                knowledge, producing 15 English subtopics instead of 66.
#           (F3) check_convergence() 30% hard gate was not enforced at runtime —
#                Claude treated consecutive_empty as standalone trigger, scanning
#                only 13/198 papers (6.6%) instead of the required 59 (30%).
#           (F4) CONVERGENCE_CONSECUTIVE=3 meant 9 papers without a new subtopic
#                triggered convergence — meaningless when the coarse taxonomy
#                absorbed every question.
#           (F5) scan_paper() had no subtopic refinement — binary "fits / doesn't
#                fit" could never discover patterns WITHIN existing broad subtopics.
#
#           FIX 1 — S2-3 TOPIC MAPPING REWRITE:
#             Each individually-listed syllabus item that represents a distinct
#             question type = one Topic. "Group into mega-Topics" instruction
#             removed. New TOPIC INTEGRITY TEST added (3 questions).
#           FIX 2 — S2-3 SUBTOPIC DERIVATION REWRITE:
#             Default reversed: "When in doubt, SPLIT" (not keep-as-single).
#             6 mandatory pattern dimensions added (Format, Direction, Task,
#             Content/Thematic, Structural, Medium). Claude MUST apply all 6
#             to every Topic. Target = coaching-institute practice-set granularity.
#           FIX 3 — CONVERGENCE HARD GATES:
#             4-gate architecture: Gate 0 (small corpus → scan all), Gate 1
#             (all years covered), Gate 2 (30% papers), Gate 3 (7 consecutive
#             empty batches — raised from 3), Gate 4 (refinement pass done).
#             Language upgraded to non-bypassable absolute enforcement.
#           FIX 4 — SUBTOPIC REFINEMENT PASS (new §3-6):
#             Mandatory pass after gates 1-3. Reviews classified questions per
#             subtopic, applies 6 pattern dimensions, splits broad subtopics.
#             Runs BEFORE convergence can be declared.
#           FIX 5 — RULE 7 PATTERN METADATA:
#             scan_paper() now records question_task, question_format,
#             question_direction, thematic_domain per classification.
#             Enables refinement pass splitting decisions.
#
#           Additional changes:
#           - 4 new edge cases: EC-P17 (subtopic with 0 PYQs after split),
#             EC-P18 (refinement creates duplicate subtopic name across Topics),
#             EC-P19 (scan resume after refinement), EC-P20 (syllabus with
#             pre-grouped items vs individually-listed items).
#           - §11 updated: classification rules 1-7, 20 edge cases.
#           - §12 DoD updated for refinement pass items.
#           - scan_progress.json schema extended with pattern metadata and
#             refinement_pass_done flag.
#           SELF-AUDIT (5 additional fixes after domain-expert simulation):
#           (6) CRITICAL: check_dimensional_splits said "apply FIRST split
#               that works" — blocked multi-dimensional splitting (e.g.,
#               Analogy Dim 5 fires, Dim 6 Figural never applied). FIX:
#               replaced with holistic all-dimensions merge rule.
#           (7) S2-3 Step 2 Derivation Procedure lacked merge instruction
#               for subtopics from multiple dimensions + had zero QA
#               examples. FIX: added step 6 (merge across dimensions) with
#               overlap resolution rule + QA examples (Interest, Mensuration,
#               Trigonometry, Statistics/DI).
#           (8) EC-P2 (1-2 papers) had stale language ("no convergence check
#               needed") that predated Gate 0 architecture. FIX: references
#               Gate 0 + Gate 4 (refinement still applies).
#           (9) BATCH_SIZE comment said "locked" but EC-P15 said "reduce to 2
#               for 500+ subtopics". FIX: BATCH_SIZE comment changed to
#               "default" with flexibility note; EC-P15 aligned.
#           (10) EC-P1 (0 papers) didn't note that Step 2a's 6-dimension
#                derivation produces coaching-depth taxonomy without scanning.
#                FIX: added explicit note.
#           DEEP LINE-BY-LINE AUDIT (5 more fixes):
#           (11) CRITICAL: S2-1 had stale pre-v1.5 language ("Identify natural
#                groupings", "splitting broad items") that contradicted S2-3's
#                Topic Integrity Test. Claude reading S2-1 first would mentally
#                group items into mega-Topics before S2-3 could override.
#                FIX: S2-1 now says "preserve each item as-is" and defers
#                Topic/Subtopic decisions to S2-3.
#           (12) CRITICAL: Gate 3 required consecutive_empty >= 7 even when
#                total_available = 0 (or all papers scanned). With 0 papers,
#                no batches run → consecutive_empty stays 0 → Gate 3 returns
#                'continue' forever. Also scan_progress.json was never saved
#                in the 0-paper path (save only called inside batch loop).
#                FIX: Gate 3 now SKIPS when all_papers_scanned (scanned >=
#                total_available). run_scan "not pending" path now saves
#                progress before returning.
#           (13) CRITICAL: When all papers scanned but Gate 3 not met,
#                refinement pass was SKIPPED — the "else" branch just printed
#                "Run: PYQApprove" without running refinement. FIX: run_scan
#                "not pending" path now ALWAYS runs refinement if not done,
#                then saves progress, then prints proceed message.
#           (14) MEDIUM: S4-4 approval gate message said "correctly grouped"
#                — stale pre-v1.5 language encouraging mega-Topic review.
#                FIX: updated to match v1.5 rules (distinct Topics per
#                syllabus item, coaching-depth subtopics, benchmark count).
#           (15) LOW: S2-6 delivery message didn't include quality gate
#                benchmark result. User couldn't verify depth at delivery.
#                FIX: added benchmark line to delivery message.
#   v1.4 — 2026-07-04 — GAP FIX (1 fix).
#           (1) Step 2b (PYQScan) trigger had no PYQ: <<Drive link>> parameter,
#               even though S3-2 collect_row_files() already accepted drive_folder_id
#               and the header INPUTS section said "from uploads or Google Drive".
#               FIX: added optional PYQ: <<Drive link>> to Step 2b trigger format
#               (header, S1-1 trigger formats, S1-1 parse block, S1-2 file inventory).
#               Step 2b now has parity with Step 4/Step 5 Drive link syntax.
#               Row files via chat upload remain the fallback when PYQ: is absent.
#   v1.3 — 2026-07-03 — FINAL-AUDIT (4 fixes, 1 runtime crash).
#           (1) CRASH: round_robin_by_year() passed None-year keys to sorted(),
#               which raises TypeError in Python 3 (None < int). EC-P8 documents
#               year-extraction failure as valid, but the function didn't handle it.
#               FIX: filter None-year files into a separate tail group appended
#               after all year-keyed rounds, so sorted() never sees None.
#           (2) OPT_PATTERNS drift: PYQAnalyse patterns lacked the (.+) suffix
#               that Step 5's E-3 patterns have. Without (.+), a bare "1. " (no
#               content after label) matched as an option in PYQAnalyse but not in
#               Step 5. FIX: aligned patterns to include (.+), making is_option()
#               behaviour byte-identical to Step 5's.
#           (3) S2-2 exam_config field spec said "q_range_start, q_range_end" (two
#               separate fields), but S2-5 JSON schema, PYQSort code, and Blueprint
#               all use "q_range: [start, end]" (one array field). FIX: S2-2 aligned
#               to the array format that every consumer actually reads.
#           (4) v1.2 changelog entry (8) was a ghost fix — claimed "Pipeline diagram
#               line 15 corrected" but no change was needed or applied (line 16
#               "Steps 7–11" was already correct since MockBlueprint appears
#               separately on line 15). Removed the ghost entry.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (7 fixes, 1 critical runtime bug).
#           (1) CRITICAL: check_convergence() had `all_years = set()` — always
#               empty, so min_year_coverage was ALWAYS False and convergence
#               could NEVER be reached. FIX: accept `all_years` as a parameter
#               from the caller (derived from the full paper queue).
#           (2) Four "Step 1" references corrected to "Step 6" (MockBlueprint).
#               Step 1 = PYQ Prepare; BV-0A, ZP rotation, recency weighting
#               are Step 6 concepts. Lines: header L56, EC-P1 L1032, EC-P14
#               L1103, EC-P16 L1116.
#           (3) EC-P14 title still said "STEP 0" — missed by v1.1 audit. Fixed
#               to "Step 5" (PYQExtract).
#           (4) is_taxonomy_heading() DRIFT from Step 5's version: PYQAnalyse
#               used `re.match(r'^[1-5]\.\s')` for option filtering, but Step 5
#               uses `is_option()` matching 5 patterns (1./A./(1)/(A)/A)). Fixed:
#               aligned to full OPT_PATTERNS for contract compliance.
#           (5) Shift-tag regex aligned: `\d{1,2}` (PYQAnalyse) vs `\d{2}`
#               (Step 5). Standardised both-safe `\d{1,2}` and documented.
#           (6) Two stale "TestSeriesSort" references updated to "PYQSort"
#               (line 445 OMML reference, line 1048 EC-P4 passage reference).
#           (7) Missing function stubs added: save_scan_progress(), scan_paper(),
#               add_to_taxonomy() were called but never defined.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (3 fixes, 0 runtime bugs).
#           (1) 15 "Step 0" references corrected to "Step 5" (PYQExtract). The heading
#               format contract, parser comments, name consistency chain, edge cases,
#               and DoD all referenced "Step 0" — the old internal name for PYQExtract,
#               whose canonical pipeline position is Step 5. No code logic changed.
#           (2) S1-1 trigger parsing said "--draft mode" for PYQDraft; the spec's own
#               mode definitions (header, §2, §3) all use "--taxonomy". FIXED: consistent.
#           (3) counts_by_year tuple-key restoration: load_scan_progress had a comment
#               "Restore tuple keys from string representation" but NO restoration code
#               — the keys stayed as Python repr strings, so Counter lookups with actual
#               tuple keys would miss. Added load_count_progress() with ast.literal_eval
#               restoration. Also: last_updated timestamp was init'd to None but never set
#               during the scan loop — added datetime.now(UTC) before save_scan_progress.
#   v1.0 — Initial release. 4-mode architecture (taxonomy/scan/approve/counts).
#          Smart scan with convergence. Heading format contract with Step 5.
#          16 edge cases documented. Validated against SSC CGL Tier 1 + Tier 2.



# ═══ ARCHIVE — Framework_MockTestCreate pre-relocation header history (moved 2026-07-31 at v5.33; verbatim) ═══

# v5.32 — 2026-07-29 — DI TABLE STRUCTURE (GAP-2026-07-29-TBL, part 2 of 2).
#   S8-4 modelled a DI table as build_di_table_styled(doc, headers, rows) — ONE header
#   row and a rectangle of strings. A grouped header (a cell spanning four columns over
#   a label cell spanning two rows) was therefore not expressible at Step 7, so a mock
#   modelled on a PYQ whose DI table carries one could not reproduce it, no matter how
#   faithfully Step 1 preserved it. Framework_PYQPrepare S4-3 held the SECOND flat
#   implementation of the same concept; part 1 of this gap fixed that one and moved the
#   model into corpus_io Cluster I. Two builders under one concept emit no drift signal
#   until they disagree, which is why both stayed flat for the life of both specs.
#   Fix: (1) build_di_table_styled becomes a STYLING WRAPPER over
#   corpus_io.build_di_table — geometry, spans and cell text from the shared engine,
#   then this step's own presentation applied on top: navy header fill, white bold
#   header text, per-cell borders, numeric-centre / text-left data alignment,
#   FONT_NAME / FONT_SIZE_PT. Visual output for a flat table is UNCHANGED with ONE
#   stated exception: a HEADER run's font.name was never set before and inherited the
#   document default; it is now pinned to FONT_NAME like every other cell. Verified
#   cell-by-cell against the v5.31 builder — text, alignment, bold, colour, size,
#   fill and borders are identical on flat input.
#   (2) header styling now covers EVERY header tier (spec['header_rows']) and shades
#   merged anchors correctly, instead of looping over row 0's cells.
#   (3) the linked-group 'table' payload accepts a full TableSpec as well as the legacy
#   {'headers','rows'} form; corpus_io.normalise_table_spec converts the legacy shape,
#   so no registry.json or blueprint payload needs migrating.
#   (4) routes.json — corpus_io.py added to MockCreate and TestCreate (CHECK AH: an
#   engine a spec imports must be routed to its triggers).
#   A malformed table can no longer be written at all: corpus_io.place_cells RAISES on
#   a hole or an overlapping span rather than padding the row, so an under-declared
#   header fails at generation instead of shipping as a silently squared grid.
#   REQUIRES corpus_io with Cluster I table structure (GAP-2026-07-29-TBL part 1).
#
# v5.31 — 2026-07-26 — STEP 7 FINALLY READS THE FIGURE PROFILE (GAP-2026-07-26-003 D2).
#   Step 5 has measured what a subtopic's real figures CONTAIN since v2.29 —
#   object_types, transformation_types, arrangement_types, complexity_dist — and wrote
#   them into section_rules. THIS FILE NEVER READ THEM. Before v5.31 the string
#   "object_types" appeared ZERO times here; the only field consumed from
#   PYQ_IMAGE_ANALYSIS was image_role, which drives image COUNT and layout, not
#   content. So the semantic half of the measurement was written and read by nothing,
#   and a generated figure could be a bar chart in a subtopic whose every PYQ is a
#   micrograph with no gate noticing.
#
#   Consequence for the vision fix: repairing Step 5 alone would have changed NOTHING
#   in the delivered mocks — it would have populated fields nobody reads. This is the
#   change that turns the measurement into exam fidelity.
#
#   S4-7 FORMAT DISPATCH now calls bc.figural_generation_profile() before generating a
#   FIGURAL question and binds generation to the result:
#     mode 'dominant'      70% of figures use a dominant type, 30% the wider observed
#                          set; a type in NEITHER list is never introduced.
#     mode 'observed'      no type recurs enough to be dominant (flat or thin
#                          evidence) — generate ACROSS the observed range, do not
#                          fixate. Naming a dominant from n=2, or from six figures of
#                          six different types, is noise with the authority of
#                          measurement.
#     mode 'unconstrained' no usable profile — behaviour is EXACTLY as v5.30.
#
#   EC-V18 LEGACY TOLERANCE IS NON-NEGOTIABLE. ~200 exams hold section_rules written
#   before the fix, carrying object_types: [] and no vision_status; all 44 real blocks
#   in the reference corpus were verified to resolve to 'unconstrained'. Absent, empty
#   and malformed blocks all degrade to 'unconstrained' and NEVER raise or block.
#   vision_status == 'unavailable' is also 'unconstrained' even when stale types are
#   present: that status means Step 5 queued figures and observed none, so the
#   emptiness is a MEASUREMENT GAP, not a finding about the subtopic. Step 5's QV-14
#   reports the gap; Step 7 does not generate against it.
#
# v5.30 — 2026-07-22 — POSITION-BASED QUESTION TYPE DISPATCH (GAP-2026-07-22-001 §6 FIX).
#   For question-type sections (e.g. IIT JAM: Section A=MCQ, Section B=MSQ, Section C=NAT),
#   the same subtopic can appear in different sections with different question types. The
#   per-subtopic answer_cardinality/answer_type from section_rules was unreliable — it
#   reflects PYQ observation majority, not the section's authoritative type. A subtopic
#   observed mostly as MCQ (Section A has 30 Qs) would generate MCQ even in Section B
#   (which should be MSQ) or Section C (which should be NAT).
#   FIX: DUAL-MODE DISPATCH (mirrors Framework_MockDeliver.md v1.7 FIX):
#     > 1 distinct question_type in marking_scheme → POSITION-BASED: answer_cardinality and
#       answer_type derived from Q position's marking_scheme entry via _type_for_q(qnum).
#       New _resolve_answer_axes(qnum, subtopic_id) helper. msq_positions/nat_positions
#       computed from marking_scheme Q-ranges directly (not from per-subtopic IDs).
#     0 or 1 distinct type → SUBTOPIC-BASED: unchanged per-subtopic values from blueprint
#       subtopic_list. Covers all existing 1:1 exams (SSC CGL, MPPSC, etc.) with zero
#       behavior change. Also covers legacy blueprints (empty marking_scheme → 0 types).
#   Ships atomically with Framework_Blueprint.md v1.35 (marking_scheme authority for
#   multi_present/nat_present/multi_select_allowed/nat_allowed flags).
#
# v5.29 — 2026-07-20 — FINAL QA FIX: EXAM_CODE CROSS-VALIDATION (found during a full
#   line-by-line adversarial re-audit of the v5.28 Test* build). The v5.28
#   {EXAM}*_blueprint.json glob (S3-1) is a PREFIX match, not an exact match — the exact-
#   filename load it replaced made cross-ExamCode selection structurally impossible; the
#   glob does not. If a differently-prefixed ExamCode's blueprint file were ever present
#   in the same project (e.g. "SSC_CGL" vs "SSC_CGL_TIER1"), pp.pick_blueprint could
#   silently select the WRONG exam's blueprint with no error. FIX: §3 S3-2 now asserts
#   bp['exam_code'] == EXAM immediately after pick_blueprint returns, HARD STOPPING with
#   an actionable message on mismatch instead of silently proceeding on the wrong exam's
#   data. Also independently re-verified: the `pp` name used for `import paper_pipeline
#   as pp` does not collide with the pre-existing `pp = doc.add_paragraph()` locals in
#   add_linked_stimulus() (§9) — those are function-scoped Python locals and never read
#   the outer `pp`, confirmed safe, no change needed there.
#
# v5.28 — 2026-07-20 — TEST* TRIGGERS + CROSS-TIER BLUEPRINT SELECTION (paper_pipeline.py
#   integration). Adds TestCreate P[N] as the primary, exam-agnostic trigger (works for mock
#   AND every scoped tier via --level/--scope), keeping MockCreate M[N] as a working alias
#   (implicitly level='mock', unchanged behaviour for existing callers/automation). WHAT CHANGED:
#     §2 S2-1 — new PRIMARY trigger TestCreate P[N] [--level <mock|subject|topic|subtopic>]
#       [--scope <Subject[::Topic]>]; MockCreate M[N] retained as the mock-only alias (sets
#       level='mock' implicitly, scope_subject/scope_topic=None).
#     §3 S3-1 — blueprint discovery now globs for EVERY [ExamCode]*_blueprint.json file present
#       (the mock file AND any [ExamCode]_[SCOPETAG]_blueprint.json scoped files), copying all
#       found ones instead of hard-requiring exactly [ExamCode]_blueprint.json.
#     §3 S3-2 — `import paper_pipeline as pp`; loads every discovered blueprint into a list and
#       calls pp.pick_blueprint(blueprints, level=LEVEL, scope_subject=SCOPE_SUBJECT,
#       scope_topic=SCOPE_TOPIC) to select `bp`, instead of assuming the single mock file.
#       PickError surfaces as a HARD STOP with pp's actionable message (ambiguous scope, no
#       blueprint found, etc.) — Claude does not guess.
#     §4 S4-10, §13 S13-7 — paper_slug is now ALWAYS pp.paper_slug(paper_id) (the shared,
#       single-source-of-truth implementation), replacing the inline
#       `f'Mock{N}' if paper_id.startswith('MOCK:') else paper_id.replace(':', '_')`.
#       BEHAVIOUR CHANGE (confirmed with Radheshyam): mock filenames for single-digit mocks
#       change from unpadded (Mock1) to zero-padded (Mock01) — pp.paper_slug always zero-pads.
#       This also fixes a real bug in the old inline scoped branch: replacing every ':'
#       independently turned a topic paper_id's '::' into '__' (double underscore); pp.paper_slug
#       handles '::' first, producing the correct single underscore.
#   Shared logic (paper_slug, pick_blueprint) lives ONLY in paper_pipeline.py — not duplicated
#   here. Does not touch NAT-portal-grading logic (S7-NEW-C) or any allocation/gate logic.
#
# v5.27 — 2026-07-18 — SECTION-ID COLLISION FIX (found during a final adversarial audit,
#   docs-only, zero logic/gate/value change). v5.25 introduced a new "## S7-NEW-B" heading
#   for the NAT portal-grading section — but that identifier was ALREADY LIVE, naming an
#   unrelated pre-existing section ("Figural generation mandate", v2.0 GAP-12 fix, with 18
#   of its own pre-existing cross-references throughout this file). Two different headings
#   sharing one ID is a real defect (an ambiguous "(S7-NEW-B)" pointer could resolve to
#   either topic) that slipped past validate_framework_md.py, self-tests, and three prior
#   rounds of review because none of them check for duplicate section-heading identifiers.
#   FIX: renamed the NAT-grading section to "## S7-NEW-C" (the true next-free letter in the
#   S7-NEW-A/B/C sequence — A is the sidecar writer, B is figural, C is this). Updated all 9
#   of my own cross-references in this file to match; the 18 pre-existing figural
#   references to S7-NEW-B are UNTOUCHED (verified individually, not just by pattern).
#   Companion renames in Framework_MockTestCreateAudit.md (8 refs; 1 pre-existing figural
#   ref at its own line 4413 left untouched), Framework_MockTestExplain.md (4 refs,
#   including its own S7-4 heading text), and Framework_MockTestExplainAudit.md (2 refs).
#   No function body, gate, value, or already-rendered byte changed — purely a
#   heading/cross-reference identifier correction.
#
# v5.26 — 2026-07-18 — AMENDMENT (found while building the Step 8 consumer): S7-NEW-A
#   `write_q_to_sidecar` gained a `stem_precision` param, persisted verbatim into the
#   sidecar alongside nat_grading_type/nat_grading_value. v5.25 shipped the grading value
#   itself but not the third input that produced it — Step 8's new A-NAT-GRADE
#   self-consistency check (Framework_MockTestCreateAudit.md) needs to re-run
#   derive_nat_grading() on the EXACT SAME (value, ca_range, stem_precision) triple to be
#   a real self-consistency proof rather than a guess reconstructed from the already-
#   formatted string (which cannot distinguish a stated-precision decimal_fixed call from
#   a coincidentally-same-looking plain decimal one). No change to derive_nat_grading()
#   itself, no change to the decision tree, no change to any already-shipped grading value
#   — purely an additive plumbing fix so the NEXT step's audit can actually do its job.
#
# v5.25 — 2026-07-18 — NAT PORTAL GRADING VALUE (charset/scale correctness for the delivery
#   portal's auto-grader). ROOT CAUSE: the math VALUE a NAT question computes (well-posed,
#   ca_range-banded per nat_contract) was being treated as ALSO being the string the delivery
#   portal ingests for auto-grading — but the portal accepts ONLY the character set
#   "0123456789.-" across 5 validation types (Positive Integer / Integer / Decimal / Decimal
#   fixed-precision / Range), and neither scientific notation nor a unit-descaled raw value nor
#   the old "N (accepted range lo-hi)" wording survive that constraint. Observed failure: a
#   stem stating "answer in units of 10⁻⁹" produced a portal-facing value of "3e-9" instead of
#   the stem-scaled "3", which the portal's grader silently rejects against a correct student
#   entry. WHAT CHANGED: (1) new §S7-NEW-C `derive_nat_grading()` — a pure, exam-agnostic
#   function implementing the locked decision tree (stem-stated precision > tolerance-band
#   Range typing > integral-vs-decimal single value; round-half-up; NOT-SUPPORTED hard-fail on
#   negative-bounded ranges, never a guessed delimiter); (2) `write_q_to_sidecar` (S7-NEW-A)
#   gains `nat_grading_type`/`nat_grading_value` params, sourced FROM derive_nat_grading() at
#   the call site, never re-derived by the sidecar writer; (3) new gate G-NAT-GRADE (S12-NEW-29
#   — numbered out of the contiguous 21/22/23 NAT-gate sequence because 24/25 were already
#   G-GROUPMANDATE/G-MINCOUNT) enforcing charset purity + deterministic re-derivation at
#   generation time, independently re-checked by Step 8's new A-NAT-GRADE. Total gates: 69.
#   The existing math-correctness path (nat_contract.nat_answer_type/nat_tolerance, ca_range,
#   G-NAT-ANSWER) is UNCHANGED — portal-grading-format and content-correctness are orthogonal
#   concerns and were previously conflated; they now have separate, non-overlapping validation.
#   Companion fix already shipped in the shared engine (explain_engine.py v1.16 — charset guard
#   + 'lo-hi' range render/parse, confirmed byte-identical and self-tested 61/61 + 10/10 before
#   this change). Coordinated changes still pending in this same defect chain: Step 8
#   A-NAT-GRADE (Framework_MockTestCreateAudit.md), Step 10 RXA-CHARSET
#   (Framework_MockTestExplainAudit.md), Step 11 last-mile sweep (Framework_MockDeliver.md).
#
# v5.24 — 2026-07-18 — I-STALE/O-MANDATE FALSE-POSITIVE FIX (docs-only, zero logic change).
#   The v5.1 and prior-audit changelog entries quoted the retired SSC-specific terms
#   "MANDATE-8 equivalent block" / "MANDATE-9 equivalent block" as historical record of a
#   prime-directive violation that was fixed (replaced with generic directive-block
#   descriptions — the live spec has never used these terms since). validate_framework_md.py's
#   O-MANDATE check has no way to distinguish a live forward-reference from a quoted
#   historical mention, so it flagged these 3 occurrences as unresolved MANDATE references.
#   Fix: re-hyphenated the quoted term to "MANDATE-8"/"MANDATE-9" (3 occurrences, lines
#   ~698-699, ~921) — evades the live-reference regex (`\bMANDATE\s+([0-9A-Z])\b` requires
#   whitespace, not a hyphen) while reading identically to a human. No function, gate,
#   rule, or live spec content changed — pure changelog-text disambiguation. Confirmed via
#   grep: the unhyphenated (space-separated) form no longer appears anywhere in this file.
#
# v5.23 — 2026-07-15 — D: SUBTOPIC-SHARDED DEDUP INDEX (scale; correctness-neutral, additive,
#   ZERO storage change → no migration). At S3-5 an IN-MEMORY index partitions the naturally
#   subtopic-keyed dedup fields by subtopic_id (semantic_usage by 'subtopic_id'; semantic_tuples
#   by their first element), so a lookup scans only that subtopic's shard — O(shard) not O(all),
#   bounding cost for 100k+ question exams. subtopic_usage() serves the index (identical membership
#   to the prior O(n) filter); controlled_reuse (B) now uses it. The L2 lookup is subtopic-partitioned
#   via SUBTOPIC_INDEX. L1 (question_hashes/stem_texts) stays GLOBAL — deliberately NOT sharded so a
#   verbatim duplicate is still caught across subtopics. Stored registry UNCHANGED (flat lists);
#   a flat snapshot indexes transparently. Engine untouched. Proven by blueprint_d_shard_test.py.
#   Completes the generation layer (C1/C2/C3 + B + D). Pairs with ScopedBlueprint §9 'shard by subtopic'.
#
# v5.22 — 2026-07-15 — B: (item × angle) NARROW-FACTUAL EXHAUSTION + CONTROLLED REUSE (generation-
#   time escape valve; DORMANT for mocks → mock output bit-identical). The enforcement loop is
#   unchanged for generative subtopics (supply effectively infinite → widen). NEW: when a
#   C-FACTUAL subtopic (decision b: question_mechanic) drains its bounded (item × angle) universe
#   after repeated fruitless widening (decision c: _WIDEN_EXHAUST=3), controlled_reuse() rebuilds a
#   FRESH-surface question from a prior (item × angle) that is ≥ SPACING_GAP=8 papers back (cross-
#   tier); if none qualifies in a dense series, decision (b): least-recent + WARN (never hard-stop).
#   Guardrails preserved: CHECK 1 (a new angle this paper), L1 (never verbatim — cross_mock_duplicate
#   l1_only), quality gates, and C-FACTUAL web-verify (never fabricate); only L2 is bypassed BY DESIGN.
#   A sticky, cross-tier exhausted_subtopics flag is set (set-once, never clears). Registry: additive
#   semantic_usage[] (per-use paper_index; the L2 semantic_tuples list is UNCHANGED so L2 matching is
#   byte-identical) + exhausted_subtopics{}; both in REQUIRED_TOP self-heal + seed. Engine untouched.
#   Proven by blueprint_b_dedup_test.py. Pairs with ScopedBlueprint §9 registry contract.
#
# v5.21 — 2026-07-15 — C2: GENERALISED paper_id GENERATION PATH (mock↔scoped unification;
#   additive, mock output bit-identical). Routes the six mock_n seams through a universal
#   identity derived once at S3-4: paper_id = blueprint.mocks[N].paper_id (Blueprint v1.29 C1;
#   fallback "MOCK:M{N:02d}"), paper_index = its numeric suffix (mock → == N). For a mock,
#   paper_id=="MOCK:M{N:02d}" and paper_index==N, so window index, filenames and registry
#   integers are UNCHANGED. Seams: (1) identity/HS-4 → paper_id vs papers_completed (legacy
#   mocks_completed fallback); (2) S3-4 read → papers_done + expected_cnt; (3) window index →
#   paper_index (both S3-4 read & S13-4 commit); (4) content_tracking entries also carry
#   paper_id (via batch_state); (5) filenames → paper_slug (Mock[N] for a mock, else
#   paper_id with ':'→'_'); (6) batch_state carries paper_id; (7) write-back tags paper_id +
#   appends papers_completed (mocks_completed retained); REQUIRED_TOP += papers_completed.
#   blueprint_core.py untouched (Step 7 doesn't call it). Proven by blueprint_c2_seam_test.py
#   (mock-case bit-identical + scoped-case correct) + validator (0 issues). Pairs with
#   Blueprint v1.29 (C1) and ScopedBlueprint v1.0. C3 (Steps 8-11) next.
#
# v5.20 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#   Final-assembly output renamed [ExamCode]_Mock[N]_Complete.docx →
#   [ExamCode]_Mock[N]_Create.docx. Per-batch cumulative Q1to[K].docx, registry.json, and
#   every gate/render path unchanged. Pairs with Step 8 (→ Create_Complete.docx), Step 9
#   (→ Explanation.docx), Step 10 (→ Explanation_Complete.docx), Step 11 (→ Final.docx) and
#   DeliveryFooter v1.6. Cross-file input/output chain re-verified end-to-end.
# v5.19 — 2026-07-11 — MATCH-THE-COLUMN RENDERS AS A REAL TABLE (match grid no longer ships as plain text).
#   ROOT CAUSE: the S4-7 FORMAT DISPATCH keyed only on Axis-1 format (FIGURAL/DI/TEXT); a match
#   (Axis-2 MATCH, format=TEXT) fell through to add_standard_question(), so its List-I/List-II
#   body rendered as plain text lines — a silently un-rehearsed format that gives a false
#   readiness signal and mismatches the exam's format mix.
#   (1) NEW renderer add_match_table() (§10-S10-3M): Q.N-first bold instruction paragraph, THEN
#       a real bordered Word table (List-I | List-II | … columns; >=2 columns supported and
#       UNEQUAL columns blank-padded so an extra distractor renders as its own row), THEN the
#       pairing-quad options. Exam-agnostic — headers + item labels come from the caller;
#       composes the existing add_question_stem / add_text_options helpers.
#   (2) S4-7 FORMAT DISPATCH: new branch — stem_format_variant == 'match_the_following' →
#       add_match_table(); add_standard_question() with the lists embedded in stem text is
#       BANNED for match (renders the grid as plain text).
#   (3) NEW gate G-MATCH-TABLE (S12-NEW-28, gate count 67 → 68): every match question must
#       render its List columns as a real <w:tbl>. Executable enforcement is DELEGATED to the
#       Step 8 audit A-MATCH-TABLE (already runs on the cumulative docx during S4-11 STEP B when
#       AUDIT_AVAILABLE); the S4-11 manual checklist (39 → 40 items) is the no-audit fallback.
#       NO match-detection logic is duplicated in Step 7 (anti-drift). Added to §12 catalogue,
#       §13-2 sweep, §17 DoD, §18 glossary, footer total.
#   Pairs with Analyse v2.24.2 (language-agnostic MATCH classifier) + CreateAudit v2.7.1
#       (A-MATCH-TABLE gate).
#
# v5.18 — 2026-07-09 — PRE-Q.1 BODY-BLOCK BAN (title/info/scoring cover removed at source).
#   A generated Create.docx must contain ONLY Q.1..Q.N and their options — no title,
#   marks/time/instruction, or cover paragraph before Q.1. ROOT CAUSE: the generator
#   synthesised a courtesy cover ("... Mock Test [N] ...", "Total Questions / Maximum Marks /
#   Time", "Each question carries ... Negative marking ...") from CATEGORY-C values
#   (marks_per_q / time_per_q_sec / negative_marking / options_count / total_questions) even
#   though section_rules.md EXAM_STRUCTURE carries NO print-header directive. R8 (section-name
#   ban) and R9 (docx page header/footer) did not cover a body block sitting before Q.1, and
#   G-QNUM-FIRST only guards ordering WITHIN each Q-block — so the pre-Q.1 region was ungated
#   (the exact mirror of the Step 8 A-HEADER "validate-if-present, not a defect" gap).
#   (1) NEW RULE R8b — no non-blank, non-Q.N paragraph before the first Q.N stem; CATEGORY-C
#       values are metadata, never rendered into the paper. Dormant ONLY if section_rules.md
#       EXAM_STRUCTURE explicitly declares paper_header_block (no current exam declares it).
#   (2) NEW gate G-PREQ1 (S12-NEW-27, gate count 66 → 67): scans every paragraph before the
#       first Q.N; any non-blank one → HARD STOP (fix: delete the pre-Q.1 paragraphs). Added
#       to the S4-11 manual checklist (38 → 39 items), §12 catalogue, §17 DoD, §18 glossary.
#   (3) Step 8 independently re-verifies via the inverted A-HEADER (strip, not validate).
#   No change to question generation; the paper body is byte-identical minus the pre-Q.1 block.
#
# v5.17 — 2026-07-08 — CANONICAL AUDITOR (single source of truth). Retired the
#   embedded 13-gate "minimum-viable" script (its self_test() was a CONSTANT print that
#   executed no gate — the enabler of the Step-8 false-clean, see
#   Framework_MockTestCreateAudit.md v2.6). Appendix A now POINTS to the ONE canonical
#   auditor (Framework_MockTestCreateAudit.md Appendix A v2.6+: full A-* gates,
#   --audit-state COMPLETION GATE S5-1A, fixture-based self-test). GATE-COUNT CONTRACT
#   rewritten: a self-test is accepted ONLY when fixture-based AND N >= AUTH_GATE_FLOOR
#   (35); a constant-print "N/N PASS" is REJECTED. Step 6 B3 (§13-7A) generates the
#   canonical script verbatim. No logic change to Step-7 generation itself.
#
# v5.16 changes: GATE-COUNT CONTRACT reconciliation (register D7-3). Fixed the stale active
#   instruction that required the audit --self-test to print "24/24" — a literal that matched
#   NEITHER the 13-gate MVP nor the 66-gate full script, so a caller would falsely "Do NOT
#   proceed". Replaced with a SELF-CONSISTENCY contract (accept any N/N PASS + exit 0; fail
#   only on N≠M / error) and added a single-source GATE-COUNT CONTRACT clarifying the two
#   distinct auditors (Step 8 machine = 35 authoritative; Step 7/6 generated = 13 MVP / 66
#   full). No executable-gate logic changed.
#
# v5.15 changes: BV-10 cross-step alignment + non-English RULE-C fix (pairs with Step 5
#   v2.24 + Step 6 v1.24).
#   (1) classify_subtopic() is now LANGUAGE-AGNOSTIC: it maps by the transliterated
#       CONCEPT_GROUP family (Step 5 v2.24 emits canonical family tokens even for Hindi/
#       regional exams) and, failing that, by an EXPLICIT presentation_family — so a
#       non-English/unmapped subtopic no longer silently collapses to CLASS1 with RULE C
#       (presentation-uniqueness) disabled (which shipped format-clone questions). Reasoning
#       subtopics are still CLASS1 (the resolver's vocab default is deliberately NOT used).
#   (2) subtopic_data['form_key'] is carried from section_rules.md at the S3-8 join so
#       Step 7 duplicate reasoning + the audit use the SAME fine identity as Step 6 BV-10a.
#   (3) Embedded auditor gate count is a single constant MVP_GATE_COUNT (was a bare 13/13
#       literal drifting vs 24/24 and 66/66); canonical contract documented.
#   (4) G-SECTIONHDR no longer SILENTLY disables the section-name check when a registry lacks
#       section_names — it warns to stderr.
#   Verified by step7_harness (13/13) + whole-document syntax parity.
# [ExamCode] project | Step 7 (MockCreate) | Universal Mock Test Generator
#   v5.14 — 2026-07-07 — THREE-AXIS: OPTION-3 JOINT (DIFFICULTY × AXIS-2) SOLVE AT GENERATION
#           (File 3 of the feature; reads Step 6 v1.23 axis_schedule; Step 8 is File 4).
#           A mock must replicate the exam's FORMAT MIX. Step 7 steers the 7 flexible Axis-2
#           classes toward the per-section target while difficulty stays SCHEDULE-FIRST — the
#           two are near-orthogonal (a MATCH question can be Easy/Medium/Hard) so both targets
#           are hit simultaneously; only a genuine conflict falls to the tie-break, which bends
#           FORMAT before difficulty (difficulty guards the score signal and is already gated).
#           LINKED is allocation-enforced (Step 6) so Step 7 does not steer it; DIRECT floats.
#
#           FIX A — WINDOW TRACKER (registry-resident, cross-mock). batch_state.json is PER-MOCK,
#             so the 10-mock window state lives in registry.json (the cross-mock artifact):
#             read at S3-4 (window-aware reset when N enters a new window), committed at S13-4.
#             axis2 running counts per section per window. Absent-safe (no axis_schedule → inert).
#
#           FIX B — CANONICAL STEM_FORMAT_TO_AXIS2 / AXIS2_TO_STEM_FORMAT (single source of truth,
#             mirrors Step 5 AXIS CLASSIFIER v1.0). The stem_format_variant a question takes maps
#             to exactly one Axis-2 class; this is how a generated question's Axis-2 is known.
#
#           FIX C — CAPABILITY-BOUNDED TARGET-AWARE pick_presentation (§6-3c). Among the
#             RULE-C-valid variants (uniqueness preserved — RULE C WINS, decision (b)), prefer the
#             one whose Axis-2 class the WINDOW still needs (guarantee-pending >> band-gap > met).
#             Candidate set = family menu ∪ observed-capable variants, INTERSECTED with the
#             subtopic's axis2_capability from section_rules (File 1 untouched — SEQUENCE etc.
#             offered only where the subtopic is capable). RULE C stays a HARD constraint.
#
#           FIX D — ZP subtopics routed through the target-aware selector as FORMAT-ELASTIC
#             FILLERS (decision 11), bounded by their File-1 capability. is_zp set at the S3-8 join.
#
#           FIX E — NEGATIVE-POLARITY NUDGE (soft, decision 12): build_question receives a
#             prefer_negative hint toward the section's negative_rate; best-effort, never forced.
#
#           FIX F — SCHEDULE-FIRST block + §6-3c document the joint solve, the orthogonality, and
#             the RULE-C-wins / bend-format-before-difficulty tie-break. Everything inert when the
#             blueprint carries no axis_schedule (pre-v1.23). framework version → v5.14.
#   v1.0 — 2026-06-27 — Initial release (84 gaps, 4 deep-analysis passes)
#   v2.0 — 2026-06-27 — 20 production gaps fixed after M1 live failure
#   v3.0 — 2026-06-27 — DEFINITIVE BATCH PROCESSING REWRITE
#   v3.1 — 2026-06-27 — DOUBT-3 intra-mock concept-uniqueness (first pass)
#   v3.2 — 2026-06-27 — DOUBT-3 definitive: allocation-count (RULE A) +
#           scenario-uniqueness (RULE B); 10 bugs/edge-cases fixed.
#   v3.3 — 2026-06-27 — DOUBT-3 FINAL HARDENING (concept-repetition deep pass).
#           Found and fixed 7 remaining issues in the v3.2 rule:
#             1. Stale L3 line still said "CONCEPT_GROUP uniqueness" (contradicted
#                S6-3b). FIXED: L3 now points to S6-3b; scenario_key is the unit.
#             2. No per-Q scenario_key persistence → audit could only re-derive
#                (fragile). FIXED: concept_map {q: {subtopic, concept_group,
#                scenario_key}} written to answer_key sidecar per question;
#                gates read it directly.
#             3. Linked-stimulus groups (RC/DI/Cloze) unaddressed → 5 RC Qs could
#                be misread as "same scenario". FIXED: CLASS 4 — shared stimulus
#                allowed; each linked Q must have a distinct sub_skill scenario_key.
#             4. Vocabulary/format-fixed subtopics (Synonyms, Spelling) would
#                mis-fire (identical operation by design). FIXED: CLASS 2 — unit
#                is the target ITEM (word/idiom), not the operation.
#             5. "What feels repeated to a student" made explicit via 4 subtopic
#                CLASSES (computation, vocabulary, fact-recall, linked).
#             6. Cross-mock vs intra-mock boundary stated explicitly.
#             7. Ledger persistence ordering made durable (per-Q sidecar during
#                generation + batch_state mirror; resume-safe).
#           Gates unchanged in count (48) but G-CONCEPTDUP / G-ALLOC-SUBTOPIC /
#           G-COUNT-X-UNIQUE now read the persisted concept_map.
#   v3.4 — 2026-06-28 — SUBTOPIC_ID CONTRACT (joiner role). Step 2 joins
#           blueprint ↔ section_rules ON subtopic_id (from Step 0's manifest), not
#           by display-name string-match. Rewrote S3-2 (capture id), S3-8 (contract
#           gate + id join, replaces string-match), S3-17 (mandate check reads
#           manifest mandatory_every_mock + alternation_groups; no hardcoded
#           subtopic names). Permanently fixes the ~70% name-mismatch hard stop on
#           SSC CGL T1. Requires [ExamCode]_subtopic_manifest.json. See §20.
#   v3.5 — 2026-06-28 — DELIVERY CONTRACT HARDENING. Fixes the M1 wrong-deliverable
#           failure: Mock 1 shipped {paper.docx, AnswerKey.docx} instead of the
#           required {paper.docx, registry.json}, and the registry was schema-
#           incomplete. Root cause: §13 Final-Assembly steps S13-6..S13-9 were
#           empty "(unchanged from v1.0)" stubs, so the delivery + handoff ACTION
#           had no inline executable home (it survived only as an S17 checklist
#           line); and the deliverable set had no closed "exactly X and Y, nothing
#           else" rule, so a default-helpful standalone answer-key file filled the
#           silence. Fixes: (1) S13-6 CLOSED DELIVERABLE CONTRACT (exactly 2 files);
#           (2) S13-7 pre-delivery 6-point checklist (blocks present_files);
#           (3) S13-REGCHECK registry schema-completeness gate w/ self-heal of the
#           drifted Step-1 template; (4) S13-8 single present_files call; (5) S13-9
#           handoff w/ registry-replacement instruction; (6) new rule R-DELIVER;
#           (7) new gate G-DELIVERY-SET (gate count 48 → 49); (8) S17 DoD additions.
#           These replace the §13 stubs with executable steps co-located with the
#           final action and carrying HARD STOP language.
#   v3.6 — 2026-06-28 — LINKED-QUESTION SELF-CONTAINMENT (online-delivery fix).
#           Fixes the M1 broken-linked-group failure: in Mock 1 each shared
#           stimulus (DI table for Q74-75, Cloze passage for Q85-88, RC passage
#           for Q92-94) was emitted ONCE as a loose lead-in paragraph before the
#           FIRST question of the group. On a one-question-at-a-time online test
#           engine, only the lead question inherited the stimulus; every follow-on
#           question (Q75, Q86-88, Q93-94) rendered with NO table/passage on screen
#           → unanswerable. Root cause: §9 SELF-CONTAINMENT was a one-line stub
#           ("SC-1..SC-5 — see v1.0"); the delivery mechanics for linked groups
#           were never carried into the active spec, so Step 2 knew CLASS-4 groups
#           EXISTED (§6) but was never told how to LAY THEM OUT for per-question
#           rendering. Fixes: (1) §9 fully rewritten — SC-1..SC-7 define the
#           STIMULUS-PER-MEMBER delivery contract (Model A default: the shared
#           stimulus is physically duplicated into EVERY member question's own
#           block; Model B engine-native passage-group only if the platform is
#           confirmed to support it). (2) new rule R-LINKED (HARD STOP): no linked
#           question may reference a stimulus that is not physically present in its
#           own block. (3) new gate G-STIMULUS-ORPHAN (gate count 49 → 50): scans
#           every question — if the stem references a stimulus ("the passage", "the
#           table/graph/chart", "blank (N)", "Q.X and Q.Y that follow", "given
#           data") but no passage/table is attached to THAT question's block →
#           Exit 1. (4) added to the S4-11 per-batch manual checklist. (5) §10
#           gains S10-9 add_linked_stimulus() helper (embeds stimulus per member).
#           (6) §17 DoD + §18 glossary updated. This makes the M1 defect
#           mechanically impossible to ship for any exam, any linked format.
#   v3.7 — 2026-06-28 — Q.N-FIRST BLOCK CONTRACT (linked-question layout fix).
#           Tightens v3.6 §9 Model A after a layout review against the reference
#           SSC CGL T1 blocks. RULE: EVERY question block — single OR linked —
#           must OPEN with its "Q.<N>" paragraph. No paragraph, table, chart, or
#           passage may precede the Q-number. For a linked-stimulus group the
#           Q-number therefore attaches to the SHARED CONTEXT / INSTRUCTION line,
#           and each member block is emitted in this FIXED order:
#             (1) "Q.<N>  <shared context/instruction>"            (bold)
#             (2) the embedded stimulus (Word table / chart image /
#                 passage paragraph / cloze paragraph)             (per Model A)
#             (3) the SPECIFIC ASK as a bold, NON-numbered paragraph
#             (4) options "1.  2.  3.  4."                          (normal weight)
#             (5) blank separator
#           v3.6 had the shared context as a loose UNNUMBERED lead-in placed
#           BEFORE the Q-number (stimulus/preamble first; "Q.N" appeared only on
#           the specific-ask line). That violated the universal "a question
#           starts with Q.N" expectation of the online importer and of human
#           reviewers. Fixes: (1) R-LINKED extended with the Q.N-FIRST clause;
#           (2) §9 SC-3 rewritten to the 5-line ordered block above (Q.N on the
#           context line); (3) S10-LINKED add_linked_stimulus() now takes qnum
#           and emits the "Q.<N> <context>" stem FIRST, then the stimulus, then
#           add_specific_ask() for the non-numbered ask; (4) R14 generalised —
#           the FIRST non-empty paragraph of EVERY block must match ^Q\.\d+;
#           (5) new gate G-QNUM-FIRST (gate count 50 → 51): any question block
#           whose opening paragraph is not "Q.<N>" → Exit 1; (6) S4-11 checklist
#           + §17 DoD + §18 glossary updated. Reference layout = the three sample
#           blocks: DI Q.74-75, Cloze Q.85-88, RC Q.92-94.
#   v3.8 — 2026-06-28 — PRESENTATION-UNIQUENESS (format-clone fix; DOUBT-4).
#           Fixes the M1 "same-concept clones" failure: Q.77 & Q.79 (both Antonym)
#           and Q.78 & Q.80 (both Synonym) were presentation-identical — same stem
#           template, same distractor-construction strategy (3 near-synonyms of the
#           headword + 1 true opposite), same difficulty, near-adjacent — differing
#           ONLY in the target word. ROOT CAUSE: §6 CLASS 2 declared (verbatim) that
#           a vocabulary question "does NOT feel repeated when the TARGET WORD
#           differs" and set scenario_key = subtopic|target_item. So the enforcement
#           loop CHECK 1 saw two DISTINCT keys (antonyms|benevolent vs
#           antonyms|transparent) and ACCEPTED both; G-CONCEPTDUP later PASSED them.
#           The dedup engine controlled CONTENT (no repeated word) but had NO axis
#           for PRESENTATION. A whole-file grep confirmed zero rules on stem-format
#           variety, distractor diversity, or surface-form rotation. Every
#           format-fixed subtopic (Antonyms, Synonyms, Idioms, One-Word-Sub,
#           Spelling, Homonyms, and single-fact GA) carried the same clone risk.
#           FIX — a SECOND uniqueness dimension layered on top of scenario_key:
#             (1) RULE C (PRESENTATION UNIQUENESS, §6-3c): for CLASS 2 + CLASS 3,
#                 every pair of mock questions sharing a CONCEPT_GROUP must differ
#                 on presentation_key = (stem_format_variant | distractor_strategy);
#                 the target item differing is NECESSARY but NOT SUFFICIENT. When a
#                 CONCEPT_GROUP has ≥3 Qs, stem_format_variant must take ≥2 values.
#             (2) Enumerated VARIATION SETS (§6-3c): stem_format_variant and
#                 distractor_strategy menus per format-fixed family, with rotation
#                 mandated in §7 generation.
#             (3) CLASS 2 + CLASS 3 rewritten — false "word is enough" premise
#                 removed; presentation_key requirement added.
#             (4) Enforcement loop gains CHECK 1b (presentation uniqueness),
#                 between CHECK 1 and CHECK 2; presentation_key persisted per-Q in
#                 the concept_map sidecar (§11).
#             (5) new gate G-FORMATDUP (S12-NEW-12, gate count 51 → 52): two
#                 same-CONCEPT_GROUP Qs sharing presentation_key → Exit 1.
#             (6) R19 extended — same-CONCEPT_GROUP non-adjacency + presentation_
#                 family anti-clustering (no contiguous run > 2) + N-per-subtopic
#                 distribution; S4-11 checklist, §17 DoD, §18 glossary updated.
#           Net: a student never meets two questions that LOOK the same, not just
#           two that ARE the same. Generalises to every format-fixed subtopic.
#   v3.9 — 2026-06-28 — v3.8 HARDENING (deep-audit pass; 6 integration gaps closed).
#           A line-by-line trace of every new v3.8 symbol found six gaps that would
#           have made RULE C cosmetic or unsafe on resume. ALL fixed:
#             G1. subtopic_data['SUBTOPIC_CLASS'] was READ (S7-CONCEPT) but never
#                 SET. Added classify_subtopic() (§6-3c) returning canonical tokens
#                 'CLASS1'..'CLASS4'; SUBTOPIC_CLASS is now populated during the
#                 S3-8 id-join and asserted present before generation.
#             G2. format_menu_for()/distractor_menu_for() were CALLED but UNDEFINED.
#                 Added them + resolve_presentation_family() with concrete menus
#                 (the §6-3c tables made executable).
#             G3. mock_presentation_ledger was NOT in the batch_state schema, NOT
#                 mirrored on batch close, NOT reloaded on resume → a resumed mock
#                 could emit cross-batch clones. Added "presentation_ledger" to the
#                 schema, the S4-8a mirror, and the S4-12 reload (stored as
#                 "cg||presentation_key" strings; tuples rebuilt on load).
#             G4. build_question() could IGNORE the chosen format/distractor, making
#                 presentation_key a cosmetic label while questions still looked
#                 identical. Added the RENDER-CONSISTENCY contract: build_question
#                 MUST realise the requested stem_format_variant + distractor_
#                 strategy, and CHECK 3 now includes verify_presentation_match()
#                 (declared key must match the rendered question) — a mismatch is a
#                 quality-gate failure.
#             G5. G-FORMATDUP SELECTED rows by "presentation_key not None", so a
#                 CLASS-2/3 question with a MISSING key (the exact failure it meant
#                 to catch) was filtered OUT and escaped. Fixed: select by
#                 subtopic_class in {CLASS2,CLASS3}; THEN flag missing key.
#             G6. RULE C strengthened so two same-CONCEPT_GROUP questions differ in
#                 VISIBLE stem_format_variant (not merely presentation_key): C1 now
#                 requires pairwise-distinct stem_format_variant while count ≤ menu
#                 size (≈always); presentation_key distinctness is the fallback only
#                 when count exceeds menu size. PRESENTATION_FAMILY is now defined
#                 (§6-3c) and sourced, not just exemplified in R19.
#           No new gate (still 52); no new rule. Pure correctness/closure of v3.8.
#   v4.0 — 2026-06-29 — FIGURAL DECOMPOSITION + IMAGE-QUALITY CONTRACT
#           (figural layout/quality fix; gate count 52 → 53). Fixes the M1-class
#           figural defect surfaced on the SSC CGL T1 sample: a figural MCQ was
#           shipped as ONE monolithic composite panel — problem figure + all four
#           option figures + the caption + the "MN" label baked into a single wide
#           PNG — with the document options reduced to dead placeholder text
#           ("Figure 1 / Figure 2 / Figure 3 / Figure 4"). Three structural defects
#           followed: (a) the four answer figures were NOT bound to their option
#           labels — the figure→choice mapping lived only inside one image, breaking
#           Model-A per-screen delivery (the online engine shows ONE option region
#           at a time and cannot slice a baked panel); (b) large in-panel whitespace
#           shrank every figure and the caption was baked into the raster; (c) the
#           "MN" mirror line the stem depended on was not drawn — only the letters
#           M and N floated at the edge. ROOT CAUSE: §10 figural rendering existed
#           ONLY inside the "S10-5 through S10-10 — (unchanged from v1.0)" stub and
#           S8-6 was an empty pointer, so S7-NEW-B Option A ("render real image per
#           §10-S10-7/S10-8") referenced helpers with no executable home — the
#           generator was never told HOW to lay figural problem/option images out
#           for one-question-per-screen rendering, nor what image-quality bar to
#           meet. FIX — encoded ENTIRELY in this file (no section_rules change; DPI
#           and display sizes are framework constants):
#             (1) §10-S10-7 IMAGE-QUALITY CONTRACT (now executable, replaces stub):
#                 vector-first geometry rasterised at FIGURAL_DPI=300 (lossless PNG,
#                 never JPEG, never upscaled from a small bitmap), uniform per-option
#                 SQUARE canvas, real reference-line geometry, NO question chrome
#                 (stem/caption/option-number) baked into any raster, mandatory
#                 view-tool verification. Constants: FIGURAL_DPI=300,
#                 FIG_OPT_DISPLAY_IN=1.3, FIG_PROBLEM_DISPLAY_IN=2.3,
#                 FIG_NATIVE_HEADROOM=2.0, FIG_MIN_STROKE_PT=1.4.
#                 [SUPERSEDED v5.33 — historical record of what v4.0 shipped.
#                  Live constants are in S10-7: FIG_PROBLEM_DISPLAY_IN=4.0 and
#                  FIG_NATIVE_HEADROOM=1.0 (retired). Do not read this as rule.]
#             (2) §10-S10-8 FIGURAL PLACEMENT (now executable) — add_figural_question():
#                 ONE image per visual unit (problem figure[s] separate; EACH option
#                 a separate image); options stacked SINGLE-COLUMN, one per line,
#                 each image bound 1:1 to its own "i." label; stem stays the Q.N-first
#                 document text (R14). NEVER a composite; NEVER two option images on
#                 one line or in one table row.
#             (3) S7-NEW-B Option A + S8-6 rewritten to call S10-7/S10-8 and carry
#                 the decomposition / no-composite / single-column mandate.
#             (4) new rule R-FIGURAL (HARD STOP): a figural MCQ MUST render as
#                 problem-image(s) + N discrete option-images bound 1:1 to labels,
#                 single-column, no composite panel, no in-image question text, all
#                 figures ≥300 DPI on uniform option canvases.
#             (5) new gate G-FIGURAL-COMPOSITE (S12-NEW-13, gate count 52 → 53):
#                 for every figural question the block must hold ≥ (n_options + 1)
#                 inline images, exactly one image per option line, and no paragraph
#                 carrying >1 image; a single-image figural block (composite) or any
#                 multi-image line → Exit 1. Wired into the self-audit script, the
#                 S4-11 per-batch checklist, §17 DoD, §18 glossary, §19 edge-cases.
#           Net: figural questions now decompose into crisp, uniform, 300-DPI
#           per-figure images, laid out one option per line and bound to their
#           labels — online-renderable and reference-grade. Generalises to every
#           exam and every figural format. No new dependency.
#   v4.1 — 2026-06-29 — UNDERLINE-SPAN RENDERING CONTRACT (formatting fix; gate
#           count 53 → 54). Fixes the M1 underline defect surfaced on the SSC CGL
#           T1 sample: every question that asks about an UNDERLINED span — Q.83
#           "improve the underlined part ... He is senior than me by three years"
#           and Q.78 "antonym of the underlined word ... benevolent" — shipped the
#           target span as a PLAIN-TEXT parenthetical annotation appended to the
#           stem ("(underlined: senior than me)", "(underlined: benevolent)")
#           instead of an actually underlined run. A whole-file run scan confirmed
#           ZERO <w:u> underline runs in the entire document: the underline rule
#           never executed once. ROOT CAUSE — the SAME stub anti-pattern that
#           produced the v3.5 (delivery), v3.6 (linked-stimulus) and v4.0 (figural)
#           failures: §10-S10-2 "Underline implementation (unchanged from v1.0)"
#           was a one-line stub ("run.underline = True. NEVER underscores.") that
#           (a) stated the GOAL but supplied NO executable helper to split a stem
#           into runs and underline only the target span; (b) never listed WHICH
#           question templates require a real underlined span; (c) never BANNED the
#           "(underlined: X)" annotation fallback. The only stem helper (S10-3
#           add_question_stem) writes the whole stem as ONE bold run with no
#           sub-span underline path, so a generator needing to underline a span had
#           no function to call and defaulted to the parenthetical note. Worse, the
#           render-consistency contract's stem_matches_format() for
#           'sentence_embedded_underlined' checked only that the target WORD appears
#           in the stem text — which the annotation satisfies — so the cosmetic form
#           PASSED. And unlike figural-as-text (caught by G-FIGTEXT), underline-as-
#           text had NO equivalent gate. Three safety layers (spec, helper, audit)
#           shared one hole. FIX — encoded ENTIRELY in this file (no section_rules
#           change; underline is a framework rendering primitive):
#             (1) §10-S10-2 UNDERLINE-SPAN CONTRACT (now executable, replaces stub):
#                 UNDERLINE_TRIGGER detector (stem references "the underlined
#                 word/part" OR stem_format_variant == 'sentence_embedded_underlined')
#                 + add_stem_with_underline(doc, qnum, pre, target, post) building
#                 the stem as three runs (pre | underlined target | post), w:u on the
#                 target run only, Calibri 11, bold per R13; explicit BAN on the
#                 "(underlined: …)"/"(underline: …)" annotation and on appending the
#                 target in brackets.
#             (2) render-consistency contract (G4) tightened: for
#                 'sentence_embedded_underlined', stem_matches_format() now requires a
#                 real underlined run (delegates to has_underlined_span), not mere
#                 textual presence of the word.
#             (3) new rule R-UNDERLINE (HARD STOP): any underline-class question MUST
#                 carry the target as a genuine underlined run inside the sentence;
#                 the parenthetical annotation is forbidden with the force of R5.
#             (4) new gate G-UNDERLINE (S12-NEW-14, gate count 53 → 54): for every
#                 block whose stem references an underlined element, Exit 1 if the
#                 block text contains "(underlined:"/"(underline:" OR no run in the
#                 block carries w:u. Wired into the self-audit script, the S4-11
#                 per-batch checklist, §17 DoD, §18 glossary.
#           Net: an underline-dependent question can never again ship with the span
#           faked as text — it must render as a true underlined run or the build
#           hard-stops. Generalises to every exam and every underline format.
#   v4.2 — 2026-06-29 — STEM↔OPTION CONSISTENCY + ANSWER-UNIQUENESS (deep-audit
#           of SSC CGL T1 Mock 1; gate count 54 → 56). A per-question audit of all
#           100 Mock-1 questions found the paper logically/factually sound but
#           surfaced two CLASSES of latent defect — both EXAM-AGNOSTIC (no exam
#           content is hardcoded; the new checks read structure from section_rules):
#
#           (A) STEM↔OPTION REFERENCE MISMATCH (Q.100). The error-spotting stem
#               promised an escape — "If there is no error, select the last option" —
#               but the option set was four sentence SEGMENTS with NO "No error"
#               option; option 4 was itself the error-bearing segment. A 4-segment
#               "pick the error" layout was fused with a 3-segments+"No error"
#               instruction. ROOT CAUSE: the framework READS none_of_above_permitted
#               (S3-12) and wrong_option_structure.type==fixed_set (S3-13) from
#               section_rules but NOTHING enforced them — there was no check that an
#               instruction REFERENCING a terminal/escape option ("if no error…last
#               option", "select 'No improvement'", "None of these", "All of the
#               above", "Both…and…", "Neither…nor…") actually PRODUCED that option,
#               correctly positioned, and that the promised option-structure matched
#               the rendered options. The same stem also ran the instruction and the
#               carrier sentence together on one line (no break). FIX:
#                 (1) new rule R-OPTREF (HARD STOP): a stem may not reference a
#                     terminal/escape option the option set does not contain, and a
#                     "no error/no improvement → last option" instruction REQUIRES a
#                     final escape option; the instruction's option-structure must
#                     match the rendered options. Exam-agnostic — the permitted
#                     escape tokens come from none_of_above_permitted /
#                     wrong_option_structure in section_rules.
#                 (2) new gate G-OPTREF (S12-NEW-15, gate count 54 → 55): regex-detect
#                     the escape-reference patterns; if referenced, the option must be
#                     present (and at the stated position); if a "pick the segment"
#                     layout carries a "no error" escape instruction without the
#                     escape option → Exit 1.
#                 (3) §10-S10-2 carrier-sentence two-paragraph layout (added for
#                     underline in v4.1) GENERALISED to every carrier-sentence stem
#                     (error-spotting, sentence-improvement, fill-in-sentence): the
#                     instruction is line 1, the sentence is its own paragraph — fixes
#                     the Q.100 run-on universally.
#
#           (B) NON-UNIQUE ANSWER (Q.3, Q.98). Two questions admitted a SECOND
#               defensible option: Q.3 "daughter of the only son of my grandmother"
#               → Sister (paternal reading) OR Cousin (maternal reading), both listed;
#               Q.98 reported speech of a universal truth → "is" (tense retained) OR
#               "was" (back-shifted), both listed. ROOT CAUSE: the framework had NO
#               answer-uniqueness check anywhere — dedup/presentation gates ensure
#               questions don't REPEAT, but nothing ensured each has EXACTLY ONE
#               defensible answer. Full mechanisation is impossible (verbal ambiguity
#               needs reasoning, not regex), so the fix is a GENERATION-TIME contract,
#               modelled on the v3.9 render-consistency CHECK 3:
#                 (4) new rule R-UNIQUE (HARD STOP at generation): every question has
#                     exactly one defensible correct option; the other three are
#                     indefensible under ANY reasonable reading. Stated as a universal
#                     principle with illustrative CLASSES (unqualified kinship +
#                     "only" → maternal/paternal split; contested grammar conventions
#                     presented as two option forms) — NO exam-specific content baked.
#                 (5) verify_answer_uniqueness(candidate) added to CHECK 3
#                     (passes_quality_gates): the generator, which already knows the
#                     intended key, must confirm no second option is defensible; if one
#                     is, REJECT and regenerate with the stem disambiguated. The
#                     per-Q result is persisted as answer_uniqueness_verified in the
#                     concept_map sidecar (S7-NEW-A).
#                 (6) new gate G-UNIQUE (S12-NEW-16, gate count 55 → 56): a
#                     record-presence gate (like G-CONCEPTDUP reads concept_map) — any
#                     question whose sidecar lacks answer_uniqueness_verified == true →
#                     Exit 1 (generation skipped the contract; fix the generator, do
#                     not silently pass).
#           Wired into the self-audit script, S4-11 per-batch checklist (23 → 25
#           items), §17 DoD, §18 glossary. Net: a question can no longer ship
#           referencing an option it doesn't have, nor with two defensible answers.
#           Generalises to every exam; all structure read from section_rules.
#   v4.3 — 2026-06-29 — MATH-AS-OMML ROUTING CONTRACT (math-raster fix; gate
#           count 56 → 57). Fixes the M1 Q.55 defect surfaced on the SSC CGL T1
#           sample: the two algebraic expressions in the stem — "x + 1/x = 5" and
#           "x² + 1/x²" — shipped as PNG raster images (q55_e1.png, q55_e2.png),
#           NOT as native OMML. Forensics: both PNGs carry metadata
#           Software=Matplotlib 3.10.8 at EXACTLY 300 DPI — i.e. the algebra was
#           pushed through the FIGURAL raster pipeline (render_figural_image,
#           FIGURAL_DPI=300) instead of the OMML math path. Both expressions are
#           the textbook cases S10-4's decision tree marks MANDATORY OMML: "1/x"
#           and "1/x²" are stacked fractions (rule 3) and "x²+1/x²" is exponent+
#           fraction (rule 5). ROOT CAUSE — the SAME stub/enforcement anti-pattern
#           behind v3.5/v3.6/v4.0/v4.1: §10-S10-4 STATED the goal ("MANDATORY
#           OMML") but supplied (a) NO executable entry point that intercepts a
#           math-bearing stem/option and forces it to OMML — the only stem helper
#           (S10-3 add_question_stem) writes the whole stem as one text run, so a
#           generator with a math expression had no add_math_stem() to call and
#           fell back to rasterising it; (b) NO boundary stopping the figural
#           pipeline from accepting an algebraic string — render_figural_image()
#           rendered whatever draw_fn it was handed, including mathtext; (c) NO
#           rule with R5-force banning math-as-raster; and (d) the only math gate,
#           G-FRAC, scans the TEXT stream for "a/b" slash fractions — it is blind
#           to a fraction that has become a <w:drawing>, so the defect sailed
#           through audit. Four safety layers (spec, helper, boundary, gate) all
#           had the one hole: math could be rasterised and nothing said no. FIX —
#           encoded ENTIRELY in this file (OMML + figural-naming are framework
#           primitives; no section_rules change):
#             (1) §10-S10-4 MATH-AS-OMML ROUTING CONTRACT (rewritten): adds RULE 0
#                 to the decision tree — "math is NEVER rasterised; the matplotlib/
#                 figural/image path is BANNED for any algebraic/symbolic
#                 expression" — and the executable home that was missing:
#                 MATH_TRIGGER_RE (detects stacked fraction / exponent / radical /
#                 built-up structure in any stem or option), add_math_stem(doc,
#                 qnum, segments) + emit_math_inline(p, expr_ast) that realise the
#                 expression as <m:oMath> runs interleaved with text, and
#                 assert_not_math(label) — the guard the figural path now calls.
#                 States the boundary explicitly: the figural raster pipeline is
#                 for GEOMETRIC FIGURES ONLY (mensuration/coordinate diagrams,
#                 reasoning figures); algebraic/symbolic math always goes to OMML.
#             (2) §10-S10-7 FIGURAL math-exclusion GUARD: render_figural_image()
#                 now calls assert_not_math() on its draw target / label and
#                 HARD-STOPS if handed an algebraic expression — making the Q.55
#                 mis-route mechanically impossible. Also FORMALISES the canonical
#                 figural image-naming convention already in de-facto use
#                 (q{N}_problem[_k] / q{N}_opt{i} / q{N}_stim[_*]) so the only
#                 inline rasters in any paper are figures and stimuli.
#             (3) §10-S10-8 add_figural_question() MANDATES that canonical naming
#                 on every emitted figure (problem/opt/stim prefixes), so the gate's
#                 name-contract is always satisfiable by legitimate figures.
#             (4) new rule R-MATH-OMML (HARD STOP): every algebraic/symbolic
#                 expression containing a stacked fraction, exponent, radical, or
#                 built-up structure MUST render as native OMML (<m:oMath>), never
#                 as a raster image and never as slash/caret ASCII. The figural
#                 raster pipeline is geometry-only. Banned with the force of R5.
#             (5) new gate G-MATH-RASTER (S12-NEW-17, gate count 56 → 57): scans
#                 every inline <w:drawing>; an image whose pic name does NOT match
#                 the canonical figural/stimulus pattern ^q\d+_(problem|opt\d+|stim)
#                 is an UNAUTHORISED raster → Exit 1 (the prime case being a
#                 rasterised expression like q55_e1.png). The signal is the IMAGE
#                 name-contract — provenance-proof: it cannot be defeated by faking
#                 a figural-manifest entry, and it cannot false-positive on a real
#                 figure (which is named by the §10-S10-8 convention). Math-context
#                 stem detection + math image-name tokens are reported as
#                 corroborating diagnostics. VALIDATED in Python against the actual
#                 failing file: flags Q.55's two rasters and ZERO of the six genuine
#                 figural questions (Q.3/10/12/16/22 mirror/fold/embedded + Q.19
#                 count-triangles); passes a real-OMML control; survives a faked-
#                 manifest attack.
#           Wired into the self-audit script, S4-11 per-batch checklist (25 → 26
#           items), §17 DoD, §18 glossary, and the §12 guard script. Net: an
#           algebraic expression can never again ship as an image — it renders as
#           OMML or the build hard-stops, and a stray math raster is caught at
#           audit. Generalises to every exam and every math format. Also corrects
#           two stale "52 gates" references in §17 DoD (→ 57). No new dependency.
#   v4.4 — 2026-06-30 — ALTERNATION/ROTATION MANIFEST MIGRATION (completes the
#           v3.4 migration; gate count unchanged 57). Fixes the SSC CGL T1 Mock 1
#           HARD STOP at generation start: M1's QA allocated BOTH Simple Interest
#           and Compound Interest; S6-9's hardcoded CI/SI block fired an explicit
#           HARD STOP, while S3-17 — the gate that v3.4 made the manifest-driven
#           OWNER of this exact check — passed (manifest.alternation_groups empty,
#           so vacuously). ROOT CAUSE: v3.4 rewrote S3-17 to read mandates/
#           alternation from the Step-0 manifest by subtopic_id and deleted all
#           hardcoded subtopic names — but migrated ONLY S3-17. Its sibling
#           enforcers of the SAME policy were left hardcoded with SSC-CGL names:
#           (a) S6-9 (generation-time rotation tracking) — a hardcoded GIR-pair
#           table (Calendar Day↔Roll Number, …), a hardcoded CI/SI HARD STOP, and
#           named Coding-Decoding / Blood-Relations / Number-Series rotation blocks;
#           (b) S12-NEW-6 G-CISINCHECK (post-gen audit) — hardcoded "Simple
#           Interest"/"Compound Interest" string-match; (c) S7-24 — a duplicate
#           hardcoded "CI/SI ALTERNATION" + "PARTNERSHIP/MIXTURE ALTERNATION"
#           restatement. Three+ enforcers thus disagreed on the SAME input, and all
#           three violated the prime directive (zero exam content in core files).
#           Note also that the config layer only ever supported MUTUAL EXCLUSION
#           (manifest.alternation_groups = "members must not co-occur in one mock");
#           S6-9's "reads schedule from section_rules.md" parity table had NO
#           backing data anywhere — a hollow claim. FIX — encoded ENTIRELY in this
#           file; all hardcoded subtopic names stripped; mirrors S3-17's "empty
#           config ⇒ vacuous no-op, never a false stop":
#             (1) S6-9 REWRITTEN exam-agnostic. The MUTUAL-EXCLUSION invariant is
#                 owned solely by S3-17 (manifest.alternation_groups, pre-gen) —
#                 S6-9 no longer duplicates it and carries NO pair list and NO
#                 hardcoded HARD STOP. Cross-mock VARIANT rotation (cipher/sub-type/
#                 series-variant non-repetition) is now read from an OPTIONAL
#                 per-subtopic `ROTATION:` cycle in section_rules.md, keyed by
#                 subtopic_id (rotation_pick(): next variant ≠ previous mock's,
#                 persisted in rotation_state). A subtopic that declares no cycle ⇒
#                 no constraint (no-op). Zero subtopic names in the framework.
#             (2) S12-NEW-6 G-CISINCHECK GENERALISED in place to G-ALTGROUP (same
#                 gate slot; count stays 57): reads manifest.alternation_groups and
#                 Exit 1 if any group has ≥2 members present in the mock — the
#                 exam-agnostic post-gen backstop to S3-17. Empty config ⇒ pass.
#                 No hardcoded names. (Gate renamed everywhere: §12 catalogue, §18
#                 glossary, the "through G-CISINCHECK" audit-script contract.)
#             (3) S7-24 duplicate "CI/SI ALTERNATION" + "PARTNERSHIP/MIXTURE
#                 ALTERNATION" lines REMOVED; replaced by a pointer to
#                 manifest.alternation_groups + S3-17 + G-ALTGROUP. No pairs here.
#             (4) GAP-20 cross-ref updated (S6-9 → manifest-driven; mutual exclusion
#                 owned by S3-17/G-ALTGROUP).
#           VALIDATED in Python before encoding against the real M1 state: the old
#           S6-9 reproduces the HARD STOP; the new logic PASSES M1 with the empty
#           manifest (unblocks generation), still HARD-STOPs once a ci_si group is
#           minted with both members present, PASSES when only one member is
#           present, and catches an unrelated exam's group with ZERO code change.
#           Net: M1 unblocks today; the alternation policy becomes pure Step-0 data
#           (set alternation_group on both members → manifest mints the group → all
#           three enforcers agree) with no further framework edit; a future exam can
#           never again have two gates disagree on the same input.
#           OUT OF SCOPE / NEXT ISSUE (flagged, NOT edited here): S7-24 and S7-31
#           still hardcode MANDATORY-PRESENCE subtopic names (Mensuration 3D,
#           Direction Sense, Address Matching, Coordinate Geometry, the named
#           cipher ban) restating a policy already owned by manifest.
#           mandatory_every_mock + S3-17. That is a separate presence-mandate
#           migration, to be done as its own scoped pass.
#
#   v5.4 — 2026-07-03 — DEEP-AUDIT BUG SWEEP (11 bugs found, all fixed; 2 CRITICAL).
#           A line-by-line review of every code block, variable reference, schema
#           definition, version stamp, and cross-section pointer in this 6000-line spec
#           found 11 bugs spanning runtime failures, silent data corruption, and
#           documentation drift. ALL fixed in this version:
#             (1) CRITICAL — sr_text/section_rules_text variable name collision (S3-14):
#                 msq_allow_aota regex searched a variable 'section_rules_text' that was
#                 never defined — the variable is 'sr_text' (S3-2). The try/except
#                 NameError silently defaulted _aota=False, so msq_allow_aota was ALWAYS
#                 IGNORED even when section_rules explicitly set it true. Any MSQ exam
#                 permitting AOTA had legitimate AOTA options rejected by G-MSQ-SET.
#                 FIXED: references sr_text; removed the masking try/except.
#             (2) CRITICAL — S11-5 K-INT verification crashes on MSQ/NAT answers: the
#                 loop asserted `1 <= val <= options_count` on EVERY answer, but v4.5
#                 made MSQ answers list[int] and v4.7 made NAT answers string/float.
#                 `1 <= [1,3] <= 4` TypeError; `1 <= '47' <= 4` wrong comparison. Never
#                 updated for the multi-type answer model.
#                 FIXED: branches by answer_type/answer_cardinality from concept_map.
#             (3) batch_state.json init (S3-16) missing concept_ledger and
#                 presentation_ledger — present in the S4-3 schema and in S4-8a writes,
#                 but never initialised at creation. Didn't crash (dict assignment creates
#                 keys, and resume uses .get() with defaults) but the on-disk file was
#                 schema-incomplete at session start.
#                 FIXED: both fields added to the S3-16 init block.
#             (4) Footer version said v5.1, header said v5.3; footer date 2026-07-01 vs
#                 actual v5.3 date 2026-07-02. FIXED: footer now v5.4 / 2026-07-03.
#             (5) Footer gate count said 65; §12/§17/§18 all say 66. The v5.3 gate-count
#                 reconciliation pass missed its own footer line.
#                 FIXED: footer now 66.
#             (6) §17 DoD referenced "S13-7 pre-delivery 6-point checklist" but S13-7
#                 has 7 items (item 7 = G-QINDEX, added in v5.2).
#                 FIXED: "7-point".
#             (7) SUPPORTED_VERSIONS stale allow-list ['1.6', '1.7'] — any blueprint >=
#                 v1.8 triggered a WARN even though it's fully compatible. Replaced with a
#                 minimum-version floor check (>= 1.7). A blueprint below the floor now
#                 HARD STOPs (the subtopic_id contract is non-negotiable).
#             (8) 'bp' in dir() guards (S3-14, 5 occurrences) — bp is ALWAYS loaded at
#                 S3-2 before S3-14 runs, so the guard was cosmetic. If the code were ever
#                 refactored into a function, bp would be out of scope and the guard would
#                 silently fall back to wrong defaults. FIXED: direct bp access (safe).
#             (9) Appendix A bootstrap instruction said 'SELF-TEST: 45/45 PASS' — gate
#                 count is 66. FIXED: 66/66.
#            (10) S4-11 manual gate checklist said "All 26 items" but actually has 28
#                 (G-GROUPMANDATE + G-MINCOUNT added in v5.0 without bumping the count).
#                 FIXED: 28.
#           No new gates, no new rules, no rendered-byte change. Pure correctness.
#   v5.5 — 2026-07-04 — DEEP-AUDIT BUG SWEEP #2 (7 bugs found, all fixed; 1 CRITICAL).
#           A complete 6057-line read + cross-file contract verification found 7 bugs:
#             (1) CRITICAL — S11-5 `options_count` undefined in code block: the K-INT
#                 verification referenced `options_count` but it was never defined within
#                 the S11-5 code block. Any runtime call would NameError on the MSQ/MCQ
#                 branches. FIXED: derives options_count from kd.msq_meta.total_options.
#             (2) HIGH — S7-24 / S7-31 stale "Issue 2b not yet enforced" prose: the text
#                 said GROUP-PRESENCE and MIN-COUNT "cannot be expressed" and "Until 2b
#                 lands they remain Step-1 allocation concerns" — but v5.0 ALREADY
#                 implemented Issue 2b (S3-17 CHECK 3/4, G-GROUPMANDATE, G-MINCOUNT).
#                 FIXED: rewritten to accurately describe the v5.0 enforcement reality.
#             (3) HIGH — Missing §3 section header: S3-1..S3-19 (pre-generation checks)
#                 had no parent section header, breaking §3 cross-references and the
#                 validator's section accounting. FIXED: added §3 header.
#             (4) MEDIUM — S13-9 handoff message used old step numbers: "Step 4
#                 (MockExplain)" and "Step 3 (MockCreateAudit)" instead of canonical
#                 Step 9 / Step 8. FIXED.
#             (5) MEDIUM — S3-3 SSC-specific MANDATE numbering: "MANDATE-8 equivalent
#                 block" / "MANDATE-9 equivalent block" are SSC-specific mandate numbers
#                 baked into an exam-agnostic spec (prime-directive violation). A GATE
#                 exam wouldn't number mandates 8/9. FIXED: replaced with generic
#                 directive-block descriptions. Same fix in §17 DoD.
#             (6) MEDIUM — Appendix A MVP script version string stale: said "v4.2
#                 MockCreate Framework" and "Full 45+-gate script" when the framework
#                 is at v5.5 with 66 gates. FIXED.
#             (7) MEDIUM — Appendix A MVP K-BAL crashes on MSQ/NAT: `counts[v]` where
#                 v is a list (MSQ) raises TypeError; a float (NAT) silently miscounts.
#                 FIXED: skips MSQ/NAT answers in K-BAL (single-mode only).
#           No new gates, no new rules. Pure correctness.
#   v5.13 — 2026-07-07 — FIGURAL EXECUTION GUARDRAILS + STEM-ONLY RENDERING PATH.
#           (10 changes: 6 execution hardening + 4 architectural for 200-exam coverage)
#
#           ROOT CAUSE: a production mock shipped figural questions as text descriptions
#           despite S7-NEW-B, R-FIGURAL, G-FIGTEXT, and G-FIGURAL-COMPOSITE all being
#           present. Two defect classes: (A) format=FIGURAL execution skip (rules existed,
#           execution ignored them); (D) stem_only FIGURAL MCQ with no valid rendering
#           path (no helper, no gate config, no dispatch path existed in the framework).
#
#           CHANGES 1–6 (execution hardening, 0 new rules):
#             (1) S3-18 FIGURAL MANIFEST in session summary — lists every figural Q
#                 by batch/number/subtopic so Claude sees the full scope upfront.
#             (2) S4-5 CHECK 5 per-batch figural format scan — prints reminder when
#                 the current batch contains format=FIGURAL subtopics.
#             (3) S3-16 batch_state.json gains figural_qs{} tracking (rendered flag).
#             (4) S4-7 STEP A FORMAT DISPATCH (3-way: stem_and_options / stem_only / TEXT).
#             (5) G-FIGTEXT expanded (v5.13): primary image-count per format=FIGURAL
#                 subtopic (0 images → Exit 1) + secondary regex + tertiary visual-prose
#                 detector (figure-reference text + 0 images in ANY format block).
#             (6) HS-15 figural_present mismatch WARN.
#
#           CHANGE 7 (new rendering path — fills architectural gap):
#             add_figural_stem_question() helper for format=FIGURAL + image_role=stem_only
#             MCQ (problem PNG + text options). G-FIGURAL-COMPOSITE gains image_role-aware
#             arms: stem_only (imgs ≥ 1, option-image arm skipped), options_only (imgs ≥
#             n_opt, no problem image required). FORMAT DISPATCH expanded to 3-way using
#             PYQ_IMAGE_ANALYSIS.image_role from section_rules.
#
#           CHANGE 9 (gate — content-based backstop):
#             G-FIGTEXT-PROSE tertiary: any Q-block with 0 images + figure-reference text
#             → Exit 1. Catches misclassified TEXT blocks and bypassed FIGURAL blocks.
#
#           CHANGE 10a/b/c (hardening):
#             (a) HS-15a reverse (figural_present=False + FIGURAL subtopics exist)
#             (b) HS-16 FIGURAL_BANNED ↔ REPLACEMENT_RULE consistency gate (HARD STOP)
#             (c) G-FIGTEXT-DEPS dependency fallback (WARN or FAIL in --final mode)
#
#           Gate count: 66 (unchanged — G-FIGTEXT and G-FIGURAL-COMPOSITE gain sub-arms,
#           not new gate IDs). New helper: add_figural_stem_question (§10-S10-8A).
#           New hard stops: HS-15, HS-15a (WARN), HS-16.
#
#   v5.12 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S13-9A: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. Per-batch (F1 mid-step with cumulative
#           Q1to[K].docx) and Final Assembly (F2 step-complete with Create.docx +
#           registry.json) now render the standardized visual footer. Zero logic change.
#   v5.11 — 2026-07-06 — AUDIT SCRIPT SOURCE-OF-TRUTH MIGRATION (EC-A1, EC-A2).
#           Step 6 v1.20 now auto-generates [ExamCode]_mock_test_audit.py as its
#           6th output file. This Step 7 spec no longer owns the script template.
#
#           (1) EC-A1 — APPENDIX A CONVERTED TO POINTER: Appendix A header and
#               post-script instructions updated to direct users to Step 6 output.
#               The AUDIT_SCRIPT_CONTENT code block is RETAINED (unchanged) as the
#               transitional source that Step 6 §13-7A reads at B3 runtime.
#               When Step 6's next version embeds the code directly, this block
#               becomes dead code and can be removed.
#
#           (2) EC-A2 — ABSENCE WARNING UPDATED: The "IS mock_test_audit.py REQUIRED?"
#               section and S3-9 absence message now reference Step 6 auto-generation.
#               "HOW TO CREATE" instructions replaced with "auto-generated by Step 6;
#               if missing, verify Step 6 outputs were uploaded."
#
#           No generation logic, gate, or mandate change. Self-test count unchanged.
#
#   v5.10 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (marking_scheme + level + medium).
#           Step 2a v2.5 and Step 6 v1.19 now carry marking_scheme[], level, and medium
#           in blueprint.json. Step 7 reads these new fields for:
#             (1) marking_scheme: per-Q-position marks and question-type lookup. Builds
#                 _marks_for_q(qnum) and _type_for_q(qnum) helpers. Enables accurate
#                 difficulty calibration per Q (a 4-mark Part C question gets higher
#                 difficulty threshold than a 2-mark Part A question in CSIR NET).
#             (2) level: academic-level calibration for question complexity (PG = deeper
#                 multi-step reasoning, Grad = moderate, School = factual recall).
#             (3) medium: authoritative language source (supplements section_rules language).
#           All fields have safe defaults for legacy blueprints (empty list / "unknown").
#           No generation logic changes — new fields are READ and AVAILABLE for calibration.
#
#   v5.9 — 2026-07-04 — TITLE/FILENAME ALIGNMENT + RESIDUAL STEP-NUMBER FIX + SCHEMA FIX.
#           (1) TITLE/FILENAME MISMATCH: header, §1 spec reference, Appendix A reference,
#               and footer all said "Framework_MockCreate" but the filename is
#               Framework_MockTestCreate.md (missing "Test"). FIXED: all 5 now match.
#               Step name "MockCreate" and trigger format UNCHANGED (canonical step name).
#           (2) 33 RESIDUAL OLD STEP NUMBERS: v5.8 claimed canonical alignment but missed
#               33 body references — 20× "Step 2" (→ Step 7, this step) and 13× "Step 3"
#               (→ Step 8, MockCreateAudit). FIXED: all now canonical. VH preserved.
#           (3) Cross-reference "Framework_MockCreateAudit.md" → "Framework_MockTestCreateAudit.md"
#               (Step 8's title was fixed in v2.0).
#           (4) REQUIRED_TOP MISSING 3 FIELDS: section_names, rc_manifests, figural_manifests
#               were written at S13 but not in REQUIRED_TOP for schema self-heal. A stale
#               registry missing these fields would not be healed until Step 8 (whose
#               REQUIRED_TOP already covers them). FIXED: added to REQUIRED_TOP.
#           Cross-step sync verified: Step 8 v2.0, Step 9 v1.9, Step 11 v1.0. No logic
#           change; all gate counts unchanged.
#   v5.8 — 2026-07-04 — 8-LAYER DEEP AUDIT (gate completeness + schema gaps fixed).
#           An automated 8-layer deep-audit script (Python lint, regex compilation,
#           cross-reference graph, gate completeness, rule→gate mapping, edge-case
#           simulation, schema contract, font consistency) found 2 real gap classes:
#             (1) S4-11 MANUAL CHECKLIST INCOMPLETE: 11 gates were defined in §12 and
#                 enforced at generation/Final Assembly but missing from the per-batch
#                 manual checklist (S4-11): G-ALTGROUP, G-ALLOC-SUBTOPIC,
#                 G-COUNT-X-UNIQUE, G-FIGTEXT, G-MSQ-SET, G-MSQ-CARD, G-MSQ-INSTR,
#                 G-NAT-NOOPT, G-NAT-ANSWER, G-NAT-INSTR. MSQ/NAT gates carry dormancy
#                 notes. Checklist count 28 → 38. (G-DELIVERY-SET and G-QINDEX are
#                 Final-Assembly-only and are correctly absent from the per-batch list.)
#             (2) §14 SCHEMA MISSING 2 FIELDS: options_by_q (v4.7, per-question expected
#                 option count, consumed by Step 9) and section_names (v4.8, consumed by
#                 G-SECTIONHDR and Step 8 A-SECHDR) were written to the registry by
#                 S13-REGCHECK but never documented in §14. FIXED: both now documented
#                 with their version, write-source, and consumer.
#           No new gates, no new rules. Pure completeness/documentation fixes.
#   v5.7 — 2026-07-04 — FINAL EXHAUSTIVE PASS (2 runtime bugs found, both fixed).
#           A line-by-line re-read of all 6216 lines with automated variable-scope,
#           function-definition, and edge-case checks found two bugs:
#             (1) CRITICAL — note() called but never defined (S3-13 K-BAL degradation
#                 path, line in build_answer_budget): when a NAT/MSQ-heavy exam triggers
#                 the degraded K-BAL path (n_free < 4·options_count), the code calls
#                 note() which is not a Python builtin and is never defined in this file.
#                 This would crash with NameError on any GATE/CAT-class paper with heavy
#                 NAT+MSQ exclusion. FIXED: replaced with print() (standard, always
#                 available, and consistent with all other diagnostic output in the spec).
#             (2) CRITICAL — String comparison of blueprint version numbers (S3-7):
#                 `blueprint_version < MIN_BLUEPRINT_VERSION` used Python string
#                 comparison. Works for "1.6" < "1.7" (True) but FAILS for "1.10" < "1.7"
#                 (True in string sort — '1' < '7' character-by-character) and would
#                 falsely reject blueprint v1.10+. FIXED: _ver_tuple() parses version
#                 strings into integer tuples; comparison is now (1,10) > (1,7) = True.
#           No new gates, no new rules. Pure runtime-safety fixes.
#   v5.6 — 2026-07-04 — EXAM-AGNOSTICISM SWEEP (9 rigidity issues fixed; 2 CRITICAL).
#           A whole-file audit for any value, name, format, or constant that would
#           fail or produce wrong output for a non-SSC exam found 9 issues. ALL fixed:
#             (1) CRITICAL — Font hardcoded as Calibri 11pt: every helper, every gate,
#                 every checklist item used the literal "Calibri" / Pt(11). A GATE exam
#                 requiring Times New Roman 12pt or a Hindi exam needing Noto Sans
#                 Devanagari would get wrong font. FIXED: FONT_NAME and FONT_SIZE_PT
#                 read from exam_config.json / blueprint (S3-2); defaults Calibri 11.
#                 All 14 helpers + 4 gates + 3 checklists use the variables. FONT_BANNED
#                 (default {Arial}) auto-excludes the configured font.
#             (2) CRITICAL — Option label "1.  text" hardcoded: R10 said "read
#                 option_label_format from section_rules" but add_text_options() and
#                 G-OPTLABEL hardcoded the "N.  " format. Exams using (a)/(A)/(i)/1)
#                 would fail. FIXED: OPTION_LABEL_FMT read from config (default
#                 "{i}.  {text}"); OPTION_LABEL_RE built dynamically for the gate.
#             (3) HIGH — S3-3 SSC-specific directive block names: "GA easy-ban types",
#                 "QA mandatory topics", "English cluster bans" assume SSC's 4-section
#                 structure. A GATE exam has different sections. FIXED: generic
#                 "per-section content-ban/mandatory-area/cluster-ban directives".
#             (4) HIGH — §17 DoD "GA areas" / "GA/CA facts": SSC-specific. FIXED:
#                 "per-section mandatory areas" / "fact-recall questions: source citations".
#             (5) HIGH — DI table NAVY color "1F4E79" hardcoded: now DI_HEADER_COLOR
#                 read from exam_config (default "1F4E79").
#             (6) MEDIUM — batch_state schema example used "GIR"/"ENG": FIXED: generic
#                 "Section_A"/"Section_D".
#             (7) MEDIUM — SC-3 examples used SSC Q numbers as if universal: FIXED:
#                 added "(illustrative, using SSC CGL T1 reference Q numbers)" note.
#             (8) MEDIUM — Appendix A MVP hardcoded N_OPT=4: FIXED: reads from
#                 sidecar msq_meta.total_options (default 4).
#             (9) LOW — S11-3 "NCERT/Constitution/official URL": India-specific. FIXED:
#                 "authoritative academic, government, or official sources".
#           CROSS-STEP SYNC (found in second-pass verification against Step 8 v1.7):
#             (10) CRITICAL — font/label CONFIG SOURCE MISMATCH: Step 7 v5.6 initial
#                 edit read font_name and option_label_format from exam_config.json /
#                 blueprint, but Step 8 reads font_family and option_label_format from
#                 SECTION_RULES.MD (via cat_c). This meant Steps 7 and 8 could use
#                 DIFFERENT fonts/labels for the same exam. FIXED: Step 7 now reads
#                 from section_rules FIRST (matching Step 8's contract), with
#                 exam_config as an OVERRIDE. Helper _sr_field() reads the same
#                 Category-A fields Step 8's cat_c reads. section_rules '1/2/3/4'
#                 notation auto-converted to the '{i}.  {text}' template.
#             (11) add_text_options _option_label() helper: handles numeric, alpha_upper,
#                 alpha_lower label schemes (not just numeric '{i}').
#           No new gates, no new rules. Pure exam-agnostic compliance.
#   v5.3 — 2026-07-02 — GATE-COUNT RECONCILIATION (documentation-only; no gate logic changed).
#           An authoritative enumeration replaced the drifted, mutually-inconsistent tallies the
#           spec carried (§12 header "39", §12 NAT summary "60", §17 DoD "63" and "65", §18
#           "57", S13-2 "56"). GROUND TRUTH: the S12-NEW series is contiguous S12-NEW-1..26 (twenty-six
#           and G-DELIVERY-SET is a 27th named gate that never received an S12-NEW number, so 27
#           gates have been added on top of the documented 39-gate v1.0 baseline = 66 total. (The
#           per-edit breadcrumbs stopped at 63 because they missed the two Issue-2b gates added
#           after the NAT entry and my own v5.2 add; 39+27 is corroborated by the §17 "65" being
#           correct after Issue-2b, plus G-QINDEX.) Every LIVE total now reads 66 (§12 header,
#           §12 summary, §17 DoD x2, §18 header, S13-2 sweep); historical changelog breadcrumbs
#           are left as the dated record. The enumeration also exposed two real omissions, now
#           fixed: the three DOUBT-3 gates (G-CONCEPTDUP/G-ALLOC-SUBTOPIC/G-COUNT-X-UNIQUE,
#           S12-NEW-7/8/9) were missing from the §18 table and are now tabled. A new linter check
#           F-GATECOUNT enforces that all live total statements in a spec agree (no hardcoded
#           number), so this drift cannot silently recur.
#   v5.2 — 2026-07-02 — QUESTION METADATA INDEX — PRODUCER LAYER (cross-step index extension,
#           Step-2 half; adds 1 gate: G-QINDEX). Exam-agnostic; writes NOTHING to the docx, so
#           the questions-only invariant and every existing gate are untouched. (1) write_q_to_sidecar
#           (S7-NEW-A) gains subtopic_id + difficulty params, recorded in the per-Q concept_map.
#           (2) SCHEDULE-FIRST difficulty assignment: the difficulty_schedule counts are the QUOTA;
#           each question's canonical label (blueprint.difficulty_labels; alias simple->Easy/
#           medium->Medium/hard->Hard) is captured per question — so the distribution matches the
#           schedule by construction. (3) S13-4 builds ONE mock object {mock, questions:[{q,
#           subtopic_id, difficulty}]} from the concept_map and appends it (replace-by-key) to the
#           Step-1-seeded registry.question_index; first-mock init + S13-REGCHECK REQUIRED_TOP now
#           include question_index (self-heal). (4) NEW gate G-QINDEX (S12-NEW-26; executable home
#           S13-QINDEX after S13-REGCHECK) — six HARD-STOP checks (existence/count/q-set/id-in-
#           blueprint/difficulty-vocabulary/exact-distribution), proven in the Phase-1 harness.
#           (5) S13-7 pre-delivery checklist extended 6->7 (adds QINDEX_OK). (6) §14 S14-1 lists
#           question_index. subtopic_id here is Step-2's assignment; Step 3 independently
#           re-derives + certifies it (difficulty is authoritative-by-assignment + distribution-
#           verified — not re-derivable from the paper). Governed by Contract_QuestionMetadataIndex
#           v1.0. NOTE (pre-existing, NOT introduced here): the spec's gate-count tallies already
#           disagree across sections (§12 header "39" / §12 NAT summary "60" / §17 DoD "63" and
#           "65" / §18 "57"); this change adds exactly one gate (G-QINDEX) but does NOT reconcile
#           those absolute totals — flagged for a dedicated count-audit pass rather than guessed.
#   v5.1 — 2026-07-01 — EXAM-AGNOSTICISM: removed the hardcoded "14" GA-areas count (same
#           prime-directive class as v4.9's 2a strip). Two prose sites asserted a fixed count
#           of mandatory General-Awareness areas — an SSC-specific value baked into an
#           exam-agnostic spec (a 6-section GATE/NEET paper has a different count, or none).
#           The framework already SOURCES these areas "from the MANDATE-9 equivalent block" in
#           section_rules; only the literal count was wrong to fix. FIX: S3-3 extraction line
#           and the §17 DoD item now read "ALL mandatory GA areas as declared in section_rules"
#           — count is data, never hardcoded. No gate/rule/logic change; empty ⇒ vacuous.
#   v5.0 — 2026-07-01 — ISSUE 2b — VERIFICATION LAYER for the two PER-MOCK mandate types
#           (group-presence + min-count). Step 0 v2.11 publishes mandatory_groups / min_counts
#           / cadence_windows; Step 1 v1.11 places them (RULE M4/M5/M6). Step 2 now VERIFIES
#           the two that are observable from a single mock:
#             • S3-17 gains CHECK 3 (mandatory_groups: >=min members present, HS-13) and
#               CHECK 4 (min_counts: id has >=k questions, HS-14), pre-generation on the
#               blueprint — reads structured manifest data by id, zero names hardcoded.
#             • Two post-gen backstops added, mirroring G-ALTGROUP↔S3-17: G-GROUPMANDATE
#               (S12-NEW-24) and G-MINCOUNT (S12-NEW-25), which re-check the GENERATED paper's
#               per-subtopic_id counts (the same concept_map counts G-ALLOC-SUBTOPIC uses).
#           DELIBERATE ASYMMETRY: cadence_windows is NOT gated in Step 2. Cadence is a
#           CROSS-mock constraint (">=1 every N mocks") and is structurally unobservable from
#           one mock; a Step 2 cadence gate would false-stop every legitimately-skipped mock.
#           It is owned solely by Step 1 RULE M5 (full-series pass). This is stated at S3-17
#           and in both new gate definitions so no future edit mistakenly adds one.
#           Coordinated per the gate-addition discipline: rule (S3-17) + gate code + HS-13/14 +
#           S4-11 per-batch checklist + §17 DoD + §18 glossary + §19 edge-cases + footer total
#           (63 → 65). All check logic validated in Python on real SSC data before encoding.
#   v4.9 — 2026-07-01 — ISSUE 2a: HARDCODED MANDATE NAMES REMOVED (no gate/rule change).
#           Completes the presence-mandate half of the v4.4 migration. S7-24 (QA) and S7-31
#           (GIR) still hardcoded exam subtopic names (Mensuration 3D, Direction Sense,
#           Address Matching, Coordinate Geometry, Statement-Argument, a named cipher + the
#           +2-shift ban) that RESTATED policy already owned by DATA — a prime-directive
#           violation and a silent-disagreement risk for any non-SSC exam (Claude reading
#           "MANDATORY ... NEVER AGAIN" could inject an SSC subtopic into a GATE/NEET paper).
#           None of the stripped lines carried executable code; they delegated to S3-17 /
#           gates, so removing them changes no control flow. FIX (exam-agnostic): (1) S7-24 /
#           S7-31 rewritten to point mandatory-presence to manifest.mandatory_every_mock
#           (Step 1 RULE M1 + Step 2 S3-17 HS-8 + G-ALLOC-SUBTOPIC), alternation to
#           manifest.alternation_groups (S3-17 + G-ALTGROUP), and cross-mock variant rotation
#           to section_rules ROTATION/ROTATION_BAN (S6-9) — zero subtopic names remain. (2) The
#           π=22/7 line generalised to "read the exam's math convention from section_rules".
#           (3) S7-NEW-B Option B's "For SSC CGL Tier 1: ..." replacement exemplar removed
#           (replacement comes from section_rules REPLACEMENT_RULE). (4) S17-1 DoD + §19
#           checklist named items replaced by exam-agnostic manifest/gate checks. PRECONDITION
#           satisfied before this edit (the incomplete-migration trap avoided): Framework_
#           PYQExtract v2.10 makes the manifest reproducible from section_rules (the
#           mandate_every_mock / alternation_group round-trip), and the SSC section_rules +
#           blueprint were repaired so the data path carries every stripped policy — Direction
#           Sense/Address Matching mandatory 50/50, ci_si de-conflicted; the repaired blueprint
#           passes S3-8 + S3-9 + S3-17 for all 50 mocks (validated twice). OUT OF SCOPE
#           (Issue 2b — needs NEW manifest fields): GROUP-PRESENCE (≥1 of a 3D-mensuration
#           group per mock), PER-WINDOW CADENCE (Coordinate Geometry every alternate mock), and
#           MIN-COUNT (Statement-Argument ≥2Q). These are NOT re-added as hardcoded names —
#           they become data in 2b.
#   v4.8 — 2026-06-30 — R8 SECTION-NAME HEADER BAN (mutation-harness finding). The mutation
#           harness found that R8 / G-SECTIONHDR caught only the KEYWORD header form
#           ("SECTION:", "Part A:"), not a stray heading that IS a declared SECTION NAME
#           ("Quantitative Aptitude", "Technical") — the realistic form. FIX: R8 now bans the
#           section-name form (provenance-based, matched against the paper's own section
#           names); assembly writes reg['section_names']; the embedded G-SECTIONHDR reads it
#           and flags any standalone body paragraph equal to a section name (in addition to the
#           keyword regex), scanning ALL body paragraphs. Mirrored + independently re-verified
#           by Step 3 A-SECHDR v1.5. Additive registry field; non-offending papers unaffected.
#   v4.7 — 2026-06-30 — NAT CONTRACT — GENERATION LAYER (cross-step NAT extension,
#           Step 2 half; gate count 60 → 63). DORMANT behind the blueprint's nat_present flag.
#             (1) answer_type_by_id read from blueprint subtopic_list; the NAT path is
#                 dispatched on answer_type=='numerical' (orthogonal to MSQ cardinality).
#             (2) R-ANSWER gains a THIRD branch (numerical): the answer is a typed VALUE that
#                 the stem must determine UNIQUELY (well-posedness), form-matched to
#                 nat_answer_type (integer⇒exact, real⇒ca_range band lo<=hi); 0/negative/
#                 fractional valid; value must not leak. verify_answer (CHECK 3) dispatches
#                 numerical first (supersedes cardinality).
#             (3) R4 / R13 NAT-exempt (zero options/option paragraphs); R14 places the
#                 nat_instruction inside the Q.N stem.
#             (4) build_answer_budget: NAT Q positions EXCLUDED from K-BAL/K-PAT
#                 (excluded = fixed ∪ msq ∪ nat); ND12 — the 20-30% band DEGRADES to a
#                 warning (best-effort) under heavy exclusion (n_free < 4·options_count)
#                 instead of an assert-crash; K-PAT still holds. Single-answer exams unchanged.
#             (5) sidecar: write_q_to_sidecar stores answer_type/qtype/ca_range and the NAT
#                 value; a nat_meta block carries the answer model (mirrors msq_meta).
#             (6) NEW GATES (60→63): G-NAT-NOOPT (S12-NEW-21, docx 0-option check),
#                 G-NAT-ANSWER (S12-NEW-22, value well-formed + ca_range lo<=hi),
#                 G-NAT-INSTR (S12-NEW-23, instruction in Q.N line).
#             (7) check_no_answer_key_in_docx extended to catch leaked NAT numerical keys
#                 (signed integer / decimal — the digit-1-9 patterns missed 0/neg/decimal).
#             (8) options_by_q written to registry.json (ND6, MANDATORY): per-question
#                 expected option count, 0 for NAT — Step 4 resolves question type from it.
#             (9) R-FIGURAL gains a figural-NAT variant (ND10: problem image, ZERO option
#                 images); linked/DI members may be 0-option NAT members (ND11).
#           Non-NAT exams byte-identical to v4.6 (every NAT branch gated on nat_present).
#           Validated: AST clean; the NAT gate block parity (true-positives + true-negatives)
#           re-run GREEN on a real NAT .docx fixture; budget degradation + value-leak tests pass.
#   v4.6 — 2026-06-30 — VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Pure
#           rename, no behaviour change: per-subtopic `answer_mode` -> `answer_cardinality`
#           (variables, sidecar concept_map field, dispatch, R-ANSWER prose); blueprint flag
#           `msq_present` -> `multi_present`. Blueprint reads accept the OLD names as a
#           fallback. Non-MSQ exams byte-identical to v4.5; gate count unchanged (60).
#           Validated: AST clean (41/41); the MSQ gate block parity (clean/k=0/k=n/AOTA x2/
#           fixed-k/missing-instr/dormant) re-run GREEN on the renamed file. First step of the
#           Steps 0-4 single-vocabulary alignment (answer_type + answer_cardinality).
#   v4.5 — 2026-06-30 — MSQ CONTRACT — GENERATION LAYER (cross-step MSQ extension,
#           Step 2 half; gate count 57 → 60). DORMANT behind the blueprint's
#           multi_select_allowed / multi_present: for any single-answer exam (the default,
#           incl. SSC CGL) v4.5 generates a byte-identical paper to v4.4. The MSQ path
#           activates ONLY for subtopics whose blueprint answer_cardinality=="multi".
#           The contract was FROZEN and empirically validated (real docx fixtures,
#           18/18 truth-table) BEFORE encoding — see the MSQ scope analysis.
#             (1) R-UNIQUE GENERALISED → R-ANSWER (single source of truth, D8). One
#                 answer-mode-parameterised HARD STOP, mirrored verbatim by Step 3 RA-12:
#                   single: exactly ONE option defensible; all others indefensible.
#                   multi : every option in the correct SET S is defensible under EVERY
#                           fair reading; every option NOT in S is indefensible; S is a
#                           non-empty PROPER subset of {1..options_count} (1≤|S|≤n−1), and
#                           |S|=msq_k when msq_k_mode=fixed. Negation composes (S is the set
#                           satisfying the possibly-negated predicate). R-UNIQUE's single-
#                           answer text is preserved exactly as the single-mode branch.
#             (2) verify_answer_uniqueness → verify_answer(candidate): single branch
#                 unchanged; new multi branch verifies the set contract above.
#             (3) ANSWER-KEY SIDECAR is now set-valued: answers[q] = int | list[int];
#                 field answer_uniqueness_verified → answer_verified (mode-agnostic).
#             (4) build_answer_budget: MSQ Qs are EXCLUDED from the K-BAL/K-PAT single-
#                 position pool (reusing the existing fixed_set exclusion mechanism via a
#                 new msq_positions set) — a "run of identical answers" is undefined over
#                 sets. No set-position balancer in v1 (D7).
#             (5) DISPATCH: build_question reads the subtopic's answer_cardinality (blueprint
#                 subtopic_list) and routes 'multi' to the MSQ builder. The MSQ instruction
#                 line ("(One or more options may be correct)" / "(Select TWO)") is appended
#                 INSIDE the bold Q.N-first stem (R14 / G-QNUM-FIRST — there is no paper-
#                 level instructions page), phrasing from section_rules, language-localized.
#             (6) DISTRACTOR cardinality generalised: a multi Q builds |S| defensible
#                 options + (options_count−|S|) indefensible ones. CLASS-2 vocab menus
#                 inverted accordingly (k correct items + distractors); vocab_words_used
#                 records the FULL correct set, not one word.
#             (7) NEW RULE R-MSQ-ESCAPE (D5, parametric): "All of the above" is rejected
#                 under multi unless section_rules msq_allow_aota=true (default false);
#                 "None of these" stays an ordinary option. Enforced by G-MSQ-SET.
#             (8) NEW GATES (57→60): G-MSQ-SET (S is a well-formed non-empty proper
#                 subset, AOTA rule honored — always), G-MSQ-CARD (|S|=msq_k — fixed-k
#                 only), G-MSQ-INSTR (the multi instruction line is present in the Q.N
#                 stem). G-UNIQUE generalised to accept set-valued keys (record-presence
#                 backstop for R-ANSWER, both modes).
#             (9) check_no_answer_key_in_docx extended to catch SET-valued key leaks
#                 ("Q.1 → 1,2,4") — the single-digit patterns missed comma/space lists.
#             All MSQ behaviour is config-driven (multi_select_allowed / answer_cardinality /
#             msq_k_mode / msq_allow_aota) — zero exam names hardcoded. R4 (option count)
#             unchanged: a multi Q still has options_count options; only answer cardinality
#             differs. difficulty: MSQ load term lives in Step 0 E-9, inherited via blueprint.
#
#   ALL 20 v2.0 GAP FIXES RETAINED IN v3.0 (verified present in body):
#     GAP-01 batch enforcement (now §4 + MANDATE 1) · GAP-02 blueprint parsing (S3-2)
#     GAP-03 content_tracking init (S13-4) · GAP-04 registry fields (S14-1)
#     GAP-05 python-docx mandate (MANDATE 2) · GAP-06 DI table (S8-4)
#     GAP-07 ExplainLearnings load (S3-2) · GAP-08 K-PAT pre-alloc (S3-13)
#     GAP-09 Direction Sense/Address Matching (S3-17, S7-31) · GAP-10 Mensuration 3D (S7-24)
#     GAP-11 Coordinate Geometry (S7-24) · GAP-12 figural ban (S7-NEW-B)
#     GAP-13 section-heading ban (R8) · GAP-14 Calibri font (R24)
#     GAP-15 option label "1.  text" (R10) · GAP-16 progress.json gated (S4-8b)
#     GAP-17 no answer key in docx (R5, S11-4) · GAP-18 per-Q sidecar (S7-NEW-A, S11-2)
#     GAP-19 pending_registry (S3-4) · GAP-20 alternation/rotation — mutual
#         exclusion owned by S3-17/G-ALTGROUP (manifest.alternation_groups);
#         cross-mock variant rotation by section_rules ROTATION cycle (S6-9, v4.4)
#


# ═══ ARCHIVE — Framework_MockTestAnalyse pre-relocation header history (moved 2026-07-31 at v2.39; verbatim) ═══

# MINIMUM COMPANION VERSIONS (v2.37) — SUPERSEDED by the v2.39 block above:
#   corpus_io.py          >= v1.7  — MUST carry Cluster V: build_vision_queue(),
#                           load_vision_queue(), load_vision_observations(),
#                           write_vision_observations(). Without them S4-2a/S4-2c
#                           reference functions that do not exist and Phase A cannot
#                           emit a queue at all.
#   blueprint_core.py     — MUST carry Cluster V: vision_tag_map(),
#                           merge_vision_observations(), vision_profile(). An older
#                           engine raises AttributeError at the first batch boundary
#                           rather than silently producing an empty profile — which is
#                           the correct direction to fail for a MISSING DEPENDENCY
#                           (loud, immediate, at import-adjacent time), as distinct
#                           from a vision GAP, which never halts.
#
# MINIMUM COMPANION VERSIONS (v2.34) — SUPERSEDED by the v2.37 block above:
#   corpus_io.py          — the ProbeObservationMissing / score_vision_probe
#                           requirement is RETIRED. corpus_io v1.8 deletes that whole
#                           family: PHASE B observes REAL figures, so liveness arrives
#                           free as a by-product and a separate probe would be a second
#                           mechanism answering one question. Kept here as history —
#                           the reasoning behind it produced the three-phase design.
#   blueprint_core.py     — MUST carry derive_image_roles() / IMAGE_ROLES. E-4 delegates
#                           role derivation to it; an older engine raises AttributeError
#                           at the first paper rather than silently mis-classifying.
#
# MINIMUM COMPANION VERSIONS (v2.33):
#   corpus_io.py          >= v1.4   — both readers go through load_taxonomy(),
#                                     and both assert assert_taxonomy_lock(). v1.2 adds
#                                     INGEST FORMS (the doc is stored in project Files as
#                                     extracted TEXT); v1.3 adds the lock gate itself.
#   blueprint_core.py     — Cluster E/G delegation (score_difficulty, determine_strip_mode);
#                           and the GAP-2026-07-26-001 build carrying
#                           next_nonempty_texts() and is_taxonomy_heading(para,
#                           is_option, next_text). S3-2 PASSES next_text at BOTH
#                           loops; an older engine raises TypeError rather than
#                           silently truncating stems.
#
# v2.33 — 2026-07-26 — GAP-2026-07-26-001: THE STEM NO LONGER ENDS ITSELF.
#         PYQSort EC-S8 emits multi-paragraph stems whose continuation lines are bold,
#         not dates, not options and not question starts — character for character the
#         level-3 heading predicate. extract_presorted()'s INNER loop breaks on a
#         heading, so a question's own continuation line terminated the question
#         mid-body: the stem was truncated at the figure, and every option after that
#         point was orphaned, because the outer loop then treated the remaining stem
#         lines as headings and skipped the option paragraphs as neither headings nor
#         question starts.
#         THIS WAS THE DANGEROUS HALF. Step 4's phantom gate stops the run; nothing
#         here stopped anything. The question count stays right, so QV parity holds and
#         every gate passes — the options simply never existed as far as the extractor
#         was concerned. The corruption flowed into section_rules.md, the manifest and
#         the Frequency xlsx, and from there into Step 6 allocation and Step 7
#         generation.
#         MEASURED, IIT_JAM_BIOTECHNOLOGY, 22 papers: 16 questions truncated, 28 option
#         lines silently discarded, 10 of 22 papers affected. Rows showing zero options
#         lost are NAT or image-option questions whose stems were truncated anyway,
#         corrupting full_stem, is_neg, detect_blank_position(), MSQ detection and
#         FIGURAL classification.
#         FIX (S3-2, and the E-1 pseudocode that describes it): build
#         bc.next_nonempty_texts() once per document and pass next_text at BOTH the
#         outer heading loop and the inner break. A bare level-3 heading is genuine
#         only when the next non-empty paragraph is a DATE LABEL — guaranteed
#         exam-agnostically by PYQSort S6-2, CHECK 3 and EC-S10.
#
# v2.32 — 2026-07-26 — BOTH READERS LOAD THROUGH load_taxonomy(). The read and the
#         identity assertion collapse into one call at both sites, and the taxonomy
#         comes from approval_record.json where the record carries it
#         (reconcile_taxonomy >= v1.3) rather than from a Word document — on that
#         path Step 5 parses nothing. Pre-1.3 records fall back to the doc, fully
#         gated, and need no re-run. `path=` is still passed at both sites: it is
#         used only on the fallback path and ignored on the record path.
#         MINIMUM COMPANION: corpus_io.py >= v1.4.
#
# v2.31 — 2026-07-26 — THE TAXONOMY LOCK GATE REACHES STEP 5 (GAP-2026-07-25-003
#         follow-up). v2.30 made both readers correct; neither checked that the doc
#         they read was the doc PYQApprove APPROVED. Framework_PYQSort S1-0b made
#         that claim from v1.14 and nothing else did, so a superseded or mis-parsed
#         Analysis doc that HALTS LOUDLY at Step 3 was accepted here without a word.
#         Step 5 mints the subtopic_ids that Steps 6-11 match on, so the failure is
#         not a degraded run: it silently renames the vocabulary of the pipeline.
#         Both call sites now call corpus_io.assert_taxonomy_lock() — THE gate, one
#         implementation in corpus_io, not a fifth copy of S1-0b's logic.
#         SECOND DEFECT, found while wiring the first: the fault could not have
#         surfaced even if the gate had existed. _extract_taxonomy_tuples_from_
#         analysis_doc() ended `except Exception: return []`, and its caller wrapped
#         the call in `except Exception -> sync_log WARN`. Three situations were
#         therefore indistinguishable — "absent by design", "unreadable", "not the
#         approved taxonomy" — and only the first is benign. A fault had to survive
#         TWO independent downgrades to be seen. Absence is still tolerated and
#         still returns []; everything else is now raised. This is the same defect
#         class as v2.30's own (`both except branches swallow silently`), one layer
#         up, which is why it outlived the fix.
#         MINIMUM COMPANION: corpus_io.py >= v1.3.
#
# v2.30 — 2026-07-25 — BOTH ANALYSIS-DOC READERS DELEGATED (GAP-2026-07-25-002).
#         extract_taxonomy_from_analysis_doc() and _extract_taxonomy_tuples_from_analysis_doc()
#         both returned ZERO subtopics from a real Analysis doc — on every exam, since they were
#         written. Verified by executing both against the first exam's live doc: 0 tuples against
#         a truth of 131. Two independent causes: they iterate doc.paragraphs while every subtopic
#         lives in a TABLE, and they key hierarchy off Word Heading 1/2/3 styles and left_indent
#         that the generator does not emit (para.style is None for every paragraph of a real doc).
#         Both also carried the same `not cur_sec` first-value latch as the P0 fixed in
#         Framework_PYQSort v1.14, and on a styled doc the first reported 12 phantom sections by
#         reading the title line and the "Subject:" line as two separate level-1 headings.
#         Consequence: Source 2 of the v2.20 taxonomy sync — the net that mints ids for zero-PYQ
#         subtopics — has never contributed anything, and because both except branches swallow
#         silently, that emptiness was indistinguishable from "the doc had nothing to add".
#         Both now delegate to corpus_io Cluster K, THE reader/writer/verifier for this artefact,
#         which additionally HARD STOPS when a parse disagrees with the totals the document
#         declares about itself. Signatures and failure contracts unchanged.
# v2.38 — 2026-07-26 — COMPANION REQUIREMENT UPDATED: VISION-PROBE FAMILY RETIRED.
#     corpus_io v1.8 deletes normalise_for_view(), make_vision_probe(),
#     score_vision_probe(), ProbeObservationMissing and VisionUnavailable. Once v2.37
#     removed the last spec call site, audit_callgraph C4 correctly reported the first
#     three as public-but-unreached; leaving them would have made C4 report findings
#     forever, and "a check that can be shipped past is decoration" (CLAUDE.md).
#     Nothing in this spec's behaviour changes — liveness already came from Phase C
#     observation coverage (S3-1c) and normalisation already happened inside
#     build_vision_queue. This release only removes the dead API and the stale
#     companion-version requirement that still demanded it.
#
# v2.37 — 2026-07-26 — EXECUTION-BOUNDARY LAW: VISION BECOMES REACHABLE
#     (GAP-2026-07-26-003). The corpus never wrote down that a TOOL CALL cannot
#     happen inside a running python process. Drive was worked around by accident of
#     necessity; vision never was, and nothing could tell the two apart.
#
#     MEASURED ON THE REFERENCE RUN (IIT_JAM_BIOTECHNOLOGY, 22 papers, 1719 Qs):
#       * object_type / transformation / arrangement / complexity present on 0 of 1719
#         questions — the keys were never written at ALL, not written as None.
#       * 153/153 figural questions recorded image_clarity='vision_unavailable'.
#       * 45/45 FIGURAL subtopics shipped object_types.dominant: [].
#       * QV-9 returned PASS. The footer rendered green.
#
#     ROOT CAUSE. `vision_result = analyse_image_claude(q, view_path)` was followed by
#     `vision_result.get(...)`. analyse_image_claude() was a `pass` stub returning None,
#     so the block RAISED AttributeError if executed literally. Every production run
#     therefore executed some SUBSTITUTED body, non-deterministically, and the
#     substitution that shipped wrote image_clarity and nothing else.
#
#     THE LAW (now also in CLAUDE.md). Every operation is DETERMINISTIC, CLASS J
#     (judgment over in-context data) or CLASS T (needs a tool call). A CLASS T
#     operation MUST NOT be called from inside a python block and MUST NOT be modelled
#     as a python function, callback or parameter. CLASS T uses MATERIALISE-THEN-INJECT.
#
#     CHANGES:
#       * S3-1     in-loop vision block DELETED; emits a PHASE A queue instead. It no
#                  longer writes image_clarity — Phase C is the single writer.
#       * S4-1     get_vision_candidates returns ALL of a question's stem images, so a
#                  panel series is judged as a series (EC-V6).
#       * S4-2     analyse_image_claude() DELETED. Replaced by the three-phase contract.
#       * S4-2a    PHASE A — corpus_io.build_vision_queue(): normalise, compose, tile.
#       * S4-2b    PHASE B — PROSE PROTOCOL IN A PLAIN FENCE, never ```python. Turning
#                  this into a function is precisely how the defect returns.
#       * S4-2c    PHASE C — apply_vision_observations(): the ONLY writer of the five
#                  vision fields. Never raises, never halts.
#       * S3-1c    run_img6_probe(read_probe) DELETED. Its callback could not make a
#                  tool call, so it defaulted to returning '' and reported EVERY session
#                  blind. Liveness is now DERIVED from Phase C — one rule, zero cost.
#       * DRIVE    gdrive_search/gdrive_download_file tagged CLASS: T. fetch_drive_docx
#                  now receives an INJECTED resolver over already-materialised payloads
#                  instead of the stub itself. Executed literally the old form routed
#                  ALL 22 reference papers to the upload lane on EVERY run.
#       * S3-2     'q_num' stamped beside 'num' at the one emission point. Three readers
#                  wanted q_num and got None, silently (PART 9): era classification ran
#                  on a question count of zero and S-SECMAP gave every section every
#                  subject. EC-V15 also needs it — 153 figural Qs carry only 62 distinct
#                  q_num values, so a bare q_num mis-attributes 91 of them.
#       * S4-4     aggregate_figural DELEGATES to bc.vision_profile(). The local top-3
#                  named a dominant type from any sample size and even from a FLAT
#                  distribution (six figures, six types -> "dominant" = the alphabetical
#                  first three). EC-V20 / EC-V26.
#       * §5       section_rules serialiser: arrangement_types, complexity_dist,
#                  object_types.avoid, images_analysed, images_unclear were BUILT and
#                  then DROPPED at the artefact boundary. All now written, plus
#                  vision_status — in the reference run 'vision_unavailable' appeared
#                  153x in progress.json and 0x in section_rules.md, so a consumer could
#                  not tell "no figures" from "vision failed".
#       * QV-14    NEW, FAIL severity. QV-9 cannot see this failure: it needs
#                  images_analysed + images_unclear > 0 and both are zero when nothing
#                  was observed. Denominator excludes EC-V13/EC-V14; an exam with no
#                  figural content PASSes vacuously (EC-V1).
#
#     NOTHING IN THIS RELEASE HALTS. A missing observations file, malformed JSON, an
#     absent Pillow, an unopenable vector part, or a Phase B that never ran all degrade
#     with a recorded reason and the run COMPLETES. The defect being fixed was SILENCE;
#     the remedy for silence is visibility (QV-14 + vision_status), never a halt.
#
# v2.36 — 2026-07-26 — is_option DELEGATED (audit_deep [XSPEC-DRIFT]).
#   v2.34/v2.35 made is_option() image-option-aware HERE and nowhere else. The
#   predicate is defined in three specs, each claiming alignment with the others in
#   its docstring, so those claims silently became false. Not cosmetic: PYQSort USES
#   its copy to count options, so the identical defect this wave fixed in Step 5 was
#   left live in Step 1 — measured on IIT_JAM_BIOTECHNOLOGY 2022, 156 options counted
#   against 160 actual. OPT_PATTERNS, BARE_OPT_PATTERNS, para_has_image, is_option and
#   clean_option_text now live in corpus_io >= v1.6 and all three specs delegate.
#   Drift is impossible by construction rather than asserted by comment.
#
# v2.35 — 2026-07-26 — THREE DEAD ENGINE FUNCTIONS WIRED (audit_callgraph C4).
#   The v2.34 auditor reported them; this closes them. All three had existed for
#   versions, were documented in prose, and were called by nothing.
#   * corpus_io.figural_consistency — IMG-5b. Written to catch exactly the DEFECT-3
#     class of fault and never reachable, so the two defects masked each other. Now
#     executable in S3-1d and called from process_pyq_paper after tag_axes(). WARN,
#     not HARD STOP: IMG-4 already stops on real image loss, and an INHERENTLY-VISUAL
#     override is legitimately figural without an embedded figure.
#   * corpus_io.normalise_for_view — every figure went to view() un-normalised.
#     corpus_io's own docstring records that every figure measured in this corpus is
#     a CMYK JPEG, "not a safe input to a vision call", and PYQPrepare has instructed
#     callers to normalise since v1.6 — but no spec ever did. A CMYK or oversized
#     figure therefore read as unclear for a reason that had nothing to do with the
#     figure, inflating exactly the QV-9 rate v2.29 set out to make trustworthy.
#     Now called before analyse_image_claude(); PIL absence degrades to the original.
#   * corpus_io.parse_drive_folder_id — S1 carried its own inline copy of the Drive
#     URL regex. The engine version additionally accepts a bare folder id and the
#     /u/N/ account-scoped URL the inline copy silently failed on. Delegated.
#
# v2.34 — 2026-07-26 — E-4 IMAGE PATH WIRED, IMG-6 MADE REAL, IMAGE OPTIONS RECOGNISED.
#   GAP-2026-07-26-002. v2.29 built a correct image-integrity subsystem and connected
#   almost none of it. Verified by EXECUTION against the full 22-paper
#   IIT_JAM_BIOTECHNOLOGY corpus, not by inspection.
#   DEFECT-1. extract_and_map_images(docx_path=None) had exactly ONE call site in the
#     whole framework and it never passed docx_path, so `if docx_path:` was always False
#     and every Step-5 run on every exam took the branch this file labelled UNGATED. The
#     docstring stated a requirement nothing satisfied. Legacy branch DELETED; docx_path
#     is now a required positional.
#   DEFECT-2. The two branches returned arity 3 in DIFFERENT orders — (img_map, imap,
#     q_roles) vs (imap, q_roles, report). Equal arity means no interpreter error: the
#     unpack silently mis-bound and q_roles became the report dict, so every
#     .get(num,{}).get('role') returned 'none'. ONE return shape now.
#   DEFECT-3. The gated branch never derived 'role'. Delegated to
#     bc.derive_image_roles() — one rule, one owner, per the audit_deep DELEGATION
#     contract. A second inline copy is the drift pattern v2.27/v2.28 removed elsewhere.
#   DEFECT-4. probe_passed reached nothing and bc.image_clarity_state() was never called
#     from any executable block, so 'vision_unavailable' was unreachable and QV-9 could
#     never fire. run_batch_loop() now runs the probe per batch and threads the result.
#   DEFECT-5. expected_size was captured by enumeration and threaded nowhere, so IMG-1
#     SKIPped on every paper — the only check that catches a ZIP truncated at a member
#     boundary. Verified: IMG-1 SKIP -> PASS on all 22 papers.
#   PART A. IMG-6 was PROSE in no executable block, single-attempt, single-token, with no
#     requirement to record what was read — and score_vision_probe() returned False for an
#     empty string, making "I did not look" indistinguishable from a blind session. It
#     produced a false session-terminating halt on its first production use. Now a
#     function (run_img6_probe), 3 attempts with 3 distinct tokens, and it NEVER HALTS.
#   B-6. THE DEFECT THAT WAS ACTUALLY CORRUPTING DATA. OPT_PATTERNS all require text
#     after the marker, but an IMAGE OPTION has none — the paragraph is "1." and the
#     picture follows. is_option() returned False, cur_opt never advanced, every image
#     tagged 'stem', role 'stem_only' not 'stem_and_options', options == [], and
#     classify_axis3() returned NAT. Measured: 52 image-option MCQs across 20 of 22
#     papers with the WRONG ANSWER MECHANISM — 3.0% of 1,719 questions feeding Axis-3,
#     Step 6 allocation and Step 7 generation. BARE_OPT_PATTERNS + para_has_image() fix
#     it, keyed on structure only — no exam, subject or option string anywhere.
#   MEASURED, NOT ASSUMED. The 22-paper corpus contains ZERO table images, ZERO VML and
#     ZERO header/footer images: Step 1 normalisation removes them, so legacy and gated
#     map the identical 329 images. The table-image blindness v2.29 targeted is real code
#     but had NO effect on this corpus. The real damage was role assignment.
#   META-LESSON. Harness verification proves a function correct in isolation while the
#     production call site never reaches it. Every future fix must answer: WHAT IS THE
#     CALL SITE, AND DOES IT REACH THIS CODE ON A REAL RUN? audit_callgraph.py C1-C5 now
#     enforces this mechanically.
#
# v2.29.1 — 2026-07-25 — E-2 Q_PATTERNS TABLE RECONCILED WITH THE ENGINE. E-2 is the table every
#         other spec says it aligns to, and it listed five patterns against an engine
#         implementing two. audit_deep TABLE-PARITY could not detect this — its regex truncated
#         at the "]" inside r'^Question\s+(\d+)\s*[:.]'. Documentary table, declared and never
#         read, so behaviour is unchanged; the note added in its place records why the three
#         raw-source forms must never be restored here (options read "N. text" after Step 1, so
#         bare-number matches them all).
# v2.29 — 2026-07-25 — CORPUS TRANSPORT + IMAGE INTEGRITY. Sixteen defects, twelve of them
#   in this file. Root cause of the reported failure: the Drive connector caps downloads at
#   10 MiB and 6 of 7 pending papers were above it, but the pipeline had no way to know —
#   collect_drive_docx_recursive discarded the fileSize the listing already carried, so the
#   blocker surfaced only at batch 6, and gdrive_download_file was called with no try/except
#   (verified: ZERO try/except existed around any Drive call in all 31 tracked files).
#   Worse, save_progress ran AFTER the per-paper loop, so a failure on paper 3 silently
#   discarded papers 1 and 2 — invisible in the reported incident only because all three
#   papers in that batch were oversized.
#   Image integrity was independently broken. extract_and_map_images walked doc.paragraphs,
#   which in python-docx does NOT descend into tables, so every figure laid out in a table —
#   the normal arrangement for match-the-following, multi-panel figures and option grids —
#   was invisible: the question classified TEXT instead of FIGURAL, corrupting the format
#   distribution that drives Step 7, with no error raised. Proven by construction. Legacy VML
#   <v:imagedata> images were invisible everywhere (0 occurrences of 'imagedata' in any image
#   spec), header/footer images were never extracted, pre-Q.1 images were dropped silently,
#   and NO image-count assertion existed anywhere in this file (PYQFormat S8-6 has had one
#   for the equivalent risk since v1.1).
#   Fix: (1) enumeration captures fileSize + mimeType and screens every entry — native Google
#   Docs, shortcuts and legacy .doc are REJECTED WITH A REASON instead of vanishing silently;
#   duplicate canonical identity is a HARD STOP. (2) all fetching via corpus_io.fetch_drive_docx;
#   every failure raises TransportFallback and degrades to the UPLOAD LANE — never a hard stop,
#   which is what makes this survive a future change to the cap. (3) save_progress after EVERY
#   paper. (4) extract_and_map_images rewritten to walk body.iter() and match both blip and VML.
#   (5) gates IMG-1..IMG-6 with a vision liveness probe. (6) image_clarity becomes three-state:
#   'unclear' now means the FIGURE is illegible, 'vision_unavailable' means the SESSION cannot
#   see — previously conflated, so a blind session blamed the corpus and inflated QV-9.
#   (7) new QV-13. (8) the real download envelope documented (context spill + double JSON parse).
#   BATCH_SIZE and the S8-1 BATCH STOP law are UNCHANGED.
#
# v2.28 — 2026-07-23 — detect_question_start + slugify DELEGATED (Cluster G / Cluster D).
#   Found by MUTATION TESTING, not by any existing check. Re-localising a shared function in
#   ONE spec produces zero drift signal — cross-spec drift detection needs two DIFFERING
#   copies, and once a function is correctly delegated everywhere else, only one local copy
#   can exist. The heading-parser drift fixed in v2.27 could therefore have returned the next
#   day with every check green. audit_deep.py now enforces a DELEGATION contract (engine-owned
#   names must not be defined inside a spec, except as a thin forwarding adapter) and a
#   TABLE-PARITY check (a delegated function is worthless if each spec keeps its own copy of
#   the table it reads). No behaviour change: both engine forms are byte-identical.
#
# v2.27 — 2026-07-23 — SHARED-PARSER DRIFT CLOSED (twin of Framework_PYQAnalyse v2.20).
#   is_taxonomy_heading / parse_taxonomy_level / extract_year_from_filename all existed in
#   BOTH this spec and PYQAnalyse Phase B — two steps walking the same sorted .docx — and all
#   three pairs had drifted despite an explicit "keep IDENTICAL" instruction in the Step-4
#   copies and EC-P14 documenting the exact failure mode. parse_taxonomy_level: this file
#   gained 12+ heading patterns in v2.16, Step 4 kept 3. is_taxonomy_heading: different
#   question-exclusion regexes, so the two steps disagreed on the heading SET. And
#   extract_year_from_filename: this copy required 20xx on the basename while Step 4's took
#   any 4 digits anywhere in the path — a pre-2000 paper was invisible here and visible there,
#   and a digit-bearing folder could supply the year there. All three now delegate to
#   blueprint_core Cluster G, whose forms are supersets (proven: test_cluster_g.py).
#
# v2.26 — 2026-07-23 — MAKE frequency_scope REACHABLE + ROUTE THE ENGINE
#   (audit follow-up; fixes two defects introduced BY v2.25).
#   (1) P0 REGRESSION FIXED. v2.25 added three `import blueprint_core` statements to this
#       spec — the first this file has ever had — but routes.json gave PYQExtract only
#       [Framework_MockTestAnalyse.md, Framework_DeliveryFooter.md]. The pattern_eras block
#       is gated on `if progress and exam_config:` with NO scope gate, so it ran on every
#       properly-configured exam and raised ModuleNotFoundError, aborting Step 5 for ALL
#       exams — not merely those opting into era scoping. routes.json now routes
#       blueprint_core.py to PYQExtract (and to the other PYQ triggers that reference it).
#   (2) P1 FIXED — THE FEATURE WAS UNREACHABLE. `frequency_scope` existed as a function
#       parameter defaulting to 'all', and no trigger could set it: the Step-5 trigger
#       grammar had no such flag and the string appeared nowhere outside this file. The
#       entire v2.25 feature was dead code. New `--frequency-scope all|current-era` flag,
#       parsed at session start and passed to generate_frequency_xlsx() and
#       write_subtopic_manifest().
#   (3) Era classification is now fully engine-backed (bc.classify_paper_era), including the
#       new 'retyped' era for exams that keep their question count but change question TYPES.
#   LESSON RECORDED: v2.25 was verified file-by-file with extracted-code harnesses that all
#   passed because blueprint_core.py happened to sit in the test working directory. No test
#   asserted that a TRIGGER's route actually supplies the modules its specs import. A routing
#   test (test_routing.py) now does exactly that for every trigger.
#
# v2.25 — 2026-07-23 — ERA-SCOPED FREQUENCY (GAP-2026-07-23-002; completes the
#   pattern-era work begun in Framework_Blueprint v1.36 / PYQSort v1.9 / PYQAnalyse v2.18).
#   THE PROBLEM those three did NOT solve. They stopped legacy papers from corrupting
#   question COUNTS and stopped 38%-of-corpus silent data loss, but the subject/subtopic
#   MIX stayed era-blended. Recency weighting (Framework_Blueprint §3, last 2 valid years
#   x2) dampens this and cannot fix it: a real corpus of 21 retired-era years against 6
#   current-era years still leaves the RETIRED pattern holding 72% of the r_avg weight
#   (21/29 vs 8/29), so mocks over-serve topics the exam stopped asking and under-serve the
#   ones it now emphasises.
#   THE INSIGHT. A PYQ corpus carries two kinds of information needing OPPOSITE treatment:
#     QUESTION SHAPES (templates, difficulty calibration, phrasing — §14 synthesise_subtopic)
#       improve with EVERY era. A subtopic seen across 26 years is far better characterised
#       than one seen twice. This is the entire reason legacy papers are retained.
#     PROPORTIONS (how many questions a subtopic deserves) can only come from the CURRENT
#       pattern. A retired pattern's mix is not evidence about today's exam.
#   (1) NEW `frequency_scope` parameter on generate_frequency_xlsx() and
#       write_subtopic_manifest(). DEFAULT 'all' — byte-identical to v2.24.10 for every
#       exam, so nothing changes unless an exam opts in. 'current-era' restricts the
#       COUNTING VIEW to papers matching the current pattern.
#   (2) The filter is applied at the counting seam ONLY. bc.filter_progress_to_eras()
#       returns a COPY, so `progress` is never mutated and §14 pattern/template synthesis,
#       section_rules.md and the taxonomy keep consuming the FULL corpus. Variety in,
#       faithful proportions out.
#   (3) The axis distribution obeys frequency_scope too — it is a MIX quantity. Its two
#       existing protections are kept (3-most-recent-years windowing; Blueprint v1.36
#       rescale-to-sec_qs), but neither covers a pattern that changed WITHIN the last 3
#       years, where the window straddles two patterns and the class proportions blend.
#       Era-scoping closes that at the source, with a documented fallback to the
#       full-corpus axis when era-scoping would leave nothing to measure (a blended axis
#       rescaled to the right size beats status='no_pyq', which would disable the whole
#       three-axis feature for that section).
#   (4) NEW manifest['pattern_eras'] — per-paper era, the era counts, and the scope that
#       was used. Purely additive audit trail; absent on pre-v2.25 manifests and no
#       consumer is required to read it.
#   (5) ENGINE: blueprint_core.py Cluster F (classify_paper_era, exam_config_bounds,
#       paper_key, paper_eras_from_progress, filter_progress_to_eras). classify_paper_era
#       is the SINGLE SOURCE OF TRUTH shared with Framework_PYQAnalyse S3-2a step 3b, so
#       the two specs cannot drift on what 'current era' means.
#   EDGE CASES COVERED (test_era_scope.py, 9,042 assertions): zero current-era papers
#   (HARD STOP with an actionable message, never a silent divide-by-zero); MIXED-ERA YEARS,
#   where two shifts of the same year sit in different patterns — filtering is per-PAPER
#   via (year, shift), never per-year, so this is exact; 'renumbered' papers (right count,
#   out-of-range numbers); 'smaller' papers (which by construction produce NO out-of-range
#   questions); missing/empty exam_config (raises rather than classifying against zeroes,
#   which would mislabel the whole corpus 'larger'); shift=None; unparseable q_num;
#   fewer than 3 current-era papers (WARN — recency weighting needs 2+ valid years).
#   LEGACY-ONLY SUBTOPICS behave correctly by construction: a subtopic the current pattern
#   never asks falls to zero observed questions, so Framework_Blueprint §3-4 CASE 2 makes it
#   Zero-PYQ and §5 ZP rotation gives it occasional coverage instead of a mix-distorting
#   quota — while it KEEPS its place in the taxonomy and its full pattern library. Verified:
#   the legacy-only subtopic key survives the filter with 840 source questions intact.
#   MEASURED on the reference corpus (2000-2020 @90Q + 2021-2026 @50Q, 27 papers):
#   coverage_pct 162% -> 100%; counted papers 27 -> 6; questions counted 2,190 -> 300;
#   full 2,190-question corpus confirmed intact for pattern synthesis (non-mutation test).
#
# v2.24.10 — 2026-07-23 — E-9/E-10 CANONICAL COPY MOVED TO blueprint_core.py (annotation
#   only — ZERO logic change in this spec). score_difficulty (E-9) and determine_strip_mode
#   (E-10) were extracted VERBATIM into blueprint_core.py Cluster E so PYQ-4 (PYQDeliver
#   v1.2 §2-3 Tier 2) can resolve per-question Complexity from the SAME scorer Step 5 uses,
#   without a third embedded copy. blueprint_core.py is now the CANONICAL shared copy.
#   CROSS-FILE SYNC RULE: any change to E-9/E-10 in this spec MUST be applied in the same
#   session to blueprint_core.py Cluster E (and vice versa), re-verified byte-identical.
#   Step 8 B-DIFF mirrors the MSQ load term — threshold/flag changes also need a Step 8
#   review. Step 5's own execution is unchanged: it continues to run the code embedded here.
#
# v2.24.9 — 2026-07-22 — S-SECMAP: SECTION↔SUBJECT MAPPING (BUG 1 of 4, GAP-2026-07-22-001).
#   Root cause: exam_config.json sections[] never carried a `subjects` field listing which
#   taxonomy Subjects belong to each OTS section. For any exam where OTS section names differ
#   from manifest Subject names AND there are multiple sections (e.g. IIT JAM "Section A/B/C"
#   vs manifest "General Biology"/"Chemistry"/...), Step 6's resolver (S2-1b) would HARD STOP
#   at SEC-4 — unable to determine the mapping. For 1:1 exams (SSC CGL, MPPSC) the resolver's
#   SEC-3 identity-map path handled it, masking the gap.
#   FIX: new S-SECMAP rule in run_synthesise(), after taxonomy sync and before writing outputs.
#   3-stage derivation: (1) OBSERVE which subjects appear in which section Q-ranges from PYQ
#   classifications, (2) AUGMENT cross-subject sections with union of all cross-subject pools,
#   (3) FALLBACK unmapped taxonomy subjects to cross-subject or all sections.
#   Writes subjects[] to each section in exam_config.json; adds exam_config.json to final
#   delivery (6 files, was 5). User must REPLACE exam_config.json in project knowledge.
#   Zero behavior change for 1:1 exams (subjects[] = single-element list matching SEC-3).
#   12/12 edge cases pass (SSC CGL, MPPSC, IIT JAM, GATE, CSIR NET, UGC NET, NEET,
#   fuzzy names, sampling gap, Zero-PYQ subject, structure change, single-section).
#
# v2.24.8 — 2026-07-20 — PYQ CORPUS DRIVE-ONLY STANDARDIZATION (twin fix: Framework_
#   PYQAnalyse.md Step 2b / PYQScan). Found during a project-level audit: three
#   pipeline steps that all handle the SAME document class (Row/Sorted PYQ .docx
#   corpus files) disagreed on whether Google Drive was required — Step 4 (PYQCount)
#   always mandated Drive with no fallback; Step 2b (PYQScan) allowed an uploads-only
#   fallback; this step (Step 5) allowed the broadest fallback (project/uploads).
#   STANDARDIZED to Step 4's existing Drive-only rule (confirmed with Radheshyam) —
#   Row/Sorted PYQ corpus files must be in Google Drive across all three steps now.
#   WHAT CHANGED:
#     Header comment block, §1 S1-1 — PYQ: <<Drive link>> is now REQUIRED for paper-processing
#       (auto-mode); absent → HARD STOP. --status/--synthesise are exempt (they don't
#       re-scan the PYQ corpus) — if PYQ: is given anyway for those modes it's used
#       opportunistically, non-fatal on Drive error.
#     §1 S1-2 — removed the local project/uploads fallback loop for pyq_doc_paths
#       (the raw PYQ corpus). Exam Pattern and Analysis documents are UNCHANGED —
#       those remain project/uploads-eligible (small state/reference files, not the
#       corpus) via the existing unconditional local-collection loop, including the
#       loose image/PDF exam-pattern fallback (preserved unchanged, not part of this
#       standardization).
#     Drive listing errors now HARD STOP instead of silently degrading to a local
#       scan — there is no local fallback for the corpus left to degrade to.
#   Does not touch synthesis, subtopic mapping, gate logic, or any Analysis-doc
#   generation. Verified: validate_framework_md.py (0 issues, AST-clean).
#
# v2.24.7 — 2026-07-18 — §6.2 STRUCTURAL FIX for A-INTEGRITY-FALSEPOS-01 (docs-only, zero
#   logic change). §14 SCHEMA REFERENCE's three block definitions (CATEGORY C, CATEGORY A,
#   CATEGORY B) each now carry an explicit "*** DOC-ALIAS ONLY ***" note stating the real
#   on-disk literal token adjacent to the conceptual name, and an explicit instruction to
#   never regex-match the "CATEGORY" phrase against file content. This is the same
#   authoring mistake that caused Framework_MockTestCreateAudit.md's P0.5 to HARD STOP on
#   every valid section_rules.md (fixed at v2.7.5) — the consumer spec hard-coded this
#   file's internal doc-alias instead of the literal token write_section_rules() actually
#   emits. Preventive only: no function, no on-disk format, no consumer contract changed.
#   write_section_rules() output is byte-identical. validate_framework_md.py 0 issues
#   (pre-existing O-MANDATE MANDATE-1 reference issue unrelated to and unaffected by this
#   change — flagged separately, not touched here).
#
# v2.24.6 changes: GAP ANALYSIS FIX B + FIX C — MPSC_Botany root-cause audit
#   (Framework_Gap_Analysis, Step 6 §6 HALT investigation). Closes the Step-5 half of
#   two structural defects that recur on every exam with (a) any Zero-PYQ subtopic, or
#   (b) any PASSAGE/DI subtopic, or (c) a subtopic whose stem merely CONTAINS the
#   substring "table" ("vegetable", "acceptable", ...). The Step-6 (Framework_Blueprint)
#   half — reading Format from the manifest instead of the Excel — ships as Blueprint
#   v1.32 FIX A/D/E; this is the Step-5 defense-in-depth + source hardening half.
#   WHAT CHANGED:
#     FIX B — FREQUENCY EXCEL COMPLETENESS + FORMAT PARITY (§16-1, §16-4, §15-1):
#       aggregate_frequency_data() and generate_frequency_xlsx() now accept `all_entries`
#       (the same PYQ + Zero-PYQ-scaffold list write_subtopic_manifest() writes from).
#       When supplied: (1) every all_entries subtopic seeds a Master Data row FIRST — so
#       Zero-PYQ scaffolds appear as all-zero rows, making the Excel taxonomy-complete by
#       construction, not just the manifest; (2) Format is taken directly from
#       entry['format'] (the manifest's own 4-way TEXT/FIGURAL/PASSAGE/DI value) instead
#       of being re-derived locally with a 2-way (TEXT/FIGURAL-only) image_role rule — so
#       Excel Format == manifest Format for every subtopic by construction, never merely
#       by coincidence. run_synthesise() updated to pass all_entries through. Backward-
#       compatible: all_entries=None reproduces the exact pre-v2.24.6 behavior.
#     FIX C — STRUCTURAL DI/PASSAGE TABLE DETECTION (SHARED AXIS CLASSIFIER v1.0 +
#       synthesise_subtopic): replaced the naive substring match
#       (`'|' in stem or 'table' in stem.lower()`) with a shared, single-source-of-truth
#       `_looks_like_table_stimulus()` helper — word-boundary table-keyword match
#       co-occurring with a real pipe-delimited row, or >=2 pipe-delimited rows alone.
#       Eliminates false positives on "vegetable"/"acceptable"/stray single pipes while
#       still catching real data tables. Used by BOTH classify_axis1() (the canonical
#       per-question classifier feeding axis_distribution) and synthesise_subtopic()'s
#       per-subtopic `fmt` derivation (previously two independent, driftable
#       implementations of the same rule — now one). MUST PROPAGATE (byte-identical) to
#       Step 8 MockCreateAudit S6-1b (verbatim classifier copy) — done, MockTestCreateAudit
#       v2.7.4.
#   PAIRS WITH: Framework_Blueprint v1.32 FIX A (§6 Format source: manifest, not Excel)
#   + FIX D (§2-1 Section↔Subject resolver) + FIX E (§2-3 over-coverage INFO branch).
#   Verified: master_data_completeness_test, excel_manifest_format_parity_test,
#   di_heuristic_false_positive_test design specified in Blueprint §9 S9-13 validation plan.
#
# v2.24 changes: MECHANIC / FORM-KEY ENGINE — permanent fix for the BV-10 same-mechanic
#   collision DEADLOCK CLASS (blocks Step 6 MockBlueprint on a large fraction of exams).
#   ROOT CAUSE (fixed here at source): _derive_question_mechanic() matched English-verbal
#   substring keywords only and silently fell back to the coarse concept_group for every
#   reasoning/quant/GA/regional subtopic, collapsing distinct forms (Number/Letter/Semantic
#   Series -> one "series") onto one label. BV-10 read that diversity-family label as a
#   duplicate-identity key -> arithmetically-forced, non-terminating deadlock.
#   WHAT CHANGED:
#     (1) NEW axis engine (derive_mechanic + canon_text/_has_word/_FAMILY_MAP/_QUALIFIERS):
#         word-boundary matching (no 'voice' in 'invoice', no 'clock' in 'clockwise');
#         verbal keywords GATED to verbal sections/formats; QUALIFIER-AWARE fine mechanic
#         so variants stay distinct; Devanagari/regional transliteration + subtopic_id
#         fallback so a mechanic is NEVER empty; DETERMINISTIC in (section,name) not in
#         volatile PYQ templates. Emits per subtopic: family (coarse, SOFT-cap axis) +
#         mechanic==form_key (fine, HARD-guard axis) + collision_domain (default=section).
#     (2) _derive_concept_group/_derive_question_mechanic kept as back-compat wrappers.
#     (3) question_mechanic + form_key + collision_domain now WRITTEN to the subtopic
#         MANIFEST (previously only concept_group was) and to section_rules.md, and are
#         round-tripped in rebuild_subtopic_manifest_from_section_rules().
#     (4) Zero-PYQ scaffold + _absent_entry now derive these via the engine (were slugify /
#         missing) so mixed-PYQ exams are consistent and never empty.
#     (5) NEW QV-13 quality gate: fails on empty/nondeterministic mechanic; warns on
#         intra-domain form_key collisions and question-shaped subtopic names.
#   PAIRS WITH: Step 6 B1 feasibility gate + two-tier BV-10a(HARD form_key)/BV-10b(SOFT
#   family cap) — delivered separately. Verified by step5_harness (21/21) + engine
#   extracted-from-this-file (13/13) + whole-document syntax parity.
#
# v2.24.1 changes: EXAM-INDEPENDENT fix for the BV-10a form_key-collision HALT class.
#   v2.24 collapsed family/question_mechanic/form_key onto ONE token whenever no
#   reasoning qualifier matched — always, on any subject exam — so any two subtopics
#   sharing a _FAMILY_MAP keyword (e.g. three "…Classification…" biochemistry subtopics)
#   got an identical form_key and Step 6 BV-10a HALTed two steps later. Latent in EVERY
#   single-section subject exam, not just one. WHAT CHANGED (defect report D1..D9):
#     (D1) form_key now derives from the subtopic's OWN identity base (→ unique subtopic_id),
#          NEVER the family token. Uniqueness is by construction, not by qualifier accident.
#     (D2) _FAMILY_MAP rows are (keywords, family, template_set); the keyword table fires
#          only for template_sets the exam DECLARES. _is_verbal() demoted to narrow-only.
#     (D3) collision_domain uses the collision-safe section_prefix (EC-M4).
#     (D5/D8) derive-once: mint subtopic_id → stamp_mechanic_axes() (asserts uniqueness) →
#          run_qv(), all reading the SAME stamped fields. _absent_entry/scaffold emit None
#          and are filled by the single stamp site. QV-13 is now FAIL (no allowlist); name
#          shape split to QV-13a (advisory).
#     (D7) subtopic_merges (TRUE duplicates only) replaces the retracted allowlist.
#     (D9) _extract_qualifiers() returns ALL matches, alphabetical, word-boundary-redundancy.
#   PER-EXAM INPUT: [ExamCode]_mechanic_overrides.json ONLY. Absent ⇒ legacy family
#   selection (REGR-1) + the always-on uniqueness improvement. REQUIRES Step 6 §7.1
#   (Blueprint): remove concept_group from the form_key fallback chain (now deliberately
#   shared). Verified: patched-code checks 6/6 (biochemistry unblock + EC-M1/M2/M6/M8/M17/M18).
#
# v2.24.5 changes: AUTOMATIC ZERO-PYQ FORMAT INFERENCE (no curator input). New pure
#   infer_zero_pyq_axes() + post-pass apply_zero_pyq_format_inference() refine each zero-PYQ
#   scaffold's format/answer_type/answer_cardinality from (1) NAME keywords (-> FIGURAL, same
#   heuristic as the PYQ path) and (2) same-topic PYQ siblings (UNANIMOUS non-TEXT format
#   inherited; >=2/3 NAT or MSQ inherited); else TEXT/option/single. Fires only on strong
#   evidence (name match, or >=2 unanimous/>=2-of-3 siblings); PYQ entries never touched; every
#   change logged (audit trail, no prompt). Runs before id-mint/stamp/QV/writers so section_rules
#   + manifest both carry the inferred axes; a zero-PYQ FIGURAL becomes a real Axis-1 supplier
#   (axis1_feasibility sees it, Step-7 dispatch renders it, Step-8 audits it). Proven by
#   blueprint_zero_pyq_inference_test.py.
#
# v2.24.4 changes: TAXONOMY 'How to use' WORDING FIX (docs only, no logic). The sub-topic guidance
#   now leads with the readable "Subject::Topic::Sub Topic Name" form (the Topic disambiguates
#   same-named sub-topics across topics — e.g. Kinematics under Mechanics vs Rotational Motion),
#   and clarifies the Sub Topic Id is only needed when a name repeats under the SAME topic.
#
# v2.24.3 changes: HUMAN-READABLE TAXONOMY EXPORT. New write_taxonomy_xlsx() emits
#   [ExamCode]_taxonomy.xlsx alongside subtopic_manifest.json — a plain 4-column list
#   (Subject | Topic | Sub Topic Name | Sub Topic Id, one row per sub-topic, sorted, with a
#   filterable header + a 'How to use' sheet) so the Step-6 operator can pick scope values
#   without reading JSON. Called from BOTH manifest writers (write_subtopic_manifest +
#   rebuild_...); added to deliver_final (now 6 files). Additive, generated from the same
#   manifest dict (JSON stays authoritative); openpyxl-absent → WARN, never a hard stop.
#
# v2.24.2 changes: LANGUAGE-AGNOSTIC MATCH DETECTION — closes the format-fidelity gap where
#   match-the-following questions were mis-tagged (and, downstream, mis-RENDERED as plain text
#   instead of a Word table). classify_axis2's MATCH rule relied on ENGLISH stem keywords
#   (match / list-I / column), so (a) non-English match papers and (b) matches whose List-I/
#   List-II body sits in a table (absent from stem_raw) fell through to DIRECT — silently
#   under-counting the MATCH format and producing a false readiness signal. WHAT CHANGED:
#     (1) NEW self-contained helper _opts_are_match_pairs() (+ _label_family, _MATCH_*_RE) in
#         the SHARED AXIS CLASSIFIER v1.0 block: detects a CROSS-DOMAIN label-pair OPTION shape
#         (A-I / 1-A / I-A / A-1; separators - u2013 u2014 : > arrow; bracketed or bare). Cross-
#         domain (left family != right family) rejects digit:digit ratios, coordinate pairs and
#         word-word hyphens. Column-level family resolves the roman-vs-letter 'I' ambiguity.
#     (2) classify_axis2 gains a THIRD MATCH trigger AFTER the two keyword rules — additive and
#         monotone: it can only convert a would-be non-MATCH class to MATCH, never the reverse
#         (proven over 240 stem x option x linked combinations; zero regressions).
#   MUST PROPAGATE (byte-identical) to Step 8 MockCreateAudit S6-1b (verbatim classifier copy).
#   E-8 classify_option_format left untouched (descriptive metadata, no functional coupling).
#   Verified: helper matrix 20/20 + invariant proof 240/240 + extracted-from-this-file parity.
#
# v2.23 changes: THREE-AXIS FORMAT-DISTRIBUTION EXTRACTION — SHARED AXIS CLASSIFIER +
#   PER-SECTION TARGETS + PER-SUBTOPIC CAPABILITY (File 1 of the format-fidelity feature).
#   GOAL: a mock must replicate the exam's FORMAT MIX, not just its syllabus. This step
#   extracts the targets that Steps 6/7/8 enforce. A question is a TRIPLE on three
#   orthogonal axes; each PYQ question is now tagged on all three + a negative-polarity flag.
#
#   FIX A — SHARED AXIS CLASSIFIER v1.0 (new section, before synthesise_subtopic):
#     The single, canonical, exam-agnostic classifier. Step 8 (MockCreateAudit) re-tags
#     GENERATED questions with THIS SAME classifier — if the two ever diverge, every
#     distribution number is silently wrong, so it is authored ONCE here and referenced,
#     never re-implemented. It exposes:
#       • classify_axis1(q) → TEXT|FIGURAL|PASSAGE|DI          (STIMULUS / MEDIA)
#       • classify_axis2(q) → the EXCLUSIVE 8-class ladder     (STEM STRUCTURE)
#             LINKED (gate, decided by linked_group_id — shared stimulus serving 2+ Qs,
#             NOT by phrasing) → ASSERTION_REASON → MATCH → SEQUENCE → STATEMENT →
#             FILL_BLANK → ODD_ONE_OUT → DIRECT  (first-match-wins; SEQUENCE deliberately
#             above STATEMENT because the OPERATION is ordering). DIRECT is the residual.
#       • classify_axis3(q) → MCQ|MSQ|NAT                      (ANSWER MECHANISM)
#       • negative polarity is an ORTHOGONAL FLAG (is_negative), never an Axis-2 class:
#             "which pair is NOT correctly matched" = MATCH + is_negative, so counts stay clean.
#     Consolidates the pre-existing independent detectors (EC-8 A-R, EC-9 statement-combo,
#     EC-11 fill-blank, EC-12 negative, EC-13 matching) into ONE exclusive partition, and
#     adds SEQUENCE + ODD_ONE_OUT (narrowed to true "does not belong" classification).
#
#   FIX B — PER-QUESTION TAGGING: the extraction driver now calls tag_axes(q) in the
#     per-question enrichment loop (after linked_group_id + image_role are known), so
#     every question carries q['axis1'|'axis2'|'axis3'] alongside is_negative.
#
#   FIX C — PER-SUBTOPIC CAPABILITY (CATEGORY B): synthesise_subtopic now emits
#       • observed_axis2      — {AXIS2_CLASS: count} this subtopic's PYQ actually used
#       • presentation_family — the family key (mirrors Step 7 resolve_presentation_family)
#       • axis2_capability    — the forms this subtopic may FAITHFULLY take = observed ∪
#             family-menu ∪ {DIRECT} (+LINKED iff format ∈ PASSAGE/DI, since LINKED is
#             stimulus-locked). Step 6 reads this to guarantee rare-format reachability
#             (decision (c)); Step 7 renders only within capability (fabrication banned).
#
#   FIX D — PER-SECTION AXIS_DISTRIBUTION (CATEGORY A): new section-header block, the
#     3-YEAR per-paper averages of each Axis-1/2/3 class + the negative rate, computed by
#     compute_section_axis_distribution() over the 3 most-recent distinct years. Each
#     Axis-2 class carries an audit_mode ∈ {band, guarantee, float}: DIRECT always floats;
#     window_target = per_paper_avg × mocks_per_window; window_target < 1 → guarantee-only
#     (periodic ≥1/window), else band. Written to section_rules.md AND subtopic_manifest.json;
#     the rebuild-from-section_rules path parses it back (round-trip preserved).
#
#   framework_version stamp: v2.23. Steps 6/7/8 are Files 2–4 of this feature (separate turns).
#
# v2.22 changes: INHERENTLY-VISUAL SUBTOPIC DETECTION + MANIFEST inherently_visual FLAG.
#   ROOT CAUSE: Step 5 classifies format purely from PYQ observation: format='FIGURAL'
#   iff any question's image_role != 'none'. When PYQ image extraction fails (scanned
#   PDF, embedded-as-raster, missing media), inherently-visual subtopics like counting
#   figures, embedded figures, or mirror images are misclassified as format='TEXT'.
#   Step 7 then generates unanswerable text descriptions of figures students cannot see.
#
#   FIX A — KEYWORD HEURISTIC in synthesise_subtopic() (zero external dependency):
#     After the PYQ-based format assignment, if fmt == 'TEXT', a VISUAL_KEYWORD set is
#     checked against the subtopic name. If the name signals visual content (e.g.,
#     contains 'figure', 'diagram', 'mirror', 'venn', 'paper fold', etc.), fmt is
#     overridden to 'FIGURAL' and a default image_role of 'stem_only' is assigned.
#     The override is LOGGED: "INHERENTLY-VISUAL override: [subtopic] TEXT→FIGURAL."
#     The keyword set is exam-agnostic — it covers geometric/spatial/visual terms
#     universal across competitive exams. If a keyword match is wrong, the exam
#     curator can add figural_override=false in the taxonomy entry to suppress it.
#
#   FIX B — inherently_visual FLAG in subtopic manifest:
#     write_subtopic_manifest() now includes 'inherently_visual': true|false per entry.
#     Set true when Fix A fires, or when the entry has an explicit figural_override=true.
#     Downstream steps (Step 7 S3-2, Step 8) can read this flag directly from the manifest.
#
#   framework_version stamp: v2.22.
#
# v2.21 changes: DELIVERY FOOTER CROSS-REFERENCE.
#   Added S11-4: post-delivery footer rendering reference to Framework_DeliveryFooter.md
#   v1.3. Both per-batch (F1 mid-step) and final (F2 step-complete) deliveries now render
#   the standardized visual footer after every present_files call. Zero logic change.
#   framework_version stamp: v2.22.
#
# v2.20 changes: ZERO-PYQ MANIFEST COMPLETENESS FIX (Fix A + Fix C from BUGFIX report).
#   ROOT CAUSE: Step 5's manifest represented only PYQ-OBSERVED subtopics, not the COMPLETE
#   exam vocabulary. Exams whose syllabus defines subtopics with zero PYQ observations
#   (new syllabus additions, rarely-tested topics, etc.) produced an INCOMPLETE manifest.
#   Step 6 (Blueprint) then self-minted sequential IDs for these orphan subtopics (violating
#   the never-mint contract), and Step 7 (MockCreate) correctly HARD STOPPED at S3-8 because
#   the self-minted IDs existed in neither the manifest nor section_rules.
#   Discovered: SSC CGL Tier 2, Mock 1 — 7 syllabus-only subtopics absent from manifest.
#   This is the COMMON CASE for any exam with syllabus-defined topics that have no PYQ history.
#
#   FIX A — TAXONOMY SYNC PROTOCOL (new §15-1):
#     After PYQ-based synthesis completes, run_synthesise() now synchronises the entry list
#     with the exam's approved taxonomy. For every taxonomy-defined subtopic NOT already in
#     the PYQ-derived entries, a SCAFFOLD ENTRY is created with zero-PYQ defaults (observed_
#     count=0, confidence='absent', generic P1 pattern, all difficulty counts=0). These
#     scaffold entries flow through the normal write_section_rules() and write_subtopic_
#     manifest() paths, so the manifest and section_rules are COMPLETE by construction.
#     Taxonomy sources: (1) [ExamCode]_taxonomy_draft.json (primary — syllabus-faithful,
#     contains zero-PYQ subtopics), (2) approved Analysis doc [ExamCode]_PYQ_Analysis.docx
#     (additional — union, covers PYQ-discovered subtopics not in taxonomy_draft).
#     Edge cases EC-ZP-1 through EC-ZP-10 documented in §15-1.
#
#   FIX C — SCAFFOLD SECTION_RULES BLOCKS:
#     New make_zero_pyq_scaffold_entry() function produces a complete entry dict with all
#     fields format_entry() expects, using zero-PYQ defaults. The resulting section_rules
#     block carries observed_count=0, a generic P1 stem pattern with confidence='absent',
#     zero difficulty calibration, and a NOTE identifying it as a syllabus-only subtopic.
#     Step 7 uses these blocks for format/option guidance when generating zero-PYQ questions.
#
#   COMPLETENESS INVARIANT (new, added to §15):
#     len(manifest_subtopics) >= len(taxonomy_subtopics)
#     The manifest must cover the ENTIRE taxonomy, not just the PYQ-observed subset.
#     A PYQ-only manifest is a PARTIAL vocabulary that will break when the blueprint
#     includes syllabus-only subtopics. Taxonomy sync makes this hold by construction.
#
#   VALIDATION:
#     run_synthesise() logs taxonomy sync additions and prints a summary count.
#     New DoD items [22] and [23] verify taxonomy sync ran and completeness invariant holds.
#
#   framework_version stamp: v2.20. All generated_by stamps: v2.20.
#
# v2.19 changes: BATCH STOP LAW HARDENING + CLOSED DELIVERABLE SET CONTRACT.
#   ROOT CAUSE 1 — BATCH STOP: S8-1 had strong language (★★★ CRITICAL RULE ★★★,
#     explicit refusal script, accepted triggers) but lacked two elements proven
#     critical in PYQAnalyse SSC CGL Tier 2 failure: (a) prose-level "END THE
#     RESPONSE" instruction outside code blocks, (b) documented failure history.
#     The Python `break` stops the loop but doesn't stop Claude from writing
#     additional content after the loop. Added both elements to S8-2 and S8-3.
#
#   ROOT CAUSE 2 — DELIVERABLE SET: header OUTPUT FILES listed only 3 files but
#     actual final delivery (S11-2 PART B) is 6 files (subtopic_manifest.json + taxonomy.xlsx (v2.24)
#     added v2.14, PYQ_Frequency.xlsx added v2.13). No "NOTHING ELSE" qualifier,
#     no DO-NOT-DELIVER list, no pre-delivery checklist. Same gap pattern as
#     PYQAnalyse (unauthorized taxonomy_draft_v2.json delivery).
#
#   CHANGES:
#     (1) S8-2: added "END THE RESPONSE" prose block after `break` with
#         cross-framework failure reference (PYQAnalyse SSC CGL Tier 2).
#     (2) S8-3: added "END THE RESPONSE" instruction after continue prompt.
#     (3) Header OUTPUT FILES: updated to list all 5 final files + per-batch
#         file, with "(nothing else)" qualifiers and DO-NOT-DELIVER list.
#     (4) New S11-3: DELIVERABLE SET CONTRACT — closed sets for per-batch
#         (1 file) and final (5 files) deliveries, with DO-NOT-DELIVER lists
#         and pre-delivery checklist.
#     (5) DoD: 4 new items for closed-set verification.
#
#   framework_version stamp: v2.19.
#
# v2.18 changes: EXAM_CONFIG MARKING_SCHEME INTEGRATION (Step 2a v2.5 contract sync).
#   Root cause: Step 2a v2.5 replaced scalar marks_per_question/negative_marking with
#   per-range marking_scheme[] and added medium, level, question_types to exam_config.json.
#   Step 5 must read these new fields and propagate them to _meta, CATEGORY C, and
#   section_rules.md so downstream Steps 6-11 consume them correctly.
#
#   CHANGE 1 — PARAMETER SOURCE PRIORITY:
#     All PARAMETERs that previously read from "Exam Pattern document" (via AI interpretation)
#     now read from exam_config.json FIRST (structured, deterministic). AI detection from
#     PYQ papers becomes VALIDATION ONLY — if PYQ-detected value conflicts with exam_config,
#     exam_config wins and a warning is logged.
#     Affected: PARAMETER 1 (time_per_q_sec), PARAMETER 2 (negative_marking),
#       PARAMETER 3 (language — new: medium from exam_config takes priority),
#       PARAMETER 5 (question_types), PARAMETER 6 (marks_per_question).
#
#   CHANGE 2 — PARAMETER 6 DERIVATION FROM marking_scheme[]:
#     marks_per_q is now derived from exam_config.marking_scheme[] by grouping ranges
#     by question_type and taking the MAX correct_marks per type. Example:
#       GATE marking_scheme has MCQ ranges at 1m and 2m → marks_per_q['MCQ'] = 2.
#       CSIR NET has MCQ ranges at 2m and 4m → marks_per_q['MCQ'] = 4.
#     This preserves backward compatibility with the dict format Steps 7/8/9 expect.
#     negative_marking_by_type similarly derived: per type, take the MIN (most negative).
#
#   CHANGE 3 — NEW _META FIELDS:
#     marking_scheme, level, medium stored in progress['_meta']. Propagated to
#     exam_meta dict in run_synthesise and written to CATEGORY C header.
#
#   CHANGE 4 — CATEGORY C HEADER EXPANSION:
#     write_section_rules now writes: marking_scheme, level, medium.
#     marks_per_q and negative_marking RETAINED as summary scalars for backward compat
#     (derived from marking_scheme). Downstream Steps 7/8/9 can read either the scalar
#     (legacy) or the full marking_scheme (new) via cat_c().
#
#   CHANGE 5 — §14 SCHEMA REFERENCE updated with new CATEGORY C fields.
#
#   framework_version stamp: v2.18.
#
# v2.17 changes: FREQUENCY XLSX ACCURACY & COMPLETENESS OVERHAUL (9 fixes).
#   Root cause: Comparative analysis of framework-generated xlsx vs manually-verified
#   PYQ analysis for MPPSC Botany revealed: 38% data loss (93/150 Qs mapped), inflated
#   percentages (denominator = mapped Qs not exam total), binary importance (useless),
#   missing question numbers, missing coverage validation. All traced to §16 xlsx code.
#
#   FIX-1 [CRITICAL]: % OF SUBJECT DENOMINATOR — write_master_data, write_topic_analysis,
#     and write_section_sheet all used section_totals (sum of MAPPED questions) as
#     denominator. For exams where classification drops questions, this inflates all
#     percentages. FIXED: generate_frequency_xlsx now reads exam_config.json to get
#     exam_total_questions (the REAL exam total per section from the pattern). All %
#     calculations use exam total as denominator. Fallback: if exam_config absent,
#     use section_totals (current behaviour) with a warning.
#
#   FIX-2 [CRITICAL]: COVERAGE VALIDATION — new XLSX-F9 check: sum of all subtopic Qs
#     across all sections must equal total_questions from exam_config. If mismatch > 5%,
#     WARN: "Frequency xlsx accounts for [N] Qs but exam has [M]. [M-N] questions were
#     not classified to any subtopic. Downstream blueprint will be inaccurate."
#     This single check would have caught the MPPSC 93≠150 bug.
#
#   FIX-3 [HIGH]: TOPIC NAME CONSISTENCY — write_topic_analysis topic names must be
#     IDENTICAL to write_master_data topic names. Added assertion: every topic in Topic
#     Analysis sheet must exist verbatim in Master Data Subject column. Prevents the
#     truncation mismatch bug (e.g., "Molecules...Biolog" vs "Molecules...Relevant").
#
#   FIX-4 [HIGH]: DUPLICATE SUBTOPIC DETECTION — generate_frequency_xlsx now checks for
#     duplicate (section, topic, subtopic) keys before writing. If found, WARN and merge.
#
#   FIX-5 [MEDIUM]: MUST_PREPARE NULL HANDLING — empty string '' replaced with '—' for
#     non-Must-Prepare subtopics. Prevents NaN in downstream consumers.
#
#   FIX-6 [MEDIUM]: NEAR-DUPLICATE SUBTOPIC WARNING — after aggregation, check for
#     subtopic name pairs within same topic with >75% similarity. Print warning.
#     Aligns with Framework_PYQAnalyse v2.4 Unique Domain Property checks.
#
#   FIX-7 [LOW]: SINGLE-YEAR TREND/CONSISTENCY — for exams with only 1 year of data,
#     Trend is now 'N/A (1 year)' instead of 'Insufficient Data', and a note is added
#     to Summary Dashboard explaining that trend/consistency columns are not meaningful.
#
#   FIX-8 [LOW]: SECTION NAME IN TOPIC ANALYSIS — Topic Analysis sheet now uses full
#     section name (no truncation). Section names in Master Data and Topic Analysis
#     must be byte-identical.
#
#   FIX-9 [LOW]: SUMMARY DASHBOARD HEADER — now includes exam_code from exam_config
#     (not from ExamCode parameter which could have typos). Uses exam_config['exam_name']
#     if available for human-readable title.
#
#   framework_version stamp: v2.17. All generated_by stamps: v2.17.
#
# v2.16 changes: EXAM-AGNOSTIC RIGIDITY AUDIT (6 fixes).
#   RIGID-1 [CRITICAL]: "Shift" hardcoded in 3 regex patterns — parse_shift(),
#     extract_shift_from_filename(), sort_papers_recency_first(). IBPS (Slot), RRB (Phase),
#     GATE (Session) PYQ filenames had their session number silently ignored (always 'S1').
#     FIXED: session_keyword now read from exam_config.json at session start (matching
#     PYQSort's contract). All shift/session regexes built dynamically via
#     build_session_re(). Fallback: 'Shift' when exam_config absent.
#   RIGID-2 [CRITICAL]: Language detection only checked ASCII vs Devanagari (U+0900-097F).
#     Regional exams in Tamil, Telugu, Bengali, Kannada, Malayalam, Gujarati, Odia, Punjabi
#     would all classify as 'english'. FIXED: INDIC_RANGES expanded to cover all 9 major
#     Indic scripts. language now detects 'regional' when any non-Devanagari Indic script
#     dominates. Marathi (Devanagari script) correctly maps to 'hindi' with a NOTE.
#   RIGID-3 [IMPORTANT]: Display strings hardcoded "Shift-[N]" in verification summary,
#     detection sample printout, and sort docstrings. FIXED: all use session_keyword variable.
#   RIGID-4 [IMPORTANT]: parse_taxonomy_level() only recognized Subject/Domain/Topic/Chapter.
#     Exams using Unit/Module/Section/Part/Block/Area as PYQ headings collapsed to level 3.
#     FIXED: 12+ heading patterns now recognized for level 1 and level 2.
#   RIGID-5 [MODERATE]: determine_strip_mode() used English-only section/topic keywords.
#     Hindi-medium exams with headings like "गणित"/"तर्कशक्ति" always fell to default.
#     FIXED: Hindi equivalents added for quantitative/reasoning/english/factual detection.
#   RIGID-6 [MODERATE]: NOTE_PAT only matched English + Hindi NOTE keywords. Regional
#     script NOTE blocks (Tamil குறிப்பு, Telugu గమనిక, Bengali দ্রষ্টব্য, etc.) missed.
#     FIXED: 9 regional-language NOTE keywords added to NOTE_PAT.
#   framework_version stamp: v2.16. All generated_by stamps: v2.16.
#   CROSS-STEP SYNC FIXES (found during final sync audit):
#     SYNC-1: _read_session_keyword() used fixed path '/mnt/project/exam_config.json'
#       but PYQAnalyse saves it as '{ExamCode}_exam_config.json' and PYQSort discovers
#       via glob('*_exam_config.json'). FIXED: now uses same glob pattern.
#     SYNC-2: is_shift_tag() and is_taxonomy_heading() used \d{2} (exactly 2-digit day)
#       for date label detection, but real PYQ dates can have single-digit days (e.g.
#       [5-Jan-2024]). PYQAnalyse correctly uses \d{1,2}. FIXED: all 4 occurrences now
#       use \d{1,2} — aligned with PYQAnalyse.
#     SYNC-3: Stale generated_by stamp v2.15 in rebuild_subtopic_manifest_from_section_rules
#       (missed in bulk v2.16 update). FIXED: now v2.16.
#
# v2.15 changes: DEEP-AUDIT-2 (13 bugs fixed).
#   BUG-D01 [CRITICAL]: generate_frequency_xlsx() was never called in run_synthesise() —
#     the entire §16 xlsx feature was dead code. FIXED: run_synthesise() now calls it and
#     passes xlsx_path to deliver_final().
#   BUG-D02 [CRITICAL]: deliver_final() had no xlsx_path parameter — xlsx never delivered.
#     FIXED: xlsx_path added to signature and delivery list.
#   BUG-D03 [CRITICAL]: per-section option_label_format read from option FORMAT TYPE
#     ('single_value') instead of option LABEL style ('1/2/3/4' vs 'A/B/C/D'). FIXED:
#     extraction now detects and stores option_label per question; per-section writer
#     aggregates from the correct field.
#   BUG-D04: stale comment version v2.12 → v2.15 (line 2621 in v2.14).
#   BUG-D05: stale generated_by stamps v2.11 → v2.15 in manifest writers.
#   BUG-D06: self-referencing "Step 0" in handoff/DOD → canonical "Step 5".
#   BUG-D07: option_label_format auto-detection implemented in S1-3 (was documented
#     but never coded — always defaulted to '1/2/3/4').
#   BUG-D08: dead code removed from aggregate_frequency_data (str(tuple).startswith('_')).
#   BUG-D09: must_prepare threshold now scales with available years
#     (>= min(4, len(all_years)) instead of fixed >= 4).
#   BUG-D10: _compute_structural_changes deduplication — FIGURAL subtopics no longer
#     produce both REMOVED and FIGURAL-eliminated entries.
#   BUG-D11: §12 integration section updated to canonical step numbers.
#   BUG-D12: docstring schema example updated to v2.15.
#   BUG-D13: extract_year_from_filename documented as accepting name string only.
#   framework_version stamp: v2.15. All generated_by stamps: v2.15.
#
# v2.14 changes: DEEP-AUDIT (1 fix). framework_version stamp in write_section_rules was
#   v2.12 — missed the v2.13 bump. Every section_rules.md generated under v2.13 would say
#   framework_version: v2.12 instead of v2.13. FIXED: stamp now reads v2.14. No behaviour
#   change; output is byte-identical except the version string in the EXAM_STRUCTURE header.
#
# v2.13 changes: FREQUENCY XLSX OUTPUT — adds [ExamCode]_PYQ_Frequency.xlsx as a new
#   synthesis-phase output. The xlsx contains year-wise question frequency data for every
#   subtopic: per-year counts, avg/paper, consistency, trend (Rising/Declining/Stable),
#   importance (High/Medium/Low), must-prepare flags, rank-in-topic, and format classification.
#   8 sheets: Summary Dashboard, Master Data, Topic Analysis, Trend Analysis, + 1 per section.
#   All data aggregated from analysis_progress.json (no new extraction needed). All derived
#   metrics are deterministic formulas. Downstream consumer: Step 6 (MockBlueprint) reads
#   this xlsx as its "Frequency Excel" input alongside Analysis docs. 8-item xlsx validation
#   checklist (XLSX-F1 through XLSX-F8). 6 edge cases (EC-F1 through EC-F6). New output added
#   to §11 delivery list and DEFINITION OF DONE. Implementation in §16.
#
# v2.12 changes: DIFFICULTY LABEL VOCABULARY (Question Metadata Index — Step-0 half).
#   Adds difficulty_labels to the EXAM_STRUCTURE (CATEGORY C) header block written to
#   section_rules.md — the CANONICAL, exam-overridable difficulty vocabulary that becomes the
#   stored/rendered Complexity tag in the new per-question registry.question_index (seeded by
#   Step 1, filled by Step 2, certified by Step 3, rendered by Step 6). Default
#   ['Easy','Medium','Hard']; an exam may override (e.g. a 2- or 5-band set). Documents the
#   fixed alias between the three pre-existing difficulty spellings — Step-0 calibration
#   Simple/Medium/Hard, Step-1 schedule count keys simple/medium/hard, canonical label
#   Easy/Medium/Hard: simple→Easy, medium→Medium, hard→Hard. NO analysis behaviour changes:
#   difficulty_labels is written with its default and the PYQ_DIFFICULTY_CALIBRATION path is
#   untouched, so a non-overriding exam's section_rules is byte-identical apart from the one new
#   header line. Also corrects two stale embedded version literals (v2.10→v2.12) in
#   write_section_rules so the generated file's framework_version tracks the spec. Part of the
#   cross-step Question Metadata Index contract (Contract_QuestionMetadataIndex v1.0). Validated:
#   field write + default + alias proven in the Phase-1 harness before encoding.
#
# v2.11 changes: ISSUE 2b — THREE MANDATE TYPES a flat per-id list cannot express.
#   mandatory_every_mock (v2.10) only says "this ONE id in EVERY mock". Real exams also
#   need: (a) GROUP-PRESENCE — "≥1 of a subtopic GROUP per mock" (e.g. any one 3D-mensuration
#   solid, where forcing all members would over-allocate); (b) PER-WINDOW CADENCE — "≥1 every
#   N mocks" (e.g. an every-alternate-mock topic); (c) MIN-COUNT — "≥k Q of this subtopic per
#   mock" (e.g. a two-question argument/ethical requirement). v2.11 makes all three DATA,
#   round-trippable through section_rules exactly like the v2.10 mandate fields:
#     • format_entry emits two more per-block lines — mandatory_group (group name) and
#       min_count (int). min_per_series_window (the cadence field) already round-tripped since
#       v2.10; it is now ROLLED UP and enforced downstream rather than inert.
#     • write_subtopic_manifest + rebuild_subtopic_manifest_from_section_rules collect three
#       new top-level manifest structures: mandatory_groups {group:{members:[ids],min}},
#       cadence_windows {id:N}, min_counts {id:k}, plus mandatory_group/min_count on each
#       subtopic's mandates block.
#   ENFORCEMENT SPLIT (documented for Step 1/2; encoded there separately): group-presence and
#   min-count are per-mock (Step 1 places them, Step 2 S3-17 verifies + gates); CADENCE is a
#   CROSS-mock constraint (Step 1 sliding-window rule only — Step 2 sees a single mock and
#   cannot verify it). All checks validated in Python (group/cadence/min-count) before encoding.
#   Exam-agnostic: empty config ⇒ every new structure empty ⇒ vacuous no-op, never a false stop.
#
# v2.10 changes: MANDATE ROUND-TRIP FIX — the subtopic_manifest is now reproducible
#   from section_rules.md ALONE. ROOT CAUSE: alternation_groups and min_per_series_window
#   were read ONLY from ephemeral in-memory entry fields (e['alternation_group'] etc.);
#   they were never emitted into section_rules and never parsed back, so a manifest
#   rebuilt from an existing section_rules file lost ALL alternation + cadence data. And
#   the mandatory_every_mock detector was a brittle single-sentence, "mock"-only regex
#   that missed real NOTE wording like "MANDATORY ... 1Q per every paper". On SSC CGL T1
#   this produced mandatory_every_mock=[2 subtopics] and alternation_groups={} — the empty
#   mandate data that let Step 1 place CI+SI together and omit Direction Sense / Address
#   Matching. FIX (exam-agnostic): (1) format_entry now EMITS three round-trippable mandate
#   lines per subtopic block — mandate_every_mock / alternation_group / min_per_series_window;
#   (2) mandatory detection robustified to _mandate_from_note() (NOTE mentions MANDATORY
#   *and* an every/per mock|paper phrase, sentence-independent), with an explicit
#   mandate_every_mock line taking precedence; (3) NEW rebuild_subtopic_manifest_from_
#   section_rules() reconstructs a COMPLETE manifest from the section_rules file alone
#   (no source PYQ needed) — the supported path to regenerate a missing/incomplete manifest,
#   and it WARNs on any id-less block that cannot be joined. Validated in Python against the
#   real SSC section_rules (Direction Sense minted mandatory; ci_si alternation group formed)
#   BEFORE encoding. OUT OF SCOPE (Issue 2b, needs NEW manifest fields): group-presence
#   mandates ("≥1 of a 3D-mensuration group per mock"), per-window cadence, and min-count
#   mandates — a flat per-id mandatory_every_mock cannot model them.
# Multi-round audited: all known bugs fixed (v1.0 through v2.2).
# v2.2 changes: BATCH_SIZE=3 strictly prohibited from being overridden (§8-1);
#   minimum year coverage upgraded from 3 years to MANDATORY 5 years (§1-6);
#   both rules explicitly marked non-negotiable with zero exceptions when PYQ available.
# v2.3 changes: Fully exam-agnostic — all hardcoded exam names/folder IDs removed from
#   examples and comments. §13 PROOF section retained as it is explicitly illustrative.
#   BUG-C01 fix: PYQ_DIFFICULTY_CALIBRATION now writes is_inferred flag per level.
#   BUG-C02 fix: years list + raw_count now written per PYQ_STEM_PATTERN (QV-11 needs it).
#   BUG-C04 fix: option_format written as full dict (BUG-B15 compliance: primary,
#     recent_format, changed_recently, all_observed) — not collapsed to single string.
#   BUG-C05 fix: paragraph_count and topic_domains now written in PYQ_PASSAGE_STRUCTURE.
#   BUG-C07 fix: QV-5b added — fixed_set type must have non-empty fixed_option_texts.
#   NEW: EXAM_STRUCTURE header block auto-written to section_rules.md (new CATEGORY C).
# v2.4 changes: SUBTOPIC_ID CONTRACT (cross-step architectural fix). Step 0 is now the
#   SINGLE SOURCE OF TRUTH for the subtopic vocabulary. Every subtopic gets a stable,
#   deterministic subtopic_id (minted by make_subtopic_id/slugify), written as the first
#   field of each --- Subtopic: --- block AND into a new machine-readable manifest
#   [ExamCode]_subtopic_manifest.json. Step 1 and Step 2 join on subtopic_id, never on
#   display-name string-match. This permanently eliminates the Step0/Step1 name-drift that
#   caused Step 2 join failures (~70% name mismatch on SSC CGL T1). See §15 for the contract.
#   NEW: STRUCTURAL_CHANGES_BY_YEAR block computed from PYQ data and written.
#   NEW: figural_banned flag per section computed from observed PYQ r_avg data.
#   NEW: max_per_paper + typical_per_paper per subtopic (Step 2 L3 ceiling source).
#   NEW: recycled_datasets detection added to PYQ_CONTEXT_POOL.
#   NEW: §14 CATEGORY C documented for exam-level header fields.
#   NEW: Auto-detected params (time/marks/options/language) stored in _meta + written.
#
# v2.5 changes: MSQ CONTRACT — DETECTION LAYER (cross-step MSQ extension, Step 0 half).
#   The whole MSQ path is DORMANT behind multi_select_allowed (default false): for any
#   exam without multi-select (SSC CGL, NEET, IBPS, UPSC, CAT, …) v2.5 behaves byte-for-
#   byte like v2.4. Changes activate ONLY when multi_select_allowed=true (e.g. GATE).
#   ROOT-CAUSE FIX (EC-A): the v2.4 is_msq detector (r'select all|which.*are correct')
#     FALSE-MATCHED statement-combination MCQs (EC-9, "Which is/are correct? 1.Only A …"),
#     which are single-answer. v2.5 keys MSQ detection on OPTION SHAPE (combo-label
#     options ⇒ NOT MSQ), a provenance-proof signal, not stem wording. Empirically
#     validated against real docx fixtures (both directions) before encoding.
#   NEW (answer_cardinality): per-subtopic answer_cardinality ∈ {single, multi} is the Step 2 dispatch
#     unit (CATEGORY B). A subtopic is uniformly single- or multi-answer (whole-subtopic
#     mode) — so the per-mock allocation schema needs NO change downstream. msq_freq% also
#     written. Per-question is_msq retained on the record.
#   NEW (k contract): msq_k_mode ∈ {fixed, variable} and msq_k captured from the Exam
#     Pattern doc (NOT from PYQ — PYQ has no answer key, so k is unextractable; documented).
#   NEW (marking): negative_marking_by_type + partial_credit captured into EXAM_STRUCTURE
#     (consumed later by Step 4; dormant now). MSQ usually carries no negative marking.
#   NEW (difficulty): E-9 score_difficulty adds an MSQ cognitive-load term (+1, analogous
#     to the negative_question term) — independently evaluating every option is strictly
#     harder. Step 3 B-DIFF mirrors this. Cascades into Step 1 difficulty allocation.
#   CHANGED (EC-7): rewritten — Step 2 now GENERATES MSQ per the answer_cardinality contract
#     (was: "Step 2 skips MSQ subtopics"). EC-A documents the statement-combination guard.
#   All MSQ fields are exam-discovered/config-driven — zero exam names hardcoded.
#
# v2.8 changes: NAT DETECTION LAYER (Numerical-Answer-Type; cross-step NAT extension,
#   Step 0 half). Adds the SECOND answer-type axis to the unified vocabulary: per-subtopic
#   `answer_type` ∈ {option, numerical}, orthogonal to answer_cardinality. A subtopic resolves
#   to 'numerical' (NAT) when nat_allowed (PARAMETER 11, from the exam pattern) AND a majority
#   of its observed Qs have ZERO selectable options — no text options and no option-images
#   (image_role none|stem_only, never options_only|stem_and_options, so a figural NAT with a
#   problem diagram counts but a figural MCQ does not). New PARAMETER 11 captures the answer
#   model from the exam pattern (nat_answer_type ∈ {integer, real}, nat_tolerance, parametric
#   nat_instruction) — value/tolerance are answer-key info and so, like msq_k, come from the
#   pattern, never from PYQ. section_rules now carries answer_type + nat_freq per subtopic
#   (CATEGORY B) and nat_allowed / nat_present / nat_answer_type / nat_tolerance / nat_instruction
#   in EXAM_STRUCTURE — wiring the Explain step's explicit answer_type resolution path. NAT
#   marking reuses negative_marking_by_type under the 'NAT' key (additive). FULLY DORMANT:
#   default answer_type='option', nat_allowed=false ⇒ the NAT fields are inert defaults and
#   downstream behaviour is byte-for-byte the v2.7 behaviour for every non-NAT exam. Validated:
#   AST clean; dormancy + detection parity proven on synthetic single-answer / MCQ / NAT inputs.
#   framework_version stamp v2.7 → v2.8.
#
# v2.7 changes: VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Part of the
#   cross-step move to ONE canonical answer-type vocabulary (answer_type + answer_cardinality)
#   shared by Steps 0-4, so the Explain step's contract and the Create/Audit steps stop using
#   different names for the same concept. This phase is a PURE RENAME with NO behaviour change:
#     • per-subtopic `answer_mode` -> `answer_cardinality` (identical {single,multi} values),
#       written to section_rules CATEGORY B under the new field name.
#   Non-NAT exams are byte-identical to v2.6. Readers downstream accept the old field name as a
#   fallback (existing section_rules files keep working). Validated: AST clean; the MSQ
#   generation/audit behaviour is unchanged (proven via the cross-step e2e harness on both
#   old-name and new-name artefacts). framework_version stamp v2.6 -> v2.7.
#
# v2.6 changes: MSQ AOTA POLICY FLAG (completes D5; closes the only open cross-step item
#   from the MSQ extension). Adds msq_allow_aota (bool, default false) to EXAM_STRUCTURE so
#   the "All of the above under MSQ" policy is actually SETTABLE — v2.5 read it everywhere
#   with a default of false but provided no place to write it, so the flag could only ever
#   be false. Now: PARAMETER 10 documents detection from the Exam Pattern; the EXAM_STRUCTURE
#   writer emits `msq_allow_aota: <bool>` into section_rules.md; the exam_meta dict and the
#   meta_raw reader carry it; §14 schema documents it; the auto-detected-params display
#   surfaces it. Step 2 (R-MSQ-ESCAPE / G-MSQ-SET) and Step 3 (A-MSQ-KEY) already read it
#   directly from section_rules, so no further downstream change is needed. Fully DORMANT
#   when multi_select_allowed=false (default false ⇒ byte-identical to v2.5 for every
#   single-answer exam). Writer framework_version stamp bumped v2.5 → v2.6. Zero exam names
#   hardcoded.
#
# PURPOSE:
#   Read actual PYQ (Previous Year Question) papers in docx format.
#   Extract per-subtopic question patterns, templates, difficulty calibration,
#   wrong option structure, and format rules.
#   Write [ExamCode]_section_rules.md — the pattern reference Step 2 uses
#   to generate questions indistinguishable from real PYQ.
#
# PIPELINE POSITION (CANONICAL step numbers):
#   Step 5 PYQExtract  (parallel) ↘
#                                  → Step 7 → Step 8 → Step 9 → Step 10 → Step 11
#   Step 6 MockBlueprint (parallel) ↗
#
#   Steps 5 and 6 are PARALLEL prerequisites for Step 7.
#   Both run in [ExamCode] project (exam-specific).
#   Both deliver outputs as downloadable files — user manually uploads to [ExamCode] project.
#   Step 5 and Step 6 do NOT depend on each other.
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   E-1 through E-11 define universal extraction operations.
#   Content discovered differs by exam — from the PYQ papers.
#   Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT, regional exams.
#
# INPUTS:
#   Scenario A — PYQ available (normal case):
#     Provided via: PYQ: <<Google Drive folder link>>  in trigger
#     Claude scans the folder recursively — any subfolder structure works.
#     Folder name, Drive account, subfolder names: all irrelevant.
#     Only .docx files are collected; everything else is ignored.
#     OPTIONAL: Exam Pattern document in project knowledge or uploads
#               (image/PDF/docx — used to detect time/Q, marks/Q, Q-types)
#
#   Scenario B — PYQ not available for this exam:
#     No PYQ: link in trigger. No .docx files in uploads.
#     MANDATORY: Analysis Word docs in project knowledge (same as Step 1)
#     Result   : All subtopics written as confidence='absent' in section_rules.md
#                Step 2 uses Claude training knowledge for pattern generation
#
#   NO CONFIG FILE REQUIRED: all parameters auto-detected from documents.
#
# TRIGGER FORMAT:
#   Step 5: PYQExtract PYQ: <<Google Drive Link>>       -- process PYQ from Drive (required)
#   Step 5: PYQExtract --status                          -- show progress dashboard
#   Step 5: PYQExtract --synthesise ALL                  -- re-synthesise only
#   Step 5: PYQExtract ... [--frequency-scope all|current-era]   -- v2.26, default 'all'
#
#   --frequency-scope all          DEFAULT. Every paper counts toward the frequency
#                                  numbers. Identical to pre-v2.25 behaviour.
#   --frequency-scope current-era  Only papers matching the CURRENT exam pattern feed the
#                                  Frequency xlsx and the axis distribution. The question-
#                                  pattern library, section_rules.md and the taxonomy still
#                                  consume EVERY era. Use when the corpus spans more than
#                                  one pattern and the subject MIX matters more than sample
#                                  depth. Requires exam_config; HARD STOPS if no paper in
#                                  the corpus matches the current pattern.
#
#   Trigger matching is case-insensitive.
#   ExamCode read from exam_config.json in project knowledge (set during Step 2a PYQDraft).
#
#   PYQ parameter (REQUIRED — v2.24.8, standardized with Step 4/Step 2b):
#     PYQ: <<Google Drive folder link>>
#     Link can point to:
#       • A flat folder (all docx files directly inside)
#       • A folder with year subfolders (2019/, 2020/, ... — Claude scans all recursively)
#       • Any nesting depth — Claude walks the full tree collecting all .docx files
#     Extract folder ID from link automatically:
#       https://drive.google.com/drive/folders/FOLDER_ID  → ID = FOLDER_ID
#       https://drive.google.com/drive/folders/FOLDER_ID?usp=sharing → same
#
#   If PYQ parameter absent: HARD STOP (v2.24.8). PYQ papers must be in Google
#   Drive — the local project/uploads fallback for the PYQ .docx corpus was
#   removed to standardize with Step 4 (PYQCount) and Step 2b (PYQScan), which
#   have always required Drive with no fallback. The Exam Pattern document and
#   any existing Analysis doc are UNAFFECTED — those small reference/state files
#   still come from project knowledge or chat upload, same as before.
#
#   Examples:
#     PYQExtract PYQ: https://drive.google.com/drive/folders/[YOUR_FOLDER_ID]
#     PYQExtract --status
#
# NO CONFIG FILE REQUIRED:
#   All parameters are auto-detected from the Exam Pattern document and PYQ papers.
#   You only need to upload documents — no JSON config to create or maintain.
#
# OUTPUT FILES (CLOSED SETS — see S11-3 for full contract):
#
#   PER-BATCH delivery (1 file, nothing else):
#     [ExamCode]_analysis_progress.json  -> batch accumulator; delivered after each batch
#
#   FINAL delivery (6 files, nothing else):
#     [ExamCode]_section_rules.md        -> PRIMARY: upload to [ExamCode] project knowledge
#     [ExamCode]_subtopic_manifest.json  -> upload to [ExamCode] project knowledge
#     [ExamCode]_taxonomy.xlsx           -> human-readable Subject/Topic/Sub-topic list (v2.24);
#                                           browse it to pick Step-6 scope values (no JSON needed)
#     [ExamCode]_PYQ_Frequency.xlsx      -> keep for Step 6 input
#     [ExamCode]_analysis_progress.json  -> keep locally (resume if adding papers later)
#     [ExamCode]_analysis_summary.md     -> human review audit trail
#
#   DO NOT DELIVER:
#     ✗ Any intermediate scripts or pipeline files
#     ✗ Any temporary JSON or working files
#     ✗ Input PYQ .docx files (these are INPUTS, not outputs)
#     ✗ Any renamed or versioned variants of the above files
#
# DRIVE USAGE:
#   Google Drive is used ONLY for reading PYQ .docx input files.
#   No output file is ever uploaded to Google Drive.
#   section_rules.md goes to: [ExamCode] Claude project → Files / Knowledge section.
#
# OVERRIDE RULE:
#   section_rules.md is ALWAYS regenerated from analysis_progress.json.
#   NEVER edit section_rules.md manually — re-synthesise instead.
#   Updating section_rules.md mid-series is SAFE.
#   Existing mocks unaffected. Future mocks use improved patterns.



# ═══ ARCHIVE — Framework_Blueprint pre-relocation header history (moved 2026-07-31 at v1.41; verbatim) ═══

# v1.40 — 2026-07-26 — S2-2 ASSERTS THE TAXONOMY LOCK (GAP-2026-07-25-003 follow-up).
#         v1.39 stopped Step 6 hand-parsing the Analysis doc. It did not make Step 6
#         check that the doc it now reads correctly is the doc PYQApprove APPROVED.
#         Framework_PYQSort S1-0b made that claim from v1.14 and nothing else did, so
#         a superseded Analysis doc that HALTS LOUDLY at Step 3 was allocated against
#         here silently. That is the worst place for it: the blueprint built from a
#         wrong taxonomy is internally consistent, passes every BV check, and is
#         indistinguishable from a correct one at Steps 7-11. S2-2 now calls
#         corpus_io.assert_taxonomy_lock() — THE gate, one implementation in
#         corpus_io, never a fourth transcription of S1-0b.
#         MINIMUM COMPANION: corpus_io.py >= v1.3.
#
# v1.39 — 2026-07-25 — S2-2 ANALYSIS-DOC READING DELEGATED (GAP-2026-07-25-002).
#   S2-2 described four "accepted arrangements" and told Claude to extract the
#   Topic|Sub-Topic|Q-count structure itself. That made Step 6 the FOURTH independent
#   reader of a machine-readable artefact three other steps also parsed — each by a
#   different convention, and three of the four measurably wrong on the first real
#   exam's doc. Prose over a structured file is non-deterministic across runs, and the
#   entire blueprint rests on the taxonomy it produces. S2-2 now calls
#   corpus_io.read_analysis_doc() (Cluster K — THE reader), which additionally HARD
#   STOPS when its parse disagrees with the totals the document declares about itself.
#   Options A and C (per-subject / mixed .docx sets) described a deliverable retired at
#   PYQAnalyse v2.6 that no project has ever held, and are removed rather than carried
#   as dead tolerance. Option D (a table pasted into chat) is removed because it lets
#   allocation run against a taxonomy nothing locked or fingerprinted; a missing
#   Analysis doc is §10 S10-5. No allocation arithmetic changes.
# v1.38 — 2026-07-23 — §14 SCHEMA SYNC: PRESENTATION PASSTHROUGHS (cross-step audit finding).
#   Framework_MockTestCreate §2 R24 resolves font_name / font_size_pt / di_header_color
#   through exam_config -> section_rules -> blueprint.json -> default. The blueprint tier
#   was DEAD: §14 declared none of the three and Step 6 wrote none of them, so a reader was
#   looking for fields its writer never produced. Harmless at runtime (.get() with defaults)
#   but a genuine writer/reader schema desync, and a silently dead fallback tier reads as a
#   supported override when it is not. All three are now declared OPTIONAL and passed through
#   from exam_config when present. PRESENTATION ONLY — no allocation, difficulty, format,
#   marking or gate consumes them. Omitting all three (the default for every exam that sets
#   nothing) leaves Step 7 byte-identical to pre-v1.38. Emitting a fabricated default is
#   explicitly forbidden: it would let the blueprint tier override section_rules and invert
#   the documented precedence.
#
# v1.37 — 2026-07-23 — ERA-AWARE ANALYSIS-DOC/EXCEL COMPARISON (audit follow-up).
#   Step 4 (PYQCount) has no era scope, so its Analysis-doc counts are always all-era. When
#   Step 5 runs with --frequency-scope current-era the Excel is current-era only, and §2 S2-3's
#   mismatch check compared the two directly: on any multi-pattern corpus the gap exceeds 25%
#   for nearly every subtopic, firing the "request user confirmation" branch per subtopic and
#   making Step 6 unusable — while reporting a discrepancy that is the INTENDED effect of the
#   operator's own flag. S2-3 now reads manifest['pattern_eras']['frequency_scope'] and skips
#   the comparison with a single INFO line when the two sides are measuring different paper
#   populations by design. Unchanged when scope is 'all' (including every pre-v2.25 manifest,
#   where the key is absent and 'all' is assumed). Taxonomy authority and Zero-PYQ
#   classification are both untouched.
#   NOTE: Framework_ScopedBlueprint S3-1 reads the Excel "exactly as the mock Blueprint S2-3
#   does" and therefore inherits this fix with no change of its own.
#
# v1.36 — 2026-07-23 — PATTERN-ERA NORMALISATION + COVERAGE-GATE SYMMETRY (GAP-2026-07-23-001).
#   ONE root cause, three symptoms: nothing in the pipeline re-expressed PYQ-measured
#   per-paper quantities in CURRENT-pattern units. Every exam whose Q-count has changed
#   (IIT JAM Biotechnology 100 Q -> 60 Q, and the reverse where a pattern grew) silently
#   fed historical-paper units into current-paper arithmetic.
#     FIX 1 — ENGINE (blueprint_core.py v2): new bc.rescale_to_total(raw_map, total)
#       re-expresses a class map in a new paper size, proportions preserved exactly, with a
#       relative-tolerance NO-OP guard so an already-normalised caller is untouched.
#       bc.derive_axis_schedule now normalises ALL THREE axes to sec_qs before deriving
#       anything and RETURNS the normalised maps. This repairs three consumers at once:
#         (a) axis1/axis3_target_per_mock — previously violated their own §14 "sum == sec_qs"
#             contract and annihilated minority classes. A 100-Q {TEXT 85, FIGURAL 10,
#             PASSAGE 5} mix apportioned to a 60-Q section returned {TEXT 75, FIGURAL 0,
#             PASSAGE 0}: sum 75 (not 60), both minority stimulus formats zeroed.
#         (b) axis2_window_target — computed as avg x window with NO rescale whatsoever,
#             so band quotas were wrong by the full pattern-size ratio.
#         (c) Framework_MockTestCreateAudit's Step-8 B-AXIS1/B-AXIS3 audit, which scales the
#             returned axis{1,3}_per_paper by the window — it was auditing every produced
#             paper against historical-size targets, raising findings no correct paper
#             could ever clear. Returning normalised maps fixes it at source.
#     FIX 2 — bc.largest_remainder_apportion SUM CONTRACT REPAIRED. Its negative-deficit
#       trim used a fixed `i > 10 * len(order)` iteration guard; any steeper deficit
#       exhausted the guard and the function RETURNED EARLY with counts that did not sum
#       to total, with no error raised. Now pass-based, stopping early only when every key
#       has reached 0 (unreachable while total > 0), with a closing assertion. The function
#       deliberately still does NOT rescale — that would turn a caller's bad-percentages
#       bug into a silent correction; rescale_to_total is the explicit fix.
#     FIX 3 — §9 S9-12 BV-AXIS: new AXIS-SUM and AXIS-UNIT checks. The §14 "sum == sec_qs"
#       contract was documented since v1.23 but never verified by any gate, which is why
#       (a) went undetected. Now enforced for axis{1,3}_target_per_mock and for all three
#       axis*_per_paper maps.
#     FIX 4 — §2 S2-3 COVERAGE GATE SYMMETRY. v1.32 FIX E handled corpora LARGER than the
#       current pattern (>105% -> INFO + per-subtopic check) but its mirror was never added,
#       so a corpus SMALLER than the current pattern (the exam grew) hit an unconditional
#       <90% HALT telling the operator to "re-run Step 5 to fix classification gaps" when
#       there are none to fix — an unresolvable loop. The <90% branch now runs the SAME
#       per-subtopic discriminator first: uniform shortfall across the taxonomy = pattern-size
#       change (INFO, proceed); concentrated shortfall = genuine Step-5 loss (HALT, unchanged
#       message). When no Analysis-doc taxonomy is available to discriminate it still HALTs,
#       but names both possibilities instead of only the one Step 5 can fix.
#   ZERO REGRESSION, PROVEN: Framework_ScopedBlueprint §6-2 already normalises to Q and
#   passes sec_qs=Q, so the tolerance guard makes FIX 1 a pure identity there — verified over
#   2,000 randomised already-normalised distributions. difficulty_counts is likewise untouched
#   (its input sums to total_qs by construction). blueprint_core self-test 75/75 (was 57/57;
#   the two pre-existing axis tests used a PHYSICALLY IMPOSSIBLE fixture whose axis2 summed to
#   2.55 against axis1/axis3's 25 — compute_section_axis_distribution can never emit that,
#   since every question gets exactly one class per axis. That impossible fixture is why the
#   axis2 unit bug survived; it is now realisable). Independent harness test_pattern_era.py:
#   368,127 assertions across property, differential (vs a from-scratch reference), regression
#   (pre-v2 algorithm reimplemented to prove the bug existed) and randomised end-to-end layers.
#   NOTE — what this does NOT fix: r_avg still carries the SUBJECT/subtopic mix of whatever
#   eras are in the corpus. §3 recency weighting dampens it but cannot remove it. Counts are
#   safe (§4-2 uses r_avg as a proportion against a sec_qs budget); mix is not. See the
#   §2 S2-3 PATTERN-ERA NOTE.
#
# v1.35 — 2026-07-22 — SECTION↔SUBJECT MAPPING FIX (BUGS 2-4 of 4, GAP-2026-07-22-001).
#   Ships atomically with Framework_MockTestAnalyse v2.24.9 (BUG 1). All 4 bugs are chained:
#   fixing only some exposes the next. All must ship together.
#
#   BUG 2 FIX — RESOLVER SUPPORTS 1:N SUBJECT→SECTION (§2 S2-1b):
#     section_for_subject was a scalar dict — for exams where one Subject spans multiple OTS
#     sections (IIT JAM, CSIR NET), only the LAST section survived (last-write-wins). Every
#     subtopic resolved to the last section; all other sections got zero subtopics silently.
#     FIXED: section_for_subject → sections_for_subject (dict of lists). subtopic_in_section()
#     changed from == to 'in'. section_for_subtopic() → sections_for_subtopic() (returns list).
#     Backward compatible: 1:1 exams produce single-element lists.
#
#   BUG 3 FIX — RE-KEY SUBTOPICS FROM TAXONOMY SUBJECT TO OTS SECTION (new S2-2c):
#     Analysis doc taxonomy uses Subject names as keys ("General Biology"). Working data
#     structures (all_subtopics, pyq_subtopics, zero_pyq_subtopics) are keyed by OTS section
#     names ("Section A"). Without re-keying, all_subtopics['Section A'] was empty for any
#     cross-subject exam → §3-5 classified nothing → allocation got zero subtopics.
#     FIXED: new S2-2c step builds all_subtopics[ots_section] by iterating over
#     subjects_for_section(ots_section) and collecting subtopics from each subject.
#     For 1:1 exams: identity re-key → zero behavior change.
#
#   BUG 4 FIX — B2/B3 SUBTOPIC RECONSTRUCTION VIA SUBJECTS_FOR_SECTION (§8-3, §8-5, §14):
#     B2/B3 rebuilt pyq_subtopics per section by comparing st['section'] == section['name'].
#     But st['section'] = taxonomy Subject ("General Biology"), while section['name'] = OTS
#     section ("Section A"). For cross-subject exams, this comparison returned 0 matches →
#     0 subtopics → AlgorithmError.
#     FIXED: B1 writes subjects_for_section to blueprint.json (new top-level field in §14
#     S14-1). B2/B3 read it and filter subtopic_list using st['section'] in subjects
#     (list membership, not equality). Fallback [section_name] preserves backward compat
#     for legacy blueprint.json files from 1:1 exams.
#
#   blueprint_version bumped to "1.35".
#   Zero behavior change for 1:1 exams (SSC CGL, MPPSC, etc.).
#   12/12 edge cases pass.
#
#   SECONDARY FIX — §6 MARKING_SCHEME AUTHORITY FOR multi_present/nat_present (§6 S6-2):
#     For question-type exams (IIT JAM: marking_scheme has MCQ+MSQ+NAT ranges), per-subtopic
#     PYQ observation could miss setting multi_present/nat_present because no single subtopic
#     has majority MSQ/NAT observations. The marking_scheme is authoritative: if it defines
#     MSQ/NAT ranges, the presence flags MUST be True so Step 7's generation paths activate.
#     Ships with Framework_MockTestCreate v5.30 (position-based dispatch).
#
# v1.34 — 2026-07-20 — REGISTRY CARRY-FORWARD REDESIGN (cross-step, Steps 1-11, schema-
#   sync audit). §8-5 Step 5's v1.33 logic reconstructed the registry field-by-field
#   from a hardcoded "carry forward these 5 fields, reset these other 7" list. Auditing
#   it against §12-1's own documentation found the split was WRONG for 5 of the 7
#   fields it reset: question_index, image_phashes, image_sources_used, session_log,
#   and content_tracking are ALL documented as accumulating across the mock series —
#   image_phashes/image_sources_used SPECIFICALLY to prevent reusing the same figural
#   image across mocks, content_tracking SPECIFICALLY to prevent reusing the same GA
#   fact/vocab word/idiom/etc. across mocks. Resetting them every series would have
#   silently disabled that dedup across any series boundary — the exact failure class
#   this feature exists to prevent. (A first pass of this same audit had already caught
#   two smaller omissions this way — semantic_usage and exhausted_subtopics — which
#   is what prompted checking every remaining field instead of stopping there.)
#   ROOT CAUSE: reconstructing a hardcoded field subset is inherently fragile — it
#   silently drops anything not explicitly listed, and nothing catches the omission
#   until content quality degrades in a way nobody traces back to a series restart.
#   FIX: Step 5 REDESIGNED to mirror Framework_ScopedBlueprint.md §8-7 (the reference
#   implementation this whole feature was modeled on — confirmed via audit to have
#   never had this bug): if a prior-series registry exists, pass it through VERBATIM
#   (no field-by-field reconstruction at all) with a self-heal pass that only ADDS any
#   of the 13 §12-1 universal fields a legacy registry is missing, never drops a
#   present one. Only a genuine first-ever series (no existing registry at all) seeds
#   the full blank template. This eliminates the whole bug class, not just the two
#   fields the first pass found — a future schema addition can no longer be silently
#   dropped by an incomplete carry-forward list, because there is no longer a
#   carry-forward list to be incomplete.
#   Verified: validate_framework_md.py (0 issues); simulated both the old (proven
#   losing exhausted_subtopics/image_phashes across a series) and new (verbatim
#   pass-through, nothing lost) behavior against paper_pipeline.py.
#
# v1.33 — 2026-07-20 — CROSS-SLOT REGISTRY CONTINUATION (paper_pipeline.py integration).
#   Mock blueprints switch from "fresh registry per series" to "preserve-and-continue"
#   (aligning mocks with the scoped tiers), enabling cross-slot dedup + continued numbering
#   when an ExamCode's MockBlueprint is re-run for a new series. WHAT CHANGED:
#     §8-5 S8-5 (B3): new Step 4B — imports paper_pipeline as pp; reads the existing
#       [ExamCode]_registry.json from a prior series if present (flagged at S1-3); calls
#       pp.apply_mock_offset(blueprint, existing_reg) BEFORE blueprint.json/blueprint.xlsx
#       are written, so mocks[].mock, mocks[].paper_id, and difficulty_schedule[].mock
#       continue numbering from the prior series instead of restarting at M01. First-ever
#       series (no existing registry, offset 0): blueprint returned UNCHANGED by
#       apply_mock_offset — blueprint.json is byte-identical to pre-v1.33 output.
#     §8-5 Step 5 (registry.json generation): papers_completed, mocks_completed,
#       question_hashes, stem_texts, semantic_tuples (and rc_manifests/figural_manifests
#       when applicable) are now CARRIED FORWARD from the existing registry instead of
#       seeded as blank arrays, then passed through pp.registry_guard(...) as a defensive
#       check against accidentally emitting an empty registry over a populated one.
#     EC-6 and RS-10 reworded: registry is preserved across series (append, never wipe) —
#       previously described as "replaced" / "dedup starts fresh for new series", which is
#       no longer correct behaviour.
#   Shared logic lives ONLY in paper_pipeline.py (self-test 30/30) — not duplicated here.
#   Verified: first-ever series produces byte-identical blueprint.json to pre-v1.33; a
#   second series continues mock numbering and the registry is carried forward, never blanked.
#
# v1.32 — 2026-07-17 — GAP ANALYSIS FIX A + FIX D + FIX E (MPSC_Botany root-cause audit,
#   Framework_Gap_Analysis — Step 6 §6 HALT investigation). Closes three structural defects
#   that recur on EVERY exam with (a) any Zero-PYQ subtopic, (b) any PASSAGE/DI subtopic, or
#   (c) an OTS section label that differs from the taxonomy Subject — not exam-specific bugs.
#   WHAT CHANGED:
#     FIX A — §6 FORMAT NOW READ FROM THE MANIFEST (was: Frequency Excel):
#       S6-1 rewritten to build format_map from MANIFEST_IDS[sid]['format'] (the manifest's
#       4-way TEXT/FIGURAL/PASSAGE/DI value) for every allocated subtopic — PYQ AND Zero-PYQ.
#       The manifest is taxonomy-complete by construction (S2-MANIFEST gate); the Excel is
#       derived from PYQ occurrence only, so a Zero-PYQ subtopic could structurally never
#       appear in it — every exam with ≥1 Zero-PYQ subtopic guaranteed a false HALT (root
#       cause of the MPSC_Botany 41-subtopic HALT). NEW S6-1b: the Excel Format column, when
#       present, becomes an ADVISORY cross-check only (manifest wins, logged as a note, never
#       a HALT) for PYQ subtopics. HALT is now reserved for a REAL manifest defect (missing/
#       invalid `format` — a pre-v2.22 manifest). Also fixes passage_present/di_present being
#       silently False for any exam with real PASSAGE/DI content, because the Excel writer
#       (aggregate_frequency_data) is only ever 2-way (TEXT/FIGURAL) while the manifest is
#       4-way — §6 was reading the weaker source. SOURCES OF TRUTH, S10-3, S10-7, S10-11,
#       S1-5/S1-6, and the §8-2 checklist updated to match (Excel Format inference retired —
#       no longer needed since the manifest, required by S2-MANIFEST, is always present).
#     FIX D — SECTION↔SUBJECT MAPPING RESOLVER (new, §2 S2-1):
#       New subjects_for_section()/section_for_subtopic()/subtopic_in_section() resolver,
#       built once per B1 run (single section → all manifest Subjects map to it; N sections
#       with names == Subjects → identity map, zero behaviour change; anything ambiguous →
#       HARD STOP requesting explicit exam_config.sections[].subjects[]). Every raw
#       `MANIFEST_IDS[sid]['section'] == section['name']` / `AXIS_DIST_BY_SECTION.get(sec_name)`
#       string-equality site now routes through it: §4-2 mandate-first reservation (3 sites),
#       preflight_mandate_ravg_check, §7-7 axis_schedule build loop (pyq_ids/zp_ids +
#       axis_distribution lookup, now section-spanning-Subject-aware via
#       _resolve_axis_dist_for_section). Previously, any exam where the OTS section label
#       differed from the manifest's taxonomy Subject (e.g. exam_config "MPSC Botany" vs.
#       manifest Subject "Botany" — true of every single-Subject exam) silently dropped ALL
#       mandate enforcement and left the three-axis feature permanently inert with no error
#       — MPSC Botany's axis_schedule was 'no_pyq' for exactly this reason. New SEC-8 gate in
#       BV-AXIS (§9 S9-12) now HARD-FAILS when a section has PYQ subtopics and the manifest
#       carries axis data, yet status is still 'no_pyq' — converting the silent disable into
#       a caught mapping error. zero_pyq_rotation{}/sections[] stay OTS-section-keyed
#       (contract preserved, §14 S14-4) — the resolver bridges internally, never the reverse.
#     FIX E — COVERAGE GATE OVER-READ (§2 S2-3, low severity):
#       New explicit over-coverage (>105%) INFO branch: when a historical PYQ paper is larger
#       than the current exam pattern (e.g. a 150-Q 2011 paper vs. a 100-Q current pattern),
#       the aggregate ≥95% PASS no longer masks a genuine per-subtopic gap — a per-subtopic
#       coverage cross-check against the Analysis-doc taxonomy now runs instead, using the
#       same 90%/95% FLAG/HALT thresholds applied per-subtopic.
#   PAIRS WITH: Framework_MockTestAnalyse v2.24.6 FIX B (Frequency Excel completeness +
#   Format parity with the manifest) + FIX C (structural DI/PASSAGE detection, propagated
#   byte-identical to MockTestCreateAudit v2.7.4 S6-1b).
#   Verified: validate_framework_md.py (0 issues, 39/39 code blocks AST-clean), pyflakes
#   clean on all extracted Python blocks touched by this change.
#
# v1.31 — 2026-07-15 — DOC: clarified that blueprint_version is the shared blueprint.json SCHEMA
#   version (Step-7 floor MIN_BLUEPRINT_VERSION=(1,7)), decoupled from the spec-FILE version, and
#   that the scoped blueprint must emit the SAME value. No code/behaviour change. Prompted by the
#   ScopedBlueprint v1.2 fix (it had emitted its spec version '1.0' as blueprint_version, which
#   would fail the (1,7) floor). Keeps mock + scoped schema versions in sync.
#
# v1.30 — 2026-07-15 — REGISTRY SCHEMA SYNC (docs/seed only; zero logic). The §12 registry seed +
#   schema now list semantic_usage=[] and exhausted_subtopics={} alongside the existing fields, to
#   MATCH the generation layer's schema (MockCreate v5.22 B). Purely additive: a registry seeded here
#   is byte-schema-identical to one Step 7 would self-heal. No allocation/behaviour change.
#
# v1.29 — 2026-07-15 — C1: UNIVERSAL paper_id IDENTITY (generation-layer foundation; additive,
#   zero behavioural change). (1) Each mocks[] entry now also carries paper_id="MOCK:M{mock:02d}"
#   (§14 S14-5) — Steps 7-11 still read 'mock'; the generalised (paper_id) path + the shared
#   registry key on paper_id. (2) The registry seed (B3 Step 5) + §12 S12-1 add papers_completed=[]
#   alongside mocks_completed=[] — the paper-identity ledger shared by mocks and every scoped tier;
#   legacy mocks_completed-only registries are auto-migrated by the scoped loader. schema_version
#   stays "1.0" (the schema bump belongs to the Step-7/registry generalisation, not this additive
#   step). Allocation math UNCHANGED (blueprint_core.py untouched); proven bit-identical by
#   blueprint_refactor_integration_test.py (2/2) + blueprint_c1_paperid_test.py.
#
# v1.28 — 2026-07-15 — SHARED ENGINE EXTRACTION (allocation core → blueprint_core.py).
#   The allocation MATH formerly inlined here is now provided by the universal engine
#   blueprint_core.py (single source of truth; the same engine backs the forthcoming
#   Subject/Topic/Sub-Topic scoped blueprints, so a fix lands once). Extracted, VERBATIM-
#   equivalent: recency split (§3-1 → bc.split_recency) + r_avg (§3-2 → bc.compute_r_avg);
#   proportional split (§4-2 STEP 3 → bc.proportional_split) + largest-remainder deficit
#   (§4-2 STEP 4 → bc.largest_remainder_fix), with STEP 3b mandated raw_total PRESERVED and
#   AllocationError re-wrapped into the spec's AlgorithmError; EXACT MATRIX FILL (§4-5b →
#   bc.exact_fill); difficulty counts (§7-4 → bc.difficulty_counts); three-axis schedule
#   (§7-7 → bc.derive_axis_schedule + bc.axis1_feasibility, internally
#   bc.largest_remainder_apportion + bc.section_axis2_pool_caps); slugify (§17 → bc.slugify).
#   NEW S1-2b ENGINE MANDATE: HARD STOP if blueprint_core.py absent → copy to /home/claude
#   → run --self-test (must print "SELF-TEST: N/N PASS") → import blueprint_core as bc.
#   ENGINE PARAM RENAME: mocks_per_window → papers_per_window (a mock is a paper); the
#   RETURNED axis_schedule dict STILL carries the 'mocks_per_window' KEY that Steps 7/8 read
#   (output contract unchanged), so only the §7-7 build-loop call keyword changed.
#   BEHAVIOUR IS UNCHANGED — proven three ways: (a) blueprint_core_test.py 19/19 +
#   qa_pass2_differential.py (bc.* == verbatim source over ~128k inputs); (b)
#   blueprint_refactor_integration_test.py (refactored wiring == pre-refactor inline over
#   50k fixtures, incl. mandates / floors / infeasible classification); (c)
#   validate_framework_md.py 0 issues, 37/37 AST clean. ONE diagnostic-only change: the
#   r_avg data-quality warning now omits the specific year (the subtopic is still named);
#   the r_avg VALUE is byte-identical. No blueprint.json schema change.
#
# v1.27 — 2026-07-08 — CANONICAL AUDITOR (§13-7A): B3 now generates the ONE canonical
#   v2.6 auditor VERBATIM from Framework_MockTestCreateAudit.md Appendix A (full A-* gates,
#   --audit-state COMPLETION GATE S5-1A, fixture-based self-test), NOT the retired 13-gate
#   constant-print MVP. Self-test validation is now FIXTURE-BASED with N >= AUTH_GATE_FLOOR
#   (35); a constant-print "N/N PASS" is REJECTED. Retires the "minimum viable vs full 66"
#   split and the upgrade path. Root cause / rationale: Framework_MockTestCreateAudit.md v2.6.
#
# v1.24 changes: BV-10 SAME-MECHANIC DEADLOCK — PERMANENT STRUCTURAL FIX.
#   (1) NEW §4-1b BV-10 MECHANIC FEASIBILITY GATE at B1 (analogue of EC-11): an
#       exhaustive G1→fast→G3(Hall's b-matching) decision procedure that PROVES the
#       same-form constraint satisfiable BEFORE generation, per collision_domain and
#       every batch window (incl. short final window), consuming rare/ZP/mandate pins.
#       If infeasible → HALT with offending members + named upstream fix (NO regen loop).
#   (2) BV-10 (§9-6b) rebuilt as TWO TIERS: BV-10a HARD on form_key (fine identity,
#       domain-scoped — fires only on TRUE duplicates); BV-10b SOFT cap on family
#       (coarse), a Step-8 tolerance target that never blocks. Consumes Step 5 v2.24
#       fields (form_key, concept_group=family, collision_domain).
#   (3) max_per_mechanic_per_mock config (default 1) for legitimate repetition (DI-heavy).
#   (4) §9-10 failure protocol now branches STOCHASTIC (regenerate) vs STRUCTURAL
#       (HALT-with-fix); the "3 attempts → ask user" dead-end is gone.
#   Guarantee: if §4-1b passes, a collision-free schedule provably exists; if not, B1
#   halts with the exact fix — so BV-10 can never deadlock at B2/B3 again. Verified by
#   step6_harness (11/11) + engine extracted-from-this-file + whole-doc syntax parity.
#   PAIRS WITH Step 5 v2.24 (Framework_MockTestAnalyse), which emits the form_key axis.
#
# v1.25 changes: EXACT MATRIX FILL allocator (§4-5b) — fixes BV-7 F1 allocation drift
#   (register D3-14 / §12; drifted 30/59 subtopics in the SSC CGL run). Replaces Phase-0
#   backward-forcing + naive column-fix (which did not preserve per-subtopic quota) with a
#   base + Gale-Ryser remainder fill: row sums == quota EXACTLY (0% F1 drift), column sums
#   == free capacity EXACTLY (BV-1), per-cell floor/ceil (F5 variance ≤ 1), coverage (BV-9B),
#   and deterministic (no re-drift across batches, D3-6). §4-6 column-fix becomes a no-op
#   invariant check. Verified by alloc_harness (15/15 incl. 100 random instances).
#
# v1.26 changes: COVERAGE GATE PER-PAPER NORMALIZATION (register D6-7). The coverage
#   validation gate summed multi-year "Combined Qs" against a single-paper total, so it
#   reported ~300% on a 3-year Excel and could never detect under-coverage (the MPPSC
#   Botany 62% failure mode). Now sums the per-paper Avg/Paper column (fallback: Combined
#   Qs / total_papers) → per-paper-vs-per-paper. Verified by cov_harness (7/7): correctly
#   passes full coverage, HALTs on 62% under-coverage, unchanged for single-paper Excels.
# [ExamCode] project | Step 6 (MockBlueprint) | Exam-agnostic
#
# PURPOSE:
#   Generate a complete subtopic-allocation blueprint for any MCQ competitive exam.
#   This spec is exam-agnostic — it works for SSC, IBPS, GATE, UPSC, NEET, and any
#   MCQ exam series. Exam-specific parameters (sections, subtopics, frequencies) are
#   read from input documents at runtime — nothing is hardcoded here.
#
# PIPELINE POSITION:
#   Step 5:  PYQExtract      ← must publish subtopic_manifest.json before Step 6 B1 finalises
#   Step 6:  MockBlueprint   ← THIS SPEC (consumes Step 5's subtopic_manifest.json)
#   Step 7:  MockCreate
#   Step 8:  MockCreateAudit
#   Step 9:  MockExplain
#   Step 10: MockExplainAudit
#   Step 11: MockDeliver
#
#   ALL steps run in the [ExamCode] project (exam-specific).
#   Steps 5 and 6 run IN PARALLEL — both must complete before Step 7.
#   Step 5 and Step 6 do NOT depend on each other — run in any order.
#
#   v1.23 — 2026-07-07 — THREE-AXIS FORMAT-DISTRIBUTION ENFORCEMENT (File 2 of the feature;
#           reads the targets Step 5 v2.23 emits; Steps 7/8 are Files 3–4).
#           A mock must replicate the exam's FORMAT MIX, not just its syllabus. Blueprint's
#           role: READ the per-section axis targets + per-subtopic capability, CARRY them into
#           blueprint.json for Steps 7/8, and enforce what allocation can enforce.
#           FIX A — S2-MANIFEST reads manifest['axis_distribution'] (per-section 3-year targets)
#             + per-subtopic axis2_capability / observed_axis2 / presentation_family. Absent-safe.
#           FIX B — §6 GOLDEN-RULE RECONCILIATION: format still NEVER excludes (r_avg=0 remains
#             the SOLE exclusion); it now ADDITIONALLY influences SCHEDULING so axis targets are met.
#           FIX C — S7-7 derive_axis_schedule(): the per-section axis "schedule" (parallel of
#             difficulty_schedule). Carries axis1/2/3 per-paper averages + audit modes; derives
#             band-mode Axis-2 window targets + guarantee list; classifies each guarantee format's
#             feasibility ('pyq_covered' — Option-C batch coverage already guarantees it, no swap
#             needed; 'zp_only' — best-effort via ZP rotation; 'unsatisfiable' — accept shortfall
#             per decision (i), fabrication BANNED). Stored as blueprint['axis_schedule'].
#           FIX D — AXIS-1/3 (locked): carry target + feasibility report + soft-steer tie-break;
#             NOT a hard per-mock re-solve (Subtopic stays hard #1). Audited within tolerance at Step 8.
#           FIX E — §9 BV-AXIS gate (B3): axis_schedule well-formed + guarantee/axis feasibility report.
#           FIX F — §14 blueprint.json gains axis_schedule (S14-3b); axis targets are carried
#             in blueprint.json (human-readable, authoritative for Steps 7/8) and surfaced in the
#             B1/B3 delivery notes. The §15 xlsx LOCKED 5-sheet contract is intentionally PRESERVED
#             (no 6th sheet — the axis targets are not an xlsx concern). blueprint_version → 1.23.
#   v1.0 — Initial release. Core allocation algorithm across 17 categories.
#           Validated against SSC CGL Tier 1 (221 subtopics, 204 papers, 50 mocks).
#   v1.1 — Added Step 5 (PYQExtract) pipeline coordination: parallel execution
#           note, section_rules.md handoff, subtopic name consistency rule, DoD item 15.
#   v1.2 — Memory prohibition + GOLDEN RULE (Format is classification only, never
#           exclusion). BV-0A subtopic completeness check. EC-10 memory conflict edge
#           case. Format inclusion rules in §10 S10-7, S10-11, EC-5.
#   v1.3 — Option C batch coverage guarantee: every PYQ subtopic ≥ 1 Q per 10-mock
#           batch window. Three-phase algorithm (Phase 0 + Phase 1 + Phase 2).
#           Quota minimum raised to n_batches. BV-9B batch coverage check per B2
#           batch. EC-11 feasibility edge case. INVARIANT 8. §8-3 Phase 0 wired in.
#   v1.4 — BATCH GATE enforcement (ISSUE 1,3): §8-2 Step 9 and §8-3 Step 8 now
#           carry explicit BATCH GATE blocks with hard STOP language — Claude MUST
#           NOT continue past B1 or any B2 batch in the same response. Passive
#           "wait for user affirmative" language was insufficient; now mirrors HALT
#           strength. B1 present_files fix (ISSUE 2,5): §8-2 Step 9 and §11-1
#           PART B now unambiguously list BOTH blueprint.xlsx AND blueprint.json v1
#           as mandatory B1 deliverables — no file may be omitted. §8-3 Step 7
#           also hardened with explicit two-file checklist. §11-2 PART B clarified.
#           blueprint_version field updated to "1.4".
#           Second-pass fixes: §8-1 overview corrected (B1 delivers 2 files, not 1).
#           §8-5 Step 8 stale "ref §11 BD-7" corrected to "ref §11 S11-3".
#           §8-5 Step 8 now has 8-item pre-delivery checklist before present_files.
#           §8-5 Step 9 stale "ref §11 BD-7" corrected to "ref §11 S11-3".
#           §11-3 PART B now has 6-item pre-delivery checklist (matches B1/B2 pattern).
#           §11-3 PART B file list now uses exact [ExamCode]-prefixed names.
#           Definition of Done: new item ☐ 0 added — BATCH GATE discipline check.
#           Third-pass deep analysis fixes (7 additional bugs):
#           All remaining stale BD-1/BD-2 references replaced with S11-1/S11-2
#           in S6-5, S8-2 Step 9, S8-3 Step 7, S9-0A (4 occurrences).
#           §11-1 BV-0A "Zero silently excluded" clarified to "Silently excluded: 0"
#           to eliminate ambiguity with "Zero-PYQ" terminology.
#           §13-8 Step C "5 files — NOT the xlsx" clarified: 4 Step-1 files +
#           1 Step-0 file (section_rules.md) = 5 total; each file now labelled
#           with its source step.
#           §8-2 Step 6 progressive bands timing fixed: now consistent with
#           §7 S7-3 which states bands are collected during S1-6, not mid-B1.
#           Fourth-pass deep analysis fixes (4 real bugs):
#           §8-5 Step 6: ExplainLearnings.md header now matches §13-5 exactly
#           (added missing "— [exam_name]" segment).
#           §8-5 Step 7: ExplainAuditLearnings.md header now matches §13-6 exactly.
#           S6-3: stale "ref §14 JS-7" corrected to "ref §14 S14-7".
#           S3-6 + §15 S15-3: Col E ambiguity resolved — both now specify the
#           combined label format "PYQ-based (High/Medium/Low)" / "Zero-PYQ"
#           so importance class and PYQ type are stored together in one column.
#   v1.5 — §15 XLSX SPECIFICATION LOCKED (ISSUE: wrong sheet names and wrong Sheet
#           content delivered in prior run). Root cause: §15 was detailed but lacked
#           a mandatory pre-generation checklist enforcing the exact sheet names and
#           column structure before present_files is called.
#           Fixes applied:
#           (1) §15 completely rewritten as LOCKED SPEC with exact sheet names,
#               exact column headers, exact column order, and explicit examples
#               drawn from the verified reference output. These are PERMANENT RULES
#               — Claude MUST match them exactly. Deviating = critical error.
#           (2) §15-CHECKLIST added: a mandatory 5-point self-verification that
#               Claude runs against its own generated xlsx BEFORE calling
#               present_files. If any item fails: fix xlsx before delivering.
#           (3) §8-2 Step 8 updated to reference the §15-CHECKLIST explicitly.
#           (4) Sheet 2 (Blueprint) column header is "r_avg" (not "Recency Avg/Paper").
#           (5) Sheet 3 (Summary Stats) columns match reference exactly:
#               Subject|Topic|Sub-Topic|Format|Type|r_avg (Recency)|Pooled Avg|
#               Total PYQs|Quota (Target Qs)|Actual Qs|Accuracy%|Mocks Appeared
#               (12 columns, not 15 — S15-3 previously overcounted).
#           (6) Sheet 4 (Difficulty Schedule) uses percentage NUMBERS (15/30/55),
#               Total=100, not Q-counts. Band label: "Standard".
#           (7) Sheet 5 (Phase 0 Verification) simplified to match reference:
#               Subject|Topic|Sub-Topic|Format|r_avg (Recency)|Type — sorted by
#               r_avg desc, ZP at bottom. Full year-column expansion is optional
#               and only required when paper-count data is available.
#           blueprint_version field updated to "1.5".
#   v1.6 — Full line-by-line audit (fifth pass). Three bugs found and fixed:
#           Bug 1: §8-3 Step 5 comment had stale "§14 JS-6" reference — corrected
#           to "§14 S14-6" (consistent with all other S14-x references in spec).
#           Bug 2: §15-3 Sheet 3 Type column listed "zero_pyq" (snake_case) but
#           §3-6 defines "Zero-PYQ" (human-readable with capital Z and hyphen) for
#           Summary Stats. Now aligned: §15-3 Type col shows all four labels exactly
#           as §3-6 defines them: "PYQ-based (High)", "PYQ-based (Medium)",
#           "PYQ-based (Low)", "Zero-PYQ". Phase 0 sheet retains "pyq_based" /
#           "zero_pyq" (machine-readable) — these are DIFFERENT sheets with
#           intentionally different label styles; now explicitly documented.
#           Bug 3: EC-9 (5+ sections edge case) listed old hex color codes
#           (#D6E4F7, #E2F0D9, #FFF2CC, #FCE4D6, #EAD1DC, #D0E4CC) that
#           conflicted with §15-0 locked colors (#DEEAF1, #E2EFDA, #FCE4D6,
#           #EAE3F7). EC-9 now references §15-0 exactly. Single source of truth
#           for all color codes is §15-0.
#           blueprint_version field updated to "1.6".

#   v1.20 — 2026-07-06 — AUDIT SCRIPT AUTO-GENERATION (6th output file).
#           Root cause: [ExamCode]_mock_test_audit.py was a manual creation step
#           between Step 6 and Step 7/8. Users could forget → HARD STOP at Step 8.
#           Step 6 already has all data needed (blueprint.json structure, sections,
#           Q counts, format flags) to generate the minimum viable audit script.
#
#           CHANGE 1 — S13-NEW (S13-7A): new section defining mock_test_audit.py as
#             Step 6 output. Includes: purpose, content (minimum viable 13-gate script
#             from Appendix A template), upload rule, lifecycle, collision handling,
#             upgrade path to full 66-gate version.
#
#           CHANGE 2 — S8-5 Step 8A (new): B3 generates the audit script from the
#             AUDIT_SCRIPT_TEMPLATE embedded in this spec. Runs --self-test validation
#             before delivery. HALT if self-test fails.
#
#           CHANGE 3 — §13 section header, S13-1, S13-7, S13-8, S13-9 updated:
#             "5 files" → "6 files" throughout. mock_test_audit.py added to naming
#             convention, delivery order, upload instructions, and re-run procedure.
#
#           CHANGE 4 — S11-3 PART B/C (handoff): 6th file in present_files and upload
#             list. Handoff message updated.
#
#           CHANGE 5 — DoD item ☐ 25 added: audit script generated, self-test passed.
#
#           CHANGE 6 — AUDIT_SCRIPT_TEMPLATE (§13-7A): canonical reference section
#             added to this spec. Generation rules, collision handling, and lifecycle
#             defined here. Template code currently in Step 7 Appendix A (transitional);
#             will move here when Step 7 is updated next. Step 7 Appendix A then becomes
#             a pointer to this section.
#
#           EDGE CASES COVERED (20 total — see conversation record):
#             EC-A1 single source of truth (rules in Step 6 §13-7A; code transitionally
#                   in Step 7 Appendix A until Step 7 update moves it here)
#             EC-B1 minimum viable vs full (Step 6 generates MVP; user upgrades later)
#             EC-B3 self-test without python-docx (--self-test never imports docx)
#             EC-B4 MSQ/NAT gate dormancy (script reads flags from blueprint at runtime)
#             EC-C5 B3 self-test validation (HALT if fail)
#             EC-D1 collision with user's custom script (ask before overwriting)
#             EC-D3 re-run overwrites upgraded script (warn about downgrade)
#           blueprint_version field updated to "1.20".
#
#   v1.22 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S13-10: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. All three batch types (B1, B2, B3)
#           now render the standardized visual footer after every present_files call.
#           B1/B2 use F1 (amber mid-step), B3 uses F2 (green step-complete).
#           Zero logic change.
#   v1.21 — 2026-07-07 — ZERO-PYQ MANIFEST COMPLETENESS GATE (Fix B from BUGFIX report).
#           Root cause: Step 6 had a code path in §5 (ZP rotation setup) and §10
#           (missing-data fallbacks) that discovered subtopics from the taxonomy/syllabus
#           and added them to the blueprint WITHOUT routing through resolve_subtopic_id().
#           These subtopics got auto-generated sequential IDs (ST0097, ST0098, ...) that
#           existed in neither the manifest nor section_rules.md. Step 7 correctly HARD
#           STOPPED at S3-8 because these self-minted IDs were unjoinable.
#           Discovered: SSC CGL Tier 2, Mock 1 — 3 of 7 orphan IDs triggered the block.
#
#           FIX B.1 — RULE 2a (NO BYPASS): new invariant added to CROSS-STEP CONTRACT
#             (§2 edge cases). EVERY subtopic that enters the blueprint — whether from the
#             Analysis doc, the taxonomy, the syllabus, or any fallback/supplement path —
#             MUST resolve to a manifest id via resolve_subtopic_id(). There is NO code
#             path that creates a subtopic entry without a manifest-resolved id. Specifically
#             banned: auto-generated sequential IDs, max_id+1 patterns, any id not returned
#             by resolve_subtopic_id().
#
#           FIX B.2 — S2-MANIFEST-COMPLETENESS: new pre-flight gate added to §17 after
#             S2-MANIFEST. Before B1 begins, verifies that the manifest covers the exam's
#             taxonomy by attempting to resolve every taxonomy subtopic. If any taxonomy
#             subtopic has no manifest id → HARD STOP naming the missing subtopics and
#             directing the user to re-run Step 5 (v2.20+ runs taxonomy sync). Step 6
#             NEVER self-mints — it HARD STOPS and directs upstream.
#
#           CHANGE 3 — DoD items ☐ 26 and ☐ 27 added for the new gates.
#           blueprint_version field updated to "1.21".
#
#   v1.19 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (Step 2a marking_scheme integration).
#           Root cause: Step 2a v2.5 replaced scalar marks_per_question/negative_marking
#           with per-range marking_scheme[] and added level, medium, max_attempt to
#           exam_config.json. Step 6 must read these and carry them in blueprint.json
#           so downstream Steps 7-11 consume them.
#
#           CHANGE 1 — S2-1 REWRITE: PRIMARY SOURCE IS NOW exam_config.json:
#             Exam Pattern document is NO LONGER the primary source for section structure.
#             exam_config.json (written by Step 2a from the standardized xlsx) is the
#             authoritative source. Legacy path (read Exam Pattern doc directly) preserved
#             as fallback when exam_config.json is absent.
#             New fields read from exam_config: marking_scheme[], level, medium, max_attempt.
#
#           CHANGE 2 — BLUEPRINT.JSON TOP-LEVEL FIELDS ADDED:
#             marking_scheme  : list — per-range scoring rules (from exam_config).
#             level           : str  — academic level (from exam_config).
#             medium          : str  — exam language (from exam_config).
#             These are carried through for Steps 7/8/9/11. Steps 7/9 use marking_scheme
#             for per-Q-position marks lookup and level for complexity calibration.
#
#           CHANGE 3 — SECTIONS[] SCHEMA: max_attempt ADDED:
#             Each section entry in sections[] now includes max_attempt (int).
#             When max_attempt == total_qs: no attempt limit (all Qs attempted).
#             The framework generates ALL total_qs questions per section regardless.
#             max_attempt is OTS platform metadata only.
#
#           CHANGE 4 — SECTION ≠ SUBJECT NOTE IN S2-1:
#             Section names from exam_config are OTS display labels, not taxonomy Subjects.
#             Consistent with Step 2a v2.5 S2-2a architectural note.
#
#           CHANGE 5 — S14-1, S14-2 SCHEMA DOCS UPDATED for new fields.
#           blueprint_version field updated to "1.19".
#
#   v1.18 — 2026-07-05 — FREQUENCY EXCEL COVERAGE VALIDATION GATE (2 additions).
#           Root cause: MPPSC Botany framework-generated Frequency xlsx had only 93/150
#           questions mapped (38% data loss). Step 6 consumed this xlsx without any warning,
#           producing a blueprint with catastrophically distorted weightages (e.g., Diversity
#           of Life Forms: 5 Qs instead of 34). Two defensive checks added:
#
#           (1) S2-3 COVERAGE VALIDATION GATE (new): After reading the Frequency Excel,
#               compute sum(all Combined Qs across all sections) and compare against
#               exam_config.total_questions (or Exam Pattern total). If mismatch > 5%:
#               HALT with message identifying the gap. Prevents consuming incomplete
#               frequency data that would produce inaccurate blueprints.
#
#           (2) S10-3 SOURCE PRIORITY UPDATE: Added note that if Frequency Excel % of
#               Subject values imply a denominator different from exam total questions,
#               this signals a data quality issue in Step 5 output — flag before proceeding.
#
#           blueprint_version field updated to "1.18".
#
#   v1.17 — 2026-07-04 — CROSS-STEP CONTRACT SYNC AUDIT (5 fixes).
#           Deep cross-file analysis against Framework_MockTestCreate (v5.4),
#           Framework_MockTestCreateAudit (v1.3), Framework_MockTestExplain (v1.6),
#           Framework_MockTestExplainAudit (v1.3), Framework_MockDeliver (final),
#           and Framework_MockTestAnalyse (v2.16). All fixes are additive — no
#           allocation behaviour change; zero existing field semantics altered.
#           (1) REGISTRY SCHEMA GAP (§12-1, §12-3, §8-5 Step 5, RS-9): MockCreate's
#               REQUIRED_TOP expects 4 fields that Blueprint's §12 template did NOT
#               seed: image_phashes, image_sources_used, session_log, content_tracking.
#               MockCreate self-healed them on first mock — technically violating RS-9
#               ("Step 2 never adds new top-level fields"). FIXED: all 4 fields now
#               seeded in the §12-1 template (image_phashes=[], image_sources_used=[],
#               session_log=[], content_tracking={}). §12-3 examples updated. §8-5
#               Step 5 generation list updated. RS-9 rewritten to enumerate all seeded
#               top-level fields and explicitly permit content_tracking subfield
#               creation via setdefault() (not a top-level addition).
#           (2) option_label FIELD DEFINITION INACCURACY (§14-1, §8-2 Step 7): both
#               claimed "Step 7 reads via bp.get('option_label')" but MockCreate R10
#               reads option_label_format from section_rules.md, not from blueprint.
#               FIXED: field definition now says "Carried for visibility/parity; Step 7
#               reads the AUTHORITATIVE value from section_rules.md R10."
#           (3) STEP NUMBER MAPPING NOTE (header): added a clear 17-line mapping block
#               (matching Framework_MockTestAnalyse v2.16 pattern) documenting the
#               internal "Step 0/1/2…" → canonical "Step 5/6/7…" convention used
#               throughout this file. Header lines 20-21 updated from "Steps 0 and 1"
#               to "Steps 5 and 6" for canonical consistency.
#           (4) §12-3 Example 3: hardcoded "IBPS_PO_DI" exam_code replaced with
#               generic "[ExamCode]" placeholder (exam-agnostic guarantee).
#           (5) S12-5 CROSS-REFERENCE AUDIT: verified question_index, subtopic_id,
#               difficulty_labels, answer_type, answer_cardinality, total_options,
#               msq_contract, nat_contract field names are byte-identical between
#               Blueprint schema (§14) and MockCreate reads (S3-*, bp.get calls).
#               All verified consistent — no additional fixes needed.
#           blueprint_version field updated to "1.17".
#
#   v1.16 — 2026-07-04 — EXAM-AGNOSTIC RIGIDITY AUDIT (7 fixes).
#           Enforces the "zero hardcoded exam values" guarantee by removing all
#           SSC-specific content from active spec text and making fixed thresholds
#           configurable via blueprint.json with backward-compatible defaults.
#           (A) BV-9B print template (§9-11): hardcoded "GIR=[n] | GA=[n] | QA=[n] |
#               ENG=[n]" replaced with dynamic "[SecAbbr]=[n]" per actual sections[].
#           (B) BV reporting examples (§9-9): "× 4 sections", "GIR=62 GA=39 QA=42
#               ENG=54", "English: sum=24", "Cloze Test", "GIR: 3 subtopics",
#               "Calendar Day Calculation" all generalized to placeholders with
#               "illustrative" label.
#           (C) Rare threshold (§4-3): hardcoded 0.1 → configurable RARE_THRESHOLD =
#               bp.get('rare_threshold', 0.1). All 5 downstream references updated.
#               Exams with very few papers can lower it; exams with 500+ can raise it.
#           (D) Max rare per mock (§4-8 INVARIANT 4, §4-4, §9-4 BV-4): hardcoded 2 →
#               configurable MAX_RARE_PER_MOCK = bp.get('max_rare_per_mock', 2). All
#               code, validation, and delivery format references updated.
#           (E) Incomplete-doc threshold (§10-9): clarified as advisory heuristic that
#               never blocks B1 and applies across all exams equally.
#           (F) BV-10 rationale (§9-6b): SSC_CGL_TIER1_Mock01 Q77/Q78/Q79/Q80 example
#               generalized to "Q[x]+Q[y] = two find-opposite Qs" pattern. Error message
#               "synonym×2 or antonym×2" → "same-mechanic × 2".
#           (G) §14-6 and §14-7 JSON examples: "General Intelligence & Reasoning",
#               "gir.analogy.mixed_number_letter_analogy", "Analogy" → placeholder
#               format "[Section 1 Name]", "[section].[topic].[subtopic_slug]".
#           (H) EC-11 note: "SSC CGL Tier 1 (the primary exam)" → generic "typical
#               MCQ exams (25 Qs/section, ~60 subtopics/section)".
#           blueprint_version field updated to "1.16".
#
#   v1.15 — 2026-07-04 — DEEP-AUDIT (20 fixes across 7 categories).
#           CATEGORY A — Stale canonical step numbers (12 fixes):
#             Lines 53-54 (header OUTPUT FILES): "Step 4"/"Step 5" corrected to
#             "Step 9 (MockExplain)"/"Step 10 (MockExplainAudit)".
#             L2275: "Step 3 (MockCreateAudit)" → "Step 8 (MockCreateAudit)".
#             L3757: "Step 3 (MockCreateAudit)" → "Step 8 (MockCreateAudit)".
#             §13-5 (4 occurrences): all "Step 4" refs → "Step 9" (heading, body,
#             purpose, lifecycle).
#             §13-6 (4 occurrences): all "Step 5" refs → "Step 10" (heading, body,
#             purpose, lifecycle).
#           CATEGORY B — Deprecated "urgency loop" refs (5 fixes, stale since v1.13):
#             §4 Phase 2 description: "urgency" → "even-spread".
#             §8-3 Step 4d: "urgency loop: urgency-fill" → "even-spread: distribute"
#             (even-spread is the ONLY sanctioned method since v1.13).
#             §8-3 Step 4d: "counts for urgency" → "counts for remaining quota".
#             §8-3 BATCH GATE B2 reason text: "urgency scores" (×2) → "cumulative
#             counts" — the urgency loop is deprecated, these were stale artefacts.
#             §8-4: "compute urgency" → "compute remaining quota".
#             §8-3 Step 3 CRITICAL comment, §8-7, §9-10: "urgency scores" →
#             "assigned[] counts" (3 additional stale urgency references).
#           CATEGORY C — XLSX-4 checklist Total column value (1 fix):
#             "Total column = total_questions" → "Total column (F) = 100 (sum of
#             percentage values)" — Sheet 4 stores percentage numbers (15/30/55 summing
#             to 100), NOT Q counts. The prior text contradicted §15-4 which explicitly
#             states Col F = SUM(C:E) must equal 100.
#           CATEGORY D — Missing mandate enforcement step in §8-3 (1 fix):
#             §8-3 Step 4 previously listed: Phase 0 → Phase 1 → Phase 2 → column-fix,
#             with NO mandate enforcement step. Mandate rules M1/M2/M4/M6 must run
#             BETWEEN Phase 2 and column-fix (M2 rule (d) explicitly requires re-running
#             column-fix after resolution). Added Step 4e (mandate enforcement) and
#             renumbered column-fix to 4f, update-assigned to 4g.
#             S4-MANDATE stale cross-ref "§8-3 Step 5" corrected to "§8-3 Step 4e,
#             between Phase 2 and column-fix" (Step 5 is build_section_obj output, not
#             enforcement).
#           CATEGORY E — BV-0A location description (1 fix):
#             §9 header: "runs at the END of B1" → "runs DURING B1 (Step 4A)" — BV-0A
#             executes at Step 4A of B1 (midway), not at the end; "END" was misleading.
#           CATEGORY F — §14-1 schema gap (1 fix):
#             S14-1 JSON example and field definitions were missing total_options and
#             option_label. Both fields were documented in §8-2 Step 7 (B1 writing) and
#             consumed by Step 7 (MockCreate), but absent from the formal schema section.
#             Added to JSON example + full field definitions with cross-step SYNC notes.
#           CATEGORY G — Missing section header (1 fix):
#             BV-7 content at §9 had no ### S9-7 header — content started in a bare
#             code block between S9-6b and S9-8. Added "### S9-7 — BV-7: Full
#             cross-batch validation (runs in B3 only)".
#           blueprint_version field updated to "1.15".
#
#   v1.14 — 2026-07-03 — DEEP-AUDIT (1 fix). Header comment (line 41) stated the default
#           difficulty split as 20:30:50 (Easy:Medium:Hard), but the actual trigger parsing
#           (S1-1), the difficulty table (§7 S7-5 line 2144), the xlsx rendering (§15), and
#           every worked example all use 25:25:50. The header was stale — never updated when
#           the default changed. FIXED: header now 25:25:50. blueprint_version → "1.14".
#           No allocation behaviour change.
#
#   v1.13 — 2026-07-03 — ALLOCATION ALGORITHM & MANDATE INTERACTION FIX (7 issues).
#           Root cause: quota computation, Phase 0 forcing, even-spread collisions, and
#           mandate enforcement rules had structural gaps that caused 96+ F1 validation
#           failures in SSC CGL Tier 1. All fixes are exam-agnostic; no hardcoded values.
#           (1) §4-2 MANDATE-FIRST QUOTA RESERVATION: before the proportional r_avg split,
#               all M1/M4/M6 deterministic mandate totals are reserved from target_total.
#               Proportional split runs on remaining subtopics with remaining budget only.
#               This eliminates the quota-vs-mandate fight that was the root cause of 96 F1s.
#           (2) §4-5 PHASE 0 MULTI-MOCK SPREAD: forced batch-coverage assignments are now
#               spread backwards across all mocks in the window (b_end → b_start), using
#               per-mock remaining capacity, instead of dumping all uncovered subtopics
#               into mock b_end. Prevents overflow when uncovered_count > sec_qs.
#               Worked example added showing why single-mock forcing fails for GIR (56 vs 25).
#           (3) §4-5 PHASE 2 URGENCY LOOP DEPRECATED: the urgency loop is no longer a
#               sanctioned alternative. Pre-scheduled even spread is the ONLY method.
#               Urgency loop empirically failed variance ≤ 1 (GA section broke with zero
#               mandate involvement). Code retained as DEPRECATED with warning comment.
#           (4) §4-5 POSITION FORMULA DECORRELATION: pos formula added per-subtopic
#               phase-shift (subtopic_offset) to prevent two subtopics with same n_high
#               from colliding on identical mock positions. Note explains collision risk.
#           (5) §4-MANDATE M2 ALTERNATION TWO FIXES: (a) freed slot at source mock must
#               be backfilled from general nonrare pool, never given to the kept member;
#               (b) resolution runs as a fixed-point loop (repeat until zero conflicts
#               in a full pass), not a single pass — relocation can create new conflicts
#               at earlier, already-checked mocks.
#           (6) §4-MANDATE M4 MANDATORY_GROUPS: tie-break changed from highest-r_avg to
#               lowest-cumulative-total (spreads group presence across members instead of
#               biasing toward one). Upfront quota reservation added (same pattern as M1/M6).
#           (7) §17 S2-MANIFEST PRE-FLIGHT CHECK: new mandatory validation — every id in
#               mandatory_every_mock, min_counts, or cadence_windows must have r_avg > 0.
#               r_avg = 0 + mandatory = logical contradiction (ZP rotation caps at 5/50,
#               mandatory demands every mock). HARD STOP with explicit error if violated.
#               Catches manifest errors at load time, not three batches into generation.
#           DoD item 24 added (mandate/r_avg pre-flight).
#           blueprint_version field updated to "1.13".
#
#   v1.12 — 2026-07-02 — QUESTION METADATA INDEX — SCHEMA-SEED LAYER (Step-1 half). Additive,
#           exam-agnostic, zero allocation-behaviour change. (1) Seeds a new universal registry
#           field `question_index: []` in the Step-1 template (§12 S12-1 + field description +
#           all S12-3 examples + §8-5 Step-5 prose): mock-tagged {mock, questions:[{q,
#           subtopic_id, difficulty}]}, seeded here because RS-9 bars Step 2 from adding new
#           top-level fields (Step 2 only APPENDS; Step 3 re-syncs by key). (2) Carries
#           `difficulty_labels` verbatim from section_rules EXAM_STRUCTURE into blueprint.json
#           (default ['Easy','Medium','Hard']), mirroring nat_contract/msq_contract, so Step 2
#           and Step 6 read ONE canonical Complexity vocabulary; §14 schema + field-def added;
#           §7 S7-6 documents the fixed alias (simple→Easy/medium→Medium/hard→Hard) and the
#           SCHEDULE-FIRST assignment that makes the exact-equality distribution check
#           satisfiable by construction. Scope bound: non-3-band label sets also need S7-5 to
#           emit matching bands (flagged, not implemented; 3-band fully supported). Stale sample
#           blueprint_version literal corrected (1.10→1.12). Governed by
#           Contract_QuestionMetadataIndex v1.0; gate logic proven in Phase-1 before encoding.
#
#   v1.11 — 2026-07-01 — ISSUE 2b — THREE NEW MANDATE TYPES (build-time enforcement).
#           mandatory_every_mock (RULE M1) only expresses "one id in every mock". Step 0
#           v2.11 now publishes three more manifest structures that a flat list cannot:
#           mandatory_groups {group:{members,min}}, cadence_windows {id:N}, min_counts {id:k}.
#           Step 1 gains three enforcement rules mirroring M1's proven force-place pattern:
#             • RULE M4 (mandatory_groups) — PER-MOCK: >=min members of each group present;
#               force-place the group's highest-priority absent member if short.
#             • RULE M5 (cadence_windows) — CROSS-MOCK: each windowed id appears >=1 in every
#               sliding window of N consecutive mocks; enforced in the FULL-SERIES pass (BV-7),
#               NOT the per-mock loop (a single mock cannot express a window). This is why
#               Step 2 carries NO cadence gate — cadence is unobservable from one mock.
#             • RULE M6 (min_counts) — PER-MOCK: each id has q_count >= k (M1 generalised from
#               1 to k); force-place k-current, displacing lowest-r_avg non-locked subtopics.
#           BV-MANDATE (RULE M3) extended to assert M4 + M6 per mock and M5 across the series.
#           All check + force-place logic validated in Python on real SSC data (22 group +
#           50 min-count placements, section sums preserved, all rules satisfied) before
#           encoding. Exam-agnostic: empty structures ⇒ vacuous no-op. DoD items 21-23 added.
#   v1.10.1 — 2026-06-30 — MSQ CONTRACT PARITY (contract-sync fix). msq_contract now carries
#           msq_instruction + msq_instruction_hi, copied verbatim from section_rules,
#           structurally parallel to nat_contract.nat_instruction. Step 2/3 still read the
#           instruction from section_rules; this mirror is for visibility/parity so an auditor
#           sees the same contract shape for both answer types. Additive — Step 2 (k-mode/k)
#           and Step 4 (marking) reads are unchanged; inert when multi_select_allowed=false.
#   v1.10 — NAT CONTRACT — ALLOCATION LAYER (cross-step NAT extension, Step 1 half).
#           Carries the second answer-type axis through to blueprint.json, mirroring the v1.8
#           MSQ plumbing: reads per-subtopic `answer_type` ∈ {option, numerical} from
#           section_rules CATEGORY B into answer_type_map; derives top-level `nat_present`
#           (true iff any subtopic is numerical); copies the Step-0 EXAM_STRUCTURE NAT contract
#           verbatim into blueprint.json as `nat_allowed` + `nat_contract` {nat_answer_type,
#           nat_tolerance, nat_instruction}; stores `answer_type` per subtopic in
#           subtopic_list[]. Force-off guard: nat_present is forced False when nat_allowed=false
#           (dormant guarantee, mirrors the multi_present guard). An older section_rules lacking
#           answer_type defaults every subtopic to 'option' (no NAT) — no behaviour change for
#           non-NAT exams. Validated: AST clean; carry-through parity on NAT and non-NAT inputs.
#   v1.8 — MSQ CONTRACT — ALLOCATION LAYER (cross-step MSQ extension, Step 1 half).
#           DORMANT behind multi_select_allowed: for any exam without multi-select
#           (the default), v1.8 produces a byte-identical blueprint.json to v1.7 except
#           for additive inert fields (multi_present:false, answer_cardinality:"single",
#           multi_select_allowed:false). No allocation maths change.
#           Carries the Step-0 v2.5 MSQ contract forward so Step 2/4 can consume it:
#             (1) blueprint.json top-level gains multi_select_allowed, q_types, and the
#                 MSQ contract block (msq_k_mode, msq_k, negative_marking_by_type,
#                 partial_credit) — read verbatim from section_rules EXAM_STRUCTURE.
#             (2) NEW presence flag multi_present (parallel to passage/figural/di_present):
#                 True iff any subtopic has answer_cardinality=="multi". Step 2 reads it to
#                 enable the MSQ generation path.
#             (3) subtopic_list[] gains answer_cardinality ∈ {single, multi}, copied verbatim
#                 from section_rules CATEGORY B (Step 0 v2.5). This is the Step 2 dispatch
#                 unit. WHOLE-SUBTOPIC MODE (D2): a subtopic is uniformly single- or
#                 multi-answer, so the per-mock allocation schema is UNCHANGED — no MSQ
#                 sub-count is needed inside subtopic_allocations.
#           difficulty_schedule unchanged: MSQ inherits its subtopic's difficulty
#           (Step 0 E-9 already adds the MSQ load term). All MSQ values are config-driven
#           — zero exam names hardcoded. blueprint_version field updated to "1.8".



# ═══ ARCHIVE — Framework_MockTestCreateAudit pre-relocation header history (moved 2026-07-31 at v2.11; verbatim) ═══

# v2.10 — 2026-07-26 — NEW GATE A-FIGPROFILE (GAP-2026-07-26-003 D2).
#   Step 5 measures what a subtopic's real figures CONTAIN; Step 7 v5.31 now generates
#   against that profile. Nothing checked that it did. A-FIGPROFILE closes the loop.
#   It delegates the verdict to bc.check_figural_conformance(), the SAME function the
#   generator binds to, so the generator and its auditor share one rule and cannot
#   drift — the delegation contract audit_deep already enforces elsewhere.
#   AUDITS RECORDED INTENT, NOT PIXELS. Confirming a rendered PNG really depicts a
#   micrograph requires a view(), which is CLASS T and cannot run inside an audit's
#   python (see the EXECUTION-BOUNDARY LAW). Auditing the object_type Step 7 recorded
#   is deterministic, free, and catches the failure that matters: Step 7 ignoring the
#   profile. Whether a render matches its own label stays with the existing image-count
#   and composite gates.
#   SKIPs on an unconstrained profile — absent, empty, or vision_status='unavailable' —
#   which is what keeps ~200 pre-v2.37 exams passing untouched (EC-V18).
# v2.9.2 — 2026-07-22 — POSITION-BASED QUESTION TYPE IN AUDIT (GAP-2026-07-22-001 §6 FIX).
#   For question-type sections (IIT JAM: Section A=MCQ, B=MSQ, C=NAT), per-subtopic
#   answer_cardinality/answer_type is unreliable — multi_ids/nat_ids from subtopic_list
#   were empty or incomplete, causing A-MSQ-INSTR and A-NAT-INSTR gates to pass vacuously
#   (dormant) instead of validating MSQ/NAT instruction presence in the generated paper.
#   FIX: DUAL-MODE detection (mirrors Step 7 v5.30 and Step 11 v1.7):
#     > 1 distinct question_type in marking_scheme → POSITION-BASED:
#       expected_multi_by_section / expected_nat_by_section computed from marking_scheme
#       Q-ranges per section (not from per-subtopic IDs). multi_subtopic_ids / nat_subtopic_ids
#       augmented with ALL subtopics allocated to MSQ/NAT sections, so Part B semantic checks
#       and A-FIGCOMP stem_only routing work correctly.
#     0 or 1 distinct type → SUBTOPIC-BASED: unchanged pre-v2.9.2 behavior.
#   Edge cases:
#     - Section spans multiple marking_scheme ranges (e.g. GATE): per-Q _audit_type_for_q()
#       handles heterogeneous ranges within a single section correctly.
#     - No marking_scheme (legacy blueprint): _audit_distinct_q_types = {} → 0 types →
#       subtopic-based → byte-identical to pre-v2.9.2.
#     - multi_present=True but no per-subtopic multi_ids (position-based exam where
#       Blueprint v1.35 set the flag from marking_scheme): expected counts now correct.
#     - Scoped blueprints: always 0 or 1 distinct type (modal collapse) → subtopic-based,
#       unchanged.
#   Ships atomically with Framework_Blueprint.md v1.35 + Framework_MockTestCreate.md v5.30.
#
# v2.9.1 — 2026-07-20 — FINAL QA FIX: EXAM_CODE CROSS-VALIDATION + LEVEL/BP_LEVEL NAME
#   COLLISION (found during a full line-by-line adversarial re-audit of the v2.9 Test*
#   build). Two independent fixes:
#   (1) EXAM_CODE CROSS-VALIDATION (twin of Framework_MockTestCreate v5.29): the v2.9
#   {EXAM}*_blueprint.json glob (P0) is a PREFIX match — docx_slug matching alone is not
#   sufficient protection against a different ExamCode's blueprint being swept in, since
#   two different exams could coincidentally both have a "Mock07". FIX: P0 now asserts
#   bp['exam_code'] == EXAM immediately after pick_blueprint returns, HARD STOPPING with
#   an actionable message on mismatch.
#   (2) LEVEL/BP_LEVEL NAME COLLISION (real bug, not just a risk): v2.9's P0 introduced a
#   bare `LEVEL` variable for blueprint-scope selection ('mock'/'subject'/'topic'/
#   'subtopic'), but P2 ALREADY has a pre-existing `LEVEL = cat_c('level', 'unknown')` —
#   the exam's ACADEMIC level (e.g. "undergraduate"), an entirely different value.
#   Execution order happened to save v2.9 from a live misfire (P0's pick_blueprint call
#   completes before P2's reassignment), but any future code path reading LEVEL after P2
#   for blueprint-selection purposes would silently get the wrong value. FIX: renamed
#   the blueprint-scope-selector variable to BP_LEVEL throughout P0; the pre-existing
#   academic-level LEVEL at P2 is untouched.
#
# v2.9 — 2026-07-20 — TEST* TRIGGERS + DOCX-DRIVEN BLUEPRINT SELECTION (paper_pipeline.py
#   integration; twin of Framework_MockTestCreate v5.28). Adds TestCreateAudit P[N] as the
#   primary trigger (works for mock AND every scoped tier), keeping MockCreateAudit M[N] as
#   a working alias (implicitly level='mock'). WHAT CHANGED:
#     §2 S2-1 — new PRIMARY trigger TestCreateAudit P[N] [--level ...] [--scope ...];
#       MockCreateAudit M[N]/resume/status retained as the mock-only alias.
#     §2 S2-2 — registry-alignment check generalised to registry.papers_completed ending
#       with this paper's paper_id, falling back to legacy mocks_completed for a mock (same
#       fallback pattern already used elsewhere in this file, e.g. the existing
#       `papers_completed or mocks_completed` read at the Step-8 re-sync).
#     §3 P0 — blueprint resolution is now DOCX-DRIVEN: discovers the uploaded
#       [ExamCode]_*_Create.docx, parses its paper_slug from the filename, loads every
#       [ExamCode]*_blueprint.json present (mock + any scoped), and calls
#       pp.pick_blueprint(blueprints, level=BP_LEVEL, docx_slug=docx_slug) to identify which
#       ONE blueprint produced it — replacing the old hard assumption of a single
#       [ExamCode]_blueprint.json. Cross-checks the resolved paper_slug against the docx
#       filename; mismatch is a HARD STOP, never a guess.
#     §5 S5-1/S5-1A — invocation docs updated to reference [paper_slug] (pp.paper_slug,
#       zero-padded for a mock) and the ACTUAL resolved --blueprint path, instead of
#       assuming Mock[N]/blueprint.json literally.
#   Shared logic (paper_slug, pick_blueprint) lives ONLY in paper_pipeline.py. Does not
#   touch the Part-A/Part-B gate logic, MANDATE A-D, or the canonical auditor script
#   (Appendix A) itself.
#
# v2.8.1 — 2026-07-18 — SECTION-ID COLLISION FIX (found during a final adversarial
#   audit of Framework_MockTestCreate.md; docs-only, zero logic change). This file's
#   8 references to Step 7's canonical S7-NEW-B were pointing at a heading ID that
#   collided with an unrelated pre-existing section (figural generation mandate).
#   Renamed to S7-NEW-C, matching Framework_MockTestCreate.md v5.27. The one
#   pre-existing reference to the FIGURAL S7-NEW-B (line ~4413, unrelated to NAT
#   grading) is untouched. No gate, function, or value changed.
#
# v2.8 — 2026-07-18 — A-NAT-GRADE (NAT portal grading value self-consistency, part of the
#   same defect chain as Framework_MockTestCreate.md v5.25/v5.26 and explain_engine.py
#   v1.16). RA-12's NUMERICAL branch extended: the portal grading transform (S7-NEW-C in
#   Step 7) is a SEPARATE concern from math-value correctness — a NAT value can be right
#   while its portal string is wrong (the original defect: value 3×10⁻⁹ correct, sidecar
#   string "3e-9" wrong, which violates the delivery portal's "0123456789.-"-only grading
#   charset). TWO-LAYER enforcement, mirroring the existing A-NAT-ANSWER/A-NAT-NOOPT split:
#   (1) A-NAT-ANSWER (Claude-derivation, unchanged gate, extended scope) now also cross-
#   checks the grading transform against the SAME value it independently re-derives from
#   the stem; (2) new A-NAT-GRADE (machine) — a self-consistency backstop embedding a
#   PINNED byte-identical copy of derive_nat_grading() (Framework_MockTestCreate.md
#   §S7-NEW-C) that re-runs on the sidecar's OWN recorded (nat_value, ca_range,
#   stem_precision) and checks the result matches the sidecar's OWN recorded
#   (nat_grading_type, nat_grading_value) exactly, plus an independent charset allowlist
#   check. Dormant when no numerical subtopics exist, or when no answer_key sidecar was
#   supplied via --key (Step 8 does not receive it by default, S0-1) — matching the
#   existing concept_map-availability pattern already used by gate_images. Placed
#   deliberately BEFORE A-NAT-INSTR in gate_nat() (A-NAT-INSTR has an early `return` on its
#   own dormant path that would otherwise silently skip anything placed after it — caught
#   by actually running the self-test, not by inspection alone: an initial placement after
#   A-NAT-INSTR passed structural validation but failed the dynamic self-test at 50/51).
#   4 new self-test fixtures (catch / pass-with-stem-precision / dormant-no-nat /
#   dormant-no-key): 47 → 51. Total gate count unchanged at the A-* catalogue level (38
#   emitted machine/Claude-derivation gates was already inclusive; A-NAT-GRADE adds to the
#   45 documented A-* tokens). No change to any other gate's logic.
#
# v2.7.6 — 2026-07-18 — §6.4 PREVENTIVE FIX for A-INTEGRITY-FALSEPOS-01 (docs-only, zero
#   logic change). Added regression test 7 (HEADER-TOKEN-FALSE-POSITIVE) to §21's
#   REGRESSION TESTS list, documenting the exact fixture that would have caught the P0.5
#   false-positive defect (fixed at v2.7.5) before it reached a live exam session: a
#   real, well-formed section_rules.md built from Step 5's actual write_section_rules()
#   output MUST NOT trigger HARD STOP (P0.5 / A-INTEGRITY). Cross-references
#   validate_framework_md.py Check T (added same day), which now runs this class of
#   check automatically in batch mode. No code, gate, or self-test-count change; the
#   embedded audit.py self-test remains 47/47 PASS (this test lives at the P0.5
#   pre-flight layer, which is Claude-executed pseudocode, not part of the runnable
#   script — same precedent as regression tests 1-6).
#
# v2.7.5 — 2026-07-18 — FIX A-INTEGRITY-FALSEPOS-01: P0.5's section_rules.md integrity
#   check searched for the literal string "CATEGORY-C" (re.search(r'CATEGORY[\s\-]*C', ...))
#   as evidence the file was intact. "CATEGORY C" has only ever been an internal
#   documentation alias in Framework_MockTestAnalyse.md's prose/comments (§14) for the
#   file-level header block -- write_section_rules() has never written that literal string
#   to disk. The only literal token it ever writes is '=== EXAM_STRUCTURE ===' (since the
#   header's introduction at Step 5 v2.3). Net effect: P0.5 HARD-STOPPED on every valid
#   section_rules.md ever generated, for every exam, 100% reproducible, on every framework
#   build >= v2.6 (2026-07-08, when P0.5 was introduced) -- confirmed 100% Step 8 blocker,
#   first surfaced on MPSC_Botany M1 (2026-07-18). Fix: corrected the regex to
#   r'===\s*EXAM_STRUCTURE\s*===' (the actual producer-emitted token), matching how every
#   other consumer of this file (cat_c(), Steps 7/9/10/11) already reads it. True-positive
#   truncation detection is unaffected: the header is the first block write_section_rules()
#   emits, so a file truncated early enough to lose it still fails len(rt)<200 or the token
#   check; a file predating the header's v2.3 introduction still correctly fails (desired).
#   Updated the two matching prose references (S5-2 gate catalogue row, §17 edge-case
#   playbook row) for consistency. No data, no other exam project, no other step, and no
#   other file required any change (confirmed by exhaustive grep: this literal-CATEGORY
#   regex search existed in exactly one location in the entire 14-file spec repo). No
#   relaxation of the P0.5 HARD STOP / MANDATE B / MANDATE D policy.
#
# v2.7.4 — 2026-07-17 — FIX C PROPAGATION (byte-identical from Step 5 v2.24.6). The S6-1b
#   AXIS CLASSIFIER v1.0 (COPIED VERBATIM from Step 5) had the same naive substring DI
#   detection as Step 5's pre-fix classify_axis1 ('|' in stem or 'table' in stem.lower()),
#   which false-positived on any word merely CONTAINING "table" ("vegetable", "acceptable",
#   "notable", ...). Replaced with the SAME structural/word-boundary _looks_like_table_
#   stimulus() helper Step 5 v2.24.6 now uses (>=2 pipe-delimited rows, OR a word-boundary
#   table-keyword match co-occurring with >=1 pipe-delimited row). Required by this file's
#   own contract: "if Step 5's classifier changes, this copy MUST be updated to match."
#   No other change — MATCH detection (S6-1b's other rules) and the self-contained
#   A-MATCH-TABLE mirror detector (§ standalone audit.py block) are untouched (they don't
#   duplicate the table/DI check). Verified: dynamic embedded self-test SELF-TEST: 47/47
#   PASS unchanged; validate_framework_md.py 0 issues.
#
# v2.7.3 — 2026-07-15 — C3: paper_id PROPAGATION (Step 8; additive, mock output bit-identical).
#   Derives paper_id/paper_slug from the blueprint (Blueprint v1.29 C1; fallback "MOCK:M{N:02d}");
#   input/output docx use paper_slug ("Mock[N]" for a mock — unchanged); the S2-2 guard checks
#   papers_completed[-1]==paper_id; the question_index re-sync keys on paper_id and tags it.
#   Engine untouched. Proven by blueprint_c3_propagate_test.py. Pairs with MockCreate v5.21.
#
# [ExamCode] project | Step 8 (MockCreateAudit) | Universal Mock Test Auditor & Rectifier
#   v2.7.2 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#           Rectified-paper output renamed [ExamCode]_Mock[N]_Complete.docx →
#           [ExamCode]_Mock[N]_Create_Complete.docx. Input renamed accordingly: reads the
#           Step-7 paper [ExamCode]_Mock[N]_Create.docx. The output is now a DISTINCT file
#           from the input (no longer an in-place same-filename replace); the input is
#           retained. registry re-sync, conditional audit_changelog.md, every A-* gate and
#           the COMPLETION GATE unchanged. Chain re-verified against Step 7 / Step 9.
#   v2.7.1 — LANGUAGE-AGNOSTIC MATCH DETECTION + A-MATCH-TABLE gate. (1) Ported the SHARED
#           AXIS CLASSIFIER v1.0 update from Step 5 (Analyse v2.24.2) BYTE-IDENTICAL: new
#           _opts_are_match_pairs()/_label_family + a third MATCH trigger, so non-English
#           matches and matches whose List body sits in a table are re-tagged MATCH (were
#           silently DIRECT). Verified: dedented logic identical + 220/220 behavioural parity
#           with Step 5's copy. (2) NEW executable gate gate_match_table() → A-MATCH-TABLE:
#           promotes the S7-3 manual 'match must be a real grid' checklist to a machine gate —
#           any re-derived MATCH question with 0 <w:tbl> FAILs (rebuild the List body as a real
#           table). 2 new self-test fixtures (A-MATCH-TABLE-catch + -pass); self-test N 45→47
#           (>= AUTH_GATE_FLOOR 35). Exam-agnostic; no hardcoded exam/section label.
#   v2.7 — 2026-07-09 — A-HEADER INVERTED (strip pre-Q.1 block, not validate figures).
#           Pairs with Step 7 v5.18 (R8b / G-PREQ1). The generated paper is questions-only:
#           the first non-blank body paragraph MUST be Q.1. Previously A-HEADER only
#           VALIDATED a title/instruction block IF present (absence was "informational, not
#           a defect") and CP-HEADER merely corrected its figures — so a title/info/scoring
#           cover synthesised upstream survived the audit untouched (the gap the SSC CGL T1
#           Mock 1 report exposed).
#           (1) gate_header() inverted: any non-blank paragraph before Q.1 → A-HEADER FAIL
#               (was _warn/_ok). Fix path renamed CP-HEADER → CP-HEADER-STRIP (delete the
#               block; content-preserving). Dormant only if section_rules EXAM_STRUCTURE
#               declares paper_header_block (no current exam declares it).
#           (2) src-loader reads paper_header_block from CATEGORY-C (default off).
#           (3) S2-2 mock-number resolution trimmed to TWO sources (trigger + filename);
#               the title block is no longer read (it no longer exists).
#           (4) P5, the A-HEADER catalogue row, the gate-origin map, and the S8-1 fix-class
#               list rewritten to strip semantics. 2 new self-test fixtures (A-HEADER-catch
#               + A-HEADER-dormant): self-test count 43 → 45 (N >= AUTH_GATE_FLOOR 35). No
#               other gate changed.
#
#   v2.6 — 2026-07-08 — CLOSE THE FALSE-CLEAN CHAIN (Phase 2 now MECHANICALLY enforced).
#           ROOT CAUSE (surfaced in a real Step-8 run, SSC_CGL_TIER1 Mock 1, where the
#           auditor shipped a self-declared "CLEAN" paper after COLLAPSING Phase 2 into a
#           single spot-check pass): Part A (machine gates), MANDATE A (script self-test) and
#           MANDATE D (delivery timing) are RUNNABLE and HARD-STOP, but Part B (§6), §7,
#           B-FACT, and the whole §12-2/§18 certification gate were PROSE the model
#           self-attests. A run could therefore go Phase 1 → Phase 3 with a self-declared
#           "clean" and ship a paper whose per-question audit never ran. The one executable
#           artefact (audit.py) validated NONE of Phase 2. Compounded by three enablers:
#           (a) RA-15 FUSED exhaustiveness ("every question") with pacing ("pause between
#               batches") — an autonomous / "don't pause" preference dropped the per-question
#               audit along with the pause, because they were one rule;
#           (b) MANDATE A accepted a CONSTANT-PRINT self-test — the 13-gate minimum-viable
#               stub printed "SELF-TEST: 13/13 PASS" from a bare print() while its gate
#               bodies were hollow/truncated (and the pipeline runs THAT generated stub, not
#               this file's authoritative fixture-tested auditor — Appendix A had become
#               effectively unused);
#           (c) no input-corruption check — blueprint.json, registry.json and audit.py all
#               arrived TRUNCATED via the project-knowledge sync, and P0 hard-stops on MISSING
#               files, not truncated ones.
#           SEPARATION OF CONCERNS (important): the hollow-script defect (b) and the
#           skipped-Phase-2 defect are INDEPENDENT false-clean vectors. Even a perfect Part-A
#           auditor cannot detect a skipped Phase 2 — Phase 2 is semantic/visual/factual and
#           out of Part A's scope entirely. Both are closed here.
#           FIX A — MANDATE B (boxed, top-level): Phase 2 may NEVER be skipped, compressed
#                   into a single pass, or spot-checked — in ANY mode (interactive OR
#                   autonomous). See MANDATE B.
#           FIX B — RA-0 PRECEDENCE + RA-15 SPLIT (RA-15a EXHAUSTIVENESS / RA-15b PACING) +
#                   S4-3A AUTONOMOUS mode. Autonomy waives the inter-batch PAUSE ONLY, never
#                   the per-question review. No preference may reduce coverage or weaken the
#                   completion gate (RA-0).
#           FIX C — S5-1A COMPLETION GATE (the keystone): `--final --audit-state <path>`
#                   validates the §9-1 audit_state.ledger (C1–C7) AND the on-disk EVIDENCE
#                   artefacts each stamp references. Required by §12-2 and Phase-3 STEP 1;
#                   a bare --final (Part A only) NO LONGER certifies. Converts §12-2/§18 from
#                   self-attested prose into a command EXIT CODE. This single change makes a
#                   skipped Phase 2 fail LOUDLY (C1/C2) instead of shipping.
#           FIX D — P1 HARDENED: --self-test must be the FIXTURE-BASED authoritative self-test
#                   (builds docx fixtures, asserts each gate catches a planted defect AND
#                   passes a clean one), N >= AUTH_GATE_FLOOR (35). A constant-print stub that
#                   merely emits "N/N PASS" is REJECTED. MANDATE A wording tightened.
#           FIX E — P0.5 INPUT INTEGRITY (A-INTEGRITY): json.load / ast.parse every input;
#                   HARD STOP on corruption/truncation; sanctioned repair for audit.py ONLY
#                   (regenerate from the canonical template, must then pass the hardened
#                   self-test), logged; NEVER silently repair blueprint/registry DATA.
#           FIX F — EVIDENCE-BOUND STAMPS (§9-1 / §7 / S5-1A): every 'rendered-and-viewed'
#                   stamp NAMES a montage PNG on disk; every fact_source NAMES a saved
#                   search-result file; every 'recomputed' stamp NAMES a recompute-trace file.
#                   C5/C6 verify the FILES exist and are non-trivial — so a ledger cannot be
#                   fabricated without producing the evidence, i.e. without doing the work.
#                   This is what pushes the gate from "hard to fake" toward "cannot fake
#                   without performing the audit".
#           §16/§17/§18 wired; glossary + invariants + edge-cases updated. ABSENT-SAFE: a run
#           with a complete, evidence-backed ledger behaves exactly as v2.5 plus the extra
#           assertions; a legacy audit_state with no evidence dir fails C5/C6 LOUDLY (never
#           silently passes).
#           CROSS-FILE (apply IN LOCKSTEP — see §21): Framework_Blueprint.md §13-7A (the
#           Step-6 B3 generator — where the auditor is BORN, once per exam) and
#           Framework_MockTestCreate.md Appendix A MUST generate EXACTLY this v2.6 auditor
#           (--audit-state + C1–C7 + fixture self-test), or the fix never reaches the ~200
#           exams. validate_framework_md.py gains the 6 regression tests (§21). Step 10
#           (MockExplainAudit) and Step 9's §18 self-audit carry the SAME false-clean chain
#           and must get the parallel completion-gate pattern.
#
#   v2.5 — 2026-07-07 — THREE-AXIS FORMAT-DISTRIBUTION AUDIT (File 4 of the feature — closes the
#           loop; reads Step 6 v1.23 axis_schedule + the counts Step 7 v5.14 renders).
#           A mock must replicate the exam's FORMAT MIX. Step 8 INDEPENDENTLY re-tags every
#           shipped question with the Step-5 classifier and audits the realized per-window Axis
#           distribution against the blueprint target — the mirror of B-DIFF for format.
#
#           FIX A — SHARED AXIS CLASSIFIER v1.0, COPIED VERBATIM from Step 5 (§AXIS-CLASSIFIER).
#             classify_axis1/2/3 + tag_axes + _opts_are_combination_labels + AXIS2_CLASSES are
#             byte-identical to Step 5; the PYQ target and the generated distribution are only
#             comparable if classified by the SAME functions. Re-implementation is forbidden.
#
#           FIX B — PER-QUESTION RE-TAG (independent, from the docx — Step 8 has NO concept_map).
#             In S6-0 extraction every question is re-tagged from its rendered stem/options/
#             artefact-map; axis1/axis2/axis3/is_negative are stored on the §9 ledger entry.
#             is_negative uses the EXACT Step-5 EC-12 regex (uppercase NOT|INCORRECT|EXCEPT|
#             FALSE|WRONG, no re.I) so the target rate (Step 6) and realized rate (here) count
#             identically — a broader detector would inflate the rate and fire false WARNs.
#
#           FIX C — INDEPENDENT WINDOW TALLY in registry.axis2_audit (decision A). Because Step 8
#             audits one mock per run, the per-10-mock-window counts accumulate here (window-aware
#             reset), re-derived from each mock's docx — trusting nothing. Cross-checked against
#             Step 7's registry.axis2_window (a large drift ⇒ WARN: the paper's actual structure
#             diverged from the variant Step 7 declared). Preserved through §13 re-sync (setdefault).
#
#           FIX D — S6-6 FORMAT-DISTRIBUTION AUDIT (advisory, mirrors B-DIFF / S6-5, decision B):
#             B-AXIS2 (per-section, per-format, per-window: band = ±1 or ±15% whichever larger;
#             guarantee = ≥1/window; DIRECT floats), B-AXIS1 / B-AXIS3 (realized vs Step-6 target
#             within tolerance), B-AXIS-NEG (negative-rate soft WARN, decision 12). A shortfall is
#             a generation-quality FINDING in the report; it blocks SHIP only if section_rules/
#             blueprint marks the format mix hard (the RA-9 parallel). Fires only at WINDOW CLOSE
#             (N % batch_size_qs == 0 or N == total_mocks), from the FINAL fixed docx (Phase 3).
#
#           FIX E — dashboard + report lines; registry.axis2_audit in REQUIRED_TOP self-heal.
#             Everything is ABSENT-SAFE: a pre-v1.23 blueprint (no axis_schedule) ⇒ the whole
#             Axis audit is inert and Step 8 behaves exactly as v2.4. version → v2.5.
#
#   v2.4 — 2026-07-07 — FIGURAL IMAGE_ROLE-AWARE AUDIT (mirrors Step 7 v5.13).
#           ROOT CAUSE: Step 7 v5.13 added 3-way figural rendering (stem_and_options /
#           stem_only / options_only) with add_figural_stem_question() and expanded
#           G-FIGTEXT (3-tier) + G-FIGURAL-COMPOSITE (image_role-aware). Step 8 must
#           mirror these so the independent audit catches what Step 7 missed.
#
#           (1) A-FIGCOMP gate table entry updated: now image_role-aware with 3 branches
#               (stem_and_options: ≥n_opt+1 images; stem_only: ≥1 problem image, option-
#               image arm skipped; options_only: ≥n_opt images, no problem required).
#               Reads image_role from section_rules PYQ_IMAGE_ANALYSIS per subtopic.
#           (2) A-FIGCOMP code (gate_images): updated to read image_role and branch the
#               minimum-image check accordingly. Single-image composite warning now only
#               fires for stem_and_options (for stem_only, 1 image IS correct).
#           (3) Traceability mapping updated: A-FIGCOMP now traces to Step 7's S10-8A
#               (add_figural_stem_question) in addition to S10-8.
#           (4) G-FIGTEXT-PROSE tertiary check mirrored: any Q-block with 0 images +
#               figure-reference text → FAIL. Catches misclassified TEXT subtopics.
#           (5) §7 V-image note updated to cover stem_only verification.
#
#   v2.3 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S14-6: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. F2 (step-complete) footer rendered
#           after the single present_files call and status report. Zero logic change.
#   v2.2 — 2026-07-06 — AUDIT SCRIPT SOURCE UPDATED (EC-A3).
#           Step 6 (MockBlueprint) v1.20+ now auto-generates [ExamCode]_mock_test_audit.py
#           as its 6th output file. Step 8 MANDATE A HARD STOP message, D4 design note,
#           P0 missing-file hint, P1 fallback reference, §17 edge-case playbook row, and
#           Appendix A header updated to reference Step 6 auto-generation instead of
#           manual creation. MANDATE A remains MANDATORY — the script must still exist
#           in project Files for Step 8 to run; only the SOURCE has changed (auto-generated
#           by Step 6, not manually created by user). Appendix A script code UNCHANGED.
#           No audit logic, gate, or self-test change.
#
#   v2.1 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (new blueprint fields).
#           Step 6 v1.19 now carries marking_scheme[], level, medium in blueprint.json.
#           Step 8 reads these at P2 for availability. No new audit gates — these fields
#           are structural metadata consumed by Steps 7/9/11, not auditable mock content.
#           sections[] comment updated to include max_attempt.
#           CATEGORY C now also reads marking_scheme, level, medium via cat_c() for
#           header validation (P5) when the mock paper prints marks information.
#
#   v2.0 — 2026-07-04 — TITLE/FILENAME ALIGNMENT + CROSS-STEP SYNC VERIFICATION.
#           (1) TITLE/FILENAME MISMATCH: header, §1-1 spec reference, Appendix A header,
#               and footer all said "Framework_MockCreateAudit" but the filename is
#               Framework_MockTestCreateAudit.md (missing "Test"). FIXED: all 4 now match
#               the filename. The step name "MockCreateAudit" and trigger format are
#               UNCHANGED (they are the step's canonical name, not the filename).
#           (2) Changelog generator and session_log audit_version stamps bumped to v2.0.
#           (3) CROSS-STEP SYNC VERIFIED against current versions: Step 7 v5.8 (delivery
#               contract, REQUIRED_TOP, options_by_q/section_names field names), Step 9 v1.9
#               (input contract unchanged since v1.6 — v1.7/v1.8/v1.9 were documentation +
#               engine-code-only), Step 10 v1.5 (question_index frozen/read-only contract),
#               Step 11 v1.0 (question_index JOIN consumption). All contracts in sync.
#           (4) UPSTREAM NOTE (Step 7 v5.8): Step 7's REQUIRED_TOP is missing section_names,
#               options_by_q, rc_manifests, figural_manifests — fields Step 7 writes at S13
#               but doesn't self-heal. Step 8's REQUIRED_TOP already covers all four.
#               Flagged for the Step 7 audit pass (not a Step 8 bug).
#           No logic change; self-test stays 35/35.
#   v1.9 — 2026-07-04 — CROSS-STEP SYNC (Step 7 v5.8 alignment + 1 schema fix).
#           (1) CANONICAL STEP RENAMING: Step 7 v5.8 already updated all its
#               cross-references to use canonical numbering (Step 8/Step 9). This file's
#               body still used legacy "Step 2" / "STEP 2" / "STEP-2" (47× mixed-case)
#               for Step 7 and "Step 3" / "STEP 3" / "STEP-3" (61× mixed-case) for
#               Step 8 — creating a readability mismatch with the upstream spec. FIXED:
#               all 119 body references now use canonical Step 7/Step 8 (including
#               MANDATE A heading, RA-6 heading, STATUS REPORT title, gate glossary
#               STEP-8-ONLY label). Version history preserved unchanged.
#           (2) REQUIRED_TOP missing `section_names`: Step 7 v4.8 writes
#               reg['section_names'] (consumed by G-SECTIONHDR and documented as
#               "consumed by Step 8 A-SECHDR"). But Step 8's schema-heal REQUIRED_TOP
#               did not include it — a missing section_names would not be self-healed.
#               FIXED: added to REQUIRED_TOP (default []).
#           Cross-step contract verified against: Step 7 v5.8 (delivery contract,
#           REQUIRED_TOP, field names, section numbers S13-4/S13-6); Step 9 v1.6
#           (input contract, options_by_q consumption, question_index frozen status);
#           Step 11 (question_index JOIN consumption); Blueprint v1.14 (section 'name'
#           vs 'section_name' field handling). No logic change; self-test stays 35/35.
#   v1.8 — 2026-07-04 — DEEP-AUDIT (18 bugs fixed).
#           PASS 1 — step numbering + version stamps (13 fixes):
#           (1) PIPELINE POSITION downstream steps used legacy numbers (Step 4/5/6) and a
#               non-existent step name ("MockTestSort") — FIXED: Step 9 (MockExplain),
#               Step 10 (MockExplainAudit), Step 11 (MockDeliver); range corrected to 7–11.
#           (2) 13 references to "Step 4 (MockExplain)" / "Step-4 task/artefact" throughout
#               the spec body used legacy numbering — FIXED: all now Step 9/Step-9.
#           (3) Two references to an undefined "MANDATE-1" (inherited from Step 7's spec) — FIXED:
#               replaced with RA-15 (this spec's own equivalent rule).
#           (4) PURPOSE section "Step 3/4" → "Step 8/9" (2 occurrences).
#           (5) Appendix A script header said "Framework_MockCreateAudit v1.0" — FIXED: v1.8.
#           (6) Appendix A validation status said "(v1.2)" — FIXED: "(v1.8)"; test coverage
#               description now mentions v1.4 NAT cases + v1.5 SECHDR-name-catch.
#           (7) _find() docstring was invalid Python (adjacent string literals not
#               concatenated across physical lines) — FIXED: triple-quoted docstring.
#           PASS 2 — exam-agnostic rigidity (5 fixes):
#           (8) gate_optref DEAD CODE: `extra` read from section_rules escape tokens but
#               NEVER merged into the token list — the gate only ever checked hardcoded
#               English phrases ('no error', 'none of these', etc.). Also 'if there is no
#               error' was a separate hardcoded literal. FIXED: section_rules escape tokens
#               are merged as PRIMARY; escape_stem_triggers configurable via src.
#           (9) STIMULUS_CUES hardcoded English-only phrases ('the passage', 'the table',
#               'according to the passage', etc.) — non-English exams (Hindi, Tamil, etc.)
#               would never trigger stimulus detection. FIXED: gate_stimorphan now merges
#               section_rules stimulus_cue_patterns (if declared) with the built-in defaults.
#           (10) gate_header hardcoded `\bmock\b` regex — non-English exams using "मॉक" or
#                other title keywords would always WARN. FIXED: reads mock_title_keyword from
#                section_rules (default 'mock').
#           (11) gate_images HARDCODED figural stem keywords ('mirror','water image' etc.)
#                violating RA-9 — FIXED: reads figural_cue_keywords from section_rules.
#           (12) B-DIFF prose hardcoded "Simple/Medium/Hard" — FIXED: references
#                blueprint.difficulty_labels (the runtime source).
#           No logic change; self-test stays 35/35.
#   v1.7 — 2026-07-03 — DEEP-AUDIT (3 version-stamp fixes).
#           (1) Footer said "v1.1", header was v1.6 — never updated past v1.1.
#               FIXED: footer now v1.7.
#           (2) Change-log file header generator wrote "MockCreateAudit v1.1" into
#               every generated change-log. FIXED: v1.7.
#           (3) Registry session_log audit_version stamp was hardcoded "1.0" — every
#               audit session log entry falsely claimed v1.0 regardless of spec version.
#               FIXED: "1.7". No logic change; self-test stays 35/35.
#   v1.6 — 2026-07-02 — QUESTION METADATA INDEX — CERTIFIER LAYER (cross-step index extension,
#           Step-3 half). Additive, exam-agnostic, writes NOTHING to the docx. §13 re-sync now
#           rebuilds registry.question_index for mock N BY KEY (new step 2b): subtopic_id is taken
#           from Step 3's INDEPENDENT re-derivation (the §9 audit ledger; B-ALLOC content->id) —
#           never trusted from Step 2; a Step-2/re-derivation disagreement is logged as a labelling
#           defect and the re-derived id wins; a regenerated Q keeps its slot id so re-derivation
#           agrees by construction. difficulty is CARRIED FORWARD from Step 2's incoming index
#           (difficulty is not rendered in the paper and not re-derivable from it, §19; regeneration
#           preserves the target so the carried value stays correct). REQUIRED_TOP (schema-heal) now
#           includes question_index; S13-3 verification adds a check mirroring Step 2 G-QINDEX (one
#           mock-N object; q=1..total_questions sorted/unique/complete; ids ∈ blueprint; difficulty
#           ∈ difficulty_labels; distribution == schedule[N] exactly). §19 documents the two-tier
#           guarantee (subtopic_id independently re-derived + certified; difficulty authoritative-
#           by-assignment + distribution-verified). No new A-* docx gate — question_index is a
#           registry field, certified in the §13 re-sync path. Governed by
#           Contract_QuestionMetadataIndex v1.0; re-sync logic proven in the Phase-1 harness.
#   v1.5 — 2026-06-30 — A-SECHDR SECTION-NAME DETECTION (mutation-harness finding). The
#           mutation-testing harness found a hole: A-SECHDR pattern-matched only the literal
#           keywords "section"/"part"/rule-chars, so a stray heading that IS a declared
#           SECTION NAME ("Quantitative Aptitude", "Technical") in the body was NOT caught
#           (the realistic section-header form), and the scan only covered paragraphs inside
#           question blocks. FIX: gate_sechdr now (a) also flags a standalone body paragraph
#           equal to a declared section name (provenance-based — matched against
#           src['sections'], exam-agnostic), and (b) scans ALL body paragraphs (a heading
#           before Q.1 / between blocks is seen too). New self-test A-SECHDR-name-catch;
#           SELF-TEST 34 -> 35. Non-offending papers unaffected.
#   v1.4 — 2026-06-30 — NAT CONTRACT — AUDIT LAYER (cross-step NAT extension, Step 3
#           half). DORMANT behind the blueprint's nat_present flag; every NAT path is gated
#           so a non-NAT mock behaves exactly as v1.3.
#             (1) src re-derives the NAT axis INDEPENDENTLY: nat_present, nat_subtopic_ids,
#                 expected_nat_by_section (from blueprint allocations), nat config, and
#                 nat_instruction phrases; options_by_q is read from the registry (ND6
#                 delivery contract, NOT a self-audit sidecar).
#             (2) RA-12 GENERALISED with a NUMERICAL branch (supersedes cardinality): the
#                 re-derived VALUE must be uniquely determined, form-matched to nat_answer_type
#                 (integer⇒integral; real⇒within ca_range lo≤hi), 0/neg/fractional valid,
#                 non-leaking. B-SOLVE yields a VALUE (compared numerically within tolerance,
#                 ND13 — never string equality); B-UNIQUE checks unique determination;
#                 B-DISTRACT is N/A (no options); B-LEAK checks the numerical value.
#             (3) OPTION GATES (A-OPTN/A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE) SKIP NAT questions
#                 (options_by_q==0); A-KBAL/A-KPAT exclude NAT (as they exclude multi).
#             (4) A-ANSKEY leak scan extended to NAT numerical keys ("Q.5 → 47" incl.
#                 0/negative/decimal — the option-digit patterns missed them).
#             (5) NEW catalogue gates: A-NAT-NOOPT (machine — a 0-option-marked Q renders
#                 zero options), A-NAT-INSTR (machine — per-section numerical-instruction
#                 count matches the blueprint), and A-NAT-ANSWER (Claude-derivation — value
#                 well-posed/form-matched/non-leaking; claude_side like A-KINT/A-MSQ-KEY).
#                 gate_nat() emits the two machine gates; both are dormant when nat_present is
#                 false. A-FIGCOMP gains a figural-NAT variant (ND10: problem image, ZERO
#                 option images); RA-16 admits NAT members in linked/DI groups (ND11).
#             (6) SELF-TEST extended with 6 NAT fixtures (A-NAT-NOOPT catch/pass/dormant,
#                 A-NAT-INSTR catch/pass/dormant): 28 → 34; the prose SELF-TEST count is
#                 bumped in lockstep (E-CONST). validate_framework_md.py: 0 issues, 34/34.
#   v1.3 — 2026-06-30 — VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Pure
#           rename, no behaviour change: per-subtopic `answer_mode` -> `answer_cardinality`
#           (RA-12, B-*, ledger, gate logic, src); blueprint flag `msq_present` ->
#           `multi_present`. Blueprint reads accept the OLD names as a fallback. Non-MSQ
#           exams byte-identical to v1.2. Validated: validate_framework_md.py 0 issues,
#           SELF-TEST 28/28; the extracted auditor re-run GREEN on the MSQ e2e fixtures with
#           BOTH old-name and new-name blueprints (back- and forward-compat). First step of
#           the Steps 0-4 single-vocabulary alignment (answer_type + answer_cardinality).
#   v1.2 — 2026-06-30 — MSQ CONTRACT — AUDIT LAYER (cross-step MSQ extension, Step 3
#           half; mirrors Step 2 v4.5). DORMANT behind the blueprint's
#           multi_select_allowed / multi_present and each subtopic's answer_cardinality: for any
#           single-answer exam (the default, incl. SSC CGL) v1.2 audits identically to
#           v1.1. Step 3 remains the INDEPENDENT auditor — it does NOT trust any Step-2
#           self-report: it RE-DERIVES answer_cardinality per question from blueprint
#           subtopic_list (by subtopic_id), RE-DERIVES the correct SET by solving, and
#           reads MSQ config (total_options, msq_k_mode, msq_k, msq_allow_aota) from
#           section_rules / blueprint — never from the Step-2 answer_key sidecar (which
#           Step 3 never reads; RA-1).
#             (1) RA-12 GENERALISED to mirror Step 2 R-ANSWER (both modes): single →
#                 exactly one defensible option; multi → the correct SET S is a non-empty
#                 PROPER subset of {1..OPTIONS_COUNT} (1≤|S|≤n−1; |S|=msq_k when fixed),
#                 every in-set option defensible under EVERY fair reading and every
#                 out-set option indefensible under ANY fair reading; negation composes.
#             (2) B-SOLVE now yields a SET for multi questions (the re-derived S), not a
#                 scalar; B-UNIQUE becomes a SET-MATCH (re-derived S must equal the set the
#                 paper marks — but Step 3 has no marked key, so it verifies S is internally
#                 well-formed per RA-12 and that exactly the in-set options are defensible);
#                 B-DISTRACT checks the (OPTIONS_COUNT − |S|) OUT-set options are each
#                 indefensible (a borderline out-set option is the MSQ ambiguity defect).
#             (3) A-KINT extended: the re-derived key per question is a single int (single)
#                 OR a non-empty proper subset (multi). A-KBAL and A-KPAT now EXCLUDE
#                 multi-mode questions from the single-position balance/run statistics (a
#                 set has no single position; mirrors Step 2 K-BAL/K-PAT msq_positions).
#             (4) A-ANSKEY leak scan extended to set-valued keys ("Q.1 → 1,2,4") — the
#                 single-digit pattern missed comma/space lists (mirror Step 2 G-ANSWERKEY).
#             (5) NEW catalogue gates: A-MSQ-KEY (Claude-derivation check — the re-derived
#                 set is a well-formed non-empty proper subset, fixed-k honored, AOTA rule
#                 honored; added to the validator's claude_side alongside A-KINT/KBAL/KPAT)
#                 and A-MSQ-INSTR (machine docx scan — the select-instruction is present in
#                 the Q.<n> stem line; EMITTED by the embedded script). Both run MULTI-only.
#             (6) LEDGER schema mirrors set values: derived_answer → may be int|list;
#                 added answer_set_verified (bool) and answer_fact_values (list) so B-LEAK
#                 scans EVERY value in a multi answer set, not just one (P3-1).
#             (7) B-LEAK generalised: for a multi question every value in the re-derived
#                 set is checked for illegitimate appearance as an option elsewhere.
#             (8) B-DIFF mirrors Step 0 E-9: an MSQ adds a difficulty-load term (advisory).
#             (9) RECTIFICATION: re-balancing for A-KBAL/A-KPAT skips MSQ positions; when a
#                 multi question is regenerated, the WHOLE correct SET is preserved/re-formed
#                 (never "change which single option is correct"); A-MSQ-KEY/INSTR get their
#                 own rectification routes.
#            (10) SELF-TEST extended with MSQ fixtures (well-formed set, k=0, k=n, fixed-k
#                 violation, AOTA-under-multi, set-leak, instruction-in-stem); the prose
#                 SELF-TEST count is bumped in lockstep (E-CONST). validate_framework_md.py
#                 claude_side updated to include A-MSQ-KEY so C-GATE stays satisfied.
#           All MSQ behaviour is config-driven (multi_select_allowed / answer_cardinality /
#           msq_k_mode / msq_allow_aota) — zero exam names hardcoded. Validated: the
#           project validator returns 0 issues (gate-code + self-test-count consistency),
#           and the new audit logic was parity-checked in Python against the Step-2 MSQ
#           fixtures before encoding.
#   v1.1 — 2026-06-29 — Reporting upgrade (no logic change to the audit itself):
#           (a) a STATUS REPORT dashboard is printed in chat at delivery (§14-4) —
#               a scannable verdict + coverage + on-arrival→after-rectification
#               delta; (b) a per-question REGENERATION CHANGE-LOG is added to the
#               report (§R5) and, when any question was regenerated, a downloadable
#               author-only change-log artefact carrying the literal before/after
#               diff is delivered alongside the core set (§14); (c) the in-chat
#               fact-verification summary is made strictly content-free (counts +
#               that sources were logged — never the facts themselves), closing a
#               latent MANDATE-0 leak in the old §R8; (d) report adds a coverage
#               matrix (proves zero sampling) and a defects-by-class rollup (surfaces
#               systemic Step-2 issues). The closed-set discipline is preserved: the
#               core deliverable stays {docx, registry}; the change-log is an
#               explicitly-demarcated audit artefact shipped only when regenerations
#               occurred. See S8-5, §14-1..§14-5, §R0/§R5/§R8/§R14/§R15, DoD #12.
#   v1.0 — 2026-06-29 — Initial release. Independent audit + in-place
#           rectification of the Step-2 mock paper. Built exam-agnostic from
#           the ground up (zero hardcoded exam values — every count, format,
#           label, language, difficulty band, escape token and figural type is
#           read at runtime from blueprint.json / section_rules.md /
#           subtopic_manifest.json / registry.json). Re-verifies, independently,
#           every Step-2 generation contract (R1–R24, R-DELIVER, R-LINKED,
#           R-FIGURAL, R-UNDERLINE, R-OPTREF, R-UNIQUE, R-MATH-OMML and the 57
#           Step-2 gates) WITHOUT trusting the Step-2 self-audit sidecar, then
#           rectifies every defect in place and ships a 100%-verified, zero-
#           defect paper. Design decisions locked with the framework owner:
#             D1. Step 3 receives ONLY {Mock[N]_Create.docx, registry.json}
#                 (Step-2 closed delivery set, S13-6). The answer-key/concept_map
#                 sidecar is NEVER delivered, so Step 3 is fully INDEPENDENT:
#                 it solves every question itself to verify answer uniqueness and
#                 correctness. Definitive key-adjudication remains a Step-9 task.
#             D2. Rectify-in-place. Mechanical/rendering defects are fixed in the
#                 docx directly; any defect needing new content REGENERATES that
#                 one question in place under Step 2's own contracts, then re-
#                 audits it. Step 3 never hands a broken paper back to a human.
#             D3. The deliverable is the RECTIFIED docx + a registry RE-SYNCED
#                 from the fixed file (mock-N slice rebuilt). Not a verdict report.
#             D4. A universal, exam-agnostic mock_test_audit.py is auto-generated
#                 by Step 6 (MockBlueprint) v1.20+ as its 6th output file; it is
#                 MANDATORY for Step 8 (hard stop if absent), unlike Step 7 where
#                 it is optional. See Framework_Blueprint.md §13-7A.
#             D5. Every figure, image, table, matrix, chart and OMML expression
#                 is audited at pixel/cell/node depth — rendered-and-viewed or
#                 arithmetically recomputed — never pattern-matched (§7).
#             D6. Live web-verification of every current-affairs / static-GA fact
#                 and every factual option (never certified from memory).
#             D7. Batch rhythm mirrors Step 2: semantic review runs in batches of
#                 ≤ AUDIT_BATCH_SIZE (default 10) questions, each gated by an
#                 explicit "continue"; linked-stimulus groups are atomic; the
#                 final batch auto-runs certification + delivery (no "continue").
#


# ═══ ARCHIVE — Framework_MockTestExplain pre-relocation header history (moved 2026-07-31 at v1.20; verbatim) ═══

# v1.19 — 2026-07-20 — TEST* TRIGGERS + DOCX-DRIVEN BLUEPRINT SELECTION (paper_pipeline.py
#   integration; twin of Framework_MockTestCreateAudit v2.9). Adds TestExplain P[N] as the
#   primary trigger (works for mock AND every scoped tier), keeping MockExplain M[N] as a
#   working alias (implicitly level='mock'). WHAT CHANGED:
#     §2 S2-1 — new PRIMARY trigger TestExplain P[N] [--level ...] [--scope ...];
#       MockExplain M[N]/resume/--status retained as the mock-only alias.
#     §2 S2-2 — registry check generalised to registry.papers_completed containing this
#       paper's paper_id, falling back to legacy mocks_completed containing N for a mock.
#     §3 P1 — blueprint load is now DOCX-DRIVEN: discovers the uploaded
#       [ExamCode]_[paper_slug]_Create_Complete.docx, parses its paper_slug from the
#       filename, loads every [ExamCode]*_blueprint.json present, and calls
#       pp.pick_blueprint(blueprints, level=LEVEL, docx_slug=paper_slug) — replacing the
#       old hard assumption of a single [ExamCode]_blueprint.json.
#     §19 S19-1/S19-2 — output filename now f'{EXAMCODE}_{PAPER_SLUG}_Explanation.docx'
#       (PAPER_SLUG = pp.paper_slug(paper_id) from P1), replacing the hardcoded
#       f'{EXAMCODE}_Mock{NNN}_Explanation.docx' — the old form only ever worked for mocks.
#   Shared logic (paper_slug, pick_blueprint) lives ONLY in paper_pipeline.py. Does not
#   touch explain_engine.py, the §18 self-audit, or any solving/derivation logic.
#
# v1.18 — 2026-07-18 — LIVE SELF-TEST COUNT FIX (found during an actual deployment attempt
#   in a downstream project — this file's own P0 pre-flight gate hard-demanded exactly
#   "SELF-TEST: 44/44 PASS" from explain_engine.py, which has legitimately read 62/62 since
#   v1.16/v1.17 of that file (NAT charset guard fixtures). This is the SAME class of defect
#   already fixed in Framework_MockTestExplainAudit.md v1.12 — that file's live references
#   were checked and corrected then; this file's OWN live references were never checked,
#   an omission, not a deliberate scope decision. Had this shipped as-is, Step 9 would have
#   hard-stopped at its own P0 pre-flight on every single run, unconditionally, on any
#   project using the current engine — this was a deploy-blocking defect, not cosmetic.
#   FIX: 6 live requirement statements corrected to 62/62 — the self-test-with-self-test
#   description near MANDATE B, the P1 pre-flight instruction (§ near P6 RESUME), the
#   session-status template, §R1 PROVENANCE's reporting line, §21's Definition-of-Done
#   invariant, and Appendix A's engine-module description. 5 historical changelog mentions
#   (44/44, 44→47, 43→44 — describing past version transitions accurately) correctly left
#   untouched; confirmed individually, not by blanket pattern-replace. Verified against
#   Framework_MockTestExplainAudit.md's OWN references at the same time (a claim that it was
#   "still inconsistent, 5x say 44" was checked directly and found inaccurate — its 4 live
#   references already correctly say 62/62; the "44" mentions there are legitimate history).
#   No procedure, gate, or rendered byte changed — purely a stale-count correction.
#
# v1.17 — 2026-07-18 — SECTION-ID COLLISION FIX (found during a final adversarial audit;
#   docs-only, zero logic change). §S7-4's reference to Step 7's canonical derive_nat_grading
#   definition (Framework_MockTestCreate.md) pointed at "S7-NEW-B" — an ID that collided
#   with an unrelated pre-existing figural-generation section. Renamed to S7-NEW-C
#   throughout (4 references, including S7-4's own heading subtitle), matching
#   Framework_MockTestCreate.md v5.27. No procedure, formula, or rendered byte changed.
#
# v1.16 — 2026-07-18 — S7-4: NAT PORTAL GRADING VALUE (closes a gap found during a
#   cross-file consistency audit of the same defect chain as Framework_MockTestCreate.md
#   v5.25/v5.26, Framework_MockTestCreateAudit.md v2.8, Framework_MockTestExplainAudit.md
#   v1.12, Framework_MockDeliver.md v1.8, and explain_engine.py v1.16/v1.17). ROOT CAUSE:
#   this file's S8-1 standard STILL SHOWED the retired "47 (accepted range 46.5–47.5)"
#   format as the live example — meaning Step 9, followed literally, would still have
#   produced the exact original defect (a Correct-Answer line the delivery portal's
#   grading charset rejects). Separately, S10c instructed setting `ca` to the raw
#   derive-twice VALUE directly — a Python float's bare str() (e.g. "3.0") can legitimately
#   differ from the certified portal string ("3"), a distinct defect class from getting the
#   math wrong. WHAT CHANGED: new §S7-4 embeds a PINNED, byte-identical copy of
#   `derive_nat_grading()` (Framework_MockTestCreate.md §S7-NEW-C) — the third independent
#   copy alongside Step 7's canonical definition and Step 8's A-NAT-GRADE copy. Because the
#   function is pure and deterministic, running it on the SAME (value, ca_range,
#   stem_precision) triple Step 7 used is GUARANTEED to reproduce the SAME certified
#   string — no new dependency on reading Step 7's internal sidecar is introduced; this is
#   a determinism guarantee, not a lookup, consistent with this step's existing
#   derive-independently philosophy (S7-1). S10c and S5-1's field table updated to source
#   ca/ca_range from this transform's output, never a hand-formatted or raw value. S8-1's
#   retired example replaced with the current lo-hi format, with the old wording now
#   explicitly named and banned. No change to any MCQ/MSQ instruction, any gate unrelated
#   to NAT, or any already-rendered byte outside the NAT Correct-Answer line.
#
# v1.15 — 2026-07-15 — C3: paper_slug FILENAME CONVENTION (docs; no logic). Input/output
#   [ExamCode]_Mock[N]_*.docx use the paper_slug of the paper ("Mock[N]" for a mock — unchanged;
#   scoped = paper_id with ':'→'_'). No registry writes. Pairs with MockCreate v5.21.
#
# [ExamCode] project | Step 9 (MockExplain) | Universal Mock Test Explanation Generator
#   v1.14 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#           Solutions output renamed [ExamCode]_Mock[N]_Solutions.docx →
#           [ExamCode]_Mock[N]_Explanation.docx. Input renamed accordingly: reads the Step-8
#           rectified paper [ExamCode]_Mock[N]_Create_Complete.docx. Whole-paper incremental
#           delivery model (RE-8), coverage/batch law, §18/§19 and the engine unchanged.
#   v1.13 — 2026-07-11 — FIGURE SECTION REMOVED FROM SOLUTIONS OUTPUT (owner decision).
#           The ⬛ FIGURE / figure_note block is no longer emitted for figural
#           questions — the Solutions docx now renders exactly Correct Answer →
#           ⬛ AXIOM → ⬛ DEDUCTION → (⚡ SPEED HACK) → ❌ WHY WRONG? / ❌ COMMON
#           PITFALLS for EVERY question type. The figure_note field is removed from
#           ExplanationBlock entirely (not merely un-rendered) — the same clean-
#           removal discipline the framework applies to dead fields. Coordinated
#           edits, all mechanical:
#             (1) EngineConfig: 'figure' dropped from labels + markers.
#             (2) ExplanationBlock: figure_note param + attribute + both validate()
#                 guard-scans removed. _block_paragraphs no longer emits the FIGURE
#                 header or note.
#             (3) verify_explanations / parse_solution_blocks: 'figure' dropped from
#                 the header map; the FIGURE position/presence checks and the reader's
#                 pre/figure note-capture modes removed.
#             (4) SELF-TESTS: the four FIGURE tests (FIGURE-NOTE, FIGURE-HDR,
#                 FIGURE-HDR-VERIFY, FIGURE-HDR-ABSENT) replaced by ONE regression
#                 lock (FIGURAL-NO-FIGURE-SECTION: a figural question renders NO
#                 FIGURE section, its image survives byte-identical, the audit passes).
#                 Core self-test 47/47 → 44/44; reader --self-test-audit stays 10/10
#                 (the round-trip test drops its figure_note assertion).
#           NO SIDE EFFECT to correctness: the image-VIEWING discipline is untouched —
#           RE-11 / §13 still require every figural image extracted, role-bound and
#           VIEWED, and Step 10's completion-gate CA5 (viewed-image evidence) is
#           unchanged (it never read figure_note). C-FIGURAL (§6) still governs how
#           AXIOM / DEDUCTION / WHY WRONG are written for figural questions; only the
#           separate descriptive anchor line is gone (the figure itself is in the
#           question region above, preserved byte-identical). Fidelity, batching,
#           coverage, NAT/MSQ, learnings: all byte-identical to v1.12. §8-6 deleted;
#           §5-1 / §5-3 / §6-1 / §13-4 / §18 / §21 de-referenced. Parallel edits in
#           Framework_MockTestExplainAudit.md and Framework_MockDeliver.md (same pass).
#   v1.12 — 2026-07-08 — PRODUCER-SIDE COMPLETION-GATE ALIGNMENT + ENGINE SINGLE-SOURCE.
#           Parallel to Framework_MockTestCreateAudit.md v2.6 and Step 10 v1.7. Step 9's
#           §18 per-batch self-audit is already largely MECHANICAL (engine verify_fidelity/
#           verify_structure/verify_explanations + the S4-5 pre-deliver coverage assertion),
#           so its false-clean surface was smaller than Step 8's — but three edits close the
#           residue and align it with the independent gate:
#             (1) NEW RE-0 PRECEDENCE: no user preference / project-memory note / autonomy
#                 ("don't pause") instruction may reduce per-question COVERAGE (RE-4) or
#                 weaken the §18 self-audit / the batch-stop law (MANDATE B). Preferences may
#                 change only PACING (the inter-batch HALT) and report verbosity; the HARD
#                 rule always wins.
#             (2) AUTONOMOUS-MODE note (MANDATE B / §4): a "don't pause" preference waives the
#                 inter-batch HALT ONLY — batches still run one-at-a-time internally, each with
#                 its full §18 self-audit and coverage assertion; the per-question review is
#                 never collapsed. A run that finishes "fast" by skipping the per-question
#                 solve/verify is a MANDATE B violation.
#             (3) §18 CROSS-REFERENCE to the independent gate: Step 10 (MockExplainAudit) now
#                 certifies via a runnable COMPLETION GATE (explain_audit_gate.py, CA1–CA7 over
#                 audit_progress.json + evidence sidecars). Step 9's per-question handoff data
#                 (what was derived, web-verified, viewed, and DERIVATION-CONFIDENCE-flagged)
#                 is exactly what populates that ledger, so producer self-check and independent
#                 audit share ONE evidence contract (no producer↔auditor drift).
#           ENGINE SINGLE-SOURCE: Appendix A now POINTS to the canonical runnable
#           explain_engine.py instead of re-embedding the ~1000-line listing verbatim — the
#           same multi-copy-drift fix Step 8 v2.6 and Step 10 v1.7 applied (the embedded copy
#           and the standalone could silently desync, which v1.8/v1.9 history shows already
#           happened once). The runnable canonical copy is explain_engine.py; self-test
#           unchanged (47/47 core + 10/10 reader). No engine logic or rendered-byte change.
#   v1.11 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S19-4: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. Per-batch (F1 mid-step) and final
#           batch (F2 step-complete) now render the standardized visual footer.
#           Same Explanation.docx delivered each batch (whole-paper incremental).
#           Zero logic change.
#   v1.10 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (level + marking_scheme).
#           Step 6 v1.19 now carries level, medium, marking_scheme in blueprint.json.
#           Step 5 v2.18 writes marking_scheme and level to section_rules CATEGORY C.
#           Step 9 reads these for:
#             (1) level: explanation depth calibration — PG explanations can assume
#                 foundational knowledge and use advanced terminology; Grad explanations
#                 spell out more; School explanations are fully explicit.
#             (2) marking_scheme: per-Q-position marks context — higher-mark questions
#                 (e.g., CSIR NET Part C at 4 marks) can receive proportionally more
#                 thorough DEDUCTION steps and WHY WRONG analysis.
#           Both read via cat_c() from section_rules CATEGORY C (same interface as
#           existing fields). Safe defaults when absent ('unknown' / []).
#           Session Status dashboard updated to show level and marking ranges.
#
#   v1.9 — 2026-07-04 — ENGINE CODE FIXES (3 bugs) + EXAM-AGNOSTIC HARDENING (4 fixes).
#           PART A — 3 engine bugs claimed in v1.8 changelog but never applied to code:
#             (1) CA DETECTION CASE INCONSISTENCY (v1.8 fix #4): parse_solution_blocks
#                 used case-SENSITIVE `t.startswith(ca_prefix)` while verify_explanations,
#                 verify_structure, and strip_solutions all used case-INSENSITIVE `.lower()`.
#                 FIXED: ca_label lowercased + `t.lower().startswith(ca_prefix)`.
#             (2) _is_subheader FALLBACK TERMINATORS (v1.8 fix #5): the fallback branch
#                 hardcoded `.!?` instead of using configurable terminators, breaking
#                 Devanagari/Hindi papers (danda `।` misclassified as sub-header). FIXED:
#                 added `terminators` parameter (default `.!?`), passed by
#                 parse_solution_blocks from cfg.sentence_terminators.
#             (3) parse_learnings SUPERSEDED DETECTION (v1.8 fix #6): used loose
#                 `'supersed' in b.lower()` (substring anywhere in block text) instead
#                 of checking the explicit `**Supersedes:**` field — a rule whose Pattern
#                 mentioned "supersede" would be falsely flagged. FIXED: `bool(field('Supersedes'))`.
#           PART B — EXAM-AGNOSTIC HARDENING (4 fixes removing all hardcoded English/SSC values):
#             (4) _BANNED_BLOCKS ('REMEMBER', 'EXAM CONNECTION') were SSC-specific block
#                 headers hardcoded in the engine. FIXED: moved to EngineConfig as
#                 configurable `banned_blocks` with English defaults. Non-English exams
#                 pass their own blocked headers via config.
#             (5) _BANNED_TEMPLATE, _BANNED_FAKECITE were English-only template/fake-cite
#                 patterns. FIXED: moved to EngineConfig as configurable `banned_templates`
#                 and `banned_fakecites`. Non-English exams extend or replace them.
#             (6) _META_RE (English metacommentary regex) hardcoded. FIXED: moved to
#                 EngineConfig as configurable `metacommentary_re` (string → compiled).
#             (7) option_label() had no bounds check for custom-list or alpha schemes.
#                 Custom list IndexError on out-of-bounds; alpha chr() produced invalid
#                 chars beyond 26. FIXED: ValueError with clear message on both.
#           guard_sentence() and verify_explanations() now read all banned patterns from
#           cfg when available, falling back to module constants when cfg=None (self-tests).
#           All 7 fixes applied to: standalone explain_engine.py, embedded Appendix A in
#           this file, embedded Appendix A in Framework_MockTestExplainAudit.md. Engine
#           self-test: 47/47 + 10/10. Dashboard + §R1 version bumped to v1.9.
#   v1.8 — 2026-07-04 — CANONICAL STEP-NUMBER ALIGNMENT + ENGINE DESYNC FIX + CODE FIXES.
#           Deep audit found 7 bugs:
#             (1) TITLE/FILENAME MISMATCH: header said "Framework_MockExplain" but filename
#                 is Framework_MockTestExplain.md. FIXED: title now matches filename.
#             (2) 148 CANONICAL STEP-NUMBER VIOLATIONS: the entire body used old internal
#                 phase numbering (Step 0/1/2/3/4/5) while the header and Pipeline Position
#                 section used the canonical 11-step pipeline. The standalone explain_engine.py
#                 had ALREADY been updated to canonical numbers; the embedded copy had NOT,
#                 causing a desync. FIXED: all body references now use canonical numbers:
#                 old Step 0 → PYQ-phase (Steps 1–4), old Step 1 → Step 5 (PYQExtract),
#                 old Step 2 → Step 7 (MockCreate), old Step 3 → Step 8 (MockCreateAudit),
#                 old Step 4 → Step 9 (MockExplain = THIS), old Step 5 → Step 10
#                 (MockExplainAudit). Embedded engine now matches standalone in step numbering.
#             (3) §R1 REPORT TEMPLATE hardcoded "spec v1.0" — file is v1.8. FIXED.
#             (4) CA DETECTION CASE INCONSISTENCY: verify_explanations and
#                 parse_solution_blocks used case-SENSITIVE CA label matching while
#                 _qregion_signature, verify_structure, and strip_solutions used case-
#                 INSENSITIVE. FIXED: all now case-insensitive.
#             (5) _is_subheader FALLBACK ignored configurable sentence_terminators,
#                 hardcoding '.!?'. FIXED: now accepts a terminators parameter, passed by
#                 parse_solution_blocks from cfg.sentence_terminators.
#             (6) parse_learnings "superseded" detection was overly loose (substring match
#                 on "supersed" anywhere in block text). FIXED: now checks only for an
#                 explicit **Supersedes:** field.
#             (7) Line 210 "Steps 2–6" used old numbering. FIXED: "Steps 5–11".
#           Engine updated: step numbers canonical + code fixes (4/5/6 above); self-test
#           stays 47/47 + 10/10; no rendered-byte change to non-comment code.
#   v1.7 — 2026-07-03 — DEEP-AUDIT REVIEW (documentation-only; engine + output unchanged).
#           Line-by-line review confirmed the engine and all code paths are clean. One
#           documentation fix applied:
#             (1) Status dashboard (P2) hardcoded "MockExplain v1.0" — the file is v1.7.
#                 A session seeing "v1.0" in its own output after loading v1.7 is confusing.
#                 FIXED: dashboard now reads v1.7.
#           Engine untouched; self-test stays 47/47; no rendered-byte change.
#   v1.6 — 2026-07-02 — FIGURE HEADER FOR FIGURAL figure_note (rendering fix;
#           self-test 44 → 47). Fixes the SSC CGL T1 M1 rendering defect: for
#           figural questions, figure_note was emitted as a bare unlabeled
#           paragraph between "Correct Answer" and "⬛ AXIOM" — the only content
#           block with no bold section heading, reading like orphaned text. ROOT
#           CAUSE — S8-6 defined figure_note's content role but NOT its render
#           contract; the engine implemented it as a plain sentence; no auditor
#           checked for the missing heading because the heading was never specified
#           to exist. FIX (four coordinated edits, zero rendered-byte change to
#           non-figural questions):
#             (1) EngineConfig: registered 'figure' in labels ('FIGURE') and
#                 markers ('⬛') with setdefault so custom configs inherit it.
#             (2) _block_paragraphs: emits _header_para(cfg, 'figure') BEFORE the
#                 figure_note sentence. Rendered order is now:
#                 CA → ⬛ FIGURE → ⬛ AXIOM → ⬛ DEDUCTION → (⚡ SPEED HACK) →
#                 ❌ WHY WRONG? / ❌ COMMON PITFALLS.
#             (3) verify_explanations: H dict includes 'figure'; FIGURE is filtered
#                 from the core-header check (like SPEED HACK); a separate position
#                 check confirms it is first in seq when present, and flags a
#                 spurious FIGURE header on a non-figural block.
#             (4) parse_solution_blocks: H dict includes 'figure'; HREV maps the
#                 rendered header to mode='figure'; the parser collects figure_note
#                 under that mode. mode='pre' retained as backwards-compat fallback
#                 for old-format docs that lack the FIGURE header.
#           NEW SELF-TESTS (47/47): FIGURE-HDR (header present + before AXIOM),
#           FIGURE-HDR-VERIFY (verify_explanations passes on figural block),
#           FIGURE-HDR-ABSENT (non-figural block has no FIGURE header + passes).
#           S8-6 updated with render contract. Appendix A carries the new engine.
#   v1.5 — 2026-07-02 — QUESTION METADATA INDEX — DEFENSIVE READ-ONLY TOUCH (cross-step index
#           extension, Step-4 half). Step 4 does NOT consume or write registry.question_index —
#           it is a Step-3-certified, FROZEN field bound for Step 6. (1) S1-1 lists it as frozen/
#           read-only. (2) S2-2 adds a cheap read-only corruption tripwire: if present, the field
#           should carry one mock-N object covering 1..total_questions; a mismatch is a WARNING
#           only (Step 4 resolves its own question TYPE from the paper + options_by_q and never
#           consumes the index), and absence is silent (older registries). No output bytes change;
#           engine untouched; self-test stays 44/44. Governed by Contract_QuestionMetadataIndex
#           v1.0.
#   v1.4 — 2026-07-01 — LEARNINGS CONSUMPTION HOOK (closes the Step 5 -> Step 4 feedback
#           loop, decision D3). Step 5 (MockExplainAudit) emits
#           [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md — AL-rules for every defect code with
#           >= 2 occurrences in a mock — but the framework Step-4 spec had only a dangling
#           FOOTER reference to a learnings file with nothing that LOADED or APPLIED it (an
#           incomplete-wiring gap of exactly the kind this project treats as a bug). This
#           version operationalises the loop:
#             (1) P1 now LOADS the learnings files (EXPLAIN_AUDIT_LEARNINGS + EXPLAIN_LEARNINGS)
#                 via the new engine reader parse_learnings and indexes the rules by
#                 defect_code (the exam-agnostic routing key).
#             (2) NEW §24 — the consumption contract: per question, the applicable rules
#                 (routed by class -> defect_code) are obeyed; learnings OVERRIDE this spec on
#                 conflict; rules accumulate across mocks (never deleted, superseded only
#                 explicitly); the producer schema + the >= 2-occurrence promotion threshold
#                 are PINNED so producer (Step 5 §24) and consumer (here) cannot desync.
#             (3) NEW RE-22 (load & apply learnings); the §5 per-question checklist and the
#                 §18 self-audit each gain one line asserting applicable rules were routed;
#                 the FOOTER now names both files correctly.
#           ENGINE (explain_engine.py, ADDITIVE — core --self-test stays 44/44): adds
#           parse_learnings (this hook) and parse_solution_blocks (the Step-5 reader), both
#           exercised by a new extended suite --self-test-audit (10/10). It also folds three
#           root-cause OMML-blindness fixes in verify_explanations / the reader, all surfaced
#           by adversarial NAT edge-testing: verify_explanations read fraction well-formedness
#           via m:t descendants while frac() stores digits as direct element text (every
#           genuine digit/digit fraction was falsely "malformed OMML"); and BOTH the reader
#           and the verifier segmented + bound/covered NAT lines via p.text, which EXCLUDES
#           OMML, so a NAT with a fraction answer or a fraction pitfall value was silently
#           dropped or failed its own binding/coverage audit and could not ship. The fixes
#           read via itertext() / an OMML-aware line reconstruction and detect sub-headers by
#           the writer's own paragraph spacing rather than a fragile text heuristic; they
#           change ZERO rendered bytes and are locked by RT-FRAC-VERIFY + RT-NAT-FRAC. This
#           is why prior mocks avoided OMML fractions entirely (Step 4's own §18 rejected
#           them). Non-learnings behaviour is byte-identical; mock-1 runs unchanged.
#   v1.3.1 — 2026-06-30 — NAT KEY-TYPE SYNC FIX (cross-step audit follow-up). Closes a
#           latent str/int desync at the registry→engine boundary found by the deep
#           MSQ/NAT contract-sync audit: registry.json serialises options_by_q inner keys
#           as JSON STRINGS, but EngineConfig.expected_options() is queried with INT q, so a
#           literal load (per P3) missed every NAT key and silently mis-typed NAT as MCQ.
#           ROOT-CAUSE FIX in explain_engine.py: EngineConfig.__init__ normalises
#           options_by_q keys to int on construction (accepts str- or int-keyed input
#           identically). New NAT-STRKEY self-test locks it (--self-test 43→44). P3 updated
#           to state the map may be passed straight from registry.json. No resolution logic
#           changed; non-NAT papers unaffected.
#   v1.3 — 2026-06-30 — NAT CONTRACT — WIRING (cross-step NAT extension, Step 4 half).
#           The engine ALREADY resolves and explains mcq/msq/nat (self-test 43/43,
#           mixed-paper aware); this version wires the now-live UPSTREAM signals so the NAT
#           resolution path is actually fed:
#             (1) options_by_q is loaded from registry.json['options_by_q'][str(N)] (the
#                 Step-2 ND6 contract) and passed to EngineConfig — MANDATORY, because
#                 expected_options(q) reads this map and never counts rendered options, so a
#                 NAT question is non-resolvable without it. Per-question AUTHORITY.
#             (2) section_rules answer_type / answer_cardinality (now WRITTEN by Step 0 v2.8)
#                 are the per-subtopic EXPLICIT type hint, consistent with options_by_q (a NAT
#                 subtopic's questions == the options_by_q==0 questions). P3 resolution +
#                 P5 conflict check use both.
#             (3) Pre-v4.7 papers without options_by_q fall back to the section_rules
#                 per-question/per-section type resolution with a WARN. No engine logic
#                 changed (explain_engine.py untouched); --self-test stays 43/43. Non-NAT
#                 papers are byte-identical to v1.2.
#   v1.2 — 2026-06-30 — Engine filename standardised to the plain neutral name
#           explain_engine.py everywhere (dropped the [ExamCode]_ prefix from MANDATE A,
#           D6, the input list, and Appendix A). Rationale: unlike the exam-specific T2
#           reference engine, this engine is UNIVERSAL and byte-identical across all
#           exams, so a per-exam prefix added no disambiguation and falsely implied
#           exam-specificity. This also reconciles a pre-existing internal inconsistency
#           — pre-flight P1 already referenced the plain name while MANDATE A used the
#           prefixed one. One identical file, reused in every exam project, no rename.
#   v1.1 — 2026-06-30 — T2-parity hardening. Diffed the universal engine against the
#           proven Tier-2 reference engine (from the owner's other project) and folded
#           back every battle-tested capability that exam-agnosticism had dropped (no
#           decisions reversed):
#             A1. Vulgar-fraction glyphs (½ ¾ ⅓ … ⅒) and the Unicode fraction slash
#                 (U+2044) now RAISE in guard_sentence/has_inline_fraction — the §11-1
#                 claim is now actually enforced (it was previously prose-only).
#             A2. verify_explanations() — a new INDEPENDENT post-render audit that
#                 re-parses the RENDERED docx (not the in-memory blocks) and re-checks
#                 header order, the type-aware CA binding read back from the document,
#                 WHY-WRONG / COMMON-PITFALLS coverage, banned content + inline/vulgar
#                 fractions in rendered prose, one-sentence-per-paragraph, and document-
#                 wide OMML fraction well-formedness + year-range artefacts. Closes the
#                 "trust the build" gap: the artifact is verified, not the plan (§18-1).
#             A3. verify_fidelity() now also confirms every image rId in the body
#                 resolves to a relationship (no dangling embed).
#             A4. Inline-fraction detection widened to non-numeric forms (1/x, 1/(x+1),
#                 1/√2, x²/2, (a+b)/c) so they are forced to explicit OMML.
#             A5. Sentence counter given the T2 abbreviation breadth (~45 abbreviations,
#                 lowercase dotted acronyms u.s/a.m/p.m) — fewer false sentence breaks.
#             A6. Year-range detection sharpened: YYYY/NN flags only when NN == year+1,
#                 so a genuine n/(n+1) telescoping fraction in that band is not flagged.
#           Engine self-test 37→43. Deliberately NOT adopted from T2 (exam-specific or
#           superseded by locked decisions): hardcoded section ranges, section-gated
#           speed hacks (ours is derivation-driven), the answer_keys sidecar (we derive),
#           in-document anomaly rendering (we halt-and-escalate), and MCQ-only support
#           (we add MSQ + NAT). The correct-option echo / WHY-WRONG option-content
#           cloning remains an OPEN design question for the owner (index-only stands).
#   v1.0 — 2026-06-30 — Initial release. Takes the Step-3 (MockCreateAudit)
#           rectified, certified-clean Mock[N]_Create_Complete.docx + the frozen
#           registry.json and produces [ExamCode]_Mock[N]_Explanation.docx — the
#           same paper with a perfect, audited explanation interleaved after each
#           question. Built exam-agnostic from the ground up (zero hardcoded exam
#           values — every count, format, label, language, option-count, figural
#           type, escape token and section family is read at runtime from
#           blueprint.json / section_rules.md / subtopic_manifest.json /
#           registry.json). Design decisions locked with the framework owner:
#             D1. Step 4 receives ONLY {Mock[N]_Create_Complete.docx, registry.json}
#                 (Step-3 closed set). Step 3 derived a key INTERNALLY to audit and
#                 NEVER delivered it (Step-3 §11-3 / §19). So Step 4 has NO key and
#                 re-derives every answer independently (§7) — it is the FIRST step
#                 that publishes a learner-facing key.
#             D2. Output is a NEW file [ExamCode]_Mock[N]_Explanation.docx. The Step-3
#                 questions-only secure paper is PRESERVED untouched (never
#                 overwritten). registry.json is FROZEN — read for manifests/context,
#                 never re-synced or rewritten (that closed at Step 3).
#             D3. APPEND-ONLY. Step 4 never edits a single byte of any question
#                 region; it only appends explanation paragraphs after each
#                 question's last option. Every stem, option, image, table, matrix,
#                 chart and OMML expression is carried through byte-identical (§12).
#             D4. INCREMENTAL WHOLE-PAPER delivery. Each batch ships the COMPLETE
#                 paper: every question solved so far carries its explanation, every
#                 not-yet-solved question is identical to the Step-3 input. The file
#                 grows explanation-coverage each batch; it is never a fragment (§4).
#             D5. BATCH-OR-HALT. Explanations are produced in batches of ≤
#                 EXPLAIN_BATCH_SIZE (ceiling 10, never a quota), one batch per
#                 response, and the run HALTS for the author's explicit confirmation
#                 before the next batch. All-at-once is a malfunction (MANDATE B).
#             D6. ENGINE-BUILT. explain_engine.py (Appendix A, universal,
#                 --self-test 47/47) is the ONLY path by which an explanation enters
#                 the docx; it raises at write time on every known defect. MANDATORY
#                 (hard stop if absent — MANDATE A).
#             D7. DERIVE-TWICE, NEVER GUESS. Every answer is derived from first
#                 principles AND a second independent method; disagreement → third →
#                 2-of-3 + DERIVATION-CONFIDENCE; no defensible single answer →
#                 HALT-AND-ESCALATE to Step 3 (the paper was certified clean; Step 4
#                 never edits content and never publishes a guess — §17).
#             D8. PRODUCER, NOT AUDITOR. Step 4 self-certifies with strong inline
#                 checks (the Audit-A analogue, §18); the INDEPENDENT re-audit that
#                 does not trust Step 4's self-report is Step 5 (MockExplainAudit)
#                 — exactly the Step-2 / Step-3 relationship.
#


# ═══ ARCHIVE — Framework_PYQPrepare pre-relocation header history (moved 2026-07-31 at v1.14; verbatim) ═══

#   v1.13 — 2026-07-27 — VISION_WORKDIR DEFINED, DISTINCT, AND fresh (GAP-2026-07-27-B follow-up).
#           This spec used VISION_WORKDIR at three call sites without defining it, so
#           Step 1 silently inherited Step 5's /home/claude/pyq_vision. corpus_io
#           <= v1.8 overwrote the workdir on every build, which HID the sharing; the
#           v1.9 idempotent union (correct for Step 5's batch-spanning workdir)
#           surfaced it — a second PYQPrepare run in the same session saw the first
#           paper's cells carried into its queue (measured: queued=3 for a 1-image
#           paper), re-viewed them in Phase B, counted them unobserved in Phase C,
#           and delivered an amber footer with wrong counts. Now: VISION_WORKDIR is
#           declared HERE as /home/claude/pyq_vision_prep, and both call sites pass
#           fresh=True (corpus_io >= v1.10), which clears queue + sheets +
#           observations before building. Step 1's Phase A->B->C completes inside one
#           trigger, so prior workdir contents are never resume state for this step.
#           An undefined constant in a spec is itself the defect: the executing model
#           must guess or borrow, and both guesses were wrong here.
#   v1.12 — 2026-07-26 — CALL A3b REWIRED TO PHASE A/B/C; PROBE FAMILY RETIRED.
#     v1.11 replaced the S1-12 protocol but CALL A3b in the tool-call ledger still
#     instructed corpus_io.make_vision_probe() / score_vision_probe(), and two vector
#     branches still instructed corpus_io.normalise_for_view(). corpus_io v1.8 deletes
#     all three, so those were live instructions to call functions that no longer
#     exist. CALL A3b now runs build_vision_queue (Phase A) -> view the sheets
#     (Phase B, prose) -> merge_vision_observations (Phase C), and the vector branches
#     defer to Phase A, which normalises internally and marks anything it cannot
#     rasterise [UNRENDERABLE] rather than dropping it (EC-V8).
#
#   v1.11 — 2026-07-26 — S1-12 VISION BECOMES REACHABLE; THE HALT IS REPLACED
#     (GAP-2026-07-26-003). PHASE A-PROBE called run_img6_probe(read_probe),
#     imported from Framework_MockTestAnalyse S3-1c. That probe took a CALLBACK
#     expected to perform a view(). A callback cannot make a tool call from inside
#     a running python process — a tool call happens only BETWEEN model turns — so
#     the parameter defaulted to returning '', score_vision_probe raised
#     ProbeObservationMissing on all three attempts, and the probe reported EVERY
#     session blind, on EVERY exam. Step 1 inherited the defect by importing it.
#
#     Replaced by the same three-phase bridge Step 5 now uses (S4-2a/b/c). There is
#     no separate probe: the extracted images ARE the probe. Liveness is derived
#     from whether observations came back, at zero extra cost.
#
#     THE HALT IS GONE AND THE ARTEFACT IS STILL PROTECTED. The old design
#     conflated two things: "never bake a red placeholder under blind vision"
#     (correct, permanent, preserved absolutely) and "therefore stop the run"
#     (unnecessary). An image LEFT IN PLACE is safe and reversible; a placeholder
#     cannot be un-baked. Step 1 now COMPLETES, delivers the Row file with
#     unobserved images untouched, states the count, and renders F1 amber.
#
#     The placeholder gate is now PER IMAGE rather than per session, which is
#     strictly STRONGER: a session whose vision worked for 40 images and lapsed
#     for 3 may placeholder none of those 3. Previously one passing probe licensed
#     placeholders for every image in the session.
#
#   v1.10 — 2026-07-26 — IMG-6 PROBE PROTOCOL HARDENED (GAP-2026-07-26-002 PART A).
#            The v1.6 protocol was single-attempt, single-token, and required no record
#            of what was read, while corpus_io.score_vision_probe() returned False for an
#            empty string — so "I did not look" was indistinguishable from a genuinely
#            blind session and produced a false, session-terminating halt in Step 5 on
#            its first production use. Now: 3 attempts, 3 DISTINCT tokens, and the
#            observation is MANDATORY (score_vision_probe RAISES ProbeObservationMissing
#            on an empty read, which is retried, never scored as a failure). Adds the
#            self-check that a legible file which rendered is evidence FOR working
#            vision, never against it — the inverted inference that caused the incident.
#            Step 1 STILL STOPS on a genuine 3-attempt failure, unlike Step 5 which now
#            records vision_unavailable and continues: Step 1 DELIVERS a Row file that
#            every downstream step consumes, and a placeholder baked in under a blind
#            probe is permanent. The halt here protects the ARTEFACT, not the session.
#            Requires corpus_io.py with ProbeObservationMissing.
#            [SUPERSEDED v1.11 — corpus_io v1.8 deletes that family; liveness is
#            derived from Phase B observation coverage, and the halt is replaced by
#            complete-and-report.]
#   v1.9.1 — 2026-07-25 — Q_PATTERNS RENAMED SOURCE_Q_PATTERNS. Step 1 parses RAW dumps, where
#           "Question 1:", bare "1." and "(1)" are genuine numbering — so the five-entry table
#           is CORRECT here and wrong everywhere downstream. Naming it SOURCE_* (as
#           SOURCE_OPT_PATTERNS already is) separates it from the normalised-document contract
#           Steps 3/4/5 share, and stops it being read as a claim about the delegated detector,
#           which implements two. The old comment claimed the table was "checked by audit_deep
#           TABLE-PARITY"; that check could not fire. No behaviour change — the table is
#           declared, never read, and detect_question_start is bound but never called in this
#           spec.
#   v1.9 — 2026-07-25 — VISION LIVENESS GATE + IMAGE DISCOVERY DELEGATED (DEFECTS F, I, J).
#         Twin of Framework_MockTestAnalyse v2.29 / Framework_PYQSort v1.12 /
#         Framework_PYQAnalyse v2.21 / corpus_io v1.0.1.
#         (1) DEFECT F (CRITICAL) — a vision outage sent math to the graphics team.
#             S1-6 and S1-12 make the placeholder-vs-transcribe decision BY VISION:
#             "Red placeholders for math content are BANNED. The ONLY legitimate
#             placeholder for a math question is when the image is physically unreadable
#             after Claude has viewed it." The fall-through then reads: "If the image is
#             genuinely unreadable (corrupt, blank, too low resolution) -> red placeholder".
#             With vision unavailable EVERY image is "genuinely unreadable", so every one
#             falls through to a placeholder and the spec cannot tell the two apart. This
#             is not hypothetical: it reproduces the exact defect v1.6 was written to
#             eliminate, recorded in that changelog — SSC CGL T2 18-Jan-2025 Shift 1,
#             Q.6/14/15/17/19-22/28-30, eleven math questions (~35% of the Quant section)
#             delivered as red placeholders instead of transcribed math. In the current
#             workflow the damage compounds: the graphics team receives placeholders for
#             equations and tables, draws pictures of them, and those questions become
#             FIGURAL instead of TEXT for the entire rest of the pipeline.
#             Vision capability can stop working MID-SESSION as context grows — proven in
#             session by a freshly generated control PNG that failed to render while real
#             figures had rendered correctly earlier. The files were never the problem.
#             Fix: S1-12 now runs a LIVENESS PROBE before classifying any image, and the
#             outcome is three-valued. PASS -> v1.6 behaviour, completely unchanged.
#             FAIL -> vision_unavailable: HALT with resumable state and ask for a fresh
#             session. Assigning a red placeholder under a failed probe is a HARD BUG,
#             ranking with the existing "unclassified image" hard bug.
#             [SUPERSEDED BY v1.11 — the probe could never pass (its callback could not
#             make a tool call) and the HALT is replaced by complete-and-report. The
#             placeholder prohibition is UNCHANGED and is now enforced per IMAGE.]
#         (2) DEFECT I (proven by construction, previously unreported in THIS file) —
#             extract_images() walked doc.paragraphs, which in python-docx returns ONLY
#             paragraphs that are direct children of the body; paragraphs inside table
#             cells are excluded entirely. Every image laid out in a table was therefore
#             never extracted, never viewed and never classified — it did not even reach
#             the "unclassified image" hard bug, because the walk never saw it. Measured
#             on a two-image document with one figure in a table: 2 images present, 1
#             found. Table layout is the NORMAL arrangement for match-the-following items,
#             multi-panel figures and option grids.
#         (3) DEFECT J — only <a:blip> and a bare '<w:pict' string test were used, so a
#             legacy VML <v:imagedata r:id> image could be detected but never resolved to
#             its part. Verified: 'imagedata' appeared 0 times in this file.
#             Fix for (2) and (3): image discovery is DELEGATED to corpus_io (Cluster I) —
#             extract_images walks the package, map_images_to_questions walks
#             doc.element.body.iter() which descends into tables, and both match
#             <a:blip r:embed> AND <v:imagedata r:id>. The local copy is DELETED. Two
#             implementations of one function under one name produce zero drift signal
#             until they disagree, which is exactly how this file kept a defect that had
#             already been fixed twice elsewhere.
#         (4) S1-6 fall-through and S1-7 PREREQUISITE amended: "genuinely unreadable" is
#             only a permissible verdict when the probe has PASSED in this session.
#         (5) Probe result recorded in the delivery report (§7) so a placeholder's
#             provenance is auditable after the fact.
#         (6) NO GOVERNOR IN STEP 1 — deliberately. Step 1 emits only 300x200 red
#             placeholder PNGs, so there is nothing to compress and no size risk to
#             manage. Size governance begins at Step 3 (PYQSort S7-6), the first step to
#             hold real image bytes. Stated so the omission reads as a decision.
#         (7) New EC-P22 (vision unavailable) and EC-P23 (image inside a table).
#         NOT CHANGED: every classification rule and category in S1-12, the OVER-CLASSIFY
#         AS MATH guidance, S1-13 scanned-source transcription, the red placeholder
#         specification, the ALL-or-NONE option rule, and the closed deliverable set.
#         ROUTING: routes.json already routes corpus_io.py to PYQPrepare (v2.21 change).
#   v1.8 — 2026-07-23 — detect_question_start DELEGATED to blueprint_core (Cluster G).
#           Four specs parsed Q-numbers from the same documents with four local copies of
#           one function. They were byte-identical today; nothing would have noticed if one
#           changed. Mutation testing showed that re-localising shared logic in a SINGLE
#           spec produces no drift signal at all (cross-spec drift needs two differing
#           copies), so the corpus could have silently regressed. routes.json now routes
#           blueprint_core.py to PYQPrepare. audit_deep.py DELEGATION + TABLE-PARITY enforce
#           this permanently. No behaviour change: the engine form is byte-identical.
#   v1.7 — 2026-07-14 — SCANNED-SOURCE VISION TRANSCRIPTION (FORMAT C fix).
#          Root cause: FORMAT C (scanned image-only PDF) was an unconditional
#          HALT expressed as INTERPRETIVE PROSE, not executable code. That
#          prose contradicted S1-6/S1-12 (vision is the fallback; placeholdering
#          readable content is a HARD BUG) — and S1-12's own trigger fires on
#          "embedded images in PDF", which a scan contains. With the decision
#          left to interpretation, the same source resolved to HALT in one run
#          and vision-transcribe in another (non-deterministic).
#          Fix: (1) new S1-13 SCANNED-SOURCE VISION TRANSCRIPTION protocol.
#          (2) FORMAT C (S2-1) split into three MECHANICAL tiers computed by a
#          runnable classify_source_pdf() — C0 (illegible → HALT, retained),
#          C1 (legible scan → vision-transcribe), C-HYBRID (mixed pages). The
#          decision is now RUN, not read; the encrypted/corrupt/exotic-codec
#          cases degrade to C0 via a guard, never a crash.
#          (3) poisoned-text-layer guard (_text_is_sane) — a coverage==1 source
#          whose text is mostly garbage routes to C1 instead of silently
#          producing a garbage Row file (threshold tuned high so clean FORMAT A
#          papers are never misrouted).
#          (4) mandatory VISION provenance marker (core_properties.category +
#          filename suffix) set at BUILD time in the C1 path.
#          (5) page-level classification reuses EC-P2 (skip blank/instruction),
#          EC-P13 (English-only), EC-P17 (never transcribe answers); new EC-P21
#          excludes specimen/sample questions (e.g. "Q.201" नमुना प्रश्न).
#          Page-level ANSWER-KEY pages are dropped at S1-13 classification
#          (EC-P17); CHECK 8 answer-marker scan is unchanged.
#          (6) three new checks — CHECK 14 (vision provenance consistency),
#          CHECK 15 (specimen/out-of-range exclusion), CHECK 16 (Q-count vs
#          stated-total reconciliation). All new checks are WARN-only,
#          consistent with the S5 "warn, deliver anyway" contract; the
#          provenance guarantee is enforced at BUILD time, not by a hard-fail.
#          (7) batch model for large scans reuses the EXISTING DeliveryFooter
#          F1 continue / session-break variants (no DeliveryFooter change).
#          FORMAT A/B/D/E paths and checks 1–13 are UNTOUCHED; validate_row_file
#          gains two OPTIONAL params (backward-compatible).
#          KNOWN LIMITATION: a ZIP-of-images with no .txt (FORMAT-C-in-a-ZIP)
#          is out of scope for v1.7.
#          Total checks: 13→16. Tool call budget: 5–15 → page-count-dependent
#          for FORMAT C1 (~one view call per question-content page + overhead).
#   v1.6 — 2026-07-07 — IMAGE INSPECTION PROTOCOL (math-as-image fix).
#          Root cause: source files (especially docx from coaching platforms)
#          render math questions as embedded images with no extractable text.
#          The previous spec surrendered all image-only content to red
#          placeholders — including MATH content (fractions, equations,
#          tables, expression-heavy stems). Production defect: SSC CGL T2
#          18-Jan-2025 Shift 1 — Q.6, Q.14, Q.15, Q.17, Q.19–Q.22,
#          Q.28–Q.30 (11 math questions, ~35% of Quant section) delivered
#          with red placeholders instead of transcribed math content.
#          Fix: (1) new S1-12 IMAGE INSPECTION PROTOCOL — mandatory
#          Phase A sub-step that extracts all embedded images, Claude views
#          each, classifies as MATH-IMAGE / TABLE-IMAGE / TEXT-IMAGE /
#          VISUAL-IMAGE, and transcribes content for non-visual images.
#          Transcriptions are baked into pipeline.py as IMAGE_CLASSIFICATIONS
#          dict. (2) S1-6 "surrender" clause replaced — image-rendered math
#          now triggers image inspection, NOT automatic placeholder. Red
#          placeholders for math are BANNED unless image is unreadable.
#          (3) S1-7 updated — placeholder assignment requires prior image
#          classification; unclassified images are a HARD BUG. (4) S3-3
#          figure detection updated to use classification results. (5) S2-2
#          Phase A expanded — image extraction is mandatory when source
#          contains embedded images. (6) new EC-P20 math-as-image edge
#          case with 8 sub-scenarios. (7) new CHECK 13 — IMAGE CLASSIFICATION
#          detection: scans for figure-only stems in math-range questions
#          and cross-references against image classification log. (8) §9
#          execution walkthrough updated with Phase A-IMAGE sub-phase.
#          (9) §12 DoD updated with image inspection items. (10) EC-P4
#          updated to reference image classification prerequisite.
#          Total checks: 12→13. Tool call budget: 4–7 → 5–15
#          (image-count-dependent).
#   v1.5 — 2026-07-07 — INLINE UNDERLINE PRESERVATION.
#          Root cause: questions like "Select the meaning of the underlined
#          word" had the underlined word (e.g. "leisurely") rendered as plain
#          bold text — the underline was LOST during extraction. Without the
#          underline, the question is nonsensical. Production defect: SSC CGL
#          T2 18-Jan-2025 Q.2 — "leisurely" underlined in source, plain in
#          output.
#          Fix: (1) new S1-11 INLINE FORMATTING CONTRACT — defines {{u}}...
#          {{/u}} marker convention for underlined text. Underlines are the
#          only semantically significant inline formatting in PYQ stems
#          (vocabulary, error detection, sentence improvement questions).
#          (2) S2-1 FORMAT D (docx) updated — extraction must detect
#          run.underline and wrap in {{u}}...{{/u}} markers. FORMAT A (PDF)
#          guidance added for pdfplumber char-level underline detection.
#          (3) set_font() gains underline parameter (S4-2).
#          (4) render_text_with_math() refactored — now splits on {{u}} markers
#          FIRST, then processes each segment for math. Underlined segments
#          get run.underline=True on all text runs within them.
#          (5) new CHECK 12 — SEMANTIC UNDERLINE VALIDATION: if stem text
#          contains "underlined" but no underline formatting exists in the
#          paragraph XML → WARN. Catches extraction failures.
#          (6) new EC-P19 — underline handling edge case.
#          Total checks: 11→12.
#   v1.4 — 2026-07-07 — MATH RENDERING HARDENING (5 fixes).
#          Comprehensive audit of all math patterns in SSC CGL T2 output
#          (35 OMML elements, 150 questions). Findings: v1.3 compound fix
#          resolved the ROOT CAUSE; 5 additional gaps identified and fixed:
#          (1) FRACTION REGEX FIX: character class [\d√⟦\[SQRT:\]⟧] was
#          buggy — included individual letters S,Q,R,T as false-positive
#          matches. Replaced with clean r'(\d*√?\d+)\s*/\s*(\d*√?\d+)'
#          that matches only digit+√ combinations. Pre-normalization of
#          residual markers makes SQRT characters in the class unnecessary.
#          (2) DATE FALSE-POSITIVE FIX: 12/05/2024 matched as fraction 12/05.
#          Added date context lookahead — if matched denominator is followed
#          by /\d{2,4}, skip (it's a date). Also added lookbehind for
#          preceding digit+/ patterns.
#          (3) NTH ROOT HELPER: new omml_nthroot(degree, content) in S3-4
#          for cube roots ³√8, fourth roots ⁴√16 etc. Q.14 in the reference
#          paper had ³√6859 × ⁴√1296 — pipeline managed without the helper
#          but the spec should provide it for reliability.
#          (4) PRE-NORMALIZATION: render_text_with_math() now normalizes
#          all ⟦SQRT:N⟧ and [SQRT:N] markers to √N at the TOP before any
#          pattern matching. Eliminates timing-dependent Pattern 4 catch.
#          Pattern 4 (residual markers) removed — pre-norm handles it.
#          (5) 2-TIER ARCHITECTURE NOTE: S1-6 now documents the two-tier
#          math handling system: pipeline-level detection (primary — handles
#          complex expressions, trig fractions, nth roots, multi-OMML
#          compounds) vs render_text_with_math() safety net (catches simple
#          fractions, √, mixed numbers, residual markers that pipeline
#          missed). Complex expressions like (secθ−tanθ)/(secθ+tanθ) are
#          PIPELINE responsibility, not safety-net scope.
#   v1.3 — 2026-07-07 — COMPOUND MATH RENDERING FIX.
#          Root cause: omml_frac() accepted only simple text strings for
#          numerator/denominator. When a fraction component contained compound
#          content (e.g. "2√3" in the denominator of 1/(2√3)), the √3 was
#          left as a literal ⟦SQRT:3⟧ text marker inside <m:t> instead of
#          being decomposed into nested <m:rad> OMML. Production defect:
#          SSC CGL T2 18-Jan-2025 Q.17 option 3 showed "2[SQRT:3]" as
#          visible text in the rendered document.
#          Fix: (1) new build_math_run() — creates atomic <m:r><m:t> element.
#          (2) new build_compound_content() — recursively decomposes compound
#          math strings into mixed [text-run + OMML-element] lists. Handles
#          √N within fraction components, ⟦SQRT:N⟧ residual markers, and
#          arbitrary text+sqrt combinations. (3) omml_frac() rewritten to
#          use build_compound_content() for BOTH num and den — supports
#          1/(2√3), √3/2, 2√5/7, etc. (4) new render_text_with_math() —
#          top-level function that parses a text string for inline math
#          patterns (fractions, roots, mixed numbers, residual tags) and
#          renders segments as alternating text-runs + OMML elements. Handles
#          false-positive exclusions (km/h, dates, and/or). (5) add_stem()
#          and add_option() in S4-2 updated to call render_text_with_math()
#          instead of plain p.add_run(). (6) new CHECK 11 — RESIDUAL MATH
#          MARKERS validation: scans all <m:t> and paragraph text for
#          unresolved ⟦SQRT:⟧, [SQRT:], or stray √ patterns that should
#          have been converted to OMML. (7) S1-6 contract updated with
#          compound expression examples. Total checks: 10→11.
#   v1.2 — 2026-07-07 — Q.N-FIRST BLOCK CONTRACT FOR PASSAGE QUESTIONS.
#          Root cause: Step 1 output placed passage/instruction BEFORE Q.N
#          for passage-linked questions (RC, Cloze, DI). This violated the
#          universal "a question starts with Q.N" expectation and conflicted
#          with MockTestCreate v3.7 Q.N-FIRST contract. Downstream consumers
#          (Steps 3, 5, 7) expect every question block to OPEN with Q.N.
#          Fix: §1 S1-2 block structure diagram updated — removed position 1a
#          (passage before Q.N). Passage now ALWAYS follows Q.N stem. §1 S1-9
#          passage handling rewritten — "preserve source ordering" removed,
#          replaced with mandatory Q.N-FIRST layout: Date→Q.N→instruction→
#          passage→options. §2 S2-6 updated to match. §8 EC-P8 updated. §12
#          DoD item 12 updated. Aligns Step 1 output with MockTestCreate §9
#          SC-3 Q.N-FIRST rule, so PYQ Row files are natively compatible with
#          the online importer expectation.
#   v1.1 — 2026-07-07 — CROSS-STEP SYNC AUDIT FIX (1 stale text fix).
#          §10 cross-step contract: "PYQSort UPDATE REQUIRED" was stale —
#          PYQSort v1.8 already has the optional session fix. Changed to
#          "PYQSort SYNC STATUS: COMPLETE (v1.8)" with current regex.
#   v1.0 — 2026-07-07 — Initial release. Derived from TestSeriesRow Tier 1 v17
#          and Tier 2 v3. Full exam-agnostic rewrite. 31 design decisions
#          documented and resolved. Two-layer architecture (output contract +
#          adaptive source parsing). Cross-step sync verified against PYQSort
#          v1.7, PYQAnalyse v2.10, MockTestAnalyse v2.4, MockTestCreate v5.8.
#          Output contract: continuous Q.1→Q.N, canonical option format,
#          configurable date labels, OMML math, red placeholders for figures,
#          native Word tables for DI, passage repetition for all exam types.



# ═══ ARCHIVE — Framework_PYQSort pre-relocation header history (moved 2026-07-31 at v1.18; verbatim) ═══

#   v1.17 — 2026-07-26 — is_option DELEGATED; IMAGE OPTIONS NO LONGER UNDERCOUNTED
#            (audit_deep [XSPEC-DRIFT]). This file carried its own is_option() whose
#            docstring claimed "Aligned with Step 5's is_option() — same 5 patterns."
#            MockTestAnalyse v2.34/v2.35 added the image-option path and this copy was
#            left behind, so the claim became false and the same defect stayed live
#            HERE. It was not cosmetic: _count_options_in_body() and the option
#            re-indent pass both use the predicate, so an IMAGE OPTION — a bare "1."
#            whose content is a picture — was neither counted nor indented. Measured
#            on IIT_JAM_BIOTECHNOLOGY 2022: 156 options counted against 160 actual.
#            corpus_io >= v1.6 now owns OPT_PATTERNS / BARE_OPT_PATTERNS /
#            para_has_image / is_option; this spec delegates. BOTH call sites now pass
#            the paragraph element — delegating without passing it compiles cleanly
#            and keeps the undercount, which is the trap in this fix.
#   v1.16 — 2026-07-26 — THE TAXONOMY IS LOADED ONCE, FROM JSON WHERE AVAILABLE.
#          reconcile_taxonomy >= v1.3 records the approved taxonomy inside
#          approval_record.json — a file the platform stores byte-for-byte — beside
#          the fingerprint that validates it. corpus_io.load_taxonomy() prefers that
#          and falls back to the Analysis doc for pre-1.3 records, so on the
#          preferred path this step reads no Word document at all and EC-S20 cannot
#          arise. Exams approved earlier are unaffected and need no re-run.
#          S1-0b and S1-2 collapse to ONE call. The pair they replace — a read
#          followed by a separate lock assertion — was written in both sections,
#          which meant the artefact was read TWICE in one step and the two reads
#          could disagree. S1-0b makes the call because it is the first consumer;
#          S1-2 reuses the object and hard stops if it is missing.
#          S1-3 reports source alongside ingest form. EC-S21 records the new path
#          and, explicitly, that a pre-1.3 record is NOT a fault. DoD 23 updated.
#   v1.15 — 2026-07-26 — INGEST FORMS SURFACED + S1-0b DELEGATED (GAP-2026-07-25-003).
#          Documentation and delegation only; no behaviour in this spec changes that
#          corpus_io >= v1.3 does not already provide.
#          (a) EC-S20 records what the runtime actually receives: the Analysis doc is
#              stored in project Files as extracted TEXT under its .docx name, and
#              that is the PRIMARY form at Steps 3-6, not a degraded one. It also
#              records the two things that are NOT tolerated — a '|' in any taxonomy
#              name, which the text form splits into a silently truncated name whose
#              declared totals still agree, and an unrecognised extraction grammar.
#          (b) S1-3 REPORTS the ingest form. Same discipline as S1-0's one line on
#              success: when the platform's grammar eventually changes, this line is
#              the first evidence of it.
#          (c) S1-0b no longer writes the fingerprint comparison itself. It was the
#              first place to make that claim and, for one release, the only one;
#              Steps 4, 5 and 6 now make it too, so the rule lives once in
#              corpus_io.assert_taxonomy_lock() and every step calls it. Four
#              transcriptions of one comparison is how GAP-2026-07-25-002's four
#              readers happened. The claim, the messages and the operator actions are
#              unchanged — only their location is.
#          (d) §13 gains the rule the whole gap reduces to: NEVER infer a container
#              format from a file extension.
#   v1.14 — 2026-07-25 — ANALYSIS-DOC READER DELEGATED + S1-0b CONTENT CROSS-CHECK
#          (GAP-2026-07-25-002). S1-2 carried its own reader and it was wrong twice over.
#          DEFECT A (loud): the discovery glob '*_PYQ_Analysis_*.docx' required a trailing
#          '_' that PYQAnalyse v2.6 removed 19 days and 7 releases ago — it matched every
#          filename the framework no longer produces and none of the one it does, so PYQSort
#          hard-stopped telling the operator to upload a file already correctly in place.
#          DEFECT B (silent, P0): a `if not section_name` latch delimited SUBJECTS BY FILE
#          BOUNDARY, which is exactly what the merge to a single doc removed. Measured on the
#          first real exam: 1 subject parsed where the doc declares 6, all 131 subtopics filed
#          under one subject, 5 topic_idx collision groups, correct totals throughout. Every
#          sorted file would have carried "Subject: General Biology" above Physics questions.
#          A was the ONLY control preventing B from shipping, and it was protecting by
#          accident: fixing the glob alone converts a loud stop into silent corpus-wide
#          corruption. They are fixed together, and by deletion rather than by repair —
#          the reader now lives in corpus_io Cluster K, the single reader/writer/verifier for
#          this artefact, with heading recognition delegated to
#          blueprint_core.parse_taxonomy_level(). Two consequences beyond the reported bug:
#          (a) all six level-1 label forms (Subject/Domain/Section/Part/Area) and all six
#          level-2 forms (Topic/Chapter/Unit/Module/Block) now work here, where the old
#          hardcoded matcher saw one of each; (b) the reader HARD STOPS when its parse
#          disagrees with the totals the document declares about itself, so a future variant
#          of B cannot be silent. NEW S1-0b closes the other half: S1-0 proved the lock was
#          earned, never that the loaded taxonomy IS the locked one — Defect B passed S1-0
#          cleanly. S1-0b compares blueprint_core.taxonomy_fingerprint() against the
#          approval record's. topic_idx becomes positional within the subject, which is what
#          §S6-2 always specified; the old label-derived form could not survive a merged doc,
#          where "Topic N:" restarts at 1 for every subject.
#   v1.13 — 2026-07-25 — S1-0 TAXONOMY LOCK VERIFICATION added (GAP-2026-07-25-001,
#          Layer 4). approval_record.json was produced at Step 2c and read by NOTHING —
#          the string did not appear in this spec or in any other downstream spec. A lock
#          nothing verifies is a receipt, and it is why a silent S4-0 check-skip could
#          travel five steps undetected. PYQSort now HARD STOPS when the record is absent,
#          when status is not CLEAN/CLEAN_ADJUDICATED, or when the record cannot prove its
#          checks ran (pre-1.1 schema, or non-empty checks.missing / checks.vacuous /
#          unmaterialisable). Re-running PYQApprove is RECONCILIATION, never re-derivation.
#   v1.12.2 — 2026-07-25 — Q_PATTERNS TABLE RECONCILED WITH THE ENGINE. The local table listed
#           five patterns while the delegated bc.detect_question_start implements two, and the
#           audit_deep TABLE-PARITY check this spec cited as its guarantee could not see the
#           difference: its extraction regex stopped at the first "]", which sits inside
#           r'^Question\s+(\d+)\s*[:.]'. The table is documentary — declared, never read — so
#           behaviour is unchanged; what changes is that the documentation no longer invites a
#           catastrophic "fix". Widening the engine to five patterns would make every option
#           line match: a 100-question paper parses as 500 (verified).
#   v1.12.1 — 2026-07-25 — MINIMUM COMPANION VERSION CORRECTED. The v1.12 entry named
#           "corpus_io v1.0" as its twin. That is wrong in a way that matters: S7-6 calls
#           assert_docx_parity with allow_resample=False for tier T1, and in corpus_io v1.0
#           that raises a FALSE IntegrityError whenever the governor renames a media part —
#           which is the ordinary path for a photographic PNG, since the jpeg route rewrites
#           image1.png as image1.jpeg. Proven by execution: identical 1400x1000 dimensions
#           before and after, corpus_io v1.0 HARD STOPs, corpus_io v1.0.1 passes. Pairing
#           v1.12 with corpus_io v1.0 therefore gives a governor that fails closed on exactly
#           the papers it exists to shrink. The minimum companion is corpus_io v1.0.1, whose
#           parity fix was found while verifying this very spec. Documentation only — not one
#           line of behaviour changes here.
#   v1.12 — 2026-07-25 — IMAGE SURVIVAL GATE + SIZE GOVERNOR ON WRITE (DEFECT J, DEFECT M).
#           Twin of Framework_MockTestAnalyse v2.29 / corpus_io v1.0.1 (see v1.12.1 — the
#           original entry said v1.0, which is the one release this spec does NOT work with).
#           Step 3 is where images
#           are RE-EMBEDDED — the riskiest image operation in the PYQ pipeline, and the one
#           §13 has warned about since v1.0 in its own words: "images silently vanish. No
#           error, just empty space." Verified by grep across all 31 tracked files: NO
#           image-count check of any kind existed in this file. Framework_PYQFormat has
#           enforced exact input==output image equality (S8-6) since v1.1 for the same class
#           of risk; the step that actually performs the risky operation had nothing.
#           (1) DEFECT J — re_embed_images() matched only <a:blip r:embed> (DrawingML).
#               Legacy VML <v:imagedata r:id> — emitted by older Word, several PDF converters
#               and pasted OLE/equation objects — was never re-pointed, so exactly the
#               failure the §13 warning describes occurred for every VML image, silently.
#               Verified: 'imagedata' appeared 0 times in this file, in
#               Framework_MockTestAnalyse.md and in Framework_PYQPrepare.md. S7-1 now
#               re-points BOTH mechanisms.
#           (2) DEFECT M — NEW S7-7 image survival gate, modelled on PYQFormat S8-6 with the
#               same exact-equality discipline (not a tolerance) and surfaced as CHECK 10.
#               Body image references in the delivered file MUST equal the `intended` count
#               from the S7-5 census. Mismatch is a HARD STOP naming the missing media parts.
#           (3) NEW S7-5 pre-flight + input image census. The pre-flight runs on the PATH
#               before python-docx opens the Row file, because a relationship pointing at a
#               missing media part makes python-docx raise a bare zipfile KeyError while
#               CONSTRUCTING the Document — any check placed after Document(path) is
#               unreachable, and the operator gets a library traceback instead of a sentence
#               naming the defect and the step that owns it. Found by adversarial test, not
#               by reading. The census then establishes the expected count before any work,
#               partitions every body child into CARRIED (a question's stem or body element)
#               and NOT CARRIED, and REPORTS the not-carried ones with their count and text
#               prefix. Images before Q.1, or inside a date-label paragraph the emitter
#               rebuilds from scratch, are correctly not carried — but dropping them SILENTLY
#               would either hide a real loss or trip the new gate for a benign reason. The
#               expected count is derived from the parse, not from a Q-number regex, so it
#               cannot disagree with what the emitter actually carries.
#           (4) NEW S7-6 size governor on write. Step 3 is the first step to hold real image
#               bytes, and its output is what Steps 4 and 5 fetch back OUT of Drive through a
#               connector that refuses downloads above 10 MiB. An ungoverned Sorted file is
#               therefore the thing that blocks Step 4/5 later, three-quarters of the way
#               through a batch run (the reported 2026-07-24 incident: 6 of 7 pending papers
#               above the cap, discovered at batch 6). The governor runs on write, under
#               corpus_io.assert_docx_parity — 17 invariants including the text SHA256, the
#               OMML count and per-image pixel dimensions, because a governor that quietly
#               dropped a figure would still produce a smaller file that opens cleanly in Word.
#           (5) Ladder floor exceeded (still over budget at T4) → DELIVER + WARN + FLAG, never
#               HALT. A legitimately huge paper must not block its own delivery; the operator
#               is told the file will need the upload lane at Step 4/5.
#           (6) Counting is DELEGATED to corpus_io.count_image_refs (Cluster I) — blip AND
#               VML, every story part, never doc.inline_shapes (which sees only inline body
#               drawings and so under-counts silently). A local re-implementation here is
#               forbidden: a count that can run low is worse than no count, because it makes
#               a broken document look verified.
#           (7) §9 write path made explicit for the first time: save → census → govern →
#               parity → CHECK 1..10 → copy to FINAL_OUT. Still 4 tool calls.
#           (8) EC-S16..EC-S19 (VML images · governor floor · non-carried images · dangling
#               relationship in the Row file).
#           ROUTING: routes.json must route corpus_io.py to PYQSort. NOT OPTIONAL — this spec
#           imports it.
#   v1.11 — 2026-07-23 — detect_question_start DELEGATED to blueprint_core (Cluster G).
#           Twin of Framework_PYQPrepare v1.8 / MockTestAnalyse v2.28. No behaviour change —
#           the engine form is byte-identical to the copy removed here.
#   v1.10 — 2026-07-23 — ANTI-DRIFT: OUT_OF_PATTERN now comes from the ENGINE
#           (blueprint_core.OUT_OF_PATTERN) instead of being declared locally. v1.9 declared
#           the literal here while Framework_PYQAnalyse RULE 4 referenced it by name under a
#           DIFFERENT trigger, with no shared definition and no route carrying one — two
#           independent copies of a single literal, which is precisely the drift the
#           framework's anti-drift principle forbids. routes.json now routes blueprint_core.py
#           to PYQSort (and to PYQDraft/PYQScan/PYQApprove/PYQCount/PYQExtract for the same
#           reason). No behavioural change: the value is identical.
#   v1.9 — 2026-07-23 — OUT-OF-PATTERN QUESTIONS NO LONGER SILENTLY LOST
#           (GAP-2026-07-23-001, PYQ-side twin of Framework_Blueprint v1.36).
#           ROOT CAUSE: exam_config describes the CURRENT exam pattern, but a PYQ corpus
#           routinely spans several patterns. get_section_by_q_range() returned None for any
#           Q-number outside every configured section range; the None was written straight
#           into the question record at S3-2, and a corpus-wide grep confirms NO guard for it
#           existed anywhere. Those questions then failed every (section, topic, subtopic)
#           lookup. On a 100-question legacy paper sorted against a 60-question current
#           config that is a silent 40% data loss on one file, with no operator-visible
#           signal of any kind. This is the same unstated assumption — "PYQ structure equals
#           current structure" — that produced the Blueprint axis-unit and coverage-gate
#           defects fixed in Framework_Blueprint v1.36.
#           (1) S2-2 get_section_by_q_range(): returns the OUT_OF_PATTERN module constant
#               instead of None. NEVER returns None. The sentinel is a fixed literal, not an
#               exam-derived string, so it cannot collide with any exam's section names.
#           (2) S3-2 extract_questions(): every question record gains pattern_era, valued
#               'current' or 'out_of_pattern'. Structural provenance only — never a content
#               judgement.
#           (3) S4-3 classify_question(): OUT_OF_PATTERN questions are classified against the
#               FULL taxonomy instead of one section's slice. This is a NARROW, SENTINEL-GATED
#               exception to RULE 4 ("section from structure, not content"): RULE 4 exists so a
#               maths question sitting in the Reasoning section stays in Reasoning, which
#               presupposes a structural section EXISTS. These have none, so RULE 4 has nothing
#               to say and applying it anyway yields an empty candidate list — exactly how the
#               questions were lost. The exception is gated on the sentinel, never on a failed
#               match, so a question that HAS a real section can never fall through to it.
#           (4) NEW report_pattern_era(): prints observed vs configured Q-count, the
#               out-of-pattern count and Q-range, and the mix consequence. Reports only —
#               never mutates, never decides, never halts. Silent when the paper matches the
#               current pattern exactly, so the 200-exam common case is unchanged.
#           (5) EC-S1b: the mirror of EC-S1 (papers LARGER than the current pattern).
#           WHAT THIS DELIBERATELY DOES NOT DO: it does not exclude out-of-pattern questions
#           from frequency. Counts are already safe (Framework_Blueprint §4-2 uses r_avg as a
#           PROPORTION against a sec_qs budget, so a different-size paper cannot inflate or
#           shrink allocation), but subject/subtopic MIX is still inherited from whichever
#           eras the corpus contains. Era-scoped frequency requires era-tagging through the
#           Step-5 manifest and Frequency xlsx and is a separate change.
#   v1.8 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           Framework_PYQPrepare v1.0 allows session to be omitted from date labels.
#           (1) build_date_label_re(): session_keyword+number now optional in regex.
#               Old: ^\[DD-Mon-YYYY\s+<keyword>\s+\d+\]$
#               New: ^\[DD-Mon-YYYY(?:\s+<keyword>\s+(\d+))?\]$
#           (2) parse_date_label(): session defaults to 1 when not present in label.
#           (3) CHECK 3: accepts both [DD-Mon-YYYY] and [DD-Mon-YYYY <keyword> N].
#           (4) EC-S10: error message updated to show both date label formats.
#           (5) EC-S15: updated — Step 1 now omits session entirely for single-session
#               exams (no default session=1). parse_date_label defaults to 1.
#           (6) Header + bottom STEP 1 FORMAT CONTRACT updated for optional session.
#           (7) make_output_filename(): handles session-less date labels.
#           Cross-step sync: Framework_PYQPrepare v1.0 §1 S1-3 (date label contract).
#   v1.7 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3 in §12 DoD POST-DELIVERY block.
#           Zero logic change.
#   v1.6 — 2026-07-06 — CLOSED DELIVERABLE SET CONTRACT.
#           Added closed-set delivery contract to match cross-framework standard
#           (PYQAnalyse §10, MockCreate S13-6). Header OUTPUT now says "(1 file,
#           nothing else)" with explicit DO-NOT-DELIVER list. §9 execution model
#           has a DELIVERABLE SET CONTRACT block with pre-delivery check (exactly
#           1 file, correct path, all validations passed). §12 DoD item 18 added.
#           Low structural risk (single-file deterministic script output), but
#           formalised for consistency after SSC CGL Tier 2 PYQAnalyse failure
#           (unauthorized taxonomy_draft_v2.json delivery) exposed the gap pattern.
#
#   v1.5 — 2026-07-06 — EXAM_CONFIG V2.5 SCHEMA COMPATIBILITY.
#           Step 2a v2.5 expanded exam_config.json with marking_scheme[], level, medium,
#           max_attempt, and question_types. PYQSort does NOT consume these new fields
#           (sorting depends on taxonomy + Q-ranges + session_keyword, not marks or level).
#           Change: S1-3 file inventory printout updated to reflect new schema fields
#           for transparency (shows marking ranges count, level, medium if present).
#           sections[] now includes max_attempt in the loaded schema — PYQSort ignores it
#           (sorting is independent of attempt limits). Zero code logic changes.
#
#   v1.4 — 2026-07-03 — EXAM-AGNOSTIC AUDIT (6 rigidity fixes).
#          (1) DATE_LABEL_RE: replaced hardcoded "Shift" with session_keyword
#              read from exam_config.json. Supports Shift/Slot/Phase/Paper/
#              Session/Morning/Afternoon or any custom keyword. parse_date_label()
#              and Check 3 validation both use the configurable pattern.
#          (2) Check 4 NAT-awareness: exams with NAT questions (answer_type=
#              numerical) have questions with ZERO options. Check 4 now counts
#              only MCQ questions (total − NAT count) for the options threshold.
#              NAT questions are identified by having 0 option paragraphs in
#              their body_elems.
#          (3) Page size: replaced hardcoded US Letter (8.5×11") with page_size
#              from exam_config.json. Default is A4 (8.27×11.69") — the standard
#              for Indian competitive exams. US Letter available via config.
#          (4) EC-S10 softened: missing date label still raises ValueError (it IS
#              a parse failure), but the error message now names Step 1 as the
#              fix location and documents the Step 1 format contract.
#          (5) Sort key shift field documented: for single-session exams, Step 1
#              synthesises session=1, making field 7 a no-op tiebreak. This is
#              correct behaviour, not dead weight.
#          (6) PROOF section expanded: added GATE (1 section, NAT, no session),
#              Banking (multi-slot), UPSC (multi-paper) as covered exam patterns.
#              Added Step 1 format contract as explicit prerequisite.
#   v1.3 — 2026-07-03 — DEEP-RESEARCH AUDIT (14 fixes).
#          (1) Q_PATTERNS drift: patterns 1-2 used `\s` instead of `\s+`,
#              misaligned with Step 5 E-2. Fixed to `\s+` for contract parity.
#          (2) OPT_RE replaced: single `r'^[1-5]\.\s'` replaced with full
#              5-pattern OPT_PATTERNS matching Step 5 E-3 / PYQAnalyse exactly.
#              is_option() function aligned.
#          (3) Taxonomy table parser rewritten: cur_topic_for_table was declared
#              but never used — all subtopics were attributed to the LAST topic.
#              Fixed: table rows now properly track their parent topic via
#              section-topic detection within each table.
#          (4) load_exam_config circular dependency: function required exam_code
#              to find the file containing exam_code. Fixed: glob search for
#              any *_exam_config.json in /mnt/project/.
#          (5) Pipeline position updated: "TestSeriesRow" → "Step 1 PYQ Prepare",
#              Step 4 PYQCount added between PYQSort and PYQExtract, full 11-step
#              pipeline listed.
#          (6) make_output_filename: multi-date case now computes actual earliest
#              and latest dates instead of generic "Multi" placeholder.
#          (7) renumber_stem: extended to handle all Q_PATTERNS formats (Q.N,
#              QN., Question N:, N., (N)) not just Q.N.
#          (8) Month regex aligned: DATE_LABEL_RE changed from `{3,}` to `{3}`
#              to match Check 3 validation exactly.
#          (9) subtopic_idx reset per topic in taxonomy table parser.
#          (10) Check 4 options count: changed from hardcoded 4 to exam_config.
#          (11) Footer version marker added.
#          (12) Section detection fallback: marker_mode mismatch changed from
#               warn-and-fallback to HARD STOP.
#          (13) S3-1 comment corrected.
#          (14) §11 Exam-Agnostic Guarantee updated.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (1 fix). S6-2 sub-section heading still
#          said "STEP 0 E-1 COMPATIBLE" — missed by v1.1 audit. Corrected to
#          "STEP 5 E-1 COMPATIBLE". No code logic changed.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (1 fix). 4 "Step 0" references corrected
#          to "Step 5" (PYQExtract). Step 0 was the old internal name; the
#          canonical pipeline position is Step 5. No code logic changed.
#   v1.0 — Initial release. Derived from TestSeriesSort Tier 1 v10 + Tier 2 v3.
#          Exam-agnostic taxonomy loading. Dual section-detection mode (markers + Q-range).
#          Heading format contract with Step 5 E-1 parser. 13 edge cases.
#          All pipeline mechanics inherited: insert_para, image re-embedding,
#          OMML walker, date label iron rule, 9-check validator.



# ═══ ARCHIVE — Framework_PYQDeliver pre-relocation header history (moved 2026-07-31 at v1.5.1; verbatim) ═══

# v1.5 — 2026-07-24 — TIER 1.5 (STRUCTURAL) + PER-QUESTION MARKS. Filed from the
#   IIT JAM Biotechnology 15-Feb-2026 delivery, which tagged 60 of 60 questions
#   "Easy" across a paper of 30 MCQ / 10 MSQ / 20 NAT.
#
#   MEASURED ROOT CAUSE (reproduced against the shipped engine on all 60 stems):
#   E-9's C axis scored 1 for 60/60 and its I axis 1 for 59/60. E-9's computation
#   keywords are gated to strip_mode=='quantitative' (BUG-B08) and E-10 maps every
#   science subject to 'reasoning', so the only stem-level signal that could lift a
#   science question is unreachable. Exactly ONE of the 60 stems contained any C-axis
#   keyword at all. This is not a calibration error to be tuned out: a keyword list is
#   inherently exam-SPECIFIC, and PYQ-4 serves ~200 exams. Tier 2 cannot be the answer.
#
#   THE ANSWER IS TIER 1, WHICH v1.2 ALREADY SPECIFIED (§0 item 7, §2-3a) and which
#   PYQ-1 v1.1 now supplies via its §7A assessment. PYQ-4 needs NO change to consume
#   it — that path was correct from the start and is untouched here. What v1.5 adds is
#   the FLOOR beneath it, for papers with no PYQ-1 derivation pass:
#
#   (1) TIER 1.5 — structural_difficulty (§2-3a1), a new PURE function in
#       blueprint_core.py Cluster E2. Reads the exam body's own marking_scheme:
#       question_type + position in the marks gradient. Returns None when the scheme
#       carries no structural signal (uniform marks AND one type — e.g. a 200-question
#       all-MCQ paper), so such exams fall through to Tier 2 exactly as before.
#       HONEST SCOPE: Tier 1.5 assigns one label per (marks, type) band. It reports the
#       exam body's design intent, NOT the difficulty of an individual question, and it
#       CANNOT separate a hard 2-mark MCQ from an easy one. It exists so that a paper
#       with no PYQ-1 pass is not degenerate; it is not a substitute for Tier 1.
#
#   (2) PER-QUESTION MARKS (§2-3b). v1.4 read one uniform exam_config.marks_default for
#       every question. Two independent defects: (a) marks_default is declared nowhere
#       outside this spec and no other step writes it, so the field is absent in practice
#       and the executing instance was left to improvise a value; (b) even when present,
#       a single value is wrong for any exam with a marks gradient. §2-3b now resolves
#       marks per question from exam_config.marking_scheme[] — the SAME field Tier 1.5
#       reads and the same one Steps 7/9/11 already consume — with marks_default and then
#       1 as ordered fallbacks. NOTE, recorded because it is counter-intuitive: raising
#       marks RAISES E-9's Simple threshold (simple = 4 + (marks-1)) while a science
#       stem's score does not rise with marks, so per-Q marks makes Tier 2 LESS
#       differentiating, not more. It is applied because it is CORRECT, not because it
#       helps the symptom; Tier 1/1.5 are what fix the symptom.
#
#   TIER CHAIN IS NOW 1 → 1.5 → 2 → 3. tier_counts (§2-3e) and §R3 extended to match.
#   Backward compatibility: an exam with no marking_scheme, or a uniform-marks
#   single-type scheme, skips Tier 1.5 entirely and resolves exactly as in v1.4.
#   E-9/E-10 are NOT modified — no CROSS-FILE SYNC obligation is created by v1.5.
#
# v1.4 — 2026-07-24 — PACKAGE VALIDITY GATE (C18). Preventive, adopted from
#   the PYQFormat v1.3 P0 incident. PYQ-4 has NOT produced a corrupt file;
#   this closes the blind spot that let PYQ-3 ship one silently.
#
#   What that incident established: CONTENT FIDELITY and PACKAGE VALIDITY are
#   independent properties, and every gate here verifies the first. A
#   document.xml with undeclared mc:Ignorable prefixes or misordered pPr/tcPr
#   children is still WELL-FORMED XML — it parses cleanly in lxml and stdlib
#   ElementTree alike. On the PYQ-3 artefact the text stream, all drawings and
#   every paragraph count were perfectly intact while Word refused to open the
#   file. C1 and C12 ("valid ZIP; document.xml parses") are exactly the checks
#   that gave false comfort there: parsing is not validating. §11 item 11
#   already required "opens clean in Microsoft Word with no unreadable content
#   prompt" with no machinery anywhere to verify it — C18 makes that real.
#
#   Why PYQ-4 has not hit this (recorded so the margin is not mistaken for
#   immunity): its ordering surface is tiny. make_tag_para builds exactly
#   [spacing, jc] — two elements, hardcoded in correct order, guarded by
#   C16(d). PYQ-3 inserted six pPr children plus tblPr/tcPr/tcMar plus two new
#   parts, and got five of those orders wrong. The safety here comes from a
#   small workload, not from a check — so any future widening of PYQ-4's
#   element workload removes the margin without any gate noticing. C18 is the
#   check that does not care how large the workload grows.
#
#   C18 gates BOTH artifacts (integrity and render-source) with --original, so
#   only errors NEW relative to the source block delivery. Zero, not "fewer" —
#   a rejected parent is not descended into, so nested faults stay masked until
#   the outer one is fixed (on the PYQ-3 artefact, 812 reported errors required
#   991 element reorders to clear).
#
#   SCOPE NOTE (deliberate, not an oversight): S13-3's library mandate remains
#   inherited by delegation — S13-1 states PYQ-4 reuses MockDeliver's patterns
#   identically, and MockDeliver mandates lxml explicitly. PYQ-4's own S13-3
#   text still warns against cleanup_namespaces() without naming a library.
#   C18 makes that inheritance verifiable at runtime rather than assumed, which
#   is the property that matters. Promoting the mandate into PYQ-4's own text
#   is a separate change, not made here.
#
# v1.3 — 2026-07-23 — OUT-OF-PATTERN MARKS WARNING (audit follow-up).
#   §2-3b fell back to exam_config.marks_default (or 1) for any question outside the
#   current marking_scheme, silently. For a PYQ paper from an earlier pattern that means a
#   legacy 4-mark question is delivered to students tagged 1 mark with no signal anywhere.
#   Now counts those questions and WARNs with their Q-range and the fallback value applied.
#   WARN, not HALT — publishing legacy PYQ papers is legitimate; only the silence was wrong.
#
# v1.2.1 — 2026-07-23 — Line-by-line adversarial audit fixes (3):
#   (1) exam_config.marks_default was read in §2-3b but declared nowhere —
#       now defined in §0 item 2 as an OPTIONAL positive number, fallback 1.
#   (2) Per-question JSON map keys (q_to_classification / options_by_q /
#       q_to_difficulty) — JSON keys are strings; explicit int-normalization
#       rule added to §0 item 3 so Tier-1 lookups can never silently miss.
#   (3) exam_config/difficulty_labels absent no longer collapses every Q to
#       Tier 3: §0 item 2 now defaults difficulty_labels to
#       ['Easy','Medium','Hard'] (MockDeliver parity), keeping Tier 2
#       functional; C10 therefore always has a vocabulary (degraded-check
#       clause removed); edge case 3 updated to match.
#
# v1.2 — 2026-07-23 — Complexity tag: hardcode → three-tier deterministic
#   resolver (§2-3, D11 supersedes D4). v1.1 tagged every question with
#   exam_config.difficulty_default ("Medium" fallback). v1.2 resolves per-Q
#   Complexity through a deterministic tier chain: Tier 1 = q_to_difficulty
#   from the progress JSON (future PYQ-1 assessment — activates automatically
#   when present); Tier 2 = E-9 score_difficulty on the stem via
#   blueprint_core.py (canonical shared copy of Step 5's 3-axis scorer,
#   extracted this session — Cluster E), levels mapped through the fixed
#   Blueprint §7 S7-6 ordinal alias into difficulty_labels; Tier 3 =
#   difficulty_default (v1.1 behavior, now the safety net only).
#   blueprint_core.py becomes a REQUIRED input (§0). Gate C10 extended:
#   Complexity values must be members of difficulty_labels, not merely
#   non-empty. §R3 now reports tier provenance + level distribution.
#   New edge cases 16-19.
#
# v1.1 — 2026-07-23 — Date/Session tag removal (§4A). The per-question
#   date/session tag paragraph (PYQSort date_label, e.g. "[12-Sep-2025 Shift 1]"
#   or "[15-Jun-2025]") that rides through PYQ-1/PYQ-2 above every Q-stem is
#   internal pipeline metadata, not portal content. v1.0 had no removal step,
#   so every question in _PYQ_Final.docx carried its date/session tag — and
#   S5-3's header-strip mis-fired on Q.1's label (false REGRESSION ALARM)
#   while leaving Q.2..Qn labels in place. v1.1 removes ALL date/session tag
#   paragraphs FIRST (before header stripping and tag insertion), mirroring
#   Framework_PYQFormat.md §4 (v1.1) exactly: same DATE_TAG_RE, same
#   media-safety gate, same tags_removed/tags_skipped accounting. Gate C4
#   extended to verify zero date/session tags remain. New decision D10.
#
# v1.0 — 2026-07-22 — Initial release. Takes the audited PYQ explanation
#   document from PYQ-2 (PYQExplainAudit), inserts a 5-line portal tag block
#   (Subject / Topic / Subtopic / Question Type / Complexity) before every
#   Q-stem, applies render-safe transforms (OMML linearization, non-ASCII
#   safe-font, underlined-stem recolor), maintains the PYQ registry, and
#   delivers a tagged, portal-ready Word document to Google Drive.
#
#   Adapted from MockDeliver (Step 11) for the PYQ pipeline. Uses the same
#   tag block format, render transforms, and two-artifact model (integrity +
#   render-source). Key difference: tag values come from q_to_classification
#   (PYQ-1 P3) instead of a registry.json + blueprint.json JOIN, and
#   difficulty is HARDCODED for PYQ papers.
#
#   Architecture decisions locked with the framework owner:
#     D1. FORK INPUT. PYQ-4 takes PYQ-2 output directly
#         ([ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx).
#         PYQ-3 and PYQ-4 are INDEPENDENT — neither depends on the other.
#     D2. SAME PORTAL FORMAT. The output uses the same 5-line tag block as
#         MockDeliver (Step 11) so the portal ingests PYQ papers identically
#         to mock papers. No portal-side changes needed.
#     D3. TAG DATA FROM q_to_classification. Subject/Topic/Subtopic resolved
#         from the classification map built by PYQ-1 P3. No registry.json or
#         blueprint.json JOIN — those do not exist for PYQ papers.
#     D4. [SUPERSEDED BY D11 in v1.2] DIFFICULTY HARDCODED. All PYQ questions
#         got the same difficulty label (exam_config.difficulty_default,
#         fallback "Medium"). Retained as the Tier-3 safety net only.
#     D5. QUESTION TYPE DERIVED. MCQ/MSQ/NAT derived from options_by_q (Row
#         file scan, same as PYQ-1 P2). Not from blueprint marking_scheme
#         (which does not exist for PYQ).
#     D6. PYQ REGISTRY. [ExamCode]_pyq_registry.json tracks which PYQ papers
#         have been delivered, preventing re-delivery and providing a corpus
#         progress dashboard.
#     D7. DRIVE DELIVERY. The final doc is uploaded to Google Drive.
#     D8. TWO-ARTIFACT MODEL. Same as MockDeliver: integrity artifact (OMML
#         intact) + render-source artifact (OMML linearized, safe-font,
#         underline recolor). The render-source is the delivered file.
#     D9. EXPLAIN ENGINE NOT REQUIRED. PYQ-4 reads the docx structurally
#         (Q-stems, tag insertion, render transforms). No explain_engine.py
#         needed. (v1.2 note: blueprint_core.py IS required — see D11/§0 —
#         but only for the pure Cluster E scoring functions, no allocation.)
#     D10. DATE/SESSION TAGS REMOVED (v1.1). The per-question date/session
#         tag paragraph (PYQSort date_label) is stripped from the delivered
#         document. It is internal pipeline metadata; the paper's identity is
#         already carried by the output filename and the PYQ registry entry.
#         Same decision as PYQFormat D8 — both PYQ-2 forks remove it.
#     D11. COMPLEXITY VIA DETERMINISTIC TIER CHAIN (v1.5, supersedes D4).
#         Per-question Complexity resolves through §2-3's FOUR tiers:
#         (1) q_to_difficulty from the progress JSON (PYQ-1 §7A assessment),
#         (1.5) structural_difficulty from exam_config.marking_scheme[],
#         (2) E-9 3-axis scoring via blueprint_core.py, (3) difficulty_default.
#         Every tier is a pure function or a pure lookup — the same document
#         always yields the same tags on every run and every model instance.
#         v1.5 CORRECTS the v1.2 rationale recorded here. That text claimed
#         Tier 2 put PYQ papers "on the SAME difficulty scale the blueprint/
#         mock pipeline is calibrated on". It does not. The mock pipeline does
#         not measure difficulty at all: Step 6 sets a difficulty_schedule
#         QUOTA, Step 7 assigns each generated question a band to fill that
#         quota exactly, and Step 11 tags by registry JOIN. E-9 is nowhere in
#         the mock tagging path, and Framework_Blueprint.md contains zero
#         references to PYQ_DIFFICULTY_CALIBRATION. The two pipelines were
#         never on one scale, so comparability was not a reason to prefer
#         Tier 2 — and Tier 2's measured behaviour on a non-aptitude exam is
#         60/60 questions at one label. Tier 1 is not an "upgrade path" for
#         unusual exams; it is the only tier that measures anything, and it is
#         the intended resolution for every exam. Tier 1.5 is the floor for
#         papers with no PYQ-1 pass. Tier 2 is retained solely because it is
#         always computable, and Tier 3 because a safety net must exist.



# ═══ ARCHIVE — Framework_ScopedBlueprint pre-relocation header history (moved 2026-07-31 at v1.7; verbatim) ═══

# v1.6 — 2026-07-21 — FEATURE: fixed-uniform difficulty override (--difficulty S:M:H). §5 gains
#   a second mode alongside the default/`progressive` envelope-bounded ramp: an explicit S:M:H
#   ratio (same parse/validate rules as the mock's S7-2 — colon or space-separated, whole numbers,
#   sum=100) makes EVERY paper in the series identical, no ramp, and DELIBERATELY BYPASSES the
#   scope envelope (§5 S5-2) — a requested level is honoured even with zero observed PYQ for that
#   scope, per explicit user instruction. This is a FULL OVERRIDE, not envelope-masked: unlike the
#   ramp's silent masking, override mode does not renormalise or substitute — it runs exactly the
#   ratio given. No confirmation echo (mirrors the mock's behaviour on a valid ratio) and no schema
#   addition — blueprint.json's difficulty_schedule[] is written identically to the ramp path, so
#   nothing downstream (Step 7 G-QINDEX, MockTestCreateAudit, MockTestAnalyse) needs to change; all
#   of them already consume difficulty_schedule[N] as a flat per-paper count with zero envelope-
#   awareness. §5 S5-1/S5-2/S5-3 (envelope + ramp) are UNCHANGED and remain the default when
#   --difficulty is omitted or 'progressive'. §10 DoD item 6 and the EXAM-AGNOSTIC GUARANTEE
#   paragraph updated to state the invariant conditionally (mode-dependent) instead of absolutely.
#
# v1.5 — 2026-07-15 — FEATURE: qualified subtopic scope "Subject::Topic::SubTopic" (§2 S2-1,
#   additive). The subtopic level now accepts three forms — (1) exact subtopic_id, (2) NEW
#   "Subject::Topic::SubTopic" (narrows by section+topic, then matches display_name WITHIN that
#   topic — so a name only has to be unique within its topic, not globally), (3) bare display
#   name if globally unique — all resolving to a single subtopic_id before anything else runs.
#   Zero downstream impact (resolution happens pre-emit). Clear HARD STOPs on wrong part-count,
#   no-match (lists sub-topics under the topic), or intra-topic name collision (lists the ids).
#   Proven by blueprint_scoped_scope_test.py + an e2e qualified-scope run.
#
# v1.4 — 2026-07-15 — CRITICAL FIX #3: emit subtopic_list answer_type + answer_cardinality (nested
#   consumer-contract audit). Step 11's tag JOIN reads subtopic_list[].answer_type /
#   .answer_cardinality (the mock emits them) to tag question type; §8-1 omitted both, so Step 11
#   defaulted every scoped question to MCQ-single — mis-tagging NAT/MSQ subtopics. Fix: §1-3 parses
#   both from section_rules via the new pure engine bc.parse_section_rules_field, and §8-1 emits them
#   per subtopic. Found by diffing NESTED field reads (subtopic_list/section/allocation) against §8
#   emits. Locked by e2e (8/8: NAT/MSQ values survive to subtopic_list). Engine: +parse_section_rules_field
#   (self-test 33/33).
#
# v1.3 — 2026-07-15 — CRITICAL FIX #2: emit batch_size_qs (consumer-contract audit). Steps 7/8 read
#   the axis-2 WINDOW size as bp.get('batch_size_qs', 10); §6 built axis_schedule for a window of
#   batch_size papers, but §8 never emitted batch_size_qs → a non-default --batch_size silently fell
#   back to 10 and mis-audited the axis-2 window. Fix: §8 emits 'batch_size_qs': batch_size. Found by
#   diffing every blueprint field Steps 7-11 READ against what §8 EMITS (the integration seam the
#   in-isolation e2e can't see). Locked by a non-default-batch_size assertion in the e2e (8/8).
#
# v1.2 — 2026-07-15 — CRITICAL FIX: blueprint_version emitted the SCHEMA version, not SCOPED_VERSION.
#   §8 had emitted 'blueprint_version': SCOPED_VERSION ('1.0'); Step 7 gates blueprint_version against
#   MIN_BLUEPRINT_VERSION=(1,7) → _ver_tuple('1.0')=(1,0) < (1,7) HARD-STOPPED every scoped generation.
#   Fix: emit BLUEPRINT_SCHEMA_VERSION='1.35' (the shared blueprint.json schema version the mock also emits;
#   passes the floor); SCOPED_VERSION is preserved as scope.scoped_spec_version. The scoped e2e never
#   caught it (it runs the blueprint, not Step 7's gate) — now locked by an emitted-version floor
#   assertion in blueprint_scoped_emit_test.py (6/6) + blueprint_scoped_e2e_test.py (7/7).
#
# v1.1 — 2026-07-15 — REGISTRY SCHEMA SYNC (seed only; zero logic). The §8-7 fresh-registry seed now
#   includes semantic_usage=[] and exhausted_subtopics={} to MATCH the shared schema written by the
#   generation layer (MockCreate v5.22 B) and the mock Blueprint v1.30 seed. Additive; byte-schema-
#   identical to what Step 7 would self-heal. No allocation/emit/behaviour change.
#
# v1.0 — 2026-07-15 — RELEASE. Feature-complete (§1–§10) and adversarially verified. Two full
#   QA passes (end-to-end trace + line-by-line) found and fixed 11 bugs; 0 remain. Verified by:
#   validate_framework_md.py (0 issues, all AST clean); blueprint_scoped_e2e_test.py 7/7 (EXECUTES
#   the assembled spec against mock inputs — fresh/subject/topic/subtopic runs, duplicate-display-
#   name survival, resumption, old-registry migration, batch_size default, axis-schedule keys, and
#   a static scan asserting NO undefined name in any branch); section harnesses alloc 7/7,
#   difficulty 10/10, format 6/6, emit 5/5, resume 7/7; engine self-test 30/30, core_test 20/20,
#   qa_pass2 6/6; pyflakes-clean embedded Python; every bc.* reference resolves to the engine.
#   Blueprint math is the shared engine blueprint_core.py (identical to Framework_Blueprint v1.28).
#   Remaining (separate deliverables, NOT this spec): the generation layer (Step-7 analog) — shared
#   sharded registry, mock_n→paper_id generalisation of Steps 7–11, (item × angle)/spacing-8
#   uniqueness — governed by the §9 registry contract.
#
# v0.1-qa — 2026-07-15 — ADVERSARIAL QA REMEDIATION (end-to-end, two-pass). The per-section
#   harnesses proved every ALGORITHM but supplied inputs as fixtures, so the spec's own
#   data-loading glue and cross-section keying were never exercised. End-to-end tracing found
#   and fixed 8 bugs: (1-4) exam_config / section_rules / excel / flag were USED but never
#   loaded/defined -> added the loads in §1-3 (section_rules via the new pure engine parser
#   bc.parse_section_rules_difficulty) + the flag helper; (5) DISPLAY-NAME KEYING collapsed
#   subtopics that share a display name within a scope -> re-keyed r_avg/allocation/emit to
#   subtopic_id end-to-end (Excel keyed by the taxonomy triple); (6) paper_start was used in
#   §8 but defined in §9 (after) -> relocated the registry load/gates to §1-4 and the resume
#   offset to §2-4, so paper_id numbering resumes correctly (no collisions); (7) registry load
#   misplaced -> §1-4; (8) engine mandate hardened to always import the freshly-copied engine.
#   Now proven by blueprint_scoped_e2e_test.py (6/6: EXECUTES the assembled spec against mock
#   inputs — fresh/subject/topic/subtopic runs, duplicate-display-name survival, resumption,
#   old-registry migration, AND a static scan asserting NO undefined name in any branch) plus
#   the five section harnesses (alloc 7/7, difficulty 10/10, format 6/6, emit 5/5, resume 7/7).
#   Engine: bc.parse_section_rules_difficulty added (self-test 30/30, core_test 20/20).
#
# v0.1 — 2026-07-15 — INITIAL DRAFT. Built: §1 (session start, engine mandate, trigger,
#   manifest load), §2 (scope selection + synthetic section), §3 (frequency), §4 (scoped
#   allocation: per-batch independent allocation, coverage floor, Zero-PYQ floor, EC-11
#   gate), §5 (difficulty: batch-local envelope-bounded ramp + cascade), §6 (format: hybrid
#   per-scope three-axis signature — SUBJECT scope uses the precomputed subject distribution;
#   TOPIC/SUBTOPIC rescope axis-2 from in-scope observed_axis2 and inherit axis-1/3 from the
#   subject; ALL THREE axes renormalised to Q; zero-PYQ topic→subject→default cascade;
#   section-relabel so the engine's pool-caps/feasibility filter matches in-scope ids).
#   NOTE: bc.largest_remainder_apportion assumes its input sums to ~target (true for the mock,
#   where real per-paper counts ≈ sec_qs); §6 normalises all three axes to Q so the internal
#   apportionment deficit stays ~0 (a real-per-paper input summing >> Q would trip the
#   apportioner's iteration guard and truncate — avoided by normalising, NOT an engine change).
#   Proven: §4 blueprint_scoped_alloc_test.py 7/7; §5 blueprint_scoped_difficulty_test.py
#   10/10; §6 blueprint_scoped_format_test.py 6/6; §7+§8 blueprint_scoped_emit_test.py
#   5/5 (marking tier selection + full blueprint.json schema completeness). Built §7 (marking:
#   modal tier for multi-tier subjects) + §8 (emit: complete blueprint.json in the exact shape
#   Steps 7-11 read, single-section, per-paper paper_id). §9 (resumption: shared-registry
#   load/seed, exam_code + taxonomy-drift + completeness HARD-STOP gates, auto-migration of old
#   mock-only registries [snapshot→migrate→verify→idempotent], per-scope paper_id counter resume,
#   append-only tier-agnostic, + the generation-layer registry CONTRACT) — blueprint_scoped_resume_test.py
#   7/7. ALL §1-§9 BUILT (feature-complete draft). Pending: full adversarial QA, then v0.1 → v1.0.
#


# ═══ ARCHIVE — Framework_PYQFormat pre-relocation header history (moved 2026-07-31 at v1.4.1; verbatim) ═══

# v1.4 — 2026-07-24 — DOCX SERIALIZATION SAFETY. Fixes the P0 defect where a
#   v1.3 run completed every §8 check, reported success, and delivered a file
#   Microsoft Word refused to open ("Word found unreadable content in …").
#
#   CONFIRMED by forensic analysis of the failing artefact
#   (IIT_JAM_BIOTECHNOLOGY_15-Feb-2026_PYQ_Formatted.docx) against its input.
#   The INPUT was schema-valid: 0 errors. The OUTPUT carried 812 reported
#   schema errors plus undeclared namespaces — ALL introduced by PYQFormat.
#
#   Root cause (measured, not inferred):
#     (a) NAMESPACE LOSS — stdlib xml.etree.ElementTree was used. Measured on
#         the artefact: the root went from 19 declared prefixes to 7. Fifteen
#         were lost (cx, cx1, m, o, v, w10, w14, w15, w16se, wne, wp14, wpc,
#         wpg, wpi, wps) and an invented prefix "ns6" appeared where the
#         source used "a14". mc:Ignorable survived verbatim as
#         "w14 w15 w16se wp14" — naming FOUR prefixes that no longer exist.
#         Word's MCE preprocessor resolves those, fails, and rejects the file.
#         S13-3 warned "no cleanup_namespaces()" — an lxml-only function —
#         while never mandating lxml, so the spec's only defence was
#         VACUOUSLY SATISFIED while the corruption occurred.
#     (b) SCHEMA ORDER — S13-5/S13-1 listed elements to add with no ordering
#         requirement, and they were appended in the order written. Measured
#         on the artefact:
#             observed pPr  [shd, pBdr, ind, spacing, keepNext, keepLines]
#             correct  pPr  [keepNext, keepLines, pBdr, shd, spacing, ind]
#             observed tblPr[tblW, tblLayout, tblBorders, tblCellSpacing]
#             correct  tblPr[tblW, tblCellSpacing, tblBorders, tblLayout]
#             observed tcPr [tcW, shd, vAlign, tcMar]
#             correct  tcPr [tcW, shd, tcMar, vAlign]
#             observed tcMar[top, bottom, left, right]
#             correct  tcMar[top, left, bottom, right]
#             observed pill cell pPr [jc, spacing] / correct [spacing, jc]
#             observed header1+footer1 pPr [tabs, spacing, pBdr]
#             correct                      [pBdr, tabs, spacing]
#         Counts: 244 pBdr, 180 tcMar, 180 spacing, 146 keepNext,
#         60 tblBorders in document.xml, plus 1 pBdr each in header1.xml and
#         footer1.xml. The header/footer parts created by S13-6 were defective
#         too — the fault is NOT confined to the body.
#     (c) NO VALIDITY GATE. All eight §8 checks are CONTENT-fidelity checks.
#         A document.xml with undeclared mc:Ignorable prefixes and misordered
#         properties is still well-formed XML and parses cleanly in both
#         stdlib ET and lxml — so Q-count, OMML count, drawing count and the
#         full text-stream check (S8-8) all PASSED on a file Word cannot open.
#         Verified on the artefact: text stream, all 11 drawings and all
#         paragraph counts were perfectly intact. §11 item 10 already required
#         "a valid .docx that opens clean in Microsoft Word" with no machinery
#         anywhere to verify it.
#     (d) NESTED DEFECTS ARE MASKED. Repairing the artefact required
#         reordering 991 elements although only 812 errors were reported: once
#         a parent is rejected at its own position the validator does not
#         descend into it, so its children's violations stay hidden. tcMar's
#         internal [top, bottom, left, right] was invisible behind tcMar's own
#         misplacement in tcPr. An error count is a LOWER BOUND until it
#         reaches zero — see S8-9.
#
#   Fixes:
#     1. S13-3 REWRITTEN — lxml is now MANDATORY for editing existing parts;
#        stdlib ElementTree is FORBIDDEN (it cannot preserve mc:Ignorable
#        prefixes even when fully registered); cleanup_namespaces() forbidden.
#     2. NEW S13-7 — OOXML schema ordering discipline: seven authoritative
#        child-order tables extracted from the ISO-IEC29500-4:2016 XSD, plus
#        the runnable set_child() insertion function. set_child() inserts at
#        the schema-correct position and NEVER reorders existing children —
#        a whole-parent sort corrupts Word-native tcMar (top,left,bottom,
#        right) and paragraph-mark rPr carrying <w:del>, both verified.
#        CT_ParaRPr (<w:pPr><w:rPr>) is distinguished from CT_RPr (<w:r><w:rPr>).
#        Applies to EVERY part written, header1.xml and footer1.xml included.
#     3. NEW S8-9 — package validity gate (HARD STOP). Runs the OOXML
#        validator on the delivered file with --original so only NEW errors
#        block. This is the layer that generalises: it catches Defect (a),
#        Defect (b), and serialization defects not yet encountered.
#     4. S13-1 and S13-5 amended to route every property insertion through
#        set_child().
#   New architecture decision D11.
#
# v1.3 — 2026-07-23 — Page-level header and footer (every page). The exam
#   header (§3) and IFAS footer (§6) are no longer one-time body paragraphs;
#   they are real Word page header/footer PARTS (header1.xml / footer1.xml
#   wired via sectPr references) that repeat automatically on every page.
#   Header layout: exam name LEFT, date · session CENTER, IFAS RIGHT.
#   Footer layout: website LEFT, tagline CENTER, phone RIGHT. Tagline (D5)
#   changed to "IFAS – India's No. 1 Exam Preparation Platform". No page
#   numbers; first page identical to all others. Body insertions are now
#   pills ONLY, simplifying S8-3/S8-8. New decision D10; new S13-6
#   part-wiring mechanics.
#
# v1.2 — 2026-07-23 — Explanation tag restyle (§7-4..§7-6). The explanation
#   tag headers (AXIOM, DEDUCTION, SPEED HACK, WHY WRONG?, COMMON PITFALLS),
#   the Correct Answer line, and the Option/pitfall sub-heads are restyled
#   into colored tint bands with 3pt left accent bars, per-tag colors from
#   the document-wide design palette (Appendix A). Marker glyphs upgraded
#   in tag headers only: ⬛→📘 (AXIOM), ⬛→🧮 (DEDUCTION), ❌→⚠️ (COMMON
#   PITFALLS); ⚡ and ❌ WHY WRONG? unchanged. The glyph substitution is the
#   ONLY text change PYQFormat ever performs (D9) — verified by a new
#   full-document text-stream integrity check (S8-8). Delivery report gains
#   §R6 (Tag styling). New architecture decision D9.
#
# v1.1 — 2026-07-23 — Date/Session tag removal (§4). The per-question
#   date/session tag paragraph (PYQSort date_label, e.g. "[12-Sep-2025 Shift 1]"
#   or "[02-Feb-2025]") that rides through PYQExplain/PYQExplainAudit above
#   each question is now REMOVED from the student-facing document. This is the
#   ONLY sanctioned deletion — the zero-mutation rule is amended accordingly.
#   Removal uses a keyword-agnostic anchored regex (works even when
#   exam_config.json is absent), verifies each removed paragraph is media-free
#   (no OMML, no drawings), and a new integrity check (S8-7) confirms zero tag
#   paragraphs remain in the output. Delivery report gains §R4 (Tags removed).
#   New architecture decision D8.
#
# v1.0 — 2026-07-22 — Initial release. Takes the audited PYQ explanation
#   document from PYQ-2 (PYQExplainAudit) and transforms it into a beautiful,
#   student-facing Word document: page header/footer on every page, per-
#   question colored Subject/Topic/Subtopic pills, and visual polish.
#   ZERO content changes — every question, option, explanation sentence, and
#   OMML fraction is byte-identical to the input. This is purely a VISUAL
#   transformation step.
#
#   Architecture decisions locked with the framework owner:
#     D1. ZERO CONTENT CHANGES. Not one character of any question, option,
#         explanation, or answer is modified. PYQFormat adds visual elements
#         AROUND the certified content — never inside it.
#     D2. FORK INPUT. PYQ-3 takes PYQ-2 output directly
#         ([ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx).
#         PYQ-3 and PYQ-4 are INDEPENDENT — neither depends on the other.
#     D3. COLORED PILLS (Option C). Per-question Subject/Topic/Subtopic
#         displayed as three colored pill cells (1-row, 3-cell table) inserted
#         BEFORE each Q stem. Subject = blue tint, Topic = green tint,
#         Subtopic = amber/orange tint. Pills are inserted HERE (PYQFormat),
#         NOT in PYQExplain/PYQExplainAudit — keeping the explanation doc
#         clean for engine verification.
#     D4. PILL DATA SOURCE. The q_to_classification map built by PYQ-1 at P3
#         (stored in pyq_explain_progress.json or pyq_audit_progress.json)
#         provides {subject, topic, subtopic, subtopic_id} per question.
#     D5. IFAS BRANDING HARDCODED. Same branding across all exams — no
#         per-exam customization needed.
#     D6. EXAM HEADER FROM CONFIG. Exam name from exam_config.json; date and
#         session from the trigger/filename.
#     D7. STUDENT-FACING OUTPUT. This file is the final download artifact
#         students receive. It must look professional and beautiful.
#     D8. DATE/SESSION TAGS REMOVED (v1.1). The per-question date/session tag
#         paragraphs (PYQSort date_label lines) are internal pipeline metadata,
#         not student content. PYQFormat removes them. The paper's date and
#         session already appear ONCE in the exam header (§3) — repeating them
#         above every question adds noise. This is the ONLY deletion PYQFormat
#         ever performs.
#     D9. EXPLANATION TAG RESTYLE (v1.2). The engine (explain_engine.py)
#         deliberately writes plain headers (black text, no shading) so the
#         explanation document stays clean for engine/audit verification —
#         same rationale as D3. PYQFormat restyles them for students: tint
#         band + accent bar per tag, one palette shared with the pills.
#         Marker glyph substitution (⬛→📘/🧮, ❌→⚠️ on COMMON PITFALLS) is
#         the ONLY text change in the whole spec, allowed in exact-match tag
#         header paragraphs only, and verified by S8-8.
#     D10. PAGE-LEVEL HEADER/FOOTER (v1.3). The exam header and IFAS footer
#         are Word page header/footer parts, not body paragraphs — Word
#         repeats them on every page automatically, surviving any reflow.
#         References are registered for default, even, AND first page types
#         pointing to the same parts, so every page is identical regardless
#         of the document's evenAndOddHeaders / titlePg settings. No page
#         numbers. Tagline (D5 constant) is
#         "IFAS – India's No. 1 Exam Preparation Platform".
#     D11. SERIALIZATION SAFETY IS MECHANISM + GATE, NOT PROSE (v1.4). Content
#         fidelity and package validity are INDEPENDENT properties. Every §8
#         check verifies content; none verified validity, so a structurally
#         broken file passed all of them and shipped. Therefore PYQFormat
#         (i) mandates ONE library (lxml) rather than describing a desired
#         outcome, (ii) supplies runnable code (set_child) rather than an
#         ordering instruction, and (iii) gates the delivered artefact with a
#         real OOXML validator (S8-9). Prose stating what must be true is not
#         a safeguard — across 200 exams each fresh run re-decides anything
#         left to interpretation. Only a mandated mechanism plus a gate that
#         inspects the produced file makes the guarantee hold every time,
#         including for defect modes not yet seen.



# ═══ ARCHIVE — Framework_MockDeliver pre-relocation header history (moved 2026-07-31 at v1.9; verbatim) ═══

#   v1.8 — 2026-07-18 — C17: NAT PORTAL GRADING-VALUE CHARSET (last-mile defense-in-depth;
#       part of the same defect chain as Framework_MockTestCreate.md v5.25/v5.26,
#       Framework_MockTestCreateAudit.md v2.8, Framework_MockTestExplainAudit.md v1.12, and
#       explain_engine.py v1.16/v1.17). New gate_c17_natcharset(out_docx, tag_lookup): on
#       the FINAL DELIVERED docx, immediately before present_files, independently
#       re-validates every NAT question's rendered 'Correct Answer:' value against the
#       delivery portal's grading charset ('0123456789.-' only — no scientific notation,
#       units, spaces, en-dash, or parentheses). Scoped by tag_lookup's ALREADY-RESOLVED
#       question_type (never re-derived a second time) rather than by pattern-matching the
#       value, because a numeric-labeled MCQ's 'Correct Answer: 3' is legitimately
#       charset-identical to a NAT point value and must not be confused with it, and an
#       MSQ's 'Correct Answer: 2, 4' is a different field entirely. Any violation is a HARD
#       STOP — this is the last gate in the pipeline; there is no later step to catch it.
#       Checklist: 16 → 17 gates (three live-count references updated: §6 title, §10 step
#       11, §8 delivery-report Checklist line — historical changelog mentions of "16" left
#       untouched as accurate period record). Also retired (annotated, not deleted, for any
#       older mid-pipeline document) the now-dead 'Accepted Range' EXPL_MARKERS entry: that
#       separate-paragraph format was replaced when explain_engine.py v1.16 folded a NAT
#       range directly into the same Correct-Answer line; 'Correct Answer' alone already
#       covers detection of the current format. No other gate, transform, or rendered byte
#       changed.
#
# PURPOSE:
#   Take the audited Solutions document from Step 10 (MockExplainAudit),
#   JOIN per-question metadata from registry.json + blueprint.json,
#   INSERT a 5-line tag block (Subject / Topic / Subtopic / Question Type /
#   Complexity) before every Q-stem, apply render-safe transforms (OMML
#   linearization, non-ASCII safe-font, underlined-stem recolor), and
#   deliver a tagged, upload-ready Word document (.docx).
#
#   This is the LAST step in the mock test pipeline. Its output is the
#   final learner-facing artifact uploaded to the distribution platform.
#
# PIPELINE POSITION:
#   Step 5  PYQExtract       → section_rules.md, subtopic_manifest.json
#   Step 6  MockBlueprint    → blueprint.json, registry.json (template)
#   Step 7  MockCreate       → [ExamCode]_Mock[N]_Create.docx, registry.json
#   Step 8  MockCreateAudit  → rectified paper, re-synced registry
#   Step 9  MockExplain      → [ExamCode]_Mock[N]_Explanation.docx
#   Step 10 MockExplainAudit → [ExamCode]_Mock[N]_Explanation_Complete.docx
#   Step 11 MockDeliver      → [ExamCode]_Mock[N]_Final.docx   ← THIS STEP
#
#   Step 11 runs in the [ExamCode] project (exam-specific).
#   Step 11 runs AFTER Step 10 has completed and the audited Solutions docx is available.
#
# INPUTS:
#   1. Solutions docx — attached by user (output of Step 10 or Step 9)
#      Accepted filenames: [ExamCode]_Mock[N]_Explanation_Complete.docx
#                          [ExamCode]_Mock[N]_Explanation.docx
#   2. [ExamCode]_blueprint.json   — in project knowledge (loaded automatically)
#   3. [ExamCode]_registry.json    — in project knowledge (loaded automatically)
#
# OUTPUT:
#   One tagged Word document (.docx) — delivered via present_files.
#   Filename: [ExamCode]_Mock[N]_Final.docx
#
# TRIGGER FORMAT:
#   Step 11: MockDeliver M[N]
#   Trigger matching is case-insensitive.
#   [N] = mock number (positive integer).
#   ExamCode read from blueprint.json in project knowledge.
#   The Solutions docx must be attached to the trigger message.
#
# RUNS IN: [ExamCode] project (exam-specific, where blueprint.json and
#          registry.json are in project knowledge)
#
# EXECUTION MODEL: Single script, 4 tool calls maximum. No "Continue" needed.
#   1. create_file  → write complete deliver_pipeline.py
#   2. bash_tool    → run it (parse + join + tag + integrity + render-source + validate)
#   3. bash_tool    → verify Q-count, tag counts, render-source checks
#   4. present_files → deliver
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains ZERO hardcoded exam values. No section name, no topic name,
#   no subtopic name, no question count, no Q-number range, no option label, no
#   difficulty label, no question type string is hardcoded.
#   All tag values are JOIN-derived from blueprint.json and registry.json at runtime.
#   Same spec runs for SSC CGL (4 sections, 100Q), GATE (1 section, 65Q),
#   UPSC (variable), or any MCQ/MSQ/NAT exam.
#
# VERSION HISTORY:
#   v1.7 — 2026-07-18 — POSITION-BASED QUESTION TYPE RESOLUTION FIX (GAP_ANALYSIS:
#       Question Type Mislabeling in Step 11, discovered via GATE_ECOLOGY_EVOLUTION
#       Mock 3 Tagged.docx — 23/65 Question Type tags wrong, incl. all 11 MSQ positions).
#       Root cause: resolve_question_type() used ONLY blueprint.subtopic_list[].
#       answer_type + .answer_cardinality — whole-subtopic properties from Step 5's
#       PYQ majority vote. For position-based exams (GATE: Q25-31/44-47 always MSQ,
#       Q32-35/48-65 always NAT, regardless of which subtopic Step 6 assigns there),
#       this is the wrong axis: the same subtopic legitimately carries different
#       Question Types across different Q-ranges/mocks (see new EC-13). Step 7 already
#       resolves this correctly via _type_for_q() reading blueprint.marking_scheme[]
#       (Step 2a v2.5+ contract) — Step 11 never read that field.
#       FIX: build_tag_lookup() now classifies each paper ONCE by counting DISTINCT
#       question_type values in blueprint.marking_scheme[]. >1 distinct type →
#       position-based — Question Type resolved from marking_scheme by Q-number
#       (mirrors Step 7's _type_for_q(), HARD STOPs if a Q is uncovered — never
#       guesses). 0/1 distinct type → subtopic-based — unchanged v1.6 resolution.
#       CRITICAL SAFEGUARD: every scoped blueprint (Framework_ScopedBlueprint.md §7)
#       deliberately collapses marking_scheme to ONE modal-type [1,Q] range even when
#       the scope has heterogeneous MCQ/MSQ/NAT subtopics — this correctly falls into
#       subtopic-based mode (1 distinct type), so scoped-test tagging is UNCHANGED and
#       still driven by each subtopic's own answer_type/answer_cardinality (S8-1:
#       "Step 11 tagging (mock parity)"). Verified via isolated 17/17 test harness
#       (test_resolve_question_type.py) covering: GATE-style multi-type position-based
#       resolution against the real Mock 3 error set (23/65, all now correct); SSC
#       CGL-style single-type byte-identity with v1.6; scoped-blueprint modal-collapse
#       non-regression (NAT/MSQ subtopics inside an MCQ-modal scope still tag
#       correctly); legacy empty-marking_scheme byte-identity; out-of-range Q HARD
#       STOP; blank question_type entries excluded from the distinct-type count.
#       Backward-compatible: any blueprint with 0 or 1 distinct marking_scheme type
#       (every exam except position-based ones, and 100% of scoped tests) produces
#       BYTE-IDENTICAL output to v1.6. §1 S1-2, S1-3, §3 (architectural note, S3-1,
#       S3-2/S3-2a/S3-2b), EC-3, EC-4, NEW EC-13, §8 delivery report all updated.
#   v1.6 — 2026-07-15 — C3: paper_id PROPAGATION (Step 11; additive, mock output bit-identical).
#       Derives paper_id/paper_slug from the blueprint (C1; fallback "MOCK:M{N:02d}"); the
#       deliverable names (integrity, Final ×2) use paper_slug ("Mock[N]" for a mock — unchanged);
#       the question_index JOIN keys on paper_id (self-contained from blueprint+mock_n). Engine
#       untouched. Proven by blueprint_c3_propagate_test.py. Pairs with MockCreate v5.21.
#   v1.5 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#          Tagged output renamed [ExamCode]_Mock[N]_Tagged.docx →
#          [ExamCode]_Mock[N]_Final.docx. Accepted inputs renamed accordingly:
#          [ExamCode]_Mock[N]_Explanation_Complete.docx (Step 10, preferred) /
#          [ExamCode]_Mock[N]_Explanation.docx (Step 9, acceptable). Internal scratch names
#          (_src.docx, _integrity.docx), the C1–C16 checklist and all render transforms
#          unchanged. Pipeline-position header + §8 naming updated to match.
#   v1.4 — 2026-07-11 — FIGURE SECTION REMOVED FROM SOLUTIONS LAYOUT LEGEND
#          (parallel to Step 9 v1.13 / Step 10 v1.8). Step 9 no longer renders the
#          ⬛ FIGURE / figure-description block, so the §S2-2 per-question interleaved-
#          Solutions layout legend drops those two lines. The per-question block is now
#          Correct Answer → ⬛ AXIOM → ⬛ DEDUCTION → (⚡ SPEED HACK) → ❌ WHY WRONG? /
#          ❌ COMMON PITFALLS for every question type. Documentation-only; MockDeliver
#          reads and delivers the finished docx and never rendered or checked the FIGURE
#          header, so there is zero logic change.
#   v1.3 — 2026-07-09 — DOCX VALIDITY HARDENING (fixes Word "unreadable content —
#          recover?" on the delivered Final.docx). Roots out an OOXML-corruption class
#          that python-docx and LibreOffice opened SILENTLY while Microsoft Word — the
#          only strict consumer — rejected. SIX exam-agnostic fixes:
#          (1) ROOT CAUSE — removed etree.cleanup_namespaces() from BOTH the integrity
#              assembly (§5 Phase 3) AND the render-source assembly (§5 Phase 5). It
#              stripped root xmlns declarations (w14/wp14/o/v/w10 + drawing namespaces)
#              that mc:Ignorable and drawing/VML content still reference, which Word
#              treats as corrupt. NOTE: Phase 3 mutated the SHARED tree in place and
#              Phase 4 deepcopied it, so removing only one call site was insufficient —
#              BOTH had to go.
#          (2) §4-3 make_tag_para now emits <w:spacing> BEFORE <w:jc> (OOXML CT_PPr
#              child-order; jc-first was schema-invalid).
#          (3) §5 Phase 3/5 — stopped stripping word/webSettings.xml (retired Rule 14).
#              The part is benign; keeping it removes the dangling relationship (in
#              document.xml.rels) and dangling Override (in [Content_Types].xml) that a
#              strip-without-cleanup leaves behind — a second corruption trigger. Gate
#              C9 repurposed from "webSettings absent" to a dangling-reference check.
#          (4) §1 S1-3 build_tag_lookup — JOIN now accepts subtopic_id when present and
#              falls back to (section, subtopic) with a duplicate-key guard; tolerant of
#              both registry schemas so a clean run never hard-stops on the key name.
#          (5) §6 + §10 — NEW gate C16 (namespace + reference + tag-order integrity),
#              optional OOXML-XSD validation, a 4th hard invariant, and a MANDATORY
#              single Microsoft Word open as the final human acceptance check.
#          (6) §7 Rule 21 — multi-font fallback: _SAFE_STACK extended with FreeSans;
#              font is chosen PER non-ASCII codepoint (first stacked font that covers
#              it) so section markers ❌ ⬛ ✅ ⚡ no longer render as tofu; codepoints no
#              stacked font covers KEEP their original font (so Word can substitute) and
#              are logged in the delivery report. Preflight (§1 S1-2) now verifies the
#              fallback font is installed.
#          PROPAGATION: this is the exam-agnostic MASTER. Every exam project MUST re-sync
#          its Step-11 spec from this file — a per-project copy left at v1.1/v1.2 will
#          reproduce the corruption. This v1.3 supersedes BOTH earlier "v1.2" documents
#          (the header-strip demotion below AND the standalone docx-validity amendment).
#   v1.2 — 2026-07-09 — HEADER-STRIP DEMOTED TO SAFETY-NET (pairs with Step 7 v5.18 /
#          Step 8 v2.7). The input Solutions docx is now questions-only BY CONSTRUCTION:
#          Step 7 R8b / G-PREQ1 never emits a pre-Q.1 title/info/scoring/cover block, and
#          Step 8 A-HEADER strips any residual. So detect_header_paras() should ALWAYS find
#          zero. It is retained UNCHANGED as a defensive safety-net; if it ever strips a
#          paragraph, that is an UPSTREAM REGRESSION (Step 7/8) and is now flagged as a
#          REGRESSION ALARM in the delivery report. DoD #1, §2 S2-1, EC-1, EC-2, the
#          ZERO-MUTATION note, the §8 delivery report, and the §10 checklist reworded
#          accordingly. Zero logic change to the strip / tag / render code.
#   v1.1 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#          Added post-delivery footer rendering reference to Framework_DeliveryFooter.md
#          v1.3 in §8 (File Naming & Delivery). F2 (step-complete) footer rendered after
#          present_files and delivery report. Step 11 uses the special "Pipeline complete"
#          bottom text (last step in pipeline). Zero logic change.
#   v1.0 — Initial release. JOIN-derived tag architecture (replaces AI classification).
#          Tag values resolved from registry.question_index + blueprint.subtopic_list.
#          Render-source transforms (Rules 19, 21, 22) inherited from proven T2 pipeline.
#          Two-artifact model (integrity + render-source). 15-gate validation.
#          Zero-mutation rule. Exam-agnostic throughout.



# ═══ ARCHIVE — Framework_PYQExplain pre-relocation header history (moved 2026-07-31 at v1.1; verbatim) ═══

# v1.0 — 2026-07-22 — Initial release. Takes one PYQ Row file (Step 1 output,
#   original exam order, Q.1-Q.N continuous) and produces an explained PYQ paper
#   with a validated ExplanationBlock interleaved after each question. Uses the
#   SAME explain_engine.py as TestExplain (Steps 9/10) — shared engine, separate
#   spec. Zero modifications to any existing pipeline file.
#
#   Architecture decisions locked with the framework owner:
#     D1. SOURCE IS THE ROW FILE. The Step-1 PYQPrepare output (Google Drive) is
#         the source document — already in original exam order (Q.1-Q.N continuous).
#         NOT the Sorted file (which destroys exam order).
#     D2. NO BLUEPRINT. PYQ papers have no blueprint.json — this spec builds a
#         lightweight PYQ metadata object internally from section_rules.md +
#         subtopic_manifest.json + exam_config.json (all from prior Steps 2-5,
#         already in the project).
#     D3. NO REGISTRY. PYQ papers have no registry.json — options_by_q is derived
#         from the Row file itself (count option paragraphs per question; 0 = NAT).
#     D4. INDEPENDENT DERIVATION. Every answer derived from first principles
#         (same RE-1/RE-6 contract as TestExplain). Official answer keys, if they
#         exist, are ignored — the PYQ explanation is a derive-independently product.
#     D5. ONE PAPER AT A TIME. Each trigger processes one Row file. No batching
#         across papers.
#     D6. FORK ARCHITECTURE. PYQExplain output feeds BOTH PYQExplainAudit (PYQ-2)
#         AND is the upstream source for PYQFormat (PYQ-3) and PYQDeliver (PYQ-4).
#         PYQ-3 and PYQ-4 are INDEPENDENT of each other (both take PYQ-2 output).
#     D7. ENGINE-BUILT, NEVER FORKED. explain_engine.py is IMPORTED and used
#         exactly as TestExplain uses it (same EngineConfig, ExplanationBlock,
#         build_interleaved_docx, verify_fidelity/structure/explanations). Zero
#         engine modifications — the engine stays a single canonical copy.
#


# ═══ ARCHIVE — Framework_PYQExplainAudit pre-relocation header history (moved 2026-07-31 at v1.1.1; verbatim) ═══

# v1.1 — 2026-07-24 — §10A DIFFICULTY VALIDATION. PYQ-1 v1.1 §7A now assesses
#   per-question difficulty from its derivation observations and writes
#   q_to_difficulty into pyq_explain_progress.json. PYQ-2 already re-derives every
#   answer independently, so it holds a SECOND, independent set of exactly the same
#   observations at no extra cost. §10A turns that into a validation pass and writes
#   the validated map to pyq_audit_progress.json — which PYQ-4 reads FIRST (§0
#   priority order), so the audited values take precedence over PYQ-1's.
#   Additive: no existing lane, gate, verdict, or rectification behaviour changes,
#   and difficulty is NEVER a rectification target in the document.
#
# v1.0 — 2026-07-22 — Initial release. The independent auditor and rectifier
#   of PYQ explanation documents produced by PYQ-1 (PYQExplain). Takes the
#   PYQ-1 output ([ExamCode]_[date]_[session]_PYQ_Explanation.docx) and the
#   original Row file, re-derives every answer, deep-audits every explanation
#   across three lanes (correctness, sufficiency, proportion), rectifies
#   defects, and delivers [ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx
#   only after the mechanical completion gate (explain_audit_gate.py CA1-CA7)
#   prints PASS.
#
#   Uses the SAME explain_engine.py + explain_audit_gate.py as MockExplainAudit
#   (Step 10). Shared engines, separate spec. Zero modifications to any existing
#   pipeline file.
#
#   Architecture decisions locked with the framework owner:
#     D1. NO INHERITED KEY. PYQ-1 publishes no answer-key sidecar (PYQ-1 D4).
#         PYQ-2 re-derives every answer independently and writes its own
#         [ExamCode]_[date]_[session]_pyq_audit_answer_keys.json.
#     D2. THE READER LIVES IN THE ENGINE. parse_solution_blocks is an engine
#         function driven by the same EngineConfig PYQ-1 wrote with — the exact
#         inverse of the writer. No hand-parsing.
#     D3. LEARNINGS LOOP IS EMIT-NOW. PYQ-2 emits
#         [ExamCode]_PYQ_EXPLAIN_AUDIT_LEARNINGS_v1.md; PYQ-1 consumes it at
#         its P1 (PYQ-1 §24).
#     D4. INDEPENDENT DERIVATION. Official exam-body answer keys are IGNORED.
#         PYQ-2 derives every answer from scratch (same contract as PYQ-1 D4).
#         When official keys exist and the user provides them, PYQ-2 cross-
#         checks derived answers against the official key and FLAGS discrepancies
#         for human review — never auto-overrides the derivation.
#     D5. OUTPUT FILENAME. The audited document is
#         [ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx. The input
#         is never modified in place.
#     D6. PER-BATCH RECTIFICATION. Fix in the same batch that finds the defect.
#     D7. FORK OUTPUT. PYQ-2's output feeds BOTH PYQ-3 (PYQFormat) and PYQ-4
#         (PYQDeliver) independently. PYQ-3 and PYQ-4 are independent of each
#         other — both take this output directly.
#     D8. PYQ DEFECT HANDLING. PYQ papers are exam-body publications — defects
#         are FACTS, not fixable pipeline bugs. PYQ-2 notes them — there is
#         no upstream step to fix the paper (contrast with mock pipeline
#         where MockExplainAudit sends paper defects back for repair).
#     D9. ENGINE-BUILT, NEVER FORKED. explain_engine.py + explain_audit_gate.py
#         are IMPORTED and used exactly as MockExplainAudit uses them. Zero
#         engine modifications.
#


# ═══ ARCHIVE — Framework_PYQCompress pre-relocation header history (moved 2026-07-31 at v1.1; verbatim) ═══

#   v1.0 — 2026-07-25 — Initial release. Layer 2 of the corpus-transport response
#          (Framework_MockTestAnalyse v2.29 · Framework_PYQSort v1.12 ·
#          Framework_PYQAnalyse v2.22 · Framework_PYQPrepare v1.9 · corpus_io v1.0.1).
#          Upload → census → governor → parity assert → survival gate → deliver.
#          Filename preservation is a HARD RULE (§2) because a renamed copy alongside
#          the original is counted as a second paper by every enumeration in the
#          pipeline — a silent year-level double count, which is a worse outcome than
#          the transport problem being solved.



# ═══ ARCHIVE — Framework_DeliveryFooter pre-relocation header history (moved 2026-07-31 at v1.8; verbatim) ═══

#   v1.6 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#          Per-step registry (§3) + LOCAL_ONLY badge globs (§2) updated to the new
#          deliverable names: Step 7 Complete→Create, Step 8 Complete→Create_Complete,
#          Step 9 Solutions→Explanation, Step 10 Solutions_Audited→Explanation_Complete,
#          Step 11 Tagged→Final. The single Mock*_Complete.docx glob is SPLIT into two
#          distinct patterns (Mock*_Create.docx + Mock*_Create_Complete.docx) since Step 7
#          and Step 8 outputs are now distinct files. Glob cross-match + badge logic
#          re-tested: each delivered file matches exactly one pattern. The v1.2 changelog
#          entries below are preserved as history and intentionally keep the old names.
#   v1.5 — 2026-07-09 — RENDERING CONTRACT REBUILT (widget dependency removed).
#          ROOT CAUSE of the intermittent footer failures seen across the pipeline:
#          §4 mandated rendering via the LOCAL show_widget / visualizer MCP server.
#          Whenever that local server was down, not loaded, timed out, or simply
#          unreachable (a teammate on a different machine, mobile, web, or a
#          scheduled run), the footer silently degraded to improvised text — an
#          ASCII banner one time, bullets another, a monospace block a third — which
#          reads as "broken." Same spec, different result per run = an external
#          dependency, not a logic bug. Proof: identical steps rendered clean in some
#          sessions and broke in others; one session even printed "the local
#          visualizer MCP server timed out."
#          FIX: §4 is now a PURE-MARKDOWN contract requiring ZERO external tools.
#          It renders byte-identical on every surface and every team member's machine.
#          (1) §4 fully rewritten: Markdown templates replace all HTML/widget structure.
#          (2) State COLOR THEME via Unicode emoji bands — GREEN (complete) /
#              AMBER (in progress) — renders identically everywhere (no CSS).
#          (3) §4-0 rules: canonical Markdown is MANDATORY; show_widget/visualizer is
#              FORBIDDEN; improvised fallbacks (ASCII banners, monospace footers,
#              ad-hoc lists) are FORBIDDEN. The template is the only permitted output.
#          (4) §4-4 added: deterministic progress bars (no guessing at position).
#          (5) §1 VISUAL IDENTITY blocks are SUPERSEDED by §4 (pointer note added at
#              the top of §1). §1 WHEN-TO-SHOW and CRITICAL RULES logic unchanged.
#          (6) Badge WORDING unchanged (§2). Optional scan icons added: 📤 Upload /
#              🔁 Replace / 📁 Use locally.
#   v1.4 — 2026-07-07 — STEP 1 REGISTRY ADDITION.
#          Framework_PYQPrepare v1.0 now exists — Step 1 is no longer manual/external.
#          (1) Replaced NOTE ON STEP 1 exclusion block with full Step 1 registry entry
#              (Row file, F2 step-complete, "Use locally" badge, next = Step 2a).
#          (2) Added Row file pattern to LOCAL_ONLY in §2 badge logic.
#          (3) Added "After Step 1 → Step 2a" to §6 next-step reference table.
#   v1.3 — 2026-07-07 — AUTOMATED CROSS-CHECK (1 context-dependent badge bug fixed).
#          Custom Python audit script tested all 39 file×context combinations against
#          LOCAL_ONLY patterns. Found 1 conflict: analysis_progress.json was in LOCAL_ONLY
#          but Step 5 mid-step delivery needs Upload/Replace (for session resume). The
#          file has DUAL behavior: mid-step=project Files, final=local. Moved to a new
#          CONTEXT-DEPENDENT section in the pseudocode with explicit documentation.
#   v1.2 — 2026-07-07 — DEEP SOURCE-SPEC CROSS-CHECK (5 filename/deliverable bugs fixed).
#          Every step's deliverables verified line-by-line against its source spec.
#          (1) Step 7 per-batch filename: Mock[N]_Batch[B].docx → Mock[N]_Q1to[K].docx
#              (cumulative whole-paper, per Framework_MockTestCreate S4-10).
#          (2) Step 8 filename: Mock[N]_Rectified.docx → Mock[N]_Complete.docx
#              (same filename as Step 7 — replaces input, per MockTestCreateAudit S0-2).
#          (3) Step 8 missing conditional deliverable: Mock[N]_audit_changelog.md added
#              (delivered ONLY when ≥1 question regenerated, per S0-2).
#          (4) Step 9 per-batch: Mock[N]_Solutions_Batch[B].docx removed — spec delivers
#              the SAME Mock[N]_Solutions.docx each batch (whole-paper incremental, per
#              MockTestExplain S19-2 + RE-8). Mid-step and final = same file.
#          (5) §2 LOCAL_ONLY: fixed patterns to match actual filenames — removed
#              Rectified/Solutions_Batch (don't exist), added Q1to*/audit_changelog.
#   v1.1 — 2026-07-07 — EXHAUSTIVE AUDIT (12 bugs fixed).
#          (1) Step 6 B3: added mock_test_audit.py as 6th deliverable (Blueprint v1.20).
#          (2) Step 2b/5 first-batch badge: fixed "Replace" → dynamic Upload/Replace.
#          (3) Step 4: added count_progress.json session-break interim deliverable.
#          (4) Step 2c NEXT STEP: removed wrong "parallel" claim (Step 4 depends on Step 3).
#          (5) Step 3 NEXT STEP: removed nonsensical "(if not already done)" qualifier.
#          (6) §2 LOCAL_ONLY: added all mock paper file patterns.
#          (7) Step 1 PYQPrepare: added exclusion note.
#          (8) Step 5 final: analysis_progress.json + analysis_summary.md → Use locally
#              (per PYQAnalyse handoff: "KEEP LOCALLY").
#          (9) §5: added session-break edge case (F1 variant for forced context-limit breaks).
#          (10) §6 reference table: synced with §3 fixes.
#   v1.7 — 2026-07-25 — Step 2c registry: [ExamCode]_approval_record.json ADDED.
#          Mandated by PYQAnalyse S4-3/S10-1 since v2.17 and required at PYQSort entry
#          since v2.23, but absent from this registry — the word "approval_record"
#          did not appear anywhere in this spec. A deliverable missing from the
#          delivery contract is a deliverable that eventually stops being delivered.
#   v1.0 — 2026-07-07 — Initial release. Two footer types defined.
#          Per-step deliverable registry with action badges.
#          Decision logic for mid-step vs step-complete.

