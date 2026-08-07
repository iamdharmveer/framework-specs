# t3_mathcomp.py — Tier-3 structured math compiler (SHARED ENGINE).
# SINGLE SOURCE: the body below is BYTE-IDENTICAL to Framework_PYQPrepare.md
# §S3-5b (v2.0). explain_engine.self_test() carries a drift lock that fails if
# they diverge. Consumers: PYQPrepare (Step 1, via spec embed), PYQExplain
# (PYQ-1) and MockTestExplain (Step 9) via explain_engine (MANDATE A).
# ── repo-module import shim (not present in the S3-5b spec embed) ──
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn
# ── end shim; everything below is the verbatim S3-5b embed ──
# ── S3-5b — TIER 3 STRUCTURED MATH COMPILER (v2.0) ──────────────────────────────
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
}
_T3_MATRIX = {'pmatrix': ('(', ')'), 'bmatrix': ('[', ']'),
              'vmatrix': ('|', '|'), 'matrix': ('', '')}
_T3_DELIM = {'paren': ('(', ')'), 'brack': ('[', ']'),
             'set': ('{', '}'), 'abs': ('|', '|')}
_T3_FUNCS = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'exp',
             'det', 'sinh', 'cosh', 'tanh', 'gcd', 'arg'}
_T3_LIMWORDS = {'lim', 'max', 'min'}
_T3_ACCENTS = {'hat': '\u0302', 'tilde': '\u0303', 'bar': '\u0305',
               'vec': '\u20d7', 'dot': '\u0307', 'ddot': '\u0308'}
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
    'equiv': '≡', 'propto': '∝', 'sim': '~', 'emptyset': '∅',
    'setminus': '∖', 'mid': '|', 'circ': '∘', 'star': '⋆', 'cdots': '⋯',
    'ldots': '…', 'because': '∵', 'therefore': '∴', 'angle': '∠',
    'perp': '⊥', 'parallel': '∥', 'cong': '≅', 'oplus': '⊕',
    'otimes': '⊗', 'wedge': '∧', 'vee': '∨', 'neg': '¬', 'prime': '′',
    'degree': '°',
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
    if sub_elems is not None:
        n.append(_t3_wrap('m:sub', _t3_content(sub_elems)))
    if sup_elems is not None:
        n.append(_t3_wrap('m:sup', _t3_content(sup_elems)))
    n.append(_t3_e(operand_elems))             # true operand — rest of scope
    return n


def _t3_limlow(word, sub_elems):
    ll = OxmlElement('m:limLow')
    ll.append(_t3_e([_t3_run_roman(word)]))
    ll.append(_t3_wrap('m:lim', _t3_content(sub_elems)))
    return ll


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
        if nc in '{}&\\^_ ':
            out.append(_t3_run(nc))
            return i + 2
        raise MathCompileError("bad escape '\\%s' in %r" % (nc, s))
    name = m.group(1)
    j = i + m.end()
    if name in ('frac', 'sfrac'):
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_frac(_t3_compile_group(a), _t3_compile_group(b),
                            skewed=(name == 'sfrac')))
        return j
    if name == 'sqrt':
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_rad(None, _t3_compile_group(a)))
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
        else:
            jj = i
            while jj < len(s) and s[jj] not in '{}^_\\':
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
    _T3_STATS['compiled'] += 1
    return om


def count_math_regions(*texts):
    """Region count across buffer strings (CHECK 20 producer side)."""
    n = 0
    for t in texts:
        if not t:
            continue
        n += len(_t3_re.findall(_t3_re.escape(MATH_OPEN), t))
    return n
