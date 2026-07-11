#!/usr/bin/env python3
# explain_engine.py — UNIVERSAL, EXAM-AGNOSTIC explanation engine for Step 9
# (MockExplain). The ONLY path by which an explanation may enter the docx.
#
# Zero hardcoded exam values: question/option regex, option count, section
# labels, language and block-header markers are all supplied at runtime by an
# EngineConfig built from blueprint.json + section_rules.md (CATEGORY C). The
# same engine drives SSC, GATE, NEET, IBPS, UPSC, CAT and any exam with valid
# Step 5/6/7/8 outputs.
#
# Public surface (called by the Step-4 spec):
#   EngineConfig                       — runtime exam parameters (no defaults baked as exam facts)
#   ExplanationBlock(...).validate()   — validated container; raises on any structural breach
#   add_math_text(p, text)             — THE prose emitter; auto-OMMLs digit/digit; raises on bad math
#   add_math(p, omath_xml) + frac/sup/sqrt/nary/omath/_r  — explicit OMML route
#   parse_paper(path, cfg)             — read the Step-3 paper → question map (P3 validation)
#   build_interleaved_docx(src, blocks, out, cfg)  — seed WHOLE source, append blocks (append-only)
#   verify_fidelity(out, src, cfg)     — question region byte-identical to source; rIds resolve (every batch)
#   verify_structure(out, blocks, cfg) — block model + coverage + CA-binding (every batch)
#   verify_explanations(out, blocks, cfg) — INDEPENDENT post-render re-audit of the rendered docx (every batch)
#   strip_solutions(out, stripped, cfg)— questions-only copy for the Step-2 re-audit
#   self_test()                        — N/N PASS gate; run with --self-test
#   parse_solution_blocks(path, cfg)   — [STEP 5] read a Solutions docx back into blocks (inverse of build)
#   self_test_audit()                  — [STEP 5] reader round-trip gate; run with --self-test-audit
#   parse_learnings(path)              — [STEP 4] read an EXPLAIN(_AUDIT)_LEARNINGS md into structured rules (P10)
#
# This file is embedded verbatim in Appendix A of Framework_MockTestExplain.md.
# It is the canonical copy; never patch it by hand — regenerate from the spec.

import re, sys, hashlib
from docx import Document
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn

# ───────────────────────────── namespaces ──────────────────────────────────
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# ───────────────────────────── exam config ─────────────────────────────────
def _int_to_roman(n):
    out, vals = '', [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    for v, s in vals:
        while n >= v:
            out += s; n -= v
    return out

class EngineConfig:
    """Runtime exam parameters. NOTHING here is an exam fact baked into code —
    every value is passed in by the spec from blueprint.json / section_rules.md.
    The constructor defaults are STRUCTURAL fallbacks (English labels, 4 numeric
    options, single-correct MCQ, Latin-script terminators); the spec always passes
    the real values read at runtime (RE-9). Supports, per question, any of three
    question types — MCQ (one correct option), MSQ (a set of correct options) and
    NAT (a typed numerical answer, no options) — and per-section option counts,
    alphabetic/roman/custom option labels, and language-specific sentence
    terminators (e.g. the Devanagari danda)."""
    def __init__(self, q_pattern, opt_pattern, options_count,
                 labels=None, markers=None, colors=None, language='en',
                 label_scheme='numeric', sentence_terminators='.!?',
                 options_by_q=None,
                 banned_blocks=None, banned_templates=None,
                 banned_fakecites=None, metacommentary_re=None):
        self.q_re = re.compile(q_pattern)            # e.g. r'^Q\.?\s*(\d+)' or r'^Q(\d+)\.'
        self.opt_re = re.compile(opt_pattern)        # e.g. r'^([1-9])[.\)]' or r'^([A-D])[.\)]'
        self._uniform = int(options_count) if options_count is not None else None
        # v1.3.1 ROOT-CAUSE FIX (registry→engine str/int boundary, ND6): the per-question
        # option-count map round-trips through registry.json, so its keys arrive as JSON
        # STRINGS ("3") even though expected_options() is queried with an INT q
        # (ExplanationBlock.q = int(q)). Normalise keys to int on construction so a NAT
        # question (value 0) resolves regardless of how the caller keyed the map; without
        # this, int-vs-str misses fall through to the uniform count and every NAT question
        # is silently mis-typed as MCQ. Accepts int- or str-keyed input identically.
        self.options_by_q = ({int(k): v for k, v in options_by_q.items()}
                             if options_by_q else None)
        self.options_count = self._uniform           # back-compat (uniform exams)
        self.language = language
        self.label_scheme = label_scheme             # 'numeric'|'alpha_upper'|'alpha_lower'|'roman_lower'|'roman_upper'|list
        self.sentence_terminators = sentence_terminators or '.!?'
        self.labels = labels or {
            'correct_answer': 'Correct Answer',
            'axiom': 'AXIOM', 'deduction': 'DEDUCTION',
            'speed_hack': 'SPEED HACK', 'why_wrong': 'WHY WRONG?',
            'common_pitfalls': 'COMMON PITFALLS',
            'option': 'Option', 'solution_ref': 'Solution',
            'accepted_range': 'accepted range',
        }
        self.labels.setdefault('common_pitfalls', 'COMMON PITFALLS')
        self.labels.setdefault('accepted_range', 'accepted range')
        self.markers = markers or {
            'axiom': '\u2b1b', 'deduction': '\u2b1b',
            'speed_hack': '\u26a1', 'why_wrong': '\u274c', 'common_pitfalls': '\u274c',
        }
        self.markers.setdefault('common_pitfalls', '\u274c')
        self.colors = colors or {
            'ca': '003366', 'sub': '000000', 'sent': '000000',
            'hdr': '000000', 'sol_ref': '000000',
        }
        # v1.9 EXAM-AGNOSTIC: language-specific prose guards. Defaults are English
        # (the AI's primary output language); non-English exams pass their own patterns
        # via config so the guards catch language-specific template/metacommentary.
        # Pass None to use the built-in English defaults; pass an explicit list/pattern
        # to REPLACE the defaults for that exam's language.
        # NOTE on metacommentary_re: Python's \b word boundary is ASCII-only and does
        # NOT match Devanagari/CJK/Arabic word boundaries. For non-Latin scripts, omit
        # \b and use plain substring patterns (e.g. 'मुझे लगता है' not r'\bमुझे लगता है\b').
        self.banned_blocks = tuple(banned_blocks) if banned_blocks is not None else _BANNED_BLOCKS
        self.banned_templates = tuple(banned_templates) if banned_templates is not None else _BANNED_TEMPLATE
        self.banned_fakecites = tuple(banned_fakecites) if banned_fakecites is not None else _BANNED_FAKECITE
        self.metacommentary_re = (re.compile(metacommentary_re, re.I)
                                  if metacommentary_re is not None else _META_RE)

    def expected_options(self, q):
        """Option count expected for question q. 0 means NAT (no options).
        Reads the per-question map when present (mixed-section / NAT papers),
        else the uniform count."""
        if self.options_by_q is not None and q in self.options_by_q:
            return self.options_by_q[q]
        return self._uniform

    def option_label(self, i):
        """Map a 1-based option index to the paper's displayed label
        (1/2/3, A/B/C, a/b/c, i/ii/iii, or a custom list).
        Raises ValueError on out-of-bounds for custom/alpha schemes."""
        sch = self.label_scheme
        if isinstance(sch, (list, tuple)):
            if i < 1 or i > len(sch):
                raise ValueError(f'option_label({i}): out of range for custom scheme '
                                 f'of length {len(sch)} — check label_scheme vs option count')
            return str(sch[i - 1])
        if sch == 'alpha_upper':
            if i < 1 or i > 26:
                raise ValueError(f'option_label({i}): alpha_upper supports 1–26 only')
            return chr(ord('A') + i - 1)
        if sch == 'alpha_lower':
            if i < 1 or i > 26:
                raise ValueError(f'option_label({i}): alpha_lower supports 1–26 only')
            return chr(ord('a') + i - 1)
        if sch == 'roman_lower':
            return _int_to_roman(i).lower()
        if sch == 'roman_upper':
            return _int_to_roman(i)
        return str(i)                                # 'numeric' default

# ───────────────────────────── prose guards ────────────────────────────────
# Banned glyphs in student text (EX1). The block-header markers are whitelisted.
_BANNED_GLYPHS = ('\u2713', '\u2714', '\u2717', '\u2718', '\u2611', '\u2612')  # ✓✔✗✘☑☒
_BANNED_LATEX = ('\\frac', '\\sqrt', '\\left', '\\right', '$')
_BANNED_BLOCKS = ('REMEMBER', 'EXAM CONNECTION')
_BANNED_TEMPLATE = (
    'this option is wrong', 'this is a common misconception', "doesn't match the answer",
    'is incorrect as it doesn', 'this option is incorrect', 'simply wrong',
)
_BANNED_FAKECITE = (
    'official key', 'official answer', 'official solution', 'the answer key says',
    'as per the official', 'per the official key',
)

# Metacommentary as a WORD-BOUNDED regex (substring matching gave false positives:
# 'hmm' hit "ohmmeter", 'wait,' hit "await,", 'actually,' hit "factually,",
# 'as an ai' hit "has an air"). The boundaries make detection precise.
_META_RE = re.compile(
    r'\bre-reading\b|\blet me reconsider\b|\bactually,|\bhmm\b|\bwait\s*[,\u2014]|'
    r'\bas an ai\b|\blet me re-check\b|\blet me check again\b|\bi think we\b|'
    r'\bon reflection\b',
    re.I)

# digit/digit fraction with a negative lookahead so a trailing '.' (decimal) does
# NOT match — that leftover then trips has_inline_fraction (EX13, intentional).
_SIMPLE_FRAC = re.compile(r'(?<![\w/.])(\d+)\s*/\s*(\d+)(?![\d.\w/])')
# letter/letter units that are legitimately NOT fractions (km/h, m/s, w/o).
_UNIT_SLASH = re.compile(r'\b[a-zA-Z]{1,3}\s*/\s*[a-zA-Z]{1,3}\b')
# Vulgar-fraction glyphs and the Unicode fraction slash (U+2044): never allowed in
# prose — algebra/fractions must be real OMML, so these raise (A1, parity with T2).
VULGAR = '\u00bd\u2153\u2154\u00bc\u00be\u2155\u2156\u2157\u2158\u2159\u215a' \
         '\u2150\u215b\u215c\u215d\u215e\u2151\u2152\u2044'
# Inline-fraction detectors. Beyond digit/digit, catch a/letter, a/(, a/√, x²/2,
# (a+b)/c — non-convertible forms that must be built explicitly via frac() (A4).
# Units (km/h, m/s) are letter/letter and are masked out before these run.
_FRAC_PATS = (
    re.compile(r'\d\s*/\s*\d'),                  # 3/4, 2025/26
    re.compile(r'\d\s*/\s*[A-Za-z(\u221a]'),     # 1/x, 1/(x+1), 1/√2
    re.compile(r'[\u00b2\u00b3)]\s*/\s*[\dA-Za-z(]'),  # x²/2, (a+b)/c
)
# Consecutive-year slash backstop (1947/48, 2025/26, 2024/2025) — a year range must
# never silently render as a stacked fraction. Only flags when the second part is
# actually (year+1), so a genuine n/(n+1) telescoping fraction is NOT false-flagged (A6).
_YEAR_RANGE = re.compile(r'\b(1[89]\d{2}|20\d{2})\s*/\s*(\d{2}|\d{4})\b')

def _year_range_hit(text):
    """Return the matched 'YYYY/NN' string if it is a consecutive year range
    (1947/48, 2025/26, 2024/2025), else None. A real fraction whose denominator
    is not year+1 passes through untouched."""
    for m in _YEAR_RANGE.finditer(text):
        y, nxt = int(m.group(1)), m.group(2)
        if (len(nxt) == 2 and int(nxt) == (y + 1) % 100) or (len(nxt) == 4 and int(nxt) == y + 1):
            return m.group(0)
    return None

_SENT = '\u0001'   # transient sentinel standing in for a non-terminal dot

def _abbrev_safe(text):
    """Replace abbreviations / initials / decimals so the sentence counter does
    not treat their dots as sentence ends (EX2, EX12)."""
    t = text.replace('...', _SENT * 3)
    for ab in ('Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Smt.', 'Shri.', 'Sh.', 'Pt.', 'Mt.',
               'Lt.', 'Rs.', 'No.', 'Nos.', 'vs.', 'etc.', 'approx.', 'viz.', 'ft.',
               'Govt.', 'i.e.', 'e.g.', 'Col.', 'Gen.', 'Capt.', 'Maj.', 'Hon.',
               'Prof.', 'Jr.', 'Sr.', 'Corp.', 'Inc.', 'Ltd.', 'Rev.', 'Md.',
               'sq.', 'cu.', 'Art.', 'Sec.', 'Vol.', 'Ed.', 'Fig.', 'St.'):
        t = t.replace(ab, ab.replace('.', _SENT))
    # lowercase dotted acronyms: u.s, a.m, p.m, e.g, i.e (any single-letter . chain)
    t = re.sub(r'\b([a-z](?:\.[a-z])+)\.?',
               lambda m: m.group(0).replace('.', _SENT), t)
    t = re.sub(r'\b([A-Z])\.', lambda m: m.group(1) + _SENT, t)   # initials
    t = re.sub(r'(\d)\.(\d)', lambda m: m.group(1) + _SENT + m.group(2), t)  # decimals
    return t

def sentence_count(text, terminators='.!?'):
    """Abbreviation-aware sentence counter. Semicolon/comma joins count as ONE.
    `terminators` is language-configurable (e.g. include the Devanagari danda
    '\u0964' and double-danda '\u0965' for Hindi/Sanskrit/Marathi)."""
    t = _abbrev_safe(text.strip())
    cls = re.escape(''.join(dict.fromkeys(terminators)))
    parts = [p for p in re.split(f'[{cls}]+', t) if p.strip()]
    return max(1, len(parts))

def has_inline_fraction(text):
    """True if a vulgar-fraction glyph, the Unicode fraction slash, or any bare
    inline fraction (digit/digit, a/letter, a/(, a/√, x²/2, (a+b)/c) remains after
    units are masked. Such forms must be real OMML, so the prose emitter raises on
    any that survive auto-conversion (EX13, A1/A4)."""
    if any(ch in text for ch in VULGAR):
        return True
    masked = _UNIT_SLASH.sub('', text)
    return any(p.search(masked) for p in _FRAC_PATS)

def guard_sentence(text, cfg=None):
    """Validate one student-facing sentence. Raises ValueError on any breach.
    Returns the text unchanged on success. `cfg` (optional) supplies language-
    specific sentence terminators and configurable banned patterns; without it
    the English/Latin defaults are used."""
    if text is None or not str(text).strip():
        raise ValueError('empty sentence')
    s = str(text)
    low = s.lower()
    terminators = cfg.sentence_terminators if cfg is not None else '.!?'
    meta_re = cfg.metacommentary_re if cfg is not None else _META_RE
    banned_templates = cfg.banned_templates if cfg is not None else _BANNED_TEMPLATE
    banned_fakecites = cfg.banned_fakecites if cfg is not None else _BANNED_FAKECITE
    banned_blocks = cfg.banned_blocks if cfg is not None else _BANNED_BLOCKS
    for g in _BANNED_GLYPHS:
        if g in s:
            raise ValueError(f'banned glyph {g!r} in: {s[:60]!r}')
    for v in VULGAR:
        if v in s:
            raise ValueError(f'vulgar fraction glyph {v!r} — build it as OMML via frac(): {s[:60]!r}')
    for lx in _BANNED_LATEX:
        if lx in s:
            raise ValueError(f'banned LaTeX {lx!r} in: {s[:60]!r}')
    m_meta = meta_re.search(s)
    if m_meta:
        raise ValueError(f'metacommentary {m_meta.group(0)!r} in: {s[:60]!r}')
    for tp in banned_templates:
        if tp in low:
            raise ValueError(f'template sentence {tp!r} in: {s[:60]!r}')
    for fc in banned_fakecites:
        if fc in low:
            raise ValueError(f'fake citation {fc!r} in: {s[:60]!r}')
    for bb in banned_blocks:
        if bb in s:
            raise ValueError(f'banned block {bb!r} in: {s[:60]!r}')
    yr = _year_range_hit(_UNIT_SLASH.sub('', s))
    if yr:
        raise ValueError(f'year-range slash {yr!r} (use en-dash) in: {s[:60]!r}')
    if sentence_count(s, terminators) != 1:
        raise ValueError(f'not exactly one sentence: {s[:60]!r}')
    return s

# ───────────────────────────── OMML helpers ────────────────────────────────
def _r(t):     return f'<m:r xmlns:m="{M}"><m:t xml:space="preserve">{t}</m:t></m:r>'
def frac(n, d):return f'<m:f xmlns:m="{M}"><m:num>{n}</m:num><m:den>{d}</m:den></m:f>'
def sup(b, e): return f'<m:sSup xmlns:m="{M}"><m:e>{b}</m:e><m:sup>{e}</m:sup></m:sSup>'
def sqrt(x):   return (f'<m:rad xmlns:m="{M}"><m:radPr><m:degHide m:val="1"/></m:radPr>'
                       f'<m:deg/><m:e>{x}</m:e></m:rad>')
def nary(op, sub, sup_, body):
    return (f'<m:nary xmlns:m="{M}"><m:naryPr><m:chr m:val="{op}"/></m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup_}</m:sup><m:e>{body}</m:e></m:nary>')
def omath(*parts):
    return f'<m:oMath xmlns:m="{M}">{"".join(parts)}</m:oMath>'

def add_math(paragraph, omath_xml):
    """Insert an explicit OMML node into a paragraph."""
    paragraph._p.append(parse_xml(omath_xml))

def _run(paragraph, text, bold=False, color=None):
    r = paragraph.add_run(text)
    r.bold = bool(bold)
    if color:
        rpr = r._r.get_or_add_rPr()
        c = OxmlElement('w:color'); c.set(qn('w:val'), color); rpr.append(c)
    return r

def add_math_text(paragraph, text, bold=False, color=None, cfg=None):
    """THE prose emitter. Auto-converts every digit/digit fraction to stacked
    OMML; raises ValueError on any inline fraction it cannot convert, on a
    year-range slash, or on any guard breach. This is the ONLY sanctioned way to
    put explanation prose into the docx."""
    guard_sentence(text, cfg)                          # full guard first
    # Walk the string, emitting text runs and OMML fractions in order.
    # _SIMPLE_FRAC only matches digit/digit, so letter units (km/h) never match here;
    # they are handled (masked) only by the LOOSE detector in has_inline_fraction.
    pos = 0
    for m in _SIMPLE_FRAC.finditer(text):
        if text[pos:m.start()]:
            _run(paragraph, text[pos:m.start()], bold, color)
        add_math(paragraph, omath(frac(m.group(1), m.group(2))))
        pos = m.end()
    tail = text[pos:]
    if has_inline_fraction(tail):
        raise ValueError(f'unconvertible inline fraction in: {tail[:60]!r}')
    if tail:
        _run(paragraph, tail, bold, color)
    return paragraph

# ───────────────────────────── block model ─────────────────────────────────
class ExplanationBlock:
    """Validated container for one question's explanation. validate() raises on
    any structural breach BEFORE the block can be written (fail-at-construction).

    Three question types (auto-inferred or set via `qtype`):
      • 'mcq' — single correct option. ca = a 1-based int. why_wrong keys = the
                other options. (default; the common case.)
      • 'msq' — multiple correct options. ca = a set/list of 1-based ints. The last
                DEDUCTION step binds EVERY selected option; why_wrong keys = the
                NON-selected options.
      • 'nat' — numerical-answer-type, NO options. ca = the answer value (number or
                string); optional ca_range = (lo, hi) tolerance. The last DEDUCTION
                step contains the value; common_pitfalls (value -> sentences, ≥1)
                replaces why_wrong (there are no options to reject)."""
    def __init__(self, q, ca=None, axiom=None, deduction=None, speed_hack=None,
                 why_wrong=None, anomaly=None, cfg=None,
                 qtype=None, ca_range=None, common_pitfalls=None):
        self.q = int(q)
        self.cfg = cfg or EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
        self.ca = ca
        self.ca_range = ca_range
        self.axiom = list(axiom or [])
        self.deduction = list(deduction or [])
        self.speed_hack = list(speed_hack) if speed_hack else None
        self.why_wrong = dict(why_wrong or {})
        self.common_pitfalls = dict(common_pitfalls or {})
        self.anomaly = anomaly
        # infer question type if not given
        if qtype is None:
            if self.cfg.expected_options(self.q) == 0:
                qtype = 'nat'
            elif isinstance(ca, (set, list, tuple)):
                qtype = 'msq'
            else:
                qtype = 'mcq'
        self.qtype = qtype

    def ca_set(self):
        """The selected option indices as a set (mcq -> {ca}; msq -> set(ca))."""
        if self.qtype == 'mcq':
            return {self.ca}
        return set(self.ca)

    def validate(self):
        cfg = self.cfg
        g = lambda s: guard_sentence(s, cfg)
        if self.anomaly is not None:
            # anomaly is an INTERNAL escalation signal in Step 9 (never published).
            if any([self.axiom, self.deduction, self.why_wrong,
                    self.speed_hack, self.common_pitfalls]):
                raise ValueError(f'Q{self.q}: anomaly block must carry no student content')
            return True
        # AXIOM + DEDUCTION are common to all three types.
        if len(self.axiom) < 1:
            raise ValueError(f'Q{self.q}: AXIOM empty')
        for s in self.axiom:
            g(s)
        if len(self.deduction) < 2:
            raise ValueError(f'Q{self.q}: DEDUCTION needs >=2 steps')
        for s in self.deduction:
            g(s)
        if self.speed_hack is not None:
            if len(self.speed_hack) < 1:
                raise ValueError(f'Q{self.q}: SPEED HACK present but empty')
            for s in self.speed_hack:
                g(s)
        last = self.deduction[-1]
        opt_label = cfg.labels["option"]

        if self.qtype == 'nat':
            # NAT: no options, a typed value, value-bound deduction, common_pitfalls.
            if cfg.expected_options(self.q) not in (0, None):
                raise ValueError(f'Q{self.q}: NAT must have 0 expected options, '
                                 f'got {cfg.expected_options(self.q)}')
            if self.ca is None or str(self.ca).strip() == '':
                raise ValueError(f'Q{self.q}: NAT answer value missing')
            if str(self.ca) not in last:
                raise ValueError(f'Q{self.q}: DEDUCTION last step must contain the '
                                 f'answer value {str(self.ca)!r}')
            if self.why_wrong:
                raise ValueError(f'Q{self.q}: NAT uses common_pitfalls, not why_wrong')
            if len(self.common_pitfalls) < 1:
                raise ValueError(f'Q{self.q}: NAT needs >=1 common pitfall')
            for v, sents in self.common_pitfalls.items():
                if len(sents) < 1:
                    raise ValueError(f'Q{self.q}: common pitfall {v!r} empty')
                for s in sents:
                    g(s)
            if self.ca_range is not None:
                lo, hi = self.ca_range
                if not (lo <= hi):
                    raise ValueError(f'Q{self.q}: ca_range {self.ca_range} not lo<=hi')
            return True

        # MCQ / MSQ share the option machinery.
        n = cfg.expected_options(self.q)
        if not n or n < 1:
            raise ValueError(f'Q{self.q}: {self.qtype} needs >=1 option, expected={n}')
        if self.common_pitfalls:
            raise ValueError(f'Q{self.q}: {self.qtype} uses why_wrong, not common_pitfalls')
        sel = self.ca_set()
        if not sel or not sel <= set(range(1, n + 1)):
            raise ValueError(f'Q{self.q}: selected {sel} not a non-empty subset of 1..{n}')
        if self.qtype == 'mcq' and len(sel) != 1:
            raise ValueError(f'Q{self.q}: mcq must select exactly one option, got {sel}')
        # DEDUCTION last step must bind EVERY selected option (word-bounded label).
        for i in sorted(sel):
            lab = cfg.option_label(i)
            if not re.search(rf'\b{re.escape(opt_label)}\s+{re.escape(lab)}\b', last, re.I):
                raise ValueError(f'Q{self.q}: DEDUCTION last step must bind '
                                 f'{opt_label!r} {lab} (word-bounded)')
        # WHY WRONG: keys == exactly the NON-selected options.
        expected = set(range(1, n + 1)) - sel
        if set(self.why_wrong.keys()) != expected:
            raise ValueError(f'Q{self.q}: WHY WRONG keys {set(self.why_wrong)} '
                             f'!= wrong options {expected}')
        for k, sents in self.why_wrong.items():
            if len(sents) < 1:
                raise ValueError(f'Q{self.q}: WHY WRONG option {k} empty')
            for s in sents:
                g(s)
        return True

# ───────────────────────── paragraph construction ──────────────────────────
def _new_para(cfg, kind, text=None, runs=None, before=0, after=120,
              bold=False, color=None, math=True):
    """Create a standalone <w:p> element (not yet attached)."""
    p = OxmlElement('w:p')
    ppr = OxmlElement('w:pPr')
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(before)); sp.set(qn('w:after'), str(after))
    ppr.append(sp); p.append(ppr)
    # Wrap in a transient Paragraph proxy to reuse run helpers.
    from docx.text.paragraph import Paragraph
    proxy = Paragraph(p, None)
    if text is not None:
        if math:
            add_math_text(proxy, text, bold=bold, color=color, cfg=cfg)
        else:
            _run(proxy, text, bold=bold, color=color)
    return p

def _header_para(cfg, key, before=240, after=120):
    marker = cfg.markers.get(key, '')
    label = cfg.labels.get(key, key.upper())
    txt = f'{marker} {label}'.strip()
    return _new_para(cfg, 'hdr', text=txt, before=before, after=after,
                     bold=True, color=cfg.colors['hdr'], math=False)

def _block_paragraphs(cfg, blk):
    """Render one ExplanationBlock to an ordered list of <w:p> elements, shaped to
    the question type (mcq / msq / nat)."""
    out = []
    if blk.anomaly is not None:
        # Should never be written in Step 9 (halt-and-escalate); guarded here.
        raise ValueError(f'Q{blk.q}: anomaly must not be rendered in Step 9')
    ca_label = cfg.labels['correct_answer']
    opt_word = cfg.labels['option']
    # ── Correct Answer line (shaped by type; index/label only, no option text) ──
    if blk.qtype == 'nat':
        val = str(blk.ca)
        if blk.ca_range is not None:
            lo, hi = blk.ca_range
            val = f'{val} ({cfg.labels["accepted_range"]} {lo}\u2013{hi})'
        # math=True so a fractional answer renders as OMML
        out.append(_new_para(cfg, 'ca', text=f'{ca_label}: {val}', before=120,
                             after=120, bold=True, color=cfg.colors['ca'], math=True))
    else:
        disp = ', '.join(cfg.option_label(i) for i in sorted(blk.ca_set()))
        out.append(_new_para(cfg, 'ca', text=f'{ca_label}: {disp}', before=120,
                             after=120, bold=True, color=cfg.colors['ca'], math=False))
    out.append(_header_para(cfg, 'axiom'))
    for s in blk.axiom:
        out.append(_new_para(cfg, 'sent', text=s, before=0, after=120,
                             color=cfg.colors['sent']))
    out.append(_header_para(cfg, 'deduction'))
    for s in blk.deduction:
        out.append(_new_para(cfg, 'sent', text=s, before=0, after=120,
                             color=cfg.colors['sent']))
    if blk.speed_hack:
        out.append(_header_para(cfg, 'speed_hack'))
        for s in blk.speed_hack:
            out.append(_new_para(cfg, 'sent', text=s, before=0, after=120,
                                 color=cfg.colors['sent']))
    if blk.qtype == 'nat':
        # COMMON PITFALLS (wrong values), the NAT analogue of WHY WRONG
        out.append(_header_para(cfg, 'common_pitfalls'))
        for v in blk.common_pitfalls:
            out.append(_new_para(cfg, 'sub', text=str(v), before=160, after=40,
                                 bold=True, color=cfg.colors['sub'], math=True))
            for s in blk.common_pitfalls[v]:
                out.append(_new_para(cfg, 'sent', text=s, before=0, after=120,
                                     color=cfg.colors['sent']))
    else:
        out.append(_header_para(cfg, 'why_wrong'))
        for k in sorted(blk.why_wrong):
            out.append(_new_para(cfg, 'sub', text=f'{opt_word} {cfg.option_label(k)}',
                                 before=160, after=40, bold=True,
                                 color=cfg.colors['sub'], math=False))
            for s in blk.why_wrong[k]:
                out.append(_new_para(cfg, 'sent', text=s, before=0, after=120,
                                     color=cfg.colors['sent']))
    # trailing blank separator
    out.append(_new_para(cfg, 'blank', text=None, before=0, after=0))
    return out

# ───────────────────────────── paper parsing ───────────────────────────────
def parse_paper(path, cfg):
    """Read the Step-3 paper. Returns (doc, qmap) where qmap[q] = {
       'q_para': idx, 'opt_paras': [idx...], 'last_anchor': idx }.
    Validates: questions ascending+contiguous from 1, and each question carries the
    option count expected for it (cfg.expected_options(q) — a single uniform count,
    a per-section map, or 0 for NAT questions that have no options)."""
    doc = Document(path)
    paras = doc.paragraphs
    qmap = {}
    cur = None
    for i, p in enumerate(paras):
        t = p.text.strip()
        mq = cfg.q_re.match(t)
        if mq:
            cur = int(mq.group(1))
            qmap[cur] = {'q_para': i, 'opt_paras': [], 'last_anchor': i}
            continue
        if cur is not None and cfg.opt_re.match(t):
            qmap[cur]['opt_paras'].append(i)
            qmap[cur]['last_anchor'] = i
    if not qmap:
        raise ValueError('no questions matched q_re — check exam config')
    nums = sorted(qmap)
    if nums != list(range(1, len(nums) + 1)):
        raise ValueError(f'question numbers not contiguous from 1: {nums[:5]}...')
    for q in nums:
        oc = len(qmap[q]['opt_paras'])
        exp = cfg.expected_options(q)
        if exp is None:
            continue                      # no expectation supplied → skip count check
        if oc != exp:
            raise ValueError(f'Q{q} has {oc} options, expected {exp}')
    return doc, qmap

# ─────────────────────── interleaved (append-only) build ────────────────────
def build_interleaved_docx(source_path, blocks, out_path, cfg):
    """Seed the WHOLE source paper, then APPEND each block's paragraphs after that
    question's ENTIRE region — i.e. after the last body element (paragraph OR table)
    before the next question's stem (or end of document). Anchoring at the region
    end (not the last option label) is essential: figural questions place an option
    figure in a paragraph AFTER its 'N.' label, and DI questions end in a table —
    both must stay inside the question region, ahead of the appended explanation.
    Question regions are NEVER modified. Returns the count of questions explained."""
    # Validate the paper (option counts, contiguity) up front.
    parse_paper(source_path, cfg)
    doc = Document(source_path)
    body = doc.element.body
    children = [c for c in body.iterchildren()
                if c.tag in (qn('w:p'), qn('w:tbl'))]
    q_start = {}
    for idx, c in enumerate(children):
        if c.tag == qn('w:p'):
            txt = ''.join(t.text or '' for t in c.iter(qn('w:t'))).strip()
            mq = cfg.q_re.match(txt)
            if mq:
                q_start[int(mq.group(1))] = idx
    nums = sorted(q_start)
    by_q = {}
    for b in blocks:
        b.validate()
        by_q[b.q] = b
    for q, blk in by_q.items():
        if q not in q_start:
            raise ValueError(f'block for Q{q} but Q{q} not in paper')
        start = q_start[q]
        later = [q_start[n] for n in nums if q_start[n] > start]
        end = (min(later) - 1) if later else (len(children) - 1)
        cursor = children[end]               # last element of this question's region
        for pel in _block_paragraphs(cfg, blk):
            cursor.addnext(pel)
            cursor = pel
    doc.save(out_path)
    return len(by_q)

# ───────────────────────── content-fidelity verifier ───────────────────────
def _qregion_signature(path, cfg):
    """Per-question signature of the QUESTION REGION only (stem+options, in
    document order up to but excluding any appended Correct-Answer line):
       text lines, OMML <m:t> sequence, drawing count, table-cell grids."""
    doc = Document(path)
    body = doc.element.body
    ca_label = cfg.labels['correct_answer'].lower()
    sig = {}
    cur = None
    region = None
    def flush():
        if cur is not None:
            sig[cur] = region
    for child in body.iterchildren():
        tag = child.tag
        if tag == qn('w:p'):
            txt = ''.join(t.text or '' for t in child.iter(qn('w:t')))
            mt = [t.text or '' for t in child.iter(qn('m:t'))]
            ndraw = (len(child.findall('.//' + qn('w:drawing'))) +
                     len(child.findall('.//' + qn('w:pict'))))
            st = txt.strip()
            mq = cfg.q_re.match(st)
            if mq:
                flush()
                cur = int(mq.group(1)); region = {'lines': [], 'omml': [], 'draw': 0, 'tables': []}
            if cur is None:
                continue
            if st.lower().startswith(ca_label + ':'):
                # appended explanation begins → stop collecting this region
                # (mark closed by switching cur off until next question)
                flush(); cur = None; region = None
                continue
            region['lines'].append(txt)
            region['omml'].extend(mt)
            region['draw'] += ndraw
        elif tag == qn('w:tbl') and cur is not None and region is not None:
            grid = []
            for row in child.findall(qn('w:tr')):
                cells = []
                for cell in row.findall(qn('w:tc')):
                    cells.append(''.join(t.text or '' for t in cell.iter(qn('w:t'))))
                grid.append(cells)
            region['tables'].append(grid)
    flush()
    return sig

def _media_md5(path):
    import zipfile
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith('word/media/'):
                out[n] = hashlib.md5(z.read(n)).hexdigest()
    return out

def _rel_ids(path):
    """Set of relationship Ids declared in word/_rels/document.xml.rels."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        try:
            root = parse_xml(z.read('word/_rels/document.xml.rels'))
        except KeyError:
            return set()
    return {r.get('Id') for r in root if r.get('Id')}

def _embed_ids(path):
    """Every r:embed / r:id image reference in word/document.xml."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        root = parse_xml(z.read('word/document.xml'))
    ids = set()
    for el in root.iter():
        for a in (qn('r:embed'), qn('r:id'), qn('r:link')):
            v = el.get(a)
            if v:
                ids.add(v)
    return ids

def verify_fidelity(out_path, source_path, cfg):
    """Confirm every QUESTION REGION in the output is byte-identical to the
    source: stem/option text, OMML m:t sequence, drawing counts, table grids,
    that every source media part survives MD5-identical, and that every image
    relationship referenced in the body actually resolves (no dangling rId, A3).
    Returns (ok: bool, problems: list[str])."""
    problems = []
    src = _qregion_signature(source_path, cfg)
    got = _qregion_signature(out_path, cfg)
    def _rstrip_blanks(lines):
        out = list(lines)
        while out and not out[-1].strip():
            out.pop()
        return out
    for q in src:
        if q not in got:
            problems.append(f'Q{q}: region missing in output'); continue
        a, b = src[q], got[q]
        if _rstrip_blanks(a['lines']) != _rstrip_blanks(b['lines']):
            problems.append(f'Q{q}: stem/option text changed')
        if a['omml'] != b['omml']:
            problems.append(f'Q{q}: OMML math content changed')
        if a['draw'] != b['draw']:
            problems.append(f'Q{q}: drawing count changed {a["draw"]}->{b["draw"]}')
        if a['tables'] != b['tables']:
            problems.append(f'Q{q}: table cell grid changed')
    sm, gm = _media_md5(source_path), _media_md5(out_path)
    for n, h in sm.items():
        if gm.get(n) != h:
            problems.append(f'media {n}: MD5 changed or dropped')
    dangling = _embed_ids(out_path) - _rel_ids(out_path)
    if dangling:
        problems.append(f'dangling image relationship ids (no rel): {sorted(dangling)[:6]}')
    return (not problems), problems

# ───────────────────────── structure / coverage verifier ───────────────────
def verify_structure(out_path, blocks, cfg, expected_qs=None):
    """Confirm coverage and block integrity. Doc-level: every expected question
    carries a Correct-Answer line, and NO question outside expected_qs does (no
    look-ahead). Object-level: every expected block re-passes ExplanationBlock
    .validate() (header order, the CA three-way binding, WHY-WRONG key set), which
    — combined with the deterministic _block_paragraphs build — guarantees the
    written structure. Returns (ok: bool, problems: list[str])."""
    problems = []
    by_q = {b.q: b for b in blocks}
    if expected_qs is None:
        expected_qs = sorted(by_q)
    expected = set(expected_qs)
    doc = Document(out_path)
    paras = [p.text.strip() for p in doc.paragraphs]
    ca_label = cfg.labels['correct_answer'].lower()
    explained = set()
    cur = None
    for t in paras:
        mq = cfg.q_re.match(t)
        if mq:
            cur = int(mq.group(1)); continue
        if cur is not None and t.lower().startswith(ca_label + ':'):
            explained.add(cur)
    missing = expected - explained
    extra = explained - expected
    if missing:
        problems.append(f'missing explanations for {sorted(missing)}')
    if extra:
        problems.append(f'look-ahead: explained {sorted(extra)} beyond batch')
    # per-block structural re-validation (defence in depth)
    for q in sorted(expected):
        if q in by_q:
            try:
                by_q[q].validate()
            except ValueError as e:
                problems.append(str(e))
    return (not problems), problems

# ────────────────── post-render explanation audit (independent) ─────────────
def _para_mtext(p_el):
    return ''.join(t.text or '' for t in p_el.iter(qn('m:t')))

def verify_explanations(out_path, blocks, cfg, expected_qs=None):
    """Independent POST-RENDER audit (A2, parity with T2 verify_master 10-17): it
    re-parses the RENDERED docx — NOT the in-memory blocks — and re-checks the
    explanation region from the bytes that were actually written. Catches anything
    a build bug or future renderer change could let slip past the
    construction-time guards. Returns (ok, problems).

    Per question it confirms: header order AXIOM → DEDUCTION →
    (SPEED HACK) → WHY WRONG/COMMON PITFALLS; the last DEDUCTION line binds the
    answer (option / set / value, type-aware); WHY WRONG covers exactly the wrong options (mcq/msq)
    or COMMON PITFALLS the wrong values (nat); zero banned glyphs/metacommentary/
    templates/fake-cites/banned-blocks and zero inline or vulgar fractions in the
    rendered prose; one sentence per rendered prose paragraph. Document-wide it
    confirms every OMML fraction has a non-empty numerator AND denominator and that
    no fraction is a consecutive-year artifact."""
    problems = []
    by_q = {b.q: b for b in blocks}
    if expected_qs is None:
        expected_qs = sorted(by_q)
    expected = sorted(set(expected_qs))
    doc = Document(out_path)

    ca_label = cfg.labels['correct_answer']
    opt_word = cfg.labels['option']
    H = {k: f"{cfg.markers.get(k, '')} {cfg.labels.get(k, k)}".strip()
         for k in ('axiom', 'deduction', 'speed_hack', 'why_wrong', 'common_pitfalls')}
    HEADERS = set(H.values())

    # segment rendered paragraphs into per-question explanation line lists
    segs = {}
    cur = None
    in_expl = False
    for p in doc.paragraphs:
        t = p.text.strip()
        if cfg.q_re.match(t):
            cur = int(cfg.q_re.match(t).group(1)); in_expl = False; continue
        if cur is None:
            continue
        if t.startswith(ca_label + ':'):
            in_expl = True; segs[cur] = []; continue
        if in_expl:
            _s = _para_source(p._p, cur, strict=False).strip()
            if t or _s:                          # keep OMML-only paras (fraction value headers)
                segs[cur].append((t, _para_mtext(p._p), _s))

    for q in expected:
        b = by_q.get(q)
        if q not in segs:
            problems.append(f'Q{q}: no rendered explanation found'); continue
        lines = segs[q]
        texts = [t for t, _, _ in lines]
        srcs = [s for _, _, s in lines]
        seq = [t for t in texts if t in HEADERS]
        # 1. header order (SPEED HACK is positional/optional; core = the rest)
        core = [h for h in seq if h != H['speed_hack']]
        wrong_hdr = H['common_pitfalls'] if (b and b.qtype == 'nat') else H['why_wrong']
        if core != [H['axiom'], H['deduction'], wrong_hdr]:
            problems.append(f'Q{q}: header order/presence wrong: {core}')
        # 2. DEDUCTION last line binds the answer (type-aware), read from render
        if H['deduction'] in texts:
            di = texts.index(H['deduction'])
            stops = [i for i, t in enumerate(texts)
                     if i > di and t in (H['speed_hack'], wrong_hdr)]
            last_i = (stops[0] - 1) if stops else len(texts) - 1
            last = texts[last_i] if last_i > di else ''
            last_src = srcs[last_i] if last_i > di else ''
            if b is not None:
                if b.qtype == 'nat':
                    if str(b.ca) not in last_src:
                        problems.append(f'Q{q}: DEDUCTION last line does not bind value {b.ca!r}')
                else:
                    need = [f'{opt_word} {cfg.option_label(i)}' for i in sorted(b.ca_set())]
                    miss = [n for n in need if not re.search(rf'{re.escape(n)}\b', last)]
                    if miss:
                        problems.append(f'Q{q}: DEDUCTION last line missing binding {miss}')
        # 3. wrong-section coverage from render
        if b is not None:
            if b.qtype == 'nat':
                subs = {s for s in srcs if s in {str(v) for v in b.common_pitfalls}}
                if subs != {str(v) for v in b.common_pitfalls}:
                    problems.append(f'Q{q}: COMMON PITFALLS render coverage mismatch')
            else:
                subs = set()
                for t in texts:
                    mo = re.match(rf'^{re.escape(opt_word)}\s+(\S+)', t)
                    if mo and t not in HEADERS:
                        subs.add(mo.group(1))
                need = {cfg.option_label(k) for k in b.why_wrong}
                if subs != need:
                    problems.append(f'Q{q}: WHY WRONG render coverage {sorted(subs)} != {sorted(need)}')
        # 4. prose guards on rendered sentence lines (exclude headers + sub-headers)
        sub_pat = re.compile(rf'^{re.escape(opt_word)}\s+\S')
        nat_keys = {str(v) for v in (b.common_pitfalls if b else {})}
        for t, _mt, _s in lines:
            if t in HEADERS or sub_pat.match(t) or _s in nat_keys or not t:
                continue
            for g in _BANNED_GLYPHS:
                if g in t:
                    problems.append(f'Q{q}: rendered banned glyph {g!r}')
            for v in VULGAR:
                if v in t:
                    problems.append(f'Q{q}: rendered vulgar fraction {v!r}')
            lw = t.lower()
            meta_re = cfg.metacommentary_re if hasattr(cfg, 'metacommentary_re') else _META_RE
            b_templates = cfg.banned_templates if hasattr(cfg, 'banned_templates') else _BANNED_TEMPLATE
            b_fakecites = cfg.banned_fakecites if hasattr(cfg, 'banned_fakecites') else _BANNED_FAKECITE
            if meta_re.search(t) or any(x in lw for x in b_templates) \
               or any(x in lw for x in b_fakecites):
                problems.append(f'Q{q}: rendered banned phrase in {t[:40]!r}')
            if has_inline_fraction(t):
                problems.append(f'Q{q}: rendered inline fraction in {t[:40]!r}')
            if sentence_count(t, cfg.sentence_terminators) != 1:
                problems.append(f'Q{q}: rendered multi-sentence paragraph {t[:40]!r}')

    # 5. document-wide OMML fraction well-formedness + year-range artifact
    import zipfile
    root = parse_xml(zipfile.ZipFile(out_path).read('word/document.xml'))
    for f in root.iter(qn('m:f')):
        num = f.find(qn('m:num')); den = f.find(qn('m:den'))
        nt = ''.join(num.itertext()) if num is not None else ''
        dt = ''.join(den.itertext()) if den is not None else ''
        if not nt.strip() or not dt.strip():
            problems.append(f'malformed OMML fraction (empty num/den): {nt!r}/{dt!r}')
        elif _year_range_hit(f'{nt}/{dt}'):
            problems.append(f'year-range rendered as OMML fraction: {nt}/{dt}')
    return (not problems), problems

# ───────────────────────────── strip for re-audit ──────────────────────────
def strip_solutions(out_path, stripped_path, cfg):
    """Produce a questions-only copy (every appended explanation paragraph
    removed) so the Step-2 paper auditor sees ONLY the paper (Conflict-3)."""
    doc = Document(out_path)
    body = doc.element.body
    ca_label = cfg.labels['correct_answer'].lower()
    in_expl = False
    to_remove = []
    for child in list(body.iterchildren()):
        if child.tag == qn('w:p'):
            txt = ''.join(t.text or '' for t in child.iter(qn('w:t'))).strip()
            if cfg.q_re.match(txt):
                in_expl = False
            elif txt.lower().startswith(ca_label + ':'):
                in_expl = True
            if in_expl:
                to_remove.append(child)
        elif child.tag == qn('w:tbl') and in_expl:
            to_remove.append(child)
    for el in to_remove:
        el.getparent().remove(el)
    doc.save(stripped_path)
    return stripped_path

# ───────────────────────────── self-test ───────────────────────────────────
def _tiny_png():
    """Minimal valid 1x1 PNG (no external deps)."""
    import struct, zlib, io
    sig = b'\x89PNG\r\n\x1a\n'
    def chunk(typ, data):
        return (struct.pack('>I', len(data)) + typ + data +
                struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff))
    ihdr = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    idat = zlib.compress(b'\x00\xff\x00\x00')        # one red pixel row
    return io.BytesIO(sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b''))

def _make_sample_paper(path, cfg, nq=6):
    """Build a synthetic paper that EXERCISES the hard fidelity cases:
       Q2 carries an option figure in a paragraph AFTER its last option label
       (the anchor-bug case), and Q4 ends its region with a table (DI case)."""
    from docx.shared import Inches
    doc = Document()
    for q in range(1, nq + 1):
        doc.add_paragraph(f'Q.{q}  Sample stem number {q}.')
        for o in range(1, cfg.options_count + 1):
            doc.add_paragraph(f'{o}.  opt{o}')
        if q == 2:
            doc.add_paragraph().add_run().add_picture(_tiny_png(), width=Inches(0.3))
        if q == 4:
            t = doc.add_table(rows=2, cols=2)
            t.cell(0, 0).text = 'a'; t.cell(0, 1).text = 'b'
            t.cell(1, 0).text = 'c'; t.cell(1, 1).text = 'd'
        doc.add_paragraph('')
    doc.save(path)
    return path

def self_test():
    results = []
    def check(name, cond):
        results.append((name, bool(cond)))
    def _raises(fn):
        try:
            fn(); return False
        except ValueError:
            return True
    cfg = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)

    # 1 guard: banned glyph
    try: guard_sentence('value is 21 \u2713'); check('G-GLYPH', False)
    except ValueError: check('G-GLYPH', True)
    # 2 guard: LaTeX
    try: guard_sentence('use \\frac here'); check('G-LATEX', False)
    except ValueError: check('G-LATEX', True)
    # 3 guard: metacommentary
    try: guard_sentence('wait, let me reconsider this'); check('G-META', False)
    except ValueError: check('G-META', True)
    # 4 guard: template sentence
    try: guard_sentence('This option is wrong here'); check('G-TEMPLATE', False)
    except ValueError: check('G-TEMPLATE', True)
    # 5 guard: fake citation
    try: guard_sentence('per the official key it is 3'); check('G-FAKECITE', False)
    except ValueError: check('G-FAKECITE', True)
    # 6 guard: two sentences
    try: guard_sentence('First fact. Second fact.'); check('G-2SENT', False)
    except ValueError: check('G-2SENT', True)
    # 7 guard: one sentence OK
    try: check('G-1SENT', bool(guard_sentence('A single clean factual sentence here.')))
    except ValueError: check('G-1SENT', False)
    # 8 guard: year-range slash
    try: guard_sentence('in 2025/26 the budget rose.'); check('G-YEAR', False)
    except ValueError: check('G-YEAR', True)
    # 9 units are NOT fractions
    check('G-UNIT', not has_inline_fraction('speed is 60 km/h here'))
    # 10 inline fraction detected
    check('G-INLINEFRAC', has_inline_fraction('value 3/4 remains'))
    # 11 add_math_text converts a fraction without raising
    from docx.text.paragraph import Paragraph
    p = OxmlElement('w:p'); proxy = Paragraph(p, None)
    add_math_text(proxy, 'the share is 2/3 of total.')
    check('G-OMMLCONV', len(p.findall('.//' + qn('m:oMath'))) == 1)
    # 12 end-of-sentence fraction raises (EX13)
    try:
        p2 = OxmlElement('w:p'); add_math_text(Paragraph(p2, None), 'result = 3/4.')
        check('G-ENDFRAC', False)
    except ValueError: check('G-ENDFRAC', True)
    # 13 ExplanationBlock validates a good block
    good = ExplanationBlock(q=1, ca=1,
        axiom=['The sum of a group equals its average times its count.'],
        deduction=['Total is 9 times 43 = 387.',
                   'Remaining average is 235 over 5 = 47, which is Option 1.'],
        why_wrong={2: ['Option 2 uses 12 not 13 (off_by_one).'],
                   3: ['Option 3 shifts by four not three (off_by_one).'],
                   4: ['Option 4 drops the letter rule (partial_truth).']},
        cfg=cfg)
    check('B-VALID', good.validate())
    # 14 DEDUCTION must bind Option N
    try:
        bad = ExplanationBlock(q=1, ca=1, axiom=['x.'],
            deduction=['step one.', 'step two without binding.'],
            why_wrong={2:['a.'],3:['b.'],4:['c.']}, cfg=cfg); bad.validate()
        check('B-BIND', False)
    except ValueError: check('B-BIND', True)
    # 15 WHY WRONG keys must equal wrong options
    try:
        bad = ExplanationBlock(q=1, ca=1, axiom=['x.'],
            deduction=['s.', 'final is Option 1.'],
            why_wrong={2:['a.'],3:['b.']}, cfg=cfg); bad.validate()
        check('B-WWKEYS', False)
    except ValueError: check('B-WWKEYS', True)
    # 16 build + fidelity + structure round-trip (Q2 has a trailing option figure,
    #    Q4 ends in a table — both must survive byte-identical)
    import tempfile, os
    d = tempfile.mkdtemp()
    src = os.path.join(d, 'paper.docx'); out = os.path.join(d, 'sol.docx')
    _make_sample_paper(src, cfg, nq=6)
    blocks = []
    for q in range(1, 5):  # batch 1 = Q1..Q4 (covers the figure + table cases)
        blocks.append(ExplanationBlock(q=q, ca=1,
            axiom=['A reusable principle stated as a truth here.'],
            deduction=['First derived step gives a value.',
                       f'Final value maps to Option 1 for question {q}.'],
            speed_hack=['A genuinely shorter elimination route here.'],
            why_wrong={2:['Option 2 swaps a value (value_swap).'],
                       3:['Option 3 mis-signs a term (sign_error).'],
                       4:['Option 4 covers only part (partial_truth).']},
            cfg=cfg))
    n = build_interleaved_docx(src, blocks, out, cfg)
    check('BUILD-N', n == 4)
    okf, pf = verify_fidelity(out, src, cfg)
    check('FIDELITY', okf)
    oks, ps = verify_structure(out, blocks, cfg, expected_qs=[1, 2, 3, 4])
    check('STRUCT', oks)
    # 17 look-ahead is caught: claim batch is only Q1..Q3 but doc has Q4 explained
    okl, pl = verify_structure(out, blocks, cfg, expected_qs=[1, 2, 3])
    check('NO-LOOKAHEAD', (not okl))
    # 18 strip_solutions removes explanations (questions-only copy parses clean)
    stripped = os.path.join(d, 'stripped.docx')
    strip_solutions(out, stripped, cfg)
    _, qmap = parse_paper(stripped, cfg)
    check('STRIP', len(qmap) == 6 and all(len(qmap[q]['opt_paras']) == 4 for q in qmap))

    # ── edge-case guards (added after a forensic audit) ──────────────────────
    # 19 meta false-positives are GONE: 'ohmmeter'/'await'/'factually'/'air' pass
    def _passes(t):
        try: guard_sentence(t); return True
        except ValueError: return False
    check('G-META-FP', all(_passes(t) for t in [
        'The ohmmeter reads two ohms across the resistor here.',
        'Candidates await, then the second method confirms it.',
        'The statement is factually, not morally, the weaker claim.',
        'The curve has an air of symmetry about the origin here.']))
    # 20 fake-citation guard is EXAM-AGNOSTIC: a former hardcoded token now passes,
    #    while a generic fabricated-authority phrase is still caught
    check('G-NOEXAM', _passes('The SSC pattern places this topic in the first section.')
          and not _passes('The official answer key says the value is three here.'))
    # 21 CA binding is word-bounded: 12 options, ca=1 binds 'Option 1' (not 'Option 10')
    cfg12 = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9]|1[0-2])[.\)]', 12)
    okbind = ExplanationBlock(q=1, ca=1, cfg=cfg12,
        axiom=['A principle stated as a truth here.'],
        deduction=['Eliminating Option 10 and Option 11 narrows the field.',
                   'Only the first choice survives, which is Option 1.'],
        why_wrong={k: [f'Option {k} fails one condition (partial_truth).']
                   for k in range(2, 13)}).validate()
    check('B-BIND-WB-OK', okbind)
    def _bind_bad():
        try:
            ExplanationBlock(q=1, ca=1, cfg=cfg12,
                axiom=['A principle stated as a truth here.'],
                deduction=['A first step yields a value.',
                           'The survivor is Option 10 only here.'],   # ca=1 but binds Option 10
                why_wrong={k: [f'Option {k} fails one condition (partial_truth).']
                           for k in range(2, 13)}).validate()
            return False
        except ValueError:
            return True
    check('B-BIND-WB-FAIL', _bind_bad())
    # 22 five-option config builds + validates + round-trips fidelity
    cfg5 = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-5])[.\)]', 5)
    d5 = tempfile.mkdtemp(); s5 = os.path.join(d5, 'p.docx'); o5 = os.path.join(d5, 's.docx')
    _make_sample_paper(s5, cfg5, nq=3)
    b5 = [ExplanationBlock(q=q, ca=2, cfg=cfg5,
        axiom=['A principle stated as a truth here.'],
        deduction=['A first step yields a value.', f'The value maps to Option 2 for item {q}.'],
        why_wrong={1:['Option 1 swaps a value (value_swap).'],
                   3:['Option 3 mis-signs a term (sign_error).'],
                   4:['Option 4 covers only part (partial_truth).'],
                   5:['Option 5 rounds wrongly (rounding_trap).']}) for q in [1, 2]]
    n5 = build_interleaved_docx(s5, b5, o5, cfg5)
    okf5, _ = verify_fidelity(o5, s5, cfg5)
    oks5, _ = verify_structure(o5, b5, cfg5, expected_qs=[1, 2])
    check('CFG-5OPT', n5 == 2 and okf5 and oks5)
    # 23 non-English labels flow through build AND coverage detection
    hi = {'correct_answer': '\u0938\u0939\u0940 \u0909\u0924\u094d\u0924\u0930',
          'axiom': 'AXIOM', 'deduction': 'DEDUCTION', 'speed_hack': 'SPEED HACK',
          'why_wrong': 'WHY WRONG?', 'option': 'Option', 'solution_ref': 'Solution'}
    cfgL = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4, labels=hi)
    dL = tempfile.mkdtemp(); sL = os.path.join(dL, 'p.docx'); oL = os.path.join(dL, 's.docx')
    _make_sample_paper(sL, cfgL, nq=2)
    bL = [ExplanationBlock(q=1, ca=1, cfg=cfgL,
        axiom=['A principle stated as a truth here.'],
        deduction=['A first step yields a value.', 'The value maps to Option 1 here.'],
        why_wrong={2:['Option 2 swaps a value (value_swap).'],
                   3:['Option 3 mis-signs a term (sign_error).'],
                   4:['Option 4 covers only part (partial_truth).']})]
    build_interleaved_docx(sL, bL, oL, cfgL)
    oksL, _ = verify_structure(oL, bL, cfgL, expected_qs=[1])
    okfL, _ = verify_fidelity(oL, sL, cfgL)
    check('CFG-LABELS', oksL and okfL)
    # 24 an anomaly (escalation) block validates but MUST NOT render/ship
    anom = ExplanationBlock(q=1, anomaly='no single defensible answer', cfg=cfg)
    anom_ok = anom.validate()
    def _anom_blocked():
        try:
            build_interleaved_docx(src, [anom], os.path.join(d, 'x.docx'), cfg)
            return False
        except ValueError:
            return True
    check('ANOMALY-NORENDER', anom_ok and _anom_blocked())
    # 25 alternate question/option format parses (Q1. stem, (1) option)
    cfgA = EngineConfig(r'^Q(\d+)\.', r'^\(([1-9])\)', 4)
    dA = tempfile.mkdtemp(); sA = os.path.join(dA, 'p.docx')
    docA = Document()
    for q in range(1, 4):
        docA.add_paragraph(f'Q{q}. stem {q}')
        for o in range(1, 5):
            docA.add_paragraph(f'({o}) opt{o}')
        docA.add_paragraph('')
    docA.save(sA)
    _, qmA = parse_paper(sA, cfgA)
    check('CFG-ALTFMT', len(qmA) == 3 and all(len(qmA[q]['opt_paras']) == 4 for q in qmA))

    # ── NAT / MSQ / mixed-section / label-scheme / terminator tests ──────────
    # 26 NAT: a question with NO options; value answer; value-bound deduction;
    #    common pitfalls instead of why_wrong; parse allows 0 options
    cfgN = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', None,
                        options_by_q={1: 0, 2: 0})
    dN = tempfile.mkdtemp(); sN = os.path.join(dN, 'p.docx'); oN = os.path.join(dN, 's.docx')
    docN = Document()
    for q in [1, 2]:
        docN.add_paragraph(f'Q.{q} compute the numerical value and enter it')
        docN.add_paragraph('')                       # NO options
    docN.save(sN)
    _, qmN = parse_paper(sN, cfgN)
    natblk = ExplanationBlock(q=1, ca='47', cfg=cfgN, ca_range=(46.5, 47.5),
        axiom=['The mean equals the total over the count here.'],
        deduction=['The total is 235 over a count of five.',
                   'Dividing gives the value 47 as the answer.'],
        common_pitfalls={'235': ['Forgetting to divide leaves 235 (process_confusion).'],
                         '9.4': ['Dividing by the wrong count gives 9.4 (value_swap).']})
    nat_ok = natblk.validate()
    nN = build_interleaved_docx(sN, [natblk], oN, cfgN)
    okfN, _ = verify_fidelity(oN, sN, cfgN)
    oksN, _ = verify_structure(oN, [natblk], cfgN, expected_qs=[1])
    # NAT CA line shows the VALUE (not an option index)
    docNo = Document(oN)
    ca_line_ok = any(p.text.strip().startswith('Correct Answer: 47') for p in docNo.paragraphs)
    check('NAT', nat_ok and nN == 1 and okfN and oksN and ca_line_ok)

    # 26b STR-KEYED options_by_q (registry.json boundary): keys arriving as JSON strings
    #     must resolve identically to int keys. Regression lock for the str/int ND6 fix —
    #     a NAT question (0) keyed "3" must still type as nat when queried with int 3.
    cfgS = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4,
                        options_by_q={'1': 4, '2': 4, '3': 0})       # STRING keys
    check('NAT-STRKEY', cfgS.expected_options(3) == 0
                        and cfgS.expected_options(1) == 4
                        and cfgS.expected_options(2) == 4)
    # 27 NAT rejects option-style why_wrong and an unbound value
    def _nat_bad():
        try:
            ExplanationBlock(q=1, ca='47', cfg=cfgN,
                axiom=['x truth here.'], deduction=['a.', 'b.'],
                why_wrong={2: ['no.']}).validate()           # why_wrong illegal for NAT
            return False
        except ValueError:
            try:
                ExplanationBlock(q=1, ca='47', cfg=cfgN, axiom=['x truth here.'],
                    deduction=['a.', 'final value is 99 here.'],   # 47 not bound
                    common_pitfalls={'5': ['p.']}).validate()
                return False
            except ValueError:
                return True
    check('NAT-GUARDS', _nat_bad())
    # 28 MSQ: multiple correct; ca is a set; last step binds all selected;
    #    why_wrong = the non-selected options
    cfgM = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
    dM = tempfile.mkdtemp(); sM = os.path.join(dM, 'p.docx'); oM = os.path.join(dM, 's.docx')
    _make_sample_paper(sM, cfgM, nq=2)
    msq = ExplanationBlock(q=1, ca={1, 3}, cfg=cfgM, qtype='msq',
        axiom=['Each statement is judged independently here.'],
        deduction=['Statement one holds and statement three holds.',
                   'The correct set is Option 1 and Option 3 here.'],
        why_wrong={2: ['Option 2 fails one condition (partial_truth).'],
                   4: ['Option 4 inverts the relation (reversed_relationship).']})
    msq_ok = msq.validate()
    nM = build_interleaved_docx(sM, [msq], oM, cfgM)
    okfM, _ = verify_fidelity(oM, sM, cfgM)
    oksM, _ = verify_structure(oM, [msq], cfgM, expected_qs=[1])
    docMo = Document(oM)
    msq_ca_ok = any(p.text.strip() == 'Correct Answer: 1, 3' for p in docMo.paragraphs)
    check('MSQ', msq_ok and nM == 1 and okfM and oksM and msq_ca_ok)
    # 29 MSQ rejects: last step not binding all selected; wrong why_wrong keys
    def _msq_bad():
        try:
            ExplanationBlock(q=1, ca={1, 3}, cfg=cfgM, qtype='msq',
                axiom=['x truth here.'],
                deduction=['a.', 'only Option 1 here.'],      # Option 3 not bound
                why_wrong={2: ['p.'], 4: ['q.']}).validate()
            return False
        except ValueError:
            try:
                ExplanationBlock(q=1, ca={1, 3}, cfg=cfgM, qtype='msq',
                    axiom=['x truth here.'],
                    deduction=['a.', 'set is Option 1 and Option 3 here.'],
                    why_wrong={2: ['p.']}).validate()         # missing key 4
                return False
            except ValueError:
                return True
    check('MSQ-GUARDS', _msq_bad())
    # 30 mixed-section option counts: Q1 has 4, Q2 has 5 — passes with the map,
    #    and the same paper FAILS under a single uniform count
    cfgX = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', None,
                        options_by_q={1: 4, 2: 5})
    dX = tempfile.mkdtemp(); sX = os.path.join(dX, 'p.docx')
    docX = Document()
    docX.add_paragraph('Q.1 stem'); [docX.add_paragraph(f'{o}. o') for o in range(1, 5)]; docX.add_paragraph('')
    docX.add_paragraph('Q.2 stem'); [docX.add_paragraph(f'{o}. o') for o in range(1, 6)]; docX.add_paragraph('')
    docX.save(sX)
    mix_ok = False
    try:
        parse_paper(sX, cfgX); mix_ok = True
    except ValueError:
        mix_ok = False
    uni_fail = False
    try:
        parse_paper(sX, EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4))
    except ValueError:
        uni_fail = True
    check('MIXED-OPTS', mix_ok and uni_fail)
    # 31 alphabetic option labels: CA line + Option refs show A/B/C/D
    cfgAl = EngineConfig(r'^Q\.?\s*(\d+)', r'^([A-D])[.\)]', 4, label_scheme='alpha_upper')
    dAl = tempfile.mkdtemp(); sAl = os.path.join(dAl, 'p.docx'); oAl = os.path.join(dAl, 's.docx')
    docAl = Document()
    docAl.add_paragraph('Q.1 stem')
    for L in ['A', 'B', 'C', 'D']:
        docAl.add_paragraph(f'{L}. choice')
    docAl.add_paragraph(''); docAl.save(sAl)
    albl = ExplanationBlock(q=1, ca=1, cfg=cfgAl,
        axiom=['A principle stated as a truth here.'],
        deduction=['A first step yields a value.', 'The value maps to Option A here.'],
        why_wrong={2: ['Option B swaps a value (value_swap).'],
                   3: ['Option C mis-signs a term (sign_error).'],
                   4: ['Option D covers only part (partial_truth).']})
    al_ok = albl.validate()
    build_interleaved_docx(sAl, [albl], oAl, cfgAl)
    docAlo = Document(oAl)
    alpha_ca = any(p.text.strip() == 'Correct Answer: A' for p in docAlo.paragraphs)
    alpha_sub = any(p.text.strip() == 'Option B' for p in docAlo.paragraphs)
    check('LABEL-ALPHA', al_ok and alpha_ca and alpha_sub)
    # 32 Devanagari sentence terminator (danda): a 3-sentence paragraph now FAILS
    cfgHi = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4,
                         sentence_terminators='.!?\u0964\u0965')
    three = '\u092a\u0939\u0932\u093e\u0964 \u0926\u0942\u0938\u0930\u093e\u0964 \u0924\u0940\u0938\u0930\u093e\u0964'
    danda_caught = False
    try:
        guard_sentence(three, cfgHi)
    except ValueError:
        danda_caught = True
    danda_default_misses = (sentence_count(three) == 1)   # default '.!?' misses danda
    check('TERMINATOR-DANDA', danda_caught and danda_default_misses)
    # 33 OMML helpers all produce well-formed math nodes (the author-facing API)
    omml_ok = True
    for x in (sup('x', '2'), sqrt('2'), nary('\u2211', 'i', 'n', 'i'), _r('5'),
              frac('1', '2'), omath(frac('1', '2'))):
        try:
            parse_xml(x)
        except Exception:
            omml_ok = False
    check('OMML-HELPERS', omml_ok)
    # 34 figural question: NO FIGURE section is rendered (removed by design), yet
    #    the image inside the question region survives byte-identical and the
    #    post-render audit passes. Regression-lock for the FIGURE-section removal.
    cfgF = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
    dF = tempfile.mkdtemp(); sF = os.path.join(dF, 'p.docx'); oF = os.path.join(dF, 's.docx')
    docF = Document()
    docF.add_paragraph('Q.1 which figure continues the series')
    from docx.shared import Inches
    docF.add_paragraph().add_run().add_picture(_tiny_png(), width=Inches(0.3))
    for o in range(1, 5):
        docF.add_paragraph(f'{o}. figure')
    docF.add_paragraph(''); docF.save(sF)
    figblk = ExplanationBlock(q=1, ca=1, cfg=cfgF,
        axiom=['A figural series applies one fixed transformation at every step.'],
        deduction=['Tracing the rotation forward predicts the next figure.',
                   'That predicted figure matches Option 1 here.'],
        why_wrong={2:['Option 2 rotates the wrong way (reversed_relationship).'],
                   3:['Option 3 over-rotates by one step (off_by_one).'],
                   4:['Option 4 changes the wrong element (process_confusion).']})
    figblk.validate()
    build_interleaved_docx(sF, [figblk], oF, cfgF)
    okfF, _ = verify_fidelity(oF, sF, cfgF)                 # question-region image preserved
    fig_paras = [p.text.strip() for p in Document(oF).paragraphs]
    no_figure_section = not any('FIGURE' in t for t in fig_paras)   # section fully gone
    okeF, _ = verify_explanations(oF, [figblk], cfgF)       # audit passes with no FIGURE header
    check('FIGURAL-NO-FIGURE-SECTION', okfF and no_figure_section and okeF)
    # 35 vulgar-fraction glyphs and U+2044 are rejected (A1)
    vulgar_caught = all(_raises(lambda s=s: guard_sentence(s))
                        for s in ('The share is \u00bd of the total here.',
                                  'About \u2154 of the class passed today.',
                                  'The ratio 3\u20444 appears in the stem here.'))
    check('VULGAR-FRACTION', vulgar_caught and has_inline_fraction('a \u00bd here'))
    # 36 wider inline-fraction forms (1/x, x²/2, (a+b)/c) are caught; units still pass (A4)
    wide = (has_inline_fraction('the term 1/x grows here')
            and has_inline_fraction('x\u00b2/2 is the area here')
            and has_inline_fraction('(a+b)/c equals the mean')
            and not has_inline_fraction('the speed is 60 km/h here'))
    check('WIDE-FRACTION', wide)
    # 37 year-range precision: 2024/25 flagged, genuine n/(n+1) like 2024/26 NOT (A6)
    yr = (_year_range_hit('growth in 2024/25 was steady') is not None
          and _year_range_hit('the fraction 2024/26 reduces') is None)
    check('YEAR-RANGE-PRECISION', yr)
    # 38 richer sentence counter: abbreviations / acronyms / initials stay one sentence (A5)
    one = (sentence_count('Govt. data shows the approx. value here.') == 1
           and sentence_count('The meeting is at 10 a.m. sharp today.') == 1
           and sentence_count('C. V. Raman won the prize in physics.') == 1
           and sentence_count('First fact here. Second fact here.') == 2)
    check('SENTENCE-COUNTER', one)
    # 39 post-render audit passes a clean build and CATCHES a tampered explanation (A2)
    cfgP = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
    dP = tempfile.mkdtemp(); sP = os.path.join(dP, 'p.docx'); oP = os.path.join(dP, 's.docx')
    dpz = Document(); dpz.add_paragraph('Q.1 stem')
    for o in range(1, 5):
        dpz.add_paragraph(f'{o}. opt')
    dpz.add_paragraph(''); dpz.save(sP)
    pblk = ExplanationBlock(q=1, ca=1, cfg=cfgP,
        axiom=['A truth with its reason stated here.'],
        deduction=['A first step yields a value here.', 'That value is Option 1 here.'],
        why_wrong={2: ['Option 2 swaps a value (value_swap).'],
                   3: ['Option 3 mis-signs a term (sign_error).'],
                   4: ['Option 4 covers only part (partial_truth).']})
    build_interleaved_docx(sP, [pblk], oP, cfgP)
    clean_ok, _ = verify_explanations(oP, [pblk], cfgP)
    # tamper: inject a banned glyph into a rendered explanation paragraph
    dtam = Document(oP)
    for p in dtam.paragraphs:
        if p.text.strip().startswith('A first step'):
            if p.runs:
                p.runs[0].text = p.runs[0].text + ' \u2713'
            break
    tP = os.path.join(dP, 't.docx'); dtam.save(tP)
    tam_caught, _ = verify_explanations(tP, [pblk], cfgP)
    check('POST-RENDER-AUDIT', clean_ok and not tam_caught)
    # 40 rels resolution: clean build has no dangling image rIds (A3)
    okrel, _ = verify_fidelity(oF, sF, cfgF)
    check('RELS-RESOLVE', okrel and not (_embed_ids(oF) - _rel_ids(oF)))

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        if not ok:
            print(f'  FAIL: {name}')
    print(f'SELF-TEST: {passed}/{total} PASS')
    return passed == total


# ══════════════════════════════════════════════════════════════════════════════
# STEP-10 ADDITION (MockExplainAudit) — the docx→ExplanationBlock reader.
# Additive: no existing write/verify path changes; --self-test stays 44/44. The
# EXACT INVERSE of _block_paragraphs, driven by the SAME cfg, so a rectified block
# is structurally identical to how Step 9 would have written it correctly.
# ══════════════════════════════════════════════════════════════════════════════
def _omml_to_source(node, q, strict=True):
    """SOURCE-TEXT form of one OMML child. Explanation prose only contains
    digit/digit fractions (add_math_text is the sole writer), so m:f -> 'num/den'
    round-trips exactly. strict=True (the READER): any other OMML structure RAISES
    (never silently degrade). strict=False (the VERIFIER): unknown OMML degrades to
    its m:t text so a post-render audit never crashes on an unexpected node."""
    tag = node.tag
    if tag == qn('m:r'):
        return ''.join(t.text or '' for t in node.iter(qn('m:t')))
    if tag == qn('m:f'):
        num = node.find(qn('m:num')); den = node.find(qn('m:den'))
        nt = ''.join(num.itertext()) if num is not None else ''
        dt = ''.join(den.itertext()) if den is not None else ''
        return f'{nt}/{dt}'
    if strict:
        raise ValueError(f'Q{q}: unexpected OMML {tag} in explanation prose — reader '
                         f'supports digit/digit fractions only (halt, do not degrade)')
    return ''.join(t.text or '' for t in node.iter(qn('m:t')))

def _para_source(p_el, q, strict=True):
    """Rebuild the source string add_math_text was given: text runs verbatim,
    m:f as 'num/den', in document order. strict is passed to _omml_to_source."""
    out = []
    for child in p_el:
        tag = child.tag
        if tag == qn('w:pPr'):
            continue
        if tag == qn('w:r'):
            out.append(''.join(t.text or '' for t in child.iter(qn('w:t'))))
        elif tag == qn('m:oMath'):
            for m in child:
                out.append(_omml_to_source(m, q, strict))
        else:
            out.append(''.join(t.text or '' for t in child.iter(qn('w:t'))))
    return ''.join(out)

def _label_to_index(cfg, n):
    """Inverse of cfg.option_label over 1..n."""
    return {cfg.option_label(i): i for i in range(1, n + 1)}

def _para_spacing(p_el):
    """(before, after) twips from the paragraph's spacing, or None if not present."""
    pr = p_el.find(qn('w:pPr'))
    sp = pr.find(qn('w:spacing')) if pr is not None else None
    if sp is None:
        return None
    b, a = sp.get(qn('w:before')), sp.get(qn('w:after'))
    try:
        return (int(b), int(a)) if (b is not None and a is not None) else None
    except ValueError:
        return None

def _is_subheader(p_el, terminators='.!?'):
    """True if the paragraph is a rendered sub-header (an 'Option X' key or a
    COMMON-PITFALLS value header). The writer gives every sub-header before>after
    spacing while sentences get before<after, so this is structural and works even
    when the value is pure OMML (a fraction) with empty display text. Falls back to
    a text heuristic only when spacing is absent (a non-engine-written doc).
    `terminators` is language-configurable (pass cfg.sentence_terminators)."""
    sp = _para_spacing(p_el)
    if sp is not None:
        return sp[0] > sp[1]
    s = _para_source(p_el, 0, strict=False).strip()  # fallback for spacing-less docs
    return bool(s) and sentence_count(s, terminators) <= 1 and s[-1] not in terminators \
        and len(s) <= 24 and s.count(' ') <= 3

def parse_solution_blocks(path, cfg, expected_qs=None):
    """Read a Step-4 Solutions docx back into {q: ExplanationBlock}. Inverse of
    build_interleaved_docx's per-block render, driven by the same cfg (labels /
    markers / label-scheme / options). MCQ / MSQ / NAT, any label scheme, any
    language — all via cfg, nothing hardcoded. Used by Step 10 to reason about each
    explanation and to rebuild corrected blocks."""
    doc = Document(path)
    ca_label = cfg.labels['correct_answer'].lower(); opt_word = cfg.labels['option']
    acc = cfg.labels.get('accepted_range', 'accepted range')
    H = {k: f"{cfg.markers.get(k, '')} {cfg.labels.get(k, k)}".strip()
         for k in ('axiom', 'deduction', 'speed_hack', 'why_wrong', 'common_pitfalls')}
    HREV = {v: k for k, v in H.items()}
    ca_prefix = ca_label + ':'
    segs = {}; cur = None; in_expl = False
    for p in doc.paragraphs:
        t = p.text.strip()
        mq = cfg.q_re.match(t)
        if mq:
            cur = int(mq.group(1)); in_expl = False; continue
        if cur is None:
            continue
        if t.lower().startswith(ca_prefix):
            in_expl = True
            segs[cur] = {'ca': _para_source(p._p, cur).strip(), 'paras': []}
            continue
        if in_expl:
            _src = _para_source(p._p, cur).strip()
            if t or _src:                       # keep OMML-only paras; drop blank separators
                segs[cur]['paras'].append((t, _src, p._p))
    want = sorted(segs) if expected_qs is None else sorted(set(expected_qs))
    blocks = {}
    for q in want:
        if q not in segs:
            raise ValueError(f'Q{q}: no explanation region found in {path}')
        ca_src = segs[q]['ca']; body = segs[q]['paras']; n = cfg.expected_options(q)
        disp = ca_src[len(ca_prefix):].strip(); ca_range = None
        if n == 0:
            qtype = 'nat'
            if acc in disp and '(' in disp:
                head, _, tail = disp.partition('(')
                rng = tail.split(acc, 1)[1].strip().rstrip(')').strip()
                for sep in ('\u2013', '\u2014', '-'):
                    if sep in rng:
                        lo, hi = rng.split(sep, 1)
                        ca_range = (float(lo.strip()), float(hi.strip())); break
                ca = head.strip()
            else:
                ca = disp
        else:
            l2i = _label_to_index(cfg, n)
            idxs = []
            for lb in [x.strip() for x in disp.split(',') if x.strip()]:
                if lb not in l2i:
                    raise ValueError(f'Q{q}: CA label {lb!r} not in scheme 1..{n}')
                idxs.append(l2i[lb])
            if len(idxs) == 1:
                qtype = 'mcq'; ca = idxs[0]
            else:
                qtype = 'msq'; ca = set(idxs)
        axiom, deduction, speed = [], [], []
        why_wrong, pitfalls = {}, {}
        mode = None; key = None
        sub_re = re.compile(rf'^{re.escape(opt_word)}\s+(\S+)\s*$')
        for disp, s, p_el in body:
            if disp in HREV:                     # block headers are plain text
                mode = HREV[disp]; key = None; continue
            if mode == 'axiom':
                axiom.append(s)
            elif mode == 'deduction':
                deduction.append(s)
            elif mode == 'speed_hack':
                speed.append(s)
            elif mode == 'why_wrong':
                m = sub_re.match(disp)           # 'Option X' sub-headers are plain text
                if m and _is_subheader(p_el, cfg.sentence_terminators):
                    l2i = _label_to_index(cfg, n)
                    if m.group(1) not in l2i:
                        raise ValueError(f'Q{q}: WHY WRONG label {m.group(1)!r} not in 1..{n}')
                    key = l2i[m.group(1)]; why_wrong[key] = []
                else:
                    if key is None:
                        raise ValueError(f'Q{q}: WHY WRONG sentence before any Option sub-header')
                    why_wrong[key].append(s)
            elif mode == 'common_pitfalls':
                # value headers carry the writer's sub-header spacing (before > after) and
                # may be pure OMML (a fractional wrong value) with empty display text, so
                # detect structurally, not by a text heuristic.
                if _is_subheader(p_el, cfg.sentence_terminators):
                    key = s; pitfalls[key] = []
                else:
                    if key is None:
                        raise ValueError(f'Q{q}: COMMON PITFALLS sentence before any value header')
                    pitfalls[key].append(s)
        kwargs = dict(q=q, cfg=cfg, qtype=qtype, ca=ca, ca_range=ca_range,
                      axiom=axiom, deduction=deduction,
                      speed_hack=(speed or None))
        kwargs['common_pitfalls' if qtype == 'nat' else 'why_wrong'] = (
            pitfalls if qtype == 'nat' else why_wrong)
        blocks[q] = ExplanationBlock(**kwargs)
    return blocks

def parse_learnings(path):
    """Read an EXPLAIN_AUDIT_LEARNINGS / EXPLAIN_LEARNINGS markdown into structured
    rules for the Step-4 consumer (P10 load / §24 apply). Exam-agnostic: rules
    are indexed by their defect_code (the universal-taxonomy routing key), never by
    an exam section name. Accepts audit-learning (AL-*) and explain-guardrail (EX-*)
    rule headers. `path` may be a filepath or the raw markdown text. Returns
    {'rules':[{code,title,defect_code,occurrences,first_seen,pattern,prevention,
    verification,superseded}], 'by_defect':{defect_code:[rule_code,...]}}."""
    import os
    text = open(path, encoding='utf-8').read() if (isinstance(path, str)
            and len(path) < 4096 and os.path.exists(path)) else path
    rules = []
    for b in re.split(r'\n(?=## (?:AL|EX)[-\w]* \u2014 )', text):
        m = re.match(r'## ((?:AL|EX)[-\w]*) \u2014 (.+)', b)
        if not m:
            continue
        code, title = m.group(1), m.group(2).strip()
        def field(name):
            fm = re.search(rf'\*\*{name}:\*\*\s*(.+?)(?=\n\*\*|\n## |\n# |\Z)', b, re.S)
            return fm.group(1).strip() if fm else None
        rules.append({
            'code': code, 'title': title,
            'defect_code': field('Defect code'),
            'occurrences': field(r'Occurrences[^:]*'),
            'first_seen': field('First seen'),
            'pattern': field('Pattern'),
            'prevention': field('Prevention rule') or field('Rule'),
            'verification': field('Verification'),
            'superseded': bool(field('Supersedes')),
        })
    by_defect = {}
    for r in rules:
        dc = r['defect_code']
        if dc:
            by_defect.setdefault(dc, []).append(r['code'])
    return {'rules': rules, 'by_defect': by_defect}

def self_test_audit():
    """Round-trip gate for parse_solution_blocks: write -> read -> rebuild -> assert
    the read-back block reproduces the source, across mcq/msq/nat, numeric/alpha/
    roman labels, OMML fractions. Run with --self-test-audit."""
    import tempfile, os
    res = []
    def chk(name, cond): res.append((name, bool(cond)))
    def roundtrip(cfg, blocks, nq, tag):
        d = tempfile.mkdtemp(); src = os.path.join(d, 's.docx'); out = os.path.join(d, 'o.docx')
        doc = Document()
        for q in range(1, nq + 1):
            doc.add_paragraph(f'Q.{q} stem')
            for o in range(1, (cfg.expected_options(q) or 0) + 1):
                doc.add_paragraph(f'{cfg.option_label(o)}. opt')
            doc.add_paragraph('')
        doc.save(src)
        build_interleaved_docx(src, blocks, out, cfg)
        got = parse_solution_blocks(out, cfg); ok = True
        for b in blocks:
            r = got.get(b.q)
            if r is None: ok = False; break
            same = (r.qtype == b.qtype and r.ca_set() == b.ca_set()
                    and [s.strip() for s in r.axiom] == [s.strip() for s in b.axiom]
                    and [s.strip() for s in r.deduction] == [s.strip() for s in b.deduction]
                    and set(r.why_wrong) == set(b.why_wrong)
                    and set(map(str, r.common_pitfalls)) == set(map(str, b.common_pitfalls)))
            if b.qtype == 'nat':
                same = same and str(r.ca) == str(b.ca) and r.ca_range == b.ca_range
            r.validate(); ok = ok and same
        out2 = os.path.join(d, 'o2.docx')
        build_interleaved_docx(src, list(got.values()), out2, cfg)
        ve, _ = verify_explanations(out2, list(got.values()), cfg)
        chk(tag, ok and ve)
    cfg4 = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
    roundtrip(cfg4, [ExplanationBlock(q=1, ca=3, cfg=cfg4,
        axiom=['The mean equals the sum over the count here.'],
        deduction=['Divide 235/5 to get the value here.', 'The result is Option 3 here.'],
        why_wrong={1: ['Option 1 swaps a value (value_swap).'],
                   2: ['Option 2 mis-signs the term (sign_error).'],
                   4: ['Option 4 covers only part (partial_truth).']})], 1, 'RT-MCQ-FRAC')
    cfgA = EngineConfig(r'^Q\.?\s*(\d+)', r'^([A-D])[.\)]', 4, label_scheme='alpha_upper')
    roundtrip(cfgA, [ExplanationBlock(q=1, ca={1, 3}, cfg=cfgA,
        axiom=['A statement is valid when both halves hold here.'],
        deduction=['Statement one holds and three holds here.', 'So Option A and Option C are correct here.'],
        why_wrong={2: ['Option B passes one test but fails another (partial_truth).'],
                   4: ['Option D fails the parity test (process_confusion).']})], 1, 'RT-MSQ-ALPHA')
    cfgN = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', None, options_by_q={1: 0})
    roundtrip(cfgN, [ExplanationBlock(q=1, ca='47', cfg=cfgN, ca_range=(46.5, 47.5),
        axiom=['The rate equals distance over time here.'],
        deduction=['Compute the quotient step here.', 'The value is 47 here.'],
        common_pitfalls={'235': ['Forgetting to divide leaves 235 (process_confusion).'],
                         '9': ['Dividing by the wrong count gives 9 (value_swap).']})], 1, 'RT-NAT-RANGE-PITFALL')
    cfgR = EngineConfig(r'^Q\.?\s*(\d+)', r'^(i{1,3}|iv)[.\)]', 4, label_scheme='roman_lower')
    roundtrip(cfgR, [ExplanationBlock(q=1, ca=2, cfg=cfgR,
        axiom=['A tangent meets the radius at a right angle here.'],
        deduction=['Apply the perpendicular property here.', 'This gives Option ii here.'],
        why_wrong={1: ['Option i confuses radius with diameter (value_swap).'],
                   3: ['Option iii mis-reads the chord (process_confusion).'],
                   4: ['Option iv drops a factor of two (off_by_one).']})], 1, 'RT-MCQ-ROMAN')
    # regression lock for the m:num/m:den itertext fix: a REAL fraction must pass
    import tempfile as _t, os as _o
    _c = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', 4)
    _b = ExplanationBlock(q=1, ca=1, cfg=_c,
        axiom=['The mean equals the sum over the count here.'],
        deduction=['Divide 235/5 to reach the value here.', 'The result is Option 1 here.'],
        why_wrong={2: ['Option 2 swaps a value (value_swap).'],
                   3: ['Option 3 mis-signs a term (sign_error).'],
                   4: ['Option 4 covers only part (partial_truth).']})
    _d = _t.mkdtemp(); _s = _o.path.join(_d, 's.docx'); _oo = _o.path.join(_d, 'o.docx')
    _dd = Document(); _dd.add_paragraph('Q.1 stem')
    for _x in range(1, 5): _dd.add_paragraph(f'{_x}. opt')
    _dd.add_paragraph(''); _dd.save(_s)
    build_interleaved_docx(_s, [_b], _oo, _c)
    _ok, _ = verify_explanations(_oo, [_b], _c); chk('RT-FRAC-VERIFY', _ok)
    # regression: a NAT with a FRACTION answer AND a fraction pitfall value must
    # round-trip AND pass verify_explanations (both were OMML-blind before the fix).
    _cn = EngineConfig(r'^Q\.?\s*(\d+)', r'^([1-9])[.\)]', None, options_by_q={1: 0})
    _bn = ExplanationBlock(q=1, ca='3/4', cfg=_cn,
        axiom=['The probability equals favourable over total here.'],
        deduction=['Count 3 favourable of 4 here.', 'The value is 3/4 here.'],
        common_pitfalls={'1/2': ['An even split gives 1/2 here (process_confusion).'],
                         '4/3': ['Inverting gives 4/3 here (reversed_relationship).']})
    _dn = _t.mkdtemp(); _sn = _o.path.join(_dn, 's.docx'); _on = _o.path.join(_dn, 'o.docx')
    _dc = Document(); _dc.add_paragraph('Q.1 stem'); _dc.add_paragraph(''); _dc.save(_sn)
    build_interleaved_docx(_sn, [_bn], _on, _cn)
    _ven, _ = verify_explanations(_on, [_bn], _cn)
    _gn = parse_solution_blocks(_on, _cn)[1]
    chk('RT-NAT-FRAC', _ven and set(map(str, _gn.common_pitfalls)) == {'1/2', '4/3'}
        and str(_gn.ca) == '3/4')
    # parse_learnings round-trip: a synthetic AUDIT_LEARNINGS parses to structured
    # rules indexed by defect_code (the Step-4 P10 consumer contract).
    _lm = (
        "# X_EXPLAIN_AUDIT_LEARNINGS_v1.md\n\n## AL-1 \u2014 TRACE MUST PRODUCE THE WRONG VALUE\n\n"
        "**Defect code:** WHY-WRONG-DIAG\n**Occurrences in M1:** 6 of 20\n"
        "**Pattern:** the named error does not reproduce the option value.\n"
        "**Prevention rule:** execute the claimed error and confirm it yields the option.\n"
        "**Verification:** each wrong value traces to a named mistake.\n\n"
        "## AL-2 \u2014 SHORTCUT MUST BE FASTER\n\n**Defect code:** FAKE-SPEED-HACK\n"
        "**Pattern:** the speed hack restates the deduction.\n"
        "**Prevention rule:** require a distinct route with fewer steps, else omit.\n\n"
        "## EX-9 \u2014 VIEW EVERY IMAGE\n\n**Rule:** derive figural answers from the viewed image.\n")
    _pl = parse_learnings(_lm)
    _codes = {r['code'] for r in _pl['rules']}
    chk('LEARN-PARSE-COUNT', _codes == {'AL-1', 'AL-2', 'EX-9'})
    chk('LEARN-PARSE-INDEX', _pl['by_defect'].get('FAKE-SPEED-HACK') == ['AL-2']
        and _pl['by_defect'].get('WHY-WRONG-DIAG') == ['AL-1'])
    _al1 = next(r for r in _pl['rules'] if r['code'] == 'AL-1')
    chk('LEARN-PARSE-FIELDS', bool(_al1['prevention']) and '6 of 20' in (_al1['occurrences'] or '')
        and next(r for r in _pl['rules'] if r['code'] == 'EX-9')['prevention'] is not None)
    _lm2 = ("## AL-5 \u2014 NEW RULE\n\n**Defect code:** CA-WRONG-FACTUAL\n"
            "**Supersedes:** AL-1\n**Prevention rule:** web-verify every fact first.\n")
    _pl2 = parse_learnings(_lm2)
    chk('LEARN-SUPERSEDE', _pl2['rules'][0]['superseded'] is True
        and _pl2['by_defect'].get('CA-WRONG-FACTUAL') == ['AL-5'])
    passed = sum(1 for _, ok in res if ok); total = len(res)
    for nm, ok in res:
        if not ok: print(f'  AUDIT-FAIL: {nm}')
    print(f'AUDIT-SELF-TEST: {passed}/{total} PASS')
    return passed == total

if __name__ == '__main__':
    if '--self-test-audit' in sys.argv:
        sys.exit(0 if self_test_audit() else 1)
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print('explain_engine.py — universal exam-agnostic. '
          '--self-test (core) or --self-test-audit (Step-5 reader round-trip).')
