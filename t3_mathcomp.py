# t3_mathcomp.py — Tier-3 structured math compiler (SHARED ENGINE).
# SINGLE SOURCE: the body below is BYTE-IDENTICAL to Framework_PYQPrepare.md
# §S3-5b (v2.0). explain_engine.self_test() carries a drift lock that fails if
# they diverge. Consumers: PYQPrepare (Step 1, via spec embed), PYQExplain
# (PYQ-1) and MockTestExplain (Step 9) via explain_engine (MANDATE A).
# ── repo-module import shim (not present in the S3-5b spec embed) ──
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn
# ── end shim; everything below is the verbatim S3-5b embed ──
# ── S3-5b — TIER 3 STRUCTURED MATH COMPILER (v2.1) ──────────────────────────────
# Deterministic LaTeX-lite → OMML compiler. Replaces regex reconstruction for all
# structural math. A transcription buffer wraps each non-trivial expression in
# ⟦MATH: ... ⟧; the compiler emits ONE homogeneous <m:oMath> per region.
#
# STRICT CORE, FORGIVING BOUNDARY (v2.0): the compiler itself is strict — an
# unknown command or malformed region raises MathCompileError, deterministically.
# The RENDERER (S3-5 render_text_with_math) catches it: the run NEVER halts and
# the defect NEVER ships silently — the region is delivered as ORDINARY plain
# text (no colour, no highlight — it blends with the surrounding run styling),
# recorded in _T3_STATS['failed'], and reported by CHECK 20 in plain operator
# language, quoting the exact text so the operator can Ctrl+F straight to it.
# That is the GAP-2026-08-07-OMML remedy M2 contract.
#
# Grammar (region body):
#   literal text            any chars except { } ^ _ \   (√N auto-→ <m:rad>)
#   {...}                   grouping (inlined; use as ^/_ argument)
#   base^{sup}  base_{sub}  scripts — attach to preceding atom; both orders
#                           merge into <m:sSubSup>; base "...)"-terminated
#                           literals attach to the balanced (...) group
#   \frac{a}{b}             stacked fraction        <m:f>
#   \sfrac{a}{b}            skewed fraction         <m:f m:type="skw">
#   \sqrt{a}  \root{n}{a}   radicals                <m:rad>
#   \int \iint \oint        n-ary, limits subSup    <m:nary>  (scripts optional)
#   \sum \prod              n-ary, limits undOvr    <m:nary>
#   \sumi \prodi            n-ary, limits subSup (inline running-text style)
#   \lim_{...}              limit-below             <m:limLow>
#   \cases{a, & c1\\ b, & c2}   cases brace         <m:d "{"> + <m:eqArr>
#   \pmatrix{a & b\\ c & d}     ( ) matrix          <m:d> + <m:m>   (also
#   \bmatrix [ ]   \vmatrix | |   \matrix (bare)     — rows \\, cells &)
#   \pre{sub}{sup}{base}    prescripts (ⁿCᵣ)        <m:sPre>
#   \paren{a} \brack{a} \set{a} \abs{a}   stretchy ( ) [ ] { } | | <m:d>
#   \text{...}              roman (upright) text run
#   \sin \cos \tan \sec \csc \cot \log \ln \exp \det \max \min  roman functions
#   \{ \} \& \\ \^ \_ \(space)   escaped literal characters
#
# Empty required slots (e.g. \pre{}{13}{C}) are filled with U+200B so Word never
# shows a dotted placeholder box.
#
# v2.1 (GAP-2026-11-20-MATH-OMML) — STANDARD-LaTeX MATHS SPELLINGS + SCHEMA GUARD.
#   \left( … \right)  (any of ( ) [ ] | . < > \{ \} \| \langle \rangle \lfloor
#                       \rfloor \lceil \rceil \lvert \rvert \lVert \rVert)  <m:d>
#   \begin{pmatrix|bmatrix|vmatrix|Bmatrix|Vmatrix|matrix|smallmatrix|array}
#   \begin{cases|dcases}  \begin{aligned|gathered|split}   (rows \\, cells &)
#   \mathbb \mathcal \mathscr \mathfrak   letters → the Unicode math alphabets
#   \mathrm \operatorname \textrm \mbox  upright;  \mathbf b;  \boldsymbol \bm bi
#   \overline{a} \underline{a}  <m:bar>   \widehat \widetilde \overrightarrow …
#   \sup \inf \limsup \liminf (limit-below like \lim)   \arcsin … \dim \ker \Pr
#   \bigcup \bigcap \bigoplus \bigotimes \coprod \iiint \oiint  n-ary
#   \underset{a}{b} \overset{a}{b} \stackrel{a}{b} \xrightarrow{a}  <m:limLow/Upp>
#   \dfrac \tfrac \cfrac  (= \frac)   \sqrt[n]{a}   \pmod{n} \bmod \mod
#   \not\in \not= \not\subset …   \, \: \; \! \quad \qquad   \| \% \# \$
#   sizing words (\displaystyle \big \Bigl …) are accepted and ignored.
#   \sim is the tilde OPERATOR ∼ (U+223C), no longer the ASCII '~'.
#   |x| → <m:d> with stretchy | | bars, ||x|| → ‖x‖ (a bar is never left as a bare '|' in
#   <m:t>: LibreOffice's OMML import reads that as an operator with empty operands); a
#   bar with no partner (a | b, P(A|B)) is the operator ∣ U+2223. An opening bar is
#   never followed by a space and a closing bar never preceded by one.
# SCHEMA GUARD: every compiled <m:oMath> is checked against the ECMA-376 Part 1
# shared-math.xsd content model (t3_schema_errors, table _T3_CM below — child
# order, required children, attribute values). A region whose XML would violate it
# raises MathCompileError, so a schema-invalid equation can never be emitted.
# Root defect fixed: <m:nary> always carries <m:sub> and <m:sup> (EMPTY when the
# limit is hidden) — CT_Nary requires both; their absence made Word/LibreOffice
# drop or box the integrand (Mock01 Q26/Q63/Q84/Q88/Q99).

import re as _t3_re

MATH_OPEN = '\u27e6MATH:'      # ⟦MATH:
MATH_CLOSE = '\u27e7'          # ⟧
_REGION_RE = _t3_re.compile(_t3_re.escape(MATH_OPEN) + '(.*?)'
                            + _t3_re.escape(MATH_CLOSE), _t3_re.S)
_T3_STATS = {'compiled': 0, 'failed': []}   # CHECK 20 round-trip + degrade ledger


class MathCompileError(ValueError):
    """Tier-3 compile failure — the region cannot be structured. The S3-5
    renderer catches this and degrades the region to ordinary plain text
    (quoted verbatim in the CHECK 20 report so it can be found with Ctrl+F);
    the build CONTINUES (never halt, never silent)."""


_T3_NARY = {
    'int':  ('\u222b', 'subSup'), 'iint': ('\u222c', 'subSup'),
    'oint': ('\u222e', 'subSup'),
    'sum':  ('\u2211', 'undOvr'), 'prod': ('\u220f', 'undOvr'),
    'sumi': ('\u2211', 'subSup'), 'prodi': ('\u220f', 'subSup'),
    'iiint': ('\u222d', 'subSup'), 'oiint': ('\u222f', 'subSup'),
    'bigcup': ('\u22c3', 'undOvr'), 'bigcap': ('\u22c2', 'undOvr'),
    'bigoplus': ('\u2a01', 'undOvr'), 'bigotimes': ('\u2a02', 'undOvr'),
    'coprod': ('\u2210', 'undOvr'), 'bigvee': ('\u22c1', 'undOvr'),
    'bigwedge': ('\u22c0', 'undOvr'),
}
_T3_MATRIX = {'pmatrix': ('(', ')'), 'bmatrix': ('[', ']'),
              'vmatrix': ('|', '|'), 'matrix': ('', ''),
              'Bmatrix': ('{', '}'), 'Vmatrix': ('\u2016', '\u2016'),
              'smallmatrix': ('', '')}
# \begin{…} environments: matrix-like (beg, end) or a builder name
_T3_ENVS = dict(_T3_MATRIX, array=('', ''), cases='cases', dcases='cases',
                aligned='rows', gathered='rows', split='rows')
_T3_DELIM = {'paren': ('(', ')'), 'brack': ('[', ']'),
             'set': ('{', '}'), 'abs': ('|', '|')}
_T3_FUNCS = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'exp',
             'det', 'sinh', 'cosh', 'tanh', 'gcd', 'arg',
             'arcsin', 'arccos', 'arctan', 'sech', 'csch', 'coth', 'lg',
             'dim', 'ker', 'deg', 'hom', 'Pr', 'lcm', 'sgn'}
_T3_LIMWORDS = {'lim', 'max', 'min', 'sup', 'inf'}
_T3_LIMWORD_TEXT = {'limsup': 'lim\u2009sup', 'liminf': 'lim\u2009inf'}
# sizing / style words with no OMML effect — accepted, emit nothing
_T3_NOOP = {'displaystyle', 'textstyle', 'scriptstyle', 'scriptscriptstyle',
            'limits', 'nolimits', 'big', 'Big', 'bigg', 'Bigg', 'bigl', 'bigr',
            'Bigl', 'Bigr', 'biggl', 'biggr', 'Biggl', 'Biggr', 'middle'}
_T3_SPACES = {',': '\u2009', ':': '\u205f', '>': '\u205f', ';': '\u2004', '!': ''}
_T3_SPACE_WORDS = {'quad': '\u2003', 'qquad': '\u2003\u2003', 'enspace': '\u2002',
                   'thinspace': '\u2009'}
# \left / \right delimiter tokens → the character drawn ('' = \left. invisible)
_T3_DELIM_TOKENS = {'(': '(', ')': ')', '[': '[', ']': ']', '|': '|', '.': '',
                    '<': '\u27e8', '>': '\u27e9', '/': '/',
                    '\\{': '{', '\\}': '}', '\\|': '\u2016',
                    '\\lbrace': '{', '\\rbrace': '}', '\\lbrack': '[', '\\rbrack': ']',
                    '\\langle': '\u27e8', '\\rangle': '\u27e9', '\\lfloor': '\u230a',
                    '\\rfloor': '\u230b', '\\lceil': '\u2308', '\\rceil': '\u2309',
                    '\\vert': '|', '\\lvert': '|', '\\rvert': '|', '\\Vert': '\u2016',
                    '\\lVert': '\u2016', '\\rVert': '\u2016'}
_T3_NOT = {'in': '\u2209', 'ni': '\u220c', 'subset': '\u2284', 'supset': '\u2285',
           'subseteq': '\u2288', 'supseteq': '\u2289', 'equiv': '\u2262',
           'sim': '\u2241', 'approx': '\u2249', 'mid': '\u2224', 'parallel': '\u2226',
           'exists': '\u2204', 'le': '\u2270', 'ge': '\u2271', 'leq': '\u2270',
           'geq': '\u2271', 'cong': '\u2247', 'simeq': '\u2244', '=': '\u2260',
           '<': '\u226e', '>': '\u226f'}


def _t3_alpha(start, holes=None, digits=None):
    m = {chr(65 + k): chr(start + k) for k in range(26)}
    m.update(holes or {})
    if digits is not None:
        m.update({str(k): chr(digits + k) for k in range(10)})
    return m


_T3_ALPHABETS = {
    'mathbb': _t3_alpha(0x1D538, {'C': '\u2102', 'H': '\u210d', 'N': '\u2115',
                                  'P': '\u2119', 'Q': '\u211a', 'R': '\u211d',
                                  'Z': '\u2124'}, digits=0x1D7D8),
    'mathcal': _t3_alpha(0x1D49C, {'B': '\u212c', 'E': '\u2130', 'F': '\u2131',
                                   'H': '\u210b', 'I': '\u2110', 'L': '\u2112',
                                   'M': '\u2133', 'R': '\u211b'}),
    'mathfrak': _t3_alpha(0x1D504, {'C': '\u212d', 'H': '\u210c', 'I': '\u2111',
                                    'R': '\u211c', 'Z': '\u2128'}),
}
_T3_ALPHABETS['mathscr'] = _T3_ALPHABETS['mathcal']
_T3_STYLED = {'mathrm': 'p', 'textrm': 'p', 'mbox': 'p', 'mathup': 'p', 'textup': 'p',
              'operatorname': 'p', 'mathbf': 'b', 'textbf': 'b', 'boldsymbol': 'bi',
              'bm': 'bi', 'mathit': 'i', 'textit': 'i', 'emph': 'i'}
_T3_ACCENTS = {'hat': '\u0302', 'tilde': '\u0303', 'bar': '\u0305',
               'vec': '\u20d7', 'dot': '\u0307', 'ddot': '\u0308',
               'widehat': '\u0302', 'widetilde': '\u0303', 'overrightarrow': '\u20d7',
               'acute': '\u0301', 'grave': '\u0300', 'breve': '\u0306',
               'check': '\u030c', 'dddot': '\u20db', 'mathring': '\u030a'}
_T3_SYMBOLS = {
    # Greek
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ',
    'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'pi': 'π', 'rho': 'ρ',
    'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ',
    'psi': 'ψ', 'omega': 'ω', 'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ',
    'Lambda': 'Λ', 'Xi': 'Ξ', 'Pi': 'Π', 'Sigma': 'Σ', 'Phi': 'Φ',
    'Psi': 'Ψ', 'Omega': 'Ω',
    # relations / operators / arrows / sets
    'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'ne': '≠', 'neq': '≠',
    'pm': '±', 'mp': '∓', 'times': '×', 'cdot': '·', 'div': '÷',
    'in': '∈', 'notin': '∉', 'subset': '⊂', 'subseteq': '⊆',
    'supset': '⊃', 'supseteq': '⊇', 'cup': '∪', 'cap': '∩',
    'infty': '∞', 'partial': '∂', 'nabla': '∇', 'forall': '∀',
    'exists': '∃', 'to': '→', 'rightarrow': '→', 'leftarrow': '←',
    'Rightarrow': '⇒', 'Leftarrow': '⇐', 'mapsto': '↦', 'approx': '≈',
    'equiv': '≡', 'propto': '∝', 'sim': '∼', 'emptyset': '∅',
    'setminus': '∖', 'mid': '|', 'circ': '∘', 'star': '⋆', 'cdots': '⋯',
    'ldots': '…', 'because': '∵', 'therefore': '∴', 'angle': '∠',
    'perp': '⊥', 'parallel': '∥', 'cong': '≅', 'oplus': '⊕',
    'otimes': '⊗', 'wedge': '∧', 'vee': '∨', 'neg': '¬', 'prime': '′',
    'degree': '°',
    # v2.1 (GAP-2026-11-20-MATH-OMML) — maths / statistics / physics symbols
    'varepsilon': 'ε', 'vartheta': 'ϑ', 'varphi': 'φ', 'varrho': 'ϱ',
    'varsigma': 'ς', 'varpi': 'ϖ', 'varkappa': 'ϰ', 'digamma': 'ϝ', 'Upsilon': 'Υ',
    'varnothing': '∅', 'smallsetminus': '∖', 'bot': '⊥', 'top': '⊤', 'ell': 'ℓ',
    'hbar': 'ℏ', 'aleph': 'ℵ', 'beth': 'ℶ', 'Re': 'ℜ', 'Im': 'ℑ', 'wp': '℘',
    'imath': 'ı', 'jmath': 'ȷ', 'll': '≪', 'gg': '≫', 'lll': '⋘', 'ggg': '⋙',
    'iff': '⟺', 'implies': '⟹', 'impliedby': '⟸', 'Leftrightarrow': '⇔',
    'leftrightarrow': '↔', 'longrightarrow': '⟶', 'longleftarrow': '⟵',
    'Longrightarrow': '⟹', 'Longleftarrow': '⟸', 'longleftrightarrow': '⟷',
    'Longleftrightarrow': '⟺', 'longmapsto': '⟼', 'uparrow': '↑',
    'downarrow': '↓', 'Uparrow': '⇑', 'Downarrow': '⇓', 'updownarrow': '↕',
    'nearrow': '↗', 'searrow': '↘', 'swarrow': '↙', 'nwarrow': '↖',
    'hookrightarrow': '↪', 'hookleftarrow': '↩', 'twoheadrightarrow': '↠',
    'rightharpoonup': '⇀', 'rightleftharpoons': '⇌', 'leftrightarrows': '⇆',
    'gets': '←', 'ast': '∗', 'dagger': '†', 'ddagger': '‡', 'bullet': '•',
    'diamond': '⋄', 'triangle': '△', 'triangleleft': '◁', 'triangleright': '▷',
    'square': '□', 'Box': '□', 'blacksquare': '■', 'lozenge': '◊', 'qed': '∎',
    'checkmark': '✓', 'lbrace': '{', 'rbrace': '}', 'lbrack': '[', 'rbrack': ']',
    'langle': '⟨', 'rangle': '⟩', 'lfloor': '⌊', 'rfloor': '⌋', 'lceil': '⌈',
    'rceil': '⌉', 'vert': '|', 'Vert': '‖', 'lvert': '|', 'rvert': '|',
    'lVert': '‖', 'rVert': '‖', 'backslash': '∖', 'nmid': '∤', 'ni': '∋',
    'owns': '∋', 'subsetneq': '⊊', 'supsetneq': '⊋', 'nsubseteq': '⊈',
    'nsupseteq': '⊉', 'sqsubseteq': '⊑', 'sqsupseteq': '⊒', 'sqcup': '⊔',
    'sqcap': '⊓', 'uplus': '⊎', 'simeq': '≃', 'asymp': '≍', 'doteq': '≐',
    'triangleq': '≜', 'coloneqq': '≔', 'leqslant': '⩽', 'geqslant': '⩾',
    'lesssim': '≲', 'gtrsim': '≳', 'prec': '≺', 'succ': '≻', 'preceq': '⪯',
    'succeq': '⪰', 'models': '⊨', 'vdash': '⊢', 'dashv': '⊣', 'vdots': '⋮',
    'ddots': '⋱', 'dots': '…', 'dotsc': '…', 'dotsb': '⋯', 'dotsm': '⋯',
    'colon': ':', 'land': '∧', 'lor': '∨', 'lnot': '¬', 'nexists': '∄',
    'complement': '∁', 'measuredangle': '∡', 'sphericalangle': '∢',
    'nparallel': '∦', 'mho': '℧', 'eth': 'ð', 'cdotp': '·', 'odot': '⊙',
    'ominus': '⊖', 'oslash': '⊘', 'bigcirc': '◯', 'amalg': '⨿', 'wr': '≀',
    'pounds': '£', 'S': '§', 'P': '¶',
    'surd': '√', 'flat': '♭', 'natural': '♮', 'sharp': '♯', 'clubsuit': '♣',
    'diamondsuit': '♢', 'heartsuit': '♡', 'spadesuit': '♠', 'circledR': '®',
    'perthousand': '‰', 'textdegree': '°', 'AA': 'Å', 'angstrom': 'Å',
}


def _t3_run(text):
    r = OxmlElement('m:r')
    t = OxmlElement('m:t')
    t.text = text
    if text != text.strip():
        t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def _t3_run_roman(text):
    r = OxmlElement('m:r')
    rPr = OxmlElement('m:rPr')
    sty = OxmlElement('m:sty')
    sty.set(qn('m:val'), 'p')
    rPr.append(sty)
    r.append(rPr)
    t = OxmlElement('m:t')
    t.text = text
    if text != text.strip():
        t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def _t3_wrap(tag, children):
    el = OxmlElement(tag)
    for c in children:
        el.append(c)
    return el


def _t3_content(elems):
    """Non-empty content list — empty slots get a preserved-space run so neither
    Word (dotted box) nor LibreOffice (\u274f placeholder) shows an artefact."""
    return elems if elems else [_t3_run(' ')]


def _t3_e(elems):
    return _t3_wrap('m:e', _t3_content(elems))


def _t3_delim(beg, end, elems):
    d = OxmlElement('m:d')
    if beg != '(' or end != ')':
        dPr = OxmlElement('m:dPr')
        b = OxmlElement('m:begChr'); b.set(qn('m:val'), beg); dPr.append(b)
        en = OxmlElement('m:endChr'); en.set(qn('m:val'), end); dPr.append(en)
        d.append(dPr)
    d.append(_t3_e(elems))
    return d


def _t3_frac(num_elems, den_elems, skewed=False, nobar=False):
    f = OxmlElement('m:f')
    if skewed or nobar:
        fPr = OxmlElement('m:fPr')
        ty = OxmlElement('m:type')
        ty.set(qn('m:val'), 'skw' if skewed else 'noBar')
        fPr.append(ty)
        f.append(fPr)
    f.append(_t3_wrap('m:num', _t3_content(num_elems)))
    f.append(_t3_wrap('m:den', _t3_content(den_elems)))
    return f


def _t3_rad(deg_elems, content_elems):
    rad = OxmlElement('m:rad')
    radPr = OxmlElement('m:radPr')
    if deg_elems is None:
        dh = OxmlElement('m:degHide'); dh.set(qn('m:val'), '1'); radPr.append(dh)
    rad.append(radPr)
    deg = OxmlElement('m:deg')
    if deg_elems is not None:
        for el in _t3_content(deg_elems):
            deg.append(el)
    rad.append(deg)
    rad.append(_t3_e(content_elems))
    return rad


def _t3_nary(chr_, limloc, sub_elems, sup_elems, operand_elems):
    n = OxmlElement('m:nary')
    pr = OxmlElement('m:naryPr')
    c = OxmlElement('m:chr'); c.set(qn('m:val'), chr_); pr.append(c)
    ll = OxmlElement('m:limLoc'); ll.set(qn('m:val'), limloc); pr.append(ll)
    if sub_elems is None:
        sh = OxmlElement('m:subHide'); sh.set(qn('m:val'), '1'); pr.append(sh)
    if sup_elems is None:
        sh = OxmlElement('m:supHide'); sh.set(qn('m:val'), '1'); pr.append(sh)
    n.append(pr)
    # v2.1 (GAP-2026-11-20-MATH-OMML): CT_Nary REQUIRES <m:sub> and <m:sup>, in that
    # order, before <m:e> — EMPTY (with subHide / supHide) when the limit is absent.
    # Omitting them made Word / LibreOffice drop or box the integrand.
    n.append(_t3_wrap('m:sub', _t3_content(sub_elems) if sub_elems is not None else []))
    n.append(_t3_wrap('m:sup', _t3_content(sup_elems) if sup_elems is not None else []))
    n.append(_t3_e(operand_elems))             # true operand — rest of scope
    return n


def _t3_limlow(word, sub_elems):
    ll = OxmlElement('m:limLow')
    ll.append(_t3_e([_t3_run_roman(word)]))
    ll.append(_t3_wrap('m:lim', _t3_content(sub_elems)))
    return ll


def _t3_lim(tag, base_elems, lim_elems):
    """<m:limLow> / <m:limUpp> — base with a limit below / above (\\underset,
    \\overset, \\stackrel, \\xrightarrow)."""
    el = OxmlElement(tag)
    el.append(_t3_e(base_elems))
    el.append(_t3_wrap('m:lim', _t3_content(lim_elems)))
    return el


def _t3_bar(pos, base_elems):
    """<m:bar> — \\overline (pos top) / \\underline (pos bot)."""
    b = OxmlElement('m:bar')
    pr = OxmlElement('m:barPr')
    p = OxmlElement('m:pos'); p.set(qn('m:val'), pos); pr.append(p)
    b.append(pr)
    b.append(_t3_e(base_elems))
    return b


def _t3_runs(elems):
    for el in elems:
        if el.tag == qn('m:r'):
            yield el
        else:
            for sub in el.iter(qn('m:r')):
                yield sub


def _t3_restyle(elems, sty):
    """Set <m:sty> on every run (\\mathrm p, \\mathbf b, \\boldsymbol bi, \\mathit i)."""
    for r in _t3_runs(elems):
        rpr = r.find(qn('m:rPr'))
        if rpr is None:
            rpr = OxmlElement('m:rPr')
            r.insert(0, rpr)
        st = rpr.find(qn('m:sty'))
        if st is None:
            st = OxmlElement('m:sty')
            sc = rpr.find(qn('m:scr'))
            if sc is not None:
                sc.addnext(st)
            else:
                nor = rpr.find(qn('m:nor'))
                if nor is not None:
                    rpr.remove(nor)          # nor excludes sty (CT_RPR choice)
                lit = rpr.find(qn('m:lit'))
                if lit is not None:
                    lit.addnext(st)
                else:
                    rpr.insert(0, st)
        st.set(qn('m:val'), sty)
    return elems


def _t3_realphabet(elems, table):
    """\\mathbb / \\mathcal / \\mathfrak — letters become the Unicode math alphabet."""
    for r in _t3_runs(elems):
        for t in r.iter(qn('m:t')):
            if t.text:
                t.text = ''.join(table.get(ch, ch) for ch in t.text)
    return elems


def _t3_acc(chr_, base_elems):
    acc = OxmlElement('m:acc')
    pr = OxmlElement('m:accPr')
    c = OxmlElement('m:chr'); c.set(qn('m:val'), chr_); pr.append(c)
    acc.append(pr)
    acc.append(_t3_e(base_elems))
    return acc


def _t3_spre(sub_elems, sup_elems, base_elems):
    sp = OxmlElement('m:sPre')
    sp.append(_t3_wrap('m:sub', _t3_content(sub_elems)))
    sp.append(_t3_wrap('m:sup', _t3_content(sup_elems)))
    sp.append(_t3_e(base_elems))
    return sp


def _t3_group_raw(s, i):
    """s[i] == '{' → (raw_body, index_after_close), escape- and nest-aware."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise MathCompileError("unclosed '{' in %r" % s)


def _t3_req_group_raw(s, j, cmd):
    while j < len(s) and s[j] == ' ':
        j += 1
    if j >= len(s) or s[j] != '{':
        raise MathCompileError("\\%s expects a {…} argument in %r" % (cmd, s))
    return _t3_group_raw(s, j)


def _t3_compile_group(raw):
    elems, _ = _t3_seq(raw, 0, top=True)
    return elems


def _t3_rows(raw):
    rows, buf, depth, i = [], [], 0, 0
    while i < len(raw):
        c = raw[i]
        if c == '\\':
            if i + 1 < len(raw) and raw[i + 1] == '\\' and depth == 0:
                rows.append(''.join(buf)); buf = []; i += 2; continue
            buf.append(raw[i:i + 2]); i += 2; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        buf.append(c); i += 1
    rows.append(''.join(buf))
    return rows


def _t3_cells(row):
    cells, buf, depth, i = [], [], 0, 0
    while i < len(row):
        c = row[i]
        if c == '\\':
            buf.append(row[i:i + 2]); i += 2; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if c == '&' and depth == 0:
            cells.append(''.join(buf)); buf = []; i += 1; continue
        buf.append(c); i += 1
    cells.append(''.join(buf))
    return cells


def _t3_cases(raw):
    rows = _t3_rows(raw)
    if len(rows) < 2:
        raise MathCompileError("\\cases needs ≥2 rows (\\\\-separated): %r" % raw)
    eq = OxmlElement('m:eqArr')
    for row in rows:
        content = []
        for k, cell in enumerate(_t3_cells(row)):
            if k:
                content.append(_t3_run('  '))
            content.extend(_t3_compile_group(cell.strip()))
        eq.append(_t3_e(content))
    return _t3_delim('{', '', [eq])


def _t3_matrix(raw, beg, end):
    rows = _t3_rows(raw)
    mm = OxmlElement('m:m')
    width = None
    for row in rows:
        cells = _t3_cells(row)
        if width is None:
            width = len(cells)
        elif len(cells) != width:
            raise MathCompileError(
                "ragged matrix — row widths %d vs %d in %r" % (width, len(cells), raw))
        mr = OxmlElement('m:mr')
        for cell in cells:
            mr.append(_t3_e(_t3_compile_group(cell.strip())))
        mm.append(mr)
    if beg == '' and end == '':
        return mm
    return _t3_delim(beg, end, [mm])


def _t3_literal(out, chunk):
    pos = 0
    for m in _t3_re.finditer('\u221a(\\d+)', chunk):
        if m.start() > pos:
            out.append(_t3_run(chunk[pos:m.start()]))
        out.append(_t3_rad(None, [_t3_run(m.group(1))]))
        pos = m.end()
    rest = chunk[pos:]
    if '\u221a' in rest:
        raise MathCompileError(
            "literal \u221a before non-digit in %r — use \\sqrt{…}" % chunk)
    if rest:
        out.append(_t3_run(rest))


def _t3_pop_base(out, kind):
    if not out:
        raise MathCompileError("script '%s' has no base" % kind)
    base = out.pop()
    if base.tag == qn('m:r') and base.find(qn('m:rPr')) is None:
        t_el = base.find(qn('m:t'))
        txt = (t_el.text or '').rstrip()
        if not txt:
            raise MathCompileError("script '%s' base is empty text" % kind)
        if len(txt) > 1:
            if txt.endswith(')'):
                depth, k = 0, len(txt) - 1
                while k >= 0:
                    if txt[k] == ')':
                        depth += 1
                    elif txt[k] == '(':
                        depth -= 1
                        if depth == 0:
                            break
                    k -= 1
                split = k if (k >= 0 and depth == 0) else len(txt) - 1
            else:
                split = len(txt) - 1
            if split > 0:
                out.append(_t3_run(txt[:split]))
                base = _t3_run(txt[split:])
            else:
                base = _t3_run(txt)
        else:
            base = _t3_run(txt)
    return base


def _t3_children(el, *tags):
    return [el.find(qn(t)) for t in tags]


def _t3_script(s, i, out):
    kind = s[i]
    atoms, j = _t3_atom(s, i + 1)
    prev = out[-1] if out else None
    # merge x_a^b / x^b_a into m:sSubSup
    if prev is not None and prev.tag == qn('m:sSub') and kind == '^':
        e_el, sub_el = _t3_children(prev, 'm:e', 'm:sub')
        out.pop()
        ss = OxmlElement('m:sSubSup')
        ss.append(e_el); ss.append(sub_el)
        ss.append(_t3_wrap('m:sup', _t3_content(atoms)))
        out.append(ss)
        return j
    if prev is not None and prev.tag == qn('m:sSup') and kind == '_':
        e_el, sup_el = _t3_children(prev, 'm:e', 'm:sup')
        out.pop()
        ss = OxmlElement('m:sSubSup')
        ss.append(e_el)
        ss.append(_t3_wrap('m:sub', _t3_content(atoms)))
        ss.append(sup_el)
        out.append(ss)
        return j
    base = _t3_pop_base(out, kind)
    tag = 'm:sSup' if kind == '^' else 'm:sSub'
    arg = 'm:sup' if kind == '^' else 'm:sub'
    ss = OxmlElement(tag)
    ss.append(_t3_e([base]))
    ss.append(_t3_wrap(arg, _t3_content(atoms)))
    out.append(ss)
    return j


def _t3_atom(s, i):
    if i >= len(s):
        raise MathCompileError("script or command runs off end of region %r" % s)
    c = s[i]
    if c == '{':
        raw, j = _t3_group_raw(s, i)
        return _t3_compile_group(raw), j
    if c == '\\':
        out = []
        j = _t3_command(s, i, out)
        return out, j
    if c == '\u221a':
        m = _t3_re.match('\u221a(\\d+)', s[i:])
        if m:
            return [_t3_rad(None, [_t3_run(m.group(1))])], i + m.end()
        raise MathCompileError("literal \u221a before non-digit — use \\sqrt{…}")
    return [_t3_run(c)], i + 1


def _t3_command(s, i, out):
    m = _t3_re.match(r'\\([A-Za-z]+)', s[i:])
    if not m:
        nc = s[i + 1] if i + 1 < len(s) else ''
        if nc in '{}&\\^_ %#$':
            out.append(_t3_run(nc))
            return i + 2
        if nc in _T3_SPACES:                      # v2.1: \, \: \> \; \!
            if _T3_SPACES[nc]:
                out.append(_t3_run(_T3_SPACES[nc]))
            return i + 2
        if nc == '|':                             # v2.1: \| norm bars
            out.append(_t3_run('\u2016'))
            return i + 2
        raise MathCompileError("bad escape '\\%s' in %r" % (nc, s))
    name = m.group(1)
    j = i + m.end()
    if name in _T3_NOOP:
        return j
    if name in _T3_SPACE_WORDS:
        out.append(_t3_run(_T3_SPACE_WORDS[name]))
        return j
    if name in ('dfrac', 'tfrac', 'cfrac'):
        name = 'frac'
    if name in ('frac', 'sfrac'):
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_frac(_t3_compile_group(a), _t3_compile_group(b),
                            skewed=(name == 'sfrac')))
        return j
    if name == 'sqrt':
        if j < len(s) and s[j] == '[':            # v2.1: \sqrt[n]{a}
            k = _t3_bracket_end(s, j)
            d = s[j + 1:k]
            a, j = _t3_req_group_raw(s, k + 1, name)
            out.append(_t3_rad(_t3_compile_group(d), _t3_compile_group(a)))
            return j
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_rad(None, _t3_compile_group(a)))
        return j
    if name == 'left':                            # v2.1: \left … \right
        return _t3_left_right(s, j, out)
    if name in ('right', 'end'):
        raise MathCompileError("\\%s without its opening \\%s in %r"
                               % (name, 'left' if name == 'right' else 'begin', s))
    if name == 'begin':                           # v2.1: \begin{env} … \end{env}
        return _t3_environment(s, j, out)
    if name in _T3_ALPHABETS:                     # v2.1: \mathbb{R} \mathcal{F}
        a, j = _t3_req_group_raw(s, j, name)
        out.extend(_t3_realphabet(_t3_compile_group(a), _T3_ALPHABETS[name]))
        return j
    if name in _T3_STYLED:                        # v2.1: \mathrm \operatorname \mathbf …
        if name == 'operatorname' and j < len(s) and s[j] == '*':
            j += 1
        a, j = _t3_req_group_raw(s, j, name)
        out.extend(_t3_restyle(_t3_compile_group(a), _T3_STYLED[name]))
        return j
    if name in ('overline', 'underline'):
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_bar('top' if name == 'overline' else 'bot', _t3_compile_group(a)))
        return j
    if name in ('underset', 'overset', 'stackrel'):
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_lim('m:limLow' if name == 'underset' else 'm:limUpp',
                           _t3_compile_group(b), _t3_compile_group(a)))
        return j
    if name in ('xrightarrow', 'xleftarrow'):
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_lim('m:limUpp', [_t3_run('\u27f6' if name == 'xrightarrow' else '\u27f5')],
                           _t3_compile_group(a)))
        return j
    if name == 'pmod':
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_delim('(', ')', [_t3_run_roman('mod'), _t3_run(' ')] + _t3_compile_group(a)))
        return j
    if name == 'bmod':
        out.extend([_t3_run(' '), _t3_run_roman('mod'), _t3_run(' ')])
        return j
    if name == 'mod':
        out.extend([_t3_run_roman('mod'), _t3_run(' ')])
        return j
    if name == 'not':
        return _t3_not(s, j, out)
    if name in _T3_LIMWORD_TEXT:                  # v2.1: \limsup \liminf
        word = _T3_LIMWORD_TEXT[name]
        if j < len(s) and s[j] == '_':
            atoms, j = _t3_atom(s, j + 1)
            out.append(_t3_limlow(word, atoms))
            return j
        out.append(_t3_run_roman(word))
        return j
    if name == 'root':
        d, j = _t3_req_group_raw(s, j, name)
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_rad(_t3_compile_group(d), _t3_compile_group(a)))
        return j
    if name in _T3_DELIM:
        a, j = _t3_req_group_raw(s, j, name)
        beg, end = _T3_DELIM[name]
        out.append(_t3_delim(beg, end, _t3_compile_group(a)))
        return j
    if name == 'text':
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_run_roman(a))
        return j
    if name in _T3_NARY:
        ch, loc = _T3_NARY[name]
        sub = sup = None
        while j < len(s) and s[j] in '^_':
            k = s[j]
            atoms, j = _t3_atom(s, j + 1)
            if k == '_':
                sub = atoms
            else:
                sup = atoms
        rest, _ = _t3_seq(s, j, top=True)   # operand = remainder of this scope
        out.append(_t3_nary(ch, loc, sub, sup, rest))
        return len(s)
    if name in _T3_LIMWORDS:
        if j < len(s) and s[j] == '_':
            atoms, j = _t3_atom(s, j + 1)
            out.append(_t3_limlow(name, atoms))
            return j
        out.append(_t3_run_roman(name))
        return j
    if name in _T3_FUNCS:
        out.append(_t3_run_roman(name))
        return j
    if name == 'cases':
        raw, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_cases(raw))
        return j
    if name in _T3_MATRIX:
        raw, j = _t3_req_group_raw(s, j, name)
        beg, end = _T3_MATRIX[name]
        out.append(_t3_matrix(raw, beg, end))
        return j
    if name in _T3_ACCENTS:
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_acc(_T3_ACCENTS[name], _t3_compile_group(a)))
        return j
    if name == 'binom':
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        f = _t3_frac(_t3_compile_group(a), _t3_compile_group(b), nobar=True)
        out.append(_t3_delim('(', ')', [f]))
        return j
    if name in _T3_SYMBOLS:
        out.append(_t3_run(_T3_SYMBOLS[name]))
        return j
    if name == 'pre':
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        c, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_spre(_t3_compile_group(a), _t3_compile_group(b),
                            _t3_compile_group(c)))
        return j
    raise MathCompileError(
        "unknown command \\%s — not in the Tier-3 grammar (S3-5b). The renderer "
        "delivers this region as plain text and CHECK 20 quotes it; fix the "
        "⟦MATH:⟧ spelling in the buffer and rebuild" % name)


def _t3_bracket_end(s, j):
    """s[j] == '[' → index of its matching ']' (nest-aware, escape-aware)."""
    depth, k = 0, j
    while k < len(s):
        c = s[k]
        if c == '\\':
            k += 2
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return k
        k += 1
    raise MathCompileError("unclosed '[' in %r" % s)


def _t3_delim_token(s, j, what):
    """The \\left / \\right delimiter at s[j:] → (character, index after)."""
    while j < len(s) and s[j] == ' ':
        j += 1
    if j >= len(s):
        raise MathCompileError("\\%s needs a delimiter in %r" % (what, s))
    if s[j] == '\\':
        m = _t3_re.match(r'\\([A-Za-z]+)', s[j:])
        tok = ('\\' + m.group(1)) if m else s[j:j + 2]
    else:
        tok = s[j]
    if tok not in _T3_DELIM_TOKENS:
        raise MathCompileError("\\%s %s is not a delimiter in %r" % (what, tok, s))
    return _T3_DELIM_TOKENS[tok], j + len(tok)


def _t3_left_right(s, j, out):
    """\\left<d> … \\right<d> → one stretchy <m:d>; nested pairs are matched."""
    beg, k = _t3_delim_token(s, j, 'left')
    depth, p = 1, k
    while p < len(s):
        if s[p] == '\\':
            m = _t3_re.match(r'\\(left|right)(?![A-Za-z])', s[p:])
            if m:
                depth += 1 if m.group(1) == 'left' else -1
                if depth == 0:
                    inner = s[k:p]
                    end, q = _t3_delim_token(s, p + m.end(), 'right')
                    out.append(_t3_delim(beg, end, _t3_compile_group(inner)))
                    return q
                p += m.end()
                continue
            p += 2
            continue
        p += 1
    raise MathCompileError("\\left without its \\right in %r" % s)


def _t3_environment(s, j, out):
    """\\begin{env}…\\end{env} for the matrix, cases and aligned families."""
    env, k = _t3_req_group_raw(s, j, 'begin')
    env = env.strip()
    star = env.endswith('*')
    base = env[:-1] if star else env
    if base not in _T3_ENVS:
        raise MathCompileError("\\begin{%s} is not a supported environment in %r" % (env, s))
    if base == 'array':                           # column spec {lcr} — layout only
        while k < len(s) and s[k] == ' ':
            k += 1
        if k < len(s) and s[k] == '{':
            _, k = _t3_group_raw(s, k)
    open_re = _t3_re.compile(r'\\begin\s*\{' + _t3_re.escape(env) + r'\}')
    close_re = _t3_re.compile(r'\\end\s*\{' + _t3_re.escape(env) + r'\}')
    depth, p = 1, k
    while p < len(s):
        mo, mc = open_re.match(s, p), close_re.match(s, p)
        if mo:
            depth += 1; p = mo.end(); continue
        if mc:
            depth -= 1
            if depth == 0:
                body = s[k:p]
                kind = _T3_ENVS[base]
                if kind == 'cases':
                    out.append(_t3_cases(body))
                elif kind == 'rows':
                    out.append(_t3_eqarr(body))
                else:
                    out.append(_t3_matrix(body, kind[0], kind[1]))
                return mc.end()
            p = mc.end(); continue
        p += 2 if s[p] == '\\' else 1
    raise MathCompileError("\\begin{%s} without its \\end{%s} in %r" % (env, env, s))


def _t3_eqarr(raw):
    """aligned / gathered rows → <m:eqArr> (alignment marks & are layout only)."""
    eq = OxmlElement('m:eqArr')
    for row in _t3_rows(raw):
        content = []
        for cell in _t3_cells(row):
            content.extend(_t3_compile_group(cell.strip()))
        eq.append(_t3_e(content))
    return eq


def _t3_not(s, j, out):
    """\\not<relation> → the negated relation character."""
    while j < len(s) and s[j] == ' ':
        j += 1
    m = _t3_re.match(r'\\([A-Za-z]+)', s[j:])
    if m and m.group(1) in _T3_NOT:
        out.append(_t3_run(_T3_NOT[m.group(1)]))
        return j + m.end()
    if j < len(s) and s[j] in _T3_NOT:
        out.append(_t3_run(_T3_NOT[s[j]]))
        return j + 1
    raise MathCompileError("\\not before an unsupported relation in %r" % s)


def _t3_bar_close(s, i, mark):
    """Index of the closing `mark` ('|' or '||') for an opening bar ending at s[i-1],
    at the same brace depth, or -1. An opening bar is never followed by a space
    and a closing bar never preceded by one (so 'a | b' stays a lone bar)."""
    if i >= len(s) or s[i] in ' |':
        return -1
    depth, k = 0, i
    while k < len(s):
        c = s[k]
        if c == '\\':
            m = _t3_re.match(r'\\(left|right)(?![A-Za-z])\s*', s[k:])
            if m:                                 # \left| / \right| are not bars
                k += m.end() + (2 if s.startswith('\\', k + m.end()) else 1)
                continue
            m = _t3_re.match(r'\\[A-Za-z]+', s[k:])
            k += m.end() if m else 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            if depth == 0:
                return -1
            depth -= 1
        elif c == '|' and depth == 0:
            if s.startswith(mark, k) and s[k - 1] != ' ' and \
                    (mark == '||' or not s.startswith('||', k)):
                return k
            if mark == '||' or s.startswith('||', k):
                return -1
            return -1 if s[k - 1] == ' ' else k
        k += 1
    return -1


def _t3_bars(s, i, out):
    """|x| → <m:d> with | | (stretchy), ||x|| → <m:d> with ‖ ‖; a bar with no partner
    is the operator ∣ (U+2223: divides, 'such that', conditional)."""
    mark = '||' if s.startswith('||', i) else '|'
    k = _t3_bar_close(s, i + len(mark), mark)
    if k < 0:
        out.append(_t3_run('\u2016' if mark == '||' else '\u2223'))
        return i + len(mark)
    ch = '\u2016' if mark == '||' else '|'
    out.append(_t3_delim(ch, ch, _t3_compile_group(s[i + len(mark):k])))
    return k + len(mark)


def _t3_seq(s, i, top=False):
    out = []
    while i < len(s):
        c = s[i]
        if c == '}':
            if top:
                raise MathCompileError("unmatched '}' at %d in %r" % (i, s))
            return out, i + 1
        if c == '{':
            raw, i = _t3_group_raw(s, i)
            out.extend(_t3_compile_group(raw))
        elif c in '^_':
            i = _t3_script(s, i, out)
        elif c == '\\':
            i = _t3_command(s, i, out)
        elif c == '|':                            # v2.1: |x| → <m:d>, ||x|| → ‖x‖
            i = _t3_bars(s, i, out)
        else:
            jj = i
            while jj < len(s) and s[jj] not in '{}^_\\|':
                jj += 1
            _t3_literal(out, s[i:jj])
            i = jj
    if top:
        return out, i
    raise MathCompileError("missing '}' in %r" % s)


def t3_compile(body):
    """Compile one ⟦MATH:…⟧ region body → a single <m:oMath> element."""
    if MATH_OPEN in body or MATH_CLOSE in body:
        raise MathCompileError("nested/unbalanced region delimiters in %r" % body)
    if '\n' in body or '\t' in body:
        raise MathCompileError("⟦MATH:⟧ region must be single-line: %r" % body)
    elems, _ = _t3_seq(body, 0, top=True)
    if not elems:
        raise MathCompileError("empty ⟦MATH:⟧ region")
    om = OxmlElement('m:oMath')
    for e in elems:
        om.append(e)
    errs = t3_schema_errors(om)                   # v2.1 SCHEMA GUARD
    if errs:
        raise MathCompileError("schema-invalid OMML (%s) for %r — engine defect, the "
                               "region is delivered as plain text" % ('; '.join(errs[:3]), body))
    _T3_STATS['compiled'] += 1
    return om


# ── v2.1 SCHEMA GUARD — ECMA-376 Part 1 shared-math.xsd content model ───────────
# Transcribed from the schema (CT_* sequences). 'A' = an OMathArg (argPr?, math*,
# ctrlPr?); a list = the ordered child sequence [(name, min, max)], max 0 = unbounded;
# a dict entry under _T3_CM_LEAF = a property element: (attribute-type, required).
_T3_MATH_ELEMS = ('acc', 'bar', 'box', 'borderBox', 'd', 'eqArr', 'f', 'func', 'groupChr',
                  'limLow', 'limUpp', 'm', 'nary', 'phant', 'rad', 'sPre', 'sSub',
                  'sSubSup', 'sSup', 'r')
_T3_ARGS = ('e', 'num', 'den', 'sub', 'sup', 'deg', 'lim', 'fName')


def _t3_seq_model(*names):
    return [(n, 0, 1) for n in names]


_T3_CM = {
    'acc': [('accPr', 0, 1), ('e', 1, 1)], 'accPr': _t3_seq_model('chr', 'ctrlPr'),
    'bar': [('barPr', 0, 1), ('e', 1, 1)], 'barPr': _t3_seq_model('pos', 'ctrlPr'),
    'box': [('boxPr', 0, 1), ('e', 1, 1)],
    'boxPr': _t3_seq_model('opEmu', 'noBreak', 'diff', 'brk', 'aln', 'ctrlPr'),
    'borderBox': [('borderBoxPr', 0, 1), ('e', 1, 1)],
    'borderBoxPr': _t3_seq_model('hideTop', 'hideBot', 'hideLeft', 'hideRight', 'strikeH',
                                 'strikeV', 'strikeBLTR', 'strikeTLBR', 'ctrlPr'),
    'd': [('dPr', 0, 1), ('e', 1, 0)],
    'dPr': _t3_seq_model('begChr', 'sepChr', 'endChr', 'grow', 'shp', 'ctrlPr'),
    'eqArr': [('eqArrPr', 0, 1), ('e', 1, 0)],
    'eqArrPr': _t3_seq_model('baseJc', 'maxDist', 'objDist', 'rSpRule', 'rSp', 'ctrlPr'),
    'f': [('fPr', 0, 1), ('num', 1, 1), ('den', 1, 1)], 'fPr': _t3_seq_model('type', 'ctrlPr'),
    'func': [('funcPr', 0, 1), ('fName', 1, 1), ('e', 1, 1)], 'funcPr': _t3_seq_model('ctrlPr'),
    'groupChr': [('groupChrPr', 0, 1), ('e', 1, 1)],
    'groupChrPr': _t3_seq_model('chr', 'pos', 'vertJc', 'ctrlPr'),
    'limLow': [('limLowPr', 0, 1), ('e', 1, 1), ('lim', 1, 1)], 'limLowPr': _t3_seq_model('ctrlPr'),
    'limUpp': [('limUppPr', 0, 1), ('e', 1, 1), ('lim', 1, 1)], 'limUppPr': _t3_seq_model('ctrlPr'),
    'm': [('mPr', 0, 1), ('mr', 1, 0)],
    'mPr': _t3_seq_model('baseJc', 'plcHide', 'rSpRule', 'cGpRule', 'rSp', 'cSp', 'cGp', 'mcs',
                         'ctrlPr'),
    'mcs': [('mc', 1, 0)], 'mc': _t3_seq_model('mcPr'), 'mcPr': _t3_seq_model('count', 'mcJc'),
    'mr': [('e', 1, 0)],
    'nary': [('naryPr', 0, 1), ('sub', 1, 1), ('sup', 1, 1), ('e', 1, 1)],
    'naryPr': _t3_seq_model('chr', 'limLoc', 'grow', 'subHide', 'supHide', 'ctrlPr'),
    'phant': [('phantPr', 0, 1), ('e', 1, 1)],
    'phantPr': _t3_seq_model('show', 'zeroWid', 'zeroAsc', 'zeroDesc', 'transp', 'ctrlPr'),
    'rad': [('radPr', 0, 1), ('deg', 1, 1), ('e', 1, 1)], 'radPr': _t3_seq_model('degHide', 'ctrlPr'),
    'sPre': [('sPrePr', 0, 1), ('sub', 1, 1), ('sup', 1, 1), ('e', 1, 1)],
    'sPrePr': _t3_seq_model('ctrlPr'),
    'sSub': [('sSubPr', 0, 1), ('e', 1, 1), ('sub', 1, 1)], 'sSubPr': _t3_seq_model('ctrlPr'),
    'sSubSup': [('sSubSupPr', 0, 1), ('e', 1, 1), ('sub', 1, 1), ('sup', 1, 1)],
    'sSubSupPr': _t3_seq_model('alnScr', 'ctrlPr'),
    'sSup': [('sSupPr', 0, 1), ('e', 1, 1), ('sup', 1, 1)], 'sSupPr': _t3_seq_model('ctrlPr'),
    'oMathPara': [('oMathParaPr', 0, 1), ('oMath', 1, 0)], 'oMathParaPr': _t3_seq_model('jc'),
    'argPr': _t3_seq_model('argSz'),
}
_T3_ONOFF = ('true', 'false', '1', '0', 'on', 'off')
_T3_CM_LEAF = {
    'chr': ('char', True), 'begChr': ('char', True), 'sepChr': ('char', True),
    'endChr': ('char', True), 'limLoc': (('undOvr', 'subSup'), True),
    'type': (('bar', 'skw', 'lin', 'noBar'), True), 'pos': (('top', 'bot'), True),
    'vertJc': (('top', 'bot'), True), 'shp': (('centered', 'match'), True),
    'sty': (('p', 'b', 'i', 'bi'), False),
    'scr': (('roman', 'script', 'fraktur', 'double-struck', 'sans-serif', 'monospace'), False),
    'count': ((1, 255), True), 'argSz': ((-2, 2), True), 'rSpRule': ((0, 4), True),
    'cGpRule': ((0, 4), True), 'rSp': ((0, 4294967295), True), 'cSp': ((0, 4294967295), True),
    'cGp': ((0, 4294967295), True),
    'mcJc': (('left', 'center', 'right', 'inside', 'outside'), True),
    'baseJc': (('inline', 'top', 'center', 'bottom', 'inside', 'outside'), True),
    'jc': (('left', 'right', 'center', 'centerGroup'), False),
    'brk': ('brk', False),
}
for _n in ('grow', 'subHide', 'supHide', 'degHide', 'plcHide', 'maxDist', 'objDist', 'alnScr',
           'lit', 'nor', 'aln', 'opEmu', 'noBreak', 'diff', 'hideTop', 'hideBot', 'hideLeft',
           'hideRight', 'strikeH', 'strikeV', 'strikeBLTR', 'strikeTLBR', 'show', 'zeroWid',
           'zeroAsc', 'zeroDesc', 'transp'):
    _T3_CM_LEAF[_n] = (_T3_ONOFF, False)
_T3_M_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'


def _t3_local(el):
    tag = el.tag if isinstance(el.tag, str) else ''
    return tag[len(_T3_M_NS):] if tag.startswith(_T3_M_NS) else None


def _t3_check_seq(name, kids, model, errs):
    k = 0
    for child, lo, hi in model:
        n = 0
        while k < len(kids) and kids[k] == child and (hi == 0 or n < hi):
            n += 1; k += 1
        if n < lo:
            errs.append('<m:%s> requires <m:%s>' % (name, child))
    if k < len(kids):
        errs.append('<m:%s> has <m:%s> out of order or not allowed' % (name, kids[k]))


def _t3_check_leaf(name, el, errs):
    kind, required = _T3_CM_LEAF[name]
    v = el.get(_T3_M_NS + 'val')
    if name == 'brk':
        v = el.get(_T3_M_NS + 'alnAt')
        if v is not None and not (v.lstrip('-').isdigit() and 1 <= int(v) <= 255):
            errs.append('<m:brk alnAt=%r> out of range' % v)
        return
    if v is None:
        if required:
            errs.append('<m:%s> requires m:val' % name)
        return
    if kind == 'char':
        if len(v) > 1:
            errs.append('<m:%s m:val=%r> must be at most one character' % (name, v))
    elif isinstance(kind, tuple) and kind and isinstance(kind[0], int):
        if not (v.lstrip('-').isdigit() and kind[0] <= int(v) <= kind[1]):
            errs.append('<m:%s m:val=%r> out of range' % (name, v))
    elif v not in kind:
        errs.append('<m:%s m:val=%r> not allowed' % (name, v))


def t3_schema_errors(el):
    """[] when the <m:oMath> (or any OMML element) satisfies the ECMA-376
    shared-math.xsd content model; otherwise one plain message per violation.
    Elements outside the math namespace (w:rPr in runs, w:ins/w:del) are
    accepted where the schema admits them. Pure; never raises."""
    errs = []
    try:
        _t3_validate(el, errs)
    except Exception as ex:                       # noqa: BLE001 — a validator never raises
        errs.append('validator error: %s' % ex)
    return errs


def _t3_validate(el, errs):
    name = _t3_local(el)
    if name is None:
        return                                    # foreign (w:) element — schema-admitted
    kids_el = [c for c in el if isinstance(c.tag, str)]
    kids = [_t3_local(c) for c in kids_el]
    mkids = [k for k in kids if k is not None]
    if name in ('oMath',) or name in _T3_ARGS:
        body = mkids
        if name in _T3_ARGS:
            if body and body[0] == 'argPr':
                body = body[1:]
            if body and body[-1] == 'ctrlPr':
                body = body[:-1]
        for k in body:
            if k not in _T3_MATH_ELEMS:
                errs.append('<m:%s> may not contain <m:%s>' % (name, k))
    elif name == 'r':
        seen_t = False
        for idx, k in enumerate(mkids):
            if k == 'rPr':
                if idx != 0 or seen_t:
                    errs.append('<m:rPr> must be the first child of <m:r>')
            elif k == 't':
                seen_t = True
            else:
                errs.append('<m:r> may not contain <m:%s>' % k)
    elif name == 'rPr':
        order = ['lit', 'nor', 'scr', 'sty', 'brk', 'aln']
        pos = -1
        for k in mkids:
            if k not in order:
                errs.append('<m:rPr> may not contain <m:%s>' % k); continue
            if order.index(k) <= pos:
                errs.append('<m:rPr> child <m:%s> out of order or repeated' % k)
            pos = order.index(k)
        if 'nor' in mkids and ('scr' in mkids or 'sty' in mkids):
            errs.append('<m:rPr> cannot combine <m:nor> with <m:scr>/<m:sty>')
    elif name == 't':
        if mkids:
            errs.append('<m:t> holds text only')
    elif name == 'ctrlPr':
        if mkids:
            errs.append('<m:ctrlPr> holds run properties only')
    elif name in _T3_CM_LEAF:
        if mkids:
            errs.append('<m:%s> may not have children' % name)
        _t3_check_leaf(name, el, errs)
    elif name in _T3_CM:
        if len(mkids) != len(kids):
            errs.append('<m:%s> may not contain non-math elements' % name)
        _t3_check_seq(name, mkids, _T3_CM[name], errs)
    else:
        errs.append('<m:%s> is not an OMML element' % name)
    for c in kids_el:
        _t3_validate(c, errs)


def count_math_regions(*texts):
    """Region count across buffer strings (CHECK 20 producer side)."""
    n = 0
    for t in texts:
        if not t:
            continue
        n += len(_t3_re.findall(_t3_re.escape(MATH_OPEN), t))
    return n
