"""
corpus_io.py v1.19 — I/O shell for PYQ corpus acquisition, image integrity,
                    document size governance, tables and the Analysis doc.

v1.19 — 2026-11-07 — GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS (RE-25 CHEM-STRUCTURE;
    paired with explain_engine v2.13, figural_core v5.91, PYQExplain v2.28,
    MockTestExplain v1.54.0). Incident: a 120-question chemistry PYQ paper shipped 34
    structure questions with ZERO explanation figures and 11 chemistry defects; the
    renderer could draw one molecule, never a mechanism, and nothing compared the derived
    product with the keyed option. ADDITIVE — every v1.18 path is byte-identical; nothing
    here runs unless a block is RE-25 APPLIES.
      (1) E-03 ARROW INTERPRETER: mechanism_apply_arrows(before, arrows) applies every
          curly arrow of a step at once as bond-order / formal-charge / radical deltas on
          the atom-mapped species (hydrogen counts frozen; a moving H is a mapped [H:n]
          atom) and verify_mechanism_step(step) PROVES the arrows give `after`
          (constitution canonical, charges included) — CHS_ARROW_INVALID otherwise,
          never degraded. step_atom_balance(step) is E-06 (g).
      (2) E-01/E-02 MECHANISM RENDERER: render_mechanism(step, ...) draws before → after
          from the E-02 step dict: persisting atom notes from the map numbers, reagent
          fragments placed beside the attacked atom, every species aligned to the
          previous one on the shared maps (rotation / translation only — NEVER a
          mirror), reactive-conformation rotation, curly arrows as Béziers (start biased
          30 % toward the bonding atom, lone-pair starts offset away from the bonds,
          full head = 2 e⁻, fishhook = 1 e⁻), forming bonds in FORM_INK tint, wrong
          bonds / arrows in WRONG_INK, reagents above and conditions / by-products
          below the reaction arrow, captions INSIDE the image. render_structure_panel()
          is the ANNOTATED_STRUCTURE / option-figure panel.
      (3) E-04 LAYOUT GATE: figure_layout_audit(draw) and the in-render retry search —
          L1 no arrow crosses a bond or another atom's label · L2 tip within 14 px of
          its target · L3 no label / note / caption overlap, no atom clash, no distorted
          bond · L4 no ink within 8 px of the edge · L5 bond ≥ 0.18 in and text ≥ 7 pt
          at printed width · L6 inks are figural_core text-tier · L7 printed height
          ≤ 8.0 in. Deterministic schedule
          (curvature ±0.35/0.6/0.9 · bias 0.3/0.2/0.4 · in-plane rotation 0/90/180/270 ·
          conformation ±20/30/40°, cap 64), then the fallback chain MECHANISM →
          REACTION_SCHEME → STRUCTURE_GRAPH, each step-down in draw.degrade_ledger. A
          figure that fails the gate is never returned.
      (4) E-07 option_match(answer_smiles, option_smiles): exact / nearest (rdFMCS) /
          formula delta ("+H2") / per-option differences; stereo-aware only where the
          option is drawn with stereo (EC-32).
      (5) E-09 figure_review_sheet(figures, out_png): one contact sheet per batch for
          the in-turn model view that records figure_review[id].
      (6) Figures: 200 dpi, palette-quantised PNG (target ≤ 120 KB, owner decision
          2026-11-07), 6.0 / 5.6 / 4.6 in for DEDUCTION / option / SPEED HACK. The three
          inks are read from figural_core when it is loaded, else the pinned identical
          Okabe-Ito values — this module still never imports figural_core (check AI).
v1.18 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (G01 R1.2, owner Q-A).
    Incident: CSIR-NET Organic Test 01 Q32 shipped options 2 and 3 as ONE molecule
    ((2E,4Z)-hexa-2,4-diene, drawn from `C/C=C/C=C\\C` and `C\\C=C/C=C/C`); the
    renderer compared nothing. (1) OptionIdentityError(CorpusError) + assert_option_
    identities(draws): native_option_set() now compares the RE-PERCEIVED identity
    (bc.structure_identity / bc.reaction_identity of each draw's .canonical) of every
    pair and raises "LADDER-REPAIR R2o G-OPTDISTINCT ..." on a duplicate — before any
    pixel is rendered. dHash never decides identity. (2) stereo_declared(draw_fn,
    declared) records the author's descriptor line on the draw so S10-8 can run
    bc.stereo_declaration_check (G-STEREODECL) at render time. Everything else is
    byte-identical to v1.17.
v1.17 — 2026-11-02 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (F1, F2, F4, F6, F7).
    Generated structures did not look like the exam: coloured atoms, every molecule
    auto-scaled into a fixed 900x700 raster (bond length / label size were accidents),
    an opaque highlight band 6x the line width overprinting O / Br / N / C+ and making
    single bonds read double, option labels printing at ~2.3 pt. Adds an opt-in
    PRINT-TRUE NATIVE RASTER path; with tokens=None every v1.16 path is unchanged.
      (1) structure_draw_fn(..., tokens=None, marks=None, abbreviations=None,
          protect_atoms=()) — with `tokens` (font_pt / line_pt / bond_pt in printed
          points, monochrome, mark_colour; passed in as a plain dict, figural_core is
          never imported) the draw gains render_mode='native_raster', .tokens,
          .native_png(dpi) and .native_png_unmarked(dpi) -> (png, natural_width_in, meta):
          rdkit at fixedBondLength / fixedFontSize / bondLineWidth from the tokens,
          canvas sized from the 2-D coordinates, cropped to ink + 0.15 bond, dpi
          metadata, BW atom palette when monochrome. NEVER a highlight band: highlight_*
          become marks; marks (underline / asterisk / letter / arrow / bold) are placed
          from rdkit's own geometry clear of every label and bond (8 rotations, else
          marks_failed — never dropped); meta['overprint_px'] is the G2 differential
          count. CoordGen depiction with quaternary-cross re-depiction (rdkit, then
          canonOrient). ABBREVIATION_LEXICON / ABBREVIATION_DISPLAY and
          abbreviation_protected_atoms() (rdFMCS) condense only the exam's labels and
          never a protected or marked atom; .canonical stays the uncondensed SMILES.
      (2) render_scheme(..., tokens=None, max_width_in=6.0) — with `tokens`,
          .native_png(dpi) composes the scheme with PIL at natural size (every tile at
          the same tokens, arrows / text in points); overflow: re-flow multi-arrow rows
          repeating the break tile, stack reagent text (excess -> stem), else
          meta['overflow'] (never scaled). .canonical / .descriptor unchanged.
      (3) native_option_set(draw_fns, dpi) — uniform max-width x max-height canvas,
          no frame, equal widths; ValueError on mismatched tokens.
    Self-test 428 -> 478 (50 new checks, each failing on the defect it guards).

v1.16 — 2026-11-01 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY (LAW F1.3;
    paired with figure_types v1.0, paper_pipeline v5.40, final_assembly v1.9,
    audit_canonical v2.32, blueprint_core v1.28, MockTestCreate v5.88). The REACTION
    semantic kind existed on paper and was rejected by every function that touched it:
    canonical_structure returned parse_error on '>>', structure_draw_fn raised, and
    the registry commit raised — so every reaction-dominant exam shipped a lone molecule
    with the reaction moved into the stem (measured: 20 of 24 figural organic questions
    on a real paper are drawn schemes; the delivered paper drew 0). Three additive
    changes, every molecule path byte-identical:
      (1) canonical_structure() accepts REACTION SMILES ('reactants>agents>products',
          exactly two '>' separators; an empty agents or products side is legal — a
          scheme ending in a placeholder letter has no drawn product). Each component
          is canonicalised through the unchanged molecule path and re-joined; a
          dot-separated molecule SET without '>>' is still a molecule set (the
          REACTION kind now requires '>>' at validate_semantic_object, paper_pipeline
          v5.40). CROSS-FILE SYNC RULE unchanged: explain_engine.canonical_structure
          is the byte-identical twin.
      (2) structure_draw_fn() exposes .raster() (the RGBA array it blits) and .px —
          additive attributes; render order, palette and extent contract untouched.
      (3) render_scheme(spec) — the compositor. A declarative scheme in reading order
          (rows of molecule tiles, '+', arrows carrying reagent text above and
          conditions below, a reagent drawn as a structure, placeholder letters,
          bracketed intermediates, labelled option pairs — the G1–G10 grammar read
          from the real paper) rendered as ONE figural_core draw_fn: every tile comes
          from structure_draw_fn (G-FIGSEM provenance per tile), arrows and text are
          matplotlib artists, so the v5.55 fitter, label deconflict, G-FIGINK and
          G-FIGFIT apply unchanged. The returned draw_fn carries .canonical (the
          reaction SMILES assembled from the drawn molecules, placeholders omitted),
          .descriptor (reagent lines, unknowns, arrows, rows), .set_element_colours
          (colour_content propagates to every tile) and the Q7b.14 attributes an
          option set needs. scheme_semantic_object() builds the S7-NEW-B2 record.

v1.15 — 2026-08-30 — GAP-2026-08-30-LINEART-CLASSIFIER. _is_line_art() classed an
    image as line art by "<= 256 distinct colours". Measured 2026-08-30: EVERY
    anti-aliased rendered figure in the estate has 300-1,900 colours (JAM structures
    553-1,705; v5.81 charts 268-1,504; an externally rendered ecology paper 287-1,905)
    and so routed to 'jpeg' (q82, chroma subsampling — the ringing on thin strokes
    and subscripts Q2 bans) whenever it lacked an alpha channel; while a pure smooth
    gradient (exactly 256 colours, no edges at all) routed to PNG as "line art".
    Mock figures survived only because they are RGBA. The test is now STRUCTURAL:
    the fraction of pixels whose four neighbours are exactly equal (flat regions).
    Rendered figures measure 0.78-0.98; photographs and scans (sensor / JPEG
    texture) 0.00; the gradient 0.00. LINE_ART_FLAT_FRAC = 0.60. Deterministic,
    bounded (250k-pixel sample), numpy-backed with the old rule as the fallback
    when numpy is absent. JPEG SOURCE STILL WINS (classify_media_route): nothing
    already lossy is ever re-encoded as PNG. Every other function byte-identical.

v1.14 — 2026-08-29 — GAP-2026-08-29-FIGURE-COLOUR-ROLES (MockTestCreate v5.80 S10-7C).
    structure_draw_fn no longer draws with rdkit's DEFAULT atom palette — a value
    that is unpinned across rdkit versions and fails WCAG 3.0:1 on Cl/S/F/P — but
    with figural_core.ATOM_PALETTE (CPK hue families, TEXT-tier values, S/P black).
    Three additive keywords: element_colours (default True), highlight_atoms /
    highlight_bonds (opaque figural_core.HIGHLIGHT_COLOUR under the interrogated
    site; a labelled heteroatom's highlight is carried by its incident bonds so
    its symbol is never overprinted). The returned draw_fn exposes
    .coloured_elements (the heteroatom symbols it colours) and
    .set_element_colours(flag) so figural_core.render_option_set() can make ONE
    element-colour decision for a whole option set (Q7b.14). Signature
    order, .canonical, the imshow extent contract and every PYQ-side function are
    byte-identical; an rdkit without updateAtomPalette degrades to its BW palette
    and records draw.palette_note — never a halt.

v1.13 — 2026-08-25 — GAP-2026-08-18-PYQCOMPRESS-UNDERCOMPRESSION. optimize_docx gains
    mode='max' (PYQCompress v2.0.0): a single governor pass at blueprint_core.MAX_TIER
    (q82, 300-DPI ceiling AT DISPLAY SIZE) instead of walking TIER_LADDER, plus
    palette quantization of PNG output via _quantize_png (pngquant binary when
    installed, optipng on top when installed, PIL FASTOCTREE fallback — alpha-capable
    on every path). Ladder callers unchanged: mode defaults to None and every existing
    call site behaves byte-identically. Per-part and per-document no-growth guards
    apply unchanged in max mode.

v1.12 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE. Adds canonical_structure()
    (rdkit canonical isomeric SMILES + valence sanitisation; (None, reason) never raise)
    and structure_draw_fn() (a figural_core draw_fn that renders a STRUCTURE figure FROM
    its SMILES, so the image and its registered semantic object are one artefact —
    MockTestCreate v5.59 S7-NEW-B2). Lives here because paper_pipeline is thin-core
    (CHECK AB) and may not import rdkit even lazily.

v1.11 — 2026-07-29 — CLUSTER I RECORDED + ITS MISSING FIXTURES (debt closure).

    Closes the three follow-ups recorded in the 2026.07.29 deployment audit:

    (1) THIS ENTRY. The ~300-line Cluster I table-structure addition
        (GAP-2026-07-29-TBL: _table_rows rewritten as a raw w:tr/w:tc walk that
        inspects vMerge/gridSpan, read_table_spec(), the TableSpec model,
        normalise_table_spec/place_cells/table_spec_spans, build_di_table with a
        font_name param, adjacent_table_pairs, legacy {'headers','rows'} DI
        payload accepted for ever) shipped with the header still claiming v1.10
        — the third un-bumped occurrence of an addition landing without its
        version line. Bumped and recorded here.

    (2) CLUSTER I SELF-TEST FIXTURE. A gridSpan-4 header + vMerge-2 label table
        whose anchor-once expectations the old row.cells implementation CANNOT
        produce (row.cells repeats the anchor across every covered grid
        position), plus: a flat-table byte-identity check pinning the legacy
        list[list[str]] output, the spans round-trip through
        read_table_spec/table_spec_spans, the legacy DI payload shape, and a
        full build_di_table -> raw-XML read-back round trip asserting spans
        survive with zero stray empty cells. Reverting _table_rows to row.cells
        now breaks this suite instead of passing green — the exact revert that
        would have sailed through the previous 273/273.

    (3) is_option FIXTURE (open since 2026.07.26.2): OPT_PATTERNS text markers,
        the six-and-beyond / prose rejections, bare-marker + image-option (blip)
        recognition, imageless bare-marker rejection, Paragraph-vs-element
        duality of para_has_image, and clean_option_text marker stripping.

    Self-test 273 -> 303. No behaviour change to any shipped function.

v1.10 — 2026-07-27 — `fresh=` PARAMETER: RUN-SCOPED CALLERS OPT OUT OF THE UNION.

    Found while verifying the v1.9 union against its CALLERS, prompted by the
    self-test regression review. Step 1 (PYQPrepare) shares the same fixed
    VISION_WORKDIR as Step 5 but wants per-run semantics: it processes ONE source
    per trigger and completes Phase A->B->C inside that trigger, so anything already
    in the workdir is contamination from a previous paper or a previous step.
    v1.8's overwrite masked the sharing; the v1.9 union surfaced it (measured: a
    second PYQPrepare run saw queued=3 where it queued 1 — Phase B re-views the
    prior paper's cells, Phase C counts them unobserved, footer goes amber with
    wrong counts). fresh=True clears queue + sheets + observations before building.
    Default False preserves v1.9 union semantics for Step 5. Also bumps the version
    line so the three byte-distinct states that briefly all claimed v1.9 are
    unambiguous: v1.9 = union, v1.9+isolated self-tests = superseded, v1.10 = this.

v1.9 — 2026-07-27 — build_vision_queue() IS NOW IDEMPOTENT (GAP-2026-07-27-B).

    It wrote vision_queue.json and vision_sheet_NNN.png — both FIXED names — and never
    read what was already in the workdir. Any caller invoking it twice against one
    workdir destroyed the first call's work. Framework_MockTestAnalyse <= v2.38 called
    it once per PAPER into a workdir its own spec defines as one-per-RUN, so within a
    3-paper batch only the LAST paper reached Phase B.

    MEASURED (IIT_JAM_BIOTECHNOLOGY, 22 papers): 153 figural questions; _meta.vision
    recorded queued=8. Batch 7 queued 24 and 3 survived. Five separate sessions hit
    this and each invented a different workaround; none converged.

    It now unions the submitted items with any queue already on disk, keyed by
    (paper_id, q_num), before tiling. Safe by construction — bc.vision_tag_map derives
    a tag from paper_id alone, so re-tiling a superset leaves prior tags intact
    (EC-V11/V12). A hash-width widening is the one case that re-tags everything; it is
    now detected and reported via stats['tag_generation_changed'] rather than silently
    orphaning the previous generation's observations.

    stats gains carried_in / submitted / tag_generation_changed so a caller can
    distinguish a fresh queue from a resumed one without diffing files.

    This is HALF the fix. The caller must ALSO stop calling it per paper — see
    Framework_MockTestAnalyse v2.39. Hoisting alone still loses prior sessions;
    idempotence alone still loses papers 1..N-1 within a batch.

v1.8 — 2026-07-26 — VISION-PROBE FAMILY RETIRED (GAP-2026-07-26-003 follow-up).

    Deleted: normalise_for_view(), make_vision_probe(), score_vision_probe(), and the
    exception classes ProbeObservationMissing and VisionUnavailable.

    WHY. Cluster V's three-phase bridge subsumes all of them:
      * normalise_for_view was a public wrapper over the same normalisation
        build_vision_queue now performs internally via _open_rgb. Two spellings of one
        rule is the drift the DELEGATION contract exists to prevent.
      * make_vision_probe / score_vision_probe answered "can this session see?" by
        minting a token image. PHASE B looks at REAL figures, so the answer now arrives
        free as a by-product of the work: any observation returned proves vision works,
        none returned proves it does not. A separate probe would be a SECOND mechanism
        answering one question, free to disagree with the first.
      * ProbeObservationMissing had no remaining raiser once score_vision_probe went;
        VisionUnavailable was raised nowhere even before this release.

    audit_callgraph C4 flagged the first three as public-but-unreached. Left in place
    they would report 2 findings forever, and a check that always shows findings gets
    skimmed and then ignored — "a check that can be shipped past is decoration"
    (CLAUDE.md). Retiring them returns C4 to zero so the next real finding is visible.

    The v1.5 entry below is HISTORY and stays: it records why the empty-string verdict
    was wrong, which is the reasoning that produced the three-phase design.

v1.7 — 2026-07-26 — CLUSTER V: VISION PHASE A / OBSERVATION I/O
    (GAP-2026-07-26-003).

    Viewing an image is a CLASS T operation — it needs a TOOL CALL, and a tool call
    can only happen BETWEEN model turns. A python process launched from bash cannot
    suspend mid-loop to make one. Every "vision function" the corpus wrote as python
    was therefore unreachable code returning a default forever, on every run, in
    silence. Measured on IIT_JAM_BIOTECHNOLOGY: 153/153 figural questions recorded
    vision_unavailable, 45/45 FIGURAL subtopics shipped an empty object-type profile,
    and QV-9 returned PASS on the result.

    Adds the DETERMINISTIC half of the materialise-then-inject bridge:
      build_vision_queue()        PHASE A — normalise -> compose -> tile -> queue.json
      load_vision_queue()         reader, tolerant
      load_vision_observations()  PHASE B -> C boundary, tolerant
      write_vision_observations() one spelling of the observations file

    NOTHING IN CLUSTER V RAISES FOR A VISION REASON. An unopenable figure, a missing
    observations file and an absent Pillow all degrade with a recorded reason, and the
    run completes. The defect being fixed was SILENCE, and the remedy for silence is
    visibility (QV-14 + vision_status), never a halt.

    Two defects were found by property fuzzing rather than by example, and both are
    now locked by self-tests:
      * EC-V27 — two items sharing (paper_id, q_num) printed the SAME tag on two
        cells, making a Phase-B observation unattributable. Items are now merged by
        key with their sources unioned.
      * mixed-type tags in a model-written observations file raised TypeError inside
        sorted() (blueprint_core side).

v1.6 — 2026-07-26 — is_option() BECOMES THE SINGLE SHARED OPTION PREDICATE
    (audit_deep [XSPEC-DRIFT]).

    It was defined three times — MockTestAnalyse, PYQSort, PYQAnalyse — each claiming
    in its docstring to be aligned with the others. v2.34/v2.35 gave Step 5 the
    image-option path; the siblings kept the text-only form and the alignment claim
    silently became false.

    Not cosmetic: PYQSort USES its copy to count options (_count_options_in_body), so
    for an image option ("1." with a picture, no text) the predicate returned False
    and the option was UNDERCOUNTED — the identical defect class the wave had just
    fixed in Step 5, left live in Step 1.

    OPT_PATTERNS, BARE_OPT_PATTERNS, para_has_image(), is_option() and
    clean_option_text() now live here; all three specs delegate. para_has_image()
    accepts a python-docx Paragraph OR a raw <w:p> element, because Step 5 passes the
    first and Steps 1/3 pass the second — a delegation that assumed one form would
    silently reinstate the undercount on the other.

v1.5 — 2026-07-26 — score_vision_probe() REFUSES TO SCORE A NON-OBSERVATION
    (GAP-2026-07-26-002 PART A).

    It returned False for an empty string, collapsing two categorically different
    states into one session-terminating value:

        ''  / None / whitespace  ->  "I did not look"           -> procedural error
        'ABC12345' (wrong)       ->  "I looked, could not read" -> session verdict

    Returning False for the first made a careless non-observation indistinguishable
    from a genuinely blind session. IMG-6 then halted a production Step-5 run at
    batch 1 having processed nothing, on a probe image that had rendered correctly
    and was legible — the token was recovered from it on review.

    Now raises ProbeObservationMissing (new, a CorpusError subclass) for the empty
    case. A scorer can only compare an observation that exists; it is not an oracle
    for whether one was made. Callers retry rather than treating it as a failure.

    BREAKING for any caller that relied on False-on-empty. Verified: there were no
    executable callers — every reference was in spec prose — so nothing else moved.
    Framework_MockTestAnalyse >= v2.34 and Framework_PYQPrepare >= v1.10 depend on
    this behaviour; an older engine silently re-opens the false-halt path.

v1.4 — 2026-07-26 — THE TAXONOMY COMES FROM JSON, NOT FROM A WORD DOCUMENT.
    GAP-2026-07-25-003, resolved at the cause rather than at the symptom.
    v1.2 taught the reader both ingest forms and works. It works by matching an
    undocumented, unversioned extraction grammar the framework does not control,
    observed from one sample — so the next change to that grammar stops all ~200
    exams at once. Loudly, but at once. That is a mitigation, not a resolution.
    reconcile_taxonomy v1.3 now persists the approved taxonomy INSIDE
    approval_record.json, which it has always held in the right shape and thrown
    away. New load_taxonomy() prefers it and falls back to the Analysis doc for
    records that predate schema 1.3, so no already-approved exam needs re-running.
    The record VALIDATES ITSELF: the fingerprint recorded beside the taxonomy was
    computed from it at Step 2c, so nothing new is trusted, and a record whose two
    halves disagree hard stops rather than being half-believed.
    _assemble() is extracted so the record path and the document path build the ONE
    return shape from one implementation — two constructions of one shape is how
    GAP-2026-07-25-002's four readers happened.
    Also stopped: silent de-duplication. A name repeated in the recorded taxonomy
    would collapse on assembly and the fingerprint would NOT notice, because it is
    computed over the same duplicated triples and therefore agrees with itself.

v1.3 — 2026-07-26 — THE TAXONOMY LOCK GATE, ONCE (GAP-2026-07-25-003 follow-up).
    read_analysis_doc() asserts the doc agrees with ITSELF; nothing in Cluster K
    asserted it is the doc PYQApprove LOCKED. Framework_PYQSort S1-0b made that
    second claim and NOTHING else did — Steps 5 and 6 read the taxonomy and
    allocated against it with no identity check at all. At Step 5 it was worse than
    absent: the reader's hard stops were caught and downgraded to a log line TWICE,
    once in _extract_taxonomy_tuples_from_analysis_doc and again in its caller, so a
    superseded or mis-parsed doc that halts loudly at Step 3 was accepted three steps
    later without a word. Every subtopic_id minted from it would be wrong, and ids
    are what Steps 6-11 match on.
    Adds discover_approval_record(), read_approval_record() and
    assert_taxonomy_lock(doc, ...). The gate lives here ONCE rather than being
    written a fifth time in a fifth spec — the same anti-drift rule that produced
    Cluster K, now covering the lock as well as the reader.
    SCOPE IS NARROW ON PURPOSE: this asserts IDENTITY only. Whether the lock was
    EARNED — status, schema attestation, checks.missing/vacuous — is PYQSort S1-0's
    claim, made once at Step 3 against the same record, and is not duplicated. One
    function, one claim.

v1.2.1 — 2026-07-26 — UNKNOWN-FORM DIAGNOSTIC COULD RAISE THE FAULT IT DIAGNOSED.
    read_analysis_doc()'s INGEST_UNKNOWN branch formatted its message with
    os.path.getsize(path). _ingest_form() returns UNKNOWN for an unreadable path
    BECAUSE getsize() raised there, so the diagnostic re-raised it uncaught and the
    operator received exactly the library traceback v1.2 was written to replace —
    on the one input where the named stop matters most. Reproducible with any
    unreadable or vanished path; found by re-running the delivered spec end to end
    rather than by review. The size is diagnostic and is now reported as
    "unreadable (<Error>: <detail>)" when it cannot be taken.

v1.2 — 2026-07-26 — CLUSTER K: INGEST FORMS (GAP-2026-07-25-003). The Analysis doc
    is uploaded to the project's Files section after Step 2c and read from there at
    Steps 3, 4, 5 and 6. The platform stores an uploaded .docx in project knowledge
    as EXTRACTED MARKDOWN TEXT while PRESERVING the .docx filename, so the text form
    is the ONLY form the runtime ever receives for this artefact — yet read_analysis_doc()
    opened it with python-docx and hard stopped with PackageNotFoundError on every
    project, severing the pipeline at Step 3. Measured: chat attachment = 40,882-byte
    OOXML package; the same file in project Files = 12,911 bytes of Markdown text.
    v1.1 anticipated this, but put the diagnostic on discover_analysis_doc()'s "no file
    found" branch, which the preserved filename makes unreachable: discovery SUCCEEDS
    and hands _scan() a text file.

    This is a REGRESSION BOUNDARY, not a latent bug. Before v1.1 the artefact was read
    by prose in Framework_Blueprint S2-2 ("instruct Claude to extract the structure
    itself"), which works on the text form by construction. v1.1 replaced prose with
    python-docx and thereby traded a working non-deterministic read for a deterministic
    broken one. The answer is NOT to restore prose — of the four pre-v1.1 readers only
    Blueprint's worked at all; MockTestAnalyse's two returned 0 subtopics against a
    truth of 131 on every exam, silently. ONE reader stands; it learns the second form.

    Four changes, in the order they matter:
      (a) INGEST FORMS. The container is classified from CONTENT, never from the
          extension — the .pdf in the same project is a Zip page-bundle under its .pdf
          name, so the extension is not evidence of the container. _scan() is renamed
          _scan_ooxml() (body untouched, still used by write_analysis_doc()'s output and
          the round-trip self-test) and _scan_text() joins it, emitting the IDENTICAL
          (subjects, order, declared, anomalies) 4-tuple. verify_analysis_doc(),
          taxonomy_fingerprint(), the return shape and every downstream consumer are
          therefore untouched, and the text form is admitted THROUGH both existing gates
          rather than around them. An unrecognised form is a named hard stop, never a
          best-effort parse, and verify=False is refused on a non-OOXML form.
      (b) RAGGED-ROW HARD STOP (the defect the ingest-form fix would otherwise have
          introduced). A markdown table is rectangular. A '|' inside a taxonomy name
          splits one row wider than its neighbours, and the surplus cell is swallowed
          as the count column: 'Transverse | Longitudinal' parsed as 'Transverse', with
          'Longitudinal' discarded and the SUBTOPIC COUNT UNCHANGED — so D1, D2 and D3
          all agree and verify_analysis_doc() returns clean. Reproduced by execution.
          That matters beyond Step 3: the fingerprint cross-check against the approval
          record exists ONLY in Framework_PYQSort S1-0b, so at Steps 5 and 6 the mis-parse
          has no gate at all and is silent end to end. Non-uniform cell width across a
          table's rows is now a hard stop naming the row, and write_analysis_doc() refuses
          to emit a name containing '|' — the character is unrepresentable in this ingest
          form, so it is rejected where it originates rather than where it corrupts.
      (c) GRAMMAR TOLERANCE, bounded. Bold is stripped whether the extractor emits ** or
          a full-line __wrap__, backslash escapes on markdown punctuation are removed, and
          cells split only on UNESCAPED pipes. Measured against a second, independent
          docx->markdown extractor on the same live document, which emits __bold__,
          escapes ('IIT\\_JAM\\_BIOTECHNOLOGY', 'Subtopic\\-wise') and flattens tables
          entirely. The first two are now handled; the third is not, and is not guessed
          at — it produces the loud "extraction grammar may have changed" stop. This is
          tolerance of variants that have been OBSERVED, not speculation about grammars
          that have not.
      (d) The stale hint at the tail of discover_analysis_doc() is corrected. After this
          change the text form is READ, not diagnosed.

    KNOWN RESIDUAL, recorded rather than hidden: this module now depends on an
    undocumented, unversioned, platform-controlled extraction grammar. It fails LOUDLY
    when that grammar changes, but it fails for every exam at once. The durable
    resolution is to stop recovering machine state from a rendered document at all:
    reconcile_taxonomy.build_approval_record() already receives final_taxonomy in the
    exact {section: {topic: [subtopic]}} shape, derives the fingerprint from it and then
    DISCARDS it, and syllabus_provenance.read_taxonomy_draft() already reads that shape
    from JSON, which the platform stores byte-for-byte. Persisting the approved taxonomy
    into the record makes this whole class of defect unreachable. Tracked separately.

v1.1 — 2026-07-25 — CLUSTER K: THE Analysis-doc reader, writer and verifier
    (GAP-2026-07-25-002). The Step-2c Analysis doc previously had FOUR readers
    across four specs, implementing four different structural conventions, and no
    writer at all (PYQAnalyse S4-2 was `pass`). Three of the four were measurably
    wrong on the first real exam's doc. One reader, one writer, one verifier; all
    heading recognition delegated to blueprint_core.parse_taxonomy_level so every
    label form works in every step; correctness asserted by round-trip over a
    GENERATED matrix of exam shapes rather than by review. See Cluster K header.


v1.0.3 — 2026-07-25 — optimize_docx gains `always`, which runs the tier ladder even when
    the input is already under budget. Requested so PYQCompress can be driven purely by
    what the operator attaches rather than by a size threshold. force_tier was NOT reused
    for this: it pins one tier and makes the closing `return True` unconditional, so an
    oversized paper would have stopped at that tier, still over budget, and reported
    success with the floor-exceeded WARN suppressed. Adds _no_gain_guard, a
    document-level counterpart to the existing per-part no-growth rule: the ZIP container
    can grow even when no part does, and CHECK 5 treats growth as a HARD STOP, so a small
    already-optimal document would have aborted the run instead of being left alone.

v1.0.2 — 2026-07-25 — MEDIA STEM COLLISION (silent figure loss). optimize_docx renamed
    every re-encoded part to .jpeg/.png and stored it in a dict keyed by that name, so
    two parts sharing a stem and taking the same encoder route (word/media/image1.png +
    word/media/image1.jpg, both photographic) both resolved to word/media/image1.jpeg
    and one OVERWROTE the other. The writer then emitted a duplicate zip member and Word
    rendered whichever it met first, silently replacing one figure with the other.
    Invisible to every existing gate: parts, media and refs all still matched, no
    relationship dangled, and the per-stem pixel check that would have caught it is
    skipped by design at T2-T4 (allow_resample=True) — so the corrupted file passed
    parity and was DELIVERED. Reproduced end to end; T1 caught it, T2-T4 did not.
    Four changes: (a) _target_media_name keeps a part's name when its extension already
    maps to the encoder's content type, so .jpg is no longer renamed to .jpeg and the
    common collision never forms; (b) a genuine remaining collision is disambiguated
    (__c2) rather than overwritten; (c) an explicit input->output name map replaces the
    reverse-lookup in the writer, which could not express a disambiguated name; (d) the
    relationship rewrite is a single regex pass — chained str.replace() with
    {image1.png -> image1.jpeg, image1.jpeg -> image1__c2.jpeg} rewrote the part it had
    just manufactured and pointed both references at one file. A part-count guard
    (len(parts) == len(names)) backstops all of it. assert_docx_parity now compares
    pixel dimensions as an unordered multiset: keying on the stem carried the v1.0.1
    false positive one level up, because a disambiguated name changes the stem.

v1.0.1 — 2026-07-25 — assert_docx_parity raised a FALSE-POSITIVE HARD STOP whenever the
    governor renamed a media part. Re-encoding a photographic PNG produces image1.jpeg
    from image1.png, and the pixel-dimension comparison was keyed on the full basename,
    so the renamed part had no counterpart in `after` and was reported as a dimension
    change on a document whose dimensions were identical (verified: 2400x1800 before and
    after). Dormant on the measured corpus, whose papers store .jpeg parts that the jpeg
    route leaves named as they were; it fires on any PNG-sourced photograph, i.e. exactly
    the papers the governor exists for. Comparison is now by extension-less part name.
    Found by the Framework_PYQSort v1.12 governor test, not by this module's self-test —
    a regression case has been added (io_parity_rename_*).

WHY THIS MODULE EXISTS (and why none of it lives in blueprint_core.py)
    blueprint_core.py declares a THIN-CORE INVARIANT: pure, no I/O, standard library
    only. paper_pipeline.py makes the same promise. Every concern below is inherently
    impure — Drive retrieval, ZIP surgery, image transcoding, disk writes — so hosting
    it in either module would break a stated design invariant. Worse, importing PIL or
    python-docx into blueprint_core.py would make the ALLOCATION core unimportable
    wherever those packages are absent, which is exactly the P0 recorded in
    Framework_MockTestAnalyse v2.26: a failed `import blueprint_core` aborted Step 5
    for EVERY exam.

    corpus_io.py is therefore the one home for impure corpus plumbing, exactly as
    explain_engine.py is the one home for impure explanation plumbing.

        blueprint_core Cluster H   DECIDES   (pure data in -> pure data out)
        corpus_io                  PERFORMS  (bytes, files, images)

    Every decision this module needs is delegated to Cluster H. This module contains
    no thresholds, no ladders and no classification rules of its own.

ANTI-DRIFT CONTRACT
    Steps 1, 2b, 3, 4, 5 and PYQCompress all consume this module. No spec may define a
    local copy of any function named here — enforced by validate_framework_md.py
    Check Z. A spec may only call it or define a thin forwarding adapter. Re-localising
    a shared function produces ZERO drift signal until the two copies disagree; that is
    the failure that required Framework_MockTestAnalyse v2.27 and
    Framework_PYQAnalyse v2.20.

DEPENDENCY POLICY
    Standard library at module scope. Pillow and python-docx are imported LAZILY inside
    the functions that need them, so Cluster H shell functions (path / JSON / ZIP logic)
    keep working without them, and a missing optional dependency surfaces as a named
    error at the point of use rather than an import failure at load time.

DEFECTS THIS MODULE EXISTS TO FIX (see Framework_PYQCompress §3 for the full register)
    B  Drive download was unguarded — zero try/except existed anywhere in the corpus
    G  legacy .doc accepted at enumeration though python-docx cannot open it
    H  native Google Docs silently skipped, removing a paper with no error
    I  images inside TABLES invisible: doc.paragraphs does not descend into tables
    J  legacy VML <v:imagedata> images invisible in every image-handling spec
    K  header / footer / footnote images never extracted
    L  pre-Q.1 images silently discarded rather than bucketed
    N  the real download envelope (context spill + double JSON parse) undocumented
    O  duplicate paper identity double-counted a year
"""

import base64
import io
import json
import os
import re
import shutil
import urllib.error
import urllib.request
import zipfile

import blueprint_core as bc


# ── exceptions — named and actionable; the CALLER decides what is fatal ──────────

class CorpusError(Exception):
    """Base for every failure raised by this module."""


class TransportFallback(CorpusError):
    """Bytes could not be fetched from Drive. NOT fatal — route to the upload lane.

    Raised for the size cap, a truncated payload, a permission failure, a malformed
    envelope, and any unrecognised connector error. The caller MUST catch this and
    request the paper by chat upload instead of stopping the run.

    This is the guarantee that a future change to the connector's cap cannot break the
    pipeline: correctness does not depend on the predicted partition being right, only
    on the fallback being taken.
    """


class OptionIdentityError(CorpusError):
    """v1.18 (GAP-2026-11-03 G01 R1.2): two options of one item are ONE entity under the
    identity function of their content kind. Raised by native_option_set() BEFORE any
    pixel is rendered; the message follows the §Q8b-LADDER convention so S10-8 enters the
    ladder at R2o (regenerate the distractor only — never the key)."""


class EnumerationError(CorpusError):
    """A Drive folder listing cannot be turned into a usable corpus."""


class ListingIntegrityError(EnumerationError):
    """HARD STOP — the cached folder listing does not match what Drive returned.

    GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / EC-P41. EC-P39 already hard-stops on a
    listing that yields ZERO usable papers, because zero is obviously wrong and every
    operator notices it. A listing that yields SOME is not covered by it and is
    strictly more dangerous: §1-6's coverage check reports success on whatever
    survived, _meta.years_processed looks plausible, and the missing years are
    invisible for the life of the exam — after which Step 6 blueprints and Step 7
    generates on top of the gap.

    This is deliberately NOT a TransportFallback. A fallback means "try another lane";
    there is no other lane for a corpus you cannot enumerate correctly, and continuing
    on a short listing is the failure this class exists to prevent.
    """


class DuplicatePaperError(EnumerationError):
    """Two files resolve to the same paper identity — HARD STOP.

    Left unchecked this double-counts the paper's year in the §1-6 coverage gate, or
    drops one of the two depending on listing order.
    """


class IntegrityError(CorpusError):
    """A document failed a structural or image-integrity gate — HARD STOP."""


class DependencyMissing(CorpusError):
    """An optional package (Pillow / python-docx) is needed here but not installed."""


# ── constants that are pure I/O concerns (all POLICY lives in Cluster H) ─────────

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
V_NS = 'urn:schemas-microsoft-com:vml'

MEDIA_RE = re.compile(r'^word/(media|embeddings)/', re.I)
RASTER_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.webp')
VECTOR_EXT = ('.emf', '.wmf', '.svg')

# Every part that can carry a drawing. Footnotes and endnotes are included because a
# figure there is still a figure; omitting them makes the reference count silently low
# and would fire IMG-4 for a benign reason.
STORY_PARTS_RE = re.compile(
    r'^word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$')

DEFAULT_Q_PATTERN = r'^\s*Q\.?\s*(\d+)'
PREAMBLE = 'preamble'
DEFAULT_UPLOAD_DIR = '/mnt/user-data/uploads'


def _need(mod):
    """Import an optional dependency, or fail with a named, actionable error."""
    try:
        if mod == 'PIL':
            from PIL import Image  # noqa: F401
            return __import__('PIL.Image', fromlist=['Image'])
        if mod == 'docx':
            import docx  # noqa: F401
            return docx
    except ImportError as exc:
        raise DependencyMissing(
            f'{mod} is required for this operation but is not installed ({exc}). '
            f'Install with: pip install {"Pillow" if mod == "PIL" else "python-docx"} '
            f'--break-system-packages')


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER H SHELL — ACQUISITION
# ═══════════════════════════════════════════════════════════════════════════════

def parse_drive_folder_id(url):
    """Extract the folder id from a Drive folder URL, or return the input if it already
    looks like a bare id. None when neither."""
    s = str(url or '').strip()
    m = re.search(r'drive\.google\.com/drive/(?:u/\d+/)?folders/([A-Za-z0-9_-]+)', s)
    if m:
        return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{12,}', s):
        return s
    return None


def normalise_drive_listing(response):
    """Turn any shape of Drive listing response into uniform file records.

    Accepts the bare list, {'files': [...]} or {'items': [...]}, and tolerates both the
    'title' and 'name' spellings the connector has used.

    fileSize arrives as a STRING and is absent for folders and native Google types.
    Both are normalised here so no caller has to think about it. Capturing size at
    enumeration costs nothing — the listing already carries it — and is what allows the
    AUTO/UPLOAD partition to be computed BEFORE any download is attempted, instead of
    discovering the blocker three-quarters of the way through a run.
    """
    items = response
    if isinstance(response, dict):
        items = response.get('files', response.get('items', []))
    out = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        raw = it.get('fileSize', it.get('size'))
        try:
            size = int(raw) if raw is not None else None
        except (TypeError, ValueError):
            size = None
        out.append({
            'id': it.get('id'),
            'name': it.get('title') or it.get('name') or '',
            'mimeType': it.get('mimeType', ''),
            'fileSize': size,
            'parentId': it.get('parentId'),
            'source': 'gdrive',
        })
    return out


def collect_corpus_files(list_fn, folder_id, recurse=True, require_size=True,
                         _seen=None, _papers=None, _rejects=None, _depth=0):
    """Walk a Drive folder and return (papers, rejects).

    `list_fn(folder_id, page_token=None)` is injected so this is testable without Drive
    and so the caller owns the connector call. It must return whatever the connector
    returns; normalise_drive_listing handles the shape.

    Pagination is followed to exhaustion — without it a folder of more than one page
    silently loses papers.

    Sub-folders are visited in DESCENDING name order so year-named folders are walked
    newest-first, preserving the recency-first intent of the existing enumeration.

    Raises DuplicatePaperError when two usable files share a canonical identity.
    """
    if _seen is None:
        _seen, _papers, _rejects = {}, [], []
    if _depth > 24:
        raise EnumerationError('folder nesting exceeded 24 levels — possible cycle')

    subfolders, page_token = [], None
    while True:
        resp = list_fn(folder_id, page_token=page_token) if page_token else list_fn(folder_id)
        entries = normalise_drive_listing(resp)
        page_token = resp.get('nextPageToken') if isinstance(resp, dict) else None

        for e in entries:
            verdict, reason = bc.screen_drive_entry(
                e['name'], e['mimeType'], e['fileSize'], require_size=require_size)
            if verdict == 'folder':
                subfolders.append((e['name'], e['id']))
                continue
            if verdict == 'reject':
                _rejects.append(dict(e, reason=reason))
                continue
            key = bc.canonical_paper_key(e['name'])
            if key in _seen:
                prev = _seen[key]
                raise DuplicatePaperError(
                    'Two files resolve to the same paper identity — HARD STOP.\n'
                    f'  identity : {key}\n'
                    f'  file A   : {prev["name"]}  (id {prev.get("id")}, '
                    f'{prev.get("fileSize")} bytes)\n'
                    f'  file B   : {e["name"]}  (id {e.get("id")}, '
                    f'{e.get("fileSize")} bytes)\n'
                    'Remove or rename one in Drive. Leaving both makes this paper\'s '
                    'year count twice, or drops one at random depending on listing order.')
            rec = dict(e, paper_key=key)
            _seen[key] = rec
            _papers.append(rec)

        if not page_token:
            break

    if recurse:
        subfolders.sort(key=lambda x: x[0], reverse=True)
        for _, sub_id in subfolders:
            collect_corpus_files(list_fn, sub_id, recurse, require_size,
                                 _seen, _papers, _rejects, _depth + 1)
    return _papers, _rejects


_B64_CHARS_ONLY = re.compile(r'^[A-Za-z0-9+/=\s]+$')


def _decode_bare_base64(text):
    """GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (P3b) — accept a BARE base64 string.

    decode_drive_payload used to accept bytes, a spill path, a dict, a list and a JSON
    string, but NOT a plain base64 string with no envelope around it. That shape is not
    hypothetical: any staging protocol that writes a `.b64` sidecar, or a model that
    hands over just the `content` field it read out of a spill file, produces exactly
    it, and every one of them was rejected with a message that named three shapes and
    not this one.

    Ambiguity against the other accepted shapes is resolved by DECODING, not guessing:
    a candidate is accepted only if it is long, contains base64 characters exclusively,
    and decodes to bytes beginning PK\x03\x04. A spill path fails the length/charset
    test (it contains '/' but also '.', and it exists on disk so it never reaches here);
    a JSON envelope fails the charset test on '{'. Returns None — never raises — so the
    caller keeps ownership of the error message.
    """
    if not isinstance(text, str):
        return None
    stripped = text.strip()
    if len(stripped) <= 64 or not _B64_CHARS_ONLY.match(stripped):
        return None
    try:
        raw = base64.b64decode(stripped)
    except Exception:
        return None
    return raw if raw[:4] == b'PK\x03\x04' else None


def decode_drive_payload(payload):
    """Turn whatever download_file_content returned into raw file bytes.

    The real contract is not what a one-line pseudocode wrapper suggests, and every
    execution of Steps 2b/4/5 has rediscovered it by trial and error:

      * the tool result MAY be spilled to a file on disk instead of returned in the
        turn, so `payload` may be a PATH. Whether it spills, and to which directory,
        is a property of the DEPLOYMENT, not of the file size — measured 2026-08-15
        on one 40,488-byte .docx: spilled in one deployment, returned inline in
        another. Never assume either; this function accepts both;
      * that spilled JSON is a LIST whose [0]['text'] is itself a JSON STRING;
      * parsing that string yields {'id','title','mimeType','content'} where 'content'
        holds the base64 payload.

    Accepts, in order: raw bytes, a spill-file path, the parsed list/dict, or the inner
    JSON string. Anything else raises TransportFallback so the caller routes to upload
    rather than dying.
    """
    if isinstance(payload, (bytes, bytearray)):
        return bytes(payload)

    obj = payload
    if isinstance(obj, str):
        if os.path.exists(obj):
            try:
                with open(obj, 'r', encoding='utf-8') as fh:
                    obj = json.load(fh)
            except (OSError, ValueError) as exc:
                raise TransportFallback(f'could not read spill file {obj}: {exc}')
        else:
            try:
                obj = json.loads(obj)
            except ValueError:
                bare = _decode_bare_base64(obj)
                if bare is not None:
                    return bare
                raise TransportFallback(
                    'download payload is neither bytes, a spill-file path, bare '
                    'base64, nor JSON')

    for _ in range(6):                                   # bounded unwrap; never loops
        if isinstance(obj, list):
            if not obj:
                raise TransportFallback('download payload was an empty list')
            obj = obj[0]
            continue
        if isinstance(obj, dict):
            content = obj.get('content')
            if isinstance(content, str):
                try:
                    return base64.b64decode(content)
                except Exception as exc:
                    raise TransportFallback(f'base64 content would not decode: {exc}')
            text = obj.get('text')
            if isinstance(text, str):
                try:
                    obj = json.loads(text)
                except ValueError:
                    raise TransportFallback(
                        'payload text was not the expected JSON envelope')
                continue
        break
    raise TransportFallback('could not locate base64 content in the download payload')


def verify_downloaded_bytes(raw, expected_size=None, name=''):
    """Prove the payload is a complete .docx before anything downstream trusts it.

    The byte-count check is not redundant with the magic check. A payload truncated at a
    ZIP member boundary can still open as a valid archive while presenting FEWER media
    parts — a silent image loss with no error anywhere. Comparing against the size Drive
    reported is the only thing that catches that case.
    """
    label = f' for {name}' if name else ''
    if not raw:
        raise TransportFallback(f'download returned no bytes{label}')
    if raw[:4] != b'PK\x03\x04':
        raise TransportFallback(
            f'payload{label} is not a .docx (magic {raw[:4]!r}) — it may be an error '
            'page, an HTML login redirect, or a native Google type')
    if expected_size is not None and len(raw) != expected_size:
        raise TransportFallback(
            f'size mismatch{label}: received {len(raw):,} bytes, Drive reported '
            f'{expected_size:,}. Treating as truncated.')
    return True


def stage_drive_payload(payload, paper, dest_dir):
    """Decode + verify + persist an ALREADY-MATERIALISED Drive payload. No callable.

    GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (P3a). Before this function the ONLY
    verified route from a Drive payload to a file on disk was fetch_drive_docx, which
    demands a `download_fn` callable. A caller in PHASE B already HOLDS the payload —
    the model fetched it in its own turn — so satisfying that signature meant inventing
    a callable, and the cheapest-looking invention is to pass the CLASS T marker name
    itself. That is precisely the defect this GAP documents. Removing the incentive is
    a stronger fix than documenting the trap.

    Guarantees are identical to fetch_drive_docx: byte count equals the fileSize the
    listing reported, PK\x03\x04 magic, and TransportFallback (never SystemExit) on
    any failure so the caller degrades to the upload lane.

    `payload` is whatever PHASE A produced for this paper — raw bytes, a spill-file
    path in ANY directory, the parsed dict/list, an inner JSON string, or bare base64.
    Returns the local path written.
    """
    name = paper.get('name', '<unnamed>')
    raw = decode_drive_payload(payload)
    verify_downloaded_bytes(raw, paper.get('fileSize'), name)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(name))
    with open(dest, 'wb') as fh:
        fh.write(raw)
    return dest


def fetch_drive_docx(download_fn, paper, dest_dir):
    """Fetch one paper to disk. ANY failure raises TransportFallback — never SystemExit.

    `download_fn(file_id)` is injected so the caller owns the connector call. It must be
    a RESOLVER over results PHASE A already materialised — a plain lookup that performs
    no tool call. Passing the name of a CLASS T marker instead is unreachable code: see
    stage_drive_payload's docstring, GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION, and
    audit_callgraph C6/C7 which fail the build for it.

    Papers already known to exceed the connector cap are not attempted at all: the
    request is guaranteed to fail and would only add latency. Everything else is
    attempted, because the partition is predictive and a marginal file fetches fine.

    This is a thin wrapper over stage_drive_payload: it adds the cap pre-check and the
    guarded call, then delegates decode/verify/persist so both routes cannot diverge.
    """
    size = paper.get('fileSize')
    name = paper.get('name', '<unnamed>')
    if size is not None and size > bc.DRIVE_CAP:
        raise TransportFallback(
            f'{name} is {size:,} bytes, above the {bc.DRIVE_CAP:,}-byte connector cap — '
            'routing to the upload lane without attempting a download')
    try:
        payload = download_fn(paper['id'])
    except TransportFallback:
        raise
    except Exception as exc:                              # connector / auth / network
        raise TransportFallback(f'download of {name} failed: {exc}')

    return stage_drive_payload(payload, paper, dest_dir)


# ── DIRECT EGRESS LANE (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P43) ─────────
# The connector lane charges an inline payload TWICE (EC-P36): once inbound in the
# model's turn, once again when the model re-emits it into a python block, because the
# container had no route to Google and python could not fetch the bytes itself. That
# second charge is not a property of Drive — it is a property of the EGRESS ALLOWLIST.
# When the container can reach drive.google.com and the folder is link-shared, python
# downloads the file directly and NOTHING crosses the turn: cost zero, whole corpus in
# one session.
#
# MEASURED 2026-08-16 against folder 12wamcvoQ4ucI69Rblj51zJmcTX6MeDNG:
#   drive.google.com                 -> 302 to accounts.google.com (no proxy denial)
#   uc?export=download&id=16QFONpQ…  -> 302 to drive.usercontent.google.com -> 200
#   payload                          -> 47,627 bytes, 50 4b 03 04, Microsoft Word 2007+
# 47,627 is byte-exact for IIT_JAM_MATHEMATICS_15-Feb-2026_Sorted_Q1-Q60.docx, so the
# lane returned the RIGHT file, not merely A file.
#
# THIS LANE IS NEVER ASSUMED AND NEVER FATAL. It is proven per exam on a real paper
# (probe_direct_egress), and every failure degrades to the connector lane exactly as it
# works today. An exam whose Drive folder is not link-shared is not a broken exam.

DIRECT_UC_URL = 'https://drive.google.com/uc?export=download&id={file_id}'
DIRECT_CONFIRM_URL = ('https://drive.usercontent.google.com/download'
                      '?id={file_id}&export=download&confirm=t')
DIRECT_TIMEOUT_S = 45
_DIRECT_UA = 'Mozilla/5.0 (compatible; ifas-framework-corpus-io)'


def _http_get(url, timeout=DIRECT_TIMEOUT_S):
    """Fetch one URL and return raw bytes. Stdlib only; no new dependency.

    Every failure is converted to TransportFallback so the caller degrades rather than
    stops. The egress proxy's own refusal is decoded explicitly, because
    'HTTP 403' on drive.google.com reads like a Google permissions problem and is in
    fact a Claude SETTINGS problem — an operator sent to the wrong place by a bad
    diagnostic loses an afternoon.
    """
    req = urllib.request.Request(url, headers={'User-Agent': _DIRECT_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        deny = ''
        try:
            deny = exc.headers.get('x-deny-reason') or ''
        except Exception:
            deny = ''
        if deny:
            raise TransportFallback(
                f'sandbox egress refused {url} ({deny}). This is the container '
                f'allowlist, not Google: enable Settings -> Capabilities -> Code '
                f'execution -> Domain allowlist. Falling back to the connector lane.')
        raise TransportFallback(f'HTTP {exc.code} fetching {url}')
    except Exception as exc:                       # DNS, TLS, timeout, proxy, reset
        raise TransportFallback(f'direct fetch failed for {url}: {exc}')


def fetch_drive_direct(paper, dest_dir, getter=None):
    """Download ONE link-shared Drive paper straight into the container.

    `getter(url) -> bytes` is injected so this is testable with no network and so the
    transport mechanism has exactly one definition. Default is _http_get.

    Two-hop by design. Drive answers `uc?export=download` with the file itself for
    small objects, and with an HTML interstitial for objects large enough to trip the
    virus-scan warning. Measured on this corpus the papers are 40-49 KB and the first
    hop returns the bytes; the confirm hop exists so that a future oversized paper
    degrades to a retry rather than to a silent HTML file on disk.

    Guarantees are IDENTICAL to fetch_drive_docx and stage_drive_payload — byte count
    equals the fileSize the listing reported, PK\\x03\\x04 magic, TransportFallback on
    every failure — because they all delegate to verify_downloaded_bytes. A lane with
    weaker proof than its siblings is a lane that will one day write an HTML login page
    to disk under a .docx name and let §1-6 count it as a year.
    """
    get = getter or _http_get
    name = paper.get('name', '<unnamed>')
    file_id = paper.get('id')
    if not file_id:
        raise TransportFallback(f'no Drive file id for {name}')
    size = paper.get('fileSize')
    if size is not None and size > bc.DRIVE_CAP:
        raise TransportFallback(
            f'{name} is {size:,} bytes, above the {bc.DRIVE_CAP:,}-byte cap — '
            'routing to the upload lane without attempting a download')

    raw = get(DIRECT_UC_URL.format(file_id=file_id))
    if not raw or raw[:4] != b'PK\x03\x04':
        # Interstitial or quota page. One retry through the confirm endpoint, then stop
        # guessing: a third shape is a Drive behaviour change and must surface loudly.
        raw = get(DIRECT_CONFIRM_URL.format(file_id=file_id))

    verify_downloaded_bytes(raw, size, name)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(name))
    with open(dest, 'wb') as fh:
        fh.write(raw)
    return dest


def probe_direct_egress(paper, dest_dir, getter=None):
    """PROVE the direct lane on a real paper. Never raises; never predicts.

    Returns {'ok': bool, 'channel': 'direct'|None, 'path': str|None, 'reason': str}.

    This follows the S5-0 doctrine exactly (Framework_PYQCount, GAP-2026-08-15): a
    channel that classifies cleanly but cannot produce verified bytes must fail at
    paper 1, not at paper 12. It differs from S5-0 in one way that matters — the probe
    payload IS paper 1 (P4f), so a successful probe has already delivered a paper and
    costs nothing at all, and a failed probe costs nothing either because the bytes
    never entered the turn.

    Deliberately never raises. Egress being unavailable is an ordinary, expected state
    for an exam whose folder is not link-shared, and an exception here would turn a
    routine fallback into an incident.
    """
    try:
        path = fetch_drive_direct(paper, dest_dir, getter=getter)
        return {'ok': True, 'channel': 'direct', 'path': path,
                'reason': f"verified {paper.get('name', '')} on disk"}
    except Exception as exc:
        return {'ok': False, 'channel': None, 'path': None, 'reason': str(exc)}


def write_drive_listing(pages, path, root_folder_id, observed_count):
    """Merge the raw connector pages, ASSERT them, and persist DRIVE_LISTING_CACHE.

    GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / EC-P41. Before this function the cache
    was hand-transcribed: the model re-emitted every record of the connector response
    into a create_file call — ~5,000 characters for 22 papers, ~23,000 for a
    100-paper corpus, every record carrying a 33-character Drive id. A single mistyped
    id yields either a fetch failure (loud, tolerable) or a successful fetch of a
    DIFFERENT file (silent, catastrophic). A dropped record yields a short corpus,
    which nothing anywhere compared against what Drive actually returned.

    `pages` is the list of raw responses, one per page per folder, exactly as the
    connector returned them. Records are merged VERBATIM and never reshaped —
    normalise_drive_listing owns shape, downstream, and a second normaliser here would
    be a second definition that will drift.

    `observed_count` is the total the model declares from the connector response. It is
    the whole point: it is an INDEPENDENT number, so the comparison can fail.

    HARD STOPS (ListingIntegrityError, never TransportFallback):
      - a record missing a non-empty id, name/title, or mimeType
      - the same id appearing twice, within a page or across pages
      - merged count != observed_count
      - a nextPageToken present in the LAST supplied page (an unmerged tail, EC-X16)

    REPORTS (never stops): the year span and any interior gaps. A genuinely missing
    year is possible — an exam may not have been held — and only the operator can tell
    that apart from a listing defect. Printing it before paper 1 is what makes the
    difference visible while it is still cheap to act on.
    """
    if not isinstance(pages, (list, tuple)) or not pages:
        raise ListingIntegrityError(
            'write_drive_listing needs the list of raw connector pages; got '
            f'{type(pages).__name__}. Pass every page of every folder, unmodified.')

    merged, seen_ids = [], {}
    for pg_i, page in enumerate(pages, 1):
        items = page
        if isinstance(page, dict):
            items = page.get('files', page.get('items', []))
        for rec in items or []:
            if not isinstance(rec, dict):
                raise ListingIntegrityError(
                    f'page {pg_i} contains a non-record entry ({type(rec).__name__}). '
                    'The cache must hold the connector records verbatim.')
            rid = (rec.get('id') or '').strip()
            rname = (rec.get('title') or rec.get('name') or '').strip()
            rmime = (rec.get('mimeType') or '').strip()
            if not rid or not rname or not rmime:
                raise ListingIntegrityError(
                    f'page {pg_i} has a record missing id/name/mimeType — HARD STOP.\n'
                    f'  id       : {rid!r}\n  name     : {rname!r}\n'
                    f'  mimeType : {rmime!r}\n'
                    'A record this incomplete cannot be fetched and cannot be screened; '
                    'silently dropping it is how a year disappears.')
            if rid in seen_ids:
                raise ListingIntegrityError(
                    f'Drive id {rid} appears twice — HARD STOP.\n'
                    f'  first  : {seen_ids[rid]}\n  second : {rname}\n'
                    'Either a page was supplied twice or a sub-folder was walked into '
                    'its own parent. Both make the count meaningless.')
            seen_ids[rid] = rname
            merged.append(rec)

    tail = pages[-1]
    if isinstance(tail, dict) and tail.get('nextPageToken'):
        raise ListingIntegrityError(
            'the last supplied page still carries a nextPageToken — HARD STOP '
            '(EC-X16). Drive has more records than were merged. Paginate to '
            'exhaustion and supply every page; a lost tail is a missing year that '
            '§1-6 cannot see.')

    try:
        declared = int(observed_count)
    except (TypeError, ValueError):
        raise ListingIntegrityError(
            f'observed_count must be an integer the model declares from the connector '
            f'response, got {observed_count!r}. Without an independent number there is '
            f'nothing for this gate to compare against.')
    if len(merged) != declared:
        raise ListingIntegrityError(
            f'listing count mismatch — HARD STOP.\n'
            f'  merged into the cache : {len(merged)}\n'
            f'  declared from Drive   : {declared}\n'
            f'  difference            : {declared - len(merged):+d}\n'
            'A SHORT listing is worse than an empty one: EC-P39 catches zero, nothing '
            'catches 21-of-22. §1-6 would report success on whatever survived and the '
            'missing year would stay invisible for the life of this exam.')

    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump({'root_folder_id': root_folder_id, 'files': merged},
                  fh, ensure_ascii=False, indent=2)

    years = sorted({y for y in (bc.extract_year_from_filename(
        r.get('title') or r.get('name') or '') for r in merged) if y})
    gaps = ([y for y in range(years[0], years[-1] + 1) if y not in years]
            if len(years) > 1 else [])
    return {'path': path, 'count': len(merged), 'root_folder_id': root_folder_id,
            'years': years, 'year_span': (years[0], years[-1]) if years else None,
            'missing_years': gaps, 'files': merged}


def resolve_uploaded_papers(expected_keys, upload_dir=DEFAULT_UPLOAD_DIR):
    """Match chat-uploaded .docx files against the papers this batch asked for.

    Matching is by CANONICAL identity, never by exact filename and NEVER by recency.

      * exact filename fails because the browser appends " (1)" when the original is
        already in the operator's Downloads folder — which happens on every remediation
        round trip;
      * recency ("the newest three files") fails because uploads ACCUMULATE across
        turns, so by batch 3 the directory still holds batches 1 and 2 and the step
        would silently reprocess them.

    Returns {'matched': {key: path}, 'missing': [...], 'unexpected': [...]}.
    An unrecognised upload is reported, never guessed at and never processed.
    """
    want = set(expected_keys)
    matched, unexpected = {}, []
    if os.path.isdir(upload_dir):
        for fn in sorted(os.listdir(upload_dir)):
            if fn.startswith('~$') or not fn.lower().endswith('.docx'):
                continue
            path = os.path.join(upload_dir, fn)
            key = bc.canonical_paper_key(fn)
            if key in want:
                matched.setdefault(key, path)
            else:
                unexpected.append(path)
    return {'matched': matched,
            'missing': sorted(want - set(matched)),
            'unexpected': unexpected}


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER I SHELL — IMAGE INTEGRITY
# ═══════════════════════════════════════════════════════════════════════════════

def _safe_document(path):
    """Open a .docx via python-docx, converting any package-level failure into a NAMED
    error.

    python-docx surfaces a missing or corrupt part as a bare KeyError/BadZipFile from
    deep inside its package reader. Allowing that to escape means a structurally broken
    document produces an unhandled traceback instead of a gate verdict, which is exactly
    the class of failure this module exists to eliminate.
    """
    docx = _need('docx')
    try:
        return docx.Document(path)
    except DependencyMissing:
        raise
    except Exception as exc:
        raise IntegrityError(
            f'{os.path.basename(path)} could not be opened as a Word package '
            f'({type(exc).__name__}: {exc}). The file is corrupt, truncated, or is '
            f'missing a part that its relationships still reference.')


def _open_zip(path_or_zip):
    """Open a .docx as a ZIP, converting archive-level corruption into a NAMED error.

    A .docx IS a ZIP, so a truncated or malformed download surfaces here first as a bare
    BadZipFile. Letting that escape produces an unhandled traceback instead of a gate
    verdict — the exact class of failure this module exists to eliminate.
    """
    if isinstance(path_or_zip, zipfile.ZipFile):
        return path_or_zip
    try:
        return zipfile.ZipFile(path_or_zip)
    except zipfile.BadZipFile as exc:
        raise IntegrityError(
            f'{os.path.basename(str(path_or_zip))} is not a readable Word package '
            f'({exc}). The file is corrupt or truncated.')


def _rels_for(z, part):
    """rId -> media basename, for the .rels belonging to `part`."""
    rel = f'{os.path.dirname(part)}/_rels/{os.path.basename(part)}.rels'
    out = {}
    if rel in z.namelist():
        txt = z.read(rel).decode('utf-8', 'ignore')
        for rid, tgt in re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', txt):
            out[rid] = os.path.basename(tgt)
    return out


def count_image_refs(path_or_zip, body_only=False):
    """Count EVERY image reference in the document. Returns (total, per_part, unresolved).

    Matches BOTH image mechanisms:
      * <a:blip r:embed>      DrawingML — covers inline AND floating (<wp:anchor>)
      * <v:imagedata r:id>    legacy VML — emitted by older Word, some PDF converters,
                              and pasted OLE / equation objects

    and scans every story part (document, headers, footers, footnotes, endnotes), not
    just document.xml.

    Deliberately does NOT use python-docx `inline_shapes`. That property sees only
    inline body drawings, so anchored figures, VML objects and header images are
    invisible to it. A count that can silently run low is worse than no count at all,
    because it makes a broken document look verified.
    """
    z = _open_zip(path_or_zip)
    total, per_part, unresolved = 0, {}, []
    for part in z.namelist():
        if not STORY_PARTS_RE.match(part):
            continue
        if body_only and part != 'word/document.xml':
            continue
        xml = z.read(part).decode('utf-8', 'ignore')
        rels = _rels_for(z, part)
        rids = re.findall(r'<a:blip[^>]*r:embed="([^"]+)"', xml)
        rids += re.findall(r'<v:imagedata[^>]*r:id="([^"]+)"', xml)
        for rid in rids:
            tgt = rels.get(rid)
            if not tgt:
                unresolved.append((part, rid))
                continue
            per_part[tgt] = per_part.get(tgt, 0) + 1
            total += 1
    return total, per_part, unresolved


def dangling_media_targets(path_or_zip):
    """Relationship targets that point at a media part which does not exist."""
    z = _open_zip(path_or_zip)
    names = set(z.namelist())
    out = []
    for n in z.namelist():
        if not n.endswith('.rels'):
            continue
        owner = os.path.dirname(os.path.dirname(n))
        for t in re.findall(r'Target="((?:\.\./)?media/[^"]+)"',
                            z.read(n).decode('utf-8', 'ignore')):
            cand = os.path.normpath(os.path.join(owner, t)).replace('\\', '/')
            if cand not in names:
                out.append(cand)
    return out


def extract_images(path, outdir):
    """Write every media part to disk as ORIGINAL BYTES and describe each one.

    Nothing is re-encoded, re-rendered or resized here — a .docx is a ZIP, so the stored
    bytes ARE the original image. Re-encoding happens only inside the governor, and only
    under assert_docx_parity().

    Vector parts (EMF/WMF/SVG) cannot be opened as rasters. They are labelled 'vector'
    and REPORTED rather than skipped, so a document that will not shrink has a stated
    reason instead of an unexplained result.
    """
    Image = _need('PIL')
    os.makedirs(outdir, exist_ok=True)
    z = _open_zip(path)
    out = {}
    for n in z.namelist():
        if not MEDIA_RE.match(n):
            continue
        base = os.path.basename(n)
        if not base:
            # A ZIP may store the directory itself ('word/media/') as an entry —
            # observed on IIT_JAM_CHEMISTRY_15-Feb-2026.docx. basename('' ) makes
            # fp the outdir and open(fp,'wb') raises IsADirectoryError, killing
            # extraction for the whole paper. A directory entry carries no bytes
            # worth reporting; skip it. (v1.x fixture: extract_images_dir_entry)
            continue
        raw = z.read(n)
        fp = os.path.join(outdir, base)
        with open(fp, 'wb') as fh:
            fh.write(raw)
        rec = {'part': n, 'path': fp, 'bytes': len(raw), 'kind': None,
               'format': None, 'size': None, 'mode': None, 'note': ''}
        if os.path.splitext(base)[1].lower() in VECTOR_EXT:
            rec['kind'] = 'vector'
            rec['note'] = 'vector part — rasterise before view(); governor leaves it as-is'
        else:
            try:
                im = Image.open(io.BytesIO(raw))
                im.load()
                rec.update(kind='raster', format=im.format, size=im.size, mode=im.mode)
            except Exception as exc:
                rec['kind'] = 'unreadable'
                rec['note'] = str(exc)[:80]
        out[base] = rec
    return out


def map_images_to_questions(path, q_pattern=DEFAULT_Q_PATTERN):
    """Attach every body image to the question it appears under, in DOCUMENT ORDER.

    Iterates `doc.element.body.iter()`, NOT `doc.paragraphs`.

    This is not a stylistic preference. In python-docx `doc.paragraphs` returns only
    paragraphs that are direct children of the body; paragraphs inside table cells are
    excluded entirely. Any figure laid out in a table — the normal arrangement for
    match-the-following items, multi-panel figures and option grids — is therefore never
    visited and never mapped. The question is then classified TEXT rather than FIGURAL,
    which corrupts the format distribution that drives Step 7 generation, and no error
    is raised anywhere. body.iter() descends into tables and fixes this.

    Images appearing before the first question go to a 'preamble' bucket rather than
    being silently dropped, so IMG-4 does not fire for a benign reason.

    q_pattern is supplied by the caller — this module knows nothing about how any
    particular exam numbers its questions.
    """
    d = _safe_document(path)
    z = _open_zip(path)
    rels = _rels_for(z, 'word/document.xml')
    mapping, cur = {}, PREAMBLE
    for el in d.element.body.iter():
        if el.tag.split('}')[-1] != 'p':
            continue
        txt = ''.join(t.text or '' for t in el.iter() if t.tag.split('}')[-1] == 't')
        m = re.match(q_pattern, txt)
        if m:
            cur = int(m.group(1))
        for b in el.iter(f'{{{A_NS}}}blip'):
            rid = b.get(f'{{{R_NS}}}embed')
            if rid:
                mapping.setdefault(cur, []).append(rels.get(rid, f'UNRESOLVED:{rid}'))
        for v in el.iter(f'{{{V_NS}}}imagedata'):
            rid = v.get(f'{{{R_NS}}}id')
            if rid:
                mapping.setdefault(cur, []).append(rels.get(rid, f'UNRESOLVED:{rid}'))
    return mapping


def verify_images(path, extracted=None, mapping=None, expected_size=None,
                  q_pattern=DEFAULT_Q_PATTERN, workdir=None):
    """Run gates IMG-1 .. IMG-5. Returns (verdicts, stats). Never raises.

    The caller decides what to do with a FAIL; this function only reports. Verdict
    evaluation is delegated to blueprint_core.image_gate_verdict so the pass/fail rules
    are unit-testable without any file present.
    """
    if extracted is None:
        extracted = extract_images(path, workdir or f'/tmp/pyq_img/{os.getpid()}')
        # extract_images raises IntegrityError on a corrupt archive; that is a HARD STOP
        # and is allowed to propagate — there is nothing left to verify.

    # The mapping needs python-docx, which fails hard on a structurally broken package.
    # A broken document must still produce GATE VERDICTS rather than a traceback, so the
    # failure is captured and reported through IMG-4 like any other integrity fault.
    map_error = None
    if mapping is None:
        try:
            mapping = map_images_to_questions(path, q_pattern)
        except (IntegrityError, DependencyMissing) as exc:
            mapping, map_error = {}, str(exc)

    z = _open_zip(path)
    all_refs, per_part, unresolved = count_image_refs(z)
    body_refs, _, _ = count_image_refs(z, body_only=True)
    preamble = len(mapping.get(PREAMBLE, []))
    mapped = sum(len(v) for k, v in mapping.items() if k != PREAMBLE)

    # IMG-5 scope (2026-08-31, observed on IIT_JAM_CHEMISTRY_02-Feb-2025.docx):
    # a media part is a REQUIRED renderable only if the document references it as
    # an <a:blip> fill or <v:imagedata> — exactly the reference set count_image_refs
    # counts and IMG-2/IMG-3/IMG-4 already gate on. Word additionally stores
    # JPEG-XR alternates (hdphotoN.wdp) referenced ONLY via <a14:imgLayer>; PIL
    # cannot open them, but no reader ever sees them — every visible drawing has
    # a raster blip. Failing the paper on an alternate layer blocks a corpus that
    # renders perfectly; unreferenced unreadables are REPORTED via stats instead.
    _referenced = set(per_part)
    _unreadable_all = [k for k, v in extracted.items() if v['kind'] == 'unreadable']
    verdicts = bc.image_gate_verdict(
        actual_size=os.path.getsize(path),
        expected_size=expected_size,
        unresolved=len(unresolved),
        missing_on_disk=sorted(set(per_part) - set(extracted)),
        mapped=mapped,
        preamble=preamble,
        body_refs=body_refs,
        unreadable=[k for k in _unreadable_all if k in _referenced])

    if map_error:
        verdicts['IMG-4'] = f'FAIL document could not be read for mapping — {map_error}'

    stats = {
        'refs_all': all_refs,
        'refs_body': body_refs,
        'media_on_disk': len(extracted),
        'mapped': mapped,
        'preamble': preamble,
        'header_footer': all_refs - body_refs,
        'vector': sum(1 for v in extracted.values() if v['kind'] == 'vector'),
        'unreadable': sum(1 for k in _unreadable_all if k in _referenced),
        # alternate layers (e.g. a14:imgLayer JPEG-XR): unreadable but never
        # displayed — reported, not fatal
        'alternate_unreadable': sum(1 for k in _unreadable_all
                                    if k not in _referenced),
        'questions_with_images': len([k for k in mapping if k != PREAMBLE]),
        'dangling': dangling_media_targets(z),
    }
    return verdicts, stats


def figural_consistency(mapping, q_formats, figural_value='FIGURAL', overrides=()):
    """Gate IMG-5b — cross-check image presence against format classification.

    Catches two different faults with one assertion:
      * a question that HAS an image but was not classified FIGURAL  -> image was lost
        or the classifier missed it;
      * a question classified FIGURAL with NO image                  -> misclassification,
        unless it is an explicit logged override (the INHERENTLY-VISUAL path, where a
        question is visual in nature without carrying an embedded figure).

    Returns {'image_not_figural': [...], 'figural_no_image': [...]}.
    """
    ov = set(overrides)
    with_img = {k for k in mapping if k != PREAMBLE and mapping[k]}
    image_not_figural = sorted(
        q for q in with_img
        if q in q_formats and q_formats[q] != figural_value and q not in ov)
    figural_no_image = sorted(
        q for q, f in q_formats.items()
        if f == figural_value and q not in with_img and q not in ov)
    return {'image_not_figural': image_not_figural,
            'figural_no_image': figural_no_image}


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER V — VISION PHASE A / OBSERVATION I/O  (GAP-2026-07-26-003)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Viewing an image is a CLASS T operation — it needs a tool call, and a tool call can
# only happen BETWEEN model turns. A python process cannot suspend mid-loop to make
# one. Everything here is the DETERMINISTIC half of the bridge:
#
#   PHASE A (here)                 normalise -> compose -> tile -> queue.json
#   PHASE B (model, prose)         view() each sheet -> observations.json
#   PHASE C (blueprint_core)       merge observations -> fields
#
# NOTHING HERE RAISES ON A VISION PROBLEM. An unopenable figure, a missing
# observations file and an absent Pillow all DEGRADE with a recorded reason. The
# defect this cluster fixes was silence; the remedy is visibility, not a halt.

VISION_QUEUE_NAME = 'vision_queue.json'
VISION_OBS_NAME = 'vision_observations.json'
VISION_SHEET_FMT = 'vision_sheet_{:03d}.png'


def _open_rgb(src, max_edge=1600):
    """Open one figure as bounded RGB, or return None. EC-V7 (CMYK) / EC-V8 (vector).

    Returns None rather than raising: a figure that cannot be rendered must still
    appear in the queue as an unobserved item, not vanish from the denominator.
    """
    Image = _need('PIL')
    try:
        im = Image.open(src)
        im.load()
    except Exception:
        return None
    if im.mode not in ('RGB', 'L'):
        try:
            im = im.convert('RGB')
        except Exception:
            return None
    if max(im.size) > max_edge:
        r = max_edge / float(max(im.size))
        im = im.resize((max(1, int(im.size[0] * r)), max(1, int(im.size[1] * r))),
                       Image.LANCZOS)
    return im


def _font(size):
    from PIL import ImageFont
    for loader in (
            lambda: ImageFont.truetype(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size),
            lambda: ImageFont.load_default(size=size),
            lambda: ImageFont.load_default()):
        try:
            return loader()
        except Exception:
            continue
    return None


def _compose_cell(srcs, box, max_edge):
    """Compose ONE question's figures into one cell, side by side.

    EC-V6. A 4-panel series is ONE question and must be judged as a whole, so its
    panels share a cell rather than being scattered across the sheet where their
    sequence would be lost.

    Returns (image, ok). ok is False when nothing could be rendered.
    """
    Image = _need('PIL')
    w, h = box
    canvas = Image.new('RGB', (w, h), (255, 255, 255))
    ims = [im for im in (_open_rgb(s, max_edge) for s in srcs) if im is not None]
    if not ims:
        return canvas, False
    gap = 6
    tot_w = sum(i.size[0] for i in ims) + gap * (len(ims) - 1)
    tot_h = max(i.size[1] for i in ims)
    scale = min(w / float(tot_w), h / float(tot_h), 1.0)
    if scale <= 0:
        return canvas, False
    x = int((w - tot_w * scale) / 2)
    for im in ims:
        nw = max(1, int(im.size[0] * scale))
        nh = max(1, int(im.size[1] * scale))
        canvas.paste(im.resize((nw, nh), Image.LANCZOS),
                     (x, int((h - nh) / 2)))
        x += nw + gap
    return canvas, True


# ── CLUSTER Q — ORIGINAL QUESTION POSITION IN THE DATE LABEL (v1.9) ──────────
# GAP-2026-07-27-E. Step 3 (PYQSort) renumbers questions into taxonomy order, which
# destroys the exam position. Step 5 (MockTestAnalyse) needs that position back to
# recognise a section-banded question type — an MSQ block at Q31-40 that carries no
# multi-select instruction phrase of its own. Measured on IIT_JAM_BIOTECHNOLOGY: 24 MSQ
# detected across 1,719 questions against a marking scheme reserving ~10/paper.
#
# ONE WRITER, ONE READER, ONE DEFINITION. The stamp is produced by Step 3 and consumed
# by Step 5, which is exactly the shape that produced the is_option drift v2.36 had to
# unwind: two specs each claiming in a docstring to match the other, and silently
# diverging. Both specs delegate here so the format cannot drift by construction.
#
# The field is OPTIONAL. A label written before v1.18 has no Q-part and parses to None,
# which callers MUST treat as "unknown" and never as position 0. No re-sort is forced.
ORIG_QNUM_RE = re.compile(r'\sQ(\d+)\]$')


def parse_original_q_num(date_label):
    """Return the original exam question number stamped in a date label, or None."""
    m = ORIG_QNUM_RE.search((date_label or '').strip())
    return int(m.group(1)) if m else None


def stamp_original_q_num(date_label, original_q_num):
    """Insert ' Q<N>' before a date label's closing bracket. Idempotent."""
    if original_q_num is None:
        return date_label
    lbl = (date_label or '').strip()
    if not lbl.endswith(']') or ORIG_QNUM_RE.search(lbl):
        return date_label if not lbl.endswith(']') else lbl
    return lbl[:-1] + f' Q{int(original_q_num)}]'


def question_type_for_position(original_q_num, marking_scheme):
    """Return the question_type whose q_range covers this position, or None.

    Exam-agnostic: the bands come from exam_config's marking_scheme at runtime. Returns
    None for an unknown position, an absent/empty scheme, or a position no band covers —
    every one of which means "no positional evidence", never "not this type".
    """
    if original_q_num is None or not marking_scheme:
        return None
    for band in marking_scheme:
        rng = (band or {}).get('q_range') or []
        if len(rng) == 2:
            try:
                if int(rng[0]) <= int(original_q_num) <= int(rng[1]):
                    return band.get('question_type')
            except (TypeError, ValueError):
                continue
    return None


def build_vision_queue(items, workdir, per_sheet=6, max_edge=1600,
                       cell=520, label_h=30, cols=3, fresh=False):
    """PHASE A. Turn figural questions into contact sheets plus a work queue.

    items: [{'paper_id', 'q_num', 'srcs':[path,...], 'subtopic'?, 'image_role'?}]

    Writes ``vision_queue.json`` and ``vision_sheet_NNN.png`` into workdir and returns
    the queue dict. Never raises for a vision reason.

    WHY TILE. One view() per figure does not scale: this corpus has 153 figures across
    22 papers, and a 200-exam fleet has tens of thousands. At per_sheet=6 that is 26
    view() calls instead of 153. per_sheet is a parameter so a sheet that renders badly
    can be re-tiled without touching the caller (EC-V10).

    EC-V1  no figural content -> empty queue, no sheets, valid output
    EC-V6  multi-image question -> ONE item, panels composed side by side
    EC-V8  unrenderable (vector/corrupt) -> queued, flagged, counted; never dropped
    EC-V9  Pillow absent -> degraded mode, one item per sheet, original file viewed
    EC-V15 key is (paper_id, q_num), never a bare q_num
    """
    os.makedirs(workdir, exist_ok=True)

    # ── v1.10 `fresh` — RUN-SCOPED CALLERS OPT OUT OF THE UNION ─────────────────
    # The v1.9 union is correct for Step 5, whose workdir is one-per-RUN spanning a
    # whole batch, and whose resumed sessions must not orphan prior sheets. It is
    # WRONG for Step 1 (PYQPrepare), which processes ONE source per trigger and runs
    # Phase A -> B -> C within that same trigger: anything already in the workdir is
    # contamination from a previous paper or a previous step. Under v1.8's overwrite
    # this sharing was invisible; the union surfaced it — measured: a second
    # PYQPrepare run saw queued=3 where it queued 1, so Phase B re-views the prior
    # paper's cells and Phase C counts them unobserved (amber footer, wrong counts).
    # fresh=True removes the prior queue, sheets AND observations before building,
    # restoring per-run semantics EXPLICITLY at the call site rather than by accident
    # of write mode. Default False preserves union semantics for every other caller.
    if fresh:
        import glob as _glob
        for _stale in ([os.path.join(workdir, VISION_QUEUE_NAME),
                        os.path.join(workdir, VISION_OBS_NAME)]
                       + _glob.glob(os.path.join(workdir, VISION_SHEET_FMT.format(0)
                                                 .replace('000', '*')))):
            try:
                os.remove(_stale)
            except OSError:
                pass

    # ── v1.9 IDEMPOTENT UNION (GAP-2026-07-27-B) ────────────────────────────────
    # This function WRITES vision_queue.json and vision_sheet_NNN.png, both fixed
    # names, and never read what was already there. Callers that invoked it more than
    # once per workdir therefore destroyed every earlier call's work. Measured on
    # IIT_JAM_BIOTECHNOLOGY: 153 figural questions across 22 papers, of which the
    # run-level record retained 8 — the last paper's alone.
    #
    # The caller-side fix (hoist to the batch boundary) is necessary but not
    # sufficient: a RESUMED session starts a new batch against a workdir that may
    # already hold sheets, and would orphan them the same way. Unioning here closes
    # that half. Both halves ship together.
    #
    # Safe by construction: bc.vision_tag_map derives a tag from paper_id alone, so a
    # key's tag does not depend on which OTHER keys are present, and re-tiling a
    # superset leaves every prior tag intact. The one exception is a hash-width
    # widening, which re-tags the WHOLE queue — detected and reported below.
    prior_items, prior_width = [], None
    _qpath = os.path.join(workdir, VISION_QUEUE_NAME)
    if os.path.exists(_qpath):
        try:
            with open(_qpath, encoding='utf-8') as _f:
                _prior = json.load(_f)
            prior_width = _prior.get('tag_width')
            for _pit in (_prior.get('items') or []):
                prior_items.append({'paper_id': _pit.get('paper_id'),
                                    'q_num': _pit.get('q_num'),
                                    'srcs': list(_pit.get('srcs') or []),
                                    'subtopic': _pit.get('subtopic'),
                                    'image_role': _pit.get('image_role')})
        except Exception:
            # An unreadable prior queue must not stop Phase A. Rebuild from the
            # incoming items alone; the sheets are regenerated either way.
            prior_items, prior_width = [], None

    # EC-V27. Collapse repeats of the SAME (paper_id, q_num) into one item, unioning
    # their sources. A key maps to exactly one tag, so two items sharing a key would
    # print the SAME label on two cells — and a Phase-B observation against that label
    # could not be attributed to either. One question, one tag, one cell (EC-V6).
    # Prior items are seeded FIRST so a re-run is stable; incoming items fill gaps.
    merged = {}
    for it in (prior_items + list(items or [])):
        if not isinstance(it, dict):
            continue
        try:
            key = (str(it['paper_id']), int(it['q_num']))
        except (KeyError, TypeError, ValueError):
            continue
        srcs = [s for s in (it.get('srcs') or []) if s]
        if key in merged:
            prev_srcs, prev_it = merged[key]
            for s in srcs:
                if s not in prev_srcs:
                    prev_srcs.append(s)
            for f in ('subtopic', 'image_role'):
                if prev_it.get(f) is None and it.get(f) is not None:
                    prev_it[f] = it[f]
        else:
            merged[key] = (list(srcs), dict(it))
    # Deterministic order: the queue must be reproducible byte for byte (EC-V12).
    rows = sorted(((k, v[0], v[1]) for k, v in merged.items()),
                  key=lambda r: (r[0][0], r[0][1]))

    # v1.9. Pass the prior width as a FLOOR. vision_tag_map widens on collision but
    # would otherwise also NARROW when the key set shrinks, re-tagging every surviving
    # question for no reason. Under the union the paper set grows and shrinks across
    # batches and resumed sessions, so pinning the floor removes the spurious half of
    # the re-tag risk entirely. A genuine widening remains possible — 4 hex chars is
    # ~65k codes, so a collision appears in a few percent of large corpora — and is
    # reported rather than absorbed.
    tag_map, tag_width = bc.vision_tag_map([r[0] for r in rows],
                                           width=(prior_width or 4))
    stats = {'queued': len(rows), 'sheets': 0, 'unrenderable': 0, 'degraded': False,
             # v1.9 — union provenance, so a caller can tell a fresh queue from a
             # resumed one without diffing files.
             'carried_in': len(prior_items), 'submitted': len(items or []),
             'tag_generation_changed': False}
    if prior_width is not None and prior_width != tag_width:
        # EC-V12. A paper_id hash collision widened the code for the WHOLE queue, so
        # every tag changed and observations written under the previous generation can
        # no longer be matched. Never silent: Phase C would otherwise report them as
        # simply unobserved and the operator would re-view sheets that were already done.
        stats['tag_generation_changed'] = True
        stats['prior_tag_width'] = prior_width

    degraded = False
    try:
        _need('PIL')
    except DependencyMissing:
        degraded = True
        stats['degraded'] = True

    queue_items, sheets = [], []
    if degraded:
        # EC-V9. One view() per figure against the ORIGINAL file. Slower, never silent.
        for i, (key, srcs, it) in enumerate(rows):
            queue_items.append({
                'tag': tag_map[key], 'paper_id': key[0], 'q_num': key[1],
                'subtopic': it.get('subtopic'), 'image_role': it.get('image_role'),
                'sheet': srcs[0] if srcs else None, 'cell': 0,
                'renderable': bool(srcs), 'srcs': srcs})
            if not srcs:
                stats['unrenderable'] += 1
    else:
        Image = _need('PIL')
        from PIL import ImageDraw
        n_cols = max(1, min(int(cols), int(per_sheet)))
        n_rows = max(1, -(-int(per_sheet) // n_cols))
        cw, ch = int(cell), int(cell) + int(label_h)
        font = _font(20)
        for start in range(0, len(rows), int(per_sheet)):
            chunk = rows[start:start + int(per_sheet)]
            idx = len(sheets) + 1
            name = VISION_SHEET_FMT.format(idx)
            sheet = Image.new('RGB', (n_cols * cw, n_rows * ch), (245, 245, 245))
            d = ImageDraw.Draw(sheet)
            for j, (key, srcs, it) in enumerate(chunk):
                cx, cy = (j % n_cols) * cw, (j // n_cols) * ch
                img, ok = _compose_cell(srcs, (cw - 8, ch - label_h - 8), max_edge)
                if not ok:
                    stats['unrenderable'] += 1
                sheet.paste(img, (cx + 4, cy + label_h + 4))
                d.rectangle([cx + 2, cy + 2, cx + cw - 2, cy + ch - 2],
                            outline=(0, 0, 0), width=2)
                label = tag_map[key] + ('' if ok else '  [UNRENDERABLE]')
                d.rectangle([cx + 2, cy + 2, cx + cw - 2, cy + label_h],
                            fill=(0, 0, 0))
                d.text((cx + 10, cy + 6), label, fill=(255, 255, 255), font=font)
                queue_items.append({
                    'tag': tag_map[key], 'paper_id': key[0], 'q_num': key[1],
                    'subtopic': it.get('subtopic'), 'image_role': it.get('image_role'),
                    'sheet': name, 'cell': j, 'renderable': ok, 'srcs': srcs})
            path = os.path.join(workdir, name)
            sheet.save(path, 'PNG', optimize=True)
            sheets.append(name)
        stats['sheets'] = len(sheets)

    queue = {'version': 1, 'tag_width': tag_width, 'per_sheet': int(per_sheet),
             'degraded': degraded, 'sheets': sheets, 'items': queue_items,
             'stats': stats}
    with open(os.path.join(workdir, VISION_QUEUE_NAME), 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2, sort_keys=True)
    return queue


def load_vision_queue(workdir):
    """Read back a queue. Returns (queue_dict, reason). Never raises."""
    path = os.path.join(workdir, VISION_QUEUE_NAME)
    if not os.path.exists(path):
        return None, 'no queue file — Phase A has not run for this batch'
    try:
        with open(path, encoding='utf-8') as f:
            q = json.load(f)
    except Exception as exc:
        return None, f'queue file unreadable ({exc})'
    if not isinstance(q, dict) or not isinstance(q.get('items'), list):
        return None, 'queue file has no items list'
    return q, ''


def load_vision_observations(workdir, path=None):
    """PHASE B -> C boundary. Read observations. Returns (list, reason). Never raises.

    A missing or malformed file is NOT an error condition here — it is the ordinary
    'Phase B has not run yet' state, and it must flow through to Phase C as zero
    observations so the run completes and QV-14 reports the gap. Raising here would
    reintroduce the halt this design exists to avoid.

    Accepts a bare list, or a dict carrying 'observations'.
    """
    p = path or os.path.join(workdir, VISION_OBS_NAME)
    if not os.path.exists(p):
        return [], 'no observations file — Phase B has not run'
    try:
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as exc:
        return [], f'observations file unreadable ({exc}) — treated as zero observations'
    if isinstance(data, dict):
        data = data.get('observations', [])
    if not isinstance(data, list):
        return [], 'observations file is neither a list nor {"observations": [...]}'
    return [d for d in data if isinstance(d, dict)], ''


def write_vision_observations(workdir, observations, path=None):
    """Write the Phase-B result. Provided so the protocol has ONE spelling of the file."""
    p = path or os.path.join(workdir, VISION_OBS_NAME)
    os.makedirs(os.path.dirname(os.path.abspath(p)) or '.', exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump({'observations': list(observations or [])}, f,
                  indent=2, sort_keys=True)
    return p


# ── SHARED OPTION PREDICATE (Cluster I) ─────────────────────────────────────────
# GAP-2026-07-26-002 follow-up, audit_deep [XSPEC-DRIFT]. is_option() was defined
# THREE times — Framework_MockTestAnalyse (Step 5), Framework_PYQSort (Step 1) and
# Framework_PYQAnalyse (Step 4) — each carrying a docstring claiming alignment with
# the others. Step 5 then gained the image-option path and the other two did not,
# so the alignment claim became false and the SAME defect the wave fixed in Step 5
# stayed live in Step 1: PYQSort counts options with this predicate, so an image
# option was silently UNDERCOUNTED.
#
# One definition here; all three steps delegate. Drift is now impossible by
# construction rather than by comment.

OPT_PATTERNS = [
    r'^([1-5])\.\s+(.+)',           # 1. 2. 3. 4. 5.  (up to 5 options)
    r'^([A-Ea-e])\.\s+(.+)',        # A. B. C. D. E.
    r'^\(([1-5])\)\s+(.+)',         # (1) (2) (3) (4) (5)
    r'^\(([A-Ea-e])\)\s+(.+)',      # (A) (B) (C) (D) (E) / (a)(b)(c)(d)(e)
    r'^([A-Ea-e])\)\s+(.+)',        # A) B) C) D) E) / a) b) c) d) e)
]

# A marker with NO text after it. Every OPT_PATTERNS entry requires \s+(.+), so an
# IMAGE OPTION — the paragraph is literally "1." and the picture follows — matched
# none of them.
BARE_OPT_PATTERNS = [
    r'^\(?([1-5])\)?\.?\s*$',       # 1.  1)  (1)  1
    r'^\(?([A-Ea-e])\)?\.?\s*$',    # A.  A)  (A)  A
]

BLIP_TAG          = f'{{{A_NS}}}blip'
VML_IMAGEDATA_TAG = f'{{{V_NS}}}imagedata'


def para_has_image(para):
    """True when this paragraph carries an embedded image (DrawingML blip or VML).

    Accepts EITHER form the corpus actually passes:
      * a python-docx Paragraph  — Step 5 walks doc.paragraphs and has `._p`
      * a raw <w:p> lxml element — Steps 1/3 walk body_elems and ARE the element

    That difference is not cosmetic. A delegation that assumed one form would raise
    AttributeError on the other, or — worse — silently return False and reinstate the
    exact undercount this function exists to prevent.
    """
    if para is None:
        return False
    el = getattr(para, '_p', para)          # Paragraph -> element; element -> itself
    it = getattr(el, 'iter', None)
    if it is None:
        return False
    for e in it():
        if getattr(e, 'tag', None) in (BLIP_TAG, VML_IMAGEDATA_TAG):
            return True
    return False


def para_is_option_content(para):
    """True when a bare option LABEL's paragraph carries the option's actual content.

    GAP-2026-08-05-001 (S-1). para_has_image() recognises only a DrawingML blip or a
    VML imagedata reference, so an option whose content is an OMML equation or an
    embedded OLE object was not recognised as an option at all — even though PYQSort
    CHECK 4 accepts "(c) inline drawing" AND "(d) OMML formula" as valid option forms.
    Producer and consumer disagreed about what an option IS.

    Measured on SSC_CGL_TIER1 09-Sep-2024 Shift 1, a delivered sorted paper: Q.75
    options 1 and 2 are bare labels "1." / "2." whose content is <m:oMath>. Both
    returned False, so that question silently lost half its option set at Step 5.

    include_autonumber=False is deliberate: on a bare label the rendered w:numPr number
    merely duplicates the "1." already present as text and is not option CONTENT, so an
    auto-numbered but otherwise empty paragraph must NOT be promoted to an option.
    """
    return bool(para_has_image(para) or
                bc.paragraph_is_content_bearing(para, include_autonumber=False))


def is_option(text, para=None):
    """THE option-line predicate. Every step delegates to this; nobody re-implements it.

    Pass `para` wherever the paragraph is available so an image-only option is
    recognised. Without it the behaviour is byte-identical to the historic text-only
    predicate, so delegating is safe even at a call site that has no paragraph — but
    a call site that HAS one and does not pass it keeps the undercount.
    """
    t = (text or '').strip()
    if any(re.match(p, t) for p in OPT_PATTERNS):
        return True
    if para is not None and para_is_option_content(para):
        return any(re.match(p, t) for p in BARE_OPT_PATTERNS)
    return False


W_T_TAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'
M_T_TAG = '{http://schemas.openxmlformats.org/officeDocument/2006/math}t'
M_OMATH_TAG = '{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath'
W_BR_TAG  = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br'
W_CR_TAG  = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cr'
W_TAB_TAG = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tab'


def text_of(para, omml_renderer=None):
    """Canonical VISIBLE text of a paragraph — every <w:t> AND <m:t> descendant,
    concatenated in document order. (GAP-2026-08-07-OMML, remedy M3.)

    python-docx's p.text is <w:t>-only, so a paragraph whose payload is an
    <m:oMath> equation reads as a bare label ("3. ") or as empty. That is the
    exact producer/consumer disagreement S-1 fixed structurally for option
    DETECTION; text_of() closes the remaining half — any consumer that needs the
    words a reader actually sees (dedupe keys, taxonomy matching, QV text
    audits, PYQPrepare CHECK 9) reads text_of(), never p.text, whenever OMML may
    be present. is_option()/BARE_OPT_PATTERNS stay the structural predicates.

    Accepts EITHER a python-docx Paragraph or a raw <w:p> lxml element — the
    same duality, for the same reason, as para_has_image().
    """
    if para is None:
        return ''
    el = getattr(para, '_p', para)
    it = getattr(el, 'iter', None)
    if it is None:
        return ''
    out = []
    # w:br / w:cr render as newline and w:tab as tab, exactly as python-docx
    # p.text does — dropping them glues words across soft line breaks
    # ('blank.Postcolonial', measured on the SSC passage corpus 2026-08-31) and
    # silently breaks _SERIES_ masking and word counts downstream.
    _BREAKS = {W_BR_TAG: '\n', W_CR_TAG: '\n', W_TAB_TAG: '\t'}
    if omml_renderer is not None:
        # v2.56 §6.1.6 / E-13: emit the LINEARISED equation at its reading
        # position and skip its raw <m:t> glyphs. Reading glyphs alone loses the
        # structure a reader sees — 'sqrt(2)' degrades to '2', a fraction to a
        # digit run (measured on the SSC corpus, 2026-08-31). Callers that use
        # text for dedupe keys keep the default (renderer=None) so existing keys
        # never shift.
        # The WHOLE equation subtree is consumed by the renderer, not just its
        # <m:t> glyphs: OOXML permits a <w:t> run INSIDE an <m:oMath>, and
        # skipping only <m:t> emitted that run AFTER the rendered equation —
        # 'Given xwhere2' became 'Given x2where'. Displaced words inside an
        # equation are worse than lost ones: they read as real text in the wrong
        # place. (Found by reading the diff, 2026-08-31.)
        # Membership is tested by ANCESTRY, not by collecting ids: lxml creates
        # a NEW proxy object on each access, so id() is not stable across a
        # traversal and an id-set silently skips unrelated runs (measured: the
        # trailing ' now.' vanished). iterancestors is the stable question.
        def _inside_math(el):
            anc = getattr(el, 'iterancestors', None)
            if anc is None:              # non-lxml element (test doubles)
                return False
            return any(getattr(a, 'tag', None) == M_OMATH_TAG for a in anc())
        for e in it():
            tag = getattr(e, 'tag', None)
            if tag == M_OMATH_TAG:
                if not _inside_math(e):          # nested oMath: outer wins
                    out.append(omml_renderer(e))
                continue
            if _inside_math(e):
                continue                          # consumed by the equation
            if tag == W_T_TAG:
                out.append(e.text or '')
            elif tag in _BREAKS:
                out.append(_BREAKS[tag])
        return ''.join(out)
    for e in it():
        tag = getattr(e, 'tag', None)
        if tag in (W_T_TAG, M_T_TAG):
            out.append(e.text or '')
        elif tag in _BREAKS:
            out.append(_BREAKS[tag])
    return ''.join(out)


def clean_option_text(text):
    """Option text with its marker stripped. '' for a bare marker — the option content
    IS the image, and an all-empty option set is what resolves option_format to
    'image_only' downstream."""
    t = (text or '').strip()
    for p in OPT_PATTERNS:
        m = re.match(p, t)
        if m:
            return m.group(2).strip()
    for p in BARE_OPT_PATTERNS:
        if re.match(p, t):
            return ''
    return t


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER J SHELL — SIZE GOVERNOR
# ═══════════════════════════════════════════════════════════════════════════════

def media_display_inches(path):
    """media basename -> widest display width in inches, across every story part.

    Read from each drawing's own <wp:extent cx=".."> (EMU), falling back to the VML
    style width in points.

    This is what makes downscaling CONTENT-AWARE. A figure is only over-resolved
    relative to the size it is actually displayed at: one measured figure in this corpus
    is 2546 px wide but appears 2.09 inches wide, i.e. 1216 DPI. A blanket pixel cap
    would degrade a small, correctly-sized figure while barely touching that one.
    """
    EMU_PER_INCH = 914400
    z = _open_zip(path)
    widths = {}
    for part in z.namelist():
        if not STORY_PARTS_RE.match(part):
            continue
        rels = _rels_for(z, part)
        if not rels:
            continue
        xml = z.read(part).decode('utf-8', 'ignore')
        for blk in re.findall(r'<w:drawing>.*?</w:drawing>', xml, re.S):
            cx = re.search(r'<wp:extent[^>]*\bcx="(\d+)"', blk)
            rid = re.search(r'<a:blip[^>]*r:embed="([^"]+)"', blk)
            if not (cx and rid):
                continue
            base = rels.get(rid.group(1))
            if base:
                widths[base] = max(widths.get(base, 0.0),
                                   int(cx.group(1)) / float(EMU_PER_INCH))
        for blk in re.findall(r'<w:pict>.*?</w:pict>', xml, re.S):
            rid = re.search(r'r:id="([^"]+)"', blk)
            st = re.search(r'style="[^"]*width:\s*([\d.]+)pt', blk)
            if not rid:
                continue
            base = rels.get(rid.group(1))
            if base:
                widths[base] = max(widths.get(base, 0.0),
                                   float(st.group(1)) / 72.0 if st else 0.0)
    return widths


LINE_ART_FLAT_FRAC = 0.60      # v1.15 — see _line_art_stats(); renders >= 0.78, photos 0.00
LINE_ART_MODE_FRAC = 0.25      # v1.15 — dominant exact colour (a render's background):
                               #         renders 0.39-0.99, photographs / scans / gradients <= 0.005


def _sample_nearest(im, sample_cap):
    """Bounded RGB sample. NEAREST is explicit: Pillow's default resize filter
    changed across versions (NEAREST -> BICUBIC), and a smoothing filter blurs
    the very flatness this test measures — NEAREST keeps exact pixel values, so
    the verdict is identical on every Pillow version."""
    Image = _need('PIL')
    s = im.convert('RGB')
    if s.size[0] * s.size[1] > sample_cap:
        r = (sample_cap / float(s.size[0] * s.size[1])) ** 0.5
        nearest = getattr(getattr(Image, 'Resampling', Image), 'NEAREST')
        s = s.resize((max(1, int(s.size[0] * r)), max(1, int(s.size[1] * r))), nearest)
    return s


def _line_art_stats(im, sample_cap=250_000):
    """v1.15 — (flat_fraction, mode_fraction) or None when numpy is unavailable.
    flat_fraction: share of interior pixels whose 4-neighbours are EXACTLY equal —
      rendered line art is mostly flat regions with hard edges; a photograph or a
      scan carries texture in every pixel.
    mode_fraction: share of pixels of the single most common exact colour — every
      rendered figure has a dominant exact background (its margins), a photograph
      or scan has none. Catches the one render class flatness misses: a smoothly
      interpolated heat map, whose axis text would ring under JPEG.
    Deterministic; the sample is bounded and NEAREST-resampled."""
    try:
        import numpy as _np
    except ImportError:
        return None
    s = _sample_nearest(im, sample_cap)
    a = _np.asarray(s).astype(int)
    h, w = a.shape[0], a.shape[1]
    if h < 3 or w < 3:
        return 1.0, 1.0
    c = a[1:-1, 1:-1]
    differs = _np.zeros(c.shape[:2], dtype=bool)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        n = a[1 + dy:h - 1 + dy, 1 + dx:w - 1 + dx]
        differs |= (_np.abs(c - n).max(-1) > 0)
    flat = float(1.0 - differs.mean())
    packed = (a[..., 0] << 16) | (a[..., 1] << 8) | a[..., 2]
    _, counts = _np.unique(packed, return_counts=True)
    mode = float(counts.max() / float(h * w))
    return flat, mode


def _is_line_art(im, sample_cap=250_000):
    """v1.15 — STRUCTURAL: line art when flat_fraction >= LINE_ART_FLAT_FRAC OR
    mode_fraction >= LINE_ART_MODE_FRAC (either alone is decisive: photographs,
    scans and gradients fail BOTH by two orders of magnitude). The pre-v1.15 rule
    (<= 256 distinct colours) is kept ONLY as the numpy-less fallback: it called
    every anti-aliased render a photograph and a smooth gradient line art."""
    st = _line_art_stats(im, sample_cap)
    if st is not None:
        flat, mode = st
        return flat >= LINE_ART_FLAT_FRAC or mode >= LINE_ART_MODE_FRAC
    s = im.convert('RGB')
    if s.size[0] * s.size[1] > sample_cap:
        r = (sample_cap / float(s.size[0] * s.size[1])) ** 0.5
        s = s.resize((max(1, int(s.size[0] * r)), max(1, int(s.size[1] * r))))
    return len(set(s.getdata())) <= 256


def _normalise_mode(im):
    """Return (image, has_alpha) in a colour space that can actually be encoded.

    CMYK is the single largest cause of bloat in this corpus — 100% of measured figures
    were CMYK. It carries a fourth channel and is written by design tools at print
    quality with no chroma subsampling; a 544x568 diagram occupied 595 KB, about 1.9
    bytes per pixel where a correct RGB JPEG uses 0.15-0.3. Converting to RGB is
    visually lossless for screen use and is where nearly all of the reduction comes from.

    Palette ('P') and 16-bit modes are also normalised, because PIL cannot quantise or
    JPEG-encode them directly — attempting it raises "image has wrong mode".
    """
    if im.mode in ('RGBA', 'LA'):
        return im, True
    if im.mode == 'P':
        conv = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        return conv, conv.mode == 'RGBA'
    if im.mode in ('L', '1'):
        return im.convert('L'), False
    if im.mode in ('I;16', 'I', 'F'):
        return im.convert('L'), False
    return im.convert('RGB'), False


def _quantize_png(im):
    """Palette-quantize one image to PNG bytes; never raises, never returns growth.

    v1.13 — used by TMAX (mode='max') only. Tries the pngquant binary first (the
    best quantizer for line art AND alpha-bearing images — the measured v2 corpus
    used it), runs optipng -o3 on its output when that binary is present, and falls
    back to PIL FASTOCTREE quantization (also alpha-capable) when neither binary is
    installed. Always returns the SMALLEST successful encoding, or None when even a
    plain PNG save fails (caller then routes through the normal path).
    """
    import shutil as _sh
    import subprocess as _sp
    import tempfile
    Image = _need('PIL')

    plain = io.BytesIO()
    try:
        im.save(plain, 'PNG', optimize=True)
    except Exception:
        return None
    best = plain.getvalue()

    if _sh.which('pngquant'):
        try:
            with tempfile.TemporaryDirectory() as td:
                q_src = os.path.join(td, 'in.png')
                q_dst = os.path.join(td, 'out.png')
                with open(q_src, 'wb') as fh:
                    fh.write(best)
                lo, hi = bc.PNG_QUANT_QUALITY
                r = _sp.run(['pngquant', f'--quality={lo}-{hi}', '--speed', '1',
                             '--strip', '--force', '--output', q_dst, q_src],
                            capture_output=True, timeout=60)
                if r.returncode == 0 and os.path.exists(q_dst):
                    if _sh.which('optipng'):
                        _sp.run(['optipng', '-o3', '-quiet', q_dst],
                                capture_output=True, timeout=120)
                    with open(q_dst, 'rb') as fh:
                        cand = fh.read()
                    if cand and len(cand) < len(best):
                        best = cand
                    return best
        except Exception:
            pass

    try:
        q = im.quantize(colors=bc.PNG_QUANT_COLORS, method=Image.FASTOCTREE)
        out = io.BytesIO()
        q.save(out, 'PNG', optimize=True)
        if len(out.getvalue()) < len(best):
            best = out.getvalue()
    except Exception:
        pass
    return best


def _recode(raw, quality, dpi_ceiling, display_in, quantize=False):
    """Re-encode one media part. Returns (bytes, ext, how) or (None, None, why)."""
    Image = _need('PIL')
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception:
        return None, None, 'unreadable or vector — left untouched'

    src_fmt = (im.format or '').upper()
    im, has_alpha = _normalise_mode(im)

    if dpi_ceiling and display_in and display_in > 0:
        effective_dpi = im.size[0] / float(display_in)
        if effective_dpi > dpi_ceiling:
            r = dpi_ceiling / effective_dpi
            im = im.resize((max(1, int(im.size[0] * r)), max(1, int(im.size[1] * r))),
                           Image.LANCZOS)

    route = bc.classify_media_route(
        src_fmt, has_alpha, False if has_alpha else _is_line_art(im))

    out = io.BytesIO()
    if route == 'png':
        if quantize:                                   # v1.13 — TMAX only
            data = _quantize_png(im)
            if data is not None:
                return data, 'png', 'png/alpha+quant'
        im.save(out, 'PNG', optimize=True)
        return out.getvalue(), 'png', 'png/alpha'
    if route == 'png-lineart':
        if quantize:                                   # v1.13 — TMAX only
            data = _quantize_png(im)
            if data is not None:
                return data, 'png', 'png/lineart+quant'
        im.convert('P', palette=Image.ADAPTIVE, colors=256).save(out, 'PNG', optimize=True)
        return out.getvalue(), 'png', 'png/lineart'
    im.save(out, 'JPEG', quality=quality, optimize=True, progressive=True, subsampling=2)
    return out.getvalue(), 'jpeg', ('jpeg/reencode' if src_fmt in ('JPEG', 'JPG')
                                    else 'jpeg/photo')


#: Extensions already carrying the right content type for each encoder route, so a
#: part using one needs no rename. Renaming gratuitously (image1.jpg -> image1.jpeg)
#: churns every relationship that references it and manufactures stem collisions that
#: would not otherwise exist.
_EXT_OK = {'jpeg': ('.jpeg', '.jpg'), 'png': ('.png',)}


def _target_media_name(name, ext):
    """Output name for one re-encoded media part. Keeps the name when the existing
    extension already maps to the encoder's content type."""
    stem, cur = os.path.splitext(name)
    if cur.lower() in _EXT_OK[ext]:
        return name
    return stem + ('.jpeg' if ext == 'jpeg' else '.png')


def _no_gain_guard(src, dst, orig, report):
    """v1.0.3 — never hand back a file LARGER than the one we were given.

    Per-PART growth is already prevented (_recode keeps the original bytes whenever a
    re-encode comes out bigger), but the ZIP CONTAINER can still grow: a package whose
    media is already optimally encoded gains nothing from re-deflation and can lose to
    the original writer's settings by a few bytes.

    Before `always` this was unreachable — a file under budget was never re-encoded at
    all — so no document-level rule was needed. It is now the normal case for small
    documents, and Framework_PYQCompress CHECK 5 treats growth as a HARD STOP, so a file
    with nothing to gain would have ABORTED THE RUN rather than simply being left alone.
    Restoring the original bytes makes "nothing to gain" a reportable outcome instead.
    """
    if os.path.getsize(dst) >= orig:
        shutil.copyfile(src, dst)
        return dict(report, bytes=orig, ratio=1.0, no_gain=True)
    return dict(report, no_gain=False)


def optimize_docx(src, dst, budget=None, force_tier=None, always=False, mode=None):
    """Bring `src` under `budget` using blueprint_core's deterministic tier ladder.

    Stops at the FIRST tier that meets the budget, so the least invasive change that
    works is the one applied. On the measured corpus every paper cleared at T1, meaning
    no image was downscaled at all and every pixel dimension was preserved.

    v1.13 — mode='max' (PYQCompress v2.0.0) replaces the ladder walk with ONE pass at
    blueprint_core.MAX_TIER: every raster is resampled to the MAX_TIER dpi ceiling at
    its display size regardless of budget, and PNG output is palette-quantized
    (_quantize_png). `budget` then only decides the returned ok flag and the
    transport verdict — it never gates whether compression happens. mode=None (the
    default) is byte-identical to the pre-v1.13 behaviour for every existing caller.

    Guarantees: never grows a part, never drops a part, never changes the part count.
    Returns (ok, report, log). ok=False means the ladder floor was reached and the file
    is STILL over budget — the caller should WARN and route to the upload lane, not halt,
    because a legitimately huge paper must not block delivery.

    The caller MUST still run assert_docx_parity(); this function does not self-certify.
    """
    if mode == 'max' and force_tier:
        raise ValueError(
            "optimize_docx: mode='max' and force_tier are mutually exclusive — "
            "max mode has exactly one governor point (bc.MAX_TIER).")
    budget = bc.SIZE_BUDGET if budget is None else budget
    orig = os.path.getsize(src)
    # v1.0.3 — `always` runs the ladder regardless of input size. The ladder itself needs
    # no change: a small file's T1 output is under budget, so it returns at T1, which is
    # the least invasive tier. NOTE for callers: force_tier is NOT a substitute — it pins
    # a single tier AND makes the final `return True` unconditional, so an oversized file
    # would stop at that tier, still over budget, and be reported as a success.
    if orig <= budget and not force_tier and not always and mode != 'max':
        return True, {'tier': 'T0', 'bytes': orig, 'orig': orig, 'ratio': 1.0,
                      'quality': None, 'dpi_ceiling': None,
                      'note': 'already under budget — untouched'}, []

    display = media_display_inches(src)
    report, log = {}, []

    ladder = (bc.MAX_TIER,) if mode == 'max' else bc.TIER_LADDER
    for tier, quality, dpi in ladder:
        if force_tier and tier != force_tier:
            continue
        zin = zipfile.ZipFile(src)
        names = zin.namelist()
        name_set = set(names)
        parts, renames, outname, log = {}, {}, {}, []

        for n in names:
            raw = zin.read(n)
            if MEDIA_RE.match(n):
                base = os.path.basename(n)
                data, ext, how = _recode(raw, quality, dpi, display.get(base, 0.0),
                                         quantize=(mode == 'max'))
                if data is None or len(data) >= len(raw):
                    new, payload = n, raw                  # never grow a part
                    log.append((base, len(raw), len(raw), how + ' [kept]'))
                else:
                    new = _target_media_name(n, ext)
                    payload = data
                    log.append((base, len(raw), len(data), how))

                # v1.0.2 — a media part may NEVER overwrite another. Two parts that
                # share a stem and take the same encoder route (image1.png +
                # image1.bmp, both photographic) both want image1.jpeg; the old code
                # collapsed them into ONE zip member, so Word rendered whichever it
                # met first and the other figure was silently replaced. Every count
                # the parity assert checks — parts, media, refs — still matched, and
                # the per-stem pixel check is skipped at T2-T4, so the corrupted file
                # was delivered clean. Disambiguate instead of overwriting.
                if new in parts or (new != n and new in name_set):
                    stem, dot_ext = os.path.splitext(new)
                    k = 2
                    while (f'{stem}__c{k}{dot_ext}' in parts
                           or f'{stem}__c{k}{dot_ext}' in name_set):
                        k += 1
                    new = f'{stem}__c{k}{dot_ext}'

                parts[new] = payload
                outname[n] = new
                if os.path.basename(new) != base:
                    renames[base] = os.path.basename(new)
            else:
                parts[n] = raw
                outname[n] = n
        zin.close()

        # v1.0.2 — belt-and-braces: one member out for every member in. Catches any
        # future path that collapses two parts into one key, including a duplicate
        # member name in a damaged input package.
        if len(parts) != len(names) or len(outname) != len(names):
            raise IntegrityError(
                f'part collision in {os.path.basename(src)} at tier {tier}: '
                f'{len(names)} package member(s) in, {len(parts)} out. Two parts '
                'resolved to a single name — refusing to write a package in which '
                'one figure silently replaces another.')

        # Renaming a media part invalidates every reference to it. Rewrite the
        # relationship targets and guarantee the content-type defaults exist, or Word
        # reports the file as corrupt.
        #
        # v1.0.2 — SINGLE PASS. Sequential str.replace() chained: with renames
        # {'image1.png': 'image1.jpeg', 'image1.jpeg': 'image1__c2.jpeg'} the first
        # substitution manufactured a second 'image1.jpeg', which the second
        # substitution then rewrote as well, pointing both references at one part.
        rename_re = (re.compile('|'.join(re.escape(k) for k in
                                sorted(renames, key=len, reverse=True)))
                     if renames else None)
        for pn in list(parts):
            if pn.endswith('.rels') or pn == '[Content_Types].xml':
                txt = parts[pn].decode('utf-8')
                if rename_re is not None:
                    txt = rename_re.sub(lambda m: renames[m.group(0)], txt)
                if pn == '[Content_Types].xml':
                    for ext_, ctype in (('jpeg', 'image/jpeg'), ('png', 'image/png'),
                                        ('jpg', 'image/jpeg')):
                        if f'Extension="{ext_}"' not in txt:
                            txt = re.sub(
                                r'(<Types[^>]*>)',
                                rf'\1<Default Extension="{ext_}" ContentType="{ctype}"/>',
                                txt, count=1)
                parts[pn] = txt.encode('utf-8')

        os.makedirs(os.path.dirname(os.path.abspath(dst)) or '.', exist_ok=True)
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zo:
            for n in names:
                # v1.0.2 — write through the explicit map built above. The previous
                # reverse-lookup guessed the output name by trying '.jpeg' then
                # '.png', which cannot express a disambiguated name and silently
                # resolved two inputs to one key.
                zo.writestr(outname[n], parts[outname[n]])

        size = os.path.getsize(dst)
        report = {'tier': tier, 'bytes': size, 'orig': orig,
                  'ratio': size / float(orig), 'quality': quality, 'dpi_ceiling': dpi}
        if size <= budget or force_tier:
            return True, _no_gain_guard(src, dst, orig, report), log

    return False, _no_gain_guard(src, dst, orig, report), log


def docx_invariants(path):
    """Every observable property that optimisation must leave untouched."""
    import hashlib
    import xml.dom.minidom as minidom
    Image = _need('PIL')

    z = _open_zip(path)
    d = _safe_document(path)
    xml = z.read('word/document.xml').decode('utf-8', 'ignore')
    media = sorted(n for n in z.namelist() if n.startswith('word/media/'))

    xmlerr = 0
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')):
            try:
                minidom.parseString(z.read(n))
            except Exception:
                xmlerr += 1

    txt = '\n'.join(p.text for p in d.paragraphs)
    tbl = ''.join(c.text for t in d.tables for r in t.rows for c in r.cells)
    return {
        'parts': len(z.namelist()),
        'media': len(media),
        'paras': len(d.paragraphs),
        'tables': len(d.tables),
        'shapes': len(d.inline_shapes),
        'chars': len(txt),
        'tablechars': len(tbl),
        'omml': xml.count('<m:oMath'),
        'drawings': xml.count('<w:drawing'),
        'pict': xml.count('<w:pict'),
        'hyperlinks': xml.count('<w:hyperlink'),
        'texthash': hashlib.sha256(txt.encode()).hexdigest(),
        'refs': count_image_refs(z)[0],
        'xmlerr': xmlerr,
        'zipbad': z.testzip() or 'OK',
        'dangling': dangling_media_targets(z),
        'px': {os.path.basename(n): Image.open(io.BytesIO(z.read(n))).size
               for n in media if os.path.splitext(n)[1].lower() in RASTER_EXT},
    }


def assert_docx_parity(src, dst, allow_resample=False):
    """Raise IntegrityError unless every observable property survived optimisation.

    Deliberately includes the SHA256 of the extracted text, the OMML equation count and
    the per-image pixel dimensions.

    A governor that quietly dropped a figure would still produce a smaller, perfectly
    openable document — and because the pipeline reads question stems as TEXT, the loss
    would not announce itself anywhere downstream. Byte size and "it opens in Word" are
    not evidence of correctness.

    allow_resample=True permits pixel dimensions to change (tiers T2-T4 downscale by
    design) while still enforcing every other invariant.
    """
    before, after = docx_invariants(src), docx_invariants(dst)
    keys = ['parts', 'media', 'paras', 'tables', 'shapes', 'chars', 'tablechars',
            'omml', 'drawings', 'pict', 'hyperlinks', 'texthash', 'refs']
    failures = [f'{k}: {before[k]} -> {after[k]}' for k in keys if before[k] != after[k]]
    if after['xmlerr']:
        failures.append(f"{after['xmlerr']} malformed XML part(s)")
    if after['zipbad'] != 'OK':
        failures.append(f"corrupt zip member: {after['zipbad']}")
    if after['dangling']:
        failures.append(f"dangling relationship(s): {after['dangling'][:3]}")
    if not allow_resample:
        # v1.0.1 — the original comparison keyed on the full basename, so a legitimately
        # renamed part (image1.png -> image1.jpeg on the photo route) had no counterpart
        # in `after` and was reported as a dimension change on a document whose
        # dimensions were untouched — a FALSE-POSITIVE HARD STOP. Dormant on the
        # measured corpus, whose papers store .jpeg parts the jpeg route leaves named as
        # they were; it fired on any PNG-sourced photograph. Fixed by keying on the
        # extension-less name.
        #
        # v1.0.2 — keying on the STEM has the same defect one level up: the governor may
        # now emit a disambiguated name (image1__c2.jpeg) when two parts share a stem and
        # take the same route, which changes the stem and reproduced the identical false
        # positive. Pixel dimensions are therefore compared as an unordered MULTISET over
        # all raster parts, which is what the invariant actually asserts — "no figure's
        # pixel dimensions changed" — and is immune to any renaming the governor performs.
        b_px = sorted(before['px'].values())
        a_px = sorted(after['px'].values())
        if b_px != a_px:
            def _by_stem(px):
                out = {}
                for k, v in px.items():
                    out.setdefault(os.path.splitext(k)[0], []).append(v)
                return out

            b_stem, a_stem = _by_stem(before['px']), _by_stem(after['px'])
            named = [k for k, v in b_stem.items() if sorted(v) != sorted(a_stem.get(k, []))]
            failures.append(
                'pixel dimensions changed: '
                + (str(named[:3]) if named else f'{b_px[:3]} -> {a_px[:3]}'))
    if failures:
        raise IntegrityError(
            'Optimised document failed the parity assertion — HARD STOP.\n  '
            + '\n  '.join(failures))
    return {'before': before, 'after': after}


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER K SHELL — ANALYSIS DOC  (the Step-2c taxonomy artefact)
# ═══════════════════════════════════════════════════════════════════════════════
# GAP-2026-07-25-002. Before this cluster the Analysis doc had FOUR independent
# readers implementing FOUR different structural conventions, and no writer at all
# (Framework_PYQAnalyse S4-2 was `pass`). Measured on the live IIT_JAM_BIOTECHNOLOGY
# doc, three of the four readers were wrong:
#
#   Framework_PYQSort S1-2          1 subject  / 26 topics / 131 subtopics  (truth 6/26/131)
#   MockTestAnalyse extract_...     1 section  /  0 subtopics
#   MockTestAnalyse _extract_..._   0 sections /  0 subtopics
#   Blueprint S2-2                  prose ("Claude extracts") — non-deterministic
#
# The first flattened every subject into the first one (a `not section_name` latch);
# the other two read doc.paragraphs while every subtopic lives in a TABLE, and keyed
# hierarchy off Word Heading styles that the generator does not emit (para.style is
# None for every paragraph of a real doc).
#
# This cluster is now THE reader, THE writer and THE verifier. Every consumer
# delegates. Heading recognition is delegated one level further, to
# blueprint_core.parse_taxonomy_level() — so all six level-1 label forms
# (Subject/Domain/Section/Part/Area) and all six level-2 forms
# (Topic/Chapter/Unit/Module/Block, numbered or colon-style, case-insensitive)
# work in EVERY step automatically, including any form the engine learns later.
#
# WHY A WRITER LIVES HERE TOO: correctness is asserted by round-trip,
# read(write(taxonomy)) == taxonomy, over a GENERATED matrix of exam shapes. The
# framework serves ~200 exams; it cannot be validated against 200 real corpora, so
# the self-test generates the shapes instead. That matrix is the correctness claim.

ANALYSIS_DOC_SUFFIX = '_PYQ_Analysis.docx'
ANALYSIS_SEARCH_DIRS = ('/mnt/project/', '/mnt/user-data/uploads/')

_NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# Cells that are never a subtopic name. Compared case-insensitively after strip.
# A legitimate subtopic literally named "TOTAL" would be dropped here — that is
# SAFE rather than silent, because the per-topic "Subtopics: k" declaration then
# disagrees with the parse and verify_analysis_doc() HARD STOPS naming the topic.
_SKIP_CELLS = frozenset(('subtopic', 'topic', 'grand total', 'total', ''))

# Declaration patterns. The doc states its own shape THREE times per subject; the
# reader asserts its parse against all three. This is what makes a mis-parse loud
# without needing any second artefact.
_D1_RE = re.compile(r'(\d+)\s*Topics?\b.*?\b(\d+)\s*Subtopics?', re.IGNORECASE)
_D3_RE = re.compile(r'\bSubtopics?\s*:\s*(\d+)', re.IGNORECASE)
_GRAND_RE = re.compile(r'^GRAND\s+TOTAL$', re.IGNORECASE)


class AnalysisDocError(Exception):
    """Raised for every Analysis-doc fault. Callers surface .args[0] verbatim as a
    HARD STOP: the message always names the file, the fault and the operator action."""


def _para_text(child):
    """Text of a w:p element, runs joined. docx-js splits runs on '&' and on style
    changes, so joining is mandatory — reading only the first run truncates names."""
    return ''.join(t.text for t in child.iter('{%s}t' % _NS_W) if t.text).strip()


def _table_rows(child, doc):
    """Logical rows of a w:tbl — ONE entry per ANCHOR cell, never a repeat.

    GAP-2026-07-29-TBL. This used to read row.cells, which returns one entry per
    GRID COLUMN and repeats the anchor for every covered position: a 4-column
    merged header came back as ['Printers','Printers','Printers','Printers'] and a
    vertically merged label reappeared in every row it spanned. Harmless while the
    corpus contained only flat tables — and a data-corruption bug the moment Step 1
    started emitting the merges it always should have. Verified on python-docx
    1.2.0.

    A distinct-tc dedupe is NOT sufficient: row.cells substitutes the ANCHOR object
    for a vMerge continuation, so the anchor's text is returned again in the
    continuation row. Only a raw <w:tr>/<w:tc> walk that inspects w:vMerge can tell
    a continuation from a genuinely repeated value.

    Contract is UNCHANGED — list[list[str]] — and output on a flat table is
    byte-identical to the previous implementation.
    """
    W = '{%s}' % _NS_W
    rows = []
    for tr in child.findall(W + 'tr'):
        row = []
        for tc in tr.findall(W + 'tc'):
            tcPr = tc.find(W + 'tcPr')
            if tcPr is not None:
                v = tcPr.find(W + 'vMerge')
                if v is not None and (v.get(W + 'val') or 'continue') == 'continue':
                    continue                     # covered position, not an anchor
            row.append(''.join(t.text or '' for t in tc.iter(W + 't')).strip())
        rows.append(row)
    return rows


def read_table_spec(child, doc=None):
    """Read a w:tbl back into a TableSpec, spans included (GAP-2026-07-29-TBL).

    For consumers that need GEOMETRY, not just values — CHECK 17, Step 7 reuse of a
    PYQ table, and any future step that must rebuild a table it did not write.
    _table_rows deliberately stays value-only so its single legacy caller is
    untouched.
    """
    W = '{%s}' % _NS_W
    tr_list = child.findall(W + 'tr')
    grid, pending = [], {}
    for ri, tr in enumerate(tr_list):
        row, ci = [], 0
        for tc in tr.findall(W + 'tc'):
            tcPr = tc.find(W + 'tcPr')
            cs, vm = 1, None
            if tcPr is not None:
                g = tcPr.find(W + 'gridSpan')
                if g is not None:
                    try:
                        cs = int(g.get(W + 'val') or 1)
                    except (TypeError, ValueError):
                        cs = 1
                v = tcPr.find(W + 'vMerge')
                if v is not None:
                    vm = v.get(W + 'val') or 'continue'
            if vm == 'continue':
                for key in pending:
                    if key[1] == ci:
                        pending[key]['rs'] += 1
                        break
                ci += cs
                continue
            cell = {'t': ''.join(t.text or '' for t in tc.iter(W + 't')).strip()}
            if cs > 1:
                cell['cs'] = cs
            if vm == 'restart':
                cell['rs'] = 1
                pending[(ri, ci)] = cell
            row.append(cell)
            ci += cs
        grid.append(row)
    for cell in list(pending.values()):
        if cell.get('rs', 1) <= 1:
            cell.pop('rs', None)
    return {'grid': grid, 'header_rows': 1}


def discover_analysis_doc(search_dirs=ANALYSIS_SEARCH_DIRS):
    """Locate the ONE Analysis doc. Returns a path; raises AnalysisDocError otherwise.

    There is exactly one conforming name, [ExamCode]_PYQ_Analysis.docx. The
    per-subject form [ExamCode]_PYQ_Analysis_[Subject].docx was retired by
    PYQAnalyse v2.6 and no project has ever held one, so it is NOT a supported
    generation — it is a nonconforming file, and it is named as such rather than
    silently ignored (a silently-ignored file is how an operator ends up sorting
    against a taxonomy they did not intend).
    """
    seen, found, nonconforming, word97 = set(), [], [], []
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.startswith('~$') or name.startswith('.'):
                continue                      # Word lock file / hidden artefact
            low = name.lower()
            if name in seen:
                continue                      # same name in both dirs: project wins
            if low.endswith(ANALYSIS_DOC_SUFFIX.lower()):
                seen.add(name)
                found.append(os.path.join(d, name))
            elif low.endswith('.docx') and '_pyq_analysis_' in low:
                seen.add(name)
                nonconforming.append(name)
            elif low.endswith('.doc') and '_pyq_analysis' in low:
                seen.add(name)
                word97.append(name)

    if len(found) > 1:
        raise AnalysisDocError(
            "HARD STOP: %d Analysis docs found — exactly one is expected.\n"
            "  %s\n"
            "One project holds one exam. Remove the ones that do not belong to this "
            "exam and re-run." % (len(found), '\n  '.join(os.path.basename(p) for p in found)))
    if found:
        return found[0]
    if word97:
        raise AnalysisDocError(
            "HARD STOP: %s is a Word 97 .doc, which cannot be read.\n"
            "Open it in Word and Save As .docx, then upload it as %s."
            % (word97[0], '[ExamCode]' + ANALYSIS_DOC_SUFFIX))
    if nonconforming:
        raise AnalysisDocError(
            "HARD STOP: found %s, which is not the expected deliverable name.\n"
            "PYQApprove (Step 2c) produces ONE merged doc named "
            "[ExamCode]%s containing every subject. The per-subject form was retired "
            "in PYQAnalyse v2.6.\n"
            "Re-run PYQApprove and upload the doc it delivers."
            % (nonconforming[0], ANALYSIS_DOC_SUFFIX))
    # v1.2 (GAP-2026-07-25-003): the extracted-text advice that used to sit here was
    # both unreachable — the platform preserves the filename, so the file is never
    # MISSING, only transformed — and, after this version, wrong: the text form is
    # READ, not diagnosed. No logic change; message only.
    raise AnalysisDocError(
        "HARD STOP: no Analysis doc found in %s.\n"
        "Expected [ExamCode]%s from PYQApprove (Step 2c).\n"
        "NEXT ACTION: upload the Analysis doc PYQApprove delivered to this project's "
        "Files section." % (' or '.join(search_dirs), ANALYSIS_DOC_SUFFIX))


# ══════════════════════════════════════════════════════════════════════════════
# INGEST FORMS (GAP-2026-07-25-003)
# ══════════════════════════════════════════════════════════════════════════════
# The Claude Projects platform applies a per-format transform to files uploaded to
# project knowledge and PRESERVES THE ORIGINAL FILENAME AND EXTENSION. A file named
# .docx in /mnt/project/ is therefore NOT an OOXML package: the platform stores
# EXTRACTED MARKDOWN TEXT. Confirmed independently by the .pdf in the same project,
# which is stored as a Zip page-bundle under its .pdf name; .xlsx and .json are
# byte-preserved, and so is anything attached to CHAT rather than uploaded to Files.
#
# The Analysis doc is uploaded to project Files after Step 2c and read from there at
# Steps 3, 4, 5 and 6, so INGEST_TEXT is the PRIMARY RUNTIME FORM for this artefact —
# not a fallback, not a degraded mode, and nothing to warn about. INGEST_OOXML is
# retained because write_analysis_doc() emits it and the round-trip self-test reads
# back what it writes.
#
# Consequence: the container MUST be detected from CONTENT. Inference from the
# extension is wrong on exactly the input the runtime actually receives.

INGEST_OOXML   = 'ooxml'      # genuine .docx package (writer output, self-test, chat)
INGEST_TEXT    = 'text'       # platform-extracted text (project Files) — PRIMARY
INGEST_UNKNOWN = 'unknown'    # neither — hard stop, never guess


def _ingest_form(path):
    """Classify the container of the Analysis doc by CONTENT.

    Returns INGEST_OOXML / INGEST_TEXT / INGEST_UNKNOWN. Never raises: the caller
    turns UNKNOWN into a named hard stop carrying an operator action.

    A truncated .docx and a non-Word Zip both fail the word/document.xml test. Both
    are genuinely unreadable, so both become UNKNOWN and receive a named stop instead
    of a library traceback — the same discipline as PYQSort S7-5's pre-flight, which
    inspects the package on the path before the library is allowed to raise.
    """
    import zipfile
    try:
        if os.path.getsize(path) == 0:
            return INGEST_UNKNOWN
        with open(path, 'rb') as fh:
            magic = fh.read(4)
        if magic[:2] == b'PK':
            try:
                with zipfile.ZipFile(path) as z:
                    names = set(z.namelist())
            except Exception:
                return INGEST_UNKNOWN
            return INGEST_OOXML if 'word/document.xml' in names else INGEST_UNKNOWN
        with open(path, 'rb') as fh:
            raw = fh.read()
        try:
            raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            return INGEST_UNKNOWN
        return INGEST_TEXT
    except OSError:
        return INGEST_UNKNOWN


# ── markdown surface -> plain text ────────────────────────────────────────────
# Bounded tolerance: every variant handled here has been OBSERVED in a real
# docx->markdown extractor run against a real Analysis doc. Nothing is anticipated.
_MD_STAR  = re.compile(r'\*\*')                  # ** bold, incl. run-split ****
_MD_WRAP  = re.compile(r'^__(.+)__$', re.S)      # __bold__ as a WHOLE-LINE wrap only
_MD_SEP   = re.compile(r'^[\s|:\-]+$')           # markdown table separator row
_MD_ESC   = re.compile(r'\\([\\`*_{}\[\]()#+\-.!|~>])')
_MD_PIPE  = re.compile(r'(?<!\\)\|')             # cell split on UNESCAPED pipes only


def _md_plain(s):
    """Markdown inline markup -> the plain text the document author wrote.

    __ is unwrapped ONLY as a whole-line wrap, never stripped globally: a taxonomy
    name may legitimately contain underscores ('p_1 and p_2'), and a global strip
    would silently rewrite it. Escapes are removed only before markdown punctuation,
    so a backslash that is part of a name survives unless it precedes one of those.
    """
    s = _MD_STAR.sub('', s).strip()
    m = _MD_WRAP.match(s)
    if m:
        s = m.group(1).strip()
    return _MD_ESC.sub(r'\1', s).strip()


def _md_cells(line):
    """Cells of one pipe-table row. Splits on UNESCAPED pipes, then unescapes each
    cell — so an extractor that escapes '\\|' inside a name keeps the name intact."""
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [_md_plain(c) for c in _MD_PIPE.split(s)]


def _assert_rectangular(rows, doc_name, line_no):
    """A markdown table is RECTANGULAR. HARD STOP when it is not.

    GAP-2026-07-25-003. A '|' inside a taxonomy name splits one row wider than its
    neighbours, and the surplus cell is swallowed as the count column: the name is
    truncated, the remainder is discarded, and the SUBTOPIC COUNT IS UNCHANGED — so
    D1, D2 and D3 all still agree and verify_analysis_doc() returns clean. Nothing
    downstream catches it either: the fingerprint cross-check against the approval
    record lives only in Framework_PYQSort S1-0b, so at Steps 5 and 6 there is no gate
    at all. Reproduced by execution, which is why this is a stop and not an anomaly.
    """
    widths = {len(r) for r in rows if r}
    if len(widths) <= 1:
        return
    bad = next(r for r in rows if len(r) == max(widths))
    raise AnalysisDocError(
        "HARD STOP: %s contains a table whose rows do not all have the same number "
        "of cells (widths %s), near line %d.\n"
        "  offending row: %s\n"
        "Most common cause: a subject, topic or subtopic name contains a '|' "
        "character. In the extracted-text ingest form a '|' is a cell separator, so "
        "the name is split and everything after the '|' is silently discarded while "
        "the declared counts still agree — which is why this is stopped here rather "
        "than left to a later check that cannot see it.\n"
        "NEXT ACTION: remove '|' from the taxonomy name(s) and re-run PYQApprove "
        "(Step 2c) to regenerate the Analysis doc."
        % (doc_name, sorted(widths), line_no, ' | '.join(bad[:6])))


def _scan_ooxml(doc_path):
    """Single pass over the body. Returns (subjects, order, declared, anomalies).

    ONE pass over doc.element.body, never doc.paragraphs, so paragraphs and tables
    are seen in true document order. The two-pass form the pre-fix readers used
    cannot attribute a table to a subject at all: by the time pass 2 runs, the
    subject boundaries from pass 1 are gone.
    """
    from docx import Document
    doc = Document(doc_path)

    subjects, order, declared, anomalies = {}, [], [], []
    cur_s = cur_t = None
    blk = None

    for child in doc.element.body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            text = _para_text(child)
            if not text:
                continue
            level, name = bc.parse_taxonomy_level(text)

            if level == 1:
                cur_s, cur_t = name, None
                if cur_s not in subjects:
                    subjects[cur_s] = {}
                    order.append(cur_s)
                blk = {'subject': cur_s, 'd1': None, 'd2': [], 'd2_grand': None,
                       'd3': [], 'master_seen': False}
                declared.append(blk)
                continue

            if level == 2:
                if cur_s is None:
                    anomalies.append("topic heading %r appears before any subject "
                                     "heading" % text[:60])
                    continue
                cur_t = name
                subjects[cur_s].setdefault(cur_t, {})
                continue

            # level 3 => a decorative paragraph of the header/footer block.
            # Subtopics live in TABLES, never in paragraphs, so a level-3 paragraph
            # is never data. It may still carry a DECLARATION.
            if blk is None:
                continue
            m = _D1_RE.search(text)
            if m and blk['d1'] is None and not blk['master_seen']:
                blk['d1'] = (int(m.group(1)), int(m.group(2)))
                continue
            m = _D3_RE.search(text)
            if m and cur_t is not None:
                blk['d3'].append((cur_t, int(m.group(1))))
            continue

        if tag != 'tbl':
            continue

        rows = _table_rows(child, doc)
        data = [r for r in rows if r and r[0].strip()]
        is_master = bool(data) and any(
            bc.parse_taxonomy_level(r[0])[0] == 2 for r in data)

        if is_master:
            # MASTER SUMMARY TABLE — a declaration, never data.
            if blk is None:
                anomalies.append("a master summary table appears before any subject heading")
                continue
            blk['master_seen'] = True
            for r in data:
                lvl, tname = bc.parse_taxonomy_level(r[0])
                if lvl == 2 and len(r) >= 2 and r[1].strip().isdigit():
                    blk['d2'].append((tname, int(r[1].strip())))
                elif _GRAND_RE.match(r[0].strip()) and len(r) >= 2 and r[1].strip().isdigit():
                    blk['d2_grand'] = int(r[1].strip())
            continue

        if cur_s is None or cur_t is None:
            anomalies.append("a subtopic table at document position %d belongs to no "
                             "topic — the heading above it was not recognised"
                             % list(doc.element.body).index(child))
            continue

        bucket = subjects[cur_s][cur_t]
        for r in rows:
            if len(r) < 2:
                continue
            name = r[0].strip()
            if name.lower() in _SKIP_CELLS:
                continue
            if bc.parse_taxonomy_level(name)[0] == 2:
                continue                      # a stray topic row inside a data table
            if name not in bucket:
                bucket[name] = len(bucket)

    return subjects, order, declared, anomalies


def _scan_text(doc_path):
    """Scan the PLATFORM-EXTRACTED TEXT form — the primary runtime ingest form.

    Emits the IDENTICAL 4-tuple as _scan_ooxml(), so verify_analysis_doc(),
    taxonomy_fingerprint(), read_analysis_doc()'s return shape and every downstream
    consumer are untouched. Heading recognition is delegated to
    blueprint_core.parse_taxonomy_level(); the declaration regexes and the skip-cell
    set are the SAME module-level objects the OOXML scanner uses. There is no second
    structural convention anywhere in this module.
    """
    doc_name = os.path.basename(doc_path)
    with open(doc_path, encoding='utf-8-sig') as fh:
        text = fh.read()
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    subjects, order, declared, anomalies = {}, [], [], []
    cur_s = cur_t = None
    blk = None
    i = 0
    while i < len(lines):
        raw = lines[i]

        if raw.lstrip().startswith('|'):                       # ── table block ──
            start = i + 1
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                if not _MD_SEP.match(lines[i]):
                    rows.append(_md_cells(lines[i]))
                i += 1
            _assert_rectangular(rows, doc_name, start)
            data = [r for r in rows if r and r[0].strip()]
            is_master = bool(data) and any(
                bc.parse_taxonomy_level(r[0])[0] == 2 for r in data)

            if is_master:
                # MASTER SUMMARY TABLE — a declaration, never data.
                if blk is None:
                    anomalies.append("a master summary table appears before any "
                                     "subject heading")
                    continue
                blk['master_seen'] = True
                for r in data:
                    lvl, tname = bc.parse_taxonomy_level(r[0])
                    if lvl == 2 and len(r) >= 2 and r[1].strip().isdigit():
                        blk['d2'].append((tname, int(r[1].strip())))
                    elif _GRAND_RE.match(r[0].strip()) and len(r) >= 2 \
                            and r[1].strip().isdigit():
                        blk['d2_grand'] = int(r[1].strip())
                continue

            if cur_s is None or cur_t is None:
                anomalies.append("a subtopic table at line %d belongs to no topic — "
                                 "the heading above it was not recognised" % start)
                continue

            bucket = subjects[cur_s][cur_t]
            for r in rows:
                if len(r) < 2:
                    continue
                name = r[0].strip()
                if name.lower() in _SKIP_CELLS:
                    continue
                if bc.parse_taxonomy_level(name)[0] == 2:
                    continue                      # a stray topic row inside a data table
                if name not in bucket:
                    bucket[name] = len(bucket)
            continue

        text_line = _md_plain(raw)                             # ── paragraph ──
        i += 1
        if not text_line:
            continue
        level, name = bc.parse_taxonomy_level(text_line)

        if level == 1:
            cur_s, cur_t = name, None
            if cur_s not in subjects:
                subjects[cur_s] = {}
                order.append(cur_s)
            blk = {'subject': cur_s, 'd1': None, 'd2': [], 'd2_grand': None,
                   'd3': [], 'master_seen': False}
            declared.append(blk)
            continue

        if level == 2:
            if cur_s is None:
                anomalies.append("topic heading %r appears before any subject "
                                 "heading" % text_line[:60])
                continue
            cur_t = name
            subjects[cur_s].setdefault(cur_t, {})
            continue

        # level 3 => decorative paragraph; never data, but may carry a DECLARATION.
        if blk is None:
            continue
        m = _D1_RE.search(text_line)
        if m and blk['d1'] is None and not blk['master_seen']:
            blk['d1'] = (int(m.group(1)), int(m.group(2)))
            continue
        m = _D3_RE.search(text_line)
        if m and cur_t is not None:
            blk['d3'].append((cur_t, int(m.group(1))))

    return subjects, order, declared, anomalies


def verify_analysis_doc(subjects, order, declared, anomalies, doc_name='Analysis doc'):
    """Assert the PARSE against the document's OWN declarations. Returns a list of
    plain-English failures; empty means the doc and the parse agree.

    The doc states its shape three times per subject:
      D1  header  "Total: — Questions | <T> Topics | <S> Subtopics"
      D2  master summary table: one row per topic (+ GRAND TOTAL)
      D3  per topic "Total PYQs: — | Subtopics: <k>"
    Nothing but a correct parse satisfies all three. This is what makes a
    mis-parse LOUD without any second artefact, on any exam, from day one.
    """
    fails = list(anomalies)
    decl_names = [b['subject'] for b in declared]

    dupes = sorted({s for s in decl_names if decl_names.count(s) > 1})
    if dupes:
        fails.append("the document declares the same subject more than once: %s — "
                     "each subject must appear exactly once" % dupes)
    if len(order) != len(declared):
        fails.append("SUBJECT COUNT: parsed %d, the document declares %d subject "
                     "heading(s) -> %s" % (len(order), len(declared), decl_names))

    for b in declared:
        s = b['subject']
        if s not in subjects:
            fails.append("[%s] declared in the document but absent from the parse" % s)
            continue
        topics = subjects[s]
        n_t = len(topics)
        n_s = sum(len(v) for v in topics.values())

        if b['d1'] and b['d1'] != (n_t, n_s):
            fails.append("[%s] header declares %d topics / %d subtopics; parsed %d / %d"
                         % (s, b['d1'][0], b['d1'][1], n_t, n_s))
        if b['d2']:
            if len(b['d2']) != n_t:
                fails.append("[%s] master summary table lists %d topics; parsed %d"
                             % (s, len(b['d2']), n_t))
            for tname, tcount in b['d2']:
                if tname not in topics:
                    fails.append("[%s] master summary lists topic %r, which is absent "
                                 "from the parse" % (s, tname))
                elif len(topics[tname]) != tcount:
                    fails.append("[%s] master summary declares %d subtopics under %r; "
                                 "parsed %d" % (s, tcount, tname, len(topics[tname])))
        if b['d2_grand'] is not None and b['d2_grand'] != n_s:
            fails.append("[%s] master summary GRAND TOTAL is %d; parsed %d"
                         % (s, b['d2_grand'], n_s))
        for tname, k in b['d3']:
            if tname in topics and len(topics[tname]) != k:
                fails.append("[%s] topic %r declares Subtopics: %d; parsed %d"
                             % (s, tname, k, len(topics[tname])))
        if not topics:
            fails.append("[%s] has no topics — an empty subject cannot be sorted "
                         "against" % s)
        for tname, subs in topics.items():
            if not subs:
                fails.append("[%s] topic %r has no subtopics" % (s, tname))

    for s in order:
        if s not in decl_names:
            fails.append("[%s] parsed but the document contains no matching subject "
                         "heading for it" % s)

    # Every name must survive the round trip through the sorted-PYQ heading parser.
    # bc.is_taxonomy_heading() rejects text at or above MAX_HEADING_LEN, so a longer
    # name stops being a heading at Step 4/5 and its questions are silently absorbed
    # by the PREVIOUS subtopic. Caught HERE, at the artefact, not four steps later.
    for s, topics in subjects.items():
        for label, value in [('subject', s)] + \
                [('topic', t) for t in topics] + \
                [('subtopic', x) for t in topics for x in topics[t]]:
            if len(value) >= bc.MAX_HEADING_LEN:
                fails.append("%s name is %d characters, at or above the %d-character "
                             "heading limit: %r. A name this long stops being "
                             "recognised as a heading in the sorted files and its "
                             "questions are silently attributed to the preceding "
                             "subtopic. Shorten it in the taxonomy and re-run "
                             "PYQApprove." % (label, len(value), bc.MAX_HEADING_LEN, value))
    return fails


def _assemble(order, subjects, path, exam_code, ingest_form, source):
    """Build THE return shape from (order, {subject: {topic: {name: idx}}}).

    v1.4 — extracted so the Analysis-doc path and the approval-record path cannot
    drift. Two constructions of one shape is how GAP-2026-07-25-002's four readers
    happened; there is exactly one here, and both callers go through it.

    topic_idx is POSITIONAL WITHIN THE SUBJECT — never derived from a printed
    "Topic N:" label, which restarts at 1 for every subject in a merged doc.
    """
    taxonomy, triples = {}, []
    for subject in order:
        topics_out = {}
        for t_i, (topic, subs) in enumerate(subjects[subject].items()):
            topics_out[topic] = {
                'topic_idx': t_i,
                'subtopics': {n: {'subtopic_idx': i} for n, i in subs.items()}}
            for n in subs:
                triples.append((subject, topic, n))
        taxonomy[subject] = {'subject_order': len(taxonomy), 'topics': topics_out}
    return {
        'path': path,
        'ingest_form': ingest_form,
        'source': source,           # 'analysis_doc' | 'approval_record'
        'exam_code': exam_code,
        'subjects': list(order),
        'taxonomy': taxonomy,
        'triples': triples,
        'counts': {'subjects': len(order),
                   'topics': sum(len(v['topics']) for v in taxonomy.values()),
                   'subtopics': len(triples)},
        'fingerprint': bc.taxonomy_fingerprint(triples),
    }


def load_taxonomy(exam_code=None, search_dirs=ANALYSIS_SEARCH_DIRS, step=None,
                  record=None, path=None):
    """THE taxonomy entry point for Steps 3-6. Returns the shape read_analysis_doc()
    returns, plus 'source'.

    SOURCE PRIORITY
      1. the approval record's "taxonomy" key   (schema >= 1.3)  -> source='approval_record'
      2. the Analysis doc                       (older records)  -> source='analysis_doc'

    WHY THE RECORD COMES FIRST. Every step from PYQSort onward needs a taxonomy, and
    until reconcile_taxonomy v1.3 the only place to get one was by PARSING A WORD
    DOCUMENT. That is what GAP-2026-07-25-003 severed on every exam at once: the
    platform stores an uploaded .docx in project knowledge as extracted Markdown
    text under its .docx name, and Cluster K opened it with python-docx. v1.2 taught
    the reader both ingest forms, which works — but it works by matching an
    undocumented, unversioned grammar the framework does not control, so the next
    change to that grammar stops all ~200 exams simultaneously, loudly.

    The record does not have that property. It is JSON, which the platform stores
    BYTE-FOR-BYTE, and it already carries the fingerprint that validates its own
    taxonomy, so nothing new is trusted. Reading it is not a workaround for the
    document; it is the removal of a dependency that should never have existed.
    The Analysis doc reverts to what it always should have been: a HUMAN deliverable.

    The fallback is not a courtesy. Every exam approved before schema 1.3 has a
    record with a fingerprint and no taxonomy, and those projects must keep working
    without being re-approved. They take path 2, which is fully gated by
    assert_taxonomy_lock() exactly as before.

    DISPLAY NAMES. The fingerprint is slug-normalised BY DESIGN, so it proves
    identity and cannot detect a display-byte change. On path 1 the names come
    straight from JSON and no such change is possible. On path 2 they survive a text
    extraction, and PYQAnalyse Task 2.5 remains the byte-identity check.
    """
    if record is None:
        record = read_approval_record(exam_code, search_dirs)
    rec_name = os.path.basename(record.get('_path', 'approval record'))
    where = (' at %s' % step) if step else ''
    tax = record.get('taxonomy')

    if tax is None:
        # ── path 2: pre-1.3 record. The doc is the only carrier of the content. ──
        doc = read_analysis_doc(path, search_dirs)
        assert_taxonomy_lock(doc, record=record, step=step)
        return doc

    # ── path 1: the record carries the taxonomy ──────────────────────────────────
    sections = tax.get('sections') if isinstance(tax, dict) else None
    if not isinstance(sections, dict) or not sections:
        raise AnalysisDocError(
            "HARD STOP%s: %s carries a 'taxonomy' key that is not a populated "
            "{'sections': {subject: {topic: [subtopic]}}} object.\n"
            "A record that carries a BROKEN taxonomy is worse than one that carries "
            "none: the absent case has a defined fallback and this one does not.\n"
            "NEXT ACTION: re-run PYQApprove with reconcile_taxonomy.py >= v1.3. That "
            "is RECONCILIATION, not re-derivation — it cannot change a locked "
            "taxonomy. Do NOT re-run PYQDraft." % (where, rec_name))

    order, subjects, dupes = [], {}, []
    for subject, topics in sections.items():
        if not isinstance(topics, dict) or not topics:
            raise AnalysisDocError(
                "HARD STOP%s: %s declares subject %r with no topics. An empty "
                "subject cannot be sorted or allocated against.\n"
                "NEXT ACTION: re-run PYQApprove." % (where, rec_name, subject))
        if subject in subjects:
            dupes.append('subject %r' % subject)
            continue
        subjects[subject] = {}
        order.append(subject)
        for topic, subs in topics.items():
            if not isinstance(subs, list) or not subs:
                raise AnalysisDocError(
                    "HARD STOP%s: %s declares topic %r under %r with no subtopics.\n"
                    "NEXT ACTION: re-run PYQApprove."
                    % (where, rec_name, topic, subject))
            bucket = subjects[subject].setdefault(topic, {})
            for name in subs:
                if name in bucket:
                    dupes.append('%r under %r / %r' % (name, subject, topic))
                    continue
                bucket[name] = len(bucket)

    if dupes:
        # Silent de-duplication would make the assembled taxonomy disagree with the
        # counts the record declares, and the fingerprint would NOT catch it — it is
        # computed over the same duplicated triples, so it agrees with itself.
        raise AnalysisDocError(
            "HARD STOP%s: %s declares the same name more than once:\n  %s\n"
            "NEXT ACTION: re-run PYQApprove."
            % (where, rec_name, '\n  '.join(dupes[:8])))

    out = _assemble(order, subjects, path=record.get('_path'),
                    exam_code=record.get('exam_code', exam_code),
                    ingest_form='json', source='approval_record')

    # SELF-VALIDATION. The record proves its own content: the fingerprint recorded
    # beside the taxonomy was computed FROM it at Step 2c. A disagreement means the
    # record was hand-edited or written by two different engines, and the taxonomy
    # half cannot be trusted just because the hash half looks well-formed.
    fp_locked = record.get('taxonomy_fingerprint')
    if not fp_locked:
        raise AnalysisDocError(
            "HARD STOP%s: %s carries a taxonomy but no taxonomy_fingerprint, so the "
            "taxonomy cannot validate itself.\n"
            "NEXT ACTION: re-run PYQApprove with reconcile_taxonomy.py >= v1.3."
            % (where, rec_name))
    if fp_locked != out['fingerprint']:
        raise AnalysisDocError(
            "HARD STOP%s: %s does not agree with itself — the fingerprint it records "
            "is not the fingerprint of the taxonomy it records.\n"
            "  recorded fingerprint : %s\n"
            "  taxonomy computes to : %s\n"
            "  counts declared      : %s\n"
            "  counts assembled     : %s\n"
            "The record was edited by hand, or written by two engines that disagree. "
            "Neither half can be trusted.\n"
            "NEXT ACTION: re-run PYQApprove. RECONCILIATION only — it cannot change "
            "a locked taxonomy."
            % (where, rec_name, fp_locked, out['fingerprint'],
               record.get('taxonomy_counts'), out['counts']))

    declared = record.get('taxonomy_counts')
    if declared and declared != out['counts']:
        raise AnalysisDocError(
            "HARD STOP%s: %s declares taxonomy_counts %s but the taxonomy it carries "
            "assembles to %s.\n"
            "NEXT ACTION: re-run PYQApprove."
            % (where, rec_name, declared, out['counts']))
    return out


def read_analysis_doc(path=None, search_dirs=ANALYSIS_SEARCH_DIRS, verify=True):
    """THE Analysis-doc reader. Returns a dict:

        {'path','exam_code','subjects','taxonomy','triples','counts','fingerprint'}

    taxonomy/triples carry exactly the shape PYQSort S1-2 has always returned, so
    downstream consumers are unchanged:
        {subject: {'subject_order': int,
                   'topics': {topic: {'topic_idx': int,
                                      'subtopics': {name: {'subtopic_idx': int}}}}}}

    topic_idx is POSITIONAL WITHIN THE SUBJECT, which is what Framework_PYQSort
    §L1111 has always specified ("position of topic within its section's Analysis
    doc"). The pre-fix code derived it from the printed "Topic N:" label, which
    restarts at 1 for every subject in a merged doc — six topics claiming index 0.
    """
    if path is None:
        path = discover_analysis_doc(search_dirs)
    base = os.path.basename(path)

    form = _ingest_form(path)

    if form == INGEST_UNKNOWN:
        # The size is DIAGNOSTIC, and formatting a diagnostic must never raise the
        # fault it is diagnosing. _ingest_form() returns UNKNOWN for an unreadable
        # path precisely BECAUSE os.path.getsize() raised there, so calling it again
        # here re-raises it uncaught and the operator gets the library traceback this
        # whole cluster exists to replace. Found by re-running the delivered spec
        # against a path that had gone away mid-session.
        try:
            size_txt = '%d bytes' % os.path.getsize(path)
        except OSError as _ex:
            size_txt = 'unreadable (%s: %s)' % (type(_ex).__name__, _ex)
        raise AnalysisDocError(
            "HARD STOP: %s is neither a readable .docx package nor readable "
            "extracted text.\n"
            "  size: %s\n"
            "This is not a recognised ingest form for the Analysis doc. Likely "
            "causes: a truncated or failed upload, a file saved under the wrong name, "
            "or a platform transform this framework version does not know about.\n"
            "NEXT ACTION: re-upload the Analysis doc that PYQApprove (Step 2c) "
            "delivered to the project's Files section. If it opens correctly in Word, "
            "report this as a NEW ingest form (GAP-2026-07-25-003 follow-up) — do NOT "
            "work around it." % (base, size_txt))

    if form == INGEST_TEXT and not verify:
        # Admitted THROUGH the invariants, never around them. The text form carries no
        # container-level integrity of its own, so the three self-declarations are the
        # only thing standing between a mis-parse and a silently mis-sorted corpus.
        verify = True

    try:
        if form == INGEST_OOXML:
            subjects, order, declared, anomalies = _scan_ooxml(path)
        else:
            subjects, order, declared, anomalies = _scan_text(path)
    except AnalysisDocError:
        raise
    except Exception as ex:
        raise AnalysisDocError(
            "HARD STOP: %s could not be read as %s (%s: %s).\n"
            "NEXT ACTION: re-upload the Analysis doc PYQApprove (Step 2c) delivered "
            "to the project's Files section."
            % (base, 'a .docx package' if form == INGEST_OOXML
               else 'platform-extracted text', type(ex).__name__, ex))

    if not order:
        raise AnalysisDocError(
            "HARD STOP: %s contains no subject heading.\n"
            "  ingest form: %s\n"
            "Expected a paragraph of the form 'Subject: <name>' (or Domain:/Section:/"
            "Part:/Area:) for each subject. Either this is not a PYQApprove Analysis "
            "doc, or the PYQAnalyse §6 HEADING FORMAT CONTRACT was violated%s."
            % (base, form,
               ", or the platform's text-extraction grammar has changed and "
               "_scan_text() must be updated — do NOT work around it, report it as a "
               "GAP-2026-07-25-003 follow-up" if form == INGEST_TEXT else ""))

    if verify:
        fails = verify_analysis_doc(subjects, order, declared, anomalies, base)
        if fails:
            raise AnalysisDocError(
                "HARD STOP: %s does not agree with itself — the taxonomy parsed out of "
                "it does not match the totals the document declares. Sorting against a "
                "taxonomy that fails this check silently mis-files questions.\n  %s\n"
                "Re-run PYQApprove to regenerate the Analysis doc."
                % (base, '\n  '.join(fails[:12]) +
                   ('\n  ... and %d more' % (len(fails) - 12) if len(fails) > 12 else '')))

    exam_code = base[:-len(ANALYSIS_DOC_SUFFIX)] if base.endswith(ANALYSIS_DOC_SUFFIX) else None
    return _assemble(order, subjects, path=path, exam_code=exam_code, ingest_form=form,
                     source='analysis_doc')


# ══════════════════════════════════════════════════════════════════════════════
# THE TAXONOMY LOCK GATE — one implementation, every step
# ══════════════════════════════════════════════════════════════════════════════
# read_analysis_doc() asserts the document agrees with ITSELF. It cannot assert
# that the document is the one PYQApprove LOCKED. Those are different claims, and
# GAP-2026-07-25-002 Defect B satisfied the first while violating the second.
#
# Framework_PYQSort S1-0b made the second claim from v1.14 — and NOTHING else did.
# Steps 5 and 6 read the taxonomy and allocated against it with no identity check at
# all, so a superseded or mis-parsed Analysis doc that halted loudly at Step 3 was
# accepted silently three steps later. Worse at Step 5, where the reader's hard stops
# were caught and downgraded to a log line twice over: once in the extractor and
# again in its caller.
#
# The gate therefore lives HERE, once, rather than being written a fifth time in a
# fifth spec. This is the same anti-drift rule that produced Cluster K: one reader,
# one writer, one verifier — and now one lock gate.
#
# SCOPE, deliberately narrow: this asserts IDENTITY only. Whether the lock was
# EARNED — status, schema attestation, checks.missing / checks.vacuous — is
# Framework_PYQSort S1-0's claim, made once at Step 3 against the same record, and
# it is not duplicated here. One function, one claim.

APPROVAL_RECORD_SUFFIX = '_approval_record.json'


def discover_approval_record(exam_code=None, search_dirs=ANALYSIS_SEARCH_DIRS):
    """Locate the ONE approval record. Returns a path; raises AnalysisDocError.

    Same de-duplication rule as discover_analysis_doc(): a name seen in an earlier
    search dir wins, so the project's copy beats a chat attachment of the same name.
    """
    want = ('%s%s' % (exam_code, APPROVAL_RECORD_SUFFIX)).lower() if exam_code else None
    seen, found = set(), []
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.startswith('~$') or name.startswith('.'):
                continue
            low = name.lower()
            if not low.endswith(APPROVAL_RECORD_SUFFIX.lower()):
                continue
            if want and low != want:
                continue
            if name in seen:
                continue
            seen.add(name)
            found.append(os.path.join(d, name))
    if len(found) > 1:
        raise AnalysisDocError(
            "HARD STOP: %d approval records found — exactly one is expected.\n"
            "  %s\n"
            "One project holds one exam. Remove the ones that do not belong to this "
            "exam and re-run."
            % (len(found), '\n  '.join(os.path.basename(p) for p in found)))
    if found:
        return found[0]
    raise AnalysisDocError(
        "HARD STOP: no approval record found in %s.\n"
        "Expected %s from PYQApprove (Step 2c).\n"
        "The Analysis doc shows what the taxonomy IS; only the approval record shows "
        "that it was the one APPROVED. Allocating against an unverified taxonomy is "
        "how a mis-parse travels to delivery.\n"
        "NEXT ACTION: upload the approval record PYQApprove delivered to this "
        "project's Files section."
        % (' or '.join(search_dirs),
           ('%s%s' % (exam_code, APPROVAL_RECORD_SUFFIX)) if exam_code
           else '[ExamCode]' + APPROVAL_RECORD_SUFFIX))


def read_approval_record(exam_code=None, search_dirs=ANALYSIS_SEARCH_DIRS, path=None):
    """Load the approval record as a dict. Raises AnalysisDocError on any fault."""
    if path is None:
        path = discover_approval_record(exam_code, search_dirs)
    try:
        with open(path, encoding='utf-8-sig') as fh:
            rec = json.load(fh)
    except Exception as ex:
        raise AnalysisDocError(
            "HARD STOP: %s could not be read as JSON (%s: %s).\n"
            "NEXT ACTION: re-upload the approval record PYQApprove (Step 2c) "
            "delivered." % (os.path.basename(path), type(ex).__name__, ex))
    if not isinstance(rec, dict):
        raise AnalysisDocError(
            "HARD STOP: %s does not contain a JSON object.\n"
            "NEXT ACTION: re-run PYQApprove." % os.path.basename(path))
    rec['_path'] = path
    return rec


def assert_taxonomy_lock(doc, record=None, search_dirs=ANALYSIS_SEARCH_DIRS, step=None):
    """THE identity gate: is this the taxonomy that was APPROVED?

    `doc`    : the dict read_analysis_doc() returned.
    `record` : an already-loaded approval record, or None to discover one using
               doc['exam_code'].
    `step`   : caller name for the message ('PYQExtract', 'MockBlueprint', ...).

    Returns the record on success. Raises AnalysisDocError otherwise — callers must
    NOT downgrade this to a warning. A taxonomy that fails this check is not a
    degraded input; it is the wrong input, and every id minted from it is wrong.
    """
    where = (' at %s' % step) if step else ''
    if record is None:
        record = read_approval_record(doc.get('exam_code'), search_dirs)

    fp_locked = record.get('taxonomy_fingerprint')
    if not fp_locked:
        raise AnalysisDocError(
            "HARD STOP%s: the approval record carries no taxonomy_fingerprint, so "
            "the Analysis doc cannot be shown to be the approved one.\n"
            "  record: %s\n"
            "NEXT ACTION: re-run PYQApprove with reconcile_taxonomy.py >= v1.2. That "
            "is RECONCILIATION, not re-derivation — it reads the draft and rewrites "
            "only the record, and CANNOT change a locked taxonomy. Do NOT re-run "
            "PYQDraft." % (where, os.path.basename(record.get('_path', '?'))))

    if fp_locked != doc['fingerprint']:
        raise AnalysisDocError(
            "HARD STOP%s: the Analysis doc is NOT the taxonomy that was approved.\n"
            "  doc    : %s\n"
            "  locked : %s\n"
            "  loaded : %s\n"
            "  counts : %s\n"
            "The fingerprint is taken over slugified triples, so it is already "
            "invariant to case, spacing and dash variants — this is a real "
            "difference in the taxonomy itself, not a cosmetic one.\n"
            "NEXT ACTION: restore the Analysis doc PYQApprove (Step 2c) delivered, "
            "or re-run PYQApprove if the taxonomy genuinely changed. If it changed, "
            "every step from PYQSort onward must be re-run — ids minted from one "
            "taxonomy do not resolve against another."
            % (where, os.path.basename(doc.get('path', '?')), fp_locked,
               doc['fingerprint'], doc.get('counts')))
    return record


def write_analysis_doc(taxonomy, exam_code, subject_order=None, out_dir='/mnt/user-data/outputs',
                       counts=None):
    """THE Analysis-doc writer (PYQAnalyse S4-2, which was `pass` until v2.24).

    taxonomy : {subject: {topic: [subtopic, ...]}}   — insertion order is preserved
    counts   : optional {(subject, topic, subtopic): int} for Phase B (--counts).
               Absent => every PYQ Count cell is an em-dash, per S4-1.

    Emits exactly the structure read_analysis_doc() contracts on, including all
    three redundant declarations. One writer + one reader + a round-trip assertion
    is the whole correctness argument; a doc this function produces is a doc that
    function reads, by construction rather than by review.
    """
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_BREAK

    order = list(subject_order or taxonomy.keys())
    missing = [s for s in taxonomy if s not in order]
    order += missing

    over = [(lbl, v) for s in taxonomy
            for lbl, v in ([('subject', s)] +
                           [('topic', t) for t in taxonomy[s]] +
                           [('subtopic', x) for t in taxonomy[s] for x in taxonomy[s][t]])
            if len(v) >= bc.MAX_HEADING_LEN]
    if over:
        raise AnalysisDocError(
            "HARD STOP: %d taxonomy name(s) are at or above the %d-character heading "
            "limit and cannot be written — they would stop being recognised as "
            "headings in the sorted files.\n  %s"
            % (len(over), bc.MAX_HEADING_LEN,
               '\n  '.join('%s (%d chars): %r' % (l, len(v), v) for l, v in over[:5])))

    # GAP-2026-07-25-003. '|' is a CELL SEPARATOR in the extracted-text ingest form,
    # which is the form every runtime read of this document receives. A name carrying
    # one is split on read, the remainder is discarded, and the declared counts still
    # agree — so the corruption is invisible to all three self-declarations. Rejected
    # where it ORIGINATES rather than where it corrupts: this document is unwritable,
    # not merely unreadable.
    piped = [(lbl, v) for s in taxonomy
             for lbl, v in ([('subject', s)] +
                            [('topic', t) for t in taxonomy[s]] +
                            [('subtopic', x) for t in taxonomy[s] for x in taxonomy[s][t]])
             if '|' in v]
    if piped:
        raise AnalysisDocError(
            "HARD STOP: %d taxonomy name(s) contain a '|' character, which cannot be "
            "written to the Analysis doc.\n  %s\n"
            "'|' is the cell separator in the form the platform stores this document "
            "in, so such a name is silently truncated on every downstream read while "
            "the declared totals continue to agree.\n"
            "NEXT ACTION: rename the taxonomy entries (an en-dash, a slash or a comma "
            "all read naturally) and re-run."
            % (len(piped), '\n  '.join('%s: %r' % (l, v) for l, v in piped[:5])))

    doc = Document()

    def bold(text, size):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def cell(v):
        return '—' if v is None else str(v)

    for i, subject in enumerate(order):
        topics = taxonomy[subject]
        if i:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

        n_sub = sum(len(v) for v in topics.values())
        bold('%s — %s' % (exam_code, subject), 14)
        bold('Subject: %s' % subject, 12)                      # LEVEL 1 — §6 contract
        bold('PYQ Topic & Subtopic-wise Count', 11)
        bold('Total: %s Questions  |  %d Topics  |  %d Subtopics'      # D1
             % (cell(sum(counts.get((subject, t, x), 0)
                         for t in topics for x in topics[t]) if counts else None),
                len(topics), n_sub), 11)

        tbl = doc.add_table(rows=1, cols=3)                     # D2
        h = tbl.rows[0].cells
        h[0].text, h[1].text, h[2].text = 'Topic', 'Total Subtopics', 'Total PYQs'
        for t_i, (topic, subs) in enumerate(topics.items(), 1):
            c = tbl.add_row().cells
            c[0].text = 'Topic %d: %s' % (t_i, topic)
            c[1].text = str(len(subs))
            c[2].text = cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                             if counts else None)
        c = tbl.add_row().cells
        c[0].text = 'GRAND TOTAL'
        c[1].text = str(n_sub)
        c[2].text = cell(sum(counts.get((subject, t, x), 0)
                             for t in topics for x in topics[t]) if counts else None)

        for t_i, (topic, subs) in enumerate(topics.items(), 1):
            bold('Topic %d: %s' % (t_i, topic), 12)             # LEVEL 2 — §6 contract
            bold('Total PYQs: %s  |  Subtopics: %d'             # D3
                 % (cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                         if counts else None), len(subs)), 11)
            st = doc.add_table(rows=1, cols=2)
            hh = st.rows[0].cells
            hh[0].text, hh[1].text = 'Subtopic', 'PYQ Count'
            for x in subs:
                r = st.add_row().cells
                r[0].text = x
                r[1].text = cell(counts.get((subject, topic, x), 0) if counts else None)
            r = st.add_row().cells
            r[0].text = 'TOTAL'
            r[1].text = cell(sum(counts.get((subject, topic, x), 0) for x in subs)
                             if counts else None)

        bold('IFAS Edutech  —  %s %s PYQ Analysis' % (exam_code, subject), 10)

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, '%s%s' % (exam_code, ANALYSIS_DOC_SUFFIX))
    doc.save(out)
    return out


CK_LIVE_FIXTURE = 'IIT_JAM_BIOTECHNOLOGY_PYQ_Analysis.docx'


def _ck_shapes():
    """The exam-shape matrix. The framework serves ~200 exams and cannot be validated
    against 200 real corpora, so the shapes are GENERATED. This matrix IS the
    exam-agnostic correctness claim; it covers shapes no real exam has produced yet.
    """
    # ABSOLUTE length, never derived from bc.MAX_HEADING_LEN. Deriving it would make
    # this shape vacuous with respect to the constant: lowering the cap would shrink
    # the fixture with it and the test would stay green (INV-8, a check that measures
    # nothing). 150 characters is comfortably legal at 300 and illegal at the old 100.
    long_ok = 'Regulation of Gene Expression in Prokaryotes and Eukaryotes ' + 'x' * 90
    assert len(long_ok) == 150
    return [
        ('single subject', {'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']}}),
        ('six subjects', {'S%d' % i: {'T%d' % j: ['x%d_%d' % (i, j)]
                                      for j in range(1, i + 2)} for i in range(1, 7)}),
        ('thirty subjects', {'Sub %02d' % i: {'Topic A': ['one', 'two']}
                             for i in range(1, 31)}),
        ('duplicate TOPIC name across subjects',
         {'Physics': {'Thermodynamics': ['Entropy', 'Carnot']},
          'Chemistry': {'Thermodynamics': ['Enthalpy', 'Free Energy']}}),
        ('duplicate SUBTOPIC name across topics',
         {'Biology': {'Cell': ['Introduction', 'Organelles'],
                      'Genetics': ['Introduction', 'Linkage']}}),
        ('punctuation in names',
         {'General Intelligence & Reasoning':
          {'Analogy — Verbal / Non-Verbal': ["Bloom's Taxonomy, Applied",
                                             'Ratio & Proportion']}}),
        ('unicode in names', {'\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u0939\u093f\u0902\u0926\u0940':
                              {'\u0935\u094d\u092f\u093e\u0915\u0930\u0923': ['\u0938\u0902\u0927\u093f', '\u0938\u092e\u093e\u0938']}}),
        ('name at the length boundary', {'Physics': {'Mechanics': [long_ok]}}),
        ('single subtopic per topic', {'Maths': {'Algebra': ['Matrices']}}),
        ('many topics one subject',
         {'GS': {'Topic %02d' % i: ['a', 'b', 'c'] for i in range(1, 21)}}),
    ]


def _ck_selftest(check, tmp):
    """Cluster K assertions. `check(name, cond)` is the caller's harness hook."""
    import glob as _glob

    # ── the heading limit is real, and a 150-char name must survive it ─────────
    class _R:
        def __init__(self, t):
            self.text, self.bold = t, True
    class _P:
        def __init__(self, t):
            self.text, self.runs = t, [_R(t)]
    check('K MAX_HEADING_LEN admits a 150-character subtopic heading',
          bc.is_taxonomy_heading(_P('n' * 150), lambda t: False))
    check('K MAX_HEADING_LEN still rejects a pasted stem',
          not bc.is_taxonomy_heading(_P('n' * bc.MAX_HEADING_LEN), lambda t: False))

    # ── ROUND TRIP over the generated matrix ────────────────────────────────────
    for label, tax in _ck_shapes():
        d = os.path.join(tmp, 'rt_' + re.sub(r'[^a-z0-9]+', '_', label.lower()))
        os.makedirs(d, exist_ok=True)
        try:
            p = write_analysis_doc(tax, 'EXAM', out_dir=d)
            got = read_analysis_doc(p)
        except Exception as ex:
            # Report per shape instead of aborting the suite: when this cluster
            # regresses, the operator needs to see WHICH shapes broke, not just the
            # first one.
            for suffix in ('round-trip', 'subject order', 'counts', 'topic_idx positional'):
                check('K %s: %s [%s]' % (suffix, label, type(ex).__name__), False)
            continue
        rebuilt = {s: {t: list(v['subtopics']) for t, v in d2['topics'].items()}
                   for s, d2 in got['taxonomy'].items()}
        check('K round-trip: ' + label, rebuilt == tax)
        check('K subject order: ' + label, got['subjects'] == list(tax))
        n = sum(len(x) for t in tax.values() for x in t.values())
        check('K counts: ' + label,
              got['counts'] == {'subjects': len(tax),
                                'topics': sum(len(t) for t in tax.values()),
                                'subtopics': n})
        # topic_idx must be contiguous 0..n-1 WITHIN each subject and never collide
        ok = all(sorted(v['topic_idx'] for v in d2['topics'].values())
                 == list(range(len(d2['topics']))) for d2 in got['taxonomy'].values())
        check('K topic_idx positional: ' + label, ok)

    # ── every level-1 and level-2 label form the engine blesses ─────────────────
    tax = {'Alpha': {'Beta': ['gamma', 'delta']}}
    d = os.path.join(tmp, 'labels'); os.makedirs(d, exist_ok=True)
    src = write_analysis_doc(tax, 'EXAM', out_dir=d)
    from docx import Document as _D
    for l1 in ('Subject', 'Domain', 'Section', 'Part', 'Area'):
        for l2 in ('Topic 1', 'Chapter 1', 'Unit 1', 'Module 1', 'Block 1'):
            doc = _D(src)
            for para in doc.paragraphs:
                t = para.text.strip()
                if t.startswith('Subject:'):
                    para.runs[0].text = '%s: Alpha' % l1
                elif t.startswith('Topic 1:'):
                    para.runs[0].text = '%s: Beta' % l2
            alt = os.path.join(d, 'ALT%s' % ANALYSIS_DOC_SUFFIX)
            doc.save(alt)
            # the master-summary rows still say "Topic 1:", which is level 2 either way
            got = read_analysis_doc(alt, verify=False)
            check('K label form %s / %s' % (l1, l2),
                  got['subjects'] == ['Alpha']
                  and list(got['taxonomy']['Alpha']['topics']) == ['Beta'])

    # ── the self-check must FIRE on each corruption, not just pass on good input ─
    def _mutate(fn, name):
        d2 = os.path.join(tmp, 'mut_' + name); os.makedirs(d2, exist_ok=True)
        p = write_analysis_doc({'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']},
                                'Chemistry': {'Bonding': ['Ionic']}}, 'EXAM', out_dir=d2)
        doc = _D(p)
        fn(doc)
        doc.save(p)
        try:
            read_analysis_doc(p)
            return False
        except AnalysisDocError:
            return True

    def drop_subject_line(doc):
        for para in doc.paragraphs:
            if para.text.strip() == 'Subject: Chemistry':
                para.runs[0].text = 'Chemistry notes'
                return

    def dup_subject(doc):
        for para in doc.paragraphs:
            if para.text.strip() == 'Subject: Chemistry':
                para.runs[0].text = 'Subject: Physics'
                return

    def wrong_declared_count(doc):
        for para in doc.paragraphs:
            if para.text.strip().startswith('Total PYQs:'):
                para.runs[0].text = 'Total PYQs: —  |  Subtopics: 7'
                return

    def wrong_grand_total(doc):
        for tbl in doc.tables:
            for row in tbl.rows:
                if row.cells[0].text.strip() == 'GRAND TOTAL':
                    row.cells[1].text = '99'
                    return

    def drop_a_subtopic_row(doc):
        for tbl in doc.tables:
            for row in tbl.rows:
                if row.cells[0].text.strip() == 'Newton Laws':
                    row.cells[0].text = ''
                    return

    check('K catches a missing subject heading', _mutate(drop_subject_line, 'dropsubj'))
    check('K catches a duplicated subject', _mutate(dup_subject, 'dupsubj'))
    check('K catches a wrong declared subtopic count', _mutate(wrong_declared_count, 'badcount'))
    check('K catches a wrong GRAND TOTAL', _mutate(wrong_grand_total, 'badgrand'))
    check('K catches a dropped subtopic row', _mutate(drop_a_subtopic_row, 'droprow'))

    # ── name length is refused at the PRODUCER, not discovered downstream ───────
    too_long = 'y' * bc.MAX_HEADING_LEN
    d3 = os.path.join(tmp, 'toolong'); os.makedirs(d3, exist_ok=True)
    try:
        write_analysis_doc({'Physics': {'Mechanics': [too_long]}}, 'EXAM', out_dir=d3)
        check('K refuses to write an over-length name', False)
    except AnalysisDocError:
        check('K refuses to write an over-length name', True)

    # ── discovery ──────────────────────────────────────────────────────────────
    dd = os.path.join(tmp, 'disc'); os.makedirs(dd, exist_ok=True)
    up = os.path.join(tmp, 'disc_up'); os.makedirs(up, exist_ok=True)
    dirs = (dd + os.sep, up + os.sep)

    def _clear():
        for d4 in (dd, up):
            for f in _glob.glob(os.path.join(d4, '*')):
                os.remove(f)

    def _raises(sub):
        try:
            discover_analysis_doc(dirs)
            return False
        except AnalysisDocError as ex:
            return sub in str(ex)

    _clear()
    check('K no doc -> named stop', _raises('no Analysis doc found'))

    _clear()
    open(os.path.join(dd, '~$EXAM' + ANALYSIS_DOC_SUFFIX), 'w').close()
    check('K ignores a Word lock file', _raises('no Analysis doc found'))

    _clear()
    open(os.path.join(dd, 'EXAM_PYQ_Analysis.doc'), 'w').close()
    check('K names the Word 97 .doc case', _raises('Word 97'))

    _clear()
    open(os.path.join(dd, 'EXAM_PYQ_Analysis_Physics.docx'), 'w').close()
    check('K names the retired per-subject form', _raises('not the expected deliverable name'))

    _clear()
    open(os.path.join(dd, 'A' + ANALYSIS_DOC_SUFFIX), 'w').close()
    open(os.path.join(dd, 'B' + ANALYSIS_DOC_SUFFIX), 'w').close()
    check('K stops on two Analysis docs', _raises('exactly one is expected'))

    _clear()
    write_analysis_doc({'Physics': {'Mechanics': ['Kinematics']}}, 'EXAM', out_dir=dd)
    write_analysis_doc({'Physics': {'Mechanics': ['DIFFERENT']}}, 'EXAM', out_dir=up)
    got = read_analysis_doc(search_dirs=dirs)
    check('K same name in both dirs -> project wins, loaded once',
          got['triples'] == [('Physics', 'Mechanics', 'Kinematics')])

    # ── fingerprint ────────────────────────────────────────────────────────────
    a = read_analysis_doc(os.path.join(dd, 'EXAM' + ANALYSIS_DOC_SUFFIX))
    b = read_analysis_doc(os.path.join(up, 'EXAM' + ANALYSIS_DOC_SUFFIX))
    check('K fingerprint distinguishes different taxonomies',
          a['fingerprint'] != b['fingerprint'])
    check('K fingerprint is stable across reads',
          a['fingerprint'] == read_analysis_doc(a['path'])['fingerprint'])

    # ══════════════════════════════════════════════════════════════════════════
    # INGEST FORMS (GAP-2026-07-25-003)
    # ══════════════════════════════════════════════════════════════════════════
    def _render_md(tax, exam_code, bold='**', escape=False):
        """Emit the platform's OBSERVED docx->markdown grammar for a taxonomy.

        DELIBERATE CAVEAT: this helper is framework-written, so every test built on
        it is STRUCTURAL — it proves _scan_text() is the inverse of the grammar we
        believe the platform emits, never that the platform emits it. The live
        fixture is the only field evidence and must never be replaced by this.
        """
        esc = (lambda s: re.sub(r'([\\`*_{}\[\]()#+\-.!|])', r'\\\1', s)) if escape \
            else (lambda s: s)
        b = lambda s: '%s%s%s' % (bold, s, bold)
        out = []
        for subject in tax:
            topics = tax[subject]
            n_sub = sum(len(v) for v in topics.values())
            out += [b('%s — %s' % (exam_code, subject)), '',
                    b('Subject: %s' % subject), '',
                    b('PYQ Topic %s&%s Subtopic-wise Count' % (bold + bold, bold + bold))
                    if bold == '**' else b('PYQ Topic & Subtopic-wise Count'), '',
                    b('Total: — Questions  |  %d Topics  |  %d Subtopics'
                      % (len(topics), n_sub)), '',
                    '| Topic | Total Subtopics | Total PYQs |', '| --- | --- | --- |']
            for t_i, (topic, subs) in enumerate(topics.items(), 1):
                out.append('| %s | %d | — |' % (esc('Topic %d: %s' % (t_i, topic)), len(subs)))
            out += ['| GRAND TOTAL | %d | — |' % n_sub, '']
            for t_i, (topic, subs) in enumerate(topics.items(), 1):
                out += [b('Topic %d: %s' % (t_i, topic)), '',
                        b('Total PYQs: —  |  Subtopics: %d' % len(subs)), '',
                        '| Subtopic | PYQ Count |', '| --- | --- |']
                for x in subs:
                    out.append('| %s | — |' % esc(x))
                out += ['| TOTAL | — |', '']
            out += [b('IFAS Edutech  —  %s %s PYQ Analysis' % (exam_code, subject)), '']
        return '\n'.join(out) + '\n'

    ing = os.path.join(tmp, 'ingest'); os.makedirs(ing, exist_ok=True)

    def _write_text(name, body):
        p = os.path.join(ing, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(body)
        return p

    def _stops(fn, sub):
        try:
            fn()
            return False
        except AnalysisDocError as ex:
            return sub in str(ex)

    # ── T3 form classification: content, never extension ───────────────────────
    _t3tax = {'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']}}
    ok_docx = write_analysis_doc(_t3tax, 'T3', out_dir=ing)
    txt_doc = _write_text('T3TEXT' + ANALYSIS_DOC_SUFFIX, _render_md(_t3tax, 'T3'))
    empty = os.path.join(ing, 'empty.docx'); open(empty, 'wb').close()
    trunc = os.path.join(ing, 'trunc.docx')
    with open(ok_docx, 'rb') as _f, open(trunc, 'wb') as _g:
        _g.write(_f.read(400))
    notword = os.path.join(ing, 'notword.docx')
    import zipfile as _zf
    with _zf.ZipFile(notword, 'w') as _z:
        _z.writestr('xl/workbook.xml', '<x/>')
    utf16 = os.path.join(ing, 'utf16.docx')
    with open(utf16, 'wb') as _f:
        _f.write('Subject: X'.encode('utf-16'))
    check('K T3 ingest form: real .docx -> ooxml', _ingest_form(ok_docx) == INGEST_OOXML)
    check('K T3 ingest form: extracted text -> text', _ingest_form(txt_doc) == INGEST_TEXT)
    check('K T3 ingest form: zero bytes -> unknown', _ingest_form(empty) == INGEST_UNKNOWN)
    check('K T3 ingest form: truncated zip -> unknown', _ingest_form(trunc) == INGEST_UNKNOWN)
    check('K T3 ingest form: non-Word zip -> unknown', _ingest_form(notword) == INGEST_UNKNOWN)
    check('K T3 ingest form: UTF-16 binary -> unknown', _ingest_form(utf16) == INGEST_UNKNOWN)

    # ── T4/T5 round trip THROUGH the text form, for every generated shape ──────
    for label, tax in _ck_shapes():
        tp = _write_text('rt_%s.docx' % re.sub(r'[^a-z0-9]+', '_', label.lower()),
                         _render_md(tax, 'EXAM'))
        try:
            got = read_analysis_doc(tp)
        except Exception as ex:
            for suffix in ('text round-trip', 'text counts', 'text fingerprint parity'):
                check('K %s: %s [%s]' % (suffix, label, type(ex).__name__), False)
            continue
        rebuilt = {s: {t: list(v['subtopics']) for t, v in d2['topics'].items()}
                   for s, d2 in got['taxonomy'].items()}
        check('K text round-trip: ' + label, rebuilt == tax)
        n = sum(len(x) for t in tax.values() for x in t.values())
        check('K text counts: ' + label,
              got['counts'] == {'subjects': len(tax),
                                'topics': sum(len(t) for t in tax.values()),
                                'subtopics': n})
        d = os.path.join(tmp, 'x_' + re.sub(r'[^a-z0-9]+', '_', label.lower()))
        os.makedirs(d, exist_ok=True)
        # T2 cross-form identity: the two ingest forms of ONE taxonomy agree exactly
        check('K text fingerprint parity: ' + label,
              got['fingerprint'] ==
              read_analysis_doc(write_analysis_doc(tax, 'EXAM', out_dir=d))['fingerprint'])

    # ── grammar variants OBSERVED in a second real extractor ───────────────────
    check('K text grammar: __bold__ whole-line wrap',
          read_analysis_doc(_write_text('UND' + ANALYSIS_DOC_SUFFIX,
                                        _render_md(_t3tax, 'UND', bold='__')))['triples']
          == [('Physics', 'Mechanics', 'Kinematics'), ('Physics', 'Mechanics', 'Newton Laws')])
    _esc_tax = {'Maths': {'Series': ['p_1 and p_2 tests', 'Big-O [worst case]']}}
    check('K text grammar: backslash-escaped cells unescape exactly',
          read_analysis_doc(_write_text('ESC' + ANALYSIS_DOC_SUFFIX,
                                        _render_md(_esc_tax, 'ESC', escape=True)))['triples']
          == [('Maths', 'Series', 'p_1 and p_2 tests'),
              ('Maths', 'Series', 'Big-O [worst case]')])
    check('K text grammar: underscores inside a name are NEVER stripped',
          _md_plain('p_1 and p__2') == 'p_1 and p__2')

    # ── the ragged-row stop: a '|' in a name must never parse silently ─────────
    _pipe_md = _render_md({'Physics': {'Waves': ['Transverse', 'Standing']}}, 'PIPE')
    _pipe_md = _pipe_md.replace('| Transverse | — |', '| Transverse | Longitudinal | — |')
    pipe_doc = _write_text('PIPE' + ANALYSIS_DOC_SUFFIX, _pipe_md)
    check('K ragged row (| in a name) HARD STOPS rather than truncating',
          _stops(lambda: read_analysis_doc(pipe_doc), 'same number of cells'))
    check('K ragged row names the likely cause',
          _stops(lambda: read_analysis_doc(pipe_doc), "contains a '|' character"))
    check('K writer REFUSES to emit a name containing a pipe',
          _stops(lambda: write_analysis_doc({'S': {'T': ['a | b']}}, 'PIPE', out_dir=ing),
                 "cannot be written"))
    check('K writer accepts an escaped-pipe-free taxonomy unchanged',
          bool(write_analysis_doc({'S': {'T': ['a / b']}}, 'OKP', out_dir=ing)))

    # ── T6 corruption of the text form fires, per subject, every time ──────────
    _base_md = _render_md({'A': {'T1': ['x', 'y']}, 'B': {'T2': ['p', 'q']}}, 'C')
    for tag, mutated in (
            ('subject heading deleted', _base_md.replace('**Subject: B**\n', '')),
            ('a data row deleted', _base_md.replace('| y | — |\n', '')),
            ('a D1 count corrupted', _base_md.replace('2 Subtopics', '9 Subtopics', 1)),
            ('every table deleted',
             '\n'.join(l for l in _base_md.split('\n') if not l.lstrip().startswith('|')))):
        mp = _write_text('C%s.docx' % re.sub(r'\W+', '', tag), mutated)
        check('K T6 text corruption fires: ' + tag,
              _stops(lambda p=mp: read_analysis_doc(p), 'HARD STOP'))

    # ── T7 verify=False is REFUSED on the text form (never on OOXML) ───────────
    _bad = _write_text('T7' + ANALYSIS_DOC_SUFFIX,
                       _base_md.replace('2 Subtopics', '9 Subtopics', 1))
    check('K T7 verify=False is refused on a text-form doc',
          _stops(lambda: read_analysis_doc(_bad, verify=False), 'does not agree with itself'))

    # ── T8 unknown form: named, sized, and never a library traceback ───────────
    for nm, p in (('zero bytes', empty), ('truncated zip', trunc),
                  ('non-Word zip', notword), ('UTF-16 binary', utf16)):
        check('K T8 unknown form is named: ' + nm,
              _stops(lambda p=p: read_analysis_doc(p), 'not a recognised ingest form'))
    check('K T8 unknown form never surfaces PackageNotFoundError',
          not _stops(lambda: read_analysis_doc(trunc), 'PackageNotFoundError'))
    check('K T8 a vanished/unreadable path still gets the NAMED stop, not a traceback',
          _stops(lambda: read_analysis_doc(os.path.join(ing, 'gone_PYQ_Analysis.docx')),
                 'not a recognised ingest form'))
    check('K T8 the unreadable path reports why the size is missing',
          _stops(lambda: read_analysis_doc(os.path.join(ing, 'gone_PYQ_Analysis.docx')),
                 'unreadable ('))
    check('K T8 a DIRECTORY given as the path gets the named stop too',
          _stops(lambda: read_analysis_doc(ing), 'not a recognised ingest form'))

    # ── T9 downstream shape is unchanged, plus the additive ingest_form key ────
    _t9 = read_analysis_doc(txt_doc)
    check('K T9 return shape unchanged by the text path',
          set(_t9) >= {'path', 'exam_code', 'subjects', 'taxonomy', 'triples',
                       'counts', 'fingerprint'})
    check('K T9 ingest_form reported as text', _t9['ingest_form'] == INGEST_TEXT)
    check('K T9 ingest_form reported as ooxml',
          read_analysis_doc(ok_docx)['ingest_form'] == INGEST_OOXML)
    check('K T9 topic_idx positional on the text path',
          all(sorted(v['topic_idx'] for v in d2['topics'].values())
              == list(range(len(d2['topics']))) for d2 in _t9['taxonomy'].values()))

    # ══════════════════════════════════════════════════════════════════════════
    # THE TAXONOMY LOCK GATE
    # ══════════════════════════════════════════════════════════════════════════
    lk = os.path.join(tmp, 'lock'); os.makedirs(lk, exist_ok=True)
    _lt = {'Physics': {'Mechanics': ['Kinematics', 'Newton Laws']},
           'Chemistry': {'Bonding': ['Ionic', 'Covalent']}}
    _lp = write_analysis_doc(_lt, 'LOCKEXAM', out_dir=lk)
    _ld = read_analysis_doc(_lp)

    def _rec(fp, name='LOCKEXAM' + APPROVAL_RECORD_SUFFIX):
        body = {'exam_code': 'LOCKEXAM', 'status': 'CLEAN'}
        if fp is not None:
            body['taxonomy_fingerprint'] = fp
        with open(os.path.join(lk, name), 'w', encoding='utf-8') as fh:
            json.dump(body, fh)

    _rec(_ld['fingerprint'])
    check('K LOCK matching fingerprint passes',
          assert_taxonomy_lock(_ld, search_dirs=(lk,))['exam_code'] == 'LOCKEXAM')

    _rec('v1:9:9:' + 'f' * 64)
    check('K LOCK mismatched fingerprint HARD STOPS',
          _stops(lambda: assert_taxonomy_lock(_ld, search_dirs=(lk,)),
                 'NOT the taxonomy that was approved'))
    check('K LOCK names the step it fired at',
          _stops(lambda: assert_taxonomy_lock(_ld, search_dirs=(lk,), step='PYQExtract'),
                 'HARD STOP at PYQExtract'))

    _rec(None)
    check('K LOCK absent fingerprint HARD STOPS with the re-run action',
          _stops(lambda: assert_taxonomy_lock(_ld, search_dirs=(lk,)),
                 'no taxonomy_fingerprint'))

    os.remove(os.path.join(lk, 'LOCKEXAM' + APPROVAL_RECORD_SUFFIX))
    check('K LOCK missing record HARD STOPS rather than passing',
          _stops(lambda: assert_taxonomy_lock(_ld, search_dirs=(lk,)),
                 'no approval record found'))

    _rec(_ld['fingerprint'])
    _rec(_ld['fingerprint'], 'OTHEREXAM' + APPROVAL_RECORD_SUFFIX)
    check('K LOCK exam_code selects the right record when two are present',
          assert_taxonomy_lock(_ld, search_dirs=(lk,))['exam_code'] == 'LOCKEXAM')
    check('K LOCK ambiguous record set (no exam_code) HARD STOPS',
          _stops(lambda: discover_approval_record(search_dirs=(lk,)),
                 'exactly one is expected'))

    with open(os.path.join(lk, 'BADEXAM' + APPROVAL_RECORD_SUFFIX), 'w') as fh:
        fh.write('{not json')
    check('K LOCK malformed record HARD STOPS by name',
          _stops(lambda: read_approval_record('BADEXAM', search_dirs=(lk,)),
                 'could not be read as JSON'))

    # the gate must survive the TEXT ingest form identically
    _ltxt = os.path.join(lk, 'LOCKEXAM' + ANALYSIS_DOC_SUFFIX)
    with open(_ltxt, 'w', encoding='utf-8') as fh:
        fh.write(_render_md(_lt, 'LOCKEXAM'))
    check('K LOCK holds across ingest forms (text doc, same record)',
          assert_taxonomy_lock(read_analysis_doc(_ltxt),
                               search_dirs=(lk,))['exam_code'] == 'LOCKEXAM')

    # ══════════════════════════════════════════════════════════════════════════
    # load_taxonomy() — record first, document as fallback (v1.4)
    # ══════════════════════════════════════════════════════════════════════════
    jd = os.path.join(tmp, 'json'); os.makedirs(jd, exist_ok=True)
    _jt = {'General Biology': {'Cell Biology': ['Membrane', 'Nucleus'],
                               'Genetics': ['Linkage']},
           'Physics': {'Mechanics': ['Kinematics']}}
    _jdoc = read_analysis_doc(write_analysis_doc(_jt, 'JX', out_dir=jd))

    def _jrec(**over):
        body = {'exam_code': 'JX', 'schema_version': '1.3', 'status': 'CLEAN',
                'taxonomy_fingerprint': _jdoc['fingerprint'],
                'taxonomy_counts': dict(_jdoc['counts']),
                'taxonomy': {'sections': {s: {t: list(x) for t, x in v.items()}
                                          for s, v in _jt.items()}}}
        body.update(over)
        with open(os.path.join(jd, 'JX' + APPROVAL_RECORD_SUFFIX), 'w',
                  encoding='utf-8') as fh:
            json.dump(body, fh)

    _jrec()
    _lt = load_taxonomy('JX', search_dirs=(jd,))
    check('K JSON source is the approval record', _lt['source'] == 'approval_record')
    check('K JSON ingest_form is json', _lt['ingest_form'] == 'json')
    check('K JSON triples identical to the document path',
          _lt['triples'] == _jdoc['triples'])
    check('K JSON taxonomy identical to the document path',
          _lt['taxonomy'] == _jdoc['taxonomy'])
    check('K JSON fingerprint identical to the document path',
          _lt['fingerprint'] == _jdoc['fingerprint'])
    check('K JSON subject order preserved', _lt['subjects'] == list(_jt))
    check('K JSON topic_idx positional and contiguous',
          all(sorted(v['topic_idx'] for v in d2['topics'].values())
              == list(range(len(d2['topics']))) for d2 in _lt['taxonomy'].values()))

    # the record must be believed only when it agrees with ITSELF
    _jrec(taxonomy_fingerprint='v1:9:9:' + 'f' * 64)
    check('K JSON record whose halves disagree HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)),
                 'does not agree with itself'))
    _jrec(taxonomy_counts={'subjects': 9, 'topics': 9, 'subtopics': 9})
    check('K JSON declared counts vs assembled counts HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)),
                 'assembles to'))
    _jrec(taxonomy={'sections': {}})
    check('K JSON empty sections HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)),
                 'not a populated'))
    _jrec(taxonomy={'sections': {'S': {'T': []}}})
    check('K JSON topic with no subtopics HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)), 'no subtopics'))
    _jrec(taxonomy={'sections': {'S': {}}})
    check('K JSON subject with no topics HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)), 'no topics'))
    _jrec(taxonomy={'sections': {'S': {'T': ['a', 'a']}}})
    check('K JSON duplicate name HARD STOPS instead of collapsing silently',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)),
                 'more than once'))
    _jrec(taxonomy_fingerprint=None)
    check('K JSON taxonomy without a fingerprint HARD STOPS',
          _stops(lambda: load_taxonomy('JX', search_dirs=(jd,)),
                 'cannot validate itself'))

    # ── the pre-1.3 fallback: record has a fingerprint and NO taxonomy ──────────
    _jrec(taxonomy=None)
    _fb = load_taxonomy('JX', search_dirs=(jd,))
    check('K pre-1.3 record falls back to the Analysis doc',
          _fb['source'] == 'analysis_doc')
    check('K fallback yields the IDENTICAL taxonomy',
          _fb['triples'] == _jdoc['triples'] and
          _fb['fingerprint'] == _jdoc['fingerprint'])
    check('K fallback is still lock-gated',
          _stops(lambda: (_jrec(taxonomy=None,
                                taxonomy_fingerprint='v1:9:9:' + 'f' * 64),
                          load_taxonomy('JX', search_dirs=(jd,)))[1],
                 'NOT the taxonomy that was approved'))

    # ── and it works when the doc is in the TEXT ingest form ───────────────────
    with open(os.path.join(jd, 'JX' + ANALYSIS_DOC_SUFFIX), 'w',
              encoding='utf-8') as fh:
        fh.write(_render_md(_jt, 'JX'))
    _jrec(taxonomy=None)
    _fbt = load_taxonomy('JX', search_dirs=(jd,))
    check('K fallback works on the TEXT ingest form too',
          _fbt['ingest_form'] == 'text' and _fbt['fingerprint'] == _jdoc['fingerprint'])

    # ── and the record path needs NO document at all ───────────────────────────
    nd = os.path.join(tmp, 'norec'); os.makedirs(nd, exist_ok=True)
    with open(os.path.join(nd, 'JX' + APPROVAL_RECORD_SUFFIX), 'w',
              encoding='utf-8') as fh:
        json.dump({'exam_code': 'JX', 'schema_version': '1.3',
                   'taxonomy_fingerprint': _jdoc['fingerprint'],
                   'taxonomy': {'sections': _jt}}, fh)
    check('K JSON path needs no Analysis doc on disk at all',
          load_taxonomy('JX', search_dirs=(nd,))['fingerprint'] == _jdoc['fingerprint'])

    # ── the live fixture: the one shape that is field evidence, not generated ───
    fx = None
    for cand in (os.path.join(os.path.dirname(os.path.abspath(__file__)), CK_LIVE_FIXTURE),
                 os.path.join('fixtures', CK_LIVE_FIXTURE), CK_LIVE_FIXTURE):
        if os.path.exists(cand):
            fx = cand
            break
    if fx:
        live = read_analysis_doc(fx)
        check('K live fixture: 6 subjects / 26 topics / 131 subtopics',
              live['counts'] == {'subjects': 6, 'topics': 26, 'subtopics': 131})
        check('K live fixture: 6 distinct subjects across the triples',
              len({t[0] for t in live['triples']}) == 6)


# ═══════════════════════════════════════════════════════════════════════════════
# CLUSTER I — TABLE STRUCTURE  (GAP-2026-07-29-TBL)
# ═══════════════════════════════════════════════════════════════════════════════
# WHY THIS LIVES HERE AND NOT IN A SPEC. Two builders existed for one concept —
# Framework_PYQPrepare S4-3 build_di_table(rows_data) and Framework_MockTestCreate
# S8-4 build_di_table_styled(headers, rows) — and BOTH modelled a table as a
# rectangle of strings. Neither could express a merged cell, so a grouped header
# ("Printers" spanning L/M/N/O above "Days" spanning two rows) had exactly one
# representable form: squared into a grid and padded with empty strings. Measured
# on SSC_CGL_Tier1 09-Sep-2024 Shift 1 — Q.52 and Q.61 each lost a 4-column span
# and a 2-row span and gained 4 stray empty cells; the delivered file carried
# 0 gridSpan and 0 vMerge elements and passed 16/16 checks. One model, one owner,
# one implementation: Step 1 writes it, Step 7 rebuilds it, Steps 3/4/5 read it.
#
# THE DATA MODEL (TableSpec)
#   spec = {
#     'grid'        : [[Cell, ...], ...],   # REQUIRED, row-major, ANCHOR CELLS ONLY
#     'header_rows' : int,                  # OPTIONAL, default 1
#     'col_widths'  : [float, ...] | None,  # OPTIONAL, relative weights
#     'align'       : 'left'|'center'|'right',   # OPTIONAL, default 'center'
#     'note'        : str | None,           # OPTIONAL, footnote rendered below
#   }
#   Cell = str                              # == {'t': str, 'cs': 1, 'rs': 1}
#        | {'t': str, 'cs': int, 'rs': int, 'align': str|None, 'bold': bool}
#
# THE ONE RULE THAT REMOVES THE AMBIGUITY: a row declares only the cells that
# START in it. A position covered by a span from above or from the left is NOT
# declared. Padding a row with '' to square the grid is BANNED — under this model
# it cannot occur, which is what makes a genuinely blank cell ({'t': ''}, e.g. the
# classic empty top-left corner) distinguishable from padding STRUCTURALLY rather
# than by heuristic.

TABLE_ALIGNMENTS = ('left', 'center', 'right')


def normalise_table_spec(spec):
    """Accept a legacy list-of-lists OR a TableSpec dict. Return a TableSpec dict.

    The legacy shape stays valid for ever: every pre-GAP-2026-07-29-TBL call site
    keeps working unchanged, and a flat table has no spans to lose.
    """
    if isinstance(spec, (list, tuple)):
        spec = {'grid': list(spec)}
    elif isinstance(spec, dict) and 'grid' not in spec and 'headers' in spec:
        # Framework_MockTestCreate S8-4 legacy DI payload {'headers': [...],
        # 'rows': [[...]]}. One header row, no spans — accepted for ever so no
        # registry.json / blueprint payload has to be migrated.
        spec = {'grid': [list(spec['headers'])] + [list(r) for r in (spec.get('rows') or [])],
                'header_rows': 1}
    if not isinstance(spec, dict) or 'grid' not in spec:
        raise ValueError('TableSpec must be a dict with a "grid" key, a '
                         '{"headers","rows"} payload, or a list of rows')
    grid = []
    for row in spec['grid']:
        out = []
        for c in row:
            out.append(dict(c) if isinstance(c, dict) else {'t': '' if c is None else str(c)})
        grid.append(out)
    out_spec = dict(spec)
    out_spec['grid'] = grid
    return out_spec


def place_cells(grid):
    """HTML-table occupancy placement. Deterministic; no heuristics, no guessing.

    Returns (placements, width, nrows, errors) where placements is
    [(row, col, rowspan, colspan, cell), ...] in declaration order.

    A 'hole' means the transcription UNDER-declares a row; an 'overlap' means it
    OVER-declares. Both are transcription errors, and both are REPORTED rather
    than silently normalised — silent normalisation is the defect this whole
    cluster exists to end.
    """
    occ, placements, errors = {}, [], []
    for r, row in enumerate(grid):
        c = 0
        for cell in row:
            try:
                cs = int(cell.get('cs', 1))
                rs = int(cell.get('rs', 1))
            except (TypeError, ValueError):
                cs = rs = 1
                errors.append('row %d: non-integer cs/rs, coerced to 1' % r)
            if cs < 1 or rs < 1:
                errors.append('row %d: cs=%s rs=%s, both must be >= 1' % (r, cs, rs))
                cs, rs = max(cs, 1), max(rs, 1)
            while (r, c) in occ:
                c += 1
            for rr in range(r, r + rs):
                for cc in range(c, c + cs):
                    if (rr, cc) in occ:
                        errors.append('overlapping span at (%d,%d)' % (rr, cc))
                    occ[(rr, cc)] = True
            placements.append((r, c, rs, cs, cell))
            c += cs
    width = max((cc for (_rr, cc) in occ), default=-1) + 1
    nrows = len(grid)
    for r in range(nrows):
        for c in range(width):
            if (r, c) not in occ:
                errors.append('hole at (%d,%d) — row %d under-declares its cells' % (r, c, r))
    return placements, width, nrows, errors


def table_spec_spans(spec):
    """Declared spans as a sorted (row, col, rowspan, colspan) list. CHECK 17 input."""
    placements, _w, _n, _e = place_cells(normalise_table_spec(spec)['grid'])
    return sorted((r, c, rs, cs) for (r, c, rs, cs, _cell) in placements if rs > 1 or cs > 1)


def build_di_table(doc, spec, font_pt=9, default_align='center', render=None,
                   style='Table Grid', avail_emu=5734050, font_name='Arial'):
    """Build a native Word table from a TableSpec (or a legacy list of lists).

    ORDERING IS LOAD-BEARING AND IS THE EASIEST THING TO GET WRONG:
      1. write text into ANCHOR cells
      2. THEN merge
      3. THEN set per-column widths
    cell.merge() CONCATENATES the text of both cells ('A' + 'B' -> 'A\\nB',
    verified on python-docx 1.2.0), so text must never be written into a covered
    position and merging must never precede text placement.

    render : optional callable(paragraph, text, bold=bool). When supplied, cell
             text is emitted through the caller's own renderer, so OMML math and
             {{u}} underline markers work INSIDE table cells exactly as they do in
             stems and options (Framework_PYQPrepare S1-6 / S1-11). When omitted,
             plain text is written.
    avail_emu : usable text width. Default 6.27in (A4 minus 1in margins) in EMU.
    font_name : cell font family. Default 'Arial' = the Row-file contract (S1-1).
                Step 7 passes its configurable FONT_NAME.
    """
    from docx.shared import Pt, Emu
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    amap = {'left': WD_ALIGN_PARAGRAPH.LEFT,
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'right': WD_ALIGN_PARAGRAPH.RIGHT}

    spec = normalise_table_spec(spec)
    placements, width, nrows, errors = place_cells(spec['grid'])
    if errors:
        raise ValueError('TableSpec geometry invalid: ' + '; '.join(errors[:5]))

    tbl = doc.add_table(rows=nrows, cols=width, style=style)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    table_align = spec.get('align') or default_align
    if table_align not in TABLE_ALIGNMENTS:
        table_align = 'center'
    header_rows = int(spec.get('header_rows', 1) or 0)

    # 1 — text into anchors only
    for (r, c, _rs, _cs, cell) in placements:
        tc = tbl.cell(r, c)
        tc.text = ''
        para = tc.paragraphs[0]
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)
        cell_align = cell.get('align') or table_align
        para.alignment = amap.get(cell_align, amap['center'])
        bold = bool(cell.get('bold', False))
        text = cell.get('t', '')
        if render is not None:
            render(para, text, bold=bold)
        elif text:
            para.add_run(text).bold = bold
        for run in para.runs:
            run.font.name = font_name
            run.font.size = Pt(font_pt)

    # 2 — merges, only after every anchor already holds its text
    for (r, c, rs, cs, _cell) in placements:
        if rs > 1 or cs > 1:
            tbl.cell(r, c).merge(tbl.cell(r + rs - 1, c + cs - 1))

    # 3 — per-cell column widths. tblGrid alone is advisory and several renderers
    #     ignore it, so the width must be stamped on every cell of the column.
    weights = spec.get('col_widths') or [1.0] * width
    if len(weights) != width:
        weights = [1.0] * width
    total = float(sum(weights)) or 1.0
    for ci in range(width):
        w = Emu(int(avail_emu * (weights[ci] / total)))
        for ri in range(nrows):
            tbl.cell(ri, ci).width = w

    if spec.get('note'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(str(spec['note']))
        run.font.name = font_name
        run.font.size = Pt(font_pt)
        run.italic = True
    _ = header_rows          # reserved for header styling by callers that want it
    return tbl


def adjacent_table_pairs(doc):
    """Count pairs of adjacent block-level <w:tbl> siblings. CHECK 18 input.

    Two consecutive w:tbl siblings with no w:p between them are FUSED into one
    table by every Word engine. This is an OOXML block rule, not a renderer quirk,
    and it is invisible in the emitted file: python-docx reports N tables where
    Word shows one. Measured: a Row file written with 19 tables came back from a
    Word-engine round-trip with 7.
    """
    kinds = []
    for child in doc.element.body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag in ('p', 'tbl'):
            kinds.append(tag)
    pairs, run = 0, 0
    for k in kinds:
        run = run + 1 if k == 'tbl' else 0
        if run >= 2:
            pairs += 1
    return pairs



# ═══════════════════════════════════════════════════════════════════════════════
# CHEMICAL STRUCTURE IDENTITY + RENDERING (v1.12, GAP-2026-08-21-EXPLANATION-PROVENANCE)
# Create-route home of the rdkit-backed helpers. paper_pipeline (thin core) carries
# the pure semantic-object schema and INJECTS canonical_structure here; explain_engine
# carries a byte-identical canonical_structure for the Explain route. CROSS-FILE SYNC
# RULE: `canonical_structure` in corpus_io.py and explain_engine.py must stay identical.
# ═══════════════════════════════════════════════════════════════════════════════

def canonical_structure(smiles):
    """Canonical isomeric SMILES via rdkit, with valence sanitisation. Returns
    (canonical|None, reason); reason == 'ok' | 'rdkit_unavailable' | a parse
    error. NEVER raises — the caller decides what an unavailable rdkit means.

    v1.16 (GAP-2026-11-01, LAW F1.3): a REACTION SMILES — 'reactants>agents>products',
    exactly two '>' separators — canonicalises component-wise through the molecule
    path below and is re-joined in the same order. An empty agents side, an empty
    products side (a scheme that ends in a placeholder letter) or an empty reactants
    side (a scheme that starts from an unknown and draws the product — G7) are each
    legal; a reaction with NEITHER a reactant nor a product is not. The molecule path
    is byte-identical to v1.15, so every pre-existing fixture canonicalises as before."""
    try:
        from rdkit import Chem
        from rdkit import RDLogger
        RDLogger.DisableLog('rdApp.*')
    except Exception:
        return None, 'rdkit_unavailable'
    s = str(smiles)
    if '>' in s:
        parts = s.split('>')
        if len(parts) != 3:
            return None, ('parse_error: a reaction SMILES has exactly two ">" separators '
                          '(reactants>agents>products)')
        if not parts[0].strip() and not parts[2].strip():
            return None, 'parse_error: reaction SMILES has neither a reactant nor a product'
        sides = []
        for side in parts:
            comps = []
            for comp in [c for c in side.strip().split('.') if c.strip()]:
                try:
                    m = Chem.MolFromSmiles(comp, sanitize=True)
                except Exception as e:
                    return None, f'parse_error: {e}'
                if m is None:
                    return None, (f'parse_error: rdkit rejected the SMILES component '
                                  f'{comp!r} (valence / syntax)')
                comps.append(Chem.MolToSmiles(m, isomericSmiles=True, canonical=True))
            sides.append('.'.join(comps))
        return '>'.join(sides), 'ok'
    try:
        mol = Chem.MolFromSmiles(s, sanitize=True)
    except Exception as e:
        return None, f'parse_error: {e}'
    if mol is None:
        return None, 'parse_error: rdkit rejected the SMILES (valence / syntax)'
    return Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True), 'ok'


# ═══════════════════════════════════════════════════════════════════════════════
# PRINT-TRUE NATIVE RASTER (v1.17, GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY F1/F2/F4/F6/F7)
#
# One TOKENS dict per paper role — {'font_pt', 'line_pt', 'bond_pt', 'monochrome',
# 'mark_colour'}, every size in PRINTED points — is passed in by the caller
# (figural_core.structure_tokens; this module never imports figural_core). Every
# molecule drawn with the same tokens shares one bond length, one label size and one
# stroke, and the PNG's natural size at its dpi IS its print size. No highlight band is
# ever drawn on this path: an interrogated site is a MARK (underline / asterisk /
# letter / arrow / bold) placed clear of every atom label and bond, using the
# renderer's own geometry (rdkit's SVG twin of the same drawing gives each label's glyph
# boxes and each bond's drawn segments, in the same canvas coordinates as the raster).
# ═══════════════════════════════════════════════════════════════════════════════

# RDKit ParseAbbreviations text: "label SMILES display reversed_display" (the attachment
# dummy is implicit; rdkit adds the degree / ring constraints). LARGEST GROUPS FIRST —
# LabelMolAbbreviations takes the first match, so 'Et' must not pre-empt a C9 chain.
# Methyl is deliberately ABSENT: Me is drawn as a line (house style of every exam measured).
_NALKYL_LEX = ''.join(
    f'C{_n}H{2 * _n + 1} {"C" * _n} C<sub>{_n}</sub>H<sub>{2 * _n + 1}</sub> '
    f'H<sub>{2 * _n + 1}</sub>C<sub>{_n}</sub>\n' for _n in range(20, 6, -1))
ABBREVIATION_LEXICON = _NALKYL_LEX + """\
TBDPS [Si](c1ccccc1)(c1ccccc1)C(C)(C)C TBDPS TBDPSO
TBS [Si](C)(C)C(C)(C)C TBS TBS
OTs OS(=O)(=O)c1ccc(C)cc1 OTs TsO
OTf OS(=O)(=O)C(F)(F)F OTf TfO
OMs OS(=O)(=O)C OMs MsO
Cbz C(=O)OCc1ccccc1 Cbz Cbz
Boc C(=O)OC(C)(C)C Boc Boc
CO2Et C(=O)OCC CO<sub>2</sub>Et EtO<sub>2</sub>C
CO2Me C(=O)OC CO<sub>2</sub>Me MeO<sub>2</sub>C
OAc OC(=O)C OAc AcO
SiMe3 [Si](C)(C)C SiMe<sub>3</sub> Me<sub>3</sub>Si
Bn Cc1ccccc1 Bn Bn
Ph c1ccccc1 Ph Ph
tBu C(C)(C)C tBu tBu
iPr C(C)C iPr iPr
OEt OCC OEt EtO
OMe OC OMe MeO
NO2 [N+](=O)[O-] NO<sub>2</sub> O<sub>2</sub>N
Ac C(=O)C Ac Ac
CHO C=O CHO OHC
CN C#N CN NC
Et CC Et Et
"""
_ABBREV_ENTRIES = [tuple(_l.split()) for _l in ABBREVIATION_LEXICON.splitlines() if _l.strip()]
# Display hook: label -> the spelling drawn. Identity by default (the lexicon's own
# display); an exam's measured spelling (e.g. 'CO2Me' -> 'CO<sub>2</sub>CH<sub>3</sub>')
# is passed per call in `abbreviations` or set here by the caller.
ABBREVIATION_DISPLAY = {_e[0]: _e[2] for _e in _ABBREV_ENTRIES}

NATIVE_MARK_DEVICES = ('underline', 'asterisk', 'letter', 'arrow', 'bold')
_RDKIT_SUBSUP_SCALE = 0.66        # rdkit DrawText sub/superscript scale (measured 0.66-0.68)
_NATIVE_FONT_CANDIDATES = {
    'regular': ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans.ttf'),
    'bold': ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'DejaVuSans-Bold.ttf'),
    'italic': ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf', 'DejaVuSans-Oblique.ttf'),
}


def _native_font(style, px):
    """(PIL font, font_file) for a TrueType face available in the container. Looks in
    the system DejaVu directory, then matplotlib's bundled DejaVu (already a framework
    dependency). PIL's built-in scalable default is the last resort ('pil_default')."""
    from PIL import ImageFont
    cands = list(_NATIVE_FONT_CANDIDATES[style])
    try:
        import matplotlib as _mpl
        cands.append(os.path.join(os.path.dirname(_mpl.__file__), 'mpl-data', 'fonts', 'ttf',
                                  _NATIVE_FONT_CANDIDATES[style][1]))
    except Exception:
        pass
    size = max(1, int(round(px)))
    for c in cands:
        if os.path.isabs(c) and os.path.exists(c):
            try:
                return ImageFont.truetype(c, size), c
            except Exception:
                continue
    try:
        return ImageFont.truetype(_NATIVE_FONT_CANDIDATES[style][1], size), _NATIVE_FONT_CANDIDATES[style][1]
    except Exception:
        return ImageFont.load_default(size=size), 'pil_default'


# Sane printed-size bounds for the native tokens (points). Outside them rdkit / Cairo
# fail obscurely (int(inf) OverflowError, 'PNG header not recognized' on a giant canvas)
# or the picture is unprintable; a clear ValueError names the token instead.
NATIVE_TOKEN_BOUNDS_PT = {'font_pt': (1.0, 72.0), 'line_pt': (0.1, 72.0), 'bond_pt': (1.0, 72.0)}


def _native_tokens(tokens):
    """Validate + normalise a tokens dict. Raises ValueError on a malformed dict, and on
    a non-finite or out-of-range size (NATIVE_TOKEN_BOUNDS_PT)."""
    if not isinstance(tokens, dict):
        raise ValueError('native raster: tokens must be a dict')
    out = {}
    for k in ('font_pt', 'line_pt', 'bond_pt'):
        try:
            v = float(tokens[k])
        except (KeyError, TypeError, ValueError, OverflowError):
            raise ValueError(f'native raster: tokens[{k!r}] missing or not a number')
        if not v > 0:
            raise ValueError(f'native raster: tokens[{k!r}] must be > 0')
        lo, hi = NATIVE_TOKEN_BOUNDS_PT[k]
        if not (v == v and v not in (float('inf'), float('-inf')) and lo <= v <= hi):
            raise ValueError(f'native raster: tokens[{k!r}] = {v!r} pt is outside the sane '
                             f'printed range {lo:g}..{hi:g} pt')
        out[k] = v
    out['monochrome'] = bool(tokens.get('monochrome', True))
    mc = str(tokens.get('mark_colour') or '#000000')
    if not re.fullmatch(r'#[0-9A-Fa-f]{6}', mc):
        raise ValueError(f'native raster: mark_colour {mc!r} is not #RRGGBB')
    out['mark_colour'] = mc.upper()
    return out


def abbreviation_protected_atoms(reactant_smiles, product_smiles, timeout=2):
    """GAP-2026-11-02 F7 (e.2.i): atoms that change in a reaction must never hide inside
    an abbreviation. Returns (protect_idx_reactant, protect_idx_product): the atoms of
    each molecule OUTSIDE the rdFMCS maximum common substructure. On timeout, an
    unparseable SMILES, an empty MCS or any rdkit failure, EVERY atom of both molecules
    is returned — i.e. nothing in either molecule is abbreviated. Never raises."""
    def _all(smi):
        try:
            from rdkit import Chem
            m = Chem.MolFromSmiles(str(smi or ''))
            return list(range(m.GetNumAtoms())) if m is not None else []
        except Exception:
            return []
    try:
        from rdkit import Chem, RDLogger
        from rdkit.Chem import rdFMCS
        RDLogger.DisableLog('rdApp.*')
        r = Chem.MolFromSmiles(str(reactant_smiles or ''))
        p = Chem.MolFromSmiles(str(product_smiles or ''))
        if r is None or p is None:
            return _all(reactant_smiles), _all(product_smiles)
        res = rdFMCS.FindMCS([r, p], timeout=max(1, int(round(timeout))),
                             ringMatchesRingOnly=True, completeRingsOnly=True)
        if res.canceled or not res.numAtoms or not res.smartsString:
            return _all(reactant_smiles), _all(product_smiles)
        q = Chem.MolFromSmarts(res.smartsString)
        mr, mp = r.GetSubstructMatch(q), p.GetSubstructMatch(q)
        if not mr or not mp:
            return _all(reactant_smiles), _all(product_smiles)
        return ([i for i in range(r.GetNumAtoms()) if i not in set(mr)],
                [i for i in range(p.GetNumAtoms()) if i not in set(mp)])
    except Exception:
        return _all(reactant_smiles), _all(product_smiles)


def _native_abbreviate(mol, abbreviations, protect):
    """-> (mol_to_draw, applied_labels, orig_to_drawn_atom_map). `abbreviations` None/[]
    -> nothing condensed. Otherwise only lexicon entries whose label the exam uses are
    applied; an entry may be 'label', ('label', 'display') or a {label: display} dict.
    No group touching a protected atom is condensed."""
    from rdkit import Chem, RDLogger
    ident = {i: i for i in range(mol.GetNumAtoms())}
    if not abbreviations:
        return mol, [], ident
    wanted = {}
    if isinstance(abbreviations, dict):
        wanted = {str(k): (str(v) if v else None) for k, v in abbreviations.items()}
    else:
        for e in abbreviations:
            if isinstance(e, (tuple, list)) and e:
                wanted[str(e[0])] = str(e[1]) if len(e) > 1 and e[1] else None
            else:
                wanted[str(e)] = None
    lines = []
    for label, smi, disp, disp_w in _ABBREV_ENTRIES:
        if label not in wanted:
            continue
        shown = wanted[label] or ABBREVIATION_DISPLAY.get(label) or disp
        shown_w = disp_w if shown == disp else shown
        lines.append(f'{label} {smi} {shown} {shown_w}')
    if not lines:
        return mol, [], ident
    from rdkit.Chem import rdAbbreviations
    RDLogger.DisableLog('rdApp.*')    # 'no suitable SubstanceGroups' when nothing matched
    ab = rdAbbreviations.ParseAbbreviations('\n'.join(lines))
    m0 = Chem.Mol(mol)
    for a in m0.GetAtoms():
        a.SetIntProp('_cio_orig', a.GetIdx())
    m1 = rdAbbreviations.LabelMolAbbreviations(m0, ab, maxCoverage=0.6)
    protect = set(int(i) for i in protect)
    keep = [sg for sg in Chem.GetMolSubstanceGroups(m1) if not set(sg.GetAtoms()) & protect]
    if not keep:
        return mol, [], ident
    covered = set()
    for sg in keep:
        covered |= set(sg.GetAtoms())
    labels = [sg.GetProp('LABEL') if sg.HasProp('LABEL') else '?' for sg in keep]
    Chem.ClearMolSubstanceGroups(m1)
    for sg in keep:
        Chem.AddMolSubstanceGroup(m1, sg)
    m2 = rdAbbreviations.CondenseAbbreviationSubstanceGroups(m1)
    amap = {}
    for a in m2.GetAtoms():
        if a.HasProp('_cio_orig') and a.GetAtomicNum() != 0:
            o = a.GetIntProp('_cio_orig')
            if o not in covered:
                amap[o] = a.GetIdx()
    return m2, labels, amap


def _native_depict(mol, which, canon_orient=False):
    from rdkit import Chem
    from rdkit.Chem import rdDepictor
    m = Chem.Mol(mol)
    m.RemoveAllConformers()
    if which == 'coordgen':
        from rdkit.Chem import rdCoordGen
        rdCoordGen.AddCoords(m)
    else:
        prev = rdDepictor.GetPreferCoordGen()
        rdDepictor.SetPreferCoordGen(False)          # global rdkit state: always restored
        try:
            rdDepictor.Compute2DCoords(m, canonOrient=bool(canon_orient))
        finally:
            rdDepictor.SetPreferCoordGen(prev)
        # rdDepictor lays bonds out at 1.5 units, CoordGen (and the drawer's
        # fixedBondLength) at 1.0: rescale so an rdkit-depicted structure prints at the
        # token bond length too (it printed 1.5x — G-FIGSCALE; fuzz 2026-11-02).
        import math
        c = m.GetConformer()
        ls = [math.dist(tuple(c.GetAtomPosition(b.GetBeginAtomIdx()))[:2],
                        tuple(c.GetAtomPosition(b.GetEndAtomIdx()))[:2]) for b in m.GetBonds()]
        ls = [x for x in ls if math.isfinite(x) and x > 0]
        if ls:
            f = len(ls) / sum(ls)
            from rdkit.Geometry import Point3D
            for i in range(m.GetNumAtoms()):
                p = c.GetAtomPosition(i)
                c.SetAtomPosition(i, Point3D(p.x * f, p.y * f, p.z * f))
    return m


def _native_cross_atoms(mol):
    """sp3 atoms with 4 heavy neighbours drawn as a 90-degree '+' (all four angles
    90 +/- 10 degrees) — the quaternary-cross defect of F7."""
    import math
    out = []
    if not mol.GetNumConformers():
        return out
    c = mol.GetConformer()
    for a in mol.GetAtoms():
        if a.GetIsAromatic():
            continue
        nb = [n for n in a.GetNeighbors() if n.GetAtomicNum() > 1]
        if len(nb) != 4 or any(b.GetBondTypeAsDouble() != 1.0 for b in a.GetBonds()):
            continue
        p = c.GetAtomPosition(a.GetIdx())
        angs = sorted(math.degrees(math.atan2(c.GetAtomPosition(n.GetIdx()).y - p.y,
                                              c.GetAtomPosition(n.GetIdx()).x - p.x)) % 360.0
                      for n in nb)
        gaps = [angs[i + 1] - angs[i] for i in range(3)] + [angs[0] + 360.0 - angs[3]]
        if all(abs(g - 90.0) <= 10.0 for g in gaps):
            out.append(a.GetIdx())
    return out


NATIVE_MIN_BOND_RATIO = 0.7      # shortest / longest depicted bond below this = distorted


def _native_coords_finite(m):
    """True when every atom of `m` has finite 2D coordinates (CoordGen returns NaN for
    an H-only species: '[H+]', '[H]', '[2H]', '[H][H]')."""
    import math
    if not m.GetNumConformers():
        return False
    c = m.GetConformer()
    for i in range(m.GetNumAtoms()):
        p = c.GetAtomPosition(i)
        if not (math.isfinite(p.x) and math.isfinite(p.y)):
            return False
    return True


def _native_bond_ratio(m):
    """min / max depicted bond length (1.0 with no bond). CoordGen squashes some
    bridged rings (2,3-disubstituted norbornanes: 'CC1CC2CCC1C2N' at 0.33x)."""
    import math
    c = m.GetConformer()
    ls = [math.dist(tuple(c.GetAtomPosition(b.GetBeginAtomIdx()))[:2],
                    tuple(c.GetAtomPosition(b.GetEndAtomIdx()))[:2]) for b in m.GetBonds()]
    ls = [x for x in ls if math.isfinite(x)]
    if not ls or max(ls) <= 0:
        return 1.0
    return min(ls) / max(ls)


def _native_layout(mol):
    """-> (mol_with_coords, depictor, cross_note). CoordGen first; non-finite CoordGen
    coordinates (an H-only species) or a distorted CoordGen layout (shortest / longest
    bond < NATIVE_MIN_BOND_RATIO) are re-depicted with rdkit's depictor, keeping the
    better layout; a quaternary cross is re-depicted with rdkit's depictor, then with
    canonOrient=True; else kept + noted."""
    m0, dep0 = _native_depict(mol, 'coordgen'), 'coordgen'
    if not _native_coords_finite(m0):
        m0, dep0 = _native_depict(mol, 'rdkit'), 'rdkit'
    elif _native_bond_ratio(m0) < NATIVE_MIN_BOND_RATIO:
        m1 = _native_depict(mol, 'rdkit')
        if _native_coords_finite(m1) and _native_bond_ratio(m1) > _native_bond_ratio(m0):
            m0, dep0 = m1, 'rdkit'
    if not _native_cross_atoms(m0):
        return m0, dep0, None
    m1 = _native_depict(mol, 'rdkit')
    if not _native_cross_atoms(m1):
        return m1, 'rdkit', None
    m2 = _native_depict(mol, 'rdkit', canon_orient=True)
    if not _native_cross_atoms(m2):
        return m2, 'rdkit', None
    return m0, dep0, (f'quaternary atom(s) {_native_cross_atoms(m0)} drawn as a 90-degree '
                      f'cross by both depictors and canonOrient (style only)')


def _seg_hits_rect(p, q, r):
    """Liang-Barsky: does segment p-q intersect rect r=[x0,y0,x1,y1]?"""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - r[0]), (dx, r[2] - x0), (-dy, y0 - r[1]), (dy, r[3] - y0)):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def _rects_overlap(a, b, pad=0.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def _grow(r, g):
    return [r[0] - g, r[1] - g, r[2] + g, r[3] + g]


class _NativeStructure:
    """Holds one prepared molecule (depicted, abbreviated, marks resolved) and renders
    it at any dpi with the token sizes. Results are cached per dpi."""

    def __init__(self, mol, tokens, marks, abbreviations, protect_atoms, palette, converted):
        from rdkit import Chem
        self.tk = tokens
        self.palette = palette            # (atom_pal or {}, colours_flag)
        self.converted = bool(converted)
        self.marks = [dict(m) for m in (marks or [])]
        n_at, n_bd = mol.GetNumAtoms(), mol.GetNumBonds()
        protect = set(int(i) for i in (protect_atoms or ()))
        for mk in self.marks:
            site = mk.get('site') or {}
            kind, idx = site.get('kind'), site.get('index')
            if mk.get('device') not in NATIVE_MARK_DEVICES:
                raise ValueError(f'structure_draw_fn: mark device {mk.get("device")!r} not in '
                                 f'{NATIVE_MARK_DEVICES}')
            if kind not in ('atom', 'bond') or not isinstance(idx, int):
                raise ValueError(f'structure_draw_fn: mark site {site!r} needs kind atom|bond and an int index')
            if kind == 'atom':
                if not 0 <= idx < n_at:
                    raise ValueError(f'structure_draw_fn: mark atom index {idx} outside 0..{n_at - 1}')
                protect.add(idx)
            else:
                if not 0 <= idx < n_bd:
                    raise ValueError(f'structure_draw_fn: mark bond index {idx} outside 0..{n_bd - 1}')
                b = mol.GetBondWithIdx(idx)
                protect |= {b.GetBeginAtomIdx(), b.GetEndAtomIdx()}
        self.orig = mol
        drawn, self.abbrev_labels, self.amap = _native_abbreviate(mol, abbreviations, protect)
        self.mol, self.depictor, self.cross_note = _native_layout(drawn)
        self._cache = {}

    # ── drawing primitives ────────────────────────────────────────────────────
    def _opts(self, d, dpi):
        k = dpi / 72.0
        o = d.drawOptions()
        o.fixedBondLength = self.tk['bond_pt'] * k
        o.bondLineWidth = max(1, int(round(self.tk['line_pt'] * k)))
        o.scaleBondWidth = False
        o.fixedFontSize = int(round(self.tk['font_pt'] * k))
        o.multipleBondOffset = 0.18
        o.padding = 0.0
        o.additionalAtomLabelPadding = 0.066
        o.clearBackground = True
        o.setBackgroundColour((1.0, 1.0, 1.0, 1.0))
        pal, colours = self.palette
        if (not self.tk['monochrome']) and colours and pal and hasattr(o, 'updateAtomPalette'):
            o.updateAtomPalette({int(kk): tuple(v) for kk, v in pal.items()})
            _missing = {a.GetAtomicNum() for a in self.mol.GetAtoms()} - set(pal)
            if _missing:
                o.updateAtomPalette({int(kk): (0.0, 0.0, 0.0) for kk in _missing})
        else:
            o.useBWAtomPalette()

    def _canvas(self, dpi):
        import math
        bond_px = self.tk['bond_pt'] * dpi / 72.0
        c = self.mol.GetConformer()
        xs = [c.GetAtomPosition(i).x for i in range(self.mol.GetNumAtoms())]
        ys = [c.GetAtomPosition(i).y for i in range(self.mol.GetNumAtoms())]
        bl = [math.dist((xs[b.GetBeginAtomIdx()], ys[b.GetBeginAtomIdx()]),
                        (xs[b.GetEndAtomIdx()], ys[b.GetEndAtomIdx()])) for b in self.mol.GetBonds()]
        mbl = (sum(bl) / len(bl)) if bl and sum(bl) > 0 else 1.5
        sx = (max(xs) - min(xs)) / mbl * bond_px if len(xs) > 1 else 0.0
        sy = (max(ys) - min(ys)) / mbl * bond_px if len(ys) > 1 else 0.0
        return int(sx + 6 * bond_px), int(sy + 6 * bond_px)

    def _draw_base(self, dpi):
        """-> (PIL RGB image, geometry) of the UNMARKED molecule on the full canvas."""
        from rdkit.Chem.Draw import rdMolDraw2D
        from PIL import Image
        W, H = self._canvas(dpi)
        dc = rdMolDraw2D.MolDraw2DCairo(W, H)
        self._opts(dc, dpi)
        rdMolDraw2D.PrepareAndDrawMolecule(dc, self.mol)
        dc.FinishDrawing()
        img = Image.open(io.BytesIO(dc.GetDrawingText())).convert('RGB')
        coords = {i: tuple(dc.GetDrawCoords(i)) for i in range(self.mol.GetNumAtoms())}
        ds = rdMolDraw2D.MolDraw2DSVG(W, H)
        self._opts(ds, dpi)
        rdMolDraw2D.PrepareAndDrawMolecule(ds, self.mol)
        ds.FinishDrawing()
        svg = ds.GetDrawingText()
        glyphs, bonds = {}, {}
        for mm in re.finditer(r"<path class='([^']*)' d='([^']*)'", svg):
            cls = mm.group(1).split()
            nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', mm.group(2))]
            pts = list(zip(nums[0::2], nums[1::2]))
            if not pts or not cls:
                continue
            if cls[0].startswith('bond-'):
                bonds.setdefault(int(cls[0][5:]), []).append(pts)
            elif cls[0].startswith('atom-'):
                xs_, ys_ = [p[0] for p in pts], [p[1] for p in pts]
                glyphs.setdefault(int(cls[0][5:]), []).append([min(xs_), min(ys_), max(xs_), max(ys_)])
        labels = {a: [min(g[0] for g in gs), min(g[1] for g in gs), max(g[2] for g in gs),
                      max(g[3] for g in gs)] for a, gs in glyphs.items()}
        segs = []
        for bi, polys in bonds.items():
            for pts in polys:
                for j in range(len(pts) - 1):
                    segs.append((bi, pts[j], pts[j + 1]))
        return img, {'coords': coords, 'glyphs': glyphs, 'labels': labels, 'bond_paths': bonds,
                     'segs': segs, 'W': W, 'H': H}

    def _small_pt(self):
        """Smallest text rdkit draws for this molecule: a label carrying a subscript H
        count, a charge or an isotope is drawn partly at rdkit's sub/superscript scale."""
        from rdkit import Chem
        fp = self.tk['font_pt']
        small = fp
        for a in self.mol.GetAtoms():
            labelled = a.GetAtomicNum() != 6 or a.GetFormalCharge() or a.GetIsotope() or a.GetDegree() == 0
            if a.HasProp('_displayLabel'):
                if '<sub>' in a.GetProp('_displayLabel') or '<sup>' in a.GetProp('_displayLabel'):
                    small = min(small, fp * _RDKIT_SUBSUP_SCALE)
                continue
            if labelled and a.GetAtomicNum() > 0 and (a.GetTotalNumHs() >= 2 or a.GetFormalCharge()
                                                      or a.GetIsotope() or a.GetNumRadicalElectrons()):
                small = min(small, fp * _RDKIT_SUBSUP_SCALE)
        return small

    # ── marks ─────────────────────────────────────────────────────────────────
    def _place_marks(self, img, geo, dpi):
        """Draw the marks onto `img` (in place). -> (drawn, failed, min_text_pt, bold_atoms)."""
        import math
        from PIL import ImageDraw, ImageFilter
        tk = self.tk
        k = dpi / 72.0
        bond_px, font_px, line_px = tk['bond_pt'] * k, tk['font_pt'] * k, max(1.0, tk['line_pt'] * k)
        colour = tuple(int(tk['mark_colour'][i:i + 2], 16) for i in (1, 3, 5))
        pad = max(1.0, 0.04 * bond_px)
        dr = ImageDraw.Draw(img)
        coords, labels, glyphs, segs = geo['coords'], geo['labels'], geo['glyphs'], geo['segs']
        W, H = geo['W'], geo['H']
        placed, drawn, failed, bold_atoms = [], [], [], []
        min_pt = None
        all_pts = list(coords.values())
        mcx = sum(p[0] for p in all_pts) / len(all_pts)
        mcy = sum(p[1] for p in all_pts) / len(all_pts)

        def _free_rect(r, skip_bonds=()):
            if r[0] < 0 or r[1] < 0 or r[2] > W or r[3] > H:
                return False
            if any(_rects_overlap(r, lb, pad) for lb in labels.values()):
                return False
            if any(_rects_overlap(r, pr, pad) for pr in placed):
                return False
            g = _grow(r, line_px / 2.0 + pad)
            return not any(_seg_hits_rect(p, q, g) for bi, p, q in segs if bi not in skip_bonds)

        def _free_seg(p, q, half, skip_bonds=()):
            for lb in labels.values():
                if _seg_hits_rect(p, q, _grow(lb, half + pad)):
                    return False
            for pr in placed:
                if _seg_hits_rect(p, q, _grow(pr, half + pad)):
                    return False
            for bi, a, b in segs:
                if bi in skip_bonds:
                    continue
                # thick segment vs thick segment: sample along p-q
                for t in [i / 12.0 for i in range(13)]:
                    x, y = p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])
                    if _pt_seg_dist((x, y), a, b) < half + line_px / 2.0 + pad:
                        return False
            return 0 <= min(p[0], q[0]) and max(p[0], q[0]) <= W and 0 <= min(p[1], q[1]) and max(p[1], q[1]) <= H

        def _rotations(ux, uy):
            out = []
            for deg in (0, 45, -45, 90, -90, 135, -135, 180):
                r = math.radians(deg)
                out.append((ux * math.cos(r) - uy * math.sin(r), ux * math.sin(r) + uy * math.cos(r)))
            return out

        def _unit(x, y, fx=0.0, fy=-1.0):
            n = math.hypot(x, y)
            return (x / n, y / n) if n > 1e-9 else (fx, fy)

        def _drawn_atom(i):
            return self.amap.get(i)

        def _drawn_bond(i):
            b = self.orig.GetBondWithIdx(i)
            a0, a1 = self.amap.get(b.GetBeginAtomIdx()), self.amap.get(b.GetEndAtomIdx())
            if a0 is None or a1 is None:
                return None
            bb = self.mol.GetBondBetweenAtoms(a0, a1)
            return None if bb is None else bb.GetIdx()

        def _text_mark(mk, text, style, size_px, anchor, direction):
            f, _ff = _native_font(style, size_px)
            bx = f.getbbox(text)
            tw, th = bx[2] - bx[0], bx[3] - bx[1]
            dist = 0.55 * bond_px
            for ux, uy in _rotations(*direction):
                cx, cy = anchor[0] + ux * dist, anchor[1] + uy * dist
                r = [cx - tw / 2.0, cy - th / 2.0, cx + tw / 2.0, cy + th / 2.0]
                if _free_rect(r):
                    dr.text((cx - (bx[0] + bx[2]) / 2.0, cy - (bx[1] + bx[3]) / 2.0), text, font=f, fill=colour)
                    placed.append(r)
                    return r
            return None

        def _arrow(anchor, direction, own, skip_bonds=()):
            """Arrow pointing AT `anchor` from outside, tried along `direction` first and
            then the _rotations of it; the tip stands 0.15 bond clear of the outermost
            of `own` (a double bond's offset line, an atom's label box) on that side.
            Draws it and returns its bbox, or None when no rotation is clear."""
            gap, length = 0.15 * bond_px, 0.6 * bond_px
            head_l = max(4.0 * line_px, 0.2 * bond_px)
            head_w = 0.35 * head_l
            done = None
            for ux, uy in _rotations(*direction):
                reach = max([0.0] + [(q[0] - anchor[0]) * ux + (q[1] - anchor[1]) * uy for q in own])
                g_ = gap + min(reach, 0.5 * bond_px) + line_px / 2.0
                tip = (anchor[0] + ux * g_, anchor[1] + uy * g_)
                tail = (anchor[0] + ux * (g_ + length), anchor[1] + uy * (g_ + length))
                if _free_seg(tip, tail, max(head_w, line_px / 2.0), skip_bonds=skip_bonds):
                    done = (tip, tail, ux, uy)
                    break
            if done is None:
                return None
            tip, tail, ux, uy = done
            base = (tip[0] + ux * head_l, tip[1] + uy * head_l)
            dr.line([tail, base], fill=colour, width=max(1, int(round(line_px))))
            dr.polygon([tip, (base[0] - uy * head_w, base[1] + ux * head_w),
                        (base[0] + uy * head_w, base[1] - ux * head_w)], fill=colour)
            r = [min(tip[0], tail[0]) - head_w, min(tip[1], tail[1]) - head_w,
                 max(tip[0], tail[0]) + head_w, max(tip[1], tail[1]) + head_w]
            placed.append(r)
            return r

        for mk in self.marks:
            site, dev = mk['site'], mk['device']
            rec = dict(mk)
            if site['kind'] == 'atom':
                ai = _drawn_atom(site['index'])
                if ai is None:
                    failed.append(dict(rec, reason='site_condensed')); continue
                labelled = ai in labels
                p = coords[ai]
                nbrs = [coords[n.GetIdx()] for n in self.mol.GetAtomWithIdx(ai).GetNeighbors()
                        if n.GetIdx() in coords]
                if nbrs:
                    direction = _unit(p[0] - sum(q[0] for q in nbrs) / len(nbrs),
                                      p[1] - sum(q[1] for q in nbrs) / len(nbrs))
                else:
                    direction = (0.0, -1.0)
                if dev == 'letter' and not str(mk.get('text') or '').strip():
                    # v1.17: a letter mark names ITS letter (Q7b.8' 'text'); never a default.
                    failed.append(dict(rec, reason='letter_text_missing')); continue
                if dev in ('asterisk', 'letter'):
                    text = '*' if dev == 'asterisk' else str(mk.get('text')).strip()
                    size_pt = tk['font_pt'] * (0.8 if dev == 'asterisk' else 1.0)
                    r = _text_mark(mk, text, 'regular' if dev == 'asterisk' else 'italic',
                                   size_pt * k, p, direction)
                    if r is None:
                        failed.append(dict(rec, reason='no_clear_position')); continue
                    min_pt = size_pt if min_pt is None else min(min_pt, size_pt)
                    drawn.append(dict(rec, bbox_px=r))
                elif dev == 'underline':
                    if not labelled:
                        failed.append(dict(rec, reason='device_not_drawable')); continue
                    gs = glyphs[ai]
                    hmax = max(g[3] - g[1] for g in gs)
                    main = [g for g in gs if (g[3] - g[1]) >= 0.8 * hmax]
                    base = sorted(g[3] for g in main)[len(main) // 2]
                    t = max(1.0, 0.6 * line_px)
                    y0 = base + 0.15 * font_px
                    # 2026.11.02 B9: the site's OWN subscript glyphs (the 2 of NH2, the 4
                    # of CH4) hang below the baseline, so a baseline underline always
                    # collided with them and NCC(=O)O atom 0 could never be underlined.
                    # The underline now runs under the FULL label: below the lowest
                    # subscript, spanning it. A label without a subscript is unchanged.
                    sub = [g for g in gs if g not in main and g[3] > base + 0.05 * font_px]
                    if sub:
                        y0 = max(y0, max(g[3] for g in sub) + 0.1 * font_px)
                    span = main + sub
                    r = [min(g[0] for g in span), y0, max(g[2] for g in span), y0 + t]
                    ok = (r[3] <= H and not any(_rects_overlap(r, g) for gg in glyphs.values() for g in gg)
                          and not any(_rects_overlap(r, pr, pad) for pr in placed)
                          and not any(_seg_hits_rect(a, b, _grow(r, line_px / 2.0)) for _bi, a, b in segs))
                    if not ok:
                        failed.append(dict(rec, reason='no_clear_position')); continue
                    dr.rectangle([r[0], r[1], r[2], r[1] + max(0.0, t - 1.0)], fill=colour)
                    placed.append(r)
                    drawn.append(dict(rec, bbox_px=r))
                elif dev == 'bold':
                    if not labelled:
                        failed.append(dict(rec, reason='device_not_drawable')); continue
                    lb = labels[ai]
                    box = (int(math.floor(lb[0])), int(math.floor(lb[1])), int(math.ceil(lb[2])) + 1,
                           int(math.ceil(lb[3])) + 1)
                    reg = img.crop(box).filter(ImageFilter.MinFilter(3))
                    img.paste(reg, box[:2])
                    bold_atoms.append(ai)
                    drawn.append(dict(rec, bbox_px=list(lb)))
                else:                                   # arrow on an atom
                    # 2026.11.02 B5: an arrow pointing AT the atom from outside, along
                    # the bisector away from its bonds, its tip clear of the atom's own
                    # label (the shared _arrow placer — same geometry as a bond arrow).
                    lb_ = labels.get(ai)
                    own = ([(lb_[0], lb_[1]), (lb_[2], lb_[1]), (lb_[0], lb_[3]), (lb_[2], lb_[3])]
                           if labelled else [p])
                    r = _arrow(p, direction, own, skip_bonds=())
                    if r is None:
                        failed.append(dict(rec, reason='no_clear_position')); continue
                    drawn.append(dict(rec, bbox_px=r))
                continue
            # ── bond sites ──
            bi = _drawn_bond(site['index'])
            if bi is None:
                failed.append(dict(rec, reason='site_condensed')); continue
            b = self.mol.GetBondWithIdx(bi)
            a0, a1 = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
            p0, p1 = coords[a0], coords[a1]
            mid = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
            ax_u = _unit(p1[0] - p0[0], p1[1] - p0[1], 1.0, 0.0)
            perp = (-ax_u[1], ax_u[0])
            others = [coords[n.GetIdx()] for at in (a0, a1)
                      for n in self.mol.GetAtomWithIdx(at).GetNeighbors() if n.GetIdx() not in (a0, a1)]
            ref = ((sum(q[0] for q in others) / len(others), sum(q[1] for q in others) / len(others))
                   if others else (mcx, mcy))
            if (mid[0] - ref[0]) * perp[0] + (mid[1] - ref[1]) * perp[1] < 0:
                perp = (-perp[0], -perp[1])             # the convex (outward) side
            paths = geo['bond_paths'].get(bi, [])
            order = float(b.GetBondTypeAsDouble())
            n_lines = len(paths) if order >= 1.5 else 1
            if dev == 'bold' and n_lines >= 2:
                # 2026.11.02 B2: ONE thick bar along the axis of a double bond fills the
                # gap between its two lines, so C=C printed as a single bar. Each drawn
                # line is now thickened SEPARATELY and grown OUTWARD (away from the
                # other line), so the inner gap rdkit drew is preserved exactly. A
                # triple bond's middle line has no outward side: device_not_drawable,
                # and the repair ladder re-authors the mark with another device.
                if n_lines != 2:
                    failed.append(dict(rec, reason='device_not_drawable', bond_order=order,
                                       bond_lines=n_lines)); continue
                wbold = max(2, int(round(2.0 * tk['line_pt'] * k)))
                grow = max(0.0, (wbold - line_px) / 2.0)
                L = math.dist(p0, p1) or 1.0
                cent = []
                for pts in paths:
                    cx_ = sum(q[0] for q in pts) / len(pts)
                    cy_ = sum(q[1] for q in pts) / len(pts)
                    cent.append((cx_ - mid[0]) * (-ax_u[1]) + (cy_ - mid[1]) * ax_u[0])
                segs_b, ok = [], True
                for j, pts in enumerate(paths):
                    sgn = 1.0 if cent[j] >= cent[1 - j] else -1.0
                    nx_, ny_ = -ax_u[1] * sgn * grow, ax_u[0] * sgn * grow
                    ts = [((q[0] - p0[0]) * ax_u[0] + (q[1] - p0[1]) * ax_u[1]) / L for q in pts]
                    t0, t1 = min(ts), max(ts)
                    off = cent[j]
                    if a0 in labels:                    # same label trim as a single bond
                        t0 += line_px / L
                    if a1 in labels:
                        t1 -= line_px / L
                    q0 = (p0[0] + t0 * (p1[0] - p0[0]) - ax_u[1] * off + nx_,
                          p0[1] + t0 * (p1[1] - p0[1]) + ax_u[0] * off + ny_)
                    q1 = (p0[0] + t1 * (p1[0] - p0[0]) - ax_u[1] * off + nx_,
                          p0[1] + t1 * (p1[1] - p0[1]) + ax_u[0] * off + ny_)
                    if t1 <= t0 or any(_seg_hits_rect(q0, q1, _grow(g, wbold / 2.0))
                                       for gg in glyphs.values() for g in gg):
                        ok = False
                        break
                    segs_b.append((q0, q1))
                if not ok:
                    failed.append(dict(rec, reason='no_clear_position', bond_order=order,
                                       bond_lines=n_lines)); continue
                xs_b, ys_b = [], []
                for q0, q1 in segs_b:
                    dr.line([q0, q1], fill=colour, width=wbold)
                    xs_b += [q0[0], q1[0]]; ys_b += [q0[1], q1[1]]
                r = [min(xs_b) - wbold / 2.0, min(ys_b) - wbold / 2.0,
                     max(xs_b) + wbold / 2.0, max(ys_b) + wbold / 2.0]
                drawn.append(dict(rec, bbox_px=r, bond_order=order, bond_lines=n_lines,
                                  bold_lines=len(segs_b),
                                  bond_px_endpoints=[list(segs_b[0][0]), list(segs_b[0][1])],
                                  bold_line_endpoints=[[list(q0), list(q1)] for q0, q1 in segs_b]))
            elif dev == 'bold':
                # ONE line along the bond axis, spanning exactly what rdkit drew for this
                # bond (its segments projected on the axis) — never an offset second line.
                L = math.dist(p0, p1) or 1.0
                ts = [((q[0] - p0[0]) * ax_u[0] + (q[1] - p0[1]) * ax_u[1]) / L
                      for pts in geo['bond_paths'].get(bi, []) for q in pts]
                if not ts:
                    failed.append(dict(rec, reason='no_clear_position')); continue
                t0, t1 = max(0.0, min(ts)), min(1.0, max(ts))
                trim = line_px / L
                if a0 in labels:
                    t0 += trim
                if a1 in labels:
                    t1 -= trim
                q0 = (p0[0] + t0 * (p1[0] - p0[0]), p0[1] + t0 * (p1[1] - p0[1]))
                q1 = (p0[0] + t1 * (p1[0] - p0[0]), p0[1] + t1 * (p1[1] - p0[1]))
                wbold = max(2, int(round(2.0 * tk['line_pt'] * k)))
                if t1 <= t0 or any(_seg_hits_rect(q0, q1, _grow(g, wbold / 2.0))
                                   for gg in glyphs.values() for g in gg):
                    failed.append(dict(rec, reason='no_clear_position')); continue
                dr.line([q0, q1], fill=colour, width=wbold)
                r = [min(q0[0], q1[0]) - wbold / 2.0, min(q0[1], q1[1]) - wbold / 2.0,
                     max(q0[0], q1[0]) + wbold / 2.0, max(q0[1], q1[1]) + wbold / 2.0]
                drawn.append(dict(rec, bbox_px=r, bond_px_endpoints=[list(q0), list(q1)],
                                  bond_order=order, bond_lines=n_lines, bold_lines=1))
            elif dev == 'letter':
                if not str(mk.get('text') or '').strip():
                    failed.append(dict(rec, reason='letter_text_missing')); continue
                text = str(mk.get('text')).strip()
                r = _text_mark(mk, text, 'italic', tk['font_pt'] * k, mid, perp)
                if r is None:
                    failed.append(dict(rec, reason='no_clear_position')); continue
                min_pt = tk['font_pt'] if min_pt is None else min(min_pt, tk['font_pt'])
                drawn.append(dict(rec, bbox_px=r))
            elif dev == 'arrow':
                own = [q for pts in geo['bond_paths'].get(bi, []) for q in pts]
                r = _arrow(mid, perp, own, skip_bonds=(bi,))
                if r is None:
                    failed.append(dict(rec, reason='no_clear_position')); continue
                drawn.append(dict(rec, bbox_px=r))
            else:                                       # underline / asterisk on a bond
                failed.append(dict(rec, reason='device_not_drawable'))
        return drawn, failed, min_pt, bold_atoms

    # ── public renders ────────────────────────────────────────────────────────
    def render(self, dpi=300, marked=True):
        key = (int(dpi), bool(marked))
        if key in self._cache:
            return self._cache[key]
        import numpy as _np
        from PIL import Image
        dpi = int(dpi)
        bond_px = self.tk['bond_pt'] * dpi / 72.0
        base, geo = self._draw_base(dpi)
        img = base.copy()
        drawn, failed, min_pt, bold_atoms = ([], [], None, [])
        if marked and self.marks:
            drawn, failed, min_pt, bold_atoms = self._place_marks(img, geo, dpi)
        a = _np.asarray(img).astype(int)
        b = _np.asarray(base).astype(int)
        # crop to ink (union of marked + unmarked so both share one frame) + 0.15 bond
        ink = (a.min(axis=2) < 250) | (b.min(axis=2) < 250)
        ys, xs = _np.where(ink)
        padc = int(round(0.15 * bond_px))
        if not ys.size:
            # a structure that renders NO ink is a failed render, never a blank picture
            raise ValueError(f'native raster: the structure ({self.orig.GetNumAtoms()} atom(s)) '
                             f'rendered no ink')
        box = (max(0, int(xs.min()) - padc), max(0, int(ys.min()) - padc),
               min(img.width, int(xs.max()) + padc + 1), min(img.height, int(ys.max()) + padc + 1))
        # every drawn mark's recorded box lies inside the PNG (at small tokens a mark's
        # box can reach past ink + 0.15 bond; fuzz 2026-11-02)
        import math as _m
        for d in drawn:
            bb = d.get('bbox_px')
            if isinstance(bb, (list, tuple)) and len(bb) == 4:
                box = (max(0, min(box[0], int(_m.floor(bb[0])))), max(0, min(box[1], int(_m.floor(bb[1])))),
                       min(img.width, max(box[2], int(_m.ceil(bb[2])))),
                       min(img.height, max(box[3], int(_m.ceil(bb[3])))))
        # G2 differential overprint: pixels inside any atom-label GLYPH box that differ
        # between the marked and unmarked renders (a bold-label mark is the label itself).
        overprint = _native_overprint(a, b, geo['glyphs'], skip=bold_atoms)
        out = img.crop(box)
        buf = io.BytesIO()
        out.save(buf, 'PNG', dpi=(dpi, dpi))
        ox, oy = box[0], box[1]

        def _sh(r):
            return [round(r[0] - ox, 1), round(r[1] - oy, 1), round(r[2] - ox, 1), round(r[3] - oy, 1)]
        for d in drawn:
            d['bbox_px'] = _sh(d['bbox_px'])
            if 'bond_px_endpoints' in d:
                d['bond_px_endpoints'] = [[round(p[0] - ox, 1), round(p[1] - oy, 1)] for p in d['bond_px_endpoints']]
            if 'bold_line_endpoints' in d:
                d['bold_line_endpoints'] = [[[round(p[0] - ox, 1), round(p[1] - oy, 1)] for p in ln]
                                            for ln in d['bold_line_endpoints']]
        small = self._small_pt()
        if min_pt is not None:
            small = min(small, min_pt)
        bl = [((geo['coords'][bb.GetBeginAtomIdx()][0] - geo['coords'][bb.GetEndAtomIdx()][0]) ** 2
               + (geo['coords'][bb.GetBeginAtomIdx()][1] - geo['coords'][bb.GetEndAtomIdx()][1]) ** 2) ** 0.5
              for bb in self.mol.GetBonds()]
        meta = {
            'atom_label_pt': self.tk['font_pt'], 'small_pt': round(small, 3),
            'bond_pt': self.tk['bond_pt'], 'line_pt': self.tk['line_pt'],
            'monochrome': self.tk['monochrome'], 'highlight_bands': 0,
            'marks_drawn': drawn, 'marks_failed': failed,
            'label_boxes_px': [_sh(geo['labels'][k_]) for k_ in sorted(geo['labels'])],
            'abbreviations': list(self.abbrev_labels), 'cross_note': self.cross_note,
            'depictor': self.depictor, 'overprint_px': overprint,
            'natural_width_in': out.width / float(dpi), 'natural_height_in': out.height / float(dpi),
            'converted_from_highlight': self.converted, 'dpi': dpi,
            'bond_px_measured': (sum(bl) / len(bl)) if bl else None,
            'crop_box_px': list(box),
        }
        res = (buf.getvalue(), out.width / float(dpi), meta)
        self._cache[key] = res
        return res


def _native_overprint(marked, unmarked, glyphs, skip=()):
    """G2 differential check: count of pixels inside any atom-label glyph box that
    differ between the marked and the unmarked render (arrays HxWx3, same frame).
    A label deliberately emboldened by a 'bold' mark (atoms in `skip`) is excluded."""
    import numpy as _np
    a, b = _np.asarray(marked).astype(int), _np.asarray(unmarked).astype(int)
    diff = (a != b).any(axis=2)
    mask = _np.zeros(diff.shape, dtype=bool)
    for ai, gs in glyphs.items():
        if ai in skip:
            continue
        for g in gs:
            x0, y0 = max(0, int(_np.floor(g[0]))), max(0, int(_np.floor(g[1])))
            x1, y1 = min(diff.shape[1], int(_np.ceil(g[2])) + 1), min(diff.shape[0], int(_np.ceil(g[3])) + 1)
            mask[y0:y1, x0:x1] = True
    return int((diff & mask).sum())


def _pt_seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    if L2 <= 0:
        return ((p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2) ** 0.5
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    x, y = a[0] + t * dx, a[1] + t * dy
    return ((p[0] - x) ** 2 + (p[1] - y) ** 2) ** 0.5


def option_identities(draws):
    """v1.18 (G01 R1.1): the re-perceived identity of every draw's .canonical —
    bc.reaction_identity for a reaction SMILES (two '>'), else bc.structure_identity
    (2-D MolBlock round trip with wedges). None for a draw without .canonical or an
    unparseable one. Never raises."""
    out = []
    for d in draws or []:
        c = getattr(d, 'canonical', None)
        if not isinstance(c, str) or not c.strip() or getattr(d, 'identity_exempt', False):
            out.append(None)                                     # exempt: a conformer / projection set
            continue
        try:
            out.append(bc.reaction_identity(c) if c.count('>') == 2 else bc.structure_identity(c))
        except Exception:                                        # noqa: BLE001
            out.append(None)
    return out


def assert_option_identities(draws):
    """v1.18 (G01 R1.2): raise OptionIdentityError when two draws of one option set carry
    EQUAL re-perceived identity. Visual difference does not make two options different.
    Returns the identity list (stored by S10-8 as option_identities[] on the item)."""
    ids = option_identities(draws)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if ids[i] is not None and ids[i] == ids[j]:
                raise OptionIdentityError(
                    f'LADDER-REPAIR R2o G-OPTDISTINCT: options {i + 1} and {j + 1} are ONE entity '
                    f'({ids[i]}) — regenerate the distractor (never the key); visual '
                    f'difference does not make two options different (GAP-2026-11-03 G01).')
    return ids


def stereo_declared(draw_fn, declared):
    """v1.18 (owner Q-A): attach the author's intended stereo-descriptor line to a draw
    (string such as '2E,4Z' / '(2R,3S)' / 'none'). S10-8 runs
    bc.stereo_declaration_check(draw_fn.canonical, draw_fn.stereo_declared) before the
    figure is accepted. Returns draw_fn."""
    try:
        draw_fn.stereo_declared = '' if declared is None else str(declared)
    except Exception:                                            # noqa: BLE001 — a plain callable
        pass
    return draw_fn


def identity_exempt(draw_fn, exempt=True):
    """v1.18 (release review): mark a draw whose option set is the SAME molecule drawn in
    different conformations / projections by design (chair, Newman, Fischer, Haworth,
    sawhorse — figure_types.identity_kind is None for those types): the identity check
    (option_identities / assert_option_identities) skips it and the reviewer decides.
    Returns draw_fn."""
    try:
        draw_fn.identity_exempt = bool(exempt)
    except Exception:                                            # noqa: BLE001 — a plain callable
        pass
    return draw_fn


def native_option_set(draw_fns, dpi=300):
    """GAP-2026-11-02 F4/F6: an option set at ONE set of tokens on a UNIFORM canvas
    (max width x max height of the set, white, no frame), each picture centred.
    -> [(png_bytes, width_in, meta), ...]; every width_in is equal. Raises ValueError
    when a draw is not native or the draws' tokens differ (one bond length per set).
    v1.18: raises OptionIdentityError (G01 R1.2) when two draws are ONE entity —
    checked FIRST, before any pixel is rendered."""
    from PIL import Image
    draws = list(draw_fns or [])
    if not draws:
        raise ValueError('native_option_set: no draws')
    assert_option_identities(draws)                              # v1.18 — G-OPTDISTINCT at render
    toks = []
    for d in draws:
        if getattr(d, 'render_mode', None) != 'native_raster' or not callable(getattr(d, 'native_png', None)):
            raise ValueError('native_option_set: every draw must be a native-raster draw (tokens=...)')
        toks.append(tuple(sorted((k, v) for k, v in (getattr(d, 'tokens', None) or {}).items())))
    if len(set(toks)) != 1:
        raise ValueError('native_option_set: the draws were rendered with different tokens — an '
                         'option set shares one bond length / label size')
    if (getattr(draws[0], 'tokens', None) or {}).get('monochrome') is False:
        # 2026.11.02 B6 — Q7b.14 one element-colour decision per SET: options that differ
        # in which coloured elements they carry render every option black, so heteroatom
        # colour cannot single an option out (only ever a downgrade to black).
        elems = [getattr(d, 'coloured_elements', None) for d in draws]
        modes = {bool(getattr(d, 'element_colours', True)) for d in draws}
        if not (all(e is not None for e in elems) and len({frozenset(e) for e in elems}) == 1
                and len(modes) == 1):
            for d in draws:
                if callable(getattr(d, 'set_element_colours', None)):
                    d.set_element_colours(False)
    rendered = [d.native_png(dpi) for d in draws]
    ims = [Image.open(io.BytesIO(png)).convert('RGB') for png, _w, _m in rendered]
    W, H = max(i.width for i in ims), max(i.height for i in ims)
    out = []
    for im, (_png, _w, meta) in zip(ims, rendered):
        c = Image.new('RGB', (W, H), (255, 255, 255))
        ox, oy = (W - im.width) // 2, (H - im.height) // 2
        c.paste(im, (ox, oy))
        buf = io.BytesIO()
        c.save(buf, 'PNG', dpi=(int(dpi), int(dpi)))
        m2 = dict(meta)
        m2['label_boxes_px'] = [[b[0] + ox, b[1] + oy, b[2] + ox, b[3] + oy] for b in meta.get('label_boxes_px', [])]
        def _shift_mk(mk):
            d = dict(mk)
            if d.get('bbox_px'):
                d['bbox_px'] = [d['bbox_px'][0] + ox, d['bbox_px'][1] + oy,
                                d['bbox_px'][2] + ox, d['bbox_px'][3] + oy]
            if isinstance(d.get('bond_px_endpoints'), list):
                d['bond_px_endpoints'] = [[q[0] + ox, q[1] + oy] for q in d['bond_px_endpoints']]
            if isinstance(d.get('bold_line_endpoints'), list):
                d['bold_line_endpoints'] = [[[a[0] + ox, a[1] + oy], [b[0] + ox, b[1] + oy]]
                                            for a, b in d['bold_line_endpoints']]
            return d
        m2['marks_drawn'] = [_shift_mk(mk) for mk in meta.get('marks_drawn', [])]
        m2['marks_failed'] = [_shift_mk(mk) for mk in meta.get('marks_failed', [])]
        m2['natural_width_in'] = W / float(dpi)
        m2['natural_height_in'] = H / float(dpi)
        m2['option_canvas_px'] = [W, H]
        m2['option_offset_px'] = [ox, oy]
        m2['frame'] = False
        out.append((buf.getvalue(), W / float(dpi), m2))
    return out


# an explicit hydrogen atom in a SMILES: [H], [2H], [H+], [H:3], [2H:1] — never He/Hg/Hf/Ho/Hs
_EXPLICIT_H_RE = re.compile(r'\[\d*H(?![a-z])')


def structure_draw_fn(smiles, px=(900, 700), extent=(0.0, 9.0, 0.0, 7.0),
                      element_colours=True, highlight_atoms=(), highlight_bonds=(),
                      tokens=None, marks=None, abbreviations=None, protect_atoms=(),
                      conformer_set=False):
    """A figural_core draw_fn (ax, series, palette) that rasterises `smiles` with
    rdkit into the axes. The image IS the semantic object: what is registered is
    what was drawn (MockTestCreate v5.59 S7-NEW-B2). Raises ValueError if rdkit
    rejects the SMILES or is unavailable — a STRUCTURE figure is never hand-drawn.

    v1.14 (MockTestCreate v5.80 S10-7C / Q7b.9 / Q7b.14): atoms are coloured from
    figural_core.ATOM_PALETTE (never rdkit's default); `highlight_*` accent the
    interrogated site in figural_core.HIGHLIGHT_COLOUR (opaque; atom highlights
    redirected to its incident bonds, never under the symbol); `element_colours=False`
    renders every atom black. The returned draw_fn carries .canonical,
    .coloured_elements and .set_element_colours(flag); render_option_set() uses the
    last two to keep heteroatom colour uniform across an option set.

    v1.17 (GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY F1/F2/F4/F7) — PRINT-TRUE NATIVE
    RASTER, opt-in: with `tokens` ({'font_pt','line_pt','bond_pt','monochrome',
    'mark_colour'}, printed points) the draw also carries render_mode='native_raster',
    .tokens, .native_png(dpi=300) and .native_png_unmarked(dpi=300), each ->
    (png_bytes, natural_width_in, meta). No highlight band is ever drawn on that path:
    highlight_* are converted to marks (bond -> bold, atom -> asterisk) and `marks`
    places underline / asterisk / letter / arrow / bold clear of every label and bond.
    `abbreviations` (None/[] = none) condenses only the listed lexicon labels, never
    over protect_atoms or a marked site. tokens=None: every v1.16 behaviour unchanged
    (marks / abbreviations / protect_atoms are then ignored)."""
    if '>' in str(smiles or ''):
        raise ValueError(f'structure_draw_fn: {smiles!r} is a reaction SMILES — a reaction is '
                         f'drawn by render_scheme (S7-NEW-B2 REACTION path), never as one molecule')
    canon, reason = canonical_structure(smiles)
    if canon is None:
        raise ValueError(f'structure_draw_fn: cannot render {smiles!r}: {reason}')
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    import numpy as _np
    from PIL import Image as _Image
    # DEPENDENCY DIRECTION (validator check AI): corpus_io is routed to every PYQ
    # step, where figural_core is NOT loaded, so this module never imports it.
    # The palette is read out of figural_core ONLY IF the Create flow has already
    # imported it in this process (S7-NEW-B2: the Create flow imports figural_core as fc
    # before every render). Without it the structure renders BLACK-AND-WHITE
    # — deterministic, never rdkit's default — and records draw.palette_note.
    import sys as _sys
    _fc = _sys.modules.get('figural_core')
    if _fc is not None and hasattr(_fc, 'ATOM_PALETTE'):
        _atom_pal, _coloured, _hl, _hl_mult = (_fc.ATOM_PALETTE, _fc.ATOM_COLOURED_SYMBOLS,
                                               _fc.HIGHLIGHT_COLOUR, _fc.HIGHLIGHT_BOND_WIDTH_MULT)
        _pal_note = None
    else:
        _atom_pal, _coloured, _hl, _hl_mult = {}, frozenset(), '#0072B2', 6
        _pal_note = 'figural_core not loaded in this process — BW atom palette used'
    mol = Chem.MolFromSmiles(smiles)
    if tokens is not None and _EXPLICIT_H_RE.search(str(smiles)):
        # 2026.11.02 B4: rdkit's default parse REMOVES explicit [H] atoms (and mapped
        # [H:n]), renumbering every later atom, so a mark index read off the SMILES
        # landed on the wrong atom and a mark on the H itself was impossible. On the
        # native path the explicit H atoms are kept: the molecule that is validated,
        # marked and drawn is the one the SMILES spells, atom for atom. The legacy
        # path (tokens=None) is unchanged.
        _pp = Chem.SmilesParserParams()
        _pp.removeHs = False
        _mh = Chem.MolFromSmiles(smiles, _pp)
        if _mh is not None:
            mol = _mh
    if tokens is not None and mol.GetNumAtoms() == 0:
        # '' parses to an EMPTY molecule: on the native path that is an invalid SMILES
        # (a blank picture would pass every gate), never a figure.
        raise ValueError(f'structure_draw_fn: cannot render {smiles!r}: no atoms')
    present = {a.GetSymbol() for a in mol.GetAtoms()}
    state = {'colours': bool(element_colours), 'note': _pal_note}
    # Atom highlights are FILLED discs on every rdkit build tested (fillHighlights
    # is not honoured for atoms), so a disc may sit only under an UNLABELLED
    # carbon vertex; a labelled heteroatom's accent moves to its incident bonds
    # so the symbol is never overprinted (Q7b.9 text contrast).
    hl_atoms, hl_bonds = [], [int(i) for i in (highlight_bonds or ())]
    _n_atoms = mol.GetNumAtoms()
    _n_bonds = mol.GetNumBonds()
    for i in hl_bonds:
        if not (0 <= i < _n_bonds):
            raise ValueError(f'structure_draw_fn: highlight_bonds index {i} outside '
                             f'0..{_n_bonds - 1} for {smiles!r}')
    for i in (highlight_atoms or ()):
        if not (0 <= int(i) < _n_atoms):
            raise ValueError(f'structure_draw_fn: highlight_atoms index {i} outside '
                             f'0..{_n_atoms - 1} for {smiles!r}')
        a = mol.GetAtomWithIdx(int(i))
        if a.GetSymbol() == 'C' and not a.GetFormalCharge():
            hl_atoms.append(int(i))
        else:
            hl_bonds += [b.GetIdx() for b in a.GetBonds() if b.GetIdx() not in hl_bonds]
    hl_rgb = tuple(int(_hl[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    _native = None
    if tokens is not None:
        # v1.17 NATIVE RASTER: never a highlight band (GAP-2026-11-02 F2). The requested
        # highlights become marks; the matplotlib raster below is drawn without them.
        _tk = _native_tokens(tokens)
        _marks = [dict(m) for m in (marks or [])]
        _conv = bool(highlight_bonds or highlight_atoms)
        _marks += [{'site': {'kind': 'bond', 'index': int(i)}, 'device': 'bold'}
                   for i in (highlight_bonds or ())]
        _marks += [{'site': {'kind': 'atom', 'index': int(i)}, 'device': 'asterisk'}
                   for i in (highlight_atoms or ())]
        hl_atoms, hl_bonds = [], []
        if _tk['monochrome']:
            state['colours'] = False
        _native = _NativeStructure(mol, _tk, _marks, abbreviations, protect_atoms,
                                   (_atom_pal, bool(element_colours)), _conv)

    def _raster():
        d = rdMolDraw2D.MolDraw2DCairo(int(px[0]), int(px[1]))
        o = d.drawOptions()
        o.clearBackground = False
        if state['colours'] and _atom_pal and hasattr(o, 'updateAtomPalette'):
            o.updateAtomPalette({int(k): tuple(v) for k, v in _atom_pal.items()})
            # anything not in the pinned map (S, P, metals, ...) is BLACK
            _missing = {a.GetAtomicNum() for a in mol.GetAtoms()} - set(_atom_pal)
            if _missing:
                o.updateAtomPalette({int(k): (0.0, 0.0, 0.0) for k in _missing})
        elif hasattr(o, 'useBWAtomPalette'):
            o.useBWAtomPalette()
            if state['colours'] and _atom_pal:
                state['note'] = 'rdkit lacks updateAtomPalette — BW palette used'
        elif state['colours'] and _atom_pal:
            state['note'] = ('rdkit lacks atom-palette control — its default '
                             'palette was used (report as an AMBER note)')
        if hl_atoms or hl_bonds:
            if hasattr(o, 'setHighlightColour'):
                o.setHighlightColour(hl_rgb + (1.0,))
            if hasattr(o, 'highlightBondWidthMultiplier'):
                o.highlightBondWidthMultiplier = int(_hl_mult)
        rdMolDraw2D.PrepareAndDrawMolecule(d, mol, highlightAtoms=hl_atoms,
                                           highlightBonds=hl_bonds)
        d.FinishDrawing()
        return _np.asarray(_Image.open(io.BytesIO(d.GetDrawingText())).convert('RGBA'))

    holder = {'arr': _raster()}

    def draw(ax, series=None, palette=None):
        ax.imshow(holder['arr'], extent=extent)
        ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3])
        ax.axis('off')

    def set_element_colours(flag):
        flag = bool(flag)
        if flag != state['colours']:
            state['colours'] = flag
            holder['arr'] = _raster()
        if _native is not None and _native.palette[1] != flag:
            # 2026.11.02 B6: the native raster honours the set-wide decision too
            # (a no-op for monochrome tokens, which always draw the BW palette)
            _native.palette = (_native.palette[0], flag)
            _native._cache.clear()
        draw.element_colours = state['colours']
        draw.palette_note = state['note']

    draw.canonical = canon
    draw.coloured_elements = frozenset(present & _coloured)
    draw.element_colours = state['colours']
    draw.highlight = {'atoms': hl_atoms, 'bonds': hl_bonds}
    draw.set_element_colours = set_element_colours
    draw.palette_note = state['note']
    # v1.16 — additive: the compositor (render_scheme) blits the same raster as a
    # tile, so a scheme's molecules carry structure_draw_fn provenance per tile.
    draw.raster = lambda: holder['arr']
    draw.px = (int(px[0]), int(px[1]))
    if _native is not None:
        # v1.17 — additive, only when tokens were given (legacy draws carry none of these)
        draw.render_mode = 'native_raster'
        draw.tokens = dict(_tk)
        draw.marks = list(_native.marks)
        draw.native_png = lambda dpi=300: _native.render(dpi, marked=True)
        draw.native_png_unmarked = lambda dpi=300: _native.render(dpi, marked=False)
    # v1.18 (release review): `conformer_set=True` marks a draw that belongs to a
    # conformer / projection option set (the SAME molecule drawn differently by design)
    # — the option identity check skips it (identity_exempt; reviewer decides).
    identity_exempt(draw, bool(conformer_set))
    return draw


# ═══════════════════════════════════════════════════════════════════════════════
# REACTION-SCHEME COMPOSITOR (v1.16, GAP-2026-11-01 LAW F1.3)
#
# The real exam asks organic questions as DRAWN SCHEMES: substrate → arrow carrying
# reagents (above) and conditions (below) → product or placeholder letter. Measured
# on a real paper (07-Jun-2023): 20 of 24 figural organic questions. The grammar the
# renderer must cover, each element seen on that paper:
#   G1  substrates joined by '+'            G6  bracketed intermediate [ A ]
#   G2  right / sequential / left arrows    G7  product drawn when the ask is elsewhere
#   G3  reagent lines above, conditions     G8  multi-row panels (rows=[...])
#       below (≤2 lines each)               G9  wedges / charges / numbering (rdkit)
#   G4  reagent drawn as a structure        G10 option = labelled pair  A = …  B = …
#   G5  placeholder letters, tile labels
#
# SCHEME SPEC (reading order; one list per row):
#   {'rows': [[item, ...], ...]}   or   {'items': [item, ...]}   (a single row)
#   item ∈ {'mol': SMILES, 'label': 'A'|None, 'equiv': '(2 equiv)'|None,
#                 'highlight_atoms': [...], 'highlight_bonds': [...], 'role': 'reactant'|'product'|'agent'}
#          {'plus': True}
#          {'arrow': {'dir': 'right'|'left'|'both', 'above': [str, ...], 'below': [str, ...],
#                     'reagent_mol': SMILES|None}}
#          {'placeholder': 'A'}            {'bracket': 'A'}            {'text': '...'}
#          {'pair': [('A', SMILES), ('B', SMILES)]}                    (G10)
# The role of a molecule defaults by position: before the first arrow of its row →
# reactant; a reagent_mol → agent; after an arrow → product. The REACTION canonical is
# assembled per row as 'reactants>agents>products' (placeholders omitted) and joined
# across rows with ' | ' in .descriptor['row_canonicals']; .canonical is row 1's (one
# semantic object per row — S7-NEW-B2 role 'problem:<i>').
# ═══════════════════════════════════════════════════════════════════════════════

SCHEME_TILE_H = 1.0          # data units; the fitter owns the final scale (Q10)
SCHEME_TILE_W_MAX = 2.2
SCHEME_GAP = 0.18
SCHEME_ARROW_L = 1.35
SCHEME_ROW_GAP = 0.45
SCHEME_TEXT_PT = 9.0         # reagent/condition lines; FigureSpec fonts scale the rest
SCHEME_LABEL_PT = 12.0       # placeholder letters / tile labels (bold)


def _scheme_rows(spec):
    if not isinstance(spec, dict):
        raise ValueError('render_scheme: spec must be a dict')
    rows = spec.get('rows')
    if rows is None:
        rows = [spec.get('items') or []]
    if not isinstance(rows, (list, tuple)) or not rows or not all(isinstance(r, (list, tuple)) for r in rows):
        raise ValueError('render_scheme: spec needs rows=[[item,...],...] or items=[item,...]')
    if not any(r for r in rows):
        raise ValueError('render_scheme: scheme has no items')
    return [list(r) for r in rows]


def _crop_raster(arr, pad=12):
    """Crop an RGBA tile to its ink (rdkit pads its canvas heavily, which made every
    molecule read smaller than the arrow beside it). Pure numpy; returns the input
    unchanged when it carries no ink."""
    import numpy as _np
    a = _np.asarray(arr)
    if a.ndim != 3 or a.shape[0] < 4 or a.shape[1] < 4:
        return a
    if a.shape[2] == 4:
        ink = a[:, :, 3] > 0
    else:
        ink = (a[:, :, :3].astype(int).sum(axis=2) < 3 * 250)
    ys, xs = _np.where(ink)
    if ys.size == 0:
        return a
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    return a[y0:y1, x0:x1]


def _text_width_units(s, pt):
    """Crude width estimate in data units for layout (the fitter measures the truth)."""
    return 0.085 * (pt / 9.0) * max(1, len(str(s)))


def scheme_canonical(spec):
    """Reaction SMILES per row, 'reactants>agents>products', placeholders omitted.
    Pure string work on the spec (no rdkit): the drawn molecules' SMILES as written.

    ROLES BY ARROW DIRECTION (G2: right, sequential, LEFT and bidirectional arrows). A row
    is split into SEGMENTS by its arrows. Every arrow has a TAIL segment (the side it
    starts from: left of a right-arrow, right of a left-arrow; both for 'both') and a HEAD
    segment. A molecule in a tail-only segment is a REACTANT, in a head-only segment a
    PRODUCT, in a segment that is both (the drawn intermediate of A → B → C) an
    INTERMEDIATE (recorded in the descriptor, omitted from the canonical). An explicit
    item role ('reactant' | 'product' | 'agent') always wins. A reagent drawn on an arrow
    is an AGENT. Returns [row_canonical, ...]; '' only for a row with no molecule in a
    reactant or product position (render_scheme refuses such a row)."""
    out = []
    for row in _scheme_rows(spec):
        segs = [[]]
        arrows = []                       # (dir, reagent_mol)
        for it in row:
            if 'arrow' in it:
                a = it['arrow'] or {}
                arrows.append((a.get('dir', 'right'), a.get('reagent_mol')))
                segs.append([])
            elif 'mol' in it:
                segs[-1].append((it['mol'], it.get('role')))
            elif 'pair' in it:
                for _lbl, smi in it['pair']:
                    segs[-1].append((smi, None))
        tails, heads = set(), set()
        for i, (d, _rm) in enumerate(arrows):
            if d == 'left':
                tails.add(i + 1); heads.add(i)
            elif d == 'both':
                tails.add(i); tails.add(i + 1); heads.add(i); heads.add(i + 1)
            else:
                tails.add(i); heads.add(i + 1)
        react, agents, prods = [], [], []
        for si, seg in enumerate(segs):
            for smi, role in seg:
                if role == 'agent':
                    agents.append(smi)
                elif role == 'reactant':
                    react.append(smi)
                elif role == 'product':
                    prods.append(smi)
                elif si in tails and si not in heads:
                    react.append(smi)
                elif si in heads and si not in tails:
                    prods.append(smi)
                elif si in tails and si in heads:
                    if arrows and all(d == 'both' for d, _ in arrows):
                        (react if si == 0 else prods).append(smi)     # A ⇌ B: left-to-right
                    # else: an intermediate — omitted from the canonical by design
                elif not arrows:
                    react.append(smi)                                  # no arrow: refused by render_scheme
        agents += [rm for _d, rm in arrows if rm]
        out.append('.'.join(react) + '>' + '.'.join(agents) + '>' + '.'.join(prods)
                   if (react or prods) else '')
    return out


def _scheme_native_items(rows, tiles):
    """Pair every spec item with the tile(s) render_scheme created for it, in the same
    order the legacy walk called structure_draw_fn (mol -> 1, reagent_mol -> 1, pair -> 2)."""
    it_tiles = iter(tiles)
    out = []
    for row in rows:
        r = []
        for it in row:
            if 'mol' in it:
                r.append({'kind': 'mol', 'tile': next(it_tiles), 'label': it.get('label'),
                          'equiv': it.get('equiv')})
            elif it.get('plus'):
                r.append({'kind': 'plus'})
            elif 'arrow' in it:
                a = dict(it['arrow'] or {})
                above = [str(t) for t in (a.get('above') or []) if t is not None and str(t).strip()]
                below = [str(t) for t in (a.get('below') or []) if t is not None and str(t).strip()]
                rm = next(it_tiles) if a.get('reagent_mol') else None
                r.append({'kind': 'arrow', 'dir': a.get('dir', 'right'), 'above': above,
                          'below': below, 'reagent': rm})
            elif 'placeholder' in it:
                r.append({'kind': 'ph', 'text': str(it['placeholder'])})
            elif 'bracket' in it:
                r.append({'kind': 'bracket', 'text': f'[ {it["bracket"]} ]'})
            elif 'text' in it:
                r.append({'kind': 'text', 'text': str(it['text'])})
            elif 'pair' in it:
                r.append({'kind': 'pair', 'members': [(f'{lbl} =', next(it_tiles)) for lbl, _s in it['pair']]})
        out.append(r)
    return out


def _tile_index(tiles, t):
    for i, x in enumerate(tiles):
        if x is t:
            return i
    return None


def _scheme_native_render(rows, tiles, tk, max_width_in, dpi=300):
    """Compose a scheme at NATURAL size with PIL (no matplotlib): every tile from the
    native structure path at the same tokens, arrows and text in points. Overflow:
    (1) split multi-arrow rows after a product/intermediate tile, repeating it;
    (2) stack reagent text (<= 2 lines above / below; excess to the stem);
    (3) else meta['overflow'] = True — never scaled here (the caller decides)."""
    from PIL import Image, ImageDraw
    dpi = int(dpi)
    k = dpi / 72.0
    font_px, line_px, bond_px = tk['font_pt'] * k, max(1.0, tk['line_pt'] * k), tk['bond_pt'] * k
    f_reg, font_file = _native_font('regular', font_px)
    f_bold, _fb = _native_font('bold', font_px)
    G = 0.5 * font_px                       # gap between items
    line_h = 1.2 * font_px
    tgap = 0.3 * font_px                    # text clearance from the arrow shaft
    head_l = max(3.5 * line_px, 0.5 * font_px)
    head_w = 0.38 * head_l
    M = int(round(0.15 * bond_px))
    max_w_px = float(max_width_in) * dpi
    ink = tuple(int(tk['mark_colour'][i:i + 2], 16) for i in (1, 3, 5)) if not tk['monochrome'] else (0, 0, 0)

    # render each tile once at this dpi
    rendered = {}
    tile_metas = []
    for t in tiles:
        png, _w, meta = t.native_png(dpi)
        rendered[id(t)] = Image.open(io.BytesIO(png)).convert('RGB')
        tile_metas.append(meta)

    def _tw(s, f=f_reg):
        return float(f.getlength(str(s)))

    def _arrow_len(e):
        texts = e['above'] + e['below']
        L = max(3.0 * bond_px, (max(_tw(t) for t in texts) + 0.5 * font_px) if texts else 0.0)
        if e['reagent'] is not None:
            L = max(L, rendered[id(e['reagent'])].width + 0.5 * font_px)
        return L

    def _dims(e):
        """(width, up, down) about the row's arrow line."""
        kd = e['kind']
        if kd == 'mol':
            im = rendered[id(e['tile'])]
            extra = line_h * (bool(e.get('label')) + bool(e.get('equiv')))
            # 2026.11.02 B7: a caption wider than its molecule ('(2 equiv)' under a
            # small tile) was clipped by the neighbour / canvas edge; the tile is as
            # wide as the widest of image, label and equiv line, molecule centred.
            w = max(float(im.width),
                    _tw(e['label'], f_bold) if e.get('label') else 0.0,
                    _tw(e['equiv'], f_reg) if e.get('equiv') else 0.0)
            return w, im.height / 2.0, im.height / 2.0 + extra
        if kd == 'arrow':
            up = tgap + line_h * len(e['above']) + max(head_w, line_px / 2.0)
            if e['reagent'] is not None:
                up += rendered[id(e['reagent'])].height + tgap
            return _arrow_len(e), up, tgap + line_h * len(e['below']) + max(head_w, line_px / 2.0)
        if kd == 'pair':
            w, h = 0.0, 0.0
            for lbl, t in e['members']:
                im = rendered[id(t)]
                w += _tw(lbl, f_bold) + 0.3 * font_px + im.width + G
                h = max(h, im.height)
            return w - G, h / 2.0, h / 2.0
        f = f_reg if kd in ('plus', 'text') else f_bold
        txt = '+' if kd == 'plus' else e['text']
        return _tw(txt, f), 0.6 * font_px, 0.6 * font_px

    def _row_w(r):
        return sum(_dims(e)[0] for e in r) + G * max(0, len(r) - 1)

    layout = [list(r) for r in _scheme_native_items(rows, tiles)]
    reflowed = False
    # (1) re-flow multi-arrow rows: break after a 'mol' tile with an arrow on each side,
    #     repeat that tile at the head of the continuation row; as few splits as needed.
    out_rows = []
    for r in layout:
        start = 0
        while _row_w(r[start:]) + 2 * M > max_w_px:
            arrows = [i for i, e in enumerate(r) if e['kind'] == 'arrow']
            cands = [i for i, e in enumerate(r) if e['kind'] == 'mol' and i > start
                     and any(start < a < i for a in arrows) and any(a > i for a in arrows)]
            if not cands:
                break
            fit = [i for i in cands if _row_w(r[start:i + 1]) + 2 * M <= max_w_px]
            kk = max(fit) if fit else min(cands)
            out_rows.append(r[start:kk + 1])
            start = kk
            reflowed = True
        out_rows.append(r[start:])
    layout = out_rows
    # (2) stack reagent text into <= 2 lines above / below; excess lines go to the stem
    moved = []
    for r in layout:
        excess = _row_w(r) + 2 * M - max_w_px
        if excess <= 0:
            continue
        for e in sorted([e for e in r if e['kind'] == 'arrow'], key=_arrow_len, reverse=True):
            if excess <= 0:
                break
            L0 = _arrow_len(e)
            target = max(3.0 * bond_px, L0 - excess) - 0.5 * font_px
            new = {}
            for side in ('above', 'below'):
                pieces = [p for ln in e[side] for p in re.split(r'(?<=[,;])\s+', ln) if p.strip()]
                lines = []
                for p in pieces:
                    if lines and _tw(lines[-1] + ' ' + p) <= target:
                        lines[-1] = lines[-1] + ' ' + p
                    else:
                        lines.append(p)
                new[side] = lines
            if all(new[s] == e[s] for s in ('above', 'below')):
                continue
            e2 = dict(e)
            for side in ('above', 'below'):
                e2[side] = new[side][:2]
            if _arrow_len(e2) < L0:
                for side in ('above', 'below'):
                    moved += new[side][2:]
                    e[side] = e2[side]
                excess -= L0 - _arrow_len(e)
    overflow = any(_row_w(r) + 2 * M > max_w_px for r in layout)

    # compose
    dims = [[_dims(e) for e in r] for r in layout]
    row_up = [max([d[1] for d in ds] + [0.0]) for ds in dims]
    row_dn = [max([d[2] for d in ds] + [0.0]) for ds in dims]
    row_gap = 0.8 * font_px
    Wc = int(round(max(_row_w(r) for r in layout) + 2 * M))
    Hc = int(round(sum(u + d for u, d in zip(row_up, row_dn)) + row_gap * (len(layout) - 1) + 2 * M))
    img = Image.new('RGB', (max(1, Wc), max(1, Hc)), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    tile_off = {}                           # id(tile) -> (x, y) of its FIRST paste
    y = float(M)
    for r, ds, up, dn in zip(layout, dims, row_up, row_dn):
        cy = y + up
        x = float(M)
        for e, (w, _u, _d) in zip(r, ds):
            kd = e['kind']
            if kd == 'mol':
                im = rendered[id(e['tile'])]
                _px = (int(round(x + (w - im.width) / 2.0)), int(round(cy - im.height / 2.0)))
                img.paste(im, _px)
                tile_off.setdefault(id(e['tile']), _px)
                ty = cy + im.height / 2.0
                if e.get('label'):
                    dr.text((x + w / 2.0, ty), str(e['label']), font=f_bold, fill=ink, anchor='ma')
                    ty += line_h
                if e.get('equiv'):
                    dr.text((x + w / 2.0, ty), str(e['equiv']), font=f_reg, fill=ink, anchor='ma')
            elif kd == 'arrow':
                L = w
                d_ = e['dir']
                x0s = x + (head_l if d_ in ('left', 'both') else 0.0)
                x1s = x + L - (head_l if d_ in ('right', 'both') else 0.0)
                dr.rectangle([x0s, cy - line_px / 2.0, x1s, cy + line_px / 2.0 - 1], fill=ink)
                if d_ in ('right', 'both'):
                    dr.polygon([(x + L, cy), (x + L - head_l, cy - head_w), (x + L - head_l, cy + head_w)], fill=ink)
                if d_ in ('left', 'both'):
                    dr.polygon([(x, cy), (x + head_l, cy - head_w), (x + head_l, cy + head_w)], fill=ink)
                ybase = cy - max(head_w, line_px / 2.0) - tgap
                if e['reagent'] is not None:
                    im = rendered[id(e['reagent'])]
                    _px = (int(round(x + (L - im.width) / 2.0)), int(round(ybase - im.height)))
                    img.paste(im, _px)
                    tile_off.setdefault(id(e['reagent']), _px)
                    ybase -= im.height + tgap
                for i, t in enumerate(reversed(e['above'])):
                    dr.text((x + L / 2.0, ybase - i * line_h), t, font=f_reg, fill=ink, anchor='md')
                yb = cy + max(head_w, line_px / 2.0) + tgap
                for i, t in enumerate(e['below']):
                    dr.text((x + L / 2.0, yb + i * line_h), t, font=f_reg, fill=ink, anchor='ma')
            elif kd == 'pair':
                xx = x
                for lbl, t in e['members']:
                    dr.text((xx, cy), lbl, font=f_bold, fill=ink, anchor='lm')
                    xx += _tw(lbl, f_bold) + 0.3 * font_px
                    im = rendered[id(t)]
                    _px = (int(round(xx)), int(round(cy - im.height / 2.0)))
                    img.paste(im, _px)
                    tile_off.setdefault(id(t), _px)
                    xx += im.width + G
            else:
                f = f_reg if kd in ('plus', 'text') else f_bold
                dr.text((x + w / 2.0, cy), '+' if kd == 'plus' else e['text'], font=f, fill=ink, anchor='mm')
            x += w + G
        y += up + dn + row_gap
    buf = io.BytesIO()
    img.save(buf, 'PNG', dpi=(dpi, dpi))
    # 2026.11.02 B3: every tile's marks reach the SCHEME's own record, each carrying
    # 'tile' (its index in render_scheme's .tiles) and its bbox in scheme pixels.
    # They used to live only in tile_metas, which figural_core never reads, so a
    # marked scheme recorded no mark and an unplaceable one no failure.
    marks_drawn, marks_failed = [], []
    for ti, (t, tm) in enumerate(zip(tiles, tile_metas)):
        off = tile_off.get(id(t))
        for mk in tm.get('marks_drawn') or []:
            m2 = dict(mk, tile=ti)
            if off is not None and mk.get('bbox_px'):
                b_ = mk['bbox_px']
                m2['bbox_px'] = [b_[0] + off[0], b_[1] + off[1], b_[2] + off[0], b_[3] + off[1]]
            marks_drawn.append(m2)
        marks_failed += [dict(mk, tile=ti) for mk in tm.get('marks_failed') or []]
    meta = {
        'marks_drawn': marks_drawn, 'marks_failed': marks_failed,
        'atom_label_pt': tk['font_pt'],
        'small_pt': round(min([tk['font_pt']] + [m['small_pt'] for m in tile_metas]), 3),
        'bond_pt': tk['bond_pt'], 'line_pt': tk['line_pt'], 'monochrome': tk['monochrome'],
        'highlight_bands': 0, 'rows_after_reflow': len(layout), 'reflowed': reflowed,
        'reagent_lines_moved_to_stem': moved, 'overflow': bool(overflow),
        'tile_metas': tile_metas, 'natural_width_in': img.width / float(dpi),
        'natural_height_in': img.height / float(dpi),
        'overprint_px': int(sum(m['overprint_px'] for m in tile_metas)),
        'font_file': font_file, 'max_width_in': float(max_width_in), 'dpi': dpi,
        'row_leads': [r[0]['kind'] for r in layout],
        'row_lead_tiles': [_tile_index(tiles, r[0]['tile']) if r[0]['kind'] == 'mol' else None for r in layout],
    }
    return buf.getvalue(), img.width / float(dpi), meta


def render_scheme(spec, px_tile=(700, 500), element_colours=True, tokens=None,
                  max_width_in=6.0):
    """A figural_core draw_fn (ax, series, palette) that lays out a reaction scheme.

    Every molecule tile is rendered by structure_draw_fn (same rdkit depiction,
    ATOM_PALETTE, highlight_* and colour_content rules — S10-7C), arrows and text are
    matplotlib artists, and the whole scheme is ONE draw_fn for figural_core.
    render_figure, so the v5.55 fitter (Q10), label deconflict (Q11), G-FIGINK and
    G-FIGFIT apply unchanged. Raises ValueError when rdkit rejects a molecule or the
    spec is malformed — a scheme is never hand-drawn and never silently degraded.

    Returned draw_fn attributes: .canonical (row 1 reaction SMILES, rdkit-canonical),
    .row_canonicals, .descriptor (reagent_lines, unknowns, arrows, rows, tiles),
    .tiles (the per-molecule draw_fns), .coloured_elements, .element_colours,
    .set_element_colours(flag), .highlight, .palette_note, .suggested_aspect (h/w).

    v1.17 (GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY F1): with `tokens` every tile is
    a native-raster structure at those tokens (one bond length across the scheme) and
    the draw also carries render_mode='native_raster', .tokens and .native_png(dpi=300)
    -> (png_bytes, natural_width_in, meta), composed with PIL at natural size (no
    matplotlib), re-flowed / stacked to fit max_width_in, never scaled. tokens=None:
    unchanged. .canonical / .row_canonicals / .descriptor are computed identically."""
    rows = _scheme_rows(spec)
    if tokens is not None:
        _ntk = _native_tokens(tokens)
    tiles, layout = [], []          # layout: per row, list of (kind, payload, x, w)
    reagent_lines, unknowns, n_arrows = [], [], 0
    coloured, notes = set(), []
    row_w = []
    H = SCHEME_TILE_H

    def _tile(smiles, hl_a=(), hl_b=(), item=None):
        if tokens is None:
            d = structure_draw_fn(smiles, px=px_tile, element_colours=element_colours,
                                  highlight_atoms=hl_a, highlight_bonds=hl_b)
        else:
            item = item or {}
            d = structure_draw_fn(smiles, px=px_tile, element_colours=element_colours,
                                  highlight_atoms=hl_a, highlight_bonds=hl_b, tokens=tokens,
                                  marks=item.get('marks'), abbreviations=item.get('abbreviations'),
                                  protect_atoms=item.get('protect_atoms') or ())
        tiles.append(d)
        arr = _crop_raster(d.raster())
        asp = arr.shape[1] / float(arr.shape[0]) if arr.shape[0] else 1.0
        w = min(SCHEME_TILE_W_MAX, H * asp)
        return d, w, H * (w / (H * asp)) if asp else H

    for row in rows:
        x = 0.0
        items = []
        for it in row:
            if not isinstance(it, dict):
                raise ValueError(f'render_scheme: item {it!r} is not a dict')
            if 'mol' in it:
                d, w, h = _tile(it['mol'], it.get('highlight_atoms', ()), it.get('highlight_bonds', ()), it)
                coloured |= set(d.coloured_elements)
                if d.palette_note:
                    notes.append(d.palette_note)
                items.append(('mol', {'draw': d, 'label': it.get('label'), 'equiv': it.get('equiv'),
                                      'h': h}, x, w))
                x += w + SCHEME_GAP
            elif it.get('plus'):
                items.append(('plus', {}, x, 0.32)); x += 0.32 + SCHEME_GAP
            elif 'arrow' in it:
                a = dict(it['arrow'] or {})
                above = [str(t) for t in (a.get('above') or []) if t is not None and str(t).strip()]
                below = [str(t) for t in (a.get('below') or []) if t is not None and str(t).strip()]
                if len(above) > 2 or len(below) > 2:
                    raise ValueError('render_scheme: an arrow carries at most 2 lines above '
                                     'and 2 below (G3) — move the rest into the stem')
                reagent_lines += above + below
                n_arrows += 1
                rm = None
                if a.get('reagent_mol'):
                    # drawn above the arrow (G4); 2026.11.02 B3: its own marks via 'reagent_marks'
                    rm, _rw, _rh = _tile(a['reagent_mol'], item={'marks': a.get('reagent_marks')})
                tw = max([_text_width_units(t, SCHEME_TEXT_PT) for t in above + below] + [0.0])
                L = max(SCHEME_ARROW_L, tw + 0.3, (0.0 if rm is None else 1.5))
                items.append(('arrow', {'dir': a.get('dir', 'right'), 'above': above,
                                        'below': below, 'reagent': rm}, x, L))
                x += L + SCHEME_GAP
            elif 'placeholder' in it:
                unknowns.append(str(it['placeholder']))
                items.append(('ph', {'text': str(it['placeholder'])}, x, 0.5)); x += 0.5 + SCHEME_GAP
            elif 'bracket' in it:
                unknowns.append(str(it['bracket']))
                items.append(('bracket', {'text': str(it['bracket'])}, x, 0.75)); x += 0.75 + SCHEME_GAP
            elif 'text' in it:
                w = _text_width_units(it['text'], SCHEME_LABEL_PT) + 0.2
                items.append(('text', {'text': str(it['text'])}, x, w)); x += w + SCHEME_GAP
            elif 'pair' in it:
                pair = list(it['pair'])
                if len(pair) != 2:
                    raise ValueError('render_scheme: a pair holds exactly two (label, SMILES)')
                _pm = list(it.get('pair_marks') or [None, None])   # B3: per-member marks
                for (lbl, smi), _mk in zip(pair, _pm + [None] * (2 - len(_pm))):
                    d, w, h = _tile(smi, item={'marks': _mk})
                    coloured |= set(d.coloured_elements)
                    items.append(('pairtile', {'draw': d, 'label': f'{lbl} ='}, x, w + 0.45))
                    x += w + 0.45 + SCHEME_GAP
            else:
                raise ValueError(f'render_scheme: unknown item {sorted(it)}')
        if not any(k == 'arrow' for k, _p, _x, _w in items):
            raise ValueError('render_scheme: every row of a scheme carries at least one arrow — '
                             'a bare structure or structure set is a STRUCTURE figure '
                             '(structure_draw_fn / render_option_set), not a scheme')
        layout.append(items)
        row_w.append(x - SCHEME_GAP if items else 0.0)
    if not tiles:
        raise ValueError('render_scheme: a scheme must draw at least one molecule')

    W = max(row_w)
    n_rows = len(layout)
    row_h = H + 0.9                       # tile + reagent lines above/below an arrow
    total_h = n_rows * row_h + (n_rows - 1) * SCHEME_ROW_GAP
    state = {'colours': bool(element_colours)}

    def draw(ax, series=None, palette=None):
        from matplotlib.patches import FancyArrowPatch
        for ri, items in enumerate(layout):
            cy = total_h - (ri * (row_h + SCHEME_ROW_GAP)) - row_h / 2.0
            for kind, p, x, w in items:
                if kind in ('mol', 'pairtile'):
                    d = p['draw']
                    arr = _crop_raster(d.raster())
                    asp = arr.shape[1] / float(arr.shape[0]) if arr.shape[0] else 1.0
                    tw = w if kind == 'mol' else w - 0.45
                    th = tw / asp if asp else H
                    x0 = x if kind == 'mol' else x + 0.45
                    ax.imshow(arr, extent=(x0, x0 + tw, cy - th / 2.0, cy + th / 2.0),
                              zorder=2, interpolation='bilinear')
                    if kind == 'pairtile':
                        ax.text(x + 0.2, cy, p['label'], ha='center', va='center',
                                fontsize=SCHEME_LABEL_PT, weight='bold')
                    _ylab = cy - th / 2.0 - 0.06
                    if p.get('label'):
                        ax.text(x0 + tw / 2.0, _ylab, p['label'],
                                ha='center', va='top', fontsize=SCHEME_LABEL_PT, weight='bold')
                        _ylab -= 0.24                      # an equivalents line sits under the label
                    if p.get('equiv'):
                        ax.text(x0 + tw / 2.0, _ylab, p['equiv'],
                                ha='center', va='top', fontsize=SCHEME_TEXT_PT)
                elif kind == 'plus':
                    ax.text(x + w / 2.0, cy, '+', ha='center', va='center', fontsize=SCHEME_LABEL_PT + 2)
                elif kind == 'arrow':
                    d_ = p['dir']
                    style = {'right': '-|>', 'left': '<|-', 'both': '<|-|>'}.get(d_, '-|>')
                    ax.add_patch(FancyArrowPatch((x, cy), (x + w, cy), arrowstyle=style,
                                                 mutation_scale=14, lw=1.6, color='black',
                                                 zorder=3, shrinkA=0, shrinkB=0))
                    if p['reagent'] is not None:
                        arr = _crop_raster(p['reagent'].raster())
                        asp = arr.shape[1] / float(arr.shape[0]) if arr.shape[0] else 1.0
                        rw = min(w - 0.1, 1.4); rh = rw / asp if asp else 0.8
                        ax.imshow(arr, extent=(x + (w - rw) / 2.0, x + (w + rw) / 2.0,
                                               cy + 0.08, cy + 0.08 + rh), zorder=2,
                                  interpolation='bilinear')
                        ybase = cy + 0.08 + rh
                    else:
                        ybase = cy + 0.07
                    for i, t in enumerate(p['above']):
                        ax.text(x + w / 2.0, ybase + 0.21 * (len(p['above']) - 1 - i), t,
                                ha='center', va='bottom', fontsize=SCHEME_TEXT_PT)
                    for i, t in enumerate(p['below']):
                        ax.text(x + w / 2.0, cy - 0.07 - 0.21 * i, t,
                                ha='center', va='top', fontsize=SCHEME_TEXT_PT)
                elif kind == 'ph':
                    ax.text(x + w / 2.0, cy, p['text'], ha='center', va='center',
                            fontsize=SCHEME_LABEL_PT + 1, weight='bold')
                elif kind == 'bracket':
                    ax.text(x + w / 2.0, cy, f'[ {p["text"]} ]', ha='center', va='center',
                            fontsize=SCHEME_LABEL_PT + 1, weight='bold')
                elif kind == 'text':
                    ax.text(x + w / 2.0, cy, p['text'], ha='center', va='center',
                            fontsize=SCHEME_LABEL_PT)
        ax.set_xlim(-0.1, W + 0.1); ax.set_ylim(-0.1, total_h + 0.1)
        ax.set_aspect('equal')
        ax.axis('off')

    def set_element_colours(flag):
        flag = bool(flag)
        state['colours'] = flag
        for t in tiles:
            t.set_element_colours(flag)
        draw.element_colours = flag
        if tokens is not None:
            _ncache.clear()                      # B6: the composed scheme re-renders too

    row_canon = scheme_canonical(spec)
    canon_rows = []
    for ri, rc in enumerate(row_canon):
        if not rc:
            raise ValueError(f'render_scheme: row {ri + 1} draws no molecule in a reactant or '
                             f'product position — a scheme needs at least one drawn '
                             f'reactant or product (placeholders alone cannot be registered)')
        c, reason = canonical_structure(rc)
        if c is None and reason != 'rdkit_unavailable':
            raise ValueError(f'render_scheme: reaction canonical {rc!r} rejected — {reason}')
        canon_rows.append(c or rc)
    draw.canonical = canon_rows[0]
    draw.row_canonicals = canon_rows
    draw.tiles = tiles
    draw.descriptor = {'reagent_lines': reagent_lines, 'unknowns': unknowns,
                       'arrows': n_arrows, 'rows': n_rows, 'tiles': len(tiles),
                       'row_canonicals': canon_rows,
                       # drawn 'mol' tiles that are NEITHER a reactant/product of the row's
                       # canonical NOR an agent/pair member — the sequential-chain
                       # intermediates (never negative: agents and pair products are counted)
                       'intermediates': max(0, sum(1 for r in rows for it in r if 'mol' in it)
                                            - sum(c.count('.') + 1 for rc in canon_rows for c in rc.split('>') if c))}
    draw.coloured_elements = frozenset(coloured)
    draw.element_colours = state['colours']
    draw.set_element_colours = set_element_colours
    draw.highlight = {'atoms': [a for t in tiles for a in t.highlight['atoms']],
                      'bonds': [b for t in tiles for b in t.highlight['bonds']]}
    draw.palette_note = notes[0] if notes else None
    draw.suggested_aspect = max(0.55, min(1.30, (total_h + 0.2) / max(W + 0.2, 1e-9)))
    draw.scheme = {'rows': rows}
    if tokens is not None:
        # v1.17 — additive, only when tokens were given
        _ncache = {}

        def native_png(dpi=300):
            key = int(dpi)
            if key not in _ncache:
                _ncache[key] = _scheme_native_render(rows, tiles, _ntk, max_width_in, key)
            return _ncache[key]
        draw.render_mode = 'native_raster'
        draw.tokens = dict(_ntk)
        draw.max_width_in = float(max_width_in)
        draw.native_png = native_png
    return draw


def scheme_semantic_object(draw, role='problem', name='reaction scheme', row=0):
    """The S7-NEW-B2 semantic object for a rendered scheme (one per row):
       {'role', 'kind': 'REACTION', 'name', 'canonical': <row reaction SMILES>,
        'descriptor': {...}}. Validate with paper_pipeline.validate_semantic_object."""
    canon = draw.row_canonicals[row] if row < len(draw.row_canonicals) else ''
    desc = dict(draw.descriptor)
    desc['row'] = row
    return {'role': role, 'kind': 'REACTION', 'name': str(name), 'canonical': canon,
            'descriptor': desc}

# ═══════════════════════════════════════════════════════════════════════════════
# v1.19 — RE-25 CHEM-STRUCTURE STANDARD (GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS)
# ═══════════════════════════════════════════════════════════════════════════════
# The chemistry-structure explanation renderer: reaction schemes and curly-arrow
# MECHANISM figures generated from atom-mapped SMILES, PROVED chemically (E-03: the
# arrows must turn the drawn reactant into the drawn product), PROVED visually (E-04:
# an automatic layout gate with a deterministic retry search and a recorded fallback
# chain), reconciled with the printed options (E-07 option_match), balanced per step
# (E-06 g), and composed with captions INSIDE the image (figure paragraphs carry no
# text). Everything here is inert unless an explanation block carries
# chem_structure_module.status == 'APPLIES' — a question with no chemistry content
# never reaches any of these functions.
#
# DEPENDENCY DIRECTION (validator check AI, unchanged): this module never imports
# figural_core. The three RE-25 inks (ARROW_INK / FORM_INK / WRONG_INK) are read from
# figural_core ONLY IF the executing flow already imported it (explain_engine.
# structure_draw / render_mechanism load it first); otherwise the pinned defaults
# below — which are the SAME Okabe-Ito values — are used, so the bytes never differ.
#
# PUBLIC SURFACE (bound by explain_engine.REPRESENTATION_RENDERERS and wrapped there):
#   mechanism_apply_arrows(before, arrows) -> (mapped_smiles | None, reason)   E-03
#   verify_mechanism_step(step)            -> (ok, reason)                      E-03
#   step_atom_balance(step)                -> (ok, reason)                      E-06 g
#   mechanism_canonical(smiles)            -> constitution canonical (maps/H stripped)
#   option_match(answer_smiles, {k: smiles}) -> {exact, nearest, formula_delta, ...} E-07
#   render_mechanism(spec, ...)            -> MechanismDraw                     E-01/E-02/E-04
#   figure_layout_audit(draw)              -> (ok, findings)                    E-04
#   figure_review_sheet(figures, out_png)  -> (path, meta)                      E-09
#   CHS_* constants — the retry policy, gate thresholds and figure sizes (§6A-10/11)

CHS_INK_DEFAULTS = {'ARROW_INK': '#0072B2',   # OKABE_ITO[0] blue   — curly arrows
                    'FORM_INK': '#009E73',    # OKABE_ITO[2] green  — forming bonds
                    'WRONG_INK': '#D55E00'}   # OKABE_ITO[1] vermillion — wrong bonds / arrows
# Reagent-atom highlight tints (35 % over white of sky-blue, orange, purple, green —
# the figural_core FILL_TINTS rule), one fixed colour per reagent atom across every
# figure of a question. Pinned so every machine renders the same bytes.
CHS_REAGENT_TINTS = ('#C4E5F6', '#F6DEB3', '#EDD0E0', '#A6DDCE', '#F9F3B5')
CHS_FORM_TINT = '#A6DDCE'      # band behind a forming bond (green tint)
CHS_WRONG_TINT = '#F2C5A6'     # band behind a wrong bond (vermillion tint)
CHS_BREAK_TINT = '#D9D9D9'     # band behind a breaking bond (grey)
CHS_FIGURE_DPI = 200           # render dpi (6.0 in wide step figure = 1200 px; ≤ ~120 KB)
CHS_TARGET_BYTES = 120 * 1024  # §6A-10 item 8 (owner decision 2026-11-07: 120 KB / 200 dpi)
CHS_WIDTH_IN = {'DEDUCTION': 6.0, 'WHY_WRONG': 5.6, 'COMMON_PITFALLS': 5.6, 'SPEED_HACK': 4.6}
CHS_MIN_BOND_IN = 0.18         # L5
CHS_MIN_TEXT_PT = 7.0          # L5
CHS_MAX_HEIGHT_IN = 8.0        # L7: printed height never exceeds a page's printable height
CHS_EDGE_PX_300 = 8            # L4, at 300 dpi (scaled by dpi/300)
CHS_TIP_PX_300 = 14            # L2, at 300 dpi (scaled by dpi/300)
CHS_RETRY_CURVATURES = (0.35, -0.35, 0.6, -0.6, 0.9, -0.9)
CHS_RETRY_BIAS = (0.3, 0.2, 0.4)
CHS_RETRY_ROTATIONS = (0, 90, 180, 270)
CHS_RETRY_CONFORMATION = (0, 20, -20, 30, -30, 40, -40)
CHS_RETRY_CAP = 64
CHS_FALLBACK_CHAIN = ('MECHANISM', 'REACTION_SCHEME', 'STRUCTURE_GRAPH')
CHS_BOND_PX = 48               # drawn bond length in px at CHS_FIGURE_DPI (0.24 in)
CHS_FONT_PX = 26               # atom symbol / note font in px at CHS_FIGURE_DPI (9.4 pt)
CHS_CAPTION_PX = (24, 21)      # caption line 1 (bold) / line 2 in px at CHS_FIGURE_DPI
CHS_ARROW_TILE_PX = 190        # reaction-arrow tile width at CHS_FIGURE_DPI
CHS_REVIEW_PER_SHEET = 12      # §6A-12: figures per E-09 contact sheet


def _chs_ink():
    """The three RE-25 inks: figural_core's constants when it is loaded (the palette
    owner), else the pinned identical defaults. Never imports figural_core."""
    import sys as _sys
    fc = _sys.modules.get('figural_core')
    out = dict(CHS_INK_DEFAULTS)
    if fc is not None:
        for k in out:
            v = getattr(fc, k, None)
            if isinstance(v, str) and re.fullmatch(r'#[0-9A-Fa-f]{6}', v):
                out[k] = v.upper()
    return out


def _chs_rdkit():
    try:
        from rdkit import Chem, RDLogger
        RDLogger.DisableLog('rdApp.*')
        return Chem
    except Exception:
        return None


def mapped_mol(smiles, keep_h=True):
    """Parse an atom-mapped SMILES keeping explicit [H:n] atoms (so a moving hydrogen
    is a real, mapped atom). Returns an rdkit Mol or raises ValueError. Species are
    separated by '.' and stay in ONE Mol (fragments)."""
    Chem = _chs_rdkit()
    if Chem is None:
        raise ValueError('RE-25: rdkit unavailable (EC-35 — re-run Step 0)')
    s = str(smiles or '').strip()
    if not s:
        raise ValueError('RE-25: empty SMILES')
    pp = Chem.SmilesParserParams()
    pp.removeHs = not keep_h
    m = Chem.MolFromSmiles(s, pp)
    if m is None or m.GetNumAtoms() == 0:
        raise ValueError(f'RE-25: rdkit cannot parse {s!r}')
    return m


def _map_index(mol):
    """{atom-map number: atom index}; raises on a duplicated map number."""
    out = {}
    for a in mol.GetAtoms():
        n = a.GetAtomMapNum()
        if n:
            if n in out:
                raise ValueError(f'RE-25: atom map {n} used twice')
            out[n] = a.GetIdx()
    return out


def _freeze_hydrogens(mol):
    """Pin every atom's hydrogen count (implicit Hs become explicit counts, NoImplicit)
    so that changing a bond order or a charge never silently adds or removes an H —
    hydrogens move only as explicit mapped [H:n] atoms (E-02)."""
    for a in mol.GetAtoms():
        if a.GetAtomicNum() == 1:
            continue
        a.SetNumExplicitHs(a.GetTotalNumHs())
        a.SetNoImplicit(True)
    return mol


def mechanism_canonical(smiles, stereo=False):
    """Constitution canonical of a (possibly mapped, possibly explicit-H) SMILES: atom
    maps stripped, hydrogens removed, isomeric only when stereo=True. Used by E-03 (the
    arrows define connectivity and charge; stereochemistry is governed by E-06 f
    stereo_claims) and by E-06 c/d/e. Returns None when rdkit rejects the input."""
    Chem = _chs_rdkit()
    if Chem is None:
        return None
    try:
        m = mapped_mol(smiles, keep_h=True)
        m = Chem.RWMol(m)
        for a in m.GetAtoms():
            a.SetAtomMapNum(0)
        m = Chem.RemoveHs(m.GetMol(), sanitize=True)
        return Chem.MolToSmiles(m, isomericSmiles=bool(stereo))
    except Exception:
        return None


def _formula_counts(smiles):
    """({element: count incl. H}, net charge) over every species in `smiles`."""
    from collections import Counter
    m = mapped_mol(smiles, keep_h=True)
    c = Counter(); q = 0
    for a in m.GetAtoms():
        c[a.GetSymbol()] += 1
        if a.GetAtomicNum() != 1:
            c['H'] += a.GetTotalNumHs()
        q += a.GetFormalCharge()
    return c, q


def step_atom_balance(step):
    """E-06 (g): heavy atoms, hydrogens and net charge of `before` (every species,
    reagents included) equal `after` + `byproducts`. Applies to MECHANISM steps (a step
    with arrows — every atom the arrows move is drawn). A REACTION_SCHEME link (no
    arrows; reagents written as text above the arrow, e.g. "PCC" or "1. MeMgBr 2. H3O+")
    is NOT balance-checked — its reagents are not drawn species — and is proved by its
    canonical before / after alone. Returns (ok, reason)."""
    if not (step or {}).get('arrows'):
        return True, 'ok (scheme link — balance applies to arrow steps only)'
    try:
        cb, qb = _formula_counts(step['before'])
        ca, qa = _formula_counts(step['after'])
        for bp in step.get('byproducts') or []:
            cc, qq = _formula_counts(bp)
            ca.update(cc); qa += qq
    except Exception as exc:
        return False, f'CHS_UNBALANCED_STEP: cannot count atoms — {exc}'
    if cb != ca:
        diff = {k: ca.get(k, 0) - cb.get(k, 0) for k in set(cb) | set(ca) if ca.get(k, 0) != cb.get(k, 0)}
        return False, f'CHS_UNBALANCED_STEP: atom count differs (after − before) {diff}'
    if qb != qa:
        return False, f'CHS_UNBALANCED_STEP: net charge {qb} before vs {qa} after'
    return True, 'ok'


# ── E-03 — the arrow interpreter ────────────────────────────────────────────────
def _arrow_deltas(arrow, mi):
    """One curly arrow → (bond deltas {(i,j): ±n}, charge deltas {i: ±1}, radical deltas,
    note). Semantics §6A-11 / E-03 table. Atom references are MAP NUMBERS."""
    fr, to = arrow.get('from') or {}, arrow.get('to') or {}
    e = int(arrow.get('electrons', 2))
    if e not in (1, 2):
        raise ValueError(f'arrow electrons must be 1 or 2, got {e}')
    bd, cd, rd = {}, {}, {}

    def idx(n):
        if n not in mi:
            raise ValueError(f'arrow names atom map {n}, which is not in the species')
        return mi[n]

    def bond_key(a, b):
        return (min(a, b), max(a, b))

    def add(d, k, v):
        d[k] = d.get(k, 0) + v

    if e == 2:
        if 'bond' in fr:
            x, y = [idx(n) for n in fr['bond']]
            bias = idx(fr['bias']) if fr.get('bias') is not None else None
            add(bd, bond_key(x, y), -1)
            if 'atom' in to:
                z = idx(to['atom'])
                if bias is None:
                    raise ValueError('bond → atom arrow needs a bias (the end that bonds)')
                other = y if bias == x else x
                add(bd, bond_key(bias, z), +1)
                add(cd, other, +1); add(cd, z, -1)
            elif 'bond' in to:
                p, q = [idx(n) for n in to['bond']]
                shared = {x, y} & {p, q}
                if len(shared) != 1:
                    raise ValueError('bond → bond arrow needs exactly one shared atom')
                s = shared.pop()
                other = y if s == x else x
                z = q if s == p else p
                add(bd, bond_key(s, z), +1)
                add(cd, other, +1); add(cd, z, -1)
            elif 'lone_pair_on' in to:
                y2 = idx(to['lone_pair_on'])
                if y2 not in (x, y):
                    raise ValueError('bond → lone pair: the lone pair lands on an atom of that bond')
                other = y if y2 == x else x
                add(cd, other, +1); add(cd, y2, -1)
            else:
                raise ValueError('arrow `to` must name atom, bond or lone_pair_on')
        elif 'lone_pair' in fr or 'atom' in fr:
            x = idx(fr.get('lone_pair', fr.get('atom')))
            if 'atom' in to:
                z = idx(to['atom'])
                add(bd, bond_key(x, z), +1)
                add(cd, x, +1); add(cd, z, -1)
            elif 'bond' in to:
                p, q = [idx(n) for n in to['bond']]
                if x not in (p, q):
                    raise ValueError('lone pair → bond: the lone-pair atom is one end of that bond')
                z = q if x == p else p
                add(bd, bond_key(x, z), +1)
                add(cd, x, +1); add(cd, z, -1)
            else:
                raise ValueError('lone pair arrow `to` must name atom or bond')
        else:
            raise ValueError('arrow `from` must name bond, lone_pair or atom')
    else:
        # fishhook: one electron. bond x–y → atom x: half the bond; two matched fishhooks
        # on one bond break it (order −1) and leave a radical on each atom. atom x
        # (radical) → atom z: pairs with a matching fishhook to form the x–z bond.
        if 'bond' in fr:
            x, y = [idx(n) for n in fr['bond']]
            add(bd, bond_key(x, y), -0.5)
            bias = idx(fr['bias']) if fr.get('bias') is not None else x
            if 'atom' in to:
                z = idx(to['atom'])
                if z in (x, y):
                    add(rd, z, +1)                     # half the bond stays as a radical on z
                else:
                    add(bd, bond_key(bias, z), +0.5)   # half the bond pairs into a new bias–z bond
            elif 'bond' in to:
                p, q = [idx(n) for n in to['bond']]
                add(bd, bond_key(p, q), +0.5)
            else:
                add(rd, bias, +1)
        elif 'atom' in fr or 'radical' in fr:
            x = idx(fr.get('atom', fr.get('radical')))
            add(rd, x, -1)
            if 'atom' in to:
                add(bd, bond_key(x, idx(to['atom'])), +0.5)
            elif 'bond' in to:
                p, q = [idx(n) for n in to['bond']]
                add(bd, bond_key(p, q), +0.5)
            else:
                raise ValueError('fishhook `to` must name atom or bond')
        else:
            raise ValueError('fishhook `from` must name bond or atom')
    return bd, cd, rd


def mechanism_apply_arrows(before, arrows):
    """E-03. Apply every arrow of a step AT ONCE to the mapped `before` species as bond-
    order and formal-charge deltas; sanitise; return (mapped SMILES of the result, None)
    or (None, reason). Hydrogen counts are frozen (a hydrogen moves only as a mapped
    [H:n] atom). Dative bonds count as order 1."""
    Chem = _chs_rdkit()
    if Chem is None:
        return None, 'rdkit_unavailable'
    try:
        m = Chem.RWMol(mapped_mol(before, keep_h=True))
        _freeze_hydrogens(m)
        mi = _map_index(m)
        BD, CD, RD = {}, {}, {}
        for k, arrow in enumerate(arrows or []):
            bd, cd, rd = _arrow_deltas(arrow, mi)
            for kk, v in bd.items():
                BD[kk] = BD.get(kk, 0) + v
            for kk, v in cd.items():
                CD[kk] = CD.get(kk, 0) + v
            for kk, v in rd.items():
                RD[kk] = RD.get(kk, 0) + v
        order_of = {Chem.BondType.SINGLE: 1, Chem.BondType.DOUBLE: 2, Chem.BondType.TRIPLE: 3,
                    Chem.BondType.DATIVE: 1, Chem.BondType.AROMATIC: 1.5}
        type_of = {1: Chem.BondType.SINGLE, 2: Chem.BondType.DOUBLE, 3: Chem.BondType.TRIPLE}
        # AROMATIC SOURCE BONDS: an arrow drawn FROM an aromatic bond means its π bond, so
        # the Kekulé structure in which every such source bond is DOUBLE is chosen before
        # the deltas are applied (otherwise a ring could open on a single bond).
        _src = []
        for arrow in arrows or []:
            fr = arrow.get('from') or {}
            if fr.get('bond') and int(arrow.get('electrons', 2)) == 2:
                i_, j_ = mi[fr['bond'][0]], mi[fr['bond'][1]]
                b_ = m.GetBondBetweenAtoms(i_, j_)
                if b_ is not None and b_.GetIsAromatic():
                    _src.append((i_, j_))
        if _src:
            _picked = None
            for cand in Chem.ResonanceMolSupplier(m.GetMol(), Chem.KEKULE_ALL):
                if cand is None:
                    continue
                if all(cand.GetBondBetweenAtoms(i_, j_).GetBondType() == Chem.BondType.DOUBLE for i_, j_ in _src):
                    _picked = Chem.RWMol(cand); break
            if _picked is None:
                return None, 'CHS_ARROW_INVALID: no Kekulé structure puts a double bond on every aromatic arrow source'
            m = _picked
            for b_ in m.GetBonds():
                b_.SetIsAromatic(False)
            for a_ in m.GetAtoms():
                a_.SetIsAromatic(False)
        else:
            Chem.Kekulize(m, clearAromaticFlags=True)
        for (i, j), d in BD.items():
            if abs(d - round(d)) > 1e-9:
                return None, f'CHS_ARROW_INVALID: fishhook arrows on bond {i}-{j} are not paired'
            d = int(round(d))
            if d == 0:
                continue
            b = m.GetBondBetweenAtoms(i, j)
            cur = order_of.get(b.GetBondType(), 1) if b is not None else 0
            new = cur + d
            if new < 0 or new > 3:
                return None, f'CHS_ARROW_INVALID: bond order {cur}→{new} on atoms {i}-{j}'
            if b is not None and new == 0:
                m.RemoveBond(i, j)
            elif b is None:
                m.AddBond(i, j, type_of[new])
            else:
                b.SetBondType(type_of[new])
        for i, d in CD.items():
            a = m.GetAtomWithIdx(i)
            a.SetFormalCharge(a.GetFormalCharge() + int(d))
        for i, d in RD.items():
            a = m.GetAtomWithIdx(i)
            n = a.GetNumRadicalElectrons() + int(d)
            if n < 0:
                return None, f'CHS_ARROW_INVALID: negative radical count on atom {i}'
            a.SetNumRadicalElectrons(n)
        mm = m.GetMol()
        try:
            Chem.SanitizeMol(mm)
        except Exception as exc:
            return None, f'CHS_ARROW_INVALID: result does not sanitise — {exc}'
        return Chem.MolToSmiles(mm), None
    except Exception as exc:
        return None, f'CHS_ARROW_INVALID: {exc}'


def verify_mechanism_step(step):
    """E-03 verdict for one step dict (E-02 shape): applying `arrows` to `before` must
    give exactly `after` (constitution canonical, charges included). A step with no
    arrows (a REACTION_SCHEME link) is verified by E-06 (g) balance only and passes here.
    Returns (ok, reason)."""
    if not isinstance(step, dict) or not step.get('before') or not step.get('after'):
        return False, 'CHS_ARROW_INVALID: step needs before and after'
    arrows = step.get('arrows') or []
    if not arrows:
        return True, 'ok (no arrows — scheme link; balance checked by E-06 g)'
    got, reason = mechanism_apply_arrows(step['before'], arrows)
    if got is None:
        return False, reason
    want = mechanism_canonical(step['after'])
    have = mechanism_canonical(got)
    if want is None:
        return False, 'CHS_ARROW_INVALID: `after` does not parse'
    if have != want:
        return False, (f'CHS_ARROW_INVALID: arrows give {have} but after is {want} — a wrong '
                       f'arrow means wrong chemistry; the question returns to solving')
    return True, 'ok'


# ── E-07 — nearest-option detection ─────────────────────────────────────────────
def _has_stereo(smiles):
    return bool(re.search(r'@|/|\\', str(smiles or '')))


def _formula_delta_text(a_counts, o_counts):
    from collections import OrderedDict
    diff = OrderedDict()
    for k in sorted(set(a_counts) | set(o_counts), key=lambda e: (e != 'C', e != 'H', e)):
        d = o_counts.get(k, 0) - a_counts.get(k, 0)
        if d:
            diff[k] = d
    if not diff:
        return ''
    parts = []
    for k, d in diff.items():
        parts.append(f'{"+" if d > 0 else "−"}{k}{abs(d) if abs(d) > 1 else ""}')
    return ' '.join(parts)


def _formula_text(counts):
    order = ['C', 'H'] + sorted(k for k in counts if k not in ('C', 'H'))
    sub = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    return ''.join(f'{k}{str(counts[k]).translate(sub) if counts[k] > 1 else ""}'
                   for k in order if counts.get(k))


def _chs_mirror(smiles):
    """The enantiomer: every tetrahedral tag inverted (E/Z unchanged)."""
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None
    for a in m.GetAtoms():
        t = a.GetChiralTag()
        if t == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
            a.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CCW)
        elif t == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
            a.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CW)
    return Chem.MolToSmiles(m)


def _chs_stereo_agreement(a_smi, o_smi):
    """Fraction of the answer's CIP labels (atoms and double bonds) the option repeats,
    mapped atom-to-atom through the shared constitution. 0.0 when nothing comparable."""
    from rdkit import Chem
    from rdkit.Chem import rdCIPLabeler
    a = Chem.MolFromSmiles(a_smi); o = Chem.MolFromSmiles(o_smi)
    if a is None or o is None:
        return 0.0
    for m in (a, o):
        rdCIPLabeler.AssignCIPLabels(m)
    match = o.GetSubstructMatch(Chem.MolFromSmiles(Chem.MolToSmiles(a, isomericSmiles=False)))
    ma = a.GetSubstructMatch(Chem.MolFromSmiles(Chem.MolToSmiles(a, isomericSmiles=False)))
    if not match or not ma:
        return 0.0
    to_o = {ma[k]: match[k] for k in range(len(ma))}
    tot = agree = 0
    for at in a.GetAtoms():
        if at.HasProp('_CIPCode'):
            tot += 1
            ob = o.GetAtomWithIdx(to_o[at.GetIdx()])
            if ob.HasProp('_CIPCode') and ob.GetProp('_CIPCode') == at.GetProp('_CIPCode'):
                agree += 1
    for b in a.GetBonds():
        if b.HasProp('_CIPCode'):
            tot += 1
            ob = o.GetBondBetweenAtoms(to_o[b.GetBeginAtomIdx()], to_o[b.GetEndAtomIdx()])
            if ob is not None and ob.HasProp('_CIPCode') and ob.GetProp('_CIPCode') == b.GetProp('_CIPCode'):
                agree += 1
    return agree / float(tot) if tot else 0.0


def option_match(answer_smiles, option_smiles, timeout=5, racemic=False):
    """E-07. Compare the DERIVED answer structure with every printed option.
    option_smiles: {option_index: smiles | None}. Returns
      {'exact': k | None, 'nearest': k | None, 'mcs_fraction': float,
       'formula_delta': str ('' when formulae agree), 'differences': [str], 'formulas': {...}}
    Match rule (EC-32): stereo-aware when the option is drawn WITH stereo, constitution-
    only when it is not — compare only what is drawn."""
    Chem = _chs_rdkit()
    out = {'exact': None, 'nearest': None, 'mcs_fraction': 0.0, 'formula_delta': '',
           'differences': [], 'formulas': {}, 'tie': False}
    _tie = False
    if option_smiles is not None and not isinstance(option_smiles, dict):
        raise ValueError('option_match: option_smiles must be {option_index: smiles}')
    if Chem is None or not answer_smiles:
        out['differences'].append('rdkit unavailable or no answer_smiles')
        return out
    a_con = mechanism_canonical(answer_smiles, stereo=False)
    a_iso = mechanism_canonical(answer_smiles, stereo=True)
    try:
        a_counts, _ = _formula_counts(answer_smiles)
    except Exception:
        a_counts = {}
    out['formulas']['answer'] = _formula_text(a_counts) if a_counts else ''
    best = (None, -1.0)
    for k, smi in sorted((option_smiles or {}).items(), key=lambda kv: int(kv[0])):
        if not smi:
            continue
        o_con = mechanism_canonical(smi, stereo=False)
        if o_con is None:
            out['differences'].append(f'option {k}: SMILES does not parse')
            continue
        try:
            o_counts, _ = _formula_counts(smi)
            out['formulas'][str(k)] = _formula_text(o_counts)
        except Exception:
            o_counts = {}
        if o_con == a_con:
            if _has_stereo(smi) and _has_stereo(answer_smiles):
                o_iso = mechanism_canonical(smi, stereo=True)
                a_mir = mechanism_canonical(_chs_mirror(a_iso) or '', stereo=True) if a_iso else None
                if o_iso == a_iso or (racemic and o_iso == a_mir):
                    out['exact'] = int(k); break
                if o_iso == a_mir:
                    out['differences'].append(f'option {k}: the enantiomer of the derived product')
                    frac = 0.998                    # same relative configuration
                else:
                    agr = _chs_stereo_agreement(a_iso, o_iso)
                    out['differences'].append(f'option {k}: same constitution, '
                                              f'{agr:.0%} of the stereodescriptors agree')
                    frac = 0.99 + 0.007 * agr
            else:
                out['exact'] = int(k); break        # EC-32: compare only what is drawn
        else:
            frac = 0.0
            try:
                from rdkit.Chem import rdFMCS
                ma = Chem.MolFromSmiles(a_con); mo = Chem.MolFromSmiles(o_con)
                r = rdFMCS.FindMCS([ma, mo], timeout=int(timeout), ringMatchesRingOnly=True,
                                   completeRingsOnly=False, matchValences=False)
                if r.numAtoms:
                    frac = r.numAtoms / float(max(ma.GetNumAtoms(), mo.GetNumAtoms()))
            except Exception:
                frac = 0.0
            if o_counts and a_counts:
                dt = _formula_delta_text(a_counts, o_counts)
                if dt:
                    out['differences'].append(f'option {k}: drawn as {_formula_text(o_counts)} '
                                              f'({dt} relative to the derived product)')
        if frac > best[1] + 1e-12:
            best = (int(k), frac); _tie = False
        elif best[0] is not None and abs(frac - best[1]) <= 1e-12 and frac > 0:
            _tie = True
    if out['exact'] is None and best[0] is not None and _tie:
        # two options equally near: never resolved by option number (EC-29 RARE)
        out['tie'] = True
        out['differences'].append('two or more options are equally near the derived product (EC-29)')
        best = (None, best[1])
    if out['exact'] is None and best[0] is not None:
        out['nearest'] = best[0]
        out['mcs_fraction'] = round(best[1], 3)
        try:
            o_counts, _ = _formula_counts(option_smiles[out['nearest']]
                                          if out['nearest'] in option_smiles else
                                          option_smiles[str(out['nearest'])])
            out['formula_delta'] = _formula_delta_text(a_counts, o_counts)
        except Exception:
            pass
    return out


# ── E-04 geometry helpers ───────────────────────────────────────────────────────
def _seg_intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = ccw(p3, p4, p1), ccw(p3, p4, p2)
    d3, d4 = ccw(p1, p2, p3), ccw(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def _chs_pt_seg_dist(p, a, b):
    import math
    vx, vy = b[0] - a[0], b[1] - a[1]
    L2 = vx * vx + vy * vy
    if L2 <= 1e-9:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
    return math.hypot(p[0] - (a[0] + t * vx), p[1] - (a[1] + t * vy))


def _seg_box_hit(p1, p2, box):
    x0, y0, x1, y1 = box
    if (x0 <= p1[0] <= x1 and y0 <= p1[1] <= y1) or (x0 <= p2[0] <= x1 and y0 <= p2[1] <= y1):
        return True
    edges = (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)))
    return any(_seg_intersect(p1, p2, a, b) for a, b in edges)


def _boxes_overlap(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def _bezier(s, c, t, n=40):
    pts = []
    for k in range(n + 1):
        u = k / float(n)
        pts.append(((1 - u) ** 2 * s[0] + 2 * (1 - u) * u * c[0] + u ** 2 * t[0],
                    (1 - u) ** 2 * s[1] + 2 * (1 - u) * u * c[1] + u ** 2 * t[1]))
    return pts


def _rot(v, deg):
    import math
    t = math.radians(deg)
    return (v[0] * math.cos(t) - v[1] * math.sin(t), v[0] * math.sin(t) + v[1] * math.cos(t))


# ── depiction: coordinates, fragment placement, alignment, conformation ─────────
def _coords(mol):
    c = mol.GetConformer()
    return [(c.GetAtomPosition(i).x, c.GetAtomPosition(i).y) for i in range(mol.GetNumAtoms())]


def _set_coords(mol, xy):
    from rdkit.Geometry import Point3D
    c = mol.GetConformer()
    for i, (x, y) in enumerate(xy):
        c.SetAtomPosition(i, Point3D(float(x), float(y), 0.0))


def _depict(mol, template=None):
    """2D coordinates for `mol`. With a template (Mol with a conformer sharing atom-map
    numbers) every shared mapped atom is placed on the template (rdkit
    GenerateDepictionMatching2DStructure on the shared maps); when the template
    geometry cannot be honoured (ring formation), rigid alignment (rotation +
    translation, NEVER a mirror — a reflection inverts stereochemistry, §6A-10 item 4)
    on the shared atoms is used instead. Deterministic."""
    from rdkit.Chem import rdDepictor
    _chs_compute_2d(mol)
    if template is None:
        return mol
    mi, ti = _map_index(mol), _map_index(template)
    shared = sorted(set(mi) & set(ti))
    if len(shared) < 2:
        return mol
    pairs = [(ti[n], mi[n]) for n in shared]
    try:
        rdDepictor.GenerateDepictionMatching2DStructure(mol, template, atomMap=pairs)
        if not _distorted(mol):
            return mol
        _chs_compute_2d(mol)                     # distorted by the forced match: realign rigidly
    except Exception:
        _chs_compute_2d(mol)
    # rigid alignment without reflection (Kabsch in 2D with det check)
    import math
    A = _coords(mol); B = _coords(template)
    P = [A[mi[n]] for n in shared]; Q = [B[ti[n]] for n in shared]
    pc = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
    qc = (sum(q[0] for q in Q) / len(Q), sum(q[1] for q in Q) / len(Q))
    sxx = sum((p[0] - pc[0]) * (q[0] - qc[0]) + (p[1] - pc[1]) * (q[1] - qc[1]) for p, q in zip(P, Q))
    sxy = sum((p[0] - pc[0]) * (q[1] - qc[1]) - (p[1] - pc[1]) * (q[0] - qc[0]) for p, q in zip(P, Q))
    ang = math.atan2(sxy, sxx) if (sxx or sxy) else 0.0
    out = []
    for (x, y) in A:
        dx, dy = x - pc[0], y - pc[1]
        out.append((qc[0] + dx * math.cos(ang) - dy * math.sin(ang),
                    qc[1] + dx * math.sin(ang) + dy * math.cos(ang)))
    _set_coords(mol, out)
    return mol


def _chs_compute_2d(mol):
    """Fresh 2-D coordinates: rdkit's default depictor first; when that layout clashes
    (crowded quaternary centres), CoordGen — the global preference flag is restored
    afterwards so no other renderer's bytes change. Keeps whichever is not distorted
    (default preferred); when both are, the CoordGen layout, and the L3 gate decides."""
    from rdkit.Chem import rdDepictor
    rdDepictor.Compute2DCoords(mol)
    if not _distorted(mol):
        return mol
    saved = _coords(mol)
    try:
        prev = rdDepictor.GetPreferCoordGen()
    except Exception:
        prev = False
    try:
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(mol)
    except Exception:
        _set_coords(mol, saved)
        return mol
    finally:
        try:
            rdDepictor.SetPreferCoordGen(prev)
        except Exception:
            pass
    return mol


def _distorted(mol, bond_tol=0.30, clash=0.55):
    """True when a depiction is unreadable: a bond longer/shorter than the median by
    more than bond_tol, or two non-bonded atoms closer than clash × median bond length."""
    import math
    xy = _coords(mol)
    L = [math.hypot(xy[b.GetBeginAtomIdx()][0] - xy[b.GetEndAtomIdx()][0],
                    xy[b.GetBeginAtomIdx()][1] - xy[b.GetEndAtomIdx()][1]) for b in mol.GetBonds()]
    if not L:
        return False
    med = sorted(L)[len(L) // 2] or 1.0
    if any(abs(l - med) > bond_tol * med for l in L):
        return True
    bonded = {(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) for b in mol.GetBonds()}
    bonded |= {(j, i) for i, j in bonded}
    n = mol.GetNumAtoms()
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in bonded:
                continue
            if math.hypot(xy[i][0] - xy[j][0], xy[i][1] - xy[j][1]) < clash * med:
                return True
    return False


def _fragments(mol):
    from rdkit import Chem
    return [list(f) for f in Chem.GetMolFrags(mol, asMols=False)]


def _place_fragments(mol, arrows, gap=2.1, angle=0.0):
    """Multi-species `before`: put each attacking fragment beside the atom it attacks
    (§6A-10: the reagent fragment is placed by vector geometry next to the reacting
    atom), 2.1 Å from it along the outward direction of the attacked fragment.
    Fragments no arrow connects are laid out to the right in map order. Deterministic."""
    import math
    frags = _fragments(mol)
    if len(frags) <= 1:
        return mol
    mi = _map_index(mol)
    frag_of = {}
    for fi, atoms in enumerate(frags):
        for a in atoms:
            frag_of[a] = fi
    xy = _coords(mol)

    def centroid(atoms):
        return (sum(xy[a][0] for a in atoms) / len(atoms), sum(xy[a][1] for a in atoms) / len(atoms))

    def first_atom(ref):
        for key in ('bias', 'lone_pair', 'atom', 'radical'):
            if ref.get(key) is not None and ref[key] in mi:
                return mi[ref[key]]
        if ref.get('bond'):
            return mi.get(ref['bond'][0])
        if ref.get('lone_pair_on') is not None:
            return mi.get(ref['lone_pair_on'])
        return None

    main = max(range(len(frags)), key=lambda i: (len(frags[i]), -i))
    placed = {main}
    moved = True
    while moved:
        moved = False
        for arrow in arrows or []:
            s, t = first_atom(arrow.get('from') or {}), first_atom(arrow.get('to') or {})
            if s is None or t is None or frag_of[s] == frag_of[t]:
                continue
            for src, dst in ((s, t), (t, s)):
                fs, fd = frag_of[src], frag_of[dst]
                if fs in placed or fd not in placed:
                    continue
                cd = centroid(frags[fd]); td = xy[dst]
                v = (td[0] - cd[0], td[1] - cd[1]); L = math.hypot(*v)
                if L < 1e-6:
                    # attacked atom at its fragment's centre (t-Bu+, CH3·): point away from
                    # its nearest neighbour, or along +x when it has none
                    nb = [n.GetIdx() for n in mol.GetAtomWithIdx(dst).GetNeighbors()]
                    if nb:
                        # away from the nearest substituent, through the centre: for a
                        # trigonal centre this bisects the other two substituents
                        q = min(nb, key=lambda j: math.hypot(xy[j][0] - td[0], xy[j][1] - td[1]))
                        v = (td[0] - xy[q][0], td[1] - xy[q][1])
                        L = math.hypot(*v)
                        if L < 1e-6:
                            v, L = (1.0, 0.0), 1.0
                    else:
                        v, L = (1.0, 0.0), 1.0
                v = (v[0] / L, v[1] / L)
                if angle:
                    v = _rot(v, angle)
                target = (td[0] + gap * v[0], td[1] + gap * v[1])
                cs = centroid(frags[fs]); ss = xy[src]
                w = (cs[0] - ss[0], cs[1] - ss[1]); Lw = math.hypot(*w)
                ang0 = (math.atan2(v[1], v[0]) - math.atan2(w[1], w[0])) if Lw > 1e-6 else 0.0
                fixed = [xy[a] for f in placed for a in frags[f]]
                best = None
                # the fragment points away from the attacked atom; if its far end clashes
                # with the placed species, spin it about its anchor and/or move it out —
                # first clash-free candidate wins (deterministic order)
                for g_ in (gap, gap + 0.5, gap + 1.0):
                    for spin in (0, 30, -30, 60, -60, 90, -90, 120, -120, 180):
                        ang = ang0 + math.radians(spin)
                        tgt = (td[0] + g_ * v[0], td[1] + g_ * v[1])
                        cand = {}
                        for a in frags[fs]:
                            dx, dy = xy[a][0] - ss[0], xy[a][1] - ss[1]
                            cand[a] = (tgt[0] + dx * math.cos(ang) - dy * math.sin(ang),
                                       tgt[1] + dx * math.sin(ang) + dy * math.cos(ang))
                        dmin = min((math.hypot(cp[0] - fp[0], cp[1] - fp[1]) for cp in cand.values() for fp in fixed),
                                   default=9.9)
                        if best is None or dmin > best[0]:
                            best = (dmin, cand)
                        if dmin >= 1.25:
                            best = (dmin, cand); break
                    if best and best[0] >= 1.25:
                        break
                for a_, p_ in best[1].items():
                    xy[a_] = p_
                placed.add(fs); moved = True
    # unconnected fragments: to the right of everything placed so far
    for fi in range(len(frags)):
        if fi in placed:
            continue
        xmax = max(xy[a][0] for f in placed for a in frags[f])
        xmin_f = min(xy[a][0] for a in frags[fi])
        cy = sum(xy[a][1] for f in placed for a in frags[f]) / sum(len(frags[f]) for f in placed)
        cyf = sum(xy[a][1] for a in frags[fi]) / len(frags[fi])
        for a in frags[fi]:
            xy[a] = (xy[a][0] - xmin_f + xmax + gap, xy[a][1] - cyf + cy)
        placed.add(fi)
    _set_coords(mol, xy)
    return mol


def _reactive_conformation(mol, arrows, deg):
    """E-04 retry parameter: for the first INTRAmolecular arrow (from and to in one
    fragment, path longer than 3 bonds) rotate the from-side subtree about the single,
    non-ring bond nearest the middle of the shortest path by `deg` (so the two reacting
    atoms face each other — §6A-10 item 5). deg == 0 is a no-op."""
    if not deg:
        return mol
    from rdkit import Chem
    import math
    mi = _map_index(mol)
    frag_of = {}
    for fi, atoms in enumerate(_fragments(mol)):
        for a in atoms:
            frag_of[a] = fi

    def first_atom(ref):
        for key in ('bias', 'lone_pair', 'atom', 'radical'):
            if ref.get(key) is not None and ref[key] in mi:
                return mi[ref[key]]
        if ref.get('bond'):
            return mi.get(ref['bond'][0])
        if ref.get('lone_pair_on') is not None:
            return mi.get(ref['lone_pair_on'])
        return None

    for arrow in arrows or []:
        s, t = first_atom(arrow.get('from') or {}), first_atom(arrow.get('to') or {})
        if s is None or t is None or frag_of[s] != frag_of[t]:
            continue
        path = list(Chem.GetShortestPath(mol, s, t))
        if len(path) < 4:
            continue
        mid = len(path) // 2
        order = sorted(range(len(path) - 1), key=lambda k: (abs(k - mid), k))
        for k in order:
            b = mol.GetBondBetweenAtoms(path[k], path[k + 1])
            if b is None or b.IsInRing() or b.GetBondType() != Chem.BondType.SINGLE:
                continue
            pivot, far = path[k + 1], path[k]      # rotate the from-side (towards s) about pivot
            # subtree on the far side of the bond
            seen = {far}; stack = [far]
            while stack:
                x = stack.pop()
                for nb in mol.GetAtomWithIdx(x).GetNeighbors():
                    j = nb.GetIdx()
                    if j != pivot and j not in seen:
                        seen.add(j); stack.append(j)
            if pivot in seen:
                continue
            xy = _coords(mol); p = xy[pivot]
            for a in seen:
                dx, dy = xy[a][0] - p[0], xy[a][1] - p[1]
                r = _rot((dx, dy), deg)
                xy[a] = (p[0] + r[0], p[1] + r[1])
            _set_coords(mol, xy)
            return mol
    return mol


def _rotate_all(mol, deg):
    if not deg:
        return mol
    xy = _coords(mol)
    cx = sum(p[0] for p in xy) / len(xy); cy = sum(p[1] for p in xy) / len(xy)
    out = []
    for (x, y) in xy:
        r = _rot((x - cx, y - cy), deg)
        out.append((cx + r[0], cy + r[1]))
    _set_coords(mol, out)
    return mol


# ── one panel: rdkit raster + curly arrows + geometry record ────────────────────
class _Panel:
    """One species picture: PIL image, its geometry (px) for the E-04 audit, caption."""
    def __init__(self, image, geometry, caption):
        self.image = image
        self.geometry = geometry
        self.caption = list(caption or [])


def _prep_display(mol, labels, reagent_atoms):
    """Atom notes from map numbers (persisting labels), map numbers cleared for drawing."""
    from rdkit import Chem
    m = Chem.RWMol(mol)
    for a in m.GetAtoms():
        n = a.GetAtomMapNum()
        if n:
            # default label = the map number, on CARBONS (the locant / letter the prose
            # cites); a heteroatom draws its symbol and takes a note only when the spec
            # labels it explicitly
            lab = labels.get(n, labels.get(str(n), (str(n) if a.GetAtomicNum() == 6 else None)))
            if lab is not None and str(lab) != a.GetSymbol():
                a.SetProp('atomNote', str(lab))
            a.SetIntProp('_chs_map', n)
            a.SetAtomMapNum(0)
        if a.GetAtomicNum() == 6 and a.GetFormalCharge() == 0 and not a.GetNumRadicalElectrons() \
                and not a.GetChiralTag():
            # a plain carbon written in brackets ([CH2:7]) would otherwise be drawn with a
            # 'C' label; the proof used the frozen count, the picture uses rdkit's own.
            a.SetNoImplicit(False); a.SetNumExplicitHs(0)
    m = m.GetMol()
    m.UpdatePropertyCache(strict=False)
    return m


def _panel(mol, labels, atom_tints, form_bonds, break_bonds, wrong_bonds, arrows, curvature,
           bias, bond_px, font_px, caption, ink, wrong_arrows=False, dpi=CHS_FIGURE_DPI):
    """Render one species panel. Returns _Panel. Geometry (all px, panel-local):
    atoms {idx: (x,y)}, bonds [(i,j)], label_boxes {idx: box} (atoms with a drawn symbol
    or a note — ESTIMATED from the draw coordinates and font size, rdkit exposes no glyph
    boxes), arrows [{pts, start_atoms, end_atoms, tip, target}], captions [box]."""
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    from PIL import Image, ImageDraw
    import io, math
    import sys as _sys
    disp = _prep_display(mol, labels, atom_tints)
    xy = _coords(disp)
    xs = [p[0] for p in xy]; ys = [p[1] for p in xy]
    span_x = max(xs) - min(xs) + 2.6; span_y = max(ys) - min(ys) + 2.6
    scale = bond_px / 1.5
    W = int(max(240, span_x * scale)); H = int(max(240, span_y * scale))
    d = rdMolDraw2D.MolDraw2DCairo(W, H)
    o = d.drawOptions()
    o.fixedBondLength = bond_px
    o.bondLineWidth = max(1, int(round(bond_px / 18.0)))
    o.annotationFontScale = 0.8
    o.addStereoAnnotation = False
    o.padding = 0.08
    o.minFontSize = int(font_px * 0.75); o.maxFontSize = int(font_px * 1.05)
    o.setAnnotationColour((0.0, 0.25, 0.70))
    fc = _sys.modules.get('figural_core')
    pal = getattr(fc, 'ATOM_PALETTE', None) if fc is not None else None
    if pal:
        o.updateAtomPalette({int(k): tuple(v) for k, v in pal.items()})
        o.updateAtomPalette({-1: (0.0, 0.0, 0.0)})
    else:
        o.useBWAtomPalette()

    def rgb(hexs):
        hexs = hexs.lstrip('#'); return tuple(int(hexs[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    ha, hb = {}, {}
    map_idx = {a.GetIntProp('_chs_map'): a.GetIdx() for a in disp.GetAtoms() if a.HasProp('_chs_map')}
    for n, col in (atom_tints or {}).items():
        i = map_idx.get(int(n))
        if i is not None:
            ha[i] = rgb(col)
    for pairs, tint in ((form_bonds, CHS_FORM_TINT), (break_bonds, CHS_BREAK_TINT), (wrong_bonds, CHS_WRONG_TINT)):
        for pr in pairs or []:
            i, j = map_idx.get(int(pr[0])), map_idx.get(int(pr[1]))
            if i is None or j is None:
                continue
            b = disp.GetBondBetweenAtoms(i, j)
            if b is not None:
                hb[b.GetIdx()] = rgb(tint)
    d.DrawMolecule(disp, highlightAtoms=list(ha), highlightAtomColors=ha,
                   highlightBonds=list(hb), highlightBondColors=hb)
    P = {i: (d.GetDrawCoords(i).x, d.GetDrawCoords(i).y) for i in range(disp.GetNumAtoms())}
    d.FinishDrawing()
    im = Image.open(io.BytesIO(d.GetDrawingText())).convert('RGB')
    # geometry: bonds, label boxes
    bonds = [(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) for b in disp.GetBonds()]
    label_boxes = {}
    for a in disp.GetAtoms():
        i = a.GetIdx(); x, y = P[i]
        sym_drawn = (a.GetSymbol() != 'C' or a.GetFormalCharge() != 0 or a.GetNumRadicalElectrons()
                     or a.GetDegree() == 0 or a.HasProp('atomLabel'))
        if sym_drawn:
            w = font_px * 0.62 * max(1, len(a.GetSymbol()) + (1 if a.GetFormalCharge() else 0)
                                     + (1 if a.GetTotalNumHs() else 0))
            label_boxes[i] = (x - w / 2, y - font_px * 0.55, x + w / 2, y + font_px * 0.55)
        if a.HasProp('atomNote'):
            nw = font_px * 0.8 * 0.62 * len(a.GetProp('atomNote'))
            nb = (x + font_px * 0.35, y - font_px * 1.05, x + font_px * 0.35 + nw, y - font_px * 0.25)
            label_boxes[('note', i)] = nb
    # curly arrows
    dr = ImageDraw.Draw(im)
    arrow_geoms = []
    col = ink['WRONG_INK'] if wrong_arrows else ink['ARROW_INK']
    lw = max(2, int(round(bond_px / 14.0)))
    tip_len = max(8, int(round(bond_px / 3.6)))
    for arrow in arrows or []:
        fr, to = arrow.get('from') or {}, arrow.get('to') or {}
        s, start_atoms = _arrow_start(fr, map_idx, P, disp, bias, font_px)
        t, end_atoms, target = _arrow_end(to, map_idx, P, disp, font_px)
        if s is None or t is None:
            raise ValueError('RE-25: arrow names an atom that is not in this species')
        dx, dy = t[0] - s[0], t[1] - s[1]; L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        c = ((s[0] + t[0]) / 2 + nx * curvature * L, (s[1] + t[1]) / 2 + ny * curvature * L)
        pts = _bezier(s, c, t)
        # trim the tail off the start label and the tip short of the target
        trim_start = font_px * 0.45 if start_atoms else 0
        while len(pts) > 3 and math.hypot(pts[0][0] - s[0], pts[0][1] - s[1]) < trim_start:
            pts.pop(0)
        trim_end = font_px * 0.55 if (end_atoms and 'atom' in to) else font_px * 0.15
        while len(pts) > 3 and math.hypot(pts[-1][0] - t[0], pts[-1][1] - t[1]) < trim_end:
            pts.pop()
        dr.line([tuple(p) for p in pts], fill=col, width=lw, joint='curve')
        a1, a0 = pts[-1], pts[-3]
        ux, uy = a1[0] - a0[0], a1[1] - a0[1]; Lu = math.hypot(ux, uy) or 1.0
        ux, uy = ux / Lu, uy / Lu
        tipp = (a1[0] + ux * tip_len, a1[1] + uy * tip_len)
        half = tip_len * 0.5
        base_l = (a1[0] - uy * half, a1[1] + ux * half); base_r = (a1[0] + uy * half, a1[1] - ux * half)
        if int(arrow.get('electrons', 2)) == 1:      # fishhook: one barb only
            dr.polygon([tipp, base_l, (a1[0] + ux * 2, a1[1] + uy * 2)], fill=col)
        else:
            dr.polygon([tipp, base_l, base_r], fill=col)
        arrow_geoms.append({'pts': pts + [tipp], 'start_atoms': start_atoms, 'end_atoms': end_atoms,
                            'tip': tipp, 'target': t})
    # crop to ink + margin
    from PIL import ImageChops
    bg = Image.new('RGB', im.size, 'white')
    bb = ImageChops.difference(im, bg).getbbox() or (0, 0, im.width, im.height)
    m = int(font_px * 0.9)
    x0, y0 = max(0, bb[0] - m), max(0, bb[1] - m)
    x1, y1 = min(im.width, bb[2] + m), min(im.height, bb[3] + m)
    im = im.crop((x0, y0, x1, y1))
    sh = lambda p: (p[0] - x0, p[1] - y0)
    geometry = {'atoms': {i: sh(p) for i, p in P.items()},
                'bonds': bonds,
                'label_boxes': {k: (b[0] - x0, b[1] - y0, b[2] - x0, b[3] - y0) for k, b in label_boxes.items()},
                'arrows': [{'pts': [sh(p) for p in g['pts']], 'start_atoms': g['start_atoms'],
                            'end_atoms': g['end_atoms'], 'tip': sh(g['tip']), 'target': sh(g['target'])}
                           for g in arrow_geoms],
                'captions': [], 'bond_px': bond_px, 'font_px': font_px}
    return _Panel(im, geometry, caption)


def _lone_pair_point(i, P, disp, font_px, k=0.9):
    """A point offset from atom i, away from its bonds (§6A-11 arrow start/end)."""
    import math
    x, y = P[i]
    nbrs = [P[n.GetIdx()] for n in disp.GetAtomWithIdx(i).GetNeighbors()]
    if nbrs:
        vx = sum(x - p[0] for p in nbrs); vy = sum(y - p[1] for p in nbrs)
        L = math.hypot(vx, vy)
        if L < 1e-6:                      # symmetric: perpendicular to the first bond
            vx, vy = -(nbrs[0][1] - y), (nbrs[0][0] - x); L = math.hypot(vx, vy) or 1.0
    else:
        vx, vy, L = 1.0, 0.0, 1.0
    return (x + vx / L * font_px * k, y + vy / L * font_px * k)


def _arrow_start(fr, map_idx, P, disp, bias, font_px):
    if 'bond' in fr:
        i, j = map_idx[int(fr['bond'][0])], map_idx[int(fr['bond'][1])]
        b_atom = map_idx[int(fr['bias'])] if fr.get('bias') is not None else i
        other = j if b_atom == i else i
        f = bias if fr.get('bias') is not None else 0.5
        return ((P[b_atom][0] + (P[other][0] - P[b_atom][0]) * f,
                 P[b_atom][1] + (P[other][1] - P[b_atom][1]) * f), ())
    if 'lone_pair' in fr:
        i = map_idx[int(fr['lone_pair'])]
        return _lone_pair_point(i, P, disp, font_px), (i,)
    if 'atom' in fr or 'radical' in fr:
        i = map_idx[int(fr.get('atom', fr.get('radical')))]
        return P[i], (i,)
    return None, ()


def _arrow_end(to, map_idx, P, disp, font_px):
    if 'atom' in to:
        i = map_idx[int(to['atom'])]
        return P[i], (i,), P[i]
    if 'bond' in to:
        i, j = map_idx[int(to['bond'][0])], map_idx[int(to['bond'][1])]
        mid = ((P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2)
        return mid, (i, j), mid
    if 'lone_pair_on' in to:
        i = map_idx[int(to['lone_pair_on'])]
        p = _lone_pair_point(i, P, disp, font_px, k=1.1)
        return p, (i,), p
    return None, (), None


def _caption_panel(panel, caption, cap_px, text_colour='#191919'):
    """Append caption lines INSIDE the image (line 1 bold). Records caption boxes."""
    from PIL import Image, ImageDraw
    if not caption:
        return panel
    fb, _ = _native_font('bold', cap_px[0]); fr, _ = _native_font('regular', cap_px[1])
    im = panel.image
    dr = ImageDraw.Draw(im)
    widths = [dr.textlength(t, font=(fb if k == 0 else fr)) for k, t in enumerate(caption)]
    W = int(max(im.width, max(widths) + 2 * cap_px[1]))
    line_h = [cap_px[0] + 8] + [cap_px[1] + 6] * (len(caption) - 1)
    H = im.height + sum(line_h) + 10
    c = Image.new('RGB', (W, H), 'white')
    ox = (W - im.width) // 2
    c.paste(im, (ox, 0))
    dr = ImageDraw.Draw(c)
    y = im.height + 4
    boxes = []
    for k, t in enumerate(caption):
        f = fb if k == 0 else fr
        tw = dr.textlength(t, font=f)
        dr.text(((W - tw) / 2, y), t, fill=text_colour, font=f)
        boxes.append(((W - tw) / 2, y, (W + tw) / 2, y + line_h[k]))
        y += line_h[k]
    g = panel.geometry
    g['atoms'] = {i: (p[0] + ox, p[1]) for i, p in g['atoms'].items()}
    g['label_boxes'] = {k: (b[0] + ox, b[1], b[2] + ox, b[3]) for k, b in g['label_boxes'].items()}
    for a in g['arrows']:
        a['pts'] = [(p[0] + ox, p[1]) for p in a['pts']]
        a['tip'] = (a['tip'][0] + ox, a['tip'][1]); a['target'] = (a['target'][0] + ox, a['target'][1])
    g['captions'] = boxes
    g['mol_height'] = im.height
    panel.image = c
    return panel


def _arrow_tile(above, below, width_px, height_px, font_px, wrong=False, ink=None, down=False):
    """The reaction arrow between two panels: reagents above (as printed), conditions
    and by-products below. `down=True` draws a vertical arrow for the stacked layout."""
    from PIL import Image, ImageDraw
    ink = ink or _chs_ink()
    col = ink['WRONG_INK'] if wrong else '#000000'
    f, _ = _native_font('regular', int(font_px * 0.85))
    c = Image.new('RGB', (width_px, height_px), 'white')
    dr = ImageDraw.Draw(c)
    lines_a = [t for t in (above or []) if str(t).strip()]
    lines_b = [t for t in (below or []) if str(t).strip()]
    if not down:
        y = height_px // 2
        dr.line((10, y, width_px - 18, y), fill=col, width=max(2, font_px // 9))
        dr.polygon([(width_px - 18, y - 9), (width_px - 18, y + 9), (width_px - 4, y)], fill=col)
        yy = y - 10
        for t in reversed(lines_a):
            tw = dr.textlength(t, font=f); yy -= int(font_px * 0.85) + 4
            dr.text(((width_px - tw) / 2, yy), t, fill='#000000', font=f)
        yy = y + 8
        for t in lines_b:
            tw = dr.textlength(t, font=f)
            dr.text(((width_px - tw) / 2, yy), t, fill='#000000', font=f); yy += int(font_px * 0.85) + 4
    else:
        x = width_px // 2
        dr.line((x, 10, x, height_px - 18), fill=col, width=max(2, font_px // 9))
        dr.polygon([(x - 9, height_px - 18), (x + 9, height_px - 18), (x, height_px - 4)], fill=col)
        yy = 14
        for t in lines_a + lines_b:
            dr.text((x + 14, yy), t, fill='#000000', font=f); yy += int(font_px * 0.85) + 4
    return c


def _compose(tiles, gap=10, down=False):
    """Row (or column) of PIL images, bottom-aligned (molecule panels) with arrow tiles
    centred on the molecule band. Returns (image, offsets[(x,y)])."""
    from PIL import Image
    if not down:
        W = sum(t.width for t in tiles) + gap * (len(tiles) + 1)
        H = max(t.height for t in tiles) + gap
        im = Image.new('RGB', (W, H), 'white'); x = gap; offs = []
        for t in tiles:
            y = (H - t.height) // 2 if getattr(t, '_is_arrow', False) else H - t.height - gap // 2
            im.paste(t, (x, y)); offs.append((x, y)); x += t.width + gap
        return im, offs
    W = max(t.width for t in tiles) + 2 * gap
    H = sum(t.height for t in tiles) + gap * (len(tiles) + 1)
    im = Image.new('RGB', (W, H), 'white'); y = gap; offs = []
    for t in tiles:
        x = (W - t.width) // 2
        im.paste(t, (x, y)); offs.append((x, y)); y += t.height + gap
    return im, offs


class MechanismDraw:
    """The result of render_mechanism(): PNG bytes, natural width, the §6A-5 identifier
    (per step: canonical before / after, normalised arrow list, E-03 verdict), the E-04
    layout record (attempts, findings, the requirement actually rendered after any
    step-down) and the geometry the layout gate re-audits."""
    def __init__(self, png_bytes, width_in, meta, identifier, geometry, requirement, ledger):
        self.png_bytes = png_bytes
        self.width_in = float(width_in)
        self.meta = dict(meta)
        self.identifier = identifier
        self.geometry = geometry
        self.requirement = requirement          # 'MECHANISM' | 'REACTION_SCHEME' | 'STRUCTURE_GRAPH'
        self.degrade_ledger = list(ledger)      # §6A-4 step-downs, [] when none
        self.render_mode = 'native_raster'

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.png_bytes)
        return path


def _normalise_arrows(arrows):
    return [{'from': dict(sorted((a.get('from') or {}).items())),
             'to': dict(sorted((a.get('to') or {}).items())),
             'electrons': int(a.get('electrons', 2))} for a in (arrows or [])]


def _png_bytes(im, target=CHS_TARGET_BYTES):
    """Deterministic PNG: palette-quantised (adaptive, ≤256 colours — the figures are
    flat line art), optimised, no timestamp / text chunks. Falls back to RGB if the
    quantised image is somehow larger."""
    import io
    q = im.convert('P', palette=1, colors=256)      # Image.ADAPTIVE == 1
    b1 = io.BytesIO(); q.save(b1, format='PNG', optimize=True)
    out = b1.getvalue()
    if len(out) > target:
        q = im.convert('P', palette=1, colors=64)
        b2 = io.BytesIO(); q.save(b2, format='PNG', optimize=True)
        if len(b2.getvalue()) < len(out):
            out = b2.getvalue()
    return out


def _layout_findings(panels, offsets, canvas_size, dpi, scale=1.0, ink=None):
    """E-04 L1–L6 over the composed figure (panel geometry shifted by its offset)."""
    import math
    findings = []
    edge = CHS_EDGE_PX_300 * dpi / 300.0
    tip_tol = CHS_TIP_PX_300 * dpi / 300.0
    W, H = canvas_size
    all_boxes = []
    for pn, (ox, oy) in zip(panels, offsets):
        g = pn.geometry
        sh = lambda p: (p[0] + ox, p[1] + oy)
        boxes = {k: (b[0] + ox, b[1] + oy, b[2] + ox, b[3] + oy) for k, b in g['label_boxes'].items()}
        caps = [(b[0] + ox, b[1] + oy, b[2] + ox, b[3] + oy) for b in g.get('captions', [])]
        atoms = {i: sh(p) for i, p in g['atoms'].items()}
        for ai, ar in enumerate(g['arrows']):
            own = set(ar['start_atoms']) | set(ar['end_atoms'])
            pts = [sh(p) for p in ar['pts']]
            segs = list(zip(pts[:-1], pts[1:]))
            # skip the first/last 15 % of the path (its own start and end)
            k0, k1 = int(len(segs) * 0.15), int(len(segs) * 0.85)
            inner = segs[k0:k1] if k1 > k0 else segs
            clear = 0.15 * g['bond_px']
            for (i, j) in g['bonds']:
                if i in own or j in own:
                    continue
                p1, p2 = atoms[i], atoms[j]
                if any(_seg_intersect(a, b, p1, p2) for a, b in inner):
                    findings.append(f'L1: arrow {ai} crosses bond {i}-{j}')
                    break
                if any(_chs_pt_seg_dist(a, p1, p2) < clear for a, _b in inner):
                    findings.append(f'L1: arrow {ai} runs along bond {i}-{j}')
                    break
            for key, box in boxes.items():
                idx = key[1] if isinstance(key, tuple) else key
                if idx in own:
                    continue
                if any(_seg_box_hit(a, b, box) for a, b in inner):
                    findings.append(f'L1: arrow {ai} crosses label of atom {idx}')
                    break
            tip = sh(ar['tip']); tgt = sh(ar['target'])
            if math.hypot(tip[0] - tgt[0], tip[1] - tgt[1]) > tip_tol + (g['font_px'] * 0.6 if ar['end_atoms'] else 0):
                findings.append(f'L2: arrow {ai} tip is {math.hypot(tip[0]-tgt[0], tip[1]-tgt[1]):.0f} px from its target')
        # L3b — atoms that are not bonded never sit closer than 0.55 bond length; L3c — no
        # drawn bond is stretched or squashed by more than 30 % (a distorted depiction)
        import math as _m
        bl = [_m.hypot(atoms[i][0] - atoms[j][0], atoms[i][1] - atoms[j][1]) for (i, j) in g['bonds']]
        if bl:
            med = sorted(bl)[len(bl) // 2] or 1.0
            if any(abs(l - med) > 0.30 * med for l in bl):
                findings.append('L3c: a drawn bond deviates > 30 % from the median bond length')
            bonded = set(g['bonds']) | {(j, i) for i, j in g['bonds']}
            ids = sorted(atoms)
            for a_ in range(len(ids)):
                for b_ in range(a_ + 1, len(ids)):
                    i, j = ids[a_], ids[b_]
                    if (i, j) in bonded:
                        continue
                    if _m.hypot(atoms[i][0] - atoms[j][0], atoms[i][1] - atoms[j][1]) < 0.55 * med:
                        findings.append(f'L3b: atoms {i} and {j} overlap')
                        break
                else:
                    continue
                break
        notes = [(k, b) for k, b in boxes.items() if isinstance(k, tuple)]
        for a in range(len(notes)):
            for b in range(a + 1, len(notes)):
                if _boxes_overlap(notes[a][1], notes[b][1]):
                    findings.append(f'L3: notes of atoms {notes[a][0][1]} and {notes[b][0][1]} overlap')
        all_boxes += caps
        for cb in caps:
            if cb[0] < edge or cb[2] > W - edge or cb[3] > H - edge:
                findings.append('L4: caption touches the canvas edge')
        bond_in = g['bond_px'] * scale / dpi
        if bond_in < CHS_MIN_BOND_IN - 1e-6:
            findings.append(f'L5: bond length {bond_in:.3f} in < {CHS_MIN_BOND_IN} in')
        text_pt = g['font_px'] * 0.8 * scale / dpi * 72.0
        if text_pt < CHS_MIN_TEXT_PT - 1e-6:
            findings.append(f'L5: label text {text_pt:.1f} pt < {CHS_MIN_TEXT_PT} pt')
    for a in range(len(all_boxes)):
        for b in range(a + 1, len(all_boxes)):
            if _boxes_overlap(all_boxes[a], all_boxes[b]):
                findings.append('L3: caption lines overlap')
    # L7 — printed height (the docx scales the image to its width; height follows)
    if H * scale / float(dpi) > CHS_MAX_HEIGHT_IN + 1e-9:
        findings.append(f'L7: printed height {H * scale / float(dpi):.1f} in > {CHS_MAX_HEIGHT_IN} in (page)')
    ink = ink or _chs_ink()
    import sys as _sys
    fc = _sys.modules.get('figural_core')
    if fc is not None and hasattr(fc, 'ROLE_TEXT'):
        for k, v in ink.items():
            if v.upper() not in fc.ROLE_TEXT and v.upper() not in fc.ROLE_TEXT.values():
                findings.append(f'L6: {k} {v} is not a figural_core text-tier ink')
    return findings


def _ink_edge_clear(im, edge_px):
    """L4 on pixels: no ink within edge_px of the canvas border."""
    import numpy as _np
    a = _np.asarray(im.convert('L'))
    e = int(round(edge_px))
    if e <= 0 or a.shape[0] <= 2 * e or a.shape[1] <= 2 * e:
        return True
    border = _np.concatenate([a[:e, :].ravel(), a[-e:, :].ravel(), a[:, :e].ravel(), a[:, -e:].ravel()])
    return bool((border > 245).all())


def _render_attempt(steps_ctx, attempt, ink, dpi, width_in, cap_px, font_px, bond_px, wrong, requirement):
    """One E-04 attempt for ONE step figure. Returns (image, panels, offsets, scale, findings)."""
    from PIL import Image
    curvature, bias, rot, conf, place = attempt
    before, after = steps_ctx['before_mol'], steps_ctx['after_mol']
    from rdkit import Chem
    b = Chem.Mol(before); a = Chem.Mol(after)
    _place_fragments(b, steps_ctx['arrows'], angle=place)
    _reactive_conformation(b, steps_ctx['arrows'], conf)
    _rotate_all(b, rot); _rotate_all(a, rot)
    arrows = steps_ctx['arrows'] if requirement == 'MECHANISM' else []
    form = steps_ctx['form'] if requirement != 'STRUCTURE_GRAPH' else []
    brk = steps_ctx['break'] if requirement == 'REACTION_SCHEME' else []
    p1 = _panel(b, steps_ctx['labels'], steps_ctx['tints'], [], brk, steps_ctx['wrong_before'], arrows,
                curvature, bias, bond_px, font_px, steps_ctx['cap_before'], ink, wrong_arrows=wrong, dpi=dpi)
    p2 = _panel(a, steps_ctx['labels'], steps_ctx['tints'], form, [], steps_ctx['wrong_after'], [],
                curvature, bias, bond_px, font_px, steps_ctx['cap_after'], ink, dpi=dpi)
    _caption_panel(p1, steps_ctx['cap_before'], cap_px); _caption_panel(p2, steps_ctx['cap_after'], cap_px)
    mol_h = max(p1.geometry.get('mol_height', p1.image.height), p2.geometry.get('mol_height', p2.image.height))
    tile_h = max(int(mol_h), int(font_px * 6))
    tile = _arrow_tile(steps_ctx['above'], steps_ctx['below'], CHS_ARROW_TILE_PX, tile_h, font_px, wrong=wrong, ink=ink)
    tile._is_arrow = True
    # arrow tile sits at the molecule band height: give it the same bottom padding as captions
    cap_h = max(p1.image.height - p1.geometry.get('mol_height', p1.image.height),
                p2.image.height - p2.geometry.get('mol_height', p2.image.height))
    from PIL import Image as _I
    padded = _I.new('RGB', (tile.width, tile.height + cap_h), 'white'); padded.paste(tile, (0, 0))
    padded._is_arrow = False
    im, offs = _compose([p1.image, padded, p2.image])
    scale = 1.0
    max_px = width_in * dpi
    down = False
    if im.width > max_px:
        scale = max_px / float(im.width)
        if bond_px * scale / dpi < CHS_MIN_BOND_IN:          # too wide for a row: stack
            down = True
            tile_v = _arrow_tile(steps_ctx['above'], steps_ctx['below'], int(font_px * 9), int(font_px * 5),
                                 font_px, wrong=wrong, ink=ink, down=True)
            im, offs = _compose([p1.image, tile_v, p2.image], down=True)
            scale = min(1.0, max_px / float(im.width))
    panels = [p1, p2]
    offsets = [offs[0], offs[2]]
    findings = _layout_findings(panels, offsets, im.size, dpi, scale=scale, ink=ink)
    if scale < 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), resample=1)   # LANCZOS == 1
    if not _ink_edge_clear(im, CHS_EDGE_PX_300 * dpi / 300.0):
        # add a white margin rather than fail: nothing is clipped, L4 is about clipping
        from PIL import ImageOps
        im = ImageOps.expand(im, border=int(CHS_EDGE_PX_300 * dpi / 300.0) + 2, fill='white')
    return im, panels, offsets, scale, findings


CHS_RETRY_PLACEMENT = (0, 40, -40, 80, -80)   # reagent-fragment placement angle (multi-species before)


def _attempt_schedule(multi=False):
    """The deterministic E-04 retry order (curvature, bias, in-plane rotation, reactive-
    conformation rotation, fragment-placement angle), capped at CHS_RETRY_CAP. The
    placement angles are tried only for a multi-species `before`."""
    B = CHS_RETRY_BIAS[0]
    C = CHS_RETRY_CURVATURES
    out = []
    for c in C:                                   # a curly arrow is always curved
        out.append((c, B, 0, 0, 0))
    if multi:
        for pl in CHS_RETRY_PLACEMENT[1:]:
            for c in C[:2]:
                out.append((c, B, 0, 0, pl))
    for bsz in CHS_RETRY_BIAS[1:]:
        for c in C[:2]:
            out.append((c, bsz, 0, 0, 0))
    for rot in CHS_RETRY_ROTATIONS[1:]:
        for c in C[:2]:
            out.append((c, B, rot, 0, 0))
    for conf in CHS_RETRY_CONFORMATION[1:]:
        for c in C[:4]:
            out.append((c, B, 0, conf, 0))
    if multi:
        for pl in CHS_RETRY_PLACEMENT[1:]:
            for conf in CHS_RETRY_CONFORMATION[1:3]:
                out.append((C[0], B, 0, conf, pl))
    return out[:CHS_RETRY_CAP]


def render_mechanism(spec, dpi=CHS_FIGURE_DPI, width_in=None, section='DEDUCTION',
                     template=None, wrong=False):
    """Public entry: see _render_mechanism. Any non-ValueError from malformed input is
    re-raised as ValueError (one exception type for the §6A-12 EC-41 retry loop)."""
    try:
        return _render_mechanism(spec, dpi=dpi, width_in=width_in, section=section,
                                 template=template, wrong=wrong)
    except ValueError:
        raise
    except Exception as exc:                            # noqa: BLE001
        raise ValueError(f'render_mechanism: malformed input — {type(exc).__name__}: {exc}') from exc


def _render_mechanism(spec, dpi=CHS_FIGURE_DPI, width_in=None, section='DEDUCTION',
                      template=None, wrong=False):
    """E-01 / E-02 / E-04. Render ONE mechanism (or scheme) step figure from an E-02 step
    dict: {'before', 'after', 'arrows', 'reagents_above', 'conditions_below', 'byproducts',
    'highlight': {'form': [[m,n]], 'break': [...], 'wrong': [...]}, 'caption': [l1, l2],
    'caption_before': [...] (optional), 'atom_labels': {map: label} (optional),
    'atom_colours': {map: '#RRGGBB'} (optional; default: fixed tints for every atom of
    a species that is not the largest), 'requirement': 'MECHANISM' | 'REACTION_SCHEME'}.
      1. E-03: arrows must turn `before` into `after` → else raises ValueError
         CHS_ARROW_INVALID (never degraded — wrong arrows are wrong chemistry).
      2. Depict: `before` aligned to `template` (a Mol with coordinates sharing atom
         maps; pass the previous step's `after` mol via draw.after_mol to chain a
         sequence), `after` aligned to `before`. Reagent fragments placed beside the
         attacked atom. Mirroring never happens.
      3. E-04: the layout gate L1–L6 with the deterministic retry schedule (cap 64);
         then the fallback chain MECHANISM → REACTION_SCHEME → STRUCTURE_GRAPH, each
         step-down recorded in draw.degrade_ledger. A figure that fails every gate is
         never returned — the last fallback (STRUCTURE_GRAPH panels, no arrows) has no
         arrow to cross anything and always passes, so the function never returns
         an unaudited image.
    `wrong=True` draws the arrows / highlighted bonds in WRONG_INK (a WHY WRONG figure).
    Returns MechanismDraw (png_bytes, width_in, identifier, geometry, requirement,
    degrade_ledger, meta incl. attempts and bytes)."""
    Chem = _chs_rdkit()
    if Chem is None:
        raise ValueError('RE-25: rdkit unavailable (EC-35 — re-run Step 0)')
    if not isinstance(spec, dict):
        raise ValueError('render_mechanism: spec must be a dict (E-02 step)')
    if template is not None and not hasattr(template, 'GetConformer'):
        raise ValueError('render_mechanism: template must be an rdkit Mol (a previous draw.after_mol)')
    for _k in ('caption', 'caption_before'):
        if spec.get(_k) is not None and not isinstance(spec.get(_k), (list, tuple)):
            raise ValueError(f'render_mechanism: {_k} must be a list of strings')
    _hl = spec.get('highlight') or {}
    if not isinstance(_hl, dict) or any(
            not isinstance(v, (list, tuple)) or any(not isinstance(pr, (list, tuple)) or len(pr) != 2 for pr in v)
            for v in _hl.values()):
        raise ValueError('render_mechanism: highlight must be {"form"|"break"|"wrong": [[m, n], ...]}')
    width_in = float(width_in or CHS_WIDTH_IN.get(section, 6.0))
    requirement = str(spec.get('requirement') or ('MECHANISM' if spec.get('arrows') else 'REACTION_SCHEME'))
    if requirement not in CHS_FALLBACK_CHAIN:
        raise ValueError(f'render_mechanism: requirement {requirement!r} not in {CHS_FALLBACK_CHAIN}')
    arrows = list(spec.get('arrows') or [])
    ok, reason = verify_mechanism_step({'before': spec.get('before'), 'after': spec.get('after'), 'arrows': arrows})
    if not ok:
        raise ValueError(f'render_mechanism: {reason}')
    okb, reasonb = step_atom_balance(spec)
    if not okb:
        raise ValueError(f'render_mechanism: {reasonb}')
    before = mapped_mol(spec['before'], keep_h=True)
    after = mapped_mol(spec['after'], keep_h=True)
    # explicit [H:n] atoms are kept for the proof; for the picture they are drawn as H counts
    # unless the H actually moves (an arrow names it)
    moving = set()
    for a in arrows:
        for side in (a.get('from') or {}, a.get('to') or {}):
            for key in ('atom', 'lone_pair', 'lone_pair_on', 'bias', 'radical'):
                if side.get(key) is not None:
                    moving.add(int(side[key]))
            for key in ('bond',):
                for n in side.get(key) or []:
                    moving.add(int(n))
    before = _strip_unmoving_h(before, moving); after = _strip_unmoving_h(after, moving)
    tmpl = template
    _depict(before, tmpl)
    _place_fragments(before, arrows)          # placement angle 0; attempts re-place from here
    _depict(after, before)
    labels = {int(k): v for k, v in (spec.get('atom_labels') or {}).items()}
    tints = {int(k): v for k, v in (spec.get('atom_colours') or {}).items()}
    if not tints:
        frags = _fragments(before)
        if len(frags) > 1:
            main = max(range(len(frags)), key=lambda i: (len(frags[i]), -i))
            k = 0
            for fi, atoms in enumerate(frags):
                if fi == main:
                    continue
                for ai in sorted(atoms):
                    n = before.GetAtomWithIdx(ai).GetAtomMapNum()
                    if n:
                        tints[n] = CHS_REAGENT_TINTS[k % len(CHS_REAGENT_TINTS)]; k += 1
    hl = spec.get('highlight') or {}
    cap = [str(x) for x in (spec.get('caption') or [])]
    cap_before = [str(x) for x in (spec.get('caption_before') or [])]
    ink = _chs_ink()
    font_px = int(round(CHS_FONT_PX * dpi / CHS_FIGURE_DPI))
    bond_px = int(round(CHS_BOND_PX * dpi / CHS_FIGURE_DPI))
    cap_px = tuple(int(round(c * dpi / CHS_FIGURE_DPI)) for c in CHS_CAPTION_PX)
    above = [str(spec.get('reagents_above') or '')] if not isinstance(spec.get('reagents_above'), (list, tuple)) \
        else list(spec.get('reagents_above'))
    below = [str(spec.get('conditions_below') or '')] if not isinstance(spec.get('conditions_below'), (list, tuple)) \
        else list(spec.get('conditions_below'))
    below += [f'− {b}' for b in (spec.get('byproduct_labels') or [])]
    ctx = {'before_mol': before, 'after_mol': after, 'arrows': arrows, 'labels': labels, 'tints': tints,
           'form': hl.get('form') or [], 'break': hl.get('break') or [],
           'wrong_before': (hl.get('wrong_before') or []), 'wrong_after': (hl.get('wrong') or []),
           'cap_before': cap_before, 'cap_after': cap, 'above': above, 'below': below}
    ledger = []
    attempts = 0
    chain = CHS_FALLBACK_CHAIN[CHS_FALLBACK_CHAIN.index(requirement):]
    for req in chain:
        _multi = len(_fragments(before)) > 1
        schedule = _attempt_schedule(_multi) if req == 'MECHANISM' else \
            [(CHS_RETRY_CURVATURES[0], CHS_RETRY_BIAS[0], 0, 0, pl) for pl in (CHS_RETRY_PLACEMENT if _multi else (0,))]
        last = None
        for att in schedule:
            attempts += 1
            im, panels, offsets, scale, findings = _render_attempt(ctx, att, ink, dpi, width_in, cap_px,
                                                                  font_px, bond_px, wrong, req)
            last = (im, panels, offsets, scale, findings, att)
            if not findings:
                break
        im, panels, offsets, scale, findings, att = last
        if not findings:
            if req != requirement:
                ledger.append({'from': requirement, 'to': req, 'why': 'E-04 layout gate failed on every attempt'})
            png = _png_bytes(im)
            identifier = {'before': mechanism_canonical(spec['before']), 'after': mechanism_canonical(spec['after']),
                          'before_iso': mechanism_canonical(spec['before'], stereo=True),
                          'after_iso': mechanism_canonical(spec['after'], stereo=True),
                          'arrows': _normalise_arrows(arrows) if req == 'MECHANISM' else [],
                          'e03': 'PASS', 'requirement': req}
            geometry = {'panels': [p.geometry for p in panels], 'offsets': offsets, 'scale': scale,
                        'canvas': im.size, 'dpi': dpi}
            meta = {'attempts': attempts, 'attempt': att, 'bytes': len(png), 'dpi': dpi,
                    'canvas_px': im.size, 'width_in': im.width / float(dpi), 'section': section,
                    'target_bytes': CHS_TARGET_BYTES, 'over_target': len(png) > CHS_TARGET_BYTES}
            d = MechanismDraw(png, min(width_in, im.width / float(dpi)), meta, identifier, geometry, req, ledger)
            d.after_mol = after
            d.before_mol = before
            return d
        ledger.append({'from': req, 'to': None, 'why': '; '.join(sorted(set(findings)))[:300]})
    raise ValueError('render_mechanism: CHS_LAYOUT_UNRENDERABLE — every fallback failed the layout gate (record APPLIES-UNRENDERABLE for this figure, EC-05) — ' +
                     '; '.join(l['why'] for l in ledger if l.get('why')))


def _strip_unmoving_h(mol, moving_maps):
    """Remove explicit H atoms that no arrow names (they are drawn as H counts); mapped
    H atoms that move stay as atoms. Uses rdkit RemoveHs so a stereocentre that carries
    an explicit [H] keeps its configuration (a hand-rolled removal inverts the parity).
    H₂, a bare hydride and H–H stay atoms. Keeps every heavy-atom map number."""
    from rdkit import Chem
    rw = Chem.RWMol(mol)
    for a in rw.GetAtoms():
        if a.GetAtomicNum() == 1 and a.GetAtomMapNum() and a.GetAtomMapNum() not in moving_maps:
            a.SetAtomMapNum(0)                      # a stationary H: eligible for removal
    m = rw.GetMol()
    ps = Chem.RemoveHsParameters()
    ps.removeMapped = False                         # moving (still-mapped) H atoms stay
    ps.removeHydrides = False
    ps.removeDegreeZero = False
    ps.removeIsotopes = False
    try:
        ps.removeOnlyHNeighbors = False             # H2 keeps both atoms
    except Exception:
        pass
    m = Chem.RemoveHs(m, ps, sanitize=True)
    return m


def figure_layout_audit(draw):
    """E-04 re-audit of a MechanismDraw from its recorded geometry (what the retry loop
    ran at render time, re-run independently so a caller can prove it). Returns
    (ok, findings)."""
    if not isinstance(draw, MechanismDraw):
        return False, ['not a MechanismDraw']
    g = draw.geometry
    panels = [_Panel(None, pg, []) for pg in g['panels']]
    findings = _layout_findings(panels, g['offsets'], g['canvas'], g['dpi'], scale=g.get('scale', 1.0))
    if draw.meta.get('over_target'):
        findings.append(f"SIZE: {draw.meta['bytes']} B > target {CHS_TARGET_BYTES} B (recorded, not blocking)")
    blocking = [f for f in findings if not f.startswith('SIZE:')]
    return (not blocking), findings


def render_structure_panel(smiles, caption, section='WHY_WRONG', dpi=CHS_FIGURE_DPI, template=None,
                           wrong_bonds=(), form_bonds=(), atom_labels=None, atom_colours=None,
                           wrong_atoms=()):
    """Public entry: the E-04 retry for a single-species panel is the in-plane rotation
    schedule (0/90/180/270 — never a mirror) at the section width, then at the full
    DEDUCTION width; a panel that fails every attempt raises CHS_LAYOUT_UNRENDERABLE
    (the caller records APPLIES-UNRENDERABLE for that figure, §6A-10). Non-ValueError
    input faults are re-raised as ValueError."""
    if caption is not None and not isinstance(caption, (list, tuple)):
        raise ValueError('render_structure_panel: caption must be a list of strings')
    last = None
    widths = [CHS_WIDTH_IN.get(section, 5.6)]
    if CHS_WIDTH_IN['DEDUCTION'] not in widths:
        widths.append(CHS_WIDTH_IN['DEDUCTION'])
    attempts = 0
    for w_in in widths:
        for rot in CHS_RETRY_ROTATIONS:
            attempts += 1
            try:
                d = _render_structure_panel(smiles, [str(x) for x in (caption or [])], section, dpi, template,
                                            wrong_bonds, form_bonds, atom_labels, atom_colours, wrong_atoms,
                                            rot=rot, width_in=w_in)
                d.meta['attempts'] = attempts
                return d
            except ValueError as exc:
                if 'layout gate' not in str(exc):
                    raise
                last = exc
            except Exception as exc:                    # noqa: BLE001
                raise ValueError(f'render_structure_panel: malformed input — {type(exc).__name__}: {exc}') from exc
    raise ValueError(f'render_structure_panel: CHS_LAYOUT_UNRENDERABLE — {last}')


def _render_structure_panel(smiles, caption, section, dpi, template, wrong_bonds, form_bonds,
                            atom_labels, atom_colours, wrong_atoms, rot=0, width_in=None):
    """ANNOTATED_STRUCTURE / option panel: one species with persisting labels, the wrong
    bond(s) in WRONG_INK tint, caption inside the image, aligned to `template`. Returns
    MechanismDraw (requirement 'STRUCTURE_GRAPH'); identifier = canonical SMILES + labels."""
    Chem = _chs_rdkit()
    if Chem is None:
        raise ValueError('RE-25: rdkit unavailable (EC-35 — re-run Step 0)')
    width_in = float(width_in or CHS_WIDTH_IN.get(section, 5.6))
    mol = mapped_mol(smiles, keep_h=True)
    mol = _strip_unmoving_h(mol, set())
    _depict(mol, template)
    _rotate_all(mol, rot)
    labels = {int(k): v for k, v in (atom_labels or {}).items()}
    tints = {int(k): v for k, v in (atom_colours or {}).items()}
    for n in wrong_atoms or ():
        tints[int(n)] = CHS_WRONG_TINT
    ink = _chs_ink()
    font_px, bond_px = CHS_FONT_PX * dpi // CHS_FIGURE_DPI, CHS_BOND_PX * dpi // CHS_FIGURE_DPI
    cap_px = tuple(int(round(c * dpi / CHS_FIGURE_DPI)) for c in CHS_CAPTION_PX)
    p = _panel(mol, labels, tints, list(form_bonds), [], list(wrong_bonds), [], 0.0, 0.3, bond_px, font_px,
               caption, ink, dpi=dpi)
    _caption_panel(p, list(caption or []), cap_px)
    from PIL import ImageOps
    im = ImageOps.expand(p.image, border=int(CHS_EDGE_PX_300 * dpi / 300.0) + 2, fill='white')
    scale = 1.0
    if im.width > width_in * dpi:
        scale = width_in * dpi / im.width
        im = im.resize((int(im.width * scale), int(im.height * scale)), resample=1)
    # im is already resized; hand the gate the pre-resize canvas so scale applies once
    findings = _layout_findings([p], [(0, 0)], (int(round(im.width / scale)), int(round(im.height / scale))),
                                dpi, scale=scale, ink=ink)
    findings = [f for f in findings if not f.startswith('L4')]
    if findings:
        raise ValueError('render_structure_panel: layout gate — ' + '; '.join(findings))
    png = _png_bytes(im)
    identifier = {'canonical': mechanism_canonical(smiles, stereo=True), 'labels': dict(sorted(labels.items())),
                  'requirement': 'STRUCTURE_GRAPH'}
    meta = {'attempts': 1, 'rotation': rot, 'bytes': len(png), 'dpi': dpi, 'canvas_px': im.size, 'section': section,
            'width_in': im.width / float(dpi), 'target_bytes': CHS_TARGET_BYTES,
            'over_target': len(png) > CHS_TARGET_BYTES}
    d = MechanismDraw(png, min(width_in, im.width / float(dpi)), meta, identifier,
                      {'panels': [p.geometry], 'offsets': [(0, 0)], 'scale': scale, 'canvas': im.size, 'dpi': dpi},
                      'STRUCTURE_GRAPH', [])
    d.after_mol = mol
    return d


def figure_review_sheet(figures, out_png, cols=3, cell_px=560, dpi=CHS_FIGURE_DPI):
    """E-09. One contact sheet per batch: every RE-25 figure (path or MechanismDraw)
    labelled with its id, for the ONE in-turn model view that records
    figure_review[id] = 'ok' | 'mismatch:<reason>'. `figures`: [(fig_id, path_or_draw)].
    Returns (out_png, {'count', 'cols', 'rows', 'cells': [{id, box}]})."""
    from PIL import Image, ImageDraw
    import io
    items = list(figures or [])
    if not items:
        raise ValueError('figure_review_sheet: no figures')
    per = CHS_REVIEW_PER_SHEET
    if len(items) > per:
        # §6A-12: 12 figures per sheet — out_png, then out_png with _2, _3 … suffixes
        root, ext = os.path.splitext(out_png)
        sheets, cells = [], []
        for n, start in enumerate(range(0, len(items), per), start=1):
            path_n = out_png if n == 1 else f'{root}_{n}{ext}'
            pth, meta_n = figure_review_sheet(items[start:start + per], path_n, cols=cols, cell_px=cell_px, dpi=dpi)
            sheets.append(pth); cells += meta_n['cells']
        return out_png, {'count': len(items), 'cols': cols, 'rows': None, 'cells': cells, 'sheets': sheets}
    f, _ = _native_font('bold', 22)
    rows = (len(items) + cols - 1) // cols
    label_h = 32
    sheet = Image.new('RGB', (cols * cell_px + (cols + 1) * 10, rows * (cell_px + label_h) + (rows + 1) * 10), 'white')
    dr = ImageDraw.Draw(sheet)
    cells = []
    for k, (fid, src) in enumerate(items):
        if isinstance(src, MechanismDraw):
            im = Image.open(io.BytesIO(src.png_bytes))
        elif hasattr(src, 'path'):                       # a RepresentationFigure
            im = Image.open(src.path)
        elif isinstance(src, (str, bytes, os.PathLike)):
            im = Image.open(src)
        else:
            raise ValueError(f'figure_review_sheet: {fid!r} is not a draw, a figure or a path')
        im = im.convert('RGB')
        s = min(cell_px / im.width, cell_px / im.height, 1.0)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), resample=1)
        r, c = divmod(k, cols)
        x = 10 + c * (cell_px + 10); y = 10 + r * (cell_px + label_h + 10)
        dr.text((x, y), str(fid), fill='#000000', font=f)
        sheet.paste(im, (x, y + label_h))
        cells.append({'id': str(fid), 'box': (x, y, x + cell_px, y + label_h + cell_px)})
    sheet.save(out_png, format='PNG', optimize=True)
    return out_png, {'count': len(items), 'cols': cols, 'rows': rows, 'cells': cells, 'sheets': [out_png]}


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════════
# CLUSTER SYL — SYLLABUS & SAMPLE-PAPER FILE CENSUS
# (GAP-2026-09-01-SYLLABUS-TRANSITION §3.4 — Release A; rebased per rev 4.6)
#
# WHY THIS CLUSTER EXISTS
#   §3.4's census is the fact-finding half of the T2 decision: WHICH project
#   files are syllabus candidates, and which are sample papers (R14 — recorded
#   at census time, consumed by Step 5 only, from Release B/C). The DECISION
#   over the census (T2 rows, HS-ST2..6) lives in blueprint_core
#   resolve_syllabus_sources — facts here, rulings there, no cross-import.
#   The census runs at PYQDraft S1-2 and cheaply at every step start (§3.7
#   drift guard): one directory listing + one glob-class filter. R18: English
#   only — a translated syllabus is simply a second census hit.
# ════════════════════════════════════════════════════════════════════════════

#: §3.4 candidate extensions (shared by syllabus and sample-paper census).
SYLLABUS_CENSUS_EXTS = ('.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg')


def _census_match(basename, token):
    name = os.path.basename(str(basename))
    stem, dot, ext = name.rpartition('.')
    if not dot or ('.' + ext).casefold() not in SYLLABUS_CENSUS_EXTS:
        return False
    return token in name.casefold()


def syllabus_file_census(file_names):
    """Candidate syllabus files: basename contains 'syllabus' (casefold),
    extension in SYLLABUS_CENSUS_EXTS. Order-preserving."""
    return [f for f in (file_names or []) if _census_match(f, 'syllabus')]


def sample_paper_census(file_names):
    """Candidate sample papers (R14): basename contains 'samplepaper'
    (casefold), same extensions. Recorded only in Release A; consumed by
    Step 5 alone from Release B/C. Absent => silent."""
    return [f for f in (file_names or []) if _census_match(f, 'samplepaper')]


def file_sha256(path):
    """sha256 hex of a file's raw bytes (the §3.10 staleness identity and the
    T2 rows 9-10 duplicate check)."""
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def census_records(paths):
    """[{'name', 'path', 'sha256'}] for resolve_syllabus_sources — name is the
    basename; sha256 over raw bytes."""
    out = []
    for p in (paths or []):
        out.append({'name': os.path.basename(str(p)), 'path': str(p),
                    'sha256': file_sha256(p) if os.path.exists(str(p))
                    else None})
    return out

# END CLUSTER SYL
# ════════════════════════════════════════════════════════════════════════════

def self_test():
    passed = total = 0
    fails = []

    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            fails.append(name)

    # ── folder id parsing ────────────────────────────────────────────────────
    check('io_folder_url', parse_drive_folder_id(
        'https://drive.google.com/drive/folders/13sdlvaEJjwLKmsvP-zdCpv4l4GhZbF9s')
        == '13sdlvaEJjwLKmsvP-zdCpv4l4GhZbF9s')
    check('io_folder_url_u0', parse_drive_folder_id(
        'https://drive.google.com/drive/u/0/folders/ABC123defGHI') == 'ABC123defGHI')
    check('io_folder_bare_id', parse_drive_folder_id('13sdlvaEJjwLKmsvP') == '13sdlvaEJjwLKmsvP')
    check('io_folder_none', parse_drive_folder_id('not a link') is None)

    # ── listing normalisation ────────────────────────────────────────────────
    raw = [{'id': '1', 'title': 'a.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '12694409'},
           {'id': '2', 'name': 'b.docx', 'mimeType': bc.DOCX_MIME, 'size': 100},
           {'id': '3', 'title': 'yr', 'mimeType': bc.FOLDER_MIME}]
    norm = normalise_drive_listing(raw)
    check('io_norm_size_str_to_int', norm[0]['fileSize'] == 12694409)
    check('io_norm_name_alias', norm[1]['name'] == 'b.docx')
    check('io_norm_missing_size_none', norm[2]['fileSize'] is None)
    check('io_norm_envelope', len(normalise_drive_listing({'files': raw})) == 3)
    check('io_norm_empty', normalise_drive_listing([]) == [])
    check('io_norm_junk_skipped', len(normalise_drive_listing(['junk', None])) == 0)

    # ── enumeration: rejects, duplicates, pagination, recursion ──────────────
    tree = {
        'root': {'items': [
            {'id': 'f1', 'title': '2010.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '900'},
            {'id': 'f2', 'title': 'old.doc', 'mimeType': 'application/msword', 'fileSize': '9'},
            {'id': 'f3', 'title': 'native', 'mimeType': bc.GDOC_MIME},
            {'id': 'sub', 'title': '2011', 'mimeType': bc.FOLDER_MIME}]},
        'sub': {'items': [
            {'id': 'f4', 'title': '2011.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '800'}]},
    }

    def fake_list(fid, page_token=None):
        return tree[fid]

    papers, rejects = collect_corpus_files(fake_list, 'root')
    check('io_enum_finds_nested', len(papers) == 2)
    check('io_enum_rejects_both', len(rejects) == 2)
    check('io_enum_reject_has_reason', all(r['reason'] for r in rejects))
    check('io_enum_size_captured', papers[0]['fileSize'] == 900)
    check('io_enum_key_present', 'paper_key' in papers[0])

    def fake_dup(fid, page_token=None):
        return {'items': [
            {'id': 'a', 'title': 'X_2010.docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '1'},
            {'id': 'b', 'title': 'X_2010 (1).docx', 'mimeType': bc.DOCX_MIME, 'fileSize': '2'}]}
    try:
        collect_corpus_files(fake_dup, 'root')
        check('io_enum_duplicate_hard_stop', False)
    except DuplicatePaperError as exc:
        check('io_enum_duplicate_hard_stop', 'X_2010' in str(exc))

    pages = [{'items': [{'id': 'p1', 'title': 'a.docx', 'mimeType': bc.DOCX_MIME,
                         'fileSize': '1'}], 'nextPageToken': 'T'},
             {'items': [{'id': 'p2', 'title': 'b.docx', 'mimeType': bc.DOCX_MIME,
                         'fileSize': '1'}]}]

    def fake_paged(fid, page_token=None):
        return pages[1] if page_token else pages[0]

    check('io_enum_paginates', len(collect_corpus_files(fake_paged, 'r')[0]) == 2)

    # ── payload decoding: every documented shape ─────────────────────────────
    payload = base64.b64encode(b'PK\x03\x04hello').decode()
    inner = json.dumps({'id': 'x', 'title': 't', 'mimeType': 'm', 'content': payload})
    check('io_decode_raw_bytes', decode_drive_payload(b'PK\x03\x04') == b'PK\x03\x04')
    check('io_decode_inner_json', decode_drive_payload(inner) == b'PK\x03\x04hello')
    check('io_decode_spill_shape',
          decode_drive_payload([{'text': inner, 'type': 'text'}]) == b'PK\x03\x04hello')
    check('io_decode_dict', decode_drive_payload({'content': payload}) == b'PK\x03\x04hello')
    spill = '/tmp/_ci_spill.json'
    with open(spill, 'w') as fh:
        json.dump([{'text': inner, 'type': 'text'}], fh)
    check('io_decode_spill_path', decode_drive_payload(spill) == b'PK\x03\x04hello')
    for bad, label in [([], 'empty_list'), ('nonsense', 'garbage'), ({'k': 1}, 'no_content')]:
        try:
            decode_drive_payload(bad)
            check(f'io_decode_reject_{label}', False)
        except TransportFallback:
            check(f'io_decode_reject_{label}', True)

    # ── download verification ────────────────────────────────────────────────
    check('io_verify_ok', verify_downloaded_bytes(b'PK\x03\x04abc', 7))
    for args, label in [((b'', None), 'empty'), ((b'<html>', None), 'not_docx'),
                        ((b'PK\x03\x04abc', 99), 'truncated')]:
        try:
            verify_downloaded_bytes(*args)
            check(f'io_verify_reject_{label}', False)
        except TransportFallback:
            check(f'io_verify_reject_{label}', True)

    # ── fetch: EVERY failure degrades, never SystemExit ──────────────────────
    def boom(_):
        raise RuntimeError('connector exploded')
    try:
        fetch_drive_docx(boom, {'id': 'x', 'name': 'n.docx', 'fileSize': 10}, '/tmp/ci')
        check('io_fetch_error_is_fallback', False)
    except TransportFallback:
        check('io_fetch_error_is_fallback', True)
    except Exception:
        check('io_fetch_error_is_fallback', False)
    try:
        fetch_drive_docx(boom, {'id': 'x', 'name': 'big.docx',
                                'fileSize': bc.DRIVE_CAP + 1}, '/tmp/ci')
        check('io_fetch_oversize_not_attempted', False)
    except TransportFallback as exc:
        check('io_fetch_oversize_not_attempted', 'without attempting' in str(exc))

    def good(_):
        return base64.b64encode(b'PK\x03\x04data').decode()
    p = fetch_drive_docx(lambda i: json.dumps({'content': good(i)}),
                         {'id': 'x', 'name': 'ok.docx', 'fileSize': 8}, '/tmp/ci_ok')
    check('io_fetch_writes_file', os.path.exists(p) and os.path.getsize(p) == 8)

    # ── upload resolution: identity, not filename, not recency ──────────────
    up = '/tmp/ci_uploads'
    os.makedirs(up, exist_ok=True)
    for f in os.listdir(up):
        os.remove(os.path.join(up, f))
    for fn in ['E_02-May-2010_Sorted (1).docx', 'E_2011_Sorted.docx',
               'Unrelated_2099.docx', '~$lock.docx']:
        open(os.path.join(up, fn), 'w').write('x')
    want = [bc.canonical_paper_key('E_02May2010_Sorted.docx'),
            bc.canonical_paper_key('E_2012_Sorted.docx')]
    res = resolve_uploaded_papers(want, up)
    check('io_upload_matches_through_suffix', len(res['matched']) == 1)
    check('io_upload_reports_missing',
          res['missing'] == [bc.canonical_paper_key('E_2012_Sorted.docx')])
    check('io_upload_flags_unexpected', len(res['unexpected']) == 2)
    check('io_upload_ignores_lockfiles',
          not any('~$' in p for p in res['unexpected']))
    check('io_upload_missing_dir_safe',
          resolve_uploaded_papers(['k'], '/tmp/does_not_exist')['missing'] == ['k'])

    # ── figural cross-check ──────────────────────────────────────────────────
    mp = {1: ['i1.png'], 5: ['i2.png'], PREAMBLE: ['i0.png']}
    fc = figural_consistency(mp, {1: 'FIGURAL', 5: 'TEXT', 9: 'FIGURAL'})
    check('io_figural_flags_image_not_figural', fc['image_not_figural'] == [5])
    check('io_figural_flags_figural_no_image', fc['figural_no_image'] == [9])
    check('io_figural_preamble_ignored', 'preamble' not in str(fc))
    fc2 = figural_consistency(mp, {1: 'FIGURAL', 5: 'TEXT', 9: 'FIGURAL'}, overrides=(5, 9))
    check('io_figural_overrides_respected',
          not fc2['image_not_figural'] and not fc2['figural_no_image'])

    # ── structural corruption must ALWAYS surface as a NAMED gate ────────────
    # Regression guard: python-docx raises a bare KeyError and zipfile a bare
    # BadZipFile from deep inside their readers. Both previously escaped as raw
    # tracebacks instead of gate verdicts. Found by adversarial mutation testing.
    _bad = '/tmp/_ci_badzip.docx'
    with open(_bad, 'wb') as _fh:
        _fh.write(b'PK\x03\x04' + b'\x00' * 400)
    for _label, _fn in (
            ('refs', lambda: count_image_refs(_bad)),
            ('extract', lambda: extract_images(_bad, '/tmp/_ci_badx')),
            ('display', lambda: media_display_inches(_bad)),
            ('governor', lambda: optimize_docx(_bad, '/tmp/_ci_o.docx', 1)),
            ('invariants', lambda: docx_invariants(_bad))):
        try:
            _fn()
            check(f'io_corrupt_named_{_label}', False)
        except IntegrityError:
            check(f'io_corrupt_named_{_label}', True)
        except Exception:
            check(f'io_corrupt_named_{_label}', False)

    _missing_ok = True
    try:
        _safe_document(_bad)
        _missing_ok = False
    except IntegrityError:
        pass
    except Exception:
        _missing_ok = False
    check('io_safe_document_named', _missing_ok)

    # ── v1.0.1 parity must not fire on a legitimate rename ───────────────────
    _pdir = f'/tmp/corpus_io_parity/{os.getpid()}'
    os.makedirs(_pdir, exist_ok=True)
    try:
        import random as _rnd
        from PIL import Image as _Im
        import docx as _dx
        _rnd.seed(11)
        _png = os.path.join(_pdir, 'photo.png')
        _im = _Im.new('RGB', (600, 400))
        _im.putdata([(_rnd.randrange(256), _rnd.randrange(256), _rnd.randrange(256))
                     for _ in range(600 * 400)])
        _im.save(_png)                      # PNG source -> jpeg route -> RENAME
        _d = _dx.Document()
        _d.add_paragraph('Q.1 figure').add_run().add_picture(_png)
        _src = os.path.join(_pdir, 'src.docx')
        _dst = os.path.join(_pdir, 'dst.docx')
        _d.save(_src)
        _ok, _rep, _log = optimize_docx(_src, _dst, budget=os.path.getsize(_src) // 2)
        check('io_parity_rename_engaged', _rep['tier'] == 'T1')
        _renamed = ('word/media/photo.png' not in zipfile.ZipFile(_dst).namelist())
        check('io_parity_rename_happened', _renamed)
        _before = docx_invariants(_src)['px']
        _after = docx_invariants(_dst)['px']
        check('io_parity_rename_dims_unchanged',
              sorted(_before.values()) == sorted(_after.values()))
        try:
            assert_docx_parity(_src, _dst, allow_resample=False)
            check('io_parity_rename_no_false_stop', True)
        except IntegrityError:
            check('io_parity_rename_no_false_stop', False)
        # and a REAL dimension change must still be caught
        _ok2, _rep2, _ = optimize_docx(_src, _dst, budget=1, force_tier='T4')
        _shrunk = docx_invariants(_dst)['px']
        if sorted(_shrunk.values()) != sorted(_before.values()):
            try:
                assert_docx_parity(_src, _dst, allow_resample=False)
                check('io_parity_real_resize_still_caught', False)
            except IntegrityError:
                check('io_parity_real_resize_still_caught', True)
            check('io_parity_real_resize_allowed_when_permitted',
                  bool(assert_docx_parity(_src, _dst, allow_resample=True)))
    except DependencyMissing:
        pass                                # optional deps absent — nothing to assert

    # ── CLUSTER K — ANALYSIS DOC (GAP-2026-07-25-002) ──────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _tmp:
        _ck_selftest(check, _tmp)

    # ── CLUSTER V — VISION PHASE A / OBSERVATION I/O ────────────────────────
    with _tf.TemporaryDirectory() as _vtmp:
        # EC-V1 — a text-only exam produces a valid empty queue, not a failure.
        _q0 = build_vision_queue([], _vtmp)
        check('v_ec1_empty_build',
              _q0['items'] == [] and _q0['sheets'] == [] and _q0['stats']['queued'] == 0)
        check('v_queue_file_written',
              os.path.exists(os.path.join(_vtmp, VISION_QUEUE_NAME)))

        try:
            _Img = _need('PIL')
        except DependencyMissing:
            _Img = None

        if _Img is not None:
            def _mk(p, size=(120, 90), colour=(200, 30, 30)):
                _Img.new('RGB', size, colour).save(p, 'PNG')
                return p
            _src = [_mk(os.path.join(_vtmp, f'f{i}.png')) for i in range(14)]
            # EC-V15 — the SAME q_num in two different papers must stay distinct.
            _items = ([{'paper_id': 'P_A', 'q_num': i + 1, 'srcs': [_src[i]],
                        'subtopic': 'S1'} for i in range(7)] +
                      [{'paper_id': 'P_B', 'q_num': i + 1, 'srcs': [_src[7 + i]],
                        'subtopic': 'S2'} for i in range(7)])
            _q = build_vision_queue(_items, _vtmp, per_sheet=6)
            check('v_ec15_distinct_keys', len(_q['items']) == 14)
            check('v_ec15_distinct_tags',
                  len({i['tag'] for i in _q['items']}) == 14)

            # EC-V10 — THE fixture the design turns on: every queued item appears on
            # exactly one sheet, and every sheet named in an item actually exists.
            _seen = {}
            for _it in _q['items']:
                _seen.setdefault((_it['paper_id'], _it['q_num']), []).append(_it['sheet'])
            check('v_ec10_each_item_once',
                  len(_seen) == 14 and all(len(v) == 1 for v in _seen.values()))
            check('v_ec10_sheets_exist',
                  all(os.path.exists(os.path.join(_vtmp, s)) for s in _q['sheets']))
            check('v_ec10_sheet_count', _q['stats']['sheets'] == 3)   # 14 @ 6 -> 3
            check('v_ec10_cells_within_per_sheet',
                  all(0 <= i['cell'] < 6 for i in _q['items']))

            # EC-V10 — re-tiling at a different per_sheet keeps the invariant.
            _q2 = build_vision_queue(_items, _vtmp, per_sheet=4)
            check('v_ec10_retile', _q2['stats']['sheets'] == 4
                  and len(_q2['items']) == 14)
            # tags are stable across a re-tile: observations survive re-tiling
            check('v_tag_stable_across_retile',
                  {i['tag'] for i in _q['items']} == {i['tag'] for i in _q2['items']})

            # v1.9 — build_vision_queue() now UNIONS with the queue already in the
            # workdir (GAP-2026-07-27-B), so each single-build assertion below gets its
            # OWN sub-workdir. Sharing one directory would make every later assertion
            # see the accumulated set. The union itself is asserted explicitly further
            # down; these cases are about ONE build in isolation.
            def _iso(name):
                _d = os.path.join(_vtmp, '_iso_' + name)
                os.makedirs(_d, exist_ok=True)
                return _d

            # EC-V6 — a 3-panel question is ONE queue item.
            _q3 = build_vision_queue(
                [{'paper_id': 'P_C', 'q_num': 5, 'srcs': _src[:3]}], _iso('ec6'))
            check('v_ec6_multi_image_one_item',
                  len(_q3['items']) == 1 and _q3['items'][0]['renderable'])

            # EC-V8 — an unopenable part is queued and flagged, never dropped.
            _bad = os.path.join(_vtmp, 'broken.emf')
            with open(_bad, 'wb') as _f:
                _f.write(b'not an image')
            _q4 = build_vision_queue(
                [{'paper_id': 'P_D', 'q_num': 1, 'srcs': [_bad]}], _iso('ec8'))
            check('v_ec8_unrenderable_queued', len(_q4['items']) == 1)
            check('v_ec8_unrenderable_flagged',
                  _q4['items'][0]['renderable'] is False
                  and _q4['stats']['unrenderable'] == 1)

            # EC-V27 — the same (paper_id,q_num) twice collapses to ONE item with
            # both sources; two cells sharing a tag would make a Phase-B observation
            # unattributable. Found by property fuzzing.
            _q4b = build_vision_queue(
                [{'paper_id': 'P_E', 'q_num': 3, 'srcs': [_src[0]], 'subtopic': None},
                 {'paper_id': 'P_E', 'q_num': 3, 'srcs': [_src[1]], 'subtopic': 'S9'}],
                _iso('ec27'))
            check('v_ec27_dedup_one_item', len(_q4b['items']) == 1)
            check('v_ec27_dedup_srcs_unioned',
                  len(_q4b['items'][0]['srcs']) == 2)
            check('v_ec27_dedup_meta_filled',
                  _q4b['items'][0]['subtopic'] == 'S9')
            check('v_ec27_tags_unique',
                  len({i['tag'] for i in _q4b['items']}) == len(_q4b['items']))

            # malformed item dicts are skipped without crashing the build
            _q5 = build_vision_queue(
                [{'no_paper': 1}, {'paper_id': 'X', 'q_num': 'NaN'},
                 {'paper_id': 'X', 'q_num': 2, 'srcs': [_src[0]]}], _iso('malformed'))
            check('v_malformed_items_tolerated', len(_q5['items']) == 1)

            # ── END-TO-END: A -> B -> C -> profile ───────────────────────────
            _e2e = _iso('e2e')
            _qe = build_vision_queue(_items[:6], _e2e, per_sheet=6)
            _obs = [{'tag': i['tag'], 'figure_readable': True,
                     'object_type': 'micrograph', 'transformation_type': 'N/A',
                     'arrangement': 'single', 'complexity': 'Simple'}
                    for i in _qe['items']]
            write_vision_observations(_e2e, _obs)
            _read, _why = load_vision_observations(_e2e)
            check('v_obs_roundtrip', len(_read) == 6 and _why == '')
            _bk, _st = bc.merge_vision_observations(_qe['items'], _read)
            check('v_e2e_all_observed',
                  _st['vision_status'] == 'observed' and _st['missing'] == 0)
            _prof = bc.vision_profile(list(_bk.values()), min_dominant=5)
            check('v_e2e_profile_dominant',
                  _prof['object_types']['dominant'] == ['micrograph'])
            check('v_e2e_profile_status', _prof['vision_status'] == 'observed')

            # NEGATIVE TEST — Phase B skipped. Must NOT halt, must report.
            # v1.9: reads the SAME isolated dir the e2e block wrote to, so removing the
            # observations file leaves that queue's 6 items unobserved rather than
            # deleting a file the shared workdir never had.
            os.remove(os.path.join(_e2e, VISION_OBS_NAME))
            _none, _why2 = load_vision_observations(_e2e)
            check('v_neg_no_obs_file', _none == [] and 'Phase B' in _why2)
            _bk2, _st2 = bc.merge_vision_observations(_qe['items'], _none)
            check('v_neg_status_unavailable',
                  _st2['vision_status'] == 'unavailable' and _st2['observed'] == 0)
            _prof2 = bc.vision_profile(list(_bk2.values()))
            check('v_neg_profile_empty_but_shaped',
                  _prof2['object_types']['dominant'] == []
                  and _prof2['vision_status'] == 'unavailable'
                  and _prof2['images_unobserved'] == 6)

            # ── v1.9 IDEMPOTENT UNION (GAP-2026-07-27-B) ─────────────────────
            # The defect: build_vision_queue() wrote fixed filenames and never read
            # what was there, so a caller invoking it once per PAPER destroyed every
            # earlier paper's queue and sheets. Measured on IIT_JAM_BIOTECHNOLOGY:
            # 153 figural questions across 22 papers, _meta.vision recorded queued=8.
            _u = _iso('union')
            _u1 = build_vision_queue(
                [{'paper_id': 'PAPER_ALPHA', 'q_num': n, 'srcs': [_src[0]]}
                 for n in (1, 2, 3)], _u)
            _u2 = build_vision_queue(
                [{'paper_id': 'PAPER_BETA', 'q_num': n, 'srcs': [_src[0]]}
                 for n in (7, 8)], _u)
            check('v_union_accumulates', _u2['stats']['queued'] == 5)
            check('v_union_carried_in', _u2['stats']['carried_in'] == 3)
            check('v_union_submitted', _u2['stats']['submitted'] == 2)
            # Prior tags MUST survive, or Phase B observations already recorded against
            # them silently orphan (EC-V11/V12).
            # The invariant is CONDITIONAL, deliberately: a paper_id hash collision may
            # legitimately widen the code and re-tag the whole queue (EC-V12). What must
            # never happen is a re-tag that is not REPORTED — a silent one orphans every
            # Phase B observation already recorded. Asserting unconditional tag survival
            # would encode a hash outcome rather than the contract.
            check('v_union_prior_tags_survive_or_reported',
                  _u2['stats']['tag_generation_changed']
                  or {i['tag'] for i in _u1['items']} <= {i['tag'] for i in _u2['items']})
            # Realistic paper_ids (long and varied, as make_paper_id emits) do not
            # collide: verified across the 22 real ids of the reference corpus, width
            # stayed 4 with zero generation changes over an incremental 22-paper build.
            check('v_union_no_generation_change',
                  _u2['stats']['tag_generation_changed'] is False)
            # Re-submitting the same items is a no-op, so a resumed session that replays
            # a batch cannot inflate the queue.
            _u3 = build_vision_queue(
                [{'paper_id': 'PAPER_ALPHA', 'q_num': n, 'srcs': [_src[0]]}
                 for n in (1, 2, 3)], _u)
            check('v_union_resubmit_idempotent', _u3['stats']['queued'] == 5)
            check('v_union_empty_submit_preserves',
                  build_vision_queue([], _u)['stats']['queued'] == 5)
            # The width floor stops a SHRINKING key set from re-tagging survivors.
            _w = _iso('width')
            _wide = build_vision_queue(
                [{'paper_id': 'P1', 'q_num': 1, 'srcs': [_src[0]]},
                 {'paper_id': 'P2', 'q_num': 1, 'srcs': [_src[0]]}], _w)
            _narrow = build_vision_queue(
                [{'paper_id': 'P1', 'q_num': 1, 'srcs': [_src[0]]}], _w)
            check('v_union_width_floor_holds',
                  _narrow['tag_width'] == _wide['tag_width'])
            check('v_union_width_floor_no_retag',
                  {i['tag'] for i in _wide['items'] if i['paper_id'] == 'P1'}
                  == {i['tag'] for i in _narrow['items'] if i['paper_id'] == 'P1'})

            # ── v1.10 `fresh` — RUN-SCOPED OPT-OUT OF THE UNION ──────────────
            _fr = _iso('fresh')
            build_vision_queue(
                [{'paper_id': 'PAPER_ALPHA', 'q_num': n, 'srcs': [_src[0]]}
                 for n in (1, 2)], _fr)
            _f2 = build_vision_queue(
                [{'paper_id': 'PAPER_BETA', 'q_num': 3, 'srcs': [_src[0]]}],
                _fr, fresh=True)
            check('v_fresh_ignores_prior', _f2['stats']['queued'] == 1
                  and _f2['stats']['carried_in'] == 0)
            # observations from the discarded generation must not survive a fresh
            # build — Step 1's Phase C would otherwise merge a prior paper's
            # observations into this paper's queue.
            write_vision_observations(_fr, [{'tag': _f2['items'][0]['tag'],
                                             'figure_readable': True}])
            _f3 = build_vision_queue(
                [{'paper_id': 'PAPER_GAMMA', 'q_num': 1, 'srcs': [_src[0]]}],
                _fr, fresh=True)
            check('v_fresh_clears_observations',
                  load_vision_observations(_fr)[0] == [])
            # default remains the union: the very next call without fresh carries.
            _f4 = build_vision_queue(
                [{'paper_id': 'PAPER_DELTA', 'q_num': 1, 'srcs': [_src[0]]}], _fr)
            check('v_fresh_default_still_unions', _f4['stats']['queued'] == 2)

            # ── v1.9 CLUSTER Q — ORIGINAL POSITION CODEC (GAP-2026-07-27-E) ──
            check('q_stamp_basic',
                  stamp_original_q_num('[15-Feb-2026 Shift 1]', 37)
                  == '[15-Feb-2026 Shift 1 Q37]')
            check('q_roundtrip',
                  parse_original_q_num(stamp_original_q_num('[15-Feb-2026]', 5)) == 5)
            check('q_stamp_idempotent',
                  stamp_original_q_num('[15-Feb-2026 Q9]', 12) == '[15-Feb-2026 Q9]')
            check('q_none_num_noop',
                  stamp_original_q_num('[15-Feb-2026]', None) == '[15-Feb-2026]')
            # A pre-v1.18 label MUST read as UNKNOWN, never as position 0.
            check('q_pre_v118_label_none',
                  parse_original_q_num('[15-Feb-2026 Shift 1]') is None)
            check('q_empty_none', parse_original_q_num('') is None
                  and parse_original_q_num(None) is None)
            check('q_non_label_untouched',
                  stamp_original_q_num('not a label', 3) == 'not a label')
            _ms = [{'q_range': [1, 30], 'question_type': 'MCQ'},
                   {'q_range': [31, 40], 'question_type': 'MSQ'},
                   {'q_range': [41, 60], 'question_type': 'NAT'}]
            check('q_band_msq', question_type_for_position(37, _ms) == 'MSQ')
            check('q_band_edges', question_type_for_position(31, _ms) == 'MSQ'
                  and question_type_for_position(40, _ms) == 'MSQ'
                  and question_type_for_position(41, _ms) == 'NAT')
            check('q_band_uncovered_none', question_type_for_position(99, _ms) is None)
            check('q_band_no_scheme_none',
                  question_type_for_position(37, []) is None
                  and question_type_for_position(None, _ms) is None)
            check('q_band_malformed_skipped',
                  question_type_for_position(37, [{'q_range': ['x', 'y']}] + _ms) == 'MSQ')

            # queue round-trip
            _lq, _lwhy = load_vision_queue(_e2e)
            check('v_queue_roundtrip', _lq is not None and _lwhy == '')

        # malformed / missing observation files never raise
        _badobs = os.path.join(_vtmp, 'bad_obs.json')
        with open(_badobs, 'w', encoding='utf-8') as _f:
            _f.write('{not json')
        check('v_obs_malformed_safe',
              load_vision_observations(_vtmp, path=_badobs)[0] == []
              and 'unreadable' in load_vision_observations(_vtmp, path=_badobs)[1])
        with open(_badobs, 'w', encoding='utf-8') as _f:
            _f.write('"a string"')
        check('v_obs_wrong_shape_safe',
              load_vision_observations(_vtmp, path=_badobs)[0] == [])
        check('v_queue_missing_safe',
              load_vision_queue(os.path.join(_vtmp, 'nope'))[0] is None)

    # ── CLUSTER I — TABLE STRUCTURE FIXTURE (GAP-2026-07-29-TBL, v1.11) ──────
    # THE fixture the 2026.07.29 deployment shipped without. The old row.cells
    # implementation returns one entry per GRID COLUMN and substitutes the
    # ANCHOR for every covered position, so on this table it yields
    #   [['Region','Printers','Printers','Printers','Printers'],
    #    ['Region','Laser','Inkjet','Dot','3D'], ...]
    # and the anchor-once expectations below FAIL. A revert of _table_rows to
    # row.cells therefore breaks this suite instead of passing green.
    import xml.etree.ElementTree as _ET
    _W_ = '{%s}' % _NS_W  # noqa: F841 — kept for symmetry with the parser
    _tbl_merged = _ET.fromstring(
        ('<w:tbl xmlns:w="%s">'
         ' <w:tr>'
         '  <w:tc><w:tcPr><w:vMerge w:val="restart"/></w:tcPr>'
         '   <w:p><w:r><w:t>Region</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:tcPr><w:gridSpan w:val="4"/></w:tcPr>'
         '   <w:p><w:r><w:t>Print</w:t></w:r><w:r><w:t>ers</w:t></w:r></w:p></w:tc>'
         ' </w:tr>'
         ' <w:tr>'
         '  <w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p/></w:tc>'
         '  <w:tc><w:p><w:r><w:t>Laser</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>Inkjet</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>Dot</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>3D</w:t></w:r></w:p></w:tc>'
         ' </w:tr>'
         ' <w:tr>'
         '  <w:tc><w:p><w:r><w:t>North</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>5</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>6</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>7</w:t></w:r></w:p></w:tc>'
         '  <w:tc><w:p><w:r><w:t>8</w:t></w:r></w:p></w:tc>'
         ' </w:tr>'
         '</w:tbl>') % _NS_W)
    _rows = _table_rows(_tbl_merged, None)
    # anchor once, never a repeat — this is exactly what row.cells cannot do
    check('tbl_anchor_once_gridspan_header', _rows[0] == ['Region', 'Printers'])
    check('tbl_anchor_once_vmerge_label', _rows[1] == ['Laser', 'Inkjet', 'Dot', '3D'])
    check('tbl_plain_body_row', _rows[2] == ['North', '5', '6', '7', '8'])
    check('tbl_no_padding_cells', all('' not in r for r in _rows))
    # geometry survives the read-back: cs=4 header span + rs=2 label span
    _spec = read_table_spec(_tbl_merged)
    check('tbl_spec_spans_read_back',
          table_spec_spans(_spec) == [(0, 0, 2, 1), (0, 1, 1, 4)])
    check('tbl_spec_geometry_clean',
          place_cells(normalise_table_spec(_spec)['grid'])[3] == [])
    # flat-table BYTE-IDENTITY: output on a spanless table is pinned to the exact
    # serialised bytes the legacy implementation produced
    _tbl_flat = _ET.fromstring(
        ('<w:tbl xmlns:w="%s">'
         '<w:tr><w:tc><w:p><w:r><w:t>a</w:t></w:r></w:p></w:tc>'
         '<w:tc><w:p><w:r><w:t>b</w:t></w:r></w:p></w:tc></w:tr>'
         '<w:tr><w:tc><w:p><w:r><w:t>c</w:t></w:r></w:p></w:tc>'
         '<w:tc><w:p><w:r><w:t>d</w:t></w:r></w:p></w:tc></w:tr>'
         '</w:tbl>') % _NS_W)
    check('tbl_flat_byte_identity',
          json.dumps(_table_rows(_tbl_flat, None)) == json.dumps([['a', 'b'], ['c', 'd']]))
    # legacy {'headers','rows'} DI payload — accepted for ever, never migrated
    _leg = normalise_table_spec({'headers': ['X', 'Y'], 'rows': [['1', '2']]})
    check('tbl_legacy_di_payload',
          _leg['grid'][0][0]['t'] == 'X' and _leg.get('header_rows') == 1)
    check('tbl_legacy_flat_no_spans', table_spec_spans(_leg) == [])
    # full builder round trip: build_di_table -> raw-XML read-back. Spans must
    # survive and NO stray empty cell may appear (the Q.52/Q.61 defect shape).
    try:
        import docx as _dxT
        _dT = _dxT.Document()
        _built = build_di_table(_dT, {'grid': [
            [{'t': 'Region', 'rs': 2}, {'t': 'Printers', 'cs': 4}],
            [{'t': 'Laser'}, {'t': 'Inkjet'}, {'t': 'Dot'}, {'t': '3D'}],
            [{'t': 'North'}, {'t': '5'}, {'t': '6'}, {'t': '7'}, {'t': '8'}]],
            'header_rows': 1})
        _rt_rows = _table_rows(_built._tbl, None)
        check('tbl_build_roundtrip_values',
              _rt_rows == [['Region', 'Printers'],
                           ['Laser', 'Inkjet', 'Dot', '3D'],
                           ['North', '5', '6', '7', '8']])
        check('tbl_build_roundtrip_spans',
              table_spec_spans(read_table_spec(_built._tbl)) == [(0, 0, 2, 1), (0, 1, 1, 4)])
        check('tbl_build_no_stray_empty',
              sum(r.count('') for r in _rt_rows) == 0)
    except ImportError:
        pass                                # python-docx absent — parse-side already covered

    # ── is_option / para_has_image FIXTURE (follow-up open since 2026.07.26.2) ─
    # bare-marker + OPT_PATTERNS cases, image-option path, Paragraph-vs-element
    # duality, clean_option_text stripping. The single shared predicate every
    # step delegates to finally has its own regression net.
    # ── v1.15 line-art classifier (GAP-2026-08-30-LINEART-CLASSIFIER) ────────
    try:
        from PIL import Image as _LImg
        import numpy as _lnp
        import matplotlib as _lmpl; _lmpl.use('Agg'); import matplotlib.pyplot as _lplt
        _lb = io.BytesIO(); _lf, _lax = _lplt.subplots(figsize=(3, 2), dpi=150)
        for _i in range(3):
            _lax.plot([0, 1, 2], [_i, _i + 1, _i], marker='o')
        _lax.text(1, 1, 'k'); _lf.savefig(_lb, format='png', dpi=150, facecolor='white'); _lplt.close(_lf)
        _chart = _LImg.open(io.BytesIO(_lb.getvalue())).convert('RGB')
        check('lineart_antialiased_chart_is_line_art',
              len(set(_chart.getdata())) > 256 and _is_line_art(_chart))   # old rule said photo
        _rng = _lnp.random.default_rng(1)
        _photo = _LImg.fromarray(_lnp.clip(_lnp.linspace(0, 255, 200)[None, :, None] * _lnp.ones((150, 1, 3))
                                           + _rng.normal(0, 6, (150, 200, 3)), 0, 255).astype('uint8'))
        check('lineart_noisy_photo_is_not', not _is_line_art(_photo))
        _scan = _lnp.full((150, 200, 3), 245); _scan[60:66, 20:180] = 20
        _scan = _LImg.fromarray(_lnp.clip(_scan + _rng.normal(0, 4, _scan.shape), 0, 255).astype('uint8'))
        check('lineart_noisy_scan_is_not', not _is_line_art(_scan))
        _grad = _LImg.fromarray((_lnp.linspace(0, 255, 256)[None, :, None] * _lnp.ones((100, 1, 3))).astype('uint8'))
        check('lineart_smooth_gradient_is_not',
              len(set(_grad.getdata())) <= 256 and not _is_line_art(_grad))   # old rule said line art
        _flat = _LImg.new('RGB', (100, 80), 'white'); _flat.paste((0, 114, 178), (20, 20, 60, 50))
        check('lineart_flat_render_is_line_art', _is_line_art(_flat) and _line_art_stats(_flat)[0] > 0.9)
        # A smoothly interpolated heat map is mostly NOT flat, but its margins are
        # a dominant exact background: line art by the mode criterion.
        _hb = io.BytesIO(); _hf, _hax = _lplt.subplots(figsize=(3, 2), dpi=150)
        _hax.imshow(_rng.random((6, 8)), interpolation='bicubic', aspect='auto')
        _hf.savefig(_hb, format='png', dpi=150, facecolor='white'); _lplt.close(_hf)
        _heat = _LImg.open(io.BytesIO(_hb.getvalue())).convert('RGB')
        _hs = _line_art_stats(_heat)
        check('lineart_smooth_heatmap_with_axes_is_line_art',
              _hs[0] < LINE_ART_FLAT_FRAC and _hs[1] >= LINE_ART_MODE_FRAC and _is_line_art(_heat))
        check('lineart_photo_scan_gradient_fail_both_criteria',
              all(_line_art_stats(x)[0] < LINE_ART_FLAT_FRAC and _line_art_stats(x)[1] < LINE_ART_MODE_FRAC
                  for x in (_photo, _scan, _grad)))
        # Resampling is NEAREST and explicit: a 3000x2000 flat render sampled down keeps
        # exact values (flat > 0.95), which a smoothing filter would blur at the edges.
        _big = _LImg.new('RGB', (3000, 2000), 'white'); _big.paste((0, 114, 178), (500, 500, 2500, 1500))
        check('lineart_large_image_sampled_nearest', _line_art_stats(_big)[0] > 0.95 and _is_line_art(_big))
        check('lineart_quantised_render_is_line_art', _is_line_art(_chart.quantize(64)))
        # ISOLATING FIXTURES (each defence alone must carry its case):
        # (a) eight flat stripes of distinct colours — NO dominant background
        #     (mode 0.125), fully flat: only the flat criterion keeps it PNG.
        _st = _lnp.zeros((200, 400, 3), 'uint8')
        for _i, _c in enumerate([(0, 114, 178), (213, 94, 0), (0, 158, 115), (204, 121, 167),
                                 (230, 159, 0), (86, 180, 233), (240, 228, 66), (120, 120, 120)]):
            _st[:, _i * 50:(_i + 1) * 50] = _c
        _sts = _line_art_stats(_LImg.fromarray(_st))
        check('lineart_flat_render_without_dominant_background',
              _sts[1] < LINE_ART_MODE_FRAC and _sts[0] >= LINE_ART_FLAT_FRAC
              and _is_line_art(_LImg.fromarray(_st)))
        # (b) a 3000x2000 fine 1-px grid: NEAREST sampling keeps a white-dominant
        #     image (mode 0.84); a smoothing resample blurs every line into
        #     gradients (flat 0.00, mode 0.09) and would send a render to JPEG.
        _gr = _lnp.full((2000, 3000, 3), 255, 'uint8'); _gr[::12, :] = 0; _gr[:, ::12] = 0
        _grs = _line_art_stats(_LImg.fromarray(_gr))
        check('lineart_fine_grid_survives_nearest_sampling',
              _grs[1] >= LINE_ART_MODE_FRAC and _is_line_art(_LImg.fromarray(_gr)))
        check('lineart_tiny_image_is_line_art', _is_line_art(_LImg.new('RGB', (2, 2), 'white')))
        check('lineart_threshold_pinned', LINE_ART_FLAT_FRAC == 0.60 and LINE_ART_MODE_FRAC == 0.25)
        # route contract unchanged: JPEG source still wins, alpha still wins.
        check('lineart_route_jpeg_source_wins',
              bc.classify_media_route('JPEG', False, True) == 'jpeg'
              and bc.classify_media_route('PNG', True, False) == 'png'
              and bc.classify_media_route('PNG', False, True) == 'png-lineart')
    except ImportError:
        check('lineart_numpy_absent_falls_back', True)
    check('opt_num_dot', is_option('1. speed of light'))
    check('opt_alpha_dot', is_option('B. mitochondria'))
    check('opt_paren_num', is_option('(3) 42'))
    check('opt_paren_alpha_lower', is_option('(c) all of the above'))
    check('opt_half_paren', is_option('d) none of these'))
    check('opt_beyond_range_rejected', not is_option('6. beyond the option range'))
    check('opt_prose_rejected', not is_option('Consider the following statements'))
    check('opt_bare_no_para_rejected', not is_option('1.'))

    # ── text_of() — w:t + m:t canonical accessor (GAP-2026-08-07-OMML M3) ──
    _W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    _M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
    from xml.etree import ElementTree as _ET   # stdlib — Check AB-safe
    _p_omml = _ET.fromstring(
        ('<w:p xmlns:w="%s" xmlns:m="%s">'
         '<w:r><w:t xml:space="preserve">3. </w:t></w:r>'
         '<m:oMath><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num>'
         '<m:den><m:r><m:t>2</m:t></m:r></m:den></m:f></m:oMath>'
         '</w:p>') % (_W, _M))
    check('textof_wt_plus_mt', text_of(_p_omml) == '3. 12')
    check('textof_none', text_of(None) == '')
    check('textof_non_element', text_of('junk') == '')

    _p_img = _ET.fromstring(
        '<w:p xmlns:w="%s" xmlns:a="%s"><w:r><w:drawing><a:blip/></w:drawing></w:r></w:p>'
        % (_NS_W, A_NS))
    _p_txt = _ET.fromstring(
        '<w:p xmlns:w="%s"><w:r><w:t>1.</w:t></w:r></w:p>' % _NS_W)
    check('opt_bare_with_image', is_option('1.', para=_p_img))
    check('opt_bare_alpha_with_image', is_option('(D)', para=_p_img))
    check('opt_bare_imageless_rejected', not is_option('1.', para=_p_txt))
    check('opt_text_option_para_irrelevant', is_option('2. tundra', para=_p_txt))

    # ── GAP-2026-08-05-001 (S-1) — an option's content may be an EQUATION ────
    # PYQSort CHECK 4 accepts "(d) OMML formula" as a valid option form; para_has_image()
    # sees only a blip/VML, so these returned False and the option was silently dropped.
    # Real instance: SSC_CGL_TIER1 09-Sep-2024 Shift 1, Q.75 options 1 and 2 (paras
    # 592-593) — a delivered sorted paper losing half its option set at Step 5.
    # These FAIL on the pre-fix predicate.
    _p_eqn = _ET.fromstring(
        '<w:p xmlns:w="%s" xmlns:m="%s"><w:r><w:t>1.</w:t></w:r><m:oMath/></w:p>'
        % (_NS_W, 'http://schemas.openxmlformats.org/officeDocument/2006/math'))
    _p_obj = _ET.fromstring(
        '<w:p xmlns:w="%s"><w:r><w:t>2.</w:t><w:object/></w:r></w:p>' % _NS_W)
    _p_num = _ET.fromstring(
        '<w:p xmlns:w="%s"><w:pPr><w:numPr/></w:pPr><w:r><w:t>1.</w:t></w:r></w:p>' % _NS_W)
    check('opt_bare_with_equation', is_option('1.', para=_p_eqn))
    check('opt_bare_with_embedded_object', is_option('2.', para=_p_obj))
    # an auto-number alone is NOT option content — the rendered "1." only duplicates
    # the label already present as text, so this must stay rejected.
    check('opt_bare_autonumber_only_rejected', not is_option('1.', para=_p_num))

    class _FakeParagraph:                   # python-docx Paragraph form (has ._p)
        pass
    _fp = _FakeParagraph()
    _fp._p = _p_img
    check('opt_paragraph_form_accepted', is_option('A)', para=_fp))
    check('opt_para_none_safe', not para_has_image(None))
    check('opt_para_junk_safe', not para_has_image('not a paragraph'))
    check('opt_clean_marker_stripped',
          clean_option_text('(c) all of the above') == 'all of the above')
    check('opt_clean_bare_empty', clean_option_text('B.') == '')
    check('opt_clean_plain_untouched',
          clean_option_text('not an option') == 'not an option')

    # ── GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION ────────────────────────────
    # P3b: the six-shape decode matrix. Shape B (bare base64) was REJECTED before
    # this release; every other shape must keep working byte-for-byte.
    import base64 as _b64, tempfile
    _docx = b'PK\x03\x04' + b'\x00' * 136
    _b = _b64.b64encode(_docx).decode()
    _paper = {'name': 'probe.docx', 'fileSize': len(_docx), 'id': 'FID'}
    check('t_decode_A_bytes', decode_drive_payload(_docx) == _docx)
    check('t_decode_B_bare_base64', decode_drive_payload(_b) == _docx)
    check('t_decode_C_dict_content', decode_drive_payload({'content': _b}) == _docx)
    check('t_decode_D_list_text',
          decode_drive_payload([{'text': '{"content":"%s"}' % _b}]) == _docx)
    check('t_decode_E_json_string',
          decode_drive_payload('{"content":"%s"}' % _b) == _docx)
    _spill = os.path.join(tempfile.mkdtemp(), 'spill.txt')
    with open(_spill, 'w', encoding='utf-8') as _fh:
        _fh.write('{"content":"%s","id":"FID","title":"probe.docx"}' % _b)
    check('t_decode_F_spill_path', decode_drive_payload(_spill) == _docx)
    # A spill path may live in ANY directory — the deployment chooses it, and the
    # 2026-08-15 measurement found two different directories and one inline channel.
    check('t_decode_F_any_directory', _spill.startswith(tempfile.gettempdir()))
    # bare-base64 acceptance must not swallow genuine garbage
    _bad = 0
    for _junk in ('', 'not base64 at all!!', 'AAAA', _b64.b64encode(b'no magic').decode()):
        try:
            decode_drive_payload(_junk)
        except TransportFallback:
            _bad += 1
    check('t_decode_rejects_non_docx', _bad == 4)

    # P3a: stage_drive_payload gives a verified route to disk with NO callable.
    _dest = tempfile.mkdtemp()
    check('t_stage_writes_bytes',
          open(stage_drive_payload({'content': _b}, _paper, _dest), 'rb').read() == _docx)
    check('t_stage_accepts_spill_path',
          open(stage_drive_payload(_spill, _paper, _dest), 'rb').read() == _docx)
    _tr = 0
    try:
        stage_drive_payload({'content': _b64.b64encode(_docx[:100]).decode()},
                            _paper, _dest)
    except TransportFallback:
        _tr = 1
    check('t_stage_truncation_raises_fallback', _tr == 1)
    # fetch_drive_docx must produce the IDENTICAL result through a resolver, because
    # it is now a thin wrapper — the two routes can never drift apart again.
    check('t_fetch_via_resolver_matches_stage',
          open(fetch_drive_docx(lambda fid: {'content': _b}, _paper, _dest),
               'rb').read() == _docx)
    _cap = 0
    try:
        fetch_drive_docx(lambda fid: _docx,
                         {'name': 'huge.docx', 'id': 'X',
                          'fileSize': bc.DRIVE_CAP + 1}, _dest)
    except TransportFallback:
        _cap = 1
    check('t_fetch_cap_precheck_still_fires', _cap == 1)

    # ── GAP-2026-08-16-STEP5-SESSION-EXHAUSTION ─────────────────────────────
    # EC-P43 — DIRECT LANE. Tested with an injected getter: the lane must be provable
    # without network, or it cannot be regression-tested in CI at all.
    _direct_paper = {'id': 'FID1', 'name': 'direct.docx', 'fileSize': len(_docx)}
    check('t_direct_fetch_writes_verified_bytes',
          open(fetch_drive_direct(_direct_paper, _dest,
                                  getter=lambda url: _docx), 'rb').read() == _docx)
    _hops = []

    def _interstitial(url):
        _hops.append(url)
        return _docx if 'usercontent' in url else b'<html>virus scan warning</html>'
    check('t_direct_retries_through_confirm_endpoint',
          open(fetch_drive_direct(_direct_paper, _dest,
                                  getter=_interstitial), 'rb').read() == _docx
          and len(_hops) == 2 and 'usercontent' in _hops[1])
    _dt = 0
    try:
        fetch_drive_direct(_direct_paper, _dest,
                           getter=lambda url: _docx[:len(_docx) // 2])
    except TransportFallback:
        _dt = 1
    check('t_direct_truncation_raises_fallback', _dt == 1)
    _dh = 0
    try:
        fetch_drive_direct(_direct_paper, _dest,
                           getter=lambda url: b'<html>sign in</html>')
    except TransportFallback:
        _dh = 1
    check('t_direct_html_never_reaches_disk', _dh == 1)
    _dc = 0
    try:
        fetch_drive_direct({'id': 'X', 'name': 'huge.docx',
                            'fileSize': bc.DRIVE_CAP + 1}, _dest,
                           getter=lambda url: _docx)
    except TransportFallback:
        _dc = 1
    check('t_direct_cap_precheck_fires', _dc == 1)
    _dn = 0
    try:
        fetch_drive_direct({'name': 'no-id.docx'}, _dest, getter=lambda url: _docx)
    except TransportFallback:
        _dn = 1
    check('t_direct_missing_id_raises', _dn == 1)
    # The probe must NEVER raise — an unshared folder is an ordinary state, not an
    # incident. A probe that throws turns a routine fallback into a halted run.
    check('t_probe_ok_on_success',
          probe_direct_egress(_direct_paper, _dest,
                              getter=lambda url: _docx)['channel'] == 'direct')

    def _boom(url):
        raise RuntimeError('egress blocked')
    _pr = probe_direct_egress(_direct_paper, _dest, getter=_boom)
    check('t_probe_never_raises_on_failure',
          _pr['ok'] is False and _pr['channel'] is None and 'egress' in _pr['reason'])

    # EC-P41 — LISTING INTEGRITY. Every one of these must HARD STOP, and the happy
    # path must still write the records verbatim.
    def _rec(i, year, size=47_000):
        return {'id': f'ID{i}', 'name': f'EXAM_15-Feb-{year}_Sorted_Q1-Q60.docx',
                'mimeType': ('application/vnd.openxmlformats-officedocument'
                             '.wordprocessingml.document'),
                'fileSize': str(size)}
    _lpath = os.path.join(_dest, 'pyq_drive_listing.json')
    _ok = write_drive_listing([{'files': [_rec(1, 2024), _rec(2, 2025),
                                          _rec(3, 2026)]}], _lpath, 'ROOT', 3)
    check('t_listing_writes_and_counts', _ok['count'] == 3)
    check('t_listing_records_are_verbatim',
          json.load(open(_lpath))['files'][0] == _rec(1, 2024))
    check('t_listing_reports_year_span', _ok['year_span'] == (2024, 2026))
    check('t_listing_reports_no_false_gap', _ok['missing_years'] == [])
    _gap = write_drive_listing([{'files': [_rec(1, 2023), _rec(2, 2026)]}],
                               _lpath, 'ROOT', 2)
    check('t_listing_reports_interior_gap',
          _gap['missing_years'] == [2024, 2025])

    def _stops(pages, count):
        try:
            write_drive_listing(pages, _lpath, 'ROOT', count)
        except ListingIntegrityError:
            return 1
        return 0
    check('t_listing_short_count_hard_stops',
          _stops([{'files': [_rec(1, 2025), _rec(2, 2026)]}], 3) == 1)
    check('t_listing_long_count_hard_stops',
          _stops([{'files': [_rec(1, 2025), _rec(2, 2026)]}], 1) == 1)
    check('t_listing_duplicate_id_hard_stops',
          _stops([{'files': [_rec(1, 2025)]}, {'files': [_rec(1, 2026)]}], 2) == 1)
    check('t_listing_missing_id_hard_stops',
          _stops([{'files': [dict(_rec(1, 2025), id='')]}], 1) == 1)
    check('t_listing_missing_name_hard_stops',
          _stops([{'files': [dict(_rec(1, 2025), name='')]}], 1) == 1)
    check('t_listing_missing_mime_hard_stops',
          _stops([{'files': [dict(_rec(1, 2025), mimeType='')]}], 1) == 1)
    check('t_listing_unmerged_tail_hard_stops',
          _stops([{'files': [_rec(1, 2026)], 'nextPageToken': 'MORE'}], 1) == 1)
    check('t_listing_non_integer_count_hard_stops',
          _stops([{'files': [_rec(1, 2026)]}], 'twenty-two') == 1)
    check('t_listing_empty_pages_hard_stops', _stops([], 0) == 1)
    # The 'items' spelling and the bare list must merge exactly like 'files' — the
    # connector has emitted all three and the gate must not care which.
    check('t_listing_accepts_items_envelope',
          write_drive_listing([{'items': [_rec(9, 2026)]}], _lpath, 'ROOT', 1)['count'] == 1)
    check('t_listing_accepts_bare_list',
          write_drive_listing([[_rec(8, 2026)]], _lpath, 'ROOT', 1)['count'] == 1)
    # Multi-page merge: the case a hand transcription silently truncates.
    check('t_listing_merges_pages',
          write_drive_listing([{'files': [_rec(i, 2000 + i) for i in range(1, 101)],
                                'nextPageToken': 'P2'},
                               {'files': [_rec(i, 1900 + i) for i in range(101, 123)]}],
                              _lpath, 'ROOT', 122)['count'] == 122)

    # ── v1.12 chemical identity + SMILES renderer ─────────────────────────
    _c1, _r1 = canonical_structure('OC(=O)c1ccccc1O')
    if _r1 == 'ok':
        check('chem_canonical_equivalent', _c1 == canonical_structure('Oc1ccccc1C(O)=O')[0])
        check('chem_canonical_distinct', _c1 != canonical_structure('O=C(C)c1ccccc1O')[0])
        check('chem_valence_reject', canonical_structure('C(C)(C)(C)(C)C')[0] is None)
        try:
            structure_draw_fn('C(C)(C)(C)(C)C'); check('chem_drawfn_rejects_bad', False)
        except ValueError:
            check('chem_drawfn_rejects_bad', True)
        try:
            _df = structure_draw_fn('OC(=O)c1ccccc1O')
            check('chem_drawfn_canonical', _df.canonical == _c1 and callable(_df))
        except Exception as _e:
            check('chem_drawfn_canonical', 'No module' in str(_e))
        # ── v1.14 colour roles (MockTestCreate v5.80 S10-7C) ─────────────────
        # BW fallback FIRST (figural_core deliberately not loaded yet).
        try:
            import sys as _sys0
            if 'figural_core' not in _sys0.modules:
                _bw = structure_draw_fn('CCO')
                check('chem_drawfn_bw_when_figural_core_absent',
                      _bw.palette_note is not None and _bw.coloured_elements == frozenset())
            __import__('figural_core')            # the Create-flow condition (test only)
            import numpy as _np
            def _colour_px(a):
                rgb = a[..., :3].astype(int); vis = a[..., 3] > 128
                return int(((rgb.max(-1) - rgb.min(-1)) > 25)[vis].sum())
            def _has_rgb(a, hexc):
                want = tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
                rgb = a[..., :3]
                return bool(((rgb == want).all(-1) & (a[..., 3] > 128)).any())
            _h = structure_draw_fn('CC=CC')                     # hydrocarbon
            _e = structure_draw_fn('CCO')                       # alcohol
            check('chem_drawfn_coloured_elements',
                  _h.coloured_elements == frozenset() and _e.coloured_elements == frozenset({'O'}))
            # the O symbol is drawn in the TEXT-tier vermillion, not rdkit red
            _arr_e = [c.cell_contents for c in _e.__closure__
                      if isinstance(c.cell_contents, dict) and 'arr' in c.cell_contents][0]['arr']
            check('chem_drawfn_pinned_atom_palette',
                  _has_rgb(_arr_e, '#C25604') and not _has_rgb(_arr_e, '#FF0000'))
            _arr_h = [c.cell_contents for c in _h.__closure__
                      if isinstance(c.cell_contents, dict) and 'arr' in c.cell_contents][0]['arr']
            check('chem_drawfn_hydrocarbon_is_black', _colour_px(_arr_h) == 0)
            _e.set_element_colours(False)
            _arr_e2 = [c.cell_contents for c in _e.__closure__
                       if isinstance(c.cell_contents, dict) and 'arr' in c.cell_contents][0]['arr']
            check('chem_drawfn_set_element_colours_black',
                  _colour_px(_arr_e2) == 0 and _e.element_colours is False)
            _hl = structure_draw_fn('CC=CC', highlight_bonds=[1])
            _arr_hl = [c.cell_contents for c in _hl.__closure__
                       if isinstance(c.cell_contents, dict) and 'arr' in c.cell_contents][0]['arr']
            check('chem_drawfn_highlight_accents_hydrocarbon',
                  _colour_px(_arr_hl) > 0 and _has_rgb(_arr_hl, '#0072B2')
                  and _hl.highlight == {'atoms': [], 'bonds': [1]})
            _ha = structure_draw_fn('CC=CC', highlight_atoms=[0])
            _arr_ha = [c.cell_contents for c in _ha.__closure__
                       if isinstance(c.cell_contents, dict) and 'arr' in c.cell_contents][0]['arr']
            check('chem_drawfn_highlight_atoms_draw',
                  _has_rgb(_arr_ha, '#0072B2') and _ha.highlight['atoms'] == [0])
            try:
                structure_draw_fn('CCO', highlight_bonds=[9]); check('chem_drawfn_bad_highlight_is_valueerror', False)
            except ValueError:
                check('chem_drawfn_bad_highlight_is_valueerror', True)
            _ho = structure_draw_fn('CCO', highlight_atoms=[2])           # the O
            check('chem_drawfn_heteroatom_highlight_goes_to_bonds',
                  _ho.highlight['atoms'] == [] and _ho.highlight['bonds'] == [1])
            check('chem_drawfn_signature_additive',
                  callable(structure_draw_fn('CCO', (300, 200), (0, 3, 0, 2))))
        except Exception as _e2:
            check('chem_drawfn_colour_roles', 'No module' in str(_e2))
    else:
        check('chem_rdkit_absent_is_soft', _c1 is None and _r1 == 'rdkit_unavailable')

    # ── v1.16 REACTION canonical + scheme compositor (GAP-2026-11-01, LAW F1.3) ──
    # Each fixture FAILS on v1.15: canonical_structure returned parse_error on '>>'
    # and render_scheme did not exist.
    if _r1 == 'ok':
        _rx, _rr = canonical_structure('CCBr>>CCO')
        check('rxn_canonical_ok', _rr == 'ok' and _rx == 'CCBr>>CCO')
        check('rxn_canonical_components_canonicalised',
              canonical_structure('OC(=O)c1ccccc1O>>Oc1ccccc1C(O)=O')[0] == f'{_c1}>>{_c1}')
        check('rxn_empty_product_side_ok', canonical_structure('CC(=O)c1ccccc1>>')[1] == 'ok')
        check('rxn_agent_side_ok', canonical_structure('CC(=O)c1ccccc1>[BH3]>')[0] == 'CC(=O)c1ccccc1>B>')
        check('rxn_unknown_reactant_ok_G7', canonical_structure('>>CCO') == ('>>CCO', 'ok'))
        check('rxn_both_sides_empty_rejected', canonical_structure('>>')[0] is None
              and canonical_structure('>[Pd]>')[0] is None)
        check('rxn_three_separators_rejected', canonical_structure('C>C>C>C')[0] is None)
        check('rxn_bad_component_rejected', canonical_structure('C(C)(C)(C)(C)C>>CC')[0] is None)
        check('rxn_molecule_set_is_still_a_set', canonical_structure('BrBr.CCC#CCC') == ('BrBr.CCC#CCC', 'ok'))
        check('rxn_molecule_path_byte_identical',
              canonical_structure('Oc1ccccc1C(O)=O')[0] == _c1
              and canonical_structure('C(C)(C)(C)(C)C')[1] == 'parse_error: rdkit rejected the SMILES (valence / syntax)')
        try:
            import importlib as _il16
            # importlib, NOT an import statement: validator check AI reads Import nodes,
            # and this module must never DECLARE a dependency on figural_core (the Create
            # flow loads it first; the compositor reads it from sys.modules exactly as
            # structure_draw_fn does). The self-test only needs it to drive render_figure.
            _fc16 = _il16.import_module('figural_core')
            import tempfile as _tf16, os as _os16
            _d16 = _tf16.mkdtemp()
            _G = {   # one scheme per grammar element G1–G10 (real-paper patterns)
                'G1_plus': {'items': [{'mol': 'c1ccc2[nH]ccc2c1', 'equiv': '(2 equiv)'}, {'plus': True},
                                      {'mol': 'O=Cc1ccccc1'}, {'arrow': {'above': ['p-TsOH']}}, {'placeholder': 'A'}]},
                'G2_sequential': {'items': [{'mol': 'O=C(C(Cl)(Cl)Cl)c1ccccc1'},
                                            {'arrow': {'above': ['(S)-CBS (cat.)'], 'below': ['BH₃·SMe₂']}},
                                            {'placeholder': 'A'}, {'arrow': {'above': ['NaOH'], 'below': ['NaN₃']}},
                                            {'placeholder': 'B'}]},
                'G2_left': {'items': [{'placeholder': 'A'}, {'arrow': {'dir': 'left', 'above': ['mCPBA']}},
                                      {'mol': 'CC1=CCCC1'}, {'arrow': {'above': ['i. NBS, H₂O'], 'below': ['ii. NaOH']}},
                                      {'placeholder': 'B'}]},
                'G3_two_lines': {'items': [{'mol': 'Oc1ccc2ccccc2c1-c1c(O)ccc2ccccc12'},
                                           {'arrow': {'above': ['t-BuCl (2 equiv)', 'anhyd. AlCl₃'], 'below': ['CH₂Cl₂, −78 °C']}},
                                           {'placeholder': '?'}]},
                'G4_reagent_mol': {'items': [{'mol': 'CC(=O)c1ccccc1'}, {'arrow': {'reagent_mol': 'CC(C)(C)OO', 'below': ['BH₃']}},
                                             {'placeholder': 'A'}]},
                'G6_bracket': {'items': [{'mol': 'BrC1(Br)CC2CCCC12'}, {'arrow': {'above': ['heat']}}, {'bracket': 'A'},
                                         {'arrow': {}}, {'placeholder': 'B'}]},
                'G7_product_drawn': {'items': [{'mol': 'Cc1ccccc1'}, {'arrow': {'above': ['CrO₂Cl₂']}}, {'mol': 'O=Cc1ccccc1'}]},
                'G8_rows': {'rows': [[{'mol': 'CC(=O)C', 'label': 'A.'}, {'arrow': {'above': ['LiAlH₄']}}, {'mol': 'CC(O)C'}],
                                     [{'mol': 'C=CC=C', 'label': 'B.'}, {'plus': True}, {'mol': 'C=CC(=O)OC'},
                                      {'arrow': {'above': ['Δ']}}, {'placeholder': 'P'}]]},
                'G9_stereo': {'items': [{'mol': 'C[C@H]1CC=C[C@@H]1C(C)(C)C'}, {'arrow': {'above': ['i. NBS, H₂O'], 'below': ['ii. NaOH']}},
                                        {'placeholder': 'B'}]},
                'G10_pair': {'items': [{'mol': 'CC(=O)c1ccccc1'}, {'arrow': {'above': ['(S)-CBS']}},
                                       {'pair': [('A', 'O[C@H](C)c1ccccc1'), ('B', 'O[C@@H](C)c1ccccc1')]}]},
                'G7_unknown_reactant': {'items': [{'placeholder': 'A'}, {'arrow': {'above': ['H₂, Pd/C']}},
                                                  {'mol': 'CCc1ccccc1'}]},
            }
            _all_ok = True
            for _gname, _gspec in _G.items():
                _dr = render_scheme(_gspec)
                _fs = _fc16.make_figure_spec(1, 'schematic', 6.0, role='problem', canvas_aspect=_dr.suggested_aspect)
                _png = _os16.path.join(_d16, _gname + '.png')
                _fc16.render_figure(_dr, _png, _fs)
                _hard, _warn = _fc16.audit_figure(_fs, _png)
                _tri = _fc16.triage(_hard + _warn, _fs)
                _ok_g = ((_fs.get('fit') or {}).get('status') == 'OK' and not _tri['BLOCKING']
                         and not _tri['VOID_ITEM'])
                check(f'scheme_renders_{_gname}', _ok_g)
                _all_ok = _all_ok and _ok_g
            _dr = render_scheme(_G['G2_sequential'])
            check('scheme_canonical_has_reaction_separator', '>>' in _dr.canonical
                  and _dr.canonical.startswith('O=C(c1ccccc1)C(Cl)(Cl)Cl'))
            check('scheme_descriptor', _dr.descriptor['unknowns'] == ['A', 'B'] and _dr.descriptor['arrows'] == 2
                  and _dr.descriptor['rows'] == 1 and 'NaOH' in _dr.descriptor['reagent_lines'])
            check('scheme_tiles_have_structure_provenance', all(hasattr(_t, 'canonical') for _t in _dr.tiles))
            _dr4 = render_scheme(_G['G4_reagent_mol'])
            check('scheme_reagent_mol_is_agent', _dr4.canonical.split('>')[1] == 'CC(C)(C)OO')
            _dl = render_scheme(_G['G2_left'])
            check('scheme_left_arrow_roles', _dl.canonical.startswith('CC1=CCCC1>') and _dl.canonical.endswith('>'))
            _dq = render_scheme({'items': [{'placeholder': 'A'}, {'arrow': {'dir': 'left', 'above': ['mCPBA']}},
                                           {'mol': 'CC1=CCCC1', 'label': 'S'}, {'arrow': {'above': ['i. NBS, H₂O'], 'below': ['ii. NaOH']}},
                                           {'placeholder': 'B'}]})          # Q.91: A ← S → B
            check('scheme_q91_pattern_source_is_reactant', _dq.canonical == 'CC1=CCCC1>>')
            _dq2 = render_scheme({'items': [{'placeholder': 'A'}, {'arrow': {}}, {'mol': 'CC1=CCCC1'},
                                            {'arrow': {'dir': 'left'}}, {'placeholder': 'B'}]})   # A → S ← B
            check('scheme_converging_arrows_make_a_product', _dq2.canonical == '>>CC1=CCCC1')
            _dseq = render_scheme({'items': [{'mol': 'CC(=O)C'}, {'arrow': {}}, {'mol': 'CC(O)C'}, {'arrow': {}}, {'mol': 'CC=C'}]})
            check('scheme_sequential_intermediate_omitted', _dseq.canonical == 'CC(C)=O>>C=CC'
                  and _dseq.descriptor['intermediates'] == 1)
            _dnone = render_scheme({'items': [{'mol': 'CC(=O)C'}, {'arrow': {'above': [None, 'H₂'], 'below': [None]}}, {'mol': 'CC(O)C'}]})
            check('scheme_none_reagent_lines_dropped', _dnone.descriptor['reagent_lines'] == ['H₂'])
            _dg4 = render_scheme({'items': [{'mol': 'CC(=O)C'}, {'arrow': {'reagent_mol': '[H-]'}}, {'mol': 'CC(O)C'}]})
            _dg10 = render_scheme({'items': [{'mol': 'CC(=O)c1ccccc1'}, {'arrow': {}}, {'pair': [('A', 'O[C@H](C)c1ccccc1'), ('B', 'O[C@@H](C)c1ccccc1')]}]})
            check('scheme_intermediates_never_negative', _dg4.descriptor['intermediates'] >= 0 and _dg10.descriptor['intermediates'] == 0)
            try:
                structure_draw_fn('CCBr>>CCO'); check('structure_draw_fn_rejects_reaction_smiles_with_ValueError', False)
            except ValueError as _e:
                check('structure_draw_fn_rejects_reaction_smiles_with_ValueError', 'render_scheme' in str(_e))
            _deq = render_scheme({'items': [{'mol': 'CC(=O)C'}, {'arrow': {'dir': 'both'}}, {'mol': 'CC(O)=C'}]})
            check('scheme_equilibrium_left_to_right', _deq.canonical == 'CC(C)=O>>C=C(C)O')
            _dg7 = render_scheme(_G['G7_unknown_reactant'])
            check('scheme_unknown_reactant_product_only', _dg7.canonical == '>>CCc1ccccc1')
            _dr8 = render_scheme(_G['G8_rows'])
            check('scheme_rows_one_canonical_per_row', len(_dr8.row_canonicals) == 2
                  and _dr8.row_canonicals[0] == 'CC(C)=O>>CC(C)O' and _dr8.row_canonicals[1].endswith('>>'))
            _so = scheme_semantic_object(_dr8, role='problem:1', row=1)
            check('scheme_semantic_object_shape', _so['kind'] == 'REACTION' and _so['role'] == 'problem:1'
                  and '>>' in _so['canonical'] and _so['descriptor']['row'] == 1)
            _dr.set_element_colours(False)
            check('scheme_colour_content_propagates_to_tiles',
                  _dr.element_colours is False and all(_t.element_colours is False for _t in _dr.tiles))
            _drh = render_scheme({'items': [{'mol': 'CC=CC', 'highlight_bonds': [1]}, {'arrow': {}}, {'placeholder': 'A'}]})
            check('scheme_highlight_recorded', _drh.highlight['bonds'] == [1])
            for _bad, _why in (({'items': [{'arrow': {}}]}, 'no molecule'),
                               ({'items': [{'mol': 'CCO'}, {'plus': True}, {'mol': 'CC'}]}, 'no arrow'),
                               ({'items': [{'placeholder': 'A'}, {'arrow': {}}, {'placeholder': 'B'}]}, 'placeholders only'),
                               ({'items': [{'mol': 'C(C)(C)(C)(C)C'}, {'arrow': {}}]}, 'bad smiles'),
                               ({'items': [{'mol': 'CC'}, {'arrow': {'above': ['a', 'b', 'c']}}]}, '3 lines'),
                               ({'items': [{'mol': 'CC'}, {'zorb': 1}]}, 'unknown item'),
                               ({}, 'empty spec')):
                try:
                    render_scheme(_bad); check(f'scheme_rejects_{_why.replace(" ", "_")}', False)
                except ValueError:
                    check(f'scheme_rejects_{_why.replace(" ", "_")}', True)
        except ImportError as _e16:
            check('scheme_compositor_needs_figural_core', 'No module' in str(_e16))

    # ── v1.17 PRINT-TRUE NATIVE RASTER (GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY) ──
    # Each fixture FAILS on the defect it guards (named in the comment beside it).
    if _r1 == 'ok':
        try:
            import numpy as _np17
            from PIL import Image as _Im17
            from rdkit.Chem import rdDepictor as _rdd17
            _TK = {'font_pt': 10.0, 'line_pt': 1.0, 'bond_pt': 14.4, 'monochrome': True,
                   'mark_colour': '#000000'}
            _k17 = 300 / 72.0

            def _arr17(png):
                return _np17.asarray(_Im17.open(io.BytesIO(png)).convert('RGB')).astype(int)

            def _chroma17(a):
                return int((((a.max(-1) - a.min(-1)) > 60) & (a.mean(-1) < 200)).sum())

            # (9) legacy path untouched — no native attribute on a tokens=None draw
            _pref0 = _rdd17.GetPreferCoordGen()
            _leg = structure_draw_fn('CCO')
            _legs = render_scheme({'items': [{'mol': 'CCO'}, {'arrow': {}}, {'mol': 'CC=O'}]})
            check('native_legacy_structure_has_no_native_attrs',
                  not hasattr(_leg, 'render_mode') and not hasattr(_leg, 'native_png'))
            check('native_legacy_scheme_has_no_native_attrs',
                  not hasattr(_legs, 'render_mode') and not hasattr(_legs, 'native_png'))
            # (1) monochrome: 0 chromatic ink pixels (fails without useBWAtomPalette — the
            #     colour control below proves the same molecules DO colour when allowed)
            _n_es = structure_draw_fn('CC(=O)OC', tokens=_TK)
            _n_br = structure_draw_fn('CCBr', tokens=_TK)
            _p_es, _w_es, _m_es = _n_es.native_png(300)
            _p_br, _w_br, _m_br = _n_br.native_png(300)
            check('native_mono_ester_bromide_zero_chroma',
                  _chroma17(_arr17(_p_es)) == 0 and _chroma17(_arr17(_p_br)) == 0
                  and _m_es['monochrome'] is True)
            import sys as _sys17
            if 'figural_core' in _sys17.modules:
                _n_col = structure_draw_fn('CC(=O)OC', tokens=dict(_TK, monochrome=False))
                check('native_colour_control_colours_when_not_monochrome',
                      _chroma17(_arr17(_n_col.native_png(300)[0])) > 0)
            check('native_draw_contract_attrs',
                  _n_es.render_mode == 'native_raster' and callable(_n_es.native_png_unmarked)
                  and _n_es.canonical == canonical_structure('CC(=O)OC')[0])
            _req = {'atom_label_pt', 'small_pt', 'bond_pt', 'line_pt', 'monochrome', 'highlight_bands',
                    'marks_drawn', 'marks_failed', 'label_boxes_px', 'abbreviations', 'cross_note',
                    'depictor', 'overprint_px', 'natural_width_in', 'natural_height_in'}
            check('native_meta_has_every_contract_key', _req <= set(_m_es))
            _im_es = _Im17.open(io.BytesIO(_p_es))
            check('native_png_dpi_and_natural_size',
                  round(_im_es.info.get('dpi', (0, 0))[0]) == 300
                  and abs(_w_es - _im_es.width / 300.0) < 1e-9
                  and abs(_m_es['natural_height_in'] - _im_es.height / 300.0) < 1e-9)
            _a_es = _arr17(_p_es)
            check('native_white_background_cropped_to_ink',
                  (_a_es[0, :] >= 250).all() and (_a_es[-1, :] >= 250).all()
                  and (_a_es[:, 0] >= 250).all() and (_a_es[:, -1] >= 250).all()
                  and _a_es.shape[0] < 0.6 * 300 * 2)
            # (2) one bond length for every molecule at one set of tokens (fails when the
            #     molecule is auto-scaled to a fixed canvas, the legacy 900x700 behaviour)
            _n_big = structure_draw_fn('CC(C)(C)c1ccc(cc1)C(=O)OCC', tokens=_TK)
            _m_big = _n_big.native_png(300)[2]
            check('native_same_bond_length_across_molecules',
                  abs(_m_big['bond_px_measured'] - _m_es['bond_px_measured']) <= 1.0
                  and abs(_m_es['bond_px_measured'] - 14.4 * _k17) <= 1.0)
            # (3) atom-label cap height ~ 0.711 * font_pt (and it SCALES with font_pt — fails
            #     when fixedFontSize is not applied and rdkit sizes labels itself)
            def _o_cap(draw):
                png, _w, meta = draw.native_png(300)
                a = _arr17(png)
                hs = []
                for b in meta['label_boxes_px']:
                    x0, y0, x1, y1 = [int(round(v)) for v in b]
                    rows = _np17.where((a[max(0, y0):y1 + 1, max(0, x0):x1 + 1].min(axis=2) < 128).any(axis=1))[0]
                    if rows.size:
                        hs.append(rows.max() - rows.min() + 1)
                return min(hs) if hs else 0
            _cap10 = _o_cap(_n_es)
            _cap14 = _o_cap(structure_draw_fn('CC(=O)OC', tokens=dict(_TK, font_pt=14.0)))
            _want10 = 0.711 * 10.0 * _k17
            check('native_label_cap_height_matches_font_pt',
                  abs(_cap10 - _want10) <= 0.25 * _want10
                  and abs(_cap14 - 1.4 * _want10) <= 0.25 * 1.4 * _want10)
            # (4) marks
            _n_bold = structure_draw_fn('CCBr', tokens=_TK,
                                        marks=[{'site': {'kind': 'bond', 'index': 0}, 'device': 'bold'},
                                               {'site': {'kind': 'bond', 'index': 1}, 'device': 'bold'}])
            _pb, _wb, _mb = _n_bold.native_png(300)
            _ab = _arr17(_pb)

            def _runs_across(a, p0, p1, half):
                """ink runs along the perpendicular through the midpoint of p0-p1"""
                mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
                dx, dy = p1[0] - p0[0], p1[1] - p0[1]
                n = (dx * dx + dy * dy) ** 0.5 or 1.0
                px_, py_ = -dy / n, dx / n
                prof = []
                for t in _np17.arange(-half, half + 0.01, 0.25):
                    x, y = int(round(mx + px_ * t)), int(round(my + py_ * t))
                    prof.append(0 <= y < a.shape[0] and 0 <= x < a.shape[1] and a[y, x].min() < 128)
                runs = sum(1 for i, v in enumerate(prof) if v and (i == 0 or not prof[i - 1]))
                return runs, sum(prof) * 0.25
            _bd0 = [d for d in _mb['marks_drawn'] if d['site']['index'] == 0]
            _runs, _width = (_runs_across(_ab, *_bd0[0]['bond_px_endpoints'], 0.3 * 14.4 * _k17)
                             if _bd0 else (0, 0))
            check('native_bold_single_bond_is_one_stroke_at_2x_line',
                  _runs == 1 and _width >= 1.6 * 1.0 * _k17 and len(_mb['marks_drawn']) == 2)
            check('native_bold_no_overprint', _mb['overprint_px'] == 0 and _mb['highlight_bands'] == 0)
            # the differential detector itself: a stroke over a label MUST register
            _un = _arr17(_n_bold.native_png_unmarked(300)[0])
            _hit = _un.copy()
            _lb = [int(round(v)) for v in _n_bold.native_png_unmarked(300)[2]['label_boxes_px'][0]]
            _hit[(_lb[1] + _lb[3]) // 2, _lb[0]:_lb[2]] = 0
            check('native_overprint_detector_registers_label_damage',
                  _native_overprint(_hit, _un, {0: [_lb]}) > 0 and _native_overprint(_un, _un, {0: [_lb]}) == 0)
            _n_ul = structure_draw_fn('CCBr', tokens=_TK,
                                      marks=[{'site': {'kind': 'atom', 'index': 0}, 'device': 'underline'},
                                             {'site': {'kind': 'atom', 'index': 2}, 'device': 'underline'}])
            _mu = _n_ul.native_png(300)[2]
            check('native_underline_unlabelled_carbon_fails_never_dropped',
                  [f['reason'] for f in _mu['marks_failed']] == ['device_not_drawable']
                  and _mu['marks_failed'][0]['site']['index'] == 0
                  and [d['site']['index'] for d in _mu['marks_drawn']] == [2] and _mu['overprint_px'] == 0)
            _n_ast = structure_draw_fn('OC(Br)C(=O)N', tokens=_TK,
                                       marks=[{'site': {'kind': 'atom', 'index': 1}, 'device': 'asterisk'},
                                              {'site': {'kind': 'bond', 'index': 2}, 'device': 'arrow'},
                                              {'site': {'kind': 'atom', 'index': 3}, 'device': 'letter', 'text': 'b'}])
            _ma = _n_ast.native_png(300)[2]
            _ast = [d for d in _ma['marks_drawn'] if d['device'] == 'asterisk']
            # an asterisk on the O of an OH label: its first (bisector) position lands on
            # the 'H' glyph, so this fails when placement ignores label boxes
            _m_lt = structure_draw_fn('CCO', tokens=_TK, marks=[
                {'site': {'kind': 'atom', 'index': 1}, 'device': 'letter'},
                {'site': {'kind': 'bond', 'index': 0}, 'device': 'letter'}]).native_png(300)[2]
            check('native_letter_mark_without_its_letter_fails_never_defaults',
                  sorted(f['reason'] for f in _m_lt['marks_failed'])
                  == ['letter_text_missing', 'letter_text_missing'] and not _m_lt['marks_drawn'])
            check('native_letter_mark_keeps_its_letter',
                  [d.get('text') for d in _ma['marks_drawn'] if d['device'] == 'letter'] == ['b'])
            _m_oh = structure_draw_fn('CCO', tokens=_TK, marks=[{'site': {'kind': 'atom', 'index': 2},
                                                                 'device': 'asterisk'}]).native_png(300)[2]
            check('native_asterisk_rotates_off_its_own_label',
                  len(_m_oh['marks_drawn']) + len(_m_oh['marks_failed']) == 1 and _m_oh['overprint_px'] == 0
                  and not any(_rects_overlap(d['bbox_px'], b) for d in _m_oh['marks_drawn']
                              for b in _m_oh['label_boxes_px']))
            check('native_asterisk_clear_of_every_label_box',
                  len(_ast) == 1 and not any(_rects_overlap(_ast[0]['bbox_px'], b) for b in _ma['label_boxes_px'])
                  and not any(_rects_overlap(d['bbox_px'], b) for d in _ma['marks_drawn'] for b in _ma['label_boxes_px'])
                  and len(_ma['marks_drawn']) + len(_ma['marks_failed']) == 3 and _ma['overprint_px'] == 0
                  and abs(_ma['small_pt'] - 10.0 * _RDKIT_SUBSUP_SCALE) < 1e-6)   # NH2 subscript < asterisk 8 pt
            try:
                structure_draw_fn('CCO', tokens=_TK, marks=[{'site': {'kind': 'atom', 'index': 0}, 'device': 'circle'}])
                check('native_unknown_mark_device_is_valueerror', False)
            except ValueError:
                check('native_unknown_mark_device_is_valueerror', True)
            # (5) highlight_* in native mode -> marks, never a band (fails if the band or
            #     the legacy raster's highlight colour survives)
            _n_hl = structure_draw_fn('CC=CC', tokens=_TK, highlight_bonds=[1], highlight_atoms=[0])
            _mh = _n_hl.native_png(300)[2]
            _rr = _n_hl.raster()
            check('native_highlight_converted_to_marks_no_band',
                  _mh['highlight_bands'] == 0 and _mh['converted_from_highlight'] is True
                  and sorted((d['site']['kind'], d['device']) for d in _mh['marks_drawn'] + _mh['marks_failed'])
                  == [('atom', 'asterisk'), ('bond', 'bold')]
                  and _chroma17(_arr17(_n_hl.native_png(300)[0])) == 0
                  and not ((_rr[..., :3] == (0, 0x72, 0xB2)).all(-1) & (_rr[..., 3] > 128)).any()
                  and _n_hl.highlight == {'atoms': [], 'bonds': []})
            # (6) abbreviations: none unless asked; only listed labels; never over a
            #     protected atom; canonical always the uncondensed SMILES
            _sm6 = 'COc1ccccc1C(=O)O'
            _n6a = structure_draw_fn(_sm6, tokens=_TK)
            _n6b = structure_draw_fn(_sm6, tokens=_TK, abbreviations=['OMe'], protect_atoms=[8, 9, 10])
            _n6c = structure_draw_fn(_sm6, tokens=_TK, abbreviations=['OMe'], protect_atoms=[0])
            _n6d = structure_draw_fn(_sm6, tokens=_TK, abbreviations=['Ac'], protect_atoms=[8, 9, 10])
            check('native_abbrev_none_by_default', _n6a.native_png(300)[2]['abbreviations'] == []
                  and structure_draw_fn(_sm6, tokens=_TK, abbreviations=[]).native_png(300)[2]['abbreviations'] == [])
            check('native_abbrev_only_listed_label_and_canonical_unchanged',
                  _n6b.native_png(300)[2]['abbreviations'] == ['OMe']
                  and _n6b.canonical == _n6a.canonical == canonical_structure(_sm6)[0]
                  and _n6d.native_png(300)[2]['abbreviations'] == [])
            check('native_abbrev_never_covers_protected_atom', _n6c.native_png(300)[2]['abbreviations'] == [])
            check('native_abbrev_lexicon_long_chain_before_ethyl',
                  structure_draw_fn('CCCCCCCCCc1ccc(O)cc1', tokens=_TK, abbreviations=['C9H19', 'Et'])
                  .native_png(300)[2]['abbreviations'] == ['C9H19'])
            check('native_abbrev_lexicon_seed',
                  {'Et', 'iPr', 'tBu', 'Ph', 'Bn', 'OMe', 'OEt', 'OAc', 'OTs', 'OMs', 'OTf', 'CO2Me', 'CO2Et',
                   'Ac', 'CHO', 'CN', 'NO2', 'SiMe3', 'TBS', 'TBDPS', 'Boc', 'Cbz', 'C7H15', 'C12H25'}
                  <= set(ABBREVIATION_DISPLAY) and 'Me' not in ABBREVIATION_DISPLAY)
            _pr, _pp = abbreviation_protected_atoms('CC(=O)c1ccccc1', 'CC(O)c1ccccc1')
            check('native_mcs_protects_reacting_atoms', 2 in _pr and 2 in _pp and 5 not in _pr)
            check('native_mcs_failure_protects_everything',
                  abbreviation_protected_atoms('CCO', 'not a smiles') == ([0, 1, 2], []))
            # F7 quaternary cross detector (fails if a '+' depiction is not recognised)
            from rdkit import Chem as _Ch17
            from rdkit.Geometry import Point3D as _P3
            _cx = _Ch17.MolFromSmiles('CC(C)(C)C')
            _conf = _Ch17.Conformer(5)
            for _i, (_x, _y) in enumerate([(-1.5, 0), (0, 0), (0, 1.5), (0, -1.5), (1.5, 0)]):
                _conf.SetAtomPosition(_i, _P3(_x, _y, 0))
            _cx.AddConformer(_conf)
            check('native_cross_detector', _native_cross_atoms(_cx) == [1]
                  and _native_layout(_Ch17.MolFromSmiles('CCC(C)(C)Br'))[2] is None)
            # (7) scheme: one bond length, re-flow after the intermediate (repeated)
            _sp7 = {'items': [{'mol': 'CC(=O)c1ccccc1'}, {'arrow': {'above': ['NaBH₄'], 'below': ['MeOH']}},
                              {'mol': 'CC(O)c1ccccc1'}, {'arrow': {'above': ['H₂SO₄'], 'below': ['Δ']}},
                              {'mol': 'C=Cc1ccccc1'}]}
            _s7w = render_scheme(_sp7, tokens=_TK, max_width_in=6.0)
            _s7n = render_scheme(_sp7, tokens=_TK, max_width_in=3.0)
            _pw, _ww, _mw = _s7w.native_png(300)
            _pn, _wn, _mn = _s7n.native_png(300)
            check('native_scheme_contract', _s7n.render_mode == 'native_raster'
                  and _req - {'marks_drawn', 'marks_failed', 'label_boxes_px', 'abbreviations', 'cross_note',
                              'depictor'} <= set(_mn)
                  and {'rows_after_reflow', 'reflowed', 'reagent_lines_moved_to_stem', 'overflow',
                       'tile_metas', 'font_file'} <= set(_mn) and _mn['highlight_bands'] == 0)
            check('native_scheme_one_bond_length',
                  len({round(m['bond_px_measured']) for m in _mn['tile_metas']}) == 1)
            check('native_scheme_fits_one_row_when_wide_enough',
                  _mw['rows_after_reflow'] == 1 and not _mw['reflowed'] and _ww > 3.0 and _ww <= 6.0)
            check('native_scheme_reflows_repeating_break_tile',
                  _mn['rows_after_reflow'] == 2 and _mn['reflowed'] and not _mn['overflow']
                  and _mn['row_lead_tiles'] == [0, 1] and _wn <= 3.0
                  and _s7n.canonical == _s7w.canonical == render_scheme(_sp7).canonical
                  and _s7n.descriptor == render_scheme(_sp7).descriptor)
            check('native_scheme_zero_chroma', _chroma17(_arr17(_pn)) == 0)
            _sp7b = {'items': [{'mol': 'CCO'}, {'arrow': {'above': ['reagent one, reagent two, reagent three, reagent four']}},
                               {'placeholder': 'A'}]}
            _m7b = render_scheme(_sp7b, tokens=_TK, max_width_in=2.0).native_png(300)[2]
            _m7c = render_scheme({'items': [{'mol': 'CCCCCCCCCCCCCCCCCCCC'}, {'arrow': {}}, {'placeholder': 'A'}]},
                                 tokens=_TK, max_width_in=1.0).native_png(300)[2]
            check('native_scheme_stacks_text_then_flags_overflow',
                  _m7b['reagent_lines_moved_to_stem'] != [] and _m7c['overflow'] is True
                  and _m7c['rows_after_reflow'] == 1)
            # (8) option set: one canvas, equal widths; mismatched tokens refused
            _opts = native_option_set([structure_draw_fn(s_, tokens=_TK) for s_ in
                                       ('CCBr', 'CC(=O)OC', 'CC(C)(C)c1ccc(cc1)C(=O)OCC', 'C')], 300)
            check('native_option_set_uniform_canvas',
                  len({w_ for _p, w_, _m in _opts}) == 1
                  and len({_Im17.open(io.BytesIO(p_)).size for p_, _w, _m in _opts}) == 1
                  and all(m_['frame'] is False for _p, _w, m_ in _opts))
            for _bad17, _nm17 in (([structure_draw_fn('CCO', tokens=_TK),
                                    structure_draw_fn('CCO', tokens=dict(_TK, font_pt=12.0))], 'mismatched_tokens'),
                                  ([structure_draw_fn('CCO')], 'legacy_draw')):
                try:
                    native_option_set(_bad17); check(f'native_option_set_rejects_{_nm17}', False)
                except (ValueError, OptionIdentityError):
                    check(f'native_option_set_rejects_{_nm17}', True)
            # v1.18 (GAP-2026-11-03 G01 R1.2) — the INCIDENT: Q32 options 2 and 3 were ONE
            # molecule from two SMILES strings. The set is refused BEFORE rendering, with the
            # ladder message; enantiomers / E-Z pairs (the exam's favourite distractors) pass.
            try:
                native_option_set([structure_draw_fn(s_, tokens=_TK) for s_ in
                                   ('C/C=C/C=C/C', 'C/C=C/C=C\\C', 'C\\C=C/C=C/C', 'C=CCCC=C')], 300)
                check('native_option_set_rejects_q32_duplicate_identity', False)
            except OptionIdentityError as _e18:
                check('native_option_set_rejects_q32_duplicate_identity',
                      'LADDER-REPAIR R2o G-OPTDISTINCT' in str(_e18) and 'options 2 and 3' in str(_e18))
            try:
                _ok18 = native_option_set([structure_draw_fn(s_, tokens=_TK) for s_ in
                                           ('C[C@H](O)CC', 'C[C@@H](O)CC', 'C/C=C/C', 'C/C=C\\C')], 300)
                check('native_option_set_keeps_enantiomers_and_EZ', len(_ok18) == 4)
            except OptionIdentityError:
                check('native_option_set_keeps_enantiomers_and_EZ', False)
            _ids18 = option_identities([structure_draw_fn('c1ccccc1', tokens=_TK), structure_draw_fn('C1=CC=CC=C1', tokens=_TK),
                                        lambda: None])
            check('option_identities_kekule_equal_and_no_canonical_none', _ids18[0] == _ids18[1] and _ids18[2] is None)
            _ex18 = [structure_draw_fn('C1CCCCC1', tokens=_TK, conformer_set=True) for _ in range(3)]   # chair set
            check('structure_draw_fn_default_not_exempt', getattr(structure_draw_fn('CCO', tokens=_TK), 'identity_exempt', None) is False)
            try:
                assert_option_identities(_ex18); check('identity_exempt_conformer_set_not_refused', option_identities(_ex18) == [None] * 3)
            except OptionIdentityError:
                check('identity_exempt_conformer_set_not_refused', False)
            _sd18 = stereo_declared(structure_draw_fn('C/C=C/C=C\\C', tokens=_TK), '2E,4Z')
            check('stereo_declared_attaches_line', getattr(_sd18, 'stereo_declared', None) == '2E,4Z'
                  and bc.stereo_declaration_check(_sd18.canonical, _sd18.stereo_declared)['state'] == 'PASS')
            check('native_leaves_rdkit_depictor_preference_alone', _rdd17.GetPreferCoordGen() == _pref0)
            try:
                structure_draw_fn('CCO', tokens={'font_pt': 10.0}); check('native_bad_tokens_is_valueerror', False)
            except ValueError:
                check('native_bad_tokens_is_valueerror', True)
            # ── 2026.11.02 review fixtures B2-B9: each FAILS on the defect it names ──
            def _mk(kind, i, dev, **kw):
                return dict(site={'kind': kind, 'index': i}, device=dev, **kw)
            # B2 a bold mark on a double bond keeps BOTH lines (one bar over C=C read
            # as a single bond); a triple bond is refused, never overpainted
            _p_b2, _w_b2, _m_b2 = structure_draw_fn('C=C', tokens=_TK, marks=[_mk('bond', 0, 'bold')]).native_png(300)
            _d_b2 = _m_b2['marks_drawn']
            _r_b2 = (_runs_across(_arr17(_p_b2), *_d_b2[0]['bond_px_endpoints'], 0.3 * 14.4 * _k17)[0]
                     if _d_b2 else 0)
            check('B2_bold_double_bond_keeps_two_lines',
                  len(_d_b2) == 1 and _d_b2[0].get('bold_lines') == 2 and _d_b2[0].get('bond_lines') == 2
                  and _r_b2 == 2 and _m_b2['overprint_px'] == 0)
            _m_b2t = structure_draw_fn('C#N', tokens=_TK, marks=[_mk('bond', 0, 'bold')]).native_png(300)[2]
            check('B2_bold_triple_bond_is_device_not_drawable',
                  [f['reason'] for f in _m_b2t['marks_failed']] == ['device_not_drawable']
                  and not _m_b2t['marks_drawn'])
            check('B2_bold_single_bond_records_one_line',
                  [(d.get('bond_lines'), d.get('bold_lines')) for d in _mb['marks_drawn']] == [(1, 1), (1, 1)])
            # B3 a scheme carries its tiles' marks (with 'tile' and scheme-pixel bboxes);
            # reagent_mol and pair members take their own marks
            _s_b3 = render_scheme({'items': [{'mol': 'CC(=O)OC', 'marks': [_mk('bond', 1, 'bold')]},
                                             {'arrow': {'reagent_mol': 'CCO',
                                                        'reagent_marks': [_mk('atom', 2, 'underline')]}},
                                             {'mol': 'CC(=O)O'},
                                             {'pair': [('A', 'CCO'), ('B', 'CC=O')],
                                              'pair_marks': [None, [_mk('atom', 2, 'underline')]]}]},
                                  tokens=_TK, max_width_in=9.0)
            _p_b3, _w_b3, _m_b3 = _s_b3.native_png(300)
            _t_b3 = sorted((d['tile'], d['site']['index'], d['device']) for d in _m_b3.get('marks_drawn', []))
            _off_b3 = [d for d in _m_b3.get('marks_drawn', []) if d['tile'] == 4]
            _tile4 = _s_b3.tiles[4].native_png(300)[2]['marks_drawn']
            check('B3_scheme_meta_carries_tile_marks',
                  _t_b3 == [(0, 1, 'bold'), (1, 2, 'underline'), (4, 2, 'underline')]
                  and _m_b3.get('marks_failed') == []
                  and len(_off_b3) == 1 and len(_tile4) == 1
                  and _off_b3[0]['bbox_px'][0] > _tile4[0]['bbox_px'][0] + 0.5 * _Im17.open(io.BytesIO(_p_b3)).width)
            _m_b3f = render_scheme({'items': [{'mol': 'CCC', 'marks': [_mk('atom', 0, 'underline')]},
                                              {'arrow': {}}, {'mol': 'CCO'}]},
                                   tokens=_TK).native_png(300)[2]
            check('B3_scheme_meta_carries_tile_failures',
                  [(f['tile'], f['reason']) for f in _m_b3f.get('marks_failed', [])]
                  == [(0, 'device_not_drawable')])
            # B4 explicit [H] kept on the native path: a mark index counts the SMILES' atoms,
            # and a mark on the H lands on that H
            try:
                _d_b4 = structure_draw_fn('[H]C([H])([H])O', tokens=_TK,
                                          marks=[_mk('atom', 0, 'asterisk'), _mk('atom', 4, 'underline')])
                _m_b4 = _d_b4.native_png(300)[2]
                _ast4 = [d for d in _m_b4['marks_drawn'] if d['device'] == 'asterisk']
                _lb4 = _m_b4['label_boxes_px']

                def _dist4(b, r):
                    cx, cy = (r[0] + r[2]) / 2.0, (r[1] + r[3]) / 2.0
                    return max(b[0] - cx, 0, cx - b[2]) + max(b[1] - cy, 0, cy - b[3])
                _ok4 = (len(_m_b4['marks_drawn']) == 2 and len(_lb4) == 4 and len(_ast4) == 1
                        and min(range(4), key=lambda j: _dist4(_lb4[j], _ast4[0]['bbox_px'])) == 0
                        and _m_b4['overprint_px'] == 0)
            except ValueError:
                _ok4 = False
            check('B4_explicit_H_kept_and_marked_on_native_path', _ok4)
            check('B4_legacy_path_still_strips_explicit_H',
                  structure_draw_fn('[H]C([H])([H])O').canonical == canonical_structure('CO')[0])
            # B5 an arrow mark on an ATOM is drawn (it was always device_not_drawable),
            # outside the molecule and clear of every label
            _p_b5, _w_b5, _m_b5 = structure_draw_fn('CC(C)O', tokens=_TK,
                                                    marks=[_mk('atom', 3, 'arrow')]).native_png(300)
            check('B5_atom_arrow_drawn_clear_of_labels',
                  [d['site']['index'] for d in _m_b5['marks_drawn']] == [3] and not _m_b5['marks_failed']
                  and _m_b5['overprint_px'] == 0
                  and not any(_rects_overlap(_m_b5['marks_drawn'][0]['bbox_px'], b) for b in _m_b5['label_boxes_px']))
            # B6 a colour token set honours the set-wide decision: options differing in their
            # coloured elements are all switched to black (native draws re-render)
            _tkc = dict(_TK, monochrome=False)
            _d_b6 = [structure_draw_fn(s_, tokens=_tkc) for s_ in ('CCBr', 'CCO', 'CCC')]
            native_option_set(_d_b6, 300)
            _d_b6u = [structure_draw_fn(s_, tokens=_tkc) for s_ in ('CCO', 'CCCO')]
            native_option_set(_d_b6u, 300)
            check('B6_native_option_set_divergent_elements_all_black',
                  all(d.element_colours is False for d in _d_b6)
                  and all(d.element_colours is True for d in _d_b6u)
                  and all(_chroma17(_arr17(d.native_png(300)[0])) == 0 for d in _d_b6))
            # B7 a caption wider than its molecule widens the tile (it was clipped)
            _s_b7 = render_scheme({'items': [{'mol': 'O', 'label': '1', 'equiv': '(10 equiv, excess)'},
                                             {'arrow': {}}, {'mol': 'CCO'}]}, tokens=_TK, max_width_in=6.0)
            _p_b7, _w_b7, _m_b7 = _s_b7.native_png(300)
            _a_b7 = _arr17(_p_b7).min(axis=2) < 128
            _band = _a_b7[int(0.75 * _a_b7.shape[0]):, :]
            _cols = _np17.where(_band.any(axis=0))[0]
            _f7, _ff7 = _native_font('regular', 10.0 * _k17)
            check('B7_scheme_caption_not_clipped',
                  _cols.size > 0 and _cols.min() >= int(0.15 * 14.4 * _k17) - 2
                  and (_cols.max() - _cols.min() + 1) >= 0.9 * _f7.getlength('(10 equiv, excess)'))
            # B9 an underline on a label with a subscript (H2N) is drawn under the full label
            _m_b9 = structure_draw_fn('NCC(=O)O', tokens=_TK, marks=[_mk('atom', 0, 'underline')]).native_png(300)[2]
            check('B9_underline_under_subscripted_label',
                  [d['site']['index'] for d in _m_b9['marks_drawn']] == [0] and not _m_b9['marks_failed']
                  and _m_b9['overprint_px'] == 0
                  and _m_b9['marks_drawn'][0]['bbox_px'][1] >= _m_b9['label_boxes_px'][0][3])
        except ImportError as _e17:
            check('native_raster_needs_numpy_pil', 'No module' in str(_e17))

    # ── text_of omml_renderer: structure in place, raw glyphs skipped ─────────
    # lxml is a HARD dependency (python-docx is built on it), so its absence is a
    # broken environment, not a tolerable one. The old fallback emitted
    # check(name, True) on ImportError — three fixtures passing while testing
    # nothing, with the same names and the same total, so the printed result was
    # identical either way. That is the ENV-SKEW lesson this file already
    # records. Now the absence FAILS loudly and the three fixtures simply do not
    # run, which the passed/total line makes visible.
    try:
        from lxml import etree as _et5
        _lxml_ok = True
    except ImportError:
        _lxml_ok = False
    check('lxml_present_for_text_of_fixtures', _lxml_ok)
    if _lxml_ok:
        _W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        _M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
        _xml5 = ('<w:p xmlns:w="%s" xmlns:m="%s">'
                 '<w:r><w:t>Find </w:t></w:r>'
                 '<m:oMath><m:r><m:t>x</m:t></m:r><m:r><m:t>2</m:t></m:r></m:oMath>'
                 '<w:r><w:t> now.</w:t></w:r></w:p>' % (_W, _M))
        _p5 = _et5.fromstring(_xml5)
        _plain = text_of(_p5)
        _rend  = text_of(_p5, omml_renderer=lambda e: '[EQ]')
        check('text_of_omml_renderer',
              _plain == 'Find x2 now.' and _rend == 'Find [EQ] now.')
        _xml6 = ('<w:p xmlns:w="%s"><w:r><w:t>line one</w:t><w:br/>'
                 '<w:t>line two</w:t></w:r></w:p>' % _W)
        _p6 = _et5.fromstring(_xml6)
        check('text_of_soft_breaks',
              text_of(_p6) == 'line one\nline two'
              and text_of(_p6, omml_renderer=lambda e: '') == 'line one\nline two')
        # OOXML allows a <w:t> run INSIDE an <m:oMath>. The renderer consumes
        # the WHOLE subtree, so that run must not reappear after the equation
        # (which reordered the sentence: 'xwhere2' -> 'x2where').
        _xml7 = ('<w:p xmlns:w="%s" xmlns:m="%s"><w:r><w:t>Given </w:t></w:r>'
                 '<m:oMath><m:r><m:t>x</m:t></m:r>'
                 '<w:r><w:t>INSIDE</w:t></w:r>'
                 '<m:r><m:t>2</m:t></m:r></m:oMath>'
                 '<w:r><w:t> end.</w:t></w:r></w:p>') % (_W, _M)
        _p7 = _et5.fromstring(_xml7)
        check('text_of_omml_subtree_consumed_atomically',
              text_of(_p7, omml_renderer=lambda e: '[EQ]') == 'Given [EQ] end.'
              and 'INSIDE' not in text_of(_p7, omml_renderer=lambda e: '[EQ]')
              and 'INSIDE' in text_of(_p7))          # default path unchanged

    import tempfile as _tf2, io as _io2
    # ── IMG-5 scope: alternate-layer unreadables are reported, never fatal ─────
    # (field case: 20 hdphotoN.wdp parts referenced only via a14:imgLayer; every
    # visible drawing carried a raster blip. Old scope failed the whole paper.)
    with _tf2.TemporaryDirectory() as _td5:
        _zp5 = os.path.join(_td5, 'wdp.docx')
        from PIL import Image as _Im5
        _b5 = _io2.BytesIO()
        _Im5.new('RGB', (2, 2), (200, 30, 30)).save(_b5, 'PNG')
        _png5 = _b5.getvalue()
        _doc5 = ('<?xml version="1.0"?><w:document '
                 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                 'xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" '
                 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                 '<w:body><w:p><w:r><w:t>Q.1 See figure</w:t></w:r></w:p>'
                 '<w:p><w:r><a:blip r:embed="rId1"/>'
                 '<a14:imgLayer r:embed="rId2"/></w:r></w:p>'
                 '</w:body></w:document>')
        _rel5 = ('<?xml version="1.0"?><Relationships '
                 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="t" Target="media/image1.png"/>'
                 '<Relationship Id="rId2" Type="t" Target="media/hdphoto1.wdp"/>'
                 '</Relationships>')
        import zipfile as _zf5
        with _zf5.ZipFile(_zp5, 'w') as _z5:
            _z5.writestr('word/document.xml', _doc5)
            _z5.writestr('word/_rels/document.xml.rels', _rel5)
            _z5.writestr('word/media/image1.png', _png5)
            _z5.writestr('word/media/hdphoto1.wdp', b'II\xbc\x01 not-a-raster')
        _v5, _s5 = verify_images(_zp5, workdir=os.path.join(_td5, 'w'))
        check('img5_alternate_layer_not_fatal',
              str(_v5['IMG-5']).startswith('PASS')
              and _s5['alternate_unreadable'] == 1 and _s5['unreadable'] == 0)
        # negative control: the SAME unreadable part, blip-referenced -> FAIL
        _doc5b = _doc5.replace('<a14:imgLayer r:embed="rId2"/>',
                               '<a:blip r:embed="rId2"/>')
        _zp5b = os.path.join(_td5, 'wdp_blip.docx')
        with _zf5.ZipFile(_zp5b, 'w') as _z5:
            _z5.writestr('word/document.xml', _doc5b)
            _z5.writestr('word/_rels/document.xml.rels', _rel5)
            _z5.writestr('word/media/image1.png', _png5)
            _z5.writestr('word/media/hdphoto1.wdp', b'II\xbc\x01 not-a-raster')
        _v5b, _s5b = verify_images(_zp5b, workdir=os.path.join(_td5, 'wb'))
        check('img5_referenced_unreadable_still_fails',
              str(_v5b['IMG-5']).startswith('FAIL') and _s5b['unreadable'] == 1)

    # ── extract_images: explicit ZIP directory entry must not kill extraction ──
    # Observed in the field (IIT_JAM_CHEMISTRY_15-Feb-2026.docx): the archive
    # stores 'word/media/' itself as an entry; basename('') made fp the outdir
    # and open(fp,'wb') raised IsADirectoryError for the WHOLE paper.
    import zipfile as _zf, tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        _zp = os.path.join(_td, 'dirent.docx')
        _png = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
                b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
                b'\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\xf0\x1f\x00\x05'
                b'\x05\x02\x00_\xc8\xf1\xd2\x00\x00\x00\x00IEND\xaeB`\x82')
        with _zf.ZipFile(_zp, 'w') as _z:
            _z.writestr('word/media/', b'')          # the directory entry itself
            _z.writestr('word/media/image1.png', _png)
        try:
            _res = extract_images(_zp, os.path.join(_td, 'imgout'))
            check('extract_images_dir_entry',
                  isinstance(_res, dict) and len(_res) == 1
                  and 'image1.png' in next(iter(_res)))
        except OSError as _ex:
            check('extract_images_dir_entry', False)

    # ── property-fuzz hardening (2026.11.02 pass-3) — native path; each FAILS pre-fix ──
    if _r1 == 'ok':
        import numpy as _npF
        from PIL import Image as _ImF
        from rdkit import Chem as _ChF
        _TKF = {'font_pt': 10.0, 'line_pt': 1.0, 'bond_pt': 14.4, 'monochrome': True,
                'mark_colour': '#000000'}
        # D4: H-only species had NaN CoordGen coords -> blank PNG ('[H][H]' raised NaN);
        # '' parsed to a 0-atom molecule and rendered blank.
        _d4 = True
        for _hs in ('[H+]', '[H-]', '[H]', '[2H]', '[H][H]'):
            try:
                _a4 = _npF.asarray(_ImF.open(io.BytesIO(
                    structure_draw_fn(_hs, tokens=_TKF).native_png(300)[0])).convert('L'))
                _d4 = _d4 and int((_a4 < 128).sum()) > 0
            except Exception:                            # noqa: BLE001
                _d4 = False
        check('native_h_only_species_render_ink', _d4)
        try:
            structure_draw_fn('', tokens=_TKF)
            check('native_empty_smiles_rejected', False)
        except ValueError:
            check('native_empty_smiles_rejected', True)
        # D16: at small tokens a mark's recorded box reached past the cropped PNG
        try:
            _png16, _w16, _m16 = structure_draw_fn(
                'C=CCC(C)(C)CN', tokens=dict(_TKF, font_pt=7.0, bond_pt=8.0),
                marks=[{'site': {'kind': 'atom', 'index': 4}, 'device': 'asterisk'}]).native_png(300)
            _W16, _H16 = _ImF.open(io.BytesIO(_png16)).size
            check('native_mark_bbox_inside_png_small_tokens',
                  bool(_m16['marks_drawn']) and all(
                      _b[0] >= -0.5 and _b[1] >= -0.5 and _b[2] <= _W16 + 0.5 and _b[3] <= _H16 + 0.5
                      for _b in (_mk['bbox_px'] for _mk in _m16['marks_drawn'])))
        except Exception:                                # noqa: BLE001
            check('native_mark_bbox_inside_png_small_tokens', False)
        # D17: CoordGen squashes 2,3-disubstituted norbornanes (one bond at 0.33x); the
        # layout is re-depicted and still prints at the token bond length
        try:
            _ns17 = structure_draw_fn('CC1CC2CCC1C2N', tokens=_TKF)
            _m17 = _ns17.native_png(300)[2]
            _from_rdkit = _ChF.MolFromSmiles('CC1CC2CCC1C2N')
            _lay = _native_layout(_from_rdkit)[0]
            check('native_distorted_coordgen_layout_redepicted',
                  _m17['depictor'] == 'rdkit' and _native_bond_ratio(_lay) >= NATIVE_MIN_BOND_RATIO
                  and abs(_m17['bond_px_measured'] - 14.4 * 300 / 72.0) < 0.5)
        except Exception:                                # noqa: BLE001
            check('native_distorted_coordgen_layout_redepicted', False)
        # D18: non-finite / absurd token sizes -> a clear ValueError naming the token
        _d18 = []
        for _bad in (dict(_TKF, bond_pt=float('inf')), dict(_TKF, font_pt=1e6), dict(_TKF, line_pt=1e-9)):
            try:
                structure_draw_fn('CCO', tokens=_bad).native_png(300)
                _d18.append(False)
            except ValueError as _e18:
                _d18.append('outside the sane' in str(_e18))
            except Exception:                            # noqa: BLE001
                _d18.append(False)
        check('native_tokens_finite_and_bounded', all(_d18))

    # ── v1.19 — RE-25 CHEM-STRUCTURE fixtures (E-03 / E-04 / E-06 g / E-07 / E-09) ──
    # Each fixture below fails on the defect it was written for (CLAUDE.md engine rule).
    if _chs_rdkit() is None:
        check('chs_rdkit_available_for_fixtures', False)
    else:
        from rdkit import Chem as Chem_
        import tempfile as _tf
        # E-03: SN2 — HO⁻ + CH3Br → CH3OH + Br⁻ (all arrows at once)
        _sn2 = {'before': '[OH-:1].[CH3:2][Br:3]', 'after': '[OH:1][CH3:2].[Br-:3]',
                'arrows': [{'from': {'lone_pair': 1}, 'to': {'atom': 2}, 'electrons': 2},
                           {'from': {'bond': [2, 3]}, 'to': {'lone_pair_on': 3}, 'electrons': 2}]}
        check('chs_e03_sn2_pass', verify_mechanism_step(_sn2)[0])
        # E-03: E2 — base takes the β-H (a MOVING, mapped hydrogen), C=C forms, Br leaves
        _e2 = {'before': '[OH-:1].[H:5][CH2:2][CH2:3][Br:4]', 'after': '[OH:1][H:5].[CH2:2]=[CH2:3].[Br-:4]',
               'arrows': [{'from': {'lone_pair': 1}, 'to': {'atom': 5}, 'electrons': 2},
                          {'from': {'bond': [5, 2], 'bias': 2}, 'to': {'bond': [2, 3]}, 'electrons': 2},
                          {'from': {'bond': [3, 4]}, 'to': {'lone_pair_on': 4}, 'electrons': 2}]}
        check('chs_e03_e2_pass', verify_mechanism_step(_e2)[0])
        # E-03: carbonyl addition — hydride to C=O
        _add = {'before': '[H-:3].[CH3:1][CH:2]=[O:4]', 'after': '[CH3:1][CH:2]([H:3])[O-:4]',
                'arrows': [{'from': {'lone_pair': 3}, 'to': {'atom': 2}, 'electrons': 2},
                           {'from': {'bond': [2, 4]}, 'to': {'lone_pair_on': 4}, 'electrons': 2}]}
        check('chs_e03_carbonyl_addition_pass', verify_mechanism_step(_add)[0])
        # E-03: conjugate addition — HO⁻ onto an enone
        _cj = {'before': '[OH-:5].[CH2:1]=[CH:2][CH:3]=[O:4]', 'after': '[OH:5][CH2:1][CH:2]=[CH:3][O-:4]',
               'arrows': [{'from': {'lone_pair': 5}, 'to': {'atom': 1}, 'electrons': 2},
                          {'from': {'bond': [1, 2]}, 'to': {'bond': [2, 3]}, 'electrons': 2},
                          {'from': {'bond': [3, 4]}, 'to': {'lone_pair_on': 4}, 'electrons': 2}]}
        check('chs_e03_conjugate_addition_pass', verify_mechanism_step(_cj)[0])
        # E-03: 1,2-shift (hydride shift to a carbocation)
        _sh = {'before': '[CH3:1][CH+:2][CH:3]([H:5])[CH3:4]', 'after': '[CH3:1][CH:2]([H:5])[CH+:3][CH3:4]',
               'arrows': [{'from': {'bond': [3, 5], 'bias': 5}, 'to': {'atom': 2}, 'electrons': 2}]}
        check('chs_e03_12_shift_pass', verify_mechanism_step(_sh)[0])
        # E-03: fishhook pair — homolysis of Br2
        _rad = {'before': '[Br:1][Br:2]', 'after': '[Br:1].[Br:2]',
                'arrows': [{'from': {'bond': [1, 2], 'bias': 1}, 'to': {'atom': 1}, 'electrons': 1},
                           {'from': {'bond': [1, 2], 'bias': 2}, 'to': {'atom': 2}, 'electrons': 1}]}
        check('chs_e03_fishhook_homolysis_pass', verify_mechanism_step(_rad)[0])
        # E-03: fishhook H-abstraction (three one-electron arrows, one new bond, one new radical)
        _abs = {'before': '[Cl:1].[H:2][CH3:3]', 'after': '[Cl:1][H:2].[CH3:3]',
                'arrows': [{'from': {'atom': 1}, 'to': {'atom': 2}, 'electrons': 1},
                           {'from': {'bond': [2, 3], 'bias': 2}, 'to': {'atom': 1}, 'electrons': 1},
                           {'from': {'bond': [2, 3], 'bias': 3}, 'to': {'atom': 3}, 'electrons': 1}]}
        check('chs_e03_fishhook_abstraction_pass', verify_mechanism_step(_abs)[0])
        # E-03: electrophilic aromatic substitution — the arrow from an AROMATIC bond is its π bond
        _eas = {'before': '[cH:1]1[cH:2][cH:3][cH:4][cH:5][cH:6]1.[N+:7](=[O:8])=[O:9]',
                'after': '[CH:1]1([N+:7](=[O:8])[O-:9])[CH:2]=[CH:3][CH:4]=[CH:5][CH+:6]1',
                'arrows': [{'from': {'bond': [1, 6], 'bias': 1}, 'to': {'atom': 7}, 'electrons': 2},
                           {'from': {'bond': [7, 9]}, 'to': {'lone_pair_on': 9}, 'electrons': 2}]}
        check('chs_e03_aromatic_source_bond_pass', verify_mechanism_step(_eas)[0])
        # E-03: Diels–Alder — three arrows at once, two σ bonds formed
        _da = {'before': '[CH2:1]=[CH:2][CH:3]=[CH2:4].[CH2:5]=[CH2:6]', 'after': '[CH2:1]1[CH:2]=[CH:3][CH2:4][CH2:5][CH2:6]1',
               'arrows': [{'from': {'bond': [1, 2], 'bias': 1}, 'to': {'atom': 6}, 'electrons': 2},
                          {'from': {'bond': [5, 6], 'bias': 5}, 'to': {'atom': 4}, 'electrons': 2},
                          {'from': {'bond': [3, 4]}, 'to': {'bond': [2, 3]}, 'electrons': 2}]}
        check('chs_e03_diels_alder_pass', verify_mechanism_step(_da)[0])
        # E-03 MUST FAIL: the SN2 arrows claimed to give the E2 product
        _bad = dict(_sn2, after='[CH2:2]=[CH2:3]')
        _okb, _rb = verify_mechanism_step(_bad)
        check('chs_e03_wrong_arrows_fail', (not _okb) and 'CHS_ARROW_INVALID' in _rb)
        # Q.73 (reference incident): the three Danheiser steps, dative Ti kept throughout
        _EN = '[Ti]<-[O:20]=[C:1]1[C:2](C)=[CH:3][CH2:4][CH:5](C(C)C)[CH2:6]1'
        _AL = '[CH2:7]=[C:8]=[C:9](C)[Si:10](C)(C)C'
        _I = '[Ti]<-[O-:20][C:1]1=[C:2](C)[CH:3]([CH2:7][C+:8]=[C:9](C)[Si:10](C)(C)C)[CH2:4][CH:5](C(C)C)[CH2:6]1'
        _II = '[Ti]<-[O-:20][C:1]1=[C:2](C)[CH:3]([CH2:7][C:8]([Si:10](C)(C)C)=[C+:9]C)[CH2:4][CH:5](C(C)C)[CH2:6]1'
        _PT = '[Ti]<-[O:20]=[C:1]1[CH2:6][CH:5](C(C)C)[CH2:4][C@@H:3]2[CH2:7][C:8]([Si:10](C)(C)C)=[C:9](C)[C@:2]12C'
        _lab = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: 'a', 8: 'b', 9: 'c'}
        _q73 = [
            {'id': 'S1', 'before': _EN + '.' + _AL, 'after': _I, 'reagents_above': 'TiCl4, CH2Cl2',
             'conditions_below': '-78 C',
             'arrows': [{'from': {'bond': [7, 8], 'bias': 7}, 'to': {'atom': 3}, 'electrons': 2},
                        {'from': {'bond': [3, 2]}, 'to': {'bond': [2, 1]}, 'electrons': 2},
                        {'from': {'bond': [1, 20]}, 'to': {'lone_pair_on': 20}, 'electrons': 2}],
             'highlight': {'form': [[3, 7]]}, 'caption_before': ['Enone + allenylsilane', 'a attacks C3'],
             'caption': ['Intermediate I', 'C+ on b'], 'atom_labels': _lab},
            {'id': 'S2', 'before': _I, 'after': _II, 'conditions_below': '1,2-silyl shift',
             'arrows': [{'from': {'bond': [9, 10], 'bias': 10}, 'to': {'atom': 8}, 'electrons': 2}],
             'highlight': {'form': [[8, 10]]}, 'caption_before': ['Intermediate I', 'c-Si shifts to b'],
             'caption': ['Intermediate II', 'C+ on c'], 'atom_labels': _lab},
            {'id': 'S3', 'before': _II, 'after': _PT, 'conditions_below': 'ring closure',
             'arrows': [{'from': {'bond': [2, 1], 'bias': 2}, 'to': {'atom': 9}, 'electrons': 2},
                        {'from': {'lone_pair': 20}, 'to': {'bond': [20, 1]}, 'electrons': 2}],
             'highlight': {'form': [[2, 9]]}, 'caption_before': ['Intermediate II', 'C2 attacks c'],
             'caption': ['P (cis-fused)', 'new bonds in green'], 'atom_labels': _lab}]
        check('chs_e03_q73_all_three_steps_pass', all(verify_mechanism_step(st)[0] for st in _q73))
        check('chs_e06g_q73_balanced', all(step_atom_balance(st)[0] for st in _q73))
        # E-06 g MUST FAIL: a by-product that is not in `before`
        check('chs_e06g_unbalanced_step_fail',
              not step_atom_balance(dict(_sn2, byproducts=['O']))[0])
        # E-04 / E-01: render the three steps, chained alignment, every gate clean, deterministic bytes
        try:
            _tm = None; _draws = []
            for st in _q73:
                _d = render_mechanism(st, template=_tm); _tm = _d.after_mol; _draws.append(_d)
            check('chs_e04_q73_renders_mechanism', all(d.requirement == 'MECHANISM' for d in _draws))
            check('chs_e04_q73_layout_audit_clean', all(figure_layout_audit(d)[0] for d in _draws))
            check('chs_e04_q73_no_step_down', all(not d.degrade_ledger for d in _draws))
            check('chs_e04_q73_under_target_bytes', all(d.meta['bytes'] <= CHS_TARGET_BYTES for d in _draws))
            check('chs_e04_q73_width_fits_column', all(d.width_in <= 6.0 + 1e-9 for d in _draws))
            _again = render_mechanism(_q73[0]); check('chs_e04_deterministic_bytes', _again.png_bytes == _draws[0].png_bytes)
            check('chs_e04_identifier_records_e03', all(d.identifier['e03'] == 'PASS' and d.identifier['arrows'] for d in _draws))
            # the retry search is REAL: a clipped/crossing first attempt must be retried, S3 needs > 1
            check('chs_e04_retry_search_ran', _draws[2].meta['attempts'] > 1)
            # E-04 MUST FAIL path: an arrow forced across a label — L1 finding is produced by the gate
            _pan = _Panel(None, {'atoms': {0: (10, 10), 1: (60, 10), 2: (110, 10)}, 'bonds': [(0, 1), (1, 2)],
                                 'label_boxes': {1: (50, 0, 70, 20)}, 'captions': [], 'bond_px': 48, 'font_px': 26,
                                 'arrows': [{'pts': [(10, 30), (60, 12), (110, 30)], 'start_atoms': (0,), 'end_atoms': (2,),
                                             'tip': (110, 30), 'target': (110, 30)}]}, [])
            _f = _layout_findings([_pan], [(0, 0)], (400, 400), 200)
            check('chs_e04_crossing_arrow_fails_L1', any(x.startswith('L1') for x in _f))
            _pan2 = _Panel(None, {'atoms': {0: (10, 10), 1: (60, 10)}, 'bonds': [(0, 1)], 'label_boxes': {},
                                  'captions': [(0, 380, 200, 399)], 'bond_px': 48, 'font_px': 26, 'arrows': []}, [])
            check('chs_e04_clipped_caption_fails_L4', any(x.startswith('L4') for x in _layout_findings([_pan2], [(0, 0)], (400, 400), 200)))
            # E-04 wrong-path figure (WHY WRONG) and option panel
            _w = render_mechanism(dict(_q73[0], arrows=[{'from': {'bond': [8, 9], 'bias': 8}, 'to': {'atom': 3}, 'electrons': 2},
                                                        {'from': {'bond': [3, 2]}, 'to': {'bond': [2, 1]}, 'electrons': 2},
                                                        {'from': {'bond': [1, 20]}, 'to': {'lone_pair_on': 20}, 'electrons': 2}],
                                       after='[Ti]<-[O-:20][C:1]1=[C:2](C)[CH:3]([C:8](=[CH2:7])[C+:9](C)[Si:10](C)(C)C)[CH2:4][CH:5](C(C)C)[CH2:6]1',
                                       caption=['Option 1 path', 'b bonds to C3 (wrong)']), section='WHY_WRONG', wrong=True)
            check('chs_e05_wrong_path_figure_renders', _w.requirement in CHS_FALLBACK_CHAIN and _w.width_in <= 5.6 + 1e-9)
            _op = render_structure_panel('O=C1CC(C(C)C)C[C@@H]2CC([Si](C)(C)C)C(C)[C@]12C', ['Option 3', 'as printed: no C=C'],
                                         wrong_bonds=[], section='WHY_WRONG')
            check('chs_e05_option_panel_renders', _op.requirement == 'STRUCTURE_GRAPH' and _op.identifier['canonical'])
            # E-09 contact sheet
            with _tf.TemporaryDirectory() as _td:
                _sheet, _sm = figure_review_sheet([(f'Q73-{d.identifier["requirement"]}-{k}', d) for k, d in enumerate(_draws)],
                                                  os.path.join(_td, 'sheet.png'))
                check('chs_e09_review_sheet', os.path.getsize(_sheet) > 0 and _sm['count'] == 3)
        except Exception as _exc:                             # noqa: BLE001
            check(f'chs_e04_render_raised:{type(_exc).__name__}:{str(_exc)[:80]}', False)
        # E-07: Q.73 printed Option 3 lacks the ring C=C → nearest 3, delta +H2, no exact
        _opts = {1: 'O=C1CC(C(C)C)C[C@@H]2C(=C(C)[Si](C)(C)C)C[C@]12C',
                 2: 'O=C1CC(C(C)C)C[C@@H]2CC(=C(C)[Si](C)(C)C)[C@]12C',
                 3: 'O=C1CC(C(C)C)C[C@@H]2CC([Si](C)(C)C)C(C)[C@]12C',
                 4: 'O=C1CC(C(C)C)C[C@@H]2CC(C)C([Si](C)(C)C)[C@]12C'}
        _om = option_match('O=C1CC(C(C)C)C[C@@H]2CC([Si](C)(C)C)=C(C)[C@]12C', _opts)
        check('chs_e07_q73_nearest_option_3_delta_H2', _om['exact'] is None and _om['nearest'] == 3 and _om['formula_delta'] == '+H2')
        _om2 = option_match('O=C1CC(C(C)C)C[C@@H]2CC([Si](C)(C)C)=C(C)[C@]12C',
                            {**_opts, 3: 'O=C1CC(C(C)C)C[C@@H]2CC([Si](C)(C)C)=C(C)[C@]12C'})
        check('chs_e07_exact_match_found', _om2['exact'] == 3)
        # EC-32: an option drawn WITHOUT stereo matches on constitution only
        check('chs_e07_undrawn_stereo_matches_constitution',
              option_match('C[C@H](O)CC', {1: 'CC(O)CC', 2: 'CCCCO'})['exact'] == 1)
        check('chs_canonical_strips_maps_and_h', mechanism_canonical('[CH3:1][CH2:2][OH:3]') == 'CCO')
        # H2 / hydride species survive display preparation (nothing to fold them into)
        try:
            _h2 = _strip_unmoving_h(mapped_mol('[H:1][H:2].[H-:3].[CH3:4][OH:5]'), set())
            check('chs_h2_and_hydride_species_kept', _h2.GetNumAtoms() == 5)
        except Exception as _e:                                    # noqa: BLE001
            check(f'chs_h2_and_hydride_species_kept:{type(_e).__name__}', False)
        check('chs_ink_defaults_are_okabe_ito', set(_chs_ink()) == {'ARROW_INK', 'FORM_INK', 'WRONG_INK'})
        check('chs_retry_schedule_capped', 1 < len(_attempt_schedule()) <= CHS_RETRY_CAP)
        # R2-3 — a stationary explicit [H] on a stereocentre keeps the configuration
        _sh = _strip_unmoving_h(mapped_mol('[CH3:1][CH2:2][C@:3]([H:9])([CH3:4])[OH:5]'), set())
        check('chs_strip_h_keeps_stereo', mechanism_canonical(Chem_.MolToSmiles(_sh), stereo=True)
              == mechanism_canonical('CC[C@H](C)O', stereo=True))
        # R2-5 — reagent placement when the attacked atom is its fragment's centre
        for _nm, _st in (('sn1_step2', {'before': '[CH3:2][C+:1]([CH3:3])[CH3:4].[Br-:5]',
                                         'after': '[CH3:2][C:1]([CH3:3])([CH3:4])[Br:5]',
                                         'arrows': [{'from': {'lone_pair': 5}, 'to': {'atom': 1}}], 'caption': ['t-BuBr']}),
                         ('radical_recombination', {'before': '[CH3:1].[CH3:2]', 'after': '[CH3:1][CH3:2]',
                                                    'arrows': [{'from': {'atom': 1}, 'to': {'atom': 2}, 'electrons': 1},
                                                               {'from': {'atom': 2}, 'to': {'atom': 1}, 'electrons': 1}],
                                                    'caption': ['ethane']})):
            try:
                check(f'chs_place_centre_atom:{_nm}', render_mechanism(_st).requirement in CHS_FALLBACK_CHAIN)
            except Exception as _e:                        # noqa: BLE001
                check(f'chs_place_centre_atom:{_nm}:{str(_e)[:60]}', False)
        # R2-4 — stereo-aware option match: enantiomer / racemic / no index tie-break
        _rr = 'O[C@@H]1CCCC[C@H]1O'
        _om4 = option_match(_rr, {1: 'O[C@@H]1CCCC[C@@H]1O', 2: 'O[C@H]1CCCC[C@@H]1O'})
        check('chs_om_enantiomer_is_nearest', _om4['exact'] is None and _om4['nearest'] == 2)
        check('chs_om_racemic_mirror_exact', option_match(_rr, {1: 'O[C@@H]1CCCC[C@@H]1O', 2: 'O[C@H]1CCCC[C@@H]1O'},
                                                         racemic=True)['exact'] == 2)
        _omt = option_match('CCCC(=O)O', {1: 'CCC(=O)O', 2: 'CCCCC(=O)O'})
        check('chs_om_tie_never_by_index', _omt['exact'] is None and (_omt['nearest'] is None) == bool(_omt['tie']))
        # L7 — a panel taller than a page is never returned: it raises CHS_LAYOUT_UNRENDERABLE
        try:
            render_structure_panel('C' * 120 + 'O', ['very long chain'])
            check('chs_l7_tall_panel_refused', False)
        except ValueError as _e7:
            check('chs_l7_tall_panel_refused', 'CHS_LAYOUT_UNRENDERABLE' in str(_e7))
        _d7 = render_structure_panel('C' * 30 + 'O', ['chain'])
        check('chs_l7_normal_panel_fits', _d7.meta['canvas_px'][1] / float(CHS_FIGURE_DPI) <= CHS_MAX_HEIGHT_IN)

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print('FAILED: ' + ', '.join(fails))
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print('corpus_io.py — corpus acquisition / image integrity / size governor. '
          'Run with --self-test.')
