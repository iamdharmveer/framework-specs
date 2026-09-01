# Framework_NotesCreate v2.9.0 — Notes Pipeline Step NC (Subtopic Notes Drafting)
# v2.9.0 — 2026-09-01 — GAP-2026-09-01-RECALL-CONTRACT (owner decisions of the
#   2026-09-01 design session; notes_core v2.12, notes_docx v1.7, notes_audit v2.9,
#   Framework_NotesAudit v3.7.0 §5 G-14). THE DEFECT: §4 B7 fixed the Recall Check's
#   FORMAT and nothing anywhere defined its CONTENT — how many questions, which
#   concepts, what order, how hard, where the distractors come from. The count was
#   SME judgement here and then FROZEN by NA (§4 there, "FORBIDDEN — changing the
#   NUMBER"). The one section built for the student to self-test was the only
#   section with no contract — the declared-property-without-a-definition class of
#   GAP-2026-08-21-DIFFICULTY-STICKER-LABELS. THE FIX: §4 B7a, a bank-derived
#   contract in the coverage_target_for idiom (third instance after B3a and B4a):
#   notes_core.recall_target_for is the single authority NC authors to and G-14
#   gates, so author and gate cannot drift. SPREAD NOT COUNT (owner, 2026-08-13,
#   applied to Recall): one core Recall per concept section; every attested type;
#   a figure-reading item iff the slice attests figures; cumulative items ONLY
#   from EARLIER subtopics (unit_order — I-4 backward-only by construction); >= 1
#   near-miss discrimination item; >= 1 concept-COMBINING item where the exam or
#   the unit's breadth demands it (R-12); interleaved order; NO clone of a worked
#   Example; distractors from the Trap Box. DIFFICULTY ON THE EXAM'S OWN SCALE
#   (owner O-4): the SAME rubric Step 7 labels mock questions with and PYQExplain
#   profiles real PYQs with (blueprint_core, now routed here through notes_core
#   wrappers), the SAME [ExamCode]_difficulty_profile.json, the SAME
#   author-to-band / verify / re-verify discipline. A missing or partial profile
#   NEVER blocks a unit (owner O-5): the band stands on the nearest rung of a
#   disclosed evidence ladder. WHAT DID NOT CHANGE (owner O-2/O-3): the rendered
#   Recall box is byte-identical — Answer immediately after the options (the IFAS
#   portal hides it), no explanation, no key table, no attempt log, no confidence
#   tick (portal features). The contract lives in UNPRINTED model fields and in
#   the registry unit record (§9A recall_contract). ADDITIVE: every existing unit
#   keeps its Recall Check; G-14 is DORMANT on a registry unit with no record.
# v2.8.0 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3 of the figure-colour
#   programme; notes_core v2.11, notes_audit v2.8, Framework_NotesAudit v3.6.0). F-4
#   figures and the B8 mind map had NO render recipe — no palette, no dpi, no size — so
#   every notes figure was drawn from the model's judgement of the moment. §6 F-4a is the
#   recipe: the SAME constants Step 7 / Step 9 draw with, PINNED in notes_core.FIGURE_PALETTE
#   (a copy locked equal to figural_core by the SPEC-LOCK tripwire and a CI cross-check;
#   figural_core is NOT routed here and its mock gates never run on notes). What does NOT
#   transfer from the mock flow is stated in F-4a: notes TEACH, so colour-as-content is
#   ALLOWED, in-image labels stay REQUIRED (F-4), and no answer-leak rule applies. Additive:
#   every existing notes unit keeps its figures; only units drafted from v2.8.0 use F-4a.
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
# [ExamCode] project | Notes Step NC | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_docx.py >= v1.7 — the SHARED builder. NC constructs the .docx ONLY
#                           through notes_docx.build (section 4A); it never
#                           hand-rolls a paragraph, colour, border or line rule.
#                           v1.7 accepts the UNPRINTED recall-contract fields on
#                           Recall blocks (schema notes-content/1.1) and
#                           validate_model enforces §4 B7a at construction;
#                           v1.5 carries the full SPACING RHYTHM (§4 tail —
#                           context-sized gaps, one post-assembly pass);
#                           v1.3 adds the why_wrong / objective fields (§4 B3)
#                           and validate_model's per-option-count enforcement
#   notes_core.py >= v2.12 — THE RECALL CONTRACT (§4 B7a): recall_target_for,
#                           recall_cumulative_min, recall_expected_band,
#                           recall_verify_difficulty, recall_authoring_profile,
#                           difficulty_profile_load, recall_exam_mix_check,
#                           scenario_key / is_clone, normalize_complexity and
#                           the spec-lock-pinned RECALL_* constants (v2.12);
#                           format_mix + format_by_concept in
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
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_NotesCreate.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

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
2a. (v2.9.0) THE DIFFICULTY PROFILE. NC also reads
   [ExamCode]_difficulty_profile.json from project Files WHEN PRESENT, through
   notes_core.difficulty_profile_load(path, exam_code) — the SAME file the mock
   flow's TestCreate/MockBlueprint read (Framework_Blueprint §7), never a Notes
   copy of it. The loader NEVER raises: absence, a foreign exam code, a
   malformed file or a rejected schema each return (None, reason), the reason
   is carried into the §9 chat line, and the unit proceeds on the lower rungs of
   the §4 B7a difficulty ladder. The profile is never required (owner O-5).
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
      Answer IMMEDIATELY after the options. Types from the allowed set.
      validate_model and G-5 reject a Recall that carries any of those four
      teaching elements. THE RENDERED BOX IS UNCHANGED BY v2.9.0 (owner
      decisions O-2/O-3, 2026-09-01): the Answer stays directly under the
      options because the IFAS portal hides it in its own element until the
      student commits; no answer-key table, no attempt log, no re-attempt
      schedule and no confidence tick are ever printed — the portal owns those.
      Everything B7a adds is UNPRINTED (model fields + registry).
  B7a RECALL CONTRACT (v2.9.0 — GAP-2026-09-01-RECALL-CONTRACT; what "the
      right Recall Check" MEANS, so the student self-tests every concept at
      the exam's own difficulty before the next subtopic). Before drafting
      any Recall, compute the unit's contract:
        unit_order = notes_core.unit_order_from_registry(registry)
        profile, why = notes_core.difficulty_profile_load(
                           "/mnt/project/<EXAM>_difficulty_profile.json", exam_code)
        rtarget    = notes_core.recall_target_for(bank, subject, topic,
                         subtopic, unit_order, allowed_types,
                         profile=profile, subtopic_id=sid)
      and author to it. The ENGINE is the single authority for every number
      in this contract (the RECALL_* constants, spec-lock-pinned); this spec
      restates none. NotesAudit G-14 derives the SAME target from the same
      inputs and gates the shipped file, so author and gate cannot drift.
        R-1 COVERAGE — exactly rtarget["core_per_concept"] core Recall per
            concept section, integration sections (B4a) included. Never a
            second Recall on a scenario an existing one already tests: SPREAD,
            NOT COUNT (owner decision 2026-08-13) applies to Recall exactly as
            to Examples — N clones satisfy any count while testing one thing.
        R-2 TYPES — every type in rtarget["required_types"] appears at least
            once across the set (format-matching to the real exam; a
            single-type exam yields a single-type set). Type names are never
            printed (§7 ban 1).
        R-3 FIGURE — when rtarget["requires_figure_item"], at least one Recall
            READS a figure already rendered in a concept section (Recall boxes
            carry no images): its stem refers to that section's figure by
            outline number ("the graph in n.k") and the item declares
            reads_figure = "n.k". Reading a figure is a separate skill from
            knowing the theory (FMT-1 logic, extended to self-test).
        R-4 CUMULATIVE — items drawn ONLY from rtarget["cumulative_partners"]:
            the EARLIER subtopics of the SAME Section (subject) in the persisted
            teaching order (unit_order, the ONE order map; I-4 backward-only by
            construction — a Physics unit never revises Chemistry). Their count
            is notes_core.recall_cumulative_min(core_count, rtarget). A unit
            with no earlier subtopic ships none (nothing earlier exists);
            an order-less target (order_known False) makes the cumulative rule
            dormant and reported, never a demand. Partner vocabulary is
            ordinary syllabus vocabulary; every §7 ban applies to every word.
        R-5 NEAR-MISS — at least rtarget["near_miss_min"] item(s) is a
            DISCRIMINATION item: superficially similar to a core concept,
            solved by a different method (a cumulative item may be the one).
            This is the item the interleaving evidence is strongest for and
            it is never optional.
        R-6 CEILING — the whole set stays within rtarget["ceiling"]; when the
            concept count alone makes that unattainable, recall_cumulative_min
            holds the cumulative items at their floor and the overshoot is
            REPORTED, never silently trimmed.
        R-7 NO CLONES — a Recall never reuses a worked Example's scenario. It
            changes at least TWO of: context, direction (forward <-> inverse),
            given/asked quantities, representation (text <-> figure <-> table).
            Mechanical proxy: notes_core.is_clone(notes_core.scenario_key(
            recall stem), scenario_key(example stem)) must be False for every
            Example in the unit — fresh numbers alone never pass (numbers are
            dropped from the key). At least one Recall per concept keeps the
            exam's exact format for that concept (format-congruence).
        R-8 INTERLEAVED ORDER — no two consecutive Recalls share an identity
            (core: the same concept_ref; cumulative: the same partner); cumulative
            items are dispersed through the sequence, never grouped at the end.
        R-9 DISTRACTORS FROM THE TRAP BOX — every wrong option of a core
            Recall is one of the unit's documented recurring error patterns
            (B5); the item declares trap_refs (0-based B5 bullet indexes).
            Arbitrary distractors are not permitted. Provenance is free-text
            and therefore ADVISORY at G-14, never a block.
        R-10 DIFFICULTY ON THE EXAM'S OWN SCALE (owner O-4) — the mock flow's
            three-step guarantee, applied to Recall:
            (1) TARGET. Each Recall declares the concept_tags (bank tags) it
                tests, its scope and (cumulative) its partner, and whether it
                is the near-miss; its band is
                  band, basis = notes_core.recall_expected_band(rtarget, tags,
                                    is_near_miss, qtype, scope=scope,
                                    partner=partner)
                — the ONE resolver, which walks the EVIDENCE LADDER and names
                the rung it stood on (basis, one of notes_core.RECALL_BASES):
                  concept   CORE items: the harder modal `complexity` among the
                            declared tags, each tag counting only with enough
                            PYQs
                  partner   CUMULATIVE items: the PARTNER subtopic's own bank
                            complexity mode — a revision item tests the
                            partner's concept, so the partner's evidence
                            decides; this unit's concept and subtopic rungs are
                            evidence about THIS unit and never decide it
                  subtopic  CORE items: the exam's own rubric-measured mix for
                            THIS sid over the profile's DEFAULT cycle window
                            (blueprint_core.DP_CYCLES_WINDOW sittings — the mock
                            flow's default; the Notes route carries no
                            exam_config, so a per-exam cycle gap is not read)
                  topic     the bank's complexity mode over the whole parent
                            topic (both scopes)
                  exam      the profile's paper-level mix over the same window
                            (both scopes)
                  neutral   the middle label, when no evidence exists anywhere
                A near-miss item is ONE band above its base. MSQ/NAT never sit
                in the bottom band (the shared rubric's qtype floor). The
                basis of EVERY item is reported in the §9 chat line, so a
                fallback is disclosed, never silent (owner O-5).
            (2) DEFINITION. The Recall is authored to
                  notes_core.recall_authoring_profile(band, qtype, labels)
                — the observation targets that make the SHARED rubric
                (blueprint_core.assess_difficulty, the definition of a label
                on every pipeline) land in the band — and its derivation is
                recorded as difficulty_obs (question_class, deduction_steps,
                axiom_concepts, speed_hack_exists, is_negative, qtype), the
                Step-7 CHECK 3c shape.
            (3) ACCEPT/REJECT. notes_core.recall_verify_difficulty(band, obs,
                labels) must agree — up to six re-authorings, then that ONE
                item HARD STOPS the run with the measured band named; a label
                the evidence contradicts never ships and is never silently
                relabelled. NA G-14 re-runs the identical check on the shipped
                set. DRIFT-TO-EASY is the failure this closes: a stem that
                announces the method the real question made the student
                recognise scores below its band and is rewritten.
            EXAM-WIDE MIX — when the profile is present, the whole set's band
            counts are checked against the exam's measured paper-level mix by
            notes_core.recall_exam_mix_check(bands, rtarget) (largest
            remainder, ± the engine tolerance per band). Absent a profile the
            check is dormant and disclosed.
        R-11 FALLBACK IS DISCLOSED, NEVER SILENT (owner O-5). Profile absent
            -> per-item bands still resolve from the bank rungs; the exam-wide
            check is dormant; the §9 line says so. A concept with too few
            PYQs, or none (a D-6 syllabus/BRIDGE concept), resolves on the
            subtopic/topic/exam/neutral rungs with its basis named. A TIER-3
            unit (no PYQs) still ships B7 (it is in the B6–B8 set TIER-3
            keeps; only worked Examples need PYQ evidence): its bands resolve
            on the lower rungs and every basis is named.
        R-12 MULTI-CONCEPT (owner question, 2026-09-01: real exam questions
            apply two or three concepts at once). When
            notes_core.recall_multi_concept_required(rtarget, concept_count)
            is True — the unit's own PYQs include a top-band question (on the
            shared rubric a top-band item IS a multi-concept derivation), OR the
            document teaches two or more concept sections — at least ONE Recall
            combines concepts (a core item combines concepts of this unit; a
            cumulative item may combine a partner concept with one of this
            unit): its recorded derivation carries
            axiom_concepts >= the engine minimum, and
            notes_core.recall_is_multi_concept(item, rtarget) reads that SAME
            rubric-verified observation, so author, builder and gate agree by
            construction. A single-concept subtopic with no top-band evidence
            demands nothing (no evidence, no demand). The near-miss item (R-5)
            and an integration section's Recall (B4a) are natural carriers, but
            any Recall may be the one.
      THE MODEL FIELDS (unprinted; notes_docx schema notes-content/1.1; the
      rendered box is byte-identical to notes-content/1.0): on every Recall
      block — scope ("core" | "cumulative"), concept_ref (core: the outline
      number "n.k" of the concept section it tests), partner (cumulative: the
      partner subtopic's manifest scope), concept_tags, is_near_miss,
      reads_figure ("n.k" or null), trap_refs, difficulty_band,
      difficulty_basis, difficulty_obs, anchor_bank_id (the PYQ whose
      structure it mirrors; §3 bank-and-registry-only like every anchor).
      notes_docx.validate_model enforces R-1, R-6, R-7, R-8, R-12 (its
      section-count trigger; the bank trigger is G-14's) and the field
      shape at construction whenever ANY Recall block carries the fields; a
      model with none (pre-v2.9.0) validates exactly as before.
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
"notes-content/1.1" from v2.9.0; "notes-content/1.0" models are still
accepted and validate exactly as before) describing WHAT the notes say, then calls
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
  - (v2.9.0, only when the model carries §4 B7a fields) a concept section with
    no core Recall; two consecutive Recalls of one identity; a Recall whose
    scenario clones a worked Example (notes_core.is_clone); a Recall set over
    the engine ceiling where the ceiling is attainable; a unit with two or more
    concept sections and no concept-combining Recall (R-12); a Recall with an
    unknown scope, a concept_ref that is not a concept outline number, a
    missing difficulty_band or an empty difficulty_obs;
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
  F-4a FIGURE RENDER CONTRACT (v2.8.0 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT).
      Every F-4 diagram and the B8 mind map is rendered by the session with
      matplotlib (structures: notes_core.figure_structure_png) to THIS recipe:
      (1) notes_core.FIGURE_DPI (300) at the display width, opaque white
          background, PNG; identical inputs give identical bytes (NA §8).
      (2) COLOUR comes ONLY from notes_core.FIGURE_PALETTE — the same values
          Step 7 (figural_core) and Step 9 (explain_engine) draw with, pinned
          here so the Notes route never loads figural_core: series and accent
          ink from FIGURE_PALETTE['line_ink'] (four Okabe-Ito hues + black,
          at most 'series_cap' = 4 chromatic series, each with its own
          'linestyles'/'markers' entry — colour is never the only channel);
          every coloured LABEL through notes_core.figure_text_ink(hue) (the
          4.5:1 TEXT tier — F-4 labels are text); every FILL through
          notes_core.figure_fill_style(k) (fill hue, dark edge always, hatch k
          as the greyscale channel); continuous data on 'colormap' (viridis)
          only. Never a matplotlib or rdkit default colour.
      (3) STRUCTURES: notes_core.figure_structure_png(smiles, path, width_in,
          highlight_bonds=, highlight_atoms=) — the pinned atom palette (O
          #C25604, N #0072B2, halogens #158663, all else black), the concept's
          decisive site highlighted; it returns the canonical SMILES, which the
          session compares with the intended canonical form before the image
          is placed (a mismatch drops the figure and is recorded). rdkit absent
          -> ValueError('rdkit_unavailable'): the figure is omitted and noted,
          never drawn by hand and never with a default palette.
      (4) MIND MAP (B8): node fills by level through figure_fill_style(
          notes_core.MINDMAP_LEVEL_FILLS[level]) — L1 sky, L2 orange, L3
          yellow — black labels (>= 9:1 on every fill), edges black.
      (5) WHAT DOES NOT TRANSFER FROM THE MOCK FLOW: notes TEACH. Colour that IS
          the content (the colour of a complex, an indicator, a flame) is
          SHOWN; labels inside the image stay REQUIRED (F-4); there are no
          options, so no uniformity or leak rule applies; and figural_core's
          gates never run on a notes figure. Palette conformance is reported
          by NA only as an ADVISORY (G-7a meta) — never a defect of a shipped
          unit, never a re-render trigger (NA §1).
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

## §9A — DRAFT PROVENANCE (draft_ref) AND THE RECALL RECORD (recall_contract)
After building the draft, NC records
    reg["units"][sid]["draft_ref"] = notes_core.docx_ref_for(draft_path)
({filename, sha256, bytes, generated}) and saves the registry. This is the
ONLY evidence NA has that the document attached to its trigger is the document
NC produced: with a Project-Files handoff the chain was implicit, and with an
attachment there is no chain at all unless it is recorded here. NA section 0B
P-3 compares against it and HARD STOPS on a mismatch.
v2.9.0: NC ALSO records
    reg["units"][sid]["recall_contract"] = {"items": [ ... ],
                                             "profile": {"present": bool, "reason": why},
                                             "exam_mix_expected": ...}
where items is the §4 B7a field set of every Recall block in DOCUMENT ORDER
(j = 1-based position; concept_ref, scope, partner, concept_tags,
is_near_miss, reads_figure, trap_refs, difficulty_band, difficulty_basis,
difficulty_obs, anchor_bank_id). The DOCUMENT never carries these (§7 / F-6),
so the registry is the ONLY place NA G-14 can read the author's declarations
— exactly as draft_ref is the only chain to the attachment. A unit whose
record is absent (a draft built before v2.9.0) leaves G-14 DORMANT (reported)
until the unit is re-drafted here. A unit whose draft_ref is
absent (a draft built before v2.3.0) is re-run at NC — cheap, since the bank
and blueprint are untouched.

---

# END OF Framework_NotesCreate v2.9.0
