# Framework_NotesCreate v2.7.2 — Notes Pipeline Step NC (Subtopic Notes Drafting)
# v2.7.2 — 2026-08-15 — THE SPACING RHYTHM (owner refinement of v2.7.1 in
#   the same release wave; notes_docx v1.5). v2.7.1 stopped tables from
#   touching; the owner's review of the rebuilt document showed the rhythm
#   still cramped — tables hugging the bullet text above them and section
#   bars starting with no visible break. The §4 tail rule is now the full
#   SPACING RHYTHM: one deterministic post-assembly pass sizes every
#   vertical gap by context (larger before L1/L2 bars, medium between
#   tables, small between text and a table, either direction); the engine
#   constants are the single authority. All per-case spacing emission is
#   gone from the builder's block loop, so the rhythm holds for every
#   block combination by construction. Model, parse(), W-3 byte-identity:
#   unchanged. Companion: notes_docx >= v1.5.
# v2.7.1 — 2026-08-15 — UNIVERSAL SPACING INVARIANT
#   (GAP-2026-08-15-ADJACENT-TABLES; field report from the first live NC
#   run: heading bars, data tables and boxes rendered FUSED, zero gap —
#   Word merges directly adjacent tables and nearly every element of these
#   notes is a table). The §4 spacer rule was the box-after-box special
#   case; notes_docx v1.4 now guarantees the GENERAL invariant — no two
#   tables are ever adjacent anywhere in the body, enforced by a
#   post-assembly pass so it holds for every block combination, current
#   and future, by construction. Model, anatomy, colours, numbering,
#   parse(): all unchanged; W-3 byte-identity preserved. Existing drafts
#   gain the spacing on their next rebuild (NA §0B P-4b reads the byte
#   difference as the documented builder-upgrade diagnostic, never a
#   stop). Companion: notes_docx >= v1.4.
# v2.7.0 — 2026-08-15 — THE FORMAT CONTRACT (figure vs text balance; owner
#   decisions of the 2026-08-15 design session, approved proposal; pairs
#   with Framework_NotesAudit v3.5.0 §5 G-12; notes_core >= v2.10,
#   notes_audit >= v2.7). Reading a figure (V–I curve, ray diagram,
#   potential well, phase diagram) is a SEPARATE skill from knowing the
#   theory — a subtopic with perfect prose and zero figure practice is a
#   gap wherever the exam asks figure-based questions. §4 B3a gains the
#   FORMAT CONTRACT, derived entirely from evidence every bank already
#   carries (the per-question figure flag + concept tags — no new field,
#   no re-ingest): FMT-1 both formats attested -> both taught, with >= 1
#   concept section PAIRING a rendered figure with an Example that reads
#   it (HARD, G-12-enforced); FMT-2 frequency shapes EMPHASIS — the lead
#   Example follows each concept's dominant format — never exclusion and
#   never count-mirroring (spread-not-count, applied to formats); FMT-3 no
#   evidence, no demand — a zero-figure slice never forces a figure. The
#   old unit-level requires_figure ADVISORY is superseded by FMT-1's hard
#   pairing where figure evidence exists (the advisory itself still rides
#   in G-12 meta). Anatomy, colours, density, builder: all UNCHANGED —
#   figures render through the existing F-4 rules. Rollout follows the
#   G-12 precedent: applies at each unit's next audit; no grandfathering
#   flag exists or is needed.
# v2.6.2 — 2026-08-14 — ADVERSARIAL-REVIEW FIXES (independent fresh-eyes
#   review + 400-trial property fuzz; pairs with notes_core v2.9,
#   notes_audit v2.6, Framework_NotesAudit v3.4.2, Framework_NotesBlueprint
#   v3.1.1). Six fixes: (1) new I-7 — a TIER-3 unit CAN be a fusion host:
#   the inbound fused questions ARE the evidence, so it ships its TIER-3
#   anatomy PLUS the demanded integration section(s), the only Examples in
#   such a unit; G-13 demands them, G-12 (header-slice contract) never
#   double-demands. (2) I-1 placement stated for units without B5 (before
#   B6; the mechanical check is unchanged). (3) I-6: EVIDENCE OUTRANKS the
#   1-2-partner style bound — an attested 3-partner fusion at a mid-topic
#   unit gets its section there; the bound shapes unattested SME sections
#   only (the old wording deadlocked against a G-13 demand). (4) I-2:
#   duplicate partner names are Topic-qualified (NB E-16). (5) PIPELINE
#   POSITION synced to NA v3.0.0 (was "audit + convergence loop" — the
#   same stale line NB v3.0.3 fixed on its side). (6) PREREQUISITE: the
#   "returned by NA for full regeneration" path died with NA §4 L-2
#   (regeneration is NA-internal); the real NA->NC return is the missing-
#   draft_ref preflight. Companions: notes_core >= v2.9.
# v2.6.1 — 2026-08-14 — ONE ORDER-MAP BUILDER (line-by-line certification
#   sweep of the v2.6.0 feature; pairs with notes_core v2.8 and
#   Framework_NotesAudit v3.4.1). v2.6.0's I-5 said "unit_order maps
#   subtopic_key -> the registry's persisted ordinal" in PROSE and left NC
#   and NA to each build the map — the author/gate drift class this
#   framework exists to kill (two builders, one contract). I-5 now names
#   notes_core.unit_order_from_registry as the ONE builder (ordinals = the
#   persisted unit_code digits, NB §1A A-3); NA §2 and G-13 call the same
#   function, so filing can never disagree between author and gate. Wording
#   only on this side; the engine change and the companion audit-boundary
#   fix (a fused question is SOLVED where it is TAUGHT) live in notes_core
#   v2.8 / Framework_NotesAudit v3.4.1.
# v2.6.0 — 2026-08-14 — IN-SUBTOPIC INTEGRATION SECTIONS (owner decisions of
#   the 2026-08-14 design session; approved on the DC/AC Circuits placement
#   demo; pairs with Framework_NotesBlueprint v3.1.0 §3B B-1,
#   Framework_NotesAudit v3.4.0 §5 G-13; notes_core >= v2.7, notes_audit >=
#   v2.5). Real exams fuse 2-3 subtopics in ONE question; the IFAS portal
#   links one page per subtopic (owner constraint), so the fusion is taught
#   IN-SUBTOPIC: new §4 B4a — an INTEGRATION SECTION closing the concept
#   stack, after every core concept's KEY POINTS and immediately before the
#   TRAP BOX. It is an ORDINARY concept section (same block type, own example
#   stack, own KEY POINTS; numbering, colours, gates all already apply — no
#   builder change of any kind) marked ONLY by its first bullet: the Combines
#   declaration. Rules I-1..I-6: placement (end of stack), the Combines
#   declaration + bridge bullets, backward-only partners (persisted teaching
#   order — students have met every ingredient), evidence-driven authoring
#   against notes_core.integration_target_for (latest-partner filing —
#   the SAME contract NA's G-13 gates, so author and gate can never
#   disagree), the last-subtopic capstone bound, and the no-earlier-partner
#   edge (no integration section). B8's mind map stays SUBTOPIC-ONLY —
#   merged concepts never enter it (owner decision). Anatomy is otherwise
#   UNCHANGED; TIER-3 unchanged; §7 bans apply to integration prose in full.
# v2.5.1 — 2026-08-14 — STALE ANATOMY REFERENCE (line-by-line certification
#   sweep). §2.1 called the fresh-numbered practice questions "§4 B4/B7" — a
#   leftover from a pre-v2.0.0 block layout. Under the CURRENT §4 anatomy B4
#   is the KEY POINTS box; the practice questions are B3 (Examples) and B7
#   (Recall Check). Reference corrected to "§4 B3/B7". Wording only; no
#   behaviour, gate or engine change.
# v2.5.0 — 2026-08-13 — COVERAGE CONTRACT AUTHORING (Phase 2, Recommendations
#   3+4; pairs with Framework_NotesAudit v3.3.0 §5 G-12; notes_core >= v2.6).
#   New §4 B3a: before drafting Examples, NC computes the unit's coverage
#   contract with notes_core.coverage_target_for over the unit's bank slice
#   and AUTHORS TO IT — at least one worked Example for every question type
#   the unit's own PYQs attest, and Examples spread across at least the
#   required number of DISTINCT concept sections. The contract is CONCEPT
#   SPREAD, deliberately NOT an example count (owner decision, 2026-08-13):
#   more Examples on one scenario add pages, not coverage — an additional
#   Example is justified only by an uncovered concept, scenario or type.
#   NotesAudit G-12 gates the SAME bank-derived contract on the shipped
#   file, so author and gate can never disagree. An empty bank slice means
#   no contract (TIER-3 "no examples where no evidence" unchanged). No model,
#   anatomy, colour or rendering change of any kind — B3a constrains WHERE
#   Examples go and WHICH types they teach, not how they are built.
# v2.4.0 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE (Point 1;
#   pairs with Framework_NotesAudit v3.2.0 and notes_docx v1.3). Every worked
#   Example (B3) now ends with TWO new elements, and a Recall (B7) carries
#   NEITHER:
#     (1) A per-option "why the other options fail" block — ONE line per WRONG
#         option, naming the specific error that produces it (MCQ: 3 lines;
#         MSQ: 4 − #correct; NAT: this becomes a "trap values" block of >= 1
#         line, each a wrong number and the mistake that yields it). The
#         builder stores these in the example block's why_wrong field.
#     (2) A one-line Educational Objective — the transferable takeaway — stored
#         in the objective field.
#   These are built THROUGH notes_docx.build like everything else (§4A):
#   notes_docx.validate_model enforces the exact per-option count and the
#   presence of the Objective at construction, and Framework_NotesAudit G-5
#   re-asserts both on the shipped file, so a missing rationale can never reach
#   a delivered document. The autopsy header renders in the TRAP red and the
#   Objective label in the L2 teal — both EXISTING §6A colours, so no new
#   colour is introduced. The new text is document-facing prose and is subject
#   to §7 in full (no question-type names, no years, no PYQ token). Anatomy,
#   density, math and numbering (§4A–§6A otherwise) are UNCHANGED.
# v2.3.1 — 2026-08-13 — OPTION CONTRACT MADE EXPLICIT (GAP-2026-08-12-NAPARSE
#   D-1). §4 B3 now states that the "N. " option marker is the ONLY
#   guaranteed plain text (w:t) on an option line: the option's CONTENT may
#   be entirely OMML, so any reader of a built document must never require
#   w:t content beyond the marker. Framework_NotesAudit §0B P-4 enforces it.
# v2.3.0 — 2026-08-12 — SHARED BUILDER + DRAFT PROVENANCE (GAP-2026-08-12-NADOCX
#   patch P2 of 2; pairs with Framework_NotesAudit v3.0.0).
#     (1) CONSTRUCTION IS NOW AN ENGINE. NC builds the .docx by calling
#         notes_docx.build(model, path) — never by hand-rolling paragraphs.
#         Until 2026-08-12 document construction lived only in this spec's
#         prose, so NC's run-time code was the sole implementation of the
#         section 6A colour map, the decimal cascade, box styling, spacer
#         paragraphs, rule F-7 and the OMML conventions. NA now writes
#         documents too (v3.0.0), and two implementations of one contract is
#         the defect class the 2026-08-10 sweep closed for filenames. New
#         section 4A states the content model and the derived-numbering rule.
#     (2) NUMBERS ARE NO LONGER WRITTEN BY NC. Every "n.k", "n.k.m",
#         "Example j" and "Recall j" is DERIVED from block order by
#         notes_docx.outline_of at render time. Section 6A's renumber rule is
#         satisfied structurally: there is no stored number that can go stale.
#     (3) DRAFT PROVENANCE (new section 9A). NC records
#         notes_core.docx_ref_for(draft) into the registry unit as draft_ref
#         (schema notes-registry/2.1). NA now receives its input as a CHAT
#         ATTACHMENT rather than from Project Files, so nothing else would
#         prove the file audited is the file NC produced. draft_ref is the
#         evidence for NA section 0B P-3.
#     (4) HANDOFF CHANGED (section 9). The draft is NO LONGER uploaded to
#         Project Files. Its footer badge is "Use locally" and the Next
#         callout instructs the operator to ATTACH it to the NA chat. The
#         registry is still uploaded, because NA reads it from Project Files.
#     (5) t3_mathcomp.py is now ROUTED to NC. F-3(a) has always required its
#         conventions, but the engine was never on NC's route — a real gap
#         found while wiring the shared builder.
#   Companions: notes_core >= v2.3, notes_docx >= v1.0. Anatomy, density,
#   format rules and content bans (sections 4-7) are otherwise UNCHANGED.
# v2.2.1 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). A
#   deployment review found F-1 restating the filename recipe in prose while
#   notes_core.notes_filename sanitises non-alphanumeric runs in {Slug} to "_"
#   — one contract, two implementations. F-1 now names the ENGINE as the single
#   authority, states the sanitisation, and requires NC to derive the draft
#   filename by CALLING notes_core.notes_filename — never by re-implementing
#   the pattern. The same sweep marked §5 and §6A as spec-lock-pinned (the
#   notes_core v2.1 SPEC-LOCK self-test pins every literal these sections
#   restate) and replaced §9's informal "[ExamCode]_<unit>.docx" with "the
#   unit's F-1 filename". Companion: notes_core >= v2.1. No behaviour change.
# v2.2.0 — 2026-08-10 — TAXONOMY-SYNCED OPERATOR INPUT (Framework_NotesBlueprint
#   v3.0.0). Units are identified by the Step-5 manifest sid (the registry key);
#   the OPERATOR identifies a unit by copying a cell from
#   [ExamCode]_taxonomy.xlsx — the SAME convention that workbook's "How to use"
#   sheet already teaches for Step 6. NEW §0: three-tier resolution via
#   notes_core.resolve_unit — (1) Sub Topic Id (column D), (2)
#   Subject::Topic::Sub Topic Name scope (columns A::B::C), (3) bare Sub Topic
#   Name (column C), norm-matched so case/dash/&/spacing variants resolve; a
#   multi-hit bare name STOPS and lists the candidates with their Topics for the
#   operator to choose; zero hits STOP with nearest-name suggestions — NEVER a
#   fuzzy auto-pick. §1.2 additionally verifies taxonomy_ref
#   (notes_core.verify_taxonomy_ref): a manifest changed since the blueprint was
#   built STOPS the unit back to NB, exactly like the stale-bank stop. F-1's
#   {Slug} is the sid's final component (notes_core.sid_slug), so every
#   delivered filename traces visibly to its taxonomy.xlsx row. Companion:
#   notes_core >= v2.0. B1's "n" and F-1's numbers come from the unit's
#   PERSISTED unit_code/seq_in_topic (NB §1A A-3) — they never churn on a
#   taxonomy re-run. All v2.1.x behaviour otherwise unchanged.
# v2.1.5 — 2026-08-10 — §8 wording aligned with §9/DeliveryFooter §3. Each
#   multi-unit request is separate PER-UNIT RUNS, each a complete step ending F2
#   (§9); the continue-confirmation is BETWEEN runs, not batches within one (NC
#   has no intra-run batching — that F1 pattern is NB's). §8 retitled RUNS AND
#   STATE and cross-references §9. Wording only; no behaviour change.
# v2.1.4 — 2026-08-10 — CROSS-CHAT HANDOFF SPECIFIED. NC runs in its own chat, so
#   its draft .docx must reach NA (a fresh chat) the same way NB's bank reaches NC.
#   New §9: NC present_files the draft + the updated registry and renders the F2
#   footer (4-cell NOTES bar "2 of 4"; Next → NA), so the handoff persists and the
#   next-step pointer actually prints. Pairs with Framework_DeliveryFooter v1.19.
# v2.1.3 — 2026-08-10 — POST-DEPLOY REVIEW. bank_questions_for now joins by
#   RECOMPUTING the subtopic key from stored fields (drift class closed), so an
#   older bank still reads correctly. Companion: notes_core >= v1.8.
# v2.1.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   bank_questions_for now joins via the hardened notes_core.subtopic_key
#   (syllabus_provenance.norm). Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route.
# v2.1.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 1 (bank staleness stop wired).
#   §1.2's "signals a stale bank" stop now has evidence: NC reads the blueprint's
#   bank_ref and calls notes_core.verify_bank_ref(bank_path, bank_ref) before
#   drafting; a sha256 mismatch (blueprint built from a different bank than the
#   one on disk) or a missing bank_ref STOPS the unit back to NB. Companion bump
#   to notes_core >= v1.6.
# v2.1.0 — 2026-08-10 — BANK CONSUMER (Framework_NotesBlueprint v2.0.0). NC no
#   longer reads Drive or builds its own PYQ bank. It LOADS the bank NB produced
#   (notes_pyq_bank.json), filters it to the unit's subtopic
#   (notes_core.bank_questions_for), and drafts from those records. The FIGURE
#   flag is the bank's stem_figures; the correct_answer and explanation are read
#   from the bank as SME grounding (never reproduced verbatim — §3 paraphrase
#   rule unchanged). §1 rewritten accordingly; all v2.0.0 anatomy/format/gates
#   (§4-§8) are unchanged.
# v2.0.0 — 2026-08-08 — REFINEMENT RELEASE (breaking anatomy change). Encodes the
#   12-item refinement set locked in the 2026-08-08 review session and approved
#   on the Enzyme Kinetics golden sample: title-only header; plain concept
#   headings; frequency tags removed from the document; "Example N" boxes with
#   the fixed stem/options/Answer/Explanation template; question types
#   constrained to the exam's own type set; hierarchical cascade numbering;
#   level-locked colour map; figure labels inside the image with no captions
#   and no exam vocabulary; no editorial lead-ins; no exam-type words, years,
#   or PYQ references anywhere in delivered text; EXAM LENS block removed;
#   RECALL CHECK re-defined as exam-format questions; structural-OMML +
#   styled-script math standard document-wide including diagrams.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
# [ExamCode] project | Notes Step NC | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_docx.py >= v1.5 — the SHARED builder. NC constructs the .docx ONLY
#                           through notes_docx.build (section 4A); it never
#                           hand-rolls a paragraph, colour, border or line rule.
#                           v1.5 carries the full SPACING RHYTHM (§4 tail —
#                           context-sized gaps, one post-assembly pass);
#                           v1.3 adds the why_wrong / objective fields (§4 B3)
#                           and validate_model's per-option-count enforcement
#   notes_core.py >= v2.10 — format_mix + format_by_concept in
#                           coverage_target_for (§4 B3a's FORMAT CONTRACT,
#                           v2.10); fully-resolved filing + unresolved reporting +
#                           duplicate-name qualification (v2.9);
#                           unit_order_from_registry (§4 B4a I-5's ONE
#                           order-map builder, v2.8); plus
#                           notes_filename AND docx_ref_for (section 9A's
#                           draft_ref), registry schema notes-registry/2.1,
#                           the D-1 bullet counter G-1 depends on, plus:
#                           resolve_unit (operator-input resolution), sid_slug,
#                           verify_taxonomy_ref (manifest staleness check),
#                           sid-keyed registry (notes-registry/2.0); plus
#                           LEVEL_COLORS / BOX_COLORS constants, PROSE_BAN
#                           lexicon, math gates, registry transitions, the bank
#                           readers (bank_load / bank_questions_for),
#                           verify_bank_ref (blueprint/bank staleness check),
#                           coverage_target_for (§4 B3a's contract, v2.6),
#                           and integration_target_for (§4 B4a's contract,
#                           v2.7 — latest-partner filing over the persisted
#                           order; grandfathered-dormant for pre-1.2 banks)
#
# PURPOSE:
#   Produce ONE subtopic's study-notes .docx (draft) from the blueprint unit
#   record plus that subtopic's PYQ evidence, such that Step NA can verify
#   every in-scope PYQ is solvable from the notes text alone.
#
# PIPELINE POSITION:
#   Notes Step NB (NotesBlueprint) → unit table + sources + allowed types
#   Notes Step NC (NotesCreate)    → THIS SPEC (1 unit per run; §8 runs)
#   Notes Step NA (NotesAudit)     → ground-truth solvability audit; from
#                                    Framework_NotesAudit v3.0.0 NA also
#                                    CORRECTS, REBUILDS and emits the unit's
#                                    _Final.docx (v2.6.2: line synced — the
#                                    same stale description NB v3.0.3 fixed)
#   Notes Step ND (NotesDeliver)   → delivery
#
# PREREQUISITE:
#   notes_blueprint.json + notes_registry.json exist; target unit is in state
#   BLUEPRINTED (or STALE, or re-run at NC for a missing draft_ref —
#   Framework_NotesAudit §0B P-3; v2.6.2: NA's §4 L-2 regenerates BY
#   ITSELF and "does not route back to NC", so the old "returned by NA for
#   full regeneration" path no longer exists). The
#   blueprint carries allowed_question_types (Framework_NotesBlueprint §6).

## §0 — UNIT INPUT RESOLUTION (operator-facing; shared convention with NA/ND)
The trigger's unit reference is WHATEVER CELL the operator copied from
[ExamCode]_taxonomy.xlsx (the Step-5 workbook; its "How to use" sheet teaches
this same convention for Step 6 — one convention platform-wide, usable by a
non-technical operator). Resolution is notes_core.resolve_unit against the
registry's units, in this priority order:
  1. Sub Topic Id (column D)                        -> exact registry key.
  2. Subject::Topic::Sub Topic Name (A::B::C)       -> full-tuple norm match.
  3. Bare Sub Topic Name (column C)                 -> norm match (case, dashes,
     '&' vs 'and', spacing and unicode variants all resolve).
Outcomes: a UNIQUE hit proceeds. MULTIPLE bare-name hits (same name under
different topics) STOP and list every candidate with its Subject + Topic — the
operator replies with the scope form or the Sub Topic Id; NC never picks. ZERO
hits STOP with the nearest-name suggestions and the instruction to copy the
exact cell — NC never fuzzy-picks a wrong unit. A malformed scope (not 3
'::'-separated parts) STOPS with the correct shape named. The resolved unit is
confirmed in the chat line as: <Sub Topic Name> (<sid>).

## §1 — UNIT OF WORK AND INGEST (bank consumer; NC no longer reads Drive)
1. One run = one subtopic. NB has already ingested the whole corpus. NC LOADS
   the bank (notes_core.bank_load on notes_pyq_bank.json) and selects this unit's
   questions with notes_core.bank_questions_for(bank, subject, topic, subtopic).
   Each record already carries: bank_id, exam_date + q_no, type, full stem (with
   OMML math) + options, correct_answer (verbatim), explanation (verbatim),
   stem_figures / solution_figures, concept_tags. The FIGURE dependency is
   simply `bool(stem_figures)` — no image re-extraction here.
2. No re-download, no re-read of Drive, no re-checkpoint of a bank: the bank is
   NB's artifact and is authoritative. BEFORE drafting, NC verifies BOTH
   staleness links: (a) the blueprint's bank_ref via
   notes_core.verify_bank_ref(bank_path, blueprint["bank_ref"]) — a sha256
   mismatch (the blueprint was built from a DIFFERENT bank than the one on disk)
   or a missing bank_ref STOPS the unit back to NB; (b) the blueprint's
   taxonomy_ref via notes_core.verify_taxonomy_ref(manifest_path,
   blueprint["taxonomy_ref"]) when [ExamCode]_subtopic_manifest.json is present
   in project Files — a mismatch means the taxonomy changed since the blueprint
   was built and STOPS the unit back to NB (units are STALE there); a missing
   taxonomy_ref means the blueprint predates Framework_NotesBlueprint v3.0.0 and
   also routes to NB for a re-blueprint (cheap: the ingested bank is untouched).
   If the bank is present and matches but has no questions for this subtopic,
   that signals a subtopic-key mismatch or a genuinely empty subtopic, also
   handled at NB, not by drafting. The unit's bank join uses the unit's stored
   manifest triple (section, topic, name) through bank_questions_for as before.
3. The concept map (concept → bank_ids → weight) orders the concept sections and
   sets depth. It is built from the selected bank records (concept_tags + stem
   content) and is INTERNAL ONLY: no frequency marker, star, count, anchor, or
   year derived from it may appear in the delivered document (§7). The verbatim
   correct_answer + explanation ground the SME drafting (terminology, the right
   method, the real distractor traps) but are PARAPHRASED per §3 — never copied.

## §2 — CONTENT AUTHORITY (SME MODE + CARVE-OUT)
1. The memory ban stays ABSOLUTE for question generation and answer keys of
   real PYQs. Notes CONTENT (including the fresh-numbered practice questions
   of §4 B3/B7) is SME-generated by Claude and earns trust ONLY via Step NA.
2. If a reference book is present in project Files or the resolved sources,
   it grounds terminology, notation and level — never copied.
3. No human review exists anywhere in this pipeline; NA is the sole gate.

## §3 — PYQ PROTECTION (paraphrase rule)
Examples are PYQ-ANCHORED but PARAPHRASED: fresh numbers and fresh wording.
Anchors (exam-date + Q number) are recorded in the bank and audit report
ONLY — never in the document (§7). Actual PYQ text is never reproduced.

## §4 — DOCUMENT ANATOMY (v2 — 8 blocks, locked)
  B1  TITLE — one title bar: "<n>. <SUBTOPIC NAME>", where n is the
      subtopic's 1-based sequence within its parent Topic per blueprint unit
      ordering. NOTHING else: no breadcrumb/mapping line, no doc code, no
      badge table, no legend, no prerequisite line. All such metadata lives
      in the registry and the chat delivery line only.
  B2  CONCEPT SECTIONS — headings numbered n.k carrying ONLY the concept
      name (no "CONCEPT k" prefix, no tags, no counts). Content: bullets,
      tables and diagrams per §5–§6, in prerequisite order from §1.3.
  B3  EXAMPLES — inside each concept, ONE question per box, titled
      "Example j" with j a single global sequence across the document.
      Fixed template (order is mandatory):
        line 1+  stem (NAT stems MUST state the unit and rounding precision)
        options  MCQ/MSQ only: numbered lines "1." to "4.", one per line
        Answer   bold; option number(s) for MCQ ("2"), comma-joined for MSQ
                 ("1,3"), bare numeric for NAT ("20.5")
        Explanation:  label line, then the working (equations per §6 F-3)
        SPEED HACK    ONLY where a genuine shortcut exists
        DISTRACTOR AUTOPSY  a per-option "why the other options fail" block:
                 ONE line per WRONG option, each naming the SPECIFIC error
                 that produces it, not merely restating the right answer.
                 Counts are exact — MCQ: 3 lines; MSQ: 4 − (number of correct
                 options); NAT: this becomes a "trap values" block of >= 1
                 line, each a wrong NUMBER and the mistake (unit slip, factor,
                 inverted ratio) that yields it. Stored in the block's
                 why_wrong field; header text is DERIVED from the type by the
                 builder (never authored), so the numbers cannot go stale. An
                 all-correct MSQ (no wrong option) carries no autopsy lines.
        Objective:  LAST — a single-line Educational Objective, the
                 transferable takeaway (the general principle, not this item's
                 answer). Stored in the block's objective field. Required on
                 EVERY Example.
      Question types MUST be drawn exclusively from
      allowed_question_types; across the unit the examples collectively
      cover every allowed type where the concept evidence supports it. A
      single-type exam yields single-type examples. Theory-style prompts
      (no options, no numeric target) are forbidden. Type names are never
      printed — the format itself communicates the type.
  B3a COVERAGE CONTRACT (v2.5.0 — what "enough Examples" MEANS). Before
      drafting any Example, compute the unit's contract:
        target = notes_core.coverage_target_for(bank, subject, topic,
                                                subtopic, allowed_types)
      and author to it: >= 1 worked Example for EVERY type in
      target's required_types (the types the unit's own PYQs attest — a
      subtopic whose PYQs include a numeric item gets a numeric Example,
      a theory-only subtopic is never forced one), and Examples spread
      across >= min_concepts_with_examples DISTINCT concept sections.
      THE CONTRACT IS SPREAD, NOT COUNT (owner decision, 2026-08-13):
      an Example is justified only by an uncovered concept, scenario or
      type — never author a second Example of a scenario an existing one
      already teaches; N clones of one scenario satisfy any count while
      teaching one thing. An empty bank slice returns the zero contract —
      the TIER-3 "no examples where no evidence" rule is unchanged.
      NotesAudit G-12 gates this same bank-derived contract on the shipped
      file, so what NC authors to and what NA enforces cannot drift.
      THE FORMAT CONTRACT (v2.7.0 — owner decisions, 2026-08-15; reading a
      figure is a SEPARATE skill from knowing the theory, and the exam's
      own history decides where it is taught). The target carries
      format_mix (the slice's figure/text question counts) and
      format_by_concept (the same split per concept tag). Three rules:
        FMT-1 BOTH ATTESTED -> BOTH TAUGHT (HARD). format_mix["figure"]
              >= 1 means the unit's own PYQs used figures: author at least
              ONE concept section that PAIRS a rendered figure (F-4 rules
              apply in full) with a worked Example whose SOLUTION READS
              the figure — slope, intercept, area, crossing, region — with
              the distractor autopsy naming the classic misreadings. Text
              practice is demanded by the existing type/spread rules as
              ever. Seven perfect text Examples never substitute for the
              figure skill — the same owner logic as types. G-12 enforces
              the pairing mechanically (a concept block carrying a figure
              content item AND >= 1 Example; the B8 mind map never
              counts).
        FMT-2 FREQUENCY SHAPES EMPHASIS, NEVER EXCLUSION. Per concept,
              read format_by_concept: the LEAD Example — first, deepest —
              follows the concept's DOMINANT format; the minority format
              still gets its guaranteed treatment (its Example, or for a
              figure-minority concept at least the Trap Box line naming
              the known figure trick — misread slope, ignored axis scale).
              NEVER mirror the ratio with counts: 7 text + 3 figure clones
              add pages, not skill — spread-not-count applies to formats
              exactly as it does to concepts. A 100%-figure concept leads
              with the figure treatment and keeps one text Example as
              cheap insurance (formats drift across years).
        FMT-3 NO EVIDENCE, NO DEMAND. format_mix["figure"] == 0 never
              forces a figure — unchanged discipline. An UNRESOLVED image
              in the bank still counts as figure evidence (the student saw
              a figure in the real exam); a quarantined figure question
              still counts (the v3.3.1 rule — the contract reads the
              BANK). Placement of the pairing among the figure-evidenced
              concept tags (listed in G-12's meta) is SME judgement —
              tags are free text and are never name-matched to sections.
  B4  KEY POINTS — exactly one box per concept, placed AFTER that concept's
      example stack, consolidating the concept.
  B4a INTEGRATION SECTIONS (v2.6.0 — where 2-3 subtopics meet in ONE
      question). Structurally an ORDINARY concept section — same block type,
      own example stack (B3 template in full, autopsy + Objective included),
      own KEY POINTS box — so numbering, colours, density and every existing
      gate already police it; nothing new renders and no model field exists.
      What makes it an integration section is its content contract:
        I-1 PLACEMENT — integration sections CLOSE the concept stack: after
            EVERY core concept's KEY POINTS, immediately before B5 TRAP BOX.
            No core concept may follow one (G-13 checks mechanically — the
            mechanical check is "nothing core after integration", so it
            holds identically in a unit that ships no B5: there the section
            still closes the concept stack, immediately before B6).
        I-2 THE COMBINES DECLARATION — the section's FIRST bullet begins
            "Combines:" and names every partner subtopic by its manifest
            display name plus "this sub topic" (e.g. "Combines: Conductors,
            Capacitors and Dielectrics + this sub topic — one question, both
            chapters."). This line is the MECHANICAL MARKER G-13 detects and
            the student's plain-language signpost at once. Partner NAMES are
            ordinary syllabus vocabulary — every §7 ban still applies to
            every word of the section. DUPLICATE NAMES (v2.6.2, NB E-16):
            when two partners in one fusion share a bare display name, the
            target qualifies each as "<Topic> :: <Name>" — the Combines
            line then carries BOTH the topic and the name for each such
            partner (e.g. "Combines: Waves (Mechanics), Waves (Optics) +
            this sub topic"), so student and gate stay unambiguous.
        I-3 BRIDGE BULLETS + EXAMPLES — after the declaration, bridge
            bullets carry the SEAM facts (the partner-side fact and its
            this-side consequence; >= 3 parallel seam facts become a table,
            D-3 as ever), then >= 1 worked Example whose solution genuinely
            crosses the seam — a question needing only this subtopic's
            content belongs in a core concept, not here.
        I-4 BACKWARD-ONLY — partners are always EARLIER subtopics in the
            persisted teaching order (NB §1A A-3 numbering): the student has
            met every ingredient. NC never authors a forward reference to
            material not yet taught. The engine enforces this by
            construction: integration_target_for files every fused question
            at the LATEST member of its fusion set.
        I-5 EVIDENCE-DRIVEN — before drafting, compute
              unit_order = notes_core.unit_order_from_registry(registry)
              itarget    = notes_core.integration_target_for(bank, subject,
                           topic, subtopic, unit_order)
            (v2.6.1: unit_order_from_registry is the ONE builder of the
            order map — NA §2 and G-13 call the SAME function; NC never
            hand-builds the map, exactly as it never re-implements F-1's
            filename). Every attested fusion in itarget gets an integration
            section naming its partners; NotesAudit G-13 gates this SAME
            bank-derived contract on the shipped file, so author and gate
            cannot drift. A unit with no attested fusion NEEDS no
            integration section; an SME-judged bridge section without bank
            attestation is permitted under D-6 (BRIDGE-justified) and is
            listed advisory by G-13, never demanded and never blocked. A
            GRANDFATHERED bank (no integration_partners anywhere — written
            before notes-pyq-bank/1.2) yields a dormant target: author
            nothing, G-13 stays dormant.
        I-6 CAPSTONE BOUND + FIRST-SUBTOPIC EDGE — a topic's LAST subtopic
            may carry the capstone: one integration section spanning as many
            earlier subtopics of that topic as its evidence attests (2.4 in
            the approved demo). Elsewhere, integration sections TYPICALLY
            carry 1-2 partners — but EVIDENCE OUTRANKS THE STYLE BOUND
            (v2.6.2): a fused question files at the LATEST member of its
            fusion set wherever that is, and an attested 3-partner fusion at
            a mid-topic unit gets its 3-partner section THERE — the bound
            shapes SME-judged unattested sections and never overrides a
            G-13 demand (the two would otherwise deadlock). A unit with NO
            earlier subtopic in the persisted order ships NO integration
            section (nothing earlier exists to combine with; the engine
            guarantees no DEMAND can arise there — v2.9's fully-resolved
            filing keeps defective-evidence questions at their header as
            reported, non-demanding unresolved entries).
        I-7 TIER-3 UNITS (v2.6.2) — an attested fusion CAN file at a TIER-3
            unit (a BRIDGE unit late in the teaching order is a natural
            fusion host). The inbound fused questions ARE evidence, so the
            "no examples where no evidence" rule is not violated: the unit
            ships its TIER-3 anatomy PLUS the demanded integration
            section(s) with their example stacks and KEY POINTS — the ONLY
            Examples in such a unit. Placement per I-1 (before B5 when B5
            ships, else before B6). G-12's contract still derives from the
            HEADER slice (empty for a 0-PYQ bridge unit — the zero
            contract), so the integration Examples are demanded by G-13,
            not G-12; the two gates never double-demand.
  B5  TRAP BOX — recurring wrong-option patterns. No year lists, no PYQ
      counts, no evidencing references in print (evidence stays in the bank).
  B6  RAPID REVISION SUMMARY — Must-Know Formulae (OMML in cells, §6 F-3)
      + Key Associations, as level-3 sub-sections.
  B7  RECALL CHECK — exam-format questions IDENTICAL to the B3 template
      minus Explanation, SPEED HACK, the distractor autopsy AND the Objective:
      same box style, titled "Recall j", stem + options (where typed) + bold
      Answer. Types from the allowed set. validate_model and G-5 reject a
      Recall that carries any of those four teaching elements.
  B8  MIND MAP — auto-generated concept graph, last page, obeying §6 F-4.
      SUBTOPIC-ONLY (v2.6.0, owner decision): the graph maps THIS subtopic's
      core concepts only — B4a integration sections and their merged
      concepts NEVER enter the mind map. The map answers "what does this
      subtopic contain", not "what does it connect to"; the Combines
      declaration already carries the connection in words.
THE SPACING RHYTHM (v2.7.2; supersedes v2.7.1's minimal invariant —
GAP-2026-08-15-ADJACENT-TABLES and its owner-reviewed refinement): Word
renders two directly adjacent tables MERGED, and nearly every element
above IS a table (title bar, heading bars, data tables, every coloured
box). The builder therefore inserts EVERY vertical gap itself, in one
deterministic post-assembly pass (notes_docx v1.5 _apply_spacing_rhythm),
sized by context: a LARGER gap before every L1/L2 heading bar (a section
visibly begins), a MEDIUM gap between any two tables, and a SMALL gap
between running text and a table in either direction. The three sizes are
the engine constants SPACER_HEADING_PT / SPACER_TABLE_PT / SPACER_PARA_PT
— the engine is the single authority; this spec deliberately restates no
number. No two tables are ever adjacent, no table ever hugs the text
above or below it, and the old "adjacent boxes are separated" rule is the
box-after-box special case, subsumed. Emitted by the ENGINE, never
authored in the model.
TIER-3 units may ship B1–B2 + B4 + B6–B8 (no examples where no evidence) —
plus, when a fusion files there, the B4a integration section(s) with their
example stacks (§4 B4a I-7: the inbound fused questions ARE the evidence).

## §4A — CONSTRUCTION (the shared builder is the single authority)
NC does not write .docx code. It assembles a CONTENT MODEL (notes_docx schema
"notes-content/1.0") describing WHAT the notes say, then calls
notes_docx.build(model, path). notes_docx.validate_model runs first and HARD
FAILS on a structural or content defect, so the classes below cannot reach a
built file at all:
  - a bullet over the D-1 hard cap;
  - a concept with no KEY POINTS box after its example stack (B4);
  - tail blocks out of section 6A order;
  - an MCQ key outside the printed options, an MSQ key repeating an option, a
    non-numeric NAT key, or a NAT stem that omits its rounding precision;
  - an Example missing its one-line Objective, or whose distractor-autopsy line
    count does not equal the number of wrong options (MCQ 3; MSQ 4 − #correct;
    NAT >= 1 trap value) — the §4 B3 per-option contract; and a Recall that
    carries an autopsy or an Objective;
  - an unbraced multi-character math script. "V_max" is LaTeX for V-subscript-m
    followed by the letters "ax": t3_compile renders it exactly that way, it is
    correct XML, every math gate passes, and it is visibly wrong on a student's
    page. Write "V_{max}".
THE MODEL STORES NO NUMBERS. Outline numbers and the Example/Recall counters
are derived from block ORDER at render time (notes_docx.outline_of), which is
why section 6A's renumber rule cannot be violated by adding or removing a
block. Rule F-7's AUTO line rule is applied by the builder to every paragraph
it emits, so a tall equation or image can never inherit a fixed rule and clip.

## §5 — DENSITY SPEC (machine-gated in NA; constants in notes_core.py,
##      spec-lock-pinned — the constants are the single authority)
  D-1 Bullet length: target <= 20 words; HARD CAP 25. Applies to EVERY
      rendered bullet — concept bullets and the bullets inside KEY POINTS and
      TRAP boxes alike. Enforced at construction by notes_docx.validate_model
      and again at audit by gate G-1.
  D-2 No prose paragraph longer than 2 rendered lines.
  D-3 TABLE-FIRST: >= 3 parallel facts MUST become a table.
  D-4 One concept occupies ~0.5–1.5 pages.
  D-5 Subtopic length ~ concepts x 1.2 pp; typical 6–10 pp; heavy TIER-1 max
      12–15 pp.
  D-6 Every fact must be syllabus-required, PYQ-anchored, or BRIDGE-justified.

## §6 — FORMAT RULES
  F-1 Naming: the draft's filename is EXACTLY
      notes_core.notes_filename(exam_code, s, t, st, slug) — the ENGINE is the
      SINGLE AUTHORITY for this recipe (spec-lock-pinned): pattern
      {EXAM}_S{s}_T{t}_ST{nn}_{Slug}.docx with every non-alphanumeric run in
      {Slug} sanitised to "_". NC derives the filename by CALLING the function,
      never by re-implementing the pattern in prose or code. The numbers are
      the unit's PERSISTED unit_code digits (NB §1A A-3); the slug input is
      notes_core.sid_slug(sid) — already sanitary for Step-5 sids, with the
      sanitiser as the defensive layer since sids are opaque to Notes — so the
      filename traces to the taxonomy.xlsx row. Cross-references inside the
      document use the §6A outline numbers ("see n.3"), never page numbers and
      never retired labels like "Concept 3".
  F-2 Page A4, font Arial, colour strictly per the §6A level colour map.
  F-3 MATHEMATICS (dual standard, both machine-gated in NA):
      (a) EXPRESSIONS (equations, calculations, formula cells) are
          structural OMML — m:f fractions, m:sSup/m:sSub scripts — one
          homogeneous m:oMath per region, per the shared t3_mathcomp
          conventions. FORBIDDEN inside any oMath region: textual exponents
          ("^(") and unicode super/subscript characters.
      (b) SYMBOL MENTIONS in running text — bullets, tables including
          headers, box titles, stems, options, answers — render every
          math token (e.g. Vmax, Km, Ki, Kd, Keq, kcat, kd, Et, v0, S0,
          A0, t-half, k2, k-minus-1, pKa, unit powers, powers of ten) as
          styled sub/superscript runs inheriting the surrounding colour
          and weight. ZERO flat tokens may remain in any text run.
  F-4 DIAGRAMS: auto-generated; the figure's label is rendered INSIDE the
      image at the bottom; no caption paragraphs in the document; all
      symbol text inside figures uses mathtext structural scripts; no exam
      or question-type vocabulary anywhere in figure text.
  F-5 Language: English only, simple exam-coaching register.
  F-6 No version footer or pipeline metadata inside the document. Versions
      are chat-and-registry only.
  F-7 docx line spacing: image and OMML paragraphs MUST NOT inherit a fixed
      line rule (clips tall inline objects). Use auto line rule.

## §6A — OUTLINE NUMBERING AND LEVEL COLOUR MAP
Numbering (decimal cascade, document-wide, no gaps):
  Level 1: "n." on the title (B1). Level 2: "n.k" on every concept section
  and on each fixed block in order after the last concept — TRAP BOX, RAPID
  REVISION SUMMARY, RECALL CHECK, MIND MAP. Level 3: "n.k.m" on sub-sections
  (currently the two RAPID REVISION tables). Removing or adding a block
  renumbers everything after it; stale numbers are an NA gate failure.
Colour map (constants notes_core.LEVEL_COLORS / BOX_COLORS are the SINGLE
AUTHORITY, spec-lock-pinned to the values below; same level == same colour,
adjacent levels distinct):
  L1 title bar navy 1F4E79 | L2 bars teal 00838F | L3 sub-heads purple
  6A1B9A | table headers slate 44546A | Example and Recall boxes blue
  2E75B6 on E8F1FA | KEY POINTS green 2E7D32 on E4F2E4 | TRAP red C62828
  on FBE4E4. No other colour may be introduced for these roles.
  The §4 B3 distractor-autopsy header REUSES the TRAP red C62828 (error
  signalling) and the Objective label REUSES the L2 teal 00838F with the
  objective text in the L1 navy 1F4E79 — all three are existing authorities
  above, so no NEW colour enters the map and the notes_core SPEC-LOCK is
  untouched.

## §7 — CONTENT-STYLE BANS (machine-gated lexicon in notes_core.PROSE_BAN)
The delivered document text (including tables and box titles; figures are
covered by F-4) must contain NONE of the following:
  1. Question-type names (NAT, MCQ, MSQ) or the phrase EXAM LENS.
  2. The token PYQ, example anchors ("modelled on"), or star glyphs.
  3. Year references (19xx/20xx) — evidence years live in the bank/report.
  4. "Q:" stem prefixes.
  5. Editorial/meta lead-in lines ("examiner", fold-away instructions) and
     instructional heading suffixes; headings carry the number + name only.
The §4 B3 distractor-autopsy lines and the Objective line ARE delivered
document text, so they fall under every ban above — in particular a rationale
or objective must never name a question type or cite a year (G-4 scans them
with the rest of the document).
An exam whose OWN subject matter legitimately requires a banned token (e.g.
a History unit needing years) declares a documented per-unit exemption in
the blueprint; absent an exemption the gate is hard.

## §8 — RUNS AND STATE
One subtopic per run. A multi-unit request splits into separate PER-UNIT RUNS,
each a COMPLETE step that ends with its own F2 step-complete footer (§9); the
continue-confirmation sits BETWEEN those runs, not between batches within one run
(NC has no intra-run batching — that F1 batch pattern belongs to NB's ingest, not
here). On completion the unit moves BLUEPRINTED → DRAFTED with notes_version set
(starts 0.1; NA patches bump the minor).

## §9 — DELIVERY / CROSS-CHAT HANDOFF (v2.3.0: the draft is ATTACHED, not filed)
NC runs in its own chat. On completion: present_files the draft (the unit's F-1
filename) AND the updated notes_registry.json (unit -> DRAFTED, carrying
draft_ref per section 9A), then RENDER THE F2 STEP-COMPLETE FOOTER as the LAST
element of the response (Framework_DeliveryFooter section 4-1; the 4-cell NOTES
bar "2 of 4"; header "Step NC · NotesCreate"). The footer is obligatory after a
present_files call (Framework_DeliveryFooter section 4-0 R1) and is never
omitted.

THE TWO ARTIFACTS ARE HANDED OVER DIFFERENTLY, and the footer badges say so:
  - the DRAFT .docx  -> "Use locally". It is NOT uploaded to Project Files.
    The Next callout instructs: start a NEW chat and ATTACH this file to the
    NotesAudit trigger (Framework_NotesAudit section 0A).
  - notes_registry.json -> "Replace in Project Files". NA reads it from there,
    and it is where draft_ref lives.

## §9A — DRAFT PROVENANCE (draft_ref)
After building the draft, NC records
    reg["units"][sid]["draft_ref"] = notes_core.docx_ref_for(draft_path)
({filename, sha256, bytes, generated}) and saves the registry. This is the
ONLY evidence NA has that the document attached to its trigger is the document
NC produced: with a Project-Files handoff the chain was implicit, and with an
attachment there is no chain at all unless it is recorded here. NA section 0B
P-3 compares against it and HARD STOPS on a mismatch. A unit whose draft_ref is
absent (a draft built before v2.3.0) is re-run at NC — cheap, since the bank
and blueprint are untouched.

---

# END OF Framework_NotesCreate v2.7.2
