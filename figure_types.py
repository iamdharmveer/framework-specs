"""
figure_types.py v1.3 — FIGURE-TYPE REGISTRY: the one table that binds a Step-5
object_type (profile vocabulary) to a Step-7 render class, a semantic kind and a
renderer. GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY, LAW F1.

CHANGELOG
    v1.3 (2026-11-05) — GAP-2026-11-05-DIFFICULTY-FIDELITY (DL-22, guard G4): ASK
         FORMAT is an axis of its own — ASK_FORMATS + normalise_ask_format(stem,
         options), checked BEFORE the ask type and stored beside it (`ask_format`), so
         "Match the reagents in List-I ..." is reagent_identification AND match. SHAPE
         RULES: shapes_for(family, 's1') is ASK_TYPES unchanged (every reader byte-
         identical; A-SHAPEMIX reads s1 targets only); shapes_for(family, 's2') =
         ASK_TYPES_S2 adds statement / match / sequence / assertion_reason to EVERY
         family — targets written from it carry shape_rule 's2' and are gated by the
         WARN-only A-AXIS2.
    v1.2 (2026-11-03) — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (§4.7 no exam-
         specific code): per-FAMILY quality rows QUALITY_ROWS[family] = {identity_fn,
         complexity_vector, mechanism_vocabulary} naming blueprint_core functions /
         vocabularies (chemistry rows point at structure_identity / content_vector /
         MECHANISM_VOCABULARY['chemistry']; data rows at data_figure_identity; glyph
         and hand-drawn rows at None = "no identity_fn, the reviewer decides"), and the
         per-family ask-type vocabulary ASK_TYPES[family] (R5.1): the chemistry family
         gains multiple_products, outcome_ratio, two_part, quantitative_calculation;
         physics/graph and text families get their own lists. FIGURAL_ASK_TYPES is kept
         as the chemistry list's alias so every v1.1 reader is unchanged.
         normalise_ask_type() learns the four new chemistry shapes.
    v1.1 (2026-11-02) — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY (F8, §0.2): closed
         figural ask-type vocabulary FIGURAL_ASK_TYPES + normalise_ask_type(),
         REPRESENTATION_TAGS, SCHEME_GRAMMAR_TAGS, and the scope classes
         CHEM_R_OBJECT_TYPES / CHEM_H_OBJECT_TYPES DERIVED from FIGURE_TYPES.
    v1.0 (2026-11-01) — the registry (GAP-2026-11-01).

WHY THIS FILE EXISTS
    Three vocabularies described a figure and none was bound to the others:
      * Step 5 (analyse_engine) emits a FREE-TEXT object_type per PYQ figure
        (76 distinct strings on one exam) and writes it into section_rules.
      * Step 7 (figural_core) draws under one of five S10-6A RENDER CLASSES.
      * Step 7 (paper_pipeline.SEMANTIC_KINDS) records WHAT a figure depicts.
    No table said which type is drawn by which renderer under which kind, so a
    dominant type with no renderer (reaction_scheme, whose REACTION kind was
    mandated to a single-molecule renderer that rejects reaction SMILES) could
    only be mislabelled (a STRUCTURE recorded as reaction_scheme — 287 times on
    the reference registry) or omitted. Every such paper audited green.

    This registry is the single source of truth. Step 5 normalises its emitted
    strings onto it (analyse_engine), Step 6 runs the KIND-COVERAGE pre-flight
    against it (blueprint_core.kind_coverage_preflight), Step 7 dispatches a
    figure by its registry row (MockTestCreate S7-NEW-B / S7-NEW-B2) and the
    auditor's A-FIGTYPE-KIND gate checks that the row that rendered a figure is
    the row its record names (audit_canonical, blueprint_core.
    check_figural_conformance with records).

EXAM-AGNOSTIC BY CONSTRUCTION
    * The table is a VOCABULARY, not an exam: a chemistry type, a biology type
      and a reasoning-glyph type sit side by side. Adding a type is a REPO change
      with a self-test fixture, never a per-exam edit.
    * A string the table does not know is NEVER rejected and NEVER silently
      dropped: lookup() returns status 'unregistered', the caller treats it as a
      GENERIC hand-drawn schematic (the EC-V18 posture every pre-registry exam
      already runs under) and every reader DISCLOSES it (Step-5 advisory,
      Step-6 advisory, A-FIGTYPE-KIND WARN) so the vocabulary grows by evidence.
      ~200 exams carry section_rules written before this file existed; none of
      them may be halted by a vocabulary gap. Only an EXPLICITLY 'unsupported'
      type (a photograph, a micrograph — something line art cannot honestly
      stand in for) can stop a blueprint, and only when it is DOMINANT.
    * Renderer availability is a SESSION fact, not a table fact. preflight()
      imports every renderer the 'supported' rows name and reports which are
      usable now (rdkit may be absent); Step 7 S3 refuses to start a paper whose
      plan needs a renderer this session cannot load (a Type-2, input-integrity
      stop with one operator action: the pip line), instead of discovering it as
      a traceback at Q.14.

PURITY
    stdlib only at import time. Renderer modules are imported ONLY inside
    preflight(), so this file is importable on every route (PYQ steps load it
    without matplotlib or rdkit).
"""
import importlib
import re

__version__ = '1.3'

# ── S10-6A render classes (MockTestCreate) — parity with figural_core.FIGURE_CLASSES is
#    verified by mock_sync_audit MS-23; this tuple is mirrored, never imported, so the
#    registry stays importable on routes that do not load figural_core.
RENDER_CLASSES = ('data_series', 'data_single', 'schematic', 'reasoning_glyph',
                  'option_canvas')
DATA = ('data_series', 'data_single')          # class decided by measured series count
SCHEMATIC = ('schematic',)
GLYPH = ('reasoning_glyph',)

# ── paper_pipeline.SEMANTIC_KINDS — mirrored for the same reason (MS-23 parity).
SEMANTIC_KINDS = ('STRUCTURE', 'REACTION', 'NEWMAN', 'FISCHER', 'MO_DIAGRAM',
                  'ORBITAL_BOXES', 'COORDINATION', 'PLOT', 'TABLE', 'GEOMETRY', 'GENERIC')

# ── renderer symbols. 'hand_drawn+descriptor' is the S7-NEW-B2 path for kinds that are
#    drawn with matplotlib artists by the session and described by a descriptor; it needs
#    matplotlib only. 'glyph_path' is S10-7 render_figural_image (reasoning glyphs).
R_STRUCT = 'corpus_io.structure_draw_fn'
R_SCHEME = 'corpus_io.render_scheme'
R_DATA = 'figural_core.render_figure'
R_HAND = 'hand_drawn+descriptor'
# v1.3 (GAP-2026-11-10 G-12, LAW-ORG-8): chair / Newman / sawhorse / Fischer / Haworth QUESTION figures are drawn
# by the PROVEN projection renderers (corpus_io.render_projection -> render_chair ... render_haworth, each refusing a
# drawing whose 3-D rebuild does not reproduce every CIP label) — never hand-drawn. identity kind STRUCTURE_CONFORMER:
# the molecule's stereo identity PLUS its conformer descriptor (axial / equatorial per substituent, dihedral class),
# so "which conformer is most stable" options stay distinct while a mis-drawn stereoisomer is caught.
R_PROJ = 'corpus_io.render_projection'
R_GLYPH = 'glyph_path'
R_TABLE = 'add_match_table'                    # a Word table, not a raster (DI / MATCH)

STATUSES = ('supported', 'unsupported')

# Dependencies a renderer symbol needs beyond matplotlib (checked by preflight()).
RENDERER_DEPS = {
    R_STRUCT: ('rdkit',),
    R_SCHEME: ('rdkit',),
    R_DATA: (),
    R_HAND: (),
    R_PROJ: ('rdkit',),
    R_GLYPH: (),
    R_TABLE: (),
}


def _row(classes, kinds, renderer, status='supported', family=None, note=''):
    kinds = (kinds,) if isinstance(kinds, str) else tuple(kinds)
    classes = (classes,) if isinstance(classes, str) else tuple(classes)
    return {'render_classes': classes, 'semantic_kinds': kinds, 'renderer': renderer,
            'status': status, 'family': family or '', 'note': note}


# ═══════════════════════════════════════════════════════════════════════════════
# THE REGISTRY. canonical_type -> row. The FIRST semantic kind is the one a figure of
# this type registers by default; the others are the kinds the TYPE↔KIND gate also
# accepts (a coordination complex may be rdkit-drawn as a STRUCTURE).
# Families: chem_structure · chem_scheme · chem_spectrum · chem_diagram · data ·
# geometry · reasoning · table · apparatus · biology · physics · generic · raster
# ═══════════════════════════════════════════════════════════════════════════════
FIGURE_TYPES = {
    # ── chemical structures (rdkit; S7-NEW-B2 mandates structure_draw_fn) ─────────
    'chemical_structure':             _row(SCHEMATIC, ('STRUCTURE', 'COORDINATION'), R_STRUCT, family='chem_structure'),
    'organometallic_structure':       _row(SCHEMATIC, ('STRUCTURE', 'COORDINATION'), R_STRUCT, family='chem_structure'),
    'coordination_complex_structure': _row(SCHEMATIC, ('COORDINATION', 'STRUCTURE'), R_STRUCT, family='chem_structure'),
    'metal_cluster_structure':        _row(SCHEMATIC, ('COORDINATION', 'STRUCTURE', 'GENERIC'), R_STRUCT, family='chem_structure'),
    'supramolecular_structure':       _row(SCHEMATIC, ('STRUCTURE', 'GENERIC'), R_STRUCT, family='chem_structure'),
    'bioinorganic_active_site':       _row(SCHEMATIC, ('COORDINATION', 'STRUCTURE', 'GENERIC'), R_STRUCT, family='chem_structure'),
    'molecular_model':                _row(SCHEMATIC, ('STRUCTURE', 'GENERIC'), R_STRUCT, family='chem_structure'),
    'newman_projection':              _row(SCHEMATIC, 'NEWMAN', R_PROJ, family='chem_structure'),
    'fischer_projection':             _row(SCHEMATIC, 'FISCHER', R_PROJ, family='chem_structure'),
    'crystal_lattice_diagram':        _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_structure'),
    # ── reaction schemes (compositor over rdkit tiles — corpus_io.render_scheme) ──
    'reaction_scheme':                _row(SCHEMATIC, 'REACTION', R_SCHEME, family='chem_scheme'),
    'reaction_mechanism_scheme':      _row(SCHEMATIC, 'REACTION', R_SCHEME, family='chem_scheme'),
    'reaction_cycle_scheme':          _row(SCHEMATIC, ('REACTION', 'GENERIC'), R_SCHEME, family='chem_scheme'),
    'synthesis_flow_diagram':         _row(SCHEMATIC, ('REACTION', 'GENERIC'), R_SCHEME, family='chem_scheme'),
    'qualitative_analysis_scheme':    _row(SCHEMATIC, ('GENERIC', 'REACTION'), R_HAND, family='chem_scheme'),
    'isolobal_relationship_scheme':   _row(SCHEMATIC, ('GENERIC', 'STRUCTURE'), R_HAND, family='chem_scheme'),
    # ── chemistry diagrams drawn with artists + descriptor ─────────────────────────
    'molecular_orbital_diagram':      _row(SCHEMATIC, 'MO_DIAGRAM', R_HAND, family='chem_diagram'),
    'orbital_diagram':                _row(SCHEMATIC, ('ORBITAL_BOXES', 'MO_DIAGRAM'), R_HAND, family='chem_diagram'),
    'energy_level_diagram':           _row(SCHEMATIC, ('MO_DIAGRAM', 'GENERIC'), R_HAND, family='chem_diagram'),
    'jablonski_diagram':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    'thermodynamic_cycle':            _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    'molecular_symbol_diagram':       _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    'electrostatic_potential_map':    _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    'direction_diagram':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    # ── spectra and curves (data classes; kind PLOT) ───────────────────────────────
    'nmr_spectrum':                   _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'nmr_spectrum_set':               _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'ir_spectrum':                    _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'ir_spectrum_with_table':         _row(DATA, ('PLOT', 'TABLE'), R_DATA, family='chem_spectrum'),
    'mass_spectrum':                  _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'uv_vis_spectrum':                _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'spectrum':                       _row(DATA, 'PLOT', R_DATA, family='chem_spectrum',
                                           note='generic spectrum (keyword family); name the technique when known'),
    'reaction_coordinate_diagram':    _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'chromatogram':                   _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'voltammogram':                   _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'diffraction_pattern':            _row(DATA, 'PLOT', R_DATA, family='chem_spectrum',
                                           note='XRD / powder pattern as intensity vs 2θ — a PLOT, never a raster'),
    'thermal_analysis_curve':         _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'electrochemical_cell_diagram':   _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'tlc_plate':                      _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'chair_conformation':             _row(SCHEMATIC, ('GENERIC', 'STRUCTURE'), R_PROJ, family='chem_structure'),
    'haworth_projection':             _row(SCHEMATIC, ('GENERIC', 'FISCHER', 'STRUCTURE'), R_PROJ, family='chem_structure'),
    'sawhorse_projection':            _row(SCHEMATIC, ('GENERIC', 'NEWMAN', 'STRUCTURE'), R_PROJ, family='chem_structure'),
    'potential_energy_surface':       _row(SCHEMATIC + DATA, ('GENERIC', 'PLOT'), R_HAND, family='chem_diagram'),
    'latimer_diagram':                _row(SCHEMATIC, 'GENERIC', R_HAND, family='chem_diagram'),
    'frost_diagram':                  _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'pourbaix_diagram':               _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'ellingham_diagram':              _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'tanabe_sugano_diagram':          _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'walsh_diagram':                  _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC', 'MO_DIAGRAM'), R_HAND, family='chem_diagram'),
    'orgel_diagram':                  _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'epr_spectrum':                   _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'mossbauer_spectrum':             _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'rotational_spectrum':            _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'dsc_thermogram':                 _row(DATA, 'PLOT', R_DATA, family='chem_spectrum'),
    'titration_curve':                _row(DATA, 'PLOT', R_DATA, family='data'),
    'potential_energy_curve':         _row(DATA, 'PLOT', R_DATA, family='data'),
    'potential_energy_diagram':       _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'reaction_energy_profile':        _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'wavefunction_plot':              _row(DATA, 'PLOT', R_DATA, family='data'),
    'adsorption_isotherm':            _row(DATA, 'PLOT', R_DATA, family='data'),
    'phase_diagram':                  _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'pv_indicator_diagram':           _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'vp_cycle_diagram':               _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'vt_cycle_diagram':               _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='chem_diagram'),
    'vapour_pressure_composition_plot': _row(DATA, 'PLOT', R_DATA, family='data'),
    'decay_series_plot':              _row(DATA, 'PLOT', R_DATA, family='data'),
    'stress_strain_curve':            _row(DATA, 'PLOT', R_DATA, family='data'),
    'distribution_curve':             _row(DATA, 'PLOT', R_DATA, family='data'),
    # ── generic data charts ────────────────────────────────────────────────────────
    'line_graph':                     _row(DATA, 'PLOT', R_DATA, family='data'),
    'bar_chart':                      _row(DATA, 'PLOT', R_DATA, family='data'),
    'stacked_bar_chart':              _row(DATA, 'PLOT', R_DATA, family='data'),
    'bar_chart_3d':                   _row(DATA, 'PLOT', R_DATA, family='data',
                                           note='rendered as a flat bar chart (Q7 line-art contract)'),
    'scatter_plot':                   _row(DATA, 'PLOT', R_DATA, family='data'),
    'step_graph':                     _row(DATA, 'PLOT', R_DATA, family='data'),
    'log_scale_plot':                 _row(DATA, 'PLOT', R_DATA, family='data'),
    'bubble_line_chart':              _row(DATA, 'PLOT', R_DATA, family='data'),
    'pie_chart':                      _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='data'),
    'pie_chart_with_bar_chart':       _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='data'),
    'radar_chart':                    _row(SCHEMATIC + DATA, ('PLOT', 'GENERIC'), R_HAND, family='data'),
    'contour_plot':                   _row(DATA, 'PLOT', R_DATA, family='data'),
    'contour_map':                    _row(DATA + SCHEMATIC, ('PLOT', 'GENERIC'), R_DATA, family='data'),
    'colour_map_plot':                _row(DATA, 'PLOT', R_DATA, family='data'),
    'histogram':                      _row(DATA, 'PLOT', R_DATA, family='data'),
    'box_plot':                       _row(DATA, 'PLOT', R_DATA, family='data'),
    'survival_curve':                 _row(DATA, 'PLOT', R_DATA, family='data'),
    'growth_curve':                   _row(DATA, 'PLOT', R_DATA, family='data'),
    'dose_response_curve':            _row(DATA, 'PLOT', R_DATA, family='data'),
    'time_series_plot':               _row(DATA, 'PLOT', R_DATA, family='data'),
    'frequency_polygon':              _row(DATA, 'PLOT', R_DATA, family='data'),
    'ogive':                          _row(DATA, 'PLOT', R_DATA, family='data'),
    'velocity_time_graph':            _row(DATA, 'PLOT', R_DATA, family='data'),
    'displacement_time_graph':        _row(DATA, 'PLOT', R_DATA, family='data'),
    'iv_characteristic_curve':        _row(DATA, 'PLOT', R_DATA, family='data'),
    'waveform_plot':                  _row(DATA, 'PLOT', R_DATA, family='data'),
    # ── tables ─────────────────────────────────────────────────────────────────────
    'data_table':                     _row(SCHEMATIC, 'TABLE', R_TABLE, family='table'),
    'matching_table':                 _row(SCHEMATIC, 'TABLE', R_TABLE, family='table'),
    'organometallic_formula_table':   _row(SCHEMATIC, 'TABLE', R_TABLE, family='table'),
    'truth_table':                    _row(SCHEMATIC, 'TABLE', R_TABLE, family='table'),
    # ── geometry (drawn as real geometry — S10-7 Q6) ───────────────────────────────
    'geometric_figure':               _row(SCHEMATIC + GLYPH, 'GEOMETRY', R_HAND, family='geometry'),
    'geometric_solid':                _row(SCHEMATIC + GLYPH, 'GEOMETRY', R_HAND, family='geometry'),
    'cube_net':                       _row(GLYPH + SCHEMATIC, 'GEOMETRY', R_GLYPH, family='geometry'),
    'coordinate_geometry_plot':       _row(DATA + SCHEMATIC, ('GEOMETRY', 'PLOT'), R_DATA, family='geometry'),
    'triangle_diagram':               _row(SCHEMATIC + GLYPH, 'GEOMETRY', R_HAND, family='geometry'),
    'circle_diagram':                 _row(SCHEMATIC + GLYPH, 'GEOMETRY', R_HAND, family='geometry'),
    'angle_diagram':                  _row(SCHEMATIC + GLYPH, 'GEOMETRY', R_HAND, family='geometry'),
    'mirror_image_figure':            _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'water_image_figure':             _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'paper_folding_figure':           _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'embedded_figure':                _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    # ── reasoning glyphs (monochrome glyph path — S10-6A reasoning_glyph) ──────────
    'figure_series':                  _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'figure_analogy':                 _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'figure_classification':          _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'figure_matrix':                  _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'figure_completion':              _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'odd_one_out_figure':             _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'pattern_tiles':                  _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'dot_grid_puzzle':                _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'grid_puzzle':                    _row(GLYPH, ('GEOMETRY', 'GENERIC'), R_GLYPH, family='reasoning'),
    'number_grid_puzzle':             _row(GLYPH + SCHEMATIC, ('GEOMETRY', 'GENERIC'), R_GLYPH, family='reasoning'),
    'number_figure_puzzle':           _row(GLYPH + SCHEMATIC, ('GEOMETRY', 'GENERIC'), R_GLYPH, family='reasoning'),
    'dice_figure':                    _row(GLYPH, 'GEOMETRY', R_GLYPH, family='reasoning'),
    'clock_figure':                   _row(GLYPH + SCHEMATIC, ('GEOMETRY', 'GENERIC'), R_GLYPH, family='reasoning'),
    'venn_diagram':                   _row(SCHEMATIC + GLYPH, ('GEOMETRY', 'GENERIC'), R_HAND, family='reasoning'),
    'direction_sense_diagram':        _row(SCHEMATIC + GLYPH, ('GEOMETRY', 'GENERIC'), R_HAND, family='reasoning'),
    'seating_arrangement_diagram':    _row(SCHEMATIC, 'GENERIC', R_HAND, family='reasoning'),
    'blood_relation_tree':            _row(SCHEMATIC, 'GENERIC', R_HAND, family='reasoning'),
    # ── apparatus, circuits, networks, flow ────────────────────────────────────────
    'apparatus_diagram':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'circuit_diagram':                _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'logic_gate_diagram':             _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'block_diagram':                  _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'network_diagram':                _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'flowchart':                      _row(SCHEMATIC, 'GENERIC', R_HAND, family='apparatus'),
    'free_body_diagram':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'ray_diagram':                    _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'vector_diagram':                 _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'field_line_diagram':             _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'wave_diagram':                   _row(SCHEMATIC + DATA, ('GENERIC', 'PLOT'), R_HAND, family='physics'),
    'feynman_diagram':                _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'crystal_structure_diagram':      _row(SCHEMATIC, 'GENERIC', R_HAND, family='physics'),
    'band_structure_diagram':         _row(SCHEMATIC + DATA, ('GENERIC', 'PLOT'), R_HAND, family='physics'),
    # ── biology / medicine line diagrams ───────────────────────────────────────────
    'anatomical_diagram':             _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'cell_diagram':                   _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'pedigree_chart':                 _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'punnett_square':                 _row(SCHEMATIC, ('TABLE', 'GENERIC'), R_HAND, family='biology'),
    'phylogenetic_tree':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'metabolic_pathway_diagram':      _row(SCHEMATIC, ('GENERIC', 'REACTION'), R_HAND, family='biology'),
    'life_cycle_diagram':             _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'food_web_diagram':               _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'gel_electrophoresis_diagram':    _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology',
                                           note='schematic lanes/bands; a gel PHOTOGRAPH is gel_photograph (unsupported)'),
    'dna_sequence_diagram':           _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'plasmid_map':                    _row(SCHEMATIC, 'GENERIC', R_HAND, family='biology'),
    'ecg_trace':                      _row(DATA, 'PLOT', R_DATA, family='biology'),
    # ── maps and misc line art ─────────────────────────────────────────────────────
    'outline_map':                    _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    'timeline_diagram':               _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    'tree_diagram':                   _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    'concept_map':                    _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    'schematic_diagram':              _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    'generic_diagram':                _row(SCHEMATIC, 'GENERIC', R_HAND, family='generic'),
    # ── RASTER-ONLY families: line art cannot honestly stand in for these. A blueprint
    #    whose DOMINANT type is one of them HARD STOPs at Step 6 unless exam_config
    #    figure_fallback_policy == 'text_disclosed' (LAW F1.4, edge cases E2/E3).
    'photograph':                     _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'micrograph':                     _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'electron_micrograph':            _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'histology_slide':                _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'radiograph':                     _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'satellite_image':                _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'gel_photograph':                 _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'screenshot':                     _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'scanned_handwriting':            _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
    'artwork_reproduction':           _row(SCHEMATIC, 'GENERIC', None, status='unsupported', family='raster'),
}

# ═══════════════════════════════════════════════════════════════════════════════
# v1.1 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY
# ═══════════════════════════════════════════════════════════════════════════════
# §0.2 scope classes, DERIVED from the table above (never a second hand-kept list):
#   [chem-R] RDKit-rendered chemistry — renderer corpus_io.structure_draw_fn or
#            corpus_io.render_scheme;
#   [chem-H] hand-drawn chemistry drawings — family chem_structure / chem_scheme drawn
#            by the hand_drawn+descriptor path.
CHEM_R_OBJECT_TYPES = frozenset(t for t, r in FIGURE_TYPES.items() if r['renderer'] in (R_STRUCT, R_SCHEME))
CHEM_H_OBJECT_TYPES = frozenset(t for t, r in FIGURE_TYPES.items()
                                if r['family'] in ('chem_structure', 'chem_scheme') and r['renderer'] in (R_HAND, R_PROJ))
# v1.3 (G-12): the chem-H types now drawn by the PROVEN projection renderers (a subset of CHEM_H — membership of
# the GAP §0.2 classes is unchanged; what changed is that these are no longer drawn by hand)
CHEM_P_OBJECT_TYPES = frozenset(t for t, r in FIGURE_TYPES.items() if r['renderer'] == R_PROJ)

# F8 — closed vocabulary of what a figural question ASKS (order is the vocabulary order).
# v1.2 (GAP-2026-11-03 R5.1): per FAMILY. The chemistry list gains the four shapes the
# real CSIR-NET paper uses and the vocabulary lacked (multiple_products "A and B",
# outcome_ratio "A major / B minor", two_part "product and order of reactivity",
# quantitative_calculation Hammett / NMR-integral). scheme_grammar stays an independent
# axis — multi_step_lettered is NOT an ask type.
ASK_TYPES = {
    'chemistry': ('product_prediction', 'starting_material_identification',
                  'reagent_identification', 'reagent_sequence',
                  'intermediate_identification', 'mechanism_identification',
                  'which_reaction_gives', 'which_structures_satisfy',
                  'stereochemical_outcome', 'stereoisomer_count', 'property_order',
                  'spectrum_to_structure', 'nomenclature', 'matching',
                  'multiple_products', 'outcome_ratio', 'two_part', 'quantitative_calculation',
                  'other'),
    'physics_graph': ('read_value', 'compare', 'trend', 'calculate', 'identify_region', 'other'),
    'data': ('read_value', 'compare', 'trend', 'calculate', 'other'),
    'text': ('assertion_reason', 'match', 'statement', 'sequence', 'fill_blank', 'direct', 'other'),
    'reasoning': ('next_in_series', 'odd_one_out', 'analogy', 'count', 'mirror_water_image',
                  'embedded_figure', 'paper_folding', 'other'),
}
FIGURAL_ASK_TYPES = ASK_TYPES['chemistry']            # v1.1 alias — every reader unchanged

# v1.3 (GAP-2026-11-05-DIFFICULTY-FIDELITY DL-22, guard G4) — ASK FORMAT is an axis of its
# own, checked BEFORE the ask type and stored beside it (`ask_format`): the FORM of the
# question (how the stem asks) as opposed to WHAT it asks. "Match the reagents in List-I
# with the products in List-II" is ask_type reagent_identification AND ask_format match;
# through v1.2 the format was lost in the ask type. SHAPE_RULES: the s1 table is ASK_TYPES
# exactly (every existing reader byte-identical; A-SHAPEMIX reads s1 targets only); the s2
# table adds the four format shapes to EVERY family (statement / match / sequence /
# assertion_reason) — targets written from it carry shape_rule 's2' and are gated by the
# WARN-only A-AXIS2, never by a QQ gate.
ASK_FORMATS = ('direct', 'statement', 'match', 'sequence', 'assertion_reason', 'combination')
_S2_SHAPES = ('statement', 'match', 'sequence', 'assertion_reason')
ASK_TYPES_S2 = {fam: tuple(list(types[:-1]) + [sh for sh in _S2_SHAPES if sh not in types] + [types[-1]])
                if types and types[-1] == 'other' else tuple(list(types) + [sh for sh in _S2_SHAPES if sh not in types])
                for fam, types in ASK_TYPES.items()}


def shapes_for(family, shape_rule='s1'):
    """The shape vocabulary of a family under a SHAPE RULE: 's1' = ASK_TYPES (unchanged),
    's2' = ASK_TYPES_S2. An unknown family -> the 'text' family; an unknown rule -> s1."""
    tab = ASK_TYPES_S2 if str(shape_rule or '').strip().lower() == 's2' else ASK_TYPES
    return tab.get(family, tab['text'])


_AF_LIST = re.compile(r'\b(?:list|column)\s*[-\u2013]?\s*(?:i{1,2}|[12ab])\b', re.I)
_AF_ITEM = re.compile(r'(?:^|[\s(])(?:[A-Da-d]|i{1,3}|iv|[1-4])[.):]\s', re.M)
_AF_COMBO = re.compile(r'\b(?:(?:[A-Da-d]|i{1,3}|iv|[1-4])\s*(?:,|and|&)\s*)+(?:[A-Da-d]|i{1,3}|iv|[1-4])\s*(?:only)?\b', re.I)
_AF_PERM = re.compile(r'^\s*(?:[A-Da-d]|[1-4]|i{1,3}|iv)(?:\s*(?:,|>|<|→|->|,\s*)\s*(?:[A-Da-d]|[1-4]|i{1,3}|iv)){2,}\s*$', re.I)
_AF_MATCH_OPT = re.compile(r'^\s*(?:[A-Da-d]\s*[-\u2013:]\s*(?:i{1,4}|iv|v|[1-5])\s*[,;]?\s*){2,}$', re.I)


def normalise_ask_format(stem, options=None):
    """The ASK FORMAT of a question from its stem and option texts: one of ASK_FORMATS.
    assertion_reason  Assertion (A) / Reason (R) pattern
    match             List-I / List-II (or Column) pairing, or options of the A-i, B-ii form
    sequence          'correct sequence / order / arrange' with permutation options
    statement         lettered / numbered statements plus 'and-only' option combinations
    combination       lettered items plus combination options, without 'statement' wording
    direct            everything else. NEVER raises; None inputs -> 'direct'."""
    try:
        st = str(stem or '')
    except Exception:                                   # noqa: BLE001
        return 'direct'
    opts = []
    for o in (options or []):
        try:
            opts.append(str(o or ''))
        except Exception:                               # noqa: BLE001
            continue
    low = st.lower()
    if re.search(r'\bassertion\b', low) and re.search(r'\breason\b', low):
        return 'assertion_reason'
    if _AF_LIST.search(st) or (opts and sum(1 for o in opts if _AF_MATCH_OPT.match(o)) >= max(2, len(opts) // 2)):
        return 'match'
    perm = sum(1 for o in opts if _AF_PERM.match(o))
    if re.search(r'\bcorrect (?:sequence|order)\b|\barrange\b|\bsequence of\b|\border of (?:steps|reactions|events)\b', low) \
            and (perm >= 2 or not opts):
        return 'sequence'
    if perm >= max(2, len(opts) // 2) and opts:
        return 'sequence'
    items = len(_AF_ITEM.findall(st))
    combo = sum(1 for o in opts if _AF_COMBO.search(o) or re.search(r'\bonly\b|\ball of (?:the above|these)\b|\bnone of (?:the above|these)\b', o, re.I))
    if items >= 2 and combo >= max(2, len(opts) // 2):
        return 'statement' if re.search(r'\bstatements?\b', low) else 'combination'
    if re.search(r'\bstatements?\b', low) and (items >= 2 or combo >= 2):
        return 'statement'
    return 'direct'
# v1.3 (GAP-2026-11-10 F-04.1): the convention tags Phase B MEASURES from the image (a figure may carry several);
# the same tuple is blueprint_core.ORG_CONVENTION_TAGS (self-test 'ft_v13_tags_match_core' pins them equal)
REPRESENTATION_TAGS = ('skeletal', 'perspective', 'chair_conformation', 'pyranose_chair', 'haworth_projection',
                       'newman_projection', 'fischer_projection', 'sawhorse_projection', 'ring_fusion_h',
                       'wavy_bond', 'reaction_scheme', 'mechanism_arrows', 'spectrum')
SCHEME_GRAMMAR_TAGS = ('plus_partner', 'two_way', 'multi_step_lettered',
                       'reagent_as_structure', 'numbered_steps')

# v1.2 — GAP-2026-11-03 §4.7: chemistry (and every other content kind) appears ONLY as
# registry rows behind generic interfaces. Each FAMILY names the blueprint_core function
# that gives an option's IDENTITY (G01), the content COMPLEXITY vector (G02 R2.3) and the
# distractor MECHANISM vocabulary key (G06). None = the kind has no deterministic
# identity_fn / vector: the reviewer decides (R1.4) and the judge alone bands (R2.3).
QUALITY_ROWS = {
    'chem_structure': {'identity_fn': 'blueprint_core.structure_identity',
                       'complexity_vector': 'blueprint_core.content_vector',
                       'mechanism_vocabulary': 'chemistry', 'ask_family': 'chemistry'},
    'chem_scheme':    {'identity_fn': 'blueprint_core.reaction_identity',
                       'complexity_vector': 'blueprint_core.content_vector',
                       'mechanism_vocabulary': 'chemistry', 'ask_family': 'chemistry'},
    'chem_spectrum':  {'identity_fn': 'blueprint_core.data_figure_identity',
                       'complexity_vector': None, 'mechanism_vocabulary': 'chemistry', 'ask_family': 'chemistry'},
    'chem_diagram':   {'identity_fn': None, 'complexity_vector': None,
                       'mechanism_vocabulary': 'chemistry', 'ask_family': 'chemistry'},
    'data':           {'identity_fn': 'blueprint_core.data_figure_identity',
                       'complexity_vector': None, 'mechanism_vocabulary': 'quantitative', 'ask_family': 'data'},
    'physics':        {'identity_fn': 'blueprint_core.data_figure_identity',
                       'complexity_vector': None, 'mechanism_vocabulary': 'quantitative', 'ask_family': 'physics_graph'},
    'geometry':       {'identity_fn': None, 'complexity_vector': None,
                       'mechanism_vocabulary': 'reasoning', 'ask_family': 'reasoning'},
    'reasoning':      {'identity_fn': None, 'complexity_vector': None,
                       'mechanism_vocabulary': 'reasoning', 'ask_family': 'reasoning'},
    'table':          {'identity_fn': 'blueprint_core.text_identity',
                       'complexity_vector': None, 'mechanism_vocabulary': 'fact', 'ask_family': 'text'},
    'apparatus':      {'identity_fn': None, 'complexity_vector': None, 'mechanism_vocabulary': 'fact', 'ask_family': 'text'},
    'biology':        {'identity_fn': None, 'complexity_vector': None, 'mechanism_vocabulary': 'fact', 'ask_family': 'text'},
    'generic':        {'identity_fn': None, 'complexity_vector': None, 'mechanism_vocabulary': 'fact', 'ask_family': 'text'},
    'raster':         {'identity_fn': None, 'complexity_vector': None, 'mechanism_vocabulary': 'fact', 'ask_family': 'text'},
    # non-figural (TEXT) items — the universal row
    'text':           {'identity_fn': 'blueprint_core.text_identity',
                       'complexity_vector': None, 'mechanism_vocabulary': 'verbal', 'ask_family': 'text'},
}
# TEXT-kind (no figure) — the option payload is the option's text
IDENTITY_KIND_BY_SEMANTIC = {'STRUCTURE': 'STRUCTURE', 'COORDINATION': 'STRUCTURE', 'REACTION': 'REACTION',
                             'PLOT': 'DATA', 'TABLE': 'TEXT'}


def quality_row(object_type_or_family):
    """QUALITY_ROWS row for a figure type (via its family) or a family name. An
    unregistered type / family -> the 'generic' row (no identity_fn: reviewer)."""
    key = str(object_type_or_family or '')
    if key in QUALITY_ROWS:
        return QUALITY_ROWS[key]
    r = FIGURE_TYPES.get(normalise(key)) if key else None
    fam = (r or {}).get('family') or 'generic'
    return QUALITY_ROWS.get(fam, QUALITY_ROWS['generic'])


def identity_kind(semantic_kind, object_type=None):
    """The blueprint_core.option_identity kind for a figure record ('STRUCTURE' |
    'REACTION' | 'DATA' | 'TEXT') or None when the family has no identity_fn."""
    row = quality_row(object_type) if object_type else None
    if row is not None and row.get('identity_fn') is None:
        return None
    # v1.2 (release review): a CONFORMATIONAL / projection drawing (chair, Newman,
    # Fischer, Haworth, sawhorse — render class 'schematic' inside the chem_structure
    # family) is the SAME molecule drawn four different ways by design: a canonical
    # SMILES identity would call "which conformer is most stable" a duplicate set.
    # Those families have no identity_fn: the reviewer decides (dHash may WARN).
    ft = FIGURE_TYPES.get(normalise(str(object_type or ''))) if object_type else None
    if ft and ft.get('family') == 'chem_structure' and ft.get('renderer') == R_PROJ:
        return 'STRUCTURE_CONFORMER'          # v1.3 (G-12): proven projection renderer, conformer-aware identity
    if ft and ft.get('family') == 'chem_structure' and ft.get('renderer') == R_HAND:
        return None
    return IDENTITY_KIND_BY_SEMANTIC.get(str(semantic_kind or '').upper())

# Keyword rules for normalise_ask_type, matched top-down on the lower-cased stem; the
# first hit wins. ORDER MATTERS: a stem naming both a starting material and a product
# asks for the starting material; 'sequence of reagents' is not a reagent question.
_ASK_RULES = (
    # v1.2 — the four shapes the vocabulary lacked, matched before the generic rules
    (r'\bproducts?\b.{0,20}\b[a-d]\s*(?:and|&)\s*[a-d]\b|\b[a-d]\s*(?:and|&)\s*[a-d]\b.{0,30}\bproducts?\b',
     'multiple_products'),
    (r'\bmajor\b.{0,12}\bminor\b|\bminor\b.{0,12}\bmajor\b|\bratio of (?:the )?products?\b|\bwhich (?:one )?of the following is true\b.{0,40}\breaction\b',
     'outcome_ratio'),
    (r'\bproducts?\b.{0,40}\b(?:and|as well as) (?:its|the) (?:order|relative) (?:of )?reactivit|\brespectively\b',
     'two_part'),
    (r'\bhammett\b|\bmole (?:percentage|fraction|%)\b|\bintegration\b|\bρ\s*value\b|\bcalculate\b|\bkinetic isotope\b.{0,30}\bvalue\b',
     'quantitative_calculation'),
    (r'\bnmr\b|spectr(?:um|a|al|oscopic)|\buv\b|m/z|\bcm\s*[-\u2212\u2013]\s*1\b|\bδ\b|chemical shift|\bsignals?\b',
     'spectrum_to_structure'),
    (r'(?:number|how many|total)\b.{0,40}\bstereoisomers?\b|\bstereoisomers?\b.{0,20}\bpossible\b', 'stereoisomer_count'),
    (r'\bsequence of (?:reagents?|steps|reactions?|conditions)\b|\b(?:reagents?|conditions)\b.{0,30}\b(?:sequence|order)\b',
     'reagent_sequence'),
    (r'\bwhich (?:one )?of the following (?:reactions?|transformations?|sequences?)\b|\bwhich reactions?\b',
     'which_reaction_gives'),
    # the ASKED noun is the product — the stem OPENS with it ("The major product of …",
    # "The product formed …"); a stem that opens with another noun ("The reagent required
    # to obtain the major product …") asks for that noun, matched by the rules below:
    # before starting material / reagent / catalyst words that merely appear in the stem
    (r'^\s*(?:the\s+)?(?:(?:major|main|final|expected|principal)\s+)?products?\b'
     r'(?:\s+(?:formed|obtained|of|in|is|are|from|when|that)\b)', 'product_prediction'),
    (r'\bstarting (?:materials?|compounds?)\b|\bprecursors?\b|\bsubstrates?\b', 'starting_material_identification'),
    (r'\bintermediates?\b', 'intermediate_identification'),
    (r'\bmechanis(?:m|ms|tic)\b', 'mechanism_identification'),
    (r'\breagents?\b|\bcatalysts?\b', 'reagent_identification'),
    (r'\bmatch(?:ing|es)?\b|\bcolumn[- ]?(?:i|1|a)\b', 'matching'),
    (r'\biupac\b|\bname of\b|\bnamed as\b|\bnomenclature\b', 'nomenclature'),
    (r'\border of\b|\b(?:increasing|decreasing) order\b|\barrange\b|\branks?\b', 'property_order'),
    (r'\bstereochemi(?:stry|cal outcome)\b|\bconfiguration\b|\b(?:r|s)\s*/\s*(?:r|s)\b|\bdiastereo|\benantiomer',
     'stereochemical_outcome'),
    (r'\bwhich (?:one )?of the following (?:compounds?|structures?|molecules?|species|ions?|carbocations?|'
     r'carbanions?|radicals?|alkenes?|dienes?|isomers?)\b(?!.{0,30}\b(?:products?|formed)\b)',
     'which_structures_satisfy'),
    (r'\bproducts?\b|\bformed\b|\bobtained\b|\byields?\b|\bgives?\b', 'product_prediction'),
    (r'\bwhich (?:one )?of the following\b.{0,40}\b(?:is|are)\b', 'which_structures_satisfy'),
)


def normalise_ask_type(text, object_type=None):
    """Free-text ask (a stem, or a transcriber's label) -> one of FIGURAL_ASK_TYPES.
    An exact vocabulary member (any case / spacing) is returned as is; otherwise the
    keyword rules above apply; 'other' when nothing matches. NEVER raises.

    The vocabulary is CHEMISTRY's (what a structure / scheme question asks). When
    `object_type` is given and is NOT a chemistry structure/scheme type (chem-R or
    chem-H — a graph, circuit, geometry or reasoning figure), the answer is always
    'other': "How many triangles are formed" is not a product prediction."""
    if object_type is not None:
        try:
            _ct = lookup(object_type)['type']
        except Exception:                                   # noqa: BLE001
            _ct = None
        if _ct not in CHEM_R_OBJECT_TYPES and _ct not in CHEM_H_OBJECT_TYPES:
            return 'other'
    if text is None:
        return 'other'
    try:
        raw = str(text).strip()                     # a hostile __str__ must not escape
    except Exception:                               # noqa: BLE001
        return 'other'
    slug = _slug(raw)
    if slug in FIGURAL_ASK_TYPES:
        return slug
    # spectroscopy abbreviations are matched CASE-SENSITIVELY on the raw text: 'IR' (not
    # iridium 'Ir'), '1H' / '13C' not followed by '-' (not '1H-indole' nomenclature)
    if re.search(r'\bIR\b|\b1H\b(?![-\u2013])|\b13C\b(?![-\u2013])|¹H|¹³C', raw):
        return 'spectrum_to_structure'
    low = ' ' + raw.lower() + ' '
    for pat, ask in _ASK_RULES:
        if re.search(pat, low):
            return ask
    return 'other'


# Exact-string aliases (after _slug()). Keep SMALL and OBVIOUS; the keyword rules below
# carry the long tail.
ALIASES = {
    'structure': 'chemical_structure',
    'molecular_structure': 'chemical_structure',
    'molecular_structures': 'chemical_structure',
    'organic_structure': 'chemical_structure',
    'chemical_structures': 'chemical_structure',
    'reaction': 'reaction_scheme',
    'reaction_schemes': 'reaction_scheme',
    'reaction_scheme_multi_step': 'reaction_scheme',
    'multi_step_reaction_scheme': 'reaction_scheme',
    'reaction_sequence': 'reaction_scheme',
    'synthetic_scheme': 'reaction_scheme',
    'synthesis_scheme': 'reaction_scheme',
    'retrosynthesis_scheme': 'reaction_scheme',
    'mechanism': 'reaction_mechanism_scheme',
    'mechanism_scheme': 'reaction_mechanism_scheme',
    'arrow_pushing_mechanism': 'reaction_mechanism_scheme',
    'catalytic_cycle': 'reaction_cycle_scheme',
    'mo_diagram': 'molecular_orbital_diagram',
    'xrd_pattern': 'diffraction_pattern',
    'x_ray_diffraction_pattern': 'diffraction_pattern',
    'powder_xrd_pattern': 'diffraction_pattern',
    'diffractogram': 'diffraction_pattern',
    'crystal_structure': 'crystal_lattice_diagram',
    'unit_cell': 'crystal_lattice_diagram',
    'unit_cell_diagram': 'crystal_lattice_diagram',
    'lattice_diagram': 'crystal_lattice_diagram',
    'galvanic_cell': 'electrochemical_cell_diagram',
    'electrolytic_cell': 'electrochemical_cell_diagram',
    'voltaic_cell': 'electrochemical_cell_diagram',
    'daniell_cell': 'electrochemical_cell_diagram',
    'fuel_cell_diagram': 'electrochemical_cell_diagram',
    'cyclic_voltammogram': 'voltammogram',
    'hplc_chromatogram': 'chromatogram',
    'gc_chromatogram': 'chromatogram',
    'dsc_curve': 'thermal_analysis_curve',
    'tga_curve': 'thermal_analysis_curve',
    'dta_curve': 'thermal_analysis_curve',
    'band_structure': 'band_structure_diagram',
    'band_diagram': 'band_structure_diagram',
    'chair_form': 'chair_conformation',
    'cyclohexane_chair': 'chair_conformation',
    'sem_image': 'electron_micrograph',
    'tem_image': 'electron_micrograph',
    'afm_image': 'micrograph',
    'stm_image': 'micrograph',
    'graph': 'line_graph',
    'curve': 'line_graph',
    'plot': 'line_graph',
    'line_chart': 'line_graph',
    'line_plot': 'line_graph',
    'xy_plot': 'line_graph',
    'bar_graph': 'bar_chart',
    'column_chart': 'bar_chart',
    'scatter_chart': 'scatter_plot',
    'table': 'data_table',
    'match_table': 'matching_table',
    'photo': 'photograph',
    'image': 'photograph',
    'picture': 'photograph',
    'figure_series_puzzle': 'figure_series',
    'series_completion': 'figure_series',
    'analogy_figure': 'figure_analogy',
    'matrix_puzzle': 'figure_matrix',
    'geometry_figure': 'geometric_figure',
    'geometrical_figure': 'geometric_figure',
    '3d_solid': 'geometric_solid',
    'solid_figure': 'geometric_solid',
    'net_of_cube': 'cube_net',
    'dice': 'dice_figure',
    'clock': 'clock_figure',
    'circuit': 'circuit_diagram',
    'apparatus': 'apparatus_diagram',
    'experimental_setup': 'apparatus_diagram',
    'flow_chart': 'flowchart',
    'flow_diagram': 'flowchart',
    'map': 'outline_map',
    'pedigree': 'pedigree_chart',
    'family_tree': 'blood_relation_tree',
    'diagram': 'generic_diagram',
    'schematic': 'schematic_diagram',
    'histogram_chart': 'histogram',
    'nmr': 'nmr_spectrum',
    'ir': 'ir_spectrum',
    'ir_spectra': 'ir_spectrum',
    'nmr_spectra': 'nmr_spectrum',
    'mass_spec': 'mass_spectrum',
    'ms_spectrum': 'mass_spectrum',
    'uv_spectrum': 'uv_vis_spectrum',
    'esr_spectrum': 'epr_spectrum',
}

# Keyword FAMILY rules, applied in order to a slug the table and the alias map do not
# know. Each (regex, canonical) pair maps a long-tail string onto a registered row so
# the generator dispatches it and the gate can check it. The hit is recorded as
# 'inferred' (lookup()['inferred_from']) so a reader can see the mapping was by rule.
INFERENCE_RULES = (
    # ORDER MATTERS: a slug is matched top-down and the first hit wins. Raster families are
    # matched on WHOLE tokens only ('photo' never matches 'photochemical'); data families
    # (spectrum / table / chart / curve …) come before the chemistry families so that
    # 'reaction_rate_plot' is a plot and 'reaction_coordinate_diagram' an energy diagram,
    # not a reaction scheme.
    # raster: whole tokens; an x-ray is raster only as an IMAGE/film/photo (x_ray_diffraction is a plot)
    (r'(^|_)(photo|photos|photograph|photographs|micrograph|micrographs|radiograph|x_ray_image|x_ray_film|x_ray_photo|xray_image|xray_photo|mri|ct_scan|satellite_image|screenshot|histology_slide|sem_image|tem_image|electron_micrograph|microscopy_image)(_|$)', 'photograph'),
    (r'(^|_)(diffraction|diffractogram|xrd)(_|$)', 'diffraction_pattern'),
    (r'(^|_)(chromatogram|chromatography_trace)', 'chromatogram'),
    (r'(^|_)(voltammogram|voltammetry)', 'voltammogram'),
    (r'(^|_)(thermogram|dsc|tga|dta)(_|$)', 'thermal_analysis_curve'),
    (r'(^|_)(band_structure|band_diagram|band_gap_diagram)', 'band_structure_diagram'),
    (r'(^|_)(latimer)', 'latimer_diagram'),
    (r'(^|_)(frost)', 'frost_diagram'),
    (r'(^|_)(pourbaix)', 'pourbaix_diagram'),
    (r'(^|_)(ellingham)', 'ellingham_diagram'),
    (r'(^|_)(tanabe)', 'tanabe_sugano_diagram'),
    (r'(^|_)(walsh)', 'walsh_diagram'),
    (r'(^|_)(orgel)', 'orgel_diagram'),
    (r'(^|_)(potential_energy_surface|pes_plot|pes_diagram)', 'potential_energy_surface'),
    (r'(^|_)(coordinate_diagram|reaction_coordinate|reaction_profile|energy_profile)', 'reaction_coordinate_diagram'),
    (r'(^|_)(energy_diagram|energy_level|jablonski|correlation_diagram)', 'energy_level_diagram'),
    (r'(^|_)(phase_diagram|pv_diagram|indicator_diagram|cycle_diagram)', 'phase_diagram'),
    (r'(^|_)(tlc)(_|$)', 'tlc_plate'),
    (r'(^|_)(chair|boat|twist_boat|conformation|conformational)(_|$)', 'chair_conformation'),
    (r'(^|_)(haworth)', 'haworth_projection'),
    (r'(^|_)(sawhorse)', 'sawhorse_projection'),
    (r'(^|_)(ray_diagram|ray_tracing|optical_ray)', 'ray_diagram'),
    (r'(^|_)(spectrum|spectra|spectrogram)', 'spectrum'),
    (r'(^|_)(table|tabular|grid_of_values)', 'data_table'),
    (r'(^|_)(pie)(_|$)', 'pie_chart'),
    (r'(^|_)(bar_chart|bar_graph|column_chart)', 'bar_chart'),
    (r'(^|_)(scatter)', 'scatter_plot'),
    (r'(^|_)(histogram)', 'histogram'),
    (r'(^|_)(isotherm|curve|graph|plot|chart|trace)(_|$)', 'line_graph'),
    (r'(^|_)(galvanic|electrolytic|electrochemical|voltaic|daniell|fuel_cell|half_cell|concentration_cell)', 'electrochemical_cell_diagram'),
    (r'(^|_)(crystal_field|ligand_field|d_orbital_splitting|cfse|splitting_diagram)', 'energy_level_diagram'),
    (r'(^|_)(solar_cell|photovoltaic)', 'apparatus_diagram'),
    (r'(^|_)(unit_cell|lattice|bravais|crystal_structure|crystal_packing|crystal_lattice)(_|$)', 'crystal_lattice_diagram'),
    (r'(^|_)(cell|cells)(_|$)', 'cell_diagram'),
    (r'(^|_)(mechanism|arrow_pushing)', 'reaction_mechanism_scheme'),
    (r'(^|_)(catalytic_cycle|reaction_cycle)', 'reaction_cycle_scheme'),
    (r'(^|_)(reaction|reactions|synthesis|synthetic|retrosynthesis|retrosynthetic|transformation_scheme)(_|$)', 'reaction_scheme'),
    (r'(^|_)(newman)', 'newman_projection'),
    (r'(^|_)(fischer)', 'fischer_projection'),
    (r'(^|_)(molecular_orbital|mo_diagram)', 'molecular_orbital_diagram'),
    (r'(^|_)(orbital)', 'orbital_diagram'),
    (r'(^|_)(coordination|complex_structure|ligand)', 'coordination_complex_structure'),
    (r'(^|_)(organometallic|metal_cluster|cluster_structure)', 'organometallic_structure'),
    (r'(^|_)(structure|structures|molecule|molecules|molecular|compound|compounds|smiles|stereo|conformer|conformers)(_|$)', 'chemical_structure'),
    (r'(^|_)(circuit|logic_gate|wiring)', 'circuit_diagram'),
    (r'(^|_)(apparatus|setup|instrument|equipment)', 'apparatus_diagram'),
    (r'(^|_)(flowchart|flow_chart|flow_diagram|block_diagram|process_diagram)', 'flowchart'),
    (r'(^|_)(pedigree|punnett|phylogen|cladogram)', 'pedigree_chart'),
    (r'(^|_)(anatom|organ|tissue|plant|animal|leaf|flower|skeleton)(_|$)', 'anatomical_diagram'),
    (r'(^|_)(venn)', 'venn_diagram'),
    (r'(^|_)(cube|net_of|dice|solid|3d)(_|$)', 'geometric_solid'),
    (r'(^|_)(mirror|water_image|reflection)', 'mirror_image_figure'),
    (r'(^|_)(fold|folding|paper_cut)', 'paper_folding_figure'),
    (r'(^|_)(series|sequence_figure)', 'figure_series'),
    (r'(^|_)(analogy)', 'figure_analogy'),
    (r'(^|_)(matrix|completion|missing_figure)', 'figure_matrix'),
    (r'(^|_)(odd_one|classification)', 'odd_one_out_figure'),
    (r'(^|_)(puzzle|tile|tiles|pattern|glyph|shape|shapes|symbol|symbols)(_|$)', 'pattern_tiles'),
    (r'(^|_)(geometr|triangle|polygon|angle|angles|circle|circles|quadrilateral)', 'geometric_figure'),
    (r'(^|_)(map)(_|$)', 'outline_map'),
    (r'(^|_)(tree|hierarchy|dendrogram)(_|$)', 'tree_diagram'),
    (r'(^|_)(timeline)', 'timeline_diagram'),
    (r'(^|_)(diagram|schematic|sketch|illustration|drawing|figure)(_|$)', 'generic_diagram'),
    # LAST: a bare 'image' / 'picture' / 'scan' with no content word is a raster; with a content
    # word ('image_of_a_table', 'reaction_scheme_image') the content decided above.
    (r'(^|_)(image|images|picture|pictures|scan|scanned)(_|$)', 'photograph'),
)

_SLUG_RE = re.compile(r'[^a-z0-9]+')


def _slug(s):
    """lower_snake_case of any object_type string; '' for a non-string / empty."""
    if s is None:
        return ''
    s = _SLUG_RE.sub('_', str(s).strip().lower()).strip('_')
    return re.sub(r'_+', '_', s)


def normalise(s):
    """Map an object_type string onto the registry.

    Returns the CANONICAL type when the string is registered, aliased, or matched by a
    keyword rule; otherwise the cleaned slug itself (an UNREGISTERED type is kept
    verbatim — never rewritten with a sentinel, because the conformance gate compares
    labels across the profile and the record and both must see the same string).
    NEVER raises; '' for empty input.
    """
    slug = _slug(s)
    if not slug:
        return ''
    if slug in FIGURE_TYPES:
        return slug
    if slug in ALIASES:
        return ALIASES[slug]
    for pat, canon in INFERENCE_RULES:
        if re.search(pat, slug):
            return canon
    return slug


def lookup(s):
    """Registry row for an object_type string (any spelling), ALWAYS a dict:
       {'type': canonical, 'raw': s, 'status': supported|unsupported|unregistered,
        'render_classes', 'semantic_kinds', 'renderer', 'family', 'inferred_from'}
    An unregistered string gets the GENERIC hand-drawn shape (the EC-V18 posture) with
    status 'unregistered' so every reader can disclose it. NEVER raises."""
    raw = s
    canon = normalise(s)
    row = FIGURE_TYPES.get(canon)
    if row is None:
        return {'type': canon, 'raw': raw, 'status': 'unregistered',
                'render_classes': SCHEMATIC + GLYPH + DATA,
                'semantic_kinds': tuple(SEMANTIC_KINDS),
                'renderer': R_HAND, 'family': 'unregistered', 'inferred_from': None,
                'note': 'not in figure_types.FIGURE_TYPES — rendered as a GENERIC '
                        'hand-drawn schematic; add a registry row to bind it'}
    slug = _slug(s)
    inferred = None if slug == canon else slug
    out = dict(row)
    out.update({'type': canon, 'raw': raw, 'inferred_from': inferred})
    return out


def status(s):
    return lookup(s)['status']


def default_kind(s):
    """The semantic kind a figure of this type registers by default (first kind)."""
    return lookup(s)['semantic_kinds'][0]


def kind_consistent(object_type, semantic_kind):
    """TYPE↔KIND consistency (LAW F2.1). Returns (verdict, detail) with verdict
    'PASS' | 'FAIL' | 'UNREGISTERED'. A reaction_scheme label over a STRUCTURE
    object is a FAIL — a false record, the one thing a pipeline must never ship."""
    row = lookup(object_type)
    if row['status'] == 'unregistered':
        return ('UNREGISTERED', f'{row["type"]!r} is not a registered figure type — '
                                f'kind {semantic_kind!r} cannot be verified')
    if semantic_kind in row['semantic_kinds']:
        return ('PASS', f'{row["type"]} ↔ {semantic_kind}')
    return ('FAIL', f'figure recorded as {row["type"]!r} but its semantic object is '
                    f'{semantic_kind!r}; the registry binds {row["type"]!r} to '
                    f'{"/".join(row["semantic_kinds"])}. A label that disagrees with '
                    f'the object it describes is a false record.')


def class_consistent(object_type, render_class):
    """TYPE↔CLASS consistency. Returns (verdict, detail); UNREGISTERED when the type
    is unknown; PASS when render_class is None (legacy spec, no class recorded)."""
    row = lookup(object_type)
    if row['status'] == 'unregistered':
        return ('UNREGISTERED', f'{row["type"]!r} is not a registered figure type')
    if render_class is None:
        return ('PASS', 'no render class recorded (legacy FigureSpec)')
    if render_class == 'option_canvas' or render_class in row['render_classes']:
        return ('PASS', f'{row["type"]} ↔ {render_class}')
    return ('FAIL', f'figure recorded as {row["type"]!r} but drawn under class '
                    f'{render_class!r}; the registry permits '
                    f'{"/".join(row["render_classes"])}.')


def _import_symbol(sym):
    """Import 'module.attr' and return the attribute, or raise."""
    mod, _, attr = sym.rpartition('.')
    m = importlib.import_module(mod)
    return getattr(m, attr)


def preflight():
    """Which renderers can THIS session load? Returns
       {'renderers': {symbol: True|False|'n/a'}, 'missing': {symbol: reason},
        'unavailable_types': [canonical types whose renderer cannot load],
        'available': {dep: bool}}
    Imports the renderer modules HERE (never at module import). NEVER raises —
    absence is reported, exactly like figural_core.preflight()."""
    avail = {}
    for dep in ('matplotlib', 'rdkit', 'PIL', 'numpy'):
        try:
            importlib.import_module(dep)
            avail[dep] = True
        except Exception:
            avail[dep] = False
    renderers, missing = {}, {}
    for sym in sorted({r['renderer'] for r in FIGURE_TYPES.values() if r['renderer']}):
        if '.' not in sym:
            # a spec-defined path (hand_drawn+descriptor, glyph_path, add_match_table):
            # needs matplotlib only, which every raster needs anyway
            renderers[sym] = True if (sym == R_TABLE or avail['matplotlib']) else False
            if not renderers[sym]:
                missing[sym] = 'matplotlib not importable'
            continue
        deps = [d for d in RENDERER_DEPS.get(sym, ()) if not avail.get(d)]
        if deps:
            renderers[sym] = False
            missing[sym] = 'missing dependency: ' + ', '.join(deps)
            continue
        try:
            _import_symbol(sym)
            renderers[sym] = True
        except Exception as e:                      # noqa: BLE001 — reported, never raised
            renderers[sym] = False
            missing[sym] = f'{type(e).__name__}: {e}'
    unavailable = sorted(t for t, r in FIGURE_TYPES.items()
                         if r['status'] == 'supported' and r['renderer']
                         and not renderers.get(r['renderer'], False))
    return {'renderers': renderers, 'missing': missing,
            'unavailable_types': unavailable, 'available': avail}


def coverage(types, session=None):
    """Classify a list of object_type strings for the KIND-COVERAGE pre-flight.
    Returns {'supported': [...], 'unsupported': [...], 'unregistered': [...],
             'unavailable': [...]}  (canonical names; 'unavailable' = supported in the
    table but its renderer cannot load in THIS session — only when `session` (a
    preflight() result) is given). Pure; never raises."""
    out = {'supported': [], 'unsupported': [], 'unregistered': [], 'unavailable': []}
    unavail = set((session or {}).get('unavailable_types') or ())
    seen = set()
    if isinstance(types, str):
        types = [types]                      # a bare string is ONE type, never its letters
    for t in (types or []):
        row = lookup(t)
        c = row['type']
        if not c or c in seen:
            continue
        seen.add(c)
        if row['status'] == 'unregistered':
            out['unregistered'].append(c)
        elif row['status'] == 'unsupported':
            out['unsupported'].append(c)
        elif c in unavail:
            out['unavailable'].append(c)
        else:
            out['supported'].append(c)
    return out


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST
# ═══════════════════════════════════════════════════════════════════════════════
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

    # 1. every row is well-formed and points at the shared vocabularies
    for t, r in FIGURE_TYPES.items():
        check(f'row_classes_{t}', all(c in RENDER_CLASSES for c in r['render_classes']))
        check(f'row_kinds_{t}', all(k in SEMANTIC_KINDS for k in r['semantic_kinds']))
        check(f'row_status_{t}', r['status'] in STATUSES)
        check(f'row_renderer_{t}', (r['renderer'] is None) == (r['status'] == 'unsupported'))
        check(f'row_slug_{t}', _slug(t) == t)
    # v1.2 — quality rows cover every family in the table; every named identity_fn /
    # vector resolves in blueprint_core; the four new chemistry shapes normalise.
    _fams = {r['family'] for r in FIGURE_TYPES.values() if r['family']}
    check('quality_rows_cover_every_family', _fams <= set(QUALITY_ROWS))
    check('ask_types_alias_unchanged_prefix', FIGURAL_ASK_TYPES[:14] == ASK_TYPES['chemistry'][:14]
          and FIGURAL_ASK_TYPES[-1] == 'other' and all(v[-1] == 'other' for v in ASK_TYPES.values()))
    check('quality_row_lookup', quality_row('reaction_scheme')['identity_fn'] == 'blueprint_core.reaction_identity'
          and quality_row('number_series')['identity_fn'] is None and quality_row('nope_type')['ask_family'] == 'text'
          and identity_kind('STRUCTURE', 'chemical_structure') == 'STRUCTURE'
          and identity_kind('STRUCTURE', 'newman_projection') == 'STRUCTURE_CONFORMER'   \
              and identity_kind('STRUCTURE', 'chair_conformation') == 'STRUCTURE_CONFORMER'
          and identity_kind('STRUCTURE', 'crystal_lattice_diagram') is None
          and identity_kind('GENERIC', 'number_series') is None)
    check('new_chemistry_shapes_normalise',
          normalise_ask_type('Identify the major products A and B in the given reactions.') == 'multiple_products'
          and normalise_ask_type('In the following reaction, which one of the following is true? A = Major; B = Minor') == 'outcome_ratio'
          and normalise_ask_type('Identify the major product formed in the following reaction and its order of reactivity in the presence of different R groups.') == 'two_part'
          and normalise_ask_type('The Hammett plot for a reaction series gives a straight line') == 'quantitative_calculation'
          and normalise_ask_type('Identify the major product, P formed in the given reaction.') == 'product_prediction')
    # v1.3 (GAP-2026-11-05 DL-22 / G4): ask FORMAT is its own axis, checked first; s1 shapes unchanged, s2 adds the four
    check('v13_ask_format_match_before_type',
          normalise_ask_format('Match the reagents in List-I with the products in List-II', ['A-ii, B-i, C-iv, D-iii', 'A-i, B-ii, C-iii, D-iv', 'A-iv, B-iii, C-i, D-ii', 'A-iii, B-iv, C-ii, D-i']) == 'match'
          and normalise_ask_type('Match the reagents in List-I with the products in List-II') == 'reagent_identification'
          and normalise_ask_format('Assertion (A): x. Reason (R): y.', ['a', 'b']) == 'assertion_reason'
          and normalise_ask_format('Which of the following statements is/are correct?\n(i) a\n(ii) b\n(iii) c', ['(i) and (ii) only', '(ii) and (iii) only', '(i) only', '(i), (ii) and (iii)']) == 'statement'
          and normalise_ask_format('The correct sequence of reagents is', ['A, B, C, D', 'B, A, D, C', 'C, D, A, B', 'D, C, B, A']) == 'sequence'
          and normalise_ask_format('Consider: A. HCl B. NaOH C. H2O. Which are acids?', ['A only', 'A and C only', 'B and C', 'All of the above']) == 'combination'
          and normalise_ask_format('The major product formed is', ['P', 'Q', 'R', 'S']) == 'direct'
          and normalise_ask_format(None, None) == 'direct' and normalise_ask_format(object(), [object()]) == 'direct')
    check('v13_shape_rules_s1_unchanged_s2_adds_four',
          shapes_for('chemistry') == ASK_TYPES['chemistry'] and shapes_for('chemistry', 's1') == ASK_TYPES['chemistry']
          and all(sh in shapes_for(f, 's2') for f in ASK_TYPES for sh in ('statement', 'match', 'sequence', 'assertion_reason'))
          and shapes_for('chemistry', 's2')[-1] == 'other' and len(shapes_for('text', 's2')) == len(ASK_TYPES['text'])
          and shapes_for('nope', 'bogus') == ASK_TYPES['text'] and all(ASK_TYPES[f] == tuple(x for x in shapes_for(f, 's2') if x in ASK_TYPES[f]) for f in ASK_TYPES))
    try:
        import importlib as _il_q
        _bcq = _il_q.import_module('blueprint_core')
        check('quality_rows_resolve_in_blueprint_core',
              all(hasattr(_bcq, v.split('.', 1)[1]) for row in QUALITY_ROWS.values()
                  for v in (row['identity_fn'], row['complexity_vector']) if v)
              and all(row['mechanism_vocabulary'] in _bcq.MECHANISM_VOCABULARY for row in QUALITY_ROWS.values()))
    except ImportError:
        pass
    check('aliases_resolve', all(v in FIGURE_TYPES for v in ALIASES.values()))
    check('alias_keys_are_slugs', all(_slug(k) == k for k in ALIASES))
    check('rules_resolve', all(c in FIGURE_TYPES for _, c in INFERENCE_RULES))
    # parity with the engines that own the mirrored vocabularies (when importable).
    # importlib, not an import statement: this module declares NO engine dependency
    # (validator check AI reads Import nodes), so it stays routable to every step.
    try:
        _pp = importlib.import_module('paper_pipeline')
        check('kinds_parity_paper_pipeline', tuple(_pp.SEMANTIC_KINDS) == SEMANTIC_KINDS)
    except Exception:
        pass
    try:
        _fc = importlib.import_module('figural_core')
        check('classes_parity_figural_core', set(_fc.FIGURE_CLASSES) == set(RENDER_CLASSES))
    except Exception:
        pass

    # 2. normalisation
    check('norm_exact', normalise('reaction_scheme') == 'reaction_scheme')
    check('norm_case_space', normalise('Reaction Scheme ') == 'reaction_scheme')
    check('norm_alias', normalise('molecular structures') == 'chemical_structure')
    check('norm_rule_reaction', normalise('two_step_reaction_panel') == 'reaction_scheme')
    check('norm_rule_mechanism', normalise('sn2_mechanism_arrows') == 'reaction_mechanism_scheme')
    check('norm_rule_photo', normalise('sem_micrograph_of_pollen') == 'photograph')
    check('norm_rule_photo_is_whole_token',
          normalise('photochemical_reaction_scheme') == 'reaction_scheme'
          and normalise('photoelectron_spectrum') == 'spectrum'
          and normalise('microscope_diagram') == 'generic_diagram')
    check('norm_rule_spectrum', normalise('raman_spectrum') == 'spectrum')
    # final-review (2026-11-01) misbinding fixtures — each string MUST land where chemistry puts it
    for _s, _want in (('x_ray_diffraction_pattern', 'diffraction_pattern'), ('xrd_pattern', 'diffraction_pattern'),
                      ('x_ray_image', 'photograph'), ('photochemical_reaction_scheme', 'reaction_scheme'),
                      ('photoelectron_spectrum', 'spectrum'), ('structure_of_photosystem', 'chemical_structure'),
                      ('microscope_ray_diagram', 'ray_diagram'), ('reaction_coordinate_diagram', 'reaction_coordinate_diagram'),
                      ('reaction_rate_plot', 'line_graph'), ('reaction_profile', 'reaction_coordinate_diagram'),
                      ('cell_structure_diagram', 'cell_diagram'), ('electrochemical_cell_diagram', 'electrochemical_cell_diagram'),
                      ('galvanic_cell', 'electrochemical_cell_diagram'), ('unit_cell_diagram', 'crystal_lattice_diagram'),
                      ('crystal_structure', 'crystal_lattice_diagram'), ('crystal_field_splitting_diagram', 'energy_level_diagram'),
                      ('cyclic_voltammogram', 'voltammogram'), ('hplc_chromatogram', 'chromatogram'),
                      ('dsc_curve', 'thermal_analysis_curve'), ('band_structure', 'band_structure_diagram'),
                      ('haworth_projection', 'haworth_projection'), ('chair_conformation', 'chair_conformation'),
                      ('tlc_plate', 'tlc_plate'), ('sem_image', 'electron_micrograph'), ('tem_micrograph', 'photograph'),
                      ('latimer_diagram', 'latimer_diagram'), ('frost_diagram', 'frost_diagram'),
                      ('pourbaix_diagram', 'pourbaix_diagram'), ('tanabe_sugano_diagram', 'tanabe_sugano_diagram'),
                      ('solar_cell_diagram', 'apparatus_diagram'), ('plant_cell', 'cell_diagram')):
        check(f'norm_review_{_s}', normalise(_s) == _want and lookup(_s)['status'] != 'unregistered')
    check('norm_review_raster_unsupported', all(status(t) == 'unsupported' for t in
          ('x_ray_image', 'sem_image', 'tem_micrograph', 'image_of_crystal', 'photograph')))
    for _s, _want in (('cell_potential_graph', 'line_graph'), ('electrochemical_series_table', 'data_table'),
                      ('galvanic_cell_emf_plot', 'line_graph'), ('fuel_cell_efficiency_chart', 'line_graph'),
                      ('crystal_field_splitting_table', 'data_table'), ('solar_cell_iv_curve', 'line_graph'),
                      ('reaction_scheme_image', 'reaction_scheme'), ('image_of_a_table', 'data_table'),
                      ('structure_image', 'chemical_structure'), ('image', 'photograph'), ('scanned_page', 'photograph'),
                      ('x_ray_image', 'photograph'), ('galvanic_cell', 'electrochemical_cell_diagram'),
                      ('cell_structure_diagram', 'cell_diagram')):
        check(f'norm_review2_{_s}', normalise(_s) == _want)
    check('norm_review2_coverage_accepts_bare_string', coverage('reaction_scheme')['supported'] == ['reaction_scheme'])
    check('norm_review_no_reaction_family_for_energy_words',
          all(normalise(t) != 'reaction_scheme' for t in ('reaction_coordinate_diagram', 'reaction_rate_plot',
                                                           'reaction_profile', 'reaction_order_plot')))
    check('norm_data_before_chemistry',
          normalise('reaction_rate_plot') == 'line_graph'
          and normalise('reaction_coordinate_diagram') == 'reaction_coordinate_diagram'
          and normalise('free_energy_diagram') == 'energy_level_diagram')
    check('norm_unregistered_kept', normalise('zorblax_widget') == 'zorblax_widget')
    check('norm_empty', normalise('') == '' and normalise(None) == '')
    check('norm_reference_exam_76_all_resolve',
          all(lookup(t)['status'] != 'unregistered' for t in (
              'adsorption_isotherm', 'apparatus_diagram', 'bar_chart', 'bar_chart_3d',
              'bioinorganic_active_site', 'bubble_line_chart', 'chemical_structure',
              'circuit_diagram', 'colour_map_plot', 'contour_map', 'contour_plot',
              'coordination_complex_structure', 'crystal_lattice_diagram', 'cube_net',
              'data_table', 'decay_series_plot', 'direction_diagram', 'distribution_curve',
              'dot_grid_puzzle', 'dsc_thermogram', 'electrostatic_potential_map',
              'energy_level_diagram', 'epr_spectrum', 'figure_analogy', 'figure_series',
              'fischer_projection', 'geometric_figure', 'geometric_solid', 'grid_puzzle',
              'ir_spectrum_with_table', 'isolobal_relationship_scheme', 'jablonski_diagram',
              'line_graph', 'log_scale_plot', 'matching_table', 'metal_cluster_structure',
              'molecular_model', 'molecular_orbital_diagram', 'molecular_symbol_diagram',
              'mossbauer_spectrum', 'network_diagram', 'newman_projection', 'nmr_spectrum',
              'nmr_spectrum_set', 'number_figure_puzzle', 'number_grid_puzzle',
              'orbital_diagram', 'organometallic_formula_table', 'organometallic_structure',
              'pattern_tiles', 'phase_diagram', 'pie_chart', 'pie_chart_with_bar_chart',
              'potential_energy_curve', 'potential_energy_diagram', 'pv_indicator_diagram',
              'qualitative_analysis_scheme', 'radar_chart', 'reaction_cycle_scheme',
              'reaction_energy_profile', 'reaction_mechanism_scheme', 'reaction_scheme',
              'rotational_spectrum', 'scatter_plot', 'stacked_bar_chart', 'step_graph',
              'stress_strain_curve', 'supramolecular_structure', 'synthesis_flow_diagram',
              'thermodynamic_cycle', 'titration_curve', 'vapour_pressure_composition_plot',
              'venn_diagram', 'vp_cycle_diagram', 'vt_cycle_diagram', 'wavefunction_plot')))

    # 3. lookup / status / kinds
    check('lookup_reaction_kind', default_kind('reaction_scheme') == 'REACTION')
    check('lookup_reaction_renderer', lookup('reaction_scheme')['renderer'] == R_SCHEME)
    check('lookup_structure_kind', default_kind('chemical_structure') == 'STRUCTURE')
    check('lookup_unsupported', status('micrograph') == 'unsupported')
    check('lookup_unregistered_shape',
          lookup('zorblax_widget')['status'] == 'unregistered'
          and lookup('zorblax_widget')['renderer'] == R_HAND
          and lookup('zorblax_widget')['type'] == 'zorblax_widget')
    check('lookup_inferred_from', lookup('two_step_reaction_panel')['inferred_from'] == 'two_step_reaction_panel')
    check('lookup_exact_not_inferred', lookup('reaction_scheme')['inferred_from'] is None)

    # 4. TYPE↔KIND gate — the fixture that fires on the reference registry (287 times)
    check('kind_fail_reaction_over_structure', kind_consistent('reaction_scheme', 'STRUCTURE')[0] == 'FAIL')
    check('kind_pass_reaction', kind_consistent('reaction_scheme', 'REACTION')[0] == 'PASS')
    check('kind_pass_structure', kind_consistent('chemical_structure', 'STRUCTURE')[0] == 'PASS')
    check('kind_pass_coordination_as_structure', kind_consistent('coordination_complex_structure', 'STRUCTURE')[0] == 'PASS')
    check('kind_unregistered', kind_consistent('zorblax_widget', 'GENERIC')[0] == 'UNREGISTERED')
    check('kind_fail_detail_names_both',
          'reaction_scheme' in kind_consistent('reaction_scheme', 'STRUCTURE')[1]
          and 'STRUCTURE' in kind_consistent('reaction_scheme', 'STRUCTURE')[1])
    check('class_pass_schematic', class_consistent('reaction_scheme', 'schematic')[0] == 'PASS')
    check('class_pass_option_canvas', class_consistent('line_graph', 'option_canvas')[0] == 'PASS')
    check('class_pass_legacy_none', class_consistent('line_graph', None)[0] == 'PASS')
    check('class_fail', class_consistent('reaction_scheme', 'data_series')[0] == 'FAIL')
    check('class_data_either', class_consistent('line_graph', 'data_single')[0] == 'PASS'
          and class_consistent('line_graph', 'data_series')[0] == 'PASS')

    # 5. coverage classification
    cov = coverage(['reaction_scheme', 'Reaction Scheme', 'micrograph', 'zorblax_widget', ''])
    check('cov_supported', cov['supported'] == ['reaction_scheme'])
    check('cov_unsupported', cov['unsupported'] == ['micrograph'])
    check('cov_unregistered', cov['unregistered'] == ['zorblax_widget'])
    check('cov_dedup', len(cov['supported']) == 1)
    cov2 = coverage(['reaction_scheme', 'line_graph'], session={'unavailable_types': ['reaction_scheme']})
    check('cov_unavailable_from_session', cov2['unavailable'] == ['reaction_scheme']
          and cov2['supported'] == ['line_graph'])
    check('cov_empty', coverage([]) == {'supported': [], 'unsupported': [], 'unregistered': [], 'unavailable': []})

    # 6. preflight never raises and reports every renderer symbol
    pf = preflight()
    syms = {r['renderer'] for r in FIGURE_TYPES.values() if r['renderer']}
    check('preflight_reports_every_renderer', set(pf['renderers']) == syms)
    check('preflight_shape', set(pf) == {'renderers', 'missing', 'unavailable_types', 'available'})
    check('preflight_rdkit_binding',
          (pf['available']['rdkit'] and pf['available']['matplotlib']) ==
          ('reaction_scheme' not in pf['unavailable_types'] and 'chemical_structure' not in pf['unavailable_types'])
          or not pf['available']['rdkit'])

    # 7. v1.1 — GAP-2026-11-02 F8 / §0.2
    check('v1_1_version', __version__ == '1.3')
    check('ask_types_closed_vocab', len(FIGURAL_ASK_TYPES) == 19 and len(set(FIGURAL_ASK_TYPES)) == 19
          and FIGURAL_ASK_TYPES[0] == 'product_prediction' and FIGURAL_ASK_TYPES[-1] == 'other')
    check('representation_tags', REPRESENTATION_TAGS[:3] == ('skeletal', 'perspective', 'chair_conformation')
          and all(t in FIGURE_TYPES for t in ('chair_conformation', 'newman_projection', 'fischer_projection',
                                              'haworth_projection', 'sawhorse_projection'))
          and CHEM_P_OBJECT_TYPES == frozenset(('chair_conformation', 'newman_projection', 'fischer_projection',
                                                'haworth_projection', 'sawhorse_projection')))
    check('scheme_grammar_tags', SCHEME_GRAMMAR_TAGS == ('plus_partner', 'two_way', 'multi_step_lettered',
          'reagent_as_structure', 'numbered_steps'))
    # §0.2 membership, pinned: a registry row that changes renderer/family moves a type
    # between classes and MUST be noticed here.
    check('chem_r_derived_matches_gap_0_2', CHEM_R_OBJECT_TYPES == frozenset((
        'chemical_structure', 'organometallic_structure', 'coordination_complex_structure',
        'metal_cluster_structure', 'supramolecular_structure', 'bioinorganic_active_site',
        'molecular_model', 'reaction_scheme', 'reaction_mechanism_scheme', 'reaction_cycle_scheme',
        'synthesis_flow_diagram')))
    check('chem_h_derived_matches_gap_0_2', CHEM_H_OBJECT_TYPES == frozenset((
        'newman_projection', 'fischer_projection', 'chair_conformation', 'haworth_projection',
        'sawhorse_projection', 'crystal_lattice_diagram', 'qualitative_analysis_scheme',
        'isolobal_relationship_scheme')))
    check('chem_r_h_examples', 'chemical_structure' in CHEM_R_OBJECT_TYPES and 'reaction_scheme' in CHEM_R_OBJECT_TYPES
          and 'newman_projection' in CHEM_H_OBJECT_TYPES and 'newman_projection' not in CHEM_R_OBJECT_TYPES
          and not (CHEM_R_OBJECT_TYPES & CHEM_H_OBJECT_TYPES)
          and 'nmr_spectrum' not in CHEM_R_OBJECT_TYPES | CHEM_H_OBJECT_TYPES
          and 'molecular_orbital_diagram' not in CHEM_R_OBJECT_TYPES | CHEM_H_OBJECT_TYPES)
    for _s, _want in (
            # real stems from GAP-2026-11-02 / the CSIR papers
            ('Identify the major product, P formed in the given reaction.', 'product_prediction'),
            ('Which of the following is the correct sequence of reagents/conditions in the given reaction?', 'reagent_sequence'),
            ('In the following reaction which one of the following starting materials, A gives the product, P?',
             'starting_material_identification'),
            ('The major product formed in the following reaction is', 'product_prediction'),
            ('The reagent(s) required for the following transformation is/are', 'reagent_identification'),
            ('The key intermediate involved in the following reaction is', 'intermediate_identification'),
            ('The total number of stereoisomers possible for the following compound is', 'stereoisomer_count'),
            ('Which of the following reactions gives the product shown?', 'which_reaction_gives'),
            ('Match the compounds in Column I with their properties in Column II', 'matching'),
            ('The correct IUPAC name of the following compound is', 'nomenclature'),
            ('The correct order of acidity of the following compounds is', 'property_order'),
            ('A compound C8H10O shows the following 1H NMR data: δ 7.2 (5H), 4.6 (1H)', 'spectrum_to_structure'),
            ('The IR spectrum shows a strong band at 1715 cm-1. The compound is', 'spectrum_to_structure'),
            ('The mechanism of the following transformation involves', 'mechanism_identification'),
            ('The stereochemical outcome of the following SN2 reaction is', 'stereochemical_outcome'),
            ('Which of the following compounds is aromatic?', 'which_structures_satisfy'),
            ('Which of the following compounds gives a positive iodoform test?', 'which_structures_satisfy'),
            ('Which of the following is the major product of the reaction?', 'product_prediction'),
            ('Which of the following compounds is the product formed?', 'product_prediction'),
            ('reagent_sequence', 'reagent_sequence'), ('Product Prediction', 'product_prediction'),
            ('', 'other'), (None, 'other'), ('Consider the following.', 'other')):
        check(f'ask_norm_{_s!r}'[:70], normalise_ask_type(_s) == _want)
    check('ask_norm_always_in_vocab', all(normalise_ask_type(x) in FIGURAL_ASK_TYPES
                                          for x in ('zz', 12, 'which of the', 'IR', 'match')))
    # the ASKED noun decides (pass-2 review): product asks are not reagent / starting
    # material asks because those words appear; 'Ir' / '1H-indole' are not spectroscopy
    for _s5, _w5 in (('The major product formed when the compound reacts with the reagent shown is', 'product_prediction'),
                     ('The product of the reaction in the presence of a Pd catalyst is', 'product_prediction'),
                     ('Oxidative addition of H2 to [Ir(CO)Cl(PPh3)2] gives the product', 'product_prediction'),
                     ('The IUPAC name of the 1H-indole derivative is', 'nomenclature'),
                     ('The major product of the reaction of the substrate with NaBH4 is', 'product_prediction'),
                     ('Which of the following reactions gives the major product shown?', 'which_reaction_gives'),
                     ('The starting material required to give the product shown is', 'starting_material_identification'),
                     ('The reagent required to obtain the major product shown is', 'reagent_identification'),
                     ('The intermediate involved in the formation of the major product is', 'intermediate_identification'),
                     ('The mechanism by which the major product is formed is', 'mechanism_identification'),
                     ('The IUPAC name of the major product is', 'nomenclature'),
                     ('The starting material that gives the major product shown below is', 'starting_material_identification'),
                     ('The catalyst required to obtain the major product is', 'reagent_identification')):
        check(f'ask_norm_asked_noun_{_s5[:40]!r}', normalise_ask_type(_s5) == _w5)
    # the vocabulary is chemistry's: a non-chemistry figure is always 'other'
    check('ask_norm_non_chem_object_type_is_other',
          normalise_ask_type('How many triangles are formed in the figure?', 'geometric_figure') == 'other'
          and normalise_ask_type('Which year gives the highest profit?', 'line_graph') == 'other'
          and normalise_ask_type('x', 'zorblax_unregistered') == 'other')
    check('ask_norm_chem_object_type_keeps_rules',
          normalise_ask_type('The major product formed in the following reaction is',
                             'reaction_scheme') == 'product_prediction'
          and normalise_ask_type('The major product formed is', 'chemical_structure') == 'product_prediction'
          and normalise_ask_type('The major product formed is', 'chair_conformation') == 'product_prediction')   # chem-H

    # D20 (fuzz 2026-11-02): str() of the input is inside the never-raise guard
    class _BadStr:
        def __str__(self):
            raise RuntimeError('boom')
    try:
        _d20 = normalise_ask_type(_BadStr()) == 'other' and normalise_ask_type(_BadStr(), 'reaction_scheme') == 'other'
    except Exception:                                   # noqa: BLE001
        _d20 = False
    check('ask_norm_hostile_str_never_raises', _d20)

    # v1.3 (GAP-2026-11-10 G-04 / G-12)
    check('ft_v13_projection_rows_proven', all(FIGURE_TYPES[k]['renderer'] == R_PROJ for k in (
        'chair_conformation', 'newman_projection', 'sawhorse_projection', 'fischer_projection', 'haworth_projection')))
    check('ft_v13_representation_tags', len(REPRESENTATION_TAGS) == 13 and 'ring_fusion_h' in REPRESENTATION_TAGS
          and 'wavy_bond' in REPRESENTATION_TAGS and 'pyranose_chair' in REPRESENTATION_TAGS)
    try:
        import blueprint_core as _bc13
        check('ft_v13_tags_match_core', tuple(_bc13.ORG_CONVENTION_TAGS) == tuple(REPRESENTATION_TAGS))
    except Exception:                                           # noqa: BLE001 — core not importable here
        check('ft_v13_tags_match_core', True)
    print(f'SELF-TEST: {passed}/{total} PASS' if passed == total
          else f'SELF-TEST: {passed}/{total} PASS — FAILED: {fails}')
    return passed == total


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    if '--preflight' in sys.argv:
        import json
        print(json.dumps(preflight(), indent=1))
        sys.exit(0)
    print("figure_types.py — figure-type registry. Run with --self-test or --preflight.")
