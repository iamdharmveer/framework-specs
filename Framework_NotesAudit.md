# Framework_NotesAudit v3.6.0 — Notes Pipeline Step NA (Closed-Book Audit + Remediation)
# v3.6.0 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3; notes_audit v2.8,
#   notes_core v2.11, Framework_NotesCreate v2.8.0 §6 F-4a). §1's v3.0.0 re-render clause
#   named figural_core, which is NOT routed to NA — the clause was non-executable. It now
#   names the F-4a recipe (notes_core), and states the one rule that protects §8's
#   idempotence: COLOUR NON-CONFORMANCE IS NEVER A RE-RENDER TRIGGER. G-7a carries a
#   figure-palette ADVISORY in meta (notes_audit.figure_palette_meta) — information for the
#   next draft, never a finding, never ok=False. Additive; an AUDITED_PASS unit re-run after
#   v3.6.0 still yields zero corrections and identical bytes.
# v3.5.0 — 2026-08-15 — G-12 FORMAT CONTRACT (figure vs text balance; owner
#   decisions of the 2026-08-15 design session, approved proposal; pairs
#   with Framework_NotesCreate v2.7.0 §4 B3a; notes_core >= v2.10,
#   notes_audit >= v2.7). §5 G-12 extended — deliberately NO new gate id
#   (format coverage IS coverage; the same reasoning that folded the
#   distractor-autopsy rules into G-5, keeping notes_audit.GATES and this
#   spec in one-to-one agreement). HARD: figure evidence in the unit's
#   slice (format_mix, notes_core v2.10) -> at least one concept section
#   pairs a rendered figure with a worked Example, detected purely from
#   block order — no new model field, no builder change, W-3 and §0B P-4
#   untouched; the B8 mind map never satisfies it. ADVISORY:
#   figure_concept_tags (where the evidence sits, for §2A placement
#   judgement) and figure_example_pairs. Lead-format emphasis (FMT-2) is
#   §2A authoring judgement, never a block. Quarantined and
#   UNRESOLVED-image figure questions still count (v3.3.1 discipline).
#   Remediation: the standing §2A net-ADD licence on a G-12 hard finding —
#   NA adds the figure and the Example that reads it. Rollout follows the
#   G-12 precedent: applies at each unit's next audit; a target without
#   format_mix skips the check (additive, never retroactive).
# [ExamCode] project | Notes Step NA | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py  >= v2.10 — format_mix + format_by_concept in
#                            coverage_target_for (§5 G-12's format
#                            contract, v2.10); plus (v2.9)
#                            fully-resolved filing, unresolved reporting,
#                            display_norm (G-13's name matching), duplicate-
#                            name qualification (all v2.9); plus
#                            audit_questions_for (§2's certification set) +
#                            unit_order_from_registry (the ONE order-map
#                            builder), both v2.8; plus
#                            notes_final_filename, docx_ref_for/verify_docx_ref,
#                            registry schema notes-registry/2.1 (draft_ref,
#                            final_ref, audit_summary), resolve_unit, the
#                            density/math/prose gates, bank_questions_for,
#                            document_text (the ONLY document text extractor),
#                            coverage_target_for + COVERAGE_CONCEPT_CEILING
#                            (§5 G-12's bank-derived contract, v2.6), and
#                            integration_target_for (§5 G-13's bank-derived
#                            contract, v2.7 — latest-partner filing;
#                            grandfathered-dormant for pre-1.2 banks)
#   notes_docx.py  >= v1.3 — the SHARED builder/parser: build/parse/
#                            validate_model/outline_of. Derived numbering and
#                            the STRICT byte-identical round trip are its
#                            guarantees; parse takes exam_code/tier (W-4). v1.3
#                            adds the why_wrong/objective fields (§4 B3) that
#                            parse recovers and the round trip preserves
#   notes_audit.py >= v2.7 — G-12 format-contract enforcement (the
#                            figure+Example pairing, v2.7); plus (v2.6)
#                            display_norm Combines matching + unresolved
#                            advisory in gate_integration (v2.6); plus
#                            SOLVABLE_KEY_CORRECTED, classify_key_conflict,
#                            record_key_correction, quarantine, gate_line_rules,
#                            gate_answer_integrity, gate_counters,
#                            gate_orphan_terms, syllabus_terms_for,
#                            gate_anatomy, gate_question_format, gate_outline,
#                            gate_coverage (§5 G-12, v2.4), gate_integration
#                            (§5 G-13, v2.5), terminal_regate, audit_summary
#
# PURPOSE:
#   Guarantee that the delivered document teaches every in-syllabus PYQ of one
#   subtopic well enough to solve it from the notes alone — and, where it does
#   not, MAKE it do so. NA is the ONLY quality gate in the Notes pipeline; no
#   human review exists anywhere in it.
#
# PIPELINE POSITION:
#   Notes Step NB (NotesBlueprint) -> notes_pyq_bank.json (the PYQ bank)
#   Notes Step NC (NotesCreate)    -> the unit's draft .docx + draft_ref
#   Notes Step NA (NotesAudit)     -> THIS SPEC -> the unit's _Final.docx
#   Notes Step ND (NotesDeliver)   -> portal formatting + delivery
#
# PREREQUISITE:
#   Unit state DRAFTED. The draft .docx is ATTACHED TO THE TRIGGER MESSAGE.
#   notes_pyq_bank.json, notes_blueprint.json and notes_registry.json are in
#   Project Files.
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_NotesAudit.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

## §0 — TRIGGER AND UNIT RESOLUTION
The trigger is:

    NotesAudit <Subject :: Topic :: Sub Topic Name>

with the unit's draft .docx ATTACHED to the same message. The unit reference is
whatever cell the operator copied from [ExamCode]_taxonomy.xlsx, resolved by
notes_core.resolve_unit exactly as in Framework_NotesCreate section 0 — all
three tiers remain accepted (Sub Topic Id, the Subject::Topic::Sub Topic Name
scope above as the CANONICAL form, or the bare Sub Topic Name). A unique hit
proceeds; multiple bare-name hits STOP and list every candidate with its
Subject + Topic; zero hits STOP with nearest-name suggestions. NA never
fuzzy-picks. The resolved unit is confirmed in chat as
<Sub Topic Name> (<sid>).

## §0A — INPUTS
  ATTACHED to the trigger : the unit's draft .docx (NC's F-1 filename).
                            EXACTLY ONE .docx. Zero attachments STOPS; more
                            than one STOPS and lists them — NA never picks.
  PROJECT FILES           : notes_pyq_bank.json, notes_blueprint.json,
                            notes_registry.json, and (when present)
                            [ExamCode]_subtopic_manifest.json.
The attachment is READ-ONLY on disk. NA copies it to a working directory
before doing anything else; it never edits the uploaded file in place, and it
writes its output to the outputs directory.

## §0B — PREFLIGHT (three HARD STOPS, run before any solving)
Until v3.0.0 NA read its input from Project Files, where NC had put it. An
attachment carries no such chain, so the chain is CHECKED. Each stop names a
different defect with a different remedy, so they are reported separately —
notes_core.verify_docx_ref returns the kind.

  P-1 FILENAME IDENTITY. Recompute the unit's draft filename with
      notes_core.notes_filename(...) from the RESOLVED unit's persisted
      unit_code digits and sid_slug. If the attached file's name differs, STOP:
      "the wrong unit's document is attached". This is the likeliest operator
      error — triggering ST06 while attaching ST07 — and it is the one error
      that would otherwise produce a perfectly clean audit of the wrong notes.
  P-2 EXAM-CODE CROSS-CHECK. The trigger's scope form carries NO exam code, so
      the {EXAM} prefix of the attached filename is the only place it appears.
      It MUST equal the registry's exam_code. A mismatch STOPS.
  P-3 BYTE IDENTITY. Compare notes_core.file_sha256 of the attachment against
      the registry unit's draft_ref (written by NC, Framework_NotesCreate
      section 9A). A mismatch means the file was modified after NC wrote it; a
      missing draft_ref means the draft predates NotesCreate v2.3.0. Both
      STOP. An operator who deliberately hand-edited the draft re-issues the
      trigger with the token --accept-modified, which downgrades P-3 to a
      warning recorded in audit_summary; P-1 and P-2 are NEVER overridable.
  P-4 PARSE FIDELITY (run immediately after P-3, before any solving).
      P-4a  notes_docx.validate_model(parse(draft, exam_code=..., tier=...))
            MUST pass. A failure means the parser did not recover something
            the builder wrote. HARD STOP, naming every finding. Do not
            proceed, do not work around it with strict=False, and do not
            hand-repair the model: a parser that loses content on this
            document loses it on every document of the same shape, and the
            defect belongs in the engine, not in one run's workaround.
      P-4b  build(parse(draft)) SHOULD reproduce the draft's
            word/document.xml byte-for-byte. A difference is REPORTED as a
            diagnostic, never a stop — a legitimate builder upgrade between
            NC and NA changes bytes without losing content.
      The asymmetry is deliberate: P-4a stops, P-4b reports. Validity is
      guaranteed across engine versions; byte-identity is not.

  The v2.0.x staleness stops are unchanged and still run: verify_bank_ref
  against the blueprint's bank_ref, and verify_taxonomy_ref against
  [ExamCode]_subtopic_manifest.json when present. Either mismatch routes the
  unit back to NB.

## §1 — FIGURES (read from the bank; no re-extraction)
Unchanged from v2.0.0 for the SOLVE. NB extracted every image and split stem
figures from solution figures at the "Correct Answer:" line, so NA reads
solve-critical images with notes_audit.figures_for (stem figures only —
solution figures are part of the key, not the prompt) and views them with the
stem. A stem figure recorded "UNRESOLVED:..." parks that question in
report['figure_pending']; it never hard-stops the run.

NEW in v3.0.0 (amended v3.6.0): NA MAY RE-RENDER a figure it judges improvable
for a LAYOUT or CONTENT reason (G-7a illegibility, G-7b geometry, a wrong
label), rendering it to the NotesCreate §6 F-4a recipe with notes_core
(figure_text_ink / figure_fill_style / figure_structure_png; figural_core is
NOT routed here and is never imported), subject to three conditions that keep
section 8's idempotence real. COLOUR ALONE IS NEVER A REASON: a figure whose
only departure from F-4a is its palette (every unit drafted before v2.8.0) is
LEFT AS IT IS — re-rendering it would change every hash the section-8 ledger
records for it. G-7a reports palette conformance as an ADVISORY in meta
(notes_audit.figure_palette_meta), for the next NotesCreate draft to act on.
  (a) the render must be DETERMINISTIC (fixed rcParams and DPI, no timestamp
      in the image metadata) — identical inputs must produce identical bytes;
  (b) each re-rendered figure's hash is recorded in audit_summary, and a
      figure already re-rendered by NA is NEVER re-judged on a later run;
  (c) every re-render re-passes F-4 (label drawn INSIDE the image, mathtext
      structural scripts, no exam or question-type vocabulary) and G-7a/G-7b.
notes_docx writes positional picture names, so a re-render to a different
temporary path does not churn document.xml.

## §2 — CLOSED-BOOK SOLVE PROTOCOL (ground-truth)
For each bank question, in order:
  P-1 Extract the tested concept(s).
  P-2 PRESENCE: locate where the notes teach each concept (block reference).
  P-3 SOLVE using ONLY the notes text plus the section 1 stem figures — no
      outside knowledge beyond the Level-assumed prerequisites declared in the
      blueprint.
  P-4 MATCH against the bank's verbatim correct_answer via
      notes_audit.verdict_against_key: MCQ option token; MSQ unordered set;
      NAT equal after rounding BOTH sides to the stem's stated precision.
  P-5 VERDICT: SOLVABLE | SOLVABLE_KEY_CORRECTED (section 3A) | PARTIAL (the
      notes teach the concept but the notes-derived answer misses the key) |
      NOT (the notes do not teach the concept). The notes location and the
      produced answer are recorded (notes_audit.record).

COVERAGE + PASS: NA audits EVERY question in the unit's CERTIFICATION SET —
  unit_order     = notes_core.unit_order_from_registry(registry)
  unit_questions = notes_core.audit_questions_for(bank, subject, topic,
                                                  subtopic, unit_order)
— and certifies ONLY through notes_audit.pass_for_unit(report,
unit_questions), which derives expected_count from that set. A run that
recorded fewer verdicts than the set holds can never certify.

THE CERTIFICATION SET FOLLOWS FILING (v3.4.1). audit_questions_for is the
header slice adjusted by latest-partner filing — the SAME shared authority
G-13's target uses, so where a fusion is taught and where it is solved can
never disagree:
  DEFERRED — a fused question in this unit's header slice whose filing home
    is a LATER partner is EXCLUDED here: its ingredients live in material
    this unit's notes must not teach (Framework_NotesCreate §4 B4a I-4), so
    this unit can never make it solvable and is never punished for that.
    Each deferral is DISCLOSED in the §9 chat line with its filing unit,
    where it WILL be solved. FILING MOVES ONLY ON FULLY-RESOLVED EVIDENCE
    (v3.4.2, notes_core v2.9): a question defers only when EVERY member of
    its fusion set — header included — is a registry unit in unit_order;
    a fused question with an unresolvable member (typo'd or out-of-registry
    partner, or an out-of-syllabus header) STAYS at its header, is audited
    there like any other question, and is reported as unresolved evidence
    (G-13 advisory / §9). ORPHANED-FILING CHECK (v3.4.2): when
    [ExamCode]_subtopic_manifest.json is present (§0A), NA cross-checks
    each deferred question's filing unit against the manifest; a filing
    unit whose sid has LEFT the manifest (NB §7 ORPHANED) is disclosed as
    ORPHANED-FILING — that PYQ's certification is PENDING the owner's
    orphan resolution (re-run Step 5 / NB), and the disclosure repeats on
    every run until it clears; the question is never silently dropped from
    the exam's coverage.
  INBOUND — a fused question from an EARLIER unit's header slice whose
    filing home is THIS unit is INCLUDED here and solved closed-book from
    THIS unit's notes: the integration section's bridge bullets carry the
    partner-side facts (NC §4 B4a I-3), so the notes alone suffice — that
    is precisely what the section exists to guarantee. A PARTIAL/NOT on an
    inbound question routes to the integration section (§5 G-13
    remediation), like any other targeted correction.
  For a GRANDFATHERED bank (or any order-less caller) the set IS the header
  slice — identical to pre-v3.4.1 behaviour; nothing changes for existing
  exams. The COVERAGE CONTRACT (§5 G-12 / coverage_target_for) DELIBERATELY
  still reads the header slice: the contract reads the BANK's evidence and
  never shrinks or grows because filing moved a question (the v3.3.1
  quarantine discipline, applied consistently).

A QUARANTINED question (section 4 L-4) is excluded from the solvable set but
STILL COUNTED in the denominator, so quarantining can never manufacture a pass
by shrinking what must be solved.

## §2A — WRITE AUTHORITY (rebuild, never XML surgery)
NA's edit cycle is exactly:
    model = notes_docx.parse(draft_path, media_dir=...,
                             exam_code=<registry exam_code>,
                             tier=<unit record tier>)
    ...correct and improve the MODEL...
    notes_docx.build(model, final_path)          # strict=True, the default
NA NEVER edits .docx XML and NEVER hand-rolls a paragraph, colour, border or
line rule. Three properties follow from the shared builder and are the reason
this is safe:
  W-1 NUMBERS ARE DERIVED, NEVER STORED. Every n.k, n.k.m, "Example j" and
      "Recall j" is computed from block ORDER at render time
      (notes_docx.outline_of). Section 6A's renumber rule therefore cannot be
      violated by inserting or dropping a block — there is no stored number to
      go stale. outline_of is also G-10's oracle.
  W-2 UNTOUCHED MATHS IS NEVER RE-AUTHORED. parse preserves each oMath element
      verbatim; build re-inserts it. NA re-compiles only an equation it
      actually changed.
  W-3 THE REBUILD IS A FIXED POINT. build -> parse -> build reproduces
      word/document.xml byte-for-byte (notes_docx self-test), which is what
      makes section 8's idempotence rule checkable rather than asserted.
      The fixture backing W-3 must exercise EVERY member of RUN_TYPES and
      every CONTENT_KINDS variant, INCLUDING an option whose content is
      entirely OMML — the commonest option shape in a quantitative exam and
      the one that GAP-2026-08-12-NAPARSE lost. A fixture that omits a shape
      does not test it, and a byte-identity check over two equally-wrong
      files proves nothing. The round-trip rebuild is STRICT.
  W-4 THE DOCUMENT CANNOT CARRY ITS OWN METADATA. Section 7 / F-6 bans
      pipeline metadata from a student-facing file, so exam_code and
      unit.tier — the two fields validate_model REQUIRES — are exactly the
      two parse() cannot recover. NA supplies both from the registry unit
      record. Parsing without them yields a model that fails validation, and
      build(strict=True) then raises for EVERY unit of EVERY exam, maths or
      not. NA NEVER passes strict=False to work around this: strict is the
      contract that makes a lossy parse visible, and switching it off
      converts a loud failure into a silently mangled student document.

SCOPE OF THE WRITE:
  ALLOWED — defect remediation (anything a verdict or a gate identifies), and
    bounded improvement: tightening a bullet over the D-1 cap, converting >= 3
    parallel facts into a table (D-3), adding a clarifying bullet or KEY
    POINTS line, adding a genuine SPEED HACK, sharpening a §4 B3
    distractor-autopsy line or the Educational Objective, improving figure
    clarity, sharpening wording; and (v3.3.0) REPLACING a redundant Example
    IN PLACE with one teaching an uncovered scenario or moving it under an
    uncovered concept section — the G-12 remediation. A one-for-one
    replacement keeps the Example count, so the global j sequence and G-5's
    type-coverage proof survive; the swap is logged as an improvement.
  FORBIDDEN — changing the NUMBER of Examples or Recall items as bounded
    IMPROVEMENT (a net add or remove moves the global j sequence and voids
    G-5's type-coverage proof; replacement is not addition). A net ADD is
    licensed ONLY by a G-12 or G-13 hard finding — a bank-attested type, a
    concept spread the existing stack cannot cover, or (v3.4.0) an attested
    fusion with no integration section to teach it — because numbering is
    derived (W-1) and G-11 re-gates the result; a net REMOVE is never
    licensed outside §4 L-2 full regeneration. Also FORBIDDEN: changing any Answer
    except through section 3A; DELETING an Example's distractor autopsy or its
    Objective, or dropping a per-option rationale below the wrong-option count
    (validate_model + G-5 would fail the rebuild); and introducing any fact
    that is not syllabus-required, PYQ-anchored or BRIDGE-justified (D-6).
    Without that last guard "improvement" is an open door for off-syllabus
    content in a student document.
  Every improvement is logged (notes_audit.log_improvement) so section 8 is
  testable.

## §3 — PYQ PROTECTION (paraphrase rule)
Unchanged. Examples are PYQ-ANCHORED but PARAPHRASED: fresh numbers, fresh
wording. Anchors (exam-date + Q number) live in the bank and the audit_summary
ONLY — never in the document (section 7). Actual PYQ text is never reproduced.
This survives the loss of the .md report because the bank still holds the
anchors.

## §3A — KEY CORRECTION (supersedes v2.0.0 owner decision 4a)
A stored key is no longer beyond appeal. Where NA's notes-derived answer
disagrees with the bank's correct_answer, NA CORRECTS the key and teaches the
correct method — it never bends the notes to fit a wrong key, because that
would mean deliberately teaching a student the wrong method so the document
agrees with a defect.

Two tiers, classified by notes_audit.classify_key_conflict on ONE question:
does the bank's VERBATIM explanation itself arrive at NA's answer?
  TIER 1 — BANK_SELF_CONTRADICTS (yes). The bank disagrees with ITSELF: its
    explanation concludes X while its correct_answer field says Y. That is a
    Step-5 extraction defect with evidence from inside the bank, so the
    correction is applied SILENTLY.
  TIER 2 — JUDGEMENT (no). The bank is internally consistent and NA still
    disagrees — NA against the examiner AND the official explanation. The
    correction is still applied, but it is DISCLOSED: named in the chat
    delivery line and recorded in audit_summary with the stored answer, NA's
    answer and the reasoning.
There is NO CAP on corrections (owner decision). NA reports the COUNT in the
chat line, because an unusual number of corrections in one unit is far more
likely to mean the wrong paper or wrong subtopic was bound upstream at Step 5
than that the examiner erred that often. The count informs; it never blocks.

THE BANK IS NEVER WRITTEN. notes_pyq_bank.json is NB's artifact and the
blueprint holds bank_ref, a sha256 over its bytes; editing it would fail
verify_bank_ref for EVERY unit in the exam on the next run and force a full NB
re-run to recover. Corrections live in the report and the registry — which is
also the form to feed back into a Step-5 fix.

Both tiers record the verdict SOLVABLE_KEY_CORRECTED, which counts toward the
pass.

## §4 — CONVERGENCE LOOP (self-contained; always ends in a delivered file)
  L-1 Any PARTIAL/NOT verdict produces a targeted correction to the MODEL
      (section 2A); the affected questions re-audit; the notes minor version
      bumps.
  L-2 After MAX_PATCHES_PER_QUESTION (3) failed corrections on the same
      question: FULL REGENERATION of the unit's model by NA itself. v3.0.0
      does not route back to NC.
  L-3 After MAX_REGENERATIONS (3) without convergence: STOP LOOPING on that
      question. With section 3A in force this is no longer "the notes are
      badly written" — NA can always teach the correct method and the correct
      answer — so a question that still cannot be made solvable from
      in-syllabus notes indicates the question does not belong to this
      subtopic or its stem is corrupt.
  L-4 QUARANTINE that question (notes_audit.quarantine) with the reason. The
      unit certifies on the remaining set (section 2 COVERAGE). The quarantine
      list is named in the chat and stored in audit_summary; it is what to
      check against Step 5, and a bank refresh re-audits it under the section
      3 standing trigger. NOTHING about a quarantined question appears in the
      document.
  L-5 Every correction is logged in the report (patch_log).

## §5 — MACHINE GATES
  G-1 DENSITY (notes_core.density_gate): bullet word counts, table-first
      violations, page count within the tier band. The bullet count covers
      EVERY rendered bullet — concept bullets and the bullets inside KEY
      POINTS and TRAP boxes alike (notes_core v2.4; before it, the counter
      recognised only Word list paragraphs and the shared builder emits a
      literal glyph, so the D-1 check saw nothing at all). D-1 is also
      enforced at CONSTRUCTION by notes_docx.validate_model, so the two layers
      agree rather than one silently covering for the other.
  G-2 MATH — three separately reported gates, all reporting ZERO findings.
      They are named G-2a / G-2b / G-2c here because those are the exact keys
      terminal_regate writes into the report and audit_summary; "G-2" alone is
      the umbrella, never a report key.
      G-2a OMML presence by XML assertion (notes_core.assert_omml). NEVER
          verify equations through a LibreOffice-rendered preview: LibreOffice
          drops OMML SILENTLY (verified 2026-08-08 with a minimal fixture).
      G-2b STRUCTURAL-OMML SCAN (notes_core.scan_omml_structural): no textual
          exponent, no unicode super/subscript character inside any oMath
          region.
      G-2c FLAT-TOKEN SCAN (notes_core.scan_flat_math_tokens): no un-styled
          math token in any plain text run.
  G-3 ANATOMY (notes_audit.gate_anatomy): required blocks for the unit's tier
      present and in section 6A order; adjacent boxes separated by spacers.
      notes_docx.validate_model owns the contract and enforces it at
      CONSTRUCTION, so this gate re-asserts it on the model that produced the
      SHIPPED file — which matters because NA edits that model after NC built
      it.
  G-4 CONTENT-STYLE BAN SCAN (notes_core.scan_prose_bans), honouring per-unit
      exemptions declared in the blueprint.
  G-5 QUESTION-FORMAT (notes_audit.gate_question_format): every Example and
      Recall matches the fixed template, its type is a member of the
      blueprint's allowed_question_types, and a Recall carries neither an
      Explanation nor a SPEED HACK. The gate reports which allowed types went
      unused across the unit so type coverage is visible rather than assumed.
      v3.2.0: G-5 also enforces the §4 B3 per-option contract on the SHIPPED
      model — every Example carries a one-line Educational Objective and one
      distractor-autopsy line per WRONG option (MCQ 3; MSQ 4 − #correct; NAT
      >= 1 trap value), and a Recall carries neither the autopsy nor the
      Objective. notes_docx.validate_model gates the same at construction, so
      the two layers agree exactly as they do for D-1; folding this into G-5
      (rather than a new gate id) keeps notes_audit.GATES and this spec in
      one-to-one agreement.
  G-6 OUTLINE-NUMBER INTEGRITY (notes_audit.gate_outline): numbering gapless
      and sequential, and every in-text cross-reference ("see n.k") resolving
      to a number that exists. notes_docx.outline_of is the oracle. Because
      numbers are DERIVED from block order, a stale cross-reference is the only
      way this can break — and it is exactly what NA's editing can introduce
      silently, since removing a block renumbers everything after it.
  G-7a VISUAL LAYOUT (notes_audit.preflight -> renderer). Render and inspect
      every page for tables past the margin, boxes split mid-Answer,
      illegible figures, orphan headings and trailing blank pages.
      LIMITATION, STATED RATHER THAN ASSUMED AWAY: LibreOffice drops OMML on
      conversion, so the rendered pages show the maths MISSING whether or not
      it fits. G-7a is therefore a NON-MATH layout gate; equation geometry is
      G-7b's job. Without a renderer the gate degrades to DORMANT and is
      REPORTED as dormant — absence never halts an audit.
      F-4a PALETTE ADVISORY (v3.6.0): G-7a's meta carries
      notes_audit.figure_palette_meta(docx) — figures counted, figures whose
      saturated ink lies outside notes_core.FIGURE_PALETTE, and a note. It is
      information ONLY: never a finding, never ok=False, never a re-render
      trigger (§1), DORMANT and reported without Pillow.
  G-7b OMML AND FIGURE GEOMETRY (notes_audit.gate_line_rules): every paragraph
      carrying an equation or an image must use an AUTO line rule. A fixed
      rule CLIPS the object while leaving it present in the XML, so G-2a
      passes and the page is still wrong. This is the mechanical replacement
      for the visual check LibreOffice cannot perform, and it is stricter than
      a human glance would be.
  G-8 ANSWER INTEGRITY (notes_audit.gate_answer_integrity): every printed key
      must be a usable answer to the printed options — MCQ in range, MSQ a
      non-repeating subset, NAT numeric, none missing. G-5 checks the
      template; nothing before v3.0.0 checked the key itself, and a wrong key
      is the worst defect that can reach a student.
  G-9 ORPHAN TERMS (notes_audit.gate_orphan_terms): a term used in a stem,
      option or explanation but taught nowhere in the notes body breaks the
      closed-book promise at vocabulary level. The section 2 solver already
      knows the subject and can silently supply the missing term; this gate
      cannot. ADVISORY — it reports for NA's judgement and does not block.
      SOURCE (GAP-2026-08-12-NAPARSE D-3): the gate reads the model's PROSE
      runs only — text and sym — NEVER a serialisation of the model and NEVER
      OMML: markup tokens (degHide, radPr, oMath) and model keys (stem,
      options, explanation) are not vocabulary and may never surface as
      findings.
      SCOPE (owner decision OD-1): EXACTLY stem, options and explanation.
      SPEED HACK is deliberately EXCLUDED — a shortcut teaches at point of
      use, so a term introduced there is not left dangling, and including it
      only multiplied noise. Widening this scope is a spec change, never an
      engine one.
      MODE (owner decision OD-2 — Design A, domain-anchored): NA passes
      syllabus_terms = notes_audit.syllabus_terms_for(unit_questions,
      extra=(subject, topic, subtopic names)) — the unit's bank concept_tags
      plus its resolved names, artifacts the pipeline already carries. A term
      reports ONLY if it is syllabus-evidenced AND untaught; everything else
      is suppressed and counted in the gate's meta. This is what lets the one
      real finding ('potential', an ordinary English word that IS a Physics
      syllabus term) surface instead of drowning among dozens of false ones —
      no stopword list can make that separation, only domain evidence.
      Nothing is ever downloaded; the exam's own artifacts are the sole
      authority, which keeps the gate exam-agnostic across the corpus.
      USABILITY BAR: a clean unit yields ZERO findings. An advisory gate that
      always fires is a gate nobody reads, and a real orphan inside dozens of
      false ones is a missed defect. The unanchored form (no syllabus_terms)
      exists only for callers with no bank in hand and its meta says so.
  G-10 COUNTER INTEGRITY (notes_audit.gate_counters): Example j and Recall j
      sequences gapless and 1-based. G-6 covers section 6A outline numbers
      only.
      G-10 reads the document through notes_core.document_text, which
      preserves ELEMENT BOUNDARIES: runs inside a paragraph concatenate with
      no separator (Word may split "2.10" across runs at any time),
      paragraphs join with one. A bare re.sub(r"<[^>]+>", "", xml) welds the
      last character of one paragraph to the first of the next: a box ending
      "Answer: 1" before the heading "2.10 MIND MAP" reads "12.10", the
      level-2 scan matches "12.10" and the derived number is reported
      missing. THAT IS THE STANDARD TAIL ANATOMY (B7 then B8), so the bare
      form fails correct documents across the corpus. No gate may implement
      its own text extraction.
  G-12 COVERAGE (notes_audit.gate_coverage) — v3.3.0, BLOCKING. The target
      is notes_core.coverage_target_for over the unit's bank slice, computed
      by NA itself (it holds the bank), so the same contract NC authored to
      is the one gated here — one authority, no drift. HARD: every question
      type the unit's own bank attests appears in >= 1 worked Example, and
      Examples span at least the required number of DISTINCT concept
      sections (from the slice's distinct concept_tags, clamped to
      notes_core.COVERAGE_CONCEPT_CEILING; a tagless slice demands a spread
      of one, and an empty slice demands nothing — no examples where no
      evidence). THE CONTRACT IS SPREAD, NOT COUNT (owner decision,
      2026-08-13): no minimum example count exists anywhere in this
      pipeline, because a count is satisfiable by clones of one scenario.
      An Example's concept is the nearest preceding concept section,
      derived from block order exactly like the outline numbers — nothing
      new is stored or rendered, so W-3 and §0B P-4 are untouched.
      THE FORMAT CONTRACT (v3.5.0, HARD; NC §4 B3a FMT-1..3): when the
      target's format_mix attests >= 1 figure-based question in the slice,
      at least ONE concept section must PAIR a rendered figure with a
      worked Example — figure-reading is a separate skill and the exam
      tests it here. The pairing is detected purely from block order (a
      concept block carrying a figure content item AND >= 1 Example); the
      B8 mind map is a different block type and NEVER satisfies it. WHERE
      the pairing belongs among the figure-evidenced concepts is §2A
      judgement, informed by the advisory figure_concept_tags below — tags
      are free text and are never name-matched to sections (the standing
      G-12 discipline). The lead-format emphasis rule (FMT-2) is authoring
      judgement, not a regex — NA sharpens it under §2A, never blocks on
      it. A quarantined figure question still counts toward format_mix
      (the v3.3.1 rule: the contract reads the BANK), and an UNRESOLVED
      image still counts (the student saw a figure in the real exam).
      Remediation of a format finding is the §2A net-ADD licence exactly
      as for any G-12 hard finding: NA adds the figure + the Example that
      reads it. Rollout is the G-12 precedent — the rule applies at each
      unit's NEXT audit; no grandfathering flag exists or is needed, and
      a pre-v2.10 hand-built target without format_mix simply skips the
      format check (additive, never retroactive).
      ADVISORY, in meta, never blocking: figure_advisory (the slice carries
      stem figures but the model has no concept figure — subsumed by the
      hard pairing wherever figure evidence exists, kept for meta
      consumers), figure_concept_tags + figure_example_pairs (v3.5.0), and
      duplicate_suspects (a concept section with more than one Example of
      one type). The SEMANTIC half of the duplicate question — do two
      Examples teach the same scenario? — cannot be a regex and is §2A's
      duty: NA, having solved every bank question closed-book, REPLACES a
      redundant Example with an uncovered scenario rather than keeping
      both. Every replacement is a §2A improvement and is logged.
      DORMANT IS NEVER A LIVE-NA OUTCOME: the bank is a required §0A input,
      so a live run ALWAYS has a target. The DORMANT form exists only for
      bank-less callers of the engine; a dormant G-12 in an NA delivery is
      itself a defect and MUST be disclosed in the §9 chat line, never
      silently accepted.
      QUARANTINE DOES NOT SHRINK THE CONTRACT (v3.3.1): a quarantined
      question (section 4 L-4) still counts toward required_types and the
      concept evidence, because coverage_target_for reads the BANK slice and
      quarantine lives in the report, never in the bank. Quarantine says
      "this one stem is corrupt or mis-filed", not "the syllabus stopped
      testing this type" — so if a unit's only numeric item is quarantined,
      the numeric-Example requirement stands and NA teaches that type from a
      FRESH scenario (the section 2A net-ADD licence covers exactly this).
      The same is true of the spread minimum: it derives from the slice's
      concept_tags, quarantined or not.
  G-13 INTEGRATION (notes_audit.gate_integration) — v3.4.0. The target is
      notes_core.integration_target_for over the bank with unit_order =
      notes_core.unit_order_from_registry(registry) (v3.4.1: the ONE order
      builder — the same map §2's certification set uses; neither map is
      ever hand-built), computed by NA itself — the SAME contract NC §4
      B4a authored to, one authority, no drift (the G-12 idiom). Filing is
      LATEST-PARTNER: a fused question attests an integration section only
      in the latest member of its fusion set, so backward-only teaching
      holds by construction and no two units are ever asked to teach the
      same fusion.
      HARD, only when the target attests a fusion for THIS unit: every
      attested fusion is taught by an integration section — a concept block
      whose FIRST bullet is the Combines declaration naming every partner
      (NC §4 B4a I-2; the mechanical marker is CONTENT, so no new model
      field exists and W-3 / §0B P-4 are untouched); integration sections
      sit AFTER every core concept section (they close the concept stack,
      before the Trap Box); and a matched section carries >= 1 worked
      Example.
      DORMANT, never blocking, always reported: a target-less call
      (bank-less engine callers only — the §0A rule that a live NA always
      has the bank applies exactly as it does to G-12), and the
      GRANDFATHERED case: a bank carrying no integration_partners anywhere
      predates notes-pyq-bank/1.2 and could not attest a fusion. UNLIKE
      G-12, grandfathered dormancy IS a legitimate live-NA outcome — it is
      disclosed in the §9 chat line, and the unit certifies without an
      integration section until the bank is refreshed with tags (NB §3B
      B-1; §7 there).
      ADVISORY, in meta, never blocking: unattested_sections — integration
      sections present without bank attestation (SME bridge-justified,
      D-6); NA judges them under §2A like any other content. Also ADVISORY
      (v3.4.2): unresolved — fused questions filed at this unit on
      DEFECTIVE evidence (a fusion-set member unknown to the unit order: a
      typo'd or out-of-registry partner). The defect is the BANK's and its
      fix is NB's next run; the gate NEVER demands a Combines line naming
      an unresolvable subtopic, and every entry is disclosed in the §9
      chat line.
      NAME MATCHING (v3.4.2): the Combines-line match normalizes BOTH
      sides with notes_core.display_norm — the SAME per-component norm
      subtopic_key uses — so legal drift between paper-header bytes and
      manifest names (& vs and, dash variants, NFKC, spacing) can never
      produce a false blocking finding. STATED RESIDUAL: the match is
      normalized CONTAINMENT, so a partner name contained in a longer name
      ("Waves" inside "Matter Waves") can over-match; the §2 closed-book
      solve of the INBOUND fused questions is the semantic net behind the
      mechanical check — a bridge that teaches the wrong partner cannot
      make them solvable, and the solve fails loudly.
      REMEDIATION ROUTING: a G-13 finding is a PARTNER-HOMING gap, and the
      remedy is the integration section — EXTEND it (a bridge bullet, a
      seam Example via one-for-one replacement) or ADD it (the §2A net-ADD
      licence covers a G-13 hard finding exactly as it covers G-12's).
      QUARANTINE IS NEVER THE ANSWER to a G-13 finding: quarantine says
      "this one stem is corrupt or mis-filed" (§4 L-4), not "the notes lack
      the partner bridge" — quarantining a fused question would hide the
      gap AND (v3.3.1 discipline) not even shrink the contract, since the
      target reads the BANK. A fused question that is genuinely corrupt
      still quarantines through §4 L-1..L-4 on its own merits, exactly as
      before.
  G-11 TERMINAL RE-GATE (notes_audit.terminal_regate) — MANDATORY, LAST.
      After the final edit, re-run the FULL solve across the unit's §2
      CERTIFICATION SET (v3.4.2 — audit_questions_for; through v3.4.1 this
      line still said "ALL of the unit's bank questions", the pre-filing
      boundary, which would have re-solved a DEFERRED question from notes
      that must not teach it) and EVERY gate above over the bytes that will
      ship, then hash them. NA edits the document, so certifying the pre-patch draft
      certifies a file that no longer exists: a correction that fixes Q7 and
      breaks Q12's cross-reference is exactly what a pre-patch certification
      misses. Only G-9 (advisory), a DORMANT G-7a, a target-less DORMANT
      G-12 and a DORMANT G-13 (target-less or grandfathered) are
      non-blocking.
      G-11 is itself REPORTED as a gate, carrying the certified sha256 and the
      number of gates run, so audit_summary shows plainly WHICH bytes were
      certified rather than asserting it in prose alone. Every identifier in
      notes_audit.GATES appears in the report; notes_sync_audit.py checks that
      this list and this section still agree.
      Gate identifiers are HISTORICAL, not positional: G-12 and G-13 were
      added after G-11 existed and are deliberately listed above it, because
      G-11 is the terminal re-gate and MUST remain last — "EVERY gate above"
      includes G-12 and G-13.

## §6 — REPORT AND STATE
There is NO .md audit report. The report OBJECT (notes_audit.new_report) is
still built and is still the certification instrument — pass_for_unit operates
on it and is the vacuous-pass floor — but the persisted artifact is
notes_audit.audit_summary(...) stored INSIDE the registry unit record
(notes-registry/2.1). The summary itself carries the report schema string
notes-audit-report/2.0 (notes_audit.REPORT_SCHEMA), so a schema bump is
visible to a reader of the registry and to notes_sync_audit.py. It carries: verdict counts by class, the key-correction
list with tiers, the judgement-tier count, the quarantine list, the
improvement and patch counts, the FIGURE_PENDING queue, every gate result,
the bank_ref and taxonomy_ref the unit was audited against, and the final_ref
of the shipped bytes. The two refs are what let the section 3 standing
re-audit trigger identify which units a refreshed bank affects.

A unit passes ONLY when notes_audit.pass_for_unit(report, unit_questions) is
True, at which point it moves DRAFTED -> AUDITED_PASS with notes_version
bumped and final_ref set.

## §7 — CONTENT-STYLE BANS AND THE DOCUMENT ITSELF
Framework_NotesCreate section 7 and F-6 apply UNCHANGED to NA's output.
NOTHING inside the document ever marks a correction, a quarantine, a version,
a warning, a comment, a review note or any pipeline metadata. Every one of
those lives in the chat and the registry. A student-facing file carries
teaching and nothing else.

## §8 — RUNS, STATE AND IDEMPOTENCE
One subtopic per run; a multi-unit request splits into separate per-unit runs,
each a complete step ending in its own footer. On completion the unit moves
DRAFTED -> AUDITED_PASS.

IDEMPOTENCE RULE: re-running NA on its own _Final.docx MUST produce zero
corrections, zero improvements and a byte-identical document. This is what
bounds section 2A's discretionary improvement — an improvement licence with no
convergence criterion would otherwise let two runs of the same input produce
two different documents. The property rests on notes_docx's fixed-point round
trip (W-3) and on section 1's deterministic, never-re-judged figure renders.

## §9 — DELIVERY
NA emits EXACTLY ONE document in every outcome, named by
notes_core.notes_final_filename(...) — {unit_code}_{Slug}_Final.docx. The name
is derived by CALLING the engine, never by spelling the pattern.

On completion: present_files the _Final.docx AND the updated
notes_registry.json (unit -> AUDITED_PASS, carrying draft_ref, final_ref and
audit_summary), then RENDER THE F2 STEP-COMPLETE FOOTER as the LAST element of
the response (Framework_DeliveryFooter section 4-1; 4-cell NOTES bar "3 of 4";
header "Step NA · NotesAudit"; Next -> ND: NotesDeliver in a new chat). The
footer is obligatory after a present_files call (section 4-0 R1) and is never
omitted.

THE CHAT DELIVERY LINE carries what the document deliberately does not:
<Sub Topic Name> (<sid>), unit_code, notes_version, n/n solvable, the
key-correction count with the JUDGEMENT-tier ones named individually (section
3A), the quarantine list with reasons (section 4 L-4), any --accept-modified
warning (section 0B P-3), the FIGURE_PENDING count, any DORMANT gate
(section 5 G-7a; a dormant G-12 is a DEFECT, section 5 G-12), and the
section 5 G-12 coverage line: concepts covered vs required, the format
line (v3.5.0 — figure evidence count, figure+Example pairs present, and
any format finding remediated, named), any
duplicate_suspects, the figure advisory if raised, and every G-12-driven
Example replacement or licensed net ADD (section 2A) named individually —
plus (v3.4.0) the section 5 G-13 integration line: fusions taught vs
attested, a GRANDFATHERED dormancy disclosed plainly when the bank predates
notes-pyq-bank/1.2, any unattested integration sections kept under D-6, and
every G-13-driven extension or licensed net ADD named individually. Also
(v3.4.1) the audit-boundary line: every DEFERRED fused question named with
its filing unit ("solved there, not here"), and every INBOUND fused question
named with its header unit — so the operator always sees why this unit's
question count differs from its taxonomy row. Also (v3.4.2): every
unresolved-evidence entry (bank_id + the unknown partner string — "fix at
the next NotesBlueprint run") and every ORPHANED-FILING deferral (§2 —
"certification pending orphan resolution"), named individually.

---

# END OF Framework_NotesAudit v3.6.0
