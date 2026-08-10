# Framework_NotesCreate v2.2.0 — Notes Pipeline Step NC (Subtopic Notes Drafting)
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
#   notes_core.py >= v2.0 — resolve_unit (operator-input resolution), sid_slug,
#                           verify_taxonomy_ref (manifest staleness check),
#                           sid-keyed registry (notes-registry/2.0); plus
#                           LEVEL_COLORS / BOX_COLORS constants, PROSE_BAN
#                           lexicon, math gates, registry transitions, the bank
#                           readers (bank_load / bank_questions_for) and
#                           verify_bank_ref (blueprint/bank staleness check)
#
# PURPOSE:
#   Produce ONE subtopic's study-notes .docx (draft) from the blueprint unit
#   record plus that subtopic's PYQ evidence, such that Step NA can verify
#   every in-scope PYQ is solvable from the notes text alone.
#
# PIPELINE POSITION:
#   Notes Step NB (NotesBlueprint) → unit table + sources + allowed types
#   Notes Step NC (NotesCreate)    → THIS SPEC (1 unit per run; §8 runs)
#   Notes Step NA (NotesAudit)     → audit + convergence loop
#   Notes Step ND (NotesDeliver)   → delivery
#
# PREREQUISITE:
#   notes_blueprint.json + notes_registry.json exist; target unit is in state
#   BLUEPRINTED (or STALE, or returned by NA for full regeneration). The
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
   of §4 B4/B7) is SME-generated by Claude and earns trust ONLY via Step NA.
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
        SPEED HACK    last, ONLY where a genuine shortcut exists
      Question types MUST be drawn exclusively from
      allowed_question_types; across the unit the examples collectively
      cover every allowed type where the concept evidence supports it. A
      single-type exam yields single-type examples. Theory-style prompts
      (no options, no numeric target) are forbidden. Type names are never
      printed — the format itself communicates the type.
  B4  KEY POINTS — exactly one box per concept, placed AFTER that concept's
      example stack, consolidating the concept.
  B5  TRAP BOX — recurring wrong-option patterns. No year lists, no PYQ
      counts, no evidencing references in print (evidence stays in the bank).
  B6  RAPID REVISION SUMMARY — Must-Know Formulae (OMML in cells, §6 F-3)
      + Key Associations, as level-3 sub-sections.
  B7  RECALL CHECK — exam-format questions IDENTICAL to the B3 template
      minus Explanation and SPEED HACK: same box style, titled "Recall j",
      stem + options (where typed) + bold Answer. Types from the allowed set.
  B8  MIND MAP — auto-generated concept graph, last page, obeying §6 F-4.
Adjacent boxes are always separated by a spacer paragraph so consecutive
box tables never merge visually.
TIER-3 units may ship B1–B2 + B4 + B6–B8 (no examples where no evidence).

## §5 — DENSITY SPEC (machine-gated in NA; constants in notes_core.py)
  D-1 Bullet length: target <= 20 words; HARD CAP 25.
  D-2 No prose paragraph longer than 2 rendered lines.
  D-3 TABLE-FIRST: >= 3 parallel facts MUST become a table.
  D-4 One concept occupies ~0.5–1.5 pages.
  D-5 Subtopic length ~ concepts x 1.2 pp; typical 6–10 pp; heavy TIER-1 max
      12–15 pp.
  D-6 Every fact must be syllabus-required, PYQ-anchored, or BRIDGE-justified.

## §6 — FORMAT RULES
  F-1 Naming: {EXAM}_S{s}_T{t}_ST{nn}_{Slug}.docx — the numbers are the
      unit's PERSISTED unit_code digits (NB §1A A-3) and {Slug} is
      notes_core.sid_slug(sid), so the filename traces to the taxonomy.xlsx
      row. Cross-references inside the document use the §6A outline numbers
      ("see n.3"), never page numbers and never retired labels like
      "Concept 3".
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
Colour map (constants notes_core.LEVEL_COLORS / BOX_COLORS; same level ==
same colour, adjacent levels distinct):
  L1 title bar navy 1F4E79 | L2 bars teal 00838F | L3 sub-heads purple
  6A1B9A | table headers slate 44546A | Example and Recall boxes blue
  2E75B6 on E8F1FA | KEY POINTS green 2E7D32 on E4F2E4 | TRAP red C62828
  on FBE4E4. No other colour may be introduced for these roles.

## §7 — CONTENT-STYLE BANS (machine-gated lexicon in notes_core.PROSE_BAN)
The delivered document text (including tables and box titles; figures are
covered by F-4) must contain NONE of the following:
  1. Question-type names (NAT, MCQ, MSQ) or the phrase EXAM LENS.
  2. The token PYQ, example anchors ("modelled on"), or star glyphs.
  3. Year references (19xx/20xx) — evidence years live in the bank/report.
  4. "Q:" stem prefixes.
  5. Editorial/meta lead-in lines ("examiner", fold-away instructions) and
     instructional heading suffixes; headings carry the number + name only.
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

## §9 — DELIVERY / CROSS-CHAT HANDOFF
NC runs in its own chat, so its draft must reach NA (a fresh chat) the same way
NB's bank reaches NC. On completion: present_files the draft
[ExamCode]_<unit>.docx AND the updated notes_registry.json (unit → DRAFTED), then
RENDER THE F2 STEP-COMPLETE FOOTER as the LAST element of the response
(Framework_DeliveryFooter §4-1; the 4-cell NOTES bar "2 of 4"; header "Step NC ·
NotesCreate"). The footer's badges upload both artifacts to Project Files and its
Next callout points to NA: NotesAudit in a NEW chat (which reads the draft + bank
from Project Files). The footer is obligatory after a present_files call
(Framework_DeliveryFooter §4-0 R1) and is never omitted.

---

# END OF Framework_NotesCreate v2.2.0
