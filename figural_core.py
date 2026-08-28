"""
figural_core.py — shared figure renderer + conformance gates for Steps
TestCreate / MockCreate (S8-5, S8-6, S10-6A, S10-7, S10-8) and their audits.

Raised by GAP-2026-07-29-FIG-R2 and VERIFY-2026-07-29-FIG-R2.

WHY THIS ENGINE EXISTS
----------------------
Before this file the framework had exactly ONE figure helper,
render_figural_image() in S10-7, which sets ax.axis("off") in both branches and
hardcodes "solid black". Across the whole corpus there was no set_xlabel, no
set_ylabel, no legend, no rcParams and no fontsize. It is an abstract-geometry
GLYPH renderer, and it was being used to draw scientific data figures, which it
structurally cannot label. That is RC-4, and no amendment to the old helper
fixes it. This engine adds the missing data-figure path beside it.

THE SCALE CONTRACT — read this before changing any constant
-----------------------------------------------------------
Placement scale S = placed_inches / (saved_px / dpi).

The shipped defect was S = 0.500 exactly on 24/24 option canvases: the canvas
was supersampled by FIG_NATIVE_HEADROOM=2.0 and then PLACED at the un-inflated
display width, halving every label. A 10 pt matplotlib label landed at 5 pt.

The fix is NOT to place figures at their native size. That inverts the
dependency and makes layout a consequence of rendering: measured on
IIT_JAM_BIOTECHNOLOGY_Mock01, D := min(N, C) inflates figure area 1.84x and
makes a four-option MCQ need 10.4 in of option stack against a ~9.0 in page
text height, orphaning options from their stem.

Display width D is a LAYOUT decision and stays fixed per figure class. The
RENDER is solved to fit it:

    figsize   := D                      (headroom removed, see below)
    saved_px  == D * FIGURAL_DPI        (exact — constrained_layout, no tight bbox)
    S         == 1.0                    (by construction, not by luck)
    p_page    == p_native               (so the floor is enforceable directly)

FIG_NATIVE_HEADROOM is retired to 1.0. At 300 dpi the supersample bought
nothing Word's own rendering does not already provide, and it was the sole
source of the halving.

WHY bbox_inches="tight" IS BANNED HERE
--------------------------------------
Tight trimming makes saved width a function of the figure's own CONTENT (label
length, legend overflow), so S becomes uncontrolled. Measured on the exhibits:
27 distinct canvas sizes across 31 problem figures, S wandering 0.495..0.666.
GAP-R2's own replacement renderer kept tight bbox while assuming the untrimmed
width, and therefore FAILED ITS OWN GATE on first use (8.4 pt against a 9.0 pt
floor, S=0.529 where it assumed 0.500). constrained_layout gives the same good
margins with a deterministic size.

WHY G-FIGLABEL DOES NOT COUNT PIXELS
------------------------------------
GAP-R2 proposed measuring on-page label size from dark connected components.
Verified counter-example: three renders at an IDENTICAL 10 pt request, identical
1304 px width, identical S — the one whose axis titles carried "µmol photons
m⁻² s⁻¹" and "Net CO₂ assimilation" FAILED at 8.5 pt while short-label renders
PASSED. Superscripts and subscripts are small components that drag the median
down. As a HARD gate that is biased against exactly the scientific notation the
spec mandates, and would block conformant chemistry, biology and physics runs.

So the HARD gate is arithmetic over the font sizes ACTUALLY USED at render
time, recorded into the FigureSpec sidecar. The pixel statistic is retained
only as a WARN-level cross-check (g_figlabel_pixels).

CLASS: DETERMINISTIC throughout. Every gate here is arithmetic over the saved
artefact and its sidecar. None requires a view() and none is CLASS T, so all of
them are legal inside an audit's python (EXECUTION-BOUNDARY LAW). Confirming a
render actually DEPICTS a micrograph remains CLASS T and is out of scope here.
"""
from __future__ import annotations

import json
import math
import os

# =============================================================================
# RUNTIME DEPENDENCIES — declared, checked, and never fatal in an audit
# =============================================================================
# Step 0 installs python-docx and nothing else, and no spec declared a
# dependency list before v5.33. This engine needs more, so absence must be
# HANDLED rather than discovered as a traceback in a live exam session.
#
# The rule follows CLAUDE.md ("Silence is the defect; a halt is not the
# remedy") and splits by role:
#   RENDER  (Create) matplotlib is genuinely required. Without it a figure
#           cannot be drawn, so render_figure() raises a FiguralError carrying
#           the pip command instead of a bare ImportError from three frames
#           down.
#   AUDIT   every gate DEGRADES TO DORMANT-BUT-REPORTED. A gate that raises is
#           worse than a gate that is absent, because it takes the whole audit
#           down with it — and an audit that dies takes ~200 projects with it.
#           A dormant gate emits an AMBER finding naming the missing package.
DEPENDENCIES = {
    "matplotlib": "render figures (Create only)",
    "PIL":        "read PNG size and DPI (Pillow)",
    "numpy":      "pixel arithmetic for colour and degeneracy gates",
    "scipy":      "advisory pixel label estimate only",
    "fontTools":  "glyph coverage / tofu detection only",
    "rdkit":      "rasterise STRUCTURE/REACTION semantic objects (Create route: "
                  "corpus_io.structure_draw_fn RAISES without it — "
                  "GAP-2026-08-28-RDKIT-UNDECLARED)",
}
PIP_INSTALL = "pip install matplotlib pillow numpy scipy fonttools rdkit --break-system-packages"


def _try_import(name):
    """Return the module, or None if it cannot be imported. Never raises.

    ACTUALLY IMPORTS IT rather than asking importlib.util.find_spec whether it
    is installed. find_spec answers "is it on the path", and the failure that
    matters is "does importing it work" — a package can be installed and still
    fail to load (numpy built against a missing BLAS, Pillow without its
    shared libs). Guarding on presence rather than on success leaves exactly
    the traceback this block exists to prevent.
    """
    import importlib
    try:
        return importlib.import_module(name)
    except Exception:                                          # noqa: BLE001
        return None


def _have(mod):
    """True if `mod` imports cleanly. Never raises."""
    return _try_import(mod) is not None


def preflight():
    """Report which capabilities are available. Never raises, never halts.

    Call at the top of Step TestCreate/MockCreate and of their audits so a
    missing package is a stated precondition rather than a traceback.
    """
    have = {m: _have(m) for m in DEPENDENCIES}
    return {
        "available": have,
        "can_render": have["matplotlib"],
        "can_gate_pixels": have["PIL"] and have["numpy"],
        "can_render_structures": have["rdkit"],
        "missing": sorted(m for m, ok in have.items() if not ok),
        "pip": PIP_INSTALL,
    }

# --- palette -----------------------------------------------------------------
# Okabe-Ito. Colour-blind safe (deuteranopia/protanopia/tritanopia), print safe.
OKABE_ITO = [
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # bluish green
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow (must carry a dark edge when used as a fill)
    "#000000",  # black
]
# Redundant encoding: colour is NEVER the sole carrier of meaning. Every series
# also differs in dash pattern and marker, so a figure survives greyscale
# printing and colour-blind readers even if the palette is overridden.
LINESTYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 1)), "-", "--"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]

# --- scale contract ----------------------------------------------------------
FIGURAL_DPI = 300
FIG_NATIVE_HEADROOM = 1.0     # RETIRED. Must stay 1.0; see module docstring.
FIG_COLUMN_IN = 6.0           # usable text column, A4/Letter at 1 in margins
FIG_PROBLEM_DISPLAY_IN = 4.0  # was 2.3 — too small to carry a labelled axis
FIG_OPT_DISPLAY_IN = 1.3      # unchanged: a layout invariant, not a defect
FIG_MIN_STROKE_PT = 1.4
# A labelled axis has an irreducible cost in inches: two axis titles, two tick
# label bands and a legend. Below this width matplotlib's constrained_layout
# collapses the plot area to zero and emits a DEGENERATE figure while every
# size and label gate still passes, because the PNG is the requested pixel size
# and the fonts were the requested points. Silent degeneracy is the one failure
# mode a purely arithmetic gate cannot see, so it is bounded at the producer.
FIG_MIN_DATA_DISPLAY_IN = 3.0
MIN_PLOT_AREA_FRAC = 0.18   # plot area / canvas area; below this = degenerate
# v5.55 GAP-2026-08-19-FIGFIT. G-FIGDEGEN's 18% floor catches a COLLAPSED plot
# area. It does not catch a figure that merely wastes its page allocation, and
# the delivered corpus sat between the two: median problem-figure ink bbox was
# 29.6% of canvas area — clear of 18%, and drawing a molecule at roughly half
# the linear size its 4.0 in slot paid for. The fitter now maximises fill, so a
# figure below this floor means the fitter did not run or was overridden.
# CALIBRATED, NOT ASPIRATIONAL. Delivered corpus (pre-fix) median 29.6%,
# range 21.4-78.0%. Post-fix, shared-window option sets measure 0.43-0.55
# and single figures higher; the union window of an option set is by
# definition larger than any one option, so a floor calibrated on single
# figures would fire on every correctly-uniform set. 0.45 clears every
# conformant post-fix measurement and still catches the shipped waste.
MIN_CONTENT_FILL_FRAC = 0.45

# --- label floors, AT DISPLAY SIZE -------------------------------------------
ONPAGE_FLOOR_PT = {
    "data_series": 9.0,
    "data_single": 9.0,
    "schematic": 9.0,
    "reasoning_glyph": 8.0,
    "option_canvas": 8.0,
}
ONPAGE_TARGET_PT = 10.0

FIGURE_CLASSES = tuple(ONPAGE_FLOOR_PT)
# Classes for which a multi-hue palette is REQUIRED (G-FIGCOLOUR applies).
COLOUR_REQUIRED = ("data_series",)
# Classes which MUST be monochrome (G-FIGMONO applies).
MONO_REQUIRED = ("reasoning_glyph",)
# v5.46 (GAP-2026-08-07-FIGACCENT): classes for which >=1 accent hue is
# MANDATORY (G-FIGACCENT applies). Closes the enforcement gap behind the
# S10-6A palette column: "1 accent hue" for data_single (now mandatory, owner
# decision 2026-08-07) and ">=1 accent for the item under interrogation" for
# schematic were normative prose with NO gate, so an all-black paper (IIT JAM
# PHYSICS Mock01: 16/16 figures at 0.0000% coloured pixels) and an accented
# paper (IIT JAM BIOTECH Mock01: 0.10-1.11%) both passed identically.
ACCENT_REQUIRED = ("data_single", "schematic")
# Accent presence floor for coloured_fraction(). Calibrated on the real
# corpus: accented figures measure >=0.105% (BIO Mock01 minimum, a single
# small blue NO2 label), all-black figures measure 0.0000%; 0.05% splits the
# populations with a 2x margin and zero false positives. DELIBERATELY not
# gated on dominant_hues(): its minimum-area cut swallows small accents (the
# same BIO q14 label registers 0 dominant hues while being clearly blue).
ACCENT_MIN_FRAC = 0.0005

# Glyphs every figure font must cover; a tofu box is a HARD failure.
REQUIRED_GLYPHS = "µ⁻²₂Å°αβθ×⇌≥≤‰Δλ"


# =============================================================================
# SEVERITY MODEL (v5.33)
# =============================================================================
# OWNER DIRECTIVE: no image-COLOUR condition may ever halt a run. This is not a
# concession; it is the framework's own doctrine. CLAUDE.md: "A CLASS T failure
# must be LOUD, and must NOT halt. These are separate properties and the corpus
# conflated them... Silence is the defect; a halt is not the remedy." A grey
# figure is a DEGRADED paper, never a void one.
#
#   AMBER      report at FAIL severity, force the amber delivery footer, ALWAYS
#              complete. Every colour and accessibility condition lives here.
#   VOID_ITEM  this QUESTION is invalid because the rendering leaks an answer
#              cue. Drop or regenerate the single question; the paper continues.
#              Never halts the run.
#   BLOCKING   reserved for REGRESSION detection on v5.33+ output only, where
#              the gate is unfireable by construction and a firing means the
#              renderer contract itself was broken. Exempt for legacy output
#              (no FigureSpec sidecar) under EC-V18.
#
# Verified over 144 figures spanning display widths 1.3-7.5 in, 2-8 series and
# four label sets including full scientific notation: G-FIGSCALE, G-FIGLABEL,
# G-FIGDPI, G-FIGCOLOUR, G-FIGSERIES and G-FIGGLYPH fired 0 times. They are
# regression detectors, not degradation reporters, which is the only reason they
# are safe to make BLOCKING on new output.
SEVERITY = {
    # colour + accessibility — NEVER halts, per owner directive
    "G-FIGCOLOUR":  "AMBER",
    "G-FIGACCENT":  "AMBER",
    "G-FIGCVD":     "AMBER",
    "G-FIGSERIES":  "AMBER",
    "G-FIGALT":     "AMBER",
    "W-FIGLABELPX": "AMBER",
    "G-FIGGLYPH":   "AMBER",
    # answer-cue leaks — void the ITEM, never the run
    "G-FIGMONO":    "VOID_ITEM",
    "G-FIGOPTUNIF": "VOID_ITEM",
    # v5.55: an overprinted label makes the option unreadable, and an option
    # set drawn at divergent scales is a size cue. Both void the ITEM.
    "G-FIGCOLLIDE":   "VOID_ITEM",
    "G-FIGOPTWINDOW": "VOID_ITEM",
    # renderer-contract regressions on v5.33+ output
    "G-FIGSCALE":   "BLOCKING",
    "G-FIGLABEL":   "BLOCKING",
    "G-FIGDPI":     "BLOCKING",
    "G-FIGDEGEN":   "BLOCKING",
    # v5.55. BLOCKING is safe here for the reason the other four are: on
    # v5.55+ output the renderer GUARANTEES the property, so a firing means
    # someone removed the fitter. EC-V18 downgrades it to AMBER for every
    # pre-v5.55 figure (no fit record), so ~200 existing exams keep auditing
    # and delivering untouched while still reporting the defect loudly.
    "G-FIGFIT":     "BLOCKING",
    "W-FIGFITPX":   "AMBER",
    # v5.57 — census-vs-pixel agreement. BLOCKING for the reason G-FIGFIT is:
    # on v5.57+ output the census is complete by construction, so ink outside
    # the measured box means a render path the census does not see — the
    # exact shape that shipped Q44. Legacy (no content_bbox_px) is silent.
    "G-FIGINK":     "BLOCKING",
    "W-FIGINK":     "AMBER",       # v5.57 — the same check on an axis-ON render
}
NEVER_BLOCKING_ON_COLOUR = ("G-FIGCOLOUR", "G-FIGACCENT", "G-FIGCVD", "G-FIGSERIES", "G-FIGMONO")

# Engine-side ids are G-* (hard) and W-* (advisory). The audit catalogue is A-*,
# and Check M-GATE matches emitted gate names against A-* tokens in the spec
# text, so the audit layer MUST emit A-* names. The mapping is explicit and
# self-tested here rather than left implicit in spec prose, because a silent
# mismatch shows up as "catalogue lists X but the script never emits it" —
# a red check, not a wrong figure, and therefore easy to paper over.
AUDIT_GATE_ID = {
    "G-FIGCOLOUR":  "A-FIGCOLOUR",
    "G-FIGACCENT":  "A-FIGACCENT",
    "G-FIGCVD":     "A-FIGCVD",
    "G-FIGSERIES":  "A-FIGSERIES",
    "G-FIGGLYPH":   "A-FIGGLYPH",
    "G-FIGALT":     "A-FIGALT",
    "W-FIGLABELPX": "A-FIGLABELPX",
    "G-FIGMONO":    "A-FIGMONO",
    "G-FIGOPTUNIF": "A-FIGOPTUNIF",
    "G-FIGSCALE":   "A-FIGSCALE",
    "G-FIGLABEL":   "A-FIGLABEL",
    "G-FIGDPI":     "A-FIGDPI",
    "G-FIGDEGEN":   "A-FIGDEGEN",
    "G-FIGFIT":       "A-FIGFIT",
    "G-FIGINK":       "A-FIGINK",
    "W-FIGINK":       "A-FIGINKPX",
    "G-FIGCOLLIDE":   "A-FIGCOLLIDE",
    "G-FIGOPTWINDOW": "A-FIGOPTWINDOW",
    "W-FIGFITPX":     "A-FIGFITPX",
}


def audit_gate_id(finding):
    """G-FIGCOLOUR: ... -> A-FIGCOLOUR. Unknown ids pass through unchanged."""
    gid = finding.split(":")[0].strip()
    return AUDIT_GATE_ID.get(gid, gid)


def _class_of(spec):
    """Figure class, tolerating an absent or partial FigureSpec.

    LEGACY SAFETY, EC-V18. Output rendered before v5.33 has NO sidecar, so the
    audit sees spec == {}. Every gate MUST tolerate that and still return a
    verdict. An earlier draft indexed spec["class"] directly and raised
    KeyError on the first delivered drawing, which would have crashed the audit
    for all ~200 existing exams — the precise inverse of EC-V18, and a direct
    breach of CLAUDE.md: "Phase C must never raise, never halt, and always
    complete." A gate that throws is worse than a gate that is absent, because
    it takes the whole audit down with it.
    """
    c = (spec or {}).get("class")
    return c if c in FIGURE_CLASSES else "unknown"


def _floor_of(spec):
    return ONPAGE_FLOOR_PT.get(_class_of(spec), min(ONPAGE_FLOOR_PT.values()))


def severity_of(gate_id):
    return SEVERITY.get(gate_id.split(":")[0].strip(), "AMBER")


def is_legacy(spec):
    """No FigureSpec sidecar == rendered before v5.33. EC-V18 legacy tolerance:
    BLOCKING gates downgrade to AMBER so ~200 existing exams keep auditing."""
    return not spec or spec.get("placement_scale") is None


def triage(findings, spec=None):
    """Split gate findings into the three severity buckets.
    NEVER raises. NEVER halts. Always returns."""
    out = {"BLOCKING": [], "VOID_ITEM": [], "AMBER": []}
    legacy = is_legacy(spec)
    for f in findings:
        gid = f.split(":")[0].strip()
        sev = severity_of(gid)
        # A gate that could not RUN is not a failed artefact. Report it loudly
        # and never halt on it: a missing package is an environment defect, and
        # blocking every paper over one would be the halt-as-remedy mistake.
        if "DORMANT" in f:
            out["AMBER"].append(f)
            continue
        if sev == "BLOCKING" and legacy:
            sev = "AMBER"          # EC-V18
        if gid in NEVER_BLOCKING_ON_COLOUR and sev == "BLOCKING":
            sev = "AMBER"          # owner directive, belt and braces
        out[sev].append(f)
    return out


class FiguralError(AssertionError):
    """Hard failure in the figural contract."""


# =============================================================================
# FigureSpec — the declaration that makes a figure auditable without vision
# =============================================================================
def make_figure_spec(question, fig_class, display_in, series=None, axes=None,
                     key_mode="none", target_onpage_pt=ONPAGE_TARGET_PT,
                     role="problem", canvas_aspect=None):
    """Build the sidecar record. Gates cross-check this against the PNG.

    A spec that declares two hues while the PNG contains one is a HARD failure —
    this is the check that would have caught the monochrome defect on day one.
    """
    if fig_class in ("data_series", "data_single") and \
            float(display_in) < FIG_MIN_DATA_DISPLAY_IN:
        raise FiguralError(
            f"G-FIGDEGEN: class {fig_class!r} requested at {display_in} in, below "
            f"FIG_MIN_DATA_DISPLAY_IN={FIG_MIN_DATA_DISPLAY_IN}. A labelled axis "
            f"does not fit; constrained_layout would collapse the plot area to "
            f"zero and emit a degenerate figure that every arithmetic gate "
            f"passes. Use 'schematic', or raise the display width.")
    if fig_class not in FIGURE_CLASSES:
        raise FiguralError(
            f"G-FIGCLASS: unknown figure class {fig_class!r}; "
            f"must be one of {FIGURE_CLASSES}. There is no default class — "
            f"inference failure is HARD, never a fallback.")
    series = list(series or [])
    if fig_class in COLOUR_REQUIRED and len(series) < 2:
        raise FiguralError(
            f"G-FIGCLASS: class {fig_class!r} means >=2 comparable series; "
            f"got {len(series)}. Use 'data_single' for one series.")
    return {
        "question": question,
        "class": fig_class,
        "role": role,
        "series": series,
        "axes": axes or {},
        "key_mode": key_mode,
        "target_onpage_pt": float(target_onpage_pt),
        "display_in": float(display_in),
        "png_dpi": FIGURAL_DPI,
        # v5.55. Canvas aspect (h/w) is a DECLARED figure property, no longer
        # a hardcoded 0.72. None keeps the historical default, so every
        # un-regenerated exam is unaffected; a portrait structure may declare
        # its own. Measured motivation: q27 of the reference paper used 33% of
        # its canvas width and 97% of its height inside a 0.72 landscape box.
        "canvas_aspect": (None if canvas_aspect is None
                          else max(FIG_CANVAS_ASPECT_MIN,
                                   min(FIG_CANVAS_ASPECT_MAX,
                                       float(canvas_aspect)))),
        # filled in by render_figure()
        "png_px": None,
        "font_pt_native": None,
        "placement_scale": None,
        # v5.55 — written by fit_and_deconflict(); read by G-FIGFIT /
        # G-FIGCOLLIDE / G-FIGOPTWINDOW. Absent == legacy (EC-V18).
        "fit": None,
    }


def series_defaults(n, monochrome=False):
    """n series, each distinct in colour AND linestyle AND marker (Q7b.2)."""
    if n > len(OKABE_ITO):
        raise FiguralError(f"G-FIGSERIES: {n} series exceeds the {len(OKABE_ITO)}-hue "
                           f"palette; split the figure.")
    return [{"id": f"s{i+1}",
             "label": f"Series {i+1}",
             "colour": "#000000" if monochrome else OKABE_ITO[i],
             "linestyle": LINESTYLES[i],
             "marker": MARKERS[i]} for i in range(n)]


# =============================================================================
# Render
# =============================================================================
def _font_plan(spec):
    """Font sizes to request from matplotlib.

    Because S == 1.0 by construction, requested pt == on-page pt and the floor
    is enforceable directly. The one place a pre-inflation is still needed is a
    figure capped at the column width (E-1): then S = C/N < 1 and fonts are
    divided through by it.
    """
    floor = ONPAGE_FLOOR_PT[spec["class"]]
    target = max(float(spec["target_onpage_pt"]), floor)
    d = float(spec["display_in"])
    cap = min(1.0, FIG_COLUMN_IN / d) if d > 0 else 1.0
    inflate = 1.0 / cap
    body = target * inflate
    small = max(floor, target - 1.0) * inflate
    return {
        "font.size": body,
        "axes.titlesize": (target + 1.0) * inflate,
        "axes.labelsize": body,
        "xtick.labelsize": small,
        "ytick.labelsize": small,
        "legend.fontsize": small,
        "_floor": floor,
        "_body": body,
        "_small": small,
    }


def figure_style(spec):
    """rcParams for a figure that will be PLACED at spec['display_in'] inches."""
    fp = _font_plan(spec)
    d = float(spec["display_in"])
    h = FIG_NATIVE_HEADROOM
    # v5.55: the 0.72 is the DEFAULT, not the law. It stays the default so
    # every existing exam renders exactly as before; a spec may declare its
    # own, and render_option_set() gives one aspect to a whole option set.
    asp = spec.get("canvas_aspect") or FIG_CANVAS_ASPECT_DEFAULT
    return {
        "figure.figsize": (d * h, d * h * asp),
        "figure.dpi": FIGURAL_DPI,
        "savefig.dpi": FIGURAL_DPI,
        "font.size": fp["font.size"],
        "axes.titlesize": fp["axes.titlesize"],
        "axes.labelsize": fp["axes.labelsize"],
        "xtick.labelsize": fp["xtick.labelsize"],
        "ytick.labelsize": fp["ytick.labelsize"],
        "legend.fontsize": fp["legend.fontsize"],
        "lines.linewidth": max(FIG_MIN_STROKE_PT, 1.8),
        "lines.markersize": 5,
        "axes.linewidth": 0.9,
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        # Opaque white: a transparent background renders as invisible text in
        # dark-mode viewers. S10-7 Q2 previously PREFERRED transparent.
        "savefig.transparent": False,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        # BANNED: savefig.bbox "tight" — see module docstring.
        "savefig.bbox": "standard",
    }


def render_figure(draw_fn, out_path, spec, palette=None, window=None):
    """
    draw_fn(ax, series, palette) -> None.  Draws ONE visual unit.
    window : v5.55 — an explicit (x0, y0, x1, y1) DATA window to draw in,
        overriding the fitter's own. render_option_set() passes the union
        window of an option set here so every option shares one scale.
    spec : from make_figure_spec(). MUTATED with the measured artefact facts.
    palette : v5.46 — optional hue list overriding OKABE_ITO (the plumbing
        Q7b.1 promised; exam_config wiring stays RESERVED until a rich-colour
        release). None -> OKABE_ITO. Ignored for MONO_REQUIRED classes, which
        always render black.

    The caller MUST place the PNG at exactly spec['display_in'] inches
    (capped to FIG_COLUMN_IN). S10-8 does this; nothing else may.
    """
    if not _have("matplotlib"):
        raise FiguralError(
            "G-FIGDEP: matplotlib is required to render a figure and is not "
            "installed. Step 0 installs python-docx only. Run:\n  "
            + PIP_INSTALL)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    mono = spec["class"] in MONO_REQUIRED
    base = list(palette) if palette else OKABE_ITO
    palette = ["#000000"] * len(base) if mono else base
    style = figure_style(spec)

    # v5.55 FULL BLEED. Classes with no ticks, no axis titles and no legend
    # have nothing for constrained_layout to reserve margin FOR, and that
    # reserved margin was measured at 35% of every option canvas width — the
    # frame sat at 252 of 390 px and the molecule inside it smaller again.
    full_bleed = (spec["class"] in FULL_BLEED_CLASSES
                  or spec.get("role") == "option")
    with plt.rc_context(style):
        if full_bleed:
            fig, ax = plt.subplots(constrained_layout=False)
            fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
            ax.set_axis_off()
        else:
            fig, ax = plt.subplots(constrained_layout=True)
        draw_fn(ax, spec["series"], palette)
        # THE SAFETY NET (v5.55). Measure what was actually drawn, separate
        # overprinted labels, and fit the data window so every mark clears
        # the frame. Runs for every class: a data figure can overprint a
        # legend on a curve exactly as a structure overprints two labels.
        rec = fit_and_deconflict(fig, ax, spec, window=window)
        if full_bleed:
            # The frame is the RENDERER's, drawn last, above every artist.
            draw_frame(ax)
        rec["data_window"] = [float(ax.get_xlim()[0]), float(ax.get_ylim()[0]),
                              float(ax.get_xlim()[1]), float(ax.get_ylim()[1])]
        fig.savefig(out_path, dpi=FIGURAL_DPI, facecolor="white",
                    transparent=False)
        plt.close(fig)

    im = Image.open(out_path)
    dpi = im.info.get("dpi", (FIGURAL_DPI, FIGURAL_DPI))[0] or FIGURAL_DPI
    native_in = im.width / dpi
    placed_in = min(float(spec["display_in"]), FIG_COLUMN_IN)

    fp = _font_plan(spec)
    spec["png_px"] = [im.width, im.height]
    spec["png_dpi"] = round(float(dpi))
    spec["placed_in"] = round(placed_in, 4)
    spec["placement_scale"] = round(placed_in / native_in, 4) if native_in else None
    spec["font_pt_native"] = {
        "body": round(fp["_body"], 3),
        "small": round(fp["_small"], 3),
        "floor": fp["_floor"],
    }
    return spec


def write_spec_sidecar(spec, png_path):
    """Sidecar next to the PNG. The audit reads this; it is the FigureSpec."""
    p = os.path.splitext(png_path)[0] + ".figspec.json"
    with open(p, "w") as fh:
        json.dump(spec, fh, indent=1, sort_keys=True)
    return p


def alt_text(spec):
    """G-FIGALT. Every drawing carries wp:docPr/@descr naming the question,
    the class and the quantities plotted."""
    ax = spec.get("axes") or {}
    def _ax(k):
        a = ax.get(k) or {}
        t, u = a.get("title"), a.get("units")
        return f"{t} ({u})" if t and u else (t or "")
    x, y = _ax("x"), _ax("y")
    quant = f" {y} against {x}." if (x and y) else ""
    names = ", ".join(s.get("label", s.get("id", ""))
                      for s in (spec.get("series") or []))
    key = f" Series: {names}." if names else ""
    return (f"Question {spec.get('question','?')} "
            f"{spec.get('role','problem')} figure, "
            f"class {_class_of(spec)}.{quant}{key}").strip()


# =============================================================================
# Colour-vision arithmetic — pinned so G-FIGCVD is reproducible
# =============================================================================
# GAP-R2 left the hue-extraction method unstated, and independent
# re-measurement of the same exhibits produced 55/65/91 % collapse against its
# reported 42/50/51 %. Same direction, different number. A HARD gate cannot
# rest on an unstated method, so every constant below is normative.
CVD_QUANT = 32          # RGB cube quantisation step
CVD_MIN_AREA = 0.0008   # a hue must cover >=0.08 % of the image to count
CVD_SAT_MIN = 60        # channel spread required to count as a hue at all
DEUT_MIN_SEP = 60.0     # summed channel units after the deuteranope transform
# NO LUMINANCE THRESHOLD. GAP-R2 §7.3.3 demanded >=20/255 luminance separation AND
# a CVD-safe palette, while §7.3.1 mandated Okabe-Ito. Those clauses are mutually
# unsatisfiable: measured over the 10 pairs of the first five Okabe-Ito hues,
# the deuteranope clause passes 10/10 and the luminance clause fails 3/10
# (blue/bluish-green 18.6, vermillion/bluish-green 13.0, purple/orange 11.0).
# Okabe-Ito is CVD-safe by design; it was never greyscale-LUMINANCE-safe, and no
# 8-hue palette can be both. Greyscale survival is delivered by Q7b.2 REDUNDANT
# ENCODING and gated by G-FIGSERIES. Gating it again on luminance made G-FIGCVD
# fire 569 times across 144 conformant figures — a gate that flags its own
# mandated palette is not a gate.
LUMA_ADVISORY_SEP = 12.0  # advisory only, never a failure


def _luma(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _deuteranope(c):
    r, g, b = c
    return (0.625 * r + 0.375 * g,
            0.700 * r + 0.300 * g,
            0.300 * g + 0.700 * b)


def dominant_hues(png_path):
    """Normative hue extraction. Returns a list of quantised RGB tuples.
    Returns None (not []) when pixel tooling is unavailable, so callers can
    tell "no hues found" apart from "could not look"."""
    np = _try_import("numpy")
    _pil = _try_import("PIL.Image")
    if np is None or _pil is None:
        return None
    Image = _pil
    a = np.array(Image.open(png_path).convert("RGB")).reshape(-1, 3).astype(int)
    sat = a.max(1) - a.min(1)
    sel = a[sat > CVD_SAT_MIN]
    if len(sel) < 50:
        return []
    q = (sel // CVD_QUANT) * CVD_QUANT
    vals, counts = np.unique(q, axis=0, return_counts=True)
    keep = vals[counts > max(30, CVD_MIN_AREA * len(a))]
    return [tuple(int(x) for x in v) for v in keep]


def coloured_fraction(png_path):
    """Fraction of visible pixels carrying any chroma. None if unavailable."""
    np = _try_import("numpy")
    _pil = _try_import("PIL.Image")
    if np is None or _pil is None:
        return None
    Image = _pil
    a = np.array(Image.open(png_path).convert("RGBA"))
    vis = a[..., 3] > 16
    rgb = a[..., :3].astype(int)
    sat = rgb.max(2) - rgb.min(2)
    return float(((sat > 25) & vis).sum()) / max(int(vis.sum()), 1)


# =============================================================================
# LAYOUT FIT + LABEL DECONFLICT  (v5.55 — GAP-2026-08-19-FIGFIT)
#
# WHY THIS EXISTS. Through v5.54 every figure gate in this engine measured
# METADATA — canvas pixels, DPI, placement scale, requested font points,
# declared hues. NOTHING measured WHERE THE INK LANDED. The consequence,
# measured on IIT_JAM_CHEMISTRY Mock01 (42 delivered drawings):
#     • 3 of 24 option canvases had ink OUTSIDE the drawn frame (up to 4.06%
#       of the image's ink) — atom labels hanging off the left edge, so the
#       frame reads as cutting the structure in half;
#     • 10 of 24 option canvases had content within 12 px (0.04 in) of the
#       frame, several with a white label bbox punching a visible hole in it;
#     • label-on-label collisions (two CH3 groups overprinted) on Newman
#       projections, unreadable at the 1.3 in display size;
#     • the frame occupied 252 of 390 canvas px (64.6% of width), and the ink
#       inside it a fraction of that again — median problem-figure ink bbox was
#       29.6% of its canvas area, so ~70% of every figure's page area was white;
#     • one problem figure (q27) used 33% of the canvas width and 97% of its
#       height, because the canvas aspect was hardcoded 0.72 landscape while
#       the molecule was portrait.
# EVERY ONE OF THOSE FIGURES PASSED EVERY GATE. They were conformant and
# unreadable, which is the exact failure shape CLAUDE.md calls out: the defect
# was SILENT.
#
# THE ROOT CAUSE IS ARCHITECTURAL, NOT COSMETIC. draw_fn is authored per
# question at generation time. Layout correctness was therefore delegated to
# hand-written drawing code, once per question, across ~200 exams, with no
# safety net and no measurement. Authoring discipline does not scale to that;
# a renderer-side invariant does. This block is that invariant: after draw_fn
# returns and BEFORE the artefact is saved, the renderer measures every
# artist's true rendered extent, resolves label collisions, fits the data
# window so all ink sits inside the frame with a mandated clearance, and
# records what it did into the FigureSpec so the gates can check it as
# ARITHMETIC (Q9.6 doctrine — never as pixel connected components).
#
# THE FRAME BELONGS TO THE RENDERER. Through v5.54 draw_fn drew its own border
# box, so a label with a white bbox drawn afterwards could erase a segment of
# it. The frame is now drawn HERE, last, at axes-fraction coordinates with
# zorder above every content artist. A label can no longer punch a hole in it,
# and it can no longer land in the middle of the canvas leaving a dead margin.
# =============================================================================

# Ink must clear the frame by this much AT DISPLAY SIZE. 0.05 in at 300 dpi is
# 15 px on the native canvas — comfortably above the 1.4 pt frame stroke (5.8
# px) so the clearance is visible, not merely arithmetic.
FIG_MIN_CLEARANCE_IN = 0.05
# Label-to-label and label-to-stroke breathing room at display size.
FIG_LABEL_PAD_IN = 0.020
# A label may be nudged this far from its authored anchor before the renderer
# stops moving it and reports a residual instead. Beyond this the label is no
# longer identifying the atom/vertex it was attached to, and a silently
# re-attached label is worse than a reported collision.
FIG_LABEL_MAX_SHIFT_IN = 0.10
# Relaxation passes. Measured: chemistry option canvases converge in 2-4.
FIG_FIT_MAX_PASSES = 8
# Residual overlap tolerated between two label boxes, as a fraction of the
# smaller box's area. Antialiased glyph boxes touch at 0 penetration; 2% is
# below visual detectability at 300 dpi and above float noise.
FIG_COLLIDE_TOL = 0.02
# Canvas aspect (height/width). The 0.72 of v5.33-v5.54 is retained as the
# DEFAULT so every un-regenerated exam renders byte-comparably, but it is no
# longer hardcoded: the fitter may propose a content-driven aspect within this
# band, and an option SET always shares one.
FIG_CANVAS_ASPECT_DEFAULT = 0.72
FIG_CANVAS_ASPECT_MIN = 0.55
FIG_CANVAS_ASPECT_MAX = 1.30
# Classes whose axes carry no ticks/titles and must therefore fill the canvas
# edge to edge. constrained_layout's default margins are pure waste for these
# and were most of the 64.6% frame-to-canvas ratio measured above.
FULL_BLEED_CLASSES = ("option_canvas", "reasoning_glyph")


def _renderer(fig):
    fig.canvas.draw()
    return fig.canvas.get_renderer()


def _visible_artists(ax):
    """Every artist that puts ink on an option/schematic canvas.

    Deliberately NOT ax.get_children() wholesale: the axes patch (background)
    and the spines are container chrome, not content, and including them makes
    the content bbox always exactly the axes bbox — which is how a fit check
    can be written and still measure nothing.

    v5.57 GAP-2026-08-20-FIGURAL-INK-CENSUS. Through v5.56 the census read
    ax.texts / ax.lines / ax.patches / ax.collections / ax.images and dropped
    any Text whose string was empty. Two kinds of ink were therefore INVISIBLE
    to the fitter: (a) an Annotation's ARROW — `ax.annotate('', xy=A, xytext=B,
    arrowprops=...)` is a common bond/arrow idiom, its arrow_patch is a CHILD
    of the Annotation (never in ax.patches), and the empty string removed the
    Annotation itself; (b) anything reached only through ax.artists / tables /
    legend. The fitter then centred the window on the ink it could see and
    CLIPPED the rest at the frame, recorded clearance >= floor, status OK, and
    every gate stayed green — a substituent bond ran off the canvas with no
    label (delivered paper, Q44). The census now walks the axes' children and
    adds an Annotation's arrow_patch explicitly; g_figink() (below) then proves
    on the SAVED PIXELS that no ink lies outside what the census measured.
    """
    out = []
    seen = set()

    def _add(kind, a):
        if id(a) in seen:
            return
        seen.add(id(a))
        out.append((kind, a))

    chrome = {id(ax.patch)} | {id(sp) for sp in ax.spines.values()} | \
             {id(ax.xaxis), id(ax.yaxis)}
    for t in list(ax.texts):
        if not t.get_visible():
            continue
        if (t.get_text() or "").strip():
            _add("text", t)
        # v5.57 — an Annotation's arrow is ink even when its text is empty.
        ap = getattr(t, "arrow_patch", None)
        if ap is not None and ap.get_visible():
            _add("stroke", ap)
    for ln in list(ax.lines):
        if ln.get_visible():
            _add("stroke", ln)
    for p in list(ax.patches):
        if p.get_visible() and not getattr(p, "_fc_is_frame", False):
            _add("stroke", p)
    for c in list(ax.collections):
        if c.get_visible():
            _add("stroke", c)
    for im in list(ax.images):
        if im.get_visible():
            _add("stroke", im)
    # v5.57 — everything else a draw_fn can attach (ax.artists: AnnotationBbox,
    # OffsetImage, free Line2D/Text added via add_artist on older matplotlib;
    # tables; a legend). Chrome is excluded by identity, never by type.
    for a in list(getattr(ax, "artists", [])) + list(getattr(ax, "tables", [])):
        if a is not None and a.get_visible() and id(a) not in chrome \
                and not getattr(a, "_fc_is_frame", False):
            _add("stroke", a)
    lg = getattr(ax, "legend_", None)
    if lg is not None and lg.get_visible():
        _add("stroke", lg)
    return out


def _extent(a, rend):
    try:
        bb = a.get_window_extent(renderer=rend)
    except TypeError:
        bb = a.get_window_extent()
    except Exception:
        return None
    if bb is None or (bb.width <= 0 and bb.height <= 0):
        return None
    if bb.width <= 0 or bb.height <= 0:
        # v5.57 — a DEGENERATE box is still ink. A Patch's extent is its path,
        # with no stroke width added, so an axis-parallel bond drawn as a
        # FancyArrowPatch (the annotate idiom) reports zero height and was
        # rejected here outright — which is how the census lost it. Pad by
        # half the stroke width in pixels and keep it.
        from matplotlib.transforms import Bbox
        try:
            lw_pt = float(a.get_linewidth())
        except Exception:
            lw_pt = 1.0
        try:
            dpi = float(a.figure.dpi)
        except Exception:
            dpi = 100.0
        pad = max(lw_pt * dpi / 72.0 / 2.0, 0.5)
        bb = Bbox.from_extents(bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad)
    return bb


def _union_display_bbox(ax, rend):
    from matplotlib.transforms import Bbox
    boxes = []
    for _kind, a in _visible_artists(ax):
        bb = _extent(a, rend)
        if bb is not None:
            boxes.append(bb)
    if not boxes:
        return None
    return Bbox.union(boxes)


def _pad_bbox(bb, pad):
    from matplotlib.transforms import Bbox
    return Bbox.from_extents(bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad)


def _overlap_frac(b1, b2):
    """Intersection area / smaller area. 0.0 when disjoint."""
    ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0)
    iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
    if ix <= 0 or iy <= 0:
        return 0.0
    inter = ix * iy
    small = max(min(b1.width * b1.height, b2.width * b2.height), 1e-9)
    return float(inter / small)


def _move_text_display(t, dx, dy):
    """Translate a Text by (dx, dy) DISPLAY px through its own transform.

    Works for transData, transAxes or a blended transform without the caller
    needing to know which — the label stays in whatever space its author
    anchored it in, which is what keeps it attached to its atom when the data
    window is subsequently rescaled.
    """
    tr = t.get_transform()
    x, y = tr.transform(t.get_position())
    nx, ny = tr.inverted().transform((x + dx, y + dy))
    t.set_position((float(nx), float(ny)))


def _axes_display_box(ax, rend):
    return ax.get_window_extent(renderer=rend)


def content_data_window(ax, rend, pad_px=0.0):
    """Union of every artist's RENDERED extent, expressed in DATA coordinates.

    This is the measurement the engine did not previously take. A text's extent
    is font-metric dependent and cannot be derived from the data it annotates,
    which is precisely why an author-side rule ("place labels 0.18 units out")
    cannot guarantee fit and a renderer-side measurement can.
    """
    bb = _union_display_bbox(ax, rend)
    if bb is None:
        return None
    bb = _pad_bbox(bb, pad_px)
    inv = ax.transData.inverted()
    (x0, y0) = inv.transform((bb.x0, bb.y0))
    (x1, y1) = inv.transform((bb.x1, bb.y1))
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def apply_data_window(ax, win, box_aspect):
    """Set xlim/ylim to a window that CONTAINS win and matches the axes box
    aspect exactly, so an equal-aspect axes needs no further adjustment and
    matplotlib never silently re-expands a limit behind the fitter's back."""
    x0, y0, x1, y1 = win
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    hw = max((x1 - x0) / 2.0, 1e-9)
    hh = max((y1 - y0) / 2.0, 1e-9)
    # Grow the deficient axis so window aspect == axes box aspect.
    if hh / hw < box_aspect:
        hh = hw * box_aspect
    else:
        hw = hh / box_aspect
    ax.set_xlim(cx - hw, cx + hw)
    ax.set_ylim(cy - hh, cy + hh)
    return (cx - hw, cy - hh, cx + hw, cy + hh)


def _collisions(ax, rend, pad_px):
    """(count, worst_frac, [(text, dx, dy), ...]) for text-vs-text and
    text-vs-stroke overprints, with the push vector each text needs."""
    items = _visible_artists(ax)
    texts = [(a, _extent(a, rend)) for k, a in items if k == "text"]
    texts = [(a, b) for a, b in texts if b is not None]
    strokes = [(a, _extent(a, rend)) for k, a in items if k == "stroke"]
    strokes = [(a, b) for a, b in strokes if b is not None]

    push = {}
    worst = 0.0
    count = 0
    for i in range(len(texts)):
        ai, bi = texts[i]
        pi = _pad_bbox(bi, pad_px)
        for j in range(i + 1, len(texts)):
            aj, bj = texts[j]
            pj = _pad_bbox(bj, pad_px)
            f = _overlap_frac(pi, pj)
            if f <= 0.0:
                continue
            count += 1
            worst = max(worst, _overlap_frac(bi, bj))
            dx = (pi.x0 + pi.x1) / 2 - (pj.x0 + pj.x1) / 2
            dy = (pi.y0 + pi.y1) / 2 - (pj.y0 + pj.y1) / 2
            n = (dx * dx + dy * dy) ** 0.5 or 1.0
            # penetration depth along each axis, halved: both labels move.
            ox = (min(pi.x1, pj.x1) - max(pi.x0, pj.x0)) / 2.0
            oy = (min(pi.y1, pj.y1) - max(pi.y0, pj.y0)) / 2.0
            step = max(min(ox, oy), 1.0)
            ux, uy = dx / n, dy / n
            push[ai] = (push.get(ai, (0.0, 0.0))[0] + ux * step,
                        push.get(ai, (0.0, 0.0))[1] + uy * step)
            push[aj] = (push.get(aj, (0.0, 0.0))[0] - ux * step,
                        push.get(aj, (0.0, 0.0))[1] - uy * step)
    # A label sitting on a bond is legitimate ONLY when it masks it (white
    # bbox). Anything else is an overprint; push it clear of the stroke's
    # bounding box along the shorter escape.
    for ai, bi in texts:
        if _has_mask_bbox(ai):
            continue
        pi = _pad_bbox(bi, pad_px)
        for aj, bj in strokes:
            f = _overlap_frac(pi, bj)
            if f <= FIG_COLLIDE_TOL:
                continue
            count += 1
            worst = max(worst, f)
            ox = min(pi.x1, bj.x1) - max(pi.x0, bj.x0)
            oy = min(pi.y1, bj.y1) - max(pi.y0, bj.y0)
            if ox < oy:
                sgn = 1.0 if (pi.x0 + pi.x1) >= (bj.x0 + bj.x1) else -1.0
                d = (sgn * ox, 0.0)
            else:
                sgn = 1.0 if (pi.y0 + pi.y1) >= (bj.y0 + bj.y1) else -1.0
                d = (0.0, sgn * oy)
            push[ai] = (push.get(ai, (0.0, 0.0))[0] + d[0],
                        push.get(ai, (0.0, 0.0))[1] + d[1])
    return count, worst, push


def _has_mask_bbox(t):
    bb = t.get_bbox_patch()
    if bb is None:
        return False
    fc = bb.get_facecolor()
    try:
        return float(fc[3]) > 0.5
    except Exception:
        return True


def draw_frame(ax, lw=None):
    """The option/glyph border box. Drawn by the RENDERER, last, at the canvas
    edge, above every content artist. Never by draw_fn — a draw_fn-owned frame
    is what a later white-bbox label punched a hole through."""
    from matplotlib.patches import Rectangle
    r = Rectangle((0.0, 0.0), 1.0, 1.0, transform=ax.transAxes, fill=False,
                  lw=(lw or FIG_MIN_STROKE_PT), edgecolor="black",
                  zorder=10000, clip_on=False)
    r._fc_is_frame = True
    ax.add_patch(r)
    return r


def _expand_label_ring(ax, rend, factor):
    """ESCALATION. Move every label radially outward from the content centroid
    by `factor`, preserving relative geometry.

    Lateral repulsion cannot separate two labels that are nearly COLLINEAR with
    the figure centre — the eclipsed-Newman case, where front and rear
    substituents sit at the same angle by construction. Pushing them apart
    tangentially needs more travel than FIG_LABEL_MAX_SHIFT_IN allows, and
    raising that cap would let a label detach from the atom it names. Moving the
    whole ring outward increases the arc length between neighbours without
    changing which bond any label points down, so no label ever changes meaning.
    The window fitter then rescales, so the figure does not grow on the page.
    """
    texts = [a for k, a in _visible_artists(ax) if k == "text"]
    if not texts:
        return 0
    xs, ys = [], []
    for t in texts:
        bb = _extent(t, rend)
        if bb is None:
            continue
        xs.append((bb.x0 + bb.x1) / 2.0)
        ys.append((bb.y0 + bb.y1) / 2.0)
    if not xs:
        return 0
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    n = 0
    for t in texts:
        bb = _extent(t, rend)
        if bb is None:
            continue
        tx, ty = (bb.x0 + bb.x1) / 2.0, (bb.y0 + bb.y1) / 2.0
        _move_text_display(t, (tx - cx) * (factor - 1.0), (ty - cy) * (factor - 1.0))
        n += 1
    return n


def fit_and_deconflict(fig, ax, spec, *, window=None):
    """The safety net. Returns the fit record (also written into spec['fit']).

    ORDER MATTERS. Deconflict first would move labels against a window that is
    about to change; fit first would fit a layout that is about to move. The
    loop alternates and converges on both, and it STOPS on residual rather than
    forcing a label past FIG_LABEL_MAX_SHIFT_IN — a label dragged off its atom
    to satisfy a gate is a wrong figure that passes, which is the failure this
    whole block exists to end.
    """
    dpi = float(fig.get_dpi())
    clear_px = FIG_MIN_CLEARANCE_IN * dpi * float(spec.get("fit_scale_ref", 1.0))
    pad_px = FIG_LABEL_PAD_IN * dpi
    max_shift_px = FIG_LABEL_MAX_SHIFT_IN * dpi

    rend = _renderer(fig)
    abox = _axes_display_box(ax, rend)
    box_aspect = (abox.height / abox.width) if abox.width else 1.0

    shifted = {}
    passes = 0
    coll_before = None
    coll_now = 0
    worst = 0.0

    for passes in range(1, FIG_FIT_MAX_PASSES + 1):
        rend = _renderer(fig)
        # (1) FIT. Scale the data window by exactly the factor that makes the
        #     rendered content, plus 2x the clearance, fit the axes box. Text
        #     extents do NOT scale with the window (font size is in points), so
        #     this is not a similarity transform and one pass is not a proof —
        #     the loop re-measures. It converges in 2-4 passes on the reference
        #     chemistry set; FIG_FIT_MAX_PASSES bounds the pathological case.
        if window is not None:
            apply_data_window(ax, window, box_aspect)
        else:
            abox = _axes_display_box(ax, rend)
            ubb = _union_display_bbox(ax, rend)
            if ubb is None:
                break
            sx = (ubb.width + 2.0 * clear_px) / max(abox.width, 1e-9)
            sy = (ubb.height + 2.0 * clear_px) / max(abox.height, 1e-9)
            k = max(sx, sy)
            inv = ax.transData.inverted()
            (cx, cy) = inv.transform(((ubb.x0 + ubb.x1) / 2.0,
                                      (ubb.y0 + ubb.y1) / 2.0))
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            hw = abs(x1 - x0) / 2.0 * k
            hh = abs(y1 - y0) / 2.0 * k
            apply_data_window(ax, (cx - hw, cy - hh, cx + hw, cy + hh), box_aspect)
        # (2) DECONFLICT — measured label repulsion.
        rend = _renderer(fig)
        n, w, push = _collisions(ax, rend, pad_px)
        if coll_before is None:
            coll_before = n
        coll_now, worst = n, w
        moved_any = False
        for t, (dx, dy) in push.items():
            sxx, syy = shifted.get(t, (0.0, 0.0))
            nx, ny = sxx + dx, syy + dy
            if (nx * nx + ny * ny) ** 0.5 > max_shift_px:
                continue                      # residual — reported, not forced
            _move_text_display(t, dx, dy)
            shifted[t] = (nx, ny)
            moved_any = True
        # (3) CONVERGED? Both properties must hold on the SAME measurement, or
        #     the fitter reports what it achieved rather than what it attempted.
        rend = _renderer(fig)
        abox = _axes_display_box(ax, rend)
        ubb = _union_display_bbox(ax, rend)
        ok_clear = ubb is not None and min(
            ubb.x0 - abox.x0, ubb.y0 - abox.y0,
            abox.x1 - ubb.x1, abox.y1 - ubb.y1) >= clear_px - 0.5
        if ok_clear and not moved_any:
            break

    # ESCALATION (v5.55). Lateral repulsion has converged or given up. If
    # labels are still overprinted, expand the label ring in bounded steps and
    # re-run the lateral pass after each. Bounded and deterministic: three 10%
    # steps, then stop and REPORT. The gate voids the item rather than the
    # renderer inventing a layout nobody authored.
    ring = 1.0
    for _step in range(3):
        rend = _renderer(fig)
        n_now, _w, _p = _collisions(ax, rend, pad_px)
        if n_now == 0:
            break
        ring *= 1.10
        _expand_label_ring(ax, rend, 1.10)
        for _ in range(3):
            rend = _renderer(fig)
            abox = _axes_display_box(ax, rend)
            ubb = _union_display_bbox(ax, rend)
            if ubb is None:
                break
            sx = (ubb.width + 2.0 * clear_px) / max(abox.width, 1e-9)
            sy = (ubb.height + 2.0 * clear_px) / max(abox.height, 1e-9)
            k = max(sx, sy)
            inv = ax.transData.inverted()
            (cx, cy) = inv.transform(((ubb.x0 + ubb.x1) / 2.0,
                                      (ubb.y0 + ubb.y1) / 2.0))
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
            hw = abs(x1 - x0) / 2.0 * k
            hh = abs(y1 - y0) / 2.0 * k
            apply_data_window(ax, (cx - hw, cy - hh, cx + hw, cy + hh), box_aspect)
            if window is not None:
                apply_data_window(ax, window, box_aspect)
                break
            if abs(k - 1.0) < 0.005:
                break
        rend = _renderer(fig)
        _n, _w, push2 = _collisions(ax, rend, pad_px)
        for t, (dx, dy) in push2.items():
            sxx, syy = shifted.get(t, (0.0, 0.0))
            nx, ny = sxx + dx, syy + dy
            if (nx * nx + ny * ny) ** 0.5 > max_shift_px:
                continue
            _move_text_display(t, dx, dy)
            shifted[t] = (nx, ny)

    # Final measured truth, after the loop.
    rend = _renderer(fig)
    if window is not None:
        apply_data_window(ax, window, box_aspect)
        rend = _renderer(fig)
    coll_now, worst, _ = _collisions(ax, rend, pad_px)
    abox = _axes_display_box(ax, rend)
    ubb = _union_display_bbox(ax, rend)
    if ubb is not None:
        clear = min(ubb.x0 - abox.x0, ubb.y0 - abox.y0,
                    abox.x1 - ubb.x1, abox.y1 - ubb.y1)
        fill = (ubb.width * ubb.height) / max(abox.width * abox.height, 1e-9)
    else:
        clear, fill = 0.0, 0.0
    max_shift = max([(x * x + y * y) ** 0.5 for x, y in shifted.values()] or [0.0])

    rec = {
        "passes": passes,
        "clearance_in": round(float(clear) / dpi, 4),
        "clearance_floor_in": FIG_MIN_CLEARANCE_IN,
        "content_fill_frac": round(float(fill), 4),
        "collisions_before": int(coll_before or 0),
        "collisions_after": int(coll_now),
        "worst_overlap_frac": round(float(worst), 4),
        "collide_tol": FIG_COLLIDE_TOL,
        "label_shift_max_in": round(float(max_shift) / dpi, 4),
        "label_shift_cap_in": FIG_LABEL_MAX_SHIFT_IN,
        "box_aspect": round(float(box_aspect), 4),
        "ring_expansion": round(float(ring), 3),
        "engine": "fit_and_deconflict/v5.57",
    }
    rec["status"] = ("OK" if (clear >= clear_px * 0.999
                              and coll_now == 0) else "RESIDUAL")
    # v5.57 — the census box and the axes box in SAVED-PIXEL coordinates
    # (origin top-left, FIGURAL_DPI), so g_figink() can compare what the
    # fitter MEASURED against where ink actually LANDED without re-deriving
    # any extent from pixels. Saved px = display px * (FIGURAL_DPI / fig.dpi).
    try:
        k = float(FIGURAL_DPI) / dpi
        fh = float(fig.get_figheight()) * dpi
        def _px(bb):
            return [round(bb.x0 * k, 1), round((fh - bb.y1) * k, 1),
                    round(bb.x1 * k, 1), round((fh - bb.y0) * k, 1)]
        rec["content_bbox_px"] = _px(ubb) if ubb is not None else None
        rec["axes_bbox_px"] = _px(abox)
        rec["axis_on"] = bool(getattr(ax, "axison", True))
    except Exception:
        rec["content_bbox_px"] = None
        rec["axes_bbox_px"] = None
        rec["axis_on"] = True
    # v5.61 (GAP-2026-08-22-FIGASPECT-SELF-FULFILLING) — the RAW ink extent in
    # DATA coordinates, BEFORE any window inflation to the canvas aspect. This
    # is the only extent from which a canvas aspect can honestly be derived:
    # data_window has already been grown by apply_data_window() to match the
    # axes box, so its shape always "confirms" whatever canvas it was rendered
    # on. render_option_set() v5.60 derived the set aspect from the UNION of
    # data_windows — a self-fulfilling loop that locked square molecule sets
    # into the 0.72 landscape default forever (measured: hexagon option set,
    # true content aspect ~1.0, derived 0.69, set fill 41% < the 45% floor,
    # G-FIGFIT BLOCKING on a correct drawing).
    try:
        _cw = content_data_window(ax, rend)
        rec["content_window"] = ([round(float(v), 6) for v in _cw]
                                 if _cw is not None else None)
    except Exception:
        rec["content_window"] = None
    # v5.61 — the STROKE window: the same union, Text artists excluded. A text
    # extent in data coordinates scales with the zoom (font size is in points),
    # so a content_window measured on one canvas over-reports the aspect a
    # label-heavy figure would have on another. Stroke geometry is pure data —
    # zoom-invariant — which makes it the one honest source for a canvas-shape
    # decision. None when the figure is all text; the aspect derivation then
    # falls back to content_window.
    try:
        # _visible_artists yields (kind, artist); the census already classifies
        # text vs stroke ink, so the exclusion uses its tag, not isinstance.
        _bbs = [_extent(a, rend) for kind, a in _visible_artists(ax)
                if kind != "text"]
        _bbs = [b for b in _bbs if b is not None]
        if _bbs:
            from matplotlib.transforms import Bbox as _Bbox
            _u = _Bbox.union(_bbs)
            inv = ax.transData.inverted()
            (_x0, _y0) = inv.transform((_u.x0, _u.y0))
            (_x1, _y1) = inv.transform((_u.x1, _u.y1))
            rec["stroke_window"] = [round(float(min(_x0, _x1)), 6),
                                    round(float(min(_y0, _y1)), 6),
                                    round(float(max(_x0, _x1)), 6),
                                    round(float(max(_y0, _y1)), 6)]
        else:
            rec["stroke_window"] = None
    except Exception:
        rec["stroke_window"] = None
    spec["fit"] = rec
    return rec


# =============================================================================
# GATES — all DETERMINISTIC, all legal inside an audit's python
# =============================================================================
def g_figdegen(spec, png_path):
    """Catches the one failure arithmetic cannot see: a figure whose plot area
    collapsed, so the PNG is the right size and the fonts the right points but
    there is nothing legible inside."""
    np = _try_import("numpy")
    Image = _try_import("PIL.Image")
    if np is None or Image is None:
        return ["G-FIGDEGEN: DORMANT — numpy/Pillow unavailable, plot-area "
                "collapse unverifiable. " + PIP_INSTALL]
    a = np.array(Image.open(png_path).convert("L"))
    ink = (a < 160)
    rows = np.where(ink.any(1))[0]
    cols = np.where(ink.any(0))[0]
    if len(rows) < 2 or len(cols) < 2:
        return ["G-FIGDEGEN: figure contains no ink."]
    frac = ((rows[-1] - rows[0]) * (cols[-1] - cols[0])) / float(a.size)
    if frac < MIN_PLOT_AREA_FRAC:
        return [f"G-FIGDEGEN: drawn area is {frac:.1%} of the canvas "
                f"(floor {MIN_PLOT_AREA_FRAC:.0%}); the plot area has collapsed."]
    return []


def g_figdpi(spec, png_path):
    Image = _try_import("PIL.Image")
    if Image is None:
        return ["G-FIGDPI: DORMANT — Pillow unavailable, DPI unverifiable. "
                + PIP_INSTALL]
    d = Image.open(png_path).info.get("dpi")
    if not d or not d[0]:
        return ["G-FIGDPI: PNG carries no DPI metadata; native size is undefined. "
                "Never assume 300."]
    return []


def g_figscale(spec, png_path=None):
    """S must be 1.0, or exactly the column cap when the figure is capped."""
    s = spec.get("placement_scale")
    if s is None:
        return ["G-FIGSCALE: placement_scale not recorded; renderer did not read "
                "back the saved artefact."]
    d = float(spec.get("display_in") or 0) or None
    if d is None:
        return []
    expected = min(1.0, FIG_COLUMN_IN / d) if d > FIG_COLUMN_IN else 1.0
    if abs(s - expected) > 0.02:
        return [f"G-FIGSCALE: placement scale {s:.3f}, expected {expected:.3f}. "
                f"Labels land at {s:.2f}x their requested size."]
    return []


def g_figlabel(spec):
    """HARD, arithmetic. On-page pt == requested pt x S, both recorded."""
    f = spec.get("font_pt_native")
    s = spec.get("placement_scale")
    if not f or s is None:
        return ["G-FIGLABEL: font metrics or placement scale not recorded."]
    floor = _floor_of(spec)
    onpage = f["small"] * s
    if onpage < floor - 1e-6:
        return [f"G-FIGLABEL: smallest label lands at {onpage:.2f} pt on page "
                f"(floor {floor} pt for class {_class_of(spec)}); scale {s:.2f}x."]
    return []


def g_figlabel_pixels(spec, png_path):
    """WARN only. Biased against superscripts/subscripts — see docstring."""
    np = _try_import("numpy")
    Image = _try_import("PIL.Image")
    _sp = _try_import("scipy.ndimage")
    if np is None or Image is None or _sp is None:
        return []          # advisory only — dormancy here is not worth a finding
    ndimage = _sp
    a = np.array(Image.open(png_path).convert("RGBA"))
    vis = a[..., 3] > 16
    rgb = a[..., :3].astype(int)
    dark = (rgb.max(2) < 160) & vis
    lab, _ = ndimage.label(dark)
    hs = []
    for sl in ndimage.find_objects(lab):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if 5 <= h <= 90 and 2 <= w <= 90 and w / h < 5:
            hs.append(h)
    if len(hs) < 6:
        return []
    dpi = spec.get("png_dpi") or FIGURAL_DPI
    s = spec.get("placement_scale") or 1.0
    onpage = float(np.median(hs)) / dpi * 72 / 0.70 * s
    floor = _floor_of(spec)
    if onpage < floor * 0.75:
        return [f"W-FIGLABELPX: pixel estimate {onpage:.1f} pt vs floor {floor} pt. "
                f"ADVISORY — this statistic under-reads figures containing "
                f"superscripts or subscripts. Check g_figlabel first."]
    return []


def g_figcolour(spec, png_path):
    if _class_of(spec) not in COLOUR_REQUIRED:
        return []
    frac = coloured_fraction(png_path)
    hues = dominant_hues(png_path)
    if frac is None or hues is None:
        return ["G-FIGCOLOUR: DORMANT — numpy/Pillow unavailable, colour "
                "presence unverifiable. " + PIP_INSTALL]
    out = []
    if frac < 0.005:
        out.append(f"G-FIGCOLOUR: {frac:.3%} coloured pixels (need >=0.5%) on a "
                   f"{_class_of(spec)} figure.")
    declared = len(spec.get("series") or [])
    if declared >= 2 and len(hues) < 2:
        out.append(f"G-FIGCOLOUR: {len(hues)} dominant hue(s) in the PNG but "
                   f"{declared} series declared.")
    return out


def g_figaccent(spec, png_path):
    """v5.46 (GAP-2026-08-07-FIGACCENT). Accent presence for data_single and
    schematic — the S10-6A palette column made normative and enforceable.

    Fires when a class in ACCENT_REQUIRED renders with fewer than
    ACCENT_MIN_FRAC coloured pixels, i.e. the draw_fn ignored the palette and
    drew everything in black (the pre-v5.33 "solid black" habit, RC-1).
    AMBER by construction — a fire-0-times history does not exist yet for this
    gate, so it must NOT start BLOCKING (regression-detector doctrine, and the
    owner directive that no image-COLOUR condition may ever halt a run).
    Deliberately reads coloured_fraction() only, never dominant_hues(): the
    hue detector's minimum-area cut swallows small accents. EC-V18 safe:
    a legacy spec has no class, _class_of() returns "unknown", the gate is
    silent for the ~200 pre-v5.33 exams.
    """
    if _class_of(spec) not in ACCENT_REQUIRED:
        return []
    frac = coloured_fraction(png_path)
    if frac is None:
        return ["G-FIGACCENT: DORMANT — numpy/Pillow unavailable, accent "
                "presence unverifiable. " + PIP_INSTALL]
    if frac < ACCENT_MIN_FRAC:
        return [f"G-FIGACCENT: {frac:.4%} coloured pixels (floor "
                f"{ACCENT_MIN_FRAC:.2%}) on a {_class_of(spec)} figure. "
                f"Q7b.8: the interrogated item (schematic) or the series ink "
                f"(data_single) MUST carry an Okabe-Ito accent; the draw_fn "
                f"must take its accent ink from the palette argument, never "
                f"hardcode black."]
    return []


def g_figmono(spec, png_path):
    """Colour in an abstract-reasoning item can leak the answer."""
    if _class_of(spec) not in MONO_REQUIRED:
        return []
    allowed = {s.get("colour", "").lower() for s in (spec.get("series") or [])
               if s.get("accent_marker")}
    frac = coloured_fraction(png_path)
    if frac is None:
        return ["G-FIGMONO: DORMANT — numpy/Pillow unavailable, monochrome "
                "contract unverifiable. " + PIP_INSTALL]
    if frac > 0.02 and not allowed:
        return [f"G-FIGMONO: {frac:.2%} coloured pixels in a reasoning_glyph. "
                f"Colour may leak the answer; only a declared missing-element "
                f"accent is permitted."]
    return []


def g_figseries(spec):
    """Colour must never be the sole carrier of meaning."""
    ser = spec.get("series") or []
    if len(ser) < 2:
        return []
    out = []
    for i in range(len(ser)):
        for j in range(i + 1, len(ser)):
            a, b = ser[i], ser[j]
            same_ls = a.get("linestyle") == b.get("linestyle")
            same_mk = a.get("marker") == b.get("marker")
            if same_ls and same_mk:
                out.append(
                    f"G-FIGSERIES: series {a.get('id')} and {b.get('id')} differ "
                    f"only in colour. Add a distinct linestyle, marker or hatch.")
    return out


def _hex_rgb(h):
    h = (h or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def g_figcvd(spec, png_path=None):
    """Gates the DECLARED series colours, never extracted pixels.

    Extracted hues carry quantisation and antialiasing error: the declared
    Okabe-Ito blue (0,114,178) and bluish-green (0,158,115) separate by 60.6,
    which clears DEUT_MIN_SEP — but quantised onto a 32-step cube they become
    (0,96,160) and (0,128,96), separating by 57, and the gate fired on its own
    mandated palette. That is measurement error being reported as a defect.

    Gating the declaration makes this exact and fully reproducible, which also
    closes VERIFY §9: the same figures measured by two pixel methods gave 48 %
    and 70 % collapse rates, and a HARD gate cannot rest on an unstated method.
    Whether the RENDER honoured the declaration is a different question, and
    G-FIGCOLOUR already answers it by comparing hue COUNT.

    Note the calibration: Okabe-Ito's tightest pair sits at 60.6 against a
    threshold of 60.0. The threshold is set to just admit the mandated palette,
    so it is meaningful only for an exam_config.figure_palette override.
    """
    ser = [s for s in spec.get("series", []) if not s.get("accent_marker")]
    cols = [(s.get("id", "?"), _hex_rgb(s.get("colour"))) for s in ser]
    cols = [(i, c) for i, c in cols if c]
    out = []
    for x in range(len(cols)):
        for y in range(x + 1, len(cols)):
            (ia, a), (ib, b) = cols[x], cols[y]
            if a == b:
                out.append(f"G-FIGCVD: series {ia} and {ib} declare the same colour "
                           f"{a}; they are indistinguishable.")
                continue
            da, db = _deuteranope(a), _deuteranope(b)
            sep = sum(abs(u - v) for u, v in zip(da, db))
            if sep < DEUT_MIN_SEP:
                out.append(f"G-FIGCVD: declared colours for series {ia} {a} and "
                           f"{ib} {b} collapse for a deuteranope "
                           f"(sep {sep:.0f} < {DEUT_MIN_SEP:.0f}).")
    return out


def g_figalt(descr):
    """WARN. Alt text present and non-empty."""
    if not (descr or "").strip():
        return ["G-FIGALT: drawing carries no wp:docPr/@descr alt text."]
    return []


def g_figoptunif(specs, png_paths):
    """All option canvases in a set share size and style budget."""
    Image = _try_import("PIL.Image")
    if Image is None:
        return ["G-FIGOPTUNIF: DORMANT — Pillow unavailable, canvas sizes "
                "unverifiable. " + PIP_INSTALL]
    sizes = {Image.open(p).size for p in png_paths}
    out = []
    if len(sizes) != 1:
        out.append(f"G-FIGOPTUNIF: option canvases not uniform: {sorted(sizes)}. "
                   f"A size difference is an answer cue.")
    placed = {round(float(s.get("display_in") or 0), 4) for s in specs}
    if len(placed) != 1:
        out.append(f"G-FIGOPTUNIF: option canvases placed at differing widths: "
                   f"{sorted(placed)}.")
    return out


def g_figglyph(spec, png_path=None):
    """Tofu detection. Any glyph the figure font cannot render is a HARD fail."""
    _fm = _try_import("matplotlib.font_manager")
    _ft = _try_import("fontTools.ttLib")
    if _fm is None or _ft is None:
        return []          # tofu detection is best-effort; absence is not a defect
    findfont, FontProperties = _fm.findfont, _fm.FontProperties
    TTFont = _ft.TTFont
    texts = []
    for k in ("x", "y"):
        a = (spec.get("axes") or {}).get(k) or {}
        texts += [a.get("title") or "", a.get("units") or ""]
    texts += [s.get("label", "") for s in (spec.get("series") or [])]
    need = {ch for t in texts for ch in t if ord(ch) > 127}
    if not need:
        return []
    try:
        font = TTFont(findfont(FontProperties()), fontNumber=0)
        cmap = set()
        for table in font["cmap"].tables:
            cmap |= set(table.cmap)
    except Exception:
        return []
    missing = sorted(ch for ch in need if ord(ch) not in cmap)
    if missing:
        return [f"G-FIGGLYPH: figure font cannot render {missing}; these render "
                f"as tofu boxes."]
    return []


def g_figfit(spec):
    """HARD, arithmetic (Q10). Did the ink land inside the frame?

    Reads the fit record the renderer wrote. It is NOT a pixel gate, for the
    same reason G-FIGLABEL is not: the renderer already holds the exact
    rendered extents, and re-deriving them from pixels re-introduces the
    superscript/subscript bias Q9.6 documents. figural_core.g_figfit_pixels()
    is the WARN-level cross-check.
    """
    f = spec.get("fit")
    if f is None:
        if is_legacy(spec):
            return []                      # EC-V18 — pre-v5.55 output is silent
        return ["G-FIGFIT: no fit record; renderer did not run "
                "fit_and_deconflict(). Every label position is unverified."]
    c = float(f.get("clearance_in", -1.0))
    floor = float(f.get("clearance_floor_in", FIG_MIN_CLEARANCE_IN))
    out = []
    if c < 0:
        out.append(f"G-FIGFIT: ink lies OUTSIDE the frame by "
                   f"{abs(c):.3f} in — the frame cuts through the drawing.")
    elif c + 1e-6 < floor:
        out.append(f"G-FIGFIT: ink-to-frame clearance {c:.3f} in is below the "
                   f"{floor:.3f} in floor; the drawing touches its own border.")
    # For a shared-window option SET the per-option fill is legitimately below
    # the floor — the window is the UNION, so only the largest option fills it.
    # The floor is therefore evaluated on the SET. Gating it per option would
    # fire on every correctly-uniform option set, which is how a fill gate ends
    # up disabled and the waste ships anyway.
    fill = float(f.get("set_fill_frac") if f.get("window_shared")
                 else f.get("content_fill_frac", 0.0))
    if fill and fill < MIN_CONTENT_FILL_FRAC:
        out.append(f"G-FIGFIT: content fills {fill:.1%} of the canvas "
                   f"(floor {MIN_CONTENT_FILL_FRAC:.0%}); the figure is mostly "
                   f"white space and is being displayed far smaller than its "
                   f"page allocation.")
    return out


def g_figcollide(spec):
    """VOID_ITEM (Q11). Two labels overprinted, or a label over a stroke it does
    not mask. An option a candidate cannot read is not a degraded option, it is
    an unanswerable one — so the ITEM is void and regenerated. The RUN never
    halts (CLAUDE.md: silence is the defect; a halt is not the remedy)."""
    f = spec.get("fit")
    if f is None:
        return [] if is_legacy(spec) else [
            "G-FIGCOLLIDE: no fit record; label overprints unverifiable."]
    n = int(f.get("collisions_after", 0))
    if n == 0:
        return []
    return [f"G-FIGCOLLIDE: {n} unresolved label overprint(s); worst overlap "
            f"{float(f.get('worst_overlap_frac', 0.0)):.1%} of the smaller "
            f"label box (tolerance {float(f.get('collide_tol', FIG_COLLIDE_TOL)):.1%}). "
            f"Labels were nudged up to {float(f.get('label_shift_max_in', 0.0)):.3f} in "
            f"(cap {float(f.get('label_shift_cap_in', FIG_LABEL_MAX_SHIFT_IN)):.3f} in) "
            f"and could not be separated: redraw this figure with fewer or "
            f"shorter labels, or a larger display width."]


def g_figfit_pixels(spec, png_path):
    """WARN cross-check on the SAVED artefact: ink outside the drawn frame.

    Kept advisory for the Q9.6 reason — it is a pixel statistic and inherits
    every pixel statistic's bias — but it is the check that reproduces the
    shipped defect from the delivered file alone, with no sidecar, which is
    what makes ~200 legacy exams auditable without re-rendering them.
    """
    np = _try_import("numpy")
    Image = _try_import("PIL.Image")
    if np is None or Image is None:
        return ["W-FIGFITPX: DORMANT — numpy/Pillow unavailable. " + PIP_INSTALL]
    a = np.array(Image.open(png_path).convert("L")).astype(int)
    ink = a < 160
    if not ink.any():
        return []
    rowfrac = ink.mean(1)
    colfrac = ink.mean(0)
    brows = np.where(rowfrac > 0.6)[0]
    bcols = np.where(colfrac > 0.6)[0]
    if len(brows) < 2 or len(bcols) < 2:
        return []                       # no frame drawn — nothing to be outside
    t, b = int(brows.min()), int(brows.max())
    l, r = int(bcols.min()), int(bcols.max())
    out = ink.copy()
    out[max(t - 2, 0):b + 3, max(l - 2, 0):r + 3] = False
    n_out = int(out.sum())
    if n_out == 0:
        return []
    return [f"W-FIGFITPX: {n_out} px ({n_out / float(ink.sum()):.2%} of the ink) "
            f"lies outside the drawn frame in {os.path.basename(png_path)}."]


FIG_INK_TOL_PX = 4          # anti-aliasing + stroke-cap allowance, saved px
FIG_INK_EDGE_FRAC = 0.03    # frame detection: only within this band of an edge


def _ink_mask_and_frame(a, np):
    """Ink mask (L < 160) with any RENDERER FRAME removed. The frame is the
    near-solid rows/cols lying within FIG_INK_EDGE_FRAC of a canvas edge —
    restricted to the edge band so a long horizontal bond or a ring edge in
    the interior is never mistaken for a frame (W-FIGFITPX's looser rule did
    exactly that on a benzene ring)."""
    ink = a < 160
    h, w = ink.shape
    bh, bw = max(2, int(h * FIG_INK_EDGE_FRAC)), max(2, int(w * FIG_INK_EDGE_FRAC))
    rowfrac = ink.mean(1); colfrac = ink.mean(0)
    frame_rows = [r for r in range(h) if rowfrac[r] > 0.6 and (r < bh or r >= h - bh)]
    frame_cols = [c for c in range(w) if colfrac[c] > 0.6 and (c < bw or c >= w - bw)]
    content = ink.copy()

    def _grow(idx, frac, n):
        # Strip the frame line AND its anti-aliased tail: walk outward from
        # each frame row/col while the ink fraction stays above 15%.
        out = set()
        for i in idx:
            out.add(i)
            j = i - 1
            while j >= 0 and frac[j] > 0.15:
                out.add(j); j -= 1
            j = i + 1
            while j < n and frac[j] > 0.15:
                out.add(j); j += 1
        return out

    for r in _grow(frame_rows, rowfrac, h):
        content[max(r - 1, 0):r + 2, :] = False
    for c in _grow(frame_cols, colfrac, w):
        content[:, max(c - 1, 0):c + 2] = False
    return ink, content, bool(frame_rows or frame_cols)


def g_figink(spec, png_path):
    """HARD (v5.57, GAP-2026-08-20-FIGURAL-INK-CENSUS). Does every inked pixel
    lie inside the box the fitter MEASURED?

    G-FIGFIT is arithmetic over the fit record and is correct whenever its
    INPUT — the artist census — is complete. It cannot detect an incomplete
    census: ink the census never saw is ink the record never mentions, and the
    record says OK. This gate closes that by comparing the census box written
    at render time (fit.content_bbox_px) against the ink actually present in
    the saved PNG. It is NOT a pixel re-derivation of clearance (the Q9.6
    objection): the only question asked is "is there ink OUTSIDE the measured
    box?", and the superscript/subscript extent bias only ever makes the census
    box LARGER than the ink, so it can never produce a false positive here.
    Legacy output (no content_bbox_px) is silent, as every v5.57+ gate is for
    pre-v5.57 renders (EC-V18)."""
    np = _try_import("numpy")
    Image = _try_import("PIL.Image")
    if np is None or Image is None:
        return ["G-FIGINK: DORMANT — numpy/Pillow unavailable. " + PIP_INSTALL]
    f = (spec or {}).get("fit") or {}
    box = f.get("content_bbox_px")
    try:
        a = np.array(Image.open(png_path).convert("L")).astype(int)
    except Exception as e:
        return [f"G-FIGINK: DORMANT — cannot read {os.path.basename(png_path)}: {e}"]
    ink, content, _framed = _ink_mask_and_frame(a, np)
    if not content.any():
        return []
    h, w = content.shape
    if not box:
        # LEGACY (pre-v5.57 render, no census box). The edge form of the same
        # check works on a FRAMED canvas alone: there the axes box IS the
        # canvas, the v5.55 fitter guaranteed the census box cleared it by
        # FIG_MIN_CLEARANCE_IN on every side, so content ink inside that band
        # is ink the census never saw. AMBER (W-FIGINK), the EC-V18 posture,
        # and it is what makes the ~200 delivered exams auditable for this
        # defect without re-rendering: on the reference paper it flagged five
        # option canvases whose horizontal substituent bond ran into the frame.
        if not _framed:
            return []
        rows = np.where(content.any(1))[0]; cols = np.where(content.any(0))[0]
        dpi = float((spec or {}).get("png_dpi") or FIGURAL_DPI)
        band = int(FIG_MIN_CLEARANCE_IN * dpi) - FIG_INK_TOL_PX
        margin = int(min(cols.min(), rows.min(), w - 1 - cols.max(), h - 1 - rows.max()))
        if margin >= band:
            return []
        side = ["left", "top", "right", "bottom"][int(np.argmin(
            [cols.min(), rows.min(), w - 1 - cols.max(), h - 1 - rows.max()]))]
        return [f"W-FIGINK: content ink lies {margin} px from the {side} frame "
                f"(clearance floor {band + FIG_INK_TOL_PX} px) in "
                f"{os.path.basename(png_path)} — a pre-v5.57 render whose census "
                f"missed a stroke (typically an axis-parallel bond drawn as an "
                f"annotation arrow); the stroke is clipped at the frame. "
                f"Re-render under v5.57."]
    # The census measures CONTENT, never chrome (ticks, tick labels, axis
    # titles, spines live outside or on the axes box by design — G-FIGFIT's
    # own docstring). So the comparison is confined to the axes-box INTERIOR.
    # On an axis-OFF render (every schematic / option / glyph, the class that
    # shipped Q44) no chrome can exist inside it and the gate is HARD. On an
    # axis-ON render gridlines and minor ticks may legitimately sit inside, so
    # the spine band is excluded and the finding is AMBER (W-FIGINK).
    axis_on = bool(f.get("axis_on", True))
    abox = f.get("axes_bbox_px")
    if abox:
        ax0, ay0, ax1, ay1 = abox
        shrink = 3 if axis_on else 0
        keep = np.zeros_like(content)
        keep[max(int(ay0) + shrink, 0):min(int(ay1) - shrink + 1, h),
             max(int(ax0) + shrink, 0):min(int(ax1) - shrink + 1, w)] = True
        content = content & keep
        if not content.any():
            return []
    gid = "W-FIGINK" if axis_on else "G-FIGINK"
    x0, y0, x1, y1 = box
    t = FIG_INK_TOL_PX
    lo_x, lo_y = max(int(x0 - t), 0), max(int(y0 - t), 0)
    hi_x, hi_y = min(int(x1 + t) + 1, w), min(int(y1 + t) + 1, h)
    outside = content.copy()
    outside[lo_y:hi_y, lo_x:hi_x] = False
    n_out = int(outside.sum())
    if n_out == 0:
        return []
    rows = np.where(outside.any(1))[0]; cols = np.where(outside.any(0))[0]
    sides = []
    if cols.max() >= hi_x: sides.append("right")
    if cols.min() < lo_x: sides.append("left")
    if rows.min() < lo_y: sides.append("top")
    if rows.max() >= hi_y: sides.append("bottom")
    return [f"{gid}: {n_out} px of ink ({n_out / float(content.sum()):.1%}) lie "
            f"OUTSIDE the content box the fitter measured "
            f"({', '.join(sides) or 'interior'}) in {os.path.basename(png_path)} — "
            f"the artist census missed a render path (an Annotation arrow, an "
            f"add_artist() child, a table or legend); the fitter windowed that "
            f"ink out and may have CLIPPED it at the frame."]


def g_figoptwindow(specs):
    """VOID_ITEM. Every option of a question must be drawn in the SAME data
    window on the SAME canvas.

    This is a correctness gate, not a tidiness one. When each option is fitted
    independently, a small molecule is magnified to fill its box and a large one
    is shrunk — so relative size, which in a structure question is MEANING,
    becomes an artefact of the renderer, and any option drawn at a visibly
    different scale is an answer cue. Q7b.6 already forbids a differing style
    budget; this closes the same hole on geometry.
    """
    if len(specs) < 2:
        return []
    wins = []
    canv = set()
    for s in specs:
        f = s.get("fit") or {}
        w = f.get("data_window")
        if w is None:
            if is_legacy(s):
                return []
            return ["G-FIGOPTWINDOW: option set has no recorded data window; "
                    "options were fitted independently."]
        wins.append([round(float(v), 6) for v in w])
        canv.add(tuple(s.get("png_px") or ()))
    if len({tuple(w) for w in wins}) != 1:
        return [f"G-FIGOPTWINDOW: options were drawn in {len({tuple(w) for w in wins})} "
                f"different data windows; relative size is not comparable across "
                f"the option set and scale differences read as an answer cue."]
    if len(canv) != 1:
        return [f"G-FIGOPTWINDOW: option canvases differ: {sorted(canv)}."]
    return []


def render_option_set(draw_fns, out_paths, specs, palette=None):
    """Render a question's WHOLE option set in ONE shared, fitted window.

    Two passes by necessity: the common window cannot be known until every
    option has been drawn and measured once. Pass 1 fits each option alone and
    records its content window; pass 2 re-renders all of them in the UNION of
    those windows, so every option shares one canvas, one scale and one frame.

    This is the API S10-8 must call for figural options. render_figure() on its
    own is correct for a problem figure and INSUFFICIENT for an option set,
    because a per-option fit is exactly what makes the scales diverge.
    """
    if not (len(draw_fns) == len(out_paths) == len(specs)):
        raise FiguralError("G-FIGOPTWINDOW: draw_fns, out_paths and specs must "
                           "be the same length (one entry per option).")
    if len(specs) < 2:
        raise FiguralError("G-FIGOPTWINDOW: an option set needs >=2 options.")
    wins, cwins = [], []
    for fn, p, s in zip(draw_fns, out_paths, specs):
        render_figure(fn, p, s, palette=palette)
        f = s.get("fit") or {}
        if f.get("data_window"):
            wins.append(f["data_window"])
        if f.get("content_window"):
            cwins.append(f["content_window"])
    if not wins:
        return specs
    # v5.61 (GAP-2026-08-22-FIGASPECT-SELF-FULFILLING). The canvas ASPECT comes
    # from the CONTENT extent, never from the fitted window. v5.55-v5.60 derived
    # it from the union of pass-1 data_windows — but apply_data_window() has
    # already inflated every one of those to the canvas aspect pass 1 rendered
    # on, so the "derivation" returned the default it started from: a square
    # molecule set stayed in a 0.72 landscape canvas, filled 41% of it, and
    # G-FIGFIT correctly BLOCKED a correct drawing. content_window is the raw
    # ink extent in data coordinates and carries no such imprint. Precedence:
    #   1. A canvas_aspect declared identically on EVERY spec of the set is the
    #      author's decision and is honoured EXACTLY — v5.60 silently clobbered
    #      it with the circular derivation, which disabled the documented
    #      workaround precisely where it was needed.
    #   2. Otherwise the aspect is derived from the union of content_windows,
    #      clamped to the [FIG_CANVAS_ASPECT_MIN, FIG_CANVAS_ASPECT_MAX] band.
    #   3. A set with no content_window at all (defensive; empty draws) keeps
    #      the v5.60 window-union derivation rather than crashing.
    # One aspect for the whole SET, so uniformity (Q4 / G-FIGOPTUNIF) is
    # preserved by construction — unchanged.
    swins = [f2 for f2 in
             ((s.get("fit") or {}).get("stroke_window") for s in specs) if f2]
    _decl = {s.get("canvas_aspect") for s in specs}
    if len(_decl) == 1 and None not in _decl:
        asp = float(_decl.pop())
    else:
        # Stroke union first: zoom-invariant pure geometry, so a square ring is
        # a square whatever canvas pass 1 happened to render on. Content union
        # (labels included) only when the set draws no strokes at all; window
        # union only in the degenerate no-measurement case.
        src = swins or cwins or wins
        cu = (min(w[0] for w in src), min(w[1] for w in src),
              max(w[2] for w in src), max(w[3] for w in src))
        cw = max(cu[2] - cu[0], 1e-9)
        ch = max(cu[3] - cu[1], 1e-9)
        asp = max(FIG_CANVAS_ASPECT_MIN, min(FIG_CANVAS_ASPECT_MAX, ch / cw))
    for s in specs:
        s["canvas_aspect"] = round(float(asp), 4)
    # Pass 2 seeds from the CONTENT union too: seeding from the pass-1 window
    # union would re-import the pass-1 canvas shape through the back door. The
    # clearance-deficit loop below grows it to the 0.05 in floor as before.
    if cwins:
        common = (min(w[0] for w in cwins), min(w[1] for w in cwins),
                  max(w[2] for w in cwins), max(w[3] for w in cwins))
    else:
        common = (min(w[0] for w in wins), min(w[1] for w in wins),
                  max(w[2] for w in wins), max(w[3] for w in wins))
    # Pass 2, with a bounded re-expansion. A shared window is applied AS GIVEN,
    # so an option whose labels moved during its own deconflict pass can still
    # sit closer to the frame than the floor. The window is then grown for ALL
    # options by the single worst factor — never per option, because a per-option
    # correction is exactly the scale divergence G-FIGOPTWINDOW exists to stop.
    for _ in range(6):
        for fn, p, s in zip(draw_fns, out_paths, specs):
            render_figure(fn, p, s, palette=palette, window=common)
        deficit = 0.0
        for s in specs:
            f = s.get("fit") or {}
            c = float(f.get("clearance_in", FIG_MIN_CLEARANCE_IN))
            deficit = max(deficit, FIG_MIN_CLEARANCE_IN - c)
        if deficit <= 1e-4:
            break
        # grow the window so the worst option gains `deficit` inches on each side
        w = common[2] - common[0]
        h = common[3] - common[1]
        gx = max(deficit / max(float(specs[0]["display_in"]), 1e-9) * w * 3.0,
                 0.004 * w)
        gy = gx * (h / max(w, 1e-9))
        common = (common[0] - gx, common[1] - gy, common[2] + gx, common[3] + gy)
    set_fill = max([float((s.get("fit") or {}).get("content_fill_frac", 0.0))
                    for s in specs] or [0.0])
    for s in specs:
        if s.get("fit"):
            s["fit"]["window_shared"] = True
            s["fit"]["set_fill_frac"] = round(set_fill, 4)
            s["fit"]["status"] = ("OK" if (s["fit"]["clearance_in"] + 1e-4
                                           >= FIG_MIN_CLEARANCE_IN
                                           and s["fit"]["collisions_after"] == 0)
                                  else "RESIDUAL")
    return specs


def audit_figure(spec, png_path, descr=None):
    """Run every gate. Returns (hard_failures, warnings)."""
    hard = []
    hard += g_figdpi(spec, png_path)
    hard += g_figdegen(spec, png_path)
    hard += g_figscale(spec, png_path)
    hard += g_figlabel(spec)
    hard += g_figfit(spec)                 # v5.55 Q10 — ink inside the frame
    _ink = g_figink(spec, png_path)        # v5.57 — census == pixels
    hard += [x for x in _ink if x.startswith("G-FIGINK") and "DORMANT" not in x]
    hard += g_figcollide(spec)             # v5.55 Q11 — no overprinted labels
    hard += g_figcolour(spec, png_path)
    hard += g_figaccent(spec, png_path)
    hard += g_figmono(spec, png_path)
    hard += g_figseries(spec)
    hard += g_figcvd(spec, png_path)
    hard += g_figglyph(spec, png_path)
    warn = []
    warn += g_figlabel_pixels(spec, png_path)
    warn += [x for x in _ink if not (x.startswith("G-FIGINK") and "DORMANT" not in x)]
    warn += g_figfit_pixels(spec, png_path)   # v5.55 — legacy-auditable
    warn += g_figalt(descr)
    return hard, warn


# =============================================================================
# SELF-TEST — python3 figural_core.py --self-test  →  "SELF-TEST: N/N PASS"
#
# CLAUDE.md: "that self-test MUST contain a fixture that fails on the defect it
# was written for. A regression test that passes on the broken code tests
# nothing." Fixtures D1/D2/D5 below reproduce the SHIPPED defects and assert
# that the gates catch them.
# =============================================================================
def self_test():
    import tempfile
    passed = total = 0
    fails = []

    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            fails.append(name)

    tmp = tempfile.mkdtemp()

    def draw2(ax, series, palette):
        xs = list(range(0, 11))
        for i, s in enumerate(series):
            ax.plot(xs, [(i + 1) * v ** 0.5 for v in xs],
                    color=s["colour"], linestyle=s["linestyle"],
                    marker=s["marker"], label=s["label"])
        ax.set_xlabel("PPFD (µmol photons m⁻² s⁻¹)")
        ax.set_ylabel("Net CO₂ assimilation (µmol m⁻² s⁻¹)")
        ax.legend()

    # ---- the corrected path must be clean --------------------------------
    spec = make_figure_spec(
        4, "data_series", FIG_PROBLEM_DISPLAY_IN,
        series=series_defaults(2),
        axes={"x": {"title": "PPFD", "units": "µmol photons m⁻² s⁻¹"},
              "y": {"title": "Net CO₂ assimilation", "units": "µmol m⁻² s⁻¹"}},
        key_mode="legend")
    png = os.path.join(tmp, "ok.png")
    render_figure(draw2, png, spec)

    check("scale_is_exactly_one", abs(spec["placement_scale"] - 1.0) <= 0.02)
    check("saved_px_is_deterministic",
          spec["png_px"][0] == round(FIG_PROBLEM_DISPLAY_IN * FIGURAL_DPI))
    hard, warn = audit_figure(spec, png, descr=alt_text(spec))
    check("corrected_render_has_no_hard_failure", hard == [])
    check("alt_text_non_empty", bool(alt_text(spec).strip()))
    check("headroom_is_retired", FIG_NATIVE_HEADROOM == 1.0)

    # ---- FIXTURE D-1: monochrome data figure (the JAM defect) -------------
    # 0 of 55 shipped images contained a single coloured pixel.
    mono_spec = make_figure_spec(4, "data_series", FIG_PROBLEM_DISPLAY_IN,
                                 series=series_defaults(2, monochrome=True),
                                 key_mode="legend")
    mono_png = os.path.join(tmp, "mono.png")
    render_figure(draw2, mono_png, mono_spec)
    check("D1_monochrome_data_figure_is_caught",
          any("G-FIGCOLOUR" in m for m in g_figcolour(mono_spec, mono_png)))

    # ---- FIXTURE D-7 (v5.46): all-black schematic / data_single -----------
    # GAP-2026-08-07-FIGACCENT. IIT JAM PHYSICS Mock01 shipped 16/16 figures
    # at 0.0000% coloured pixels while IIT JAM BIOTECH Mock01 shipped accented
    # ones; both passed every gate. This fixture reproduces the shipped defect
    # (a schematic drawn entirely in black) and asserts G-FIGACCENT catches
    # it; the accented render of the SAME geometry must pass.
    def draw_schem(ax, series, palette, ink="#000000"):
        ax.plot([0, 1, 2], [0, 1, 0], color="#000000", lw=FIG_MIN_STROKE_PT)
        ax.plot([0.8, 1.2], [0.5, 0.5], color=ink, lw=3.0)   # interrogated item
        ax.set_xlabel("position"); ax.set_ylabel("level")
    schem_black = make_figure_spec(7, "schematic", FIG_PROBLEM_DISPLAY_IN,
                                   series=series_defaults(1, monochrome=True))
    p_black = os.path.join(tmp, "schem_black.png")
    render_figure(lambda ax, s, pal: draw_schem(ax, s, pal, "#000000"),
                  p_black, schem_black)
    check("D7_all_black_schematic_is_caught",
          any("G-FIGACCENT" in m for m in g_figaccent(schem_black, p_black)))
    schem_acc = make_figure_spec(7, "schematic", FIG_PROBLEM_DISPLAY_IN,
                                 series=series_defaults(1))
    p_acc = os.path.join(tmp, "schem_acc.png")
    render_figure(lambda ax, s, pal: draw_schem(ax, s, pal, pal[0]),
                  p_acc, schem_acc)
    check("D7_accented_schematic_passes", g_figaccent(schem_acc, p_acc) == [])
    # data_series is G-FIGCOLOUR territory, never G-FIGACCENT's — no double gate
    check("D7_accent_gate_ignores_data_series",
          g_figaccent(mono_spec, mono_png) == [])
    # reasoning_glyph is exempt: monochrome there is MANDATORY (G-FIGMONO)
    check("D7_accent_gate_ignores_reasoning_glyph",
          g_figaccent({"class": "reasoning_glyph"}, p_black) == [])
    # EC-V18: a legacy figure with no sidecar must stay silent
    check("D7_accent_gate_is_legacy_safe", g_figaccent({}, p_black) == [])
    # WIRING, not just logic: the audit pipeline reaches this gate ONLY through
    # audit_figure(). Found by mutation testing 2026-08-07 — with the += line
    # deleted every fixture stayed green, the exact hollow-branch class
    # audit_mutation.py exists for. This fixture kills that mutant.
    _h7, _w7 = audit_figure(schem_black, p_black)
    check("D7_accent_finding_flows_through_audit_figure",
          any("G-FIGACCENT" in m for m in _h7))
    _h7c, _w7c = audit_figure(schem_acc, p_acc)
    check("D7_accented_is_clean_through_audit_figure",
          not any("G-FIGACCENT" in m for m in _h7c))
    check("D7_accent_gate_never_blocks",
          severity_of("G-FIGACCENT") == "AMBER"
          and "G-FIGACCENT" in NEVER_BLOCKING_ON_COLOUR
          and AUDIT_GATE_ID["G-FIGACCENT"] == "A-FIGACCENT")
    # v5.46 palette plumbing: an override must reach the draw and stay
    # backwards compatible when omitted
    ovr_spec = make_figure_spec(7, "schematic", FIG_PROBLEM_DISPLAY_IN,
                                series=series_defaults(1))
    p_ovr = os.path.join(tmp, "schem_ovr.png")
    render_figure(lambda ax, s, pal: draw_schem(ax, s, pal, pal[0]),
                  p_ovr, ovr_spec, palette=["#D55E00"])
    check("D7_palette_override_reaches_draw_fn",
          g_figaccent(ovr_spec, p_ovr) == [])

    # ---- FIXTURE D-2: headroom halving (S = 0.500 on 24/24 option canvases)
    halved = dict(spec)
    halved["placement_scale"] = 0.500
    check("D2_halved_placement_is_caught",
          any("G-FIGSCALE" in m for m in g_figscale(halved)))

    # ---- FIXTURE D-5: label below the on-page floor -----------------------
    tiny = dict(spec)
    tiny["placement_scale"] = 0.500
    tiny["font_pt_native"] = {"body": 10.0, "small": 9.0, "floor": 9.0}
    check("D5_sub_floor_label_is_caught",
          any("G-FIGLABEL" in m for m in g_figlabel(tiny)))
    check("D5_gate_is_arithmetic_not_pixels",
          g_figlabel(tiny) and "pt on page" in g_figlabel(tiny)[0])

    # ---- the long-label false positive that sank the GAP-R2 renderer ------
    # Identical font request, long scientific axis titles. Must NOT hard-fail.
    check("long_scientific_labels_do_not_hard_fail", hard == [])

    # ---- colour-only encoding --------------------------------------------
    colour_only = make_figure_spec(9, "data_series", 4.0, series=[
        {"id": "a", "label": "A", "colour": "#0072B2", "linestyle": "-", "marker": "o"},
        {"id": "b", "label": "B", "colour": "#D55E00", "linestyle": "-", "marker": "o"}])
    check("colour_only_encoding_is_caught",
          any("G-FIGSERIES" in m for m in g_figseries(colour_only)))
    check("redundant_encoding_passes", g_figseries(spec) == [])

    # ---- CVD ---------------------------------------------------------------
    check("okabe_ito_pairs_are_cvd_safe", g_figcvd(spec) == [])
    check("duplicate_declared_colour_is_caught",
          any("same colour" in m for m in g_figcvd(
              {"series": [{"id": "a", "colour": "#0072B2"},
                          {"id": "b", "colour": "#0072B2"}]})))
    check("cvd_gate_is_pixel_free_and_reproducible",
          g_figcvd(spec) == g_figcvd(spec) == [])
    check("cvd_constants_are_pinned",
          all(isinstance(v, (int, float)) for v in
              (CVD_QUANT, CVD_MIN_AREA, CVD_SAT_MIN, LUMA_ADVISORY_SEP, DEUT_MIN_SEP)))

    # ---- reasoning glyphs stay monochrome ---------------------------------
    def draw_glyph(ax, series, palette):
        ax.add_patch(__import__("matplotlib").patches.Rectangle(
            (0.1, 0.1), 0.8, 0.8, fill=False, lw=FIG_MIN_STROKE_PT,
            edgecolor=palette[0]))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    gspec = make_figure_spec(1, "reasoning_glyph", FIG_OPT_DISPLAY_IN,
                             role="option")
    gpng = os.path.join(tmp, "glyph.png")
    render_figure(draw_glyph, gpng, gspec)
    check("reasoning_glyph_renders_monochrome",
          coloured_fraction(gpng) < 0.005)
    check("reasoning_glyph_exempt_from_colour_gate",
          g_figcolour(gspec, gpng) == [])
    check("option_canvas_scale_is_one",
          abs(gspec["placement_scale"] - 1.0) <= 0.02)

    # ---- option canvas uniformity ------------------------------------------
    g2 = make_figure_spec(1, "reasoning_glyph", FIG_OPT_DISPLAY_IN, role="option")
    gpng2 = os.path.join(tmp, "glyph2.png")
    render_figure(draw_glyph, gpng2, g2)
    check("uniform_option_canvases_pass",
          g_figoptunif([gspec, g2], [gpng, gpng2]) == [])
    g3 = make_figure_spec(1, "reasoning_glyph", 2.0, role="option")
    gpng3 = os.path.join(tmp, "glyph3.png")
    render_figure(draw_glyph, gpng3, g3)
    check("non_uniform_option_canvases_are_caught",
          g_figoptunif([gspec, g3], [gpng, gpng3]) != [])

    # ---- class discipline ---------------------------------------------------
    try:
        make_figure_spec(1, "chart", 4.0)
        check("unknown_class_is_hard", False)
    except FiguralError:
        check("unknown_class_is_hard", True)
    try:
        make_figure_spec(1, "data_series", 4.0, series=series_defaults(1))
        check("data_series_needs_two_series", False)
    except FiguralError:
        check("data_series_needs_two_series", True)

    # ---- OWNER DIRECTIVE: no colour condition may ever halt ----------------
    for g in ("G-FIGCOLOUR", "G-FIGCVD", "G-FIGSERIES", "G-FIGMONO"):
        check(f"colour_gate_never_blocking_{g}",
              severity_of(g) != "BLOCKING")
    check("mono_leak_voids_item_not_run", severity_of("G-FIGMONO") == "VOID_ITEM")
    check("triage_never_raises",
          isinstance(triage(["G-FIGCOLOUR: x", "G-FIGSCALE: y"], spec), dict))
    check("triage_puts_colour_in_amber",
          "G-FIGCOLOUR: x" in triage(["G-FIGCOLOUR: x"], spec)["AMBER"])
    # EC-V18: legacy output (no sidecar) must never hit a BLOCKING verdict
    _legacy = triage(["G-FIGSCALE: s=0.500", "G-FIGCOLOUR: mono"], None)
    check("EC-V18_legacy_downgrades_to_amber", _legacy["BLOCKING"] == [])
    check("EC-V18_legacy_still_reports_loudly", len(_legacy["AMBER"]) == 2)
    # v5.33 output DOES trip the regression detector
    _regressed = dict(spec); _regressed["placement_scale"] = 0.5
    check("v533_regression_is_blocking",
          triage(g_figscale(_regressed), _regressed)["BLOCKING"] != [])

    # ---- DEPENDENCY ABSENCE MUST NEVER RAISE IN AN AUDIT --------------------
    # Step 0 installs python-docx only. Every gate must survive a missing
    # package, because an audit that dies takes ~200 projects with it.
    # Blocks importlib.import_module too, which a builtins.__import__ hook does
    # NOT: import_module drives the import system directly. An earlier version
    # of this fixture patched __import__ only, so nothing was ever blocked and
    # all six cases passed against unguarded code — a test that proves nothing.
    import sys as _sys

    class _Blocker:
        def __init__(self, names):
            self.names = tuple(names)

        def find_module(self, fullname, path=None):
            return self.find_spec(fullname, path)

        def find_spec(self, fullname, path=None, target=None):
            if fullname.split(".")[0] in self.names:
                raise ImportError(f"blocked {fullname}")
            return None

    for _blocked in (("numpy",), ("PIL",), ("scipy",), ("fontTools",),
                     ("numpy", "PIL"), ("numpy", "PIL", "scipy", "fontTools")):
        _evicted = {k: v for k, v in _sys.modules.items()
                    if k.split(".")[0] in _blocked}
        for k in _evicted:
            del _sys.modules[k]
        _bl = _Blocker(_blocked)
        _sys.meta_path.insert(0, _bl)
        try:
            _h, _w = audit_figure(spec, png, descr="x")
            _ok_run, _t = True, triage(_h + _w, spec)
        except Exception:                                      # noqa: BLE001
            _ok_run, _t = False, None
        finally:
            _sys.meta_path.remove(_bl)
            _sys.modules.update(_evicted)
        _tag = "_".join(_blocked)
        check(f"audit_survives_missing_{_tag}", _ok_run)
        check(f"missing_{_tag}_never_blocks",
              _ok_run and _t["BLOCKING"] == [])
        check(f"missing_{_tag}_is_reported_not_silent",
              _ok_run and (len(_t["AMBER"]) > 0
                           or _blocked in (("scipy",), ("fontTools",))))

    check("preflight_never_raises", isinstance(preflight(), dict))
    check("preflight_names_missing_packages",
          "missing" in preflight() and "pip" in preflight())
    check("dependencies_are_declared", set(DEPENDENCIES) >= {
        "matplotlib", "PIL", "numpy", "scipy", "fontTools"})
    check("dormant_findings_route_to_amber",
          triage(["G-FIGDPI: DORMANT — Pillow unavailable"], spec)["AMBER"] != [])
    check("dormant_findings_never_block",
          triage(["G-FIGDPI: DORMANT — x", "G-FIGSCALE: DORMANT — y"],
                 spec)["BLOCKING"] == [])

    # ---- EC-V18: a gate must NEVER raise on legacy output (no sidecar) ------
    # An earlier draft indexed spec["class"] and raised KeyError on the first
    # delivered drawing, which would have crashed the audit for ~200 exams.
    _raised = None
    try:
        _h, _w = audit_figure({}, png, descr=None)
    except Exception as _e:                                    # noqa: BLE001
        _raised = _e
    check("legacy_empty_spec_does_not_raise", _raised is None)
    check("legacy_empty_spec_still_returns_findings",
          _raised is None and isinstance(_h, list))
    check("legacy_empty_spec_never_blocks",
          _raised is None and triage(_h + _w, {})["BLOCKING"] == [])
    for _partial in ({"class": "data_series"}, {"series": []},
                     {"display_in": 4.0}, {"class": "bogus"},
                     {"placement_scale": None}, {"font_pt_native": {}}):
        try:
            audit_figure(_partial, png, descr=None)
            _pok = True
        except Exception:                                      # noqa: BLE001
            _pok = False
        check(f"partial_spec_tolerated_{sorted(_partial)[0]}", _pok)
    check("alt_text_tolerates_empty_spec", isinstance(alt_text({}), str))

    # ---- audit-id mapping must be total and A-* prefixed --------------------
    check("every_gate_has_an_audit_id",
          set(AUDIT_GATE_ID) == set(SEVERITY))
    check("audit_ids_are_all_A_prefixed",
          all(v.startswith("A-") for v in AUDIT_GATE_ID.values()))
    check("audit_ids_are_unique",
          len(set(AUDIT_GATE_ID.values())) == len(AUDIT_GATE_ID))
    check("audit_ids_match_M_GATE_catalogue_regex",
          all(__import__("re").fullmatch(r"A-[A-Z]+(?:-[A-Z]+)*", v)
              for v in AUDIT_GATE_ID.values()))
    check("audit_gate_id_maps_a_finding",
          audit_gate_id("G-FIGCOLOUR: 0.000% coloured") == "A-FIGCOLOUR")
    # v5.55: 13 -> 17 (+G-FIGFIT, +G-FIGCOLLIDE, +G-FIGOPTWINDOW, +W-FIGFITPX).
    # The count is asserted, not hardcoded in prose, so a gate added without a
    # severity cannot ship silently at the default.
    check("gate_count_is_nineteen", len(SEVERITY) == 19)
    # Every id a gate can EMIT must be registered. The alt-text gate once
    # emitted "W-FIGALT" while SEVERITY keyed "G-FIGALT", so a real alt-text
    # failure mapped to no catalogue gate and was reported under an id the audit
    # spec does not document. An unregistered id degrades silently to AMBER,
    # which is the safe direction and therefore the easy one to miss.
    _emitted_ids = set()
    _probe_specs = [spec, mono_spec, gspec, {}, colour_only]
    for _ps in _probe_specs:
        for _fn, _args in ((g_figdpi, (_ps, png)), (g_figdegen, (_ps, png)),
                           (g_figscale, (_ps,)), (g_figlabel, (_ps,)),
                           (g_figcolour, (_ps, png)), (g_figmono, (_ps, png)),
                           (g_figseries, (_ps,)), (g_figcvd, (_ps,)),
                           (g_figglyph, (_ps, png)),
                           (g_figlabel_pixels, (_ps, png)),
                           (g_figalt, (None,))):
            try:
                for _m in _fn(*_args):
                    _emitted_ids.add(_m.split(":")[0].strip())
            except Exception:                                  # noqa: BLE001
                pass
    _unregistered = sorted(_emitted_ids - set(SEVERITY))
    check("every_emitted_id_is_registered_in_SEVERITY", _unregistered == [])
    check("every_emitted_id_maps_to_an_audit_gate",
          all(audit_gate_id(i + ": x").startswith("A-") for i in _emitted_ids))

    # ---- G-FIGCVD must not flag the palette the spec mandates --------------
    _cvdfired = 0
    for _k in (2, 3, 4, 5, 8):
        _s = make_figure_spec(1, "data_series", 4.0, series=series_defaults(_k),
                              axes={"x": {"title": "t"}, "y": {"title": "y"}},
                              key_mode="legend")
        _p = os.path.join(tmp, f"cvd{_k}.png")
        render_figure(draw2, _p, _s)
        _cvdfired += len(g_figcvd(_s, _p))
    check("okabe_ito_does_not_trip_its_own_cvd_gate", _cvdfired == 0)

    # ---- degeneracy: bounded at the producer -------------------------------
    try:
        make_figure_spec(1, "data_series", 1.3, series=series_defaults(2))
        check("data_class_below_min_width_is_refused", False)
    except FiguralError:
        check("data_class_below_min_width_is_refused", True)
    check("degeneracy_gate_passes_a_good_figure", g_figdegen(spec, png) == [])

    # ---- layout regression: the fix must not inflate the page --------------
    # D := min(N, C) would place a 1.3 in option canvas at 2.6 in, making a
    # four-option stack 10.4 in against a ~9.0 in page text height.
    check("option_display_width_is_preserved",
          FIG_OPT_DISPLAY_IN == 1.3 and gspec["placed_in"] == 1.3)
    check("four_option_stack_fits_a_page",
          4 * FIG_OPT_DISPLAY_IN < 9.0)

    # ---- v5.55 GAP-2026-08-19-FIGFIT regression fixtures -------------------
    # CLAUDE.md: "that self-test MUST contain a fixture that fails on the defect
    # it was written for. A regression test that passes on the broken code tests
    # nothing." D6-D11 reproduce the SHIPPED defects measured on
    # IIT_JAM_CHEMISTRY Mock01 and assert the new gates catch them.

    # D6 — ink outside the frame (Q3 opt A: 4.06% of the ink beyond the border).
    _outside = dict(gspec)
    _outside["fit"] = {"clearance_in": -0.031, "clearance_floor_in": 0.05,
                       "content_fill_frac": 0.62, "collisions_after": 0,
                       "worst_overlap_frac": 0.0}
    check("D6_figfit_catches_ink_outside_frame",
          any("OUTSIDE the frame" in f for f in g_figfit(_outside)))

    # D7 — content touching the frame (10 of 24 delivered canvases, < 0.04 in).
    _touch = dict(gspec)
    _touch["fit"] = {"clearance_in": 0.008, "clearance_floor_in": 0.05,
                     "content_fill_frac": 0.62, "collisions_after": 0,
                     "worst_overlap_frac": 0.0}
    check("D7_figfit_catches_content_touching_frame",
          any("below the" in f for f in g_figfit(_touch)))

    # D8 — wasted page allocation (delivered median ink bbox 29.6% of canvas).
    _waste = dict(gspec)
    _waste["fit"] = {"clearance_in": 0.09, "clearance_floor_in": 0.05,
                     "content_fill_frac": 0.296, "collisions_after": 0,
                     "worst_overlap_frac": 0.0}
    check("D8_figfit_catches_wasted_canvas",
          any("white space" in f for f in g_figfit(_waste)))

    # D9 — CH3 printed on top of CH3 (Q11 opts C and D).
    _coll = dict(gspec)
    _coll["fit"] = {"clearance_in": 0.09, "clearance_floor_in": 0.05,
                    "content_fill_frac": 0.62, "collisions_after": 2,
                    "worst_overlap_frac": 0.97, "collide_tol": FIG_COLLIDE_TOL,
                    "label_shift_max_in": 0.10, "label_shift_cap_in": 0.10}
    check("D9_figcollide_catches_overprinted_labels", g_figcollide(_coll) != [])
    check("D9_figcollide_is_void_item_never_blocking",
          SEVERITY["G-FIGCOLLIDE"] == "VOID_ITEM"
          and triage(g_figcollide(_coll), _coll)["BLOCKING"] == [])

    # D10 — options fitted independently: divergent scales are an answer cue.
    _a = dict(gspec); _a["fit"] = {"data_window": [0, 0, 1, 1]}
    _b = dict(gspec); _b["fit"] = {"data_window": [0, 0, 2, 2]}
    check("D10_figoptwindow_catches_divergent_scale",
          g_figoptwindow([_a, _b]) != [])
    _c = dict(gspec); _c["fit"] = {"data_window": [0, 0, 1, 1]}
    check("D10_figoptwindow_passes_a_shared_window",
          g_figoptwindow([_a, _c]) == [])

    # D11 — EC-V18: pre-v5.55 output has no fit record and MUST stay silent, or
    # ~200 existing exams fail their next audit on a gate that did not exist
    # when they were rendered.
    check("D11_legacy_spec_is_silent_under_figfit", g_figfit({}) == [])
    check("D11_legacy_spec_is_silent_under_figcollide", g_figcollide({}) == [])
    _nofit = dict(gspec); _nofit["fit"] = None
    check("D11_new_output_without_fit_record_is_loud",
          (not is_legacy(_nofit)) and g_figfit(_nofit) != [])
    check("D11_figfit_blocking_downgrades_for_legacy",
          triage(["G-FIGFIT: ink lies OUTSIDE the frame by 0.031 in."],
                 {})["BLOCKING"] == [])

    # D12 — the fitter actually repairs a real overflow. Not a mocked record:
    # this renders a draw_fn that puts a label far outside the authored window
    # (the shipped shape) and asserts the saved artefact clears the frame.
    if _have("matplotlib"):
        _fp = os.path.join(tempfile.mkdtemp(), "q1_opt1.png")

        def _runaway(ax, series, palette):
            ax.plot([0, 1], [0, 1], color="#000000", lw=FIG_MIN_STROKE_PT)
            ax.text(3.4, 3.4, "OH", fontsize=10, color=palette[0])
            ax.text(-2.6, -2.2, "CH$_3$", fontsize=10, color=palette[0])

        _rs = make_figure_spec(1, "option_canvas", FIG_OPT_DISPLAY_IN,
                               role="option")
        render_figure(_runaway, _fp, _rs)
        check("D12_fitter_brings_runaway_labels_inside_the_frame",
              g_figfit(_rs) == [] or "OUTSIDE" not in " ".join(g_figfit(_rs)))
        check("D12_fit_record_is_written", (_rs.get("fit") or {}).get("engine")
              == "fit_and_deconflict/v5.57")
        check("D12_renderer_frame_is_not_overprinted",
              g_figfit_pixels(_rs, _fp) == [])
        check("D12_placement_scale_is_still_one", _rs["placement_scale"] == 1.0)

    # D13 — v5.57 GAP-2026-08-20-FIGURAL-INK-CENSUS. Reproduces the shipped
    # Q44 shape: a ring plus a substituent bond drawn with the empty-text
    # annotate idiom. Through v5.56 the census never saw the bond, the window
    # was symmetric about the ring, the bond was clipped at the frame, the fit
    # record said OK and no gate fired. The fixtures assert (a) the census now
    # sees the arrow, (b) the saved artefact carries the whole bond, (c) G-FIGINK
    # is silent on a conformant render, (d) G-FIGINK FIRES when ink is forced
    # outside the measured box, (e) legacy specs stay silent.
    if _have("matplotlib") and _have("numpy") and _have("PIL.Image"):
        import numpy as _np
        from PIL import Image as _Im

        def _ring(ax):
            pts = [(math.cos(math.radians(60 * i)), math.sin(math.radians(60 * i)))
                   for i in range(7)]
            ax.plot([p[0] for p in pts], [p[1] for p in pts],
                    color="#000000", lw=FIG_MIN_STROKE_PT)
            ax.set_axis_off()          # as every Step-7 schematic draw_fn does
            # (no set_aspect: the fitter owns the window/aspect — apply_data_window)

        def _q44_shape(ax, series, palette):
            _ring(ax)
            ax.annotate("", xy=(1.0, 0.0), xytext=(1.55, 0.0),
                        arrowprops=dict(arrowstyle="-", color=palette[0],
                                        lw=FIG_MIN_STROKE_PT))

        _d13 = os.path.join(tempfile.mkdtemp(), "q44_problem.png")
        _s13 = make_figure_spec(44, "schematic", 4.0, series=[], axes={})
        _s13["role"] = "problem"
        render_figure(_q44_shape, _d13, _s13)
        _w13 = _s13["fit"]["data_window"]
        check("D13_census_sees_annotation_arrow",
              _w13[2] > 1.5 and (_w13[2] - 1.0) > (-_w13[0] - 1.0) + 0.2)
        _a13 = _np.array(_Im.open(_d13).convert("L"))
        _ink13, _c13, _ = _ink_mask_and_frame(_a13, _np)
        _cols13 = _np.where(_c13.any(0))[0]
        check("D13_bond_not_clipped_at_frame",
              _cols13.max() < _a13.shape[1] - 1 - FIG_INK_TOL_PX)
        check("D13_figink_silent_on_conformant_render", g_figink(_s13, _d13) == [])
        check("D13_fit_record_carries_content_bbox_px",
              isinstance(_s13["fit"].get("content_bbox_px"), list)
              and len(_s13["fit"]["content_bbox_px"]) == 4)
        # (d) force the defect: a window that windows the bond out.
        _d13b = os.path.join(tempfile.mkdtemp(), "q44_clipped.png")
        _s13b = make_figure_spec(44, "schematic", 4.0, series=[], axes={})
        _s13b["role"] = "problem"
        render_figure(_q44_shape, _d13b, _s13b, window=(-1.3, -1.0, 1.3, 1.0))
        # the census box is now the full (clipped) content; shrink it to what a
        # blind census would have recorded (the ring only) and the gate must fire.
        _bb = list(_s13b["fit"]["content_bbox_px"])
        _ax0, _ay0, _ax1, _ay1 = _s13b["fit"]["axes_bbox_px"]
        _s13b["fit"]["content_bbox_px"] = [_bb[0], _bb[1],
                                           _bb[0] + 0.78 * (_bb[2] - _bb[0]), _bb[3]]
        _f13 = g_figink(_s13b, _d13b)
        check("D13_figink_fires_on_ink_outside_measured_box",
              len(_f13) == 1 and "OUTSIDE" in _f13[0] and "right" in _f13[0])
        check("D13_figink_is_blocking_on_new_output",
              triage(_f13, _s13b)["BLOCKING"] == _f13)
        check("D13_figink_legacy_unframed_is_silent", g_figink({}, _d13b) == []
              and g_figink({"fit": {"clearance_in": 0.06}}, _d13b) == [])
        # legacy FRAMED canvas with a clipped stroke: AMBER edge form fires;
        # a clean legacy framed canvas stays silent.
        _d13e = os.path.join(tempfile.mkdtemp(), "q1_opt_legacy.png")
        _s13e = make_figure_spec(1, "option_canvas", FIG_OPT_DISPLAY_IN, role="option")
        render_figure(_q44_shape, _d13e, _s13e, window=(-1.3, -1.0, 1.3, 1.0))
        _leg_e = {"png_dpi": FIGURAL_DPI, "fit": {"clearance_in": 0.06}}
        _f13e = g_figink(_leg_e, _d13e)
        check("D13_legacy_framed_clip_is_amber",
              len(_f13e) == 1 and _f13e[0].startswith("W-FIGINK")
              and "right" in _f13e[0] and triage(_f13e, {})["BLOCKING"] == [])
        check("D13_figink_maps_to_audit_id",
              audit_gate_id("G-FIGINK: x") == "A-FIGINK"
              and audit_gate_id("W-FIGINK: x") == "A-FIGINKPX")
        # axis-ON render (ticks, spines are legitimate chrome): the same
        # forced clip is reported AMBER, never BLOCKING, and chrome alone
        # never fires.
        def _q44_axis_on(ax, series, palette):
            _q44_shape(ax, series, palette)
            ax.set_axis_on()
        _d13d = os.path.join(tempfile.mkdtemp(), "q44_axis_on.png")
        _s13d = make_figure_spec(44, "schematic", 4.0, series=[], axes={})
        _s13d["role"] = "problem"
        render_figure(_q44_axis_on, _d13d, _s13d)
        check("D13_axis_on_chrome_never_fires", g_figink(_s13d, _d13d) == [])
        _bbd = list(_s13d["fit"]["content_bbox_px"])
        _s13d["fit"]["content_bbox_px"] = [_bbd[0], _bbd[1],
                                           _bbd[0] + 0.78 * (_bbd[2] - _bbd[0]), _bbd[3]]
        _f13d = g_figink(_s13d, _d13d)
        check("D13_axis_on_clip_is_amber_not_blocking",
              len(_f13d) == 1 and _f13d[0].startswith("W-FIGINK")
              and triage(_f13d, _s13d)["BLOCKING"] == []
              and triage(_f13d, _s13d)["AMBER"] == _f13d)
        _hd, _wd = audit_figure(_s13d, _d13d, "x")
        check("D13_audit_figure_routes_w_figink_to_warn",
              not any("FIGINK" in x for x in _hd) and any("W-FIGINK" in x for x in _wd))
        # (f) a framed option render with a real label stays clean end to end.
        def _opt_shape(ax, series, palette):
            _ring(ax)
            ax.plot([1.0, 1.5], [0.0, 0.0], color=palette[0], lw=FIG_MIN_STROKE_PT)
            ax.text(1.6, 0.0, "COOH", color=palette[0], fontsize=10, va="center")
        _d13c = os.path.join(tempfile.mkdtemp(), "q1_opt1.png")
        _s13c = make_figure_spec(1, "option_canvas", FIG_OPT_DISPLAY_IN, role="option")
        render_figure(_opt_shape, _d13c, _s13c)
        _h13c, _ = audit_figure(_s13c, _d13c, "ring with carboxyl")
        check("D13_legacy_framed_clean_is_silent", g_figink(_leg_e, _d13c) == [])
        check("D13_framed_option_with_label_is_silent_under_figink",
              [x for x in _h13c if "FIGINK" in x] == []
              and (_s13c["fit"].get("content_bbox_px") or [0, 0, 0, 0])[2] > 300)

        # ── R2 (v5.61, GAP-2026-08-22-FIGASPECT-SELF-FULFILLING) ────────────
        # The defect, pinned: v5.60 derived the option-set canvas aspect from
        # the union of pass-1 data_windows, which apply_data_window() had
        # already inflated to the canvas pass 1 rendered on — so the derivation
        # returned its own assumption. Measured on this exact fixture: a square
        # hexagon set derived 0.69, filled 41% (< the 45% floor), and G-FIGFIT
        # BLOCKED a correct drawing. The aspect now comes from zoom-invariant
        # STROKE geometry; a unanimous author declaration is honoured exactly.
        import math as _math
        def _hexopt(tag):
            def _d(ax, series, palette):
                _pts = [( _math.cos(a), _math.sin(a))
                        for a in [_math.pi / 6 + i * _math.pi / 3 for i in range(6)]]
                for i in range(6):
                    _x0, _y0 = _pts[i]; _x1, _y1 = _pts[(i + 1) % 6]
                    ax.plot([_x0, _x1], [_y0, _y1], color="black", lw=2.0)
                ax.text(0, 1.25, "CH3", ha="center", va="bottom", fontsize=9)
                ax.text(1.15, 0, tag, ha="left", va="center", fontsize=9)
            return _d
        _r2d = tempfile.mkdtemp()
        _r2s = [make_figure_spec(7, "option_canvas", FIG_OPT_DISPLAY_IN,
                                 role="option") for _ in range(2)]
        render_option_set([_hexopt("Cl"), _hexopt("Br")],
                          [os.path.join(_r2d, f"r2_{i}.png") for i in range(2)],
                          _r2s)
        _asp = _r2s[0]["canvas_aspect"]
        check("R2_square_strokes_get_square_canvas",
              1.05 <= _asp <= 1.25 and _r2s[1]["canvas_aspect"] == _asp)
        check("R2_square_set_fill_clears_floor",
              _r2s[0]["fit"]["set_fill_frac"] >= MIN_CONTENT_FILL_FRAC
              and not [x for x in g_figfit(_r2s[0]) if "fills" in x])
        check("R2_fit_records_both_windows",
              _r2s[0]["fit"].get("stroke_window") is not None
              and _r2s[0]["fit"].get("content_window") is not None)
        _sw, _cw2, _dw = (_r2s[0]["fit"]["stroke_window"],
                          _r2s[0]["fit"]["content_window"],
                          _r2s[0]["fit"]["data_window"])
        check("R2_windows_nest_stroke_content_data",
              _dw[0] <= _cw2[0] <= _sw[0] + 1e-6 and _dw[1] <= _cw2[1] <= _sw[1] + 1e-6
              and _sw[2] - 1e-6 <= _cw2[2] <= _dw[2] and _sw[3] - 1e-6 <= _cw2[3] <= _dw[3])
        # unanimous declaration: honoured EXACTLY, never clobbered (v5.60 bug 2)
        _r2b = [make_figure_spec(7, "option_canvas", FIG_OPT_DISPLAY_IN,
                                 role="option", canvas_aspect=0.8) for _ in range(2)]
        render_option_set([_hexopt("F"), _hexopt("I")],
                          [os.path.join(_r2d, f"r2b_{i}.png") for i in range(2)],
                          _r2b)
        check("R2_unanimous_declared_aspect_honoured",
              all(x["canvas_aspect"] == 0.8 for x in _r2b))
        # wide strokes clamp at the band floor; a non-unanimous declaration is
        # NOT a set decision and falls through to content derivation
        def _chain(tag):
            def _d(ax, series, palette):
                ax.plot([0, 8], [0, 0.6], color="black", lw=2.0)
                ax.text(4, 0.75, tag, ha="center", fontsize=9)
            return _d
        _r2c = [make_figure_spec(8, "option_canvas", FIG_OPT_DISPLAY_IN,
                                 role="option",
                                 canvas_aspect=(0.9 if i == 0 else None))
                for i in range(2)]
        render_option_set([_chain("A"), _chain("B")],
                          [os.path.join(_r2d, f"r2c_{i}.png") for i in range(2)],
                          _r2c)
        check("R2_wide_clamps_and_mixed_declaration_ignored",
              _r2c[0]["canvas_aspect"] == FIG_CANVAS_ASPECT_MIN
              and _r2c[1]["canvas_aspect"] == FIG_CANVAS_ASPECT_MIN)
        # an all-text set has no strokes: content fallback, no crash, in-band
        def _txt(tag):
            def _d(ax, series, palette):
                ax.text(0.5, 0.5, tag, ha="center", va="center", fontsize=11)
            return _d
        _r2e = [make_figure_spec(9, "option_canvas", FIG_OPT_DISPLAY_IN,
                                 role="option") for _ in range(2)]
        render_option_set([_txt("syn"), _txt("anti")],
                          [os.path.join(_r2d, f"r2e_{i}.png") for i in range(2)],
                          _r2e)
        check("R2_textonly_set_falls_back_in_band",
              FIG_CANVAS_ASPECT_MIN <= _r2e[0]["canvas_aspect"]
              <= FIG_CANVAS_ASPECT_MAX
              and _r2e[0]["fit"].get("stroke_window") is None)

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("figural_core.py — shared figure renderer + gates. Run with --self-test.")
