#!/usr/bin/env python3
# ============================================================================
# [ExamCode]_mock_test_audit.py
# UNIVERSAL, EXAM-AGNOSTIC Part-A machine-gate auditor for Step 8
# (Framework_MockTestCreateAudit v2.6, Appendix A).
#
# Zero hardcoded exam values: every expected value (question/section counts,
# q_ranges, options_count, option label format, language, OMML-required
# subtopics, figural/linked maps) is read at runtime from blueprint.json /
# section_rules.md / subtopic_manifest.json / registry.json. The SAME script
# audits any exam with valid Step 0/1/2 outputs.
#
# v2.6 — adds the S5-1A COMPLETION GATE (--audit-state): after Part A, validates
# the Phase-2 audit_state ledger (C1-C7) and the on-disk evidence artefacts each
# stamp names, so a skipped/collapsed Phase 2 fails LOUDLY instead of shipping.
# The self-test is FIXTURE-BASED (MANDATE A / P1): a constant-print stub is not a
# valid auditor.
#
# Dependencies: python-docx + Python stdlib ONLY.
#
# Usage:
#   python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#       --blueprint BP.json --rules RULES.md --manifest MAN.json \
#       --registry REG.json --mockN N [--final] [--audit-state STATE.json]
#   python3 [ExamCode]_mock_test_audit.py --self-test
#
# Exit code: 0 if no FAIL AND (when --audit-state) COMPLETION-GATE PASS, else 1.
# WARNs are printed for reviewer adjudication (Part B / §7) and do not change the
# exit code; the Step-8 certification gate (spec §12-2) decides whether a fixable
# WARN blocks delivery.
# ============================================================================
import sys, os, re, json, hashlib, zipfile, argparse, tempfile, unicodedata
import io, zlib, struct          # v2.13 — stdlib PNG fixtures (D4); no PIL needed
from pathlib import Path
from collections import Counter, defaultdict

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.document import Document as _DocClass

# ---- OOXML namespaces ------------------------------------------------------
W  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M  = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A  = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
def W_(t):  return f'{{{W}}}{t}'
def M_(t):  return f'{{{M}}}{t}'

# ---- v2.6 constants (MANDATE A / S5-1A) ------------------------------------
AUTH_GATE_FLOOR   = 35    # P1: the self-test must exercise >= this many fixtures.
EVIDENCE_MIN_BYTES = 100  # S5-1A C6: a montage evidence file must be a real raster.

# ---- result accumulator ----------------------------------------------------
RESULTS = []   # list of (level, code, message)
def _ok(c, m):   RESULTS.append(('OK',   c, m))
def _warn(c, m): RESULTS.append(('WARN', c, m))
def _fail(c, m): RESULTS.append(('FAIL', c, m))
def _reset():    RESULTS.clear()

# ---- block model -----------------------------------------------------------
QNUM_RE = re.compile(r'^\s*Q\.?\s*(\d+)\b')

class Block:
    __slots__ = ('qnum', 'items', 'paras', 'tables', 'images')
    def __init__(self, qnum):
        self.qnum = qnum
        self.items = []       # ordered ('p',Paragraph) / ('t',Table)
        self.paras = []       # Paragraph objects in this block
        self.tables = []      # Table objects in this block
        # v2.13 (GAP-2026-08-01-FIGSPEC-TRANSPORT D1): POPULATED by
        # attach_block_images() — one dict per inline image in this block, in
        # document order:
        #   {'name': docPr/@name, 'rid': r:embed, 'descr': docPr/@descr,
        #    'part': media part basename, 'path': extracted PNG path|None}
        # It was declared '# reserved' from v1.0 and never appended to anywhere,
        # so the twelve v2.11 figure-conformance gates iterated an always-empty
        # list and printed "0 figure(s) conform." on every paper in every exam.
        self.images = []


def iter_block_items(doc):
    """Yield Paragraph and Table objects in true document order."""
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield ('p', Paragraph(child, doc))
        elif child.tag == qn('w:tbl'):
            yield ('t', Table(child, doc))


def para_text(p):
    """Readable text of a paragraph, merging normal text (w:t) and math (m:t)
    in document order so a math-bearing or pure-OMML stem is never seen empty."""
    out = []
    for node in p._element.iter():
        if node.tag == W_('t') or node.tag == M_('t'):
            out.append(node.text or '')
    return ''.join(out)


def para_images(p):
    """Return [(docPr_name, blip_rEmbed)] for inline images in this paragraph."""
    imgs = []
    el = p._element
    names = el.findall(f'.//{{{WP}}}docPr')
    blips = el.findall(f'.//{{{A}}}blip')
    embeds = [b.get(qn('r:embed')) for b in blips]
    for i, emb in enumerate(embeds):
        nm = names[i].get('name') if i < len(names) else None
        imgs.append((nm, emb))
    return imgs


def para_images_ext(p):
    """v2.13 — the STRUCTURED form of para_images(): one dict per inline image,
    carrying its docPr name, its r:embed rid and its docPr alt text (@descr).

    Walks each <w:drawing> as a UNIT and reads that drawing's own docPr + blip,
    rather than zipping two flat document-order lists as para_images() does. The
    zip is correct while every drawing has exactly one docPr and one blip, but a
    paragraph mixing an inline drawing with an anchored one, or a blip carrying
    a <a:blip r:link> alternate, misaligns it. A-FIGALT reads @descr, so a
    misalignment here would attribute one figure's alt text to another.

    para_images() is left BYTE-UNCHANGED: it is read at six call sites that need
    only presence/naming, and its behaviour is fixture-locked.
    """
    out = []
    for dr in p._element.findall(f'.//{W_("drawing")}'):
        nm = dr.find(f'.//{{{WP}}}docPr')
        bl = dr.find(f'.//{{{A}}}blip')
        if bl is None:
            continue
        out.append({'name': (nm.get('name') if nm is not None else None) or '',
                    'descr': (nm.get('descr') if nm is not None else None) or '',
                    'rid': bl.get(qn('r:embed'))})
    return out


def block_image_paras(b):
    """Every paragraph of a block that can carry an inline image, INCLUDING the
    paragraphs inside its tables. Figural options are placed one-per-paragraph
    (S10-8), but a DI chart or a figure/option fusion table puts drawings inside
    table cells, and a block-level paras scan would miss those entirely."""
    seen = set()
    for p in b.paras:
        if id(p._element) not in seen:
            seen.add(id(p._element)); yield p
    for t in b.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if id(p._element) not in seen:
                        seen.add(id(p._element)); yield p


def extract_media(docx_path, media_map):
    """v2.13 — extract every referenced media part to a temp dir and return
    {rid: absolute path}. The twelve figure-conformance gates are arithmetic
    over the saved PNG, so they need a real file on disk; a docx part is a ZIP
    member and PIL cannot open it in place.

    NEVER raises (RA-9 / CLAUDE.md): an unreadable archive degrades to an empty
    map, which the caller reports as a coverage WARN. A figure gate must never
    be the reason a run dies — that is the exact defect class v2.12 closed.
    """
    paths = {}
    try:
        d = tempfile.mkdtemp(prefix='auditmedia_')
        with zipfile.ZipFile(docx_path) as z:
            names = set(z.namelist())
            for rid, base in media_map.items():
                for cand in (f'word/media/{base}', f'media/{base}'):
                    if cand in names:
                        dst = os.path.join(d, f'{rid}_{base}')
                        with open(dst, 'wb') as fh:
                            fh.write(z.read(cand))
                        paths[rid] = dst
                        break
    except Exception:
        return paths
    return paths


def attach_block_images(blocks, media_map, media_paths):
    """v2.13 (D1) — fill Block.images. Returns (declared, resolved): how many
    inline images the paper physically carries, and how many of those have a
    usable PNG on disk. The two are reported separately because 'no figures'
    and 'figures I could not open' are opposite facts, and printing OK for the
    second is the vacuous-pass defect this release exists to close."""
    declared = resolved = 0
    for b in blocks:
        for p in block_image_paras(b):
            for im in para_images_ext(p):
                rid = im.get('rid')
                pth = media_paths.get(rid)
                declared += 1
                if pth:
                    resolved += 1
                b.images.append({'name': im.get('name') or '',
                                 'rid': rid,
                                 'descr': im.get('descr') or '',
                                 'part': media_map.get(rid, ''),
                                 'path': pth})
    return declared, resolved


def resolve_figure_spec(img, specs):
    """v2.13 (D2) — find this image's FigureSpec in the registry-borne map.

    Step 7 stamps every drawing with its canonical name at S10-8
    (_name_last_drawing -> 'q{N}_problem.png' / 'q{N}_opt{i}.png'), and
    write_spec_sidecar() names the sidecar after the same PNG, so the docPr name
    IS the key. Fall back to the extension-stripped form and to the media part
    name so a re-emitted or renamed drawing (CP-IMGNAME) still resolves.

    An unresolved lookup returns {} — which fc.is_legacy() reads as pre-v5.33
    output and EC-V18 then treats leniently. That is the CORRECT default: an
    absent spec must degrade, never fabricate a verdict.
    """
    if not specs:
        return {}
    for k in (img.get('name'), img.get('part')):
        if not k:
            continue
        if k in specs:
            return specs[k] or {}
        stem = os.path.splitext(k)[0]
        if stem in specs:
            return specs[stem] or {}
        if (stem + '.png') in specs:
            return specs[stem + '.png'] or {}
    return {}


def parse_blocks(doc):
    """Split the document body into per-question blocks. Items before the first
    Q.<n> are the title/instruction block (returned separately)."""
    blocks, title_items = [], []
    cur = None
    for kind, obj in iter_block_items(doc):
        if kind == 'p':
            mobj = QNUM_RE.match(para_text(obj))
            if mobj:
                cur = Block(int(mobj.group(1)))
                blocks.append(cur)
        if cur is None:
            title_items.append((kind, obj))
            continue
        cur.items.append((kind, obj))
        if kind == 'p':
            cur.paras.append(obj)
        else:
            cur.tables.append(obj)
    return title_items, blocks


# ---- source-file parsing (exam-agnostic) -----------------------------------
def cat_c(rules_txt, key, default=None):
    mobj = re.search(rf'^[ \t]*{re.escape(key)}[ \t]*[:=][ \t]*(.+?)[ \t]*$',
                     rules_txt, re.M | re.I)
    return mobj.group(1).strip() if mobj else default


def load_sources(args):
    src = {}
    src['blueprint'] = json.load(open(args.blueprint, encoding='utf-8')) if args.blueprint else {}
    src['registry']  = json.load(open(args.registry,  encoding='utf-8')) if args.registry  else {}
    src['manifest']  = json.load(open(args.manifest,  encoding='utf-8')) if args.manifest  else {}
    src['rules_txt'] = open(args.rules, encoding='utf-8').read() if args.rules else ''
    bp = src['blueprint']
    src['total_questions'] = bp.get('total_questions')
    src['sections'] = bp.get('sections', [])
    rt = src['rules_txt']
    src['language']      = (cat_c(rt, 'language', 'english') or 'english').lower()
    src['options_count'] = int(cat_c(rt, 'options_count', '4'))
    src['opt_label_fmt'] = cat_c(rt, 'option_label_format', '1/2/3/4')
    src['font_family']   = cat_c(rt, 'font_family', 'Calibri')
    # OMML-required subtopics present at all?
    src['omml_required_present'] = bool(re.search(r'OMML_required\s*[:=]\s*(true|yes|1)',
                                                  rt, re.I))
    # mock-scoped maps from registry
    N = args.mockN
    reg = src['registry']
    rc  = next((x for x in reg.get('rc_manifests', []) if x.get('mock') == N), None)
    src['passage_linked'] = set(rc.get('passage_linked', [])) if rc else set()
    src['cloze_linked']   = set(rc.get('cloze_linked', []))   if rc else set()
    fig = next((x for x in reg.get('figural_manifests', []) if x.get('mock') == N), None)
    src['figural_qs'] = set(int(q) for q in fig.get('figural_qs', [])) if fig else set()
    # v2.10 (GAP-2026-07-26-003 D2): A-FIGPROFILE needs the object_type Step 7 v5.31
    # recorded per figural question, plus that question's subtopic_id. Both travel in
    # the registry figural_manifest, which Step 8 DOES receive — unlike the answer_key
    # sidecar (S0-1), so no concept_map is required. A pre-v5.31 registry simply has
    # neither key and the gate goes dormant.
    src['figural_object_types'] = (fig.get('object_types') or {}) if fig else {}
    src['figural_subtopics'] = (fig.get('subtopic_ids') or {}) if fig else {}
    # v2.13 (GAP-2026-08-01-FIGSPEC-TRANSPORT D2): the FigureSpec sidecars, keyed
    # by canonical PNG name. figural_core.write_spec_sidecar() drops these beside
    # each PNG in the STEP-7 session's working dir; that dir is internal and is
    # never delivered (S0-1), so without a transport channel Step 8 saw spec=={}
    # on every figure and EC-V18 downgraded every BLOCKING verdict on output that
    # was not, in fact, legacy. The registry is the sanctioned channel — exactly
    # the precedent object_types/subtopic_ids set at v5.31. Absent key => {} =>
    # every figure reads as legacy, which is the correct pre-v5.34 behaviour.
    src['figure_specs'] = (fig.get('figure_specs') or {}) if fig else {}
    # v2.4: section_rules full text for image_role lookups in gate_images
    src['section_rules_text'] = rt   # already loaded at src['rules_txt']
    # v2.4: concept_map — Step 8 does NOT receive the answer_key sidecar (S0-1),
    # so concept_map is unavailable by default. If the answer_key is available
    # (e.g., passed via --key), load it; otherwise empty dict (gate_images falls
    # back to default image_role='stem_and_options' per subtopic).
    src['concept_map'] = {}
    src['answers'] = {}
    if getattr(args, 'key', None) and Path(args.key).exists():
        _key_data = json.load(open(args.key, encoding='utf-8'))
        src['concept_map'] = _key_data.get('concept_map', {})
        src['answers'] = _key_data.get('answers', {})

    # v1.2 — MSQ re-derivation (INDEPENDENT of any Step-7 self-report). Dormant when the
    # blueprint declares no multi subtopics (every value below is empty/zero ⇒ the MSQ
    # gates pass vacuously and behave exactly as v1.1).
    src['multi_present'] = bool(bp.get('multi_present', bp.get('msq_present', False)))  # Phase-0 back-compat
    multi_ids = {s.get('subtopic_id') for s in bp.get('subtopic_list', [])
                 if s.get('answer_cardinality', s.get('answer_mode')) == 'multi'}
    src['multi_subtopic_ids'] = multi_ids
    # expected count of multi-mode questions per section, from THIS mock's allocations.
    mock_entry = next((m for m in bp.get('mocks', []) if m.get('mock') == N), None)

    # v2.9 POSITION-BASED QUESTION TYPE (GAP-2026-07-22-001 §6 FIX, mirrors Step 7 v5.30
    # and Step 11 v1.7 dual-mode pattern):
    # For question-type sections (IIT JAM: Section A=MCQ, B=MSQ, C=NAT), per-subtopic
    # answer_cardinality/answer_type is unreliable — multi_ids/nat_ids from subtopic_list
    # would be empty or incomplete because no single subtopic has majority MSQ/NAT
    # observations. The marking_scheme is authoritative: if it defines >1 distinct
    # question_type, derive expected MSQ/NAT counts from Q-position ranges directly.
    #
    # MODE SELECTION (identical to Step 7/Step 11):
    #   > 1 distinct question_type in marking_scheme → POSITION-BASED
    #   0 or 1 distinct type → SUBTOPIC-BASED (unchanged behavior)
    #
    # For POSITION-BASED mode:
    #   expected_multi_by_section = count of Qs in each section whose marking_scheme says MSQ
    #   expected_nat_by_section = count of Qs in each section whose marking_scheme says NAT
    #   multi_subtopic_ids = ALL subtopics that appear in MSQ ranges (for Part B checks)
    #   nat_subtopic_ids = ALL subtopics that appear in NAT ranges (for A-FIGCOMP stem_only)
    #
    # Backward compatible: 0 or 1 distinct type → exact pre-v2.9 behavior. Covers all
    # existing exams (SSC CGL, MPPSC, etc.) and legacy blueprints with no marking_scheme.
    _bp_ms = bp.get('marking_scheme', [])
    _audit_distinct_q_types = {ms.get('question_type') for ms in _bp_ms
                               if ms.get('question_type')}
    _audit_position_based = len(_audit_distinct_q_types) > 1

    def _audit_type_for_q(qnum):
        """Return question_type for a given Q number from marking_scheme."""
        for ms in _bp_ms:
            qr = ms.get('q_range', [0, 0])
            if qr[0] <= qnum <= qr[1]:
                return ms.get('question_type', 'MCQ')
        return 'MCQ'

    exp = {}
    if _audit_position_based and mock_entry:
        # POSITION-BASED: expected counts from marking_scheme Q-ranges per section
        for sec in mock_entry.get('sections', []):
            sec_name = sec.get('section_name')
            qr = sec.get('q_range', [0, 0])
            msq_count = sum(1 for q in range(qr[0], qr[1] + 1)
                            if _audit_type_for_q(q) == 'MSQ')
            if msq_count:
                exp[sec_name] = msq_count
        # Augment multi_subtopic_ids: for position-based exams, ANY subtopic in an MSQ
        # range is effectively MSQ — add all subtopics allocated to MSQ sections.
        for sec in mock_entry.get('sections', []):
            qr = sec.get('q_range', [0, 0])
            if any(_audit_type_for_q(q) == 'MSQ' for q in range(qr[0], qr[1] + 1)):
                for sa in sec.get('subtopic_allocations', []):
                    sid = sa.get('subtopic_id')
                    if sid:
                        multi_ids.add(sid)
        src['multi_subtopic_ids'] = multi_ids
    elif mock_entry and multi_ids:
        # SUBTOPIC-BASED: unchanged pre-v2.9 behavior
        for sec in mock_entry.get('sections', []):
            c = sum(sa.get('q_count', 0) for sa in sec.get('subtopic_allocations', [])
                    if sa.get('subtopic_id') in multi_ids)
            if c:
                exp[sec.get('section_name')] = c
    src['expected_multi_by_section'] = exp
    # MSQ config (section_rules / blueprint) — read where needed, never from a sidecar.
    mc = bp.get('msq_contract', {})
    src['msq_k_mode'] = mc.get('msq_k_mode', 'variable')
    src['msq_k']      = mc.get('msq_k', None)
    src['msq_allow_aota'] = bool(re.search(r'^\s*msq_allow_aota\s*:\s*true\s*$', rt, re.I | re.M))
    # select-instruction phrases: exam's own (section_rules msq_instruction[_hi]) + universal.
    phrases = []
    for m in re.finditer(r'^\s*msq_instruction(?:_hi)?\s*:\s*(.+?)\s*$', rt, re.I | re.M):
        phrases.append(m.group(1).strip().strip('()'))
    src['msq_instruction_phrases'] = phrases + [
        'one or more', 'may be correct', 'select two', 'select three',
        'select all that apply', 'एक या अधिक']

    # v1.4 — NAT re-derivation (INDEPENDENT of any Step-7 self-report). Dormant when the
    # blueprint declares no numerical subtopics (every value below empty/zero ⇒ the NAT
    # gates pass vacuously and behave exactly as v1.3).
    src['nat_present'] = bool(bp.get('nat_present', False))
    nat_ids = {s.get('subtopic_id') for s in bp.get('subtopic_list', [])
               if s.get('answer_type', 'option') == 'numerical'}
    src['nat_subtopic_ids'] = nat_ids
    # expected count of numerical questions per section, from THIS mock's allocations.
    nexp = {}
    if _audit_position_based and mock_entry:
        # POSITION-BASED: expected NAT counts from marking_scheme Q-ranges per section
        for sec in mock_entry.get('sections', []):
            sec_name = sec.get('section_name')
            qr = sec.get('q_range', [0, 0])
            nat_count = sum(1 for q in range(qr[0], qr[1] + 1)
                            if _audit_type_for_q(q) == 'NAT')
            if nat_count:
                nexp[sec_name] = nat_count
        # Augment nat_subtopic_ids: for position-based exams, ANY subtopic in a NAT
        # range is effectively NAT — add all subtopics allocated to NAT sections.
        # This ensures A-FIGCOMP correctly treats figural NAT Qs as stem_only (line ~4505).
        for sec in mock_entry.get('sections', []):
            qr = sec.get('q_range', [0, 0])
            if any(_audit_type_for_q(q) == 'NAT' for q in range(qr[0], qr[1] + 1)):
                for sa in sec.get('subtopic_allocations', []):
                    sid = sa.get('subtopic_id')
                    if sid:
                        nat_ids.add(sid)
        src['nat_subtopic_ids'] = nat_ids
    elif mock_entry and nat_ids:
        # SUBTOPIC-BASED: unchanged pre-v2.9 behavior
        for sec in mock_entry.get('sections', []):
            c = sum(sa.get('q_count', 0) for sa in sec.get('subtopic_allocations', [])
                    if sa.get('subtopic_id') in nat_ids)
            if c:
                nexp[sec.get('section_name')] = c
    src['expected_nat_by_section'] = nexp
    # v1.4 (ND6): per-question EXPECTED option count from the registry (Step-7 delivery
    # contract, NOT a self-audit sidecar). 0 marks a NAT question. Used to SKIP the option
    # gates for NAT Qs; A-NAT-NOOPT then independently verifies each claimed-NAT Q truly
    # renders 0 options (and A-OPTN still fires if a claimed-MCQ Q renders 0) — so a
    # mislabelled options_by_q cannot let a defect through either direction. {} ⇒ inert.
    src['options_by_q'] = {str(k): v for k, v in
                           reg.get('options_by_q', {}).get(str(N), {}).items()}
    # NAT config (blueprint nat_contract) — read where needed, never from a sidecar.
    nc = bp.get('nat_contract', {})
    src['nat_answer_type'] = nc.get('nat_answer_type', 'real')
    src['nat_tolerance']   = nc.get('nat_tolerance', '0')
    # numerical-entry instruction phrases: exam's own (section_rules nat_instruction[_hi]) + universal.
    nphrases = []
    for m in re.finditer(r'^\s*nat_instruction(?:_hi)?\s*:\s*(.+?)\s*$', rt, re.I | re.M):
        nphrases.append(m.group(1).strip().strip('()'))
    src['nat_instruction_phrases'] = nphrases + [
        'numerical value', 'enter your answer', 'enter the value', 'numerical answer',
        'संख्यात्मक मान']
    # figural stem-cue keywords: exam's own (section_rules figural_cue_keywords) if
    # declared, else a universal default set. RA-9: these are never hardcoded in the gate.
    fcue_m = re.search(r'^\s*figural_cue_keywords\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if fcue_m:
        src['figural_cue_keywords'] = [k.strip().lower() for k in fcue_m.group(1).split(',')]
    # else: gate_images falls back to a built-in default list (see gate_images)
    # escape-reference phrases: if the whole phrase appears in a stem, it references
    # the escape option the phrase implies. Read from section_rules (RA-9);
    # gate_optref falls back to English defaults when absent.
    eref_m = re.search(r'^\s*escape_reference_phrases\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if eref_m:
        src['escape_reference_phrases'] = [t.strip() for t in eref_m.group(1).split(',')]
    # stimulus detection cues: exam's own (section_rules stimulus_cue_patterns) if
    # declared; gate_stimorphan merges them with the built-in English cues. RA-9.
    scue_m = re.search(r'^\s*stimulus_cue_patterns\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if scue_m:
        src['stimulus_cue_patterns'] = [c.strip() for c in scue_m.group(1).split(',')]
    # mock title keyword: exam's own (section_rules mock_title_keyword) if declared,
    # else default 'mock'. RA-9: gate_header reads from src.
    src['mock_title_keyword'] = cat_c(rt, 'mock_title_keyword', 'mock')
    # v2.7: paper_header_block opt-in (gate_header / A-HEADER dormancy). Default OFF — no
    # current section_rules declares it, so the pre-Q.1 body-block ban is absolute.
    src['paper_header_block'] = str(cat_c(rt, 'paper_header_block', '')).strip().lower() \
        in ('true', '1', 'yes', 'on')
    return src


def option_label_family(fmt):
    first = (fmt or '1/2/3/4').split('/')[0].strip().strip('()').strip('.').strip(')')
    if first.isdigit():                         return 'num'
    if re.fullmatch(r'[ivxIVX]+', first):       return 'roman'
    if len(first) == 1 and first.isalpha():     return 'alpha'
    return 'num'

OPT_RE = re.compile(r'^\s*\(?\s*([0-9]+|[A-Za-z]|[ivxIVX]+)\s*\)?\s*[.)]\s+\S')
# bare-or-full option label (figural options are a bare '1.' label paragraph
# followed by an image paragraph; text options are 'label. text').
OPT_LABEL_RE = re.compile(r'^\s*\(?\s*([0-9]+|[A-Za-z]|[ivxIVX]+)\s*\)?\s*[.)](\s|$)')

def option_paras(block):
    """Paragraphs in the block that look like labelled options."""
    out = []
    for p in block.paras:
        t = para_text(p)
        if QNUM_RE.match(t):      # never the Q.<n> line
            continue
        mobj = OPT_RE.match(t)
        if mobj:
            out.append((mobj.group(1), p, t))
    return out


def block_stem_text(block):
    """All non-option paragraph text in the block, with the leading 'Q.<n>'
    token stripped. In the Step-7 format the stem lives ON the Q.<n> line
    (e.g. 'Q.74  Study the following table ...'), so the Q.<n> paragraph must
    be INCLUDED (prefix removed), not excluded."""
    parts = []
    for p in block.paras:
        t = para_text(p)
        if OPT_LABEL_RE.match(t):
            continue
        t = QNUM_RE.sub('', t, count=1).strip()
        if t:
            parts.append(t)
    return ' '.join(parts)


# ============================================================================
# GATES
# ============================================================================
STIMULUS_CUES = re.compile(
    r'\b(the passage|the table|the graph|the chart|the given data|the following '
    r'(table|passage|graph|chart|bar|pie|line|data)|blank\s*\(|according to the '
    r'passage|read the (passage|following passage))\b', re.I)
CROSSREF_RE = re.compile(r'Q\.?\s*\d+\s*(and|to|&|–|-)\s*Q?\.?\s*\d+', re.I)
UNDERLINE_REF = re.compile(r'\bunderlin(e|ed)\b', re.I)
FAKE_UNDERLINE = re.compile(r'\(\s*underlin(e|ed)[^)]*:', re.I)
ESCAPE_TOKENS_DEFAULT = [
    r'no error', r'no improvement', r'none of (these|the above|them)',
    r'all of the above', r'both .+ and ', r'neither .+ nor ']
MATH_TOKEN_NAME = re.compile(r'_(e\d+|eqn|expr|frac|math)\b', re.I)
CANON_IMG_NAME = re.compile(r'^q\d+_(problem|opt\d+|stim)', re.I)
ASCII_CARET = re.compile(r'[A-Za-z0-9]\s*\^\s*[0-9A-Za-z]')
SLASH_FRAC  = re.compile(r'(?<![A-Za-z0-9])\d+\s*/\s*\d+(?![A-Za-z0-9])')


def gate_structure(blocks, src):
    tq = src['total_questions']
    nums = [b.qnum for b in blocks]
    if tq is not None:
        (_ok if len(blocks) == tq else _fail)(
            'A-COUNT', f'{len(blocks)} question blocks (expected {tq}).')
        expected = set(range(1, tq + 1))
        got = set(nums)
        if got == expected:
            _ok('A-SEQ', f'Q-numbers complete 1..{tq}.')
        else:
            miss = sorted(expected - got); extra = sorted(got - expected)
            _fail('A-SEQ', f'missing={miss[:10]} extra={extra[:10]}.')
    else:
        _warn('A-COUNT', 'blueprint.total_questions absent; count check skipped.')
    if nums == sorted(nums) and len(nums) == len(set(nums)):
        _ok('A-MONO', 'Q-numbers strictly increasing.')
    else:
        _fail('A-MONO', 'Q-numbers not strictly increasing in document order.')


def gate_seccount(blocks, src):
    secs = src['sections']
    if not secs:
        _warn('A-SECCOUNT', 'blueprint.sections absent; section-count check skipped.')
        return
    nums = set(b.qnum for b in blocks)
    bad = []
    for s in secs:
        lo, hi = s['q_range']
        cnt = sum(1 for q in nums if lo <= q <= hi)
        if cnt != s.get('total_qs', hi - lo + 1):
            bad.append(f"{s.get('name','?')}:{cnt}/{s.get('total_qs', hi-lo+1)}")
    (_ok if not bad else _fail)('A-SECCOUNT',
        'section counts match q_ranges.' if not bad else 'mismatch ' + '; '.join(bad))


def _label_paras(block):
    """All option-label paragraphs in the block (bare '1.' or full '1. text'),
    in document order, as (token, full_text, text_after_label)."""
    out = []
    for p in block.paras:
        t = para_text(p)
        if QNUM_RE.match(t):
            continue
        m = OPT_LABEL_RE.match(t)
        if m:
            out.append((m.group(1), t, t[m.end():].strip()))
    return out


def _fam_of(l):
    if l.isdigit():
        return 'num'
    if re.fullmatch(r'[ivxIVX]+', l):
        return 'roman'
    return 'alpha'


def _idx_of(l, fam):
    if l.isdigit():
        return int(l)
    if fam == 'roman':
        seq = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        return seq.index(l.lower()) + 1 if l.lower() in seq else 0
    return ord(l.lower()) - ord('a') + 1


def gate_options(blocks, src):
    oc = src['options_count']; fam = option_label_family(src['opt_label_fmt'])
    obq = src.get('options_by_q', {})   # v1.4: per-Q expected option count (0 = NAT)
    bad_n, bad_lab, bad_ord, bad_uni = [], [], [], []
    for b in blocks:
        # v1.4 NAT: a numerical question expects 0 options — the option gates (A-OPTN/
        # A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE) DO NOT APPLY to it. Skip when the registry
        # marks it 0-option; A-NAT-NOOPT separately verifies it truly renders no options.
        if str(b.qnum) in obq and obq[str(b.qnum)] == 0:
            continue
        labs = _label_paras(b)
        # Options are the TRAILING oc label-paragraphs (Step-7 puts the option
        # block last). A stray earlier label (e.g. an enumerated passage point
        # '1. ...') is ignored, so it never inflates the count; a genuinely short
        # option set (< oc labels) still FAILs.
        if len(labs) < oc:
            bad_n.append(f'Q{b.qnum}:{len(labs)}')
            continue
        opt_labs = labs[-oc:]
        tokens = [x[0] for x in opt_labs]
        texts  = [x[2].casefold() for x in opt_labs]
        if any(_fam_of(t) != fam for t in tokens):
            bad_lab.append(f'Q{b.qnum}')
        idxs = [_idx_of(t, fam) for t in tokens]
        if 0 in idxs or idxs != list(range(idxs[0], idxs[0] + oc)):
            bad_ord.append(f'Q{b.qnum}')
        # text-uniqueness applies only when options are TEXT (figural options are
        # bare labels followed by images → empty text → uniqueness checked in §7).
        nonempty = [x for x in texts if x]
        if len(nonempty) == oc and len(set(nonempty)) != oc:
            bad_uni.append(f'Q{b.qnum}')
    (_ok if not bad_n else _fail)('A-OPTN',
        f'every Q has {oc} options.' if not bad_n else 'wrong count: ' + ' '.join(bad_n[:15]))
    (_ok if not bad_lab else _fail)('A-OPTLABEL',
        'labels match format.' if not bad_lab else 'bad label family: ' + ' '.join(bad_lab[:15]))
    (_ok if not bad_ord else _fail)('A-OPTORDER',
        'options in order.' if not bad_ord else 'out of order: ' + ' '.join(bad_ord[:15]))
    (_ok if not bad_uni else _fail)('A-OPTUNIQUE',
        'options distinct within Q.' if not bad_uni else 'dup options: ' + ' '.join(bad_uni[:15]))


def gate_qnfirst(blocks):
    """Q.N-FIRST (R14): nothing may precede a block's Q.<n>. Because the parser
    starts a block at Q.<n>, the violation manifests as stimulus content (table /
    image / long passage) sitting AFTER the previous block's last option and
    BEFORE the next block's Q.<n> — i.e. a lead-in orphaned ahead of its Q.N.
    It is attributed to the block whose Q.<n> it precedes."""
    viol = []
    for k, b in enumerate(blocks):
        last_opt = -1
        for idx, (kind, obj) in enumerate(b.items):
            if kind == 'p' and OPT_RE.match(para_text(obj)):
                last_opt = idx
        if last_opt < 0 or k + 1 >= len(blocks):
            continue
        for kind, obj in b.items[last_opt + 1:]:
            if kind == 't':
                viol.append(f'Q{blocks[k+1].qnum}'); break
            if kind == 'p':
                if para_images(obj):
                    viol.append(f'Q{blocks[k+1].qnum}'); break
                if len(para_text(obj).split()) >= 35:
                    viol.append(f'Q{blocks[k+1].qnum}'); break
    (_ok if not viol else _fail)('A-QNFIRST',
        'every block opens with Q.<n> (no orphaned lead-in).' if not viol else
        'stimulus orphaned before Q.<n>: ' + ' '.join(sorted(set(viol))[:15]))


def gate_blanksep(doc, blocks):
    # blank separator: at least one empty paragraph between the last option of a
    # block and the next block's Q.<n>. Approx: count empty paragraphs overall vs blocks.
    empties = sum(1 for kind, obj in iter_block_items(doc)
                  if kind == 'p' and not para_text(obj).strip()
                  and not para_images(obj))
    (_ok if empties >= max(0, len(blocks) - 1) else _warn)('A-BLANKSEP',
        f'{empties} blank separators for {len(blocks)} blocks.'
        if empties >= len(blocks) - 1 else
        f'only {empties} blank separators for {len(blocks)} blocks (some missing).')


def gate_font(doc, src):
    fam = src['font_family']
    bad = set()
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        for r in obj.runs:
            nm = r.font.name
            if nm not in (None, fam):
                bad.add(nm)
    (_ok if not bad else _fail)('A-FONT',
        f'all runs {fam}.' if not bad else f'non-{fam} fonts present: {sorted(bad)[:6]}')


def gate_sechdr(blocks, doc, src):
    # v1.5 — two detectors, over ALL body paragraphs (not only within question blocks, so a
    # heading before Q.1 or between blocks is seen too):
    #   (a) KEYWORD form — text opening with "section"/"part N"/rule characters;
    #   (b) SECTION-NAME form (the realistic case the keyword pattern MISSED): a standalone
    #       paragraph that IS a declared section name ("Quantitative Aptitude", "Technical",
    #       "General Awareness"). PROVENANCE-BASED — matched against the blueprint's own
    #       section names (src['sections']), not a generic word list, so it flags exactly the
    #       headings this paper's sections would produce and stays exam-agnostic.
    # A questions-only paper (R8, Q.N-first) has no standalone non-Q/non-option paragraph, so
    # any body line equal to a section name is a leaked header, never legitimate content.
    pat = re.compile(r'^\s*(section\b|part\s+[IVXA-D0-9]+\b|=====|─────|-----)', re.I)
    sec_names = set()
    for s in src.get('sections', []):
        nm = (s.get('name') or s.get('section_name') or '').strip().lower()
        if nm:
            sec_names.add(nm)
    hits = []
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        t = para_text(obj).strip()
        if not t or QNUM_RE.match(t):        # blank or a Q.<n> stem line — never a stray header
            continue
        if (pat.match(t) and len(t) < 60) or (t.lower() in sec_names):
            hits.append(t[:40])
    (_ok if not hits else _fail)('A-SECHDR',
        'no body section headers.' if not hits else 'section-header text in body: ' + ' | '.join(hits[:10]))


def gate_anskey(doc):
    full = '\n'.join(para_text(obj) for kind, obj in iter_block_items(doc) if kind == 'p')
    # v1.2: the last pattern now matches SET-valued keys ("Q.1 → 1,2,4"), not just a
    # single trailing digit/letter — mirrors Step 7 G-ANSWERKEY. A leaked MSQ key is a
    # comma/space list of option positions; the v1.1 single-token pattern missed it.
    pats = [r'\banswer\s*key\b', r'\banswers?\s*:', r'^\s*key\s*:',
            r'Q\.?\s*\d+\s*[:\-–>]+\s*[\(]?[1-9a-dA-D][\)]?(?:\s*[,\s]\s*[\(]?[1-9a-dA-D][\)]?)*\s*$',
            # v1.4: NAT numerical-value answer-key lines ("Q.5 → 47" / "→ 0" / "→ -3" /
            # "→ 3.14"). The option-position pattern above only matches 1-9/a-d, so a leaked
            # NAT key (incl. 0/negative/decimal) slipped through. Mirrors Step 7 v4.7.
            r'Q\.?\s*\d+\s*[:\-–>]+\s*-?\d+(?:\.\d+)?\s*$']
    hit = [p for p in pats if re.search(p, full, re.I | re.M)]
    (_ok if not hit else _fail)('A-ANSKEY',
        'no answer key/markers in body.' if not hit else f'answer-key signal(s): {hit}')


def gate_msq_instr(blocks, src):
    # v1.2 — A-MSQ-INSTR (machine, MULTI only). INDEPENDENT of any Step-7 self-report:
    # the EXPECTED number of multi-mode questions per section is re-derived from the
    # blueprint allocations (src['expected_multi_by_section']); the OBSERVED number is
    # the count of Q blocks in that section's q_range whose stem line carries a select-
    # instruction phrase. A mismatch means a multi Q is missing its instruction (or a
    # single Q wrongly carries one). Pinpointing WHICH Q is refined in Part B (semantic),
    # where the question's subtopic is known from content. Fully dormant when the blueprint
    # declares no multi subtopics (expected map empty ⇒ pass).
    exp = src.get('expected_multi_by_section', {})
    if not exp:
        return _ok('A-MSQ-INSTR', 'no multi-mode subtopics in this mock (dormant).')
    phrases = [p.lower() for p in src.get('msq_instruction_phrases', [])]
    sec_of = src.get('section_of_qnum', {})    # {qnum: section_name} if available
    secs   = src.get('sections', [])
    def section_for(qnum):
        if qnum in sec_of:
            return sec_of[qnum]
        for s in secs:                          # fall back to q_range membership
            lo, hi = (s.get('q_range') or [0, 0])[:2]
            if lo <= qnum <= hi:
                return s.get('section_name') or s.get('name')   # blueprint uses 'name'
        return None
    observed = {}
    for b in blocks:
        stem = para_text(b.paras[0]) if getattr(b, 'paras', None) else getattr(b, 'stem', '')
        if any(ph in stem.lower() for ph in phrases):
            observed[section_for(b.qnum)] = observed.get(section_for(b.qnum), 0) + 1
    bad = [f'{sec}: expected {n} multi, saw {observed.get(sec, 0)} instruction-carrying'
           for sec, n in exp.items() if observed.get(sec, 0) != n]
    (_ok if not bad else _fail)('A-MSQ-INSTR',
        'observed multi instruction counts match the blueprint per section.' if not bad
        else 'multi instruction-count mismatch — ' + ' | '.join(bad))


def gate_nat(blocks, src):
    # v1.4 — A-NAT-NOOPT + A-NAT-INSTR (machine, NUMERICAL only). INDEPENDENT of any
    # Step-7 self-report. Fully dormant when the blueprint declares no numerical subtopics.
    obq = src.get('options_by_q', {})
    nat_present = src.get('nat_present', False)
    # A-NAT-NOOPT: every question the registry marks 0-option (NAT) must render ZERO
    # option-label paragraphs. A-OPTN covers the inverse (a claimed-MCQ Q with too few
    # options) — and if options_by_q is absent, NAT Qs are NOT skipped there, so A-OPTN
    # fails LOUD, surfacing the missing ND6 contract rather than silently passing.
    if nat_present and obq:
        bad_opt = []
        for b in blocks:
            if obq.get(str(b.qnum)) == 0 and len(_label_paras(b)) != 0:
                bad_opt.append(f'Q{b.qnum}:{len(_label_paras(b))}')
        (_ok if not bad_opt else _fail)('A-NAT-NOOPT',
            'every numerical Q renders zero options.' if not bad_opt
            else 'numerical Q carries options: ' + ' '.join(bad_opt[:15]))
    else:
        _ok('A-NAT-NOOPT', 'no numerical subtopics in this mock (dormant).')
    # v2.8 — A-NAT-GRADE (machine, NUMERICAL only): self-consistency backstop for the
    # portal grading transform (S7-NEW-C). Re-runs derive_nat_grading() on the SIDECAR's
    # OWN recorded (nat_value, ca_range) and checks the result matches the sidecar's OWN
    # recorded (nat_grading_type, nat_grading_value) EXACTLY. This does NOT re-derive the
    # math value from the stem (that is A-NAT-ANSWER's Claude-derivation job, run
    # separately in Phase 2) — it only proves Step 7's own execution of the SAME function
    # this file also embeds actually ran correctly and wasn't hand-edited or bypassed.
    # PINNED: this function body MUST stay byte-identical to Framework_MockTestCreate.md
    # §S7-NEW-C derive_nat_grading() — never re-implemented independently (anti-drift).
    # NOTE: placed BEFORE A-NAT-INSTR deliberately — A-NAT-INSTR has an early `return` on
    # its own dormant path, which would silently skip any code placed after it.
    from decimal import Decimal, ROUND_HALF_UP
    _NAT_GRADE_CHARSET = frozenset('0123456789.-')
    _NAT_INTEGRAL_EPS = Decimal('1e-9')
    def _fmt_portal_number(value, precision=None):
        d = Decimal(str(value))
        if precision is not None:
            q = Decimal(1).scaleb(-precision)
            d = d.quantize(q, rounding=ROUND_HALF_UP)
            s = format(d, 'f')
        else:
            if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
                s = str(int(d.to_integral_value()))
            else:
                s = format(d.normalize(), 'f')
        if re.fullmatch(r'-0(\.0+)?', s):
            s = s.lstrip('-')
        return s
    def _fmt_portal_range(lo, hi, precision=None):
        lo_s = _fmt_portal_number(lo, precision); hi_s = _fmt_portal_number(hi, precision)
        if lo_s.startswith('-') or hi_s.startswith('-'):
            raise ValueError(f'NOT SUPPORTED negative-bound range lo={lo_s} hi={hi_s}')
        if Decimal(lo_s) > Decimal(hi_s):
            raise ValueError(f'lo>hi {lo_s} {hi_s}')
        return f'{lo_s}-{hi_s}'
    def _derive_nat_grading(value, ca_range=None, stem_precision=None):
        if stem_precision is not None:
            if ca_range is not None:
                lo, hi = ca_range
                return ('range', _fmt_portal_range(lo, hi, precision=stem_precision))
            return ('decimal_fixed', _fmt_portal_number(value, precision=stem_precision))
        if ca_range is not None:
            lo, hi = ca_range
            return ('range', _fmt_portal_range(lo, hi, precision=None))
        d = Decimal(str(value))
        if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
            v_int = int(d.to_integral_value())
            return (('positive_integer', str(v_int)) if v_int >= 0 else ('integer', str(v_int)))
        return ('decimal', _fmt_portal_number(value, precision=None))
    if not nat_present:
        _ok('A-NAT-GRADE', 'no numerical subtopics in this mock (dormant).')
    elif not src.get('concept_map'):
        # Step 8 does not receive the answer_key sidecar by default (S0-1) — this
        # self-consistency backstop is only checkable when --key is supplied,
        # exactly like the concept_map-dependent parts of gate_images.
        _ok('A-NAT-GRADE', 'answer_key sidecar not supplied via --key (dormant).')
    else:
        cmap = src.get('concept_map', {})
        answers = src.get('answers', {})
        bad_grade = []
        for b in blocks:
            entry = cmap.get(str(b.qnum), {})
            if entry.get('qtype') != 'nat':
                continue
            nat_value = answers.get(str(b.qnum))
            ca_range = entry.get('ca_range')
            g_type = entry.get('nat_grading_type'); g_val = entry.get('nat_grading_value')
            if nat_value is None:
                bad_grade.append(f'Q{b.qnum}: nat_value missing from sidecar answers'); continue
            if g_val is None:
                bad_grade.append(f'Q{b.qnum}: nat_grading_value missing from sidecar'); continue
            bad_chars = sorted(set(str(g_val)) - _NAT_GRADE_CHARSET)
            if bad_chars:
                bad_grade.append(f'Q{b.qnum}: nat_grading_value {g_val!r} has banned chars {bad_chars}')
                continue
            try:
                re_type, re_val = _derive_nat_grading(
                    nat_value, tuple(ca_range) if ca_range is not None else None,
                    stem_precision=entry.get('stem_precision'))
            except ValueError as e:
                bad_grade.append(f'Q{b.qnum}: re-derivation raised: {e}'); continue
            if (re_type, re_val) != (g_type, g_val):
                bad_grade.append(f'Q{b.qnum}: sidecar says ({g_type!r},{g_val!r}), '
                                  f're-derived ({re_type!r},{re_val!r})')
        (_ok if not bad_grade else _fail)('A-NAT-GRADE',
            'every NAT grading value is self-consistent and charset-pure.' if not bad_grade
            else 'grading value defect(s): ' + ' | '.join(bad_grade[:15]))
    # A-NAT-INSTR: per-section EXPECTED NAT count (re-derived from blueprint allocations,
    # src['expected_nat_by_section']) vs OBSERVED count of Q blocks whose stem carries a
    # numerical-entry instruction phrase. Mismatch ⇒ a NAT Q missing its instruction (or a
    # non-NAT Q wrongly carrying one). Mirrors A-MSQ-INSTR. Dormant when the map is empty.
    exp = src.get('expected_nat_by_section', {})
    if not exp:
        return _ok('A-NAT-INSTR', 'no numerical subtopics in this mock (dormant).')
    phrases = [p.lower() for p in src.get('nat_instruction_phrases', [])]
    secs   = src.get('sections', [])
    sec_of = src.get('section_of_qnum', {})
    def section_for(qnum):
        if qnum in sec_of:
            return sec_of[qnum]
        for s in secs:
            lo, hi = (s.get('q_range') or [0, 0])[:2]
            if lo <= qnum <= hi:
                return s.get('section_name') or s.get('name')
        return None
    observed = {}
    for b in blocks:
        stem = para_text(b.paras[0]) if getattr(b, 'paras', None) else getattr(b, 'stem', '')
        if any(ph in stem.lower() for ph in phrases):
            observed[section_for(b.qnum)] = observed.get(section_for(b.qnum), 0) + 1
    bad = [f'{sec}: expected {n} NAT, saw {observed.get(sec, 0)} instruction-carrying'
           for sec, n in exp.items() if observed.get(sec, 0) != n]
    (_ok if not bad else _fail)('A-NAT-INSTR',
        'observed numerical instruction counts match the blueprint per section.' if not bad
        else 'numerical instruction-count mismatch — ' + ' | '.join(bad))





def gate_stimorphan(blocks, src):
    linked = src['passage_linked'] | src['cloze_linked']
    # Merge section_rules stimulus cues (if declared) with the built-in English set (RA-9).
    extra_pats = src.get('stimulus_cue_patterns', [])
    cue_re = STIMULUS_CUES
    if extra_pats:
        combined = STIMULUS_CUES.pattern + '|' + '|'.join(r'\b' + p + r'\b' for p in extra_pats)
        cue_re = re.compile(combined, re.I)
    orphan, crossref = [], []
    bynum = {b.qnum: b for b in blocks}
    for b in blocks:
        stem = block_stem_text(b)
        if CROSSREF_RE.search(' '.join(para_text(p) for p in b.paras)):
            crossref.append(f'Q{b.qnum}')
        refs_stim = bool(cue_re.search(stem)) or (b.qnum in linked)
        if refs_stim:
            has_tbl = len(b.tables) > 0
            has_img = any(para_images(p) for p in b.paras)
            has_long = any(len(para_text(p).split()) >= 35 for p in b.paras)
            if not (has_tbl or has_img or has_long):
                orphan.append(f'Q{b.qnum}')
    (_ok if not orphan else _fail)('A-STIMORPHAN',
        'linked members carry their stimulus.' if not orphan else
        'orphaned stimulus (no embedded table/image/passage): ' + ' '.join(orphan[:12]))
    if crossref:
        _fail('A-STIMORPHAN-XREF', 'cross-question reference in stem: ' + ' '.join(crossref[:12]))
    else:
        _ok('A-STIMORPHAN-XREF', 'no "Q.x and Q.y" cross-references.')


# ── self-contained MATCH detector for the machine gate (v2.7.1) ────────────────
# The runnable audit.py (this block) is standalone and does NOT import the S6-1b spec
# classifier, so A-MATCH-TABLE carries its OWN detector. It MIRRORS the S6-1b classifier's
# MATCH rules EXACTLY (keyword rules + cross-domain label-pair option shape) — both live in
# THIS file (S6-1b + here); if one changes the other MUST match. Kept minimal: only the
# MATCH decision is needed here, not the full 8-class ladder.
_MT_PAIR_RE = re.compile(r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
                         r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MT_SUB = (r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
           r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MT_OPT_RE = re.compile(r'^\s*' + _MT_SUB + r'(?:[,;\s]+' + _MT_SUB + r'){1,}\s*$')

def _mt_family(tokens):
    low = [x.lower() for x in tokens if x]
    if not low:
        return 'other'
    if all(re.fullmatch(r'\d{1,2}', x) for x in low):
        return 'digit'
    romanish = all(re.fullmatch(r'[ivxlcdm]+', x) for x in low)
    if romanish and any(len(x) > 1 for x in low):
        return 'roman'
    if all(re.fullmatch(r'[a-z]', x) for x in low):
        return 'roman' if set(low) <= {'i', 'v', 'x'} else 'alpha'
    if romanish:
        return 'roman'
    if all(re.fullmatch(r'[a-z]{1,4}', x) for x in low):
        return 'alpha'
    return 'other'

def _opts_match_pairs(opts):
    if not opts:
        return False
    hits = 0
    for o in opts:
        s = (o or '').strip()
        if not s or not _MT_OPT_RE.match(s):
            continue
        pairs = _MT_PAIR_RE.findall(s)
        if len(pairs) < 2:
            continue
        lf = _mt_family([p[0] for p in pairs])
        rf = _mt_family([p[1] for p in pairs])
        if lf == rf or 'other' in (lf, rf):
            continue
        hits += 1
    return hits >= max(2, (len(opts) + 1) // 2)

def _block_is_match(stem, opts):
    # Mirror the S6-1b ladder precedence: ASSERTION_REASON outranks MATCH, so an
    # assertion/reason stem is NOT a match even if its options look like pairs. (LINKED also
    # outranks MATCH; the gate skips linked members via src, below.)
    s = (stem or '').lower()
    if re.search(r'\bassertion\b', s) and re.search(r'\breason\b', s):
        return False
    if re.search(r'\bmatch\b', s) and re.search(r'\b(following|list|column|set)\b', s):
        return True
    if re.search(r'list[\s\-]*i\b|column[\s\-]*(i|a)\b', s):
        return True
    return _opts_match_pairs(opts)


def gate_match_table(blocks, src):
    """A-MATCH-TABLE (v2.7.1) — executable promotion of the S7-3 'MATRICES & MATCH-THE-COLUMN
    must be a REAL grid' checklist item. For every block re-derived as Axis-2 MATCH by the
    SHARED classifier (S6-1b — the SAME functions Step 5 and Step 7 use), the List columns
    MUST render as a real <w:tbl>. A match rendered as plain text lines (or space/tab pseudo-
    columns) is a format-fidelity defect: S6-6 still counts the MATCH format PRESENT while the
    skill is left un-rehearsed — a false readiness signal. Exam-agnostic: the MATCH signal is
    language-independent (keyword OR cross-domain option shape), never a hardcoded exam label."""
    if not blocks:
        return
    oc = src.get('options_count', 4)
    linked = src.get('passage_linked', set()) | src.get('cloze_linked', set())
    missing = []
    for b in blocks:
        if b.qnum in linked:          # LINKED outranks MATCH (S6-1b); A-STIMORPHAN covers it
            continue
        labs = _label_paras(b)
        opts = [x[2] for x in (labs[-oc:] if len(labs) >= oc else labs)]
        if _block_is_match(block_stem_text(b), opts):
            if not b.tables:
                missing.append(f'Q{b.qnum}')
    (_ok if not missing else _fail)('A-MATCH-TABLE',
        'every MATCH question renders its List columns as a real table.' if not missing else
        'MATCH question(s) rendered without a <w:tbl> grid (S7-3 defect — rebuild the List '
        'body as a real table, never text/space columns): ' + ' '.join(missing[:15]))


def gate_underline(blocks):
    missing, fake = [], []
    for b in blocks:
        whole = ' '.join(para_text(p) for p in b.paras)
        if FAKE_UNDERLINE.search(whole):
            fake.append(f'Q{b.qnum}')
        if UNDERLINE_REF.search(' '.join(para_text(p) for p in b.paras[:3])):
            # require a real w:u run somewhere in the block
            has_u = False
            for p in b.paras:
                for u in p._element.iter(W_('u')):
                    val = u.get(W_('val'))
                    if val not in ('none',):
                        has_u = True
                        break
                if has_u:
                    break
            if not has_u:
                missing.append(f'Q{b.qnum}')
    (_ok if not missing else _fail)('A-UNDERLINE',
        'underline-class Qs use real <w:u>.' if not missing else
        'no real underline run: ' + ' '.join(missing[:12]))
    if fake:
        _fail('A-UNDERLINE-FAKE', '"(underlined: X)" annotation present: ' + ' '.join(fake[:12]))
    else:
        _ok('A-UNDERLINE-FAKE', 'no faked-underline annotations.')


def gate_omml(doc, src, final):
    nfrac_bad, yearfrac = [], []
    n_omath = 0
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        for om in obj._element.iter(M_('oMath')):
            n_omath += 1
        for f in obj._element.iter(M_('f')):
            num = f.find(M_('num')); den = f.find(M_('den'))
            num_t = ''.join(t.text or '' for t in (num.iter(M_('t')) if num is not None else []))
            den_t = ''.join(t.text or '' for t in (den.iter(M_('t')) if den is not None else []))
            if not num_t.strip() or not den_t.strip():
                nfrac_bad.append('empty-frac')
            if re.fullmatch(r'\s*20\d\d\s*', num_t) and re.fullmatch(r'\s*\d{2}\s*', den_t):
                yearfrac.append(f'{num_t.strip()}/{den_t.strip()}')
    (_ok if not nfrac_bad else _fail)('A-OMML',
        f'{n_omath} oMath; all fractions well-formed.' if not nfrac_bad else
        f'{len(nfrac_bad)} fraction(s) with empty num/den.')
    if yearfrac:
        _warn('A-OMML-YEAR', f'year-range rendered as stacked fraction: {yearfrac[:6]}')
    if final and src['omml_required_present'] and n_omath == 0:
        _warn('A-OMML-FLOOR',
              'OMML_required subtopic(s) declared but ZERO <m:oMath> in paper — '
              'built-up math may be hiding as ASCII/raster; investigate (S7-5).')
    elif final and src['omml_required_present']:
        _ok('A-OMML-FLOOR', f'OMML floor satisfied ({n_omath} oMath).')


def gate_frac_ascii(blocks, src):
    caret, slash = [], []
    omml_ctx = src['omml_required_present']
    for b in blocks:
        stem = block_stem_text(b)
        if ASCII_CARET.search(stem):
            caret.append(f'Q{b.qnum}')
        if omml_ctx and SLASH_FRAC.search(stem):
            slash.append(f'Q{b.qnum}')
    (_ok if not caret else _fail)('A-FRAC',
        'no ASCII caret exponents.' if not caret else 'ASCII "^" exponent: ' + ' '.join(caret[:12]))
    if slash:
        _warn('A-FRAC-SLASH', 'slash fraction in math-context stem (view in Part B): '
              + ' '.join(slash[:12]))


def gate_images(blocks, src, media_map):
    """A-MATHRASTER (Tier 1) + A-FIGCOMP (structural, v2.4 image_role-aware)
    + A-FIGTEXT-PROSE (v2.4 — visual prose detector)."""
    math_raster, warn_view, composite, multi_per_line = [], [], [], []
    figtext_prose = []   # v2.4: figure-reference text in zero-image blocks
    fig = src['figural_qs']
    oc = src['options_count']
    # v2.4: read image_role per subtopic from section_rules
    sr_text = src.get('section_rules_text', '')
    concept_map = src.get('concept_map', {})
    # v2.4: figure-reference pattern for prose detector
    _fig_ref_re = re.compile(
        r'(?i)\b(in the given figure|in the following figure|'
        r'from the (given|following) (figure|diagram)|'
        r'figure \(X\)|the figure (shows|below|above)|'
        r'how many .{0,30}(triangles|squares|circles|lines|shapes|'
        r'angles|sides|regions|parts)\s+(are|in|does|can))')
    for b in blocks:
        block_imgs = []
        for p in b.paras:
            pim = para_images(p)
            if len(pim) >= 2:
                multi_per_line.append(f'Q{b.qnum}')
            for nm, emb in pim:
                tgt = media_map.get(emb, '')
                block_imgs.append((nm or '', tgt))
        # v2.4: A-FIGTEXT-PROSE — zero-image blocks referencing figures
        if not block_imgs:
            stem = ' '.join(para_text(p) for p in b.paras)
            if _fig_ref_re.search(stem):
                figtext_prose.append(f'Q{b.qnum}')
            continue
        stem = ' '.join(para_text(p) for p in b.paras[:3])
        math_ctx = src['omml_required_present']  # coarse; refined in Part B
        for nm, tgt in block_imgs:
            hay = f'{nm} {tgt}'
            if MATH_TOKEN_NAME.search(hay):
                math_raster.append(f'Q{b.qnum}')
            elif not CANON_IMG_NAME.match(nm or ''):
                warn_view.append(f'Q{b.qnum}')
        # A-FIGCOMP (v2.4 — image_role-aware):
        # Determine image_role for this question
        figural_cues = src.get('figural_cue_keywords',
                              ['which of the', 'odd one', 'mirror', 'water image',
                               'embedded', 'complete the', 'series', 'fold'])
        is_figural = b.qnum in fig or any(k in stem.lower() for k in figural_cues)
        if is_figural:
            # v2.4: determine image_role from section_rules via concept_map
            _q_role = 'stem_and_options'   # default
            qnum_str = str(b.qnum)
            if qnum_str in concept_map and sr_text:
                _sid = concept_map[qnum_str].get('subtopic_id', '')
                if _sid:
                    _rm = re.search(
                        r'subtopic_id:\s*' + re.escape(_sid) +
                        r'((?:(?!subtopic_id:).)*?)image_role:\s*(\S+)',
                        sr_text, re.DOTALL)
                    if _rm:
                        _q_role = _rm.group(2)
            # Also check NAT: if this Q's subtopic is in nat_subtopic_ids → stem_only
            _nat_ids = src.get('nat_subtopic_ids', set())
            if _nat_ids and qnum_str in concept_map:
                _q_sid = concept_map[qnum_str].get('subtopic_id', '')
                if _q_sid in _nat_ids:
                    _q_role = 'stem_only'
            # Branch by image_role
            if _q_role == 'stem_only':
                if len(block_imgs) < 1:
                    composite.append(f'Q{b.qnum}(stem_only:0img)')
                # 1 image IS correct for stem_only — do NOT flag as composite
            elif _q_role == 'options_only':
                n_opt = oc   # oc is int (exam-wide OPTIONS_COUNT from section_rules)
                if len(block_imgs) < n_opt:
                    composite.append(f'Q{b.qnum}(opts_only:{len(block_imgs)}<{n_opt})')
            else:   # stem_and_options (default)
                if len(block_imgs) == 1:
                    composite.append(f'Q{b.qnum}')
    (_ok if not math_raster else _fail)('A-MATHRASTER',
        'no math-token raster names.' if not math_raster else
        'image named like a math raster: ' + ' '.join(sorted(set(math_raster))[:12]))
    if warn_view:
        _warn('A-MATHRASTER-VIEW',
              f'{len(set(warn_view))} block(s) have non-canonically-named images — '
              'VIEW in Part B (§7) to confirm figure vs math raster: '
              + ' '.join(sorted(set(warn_view))[:12]))
    if multi_per_line:
        _fail('A-FIGCOMP-LINE', 'multiple images on one line (option-per-line broken): '
              + ' '.join(sorted(set(multi_per_line))[:12]))
    else:
        _ok('A-FIGCOMP-LINE', 'at most one image per line.')
    if composite:
        _warn('A-FIGCOMP',
              'figural block image-count mismatch (per image_role) — '
              'VIEW + fix in Part B: ' + ' '.join(sorted(set(composite))[:12]))
    else:
        _ok('A-FIGCOMP', 'figural blocks pass image_role-aware check (v2.4).')

    # ── A-FIGPROFILE (v2.10, GAP-2026-07-26-003 D2) ──────────────────────────
    # Did generation honour the figure profile Step 5 measured? The verdict is
    # DELEGATED to bc.check_figural_conformance(), the same function Step 7 v5.31
    # generates against, so the generator and its auditor cannot drift apart.
    #
    # AUDITS RECORDED INTENT, NOT PIXELS. Confirming a render truly depicts a
    # micrograph needs a view(), which is CLASS T and cannot run inside this python
    # (EXECUTION-BOUNDARY LAW). Intent is deterministic and catches the failure that
    # matters: Step 7 ignoring the profile.
    #
    # SOURCES, both of which Step 8 actually receives (S0-1):
    #   registry figural_manifests[mock].object_types  {qnum: type, ...}  (v5.31+)
    #   section_rules TEXT -> bc.parse_image_analysis_blocks()
    # Step 8 does NOT receive the answer_key sidecar, so no concept_map is used here;
    # subtopic_id travels with each figural_qs record instead.
    _fig_types = src.get('figural_object_types') or {}
    _fig_subs = src.get('figural_subtopics') or {}
    if not _fig_types:
        # Pre-v5.31 registry, or a mock with no figural questions. Dormant, exactly
        # like the concept_map-dependent gates above — never a FAIL for a missing
        # optional input (EC-V18).
        _ok('A-FIGPROFILE',
            'registry carries no per-question object_types (pre-v5.31 mock) — dormant.')
    else:
        # ── FIX GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING (D1/D2) — v2.12 ──────
        # BIND THE ENGINE. Until v2.12 `bc` was READ at three sites and BOUND at
        # none: the v2.10 delegation was written into the comments and the call
        # sites, but the import was never added. Any registry carrying
        # object_types (Step 7 v5.31+) raised NameError out of gate_images() and
        # killed the whole run before a single gate line printed.
        #
        # THREE-LAYER GUARD (each layer closes a distinct crash path; an import
        # guard alone is NOT sufficient — measured, not assumed):
        #   L1 IMPORT     except Exception, NOT except ImportError. A truncated
        #                 engine (project-knowledge size caps — blueprint_core.py
        #                 is ~168 KB, exactly the range P0.5 exists for) raises
        #                 SyntaxError, which ImportError does not catch.
        #   L2 CAPABILITY hasattr() on all three delegated functions. A stale
        #                 engine imports cleanly and then raises AttributeError at
        #                 the call site — a crash the import guard never sees.
        #   L3 CALL SITE  the delegated calls run inside try/except Exception, so
        #                 a raise INSIDE the engine degrades to a reported skip
        #                 instead of aborting the audit.
        #
        # SEVERITY IS _warn, DELIBERATELY:
        #   not _ok   — the gate DID NOT RUN; reporting it green is the silent-pass
        #               failure the v1.8 DeliveryFooter quality gate exists to kill.
        #   not _fail — a missing/broken ENGINE is an environment condition, not a
        #               paper defect, and must never block delivery of a sound
        #               paper (EC-V18 tolerance; owner directive: no dependency
        #               condition may halt a run).
        _BC_FNS = ('parse_image_analysis_blocks',
                   'figural_generation_profile',
                   'check_figural_conformance')
        try:
            import blueprint_core as bc          # L1
        except Exception as _e:
            bc = None
            _bc_why = f'{type(_e).__name__}: {_e}'
        else:
            _bc_missing = [_f for _f in _BC_FNS if not hasattr(bc, _f)]   # L2
            if _bc_missing:
                _bc_why = ('stale engine — missing ' + ', '.join(_bc_missing))
                bc = None
            else:
                _bc_why = ''
        if bc is None:
            _warn('A-FIGPROFILE',
                  'blueprint_core engine unavailable — figure-profile conformance '
                  f'NOT CHECKED (dependency degraded: {_bc_why}). Logged skip; '
                  'audit continues (RA-9).')
        else:
            try:                                                          # L3
                _sr_blocks = bc.parse_image_analysis_blocks(
                    src.get('section_rules_text', '') or '')
                _by_sub = {}
                for _qn, _ty in _fig_types.items():
                    _sid = _fig_subs.get(str(_qn))
                    if _sid:
                        _by_sub.setdefault(_sid, []).append(_ty)
                _fig_bad, _fig_ok, _fig_skip = [], 0, 0
                for _sid, _gen_types in sorted(_by_sub.items()):
                    _prof = bc.figural_generation_profile(_sr_blocks.get(_sid))
                    _verdict, _detail = bc.check_figural_conformance(_gen_types, _prof)
                    if _verdict == 'FAIL':
                        _fig_bad.append(f'{_sid}: {_detail}')
                    elif _verdict == 'PASS':
                        _fig_ok += 1
                    else:
                        _fig_skip += 1
            except Exception as _e:
                _warn('A-FIGPROFILE',
                      'blueprint_core raised during conformance evaluation — '
                      f'figure-profile conformance NOT CHECKED ({type(_e).__name__}: '
                      f'{_e}). Logged skip; audit continues (RA-9).')
            else:
                if _fig_bad:
                    _fail('A-FIGPROFILE',
                          'generated figure types do not match the measured PYQ profile — '
                          + ' | '.join(_fig_bad[:4]))
                elif not _by_sub:
                    # 0/0 is NOT evidence of conformance (edge case 6). The registry
                    # carried object_types but no usable subtopic_ids, so nothing was
                    # actually judged. Reporting _ok here would claim coverage the
                    # gate never had.
                    _warn('A-FIGPROFILE',
                          'registry carries object_types but no usable subtopic_ids — '
                          '0 subtopic(s) evaluated; conformance NOT ESTABLISHED '
                          '(manifest incomplete).')
                else:
                    _ok('A-FIGPROFILE',
                        f'{_fig_ok} subtopic(s) conform to the measured figure profile; '
                        f'{_fig_skip} skipped (no usable profile — EC-V18).')
    # v2.4: A-FIGTEXT-PROSE — figure-reference text in zero-image blocks
    if figtext_prose:
        _fail('A-FIGTEXT-PROSE',
              'Q-block references a figure but contains 0 images — '
              'render the figure or replace the subtopic (S7-NEW-B): '
              + ' '.join(sorted(set(figtext_prose))[:12]))
    else:
        _ok('A-FIGTEXT-PROSE', 'no figure-reference prose in zero-image blocks.')

    # ── v2.11 FIGURE CONFORMANCE — 12 gates (GAP-2026-07-29-FIG-R2) ──────────
    # Every check below is DETERMINISTIC arithmetic over the saved PNG and its
    # FigureSpec sidecar, and is therefore legal inside this python block. This
    # is the correction to the reasoning that let the defect ship: A-FIGPROFILE
    # rightly declines pixels because "does this depict a micrograph" needs a
    # view() (CLASS T), and that one true fact was generalised to every figure
    # property. None of these twelve needs eyes.
    #
    # SEVERITY. No colour condition may EVER halt a run (owner directive; and
    # CLAUDE.md: "A CLASS T failure must be LOUD, and must NOT halt... Silence is
    # the defect; a halt is not the remedy"). fc.triage() sorts findings into
    # AMBER / VOID_ITEM / BLOCKING, applies EC-V18 legacy tolerance, and NEVER
    # raises. A grey figure is a DEGRADED paper, never a void one.
    # ── FIX GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING (D3) — v2.12 ────────────
    # except Exception, not except ImportError: a TRUNCATED figural_core.py
    # raises SyntaxError and the old guard let it kill the run — the same crash
    # path D1 produced, one engine over.
    try:
        import figural_core as fc
    except Exception as _e:
        fc = None
        _fc_why = f'{type(_e).__name__}: {_e}'
    else:
        _fc_why = ''
    if fc is None:
        # LOUD DEGRADATION, ONE LINE PER GATE (D3). Until v2.12 a single
        # self-naming A-FIGSCALE WARN stood in for all twelve, so ELEVEN gates —
        # including A-FIGMONO (VOID_ITEM, an answer-cue leak) and A-FIGDEGEN
        # (BLOCKING) — vanished from STDOUT with no line at all. A reader could
        # not tell they had not been evaluated. That is precisely the silence
        # CLAUDE.md forbids: "Silence is the defect; a halt is not the remedy."
        # Emitting all twelve also makes the printed gate roster INVARIANT
        # regardless of environment, which restores §R15 reproducibility and
        # makes the gate count itself a usable integrity signal.
        for _g in ('A-FIGSCALE', 'A-FIGLABEL', 'A-FIGDPI', 'A-FIGDEGEN',
                   'A-FIGMONO', 'A-FIGOPTUNIF', 'A-FIGCOLOUR', 'A-FIGCVD',
                   'A-FIGSERIES', 'A-FIGGLYPH', 'A-FIGALT', 'A-FIGLABELPX'):
            _warn(_g, 'figural_core engine unavailable — gate NOT RUN '
                      f'(dependency degraded: {_fc_why}).')
    else:
        _fig_specs = src.get('figure_specs') or {}
        _amber, _void, _block = [], [], []
        _seen, _legacy_n = 0, 0
        _declared, _unusable = 0, 0
        for _blk in blocks:
            for _img in (getattr(_blk, 'images', None) or []):
                _declared += 1
                _png = _img.get('path')
                if not _png:
                    continue
                _spec = resolve_figure_spec(_img, _fig_specs)
                # ── v2.13: PER-FIGURE L3 GUARD (the three-layer pattern v2.12
                # established for blueprint_core, applied to figural_core's
                # PER-ITEM calls). The spec now arrives from the REGISTRY, i.e.
                # from outside this process, and a partially-recorded one raises:
                # render_figure() mutates font_pt_native/png_px/placement_scale
                # only after it reads the artefact back, so a render that died
                # mid-way leaves a spec whose shape the gates index into. Caught
                # empirically — one such figure raised TypeError out of
                # g_figlabel(), _safe_gate() converted it to A-GATEERROR, and the
                # WHOLE A-IMAGES gate died: TWELVE gate lines vanished and the
                # roster fell from 47 to 36, breaking the §R15 invariance v2.12
                # had just restored. One bad figure must never cost eleven other
                # gates their verdict. Skipped figures are counted and REPORTED,
                # never silently dropped.
                try:
                    _hard, _warns = fc.audit_figure(_spec, _png,
                                                    descr=_img.get('descr'))
                    _t = fc.triage(_hard + _warns, _spec)
                    _leg = bool(fc.is_legacy(_spec))
                except Exception:
                    _unusable += 1
                    continue
                _seen += 1
                if _leg:
                    _legacy_n += 1
                # v2.13: carry (finding, legacy?) so a gate can distinguish
                # "this v5.33+ render regressed" from "this pre-v5.33 render has
                # no sidecar to check against" — see _fig_verdict.
                _amber += [(_f, _leg) for _f in _t['AMBER']]
                _void += [(_f, _leg) for _f in _t['VOID_ITEM']]
                _block += [(_f, _leg) for _f in _t['BLOCKING']]

        # Emit one verdict per gate id, mapped engine G-*/W-* -> catalogue A-*.
        _by_gate = {}
        for _sev, _findings in (('BLOCKING', _block), ('VOID_ITEM', _void),
                                ('AMBER', _amber)):
            for _f, _leg in _findings:
                _e = _by_gate.setdefault(fc.audit_gate_id(_f), (_sev, [], []))
                _e[1].append(_f)
                _e[2].append(_leg)

        # Each gate is emitted by an EXPLICIT call with a LITERAL id. Check
        # M-GATE discovers emitted gates statically, so a loop over a variable
        # gate id is invisible to it and the catalogue would read as unemitted.
        # v2.13: coverage suffix — an incomplete sweep is stated on EVERY gate's
        # own line, so no verdict can be read as fuller coverage than it had.
        _cov = (f' [coverage: {_seen}/{_declared} evaluated; {_unusable} skipped — '
                f'unusable FigureSpec]') if _unusable else ''

        def _fig_verdict(gid, bucket):
            if gid not in bucket:
                # ── v2.13 (D3): 0 EVALUATED IS NOT EVIDENCE OF CONFORMANCE ──
                # This gate family printed "0 figure(s) conform." on EVERY paper
                # in EVERY exam from v2.11 to v2.12.1, because Block.images was
                # never populated. Zero-of-zero is the same false-clean the v2.12
                # A-FIGPROFILE edge case 6 already rejects; the rule is applied
                # here too, and for the same reason.
                if not _declared:
                    _ok(gid, 'no inline drawings in the paper; dormant.')
                elif not _seen:
                    _warn(gid, f'{_declared} inline drawing(s) present but 0 could be '
                               f'evaluated — conformance NOT ESTABLISHED (coverage gap, '
                               f'not a pass). Check A-ZIP and the registry '
                               f'figure_specs, then re-run.')
                elif _unusable:
                    _warn(gid, f'{_seen} figure(s) conform, but coverage is INCOMPLETE'
                               + _cov + ' — not a full pass; re-render those figures '
                               f'(Step 7 v5.34+) for full coverage.')
                else:
                    _ok(gid, f'{_seen} figure(s) conform'
                             + (f' ({_legacy_n} legacy, EC-V18).' if _legacy_n else '.'))
                return
            _sev, _msgs, _legs = bucket[gid]
            _detail = ' | '.join(_msgs[:3])
            # v2.13: a MIXED paper (some figures carry a sidecar, some do not)
            # must not report one number for two different populations — the
            # operator acts on this line, and "56 figure(s)" when one regressed
            # and 55 are merely old sends them to the wrong repair.
            _nl = sum(1 for _x in _legs if not _x)
            _lg = len(_legs) - _nl
            _mix = (f' (+{_lg} pre-v5.33 figure(s) reported under EC-V18, not '
                    f'blocking)') if _lg else ''
            # ── v2.13 (D3): EC-V18 IS A DELIVERY TOLERANCE, NOT ONLY A SEVERITY
            # RELABEL. The spec's EC-V18 clause is explicit and non-negotiable:
            # output with no FigureSpec sidecar predates Step 7 v5.33, so roughly
            # 200 existing exams "keep auditing AND DELIVERING untouched while the
            # defect is reported loudly on every one." A _fail() here exits
            # non-zero, and MANDATE D requires exit 0 to certify — so emitting
            # FAIL for a legacy-only finding would have converted this coverage
            # fix into an estate-wide delivery outage the moment the gates stopped
            # being vacuous. A legacy figure cannot be repaired at Step 8 (Step 8
            # cannot retro-fit a sidecar onto an already-rendered paper), which is
            # precisely the "genuinely-not-fixable diagnostic" S5-4 admits as an
            # ACCEPTED WARN. It stays LOUD, it forces the amber footer, it is
            # recorded as a §R13 limitation — it simply does not block a paper
            # whose only sin is being older than the contract.
            if all(_legs):
                _warn(gid, f'DEGRADED, NOT VOID — {len(_msgs)} pre-v5.33 figure(s) carry '
                           f'no FigureSpec sidecar (EC-V18 legacy): reported, amber '
                           f'footer applies, delivery NOT blocked; record as a §R13 '
                           f'limitation. Re-run Step 7 v5.34+ for full coverage.'
                           + _cov + f' {_detail}')
                return
            if _sev == 'BLOCKING':
                _fail(gid, f'RENDERER-CONTRACT REGRESSION on v5.33+ output — '
                           f'{_nl} figure(s) carrying a FigureSpec' + _mix
                           + ':' + _cov + f' {_detail}')
            elif _sev == 'VOID_ITEM':
                _fail(gid, f'ANSWER-CUE LEAK — {len(_msgs)} item(s) VOID; drop or '
                           f'regenerate those questions, the paper continues:'
                           + _cov + f' {_detail}')
            else:
                # AMBER: FAIL severity forces the amber delivery footer
                # (Framework_DeliveryFooter §5) and NEVER halts the run.
                _fail(gid, f'DEGRADED, NOT VOID — delivery continues under an '
                           f'amber footer; {_nl} figure(s) carrying a FigureSpec'
                           + _mix + ':' + _cov + f' {_detail}')

        _fig_verdict('A-FIGSCALE', _by_gate)
        _fig_verdict('A-FIGLABEL', _by_gate)
        _fig_verdict('A-FIGDPI', _by_gate)
        _fig_verdict('A-FIGDEGEN', _by_gate)
        _fig_verdict('A-FIGMONO', _by_gate)
        _fig_verdict('A-FIGOPTUNIF', _by_gate)
        _fig_verdict('A-FIGCOLOUR', _by_gate)
        _fig_verdict('A-FIGCVD', _by_gate)
        _fig_verdict('A-FIGSERIES', _by_gate)
        _fig_verdict('A-FIGGLYPH', _by_gate)
        _fig_verdict('A-FIGALT', _by_gate)
        _fig_verdict('A-FIGLABELPX', _by_gate)

        # v2.13: the EC-V18 legacy count was previously emitted as a SECOND
        # A-FIGDPI line, which breaks the v2.12 roster rule ("EVERY gate prints
        # EXACTLY ONE line on EVERY run") and would have made the gate count
        # stop being a usable integrity signal the moment _seen became non-zero.
        # It was unreachable while Block.images was empty; now that figures are
        # actually evaluated it is folded into each gate's own single verdict.


def gate_optref(blocks, src):
    """A-OPTREF (machine half): if a stem references a terminal/escape option,
    that option must be present in the option set."""
    rt = src['rules_txt']
    # Read escape tokens from section_rules (RA-9) as PRIMARY; English defaults as FALLBACK.
    extra = re.findall(r'(?:none_of_above_permitted|escape_option_tokens)\s*[:=]\s*(.+)', rt, re.I)
    if extra:
        # section_rules declared exam-specific escape tokens — merge with defaults.
        tokens = [t.strip() for e in extra for t in e.split(',')]  + list(ESCAPE_TOKENS_DEFAULT)
    else:
        tokens = list(ESCAPE_TOKENS_DEFAULT)
    # Escape-reference phrases: if the WHOLE phrase appears in the stem, the stem is
    # referencing the escape option that phrase implies. Read from section_rules (RA-9);
    # English defaults as fallback.
    ref_phrases = src.get('escape_reference_phrases',
                          [r'if there is no error'])
    miss = []
    for b in blocks:
        stem = block_stem_text(b)
        opts = [o[2].lower() for o in option_paras(b)]
        for tok in tokens:
            # MODE 1: a select/mark/choose verb near the escape token in the stem.
            triggered = bool(re.search(r'(select|mark|choose).{0,40}' + tok, stem, re.I))
            # MODE 2: a direct escape-reference phrase in the stem that implies this token.
            if not triggered:
                for phrase in ref_phrases:
                    if re.search(phrase, stem, re.I) and re.search(tok, phrase, re.I):
                        triggered = True
                        break
            if triggered:
                present = any(re.search(tok, o, re.I) for o in opts)
                if not present:
                    miss.append(f'Q{b.qnum}')
                break
    (_ok if not miss else _fail)('A-OPTREF',
        'escape-option references are satisfied.' if not miss else
        'stem references an absent escape/terminal option: ' + ' '.join(sorted(set(miss))[:12]))


def gate_encoding_script(doc, src):
    full = '\n'.join(para_text(obj) for kind, obj in iter_block_items(doc) if kind == 'p')
    if '�' in full:
        _fail('A-ENCODING', 'U+FFFD replacement character present (encoding corruption).')
    else:
        _ok('A-ENCODING', 'no U+FFFD replacement characters.')
    if src['language'] == 'english':
        # Flag only RUNS (>=2) of foreign-SCRIPT letters (Devanagari, Cyrillic, CJK,
        # Arabic, ...). Accented Latin (café, résumé) and Greek math symbols
        # (alpha, beta, theta) are LEGITIMATE on an english exam and must not be
        # flagged. Isolated symbols never trip the gate; only a multi-letter
        # foreign-script word does (the copy-paste-corruption signature).
        def _foreign_letter(ch):
            if ord(ch) <= 0x7F or not ch.isalpha():
                return False
            try:
                nm = unicodedata.name(ch, '')
            except ValueError:
                nm = ''
            return not (nm.startswith('LATIN') or nm.startswith('GREEK'))
        run = 0; hits = []
        for ch in full:
            if _foreign_letter(ch):
                run += 1
                if run == 2:
                    hits.append(ch)
            else:
                run = 0
        if hits:
            _fail('A-SCRIPT', f'foreign-script word(s) on an english exam '
                              f'(copy-paste corruption?): {len(hits)} run(s).')
        else:
            _ok('A-SCRIPT', 'no foreign-script text (accented Latin / Greek symbols OK).')
    else:
        _ok('A-SCRIPT', f"language={src['language']}: non-Latin script permitted.")


def gate_dup(blocks, src):
    reg = src['registry']; tq = src['total_questions']
    stems_all = reg.get('stem_texts', [])
    if not stems_all or tq is None:
        _warn('A-DUP', 'registry stem_texts empty or total_questions unknown; '
                       'cross-mock dedup skipped.')
        return
    prior = stems_all[:max(0, len(stems_all) - tq)]   # self-exclude trailing mock N
    if not prior:
        _ok('A-DUP', 'no prior-mock stems in registry (first mock or registry holds only mock N); cross-mock dedup vacuous.')
        return
    norm = lambda s: re.sub(r'\s+', ' ', s).strip().lower()
    prior_norm = set(norm(s) for s in prior)
    prior_tokens = [set(norm(s).split()) for s in prior]
    exact, near = [], []
    for b in blocks:
        stem = norm(block_stem_text(b))
        if not stem:
            continue
        if stem in prior_norm:
            exact.append(f'Q{b.qnum}')
            continue
        toks = set(stem.split())
        if toks:
            for pt in prior_tokens:
                if pt:
                    j = len(toks & pt) / len(toks | pt)
                    if j >= 0.75:
                        near.append(f'Q{b.qnum}')
                        break
    (_ok if not exact and not near else _fail)('A-DUP',
        'no cross-mock stem duplication.' if not exact and not near else
        f'exact={sorted(set(exact))[:8]} near={sorted(set(near))[:8]} (vs prior mocks).')


def gate_header(doc, blocks, src):
    # v2.7: A-HEADER INVERTED. The paper is questions-only (Step 7 R8b / G-PREQ1): NO
    # title/info/scoring/cover paragraph may sit before Q.1. Any non-blank paragraph before
    # Q.1 is a DEFECT → strip it in Phase 1 (CP-HEADER-STRIP). CATEGORY-C values
    # (marks/time/negative/options/total) are metadata, never printed — nothing to
    # figure-check. DORMANT only if section_rules EXAM_STRUCTURE declares paper_header_block.
    title_items, _ = parse_blocks(doc)
    title = ' '.join(para_text(obj) for kind, obj in title_items if kind == 'p').strip()
    if src.get('paper_header_block'):
        _ok('A-HEADER', 'pre-Q.1 header permitted (EXAM_STRUCTURE paper_header_block); dormant.')
    elif not title:
        _ok('A-HEADER', 'questions-only: no non-blank paragraph before Q.1.')
    else:
        _fail('A-HEADER', f'non-Q paragraph(s) before Q.1: "{title[:60]}". Strip the '
                          'pre-Q.1 title/info/scoring/cover block (CP-HEADER-STRIP) — the '
                          'paper is questions-only (R8b/G-PREQ1); marks/time/negative/'
                          'options/total are metadata, never printed.')


def gate_zip(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        names = set(z.namelist())
        if 'word/document.xml' not in names:
            _fail('A-ZIP', 'word/document.xml missing.')
            return {}
        doc_xml = z.read('word/document.xml').decode('utf-8', 'replace')
        rels = (z.read('word/_rels/document.xml.rels').decode('utf-8')
                if 'word/_rels/document.xml.rels' in names else '')
        # parse each <Relationship .../> element, then pull Id + Target from
        # within it (attribute ORDER-INDEPENDENT — some generators emit Target
        # before Id, which an "Id...Target" regex would miss).
        rel_map = {}
        for tag in re.findall(r'<Relationship\b[^>]*/?>', rels):
            idm = re.search(r'\bId="([^"]+)"', tag)
            tgm = re.search(r'\bTarget="([^"]+)"', tag)
            if idm and tgm:
                rel_map[idm.group(1)] = tgm.group(1)
        ref_ids = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', doc_xml))
        bad = []
        media_map = {}
        for rid in ref_ids:
            tgt = rel_map.get(rid)
            if tgt is None:
                bad.append(rid); continue
            if tgt.startswith('http'):
                continue
            part = ('word/' + tgt).replace('word/../', '')
            if part not in names and ('word/' + tgt) not in names:
                bad.append(rid)
            media_map[rid] = tgt.split('/')[-1]
        (_ok if not bad else _fail)('A-ZIP',
            'all rIds resolve to parts.' if not bad else f'unresolved rIds: {bad[:8]}')
        return media_map


# ============================================================================
# S5-1A — COMPLETION GATE (v2.6) — Phase-3 mechanical Part-B/§7 enforcement
# ============================================================================
def _resolve_evidence(evidence_dir, stored):
    """Resolve a ledger-stored evidence path to an existing absolute path. Accepts an
    absolute path, a path relative to evidence_dir, a bare basename under evidence_dir,
    or a path with a leading 'evidence/' segment. Returns the resolved path or None."""
    if not stored:
        return None
    cands = [stored]
    if not os.path.isabs(stored):
        cands.append(os.path.join(evidence_dir, stored))
        cands.append(os.path.join(evidence_dir, os.path.basename(stored)))
        parts = stored.replace('\\', '/').split('/')
        if parts and parts[0] == 'evidence':
            cands.append(os.path.join(evidence_dir, *parts[1:]))
    for c in cands:
        if c and os.path.exists(c):
            return c
    # v2.15 (C1) — last resort: the stored path may be an ABSOLUTE path from a
    # previous session's container (checkpoint restore rebases these, but a
    # hand-edited or partially-rebased state must still resolve rather than
    # silently fail C5/C6). Search the evidence tree by basename.
    base = os.path.basename(stored.replace('\\', '/'))
    if base and evidence_dir and os.path.isdir(evidence_dir):
        for root, _dirs, files in os.walk(evidence_dir):
            if base in files:
                return os.path.join(root, base)
    return None


def _file_ok(path, min_bytes):
    return bool(path) and os.path.exists(path) and os.path.getsize(path) >= min_bytes


# v2.14 (B3 — FACT CONTEXT DISCIPLINE). RA-11 has always required the saved fact
# to carry query + URL + retrieval-time + snippet. C5 only ever checked that the
# file EXISTED and was >= 1 byte, so a one-character stub certified. That gap did
# not matter while the full search result also sat in the reasoning stream — the
# evidence was duplicated. It matters now: B3 moves the raw result OUT of context
# and onto disk, which makes the saved file the ONLY copy. If the gate does not
# verify its shape, the discipline degrades from "save it" to "touch a file", and
# C5 would certify an audit whose evidence no longer exists in any form.
FACT_REQUIRED_FIELDS = ('query', 'url', 'retrieved_at', 'snippet')


def _fact_record_ok(path):
    """Validate one saved fact-evidence file. Accepts a single record object or a
    LIST of them (one file may hold the key fact plus its options, and one file may
    be SHARED by several questions that turn on the same concept — the B3 cache).
    Returns (ok, reason). The reason names FIELDS only, never fact content
    (MANDATE 0)."""
    if not path or not os.path.exists(path):
        return False, 'missing'
    try:
        with open(path, encoding='utf-8') as fh:
            obj = json.load(fh)
    except Exception as e:
        return False, f'unparseable ({type(e).__name__})'
    recs = obj if isinstance(obj, list) else [obj]
    if not recs:
        return False, 'no records'
    for r in recs:
        if not isinstance(r, dict):
            return False, 'record is not an object'
        miss = [k for k in FACT_REQUIRED_FIELDS if not str(r.get(k) or '').strip()]
        if miss:
            return False, 'missing/blank ' + ','.join(miss)
    return True, ''


def _block_has_omml(b):
    for p in b.paras:
        for _ in p._element.iter(M_('oMath')):
            return True
    return False


def _block_has_image(b):
    return any(para_images(p) for p in b.paras)


def completion_gate(audit_state_path, total_questions, blocks, doc):
    """S5-1A — validate the Phase-2 audit_state ledger (C1-C7) AND the on-disk evidence
    artefacts each stamp names. Appends C0..C7 results to RESULTS so the exit code
    reflects them, and prints the COMPLETION-GATE summary line. MANDATE-0 safe:
    Q-numbers + codes only, never content/URLs. Returns 0 (PASS) or 1 (FAIL)."""
    try:
        state = json.load(open(audit_state_path, encoding='utf-8'))
    except Exception as e:
        _fail('C0', f'audit_state unreadable/absent ({e}).')
        print('COMPLETION-GATE: FAIL (audit_state unreadable)')
        return 1
    ledger = (state.get('ledger') or {}).get('entries', {}) or {}
    entries = {int(k): v for k, v in ledger.items()}
    evidence_dir = state.get('evidence_dir', '') or ''
    K = state.get('K')
    if not K:
        plan = state.get('plan') or []
        K = len(plan) if plan else (max(state.get('batches_done', []) or [0]) or 0)
    batches_done = set(state.get('batches_done', []) or [])

    # C1 — every planned batch closed
    if K and set(range(1, K + 1)) <= batches_done:
        _ok('C1', f'all {K} batches closed.')
    else:
        _fail('C1', f'batches_done={sorted(batches_done)} does not cover 1..{K} '
                    f'(Phase 2 skipped/partial — MANDATE B).')
    # C2 — every question reviewed
    want = set(range(1, (total_questions or 0) + 1))
    got = set(entries.keys())
    if total_questions and got == want:
        _ok('C2', f'all {total_questions} questions have a ledger entry.')
    else:
        miss = sorted(want - got)[:15]; extra = sorted(got - want)[:15]
        _fail('C2', f'ledger != 1..{total_questions}: missing={miss} extra={extra}.')
    # C3 — every entry closed
    bad3 = [q for q, e in entries.items() if e.get('status') not in ('verified', 'regenerated')]
    (_ok if not bad3 else _fail)('C3',
        'all entries verified/regenerated.' if not bad3 else
        f'entries not closed (pending/absent): {sorted(bad3)[:15]}')
    # C4 — uniqueness / set ran
    bad4 = []
    for q, e in entries.items():
        if e.get('answer_cardinality') == 'multi':
            if not e.get('answer_set_verified'):
                bad4.append(q)
        else:
            if not e.get('answer_unique'):
                bad4.append(q)
    (_ok if not bad4 else _fail)('C4',
        'B-UNIQUE/A-MSQ-KEY ran for every Q.' if not bad4 else
        f'uniqueness/set not verified: {sorted(bad4)[:15]}')
    # C5 — factual entries sourced AND the saved evidence file exists, parses, and
    # carries the RA-11 record fields (v2.14/B3: shape, not just existence).
    bad5 = []
    _fact_files, _fact_refs = set(), 0
    for q, e in entries.items():
        if e.get('is_factual'):
            fs = e.get('fact_sources') or []
            if not fs:
                bad5.append((q, 'no fact_sources')); continue
            for rec in fs:
                saved = rec.get('saved') if isinstance(rec, dict) else None
                _fact_refs += 1
                _p = _resolve_evidence(evidence_dir, saved)
                ok, why = _fact_record_ok(_p)
                if not ok:
                    bad5.append((q, why)); break
                _fact_files.add(os.path.realpath(_p))
    _dedup = (f' ({len(_fact_files)} distinct source file(s) for {_fact_refs} '
              f'reference(s) — B3 cache reuse)') if _fact_refs else ''
    (_ok if not bad5 else _fail)('C5',
        f'every factual entry has a saved, well-formed sourced fact.{_dedup}'
        if not bad5 else
        'factual entries unsourced / saved fact file missing or malformed: '
        + '; '.join(f'Q{q}:{why}' for q, why in sorted(set(bad5))[:15]))
    # C6 — artefact stamps present AND their evidence files exist/non-trivial
    bad6 = []
    for q, e in entries.items():
        st = e.get('artefact_stamps') or {}
        ok = True
        for img in (st.get('images') or []):
            if not _file_ok(_resolve_evidence(evidence_dir, img.get('montage')), EVIDENCE_MIN_BYTES):
                ok = False
        for kind in ('tables', 'charts', 'omml'):
            for rec in (st.get(kind) or []):
                path = rec.get('trace') or rec.get('montage')
                if not _file_ok(_resolve_evidence(evidence_dir, path), 1):
                    ok = False
        if not ok:
            bad6.append(q)
    (_ok if not bad6 else _fail)('C6',
        'every artefact stamp is backed by an existing evidence file.' if not bad6 else
        f'artefact stamp evidence missing/trivial: {sorted(set(bad6))[:15]}')
    # C7 — coverage: every artefact PRESENT IN THE PAPER is represented in the ledger
    bad7 = []
    for b in blocks:
        e = entries.get(b.qnum, {})
        st = e.get('artefact_stamps') or {}
        if _block_has_image(b) and not st.get('images'):
            bad7.append(f'Q{b.qnum}:img'); continue
        if b.tables and not (st.get('tables') or st.get('charts')):
            bad7.append(f'Q{b.qnum}:tbl'); continue
        if _block_has_omml(b) and not st.get('omml'):
            bad7.append(f'Q{b.qnum}:omml'); continue
    (_ok if not bad7 else _fail)('C7',
        'every paper artefact is covered by a ledger stamp.' if not bad7 else
        f'paper artefact not audited (no ledger stamp): {sorted(set(bad7))[:15]}')

    cfails = [c for lvl, c, _ in RESULTS if lvl == 'FAIL' and (c == 'C0' or c.startswith('C'))
              and c[1:].isdigit()]
    if not cfails:
        F = sum(1 for e in entries.values() if e.get('is_factual'))
        V = sum(len((e.get('artefact_stamps') or {}).get(k, []))
                for e in entries.values() for k in ('images', 'tables', 'charts', 'omml'))
        print(f'COMPLETION-GATE: PASS (Q reviewed={len(entries)}/{total_questions}, '
              f'facts sourced={F}, artefacts stamped={V}, evidence files present={V + F})')
        return 0
    print(f'COMPLETION-GATE: FAIL ({len(cfails)} assertion(s): {sorted(set(cfails))})')
    return 1


# ============================================================================
# RUNNER
# ============================================================================
def _safe_gate(_name, _fn, *a, **kw):
    """v2.12 — GATE FAULT ISOLATION (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING, P6).

    THE STRUCTURAL LESSON OF THIS GAP. The `bc` NameError was one defect, but the
    reason it produced a PERMANENT HALT WITH ZERO OUTPUT is that run_audit called
    21 gates in bare sequence with no isolation, and print_results() runs only
    after the last one. A single raise anywhere therefore destroyed the entire
    report — including the 30+ gates that had already passed and the completion
    gate that certifies Phase 3.

    Binding `bc` fixes THIS defect. Isolation fixes the DEFECT CLASS: from v2.12
    no gate, present or future, can abort the run. An unexpected raise becomes a
    LOUD, NAMED, non-recoverable FAIL line and the remaining gates still execute.

    SEVERITY IS _fail, NOT _warn — deliberately, and this is the one place where
    the "never halt" directive must not be read as "never block". A gate that
    crashed DID NOT AUDIT THE PAPER. Reporting it as a warning would let an
    unaudited paper reach certification, which is the false-clean outcome the
    whole v2.6 hardening exists to prevent. FAIL yields exit 1, so the paper
    cannot be certified — while the run still COMPLETES and prints everything.
    That is exactly CLAUDE.md's rule: "A CLASS T failure must be LOUD, and must
    NOT halt... Silence is the defect; a halt is not the remedy."
    """
    try:
        return _fn(*a, **kw)
    except Exception as _e:
        import traceback as _tb
        _fail('A-GATEERROR',
              f'gate {_name} raised {type(_e).__name__}: {_e} — this gate DID NOT '
              f'RUN and the paper is NOT audited for it. Framework defect: capture '
              f'this line and file a gap report (§17). Remaining gates still ran.')
        # The traceback goes to STDERR (never STDOUT — the report must stay
        # machine-parseable) so a maintainer can diagnose the framework defect.
        # Suppressed under --self-test, where fixture 50 raises on purpose.
        if not any(a == '--self-test' for a in sys.argv):
            try:
                print(f'--- A-GATEERROR traceback ({_name}) ---', file=sys.stderr)
                _tb.print_exc()
            except Exception:
                pass
        return None


# ============================================================================
# C1 — CROSS-SESSION CHECKPOINT (v2.15)
#
# WHY THIS EXISTS. RA-18 called Step 8 "resume-safe" and stored every piece of
# cross-batch state — the ledger, the batch plan, the WIP docx and the ENTIRE
# evidence tree — under /home/claude. That directory does not survive a session
# boundary. So resume worked inside one session and not at all across one, and
# the failure was silent-then-fatal: a session that exhausted mid-Phase-2 lost
# the audit outright, because S5-1A C5/C6 assert that every stamped evidence file
# EXISTS. A perfectly remembered ledger cannot certify against montages and saved
# fact records that no longer exist. The retry then exhausted the same way. That
# loop — not any single gate — is what made this step keep failing.
#
# The checkpoint is a PORTABLE, HASH-MANIFESTED bundle the author downloads and
# re-uploads, so an audit may legitimately span sessions and still certify.
#
# BINDING IS THE WHOLE SAFETY ARGUMENT. A checkpoint restored onto the WRONG
# paper would certify an audit of a document nobody audited — strictly worse than
# losing the audit. Restore therefore refuses unless the bundle's recorded
# exam_code, mock number AND paper MD5 all match the paper in hand, and unless
# every member's sha256 matches the manifest. Prose describes; only code
# certifies (§21).
# ============================================================================
CHECKPOINT_SCHEMA = 1
CHECKPOINT_MANIFEST = 'checkpoint_manifest.json'


class CheckpointError(Exception):
    """Refusal to build or restore. Always names WHY, never fact/question content."""


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def _md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def _now_utc():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def make_checkpoint(state_path, out_zip, docx_path=None, exam=None, mockN=None):
    """Bundle audit_state.json + the evidence tree + the WIP docx into out_zip.

    The bundle is self-describing: checkpoint_manifest.json records the schema,
    the identity triple (exam_code, mock, paper_md5), progress counters, and a
    sha256 for EVERY member. Returns the manifest dict.
    """
    if not os.path.exists(state_path):
        raise CheckpointError(f'audit_state not found: {state_path}')
    try:
        with open(state_path, encoding='utf-8') as fh:
            st = json.load(fh)
    except Exception as e:
        raise CheckpointError(f'audit_state unparseable ({type(e).__name__})')

    # v2.15 — THE PAPER IS MANDATORY, NOT OPTIONAL. paper_md5 is the strongest of
    # the three identity bindings, and a bundle built without the docx would carry
    # paper_md5=None, which makes restore's MD5 check vacuous — a checkpoint that
    # could then be restored onto ANY document. Caught in end-to-end testing when a
    # shell quoting slip left the docx absent and the checkpoint was written anyway,
    # cheerfully, with no binding at all. Refuse instead: a checkpoint whose safety
    # argument is missing is worse than no checkpoint, because it looks like one.
    if not docx_path or not os.path.exists(docx_path):
        raise CheckpointError(
            'the paper (.docx) is REQUIRED to build a checkpoint — it supplies the '
            'paper_md5 binding that stops the bundle being restored onto a different '
            'document. Pass the Create.docx being audited.')
    members = [('audit_state.json', state_path),
               ('paper/' + os.path.basename(docx_path), docx_path)]
    evd = st.get('evidence_dir')
    if evd and os.path.isdir(evd):
        for root, _dirs, files in os.walk(evd):
            for f in sorted(files):
                ap = os.path.join(root, f)
                arc = 'evidence/' + os.path.relpath(ap, evd).replace(os.sep, '/')
                members.append((arc, ap))

    man = {
        'schema': CHECKPOINT_SCHEMA,
        'created_utc': _now_utc(),
        'exam_code': exam or st.get('exam_code'),
        'mock': st.get('mock', mockN),
        'paper_id': st.get('paper_id'),
        'paper_md5': _md5_file(docx_path),
        'paper_name': os.path.basename(docx_path),
        'K': st.get('K'),
        'batches_done': sorted(st.get('batches_done') or []),
        'ledger_entries': len(((st.get('ledger') or {}).get('entries')) or {}),
        'evidence_files': sum(1 for a, _ in members if a.startswith('evidence/')),
        'files': {arc: _sha256_file(ap) for arc, ap in members},
    }
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc, ap in members:
            z.write(ap, arc)
        z.writestr(CHECKPOINT_MANIFEST,
                   json.dumps(man, indent=1, ensure_ascii=False))
    return man


_EVIDENCE_PATH_KEYS = ('saved', 'montage', 'trace')


def _rebase_evidence_paths(obj, old_evd, new_evd):
    """Rewrite every recorded evidence path in a restored audit_state so it points
    into the NEW evidence directory. Returns how many were rewritten.

    The ledger stores absolute paths from the session that wrote them
    (evidence/facts/q1_x.json, evidence/montages/q7_montage.png, ...). After a
    session boundary those directories do not exist, and S5-1A C5/C6 assert that
    each named file EXISTS — so without this every restored audit would fail
    certification while the files sat right there, correctly restored. Rebasing is
    done EXPLICITLY here rather than left to the resolver's fallback so the state
    on disk is truthful and a human reading it sees real paths.
    """
    n = 0
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in _EVIDENCE_PATH_KEYS and isinstance(v, str) and v.strip():
                rel = None
                norm = v.replace('\\', '/')
                if old_evd:
                    oe = old_evd.replace('\\', '/').rstrip('/')
                    if norm == oe or norm.startswith(oe + '/'):
                        rel = norm[len(oe):].lstrip('/')
                if rel is None:
                    parts = norm.split('/')
                    if 'evidence' in parts:
                        rel = '/'.join(parts[parts.index('evidence') + 1:])
                if rel:
                    obj[k] = os.path.join(new_evd, *rel.split('/'))
                    n += 1
            else:
                n += _rebase_evidence_paths(v, old_evd, new_evd)
    elif isinstance(obj, list):
        for v in obj:
            n += _rebase_evidence_paths(v, old_evd, new_evd)
    return n


def restore_checkpoint(zip_path, into_dir, docx_path=None, exam=None, mockN=None):
    """Verify and unpack a checkpoint. Returns (manifest, state_path, evidence_dir).

    HARD refusals — every one of these would otherwise let Step 8 certify an audit
    that was never performed on the paper in hand:
      * absent/unparseable manifest, or a schema this build does not know;
      * ANY member whose sha256 differs from the manifest (tamper/truncation);
      * exam_code, mock or paper MD5 disagreeing with the paper being audited.
    On success the restored audit_state.evidence_dir is REWRITTEN to the new
    location — the recorded path is from the previous session's container and no
    longer exists, and S5-1A resolves every stamp through it.
    """
    if not os.path.exists(zip_path):
        raise CheckpointError(f'checkpoint not found: {zip_path}')
    try:
        z = zipfile.ZipFile(zip_path)
    except Exception as e:
        raise CheckpointError(f'checkpoint is not a readable archive ({type(e).__name__})')
    with z:
        names = set(z.namelist())
        if CHECKPOINT_MANIFEST not in names:
            raise CheckpointError('checkpoint_manifest.json missing — not a Step-8 checkpoint.')
        try:
            man = json.loads(z.read(CHECKPOINT_MANIFEST).decode('utf-8'))
        except Exception as e:
            raise CheckpointError(f'checkpoint manifest unparseable ({type(e).__name__})')
        if man.get('schema') != CHECKPOINT_SCHEMA:
            raise CheckpointError(
                f'checkpoint schema {man.get("schema")!r} != {CHECKPOINT_SCHEMA} — '
                f'built by a different framework version; re-run the audit.')
        # identity binding, BEFORE anything is written to disk
        if exam and man.get('exam_code') and man['exam_code'] != exam:
            raise CheckpointError(
                f'checkpoint is for exam_code {man["exam_code"]!r}, not {exam!r}.')
        if mockN is not None and man.get('mock') is not None and int(man['mock']) != int(mockN):
            raise CheckpointError(
                f'checkpoint is for mock {man["mock"]}, not mock {mockN}.')
        if not man.get('paper_md5'):
            raise CheckpointError(
                'checkpoint carries no paper_md5 binding — it cannot be proven to '
                'belong to this paper. Re-run the audit rather than resuming from an '
                'unbindable bundle.')
        if docx_path:
            live = _md5_file(docx_path)
            if live != man['paper_md5']:
                raise CheckpointError(
                    'checkpoint paper MD5 does not match the docx being audited — the '
                    'paper changed, or this checkpoint belongs to another paper. '
                    'Re-run the audit from Phase 1 rather than resuming onto a '
                    'different document.')
        # integrity: every declared member present and hash-exact
        bad = []
        for arc, want in (man.get('files') or {}).items():
            if arc not in names:
                bad.append(f'{arc}:absent'); continue
            got = hashlib.sha256(z.read(arc)).hexdigest()
            if got != want:
                bad.append(f'{arc}:hash')
        if bad:
            raise CheckpointError('checkpoint integrity failure (' + str(len(bad))
                                  + ' member(s)): ' + ', '.join(sorted(bad)[:8]))
        os.makedirs(into_dir, exist_ok=True)
        for arc in (man.get('files') or {}):
            dst = os.path.join(into_dir, *arc.split('/'))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'wb') as fh:
                fh.write(z.read(arc))

    state_path = os.path.join(into_dir, 'audit_state.json')
    evidence_dir = os.path.join(into_dir, 'evidence')
    with open(state_path, encoding='utf-8') as fh:
        st = json.load(fh)
    _old_evd = st.get('evidence_dir')
    _rebased = _rebase_evidence_paths(st.get('ledger'), _old_evd, evidence_dir)
    st['evidence_dir'] = evidence_dir          # last session's path is gone
    st.setdefault('session_log', {})
    if isinstance(st['session_log'], dict):
        st['session_log'].setdefault('checkpoints_restored', []).append(
            {'from': os.path.basename(zip_path), 'at': _now_utc(),
             'batches_done': man.get('batches_done'),
             'evidence_paths_rebased': _rebased})
    with open(state_path, 'w', encoding='utf-8') as fh:
        json.dump(st, fh, indent=1, ensure_ascii=False)
    return man, state_path, evidence_dir


def run_audit(args):
    _reset()
    src = load_sources(args)
    src['_mockN'] = args.mockN
    media_map = _safe_gate('gate_zip', gate_zip, args.docx) or {}
    # The docx itself is the audit SURFACE, not a gate: if it cannot be opened
    # there is genuinely nothing to audit. Still report it as a gate line and a
    # complete roster rather than a raw traceback (v2.12).
    try:
        doc = Document(args.docx)
        _title, blocks = parse_blocks(doc)
    except Exception as _e:
        _fail('A-DOCXOPEN',
              f'cannot open/parse the paper ({type(_e).__name__}: {_e}) — the audit '
              f'surface is unreadable. Re-upload an intact docx (P0.5).')
        return print_results()
    # v2.13 (D1) — bind every inline drawing to its extracted PNG BEFORE the
    # gates run. Guarded and non-fatal by construction: extract_media() never
    # raises, and a resolution shortfall becomes a coverage WARN inside
    # _fig_verdict rather than a missing gate line or a silent pass.
    _safe_gate('A-MEDIA', attach_block_images, blocks, media_map,
               extract_media(args.docx, media_map))
    _safe_gate('A-STRUCTURE', gate_structure, blocks, src)
    _safe_gate('A-SECCOUNT', gate_seccount, blocks, src)
    _safe_gate('A-OPTIONS', gate_options, blocks, src)
    _safe_gate('A-QNFIRST', gate_qnfirst, blocks)
    _safe_gate('A-MSQ-INSTR', gate_msq_instr, blocks, src)   # v1.2 — MULTI only; dormant otherwise
    _safe_gate('A-NAT', gate_nat, blocks, src)               # v1.4 — NUMERICAL only; dormant otherwise
    _safe_gate('A-BLANKSEP', gate_blanksep, doc, blocks)
    _safe_gate('A-FONT', gate_font, doc, src)
    _safe_gate('A-SECHDR', gate_sechdr, blocks, doc, src)
    _safe_gate('A-ANSKEY', gate_anskey, doc)
    _safe_gate('A-STIMORPHAN', gate_stimorphan, blocks, src)
    _safe_gate('A-MATCHTABLE', gate_match_table, blocks, src)  # v2.7.1 — MATCH must render a real table
    _safe_gate('A-UNDERLINE', gate_underline, blocks)
    _safe_gate('A-OMML', gate_omml, doc, src, args.final)
    _safe_gate('A-FRACASCII', gate_frac_ascii, blocks, src)
    _safe_gate('A-IMAGES', gate_images, blocks, src, media_map)
    _safe_gate('A-OPTREF', gate_optref, blocks, src)
    _safe_gate('A-ENCODING', gate_encoding_script, doc, src)
    _safe_gate('A-DUP', gate_dup, blocks, src)
    _safe_gate('A-HEADER', gate_header, doc, blocks, src)
    rc = print_results()
    # v2.6 — S5-1A COMPLETION GATE: Phase-3 mechanical Part-B/§7 enforcement.
    if getattr(args, 'audit_state', None):
        cg = completion_gate(args.audit_state, src.get('total_questions'), blocks, doc)
        return 0 if (rc == 0 and cg == 0) else 1
    return rc


def print_results():
    n_fail = sum(1 for lvl, _, _ in RESULTS if lvl == 'FAIL')
    n_warn = sum(1 for lvl, _, _ in RESULTS if lvl == 'WARN')
    n_ok   = sum(1 for lvl, _, _ in RESULTS if lvl == 'OK')
    print('=' * 70)
    print(f'PART-A MACHINE AUDIT  |  OK={n_ok}  WARN={n_warn}  FAIL={n_fail}')
    print('=' * 70)
    for lvl, code, msg in RESULTS:
        mark = {'OK': '  ok ', 'WARN': ' WARN', 'FAIL': ' FAIL'}[lvl]
        print(f'[{mark}] {code:20s} {msg}')
    print('-' * 70)
    if n_fail == 0:
        print(f'RESULT: PASS (0 FAIL, {n_warn} WARN for reviewer adjudication)')
    else:
        print(f'RESULT: FAIL ({n_fail} gate(s) failed)')
    return 0 if n_fail == 0 else 1


# ============================================================================
# SELF-TEST  (builds tiny docx fixtures; asserts each gate catches + passes)
# ============================================================================
def _mini_doc(tmp, build):
    from docx import Document as D
    d = D()
    build(d)
    p = os.path.join(tmp, 'x.docx')
    d.save(p)
    return p

def _src_stub(tq=2, oc=4, lang='english', sections=None, omml=False):
    return {'total_questions': tq, 'sections': sections or
            [{'name': 'S1', 'q_range': [1, tq], 'total_qs': tq}],
            'options_count': oc, 'opt_label_fmt': '1/2/3/4', 'font_family': 'Calibri',
            'language': lang, 'omml_required_present': omml, 'rules_txt': '',
            'registry': {}, 'manifest': {}, 'blueprint': {},
            'passage_linked': set(), 'cloze_linked': set(), 'figural_qs': set(),
            '_mockN': 1}

def _add_q(d, n, opts=('Alpha', 'Beta', 'Gamma', 'Delta'), qn_first=True, stem='Solve.'):
    if qn_first:
        d.add_paragraph(f'Q.{n}  {stem}')
    else:
        d.add_paragraph(stem)               # stimulus-first (defect)
        d.add_paragraph(f'Q.{n}  {stem}')
    for i, o in enumerate(opts, 1):
        d.add_paragraph(f'{i}.  {o}')
    d.add_paragraph('')

def self_test():
    passed = 0; total = 0; fails = []
    tmp = tempfile.mkdtemp()
    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond: passed += 1
        else: fails.append(name)

    # 1. clean paper passes structure/options/qnfirst
    def b_clean(d):
        _add_q(d, 1); _add_q(d, 2)
    p = _mini_doc(tmp, b_clean)
    _reset(); doc = Document(p); _t, blocks = parse_blocks(doc)
    src = _src_stub()
    gate_structure(blocks, src); gate_options(blocks, src); gate_qnfirst(blocks)
    check('clean-no-fail', not any(l == 'FAIL' for l, _, _ in RESULTS))

    # 2. A-COUNT catches wrong count
    _reset(); gate_structure(blocks, _src_stub(tq=5))
    check('A-COUNT-catch', any(c == 'A-COUNT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 3. A-OPTN catches 3 options
    def b_3opt(d): _add_q(d, 1, opts=('A', 'B', 'C'))
    p = _mini_doc(tmp, b_3opt); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTN-catch', any(c == 'A-OPTN' and l == 'FAIL' for l, c, _ in RESULTS))

    # 4. A-OPTUNIQUE catches duplicate options
    def b_dupopt(d): _add_q(d, 1, opts=('Same', 'Same', 'B', 'C'))
    p = _mini_doc(tmp, b_dupopt); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTUNIQUE-catch', any(c == 'A-OPTUNIQUE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5. A-QNFIRST catches stimulus orphaned before the next Q.N
    def b_notfirst(d):
        _add_q(d, 1)                                   # Q.1 + options + blank
        d.add_paragraph(' '.join(['word'] * 60))       # passage orphaned before Q.2
        _add_q(d, 2)
    p = _mini_doc(tmp, b_notfirst); _reset()
    _t, bl = parse_blocks(Document(p)); gate_qnfirst(bl)
    check('A-QNFIRST-catch', any(c == 'A-QNFIRST' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5b. A-MATCH-TABLE catches a MATCH question rendered WITHOUT a real table (v2.7.1)
    _MPAIRS = ('(A)-(I), (B)-(III), (C)-(IV), (D)-(II)', '(A)-(II), (B)-(IV), (C)-(III), (D)-(I)',
               '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(III), (B)-(I), (C)-(IV), (D)-(II)')
    def b_match_notable(d):
        d.add_paragraph('Q.1  Match List-I with List-II.')
        for i, o in enumerate(_MPAIRS, 1):
            d.add_paragraph(f'{i}.  {o}')
        d.add_paragraph('')
    p = _mini_doc(tmp, b_match_notable); _reset()
    _t, bl = parse_blocks(Document(p)); gate_match_table(bl, _src_stub(tq=1))
    check('A-MATCH-TABLE-catch', any(c == 'A-MATCH-TABLE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5c. A-MATCH-TABLE passes (dormant) when the MATCH body IS a real table
    def b_match_table(d):
        d.add_paragraph('Q.1  Match List-I with List-II.')
        tb = d.add_table(rows=2, cols=2)
        tb.cell(0, 0).text = '(A) Collagen'; tb.cell(0, 1).text = '(I) triple helix'
        tb.cell(1, 0).text = '(B) Keratin';  tb.cell(1, 1).text = '(II) coiled coil'
        for i, o in enumerate(_MPAIRS, 1):
            d.add_paragraph(f'{i}.  {o}')
        d.add_paragraph('')
    p = _mini_doc(tmp, b_match_table); _reset()
    _t, bl = parse_blocks(Document(p)); gate_match_table(bl, _src_stub(tq=1))
    check('A-MATCH-TABLE-pass', not any(c == 'A-MATCH-TABLE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 6. A-FONT catches Arial run
    def b_arial(d):
        para = d.add_paragraph()
        run = para.add_run('Q.1  Stem'); run.font.name = 'Arial'
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_arial); _reset()
    gate_font(Document(p), _src_stub(tq=1))
    check('A-FONT-catch', any(c == 'A-FONT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 7. A-ANSKEY catches an answer-key line
    def b_key(d):
        _add_q(d, 1); d.add_paragraph('Answer Key: Q.1 -> 2')
    p = _mini_doc(tmp, b_key); _reset()
    gate_anskey(Document(p))
    check('A-ANSKEY-catch', any(c == 'A-ANSKEY' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8. A-SECHDR catches a body section header INSIDE a question block (KEYWORD form)
    def b_hdr2(d):
        d.add_paragraph('Q.1  Stem'); d.add_paragraph('SECTION A: Reasoning')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p2 = _mini_doc(tmp, b_hdr2); _reset()
    _t, bl2 = parse_blocks(Document(p2))
    gate_sechdr(bl2, Document(p2), {'sections': [{'name': 'Reasoning'}]})
    check('A-SECHDR-catch', any(c == 'A-SECHDR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8b. A-HEADER (inverted, v2.7): a title/info block BEFORE Q.1 → A-HEADER FAIL (strip).
    def b_hdr_preq1(d):
        d.add_paragraph('SSC CGL Tier 1 — Mock Test 1')
        d.add_paragraph('Total Questions: 100    |    Maximum Marks: 200    |    Time: 60 Minutes')
        _add_q(d, 1)
    p = _mini_doc(tmp, b_hdr_preq1); _reset()
    dh = Document(p); _t, blh = parse_blocks(dh)
    gate_header(dh, blh, _src_stub(tq=1))
    check('A-HEADER-catch', any(c == 'A-HEADER' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8c. A-HEADER dormant (v2.7): the SAME pre-Q.1 block, but section_rules EXAM_STRUCTURE
    #     declares paper_header_block → the opt-in permits it → NO A-HEADER failure.
    _reset()
    sd = _src_stub(tq=1); sd['paper_header_block'] = True
    gate_header(dh, blh, sd)
    check('A-HEADER-dormant', not any(c == 'A-HEADER' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8b. v1.5 — A-SECHDR catches a stray heading that IS a declared SECTION NAME (the case
    #     the keyword pattern missed — found by the mutation harness). "Quantitative Aptitude"
    #     as a body paragraph, matched against src['sections'], must FAIL.
    def b_hdr3(d):
        d.add_paragraph('Quantitative Aptitude')          # section-name header, no keyword
        d.add_paragraph('Q.1  Stem')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p3 = _mini_doc(tmp, b_hdr3); _reset()
    _t, bl3 = parse_blocks(Document(p3))
    gate_sechdr(bl3, Document(p3), {'sections': [{'name': 'Quantitative Aptitude'}]})
    check('A-SECHDR-name-catch', any(c == 'A-SECHDR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 9. A-UNDERLINE-FAKE catches "(underlined: X)"
    def b_fakeu(d):
        d.add_paragraph('Q.1  Find the synonym of the underlined word. (underlined: brisk)')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_fakeu); _reset()
    _t, bl = parse_blocks(Document(p)); gate_underline(bl)
    check('A-UNDERLINE-catch', any(c.startswith('A-UNDERLINE') and l == 'FAIL'
                                   for l, c, _ in RESULTS))

    # 10. A-FRAC catches ASCII caret exponent
    def b_caret(d):
        d.add_paragraph('Q.1  If x^2 + 1 = 5 then x?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_caret); _reset()
    _t, bl = parse_blocks(Document(p)); gate_frac_ascii(bl, _src_stub(tq=1, omml=True))
    check('A-FRAC-catch', any(c == 'A-FRAC' and l == 'FAIL' for l, c, _ in RESULTS))

    # 11. A-STIMORPHAN catches a passage-reference with no embedded stimulus
    def b_orphan(d):
        d.add_paragraph('Q.1  According to the passage, what is the tone?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_orphan); _reset()
    _t, bl = parse_blocks(Document(p)); gate_stimorphan(bl, _src_stub(tq=1))
    check('A-STIMORPHAN-catch', any(c == 'A-STIMORPHAN' and l == 'FAIL' for l, c, _ in RESULTS))

    # 12. A-STIMORPHAN passes when a long passage is embedded
    def b_embed(d):
        long = ' '.join(['word'] * 60)
        d.add_paragraph('Q.1  Read the following passage and answer the question. ' + long)
        d.add_paragraph('What is the tone?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_embed); _reset()
    _t, bl = parse_blocks(Document(p)); gate_stimorphan(bl, _src_stub(tq=1))
    check('A-STIMORPHAN-pass', not any(c == 'A-STIMORPHAN' and l == 'FAIL'
                                       for l, c, _ in RESULTS))

    # 13. A-ENCODING catches U+FFFD
    def b_fffd(d):
        d.add_paragraph('Q.1  Bad char � here')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_fffd); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1))
    check('A-ENCODING-catch', any(c == 'A-ENCODING' and l == 'FAIL' for l, c, _ in RESULTS))

    # 14. A-SCRIPT passes Devanagari when language=hindi, fails when english
    def b_dev(d):
        d.add_paragraph('Q.1  प्रश्न यहाँ है')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_dev)
    _reset(); gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    eng_fail = any(c == 'A-SCRIPT' and l == 'FAIL' for l, c, _ in RESULTS)
    _reset(); gate_encoding_script(Document(p), _src_stub(tq=1, lang='hindi'))
    hin_ok = not any(c == 'A-SCRIPT' and l == 'FAIL' for l, c, _ in RESULTS)
    check('A-SCRIPT-lang-aware', eng_fail and hin_ok)

    # 15. A-DUP catches a stem repeated from a prior mock
    def b_dupstem(d):
        d.add_paragraph('Q.1  The capital of France is which city among these')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_dupstem); _reset()
    src = _src_stub(tq=1)
    src['registry'] = {'stem_texts': ['the capital of france is which city among these',
                                      'unrelated prior stem about rivers and lakes here']}
    # prior = all but trailing tq(=1) → first entry is prior
    _t, bl = parse_blocks(Document(p)); gate_dup(bl, src)
    check('A-DUP-catch', any(c == 'A-DUP' and l == 'FAIL' for l, c, _ in RESULTS))

    # 16. A-MATHRASTER name-contract: math-token names flagged, generic names not
    check('A-MATHRASTER-regex', bool(MATH_TOKEN_NAME.search('q55_e1.png'))
          and not MATH_TOKEN_NAME.search('Picture 3'))

    # 17. A-OPTREF catches missing escape option
    def b_optref(d):
        d.add_paragraph('Q.1  Identify the error; if there is no error select the last option.')
        for i, o in enumerate(('Part A', 'Part B', 'Part C', 'Part D'), 1):
            d.add_paragraph(f'{i}.  {o}')   # no "No error" option
    p = _mini_doc(tmp, b_optref); _reset()
    _t, bl = parse_blocks(Document(p)); gate_optref(bl, _src_stub(tq=1))
    check('A-OPTREF-catch', any(c == 'A-OPTREF' and l == 'FAIL' for l, c, _ in RESULTS))

    # 18. block parser merges OMML text (pure-math stem not seen empty)
    check('omml-merge-helper', callable(para_text))

    # 19. A-SCRIPT: accented Latin (cafe/resume) NOT flagged on an english exam
    def b_acc(d):
        d.add_paragraph('Q.1  The café served a résumé with naïve charm.')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_acc); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    check('A-SCRIPT-accented-latin-ok', not any(c == 'A-SCRIPT' and l == 'FAIL'
                                                for l, c, _ in RESULTS))

    # 20. A-SCRIPT: Greek math symbols NOT flagged on an english exam
    def b_grk(d):
        d.add_paragraph('Q.1  If α + β = θ then θ = ?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_grk); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    check('A-SCRIPT-greek-ok', not any(c == 'A-SCRIPT' and l == 'FAIL'
                                       for l, c, _ in RESULTS))

    # 21. A-ZIP: rels parsing is attribute-ORDER-INDEPENDENT (Target before Id)
    rels_tf = '<Relationship Target="media/image1.png" Type="x" Id="rId9"/>'
    rel_map = {}
    for tag in re.findall(r'<Relationship\b[^>]*/?>', rels_tf):
        idm = re.search(r'\bId="([^"]+)"', tag); tgm = re.search(r'\bTarget="([^"]+)"', tag)
        if idm and tgm:
            rel_map[idm.group(1)] = tgm.group(1)
    check('A-ZIP-attr-order', rel_map.get('rId9') == 'media/image1.png')

    # 22. A-OPTN: an enumerated passage point before the options does NOT inflate
    #     the option count (trailing-oc extraction)
    def b_enum(d):
        d.add_paragraph('Q.1  Read the data.')
        d.add_paragraph('1.  earlier enumerated passage point that is not an option')
        d.add_paragraph('Which is correct?')
        for i, o in enumerate(('Opt1', 'Opt2', 'Opt3', 'Opt4'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_enum); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTN-enum-no-false', not any(c == 'A-OPTN' and l == 'FAIL'
                                          for l, c, _ in RESULTS))

    # 23. A-OPTN passes figural bare-label image options; roman + alpha label sets
    def b_fig(d):
        d.add_paragraph('Q.1  Select the figure.')
        for i in range(1, 5):
            d.add_paragraph(f'{i}.')          # bare label (image would follow)
    p = _mini_doc(tmp, b_fig); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    fig_ok = not any(c == 'A-OPTN' and l == 'FAIL' for l, c, _ in RESULTS)
    def b_rom(d):
        d.add_paragraph('Q.1  Pick.')
        for lab in ('i', 'ii', 'iii', 'iv'):
            d.add_paragraph(f'{lab}.  t{lab}')
    p = _mini_doc(tmp, b_rom); _reset()
    _t, bl = parse_blocks(Document(p))
    s2 = _src_stub(tq=1); s2['opt_label_fmt'] = 'i/ii/iii/iv'
    gate_options(bl, s2)
    rom_ok = not any(l == 'FAIL' for l, c, _ in RESULTS)
    check('A-OPTN-figural+roman', fig_ok and rom_ok)

    # 24. A-MSQ-INSTR (machine): a section expecting 1 multi Q but 0 instruction-carrying
    #     stems → FAIL (a multi Q is missing its select-instruction).
    def b_msq_missing(d):
        _add_q(d, 1, stem='Which of the following are prime?')   # multi expected, NO instruction
    p = _mini_doc(tmp, b_msq_missing); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_multi_by_section'] = {'S1': 1}
    s['msq_instruction_phrases'] = ['one or more', 'may be correct']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-catch', any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 25. A-MSQ-INSTR passes when the multi Q carries its instruction in the Q.N line.
    def b_msq_ok(d):
        _add_q(d, 1, stem='Which of the following are prime? (One or more options may be correct)')
    p = _mini_doc(tmp, b_msq_ok); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_multi_by_section'] = {'S1': 1}
    s['msq_instruction_phrases'] = ['one or more', 'may be correct']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-pass', not any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 26. A-MSQ-INSTR is DORMANT when the blueprint declares no multi subtopics.
    def b_single(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_single); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['expected_multi_by_section'] = {}
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-dormant', not any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 27. A-ANSKEY catches a SET-valued key leak ("Q.1 -> 1,2,4"), not just single-digit.
    def b_setkey(d):
        _add_q(d, 1); d.add_paragraph('Answer Key: Q.1 -> 1,2,4')
    p = _mini_doc(tmp, b_setkey); _reset()
    gate_anskey(Document(p))
    check('A-ANSKEY-setleak-catch', any(c == 'A-ANSKEY' and l == 'FAIL' for l, c, _ in RESULTS))

    # 28. empty document does not crash any gate
    def b_empty(d):
        pass  # CLASS: J — inert test fixture: builds an empty doc for the self-test.
              # No tool call and no model agency at all; tagged so C6 has a verdict.
    p = _mini_doc(tmp, b_empty); _reset()
    try:
        mm = gate_zip(p); doc = Document(p); _t, bl = parse_blocks(doc)
        st = _src_stub(tq=0)
        for fn in (lambda: gate_structure(bl, st), lambda: gate_options(bl, st),
                   lambda: gate_qnfirst(bl), lambda: gate_blanksep(doc, bl),
                   lambda: gate_font(doc, st), lambda: gate_sechdr(bl, doc, st),
                   lambda: gate_anskey(doc), lambda: gate_stimorphan(bl, st),
                   lambda: gate_underline(bl), lambda: gate_omml(doc, st, True),
                   lambda: gate_frac_ascii(bl, st), lambda: gate_images(bl, st, mm),
                   lambda: gate_optref(bl, st), lambda: gate_encoding_script(doc, st),
                   lambda: gate_dup(bl, st), lambda: gate_header(doc, bl, st),
                   lambda: gate_nat(bl, st)):
            fn()
        empty_ok = True
    except Exception:
        empty_ok = False
    check('empty-doc-no-crash', empty_ok)

    # 29. A-NAT-NOOPT (machine): a Q the registry marks NAT (options_by_q=0) that RENDERS
    #     options → FAIL (a numerical question must carry none).
    def b_nat_hasopts(d):
        _add_q(d, 1, stem='Find the value. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_hasopts); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True; s['options_by_q'] = {'1': 0}
    gate_nat(bl, s)
    check('A-NAT-NOOPT-catch', any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 30. A-NAT-NOOPT passes when the NAT Q renders zero options.
    def b_nat_noopts(d):
        _add_q(d, 1, opts=(), stem='Find the value. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_noopts); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True; s['options_by_q'] = {'1': 0}
    gate_nat(bl, s)
    check('A-NAT-NOOPT-pass', not any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 31. A-NAT-NOOPT is DORMANT when the blueprint declares no numerical subtopics.
    def b_nat_dormant(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_nat_dormant); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)   # nat_present default false; options_by_q empty
    gate_nat(bl, s)
    check('A-NAT-NOOPT-dormant', not any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 32. A-NAT-INSTR (machine): a section expecting 1 NAT Q but 0 instruction-carrying
    #     stems → FAIL (a numerical Q is missing its numerical-entry instruction).
    def b_nat_missing(d):
        _add_q(d, 1, opts=(), stem='Find the value of x.')
    p = _mini_doc(tmp, b_nat_missing); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_nat_by_section'] = {'S1': 1}
    s['nat_instruction_phrases'] = ['numerical value', 'enter your answer']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_nat(bl, s)
    check('A-NAT-INSTR-catch', any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 33. A-NAT-INSTR passes when the NAT Q carries its instruction in the Q.N line.
    def b_nat_ok(d):
        _add_q(d, 1, opts=(), stem='Find the value of x. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_ok); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_nat_by_section'] = {'S1': 1}
    s['nat_instruction_phrases'] = ['numerical value', 'enter your answer']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_nat(bl, s)
    check('A-NAT-INSTR-pass', not any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 34. A-NAT-INSTR is DORMANT when the blueprint declares no numerical subtopics.
    def b_nat_dormant2(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_nat_dormant2); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['expected_nat_by_section'] = {}
    gate_nat(bl, s)
    check('A-NAT-INSTR-dormant', not any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 35. A-NAT-GRADE (machine, v2.8): sidecar's own nat_grading_value does NOT match a
    #     fresh derive_nat_grading() re-run on the sidecar's own nat_value/ca_range/
    #     stem_precision -> FAIL (e.g. Step 7 stored '3e-9' instead of the correct '3').
    def b_grade_bad(d):
        _add_q(d, 1, opts=(), stem='Find the rate. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_grade_bad); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True
    s['concept_map'] = {'1': {'qtype': 'nat', 'ca_range': None,
                               'nat_grading_type': 'positive_integer',
                               'nat_grading_value': '3e-9', 'stem_precision': None}}
    s['answers'] = {'1': 3}
    gate_nat(bl, s)
    check('A-NAT-GRADE-catch', any(c == 'A-NAT-GRADE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 36. A-NAT-GRADE passes when the sidecar's grading value matches a fresh re-run,
    #     including the stem_precision-driven decimal_fixed branch (round-half-up, padded).
    def b_grade_ok(d):
        _add_q(d, 1, opts=(), stem='Find the value. Round off to two decimal places.')
    p = _mini_doc(tmp, b_grade_ok); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True
    s['concept_map'] = {'1': {'qtype': 'nat', 'ca_range': None,
                               'nat_grading_type': 'decimal_fixed',
                               'nat_grading_value': '3.00', 'stem_precision': 2}}
    s['answers'] = {'1': 3}
    gate_nat(bl, s)
    check('A-NAT-GRADE-pass', not any(c == 'A-NAT-GRADE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 37. A-NAT-GRADE is DORMANT when the blueprint declares no numerical subtopics.
    def b_grade_dormant(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_grade_dormant); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)   # nat_present default false
    gate_nat(bl, s)
    check('A-NAT-GRADE-dormant-nonat',
          not any(c == 'A-NAT-GRADE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 38. A-NAT-GRADE is DORMANT when nat_present=True but no --key sidecar was supplied
    #     (Step 8 does not receive the answer_key sidecar by default, S0-1).
    def b_grade_dormant_nokey(d):
        _add_q(d, 1, opts=(), stem='Find the value. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_grade_dormant_nokey); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True   # concept_map left empty (no --key)
    gate_nat(bl, s)
    check('A-NAT-GRADE-dormant-nokey',
          not any(c == 'A-NAT-GRADE' and l == 'FAIL' for l, c, _ in RESULTS))

    # ── v2.6 COMPLETION-GATE fixtures (S5-1A C1–C7) ────────────────────────────
    # Shared: a clean 1-Q docx (no artefacts) and an evidence dir.
    def _cg_doc(build):
        pp = _mini_doc(tmp, build)
        dd = Document(pp); _tt, bb = parse_blocks(dd)
        return dd, bb
    def _write_state(name, state):
        sp = os.path.join(tmp, name)
        json.dump(state, open(sp, 'w', encoding='utf-8'))
        return sp
    _evd = os.path.join(tmp, 'evdir'); os.makedirs(_evd, exist_ok=True)

    # 35. COMPLETION-GATE PASS on a complete, evidence-clean single-Q ledger.
    dcg, bcg = _cg_doc(lambda d: _add_q(d, 1))
    _reset()
    st35 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'fact_sources': [], 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st35.json', st35), 1, bcg, dcg)
    check('CG-pass', rc == 0 and not any(l == 'FAIL' for l, c, _ in RESULTS))

    # 36. SKIPPED-PHASE-2: empty ledger + no batches → C1 + C2 FAIL.
    _reset()
    st36 = {'K': 1, 'batches_done': [], 'evidence_dir': _evd, 'ledger': {'entries': {}}}
    rc = completion_gate(_write_state('st36.json', st36), 1, bcg, dcg)
    check('CG-skipped-phase2', rc == 1
          and any(c == 'C1' and l == 'FAIL' for l, c, _ in RESULTS)
          and any(c == 'C2' and l == 'FAIL' for l, c, _ in RESULTS))

    # 37. PARTIAL-REVIEW: tq=2 but only Q1 in the ledger → C2 FAIL.
    _reset()
    st37 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False, 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st37.json', st37), 2, bcg, dcg)
    check('CG-partial-review', rc == 1 and any(c == 'C2' and l == 'FAIL' for l, c, _ in RESULTS))

    # 38. UNSOURCED-FACT: a factual entry with no fact_sources → C5 FAIL.
    _reset()
    st38 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': True,
                        'fact_sources': [], 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st38.json', st38), 1, bcg, dcg)
    check('CG-unsourced-fact', rc == 1 and any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 39. UNVIEWED artefact (paper has a table, ledger has no stamp) → C7 FAIL.
    def b_tbl(d):
        d.add_paragraph('Q.1  Study the table.')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
        tt = d.add_table(rows=2, cols=2)
        tt.cell(0, 0).text = 'h1'; tt.cell(0, 1).text = 'h2'
        tt.cell(1, 0).text = '1'; tt.cell(1, 1).text = '2'
    dtbl, btbl = _cg_doc(b_tbl)
    _reset()
    st39 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False, 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st39.json', st39), 1, btbl, dtbl)
    check('CG-unviewed-artefact', rc == 1 and any(c == 'C7' and l == 'FAIL' for l, c, _ in RESULTS))

    # 40. MISSING evidence FILE (stamp present, trace file absent) → C6 FAIL.
    _reset()
    st40 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'artefact_stamps': {'tables': [{'idx': 0, 'stamp': 'recomputed',
                                            'trace': os.path.join(_evd, 'does_not_exist.txt')}]}}}}}
    rc = completion_gate(_write_state('st40.json', st40), 1, btbl, dtbl)
    check('CG-missing-evidence-file', rc == 1 and any(c == 'C6' and l == 'FAIL' for l, c, _ in RESULTS))

    # 41. FACT saved-file MISSING (source named but file absent) → C5 FAIL.
    _reset()
    st41 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': True,
                        'fact_sources': [{'url': 'x', 'date': 'y',
                                          'saved': os.path.join(_evd, 'nf.json')}],
                        'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st41.json', st41), 1, bcg, dcg)
    check('CG-factfile-missing', rc == 1 and any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 42. EVIDENCE-BACKED artefact stamp (trace file exists) → PASS.
    _trace = os.path.join(_evd, 'q1_table.txt')
    open(_trace, 'w', encoding='utf-8').write('grid a,b / 1,2 ; total row recomputed = 3 OK')
    _reset()
    st42 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'artefact_stamps': {'tables': [{'idx': 0, 'stamp': 'recomputed',
                                            'trace': _trace}]}}}}}
    rc = completion_gate(_write_state('st42.json', st42), 1, btbl, dtbl)
    check('CG-evidence-backed-pass', rc == 0 and not any(l == 'FAIL' for l, c, _ in RESULTS))

    # ════════════════════════════════════════════════════════════════════
    # v2.12 — GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING regression lock (D4)
    # ════════════════════════════════════════════════════════════════════
    # WHY THESE EXIST. Until v2.12 this suite returned 51/51 PASS on a file that
    # could not survive a real run, because NO fixture ever built a registry
    # carrying figural_manifests[].object_types. Every fixture took A-FIGPROFILE's
    # DORMANT branch, so the unbound `bc` at the primary branch was never
    # executed. The v2.6 hardening caught hollow FILES; it did not catch a hollow
    # BRANCH. These fixtures execute the primary branch in every environment the
    # estate actually presents, which is the only thing that would have caught it.
    import importlib as _il

    def _figsrc(obj_types, sub_ids, rules=''):
        s = _src_stub(tq=2)
        s['figural_object_types'] = obj_types
        s['figural_subtopics'] = sub_ids
        s['section_rules_text'] = rules
        s['figural_qs'] = {1, 2}
        return s

    def _run_figprofile(src_d):
        """Run ONLY the A-FIGPROFILE path via gate_images on a 2-Q fixture."""
        p = _mini_doc(tmp, lambda d: (_add_q(d, 1), _add_q(d, 2)))
        _reset()
        doc = Document(p); _t, blks = parse_blocks(doc)
        _safe_gate('A-IMAGES', gate_images, blks, src_d, {})
        return [(l, c, m) for l, c, m in RESULTS if c in ('A-FIGPROFILE', 'A-GATEERROR')]

    class _StubBC:
        """A complete, conforming stand-in for blueprint_core."""
        @staticmethod
        def parse_image_analysis_blocks(t): return {'s.a': {'dominant_object_type': 'x'}}
        @staticmethod
        def figural_generation_profile(p): return {'dominant_object_type': 'x'}
        @staticmethod
        def check_figural_conformance(g, p): return ('PASS', '')

    _saved_bc = sys.modules.get('blueprint_core')

    def _with_bc(mod):
        if mod is None:
            sys.modules.pop('blueprint_core', None)
            sys.modules['blueprint_core'] = None   # forces ImportError on import
        else:
            sys.modules['blueprint_core'] = mod

    _OT = {'1': 'cycle_diagram', '2': 'cycle_diagram'}
    _SI = {'1': 's.a', '2': 's.a'}

    # 43. NON-DORMANT-BRANCH COVERAGE — the fixture that would have caught D1.
    #     object_types present + engine importable → the primary branch EXECUTES
    #     and must produce a real verdict, never a NameError.
    _with_bc(_StubBC)
    r = _run_figprofile(_figsrc(_OT, _SI))
    check('FIGPROFILE-primary-branch-runs',
          any(c == 'A-FIGPROFILE' and l == 'OK' for l, c, _ in r)
          and not any(c == 'A-GATEERROR' for _, c, _ in r))

    # 44. CATCH PATH — a non-conforming subtopic must FAIL, naming it.
    class _FailBC(_StubBC):
        @staticmethod
        def check_figural_conformance(g, p): return ('FAIL', 'type mismatch')
    _with_bc(_FailBC)
    r = _run_figprofile(_figsrc(_OT, _SI))
    check('FIGPROFILE-catches-nonconformance',
          any(c == 'A-FIGPROFILE' and l == 'FAIL' for l, c, _ in r))

    # 45. MISSING-ENGINE DEGRADATION — must WARN "NOT CHECKED", never raise.
    _with_bc(None)
    r = _run_figprofile(_figsrc(_OT, _SI))
    check('FIGPROFILE-missing-engine-warns',
          any(c == 'A-FIGPROFILE' and l == 'WARN' and 'NOT CHECKED' in m for l, c, m in r)
          and not any(c == 'A-GATEERROR' for _, c, _ in r))

    # 46. STALE-ENGINE — imports fine, lacks a delegated function. The capability
    #     check (L2) must catch it; an import guard alone would let the call site
    #     raise AttributeError and abort the run.
    class _StaleBC:
        @staticmethod
        def parse_image_analysis_blocks(t): return {}
        @staticmethod
        def figural_generation_profile(p): return None
    _with_bc(_StaleBC)
    r = _run_figprofile(_figsrc(_OT, _SI))
    check('FIGPROFILE-stale-engine-warns',
          any(c == 'A-FIGPROFILE' and l == 'WARN' and 'stale engine' in m for l, c, m in r)
          and not any(c == 'A-GATEERROR' for _, c, _ in r))

    # 47. ENGINE RAISES AT THE CALL SITE — L3 must convert it to a logged skip.
    class _BoomBC(_StubBC):
        @staticmethod
        def parse_image_analysis_blocks(t): raise RuntimeError('boom')
    _with_bc(_BoomBC)
    r = _run_figprofile(_figsrc(_OT, _SI))
    check('FIGPROFILE-engine-raise-warns',
          any(c == 'A-FIGPROFILE' and l == 'WARN' for l, c, _ in r)
          and not any(c == 'A-GATEERROR' for _, c, _ in r))

    # 48. 0/0 IS NOT EVIDENCE — object_types present but no usable subtopic_ids
    #     must WARN, not claim conformance it never tested (edge case 6).
    _with_bc(_StubBC)
    r = _run_figprofile(_figsrc(_OT, {}))
    check('FIGPROFILE-zero-of-zero-warns',
          any(c == 'A-FIGPROFILE' and l == 'WARN' and 'NOT ESTABLISHED' in m for l, c, m in r))

    # 49. LEGACY PATH UNCHANGED — no object_types → dormant _ok. ~200 exams on
    #     pre-v5.31 output must keep passing exactly as before (EC-V18).
    _with_bc(None)
    r = _run_figprofile(_figsrc({}, {}))
    check('FIGPROFILE-legacy-dormant-ok',
          any(c == 'A-FIGPROFILE' and l == 'OK' and 'dormant' in m for l, c, m in r))

    # restore the real module state
    if _saved_bc is not None:
        sys.modules['blueprint_core'] = _saved_bc
    else:
        sys.modules.pop('blueprint_core', None)

    # 50. GATE FAULT ISOLATION (P6) — an exploding gate must become a LOUD, NAMED
    #     FAIL while the run continues. This is the fixture that makes the entire
    #     "permanent halt" failure mode impossible for any future gate.
    _reset()
    def _boom(*a, **k): raise ValueError('synthetic')
    _safe_gate('A-SYNTHETIC', _boom)
    check('GATEERROR-isolates-and-names',
          any(c == 'A-GATEERROR' and l == 'FAIL' and 'A-SYNTHETIC' in m for l, c, m in RESULTS))

    # 51. FAULT ISOLATION DOES NOT MASK — a crashed gate is FAIL severity, so the
    #     run exits non-zero and the paper CANNOT be certified clean. Degradation
    #     must never be quietly survivable.
    check('GATEERROR-blocks-certification',
          any(l == 'FAIL' for l, _, _ in RESULTS))

    # 52. UNDEFINED-NAME SCAN (test 10) — self-hosted. Scans THIS file for any
    #     Load-context name never bound anywhere. This is the generalised guard:
    #     it catches the next `bc`-class defect automatically, in any gate.
    _und = {}
    try:
        import builtins as _bi, ast
        _tree = ast.parse(open(__file__, encoding='utf-8').read())
        _bnd = set(dir(_bi)) | {'__file__', '__name__', '__doc__', '__builtins__'}
        for _n in ast.walk(_tree):
            if isinstance(_n, ast.alias): _bnd.add(_n.asname or _n.name.split('.')[0])
            elif isinstance(_n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): _bnd.add(_n.name)
            elif isinstance(_n, ast.Name) and isinstance(_n.ctx, (ast.Store, ast.Del)): _bnd.add(_n.id)
            elif isinstance(_n, ast.arg): _bnd.add(_n.arg)
            elif isinstance(_n, ast.ExceptHandler) and _n.name: _bnd.add(_n.name)
            elif isinstance(_n, (ast.Global, ast.Nonlocal)): _bnd |= set(_n.names)
        for _n in ast.walk(_tree):
            if isinstance(_n, ast.Name) and isinstance(_n.ctx, ast.Load) and _n.id not in _bnd:
                _und.setdefault(_n.id, []).append(_n.lineno)
    except Exception:
        _und = {'<scan-failed>': []}
    check('NO-UNDEFINED-NAMES', not _und)

    # ════════════════════════════════════════════════════════════════════
    # v2.13 — GAP-2026-08-01-FIGSPEC-TRANSPORT regression lock (D4)
    # ════════════════════════════════════════════════════════════════════
    # WHY THESE EXIST. v2.12 closed the HALT and left the twelve gates it
    # rescued VACUOUS: Block.images was declared '# reserved' and appended to
    # nowhere, so every gate iterated an empty list and printed "0 figure(s)
    # conform." on every paper in every exam. 61/61 PASS again coexisted with
    # zero real coverage — the same hollow-branch class as the halt itself, one
    # gate-family over. NO fixture had ever put an image in a block. These do.
    #
    # figural_core is STUBBED (the pattern v2.12 used for blueprint_core) so the
    # severity-routing fixtures assert THIS file's logic and hold identically on
    # a machine with no matplotlib/PIL — the environment ~200 exams may present.

    def _png_bytes(w=8, h=8):
        """A minimal, valid RGB PNG. stdlib only — the self-test must never
        require matplotlib or PIL to prove that images are attached."""
        raw = b''.join(b'\x00' + b'\xff\x00\x00' * w for _ in range(h))
        def _ck(t, d):
            c = t + d
            return (struct.pack('>I', len(d)) + c
                    + struct.pack('>I', zlib.crc32(c) & 0xffffffff))
        return (b'\x89PNG\r\n\x1a\n'
                + _ck(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                + _ck(b'IDAT', zlib.compress(raw))
                + _ck(b'IEND', b''))

    def _img_doc(names, in_table=False):
        """A 1-question docx carrying len(names) inline drawings, each stamped
        with its canonical docPr name + its OWN alt text (S10-8 does exactly
        this via _name_last_drawing). in_table places them in a table cell."""
        from docx import Document as D
        from docx.shared import Inches
        d = D()
        d.add_paragraph('Q.1  Study the figure.')
        holder = d.add_table(rows=1, cols=1).rows[0].cells[0] if in_table else d
        for nm in names:
            p = holder.add_paragraph()
            p.add_run().add_picture(io.BytesIO(_png_bytes()), width=Inches(1.0))
        d.add_paragraph('')
        pth = os.path.join(tmp, 'img.docx')
        d.save(pth)
        # stamp canonical name + per-drawing descr, in document order
        import shutil as _sh
        tmpd = tempfile.mkdtemp(); out = os.path.join(tmpd, 'stamped.docx')
        with zipfile.ZipFile(pth) as zin:
            items = zin.infolist()
            xml = zin.read('word/document.xml').decode('utf-8')
            it = iter(names)
            _cnt = [0]
            def _sub(mo):
                nm = next(it, 'x.png'); _cnt[0] += 1
                close = '/>' if mo.group(0).rstrip().endswith('/>') else '>'
                return (f'<wp:docPr id="{_cnt[0]}" name="{nm}" '
                        f'descr="alt for {nm}"{close}')
            xml = re.sub(r'<wp:docPr\b[^>]*>', _sub, xml)
            with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zo:
                for i in items:
                    zo.writestr(i, xml.encode('utf-8')
                                if i.filename == 'word/document.xml'
                                else zin.read(i.filename))
        return out

    def _attach(docx_path):
        _reset()
        mm = gate_zip(docx_path)
        doc = Document(docx_path); _t, blks = parse_blocks(doc)
        dec, res = attach_block_images(blks, mm, extract_media(docx_path, mm))
        return blks, dec, res

    class _StubFC:
        """figural_core stand-in. LEGACY / FINDINGS are set per fixture."""
        LEGACY = True
        FINDINGS = []
        @staticmethod
        def is_legacy(spec): return _StubFC.LEGACY
        @staticmethod
        def audit_figure(spec, png, descr=None): return (list(_StubFC.FINDINGS), [])
        @staticmethod
        def audit_gate_id(f): return f.split(':')[0].strip()
        @staticmethod
        def triage(findings, spec=None):
            sev = 'AMBER' if _StubFC.LEGACY else 'BLOCKING'
            return {'BLOCKING': findings if sev == 'BLOCKING' else [],
                    'VOID_ITEM': [], 'AMBER': findings if sev == 'AMBER' else []}

    _saved_fc = sys.modules.get('figural_core')

    def _run_figgates(blks, specs=None, legacy=True, findings=()):
        _StubFC.LEGACY = legacy; _StubFC.FINDINGS = list(findings)
        sys.modules['figural_core'] = _StubFC
        s = _src_stub(tq=1)
        s['figure_specs'] = specs or {}
        _reset()
        _safe_gate('A-IMAGES', gate_images, blks, s, {})
        return [(l, c, m) for l, c, m in RESULTS if c.startswith('A-FIG')
                or c == 'A-GATEERROR']

    _FIGGATES = ('A-FIGSCALE', 'A-FIGLABEL', 'A-FIGDPI', 'A-FIGDEGEN',
                 'A-FIGMONO', 'A-FIGOPTUNIF', 'A-FIGCOLOUR', 'A-FIGCVD',
                 'A-FIGSERIES', 'A-FIGGLYPH', 'A-FIGALT', 'A-FIGLABELPX')

    # 53. BLOCK.IMAGES IS POPULATED — the fixture whose absence WAS the defect.
    #     Nothing in this suite had ever asserted that a block carries an image.
    _b53, _d53, _r53 = _attach(_img_doc(['q1_problem.png', 'q1_opt1.png']))
    check('IMAGES-attached-to-block',
          _d53 == 2 and _r53 == 2 and len(_b53[0].images) == 2
          and all(i.get('path') and os.path.exists(i['path']) for i in _b53[0].images))

    # 54. NAME + PER-DRAWING ALT TEXT — A-FIGALT reads @descr, so a drawing must
    #     carry ITS OWN, not the neighbouring drawing's (para_images_ext walks
    #     each <w:drawing> as a unit rather than zipping two flat lists).
    check('IMAGES-name-and-descr-per-drawing',
          [i['name'] for i in _b53[0].images] == ['q1_problem.png', 'q1_opt1.png']
          and _b53[0].images[0]['descr'] == 'alt for q1_problem.png'
          and _b53[0].images[1]['descr'] == 'alt for q1_opt1.png')

    # 55. TABLE-EMBEDDED DRAWINGS COUNTED — a DI chart or a figure/option fusion
    #     table puts images in cells; a block-level paras scan misses them all.
    _b55, _d55, _r55 = _attach(_img_doc(['q1_stim.png'], in_table=True))
    check('IMAGES-inside-tables-counted', _d55 == 1 and _r55 == 1)

    # 56. THE VACUOUS-PASS CATCH. With figures present the gates must report a
    #     NON-ZERO evaluated count. On v2.11-v2.12.1 every one of these printed
    #     "0 figure(s) conform." and this fixture fails on that build.
    r = _run_figgates(_b53)
    check('FIGGATES-not-vacuous',
          all(any(c == g and '0 figure(s)' not in m for l, c, m in r)
              for g in _FIGGATES))

    # 57. ROSTER INVARIANCE (§R15) — exactly ONE line per figure gate, with and
    #     without figures. Also locks out the duplicate second A-FIGDPI line the
    #     old EC-V18 note emitted, which would have broken the count signal.
    _b57, _, _ = _attach(_mini_doc(tmp, lambda d: _add_q(d, 1)))
    r0 = _run_figgates(_b57)
    check('FIGGATES-roster-invariant',
          all(sum(1 for _, c, _ in r if c == g) == 1 for g in _FIGGATES)
          and all(sum(1 for _, c, _ in r0 if c == g) == 1 for g in _FIGGATES))

    # 58. ZERO-IMAGE PAPER IS DORMANT, NOT "CONFORMANT" — a paper with no
    #     drawings must say so, never claim a conformance it never tested.
    check('FIGGATES-zero-image-dormant',
          all(any(c == g and l == 'OK' and 'dormant' in m for l, c, m in r0)
              for g in _FIGGATES))

    # 59. DECLARED-BUT-UNREADABLE ⇒ COVERAGE WARN (D3, edge case 6 applied here):
    #     drawings present but none openable is a coverage GAP, never a pass.
    _b59 = [Block(1)]
    _b59[0].images = [{'name': 'q1_problem.png', 'rid': 'rId9',
                       'part': 'image1.png', 'descr': '', 'path': None}]
    r = _run_figgates(_b59)
    check('FIGGATES-declared-unreadable-warns',
          all(any(c == g and l == 'WARN' and 'NOT ESTABLISHED' in m
                  for l, c, m in r) for g in _FIGGATES))

    # 60. SPEC TRANSPORT RESOLVES (D2) — registry-borne figure_specs keyed by the
    #     canonical docPr name, with extension-stripped and media-part fallbacks.
    _spec = {'class': 'data_series', 'placement_scale': 1.0}
    check('FIGSPEC-transport-resolves',
          resolve_figure_spec({'name': 'q1_problem.png', 'part': 'image1.png'},
                              {'q1_problem.png': _spec}) is _spec
          and resolve_figure_spec({'name': 'q1_problem.png', 'part': ''},
                                  {'q1_problem': _spec}) is _spec
          and resolve_figure_spec({'name': '', 'part': 'image1.png'},
                                  {'image1.png': _spec}) is _spec
          and resolve_figure_spec({'name': 'Picture 1', 'part': 'image9.png'},
                                  {'q1_problem.png': _spec}) == {})

    # 61. NON-LEGACY DEFECT BLOCKS CERTIFICATION — a v5.33+ render that carries a
    #     sidecar and still regresses is a real FAIL; exit is non-zero (MANDATE D).
    r = _run_figgates(_b53, specs={'q1_problem.png': _spec, 'q1_opt1.png': _spec},
                      legacy=False, findings=['A-FIGSCALE: scale 0.5 != 1.0'])
    check('FIGGATES-nonlegacy-defect-fails',
          any(c == 'A-FIGSCALE' and l == 'FAIL' and 'REGRESSION' in m for l, c, m in r))

    # 62. EC-V18 IS A DELIVERY TOLERANCE — the SAME finding on a pre-v5.33 figure
    #     with no sidecar must stay LOUD but must NOT block: the spec's EC-V18 is
    #     non-negotiable that ~200 existing exams "keep auditing AND DELIVERING
    #     untouched". A FAIL here exits non-zero and MANDATE D then refuses to
    #     certify — turning a coverage fix into an estate-wide outage.
    r = _run_figgates(_b53, legacy=True, findings=['A-FIGSCALE: scale 0.5 != 1.0'])
    check('FIGGATES-legacy-degrades-without-blocking',
          any(c == 'A-FIGSCALE' and l == 'WARN' and 'EC-V18' in m for l, c, m in r)
          and not any(c == 'A-FIGSCALE' and l == 'FAIL' for l, c, _ in r))

    # 63. END-TO-END WIRING THROUGH run_audit — THE M1 FIXTURE.
    #     Fixtures 53-62 call attach_block_images() directly, so every one of
    #     them still passes if the CALL inside run_audit is deleted. That is the
    #     precise shape of the v2.10 defect this whole gap family descends from:
    #     the delegation was written at the call sites and never bound, and no
    #     fixture exercised the real entry point. Mutation-verified: removing the
    #     run_audit call fails THIS check and only this check.
    _StubFC.LEGACY = True; _StubFC.FINDINGS = []
    sys.modules['figural_core'] = _StubFC
    _e2e = _img_doc(['q1_problem.png', 'q1_opt1.png'])
    _args63 = argparse.Namespace(docx=_e2e, blueprint=None, rules=None,
                                 manifest=None, registry=None, mockN=1,
                                 final=False, audit_state=None, key=None,
                                 self_test=True)
    _so = sys.stdout
    try:
        sys.stdout = io.StringIO()
        run_audit(_args63)
        _r63 = list(RESULTS)
    finally:
        sys.stdout = _so
    check('FIGGATES-wired-into-run-audit',
          all(any(c == g and '0 figure(s)' not in m and 'NOT ESTABLISHED' not in m
                  and 'dormant' not in m for l, c, m in _r63) for g in _FIGGATES))

    # 64. PER-FIGURE FAULT ISOLATION — ONE BAD SPEC MUST NOT COST ELEVEN GATES
    #     THEIR VERDICT. Found empirically while testing D2 against a real paper:
    #     a partially-recorded FigureSpec (render_figure() fills png_px /
    #     font_pt_native / placement_scale only AFTER it reads the artefact back,
    #     so a render that died mid-way leaves a shape the gates index into)
    #     raised TypeError out of g_figlabel(); _safe_gate turned it into
    #     A-GATEERROR and the WHOLE A-IMAGES gate died — twelve gate lines gone,
    #     roster 47 -> 36, the §R15 invariance v2.12 had just restored broken by
    #     one figure. The spec now arrives from the REGISTRY, i.e. from outside
    #     this process, so a per-item L3 guard is mandatory, exactly as v2.12
    #     required one for blueprint_core's call sites.
    class _RaisingFC(_StubFC):
        @staticmethod
        def audit_figure(spec, png, descr=None):
            raise TypeError('list indices must be integers or slices, not str')
    _StubFC.LEGACY = True; _StubFC.FINDINGS = []
    sys.modules['figural_core'] = _RaisingFC
    _s64 = _src_stub(tq=1); _s64['figure_specs'] = {}
    _reset()
    _safe_gate('A-IMAGES', gate_images, _b53, _s64, {})
    _r64 = [(l, c, m) for l, c, m in RESULTS if c.startswith('A-FIG') or c == 'A-GATEERROR']
    check('FIGGATES-per-figure-fault-isolation',
          not any(c == 'A-GATEERROR' for _, c, _ in _r64)
          and all(sum(1 for _, c, _ in _r64 if c == g) == 1 for g in _FIGGATES)
          and all(any(c == g and l == 'WARN' and 'NOT ESTABLISHED' in m
                      for l, c, m in _r64) for g in _FIGGATES))

    if _saved_fc is not None:
        sys.modules['figural_core'] = _saved_fc
    else:
        sys.modules.pop('figural_core', None)

    # ════════════════════════════════════════════════════════════════════
    # v2.14 — B3 FACT CONTEXT DISCIPLINE regression lock
    # ════════════════════════════════════════════════════════════════════
    # B3 moves the raw search result OUT of the reasoning stream and onto disk,
    # so the saved file becomes the ONLY copy of the evidence. C5 previously
    # accepted any file >= 1 byte, which was tolerable while the result was also
    # duplicated in context and is NOT tolerable now: without a shape check the
    # discipline silently degrades from "save the result" to "touch a file".
    def _fact_state(name, recs, q='1', extra=None):
        pth = os.path.join(_evd, name)
        with open(pth, 'w', encoding='utf-8') as fh:
            if isinstance(recs, str):
                fh.write(recs)
            else:
                json.dump(recs, fh)
        srcs = [{'url': 'u', 'date': 'd', 'saved': pth}]
        ent = {'status': 'verified', 'answer_cardinality': 'single',
               'answer_unique': True, 'is_factual': True,
               'fact_sources': srcs, 'artefact_stamps': {}}
        led = {q: ent}
        if extra:
            led.update(extra)
        return {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
                'ledger': {'entries': led}}, pth

    _GOODREC = {'query': 'q', 'url': 'https://example.org/a',
                'retrieved_at': '2026-08-01T00:00:00Z', 'snippet': 's'}

    # 65. WELL-FORMED RECORD → C5 PASS (the positive control).
    _reset()
    stA, _ = _fact_state('f_ok.json', _GOODREC)
    rc = completion_gate(_write_state('stA.json', stA), 1, bcg, dcg)
    check('CG-fact-record-wellformed-passes',
          not any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 66. ONE-BYTE STUB → C5 FAIL. This is the exact file that CERTIFIED before
    #     v2.14 and that B3 makes dangerous.
    _reset()
    stB, _ = _fact_state('f_stub.json', 'x')
    rc = completion_gate(_write_state('stB.json', stB), 1, bcg, dcg)
    check('CG-fact-stub-file-fails',
          rc == 1 and any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 67. MISSING A MANDATED FIELD → C5 FAIL, naming the FIELD (never the fact —
    #     MANDATE 0). RA-11 requires query + URL + retrieval-time + snippet.
    _reset()
    _partial = dict(_GOODREC); _partial.pop('retrieved_at')
    stC, _ = _fact_state('f_partial.json', _partial)
    rc = completion_gate(_write_state('stC.json', stC), 1, bcg, dcg)
    check('CG-fact-missing-field-fails',
          rc == 1 and any(c == 'C5' and l == 'FAIL' and 'retrieved_at' in m
                          for l, c, m in RESULTS))

    # 68. BLANK FIELD IS NOT A FIELD — an empty url must fail exactly like an
    #     absent one, or "save the record" becomes "save the keys".
    _reset()
    _blank = dict(_GOODREC); _blank['url'] = '   '
    stD, _ = _fact_state('f_blank.json', _blank)
    rc = completion_gate(_write_state('stD.json', stD), 1, bcg, dcg)
    check('CG-fact-blank-field-fails',
          rc == 1 and any(c == 'C5' and l == 'FAIL' and 'url' in m
                          for l, c, m in RESULTS))

    # 69. CACHE REUSE IS LEGITIMATE — B3 dedupes a concept shared by several
    #     questions to ONE search. A record LIST, and one file referenced by two
    #     questions, must both certify; the gate reports the reuse rather than
    #     treating it as a shortfall.
    _reset()
    dcg2, bcg2 = _cg_doc(lambda d: (_add_q(d, 1), _add_q(d, 2)))
    _shared = os.path.join(_evd, 'f_shared.json')
    with open(_shared, 'w', encoding='utf-8') as fh:
        json.dump([_GOODREC, dict(_GOODREC, query='q2')], fh)
    _ent = {'status': 'verified', 'answer_cardinality': 'single',
            'answer_unique': True, 'is_factual': True,
            'fact_sources': [{'url': 'u', 'date': 'd', 'saved': _shared}],
            'artefact_stamps': {}}
    stE = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
           'ledger': {'entries': {'1': dict(_ent), '2': dict(_ent)}}}
    rc = completion_gate(_write_state('stE.json', stE), 2, bcg2, dcg2)
    check('CG-fact-cache-reuse-passes',
          not any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS)
          and any(c == 'C5' and 'cache reuse' in m for _, c, m in RESULTS))

    # ════════════════════════════════════════════════════════════════════
    # v2.15 — C1 CROSS-SESSION CHECKPOINT regression lock
    # ════════════════════════════════════════════════════════════════════
    # RA-18 claimed "resume-safe" while storing the ledger AND the evidence tree
    # under /home/claude, which does not survive a session boundary. Resume
    # therefore worked inside one session and not across one, and the failure was
    # fatal rather than degraded: C5/C6 assert that every stamped evidence file
    # EXISTS, so a perfectly remembered ledger could not certify once the files
    # were gone. Fixture 71 is the one that matters — it proves a checkpoint
    # taken in one container and restored into another still CERTIFIES.
    _ckdir = os.path.join(tmp, 'ck'); os.makedirs(_ckdir, exist_ok=True)
    _ck_evd = os.path.join(_ckdir, 'evidence'); os.makedirs(_ck_evd, exist_ok=True)
    os.makedirs(os.path.join(_ck_evd, 'facts'), exist_ok=True)
    _ck_fact = os.path.join(_ck_evd, 'facts', 'q1_abc.json')
    with open(_ck_fact, 'w', encoding='utf-8') as fh:
        json.dump(_GOODREC, fh)
    _ck_paper = _mini_doc(tmp, lambda d: _add_q(d, 1))
    _ck_state = os.path.join(_ckdir, 'audit_state.json')
    _ck_st = {'mock': 1, 'exam_code': 'EX', 'paper_id': 'MOCK:M01', 'K': 1,
              'batches_done': [1], 'evidence_dir': _ck_evd,
              'ledger': {'entries': {'1': {'status': 'verified',
                          'answer_cardinality': 'single', 'answer_unique': True,
                          'is_factual': True,
                          'fact_sources': [{'url': 'u', 'date': 'd', 'saved': _ck_fact}],
                          'artefact_stamps': {}}}}}
    with open(_ck_state, 'w', encoding='utf-8') as fh:
        json.dump(_ck_st, fh)
    _ck_zip = os.path.join(tmp, 'ck.zip')
    _man = make_checkpoint(_ck_state, _ck_zip, docx_path=_ck_paper,
                           exam='EX', mockN=1)

    # 70. BUNDLE IS COMPLETE AND SELF-DESCRIBING — state + evidence + paper, an
    #     identity triple, and a sha256 for every member.
    check('CK-bundle-complete',
          _man['schema'] == CHECKPOINT_SCHEMA and _man['exam_code'] == 'EX'
          and _man['mock'] == 1 and _man['ledger_entries'] == 1
          and _man['evidence_files'] == 1 and _man['paper_md5']
          and 'audit_state.json' in _man['files']
          and any(a.startswith('evidence/') for a in _man['files'])
          and any(a.startswith('paper/') for a in _man['files']))

    # 71. ROUND TRIP THEN CERTIFY — THE FIXTURE THIS RELEASE EXISTS FOR.
    #     Simulate the session boundary by DESTROYING the original directory, then
    #     restore into a fresh one and run the real completion gate. Before C1 this
    #     was impossible: the evidence was gone and C5 failed for ever.
    import shutil as _sh71
    _sh71.rmtree(_ckdir)
    _newdir = os.path.join(tmp, 'ck_restored')
    _man2, _stp2, _evd2 = restore_checkpoint(_ck_zip, _newdir,
                                             docx_path=_ck_paper, exam='EX', mockN=1)
    _reset()
    _dck = Document(_ck_paper); _t, _bck = parse_blocks(_dck)
    rc = completion_gate(_stp2, 1, _bck, _dck)
    check('CK-restore-then-certify',
          rc == 0 and not any(l == 'FAIL' for l, _, _ in RESULTS)
          and os.path.exists(os.path.join(_evd2, 'facts', 'q1_abc.json')))

    # 72. EVIDENCE_DIR IS REWRITTEN — the recorded path belongs to the previous
    #     session's container. If restore did not rewrite it, every C5/C6 stamp
    #     would resolve to a directory that no longer exists.
    with open(_stp2, encoding='utf-8') as fh:
        _rst = json.load(fh)
    check('CK-evidence-dir-rebased',
          _rst['evidence_dir'] == _evd2 and os.path.isdir(_rst['evidence_dir'])
          and _rst['session_log']['checkpoints_restored'][0]['batches_done'] == [1])

    # 72b. NESTED EVIDENCE PATHS REBASE — a montage in evidence/montages/ must
    #      resolve after restore, not merely a file sitting at the evidence root.
    #      Verified explicitly because the resolver's basename fallback would mask
    #      a broken rebase on a flat tree and hide it until a real paper.
    check('CK-nested-paths-rebased',
          _rst['ledger']['entries']['1']['fact_sources'][0]['saved']
              == os.path.join(_evd2, 'facts', 'q1_abc.json')
          and _rst['session_log']['checkpoints_restored'][0]['evidence_paths_rebased'] == 1)

    # 73. TAMPER / TRUNCATION IS REFUSED — a member whose bytes changed since the
    #     manifest was written must never be restored.
    _bad_zip = os.path.join(tmp, 'ck_tampered.zip')
    with zipfile.ZipFile(_ck_zip) as zin, \
         zipfile.ZipFile(_bad_zip, 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in zin.infolist():
            data = zin.read(i.filename)
            if i.filename.startswith('evidence/'):
                data = data + b' '          # one byte; hash must catch it
            zout.writestr(i, data)
    try:
        restore_checkpoint(_bad_zip, os.path.join(tmp, 'ck_t'), docx_path=_ck_paper)
        _t73 = False
    except CheckpointError as e:
        _t73 = 'integrity' in str(e)
    check('CK-tamper-refused', _t73)

    # 74. WRONG PAPER IS REFUSED — restoring onto a different document would
    #     certify an audit nobody performed on it. Strictly worse than losing the
    #     audit, so this binding is HARD.
    _other = _mini_doc(tmp, lambda d: (_add_q(d, 1), _add_q(d, 2)))
    try:
        restore_checkpoint(_ck_zip, os.path.join(tmp, 'ck_w'), docx_path=_other)
        _t74 = False
    except CheckpointError as e:
        _t74 = 'MD5' in str(e)
    check('CK-wrong-paper-refused', _t74)

    # 75. WRONG MOCK / WRONG EXAM ARE REFUSED — the other two thirds of the
    #     identity triple, checked BEFORE anything is written to disk.
    _t75a = _t75b = False
    try:
        restore_checkpoint(_ck_zip, os.path.join(tmp, 'ck_m'), mockN=2)
    except CheckpointError as e:
        _t75a = 'mock' in str(e)
    try:
        restore_checkpoint(_ck_zip, os.path.join(tmp, 'ck_e'), exam='OTHER')
    except CheckpointError as e:
        _t75b = 'exam_code' in str(e)
    check('CK-wrong-identity-refused', _t75a and _t75b)

    # 76. A NON-CHECKPOINT ARCHIVE IS REFUSED, not half-unpacked.
    _plain = os.path.join(tmp, 'plain.zip')
    with zipfile.ZipFile(_plain, 'w') as z:
        z.writestr('hello.txt', 'hi')
    try:
        restore_checkpoint(_plain, os.path.join(tmp, 'ck_p'))
        _t76 = False
    except CheckpointError as e:
        _t76 = 'manifest' in str(e)
    check('CK-not-a-checkpoint-refused',
          _t76 and not os.path.exists(os.path.join(tmp, 'ck_p', 'audit_state.json')))

    # 75b. AN UNBINDABLE BUNDLE IS REFUSED AT BOTH ENDS — building without the
    #      paper is refused outright (paper_md5 is the strongest binding, and a
    #      None there makes restore's check vacuous), and a manifest that somehow
    #      lacks it is refused on restore. Found in end-to-end testing, not by
    #      inspection: a shell quoting slip left the docx absent and the checkpoint
    #      was written anyway, with no binding at all.
    try:
        make_checkpoint(_stp2, os.path.join(tmp, 'ck_nopaper.zip'), docx_path=None)
        _t75c = False
    except CheckpointError as e:
        _t75c = 'REQUIRED' in str(e)
    _nb = os.path.join(tmp, 'ck_nobind.zip')
    with zipfile.ZipFile(_ck_zip) as zin, \
         zipfile.ZipFile(_nb, 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in zin.infolist():
            data = zin.read(i.filename)
            if i.filename == CHECKPOINT_MANIFEST:
                _m = json.loads(data.decode('utf-8')); _m['paper_md5'] = None
                data = json.dumps(_m).encode('utf-8')
            zout.writestr(i, data)
    try:
        restore_checkpoint(_nb, os.path.join(tmp, 'ck_nb'), docx_path=_ck_paper)
        _t75d = False
    except CheckpointError as e:
        _t75d = 'paper_md5' in str(e)
    check('CK-unbindable-refused',
          _t75c and _t75d
          and not os.path.exists(os.path.join(tmp, 'ck_nb', 'audit_state.json')))

    # 76b. UNKNOWN SCHEMA IS REFUSED — a checkpoint written by a different
    #      framework build may carry fields this one misreads. Refusing is the
    #      only safe answer: half-understanding a resume state is how an audit
    #      certifies work it never did. (Uncovered until mutation testing showed
    #      the schema guard could be deleted with every other fixture still green.)
    _fut = os.path.join(tmp, 'ck_future.zip')
    with zipfile.ZipFile(_ck_zip) as zin, \
         zipfile.ZipFile(_fut, 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in zin.infolist():
            data = zin.read(i.filename)
            if i.filename == CHECKPOINT_MANIFEST:
                _m = json.loads(data.decode('utf-8'))
                _m['schema'] = CHECKPOINT_SCHEMA + 1
                data = json.dumps(_m).encode('utf-8')
            zout.writestr(i, data)
    try:
        restore_checkpoint(_fut, os.path.join(tmp, 'ck_f'), docx_path=_ck_paper)
        _t76b = False
    except CheckpointError as e:
        _t76b = 'schema' in str(e)
    check('CK-unknown-schema-refused',
          _t76b and not os.path.exists(os.path.join(tmp, 'ck_f', 'audit_state.json')))

    # 77. REFUSAL IS TOTAL — a rejected restore must leave NO partial state behind.
    #     A half-unpacked checkpoint is the worst outcome of all: it looks resumable.
    check('CK-refusal-leaves-nothing',
          not os.path.exists(os.path.join(tmp, 'ck_t', 'audit_state.json'))
          and not os.path.exists(os.path.join(tmp, 'ck_w', 'audit_state.json'))
          and not os.path.exists(os.path.join(tmp, 'ck_m', 'audit_state.json'))
          and not os.path.exists(os.path.join(tmp, 'ck_f', 'audit_state.json')))

    print(f'SELF-TEST: {passed}/{total} PASS' if passed == total
          else f'SELF-TEST: {passed}/{total} PASS  (FAILURES: {fails})')
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser(description='Universal exam-agnostic Part-A mock auditor')
    ap.add_argument('docx', nargs='?', help='the Mock[N]_Create.docx to audit')
    ap.add_argument('--blueprint'); ap.add_argument('--rules')
    ap.add_argument('--manifest');  ap.add_argument('--registry')
    ap.add_argument('--mockN', type=int)
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--audit-state', dest='audit_state',
                    help='Phase-3 COMPLETION GATE (S5-1A): validate the audit_state ledger '
                         '+ evidence artefacts (C1-C7). Use with --final.')
    ap.add_argument('--key', dest='key',
                    help='optional answer_key.json (concept_map) — normally NOT delivered (S0-1).')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    # C1 (v2.15) — cross-session checkpoint. /home/claude does not survive a
    # session boundary, so an audit that spans sessions must carry its ledger AND
    # its evidence with it or S5-1A C5/C6 can never certify.
    ap.add_argument('--make-checkpoint', dest='make_checkpoint',
                    help='write a portable checkpoint zip (needs --audit-state; '
                         'pass the docx to bind the bundle to this paper).')
    ap.add_argument('--restore-checkpoint', dest='restore_checkpoint',
                    help='verify + unpack a checkpoint zip (needs --into).')
    ap.add_argument('--into', dest='into',
                    help='destination directory for --restore-checkpoint.')
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if args.make_checkpoint:
        if not args.audit_state:
            ap.error('--make-checkpoint requires --audit-state')
        try:
            man = make_checkpoint(args.audit_state, args.make_checkpoint,
                                  docx_path=args.docx, mockN=args.mockN)
        except CheckpointError as e:
            print(f'CHECKPOINT: REFUSED — {e}'); sys.exit(1)
        print(f"CHECKPOINT: WRITTEN {os.path.basename(args.make_checkpoint)} "
              f"(mock {man.get('mock')}, batches {man.get('batches_done')}/"
              f"{man.get('K')}, {man.get('ledger_entries')} ledger entr(ies), "
              f"{man.get('evidence_files')} evidence file(s))")
        sys.exit(0)
    if args.restore_checkpoint:
        if not args.into:
            ap.error('--restore-checkpoint requires --into')
        try:
            man, stp, evd = restore_checkpoint(args.restore_checkpoint, args.into,
                                               docx_path=args.docx, mockN=args.mockN)
        except CheckpointError as e:
            print(f'CHECKPOINT: REFUSED — {e}'); sys.exit(1)
        print(f"CHECKPOINT: RESTORED (mock {man.get('mock')}, batches "
              f"{man.get('batches_done')}/{man.get('K')}, "
              f"{man.get('ledger_entries')} ledger entr(ies), "
              f"{man.get('evidence_files')} evidence file(s)) -> {stp}")
        sys.exit(0)
    if not args.docx:
        ap.error('docx path required (or use --self-test)')
    sys.exit(run_audit(args))


if __name__ == '__main__':
    main()
