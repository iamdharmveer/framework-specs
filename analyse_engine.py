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
import json
import os
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



# ═══ FROM Framework_MockTestAnalyse.md §3, fence L1884-2046 (v2.53.2) — VERBATIM ═══

def extract_shift_from_filename(path, session_re=None):
    """v2.16 RIGID-1: session/shift detection from the configurable keyword.

    WAVE 2 PART C B3 — THE ONE SESSION GLOBAL IN THE ENTIRE EXTRACTION SCOPE.
    This read module-level `SESSION_RE`, which §1 builds from exam_config.json's
    `session_keyword` at session start. An engine has its own globals and inherits
    nothing, so the regex is now INJECTED rather than reached for.

    It is a parameter, not module state set by a configure() call, deliberately:
    module state makes the engine non-reentrant and lets a caller that forgot to
    configure it silently use a STALE regex from a previous exam — a wrong answer
    rather than an error, which is this corpus's most expensive failure shape.
    A caller that forgets instead fails immediately and says what to pass, matching
    the v2.39 `vision_pending` precedent in process_pyq_paper below.
    """
    if session_re is None:
        raise RuntimeError(
            "extract_shift_from_filename: session_re not supplied. Pass "
            "session_re=SESSION_RE, the compiled regex §1 builds from "
            "exam_config.json's session_keyword via build_session_re(). It is exam "
            "configuration and cannot be defaulted here — guessing the keyword would "
            "silently mislabel every paper's shift (v2.16 RIGID-1).")
    m = session_re.search(os.path.basename(path))
    return f'S{m.group(1)}' if m else 'S1'

def process_pyq_paper(docx_path, paper_id, exam_code,
                      time_per_q, marks_per_q, options_count, multi_select,
                      progress, expected_size=None, vision_pending=None,
                      session_re=None):
    """
    All parameters auto-detected in S1-3, passed directly — no cfg dict.
    taxonomy not needed: presorted papers carry their own taxonomy headings.
    extract_presorted() is the only extraction path.

    v2.34 (GAP-2026-07-26-002):
      expected_size — DEFECT-5. The byte size Drive enumeration already captured, from
        paper_ref['fileSize']. Threaded to IMG-1, which SKIPped on every paper before
        this because nothing connected the two. None is still accepted (the upload lane
        may not know it) and IMG-1 then SKIPs for a legitimate reason.
    v2.37 (GAP-2026-07-26-003):
      probe_passed is GONE. Its only consumer was the in-loop vision block, which
        could not execute (see S3-1 / S4-2). This function now runs PHASE A only —
        it queues figural work and writes NO vision field. image_clarity has exactly
        one writer, apply_vision_observations() (S4-2c).
    """
    from docx import Document
    doc   = Document(docx_path)   # opened ONCE; passed to all sub-functions
    year  = extract_year_from_filename(docx_path)
    shift = extract_shift_from_filename(docx_path, session_re=session_re)

    # E-4: extract images. docx_path and expected_size are REQUIRED — without them the
    # v2.29 gates cannot run. Unpack order matches the single return shape
    # (image_map, q_roles, report); the old three-way unpack mis-bound silently because
    # both branches returned arity 3 in different orders (GAP-2026-07-26-002 DEFECT-2).
    image_map, q_roles, img_report = extract_and_map_images(
        doc, paper_id, docx_path, expected_size=expected_size)

    # Always presorted — single extraction path
    # v2.39 (GAP-2026-07-27-E): marking_scheme comes from exam_config via _meta and maps
    # an original exam position to a declared question_type. Exam-agnostic — the bands
    # are read at runtime and nothing about any exam is hardcoded. Absent scheme => the
    # positional branch is inert and detection is exactly v2.38.
    _mscheme = (progress.get('_meta', {}) or {}).get('marking_scheme') or []
    questions = extract_presorted(doc, year, shift, paper_id, q_roles,
                                  options_count, multi_select,
                                  marking_scheme=_mscheme)

    linked_groups = detect_linked_groups(questions)
    link_map = {qn: g['group_id'] for g in linked_groups for qn in g['q_numbers']}

    for q in questions:
        sm      = determine_strip_mode(q.get('section',''), q.get('topic',''), q.get('subtopic',''))
        # Determine marks per question: try 'MCQ' key first (most exams),
        # then try all values and use the max (handles GATE 1-mark/2-mark structure
        # where marks_per_q = {'1-mark':1,'2-mark':2} — use max available mark as default).
        q_marks = marks_per_q.get('MCQ') or marks_per_q.get('mcq') or max(marks_per_q.values(), default=1)
        q['option_format']   = classify_option_format(q.get('options', []))
        q['paper_id']        = paper_id   # needed for max_per_paper/typical_per_paper computation
        q['difficulty']      = score_difficulty(q, marks=q_marks, strip_mode=sm)
        q['image_role']      = q_roles.get(q['num'], {}).get('role', 'none')
        q['linked_group_id'] = link_map.get(q['num'])
        q['year']            = year
        q['shift']           = shift
        q['paper_id']        = paper_id
        # v2.23 THREE-AXIS TAGGING: tag Axis-1/2/3 now that linked_group_id + image_role
        # + options are all set (the LINKED gate and FIGURAL/NAT signals need them).
        # Step 8 re-tags GENERATED questions with the SAME AXIS CLASSIFIER v1.0 functions.
        tag_axes(q)

    # IMG-5b: cross-check image presence against Axis-1 now that tag_axes() has run.
    img5b = run_img5b({e['q_num']: [e['path']] for e in image_map}, questions,
                      overrides=tuple(progress.get('_meta', {}).get('inherently_visual', ())))

    # §4: PHASE A. Claude CANNOT view an image from inside this python process — a
    # view() is a TOOL CALL and a tool call can only happen BETWEEN model turns. This
    # loop therefore QUEUES the work and writes contact sheets to disk; Phase B (S4-2b)
    # performs the views at the batch boundary the run already stops at; Phase C
    # (S4-2c) folds the observations back in. See EXECUTION-BOUNDARY LAW.
    #
    # GAP-2026-07-26-003. What stood here was `vision_result = analyse_image_claude(...)`
    # followed by `vision_result.get(...)`. analyse_image_claude() was a `pass` stub, so
    # the call returned None and the next line raised AttributeError — meaning the block
    # could not run AS WRITTEN at all. Every production run therefore executed some
    # SUBSTITUTED body, and the substitution that shipped wrote image_clarity only.
    # Measured on IIT_JAM_BIOTECHNOLOGY: object_type/transformation/arrangement/
    # complexity present on 0 of 1719 questions; 153/153 figural = vision_unavailable;
    # 45/45 FIGURAL subtopics shipped an empty profile; QV-9 returned PASS.
    #
    # NOTHING HERE HALTS. image_clarity is NOT written in this loop — Phase C is its
    # only writer (one writer, no drift). Until Phase C runs the field is simply absent.
    # v2.39 (GAP-2026-07-27-B) — THIS FUNCTION NO LONGER BUILDS THE QUEUE.
    #
    # build_vision_queue() WRITES vision_queue.json and vision_sheet_NNN.png into
    # VISION_WORKDIR, which S4-2a defines as one directory per RUN, not per paper. It
    # never read an existing queue, and both filenames are fixed constants
    # (VISION_QUEUE_NAME, VISION_SHEET_FMT) — so calling it once per paper meant paper N
    # OVERWROTE the queue and sheets of papers 1..N-1. Only the last paper of a batch
    # ever survived into Phase B.
    #
    # MEASURED on IIT_JAM_BIOTECHNOLOGY: 153 figural questions across 22 papers, but
    # _meta.vision recorded queued=8 — the final paper's count alone. Batch 7 queued
    # 11 + 10 + 3 = 24 and 3 survived. Five separate sessions hit this and each invented
    # a DIFFERENT workaround (run-level vision_records.json, vision_items.json rebuilt
    # over a union, carry-forward from disk, two independent hoists); no two agreed, and
    # divergent tag assignment between them would orphan observations silently.
    #
    # The stated Phase A invariant — "every queued item appears on exactly one sheet,
    # and that sheet exists" — was violated in the OPPOSITE direction: sheets existed
    # that no queue referenced.
    #
    # Candidates are accumulated here and the queue is built ONCE, at the batch
    # boundary, in run_batch_loop() immediately before Phase B.
    vision_candidates = get_vision_candidates(questions, q_roles, image_map)
    if vision_pending is None:
        # A caller that forgets the accumulator would silently drop every figure in the
        # paper — the exact failure mode this fix exists to remove. Fail loudly instead.
        raise RuntimeError(
            "process_pyq_paper: vision_pending accumulator not supplied. Phase A "
            "candidates must be collected at the RUN level and passed to "
            "corpus_io.build_vision_queue() ONCE, at the batch boundary (v2.39 "
            "GAP-2026-07-27-B). Pass vision_pending=<list> from run_batch_loop().")
    vision_pending.extend(
        {'paper_id': paper_id, 'q_num': q['num'],
         'srcs': [p for p in srcs if p],
         'subtopic': q.get('subtopic'), 'image_role': q.get('image_role')}
        for q, srcs in vision_candidates)
    if vision_candidates:
        print(f"    PHASE A: {len(vision_candidates)} figural question(s) accumulated "
              f"for this paper ({len(vision_pending)} pending in this batch)")

    for q in questions:
        key = (q.get('section','?'), q.get('topic','?'), q.get('subtopic','?'))
        progress.setdefault(key, []).append(q)

    progress.setdefault('_linked_groups', {})
    for g in linked_groups:
        progress['_linked_groups'][g['group_id']] = g

    meta = progress.setdefault('_meta', {'papers_processed':[],'total_questions':0,
                                          'years_processed':[]})
    meta['papers_processed'].append(paper_id)
    meta['total_questions'] += len(questions)
    if year and year not in meta['years_processed']:
        meta['years_processed'].append(year)

    # GAP-2026-08-16-BASELINE-SUPPRESSED-NAMEERRORS (D5). This line read `n_vision`,
    # which is a LOCAL of run_batch_loop() in §8 — bound nowhere in this function, this
    # section, or at module scope. process_pyq_paper() therefore raised
    # `NameError: name 'n_vision' is not defined` on its second-to-last statement, on
    # EVERY paper of EVERY exam, unguarded, after all the work was done and before
    # `return questions, linked_groups` could run.
    # It survived because spec_name_audit DETECTED it and `n_vision` sat in
    # spec_name_audit_baseline.json as an accepted unbound name — the same untyped
    # baseline that hid D2/D3 in GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE.
    # The per-paper figural count is len(vision_candidates); §8's n_vision is the
    # BATCH-level queue size and was never the right number here. "queued" not
    # "analysed": Phase B does the analysis, this is Phase A accumulation.
    print(f"  {os.path.basename(docx_path)}: {len(questions)} Qs, "
          f"{len(linked_groups)} linked groups, "
          f"{len(vision_candidates)} figural image(s) queued for vision")
    return questions, linked_groups

# ═══ FROM Framework_MockTestAnalyse.md §3, fence L2083-2093 (v2.53.2) — VERBATIM ═══
def vision_liveness(stats):
    """Session vision verdict, derived from Phase-C merge stats. Never raises.

    'not_applicable' — nothing was queued (a text-only exam is not a failure)
    'unavailable'    — figures were queued and NOTHING came back
    'partial'        — some cells observed, some omitted (procedural, re-runnable)
    'observed'       — every queued figure observed
    """
    return stats.get('vision_status', 'not_applicable')

# ═══ FROM Framework_MockTestAnalyse.md §3, fence L2144-2170 (v2.53.2) — VERBATIM ═══
def run_img5b(mapping, questions, overrides=()):
    """Gate IMG-5b — cross-check image presence against Axis-1 classification.

    v2.35 (audit_callgraph C4). corpus_io.figural_consistency() has existed since
    v2.29 and was called from NOWHERE — it appeared only in the prose bullet above,
    so the gate written to catch exactly the DEFECT-3 class of fault never ran. Two
    defects were masking each other: IMG-5b would have detected the missing
    q_roles['role'], but IMG-5b itself was unreachable.

    WARN, not HARD STOP: a mismatch can be legitimate (an INHERENTLY-VISUAL override
    is visual without carrying an embedded figure), and IMG-4 already hard-stops on
    actual image loss. This gate reports classification disagreement.
    """
    q_formats = {q['num']: q.get('format') or q.get('axis1') for q in questions}
    fc = corpus_io.figural_consistency(mapping, q_formats, overrides=overrides)
    if fc['image_not_figural']:
        print(f"    ! IMG-5b WARN — question(s) carry an image but are not FIGURAL: "
              f"{fc['image_not_figural'][:10]}")
        print(f"      An image present in the document but absent from the format "
              f"distribution is the silent corruption IMG-4 cannot see.")
    if fc['figural_no_image']:
        print(f"    ! IMG-5b WARN — question(s) classified FIGURAL with no image: "
              f"{fc['figural_no_image'][:10]}")
        print(f"      Expected only for logged INHERENTLY-VISUAL overrides.")
    return fc

# ═══ FROM Framework_MockTestAnalyse.md §3, fence L2174-2478 (v2.53.2) — VERBATIM ═══
# v2.27 — DELEGATED TO THE ENGINE (blueprint_core Cluster G). These three functions existed
# in BOTH this spec and Framework_PYQAnalyse Phase B, which walk the SAME sorted .docx and
# must agree. Each pair had drifted despite an explicit "keep IDENTICAL" instruction and
# EC-P14 naming the failure mode. One definition now, so they cannot drift again.
# GAP-2026-07-26-001 — next_text IS MANDATORY for sorted-PYQ walks.
# PYQSort EC-S8 emits multi-paragraph stems whose continuation lines are bold, not
# dates, not options and not question starts — character for character the heading
# predicate. In extract_presorted() below this is the DANGEROUS half of the defect:
# the inner loop breaks on a heading, so a continuation line terminated its own
# question mid-body, truncating the stem and orphaning every option after it, with
# no error raised anywhere. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers): 16
# questions truncated, 28 option lines silently discarded, 10 papers affected.
# Step 4's phantom gate stops the run; nothing here stopped anything.
is_taxonomy_heading      = lambda para, next_text=None, colour_available=False: bc.is_taxonomy_heading(para, is_option, next_text, colour_available)
parse_taxonomy_level     = bc.parse_taxonomy_level
extract_year_from_filename = bc.extract_year_from_filename

def detect_blank_position(stem):
    m = re.search(r'_{3,}', stem)
    if not m: return 'none'
    pos = m.start() / max(len(stem), 1)
    return 'start' if pos < 0.2 else ('end' if pos > 0.8 else 'middle')

# ── v2.5 MSQ detection (EC-A root-cause fix) ──────────────────────────────────
# Forgery-resistant: keys on OPTION SHAPE, not stem wording. A statement-
# combination MCQ (EC-9) whose options are predominantly combination-labels
# ("Only 1", "Both 1 and 2", "Neither … nor …", "1 and 3", "None of …",
# "All of the above") is SINGLE-answer and must never be tagged MSQ, even when
# its stem reads "Which is/are correct". Conversely a genuine multi-select stem
# with ordinary content options IS an MSQ. Used only when multi_select=True.
_MSQ_INSTR_RE = re.compile(
    r'select all that apply|select all|one or more (?:options?|are|may)|'
    r'select\s+two|select\s+three|more than one (?:option|correct)|'
    r'which .*\bare correct\b', re.IGNORECASE)
_COMBO_OPT_RE = re.compile(
    r'^\s*(only\b|both\b|neither\b|all of\b|none of\b|'
    r'\d+\s+and\s+\d+\b|\d+\s*,\s*\d+)', re.IGNORECASE)

def _is_statement_combination(options):
    """True when the option SET is predominantly combination-labels (EC-9 MCQ)."""
    opts = [o for o in (options or []) if isinstance(o, str) and o.strip()]
    if not opts:
        return False
    combo = sum(1 for o in opts if _COMBO_OPT_RE.match(o.strip()))
    return combo >= max(2, len(opts) - 1)   # most/all options are combo-labels

def detect_is_msq(full_stem, options, positional_type=None):
    """v2.5 contract detector. Caller already gated on multi_select=True.

    v2.39 (GAP-2026-07-27-E) — POSITIONAL BRANCH ADDED.

    The instruction-phrase test alone measured 24 MSQ across 1,719 questions on an exam
    whose marking scheme reserves Q31-40 for MSQ (~10/paper, so ~120 in the current era
    alone). The cause is cross-step information destruction, not a weak regex: PYQSort
    renumbers questions into taxonomy order, so by the time Step 5 reads the paper the
    exam positions that identify the MSQ band no longer exist. Step 5 could not recover
    what Step 3 had discarded.

    PYQSort v1.18 now stamps the original position into the date label, so the band is
    knowable again. positional_type is the question_type whose marking_scheme q_range
    covers that position — exam-agnostic, read from exam_config at runtime, no hardcoded
    ranges anywhere.

    PRECEDENCE. The EC-A guard still wins: a statement-combination MCQ is NEVER MSQ,
    however it is banded, because its option SHAPE is forgery-resistant evidence about
    the answer mechanism and a band is only evidence about where the question sat. A
    paper that deviates from its own declared scheme is thereby not mis-typed.

    positional_type is None for a pre-v1.18 sorted file, an absent marking_scheme, or a
    position no band covers. All three mean "no positional evidence" and fall back to
    v2.5 behaviour exactly — so no exam changes until its papers are re-sorted.
    """
    if _is_statement_combination(options):   # EC-A guard — highest precedence
        return False
    if _MSQ_INSTR_RE.search(full_stem or ''):
        return True
    return positional_type == 'MSQ'


def _detect_option_label_style(raw_option_lines):
    """
    v2.15 BUG-D07: Detect option LABEL style from raw option lines.
    Returns: '1/2/3/4' | 'A/B/C/D' | '(1)/(2)/(3)/(4)' | '(A)/(B)/(C)/(D)' | 'A)/B)/C)/D)' | 'unknown'
    Distinct from option FORMAT type (single_value etc.) which describes CONTENT shape.
    """
    if not raw_option_lines:
        return 'unknown'
    for line in raw_option_lines:
        t = line.strip()
        if re.match(r'^[1-5]\.\s+', t):       return '1/2/3/4'
        if re.match(r'^[A-E]\.\s+', t):        return 'A/B/C/D'
        if re.match(r'^[a-e]\.\s+', t):        return 'a/b/c/d'
        if re.match(r'^\([1-5]\)\s+', t):      return '(1)/(2)/(3)/(4)'
        if re.match(r'^\([A-E]\)\s+', t):      return '(A)/(B)/(C)/(D)'
        if re.match(r'^\([a-e]\)\s+', t):      return '(a)/(b)/(c)/(d)'
        if re.match(r'^[A-E]\)\s+', t):        return 'A)/B)/C)/D)'
        if re.match(r'^[a-e]\)\s+', t):        return 'a)/b)/c)/d)'
    return 'unknown'


def extract_presorted(doc, year, shift, paper_id, q_roles, options_count, multi_select,
                      marking_scheme=None):
    questions = []
    cur_sec = cur_top = cur_sub = ''
    cur_date_label = None          # v2.39 — carries the stamped original position
    # GAP-2026-07-26-001 + GAP-2026-08-05-001. BLOCK-level: tables are not paragraphs,
    # and an image/equation/object-only paragraph has no TEXT — the old lookahead
    # skipped both and returned the next question's date label, so a bold stem
    # continuation passed the level-3 heading test and TRUNCATED its own question here.
    paras, nxt = bc.sorted_body_lookahead(doc)
    colour_ok  = bc.heading_colour_available(paras)   # D6 — probed ONCE per FILE
    terminated_by_heading = 0     # QV-15 counter (GAP-2026-08-05-001)
    # Per-question flag, RESET at the top of every question body below. Initialised
    # here as well so it is defined even for a question whose body loop never runs.
    _ended_by_heading = False
    i = 0

    while i < len(paras):
        para = paras[i]; text = para.text.strip()
        if not text: i += 1; continue

        if is_taxonomy_heading(para, nxt[i], colour_ok):   # GAP-2026-07-26-001 + -08-05-001
            lv, content = parse_taxonomy_level(text)
            if lv == 1: cur_sec = content
            elif lv == 2: cur_top = content
            else: cur_sub = content
            i += 1; continue

        # BUG-A16 fix: case-insensitive shift tag check via pattern
        # v2.39 (GAP-2026-07-27-E): the label is RETAINED, not merely skipped. PYQSort
        # v1.18 stamps the original exam position into it, which is the only surviving
        # evidence of the MSQ band after Step 3's renumbering.
        # bc.is_position_label is THE predicate (bc.DATE_TAG_RE). The inline literal
        # that stood here is the one bc.DATE_TAG_RE's own comment claims to have
        # replaced at GAP-2026-07-26-001; it had not been. Writer (PYQSort) and reader
        # (here) now share one definition, so they cannot drift apart again.
        if bc.is_position_label(text):
            cur_date_label = text
            i += 1; continue

        q_num = detect_question_start(text)
        if q_num is None: i += 1; continue

        options      = []
        options_raw  = []   # v2.15 BUG-D07: raw option lines for label detection
        omml_present = False
        omml_ok      = True   # BUG-A05 fix: start True, AND-reduce below

        # ── GAP-2026-08-15-BAREQ, defect F-2 — THE STEM PARAGRAPH IS A PARAGRAPH TOO ──
        # Until 2026-08-15 stem_parts[0] was built from `text`, i.e. para.text, which is
        # <w:t>-only. Every CONTINUATION line went through enrich_paragraph_with_omml();
        # the stem paragraph — the one paragraph guaranteed to exist for every question —
        # did not. So the equation in a stem paragraph, which is the NORMAL shape for a
        # mathematics, physics, statistics or quantitative-aptitude paper, was silently
        # dropped from full_stem, and therefore from 'stem', 'stem_raw', detect_is_msq(),
        # detect_blank_position(), the negative-question test, the dedupe/taxonomy keys,
        # PYQ_STEM_PATTERNS and every mock question derived from the item.
        #
        # Measured on IIT_JAM_MATHEMATICS 12-Feb-2017: 46 of 60 stems (77%) lost part or
        # all of their mathematics, and a stem that was ENTIRELY OMML extracted as ''.
        #
        # omml_present was computed from the body loop alone, so a question whose maths
        # lives only in the stem paragraph was recorded omml_present=False — which made
        # QV-8 (OMML recovery >= 80%) skip exactly those questions (om == [] -> PASS).
        # Producer and consumer sharing a blind spot is what made this silent, the same
        # shape as the Q-detector defect above. Seeding both flags from the stem closes it.
        _stem_txt = re.sub(r'^Q\.?\d+\.?\s*', '', text).strip()
        _stem_txt, _stem_ok, _stem_has_omml = enrich_paragraph_with_omml(_stem_txt, para)
        if _stem_has_omml:
            omml_present = True
            omml_ok      = omml_ok and _stem_ok
        stem_parts   = [_stem_txt]
        i += 1

        while i < len(paras):
            nt = paras[i].text.strip()
            if not nt: i += 1; continue
            # ── GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION ────────────────────
            # A PYQSort position label ALWAYS precedes the next question and can never
            # be part of THIS question's body. Terminating here — rather than absorbing
            # it as a stem continuation — is what lets the OUTER loop refresh
            # cur_date_label PER QUESTION. Without it the outer loop's label branch is
            # UNREACHABLE after the first question of a taxonomy block, so every
            # question in that block inherits the block's FIRST exam position and the
            # label text is concatenated into the preceding stem.
            # MEASURED (IIT_JAM_MATHEMATICS, 3 papers, declared A=90/B=30/C=60): bands
            # read 150/17/13; is_msq 18 against 30; 179 of 180 stems carried embedded
            # label text. After this line: 90/30/60 exact, is_msq 30, 0 pollution,
            # holding to 884/884 across the full 22-paper corpus.
            # WHY THE EXISTING TERMINATORS CANNOT CATCH IT: a label is not a question
            # start, and is_taxonomy_heading() fires on 0 of 60 labels (measured). The
            # loop was structurally incapable of stopping here; this is not tuning.
            # THIS TEST MUST SIT ABOVE THE HEADING TEST. A label is definitionally not
            # a heading, and evaluating it there would let a mis-inference increment
            # QV-15's terminated_by_heading on a paragraph that can never be one.
            # BREAK WITHOUT ADVANCING i. Control returns to the outer loop with i still
            # on the label; the outer loop re-reads it, matches its own branch, assigns
            # and advances. This mirrors the question-start break exactly and keeps
            # cur_date_label at ONE writer. Termination is safe because both tests are
            # the SAME engine predicate, so if the inner fires the outer necessarily
            # fires — divergence is the only spin risk and one definition makes it
            # unreachable. Cost: one redundant predicate call per question.
            if bc.is_position_label(nt):
                break
            # GAP-2026-07-26-001: nxt[i] is what stops a bold STEM CONTINUATION from
            # terminating its own question here. Without it the stem is truncated and
            # every option after this point is silently discarded.
            # _ended_by_heading is initialised to False before this loop (see above),
            # so a question whose body loop never runs can never leave it unbound.
            _ended_by_heading = (detect_question_start(nt) is None and
                                 is_taxonomy_heading(paras[i], nxt[i], colour_ok))
            if detect_question_start(nt) is not None or _ended_by_heading:
                if _ended_by_heading:
                    terminated_by_heading += 1   # QV-15 (GAP-2026-08-05-001)
                break
            if is_option(nt, paras[i]):
                options.append(clean_option_text(nt))
                options_raw.append(nt)   # v2.15: preserve raw line for label detection
            else:
                enriched, ok, has_omml = enrich_paragraph_with_omml(nt, paras[i])
                if has_omml:
                    omml_present = True
                    omml_ok      = omml_ok and ok  # BUG-A05 fix: AND not replace
                    stem_parts.append(enriched)
                else:
                    stem_parts.append(nt)
            i += 1

        full_stem  = ' '.join(stem_parts)
        clean_stem, note, note_found = extract_note_block(full_stem)
        blank_pos  = detect_blank_position(clean_stem)
        is_neg     = bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', full_stem))
        # multi_select is auto-detected in S1-3 from exam pattern + PYQ stems.
        # v2.5 EC-A ROOT-CAUSE FIX: the old detector (r'select all|which.*are correct')
        # false-matched statement-combination MCQs (EC-9: "Which is/are correct?" with
        # combo-label options "1. Only A", "3. Both A and B"), which are SINGLE-answer.
        # The forgery-resistant signal is OPTION SHAPE, not stem wording:
        #   - a stem with a genuine multi-select instruction phrase, AND
        #   - options that are NOT predominantly combination-labels (only/both/neither/
        #     "X and Y"/none-of/all-of) ⇒ MSQ.
        # A statement-combination MCQ (most options are combo-labels) is NEVER MSQ even
        # when its stem says "are correct". Validated empirically (both directions).
        # v2.39 (GAP-2026-07-27-E): resolve the exam position stamped by PYQSort v1.18
        # into a declared question_type. Both helpers live in corpus_io Cluster Q — the
        # same engine PYQSort delegates its stamp to — so writer and reader cannot drift.
        _orig_q = corpus_io.parse_original_q_num(cur_date_label)
        _pos_ty = corpus_io.question_type_for_position(_orig_q, marking_scheme)
        is_msq = bool(multi_select) and detect_is_msq(full_stem, options,
                                                      positional_type=_pos_ty)

        # BUG-D07 fix (v2.15): detect option label style per question
        # from the RAW option lines (before clean_option_text strips the label).
        # This is the LABEL style ('1/2/3/4' vs 'A/B/C/D' etc.), distinct from
        # option FORMAT type ('single_value' etc.) which describes content shape.
        _label = _detect_option_label_style(options_raw)

        # GAP-2026-08-05-001 (QV-15). Record whether an INFERRED heading ended this
        # question's body. When the inference is wrong the stem is truncated and every
        # remaining option is discarded — silently, because nothing counted it. Stamped
        # here so QV-15 can test it per question rather than only in aggregate.
        questions.append({
            'num'         : q_num,
            'terminated_by_heading': _ended_by_heading,
            # v2.37 (GAP-2026-07-26-003 PART 9). BOTH keys are stamped at the ONE
            # emission point. This dict was emitted with 'num' only, while
            # blueprint_core.paper_eras_from_progress() reads q.get('q_num') and the
            # S-SECMAP block reads _q['q_num'] behind a "'q_num' not in _q: continue"
            # guard. The era classifier therefore collected None for every question,
            # filtered to an empty list and labelled all 22 reference papers on a
            # question count of ZERO; S-SECMAP's Stage-1 observation was empty, so
            # every subject fell through to the Stage-3 fallback and every section
            # received every subject. Both failures were SILENT.
            # EC-V15 also depends on this: the vision queue is keyed (paper_id, q_num),
            # and a bare q_num collides across papers — measured on the reference
            # corpus, 153 figural questions carry only 62 distinct q_num values, so
            # keying on q_num alone would have mis-attributed 91 of them.
            'q_num'       : q_num,
            # v2.39 (GAP-2026-07-27-E + GAP-X residual). The ORIGINAL exam position and
            # the type declared for its band are persisted, not just consumed. Two
            # reasons: classify_paper_era()'s type-corroboration branch was inert
            # because question_type never reached the persisted dict (measured:
            # type_checked False on all 22 reference papers, so era rested on question
            # COUNT alone); and a re-synthesis from progress.json alone can now redo
            # positional typing without re-reading any docx. None means "unknown" — a
            # pre-v1.18 sorted file, or a position no band covers — never "position 0".
            'original_q_num': _orig_q,
            'question_type' : _pos_ty,
            'stem'        : clean_stem,
            'stem_raw'    : full_stem,
            'options'     : options,
            'section'     : cur_sec,
            'topic'       : cur_top,
            'subtopic'    : cur_sub,
            'has_note'    : note_found,
            'note_text'   : note,
            'blank_pos'   : blank_pos,
            'is_negative' : is_neg,
            'is_msq'      : is_msq,
            'omml_present': omml_present,
            'omml_failed' : omml_present and not omml_ok,
            'option_label': _label,   # v2.15 BUG-D07: '1/2/3/4' | 'A/B/C/D' | etc.
        })
    return questions

# ═══ FROM Framework_MockTestAnalyse.md §5, fence L2667-2676 (v2.53.2) — VERBATIM ═══
def pre_synthesis_check(progress, taxonomy, target='ALL'):
    for sec, entries in taxonomy.items():
        if target != 'ALL' and sec != target: continue
        for e in entries:
            key   = (sec, e['topic'], e['subtopic'])
            count = len(progress.get(key, []))
            if count == 0:  print(f"ABSENT: {e['subtopic']} -- no PYQ data")
            elif count < 3: print(f"SPARSE: {e['subtopic']} -- only {count} Qs (inferred)")

# ═══ FROM Framework_MockTestAnalyse.md §5, fence L2680-3614 (v2.53.2) — VERBATIM ═══
# ════════════════════════════════════════════════════════════════════════════
# AXIS CLASSIFIER v1.0  (v2.23 — SHARED SINGLE SOURCE OF TRUTH)
# ────────────────────────────────────────────────────────────────────────────
# The canonical, exam-agnostic classifier for the three orthogonal format axes.
# audit_canonical.py MUST re-tag GENERATED questions with THESE SAME
# functions (import/copy verbatim, never re-implement) — the PYQ distribution and
# the generated distribution are only comparable if classified identically.
#
#   Axis 1  STIMULUS/MEDIA  : TEXT | FIGURAL | PASSAGE | DI
#   Axis 2  STEM STRUCTURE  : the exclusive 8-class ladder (below)
#   Axis 3  ANSWER MECHANISM: MCQ | MSQ | NAT
#   negative polarity       : an ORTHOGONAL boolean flag (is_negative), NOT a class
#
# EXCLUSIVITY: every question maps to exactly ONE Axis-2 class (first-match-wins).
# LINKED is a GATE decided by shared-stimulus membership (linked_group_id), never by
# phrasing — an assertion-reason question printed inside a passage is LINKED, and its
# inner shape becomes a secondary detail only. SEQUENCE sits ABOVE STATEMENT because
# "arrange the following statements in order" is fundamentally an ordering task.
# ════════════════════════════════════════════════════════════════════════════

AXIS2_CLASSES = ['LINKED', 'ASSERTION_REASON', 'MATCH', 'SEQUENCE', 'STATEMENT',
                 'FILL_BLANK', 'ODD_ONE_OUT', 'DIRECT']   # ladder order == precedence

# Canonical stem_format_variant → Axis-2 class map. Step 7's STEM_FORMAT_MENU tokens
# MUST map through this table (File 4 wires Step 7 to it) so capability stays consistent.
STEM_FORMAT_TO_AXIS2 = {
    'direct_question': 'DIRECT', 'isolated_word': 'DIRECT', 'phrase_to_word': 'DIRECT',
    'reverse_word_to_phrase': 'DIRECT', 'definition_to_word': 'DIRECT',
    'meaning_of_idiom': 'DIRECT', 'idiom_for_situation': 'DIRECT',
    'sentence_substitution': 'DIRECT', 'sentence_embedded_underlined': 'DIRECT',
    'fill_blank': 'FILL_BLANK', 'fill_in_context_blank': 'FILL_BLANK',
    'assertion_reason': 'ASSERTION_REASON', 'match_the_following': 'MATCH',
    'statement_correctness': 'STATEMENT', 'sequence_ordering': 'SEQUENCE',
    'odd_one_out': 'ODD_ONE_OUT', 'odd_one_out_pair': 'ODD_ONE_OUT',
}

# family → set of Axis-2 classes its Step-7 menu can faithfully render (derived from
# Step 7 STEM_FORMAT_MENU via STEM_FORMAT_TO_AXIS2; kept explicit for round-trip clarity).
FAMILY_AXIS2_MENU = {
    'vocab_single_word'    : {'DIRECT', 'FILL_BLANK', 'ODD_ONE_OUT'},
    'one_word_substitution': {'DIRECT'},
    'idiom_phrase'         : {'DIRECT', 'ODD_ONE_OUT'},
    'fact_recall'          : {'DIRECT', 'FILL_BLANK', 'ASSERTION_REASON', 'MATCH',
                              'ODD_ONE_OUT', 'STATEMENT'},
}

_TABLE_WORD_RE = re.compile(r'(?i)\b(table|tabulated|following data|dataset)\b')
def _looks_like_table_stimulus(stem):
    """v2.24.6 FIX C — SHARED, single-source-of-truth structural table detector.
    Was, independently in TWO places (classify_axis1 here and synthesise_subtopic's
    has_tbl), a naive substring match `'|' in stem or 'table' in stem.lower()` that
    false-positived on any word merely CONTAINING "table" — "vegetable", "acceptable",
    "notable" — with no real tabular data present. Requires either (a) >=2 pipe-delimited
    rows (a real rendered table), or (b) a word-boundary table-keyword match co-occurring
    with >=1 pipe-delimited row. A bare stray '|' or an unrelated "table"-containing word
    alone no longer qualifies. MUST PROPAGATE (byte-identical) to audit_canonical.py's
    verbatim classifier copy — same requirement as classify_axis2's MATCH rule.
    """
    stem = stem or ''
    pipe_rows = sum(1 for ln in stem.splitlines() if ln.count('|') >= 2)
    return pipe_rows >= 2 or (bool(_TABLE_WORD_RE.search(stem)) and pipe_rows >= 1)

def classify_axis1(q):
    """STIMULUS/MEDIA. Priority FIGURAL > PASSAGE > DI > TEXT — identical ordering to
    the per-subtopic `fmt` line in synthesise_subtopic (a linked DI passage resolves
    PASSAGE, matching that function)."""
    if q.get('image_role', 'none') not in ('none', None):
        return 'FIGURAL'
    if q.get('linked_group_id'):
        return 'PASSAGE'
    stem = (q.get('stem') or q.get('stem_raw') or '')
    if _looks_like_table_stimulus(stem):
        return 'DI'
    return 'TEXT'

def classify_axis3(q):
    """ANSWER MECHANISM. NAT = no selectable options (mirrors the answer_type=='numerical'
    detection: zero text options AND no option-images). MSQ = is_msq. Else MCQ."""
    opts = q.get('options', []) or []
    if len(opts) == 0 and q.get('image_role', 'none') not in ('options_only', 'stem_and_options'):
        return 'NAT'
    return 'MSQ' if q.get('is_msq') else 'MCQ'

def _opts_are_combination_labels(opts):
    """EC-A signal: options predominantly combination-labels (Only N / Both N and M /
    Neither…nor / None of / All of the above / "N and M"). Distinguishes STATEMENT and
    MATCH combo-answer stems from genuine free-form options."""
    if not opts:
        return False
    combo = 0
    for o in opts:
        t = (o or '').strip().lower()
        if re.search(r'\b(only|both|neither|none of|all of)\b', t) or \
           re.match(r'^[a-d1-4](\s*(and|,|&|-)\s*[a-d1-4])+$', t):
            combo += 1
    return combo >= max(2, (len(opts) + 1) // 2)

# ── MATCH option-shape backstop (v2.24.2) ──────────────────────────────────────
# A language-agnostic MATCH signal: the OPTIONS are a set of CROSS-DOMAIN label pairs
# (e.g. "A-I, B-III, C-IV, D-II" / "1-C 2-A 3-D 4-B" / "(A)-(i), (B)-(iv) ..."). It fires
# when the stem keywords (match / list-I / column) are ABSENT — the two cases that matter:
#   (a) NON-ENGLISH match papers (Hindi/regional), whose stems carry no English cue;
#   (b) matches whose List-I/List-II body has been rendered into a Word table, so the list
#       labels no longer appear in stem_raw (only the "Match ..." instruction does).
# CROSS-DOMAIN (left label family != right label family) is REQUIRED, so digit:digit ratios
# ("2:3, 4:5"), coordinate pairs and word-word hyphenations never trip it. The family of a
# COLUMN (not a single token) is used so the roman-vs-letter "I" ambiguity resolves from
# context (a column carrying II/III/IV is roman even where a bare I appears).
_MATCH_PAIR_RE = re.compile(
    r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
    r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MATCH_PAIR_SUB = (r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
                   r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MATCH_OPT_RE = re.compile(r'^\s*' + _MATCH_PAIR_SUB + r'(?:[,;\s]+' + _MATCH_PAIR_SUB + r'){1,}\s*$')

def _label_family(tokens):
    """Family of a same-side label COLUMN: 'digit' | 'roman' | 'alpha' | 'other'.
    Column-level (not per-token) so a bare 'I' resolves to roman when its column also
    carries II/III/IV, and to alpha when its column is A/B/C/D."""
    low = [t.lower() for t in tokens if t]
    if not low:
        return 'other'
    if all(re.fullmatch(r'\d{1,2}', t) for t in low):
        return 'digit'
    romanish = all(re.fullmatch(r'[ivxlcdm]+', t) for t in low)
    if romanish and any(len(t) > 1 for t in low):
        return 'roman'
    if all(re.fullmatch(r'[a-z]', t) for t in low):
        return 'roman' if set(low) <= {'i', 'v', 'x'} else 'alpha'
    if romanish:
        return 'roman'
    if all(re.fullmatch(r'[a-z]{1,4}', t) for t in low):
        return 'alpha'
    return 'other'

def _opts_are_match_pairs(opts):
    """True when a MAJORITY of options are each a set of >=2 CROSS-DOMAIN label pairs that
    consume the whole option text. Threshold mirrors _opts_are_combination_labels. Used by
    classify_axis2 AFTER the keyword rules, so it can only convert a would-be non-MATCH
    class to MATCH, never the reverse (additive + monotone)."""
    if not opts:
        return False
    hits = 0
    for o in opts:
        st = (o or '').strip()
        if not st or not _MATCH_OPT_RE.match(st):
            continue
        pairs = _MATCH_PAIR_RE.findall(st)
        if len(pairs) < 2:
            continue
        lf = _label_family([p[0] for p in pairs])
        rf = _label_family([p[1] for p in pairs])
        if lf == rf or 'other' in (lf, rf):
            continue
        hits += 1
    return hits >= max(2, (len(opts) + 1) // 2)

def classify_axis2(q):
    """STEM STRUCTURE — the exclusive 8-class ladder (first-match-wins). Discrimination
    is by task-verb + option-shape, not ladder position alone, so collisions are rare and
    deterministic. Grounded in EC-8/9/11/12/13; SEQUENCE + ODD_ONE_OUT added in v2.23."""
    # GATE 0 — LINKED: structural, decided by shared-stimulus membership, not phrasing.
    if q.get('linked_group_id'):
        return 'LINKED'
    stem = (q.get('stem_raw') or q.get('stem') or '')
    s    = stem.lower()
    opts = q.get('options', []) or []
    # 1 — ASSERTION_REASON (EC-8): both an Assertion and a Reason clause present.
    if re.search(r'\bassertion\b', s) and re.search(r'\breason\b', s):
        return 'ASSERTION_REASON'
    # 2 — MATCH (EC-13): match/list-I/column stems, OR (v2.24.2) a CROSS-DOMAIN label-pair
    #     option shape. The option-shape backstop is language-agnostic and table-safe (see
    #     _opts_are_match_pairs): it catches non-English matches and matches whose List-I/
    #     List-II body has moved into a Word table. Placed AFTER the keyword rules it is
    #     additive/monotone — it only converts a would-be non-MATCH class to MATCH.
    if re.search(r'\bmatch\b', s) and re.search(r'\b(following|list|column|set)\b', s):
        return 'MATCH'
    if re.search(r'list[\s\-]*i\b|column[\s\-]*(i|a)\b', s):
        return 'MATCH'
    if _opts_are_match_pairs(opts):
        return 'MATCH'
    # 3 — SEQUENCE / ORDERING (v2.23): the OPERATION is arranging (kept above STATEMENT).
    if re.search(r'\b(arrange|rearrange|correct sequence|proper sequence|correct order|'
                 r'logical order|chronological order|sequence of the following|'
                 r'order of the following)\b', s):
        return 'SEQUENCE'
    # 4 — STATEMENT-BASED (EC-9): "consider the following statements … which is/are correct"
    #     with combination-label options (the EC-A option-shape signal confirms it).
    if re.search(r'consider the following statements?|following statements?\b', s) and \
       (re.search(r'which .*(is|are) (correct|true|incorrect|false)', s)
        or _opts_are_combination_labels(opts)):
        return 'STATEMENT'
    # 5 — FILL_BLANK / CLOZE (EC-11): a blank to complete.
    #
    # v2.39 (GAP-2026-07-27-F). Gated on the question HAVING OPTIONS. Every NAT question
    # carries an answer-entry blank as a artefact of the current-era answer line, and
    # detect_blank_position() cannot tell that blank from a cloze gap in the stem.
    #
    # MEASURED (IIT_JAM_BIOTECHNOLOGY, 1719 Qs): FILL_BLANK fired on 218 of 261 NAT
    # questions (83.5%) against 37 of 1434 MCQ (2.6%) — a 32x enrichment that tracks the
    # answer mechanism, not the question form. The decisive control is batch 7: across
    # 300 legacy-era questions, which carry almost no NAT, FILL_BLANK moved by exactly 1.
    #
    # The axes are orthogonal so nothing downstream is corrupted TODAY, but the NAT
    # section's Axis-2 profile reads as ~100% cloze, and Step 7 rendering that literally
    # emits NAT stems as fill-in-the-blank.
    #
    # A NAT question with a genuine cloze stem is real but rare, and is not recoverable
    # from the artefact — it is deliberately classified by its residual form instead of
    # being asserted on evidence that cannot distinguish the two.
    if (opts and (q.get('blank_pos', 'none') not in ('none', None)
                  or re.search(r'_{3,}|\bfill in the blank', s))):
        return 'FILL_BLANK'
    # 6 — ODD_ONE_OUT: genuine "which does not belong" classification (narrowed — mere
    #     negative phrasing is is_negative, handled orthogonally, not this class).
    if re.search(r'\bodd one out\b|does not belong|which one is different|find the odd', s):
        return 'ODD_ONE_OUT'
    # 7 — DIRECT: residual floor.
    return 'DIRECT'

def tag_axes(q):
    """Attach the three exclusive axis labels to a question dict in place. is_negative is
    already set during extraction (EC-12). Idempotent."""
    q['axis1'] = classify_axis1(q)
    q['axis2'] = classify_axis2(q)
    q['axis3'] = classify_axis3(q)
    return q

# family keyword → family key (Step-5 approximation of Step 7 resolve_presentation_family;
# Step 7 refines with CONCEPT_GROUP at its S3-8 join. Exam-agnostic keyword sets.)
_FAMILY_KEYWORDS = {
    'vocab_single_word'    : ('antonym', 'synonym', 'spelling', 'homonym'),
    'one_word_substitution': ('one word substitution', 'one-word'),
    'idiom_phrase'         : ('idiom', 'phrase'),
    'fact_recall'          : ('gk', 'general awareness', 'general knowledge', 'static',
                              'current affairs', 'fact'),
}

def resolve_presentation_family_s5(subtopic, fmt):
    """Lightweight family resolution from the subtopic name + format. Returns a family key
    or None. Mirrors Step 7 PRESENTATION_FAMILIES; used only to seed axis2_capability —
    Step 7 remains authoritative once CONCEPT_GROUP is joined."""
    name = (subtopic or '').lower()
    for fam, kws in _FAMILY_KEYWORDS.items():
        if any(kw in name for kw in kws):
            return fam
    return None

def axis2_capability(observed_axis2, presentation_family, fmt):
    """The Axis-2 forms a subtopic may FAITHFULLY take (decisions (b)/(c)):
       observed ∪ family-menu ∪ {DIRECT}, with LINKED added iff the subtopic is
       stimulus-linked (format PASSAGE/DI) and removed otherwise. Forcing a form OUTSIDE
       this set is fabrication (Step 7 decision-(iii) ban)."""
    cap = set(observed_axis2) | {'DIRECT'}
    cap |= FAMILY_AXIS2_MENU.get(presentation_family, set())
    if str(fmt).upper() in ('PASSAGE', 'DI'):
        cap.add('LINKED')
    else:
        cap.discard('LINKED')
    return [c for c in AXIS2_CLASSES if c in cap]   # canonical ladder order

def compute_section_axis_distribution(sec_entries, progress, mocks_per_window=10,
                                      window_years=None):
    """CATEGORY A per-section target. Averages each axis's class counts PER PAPER over the
    N most-recent distinct years, and classifies each Axis-2 class band vs guarantee-only.
    Returns None for a section with no observed questions (all Zero-PYQ scaffolds).

    v2.26 — N is bc.AXIS_WINDOW_YEARS (5), raised from a hardcoded 3. Two separate
    questions must not share one sample:
      • HOW MANY of a class a mock gets  → this window (5 years). A wider window is a
        steadier average; on the reference exam the figural mean moved only 4.33 → 4.40,
        which is the point — the number should not lurch on one unusual paper.
      • WHICH subtopics may carry it     → the FULL corpus (figural_rate, below). Most
        subtopics appear 1-3 times per paper, so a 5-paper sample leaves their denominator
        far too small to rate; the reference exam's Population Genetics reads 0/8 over five
        years and 1/16 over twenty-two.

    The §S1-3 `get_detection_sample()` window stays at 3 ON PURPOSE and is NOT this
    constant: it detects the CURRENT PATTERN (option format, section layout, marking), and
    a layout that changed four years ago must not pollute today's reading of the paper.

    ERA-SCOPING STILL RUNS FIRST (frequency_scope == 'current-era', §14). A wider window
    can therefore never straddle a pattern change — it widens only WITHIN the current era.
    """
    import blueprint_core as bc
    window_years = int(window_years or bc.AXIS_WINDOW_YEARS)
    qs = []
    for e in sec_entries:
        qs.extend(progress.get((e['section'], e['topic'], e['subtopic']), []))
    if not qs:
        return None
    for q in qs:                                   # ensure tagged (idempotent)
        if 'axis2' not in q:
            tag_axes(q)
    years   = sorted({q.get('year') for q in qs if q.get('year')}, reverse=True)
    recentN = set(years[:window_years]) if years else set()
    rq      = [q for q in qs if q.get('year') in recentN] or qs
    n_papers = max(1, len({(q.get('year'), q.get('shift')) for q in rq}))

    def per_paper(axis):
        c = Counter(q.get(axis, '?') for q in rq)
        return {k: round(v / n_papers, 3) for k, v in c.items()}

    axis2 = per_paper('axis2')
    audit_mode = {}
    for cls, avg in axis2.items():
        if cls == 'DIRECT':
            audit_mode[cls] = 'float'              # residual filler — never audited (decision 5/10)
        else:
            audit_mode[cls] = 'band' if avg * mocks_per_window >= 1 else 'guarantee'
    # v2.44 — the raw per-paper figural counts and the per-subtopic totals, carried
    # through so Step 6 can build the target SERIES and the per-subtopic figure quota,
    # and so the auditor's band is this exam's own volatility. Without these the band is
    # a fixed percentage, which rejected four of the reference exam's five real papers.
    # PAPER KEY: str() everything. sorted() over a mixed {2026, None} set raises
    # TypeError in Python 3 ("'<' not supported between int and NoneType"), which is
    # reachable the moment ONE question in the corpus lacks a year or paper_id — a
    # scan gap, a hand-added question, a legacy row. That would take out the whole of
    # Step 5 for an entire exam. A missing key becomes its own bucket rather than a crash.
    def _paper_key(q):
        return str(q.get('paper_id') or q.get('year') or '__unknown__')

    # SUBTOPIC KEY: subtopic_id ONLY, never the display name. Step 7 matches these keys
    # against blueprint subtopic_ids; a display-name key matches NOTHING, so the mock
    # would silently render ZERO figures with every fixture green. Falling back to the
    # display name looks defensive and is the more dangerous failure — a hard skip of the
    # unkeyed question keeps the quota honest and is visible in the totals.
    # v2.46 — MEASURE EVERY STIMULUS CLASS, NOT JUST FIGURAL. v2.44/v2.45 measured
    # figures per paper and per subtopic and left DI and PASSAGE with a rate and nothing
    # else, so Step 6 could build the quota/series chain for FIGURAL only. On a DI-heavy
    # exam that means DI reaches its budget but ignores each subtopic's measured DI
    # frequency. Measuring per class costs one loop and lets a future class inherit the
    # whole chain rather than needing its own release.
    def _class_of(q):
        if q.get('image_role', 'none') != 'none':
            return 'FIGURAL'
        if q.get('linked_group_id'):
            return 'PASSAGE'
        if _looks_like_table_stimulus(q.get('stem', '')) or q.get('has_rendered_table'):
            return 'DI'
        return 'TEXT'

    # GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D2). These three lines are
    # MODULE-QUALIFIED — `collections.X`, not the bare `Counter` used everywhere
    # else in §5 — but `import collections` appears NOWHERE in this file. Every
    # other import is the `from collections import ...` form, which binds
    # `Counter` / `defaultdict` and never the module name; the sole
    # `import collections as _c` (§8) is function-local to another function.
    # So this function raised `NameError: name 'collections' is not defined`
    # every time it ran, from v2.46.0 (2026-08-06) onward. write_section_rules
    # calls it, so section_rules.md — the primary Step 5 artefact — was never
    # written.
    # WHY IT SURVIVED: spec_name_audit DID detect it. `collections` sits in
    # spec_name_audit_baseline.json under this file, accepted as a known unbound
    # name, so the ratchet reported OK. A baseline entry cannot distinguish "this
    # name is legitimately bound elsewhere at runtime" from "this name is a
    # guaranteed NameError" — see the typed-reason baseline added in this release.
    # The import is function-local, matching this file's dominant idiom.
    import collections
    _by_paper = collections.defaultdict(collections.Counter)   # cls -> paper -> n
    _by_sub = collections.defaultdict(collections.Counter)     # cls -> subtopic_id -> n
    _unkeyed = collections.Counter()                           # cls -> n
    for _q in rq:
        _c = _class_of(_q)
        if _c == 'TEXT':
            continue
        _by_paper[_c][_paper_key(_q)] += 1
        _sid = _q.get('subtopic_id')
        if _sid:
            _by_sub[_c][str(_sid)] += 1
        else:
            _unkeyed[_c] += 1
    _papers = sorted({_paper_key(_q) for _q in rq})
    _obs_by_class = {c: [_by_paper[c].get(p, 0) for p in _papers] for c in _by_paper}
    _mean_by_class = {c: (sum(v) / len(v) if v else 0.0) for c, v in _obs_by_class.items()}

    _fig_by_paper = _by_paper['FIGURAL']
    _fig_by_sub = _by_sub['FIGURAL']
    _fig_unkeyed = _unkeyed['FIGURAL']
    _per_paper = [_fig_by_paper.get(_p, 0) for _p in _papers]
    return {
        'figural_per_paper_observed' : _per_paper,                       # v2.44
        'figural_per_paper_mean'     : (sum(_per_paper) / len(_per_paper)) if _per_paper else 0.0,
        'figural_count_by_subtopic'  : dict(_fig_by_sub),                # v2.44
        # v2.46 — per-class views, consumed by derive_axis_schedule to build the
        # quota/series chain for EVERY stimulus class rather than FIGURAL alone.
        'per_paper_observed_by_class': {c: list(v) for c, v in _obs_by_class.items()},
        'per_paper_mean_by_class'    : dict(_mean_by_class),
        'count_by_subtopic_by_class' : {c: dict(v) for c, v in _by_sub.items()},
        'unkeyed_questions_by_class' : dict(_unkeyed),
        'figural_unkeyed_questions'  : _fig_unkeyed,   # v2.45 — figural questions with
                                                       # no subtopic_id, excluded from the
                                                       # quota. Non-zero means the corpus
                                                       # lost keys upstream; surfaced so a
                                                       # shortfall has a visible cause
                                                       # instead of looking like a bug here.
        'recent_years'    : sorted(recentN, reverse=True),
        'window_years'    : window_years,     # v2.26 provenance — Step 6 echoes this into
                                              # blueprint.axis_schedule.axis_window_years so
                                              # a target can always be traced to its sample.
        'n_papers_recent' : n_papers,
        'mocks_per_window': mocks_per_window,
        'axis1_per_paper' : per_paper('axis1'),
        'axis2_per_paper' : axis2,
        'axis3_per_paper' : per_paper('axis3'),
        'axis2_audit_mode': audit_mode,
        'negative_rate'   : round(sum(1 for q in rq if q.get('is_negative')) / len(rq), 3),
    }

# v2.44 — plain-majority threshold, both halves of the reducibility test (§S5-FIG).
# MODULE SCOPE deliberately: it is referenced inside synthesise_subtopic() before the
# line it was first written on, which is a NameError waiting for the first exam whose
# corpus reaches that branch. Not tunable per exam ON PURPOSE — a per-exam knob here is
# how an exemption rule gets quietly widened until it swallows the budget again.
FIGURAL_IRREDUCIBLE_RATE = 0.50


def synthesise_subtopic(section, topic, subtopic, questions, progress, figural_data=None,
                        nat_allowed=False):
    """
    BUG-A07 fix: progress added to function signature (cfg parameter removed — no config file).
    BUG-A10 fix: sub_format value ('Cloze' or 'RC') has no leading space.
    BUG-A13 fix: empty patterns from FIGURAL subtopics handled with placeholder.
    BUG-B09 fix: difficulty calibration stores is_inferred bool, not fragile string.
    BUG-B14 fix: figural subtopics with all-empty stems get placeholder pattern.
    BUG-B15 fix: §14 schema documents option_format as dict.
    """
    if not questions:
        return _absent_entry(section, topic, subtopic)

    mode     = determine_strip_mode(section, topic, subtopic)
    patterns = generate_templates(questions, mode)

    # BUG-A13 / BUG-B14 fix: handle empty patterns for figural or other edge cases
    if not patterns and questions:
        year_set = sorted(set(q.get('year') for q in questions if q.get('year')))
        patterns = [{
            'id':'P1', 'template':'(figural -- no text stem)',
            'frequency':100, 'raw_count':len(questions),
            'confidence':'observed', 'deprecated':False, 'years':year_set,
        }]

    # E-6: NOTE block analysis
    note_count  = sum(1 for q in questions if q.get('has_note'))
    notes_by_yr = {}
    for q in questions:
        if q.get('has_note') and q.get('year'):
            notes_by_yr.setdefault(q['year'], []).append(q.get('note_text',''))
    note_freq  = classify_note_frequency(note_count, len(questions))
    canon_note = canonical_note_text(notes_by_yr)

    for p in patterns:
        p['note_block'] = note_freq
        p['note_text']  = canon_note if note_freq in ('mandatory','conditional') else ''
        p['approach']   = infer_approach(p['template'], mode, subtopic)

    opt_fmt   = subtopic_option_format(questions)
    dg        = {'Simple':[],'Medium':[],'Hard':[]}
    for q in questions:
        dg[q.get('difficulty',{}).get('level','Medium')].append(q)
    # BUG-B09 fix: store is_inferred flag in calibration dict
    diff_cal  = {lv: build_diff_criteria(lv, qs, subtopic, mode) for lv, qs in dg.items()}
    wrong_opt = classify_wrong_option_structure(questions)

    neg_ct  = sum(1 for q in questions if q.get('is_negative'))
    blank_d = Counter(q.get('blank_pos','none') for q in questions).most_common(1)[0][0]
    sw      = [len(q['stem'].split()) for q in questions if q.get('stem')]
    # ── v2.26 (GAP-2026-08-06-AXIS1) — FIGURAL IS A RATE, NOT A FLAG ────────────────
    # WAS: has_img = any(q.get('image_role','none') != 'none' for q in questions)
    #
    # `any()` is an EXISTENTIAL quantifier with no denominator: ONE figural question
    # anywhere in a 22-year corpus stamped the subtopic FIGURAL permanently. Because
    # Step 7 read `format` as a RENDERING IMPERATIVE ("format==FIGURAL ⇒ draw a
    # picture"), that flag then forced a figure onto EVERY mock question the subtopic
    # ever received. Measured on the reference exam: 46 of 131 subtopics flagged,
    # holding 42.7% of allocation weight, against a true question-level figural rate
    # of 7.3% — and the delivered mocks carried 26 and 30 figures against a blueprint
    # budget of 4. Both passed every gate, because no gate counted.
    #
    # COUNT QUESTIONS, NOT IMAGES. A `stem_and_options` question contributes ONE to
    # figural_q_count and FIVE to images_analysed (one stem figure + four option
    # figures). The two fields answer different questions and must never be confused:
    #   figural_q_count  → HOW MANY QUESTIONS carry a figure   → drives the Axis-1 budget
    #   images_analysed  → HOW MANY IMAGES were inspected      → drives the figure PROFILE
    # Reading images_analysed as a question count inflates the reference corpus from
    # ~118 figural questions to 154 and biases every rate toward option-figure subtopics.
    #
    # `format` SURVIVES UNCHANGED for back-compat (~200 deployed exams read it, and the
    # GOLDEN RULE still forbids it from EXCLUDING anything). What changes is its meaning
    # downstream: from "always draw this" to "CAPABLE of being drawn this way". The new
    # figural_rate decides which capable questions actually claim the scarce budget.
    _fig_qs  = [q for q in questions if q.get('image_role', 'none') != 'none']
    figural_q_count     = len(_fig_qs)
    figural_denominator = len(questions)
    figural_rate = (figural_q_count / float(figural_denominator)) if figural_denominator else 0.0

    # REDUCIBILITY. A question whose OPTIONS are themselves images (organic structures,
    # circuit diagrams, spectra) cannot be rewritten as text without becoming
    # unanswerable, so it is granted a figure even over budget (bc.axis_grant_figural
    # rule 2). A stem-only figure usually CAN be replaced by an attested text question
    # from the same subtopic — which is what REPLACEMENT_RULE below is for.
    # ── v2.44 (GAP-2026-08-06-IRREDUCIBLE) — REDUCIBILITY IS A RATE, NOT AN any() ──
    # WAS: figural_reducible = not any(q.image_role in ('stem_and_options',...))
    #
    # THE SAME EXISTENTIAL DEFECT THIS FILE EXISTS TO FIX, ONE FIELD TO THE LEFT.
    # v2.26 replaced `has_img = any(...)` with a rate, and then decided reducibility
    # with a fresh any(). One question anywhere in a 22-year corpus made a subtopic
    # PERMANENTLY EXEMPT FROM THE FIGURAL BUDGET — and irreducible grants pass even
    # over budget by design, so the exemption silently became the budget.
    #
    # MEASURED ON THE REFERENCE EXAM (2026-08-06, first real PYQExtract run):
    #     21 of 133 subtopics marked irreducible, forcing a mean of 14.3 figures per
    #     mock against a budget of 5; 13 of 15 mocks over budget; worst mock 29.
    #     Complex Formation was exempt on 1 figural question in 32 (3.1%).
    #     Chemical Bonding on 1 in 24. Trigonometry on 1 in 15.
    #     ELEVEN of the 21 carried aggregate image_role 'stem_only' — the figure is in
    #     the stem and the options are TEXT, which is the REDUCIBLE case by definition.
    #     They were exempt anyway, because one minority question had image options.
    #
    # THE CORRECT TEST IS 'ARE THE OPTIONS USUALLY IMAGES', WHICH NEEDS A DENOMINATOR.
    # An exemption must earn itself twice over: the subtopic has to be figure-dominant
    # AT ALL (figural_rate), and its figures have to live in the OPTIONS rather than the
    # stem (option_image_rate). A stem figure with text options can nearly always be
    # replaced by an attested text question from the same subtopic; option figures —
    # organic structures, circuit diagrams, spectra — cannot, because the answer set
    # itself is pictorial.
    #
    # Thresholds tested against the reference exam's real 15-mock allocation:
    #     rule                                   irreducible   mean forced   over budget
    #     any()                     (v2.26)         21 / 133       14.3        13 / 15
    #     aggregate role only                       10 / 133        6.1         7 / 15
    #     rate>=0.50 AND option-majority (THIS)       3 / 133        1.5         0 / 15
    # The three survivors are Alcohols/Aldehydes (71% figural), Aromatic Compounds
    # (71%) and Carboxylic Acids (56%) — every one a case where the options ARE the
    # structures. 0.50 is the plain majority line, deliberately not a tuned constant.
    _opt_img = [q for q in _fig_qs
                if str(q.get('image_role', '')).strip() in ('stem_and_options', 'options_only')]
    option_image_rate = (len(_opt_img) / float(len(_fig_qs))) if _fig_qs else 0.0
    figural_reducible = not (figural_rate >= FIGURAL_IRREDUCIBLE_RATE
                             and option_image_rate >= FIGURAL_IRREDUCIBLE_RATE)

    has_img  = figural_q_count > 0
    has_pass = any(q.get('linked_group_id') for q in questions)

    # ── v2.43 (GAP-2026-08-06-DI) — DI IS A RATE TOO ────────────────────────────
    # `has_tbl` below is the SAME existential quantifier that produced the figural
    # defect: one table-bearing question anywhere in the corpus marks the subtopic DI
    # forever, with no denominator. Measured on the reference exam, Electrochemistry
    # (14 observed questions) and Matrices & Determinants (19) are both flagged DI on
    # roughly one table each. DI is less damaging than FIGURAL was — DI and TEXT share
    # a rendering path, so the flag never FORCED a table the way format=FIGURAL forced
    # an image — but the same rate belongs here for the same reasons: it ranks claims
    # on the Axis-1 DI budget, and it stops a 1-in-19 subtopic outranking a genuine one.
    _di_qs = [q for q in questions
              if _looks_like_table_stimulus(q.get('stem', ''))
              or q.get('has_rendered_table')]
    di_q_count = len(_di_qs)
    di_rate = (di_q_count / float(len(questions))) if questions else 0.0
    # A DI question whose data table IS the question (a computation over supplied
    # values) has no table-free form; one that merely tabulates prose does. Absent a
    # per-question signal the conservative reading is reducible — the stricter of the
    # two, since it lets the budget bind.
    di_reducible = True
    # v2.24.6 FIX C — delegates to the SAME structural/word-boundary table detector used
    # by the canonical classify_axis1() (SHARED AXIS CLASSIFIER v1.0, below) — was a
    # locally-duplicated naive substring match (`'table' in stem.lower()`), which
    # false-positived on "vege**table**", "accep**table**", "no**table**", etc. Single
    # source of truth now; both DI derivations can never drift apart again.
    # v2.45 — THE LAST EXISTENTIAL OF THIS FAMILY. `has_tbl = any(...)` is the same
    # construct that produced GAP-2026-08-06-AXIS1 (format) and GAP-2026-08-06-
    # IRREDUCIBLE (reducibility): ONE table-bearing question anywhere in a 22-year
    # corpus marked the whole subtopic DI. On the reference exam that put
    # Electrochemistry (1 table in 14) and Matrices & Determinants (1 in 19) into DI
    # permanently. DI was less damaging than FIGURAL only because DI and TEXT share a
    # rendering path, so the flag never FORCED a table — an accident of wiring, not a
    # property of the rule, and it would bite on the first DI-heavy exam (banking or
    # CAT-style aptitude) where the class carries real weight.
    #
    # `di_rate` is already computed above from the same predicate. Use it, with the same
    # plain-majority line the reducibility test uses, and require at least 2 observed
    # table questions so a lone outlier can never define a subtopic's format.
    # A subtopic below the line keeps its DI questions in the corpus and its di_rate for
    # ranking; it simply stops being DECLARED a DI subtopic. Nothing is dropped.
    has_tbl = (di_q_count >= 2 and di_rate >= FIGURAL_IRREDUCIBLE_RATE)
    fmt      = ('FIGURAL' if has_img else 'PASSAGE' if has_pass else
                'DI' if has_tbl else 'TEXT')

    # v2.22 — INHERENTLY-VISUAL OVERRIDE (keyword heuristic):
    # Some subtopics are inherently visual by definition (e.g. counting figures,
    # embedded figures, mirror images). If PYQ image extraction failed (scanned
    # PDF, missing media), has_img is False and fmt becomes TEXT — a misclassification.
    # This heuristic checks the subtopic name against a universal visual-keyword set
    # and overrides to FIGURAL when a match is found AND fmt is currently TEXT.
    # Exam-agnostic — keywords cover geometric/spatial/visual terms across all exams.
    _VISUAL_KEYWORDS = re.compile(
        r'(?i)\b(figure[s]?|figural|diagram[s]?|venn|'
        r'mirror\s+image[s]?|water\s+image[s]?|paper\s*fold(ing)?|'
        r'counting\s+(figure|triangle|shape)[s]?|embedded\s+figure[s]?|'
        r'completion\s+of\s+(figure|pattern)[s]?|dice|cube\s+fold(ing)?|'
        r'pattern\s+completion|image\s+series|visual\s+reasoning)\b')
    _inherently_visual = False
    if fmt == 'TEXT' and _VISUAL_KEYWORDS.search(subtopic):
        fmt = 'FIGURAL'
        _inherently_visual = True
        # v2.26 — this branch fires precisely when NO PYQ image was observed (extraction
        # failed, or the corpus is a scanned PDF), so the measured figural_rate is 0.0 and
        # the subtopic would rank LAST for the Axis-1 budget and never be drawn. But a
        # subtopic named "mirror images" or "paper folding" IS the figure — there is no
        # text form of it. Mark it irreducible so bc.axis_grant_figural() grants it
        # regardless of budget, and give it rate 1.0 so ranking treats it as the certainty
        # it is. Non-figural exams are untouched: the keyword set never matches them.
        figural_reducible = False
        figural_rate = 1.0
        if not figural_q_count:
            figural_q_count = figural_denominator
        # Assign a default figural_data with image_role='stem_only' (conservative:
        # most inherently-visual TEXT-classified subtopics have text options).
        # If PYQ data DID have figural info, it would have set has_img=True above,
        # so we only reach this branch when no PYQ images were observed at all.
        if not figural_data:
            figural_data = {
                'image_role': 'stem_only',
                'object_types': {'dominant': [], 'observed': [], 'avoid': []},
                'transformation_types': [],
                'arrangement_types': [],
                'complexity_dist': {},
                'images_analysed': 0,
                'images_unclear': 0,
            }
        print(f"  INHERENTLY-VISUAL override: '{subtopic}' TEXT→FIGURAL "
              f"(keyword match, image_role={figural_data.get('image_role', 'stem_only')})")
    # Allow explicit curator override via entry field (from taxonomy_draft or prior run):
    # figural_override=true forces FIGURAL; figural_override=false suppresses keyword match.
    # Checked via the 'questions' metadata: if ANY question in the PYQ set carries
    # a figural_override annotation, respect it. (Future: read from taxonomy_draft entry.)

    # BUG-A07 fix: progress now properly in scope via parameter
    q_nums  = {q['num'] for q in questions}
    lk_grps = [g for g in progress.get('_linked_groups',{}).values()
               if any(qn in q_nums for qn in g.get('q_numbers',[]))]
    lk_size = round(sum(len(g['q_numbers']) for g in lk_grps)/len(lk_grps)) \
              if lk_grps else 0

    # NEW (v2.3): max_per_paper + typical_per_paper from per-paper question counts
    paper_q_counts = Counter(q.get('paper_id', '?') for q in questions)
    pvals          = list(paper_q_counts.values())
    max_pp     = max(pvals)                           if pvals else 0
    typical_pp = round(sum(pvals) / len(pvals))       if pvals else 0

    # NEW (v2.3): recycled_datasets — stimuli appearing in >=2 different papers
    recycled = _detect_recycled_stimuli(questions)
    ctx_pool = extract_context_pool(questions, mode)
    if recycled:
        ctx_pool = ctx_pool or {}
        ctx_pool['recycled_datasets'] = recycled
        ctx_pool['ban_recycled']      = True

    # NEW (v2.5): per-subtopic MSQ aggregation → answer_cardinality (Step 7 dispatch unit).
    # Whole-subtopic mode: a subtopic is treated as uniformly single- or multi-answer.
    # A subtopic is 'multi' when a MAJORITY of its observed Qs are MSQ (>50%), so a
    # stray false-detect cannot flip a single-answer subtopic. msq_freq% is recorded
    # for transparency. Inert when multi_select_allowed=false (is_msq always False).
    msq_ct    = sum(1 for q in questions if q.get('is_msq'))
    msq_freq  = round(msq_ct / len(questions) * 100) if questions else 0
    answer_cardinality = 'multi' if msq_freq > 50 else 'single'

    # NEW (v2.8): per-subtopic NAT aggregation → answer_type (the SECOND dispatch axis).
    # A question is NAT when it has NO selectable options at all — neither text option
    # labels NOR option-images. The forgery-resistant signal is option SHAPE (zero options)
    # plus image_role: a NAT carries no option-images (image_role is 'none' for a text NAT
    # or 'stem_only' for a figural NAT — a problem diagram with a typed answer, per ND10),
    # whereas a figural MCQ carries option-images ('options_only'/'stem_and_options') and is
    # therefore NOT NAT. Gated on nat_allowed (PARAMETER 11) so the entire path is inert for
    # non-NAT exams: answer_type is always 'option' unless the exam pattern enables NAT.
    # Whole-subtopic majority (>50%) mirrors the MSQ aggregation, so a stray detect cannot
    # flip a subtopic. answer_type is ORTHOGONAL to answer_cardinality: a 'numerical'
    # subtopic's cardinality is moot (kept 'single' by convention).
    _OPT_IMG_ROLES = ('options_only', 'stem_and_options')
    nat_ct = sum(1 for q in questions
                 if len(q.get('options', [])) == 0
                 and q.get('image_role', 'none') not in _OPT_IMG_ROLES)
    nat_freq    = round(nat_ct / len(questions) * 100) if questions else 0
    answer_type = 'numerical' if (nat_allowed and nat_freq > 50) else 'option'

    # v2.23 THREE-AXIS (CATEGORY B): this subtopic's observed Axis-2 distribution + the
    # capability set Step 6/7 read. Every question is tagged by tag_axes() at extraction;
    # the guard below re-tags defensively if `questions` came from a loaded/pre-v2.23
    # progress json (idempotent — otherwise observed_axis2 would collapse to all-DIRECT).
    for q in questions:
        if 'axis2' not in q:
            tag_axes(q)
    observed_axis2 = dict(Counter(q.get('axis2', 'DIRECT') for q in questions))
    pres_family    = resolve_presentation_family_s5(subtopic, fmt)
    axis2_cap      = axis2_capability(observed_axis2.keys(), pres_family, fmt)

    return {
        'subtopic'               : subtopic,
        'section'                : section,
        'topic'                  : topic,
        'observed_count'         : len(questions),
        'format'                 : fmt,
        'option_format'          : opt_fmt,   # BUG-B15/C04: full dict, see format_entry
        'OMML_required'          : any(q.get('omml_present') for q in questions),
        'negative_question_freq' : round(neg_ct / len(questions) * 100),
        'answer_type'            : answer_type,   # v2.8: 'option'|'numerical' (NAT axis)
        'nat_freq'               : nat_freq,      # v2.8: % of observed Qs that are NAT
        'answer_cardinality'            : answer_cardinality,   # v2.5: 'single'|'multi' (Step 7 dispatch)
        'msq_freq'               : msq_freq,      # v2.5: % of observed Qs that are MSQ
        'observed_axis2'         : observed_axis2, # v2.23: {AXIS2_CLASS: count} this subtopic
        'presentation_family'    : pres_family,    # v2.23: family key (Step 7 menu source)
        'axis2_capability'       : axis2_cap,      # v2.23: forms this subtopic may faithfully take
        'fill_in_blank'          : blank_d,
        'linked_group_size'      : lk_size,
        'max_per_paper'          : max_pp,
        'typical_per_paper'      : typical_pp,
        'stem_word_count'        : {'min':(min(sw) if sw else 0),
                                     'max':(max(sw) if sw else 0),
                                     'typical':round(sum(sw)/len(sw)) if sw else 0},
        'sub_type_label'         : subtopic,
        'PYQ_STEM_PATTERNS'      : patterns,
        'PYQ_DIFFICULTY_CALIBRATION': diff_cal,
        'wrong_option_structure' : wrong_opt,
        'PYQ_NUMBER_RANGES'      : extract_number_ranges(questions, mode),
        'PYQ_CONTEXT_POOL'       : ctx_pool,
        'PYQ_IMAGE_ANALYSIS'     : figural_data,
        'PYQ_PASSAGE_STRUCTURE'  : extract_passage_structure(questions) if has_pass else None,
        'inherently_visual'      : _inherently_visual,   # v2.22: True if keyword heuristic fired
        # v2.26 (GAP-2026-08-06-AXIS1) — the three fields that turn `format` from an
        # imperative into an eligibility flag. Additive: a consumer that ignores them
        # behaves exactly as before, which is what keeps ~200 exams working un-remeasured.
        'figural_q_count'        : figural_q_count,      # QUESTIONS with a figure (not images)
        'figural_denominator'    : figural_denominator,  # observed questions in this subtopic
        'figural_rate'           : round(figural_rate, 4),  # ranks claims on the Axis-1 budget
        'figural_reducible'      : figural_reducible,    # False ⇒ options ARE images ⇒ never
                                                         # downgrade to text (unanswerable)
        'option_image_rate'      : round(option_image_rate, 4),   # v2.44 — the DENOMINATOR
                                                         # the old any() threw away; makes
                                                         # every exemption auditable
        # v2.43 — DI counterparts. Same contract, same absent-safe defaults.
        'di_q_count'             : di_q_count,           # QUESTIONS with a data table
        'di_rate'                : round(di_rate, 4),    # ranks claims on the DI budget
        'di_reducible'           : di_reducible,
    }

def _detect_recycled_stimuli(questions):
    """
    NEW (v2.3): Detect linked-group stimuli that appear in >=2 different PYQ papers.
    When the same passage/puzzle/table appears across multiple papers it is a recycled
    dataset — Step 7 must not reproduce it verbatim.
    Returns list of short identifying descriptors (first 12 words of stimulus).
    Called from synthesise_subtopic; result written to PYQ_CONTEXT_POOL.
    """
    stim_papers = {}  # normalised_key → set of paper_ids
    for q in questions:
        if not q.get('linked_group_id'):
            continue
        words = q.get('stem', '').split()
        key   = ' '.join(words[:12]).lower().strip()
        if len(key) < 20:
            continue   # too short to be a meaningful stimulus identifier
        pid = q.get('paper_id', '?')
        stim_papers.setdefault(key, set()).add(pid)
    # Return descriptors for stimuli seen in 2+ distinct papers
    return [key[:80] for key, pids in stim_papers.items() if len(pids) >= 2]


def _absent_entry(section, topic, subtopic):
    _fam = resolve_presentation_family_s5(subtopic, 'TEXT')   # v2.23
    return {
        'subtopic':subtopic,'section':section,'topic':topic,'observed_count':0,
        'format':'TEXT',
        'option_format':{'primary':'single_value','recent_format':'single_value',
                         'changed_recently':False,'all_observed':[]},
        'OMML_required':False,'negative_question_freq':0,'fill_in_blank':'none',
        'answer_type':'option','nat_freq':0,           # v2.8: no PYQ → assume option-type
        'answer_cardinality':'single','msq_freq':0,   # v2.5: no PYQ → assume single-answer
        'linked_group_size':0,'max_per_paper':0,'typical_per_paper':0,
        'stem_word_count':{'min':0,'max':0,'typical':0},
        'sub_type_label':subtopic,
        'concept_group': None,        # v2.24.1 (D8): stamped later by stamp_mechanic_axes()
        'question_mechanic': None,    # v2.24.1 (D8)
        'form_key': None,             # v2.24.1 (D8)
        'collision_domain': None,     # v2.24.1 (D8)
        'PYQ_STEM_PATTERNS':[{'id':'P1','template':'(no PYQ observed)','approach':'(unknown)',
                               'frequency':100,'raw_count':0,'confidence':'absent',
                               'deprecated':False,'years':[],'note_block':'never','note_text':''}],
        'PYQ_DIFFICULTY_CALIBRATION':{
            'Simple':{'criteria':'(inferred)','is_inferred':True},
            'Medium':{'criteria':'(inferred)','is_inferred':True},
            'Hard':  {'criteria':'(inferred)','is_inferred':True}},
        'wrong_option_structure':{'type':'varied','description':'No PYQ data'},
        'PYQ_NUMBER_RANGES':None,'PYQ_CONTEXT_POOL':None,
        'PYQ_IMAGE_ANALYSIS':None,'PYQ_PASSAGE_STRUCTURE':None,
        'inherently_visual':False,   # v2.22: no PYQ → cannot determine; default False
        # v2.23: no PYQ → no observed Axis-2; capability = family menu ∪ {DIRECT} so a
        # Zero-PYQ subtopic is still a usable format-elastic filler for Step 7 (decision 11).
        'observed_axis2':{}, 'presentation_family':_fam,
        'axis2_capability':axis2_capability([], _fam, 'TEXT'),
    }

def build_diff_criteria(level, qs, subtopic, mode):
    """BUG-B09 fix: returns dict with is_inferred bool, not fragile string."""
    if not qs:
        return {'criteria':f'(inferred -- no {level} Qs observed in PYQ)',
                'is_inferred':True}
    sc   = [q.get('difficulty',{}) for q in qs[:3]]
    avgC = round(sum(s.get('C',1) for s in sc)/len(sc), 1)
    avgV = round(sum(s.get('V',1) for s in sc)/len(sc), 1)
    ex   = qs[0]['stem'][:80] if qs[0].get('stem') else '(no example)'
    return {'criteria': f'C~{avgC} steps, V~{avgV} complexity. Example: "{ex}..."',
            'is_inferred': False}

def infer_approach(template, mode, subtopic):
    t = template.lower(); u = subtopic.lower()
    if mode == 'quantitative':
        if 'interest' in u or '_p_' in t: return 'Apply SI/CI formula'
        if 'profit' in u:                  return 'Apply profit/loss formula'
        if 'speed' in t or 'distance' in t:return 'Apply speed-distance-time formula'
        return 'Solve using relevant arithmetic formula'
    elif mode == 'reasoning':
        if 'coded as' in t or 'written as' in t: return 'Decode substitution pattern'
        if 'related to' in t: return 'Find operation A->B, apply same to C'
        return 'Apply logical reasoning pattern'
    elif mode == 'factual':
        if 'who' in t:    return 'Identify person from contextual clues'
        if '_year_' in t: return 'Recall year of event'
        return 'Recall factual information'
    elif mode == 'english':
        if 'synonym' in u: return 'Select semantically equivalent word'
        if 'antonym' in u: return 'Select semantically opposite word'
        return 'Apply English language rule'
    elif mode == 'logical':
        return 'Evaluate statement-conclusion pairs using syllogism rules'
    return 'Apply appropriate strategy'

def extract_number_ranges(questions, mode):
    if mode != 'quantitative': return None
    # BUG-A14 fix: non-raw string so \u20b9 is actual ₹ character
    VAR_PATS = [
        ('P',   '\u20b9\\s*([\\d,]+)'),
        ('R',   r'(\d+(?:\.\d+)?)%'),
        ('T',   r'(\d+)\s*(?:years?|months?)'),
        ('NUM', r'\b(\d+)\b'),
    ]
    var_vals = {}
    for q in questions:
        for var, pat in VAR_PATS:
            for m in re.finditer(pat, q.get('stem',''), re.IGNORECASE):
                try: var_vals.setdefault(var,[]).append(int(m.group(1).replace(',','')))
                except: pass
    if not var_vals: return None
    from math import gcd
    from functools import reduce
    result = {}
    for var, vals in var_vals.items():
        gcf = reduce(gcd, vals[:10]) if len(vals) >= 2 else vals[0]
        result[var] = {'min':min(vals),'max':max(vals),'multiples_of':gcf,
                       'notes':f'n={len(vals)} observed'}
    return result

def extract_context_pool(questions, mode):
    if mode != 'quantitative': return None
    CTXS = [
        (r'\bborrow|lend|loan\b','loan'),
        (r'\bbank|deposit|savings\b','bank_deposit'),
        (r'\bshop|sell|buy|profit\b','retail_trade'),
        (r'\btrain|speed|distance\b','speed_distance'),
        (r'\bpipe|cistern|tank\b','pipes_cisterns'),
        (r'\bwork|days|complete\b','work_time'),
        (r'\bscheme|invest\b','investment'),
    ]
    counts = Counter()
    for q in questions:
        for pat, label in CTXS:
            if re.search(pat, q.get('stem',''), re.IGNORECASE): counts[label] += 1
    if not counts: return None
    tot = len(questions)
    return {'dominant':[c for c,n in counts.items() if n/tot>0.20],
            'common'  :[c for c,n in counts.items() if 0.05<=n/tot<=0.20],
            'rare'    :[c for c,n in counts.items() if 0<n/tot<0.05],
            'avoid'   :[]}

def extract_passage_structure(questions):
    """
    BUG-A10 fix: 'Cloze' without leading space.
    BUG-C05/v2.3: paragraph_count estimated from avg word count;
                  topic_domains populated from content keyword matching.
    """
    linked = [q for q in questions if q.get('linked_group_id')]
    if not linked: return None
    words  = [len(q.get('stem','').split()) for q in linked]
    qtypes = Counter()
    for q in linked:
        s = q.get('stem','').lower()
        if any(kw in s for kw in ['suggest','imply','infer','conclude']): qtypes['inference'] += 1
        elif any(kw in s for kw in ['according','states','passage']):      qtypes['direct']    += 1
        elif any(kw in s for kw in ['meaning','synonym','vocabulary']):    qtypes['vocab']     += 1
        elif any(kw in s for kw in ['blank','fill','appropriate']):        qtypes['grammar']   += 1
        else:                                                                qtypes['direct']    += 1
    tot  = sum(qtypes.values()) or 1
    dist = {k:round(v/tot*100) for k,v in qtypes.items()}
    has_cloze = any('blank' in q.get('stem','').lower() for q in linked)

    # Estimate paragraph_count from average stimulus word count
    # (typical prose: ~80 words/paragraph; Cloze: 1-2 paragraphs)
    avg_words = round(sum(words) / len(words)) if words else 0
    est_paras = max(1, round(avg_words / 80)) if not has_cloze else max(1, round(avg_words / 120))

    # Detect topic domains from stimulus content (exam-agnostic keyword matching)
    # These are the most common passage domain categories across competitive exams.
    DOMAIN_MAP = [
        (['science','technology','research','experiment','discovery','innovation'],'science_technology'),
        (['social','society','community','culture','tradition','diversity'],'social_issues'),
        (['environment','ecology','climate','biodiversity','conservation','pollution'],'environment'),
        (['economy','economic','finance','trade','market','gdp','inflation'],'economy'),
        (['history','ancient','medieval','civilization','empire','dynasty'],'history'),
        (['health','medicine','disease','body','nutrition','mental','therapy'],'health_medicine'),
        (['education','school','learning','student','knowledge','pedagogy'],'education'),
        (['philosophy','ethics','morality','consciousness','value','virtue'],'philosophy'),
        (['governance','policy','government','law','constitution','democracy'],'governance'),
        (['sport','game','athletic','champion','competition','tournament'],'sports'),
        (['literature','poetry','novel','author','narrative','character'],'literature'),
        (['art','music','painting','sculpture','aesthetic','creative'],'arts'),
    ]
    all_stems = ' '.join(q.get('stem','').lower() for q in linked[:5])
    observed_domains = [label for keywords, label in DOMAIN_MAP
                        if any(kw in all_stems for kw in keywords)]

    return {'sub_format'         : 'Cloze' if has_cloze else 'RC',
            'word_range'         : {'min':(min(words) if words else 0),'max':(max(words) if words else 0)},
            'paragraph_count'    : {'typical': est_paras},
            'topic_domains'      : {'observed': observed_domains, 'avoid': []},
            'q_type_distribution': dist}

# ═══ FROM Framework_MockTestAnalyse.md §5, fence L3618-5667 (v2.53.2) — VERBATIM ═══
def _compute_structural_changes(entries):
    """
    NEW (v2.3): Compute observable year-over-year structural changes from PYQ data.
    Returns list of strings for STRUCTURAL_CHANGES_BY_YEAR block.
    All conclusions are DATA-DRIVEN — zero hardcoding.
    Detects: subtopics removed in recent years, new subtopics, DI format shifts,
             FIGURAL elimination, format type changes.
    Called by write_section_rules.
    """
    changes = []

    # Collect global year range from all pattern years lists
    all_years = sorted(set(
        y for e in entries
        for p in e.get('PYQ_STEM_PATTERNS', [])
        for y in p.get('years', [])
        if isinstance(y, int)
    ), reverse=True)

    if not all_years:
        return changes   # no year data — cannot compute changes

    max_year = all_years[0]

    for e in entries:
        subtopic = e['subtopic']
        years_seen = sorted(set(
            y for p in e.get('PYQ_STEM_PATTERNS', [])
            for y in p.get('years', []) if isinstance(y, int)
        ))
        if not years_seen:
            continue

        last_seen = max(years_seen)
        first_seen = min(years_seen)

        # Subtopic absent from most recent year and last seen 2+ years ago → REMOVED
        if last_seen < max_year - 1:
            changes.append(
                f'  {subtopic} (format={e["format"]}): '
                f'last seen {last_seen} — likely REMOVED after {last_seen}'
            )

        # Subtopic appears only in last 1-2 years → NEW
        elif first_seen >= max_year - 1 and len(years_seen) <= 2:
            changes.append(
                f'  {subtopic} (format={e["format"]}): '
                f'first seen {first_seen} — NEW subtopic'
            )

        # v2.15 BUG-D10 fix: only emit FIGURAL-eliminated if not already flagged as REMOVED
        # (a REMOVED FIGURAL subtopic would otherwise produce two entries).
        if (e.get('format') == 'FIGURAL' and e.get('observed_count', 0) == 0
                and not (last_seen < max_year - 1)):
            changes.append(
                f'  {subtopic} (FIGURAL): observed_count=0 '
                f'— FIGURAL format appears eliminated for this subtopic'
            )

        # DI: single-Q format (linked_group_size <= 1) — may indicate format shift
        if e.get('format') == 'DI' and e.get('linked_group_size', 0) <= 1 and e.get('observed_count', 0) > 0:
            changes.append(
                f'  {subtopic} (DI): linked_group_size={e["linked_group_size"]} '
                f'— single-Q DI format observed (previously multi-Q)'
            )

    return changes


# ══════════════════════════════════════════════════════════════════════════════
# v2.24.1 MECHANIC / FORM-KEY ENGINE  (permanent, EXAM-INDEPENDENT fix for the
#                                      BV-10a form_key-collision HALT class)
# ------------------------------------------------------------------------------
# THREE AXES, THREE GRANULARITIES. They are NOT the same variable.
#   family / concept_group  — COARSE. May be shared. Feeds BV-10b (SOFT cap).
#   question_mechanic       — SEMANTIC FORM. May be shared. Feeds Step 7 CHECK D.
#   form_key                — IDENTITY. MUST be unique per collision_domain.
#                             Feeds BV-10a (HARD cap = 1, not configurable).
#
# v2.24 collapsed all three onto `family` whenever no qualifier was found — which,
# because _QUALIFIERS is a reasoning-domain vocabulary, is ALWAYS the case on a
# subject-knowledge exam. Any two subtopics sharing a _FAMILY_MAP keyword then got
# an IDENTICAL form_key, and Step 6 BV-10a HALTed two steps later. This is not
# exam-specific: it is latent in EVERY single-section subject exam. See the
# v2.24.1 defect report (D1..D9).
#
# v2.24.1 relocates the uniqueness guarantee from an ACCIDENT (a reasoning
# qualifier happening to match the name) to a CONSTRUCTION: form_key derives from
# the subtopic's own identity base, which bottoms out at the unique subtopic_id.
# It scopes the keyword table by a per-exam `template_sets` declaration, derives +
# stamps every axis exactly ONCE after id minting, and asserts form_key uniqueness
# BEFORE any artifact is written. The failure mode (defective manifest promoted,
# HALT two steps later) is therefore impossible for any exam: the worst case is a
# LOUD Step-5 FAIL naming the offending ids, never a silent downstream HALT.
#
# EXAM-INDEPENDENCE: the engine is identical for every exam. The ONLY per-exam
# input is [ExamCode]_mechanic_overrides.json. Absent file ⇒ legacy family
# selection (REGR-1) PLUS the SPEC-1 uniqueness improvement, which is always on.

def canon_text(s):
    """NFC + casefold + hyphen/slash/ampersand->space + collapse whitespace. Never raises."""
    import re, unicodedata
    s = unicodedata.normalize('NFC', (s or ''))
    for ch in ('—','–','-','/','&'):
        s = s.replace(ch, ' ')
    s = s.casefold().strip()
    return re.sub(r'\s+', ' ', s)

def _has_word(text, kw):
    """Word-boundary containment; allows only simple plural (s/es), never arbitrary
    continuation. 'voice' does NOT match 'invoice'; 'clock' does NOT match 'clockwise';
    but 'antonym' DOES match 'antonyms'. EC-M12: plural suffix applies to the FINAL
    token of a multi-word keyword too."""
    import re
    if ' ' in kw:
        head, _, tail = kw.rpartition(' ')
        pat = r'(?<!\w)' + re.escape(head) + r'\s+' + re.escape(tail) + r'(?:e?s)?(?!\w)'
        return re.search(pat, text) is not None
    return re.search(r'\b'+re.escape(kw)+r'(?:e?s)?\b', text) is not None

# Minimal, extensible transliteration for common Hindi verbal/reasoning terms so a
# pure-Devanagari name never collapses to '' for the FAMILY axis (never for form_key).
_HI_MAP = {
    'पर्यायवाची':'synonym',
    'विलोम':'antonym',
    'मुहावरे':'idiom','मुहावरा':'idiom',
    'श्रृंखला':'series','शृंखला':'series',
    'सादृश्य':'analogy','वर्गीकरण':'classification',
    'कोडिंग':'coding_decoding','दिशा':'direction_sense',
    'वर्तनी':'spelling',
}
def _translit_hint(raw):
    for k,v in _HI_MAP.items():
        if k in (raw or ''):
            return v
    return None

_VERBAL_SECTION_HINTS = ('english','verbal','language','comprehension','hindi',
                         'हिंदी','भाषा')
def _is_verbal(section, fmt):
    """v2.24.1: DEMOTED. It may only NARROW a declared template set (advisory), never
    WIDEN one. Its old ability to enable the verbal table for any TEXT exam (the D2
    defect) is gone — the verbal table now fires only when the exam DECLARES 'verbal'
    in template_sets AND this returns True."""
    sec = canon_text(section)
    if any(h in sec for h in _VERBAL_SECTION_HINTS):
        return True
    return (fmt or 'TEXT').upper() in ('TEXT','PASSAGE')

# ── Per-exam overrides loader (SPEC-2 / SPEC-6; EC-M17 exam_code, EC-M18 malformed) ──
_OVERRIDES = None
_MERGE_LOG = []          # populated by apply_subtopic_merges(); read by write_analysis_summary()

def load_mechanic_overrides(exam_code):
    """Discovery: /mnt/project/, then /mnt/user-data/uploads/.
    Absent               → all defaults (legacy family selection; SPEC-1 still applies).
    Present + malformed  → FAIL (EC-M18).  exam_code mismatch → FAIL (EC-M17)."""
    global _OVERRIDES
    if _OVERRIDES is not None:
        return _OVERRIDES
    _OVERRIDES = {'template_sets': None, 'template_sets_by_section': {},
                  'subtopic_overrides': {}, 'subtopic_merges': []}
    for d in ('/mnt/project/', '/mnt/user-data/uploads/'):
        path = os.path.join(d, f'{exam_code}_mechanic_overrides.json')
        if not os.path.exists(path):
            continue
        try:
            with io_open_utf8(path) as fh:
                data = json.load(fh)
        except json.JSONDecodeError as ex:
            raise SystemExit(f'FAIL: {path} is not valid JSON — {ex}')                 # EC-M18
        if data.get('exam_code') != exam_code:                                          # EC-M17
            raise SystemExit(f"FAIL: {path} declares exam_code={data.get('exam_code')!r}, "
                             f"expected {exam_code!r}")
        _valid = {'verbal','reasoning'}
        bad = set(data.get('template_sets') or []) - _valid                             # OV-5
        if bad:
            raise SystemExit(f"FAIL: {path} template_sets has unknown values {sorted(bad)}")
        for _sec, _sets in (data.get('template_sets_by_section') or {}).items():         # OV-5b
            _badsec = set(_sets or []) - _valid
            if _badsec:
                raise SystemExit(f"FAIL: {path} template_sets_by_section[{_sec!r}] has "
                                 f"unknown values {sorted(_badsec)} (check case/whitespace)")
        _OVERRIDES.update(data)
        break
    return _OVERRIDES

def io_open_utf8(path):
    import io as _io
    return _io.open(path, encoding='utf-8')

# ── The keyword table. Rows are 3-tuples now: (keywords, family, template_set). ──
#    Every former verbal_only=True row is 'verbal'; every former False row is
#    'reasoning'. A row fires only if its template_set is declared for the exam.
_FAMILY_MAP = [
    (['synonym','similar in meaning','nearest in meaning'], 'synonym', 'verbal'),
    (['antonym','opposite in meaning','opposite meaning'],  'antonym', 'verbal'),
    (['one word substitution','one word substitute'],       'one_word_substitution', 'verbal'),
    (['idiom','phrasal verb'],                              'idiom', 'verbal'),
    (['cloze'],                                             'cloze_test', 'verbal'),
    (['fill in the blank','fill in the blanks','sentence completion'], 'fill_in_blank', 'verbal'),
    (['spelling','correctly spelt','misspelt'],             'spelling', 'verbal'),
    (['grammatical error','error detection','spotting error','find the error'], 'error_detection', 'verbal'),
    (['sentence improvement','sentence correction','best improves'], 'sentence_improvement', 'verbal'),
    (['voice','active voice','passive voice'],              'voice', 'verbal'),
    (['narration','direct speech','indirect speech','reported speech'], 'narration', 'verbal'),
    (['para jumble','sentence rearrangement','sentence order'], 'para_jumble', 'verbal'),
    (['reading comprehension'],                            'reading_comprehension', 'verbal'),
    (['series'],                                           'series', 'reasoning'),
    (['analogy'],                                          'analogy', 'reasoning'),
    (['classification','odd one out','odd pair','does not belong'], 'classification', 'reasoning'),
    (['coding','decoding'],                                'coding_decoding', 'reasoning'),
    (['blood relation','family relation'],                 'blood_relation', 'reasoning'),
    (['direction'],                                        'direction_sense', 'reasoning'),
    (['seating','arrangement','puzzle'],                   'arrangement', 'reasoning'),
    (['syllogism','statement conclusion','statement assumption','course of action','logical deduction'], 'syllogism', 'reasoning'),
    (['mirror image'],                                     'mirror_image', 'reasoning'),
    (['water image'],                                      'water_image', 'reasoning'),
    (['paper folding','paper cutting'],                    'paper_folding', 'reasoning'),
    (['embedded figure','hidden figure'],                  'embedded_figure', 'reasoning'),
    (['venn diagram'],                                     'venn_diagram', 'reasoning'),
    (['dice','cube'],                                      'dice', 'reasoning'),
    (['missing number','number matrix','number grid'],     'missing_number', 'reasoning'),
    (['calendar'],                                         'calendar', 'reasoning'),
    (['clock'],                                            'clock', 'reasoning'),
    (['data interpretation','bar graph','pie chart','line graph','tabulation'], 'data_interpretation', 'reasoning'),
    (['current affairs'],                                  'current_affairs', 'reasoning'),
    (['static gk','static general knowledge'],             'static_gk', 'reasoning'),
]
_QUALIFIERS = ['alphanumeric','symbolic','semantic','number','numeric','numerical',
               'letter','alphabet','word','figural','figure','spatial',
               'linear','circular','floor','matrix','wheel','triangle','substitution']
_QUALIFIABLE = {'series','analogy','classification','coding_decoding','missing_number',
                'arrangement','mirror_image','paper_folding','embedded_figure'}
_ALL_FAMILY_NAMES = {fam for _, fam, _ in _FAMILY_MAP}
_TEMPLATE_SET     = {fam: ts for _, fam, ts in _FAMILY_MAP}

def _identity_base(display_name, subtopic_id):
    """SPEC-1 / EC-M2. The collision-safe identity root. ONE recipe, ONE call site.
    A fully non-Latin name slugifies to '' and must still yield a stable, unique,
    call-site-independent value. Ultimately bottoms out at the unique subtopic_id."""
    import hashlib as _hl
    return (slugify(display_name)
            or slugify(subtopic_id)
            or ('u_' + _hl.md5((display_name or '').encode('utf-8')).hexdigest()[:8]))

def _redundant(qual, base):
    """EC-M13: word-boundary test, not substring. 'number' is redundant against base
    'missing_number' only if it appears there as a whole token."""
    return _has_word(base.replace('_', ' '), qual)

def _extract_qualifiers(name_c):
    """EC-M14: ALL matching qualifiers, canonical (alphabetical) order — order-independent."""
    import re
    return tuple(sorted(re.sub(r'\s+', '_', q) for q in _QUALIFIERS if _has_word(name_c, q)))

def _allowed_template_sets(section, ov):
    allowed = ov.get('template_sets_by_section', {}).get(section, ov.get('template_sets'))
    if allowed is None:
        allowed = ['verbal', 'reasoning']            # ABSENT ⇒ legacy behaviour (REGR-1)
    return allowed

def derive_mechanic(section, subtopic, sub_type_label=None, templates='',
                    fmt='TEXT', subtopic_id=None, prefix_overrides=None):
    """Returns {family, mechanic, form_key, collision_domain}.
    PRECONDITION: subtopic_id is the FINAL, de-duplicated, minted id (EC-M3)."""
    import re
    ov       = _OVERRIDES or {}
    raw_name = subtopic or sub_type_label or ''
    name_c   = canon_text(raw_name + ' ' + (sub_type_label or ''))
    base     = _identity_base(raw_name, subtopic_id)
    domain   = section_prefix(section, prefix_overrides) or 'default'    # SPEC-3 / EC-M4
    allowed  = _allowed_template_sets(section, ov)                       # SPEC-2 / EC-M6

    def _match(hay):
        for kws, fam, tset in _FAMILY_MAP:
            if tset not in allowed:                                 continue
            if tset == 'verbal' and not _is_verbal(section, fmt):   continue   # advisory NARROW only
            if any(_has_word(hay, kw) for kw in kws):
                return fam
        return None

    # COARSE axis. NAME is authoritative. Templates rescue ONLY a name with no
    # alphanumeric content at all (never merely "a name that matched nothing").
    family = _match(name_c) if name_c.strip() else None
    if family is None and not re.search(r'[a-z0-9]', name_c):
        family = _match(canon_text(templates))
    if family is None:
        family = _translit_hint(raw_name)                           # EC-M2: family ONLY
    if family is None:
        family = base                                               # coarse identity == the name

    # FINE axis. SPEC-1: starts from the NAME/id base, NEVER from the family token.
    quals    = _extract_qualifiers(name_c) if family in _QUALIFIABLE else ()
    suffix   = '__'.join(q for q in quals if not _redundant(q, base))   # EC-M13 / EC-M14
    form_key = f'{base}__{suffix}' if suffix else base

    # Explicit curator override wins over everything (applied per subtopic_id).
    per      = ov.get('subtopic_overrides', {}).get(subtopic_id or '', {})
    family   = per.get('concept_group',     family)
    form_key = per.get('form_key',          form_key)
    mechanic = per.get('question_mechanic', form_key)               # v2.24.1: mechanic == form_key

    return {'family': family, 'mechanic': mechanic,
            'form_key': form_key, 'collision_domain': domain}

def mint_subtopic_ids(entries, exam_meta=None):
    """v2.24.1: mint the canonical, collision-safe subtopic_id for every entry, IDEMPOTENTLY
    (an entry that already carries an id is left untouched). Called from run_synthesise()
    BEFORE merges/stamp/QV so the gate and every writer read the SAME id. write_section_rules()
    also calls it as a no-op guard."""
    pov  = (exam_meta or {}).get('section_prefix_overrides', {})
    pmap = build_section_prefix_map(sorted({e['section'] for e in entries}), pov)
    seen = {}
    for e in entries:
        if e.get('subtopic_id'):
            seen[e['subtopic_id']] = (e['section'], e['topic'], e['subtopic'])
    for e in entries:
        if e.get('subtopic_id'):
            continue
        sid = make_subtopic_id(e['section'], e['topic'], e['subtopic'], pmap)
        base = sid; n = 2
        key = (e['section'], e['topic'], e['subtopic'])
        while sid in seen and seen[sid] != key:
            sid = f'{base}_{n}'; n += 1
        seen[sid] = key
        e['subtopic_id'] = sid
    return entries

def apply_subtopic_merges(entries, exam_code):
    """D7 / SPEC-7. TRUE-duplicate merge (NOT an allowlist). Each group of >=2 subtopic_ids
    is collapsed into the FIRST member; the others are dropped. Members must share a section
    (OV-3). Runs AFTER id minting, BEFORE stamp/QV. Records every drop in _MERGE_LOG so
    write_analysis_summary() can emit the mandatory '## MERGED SUBTOPICS' section (a merge
    removes a subtopic_id that Steps 6/7 join on — the curator must see what disappeared)."""
    global _MERGE_LOG
    _MERGE_LOG = []
    ov = load_mechanic_overrides(exam_code)
    groups = ov.get('subtopic_merges', []) or []
    if not groups:
        return entries
    by_id = {e.get('subtopic_id'): e for e in entries}
    drop  = set()
    _across = {}                                                                     # id -> group index
    for _gi, _grp in enumerate(groups):                                              # OV-4b: groups disjoint
        for _g in _grp:
            if _g in _across:
                raise SystemExit(f"FAIL: subtopic_merges: {_g!r} appears in two groups "
                                 f"({groups[_across[_g]]} and {_grp}); groups must be disjoint")
            _across[_g] = _gi
    for grp in groups:
        if len(grp) < 2:                                                             # OV-4
            raise SystemExit(f"FAIL: subtopic_merges group {grp} has <2 members")
        missing = [g for g in grp if g not in by_id]
        if missing:                                                                  # OV-3
            raise SystemExit(f"FAIL: subtopic_merges references unknown subtopic_id(s) {missing}")
        secs = {by_id[g]['section'] for g in grp}
        if len(secs) > 1:                                                            # OV-3
            raise SystemExit(f"FAIL: subtopic_merges group {grp} spans sections {sorted(secs)}")
        survivor = by_id[grp[0]]
        members  = [by_id[g] for g in grp]
        survivor['observed_count'] = sum(m.get('observed_count', 0) for m in members)
        survivor['max_per_paper']  = max(m.get('max_per_paper', 0) for m in members)
        tpp = [m.get('typical_per_paper', 0) for m in members]
        survivor['typical_per_paper'] = round(sum(tpp) / len(tpp)) if tpp else 0
        for g in grp[1:]:
            drop.add(g)
            _MERGE_LOG.append((g, grp[0]))
    kept = [e for e in entries if e.get('subtopic_id') not in drop]
    for g, keep in _MERGE_LOG:
        print(f"  MERGE: {g} → {keep} (observed_count summed)")
    return kept

def stamp_mechanic_axes(entries, exam_code, exam_meta=None):
    """SPEC-5 / D8. Derive ONCE, stamp, then assert. Called from run_synthesise() AFTER
    taxonomy sync, AFTER merges, AFTER subtopic_id minting — and BEFORE run_qv() and any
    writer. Every downstream consumer reads the stamped field; NONE recompute."""
    import difflib
    ov = load_mechanic_overrides(exam_code)
    pov = (exam_meta or {}).get('section_prefix_overrides', {})
    po  = build_section_prefix_map(sorted({e['section'] for e in entries}), pov)

    # PRECONDITION (§8-4): every entry must already carry a minted subtopic_id. mint runs
    # before stamp in run_synthesise; guard here so a misordered caller fails clearly, not
    # with a bare KeyError.
    _noid = [i for i, e in enumerate(entries) if not e.get('subtopic_id')]
    if _noid:
        raise SystemExit(f"stamp_mechanic_axes precondition violated: {len(_noid)} entr(y/ies) "
                         f"have no subtopic_id — mint_subtopic_ids() must run first.")

    known   = {e['subtopic_id'] for e in entries}
    unknown = set(ov.get('subtopic_overrides', {})) - known                          # OV-1 / EC-M7
    if unknown:
        for u in sorted(unknown):
            near = difflib.get_close_matches(u, list(known), n=3)
            print(f'  FAIL: override key {u!r} matches no subtopic_id. Did you mean: {near}')
        raise SystemExit(f'OV-1: {len(unknown)} override key(s) match no subtopic_id')
    for sec in ov.get('template_sets_by_section', {}):                               # OV-6
        if sec not in {e['section'] for e in entries}:
            raise SystemExit(f"OV-6: template_sets_by_section names unknown section {sec!r}")

    _ovsub = ov.get('subtopic_overrides', {})
    _forced_fk = set()          # ids whose form_key was set by an EXPLICIT curator override
    for e in entries:
        templates = ' '.join(p.get('template', '') for p in e.get('PYQ_STEM_PATTERNS', []))
        ax = derive_mechanic(e['section'], e.get('subtopic') or e.get('sub_type_label',''),
                             e.get('sub_type_label'), templates,
                             e.get('format', 'TEXT'), e['subtopic_id'], po)
        e['concept_group']     = ax['family']
        e['question_mechanic'] = ax['mechanic']
        e['form_key']          = ax['form_key']
        e['collision_domain']  = ax['collision_domain']
        if 'form_key' in _ovsub.get(e['subtopic_id'], {}):
            _forced_fk.add(e['subtopic_id'])

    # EC-M1: two subtopics whose DISPLAY_NAME yields the SAME derived base in one
    # collision_domain both fall back to slugify(subtopic_id) — deterministic, unique.
    # This applies ONLY to derived collisions. A collision in which ANY member carries an
    # EXPLICIT override form_key is NOT auto-resolved: that is an OV-2 curator error and
    # must FAIL loudly below (silently rewriting a curator's declared value would hide a
    # real mistake). See EC-M8.
    import hashlib as _hl
    claims = {}
    for e in entries:
        claims.setdefault((e['collision_domain'], e['form_key']), []).append(e)
    for (_dom, _fk), grp in claims.items():
        if len({e['subtopic_id'] for e in grp}) > 1 and not any(e['subtopic_id'] in _forced_fk for e in grp):
            for e in grp:
                e['form_key'] = slugify(e['subtopic_id'])
    # Residual guard: subtopic_ids are unique, but slugify() maps '.' and '_' alike, so two
    # DISTINCT ids can slugify to the same string (e.g. 'p.a_b.c' and 'p.a.b_c'). Any residual
    # (domain, form_key) collision among AUTO-RESOLVED entries (no forced override) is broken
    # deterministically with a short id-hash suffix, so genuinely-distinct subtopics never
    # provoke a false HALT. Override-induced collisions are left for the invariant to reject.
    _res = {}
    for e in entries:
        _res.setdefault((e['collision_domain'], e['form_key']), []).append(e)
    for (_dom, _fk), grp in _res.items():
        if len({e['subtopic_id'] for e in grp}) > 1 and not any(e['subtopic_id'] in _forced_fk for e in grp):
            for e in grp:
                _h = _hl.md5(e['subtopic_id'].encode('utf-8')).hexdigest()[:6]
                e['form_key'] = f"{e['form_key']}_{_h}"

    # OV-2 / D7 / EC-M8 / EC-M15: uniqueness is an INVARIANT, asserted before any write.
    seen, violations = {}, []
    for e in entries:
        k = (e['collision_domain'], e['form_key'])
        if not e['form_key']:
            violations.append(f"{e['subtopic_id']}: empty form_key")
        if e['form_key'] == e['collision_domain']:
            violations.append(f"{e['subtopic_id']}: form_key equals collision_domain")
        if k in seen and seen[k] != e['subtopic_id']:
            violations.append(f"{k[0]}:{k[1]} shared by {seen[k]} and {e['subtopic_id']}")
        seen[k] = e['subtopic_id']
    if violations:
        raise SystemExit(
            'form_key uniqueness invariant violated. A manifest with a shared form_key is a '
            'latent Step 6 BV-10a HALT whose triggering depends on N_mocks and batch_size, '
            'which Step 5 cannot know. Merge the subtopics via subtopic_merges, or give them '
            'distinct form_keys via subtopic_overrides.\n  ' + '\n  '.join(violations))
    print(f'  form_key invariant: PASS — {len(entries)} entries, '
          f'{len(seen)} distinct (collision_domain, form_key) pairs')
    return entries

# ── Back-compat wrappers. They read the STAMPED field first and only fall back to a
#    fresh derivation for a legacy caller that never ran stamp_mechanic_axes(). After
#    the v2.24.1 run_synthesise() path they always return the stamped value. ──
def _derive_axes(entry):
    templates = ' '.join(p.get('template','') for p in entry.get('PYQ_STEM_PATTERNS', []))
    return derive_mechanic(entry.get('section',''),
                           entry.get('subtopic') or entry.get('sub_type_label',''),
                           entry.get('sub_type_label'), templates,
                           entry.get('format','TEXT'), entry.get('subtopic_id'))

def _derive_concept_group(entry):
    return entry.get('concept_group') or _derive_axes(entry)['family']

def _derive_question_mechanic(entry):
    return entry.get('question_mechanic') or _derive_axes(entry)['mechanic']

def _derive_form_key(entry):
    return entry.get('form_key') or _derive_axes(entry)['form_key']

def _derive_collision_domain(entry):
    return entry.get('collision_domain') or _derive_axes(entry)['collision_domain']


# ── PROVENANCE STAMPS — ONE DEFINITION (v2.50.0) ─────────────────────────────
# These three strings are the ONLY place this spec's version appears in emitted
# output. Until v2.50.0 the same number was hand-copied into five scattered lines,
# and it drifted at four separate releases (CHANGELOG v2.14/v2.15/v2.17/v2.47) and
# again at the v2.49.1 -> v2.50.0 bump, where it blocked release 2026.08.15.8: the
# header said v2.50 while every section_rules.md and subtopic_manifest.json would
# have been stamped "produced by v2.49", on every run of every exam, with the
# artefacts persisting into Steps 6 and 7.
#
# THEY ARE DELIBERATELY LITERAL, NOT DERIVED. mock_sync_audit MS-3 STAMP-PARITY
# verifies them by scanning this file's fences for the three patterns below and
# comparing each against the header's major.minor. Building them from an f-string
# would leave MS-3 with nothing to match: the check would report 0 issues while
# verifying nothing — a check-shaped hole of exactly the kind C6-PRE was added to
# close one level up. One literal per pattern is the smallest form MS-3 can still
# police, and MS-3 now also fails if any of the three disappears.
#
# ON A VERSION BUMP: change the major.minor here and nowhere else in emitted code.
# The illustrative copy inside write_subtopic_manifest's docstring documents the
# OUTPUT shape and is checked by MS-3 too, so keep it in step.
FRAMEWORK_STAMP         = 'Framework_MockTestAnalyse v2.53'
GENERATED_BY_STAMP      = 'Generated by Framework_MockTestAnalyse v2.53'
FRAMEWORK_VERSION_STAMP = 'framework_version: v2.53'


def write_section_rules(entries, exam_code, exam_meta=None, progress=None):
    """
    BUG-A25 fix: output to /mnt/user-data/outputs/ for present_files access.
    v2.3 NEW: writes EXAM_STRUCTURE header block (CATEGORY C) when exam_meta provided.
    v2.3 NEW: writes STRUCTURAL_CHANGES_BY_YEAR block computed from PYQ data.
    v2.3 NEW: writes figural_banned flag per section header.
    v2.15 BUG-D03: accepts progress dict for per-section option_label_format aggregation.

    exam_meta: dict built by run_synthesise from progress['_meta'].
      Keys: time_per_q_sec, language, q_types, marks_per_q, negative_marking,
            options_count, multi_select_allowed, papers_analysed, questions_analysed,
            years_covered, generation_date, option_label_format,
            marking_scheme, level, medium (v2.18 additions).
    progress: the full progress dict (needed for per-question option_label aggregation).
    """
    from datetime import datetime
    out  = f'/mnt/user-data/outputs/{exam_code}_section_rules.md'
    meta = exam_meta or {}
    progress = progress or {}   # v2.15: safe fallback for label aggregation

    # ── CATEGORY C: exam-level header (auto-detected — not hardcoded) ─────────
    lines = [
        f'# {exam_code}_section_rules.md',
        f'# Generated by {GENERATED_BY_STAMP}',
        f'# DO NOT edit manually -- regenerate via: PYQExtract {exam_code} --synthesise ALL',
        f'# Download this file from chat → upload to {exam_code} project Files/Knowledge section.',
        '',
        '=== EXAM_STRUCTURE ===',
        f'exam_code: {exam_code}',
        f'total_papers_analysed: {meta.get("papers_analysed", 0)}',
        f'total_questions_analysed: {meta.get("questions_analysed", 0)}',
        f'years_covered: {meta.get("years_covered", [])}',
        f'generation_date: {meta.get("generation_date", datetime.now().isoformat()[:10])}',
        f'time_per_q_sec: {meta.get("time_per_q_sec", "unknown")}',
        f'language: {meta.get("language", "unknown")}',
        # v2.18: new fields from Step 2a v2.5 exam_config contract
        f'medium: {meta.get("medium", "unknown")}',
        f'level: {meta.get("level", "unknown")}',
        f'q_types: {meta.get("q_types", ["MCQ"])}',
        f'marks_per_q: {meta.get("marks_per_q", {"MCQ": 1})}',
        f'negative_marking: {meta.get("negative_marking", 0)}',
        # v2.18: full per-range marking_scheme from exam_config. Steps 7/8/9 can use this
        # for exact per-Q-position marks lookup (e.g., CSIR NET Q.72 → 4 marks, Q.25 → 2 marks).
        # marks_per_q and negative_marking above remain as summary scalars for backward compat.
        f'marking_scheme: {meta.get("marking_scheme", [])}',
        f'options_count: {meta.get("options_count", 4)}',
        # options_count → S1 reads as total_options and writes to blueprint.json Step 7.
        # S2 reads as num_options via bp.get('total_options', 4). SYNC CHAIN:
        #   S0 writes options_count → S1 reads → writes total_options → S2 reads.
        f'option_label_format: {meta.get("option_label_format", "1/2/3/4")}',
        # option_label_format → S1 reads and writes as option_label to blueprint.json Step 7.
        # S2 reads via bp.get('option_label','1/2/3/4') AND re-reads per section from
        # section_rules.md option_label_format field below (per-section override).
        # HOW TO DETECT option_label_format from PYQ: scan PYQ option lines for pattern:
        #   "(1)" / "(A)" / "1." / "A." → set option_label_format accordingly.
        #   Most SSC/banking exams: "1/2/3/4". UPSC/GATE: "A/B/C/D". Regional: varies.
        f'multi_select_allowed: {str(meta.get("multi_select_allowed", False)).lower()}',
        # v2.5 MSQ contract fields (consumed by Step 6/7/9). Inert when multi_select_allowed=false.
        f'msq_k_mode: {meta.get("msq_k_mode", "n/a")}',
        f'msq_k: {meta.get("msq_k", "none")}',
        # v2.6 D5: AOTA policy under MSQ. Step 7 (R-MSQ-ESCAPE/G-MSQ-SET) and Step 8
        # (A-MSQ-KEY) read this directly from section_rules. Default false.
        f'msq_allow_aota: {str(meta.get("msq_allow_aota", False)).lower()}',
        # v2.9 (contract-sync fix): the localized MSQ select-instruction, the EXACT MSQ
        # analogue of nat_instruction below. Step 7 (msq_instruction_for) and Step 8
        # (msq_instruction_phrases) READ this from section_rules; before v2.9 no producer
        # emitted it, so the instruction was silently locked to a hardcoded fallback and was
        # not exam-configurable/localizable the way NAT's is. Now authoritative + overridable
        # per exam; the *_hi variant carries the Hindi/bilingual phrasing. Parenthesised so it
        # reads as an in-stem instruction. Inert when multi_select_allowed=false.
        f'msq_instruction: {meta.get("msq_instruction", "(One or more options may be correct)")}',
        f'msq_instruction_hi: {meta.get("msq_instruction_hi", "(एक या अधिक विकल्प सही हो सकते हैं)")}',
        f'negative_marking_by_type: {meta.get("negative_marking_by_type", {})}',
        f'partial_credit: {str(meta.get("partial_credit", False)).lower()}',
        # v2.12 difficulty_labels — the CANONICAL, exam-overridable difficulty vocabulary
        # used as the RENDERED/stored Complexity value in the per-question index
        # (registry.question_index: Step 6 seeds, Step 7 fills, Step 8 certifies, Step 11
        # renders). Default ['Easy','Medium','Hard']. ALIAS CONTRACT — do NOT conflate the
        # three pre-existing internal spellings:
        #   • Step 5 PYQ_DIFFICULTY_CALIBRATION levels : Simple / Medium / Hard  (analysis)
        #   • Step 6 difficulty_schedule COUNT keys     : simple / medium / hard  (per-mock counts)
        #   • canonical LABEL (this field, index/tags)  : Easy  / Medium / Hard
        # Fixed alias: simple→Easy, medium→Medium, hard→Hard. An exam may override this list
        # (e.g. a 2- or 5-band set); the index value and the schedule bands then draw from it.
        f'difficulty_labels: {meta.get("difficulty_labels", ["Easy", "Medium", "Hard"])}',
        # v2.8 NAT contract fields (consumed by Step 6/7/9). nat_allowed is the capability
        # gate (mirrors multi_select_allowed); nat_present is a rollup of THIS analysis
        # (true iff any subtopic resolved to answer_type=='numerical'). All inert/absent-safe
        # when nat_allowed=false. nat_answer_type/tolerance/instruction define the answer model.
        f'nat_allowed: {str(meta.get("nat_allowed", False)).lower()}',
        f'nat_present: {str(any(e.get("answer_type") == "numerical" for e in entries)).lower()}',
        f'nat_answer_type: {meta.get("nat_answer_type", "real")}',
        f'nat_tolerance: {meta.get("nat_tolerance", "0")}',
        f'nat_instruction: {meta.get("nat_instruction", "Enter your answer as a numerical value.")}',
        f'total_sections: {len(set(e["section"] for e in entries))}',
        f'{FRAMEWORK_VERSION_STAMP}',  # v2.50.0: was five hand-copied literals — a five-times-recurred stamp-drift class (CHANGELOG v2.14/v2.15/v2.17/v2.47, and again at the v2.49.1->v2.50.0 bump, which blocked release 2026.08.15.8). Now ONE definition; no consumer parses it (verified), keep honest anyway
        '',
    ]

    # ── STRUCTURAL_CHANGES_BY_YEAR (observed from data — not hardcoded) ───────
    year_changes = _compute_structural_changes(entries)
    if year_changes:
        lines += [
            '=== STRUCTURAL_CHANGES_BY_YEAR ===',
            '# Observed from PYQ data — NOT hardcoded. Shows removed/new subtopics,',
            '# format changes, DI shifts, FIGURAL elimination across years.',
            '# Step 7 reads these to understand recent exam structural changes.',
        ]
        lines += year_changes
        lines.append('')

    by_sec = {}
    for e in entries: by_sec.setdefault(e['section'], []).append(e)

    # ── v2.4 / v2.24.1 SUBTOPIC_ID: mint once, collision-safe, IDEMPOTENT ──
    # v2.24.1: run_synthesise() now mints ids BEFORE run_qv() (so the gate and every
    # writer read the SAME id). This is a no-op guard for entries already stamped.
    mint_subtopic_ids(entries, exam_meta)

    for section, sec_entries in by_sec.items():
        # v2.15 BUG-D03 fix: derive option LABEL style from per-question option_label
        # stored during extraction — NOT from option_format.primary (which is the
        # content FORMAT type like 'single_value', a completely different domain).
        # Aggregation: collect option_label from all observed Qs in this section via
        # progress, then majority-vote. Fallback to exam-level option_label_format.
        sec_keys = [(e['section'], e['topic'], e['subtopic']) for e in sec_entries]
        all_labels = []
        for sk in sec_keys:
            for q in progress.get(sk, []):
                lbl = q.get('option_label', 'unknown')
                if lbl != 'unknown':
                    all_labels.append(lbl)
        if all_labels:
            fmt_label = Counter(all_labels).most_common(1)[0][0]
        else:
            fmt_label = meta.get('option_label_format', '1/2/3/4')

        # figural_banned: True when ALL FIGURAL subtopics in section are deprecated/absent
        # Computed from observed data — NOT hardcoded per exam.
        figural_entries = [e for e in sec_entries if e.get('format') == 'FIGURAL']
        figural_banned  = bool(figural_entries) and all(
            e.get('observed_count', 0) == 0
            or all(p.get('deprecated', False)
                   for p in e.get('PYQ_STEM_PATTERNS', []))
            for e in figural_entries
        )

        lines += ['', f'=== SECTION: {section} ===',
                  f'option_label_format: {fmt_label}',
                  f'figural_banned: {str(figural_banned).lower()}',
                  'sub_types_observed:']
        for e in sorted(sec_entries, key=lambda x: -x['observed_count']):
            lines.append(f'  - {e["sub_type_label"]} (n={e["observed_count"]})')
        # v2.23 THREE-AXIS (CATEGORY A): the per-section 3-year format-distribution TARGET
        # (per-paper averages) that Step 6 (allocation: Axis-1/3 + LINKED) and Step 7
        # (generation: the other 7 Axis-2 classes, joint-solved with difficulty) enforce,
        # and Step 8 audits. Omitted for all-Zero-PYQ sections (compute returns None).
        axdist = compute_section_axis_distribution(sec_entries, progress)
        if axdist:
            lines.append('axis_distribution:')
            lines.append(f'  recent_years: {axdist["recent_years"]}')
            lines.append(f'  n_papers_recent: {axdist["n_papers_recent"]}')
            lines.append(f'  mocks_per_window: {axdist["mocks_per_window"]}')
            lines.append(f'  negative_rate: {axdist["negative_rate"]}')
            lines.append(f'  axis1_per_paper: {axdist["axis1_per_paper"]}')
            lines.append(f'  axis2_per_paper: {axdist["axis2_per_paper"]}')
            lines.append(f'  axis3_per_paper: {axdist["axis3_per_paper"]}')
            lines.append(f'  axis2_audit_mode: {axdist["axis2_audit_mode"]}')
        for e in sorted(sec_entries, key=lambda x: -x['observed_count']):
            lines += format_entry(e)

    with open(out, 'w', encoding='utf-8') as f: f.write('\n'.join(lines))
    print(f'Written: {out} ({len(lines)} lines)')
    return out

slugify = bc.slugify   # DELEGATED (Cluster D) — one definition corpus-wide


# Section-prefix recipe (v2.4): readable, stable, deterministic.
# Uses the INITIALS of significant section words (skipping and/of/the/...), so
# 'General Intelligence & Reasoning' -> 'gir', 'Quantitative Aptitude' -> 'qa'.
# Single-word sections fall back to first 4 chars. Prefix collisions between two
# DISTINCT sections are resolved by build_section_prefix_map() with a numeric
# suffix (gs, gs2, ...). exam_meta['section_prefix_overrides'] can pin a prefix.
_PREFIX_STOPWORDS = ('and', 'of', 'the', 'for', 'in', 'to', 'a', 'an')

def section_prefix(section_name, overrides=None):
    overrides = overrides or {}
    if section_name in overrides:
        return overrides[section_name]
    words = [w for w in slugify(section_name).split('_') if w not in _PREFIX_STOPWORDS]
    if len(words) >= 2:
        return ''.join(w[0] for w in words)   # word-initials, e.g. gir / qa / ec
    return (words[0][:4] if words else 'sec')

def build_section_prefix_map(sections, overrides=None):
    """
    Deterministic, collision-safe section→prefix map. Two DISTINCT sections that
    would collapse to the same prefix get numeric suffixes (gs, gs2, ...).
    Build this ONCE from the full section list, then pass the resulting overrides
    into make_subtopic_id so every subtopic uses the same stable prefix.
    """
    seen = {}; result = {}
    for s in sections:
        p = section_prefix(s, overrides)
        if p in seen and seen[p] != s:
            base = p; n = 2
            while p in seen and seen[p] != s:
                p = f'{base}{n}'; n += 1
        seen[p] = s; result[s] = p
    return result

def _as_mandate_int(v):
    """v2.30 — renamed from _as_int (GAP-2026-07-25-002): blueprint_core defines a
    DIFFERENT _as_int with different semantics (returns a 0 default, not None). Two
    private helpers sharing a name across an engine and a spec that imports it is a
    trap waiting for the first `from blueprint_core import *`.
    v2.11 — coerce a mandate integer field (may arrive as a str from section_rules,
    or as 'none'/None/'' when unset) to int or None. Used for min_per_series_window,
    min_count, and any future numeric mandate field."""
    if v in (None, '', 'none', 'None'):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _mandate_from_note(note):
    """v2.10 — Robust, sentence-independent 'mandatory every mock' detector.
    Returns True iff the NOTE both (a) mentions MANDATORY and (b) contains an
    every/per mock|paper phrase — anywhere, not necessarily in the same sentence.
    Replaces the v2.4 regex MANDATORY[^.\\n]*\\b(every mock|per mock)\\b, which was
    anchored to a single sentence and accepted only "mock", so it silently missed
    real wording such as "MANDATORY SUBTOPIC ... 1Q per every paper". An explicit
    mandate_every_mock line (emitted by format_entry / editable in section_rules)
    always takes precedence over this fallback. Exam-agnostic."""
    import re as _re
    if not note:
        return False
    return bool(_re.search(r'\bMANDATORY\b', note, _re.I)) and \
           bool(_re.search(r'\b(?:every|per)\s+(?:mock|paper)\b', note, _re.I))


def make_subtopic_id(section, topic, subtopic, prefix_overrides=None):
    """
    Mint the canonical subtopic_id: <section_prefix>.<topic_slug>.<subtopic_slug>
    - Deterministic: same (section, topic, subtopic) → same id, always.
    - Independent of concept_group (a separate concern — DOUBT-3 uniqueness).
    - Human-debuggable: e.g. 'qa.mensuration.mensuration_3d_combined',
      'gir.analogy.mixed_number_letter_analogy'.
    - prefix_overrides: the map from build_section_prefix_map() (collision-safe).
    Collisions (two different subtopics producing the same id) are detected and
    de-duplicated by write_subtopic_manifest() with a numeric suffix _2, _3, ...
    """
    return f'{section_prefix(section, prefix_overrides)}.{slugify(topic)}.{slugify(subtopic)}'


# ═══════════════════════════════════════════════════════════════════════════
# v2.20 — ZERO-PYQ SCAFFOLD ENTRY + TAXONOMY SYNC
# ═══════════════════════════════════════════════════════════════════════════
# These two functions implement Fix A (taxonomy sync) and Fix C (scaffold
# section_rules blocks) from the BUGFIX_Zero_PYQ_Manifest_Gap report.
# Called by run_synthesise() AFTER PYQ-based entries are built and BEFORE
# write_section_rules() / write_subtopic_manifest() run.

# ── v2.24.5: AUTOMATIC ZERO-PYQ FORMAT INFERENCE ────────────────────────────────
# Mirrors the _VISUAL_KEYWORDS set used in synthesise() (the PYQ path). KEEP IN SYNC — any
# keyword added there should be added here so PYQ and zero-PYQ agree on what "looks visual".
_ZP_VISUAL_KEYWORDS = re.compile(
    r'(?i)\b(figure[s]?|figural|diagram[s]?|venn|'
    r'mirror\s+image[s]?|water\s+image[s]?|paper\s*fold(ing)?|'
    r'counting\s+(figure|triangle|shape)[s]?|embedded\s+figure[s]?|'
    r'completion\s+of\s+(figure|pattern)[s]?|dice|cube\s+fold(ing)?|'
    r'pattern\s+completion|image\s+series|visual\s+reasoning)\b')


def infer_zero_pyq_axes(name, sibling_formats, sibling_answer_types, sibling_cardinalities):
    """v2.24.5 — PURE. Automatically infer a zero-PYQ subtopic's Axis-1 format + answer_type +
    answer_cardinality from evidence available WITHOUT any curator input:
      (1) NAME keyword  -> FIGURAL  (per-subtopic; the same heuristic trusted for PYQ subtopics);
      (2) same-topic PYQ SIBLINGS   -> inherit a UNANIMOUS non-TEXT format (>=2 siblings, all
          identical); inherit 'numerical' / 'multi' when >= two-thirds of (>=2) siblings are.
    Falls back to TEXT / option / single when there is no strong signal. Deterministic; no I/O.
    Precedence: name keyword (1) beats sibling inheritance (2). Returns
      {format, answer_type, answer_cardinality, inherently_visual, reason}.
    """
    fmt, inh_vis, reason = 'TEXT', False, 'default'
    if _ZP_VISUAL_KEYWORDS.search(name or ''):                      # (1) name -> FIGURAL
        fmt, inh_vis, reason = 'FIGURAL', True, 'name_keyword'
    else:                                                           # (2) UNANIMOUS topic siblings
        sibs = [f for f in (sibling_formats or []) if f]
        if len(sibs) >= 2 and len(set(sibs)) == 1 and sibs[0] != 'TEXT':
            fmt, reason = sibs[0], 'topic_unanimous'

    ans_type = 'option'                                             # NAT: >=2/3 of >=2 siblings
    at = [a for a in (sibling_answer_types or []) if a]
    if len(at) >= 2 and at.count('numerical') * 3 >= len(at) * 2:
        ans_type = 'numerical'

    ans_card = 'single'                                             # MSQ: >=2/3 of >=2 siblings
    ac = [c for c in (sibling_cardinalities or []) if c]
    if len(ac) >= 2 and ac.count('multi') * 3 >= len(ac) * 2:
        ans_card = 'multi'

    return {'format': fmt, 'answer_type': ans_type, 'answer_cardinality': ans_card,
            'inherently_visual': inh_vis, 'reason': reason}


def apply_zero_pyq_format_inference(entries):
    """v2.24.5 — In-place post-pass over the full entry set. For each ZERO-PYQ entry
    (observed_count == 0), infer format/answer_type/answer_cardinality from its NAME and its
    same-(section, topic) PYQ siblings (observed_count > 0), via infer_zero_pyq_axes(). PYQ
    entries are NEVER touched. Every change is logged (audit trail; no prompt). Runs BEFORE
    id-mint / stamp / QV / writers, so both section_rules and the manifest see the inferred axes.
    """
    from collections import defaultdict
    sib_fmt, sib_at, sib_ac = defaultdict(list), defaultdict(list), defaultdict(list)
    for e in entries:
        if e.get('observed_count', 0) > 0:                          # PYQ sibling
            k = (e.get('section'), e.get('topic'))
            sib_fmt[k].append(e.get('format', 'TEXT'))
            sib_at[k].append(e.get('answer_type', 'option'))
            sib_ac[k].append(e.get('answer_cardinality', 'single'))

    changed = 0
    for e in entries:
        if e.get('observed_count', 0) != 0:                         # PYQ subtopic — untouched
            continue
        k = (e.get('section'), e.get('topic'))
        res = infer_zero_pyq_axes(e.get('subtopic', ''), sib_fmt.get(k, []),
                                  sib_at.get(k, []), sib_ac.get(k, []))
        if res['reason'] == 'default' and res['answer_type'] == 'option' \
                and res['answer_cardinality'] == 'single':
            continue                                                # no signal → keep safe defaults
        before = (e.get('format'), e.get('answer_type'), e.get('answer_cardinality'))
        e['format'] = res['format']
        e['answer_type'] = res['answer_type']
        e['answer_cardinality'] = res['answer_cardinality']
        e['inherently_visual'] = bool(res['inherently_visual']) or e.get('inherently_visual', False)
        # keep the freq fields consistent with the inferred string type (some derivations read them)
        if res['answer_type'] == 'numerical':
            e['nat_freq'] = max(e.get('nat_freq', 0), 100)
        if res['answer_cardinality'] == 'multi':
            e['msq_freq'] = max(e.get('msq_freq', 0), 100)
        if res['format'] == 'FIGURAL' and not e.get('figural_data'):
            e['figural_data'] = {                                   # same conservative default as PYQ path
                'image_role': 'stem_only',
                'object_types': {'dominant': [], 'observed': [], 'avoid': []},
                'transformation_types': [], 'arrangement_types': [],
                'complexity_dist': {}, 'images_analysed': 0, 'images_unclear': 0}
        changed += 1
        print(f"  ZERO-PYQ INFERENCE: '{e.get('subtopic')}' "
              f"[{e.get('section')} > {e.get('topic')}] {before} -> "
              f"({res['format']}, {res['answer_type']}, {res['answer_cardinality']}) "
              f"[{res['reason']}]")
    if changed:
        print(f"Zero-PYQ format inference: {changed} scaffold entr"
              f"{'y' if changed == 1 else 'ies'} refined from name/topic evidence.")
    return entries


def make_zero_pyq_scaffold_entry(section, topic, subtopic):
    """
    v2.20 Fix C — Create a COMPLETE entry dict for a zero-PYQ subtopic.
    This entry has every field that format_entry() expects, filled with
    zero-PYQ defaults. The resulting section_rules block gives Step 7
    enough structure to generate questions using training knowledge +
    format guidance, even though no PYQ data exists for this subtopic.

    Returns: dict matching the synthesise_subtopic() output schema.
    """
    return {
        'section': section,
        'topic': topic,
        'subtopic': subtopic,
        'observed_count': 0,
        'format': 'TEXT',
        'option_format': {
            'primary': 'single_value',
            'recent_format': 'single_value',
            'changed_recently': False,
            'all_observed': ['single_value']
        },
        'OMML_required': False,
        'negative_question_freq': 0,
        'answer_type': 'option',
        'nat_freq': 0,
        'answer_cardinality': 'single',
        'msq_freq': 0,
        # v2.23: Zero-PYQ scaffold — no observed Axis-2; capability = family ∪ {DIRECT}
        # so Step 7 can use it as a format-elastic filler (decision 11).
        'observed_axis2': {},
        'presentation_family': resolve_presentation_family_s5(subtopic, 'TEXT'),
        'axis2_capability': axis2_capability(
            [], resolve_presentation_family_s5(subtopic, 'TEXT'), 'TEXT'),
        'fill_in_blank': 'none',
        'linked_group_size': 0,
        'max_per_paper': 2,
        'typical_per_paper': 1,
        'stem_word_count': {'min': 10, 'max': 50, 'typical': 25},
        'sub_type_label': subtopic,
        'concept_group': None,        # v2.24.1 (D8): stamped later by stamp_mechanic_axes()
        'question_mechanic': None,    # v2.24.1 (D8)
        'form_key': None,             # v2.24.1 (D8)
        'collision_domain': None,     # v2.24.1 (D8)
        'mandate_every_mock': False,
        'alternation_group': None,
        'min_per_series_window': None,
        'mandatory_group': None,
        'min_count': None,
        'PYQ_STEM_PATTERNS': [
            {
                'id': 'P1',
                'template': f'Standard {subtopic} question',
                'approach': 'direct',
                'frequency': 100,
                'confidence': 'absent',
                'raw_count': 0,
                'years': [],
                'note_block': 'never',
                'deprecated': False
            }
        ],
        'PYQ_DIFFICULTY_CALIBRATION': {
            'Simple': {'criteria': '(no PYQ data)', 'is_inferred': True},
            'Medium': {'criteria': '(no PYQ data)', 'is_inferred': True},
            'Hard':   {'criteria': '(no PYQ data)', 'is_inferred': True}
        },
        'wrong_option_structure': {
            'type': 'same_category',
            'description': 'Options from the same conceptual category as the correct answer.'
        },
        'NOTE': (f'Zero-PYQ subtopic. No PYQ observations available. '
                 f'Added from exam syllabus/taxonomy via v2.20 taxonomy sync. '
                 f'Step 7 generates questions using exam-level knowledge and '
                 f'the format/option guidance above.'),
        'note_text': (f'Zero-PYQ subtopic. No PYQ observations available. '
                      f'Added from exam syllabus/taxonomy via v2.20 taxonomy sync. '
                      f'Step 7 generates questions using exam-level knowledge and '
                      f'the format/option guidance above.')
    }


def taxonomy_sync_entries(existing_entries, exam_code):
    """
    v2.20 Fix A — TAXONOMY SYNC PROTOCOL.

    After PYQ-based synthesis produces the entry list, this function
    synchronises it with the exam's approved taxonomy to ensure the
    manifest covers the COMPLETE subtopic vocabulary, not just the
    PYQ-observed subset.

    For every taxonomy-defined subtopic NOT already in existing_entries,
    creates a scaffold entry via make_zero_pyq_scaffold_entry().

    Taxonomy sources (UNION — both loaded, not primary/fallback):
      1. taxonomy_draft.json: [ExamCode]_taxonomy_draft.json in project
         knowledge — the syllabus-faithful taxonomy from Step 2a. This is
         the source that contains zero-PYQ subtopics (new syllabus entries
         that have never appeared in any PYQ paper). PRIMARY source.
      2. Approved Analysis doc: [ExamCode]_PYQ_Analysis.docx in project
         knowledge — ADDITIONAL source. The Analysis doc typically contains
         only PYQ-observed subtopics (which are already in existing_entries),
         but is loaded as a safety net in case taxonomy_draft is absent.

    WHY taxonomy_draft IS PRIMARY (not Analysis doc):
      The Analysis doc (Step 2c output) contains ~PYQ-observed subtopics.
      Zero-PYQ subtopics (the ones this function exists to find) are NOT
      in the Analysis doc — they have zero PYQ observations so they were
      never processed. The taxonomy_draft.json (Step 2a output) IS the
      syllabus-faithful source that contains ALL subtopics including
      zero-PYQ ones. Evidence: SSC CGL Tier 2 — taxonomy_draft had 93
      subtopics (all 7 orphans present), Analysis doc had ~96 (orphans
      absent, but finer PYQ-discovered splits present).

    Returns: (new_entries_list, sync_log_lines)
      new_entries_list: scaffold entries to APPEND to existing_entries.
      sync_log_lines:   human-readable log of what was added/skipped.

    EDGE CASES (ref: BUGFIX_Zero_PYQ_Manifest_Gap.md):
      EC-ZP-1: Taxonomy subtopic name COLLIDES with existing entry
               (same slugified name) → use existing, do not duplicate.
      EC-ZP-2: Taxonomy subtopic is COVERED by finer-grained existing
               entries (e.g., taxonomy "Geometry" but entries have
               "Triangles", "Circles") → do not create; log coverage.
      EC-ZP-3: Taxonomy subtopic under DIFFERENT section than existing
               → section mismatch is a HARD STOP (taxonomy must align
               with exam_config sections).
      EC-ZP-4: Exam with ZERO PYQ papers (100% zero-PYQ) → all
               subtopics become scaffold entries. Supported.
      EC-ZP-5: taxonomy_draft.json absent AND Analysis doc absent
               → sync SKIPS (cannot add what doesn't exist). Log warning.
      EC-ZP-6: PYQ-discovered subtopic NOT in taxonomy → already in
               entries. Taxonomy sync only ADDS; it never removes.
      EC-ZP-7: Same subtopic in MULTIPLE sections in taxonomy
               → each gets its own entry (slugify includes section prefix).
      EC-ZP-8: Subtopic in taxonomy_draft but REMOVED from Analysis doc
               → taxonomy_draft is the syllabus-faithful source; if a
               subtopic is in taxonomy_draft it represents the exam
               authority's syllabus. If it was intentionally excluded,
               it should be removed from taxonomy_draft.json itself.
      EC-ZP-9: Subtopic in section_rules but not manifest → handled by
               rebuild_subtopic_manifest_from_section_rules() (separate).
      EC-ZP-10: Large exam (300+ taxonomy, 50 in PYQs) → adds 250+
                scaffold entries. No performance issue (flat list).
    """
    import json, os, glob, re

    sync_log = []
    new_entries = []

    # ── Step 1: Build the EXISTING subtopic index from PYQ-derived entries ──
    # Key: (section_slug, topic_slug, subtopic_slug) for collision detection.
    # Also build a set of subtopic_slugs per section for EC-ZP-2 coverage check.
    existing_keys = set()
    existing_slugs_by_section = {}   # section -> set of subtopic slugs
    existing_topic_slugs_by_section = {}  # section -> set of topic slugs
    for e in existing_entries:
        sec_s = slugify(e['section'])
        top_s = slugify(e['topic'])
        sub_s = slugify(e['subtopic'])
        existing_keys.add((sec_s, top_s, sub_s))
        existing_slugs_by_section.setdefault(sec_s, set()).add(sub_s)
        existing_topic_slugs_by_section.setdefault(sec_s, set()).add(top_s)

    # ── Step 2: Load taxonomy sources (UNION — both tried) ──
    taxonomy_tuples = []   # list of (section, topic, subtopic) raw strings
    seen_tuples = set()    # dedup across sources

    # Source 1 (PRIMARY): taxonomy_draft.json — the syllabus-faithful taxonomy
    # This is the source that contains zero-PYQ subtopics (the orphans).
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, f'*taxonomy_draft*.json')):
            try:
                with open(f, encoding='utf-8') as fp:
                    tax_data = json.load(fp)
                # v2.17 BUGFIX — the taxonomy lives under ['sections'], not at
                # top level. Reading the top level made the isinstance guards
                # skip everything: this PRIMARY source silently yielded ~0
                # subtopics and fell through to Source 2, losing exactly the
                # zero-PYQ orphan subtopics it exists to supply. Consistent with
                # the SSC CGL Tier 2 Mock 1 incident (7 syllabus-only subtopics
                # first surfacing at Step 6/7). Pre-existing, not v2.17.
                # CANONICAL READER — do not hand-roll another copy.
                from syllabus_provenance import read_taxonomy_draft
                for (sec, top, sub) in read_taxonomy_draft(tax_data):
                    tup_key = (slugify(sec), slugify(top), slugify(sub))
                    if tup_key not in seen_tuples:
                        taxonomy_tuples.append((sec, top, sub))
                        seen_tuples.add(tup_key)
                if taxonomy_tuples:
                    sync_log.append(f'  Taxonomy source 1 (PRIMARY): taxonomy_draft.json ({os.path.basename(f)}) — {len(taxonomy_tuples)} subtopics')
                    break
            except Exception as ex:
                sync_log.append(f'  WARN: taxonomy_draft.json unreadable: {ex}')

    # Source 2 (ADDITIONAL): approved Analysis doc — safety net for when
    # taxonomy_draft is absent. Read through corpus_io Cluster K (v2.30) and
    # asserted against the approval record's taxonomy_fingerprint (v2.31).
    analysis_added = 0
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, '*.docx')):
            bn = os.path.basename(f).lower()
            if 'analysis' in bn and exam_code.lower() in bn:
                try:
                    doc_tuples = _extract_taxonomy_tuples_from_analysis_doc(f)
                    for tup in doc_tuples:
                        tup_key = (slugify(tup[0]), slugify(tup[1]), slugify(tup[2]))
                        if tup_key not in seen_tuples:
                            taxonomy_tuples.append(tup)
                            seen_tuples.add(tup_key)
                            analysis_added += 1
                    if doc_tuples:
                        sync_log.append(
                            f'  Taxonomy source 2 (ADDITIONAL): Analysis doc ({os.path.basename(f)}) — '
                            f'{analysis_added} new subtopics added beyond taxonomy_draft')
                except corpus_io.AnalysisDocError:
                    # v2.31 — NEVER a WARN. An unreadable or unapproved Analysis doc
                    # is not a source that happened to contribute nothing; it is the
                    # wrong taxonomy, and every id minted from it is wrong. The old
                    # code caught this here AND inside the extractor, so the fault
                    # had to survive two independent downgrades to be seen at all.
                    raise
                except Exception as ex:
                    sync_log.append(f'  WARN: Analysis doc {os.path.basename(f)} unreadable: {ex}')

    # EC-ZP-5: no taxonomy source found → skip sync
    if not taxonomy_tuples:
        sync_log.append(
            '  Taxonomy sync SKIPPED: no taxonomy_draft.json or Analysis doc found. '
            'If Step 6 encounters unresolvable subtopics, re-run Step 2a (PYQDraft) '
            'to generate taxonomy_draft.json, then re-run Step 5.')
        return new_entries, sync_log

    sync_log.append(f'  Total taxonomy subtopics (union): {len(taxonomy_tuples)}')

    # ── Step 3: Diff taxonomy against existing entries ──
    added_count = 0
    skipped_existing = 0
    skipped_covered = 0

    for (tax_sec, tax_top, tax_sub) in taxonomy_tuples:
        sec_s = slugify(tax_sec)
        top_s = slugify(tax_top)
        sub_s = slugify(tax_sub)

        # EC-ZP-1: exact match (same section+topic+subtopic slug) → already exists
        if (sec_s, top_s, sub_s) in existing_keys:
            skipped_existing += 1
            continue

        # EC-ZP-1 variant: same subtopic slug under same section (different topic slug)
        # Check if ANY existing entry in this section has the same subtopic slug.
        # This catches renames/reclassifications at the topic level.
        if sec_s in existing_slugs_by_section and sub_s in existing_slugs_by_section[sec_s]:
            skipped_existing += 1
            sync_log.append(
                f'  SKIP (EC-ZP-1): "{tax_sub}" in [{tax_sec}] — slug matches existing entry.')
            continue

        # EC-ZP-2: coverage check — is this taxonomy subtopic COVERED by finer-grained
        # existing entries? If the taxonomy subtopic slug is a PREFIX of any existing
        # subtopic's topic_slug or subtopic_slug within the same section, the finer
        # entries likely cover the taxonomy scope.
        if sec_s in existing_slugs_by_section:
            covered_by = [s for s in existing_slugs_by_section[sec_s]
                          if sub_s in s and sub_s != s]
            if covered_by:
                skipped_covered += 1
                sync_log.append(
                    f'  SKIP (EC-ZP-2): "{tax_sub}" in [{tax_sec}] — covered by '
                    f'finer entries: {covered_by[:5]}')
                continue

        # Not in existing → create scaffold entry
        scaffold = make_zero_pyq_scaffold_entry(tax_sec, tax_top, tax_sub)
        new_entries.append(scaffold)
        existing_keys.add((sec_s, top_s, sub_s))
        existing_slugs_by_section.setdefault(sec_s, set()).add(sub_s)
        added_count += 1
        sync_log.append(f'  ADDED: "{tax_sub}" [{tax_sec} > {tax_top}] — zero-PYQ scaffold')

    sync_log.append(
        f'  Taxonomy sync complete: {added_count} zero-PYQ scaffolds added, '
        f'{skipped_existing} already existed, {skipped_covered} covered by finer entries.')

    return new_entries, sync_log


def _extract_taxonomy_tuples_from_analysis_doc(docx_path):
    """(section, topic, subtopic) tuples from the approved Analysis doc.

    v2.30 (GAP-2026-07-25-002) — DELEGATED to corpus_io Cluster K, THE reader for
    this artefact. The previous implementation was the tuple-returning twin of
    extract_taxonomy_from_analysis_doc() and shared all of its defects: paragraphs
    only (subtopics are in tables), Heading-style detection against a generator
    that emits no styles, and a first-value latch. It returned an empty list from
    every real Analysis doc, and — because both its except branches swallow
    silently — that emptiness was indistinguishable from "the doc had nothing to
    add". Measured on the first exam's live doc: 0 tuples against a truth of 131.

    Returns [] when the doc is ABSENT, which is a supported configuration: this is
    an ADDITIONAL source and Step 5 must still run without it.

    v2.31 — WHAT IT NO LONGER SWALLOWS. The old body was `except Exception: return
    []`, which made three different situations indistinguishable: "no Analysis doc,
    by design", "the Analysis doc is unreadable", and "the Analysis doc is not the
    approved one". Only the first is benign. The other two returned [] and the
    caller logged a WARN, so the safety net that mints ids for zero-PYQ subtopics
    quietly contributed nothing — exactly the shape of the v2.30 defect, one layer
    up. Absence is still tolerated; a doc that is PRESENT and wrong is now loud.
    """
    import corpus_io
    try:
        doc = corpus_io.load_taxonomy(path=docx_path, step='PYQExtract')
    except corpus_io.AnalysisDocError as ex:
        if 'no Analysis doc found' in str(ex):
            return []                      # absent by design — the only benign case
        raise                              # present but unreadable — never a WARN
    return list(doc['triples'])


def write_taxonomy_xlsx(manifest, exam_code):
    """v2.24 — Emit [ExamCode]_taxonomy.xlsx: a plain, human-readable list of
    Subject | Topic | Sub Topic Name | Sub Topic Id | Upload Order (one row per
    sub-topic, in MANIFEST ORDER), so the Step-6 operator can pick scope values
    WITHOUT reading the manifest JSON. It is a companion to
    subtopic_manifest.json, generated from the SAME dict — the JSON stays
    authoritative. Failure to write (e.g. openpyxl absent) is a WARN, never a
    hard stop.

    v2.48.0 — ROW ORDER IS THE TEACHING ORDER, NEVER RE-SORTED
    (GAP-2026-08-14-TAXONOMY-ORDER). Through v2.47.x this function sorted rows
    alphabetically "for readability" — which silently DISCARDED the manifest's
    curated order. That order is load-bearing three times over:
    notes_core.assign_numbering freezes first-seen manifest order into the
    permanent S/T/ST unit numbers (verified against delivered filenames:
    Vector Calculus is ST02 by syllabus order, ST06 alphabetically); the Notes
    portal upload sequence follows this sheet top-to-bottom; and the Notes
    integration sections' backward-only rule runs on the same order. An
    alphabetical resort therefore showed the operator a DIFFERENT order from
    the one every filename and title number already carried. Rows now emit in
    manifest insertion order with an explicit Upload Order column (E). Columns
    A-D are UNCHANGED in position and meaning — every downstream instruction
    that says "column D" still holds.

    Column -> Step-6 use:  Subject = subject scope · "Subject::Topic" = topic scope ·
    "Subject::Topic::Sub Topic Name" = subtopic scope (or the Sub Topic Id if that name repeats
    under the same topic). Upload Order (column E) is for the PORTAL: upload
    sub-topics in this sequence, top to bottom.
    """
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("WARN: openpyxl unavailable — skipped taxonomy.xlsx (manifest.json is authoritative).")
        return None

    # MANIFEST ORDER, verbatim — dict insertion order IS the taxonomy order
    # (the same order notes_core.assign_numbering freezes into unit numbers).
    rows = [[v.get('section', ''), v.get('topic', ''), v.get('display_name', ''),
             sid, i]
            for i, (sid, v) in enumerate(manifest.get('subtopics', {}).items(),
                                         start=1)]

    wb = Workbook()
    ws = wb.active
    ws.title = 'Taxonomy'
    head_font = Font(name='Arial', size=11, bold=True, color='FFFFFF')
    head_fill = PatternFill('solid', fgColor='1F4E79')
    arial = Font(name='Arial', size=11)
    thin = Side(style='thin', color='D0D0D0')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c, name in enumerate(['Subject', 'Topic', 'Sub Topic Name', 'Sub Topic Id',
                              'Upload Order'], start=1):
        cell = ws.cell(row=1, column=c, value=name)
        cell.font = head_font
        cell.fill = head_fill
        cell.alignment = Alignment(horizontal='left', vertical='center')
        cell.border = border
    band = PatternFill('solid', fgColor='F2F6FB')
    prev_subject, shade = None, False
    for i, row in enumerate(rows, start=2):
        if row[0] != prev_subject:
            shade = not shade
            prev_subject = row[0]
        for c, val in enumerate(row, start=1):
            cell = ws.cell(row=i, column=c, value=val)
            cell.font = arial
            cell.border = border
            cell.alignment = Alignment(horizontal='left', vertical='center')
            if shade:
                cell.fill = band
    for c, width in enumerate([26, 30, 46, 30, 14], start=1):
        ws.column_dimensions[get_column_letter(c)].width = width
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:E{len(rows) + 1}'

    hw = wb.create_sheet('How to use')
    guide = [
        (f'{exam_code} — how to use this list in Step 6', True),
        ('', False),
        ('This lists every Subject, Topic and Sub-Topic in your exam. Pick from the', False),
        ('"Taxonomy" tab, then copy the value into the Step-6 trigger (match text EXACTLY —', False),
        ('spelling and capital letters matter). Use the header filter arrows to narrow down.', False),
        ('', False),
        ('PORTAL UPLOAD ORDER — the rows are already in the correct teaching sequence', True),
        ('(basics first). Upload sub-topics to the portal from TOP TO BOTTOM, exactly as', False),
        ('listed; the "Upload Order" column (E) numbers that sequence. Do NOT re-sort', False),
        ('this sheet before uploading — the row order matches the numbering printed in', False),
        ('every delivered file.', False),
        ('', False),
        ('SUBJECT test   -> copy the Subject cell (column A):', True),
        ('    ScopedBlueprint --level subject  --scope "<Subject>"          --count N --qs_per_paper Q', False),
        ('', False),
        ('TOPIC test     -> join Subject and Topic with "::" (columns A and B):', True),
        ('    ScopedBlueprint --level topic    --scope "<Subject>::<Topic>" --count N --qs_per_paper Q', False),
        ('', False),
        ('SUB-TOPIC test -> join Subject + Topic + Sub Topic Name with "::" (columns A, B, C):', True),
        ('    ScopedBlueprint --level subtopic --scope "<Subject>::<Topic>::<Sub Topic Name>" --count N --qs_per_paper Q', False),
        ('    The Topic in the middle keeps same-named sub-topics apart — e.g. "Kinematics"', False),
        ('    under Mechanics vs under Rotational Motion resolve to two DIFFERENT sub-topics.', False),
        ('    Use the Sub Topic Id (column D) ONLY if the same name repeats under the same Topic:', False),
        ('        --scope <Sub Topic Id>', False),
    ]
    for i, (text, bold) in enumerate(guide, start=1):
        hw.cell(row=i, column=1, value=text).font = Font(name='Arial', size=11, bold=bold)
    hw.column_dimensions['A'].width = 100

    out = f'/mnt/user-data/outputs/{exam_code}_taxonomy.xlsx'
    wb.save(out)
    print(f'Written: {out} ({len(rows)} sub-topics — human-readable taxonomy for Step 6)')
    return out


# ═══ SUBTOPIC ORDERING RULE (v2.48.0 — GAP-2026-08-14-TAXONOMY-ORDER) ═══
# The ORDER in which subtopics enter this manifest is the exam's PERMANENT
# order: notes_core.assign_numbering derives the S/T/ST unit numbers from
# manifest insertion order and preserves them verbatim forever after (a
# re-run never renumbers a delivered unit). The taxonomy xlsx above emits
# rows in this same order, and the operator uploads to the portal top to
# bottom. Three consequences, all binding:
#   (1) FIRST EXTRACTION OF A NEW EXAM: enter each topic's subtopics in
#       TEACHING ORDER — the official syllabus order by default (syllabi are
#       written basics-first), adjusted by SME judgement where the syllabus
#       order is not pedagogical. Alphabetical entry is a DEFECT: it freezes
#       an arbitrary order into every filename, title number and portal link
#       the exam will ever ship.
#   (2) RE-RUNS APPEND, NEVER INSERT: a Step-5 re-run that discovers a new
#       subtopic adds it at the END of its topic's block, so manifest order
#       and the persisted numbering can never disagree mid-list.
#   (3) EXISTING EXAMS ARE NEVER REORDERED: persisted numbering makes a
#       reorder cosmetic at best and a filename churn at worst. The fix for
#       an exam whose order is already frozen is none — its numbering was
#       taken from syllabus order at first extraction and stands.
def write_subtopic_manifest(entries, exam_code, exam_meta=None, progress=None,
                            frequency_scope='all', exam_config=None):
    """
    v2.4 — Write [ExamCode]_subtopic_manifest.json: the AUTHORITATIVE id↔name
    registry and the formal cross-step contract artifact.
    v2.23 — also carries the THREE-AXIS machine data Step 6 reads without re-parsing PYQ:
      • per subtopic: observed_axis2, presentation_family, axis2_capability
      • top-level 'axis_distribution': {SUBJECT: <compute_section_axis_distribution()>}
      • top-level 'axis_distribution_by_exam_section' (v2.26): the same statistic counted
        per EXAM SECTION via exam_config q_ranges. Step 6 PREFERS this; without it Step 6
        must sum every subject and split by section SIZE, which mis-assigns the mix
        (reference exam: measured A 1.4 / B 1.0 / C 2.0 vs apportioned A 2.2 / B 0.7 / C 1.4).
        (needs `progress`; omitted per-section when progress is absent — section_rules.md
        remains the authoritative human-readable copy either way).

    This manifest is the SINGLE SOURCE OF TRUTH for the subtopic vocabulary.
    Step 6 (Blueprint) and Step 7 (Create) MUST read it and reference subtopics
    by subtopic_id. They never invent ids; an unknown id is a HARD STOP.

    Structure:
    {
      "exam_code": "...",
      "manifest_version": "1.0",
      "generated_by": "Framework_MockTestAnalyse v2.53",
      "id_recipe": "<section_prefix>.<topic_slug>.<subtopic_slug> via slugify v2.4",
      "subtopics": {
         "<subtopic_id>": {
            "display_name": "...",      # decorative; may change without breaking joins
            "section": "...",
            "topic": "...",
            "concept_group": "...",     # carried for convenience; NOT part of the id
            "format": "TEXT|PASSAGE|FIGURAL|DI|...",
            "inherently_visual": false,   // v2.22: true if keyword heuristic fired
            "mandates": {               # structured MANDATE data (not prose)
               "mandatory_every_mock": false,
               "alternation_group": null,   # e.g. "ci_si" ; members alternate, never co-occur
               "min_per_series_window": null
            }
         }, ...
      },
      "alternation_groups": {           # groups whose members must NOT co-occur in one mock
         "ci_si": ["qa.interest.simple_interest", "qa.interest.compound_interest"]
      },
      "mandatory_every_mock": [ "<id>", ... ]   # flat list for fast Step-1/2 checks
    }

    MANDATE EXTRACTION (exam-agnostic, v2.10). Three round-trippable fields per
    subtopic, emitted by format_entry and read here AND by
    rebuild_subtopic_manifest_from_section_rules():
      • mandatory_every_mock — an explicit entry field mandate_every_mock wins;
        else _mandate_from_note() (NOTE mentions MANDATORY *and* an every/per
        mock|paper phrase, sentence-independent). This replaces the pre-v2.10
        single-sentence, mock-only regex that missed wording like "1Q per every paper".
      • alternation_group — the authored group name on BOTH members (e.g. set
        alternation_group='ci_si' on Simple Interest AND Compound Interest); the
        manifest groups members by that name. Members must NOT co-occur in one mock.
      • min_per_series_window — authored cadence integer (reserved for the Issue-2b
        window/cadence enforcement; carried through as data, inert until then).
    Because format_entry now writes all three into section_rules, the manifest is
    fully reproducible from the section_rules FILE alone — no ephemeral entry state.
    """
    import json, re
    out = f'/mnt/user-data/outputs/{exam_code}_subtopic_manifest.json'
    meta = exam_meta or {}
    overrides = meta.get('section_prefix_overrides', {})

    manifest = {
        'exam_code': exam_code,
        'manifest_version': '1.0',
        'generated_by': FRAMEWORK_STAMP,
        'id_recipe': '<section_prefix>.<topic_slug>.<subtopic_slug>; section_prefix=word-initials (gir/ga/qa/ec), slugify v2.4',
        'subtopics': {},
        'alternation_groups': {},
        'mandatory_every_mock': [],
        # v2.11 — the three mandate types a flat per-id list cannot express (Issue 2b):
        'mandatory_groups': {},   # {group: {members:[ids], min:int}} — >=min members present per mock
        'cadence_windows': {},    # {id: N}  — subtopic must appear >=1 in every N-mock window
        'min_counts': {},         # {id: k}  — subtopic must have >=k Q per mock
        'axis_distribution': {},  # v2.23 {SUBJECT: per-subject format-distribution target}
        'axis_distribution_by_exam_section': {},  # v2.26 {EXAM SECTION: same, measured directly}
        'pattern_eras': {}        # v2.25 per-paper era + the scope used (audit trail)
    }

    # v2.23 per-section axis distribution (needs the question lists in `progress`).
    # v2.25 — the axis distribution is a MIX quantity, so it obeys frequency_scope exactly
    # as the Frequency xlsx does. Two protections already existed and both are kept:
    #   (a) compute_section_axis_distribution() windows to the 3 most recent distinct years,
    #       which for most pattern changes is already entirely current-era; and
    #   (b) bc.derive_axis_schedule() (Framework_Blueprint v1.36) rescales every axis to
    #       sec_qs, so the SIZE is right even when the measurement era is not.
    # Neither fixes the residual case where the pattern changed WITHIN the last 3 years:
    # there the 3-year window straddles two patterns and the class PROPORTIONS are blended.
    # Era-scoping closes that gap at the source. `progress` is never mutated — the filtered
    # structure is a counting view (bc.filter_progress_to_eras returns a copy), so §14
    # pattern synthesis below still sees every era.
    if progress:
        _axis_progress = progress
        if frequency_scope == 'current-era' and exam_config:
            import blueprint_core as bc
            _eras = bc.paper_eras_from_progress(progress, exam_config)
            _filtered, _st = bc.filter_progress_to_eras(progress, _eras,
                                                        keep=('current',))
            # Never trade a real distribution for an empty one: if era-scoping would leave
            # nothing to measure, keep the full-corpus axis and say so. A blended axis that
            # is rescaled to the right size beats no axis at all (status='no_pyq' would
            # switch the whole three-axis feature off for this section).
            if _st['kept_questions'] > 0:
                _axis_progress = _filtered
            else:
                print("  NOTE: era-scoped axis skipped — no current-era questions; "
                      "using full-corpus axis (still rescaled to sec_qs at Step 6).")
        _by_sec = {}
        for e in entries:
            _by_sec.setdefault(e['section'], []).append(e)
        for _sec, _ents in _by_sec.items():
            _ax = compute_section_axis_distribution(_ents, _axis_progress)
            if _ax:
                manifest['axis_distribution'][_sec] = _ax

        # ── v2.26 (GAP-2026-08-06-AXIS1) — MEASURE THE EXAM SECTIONS DIRECTLY ──────
        # The map above is keyed by SUBJECT (the taxonomy's top level). Step 6 needs it
        # per EXAM SECTION (A/B/C), and until now bridged that gap by SUMMING every
        # subject and splitting the total by section SIZE. That is a real distortion,
        # not a rounding detail — on the reference exam:
        #
        #     measured per section   : A 1.4   B 1.0   C 2.0   (figures/paper)
        #     size-apportioned       : A 2.2   B 0.7   C 1.4
        #
        # It hands the FEWEST figures to Section C, which actually carries the MOST
        # (5 of the 8 figures in the most recent paper). Sections are format bands, not
        # content domains; their format mix has no reason to track their question count.
        #
        # Counting them directly is possible because every question already carries its
        # q_num, and exam_config already carries each section's q_range. Emitted under a
        # SEPARATE key so a consumer that wants the subject view still has it, and a
        # pre-v2.26 blueprint that never looks here is completely unaffected.
        _ranges = []
        for _s in (exam_config or {}).get('sections', []) or []:
            _r = _s.get('q_range') or []
            if len(_r) >= 2:
                _ranges.append((_s.get('section_name') or _s.get('name'),
                                int(_r[0]), int(_r[1])))
        if _ranges:
            manifest['axis_distribution_by_exam_section'] = {}
            for _nm, _lo, _hi in _ranges:
                # A counting VIEW over the same question lists — `progress` is never
                # mutated, exactly as the era filter above leaves it untouched.
                _sec_view, _seen = {}, False
                for _k, _qs in _axis_progress.items():
                    _keep = [q for q in _qs
                             if q.get('q_num') is not None and _lo <= int(q['q_num']) <= _hi]
                    if _keep:
                        _sec_view[_k] = _keep
                        _seen = True
                if not _seen:
                    continue      # section not represented (out-of-pattern era) — skip
                _ents_all = [{'section': k[0], 'topic': k[1], 'subtopic': k[2]}
                             for k in _sec_view]
                _ax = compute_section_axis_distribution(_ents_all, _sec_view)
                if _ax:
                    _ax['measured_by'] = 'measured'   # provenance → blueprint.axis_measured_by
                    manifest['axis_distribution_by_exam_section'][_nm] = _ax

    # v2.25 — record every paper's pattern era in the manifest so the decision is auditable
    # downstream and after the fact. Purely additive: absent on a pre-v2.25 manifest, and no
    # consumer is required to read it.
    if progress and exam_config:
        import blueprint_core as bc
        try:
            _pe = bc.paper_eras_from_progress(progress, exam_config)
            manifest['pattern_eras'] = {
                'frequency_scope': frequency_scope,
                'papers': {f'{y}|{sh}': info for (y, sh), info in sorted(
                    _pe.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1])))},
                'era_counts': {e: sum(1 for i in _pe.values() if i['era'] == e)
                               for e in bc.PATTERN_ERAS},
            }
        except ValueError:
            pass          # exam_config without sections[] — nothing to classify against

    seen_ids = {}
    for e in entries:
        # Reuse the id stamped by write_section_rules (e['subtopic_id']) so the
        # manifest id is IDENTICAL to the section_rules block id. Only recompute as
        # a fallback if write_subtopic_manifest is ever called before stamping.
        sid = e.get('subtopic_id')
        if not sid:
            sid = make_subtopic_id(e['section'], e['topic'], e['subtopic'],
                                   build_section_prefix_map(
                                       sorted({x['section'] for x in entries}), overrides))
            base = sid; n = 2
            key = (e['section'], e['topic'], e['subtopic'])
            while sid in seen_ids and seen_ids[sid] != key:
                sid = f'{base}_{n}'; n += 1
        seen_ids[sid] = (e['section'], e['topic'], e['subtopic'])

        note = (e.get('NOTE') or e.get('note') or e.get('note_text') or '')
        # v2.10: an explicit mandate_every_mock (from the entry / round-tripped from
        # section_rules) wins; otherwise the robust sentence-independent detector
        # (_mandate_from_note) replaces the brittle single-sentence, mock-only regex
        # that missed wording like "MANDATORY ... 1Q per every paper".
        mand_every = bool(e['mandate_every_mock']) if 'mandate_every_mock' in e \
                     else _mandate_from_note(note)
        manifest['subtopics'][sid] = {
            'display_name': e['subtopic'],
            'section': e['section'],
            'topic': e['topic'],
            'concept_group': e.get('concept_group') or _derive_concept_group(e),
            'question_mechanic': e.get('question_mechanic') or _derive_question_mechanic(e),  # v2.24
            'form_key': e.get('form_key') or _derive_form_key(e),                             # v2.24
            'collision_domain': e.get('collision_domain') or _derive_collision_domain(e),     # v2.24
            'format': e.get('format', 'TEXT'),
            'inherently_visual': bool(e.get('inherently_visual', False)),   # v2.22
            # v2.26 — Step 6 copies these into blueprint.subtopic_list and Step 7 ranks
            # the Axis-1 budget by them. Absent on a pre-v2.26 manifest, in which case
            # bc.rank_figural_candidates() degrades to irreducible-first ordering and the
            # budget is still enforced — the cap is what matters; the ranking is what
            # makes the capped set faithful.
            'figural_q_count'  : int(e.get('figural_q_count', 0)),
            'figural_rate'     : float(e.get('figural_rate', 0.0)),
            'figural_reducible': bool(e.get('figural_reducible', True)),
            'di_q_count'       : int(e.get('di_q_count', 0)),          # v2.43
            'di_rate'          : float(e.get('di_rate', 0.0)),         # v2.43
            'di_reducible'     : bool(e.get('di_reducible', True)),    # v2.43
            # v2.23 THREE-AXIS per-subtopic capability (Step 6 rare-format reachability;
            # Step 7 renders only within axis2_capability — fabrication banned).
            'observed_axis2': e.get('observed_axis2', {}),
            'presentation_family': e.get('presentation_family'),
            'axis2_capability': e.get('axis2_capability', ['DIRECT']),
            'mandates': {
                'mandatory_every_mock': mand_every,
                'alternation_group': e.get('alternation_group'),
                'min_per_series_window': _as_mandate_int(e.get('min_per_series_window')),
                'mandatory_group': e.get('mandatory_group'),          # v2.11 group-presence
                'min_count': _as_mandate_int(e.get('min_count'))              # v2.11 min Q per mock
            }
        }
        if mand_every:
            manifest['mandatory_every_mock'].append(sid)
        ag = e.get('alternation_group')
        if ag:
            manifest['alternation_groups'].setdefault(ag, [])
            if sid not in manifest['alternation_groups'][ag]:
                manifest['alternation_groups'][ag].append(sid)
        # v2.11 rollups (Issue 2b) — group-presence, cadence, min-count:
        mg = e.get('mandatory_group')
        if mg and mg != 'none':
            g = manifest['mandatory_groups'].setdefault(mg, {'members': [], 'min': 1})
            if sid not in g['members']:
                g['members'].append(sid)
        _win = _as_mandate_int(e.get('min_per_series_window'))
        if _win:
            manifest['cadence_windows'][sid] = _win
        _mc = _as_mandate_int(e.get('min_count'))
        if _mc:
            manifest['min_counts'][sid] = _mc

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'Written: {out} ({len(manifest["subtopics"])} subtopic ids, '
          f'{len(manifest["mandatory_every_mock"])} mandatory-every-mock, '
          f'{len(manifest["alternation_groups"])} alternation groups, '
          f'{len(manifest["mandatory_groups"])} group-presence, '
          f'{len(manifest["cadence_windows"])} cadence, '
          f'{len(manifest["min_counts"])} min-count)')
    write_taxonomy_xlsx(manifest, exam_code)   # v2.24 — human-readable companion
    return out


def rebuild_subtopic_manifest_from_section_rules(section_rules_path, exam_code):
    """v2.10 — Reconstruct a COMPLETE subtopic_manifest.json from an existing
    section_rules.md ALONE (no source PYQ, no in-memory entries). This is the
    supported path to (re)generate a MISSING or INCOMPLETE manifest — e.g. a project
    that has section_rules + blueprint but lost the manifest, or one whose mandate
    markers were edited by hand and must be re-minted.

    It parses every '--- Subtopic: --- block and reads the round-trippable mandate
    lines emitted by format_entry (mandate_every_mock / alternation_group /
    min_per_series_window), falling back to the robust NOTE detector
    (_mandate_from_note) only when an explicit mandate_every_mock line is absent
    (legacy blocks written before v2.10). ONLY id-carrying blocks enter the manifest
    join; a block without subtopic_id cannot be joined by Step 6/7, so it is skipped
    and surfaced as a WARN (mint its id in Step 5, or add one, then re-run).

    Output schema is byte-identical to write_subtopic_manifest(). Exam-agnostic —
    zero subtopic names hardcoded.
    """
    import json, re, ast
    text = open(section_rules_path, encoding='utf-8').read()
    manifest = {
        'exam_code': exam_code,
        'manifest_version': '1.0',
        'generated_by': f'{FRAMEWORK_STAMP} (rebuild_from_section_rules)',
        'id_recipe': '<section_prefix>.<topic_slug>.<subtopic_slug>; slugify v2.4',
        'subtopics': {},
        'alternation_groups': {},
        'mandatory_every_mock': [],
        'mandatory_groups': {},   # v2.11 group-presence
        'cadence_windows': {},    # v2.11 cadence
        'min_counts': {},         # v2.11 min Q per mock
        'axis_distribution': {}   # v2.23 (round-tripped from the AXIS_DISTRIBUTION block below)
    }

    def _lit(s, default):
        """Safe Python-literal parse for round-tripped axis fields ({...}/[...]/floats)."""
        try:
            return ast.literal_eval(s.strip())
        except Exception:
            return default
    EXPL_MAND = re.compile(r'^\s*mandate_every_mock:\s*(true|false)\s*$', re.I | re.M)
    EXPL_ALT  = re.compile(r'^\s*alternation_group:\s*(\S+)\s*$', re.M)
    EXPL_WIN  = re.compile(r'^\s*min_per_series_window:\s*(\S+)\s*$', re.M)
    EXPL_GRP  = re.compile(r'^\s*mandatory_group:\s*(\S+)\s*$', re.M)          # v2.11
    EXPL_MINC = re.compile(r'^\s*min_count:\s*(\S+)\s*$', re.M)               # v2.11
    ID_RE     = re.compile(r'^\s*subtopic_id:\s*(\S+)\s*$', re.M)
    SEC_RE    = re.compile(r'^\s*section:\s*(.+)$', re.M)
    TOP_RE    = re.compile(r'^\s*topic:\s*(.+)$', re.M)
    FMT_RE    = re.compile(r'^\s*format:\s*(\S+)\s*$', re.M)
    INHERENT_RE = re.compile(r'^\s*inherently_visual:\s*(true|false)\s*$', re.I | re.M)  # v2.22
    # v2.26 (GAP-2026-08-06-AXIS1) — round-trip the figural rate fields. Tolerant by
    # construction: a block written before v2.26 carries none of them, and every
    # consumer defaults (rate 0.0, reducible True) to the pre-v2.26 reading. A parser
    # that HALTED on the older shape would strand ~200 deployed exams on re-read.
    FIGRATE_RE = re.compile(r'^\s*figural_rate:\s*([0-9]*\.?[0-9]+)\s*$', re.I | re.M)
    FIGQC_RE   = re.compile(r'^\s*figural_q_count:\s*(\d+)\s*$', re.I | re.M)
    FIGRED_RE  = re.compile(r'^\s*figural_reducible:\s*(true|false)\s*$', re.I | re.M)
    OPTIMG_RE  = re.compile(r'^\s*option_image_rate:\s*([0-9]*\.?[0-9]+)\s*$', re.I | re.M)
    DIRATE_RE  = re.compile(r'^\s*di_rate:\s*([0-9]*\.?[0-9]+)\s*$', re.I | re.M)   # v2.43
    DIQC_RE    = re.compile(r'^\s*di_q_count:\s*(\d+)\s*$', re.I | re.M)
    DIRED_RE   = re.compile(r'^\s*di_reducible:\s*(true|false)\s*$', re.I | re.M)
    CG_RE     = re.compile(r'^\s*concept_group:\s*(.+)$', re.M)
    QM_RE      = re.compile(r'^\s*question_mechanic:\s*(.+)$', re.M)    # v2.24
    FORMKEY_RE = re.compile(r'^\s*form_key:\s*(.+)$', re.M)             # v2.24
    CDOM_RE    = re.compile(r'^\s*collision_domain:\s*(.+)$', re.M)     # v2.24
    NOTE_RE   = re.compile(r'^\s*NOTE\s*:\s*(.+)$', re.M | re.I)
    OBSAX_RE  = re.compile(r'^\s*observed_axis2:\s*(.+)$', re.M)          # v2.23
    PFAM_RE   = re.compile(r'^\s*presentation_family:\s*(.+)$', re.M)     # v2.23
    AX2CAP_RE = re.compile(r'^\s*axis2_capability:\s*(.+)$', re.M)        # v2.23

    id_less = []
    for raw in re.split(r'\n--- Subtopic:', text)[1:]:
        disp  = raw.split('---', 1)[0].strip()
        sid_m = ID_RE.search(raw)
        if not sid_m:
            id_less.append(disp)                 # cannot be joined — skip, warn below
            continue
        sid    = sid_m.group(1)
        note_m = NOTE_RE.search(raw)
        note   = note_m.group(1) if note_m else ''
        em = EXPL_MAND.search(raw)
        mand = (em.group(1).lower() == 'true') if em else _mandate_from_note(note)
        av = EXPL_ALT.search(raw)
        ag = av.group(1) if (av and av.group(1).lower() != 'none') else None
        wv  = EXPL_WIN.search(raw)
        win = _as_mandate_int(wv.group(1)) if wv else None
        gv  = EXPL_GRP.search(raw)                                   # v2.11
        grp = gv.group(1) if (gv and gv.group(1).lower() != 'none') else None
        mcv = EXPL_MINC.search(raw)                                  # v2.11
        mc  = _as_mandate_int(mcv.group(1)) if mcv else None
        _sec_r = SEC_RE.search(raw).group(1).strip() if SEC_RE.search(raw) else ''   # v2.24
        _fmt_r = FMT_RE.search(raw).group(1) if FMT_RE.search(raw) else 'TEXT'        # v2.24
        _ax_r  = derive_mechanic(_sec_r, disp, None, '', _fmt_r, sid)                 # v2.24
        manifest['subtopics'][sid] = {
            'display_name':  disp,
            'section':       (SEC_RE.search(raw).group(1).strip() if SEC_RE.search(raw) else ''),
            'topic':         (TOP_RE.search(raw).group(1).strip() if TOP_RE.search(raw) else ''),
            'concept_group': (CG_RE.search(raw).group(1).strip()  if CG_RE.search(raw)  else _ax_r['family']),
            'question_mechanic': (QM_RE.search(raw).group(1).strip() if QM_RE.search(raw) else _ax_r['mechanic']),   # v2.24
            'form_key': (FORMKEY_RE.search(raw).group(1).strip() if FORMKEY_RE.search(raw) else _ax_r['form_key']),  # v2.24
            'collision_domain': (CDOM_RE.search(raw).group(1).strip() if CDOM_RE.search(raw) else _ax_r['collision_domain']),  # v2.24
            'format':        (FMT_RE.search(raw).group(1)         if FMT_RE.search(raw) else 'TEXT'),
            'inherently_visual': (INHERENT_RE.search(raw).group(1).lower() == 'true'
                                  if INHERENT_RE.search(raw) else False),   # v2.22
            'figural_rate': (float(FIGRATE_RE.search(raw).group(1))
                             if FIGRATE_RE.search(raw) else 0.0),            # v2.26
            'figural_q_count': (int(FIGQC_RE.search(raw).group(1))
                                if FIGQC_RE.search(raw) else 0),             # v2.26
            'figural_reducible': (FIGRED_RE.search(raw).group(1).lower() == 'true'
                                  if FIGRED_RE.search(raw) else True),       # v2.26
            'option_image_rate': (float(OPTIMG_RE.search(raw).group(1))
                                  if OPTIMG_RE.search(raw) else 0.0),        # v2.44
            'di_rate': (float(DIRATE_RE.search(raw).group(1))
                        if DIRATE_RE.search(raw) else 0.0),                  # v2.43
            'di_q_count': (int(DIQC_RE.search(raw).group(1))
                           if DIQC_RE.search(raw) else 0),                   # v2.43
            'di_reducible': (DIRED_RE.search(raw).group(1).lower() == 'true'
                             if DIRED_RE.search(raw) else True),             # v2.43
            # v2.23 THREE-AXIS per-subtopic (round-tripped; safe defaults for legacy blocks)
            'observed_axis2':      (_lit(OBSAX_RE.search(raw).group(1), {})
                                    if OBSAX_RE.search(raw) else {}),
            'presentation_family': ((lambda v: None if v in ('None', '') else v)
                                    (PFAM_RE.search(raw).group(1).strip())
                                    if PFAM_RE.search(raw) else None),
            'axis2_capability':    (_lit(AX2CAP_RE.search(raw).group(1), ['DIRECT'])
                                    if AX2CAP_RE.search(raw) else ['DIRECT']),
            'mandates': {
                'mandatory_every_mock': mand,
                'alternation_group':    ag,
                'min_per_series_window': win,
                'mandatory_group':      grp,     # v2.11 group-presence
                'min_count':            mc       # v2.11 min Q per mock
            }
        }
        if mand and sid not in manifest['mandatory_every_mock']:
            manifest['mandatory_every_mock'].append(sid)
        if ag:
            manifest['alternation_groups'].setdefault(ag, [])
            if sid not in manifest['alternation_groups'][ag]:
                manifest['alternation_groups'][ag].append(sid)
        # v2.11 rollups (Issue 2b) — group-presence, cadence, min-count:
        if grp:
            g = manifest['mandatory_groups'].setdefault(grp, {'members': [], 'min': 1})
            if sid not in g['members']:
                g['members'].append(sid)
        if win:
            manifest['cadence_windows'][sid] = win
        if mc:
            manifest['min_counts'][sid] = mc

    # v2.23 — round-trip the per-section AXIS_DISTRIBUTION block so a rebuilt manifest is
    # schema-identical to the write path. Each '=== SECTION: X ===' chunk may carry an
    # 'axis_distribution:' sub-block of indented 'key: <python-literal>' lines.
    _AXKEYS = {'recent_years', 'n_papers_recent', 'mocks_per_window', 'negative_rate',
               'axis1_per_paper', 'axis2_per_paper', 'axis3_per_paper', 'axis2_audit_mode'}
    for chunk in re.split(r'^=== SECTION:\s*', text, flags=re.M)[1:]:
        sec_name = chunk.split('===', 1)[0].strip()
        m = re.search(r'^axis_distribution:\s*$', chunk, flags=re.M)
        if not m:
            continue
        block = {}
        for ln in chunk[m.end():].splitlines():
            if not ln.startswith('  '):           # indented sub-lines only; stop at dedent
                if ln.strip() == '':
                    continue
                break
            km = re.match(r'\s+(\w+):\s*(.+)$', ln)
            if km and km.group(1) in _AXKEYS:
                block[km.group(1)] = _lit(km.group(2), km.group(2).strip())
        if block:
            manifest['axis_distribution'][sec_name] = block

    out = f'/mnt/user-data/outputs/{exam_code}_subtopic_manifest.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'Rebuilt: {out} ({len(manifest["subtopics"])} ids, '
          f'{len(manifest["mandatory_every_mock"])} mandatory-every-mock, '
          f'{len(manifest["alternation_groups"])} alternation groups, '
          f'{len(manifest["mandatory_groups"])} group-presence, '
          f'{len(manifest["cadence_windows"])} cadence, '
          f'{len(manifest["min_counts"])} min-count)')
    if id_less:
        print(f'WARN: {len(id_less)} subtopic block(s) had NO subtopic_id and were '
              f'SKIPPED (cannot be joined by Step 6/7): {id_less[:8]}'
              f'{" ..." if len(id_less) > 8 else ""}. Mint ids in Step 5 or add them, '
              f'then re-run rebuild.')
    write_taxonomy_xlsx(manifest, exam_code)   # v2.24 — human-readable companion
    return out


def format_entry(e):
    # BUG-C04 fix (v2.3): option_format written as full dict per §14 BUG-B15 spec
    ofmt = e['option_format']
    if isinstance(ofmt, dict):
        ofmt_primary  = ofmt.get('primary', 'single_value')
        ofmt_recent   = ofmt.get('recent_format', ofmt_primary)
        ofmt_changed  = str(ofmt.get('changed_recently', False)).lower()
        ofmt_all      = ofmt.get('all_observed', [ofmt_primary])
    else:
        ofmt_primary = ofmt_recent = str(ofmt)
        ofmt_changed = 'false'
        ofmt_all     = [str(ofmt)]
    lines = [
        '', f'--- Subtopic: {e["subtopic"]} ---',
        # ── subtopic_id (v2.4 — CROSS-STEP JOIN KEY, the single source of truth) ──
        # subtopic_id is the STABLE machine identifier that Step 6 and Step 7 use to
        # join blueprint.json ↔ section_rules.md. It is minted HERE (Step 5) and
        # ONLY here. Downstream steps copy it verbatim and NEVER invent their own.
        # The display name ("--- Subtopic: X ---") is decorative and may be reworded
        # freely WITHOUT breaking the pipeline, because the id (not the name) is the
        # load-bearing join key. See §15 SUBTOPIC_ID CONTRACT for the full recipe.
        f'subtopic_id: {e["subtopic_id"]}',
        f'section: {e["section"]}', f'topic: {e["topic"]}',
        f'observed_count: {e["observed_count"]}', f'format: {e["format"]}',
        f'inherently_visual: {str(e.get("inherently_visual", False)).lower()}',
        # ── v2.26 (GAP-2026-08-06-AXIS1) ────────────────────────────────────────────
        # figural_rate is the SHARE OF THIS SUBTOPIC'S OBSERVED QUESTIONS that carried a
        # figure — read `4/39` not `10%` when you are debugging, because the denominator
        # is what the old boolean threw away. Step 7 ranks claims on the scarce Axis-1
        # budget by this number, so a subtopic the exam illustrates 79% of the time
        # (organic stereochemistry) outranks one it illustrates 3% of the time (complex
        # formation) — both of which the pre-v2.26 flag marked identically FIGURAL.
        f'figural_q_count: {int(e.get("figural_q_count", 0))}',
        f'figural_rate: {float(e.get("figural_rate", 0.0)):.4f}',
        # figural_reducible: false ⇒ the OPTIONS are images, so there is no text form of
        # this question. Granted a figure even over budget (bc.axis_grant_figural rule 2);
        # the audit raises its expectation by the same count so the overage is silent.
        f'figural_reducible: {str(e.get("figural_reducible", True)).lower()}',
        # v2.44 — share of this subtopic's FIGURAL questions whose figure is in the
        # OPTIONS. Read '2/15' not '13%' when debugging: the denominator is exactly what
        # the pre-v2.44 any() discarded, and discarding it made 21 subtopics exempt from
        # a budget of 5 on the strength of one question each.
        f'option_image_rate: {float(e.get("option_image_rate", 0.0)):.4f}',
        # v2.43 — DI rate, read by Step 7 to rank claims on the Axis-1 DI budget and by
        # A-AXIS1 to know whether a DI target is reachable at all.
        f'di_q_count: {int(e.get("di_q_count", 0))}',
        f'di_rate: {float(e.get("di_rate", 0.0)):.4f}',
        f'di_reducible: {str(e.get("di_reducible", True)).lower()}',
        # REPLACEMENT_RULE — what to render when a FIGURAL-CAPABLE question does NOT win
        # a budget slot. It is NOT a downgrade to a worse question: it draws from this
        # subtopic's OWN observed text patterns (PYQ_STEM_PATTERNS below), which is the
        # majority shape for every subtopic whose figural_rate is under 50%. Required by
        # HS-16 for any subtopic that can be denied a figure — which, post-v2.26, is every
        # reducible FIGURAL subtopic, so it is emitted unconditionally rather than left to
        # a hand-authored ban list (the reference exam had 46 FIGURAL subtopics and ZERO
        # REPLACEMENT_RULE blocks, so nothing was ever downgradable and the cap could not
        # have been honoured even if Step 7 had tried).
        ('REPLACEMENT_RULE: render as TEXT using this subtopic\'s observed '
         'PYQ_STEM_PATTERNS; preserve subtopic, difficulty band and answer_cardinality; '
         'never substitute another subtopic'
         if str(e.get('format', 'TEXT')).upper() == 'FIGURAL'
            and bool(e.get('figural_reducible', True))
         else 'REPLACEMENT_RULE: none (not reducible)'),
        f'option_format_primary: {ofmt_primary}',
        f'option_format_recent: {ofmt_recent}',
        f'option_format_changed_recently: {ofmt_changed}',
        f'option_format_all_observed: {ofmt_all}',
        f'OMML_required: {str(e["OMML_required"]).lower()}',
        f'negative_question_freq: {e["negative_question_freq"]}%',
        f'answer_type: {e.get("answer_type", "option")}',
        f'nat_freq: {e.get("nat_freq", 0)}%',
        f'answer_cardinality: {e.get("answer_cardinality", "single")}',
        f'msq_freq: {e.get("msq_freq", 0)}%',
        # v2.23 THREE-AXIS (CATEGORY B). observed_axis2 = PYQ-observed counts; axis2_capability
        # = faithful forms Step 6/7 may use; presentation_family = Step 7 menu key. Single-line
        # so rebuild_subtopic_manifest_from_section_rules() can round-trip them.
        f'observed_axis2: {e.get("observed_axis2", {})}',
        f'presentation_family: {e.get("presentation_family")}',
        f'axis2_capability: {e.get("axis2_capability", [])}',
        f'fill_in_blank: {e["fill_in_blank"]}',
        f'linked_group_size: {e["linked_group_size"]}',
        f'max_per_paper: {e.get("max_per_paper", 0)}',
        f'typical_per_paper: {e.get("typical_per_paper", 0)}',
        f'stem_word_count: min={e["stem_word_count"]["min"]} '
          f'max={e["stem_word_count"]["max"]} typical={e["stem_word_count"]["typical"]}',
        f'sub_type_label: {e["sub_type_label"]}',
        # ── CONCEPT_GROUP and QUESTION_MECHANIC (MANDATORY — Step 7 relies on these) ──
        # CONCEPT_GROUP: broad theme grouping (Step 7 resolve_concept_group priority #1).
        # QUESTION_MECHANIC: the normalised student task for CHECK D mechanic-collision.
        # Both MUST be written here. If absent → Step 7 falls to keyword-matching
        # fallback which FAILS for non-standard subtopic names → mechanic collisions
        # like synonym×2 or antonym×2 in the same mock go undetected.
        #
        # HOW TO DERIVE concept_group (exam-agnostic):
        #   Read the PYQ_STEM_PATTERNS template for this subtopic.
        #   Group all subtopics that share the same broad topic theme.
        #   Example: all "find missing number" variants → concept_group: missing_number
        #   Example: all "series" variants              → concept_group: series
        #   Use the SAME string for every subtopic in the same theme group.
        #
        # HOW TO DERIVE question_mechanic (exam-agnostic):
        #   Normalise the stem instruction to its atomic task:
        #     "opposite in meaning" / "ANTONYM"       → antonym
        #     "similar in meaning"  / "SYNONYM"       → synonym
        #     "find the error"                        → error_detection
        #     "improve the sentence" / "best replaces"→ sentence_improvement
        #     "one word substitution"                 → one_word_substitution
        #     "fill in the blank"                     → fill_in_blank
        #     "meaning of idiom/phrase"               → idiom
        #     "select the correctly spelt"            → spelling
        #     "active/passive voice"                  → voice
        #     "direct/indirect speech"                → narration
        #     (derive from PYQ_STEM_PATTERNS template — never hardcode exam names)
        #   Two subtopics with the SAME question_mechanic MUST NOT appear in
        #   the same mock (MockCreate mandate-7 CHECK D).
        #
        # SYNONYM vs ANTONYM: these are DIFFERENT mechanics. Both CAN appear in
        # one mock (one synonym Q + one antonym Q = different mechanics = allowed).
        # But two synonym Qs = SAME mechanic = BLOCKED by CHECK D. Always separate.
        f'concept_group: {e.get("concept_group") or _derive_concept_group(e)}',
        f'question_mechanic: {e.get("question_mechanic") or _derive_question_mechanic(e)}',
        f'form_key: {e.get("form_key") or _derive_form_key(e)}',                     # v2.24 (BV-10a HARD identity)
        f'collision_domain: {e.get("collision_domain") or _derive_collision_domain(e)}',  # v2.24 (default=section)
        # ── v2.10 MANDATE ROUND-TRIP: emit the three mandate fields as parseable lines
        #    so the manifest is reproducible from THIS FILE (not only from in-memory
        #    entries). mandate_every_mock defaults to the robust NOTE detector; an explicit
        #    e['mandate_every_mock'] overrides. alternation_group + min_per_series_window
        #    are authored fields ('none' when unset). write_subtopic_manifest AND
        #    rebuild_subtopic_manifest_from_section_rules read these back; Step 6 consumes
        #    the manifest (RULE M1/M2); Step 7 reads it (S3-17). These lines are also the
        #    HAND-EDIT point: set 'mandate_every_mock: true' / 'alternation_group: <name>'
        #    on a block and regenerate the manifest to change policy — no re-analysis.
        f'mandate_every_mock: {str(e.get("mandate_every_mock", _mandate_from_note(e.get("note_text") or e.get("NOTE") or ""))).lower()}',
        f'alternation_group: {e.get("alternation_group") or "none"}',
        f'min_per_series_window: {e.get("min_per_series_window") if e.get("min_per_series_window") not in (None, "") else "none"}',
        # v2.11 (Issue 2b) — two more round-trippable mandate fields:
        #   mandatory_group : a group name; a mock must contain >=1 member of the group
        #                     (group-presence, e.g. any one member of a 3D-solids group).
        #   min_count       : minimum questions of THIS subtopic per mock (>=k).
        f'mandatory_group: {e.get("mandatory_group") or "none"}',
        f'min_count: {e.get("min_count") if e.get("min_count") not in (None, "") else "none"}'
        # _derive_concept_group() and _derive_question_mechanic() are defined below.
        # They extract from PYQ_STEM_PATTERNS when not explicitly set in input data.
    ]
    for p in e.get('PYQ_STEM_PATTERNS', []):
        # BUG-C02 fix (v2.3): raw_count and years written — QV-11 uses years
        dep_tag = ' [DEPRECATED]' if p.get('deprecated') else ''
        lines += [
            f'  {p["id"]}: "{p["template"]}"',
            f'      approach: "{p.get("approach","")}"',
            f'      frequency: {p["frequency"]}%  confidence: {p["confidence"]}{dep_tag}',
            f'      raw_count: {p.get("raw_count", 0)}',
            f'      years: {p.get("years", [])}',
            f'      note_block: {p.get("note_block","never")}',
        ]
        if p.get('note_text'): lines.append(f'      note_text: "{p["note_text"][:120]}"')
        # ── SYNC fields: read by Step 7 sub-step 4b (UL-GATE) and sub-step 4c (ANCHOR-LOCK) ──
        # underline_required: true/false — Step 7 sub-step 4b reads this to determine
        #   whether stem_underline_ranges must be computed. Set true for subtopics
        #   where the stem instruction says "underlined" (idiom, sentence_improvement,
        #   error_detection, one_word_substitution, etc.).
        #   HOW TO DETECT from PYQ: if p['template'] contains 'underlined' or 'underline'
        #   → set underline_required: true. Otherwise false.
        _ul_req = 'true' if any(kw in p.get('template','').lower()
                                for kw in ['underlined','underline']) else 'false'
        lines.append(f'      underline_required: {_ul_req}')
        # anchor_option_required: true/false — Step 7 sub-step 4c reads this to determine
        #   whether an anchor option (e.g. "No error", "No improvement required") must
        #   be pinned to a fixed position during shuffle.
        #   HOW TO DETECT from PYQ: if p['template'] contains a phrase like
        #   "select option (N) if there is no error" or "if no improvement" + option number
        #   → set anchor_option_required: true and record anchor_position.
        import re as _re
        _anch_m = _re.search(
            r'select\s+option\s*\(?(\d+|[A-Da-d])\)?.*?(?:no error|no improvement|no change)',
            p.get('template',''), _re.IGNORECASE)
        _anch_req = 'true' if _anch_m else 'false'
        lines.append(f'      anchor_option_required: {_anch_req}')
        if _anch_m:
            # anchor_position: the 1-indexed position stated in the stem
            _pos_str = _anch_m.group(1)
            _pos_int = int(_pos_str) if _pos_str.isdigit() else (ord(_pos_str.upper())-64)
            lines.append(f'      anchor_position: {_pos_int}')
        lines.append('')
    # BUG-C01 fix (v2.3): is_inferred flag written alongside criteria
    calib = e.get('PYQ_DIFFICULTY_CALIBRATION', {})
    lines += ['PYQ_DIFFICULTY_CALIBRATION:']
    for lv in ['Simple','Medium','Hard']:
        c = calib.get(lv, {'criteria':'(inferred)','is_inferred':True})
        inf_tag = ' [INFERRED]' if c.get('is_inferred', True) else ''
        lines.append(f'  {lv}: "{c["criteria"]}"{inf_tag}')
    lines.append('')
    wo = e.get('wrong_option_structure', {})
    lines += ['wrong_option_structure:',
              f'  type: {wo.get("type","varied")}',
              f'  description: "{wo.get("description","")}"']
    if wo.get('fixed_option_texts'): lines.append(f'  fixed_option_texts: {wo["fixed_option_texts"]}')
    if wo.get('shared_pool_words'):  lines.append(f'  shared_pool_words: {wo["shared_pool_words"]}')
    lines.append('')
    if e.get('PYQ_NUMBER_RANGES'):
        lines.append('PYQ_NUMBER_RANGES:')
        for var,rng in e['PYQ_NUMBER_RANGES'].items():
            lines.append(f'  {var}: {{min:{rng["min"]},max:{rng["max"]},'
                         f'multiples_of:{rng.get("multiples_of","N/A")}}}')
        lines.append('')
    if e.get('PYQ_CONTEXT_POOL'):
        cp = e['PYQ_CONTEXT_POOL']
        cp_lines = ['PYQ_CONTEXT_POOL:',
                    f'  dominant: {cp.get("dominant",[])}',
                    f'  common: {cp.get("common",[])}',
                    f'  avoid: {cp.get("avoid",[])}',
                   ]
        # NEW v2.3: write recycled_datasets and ban_recycled if present
        if cp.get('recycled_datasets'):
            cp_lines.append(f'  recycled_datasets: {cp["recycled_datasets"]}')
            cp_lines.append(f'  ban_recycled: {str(cp.get("ban_recycled", True)).lower()}')
        cp_lines.append('')
        lines += cp_lines
    if e.get('PYQ_IMAGE_ANALYSIS'):
        ia = e['PYQ_IMAGE_ANALYSIS']
        # v2.37 (GAP-2026-07-26-003 D3/D4). This emitter used to write FOUR fields.
        # aggregate_figural built NINE, so arrangement_types, complexity_dist,
        # object_types.avoid, images_analysed and images_unclear were computed and then
        # DROPPED at the artefact boundary — Step 7 could never have seen complexity or
        # arrangement even with vision working perfectly.
        #
        # vision_status is the D3 fix. In the reference run 'vision_unavailable'
        # appeared 153 times in progress.json and ZERO times in section_rules.md, so a
        # consumer reading `dominant: []` had no way to tell "this exam has no figures"
        # from "vision failed and this profile is empty". The artefact now carries its
        # own provenance.
        _ot = ia.get('object_types', {})
        lines += ['PYQ_IMAGE_ANALYSIS:',
                  f'  image_role: {ia.get("image_role","stem_only")}',
                  f'  vision_status: {ia.get("vision_status","not_applicable")}',
                  '  object_types:',
                  f'    dominant: {_ot.get("dominant",[])}',
                  f'    observed: {_ot.get("observed",[])}',
                  f'    avoid: {_ot.get("avoid",[])}',
                  f'  transformation_types: {ia.get("transformation_types",[])}',
                  f'  arrangement_types: {ia.get("arrangement_types",[])}',
                  f'  complexity_dist: {ia.get("complexity_dist",{})}',
                  f'  images_analysed: {ia.get("images_analysed",0)}',
                  f'  images_unclear: {ia.get("images_unclear",0)}',
                  f'  images_unobserved: {ia.get("images_unobserved",0)}']
        if ia.get('dominant_suppressed'):
            lines += [f'  dominant_suppressed: "{ia["dominant_suppressed"]}"']
        lines += ['']
    # BUG-C05 fix (v2.3): paragraph_count and topic_domains now written
    if e.get('PYQ_PASSAGE_STRUCTURE'):
        ps = e['PYQ_PASSAGE_STRUCTURE']
        lines += ['PYQ_PASSAGE_STRUCTURE:',
                  f'  sub_format: {ps.get("sub_format","RC")}',
                  f'  word_range: {{min:{ps.get("word_range",{}).get("min",0)},'
                    f'max:{ps.get("word_range",{}).get("max",0)}}}',
                  f'  paragraph_count: {{typical:{ps.get("paragraph_count",{}).get("typical",1)}}}',
                  f'  topic_domains_observed: {ps.get("topic_domains",{}).get("observed",[])}',
                  f'  topic_domains_avoid: {ps.get("topic_domains",{}).get("avoid",[])}',
                  f'  q_type_distribution: {ps.get("q_type_distribution",{})}', '']
    return lines

# ═══ FROM Framework_MockTestAnalyse.md §6, fence L5673-6069 (v2.53.2) — VERBATIM ═══
def run_qv(entries, taxonomy, progress):
    """
    BUG-A09 fix: QV-11 now uses global_max_year across all entries.
    BUG-B09 fix: QV-3 uses is_inferred bool from calibration dict.
    """
    results = {}
    ekeys   = {(e['section'],e['topic'],e['subtopic']):e for e in entries}

    # QV-1: Every taxonomy subtopic has an entry
    missing = [st['subtopic'] for sec,sts in taxonomy.items()
               for st in sts if (sec,st['topic'],st['subtopic']) not in ekeys]
    results['QV-1'] = ('WARN' if missing else 'PASS',
                        f'{len(missing)} missing: {missing[:5]}' if missing else 'All covered')

    # QV-1a: PYQ subtopics are in taxonomy
    pyq_subs = set(k[2] for k in ekeys)
    tax_subs = set(st['subtopic'] for sts in taxonomy.values() for st in sts)
    extra    = pyq_subs - tax_subs
    # GAP-2026-08-05-001 (SG-6). Severity RAISED from WARN to FAIL. The IDENTICAL
    # condition — a parsed subtopic that is not in the locked taxonomy — is a HARD STOP
    # at Step 4 Task 2.5 and was only a WARN here. Per Framework_DeliveryFooter §5 Q0 a
    # WARN does not force amber, so a phantom subtopic passed SILENTLY, rendered a green
    # "Step Complete" footer, and flowed into subtopic_manifest.json -> Step 6 allocation
    # -> Step 7 generation, carrying a truncated stem and dropped options with it.
    # FAIL renders F1 amber and names the check. It MUST NOT halt Step 5: per CLAUDE.md
    # a CLASS T failure must be LOUD and must NOT halt. Loud, not fatal.
    results['QV-1a'] = ('FAIL' if extra else 'PASS',
                          f'In PYQ not taxonomy: {list(extra)[:5]}' if extra else 'OK')

    # QV-15 — BODY TERMINATION SANITY (GAP-2026-08-05-001, SG-7)
    # QV-1a only fires when the phantom's TEXT is absent from the taxonomy. If a misread
    # continuation happens to canon-match a real subtopic name, QV-1a is silent, Step 4's
    # totals still reconcile, and the questions after it are attributed to the WRONG
    # subtopic with no signal anywhere. QV-15 tests the STRUCTURE instead of the name, so
    # it catches that branch too.
    # NAT IS TESTED DIFFERENTLY AND DELIBERATELY. An option-count threshold is meaningless
    # for a question that has no options, and NAT is the shape MOST exposed to a heading
    # misread (no options means its last stem paragraph sits in the same slot as a genuine
    # heading). So for NAT the assertion is on COLOUR: in a file whose date-label probe
    # passed, a body terminated by a non-navy inferred heading is a misread by definition.
    _tbh   = [e for e in entries if e.get('terminated_by_heading')]
    # GAP-2026-08-16-BASELINE-SUPPRESSED-NAMEERRORS (D6). `options_count` is a SESSION
    # parameter detected at S1-3; it is bound nowhere at module scope, so run_qv read a
    # free name. The comprehension only EVALUATES it when _tbh is non-empty — i.e. when
    # at least one question was terminated by an inferred heading — so QV-15 raised
    # NameError EXACTLY when it had something to report, and passed silently when it
    # did not. A check that crashes only on the defect it exists to detect is worse
    # than absent: it reads as a clean PASS on every corpus that does not trigger it.
    # IIT_JAM_MATHEMATICS has 0 such questions, which is the only reason the v2.53.0
    # certification run survived this line.
    # progress._meta.options_count is the parameter's persisted home (written at S1-3,
    # present in every schema_version >= 2.0 corpus). Default 4 matches the documented
    # safe default at §1 ("mixed or ambiguous -> options_count = 4").
    # Coerced, not merely defaulted. `<` between int and str raises TypeError, so a
    # hand-edited exam_config or a pre-2.0 corpus carrying "4" would reproduce the exact
    # crash this fix removes. Every non-numeric or absent value falls back to the
    # documented safe default of 4 (§1: "mixed or ambiguous -> options_count = 4").
    try:
        _options_count = int((progress.get('_meta') or {}).get('options_count') or 4)
    except (TypeError, ValueError):
        _options_count = 4
    if _options_count < 1:
        _options_count = 4
    _short = [e for e in _tbh
              if e.get('has_options', True)
              and len(e.get('options') or []) < _options_count]
    _nat_bad = [e for e in _tbh
                if not e.get('has_options', True)
                and e.get('colour_available')
                and e.get('terminating_heading_colour') != bc.HEADING_NAVY]
    _bad = _short + _nat_bad
    results['QV-15'] = ('FAIL' if _bad else 'PASS',
                        f'{len(_bad)} question(s) terminated by an inferred heading '
                        f'before their options were collected: '
                        f'{[e.get("num") for e in _bad][:5]}' if _bad else
                        f'OK ({len(_tbh)} bodies ended on a heading, all well-formed)')
    # Report the raw counter in the batch summary even when it is 0 — an unexplained
    # jump between papers of the same exam is the earliest visible symptom of a Step-1
    # rendering change that newly exposes this class.
    results['_counter_questions_terminated_by_heading'] = len(_tbh)

    # ── QV-16 — POSITION RESOLUTION INTEGRITY ────────────────────────────────
    # GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION. The defect was invisible for its
    # whole life because NO check compared the resolved positions against the paper
    # that produced them. Every QV passed, nothing raised, nothing counted it, and the
    # one artefact a reviewer inspects by eye — the template — had already been
    # scrubbed of date labels by E-10 strip_variables, hiding the leak.
    #
    # THE INVARIANT: a v1.18+ sorted paper stamps EXACTLY ONE original position per
    # question, so within one paper the resolved original_q_num values must be
    # DISTINCT. Under the defect every question in a taxonomy block collapses onto the
    # block's first position, and the collision count is the number of questions that
    # inherited a stale label. This is a property of the OUTPUT, not of the parser, so
    # it cannot share the parser's blind spot — which is the whole point (the same
    # lesson as GAP-2026-08-15-BAREQ: input and output counted with one blind detector).
    #
    # VACUOUS PASS on a pre-v1.18 corpus, where parse_original_q_num returns None for
    # every unstamped label and there is nothing to collide. That is correct, not a
    # gap: such a corpus never had positional data to corrupt.
    #
    # FAIL, NOT HALT — the CLASS T convention. The papers are still extracted and the
    # progress file is still written; the operator is told loudly that every positional
    # consumer downstream (is_msq -> answer_cardinality -> Step 7's answer mechanism)
    # is reading stale values, and can re-run from a clean progress file.
    from collections import Counter as _Counter16   # local: each fence binds its own
    _pos_by_paper = {}
    for _k, _v in progress.items():
        if not isinstance(_k, tuple):
            continue
        for _q in _v:
            if _q.get('original_q_num') is not None:
                _pos_by_paper.setdefault(_q.get('paper_id'), []).append(
                    _q['original_q_num'])
    _dupes = []
    for _pid, _nums in _pos_by_paper.items():
        if len(set(_nums)) != len(_nums):
            _rep = [n for n, c in _Counter16(_nums).items() if c > 1]
            _dupes.append(f'{_pid}: {len(_nums) - len(set(_nums))} collision(s), '
                          f'e.g. {_rep[:3]}')
    results['QV-16'] = (('FAIL', f'position collisions — every question in a taxonomy '
                                 f'block inherited the block\'s first exam position: '
                                 f'{_dupes[:3]}')
                        if _dupes else
                        ('PASS', f'{len(_pos_by_paper)} paper(s): one distinct '
                                 f'original_q_num per question'
                                 if _pos_by_paper else
                                 'vacuous — pre-v1.18 corpus, no stamped positions'))

    # QV-2: Frequency% sums to 100 per subtopic
    bad = [e['subtopic'] for e in entries if e.get('PYQ_STEM_PATTERNS') and
           abs(sum(p['frequency'] for p in e['PYQ_STEM_PATTERNS'])-100) > 1]
    results['QV-2'] = ('FAIL' if bad else 'PASS',
                        f'Sums!=100: {bad[:3]}' if bad else 'All=100%')

    # QV-3: BUG-B09 fix: check is_inferred bool, not string
    gap = [f'{e["subtopic"]}.{lv}' for e in entries if e['observed_count']>=5
           for lv in ['Simple','Medium','Hard']
           if e.get('PYQ_DIFFICULTY_CALIBRATION',{}).get(lv,{}).get('is_inferred',True)]
    results['QV-3'] = ('WARN' if gap else 'PASS',
                        f'Missing diff: {gap[:5]}' if gap else 'OK')

    # QV-4/5: option_format and wrong_option_structure classified
    no_fmt = [e['subtopic'] for e in entries if not e.get('option_format')]
    results['QV-4'] = ('FAIL' if no_fmt else 'PASS',
                        f'Missing: {no_fmt[:3]}' if no_fmt else 'OK')
    no_wo  = [e['subtopic'] for e in entries if not e.get('wrong_option_structure')]
    results['QV-5'] = ('FAIL' if no_wo else 'PASS',
                        f'Missing: {no_wo[:3]}' if no_wo else 'OK')

    # QV-5b: BUG-C07 fix (v2.3) — fixed_set must have non-empty fixed_option_texts
    bad_fixed = [e['subtopic'] for e in entries
                 if e.get('wrong_option_structure', {}).get('type') == 'fixed_set'
                 and not e.get('wrong_option_structure', {}).get('fixed_option_texts')]
    results['QV-5b'] = ('FAIL' if bad_fixed else 'PASS',
                         f'fixed_set missing texts: {bad_fixed[:3]}' if bad_fixed else 'OK')

    # QV-6: confidence accuracy
    bad_c = [f'{e["subtopic"]}.{p["id"]}' for e in entries
             for p in e.get('PYQ_STEM_PATTERNS',[])
             if p.get('confidence')=='observed' and p.get('raw_count',0)<3]
    results['QV-6'] = ('WARN' if bad_c else 'PASS',
                        f'Observed<3: {bad_c[:3]}' if bad_c else 'OK')

    # QV-7: templates have _VAR_ placeholders
    VAR_TOKENS = {'_NUM_','_P_','_R_%','_T_','_WORD_','_CODE_','_NOUN_','_LCLUS_',
                  '_YEAR_','_ORG_','_BLANK_','_NAME_','_SERIES_','_STMT_','_ADJ_'}
    no_var = [f'{e["subtopic"]}.{p["id"]}' for e in entries
              for p in e.get('PYQ_STEM_PATTERNS',[])
              if p['template'] not in ('(no PYQ observed)','(figural -- no text stem)')
              and not any(v in p['template'] for v in VAR_TOKENS)]
    results['QV-7'] = ('WARN' if no_var else 'PASS',
                        f'No _VAR_: {no_var[:3]}' if no_var else 'OK')

    # QV-8: OMML recovery >= 80%
    omml_iss = []
    for e in entries:
        if not e.get('OMML_required'): continue
        qs = progress.get((e['section'],e['topic'],e['subtopic']),[])
        om = [q for q in qs if q.get('omml_present')]
        ok = [q for q in om if not q.get('omml_failed')]
        if om and len(ok)/len(om) < 0.80:
            omml_iss.append(f'{e["subtopic"]}: {len(ok)}/{len(om)}')
    results['QV-8'] = ('WARN' if omml_iss else 'PASS',
                        f'OMML<80%: {omml_iss[:3]}' if omml_iss else 'OK')

    # QV-9: image clarity >= 80%
    img_iss = []
    for e in entries:
        if e.get('format')!='FIGURAL': continue
        ia  = e.get('PYQ_IMAGE_ANALYSIS') or {}
        tot = ia.get('images_analysed',0) + ia.get('images_unclear',0)
        if tot>0 and ia.get('images_unclear',0)/tot>0.20:
            img_iss.append(f'{e["subtopic"]}: {ia["images_unclear"]}/{tot}')
    results['QV-9'] = ('WARN' if img_iss else 'PASS',
                        f'Image<80%: {img_iss[:3]}' if img_iss else 'OK')

    # QV-10: PASSAGE subtopics have linked_group_size > 0
    no_grp = [e['subtopic'] for e in entries
               if e.get('format')=='PASSAGE' and e.get('linked_group_size',0)==0]
    results['QV-10'] = ('WARN' if no_grp else 'PASS',
                          f'Passage no groups: {no_grp}' if no_grp else 'OK')

    # QV-11: BUG-A09 fix -- global_max_year across all entries, not per-entry max
    all_years_global = [y for e in entries
                        for p in e.get('PYQ_STEM_PATTERNS',[])
                        for y in p.get('years',[]) if isinstance(y,int)]
    global_max = max(all_years_global) if all_years_global else None
    old_only = []
    if global_max:
        for e in entries:
            entry_yrs = [y for p in e.get('PYQ_STEM_PATTERNS',[])
                         for y in p.get('years',[]) if isinstance(y,int)]
            if entry_yrs and max(entry_yrs) < global_max - 1:
                old_only.append(e['subtopic'])
    results['QV-11'] = ('WARN' if old_only else 'PASS',
                          f'No recent data: {old_only[:3]}' if old_only else 'OK')

    # QV-12: no near-duplicate templates within a subtopic
    dups = []
    for e in entries:
        pats = [p['template'] for p in e.get('PYQ_STEM_PATTERNS',[])]
        for i in range(len(pats)):
            for j in range(i+1,len(pats)):
                if SequenceMatcher(None,pats[i],pats[j]).ratio()>0.90:
                    dups.append(f'{e["subtopic"]}: P{i+1}~P{j+1}')
    results['QV-12'] = ('WARN' if dups else 'PASS',
                          f'Near-dups: {dups[:3]}' if dups else 'OK')

    # QV-13 (v2.24) — MECHANIC INTEGRITY & COLLISION GUARD. Stops Step 5 from ever
    # QV-13 (v2.24.1) — MECHANIC IDENTITY INTEGRITY. FAIL severity, NO allowlist.
    # Reads the STAMPED fields (D5); never recomputes for the collision test. Step 5
    # cannot know N_mocks/batch_size, so it must reject ALL shared form_keys (D4/D7).
    from collections import defaultdict as _dd
    empty     = [e['subtopic_id'] for e in entries if not e.get('form_key')]
    unstamped = [e['subtopic_id'] for e in entries if 'form_key' not in e or e['form_key'] is None]
    # a REAL determinism check (D5): does a fresh derivation reproduce the stamped value?
    _pov = (progress.get('_meta', {}) or {}).get('section_prefix_overrides', {})
    _po  = build_section_prefix_map(sorted({e['section'] for e in entries}), _pov)
    nondet = []
    for e in entries:
        if not e.get('subtopic_id') or e.get('form_key') is None:
            continue
        _tpl = ' '.join(p.get('template','') for p in e.get('PYQ_STEM_PATTERNS', []))
        _fk  = derive_mechanic(e['section'], e.get('subtopic') or e.get('sub_type_label',''),
                               e.get('sub_type_label'), _tpl, e.get('format','TEXT'),
                               e['subtopic_id'], _po)['form_key']
        # a curator override legitimately makes the stamped value differ from a bare
        # derivation; only flag when NO override explains it.
        _ov  = (_OVERRIDES or {}).get('subtopic_overrides', {}).get(e['subtopic_id'], {})
        if _fk != e['form_key'] and 'form_key' not in _ov and e['form_key'] != slugify(e['subtopic_id']):
            nondet.append(e['subtopic_id'])
    dom = _dd(lambda: _dd(list))
    for e in entries:
        dom[e.get('collision_domain')][e.get('form_key')].append(e['subtopic_id'])
    collisions = [f'{d}:{fk}={sorted(ids)}'
                  for d, fks in dom.items() for fk, ids in fks.items() if len(ids) > 1]
    # a bare family token is illegal unless this exam declared the owning template set
    def _decl(e):
        _ov = _OVERRIDES or {}
        a = _ov.get('template_sets_by_section', {}).get(e['section'], _ov.get('template_sets'))
        return ['verbal','reasoning'] if a is None else a
    # A family-named form_key is illegal ONLY when it is a FOREIGN token, i.e. it did NOT
    # come from the subtopic's own identity base. Under v2.24.1 form_key == base for a
    # subtopic legitimately named like a family (e.g. a real verbal "Analogy"); that is not
    # contamination and must NOT FAIL. A foreign token can only arrive via a curator override.
    illegal = [e['subtopic_id'] for e in entries
               if e.get('form_key') in _ALL_FAMILY_NAMES
               and _TEMPLATE_SET.get(e.get('form_key')) not in _decl(e)
               and e['form_key'] != _identity_base(e.get('subtopic') or e.get('sub_type_label',''),
                                                    e.get('subtopic_id'))]
    same_as_domain = [e['subtopic_id'] for e in entries
                      if e.get('form_key') and e['form_key'] == e.get('collision_domain')]
    import re as _re
    bad_shape = [e['subtopic'] for e in entries
                 if len(e['subtopic']) > 60 or e['subtopic'].strip().endswith('?')
                 or _re.match(r'^\s*(what|which|how|why|find|choose|select|the average)\b',
                              e['subtopic'].strip(), _re.I)]
    if empty or unstamped or nondet or collisions or illegal or same_as_domain:
        results['QV-13'] = ('FAIL',
            f'empty={empty[:3]} unstamped={unstamped[:3]} nondeterministic={nondet[:3]} '
            f'collisions={collisions[:3]} illegal_family_token={illegal[:3]} '
            f'equals_domain={same_as_domain[:3]}')
    else:
        results['QV-13'] = ('PASS', f'{len(entries)} form_keys: non-empty, deterministic, '
                                    f'unique per collision_domain, no foreign family tokens')
    # QV-13a — NAME SHAPE. Advisory only; split so an editorial nit can neither mask nor
    # be masked by an identity failure.
    results['QV-13a'] = (('WARN', f'{len(bad_shape)} long/question-shaped names: {bad_shape[:3]}')
                         if bad_shape else ('PASS', 'OK'))

    # ── QV-14 — VISION COVERAGE (v2.37, GAP-2026-07-26-003) ─────────────────
    # FAIL, not WARN. The reference run scored QV-9 PASS with 153/153 figural
    # questions unobserved and 45/45 FIGURAL subtopics shipping an empty profile,
    # because QV-9 computes images_analysed + images_unclear and BOTH are zero when
    # nothing was observed — so its `if tot > 0` branch never fires. A WARN would not
    # have stopped that run either. This is the check that makes the failure impossible
    # to ship silently.
    #
    # QV-14 DOES NOT HALT. It reports. Framework_DeliveryFooter renders F1 amber on any
    # FAIL, and the operator re-runs PHASE B ONLY.
    #
    # DENOMINATOR. Only questions that actually carry a figure. EC-V13 (zero-PYQ
    # inferred FIGURAL subtopic) and EC-V14 (INHERENTLY-VISUAL keyword override) are
    # legitimately FIGURAL with no embedded figure; they contribute no queue item by
    # construction and are excluded here for the same reason. EC-V1: an exam with no
    # figural content at all has an empty denominator and PASSes vacuously — a
    # text-only exam must never fail this check.
    fig_qs = [q for k, v in progress.items() if isinstance(k, tuple) for q in v
              if q.get('image_role', 'none') != 'none']
    if not fig_qs:
        results['QV-14'] = ('PASS', 'no figural questions in this corpus — '
                                    'vision not applicable (EC-V1)')
    else:
        unobs = sum(1 for q in fig_qs if q.get('image_clarity') == 'vision_unavailable')
        noty = sum(1 for q in fig_qs if not q.get('object_type')
                   and q.get('image_clarity') == 'clear')
        seen = len(fig_qs) - unobs
        if unobs == len(fig_qs):
            results['QV-14'] = ('FAIL',
                f'0/{len(fig_qs)} figures observed — PHASE B did not run. '
                f'PYQ_IMAGE_ANALYSIS is empty for every FIGURAL subtopic and Step 7 '
                f'has no object-type, transformation, arrangement or complexity '
                f'guidance. The run is COMPLETE and resumable: re-run PHASE B ONLY '
                f'(S4-2b) against the queue already on disk, then re-run synthesis.')
        elif unobs / len(fig_qs) > 0.50:
            results['QV-14'] = ('FAIL',
                f'only {seen}/{len(fig_qs)} figures observed ({unobs} unobserved) — '
                f'more than half the figural corpus is missing. Re-run PHASE B; it is '
                f'idempotent and fills only the gaps.')
        elif unobs:
            results['QV-14'] = ('WARN',
                f'{seen}/{len(fig_qs)} figures observed, {unobs} unobserved — '
                f're-running PHASE B is idempotent and fills only the gaps.')
        elif noty:
            results['QV-14'] = ('WARN',
                f'{seen}/{len(fig_qs)} observed but {noty} carry no object_type — '
                f'check the Phase B protocol was followed for every labelled cell.')
        else:
            results['QV-14'] = ('PASS', f'{seen}/{len(fig_qs)} figures observed')

    return results

def print_qv(results):
    """Render run_qv()'s result mapping.

    GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D1). run_qv returns ONE dict
    carrying TWO kinds of entry, and this function used to unpack every value as
    a (status, detail) pair:

        for check,(status,detail) in results.items():

    v2.41.0 added `results['_counter_questions_terminated_by_heading'] = len(_tbh)`
    — an int, written unconditionally, "reported even when 0". From that release
    this loop raised `TypeError: cannot unpack non-iterable int object` on EVERY
    exam, and because run_synthesise calls print_qv BEFORE write_section_rules,
    Step 5 emitted NOTHING for eleven days and eleven minor versions.

    The counter was written once and read nowhere. The producer changed the dict's
    contract and the consumer was never told — the same producer/consumer blind
    spot as GAP-2026-08-15-BAREQ and GAP-2026-08-16-PYQEXTRACT-DATE-LABEL-POSITION.

    THE CONTRACT IS NOW EXPLICIT AND ENFORCED, not merely tolerated:
      * `QV-*` keys are CHECKS   -> value MUST be a (status, detail) 2-tuple.
      * `_`-prefixed keys are COUNTERS -> scalar, reported on their own line, and
        never mistaken for a check. This preserves v2.41.0's stated intent, which
        was to make the counter VISIBLE, not to make it a check.
      * Anything else raises immediately, naming the offending key, so a future
        malformed check fails loudly at its source instead of presenting as an
        unpackable int three frames from whatever produced it.
    """
    print('\n=== Quality Verification Results ===')
    icons = {'PASS':'v','WARN':'!','FAIL':'X'}
    all_ok = True
    counters = {}
    for check, value in results.items():
        if check.startswith('_'):
            counters[check] = value
            continue
        if not (isinstance(value, tuple) and len(value) == 2):
            raise TypeError(
                f"print_qv: check {check!r} must map to a (status, detail) "
                f"2-tuple, got {type(value).__name__} {value!r}. A counter or "
                f"other bookkeeping value must use a '_'-prefixed key so it is "
                f"reported rather than unpacked (D1).")
        status, detail = value
        if status not in icons:
            raise ValueError(
                f"print_qv: check {check!r} has status {status!r}; expected one "
                f"of {sorted(icons)}.")
        print(f'  {icons[status]} {check}: {status} -- {detail}')
        if status=='FAIL': all_ok = False
    for name, value in counters.items():
        print(f'  . {name.lstrip("_")}: {value}')
    print(f'\n{"All checks passed." if all_ok else "FAIL checks must be resolved."}')
    return all_ok

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

    # ══ §3 / §5 / §6 (Batch 3) ═══════════════════════════════════════════
    # ── SESSION_RE INJECTION — the one session global in the extraction scope ──
    # Omitting it must RAISE, not fall back. A default would silently mislabel every
    # paper's shift with a guessed keyword: a wrong answer, not an error, which is the
    # failure shape this corpus pays most for (v2.16 RIGID-1).
    try:
        extract_shift_from_filename('IIT_JAM_2026_Shift-2.docx')
        check('session_re_omission_raises', False)
    except RuntimeError as exc:
        check('session_re_omission_raises', 'session_re' in str(exc))
        check('session_re_error_says_what_to_pass', 'SESSION_RE' in str(exc))
    _sre = re.compile(re.escape('Shift') + r'[-_\s]?(\d+)', re.IGNORECASE)
    check('shift_parsed_with_injected_regex',
          extract_shift_from_filename('IIT_JAM_2026_Shift-2.docx', session_re=_sre) == 'S2')
    check('shift_defaults_to_S1_when_absent',
          extract_shift_from_filename('IIT_JAM_2026.docx', session_re=_sre) == 'S1')
    # A DIFFERENT keyword must give a different answer — proves the regex is really
    # the injected one and not a hidden module-level default.
    _slot = re.compile(re.escape('Slot') + r'[-_\s]?(\d+)', re.IGNORECASE)
    check('injected_regex_is_actually_used',
          extract_shift_from_filename('EXAM_Slot_3.docx', session_re=_slot) == 'S3'
          and extract_shift_from_filename('EXAM_Slot_3.docx', session_re=_sre) == 'S1')

    # ── §5 synthesis: the id/axis contract every later step joins on ──────────
    check('section_prefix_is_deterministic',
          section_prefix('Real Analysis') == section_prefix('Real Analysis'))
    _sid = make_subtopic_id('Real Analysis', 'Sequences', 'Convergence')
    check('make_subtopic_id_is_deterministic',
          _sid == make_subtopic_id('Real Analysis', 'Sequences', 'Convergence'))
    check('make_subtopic_id_is_nonempty_str', isinstance(_sid, str) and _sid)
    check('distinct_subtopics_get_distinct_ids',
          _sid != make_subtopic_id('Real Analysis', 'Sequences', 'Divergence'))

    # ── §6 QV: the contract D1 broke — checks are 2-tuples, counters are not ──
    # print_qv must render a counter WITHOUT unpacking it. v2.41.0 added an int under
    # a '_'-prefixed key and every Step 5 run raised TypeError here for eleven days
    # (GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE D1).
    import io as _io, contextlib as _cl
    _buf = _io.StringIO()
    with _cl.redirect_stdout(_buf):
        _ok = print_qv({'QV-1': ('PASS', 'all covered'), '_counter_demo': 0})
    check('print_qv_tolerates_a_counter_key', _ok is True)
    check('print_qv_renders_the_counter', 'counter_demo' in _buf.getvalue())
    with _cl.redirect_stdout(_io.StringIO()):
        check('print_qv_reports_FAIL',
              print_qv({'QV-1': ('FAIL', 'broken')}) is False)
    # A malformed CHECK must raise at its source, naming the key.
    try:
        with _cl.redirect_stdout(_io.StringIO()):
            print_qv({'QV-2': 7})
        check('print_qv_rejects_a_malformed_check', False)
    except TypeError as exc:
        check('print_qv_rejects_a_malformed_check', 'QV-2' in str(exc))

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
