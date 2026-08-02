# Framework_MockTestCreateAudit v2.21.6
# v2.21.6 — 2026-08-02 — MUTATION SCORE 100%. ZERO SURVIVORS. RATCHET AT 0.
#   The last seven untested findings closed in one release. Every finding
#   audit_canonical.py can emit is now provably detected by at least one fixture:
#   deleting ANY of the 27 finding emissions makes the self-test go red.
#
#   CLOSED IN THIS RELEASE:
#     A-NAT-GRADE (3) — fixtures 35/36 covered only the MISMATCH and the happy
#       path. Missing nat_value, missing nat_grading_value, and a re-derivation
#       that RAISES were all deletable with every test green. This gate guards the
#       exact string the delivery portal ingests to AUTO-GRADE a numerical
#       question, so a silent failure here is WRONG MARKS, not a wrong-looking
#       paper — the same severity class as the v2.21.3 A-OPTORDER anchor defect.
#       NOTE (reachability, discovered while writing 36a): an ENTIRELY EMPTY
#       answers map makes the whole gate dormant by design (Step 8 receives no key
#       unless --key is supplied), so the reachable defect is a PARTIAL sidecar —
#       answers present, this question's value absent. The fixture asserts that.
#     A-ZIP (2) — both failure modes untested: an rId with NO relationship entry,
#       and an rId whose relationship points at a part NOT IN THE ARCHIVE. A docx
#       failing either is structurally broken and images silently vanish in Word.
#       Both halves asserted plus the clean case, so neither can be "achieved" by
#       making the gate fire always.
#     A-SECCOUNT (1) — the gate proving each section holds the number of questions
#       its q_range declares had NO fixture at all. Matching-count guard included.
#     restore_checkpoint (1) — CK-tamper-refused covered a member whose CONTENT
#       changed (hash mismatch); a member LISTED IN THE MANIFEST BUT MISSING FROM
#       THE ARCHIVE had no fixture. A truncated bundle is the likelier real-world
#       corruption (interrupted upload/copy) and must be refused BEFORE anything is
#       written to disk, never resumed onto a half-restored evidence set.
#
#   Self-test 130 -> 136. Survivors 7 -> 0; score 74.1% -> 100%. §21 ratchet budget
#   LOWERED TO 0 — from this release the gate is absolute: ANY new finding that no
#   fixture can detect FAILS the build. No inherited backlog remains.
#
#   HONEST SCOPE. 100% mutation score means every finding EMISSION is covered. It
#   does NOT mean the gates are correct — a gate can be provably-fires-when-it-
#   should and still encode the wrong rule, which is exactly what the v2.21.3
#   (A-OPTORDER unanchored), v2.21.4 (A-FIGCOMP dead branch / partial sets) and
#   v2.21.5 (ND10 figural-NAT) defects were. Those were found by reading the
#   PRODUCER contract, not by mutation. Both controls are necessary; neither is
#   sufficient. AUTH_GATE_FLOOR stays 35. NO paper changes. NO Step-7 changes.
#
# v2.21.5 — 2026-08-02 — ND10 FIGURAL-NAT EXEMPTION WIRED INTO gate_images.
#   Caught in REVIEW, before deployment, by a reader checking the v2.21.4 change
#   against the PRODUCER contract rather than against its own fixtures.
#
#   Create.md R-FIGURAL v4.7 FIGURAL-NAT VARIANT (ND10): a figural question whose
#   subtopic is answer_type=='numerical' has a PROBLEM image (or SERIES images) but
#   ZERO option images — "there are no options to decompose" — and
#   G-FIGURAL-COMPOSITE "must skip its per-option-image arm" for it. ND10 says in
#   terms that without this variant "a valid figural-NAT would be hard-stopped for
#   missing option images".
#
#   gate_images had NEVER read the signal. v2.21.3 and earlier flagged a
#   SINGLE-image figural-NAT (the `len(block_imgs) == 1` arm) — a pre-existing false
#   positive. v2.21.4 tightened that arm to `< oc + 1` to catch partial option sets,
#   which WIDENED the same false positive to every 2..oc-image figural-NAT series.
#   It is a WARN, so no paper hard-stops, but it routes a human to "VIEW + fix in
#   Part B" a paper that is CORRECT — the most expensive kind of wrong answer an
#   auditor can give.
#
#   THE SIGNAL MUST BE options_by_q, NOT concept_map. The existing
#   nat_subtopic_ids mapping requires concept_map, and load_sources sets
#   concept_map = {} on any run WITHOUT a dossier or --key — its own comment says
#   "otherwise empty dict (gate_images falls back to default
#   image_role='stem_and_options')". So on a plain run the NAT mapping silently does
#   not fire and the figural-NAT lands in exactly the arm that was tightened.
#   options_by_q travels in the registry (ND6), which Step 8 ALWAYS receives, and is
#   the SAME signal gate_options has always read (obq[str(qnum)] == 0 -> skip).
#   gate_images now reads it too — one shared NAT signal, per S5-2 "ONE STRUCTURAL
#   QUESTION, ONE ANSWER".
#
#   SCOPE OF THE EXEMPTION: the per-OPTION-image arm only, in BOTH the
#   stem_and_options and options_only variants. ND10 still requires >=1 problem
#   image, so a figural-NAT rendering ZERO images REMAINS a finding (fixture 53j).
#
#   Fixtures 53i (BOTH halves: the SAME 3-image block is OK when the registry marks
#   it NAT and a FINDING when it does not — so the fix cannot be "achieved" by
#   disabling the arm) and 53j. Self-test 128 -> 130. gate_images stays at 100%
#   (7/7 killed). AUTH_GATE_FLOOR stays 35. NO paper changes. NO Step-7 changes.
#
# v2.21.4 — 2026-08-02 — A-FIGCOMP HAD A DEAD BRANCH AND ACCEPTED PARTIAL FIGURE SETS.
#   Found by working the audit_mutation.py backlog. gate_images carried SEVEN
#   surviving mutants — every finding it emits (multi_per_line, figtext_prose,
#   math_raster, warn_view, all three composite arms) could be DELETED OUTRIGHT with
#   all 120 fixtures still green. The gate owning A-FIGCOMP and A-MATHRASTER on every
#   figural paper in the estate had no fixture that could detect it going silent.
#   Probing that space surfaced TWO REAL DEFECTS. This is the third consecutive gate
#   where closing a coverage gap exposed a live bug.
#
#   DEFECT 1 — DEAD BRANCH. `if not block_imgs: ... continue` sits ABOVE the
#   stem_only arm, so `if len(block_imgs) < 1: composite.append('stem_only:0img')`
#   could NEVER be true. It was unreachable code. A REGISTRY-DECLARED FIGURAL
#   question that rendered ZERO images passed A-FIGCOMP clean — a figure that was
#   never drawn — UNLESS its stem happened to match the _fig_ref_re prose pattern.
#   Detection therefore depended on the WORDING OF THE STEM rather than on the
#   ABSENCE OF THE FIGURE. Fixed by testing the condition before the `continue`.
#   Membership is taken from the REGISTRY set only, NEVER from figural_cue_keywords:
#   that list contains ordinary MCQ phrases ('which of the', 'series', 'complete
#   the'), so applying it to zero-image blocks would false-FAIL a large share of
#   ordinary TEXT questions estate-wide. Fixture 53f locks both halves.
#
#   DEFECT 2 — PARTIAL FIGURE SETS ACCEPTED. Step-7 G-FIGURAL-COMPOSITE requires,
#   for stem_and_options, "problem image + one separate image per option" (oc+1
#   images). The check was `if len(block_imgs) == 1`, so a block rendering 2, 3 or 4
#   images — a problem figure with its OPTION FIGURES SILENTLY UNDRAWN — passed
#   A-FIGCOMP clean. Only the degenerate 1-image case was caught. A candidate cannot
#   answer a question whose option figures were never rendered. Fixed to
#   `len(block_imgs) < oc + 1`, with the count reported in the finding. Verified on
#   the real 60-question IIT_JAM_BIOTECHNOLOGY paper (57 drawings): the flagged
#   question set is IDENTICAL before and after — only the diagnostic detail is
#   richer. Fixture 53g locks it; 53a guards the canonical set staying clean.
#
#   Fixtures 53a-53h added. gate_images now scores 100% (7/7 killed). Self-test
#   120 -> 128 (-> 130 in v2.21.5). Engine-wide survivors 14 -> 7, score 48.1% -> 74.1%; §21 ratchet
#   budget LOWERED to 7. THREE gates now at 100%: gate_dossier, gate_options,
#   gate_images. AUTH_GATE_FLOOR stays 35. NO paper changes. NO Step-7 changes.
#
# v2.21.3 — 2026-08-02 — A-OPTORDER DID NOT ENFORCE ITS OWN DOCUMENTED CONTRACT.
#   Found by working the audit_mutation.py backlog: gate_options was carrying TWO
#   surviving mutants (bad_lab, bad_ord), meaning A-OPTLABEL and A-OPTORDER — which
#   police option labelling on EVERY question of EVERY paper in the estate — had no
#   fixture that could detect them going silent. Only A-OPTN and A-OPTUNIQUE were
#   covered. Probing the uncovered space to write those fixtures surfaced a REAL
#   DEFECT, which is the point of the exercise.
#
#   THE DEFECT. This gate's S5-2 row has always read "options appear in document
#   order 1..OPTIONS_COUNT". The check was
#       if 0 in idxs or idxs != list(range(idxs[0], idxs[0] + oc))
#   which accepts ANY CONSECUTIVE RUN. A block labelled 2,3,4,5 passed A-OPTORDER
#   *and* A-OPTLABEL and certified CLEAN. The engine was weaker than its own
#   documented contract, and nothing compared the two.
#
#   IT IS NOT COSMETIC. A-KINT derives the key as an int in 1..OPTIONS_COUNT. On a
#   paper labelled 2,3,4,5 the key "option 1" refers to an option that DOES NOT
#   EXIST, and keys 2..oc each point one place off — EVERY ANSWER FOR THAT QUESTION
#   IS WRONG on the delivered paper, with no gate objecting. A zero-start set
#   (0,1,2,3) was caught only incidentally, by the separate `0 in idxs` clause.
#
#   FIX: idxs != list(range(1, oc + 1)) — anchored at 1, not merely consecutive.
#   _idx_of() normalises all three label families to 1-based (num 1.., alpha a=1..,
#   roman i=1..), so the anchor is family-agnostic and no legitimate
#   option_label_format starts anywhere else. Verified on the real 60-question
#   IIT_JAM_BIOTECHNOLOGY paper: all four option gates unmoved.
#
#   Fixtures 4a-4e added (mixed family, family-vs-format mismatch, out-of-order,
#   the ANCHOR LOCK, and a three-family canonical guard so the fix cannot be
#   "achieved" by rejecting everything). gate_options now scores 100% (4/4 killed).
#   Self-test 115 -> 120. Engine-wide survivors 16 -> 14, score 40.7% -> 48.1%;
#   §21 ratchet budget LOWERED to 14. AUTH_GATE_FLOOR stays 35. NO paper changes.
#
# v2.21.2 — 2026-08-02 — MUTATION TESTING MADE MECHANICAL; 3 HOLLOW BRANCHES CLOSED.
#   Answer to "is there a more robust way to prove these two Steps are in sync?"
#   YES, and reading the code is not it. Eight times this corpus has shipped a code
#   path no fixture exercises, and every one was found by a human reading code AFTER
#   it shipped. A green self-test is exactly what a hollow branch looks like.
#
#   audit_mutation.py (new, untracked tooling) neutralises each finding emission in
#   audit_canonical.py one at a time and re-runs --self-test. A mutant that SURVIVES
#   means NO fixture can tell the difference between a gate that reports that defect
#   and a gate that does not. First run: 19 of 27 findings SURVIVED — a mutation
#   score of 29.6%. Three were in A-DOSSIER itself, the gate v2.21 had just been
#   rewritten to fix: the two set-mismatch legs (absent-from-dossier / not-in-paper)
#   and the ENTIRE subtopic_id-vs-registry leg had NEVER been executed by any
#   fixture. Half of the Tier-A cross-check was unverified while the release that
#   touched it reported 112/112 green.
#
#   Fixtures 92g/92h/92i close all three; gate_dossier is at a 100% mutation
#   score (5/5 killed). Self-test 112 -> 115. Engine-wide: 16 survivors remain,
#   score 40.7%, all inherited and all itemised in §21.
#
#   RATCHET POLICY (§21): the survivor count MUST NOT INCREASE release over release.
#   A new gate ships with fixtures that kill its own mutants, or it does not ship.
#   The 16 inherited survivors retire one release at a time by lowering the budget.
#   This is the first control in this corpus that detects a hollow branch WITHOUT
#   anyone suspecting it is there.
#
#   AUTH_GATE_FLOOR stays 35. NO paper changes. NO Step-7 changes.
#
# v2.21.1 — 2026-08-02 — NAT LEG RE-GROUNDED IN R13; A-FIGTEXT-PROSE DOCUMENTED.
#   Follow-up to GAP-2026-08-02-DOSSIER-OPTION-PREDICATE, found by a line-by-line
#   Step-7/Step-8 sync audit of THIS release.
#
#   v2.21 clamped the A-DOSSIER `nat` leg to fire only on a COMPLETE rendered option
#   set (n_opt >= oc), on the ASSUMPTION that a NAT stem may legitimately enumerate
#   ("Consider the following statements: 1. ... 2. ..."). IT MAY NOT.
#   Framework_MockTestCreate.md R13 (v4.7 NAT EXEMPTION) states that a NAT question
#   has ZERO option paragraphs — "only the bold Q.<N> stem (carrying the
#   nat_instruction per R14) and the blank separator". R13 admits no third paragraph
#   class, so an "enumerated stem" on a NAT block is an R13 VIOLATION, not a
#   legitimate shape.
#
#   THE ASSUMPTION WAS NEVER CHECKED AGAINST THE PRODUCER SPEC — the exact error
#   class v2.21 exists to remove (a belief about a sibling contract, held without
#   verifying it), committed by v2.21's own author while fixing that very class.
#
#   IT OPENED A REAL FALSE NEGATIVE. With nat_present=False and the registry marking
#   the question 0-option, gate_options SKIPS the block (obq == 0), gate_nat is
#   DORMANT (nat_present false), and the clamped A-DOSSIER was silent too — so an
#   R13 violation passed ALL THREE gates. v2.20 caught it. That configuration is
#   precisely a Step-7 INTERNAL INCONSISTENCY between blueprint and registry, which
#   is the one condition A-DOSSIER exists to detect. FIX: the nat leg fires on ANY
#   non-zero rendered count. NEVER clamp it. Fixture 92f is inverted accordingly and
#   now locks the false negative (a PARTIAL stray-label set on a claimed-NAT block IS
#   a finding, exactly as a complete one is under 92c).
#
#   ALSO: A-FIGTEXT-PROSE (v2.4, gate_images) is a LIVE roster gate that can _fail()
#   and block certification, and it had NO catalogue row, NO sub-code entry and NO
#   glossary line anywhere in this spec — the identical documentation gap that left
#   an operator with nothing to read when A-DOSSIER FAILed. Now documented in S5-2
#   and §16, mapped to its Step-7 twin G-FIGTEXT-PROSE (Create.md Tier 3).
#
#   Self-test 112 -> 115 in v2.21.2. AUTH_GATE_FLOOR stays 35. NO paper changes.
#
# v2.21 — 2026-08-02 — A-DOSSIER COULD NOT SEE AN IMAGE OPTION.
#   GAP-2026-08-02-DOSSIER-OPTION-PREDICATE. Raised by a live Step-8 TestCreateAudit
#   P1 run that HALTED PERMANENTLY with nothing on the paper to repair.
#
#   block_option_count() was built on OPT_RE, which requires a VISIBLE GLYPH after
#   the option label (`[.)]\s+\S`). An IMAGE option is a BARE label paragraph ('1.')
#   followed by a picture paragraph — the glyph IS the picture — so OPT_RE counted
#   every image option as ZERO. A-DOSSIER therefore FAILed `qtype-mcq-but-0!=N-options`
#   on every figural question in the estate, blocking certification under MANDATE D
#   while A-OPTN, A-OPTORDER, A-OPTUNIQUE and A-NAT-NOOPT all passed on the SAME
#   blocks. Two gates, one block, contradictory verdicts — that contradiction WAS the
#   defect. Its docstring asserted parity with "the same OPT_RE the option gates use";
#   the option gates do not use OPT_RE at all, they use OPT_LABEL_RE via
#   _label_paras(). The docstring encoded a BELIEF about a sibling function rather
#   than a verified fact about it, and no fixture ever compared the two.
#
#   NOT FIGURAL-ONLY. block_option_count() also had no trailing-set clamp, while
#   gate_options() takes the TRAILING oc labels precisely so an enumerated stem
#   cannot inflate the count. So every STATEMENT / SEQUENCE / MATCH /
#   ASSERTION_REASON stem that renders an enumerated list — a standard construction
#   on PURE TEXT papers — false-FAILed A-DOSSIER too.
#
#   AND IT PRODUCED A FALSE PASS. Because the same zero vacuously satisfied
#   `if qt == 'nat' and n_opt:`, a question the dossier records as NAT that actually
#   SHIPS four image options was ACCEPTED SILENTLY. The gate that exists to detect
#   "Step 7 recorded something other than what it shipped" was BLIND to that exact
#   condition for every figural question. One predicate, a false FAIL and a false
#   PASS.
#
#   FIX: block_option_count(b, oc) delegates to the option gates' OWN predicate
#   (_label_paras) and their OWN trailing-oc clamp. ONE shared rendered-option
#   count; a second implementation is drift by construction. The nat leg now fires
#   only on a COMPLETE rendered set (n_opt >= oc), so a legitimate NAT question
#   whose STEM enumerates is not a finding and A-DOSSIER is never more opinionated
#   than A-NAT-NOOPT, which OWNS that fact.
#
#   FIXTURE 92 WAS A TAUTOLOGY. It asserted
#     block_option_count(b) == sum(1 for p in b.paras if OPT_RE.match(para_text(p)))
#   — the right-hand side is a verbatim re-implementation of the left-hand side's
#   body, so it CANNOT FAIL FOR ANY PREDICATE. It reported green across v2.17-v2.20
#   on a build whose dossier gate could not see a single image option. RETIRED and
#   replaced by six fixtures: 92a-92d + 92f MUTATION-VERIFIED (measured False on the
#   OPT_RE build, True on this one) and 92e a permissiveness GUARD. Every dossier
#   fixture before this release was built from _add_q(), which emits text options
#   only — no dossier fixture had EVER rendered a non-text option. This is the
#   SEVENTH hollow-branch occurrence this corpus has recorded; the counter-measure is
#   structural, not vigilance: CHECK AN (shared-predicate parity) and CHECK AO
#   (tautological-fixture detector) now fail the build mechanically.
#
#   Self-test 107 -> 112. AUTH_GATE_FLOOR STAYS AT 35 — raising it would hard-stop
#   every un-refreshed exam and convert a coverage fix into an estate-wide outage.
#   NO PAPER CHANGES. Papers produced by Step 7 v5.35+ are correct; they were only
#   mis-audited. Step 7 requires NO change — qtype derivation and the dossier writer
#   were both verified correct.
#
# v2.20 — 2026-08-01 — ONE THIRD OF THE DOSSIER IDENTITY TRIPLE WAS NEVER CHECKED.
#   GAP-2026-08-01-DEAD-PARAMETER. Found by a line-by-line producer/consumer audit
#   of Steps 7 and 8, running the edge-case matrix rather than reading it.
#
#   load_dossier() has accepted an `exam` argument since v2.17, and S0-1 item 7b
#   documents the identity binding as exam_code / mock / paper_md5. The call site in
#   load_sources() passed docx_path and mockN and NEVER passed exam — so the
#   exam_code leg never executed and a dossier built for ANOTHER EXAM was ACCEPTED.
#   Verified empirically: the wrong-exam case returned 60 questions before v2.20 and
#   is REFUSED after.
#
#   SEVERITY, STATED HONESTLY: unreachable in practice, because paper_md5 is checked
#   and a different exam's paper cannot share this paper's hash — a wrong-exam
#   dossier would have been caught by the md5 leg. This was defence-in-depth with one
#   layer unwired, not an open door. But a documented binding that never executes is
#   the same dead-parameter class this corpus keeps rediscovering (v2.10 `bc` bound
#   nowhere, v2.13 Block.images never populated, v2.17 --dossier never passed), and
#   the whole point of a triple is that no single leg is load-bearing alone.
#
#   FIX: load_sources() passes exam=blueprint.exam_code (the authority P2 already
#   asserts equals the trigger, RS-5). Fixture 90 now checks BOTH that the leg
#   refuses a wrong exam AND that load_sources actually supplies it — because a
#   working check nobody calls is not a check, which is precisely how this defect
#   and the v2.17 --dossier defect both survived.
#
#   FULL EDGE-CASE MATRIX RE-VERIFIED (10/10): happy path ACCEPTED; paper
#   regenerated, wrong mock, wrong exam, future schema, smuggled judgment key, empty
#   questions, truncated file, and absent md5 binding all REFUSED with a named
#   reason; absent dossier degrades to the legacy WARN and the audit continues.
#
# v2.19 — 2026-08-01 — THE DOSSIER WAS DELIVERED, STAGED, AND NEVER READ.
#   GAP-2026-08-01-FLAG-NOT-INVOKED. v2.17 declared the Tier-A dossier as a
#   delivered input (S0-1 item 7b) and audit_canonical.py grew a --dossier flag to
#   consume it. NO DOCUMENTED INVOCATION PASSED THE FLAG. S5-1 and the Phase-3
#   command both omitted it, and P0 never staged the file at all. Step 7 would write
#   the dossier, the author would upload it, and the auditor would ignore it — every
#   benefit silently lost while every gate reported clean: A-NAT-GRADE dormant,
#   image_role defaulted, A-FIGCOMP reporting 27 findings where 7 are real.
#
#   THIS IS THE EXACT DEFECT THE DOSSIER EXISTS TO REPAIR, ONE LAYER UP. The original
#   finding was: Step 7 writes concept_map, audit_canonical.py has a --key consumer,
#   and nothing connects them. v2.17 fixed that and immediately recreated it — spec
#   declares the input, engine exposes the flag, no invocation wires them. Two
#   further releases shipped on top before the disconnect was noticed, and it was
#   noticed only because someone asked what "--dossier" meant.
#
#   THE FIX: P0 stages the dossier when present (and prints which branch it took);
#   S5-1 and the Phase-3 invocation both pass --dossier when P0 staged one; and
#   validate_framework_md CHECK AM now fails the build whenever a spec declares an
#   input, an engine exposes a flag for it, and no documented invocation passes it.
#   A wiring instruction written only in prose is not wiring — this corpus has now
#   proved that three times, and the third time it cost two releases.
#
#   OPERATOR SIGNAL: A-DOSSIER prints its consumed/not-consumed verdict on EVERY
#   run. If it says "no Tier-A dossier consumed" while the file exists in
#   /home/claude, the invocation is wrong. Fix it and re-run.
#
# v2.18 — 2026-08-01 — D1 (MANDATE 0 MADE IMPLEMENTABLE) + D3 (ENGINE API CONTRACT)
#   + D8 (EC-V18 PRE-FLIGHT NOTICE). Three defects CERTAIN to recur on the next run.
#   No gate semantics change; nothing about coverage changes.
#
#   D1 — MANDATE 0 WAS UNIMPLEMENTABLE, AND AN OPERATOR HAD ALREADY IMPROVISED A
#   WAIVER. Inherited verbatim from Step 7, where it is trivially satisfiable
#   because Step 7 GENERATES content and never reads it back. Step 8 must read it
#   back (§6 S6-0, S11-1), and on every rendering surface each tool result enters the
#   visible transcript — so READING IS PRINTING. Step 8 could neither run Part B
#   lawfully nor satisfy the mandate while running it. On a live audit the operator
#   asked the author to waive MANDATE 0; that waiver had NO BASIS IN THIS SPEC. The
#   contradiction is now resolved instead of waived: MANDATE 0 governs AUTHORED
#   PROSE, not spec-directed reads — the same distinction SKILL.md Rule 5 already
#   draws for in-protocol vision. The rule that actually protects the exam is
#   unchanged and absolute: Claude NEVER RESTATES content in its own prose, findings,
#   dashboards or reports. Reads must be minimal-surface, incidental leakage from
#   diagnostic code remains a VIOLATION, and P0 emits a one-time SURFACE NOTICE so
#   the author knows the session log will contain content.
#
#   D3 — APPENDIX B, INTROSPECTED NOT TRANSCRIBED. The spec orders the operator to
#   call engines whose signatures it never stated, while SKILL.md forbids reading a
#   .py into context: no sanctioned discovery path existed. Two mis-calls on a live
#   run cost two turns and produced a wrong finding. Appendix B now carries every
#   signature, argument PROVENANCE, return type and unstated precondition.
#   NOTE: it also CORRECTS a claim in the circulating gap report — an unconstrained
#   profile returns 'SKIP', not 'FAIL' (verified by introspection and source).
#   Documenting the report's version would have enshrined a false precondition.
#
#   ALSO CORRECTED: the S5-2 A-FIGPROFILE row named batch_state.figural_qs[n].
#   object_type as its input. batch_state.json is a Step-7 internal sidecar that S0-1
#   explicitly does NOT deliver; the auditor has always read registry
#   figural_manifests[].object_types. The stale row sent an operator hunting for a
#   file Step 8 can never have.
#
#   D8 — P4 now emits the EC-V18 notice BEFORE Phase 1: a paper with 0 FigureSpec
#   sidecars is destined for an AMBER footer and a permanent §R13 limitation however
#   well the audit goes, and the author deserves to know that before committing hours
#   rather than discovering it mid-audit. Partial coverage reports a RATIO and
#   degrades per figure, never per paper.
#
# v2.17 — 2026-08-01 — D7 (NO SILENT TRUNCATION) + TIER A (THE STEP-7 DOSSIER)
#   (SESSION-EXHAUSTION programme, release 4). Two changes to the SAME gate surface,
#   shipped together on purpose: fixing truncation alone would have raised
#   A-FIGCOMP from 12 visible findings to 27 — more honest but more alarming — when
#   the true cause was a missing image_role that Tier A supplies. Together the
#   diagnostics become honest AND correct: 27 -> 7 on the reference paper.
#
#   D7 — Gates printed `' '.join(sorted(set(x))[:12])`. On a real 60-Q paper
#   A-FIGCOMP had 27 findings and printed 12; the other 15 vanished with no trace,
#   in lexicographic order (Q3 after Q28). A reviewer reasonably concluded the gate
#   was non-deterministic and filed it as unreproducible. It was under-reporting, in
#   numeric-blind order. 41 truncation sites are now rendered by _flist(), which
#   sorts numerically and always states the total and any suppression.
#
#   TIER A. Step 7 already records every fact Step 8 was re-deriving, and
#   Framework_MockTestCreate.md says of concept_map: "The audit gates read it
#   directly instead of re-deriving." audit_canonical.py has carried the consumer
#   path since v2.4. S0-1 simply never delivered the sidecar — producer written,
#   consumer written, pipeline never connected. Measured: 0 of 60 concept_map
#   entries reached Step 8; A-NAT-GRADE dormant on ~200 exams; image_role defaulted
#   everywhere. The dossier repairs that channel under one line — HAND OVER FACTS,
#   NEVER JUDGMENTS — with judgment keys refused at load, identity bound to the
#   paper MD5, every fact cross-checked against the SHIPPED PAPER by A-DOSSIER, and
#   NO GATE PASSING ON DOSSIER EVIDENCE ALONE.
#
#   TWO DEFECTS IN THIS RELEASE'S OWN FIRST CUT, both found by RUNNING it:
#     • gate_dossier read `b.opts` — a field that DOES NOT EXIST on Block. getattr()
#       returned None, every mcq cross-check compared 0 against OPTIONS_COUNT, and
#       27 false failures were reported. Identical class to Block.images
#       '# reserved' (v2.13). block_option_count() now counts from the document.
#     • A-NAT-GRADE's dormancy test read `not concept_map`. The moment Tier A
#       populated it, the gate woke with no answers and FAILED every NAT question.
#       It now tests `not answers`, which is the honest condition, and goes live
#       only with the sealed key channel.
#
#   Self-test 97 -> 105. Eight guarantees mutation-verified; the A-NAT-GRADE
#   regression was found UNCOVERED by mutation testing and fixture 93 closes it.
#
# v2.16 — 2026-08-01 — D2 + D4: VISION IS A DECLARED, PROBED, DEGRADABLE DEPENDENCY
#   (SESSION-EXHAUSTION programme, release 3 of 4+). THIS IS THE DEFECT THAT ACTUALLY
#   HALTED A REAL AUDIT. Coverage is unchanged for every healthy run.
#
#   WHAT HAPPENED. On a live 60-Q paper the view() path failed mid-session. 43 images
#   across 27 figural questions became un-stampable; S5-1A C6/C7 could therefore never
#   pass; MANDATE D forbade delivery; and the spec defined NO state for "vision
#   unavailable". The audit was permanently STUCK — not degraded, not reported, stuck.
#   16 of 60 questions had been fully certified over two days and none of it could ship.
#
#   WHY THAT WAS WRONG BY THIS FRAMEWORK'S OWN DOCTRINE. §5 states "NO DEPENDENCY
#   CONDITION MAY EVER HALT A RUN", and CLAUDE.md states "Silence is the defect; a halt
#   is not the remedy." Graceful degradation was granted to blueprint_core, to
#   figural_core, to all twelve figure gates and to every colour condition — and denied
#   to the one dependency whose absence is fatal. RA-4 was doing TWO jobs with one rule:
#   blocking a LAZY OPERATOR (right) and blocking an ENVIRONMENT OUTAGE (wrong).
#
#   D2 — A THIRD STAMP STATE, AND IT IS UNFAKEABLE. 'view-unavailable' joins
#   'rendered-and-viewed' and (absent). The obvious danger is that "I could not see it"
#   is exactly what a lazy operator would claim, so the state is NEVER assertable by
#   choice: C6 admits it only when session_log.vision_probe carries a FAILED record for
#   that batch AND the montage exists at >= EVIDENCE_MIN_BYTES. C6 also FAILS when
#   vision has RECOVERED and the stamps were not upgraded — a paper that COULD have
#   been fully audited must not certify degraded. A degraded run prints
#   COMPLETION-GATE: DEGRADED (vision), exits 0, and ships under an F1 AMBER footer
#   with a §R13 limitation. Identical treatment to EC-V18 legacy figures, which ~200
#   exams already deliver under: machine-checked but not eyeballed, disclosed loudly,
#   and strictly better than no paper at all.
#
#   D4 — P3.5 VISION PROBE. Vision was ambient; now it is declared. The probe renders
#   three RANDOM glyphs and stores only a SALTED SHA-256 of them, so reading the
#   sidecar reveals nothing and reporting the glyphs requires actually seeing the card.
#   That is what turns vision from an operator claim into a MEASURED fact — the whole
#   D2 safety argument rests on it. It runs at pre-flight AND at the start of every
#   Phase-2 batch, because the incident had Batch 1 healthy and Batch 2 not: a
#   start-of-session probe alone would have missed it. A probe RENDER failure is an
#   ENVIRONMENT WARN and explicitly NOT a vision verdict (E4.5).
#
#   NOT TOUCHED: tables/matrices/charts/OMML are arithmetic, not vision (E2.7), and
#   remain fully authoritative. A missing or trivial montage is still un-audited and
#   still blocks (E2.5/E2.6). A key that cannot be derived without sight is a VOID_ITEM
#   (E2.8), never silently keyed. RA-3, RA-15a, MANDATE B and every healthy-run verdict
#   are byte-identical to v2.15.
#
#   Self-test 89 -> 97. Six guarantees mutation-verified. NO FIXTURE HAD EVER SIMULATED
#   A VISION OUTAGE — the fifth appearance of the hollow-branch class (v2.10 bc binding,
#   v2.12 A-FIGPROFILE, v2.13 Block.images, v2.15 unknown-schema, now this).
#
# v2.15 — 2026-08-01 — C1: AN AUDIT CAN NOW SURVIVE A SESSION BOUNDARY
#   (SESSION-EXHAUSTION programme, release 2 of 4). Coverage UNCHANGED.
#
#   THE DEFECT, AND WHY IT WAS THE REAL ONE. RA-18 declared Step 8 "resume-safe"
#   and stored every piece of cross-batch state — ledger, batch plan, WIP docx and
#   the ENTIRE evidence tree — under /home/claude. That directory does not survive
#   a session boundary. So resume worked inside one session and not at all across
#   one, and the failure mode was fatal rather than degraded: S5-1A C5/C6 assert
#   that every stamped evidence file EXISTS, so once the montages and saved fact
#   records were gone, a perfectly remembered ledger could NEVER certify. A
#   session that exhausted mid-Phase-2 therefore lost the whole audit, and the
#   retry exhausted the same way. That LOOP — not any individual gate — is why
#   this step kept failing on paper after paper. B3 (v2.14) made exhaustion much
#   less likely; C1 makes it survivable, which is the difference between a step
#   that usually works and one that cannot lose your work.
#
#   THE FIX. At the end of Phase 1 and of every Phase-2 batch, Step 8 writes
#   [ExamCode]_M[N]_audit_checkpoint.zip — audit_state.json + the WHOLE evidence
#   tree + the WIP docx — to the SAME filename each time, so there is exactly one
#   current bundle. On `resume`, P0.5C verifies and rehydrates the uploaded
#   bundle before any batch runs, rebasing evidence_dir AND every recorded
#   evidence path in the ledger (the previous container's absolute paths are
#   gone, and C5/C6 resolve through them). Neither build nor restore is prose:
#   both are commands in audit_canonical.py (--make-checkpoint /
#   --restore-checkpoint), per §21's rule that only code certifies.
#
#   BINDING IS THE SAFETY ARGUMENT. Restore REFUSES on an unknown schema, an
#   absent/unparseable manifest, ANY member whose sha256 differs, or an
#   exam_code / mock / paper-MD5 disagreeing with the paper in hand — and writes
#   NOTHING when it refuses, because a half-unpacked checkpoint is the worst
#   outcome of all: it looks resumable. The paper binding matters most: a
#   checkpoint restored onto a DIFFERENT document would let Step 8 certify an
#   audit nobody performed on it, which is strictly worse than losing the audit.
#
#   MANDATE D GAINS ONE EXPLICIT CARVE-OUT. The checkpoint is handed to the author
#   before certification and that is not a breach: MANDATE D forbids shipping an
#   uncertified PAPER, and the checkpoint is not a product but opaque resume state
#   containing no certified artefact. The certification delivery remains exactly
#   ONE present_files of the closed set, and S14-2 now CLEARS any checkpoint from
#   outputs and asserts (check 7) that none survives into the delivered set.
#
#   Self-test 78 -> 88. Seven guarantees mutation-verified. The unknown-schema
#   guard was found UNCOVERED by mutation testing — it could be deleted with every
#   other fixture still green, the same hollow-branch class this corpus has now
#   rediscovered three times; fixture 76b closes it.
#
# v2.14 — 2026-08-01 — B3: FACT VERIFICATION KEEPS ITS EVIDENCE, NOT ITS TRANSCRIPT
#   (SESSION-EXHAUSTION programme, release 1 of 4). Coverage is UNCHANGED. What
#   changes is where the raw search result lives.
#
#   THE PROBLEM, MEASURED. Step 8 was exhausting its session before Phase 3 on
#   ordinary papers, which is worse than it sounds: the evidence dir lives in
#   /home/claude and does NOT survive a session boundary, so an exhausted run
#   loses the whole audit and the retry exhausts the same way. On a 60-question
#   science paper the load is:
#     spec reads .............................. ~82k tokens
#     Part A STDOUT x 9 runs .................. ~11k
#     33 per-question montages ................ ~46k
#     B-FACT ................................. ~400k+
#   B-FACT dominates everything else combined. §6 S6-3 requires the keyed fact AND
#   every option to be web-verified; on ~25 C-FACTUAL questions that is ~125
#   searches, and retaining each full result set is what actually ends the session.
#
#   THE FIX (RA-11 a/b/c). (a) SAVE-THEN-SHED — the raw result goes to
#   evidence/facts/ and ONE verdict line ("q17 · VERIFIED · <domain> · <date>")
#   is carried forward. (b) CACHE BY CONCEPT — ledger.fact_cache is consulted
#   before any search, so a claim shared by several questions is verified once and
#   reused by path. (c) GROUP THE OPTIONS — where the options are same-domain, one
#   query may settle the set and the saved file holds a LIST of per-option records;
#   per-option queries remain wherever the grouped result leaves an option open.
#   S6-2 now carries the canonical save_fact()/fact_line() writers so the record
#   shape cannot drift from what the gate asserts.
#
#   AND THE GATE MOVES WITH IT — this is the part that makes B3 safe. C5 checked
#   only that the saved file EXISTED and was >= 1 byte. That was tolerable while
#   the full result ALSO sat in the reasoning stream, because the evidence was
#   duplicated. It is not tolerable once the file is the ONLY copy: without a
#   shape check the discipline degrades silently from "save the result" to "touch
#   a file", and C5 would certify an audit whose evidence no longer exists
#   anywhere. C5 now requires the file to PARSE and to carry a non-blank query +
#   url + retrieved_at + snippet in every record — exactly the four fields RA-11
#   has mandated since v2.6 and that no gate had ever checked. It also accepts one
#   file referenced by many questions and REPORTS the reuse, so the cache reads as
#   reuse and never as a coverage shortfall.
#
#   WHAT B3 DOES NOT TOUCH: which facts are checked (all of them), that the check
#   is LIVE, that it is per-option, that it is evidence-backed, or any of RA-0 /
#   RA-3 / RA-15a / MANDATE B. No preference may waive coverage and none is
#   waived here. Self-test 73 -> 78; all five new behaviours mutation-verified.
#
# v2.13 — 2026-08-01 — THE TWELVE FIGURE GATES ACTUALLY EVALUATE FIGURES
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT, D1-D6). v2.12 rescued these gates from a
#   permanent halt and left them VACUOUS. On every paper, in every exam, from
#   v2.11 through v2.12.1, all twelve printed "0 figure(s) conform."
#
#   WHAT WAS WRONG. TWO independent breaks, either one sufficient:
#     D1 — `Block.images` was declared `# reserved` at v1.0 and appended to
#          NOWHERE in the 2,484-line auditor. The twelve gates iterate
#          `blk.images`, so `_seen` was 0 on every run and every gate passed
#          vacuously. A paper with 57 drawings was audited as though it had none.
#     D2 — `src['figure_specs']` was READ at the gate site and WRITTEN nowhere,
#          and structurally could not be written: `write_spec_sidecar()` drops
#          `q{N}_*.figspec.json` beside each PNG in the STEP-7 session's working
#          directory, which is internal and never delivered (S0-1). There was no
#          transport channel at all, so even genuine v5.33+ output would read as
#          legacy for ever and EC-V18 would downgrade every BLOCKING verdict.
#
#   WHY NO GATE SAW IT. No fixture had ever put an IMAGE IN A BLOCK. All 61
#   self-tests ran on image-free documents, so `Block.images` being empty was
#   indistinguishable from correct behaviour and 61/61 PASS again coexisted with
#   zero real coverage. This is the SAME hollow-branch class as v2.12's own
#   defect — v2.12 closed it for A-FIGPROFILE and left it open one gate-family
#   over. It also contradicted this file's own doctrine: v2.12 wrote "0/0 is NOT
#   evidence of conformance (edge case 6)" for A-FIGPROFILE while twelve gates
#   printed OK on zero evaluated figures.
#
#   SIX CHANGES:
#   1. D1 — `attach_block_images()` populates `Block.images` before any gate
#      runs, fed by `extract_media()` (media parts out of the ZIP onto disk,
#      never raises) and `para_images_ext()` (walks each <w:drawing> as a UNIT,
#      so a drawing's alt text cannot be attributed to its neighbour — A-FIGALT
#      reads @descr). Table-cell paragraphs are included: a DI chart or a
#      figure/option fusion table puts drawings in cells, and a block-level
#      paragraph scan misses every one. `para_images()` is byte-unchanged.
#   2. D2 — TRANSPORT. Step 7 v5.34 carries the FigureSpec records into
#      `registry.figural_manifests[].figure_specs`, keyed by the canonical PNG
#      name S10-8 already stamps on the drawing. The registry is the sanctioned
#      channel — the precedent object_types/subtopic_ids set at v5.31, and for
#      the identical reason: Step 8 receives the registry and receives no
#      sidecar. `resolve_figure_spec()` resolves by docPr name, then the
#      extension-stripped form, then the media part name (so a CP-IMGNAME rename
#      still resolves). Unresolved returns {} => legacy => EC-V18, which is the
#      correct degradation and never a fabricated verdict.
#   3. D3 — 0 EVALUATED IS NOT EVIDENCE. Drawings present but unreadable => WARN
#      "conformance NOT ESTABLISHED"; no drawings at all => OK "dormant"; never
#      a vacuous "conform". Edge case 6, applied where it was missing. The
#      duplicate SECOND A-FIGDPI line the old EC-V18 note emitted is folded into
#      each gate's single verdict — it was unreachable while _seen was 0 and
#      would have broken v2.12's roster-count integrity signal the moment
#      figures were actually evaluated.
#   4. EC-V18 IS A DELIVERY TOLERANCE, NOT ONLY A SEVERITY RELABEL — see below.
#   5. D4 — TWELVE NEW FIXTURES (61 -> 73), every one mutation-verified to fail
#      on the specific break it locks. Includes fixture 63, which runs the REAL
#      `run_audit()` end to end: fixtures that call `attach_block_images()`
#      directly all still pass if the CALL is deleted, which is precisely the
#      v2.10 shape (written at the call sites, bound nowhere).
#   6. D6 — the §13 re-sync CARRIES FORWARD the figural manifest's audit
#      metadata instead of discarding it (see S13-2).
#
#   EC-V18 IS A DELIVERY TOLERANCE. Making the gates non-vacuous surfaced a
#   conflict between two clauses that could not collide while _seen was always
#   0: AMBER is defined as FAIL severity, and EC-V18 is defined as
#   NON-NEGOTIABLE that ~200 existing exams "keep auditing AND DELIVERING
#   untouched". A _fail() exits non-zero and MANDATE D requires exit 0 to
#   certify, so emitting FAIL for a LEGACY-ONLY finding would have converted a
#   coverage fix into an estate-wide delivery outage the moment it landed — the
#   same trap AUTH_GATE_FLOOR exists to avoid. Resolution, in EC-V18's
#   direction because EC-V18 is the clause that speaks to delivery:
#     • every finding on a figure with NO sidecar (pre-v5.33) => WARN, LOUD,
#       amber footer applies, recorded as a §R13 limitation, delivery NOT
#       blocked. Step 8 cannot retro-fit a sidecar onto an already-rendered
#       paper, which is exactly the "genuinely-not-fixable diagnostic" S5-4
#       already admits as an ACCEPTED WARN.
#     • any finding on a figure that DOES carry a sidecar (v5.33+/v5.34 output)
#       => FAIL exactly as before. A renderer-contract regression on output that
#       was supposed to conform is fixable, and it blocks certification.
#   Nothing becomes silent, nothing halts, and no existing exam stops shipping.
#
# v2.12.1 — 2026-08-01 — ENGINES COME FROM THE VERIFIED CLONE, NOT FROM THE PROJECT
#   (post-deploy correction to v2.12). v2.12 fixed the NameError but chose the wrong
#   DISTRIBUTION remedy: it added both engines to the Step-6 B3 output set, which
#   would have required uploading them to ~200 exam projects. CLAUDE.md states the
#   opposite rule, and states it correctly: engines live ONLY in the central repo,
#   `/mnt/project` is DATA and never an import source, and "no per-project engine
#   provisioning is required, and none should be performed."
#
#   WHY THE EXCEPTION LOOKED REAL. CLAUDE.md's reasoning is that Step 0 does
#   `cd "$FW"`, so a bare import resolves in the clone. That is TRUE for every
#   engine consumer EXCEPT this one, and the difference is mechanical:
#     • spec-inline code runs as `python3 - <<EOF`, so sys.path[0] == '' == cwd
#       == $FW  ->  `import blueprint_core` RESOLVES.
#     • the auditor is a standalone file run as `python3 /home/claude/X.py`, so
#       Python sets sys.path[0] to the SCRIPT'S OWN DIRECTORY. $FW is NOT on the
#       path even when cwd IS $FW  ->  the import FAILS.
#   Verified empirically in both directions. That single unnamed exception is why
#   the delegation could be written, reviewed, and shipped without its import.
#
#   THE FIX. P0 copies both engines from $FW into /home/claude — exactly the
#   pattern Framework_Blueprint.md §S1-2b already uses for blueprint_core. The
#   clone is hash-tracked and bootstrap-verified at Step 0 of every session, so the
#   engines are current BY CONSTRUCTION and a fix pushed to production reaches all
#   ~200 exams on their next clone, with nothing to upload. B3 returns to 6 files.
#   Sourcing engines from project knowledge would have created a second, unverified
#   copy per exam that can silently go stale — reintroducing precisely the
#   generator/auditor drift the v2.10 delegation exists to prevent.
#
#   Also retired here: the third and last "copy it from Framework_MockTestCreate.md
#   Appendix A" instruction (P1 REJECT hard-stop path). That route has been dead
#   since v2.11.2.
#
# v2.12 — 2026-08-01 — ENGINE BINDING + GATE FAULT ISOLATION
#   (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING, D1-D7). Step 8 HALTED PERMANENTLY
#   with ZERO gate output on any exam whose paper came from Step 7 v5.31+.
#
#   WHAT WAS WRONG. v2.10 delegated the A-FIGPROFILE verdict to blueprint_core so
#   the generator and its auditor could not drift. The delegation was written into
#   the COMMENTS and the CALL SITES; the IMPORT was never added. `bc` was read at
#   three sites and bound at none. Any registry carrying object_types raised
#   NameError out of gate_images() -> run_audit() -> main(), and because
#   print_results() runs only AFTER the last gate, the process died before a
#   single line printed. Not a failed gate — a failed RUN, blocking all three
#   phases and the completion gate with it.
#
#   WHY NO GATE SAW IT. No self-test fixture ever built a registry carrying
#   object_types, so every one of the 51 fixtures took A-FIGPROFILE's DORMANT
#   branch and the unbound name was never executed. The file returned 51/51 PASS
#   on a build that could not survive one real paper. v2.6 hardened the self-test
#   against a hollow FILE; this was a hollow BRANCH — the same miss one layer down.
#
#   FIVE CHANGES:
#   1. BIND blueprint_core with a THREE-LAYER guard. An import guard alone is NOT
#      sufficient, measured: `except ImportError` misses the SyntaxError a
#      TRUNCATED engine raises (blueprint_core.py is ~168 KB — squarely in the
#      project-knowledge truncation range P0.5 exists for), and a STALE engine
#      imports cleanly then raises AttributeError at the call site. L1 import
#      (except Exception) + L2 capability (hasattr on all three delegated fns) +
#      L3 call site (try/except) close all three paths to a reported skip.
#   2. GATE FAULT ISOLATION (_safe_gate). THE STRUCTURAL FIX. run_audit called 21
#      gates in bare sequence, so ANY raise in ANY gate destroyed the whole report.
#      From v2.12 no gate can abort the run: an unexpected raise becomes a LOUD,
#      NAMED A-GATEERROR FAIL and the remaining gates still execute. FAIL, not
#      WARN — a gate that crashed DID NOT AUDIT THE PAPER, so exit is non-zero and
#      certification is blocked, while the run still COMPLETES. This is the whole
#      "permanent halt" failure mode closed as a CLASS, for every future gate.
#   3. ALL 12 FIGURE GATES REPORT THEMSELVES. A single self-naming A-FIGSCALE WARN
#      stood in for twelve, so ELEVEN gates — including A-FIGMONO (VOID_ITEM, an
#      answer-cue leak) and A-FIGDEGEN (BLOCKING) — vanished from STDOUT with no
#      line at all. That is the silence CLAUDE.md forbids. The printed roster is
#      now INVARIANT regardless of environment, restoring §R15 reproducibility and
#      making the gate count itself a usable integrity signal.
#   4. BOTH ENGINES ARE NOW DECLARED AND DISTRIBUTED. routes.json routes
#      blueprint_core.py to Mock/TestCreateAudit AND to Mock/TestCreate (corpus_io
#      imports it — the same undeclared-dependency hole on the generator side).
#      Step 6 B3 ships both engines under BARE names (8 outputs, was 6).
#   5. TEN NEW FIXTURES (51 -> 61) executing A-FIGPROFILE's PRIMARY branch in every
#      environment the estate presents, plus a self-hosted UNDEFINED-NAME scan that
#      catches the next `bc`-class defect automatically in any gate.
#
#   AUTH_GATE_FLOOR STAYS AT 35 — deliberately. Raising it above 51 would HARD STOP
#   every deployed copy until each is refreshed; at 35 old and new copies coexist.
#
# v2.11.2 — 2026-07-31 — APPENDIX A SCRIPT EXTRACTED to audit_canonical.py (repo
#   engine, hash-tracked). The 2,194-line fenced canonical auditor moved byte-identically;
#   Appendix A retains the full contract + a pointer. Blueprint §13-7A copies the engine
#   file now. Zero behavioural change; self-test 51/51 verified on the extracted file.
# v2.11.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   584 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestCreateAudit'. The current companion block, the
#   v2.11 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v2.11 — 2026-07-29 — FIGURE CONFORMANCE GATES (GAP-2026-07-29-FIG-R2 +
#   VERIFY-2026-07-29-FIG-R2). TWELVE new Part-A gates, all DETERMINISTIC
#   arithmetic over the saved PNG and its FigureSpec sidecar.
#   WHY NO GATE SAW THIS. The reason is written in this spec's own v2.10 entry:
#   A-FIGPROFILE "AUDITS RECORDED INTENT, NOT PIXELS", because confirming a render
#   depicts a micrograph needs a view() — a CLASS T operation that cannot run
#   inside an audit's python. That is TRUE OF SEMANTICS AND FALSE OF EVERYTHING
#   ELSE. It was generalised from the one figure property that genuinely needs
#   eyes to every figure property. Colour presence, declared-hue separation,
#   placement scale, on-page label size, DPI metadata, plot-area degeneracy and
#   alt text are all cheap arithmetic; the entire gap was measured with them with
#   no vision available for most of the investigation. A-FIGPROFILE keeps its
#   intent-only scope and is unchanged.
#   SEVERITY — THREE MODES, AND NO COLOUR CONDITION MAY EVER HALT A RUN. This is
#   an owner directive and also this framework's own doctrine, CLAUDE.md: "A
#   CLASS T failure must be LOUD, and must NOT halt. These are separate
#   properties and the corpus conflated them... Silence is the defect; a halt is
#   not the remedy." A grey figure is a DEGRADED paper, never a void one.
#     AMBER      A-FIGCOLOUR, A-FIGCVD, A-FIGSERIES, A-FIGGLYPH, A-FIGALT,
#                A-FIGLABELPX. FAIL severity, forces the amber delivery footer
#                (Framework_DeliveryFooter §5), ALWAYS completes.
#     VOID_ITEM  A-FIGMONO, A-FIGOPTUNIF. The render leaks an ANSWER CUE, so that
#                QUESTION is invalid — drop or regenerate the single item. The
#                paper continues. Never halts the run.
#     BLOCKING   A-FIGSCALE, A-FIGLABEL, A-FIGDPI, A-FIGDEGEN. Renderer-contract
#                regression on Step 7 v5.33+ output ONLY. Safe to block solely
#                because they are unfireable by construction: verified 0 firings
#                across 144 conformant figures spanning display widths 1.3–7.5in,
#                2–8 series and four label sets including full scientific
#                notation. A firing means headroom or a tight bbox came back.
#   EC-V18 LEGACY TOLERANCE, NON-NEGOTIABLE. Output carrying NO FigureSpec
#   sidecar predates Step 7 v5.33, so every BLOCKING gate downgrades to AMBER for
#   it. Roughly 200 existing exams keep auditing AND DELIVERING untouched while
#   the defect is reported loudly on every one. fc.triage() never raises and
#   never halts; the audit completes on every path.
#   A-FIGLABEL IS ARITHMETIC, NOT PIXELS, and that distinction is load-bearing.
#   Three renders at an identical 10pt request and identical saved width measured
#   8.5pt when the axis titles carried "µmol photons m⁻² s⁻¹" and above the floor
#   with short labels: superscripts and subscripts are small connected components
#   that drag a pixel median down. A pixel gate is biased against exactly the
#   notation S10-7 Q9.4 mandates and would fail chemistry, biology and physics
#   papers hardest. A-FIGLABELPX retains that statistic as an ADVISORY only.
#   A-FIGCVD reads the DECLARED series colours, never extracted pixels: quantised
#   onto a 32-step cube the mandated Okabe-Ito blue and bluish-green separate by
#   57 against a true 60.6, and the check fired on its own palette — measurement
#   error reported as a defect. There is deliberately NO luminance clause;
#   greyscale survival is delivered by redundant encoding and gated by
#   A-FIGSERIES. Gate ids map from figural_core via fc.AUDIT_GATE_ID.
#
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the .docx produced by Step 7 (MockCreate) and the registry.json it
#   shipped, INDEPENDENTLY AUDIT every Question / Option / Image / Table / Matrix
#   / Chart / OMML expression / Paragraph in the paper, RECTIFY every defect
#   found, and emit a 100%-verified, zero-defect paper plus a registry re-synced
#   from the fixed file. Step 8 is the last gate before learner-facing artefacts
#   (Step 9 Explain) are built on top of the paper; a defect that survives Step 8
#   reaches students. Therefore Step 8 assumes nothing about Step 7's correctness
#   and re-derives every fact it certifies.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION
# ════════════════════════════════════════════════════════════════════════
#   Step 5 (PYQExtract)   → [ExamCode]_section_rules.md
#                                 [ExamCode]_subtopic_manifest.json
#   Step 6 (MockBlueprint) → [ExamCode]_blueprint.json
#                                 [ExamCode]_registry.json (empty template)
#   Step 7 (MockCreate)    → [ExamCode]_Mock[N]_Create.docx
#                                 [ExamCode]_registry.json (updated, mock N appended)
#   THIS STEP (MockCreateAudit) → [ExamCode]_Mock[N]_Create_Complete.docx (RECTIFIED)
#                                      [ExamCode]_registry.json (re-synced from fixed file)
#   Step 9 (MockExplain)   → consumes the rectified paper; builds the key + solutions
#   Step 10 (MockExplainAudit)
#   Step 11 (MockDeliver)
#
#   Steps 7–11 all run in the [ExamCode] project (exam-specific).
#   Step 8 runs immediately after the Step-7 session that generated mock N,
#   BEFORE Step 7 is run for mock N+1 (so the audited mock is always the most
#   recently registered one — see §13 registry re-sync, which relies on this).
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. It names no section, no
#   subtopic, no question count, no time/marks figure, no banned topic, no
#   sub-type code, no language, no figural type. Every such value is READ at
#   runtime:
#     • question/section counts, q_ranges, difficulty targets, format presence
#       → blueprint.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets,
#       difficulty calibration, OMML_required, option label format, language,
#       time/marks/negative-marking, figural object/transformation types,
#       passage word ranges, recycled-dataset bans
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, mandatory-every-mock list, alternation groups
#       → subtopic_manifest.json
#     • cross-mock dedup corpus (hashes, stems, semantic tuples, content_tracking
#       L4–L18, rc/figural manifests)
#       → registry.json
#   The same spec audits SSC CGL Tier 1, SSC CGL Tier 2, GATE, NEET, IBPS PO,
#   UPSC CSAT, CAT, regional exams — any exam with valid Step 0/1/2 outputs.
#   If a check needs an exam-specific value that is absent from these files, the
#   check is SKIPPED with a logged reason — it is NEVER hardcoded into this spec.

# ════════════════════════════════════════════════════════════════════════
# §0 — INPUT / OUTPUT CONTRACT (read before anything else)
# ════════════════════════════════════════════════════════════════════════

## S0-1 — INPUTS (what Step 8 is given)

  DELIVERED BY STEP 7 (the closed set; user uploads both to the [ExamCode] project):
    1. [ExamCode]_Mock[N]_Create.docx   — the paper to audit (the audit surface)
    2. [ExamCode]_registry.json           — dedup/tracking corpus (mock N appended)

  ALREADY IN PROJECT KNOWLEDGE (from Steps 0/1; required):
    3. [ExamCode]_section_rules.md        — per-subtopic rules + CATEGORY-C exam params
    4. [ExamCode]_blueprint.json          — allocations, sections, difficulty schedule
    5. [ExamCode]_subtopic_manifest.json  — subtopic_id ↔ name + mandate/alternation data
    6. [ExamCode]_mock_test_audit.py      — Part-A machine-gate script (MANDATORY — MANDATE A)
  NOT UPLOADED — OBTAINED FROM THE VERIFIED CLONE (v2.12.1):
    7. blueprint_core.py                  — repo engine. A-FIGPROFILE delegates its
                                            verdict to it (the SAME function Step 7
                                            v5.31+ generates against, so generator and
                                            auditor cannot drift).
    8. figural_core.py                    — repo engine. Powers the 12 figure-
                                            conformance gates (v2.11).

  These two are NOT project-knowledge inputs and must NOT be uploaded per exam.
  P0 copies them from the Step-0 verified clone ($FW) into /home/claude — the same
  pattern Framework_Blueprint.md §S1-2b already uses for blueprint_core. Engines
  live ONLY in the central repo (CLAUDE.md); a per-project copy would be a second,
  unverified source that can silently go stale. They keep their BARE names wherever
  copied: they are imported as Python modules and an [ExamCode]_ prefix breaks
  `import blueprint_core`.

  ENGINE ABSENCE IS NOT A HARD STOP (v2.12). Both are lazily imported and guarded.
  If either is missing, truncated, or stale, its gates report an explicit WARN
  ("NOT CHECKED" / "NOT RUN") and the audit COMPLETES. A missing engine is an
  ENVIRONMENT condition, not a paper defect, and must never block delivery of a
  sound paper (EC-V18). But it is never silent either: the WARN is a S5-4
  zero-warning blocker until the engine is uploaded or the skip is documented.

  7b. [ExamCode]_M[N]_audit_dossier.json  — TIER-A FACT DOSSIER (v2.17). OPTIONAL;
       absent on every pre-v5.35 paper and the audit then behaves exactly as before.
       Carries, per question, the FACTS Step 7 recorded: subtopic_id, qtype,
       image_role, difficulty, stem_precision, nat_grading_type/value, ca_range and
       the MSQ/NAT in-stem flags — plus an identity binding (exam_code, mock,
       paper_md5) and a schema.
       WHY IT EXISTS. Framework_MockTestCreate.md already says of concept_map "The
       audit gates read it directly instead of re-deriving", and audit_canonical.py
       has carried the consumer path since v2.4 — but nothing ever delivered it.
       Measured on a real 60-Q paper: 0 of 60 concept_map entries reached Step 8,
       A-NAT-GRADE printed "dormant" on all ~200 exams, image_role defaulted for
       every question, and A-FIGCOMP false-flagged 27 of 33 figural blocks (7 with
       the dossier). This is a REPAIR of a designed channel, not a new privilege.
       THE LINE: HAND OVER FACTS STEP 7 RECORDED; NEVER HAND OVER JUDGMENTS STEP 7
       REACHED. A fact is checkable against the artefact or the world; a judgment is
       what Step 8 exists to form. load_dossier() REFUSES any file carrying answers,
       answer_verified, derived_answer or any other judgment key, and refuses an
       identity mismatch — a dossier describing a different document would let Step 8
       audit against facts about another paper.
       AND THE RULE THAT KEEPS IT HONEST: **NO GATE MAY PASS ON DOSSIER EVIDENCE
       ALONE.** The dossier may make a check cheaper or make a mismatch visible; it
       may never be the thing that certifies. A-DOSSIER cross-checks every fact
       against the SHIPPED PAPER and the registry, and a disagreement is a FAIL —
       never a silent overwrite in either direction — because it means Step 7
       RECORDED something other than what it SHIPPED.

  NOT DELIVERED (Step 8 must do without these — by design, S13-6):
    ✗ [ExamCode]_M[N]_answer_key.json     — the answers + per-Q concept_map.
       CONSEQUENCE: Step 8 has NO answer key and NO concept_map. It re-derives
       both independently (§11 answer derivation; §9 audit ledger). Gates that
       Step 7 ran by reading the sidecar (G-CONCEPTDUP, G-ALLOC-SUBTOPIC,
       G-COUNT-X-UNIQUE, G-FORMATDUP, G-UNIQUE) are re-implemented here against
       the OBSERVABLE paper (the rendered text/images) + the registry, never
       against a sidecar.
    ✗ fig_manifest.json / batch_state.json / progress.json — internal Step-7 sidecars.
       The figural and RC/cloze maps Step 8 needs are embedded in registry.json
       (figural_manifests[], rc_manifests[]) and re-extracted at S3-PRE (§3).
    ✗ q{N}_*.figspec.json — the per-figure FigureSpec sidecars figural_core writes
       beside each PNG in the Step-7 working directory. Also internal, also never
       delivered. v2.13: their CONTENT nonetheless reaches Step 8, because Step 7
       v5.34 copies it into registry.figural_manifests[].figure_specs — the same
       registry-as-channel pattern object_types/subtopic_ids use (v5.31). This is
       what the twelve v2.11 figure-conformance gates audit against; a manifest
       with no figure_specs key (any pre-v5.34 paper) makes every figure read as
       legacy, and EC-V18 then applies — the correct degradation, never a wrong
       verdict, and never a halt.

## S0-2 — OUTPUTS (what Step 8 delivers)

  CORE DELIVERABLE SET (always; via ONE present_files call, at certification / Phase 3):
    1. [ExamCode]_Mock[N]_Create_Complete.docx   — the RECTIFIED, zero-defect paper
                                            (distinct filename — reads Mock[N]_Create.docx,
                                             writes Mock[N]_Create_Complete.docx; input retained)
    2. [ExamCode]_registry.json           — RE-SYNCED from the fixed file (§13):
                                            mock-N hashes/stems/tuples/manifests/
                                            content_tracking rebuilt to match the
                                            rectified content.
  CONDITIONAL DELIVERABLE (only when ≥1 question was REGENERATED — Class RG, §8):
    3. [ExamCode]_Mock[N]_audit_changelog.md  — an AUTHOR-ONLY audit artefact
                                            carrying, per regenerated question, the
                                            literal BEFORE→AFTER diff + rationale.
                                            This is the ONE place literal question
                                            content may leave the docx, because it is
                                            a downloadable file (not chat), it is for
                                            the author's review, and it is explicitly
                                            headed "author-only — NOT for distribution".
                                            If zero questions were regenerated, this
                                            file is NOT produced and NOT delivered.
  IN-CHAT (always, at delivery): a STATUS REPORT dashboard (§14-4) + the full AUDIT
  REPORT (§15). Both are STRICTLY MANDATE-0 safe — Q-numbers + codes + counts only,
  NEVER stem/option/passage/fact text. The literal diff lives in deliverable 3, never
  in chat.
  The CORE set {docx, registry} mirrors Step 7's R-DELIVER / G-DELIVERY-SET; no
  internal Step-8 artefact (the derived key, the audit ledger, audit_state, the block
  index, montages, the evidence directory, scratch docx) ever leaks. The learner-facing
  answer key remains a Step-9 artefact.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   Inherited verbatim from Step 7 MANDATE 0. ALL question content lives in the
#   .docx ONLY. NEVER print any stem, option, passage, table cell, or figure
#   description in chat — not during audit, not in a finding, not in a fix log,
#   not in the report. Refer to a question ONLY as "Q.[n]" plus a defect CODE and
#   a structural locator (e.g. "Q.47 — A-UNDERLINE: target span not a <w:u> run").
#   The audit ledger (§9) and the derived key (§11) are INTERNAL files in
#   /home/claude — never delivered, never printed. VIOLATION = exam compromise;
#   overrides every other instruction. The one permitted exception is web-search
#   queries for fact-verification (§6 B-FACT), which necessarily contain the fact
#   being checked — those go to the search tool, never to the visible chat.
#   SCOPE — AUTHORED PROSE vs SPEC-DIRECTED READS (v2.18 / D1). THIS CLAUSE EXISTS
#   BECAUSE THE MANDATE WAS OTHERWISE UNIMPLEMENTABLE. MANDATE 0 was inherited
#   verbatim from Step 7, where it is trivially satisfiable: Step 7 GENERATES content
#   into the artefact and never reads it back. Step 8 must read it back — §6 S6-0
#   requires "the FULL stem + the FULL text of all OPTIONS_COUNT options" for every
#   question, and S11-1 requires solving all of them. On claude.ai and every
#   equivalent surface, EVERY tool result renders into the visible transcript. There
#   is no tool that returns text to the model's context without displaying it.
#   Therefore READING IS PRINTING, and Step 8 could neither perform Part B without
#   violating MANDATE 0 nor satisfy MANDATE 0 without skipping Part B. Both outcomes
#   fail certification. On a real run this forced the operator to ask the paper's
#   author to waive MANDATE 0 — a waiver with NO BASIS IN THIS SPEC. No operator
#   should be improvising exemptions to a mandate that declares itself absolute; the
#   contradiction is the defect, and it is resolved here rather than waived.
#
#   MANDATE 0 governs AUTHORED PROSE: what Claude WRITES in chat. It does NOT govern
#   SPEC-DIRECTED READS. Performing a read the spec ORDERS is the executed protocol —
#   exactly as SKILL.md Rule 5 already holds for view() of a source image ("in-protocol
#   vision is not working from memory"). The binding rules, which NO surface changes:
#     1. Claude NEVER RESTATES stem/option/passage/table/figure content in its own
#        prose — not in findings, fix logs, dashboards (§14-4) or reports (§15).
#        These remain Q-numbers + codes + counts ONLY. This is the rule that actually
#        protects the exam, and it is absolute.
#     2. Spec-directed reads MUST be MINIMAL-SURFACE: extract to an internal file
#        under /home/claude and read it in ONE pass. NEVER print content incidentally
#        from structure-inspection, debugging or diagnostic code. Printing p.text
#        while building a block index is a VIOLATION; printing len(block.opts) is
#        correct. Incidental leakage is logged to session_log.mandate0_incidents[]
#        and disclosed in §R13.
#     3. P0 emits the SURFACE NOTICE below exactly once, before any Part-B read.
#
#   P0 SURFACE NOTICE (mandatory, verbatim, once per session):
#     "MANDATE 0 SURFACE NOTICE: this deployment renders tool results into the
#      transcript. §6 Part B requires reading every stem and option, so question
#      content WILL appear in this session log. Authored output remains content-free.
#      If this session log will be shared beyond the paper's author, stop and run
#      Step 8 on a non-rendering surface."
#   If the surface type is unknown, ASSUME RENDERING and emit the notice (fail safe).
#   On a shared or multi-tenant project the notice instructs a HALT — that is the ONLY
#   case in which Step 8 should stop for MANDATE-0 reasons.
#
#   SCOPE NOTE (v1.1): MANDATE 0 governs the CHAT STREAM. The two content-bearing
#   artefacts the author downloads — the rectified .docx and (only when questions were
#   regenerated) the audit change-log .md (S8-5 / S14-1) — are FILES, not chat, and
#   are the legitimate homes for question content. The change-log is headed
#   "author-only — not for distribution". Nothing changes for chat: the status
#   dashboard (§14-4), the report (§15), every finding and fix log remain strictly
#   content-free (Q-numbers + codes + counts only). "Put the diff in chat" is still
#   forbidden; the diff goes in the file. The evidence artefacts (§9-1 / §7 montages,
#   saved fact-sources, recompute traces) also live in /home/claude and are NEVER
#   delivered or printed (they may contain answer-bearing content).

# ════════════════════════════════════════════════════════════════════════
# MANDATE A — mock_test_audit.py IS MANDATORY FOR STEP 8 (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Step 7 treats the audit script as OPTIONAL (a manual checklist substitutes).
#   Step 8 does NOT: Part A (the machine-gate sweep) cannot run without it, and
#   Part A is a precondition for the whole-paper re-verification that makes
#   per-batch sign-off honest (§4). If [ExamCode]_mock_test_audit.py is absent
#   from project knowledge:
#     HARD STOP. Print:
#       "HARD STOP (MANDATE A): [ExamCode]_mock_test_audit.py not found in the
#        [ExamCode] project Files. Step 8 cannot run Part A without it.
#        This file is auto-generated by Step 6 (MockBlueprint) v1.20+.
#        Verify that all 6 Step 6 output files were uploaded to project Files.
#        If Step 6 was run before v1.20: re-run Step 6 B3 to generate the script.
#        (The live source is the repo engine audit_canonical.py. The former
#        'copy it from Framework_MockTestCreate.md Appendix A' fallback is DEAD —
#        that file has carried no auditor fence since v2.11.2 and now only points
#        here. Corrected v2.12.)"
#   The script is auto-generated ONCE by Step 6 at B3 and uploaded alongside
#   blueprint.json, registry.json, and other Step 6 outputs.
#   v2.6 — MANDATE A GUARANTEES A WORKING AUDITOR, NOT A FILE THAT PRINTS "PASS".
#   The script self-tests with `--self-test`, which MUST be the FIXTURE-BASED
#   authoritative self-test: it builds tiny docx fixtures and asserts each gate
#   CATCHES a planted defect AND PASSES a clean fixture, and it must print
#   "SELF-TEST: N/N PASS" with N >= AUTH_GATE_FLOOR (currently 35 — the Appendix A
#   authoritative count) AND include the C1–C7 completion-gate fixtures. A
#   CONSTANT-PRINT stub that merely emits "N/N PASS" without executing any gate
#   (e.g. the 13-gate minimum-viable stub `def self_test(): print("SELF-TEST:
#   13/13 PASS"); return 0`) is REJECTED at P1 — it is NOT an acceptable auditor.
#   The one canonical script that satisfies this is Appendix A (and its lockstep
#   twins — see §21). For the generation/lifecycle contract see
#   Framework_Blueprint.md §13-7A.

# ════════════════════════════════════════════════════════════════════════
# MANDATE D — DELIVER ONCE, ONLY WHEN CERTIFIED CLEAN (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   present_files is FORBIDDEN until the WHOLE paper is certified clean at Phase 3.
#   ONE EXPLICIT CARVE-OUT (v2.15/C1) — THE CHECKPOINT IS NOT A DELIVERY. The
#   per-batch [ExamCode]_M[N]_audit_checkpoint.zip (S4-7 / RA-18) IS handed to the
#   author before certification, and that does NOT breach this mandate. What
#   MANDATE D forbids is shipping a PAPER that is not certified — mid-audit the
#   docx is deliberately inconsistent and must never be presented as a product.
#   The checkpoint is not a product: it is opaque resume state, it is explicitly
#   headed as such, it contains no certified artefact, and its only use is being
#   handed back on `resume`. Without it MANDATE D's own promise is unkeepable,
#   because an exhausted session destroys the evidence that certification depends
#   on. The CERTIFICATION delivery remains exactly ONE present_files call of the
#   closed set at Phase 3 (§14), and S14-2 check 6 still requires /mnt/user-data/
#   outputs to hold EXACTLY that set — so the checkpoint MUST be cleared from
#   outputs before the final delivery (S14-2 check 7).
#   v2.6 — "certified clean" is now a COMMAND RESULT, not a self-judgment: the
#   Phase-3 COMPLETION GATE (S5-1A) must print "COMPLETION-GATE: PASS" (final Part A
#   exit 0 + zero fixable WARN + the C1–C7 ledger/evidence assertions all pass +
#   registry re-synced). A self-declared "clean" is NOT acceptance — the completion
#   gate is (MANDATE B). Mid-audit the docx is deliberately inconsistent (a fix in
#   one batch can transiently open a global defect that the next whole-paper Part A
#   closes), so a partial file must never be presented. /mnt/user-data/outputs stays
#   EMPTY until Phase 3; the work-in-progress docx is staged in /home/claude across
#   "continue" turns so it is never lost. This mirrors Step 7 S13-7 and the T2 §12
#   invariant "present_files FORBIDDEN until exit 0 + verdict clean". The ONE
#   present_files call ships the core set (+ the change-log artefact when
#   regenerations occurred) — see §14.

# ════════════════════════════════════════════════════════════════════════
# MANDATE B — EXHAUSTIVE BATCHED REVIEW (Phase 2 cannot be collapsed) (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Phase 2 (§4 S4-3) audits EVERY question — zero sampling (RA-3) — in K batches of
#   ≤ AUDIT_BATCH_SIZE (§4 S4-6). It may NEVER be skipped, compressed into a single
#   consolidated pass, or replaced by a spot-check, in ANY mode (interactive OR
#   autonomous). The spec keeps two things SEPARATE, and only one is waivable:
#     • EXHAUSTIVENESS (RA-15a) — every question gets B-SOLVE / B-UNIQUE / B-DISTRACT /
#       B-STEMOPT / B-FACT / B-PASSAGE (§6) + §7 view/recompute, each leaving a STAMPED
#       entry in audit_state.ledger (§9-1) that NAMES its on-disk evidence artefact
#       (§7 montage / saved fact-source / recompute trace). NON-NEGOTIABLE.
#       Mode-independent.
#     • PACING (RA-15b) — one batch = one response, continue-gated. MAY be waived in
#       autonomous mode (§4 S4-3A). Waiving the PAUSE NEVER waives the REVIEW.
#   ENFORCEMENT (not prose): Phase 3 (§4 S4-4 STEP 1) runs the audit.py COMPLETION
#   GATE — `--final --audit-state <path>` (S5-1A). It asserts, from audit_state.json:
#   batches_done == K; one stamped ledger entry per question (== total_questions);
#   B-UNIQUE / A-MSQ-KEY ran per question; every factual entry has a recorded
#   fact_source WHOSE SAVED FILE EXISTS (RA-11); every §7 artefact carries its RA-19
#   stamp AND the montage/recompute file it names EXISTS and is non-trivial. ANY
#   failed assertion → exit non-zero → HARD STOP: present_files is FORBIDDEN
#   (MANDATE D). A self-declared "clean" is NOT acceptance — the completion gate is.
#   This closes the Phase-1→Phase-3 shortcut that a machine-only Part A + a hollow
#   self-test cannot catch. "I ran fast because I skipped Phase 2" is a MANDATE B
#   violation, not a valid autonomous run.

# ════════════════════════════════════════════════════════════════════════
# THE CORE PRINCIPLE — fix locally, verify globally, certify whole-paper last
# ════════════════════════════════════════════════════════════════════════
#   Auditing differs from generating in two ways that drive the whole architecture:
#     (1) The paper exists IN FULL at second zero. So machine gates that are
#         WHOLE-PAPER by nature (answer-run patterns, cross-mock dedup, allocation
#         tallies, cross-section boundaries) run over the ENTIRE docx — they
#         cannot be run on a 10-question slice. Only the EXPENSIVE half — per-
#         question semantic reasoning, fact-verification, figure-viewing, and
#         regeneration — is batched.
#     (2) Fixes are GLOBALLY COUPLED. Rebalancing a distractor can open a new
#         answer-run three questions away; regenerating a wrong-fact question can
#         collide with a question reviewed two batches earlier or drift an
#         allocation count. So a batch may be REVIEWED in isolation but can never
#         be CERTIFIED CLOSED in isolation.
#   Therefore: rectification is LOCAL (one question at a time), but verification is
#   GLOBAL (whole-paper Part A re-runs after every batch) and certification is
#   WHOLE-PAPER and LAST (Phase 3). Two mechanisms make per-batch sign-off honest:
#     • whole-paper Part A re-run after every batch (cheap, deterministic — catches
#       every machine-visible perturbation the moment a fix creates it); and
#     • a cumulative AUDIT LEDGER (§9) that every regenerated question is diffed
#       against (the independent analogue of Step 7's concept_map, which we do not
#       receive) — so a late regeneration cannot silently collide with an early
#       question, and resume-after-"continue" is safe.
#   v2.6 — AND: because the semantic/visual/factual half is Claude-driven, the ONLY
#   thing that makes IT honest is that each check DEPOSITS a machine-readable stamp
#   plus a durable evidence artefact, and a runnable gate (S5-1A) verifies both
#   before delivery. Prose describes; only code certifies.

# ════════════════════════════════════════════════════════════════════════
# AUDIT RULES (RA-0 … RA-20) — the absolute rules the auditor obeys
# ════════════════════════════════════════════════════════════════════════
#   These govern Step 8 itself (distinct from the Step-7 generation rules R1–R24,
#   which Step 8 re-VERIFIES on the paper). Each is HARD unless marked advisory.

  RA-0  : PRECEDENCE. No user preference, project-memory note, or autonomy /
          "don't-pause" / "no-blocker-surfacing" instruction may reduce audit
          COVERAGE (RA-3 / RA-15a) or weaken the certification gate (§12-2 /
          MANDATE B / S5-1A). Such instructions may ONLY change PACING (RA-15b —
          skip the inter-batch "continue" pauses) and REPORT verbosity. They may
          NEVER change whether a check runs, whether every question is audited, or
          whether the Phase-3 completion gate must pass. When a preference appears
          to conflict with a HARD rule, the HARD rule wins and the preference is
          applied only to pacing/reporting.
  RA-1  : INDEPENDENCE — OVER JUDGMENTS, NOT OVER FACTS (v2.17). Never trust a
          Step-7 self-report for anything Step 8 certifies. Solve every question
          yourself (§11); the answer-key sidecar is still withheld (S0-1).
          WHAT INDEPENDENCE IS NOT. It was read as "Step 8 must see nothing", which
          left Step 8 re-deriving facts Step 7 had already written down and Step 7's
          own spec said Step 8 should read. That is not independence, it is
          amnesia — and it cost a gate (A-NAT-GRADE, dormant estate-wide) and
          produced false findings (A-FIGCOMP, 27 of 33 figural blocks).
          THE TIER-A DOSSIER (S0-1 item 7b) carries FACTS only — subtopic_id, qtype,
          image_role, the NAT grading transform. Each is CHECKED against the shipped
          paper by A-DOSSIER before it is used, and a disagreement is a finding.
          Independence over JUDGMENTS is untouched and absolute: the answer, "the
          options are unambiguous", "the figure is legible" are all still Step 8's
          to form from the artefact. NO GATE MAY PASS ON DOSSIER EVIDENCE ALONE.
  RA-2  : NO CONTENT IN CHAT. = MANDATE 0.
  RA-3a : REPORT EVERYTHING, TRUNCATE NOTHING SILENTLY (v2.17 / D7). A findings
          list is rendered by _flist(): it sorts Q-numbers NUMERICALLY and, when it
          shows a head, states "[+N MORE NOT SHOWN; T TOTAL]". Gates previously
          printed `sorted(set(x))[:12]`, so A-FIGCOMP with 27 findings showed 12 and
          15 vanished without trace — in lexicographic order (Q3 after Q28), which
          read as non-determinism and was filed as an unreproducible gate. It was
          neither: it was under-reporting, in numeric-blind order. A finding that
          exists and is not shown is the same false-clean class as a vacuous pass.
  RA-3  : AUDIT EVERYTHING, SAMPLE NOTHING. Every question, every option, every
          image, every table cell, every OMML node is checked. Zero sampling.
          "Spot-check N random Qs" is FORBIDDEN for any content-correctness check.
  RA-4  : RENDER-OR-RECOMPUTE OR IT DOESN'T COUNT — WITH ONE DECLARED, MEASURED
          ENVIRONMENT STATE (v2.16 / D2). A visual/structured check is valid only if
          the artefact was rendered and VIEWED (images/charts) or parsed and
          ARITHMETICALLY RECOMPUTED (tables/matrices/OMML). A check asserted from
          filename, alt-text, p.text, or "looks present" is void and the item is
          treated as un-audited (§7, §18 invariants). The VIEW/RECOMPUTE must leave a
          durable evidence artefact on disk (§9-1) that S5-1A verifies — an un-backed
          stamp is treated as un-audited.
          WHY v2.16 EXISTS. Until now RA-4 did TWO jobs with one rule: it blocked a
          LAZY OPERATOR from skipping a view (correct, and unchanged) and it also
          blocked an ENVIRONMENT OUTAGE from degrading (wrong). When the view path
          failed mid-session on a real 60-Q paper, 43 images across 27 figural
          questions became un-stampable, C6/C7 could never pass, MANDATE D forbade
          delivery, and there was NO defined state for "vision unavailable": the audit
          was permanently STUCK, not degraded. That contradicts this framework's own
          doctrine — §5's "NO DEPENDENCY CONDITION MAY EVER HALT A RUN" and CLAUDE.md's
          "Silence is the defect; a halt is not the remedy." Degradation was granted to
          blueprint_core, to figural_core, to all twelve figure gates and to every
          colour condition, and denied to the one dependency whose absence is fatal.
          THREE STAMP STATES, and only three:
            • 'rendered-and-viewed' — montage saved AND actually viewed. Certifies
              normally. This remains the ONLY clean state.
            • 'view-unavailable'    — montage saved and >= EVIDENCE_MIN_BYTES, AND a
              P3.5 probe MEASURED the outage for that batch. NEVER assertable by
              choice (see below). Certifies DEGRADED.
            • (absent)              — un-audited. Blocks exactly as before.
          THE STAMP IS UNFAKEABLE, WHICH IS THE WHOLE SAFETY ARGUMENT. "I could not
          see it" is precisely what a lazy operator would claim, so it may never be an
          operator's word. S5-1A C6 admits 'view-unavailable' ONLY when
          session_log.vision_probe carries a FAILED record — a MEASURED fact produced
          by P3.5, whose expected glyphs are stored as a salted SHA-256 so that
          reporting them requires actually seeing the card. C6 additionally FAILS if
          vision has since RECOVERED and the stamps were not upgraded (E2.3): a paper
          that COULD have been fully audited must not certify degraded.
          DELIVERY CONSEQUENCE. A degraded run prints
          `COMPLETION-GATE: DEGRADED (vision) — ...`, exits 0, certifies as
          CERTIFIED-DEGRADED (VISION), forces the F1 AMBER footer and writes a §R13
          limitation. Delivery is NOT blocked. This is the identical treatment EC-V18
          legacy figures already receive across ~200 exams: a paper whose figures were
          machine-checked but not eyeballed is in the same epistemic class, and is
          demonstrably better than the current outcome, which is NO PAPER AT ALL.
          WHAT DOES NOT DEGRADE. Tables, matrices, charts-as-data and OMML are
          ARITHMETIC, not vision (E2.7) — unaffected by an outage and still fully
          authoritative. A missing or trivial montage is NOT a vision condition
          (E2.5/E2.6): the item is un-audited and blocks. A question whose key cannot
          be derived without sight (E2.8) is a VOID_ITEM — status
          'regenerated-required', listed in §R13 and the dashboard as KEY NOT
          DERIVABLE. It MUST NOT be silently keyed.
  RA-5  : RECTIFY, DON'T JUST REPORT. Every defect found is FIXED in the same
          session (§8): mechanical defects in place; content defects by
          regenerating that one question under Step 7's contracts; then re-audited.
          Step 8 never ends with a known-unfixed defect and a "DON'T SHIP".
  RA-6  : REGENERATION OBEYS STEP-7 CONTRACTS. Any replacement question must
          satisfy EVERY Step-7 rule it would have had to satisfy at generation:
          blueprint count + subtopic_id join, section_rules pattern + difficulty +
          wrong_option_structure, registry dedup (L1–L18), intra-mock scenario +
          presentation uniqueness, and all render contracts (R-LINKED, R-FIGURAL,
          R-UNDERLINE, R-OPTREF, R-UNIQUE, R-MATH-OMML, R10/R13/R14/R24). A fix
          that introduces a new violation is itself a defect (§8 re-audit loop).
  RA-7  : FIX LOCALLY, VERIFY GLOBALLY. After any batch's fixes, re-run the
          WHOLE-PAPER Part A before ending the batch; resolve any global
          perturbation in the same response (core principle).
  RA-8  : NEVER REDUCE COUNT TO "FIX". A duplicate/clone/over-allocation is fixed
          by REGENERATING on a new scenario/presentation — never by deleting a
          question (which would break the blueprint allocation). Inherited from
          Step 7 G-CONCEPTDUP / G-FORMATDUP fix discipline.
  RA-9  : EXAM-AGNOSTIC. Read every exam-specific value from the source files
          (EXAM-AGNOSTIC GUARANTEE). Hardcode nothing. A missing value → SKIP the
          dependent check with a logged reason, never a hardcoded substitute.
  RA-10 : LANGUAGE-AWARE. The non-ASCII / regional-script check (A-SCRIPT) is
          conditioned on section_rules CATEGORY-C `language`. Devanagari/Tamil/etc.
          is LEGITIMATE on a hindi/bilingual/regional exam and must NOT be flagged
          as corruption; it is flagged ONLY when language == 'english' (then it is
          copy-paste corruption). U+FFFD replacement characters are ALWAYS a defect
          regardless of language.
  RA-11 : LIVE FACT-CHECK, EVIDENCE ON DISK, ONE LINE IN CONTEXT (v2.14/B3).
          Every current-affairs and static-GA fact, and every factual option, is
          web-verified at audit time (§6 B-FACT). Never certify a fact from model
          memory. A fact that cannot be sourced, or is wrong, is a defect →
          regenerate. The verification MUST save its raw result (query + URL +
          retrieval-time + snippet) to the evidence dir and the ledger entry's
          fact_sources[] MUST name that saved file — S5-1A C5 fails if the file is
          absent, unparseable, or missing any of those four fields (a bare URL
          string is not sufficient, and neither is a touched stub).
          CONTEXT DISCIPLINE (B3 — the reason Step 8 exhausted sessions). The raw
          search result goes to DISK, not into the reasoning stream. After each
          verification, carry forward ONE line — "q17 · VERIFIED · <domain> ·
          <retrieval-date>" or "q17 · UNSOURCED → RG" — and nothing else. Measured:
          on a 60-question science paper the C-FACTUAL fan-out (keyed fact + every
          option, ~25 questions) is ~125 searches; retaining full result sets costs
          upwards of 400k tokens and alone exhausts the session before Phase 3,
          which then loses the whole audit (the evidence dir does not survive a
          session boundary — see RA-18).
          THREE RULES, none of which reduces coverage:
            (a) SAVE-THEN-SHED. Write the full result to evidence/facts/ and keep
                only the verdict line. The saved file is the audit's evidence and
                C5 verifies its shape; context is not a second copy of it.
            (b) CACHE BY CONCEPT. Maintain ledger.fact_cache keyed by the
                normalised fact concept. A concept already verified in this mock
                is NOT searched again — the later question REUSES the saved file
                by path. C5 accepts one file referenced by many questions and
                reports the reuse. Re-searching a settled concept is redundant
                work, not extra rigour.
            (c) GROUP THE OPTIONS. Where a question's options are same-domain
                claims, ONE well-formed query may adjudicate the whole option set;
                record every option's verdict in the one saved record (the file
                may hold a LIST). Split into per-option queries only where the
                grouped result does not settle an option. Every option is still
                verified — what changes is how many result sets are retained.
          WHAT B3 DOES NOT TOUCH: which facts are checked (all of them), that the
          check is LIVE, that it is per-option, or that it is evidence-backed.
          Coverage is identical; only the context footprint changes.
  RA-12 : DEFENSIBLE-ANSWER CONTRACT (mirrors Step 7 R-ANSWER; parameterised by the
          subtopic's answer_cardinality, re-derived from blueprint subtopic_list — default
          'single'). SINGLE: every question has exactly one defensible correct option
          (a second defensible option = defect → disambiguate the stem or replace the
          colliding option, §8). MULTI (MSQ): the re-derived correct SET S is a non-empty
          PROPER subset of {1..OPTIONS_COUNT} (1≤|S|≤n−1, and |S|=msq_k when
          msq_k_mode=fixed); every IN-set option is defensible under EVERY fair reading
          and every OUT-set option is indefensible under ANY fair reading — a borderline
          OUT-set option (one that should arguably be selected) is the MSQ analogue of the
          two-defensible-answers defect → disambiguate or move/remove it. Negation
          composes (derive S for the negated predicate, then apply the contract). This is
          the single most student-harmful content defect; it is checked for EVERY Q in the
          mode that question's subtopic declares.
          NUMERICAL (NAT; v1.4, when the subtopic is answer_type=='numerical'): the axis is
          checked FIRST and supersedes cardinality — there are no options to adjudicate. The
          re-derived answer is a single VALUE that the stem must determine UNIQUELY (two
          defensible values under a fair reading — ambiguous rounding, under-specified figure,
          missing unit — is the NAT analogue of the two-defensible-answers defect → disambiguate
          the stem). The value's form must match nat_answer_type (integer⇒integral; real⇒a
          decimal at the exam's precision); for real NAT the accepted band is
          [value−nat_tolerance, value+nat_tolerance] = ca_range (lo≤hi). A 0/negative/fractional
          value is valid (presence-tested, never truthiness). The value must not leak as a given
          elsewhere.
          v2.8 — PORTAL GRADING VALUE (S7-NEW-C in Step 7; separate concern from the math VALUE
          above): the sidecar's nat_grading_type/nat_grading_value must be exactly what
          `derive_nat_grading()` (byte-identical to Step 7's canonical §S7-NEW-C definition —
          copied here, never re-implemented independently, per anti-drift-by-design) produces
          from the SAME re-derived value + ca_range + any stem-stated rounding instruction. A
          mismatch here is a defect on the GRADING TRANSFORM, not the math — the value can be
          correct while its portal string is wrong (this was the original SSC-Biology defect:
          value 3×10⁻⁹ correct, portal string "3e-9" wrong). Enforced by A-NAT-ANSWER
          (Claude-derivation — cross-checks the grading transform against the SAME value it just
          independently re-derived, in the same review pass) + A-NAT-GRADE (machine — a
          self-consistency backstop: re-runs derive_nat_grading() on the SIDECAR's OWN recorded
          value/ca_range/tolerance and checks the result matches the sidecar's OWN recorded
          grading type/value, catching a Step-7-side execution bug independent of whether the
          math value itself is later found correct or incorrect).
          Enforced by A-NAT-ANSWER (Claude-derivation) + A-NAT-NOOPT/A-NAT-INSTR/A-NAT-GRADE
          (machine) — see §5.
  RA-13 : CROSS-MOCK INTEGRITY. Cross-mock dedup runs FULLY against registry.json
          with --mockN N self-exclusion (so re-auditing the registered mock does
          not flag its own stems). Intra-mock dedup is verified in its OBSERVABLE
          form (rendered text/images), since the concept_map is not delivered (§10).
  RA-14 : DELIVER ONCE, CLEAN. = MANDATE D.
  RA-15a : EXHAUSTIVENESS. Every question in Phase 2 is audited — zero sampling
           (RA-3) — and leaves a stamped audit_state.ledger entry (§9-1) that names
           its on-disk evidence artefact. Holds in EVERY mode; no preference may
           waive it (RA-0). This is the WHAT. Mechanically enforced by S5-1A
           (C2/C3 + evidence checks).
  RA-15b : PACING / BATCH STOP LAW. Interactively: one batch = one response, each
           ending on an explicit "continue"; Claude never auto-advances. In
           AUTONOMOUS mode (§4 S4-3A) the pause is waived and Batches 1..K run
           sequentially in one session — RA-15a still holds for every question.
           Phase 1 ends waiting for "continue" (interactive only); Phase 3 auto-runs
           after batch K in both modes. This is the WHEN. Linked-stimulus groups are
           atomic (RA-16); the whole-paper machine sweep (Phase 1) and the final
           certification (Phase 3) never wait for "continue".
  RA-16 : ATOMIC LINKED GROUPS. A linked-stimulus group (RC passage set, cloze
          set, DI table/chart set, puzzle set) is NEVER split across batches; it is
          reviewed as one unit so cross-member consistency is checkable together.
          v1.4 (ND11): a linked group MAY contain NAT members (a shared DI table/chart
          followed by numerical-answer questions). A NAT member is a 0-option member — the
          shared-stimulus self-containment audit (A-STIMORPHAN) and atomic-group review are
          UNCHANGED (orthogonal to whether a member has options); the member is simply audited
          under the numerical gates (A-NAT-NOOPT/INSTR, A-NAT-ANSWER, B-SOLVE/UNIQUE/LEAK NAT).
  RA-17 : REGISTRY RE-SYNC FROM THE FIXED FILE ONLY. The output registry is rebuilt
          from the FINAL rectified docx (§13), never from the input registry's stale
          mock-N entries and never from generation memory.
  RA-18 : RESUME-SAFE — WITHIN A SESSION *AND* ACROSS ONE (v2.15/C1). All
          cross-batch state (audit ledger, batch plan, the WIP docx, the derived
          key, the evidence dir) persists in
          /home/claude/[ExamCode]_M[N]_audit_state.* so a "continue" after any gap
          resumes exactly, re-reviewing nothing and forgetting nothing (RA-3 still
          holds across resume).
          /home/claude DOES NOT SURVIVE A SESSION BOUNDARY. Until v2.15 that made
          "resume-safe" true only inside one session, and the failure was fatal
          rather than degraded: S5-1A C5/C6 assert that every stamped evidence
          file EXISTS, so once the montages and saved fact records were gone a
          perfectly remembered ledger could never certify. A session that
          exhausted mid-Phase-2 lost the entire audit, and the retry exhausted the
          same way — a loop, not a one-off.
          THEREFORE: at the end of every Phase-2 batch, Step 8 writes
          [ExamCode]_M[N]_audit_checkpoint.zip — audit_state.json + the WHOLE
          evidence tree + the WIP docx, with a manifest carrying the identity
          triple (exam_code, mock, paper MD5) and a sha256 for every member — and
          hands it to the author (S4-7). On `resume` the uploaded checkpoint is
          verified and rehydrated at P0.5C before any batch runs. Neither the build
          nor the restore is prose: both are commands in audit_canonical.py, and
          restore REFUSES on a schema it does not know, on any member whose hash
          differs, or on an exam_code / mock / paper-MD5 that disagrees with the
          paper in hand. Restoring a checkpoint onto the WRONG paper would certify
          an audit nobody performed on it — strictly worse than losing the audit —
          so those bindings are HARD and are checked before a single byte is
          written to disk. A refused restore leaves NOTHING behind: a
          half-unpacked checkpoint is the worst outcome of all, because it looks
          resumable.
  RA-19 : PROVENANCE STAMPS. Every certified item carries a stamp in the ledger
          ('machine' | 'recomputed' | 'rendered-and-viewed' | 'web-verified+source'
          | 'reviewer-verified') AND, for every visual/structured/factual item, the
          PATH of the durable evidence artefact that stamp is backed by (§9-1).
          Phase 3 refuses to certify if any item lacks the stamp its check-class
          requires OR if the named evidence file is missing/trivial (§18, S5-1A). An
          un-stamped or un-backed visual/structured item blocks delivery (RA-4).
  RA-20 : KINDNESS TO THE NEXT STEP. The handoff (§14) states plainly what was
          fixed/regenerated (by Q-number + code, never content) and instructs the
          user to replace the registry in project knowledge before Step 9 / the
          next mock — so dedup integrity is preserved across the series (RS-10).

# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S1-1 — Sources of truth (strict priority order)

  Priority 1: This spec (Framework_MockTestCreateAudit.md)        — audit procedure
  Priority 2: [ExamCode]_blueprint.json    — counts, sections, q_ranges, difficulty,
                                              format presence (CONFLICT WINNER on
                                              allocation/structure, per Step 7 S1-2)
  Priority 3: [ExamCode]_section_rules.md  — per-subtopic patterns, formats, escape
                                              tokens, OMML_required, language, exam params
  Priority 4: [ExamCode]_subtopic_manifest.json — subtopic_id join + mandate/alternation
  Priority 5: [ExamCode]_registry.json     — cross-mock dedup corpus + embedded manifests
  Priority 6: The paper itself             — the audit surface (never a source of
                                              "truth" about what is CORRECT; only the
                                              object under test)

  CONFLICT RULE (inherited from Step 7): blueprint.json wins over section_rules.md
  on format assignments, allocation counts, and structural decisions. section_rules
  wins on per-subtopic CONTENT patterns, escape tokens and rendering requirements.
  The paper never overrides a source file — a paper that disagrees with a source
  file is, by definition, the defect under repair.

## S1-2 — Memory prohibition

  ABSOLUTE (= Step 7 S1-4): Claude must NEVER use training memory to decide whether
  a question is correct, whether a fact is current, what a subtopic's scope is, or
  what a pattern should look like. Content correctness is decided by RE-DERIVATION
  (solve it) and WEB-VERIFICATION (source it). DOCUMENTS + LIVE SOURCES WIN OVER
  MEMORY. The one thing memory may do is FLAG suspicion ("this fact looks stale") —
  which then triggers a web check, never a verdict.

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER FORMAT & MOCK-NUMBER RESOLUTION
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger formats

  PRIMARY: TestCreateAudit P[N] [--level <mock|subject|topic|subtopic>] [--scope <Subject[::Topic]>]
  RESUME : TestCreateAudit P[N] resume     (re-enter mid-audit; §4 / RA-18)
  STATUS : TestCreateAudit P[N] status     (print audit dashboard, no work)

  ALIAS (v2.9 — mock-only, working alias, unchanged behaviour):
    MockCreateAudit M[N]          == TestCreateAudit P[N] --level mock
    MockCreateAudit M[N] resume   == TestCreateAudit P[N] --level mock resume
    MockCreateAudit M[N] status   == TestCreateAudit P[N] --level mock status

  --level: cross-checked (not required) against the blueprint pp.pick_blueprint resolves
    via the uploaded docx (P0). If given and it disagrees with the docx's actual tier,
    HARD STOP. MockCreateAudit M[N] always implies level='mock'.

  ExamCode: read from exam_config.json in project knowledge; must match blueprint + registry exam_code.
  [N]       : integer ≥ 1. The mock/paper to audit. Resolution + validation in S2-2.

## S2-2 — Mock/paper-number resolution (do this BEFORE loading questions)

  N is resolved from TWO sources; both must agree:
    (a) the trigger's M[N] / P[N];
    (b) the uploaded docx filename [ExamCode]_[paper_slug]_Create.docx (v5.28: paper_slug
        is "Mock[N]" zero-padded for a mock, else the scoped pp.paper_slug — P0 parses N
        back out of whichever slug it actually is, via the matched blueprint mock entry).
  (v2.7: the paper's own title block is NO LONGER a source. Step 7 R8b / G-PREQ1 makes
   the Create.docx questions-only — the first non-blank paragraph is Q.1, so there is
   no title paragraph to read. A-HEADER now STRIPS any residual pre-Q.1 block rather than
   reading N from it. Trigger + filename are sufficient and are the two reliable sources.)
  DISAGREEMENT → HARD STOP. Print which sources disagree and ask the user to
  confirm N. A wrong N corrupts the registry re-sync (§13) and the --mockN
  self-exclusion of cross-mock dedup (§10). Never guess.

  REGISTRY ALIGNMENT (critical for §13): registry.papers_completed must END with this
  paper's paper_id (Step 7 appended it) — falling back to registry.mocks_completed
  ending with N for a legacy registry auditing a mock. If neither holds:
    HARD STOP. Print:
      "HARD STOP (S2-2): registry.papers_completed = [...] does not end with paper_id
       [paper_id]. Step 8 re-syncs the registry by rebuilding the most-recently-appended
       paper's slice; that requires the registry from the Step-7 run that generated
       this paper. Upload the registry delivered alongside this docx, then re-run."
    This catches: a stale registry, a skipped mock/paper, or auditing an out-of-order
    mock/paper — all of which would make the §13 trailing-slice rebuild unsafe.

# ════════════════════════════════════════════════════════════════════════
# §3 — SESSION START: PRE-FLIGHT (P0 … P9) — run ALL before any audit
# ════════════════════════════════════════════════════════════════════════
#   Do not parse questions, do not run gates, until every P-check passes. These
#   are integrity and provenance checks; failing one means the audit would be
#   built on sand. Each P-check is HARD STOP unless noted.

## P0 — Copy inputs to the working directory

  ```python
  import shutil, os, json, re, sys, zipfile, hashlib, glob
  EXAM = "[ExamCode]"     # from trigger
  N    = [N]              # resolved mock/paper number (S2-2)
  WORK = "/home/claude"
  PROJ = "/mnt/project"
  UPL  = "/mnt/user-data/uploads"

  def _find(name):
      """Inputs may arrive in project knowledge OR in uploads. Prefer uploads for
      the docx+registry (the freshly delivered pair); prefer project for the static
      Step-0/1 files and the audit script."""
      for base in (UPL, PROJ):
          p = os.path.join(base, name)
          if os.path.exists(p):
              return p
      return None

  def _find_glob(pattern):
      for base in (UPL, PROJ):
          hits = sorted(glob.glob(os.path.join(base, pattern)))
          if hits:
              return hits
      return []

  import paper_pipeline as pp

  # v5.28 (twin of MockTestCreate v5.28): infer WHICH blueprint (mock or scoped) this audit
  # is for from the UPLOADED docx itself, rather than assuming the single mock blueprint file.
  # 1) find the Create.docx (uploads preferred, then project); 2) parse its paper_slug from
  # the filename; 3) load every discovered blueprint; 4) pp.pick_blueprint(docx_slug=...)
  # identifies the ONE blueprint that produced it (cross-checked against --level if given).
  _docx_hits = _find_glob(f'{EXAM}_*_Create.docx')
  if not _docx_hits:
      raise SystemExit(f"HARD STOP: no {EXAM}_*_Create.docx found in uploads or project "
                       f"knowledge. Upload the Step-7 output, then retry.")
  if len(_docx_hits) > 1:
      raise SystemExit(f"HARD STOP: {len(_docx_hits)} candidate Create.docx files found "
                       f"({[os.path.basename(h) for h in _docx_hits]}) — remove the stale "
                       f"one(s), keep only the paper you're auditing.")
  _docx_path = _docx_hits[0]
  _docx_name = os.path.basename(_docx_path)
  _docx_m = re.match(rf'^{re.escape(EXAM)}_(.+)_Create\.docx$', _docx_name)
  if not _docx_m:
      raise SystemExit(f"HARD STOP: could not parse a paper_slug from docx filename "
                       f"{_docx_name!r}.")
  docx_slug = _docx_m.group(1)

  # BP_LEVEL comes from the trigger (§2 S2-1): MockCreateAudit M[N] alias -> 'mock';
  # TestCreateAudit P[N] --level X -> X; TestCreateAudit P[N] with no --level -> None.
  # NOTE: named BP_LEVEL (not LEVEL) to avoid colliding with the unrelated LEVEL =
  # cat_c('level', ...) academic-level variable assigned later at P2.

  _bp_srcs = sorted(glob.glob(os.path.join(PROJ, f'{EXAM}*_blueprint.json'))) or \
             sorted(glob.glob(os.path.join(UPL, f'{EXAM}*_blueprint.json')))
  if not _bp_srcs:
      raise SystemExit(f"HARD STOP: no {EXAM}*_blueprint.json found in project knowledge.")
  _bp_paths_by_dict = []
  for src in _bp_srcs:
      dst = os.path.join(WORK, os.path.basename(src))
      shutil.copy(src, dst)
      _bp_paths_by_dict.append((dst, json.load(open(dst, encoding='utf-8'))))
  _blueprints = [d for _, d in _bp_paths_by_dict]

  try:
      bp = pp.pick_blueprint(_blueprints, level=BP_LEVEL, docx_slug=docx_slug)
  except pp.PickError as e:
      raise SystemExit(f"HARD STOP: {e}")
  _bp_path = next(p for p, d in _bp_paths_by_dict if d is bp)

  # v2.9.1 SAFETY CHECK: the {EXAM}*_blueprint.json glob is a PREFIX match — if a
  # different ExamCode's files were ever uploaded into this project, the glob could
  # sweep one in. docx_slug matching alone is not sufficient protection: two different
  # exams could coincidentally both have a "Mock07". The exact-filename match this
  # replaced made cross-exam selection structurally impossible; the glob does not, so
  # check explicitly.
  if bp['exam_code'] != EXAM:
      raise SystemExit(
          f"HARD STOP: selected blueprint's exam_code {bp['exam_code']!r} does not "
          f"match the trigger's ExamCode {EXAM!r}. A blueprint file from a different "
          f"ExamCode may have been picked up by the {EXAM}*_blueprint.json glob — check "
          f"this project for a similarly-prefixed ExamCode's files.")

  _tp = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None)
  if _tp is None:
      raise SystemExit(f"HARD STOP (S2-2): mock/paper number {N} not found in the "
                       f"selected blueprint's mocks[].")
  paper_id   = _tp.get('paper_id', f"MOCK:M{N:02d}")   # fallback for pre-C1 blueprints
  paper_slug = pp.paper_slug(paper_id)
  if paper_slug != docx_slug:
      raise SystemExit(f"HARD STOP: uploaded docx paper_slug {docx_slug!r} does not match "
                       f"blueprint mock {N}'s paper_slug {paper_slug!r}. Wrong docx, wrong "
                       f"N, or stale blueprint — resolve before continuing.")

  REQUIRED = {
      'docx'    : f'{EXAM}_{paper_slug}_Create.docx',
      'registry': f'{EXAM}_registry.json',
      'rules'   : f'{EXAM}_section_rules.md',
      'manifest': f'{EXAM}_subtopic_manifest.json',
      'audit_py': f'{EXAM}_mock_test_audit.py',     # MANDATE A — hard stop if absent
  }
  paths = {'blueprint': _bp_path}   # already copied above
  missing = []
  for kind, name in REQUIRED.items():
      src = _find(name)
      if src is None:
          missing.append(name); continue
      dst = os.path.join(WORK, name)
      shutil.copy(src, dst)
      paths[kind] = dst
  # v2.19 — OPTIONAL Tier-A dossier (S0-1 item 7b). Absent on every pre-v5.35 mock,
  # so it is staged if present and never required. Without this staging step the
  # file would sit in uploads and never reach the auditor.
  _dos_name = f'{EXAM}_M{N}_audit_dossier.json'
  _dos_src = _find(_dos_name)
  if _dos_src:
      shutil.copy(_dos_src, os.path.join(WORK, _dos_name))
      paths['dossier'] = os.path.join(WORK, _dos_name)
      print(f"P0: Tier-A dossier staged ({_dos_name}) — will be passed to Part A "
            f"via --dossier (S5-1).")
  else:
      paths['dossier'] = None
      print(f"P0: no Tier-A dossier found ({_dos_name}) — legacy behaviour; "
            f"subtopic/qtype/image_role are re-derived or defaulted (A-DOSSIER WARN).")
  if missing:
      raise SystemExit(
          "HARD STOP (P0): missing required input(s): " + ", ".join(missing) +
          ". Upload them to the [" + EXAM + "] project / chat, then re-run. "
          "(If only the audit script is missing, see MANDATE A — it is auto-generated "
          "by Step 6 v1.20+. Verify Step 6 outputs were uploaded.)")

  # ── v2.12.1 (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D2/D3, corrected) ─────
  # ENGINES COME FROM THE VERIFIED CLONE ($FW), NOT FROM PROJECT KNOWLEDGE.
  #
  # WHY $FW AND NOT _find(). CLAUDE.md states the estate-wide rule: engines live
  # ONLY in the central repo, `/mnt/project` is DATA and never an import source,
  # and "a fix pushed to production reaches all ~200 exam projects on their next
  # clone — no per-project engine provisioning is required, and none should be
  # performed." That rule is CORRECT. It has exactly ONE mechanical exception,
  # which is this file, and which is why the A-FIGPROFILE defect existed at all:
  #
  #   Spec-inline code runs as `python3 - <<EOF` with cwd == $FW, so
  #   sys.path[0] == '' == cwd == $FW, and a bare `import blueprint_core`
  #   RESOLVES. This is every other engine consumer in the framework.
  #
  #   The auditor is DIFFERENT: it is a standalone .py executed as
  #   `python3 /home/claude/[ExamCode]_mock_test_audit.py`. Python sets
  #   sys.path[0] to the SCRIPT'S OWN DIRECTORY, not the cwd — so /home/claude
  #   goes on the path and $FW does NOT, even when cwd is $FW. Verified
  #   empirically, both cases. That single exception is the whole reason the
  #   engines had to reach /home/claude somehow.
  #
  # Copying them from $FW closes it WITHOUT provisioning anything per-exam: the
  # clone is fresh, hash-tracked and bootstrap-verified at Step 0 of every
  # session, so the engines are always current by construction. Sourcing them
  # from project knowledge instead would create a SECOND, unverified copy per
  # exam that can silently go stale — reintroducing exactly the generator/auditor
  # drift that the v2.10 delegation to blueprint_core existed to prevent.
  #
  # GATE-SCOPED, NOT AUDIT-SCOPED — a WARN, never a HARD STOP. BARE names are
  # mandatory: they are imported as Python modules and an [ExamCode]_ prefix
  # breaks `import blueprint_core` and silently disables the gates.
  FW = os.environ.get('FW', '/tmp/fw')      # the Step-0 clone; always present
  ENGINES = ['blueprint_core.py', 'figural_core.py']   # BARE names — do NOT prefix
  engines_missing = []
  for eng in ENGINES:
      src = os.path.join(FW, eng)
      if not os.path.exists(src):
          # Fallback ONLY if the clone is somehow unavailable. A project/upload
          # copy is UNVERIFIED and may be stale — usable, but say so.
          src = _find(eng)
          if src is None:
              engines_missing.append(eng); continue
          print(f"WARN (P0): {eng} not found in the verified clone ({FW}); using an "
                f"UNVERIFIED copy from project knowledge/uploads. It may be stale — "
                f"prefer re-running Step 0 so the clone is present.")
      shutil.copy(src, os.path.join(WORK, eng))
  if engines_missing:
      print("WARN (P0): repo engine(s) unavailable: "
            + ", ".join(engines_missing) + ". The audit WILL still run and WILL "
            "complete — the dependent gates report an explicit WARN skip rather "
            "than running. Affected: blueprint_core -> A-FIGPROFILE; figural_core "
            "-> the 12 A-FIG* conformance gates. Re-run Step 0 to restore the "
            "clone, then re-run, to obtain FULL gate coverage. Record this in "
            "session_log and §R13/§19 as reduced coverage.")
  ```

  RUN DIRECTORY IS NORMATIVE (v2.12). The auditor MUST be executed with
  /home/claude as the current working directory, so that sys.path[0] resolves the
  engines copied above. Running it from elsewhere silently loses them, which is
  how two audits of the same paper could previously print different gate counts —
  a §R15 reproducibility break.

## P0.5 — INPUT INTEGRITY (corruption / truncation) — HARD STOP unless repairable

  P0 catches MISSING inputs; P0.5 catches CORRUPT / TRUNCATED ones. Observed in the
  wild: large files synced through project-knowledge size caps arrive truncated
  (a 195 KB blueprint cut mid-object; a registry cut to 305 bytes; the audit.py cut
  mid-function while --self-test still printed PASS). A bare json.load on a truncated
  file throws an ugly traceback, not a clean stop; a file truncated exactly at an
  object boundary can even load and LOOK valid while being incomplete. So P0.5 checks
  parseability AND required-key presence, for each copied input:

  ```python
  import ast
  REQUIRED_KEYS = {
      'blueprint': ['exam_code', 'total_questions', 'sections', 'mocks'],
      'registry' : ['exam_code', 'mocks_completed', 'stem_texts'],
      'manifest' : ['exam_code'],
  }
  integrity_fail = []
  for kind in ('blueprint', 'registry', 'manifest'):
      p = paths[kind]
      try:
          obj = json.load(open(p, encoding='utf-8'))
      except Exception as e:
          integrity_fail.append(f"{os.path.basename(p)}: JSON parse failed ({e})")
          continue
      for k in REQUIRED_KEYS[kind]:
          if k not in obj:
              integrity_fail.append(f"{os.path.basename(p)}: required top-level key "
                                    f"{k!r} missing (likely truncated)")
  # section_rules must be non-empty AND contain the EXAM_STRUCTURE header block
  # (the on-disk literal token written by Step 5 write_section_rules(); this block is
  # referred to as "CATEGORY C" ONLY in spec prose/comments -- never search for that
  # phrase as literal file content, see Framework_MockTestAnalyse.md §14):
  try:
      rt = open(paths['rules'], encoding='utf-8').read()
      if len(rt) < 200 or not re.search(r'===\s*EXAM_STRUCTURE\s*===', rt, re.I):
          integrity_fail.append(f"{os.path.basename(paths['rules'])}: empty or missing "
                                f"EXAM_STRUCTURE header block (likely truncated)")
  except Exception as e:
      integrity_fail.append(f"section_rules read failed ({e})")
  # audit.py must ast.parse (a mid-function truncation is a SyntaxError) AND pass the
  # HARDENED fixture self-test (P1) — the self-test alone is not enough because a
  # constant-print stub parses AND prints PASS; ast.parse catches the truncated body,
  # P1 catches the hollow body.
  try:
      ast.parse(open(paths['audit_py'], encoding='utf-8').read())
  except SyntaxError as e:
      integrity_fail.append(f"{os.path.basename(paths['audit_py'])}: ast.parse "
                            f"SyntaxError line {e.lineno} (truncated/corrupt script)")

  # v2.12 — ENGINE INTEGRITY. Separate list: a truncated ENGINE is NOT an
  # audit-scoped blocker. blueprint_core.py is ~168 KB — squarely inside the range
  # where project-knowledge size caps have been observed to truncate files, which
  # is the exact failure mode P0.5 exists for. A truncated engine raises
  # SyntaxError on import; the v2.12 guards catch it and report a skip, so the
  # audit still completes. Report it, repair it if you can, never halt for it.
  engine_degraded = []
  for eng in ENGINES:
      ep = os.path.join(WORK, eng)
      if not os.path.exists(ep):
          continue                      # already WARNed at P0
      try:
          ast.parse(open(ep, encoding='utf-8').read())
      except SyntaxError as e:
          engine_degraded.append(f"{eng}: ast.parse SyntaxError line {e.lineno} "
                                 f"(truncated — re-upload from the repo)")
  if engine_degraded:
      print("WARN (P0.5 / A-INTEGRITY-ENGINE): " + "; ".join(engine_degraded) +
            ". SANCTIONED REPAIR policy (b) applies: engines are reconstructible "
            "VERBATIM from the framework repo, so re-copying an intact engine is "
            "always safe. Log to session_log.inputs_repaired[] and disclose in "
            "§R13. If it cannot be repaired, the dependent gates report a WARN "
            "skip and the audit still completes with reduced coverage.")

  if integrity_fail:
      # POLICY (a) DEFAULT → HARD STOP (code A-INTEGRITY). A truncated blueprint/registry
      # silently breaks allocation checks (§6-4) and the re-sync (§13) — auditing against
      # it is auditing against sand.
      # POLICY (b) SANCTIONED REPAIR is permitted for [ExamCode]_mock_test_audit.py
      # (regenerate from audit_canonical.py / Step 6 B3 — §21) and, from v2.12, for
      # ANY REPO ENGINE copied into the project (blueprint_core.py, figural_core.py)
      # — all are reconstructible VERBATIM from the hash-tracked repo, so a repair
      # is a byte-exact restore and never a guess. Permitted ONLY when the repaired
      # script then passes the hardened self-test (P1). Log it to
      # session_log.inputs_repaired[] and disclose in §R13. NEVER silently repair
      # blueprint/registry DATA — its content is not reconstructible and a guess corrupts
      # every downstream gate. (If only mock N's own slice of a large blueprint is intact
      # and reachable, auditing MAY proceed against that slice ONLY with an explicit §R13
      # limitation and the missing-data hard-stop for any gate that needs the truncated
      # part.)
      audit_py_only = all('mock_test_audit.py' in f for f in integrity_fail)
      if audit_py_only:
          # regenerate the canonical script (§21) → re-run P0.5 + P1; proceed only if clean.
          raise SystemExit("A-INTEGRITY (P0.5): [ExamCode]_mock_test_audit.py is corrupt/"
                           "truncated. SANCTIONED REPAIR: regenerate the canonical auditor "
                           "(Appendix A / Step 6 B3), re-upload, re-run. Log to "
                           "session_log.inputs_repaired[].")
      raise SystemExit("HARD STOP (P0.5 / A-INTEGRITY): corrupt/truncated input(s): "
                       + "; ".join(integrity_fail) +
                       ". Re-upload the INTACT file(s); never audit against truncated "
                       "blueprint/registry data.")
  ```

## P0.5C — CHECKPOINT REHYDRATION (v2.15 / C1) — `resume` ONLY

  Runs on a `resume` trigger, AFTER P0/P0.5 (the auditor must self-test before it
  is trusted to verify a bundle) and BEFORE P1..P9. Skipped entirely on a fresh
  run — P6..P9 then build the state from scratch exactly as before.

  ```python
  import glob, subprocess, os
  RESTORE = os.path.join(WORK, f'{EXAM}_M{N}_restored')
  _cks = sorted(glob.glob(os.path.join(UPL, f'{EXAM}_M{N}_audit_checkpoint.zip'))) or \
         sorted(glob.glob(os.path.join(UPL, '*_audit_checkpoint.zip')))
  if not _cks:
      print("RESUME: no checkpoint uploaded. /home/claude does not survive a session "
            "boundary, so there is no state to resume from — restarting at Phase 1. "
            "NEVER reconstruct a ledger from memory to satisfy S5-1A (§19).")
      RESUMED = False
  else:
      r = subprocess.run(['python3', paths['audit_py'], paths['docx'],
                          '--mockN', str(N),
                          '--restore-checkpoint', _cks[-1], '--into', RESTORE],
                         capture_output=True, text=True)
      print(r.stdout.strip() or r.stderr.strip())
      if r.returncode != 0:
          raise SystemExit(
              "HARD STOP (P0.5C): checkpoint REFUSED — see the reason above. Do NOT "
              "improvise a partial resume: restore is all-or-nothing precisely so a "
              "half-restored state can never be mistaken for a complete one. Either "
              "upload the correct checkpoint for THIS paper, or re-run without "
              "`resume` to audit from Phase 1.")
      RESUMED = True
      audit_state_path = os.path.join(RESTORE, 'audit_state.json')
  ```
  On success the ledger, the batch plan, batches_done and the whole evidence tree
  are back, with every recorded evidence path rebased to the restored directory.
  P8 does NOT recompute the batch plan (it is in the restored state) and P9 does
  NOT re-initialise the ledger — both are reloaded (RA-18). Phase 2 resumes at the
  first batch not in batches_done; already-reviewed questions are NOT re-reviewed;
  the whole-paper Part A still runs for each resumed batch (RA-7).

## P3.5 — VISION PROBE (v2.16 / D4) — MANDATORY, NEVER A HARD STOP

  WHY. Pre-flight validated engines, JSON integrity, ZIP/rId, encoding, block count,
  sequence, monotonicity and ran a 97-fixture self-test — and then the audit failed on
  a dependency NEVER CHECKED AT ALL. §3 treated vision as ambient despite RA-4 making
  it load-bearing for C6/C7 and therefore for delivery. This converts a two-day
  discovery into a one-minute fact, and it is the cheapest change in this release.

  ```bash
  # 1) render the probe card (3 random glyphs; expected value stored ONLY as a
  #    salted sha256, so the sidecar reveals nothing)
  python3 /home/claude/[ExamCode]_mock_test_audit.py /home/claude/[paper].docx \
      --vision-probe /home/claude/[ExamCode]_M[N]_evidence --batch [b]
  # 2) VIEW evidence/montages/_probe.png, then report what you actually saw
  python3 /home/claude/[ExamCode]_mock_test_audit.py /home/claude/[paper].docx \
      --vision-probe-verify /home/claude/[ExamCode]_M[N]_evidence \
      --glyphs [what you saw] --batch [b] \
      --audit-state /home/claude/[ExamCode]_M[N]_audit_state.json
  ```

  • `VISION-PROBE: OK`        → normal operation for this batch.
  • `P3.5 VISION PROBE FAILED` → §7 Layer-B viewing is unavailable. The audit RUNS and
    DELIVERS; every figural item audited under this outage carries 'view-unavailable'
    and the paper certifies CERTIFIED-DEGRADED (VISION) with an F1 AMBER footer.
    **NOT a hard stop.**
  • `P3.5-RENDER-FAIL`         → ENVIRONMENT WARN only (E4.5). Inferring an outage from
    "we could not draw the test card" would degrade a healthy run. NEVER a vision
    verdict.

  RUN IT AT PRE-FLIGHT **AND AT THE START OF EVERY PHASE-2 BATCH**, recording the
  result per batch. A mid-run transition in EITHER direction is expected and must be
  captured — the incident that motivated this release had Batch 1 healthy and Batch 2
  not, so a start-of-session probe alone would have missed it. Two failed attempts on
  distinct paths constitute FAILED for that batch; no flapping (E4.3). If vision
  RECOVERS, every prior 'view-unavailable' MUST be re-attempted and upgraded before
  Phase 3 — C6 FAILS otherwise (E2.3). A paper with zero images still runs the probe
  and records the result, but it is non-blocking and not reported in §R13 (E4.4).

## P1 — Audit-script self-test (MANDATE A) — HARDENED (v2.6)

  ```
  python3 /home/claude/[ExamCode]_mock_test_audit.py --self-test
      → MUST print  "SELF-TEST: N/N PASS"  where:
          • N >= AUTH_GATE_FLOOR (currently 35 — the Appendix A authoritative count), AND
          • the self-test is FIXTURE-BASED: it builds tiny docx fixtures and asserts
            each gate CATCHES a planted defect and PASSES a clean fixture
            (Appendix A self_test()), AND
          • it includes the C1–C7 completion-gate fixtures (S5-1A).
  ```
  REJECTED — HARD STOP (each yields false-clean audits):
    • a CONSTANT-PRINT self-test that prints PASS without executing any gate
      (e.g. the minimum-viable 13-gate stub: `def self_test(): print("SELF-TEST:
      13/13 PASS"); return 0`). No longer acceptable — MANDATE A must guarantee a
      WORKING auditor, not a file that prints "PASS".
    • N < AUTH_GATE_FLOOR (a reduced/stub gate set).
    • any traceback / FAIL / non-zero exit.
    • a body that ast-parses (P0.5) but whose gates raise at runtime — caught here
      because the fixture self-test actually INVOKES them (a truncated/regex-broken
      body that still prints a hollow PASS is exactly what slipped through in v2.5).
  On any REJECT → HARD STOP: regenerate/replace with the canonical auditor — copy
  the repo engine `audit_canonical.py` from the Step-0 verified clone (Step 6 B3
  does the same; §21). The former "Framework_MockTestCreate.md Appendix A" route is
  DEAD: that file has carried no auditor fence since v2.11.2 and only points here
  (third and last instance retired at v2.12.1). NEVER audit with a script that
  fails the hardened self-test: a broken/hollow gate gives false-clean results.

## P2 — Load + validate the source files

  ```python
  blueprint = json.load(open(paths['blueprint'], encoding='utf-8'))
  registry  = json.load(open(paths['registry'],  encoding='utf-8'))
  manifest  = json.load(open(paths['manifest'],  encoding='utf-8'))
  rules_txt = open(paths['rules'], encoding='utf-8').read()

  # exam_code coherence (RS-5):
  for nm, obj in (('blueprint', blueprint), ('registry', registry), ('manifest', manifest)):
      if obj.get('exam_code') != EXAM:
          raise SystemExit(f"HARD STOP (P2): {nm}.exam_code="
                           f"{obj.get('exam_code')!r} != trigger {EXAM!r}.")

  # blueprint readability for mock N (Step 7 S3-2 structure):
  total_questions = blueprint['total_questions']
  sections        = blueprint['sections']                  # [{name,q_range,total_qs,max_attempt}]
  # v2.1: new fields from Step 6 v1.19 (exam_config v2.5 contract).
  # Read for availability; no new audit gates — structural metadata, not auditable content.
  bp_marking_scheme = blueprint.get('marking_scheme', [])
  bp_level          = blueprint.get('level', 'unknown')
  bp_medium         = blueprint.get('medium', 'unknown')
  # v2.5 THREE-AXIS: per-section format-distribution target + window params. Absent-safe:
  # a pre-v1.23 blueprint has no axis_schedule → {} → the whole Axis audit (S6-6) stays inert.
  axis_schedule   = blueprint.get('axis_schedule', {})
  AXIS_WINDOW     = blueprint.get('batch_size_qs', 10)          # mocks per window (== Step 6/7)
  TOTAL_MOCKS     = blueprint.get('total_mocks')                # for last-partial-window close
  mock_obj = next((m for m in blueprint['mocks'] if m['mock'] == N), None)
  if mock_obj is None:
      raise SystemExit(f"HARD STOP (P2): blueprint.mocks has no entry for mock {N}.")
  alloc = {}   # subtopic_id -> q_count (blueprint truth for this mock)
  for sec in mock_obj['sections']:
      for a in sec['subtopic_allocations']:
          alloc[a['subtopic_id']] = a   # carries q_count, format, type, names

  # CATEGORY-C exam params (auto-detected by Step 0; NEVER hardcoded here):
  def cat_c(key, default=None):
      m = re.search(rf'^\s*{re.escape(key)}\s*[:=]\s*(.+?)\s*$', rules_txt, re.M)
      return m.group(1).strip() if m else default
  LANGUAGE        = (cat_c('language', 'english') or 'english').lower()
  OPTIONS_COUNT   = int(cat_c('options_count', '4'))
  MARKS_PER_Q     = cat_c('marks_per_q')           # dict-ish string; parsed if header check needs it
  NEG_MARKING     = cat_c('negative_marking', '0')
  TIME_PER_Q_SEC  = cat_c('time_per_q_sec')
  OPTION_LABEL_FMT= cat_c('option_label_format', '1/2/3/4')   # CATEGORY-A may override per section
  # v2.1: new CATEGORY C fields from Step 5 v2.18
  MARKING_SCHEME  = cat_c('marking_scheme', '[]')  # per-range scoring rules (string repr of list)
  LEVEL           = cat_c('level', 'unknown')       # academic level
  MEDIUM          = cat_c('medium', 'unknown')      # exam language
  ```
  VALIDATE: total_questions > 0; sections non-empty and contiguous (q_ranges tile
  [1..total_questions] with no gap/overlap); difficulty_schedule has an entry for N
  whose simple+medium+hard == total_questions. Any failure → HARD STOP (corrupt
  blueprint; do not audit against a broken plan). (P0.5 already caught a TRUNCATED
  blueprint; this catches a STRUCTURALLY INCOHERENT one.)

## P3 — Open the docx + ZIP/rId/encoding integrity (A-ZIP, A-ENCODING)

  ```python
  docx = paths['docx']
  if os.path.getsize(docx) < 50_000:
      print("P3 WARN: docx < 50 KB — unusually small for a full paper; verify N.")
  with zipfile.ZipFile(docx) as z:
      names = set(z.namelist())
      assert 'word/document.xml' in names, "P3 HARD STOP: word/document.xml missing."
      doc_xml = z.read('word/document.xml').decode('utf-8', 'replace')
      rels = z.read('word/_rels/document.xml.rels').decode('utf-8') \
             if 'word/_rels/document.xml.rels' in names else ''
      # every r:embed / r:id referenced in document.xml must resolve in rels AND
      # point to a part that physically exists in the ZIP:
      ref_ids = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', doc_xml))
      rel_map = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
      for rid in ref_ids:
          tgt = rel_map.get(rid)
          if tgt is None:
              raise SystemExit(f"HARD STOP (P3/A-ZIP): rId {rid} unresolved in rels.")
          part = ('word/' + tgt) if not tgt.startswith(('http', '/')) else tgt
          if not tgt.startswith('http') and part.replace('word/../','') not in names \
             and ('word/'+tgt.replace('../','')) not in names:
              raise SystemExit(f"HARD STOP (P3/A-ZIP): rId {rid} → {tgt} not in ZIP.")
      # U+FFFD replacement char (encoding corruption) — ALWAYS a defect (RA-10):
      if '�' in doc_xml:
          print("P3/A-ENCODING: U+FFFD replacement char(s) present → flagged for "
                "rectification (encoding corruption).")
  ```
  A-ZIP failures are HARD (a paper with a dangling image rId is structurally
  broken). A-ENCODING (U+FFFD) is recorded as a defect to RECTIFY in Phase 1
  (regenerate the affected run/question), not a hard stop.

## P4 — Extract the embedded maps from the registry (the Step-8 analogue of T2 S3b)

  P4 NOTICE — EC-V18 LEGACY FIGURES (v2.18 / D8). Emit BEFORE Phase 1 whenever
  figural questions are present and registry figure_specs is empty or partial. The
  status was previously discovered mid-audit, after full pre-flight had run, when the
  author had already committed hours to a paper they might have preferred to
  regenerate.

  ```python
  _fs = figure_specs or {}
  _nfig = len(figural_qs)
  if _nfig and not _fs:
      print(f"P4 NOTICE (EC-V18): this paper carries 0 FigureSpec sidecars for {_nfig} "
            f"figural question(s) — it predates Step 7 v5.34. The twelve figure-"
            f"conformance gates will evaluate only their PIXEL-side half. This paper "
            f"CAN be certified but WILL ship with an AMBER footer and a permanent §R13 "
            f"limitation. If you intend to regenerate on Step 7 v5.34+, DO SO BEFORE "
            f"AUDITING — a regenerated paper invalidates this audit entirely.")
  elif _nfig and len(_fs) < _nfig:
      print(f"P4 NOTICE (EC-V18, PARTIAL): {len(_fs)}/{_nfig} figural question(s) carry "
            f"a FigureSpec. Degradation is PER FIGURE, not per paper — the covered "
            f"figures are audited in full.")
  ```
  E8.3: suppressed entirely when the paper has no figures.

  ```python
  # RC / cloze map for this mock (drives A-STIMORPHAN linked-group completeness):
  rc_entry = next((m for m in registry.get('rc_manifests', []) if m.get('mock') == N), None)
  passage_linked = set(rc_entry['passage_linked']) if rc_entry else set()
  cloze_linked   = set(rc_entry['cloze_linked'])   if rc_entry else set()
  # Figural map for this mock (drives A-FIGCOMP + §7 image audit coverage):
  fig_entry = next((m for m in registry.get('figural_manifests', []) if m.get('mock') == N), None)
  figural_qs = set(int(q) for q in fig_entry['figural_qs']) if fig_entry else set()
  # v2.13 (GAP-2026-08-01-FIGSPEC-TRANSPORT D2): the FigureSpec records Step 7 v5.34
  # carried into the registry, keyed by canonical PNG name ("q7_problem.png"). These
  # are the twelve figure-conformance gates' only non-pixel input. Absent on every
  # pre-v5.34 paper -> {} -> every figure reads legacy -> EC-V18 (audit completes,
  # reports loudly, delivery not blocked). NEVER hardcode a substitute (RA-9).
  figure_specs = (fig_entry.get('figure_specs') or {}) if fig_entry else {}
  # NOTE: registry image_hashes for the mock may be EMPTY (observed in the wild);
  #   §7/§10 therefore HASH word/media/ directly rather than trusting registry hashes.

  # v2.5 THREE-AXIS: window-level state (cross-mock; batch_state is per-mock in Step 7 too).
  #   registry.axis2_window : Step 7's SELF-REPORTED counts (what it declared it rendered).
  #   registry.axis2_audit  : Step 8's OWN INDEPENDENT tally, re-derived from each mock's docx.
  # Both key the current 10-mock window. Load Step 8's tally with a window-aware reset so a new
  # window starts from zero; mock N's re-derived counts are added at Phase 3 (from the FIXED docx).
  _cur_window       = (N - 1) // max(1, AXIS_WINDOW)
  s7_axis_window    = registry.get('axis2_window', {})          # Step 7's counts (for the drift WARN)
  _reg_audit        = registry.get('axis2_audit', {})
  if _reg_audit.get('window') != _cur_window:
      axis2_audit_sections = {}                                  # new window → fresh independent tally
      axis2_audit_mocks    = []                                  # mocks counted this window (idempotency)
  else:
      axis2_audit_sections = dict(_reg_audit.get('sections', {}))
      axis2_audit_mocks    = list(_reg_audit.get('mocks', []))
  # axis2_audit_sections[section] = {'axis1':{cls:n}, 'axis2':{cls:n}, 'axis3':{cls:n},
  #                                  'neg':int, 'total':int}  — accumulated across the window.
  ```
  These maps are a STARTING POINT, not gospel: §6/§7 re-derive linked groups and
  figural questions from the paper's own cues as a backstop (a question that
  references a stimulus but is absent from the manifest is itself a defect).

## P5 — Pre-Q.1 body-block check (A-HEADER — questions-only paper, v2.7)

  The generated paper is questions-only (Step 7 R8b / G-PREQ1): the FIRST non-blank body
  paragraph MUST be the bold "Q.1" stem. Read the paragraphs before Q.1 (this is
  structural metadata, not question content; MANDATE 0 permits reading it, never printing
  stems). Then:
    • ZERO non-blank paragraphs before Q.1 → A-HEADER PASS (questions-only).
    • ANY non-blank paragraph before Q.1 — a title ("... Mock Test [N] ..."), a
      "Total Questions / Maximum Marks / Time" line, an "Each question carries ...
      Negative marking ..." instruction, or any cover/preamble → A-HEADER DEFECT →
      STRIP the entire pre-Q.1 block in Phase 1 (CP-HEADER-STRIP). This is a
      content-preserving fix (the block is not question content), so it stays in Phase 1
      and never escalates to Phase 2.
  There is NO figure-checking: CATEGORY-C values (marks_per_q, time_per_q_sec,
  negative_marking, options_count, total_questions) are STRUCTURED METADATA in
  section_rules.md / blueprint.json / registry — they are NEVER printed in the paper, so
  there is nothing in the paper to reconcile against them; a downstream platform may
  render them from that metadata.
  Blank separator paragraphs before Q.1 are ignored (not a defect).
  DORMANT (exam-agnostic opt-in): if — and only if — section_rules.md EXAM_STRUCTURE
  declares `paper_header_block`, a printed header is permitted and A-HEADER does not fire.
  No current section_rules.md declares it, so the ban is absolute for every present exam.
  This is the Step-8 independent re-verification of Step 7 R8b / G-PREQ1.

## P6 — Build the question-block index (document-order parse; the audit's spine)

  Parse the docx body (paragraphs AND tables interleaved, in true document order)
  into per-question BLOCKS. A block = the opening "Q.<n>" paragraph through the
  paragraph/table/image immediately before the next "Q.<n>" paragraph. For each
  block record (no content leaves /home/claude): qnum; section (by q_range);
  the items trailing the last option of the block (used to detect a stimulus
  orphaned before the NEXT block's Q.<n> — the observable form of an A-QNFIRST
  violation, since the parser starts each block AT its Q.<n>); option paragraphs;
  attached tables; attached inline images (with their part names + media files);
  whether the stem carries OMML (<m:oMath>); whether any run carries <w:u>; the
  stem's structural cues (linked-stimulus references, escape-option references,
  underline references, math triggers). This index is written to
  /home/claude/[ExamCode]_M[N]_blockindex.json and is the input to Part A, Part B,
  and §7. OMML/text extraction MUST merge <m:t> (math) with <w:t> (text) — a stem
  that is pure OMML is BLANK in p.text and must never be judged "empty" (RA-4).

## P7 — Coverage cross-check (no question silently lost)

  assert len(blocks) == total_questions, else HARD STOP (A-COUNT pre-check): the
  paper does not contain blueprint.total_questions question blocks. Confirm the
  block q-numbers are exactly {1..total_questions} (A-SEQ pre-check) and strictly
  increasing in document order (A-MONO pre-check). These are re-asserted by the
  machine script in Phase 1; here they gate whether the index is even usable.

## P8 — Compute the BATCH PLAN once (possible because the whole paper is visible)

  Walk q = 1..total_questions, filling batches up to AUDIT_BATCH_SIZE (default 10).
  ATOMIC LINKED GROUPS (RA-16): a linked group (from passage_linked / cloze_linked /
  di groups / re-derived puzzle sets) is never split — if adding the next group
  would overflow the current batch, CLOSE the batch before the group and start the
  group in a fresh batch. The only batch permitted to exceed the cap is a single
  group larger than the cap (it becomes its own batch). Persist the plan to
  /home/claude/[ExamCode]_M[N]_audit_state.json (RA-18). K = number of batches.
  K is derived from the paper — never hardcoded — so a 100-Q paper and a 200-Q
  paper simply yield different K (fully exam-agnostic). K is the value the Phase-3
  completion gate asserts against batches_done (S5-1A C1).

## P9 — Initialise the audit ledger + the derived-key store + the evidence dir (§9, §11)

  Create /home/claude/[ExamCode]_M[N]_audit_state.json with:
    {mock:N, K:<from P8>, plan:[...], batches_done:[],
     evidence_dir: "/home/claude/[ExamCode]_M[N]_evidence",
     ledger:{entries:{}, scenarios:[], presentations:[], facts:[], vocab:[],
             images:[], derived_key:{}, fact_cache:{}},   # v2.14 B3 (RA-11 b)
     defects:[], regenerations:[], stamps:{},
     session_log:{inputs_repaired:[]}}
  And create the evidence directory with subfolders (RA-19 / §7 / S5-1A):
    /home/claude/[ExamCode]_M[N]_evidence/montages/    — §7 image montages (VIEW proof)
    /home/claude/[ExamCode]_M[N]_evidence/facts/       — saved B-FACT search results
    /home/claude/[ExamCode]_M[N]_evidence/recompute/   — table/matrix/chart/OMML traces
  On a `resume` trigger the audit_state file is RELOADED (RA-18): nothing already
  reviewed is re-reviewed; nothing is forgotten; the evidence dir persists so its
  files still satisfy S5-1A at Phase 3.

  PRE-FLIGHT COMPLETE → print the dashboard (§15 short form) and BEGIN PHASE 1.

# ════════════════════════════════════════════════════════════════════════
# §4 — AUDIT ARCHITECTURE (three phases; the continue contract)
# ════════════════════════════════════════════════════════════════════════

## S4-1 — The three phases (overview)

  PHASE 1 — Whole-paper machine sweep + content-preserving fixes   (ONE response)
  PHASE 2 — Batched semantic + visual audit & rectification        (K responses,
                                                                    continue-gated
                                                                    interactively;
                                                                    sequential in
                                                                    autonomous mode)
  PHASE 3 — Final certification + registry re-sync + delivery      (auto; no continue)

  The split is forced by the core principle: machine gates are whole-paper by
  nature (Phase 1, and re-run inside every Phase-2 batch); semantic/visual review
  and regeneration are expensive and are batched (Phase 2); certification is whole-
  paper and last (Phase 3). PHASE 2 IS NEVER SKIPPED OR COLLAPSED (MANDATE B).

## S4-2 — PHASE 1 — whole-paper machine sweep (ONE response, no continue)

  STEP 1. Pre-flight §3 (P0–P9). If any HARD STOP fired, stop here.
  STEP 2. Run Part A (§5) over the ENTIRE docx → the global machine-defect map.
          Append the script STDOUT to the response (it is MANDATE-0 safe — codes
          + Q-numbers only).
  STEP 3. Apply ALL content-preserving fixes (§8 class CP) in one pass. These do
          NOT change which option is correct, so they are safe paper-wide and need
          no per-question re-solve:
            CP-FONT (→Calibri 11), CP-OPTLABEL (→option_label_format), CP-SECHDR
            (strip body section headers), CP-QNFIRST (re-emit block Q.N-first),
            CP-UNDERLINE (real <w:u> run; drop "(underlined: X)"), CP-MATHOMML
            (re-render built-up math as OMML; drop the raster/ASCII), CP-STIMEMBED
            (embed the shared stimulus into every linked member, Model A),
            CP-FIGDECOMP (decompose a composite figural panel into problem +
            per-option images — re-render under §7/Step-7 S10-8), CP-IMGNAME
            (rename mis-named legitimate figures to the canonical q{N}_* contract),
            CP-BLANKSEP (insert missing blank separators), CP-ENCODING (repair
            U+FFFD runs), CP-HEADER-STRIP (delete any non-blank paragraph before Q.1 —
            the paper is questions-only; Step 7 R8b / G-PREQ1).
          A fix that CANNOT be done without changing content (e.g. a figural panel
          whose underlying figure is wrong, not merely composited) is DEFERRED to
          Phase 2 as a content defect (§8 class RG) and only TAGGED here.
  STEP 4. Re-run Part A → confirm every machine gate that was content-preserving-
          fixable is now green. Remaining Part A FAILs are content defects to be
          resolved in Phase 2 (recorded in audit_state.defects with their batch).
  STEP 5. Print the Phase-1 summary (§15): gates fixed, gates still open (by code +
          Q-number), and the batch plan (K batches). Stage NOTHING to outputs
          (MANDATE D). Save the WIP docx + audit_state to /home/claude.
  STEP 6. INTERACTIVE mode: print "Phase 1 complete. Type 'continue' to begin
          semantic Batch 1 of K." and END THE RESPONSE. (RA-15b; interactive mode.
          AUTONOMOUS mode (S4-3A): no stop — fall straight into Batch 1; the review
          still runs for every question, RA-15a.)

  WHY mechanical fixes go first: when Phase 2 reads a question it then reads a
  STRUCTURALLY CLEAN block — it reviews the real OMML expression (not a raster),
  the embedded passage (not an orphan reference), the decomposed option images
  (not a baked panel). Semantic review is only meaningful on a structurally sound
  block.

## S4-3 — PHASE 2 — semantic + visual batch (≤ AUDIT_BATCH_SIZE Q; continue-gated)

  INTERACTIVE mode: triggered by "continue" / "go" / "next" (case-insensitive). Any
  other user message → answer it, then re-print "Type 'continue' to begin Batch [b]
  of K." (RA-15b; interactive. Claude NEVER auto-advances a Phase-2 batch
  interactively. AUTONOMOUS mode advances without the pause — S4-3A — but never
  skips a question, RA-15a.)

  For batch b (its q-list from the P8 plan):
    STEP A — SEMANTIC REVIEW (§6), every question in the batch, zero sampling:
       solve it (§11 B-SOLVE); verify exactly one defensible answer (B-UNIQUE);
       verify each distractor indefensible (B-DISTRACT); verify stem↔option
       coherence + escape-option coherence (B-STEMOPT / B-OPTREF-SEM);
       web-verify every CA/static-GA fact + factual option (B-FACT) AND SAVE each
       result to the evidence dir facts/ (RA-11); verify passage/cloze derivability
       (B-PASSAGE); record findings + a STAMPED ledger entry per question (§9-1).
    STEP B — VISUAL / STRUCTURED DEEP AUDIT (§7) for every image/table/matrix/
       chart/OMML in the batch: VIEW every image (save the montage PNG to the
       evidence dir montages/); PARSE + RECOMPUTE every table/matrix/chart and
       every OMML expression (save the recompute trace to recompute/). (RA-4/RA-19)
    STEP C — RECTIFY (§8): mechanical leftovers in place; content defects by
       REGENERATING that question under Step-7 contracts (RA-6); re-audit each
       regenerated/fixed question immediately (it is not "done" while it carries an
       unreviewed change). Diff every regeneration against the WHOLE ledger (§9) and
       the registry (§10) — not just this batch.
    STEP D — WHOLE-PAPER Part A re-run (RA-7): catch any GLOBAL perturbation this
       batch's fixes introduced (new answer-run, new dup, drifted count, new
       orphan). Resolve it before the batch ends.
    STEP E — Persist audit_state (ledger, defects, regenerations, stamps, evidence
       paths, WIP docx) to /home/claude (RA-18). Append b to batches_done. Stage
       NOTHING to outputs EXCEPT the S4-7 checkpoint, which is not a delivery
       (MANDATE D carve-out) and is written AFTER batches_done is appended so the
       bundle always reflects completed work only.
    STEP F — Print the batch report (§15): whole-paper Part A status; this batch's
       findings by Q-number + code; running totals (reviewed / fixed / regenerated).
    STEP G — If b < K: INTERACTIVE — print "Type 'continue' to begin Batch [b+1] of
             K." and END (RA-15b; interactive, one batch = one response). AUTONOMOUS
             (S4-3A) — proceed to Batch b+1 in the same session (no pause), still one
             batch processed at a time internally with its whole-paper Part A re-run.
             If b == K: do NOT wait — fall straight into PHASE 3 (RA-15b / Step 7 R24)
             in BOTH modes.

## S4-3A — AUTONOMOUS (headless) mode  (PACING WAIVER ONLY — RA-15b)

  TRIGGER: the user or a project-memory preference requests non-interactive /
  end-to-end / "don't pause" / "no-blocker-surfacing" execution, OR the run is
  scheduled/headless.

  EFFECT (PACING ONLY — RA-15b): Phase 1 does NOT stop for "continue"; Phase-2
  Batches 1..K run SEQUENTIALLY within the one session with no inter-batch pause;
  Phase 3 auto-runs. The per-batch structure (STEP A..G of S4-3) is UNCHANGED —
  batches are still processed one at a time internally, each with its whole-paper
  Part A re-run (RA-7) and its ledger + evidence writes; only the human "continue"
  gate is removed.

  UNCHANGED (RA-15a — HARD): every question is audited (zero sampling, RA-3); every
  §6 and §7 check runs and SAVES its evidence; audit_state.ledger gets one stamped
  entry per question; the Phase-3 COMPLETION GATE (S5-1A) MUST pass before
  present_files. NO preference may waive any of this (RA-0).

  Autonomous mode changes WHEN work is reported, never WHETHER work is done. A run
  that finishes "fast" because it collapsed Phase 2 is a MANDATE B violation, not a
  valid autonomous run — and S5-1A will FAIL it (C1/C2) at Phase 3. Report all K
  batch summaries in sequence in the final output.

## S4-4 — PHASE 3 — certification + re-sync + delivery (auto; no continue)

  Runs automatically after the last Phase-2 batch is clean.
    STEP 1. FINAL whole-paper Part A **with --audit-state** (S5-1A) → MUST print
            COMPLETION-GATE: PASS and exit 0 with zero fixable WARN. A bare --final
            (Part A only) is NOT sufficient to certify (MANDATE B / MANDATE D).
    STEP 2. Certification gate (§12-2 / §18): the S5-1A COMPLETION-GATE: PASS line
            supersedes self-attestation — every Part-B + §7 checklist item is now a
            C1–C7 assertion, zero residual defects, every item carries the provenance
            stamp its check-class requires AND the evidence file it names exists
            (RA-19). If anything is open → it becomes (or re-opens) a Phase-2 batch;
            Phase 3 does NOT proceed until COMPLETION-GATE: PASS. (There is no
            "PROVISIONAL ship" — Step 8 ships only a certified-clean paper.)
    STEP 3. REGISTRY RE-SYNC (§13) from the FINAL fixed docx (rebuild mock-N slice).
    STEP 4. Stage EXACTLY the closed deliverable set to /mnt/user-data/outputs; run the
            §14 pre-delivery checklist (closed set); ONE present_files call.
    STEP 5. Print the §15 full audit report + the §14 handoff. END THE RESPONSE.

## S4-5 — The "continue" contract + resume

  • INTERACTIVE: Phase 1 ends waiting for "continue". Each Phase-2 batch < K ends
    waiting for "continue". Phase 3 auto-runs after batch K (no "continue").
    AUTONOMOUS (S4-3A): no inter-batch pause; all phases run in one session.
  • "I'll now start the next batch" in the SAME response, INTERACTIVELY = a
    BATCH-STOP-LAW violation (RA-15b). Interactively, one batch = one response.
    (In autonomous mode advancing without the pause is CORRECT — the violation is
    skipping the REVIEW, not skipping the pause.)
  • `MockCreateAudit M[N] resume` reloads audit_state.json and resumes at the first
    not-done batch; already-reviewed questions are NOT re-reviewed (RA-18) but the
    whole-paper Part A still runs each batch (RA-7); the evidence dir persists.
  • `status` prints the dashboard (batches done / open defects / regenerations) and
    does no work.

## S4-6 — AUDIT_BATCH_SIZE

  AUDIT_BATCH_SIZE = 10 (default). It is a batch CEILING, not a target; a batch may
  be smaller when a linked group forces an early close (RA-16). It may be overridden
  ONLY downward (never above 10) and never in a way that splits a linked group. K is
  computed from this constant + the paper (P8) — never hardcoded per exam. NOTE:
  reducing the batch size changes K (more, smaller batches); it NEVER reduces
  coverage — every question is still audited (RA-15a) and S5-1A still asserts
  batches_done == K.

## S4-7 — THE CROSS-SESSION CHECKPOINT (v2.15 / C1 — RA-18)

  WHEN: at the end of every Phase-2 batch (STEP E), in BOTH modes. Overwrite the
  SAME filename each time, so there is only ever ONE current checkpoint and no
  ambiguity about which to hand back. Also written at the end of Phase 1, so a
  session that dies before Batch 1 does not lose the pre-flight + CP-fix work.

  BUILD (never hand-rolled — the manifest and hashes are the safety argument):
  ```bash
  python3 /home/claude/[ExamCode]_mock_test_audit.py \
      /home/claude/[ExamCode]_[paper_slug]_Create.docx \
      --mockN [N] \
      --audit-state /home/claude/[ExamCode]_M[N]_audit_state.json \
      --make-checkpoint /mnt/user-data/outputs/[ExamCode]_M[N]_audit_checkpoint.zip
  ```
  Prints `CHECKPOINT: WRITTEN ... (mock N, batches [..]/K, E ledger entr(ies),
  F evidence file(s))`. Present it with a one-line instruction: "resume state —
  keep this; upload it if this session ends before delivery. It is not the paper."
  It carries audit_state.json, the WHOLE evidence tree (montages / facts /
  recompute) and the WIP docx.

  RESTORE (P0.5C, on a `resume` trigger — BEFORE any batch runs):
  ```bash
  python3 /home/claude/[ExamCode]_mock_test_audit.py \
      /home/claude/[ExamCode]_[paper_slug]_Create.docx \
      --mockN [N] \
      --restore-checkpoint /mnt/user-data/uploads/[ExamCode]_M[N]_audit_checkpoint.zip \
      --into /home/claude/[ExamCode]_M[N]_restored
  ```
  Prints `CHECKPOINT: RESTORED ...` and exits 0, or `CHECKPOINT: REFUSED — <why>`
  and exits 1. On success, audit_state.json is at <into>/audit_state.json with its
  evidence_dir REBASED to <into>/evidence and every recorded evidence path in the
  ledger rewritten to match — the old session's absolute paths no longer exist,
  and S5-1A resolves every C5/C6 stamp through them. Resume then proceeds at the
  first batch not in batches_done (RA-18): nothing already reviewed is re-reviewed.

  REFUSAL IS HARD AND TOTAL. Restore refuses — writing NOTHING — on an unknown
  schema, an absent/unparseable manifest, ANY member whose sha256 differs, or an
  exam_code / mock / paper-MD5 that disagrees with the paper in hand. The paper
  binding is the important one: a checkpoint restored onto a DIFFERENT document
  would let Step 8 certify an audit nobody performed on it, which is strictly
  worse than losing the audit. On REFUSED, do not improvise: report the reason and
  re-run from Phase 1. A partially-restored state is never accepted.

  IF NO CHECKPOINT IS AVAILABLE on a `resume`, say so plainly and restart from
  Phase 1. NEVER reconstruct a ledger from memory to satisfy S5-1A — that is
  precisely the false-clean the completion gate exists to prevent (§19 residual).

# ════════════════════════════════════════════════════════════════════════
# §5 — PART A: MACHINE GATES (whole-paper; run by the universal audit.py)
# ════════════════════════════════════════════════════════════════════════
#   Part A is the deterministic half. It runs over the ENTIRE docx (Phase 1, and
#   re-run after every Phase-2 batch). It re-verifies — INDEPENDENTLY, from the
#   paper + source files, never from a Step-7 sidecar — every machine-checkable
#   Step-7 contract. Every gate derives its expected values from blueprint.json /
#   section_rules.md / subtopic_manifest.json / registry.json (RA-9). Exit 0 +
#   zero fixable WARN is required to certify (MANDATE D). At Phase 3 the SAME script
#   ALSO runs the COMPLETION GATE (S5-1A) via --audit-state — the mechanical
#   enforcement of the Claude-driven Part B / §7 half.
#
#   ── GATE ROSTER COMPLETENESS (v2.12 — a HARD reading rule) ──────────────────
#   EVERY gate prints EXACTLY ONE line on EVERY run, in EVERY environment. There
#   is no environment in which a gate legitimately produces no output. A gate that
#   could not run says so, by name, as a WARN. Read the roster accordingly:
#     • WARN "NOT CHECKED" / "NOT RUN" = the gate DID NOT EVALUATE the paper. It is
#       NOT a pass. Certifying past it certifies coverage you do not have.
#     • A-GATEERROR = a gate CRASHED. FRAMEWORK defect, never a paper defect. The
#       run still completed and every other gate remains valid, but exit is
#       non-zero and certification is blocked until the framework is repaired.
#     • A SHORT ROSTER = the auditor copy predates v2.12 (before which eleven of
#       the twelve figure gates went dark with no line at all, and any gate raise
#       killed the run before ANY line printed). Refresh it — §21 path (A) or (B).
#   Because the roster is invariant, THE GATE COUNT ITSELF IS AN INTEGRITY SIGNAL:
#   two audits of the same paper must print the same number of lines. This is the
#   §R15 reproducibility guarantee, restored at v2.12.
#
#   NO DEPENDENCY CONDITION MAY EVER HALT A RUN. A missing, truncated, or stale
#   engine is an ENVIRONMENT condition, not a paper defect; it degrades to a
#   reported skip and the paper still completes and delivers. This is the same
#   principle already binding on colour (AMBER never halts): the remedy for a
#   defect is LOUDNESS, never silence, and never a halt.

## S5-1 — Invocation

  ```bash
  python3 /home/claude/[ExamCode]_mock_test_audit.py \
      /home/claude/[ExamCode]_[paper_slug]_Create.docx \
      --blueprint /home/claude/[blueprint filename resolved by pp.pick_blueprint, P0] \
      --rules     /home/claude/[ExamCode]_section_rules.md \
      --manifest  /home/claude/[ExamCode]_subtopic_manifest.json \
      --registry  /home/claude/[ExamCode]_registry.json \
      --mockN     [N] \
      --dossier   /home/claude/[ExamCode]_M[N]_audit_dossier.json \
      --final
  ```
  v2.19 — --dossier IS MANDATORY WHEN paths['dossier'] IS NOT None, and OMITTED
  when it is None. Step 7 v5.35+ delivers the Tier-A dossier and P0 stages it; if
  this flag is not passed, the auditor NEVER READS IT and every benefit is silently
  lost — A-NAT-GRADE stays dormant, image_role defaults, and A-FIGCOMP over-reports
  (27 findings instead of 7 on the reference paper). That was the state between
  v2.17 and v2.19: the flag existed on the script, the file was delivered, and no
  documented invocation passed it — the SAME producer/consumer disconnect the
  dossier itself was created to repair, reintroduced one layer up. A-DOSSIER prints
  the consumed/not-consumed verdict on EVERY run precisely so this cannot recur
  silently: if it says "no Tier-A dossier consumed" while the file exists in
  /home/claude, the invocation is wrong — fix it and re-run.
  v5.28: [paper_slug] is pp.paper_slug(paper_id) — "Mock[N]" zero-padded for a mock,
  else the scoped slug; the --blueprint path is whichever [ExamCode]*_blueprint.json
  file P0's pp.pick_blueprint actually selected (paths['blueprint']) — not necessarily
  the plain [ExamCode]_blueprint.json filename when auditing a scoped paper.
  --mockN [N] makes cross-mock dedup self-exclude mock N's own stems (re-auditing
  the registered mock is legal and must not flag the mock against itself). --final
  applies the full gate set + the OMML floor. Record exit code + full STDOUT;
  append STDOUT to the batch reply (RA-2 safe). Exit 0 = all gates passed. (Phase 1
  and every per-batch re-run use THIS form. Phase 3 adds --audit-state — S5-1A.)

## S5-1A — THE COMPLETION GATE (Phase-3 mechanical Part-B / §7 check) — v2.6

  Part A is machine-checkable; Part B (§6) and §7 are Claude-driven and — until
  v2.6 — were verified ONLY by the PROSE checklist §12-2, i.e. self-attested and
  therefore skippable. S5-1A makes them mechanically enforced by validating the
  audit_state.ledger (§9-1) that Claude already maintains AND the on-disk EVIDENCE
  artefacts each ledger stamp names. No new author-facing artefact is introduced;
  an existing internal one becomes load-bearing.

  NEW Phase-3 invocation (REQUIRED to certify):
    python3 .../[ExamCode]_mock_test_audit.py \
        /home/claude/[ExamCode]_[paper_slug]_Create.docx \
        --blueprint ... --rules ... --manifest ... --registry ... --mockN N \
        --dossier /home/claude/[ExamCode]_M[N]_audit_dossier.json \
        --final --audit-state /home/claude/[ExamCode]_M[N]_audit_state.json
    (--dossier included whenever P0 staged one; omitted otherwise. The Phase-3 run
     is the one that CERTIFIES, so a dossier consumed in Phase 1 and dropped here
     would certify against different facts than were audited.)

  With --audit-state, run_audit performs Part A, then ADDS these assertions (ALL
  HARD; exit != 0 on any failure). K and total_questions come from the paper/state
  itself; the evidence dir is read from audit_state.evidence_dir:
    C1  audit_state.batches_done covers 1..K            (every planned batch closed)
    C2  set(ledger.entries.keys()) == {1..total_questions}   (no question unreviewed)
    C3  every entry.status in {verified, regenerated}        (none pending/absent)
    C4  single-mode entry ⇒ answer_unique == True             (B-UNIQUE ran)
        multi-mode  entry ⇒ answer_set_verified == True       (A-MSQ-KEY ran)
    C5  factual entry (GA/CA section OR factual-option flag) ⇒ len(fact_sources) >= 1
        AND every fact_source names a SAVED file under evidence/facts/ that EXISTS,
        PARSES as JSON, and carries a non-blank query + url + retrieved_at + snippet
        in every record (v2.14/B3 — shape, not merely existence: once the raw result
        lives ONLY on disk, a touched stub would erase the evidence while still
        certifying). One file MAY be referenced by several questions — that is the
        RA-11 (b) concept cache, and the gate reports the reuse rather than
        penalising it                                        (B-FACT / RA-11)
    C6  figural entry ⇒ 'image' stamp present AND the montage file it names EXISTS
        under evidence/montages/ and is >= EVIDENCE_MIN_BYTES (a real raster, not a
        0-byte touch); table/chart/omml entry ⇒ 'recompute' stamp present AND the
        recompute-trace file it names EXISTS under evidence/recompute/ and is
        non-empty                                            (RA-4 / RA-19)
    C7  COVERAGE TOTALS (belt-and-suspenders vs a ledger that under-counts the
        paper): #entries with an 'image' evidence stamp == #inline images physically
        in the docx; #recompute-stamped == #tables+charts+OMML expressions present;
        #fact-verified entries == #factual entries. A shortfall means an artefact in
        the paper was never viewed/recomputed/verified — SHIP is blocked.
  SUCCESS prints:
    COMPLETION-GATE: PASS (Q reviewed=[tq]/[tq], facts sourced=[F], artefacts
    stamped=[V], evidence files present=[E])
  FAILURE prints, per failed assertion, the Q-numbers involved (MANDATE-0 safe:
    numbers + codes only, never content or the fact/URL text) and exits non-zero.

  Without --audit-state, --final behaves exactly as v2.5 (Part A only). BUT Phase 3
  (§4 S4-4 STEP 1) NOW REQUIRES the --audit-state form: a bare --final is no longer
  sufficient to certify (MANDATE D + MANDATE B). This is the single change that makes
  a skipped Phase 2 fail LOUDLY instead of shipping false-clean.

  WHY EVIDENCE FILES, not just booleans (FIX F): the ledger is written by the same
  model the gate polices. A presence-only gate would upgrade "say clean" to
  "fabricate a stamped ledger" — better, but still self-attested. Binding each stamp
  to a durable artefact (a montage PNG that must exist for a VIEW, a saved search
  result for a FACT, a recompute trace) means faking a pass requires producing every
  montage, every saved source, and every trace — i.e. performing the audit. That is
  the point at which faking and doing converge (§19 notes the residual).

## S5-2 — The Part-A gate catalogue

  Each row: GATE — checks — exam-agnostic SOURCE of the expectation — Step-7
  contract re-verified — auto-fixable? (CP = content-preserving, done in Phase 1;
  RG = needs regeneration, done in Phase 2; HALT = structural, halts if unfixable).

  STRUCTURE & SEQUENCE
  | A-COUNT    | #question blocks == total_questions                     | blueprint.total_questions          | R7  | RG/HALT |
  | A-SEQ      | Q-numbers are exactly {1..total_questions}, no gaps      | blueprint.total_questions          | R7  | RG      |
  | A-MONO     | Q-numbers strictly increasing in document order         | —                                  | R7  | CP      |
  | A-SECCOUNT | each section holds exactly its q_range's count of Qs     | blueprint.sections[].q_range       | R18 | RG      |

  OPTIONS  (v1.4: SKIPPED for a NAT question — answer_type=='numerical', registry options_by_q==0;
            A-NAT-NOOPT verifies those render zero options instead)
  | A-OPTN     | every Q has exactly OPTIONS_COUNT options (NAT Qs skipped)| section_rules options_count        | R4  | RG      |
  | A-OPTLABEL | option labels match option_label_format (default "n.  ")| section_rules option_label_format  | R10 | CP      |
  | A-OPTORDER | options appear in document order 1..OPTIONS_COUNT — ANCHORED AT 1 (v2.21.3), not merely consecutive: a set labelled 2,3,4,5 is a FAIL. A-KINT derives the key in 1..OPTIONS_COUNT, so an unanchored set misaligns EVERY key on that question. Family-agnostic: _idx_of() normalises num/alpha/roman to 1-based | — | R13 | CP      |
  | A-OPTUNIQUE| options distinct within a Q (strip+casefold)            | —                                  | R4  | RG      |

  BODY HYGIENE
  | A-SECHDR   | no section-heading paragraph in the body — KEYWORD form ("section"/"part N"/rule chars) AND (v1.5) SECTION-NAME form: a standalone body paragraph equal to a declared section name (blueprint src['sections']); scans all body paragraphs, not only within blocks | blueprint sections + (universal ban) | R8  | CP      |
  | A-ANSKEY   | no answer key / correct-marker / hint anywhere (incl. SET-valued "Q.1 → 1,2,4" AND NAT numerical "Q.5 → 47" leaks, not just single-digit) | (universal ban) | R5  | CP      |
  | A-FONT     | every run Calibri (font.name in {Calibri, None})        | section_rules (default Calibri 11) | R24 | CP      |
  | A-BLANKSEP | ≥1 blank paragraph separates consecutive Q blocks       | —                                  | R13 | CP      |
  | A-QNFIRST  | each block OPENS with its "Q.<n>" paragraph             | (Q.N-FIRST contract)               | R14 | CP      |
  | A-MSQ-INSTR| (multi only) the select-instruction ("(One or more options may be correct)" / "(Select TWO)" / localized) is present INSIDE the Q.<n> stem line — no separate instruction paragraph (would break A-QNFIRST), no paper-level instructions page | section_rules msq_instruction + blueprint answer_cardinality | R14 | RG (re-emit stem with instruction on the Q.N line) |
  | A-NAT-NOOPT| (numerical only) every Q the registry marks 0-option (NAT) renders ZERO option paragraphs | registry options_by_q + blueprint nat_present | R4/R13 | RG (re-emit as a 0-option NAT block) |
  | A-NAT-INSTR| (numerical only) the numerical-entry instruction (nat_instruction / localized) is present INSIDE the Q.<n> stem line; per-section observed count matches the blueprint NAT allocation | section_rules nat_instruction + blueprint expected_nat_by_section | R14 | RG (re-emit stem with instruction on the Q.N line) |

  LINKED-STIMULUS SELF-CONTAINMENT
  | A-STIMORPHAN | every linked member carries its stimulus in its own block; no "Q.x and Q.y" cross-ref | registry rc_manifests + di groups + re-derived cues | R-LINKED | CP* |
       *CP when the stimulus exists elsewhere in the group (embed a copy, Model A);
        RG only if the stimulus itself is absent/defective.

  MATCH-GRID RENDERING
  | A-MATCH-TABLE | every Axis-2 MATCH question (re-derived by the shared S6-1b classifier) renders its List columns as a real <w:tbl>; a match rendered as text lines or space/tab pseudo-columns is a format-fidelity defect (MATCH counted present, skill un-rehearsed) | re-derived axis2 (S6-1b) + block.tables | S7-3 / G-MATCH-TABLE | CP (rebuild List body as a real table) |

  RENDERING FIDELITY (the gates that catch "faked-as-text/raster" defects)
  | A-UNDERLINE | underline-class Q carries a real <w:u> run; no "(underlined: X)" | section_rules (sentence_embedded_underlined) + stem cue | R-UNDERLINE | CP |
  | A-MATHRASTER| no built-up math shipped as a raster image (see S5-3)    | section_rules OMML_required + math cues | R-MATH-OMML | CP/RG |
  | A-FRAC      | no slash/caret ASCII built-up math in a math-context stem| section_rules OMML_required        | R-MATH-OMML | CP |
  | A-OMML      | every <m:f> has non-empty numerator AND denominator; no year-range "YYYY/YY" stacked fraction; OMML floor ≥1 if any subtopic OMML_required | section_rules OMML_required | R-MATH-OMML | CP |

  FIGURAL DECOMPOSITION
  | A-FIGCOMP  | v2.4 image_role-aware: each figural Q is structured per its image_role variant. stem_and_options (default): problem image(s) + 1 image/option, single-column, 1 per line, bound 1:1 to labels; no composite panel; no "Figure k" dummy-text option. stem_only (v2.4): ≥1 problem image + TEXT options — option-image arm SKIPPED. options_only (v2.4): ≥n option images, no problem image required. FIGURAL-NAT (answer_type=='numerical', options_by_q==0): treated as stem_only — problem image(s) only with ZERO option images. All variants: single-column/no-composite/300-DPI/named-image discipline checked. image_role read from section_rules PYQ_IMAGE_ANALYSIS per subtopic_id | registry figural_manifests + section_rules PYQ_IMAGE_ANALYSIS + figural stem cues + registry options_by_q | R-FIGURAL | CP/RG | v2.21.4: a REGISTRY-DECLARED figural Q rendering ZERO images is a finding (the zero-image case previously hit an early `continue`, making the stem_only arm DEAD CODE); and stem_and_options requires the FULL set of oc+1 images, not merely more than one — a partial option-image set was previously accepted. v2.21.5 (ND10): a question the registry marks 0-option is NUMERICAL — the per-OPTION-image arm DOES NOT APPLY in either the stem_and_options or options_only variant; the signal is registry options_by_q (the same one gate_options reads), NEVER concept_map, which is empty on any run without a dossier or --key. >=1 problem image is still required.
  | A-FIGPROFILE | v2.10 (GAP-2026-07-26-003 D2): each FIGURAL subtopic's GENERATED figure types conform to the profile Step 5 measured. Reads section_rules PYQ_IMAGE_ANALYSIS via bc.figural_generation_profile(), reads the object_type Step 7 recorded per question in registry.figural_manifests[mock].object_types (v2.18 CORRECTION: this row previously named batch_state.figural_qs[n].object_type, a Step-7 INTERNAL sidecar that S0-1 explicitly does NOT deliver — the auditor has always read the registry. The stale row sent an operator hunting for a file Step 8 can never have, and cost two turns and one wrong intermediate finding on a live run), and delegates the verdict to bc.check_figural_conformance() — the SAME function Step 7 generates against, so generator and auditor cannot drift. FAIL when a generated type appears in neither the dominant nor the observed list, or when dominant-mode coverage falls below the 55% floor (target 70%). SKIP when the profile is unconstrained — absent, empty, or vision_status='unavailable'. AUDITS RECORDED INTENT, NOT PIXELS: confirming a render actually depicts a micrograph needs a view(), a CLASS T operation that cannot run inside an audit's python; intent is deterministic and catches the real failure, which is Step 7 ignoring the profile. EC-V18: SKIP keeps ~200 pre-v2.37 exams passing untouched. | section_rules PYQ_IMAGE_ANALYSIS + registry figural_manifests[].object_types | R-FIGURAL | CP/RG |

  FIGURE CONFORMANCE (v2.11, GAP-2026-07-29-FIG-R2). Twelve gates, all arithmetic
            over the saved PNG and its FigureSpec sidecar — NOT vision.
            A-FIGPROFILE above audits recorded INTENT and rightly declines pixels,
            because "does this depict a micrograph" needs a view() (CLASS T). That
            one true fact had been generalised to every figure property; these
            need only arithmetic, which is how the whole gap was measured with no
            vision available. Severity: NO COLOUR CONDITION MAY EVER HALT A RUN
            (owner directive; CLAUDE.md "a halt is not the remedy"). AMBER = FAIL
            severity + amber delivery footer, always completes. VOID_ITEM = the
            QUESTION is invalid because the render leaks an answer cue; drop or
            regenerate that item and the paper continues. BLOCKING =
            renderer-contract regression on Step 7 v5.33+ output only. EC-V18:
            output with NO sidecar predates v5.33, so every BLOCKING gate
            downgrades to AMBER — ~200 existing exams keep auditing and delivering
            untouched while still reporting the defect loudly.
            v2.13 — TWO RULES MADE EXPLICIT, both previously unreachable because
            the gates evaluated nothing (Block.images was never populated):
              • COVERAGE. Each gate reports the NUMBER of figures it evaluated.
                Drawings present but unreadable => WARN "conformance NOT
                ESTABLISHED"; a paper with no drawings => OK "dormant". A gate
                NEVER prints a conformance verdict over zero figures — the same
                0/0-is-not-evidence rule A-FIGPROFILE already carries.
              • EC-V18 IS A DELIVERY TOLERANCE. A finding on a figure with NO
                sidecar is a WARN (loud, amber footer, §R13 limitation, delivery
                NOT blocked): Step 8 cannot retro-fit a sidecar onto an
                already-rendered paper, so it is an S5-4 ACCEPTED WARN. A finding
                on a figure that DOES carry a sidecar is a FAIL and blocks
                certification, exactly as before. Without this split, the moment
                the gates stopped being vacuous every legacy exam would have
                exited non-zero and MANDATE D would have refused to certify it —
                a coverage fix turned into an estate-wide outage.
  | A-FIGCOLOUR | class data_series carries >=2 declared hues AND >=0.5% coloured pixels. Measured 0 of 55 delivered IIT JAM figures coloured, 256/256 distinct RGB (a pure grey ramp), because S10-7 Q7 MANDATED "solid black" — the output was CONFORMANT and the spec was the defect | FigureSpec sidecar + PNG pixels | R-FIGURAL / S10-7 Q7b.1 | AMBER |
  | A-FIGCVD | every pair of DECLARED series colours stays separable under a deuteranope transform. Reads the declaration, never extracted pixels. No luminance clause: Okabe-Ito is CVD-safe by design and was never greyscale-luminance-safe (deuteranope 10/10 pass, luminance 3/10 fail), so greyscale survival is gated by A-FIGSERIES instead | FigureSpec sidecar | S10-7 Q7b.3 | AMBER |
  | A-FIGSERIES | every declared series differs from every other in >=1 NON-COLOUR channel (linestyle, marker or hatch). This is what makes a figure survive a greyscale printer and a colour-blind reader even if the palette is overridden | FigureSpec sidecar | S10-7 Q7b.2 | AMBER |
  | A-FIGGLYPH | the figure font covers the exam glyph set; a missing glyph renders as a tofu box | FigureSpec sidecar + font cmap | S10-7 Q9.4 | AMBER |
  | A-FIGALT | wp:docPr/@descr alt text present and non-empty. Measured 0 of 208 delivered drawings | docx drawing XML | S10-7 Q9.5 | AMBER |
  | A-FIGLABELPX | ADVISORY pixel cross-check on on-page label size. Never authoritative: identical 10pt requests at identical saved width measured 8.5pt when axis titles carried scientific notation and above the floor with short labels, because superscripts and subscripts are small connected components that drag the median down. A-FIGLABEL is the authoritative check | PNG pixels | S10-7 Q9.6 | AMBER |
  | A-FIGMONO | class reasoning_glyph is monochrome apart from a declared missing-element accent. Colour in an abstract-reasoning item can reveal WHICH option is correct — that is not an ugly question, it is a wrong one | FigureSpec sidecar + PNG pixels | S10-7 Q7b.7 | VOID_ITEM |
  | A-FIGOPTUNIF | all option canvases in a set share pixel size and placed width. A size difference between options is an answer cue. The delivered uniform 780x780 option canvases were CORRECT on this point and the property is preserved | FigureSpec sidecar + PNG sizes | S10-7 Q7b.6 | VOID_ITEM |
  | A-FIGSCALE | placement scale S == 1.0, or exactly the column cap when capped. Measured S = 0.500 EXACTLY on 24 of 24 delivered option canvases: FIG_NATIVE_HEADROOM=2.0 supersampled the canvas while placement took its width from a CONFIGURATION constant, so p_page = p_native x S and the spec controlled neither | FigureSpec sidecar + PNG header | S10-7 Q3 / S10-8 | BLOCKING |
  | A-FIGLABEL | smallest on-page label >= the class floor (9pt data/schematic, 8pt glyph/option). ARITHMETIC over the font sizes actually used at render time x the recorded scale, never pixel components. Measured median 6.7pt as delivered | FigureSpec sidecar | S10-7 Q9.1 | BLOCKING |
  | A-FIGDPI | PNG carries DPI metadata; without it native size is undefined and S cannot be computed. Never assume 300 | PNG header | S10-7 Q3 | BLOCKING |
  | A-FIGDEGEN | the drawn area is >=18% of the canvas. Catches the one failure arithmetic cannot otherwise see: below ~3in a labelled axis does not fit, constrained_layout collapses the plot area to zero, and the degenerate figure passes every size and font gate because the PNG is the requested pixel size and the fonts were the requested points | PNG pixels | S10-7 Q3 / FIG_MIN_DATA_DISPLAY_IN | BLOCKING |

  STEM↔OPTION COHERENCE (machine layer; semantic layer in §6)
  | A-OPTREF   | a stem that references a terminal/escape option ("no error→last option", "None of these", "All of the above", "Both…and…", "Neither…nor…") actually CONTAINS that option, at the named position; a "pick-the-segment" layout does not carry a "no error" escape without a real "No error" option | section_rules none_of_above_permitted (S3-12) + wrong_option_structure/fixed_set (S3-13) | R-OPTREF | RG |

  INTEGRITY
  | A-ZIP      | document.xml present; every image rId resolves to an existing part | —                          | (structural) | HALT |
  | A-ENCODING | no U+FFFD replacement characters                        | —                                  | (structural) | RG  |
  | A-SCRIPT   | non-ASCII regional script present ONLY if language permits it (else copy-paste corruption) | section_rules language (RA-10) | (structural) | RG |
  | A-INTEGRITY| (P0.5 pre-flight) every JSON input parses + carries its required top-level keys; audit.py ast-parses + passes the hardened self-test; section_rules non-empty with EXAM_STRUCTURE header | (structural) | HALT (repair audit.py / engines only) |
  | A-GATEERROR| (v2.12) a gate raised an unexpected exception. The gate DID NOT audit the paper; every other gate still ran and the report is complete. FRAMEWORK defect — never fix the paper for this | (structural) | FAIL — blocks certification; file a gap report |
  | A-FIGPROFILE| generated figure object_types conform to the PYQ profile Step 5 measured; verdict DELEGATED to blueprint_core (the same function Step 7 generates against, so generator and auditor cannot drift). Dormant on pre-v5.31 registries; WARN "NOT CHECKED" if the engine is absent/truncated/stale | RG | FAIL / WARN |

  | A-FIGTEXT-PROSE | (v2.4, sub-code of gate_images) a block containing ZERO images must not carry figure-reference PROSE ("in the figure above", "the diagram shows"). A figural subtopic rendered as prose is a figure that was never drawn; the candidate is asked to read something that is not there. Blocks with >=1 image are skipped (no false positive). Twin of Step-7 G-FIGTEXT-PROSE (Create.md Tier 3) | rendered block text vs image presence | R-FIGURAL / G-FIGTEXT-PROSE | RG (render the figure per S7-NEW-B OPTION A, or replace the subtopic) |

  CROSS-MOCK DEDUP
  | A-DUP      | no stem in mock N exact-matches OR near-matches (Jaccard ≥ J_FAIL) a stem from a PRIOR mock in registry.stem_texts (self-excluding mock N via --mockN); image MD5/pHash not reused from a prior mock | registry stem_texts/question_hashes/image_phashes/content_tracking | R2/R3 | RG |

  TIER-A DOSSIER CROSS-CHECK (v2.17; predicate corrected v2.21)
  | A-DOSSIER  | every Tier-A FACT (qtype, subtopic_id) agrees with the SHIPPED PAPER and the registry. qtype is checked against the RENDERED OPTION COUNT, which MUST be obtained from the SAME helper the option gates use — block_option_count(b, oc) -> _label_paras() + trailing-oc clamp — NEVER from a second predicate. An IMAGE option is a BARE label paragraph followed by a picture paragraph and carries NO text glyph, so any predicate requiring one counts it as ZERO (GAP-2026-08-02). The nat leg fires on ANY non-zero rendered count and MUST NEVER be clamped (v2.21.1): Create R13 (v4.7 NAT EXEMPTION) gives a NAT block ONLY the bold Q.<N> stem and the blank separator — ZERO option paragraphs, with no 'enumerated stem' class — so any option-label paragraph on a claimed-NAT block is an R13 violation. Clamping it opened a false negative in the nat_present=False + registry-0 configuration, where gate_options skips and gate_nat is dormant and A-DOSSIER is the only remaining gate. subtopic_id is checked against registry figural subtopic_ids. A disagreement is a FAIL, never a silent overwrite in either direction. Dossier ABSENT => WARN (legacy, not a paper defect). NO GATE MAY PASS ON DOSSIER EVIDENCE ALONE | dossier + registry options_by_q + rendered block | S13-4b (v5.35) | RG (Step-7 side) / none (paper) |

  HEADER
  | A-HEADER   | NO non-blank paragraph before Q.1 — the paper is questions-only; any title/info/scoring/cover block is a defect → STRIP it (CP-HEADER-STRIP). Dormant only if section_rules EXAM_STRUCTURE declares paper_header_block | section_rules CATEGORY-C (paper_header_block) | R8b/G-PREQ1 | CP |

  DERIVED-KEY GATES (run ONLY after §11 builds Step 8's independent key; advisory→fix)
  NOTE: these are computed by CLAUDE from the §11 derived key — the machine
  script never receives a key (none is delivered, S0-1), so it does not emit them.
  | A-KINT     | derived key per Q is a single int in 1..OPTIONS_COUNT (single) OR a non-empty proper subset of 1..OPTIONS_COUNT (multi); total_questions entries | section_rules options_count + blueprint answer_cardinality | —    | n/a (derivation check) |
  | A-KBAL     | per-section answer-option balance within the band (SINGLE-mode Qs only; multi AND numerical excluded) | OPTIONS_COUNT + per-section counts | — | RG (rotate distractor) |
  | A-KPAT     | no same-answer run ≥ RUN_MAX across the SINGLE-mode Qs in Q1..QN incl. cross-section boundaries (multi AND numerical excluded) | RUN_MAX=3 (framework const) | — | RG (rotate distractor) |
  | A-MSQ-KEY  | (multi only) re-derived set S is a non-empty PROPER subset of 1..OPTIONS_COUNT (1≤|S|≤n−1; |S|=msq_k when msq_k_mode=fixed); no banned AOTA option under multi (msq_allow_aota) | blueprint answer_cardinality + msq_k_mode/msq_k + section_rules msq_allow_aota | RA-12 | RG (re-form the set) |
  | A-NAT-ANSWER| (numerical only; Claude-derivation) re-derived VALUE is uniquely determined by the stem, form-matched to nat_answer_type (integer⇒integral; real⇒within ca_range, lo≤hi); 0/negative/fractional valid; value does not leak; the grading transform (nat_grading_type/value, S7-NEW-C) matches derive_nat_grading() applied to this SAME re-derived value | blueprint nat_answer_type/nat_tolerance | RA-12 | RG (disambiguate the stem / re-derive the value / re-run the grading transform) |
  | A-NAT-GRADE | (numerical only; machine) sidecar's OWN nat_grading_type/nat_grading_value exactly matches derive_nat_grading() applied to the sidecar's OWN recorded value/ca_range/tolerance; charset is 0-9.- only | sidecar concept_map (nat_value, ca_range, nat_grading_type, nat_grading_value) | RA-12 | RG (re-run derive_nat_grading(); rework Q if NOT-SUPPORTED negative-range) |

  SUB-CODES: a parent gate may emit refinement sub-codes that sharpen the locator —
  A-STIMORPHAN-XREF (a "Q.x and Q.y" cross-reference), A-UNDERLINE-FAKE (a
  "(underlined: X)" annotation), A-OMML-YEAR (a year-range rendered as a stacked
  fraction), A-OMML-FLOOR (OMML_required declared but zero <m:oMath>), A-FRAC-SLASH
  (a slash fraction in a math-context stem), A-MATHRASTER-VIEW (non-canonically-named
  images to VIEW in Part B), A-FIGCOMP-LINE (two images on one line). A "-VIEW"/
  "-SLASH"/"-YEAR"/"-FLOOR" sub-code is a WARN routed to Part B/§7; the others are
  FAILs of their parent gate.

  ONE STRUCTURAL QUESTION, ONE ANSWER (v2.21 — GAP-2026-08-02-DOSSIER-OPTION-PREDICATE).
  Where two or more gates need the SAME structural fact about a block — how many
  options it renders, how many images it carries, how many tables it holds — they
  MUST obtain it from ONE shared helper. A second implementation is DRIFT BY
  CONSTRUCTION: it will be written against the author's BELIEF about the first
  rather than against the first, and the divergence stays invisible until a paper
  exercises the difference. This is the SAME anti-drift rule already binding on
  derive_nat_grading() ("byte-identical to Framework_MockTestCreate.md §S7-NEW-C,
  never re-implemented independently") and on bc.check_figural_conformance() ("the
  SAME function Step 7 generates against, so generator and auditor cannot drift") —
  it had simply never been stated for two gates inside the SAME file. A-DOSSIER
  answered "how many options does this block render?" with OPT_RE while A-OPTN
  answered it with OPT_LABEL_RE, and the two disagreed on EVERY image option in the
  estate for four consecutive releases. Enforced mechanically by
  validate_framework_md.py CHECK AN. A helper that answers such a question MUST NOT
  claim parity with a sibling in its docstring unless a fixture MEASURES that parity
  (fixture 92d).

## S5-3 — A-MATHRASTER: robust, exam-agnostic, view-backed (the naming-gap fix)

  Step 7's G-MATH-RASTER authenticates legitimate rasters by an image NAME contract
  (^q\d+_(problem|opt\d+|stim)). In the wild, the docx emitter (python-docx) often
  overwrites image names with generic defaults ("Picture 1"…"Picture k"), so a NAME-
  ONLY gate would FALSE-FAIL every legitimate figure. Step 8 therefore does NOT rely
  on the emitter naming. A-MATHRASTER works in TWO tiers:
    TIER 1 (machine, in audit.py): FAIL only on a HIGH-CONFIDENCE math-raster signal —
      an inline image whose part/docPr name carries an explicit math token
      (_e\d, _eqn, _expr, _frac, _math) OR an image that sits in a block whose stem
      is math-context (OMML_required subtopic / built-up math cue) AND is NOT one of
      the manifest's figural_qs AND is NOT a DI chart. All OTHER non-canonically-named
      images are emitted as a WARN LIST for Tier 2 (not a FAIL — avoids blocking on a
      mis-named-but-legitimate figure).
    TIER 2 (§7, Part B view): every image on the WARN list (and every image generally)
      is VIEWED. If a viewed image is in fact a rasterised algebraic expression, it is
      a defect → CP-MATHOMML (re-render as OMML, drop the raster). If it is a genuine
      figure that was merely mis-named, CP-IMGNAME renames it to the canonical
      q{N}_problem / q{N}_opt{i} / q{N}_stim contract so future steps and any re-run of
      the name-contract gate pass. The VIEW is the authority (RA-4); the name contract
      is a fast diagnostic, never the sole verdict.
  This makes A-MATHRASTER both provenance-aware AND robust to emitter naming, on every
  exam and every generator — no false-FAIL on legitimate figures, no escape for a real
  math raster.

## S5-4 — Zero-Warning Policy (= Step 7 S12-0)

  Every fixable WARN is a blocker (same as FAIL). Fix it, re-run, iterate. No
  advisory carries forward to Step 9 or the next mock. The only WARNs that may be
  ACCEPTED (documented, not fixed) are genuinely-not-fixable diagnostics (e.g. a
  registry that lags such that cross-mock dedup is partial — recorded as a §15
  limitation), never a content or rendering defect.

## S5-5 — Part A is NOT the whole audit (the blind-spot contract)

  Part A proves STRUCTURE and FORMAT, not CONTENT TRUTH. It cannot prove a fact is
  current, that a figure's transformation is correct, that exactly one option is
  defensible, that a DI table's numbers actually yield the keyed answer, or that an
  OMML expression computes correctly. Those are Part B (§6) and the §7 deep audit,
  which carry equal force: a paper that passes Part A but fails Part B/§7 is NOT
  certifiable (no SHIP). Each Part-A gate's blind spot is explicitly covered by a
  named Part-B / §7 check (§6 and §7 cross-reference the gate they backstop).
  v2.6 — AND: because Part B / §7 are Claude-driven, they were the ONLY skippable
  half. The COMPLETION GATE (S5-1A) removes that: a Part-B/§7 check that did not run
  leaves no stamped-and-evidenced ledger entry, so C2–C7 fail and delivery is
  blocked. "Passed Part A, skipped Part B" is now a LOUD failure, not a silent ship.

# ════════════════════════════════════════════════════════════════════════
# §6 — PART B: SEMANTIC REVIEW (every question; zero sampling; batched)
# ════════════════════════════════════════════════════════════════════════
#   Part B is the reasoning half — the checks no regex can prove. It runs per
#   Phase-2 batch (≤10 Q), every question, zero sampling (RA-3). It is organised by
#   UNIVERSAL question CLASS (derived at runtime from the question's format +
#   wrong_option_structure in section_rules), NOT by exam-specific sub-types — so
#   the same checklist audits an SSC antonym, a GATE numerical-answer, a NEET
#   assertion-reason, or a UPSC match-the-column. No exam content is named here.
#   v2.6 — every check writes a STAMPED ledger entry (§9-1); B-FACT additionally
#   SAVES its search result to evidence/facts/ and names it in the entry. The
#   COMPLETION GATE (S5-1A) reads these — an un-run check leaves no entry and fails
#   certification.

## S6-0 — Extraction protocol (do this for every question before judging it)

  1. MERGE OMML + text: extract <m:t> (math) interleaved with <w:t> (text) in
     document order, so a math-bearing or pure-OMML stem reads correctly. Never
     judge a stem "empty" from p.text (RA-4).
  2. Read the FULL stem + the FULL text of all OPTIONS_COUNT options. Two options
     may share a long prefix and differ only at the end — read to the end.
  3. Build the per-question artefact map (from P6 index): attached tables, inline
     images (with media files), OMML nodes, <w:u> runs.
  4. Classify the question (S6-1) from section_rules (format + wrong_option_structure
     + stem cues). The class selects which checklists apply.
  5. "shown below"/"as given"/"as shown" in a TEXT stem (seating, directions) is
     NORMAL phrasing — confirm a missing-artefact suspicion against the actual
     artefact map before flagging (avoids false A-STIMORPHAN positives).
  6. v2.5 — TAG THE AXES: run `tag_axes(qa)` + `derive_is_negative(qa)` (S6-1b) on the
     extracted `{stem_raw, options, image_role, linked_group_id, blank_pos, is_msq}`, and
     store axis1/axis2/axis3/is_negative on this question's §9 ledger entry. This is the
     INDEPENDENT re-tag the S6-6 format-distribution audit consumes. Inert-safe: harmless
     when blueprint has no axis_schedule (the S6-6 audit simply never reads them).
  7. v2.6 — OPEN the §9 ledger entry for this q at the START of review (status
     'pending'), and CLOSE it to 'verified'/'regenerated' only when every applicable
     §6 + §7 check has run and its evidence is saved. A question left 'pending' fails
     S5-1A C3 — so a half-reviewed question can never certify.

## S6-1 — Universal question CLASSES (runtime-derived; exam-agnostic)

  Derived from section_rules format + wrong_option_structure.type + stem cues.
  A question may carry more than one class facet (e.g. LINKED + COMPUTATIONAL).

  C-COMPUTATIONAL : numeric/quantitative answer from a computation (format TEXT/DI,
                    quantitative number ranges). Audited by re-solving (B-SOLVE)
                    and tracing every distractor to a named error path (B-DISTRACT).
  C-FORMAL-LOGIC  : answer from a fixed formal procedure with a FIXED option set
                    (wrong_option_structure.type == fixed_set) — syllogism, data-
                    sufficiency, assertion-reason, cause-effect, statement-conclusion,
                    inequality chains, etc. Audited by executing the formal rule and
                    confirming the fixed option order matches fixed_option_texts.
  C-FACTUAL       : answer is a fact (general awareness, science recall, current
                    affairs, computer/domain fact). Audited by WEB-VERIFICATION of the
                    keyed fact AND every option (B-FACT); distractors must be real,
                    same-domain, verifiably-wrong facts.
  C-VOCAB-ITEM    : answer about a target ITEM (synonym/antonym/idiom/one-word/
                    spelling/homonym/word-meaning). Audited for single-context-validity
                    of the key, no-context-validity of distractors, real underline if
                    'sentence_embedded_underlined', and presentation variety (B-PRESENTDUP).
  C-GRAMMAR       : sentence transformation/correctness (error-spotting, sentence-
                    improvement, active/passive, narration, fill-in-sentence, jumble).
                    Audited by re-deriving the correct form; each distractor violates
                    exactly one rule; escape-option coherence (B-OPTREF-SEM).
  C-LINKED        : member of a shared-stimulus group (RC/cloze/DI/puzzle). Audited
                    for stimulus self-containment (already A-STIMORPHAN) PLUS
                    derivability-from-stimulus-alone (B-PASSAGE) and per-blank/
                    per-member coverage.
  C-FIGURAL       : answer is a figure or depends on a figure/diagram. Audited entirely
                    in §7 (view every image; transformation true; key unique).
  C-MATRIX/MATCH  : match-the-column / matrix. Audited in §7 (parse grid; re-derive
                    every pair; one fully-correct option).

  Class detection reads section_rules; an unknown format defaults to the closest of
  the above by wrong_option_structure.type, and the generic checks (S6-2) still apply.

## S6-1b — AXIS CLASSIFIER v1.0 (COPIED VERBATIM from Step 5 — v2.5)

  The three-axis format audit (S6-6) is only valid if generated questions are classified
  by the EXACT SAME functions Step 5 used on the PYQ papers. These functions are copied
  BYTE-IDENTICAL from Step 5's `AXIS CLASSIFIER v1.0` block — never re-implemented, never
  "improved" here. If Step 5's classifier changes, this copy MUST be updated to match.
  They read only fields Step 8 already extracts per question (S6-0): the rendered stem
  (`stem_raw`), the option texts (`options`), `image_role`, `linked_group_id`, `blank_pos`,
  and `is_msq` — so Step 8 re-derives the axes INDEPENDENTLY from the shipped paper.

  ```python
  import re

  AXIS2_CLASSES = ['LINKED', 'ASSERTION_REASON', 'MATCH', 'SEQUENCE', 'STATEMENT',
                   'FILL_BLANK', 'ODD_ONE_OUT', 'DIRECT']   # ladder order == precedence

  # v2.7.4 FIX C PROPAGATION (byte-identical to Step 5 v2.24.6) — see Step 5's
  # _looks_like_table_stimulus docstring for full rationale. Was a naive substring
  # match ('|' in stem or 'table' in stem.lower()) that false-positived on any word
  # merely containing "table" (vegetable, acceptable, notable, ...).
  _TABLE_WORD_RE = re.compile(r'(?i)\b(table|tabulated|following data|dataset)\b')
  def _looks_like_table_stimulus(stem):
      stem = stem or ''
      pipe_rows = sum(1 for ln in stem.splitlines() if ln.count('|') >= 2)
      return pipe_rows >= 2 or (bool(_TABLE_WORD_RE.search(stem)) and pipe_rows >= 1)

  def classify_axis1(q):
      """STIMULUS/MEDIA. Priority FIGURAL > PASSAGE > DI > TEXT — identical ordering to
      the per-subtopic `fmt` line in synthesise_subtopic (a linked DI passage resolves
      PASSAGE, matching that function)."""
      if q.get('image_role', 'none') not in ('none', None):
          return 'FIGURAL'
      if q.get('linked_group_id'):
          return 'PASSAGE'
      stem = (q.get('stem') or q.get('stem_raw') or '')
      if _looks_like_table_stimulus(stem):
          return 'DI'
      return 'TEXT'

  def classify_axis3(q):
      """ANSWER MECHANISM. NAT = no selectable options (mirrors the answer_type=='numerical'
      detection: zero text options AND no option-images). MSQ = is_msq. Else MCQ."""
      opts = q.get('options', []) or []
      if len(opts) == 0 and q.get('image_role', 'none') not in ('options_only', 'stem_and_options'):
          return 'NAT'
      return 'MSQ' if q.get('is_msq') else 'MCQ'

  def _opts_are_combination_labels(opts):
      """EC-A signal: options predominantly combination-labels (Only N / Both N and M /
      Neither…nor / None of / All of the above / "N and M"). Distinguishes STATEMENT and
      MATCH combo-answer stems from genuine free-form options."""
      if not opts:
          return False
      combo = 0
      for o in opts:
          t = (o or '').strip().lower()
          if re.search(r'\b(only|both|neither|none of|all of)\b', t) or \
             re.match(r'^[a-d1-4](\s*(and|,|&|-)\s*[a-d1-4])+$', t):
              combo += 1
      return combo >= max(2, (len(opts) + 1) // 2)

  # ── MATCH option-shape backstop (v2.24.2) ──────────────────────────────────────
  # A language-agnostic MATCH signal: the OPTIONS are a set of CROSS-DOMAIN label pairs
  # (e.g. "A-I, B-III, C-IV, D-II" / "1-C 2-A 3-D 4-B" / "(A)-(i), (B)-(iv) ..."). It fires
  # when the stem keywords (match / list-I / column) are ABSENT — the two cases that matter:
  #   (a) NON-ENGLISH match papers (Hindi/regional), whose stems carry no English cue;
  #   (b) matches whose List-I/List-II body has been rendered into a Word table, so the list
  #       labels no longer appear in stem_raw (only the "Match ..." instruction does).
  # CROSS-DOMAIN (left label family != right label family) is REQUIRED, so digit:digit ratios
  # ("2:3, 4:5"), coordinate pairs and word-word hyphenations never trip it. The family of a
  # COLUMN (not a single token) is used so the roman-vs-letter "I" ambiguity resolves from
  # context (a column carrying II/III/IV is roman even where a bare I appears).
  _MATCH_PAIR_RE = re.compile(
      r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
      r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?')
  _MATCH_PAIR_SUB = (r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
                     r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?')
  _MATCH_OPT_RE = re.compile(r'^\s*' + _MATCH_PAIR_SUB + r'(?:[,;\s]+' + _MATCH_PAIR_SUB + r'){1,}\s*$')

  def _label_family(tokens):
      """Family of a same-side label COLUMN: 'digit' | 'roman' | 'alpha' | 'other'.
      Column-level (not per-token) so a bare 'I' resolves to roman when its column also
      carries II/III/IV, and to alpha when its column is A/B/C/D."""
      low = [t.lower() for t in tokens if t]
      if not low:
          return 'other'
      if all(re.fullmatch(r'\d{1,2}', t) for t in low):
          return 'digit'
      romanish = all(re.fullmatch(r'[ivxlcdm]+', t) for t in low)
      if romanish and any(len(t) > 1 for t in low):
          return 'roman'
      if all(re.fullmatch(r'[a-z]', t) for t in low):
          return 'roman' if set(low) <= {'i', 'v', 'x'} else 'alpha'
      if romanish:
          return 'roman'
      if all(re.fullmatch(r'[a-z]{1,4}', t) for t in low):
          return 'alpha'
      return 'other'

  def _opts_are_match_pairs(opts):
      """True when a MAJORITY of options are each a set of >=2 CROSS-DOMAIN label pairs that
      consume the whole option text. Threshold mirrors _opts_are_combination_labels. Used by
      classify_axis2 AFTER the keyword rules, so it can only convert a would-be non-MATCH
      class to MATCH, never the reverse (additive + monotone)."""
      if not opts:
          return False
      hits = 0
      for o in opts:
          st = (o or '').strip()
          if not st or not _MATCH_OPT_RE.match(st):
              continue
          pairs = _MATCH_PAIR_RE.findall(st)
          if len(pairs) < 2:
              continue
          lf = _label_family([p[0] for p in pairs])
          rf = _label_family([p[1] for p in pairs])
          if lf == rf or 'other' in (lf, rf):
              continue
          hits += 1
      return hits >= max(2, (len(opts) + 1) // 2)

  def classify_axis2(q):
      """STEM STRUCTURE — the exclusive 8-class ladder (first-match-wins). Discrimination
      is by task-verb + option-shape, not ladder position alone, so collisions are rare and
      deterministic. Grounded in EC-8/9/11/12/13; SEQUENCE + ODD_ONE_OUT added in v2.23."""
      # GATE 0 — LINKED: structural, decided by shared-stimulus membership, not phrasing.
      if q.get('linked_group_id'):
          return 'LINKED'
      stem = (q.get('stem_raw') or q.get('stem') or '')
      s    = stem.lower()
      opts = q.get('options', []) or []
      # 1 — ASSERTION_REASON (EC-8): both an Assertion and a Reason clause present.
      if re.search(r'\bassertion\b', s) and re.search(r'\breason\b', s):
          return 'ASSERTION_REASON'
      # 2 — MATCH (EC-13): match/list-I/column stems, OR (v2.24.2) a CROSS-DOMAIN label-pair
      #     option shape. The option-shape backstop is language-agnostic and table-safe (see
      #     _opts_are_match_pairs): it catches non-English matches and matches whose List-I/
      #     List-II body has moved into a Word table. Placed AFTER the keyword rules it is
      #     additive/monotone — it only converts a would-be non-MATCH class to MATCH.
      if re.search(r'\bmatch\b', s) and re.search(r'\b(following|list|column|set)\b', s):
          return 'MATCH'
      if re.search(r'list[\s\-]*i\b|column[\s\-]*(i|a)\b', s):
          return 'MATCH'
      if _opts_are_match_pairs(opts):
          return 'MATCH'
      # 3 — SEQUENCE / ORDERING (v2.23): the OPERATION is arranging (kept above STATEMENT).
      if re.search(r'\b(arrange|rearrange|correct sequence|proper sequence|correct order|'
                   r'logical order|chronological order|sequence of the following|'
                   r'order of the following)\b', s):
          return 'SEQUENCE'
      # 4 — STATEMENT-BASED (EC-9): "consider the following statements … which is/are correct"
      #     with combination-label options (the EC-A option-shape signal confirms it).
      if re.search(r'consider the following statements?|following statements?\b', s) and \
         (re.search(r'which .*(is|are) (correct|true|incorrect|false)', s)
          or _opts_are_combination_labels(opts)):
          return 'STATEMENT'
      # 5 — FILL_BLANK / CLOZE (EC-11): a blank to complete.
      if q.get('blank_pos', 'none') not in ('none', None) or re.search(r'_{3,}|\bfill in the blank', s):
          return 'FILL_BLANK'
      # 6 — ODD_ONE_OUT: genuine "which does not belong" classification (narrowed — mere
      #     negative phrasing is is_negative, handled orthogonally, not this class).
      if re.search(r'\bodd one out\b|does not belong|which one is different|find the odd', s):
          return 'ODD_ONE_OUT'
      # 7 — DIRECT: residual floor.
      return 'DIRECT'

  def tag_axes(q):
      """Attach the three exclusive axis labels to a question dict in place. is_negative is
      already set during extraction (EC-12). Idempotent."""
      q['axis1'] = classify_axis1(q)
      q['axis2'] = classify_axis2(q)
      q['axis3'] = classify_axis3(q)
      return q

  # v2.5 — is_negative re-derivation for the negative-rate WARN. MUST match Step 5 EC-12
  # BYTE-FOR-BYTE so the target (Step 6, from Step 5) and the realized rate (here) are counted
  # the SAME way. Step 5 EC-12 is: bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b',
  # full_stem)) — UPPERCASE only (exam convention capitalises the negative marker), no re.I,
  # exactly these 5 terms. Do NOT broaden it (case-folding / extra terms) or the rates diverge
  # and every window fires a false WARN. SOFT signal only; negativity is orthogonal to Axis-2.
  def derive_is_negative(q):
      s = (q.get('stem_raw') or q.get('stem') or '')
      return bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', s))
  ```

  USAGE (in S6-0, once per question, from the docx parse — NOT from any Step-7 sidecar):
  ```python
  qa = {'stem_raw': stem_text, 'options': option_texts, 'is_msq': (answer_cardinality == 'multi'),
        'image_role': image_role_for_q, 'linked_group_id': linked_group_id_for_q,
        'blank_pos': blank_pos_for_q}
  tag_axes(qa)                          # → qa['axis1'], qa['axis2'], qa['axis3']
  qa['is_negative'] = derive_is_negative(qa)
  # stored on the §9 ledger entry (S9-1): axis1, axis2, axis3, is_negative.
  ```

## S6-2 — Generic checks (EVERY question, every class)

  B-SOLVE (§11): independently solve/derive the intended answer from the stem +
     attached artefacts ALONE. Unsolvable, or answer not among the options → defect.
     v1.2: for a multi (MSQ) question the derivation yields a SET S of correct option
     positions (every option independently judged correct/incorrect from first
     principles); S not derivable, or any in-set value not among the options → defect.
     v1.4: for a NAT (numerical) question the derivation yields a VALUE (no options to
     match against); unsolvable, or a value the stem does not uniquely determine → defect.
     The value is compared NUMERICALLY within tolerance (ND13) — OMML fractions parsed to a
     rational, units stripped — never by string equality; integer NAT = exact, real NAT =
     within ca_range.
  B-UNIQUE (RA-12 / R-ANSWER): answer_type/answer_cardinality-parameterised (re-derived from blueprint).
     SINGLE: exactly ONE option is defensible under EVERY reasonable reading. A second
     defensible option (ambiguous relation, contested convention presented as two option
     forms, two rules each yielding a listed option, rounding that makes two options
     "match") → defect → §8 disambiguate or replace the colliding option. MULTI: the
     re-derived set S must satisfy RA-12 multi — a non-empty proper subset (1≤|S|≤n−1,
     |S|=msq_k when fixed) with every in-set option defensible; if the paper's rendered
     option set makes an out-set option also defensible, that is the MULTI ambiguity
     defect. NUMERICAL (v1.4): the re-derived VALUE must be uniquely determined by the stem
     — two defensible values under a fair reading (ambiguous rounding, under-specified
     figure, missing unit) is the NAT analogue of the two-defensible-answers defect → §8
     disambiguate the stem. Checked for EVERY question, no exception.
  B-DISTRACT: every OUT-set option is INDEFENSIBLE under any reasonable reading, and
     traces to a named error path appropriate to the class (computational slip /
     wrong-formula / converse-error / near-miss vocab / one-rule grammar violation /
     adjacent-but-wrong fact). SINGLE: the other (OPTIONS_COUNT − 1) options. MULTI: the
     (OPTIONS_COUNT − |S|) options not in S. A distractor that is "sort of right" is a
     B-UNIQUE failure in disguise (single: a 2nd defensible option; multi: a borderline
     out-set option that should arguably be in S). NUMERICAL (v1.4): N/A — a NAT question
     has no options, hence no distractors to adjudicate (the analogue "wrong values students
     compute" lives in Step 9's common-pitfalls, not in the audited paper).
  B-STEMOPT (R17): options are grammatically + logically consistent with the stem;
     option-length parity (no single option wildly longer/shorter as an answer tell);
     no answer leakage from stem to options.
  B-OPTREF-SEM (R-OPTREF): the SEMANTIC half of A-OPTREF — the escape/terminal option
     the stem references is not only PRESENT (machine) but CORRECT in meaning and
     position, and the instruction template matches the option structure. Escape tokens
     are read from section_rules (RA-9), never hardcoded.
  B-FACT (RA-11 — LIVE, EVIDENCE-SAVED, CONTEXT-DISCIPLINED): every current-affairs /
     static-GA fact and every factual option is web-verified at audit time. The search
     query necessarily contains the fact (permitted to the search tool only — MANDATE 0).
     SAVE the raw result (query + URL + retrieval-time + snippet) to
     evidence/facts/q{n}_*.json and record its path in ledger.entries[q].fact_sources[].
     S5-1A C5 verifies the file exists, parses, and carries all four fields — a bare URL
     string does not certify, and neither does a touched stub. Never certify from memory.
     v2.14 (B3): the raw result goes to DISK and ONE verdict line is carried forward
     (RA-11 a/b/c). Consult ledger.fact_cache BEFORE searching: a concept already
     verified in this mock is reused by path, never re-searched. Where the options are
     same-domain claims, one grouped query may settle the set and the saved file holds a
     LIST of per-option records. Use this writer so the record shape cannot drift from
     what C5 asserts:

     ```python
     import json, os, re, hashlib
     from datetime import datetime, timezone

     def _concept_key(text):
         """Normalised cache key. Case/punctuation/whitespace-insensitive so the same
         claim asked two ways hits once. MANDATE 0: the key stays in /home/claude."""
         return hashlib.md5(re.sub(r'[^a-z0-9 ]+', '',
                                   (text or '').lower()).strip().encode()).hexdigest()[:16]

     def save_fact(evidence_dir, q, records, cache, concept):
         """Write ONE fact-evidence file and return (path, reused).
         records : [{query, url, retrieved_at, snippet}, ...] — one per claim settled
                   (the keyed fact and/or each option). EVERY field is mandatory and
                   must be non-blank; S5-1A C5 fails the audit otherwise.
         cache   : ledger.fact_cache — {concept_key: saved_path}. A hit returns the
                   EXISTING path and performs no search (RA-11 b)."""
         k = _concept_key(concept)
         if k in cache and os.path.exists(cache[k]):
             return cache[k], True                      # reuse; C5 accepts sharing
         d = os.path.join(evidence_dir, 'facts')
         os.makedirs(d, exist_ok=True)
         p = os.path.join(d, f'q{q}_{k}.json')
         for r in records:                              # fail LOUDLY here, not at C5
             miss = [f for f in ('query', 'url', 'retrieved_at', 'snippet')
                     if not str(r.get(f) or '').strip()]
             assert not miss, f'B-FACT record for q{q} missing/blank: {miss}'
         with open(p, 'w', encoding='utf-8') as fh:
             json.dump(records, fh, ensure_ascii=False, indent=1)
         cache[k] = p
         return p, False

     def fact_line(q, ok, url, retrieved_at):
         """The ONLY thing that enters the reasoning stream (RA-11 a). MANDATE-0 safe:
         Q-number, verdict, domain, date — never the fact itself."""
         dom = re.sub(r'^https?://([^/]+).*$', r'\1', url or '')
         return f"q{q} · {'VERIFIED' if ok else 'UNSOURCED → RG'} · {dom} · {retrieved_at}"
     ```
  B-LEAK (inter-question): a question's correct numeric/fact answer does not appear as a
     GIVEN quantity/fact in another question's stem in the same mock (cross-question
     leakage). Checked mock-wide at Phase 3 using the ledger's recorded answers. v1.2:
     for a multi question EVERY value in the re-derived set is checked (the ledger stores
     answer_fact_values as a list), not just one — a leaked member is still a leak. v1.4:
     for a NAT question the re-derived VALUE is checked the same way (a leaked numerical
     answer appearing as a given elsewhere is a leak), compared numerically within tolerance.

## S6-3 — Class-specific checks

  C-COMPUTATIONAL:
    [ ] Re-solve from scratch; keyed value is exact (or stem says "rounded to k dp"
        AND options are consistent with that rounding).
    [ ] Every distractor = a specific, nameable error (sign slip, wrong formula,
        unit confusion, off-by-one) — listed in the ledger, not invented noise.
    [ ] No two computational questions in the mock share the SAME archetype AND the
        SAME seed values (observable scenario dup — B-SCENARIODUP).

  C-FORMAL-LOGIC:
    [ ] Execute the formal rule (Venn/traversal/causal/sufficiency) independently;
        keyed option follows; no second option follows.
    [ ] Option set EXACTLY matches wrong_option_structure.fixed_option_texts in the
        EXACT order section_rules specifies — never rephrased, never reordered.
    [ ] For "only one of the conclusions holds" cases, an "Only I"/"Only II"-type
        singleton option exists (not only combined options) — read the permitted set
        from section_rules.

  C-FACTUAL (RA-11 — live web-verification, never memory; B3 context discipline):
    [ ] Check ledger.fact_cache FIRST (RA-11 b). A concept already verified in this mock
        is REUSED by path — do not search it again. Record the reuse; C5 accepts one
        saved file referenced by several questions.
    [ ] Web-verify the KEYED fact with a citable, current source; SAVE query+URL+
        retrieval-time+snippet via save_fact() and record the path in the ledger (never
        in chat — MANDATE 0). Carry forward fact_line() ONLY (RA-11 a).
    [ ] Web-verify EVERY option is a real, same-domain fact; a distractor must be a
        genuine adjacent fact, not an invented one. Where the options are same-domain,
        ONE grouped query may settle the set and the saved file holds a LIST of
        per-option records (RA-11 c); split per-option only where the grouped result
        leaves an option unsettled. Every option is still verified.
    [ ] Currency: a fact that has changed since section_rules' analysis window is
        treated as current-affairs and re-verified; a stale "current" fact → defect.
    [ ] A fact that cannot be sourced → defect → regenerate with a sourceable fact.
    [ ] Minimum/permitted current-affairs count + recency window, IF section_rules
        declares one, is checked; else skipped (RA-9 — never a hardcoded count).

  C-VOCAB-ITEM:
    [ ] Key is correct in the sentence's CONTEXT; no distractor is a valid answer in
        ANY context.
    [ ] If 'sentence_embedded_underlined': the target is a real <w:u> run (already
        A-UNDERLINE) AND it is the correct span.
    [ ] Presentation variety (B-PRESENTDUP, observable form of G-FORMATDUP): two
        same-concept vocab questions must not share BOTH stem-format AND distractor
        strategy AND be adjacent. Read the family/menu from section_rules; this is the
        OBSERVABLE re-derivation (the concept_map is not delivered — §10).
    [ ] Cross-mock: the target item not used in a prior mock (registry
        content_tracking.vocab_words_used) — A-DUP backstop.

  C-GRAMMAR:
    [ ] Re-derive the single correct transformation/correction; the source sentence is
        itself correct where the task assumes it.
    [ ] Each distractor violates exactly one rule; meaning is preserved where the task
        requires (narration/voice).
    [ ] Escape option ("No improvement"/"No error") present where the template
        promises it, and genuinely correct in ~its expected share (B-OPTREF-SEM).

  C-LINKED (in addition to A-STIMORPHAN structural pass):
    [ ] Every member is answerable from THIS member's embedded stimulus ALONE (no
        outside knowledge; no reference to another question) — B-PASSAGE.
    [ ] The keyed answer is derivable from the stimulus, not contradicted by it; the
        passage↔question linkage is correct (a mis-linked passage makes every member
        wrong — re-solve each member from its own embedded stimulus).
    [ ] CLOZE: every blank covered by exactly one member; no blank uncovered; no blank
        asked twice; the numbered blank the member asks for actually exists in the
        embedded passage.
    [ ] Each member's sub-skill is distinct (the CLASS-4 exception: shared stimulus is
        allowed, but members must not be the same question twice).

## S6-4 — Allocation, mandate & intra-mock dedup (observable; verified per S6 + Phase 3)

  B-ALLOC: tally questions per subtopic (mapping each question to its subtopic_id by
     matching its content to section_rules patterns + the manifest) and compare to
     blueprint mock_obj subtopic_allocations q_count. Any subtopic count ≠ its
     blueprint q_count → defect (over → regenerate the extra as a different needed
     subtopic; under → the missing subtopic is absent → regenerate). SECTION totals
     are A-SECCOUNT (machine); PER-SUBTOPIC is this manual mapping (the concept_map is
     not delivered, so the mapping is re-derived).
  B-MANDATE: every subtopic in manifest.mandatory_every_mock appears ≥1× in the mock;
     no two members of any manifest.alternation_groups co-occur in the mock. Read from
     the manifest (RA-9).
  B-SCENARIODUP (observable G-CONCEPTDUP): no two questions in the mock are the same
     scenario (same computation on the same seed values; same fact in different
     wording; same vocab target; same figural transformation). Re-derived from the
     rendered content + the ledger, since the concept_map is not delivered.
  B-PRESENTDUP (observable G-FORMATDUP + R19): no two same-family questions share BOTH
     stem-format AND distractor strategy; no contiguous run > 2 of the same
     presentation family; a subtopic's N questions are distributed, not clustered.
  These four are TALLY/scan checks completed across the whole mock; per-batch they are
  populated into the ledger, and they are FINALISED at Phase 3 (when every question has
  been classified). A failure → §8 regeneration (never count reduction — RA-8).

## S6-5 — Difficulty (advisory unless section_rules makes it hard)

  B-DIFF: estimate difficulty per question using blueprint.difficulty_labels (tag every
     estimate [estimate]) and compare the per-section distribution to blueprint difficulty_schedule[N]. Interleaving:
     no excessively long run of Hard (or of Easy) within a section. v1.2: mirror Step 0
     E-9 — a multi (MSQ) question carries an additional difficulty-load term (selecting an
     exact SET is harder than picking one option), so an MSQ should not be estimated below
     the band its single-answer analogue would receive; treat this as advisory input to the
     estimate, not a separate gate. A shortfall is a generation-quality FINDING logged in
     the report; it blocks SHIP only if section_rules/blueprint marks the difficulty mix as
     a hard requirement (RA-9).

## S6-6 — Format distribution / THREE-AXIS audit (advisory; mirrors S6-5 — v2.5)

  The mirror of B-DIFF for FORMAT. Step 8 has re-tagged every shipped question with the
  Step-5 AXIS CLASSIFIER v1.0 (S6-1b) and stored axis1/axis2/axis3/is_negative on the ledger.
  This section aggregates the realized per-section distribution over the current 10-mock
  WINDOW (registry.axis2_audit, Step 8's independent tally) and compares it to the blueprint
  axis_schedule target. Like B-DIFF, a shortfall is a generation-quality FINDING logged in the
  report; it blocks SHIP only if section_rules/blueprint marks the format mix a HARD requirement.

  INERT when blueprint has no axis_schedule (pre-v1.23) OR a section's schedule status != 'ok'.
  The audit FIRES ONLY AT WINDOW CLOSE (this mock is the last of its window), from the FINAL
  fixed docx — a partial mid-window mock only ACCUMULATES (Phase 3), it does not yet judge.

  ```python
  def axis_window_is_closing(N, window, total_mocks):
      """True iff mock N is the last mock of its 10-mock window (a full window boundary,
      or the final mock of the run when the last window is partial)."""
      if total_mocks is not None and N >= total_mocks:
          return True
      return (N % max(1, window)) == 0

  def _axis_tolerance(target):
      """decision 10: per-format window tolerance = ±1 OR ±15% of target, whichever is LARGER."""
      return max(1.0, 0.15 * float(target))

  def audit_axis2(section_name, sched, realized_counts, scale=1.0):
      """B-AXIS2 — per-section, per-format, per-window (advisory FINDINGS list).
         realized_counts = {AXIS2_CLASS: n} accumulated over the window (Step 8's tally).
         scale     = mocks_in_window / AXIS_WINDOW — scales band targets so a PARTIAL final
                     window (total_mocks not a multiple of the window) is judged fairly.
         band    : |realized − scaled_target| ≤ max(1, 15%·scaled_target)   → else FINDING
         guarantee: realized ≥ 1 over the window                            → else FINDING
         DIRECT  : floats — never audited (residual filler, decisions 5/10)."""
      findings = []
      if not sched or sched.get('status') != 'ok':
          return findings                                   # inert section
      band  = sched.get('axis2_window_target', {})          # {cls: per-FULL-window quota}
      guar  = sched.get('axis2_guarantee', [])              # [cls] must appear ≥1/window
      feas  = sched.get('guarantee_feasibility', {})        # pyq_covered|zp_only|unsatisfiable
      for cls, tgt in band.items():
          if cls == 'DIRECT':
              continue                                       # floats
          stgt = float(tgt) * scale                          # partial-window-scaled target
          have = realized_counts.get(cls, 0)
          if abs(have - stgt) > _axis_tolerance(stgt):
              findings.append(f"B-AXIS2 [{section_name}] band '{cls}': realized {have} vs "
                              f"target {stgt:.1f} (tol ±{_axis_tolerance(stgt):.1f}/window) — FINDING.")
      for cls in guar:
          if realized_counts.get(cls, 0) < 1:
              # An 'unsatisfiable' guarantee (no capable subtopic) was ACCEPTED as absent at
              # Step 6 — report it as expected-absent, not a defect (never fabricated).
              if feas.get(cls) == 'unsatisfiable':
                  findings.append(f"B-AXIS2 [{section_name}] guarantee '{cls}': absent — "
                                  f"no capable subtopic (accepted shortfall, not fabricated).")
              else:
                  findings.append(f"B-AXIS2 [{section_name}] guarantee '{cls}': 0 in this "
                                  f"window (expected ≥1; feasibility={feas.get(cls,'?')}) — FINDING.")
      return findings

  def audit_axis13(section_name, axis_key, per_paper_target, realized_counts, window):
      """B-AXIS1 / B-AXIS3 — realized stimulus/mechanism mix vs the Step-6 per-PAPER target,
         scaled to the window and checked within the same ±1/±15% tolerance. Advisory."""
      findings = []
      if not per_paper_target:
          return findings
      for cls, avg in per_paper_target.items():
          tgt  = float(avg) * window                         # window-scaled target
          have = realized_counts.get(cls, 0)
          if abs(have - tgt) > _axis_tolerance(tgt):
              findings.append(f"B-AXIS{axis_key} [{section_name}] '{cls}': realized {have} vs "
                              f"~{tgt:.1f}/window (tol ±{_axis_tolerance(tgt):.1f}) — FINDING.")
      return findings

  def audit_axis_negative(section_name, sched, neg, total):
      """B-AXIS-NEG — negative-polarity rate is a SOFT target (decision 12): WARN only."""
      if not sched or sched.get('status') != 'ok' or total <= 0:
          return []
      rate_tgt = float(sched.get('negative_rate', 0.0))
      if rate_tgt <= 0:
          return []
      cur = neg / total
      if abs(cur - rate_tgt) > 0.10:                         # 10-point soft band
          return [f"B-AXIS-NEG [{section_name}]: negative rate {cur:.0%} vs target "
                  f"{rate_tgt:.0%} (soft ±10pt) — WARN."]
      return []

  def cross_check_step7(section_name, s8_axis2, s7_sections):
      """Consistency signal (decision A): Step 8's independently re-derived Axis-2 counts vs
      Step 7's self-reported registry.axis2_window. A large drift means the paper's actual
      structure diverged from the variant Step 7 declared (a render-fidelity WARN, not a hard
      fail). Compares only where both have data."""
      s7 = (s7_sections.get(section_name) or {}).get('counts', {})
      if not s7:
          return []
      drift = sum(abs(s8_axis2.get(c, 0) - s7.get(c, 0)) for c in set(s8_axis2) | set(s7))
      s8_total = sum(s8_axis2.values()) or 1
      if drift > max(2, 0.20 * s8_total):                    # >20% aggregate divergence
          return [f"B-AXIS2 [{section_name}] render-drift: Step-8 re-tag differs from Step-7's "
                  f"declared counts by {drift} (>20%). Check RENDER-CONSISTENCY (Step 7 G4) — WARN."]
      return []
  ```

  HARD-vs-advisory (RA-9 parallel): every FINDING/WARN above is ADVISORY and logged in the
  report by default. It escalates to a SHIP-blocking defect ONLY when section_rules/blueprint
  declares the format mix a hard requirement (the same switch B-DIFF uses for difficulty).
  A window-distribution shortfall is never "fixed" by editing one mock — it is reported so the
  series self-corrects; a per-question RENDER mismatch (cross_check drift) points at the
  specific Step-7 fidelity bug to fix in the next generation.


# ════════════════════════════════════════════════════════════════════════
# §7 — VISUAL & STRUCTURED-CONTENT DEEP AUDIT (the no-gaps section)
# ════════════════════════════════════════════════════════════════════════
#   GOVERNING RULE (RA-4): a visual or structured artefact is audited ONLY by being
#   RENDERED-AND-VIEWED (images, charts) or PARSED-AND-RECOMPUTED (tables, matrices,
#   OMML). A check asserted from a filename, alt-text, p.text, manifest entry, or
#   "looks present" is VOID and the artefact counts as un-audited — which BLOCKS
#   delivery (RA-19, §18). This runs inside Phase-2 batches (STEP B). Exam-agnostic:
#   the qtypes/object-types/transformations come from section_rules
#   PYQ_IMAGE_ANALYSIS / PYQ_PASSAGE_STRUCTURE — never a hardcoded list.
#   v2.6 — EVERY view/recompute MUST leave a durable evidence artefact on disk (the
#   montage PNG that was viewed; the recompute trace) and record its path in the §9
#   ledger entry. S5-1A C6/C7 verify those files exist and are non-trivial. A stamp
#   with no backing file is treated as un-audited (RA-4).

## S7-1 — IMAGES & FIGURES — every single one rasterised and VIEWED

  COVERAGE: every inline image in the mock (from the P6 index), whether or not it is
  in registry.figural_manifests. A figural question is identified by (a) the manifest
  figural_qs, UNION (b) re-derivation from stem cues (section_rules figural cue set).
  An image present but unaccounted-for, or a figural cue with no image, is itself a
  defect.

  LAYER A — provenance & structure (machine; from §5 A-FIGCOMP + A-MATHRASTER Tier 1):
    [ ] every image rId resolves to an existing media part (A-ZIP).
    [ ] figural block is DECOMPOSED: problem image(s) + exactly one image per option,
        single-column, one image per line, each bound 1:1 to its option label; NO
        composite panel; NO "Figure k" dummy-text option (A-FIGCOMP / R-FIGURAL).
    [ ] no inline image is a rasterised algebraic expression (A-MATHRASTER; the VIEW
        in Layer B is the authority — S5-3).
    [ ] image naming: legitimate figures carry (or are renamed to) the canonical
        q{N}_problem / q{N}_opt{i} / q{N}_stim contract (CP-IMGNAME).

  LAYER B — actual visual content (VIEW every image; zero sampling; the authority):
    Render each question's problem + option images as a montage (PIL: problem top,
    options stacked/grid), SAVE the montage to evidence/montages/q{N}_montage.png, and
    VIEW it with the view tool. Record the montage path + 'rendered-and-viewed' stamp
    in the ledger (S5-1A C6 reads it). Per qtype (read from section_rules / figural
    manifest), verify:
    UNIVERSAL (all figural):
      [ ] resolution ≥ FIGURAL_DPI (300); no grey boxes, no clipping, no corrupted
          pixels; uniform per-option canvas; NO stem/caption/option-number/instruction
          baked into any raster (only intrinsic annotations — mirror-line endpoints,
          vertices, axis labels — belong inside).
      [ ] within-question: every option image is visually DISTINCT from the others
          (dHash Hamming separation); no two identical option figures.
      [ ] figure ↔ stem agreement: every value/label/landmark the stem references is
          present in the image and consistent with it; a label that contradicts the
          stem is a defect (regenerate figure AND dependent values together).
    TRANSFORMATION-SPECIFIC (the qtype set is read from section_rules; examples of the
    universal checks the framework applies to whatever types the exam declares):
      [ ] the stated transformation is ACTUALLY TRUE for the keyed option (a mirror is a
          real reflection about the stated line; a fold yields the keyed hole pattern; a
          series rule continues in exactly the keyed figure; an embedded target sits in
          the key WITHOUT rotation when rotation is barred; an odd-one-out has exactly
          one figure breaking the shared property; a net folds to the keyed solid).
      [ ] UNIQUENESS: no distractor also satisfies the rule (two valid figures = defect).
      [ ] DISTRACTORS verified to BREAK the rule (and, for embedded/odd-one-out, to NOT
          contain the target / to share the property).
      [ ] placement/rotation instructions the qtype requires are present in the stem
          (e.g. mirror line, "rotation is not allowed").
    CROSS-MOCK (RA-13): hash word/media/ directly (registry image_hashes may be empty);
      every image's dHash/MD5 is sufficiently distant from every registered prior-mock
      image; no figural concept repeats a prior mock's recorded pattern (registry
      content_tracking / figural_manifests).
    FIX: any Layer-B failure → re-render the figure(s) (or regenerate the question)
      under the Step-7 §10-S10-7/S10-8 contracts, then RE-VIEW (a re-rendered image is
      not certified until viewed again — re-save the montage). Stamp 'rendered-and-viewed'
      in the ledger with the montage path.

## S7-2 — TABLES & DI SETS — parsed to a grid and RECOMPUTED

  For every Word table (DI/caselet/matching) in the paper:
    [ ] it is a REAL <w:tbl> object — not plain-text columns faked with spaces/tabs
        (a text-grid masquerading as a table is a defect → rebuild as a real table).
    [ ] read it cell-by-cell into a structured grid; row/column headers + units are
        present and unambiguous.
    [ ] internal consistency: if a Total/Subtotal/Average row or column is shown,
        RECOMPUTE it from the cells and confirm it matches (a printed total that does
        not add up is a defect).
    [ ] SELF-CONTAINMENT (A-STIMORPHAN): for a linked DI set, the table is embedded in
        EVERY member's block (Model A), re-emitted as a real table object — not "the
        table above".
    [ ] RE-SOLVE every dependent question FROM THE TABLE'S OWN NUMBERS: confirm the
        keyed answer follows from the grid and is UNIQUE. A DI table whose values do
        not actually yield the keyed answer is the most dangerous table defect →
        regenerate table AND dependent answers together.
    v2.6: write the parsed grid + the recomputed totals/derivations to
    evidence/recompute/q{N}_table.txt and record the path + 'recomputed' stamp in the
    ledger for the table and each dependent question (S5-1A C6 reads it).

## S7-3 — MATRICES & MATCH-THE-COLUMN

  [ ] rendered as a real grid/table (S7-2 structural checks apply).
  [ ] option format matches the label scheme section_rules declares (e.g. letter-roman
      vs number-letter) — read, never assumed.
  [ ] RE-DERIVE every pairing independently; exactly one option has ALL pairings
      correct; each distractor contains ≥1 demonstrably wrong pairing (B-DISTRACT).
  [ ] no second option is also fully correct (B-UNIQUE).
  Stamp 'recomputed' with the evidence/recompute/ trace path.

## S7-4 — CHARTS / GRAPHS

  [ ] a stem that references a chart/graph has a REAL rendered image for it (a "chart"/
      "graph" keyword with no inline image is a defect).
  [ ] VIEW the chart (save the montage); axes, labels, legend, units, scale are present
      and consistent with the stem; data series are legible.
  [ ] SELF-CONTAINMENT: the chart image is embedded in every dependent member (Model A).
  [ ] RE-SOLVE every dependent question by READING VALUES off the chart; keyed answer
      follows and is unique (save the derivation to evidence/recompute/).
  Stamp 'rendered-and-viewed' (montage path) + 'recomputed' (trace path) for dependents.

## S7-5 — OMML MATHS — extracted from the math XML, RECOMPUTED, render-verified

  Text extraction is blindest here, so this is the deepest check.
    [ ] ROUTING (R-MATH-OMML): every built-up expression (stacked fraction, exponent,
        radical, trig-with-fraction) is native <m:oMath> — NOT a raster (A-MATHRASTER)
        and NOT slash/caret ASCII (A-FRAC). Scan inline images for math smuggled as a
        picture and the text stream for slash/caret fallbacks. (Observed in the wild:
        zero <m:oMath> in a paper that has a quantitative section is a live flag — math
        is hiding as ASCII or raster — resolve it, never wave it past.)
    [ ] STRUCTURE (A-OMML): every <m:f> has a non-empty numerator AND denominator; no
        year-range "YYYY/YY" rendered as a stacked fraction (use an en-dash); radicals/
        scripts well-formed; the OMML floor (≥1 <m:oMath> when any subtopic is
        OMML_required) holds.
    [ ] SEMANTICS: reconstruct each expression FROM THE OMML TREE (not p.text), and
        RECOMPUTE the question; the math is correct AND the keyed option is the unique
        result. A perfectly-rendered fraction that makes the answer ambiguous is still a
        B-UNIQUE defect.
    [ ] RENDER-VERIFY: where structure is subtle, rasterise the page region and VIEW it
        to confirm it displays as intended (save that raster to evidence/montages/).
    FIX: a math defect → CP-MATHOMML re-render via the Step-7 §10-S10-4 add_math_stem /
      emit_math_inline path (interleave <m:oMath> with the stem text) and drop any
      raster/ASCII; if a flagged image was a genuine figure mis-named with a math token,
      re-emit it canonically (CP-IMGNAME). Stamp 'recomputed' (+ 'rendered-and-viewed'
      where render-verified) with the evidence path.

## S7-6 — The §7 completeness gate (feeds Phase-3 certification)

  At Phase 3, EVERY image must carry a 'rendered-and-viewed' stamp naming a montage file
  that EXISTS, EVERY table/matrix/chart and EVERY OMML expression a 'recomputed' stamp
  naming a trace file that EXISTS, in the ledger. Any artefact lacking its required stamp
  OR whose named evidence file is missing/trivial = an un-audited visual/structured item
  = SHIP is BLOCKED (RA-4 / RA-19 / §18 / S5-1A C6/C7). There is NO sampling and NO
  "[not-viewed]" exemption.
  v2.16 (D2) — THE ONE EXCEPTION, AND IT IS MEASURED, NOT CLAIMED. An image artefact
  may carry 'view-unavailable' when, and only when, a P3.5 probe FAILED for that batch
  AND its montage exists at >= EVIDENCE_MIN_BYTES. Such a paper certifies DEGRADED —
  never clean — exits 0, and ships under an F1 AMBER footer with a §R13 limitation.
  Absent a failed probe, or with a missing/trivial montage, the sentence above stands
  unchanged and SHIP is BLOCKED. Vision degradation is never an operator's word.

# ════════════════════════════════════════════════════════════════════════
# §8 — RECTIFICATION ENGINE (fix in place; regenerate under Step-7 contracts)
# ════════════════════════════════════════════════════════════════════════
#   Every defect is FIXED in this session (RA-5). Two fix classes:

## S8-1 — Class CP — CONTENT-PRESERVING fixes (do not change the correct option)

  Applied in Phase 1 (paper-wide) and as leftovers per batch. They edit the docx
  directly; no re-solve needed because the answer is unchanged.
    CP-FONT      → set every run to Calibri 11 (R24).
    CP-OPTLABEL  → relabel options to option_label_format (R10).
    CP-SECHDR    → delete body section-heading paragraphs (R8).
    CP-ANSKEY    → remove any answer-key/marker/hint paragraph or run (R5).
    CP-QNFIRST   → re-emit the block Q.N-first: Q.N context line → stimulus →
                   non-numbered specific-ask → options → blank (R14 / §9 SC-3).
    CP-BLANKSEP  → insert the missing blank separator (R13).
    CP-UNDERLINE → split the carrier sentence into runs and apply a real <w:u> to the
                   target span; delete the "(underlined: X)" annotation (R-UNDERLINE).
    CP-MATHOMML  → re-render a built-up expression as <m:oMath> (Step-7 §10-S10-4) and
                   delete the raster/ASCII form (R-MATH-OMML).
    CP-STIMEMBED → embed the shared stimulus (passage/table/chart/cloze paragraph) into
                   every linked member's block, Model A (R-LINKED / §9 SC-3); re-emit a
                   DI table as a real table object per member, re-insert a chart image
                   per member (intra-group reuse is exempt — SC-6).
    CP-FIGDECOMP → decompose a composite figural panel into a problem image + one image
                   per option, single-column, bound 1:1 to labels (R-FIGURAL). If the
                   underlying figures are CORRECT and only the LAYOUT is composite, this
                   is CP (re-slice/re-emit). If a figure is WRONG, it is RG.
    CP-IMGNAME   → rename a legitimate-but-mis-named figure to the canonical q{N}_* part
                   name (so the provenance contract + any name-contract gate pass).
    CP-ENCODING  → re-emit a run containing U+FFFD with the correct characters.
    CP-HEADER-STRIP → delete any non-blank paragraph before Q.1 (title/info/scoring/cover).
                   The paper is questions-only (Step 7 R8b / G-PREQ1); the block is not
                   question content, so removing it preserves all content. Dormant only if
                   section_rules EXAM_STRUCTURE declares paper_header_block.
  After CP fixes, re-run Part A to confirm the targeted gate(s) are green.

## S8-2 — Class RG — REGENERATION (defect requires new content)

  When a fix cannot preserve the answer — a wrong/unsourceable FACT, TWO defensible
  answers, a WRONG figure/table value, an impossible figure, a cross-mock/intra-mock
  DUPLICATE, an allocation/mandate miss, a wrong escape-option structure — REGENERATE
  that ONE question in place. Regeneration OBEYS EVERY STEP-7 CONTRACT (RA-6):
    1. KEEP the slot: same subtopic_id (blueprint join), same section, same difficulty
       target, same format — so the blueprint allocation and mandate stay satisfied
       (NEVER delete the question to "fix" a dup — RA-8).
    2. Generate the new question from section_rules patterns + wrong_option_structure
       for that subtopic_id (the same source Step 7 used).
    3. Enforce R-ANSWER (single: one defensible answer; multi: the correct set), R17 (stem↔option coherence), R-OPTREF
       (escape coherence), R13/R14/R24 (render), and the format's render contract
       (R-LINKED / R-FIGURAL / R-UNDERLINE / R-MATH-OMML) as applicable.
    4. DEDUP the replacement against (a) the WHOLE audit ledger (§9) — every other
       question reviewed so far, this mock — AND (b) the registry (§10) — every prior
       mock, with --mockN self-exclusion. The replacement must be a NEW scenario AND a
       distinct presentation (B-SCENARIODUP / B-PRESENTDUP).
    5. For a fact: web-verify the new fact + options (RA-11) before accepting AND save
       the evidence (evidence/facts/).
    6. RE-AUDIT the regenerated question fully (Part A on its block + the full Part B/§7
       checklist for its class, re-saving its evidence) — it is NOT done while it
       carries an unreviewed change; its ledger entry status becomes 'regenerated'.
    7. Update the ledger + the derived key (§11) for the new content.
    8. RECORD THE CHANGE (S8-5) into audit_state.regenerations — captures, for this one
       question, the structural diff (for the in-chat report, content-free) AND the
       literal before→after (for the downloadable change-log artefact). This is what
       lets the report say exactly which questions were replaced and how.

## S8-3 — The re-audit loop (per batch) + global reconciliation

  After applying CP + RG fixes in a batch:
    a) re-audit every fixed/regenerated question (S8-2 step 6);
    b) re-run WHOLE-PAPER Part A (RA-7) — a fix can perturb a global invariant
       (new K-PAT run, new dup, drifted count, new orphan); resolve any new failure
       (which may itself be CP or RG) IN THIS BATCH before ending;
    c) iterate (a)–(b) until the batch's slice AND whole-paper Part A are clean.
  A regeneration that re-perturbs is re-fixed; the loop terminates because each
  iteration strictly reduces the open-defect set (a replacement is dedup-checked
  against everything, so it cannot re-introduce the same class).

## S8-4 — Repair constraints (inherited discipline)

  • Replacing a question: fresh vs ALL prior mocks AND this mock (ledger + registry).
  • Re-balancing a distractor for A-KBAL/A-KPAT: NEVER change which option is correct;
    rotate a distractor's position; re-run A-KPAT after (re-balancing can create runs);
    re-read each rebalanced option for grammatical sense. v1.2: A-KBAL/A-KPAT re-balancing
    operates ONLY on single-mode questions (multi positions are excluded from the
    single-position statistics); a multi question is never rotated to "fix" balance.
  • Repairing a multi (MSQ) question (A-MSQ-KEY / B-UNIQUE-multi / B-DISTRACT-multi):
    NEVER change one membership to silence a flag — preserve/re-form the WHOLE correct SET
    so RA-12 multi holds (non-empty proper subset, fixed-k honored, every in-set option
    defensible and every out-set option indefensible). A borderline out-set option is fixed
    by disambiguating the stem or replacing that option, exactly like the single-mode
    second-defensible-option repair. A-MSQ-INSTR is repaired by re-emitting the stem with
    the select-instruction on the Q.<n> line (never as a separate paragraph — that breaks
    A-QNFIRST).
  • Re-rendering a figure: verify the new media part is NOT byte-identical to any other
    question's image before overwriting (R3), then RE-VIEW it (§7) and re-save its montage.
  • Any built-up math in a replacement → OMML (R-MATH-OMML).
  • After ANY repair: re-run the ENTIRE relevant gate set; iterate to zero FAIL + zero
    fixable WARN. A failing question is NEVER left in the paper; the paper is never
    delivered with a known-open defect.

## S8-5 — Change-record capture (feeds the report §R5 + the change-log artefact)

  Every Class-RG regeneration (and any CP fix that materially altered a question's
  rendered form, e.g. CP-MATHOMML / CP-FIGDECOMP) appends one record to
  audit_state.regenerations. Two views are derived from the SAME record:

  STRUCTURAL view (for the in-chat report — MANDATE-0 safe, NO content):
    { q, class:'RG'|'CP', defect_code, change_class, invariants_preserved,
      reaudit:'clean', dedup:'clean' }
    where:
      • defect_code      = the code that triggered it (e.g. B-UNIQUE, B-FACT, A-DUP,
                           A-MATHRASTER, B-PRESENTDUP).
      • change_class     = a content-free description of WHAT changed, drawn from a
                           fixed vocabulary: 'scenario replaced' | 'distractor
                           rebalanced' | 'fact corrected (web-verified)' | 'figure
                           re-rendered' | 'math re-rendered as OMML' | 'option set
                           re-templated' | 'stem disambiguated' | 'stimulus embedded'.
      • invariants_preserved = the Step-7 join points kept identical so the blueprint
                           stays satisfied: subtopic_id, section, difficulty, format
                           (+ 'answer position UNCHANGED' when the fix did not move the
                           key — true for every CP fix and for distractor rebalances).
  LITERAL view (for the downloadable change-log artefact ONLY — never chat):
    { q, defect_code, before:{stem, options, key}, after:{stem, options, key},
      rationale }  — the actual old and new text, so the author can see the real diff.

  The literal view is written ONLY to /home/claude staging and emitted ONLY into
  deliverable #3 (the change-log .md, S14-1). It is NEVER printed in chat (MANDATE 0).
  If no record exists (zero regenerations), no change-log file is produced.

# ════════════════════════════════════════════════════════════════════════
# §9 — THE AUDIT LEDGER (Step 8's independent concept/answer memory)
# ════════════════════════════════════════════════════════════════════════
#   The concept_map/presentation_ledger Step 7 used is NOT delivered (S0-1). §9 is
#   Step 8's INDEPENDENT, re-derived equivalent — built as the audit proceeds, used
#   to dedup regenerations against the whole mock and to make per-batch sign-off and
#   resume honest. Stored in /home/claude/[ExamCode]_M[N]_audit_state.json (never
#   delivered, never printed — MANDATE 0). v2.6 — it is ALSO the object the Phase-3
#   COMPLETION GATE (S5-1A) validates, so its per-question entries and their evidence
#   references are LOAD-BEARING, not merely a memory aid.

## S9-1 — Ledger schema (per reviewed question)

  ledger.entries[q] = {
    subtopic_id, section, class,                # classification (S6-1)
    answer_cardinality,                                # v1.2: 'single' | 'multi' (re-derived)
    scenario_sketch,                            # MANDATE-0-safe abstraction of the
                                                #   scenario (archetype + seed sketch /
                                                #   fact-concept / vocab-target / figural
                                                #   transformation) — NOT the stem text
    presentation_family, stem_format, distractor_strategy,   # for B-PRESENTDUP
    axis1, axis2, axis3, is_negative,           # v2.5: re-derived by AXIS CLASSIFIER v1.0 (S6-1b)
                                                #   from the shipped question — feeds S6-6 audit.
    is_factual (bool),                          # v2.6: this q (or an option) carries a
                                                #   CA/static-GA fact → S5-1A C5 requires a source
    # v1.2 — answer memory is mode-aware: single ⇒ derived_answer is an int and
    # answer_fact_value a scalar; multi ⇒ derived_answer is the SORTED set (list[int]),
    # answer_set_verified records RA-12-multi pass, and answer_fact_values is the LIST of
    # every value in the set so B-LEAK scans them all (P3-1), not just one.
    derived_answer, answer_unique (bool), answer_fact_value,   # for B-LEAK / §11 (single)
    answer_set_verified (bool), answer_fact_values: [...],     # for B-LEAK / §11 (multi)
    # v2.6 — EVIDENCE-BOUND provenance (RA-19 / FIX F). Each stamp NAMES the on-disk
    # artefact that proves the Claude-driven check actually ran. S5-1A C5/C6/C7 verify
    # these files EXIST and are non-trivial — a stamp with no backing file is un-audited.
    fact_sources: [ {url, date, saved: "evidence/facts/q{n}_k.json"}, ... ],  # C-FACTUAL
    artefact_stamps: {
        images:   [ {rid_or_name, stamp:'rendered-and-viewed', montage:"evidence/montages/q{n}_montage.png"} ],
        tables:   [ {idx, stamp:'recomputed', trace:"evidence/recompute/q{n}_table.txt"} ],
        charts:   [ {idx, stamp:'rendered-and-viewed'+'recomputed', montage:..., trace:...} ],
        omml:     [ {idx, stamp:'recomputed', trace:"evidence/recompute/q{n}_omml.txt"} ]
    },
    status: 'pending' | 'verified' | 'regenerated'   # opened 'pending' at S6-0.7; closed
                                                     # only when every applicable check ran
  }
  Plus rollups: scenarios[], presentations[], vocab_targets[], facts[], image_hashes[].
  v2.14 (B3): ledger.fact_cache = {concept_key: saved_path} — the mock-wide
  concept->evidence map RA-11 (b) consults BEFORE any search, so a claim shared by
  several questions is verified ONCE and reused by path. It is INTERNAL (never
  delivered, never printed) and is rebuilt on resume with the rest of the ledger.
  S5-1A C5 reports how many distinct source files back how many references, so cache
  reuse is visible as reuse and can never be mistaken for a coverage shortfall.

## S9-2 — How the ledger is used

  • REGENERATION dedup (§8-2 step 4): a replacement's scenario_sketch + presentation must
    not collide with ANY ledger entry (whole mock), not just the current batch — this is
    what stops a batch-K regeneration from semantically colliding with a batch-1 question
    the machine cannot see.
  • B-SCENARIODUP / B-PRESENTDUP (§6-4): finalised at Phase 3 by scanning the ledger.
  • B-LEAK (§6-2): finalised at Phase 3 from ledger.derived_answer / answer_fact_value
    (single) and ledger.answer_fact_values (multi — every value in the set is scanned).
  • RESUME (RA-18): the ledger is reloaded; reviewed questions are not re-reviewed; the
    whole-paper Part A still runs each resumed batch; the evidence dir persists.
  • STAMPS (RA-19): artefact_stamps + their evidence files feed the §7-6 / §18 / S5-1A
    certification gate — presence AND backing-file existence are both checked.
  • COMPLETION GATE (S5-1A): reads entries.keys() (C2), status (C3), answer_unique /
    answer_set_verified (C4), fact_sources + saved files (C5), artefact_stamps + montage/
    trace files (C6), and coverage totals (C7). The ledger is the contract between the
    Claude-driven audit and the machine gate that certifies it.

# ════════════════════════════════════════════════════════════════════════
# §10 — CROSS-MOCK DEDUP (registry-based; full; self-excluding)
# ════════════════════════════════════════════════════════════════════════

## S10-1 — Scope

  Cross-mock dedup runs FULLY (RA-13) — Step 8 HAS the registry. A-DUP (machine) +
  the §6 content checks together cover it. --mockN N self-excludes mock N's own stems
  (re-auditing the registered mock must not flag it against itself; the registry
  already contains mock N because Step 7 appended it — S2-2 guards alignment).

## S10-2 — What is checked against the registry

  [ ] STEM dedup: each mock-N stem vs every PRIOR-mock stem in registry.stem_texts —
      exact match = defect; near-match (token Jaccard ≥ J_FAIL, default 0.75) = defect;
      borderline (J_WARN..J_FAIL, default 0.60–0.75) = read both, document if genuinely
      distinct else regenerate. (Self-exclude same-mock via --mockN.)
  [ ] IMAGE dedup: hash word/media/ DIRECTLY (registry image_hashes may be empty) —
      no MD5/pHash match to a registered prior-mock image (R3 cross-mock).
  [ ] CONTENT-TRACKING blind spots (registry.content_tracking L4–L18): vocab targets,
      GA facts (concept level), numeric seeds, analogy schemes, idioms, grammar rules,
      computer/domain facts, cause-effect domains, syllogism domains, option sets,
      passage/cloze topics — none repeats beyond its allowed frequency. These are the
      checks G-DUP is blind to (figural, <5-token stems, concept echoes); they are done
      from the registry + the ledger.

## S10-3 — Registry as the dedup source of truth

  RS-10 (Step 1): the registry MUST be replaced in project knowledge after each Step-7
  session. If the registry handed to Step 8 lags (mocks_completed missing an earlier
  mock, or stem_texts count ≠ Σ prior mock sizes), cross-mock dedup is PARTIAL — record
  it as a §15/§19 limitation (NOT a content defect; not fixable at Step 8) and proceed
  with the dedup the registry supports. S2-2 already hard-stops the worst case (registry
  not ending in mock N).

# ════════════════════════════════════════════════════════════════════════
# §11 — ANSWER DERIVATION & UNIQUENESS (no key delivered — solve it)
# ════════════════════════════════════════════════════════════════════════

## S11-1 — Independent solve

  Step 8 receives NO answer key (S0-1). For every question it INDEPENDENTLY derives the
  intended answer from the stem + attached artefacts + (for facts) live web sources. The
  derived key is stored in audit_state.derived_key {q: option_index} — INTERNAL, never
  delivered (the learner key is a Step-9 artefact), never printed (MANDATE 0).

## S11-2 — What the derived key is FOR

  • B-UNIQUE: confirm exactly one option is defensible (the derivation must land on one,
    and only one, option). If the derivation finds TWO defensible options → R-ANSWER (single)
    defect → §8 disambiguate/replace.
  • B-DISTRACT: confirm the other options are wrong.
  • A-KINT/A-KBAL/A-KPAT: run the key-health gates against the DERIVED key (the only key
    Step 8 has). These are advisory→fix: a balance/run defect is fixed by rotating a
    DISTRACTOR (never changing the correct option — §8-4). A-KBAL/A-KPAT operate over
    single-mode questions only.
  • (multi only) A-MSQ-KEY: the re-derived set is a non-empty proper subset (fixed-k +
    AOTA rules honored); A-MSQ-INSTR: the per-section multi instruction count matches the
    blueprint. Both dormant when no subtopic is answer_cardinality=='multi'.
  • B-LEAK: the derived answer values feed the inter-question leakage scan (every value in
    a multi set, not just one).

## S11-3 — Boundary with Step 9

  Step 8 does NOT deliver or certify the learner-facing key — Step 9 (MockExplain)
  independently re-derives and publishes it. Step 8's derivation exists to AUDIT
  (uniqueness, correctness, balance), and to ensure that when Step 9 solves the paper it
  will find exactly one defensible answer per question. A divergence between Step 8's
  derived key and a (future) Step-9 key on a question that Step 8 certified as unique is
  a Step-9 escalation, not a Step-8 deliverable.

# ════════════════════════════════════════════════════════════════════════
# §12 — VERDICT & CERTIFICATION (Step 8 ships only a clean paper)
# ════════════════════════════════════════════════════════════════════════

## S12-1 — There is no "DON'T SHIP" terminal state

  Unlike a pure auditor, Step 8 RECTIFIES (RA-5). "DON'T SHIP" is never a final
  outcome — a found defect triggers §8 repair-and-re-audit until clean. The only
  outcomes are: CERTIFIED CLEAN (deliver) or HARD STOP (a pre-flight/integrity
  blocker that prevents auditing at all — e.g. missing input, corrupt/truncated input
  (P0.5), failed hardened self-test (P1), unresolvable rId, N-disagreement; these
  require user action, not a verdict).

## S12-2 — Certification gate (Phase 3, all must hold)

  [ ] audit.py --final --audit-state <path>  →  "COMPLETION-GATE: PASS"  (S5-1A).
      (v2.6 — THIS LINE SUPERSEDES SELF-ATTESTATION: it is a COMMAND RESULT, not a
      sentence the model writes. If it fails, NOTHING below is "clean". The items
      beneath are the human-readable expansion of what the gate now checks
      mechanically — they are no longer the certification themselves.)
  [ ] Final whole-paper Part A: exit 0, zero fixable WARN.
  [ ] Every Part-B check (§6) complete for every question; zero open content defect.
      (mechanically asserted by S5-1A C2+C3; not self-attested)
  [ ] Every §7 artefact carries its required stamp (image='rendered-and-viewed';
      table/matrix/chart/OMML='recomputed') AND the montage/trace file it names EXISTS;
      zero un-audited visual/structured item. (mechanically asserted by S5-1A C6+C7)
  [ ] B-ALLOC / B-MANDATE / B-SCENARIODUP / B-PRESENTDUP / B-LEAK finalised clean
      across the whole mock.
  [ ] Every CA/static-GA fact web-verified with a recorded, SAVED source (RA-11).
      (mechanically asserted by S5-1A C5)
  [ ] derived key A-KINT clean (single int or proper subset per mode);
      A-KBAL/A-KPAT within band (single-mode questions only). (S5-1A C4 for uniqueness)
  [ ] (multi only) A-MSQ-KEY clean — every re-derived set is a non-empty proper subset
      (fixed-k honored, AOTA rule honored); A-MSQ-INSTR clean — observed multi
      instruction counts match the blueprint per section. Dormant when multi_present=false.
  [ ] registry re-synced from the FINAL fixed file (§13) and schema-complete.
  Any item open → re-open the relevant Phase-2 work; Phase 3 does NOT proceed. Only
  when the COMPLETION GATE prints PASS and ALL hold is present_files permitted
  (MANDATE D).

# ════════════════════════════════════════════════════════════════════════
# §13 — REGISTRY RE-SYNC (rebuild mock-N's slice from the FIXED file)
# ════════════════════════════════════════════════════════════════════════
#   Step 7 already appended mock N to the registry (S13-4) BEFORE this audit. If
#   Step 8 changed any content, the registry's mock-N hashes/stems/manifests are now
#   STALE. Step 8 re-syncs them FROM THE FINAL FIXED DOCX (RA-17), so Step 9 and the
#   next mock dedup against the rectified content, not the pre-audit content.

## S13-1 — Why a trailing-slice rebuild is correct and safe

  registry.question_hashes / stem_texts / semantic_tuples are FLAT arrays appended in
  mock order (Step 1 §12; confirmed in the wild — stem_texts are plain strings). Step 8
  audits the MOST RECENTLY appended mock (S2-2 hard-stops unless mocks_completed[-1]==N).
  Therefore mock N occupies the TRAILING `count_N` entries of each flat array, where
  count_N == total_questions for this mock. Step 8 rebuilds exactly that trailing slice.
  Mock-tagged structures (rc_manifests, figural_manifests, content_tracking L4–L18,
  session_log) carry an explicit mock/mock_n field and are replaced BY KEY (mock==N).

## S13-2 — Re-sync procedure (run at Phase 3, from the fixed docx)

  ```python
  import json, hashlib, re
  from docx import Document   # parse_blocks/block_stem_text are the §P6 helpers

  reg = json.load(open(f'/home/claude/{EXAM}_registry.json', encoding='utf-8'))
  _pc = reg.get('papers_completed') or [f"MOCK:M{int(x):02d}" for x in reg.get('mocks_completed', [])]
  assert _pc[-1] == paper_id, "S2-2 guard: registry must end with THIS paper (paper_id)."  # C3
  _title, fixed_blocks = parse_blocks(Document(FIXED_DOCX))   # §P6 → (title, blocks)
  assert len(fixed_blocks) == total_questions

  # 1) trailing-slice rebuild of the flat arrays (mock N == last total_questions entries)
  #    qhash MUST mirror the Step-7 S13-4 hashing recipe so future-mock dedup that
  #    compares hashes stays consistent; stem_texts (the PRIMARY dedup field) is
  #    rebuilt faithfully regardless. If the Step-7 recipe is unknown, rely on the
  #    faithfully-rebuilt stem_texts and recompute hashes with the recipe below.
  def clean_stem(b):                              # same normalisation Step 7 used
      return re.sub(r'\s+', ' ', block_stem_text(b)).strip()
  def qhash(b):
      return hashlib.md5(f"M{N}Q{b.qnum}|{clean_stem(b).lower()}".encode()).hexdigest()

  for arr, builder in (('question_hashes', qhash),
                       ('stem_texts',     clean_stem),
                       ('semantic_tuples', semantic_tuple)):   # semantic_tuple re-derived
      old = reg.get(arr, [])
      assert len(old) >= total_questions, \
          f"S13 guard: {arr} shorter than one mock — registry corrupt (re-check S2-2)."
      keep = old[:len(old) - total_questions]
      reg[arr] = keep + [builder(b) for b in fixed_blocks]

  # 2) replace mock-tagged manifests BY KEY (rebuilt from the fixed file)
  reg['rc_manifests'] = [m for m in reg.get('rc_manifests', []) if m.get('mock') != N]
  if passage_present_in_fixed:
      reg['rc_manifests'].append({'mock': N,
          'passage_linked': sorted(passage_linked_fixed),
          'cloze_linked':   sorted(cloze_linked_fixed)})
  # v2.13 (GAP-2026-08-01-FIGSPEC-TRANSPORT D6) — CARRY FORWARD, DO NOT DROP.
  # The rebuild used to construct a FRESH dict holding only {mock, figural_qs,
  # image_hashes}, silently discarding every other key Step 7 put in the mock-N
  # manifest: object_types and subtopic_ids (v5.31 — A-FIGPROFILE's ONLY inputs),
  # figure_specs (v5.34 — the twelve figure gates' only inputs), paper_id and
  # visual_verified. The effect was invisible on the audited run and appeared on
  # the NEXT one: a re-audit, or Step 9/10 reading the re-synced registry, found
  # A-FIGPROFILE dormant and every figure legacy on a paper that was neither.
  # Step 8 re-derives what it OBSERVES in the fixed docx (figural_qs, image
  # hashes) and PRESERVES what only Step 7 can know (how each figure was
  # generated) — the same split §13-2b already applies to subtopic_id vs
  # difficulty. RA-17 is unaffected: nothing stale is carried, because these
  # fields describe the RENDER, and a Step-8 re-render updates them via §8-4.
  _prev_fig = next((m for m in reg.get('figural_manifests', [])
                    if m.get('mock') == N), {})
  reg['figural_manifests'] = [m for m in reg.get('figural_manifests', []) if m.get('mock') != N]
  if figural_present_in_fixed:
      _fm = dict(_prev_fig)                      # keep object_types/subtopic_ids/
      _fm.update({'mock': N,                     #   figure_specs/paper_id/...
          'figural_qs':  sorted(figural_qs_fixed, key=int),
          'image_hashes': image_hashes_fixed})    # hashed from word/media of the FIXED file
      # A regenerated/re-rendered figure invalidates the spec Step 7 recorded for
      # it: drop ONLY those keys, never the whole map (S8-4 re-render path).
      if _fm.get('figure_specs'):
          _rekeys = {f'q{r["q"]}_' for r in audit_state.get('regenerations', [])}
          _fm['figure_specs'] = {k: v for k, v in _fm['figure_specs'].items()
                                 if not any(k.startswith(p) for p in _rekeys)}
      reg['figural_manifests'].append(_fm)

  # 2b) question_index re-sync BY KEY (v1.6 — Contract_QuestionMetadataIndex v1.0).
  #     subtopic_id : the CERTIFIED value is Step 8's INDEPENDENT re-derivation (the §9 audit
  #                   ledger's per-q subtopic_id, from the B-ALLOC content->id mapping) — NEVER
  #                   trusted from Step 7. A disagreement with Step 7's incoming index is a
  #                   labelling defect (logged); the re-derived id wins. A regenerated Q keeps its
  #                   slot id (RA-6), so re-derivation agrees by construction.
  #     difficulty  : CARRIED FORWARD from Step 7's incoming index — difficulty is NOT rendered in
  #                   the paper and is NOT re-derivable from it (§19). Regeneration preserves the
  #                   difficulty target (RA-6 / S8-2), so the carried value stays correct.
  #     This is Step 8's certification of the four subtopic_id-derived tags + the carried Complexity
  #     tag that Step 6 renders. Exam-agnostic; writes NOTHING to the docx.
  _s2      = next((e for e in reg.get('question_index', [])
                   if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == paper_id),
                  {'questions': []})   # C3: key on paper_id (== mock for a mock)
  _s2map   = {int(x['q']): x for x in _s2.get('questions', [])}
  _regen_q = {r['q'] for r in audit_state.get('regenerations', [])}
  _qi = []
  for q in range(1, total_questions + 1):
      _cert_id = ledger.entries[q]['subtopic_id']          # §9 independent re-derivation
      _s2q     = _s2map.get(q, {})
      if q not in _regen_q and _s2q.get('subtopic_id') != _cert_id:
          audit_state.setdefault('findings', []).append(
              f"question_index: Q{q} Step-7 subtopic_id {_s2q.get('subtopic_id')!r} "
              f"!= re-derived {_cert_id!r} — re-derived id wins (Step-7 labelling defect).")
      _qi.append({'q': q,
                  'subtopic_id': _cert_id,                 # certified = independently re-derived
                  'difficulty':  _s2q.get('difficulty')})  # carried forward (never from the docx)
  reg['question_index'] = [e for e in reg.get('question_index', [])
                           if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") != paper_id]
  reg['question_index'].append({'mock': N, 'paper_id': paper_id, 'questions': _qi})   # C3

  # 3) content_tracking L4–L18: drop mock_n==N rows, re-append from the fixed file's ledger
  ct = reg.setdefault('content_tracking', {})
  for field in ['ga_facts_used','passage_topics','cloze_topics','vocab_words_used',
                'idioms_used','grammar_rules_used','computer_facts','numeric_seeds',
                'analogy_schemes','cause_effect_domains','syllogism_domains','option_sets']:
      ct[field] = [r for r in ct.get(field, []) if r.get('mock_n') != N] \
                  + audit_ledger_content_tracking(field, N)   # from §9 ledger

  # 4) image_phashes (top-level) for mock N: drop+re-add from fixed media
  reg['image_phashes'] = [h for h in reg.get('image_phashes', []) if h.get('mock_n') != N] \
                         + image_phashes_fixed

  # 5) audit session-log entry (does NOT duplicate Step 7's; records the audit)
  reg.setdefault('session_log', []).append({
      'mock': N, 'step': 'MockCreateAudit', 'audit_version': '2.6',
      'verdict': 'CERTIFIED_CLEAN',
      'completion_gate': 'PASS',                 # v2.6: S5-1A result recorded
      'defects_fixed': len(audit_state['defects']),
      'regenerated': len(audit_state['regenerations']),
      'inputs_repaired': audit_state.get('session_log', {}).get('inputs_repaired', []),
      'timestamp': now_utc_iso(), 'notes': 'registry re-synced from fixed file'})

  # 5b) v2.5 THREE-AXIS — accumulate THIS mock's independently re-tagged axes into the window
  #     tally, then (only at window close) run the S6-6 format-distribution audit. Counts come
  #     from the §9 ledger, which tagged each question from the FINAL fixed docx (S6-1b).
  if axis_schedule:                                          # inert when blueprint has no target
      # IDEMPOTENCY (resume/re-audit safe): a mock is added to the window tally AT MOST ONCE.
      # axis2_audit_mocks (loaded in P4, window-aware) lists mocks already counted this window.
      _already_counted = (N in axis2_audit_mocks)
      for sec in sections:
          nm = sec['name']
          acc = axis2_audit_sections.setdefault(
              nm, {'axis1': {}, 'axis2': {}, 'axis3': {}, 'neg': 0, 'total': 0})
          if _already_counted:
              continue                                        # do NOT re-add mock N's counts
          for q, e in ledger.entries.items():                 # this mock's per-question ledger
              if e.get('section') != nm:
                  continue
              for ax in ('axis1', 'axis2', 'axis3'):
                  c = e.get(ax)
                  if c:
                      acc[ax][c] = acc[ax].get(c, 0) + 1
              acc['total'] += 1
              if e.get('is_negative'):
                  acc['neg'] += 1
      if not _already_counted:
          axis2_audit_mocks.append(N)
      reg['axis2_audit'] = {'window': _cur_window, 'sections': axis2_audit_sections,
                            'mocks': sorted(set(axis2_audit_mocks))}

      if axis_window_is_closing(N, AXIS_WINDOW, TOTAL_MOCKS):
          # PARTIAL-WINDOW SCALING: the last window may hold fewer than AXIS_WINDOW mocks
          # (total_mocks not a multiple of the window). Scale every per-window target to the
          # ACTUAL number of mocks in this window so a short final window is judged fairly.
          mocks_in_window = N - _cur_window * AXIS_WINDOW      # e.g. W=10, N=13, w=1 → 3
          if mocks_in_window <= 0:
              mocks_in_window = AXIS_WINDOW                    # defensive (never expected)
          scale = mocks_in_window / float(AXIS_WINDOW)
          s7_sections = s7_axis_window.get('sections', {}) if s7_axis_window.get('window') == _cur_window else {}
          axis_findings = []
          for sec in sections:
              nm  = sec['name']
              sch = axis_schedule.get(nm)
              acc = axis2_audit_sections.get(nm, {'axis1':{}, 'axis2':{}, 'axis3':{}, 'neg':0, 'total':0})
              axis_findings += audit_axis2(nm, sch, acc['axis2'], scale=scale)
              if sch and sch.get('status') == 'ok':
                  axis_findings += audit_axis13(nm, '1', sch.get('axis1_per_paper', {}), acc['axis1'], mocks_in_window)
                  axis_findings += audit_axis13(nm, '3', sch.get('axis3_per_paper', {}), acc['axis3'], mocks_in_window)
                  axis_findings += audit_axis_negative(nm, sch, acc['neg'], acc['total'])
              # cross-check only within the SAME window (guarded above via s7_sections).
              axis_findings += cross_check_step7(nm, acc['axis2'], s7_sections)
          # ADVISORY by default (RA-9 parallel): log to the report; escalate to a blocking defect
          # only if section_rules/blueprint marks the format mix a hard requirement.
          for _af in axis_findings:
              audit_state.setdefault('findings', []).append(_af)
          audit_state['axis_window_audited']  = _cur_window    # dashboard reads these
          audit_state['axis_window_findings'] = len(axis_findings)

  # 6) schema-completeness (idempotent self-heal — same intent as Step 7 S13-REGCHECK)
  REQUIRED_TOP = ['exam_code','schema_version','mocks_completed','question_hashes',
                  'stem_texts','semantic_tuples','question_index','image_phashes',
                  'image_sources_used','session_log','content_tracking','section_names',
                  'rc_manifests','figural_manifests']
  for f in REQUIRED_TOP:
      reg.setdefault(f, {} if f == 'content_tracking' else [])
  reg.setdefault('axis2_audit', {})     # v2.5: dict; preserved across re-syncs (never dropped)

  json.dump(reg, open(f'/home/claude/{EXAM}_registry.json','w',encoding='utf-8'),
            indent=2, ensure_ascii=False)
  ```

## S13-3 — Re-sync verification (gate before delivery)

  [ ] len(question_hashes) == len(stem_texts) == len(semantic_tuples).
  [ ] the trailing total_questions stems all carry mock-N's fixed content (re-hash the
      fixed file, compare).
  [ ] mocks_completed unchanged (Step 8 NEVER appends a mock — it only re-syncs mock N).
  [ ] no mock_n==N row survives in any content_tracking field except the re-appended ones.
  [ ] registry schema-complete.
  [ ] question_index (v1.6): exactly ONE mock-N object; its questions cover q=1..total_questions
      (sorted, unique, complete); every subtopic_id ∈ blueprint.subtopic_list[]; every difficulty
      ∈ blueprint.difficulty_labels; difficulty distribution == difficulty_schedule[N] EXACTLY.
      subtopic_id values are Step 8's INDEPENDENT re-derivation (§9 ledger); difficulty values are
      CARRIED FORWARD from Step 7 (not re-derived from the paper — §19). Mirrors Step 7 G-QINDEX
      (Contract_QuestionMetadataIndex v1.0).
  Any failure → HARD STOP (do not deliver a corrupt registry; inspect S13-2).

# ════════════════════════════════════════════════════════════════════════
# §14 — DELIVERY (core closed set + conditional change-log; ONE present_files)
# ════════════════════════════════════════════════════════════════════════

## S14-1 — The deliverable set (CORE closed; change-log conditional)

  CORE SET (always — = Step 7 R-DELIVER discipline):
    1. /mnt/user-data/outputs/[ExamCode]_Mock[N]_Create_Complete.docx   — RECTIFIED paper
    2. /mnt/user-data/outputs/[ExamCode]_registry.json           — RE-SYNCED registry
  CONDITIONAL (iff audit_state.regenerations is non-empty — S8-5):
    3. /mnt/user-data/outputs/[ExamCode]_Mock[N]_audit_changelog.md  — author-only
       BEFORE→AFTER diff for every regenerated question.
  NEVER deliver: the derived key, the audit ledger, audit_state, the block index,
    the evidence dir (montages/facts/recompute), montages, any scratch/WIP docx, any
    other internal sidecar. The learner key is a Step-9 artefact (R-DELIVER).

## S14-1b — Build the change-log artefact (only if regenerations occurred)

  ```python
  import os
  regens = audit_state.get('regenerations', [])
  changelog = None
  if regens:
      out = '/mnt/user-data/outputs'
      changelog = f'{out}/{EXAM}_Mock{N}_audit_changelog.md'
      with open(changelog, 'w', encoding='utf-8') as f:
          f.write(f"# Mock {N} Audit Change-Log — {EXAM}\n")
          f.write("# AUTHOR-ONLY AUDIT ARTEFACT — NOT FOR DISTRIBUTION.\n")
          f.write("# Contains the literal before/after of every regenerated question.\n")
          f.write(f"# Generated by Step 8 (MockCreateAudit v2.6). "
                  f"Questions regenerated: {len(regens)}.\n\n")
          for r in regens:                       # r carries the LITERAL view (S8-5)
              f.write(f"## Q.{r['q']} — {r['class']} (defect: {r['defect_code']})\n\n")
              f.write(f"**What changed:** {r['change_class']}  ·  "
                      f"**Preserved:** {', '.join(r['invariants_preserved'])}\n\n")
              b, a = r['before'], r['after']
              f.write("### BEFORE\n")
              f.write(b['stem'] + "\n")
              for i, o in enumerate(b['options'], 1): f.write(f"  {i}. {o}\n")
              f.write(f"  [key: option {b['key']}]\n\n")
              f.write("### AFTER\n")
              f.write(a['stem'] + "\n")
              for i, o in enumerate(a['options'], 1): f.write(f"  {i}. {o}\n")
              f.write(f"  [key: option {a['key']}]\n\n")
              f.write(f"### Rationale\n{r['rationale']}\n\n")
              f.write(f"### Re-audit\nPart A + Part B/§7 for the question's class: "
                      f"clean.  Dedup vs ledger + registry: clean.\n\n---\n\n")
  ```

## S14-2 — Pre-delivery checklist (MANDATORY before present_files; MANDATE D)

  ```python
  import os
  out = '/mnt/user-data/outputs'
  docx_name = f'{EXAM}_{paper_slug}_Create_Complete.docx'; reg_name = f'{EXAM}_registry.json'  # C3
  cl_name   = f'{EXAM}_Mock{N}_audit_changelog.md'
  expected  = {docx_name, reg_name} | ({cl_name} if regens else set())
  for _ck in [f for f in os.listdir(out) if f.endswith('_audit_checkpoint.zip')]:
      os.remove(os.path.join(out, _ck))   # v2.15: resume state, never a deliverable
  present   = set(os.listdir(out))
  BANNED    = ('answer', 'key', 'ledger', 'audit_state', 'blockindex', 'montage', 'evidence')
  # the change-log legitimately contains 'audit' + Q content; exempt it from the
  # banned-substring scan, but ban every OTHER internal sidecar:
  leaked = [f for f in present if f != cl_name
            and any(b in f.lower() for b in BANNED)]
  checks = [
    ('1 fixed docx in outputs',         os.path.exists(f'{out}/{docx_name}')),
    ('2 re-synced registry in outputs', os.path.exists(f'{out}/{reg_name}')),
    ('3 change-log present iff regens',  os.path.exists(f'{out}/{cl_name}') == bool(regens)),
    ('4 completion gate passed',        bool(globals().get('COMPLETION_GATE_PASS'))),
    ('5 no internal sidecar leaked',    not leaked),
    ('6 outputs == exactly expected set', present == expected),
    # v2.15 (C1): the per-batch checkpoint is staged in outputs by design
    # (MANDATE D carve-out) and is NOT a deliverable. Clear it BEFORE this check
    # so the certification delivery is exactly the closed set.
    ('7 no checkpoint left in outputs', not any(
        f.endswith('_audit_checkpoint.zip') for f in present)),
  ]
  fails = [n for n, ok in checks if not ok]
  if fails:
      raise SystemExit("HARD STOP (S14-2): " + "; ".join(fails) +
                       ". Fix, then re-run S14-2. Do NOT call present_files yet.")
  ```
  Stage ONLY the deliverables in outputs; keep everything else (incl. the evidence
  dir) in /home/claude. Check 4 (COMPLETION_GATE_PASS) is set ONLY by an actual
  S5-1A "COMPLETION-GATE: PASS" exit-0 run — never by a self-declared flag.

## S14-3 — The single present_files call

  ```python
  files = [f'/mnt/user-data/outputs/{EXAM}_{paper_slug}_Create_Complete.docx',
           f'/mnt/user-data/outputs/{EXAM}_registry.json']
  if regens:
      files.append(f'/mnt/user-data/outputs/{EXAM}_Mock{N}_audit_changelog.md')
  present_files(files)        # docx first; the ONLY present_files call (MANDATE D)
  ```

## S14-4 — STATUS REPORT dashboard (print in chat at delivery; MANDATE-0 safe)

  A single scannable block printed right after present_files (before the §15 detail and
  the handoff). All figures come from real audit STDOUT + audit_state — never memory.
  NO question content (counts, codes, Q-numbers only).

  ```
  ╔════════════════════════════════════════════════════════════════════╗
  ║  STEP 8 · MOCK [N] AUDIT — STATUS REPORT            ✅ CERTIFIED ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  Paper    : [ExamCode]_Mock[N]_Create_Complete.docx ([size], md5 [….])    ║
  ║  Verdict  : CERTIFIED CLEAN — delivered                             ║
  ║  Gate     : COMPLETION-GATE: PASS (C1–C7)   [S5-1A]                 ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  ON ARRIVAL              →   AFTER RECTIFICATION                    ║
  ║  Part A  : [a] FAIL · [w] WARN   →   0 FAIL · 0 fixable WARN        ║
  ║  Content defects open : [c]      →   0                              ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  COVERAGE (zero sampling — RA-3; evidence-backed — S5-1A)          ║
  ║    Questions reviewed ........ [N]/[N]                              ║
  ║    Batches run .............. [K]/[K]                               ║
  ║    Images rendered & viewed .. [i]/[i]   (montage files present)    ║
  ║    Tables recomputed ......... [t]/[t]   (trace files present)      ║
  ║    Charts viewed ............. [ch]/[ch]                            ║
  ║    OMML expressions recomputed [o]/[o]                              ║
  ║    Facts web-verified ........ [f]/[f]   (sources saved, not shown) ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  RECTIFICATION                                                     ║
  ║    Content-preserving fixes (CP) : [cp]  (top: [code×n], [code×n]) ║
  ║    Questions regenerated   (RG)  : [rg]  → see Change-Log below     ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  DEDUP    : cross-mock [PASS|PARTIAL] · intra-mock [PASS]          ║
  ║  FORMAT   : Axis mix [window K: within tol | N finding(s) | inert]║
  ║  REGISTRY : re-synced from fixed file ✓ (mocks_completed unchanged)║
  ║  DELIVERED: [2|3] files (docx · registry[ · change-log])           ║
  ╚════════════════════════════════════════════════════════════════════╝
  ```
  Render the box with whatever box-drawing the client supports; if alignment is a
  concern, a plain "key: value" list with the same fields is equally acceptable —
  the CONTENT (verdict, completion-gate result, on-arrival→after delta, coverage
  matrix incl. batches-run, CP/RG counts, dedup, registry, file count) is what
  matters, not the borders.

## S14-5 — Handoff message (print after the dashboard + §15, then END)

  ```
  === MOCK [N] AUDIT COMPLETE — Step 8 done (CERTIFIED CLEAN) ===
  Delivered ([2|3] files):
    • [ExamCode]_Mock[N]_Create_Complete.docx       — rectified, zero-defect paper
    • [ExamCode]_registry.json               — re-synced from the fixed file
    • [ExamCode]_Mock[N]_audit_changelog.md  — author-only before/after diff
                                               (ONLY if questions were regenerated)

  Regenerated questions: [list of Q-numbers, or "none"].
  (The structural diff is in the report above; the literal before/after text is in
   the change-log file — open it outside chat. It is author-only; do not distribute.)

  ⚠ REGISTRY HANDOFF — REQUIRED before Step 9 / the next mock:
    Replace registry.json in your [ExamCode] project Files with the one just
    delivered (it now reflects the RECTIFIED content). Skipping this re-introduces
    the pre-audit stems into the dedup corpus.

  Next step → Step 9 (MockExplain): build the learner key + solutions on this
  certified paper.
  =============================================================
  ```
  After printing: END THE RESPONSE. Write nothing more.

## S14-6 — Post-delivery footer (MANDATORY after present_files)

```
After the present_files call, status report (S14-4), and handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type (F2 step-complete — always for
Step 8 since it has no batches), file badges (Use locally for docx + changelog,
Replace for registry.json), and next-step reference.
```

# ════════════════════════════════════════════════════════════════════════
# §15 — AUDIT REPORT FORMAT (MANDATE-0 safe; built from real STDOUT + findings)
# ════════════════════════════════════════════════════════════════════════
#   Built from actual audit STDOUT + reviewer findings — never re-summarised from
#   memory. NO question content anywhere (codes + Q-numbers only).

  §R0 Status dashboard : the §14-4 STATUS REPORT block (verdict · completion-gate
                   result · on-arrival→after delta · coverage matrix · CP/RG counts ·
                   dedup · registry · files). Printed first so the outcome is scannable.
  §R1 Provenance : docx name+size+MD5 · audit_version (2.6) · script self-test N/N
                   (fixture-based) · COMPLETION-GATE result · registry state
                   (mocks_completed, alignment) · blueprint/manifest ids · any
                   inputs_repaired (P0.5) · timestamp.
  §R2 Outcome    : CERTIFIED CLEAN (delivered) — unambiguous; backed by
                   "COMPLETION-GATE: PASS" (S5-1A), not a self-declaration.
  §R3 Part A     : on-arrival vs final — every gate OK/FAIL/WARN with its verbatim
                   message; the FAIL/WARN count the audit STARTED with → 0/0 final.
  §R4 Defects fixed (Class CP): grouped — code · count · Q-number list · one-line what.
  §R5 Regeneration change-log (Class RG): for EACH regenerated question, the STRUCTURAL
                   (content-free) record from S8-5 —
                     "Q.[n] · [defect_code] · [change_class] · preserved:[subtopic_id,
                      section,difficulty,format(,answer position)] · re-audit:clean ·
                      dedup:clean".
                   State plainly that the LITERAL before→after diff is in the delivered
                   change-log artefact (deliverable #3), not in chat (MANDATE 0). If
                   zero regenerations: "Regenerations: none — no change-log produced."
  §R6 Part B     : per-class results; clean classes stated as "all [n] verified — 0 defects".
  §R7 Coverage matrix (proves zero sampling — RA-3; evidence-backed — S5-1A): questions
                   reviewed [n/n] · batches run [K/K] · images rendered-and-viewed [n/n] ·
                   tables recomputed [n/n] · charts viewed [n/n] · OMML recomputed [n/n] —
                   every item stamped AND its evidence file present (RA-19); zero un-audited.
  §R8 Fact verification (CONTENT-FREE): COUNTS only — "[f] current-affairs / static-GA
                   facts and factual options web-verified; every source URL + date +
                   result saved to /home/claude evidence (and, for any regenerated fact,
                   into the change-log artefact)". NEVER list the facts themselves in chat
                   (they are answer content — MANDATE 0). A fact that could not be sourced
                   was regenerated (counted under §R5), never shipped.
  §R9 Dedup      : cross-mock (stems/images/content_tracking) result; intra-mock
                   B-SCENARIODUP/B-PRESENTDUP result.
  §R10 Allocation/Mandate: per-subtopic counts vs blueprint; mandatory/alternation status.
  §R11 Key health: A-KINT/A-KBAL/A-KPAT on the derived key (with the Step-9 boundary note);
       (multi only) A-MSQ-KEY (set well-formedness) + A-MSQ-INSTR (instruction-count match).
  §R12 Registry delta: trailing-slice rebuilt; manifests re-keyed; guard assertions; "replace before next mock".
  §R13 Limitations: anything not fully mechanisable (difficulty labels [estimate];
                   partial cross-mock dedup if registry lags; key adjudication is Step-9;
                   any P0.5 inputs_repaired; the S5-1A residual — §19).
  §R14 Defects-by-class rollup: a count of each defect CODE found+fixed, CP vs RG, so a
                   systemic Step-7 issue is visible at a glance (e.g. "A-MATHRASTER ×7 →
                   a generator-side math-rendering gap worth fixing upstream"). This turns
                   the audit into upstream feedback, not just a one-paper fix.
  §R15 Batch trace: batches run [K], re-audit iterations, and (on a resume) which batches
                   were carried over — so the run is reproducible and auditable.

  PROVENANCE STAMPS used: 'machine' · 'recomputed' · 'rendered-and-viewed' ·
  'web-verified+source' · 'reviewer-verified' · 'estimate'.

# ════════════════════════════════════════════════════════════════════════
# §16 — AUDIT GATE GLOSSARY (Step-8 gates ↔ the Step-7 contract each re-verifies)
# ════════════════════════════════════════════════════════════════════════
#   Step 8 re-verifies, INDEPENDENTLY, every machine-checkable Step-7 contract, and
#   adds Step-8-only integrity/semantic checks. The mapping (so nothing is lost):

  PART A (machine — universal audit.py):
    A-COUNT/A-SEQ/A-MONO/A-SECCOUNT      ← R7, R18 (+ Step-7 S3-9)
    A-OPTN/A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE ← R4, R10, R13
    A-SECHDR ← R8/G-SECTIONHDR · A-ANSKEY ← R5/G-ANSWERKEY · A-FONT ← R24/G-FONTCHECK
    A-BLANKSEP ← R13 · A-QNFIRST ← R14/G-QNUM-FIRST
    A-STIMORPHAN ← R-LINKED/G-STIMULUS-ORPHAN
    A-MATCH-TABLE ← S7-3/G-MATCH-TABLE (Step 7 match-render mandate; re-derived MATCH must carry a real table)
    A-UNDERLINE ← R-UNDERLINE/G-UNDERLINE
    A-MATHRASTER ← R-MATH-OMML/G-MATH-RASTER (view-backed, S5-3) · A-FRAC ← G-FRAC
    A-OMML ← R-MATH-OMML/G-OMML(+FLOOR)
    A-FIGCOMP ← R-FIGURAL/G-FIGURAL-COMPOSITE (+ G-FIGTEXT figural-as-text + G-FIGTEXT-PROSE; S10-8/S10-8A)
    A-OPTREF ← R-OPTREF/G-OPTREF
    A-DUP ← R2/R3/G-DUP (cross-mock, --mockN self-exclude)
    A-KINT/A-KBAL/A-KPAT ← K-INT/K-BAL/K-PAT (on Step-8's DERIVED key, §11)
    A-HEADER ← R8b/G-PREQ1 (Step 7 pre-Q.1 body-block ban; strip if present)
    A-FIGTEXT-PROSE <- R-FIGURAL/G-FIGTEXT-PROSE (Create Tier 3). Live roster gate,
                CAN FAIL; zero-image block carrying figure-reference prose.
    A-DOSSIER <- S13-4b Tier-A fact channel (v2.17; predicate corrected v2.21).
                Step-8-only; no Step-7 gate equivalent. Cross-checks FACTS, never
                JUDGMENTS (RA-1); passes NOTHING on dossier evidence alone. Its
                rendered-option count is the SHARED one (block_option_count(b, oc)),
                never a second predicate — S5-2 "ONE STRUCTURAL QUESTION, ONE ANSWER".
    STEP-8-ONLY: A-ZIP, A-ENCODING (U+FFFD), A-SCRIPT (language-conditioned, RA-10),
                 A-INTEGRITY (P0.5 input corruption/truncation)

  COMPLETION GATE (Phase-3 mechanical Part-B/§7 enforcement — S5-1A):
    C1 batches-complete · C2 all-questions-reviewed · C3 all-status-closed ·
    C4 B-UNIQUE/A-MSQ-KEY ran · C5 facts sourced + saved file exists (RA-11) ·
    C6 artefacts stamped + montage/trace file exists (RA-19) · C7 coverage totals match
    → prints COMPLETION-GATE: PASS; required by §12-2 / MANDATE B / MANDATE D.

  PART B (semantic — Claude reasoning, §6):
    B-SOLVE/B-UNIQUE ← R-ANSWER/G-UNIQUE · B-DISTRACT ← wrong-option quality
    B-STEMOPT ← R17 · B-OPTREF-SEM ← R-OPTREF (semantic half)
    B-FACT ← live web-verification + saved evidence (RA-11; Step-7 had no live check)
    B-PASSAGE ← passage/cloze derivability · B-LEAK ← inter-question leakage
    B-ALLOC ← R6/G-ALLOC-SUBTOPIC (observable re-derivation, §6-4)
    B-MANDATE ← manifest mandatory_every_mock/alternation_groups (+ G-CISINCHECK class)
    B-SCENARIODUP ← G-CONCEPTDUP (observable) · B-PRESENTDUP ← G-FORMATDUP/R19 (observable)
    B-DIFF ← difficulty_schedule (advisory)

  §7 (visual/structured — view/recompute; evidence-saved):
    V-image (view every) ← R-FIGURAL/G-FIGURAL-COMPOSITE/G-FIGTEXT/G-FIGTEXT-PROSE + transformation truth (v2.4: stem_only Qs verified for problem image presence)
    V-table/matrix/chart (parse+recompute) ← DI/match self-containment + answer derivability
    V-omml (extract+recompute+render-verify) ← R-MATH-OMML

  NONE of the Step-7 57 gates is dropped: each is either re-run by audit.py (machine),
  re-derived in §6 (the sidecar-dependent ones, observable form), or subsumed by §7
  (visual). Step-8-only additions: A-ZIP, A-ENCODING, A-SCRIPT, A-INTEGRITY, B-FACT
  (live), the §7 view/recompute mandates, and the S5-1A completion gate.

# ════════════════════════════════════════════════════════════════════════
# §17 — EDGE-CASE PLAYBOOK
# ════════════════════════════════════════════════════════════════════════
  | Scenario | Action |
  |---|---|
  | audit.py missing | HARD STOP (MANDATE A) — auto-generated by Step 6 v1.20+; verify all 6 Step 6 outputs were uploaded. Fallback: re-copy the repo engine `audit_canonical.py` (the live single source of truth). The old "copy from Framework_MockTestCreate.md Appendix A" route is DEAD — that file has carried no auditor fence since v2.11.2 (corrected v2.12). |
  | audit.py self-test not a fixture-based N/N (N>=AUTH_GATE_FLOOR) | HARD STOP (P1 hardened) — a constant-print PASS is REJECTED; regenerate the canonical auditor. |
  | audit.py truncated but --self-test prints PASS | HARD STOP (P0.5 ast.parse + P1 hardened) — hollow/constant self-test rejected; regenerate from Appendix A / Step 6 B3. |
  | **audit.py raises a traceback on the REAL paper (not --self-test)** | **FRAMEWORK DEFECT, not an input defect — v2.12.** Do NOT regenerate from the exam's own copy: it reproduces the identical defect (the file is not corrupt — it ast-parses, passes the self-test, and is byte-identical to its source). From v2.12 this should be IMPOSSIBLE: `_safe_gate()` converts any gate raise into a named `A-GATEERROR` FAIL and the run completes. If a traceback still escapes, the auditor copy PREDATES v2.12. SANCTIONED REPAIR policy (b): replace `[ExamCode]_mock_test_audit.py` with the current `audit_canonical.py` from the repo, re-run P0.5+P1, log to `session_log.inputs_repaired[]`, disclose in §R13, and file a gap report against the repo. |
  | **`A-GATEERROR` appears in the Part-A report** | A gate CRASHED, so the paper is NOT audited for it. This is a framework defect, never a paper defect — do not attempt to "fix" the paper. The run completed and every other gate is valid. Capture the named gate + the STDERR traceback, file a gap report, and treat certification as BLOCKED (exit is non-zero by design) until the framework is repaired. |
  | **`A-FIGPROFILE` WARNs "NOT CHECKED" / `A-FIG*` WARN "NOT RUN"** | The named ENGINE is missing, truncated, or stale — an environment condition, NOT a paper defect. The audit is valid but has REDUCED COVERAGE. Upload `blueprint_core.py` / `figural_core.py` under their BARE names (Step 6 B3 delivers both) and re-run to obtain full coverage. If unobtainable, document the skip under S5-4 and record it as a §19 limitation. NEVER certify while pretending the gate ran. |
  | Part-A prints FEWER gate lines than a full roster | Treat as INCOMPLETE COVERAGE, not as a pass. From v2.12 the roster is INVARIANT — every gate prints a line in every environment — so a short roster means the auditor copy predates v2.12. Refresh it (policy (b)). |
  | **`A-DOSSIER` FAIL `qtype-mcq-but-0!=N-options` on FIGURAL questions** | **FRAMEWORK defect, NOT a paper defect (GAP-2026-08-02, fixed v2.21).** The auditor copy predates v2.21 and counts options with a predicate (OPT_RE) that CANNOT SEE an IMAGE option — a bare label paragraph followed by a picture. Confirm in ONE step: if `A-OPTN` is `ok` on the same questions, the PAPER IS CORRECT and the GATE IS WRONG. **DO NOT MODIFY THE PAPER** — adding text after the option labels would violate A-FIGCOMP (no dummy-text options) and R-FIGURAL, i.e. introduce a real defect to silence a false one. SANCTIONED REPAIR policy (b): replace `[ExamCode]_mock_test_audit.py` with the current repo `audit_canonical.py` (v2.21+), re-run P0.5 + P1, log to `session_log.inputs_repaired[]`, disclose in §R13. No `resume`/checkpoint is needed — the failure occurs in Phase 1 before any Phase-2 work exists. |
  | **`A-DOSSIER` FAIL `qtype-mcq-but-M!=N-options` where M > N** | Same root cause, **TEXT-option papers**: an enumerated stem ("1. ... 2. ...") inflated the count because the pre-v2.21 counter had no trailing-set clamp. Standard on STATEMENT / SEQUENCE / MATCH / ASSERTION_REASON items. Same remedy. |
  | **`A-DOSSIER` FAIL `qtype-nat-but-M-options` on a NAT question whose STEM enumerates** | Same root cause. Pre-v2.21 the nat leg fired on ANY non-zero label count, so a legitimate NAT stem carrying an enumerated list was reported as if it rendered options. Same remedy. |
  | **`A-DOSSIER` FAIL and `A-OPTN` ALSO fails on the same Q** | **Now it IS a paper defect** — the option set is genuinely wrong. Route to Phase 2, class RG, per the normal option-count repair path. **The `A-OPTN` verdict is the discriminator between a framework defect and a paper defect; always read the two together.** |
  | **`A-FIG*` gates print "0 figure(s)" on a paper that HAS drawings** | The auditor copy PREDATES v2.13 — `Block.images` was never populated, so all twelve gates passed vacuously. NOT a paper property and NOT a pass: the paper was never audited for figure conformance. Refresh the copy (§21 path (A) or (B)) and re-run. |
  | **`A-FIG*` WARN "conformance NOT ESTABLISHED"** | Drawings are declared in the docx but none could be read out of the ZIP. A COVERAGE gap, never a pass — check A-ZIP first (a dangling rId is a hard stop in its own right), then re-run. Never certify past it. |
  | **`A-FIG*` WARN "EC-V18 legacy ... delivery NOT blocked"** | The paper predates Step 7 v5.34, so its figures carry no FigureSpec sidecar and the gate has no record to check against. LOUD but not fixable at Step 8 — an S5-4 ACCEPTED WARN: record it under §R13, the amber footer applies, and the paper still certifies and ships. To obtain full figure coverage, regenerate the paper on Step 7 v5.34+. |
  | **`A-FIG*` FAIL "RENDERER-CONTRACT REGRESSION"** | The figure DOES carry a sidecar, so this is v5.34+ output that regressed — a real, fixable defect. Re-render under S10-7/S10-8, RE-VIEW (§7), and re-run; certification is blocked until clean. |
  | *.json input fails to parse / missing required keys (truncated/corrupt) | HARD STOP (P0.5 / A-INTEGRITY) — re-upload intact; never audit against a truncated blueprint/registry. |
  | section_rules empty or missing EXAM_STRUCTURE header | HARD STOP (P0.5 / A-INTEGRITY) — re-upload intact. |
  | Phase 2 skipped / spot-checked instead of batched | IMPOSSIBLE to certify — completion gate (S5-1A) fails C1/C2; MANDATE B / MANDATE D block delivery. |
  | Ledger fabricated with stamps but no evidence files | Caught — S5-1A C5/C6 fail (named montage/fact/trace file absent); certification blocked. |
  | Autonomous/"don't pause" preference given | Waive the inter-batch pause ONLY (RA-15b / S4-3A); every question still audited + stamped + evidenced (RA-15a / RA-0). |
  | Trigger N ≠ filename N ≠ title N | HARD STOP (S2-2) — ask; wrong N corrupts re-sync + dedup. |
  | registry.papers_completed doesn't end with this paper_id (or legacy mocks_completed doesn't end with N) | HARD STOP (S2-2) — upload the registry delivered with this docx. |
  | Only docx uploaded, registry missing | HARD STOP (P0) — registry is required (dedup + re-sync). |
  | registry lags by an earlier mock | Cross-mock dedup PARTIAL — log as §19 limitation; audit proceeds. |
  | docx < 50 KB | WARN — verify N; tiny paper is suspicious. |
  | image rId unresolved | HARD STOP (A-ZIP) — structural break; the generating step must re-emit. |
  | U+FFFD in text | RG — encoding corruption; regenerate the affected run/question. |
  | Non-ASCII script present | Flag ONLY if language=='english' (RA-10); else legitimate. |
  | Composite figural panel (figures correct) | CP-FIGDECOMP — re-slice into discrete images. |
  | Composite figural panel (a figure wrong) | RG — regenerate the question + figures. |
  | Math shipped as raster | View (S5-3); if algebra → CP-MATHOMML; if mis-named figure → CP-IMGNAME. |
  | Zero OMML but a quantitative section exists | Investigate (S7-5) — math is hiding as ASCII/raster; resolve. |
  | Underline faked as "(underlined: X)" or "____" | CP-UNDERLINE — real <w:u> run. |
  | Stimulus orphaned (lead-in only) | CP-STIMEMBED — embed per member (Model A). |
  | "Q.x and Q.y" cross-reference in a stem | CP — rewrite to singular per-member context (A-STIMORPHAN). |
  | Two defensible answers | RG — disambiguate stem or replace the colliding option (R-ANSWER). |
  | Wrong/unsourceable fact | RG — replace with a web-verified, sourceable fact (save evidence). |
  | DI table values don't yield the keyed answer | RG — regenerate table + dependent answers together. |
  | Impossible/contradictory figure | RG — replace with a valid figure; re-verify dependents. |
  | Escape-option instruction without the option | RG/CP — add the escape option (re-balance) or switch template (R-OPTREF). |
  | Cross-mock duplicate stem/image | RG — regenerate on a new scenario (NEVER delete — RA-8). |
  | Per-subtopic allocation off | RG — regenerate the missing/extra as the needed subtopic_id. |
  | Mandatory subtopic missing | RG — regenerate one question into the mandatory subtopic. |
  | Alternation-group members co-occur | RG — replace one with its alternation partner / a different subtopic. |
  | A batch fix opens a global defect | Resolve in the same batch via the §8-3 loop before ending (RA-7). |
  | **`view()` fails / vision path unavailable** | NOT a halt (v2.16/D2). Run P3.5 (`--vision-probe` then `--vision-probe-verify`). On FAILED, continue the audit and stamp those items `view-unavailable`: the paper certifies CERTIFIED-DEGRADED (VISION), exits 0, ships with an F1 AMBER footer and a §R13 limitation. Tables/OMML/charts are arithmetic and unaffected. A question whose key needs sight is a VOID_ITEM — KEY NOT DERIVABLE, never silently keyed. |
  | **`C6 FAIL: view-unavailable claimed with NO FAILED vision probe`** | The stamp is not admissible. Vision degradation is a MEASURED fact, not a claim — run P3.5 and record its result, or view the images. This gate exists precisely so "I couldn't see it" cannot become a way to skip work. |
  | **`C6 FAIL: vision has RECOVERED but view-unavailable stamps were not upgraded`** | The view tool came back. Re-attempt every degraded item and upgrade its stamp before Phase 3. A paper that CAN be fully audited must not certify degraded. |
  | **`P3.5-RENDER-FAIL`** | Environment WARN only (PIL unavailable). NOT a vision verdict — do not infer an outage, and do not degrade any stamp on this basis. |
  | **Session exhausted mid-Phase-2** | Upload the last `[ExamCode]_M[N]_audit_checkpoint.zip` and re-run with `resume` (v2.15/C1). P0.5C verifies and rehydrates it; the audit continues at the first unfinished batch with its evidence intact. WITHOUT a checkpoint the audit CANNOT be resumed — /home/claude does not survive a session boundary and S5-1A C5/C6 assert the evidence files exist — so it restarts at Phase 1. Never fabricate a ledger to satisfy the gate. |
  | **`CHECKPOINT: REFUSED — ...`** | Restore is all-or-nothing and wrote nothing. Read the reason: unknown schema (bundle from a different framework build), integrity failure (a member's sha256 changed), or an identity mismatch (exam_code / mock / paper MD5 disagree with the paper in hand). The paper-MD5 case is the critical one — restoring onto a different document would certify an audit nobody performed on it. Upload the correct bundle or re-run from Phase 1. Never hand-edit a checkpoint. |
  | **Checkpoint zip appears in /mnt/user-data/outputs at delivery** | Expected mid-audit (MANDATE D carve-out) and cleared automatically by S14-2 before the ONE certification present_files. If it ever survives into the delivered set, S14-2 check 7 fails — fix, do not ship. |
  | Resume after a gap | `... M[N] resume` — reload audit_state; resume at first not-done batch; evidence dir persists (RA-18). |
  | Re-audit of an already-audited mock | Legal — `--mockN N` self-excludes; idempotent (a clean, evidence-complete ledger yields zero fixes and passes S5-1A). |

# ════════════════════════════════════════════════════════════════════════
# §18 — DEFINITION OF DONE / HARD INVARIANTS (ANY violation = do NOT deliver)
# ════════════════════════════════════════════════════════════════════════
  1.  Pre-flight P0–P9 all passed; input integrity clean (P0.5); audit.py fixture
      self-test N/N (N>=AUTH_GATE_FLOOR, P1 hardened); N resolved + registry-aligned.
  2.  Part A: exit 0 on the FINAL whole paper; zero fixable WARN.
  3.  Part B: every question reviewed (zero sampling); zero open content defect.
      (mechanically asserted by S5-1A C2+C3; not self-attested)
  4.  §7: every image rendered-and-viewed; every table/matrix/chart/OMML recomputed;
      zero un-audited visual/structured item (no "[not-viewed]"); a MEASURED-outage
      'view-unavailable' stamp (RA-4 v2.16) satisfies this as DEGRADED, not clean; all stamped AND their
      evidence files present (RA-4/RA-19). (mechanically asserted by S5-1A C6+C7)
  5.  B-UNIQUE verified for EVERY question (exactly one defensible answer).
      (mechanically asserted by S5-1A C4)
  6.  Every CA/static-GA fact + factual option web-verified with a recorded, SAVED
      source. (mechanically asserted by S5-1A C5)
  7.  B-ALLOC/B-MANDATE/B-SCENARIODUP/B-PRESENTDUP/B-LEAK finalised clean (whole mock).
  8.  Cross-mock dedup run (full, or partial-with-logged-limitation if registry lags).
  9.  Every defect found was RECTIFIED (CP or RG) and re-audited; nothing left open (RA-5).
  10. Every regeneration obeyed the Step-7 contracts + dedup vs whole ledger + registry (RA-6).
  11. Registry re-synced from the FINAL fixed file; §13-3 verification clean; mocks_completed
      unchanged; schema-complete.
  12. Deliverable set == CORE {fixed docx, re-synced registry} PLUS the change-log
      artefact iff ≥1 question was regenerated; nothing else (no key/ledger/state/index/
      montage/evidence) leaked. The change-log is the only artefact permitted to carry
      literal content, it is headed author-only, and it is produced iff regenerations occurred.
  13. present_files called EXACTLY once, only after the certification gate (§12-2 / S5-1A).
  14. Report (§15) built from real STDOUT + findings; MANDATE-0 safe; handoff printed.
  15. No question content ever printed in chat anywhere in the session (MANDATE 0).
  16. Completion gate S5-1A printed COMPLETION-GATE: PASS with --audit-state before
      present_files (MANDATE B). A bare --final (Part A only) never certifies.

# ════════════════════════════════════════════════════════════════════════
# §19 — KNOWN LIMITATIONS (disclose in §R13 of every report)
# ════════════════════════════════════════════════════════════════════════
  • Key adjudication (which option index is correct, as a learner-facing key) is a
    Step-9 responsibility; Step 8 derives a key only to AUDIT uniqueness/correctness/balance.
  • Difficulty labels are self-estimated [estimate]; not independently provable.
  • The registry.question_index Complexity value is CARRIED FORWARD from Step 7
    (authoritative-by-assignment): Step 8 verifies its vocabulary + exact distribution vs
    difficulty_schedule[N] but does NOT independently re-derive the per-question label (difficulty
    is not rendered in the paper). The index's subtopic_id, by contrast, IS independently
    re-derived and certified (§13 step 2b) — the four subtopic_id-derived tags are provable, the
    Complexity tag is not (Contract_QuestionMetadataIndex v1.0, two-tier guarantee).
  • Cross-mock dedup is only as complete as the registry handed in; a lagging registry
    yields partial dedup (logged, not silently passed).
  • Figural transformation correctness and answer uniqueness rest on reviewer reasoning
    over the VIEWED image (no machine proof) — but viewing is mandatory, un-sampled, and
    evidence-backed (the montage that was viewed is saved and its presence is gated).
  • CERTIFIED-DEGRADED (VISION) IS A REAL, DISCLOSED WEAKNESS (v2.16/D2). Under a
    measured vision outage the twelve figure gates still run (they are arithmetic over
    the PNG), tables and OMML are still recomputed, and every question is still solved
    — but no human or model EYE confirmed the affected figures. Legibility, mislabelled
    axes and figure/stem mismatch are exactly what viewing catches and arithmetic does
    not. Such a paper certifies, ships, and says so loudly: DEGRADED on the completion
    line, F1 AMBER on the footer, a §R13 limitation naming the count. Re-run on a
    session with a working view tool for full coverage. This is a deliberate choice of
    a disclosed partial audit over no paper at all — the same trade EC-V18 already
    makes for ~200 legacy exams.
  • RESUMING ACROSS A SESSION REQUIRES THE CHECKPOINT (v2.15/C1). Step 8's state
    lives in /home/claude, which does not survive a session boundary. The
    checkpoint makes a multi-session audit possible, but it is an ARTEFACT THE
    AUTHOR MUST KEEP: if it is not uploaded on `resume`, the audit genuinely
    restarts at Phase 1, because the evidence S5-1A certifies against no longer
    exists in any form. This is disclosed rather than papered over — the
    alternative (accepting a ledger without its evidence) is exactly the
    false-clean the completion gate exists to prevent.
  • FACT EVIDENCE IS ON DISK, NOT IN THE TRANSCRIPT (v2.14/B3). The reasoning
    stream carries one verdict line per verification; the raw query/URL/time/
    snippet lives in evidence/facts/ and is what C5 certifies against. A reader
    auditing the audit must open those files — the chat transcript is deliberately
    not a second copy of them, because retaining it is what exhausted the session
    and, with it, the evidence dir. The concept cache means a claim shared by
    several questions is verified ONCE; C5 reports distinct-files-per-reference so
    that reuse is visible and distinguishable from a shortfall.
  • FIGURE CONFORMANCE ON PRE-v5.34 PAPERS (v2.13). The twelve figure-conformance
    gates are arithmetic over the saved PNG AND its FigureSpec sidecar. A paper
    generated before Step 7 v5.34 carries no sidecar in its registry, so the
    sidecar-dependent half of each gate (placement scale, on-page label size,
    declared hues, series redundancy, glyph coverage) cannot be evaluated for it
    and is reported as an EC-V18 legacy WARN rather than a verdict. The
    PIXEL-only half (DPI metadata, plot-area degeneracy, coloured fraction, alt
    text) still runs on every paper. Full figure coverage requires regeneration
    on Step 7 v5.34+; until then the shortfall is disclosed here on every run and
    is never presented as a pass.
  • Web-verified facts are correct as of the audit timestamp; later real-world changes
    are outside Step 8's window.
  • Step 8 cannot prove a distractor is wrong in EVERY conceivable context — it proves
    wrongness under every REASONABLE reading (RA-12); genuinely contested conventions are
    pinned via section_rules, never adjudicated ad hoc.
  • COMPLETION-GATE RESIDUAL (v2.6): S5-1A verifies that each stamp names a durable
    evidence file that EXISTS and is non-trivial — it cannot prove the model reasoned
    correctly INSIDE that evidence (that a saved source actually supports the fact, that a
    viewed montage was truly scrutinised). Evidence-binding shrinks the residual to "the
    model would have to produce every montage, saved source and recompute trace — i.e.
    perform the audit — in order to fake having performed it," which is the point at which
    faking and doing converge. This is the structural ceiling of an LLM-driven audit; it is
    not a mathematical guarantee of reasoning correctness, and it is disclosed here rather
    than overclaimed.

# ════════════════════════════════════════════════════════════════════════
# §20 — SUBTOPIC_ID CONTRACT (consumer role — v1.7/v2.4 cross-step authority)
# ════════════════════════════════════════════════════════════════════════
#   Step 8 is a pure CONSUMER of the subtopic_id contract (Step 0 mints; Step 1
#   enforces; Step 7 joins). Step 8 reads subtopic_manifest.json to:
#     • map each question to a subtopic_id (B-ALLOC) by matching its rendered content
#       to section_rules patterns keyed by id — never by display-name string-match;
#     • read mandatory_every_mock[] + alternation_groups{} (B-MANDATE);
#     • re-derive presentation_family / concept_group hints (manifest carries them) for
#       B-SCENARIODUP / B-PRESENTDUP.
#   Step 8 NEVER mints an id and NEVER joins on a display name. A question that cannot be
#   mapped to any manifest subtopic_id is itself a defect (it does not belong to the
#   blueprint allocation) → investigate + RG. The id recipe and contract carry zero
#   exam-specific values (Step 0 §15).

# ════════════════════════════════════════════════════════════════════════
# §21 — CROSS-FILE PROPAGATION & REGRESSION LOCK (v2.6 — apply IN LOCKSTEP)
# ════════════════════════════════════════════════════════════════════════
#   The v2.6 completion gate + hardened self-test do NOT reach the ~200 exams if they
#   live only in this spec's PROSE. The audit.py each exam actually runs is BORN in the
#   Step-6 generator, per exam. Therefore these changes MUST be applied together:
#
#   | File | Required change (P0 — without it the fix is inert for real exams) |
#   |---|---|
#   | THIS file (Appendix A) | The canonical auditor: --audit-state + C1–C7 completion |
#   |                        | gate + the fixture-based self-test (already below).       |
#   | Framework_Blueprint.md §13-7A (the Step-6 B3 generator) | Generate EXACTLY this   |
#   |   canonical script — NOT the 13-gate constant-print MVP. This is where the auditor |
#   |   the Step-8 run executes is created; if the generator still emits the hollow stub,|
#   |   P1 (hardened) will HARD STOP every exam until it is fixed here. Retire the MVP    |
#   |   `def self_test(): print("SELF-TEST: 13/13 PASS")` stub.                          |
#   | Framework_MockTestCreate.md Appendix A (transitional template source) | Replace the|
#   |   AUDIT_SCRIPT_CONTENT constant-print self_test with the fixture-based one; add     |
#   |   --audit-state + C1–C7. Retire the "GATE-COUNT CONTRACT accepts ANY N/N" clause —  |
#   |   it must accept ONLY a fixture-based N/N with N>=AUTH_GATE_FLOOR.                   |
#   | validate_framework_md.py | Add the 6 regression tests below + a check that MANDATE  |
#   |   B / RA-0 / RA-15a / RA-15b / S4-3A / S5-1A / P0.5 headings all exist and          |
#   |   cross-refs resolve.                                                               |
#   | Framework_MockTestExplainAudit.md (Step 10) + Framework_MockTestExplain.md §18      |
#   |   (Step 9 self-audit) | Same false-clean chain (Claude-driven Part-B-style          |
#   |   certification behind prose). Apply the parallel completion-gate pattern so a bad  |
#   |   explanation / answer-key set cannot ship the way a bad paper did.                 |
#   | audit_mutation.py (v2.21.2) | MUTATION TESTING IS A RELEASE GATE. Run              |
#   |   `python3 audit_mutation.py --max-survivors N` where N is the CURRENT budget      |
#   |   (0 as of 2026.08.02.6 — ABSOLUTE). The count MUST NOT INCREASE: a release that   |
#   |   untested finding FAILS here. Lower N whenever survivors are retired; never       |
#   |   raise it. A SURVIVING mutant means no fixture can detect that finding being      |
#   |   deleted outright — the hollow-branch class, caught mechanically instead of by    |
#   |   a human reading code after it shipped. Inherited survivors awaiting fixtures:    |
#   |   NO INHERITED SURVIVORS REMAIN. All gates at 100%: gate_dossier (v2.21.2),         |
#   |   gate_options (v2.21.3), gate_images (v2.21.4), gate_nat + gate_zip +              |
#   |   gate_seccount + restore_checkpoint (v2.21.6). 27/27 emissions killed.             |
#   |   restore_checkpoint (1). CHECK AO catches a tautological fixture SHAPE; only      |
#   |   mutation catches a finding that is simply never triggered. Both are required.    |
#   | audit_canonical.py self_test() (v2.21) | EVERY new gate MUST ship at least one   |
#   |   DISCRIMINATING fixture per BLOCK SHAPE it can meet — text options, IMAGE options |
#   |   (bare label + picture), NAT (zero options), ENUMERATED-STEM, and a short-set     |
#   |   negative. A fixture that RESTATES THE IMPLEMENTATION (old fixture 92, retired    |
#   |   v2.21) is NOT a fixture: it cannot fail and it reports green. MUTATION-VERIFY    |
#   |   each one — it MUST measure False on the pre-fix build. Enforced by CHECK AO.     |
#   |   Any helper answering a structural question two gates share MUST be exercised by  |
#   |   a PARITY fixture (92d). Enforced by CHECK AN.                                    |
#   | Framework_DeliveryFooter.md | No change; F2 already fires only post-certification.  |
#   |   Its correctness now depends on S5-1A actually gating certification.               |
#
#   REGRESSION TESTS (add to validate_framework_md.py / the Appendix A self-test — a
#   build that passes all seven is provably immune to the exact failure that occurred):
#     1. SKIPPED-PHASE-2: audit_state with batches_done=[] and empty ledger; run
#        --final --audit-state → MUST exit non-zero, COMPLETION-GATE failing C1+C2.
#     2. PARTIAL-REVIEW: ledger with total_questions-1 entries → MUST fail C2 naming
#        the missing Q.
#     3. UNSOURCED-FACT: a factual entry with fact_sources=[] (or a named file absent)
#        → MUST fail C5.
#     4. UNVIEWED-FIGURE: a figural entry with no 'image' stamp (or its montage file
#        absent) → MUST fail C6.
#     5. HOLLOW-SELF-TEST: a script whose self_test() only prints "N/N PASS" with no
#        fixtures → MUST be rejected at P1 (fixture-based check fails / N<floor).
#     6. TRUNCATED-INPUT: a blueprint.json cut mid-object → MUST HARD STOP at P0.5
#        (A-INTEGRITY), not proceed.
#     7. HEADER-TOKEN-FALSE-POSITIVE (v2.7.5 — A-INTEGRITY-FALSEPOS-01): run P0.5 against
#        a section_rules.md fixture built by literally invoking (or byte-for-byte
#        replicating the header-writing portion of) Step 5's write_section_rules() —
#        i.e., a real, complete, well-formed file using the actual '=== EXAM_STRUCTURE
#        ===' token. MUST NOT raise HARD STOP (P0.5 / A-INTEGRITY). This is the
#        regression fixture that would have caught the exact false-positive defect that
#        blocked every exam's Step 8 on framework builds v2.6-v2.7.4 (fixed at v2.7.5) —
#        empirically verified via a 5-fixture harness (valid file / empty file / early
#        truncation / pre-v2.3 legacy file / valid file containing an unrelated
#        "same_category" substring), all five behaving correctly post-fix. Paired with
#        validate_framework_md.py Check T (§6.3), which catches this defect class
#        automatically at spec-authoring time by cross-checking every consumer's literal
#        hard-stop pattern against the actual producer output, across all files in a
#        batch run — not just this one instance.
#
#     ── v2.12 additions (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING) ──────────────
#     Tests 8 and 9 are the two that would have caught the v2.10 defect. All eight
#     are implemented as fixtures 43-52 in audit_canonical.py self_test() (61/61 at
#     v2.12; the v2.21.6 build prints 136/136 — see tests 16-20).
#     8. NON-DORMANT-BRANCH COVERAGE: a registry carrying figural_manifests[].
#        object_types + subtopic_ids, with blueprint_core importable → the run MUST
#        NOT raise and A-FIGPROFILE MUST print a NON-DORMANT verdict. THE ENTIRE
#        ROOT CAUSE WAS THAT NO FIXTURE DID THIS. (fixtures 43, 44)
#     9. MISSING-ENGINE DEGRADATION: same fixture, blueprint_core NOT importable →
#        MUST NOT raise, MUST exit 0, MUST print A-FIGPROFILE WARN "NOT CHECKED".
#        (fixture 45)
#    10. UNDEFINED-NAME SCAN: AST-scan the file for any Load-context name never
#        bound at any scope, builtins whitelisted → ZERO results. Self-hosted as
#        fixture 52, so it runs on EVERY self-test in EVERY exam project, not only
#        in CI. This is the GENERALISED guard: it catches the next `bc`-class
#        defect automatically, in any gate, without anyone remembering to look.
#    11. DECLARED-VS-ACTUAL DEPENDENCY PARITY: for each routed .py, every repo
#        module it imports MUST appear in that trigger's routes.json entry.
#        (validate_framework_md.py — catches D5/D7 automatically for all future
#        delegations, on BOTH the generator and auditor sides.)
#    12. TRUNCATED-ENGINE: blueprint_core truncated mid-function → WARN, no
#        traceback. Proves the guard catches SyntaxError, not merely ImportError —
#        `except ImportError` alone FAILS this test. (fixture 45 pattern / P0.5)
#    13. STALE-ENGINE: an engine missing one delegated function → WARN, no
#        traceback. Proves the L2 capability check is present; an import guard
#        alone lets AttributeError escape at the call site. (fixture 46)
#    14. GATE-ROSTER INVARIANCE: run with and without the engines → IDENTICAL COUNT
#        of printed gate lines; only severities differ. Restores §R15.
#    15. CONTEXT-2 SIMULATION: copy audit_canonical.py ALONE into an empty dir with
#        only the data files and run it. THIS IS THE TEST WHOSE ABSENCE PRODUCED THE
#        WHOLE DEFECT CLASS. The developer environment is Context 1 (all 33 repo
#        files importable); every one of the ~200 exams runs Context 2 (the script
#        alone beside 5 data files). A CI job that never simulates Context 2 cannot
#        protect Context 2. Every other test can pass and this failure mode can
#        still recur.
#
#    16. IMAGES-IN-A-BLOCK: build a docx with real inline drawings and assert
#        Block.images is populated with name/rid/descr/path. NO FIXTURE HAD EVER
#        PUT AN IMAGE IN A BLOCK — that absence is the entire D1 root cause, the
#        exact analogue of test 8's missing object_types registry. (fixtures
#        53-55: attachment, per-drawing alt-text attribution, table-cell images)
#    17. NON-VACUOUS FIGURE GATES: with figures present, every one of the twelve
#        must report a NON-ZERO evaluated count, and a zero-image paper must say
#        "dormant" rather than "conform". (fixtures 56, 58, 59)
#    18. FIGURE-GATE ROSTER INVARIANCE: exactly ONE line per figure gate, with
#        and without figures — locks out the duplicate second A-FIGDPI line and
#        keeps the v2.12 gate-count integrity signal usable. (fixture 57)
#    19. SEVERITY SPLIT: an identical finding must FAIL on a figure carrying a
#        sidecar and WARN on one that does not (EC-V18 delivery tolerance). A
#        build that FAILs the legacy case takes every pre-v5.34 exam out of
#        certification. (fixtures 60-62, incl. spec-transport key resolution)
#    20. END-TO-END WIRING: run the REAL run_audit() on an image-bearing docx and
#        assert the gates evaluated figures. Fixtures that call the helper
#        directly ALL still pass when the call inside run_audit is deleted —
#        mutation-verified — which is the v2.10 defect shape exactly: written at
#        the call sites, bound nowhere. Test 15 (Context-2) proves the file runs
#        ALONE; this proves its entry point actually invokes what it added.
#        (fixture 63)
#    24. VISION DEGRADATION (v2.16/D2+D4): a MEASURED outage certifies DEGRADED at
#        exit 0; the SAME stamp with no failed probe FAILS; a RECOVERED probe with
#        un-upgraded stamps FAILS; a trivial montage still blocks; a MIXED ledger is
#        legal; a healthy run is byte-identical to v2.15; the probe sidecar leaks no
#        glyph; and a render failure is never a vision verdict. NO FIXTURE HAD EVER
#        SIMULATED A VISION OUTAGE before v2.16 — the fifth hollow branch this corpus
#        has found. (fixtures 78-85)
#    23. CHECKPOINT ROUND TRIP (v2.15/C1): build a checkpoint, DESTROY the source
#        directory (the session boundary), restore into a fresh one, and run the
#        REAL completion gate -> MUST certify. This is the fixture the release
#        exists for; before C1 it was impossible. Plus: nested evidence paths
#        rebase; a tampered member, a wrong paper MD5, a wrong mock/exam, a
#        non-checkpoint archive and an UNKNOWN SCHEMA are each REFUSED, and every
#        refusal leaves NOTHING on disk. The unknown-schema case was found by
#        mutation testing — the guard could be deleted with every other fixture
#        still green, which is exactly the hollow-branch class this corpus keeps
#        rediscovering. (fixtures 70-77)
#    22. FACT-RECORD SHAPE (v2.14/B3): a saved fact that is a 1-byte stub, is
#        unparseable, or blanks any of query/url/retrieved_at/snippet MUST fail
#        C5; a well-formed record MUST pass; a record LIST and a file shared by
#        two questions MUST pass and be REPORTED as cache reuse. The stub case is
#        the file that CERTIFIED before v2.14 — once the raw result lives only on
#        disk, accepting it would erase the evidence while still certifying.
#        (fixtures 65-69)
#    21. PER-FIGURE FAULT ISOLATION: make figural_core raise on one figure and
#        assert NO A-GATEERROR, all twelve gate lines still printed, and a
#        coverage WARN. Found empirically, not by inspection: one partially
#        recorded FigureSpec raised out of g_figlabel(), _safe_gate turned it
#        into A-GATEERROR, and the whole A-IMAGES gate died — roster 47 -> 36.
#        The spec now arrives from the REGISTRY, so a per-item L3 guard is
#        mandatory exactly as v2.12 required one for blueprint_core. (fixture 64)
#
#   ── OPERATOR ACTION: REFRESHING THE ~200 DEPLOYED COPIES (v2.12) ──────────────
#   Fixing the repo does NOT fix the estate. Every exam project's
#   [ExamCode]_mock_test_audit.py is a COPY taken at Step 6 B3. Two sanctioned
#   paths, both safe; use either or both:
#     (A) PER-EXAM REGENERATION (preferred, permanent). Re-run Step 6 B3 for the
#         exam. It re-copies the corrected audit_canonical.py and now also ships
#         blueprint_core.py + figural_core.py. §13-7A collision handling makes this
#         idempotent and safe to repeat.
#     (B) IN-SESSION REPAIR (immediate, per-run). If a Step-8 run meets an auditor
#         copy that predates v2.12 — diagnosed by a traceback on the real paper, or
#         by a short gate roster — Step 8 is AUTHORISED under P0.5 sanctioned-repair
#         policy (b) to replace that copy with the current repo audit_canonical.py,
#         re-run P0.5 + P1, log to session_log.inputs_repaired[], and disclose in
#         §R13. This is a byte-exact restore from a hash-tracked source, never a
#         guess, so it carries none of the risk that bars repairing DATA files.
#   Until an exam is refreshed by (A), path (B) makes every Step-8 run complete.
#   Neither path changes any paper, any answer, or any registry content.
#
#   AUTH_GATE_FLOOR REMAINS 35 — do NOT raise it to 61. The floor gates the DEPLOYED
#   copies; raising it above their printed count would HARD STOP every un-refreshed
#   exam and convert a coverage improvement into an estate-wide outage. At 35, a
#   v2.11 copy (51/51), a v2.12 copy (61/61), a v2.13 copy (107/107) and a v2.21 copy
#   (136/136) all pass, and
#   the estate migrates
#   exam by exam with zero downtime.
#
#   THE UNIFYING PRINCIPLE (why this closes the chain across all 200 exams): every
#   certification claim is the EXIT CODE OF A COMMAND, never a sentence the model writes
#   about itself. Where a check is Claude-driven (semantic, visual, factual), it deposits
#   a stamp AND a durable evidence artefact in a machine-readable ledger, and a runnable
#   gate verifies both before delivery. Prose describes; only code certifies.


# ════════════════════════════════════════════════════════════════════════
# APPENDIX B — ENGINE API CONTRACT (NORMATIVE, v2.18 / D3)
# ════════════════════════════════════════════════════════════════════════
#   WHY THIS EXISTS. The spec ORDERS the operator to call these engines (S0-1
#   items 7-8, the S5-2 A-FIGPROFILE row) while SKILL.md Rule 2 forbids reading a
#   .py into context. That left NO sanctioned discovery path for an API the spec
#   mandates, so trial and error was the only route — and it produced wrong
#   verdicts along the way. On a live run this cost two turns and one materially
#   wrong intermediate finding (6 failing subtopics reported where the true answer
#   was 2). audit_canonical.py calls these functions correctly internally, so all
#   105 fixtures passed while the gap bit the OPERATOR every time.
#
#   Signatures below are INTROSPECTED from the engines in the verified clone, not
#   transcribed. Regenerate with:
#     python3 -c "import inspect,blueprint_core as bc;print(inspect.signature(bc.check_figural_conformance))"
#
#   ── blueprint_core ────────────────────────────────────────────────────────
#   figural_generation_profile(pyq_image_analysis: dict) -> dict
#       ARGUMENT PROVENANCE — THE ONE THAT BITES: a PARSED PYQ_IMAGE_ANALYSIS
#       block. NOT the raw section_rules.md text. Passing raw text returns
#       mode='unconstrained' for EVERY subtopic, which reads as "the profile
#       system is inert paper-wide" and is silently wrong.
#       RETURNS keys: mode ('unconstrained'|'observed'|'dominant'), dominant[],
#       observed[], transformation_types[], arrangement_types[],
#       complexity_dist{}, reason.
#
#   check_figural_conformance(generated_types: list[str], profile: dict,
#                             floor: float = 0.55) -> tuple[str, str]
#       RETURNS A 2-TUPLE ('PASS'|'FAIL'|'SKIP', message) — NOT a dict. Truth-testing
#       the tuple makes every subtopic read as PASS (a non-empty tuple is always
#       truthy); .get('ok') raises. Read element [0].
#       CORRECTION TO A WIDELY-CIRCULATED CLAIM: an unconstrained profile returns
#       'SKIP', NOT 'FAIL'. Verified by introspection and source. A gap report
#       asserted the opposite and prescribed a caller-side skip guard; documenting
#       that would have enshrined a false precondition. The engine already handles
#       it — SKIP is what keeps ~200 legacy exams passing untouched (EC-V18).
#
#   derive_image_roles(imap: dict) -> dict
#   IMAGE_ROLES = ('stem_and_options', 'stem_only', 'options_only', 'none')
#   classify_paper_era(observed_q_numbers, cfg_total, min_cfg_q, max_cfg_q,
#                      observed_types=None, cfg_type_for_q=None)
#
#   ── figural_core ──────────────────────────────────────────────────────────
#   make_figure_spec(question, fig_class, display_in, series=None, axes=None,
#                    key_mode='none', target_onpage_pt=10.0, role='problem') -> dict
#   render_figure(draw_fn, out_path, spec)      # MUTATES spec with png_px, png_dpi,
#                                               # placed_in, placement_scale,
#                                               # font_pt_native — read back from the
#                                               # SAVED artefact, not predicted
#   write_spec_sidecar(spec, png_path)          # -> <png stem>.figspec.json
#   audit_figure(spec, png_path, descr=None) -> (hard: list, warns: list)
#   triage(findings, spec=None) -> {'BLOCKING': [], 'VOID_ITEM': [], 'AMBER': []}
#   is_legacy(spec) -> bool                     # no sidecar => pre-v5.33 => EC-V18
#   audit_gate_id(finding) -> str               # engine G-*/W-* -> catalogue A-*
#   preflight() -> {'available': {...}}
#
#   PRECONDITIONS THAT ARE NOT IN THE SIGNATURES:
#     • A-FIGPROFILE reads object types from registry.figural_manifests[mock].
#       object_types (v5.31+). batch_state.json is a Step-7 INTERNAL sidecar and is
#       NOT delivered to Step 8 (S0-1) — never look for it.
#     • S5-2 prose says SKIP unconstrained profiles and profiles whose
#       vision_status is 'unavailable'; the engine's own SKIP covers the former.
#     • Engine absent/truncated/stale: the v2.12 three-layer guard applies. Never
#       hand-roll a substitute (RA-9).
#
# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — UNIVERSAL EXAM-AGNOSTIC mock_test_audit.py (MANDATE A)
# ════════════════════════════════════════════════════════════════════════
#   v2.2 NOTE: This script is now AUTO-GENERATED by Step 6 (MockBlueprint) v1.20+
#   as its 6th output file. Users no longer need to copy it manually.
#   See Framework_Blueprint.md §13-7A for generation rules and lifecycle.
#   v2.6 NOTE: This is the CANONICAL auditor. Step 6 §13-7A + Framework_MockTestCreate.md
#   Appendix A MUST generate EXACTLY this (with the --audit-state completion gate and the
#   fixture-based self-test) — NOT the retired 13-gate constant-print MVP (§21). MANDATE A
#   (P1 hardened) REJECTS any script whose self-test is not fixture-based with N>=35.
#
#   The script below is RETAINED as a FALLBACK for cases where Step 6 was run
#   before v1.20 (legacy). If the script is missing from project Files:
#     PREFERRED: re-run Step 6 B3 (generates the script automatically).
#     FALLBACK:  copy the script below verbatim, save as [ExamCode]_mock_test_audit.py,
#                upload to the [ExamCode] project Files.
#   No exam-specific edits are required (it parameterises itself entirely from
#   blueprint.json + section_rules.md + subtopic_manifest.json + registry.json).
#   MANDATE A requires it for Step 8.
#
#   Validation status (v2.8):
#     • `--self-test`  → SELF-TEST: 136/136 PASS  (exit 0) on the v2.21.6 canonical
#       build (was 51/51 at v2.8, 61/61 at v2.12). The 35 v2.5 tests cover every
#       gate plus the edge cases (roman/alpha/figural option labels; an enumerated
#       passage point that must NOT inflate the option count; accented-Latin and
#       Greek-math text that must NOT trip A-SCRIPT; a Devanagari word that MUST trip
#       it on an english exam and pass on a hindi one; attribute-order-independent rels
#       parsing; the v1.2 MSQ cases; the v1.4 NAT cases; the v1.5 A-SECHDR-name-catch;
#       a 0-block document that must not crash) PLUS 8 v2.6 COMPLETION-GATE fixtures
#       (S5-1A C1–C7): a complete evidence-backed ledger ⇒ COMPLETION-GATE PASS; a
#       skipped Phase 2 ⇒ C1+C2 FAIL; a partial review ⇒ C2 FAIL; an unsourced fact ⇒
#       C5 FAIL; a fact whose saved file is missing ⇒ C5 FAIL; a paper artefact with no
#       ledger stamp ⇒ C7 FAIL; a stamp whose evidence file is missing ⇒ C6 FAIL; a
#       stamp whose evidence file exists ⇒ PASS. PLUS 2 v2.7 A-HEADER-inversion fixtures
#       (a pre-Q.1 title/info block ⇒ A-HEADER FAIL i.e. strip; the SAME block with
#       EXAM_STRUCTURE paper_header_block declared ⇒ dormant, no failure). PLUS 2 v2.7.1
#       A-MATCH-TABLE fixtures (a MATCH question rendered WITHOUT a table ⇒ A-MATCH-TABLE
#       FAIL; the same MATCH body rendered AS a real table ⇒ dormant, no failure). PLUS
#       4 v2.8 A-NAT-GRADE fixtures (S7-NEW-C self-consistency backstop: a sidecar
#       nat_grading_value that doesn't match a fresh derive_nat_grading() re-run on its
#       own recorded inputs ⇒ FAIL, e.g. a stored '3e-9' when re-derivation gives '3';
#       a stem_precision-driven decimal_fixed value that DOES match ⇒ PASS; dormant when
#       no numerical subtopics; dormant when no --key sidecar supplied).
#     • AUTH_GATE_FLOOR = 35 (MANDATE A / P1). N (51) >= floor.
#     • run against a real 100-question paper → parses all 100 blocks; the
#       blueprint-driven gates (A-COUNT 100/100, A-SEQ 1..100, A-SECCOUNT
#       25/25/25/25) pass; A-OPTN correctly reads 4 image-options on figural
#       questions (no false FAIL); A-OMML-FLOOR raises the "zero OMML in a
#       quant paper → math may be hiding as raster" flag; A-FIGCOMP-LINE
#       catches a genuine two-rasters-on-one-line defect. No false positives
#       on legitimate figural images named "Picture N" (the emitter-naming gap
#       — handled by the view-backed two-tier A-MATHRASTER, S5-3). With
#       --final --audit-state on a certified run → COMPLETION-GATE: PASS.
#
#   Dependencies (CORRECTED v2.12 — the previous "python-docx + Python stdlib only"
#   claim became false at v2.10 and was never updated; a maintainer reading it had an
#   explicit in-spec assurance that no repo engine was needed, which is how the
#   A-FIGPROFILE delegation shipped without its import):
#     python-docx + Python stdlib, PLUS two repo engines —
#       blueprint_core.py  -> A-FIGPROFILE (figure-profile conformance)
#       figural_core.py    -> the 12 A-FIG* figure-conformance gates (v2.11)
#     Both are LAZILY imported and TRIPLE-GUARDED (import / capability / call site).
#     If either is absent, truncated, or stale, its gates report an explicit WARN
#     skip and the audit STILL COMPLETES. No engine condition can halt a run.
#   Exit 0 iff no FAIL AND (when
#   --audit-state is given) COMPLETION-GATE: PASS; WARNs are surfaced for Part-B / §7
#   reviewer adjudication (the Step-8 certification gate, §12-2, decides whether a
#   fixable WARN blocks delivery).
#
#   USAGE:
#     python3 [ExamCode]_mock_test_audit.py --self-test
#     python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#         --blueprint BP.json --rules RULES.md --manifest MAN.json \
#         --registry REG.json --mockN N --final
#     python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#         --blueprint BP.json --rules RULES.md --manifest MAN.json \
#         --registry REG.json --mockN N --final \
#         --audit-state [ExamCode]_M[N]_audit_state.json     # Phase-3 completion gate (S5-1A)
#
#   The script body follows (save the fenced content below as the .py file):

```
# THE CANONICAL AUDITOR SOURCE WAS EXTRACTED (2026-07-31, v2.11.2) TO THE
# HASH-TRACKED REPO ENGINE FILE:   audit_canonical.py   (bootstrap-verified,
# byte-identical to the fenced block that lived here through v2.11.1).
#
# SINGLE SOURCE OF TRUTH: audit_canonical.py. To generate an exam's auditor,
# copy that file VERBATIM to [ExamCode]_mock_test_audit.py (it self-parameterises
# at runtime; no exam-specific edits). VALIDATE with:  --self-test  (fixture-based,
# N>=35; currently 136/136). All MANDATE A / P1 / §21 rules apply to that file
# unchanged; §21's regression tests run against it.
```

# ════════════════════════════════════════════════════════════════════════
# END OF Framework_MockTestCreateAudit v2.21.6
# ════════════════════════════════════════════════════════════════════════
