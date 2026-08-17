#!/usr/bin/env python3
"""analyse_engine.py v1.0 — Step 5 (PYQExtract) shared extraction engine.

WHAT THIS IS. The §2 universal extraction primitives (E-1 .. E-11) and the §4 vision
aggregation helpers of Framework_MockTestAnalyse.md, moved here VERBATIM. The spec
retains every contract, edge case, DoD item and word of narrative; this file holds the
code. Same treatment §16 received at v2.39.2, when its implementation moved to
frequency_xlsx.py and its sections kept the contract.

WHY. Framework_MockTestAnalyse.md carried 6,667 lines of executable python that the
model READ INTO CONTEXT and then RE-EMITTED as code. Every other mature pipeline in
this repo — blueprint_core, corpus_io, notes_core, frequency_xlsx — puts that in an
engine that is imported and never read. Step 5 never got the treatment, and the cost was
not merely tokens:

  A model that re-emits code repairs it on the way past. GAP-2026-08-16-STEP5-SYNTHESIS-
  UNRUNNABLE found `collections` used in §5 and imported nowhere in the file, live for
  ten days; GAP-2026-08-16-BASELINE-SUPPRESSED-NAMEERRORS found process_pyq_paper()
  raising NameError on every paper of every exam. Both survived because each session
  silently supplied what the spec lacked, succeeded, and wrote nothing down. An engine
  that is imported cannot be repaired mid-flight. It fails once, loudly, in CI, and is
  fixed at source for all 200 exams at once.

HOW THE BOUNDARY WAS CHOSEN — not by section number, by the call graph. §2+§4 is the
subset that closes: it needs NOTHING from any other extractable section. §2+§3+§4 does
not close (§3's process_pyq_paper calls §5's tag_axes), and §3+§5+§6 needs 16 names from
§2. So §2+§4 ships first and §3+§5+§6 follows, each a set that can be asserted whole.

WHAT MOVED AND WHAT DID NOT. Every top-level node of the §2 and §4 python fences is a
DEFINITION — measured: 33 definitions, ZERO top-level session-flow statements. That is
why these fences could move intact rather than being picked apart. §1 (session start,
40 defs / 31 flow) and §8 (batch orchestration, 20 defs / 1 flow) carry the CLASS: T
tool calls and the session flow, and stay in the spec permanently.

CONTRACT. This module is IMPORTED AND EXECUTED, NEVER READ as part of a session's spec
budget (bootstrap.py verifies its checksum; SKILL Rule 2 does not route .py files).
Callers bind the 20 public names listed in __all__ via the import stubs that replaced
the fences. The 11 remaining names are engine-internal.

Stdlib + repo engines only. No I/O at import time.
"""
import re
import sys
from collections import Counter
from difflib import SequenceMatcher

import blueprint_core as bc      # Cluster H — pure acquisition/image decisions
import corpus_io                 # I/O shell — Drive fetch, image integrity, governor

# WHY THESE ARE DECLARED HERE AND WERE NOT FREE NAMES IN THE SPEC.
# In Framework_MockTestAnalyse.md the §1 fence imports bc / corpus_io / SequenceMatcher
# at module scope, and every later fence inherits them from the shared session
# namespace. A free-name analysis of §2+§4 ALONE therefore reports them as bound and
# says nothing is missing — which is exactly the shape of GAP-2026-08-16-STEP5-
# SYNTHESIS-UNRUNNABLE D2, where §5 used `collections` that no fence in the file ever
# imported and the defect hid for ten days behind the same inheritance.
# An engine has its own globals and inherits nothing. Every dependency is named here,
# at the top, where a reader and an auditor can both see it. That is the point of
# moving the code, not a side effect of it.

__all__ = [
    # §2 — universal extraction primitives (E-1 .. E-11)
    'detect_question_start', 'is_option', 'clean_option_text',
    'extract_and_map_images', 'enrich_paragraph_with_omml',
    'extract_note_block', 'classify_note_frequency', 'canonical_note_text',
    'detect_linked_groups', 'classify_option_format', 'subtopic_option_format',
    'score_difficulty', 'determine_strip_mode', 'generate_templates',
    'classify_wrong_option_structure',
    # §4 — vision aggregation
    'get_vision_candidates', 'apply_vision_observations', 'aggregate_figural',
    'VISION_PER_SHEET', 'VISION_WORKDIR',
]


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1624-1667 (v2.53.1) — VERBATIM ═══
Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1
    r'^Q(\d+)\.\s+',               # Q1.  Q25.
    r'^Q\.\s*(\d+)\s*$',           # Q.4   bare label — OMML / figure / empty stem
    r'^Q(\d+)\.\s*$',              # Q4.   bare label, alt form
]

# DELEGATED to the engine (blueprint_core Cluster G). Four specs parse Q-numbers from the
# same documents and must agree exactly; a local copy in any one of them is drift waiting to
# happen. This table mirrors the engine's canonical table EXACTLY and is verified by
# audit_deep.py TABLE-PARITY.
#
# WHY THESE FOUR AND NO MORE (2026-07-25, extended 2026-08-15).
#
# Entries 1-2 are the WITH-CONTENT forms. Three further forms exist in RAW exam sources —
# "Question 1:", bare "1." and "(1)" — and Step 1 detects them via its own
# SOURCE_Q_PATTERNS. They are deliberately ABSENT here and must never be restored. After
# Step 1 every document is NORMALISED: questions read "Q.N" and OPTIONS read "N. text".
# The bare-number pattern therefore matches every option line. Verified by execution on a
# canonical two-question fixture: the two-pattern table finds 2 question starts; the
# five-pattern table finds 10. A 100-question paper would parse as 500.
# Until 2026-07-25 these tables carried all five entries while the engine implemented two,
# and audit_deep TABLE-PARITY could not see it: its extraction regex stopped at the first
# ']', which occurs inside r'^Question\s+(\d+)\s*[:.]', so it compared a silently truncated
# two-entry slice against the engine's two and always passed.
#
# Entries 3-4 are the BARE-LABEL forms (GAP-2026-08-15-BAREQ). python-docx's p.text is
# <w:t>-only, so a stem paragraph whose entire payload is <m:oMath>, a drawing, or nothing
# at all (PYQPrepare S1-4 "empty/corrupt") reads as just "Q.N" — and entries 1-2 require
# whitespace AFTER the digits, applied to already-stripped text, so they can never match.
# Such a question DID NOT EXIST for this parser: its stem, its options and its date label
# were absorbed into the preceding question's body, and every check below passed because
# input and output are counted with the SAME blind detector. Measured on
# IIT_JAM_MATHEMATICS 12-Feb-2017: 4 of 60 questions (Q.4, Q.6, Q.25, Q.27) lost.
# This is the QUESTION half of GAP-2026-08-07-OMML, whose OPTION half shipped as
# corpus_io.BARE_OPT_PATTERNS + is_option(para=); OPT_PATTERNS had a bare-label companion
# and Q_PATTERNS did not.
# The $ anchor is LOAD-BEARING: it admits ONLY a paragraph that is nothing but the label,
# so it can never match an option line (options never begin with Q), an in-passage
# cross-reference "Q.11-15", a date label, a heading, or "Q1 Analysis". Verified by
# execution over a 34-case adversarial fixture in blueprint_core.self_test().
detect_question_start = bc.detect_question_start


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1671-1688 (v2.53.1) — VERBATIM ═══
# ── OPTION PREDICATE — DELEGATED (v2.36, audit_deep [XSPEC-DRIFT]) ────────────
# is_option() was defined in THREE specs (here, PYQSort, PYQAnalyse), each with a
# docstring claiming alignment with the others. v2.34/v2.35 added the image-option
# path HERE only, so those claims became false and PYQSort — which uses the predicate
# to COUNT options — kept undercounting image options. Measured on
# IIT_JAM_BIOTECHNOLOGY 2022: 156 options counted, 160 actual.
# corpus_io now owns the single definition. Do NOT re-localise any of these names.
OPT_PATTERNS      = corpus_io.OPT_PATTERNS
BARE_OPT_PATTERNS = corpus_io.BARE_OPT_PATTERNS
para_has_image    = corpus_io.para_has_image
is_option         = corpus_io.is_option
clean_option_text = corpus_io.clean_option_text

# After collecting options per Q: options = options[:options_count]
# If still < options_count: try E-5 OMML and E-4 image check.
# If still missing: q_incomplete=True, exclude from template extraction.


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1692-1767 (v2.53.1) — VERBATIM ═══
from docx import Document
import os

def extract_and_map_images(doc, paper_id, docx_path, expected_size=None):
    """
    BUG-A03 fix: accepts already-opened Document object, not doc_path.
    Caller (S3-1) opens Document once and passes it here.

    v2.34 — SINGLE GATED PATH. The legacy DOM-only branch is DELETED and docx_path is
    now a REQUIRED POSITIONAL. GAP-2026-07-26-002 DEFECT-1/2/3/5:

      * DEFECT-1. docx_path was optional and the ONLY call site in the entire framework
        (S3-1) never passed it, so `if docx_path:` was always False and every Step-5 run
        on every exam silently took the branch this file itself labelled UNGATED. The
        docstring documented a requirement nothing satisfied. A fallback that no caller
        ever avoids is not a safety net — it IS the default path.
      * DEFECT-2. The two branches returned THREE values each in DIFFERENT orders with
        DIFFERENT meanings — (img_map, imap, q_roles) vs (imap, q_roles, report). Equal
        arity means the interpreter raises nothing; the unpack simply mis-binds and
        q_roles becomes the report dict, so every .get(num,{}).get('role') returns the
        'none' default. There is now ONE return shape: (image_map, q_roles, report).
      * DEFECT-3. The gated branch built {'stem','opts'} but never derived 'role', the
        documented contract read by S3-1 (image_role) and S4-1 (get_vision_candidates).
        Role derivation is DELEGATED to bc.derive_image_roles() so one rule exists in
        one place — the same contract audit_deep.py enforces for detect_question_start.
      * DEFECT-5. expected_size was captured by enumeration and threaded nowhere, so
        IMG-1 evaluated against None and SKIPped on every paper, permanently. It is the
        only check that catches a payload truncated at a ZIP member boundary.

    Measured on the 22-paper IIT_JAM_BIOTECHNOLOGY corpus: this path maps the identical
    329 images the legacy walk did (that corpus carries no table/VML/header images —
    Step 1 normalisation removes them), but assigns the CORRECT role to the image-option
    questions the legacy walk mis-typed as stem_only. All 22 papers PASS IMG-1..IMG-5;
    zero hard stops.

    docx_path is required: the gates read the PACKAGE, not the DOM.
    """
    img_dir = f'/home/claude/pyq_images/{paper_id}'
    extracted = corpus_io.extract_images(docx_path, img_dir)
    mapping   = corpus_io.map_images_to_questions(docx_path)
    verdicts, stats = corpus_io.verify_images(
        docx_path, extracted=extracted, mapping=mapping,
        expected_size=expected_size, workdir=img_dir)

    if not bc.gates_passed(verdicts):
        failed = {k: v for k, v in verdicts.items() if not str(v).startswith(('PASS', 'SKIP'))}
        raise SystemExit(
            f"HARD STOP — image integrity gate failed for {paper_id}:\n  "
            + "\n  ".join(f"{k}: {v}" for k, v in failed.items())
            + "\n\nAn image that is present in the document but missing from the "
              "mapping becomes a question classified TEXT instead of FIGURAL, which "
              "silently corrupts the format distribution used by Step 7. Resolve the "
              "document before continuing; do not process it partially.")

    if stats['preamble']:
        print(f"    note: {stats['preamble']} image(s) before Q.1 (not question figures)")
    if stats['header_footer']:
        print(f"    note: {stats['header_footer']} header/footer image(s) (not question figures)")
    if stats['vector']:
        print(f"    note: {stats['vector']} vector part(s) — rasterised before view()")

    image_map = []
    for q_num, parts in mapping.items():
        if q_num == corpus_io.PREAMBLE:
            continue
        for i, base in enumerate(parts):
            rec = extracted.get(base, {})
            image_map.append({'img_idx': i, 'q_num': q_num,
                              'position': 'stem' if i == 0 else f'opt{i}',
                              'path': rec.get('path'), 'kind': rec.get('kind')})

    # DEFECT-3: ONE role rule, owned by the engine. Never re-implement inline.
    q_roles = bc.derive_image_roles(image_map)
    return image_map, q_roles, {'verdicts': verdicts, 'stats': stats}


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1777-1824 (v2.53.1) — VERBATIM ═══
MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

def omml_to_linear(omath_elem):
    def recurse(el):
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag == 'r':
            t = el.find(f'{{{MATH_NS}}}t')
            return (t.text or '') if t is not None else ''
        elif tag == 'f':
            n = el.find(f'{{{MATH_NS}}}num'); d = el.find(f'{{{MATH_NS}}}den')
            return f'({recurse(n)})/({recurse(d)})' if n is not None and d is not None else '?/?'
        elif tag == 'sSup':
            b = el.find(f'{{{MATH_NS}}}e'); s = el.find(f'{{{MATH_NS}}}sup')
            return f'{recurse(b)}^{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'sSub':
            b = el.find(f'{{{MATH_NS}}}e'); s = el.find(f'{{{MATH_NS}}}sub')
            return f'{recurse(b)}_{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'rad':
            d = el.find(f'{{{MATH_NS}}}deg'); b = el.find(f'{{{MATH_NS}}}e')
            btext = recurse(b) if b is not None else '?'
            return f'root({d.text},{btext})' if d is not None and d.text else f'sqrt({btext})'
        else:
            return ''.join(recurse(c) for c in el)
    try:    return recurse(omath_elem).strip()
    except: return '[OMML_FAILED]'

def enrich_paragraph_with_omml(stem_text, paragraph):
    """
    Find all OMML nodes in paragraph, convert to linear text.
    BUG-A05 fix: all_ok starts True and is AND-reduced (not last-write-wins).
    Returns: (enriched_text, all_ok, has_omml)
    Failed OMML nodes are skipped (not appended) to avoid polluting templates.
    """
    additions = []
    all_ok    = True   # True = every OMML node in this paragraph converted OK
    for elem in paragraph._p.iter():
        if elem.tag == f'{{{MATH_NS}}}oMath':
            linear = omml_to_linear(elem)
            if '[OMML_FAILED]' in linear:
                all_ok = False          # propagate failure via AND
                # do NOT append failed output to stem
            else:
                additions.append(linear)
    has_omml = bool(additions) or not all_ok
    enriched = stem_text + (' ' + ' '.join(additions) if additions else '')
    return enriched.strip(), all_ok, has_omml


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1828-1877 (v2.53.1) — VERBATIM ═══
# BUG-A14-related (Unicode): NOTE_PAT is a non-raw string so \u escapes ARE processed.
# v2.16 RIGID-6: expanded from English+Hindi to ALL major Indic scripts.
# Regional exams (Tamil Nadu PSC, AP/TS PSC, WBPSC, KPSC, etc.) use NOTE blocks
# in their respective scripts. Missing these would lose instruction metadata.
NOTE_PAT = re.compile(
    '\\((?:NOTE|Note|INSTRUCTION|Important|Caution'
    '|\u0928\u094b\u091f'           # Hindi/Marathi (Devanagari): नोट
    '|\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923'  # Hindi: महत्वपूर्ण
    '|\u0b95\u0bc1\u0bb1\u0bbf\u0baa\u0bcd\u0baa\u0bc1'              # Tamil: குறிப்பு
    '|\u0c17\u0c2e\u0c28\u0c3f\u0c15'                                # Telugu: గమనిక
    '|\u09a6\u09cd\u09b0\u09b7\u09cd\u099f\u09ac\u09cd\u09af'       # Bengali: দ্রষ্টব্য
    '|\u0c9f\u0cbf\u0caa\u0ccd\u0caa\u0ca3\u0cbf'                   # Kannada: ಟಿಪ್ಪಣಿ
    '|\u0d15\u0d41\u0d31\u0d3f\u0d2a\u0d4d\u0d2a\u0d4d'             # Malayalam: കുറിപ്പ്
    '|\u0a28\u0a4b\u0a1f'                                            # Punjabi (Gurmukhi): ਨੋਟ
    '|\u0aa8\u0acb\u0a82\u0aa7'                                      # Gujarati: નોંધ
    '|\u0b1f\u0b3f\u0b2a\u0b4d\u0b2a\u0b23\u0b40'                   # Odia: ଟିପ୍ପଣୀ
    ')[^)]{10,}\\)',
    re.DOTALL
)

def extract_note_block(stem_text):
    """Return (clean_stem, note_text, found)."""
    m = NOTE_PAT.search(stem_text)
    if m:
        note    = m.group(0)
        cleaned = (stem_text[:m.start()] + ' ' + stem_text[m.end():]).strip()
        return cleaned, note, True
    return stem_text, '', False

def classify_note_frequency(note_count, total):
    """mandatory >=80% | conditional 20-79% | rare 1-19% | never 0%"""
    if total == 0: return 'never'
    pct = note_count / total * 100
    if pct >= 80: return 'mandatory'
    if pct >= 20: return 'conditional'
    if pct >= 1:  return 'rare'
    return 'never'

def canonical_note_text(notes_by_year):
    """Most common NOTE text from most recent year. Skips None keys."""
    if not notes_by_year: return ''
    int_years = {k: v for k, v in notes_by_year.items() if isinstance(k, int)}
    if int_years:
        recent = max(int_years.keys())
        texts  = int_years[recent]
    else:
        texts  = list(notes_by_year.values())[0] if notes_by_year else []
    return Counter(texts).most_common(1)[0][0] if texts else ''


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1881-1929 (v2.53.1) — VERBATIM ═══
def detect_linked_groups(questions):
    """
    Method 1: reprinted stimulus — verbatim match >=90% (Cloze, DI, Reading Comprehension etc.).
    Method 2: proximity stimulus (non-reprinted passage) applied during extraction
              (long para before run of short-stem Qs — used in CAT, UPSC, CLAT etc.).
    """
    groups, visited = [], set()

    for i, q in enumerate(questions):
        if q['num'] in visited: continue
        visited.add(q['num'])   # mark lead question immediately to prevent re-processing
        stim_q = extract_stimulus(q['stem'])
        if not stim_q: continue
        members = [q['num']]

        for j in range(i+1, min(i+8, len(questions))):
            nq = questions[j]
            if nq['num'] in visited: break
            stim_nq = extract_stimulus(nq['stem'])
            if not stim_nq: break
            if SequenceMatcher(None, stim_q, stim_nq).ratio() >= 0.90:
                members.append(nq['num']); visited.add(nq['num'])
            else:
                break

        if len(members) > 1:
            groups.append({'group_id'      : f'G{len(groups)+1}',
                           'q_numbers'     : members,
                           'stimulus_text' : stim_q,
                           'stimulus_type' : classify_stimulus(stim_q),
                           'word_count'    : len(stim_q.split())})
            visited.update(members)

    return groups

def extract_stimulus(stem):
    """Extract shared stimulus portion (content before question ask)."""
    m = re.search(r'\b(Select|Find|Which|Who|What|How|Identify|Choose)\b', stem)
    if m and m.start() > 100: return stem[:m.start()].strip()
    return stem if len(stem.split()) > 50 else ''

def classify_stimulus(text):
    t = text.lower()
    if '|' in text or 'table' in t: return 'table'
    if any(kw in t for kw in ['clue','sitting','puzzle','arrangement']): return 'puzzle'
    if 'code' in t and 'means' in t: return 'code'
    return 'passage'


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L1933-2017 (v2.53.1) — VERBATIM ═══
def classify_option_format(opts):
    """
    BUG-A23 fix: en-dash U+2013 matched via actual Unicode char (non-raw string).
    BUG-A12 / BUG-B19 fix: empty opts handled before any index access.
    12 types: single_value, value_pair, coordinate_pair, letter_cluster, code_pair,
              sentence, label_only, segment_label, roman_label, image_only,
              value_pair_quad, word_form_number
    """
    cleaned = [o.strip() for o in opts if isinstance(o, str)]
    if not cleaned or all(o == '' for o in cleaned): return 'image_only'

    wnums = {'one','two','three','four','five','six','seven','eight','nine','ten',
             'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen',
             'eighteen','nineteen','twenty'}
    if all(o.lower() in wnums for o in cleaned if o): return 'word_form_number'
    if all(o.lower() in {'i','ii','iii','iv','v','vi'} for o in cleaned if o):
        return 'roman_label'
    if all(len(o)==1 and o.upper() in 'ABCD' for o in cleaned if o):
        return 'segment_label'

    sent_kw = {'only','both','follow','follows','correct','neither','none'}
    if any(any(kw in o.lower() for kw in sent_kw) for o in cleaned if o):
        return 'sentence' if any(len(o.split()) > 3 for o in cleaned if o) else 'label_only'

    if all(re.match(r'^[A-D]-\d+(?:,\s*[A-D]-\d+)*$', o) for o in cleaned if o):
        return 'value_pair_quad'
    if all(re.match(r'^\(\d+,\s*\d+\)$', o) for o in cleaned if o):
        return 'coordinate_pair'

    # BUG-A23 fix: actual en-dash U+2013 embedded as literal character in raw string.
    # Cannot use \u2013 in raw string (r-prefix disables escapes).
    # Instead: compile pattern with en-dash as literal char (avoids SyntaxWarning).
    _VALUE_PAIR_PAT = re.compile(r'\d+\s*[-–]\s*\d+$')
    if all(_VALUE_PAIR_PAT.match(o) for o in cleaned if o):
        return 'value_pair'

    if all(re.match(r'^[A-Z]{2,6}$', o) for o in cleaned if o):
        return 'letter_cluster'
    if all('\u2192' in o or (' - ' in o and bool(re.search(r'[A-Z]{3,}', o)))
           for o in cleaned if o):
        return 'code_pair'
    return 'single_value'

def subtopic_option_format(qs):
    """
    BUG-A12 fix: guard for empty qs list (years[-1] IndexError).
    """
    if not qs:
        return {'primary':'single_value','recent_format':'single_value',
                'changed_recently':False,'all_observed':[]}
    fmts = [classify_option_format(q.get('options', [])) for q in qs]
    by_year = {}
    for q, fmt in zip(qs, fmts):
        by_year.setdefault(q.get('year', '?'), []).append(fmt)
    primary = Counter(fmts).most_common(1)[0][0]
    years   = sorted(by_year.keys())
    # GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D4) — ARTEFACT NONDETERMINISM.
    # `all_observed` was list(set(fmts)). Set iteration order for str elements
    # depends on PYTHONHASHSEED, which python randomises PER PROCESS, so this list
    # came out in a different order on every run. It is emitted verbatim by
    # write_section_rules as `option_format_all_observed:` (§14), which means TWO
    # runs of identical code over an identical corpus produced two different
    # section_rules.md files — measured: same 433,260 bytes, different sha256,
    # differing at 34 lines, one per subtopic.
    #
    # CONSEQUENCE: no Step 5 artefact was ever reproducible, so no diff between two
    # runs could distinguish a real regression from hash-seed noise, and any
    # byte-identity gate over this pipeline was impossible to build. That is why
    # this is fixed HERE, in the release that establishes the Wave 2 Part C
    # regression floor, rather than deferred: without it the floor cannot exist.
    #
    # WHY IT HID: a single process reuses one seed, so back-to-back runs inside one
    # session agree with each other and look deterministic. Only a fresh process
    # disagrees — and every real run is a fresh process.
    #
    # sorted() not list(): a stable, explicit, reviewable order.
    if not years:
        return {'primary':primary,'recent_format':primary,
                'changed_recently':False,'all_observed':sorted(set(fmts))}
    recent = Counter(by_year.get(years[-1], [])).most_common(1)
    rfmt   = recent[0][0] if recent else primary
    return {'primary':primary,'recent_format':rfmt,
            'changed_recently':rfmt != primary,'all_observed':sorted(set(fmts))}


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L2027-2039 (v2.53.1) — VERBATIM ═══
def score_difficulty(q, marks=1, strip_mode='reasoning'):
    """v2.30 — DELEGATED to blueprint_core Cluster E (GAP-2026-07-25-002).
    This spec carried a byte-identical second copy of the engine's implementation.
    Identical TODAY is not a mechanism for staying identical: the corpus has already
    paid for that assumption once (PYQAnalyse v2.20, parse_taxonomy_level drifting
    from Step 5's copy despite a comment in each demanding they match). One
    definition, called from both places."""
    import blueprint_core as bc      # local: this code block does not share the
                                     # module-level alias bound in the S1-1 block
    return bc.score_difficulty(q, marks=marks, strip_mode=strip_mode)



# ═══ FROM Framework_MockTestAnalyse.md §2, fence L2047-2171 (v2.53.1) — VERBATIM ═══
def determine_strip_mode(section, topic, subtopic):
    """v2.30 — DELEGATED to blueprint_core Cluster E (GAP-2026-07-25-002).
    Second copy removed; see score_difficulty above. The engine's version carries the
    v2.16 RIGID-5 Devanagari terms, so delegating also means a Hindi-medium exam is
    classified by the same table everywhere rather than by whichever copy ran."""
    import blueprint_core as bc      # local: see score_difficulty above
    return bc.determine_strip_mode(section, topic, subtopic)

def strip_variables(stem, mode):
    """
    Strip variable parts from stem to produce structural skeleton.
    BUG-A14 fix: currency pattern uses non-raw string with actual \u20b9 (₹),
                 so the Unicode escape IS processed correctly.
    BUG-B10 fix: logical mode preserves trailing punctuation.
    """
    t = stem
    if mode == 'quantitative':
        t = re.sub('\u20b9\\s*[\\d,]+(?:\\.\\d+)?', '\u20b9_P_', t)  # ₹ currency
        t = re.sub(r'\d+(?:\.\d+)?%', '_R_%', t)
        t = re.sub(r'\b\d+\s*(?:years?|months?|days?|hours?|weeks?)\b',
                   '_T_', t, flags=re.IGNORECASE)
        t = re.sub(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', '_NUM_', t)
        t = re.sub(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', '_NAME_', t)
    elif mode == 'reasoning':
        t = re.sub(r'\b[A-Z]{3,}\b', '_WORD_', t)
        t = re.sub(r'\b[A-Z]{2,4}(?:\s*:\s*[A-Z]{2,4})+\b', '_LCLUS_:_LCLUS_', t)
        t = re.sub(r'\b\d+(?:,\s*\d+){2,}\b', '_SERIES_', t)
        t = re.sub(r'\b\d+\b', '_NUM_', t)
    elif mode == 'factual':
        t = re.sub(r'\b(19|20)\d{2}\b', '_YEAR_', t)
        t = re.sub(r'\b\d+(?:st|nd|rd|th)?\b', '_NUM_', t)
    elif mode == 'english':
        t = re.sub(r'_{3,}', '_BLANK_', t)
    elif mode == 'logical':
        # BUG-B10 fix: strip trailing punctuation separately, restore after
        quantifiers = {'All','all','Some','some','No','no','None','none',
                       'are','is','can','never','be','being'}
        words  = t.split()
        result = []
        for w in words:
            w_clean  = w.rstrip('.,;:!?')
            trailing = w[len(w_clean):]
            if w_clean in quantifiers or not (w_clean and w_clean[0].isupper()):
                result.append(w)
            else:
                result.append('_NOUN_' + trailing)
        t = ' '.join(result)
    t = re.sub(r'^Q\.?\d+\.?\s*', '', t)
    t = re.sub(r'\[\d{1,2}-\w+-\d{4}[^\]]*\]', '', t)
    return t.strip()

def generate_templates(questions, strip_mode):
    """
    BUG-A04 fix: SequenceMatcher imported at module top (§1 S1-1).
    BUG-A13 fix: empty skeletons returns [] — caller handles this case.
    BUG-A20 fix: deprecated flag added to each pattern dict.
    """
    if not questions: return []

    years = sorted(set(q.get('year', 2020) for q in questions))
    last2 = set(years[-2:]) if len(years) >= 2 else set(years)

    skeletons = []
    for q in questions:
        if not q.get('stem'): continue
        skel = strip_variables(q['stem'], strip_mode)
        if not skel.strip(): continue
        weight = 2 if q.get('year') in last2 else 1
        skeletons.append({'skel':skel, 'weight':weight, 'year':q.get('year', 2020)})

    if not skeletons: return []

    clusters = []
    for item in skeletons:
        placed = False
        for c in clusters:
            if SequenceMatcher(None, c[0]['skel'], item['skel']).ratio() >= 0.90:
                c.append(item); placed = True; break
        if not placed: clusters.append([item])

    total_w  = sum(s['weight'] for s in skeletons) or 1
    pats_raw = sorted([{
        'skel'     : c[0]['skel'],
        'w_count'  : sum(i['weight'] for i in c),
        'raw_count': len(c),
        'years'    : sorted(set(i['year'] for i in c)),
    } for c in clusters], key=lambda p: -p['w_count'])

    for p in pats_raw:
        p['raw_pct']   = p['w_count'] / total_w * 100
        p['frequency'] = int(p['raw_pct'])
    deficit = 100 - sum(p['frequency'] for p in pats_raw)
    if deficit > 0:
        for p in sorted(pats_raw, key=lambda p: -(p['raw_pct']-p['frequency']))[:deficit]:
            p['frequency'] += 1

    result = []
    for i, p in enumerate(pats_raw, 1):
        conf = 'observed' if p['raw_count'] >= 3 else 'inferred'
        if p['years'] and all(y in last2 for y in p['years']) and len(p['years']) <= 2:
            conf = 'observed_recent'
        # BUG-A20 fix: deprecated flag for patterns absent from last 2 years
        deprecated = bool(p['years'] and not any(y in last2 for y in p['years']))
        result.append({
            'id'        : f'P{i}',
            'template'  : p['skel'],
            'frequency' : p['frequency'],
            'raw_count' : p['raw_count'],
            'confidence': conf,
            'deprecated': deprecated,
            'years'     : p['years'],
        })
    # Filter out patterns with frequency=0 (can occur for very rare templates
    # when raw_pct < 0.5% and largest-remainder does not assign them +1).
    # Such templates would appear in section_rules.md but never be selected by Step 7.
    result = [p for p in result if p['frequency'] >= 1]
    # Re-normalize if any were removed (ensure sum still = 100)
    if result:
        total_freq = sum(p['frequency'] for p in result)
        if total_freq != 100:
            # Add deficit to highest-frequency pattern (always the first after DESC sort)
            result[0]['frequency'] += (100 - total_freq)
    return result


# ═══ FROM Framework_MockTestAnalyse.md §2, fence L2182-2260 (v2.53.1) — VERBATIM ═══
def classify_wrong_option_structure(subtopic_qs):
    """
    BUG-A08 fix: image-only check before fixed_set detection.
    BUG-A24 fix: empty strings filtered from shared_pool counter.
    BUG-B12 fix: image_only added to DESC dict (11th type).
    """
    all_opt_sets = [q['options'] for q in subtopic_qs if q.get('options')]
    if not all_opt_sets:
        return {'type':'varied','description':'No options to classify'}

    # BUG-A08 fix: detect image-only before entering fixed_set logic
    if all(o.strip() == '' for opts in all_opt_sets for o in opts):
        return {'type':'image_only',
                'description':'All options are images — option text is blank.'}

    frozen  = [frozenset(o.strip().lower() for o in s) for s in all_opt_sets]
    top_s, ct = Counter(frozen).most_common(1)[0]
    if ct / len(frozen) >= 0.80:
        canon = next(s for s in all_opt_sets
                     if frozenset(o.strip().lower() for o in s) == top_s)
        return {'type':'fixed_set',
                'description':'Identical options every question of this type.',
                'fixed_option_texts':[o.strip() for o in canon]}

    # BUG-A24 fix: filter empty strings from shared_pool counter
    all_words = Counter(o.strip().lower() for s in all_opt_sets for o in s if o.strip())
    top4      = [w for w, _ in all_words.most_common(4)]
    coverage  = sum(1 for s in all_opt_sets if any(o.strip().lower() in top4 for o in s))
    if top4 and coverage / len(all_opt_sets) >= 0.50 and len(all_words) < 8:
        return {'type':'shared_pool',
                'description':'Same word pool rotated as options across linked questions.',
                'shared_pool_words':top4}

    votes = Counter(_classify_one_set([o.strip() for o in s if o.strip()])
                    for s in all_opt_sets)
    dom   = votes.most_common(1)[0][0]
    # BUG-B12 fix: image_only added as 11th type in DESC
    DESC  = {
        'adjacent_values': 'Numeric options within +-20% — near-miss calculations.',
        'anagram'        : 'Options are character rearrangements of each other.',
        'alliterative'   : '3+ options share first letter — deliberate distractor.',
        'same_category'  : 'All options are real entities of the same class.',
        'sentence_label' : '"Only I follows" / "Both II and III follow" style.',
        'segment_label'  : 'Options are A/B/C/D referring to labelled stem segments.',
        'roman_label'    : 'Options are i/ii/iii/iv referring to numbered sub-items.',
        'value_pair_quad': 'Matching combinations: A-1, B-2, C-3, D-4.',
        'word_form'      : 'Options are number word forms: One/Two/Three/Four.',
        'image_only'     : 'All options are images — option text is blank.',
        'varied'         : 'No consistent structural pattern detected.',
    }
    return {'type':dom, 'description':DESC.get(dom, 'Pattern detected.')}

def _classify_one_set(opts):
    if not opts: return 'varied'
    if set(o.upper() for o in opts) == {'A','B','C','D'} and all(len(o)==1 for o in opts):
        return 'segment_label'
    if all(o.lower() in {'i','ii','iii','iv','v','vi'} for o in opts): return 'roman_label'
    wn = {'one','two','three','four','five','six','seven','eight','nine','ten'}
    if all(o.lower() in wn for o in opts): return 'word_form'
    kw = {'only','both','follow','correct','neither'}
    if any(any(k in o.lower() for k in kw) for o in opts): return 'sentence_label'
    csets = [Counter(o.upper().replace(' ','')) for o in opts]
    if len(set(frozenset(c.items()) for c in csets)) == 1 and len(opts[0]) <= 6:
        return 'anagram'
    fl = [o[0].upper() for o in opts if o]
    # Guard for empty fl (all opts were empty after filtering)
    most_fl = Counter(fl).most_common(1)
    if most_fl and most_fl[0][1] >= 3: return 'alliterative'
    nums = []
    for o in opts:
        try: nums.append(float(re.sub('[,\u20b9%\\s]', '', o)))
        except: pass
    if len(nums) == len(opts) and nums and max(nums) / max(min(nums), 0.001) <= 1.4:
        return 'adjacent_values'
    cap = sum(1 for o in opts if o and o[0].isupper() and not any(c.isdigit() for c in o))
    if cap >= 3: return 'same_category'
    return 'varied'


# ═══ FROM Framework_MockTestAnalyse.md §4, fence L2875-2919 (v2.53.1) — VERBATIM ═══
def get_vision_candidates(questions, q_roles, imap):
    """
    Returns list of (q, [image_path, ...]) pairs requiring vision analysis.
    Only questions where the image is in the stem (or stem+options).
    options_only: E-11 classifies those from text patterns, no vision needed.
    Text-extractable subtopics (dice, cube, counting shapes etc.): values
    already present in stem text — vision adds nothing for these.
    imap: image mapping list from extract_and_map_images() — passed explicitly.

    EC-V6 (GAP-2026-07-26-003). ALL of a question's stem images are returned, not
    just the first. A 4-panel series is ONE question whose rule can only be read
    across the panels; handing the queue panel 1 alone and asking for the
    transformation guaranteed either a wrong answer or an unreadable verdict. The
    panels are composed into a single cell so they are judged together (S4-2a).
    """
    candidates = []
    # SKIP_TEXT_EXTRACTABLE: subtopics where the image contains countable/readable
    # values already present as text in the stem — vision adds no information.
    # Detected by checking if stem contains numeric/face values AND subtopic name
    # suggests a counting/identification task (dice, cube, counting shapes, etc.).
    # This list is NOT hardcoded — it is inferred from subtopic name keywords.
    SKIP_KEYWORDS = {'dice', 'cube', 'count', 'counting', 'dots', 'faces', 'nets'}

    for q in questions:
        role = q_roles.get(q['num'], {}).get('role', 'none')

        if role not in ('stem_only', 'stem_and_options'):
            continue   # options_only or none: no stem image, skip

        sub_lower = q.get('subtopic', '').lower()
        if any(kw in sub_lower for kw in SKIP_KEYWORDS):
            continue   # stem already has the values; vision not needed

        # Get the path(s) of stem images for this Q (imap passed from E-4), in
        # document order — the series order IS the question's meaning.
        stem_imgs = [entry for entry in imap
                     if entry['q_num'] == q['num']
                     and entry['position'] == 'stem']
        paths = [e['path'] for e in stem_imgs if e.get('path')]
        if paths:
            candidates.append((q, paths))

    return candidates


# ═══ FROM Framework_MockTestAnalyse.md §4, fence L2957-2964 (v2.53.1) — VERBATIM ═══
# Where the queue and its sheets live. One directory per run, NOT per paper: a
# batch's sheets are viewed together in Phase B, and EC-V15 keys every item by
# (paper_id, q_num) so one shared queue cannot confuse two papers.
VISION_WORKDIR   = '/home/claude/pyq_vision'
VISION_PER_SHEET = 6      # 153 figures -> 26 view() calls instead of 153.
                          # A parameter, not a constant of nature: re-tile freely.


# ═══ FROM Framework_MockTestAnalyse.md §4, fence L3024-3064 (v2.53.1) — VERBATIM ═══
def apply_vision_observations(progress, workdir=VISION_WORKDIR):
    """Fold Phase-B observations onto the questions. THE ONLY WRITER of image_clarity.

    Returns the merge stats dict. NEVER raises, NEVER halts: a missing or malformed
    observations file is the ordinary 'Phase B has not run' state and must flow
    through as zero observations so the run completes and QV-14 reports the gap.

    Idempotent (EC-V12): running it twice on the same inputs yields the same fields.
    """
    queue, why = corpus_io.load_vision_queue(workdir)
    if queue is None:
        print(f"    PHASE C: {why} — no figural vision data this run")
        return {'queued': 0, 'observed': 0, 'missing': 0, 'unreadable': 0,
                'unknown': [], 'duplicate': [], 'vision_status': 'not_applicable'}

    observations, why = corpus_io.load_vision_observations(workdir)
    if why:
        print(f"    PHASE C: {why}")

    by_key, stats = bc.merge_vision_observations(queue['items'], observations)

    # Stamp the fields onto the live question dicts, keyed (paper_id, q_num) — EC-V15.
    for key, entries in progress.items():
        if not isinstance(key, tuple):
            continue
        for q in entries:
            rec = by_key.get((str(q.get('paper_id')), q.get('q_num')))
            if rec:
                q.update({'object_type'   : rec['object_type'],
                          'transformation': rec['transformation_type'],
                          'arrangement'   : rec['arrangement'],
                          'complexity'    : rec['complexity'],
                          'image_clarity' : rec['image_clarity']})

    print(f"    PHASE C: {stats['observed']}/{stats['queued']} figure(s) observed "
          f"({stats['vision_status']})"
          + (f", {stats['unreadable']} illegible" if stats['unreadable'] else '')
          + (f", {len(stats['unknown'])} unknown tag(s) ignored" if stats['unknown'] else ''))
    return stats


# ═══ FROM Framework_MockTestAnalyse.md §4, fence L3086-3132 (v2.53.1) — VERBATIM ═══
def aggregate_figural(questions_for_subtopic, q_roles=None):
    """
    Called during synthesis (§5) for FIGURAL subtopics.

    v2.37 (GAP-2026-07-26-003). The aggregation itself is DELEGATED to
    bc.vision_profile(). It used to be re-implemented here as a plain top-3 over
    object_type, which had two defects:

      * it named a dominant type from ANY number of observations. Two figures cannot
        support a claim about what a subtopic "typically" looks like, and Step 7
        generates against that claim (EC-V20).
      * it named a dominant type even when the distribution was FLAT. Six figures of
        six DIFFERENT types produced a "dominant" list of the alphabetically-first
        three — handing the generator a fixation the evidence did not support. Caught
        by end-to-end test, not by inspection (EC-V26).

    One aggregation rule, in the engine, unit-tested. Never re-implement it here.

    image_role stays local: it is derived from q['image_role'] (stored per question in
    S3-1) rather than from q_roles, which is NOT persisted in progress.json across
    sessions. q_roles is retained for backward compatibility and is unused.
    """
    from collections import Counter

    # Dominant image_role from q['image_role'] stored in each question dict during S3-1.
    roles = [q.get('image_role', 'none') for q in questions_for_subtopic
             if q.get('image_role', 'none') != 'none']
    dominant_role = Counter(roles).most_common(1)[0][0] if roles else 'stem_only'

    # Only questions that actually carry a figure enter the vision denominator.
    # EC-V13/EC-V14: a zero-PYQ inferred FIGURAL subtopic and an INHERENTLY-VISUAL
    # keyword override are legitimately FIGURAL with no embedded figure, so they
    # contribute no records and are excluded from QV-14 by construction.
    figural = [q for q in questions_for_subtopic
               if q.get('image_role', 'none') != 'none']

    prof = bc.vision_profile([
        {'image_clarity'      : q.get('image_clarity', 'vision_unavailable'),
         'object_type'        : q.get('object_type'),
         'transformation_type': q.get('transformation'),
         'arrangement'        : q.get('arrangement'),
         'complexity'         : q.get('complexity')}
        for q in figural])
    prof['image_role'] = dominant_role
    return prof



# ────────────────────────────────────────────────────────────── self-test
def self_test():
    """python3 analyse_engine.py --self-test

    Every assertion below pins a behaviour some caller in Framework_MockTestAnalyse.md
    depends on. A fixture that merely restates the implementation proves nothing, so
    each one names a real input shape and the answer the pipeline needs.
    """
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    # ── E-1 question-start detection ──────────────────────────────────────
    # Returns the question NUMBER, not a bool. Q_PATTERNS accepts ONLY `Q.N` and
    # `QN.` forms; a bare `1.` is deliberately NOT a question start, which is what
    # stops an ordinary numbered list inside a stem from splitting the paper.
    check('qstart_Q.1', detect_question_start('Q.1 What is x?') == 1)
    check('qstart_Q.10_two_digits', detect_question_start('Q.10') == 10)
    check('qstart_Q1.', detect_question_start('Q1.') == 1)
    for s_ in ('1. What is x?', '12.', '(1) x', 'Q 1 What is x?'):
        check(f'qstart_rejects_non_Q_form[{s_!r}]', detect_question_start(s_) is None)
    check('qstart_rejects_mid_sentence',
          detect_question_start('The value of Q.1 is') is None)
    check('qstart_empty_is_safe', detect_question_start('') is None)

    # ── E-2 option recognition ────────────────────────────────────────────
    for s_ in ('(A) first', 'A. first', '(a) first'):
        check(f'is_option[{s_!r}]', bool(is_option(s_)))
    for s_ in ('A group of students', ''):
        check(f'not_option[{s_!r}]', not is_option(s_))
    check('clean_option_text_strips_label', clean_option_text('(A) 42').strip() == '42')

    # ── E-8 option-format classification (12 types) ───────────────────────
    # Options arrive LABEL-FREE here; the (A)/(B) prefix is stripped upstream.
    SHAPES = {
        'single_value':     ['1', '2', '3', '4'],
        'coordinate_pair':  ['(1, 2)', '(3, 4)', '(5, 6)', '(7, 8)'],
        'image_only':       ['', '', '', ''],
        'word_form_number': ['one', 'two', 'three', 'four'],
        'roman_label':      ['i', 'ii', 'iii', 'iv'],
        'value_pair':       ['1-2', '3-4', '5-6', '7-8'],
        'letter_cluster':   ['ABC', 'BCD', 'CDA', 'DAB'],
        'segment_label':    ['A', 'B', 'C', 'D'],
    }
    for want, opts in SHAPES.items():
        check(f'opt_format[{want}]', classify_option_format(opts) == want)
    check('opt_format_empty_list_is_image_only',
          classify_option_format([]) == 'image_only')

    # all_observed MUST be SORTED, and the fixture must span MORE THAN ONE format or
    # the assertion is vacuous — a sorted 1-element list proves nothing, which is the
    # "finding no fixture can distinguish from silence" shape MUTATION_BUDGETS.json
    # exists to name. Three distinct formats across three years.
    # WHY THIS IS PINNED: unsorted set order made section_rules.md irreproducible
    # across processes. Two runs of identical code over an identical corpus produced
    # the same 433,260 bytes with a different sha256, differing at 34 lines — one per
    # subtopic (GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE D4). Set iteration order
    # over str depends on PYTHONHASHSEED, which python randomises PER PROCESS, so a
    # single process cannot see the defect and back-to-back runs look deterministic.
    qs = [{'options': SHAPES['single_value'], 'year': 2023},
          {'options': SHAPES['coordinate_pair'], 'year': 2024},
          {'options': SHAPES['image_only'], 'year': 2025}]
    fmt = subtopic_option_format(qs)
    check('all_observed_spans_three_formats', len(fmt['all_observed']) == 3)
    check('all_observed_is_sorted', fmt['all_observed'] == sorted(fmt['all_observed']))
    check('all_observed_exact',
          fmt['all_observed'] == ['coordinate_pair', 'image_only', 'single_value'])
    check('recent_format_is_the_latest_year', fmt['recent_format'] == 'image_only')
    check('changed_recently_true_when_latest_differs',
          fmt['changed_recently'] is True)
    empty = subtopic_option_format([])
    check('subtopic_option_format_empty_shape',
          empty['all_observed'] == [] and empty['changed_recently'] is False
          and empty['primary'] == 'single_value')

    # ── E-9 difficulty scoring: the 3-axis C/I/V contract Step 6 reads ─────
    d = score_difficulty({'stem': 'Compute 2+2.',
                          'options': ['(A) 3', '(B) 4', '(C) 5', '(D) 6']})
    check('score_difficulty_has_CIV_axes', all(k in d for k in ('C', 'I', 'V')))
    check('score_difficulty_score_is_sum_of_axes',
          d['score'] == d['C'] + d['I'] + d['V'])
    check('score_difficulty_has_level_and_flags',
          isinstance(d.get('level'), str) and isinstance(d.get('flags'), list))

    # ── E-10 strip mode / templates ───────────────────────────────────────
    check('determine_strip_mode_quantitative_for_maths',
          determine_strip_mode('Maths', 'Algebra', 'Quadratics') == 'quantitative')
    check('generate_templates_empty_is_safe', generate_templates([], 'numeric') == [])

    # ── E-11 note handling ────────────────────────────────────────────────
    check('note_freq_all_years_is_mandatory', classify_note_frequency(5, 5) == 'mandatory')
    check('note_freq_zero_total_is_safe', classify_note_frequency(0, 0) is not None)
    check('canonical_note_text_empty_is_empty_string', canonical_note_text({}) == '')

    # ── §4 vision aggregation ─────────────────────────────────────────────
    check('get_vision_candidates_empty_is_empty_list',
          get_vision_candidates([], {}, {}) == [])
    check('VISION_PER_SHEET_is_positive_int',
          isinstance(VISION_PER_SHEET, int) and VISION_PER_SHEET > 0)
    check('VISION_WORKDIR_is_absolute', str(VISION_WORKDIR).startswith('/'))

    # ── export surface: the stubs in the spec import exactly these ────────
    check('all_exports_exist', all(n in globals() for n in __all__))

    print(f"analyse_engine self-test: {passed} passed, {len(fails)} failed"
          + ("  — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("analyse_engine.py — Step 5 shared extraction engine. Run with --self-test.")
