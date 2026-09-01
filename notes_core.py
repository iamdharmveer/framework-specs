"""
notes_core.py v2.12 — Shared engine for the Notes pipeline (Steps NB/NC/NA/ND).

v2.12 — 2026-09-01 — THE RECALL CONTRACT (GAP-2026-09-01-RECALL-CONTRACT; pairs
    with Framework_NotesCreate v2.9.0 §4 B7/B7a, Framework_NotesAudit v3.7.0 §5
    G-14; notes_docx >= v1.7, notes_audit >= v2.9). The Recall Check (B7) had
    a FORMAT contract and no CONTENT contract: nothing anywhere defined how
    many Recall questions a unit carries, which concepts they cover, their
    order, their difficulty, or where their distractors come from — the
    declared-property-without-a-definition defect class of
    GAP-2026-08-21-DIFFICULTY-STICKER-LABELS, on the one section built for the
    student to self-test. This engine now carries the contract, derived
    entirely from data every exam already has (the bank slice, the registry
    order map, and — when present — the exam's own difficulty profile), so NC
    authors to it and NA G-14 gates it and the two can never drift (the
    coverage_target_for / integration_target_for idiom, third instance):
      recall_target_for        — the unit's RECALL CONTRACT: required types,
                                 figure-item demand, EARLIER-only cumulative
                                 partners (unit_order; I-4 backward-only by
                                 construction), the near-miss demand, and the
                                 four-rung DIFFICULTY LADDER (concept tag ->
                                 subtopic (profile) -> topic -> exam -> neutral)
                                 with every rung's evidence count.
      recall_cumulative_min    — ceil(core / RECALL_CUMULATIVE_DIVISOR), floor
                                 RECALL_CUMULATIVE_FLOOR, 0 without an earlier
                                 subtopic, capped by RECALL_CEILING.
      recall_expected_band     — the ONE band resolver (author and gate call
                                 it): nearest rung with evidence, near-miss +1
                                 band, MSQ/NAT floor from the shared rubric.
      recall_verify_difficulty / recall_authoring_profile — thin wrappers over
                                 blueprint_core.verify_difficulty_obs /
                                 difficulty_authoring_profile — the SAME rubric
                                 Step 7 labels mock questions with and PYQExplain
                                 profiles real PYQs with. Imported LAZILY: absence
                                 is reported as dormant, never a crash.
      difficulty_profile_load  — reads [ExamCode]_difficulty_profile.json; NEVER
                                 raises (None + reason on any defect: the
                                 O-5 owner rule that a missing/partial profile
                                 never blocks a unit).
      recall_exam_mix_check    — the shipped set's band mix vs the exam's
                                 measured paper-level mix, ±RECALL_EXAM_MIX_
                                 TOLERANCE items per band; dormant without a
                                 profile.
      recall_multi_concept_required / recall_is_multi_concept — R-12: where the
                                 exam's own questions combine concepts (a
                                 top-band PYQ) or the unit teaches >= 2 concepts,
                                 >= 1 Recall combines concepts, read from the
                                 rubric-verified axiom_concepts observation.
      scenario_key / is_clone  — content-token set of a stem and the Jaccard
                                 clone test (RECALL_CLONE_JACCARD) behind the
                                 no-clone rule (NC §4 B7a R-7).
      normalize_complexity     — bank `complexity` tag -> exam band label.
    Constants RECALL_* are spec-lock-pinned (forward + reverse halves); the
    specs restate NONE of the numbers outside the gap entry. ADDITIVE: every
    existing unit keeps its Recall Check byte-identical; a registry unit with
    no recall_contract record leaves G-14 DORMANT (reported).

v2.11 — 2026-08-30 — GAP-2026-08-30-NOTES-FIGURE-CONTRACT (P3 of the figure-colour
    programme; pairs with Framework_NotesCreate v2.8.0 §6 F-4a and
    Framework_NotesAudit v3.6.0 §1 / G-7a). NotesCreate figures (F-4 diagrams,
    B8 mind map) had NO render recipe — no palette, no dpi, no size — and
    NotesAudit's "re-render via figural_core" clause was non-executable as
    routed. This engine now carries FIGURE_PALETTE: the SAME values Step 7's
    figural_core draws with (Okabe-Ito hues, TEXT tier, FILLS, HATCHES, the
    pinned ATOM_PALETTE, FIGURE_DPI 300), PINNED HERE by copy and locked by the
    SPEC-LOCK tripwire plus a CI equality check against figural_core (the
    self-test imports figural_core dynamically, test-only). Same numbers,
    verified, NO runtime coupling: figural_core is NOT routed to Notes and its
    13 mock gates never run here. Helpers figure_text_ink() / figure_fill_style()
    / figure_structure_png() are the Notes-side calls the F-4a contract names.
    Everything is ADDITIVE; no existing notes unit is re-rendered.

v2.10 — 2026-08-15 — THE FORMAT CONTRACT (figure vs text balance; owner
    decisions of the 2026-08-15 design session, approved proposal; pairs
    with Framework_NotesCreate v2.7.0 §4 B3a and Framework_NotesAudit
    v3.5.0 §5 G-12; notes_audit >= v2.7). Reading a figure is a separate
    skill from knowing the theory, and the exam's own history decides where
    it must be taught. coverage_target_for gains two ADDITIVE fields,
    derived entirely from data every bank already carries (the figure flag
    + concept_tags — no new field, no re-ingest, no grandfathering needed;
    the G-12 rollout precedent):
      format_mix        — {"figure": n, "text": n} over the unit's slice.
      format_by_concept — the same split per normalized concept_tag; NC
                          picks each concept's LEAD Example format from it
                          (frequency shapes EMPHASIS, never exclusion) and
                          G-12 lists figure-evidenced tags advisory.
    The three owner rules the fields encode: (1) BOTH formats attested ->
    BOTH taught — the hard downstream demand is deliberately minimal, >= 1
    concept section pairing a rendered figure with an Example whenever
    format_mix["figure"] >= 1; (2) frequency shapes EMPHASIS, never
    exclusion, and never count-mirroring (the spread-not-count decision
    applied to formats); (3) no evidence, no demand — a zero-figure slice
    never demands a figure. An UNRESOLVED image still counts as figure
    evidence (the student saw a figure in the real exam); a quarantined
    figure question still counts (the v3.3.1 discipline — the contract
    reads the BANK). Callers passing hand-built targets without the new
    keys are unaffected: the gate skips the format check when format_mix
    is absent.

v2.9 — 2026-08-14 — FULLY-RESOLVED FILING + ONE NAME NORM (independent
    adversarial review + 400-trial property fuzz of the integration feature;
    pairs with Framework_NotesBlueprint v3.1.1, Framework_NotesCreate
    v2.6.2, Framework_NotesAudit v3.4.2; notes_audit >= v2.6). Four fixes:
      (1) FILING MOVES ONLY ON FULLY-RESOLVED EVIDENCE. A fused question now
          moves off its header ONLY when EVERY member of its fusion set —
          header included — is in unit_order. Before: an OUT-OF-SYLLABUS
          header's question could file INTO a certifiable unit's set (the
          excluded subtopic is not in the registry, so the partner became
          "latest known"), and a typo'd partner silently under-filed. Now
          any unresolved member keeps the question at its header — exactly
          the pre-feature boundary — and the defect is REPORTED, never
          silently absorbed.
      (2) unresolved REPORTING. integration_target_for returns an
          "unresolved" list ({bank_id, unknown scope strings}) for fused
          questions filed at this unit on defective evidence; G-13 surfaces
          it ADVISORY (an ingest defect routes to NB, not to the notes) and
          never demands a Combines line naming an unresolvable subtopic.
      (3) display_norm — the ONE name normalization for matching a display
          name in prose, wrapping syllabus_provenance.norm (the same norm
          subtopic_key uses). G-13's Combines match now uses it, so legal
          header-vs-manifest drift (& vs and, dashes, NFKC) can no longer
          produce a false blocking finding.
      (4) DUPLICATE-NAME QUALIFICATION (E-16): when two partners in one
          fusion share a bare display name, the target qualifies each as
          "<Topic> :: <Name>", so the Combines line and the gate stay
          unambiguous.
    Shared-authority discipline unchanged: _integration_filing_key drives
    both teaching and audit homes; the 400-trial fuzz invariants (partition,
    backward-only, determinism, grandfather identity) all hold.

v2.8 — 2026-08-14 — INTEGRATION HANDSHAKE CLOSED (line-by-line certification
    sweep of the v2.7 feature; pairs with Framework_NotesCreate v2.6.1 and
    Framework_NotesAudit v3.4.1). Two defects, both found by tracing ONE
    fused question through NB -> NC -> NA:
      (1) THE AUDIT BOUNDARY NOW FOLLOWS FILING. v2.7 filed the fused
          question's TEACHING at the latest partner, but NA's closed-book
          solve still read the HEADER slice (bank_questions_for): the
          earlier unit was asked to solve a question whose ingredients its
          own notes must not teach (backward-only), while the filing unit —
          whose integration section exists to make it solvable — never
          solved it at all. New audit_questions_for(bank, subject, topic,
          subtopic, unit_order=None): the unit's CERTIFICATION SET — every
          bank question whose FILING HOME is this unit (header slice, minus
          fused questions DEFERRED to a later partner, plus fused questions
          INBOUND from earlier slices). Identical to bank_questions_for
          when the bank is grandfathered or no order is supplied, so
          nothing changes for any existing exam. The filing decision is one
          shared helper (_integration_filing_key) used by BOTH
          integration_target_for and audit_questions_for — one authority,
          the two can never disagree.
      (2) THE ORDER MAP HAS ONE BUILDER. v2.7 said "unit_order maps
          subtopic_key -> persisted ordinal" in prose and left NC and NA to
          each build it — the author/gate drift class this framework exists
          to kill. New unit_order_from_registry(registry): ordinals are the
          (s, t, nn) digits parsed from each unit's PERSISTED unit_code
          (NB §1A A-3 — assigned from manifest row order, never renumbered),
          keyed by subtopic_key(section, topic, name). NC and NA both call
          it; neither builds a map by hand. Units without a parseable
          unit_code or a complete manifest triple (pre-v3 legacy) are
          skipped — their resolution already routes to NB (MIGRATION).
    coverage_target_for DELIBERATELY still reads the header slice: the
    coverage contract reads the BANK's evidence (the v3.3.1 quarantine
    discipline — the contract never shrinks because filing moved a
    question); only the SOLVE/certification boundary follows filing.

v2.7 — 2026-08-14 — INTEGRATION EVIDENCE (in-subtopic Integration sections;
    pairs with Framework_NotesCreate v2.6.0 §4 B4a, Framework_NotesBlueprint
    v3.1.0 §3B B-1, Framework_NotesAudit v3.4.0 §5 G-13; notes_audit >= v2.5).
    Real exams fuse 2-3 subtopics in one question; the portal links one page
    per subtopic, so the fusion is taught IN-SUBTOPIC: an integration section
    at the end of the concept stack, before the Trap Box, in the LATEST
    partner subtopic (backward-only — students have met every ingredient).
    Two additions, both additive:
      (1) PYQ_BANK_SCHEMA -> notes-pyq-bank/1.2. bank_add_question accepts an
          OPTIONAL integration_partners list: the OTHER subtopics a question
          genuinely fuses, each in the canonical Subject::Topic::Sub Topic
          Name scope form (the same form resolve_unit teaches). Malformed
          entries and a question naming its OWN subtopic as a partner raise.
          1.0/1.1 banks still load and migrate; the field defaults absent.
      (2) integration_target_for(bank, subject, topic, subtopic,
          unit_order=None) — the unit's INTEGRATION CONTRACT, the single
          authority NC authors to and NA G-13 gates (the coverage_target_for
          idiom one feature over). unit_order maps subtopic_key -> persisted
          ordinal (registry numbering); a fused question FILES at the LATEST
          member of its fusion set present in the order (latest-partner
          filing), so earlier partners never teach material the student has
          not reached. Without unit_order the question's own header subtopic
          is the filing home. GRANDFATHERING: a bank carrying NO
          integration_partners anywhere returns dormant=True — pre-1.2 banks
          never fail a gate they could not have satisfied.
    Deterministic throughout; no clock, no randomness (NA §8 idempotence).

v2.6 — 2026-08-13 — COVERAGE TARGET (Phase 2, Recommendations 3+4; pairs with
    Framework_NotesCreate v2.5.0 §4 B3a and Framework_NotesAudit v3.3.0 §5
    G-12; notes_audit >= v2.4). coverage_target_for(bank, subject, topic,
    subtopic, allowed_types=()) is the SINGLE authority for a unit's coverage
    contract, derived ENTIRELY from the unit's bank slice so NC (author) and
    NA (gate) can never disagree:
      required_types            — CANONICAL_TYPES attested in the slice,
                                  intersected with allowed_types when given.
                                  Each must appear in >= 1 worked Example.
      min_concepts_with_examples— distinct normalized concept_tags in the
                                  slice, clamped to COVERAGE_CONCEPT_CEILING;
                                  >= 1 whenever the slice is non-empty (a bank
                                  with no tags never over-demands). This is
                                  CONCEPT SPREAD, deliberately NOT an example
                                  count: N clones of one scenario satisfy a
                                  count and teach one thing — examples must
                                  span distinct concept sections instead.
      requires_figure           — any slice question carries a stem figure
                                  (ADVISORY downstream, never blocking).
      pyq_count / distinct_concept_tags — evidence meta for the report.
    An empty slice returns a ZERO target (no types, no minimum, no figure) —
    "no examples where no evidence" (NC B3/TIER-3) is preserved exactly.
    Deterministic: same bank slice -> same target, so NA idempotence holds.

v2.5 — 2026-08-13 — PUBLIC TEXT AUTHORITY (GAP-2026-08-12-NAPARSE D-2).
    document_text() is the PUBLIC single authority for the plain-text view of
    a .docx: runs inside a paragraph concatenate with NO separator (a run
    break is formatting, not text — Word may split "2.10" across runs),
    paragraphs join with one. The old _document_text was PRIVATE, which is
    why notes_audit.gate_counters reasonably rolled its own bare tag strip —
    the "one contract, two implementations" channel this closes. The private
    name survives as a sep=" " wrapper so the two existing prose/token
    scanners keep their historic behaviour bit-for-bit.

v2.4 — 2026-08-12 — FINAL-AUDIT FIXES (GAP-2026-08-12-NADOCX patch P3 of 3).
    Two defects found by the end-to-end sync audit of the four Notes specs.

    (A) THE D-1 DENSITY GATE WAS DEAD ON EVERY NOTES DOCUMENT. G-1 calls
        bullet_word_counts, which counted ONLY paragraphs carrying <w:numPr> —
        Word list paragraphs. notes_docx (v1.0) renders a bullet as a literal
        "\u2022  " text run, not a list paragraph, so bullet_word_counts
        returned [] for EVERY document the shared builder produces and
        density_gate reported CLEAN with 60-word bullets throughout. A gate
        that reports clean while checking nothing is worse than no gate: it
        buys false confidence. bullet_word_counts now recognises BOTH
        conventions — <w:numPr> and a leading bullet glyph — so it works on
        documents built before and after notes_docx, in table cells (where the
        KEY POINTS and TRAP bullets live) as well as body text.

    (B) A SLUG WITH NO ASCII COLLAPSED TO AN EMPTY, COLLIDING FILENAME. The
        sanitiser maps every non-alphanumeric run to "_", so a Devanagari,
        Tamil or Bengali slug — or one that is all punctuation — sanitised to
        "" and produced EX_S1_T1_ST01__Final.docx. Two different units in the
        same topic would then write the SAME filename and one would silently
        overwrite the other. The framework is exam-agnostic across 200+ Indian
        exams, so a non-ASCII sid is a realistic input, not a curiosity.
        _notes_stem now falls back to a short, deterministic hash of the RAW
        slug when sanitisation leaves nothing, which is stable across runs and
        cannot collide. An ASCII slug is completely unaffected — every
        existing filename is byte-identical.

    Both fixes are spec-lock-pinned and mutation-verified. No other surface
    changed.

v2.3 — 2026-08-12 — REGISTRY SCHEMA 2.1 (GAP-2026-08-12-NADOCX patch P2 of 2).
    P1 landed the 2.1 SHAPE while still emitting 2.0, because an engine that
    emits a schema string its own specs do not cite is exactly the drift the
    SPEC-LOCK block catches. P2 moves the specs, so the emitted schema moves
    with them:
      REGISTRY_SCHEMA -> "notes-registry/2.1". Unit records now carry
      draft_ref (written by NC), final_ref (written by NA) and audit_summary
      (NA's registry-embedded replacement for the .md audit report). 1.x and
      2.0 registries still load, gaining the three fields as None — the P1
      read-side default is unchanged, so nothing needs migrating.
    No other surface changed.

v2.2 — 2026-08-12 — NOTESAUDIT-AS-WRITER FOUNDATION (GAP-2026-08-12-NADOCX,
    patch P1 of 2). PURELY ADDITIVE: no existing function changes behaviour,
    no emitted schema string moves, so P1 deploys and verifies on its own and
    every current NB/NC/NA/ND run is byte-for-byte unaffected. P2 (the
    Framework_NotesAudit v3.0.0 rewrite and its companion specs) is what
    switches these on.
      (1) TWO NEW FILENAME AUTHORITIES beside notes_filename, same recipe and
          same sanitisation, so no step ever spells a filename itself:
            notes_final_filename   -> {unit_code}_{Slug}_Final.docx   (NA)
            notes_deliver_filename -> {unit_code}_{Slug}_Deliver.docx (ND)
          All three are spec-lock-pinned. A step that needs a name CALLS one.
      (2) docx_ref_for / verify_docx_ref — the bank_ref/taxonomy_ref staleness
          idiom applied to a .docx: {filename, sha256, bytes, generated}.
          NotesAudit now receives its input as a CHAT ATTACHMENT rather than
          from Project Files, so there is no longer any implicit guarantee
          that the file audited is the file NotesCreate produced. This is the
          evidence for that check. verify_docx_ref reports filename mismatch
          and sha256 mismatch SEPARATELY, because the two mean different
          things: the first is usually the wrong unit attached, the second a
          hand-edit between steps.
      (3) "notes-registry/2.1" is ACCEPTED but NOT yet emitted (REGISTRY_SCHEMA
          stays 2.0 until P2 moves the specs with it — an engine that emitted a
          schema the specs do not cite would be exactly the drift this file's
          SPEC-LOCK exists to prevent). registry_load additionally defaults the
          2.1 per-unit fields draft_ref / final_ref / audit_summary, so a 2.0
          registry read by a P2 step already has the shape.
    Companion: notes_docx.py >= v1.0 (the shared builder; construction left
    prose and became an engine in the same patch).

v2.1 — 2026-08-10 — SPEC-LOCK TRIPWIRE (defect-class closure). A deployment
    review found Framework_NotesCreate F-1 restating the filename recipe in
    prose while notes_filename sanitises non-alphanumerics to "_" — one
    contract, two implementations. The CLASS is any spec restating an
    engine-owned literal. Resolution: (a) the specs now name the engine as the
    SINGLE AUTHORITY at every such spot; (b) this file gains a SPEC-LOCK
    self-test block in TWO halves.
      FORWARD half — pins each spec-restated literal to its documented value:
        LEVEL_COLORS/BOX_COLORS (NC §6A), density constants + tier page bands
        (NC §5 / NB §5), schema strings, ROLES/STATES/TIERS vocabularies, the
        unit_code format and the notes_filename recipe INCLUDING its
        sanitisation. Fires when the ENGINE moves.
      REVERSE half — reads Framework_NotesCreate.md and compares the prose
        itself (F-1's deferral + sanitisation statement, the §6A colour
        literals, §5 D-1's word counts). Fires when the SPEC moves.
    The reverse half is the one that closes THIS defect: the engine was
    already correct and the prose was stale, so every forward pin passes
    verbatim against the pre-v2.2.1 text. Coverage is deliberately narrow —
    NotesCreate only, the three literals above; NB §5's tier bands and the
    NA/ND restatements are NOT yet spec-read and can still drift prose-side.
    No functional surface changed; all v2.0 self-tests retained verbatim.

v2.0 — 2026-08-10 — TAXONOMY CONSUMER (Framework_NotesBlueprint v3.0.0; owner
    decision: ONE subtopic vocabulary across Test Creation and Notes Creation).
    The Step-5 [ExamCode]_subtopic_manifest.json is now the single source of
    truth for Notes unit identity, mirroring the Mock pipeline's Cross-Step
    Subtopic Contract (Framework_Blueprint RULES 1/2/2a). New here:
      (1) load_subtopic_manifest() — loads + structurally validates the manifest
          and HARD-STOPS (ValueError) on an exam_code mismatch (wrong exam's
          manifest in Files can never be consumed silently).
      (2) taxonomy_ref_for() / verify_taxonomy_ref() — the same staleness idiom
          as bank_ref: {path, sha256, subtopics, generated} over the manifest
          bytes, so a re-uploaded manifest is detectable and flips units STALE.
      (3) assign_numbering(manifest, prior) — derives S/T/ST numbers from
          manifest row order, PRESERVING any prior assignment verbatim (persisted
          numbering: a Step-5 re-run that inserts or reorders subtopics never
          renumbers already-assigned units; new sids append with next numbers).
      (4) resolve_unit() — the three-tier operator-input resolution shared by
          NC/NA/ND: exact Sub Topic Id -> 'Subject::Topic::Sub Topic Name'
          scope (norm per component) -> bare Sub Topic Name (norm). Unique hit
          proceeds; multiple hits return 'ambiguous' with the candidates; zero
          hits return 'none' with nearest-name suggestions. Never fuzzy-picks.
      (5) sid_slug() — the sid's final component, used as the F-1 filename slug.
      (6) REGISTRY_SCHEMA -> notes-registry/2.0 and BLUEPRINT_SCHEMA ->
          notes-blueprint/2.0: units are KEYED BY sid (registry_init keys by
          u['sid'] when present, else legacy u['unit_code']); unit records carry
          sid, section, topic, unit_code, slug; the registry carries
          taxonomy_ref. 1.x registries/blueprints still load (read-only
          migration: sid defaults None; a real migration is a re-blueprint).
    All v1.8 self-tests retained verbatim; v2.0 adds its own.

v1.8 — 2026-08-10 — POST-DEPLOY REVIEW (drift class closed + doc fixes).
    (A) subtopic_key is a DERIVED field that was also STORED in every bank
    question, and the readers compared a fresh key against the stored one — so the
    v1.7 normalization change meant a bank written by v1.6 returned 0 questions for
    any subtopic containing '&' or an en-dash. Root fix: bank_questions_for and
    derive_taxonomy_counts now RECOMPUTE the key from each question's
    subject/topic/subtopic and never trust the stored value, which ends the drift
    class for this and any future subtopic_key change. The stored key is now
    informational only. PYQ_BANK_SCHEMA -> notes-pyq-bank/1.1 (accepts 1.0 and
    1.1); bank_load migrates a 1.0 bank by refreshing its stored keys so an
    inspected bank is self-consistent. (C) load_blueprint docstring corrected to
    say it accepts 1.0/1.1/1.2 and migrates to the 1.2 shape (the code already
    did). No public signature changed; all v1.7 self-tests retained.

v1.7 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
    subtopic_key now REUSES syllabus_provenance.norm per path component — the same
    canonical form the rest of the framework's taxonomy joins use (NFKC, dash
    unification, & -> and, '/' kept as data) — and additionally collapses spaces
    around '/'. Previously it only lowercased + collapsed whitespace, so a subtopic
    written "Microbial & Plant Biotech" in the syllabus and "Microbial and Plant
    Biotech" on the paper header produced DIFFERENT keys; the bank count never
    joined the blueprint unit, which silently got pyq_count=0 and the wrong tier.
    Measured before the fix: 4 of 5 realistic label variants missed the join.
    No public signature changed; downstream (bank_add_question stores the key,
    derive_taxonomy_counts / bank_questions_for read it) is unaffected beyond
    producing correct joins. All v1.6 self-tests retained.

v1.6 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 1 (bank_ref staleness link). The
    blueprint now carries a real bank_ref so a blueprint built from bank vN can
    never be silently paired with bank vM. BLUEPRINT_SCHEMA -> notes-blueprint/1.2
    (load_blueprint migrates 1.0/1.1 by defaulting bank_ref=None); new
    verify_bank_ref(bank_path, bank_ref) recomputes the bank's sha256 and returns
    (ok, detail) so NC §1.2's "stale bank" stop finally has the evidence to fire.
    file_sha256() is exposed (syllabus_sha256 kept as an alias). No other v1.5
    surface changed.

v1.5 — 2026-08-10 — NOTES-INGEST BASE (Framework_NotesBlueprint v2.0.0). NB is
    now the eager full-corpus ingest step: it reads every sorted-PYQ paper from
    Drive via corpus_io and emits a verified notes_pyq_bank.json that NC and NA
    consume read-only. New here: (1) PYQ_BANK_SCHEMA + bank_new/bank_add_paper/
    bank_add_question/bank_validate/bank_save/bank_load with per-question fields
    incl. verbatim correct_answer + explanation and a stem_figures/
    solution_figures split; (2) subtopic_key() and derive_taxonomy_counts(),
    which compute subtopic-wise pyq_count + recent-3-year counts DIRECTLY from
    the bank so the separate PYQ Analysis doc is no longer a prerequisite
    (owner decision 5i); (3) parse_exam_date_from_filename() — the filename is
    authoritative for exam date (owner decision 2/3); (4) ground-truth answer
    matching: normalize_answer(), nat_precision_from_stem(),
    nat_within_tolerance() (rounding-precision, owner decision 4b) and
    msq_match() (unordered set). Nothing in the v1.4 gate/registry surface
    changed; all v1.4 self-tests are retained verbatim.

v1.4 — 2026-08-08 — THIRD-WAVE CLOSURE; file rewritten whole (no incremental
    patches) after edit-scar corruption. Reviewer designs adopted verbatim:
    (1) Year detection: determiner cue "the" removed (the "the 1700 peak" /
    "the 1857 revolt" shapes are indistinguishable; the cue-less year is the
    reviewer-accepted documented miss) plus a UNIT-SUFFIX VETO — a candidate
    with a unit token (cm, nm, K, g/mol, rpm, Hz, degree-C, mol, Pa, ppm, eV,
    ... incl. cm-1 spellings; bare "s" deliberately absent, it collides with
    the 1990s suffix) within a short following window is a measurement. The
    IR spellings 1600-1800 cm-1 and 1650, 1700, 1750 cm-1 scan clean.
    (2) Flat-token measurement suppression is Km-ONLY (the sole real unit
    collision, kilometre) and contextual: digit-preceded Km followed by
    punctuation/digit/direction/preposition is a distance; "the 2 Kd values",
    "Table 3 Km column", "compare 4 Vmax estimates" flag as symbol mentions.
    (3) The scan_omml_structural self-test fixture uses a defect-carrying
    ATTRIBUTED oMath region and asserts non-empty (previous fixture was
    vacuous). (4) Both reviewer tables are permanent fixtures.

v1.3 — 2026-08-08 — Second wave: positive-evidence years; case-insensitive
    lexicon (NAT exact-case by design); blueprint schema 1.1 + migration;
    first (too-broad) measurement suppression.
v1.2 — 2026-08-08 — density_gate unknown-tier finding; attribute-tolerant
    oMath matching; self_test() added per CLAUDE.md engine rule.
v1.1 — 2026-08-08 — Refinement gates: colour map, PROSE_BAN, math scans,
    type canonicalisation, registry 1.1 migration.
v1.0 — 2026-08-08 — Initial release.
"""
import copy, hashlib, json, os, re, zipfile
import syllabus_provenance
from datetime import datetime, timezone

# ---------------------------------------------------------------- constants
ROLES = ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
STATES = ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
TIERS = ("TIER-1", "TIER-2", "TIER-3")

BULLET_TARGET_WORDS = 20
BULLET_HARD_CAP_WORDS = 25
TIER_PAGE_BANDS = {"TIER-1": (6, 15), "TIER-2": (4, 8), "TIER-3": (2, 5)}

# v2.6: G-12 concept-spread clamp. concept_tags are free-ish text, so the
# distinct-tag count is a PROXY for the tested-concept count — two tags can
# name one concept. The ceiling keeps that noise from over-demanding sections
# a unit cannot honestly carry; it is the single tuning knob of the coverage
# contract and lives HERE so specs defer to it instead of restating numbers.
COVERAGE_CONCEPT_CEILING = 6

# v2.12: THE RECALL CONTRACT constants (GAP-2026-09-01-RECALL-CONTRACT). The
# engine is the SINGLE AUTHORITY; Framework_NotesCreate §4 B7a and
# Framework_NotesAudit §5 G-14 defer to these names and restate no number.
RECALL_CORE_PER_CONCEPT = 1          # exactly one core Recall per concept section
RECALL_CUMULATIVE_DIVISOR = 3        # cumulative = ceil(core / divisor) ...
RECALL_CUMULATIVE_FLOOR = 2          # ... but never fewer than this when an earlier subtopic exists
RECALL_NEAR_MISS_MIN = 1             # >= 1 discrimination item
RECALL_MULTI_CONCEPT_MIN_AXIOMS = 2  # a multi-concept Recall combines >= this many concepts (difficulty_obs.axiom_concepts)
RECALL_CEILING = 15                  # hard ceiling on the whole Recall set
RECALL_MIN_PYQ_FOR_TAG_BAND = 3      # a concept tag needs this many PYQs to set its own band
RECALL_EXAM_MIX_TOLERANCE = 1        # ± items per band against the exam's measured mix
RECALL_CLONE_JACCARD = 0.6           # stem content-token overlap at/above which a Recall clones an Example
RECALL_NEUTRAL_BAND_INDEX = 1        # the middle label when no evidence exists anywhere
DIFFICULTY_LABELS_DEFAULT = ("Easy", "Medium", "Hard")
# bank `complexity` is a free-text human tag from PYQPrepare; these aliases
# map it onto the exam's 3-label vocabulary by POSITION (0 = bottom band).
COMPLEXITY_ALIASES = {
    0: ("easy", "simple", "e", "low", "basic", "l1", "1"),
    1: ("medium", "moderate", "m", "mid", "average", "l2", "2"),
    2: ("hard", "difficult", "tough", "h", "high", "l3", "3"),
}
RECALL_BASES = ("concept", "partner", "subtopic", "topic", "exam", "neutral")
RECALL_SCOPES = ("core", "cumulative")

# v2.3: the specs now cite 2.1 (Framework_NotesAudit v3.0.0 /
# Framework_NotesCreate v2.3.0), so the engine emits it. P1 deliberately held
# this back for one release: an engine emitting a schema string its own specs
# do not name is precisely the drift the SPEC-LOCK block at the foot of this
# file exists to catch.
REGISTRY_SCHEMA = "notes-registry/2.1"
REGISTRY_SCHEMAS_ACCEPTED = ("notes-registry/1.0", "notes-registry/1.1",
                             "notes-registry/2.0", "notes-registry/2.1")
BLUEPRINT_SCHEMA = "notes-blueprint/2.0"
BLUEPRINT_SCHEMAS_ACCEPTED = ("notes-blueprint/1.0", "notes-blueprint/1.1",
                              "notes-blueprint/1.2", "notes-blueprint/2.0")

# ── v2.11 FIGURE PALETTE (GAP-2026-08-30-NOTES-FIGURE-CONTRACT) ──────────────
# Pinned COPY of figural_core's figure constants (P1 2026.08.29.1). The Notes
# route does not load figural_core; equality is enforced by the SPEC-LOCK
# tripwire below and by the self-test's dynamic cross-check. Change ONLY by
# changing figural_core first, then re-pinning here in the same release.
FIGURE_PALETTE = {
    "okabe_ito": ["#0072B2", "#D55E00", "#009E73", "#CC79A7",
                  "#E69F00", "#56B4E9", "#F0E442", "#000000"],
    "line_ink": ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#000000"],
    "text_tier": {"#0072B2": "#0072B2", "#D55E00": "#C25604",
                  "#009E73": "#158663", "#CC79A7": "#AB5D89",
                  "#000000": "#000000"},
    "fills": ["#56B4E9", "#E69F00", "#F0E442", "#A6DDCE", "#EDD0E0"],
    "hatches": ["", "//", "..", "xx", "\\\\"],
    "linestyles": ["-", "--", "-.", ":"],
    "markers": ["o", "s", "^", "D"],
    "series_cap": 4,
    "highlight": "#0072B2",
    "atom_palette": {6: (0.0, 0.0, 0.0), 1: (0.0, 0.0, 0.0),
                     7: (0.0, 0.447, 0.698), 8: (0.761, 0.337, 0.016),
                     9: (0.082, 0.525, 0.388), 17: (0.082, 0.525, 0.388),
                     35: (0.082, 0.525, 0.388), 53: (0.082, 0.525, 0.388)},
    "colormap": "viridis",
}
FIGURE_DPI = 300
# Mind-map (B8) level fills: L1 sky, L2 orange, L3 yellow — fill hues only,
# black labels (>= 9:1 on every fill), dark edge always.
MINDMAP_LEVEL_FILLS = {"L1": 0, "L2": 1, "L3": 2}


def figure_text_ink(hue):
    """TEXT-tier value of a palette hue (F-4a): use for EVERY coloured label
    inside a notes figure. Black aliases normalise; an unknown hue returns
    itself (the author then owns its contrast)."""
    h = str(hue).strip().upper()
    if h in ("K", "BLACK"):
        h = "#000000"
    return FIGURE_PALETTE["text_tier"].get(h, h)


def figure_fill_style(k, edge="#000000"):
    """Fill k of a notes figure (F-4a): facecolor from FIGURE_PALETTE fills,
    dark edge ALWAYS, hatch k as the greyscale channel."""
    k = int(k)
    fills, hatches = FIGURE_PALETTE["fills"], FIGURE_PALETTE["hatches"]
    if k < 0 or k >= len(fills):
        raise ValueError(f"figure_fill_style: fill index {k} outside 0..{len(fills) - 1}")
    return {"facecolor": fills[k], "edgecolor": edge,
            "hatch": hatches[k % len(hatches)], "linewidth": 1.0}


def figure_structure_png(smiles, path, width_in=4.0, highlight_bonds=(),
                         highlight_atoms=(), px=(1200, 864)):
    """Render a molecular structure for a notes figure with the PINNED atom
    palette (never rdkit's default) at FIGURE_DPI for width_in. Returns the
    canonical SMILES (F-4a proof, like §6A-5) or raises ValueError. rdkit
    absent -> ValueError('rdkit_unavailable'): the caller records it and the
    figure is omitted (NC §6 F-4a: never a library-default render)."""
    try:
        from rdkit import Chem
        from rdkit.Chem.Draw import rdMolDraw2D
    except Exception:
        raise ValueError("rdkit_unavailable")
    if not (float(width_in) > 0):
        raise ValueError(f"figure_structure_png: width_in must be > 0, got {width_in!r}")
    mol = Chem.MolFromSmiles(str(smiles or "").strip())
    if mol is None or mol.GetNumAtoms() == 0:      # '' parses to an EMPTY mol
        raise ValueError(f"figure_structure_png: unparseable or empty SMILES {smiles!r}")
    d = rdMolDraw2D.MolDraw2DCairo(int(px[0]), int(px[1]))
    o = d.drawOptions()
    pal = FIGURE_PALETTE["atom_palette"]
    if hasattr(o, "updateAtomPalette"):
        o.updateAtomPalette({int(k): tuple(v) for k, v in pal.items()})
        missing = {a.GetAtomicNum() for a in mol.GetAtoms()} - set(pal)
        if missing:
            o.updateAtomPalette({int(k): (0.0, 0.0, 0.0) for k in missing})
    elif hasattr(o, "useBWAtomPalette"):
        o.useBWAtomPalette()
    hl_b = [int(i) for i in (highlight_bonds or ())]
    n_at, n_bd = mol.GetNumAtoms(), mol.GetNumBonds()
    for i in hl_b:
        if not (0 <= i < n_bd):
            raise ValueError(f"figure_structure_png: highlight_bonds index {i} outside 0..{n_bd - 1}")
    hl_a = []
    for i in (highlight_atoms or ()):
        if not (0 <= int(i) < n_at):
            raise ValueError(f"figure_structure_png: highlight_atoms index {i} outside 0..{n_at - 1}")
        a = mol.GetAtomWithIdx(int(i))
        if a.GetSymbol() == "C" and not a.GetFormalCharge():
            hl_a.append(int(i))
        else:                       # labelled atom: accent its bonds, never its symbol
            hl_b += [b.GetIdx() for b in a.GetBonds() if b.GetIdx() not in hl_b]
    if hl_a or hl_b:
        hh = FIGURE_PALETTE["highlight"]
        rgb = tuple(int(hh[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
        if hasattr(o, "setHighlightColour"):
            o.setHighlightColour(rgb + (1.0,))
        if hasattr(o, "highlightBondWidthMultiplier"):
            o.highlightBondWidthMultiplier = 6
    rdMolDraw2D.PrepareAndDrawMolecule(d, mol, highlightAtoms=hl_a, highlightBonds=hl_b)
    d.FinishDrawing()
    from PIL import Image
    import io as _io
    im = Image.open(_io.BytesIO(d.GetDrawingText())).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    out = bg.convert("RGB")
    # resample so the file is FIGURE_DPI at width_in (F-4a)
    target_w = int(round(width_in * FIGURE_DPI))
    if out.size[0] != target_w:
        out = out.resize((target_w, int(round(out.size[1] * target_w / out.size[0]))),
                         Image.LANCZOS)
    out.save(path, dpi=(FIGURE_DPI, FIGURE_DPI))
    return Chem.MolToSmiles(mol)


LEVEL_COLORS = {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                "table_header": "44546A"}
BOX_COLORS = {"example": ("2E75B6", "E8F1FA"), "recall": ("2E75B6", "E8F1FA"),
              "key_points": ("2E7D32", "E4F2E4"), "trap": ("C62828", "FBE4E4")}

CANONICAL_TYPES = ("MCQ", "MSQ", "NAT")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- identity
def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# syllabus_sha256 kept as a named alias for existing call sites / clarity.
syllabus_sha256 = file_sha256


def unit_code(exam_code, s_no, t_no, st_no):
    return f"{exam_code}_S{int(s_no)}_T{int(t_no)}_ST{int(st_no):02d}"


def _notes_stem(exam_code, s_no, t_no, st_no, slug):
    """The one place the {unit_code}_{Slug} stem is formed. Every filename
    authority below derives from it, so the sanitisation rule cannot drift
    between the draft, the audited file and the delivered file.

    v2.4 EMPTY-SLUG FALLBACK. The sanitiser maps every non-alphanumeric run to
    "_", so a slug with no ASCII alphanumerics at all — Devanagari, Tamil,
    Bengali, or pure punctuation — sanitised to "" and produced a filename
    like EX_S1_T1_ST01__Final.docx. Two different units in the same topic
    would then write the SAME filename and one would silently overwrite the
    other. Since sids are opaque to Notes and the framework serves 200+ Indian
    exams, that is a realistic input. The fallback is a short hash of the RAW
    slug: deterministic across runs, collision-free, and never reached for an
    ASCII slug — so every filename that worked before is byte-identical.
    """
    raw = slug
    slug = re.sub(r"[^A-Za-z0-9]+", "_", slug).strip("_")
    if not slug:
        slug = "u" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]
    return f"{unit_code(exam_code, s_no, t_no, st_no)}_{slug}"


def notes_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesCreate F-1 — the NC DRAFT filename."""
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + ".docx"


def notes_final_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesAudit — the AUDITED, student-ready filename.

    v2.2. NA emits one file in every outcome and it always carries this name,
    so an operator on a phone can never confuse NC's draft with NA's certified
    output. The stem is shared with notes_filename, so the two can never
    disagree about sanitisation.
    """
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + "_Final.docx"


def notes_deliver_filename(exam_code, s_no, t_no, st_no, slug):
    """Framework_NotesDeliver — the portal-formatted delivery filename."""
    return _notes_stem(exam_code, s_no, t_no, st_no, slug) + "_Deliver.docx"


def docx_ref_for(path):
    """A staleness/provenance ref over a .docx, mirroring bank_ref and
    taxonomy_ref. Stored by NC as draft_ref and by NA as final_ref."""
    return {"filename": os.path.basename(path),
            "sha256": file_sha256(path),
            "bytes": os.path.getsize(path),
            "generated": _now()}


def verify_docx_ref(path, ref, expected_filename=None):
    """Returns (ok, kind, detail). kind is one of:
        "ok" | "missing_ref" | "not_found" | "filename" | "sha256"

    The kinds are reported SEPARATELY on purpose. A filename mismatch almost
    always means the wrong unit's file was attached to the trigger — a
    different defect, with a different remedy, from a sha256 mismatch, which
    means the right file was attached but its bytes changed since the
    producing step wrote it (a hand-edit in between).
    """
    if expected_filename and os.path.basename(path) != expected_filename:
        return (False, "filename",
                f"attached file is {os.path.basename(path)!r} but this unit's "
                f"filename is {expected_filename!r} — the wrong unit's "
                f"document appears to be attached.")
    if not ref or not ref.get("sha256"):
        return (False, "missing_ref",
                "no reference recorded for this document by the producing "
                "step — re-run it so the reference exists.")
    if not os.path.exists(path):
        return (False, "not_found", f"file not found at {path}.")
    actual = file_sha256(path)
    if actual != ref["sha256"]:
        return (False, "sha256",
                f"the recorded document is sha256 {ref['sha256'][:12]}… but "
                f"the file present is {actual[:12]}… — it was modified after "
                f"the producing step wrote it.")
    return (True, "ok", "document matches the recorded reference.")


# ---------------------------------------------------------------- roles/tiers
def assign_role(in_syllabus, pyq_count, is_bridge, recent3_count):
    """Framework_NotesBlueprint rules. Returns role or None (=excluded)."""
    if is_bridge:
        return "BRIDGE"
    if in_syllabus:
        return "PYQ_WEIGHTED" if pyq_count >= 3 else "COVERAGE"
    return "EVIDENCE_ADDED" if recent3_count >= 2 else None


def assign_tier(role, pyq_count):
    if role == "PYQ_WEIGHTED":
        return "TIER-1" if pyq_count >= 15 else "TIER-2"
    if role == "EVIDENCE_ADDED":
        return "TIER-2"
    return "TIER-3"


def normalize_types(raw_values):
    """Range-tab Type values -> ordered unique canonical set."""
    out = []
    for v in raw_values:
        c = re.sub(r"[^A-Z]", "", str(v or "").upper())
        for k in CANONICAL_TYPES:
            if k in c and k not in out:
                out.append(k)
    return out


# ---------------------------------------------------------------- registry
def registry_init(exam_code, syllabus_hash, level, units, taxonomy_ref=None):
    """v2.0: units are KEYED BY sid (the verbatim Step-5 Sub Topic Id) when the
    unit carries one; a legacy unit without a sid keys by unit_code so 1.x-shaped
    callers still work. Unit records carry the manifest triple (section, topic,
    name==display_name verbatim) plus the DERIVED unit_code and slug; the
    registry carries taxonomy_ref (verify_taxonomy_ref staleness link)."""
    reg = {"schema": REGISTRY_SCHEMA, "exam_code": exam_code,
           "syllabus_sha256": syllabus_hash, "exam_level": level,
           "allowed_question_types": None, "taxonomy_ref": taxonomy_ref,
           "created": _now(), "updated": _now(), "units": {}}
    for u in units:
        key = u.get("sid") or u["unit_code"]
        reg["units"][key] = {
            "sid": u.get("sid"), "name": u["name"],
            "section": u.get("section"), "topic": u.get("topic"),
            "unit_code": u.get("unit_code"), "slug": u.get("slug"),
            "role": u["role"], "tier": u["tier"],
            "pyq_count": u.get("pyq_count", 0),
            "provenance": u.get("provenance", "syllabus"),
            "seq_in_topic": u.get("seq_in_topic"),
            "prose_ban_exemptions": u.get("prose_ban_exemptions", []),
            "state": "BLUEPRINTED", "stale": False, "notes_version": None,
            "audit": None, "artifacts": {},
            # v2.3 (notes-registry/2.1)
            "draft_ref": None, "final_ref": None, "audit_summary": None,
            "history": [{"at": _now(), "event": "BLUEPRINTED"}]}
    return reg


def registry_load(path):
    """Accept registry schema 1.0/1.1/2.0; migrate older ones IN PLACE to the
    2.0 shape (read-only migration: a 1.x unit gains sid=None and keeps its
    unit_code key — sid-keyed identity requires a re-blueprint at NB, which is
    cheap because the ingested bank is untouched)."""
    reg = json.load(open(path, encoding="utf-8"))
    if reg.get("schema") not in REGISTRY_SCHEMAS_ACCEPTED:
        raise ValueError(f"registry schema mismatch: {reg.get('schema')}")
    if reg["schema"] not in (REGISTRY_SCHEMA, "notes-registry/2.1"):
        reg["schema"] = REGISTRY_SCHEMA
        reg.setdefault("allowed_question_types", None)
        reg.setdefault("taxonomy_ref", None)
        for key, u in reg.get("units", {}).items():
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
            u.setdefault("sid", None)
            u.setdefault("section", None)
            u.setdefault("topic", None)
            u.setdefault("slug", None)
            u.setdefault("unit_code", key)
    # v2.2 (additive, applied to EVERY accepted schema): the 2.1 per-unit
    # fields are defaulted on load, so a P2 step reads a uniform shape whether
    # the registry on disk was written by a 1.x, 2.0 or 2.1 producer.
    for u in reg.get("units", {}).values():
        u.setdefault("draft_ref", None)
        u.setdefault("final_ref", None)
        u.setdefault("audit_summary", None)
    return reg


def registry_save(reg, path):
    reg["updated"] = _now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def transition(reg, unit_code_, new_state, **extra):
    order = {s: i for i, s in enumerate(STATES)}
    u = reg["units"][unit_code_]
    cur = u["state"]
    ok = (new_state in STATES
          and (order[new_state] == order[cur] + 1
               or (cur == "DELIVERED" and new_state == "AUDITED_PASS")
               or (cur == "AUDITED_PASS" and new_state == "DRAFTED")))
    if not ok:
        raise ValueError(f"illegal transition {cur} -> {new_state} for {unit_code_}")
    u["state"] = new_state
    u.update(extra)
    u["history"].append({"at": _now(), "event": new_state, **extra})
    return u


REGISTRY_CARRY_FIELDS = ("state", "notes_version", "audit", "artifacts", "history",
                         "draft_ref", "final_ref", "audit_summary", "recall_contract")


def registry_carry_over(new_reg, prior_reg):
    """v2.12 — THE ONE carry-over list for an NB re-run (Framework_NotesBlueprint
    §7). registry_init writes every unit BLUEPRINTED with the downstream fields
    None; before this function the §7 promise "existing unit states preserved"
    had no engine behind it, so a re-blueprint silently reset draft_ref /
    final_ref / audit_summary — and would have reset recall_contract, leaving
    G-14 dormant on a unit NC had already drafted. For every unit of new_reg
    whose sid key also exists in prior_reg, copy REGISTRY_CARRY_FIELDS from the
    prior record (a None prior value never overwrites a fresh default). Units
    new to the manifest keep their fresh BLUEPRINTED record; prior units absent
    from new_reg are NOT copied (NB §7 ORPHANED — reported, never re-created
    here). Returns the sorted list of carried sid keys. Pure: no I/O."""
    carried = []
    prior_units = (prior_reg or {}).get("units") or {}
    for key, u in (new_reg.get("units") or {}).items():
        pu = prior_units.get(key)
        if not isinstance(pu, dict):
            continue
        for f in REGISTRY_CARRY_FIELDS:
            if pu.get(f) is not None:
                u[f] = copy.deepcopy(pu[f])
        carried.append(key)
    return sorted(carried)


def load_blueprint(path):
    """Accept blueprint schema 1.0/1.1/1.2/2.0; migrate older ones in place so
    consumers can rely on the 2.0 shape (symmetric with registry_load): a 1.x
    unit gains sid/section/topic = None and taxonomy_ref = None."""
    bp = json.load(open(path, encoding="utf-8"))
    if bp.get("schema") not in BLUEPRINT_SCHEMAS_ACCEPTED:
        raise ValueError(f"blueprint schema mismatch: {bp.get('schema')}")
    if bp["schema"] != BLUEPRINT_SCHEMA:
        bp["schema"] = BLUEPRINT_SCHEMA
        bp.setdefault("allowed_question_types", [])
        bp.setdefault("bank_ref", None)
        bp.setdefault("taxonomy_ref", None)
        for u in bp.get("units", []):
            u.setdefault("seq_in_topic", None)
            u.setdefault("prose_ban_exemptions", [])
            u.setdefault("sid", None)
            u.setdefault("section", None)
            u.setdefault("topic", None)
    return bp


def verify_bank_ref(bank_path, bank_ref):
    """Fix 1 (deployment review): the staleness link NC §1.2 needs. Returns
    (ok, detail). A blueprint with no bank_ref predates the bank and must be
    rebuilt at NB. A bank_ref whose sha256 does not match the bank on disk means
    the blueprint was built from a DIFFERENT bank than the one present — the
    exact silent-mismatch this catches."""
    if not bank_ref or not bank_ref.get("sha256"):
        return (False, "blueprint carries no bank_ref — rebuild it at NB (the "
                       "blueprint predates the current bank).")
    if not os.path.exists(bank_path):
        return (False, f"notes_pyq_bank.json not found at {bank_path}.")
    actual = file_sha256(bank_path)
    if actual != bank_ref["sha256"]:
        return (False, "STALE BANK: the blueprint was built from bank sha256 "
                f"{bank_ref['sha256'][:12]}… but notes_pyq_bank.json is now "
                f"{actual[:12]}…. Re-run NB so blueprint and bank agree.")
    return (True, "bank_ref matches the bank on disk.")


# ================================================================ TAXONOMY
# v2.0 — the Step-5 subtopic manifest is the SINGLE SOURCE OF TRUTH for the
# Notes unit vocabulary (owner decision 2026-08-10; mirrors the Mock pipeline's
# Cross-Step Subtopic Contract). Notes NEVER mints a subtopic id. Step 5 is
# untouched: everything below CONSUMES [ExamCode]_subtopic_manifest.json.

def load_subtopic_manifest(path, expected_exam_code=None):
    """Load + structurally validate the Step-5 manifest. HARD STOP (ValueError)
    on: unreadable/shapeless file, empty subtopics, an entry missing
    display_name/section/topic, or an exam_code mismatch (the wrong exam's
    manifest in project Files must never be consumed silently). The Step-5 id
    recipe is NOT re-validated here — the recipe is Step 5's contract and may
    evolve; Notes treats each sid as an opaque verbatim key."""
    m = json.load(open(path, encoding="utf-8"))
    subs = m.get("subtopics")
    if not isinstance(subs, dict) or not subs:
        raise ValueError(f"subtopic manifest at {path} has no 'subtopics' map")
    for sid, v in subs.items():
        if not sid or not isinstance(sid, str):
            raise ValueError(f"subtopic manifest has an empty/non-string id: {sid!r}")
        missing = [k for k in ("display_name", "section", "topic")
                   if not (isinstance(v, dict) and v.get(k))]
        if missing:
            raise ValueError(f"manifest entry {sid!r} missing {missing}")
    mc = m.get("exam_code")
    if expected_exam_code and mc != expected_exam_code:
        raise ValueError(
            "HARD STOP: manifest exam_code %r does not match this project's "
            "exam_code %r — the wrong exam's %s is in project Files."
            % (mc, expected_exam_code, os.path.basename(str(path))))
    return m


def taxonomy_ref_for(manifest_path):
    """The {path, sha256, subtopics, generated} reference embedded in the
    blueprint + registry — the same staleness idiom as bank_ref. sha256 is over
    the manifest bytes on disk, so a re-uploaded/re-generated manifest is
    detectable (verify_taxonomy_ref) and flips units STALE at NB §7."""
    m = load_subtopic_manifest(manifest_path)
    return {"path": manifest_path, "sha256": file_sha256(manifest_path),
            "subtopics": len(m["subtopics"]), "generated": _now()}


def verify_taxonomy_ref(manifest_path, taxonomy_ref):
    """Mirror of verify_bank_ref for the subtopic manifest. Returns (ok, detail).
    A blueprint/registry with no taxonomy_ref predates the taxonomy-consumer
    architecture and must be rebuilt at NB. A sha256 mismatch means the manifest
    on disk is not the one the blueprint was built from."""
    if not taxonomy_ref or not taxonomy_ref.get("sha256"):
        return (False, "no taxonomy_ref — rebuild at NB (the blueprint predates "
                       "the taxonomy-consumer architecture).")
    if not os.path.exists(manifest_path):
        return (False, f"subtopic manifest not found at {manifest_path}.")
    actual = file_sha256(manifest_path)
    if actual != taxonomy_ref["sha256"]:
        return (False, "STALE TAXONOMY: the blueprint was built from manifest "
                f"sha256 {taxonomy_ref['sha256'][:12]}… but the manifest on disk "
                f"is {actual[:12]}…. Re-run NB so blueprint and taxonomy agree.")
    return (True, "taxonomy_ref matches the manifest on disk.")


def sid_slug(sid):
    """The sid's final dot-component — the filesystem-safe subtopic slug used
    as the F-1 filename slug (S/T/ST numbers already encode section + topic)."""
    return str(sid).rsplit(".", 1)[-1]


def assign_numbering(manifest, prior=None):
    """Derive per-sid S/T/ST numbers from MANIFEST ROW ORDER, preserving any
    prior assignment VERBATIM (persisted numbering, owner decision 2026-08-10):
    a Step-5 re-run that inserts or reorders subtopics never renumbers an
    already-assigned unit — delivered filenames and printed title numbers stay
    stable. New sections/topics/subtopics take the next free number in their
    scope. prior: {sid: {"s_no","t_no","st_no"}} (a prior registry's map; sids
    no longer in the manifest keep their numbers and are the caller's ORPHANED
    report). Returns {sid: {"s_no","t_no","st_no"}} covering the union."""
    subs = manifest["subtopics"]
    out = {}
    sec_no, top_no, st_used = {}, {}, {}
    for sid, num in (prior or {}).items():
        s, t, st = int(num["s_no"]), int(num["t_no"]), int(num["st_no"])
        out[sid] = {"s_no": s, "t_no": t, "st_no": st}
        v = subs.get(sid)
        if v:                       # anchor the section/topic numbers it proves
            sec_no.setdefault(v["section"], s)
            top_no.setdefault((v["section"], v["topic"]), t)
        st_used[(s, t)] = max(st_used.get((s, t), 0), st)
    next_sec = max(sec_no.values(), default=0)
    next_top = {}
    for (sec, _t), t in top_no.items():
        next_top[sec] = max(next_top.get(sec, 0), t)
    for sid, v in subs.items():     # manifest insertion order == taxonomy order
        if sid in out:
            continue
        sec, top = v["section"], v["topic"]
        if sec not in sec_no:
            next_sec += 1
            sec_no[sec] = next_sec
        s = sec_no[sec]
        if (sec, top) not in top_no:
            next_top[sec] = next_top.get(sec, 0) + 1
            top_no[(sec, top)] = next_top[sec]
        t = top_no[(sec, top)]
        st_used[(s, t)] = st_used.get((s, t), 0) + 1
        out[sid] = {"s_no": s, "t_no": t, "st_no": st_used[(s, t)]}
    return out


def resolve_unit(units_by_sid, operator_input):
    """Three-tier operator-input resolution (shared by NC/NA/ND; the operator
    copies a cell from [ExamCode]_taxonomy.xlsx — Sub Topic Id, a
    'Subject::Topic::Sub Topic Name' scope, or the bare Sub Topic Name).
    units_by_sid: {sid: {..., 'name'/'display_name', 'section', 'topic'}}.
    Returns {'status': 'ok'|'ambiguous'|'none', 'sid', 'via', 'matches',
    'suggestions', 'detail'}. NEVER fuzzy-picks: multiple bare-name hits are
    returned for the operator to choose; zero hits return nearest-name
    suggestions and stop."""
    def _name(u):
        return u.get("display_name") or u.get("name") or ""
    n = syllabus_provenance.norm
    t = str(operator_input or "").strip().strip('"').strip("'").strip()
    if not t:
        return {"status": "none", "sid": None, "via": None, "matches": [],
                "suggestions": [], "detail": "empty unit reference"}
    if t in units_by_sid:
        return {"status": "ok", "sid": t, "via": "sid", "matches": [t],
                "suggestions": [], "detail": "exact Sub Topic Id"}
    if "::" in t:
        parts = [p.strip() for p in t.split("::")]
        if len(parts) != 3:
            return {"status": "none", "sid": None, "via": "scope", "matches": [],
                    "suggestions": [],
                    "detail": "a scope must be Subject::Topic::Sub Topic Name "
                              "(3 parts) — got %d part(s)" % len(parts)}
        want = tuple(n(p) for p in parts)
        hits = [sid for sid, u in units_by_sid.items()
                if (n(u.get("section")), n(u.get("topic")), n(_name(u))) == want]
        if len(hits) == 1:
            return {"status": "ok", "sid": hits[0], "via": "scope",
                    "matches": hits, "suggestions": [], "detail": "scope match"}
        return {"status": "ambiguous" if hits else "none", "sid": None,
                "via": "scope", "matches": hits, "suggestions": [],
                "detail": "scope matched %d unit(s)" % len(hits)}
    want = n(t)
    hits = [sid for sid, u in units_by_sid.items() if n(_name(u)) == want]
    if len(hits) == 1:
        return {"status": "ok", "sid": hits[0], "via": "name", "matches": hits,
                "suggestions": [], "detail": "unique Sub Topic Name"}
    if hits:
        return {"status": "ambiguous", "sid": None, "via": "name",
                "matches": hits, "suggestions": [],
                "detail": "Sub Topic Name matches %d units — re-trigger with "
                          "the Subject::Topic::Sub Topic Name scope or the "
                          "Sub Topic Id" % len(hits)}
    sugg = [sid for sid, u in units_by_sid.items()
            if want and (want in n(_name(u)) or n(_name(u)) in want)][:5]
    return {"status": "none", "sid": None, "via": "name", "matches": [],
            "suggestions": sugg,
            "detail": "no unit named %r — copy the exact Sub Topic Name (or "
                      "Sub Topic Id) from [ExamCode]_taxonomy.xlsx" % t}


# ---------------------------------------------------------------- docx text
def _docx_xml(path):
    return zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")


def document_text(docx_path, sep="\n"):
    """PUBLIC single authority for the plain-text view of a .docx.

    ELEMENT BOUNDARIES ARE PRESERVED, and that is the whole point:
      - runs INSIDE one paragraph are concatenated with NO separator, because
        a run break is a formatting artefact, not a text boundary. Word may
        split "2.10" into the runs "2." and "10" at any time;
      - paragraphs (including those inside table cells) are joined with `sep`,
        because a paragraph break IS a text boundary.
    Stripping tags with a bare re.sub(r"<[^>]+>", "", xml) does neither: it
    welds the last character of one paragraph to the first of the next, so
    "Answer: 1" followed by the heading "2.10 MIND MAP" reads "12.10" and any
    numeric scan is wrong. EVERY gate that scans document text must call this.

    m:t (OMML) is deliberately EXCLUDED — this is the plain-text layer. A gate
    that needs the maths reads the oMath regions directly (scan_omml_*).
    """
    xml = _docx_xml(docx_path)
    paras = []
    for para in re.findall(r"<w:p\b.*?</w:p>", xml, re.S):
        paras.append("".join(
            re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", para, re.S)))
    return sep.join(paras)


def _document_text(docx_path):
    # Retained name for the existing prose/token scanners. " " keeps their
    # historic run-joining behaviour for substring bans; document_text() is
    # the boundary-preserving form any NEW scanner must use.
    return document_text(docx_path, sep=" ")


# ---------------------------------------------------------------- density
# The glyph notes_docx uses to render a bullet. A document built by the shared
# builder has no <w:numPr> anywhere, so recognising this is what keeps G-1
# alive (v2.4 defect A).
BULLET_GLYPH = "\u2022"


def bullet_word_counts(docx_path):
    """Word counts for every bullet in the document, for gate G-1 / rule D-1.

    v2.4: counts a paragraph as a bullet if it carries <w:numPr> (a Word list
    paragraph) OR its text begins with the bullet glyph. Before this, only
    <w:numPr> counted — and notes_docx renders bullets as a literal glyph run,
    so this returned [] for EVERY document the shared builder produces and the
    density gate passed 60-word bullets. The regex walks all of document.xml,
    so bullets inside table cells (KEY POINTS, TRAP) are included, which is
    where most box bullets live.
    """
    xml = _docx_xml(docx_path)
    counts = []
    for para in re.findall(r"<w:p\b.*?</w:p>", xml, re.S):
        text = "".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", para, re.S))
        # "<w:numPr" not "<w:numPr>": Word writes a container
        # <w:numPr>...</w:numPr>, but a self-closing <w:numPr/> is equally
        # valid OOXML and the old literal missed it.
        is_list = "<w:numPr" in para
        is_glyph = text.lstrip().startswith(BULLET_GLYPH)
        if not (is_list or is_glyph):
            continue
        if is_glyph:
            text = text.lstrip()[len(BULLET_GLYPH):]
        words = len(re.findall(r"\S+", text))
        if words:
            counts.append(words)
    return counts


def density_gate(docx_path, tier, page_count):
    """NA gate G-1. Unknown tier is a finding, never a crash."""
    findings = []
    for w in bullet_word_counts(docx_path):
        if w > BULLET_HARD_CAP_WORDS:
            findings.append(f"bullet exceeds hard cap: {w} words")
    band = TIER_PAGE_BANDS.get(tier)
    if band is None:
        findings.append(f"unknown tier: {tier!r}")
    else:
        lo, hi = band
        if not (lo <= page_count <= hi):
            findings.append(f"page count {page_count} outside {tier} band {lo}-{hi}")
    return (not findings, findings)


# ---------------------------------------------------------------- prose bans
# Word-like patterns are case-insensitive. NAT is exact-case BY DESIGN:
# lowercase "nat" is a plausible fragment of ordinary text.
PROSE_BAN = [
    (r"(?<![A-Za-z])NAT(?![A-Za-z])", "question-type name NAT", 0),
    (r"(?<![A-Za-z])MCQ(?![A-Za-z])", "question-type name MCQ", re.I),
    (r"(?<![A-Za-z])MSQ(?![A-Za-z])", "question-type name MSQ", re.I),
    (r"(?<![A-Za-z])PYQ", "PYQ token", re.I),
    (r"EXAM\s+LENS", "retired block name", re.I),
    ("[\u2605\u2606]", "star glyph", 0),
    (r"(?m)(?:^|[>\s])Q:\s", "Q: stem prefix", re.I),
    (r"modelled\s+on", "example anchor phrase", re.I),
    (r"examiner", "editorial lead-in", re.I),
]

# Positive-evidence year detection. _YR is 1600-2099. Determiner "the" is
# deliberately NOT a cue ("the 1700 peak" vs "the 1857 revolt" are the same
# shape); the cue-less year is the reviewer-accepted documented miss.
_YR = r"(?:1[6-9]\d\d|20\d\d)"
YEAR_EVIDENCE = [
    r"(?i)(?<![A-Za-z0-9])(?:in|by|since|from|until|till|during|circa|year|"
    r"early|late|mid|pre|post)\s+" + _YR + r"(?!\d)",
    _YR + r"(?:s|\s+(?:AD|CE|BCE|BC))(?![A-Za-z0-9])",
    _YR + r"\s*,\s*" + _YR,
    _YR + r"\s*[\u2013\u2014-]\s*" + _YR,
    _YR + r"\s+Q\d",
]

# Unit-suffix veto: a year-candidate with a unit token in the following
# window is a measurement. Bare "s" deliberately absent (1990s collision).
_UNIT_WINDOW = 26
_UNIT_RE = re.compile(
    "(?<![A-Za-z])"
    "(?:cm|mm|nm|\u00b5m|um|km|kg|mg|\u00b5g|g/mol|mol|K|\u00b0C|\u00b0F"
    "|Hz|kHz|MHz|GHz|rpm|Pa|kPa|MPa|ppm|eV|kJ|kcal|cal|mL|\u00b5L|L|g|min|h)"
    "(?:-1)?(?![A-Za-z])")


def _year_hit(text):
    for p in YEAR_EVIDENCE:
        for m in re.finditer(p, text):
            window = text[m.start():m.end() + _UNIT_WINDOW]
            if not _UNIT_RE.search(window):
                return True
    return False


def scan_prose_bans(docx_path, exemptions=()):
    """NA gate G-4. Returns findings (empty == pass)."""
    text = _document_text(docx_path)
    findings = []
    for pat, label, flags in PROSE_BAN:
        if label in exemptions:
            continue
        if re.search(pat, text, flags):
            findings.append(label)
    if "year reference" not in exemptions and _year_hit(text):
        findings.append("year reference")
    return findings


# ---------------------------------------------------------------- math gates
_SCRIPT_CHARS = ("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078"
                 "\u2079\u207b\u2080\u2081\u2082\u2083\u00bd")
MATH_TOKEN_RES = [r"(?<![A-Za-z])" + t + r"(?![A-Za-z])" for t in
                  ("Vmax", "Km", "Ki", "Kd", "Keq", "kcat", "kd", "Et")] + \
                 [r"pKa(?![A-Za-z])", "[" + _SCRIPT_CHARS + "]"]

_KM_DIST_FOLLOW = re.compile(
    r"^\s*(?:$|[.,;:)\]]|\d|north|south|east|west|away|apart|ahead|along|"
    r"across|downstream|upstream|offshore|long|wide|deep|high|per|from|to|"
    r"in|at|of|off|on|over|beyond|before|behind)", re.I)


def scan_flat_math_tokens(docx_path):
    """NA gate G-2c: no un-styled math token in any plain text run.
    Suppression is Km-ONLY (kilometre collision) and contextual:
    digit-preceded Km followed by punctuation/digit/direction/preposition is
    a distance. Digit-preceded Kd/Vmax/etc. remain symbol mentions."""
    text = _document_text(docx_path)
    findings = []
    for p in MATH_TOKEN_RES:
        for m in re.finditer(p, text):
            pre = text[max(0, m.start() - 2):m.start()]
            post = text[m.end():m.end() + 14]
            if ("Km" in p and re.search(r"\d\s?$", pre)
                    and _KM_DIST_FOLLOW.search(post)):
                continue
            findings.append("flat math token: " + p)
            break
    return findings


def scan_omml_structural(docx_path):
    """NA gate G-2b: no textual exponents or unicode script chars inside any
    oMath region. Attribute-tolerant tag matching."""
    xml = _docx_xml(docx_path)
    joined = "\n".join(re.findall(r"<m:oMath\b[^>]*>.*?</m:oMath>", xml, re.S))
    findings = []
    if "^(" in joined:
        findings.append("textual exponent inside oMath")
    for ch in _SCRIPT_CHARS:
        if ch in joined:
            findings.append("unicode script char inside oMath: %r" % ch)
            break
    return findings


def assert_omml(docx_path, expected_min, required_tokens=()):
    """NA gate G-2a: verify equations STRUCTURALLY (XML), never via
    LibreOffice previews (LO drops OMML silently). Attribute-tolerant."""
    xml = _docx_xml(docx_path)
    maths = re.findall(r"<m:oMath\b[^>]*>.*?</m:oMath>", xml, re.S)
    if len(maths) < expected_min:
        raise AssertionError(f"OMML count {len(maths)} < expected {expected_min}")
    joined = "\n".join(maths)
    missing = [tok for tok in required_tokens if tok not in joined]
    if missing:
        raise AssertionError(f"OMML tokens missing: {missing}")
    return len(maths)


# ================================================================ PYQ BANK
# The bank is NB's ingest artifact (notes_pyq_bank.json). It is a PROJECT
# artifact, not a framework file — its SCHEMA lives here so it is bootstrap-
# verified and unit-testable. NC filters it per subtopic; NA solves against
# its verbatim correct_answer. Both consume it read-only; neither re-reads Drive.
PYQ_BANK_SCHEMA = "notes-pyq-bank/1.2"
PYQ_BANK_SCHEMAS_ACCEPTED = ("notes-pyq-bank/1.0", "notes-pyq-bank/1.1",
                             "notes-pyq-bank/1.2")

BANK_REQUIRED_FIELDS = ("bank_id", "paper_key", "exam_date", "exam_year",
                        "q_no", "type", "subject", "topic", "subtopic", "stem")

_MONTHS = {m: i for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"), 1)}


def parse_exam_date_from_filename(name):
    """Exam date from a sorted-PYQ filename (owner decision 2/3: the filename is
    authoritative and stable). Returns (iso 'YYYY-MM-DD', year int,
    label 'DD-Mon-YYYY') or None. Tolerant of prefixes/suffixes, 'Copy of',
    '(1)', and DD-Mon-YYYY / DDMonYYYY / Mon-YYYY / YYYY-only shapes."""
    stem = re.sub(r"\.(?:docx|doc)$", "", os.path.basename(str(name)), flags=re.I)
    m = re.search(r"(?<!\d)(\d{1,2})[\-_ ]?([A-Za-z]{3,9})[\-_ ]?((?:19|20)\d\d)",
                  stem)
    if m and _MONTHS.get(m.group(2)[:3].lower()):
        d, mon, y = int(m.group(1)), _MONTHS[m.group(2)[:3].lower()], int(m.group(3))
        if 1 <= d <= 31:
            return (f"{y:04d}-{mon:02d}-{d:02d}", y,
                    f"{d:02d}-{m.group(2)[:3].title()}-{y}")
    m = re.search(r"(?<![A-Za-z])([A-Za-z]{3,9})[\-_ ]?((?:19|20)\d\d)", stem)
    if m and _MONTHS.get(m.group(1)[:3].lower()):
        mon, y = _MONTHS[m.group(1)[:3].lower()], int(m.group(2))
        return (f"{y:04d}-{mon:02d}-01", y, f"{m.group(1)[:3].title()}-{y}")
    m = re.search(r"(?<!\d)((?:19|20)\d\d)(?!\d)", stem)
    if m:
        y = int(m.group(1))
        return (f"{y:04d}-01-01", y, str(y))
    return None


def subtopic_key(subject, topic, subtopic):
    """Canonical subtopic identity so bank counts and blueprint units join even
    when the syllabus and the paper header differ only in punctuation or unicode.
    Reuses syllabus_provenance.norm per component (NFKC, dash unification,
    & -> and, casefold, '/' kept as data) — the same normalization the rest of the
    framework's taxonomy joins use — and additionally collapses spaces around '/'
    so 'Optics/Polarization' and 'Optics / Polarization' resolve identically."""
    def n(x):
        return re.sub(r"\s*/\s*", "/", syllabus_provenance.norm(x))
    return f"{n(subject)}|||{n(topic)}|||{n(subtopic)}"


def normalize_answer(qtype, raw):
    """Normalise a doc-declared answer by type (never re-derived; owner
    decision 4). MCQ -> option string ('2'); MSQ -> sorted int list ([1, 3]);
    NAT -> float."""
    t = (qtype or "").upper()
    s = str("" if raw is None else raw).strip()
    if t == "MSQ":
        return sorted({int(x) for x in re.findall(r"\d+", s)})
    if t == "NAT":
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        return float(m.group(0)) if m else None
    m = re.search(r"\d+", s)
    return m.group(0) if m else s


def nat_precision_from_stem(stem):
    """Decimal places a NAT stem asks for (NC B3 requires NAT stems to state
    rounding). Defaults to 2. 'nearest integer' -> 0."""
    s = stem or ""
    if re.search(r"nearest\s+(?:integer|whole)", s, re.I):
        return 0
    m = re.search(r"(?:to|up\s*to|correct\s+to|round(?:ed)?\s+to)\s+(\d+)\s*"
                  r"(?:decimal|dp|place)", s, re.I) \
        or re.search(r"(\d+)\s*decimal\s*place", s, re.I)
    return int(m.group(1)) if m else 2


def nat_within_tolerance(computed, target, precision_decimals=2):
    """Ground-truth NAT match (owner decision 4b): equal after rounding BOTH to
    the stem's stated precision. None on either side is never a match."""
    if computed is None or target is None:
        return False
    p = int(precision_decimals)
    return round(float(computed), p) == round(float(target), p)


def msq_match(computed, target):
    """MSQ ground-truth match: unordered set equality."""
    def norm(x):
        if isinstance(x, (list, tuple, set)):
            return {int(i) for i in x}
        return {int(i) for i in re.findall(r"\d+", str(x))}
    return norm(computed) == norm(target)


def bank_new(exam_code):
    return {"schema": PYQ_BANK_SCHEMA, "exam_code": exam_code,
            "created": _now(), "updated": _now(),
            "papers": [], "questions": []}


def bank_add_paper(bank, paper_key, exam_date, exam_year, filename,
                   n_questions, image_report=None):
    bank["papers"].append({
        "paper_key": paper_key, "exam_date": exam_date,
        "exam_year": int(exam_year), "filename": filename,
        "questions": int(n_questions), "image_report": image_report or {}})


def bank_add_question(bank, rec):
    """Append one validated question. rec keys: the BANK_REQUIRED_FIELDS plus
    optional complexity, options, correct_answer, explanation (verbatim),
    stem_figures, solution_figures, concept_tags, integration_partners.
    stem_figures present -> figure flag True (NC FIGURE dependency; owner
    decision 3 split). integration_partners (v2.7, notes-pyq-bank/1.2,
    OPTIONAL): the OTHER subtopics this question genuinely fuses, each in the
    canonical Subject::Topic::Sub Topic Name scope form — a malformed entry or
    the question's OWN subtopic raises (a fusion needs a partner that is not
    itself)."""
    missing = [k for k in BANK_REQUIRED_FIELDS if rec.get(k) in (None, "")]
    if missing:
        raise ValueError(f"bank question {rec.get('bank_id')!r} missing {missing}")
    t = str(rec["type"]).upper()
    if t not in CANONICAL_TYPES:
        raise ValueError(f"bank question {rec['bank_id']!r} non-canonical type "
                         f"{rec['type']!r}")
    raw_partners = rec.get("integration_partners") or []
    if not isinstance(raw_partners, (list, tuple)):
        raise ValueError(f"bank question {rec['bank_id']!r} integration_partners "
                         f"must be a list of Subject::Topic::Sub Topic Name "
                         f"scope strings")
    own_key = subtopic_key(rec["subject"], rec["topic"], rec["subtopic"])
    partners, seen_keys = [], set()
    for p in raw_partners:
        parts = [x.strip() for x in str(p).split("::")]
        if len(parts) != 3 or not all(parts):
            raise ValueError(
                f"bank question {rec['bank_id']!r} integration partner {p!r} "
                f"is not the Subject::Topic::Sub Topic Name scope form")
        k = subtopic_key(*parts)
        if k == own_key:
            raise ValueError(
                f"bank question {rec['bank_id']!r} names its OWN subtopic as "
                f"an integration partner — a fusion needs a partner that is "
                f"not itself")
        if k not in seen_keys:
            seen_keys.add(k)
            partners.append("::".join(parts))
    q = {"bank_id": rec["bank_id"], "paper_key": rec["paper_key"],
         "exam_date": rec["exam_date"], "exam_year": int(rec["exam_year"]),
         "q_no": rec["q_no"], "type": t, "complexity": rec.get("complexity"),
         "subject": rec["subject"], "topic": rec["topic"],
         "subtopic": rec["subtopic"],
         "subtopic_key": subtopic_key(rec["subject"], rec["topic"], rec["subtopic"]),
         "stem": rec["stem"], "options": list(rec.get("options", [])),
         "correct_answer": rec.get("correct_answer"),
         "explanation": rec.get("explanation", ""),
         "stem_figures": list(rec.get("stem_figures", [])),
         "solution_figures": list(rec.get("solution_figures", [])),
         "figure": bool(rec.get("stem_figures")),
         "concept_tags": list(rec.get("concept_tags", []))}
    if partners:
        q["integration_partners"] = partners
    bank["questions"].append(q)
    return q


def bank_validate(bank):
    if bank.get("schema") not in PYQ_BANK_SCHEMAS_ACCEPTED:
        raise ValueError(f"bank schema mismatch: {bank.get('schema')}")
    ids = [q["bank_id"] for q in bank.get("questions", [])]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        raise ValueError(f"duplicate bank_id(s): {dupes}")
    for q in bank.get("questions", []):
        if str(q.get("type")).upper() not in CANONICAL_TYPES:
            raise ValueError(f"bank_id {q.get('bank_id')!r} bad type {q.get('type')!r}")
    return True


def bank_save(bank, path):
    bank["updated"] = _now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)
    return path


def bank_load(path):
    bank = json.load(open(path, encoding="utf-8"))
    bank_validate(bank)
    # Migrate a pre-1.1 bank: subtopic_key is DERIVED, and older banks stored it
    # under a weaker normalization. Refresh the stored key from the authoritative
    # subject/topic/subtopic so an inspected bank is self-consistent, and stamp the
    # schema. Reads recompute the key regardless (bank_questions_for /
    # derive_taxonomy_counts), so this migration is cosmetic — the drift class is
    # already closed; it just keeps the stored field honest.
    if bank.get("schema") != PYQ_BANK_SCHEMA:
        for q in bank.get("questions", []):
            q["subtopic_key"] = subtopic_key(q.get("subject"), q.get("topic"),
                                             q.get("subtopic"))
        bank["schema"] = PYQ_BANK_SCHEMA
    return bank


def bank_questions_for(bank, subject, topic, subtopic):
    """Every bank question under one subtopic (NC §1 unit filter). Identity is
    RECOMPUTED from each question's stored subject/topic/subtopic — the stored
    subtopic_key is never trusted — so a bank written by an older notes_core with
    a different subtopic_key normalization still joins correctly."""
    k = subtopic_key(subject, topic, subtopic)
    return [q for q in bank["questions"]
            if subtopic_key(q["subject"], q["topic"], q["subtopic"]) == k]


def coverage_target_for(bank, subject, topic, subtopic, allowed_types=()):
    """v2.6 — the unit's COVERAGE CONTRACT, derived entirely from its bank
    slice (G-12's single authority; NC §4 B3a authors to it, NA §5 G-12 gates
    it, so author and gate can never disagree).

    Returns {"required_types", "min_concepts_with_examples", "requires_figure",
    "pyq_count", "distinct_concept_tags"}.

    Design (owner decision, Phase 2): the contract is CONCEPT SPREAD, not an
    example count — N examples on one scenario satisfy any count while
    teaching one thing. min_concepts_with_examples is the number of DISTINCT
    concept sections that must carry at least one Example, from the slice's
    distinct normalized concept_tags clamped to COVERAGE_CONCEPT_CEILING.
    Tags are optional in the bank (bank_add_question defaults them empty), so
    a tagless slice demands spread of 1, never more — the proxy can only
    under-demand, never invent evidence. An EMPTY slice returns the ZERO
    target: no types, no minimum, no figure ("no examples where no evidence",
    NC §4 B3/TIER-3). allowed_types, when given, intersects required_types so
    a slice question mis-typed against the exam pattern is never demanded.
    Deterministic by construction — no clock, no randomness — so a re-run of
    NA on its own output derives the identical contract (NA §8)."""
    qs = bank_questions_for(bank, subject, topic, subtopic)
    if not qs:
        return {"required_types": [], "min_concepts_with_examples": 0,
                "requires_figure": False, "pyq_count": 0,
                "distinct_concept_tags": 0,
                "format_mix": {"figure": 0, "text": 0},
                "format_by_concept": {}}
    types = {str(q.get("type", "")).upper() for q in qs}
    types &= set(CANONICAL_TYPES)
    if allowed_types:
        types &= {str(t).upper() for t in allowed_types}
    tags = {" ".join(str(t).lower().split())
            for q in qs for t in (q.get("concept_tags") or ()) if str(t).strip()}
    # v2.10 — THE FORMAT CONTRACT (owner decisions, 2026-08-15): the exam's
    # own history decides the figure/text balance. format_mix counts the
    # slice's figure-flagged vs text questions (bool(stem_figures), recorded
    # since the bank existed — an UNRESOLVED image still counts: the student
    # saw a figure in the real exam). format_by_concept is the same split per
    # normalized concept_tag — NC §4 B3a reads it to pick each concept's LEAD
    # Example format (frequency shapes EMPHASIS, never exclusion) and G-12
    # lists its figure-evidenced tags advisory. The HARD demand downstream is
    # deliberately minimal: format_mix["figure"] >= 1 -> the notes must pair
    # >= 1 rendered figure with >= 1 Example in one concept section. No
    # evidence, no demand — a zero-figure slice never demands a figure.
    fmt = {"figure": sum(1 for q in qs if q.get("figure")),
           "text": sum(1 for q in qs if not q.get("figure"))}
    by_concept = {}
    for q in qs:
        for t in (q.get("concept_tags") or ()):
            t = " ".join(str(t).lower().split())
            if not t:
                continue
            d = by_concept.setdefault(t, {"figure": 0, "text": 0})
            d["figure" if q.get("figure") else "text"] += 1
    return {"required_types": sorted(types),
            "min_concepts_with_examples": min(max(1, len(tags)),
                                              COVERAGE_CONCEPT_CEILING),
            "requires_figure": any(q.get("figure") for q in qs),
            "pyq_count": len(qs),
            "distinct_concept_tags": len(tags),
            "format_mix": fmt,
            "format_by_concept": by_concept}


def display_norm(s):
    """v2.9 — the ONE name normalization for matching a subtopic display name
    inside prose (G-13's Combines-line match). Wraps syllabus_provenance.norm
    — the SAME normalization subtopic_key uses per component — so legal
    header-vs-manifest drift (& vs and, dash variants, NFKC, spacing) never
    produces a false gate finding. No gate may roll its own name norm."""
    return syllabus_provenance.norm(s)


def _integration_members(q):
    """The fusion set of q as {subtopic_key: (subject, topic, name)} —
    header first, then every well-formed declared partner."""
    home = subtopic_key(q["subject"], q["topic"], q["subtopic"])
    members = {home: (q["subject"], q["topic"], q["subtopic"])}
    for p in (q.get("integration_partners") or []):
        parts = [x.strip() for x in str(p).split("::")]
        if len(parts) == 3 and all(parts):
            members[subtopic_key(*parts)] = tuple(parts)
    return home, members


def _integration_filing_key(q, unit_order):
    """v2.8/v2.9 — THE filing authority, shared by integration_target_for and
    audit_questions_for so the teaching home and the audit home can never
    disagree. Returns the subtopic_key of the unit where question q FILES.

    An unfused question files at its header subtopic. A fused question MOVES
    to the LATEST member of its fusion set (header + declared partners) ONLY
    when the evidence is FULLY RESOLVED — every member, header included, is
    present in unit_order (v2.9, certification-sweep finding): filing on
    partial evidence either dragged an OUT-OF-SYLLABUS header's question
    into a certifiable unit's set, or under-filed when a typo'd partner was
    really a later unit. Any unresolved member -> the question STAYS at its
    header (exactly the pre-feature boundary) and the defect is REPORTED
    (integration_target_for's unresolved list; NB's next run is the fix).
    Without unit_order the header is always the filing home (the
    degenerate-caller fallback; NC and NA always pass
    unit_order_from_registry, spec-mandated)."""
    home, members = _integration_members(q)
    if len(members) == 1 or not unit_order:
        return home
    if any(k not in unit_order for k in members):
        return home
    return max(members, key=lambda k: unit_order[k])


def unit_order_from_registry(registry):
    """v2.8 — the ONE builder of the unit_order map (NC §4 B4a I-5 and NA §2
    both call this; neither hand-builds a map — the author/gate drift class
    stays closed). Ordinal = the (s, t, nn) digits parsed from each unit's
    PERSISTED unit_code (NB §1A A-3: assigned from manifest row order and
    NEVER renumbered, so the ordinal is stable teaching order), keyed by
    subtopic_key(section, topic, name). Units without a parseable unit_code
    or a complete manifest triple (pre-v3 legacy registries) are SKIPPED —
    their resolution already routes to NB (MIGRATION); a skipped unit simply
    keeps header filing. Deterministic; tuples compare lexicographically."""
    order = {}
    for u in registry.get("units", {}).values():
        code = u.get("unit_code") or ""
        m = re.search(r"_S(\d+)_T(\d+)_ST(\d+)$", str(code))
        if not m:
            continue
        sec, top, name = u.get("section"), u.get("topic"), u.get("name")
        if not (sec and top and name):
            continue
        order[subtopic_key(sec, top, name)] = (int(m.group(1)),
                                               int(m.group(2)),
                                               int(m.group(3)))
    return order


def audit_questions_for(bank, subject, topic, subtopic, unit_order=None):
    """v2.8 — the unit's CERTIFICATION SET for NA's closed-book solve (§2):
    every bank question whose FILING HOME (_integration_filing_key) is this
    unit. That is the header slice MINUS fused questions DEFERRED to a later
    partner (their ingredients live in material this unit's notes must not
    teach — backward-only — so this unit can never make them solvable) PLUS
    fused questions INBOUND from earlier units' slices (this unit's
    integration section exists exactly to make them solvable closed-book).

    IDENTICAL to bank_questions_for when the bank is GRANDFATHERED (no
    integration_partners anywhere) or unit_order is not supplied — no
    behaviour change for any existing exam, and pass_for_unit's denominator
    still can never be shrunk by a caller: it derives from THIS list.
    coverage_target_for deliberately still reads the header slice (the
    contract reads the bank's evidence; only the solve boundary follows
    filing)."""
    if not any(q.get("integration_partners") for q in bank.get("questions", ())):
        return bank_questions_for(bank, subject, topic, subtopic)
    own = subtopic_key(subject, topic, subtopic)
    return [q for q in bank["questions"]
            if _integration_filing_key(q, unit_order) == own]


def integration_target_for(bank, subject, topic, subtopic, unit_order=None):
    """v2.7 — the unit's INTEGRATION CONTRACT, derived entirely from the bank
    (G-13's single authority; NC §4 B4a authors to it, NA §5 G-13 gates it,
    so author and gate can never disagree — the coverage_target_for idiom).

    Returns {"dormant", "attested", "fusions": [{"partners": [display names of
    the OTHER subtopics], "bank_ids": [...]}], "pyq_count"}.

    GRANDFATHERING: a bank with NO integration_partners field on ANY question
    (a bank written before notes-pyq-bank/1.2) returns dormant=True — the gate
    reports DORMANT and never blocks, because the bank could not have carried
    the evidence. The moment ANY question in the bank declares a partner, the
    contract is live for every unit.

    LATEST-PARTNER FILING (backward-only, owner decision 2026-08-14): a fused
    question's FUSION SET is its own header subtopic plus every declared
    partner. The question files at — attests an integration section in — the
    LATEST member of that set under unit_order (built ONLY by
    unit_order_from_registry; NB §1A A-3 makes that order teaching order).
    Earlier members never teach the fusion: their students have not met the
    later ingredients yet. v2.8: the filing decision is
    _integration_filing_key — the SAME authority audit_questions_for uses,
    so where a fused question is TAUGHT and where it is SOLVED can never
    disagree. Without unit_order the header subtopic is the filing home.
    Deterministic by construction — no clock, no randomness (NA §8)."""
    questions = bank.get("questions", [])
    if not any(q.get("integration_partners") for q in questions):
        return {"dormant": True, "attested": False, "fusions": [],
                "unresolved": [], "pyq_count": 0}
    own = subtopic_key(subject, topic, subtopic)
    fusions, unresolved = {}, []
    for q in questions:
        declared = q.get("integration_partners") or []
        if not declared:
            continue
        if _integration_filing_key(q, unit_order) != own:
            continue
        home, members = _integration_members(q)
        # v2.9: a fused question that filed HERE only because its evidence is
        # not fully resolved (some member unknown to unit_order) is NOT a
        # teaching demand — it is a REPORTED ingest defect (fix at NB), and
        # the question is simply audited here like any other (§2). Demanding
        # a Combines line that names an unresolvable subtopic would deadlock
        # a correct document.
        if unit_order and any(k not in unit_order for k in members):
            unresolved.append({
                "bank_id": q["bank_id"],
                "unknown": sorted("::".join(members[k]) for k in members
                                  if k not in unit_order)})
            continue
        # v2.9: qualify a partner name with its Topic when two partners in
        # this fusion share a bare display name (E-16 duplicate-name case) —
        # the Combines line must be unambiguous for student and gate alike.
        others = [members[k] for k in members if k != own]
        names = [t[2] for t in others]
        partner_names = tuple(sorted(
            (f"{t[1]} :: {t[2]}" if names.count(t[2]) > 1 else t[2])
            for t in others))
        fusions.setdefault(partner_names, []).append(q["bank_id"])
    out = [{"partners": list(names), "bank_ids": ids}
           for names, ids in sorted(fusions.items())]
    return {"dormant": False, "attested": bool(out), "fusions": out,
            "unresolved": unresolved,
            "pyq_count": sum(len(f["bank_ids"]) for f in out)}


# ------------------------------------------------------------ recall contract
# v2.12 — GAP-2026-09-01-RECALL-CONTRACT. Everything below is deterministic:
# no clock, no randomness, no I/O except difficulty_profile_load (which never
# raises). blueprint_core is imported LAZILY inside the three wrappers only —
# it is routed to NotesCreate/NotesAudit from this release, but its absence is
# reported as dormant rather than crashing a unit (the G-7a discipline).

_STOP = frozenset("""a an and are as at be by for from has have if in into is it its of on
or that the their this to was were which will with when what where who
find calculate determine compute given following statement statements
correct incorrect true false not except which one option options value
""".split())
_TOKEN_RE = re.compile(r"[a-z][a-z0-9_]+")


def normalize_complexity(raw, labels=DIFFICULTY_LABELS_DEFAULT):
    """A bank question's free-text `complexity` tag -> one of `labels` (by band
    position) or None when it names no band. Case/space-insensitive; an exact
    label name always wins over the alias table."""
    if raw is None:
        return None
    t = " ".join(str(raw).lower().split())
    if not t:
        return None
    labs = list(labels or DIFFICULTY_LABELS_DEFAULT)
    if len(labs) != 3:
        return None
    for i, lab in enumerate(labs):
        if t == str(lab).lower():
            return labs[i]
    for i, names in COMPLEXITY_ALIASES.items():
        if t in names:
            return labs[i]
    return None


def _band_counts_from(values, labels):
    counts = {lab: 0 for lab in labels}
    for v in values:
        if isinstance(v, str) and v in counts:     # a non-string "band" is junk, not a band
            counts[v] += 1
    return counts


def _mode_band(counts, labels):
    """Modal band; ties resolve to the HARDER band (the contract never
    under-demands). None when nothing was counted."""
    total = sum(counts.get(lab, 0) for lab in labels)
    if not total:
        return None
    best, best_n = None, -1
    for lab in labels:                      # ascending difficulty ...
        n = counts.get(lab, 0)
        if n >= best_n and n > 0:           # ... so >= keeps the later (harder) label on a tie
            best, best_n = lab, n
    return best


def difficulty_profile_load(path, exam_code=None):
    """Read [ExamCode]_difficulty_profile.json for the Recall contract.

    NEVER RAISES (owner rule O-5, 2026-09-01: a missing or partial profile never
    blocks a unit). Returns (profile, None) or (None, reason). The profile is
    checked with blueprint_core.dp_check_profile against its OWN _meta labels —
    the Notes route has no exam_config; the exam_code check runs when given."""
    if not path or not os.path.exists(path):
        return (None, "difficulty profile absent")
    try:
        with open(path, encoding="utf-8") as fh:
            prof = json.load(fh)
    except Exception as exc:                        # pragma: no cover - defensive
        return (None, f"difficulty profile unreadable: {exc}")
    try:
        import blueprint_core as _bc
    except ImportError:
        return (None, "blueprint_core unavailable — rubric dormant")
    try:
        labels = (prof.get("_meta") or {}).get("difficulty_labels")
        code = exam_code if exam_code is not None else (prof.get("_meta") or {}).get("exam_code")
        _bc.dp_check_profile(prof, code, labels)
    except Exception as exc:
        return (None, f"difficulty profile rejected: {exc}")
    return (prof, None)


def _profile_band_counts(profile, labels, subtopic_id=None):
    """{label: count} over the profile's DP window (the SAME cycles the mock flow
    reads), filtered to one subtopic_id when given, else paper-level."""
    out = {lab: 0 for lab in labels}
    if not profile:
        return out
    try:
        import blueprint_core as _bc
        cycles = _bc.dp_window(profile)
    except Exception:
        return out
    for c in cycles:
        for key in c.get("papers", []):
            qs = ((profile.get("papers") or {}).get(key) or {}).get("questions") or {}
            for _q, rec in (qs.items() if isinstance(qs, dict) else ()):
                if not isinstance(rec, dict):
                    continue                     # a corrupted question record carries no evidence
                if subtopic_id is not None and str(rec.get("subtopic_id") or "") != str(subtopic_id):
                    continue
                try:
                    band = _bc.band_for_score(int(rec.get("score")), list(labels))
                except Exception:
                    band = None
                if band in out:
                    out[band] += 1
    return out


def _rung(counts, labels, source):
    band = _mode_band(counts, labels)
    return {"band": band, "count": sum(counts.values()), "counts": counts,
            "source": source} if band else None


def recall_target_for(bank, subject, topic, subtopic, unit_order=None,
                      allowed_types=(), profile=None, subtopic_id=None,
                      difficulty_labels=None):
    """v2.12 — the unit's RECALL CONTRACT (G-14's single authority; NC §4 B7a
    authors to it, NA §5 G-14 gates it, so author and gate can never disagree —
    the coverage_target_for idiom).

    Composition (owner decisions 2026-09-01, SPREAD NOT COUNT): one core Recall
    per concept section; every attested type once; a figure-reading item iff the
    slice attests figures; cumulative items ONLY from EARLIER subtopics of the
    SAME Section (unit_order — the ONE order map, unit_order_from_registry);
    >= 1 near-miss.
    Difficulty (owner rule O-4: the same scale as the real paper) is a LADDER of
    rungs, each carrying its evidence so the nearest rung with evidence decides
    and the basis is reported, never silent (O-5):
      difficulty_by_tag   per normalized concept_tag from the bank slice's
                          `complexity` — a band only at >= RECALL_MIN_PYQ_FOR_TAG_BAND
      difficulty_by_partner per EARLIER same-section partner: the partner's own
                          bank complexity mode (a cumulative item's evidence)
      difficulty_subtopic the exam's OWN rubric-measured band mix for this
                          subtopic_id over the profile's default cycle window
      difficulty_topic    the bank's complexity mode over the whole parent topic
      difficulty_exam     the profile's paper-level mix over the same window
      difficulty_neutral  labels[RECALL_NEUTRAL_BAND_INDEX]
    Deterministic — no clock, no randomness (NA §8)."""
    labels = list(difficulty_labels or (((profile or {}).get("_meta") or {}).get("difficulty_labels")
                                        or DIFFICULTY_LABELS_DEFAULT))
    if len(labels) != 3:
        labels = list(DIFFICULTY_LABELS_DEFAULT)
    qs = bank_questions_for(bank, subject, topic, subtopic)
    own = subtopic_key(subject, topic, subtopic)
    types = {str(q.get("type", "")).upper() for q in qs} & set(CANONICAL_TYPES)
    if allowed_types:
        types &= {str(t).upper() for t in allowed_types}
    # earlier subtopics of the SAME Section ONLY (I-4 backward-only by construction)
    partners, order_known = [], False
    if unit_order and own in unit_order:
        order_known = True
        mine = unit_order[own]
        # EARLIER and in the SAME Section (subject): ordinal (s, t, nn) with the
        # same s and a smaller tuple. Cross-subject revision is never demanded.
        partners = sorted((k for k, o in unit_order.items()
                           if o < mine and o[0] == mine[0]),
                          key=lambda k: unit_order[k])
    # difficulty ladder
    by_tag, tag_n = {}, {}
    for q in qs:
        band = normalize_complexity(q.get("complexity"), labels)
        for t in (q.get("concept_tags") or ()):
            t = " ".join(str(t).lower().split())
            if not t:
                continue
            d = by_tag.setdefault(t, {lab: 0 for lab in labels})
            tag_n[t] = tag_n.get(t, 0) + 1
            if band:
                d[band] += 1
    diff_by_tag = {}
    for t, counts in sorted(by_tag.items()):
        n = tag_n[t]                        # PYQs carrying the tag, banded or not
        diff_by_tag[t] = {"band": _mode_band(counts, labels) if n >= RECALL_MIN_PYQ_FOR_TAG_BAND else None,
                          "count": n, "counts": counts}
    sub_counts = _profile_band_counts(profile, labels, subtopic_id) if (profile and subtopic_id) else {lab: 0 for lab in labels}
    own_topic = own.rsplit("|||", 1)[0]
    topic_vals = [normalize_complexity(q.get("complexity"), labels)
                  for q in bank.get("questions", [])
                  if subtopic_key(q["subject"], q["topic"], q["subtopic"]).rsplit("|||", 1)[0]
                  == own_topic]
    topic_counts = _band_counts_from(topic_vals, labels)
    # v2.12 — a CUMULATIVE Recall tests a PARTNER's concept, so its band must
    # stand on the PARTNER's evidence: the partner's own bank slice complexity
    # mode (found by the dry run of 2026-09-01: resolving it on THIS unit's
    # subtopic rung forced an easy revision item up to the unit's band).
    by_partner = {}
    for pk in partners:
        vals = [normalize_complexity(q.get("complexity"), labels)
                for q in bank.get("questions", [])
                if subtopic_key(q["subject"], q["topic"], q["subtopic"]) == pk]
        by_partner[pk] = _rung(_band_counts_from(vals, labels), labels, "bank")
    exam_counts = _profile_band_counts(profile, labels) if profile else {lab: 0 for lab in labels}
    exam_rung = _rung(exam_counts, labels, "profile")
    if exam_rung:
        n = exam_rung["count"]
        exam_rung["pct"] = {lab: (100 * exam_counts[lab] / n) for lab in labels}
    return {"core_per_concept": RECALL_CORE_PER_CONCEPT,
            "required_types": sorted(types),
            "requires_figure_item": any(q.get("figure") for q in qs),
            # R-12 (owner question 2026-09-01: "real exam questions combine 2-3
            # concepts"): the slice attests a top-band question — on the shared
            # rubric a top-band item IS a multi-concept derivation — so the
            # self-test must carry >= 1 Recall combining concepts. The second
            # trigger (>= 2 concept sections in the document) is decided by the
            # gate from the model, since the bank cannot see the section count.
            "requires_multi_concept_item": any(
                normalize_complexity(q.get("complexity"), labels) == labels[-1] for q in qs),
            "multi_concept_min_axioms": RECALL_MULTI_CONCEPT_MIN_AXIOMS,
            "cumulative_divisor": RECALL_CUMULATIVE_DIVISOR,
            "cumulative_floor": RECALL_CUMULATIVE_FLOOR,
            "cumulative_partners": partners,
            "order_known": order_known,
            "near_miss_min": RECALL_NEAR_MISS_MIN,
            "ceiling": RECALL_CEILING,
            "pyq_count": len(qs),
            "difficulty_labels": labels,
            "difficulty_by_tag": diff_by_tag,
            "difficulty_by_partner": by_partner,
            "difficulty_subtopic": _rung(sub_counts, labels, "profile"),
            "difficulty_topic": _rung(topic_counts, labels, "bank"),
            "difficulty_exam": exam_rung,
            "difficulty_neutral": labels[RECALL_NEUTRAL_BAND_INDEX],
            "profile_present": bool(profile)}


def recall_is_multi_concept(item, target=None):
    """R-12: does this Recall combine concepts? Read from the SAME recorded
    derivation the rubric verifies (difficulty_obs.axiom_concepts >=
    multi_concept_min_axioms), so author, builder and gate agree by construction.
    Junk observations are not evidence -> False."""
    try:
        thr = int((target or {}).get("multi_concept_min_axioms") or RECALL_MULTI_CONCEPT_MIN_AXIOMS)
    except (TypeError, ValueError):
        thr = RECALL_MULTI_CONCEPT_MIN_AXIOMS      # a junk threshold falls back to the engine constant
    obs = (item or {}).get("difficulty_obs") if isinstance(item, dict) else None
    if not isinstance(obs, dict):
        return False
    try:
        return int(obs.get("axiom_concepts")) >= thr
    except (TypeError, ValueError):
        return False


def recall_multi_concept_required(target, concept_count):
    """R-12 trigger: the slice attests a top-band question OR the document has
    >= 2 concept sections. A single-concept subtopic with no top-band evidence
    demands nothing (no evidence, no demand)."""
    return bool((target or {}).get("requires_multi_concept_item")) or int(concept_count) >= 2


def recall_cumulative_min(core_count, target):
    """How many cumulative (earlier-subtopic) Recalls the set must carry.
    0 when the unit has no earlier subtopic (nothing exists to combine with);
    else max(floor, ceil(core / divisor)), reduced toward the floor so that
    core + cumulative <= ceiling where that is attainable. Returns (n,
    ceiling_attainable)."""
    core = int(core_count)
    if not target.get("cumulative_partners"):
        return (0, core <= int(target.get("ceiling", RECALL_CEILING)))
    div = int(target.get("cumulative_divisor", RECALL_CUMULATIVE_DIVISOR))
    floor = int(target.get("cumulative_floor", RECALL_CUMULATIVE_FLOOR))
    ceil_ = int(target.get("ceiling", RECALL_CEILING))
    n = max(floor, -(-core // div))
    if core + n > ceil_:
        n = max(floor, ceil_ - core)
    return (n, core + n <= ceil_)


def _qtype_floor_index(qtype, labels):
    """MSQ/NAT cannot honestly reach the bottom band (the shared rubric's qtype
    floor). Mirrors blueprint_core.difficulty_min_band; falls back to the same
    arithmetic when the rubric is unavailable."""
    try:
        import blueprint_core as _bc
        b = _bc.difficulty_min_band(str(qtype or "mcq").lower(), list(labels))
        if b in labels:
            return labels.index(b)
    except Exception:
        pass
    return 1 if str(qtype or "").upper() in ("MSQ", "NAT") else 0


def recall_expected_band(target, tags=(), is_near_miss=False, qtype="MCQ",
                         scope="core", partner=None):
    """THE ONE band resolver (NC authors to it; NA G-14 re-derives it).
    Returns (label, basis). CORE rung order: the harder band among the item's
    declared concept tags that carry a band -> subtopic (profile) -> topic
    (bank) -> exam (profile) -> neutral. CUMULATIVE rung order: the PARTNER's
    own bank complexity mode -> topic -> exam -> neutral — this unit's concept
    and subtopic rungs are evidence about THIS unit and never decide a
    partner's item. A near-miss item is ONE band above its base (capped at
    the top). The MSQ/NAT floor is applied last."""
    labels = list(target.get("difficulty_labels") or DIFFICULTY_LABELS_DEFAULT)
    if len(labels) != 3:                # the rubric is a 3-band scale; anything else is not a vocabulary
        labels = list(DIFFICULTY_LABELS_DEFAULT)
    idx, basis = None, None
    cumulative = (scope == "cumulative")
    if cumulative:
        pk = _partner_key_norm(partner)
        r = (target.get("difficulty_by_partner") or {}).get(pk)
        if r and r.get("band") in labels:
            idx, basis = labels.index(r["band"]), "partner"
    else:
        by_tag = target.get("difficulty_by_tag") or {}
        if isinstance(tags, str):
            tags = (tags,)
        elif not isinstance(tags, (list, tuple, set, frozenset)):
            tags = ()                   # a corrupted declaration carries no tag evidence
        for t in tags:
            t = " ".join(str(t).lower().split())
            b = (by_tag.get(t) or {}).get("band")
            if b in labels:
                i = labels.index(b)
                if idx is None or i > idx:
                    idx, basis = i, "concept"
    if idx is None:
        rungs = (("difficulty_topic", "topic"), ("difficulty_exam", "exam")) if cumulative else \
                (("difficulty_subtopic", "subtopic"), ("difficulty_topic", "topic"),
                 ("difficulty_exam", "exam"))
        for key, name in rungs:
            r = target.get(key)
            if r and r.get("band") in labels:
                idx, basis = labels.index(r["band"]), name
                break
    if idx is None:
        idx, basis = RECALL_NEUTRAL_BAND_INDEX, "neutral"
    if is_near_miss:
        idx = min(idx + 1, len(labels) - 1)
    idx = min(max(idx, _qtype_floor_index(qtype, labels)), len(labels) - 1)
    return (labels[idx], basis)


def _partner_key_norm(partner):
    """A declared partner — a manifest scope 'Subject::Topic::Sub Topic Name'
    or an already-normalized subtopic_key — as the subtopic_key the target's
    cumulative_partners / difficulty_by_partner carry. Junk stays a string."""
    p = str(partner or "")
    if "|||" in p:
        return p
    parts = [x.strip() for x in p.split("::")]
    if len(parts) == 3 and all(parts):
        return subtopic_key(*parts)
    return p


def recall_verify_difficulty(label, obs, labels=DIFFICULTY_LABELS_DEFAULT):
    """label == the shared rubric's band for the recorded observations?
    Wraps blueprint_core.verify_difficulty_obs — the SAME check Step 7's G-DIFF
    and A-QINDEX check 8 run. Returns (ok, measured, dormant_reason)."""
    try:
        import blueprint_core as _bc
    except ImportError:
        return (True, None, "blueprint_core unavailable — rubric dormant")
    ok, measured = _bc.verify_difficulty_obs(label, obs, list(labels))
    if measured is None:
        return (True, None, "observations unusable — rubric fall-through")
    return (bool(ok), measured, None)


def recall_authoring_profile(band, qtype, labels=DIFFICULTY_LABELS_DEFAULT):
    """The observation targets that land a Recall of `qtype` IN `band` —
    blueprint_core.difficulty_authoring_profile, or None when the rubric is
    unavailable (NC then authors to the band by judgement and G-14 reports
    the rubric dormant)."""
    try:
        import blueprint_core as _bc
    except ImportError:
        return None
    return _bc.difficulty_authoring_profile(band, str(qtype or "mcq").lower(), list(labels))


def scenario_key(text):
    """Content-token set of a stem (lower-case alphabetic tokens minus a small
    stoplist and pure numbers) — the deterministic proxy behind the no-clone
    rule. Numbers are dropped on purpose: fresh numbers alone do not make a
    fresh scenario."""
    return frozenset(t for t in _TOKEN_RE.findall(str(text or "").lower())
                     if t not in _STOP and len(t) > 2)


def is_clone(key_a, key_b, threshold=None):
    """Jaccard(key_a, key_b) >= RECALL_CLONE_JACCARD -> the two stems share a
    scenario. Two empty keys are not a clone (nothing to compare)."""
    a, b = frozenset(key_a or ()), frozenset(key_b or ())
    if not a or not b:
        return False
    thr = RECALL_CLONE_JACCARD if threshold is None else threshold
    return len(a & b) / len(a | b) >= thr


def recall_exam_mix_check(bands, target):
    """The shipped set's band counts vs the exam's measured paper-level mix
    (target['difficulty_exam']['pct']) applied to the set size, largest
    remainder, ±RECALL_EXAM_MIX_TOLERANCE items per band. Returns
    (findings, expected|None). expected None == dormant (no profile mix)."""
    ex = target.get("difficulty_exam")
    labels = list(target.get("difficulty_labels") or DIFFICULTY_LABELS_DEFAULT)
    if not ex or not ex.get("pct") or not bands:
        return ([], None)
    n = len(bands)
    raw = {lab: n * float(ex["pct"].get(lab, 0)) / 100.0 for lab in labels}
    exp = {lab: int(raw[lab]) for lab in labels}
    rem = n - sum(exp.values())
    for lab in sorted(labels, key=lambda l: (-(raw[l] - exp[l]), labels.index(l))):
        if rem <= 0:
            break
        exp[lab] += 1
        rem -= 1
    actual = _band_counts_from(bands, labels)
    findings = []
    for lab in labels:
        if abs(actual[lab] - exp[lab]) > RECALL_EXAM_MIX_TOLERANCE:
            findings.append(f"Recall set carries {actual[lab]} {lab} item(s) but the exam's "
                            f"measured mix expects {exp[lab]} of {n} (±{RECALL_EXAM_MIX_TOLERANCE})")
    return (findings, exp)


def derive_taxonomy_counts(bank, latest_years=3):
    """Owner decision 5(i): subtopic-wise pyq_count and recent-N-year counts
    computed DIRECTLY from the ingested bank — the separate PYQ Analysis doc is
    no longer required. 'recent3' counts questions whose exam_year is among the
    top `latest_years` DISTINCT exam years present in the corpus (so a corpus
    that stops in 2024 still has a well-defined recent window). Returns
    {subtopic_key: {subject, topic, subtopic, pyq_count, recent3_count,
    per_year{year:count}}}."""
    years = sorted({q["exam_year"] for q in bank["questions"]}, reverse=True)
    recent = set(years[:max(0, int(latest_years))])
    out = {}
    for q in bank["questions"]:
        # Recompute the key from stored fields — never trust the stored
        # subtopic_key — so counts are correct even on a bank written by an older
        # notes_core (drift class closed, v1.8).
        e = out.setdefault(subtopic_key(q["subject"], q["topic"], q["subtopic"]),
                           {"subject": q["subject"], "topic": q["topic"],
                            "subtopic": q["subtopic"], "pyq_count": 0,
                            "recent3_count": 0, "per_year": {}})
        e["pyq_count"] += 1
        e["per_year"][q["exam_year"]] = e["per_year"].get(q["exam_year"], 0) + 1
        if q["exam_year"] in recent:
            e["recent3_count"] += 1
    return out


# ---------------------------------------------------------------- self-test
def self_test():
    import tempfile
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def mini_docx(text, extra_xml=""):
        fp = tempfile.mktemp(suffix=".docx")
        with zipfile.ZipFile(fp, "w") as z:
            z.writestr("word/document.xml",
                       "<w:document>%s<w:p><w:r><w:t>%s</w:t></w:r></w:p>"
                       "</w:document>" % (extra_xml, text))
            z.writestr("[Content_Types].xml", "<Types/>")
        return fp

    # density: unknown tier is a finding (v1.2 defect fixture); band edges
    d = mini_docx("short bullet")
    try:
        okr, f = density_gate(d, "TIER-9", 7)
        check("unknown tier is a finding, not a crash",
              okr is False and any("unknown tier" in x for x in f))
    except KeyError:
        check("unknown tier is a finding, not a crash", False)
    check("band edge 6 passes TIER-1", density_gate(d, "TIER-1", 6)[0])
    check("band edge 15 passes TIER-1", density_gate(d, "TIER-1", 15)[0])
    check("band edge 5 fails TIER-1", not density_gate(d, "TIER-1", 5)[0])
    check("band edge 16 fails TIER-1", not density_gate(d, "TIER-1", 16)[0])

    # oMath: attributed tag counted (v1.2) AND attributed defect caught (v1.4
    # — the previously vacuous fixture, reviewer-prescribed)
    fp = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(fp, "w") as z:
        z.writestr("word/document.xml",
                   '<w:document><m:oMath xmlns:m="http://x"><m:r><m:t>V</m:t>'
                   "</m:r></m:oMath></w:document>")
    try:
        check("attributed oMath counted", assert_omml(fp, 1) == 1)
    except AssertionError:
        check("attributed oMath counted", False)
    fp2 = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(fp2, "w") as z:
        z.writestr("word/document.xml",
                   '<w:document><w:p><w:r><w:t>prose</w:t></w:r></w:p>'
                   '<m:oMath xmlns:m="http://x"><m:r><m:t>x^(2)</m:t></m:r>'
                   "</m:oMath></w:document>")
    check("attributed oMath defect caught",
          scan_omml_structural(fp2) == ["textual exponent inside oMath"])

    # prose bans: wave-1 basics
    check("prose ban: year", scan_prose_bans(mini_docx("in 1857 it began"))
          == ["year reference"])
    check("prose ban: exemption",
          scan_prose_bans(mini_docx("in 1857 it began"),
                          exemptions=("year reference",)) == [])
    check("prose ban: boundaries safe",
          scan_prose_bans(mini_docx("NATO NATure signature Nature Q3")) == [])
    check("prose ban: attrs ignored",
          scan_prose_bans(mini_docx("clean", '<w:gridCol w:w="1700"/>')) == [])

    # reviewer tables (waves 2+3) verbatim: must all be CLEAN
    for sci in ("absorption at 1650 cm\u207b\u00b9", "a load of 1700 held",
                "melting near 1750", "molar mass 1800 g/mol",
                "rotates 2000 per second", "range 1600 to saturation",
                "the 1650 cm-1 band", "at the 1700 peak",
                "from 1600 to 1800 cm-1", "range 1600-1800 cm-1",
                "band 1600, 1700 and 1750 cm-1",
                "bands at 1650, 1700, 1750 cm\u207b\u00b9",
                "range 1600\u20131800 cm\u207b\u00b9"):
        check("no year on: " + sci, scan_prose_bans(mini_docx(sci)) == [])
    for yr in ("in 2014 the pattern", "since 2006 it recurs",
               "seen 2006, 2009, 2014", "span 2005\u20132026",
               "the 1990s trend", "asked 2013 Q32"):
        check("year on: " + yr,
              scan_prose_bans(mini_docx(yr)) == ["year reference"])
    check("documented miss: the 1857 revolt",
          scan_prose_bans(mini_docx("the 1857 revolt")) == [])

    # case-insensitivity (wave-2 reverts bind); NAT exact-case trade-off
    for t2 in ("The Examiner expects", "EXAMINER note", "pyq bank", "Pyq",
               "exam lens returns", "Modelled On a pattern", "mcq set",
               "q: hello"):
        check("case-insensitive ban: " + t2,
              scan_prose_bans(mini_docx(t2)) != [])
    check("NAT stays exact-case (documented trade-off)",
          scan_prose_bans(mini_docx("a nat fragment")) == [])

    # reviewer table (wave 3): measurement vs symbol-mention
    for clean in ("distance 5 Km north", "walked 5 Km in the field",
                  "a 12 Km, then rest"):
        check("measurement clean: " + clean,
              scan_flat_math_tokens(mini_docx(clean)) == [])
    for flg in ("the 2 Kd values", "Table 3 Km column",
                "compare 4 Vmax estimates", "the Km of this enzyme"):
        check("symbol mention flags: " + flg,
              scan_flat_math_tokens(mini_docx(flg)) != [])
    check("split runs clean",
          scan_flat_math_tokens(mini_docx("V and max apart")) == [])

    # registry + blueprint migrations, transitions, roles/tiers
    import json as _json
    rp = tempfile.mktemp(suffix=".json")
    _json.dump({"schema": "notes-registry/1.0", "exam_code": "X",
                "syllabus_sha256": "h", "exam_level": "G", "created": "c",
                "updated": "u", "units": {"U": {"name": "n", "role": "COVERAGE",
                "tier": "TIER-3", "pyq_count": 0, "provenance": "syllabus",
                "state": "BLUEPRINTED", "stale": False, "notes_version": None,
                "audit": None, "artifacts": {}, "history": []}}}, open(rp, "w"))
    reg = registry_load(rp)
    check("1.0 registry migrates", reg["schema"] == REGISTRY_SCHEMA
          and reg["units"]["U"]["prose_ban_exemptions"] == [])
    transition(reg, "U", "DRAFTED")
    try:
        transition(reg, "U", "DELIVERED")
        check("illegal transition rejected", False)
    except ValueError:
        check("illegal transition rejected", True)
    bp10 = {"schema": "notes-blueprint/1.0", "exam_code": "X", "level": "G",
            "syllabus_sha256": "h", "generated": "g", "sources": {},
            "units": [{"unit_code": "X_S1_T1_ST01", "name": "n", "slug": "n",
                       "role": "COVERAGE", "tier": "TIER-3", "pyq_count": 0,
                       "provenance": "syllabus"}], "excluded": []}
    fp3 = tempfile.mktemp(suffix=".json")
    _json.dump(bp10, open(fp3, "w"))
    bp = load_blueprint(fp3)
    check("blueprint 1.0 migrates to 1.2", bp["schema"] == BLUEPRINT_SCHEMA
          and bp["allowed_question_types"] == []
          and bp["bank_ref"] is None
          and bp["units"][0]["prose_ban_exemptions"] == [])
    _json.dump(dict(bp10, schema="notes-blueprint/0.9"), open(fp3, "w"))
    try:
        load_blueprint(fp3)
        check("unknown blueprint schema rejected", False)
    except ValueError:
        check("unknown blueprint schema rejected", True)

    # bank_ref staleness link (fix 1)
    bpath = tempfile.mktemp(suffix=".json")
    bnk = bank_new("EX"); bank_save(bnk, bpath)
    ref = {"path": bpath, "sha256": file_sha256(bpath), "questions": 0}
    check("verify_bank_ref matches", verify_bank_ref(bpath, ref)[0] is True)
    with open(bpath, "a", encoding="utf-8") as _f:
        _f.write(" ")   # mutate the bank on disk
    check("verify_bank_ref detects a stale bank",
          verify_bank_ref(bpath, ref)[0] is False)
    check("verify_bank_ref flags a missing ref",
          verify_bank_ref(bpath, None)[0] is False)
    check("role: evidence rule", assign_role(False, 5, False, 1) is None
          and assign_role(False, 5, False, 2) == "EVIDENCE_ADDED")
    check("tier: thresholds", assign_tier("PYQ_WEIGHTED", 15) == "TIER-1"
          and assign_tier("PYQ_WEIGHTED", 14) == "TIER-2")
    check("types normalized",
          normalize_types(["MCQ", "mcq (Single)", "NAT x"]) == ["MCQ", "NAT"])
    LC = LEVEL_COLORS
    check("colour map distinct",
          len({LC["L1"], LC["L2"], LC["L3"], LC["table_header"]}) == 4)
    check("example/recall boxes identical",
          BOX_COLORS["example"] == BOX_COLORS["recall"])

    # ---- v1.5 ingest base -------------------------------------------------
    # filename date parsing (the live physics name + variants + fallbacks)
    check("date: DD-Mon-YYYY",
          parse_exam_date_from_filename(
              "IIT_JAM_PHYSICS_15-Feb-2026_PYQ_Final.docx")
          == ("2026-02-15", 2026, "15-Feb-2026"))
    check("date: compact DDMonYYYY + Copy of + (1)",
          parse_exam_date_from_filename(
              "Copy of IIT_JAM_BIOTECHNOLOGY_02May2010_Sorted (1).docx")[:2]
          == ("2010-05-02", 2010))
    check("date: Mon-YYYY fallback",
          parse_exam_date_from_filename("EXAM_Feb-2019.docx")[:2]
          == ("2019-02-01", 2019))
    check("date: YYYY-only fallback",
          parse_exam_date_from_filename("EXAM_2005_sorted.docx")[1] == 2005)
    check("date: none when absent",
          parse_exam_date_from_filename("no_date_here.docx") is None)

    # answer normalisation + ground-truth matching
    check("norm MCQ", normalize_answer("MCQ", "2") == "2")
    check("norm MSQ set", normalize_answer("MSQ", "1, 3, 4") == [1, 3, 4])
    check("norm NAT float", normalize_answer("NAT", "-8") == -8.0
          and normalize_answer("NAT", "274.4") == 274.4)
    check("nat precision from stem",
          nat_precision_from_stem("... answer to 2 decimal places.") == 2
          and nat_precision_from_stem("... to the nearest integer.") == 0
          and nat_precision_from_stem("no hint") == 2)
    check("nat tolerance match",
          nat_within_tolerance(0.4149, 0.41, 2) is True
          and nat_within_tolerance(0.418, 0.41, 2) is False
          and nat_within_tolerance(None, 0.41, 2) is False)
    check("msq unordered match",
          msq_match([3, 1], [1, 3]) is True
          and msq_match("1, 3", {1, 3}) is True
          and msq_match([1, 2], [1, 3]) is False)

    # bank build/validate/counts + subtopic join + recent-window
    b = bank_new("IITJAM_PH")
    bank_add_paper(b, "k2026", "2026-02-15", 2026, "..2026..docx", 2)
    bank_add_paper(b, "k2013", "2013-02-10", 2013, "..2013..docx", 1)
    bank_add_question(b, dict(bank_id="PH-1", paper_key="k2026",
        exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
        subject="Physics", topic="Optics", subtopic="Polarization",
        stem="s1", correct_answer="2", stem_figures=["m1.png"]))
    bank_add_question(b, dict(bank_id="PH-2", paper_key="k2026",
        exam_date="2026-02-15", exam_year=2026, q_no=2, type="NAT",
        subject="Physics", topic="Optics", subtopic="Polarization",
        stem="s2", correct_answer="0.41"))
    bank_add_question(b, dict(bank_id="PH-3", paper_key="k2013",
        exam_date="2013-02-10", exam_year=2013, q_no=5, type="MSQ",
        subject="Physics", topic="Thermo", subtopic="Carnot", stem="s3",
        correct_answer="1,3"))
    check("bank validates", bank_validate(b) is True)
    check("figure flag from stem_figures",
          b["questions"][0]["figure"] is True
          and b["questions"][1]["figure"] is False)
    counts = derive_taxonomy_counts(b, latest_years=1)
    pol = counts[subtopic_key("Physics", "Optics", "Polarization")]
    car = counts[subtopic_key("Physics", "Thermo", "Carnot")]
    check("counts: subtopic pyq_count", pol["pyq_count"] == 2 and car["pyq_count"] == 1)
    check("counts: recent window = top-1 year (2026)",
          pol["recent3_count"] == 2 and car["recent3_count"] == 0)
    check("subtopic filter", len(bank_questions_for(b, "Physics", "optics",
          " Polarization ")) == 2)

    # ---- v2.6: coverage_target_for (G-12's single authority) -------------
    tgt = coverage_target_for(b, "Physics", "Optics", "Polarization")
    check("coverage: required types are the slice's attested types",
          tgt["required_types"] == ["MCQ", "NAT"])
    check("coverage: figure requirement follows any stem figure in the slice",
          tgt["requires_figure"] is True
          and coverage_target_for(b, "Physics", "Thermo",
                                  "Carnot")["requires_figure"] is False)
    check("coverage: a TAGLESS slice demands spread of exactly 1 "
          "(the proxy never invents evidence)",
          tgt["min_concepts_with_examples"] == 1
          and tgt["distinct_concept_tags"] == 0)
    check("coverage: allowed_types intersects (a mis-typed question is "
          "never demanded)",
          coverage_target_for(b, "Physics", "Optics", "Polarization",
                              allowed_types=("MCQ",))["required_types"]
          == ["MCQ"])
    check("coverage: an EMPTY slice returns the ZERO target "
          "(no examples where no evidence)",
          coverage_target_for(b, "Physics", "Optics", "Nothing")
          == {"required_types": [], "min_concepts_with_examples": 0,
              "requires_figure": False, "pyq_count": 0,
              "distinct_concept_tags": 0,
              "format_mix": {"figure": 0, "text": 0},
              "format_by_concept": {}})
    # ---- v2.10: the format contract --------------------------------------
    tf = coverage_target_for(b, "Physics", "Optics", "Polarization")
    check("format: unit mix counts figure vs text from the slice",
          tf["format_mix"] == {"figure": 1, "text": 1})
    bf = bank_new("EX")
    bank_add_paper(bf, "kf", "2026-02-15", 2026, "..f..docx", 4)
    for i, (tags, figs) in enumerate([(["Ohm's Law"], ["v_i.png"]),
                                      (["Ohm's Law"], []),
                                      (["ohm's  law"], []),
                                      (["Resonance"], [])]):
        bank_add_question(bf, dict(bank_id=f"F{i}", paper_key="kf",
            exam_date="2026-02-15", exam_year=2026, q_no=i + 1, type="MCQ",
            subject="S", topic="T", subtopic="ST", stem="s",
            correct_answer="1", concept_tags=tags, stem_figures=figs))
    tfc = coverage_target_for(bf, "S", "T", "ST")
    check("format: per-concept split with tag normalization (frequency "
          "shapes emphasis — 1 figure vs 2 text on one concept)",
          tfc["format_by_concept"] == {"ohm's law": {"figure": 1, "text": 2},
                                       "resonance": {"figure": 0, "text": 1}}
          and tfc["format_mix"] == {"figure": 1, "text": 3})
    check("format: UNRESOLVED image still counts as figure evidence",
          coverage_target_for(
              (lambda bb: (bank_add_question(bb, dict(bank_id="U1",
                  paper_key="kf", exam_date="2026-02-15", exam_year=2026,
                  q_no=9, type="MCQ", subject="S", topic="T", subtopic="SU",
                  stem="s", correct_answer="1",
                  stem_figures=["UNRESOLVED:rId9"])), bb)[1])(bf),
              "S", "T", "SU")["format_mix"] == {"figure": 1, "text": 0})
    check("format: deterministic",
          tfc == coverage_target_for(bf, "S", "T", "ST"))
    check("format: zero-figure slice demands nothing (no evidence, no "
          "demand)",
          coverage_target_for(bf, "S", "T", "SX")["format_mix"]
          == {"figure": 0, "text": 0})
    _bfp = tempfile.mktemp(suffix=".json"); bank_save(bf, _bfp)
    check("format: survives a bank save/load round trip",
          coverage_target_for(bank_load(_bfp), "S", "T", "ST") == tfc)
    bt = bank_new("EX")
    bank_add_paper(bt, "k1", "2026-02-15", 2026, "..x..docx", 1)
    for i, tags in enumerate([["Michaelis-Menten"], ["michaelis-menten "],
                              ["Inhibition"], ["pH effects"], ["Kd binding"],
                              ["Deactivation"], ["Specific activity"],
                              ["Units"], ["Turnover"]]):
        bank_add_question(bt, dict(bank_id=f"E-{i}", paper_key="k1",
            exam_date="2026-02-15", exam_year=2026, q_no=i + 1, type="MCQ",
            subject="B", topic="T", subtopic="EK", stem="s",
            correct_answer="2", concept_tags=tags))
    ct = coverage_target_for(bt, "B", "T", "EK")
    check("coverage: tag normalization collapses case/whitespace duplicates",
          ct["distinct_concept_tags"] == 8)
    check("coverage: concept spread clamps at COVERAGE_CONCEPT_CEILING",
          ct["min_concepts_with_examples"] == COVERAGE_CONCEPT_CEILING)
    check("coverage: deterministic (same slice -> identical target)",
          ct == coverage_target_for(bt, "B", "T", "EK"))

    # ---- v2.7: integration_partners + integration_target_for (G-13) -----
    check("integration: a partnerless bank is GRANDFATHERED dormant",
          integration_target_for(b, "Physics", "Optics", "Polarization")
          == {"dormant": True, "attested": False, "fusions": [],
              "unresolved": [], "pyq_count": 0})
    bi = bank_new("PH")
    bank_add_paper(bi, "kp", "2026-02-15", 2026, "..x..docx", 3)
    bank_add_question(bi, dict(bank_id="I-1", paper_key="kp",
        exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
        subject="Physics", topic="EM", subtopic="Capacitors", stem="s",
        correct_answer="1",
        integration_partners=["Physics::EM::DC and AC Circuits"]))
    bank_add_question(bi, dict(bank_id="I-2", paper_key="kp",
        exam_date="2026-02-15", exam_year=2026, q_no=2, type="MCQ",
        subject="Physics", topic="EM", subtopic="DC and AC Circuits",
        stem="s", correct_answer="2",
        integration_partners=["Physics::EM::Capacitors"]))
    bank_add_question(bi, dict(bank_id="I-3", paper_key="kp",
        exam_date="2026-02-15", exam_year=2026, q_no=3, type="NAT",
        subject="Physics", topic="EM", subtopic="Electrostatics", stem="s",
        correct_answer="4.2"))
    order = {subtopic_key("Physics", "EM", "Electrostatics"): 1,
             subtopic_key("Physics", "EM", "Capacitors"): 2,
             subtopic_key("Physics", "EM", "DC and AC Circuits"): 3}
    ti = integration_target_for(bi, "Physics", "EM", "DC and AC Circuits",
                                unit_order=order)
    check("integration: BOTH fused questions file at the LATEST partner",
          ti["attested"] is True and ti["pyq_count"] == 2
          and ti["fusions"] == [{"partners": ["Capacitors"],
                                 "bank_ids": ["I-1", "I-2"]}])
    check("integration: the EARLIER partner is never asked to teach the "
          "fusion (backward-only by construction)",
          integration_target_for(bi, "Physics", "EM", "Capacitors",
                                 unit_order=order)["attested"] is False)
    check("integration: an unfused unit in a live bank has no contract",
          integration_target_for(bi, "Physics", "EM", "Electrostatics",
                                 unit_order=order)
          == {"dormant": False, "attested": False, "fusions": [],
              "unresolved": [], "pyq_count": 0})

    # ---- v2.9: fully-resolved filing + unresolved reporting + name norm --
    bx = bank_new("EX")
    bank_add_paper(bx, "kx", "2026-02-15", 2026, "..x..docx", 3)
    # X-1: header is an EXCLUDED subtopic (not in the registry/order),
    # partner is a real unit -> must STAY at its header, leak nowhere
    bank_add_question(bx, dict(bank_id="X-1", paper_key="kx",
        exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
        subject="Physics", topic="EM", subtopic="Excluded Extras", stem="s",
        correct_answer="1",
        integration_partners=["Physics::EM::DC and AC Circuits"]))
    # X-2: header is a real unit, partner is a TYPO (resolves to nothing)
    # -> stays at header AND is reported unresolved there
    bank_add_question(bx, dict(bank_id="X-2", paper_key="kx",
        exam_date="2026-02-15", exam_year=2026, q_no=2, type="MCQ",
        subject="Physics", topic="EM", subtopic="Capacitors", stem="s",
        correct_answer="1", integration_partners=["Physics::EM::Capacitance"]))
    # X-3: fully resolved -> normal latest-partner filing
    bank_add_question(bx, dict(bank_id="X-3", paper_key="kx",
        exam_date="2026-02-15", exam_year=2026, q_no=3, type="MCQ",
        subject="Physics", topic="EM", subtopic="Capacitors", stem="s",
        correct_answer="1",
        integration_partners=["Physics::EM::DC and AC Circuits"]))
    ox = {subtopic_key("Physics", "EM", "Capacitors"): 1,
          subtopic_key("Physics", "EM", "DC and AC Circuits"): 2}
    check("v2.9: excluded-header fused question leaks into NO unit's "
          "audit set (stays at its non-unit header)",
          "X-1" not in [q["bank_id"] for q in audit_questions_for(
              bx, "Physics", "EM", "DC and AC Circuits", ox)]
          and "X-1" not in [q["bank_id"] for q in audit_questions_for(
              bx, "Physics", "EM", "Capacitors", ox)])
    check("v2.9: excluded-header fusion is never DEMANDED anywhere",
          all(not any("Excluded" in p for f in integration_target_for(
                  bx, "Physics", "EM", u, unit_order=ox)["fusions"]
                  for p in f["partners"])
              for u in ("Capacitors", "DC and AC Circuits")))
    tx = integration_target_for(bx, "Physics", "EM", "Capacitors",
                                unit_order=ox)
    check("v2.9: typo'd partner -> question stays home, REPORTED "
          "unresolved, never a Combines demand",
          "X-2" in [q["bank_id"] for q in audit_questions_for(
              bx, "Physics", "EM", "Capacitors", ox)]
          and tx["unresolved"] == [{"bank_id": "X-2",
              "unknown": ["Physics::EM::Capacitance"]}]
          and tx["attested"] is False)
    check("v2.9: fully-resolved question still files at latest partner",
          [f["bank_ids"] for f in integration_target_for(
              bx, "Physics", "EM", "DC and AC Circuits",
              unit_order=ox)["fusions"]] == [["X-3"]])
    # duplicate-name qualification (E-16): two partners, same bare name
    bd = bank_new("EX")
    bank_add_paper(bd, "kd", "2026-02-15", 2026, "..d..docx", 1)
    bank_add_question(bd, dict(bank_id="D-1", paper_key="kd",
        exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
        subject="Phy", topic="Optics", subtopic="Interference", stem="s",
        correct_answer="1",
        integration_partners=["Phy::Optics::Waves", "Phy::Mechanics::Waves"]))
    od = {subtopic_key("Phy", "Optics", "Waves"): 1,
          subtopic_key("Phy", "Mechanics", "Waves"): 2,
          subtopic_key("Phy", "Optics", "Interference"): 3}
    td = integration_target_for(bd, "Phy", "Optics", "Interference",
                                unit_order=od)
    check("v2.9: duplicate partner names are Topic-qualified (E-16)",
          td["fusions"][0]["partners"]
          == ["Mechanics :: Waves", "Optics :: Waves"])
    check("v2.9: display_norm matches across & / and / dash drift "
          "(the subtopic_key component norm)",
          display_norm("Conductors & Di–electrics")
          == display_norm("Conductors and Di-electrics"))
    check("integration: without unit_order the header subtopic files it",
          integration_target_for(bi, "Physics", "EM",
                                 "Capacitors")["pyq_count"] == 1
          and integration_target_for(bi, "Physics", "EM",
                                     "DC and AC Circuits")["pyq_count"] == 1)
    check("integration: deterministic (same bank -> identical target)",
          ti == integration_target_for(bi, "Physics", "EM",
                                       "DC and AC Circuits",
                                       unit_order=order))
    try:
        bank_add_question(bi, dict(bank_id="I-BAD1", paper_key="kp",
            exam_date="2026-02-15", exam_year=2026, q_no=4, type="MCQ",
            subject="Physics", topic="EM", subtopic="Capacitors", stem="s",
            correct_answer="1",
            integration_partners=["Physics::EM::Capacitors"]))
        check("integration: OWN subtopic as partner raises", False)
    except ValueError:
        check("integration: OWN subtopic as partner raises", True)
    try:
        bank_add_question(bi, dict(bank_id="I-BAD2", paper_key="kp",
            exam_date="2026-02-15", exam_year=2026, q_no=5, type="MCQ",
            subject="Physics", topic="EM", subtopic="Capacitors", stem="s",
            correct_answer="1", integration_partners=["just a bare name"]))
        check("integration: a non-scope-form partner raises", False)
    except ValueError:
        check("integration: a non-scope-form partner raises", True)

    # ---- v2.8: the audit boundary follows filing (handshake closure) -----
    aud_late = audit_questions_for(bi, "Physics", "EM", "DC and AC Circuits",
                                   unit_order=order)
    aud_early = audit_questions_for(bi, "Physics", "EM", "Capacitors",
                                    unit_order=order)
    check("audit set: the filing unit SOLVES both fused questions — "
          "including the one headered under the earlier unit",
          sorted(q["bank_id"] for q in aud_late) == ["I-1", "I-2"])
    check("audit set: the earlier unit DEFERS its fused question and keeps "
          "none (its notes must not teach the later ingredients)",
          aud_early == [])
    check("audit set: an unfused unit is untouched by filing",
          [q["bank_id"] for q in
           audit_questions_for(bi, "Physics", "EM", "Electrostatics",
                               unit_order=order)] == ["I-3"])
    check("audit set: teaching home and audit home are the SAME authority "
          "(every audited fused question is exactly the attested set)",
          sorted(q["bank_id"] for q in aud_late
                 if q.get("integration_partners"))
          == sorted(x for f in integration_target_for(
                 bi, "Physics", "EM", "DC and AC Circuits",
                 unit_order=order)["fusions"] for x in f["bank_ids"]))
    check("audit set: GRANDFATHERED bank -> identical to the header slice",
          audit_questions_for(b, "Physics", "Optics", "Polarization")
          == bank_questions_for(b, "Physics", "Optics", "Polarization"))
    check("audit set: no unit_order -> header filing (degenerate caller)",
          [q["bank_id"] for q in
           audit_questions_for(bi, "Physics", "EM", "Capacitors")]
          == ["I-1"])
    reg_order = unit_order_from_registry({"units": {
        "s1": {"unit_code": "EX_S1_T1_ST01", "section": "Physics",
               "topic": "EM", "name": "Electrostatics"},
        "s2": {"unit_code": "EX_S1_T1_ST02", "section": "Physics",
               "topic": "EM", "name": "Capacitors"},
        "s3": {"unit_code": "EX_S1_T2_ST01", "section": "Physics",
               "topic": "EM", "name": "DC and AC Circuits"},
        "legacy": {"unit_code": None, "section": None, "topic": None,
                   "name": "Old Unit"}}})
    check("unit_order_from_registry: (s,t,nn) ordinals from persisted "
          "unit_code; legacy units without code/triple are skipped",
          reg_order[subtopic_key("Physics", "EM", "Capacitors")] == (1, 1, 2)
          and reg_order[subtopic_key("Physics", "EM",
                                     "DC and AC Circuits")] == (1, 2, 1)
          and len(reg_order) == 3)
    check("unit_order_from_registry: tuple ordinals order cross-topic "
          "correctly (T2 after T1)",
          integration_target_for(bi, "Physics", "EM", "DC and AC Circuits",
                                 unit_order=reg_order)["attested"] is True
          and integration_target_for(bi, "Physics", "EM", "Capacitors",
                                     unit_order=reg_order)["attested"]
          is False)

    # v1.7: subtopic_key joins across syllabus-vs-header label drift (fix 3)
    def _joins(a, bb):
        return subtopic_key("S", "T", a) == subtopic_key("S", "T", bb)
    check("join: & vs and", _joins("Microbial & Plant Biotech",
                                   "Microbial and Plant Biotech"))
    check("join: en-dash vs hyphen", _joins("Enzyme Kinetics \u2013 Basics",
                                            "Enzyme Kinetics - Basics"))
    check("join: fullwidth NFKC", _joins("\uff2e\uff2d\uff32 Spectroscopy",
                                         "NMR Spectroscopy"))
    check("join: slash spacing", _joins("Optics/Polarization",
                                        "Optics / Polarization"))
    check("join: still distinguishes real differences",
          not _joins("Carnot Cycle", "Otto Cycle"))

    # v1.8: reads recompute the key, so a bank whose STORED keys are stale (as a
    # v1.6-written bank's would be) still joins correctly and counts correctly.
    b2 = bank_new("EX")
    bank_add_paper(b2, "p", "2026-02-15", 2026, "x_15-Feb-2026.docx", 2)
    bank_add_question(b2, dict(bank_id="X1", paper_key="p", exam_date="2026-02-15",
        exam_year=2026, q_no=1, type="MCQ", subject="Bio", topic="Enz",
        subtopic="Microbial & Plant Biotech", stem="a", correct_answer="1"))
    bank_add_question(b2, dict(bank_id="X2", paper_key="p", exam_date="2026-02-15",
        exam_year=2026, q_no=2, type="MCQ", subject="Bio", topic="Enz",
        subtopic="Microbial and Plant Biotech", stem="b", correct_answer="2"))
    # Simulate a stale/legacy stored key (what a weaker normaliser would have left)
    b2["questions"][0]["subtopic_key"] = "bio|||enz|||microbial & plant biotech"
    b2["questions"][1]["subtopic_key"] = "bio|||enz|||microbial and plant biotech"
    got = bank_questions_for(b2, "Bio", "Enz", "Microbial and Plant Biotech")
    check("reader ignores stale stored key (join by recompute)", len(got) == 2)
    cnts = derive_taxonomy_counts(b2)
    check("counts ignore stale stored key", len(cnts) == 1
          and list(cnts.values())[0]["pyq_count"] == 2)

    # schema acceptance + migration
    check("bank_validate accepts 1.0, 1.1 and 1.2",
          bank_validate({"schema": "notes-pyq-bank/1.0", "questions": []}) is True
          and bank_validate({"schema": "notes-pyq-bank/1.1", "questions": []}) is True
          and bank_validate({"schema": "notes-pyq-bank/1.2", "questions": []}) is True)
    try:
        bank_validate({"schema": "notes-pyq-bank/0.9", "questions": []})
        check("bank_validate rejects unknown schema", False)
    except ValueError:
        check("bank_validate rejects unknown schema", True)
    b2["schema"] = "notes-pyq-bank/1.0"
    b2["questions"][0]["subtopic_key"] = "STALE"
    _bp = tempfile.mktemp(suffix=".json"); bank_save(b2, _bp)
    reloaded = bank_load(_bp)
    check("bank_load migrates 1.0 -> current + refreshes stored key",
          reloaded["schema"] == PYQ_BANK_SCHEMA
          and reloaded["questions"][0]["subtopic_key"]
          == subtopic_key("Bio", "Enz", "Microbial & Plant Biotech"))
    try:
        bank_add_question(b, dict(bank_id="X", paper_key="k", exam_date="d",
            exam_year=2000, q_no=9, type="FOO", subject="s", topic="t",
            subtopic="st", stem="x"))
        check("non-canonical type rejected", False)
    except ValueError:
        check("non-canonical type rejected", True)
    try:
        bank_add_question(b, dict(bank_id="PH-1", paper_key="k2026",
            exam_date="2026-02-15", exam_year=2026, q_no=1, type="MCQ",
            subject="Physics", topic="Optics", subtopic="Polarization", stem="d"))
        bank_validate(b)
        check("duplicate bank_id rejected", False)
    except ValueError:
        check("duplicate bank_id rejected", True)

    # ---- v2.0 taxonomy consumer ------------------------------------------
    _man = {"exam_code": "EXBT", "subtopics": {
        "gb.cell.membranes": {"display_name": "Membrane Structure and Function",
                              "section": "General Biology", "topic": "Cell"},
        "gb.cell.signalling": {"display_name": "Cell Signalling - Endocrine and "
                               "Paracrine Pathways",
                               "section": "General Biology", "topic": "Cell"},
        "gb.genetics.linkage": {"display_name": "Linkage and Mapping",
                                "section": "General Biology",
                                "topic": "Genetics"},
        "ch.bonding.vsepr": {"display_name": "VSEPR Theory",
                             "section": "Chemistry (10+2+3 level)",
                             "topic": "Bonding"}}}
    mp = tempfile.mktemp(suffix=".json")
    _json.dump(_man, open(mp, "w", encoding="utf-8"))
    check("manifest loads with matching exam_code",
          load_subtopic_manifest(mp, "EXBT")["exam_code"] == "EXBT")
    try:
        load_subtopic_manifest(mp, "OTHER_EXAM")
        check("manifest exam_code mismatch hard-stops", False)
    except ValueError as e:
        check("manifest exam_code mismatch hard-stops", "OTHER_EXAM" in str(e))
    bad = tempfile.mktemp(suffix=".json")
    _json.dump({"exam_code": "EXBT", "subtopics": {"x": {"section": "S"}}},
               open(bad, "w"))
    try:
        load_subtopic_manifest(bad)
        check("manifest entry missing fields hard-stops", False)
    except ValueError:
        check("manifest entry missing fields hard-stops", True)

    ref2 = taxonomy_ref_for(mp)
    check("taxonomy_ref_for yields sha+count",
          len(ref2["sha256"]) == 64 and ref2["subtopics"] == 4)
    check("verify_taxonomy_ref matches", verify_taxonomy_ref(mp, ref2)[0] is True)
    with open(mp, "a", encoding="utf-8") as _f:
        _f.write(" ")
    check("verify_taxonomy_ref detects a changed manifest",
          verify_taxonomy_ref(mp, ref2)[0] is False)
    check("verify_taxonomy_ref flags a missing ref",
          verify_taxonomy_ref(mp, None)[0] is False)

    check("sid_slug takes final component",
          sid_slug("gb.cell.membranes") == "membranes"
          and sid_slug("plainslug") == "plainslug")

    num = assign_numbering(_man)
    check("numbering from manifest order",
          num["gb.cell.membranes"] == {"s_no": 1, "t_no": 1, "st_no": 1}
          and num["gb.cell.signalling"] == {"s_no": 1, "t_no": 1, "st_no": 2}
          and num["gb.genetics.linkage"] == {"s_no": 1, "t_no": 2, "st_no": 1}
          and num["ch.bonding.vsepr"] == {"s_no": 2, "t_no": 1, "st_no": 1})
    # persistence: an INSERTED subtopic must not renumber existing units, and a
    # sid removed from the manifest keeps its number (caller's ORPHANED report)
    _man2 = {"exam_code": "EXBT", "subtopics": {}}
    _man2["subtopics"]["gb.cell.transport"] = {
        "display_name": "Membrane Transport", "section": "General Biology",
        "topic": "Cell"}                       # inserted FIRST in row order
    for k, v in _man["subtopics"].items():
        if k != "gb.genetics.linkage":         # linkage removed upstream
            _man2["subtopics"][k] = v
    num2 = assign_numbering(_man2, prior=num)
    check("prior numbering preserved verbatim",
          all(num2[k] == num[k] for k in num))
    check("inserted sid appends, never renumbers",
          num2["gb.cell.transport"] == {"s_no": 1, "t_no": 1, "st_no": 3})
    check("removed sid keeps its number (orphan)",
          num2["gb.genetics.linkage"] == num["gb.genetics.linkage"])
    # collision safety under the harshest re-run: an ENTIRE prior section is
    # orphaned and a NEW section arrives. Even if the numeric s is reused, the
    # (s,t,st) TRIPLE can never collide, because st_used is seeded from EVERY
    # prior assignment (unconditionally), so new STs continue after orphans.
    _man3 = {"exam_code": "EXBT", "subtopics": {
        k: v for k, v in _man["subtopics"].items() if not k.startswith("ch.")}}
    _man3["subtopics"]["ph.mech.kinematics"] = {
        "display_name": "Kinematics", "section": "Physics", "topic": "Mechanics"}
    num3 = assign_numbering(_man3, prior=num)
    trips = [(v["s_no"], v["t_no"], v["st_no"]) for v in num3.values()]
    check("orphaned-section re-run: all (s,t,st) triples unique",
          len(trips) == len(set(trips)))
    check("orphaned section keeps numbers; new section STs never collide",
          num3["ch.bonding.vsepr"] == num["ch.bonding.vsepr"]
          and num3["ph.mech.kinematics"]["st_no"]
          > num["ch.bonding.vsepr"]["st_no"] - 1)

    units_ix = {sid: dict(_man["subtopics"][sid],
                          name=_man["subtopics"][sid]["display_name"])
                for sid in _man["subtopics"]}
    r = resolve_unit(units_ix, "gb.cell.membranes")
    check("resolve: exact sid", r["status"] == "ok" and r["via"] == "sid")
    r = resolve_unit(units_ix, "General Biology::Cell::Membrane Structure and Function")
    check("resolve: 3-part scope", r["status"] == "ok"
          and r["sid"] == "gb.cell.membranes")
    r = resolve_unit(units_ix, "membrane structure & function")
    check("resolve: bare name, norm (& vs and, case)",
          r["status"] == "ok" and r["sid"] == "gb.cell.membranes")
    r = resolve_unit(units_ix,
                     "Cell Signalling \u2013 Endocrine and Paracrine Pathways")
    check("resolve: bare name, en-dash vs hyphen",
          r["status"] == "ok" and r["sid"] == "gb.cell.signalling")
    dup = dict(units_ix)
    dup["ch.misc.linkage"] = {"display_name": "Linkage and Mapping",
                              "section": "Chemistry (10+2+3 level)",
                              "topic": "Misc", "name": "Linkage and Mapping"}
    r = resolve_unit(dup, "Linkage and Mapping")
    check("resolve: duplicate bare name -> ambiguous with both candidates",
          r["status"] == "ambiguous" and sorted(r["matches"])
          == ["ch.misc.linkage", "gb.genetics.linkage"])
    r = resolve_unit(dup, "Chemistry (10+2+3 level)::Misc::Linkage and Mapping")
    check("resolve: scope disambiguates the duplicate",
          r["status"] == "ok" and r["sid"] == "ch.misc.linkage")
    r = resolve_unit(units_ix, "Membrane")
    check("resolve: typo/partial -> none with suggestions, never auto-picked",
          r["status"] == "none" and "gb.cell.membranes" in r["suggestions"])
    r = resolve_unit(units_ix, "Cell::Membrane Structure and Function")
    check("resolve: 2-part scope refused with guidance",
          r["status"] == "none" and "3 parts" in r["detail"])

    # registry v2: sid keying + taxonomy_ref carried + 1.x load unaffected
    reg2 = registry_init("EXBT", "h", "G", [
        {"sid": "gb.cell.membranes", "unit_code": "EXBT_S1_T1_ST01",
         "name": "Membrane Structure and Function", "section": "General Biology",
         "topic": "Cell", "slug": "membranes", "role": "PYQ_WEIGHTED",
         "tier": "TIER-2", "pyq_count": 5}], taxonomy_ref=ref2)
    check("registry v2 keys by sid and carries taxonomy_ref",
          "gb.cell.membranes" in reg2["units"]
          and reg2["units"]["gb.cell.membranes"]["unit_code"] == "EXBT_S1_T1_ST01"
          and reg2["taxonomy_ref"]["sha256"] == ref2["sha256"])
    check("1.x registry load gains v2 defaults",
          reg["units"]["U"]["sid"] is None
          and reg["units"]["U"]["unit_code"] == "U")
    check("blueprint 1.0 migrate gains taxonomy_ref default",
          bp["taxonomy_ref"] is None and bp["units"][0]["sid"] is None)

    # ---- v2.12 RECALL CONTRACT (GAP-2026-09-01-RECALL-CONTRACT) ----------
    # Every finding G-14 / validate_model can emit has a fixture here or in the
    # notes_docx / notes_audit suites that kills its mutant (MUTATION_BUDGETS
    # policy: a new gate ships with fixtures that kill its own mutants).
    check("recall: complexity aliases map by band position; unknown -> None",
          normalize_complexity("Simple") == "Easy"
          and normalize_complexity(" MODERATE ") == "Medium"
          and normalize_complexity("tough", ("L", "M", "H")) == "H"
          and normalize_complexity("H", ("L", "M", "H")) == "H"
          and normalize_complexity("banana") is None
          and normalize_complexity(None) is None)
    check("recall: modal band resolves ties to the HARDER band, None on empty",
          _mode_band({"Easy": 2, "Medium": 2, "Hard": 0}, ["Easy", "Medium", "Hard"]) == "Medium"
          and _mode_band({"Easy": 3, "Medium": 1, "Hard": 1}, ["Easy", "Medium", "Hard"]) == "Easy"
          and _mode_band({"Easy": 0, "Medium": 0, "Hard": 0}, ["Easy", "Medium", "Hard"]) is None)
    rb = bank_new("RC")
    bank_add_paper(rb, "kr", "2025-02-01", 2025, "..r..docx", 6)
    for i, (typ, cx, tags, fig) in enumerate([
            ("MCQ", "Medium", ["km"], []), ("MCQ", "Medium", ["km"], []),
            ("NAT", "Hard", ["km"], ["f.png"]), ("MCQ", "Easy", ["vmax"], []),
            ("MSQ", "Hard", ["vmax"], []), ("MCQ", None, ["lineweaver"], [])], 1):
        bank_add_question(rb, dict(bank_id=f"R{i}", paper_key="kr",
            exam_date="2025-02-01", exam_year=2025, q_no=i, type=typ,
            complexity=cx, concept_tags=tags, stem_figures=fig,
            subject="Bio", topic="Enzymes", subtopic="Kinetics",
            stem=f"s{i}", correct_answer="1"))
    bank_add_question(rb, dict(bank_id="R7", paper_key="kr",
        exam_date="2025-02-01", exam_year=2025, q_no=7, type="MCQ",
        complexity="Hard", subject="Bio", topic="Enzymes",
        subtopic="Inhibition", stem="s7", correct_answer="2"))
    bank_add_question(rb, dict(bank_id="R8", paper_key="kr",
        exam_date="2025-02-01", exam_year=2025, q_no=8, type="MCQ",
        complexity="Easy", subject="Bio", topic="Enzymes",
        subtopic="Classification", stem="s8", correct_answer="3"))
    r_order = unit_order_from_registry({"units": {
        "a": {"unit_code": "RC_S1_T1_ST01", "section": "Bio", "topic": "Enzymes", "name": "Classification"},
        "b": {"unit_code": "RC_S1_T1_ST02", "section": "Bio", "topic": "Enzymes", "name": "Kinetics"},
        "c": {"unit_code": "RC_S1_T1_ST03", "section": "Bio", "topic": "Enzymes", "name": "Inhibition"},
        "z": {"unit_code": "RC_S0_T9_ST01", "section": "Chem", "topic": "Acids", "name": "pH"}}})
    rt = recall_target_for(rb, "Bio", "Enzymes", "Kinetics", unit_order=r_order,
                           allowed_types=("MCQ", "MSQ", "NAT"))
    check("recall_target_for: types, figure demand, EARLIER + SAME-SECTION partners "
          "(the earlier Chem unit is excluded), spec-lock constants echoed",
          rt["required_types"] == ["MCQ", "MSQ", "NAT"]
          and rt["requires_figure_item"] is True and rt["order_known"] is True
          and rt["cumulative_partners"] == [subtopic_key("Bio", "Enzymes", "Classification")]
          and rt["ceiling"] == RECALL_CEILING and rt["near_miss_min"] == RECALL_NEAR_MISS_MIN
          and rt["pyq_count"] == 6 and rt["profile_present"] is False)
    check("recall_target_for: tag band only at >= RECALL_MIN_PYQ_FOR_TAG_BAND "
          "(km: 3 PYQs -> Medium; vmax: 2 -> None; untagged complexity ignored)",
          rt["difficulty_by_tag"]["km"]["band"] == "Medium"
          and rt["difficulty_by_tag"]["km"]["count"] == 3
          and rt["difficulty_by_tag"]["vmax"]["band"] is None
          and rt["difficulty_by_tag"]["lineweaver"]["count"] == 1)
    check("recall_target_for: topic rung spans the WHOLE parent topic (8 PYQs, 7 banded; "
          "Hard 3 vs Medium 2 vs Easy 2 -> Hard); subtopic/exam rungs absent without a profile",
          rt["difficulty_topic"]["band"] == "Hard" and rt["difficulty_topic"]["count"] == 7
          and rt["difficulty_topic"]["counts"] == {"Easy": 2, "Medium": 2, "Hard": 3}
          and rt["difficulty_subtopic"] is None and rt["difficulty_exam"] is None
          and rt["difficulty_neutral"] == "Medium")
    rt_first = recall_target_for(rb, "Bio", "Enzymes", "Classification", unit_order=r_order)
    rt_none = recall_target_for(rb, "Bio", "Enzymes", "Kinetics")
    check("recall_target_for: first subtopic has NO partners; order-less caller "
          "reports order_known False (cumulative dormant)",
          rt_first["cumulative_partners"] == [] and rt_first["order_known"] is True
          and rt_none["cumulative_partners"] == [] and rt_none["order_known"] is False)
    check("R-12: the slice attests a top-band question -> multi-concept item required; "
          "a slice without one leaves the flag False; the trigger also fires on >= 2 "
          "concept sections; a single-concept unit with no Hard evidence demands nothing",
          rt["requires_multi_concept_item"] is True
          and rt["multi_concept_min_axioms"] == RECALL_MULTI_CONCEPT_MIN_AXIOMS
          and (lambda t0: t0["requires_multi_concept_item"] is False
                          and recall_multi_concept_required(t0, 1) is False
                          and recall_multi_concept_required(t0, 2) is True)(
                  recall_target_for(rb, "Bio", "Enzymes", "NoHardHere"))
          and recall_target_for(rb, "Bio", "Enzymes", "Classification")["requires_multi_concept_item"] is False
          and recall_multi_concept_required(rt, 1) is True)
    check("R-12: recall_is_multi_concept reads the rubric-verified axiom_concepts; "
          "junk is not evidence",
          recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": 2}}) is True
          and recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": 1}}) is False
          and recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": "x"}}) is False
          and recall_is_multi_concept({"difficulty_obs": None}) is False
          and recall_is_multi_concept({}) is False
          and recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": 3}},
                                      {"multi_concept_min_axioms": 4}) is False
          and recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": 2}},
                                      {"multi_concept_min_axioms": None}) is True
          and recall_is_multi_concept({"difficulty_obs": {"axiom_concepts": 2}},
                                      {"multi_concept_min_axioms": "x"}) is True
          and recall_is_multi_concept("junk") is False)
    check("recall_cumulative_min: ceil(core/3) floor 2; 0 without partners; "
          "ceiling yields when unattainable",
          recall_cumulative_min(6, rt) == (2, True) and recall_cumulative_min(7, rt) == (3, True)
          and recall_cumulative_min(6, rt_first) == (0, True)
          and recall_cumulative_min(13, rt) == (2, True)
          and recall_cumulative_min(14, rt) == (2, False))
    check("recall_expected_band: a CUMULATIVE item stands on the PARTNER's own bank "
          "evidence (Classification: 1 Easy PYQ -> Easy, while the rest of the topic is "
          "Hard), never on this unit's concept or subtopic rung; an unknown partner falls "
          "to topic/exam/neutral",
          rt["difficulty_by_partner"][subtopic_key("Bio", "Enzymes", "Classification")]["band"] == "Easy"
          and rt["difficulty_by_partner"][subtopic_key("Bio", "Enzymes", "Classification")]["count"] == 1
          and recall_expected_band(rt, ["km"], scope="cumulative",
                                   partner="Bio::Enzymes::Classification") == ("Easy", "partner")
          and recall_expected_band(rt, [], scope="cumulative", qtype="MSQ",
                                   partner="Bio::Enzymes::Classification") == ("Medium", "partner")
          and recall_expected_band(rt, [], scope="cumulative", partner="Bio::Enzymes::Nope")
              == ("Hard", "topic")
          and recall_expected_band({"difficulty_labels": ["Easy", "Medium", "Hard"],
                                    "difficulty_subtopic": {"band": "Easy"}}, [],
                                   scope="cumulative", partner="x") == ("Medium", "neutral"))
    check("recall_expected_band: a non-3-label vocabulary falls back to the default "
          "labels (never an index error)",
          recall_expected_band({"difficulty_labels": ["A"]}, [], True, "NAT") == ("Hard", "neutral")
          and recall_expected_band({"difficulty_labels": []}, []) == ("Medium", "neutral"))
    check("recall_expected_band: across two BANDED tags the HARDER one decides (Easy + Hard -> Hard)",
          recall_expected_band({"difficulty_labels": ["Easy", "Medium", "Hard"],
                                "difficulty_by_tag": {"a": {"band": "Easy"}, "b": {"band": "Hard"}}},
                               ["a", "b"]) == ("Hard", "concept")
          and recall_expected_band({"difficulty_labels": ["Easy", "Medium", "Hard"],
                                    "difficulty_by_tag": {"a": {"band": "Easy"}, "b": {"band": "Hard"}}},
                                   ["b", "a"]) == ("Hard", "concept"))
    check("is_clone: the threshold is INCLUSIVE (Jaccard exactly RECALL_CLONE_JACCARD is a clone; "
          "just below is not); an explicit threshold overrides",
          is_clone(frozenset("abcde"), frozenset("abcxy"), threshold=0.6) is False   # 3/7 = 0.43
          and is_clone(frozenset("abc"), frozenset("abcde"), threshold=0.6) is True  # 3/5 = 0.60 exactly
          and is_clone(frozenset("abc"), frozenset("abcd"), threshold=0.75) is True  # 3/4 exactly
          and is_clone(frozenset("abc"), frozenset("abcd"), threshold=0.76) is False)
    check("recall_cumulative_min: the FLOOR binds when ceil(core/divisor) is below it "
          "(core 1 -> 2, core 3 -> 2, core 4 -> 2, core 7 -> 3)",
          recall_cumulative_min(1, rt) == (2, True) and recall_cumulative_min(3, rt) == (2, True)
          and recall_cumulative_min(4, rt) == (2, True) and recall_cumulative_min(7, rt) == (3, True))
    check("scenario_key: drops stopwords, pure numbers and tokens of <= 2 letters; keeps content words",
          scenario_key("An enzyme at 20 mM km; the Vmax is 7") == frozenset({"enzyme", "vmax"}))
    check("recall_expected_band: a string tag is one tag; a non-list tag value is "
          "no evidence (never a crash)",
          recall_expected_band(rt, "km") == ("Medium", "concept")
          and recall_expected_band(rt, 3.5) == ("Hard", "topic")
          and recall_expected_band(rt, {"km": 1}) == ("Hard", "topic"))
    check("recall_expected_band: concept rung wins; harder tag wins across tags; "
          "near-miss +1 capped; MSQ/NAT floor; neutral when nothing carries a band",
          recall_expected_band(rt, ["km"]) == ("Medium", "concept")
          and recall_expected_band(rt, ["km"], is_near_miss=True) == ("Hard", "concept")
          and recall_expected_band(rt, ["vmax"]) == ("Hard", "topic")
          and recall_expected_band(rt, ["km", "vmax"]) == ("Medium", "concept")
          and recall_expected_band(rt_none, [], qtype="NAT")[0] == "Hard"
          and recall_expected_band({"difficulty_labels": ["Easy", "Medium", "Hard"]}, [], qtype="MCQ")
              == ("Medium", "neutral")
          and recall_expected_band({"difficulty_labels": ["Easy", "Medium", "Hard"],
                                    "difficulty_by_tag": {"x": {"band": "Easy"}}}, ["x"], qtype="MSQ")
              == ("Medium", "concept"))
    # difficulty profile — the SAME file the mock flow reads; fixture shaped as
    # blueprint_core.dp_add_paper writes it (schema 1, _meta, papers/questions).
    import tempfile as _tf2, json as _json2
    _prof = {"_meta": {"schema": 1, "exam_code": "RC",
                       "difficulty_labels": ["Easy", "Medium", "Hard"],
                       "band_edges": {"easy_max": 2, "medium_max": 5},
                       "written_by": "t", "updated_at": ""},
             "papers": {"01-Feb-2025": {"source_file": "RC_01-Feb-2025.docx", "date": "01-Feb-2025",
                                        "session": "", "q_total": 3, "q_scored": 3, "unscored": {},
                                        "explained_at": "",
                                        "questions": {"1": {"subtopic_id": "b", "score": 7, "qtype": "mcq"},
                                                      "2": {"subtopic_id": "b", "score": 4, "qtype": "mcq"},
                                                      "3": {"subtopic_id": "c", "score": 1, "qtype": "mcq"}}}},
             "excluded_papers": {}, "summary_at_write": {}}
    _pp = os.path.join(_tf2.mkdtemp(), "RC_difficulty_profile.json")
    with open(_pp, "w", encoding="utf-8") as _fh:
        _json2.dump(_prof, _fh)
    _pl, _pr = difficulty_profile_load(_pp, "RC")
    check("difficulty_profile_load: a well-formed profile loads; wrong exam, "
          "missing file and unreadable JSON return (None, reason) — NEVER raise",
          _pl is not None and _pr is None
          and difficulty_profile_load(_pp, "OTHER")[0] is None
          and "OTHER" in difficulty_profile_load(_pp, "OTHER")[1]
          and difficulty_profile_load(_pp + ".missing", "RC") == (None, "difficulty profile absent")
          and (lambda q: (open(q, "w").write("{not json"), difficulty_profile_load(q, "RC")[0] is None)[1])(_pp + ".bad"))
    rtp = recall_target_for(rb, "Bio", "Enzymes", "Kinetics", unit_order=r_order,
                            profile=_pl, subtopic_id="b")
    check("recall_target_for + profile: subtopic rung is the rubric-measured mix "
          "for THIS sid (Hard 1, Medium 1 -> tie -> Hard); exam rung is paper-level "
          "with pct; profile_present reported",
          rtp["difficulty_subtopic"]["band"] == "Hard" and rtp["difficulty_subtopic"]["count"] == 2
          and rtp["difficulty_exam"]["count"] == 3
          and abs(rtp["difficulty_exam"]["pct"]["Easy"] - 100 / 3) < 1e-9
          and rtp["profile_present"] is True
          and recall_expected_band(rtp, ["vmax"]) == ("Hard", "subtopic"))
    _corrupt = {"_meta": _prof["_meta"], "excluded_papers": {}, "summary_at_write": {},
                "papers": {"01-Feb-2025": {"date": "01-Feb-2025", "questions":
                           {"1": {"subtopic_id": "b", "score": None}, "2": {"score": "zz"},
                            "3": 5, "4": {"subtopic_id": "b", "score": 7}}}}}
    _rtc = recall_target_for(rb, "Bio", "Enzymes", "Kinetics", profile=_corrupt, subtopic_id="b")
    check("profile rungs: corrupted question records (None / non-numeric score, non-dict) "
          "are skipped, never a crash; the one sound record still counts",
          _rtc["difficulty_subtopic"]["count"] == 1 and _rtc["difficulty_subtopic"]["band"] == "Hard"
          and _rtc["difficulty_exam"]["count"] == 1)
    check("recall_exam_mix_check: a non-string band value is junk, not a band (never a crash)",
          recall_exam_mix_check([["Hard"], {"a": 1}, "Hard"], rtp)
          == ([], {"Easy": 1, "Medium": 1, "Hard": 1}))
    _fm, _ex = recall_exam_mix_check(["Easy", "Medium", "Hard", "Hard", "Hard", "Hard"], rtp)
    check("recall_exam_mix_check: largest-remainder expectation, ±tolerance, "
          "a finding names the band; dormant (None) without a profile mix",
          _ex == {"Easy": 2, "Medium": 2, "Hard": 2} and len(_fm) == 1 and "Hard" in _fm[0]
          and recall_exam_mix_check(["Easy", "Medium", "Hard", "Hard"], rtp)[0] == []
          and recall_exam_mix_check(["Easy"], rt) == ([], None))
    _ok1, _m1, _d1 = recall_verify_difficulty(
        "Medium", {"question_class": ["C-COMPUTATIONAL"], "deduction_steps": 2,
                   "axiom_concepts": 1, "speed_hack_exists": False,
                   "is_negative": False, "qtype": "mcq"})
    _ok2, _m2, _d2 = recall_verify_difficulty(
        "Easy", {"question_class": ["C-COMPUTATIONAL"], "deduction_steps": 2,
                 "axiom_concepts": 1, "speed_hack_exists": False,
                 "is_negative": False, "qtype": "mcq"})
    check("recall_verify_difficulty: agrees with the shared rubric; a label the "
          "evidence contradicts is ok=False with the measured band; empty obs is dormant",
          _ok1 is True and _m1 == "Medium" and _d1 is None
          and _ok2 is False and _m2 == "Medium"
          and recall_verify_difficulty("Hard", {})[2] is not None)
    check("recall_authoring_profile: the rubric's authoring targets for a band/qtype",
          (recall_authoring_profile("Hard", "MCQ") or {}).get("steps", (0,))[0] >= 3
          and recall_authoring_profile("Nope", "MCQ") is None)
    check("scenario_key / is_clone: same scenario with fresh numbers IS a clone; "
          "a changed context is not; empty keys never clone",
          is_clone(scenario_key("An enzyme reaction reaches half its maximum rate at 20 mM substrate; find Km"),
                   scenario_key("An enzyme reaction reaches half its maximum rate at 35 mM substrate; find Km"))
          and not is_clone(scenario_key("An enzyme reaction reaches half its maximum rate at 20 mM substrate; find Km"),
                           scenario_key("A competitive inhibitor doubles the apparent Km; what happens to Vmax"))
          and not is_clone(scenario_key(""), scenario_key("")))

    _new = registry_init("EX", "h", "G", [
        {"sid": "a", "unit_code": "EX_S1_T1_ST01", "name": "A", "role": "PYQ_WEIGHTED", "tier": "TIER-1"},
        {"sid": "b", "unit_code": "EX_S1_T1_ST02", "name": "B", "role": "PYQ_WEIGHTED", "tier": "TIER-2"},
        {"sid": "new", "unit_code": "EX_S1_T1_ST03", "name": "N", "role": "COVERAGE", "tier": "TIER-3"}])
    _prior = {"units": {
        "a": {"state": "DRAFTED", "notes_version": "0.1", "draft_ref": {"sha256": "aa"},
              "recall_contract": {"items": [{"scope": "core"}]}, "history": [{"event": "X"}],
              "final_ref": None},
        "gone": {"state": "DELIVERED", "recall_contract": {"items": []}}}}
    _c = registry_carry_over(_new, _prior)
    check("registry_carry_over: NB re-run carries state/draft_ref/recall_contract "
          "onto matching sids; None never overwrites; new sids stay fresh; orphans "
          "are not re-created",
          _c == ["a"]
          and _new["units"]["a"]["state"] == "DRAFTED"
          and _new["units"]["a"]["draft_ref"] == {"sha256": "aa"}
          and _new["units"]["a"]["recall_contract"] == {"items": [{"scope": "core"}]}
          and _new["units"]["a"]["final_ref"] is None
          and _new["units"]["b"]["state"] == "BLUEPRINTED"
          and _new["units"]["b"]["recall_contract"] is None if "recall_contract" in _new["units"]["b"] else True
          and "gone" not in _new["units"]
          and registry_carry_over(_new, None) == []
          and REGISTRY_CARRY_FIELDS[-1] == "recall_contract")
    _prior["units"]["a"]["recall_contract"]["items"].append({"scope": "cumulative"})
    check("registry_carry_over: copies are deep (a later edit to the prior record "
          "does not leak into the new registry)",
          len(_new["units"]["a"]["recall_contract"]["items"]) == 1)

    # ---- v2.1 SPEC-LOCK (defect-class tripwire) --------------------------
    # FORWARD half: every literal a Framework_Notes* spec restates in prose is
    # PINNED here to its documented value, so a moving ENGINE constant fails the
    # self-test. These pins compare the engine to a literal in this same file —
    # they say nothing about what the spec text actually reads, which is why the
    # REVERSE half below exists and is what closes the defect this was written
    # for. Neither half alone catches "one contract, two implementations".
    # v2.11 — FIGURE PALETTE is a pinned copy of figural_core's constants.
    check("spec-lock: NC §6 F-4a figure palette (pinned copy)",
          FIGURE_PALETTE["okabe_ito"][:4] == ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]
          and FIGURE_PALETTE["text_tier"]["#D55E00"] == "#C25604"
          and FIGURE_PALETTE["fills"][3:] == ["#A6DDCE", "#EDD0E0"]
          and FIGURE_PALETTE["series_cap"] == 4 and FIGURE_DPI == 300)
    # CROSS-ENGINE EQUALITY (test-only dynamic import: figural_core is NOT
    # routed to Notes and must never be imported at runtime here).
    try:
        _fc = __import__("figural_core")
        check("spec-lock: figure palette EQUALS figural_core (P1 owner)",
              FIGURE_PALETTE["okabe_ito"] == list(_fc.OKABE_ITO)
              and FIGURE_PALETTE["line_ink"] == list(_fc.ROLE_LINE)
              and FIGURE_PALETTE["text_tier"] == dict(_fc.ROLE_TEXT)
              and FIGURE_PALETTE["fills"] == list(_fc.FILLS)
              and FIGURE_PALETTE["hatches"] == list(_fc.HATCHES)
              and FIGURE_PALETTE["linestyles"] == list(_fc.LINESTYLES[:4])
              and FIGURE_PALETTE["markers"] == list(_fc.MARKERS[:4])
              and FIGURE_PALETTE["series_cap"] == _fc.SERIES_CHROMATIC_CAP
              and FIGURE_PALETTE["highlight"] == _fc.HIGHLIGHT_COLOUR
              and {int(k): tuple(v) for k, v in FIGURE_PALETTE["atom_palette"].items()}
                  == {int(k): tuple(v) for k, v in _fc.ATOM_PALETTE.items()}
              and FIGURE_DPI == _fc.FIGURAL_DPI)
    except ImportError:
        check("spec-lock: figure palette EQUALS figural_core (P1 owner)", False)
    check("F-4a helpers: text ink, fill style, overflow",
          figure_text_ink("#D55E00") == "#C25604" and figure_text_ink("k") == "#000000"
          and figure_fill_style(1)["hatch"] == "//" and figure_fill_style(1)["edgecolor"] == "#000000")
    try:
        figure_fill_style(9); check("F-4a fill overflow raises", False)
    except ValueError:
        check("F-4a fill overflow raises", True)
    try:
        import tempfile as _tf, os as _os
        _p = _os.path.join(_tf.mkdtemp(), "st_struct.png")
        _c = figure_structure_png("CCO", _p, width_in=4.0, highlight_atoms=[2])
        from PIL import Image as _Im
        _im = _Im.open(_p); _w, _h = _im.size
        import numpy as _np
        _a = _np.array(_im.convert("RGB"))
        _has = lambda hx: (_a == _np.array([int(hx[i:i + 2], 16) for i in (1, 3, 5)])).all(-1).any()
        check("F-4a structure: pinned palette, 300 dpi at width, deterministic canonical",
              _c == "CCO" and _w == 1200 and abs(_im.info.get("dpi", (300, 300))[0] - 300) < 0.01
              and _has("#C25604") and not _has("#FF0000") and _has("#0072B2"))
        _p2 = _os.path.join(_tf.mkdtemp(), "st_struct2.png"); figure_structure_png("CCO", _p2, width_in=4.0, highlight_atoms=[2])
        check("F-4a structure: identical bytes on re-render",
              open(_p, "rb").read() == open(_p2, "rb").read())
        try:
            figure_structure_png("CCO", _p2, highlight_bonds=[9]); check("F-4a structure: bad highlight is ValueError", False)
        except ValueError:
            check("F-4a structure: bad highlight is ValueError", True)
        try:
            figure_structure_png("", _p2); check("F-4a structure: empty SMILES is ValueError", False)
        except ValueError:
            check("F-4a structure: empty SMILES is ValueError", True)
    except ValueError as _e:
        check("F-4a structure: rdkit absent is soft", str(_e) == "rdkit_unavailable")
    check("spec-lock: NC §6A level colours",
          LEVEL_COLORS == {"L1": "1F4E79", "L2": "00838F", "L3": "6A1B9A",
                           "table_header": "44546A"})
    check("spec-lock: NC §6A box colours",
          BOX_COLORS == {"example": ("2E75B6", "E8F1FA"),
                         "recall": ("2E75B6", "E8F1FA"),
                         "key_points": ("2E7D32", "E4F2E4"),
                         "trap": ("C62828", "FBE4E4")})
    check("spec-lock: NC §5 density constants",
          BULLET_TARGET_WORDS == 20 and BULLET_HARD_CAP_WORDS == 25)
    check("spec-lock: NB §5 / NC §5 tier page bands",
          TIER_PAGE_BANDS == {"TIER-1": (6, 15), "TIER-2": (4, 8),
                              "TIER-3": (2, 5)})
    check("spec-lock: NA §5 G-12 concept-spread clamp",
          COVERAGE_CONCEPT_CEILING == 6)
    check("spec-lock: NC §4 B7a / NA §5 G-14 recall-contract constants",
          RECALL_CORE_PER_CONCEPT == 1 and RECALL_CUMULATIVE_DIVISOR == 3
          and RECALL_CUMULATIVE_FLOOR == 2 and RECALL_NEAR_MISS_MIN == 1
          and RECALL_CEILING == 15 and RECALL_MIN_PYQ_FOR_TAG_BAND == 3
          and RECALL_MULTI_CONCEPT_MIN_AXIOMS == 2
          and RECALL_EXAM_MIX_TOLERANCE == 1 and RECALL_CLONE_JACCARD == 0.6
          and RECALL_NEUTRAL_BAND_INDEX == 1
          and DIFFICULTY_LABELS_DEFAULT == ("Easy", "Medium", "Hard")
          and RECALL_BASES == ("concept", "partner", "subtopic", "topic", "exam", "neutral")
          and RECALL_SCOPES == ("core", "cumulative"))
    check("spec-lock: schema strings as the specs cite them",
          REGISTRY_SCHEMA == "notes-registry/2.1"
          and BLUEPRINT_SCHEMA == "notes-blueprint/2.0"
          and PYQ_BANK_SCHEMA == "notes-pyq-bank/1.2")
    check("spec-lock: NB §4 / registry vocabularies",
          ROLES == ("PYQ_WEIGHTED", "BRIDGE", "EVIDENCE_ADDED", "COVERAGE")
          and STATES == ("BLUEPRINTED", "DRAFTED", "AUDITED_PASS", "DELIVERED")
          and TIERS == ("TIER-1", "TIER-2", "TIER-3")
          and CANONICAL_TYPES == ("MCQ", "MSQ", "NAT"))
    check("spec-lock: NB §1A A-3 unit_code format",
          unit_code("EX", 1, 2, 3) == "EX_S1_T2_ST03")
    check("spec-lock: NC F-1 filename recipe INCLUDING sanitisation "
          "(the engine is the single authority; deployment-review fixture)",
          notes_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers.docx"
          and notes_filename("EX", 1, 2, 3, "membrane_structure")
          == "EX_S1_T2_ST03_membrane_structure.docx"
          and notes_filename("EX", 1, 2, 3, sid_slug("gb.cell.membranes"))
          == "EX_S1_T2_ST03_membranes.docx")

    # ---- v2.2 SPEC-LOCK: the three filename authorities ------------------
    # All three share one stem, so sanitisation cannot drift between the
    # draft, the audited file and the delivered file.
    check("spec-lock: NA _Final filename authority",
          notes_final_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers_Final.docx")
    check("spec-lock: ND _Deliver filename authority",
          notes_deliver_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers_Deliver.docx")
    check("spec-lock: all three filenames share one sanitised stem",
          notes_filename("EX", 1, 2, 3, "a-b&c")[:-len(".docx")]
          == notes_final_filename("EX", 1, 2, 3, "a-b&c")[:-len("_Final.docx")]
          == notes_deliver_filename("EX", 1, 2, 3,
                                    "a-b&c")[:-len("_Deliver.docx")])
    check("spec-lock: the three filenames are mutually distinct",
          len({notes_filename("EX", 1, 2, 3, "x"),
               notes_final_filename("EX", 1, 2, 3, "x"),
               notes_deliver_filename("EX", 1, 2, 3, "x")}) == 3)

    # ---- v2.2: docx_ref_for / verify_docx_ref ----------------------------
    _fp = tempfile.mktemp(suffix=".docx")
    with open(_fp, "wb") as _f:
        _f.write(b"original bytes")
    _ref = docx_ref_for(_fp)
    check("docx_ref_for captures filename, sha256 and size",
          _ref["filename"] == os.path.basename(_fp)
          and len(_ref["sha256"]) == 64 and _ref["bytes"] == 14)
    check("verify_docx_ref: unmodified file verifies",
          verify_docx_ref(_fp, _ref)[0] is True)
    with open(_fp, "wb") as _f:
        _f.write(b"tampered bytes!")
    _ok, _kind, _ = verify_docx_ref(_fp, _ref)
    check("verify_docx_ref: a modified file fails as 'sha256'",
          _ok is False and _kind == "sha256")
    _ok, _kind, _ = verify_docx_ref(_fp, _ref,
                                    expected_filename="OTHER_UNIT.docx")
    check("verify_docx_ref: wrong unit attached fails as 'filename' — a "
          "DIFFERENT defect from a hand-edit, so it is reported separately",
          _ok is False and _kind == "filename")
    check("verify_docx_ref: absent ref fails as 'missing_ref'",
          verify_docx_ref(_fp, None)[1] == "missing_ref")
    check("verify_docx_ref: absent file fails as 'not_found'",
          verify_docx_ref(tempfile.mktemp(suffix=".docx"), _ref)[1]
          == "not_found")

    # ---- v2.2: registry schema forward-compatibility ---------------------
    check("registry: 2.1 is now EMITTED, and 1.x/2.0 still load",
          REGISTRY_SCHEMA == "notes-registry/2.1"
          and {"notes-registry/1.0", "notes-registry/2.0"}
          <= set(REGISTRY_SCHEMAS_ACCEPTED))
    check("registry_init emits the 2.1 per-unit fields",
          all(k in registry_init("EX", "h", "PG",
                                 [{"sid": "s", "name": "N", "role": "COVERAGE",
                                   "tier": "TIER-3",
                                   "unit_code": "EX_S1_T1_ST01"}]
                                 )["units"]["s"]
              for k in ("draft_ref", "final_ref", "audit_summary")))
    _rp = tempfile.mktemp(suffix=".json")
    _reg = registry_init("EX", "h", "PG",
                         [{"sid": "a.b.c", "name": "N", "role": "COVERAGE",
                           "tier": "TIER-3", "unit_code": "EX_S1_T1_ST01"}])
    registry_save(_reg, _rp)
    _loaded = registry_load(_rp)
    check("registry_load defaults the 2.1 per-unit fields on any schema",
          all(k in _loaded["units"]["a.b.c"]
              for k in ("draft_ref", "final_ref", "audit_summary")))
    check("registry_load leaves the 2.1 defaults empty (additive, not lossy)",
          _loaded["units"]["a.b.c"]["draft_ref"] is None
          and _loaded["units"]["a.b.c"]["audit_summary"] is None)

    # ---- v2.4 FINAL-AUDIT FIXTURES --------------------------------------
    # (A) The D-1 gate must SEE the shared builder's bullets. Before v2.4 it
    # counted only <w:numPr> paragraphs, so a notes_docx document — which
    # renders a literal glyph — reported ZERO bullets and passed 60-word ones.
    _b1 = mini_docx("x", extra_xml=(
        "<w:p><w:r><w:t>\u2022  " + " ".join(["w"] * 60) + "</w:t></w:r></w:p>"))
    check("v2.4-A: a glyph bullet is COUNTED (the shared builder emits no "
          "numPr, so this is the only way G-1 can see it)",
          bullet_word_counts(_b1) == [60])
    check("v2.4-A: ...and density_gate therefore FAILS it",
          density_gate(_b1, "TIER-3", 3)[0] is False)
    _b2 = mini_docx("x", extra_xml=(
        "<w:p><w:pPr><w:numPr/></w:pPr><w:r><w:t>"
        + " ".join(["w"] * 30) + "</w:t></w:r></w:p>"))
    check("v2.4-A: the legacy numPr convention still counts (documents built "
          "before notes_docx keep working)",
          bullet_word_counts(_b2) == [30])
    _b3 = mini_docx("x", extra_xml=(
        "<w:p><w:r><w:t>\u2022  short bullet here</w:t></w:r></w:p>"))
    check("v2.4-A: the glyph itself is not counted as a word",
          bullet_word_counts(_b3) == [3])
    _b4 = mini_docx("plain prose that is not a bullet at all and runs long "
                    + " ".join(["w"] * 40))
    check("v2.4-A: a non-bullet paragraph is still ignored",
          bullet_word_counts(_b4) == [])

    # (B) A slug with no ASCII must not collapse to an empty, COLLIDING name.
    _n1 = notes_final_filename("EX", 1, 1, 1, "\u092a\u093e\u0920")
    _n2 = notes_final_filename("EX", 1, 1, 1, "\u0aaa\u0abe\u0aa0")
    check("v2.4-B: a non-ASCII slug still yields a non-empty stem",
          "__" not in _n1 and _n1.endswith("_Final.docx"))
    check("v2.4-B: two DIFFERENT non-ASCII slugs cannot collide "
          "(they used to produce one identical filename)", _n1 != _n2)
    check("v2.4-B: an all-punctuation slug also cannot collide",
          notes_final_filename("EX", 1, 1, 1, "...")
          != notes_final_filename("EX", 1, 1, 1, "---"))
    check("v2.4-B: the fallback is DETERMINISTIC across calls",
          notes_final_filename("EX", 1, 1, 1, "\u092a\u093e\u0920") == _n1)
    check("v2.4-B: all three authorities share the fallback stem",
          notes_filename("EX", 1, 1, 1, "\u092a\u093e\u0920")[:-len(".docx")]
          == _n1[:-len("_Final.docx")])
    check("v2.4-B: an ASCII slug is COMPLETELY unaffected (no existing "
          "filename moves)",
          notes_filename("EX", 1, 2, 3, "pH & buffers")
          == "EX_S1_T2_ST03_pH_buffers.docx")

    # ---- SPEC-LOCK, REVERSE HALF (the drift direction that produced the bug)
    # The pins above compare the engine to a literal in THIS file, so they fire
    # only when the ENGINE moves. The defect they were written for ran the other
    # way: the engine was right and Framework_NotesCreate's prose was stale, and
    # every pin above passes verbatim against that stale text (verified). So the
    # spec text itself is read and compared, the same way explain_engine's
    # T3-DRIFT-LOCK reads Framework_PYQPrepare §S3-5b. Missing spec = loud crash,
    # never a silent pass — also as in T3-DRIFT-LOCK.
    _spec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "Framework_NotesCreate.md"), encoding="utf-8").read()
    _f1 = _spec.split("F-1 Naming:", 1)[1].split("F-2 ", 1)[0]
    check("spec-lock/reverse: NC F-1 defers to the engine and states the "
          "sanitisation (fails on the pre-v2.2.1 prose recipe)",
          "notes_core.notes_filename" in _f1
          and "non-alphanumeric" in _f1 and "sanitis" in _f1)
    _cmap = _spec.split("Colour map (constants", 1)[1].split(
        "No other colour", 1)[0]
    _engine_hex = set(LEVEL_COLORS.values())
    for _fg, _bg in BOX_COLORS.values():
        _engine_hex |= {_fg, _bg}
    check("spec-lock/reverse: NC §6A colour literals == LEVEL_COLORS/BOX_COLORS",
          set(re.findall(r"\b[0-9A-F]{6}\b", _cmap)) == _engine_hex)
    _d5 = _spec.split("D-1 Bullet length:", 1)[1].split("\n", 1)[0]
    check("spec-lock/reverse: NC §5 D-1 word counts == the engine constants",
          [int(x) for x in re.findall(r"\d+", _d5)]
          == [BULLET_TARGET_WORDS, BULLET_HARD_CAP_WORDS])

    _b7 = _spec.split("B7a RECALL CONTRACT", 1)[1].split("B8 ", 1)[0]
    check("spec-lock/reverse: NC §4 B7a defers to recall_target_for / "
          "recall_expected_band / recall_cumulative_min and names the ladder rungs",
          "notes_core.recall_target_for" in _b7
          and "notes_core.recall_expected_band" in _b7
          and "notes_core.recall_cumulative_min" in _b7
          and all(r in _b7 for r in RECALL_BASES))
    check("spec-lock/reverse: NC §4 B7a restates NO recall-contract number "
          "(RECALL_CEILING / floor / divisor live in the engine)",
          not re.search(r"\bceiling(?: of| is| =)?\s+\d+", _b7, re.I)
          and not re.search(r"\bfloor(?: of| is| =)?\s+\d+", _b7, re.I))

    print(f"notes_core self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_core.py — shared Notes pipeline core. Run with --self-test.")
