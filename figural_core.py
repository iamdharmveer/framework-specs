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
    "G-FIGCVD":     "AMBER",
    "G-FIGSERIES":  "AMBER",
    "G-FIGALT":     "AMBER",
    "W-FIGLABELPX": "AMBER",
    "G-FIGGLYPH":   "AMBER",
    # answer-cue leaks — void the ITEM, never the run
    "G-FIGMONO":    "VOID_ITEM",
    "G-FIGOPTUNIF": "VOID_ITEM",
    # renderer-contract regressions on v5.33+ output
    "G-FIGSCALE":   "BLOCKING",
    "G-FIGLABEL":   "BLOCKING",
    "G-FIGDPI":     "BLOCKING",
    "G-FIGDEGEN":   "BLOCKING",
}
NEVER_BLOCKING_ON_COLOUR = ("G-FIGCOLOUR", "G-FIGCVD", "G-FIGSERIES", "G-FIGMONO")

# Engine-side ids are G-* (hard) and W-* (advisory). The audit catalogue is A-*,
# and Check M-GATE matches emitted gate names against A-* tokens in the spec
# text, so the audit layer MUST emit A-* names. The mapping is explicit and
# self-tested here rather than left implicit in spec prose, because a silent
# mismatch shows up as "catalogue lists X but the script never emits it" —
# a red check, not a wrong figure, and therefore easy to paper over.
AUDIT_GATE_ID = {
    "G-FIGCOLOUR":  "A-FIGCOLOUR",
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
                     role="problem"):
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
        # filled in by render_figure()
        "png_px": None,
        "font_pt_native": None,
        "placement_scale": None,
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
    return {
        "figure.figsize": (d * h, d * h * 0.72),
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


def render_figure(draw_fn, out_path, spec):
    """
    draw_fn(ax, series, palette) -> None.  Draws ONE visual unit.
    spec : from make_figure_spec(). MUTATED with the measured artefact facts.

    The caller MUST place the PNG at exactly spec['display_in'] inches
    (capped to FIG_COLUMN_IN). S10-8 does this; nothing else may.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    mono = spec["class"] in MONO_REQUIRED
    palette = ["#000000"] * len(OKABE_ITO) if mono else OKABE_ITO
    style = figure_style(spec)

    with plt.rc_context(style):
        fig, ax = plt.subplots(constrained_layout=True)
        draw_fn(ax, spec["series"], palette)
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
    """Normative hue extraction. Returns a list of quantised RGB tuples."""
    import numpy as np
    from PIL import Image
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
    """Fraction of visible pixels carrying any chroma."""
    import numpy as np
    from PIL import Image
    a = np.array(Image.open(png_path).convert("RGBA"))
    vis = a[..., 3] > 16
    rgb = a[..., :3].astype(int)
    sat = rgb.max(2) - rgb.min(2)
    return float(((sat > 25) & vis).sum()) / max(int(vis.sum()), 1)


# =============================================================================
# GATES — all DETERMINISTIC, all legal inside an audit's python
# =============================================================================
def g_figdegen(spec, png_path):
    """Catches the one failure arithmetic cannot see: a figure whose plot area
    collapsed, so the PNG is the right size and the fonts the right points but
    there is nothing legible inside."""
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return []
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
    from PIL import Image
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
    try:
        import numpy as np
        from PIL import Image
        from scipy import ndimage
    except ImportError:
        return []
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
    out = []
    if frac < 0.005:
        out.append(f"G-FIGCOLOUR: {frac:.3%} coloured pixels (need >=0.5%) on a "
                   f"{_class_of(spec)} figure.")
    declared = len(spec.get("series") or [])
    if declared >= 2 and len(hues) < 2:
        out.append(f"G-FIGCOLOUR: {len(hues)} dominant hue(s) in the PNG but "
                   f"{declared} series declared.")
    return out


def g_figmono(spec, png_path):
    """Colour in an abstract-reasoning item can leak the answer."""
    if _class_of(spec) not in MONO_REQUIRED:
        return []
    allowed = {s.get("colour", "").lower() for s in (spec.get("series") or [])
               if s.get("accent_marker")}
    frac = coloured_fraction(png_path)
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
    from PIL import Image
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
    try:
        from matplotlib.font_manager import findfont, FontProperties
        from fontTools.ttLib import TTFont
    except ImportError:
        return []
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


def audit_figure(spec, png_path, descr=None):
    """Run every gate. Returns (hard_failures, warnings)."""
    hard = []
    hard += g_figdpi(spec, png_path)
    hard += g_figdegen(spec, png_path)
    hard += g_figscale(spec, png_path)
    hard += g_figlabel(spec)
    hard += g_figcolour(spec, png_path)
    hard += g_figmono(spec, png_path)
    hard += g_figseries(spec)
    hard += g_figcvd(spec, png_path)
    hard += g_figglyph(spec, png_path)
    warn = []
    warn += g_figlabel_pixels(spec, png_path)
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
    check("gate_count_is_twelve", len(SEVERITY) == 12)
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

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("figural_core.py — shared figure renderer + gates. Run with --self-test.")
