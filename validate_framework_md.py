#!/usr/bin/env python3
"""
validate_framework_md.py v3.1 — Universal Framework .md Validator
Replaces both the old Step-8-specific validator AND the universal validator.
Runs universal checks on ANY framework .md file, PLUS auto-detects and runs
extended checks when the file contains patterns that warrant them:
  • Gate-code emission checks (files with an embedded audit script using A-* codes)
  • RA-rule anchor checks (files defining RA-N rules)
  • MANDATE anchor checks (files defining MANDATE blocks)
  • Dynamic embedded script execution (files with a self_test() function)
  • Constant consistency (AUDIT_BATCH_SIZE, RUN_MAX — when present)
  • Completion-gate wiring + regression fixtures (v2.6 — files defining completion_gate)

Checks (each reports PASS/issues):
  ═══ UNIVERSAL (always run) ═══
  A. FENCED CODE BLOCKS — pairing + indentation consistency
  B. PYTHON AST — every ```python block is syntax-clean (placeholder-tolerant)
  C. VERSION CONSISTENCY — header version == footer version == changelog top entry
     (accepts both the dated 'vX.Y — DATE — ...' format AND the undated 'vX.Y changes:
     ...' format used by several files' latest entries — v2.8)
  D. GATE COUNT DRIFT — all live gate-count totals agree (no hardcoded number)
  E. STEP NUMBER VALIDATION — Step N (Name) patterns vs the canonical pipeline
  F. VARIABLE REFERENCES — known dangerous patterns in code blocks
  G. CHECKLIST COUNT — "All N items" matches actual [ ] count in that section
  H. CROSS-REFERENCES — §N references resolve to defined section headers
  I. STALE MARKERS — TODO / FIXME / PLACEHOLDER / TBD (word-boundary matched — v2.8, so a
     legitimate identifier like `_PLACEHOLDER` or `PLACEHOLDER_URL` is not false-flagged;
     a genuine standalone marker still is)
  J. SELF-TEST COUNT — prose "N/N PASS" matches actual unique check() names
  K. DUPLICATE SECTIONS — no §N or sub-section defined twice

  ═══ AUTO-DETECTED EXTENDED (run when patterns found) ═══
  M. GATE-CODE EMISSION — embedded script emitted codes vs documented A-* codes
  N. RA-RULE ANCHORS — every RA-N reference resolves to a definition (checked locally;
     ALSO checked against every other file in the batch when 2+ files are passed — v2.8,
     since RA-N is a framework-wide numbering space, not per-file: e.g. RA-12 is
     referenced in Framework_MockTestCreate.md but defined in
     Framework_MockTestCreateAudit.md)
  O. MANDATE ANCHORS — every MANDATE X reference resolves to a definition (same v2.8
     local-then-batch fallback as N; MANDATE 0/1/2 are GLOBAL — defined once in
     Framework_MockTestCreate.md, referenced from other Step specs — while MANDATE A/B/D
     are intentionally redefined LOCALLY per Step spec; cross-file fallback is harmless
     for the latter since this check only verifies an anchor exists somewhere, never
     compares content)
  P. CONSTANT CONSISTENCY — AUDIT_BATCH_SIZE, RUN_MAX values agree
  Q. DYNAMIC EXECUTION — extract + run the largest embedded script --self-test
  R. RA/SUB-SECTION DUPLICATES — RA-N and S/P sub-anchors not defined twice
  S. COMPLETION-GATE (v2.6) — S5-1A wiring + C1-C7 regression fixtures present

  ═══ BATCH-LEVEL (only runs / only fully effective when 2+ files are passed) ═══
  T. CROSS-FILE TOKEN CONTRACT (v2.7 — added after A-INTEGRITY-FALSEPOS-01) — for every
     consumer spec's literal re.search()/re.match() applied against a KNOWN producer
     artifact's content (currently: section_rules.md, produced by
     Framework_MockTestAnalyse.md's write_section_rules()), verify the literal pattern
     can actually match one of the producer's real emitted tokens. Catches a consumer
     hard-coding a producer's internal DOC-ALIAS name (e.g. "CATEGORY C") instead of the
     literal on-disk text the producer actually writes (e.g. '=== EXAM_STRUCTURE ===') —
     the exact defect class that caused P0.5 to HARD STOP on every valid exam
     (Framework_MockTestCreateAudit.md v2.6-v2.7.4). Only runs in batch mode (2+ files),
     since it is inherently a cross-file check; silently skipped for single-file runs.
  U. JSON PRODUCER/CONSUMER FIELD CONTRACT (v2.8) — the same defect class as Check T,
     applied to blueprint.json/registry.json instead of literal text markers. Flags a
     bare-indexed d['field'] READ (not a `.get('field', default)` read, which is already
     safe against a missing key by Python's own fallback) where 'field' cannot be found
     in that artifact's own "§N — ... SCHEMA" reference section(s). Schema sources:
     Framework_Blueprint.md §14 (blueprint.json) and §12 (registry.json base fields) +
     Framework_MockTestCreate.md §14 (registry.json Step-7 additions). Only runs when at
     least one relevant schema source file is present in the batch.

  ═══ CORPUS TRANSPORT / DELEGATION (v3.0 — added after the 2026-07-24 incident) ═══
  V.  UNGUARDED DRIVE FETCH — a Drive download called outside try/ and not routed
      through corpus_io.fetch_drive_docx. Verified at the time: ZERO try/except existed
      around any Drive call in the entire corpus, so one oversized paper ended a
      200-paper run. Per-file, AST-based; silent on files that never fetch.
  W.  ENUMERATION CAPTURES fileSize — a Drive paper record built with 'source':'gdrive'
      must also carry 'fileSize'. The listing already contains it; discarding it makes
      the AUTO/UPLOAD partition impossible, so an unfetchable paper is discovered only
      mid-run.
  X.  PER-ITEM DURABILITY — a loop that does per-item work (process_*_paper /
      count_*_file / scan_*_paper) inside a block that saves progress must save INSIDE
      the loop. When the save sits after the loop, an exception discards every item
      already processed in that batch.
  Y.  IMAGE ACCOUNTING — a spec that extracts or maps images must also reference an
      image count assertion. A mapped-but-missing image produces a wrong classification,
      never an error.
  Z.  DELEGATION CONTRACT — no spec may define a function owned by the shared
      transport/image engine (corpus_io, blueprint_core Cluster H). Thin forwarding
      adapters are permitted. Names are read from the engine sources, so the check
      cannot go stale; generic harness names (check/self_test/main) are excluded.

  ═══ CORPUS-LEVEL (run when the engines / routes sit beside the specs) ═══
  AA. ROUTES <-> SKILL SYNC — both directions, plus the skill's spec/engine counts.
      A routed trigger the skill never names is unreachable; a skill trigger with no
      route runs the step with no spec loaded.
  AB. THIN-CORE PURITY — blueprint_core.py and paper_pipeline.py may import only the
      standard library and must perform no file I/O. This invariant was documented as
      "enforced by validate_framework_md.py" while no such check existed; a PIL import
      landing in the core is the v2.26 P0 that aborted Step 5 for every exam.

Usage:
  python3 validate_framework_md.py <file.md>
  python3 validate_framework_md.py /mnt/project/*.md   (batch mode — enables Check T)
"""
import re, ast, sys, os, glob
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════
# CANONICAL PIPELINE — the single source of truth for step numbers
# ═══════════════════════════════════════════════════════════════════════
PIPELINE = {
    'PYQPrepare': '1', 'PYQDraft': '2a', 'PYQScan': '2b', 'PYQApprove': '2c',
    'PYQSort': '3', 'PYQCount': '4', 'PYQExtract': '5',
    'PYQExplain': 'PYQ-1', 'PYQExplainAudit': 'PYQ-2', 'PYQFormat': 'PYQ-3', 'PYQDeliver': 'PYQ-4',
    'PYQCompress': 'L2',
    'MockTestAnalyse': '5', 'MockBlueprint': '6', 'Blueprint': '6', 'ScopedBlueprint': '6S',
    'MockCreate': '7', 'MockCreateAudit': '8', 'TestCreate': '7', 'TestCreateAudit': '8',
    'MockExplain': '9', 'MockExplainAudit': '10', 'MockDeliver': '11',
    'TestExplain': '9', 'TestExplainAudit': '10', 'TestDeliver': '11',
}

def validate(path, all_texts=None):
    """all_texts: optional {basename: text} for every file in the current batch run,
    including this one. When provided (batch mode, 2+ files), RA-N and MANDATE X
    references that don't resolve locally are ALSO checked against every other file in
    the batch before being flagged — a reference is only reported unresolved if it fails
    to resolve ANYWHERE in the batch. In single-file mode (all_texts is None), behavior
    is unchanged from before: local-file resolution only."""
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    fname = os.path.basename(path)
    issues = []
    info = []
    def add(cat, msg): issues.append((cat, msg))

    # ── v2.9: SPEC vs DOCUMENTATION-RECORD classification ─────────────────────
    # This validator's structural checks were written for SPEC files (Framework_*.md):
    # fenced code, numbered §-sections, an END OF sentinel. The corpus also carries prose
    # RECORD files (architecture notes, audit/verification records) that live in the same
    # directory and are passed to the same batch run. Applying spec-structural checks to
    # prose produces false positives that are impossible to fix without corrupting the
    # record itself, namely:
    #   H-XREF   — a record legitimately cites ANOTHER file's section ("Framework_Blueprint
    #              §7.1"). The check resolves §N only against the LOCAL file's headers, so
    #              every cross-file citation is reported as an undefined section.
    #   I-STALE  — a record that DOCUMENTS stale-marker handling must write the words. The
    #              architecture note's own "Resolved" list contains the sentence
    #              "PLACEHOLDER identifier false positives (#3/#4)", which is a statement
    #              that they WERE fixed, flagged as if it were an unfinished stub.
    # Both were reported for months as "known pre-existing issues" and neither was a defect.
    # A record is identified STRUCTURALLY, not by filename, so the rule generalises: a file
    # with no fenced code blocks AND no numbered §-section headers is not a spec. The
    # filename prefix is accepted as a secondary signal for this corpus's claude_* records.
    _has_code = '```' in text
    _has_sections = bool(re.search(r'^#+ §\d+\b', text, re.M))
    is_record = (not _has_code and not _has_sections) or (
        fname.startswith('claude_') and not _has_code)
    if is_record:
        info.append('classified as a DOCUMENTATION RECORD (no code blocks, no §-sections) — '
                    'spec-structural checks H-XREF and I-STALE are not applicable and are '
                    'skipped; every other check still runs.')

    # ─────────────────── A: FENCED CODE BLOCKS ───────────────────
    fences = []
    for i, l in enumerate(lines, 1):
        st = l.lstrip()
        if st.startswith('```'):
            indent = len(l) - len(st)
            lang = st[3:].strip() or None
            fences.append((i, indent, lang))
    stack, pairs = [], []
    for (ln, ind, lang) in fences:
        if stack and lang is None:
            pairs.append((stack.pop(), (ln, ind, lang)))
        elif lang is not None:
            stack.append((ln, ind, lang))
        else:
            if stack: pairs.append((stack.pop(), (ln, ind, lang)))
            else: stack.append((ln, ind, lang))
    for s in stack:
        add('A-FENCE', f'unclosed code fence at line {s[0]} (lang={s[2]})')
    for (op, cl) in pairs:
        if op[1] != cl[1]:
            add('A-FENCE', f'fence indent mismatch: L{op[0]} indent={op[1]} vs L{cl[0]} indent={cl[1]}')

    # ─────────────────── B: PYTHON AST ───────────────────────────
    def block_lines(op, cl):
        return lines[op[0]:cl[0]-1]
    py_blocks = [(op, cl) for (op, cl) in pairs if op[2] == 'python']
    ast_ok = 0
    for (op, cl) in py_blocks:
        raw = block_lines(op, cl)
        ind = op[1]
        body = '\n'.join(l[ind:] if l[:ind].strip() == '' else l for l in raw)
        probe = re.sub(r'\[ExamCode\]', 'EXAMCODE', body)
        probe = re.sub(r'\[N\]', 'NNN', probe)
        probe = re.sub(r'\[ExamName\]', 'EXAMNAME', probe)
        probe = re.sub(r'<<[^>]+>>', 'PLACEHOLDER_URL', probe)
        try:
            ast.parse(probe); ast_ok += 1
        except SyntaxError as e:
            add('B-PYAST', f'python block L{op[0]}-{cl[0]}: {e.msg} (line {e.lineno} of block)')

    # ─────────────────── C: VERSION CONSISTENCY ──────────────────
    # v3.1: versions are matched in FULL, not truncated to two components. The old
    # r'(\d+\.\d+)' captured '1.16' from 'v1.16.1' on one side and the whole string on
    # the other, so a patch-level bump could report a mismatch that did not exist —
    # and, worse, could hide one.
    _VER = r'(\d+(?:\.\d+)+)'
    header_ver = None
    m = re.match(r'^#?\s*\S+\s+v' + _VER, lines[0])
    if not m:  # try "Version: vX.Y" format
        for l in lines[:15]:
            m2 = re.match(r'^Version:\s*v?' + _VER, l)
            if m2: header_ver = m2.group(1); break
    else:
        header_ver = m.group(1)

    # v3.1: BOTH end-sentinel forms are recognised. Two are in live use across the
    # corpus — '# END OF <name> vN' and '**End of <name>.md (vN)**' — and Check C
    # previously knew only the first. A file using the second had NO footer detected,
    # so the header/footer comparison was silently skipped rather than failing: it
    # printed a header version, no footer version, and reported clean. Four files were
    # in that state, one of them eight minor versions stale (Framework_MockTestExplain-
    # Audit.md, header v1.16, sentinel v1.8) and invisible to audit_specs_ext too,
    # whose check_z_version reads the header from line 1 only and that file's line 1
    # carries no version. A check that skips silently is worse than no check, because
    # the clean result is read as evidence.
    footer_ver = None
    for l in reversed(lines):
        m = re.search(r'END OF \S+ v' + _VER, l, re.I)
        if m: footer_ver = m.group(1); break
        m = re.search(r'\*\*End of \S+ \(v' + _VER + r'\)\*\*', l, re.I)
        if m: footer_ver = m.group(1); break
        m = re.search(r'^#\s*Version:\s*' + _VER, l)
        if m and footer_ver is None: footer_ver = m.group(1)
    if header_ver and footer_ver and header_ver != footer_ver:
        add('C-VERSION', f'header version v{header_ver} != footer version v{footer_ver}')

    changelog_ver = None
    # v2.8: accept EITHER the dated 'vX.Y — DATE — ...' format (original, used by the
    # majority of entries project-wide) OR the undated 'vX.Y changes: ...' format (used by
    # several files' most-recent entries, e.g. Framework_PYQAnalyse.md v2.12-v2.14 and
    # Framework_MockTestAnalyse.md's v2.24 entry — confirmed a real, repeated project
    # convention rather than a typo, by checking multiple files). Previously only the dated
    # form was recognised, so an undated latest-entry silently failed to register as the
    # "current" version and a lower, older dated entry won the max() comparison instead —
    # producing a false "header vX.Y != highest changelog entry vY.Z" report even when the
    # header correctly matched the file's actual latest (undated) entry.
    for l in lines:
        # v3.1: full version, so a patch-level entry (v1.5.1) is not truncated to v1.5
        # and then reported as disagreeing with its own header.
        m = re.match(r'^[#*\s]*v(\d+(?:\.\d+)+)\s*(?:[—–-]\s*\d{4}|changes:)', l.strip())
        if m:
            v = m.group(1)
            if changelog_ver is None or tuple(map(int, v.split('.'))) > tuple(map(int, changelog_ver.split('.'))):
                changelog_ver = v
    if header_ver and changelog_ver and header_ver != changelog_ver:
        add('C-VERSION', f'header v{header_ver} != highest changelog entry v{changelog_ver}')

    # ─────────────────── D: GATE COUNT DRIFT ─────────────────────
    live_pats = [r'all (\d+) gates', r'Total guard gates:\s*(\d+)',
                 r'\((\d+) gates\s*(?:total)?\)', r'(\d+) gates total']
    live_counts = {}
    for i, l in enumerate(lines, 1):
        if any(x in l for x in ['→', '->', 'gate count', 'new gates', 'adds']):
            continue
        for p in live_pats:
            for m in re.finditer(p, l):
                live_counts.setdefault(int(m.group(1)), []).append(i)
    if len(live_counts) > 1:
        vals = '; '.join(f'{v} (L{",".join(map(str,ls))})' for v, ls in sorted(live_counts.items()))
        add('D-GATECOUNT', f'live gate-count totals disagree: {vals}')

    # ─────────────────── E: STEP NUMBER VALIDATION ───────────────
    for m in re.finditer(r'Step\s+(\d+[a-c]?)\s+\((\w+)\)', text):
        step_num, step_name = m.group(1), m.group(2)
        expected = PIPELINE.get(step_name)
        if expected and expected != step_num:
            line_idx = text[:m.start()].count('\n') + 1
            lt = lines[line_idx - 1].strip() if line_idx <= len(lines) else ''
            if lt.startswith('#') or lt.startswith('*'):
                continue
            add('E-STEPNUM', f'L{line_idx}: Step {step_num} ({step_name}) should be Step {expected}')

    # ─────────────────── F: VARIABLE REFERENCES ──────────────────
    for (op, cl) in py_blocks:
        raw = block_lines(op, cl)
        for i, l in enumerate(raw, op[0]):
            stripped = l.strip()
            if "'bp' in dir()" in stripped and not stripped.startswith('#'):
                add('F-VARREF', f'L{i+1}: fragile "\'bp\' in dir()" guard in live code')

    # ─────────────────── G: CHECKLIST COUNT ──────────────────────
    for m in re.finditer(r'All (\d+) items must PASS', text):
        claimed = int(m.group(1))
        pos = m.start()
        section_start = text.rfind('\n## ', 0, pos)
        if section_start < 0: section_start = 0
        actual = text[section_start:pos].count('[ ]')
        if actual != claimed:
            line_num = text[:pos].count('\n') + 1
            add('G-CHECKLIST', f'L{line_num}: claims "All {claimed} items" but section has {actual} [ ] items')

    for m in re.finditer(r'(\d+)-point self-verification', text):
        claimed = int(m.group(1))
        pos = m.start()
        block_start = text.find('```', pos)
        block_end = text.find('```', block_start + 3) if block_start >= 0 else -1
        if block_start >= 0 and block_end >= 0:
            actual = len(re.findall(r"checks\.append\(", text[block_start:block_end]))
            if actual > 0 and actual != claimed:
                line_num = text[:pos].count('\n') + 1
                add('G-CHECKLIST', f'L{line_num}: "{claimed}-point" but {actual} checks.append() calls')

    # ─────────────────── H: CROSS-REFERENCES ─────────────────────
    # def_sections is ALSO consumed by the summary report below, so it must be computed
    # unconditionally — only the FLAGGING is gated (v2.9).
    def_sections = set(re.findall(r'^#+ §(\d+)\b', text, re.M))
    ref_sections = set(re.findall(r'§(\d+)\b', text))
    if not is_record:                      # v2.9: records cite OTHER files' sections
        for s in sorted(int(x) for x in (ref_sections - def_sections) if x.isdigit()):
            add('H-XREF', f'reference to §{s} but no section §{s} header defined')

    # ─────────────────── I: STALE MARKERS ────────────────────────
    # v2.8: word-boundary matching (not bare substring) — a bare substring search
    # false-flags legitimate identifiers that happen to CONTAIN a stale-marker word, e.g.
    # a real Python constant `_PLACEHOLDER = {...}` (used as a genuine sentinel-value set,
    # not an unfinished stub) and its call sites. \b requires a non-word character (or
    # string boundary) on each side, so "_PLACEHOLDER" does NOT match (no boundary between
    # '_' and 'P' — '_' is a word character) while a genuine standalone "PLACEHOLDER",
    # "TODO", "FIXME", or "TBD" — always separated from surrounding text by whitespace,
    # punctuation, or quotes in real usage — is still caught exactly as before.
    if not is_record:                      # v2.9: records DOCUMENT these markers by name
        for kw in ('TODO', 'FIXME', 'PLACEHOLDER', 'TBD'):
            kw_pat = re.compile(r'\b' + re.escape(kw) + r'\b')
            for i, l in enumerate(lines, 1):
                if kw_pat.search(l) and not l.strip().startswith('#') and not l.strip().startswith('*'):
                    add('I-STALE', f'L{i}: stale marker "{kw}" found')

    # ─────────────────── J: SELF-TEST COUNT ──────────────────────
    prose_counts = set(re.findall(r'SELF-TEST:\s*(\d+)/\1\s*PASS', text))
    if py_blocks:
        big = max(py_blocks, key=lambda pc: pc[1][0] - pc[0][0])
        big_text = '\n'.join(block_lines(big[0], big[1]))
        st_start = big_text.find('def self_test(')
        st_end = big_text.find('def self_test_audit(', st_start + 1) if st_start >= 0 else -1
        if st_start >= 0:
            core = big_text[st_start:st_end] if st_end > st_start else big_text[st_start:]
            check_names = set(re.findall(r"check\('([^']+)'", core))
            if prose_counts and check_names:
                claimed = max(int(x) for x in prose_counts)
                if claimed != len(check_names):
                    add('J-SELFTEST', f'prose claims SELF-TEST {claimed}/{claimed} '
                        f'but self_test() has {len(check_names)} unique test names')

    # ─────────────────── K: DUPLICATE SECTIONS ───────────────────
    sec_defs = re.findall(r'^(#+\s+§\d+\b[^\n]*)', text, re.M)
    for k, v in Counter(sec_defs).items():
        if v > 1: add('K-DUP', f'section header "{k[:60]}" defined {v} times')
    sub_defs = re.findall(r'^(#{2,}\s+S\d+-\d+\b)', text, re.M)
    for k, v in Counter(sub_defs).items():
        if v > 1: add('K-DUP', f'sub-section "{k}" defined {v} times')

    # ═══════════════════════════════════════════════════════════════
    # AUTO-DETECTED EXTENDED CHECKS
    # ═══════════════════════════════════════════════════════════════

    has_gate_codes = bool(re.search(r'\bA-[A-Z][A-Z0-9]+\b', text))
    has_ra_rules   = bool(re.search(r'\bRA-\d+\b', text))
    has_mandates   = bool(re.search(r'^#\s*MANDATE\s+\w', text, re.M))
    has_embedded   = any('def self_test(' in '\n'.join(block_lines(op, cl))
                         for (op, cl) in py_blocks)
    has_batch_size = 'AUDIT_BATCH_SIZE' in text
    extended_ran = []

    # ─────────────────── M: GATE-CODE EMISSION ───────────────────
    if has_gate_codes and py_blocks:
        extended_ran.append('M-GATE')
        _big = max(py_blocks, key=lambda pc: pc[1][0] - pc[0][0])
        _raw = lines[_big[0][0]:_big[1][0]-1]; _ind = _big[0][1]
        _body = '\n'.join(l[_ind:] if l[:_ind].strip() == '' else l for l in _raw)
        emitted = set(re.findall(r"\(\s*'([A-Z]-[A-Z0-9\-]+)'\s*,", _body))
        documented = set(re.findall(r'\bA-[A-Z][A-Z0-9]+(?:-[A-Z]+)*\b', text))
        # Claude-side gates the script legitimately does NOT emit
        claude_side = set()
        # Try to detect from the spec text itself
        for cs_pat in [r'claude.side.*?\{([^}]+)\}', r'claude_side\s*=\s*\{([^}]+)\}']:
            cs_m = re.search(cs_pat, text, re.I | re.S)
            if cs_m:
                claude_side |= set(re.findall(r"'(A-[A-Z0-9-]+)'", cs_m.group(1)))
        # Also detect from prose: "claude_side" or "Claude-side" near a gate code
        for cs_m in re.finditer(r'[Cc]laude.side[^.]*?(A-[A-Z0-9-]+)', text):
            claude_side.add(cs_m.group(1))
        # Hardcoded well-known Claude-side gates as fallback
        # A-INTEGRITY is a P0.5 PRE-FLIGHT check (Claude-executed in the spec, not emitted
        # by the audit.py gate body) — like A-KINT/A-KBAL/A-KPAT it is catalogue-listed but
        # never printed by _fail(), so exclude it from the "never emitted" complaint.
        claude_side |= {'A-KINT', 'A-KBAL', 'A-KPAT', 'A-MSQ-KEY', 'A-NAT-ANSWER', 'A-INTEGRITY'}
        if emitted:
            for c in sorted(emitted - documented):
                add('M-GATE', f'script emits gate {c} but it is NOT documented in the spec')
            catalogue = set(re.findall(r'\|\s*(A-[A-Z]+(?:-[A-Z]+)*)\s*\|', text))
            for c in sorted((catalogue - emitted) - claude_side):
                add('M-GATE', f'catalogue lists {c} but the script never emits it')
            info.append(f'gate codes: {len(emitted)} emitted, {len(documented)} documented A-* tokens')

    # ─────────────────── N: RA-RULE ANCHORS ──────────────────────
    if has_ra_rules:
        extended_ran.append('N-RA')
        # v2.6: a SPLIT rule (RA-15a / RA-15b) DEFINES the base number RA-15 for
        # reference resolution; the duplicate check keys on the FULL label so 15a and
        # 15b are distinct and do not read as "RA-15 defined twice".
        def_ra = set(re.findall(r'^\s{0,4}RA-(\d+)[a-z]?\s', text, re.M))
        ref_ra = set(re.findall(r'\bRA-(\d+)\b', text))
        unresolved_ra = ref_ra - def_ra
        # CROSS-FILE FALLBACK (v2.8): a reference unresolved LOCALLY may still be defined
        # in a sibling spec file — RA-N rules are a framework-wide numbering space, not
        # per-file (e.g. RA-12 is referenced in Framework_MockTestCreate.md but DEFINED in
        # Framework_MockTestCreateAudit.md). Only flag if unresolved EVERYWHERE in the batch.
        if all_texts and unresolved_ra:
            other_def_ra = set()
            for ofname, otext in all_texts.items():
                if ofname == fname:
                    continue
                other_def_ra |= set(re.findall(r'^\s{0,4}RA-(\d+)[a-z]?\s', otext, re.M))
            unresolved_ra -= other_def_ra
        for r in sorted(int(x) for x in unresolved_ra):
            add('N-RA', f'reference to RA-{r} but no RA-{r} definition (checked '
                        f'{"this file + batch" if all_texts else "this file only"})')
        for k, v in Counter(re.findall(r'^\s{0,4}(RA-\d+[a-z]?)\s', text, re.M)).items():
            if v > 1: add('N-RA', f'{k} defined {v} times')

    # ─────────────────── O: MANDATE ANCHORS ──────────────────────
    if has_mandates:
        extended_ran.append('O-MANDATE')
        # MANDATE definitions: "# MANDATE X —" where X is 0-9 or a single uppercase letter
        def_mand = set(re.findall(r'^#\s*MANDATE\s+([0-9A-Z])\b', text, re.M))
        # References: "MANDATE X" where X is 0-9 or a single uppercase letter (not full words)
        ref_mand = set(re.findall(r'\bMANDATE\s+([0-9A-Z])\b', text))
        unresolved_mand = ref_mand - def_mand
        # CROSS-FILE FALLBACK (v2.8): MANDATE 0/1/2 are GLOBAL — defined once (in
        # Framework_MockTestCreate.md) and legitimately referenced from other Step specs
        # (e.g. Framework_MockTestAnalyse.md, Framework_PYQAnalyse.md). MANDATE A/B/D are
        # LOCAL — each Step spec intentionally defines its OWN A/B/D with step-specific
        # content, so those never need cross-file resolution but resolving them cross-file
        # too is harmless (same letter existing elsewhere doesn't change local semantics,
        # and the anchor-existence check never inspects content). Only flag if unresolved
        # EVERYWHERE in the batch.
        if all_texts and unresolved_mand:
            other_def_mand = set()
            for ofname, otext in all_texts.items():
                if ofname == fname:
                    continue
                other_def_mand |= set(re.findall(r'^#\s*MANDATE\s+([0-9A-Z])\b', otext, re.M))
            unresolved_mand -= other_def_mand
        for m in sorted(unresolved_mand):
            add('O-MANDATE', f'reference to MANDATE {m} but no MANDATE {m} definition '
                              f'(checked {"this file + batch" if all_texts else "this file only"})')

    # ─────────────────── P: CONSTANT CONSISTENCY ─────────────────
    if has_batch_size:
        extended_ran.append('P-CONST')
        # match only VALUE ASSIGNMENTS ("AUDIT_BATCH_SIZE = 10"), not references like
        # "AUDIT_BATCH_SIZE (§4 S4-6)" where the next digit is a section number, not a size.
        abs_vals = set(re.findall(r'AUDIT_BATCH_SIZE\s*=\s*(\d+)', text))
        if len(abs_vals) > 1:
            add('P-CONST', f'AUDIT_BATCH_SIZE inconsistent values: {sorted(abs_vals)}')
    runmax = set(re.findall(r'RUN_MAX[=\s]+(\d+)', text))
    if len(runmax) > 1:
        extended_ran.append('P-CONST')
        add('P-CONST', f'RUN_MAX inconsistent values: {sorted(runmax)}')

    # ─────────────────── Q: DYNAMIC EXECUTION ────────────────────
    if has_embedded and py_blocks:
        extended_ran.append('Q-DYNAMIC')
        big = max(py_blocks, key=lambda pc: pc[1][0] - pc[0][0])
        raw = block_lines(big[0], big[1]); ind = big[0][1]
        body = '\n'.join(l[ind:] if l[:ind].strip() == '' else l for l in raw)
        import tempfile, subprocess
        tf = os.path.join(tempfile.mkdtemp(), 'emb.py')
        open(tf, 'w').write(body + '\n')
        dyn_status = 'SKIPPED'
        try:
            r = subprocess.run([sys.executable, tf, '--self-test'],
                               capture_output=True, text=True, timeout=180)
            out = (r.stdout + r.stderr).strip().splitlines()
            last = out[-1] if out else ''
            dyn_status = last
            if not re.match(r'SELF-TEST: (\d+)/\1 PASS', last) or r.returncode != 0:
                add('Q-DYNAMIC', f'embedded self-test did not pass: {last!r}')
        except Exception as e:
            dyn_status = f'ERROR: {e}'
            add('Q-DYNAMIC', f'embedded script execution failed: {e!r}')
        info.append(f'dynamic embedded self-test: {dyn_status}')

    # ─────────────────── S: COMPLETION-GATE (v2.6) ───────────────
    # Triggers ONLY on the file that DEFINES the completion gate (the canonical auditor
    # spec) — not on files that merely mention S5-1A in prose. Locks the fix so the
    # completion gate and its 6 regression fixtures cannot be silently removed.
    has_completion = 'def completion_gate(' in text
    if has_completion:
        extended_ran.append('S-COMPLETION')
        required = ['MANDATE B', 'RA-0', 'RA-15a', 'RA-15b', 'S4-3A', 'S5-1A',
                    'P0.5', 'A-INTEGRITY']
        for h in required:
            if h not in text:
                add('S-COMPLETION', f'file defines completion_gate() but v2.6 anchor {h!r} is missing')
        big = max(py_blocks, key=lambda pc: pc[1][0] - pc[0][0])
        body = '\n'.join(block_lines(big[0], big[1]))
        cg = set(re.findall(r"check\('(CG-[^']+)'", body))
        if len(cg) < 6:
            add('S-COMPLETION',
                f'completion-gate regressions missing: found {len(cg)} CG-* self-tests, '
                'need >=6 (skipped-phase2 / partial-review / unsourced-fact / '
                'unviewed-artefact / missing-evidence-file / evidence-backed-pass)')
        # the gate must assert on the ledger AND on on-disk evidence (FIX F)
        for token in ('batches_done', 'evidence_dir', 'fact_sources', 'artefact_stamps'):
            if token not in body:
                add('S-COMPLETION', f'completion_gate() does not reference {token!r} '
                    '(ledger/evidence assertion may be incomplete)')

    # ─────────────────── S2: EXPLAIN COMPLETION-GATE (Step 9/10, v1.7) ────
    # The explanation pipeline wires a SEPARATE ledger-based gate
    # (explain_audit_gate.py — reads audit_progress.json, not the docx). If a file
    # references it, it must name the module AND state the CA1-CA7 contract, so the
    # wiring cannot be mentioned without the enforcing gate + evidence binding.
    # "Wired" means the gate is actually INVOKED (a CLI run line) or its PASS-output
    # contract is documented — NOT merely named in prose. A spec that only disclaims the
    # gate (e.g. "✗ explain_audit_gate.py — no audit performed", or "used by PYQ-2, not
    # this step") names the module without a `.py --` invocation, so it no longer trips
    # this check (self-contained PYQ-3/PYQ-4 + the PYQ-1 delegation note).
    has_explain_gate = ('AUDIT-COMPLETION-GATE' in text) or bool(re.search(r'explain_audit_gate\.py\s+--', text))
    if has_explain_gate:
        extended_ran.append('S2-EXPLAINGATE')
        if 'explain_audit_gate' not in text:
            add('S2-EXPLAINGATE', 'references AUDIT-COMPLETION-GATE but does not name '
                'explain_audit_gate.py (the enforcing module)')
        if not re.search(r'CA1\s*[–—-]\s*CA7|CA1.{0,60}CA7', text):
            add('S2-EXPLAINGATE', 'wires the explanation completion gate but does not '
                'state the CA1-CA7 contract')
        for token in ('audit_progress', 'evidence'):
            if token not in text:
                add('S2-EXPLAINGATE', f'explanation completion gate wired but {token!r} '
                    '(ledger/evidence) is not mentioned')

    # ═════════════════ V-Z — CORPUS TRANSPORT / DELEGATION (v3.0) ═════════════
    # Added after the 2026-07-24 Drive-transport incident and the sixteen-defect
    # register that followed it. Every check below encodes a defect that was found by
    # hand and would otherwise be found by hand again. They are deliberately NARROW:
    # a check that fires on correct work trains people to ignore the validator, which
    # is worse than not having the check.
    # py_blocks holds (open, close) fence markers; reconstruct the source the same way
    # Check B does, including its placeholder substitutions, so a block that Check B
    # accepts is also analysable here.
    _py_trees = []
    for _bi, (_op, _cl) in enumerate(py_blocks):
        _raw = block_lines(_op, _cl)
        _ind = _op[1]
        _body = '\n'.join(l[_ind:] if l[:_ind].strip() == '' else l for l in _raw)
        _probe = re.sub(r'\[ExamCode\]', 'EXAMCODE', _body)
        _probe = re.sub(r'\[N\]', 'NNN', _probe)
        _probe = re.sub(r'\[ExamName\]', 'EXAMNAME', _probe)
        _probe = re.sub(r'<<[^>]+>>', 'PLACEHOLDER_URL', _probe)
        try:
            _py_trees.append((_bi, _probe, ast.parse(_probe)))
        except SyntaxError:
            continue          # placeholder-bearing block; Check B already reports it

    def _call_name(node):
        f = node.func
        if isinstance(f, ast.Name):
            return f.id
        if isinstance(f, ast.Attribute):
            base = getattr(f.value, 'id', '')
            return f'{base}.{f.attr}' if base else f.attr
        return ''

    # ── V — UNGUARDED DRIVE FETCH ─────────────────────────────────────────────
    # DEFECT B. Verified at the time: ZERO try/except existed around any Drive call
    # in the entire 31-file corpus, so one paper above the connector's size cap
    # terminated a 200-paper run. A fetch must either sit inside a try/ or be handed
    # to corpus_io.fetch_drive_docx, which raises TransportFallback for the caller to
    # route to the upload lane.
    DRIVE_FETCH = {'gdrive_download_file', 'download_file_content', 'gdrive_get_file',
                   'drive_download', 'gdrive_read_file'}
    _v_ran = False
    for _bi, _blk, _tree in _py_trees:
        _guarded = set()
        for _n in ast.walk(_tree):
            if isinstance(_n, ast.Try):
                for _sub in ast.walk(_n):
                    _guarded.add(id(_sub))
        for _n in ast.walk(_tree):
            if isinstance(_n, ast.Call) and _call_name(_n) in DRIVE_FETCH:
                _v_ran = True
                if id(_n) not in _guarded:
                    add('V-DRIVEGUARD',
                        f'{_call_name(_n)}() called unguarded in python block {_bi} '
                        f'(line {_n.lineno} of the block). Wrap it in try/except, or '
                        f'route it through corpus_io.fetch_drive_docx so a transport '
                        f'failure degrades to the upload lane instead of ending the run.')
    if _v_ran:
        extended_ran.append('V-DRIVEGUARD')

    # ── W — ENUMERATION CAPTURES fileSize ─────────────────────────────────────
    # DEFECT A. The Drive listing carries fileSize inline. Discarding it makes the
    # AUTO/UPLOAD partition impossible, so an unfetchable paper surfaces only when the
    # download is attempted — in the reported incident, at batch 6 of a clean-looking run.
    for _bi, _blk, _tree in _py_trees:
        for _n in ast.walk(_tree):
            if not isinstance(_n, ast.Dict):
                continue
            _keys = [k.value for k in _n.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            _is_paper = ('source' in _keys and any(
                isinstance(v, ast.Constant) and v.value == 'gdrive' for v in _n.values))
            if not _is_paper:
                continue
            extended_ran.append('W-ENUMSIZE')
            if 'fileSize' not in _keys:
                add('W-ENUMSIZE',
                    f'python block {_bi} builds a Drive paper record '
                    f'{{{", ".join(repr(k) for k in _keys)}}} without fileSize. '
                    f'Capture it at enumeration — it costs no extra API call and it is '
                    f'the only thing that lets transport be planned before fetching.')

    # ── X — PER-ITEM DURABILITY ───────────────────────────────────────────────
    # DEFECT C. The durability unit must be the ITEM, not the batch. When the save runs
    # only after the inner loop, any exception inside it discards every item already
    # processed in that batch: the progress file shows them as never done, and the work
    # is repeated (or, if the accumulator and the processed-list are persisted at
    # different moments, double-counted on resume).
    ITEM_WORK = re.compile(r'^(process|scan|count|analyse|analyze)_\w*(paper|file|docx)$')
    SAVE_FN = re.compile(r'^save_\w*(progress|state)$')
    for _bi, _blk, _tree in _py_trees:
        _block_saves = [_n for _n in ast.walk(_tree)
                        if isinstance(_n, ast.Call) and SAVE_FN.match(_call_name(_n))]
        if not _block_saves:
            continue
        for _n in ast.walk(_tree):
            if not isinstance(_n, ast.For):
                continue
            _inner = list(ast.walk(_n))
            _does_work = any(isinstance(c, ast.Call) and ITEM_WORK.match(_call_name(c))
                             for c in _inner)
            if not _does_work:
                continue                      # a reporting/printing loop needs no save
            extended_ran.append('X-DURABILITY')
            _saves_inside = any(isinstance(c, ast.Call) and SAVE_FN.match(_call_name(c))
                                for c in _inner)
            if not _saves_inside:
                _worker = next(_call_name(c) for c in _inner
                               if isinstance(c, ast.Call) and ITEM_WORK.match(_call_name(c)))
                add('X-DURABILITY',
                    f'python block {_bi}: the loop at block-line {_n.lineno} calls '
                    f'{_worker}() per item but never saves inside the loop — the only '
                    f'save is outside it. An exception mid-loop discards every item '
                    f'already processed. Save immediately after each item; keep any '
                    f'batch-level save as a redundant flush.')

    # ── Y — IMAGE WORK MUST BE ACCOUNTED FOR ──────────────────────────────────
    # DEFECT D. Extraction and mapping without a count assertion is how table-embedded
    # and VML images vanished silently for as long as they did: the question simply
    # reads as text and no error is raised anywhere.
    IMG_WORK = ('corpus_io.extract_images', 'corpus_io.map_images_to_questions',
                'extract_and_map_images', 'extract_source_images')
    IMG_ACCOUNT = ('count_image_refs', 'verify_images', 'image_gate_verdict',
                   'gates_passed', 'assert_image_survival')
    if any(w in text for w in IMG_WORK):
        extended_ran.append('Y-IMGGATE')
        if not any(a in text for a in IMG_ACCOUNT):
            add('Y-IMGGATE',
                'performs image extraction/mapping but references no image accounting '
                f'({" / ".join(IMG_ACCOUNT)}). An image that is present in the document '
                'and absent from the mapping produces a wrong classification, never an '
                'error — the count assertion is the only thing that can notice.')

    # ── Z — DELEGATION CONTRACT (Cluster H / I / J) ───────────────────────────
    # A spec may CALL a shared function or write a thin forwarding adapter; it may not
    # keep its own copy. Two implementations under one name emit ZERO drift signal until
    # they disagree — which is exactly how Framework_PYQPrepare kept a table-blind
    # extract_images() long after the same defect had been fixed twice elsewhere.
    # Scope is deliberately the transport/image/governor clusters only. A generic name
    # like check() or self_test() colliding by coincidence is not drift.
    _dir = os.path.dirname(os.path.abspath(path))
    _guarded_names = _cluster_hij_names(_dir)
    if _guarded_names:
        extended_ran.append('Z-DELEGATION')
        for _name in sorted(_guarded_names):
            for _m in re.finditer(r'^([ \t]*)def ' + re.escape(_name) + r'\(', text, re.M):
                _ln = text[:_m.start()].count('\n') + 1
                if _is_forwarding_adapter(text, _m.end()):
                    continue                  # thin adapter that delegates — permitted
                add('Z-DELEGATION',
                    f'line {_ln}: defines {_name}(), which is owned by the shared '
                    f'transport/image engine. Call it or write a thin forwarding '
                    f'adapter; a local copy drifts silently.')

    # ─────────────────── REPORT ──────────────────────────────────
    print(f'\n{"="*60}')
    print(f'FILE: {fname}')
    print(f'  Lines: {len(lines)}')
    print(f'  Code blocks: {len(pairs)} paired | Python AST clean: {ast_ok}/{len(py_blocks)}')
    if header_ver:
        print(f'  Version: header=v{header_ver}' +
              (f' footer=v{footer_ver}' if footer_ver else '') +
              (f' changelog=v{changelog_ver}' if changelog_ver else ''))
    if live_counts:
        print(f'  Gate counts: {sorted(live_counts.keys())}')
    print(f'  Sections defined: {len(def_sections)}')
    if extended_ran:
        _seen_ext = []
        for _e in extended_ran:
            if _e not in _seen_ext:
                _seen_ext.append(_e)
        print(f'  Extended checks: {", ".join(_seen_ext)}')
    for inf in info:
        print(f'  {inf}')
    print(f'-'*60)

    if not issues:
        print(f'RESULT: ✅ 0 ISSUES — all checks pass.')
        return 0
    by_cat = {}
    for cat, msg in issues:
        by_cat.setdefault(cat, []).append(msg)
    for cat in sorted(by_cat):
        print(f'  [{cat}] {len(by_cat[cat])} issue(s):')
        for m in by_cat[cat]:
            print(f'      - {m}')
    print(f'-'*60)
    print(f'RESULT: ❌ {len(issues)} ISSUE(S) FOUND.')
    return len(issues)

# ═══════════════════════════════════════════════════════════════════════
# CHECK Z SUPPORT — which names the shared engine owns
# ═══════════════════════════════════════════════════════════════════════
# Names that collide by coincidence rather than by duplication. A harness helper
# called check() in a spec is not a re-implementation of blueprint_core.check().
_Z_GENERIC = {'self_test', 'check', 'main', 'run', 'setup'}
_Z_CACHE = {}


def _cluster_hij_names(directory):
    """Public names owned by corpus_io (Clusters I/J) and blueprint_core Cluster H.

    Read from the engine sources themselves, never from a hardcoded list, so the check
    cannot go stale the moment a function is added. Returns an empty set when the
    engines are not present next to the specs — the check then silently does not run,
    which is correct: with no engine there is nothing to delegate to.
    """
    if directory in _Z_CACHE:
        return _Z_CACHE[directory]
    names = set()
    cio = os.path.join(directory, 'corpus_io.py')
    if os.path.exists(cio):
        try:
            src = open(cio, encoding='utf-8').read()
            names |= {n.name for n in ast.parse(src).body
                      if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                      and not n.name.startswith('_')}
        except (SyntaxError, OSError):
            pass
    bcp = os.path.join(directory, 'blueprint_core.py')
    if os.path.exists(bcp):
        try:
            # GAP-2026-07-25-002. This used to start at the 'CLUSTER H' marker, which
            # guarded 10 of the engine's 40 public names. The 30 it did NOT guard were
            # Clusters A-G — the entire taxonomy-parsing surface (parse_taxonomy_level,
            # is_taxonomy_heading, slugify, detect_question_start) and the entire
            # allocation core. Measured consequence: the corpus reported 0 issues while
            # Framework_MockTestAnalyse carried duplicate copies of score_difficulty and
            # determine_strip_mode, and Framework_PYQSort re-implemented heading matching
            # rather than calling the canonical parser it already imported — which is the
            # defect this gap was raised for. A check that covers a quarter of what it
            # names is not a check. The whole public surface is now owned.
            src = open(bcp, encoding='utf-8').read()
            names |= {n.name for n in ast.parse(src).body
                      if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                      and not n.name.startswith('_')}
        except (SyntaxError, OSError):
            pass
    names -= _Z_GENERIC
    _Z_CACHE[directory] = names
    return names


def _is_forwarding_adapter(text, def_end):
    """True when a local def exists only to hand the call straight to the engine.

    A thin adapter is legitimate — it keeps a spec's call sites readable without owning
    any logic. Anything longer is a second implementation. The test is deliberately
    crude and generous: within the first stretch of the body, a call qualified by a
    module name (corpus_io.x / bc.x) must appear.
    """
    body = text[def_end:def_end + 900]
    body = body.split('\ndef ')[0]
    return bool(re.search(r'\b(corpus_io|bc|blueprint_core)\.\w+\s*\(', body))


# ═══════════════════════════════════════════════════════════════════════
# CHECK AF — DELIVERABLE FILENAME CONTRACT (corpus-level)
# ═══════════════════════════════════════════════════════════════════════
# GAP-2026-07-25-002. Producers declare deliverables as [ExamCode]_<n>.<ext> in
# their delivery contracts; consumers discover them with glob() literals. NOTHING
# compared the two. PYQAnalyse v2.6 renamed the Analysis doc and PYQSort's glob
# became EXACTLY COMPLEMENTARY to the new name — it matched every filename the
# framework no longer produced and none of the one it did — for 19 days and 7
# releases, through a changelog that asserted downstream compatibility.
#
# This is Check T's idea applied to the right primitive: T covers re.search/re.match
# against paths['KEY'] and cannot see glob().
#
# A pattern matching at least ONE declared deliverable passes: a consumer may
# legitimately accept several shapes. The point is that it must match SOMETHING the
# corpus actually produces.
DELIVERABLE_DECL_RE = re.compile(
    r'\[ExamCode\]_([A-Za-z0-9_\[\]]+)\.(docx|json|xlsx|md)')
GLOB_LITERAL_RE = re.compile(r"glob\.glob\(\s*(?:os\.path\.join\([^,]+,\s*)?"
                             r"f?['\"]([^'\"]+)['\"]")
# Matched against the pattern text WITHOUT a leading underscore. The first draft of
# this check watched '_exam_config' and '_taxonomy_draft', which silently skipped
# the four real globs written as '*exam_config.json' and '*taxonomy_draft*.json' —
# the two most load-bearing JSON artefacts in Phase 1 would have been free to be
# renamed undetected. A watchlist that misses the live cases is decoration.
AF_WATCHED = ('PYQ_', 'Analysis', 'blueprint', 'registry', 'exam_config',
              'approval_record', 'taxonomy_draft', 'Create', 'scan_progress',
              'classifications', 'count_progress', 'subtopic_manifest',
              'section_rules')


def check_af_deliverable_filename_contract(all_texts):
    """Every watched glob literal must match at least one declared deliverable."""
    import fnmatch
    declared = set()
    for text in all_texts.values():
        for m in DELIVERABLE_DECL_RE.finditer(text):
            stem, ext = m.group(1), m.group(2)
            stem = re.sub(r'\[[^\]]+\]', 'X', stem)   # [N]/[Subject] -> probe value
            declared.add('EXAMCODE_%s.%s' % (stem, ext))
    if not declared:
        return []
    issues = []
    for fname, text in sorted(all_texts.items()):
        for i, line in enumerate(text.split('\n'), 1):
            for m in GLOB_LITERAL_RE.finditer(line):
                pat = os.path.basename(m.group(1))
                if not any(w in pat for w in AF_WATCHED):
                    continue
                probe = (pat.replace('{EXAM}', 'EXAMCODE')
                            .replace('{exam_code}', 'EXAMCODE'))
                if not any(fnmatch.fnmatch(d, probe) for d in declared):
                    issues.append((fname,
                        'L%d: glob pattern %r matches NONE of the deliverable '
                        'filenames declared anywhere in the corpus. A deliverable '
                        'rename is a cross-step contract change, not a docs edit '
                        '(GAP-2026-07-25-002).' % (i, pat)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AG — SHARED ARTEFACT READERS (corpus-level)
# ═══════════════════════════════════════════════════════════════════════
# GAP-2026-07-25-002, the structural half. Check AF catches a consumer that looks
# for the WRONG NAME. It cannot catch a consumer that finds the right file and then
# parses it WRONGLY — which was the silent P0, and which had three instances at
# once: PYQSort flattened six subjects into one, and both of Step 5's readers
# returned zero subtopics from any real Analysis doc.
#
# Root cause was structural, not attentional: nothing prevented a spec from opening
# a shared artefact and inventing its own parse. corpus_io Cluster K is now THE
# reader/writer/verifier for the Analysis doc; this check enforces that it is the
# ONLY one, so the class cannot be reintroduced by a future edit that looks locally
# reasonable.
AG_ARTEFACTS = {'Analysis': ('_PYQ_Analysis', 'Analysis doc', 'Analysis Word'),
                }
AG_READER_HINTS = ('read_analysis_doc', 'write_analysis_doc', 'corpus_io')


def check_ag_shared_artefact_readers(all_texts):
    """No spec may hand-parse a shared artefact that an engine owns a reader for."""
    issues = []
    opener = re.compile(r'\b(?:Document|WDoc)\s*\(')
    for fname, text in sorted(all_texts.items()):
        if not fname.endswith('.md'):
            continue
        for block in re.findall(r'```python\n(.*?)```', text, re.S):
            if not opener.search(block):
                continue
            if not any(tok in block for tok in AG_ARTEFACTS['Analysis']):
                continue
            if any(h in block for h in AG_READER_HINTS):
                continue          # delegates — correct
            first = block.strip().split('\n', 1)[0][:70]
            issues.append((fname,
                'a code block opens a Word document and refers to the Analysis doc '
                'without going through corpus_io Cluster K. The Analysis doc has '
                'exactly ONE reader (corpus_io.read_analysis_doc) and ONE writer '
                '(corpus_io.write_analysis_doc). Four independent readers is how '
                'GAP-2026-07-25-002 happened: three of them were wrong and nothing '
                'compared them. Block starts: %r' % first))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AH — SPEC <-> ENGINE ROUTING (corpus-level)
# ═══════════════════════════════════════════════════════════════════════
# GAP-2026-07-25-002, found by the post-release sync audit. Check AA proves every
# trigger in routes.json is nameable in the skill and vice versa. It says nothing
# about whether the ENGINES a spec actually imports are routed to the trigger that
# runs it — and 9 such desyncs existed silently, including corpus_io.py absent from
# PYQApprove. That one was harmless only for as long as S4-2 was a `pass` stub; the
# moment S4-2 became a real call it would have been an ImportError at the exact
# point PYQApprove generates the Analysis doc.
#
# Rule, deliberately conservative: every engine a spec imports or calls by module
# alias must be routed to EVERY trigger that loads that spec. Routing an engine a
# particular trigger does not exercise costs nothing; omitting one it does is a
# runtime failure the operator sees as an unexplained traceback.
_AH_ENGINES = ('blueprint_core.py', 'corpus_io.py', 'reconcile_taxonomy.py',
               'paper_pipeline.py', 'explain_engine.py', 'explain_audit_gate.py',
               'syllabus_provenance.py')


def check_ah_spec_engine_routing(directory):
    issues = []
    routes_path = os.path.join(directory, 'routes.json')
    if not os.path.exists(routes_path):
        return issues
    try:
        import json as _json
        routes = _json.load(open(routes_path, encoding='utf-8'))
    except Exception as exc:
        return [('routes.json', 'unreadable: %s' % exc)]
    cache = {}
    for trig, files in sorted(routes.items()):
        for spec in [f for f in files if f.startswith('Framework_')]:
            path = os.path.join(directory, spec)
            if not os.path.exists(path):
                continue
            if spec not in cache:
                try:
                    cache[spec] = open(path, encoding='utf-8').read()
                except OSError:
                    cache[spec] = ''
            text = cache[spec]
            for eng in _AH_ENGINES:
                mod = eng[:-3]
                used = (re.search(r'(?:^|\n)\s*(?:import\s+%s\b|from\s+%s\s+import)'
                                  % (mod, mod), text)
                        or re.search(r'(?:^|\n)[^#\n]*\b%s\.\w+\s*\(' % mod, text))
                if used and eng not in files:
                    issues.append(('routes.json',
                        'trigger %r loads %s, which imports %s — but %s is not routed '
                        'to that trigger. The step will raise ImportError at the first '
                        'call (GAP-2026-07-25-002).' % (trig, spec, eng, eng)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AI — DECLARED-VS-ACTUAL ENGINE DEPENDENCY PARITY
# (v2.12 — GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D5/D7)
#
# CHECK AH covers SPEC -> engine. This covers ENGINE -> engine, which AH cannot
# see: audit_canonical.py imports blueprint_core, and corpus_io.py imports
# blueprint_core, yet blueprint_core.py was routed to NEITHER the audit triggers
# NOR the create triggers. routes.json therefore actively told the operator that
# blueprint_core was not needed — the machine-readable root cause of the gap.
# For every routed .py, every repo module it imports must be routed alongside it.
# ═══════════════════════════════════════════════════════════════════════
def check_ai_engine_dependency_parity(directory):
    issues = []
    routes_path = os.path.join(directory, 'routes.json')
    if not os.path.exists(routes_path):
        return issues
    try:
        import json as _json
        routes = _json.load(open(routes_path, encoding='utf-8'))
    except Exception as exc:
        return [('routes.json', 'unreadable: %s' % exc)]
    import ast as _ast
    repo_mods = {f[:-3] for f in os.listdir(directory) if f.endswith('.py')}
    deps = {}
    for fname in sorted(f for f in os.listdir(directory) if f.endswith('.py')):
        try:
            tree = _ast.parse(open(os.path.join(directory, fname), encoding='utf-8').read())
        except SyntaxError:
            continue
        found = set()
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                found |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, _ast.ImportFrom) and node.module:
                found.add(node.module.split('.')[0])
        found &= repo_mods
        found.discard(fname[:-3])
        deps[fname] = sorted(found)
    for trig, files in sorted(routes.items()):
        if not isinstance(files, list):
            continue
        for eng in [f for f in files if f.endswith('.py')]:
            for dep in deps.get(eng, []):
                if dep + '.py' not in files:
                    issues.append(('routes.json',
                        'trigger %r routes %s, which imports %s.py — but %s.py is '
                        'NOT routed to that trigger. The declared dependency set '
                        'diverges from the actual one; the step will hit an '
                        'ImportError or a silently-degraded gate '
                        '(GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D5/D7).'
                        % (trig, eng, dep, dep)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AJ — UNDEFINED-NAME SCAN (every repo engine)
# (v2.12 — GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D1)
#
# THE GENERALISED GUARD. `bc` was READ at three sites in audit_canonical.py and
# BOUND at none: the v2.10 delegation was written into the comments and the call
# sites, but the import was never added. Every gate, every fixture and the whole
# 51/51 self-test passed over it, because the only branch that touched `bc` was
# never executed by any fixture. A whole-file AST scan finds this class of defect
# in ONE pass, without anyone having to anticipate which gate will have it next.
# ═══════════════════════════════════════════════════════════════════════
def check_aj_undefined_names(directory):
    issues = []
    import ast as _ast, builtins as _bi
    for fname in sorted(f for f in os.listdir(directory) if f.endswith('.py')):
        path = os.path.join(directory, fname)
        try:
            tree = _ast.parse(open(path, encoding='utf-8').read())
        except SyntaxError as exc:
            issues.append((fname, 'ast.parse SyntaxError line %s (truncated/corrupt)'
                           % exc.lineno))
            continue
        bound = set(dir(_bi)) | {'__file__', '__name__', '__doc__',
                                 '__builtins__', '__spec__', '__package__'}
        for node in _ast.walk(tree):
            if isinstance(node, _ast.alias):
                bound.add(node.asname or node.name.split('.')[0])
            elif isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
                bound.add(node.name)
            elif isinstance(node, _ast.Name) and isinstance(node.ctx, (_ast.Store, _ast.Del)):
                bound.add(node.id)
            elif isinstance(node, _ast.arg):
                bound.add(node.arg)
            elif isinstance(node, _ast.ExceptHandler) and node.name:
                bound.add(node.name)
            elif isinstance(node, (_ast.Global, _ast.Nonlocal)):
                bound |= set(node.names)
        undefined = {}
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Name) and isinstance(node.ctx, _ast.Load)
                    and node.id not in bound):
                undefined.setdefault(node.id, []).append(node.lineno)
        for name, lines in sorted(undefined.items()):
            issues.append((fname,
                'name %r is READ at line(s) %s but BOUND NOWHERE. Either the import '
                'is missing (the exact v2.10 A-FIGPROFILE defect: a delegation '
                'written into the comments and call sites but never imported) or it '
                'is a typo. Either way this raises NameError the first time that '
                'branch executes (GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING D1).'
                % (name, ', '.join(str(x) for x in sorted(set(lines))))))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AK — B3 DELIVERABLE CARDINALITY CONSISTENCY
# (v2.12 — GAP-2026-08-01-FIGPROFILE-ENGINE-BINDING, deployment-hold review)
#
# WHY THIS EXISTS. The 6 -> 8 B3 cardinality change first landed in §13-7 ONLY.
# Nine other sites in Framework_Blueprint.md, one in Framework_DeliveryFooter.md
# and one in Framework_MockTestCreateAudit.md still said 6 — including §11 S11-3
# PART B, which is the OPERATIVE present_files call. A session following the spec
# would still have delivered 6 files and the two engines would never have reached
# the exam project: the fix would have been inert, exactly the failure D2/D3 exist
# to end. Worse, the S11-3 checklist mandated [ExamCode]-prefixed names for ALL
# files, which for the two engines is the prefix that BREAKS the module import.
#
# CLAUDE.md states the rule this enforces: "A deliverable RENAME or CARDINALITY
# change is a cross-step contract change, never a docs-only edit." Prose cannot
# enforce that; this check can. Any B3 delivery-count claim that disagrees with
# the others is reported, so the next cardinality change cannot land partially.
# ═══════════════════════════════════════════════════════════════════════
_AK_B3_EXPECTED = 6      # B3 deliverable count — bump here AND in every spec site
                         # 6, not 8 (v2.12.1): the repo engines are NOT B3
                         # deliverables. Step 8 copies them from the verified
                         # clone; engines are never provisioned per-exam.

# ─────────────────────────────────────────────────────────────────────────────
# CHECK AL — STEP-7 DELIVERY-SET CONTRACT (cross-step)
# ─────────────────────────────────────────────────────────────────────────────
# MOTIVATING DEFECT — GAP-2026-08-01-DELIVERY-SET-DRIFT. Framework_MockTestCreate
# v5.35 added the Tier-A audit dossier as a THIRD delivered file (S13-4b) and did
# not widen S13-7 check 6, which asserted `staged == {docx_name, reg_name}` — a
# hardcoded set of two. The extra file made the comparison false and S13-7 raised
# SystemExit, so Step 7 could not deliver AT ALL, on every exam and every mock. It
# would have failed on the first run after deployment.
#
# Every existing auditor passed, twice, plus a fresh-clone deployment simulation.
# NOTHING cross-verified the delivery set: it was stated in prose at four sites and
# asserted in code at one, with nothing binding them. Check AK guards the Step-6 B3
# bundle, a different contract entirely. This closes that blind spot.
#
# The rule enforced: the ASSERTION must be DERIVED, never hardcoded. A gate that
# hardcodes what its own producer writes will drift the moment the producer changes,
# and the drift is a HARD STOP rather than a warning.
_AL_HARDCODED = re.compile(r'staged\s*==\s*\{\s*docx_name\s*,\s*reg_name\s*\}')
_AL_STALE_PROSE = re.compile(
    r'(?:EXACTLY|exactly) the (?:2|two) deliverables?'
    r'|delivers EXACTLY two files'
    r'|Stage ONLY the two deliverables')


def check_al_delivery_set(directory):
    issues = []
    for fname in sorted(f for f in os.listdir(directory)
                        if f.startswith('Framework_') and f.endswith('.md')):
        try:
            text = open(os.path.join(directory, fname), encoding='utf-8').read()
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            # Version-history prose QUOTES the defective assertion in order to
            # explain it; quoting a defect is not committing it. Only live spec
            # body counts. (Found on AL's first run: the check flagged this very
            # file's own v5.36 changelog entry describing the bug it guards.)
            if line.lstrip().startswith('#'):
                continue
            if _AL_HARDCODED.search(line):
                issues.append((fname,
                    'line %d hardcodes the Step-7 delivery set as {docx, registry}. '
                    'It MUST be DERIVED from what was actually staged (docx + '
                    'registry always, dossier when S13-4b wrote one). A hardcoded '
                    'set drifts the moment a producer adds a file, and S13-7 turns '
                    'that drift into a HARD STOP — exactly the v5.35 defect.'
                    % lineno))
            if _AL_STALE_PROSE.search(line):
                issues.append((fname,
                    'line %d still describes the Step-7 delivery as exactly TWO '
                    'files. Since v5.35 the closed set also carries '
                    '[ExamCode]_M[N]_audit_dossier.json when S13-4b writes one. A '
                    'cardinality claim is a cross-step contract: every site must '
                    'move together, or a session following THIS site stages the '
                    'wrong set.' % lineno))
    return issues


def check_ak_b3_cardinality(directory):
    issues = []
    # Sites that talk about the Step-6 B3 delivery specifically. Step 5's own
    # 6-file delivery and unrelated numerics must NOT be swept in, so each
    # pattern is anchored on B3 / MockBlueprint / Step-1-output vocabulary.
    pats = [
        (r'present_files with all (\d+) output files', 'S11-3 / §13-7A delivery call'),
        (r'B3\s*:\s*Final validation → generate all (\d+) output files', '§8 batch overview'),
        (r'B3 delivers all (\d+) files in ONE present_files call', '§13-7 delivery order'),
        (r'B3 FINAL DELIVERABLES \((\d+) files', 'DeliveryFooter §3 registry'),
        (r'Step 6 MockBlueprint: after B3 final delivery of all (\d+) files',
         'DeliveryFooter §1 F2'),
        (r'All (\d+) files exist at /mnt/user-data/outputs/', 'S11-3 checklist'),
        (r'All (\d+) files produced by Step 1', '§13 header'),
        (r'All (\d+) output files generated and present_files called', '§15 checklist'),
        (r'After downloading all (\d+) files from B3', '§13-8 header'),
        (r'B3 → all (\d+) output files re-delivered', 're-generation path'),
        (r'present_files\(all (\d+) final files\)', '§13-1 pipeline map'),
        (r'B3 final delivery \((\d+) files\)', 'footer-type map'),
        (r'Verify that all (\d+) Step 6 output files were uploaded', 'MANDATE A hard stop'),
        (r're-run B3 → all (\d+) output', 're-generation path'),
        (r'Run Step 1 again → download all (\d+) new output files', 'restart path'),
    ]
    for fname in sorted(f for f in os.listdir(directory)
                        if f.startswith('Framework_') and f.endswith('.md')):
        try:
            text = open(os.path.join(directory, fname), encoding='utf-8').read()
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith('#   ') and 'previously read' in line:
                continue          # historical changelog prose in headers
            for pat, where in pats:
                m = re.search(pat, line)
                if m and int(m.group(1)) != _AK_B3_EXPECTED:
                    issues.append((fname,
                        'line %d (%s) claims the Step-6 B3 delivery is %s files, but '
                        'the contract is %d. A CARDINALITY change is a cross-step '
                        'contract change, never a docs-only edit — every site that '
                        'describes the delivery must move together, or a session '
                        'following THIS site delivers the wrong set.'
                        % (lineno, where, m.group(1), _AK_B3_EXPECTED)))
            # HOLLOW-MVP SIGNATURE. "13/13" (and its siblings) was the RETIRED
            # constant-print self_test that executed no gate. P1 instructs the
            # operator to REJECT it as proof of a false-clean. Any site that
            # instead tells the operator to CONFIRM it inverts that rule — which
            # is what a stale B3 checklist did at two separate sites. Historical
            # prose that names the literal in order to retire it is fine; a
            # checkbox or "passed (N/N)" assertion is not.
            if re.search(r'(13/13|24/24|66/66)', line):
                asserts_it = re.search(r'(☐|✓|MUST print|passed)\s*[^#]*?(13/13|24/24|66/66)',
                                       line)
                retires_it = re.search(r'RETIRED|REJECT|stale|superseded|hollow|constant.print'
                                       r'|previously read|old\b', line, re.I)
                if asserts_it and not retires_it:
                    issues.append((fname,
                        'line %d asserts the RETIRED hollow-MVP self-test signature '
                        '(%s) as a PASS criterion. That literal is the constant-print '
                        'stub which executed no gate and which P1 is instructed to '
                        'REJECT; confirming it certifies a false-clean. Require a '
                        'FIXTURE-BASED N/N with N >= AUTH_GATE_FLOOR instead.'
                        % (lineno, asserts_it.group(2))))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AA — ROUTES <-> SKILL SYNC (batch-level, both directions)
# ═══════════════════════════════════════════════════════════════════════
def check_aa_routes_skill_sync(directory):
    """Every routed trigger must be nameable in the skill, and vice versa.

    Two independent failure directions, both silent:
      * a trigger in routes.json the skill never mentions is unreachable — the operator
        types it and nothing routes;
      * a trigger named in the skill with no route loads no spec, so the step runs from
        memory, which is the one thing the framework exists to prevent.
    The engine-count claim is checked too: it is prose that goes stale the moment a
    module is routed, and it is the only place the corpus states how many there are.

    Skips silently when either file is unreachable — the skill normally lives outside
    the project directory.
    """
    issues = []
    routes_path = os.path.join(directory, 'routes.json')
    if not os.path.exists(routes_path):
        return issues
    try:
        import json as _json
        routes = _json.load(open(routes_path, encoding='utf-8'))
    except Exception as exc:
        return [('routes.json', 'unreadable: %s' % exc)]

    skill = None
    for cand in (os.path.join(directory, 'SKILL.md'),
                 '/mnt/skills/user/mock-test-framework/SKILL.md'):
        if os.path.exists(cand):
            try:
                skill = open(cand, encoding='utf-8').read()
                break
            except OSError:
                pass
    if skill is None:
        return issues

    for trig in routes:
        if not re.search(r'\b' + re.escape(trig) + r'\b', skill):
            issues.append(('routes.json',
                           'trigger %r is routed but never named in SKILL.md — '
                           'it cannot be invoked' % trig))
    for m in re.finditer(r'\b(PYQ[A-Z]\w+|Mock[A-Z]\w+|Test[A-Z]\w+|ScopedBlueprint)\b', skill):
        if m.group(1) not in routes:
            issues.append(('SKILL.md',
                           'names trigger %r but routes.json has no such entry — the step '
                           'would run with no spec loaded' % m.group(1)))
    m = re.search(r'(\d+)\s+framework specs and\s+(\d+)\s+engine scripts', skill)
    if m:
        real_engines = len({f for v in routes.values() for f in v if f.endswith('.py')})
        if int(m.group(2)) != real_engines:
            issues.append(('SKILL.md', 'claims %s engine scripts; routes.json routes %d'
                           % (m.group(2), real_engines)))
        # The spec-count claim is only meaningful when this directory really IS the
        # corpus. Validating one file in a scratch directory must not report that the
        # corpus has shrunk — so the count is compared only when every routed spec
        # resolves here.
        routed_specs = {f for v in routes.values() for f in v if f.endswith('.md')}
        is_full_corpus = routed_specs and all(
            os.path.exists(os.path.join(directory, f)) for f in routed_specs)
        real_specs = len([f for f in os.listdir(directory)
                          if f.startswith('Framework_') and f.endswith('.md')])
        if is_full_corpus and real_specs and int(m.group(1)) != real_specs:
            issues.append(('SKILL.md', 'claims %s framework specs; the corpus has %d'
                           % (m.group(1), real_specs)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AB — THIN-CORE PURITY (batch-level)
# ═══════════════════════════════════════════════════════════════════════
# blueprint_core.py and paper_pipeline.py are imported at runtime by Steps 6-11 purely
# for arithmetic. The invariant was documented as "enforced by validate_framework_md.py"
# while no such check existed. It matters: a PIL import landing in blueprint_core.py
# makes it unimportable wherever Pillow is absent — the P0 recorded in
# Framework_MockTestAnalyse v2.26, where a failed `import blueprint_core` aborted Step 5
# for EVERY exam. It is also the whole reason corpus_io.py exists as a separate module.
#
# The standard-library set is taken from the running interpreter rather than written out
# here, so the check cannot drift as Python evolves.
_AB_STDLIB = set(getattr(sys, 'stdlib_module_names', ()) or
                 ('abc ast collections contextlib copy csv datetime decimal difflib enum '
                  'fnmatch fractions functools glob hashlib heapq io itertools json '
                  'logging math os pathlib random re shutil statistics string sys '
                  'tempfile textwrap time traceback types typing unicodedata urllib '
                  'uuid warnings zipfile zlib').split())

_AB_IO_CALLS = {'open', 'os.makedirs', 'os.mkdir', 'os.remove', 'os.unlink', 'os.rename',
                'os.rmdir', 'shutil.copy', 'shutil.copy2', 'shutil.move', 'shutil.rmtree',
                'os.walk', 'os.listdir'}
_AB_MODULES = ('blueprint_core.py', 'paper_pipeline.py')


def check_ab_thin_core_purity(directory):
    """The thin core must import only the standard library and touch no files."""
    issues = []
    for mod in _AB_MODULES:
        path = os.path.join(directory, mod)
        if not os.path.exists(path):
            continue
        try:
            tree = ast.parse(open(path, encoding='utf-8').read())
        except (SyntaxError, OSError) as exc:
            issues.append((mod, 'could not be parsed: %s' % exc))
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    root = a.name.split('.')[0]
                    if root not in _AB_STDLIB:
                        issues.append((mod, 'line %d: imports %r, which is not in the '
                                            'standard library. The thin core must stay '
                                            'importable everywhere — put impure '
                                            'dependencies in corpus_io.py or '
                                            'explain_engine.py.' % (n.lineno, root)))
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                root = n.module.split('.')[0]
                if root not in _AB_STDLIB:
                    issues.append((mod, 'line %d: imports from %r, which is not in the '
                                        'standard library.' % (n.lineno, root)))
            elif isinstance(n, ast.Call):
                f = n.func
                if isinstance(f, ast.Name):
                    name = f.id
                elif isinstance(f, ast.Attribute):
                    name = '%s.%s' % (getattr(f.value, 'id', ''), f.attr)
                else:
                    name = ''
                if name in _AB_IO_CALLS:
                    issues.append((mod, 'line %d: calls %s() — the thin core performs no '
                                        'file I/O. Move it to the I/O shell.'
                                   % (n.lineno, name)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AC — AGGREGATOR SINGLE-EXIT           (GAP-2026-07-25-001, D-1)
# ═══════════════════════════════════════════════════════════════════════
# A function that accumulates into ONE local list and returns it is an
# AGGREGATOR. A `return` positioned after accumulation has begun silently
# discards every later accumulation on that path. This is not a style rule:
# reconcile() v1.0 expressed "don't also run the other form of C4" as `return`,
# which terminated the function and disabled three unrelated checks (C5, C6, C7)
# for every current-generation exam, producing a CLEAN record that auto-locked
# the taxonomy.
#
# A name-presence check CANNOT catch this — every finding-class literal was
# present in the engine. The code was unreachable. So this check targets
# REACHABILITY, not vocabulary.
#
# Guard clauses that precede ALL accumulation are the correct idiom and are
# immune (e.g. `if not os.path.exists(p): return issues`).
def check_ac_aggregator_single_exit(directory):
    issues = []
    for path in sorted(glob.glob(os.path.join(directory, '*.py'))):
        mod = os.path.basename(path)
        try:
            tree = ast.parse(open(path, encoding='utf-8').read())
        except (SyntaxError, OSError) as exc:
            issues.append((mod, 'could not be parsed: %s' % exc))
            continue
        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            acc = {}
            for n in ast.walk(fn):
                if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                        and n.func.attr in ('append', 'extend')
                        and isinstance(n.func.value, ast.Name)):
                    acc.setdefault(n.func.value.id, []).append(n.lineno)
            rets = [n for n in ast.walk(fn) if isinstance(n, ast.Return)]
            for name, lines in acc.items():
                if len(lines) < 3:
                    continue
                if not any(isinstance(r.value, ast.Name) and r.value.id == name
                           for r in rets):
                    continue
                first, last = min(lines), max(lines)
                early = sorted(r.lineno for r in rets if first < r.lineno < last)
                if early:
                    issues.append((mod,
                        '%s() @L%d accumulates into %r at %d sites (last @L%d) but '
                        'returns early at L%s — every accumulation after that line is '
                        'unreachable on that path. If the intent was to skip a sibling '
                        'branch, use if/else; a function that aggregates must have a '
                        'SINGLE EXIT.' % (fn.name, fn.lineno, name, len(lines), last, early)))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AD — EMITTED FINDING-CLASS IS DOCUMENTED        (D-6)
# ═══════════════════════════════════════════════════════════════════════
# An engine may not emit a finding class that no spec documents. C7's four
# classes (UNANCHORABLE_SUBJECT, DECLARED_DEVIATION, ANCHOR_MAP_UNUSED,
# NAME_CANONICALIZED) appeared in no spec at all, while the S4-4 gate template
# REQUIRED four lines built from them. An undocumented check is one no reader
# can notice is missing — a direct contributor to D-1's invisibility.
def check_ad_emitted_class_documented(directory):
    issues = []
    specs = {}
    for p in sorted(glob.glob(os.path.join(directory, 'Framework_*.md'))):
        try:
            specs[os.path.basename(p)] = open(p, encoding='utf-8').read()
        except OSError:
            pass
    if not specs:
        return issues
    for path in sorted(glob.glob(os.path.join(directory, '*.py'))):
        mod = os.path.basename(path)
        try:
            tree = ast.parse(open(path, encoding='utf-8').read())
        except (SyntaxError, OSError):
            continue
        emitted = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Dict):
                for k, v in zip(n.keys, n.values):
                    if (isinstance(k, ast.Constant) and k.value == 'class'
                            and isinstance(v, ast.Constant)
                            and isinstance(v.value, str) and v.value.isupper()):
                        emitted.add(v.value)
        for cls in sorted(emitted):
            if not any(cls in text for text in specs.values()):
                issues.append((mod,
                    'emits finding class %r which appears in NO Framework_*.md. '
                    'A check the specs do not document is a check no reader can '
                    'notice is missing.' % cls))
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK AE — NORMALIZATION CONFORMANCE                  (N-1)
# ═══════════════════════════════════════════════════════════════════════
# A module that defines normalize_label() has declared that names are compared
# in canonical form. A raw `==` between a subscripted value and a loop/local
# variable in such a module is a latent silent no-op: the two sides are usually
# sourced from DIFFERENT pipeline stages (syllabus vs scan), and a difference of
# case, spacing or dash form makes the comparison never match — zeroing the
# check's measurement domain while the check still reports "ran".
#
# Calibration: comparisons against an ALL_CAPS module constant (version and
# schema identity, which must be exact) and comparisons inside self-test
# functions are excluded — both were measured false positives.
def check_ae_normalization_conformance(directory):
    issues = []
    for path in sorted(glob.glob(os.path.join(directory, '*.py'))):
        mod = os.path.basename(path)
        try:
            src = open(path, encoding='utf-8').read()
        except OSError:
            continue
        if 'def normalize_label' not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        skip = set()
        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            if fn.name.startswith('_self_test') or fn.name.startswith('test'):
                for n in ast.walk(fn):
                    skip.add(id(n))
        for n in ast.walk(tree):
            if id(n) in skip:
                continue
            if not (isinstance(n, ast.Compare) and len(n.ops) == 1
                    and isinstance(n.ops[0], (ast.Eq, ast.NotEq))):
                continue
            seg = ast.get_source_segment(src, n) or ''
            if 'normalize_label' in seg:
                continue
            pair = (n.left, n.comparators[0])
            for a, b in (pair, pair[::-1]):
                if isinstance(a, ast.Subscript) and isinstance(b, ast.Name):
                    if b.id.isupper():
                        continue        # module constant — exact by design
                    issues.append((mod,
                        'line %d: raw equality `%s` in a module that defines '
                        'normalize_label(). If these operands come from different '
                        'pipeline stages, cosmetic variance makes this silently '
                        'never match and the surrounding check measures nothing. '
                        'Compare normalize_label() forms, or add an explicit '
                        'comment stating why byte-identity is required.'
                        % (n.lineno, seg)))
                    break
    return issues


# ═══════════════════════════════════════════════════════════════════════
# CHECK T — CROSS-FILE TOKEN CONTRACT (batch-level; needs 2+ files)
# ═══════════════════════════════════════════════════════════════════════
# Registry of known producer functions and the literal on-disk marker tokens they emit.
# Each entry maps an artifact key (matching the `paths['KEY']` naming convention already
# used consistently across every step spec: 'rules', 'blueprint', 'registry', 'manifest')
# to the function that produces it and a regex that extracts its literal marker strings
# from that function's source body. Extend this dict as new producer/marker pairs are
# added to the framework — that is what closes this defect class permanently, rather than
# only for the one instance that has already been found and fixed.
PRODUCER_REGISTRY = {
    'rules': {
        # 'produced_by' must be the literal ACTUAL FUNCTION DEFINITION line (anchored on
        # 'def '), never a bare function-name substring — a bare substring can false-match
        # prose mentions of the function name elsewhere in the file (e.g. changelog text
        # saying "...written by write_section_rules()...") and silently find the WRONG,
        # earlier occurrence, causing this check to find no producer and go silently inert.
        # This exact failure mode was caught empirically during this check's own regression
        # test (a changelog entry mentioning the function name preceded the real def line).
        'produced_by': 'def write_section_rules(',
        'display_name': 'write_section_rules()',
        # Literal marker tokens are plain (non-f-string) quoted strings containing '===' or
        # '---' assigned inside the producer function — e.g. '=== EXAM_STRUCTURE ===',
        # '=== SECTION: {section} ===', '--- Subtopic: {e["subtopic"]} ---'. The f-string
        # {…} placeholders are normalized to a wildcard so a consumer's regex can be tested
        # against a realistic instance of the token.
        'token_pattern': re.compile(r"""['"]((?:===|---)[^'"]*(?:===|---))['"]"""),
    },
}

# ═══════════════════════════════════════════════════════════════════════
# CHECK U — JSON PRODUCER/CONSUMER FIELD CONTRACT (batch-level; needs 2+ files)
# ═══════════════════════════════════════════════════════════════════════
# Same underlying defect class as Check T (a consumer trusting a key/token that no
# producer ever actually emits), applied to JSON artifacts instead of literal text
# markers. Deliberately scoped narrower than "every dict access": a `.get('key', default)`
# read is inherently safe against a missing key (Python's own fallback), so it is NOT the
# same risk category as P0.5's unconditional regex search — flagging every `.get()` call
# would be noise, not signal. The genuinely risky pattern is BARE INDEXING (`d['key']`),
# which raises KeyError if the producer never wrote that key. This check flags exactly
# that: a bare-indexed READ (not a write — `d['key'] = ...` is excluded) of a key that
# cannot be found anywhere in the artifact's own documented schema section(s).
#
# Schema sources are the "§N — ... SCHEMA" reference sections the spec authors themselves
# already maintain as the canonical contract (Framework_Blueprint.md §14 for blueprint.json,
# §12 for registry.json's base fields + Framework_MockTestCreate.md §14 for registry.json's
# Step-7 additions). Field names are extracted from BOTH JSON-literal key syntax
# ("field_name":) and Python write-assignment syntax (registry['field_name'] = ...) within
# each bounded section — the registry schema documents its CONDITIONAL fields (added only
# for passage/figural exams) as Python code, not a JSON block, so scanning only JSON syntax
# would incorrectly report figural_manifests/rc_manifests as undocumented.

def _python_code_line_numbers(text):
    """Return the set of 1-indexed line numbers that are (a) inside an actual ```python
    fenced code block and (b) not themselves a bare '#'-comment line. Reuses the same
    fence-pairing algorithm as Check A. This exists because a bracket-index expression
    like reg['field'] can appear in THREE contexts that are NOT live, executable code and
    must not be treated as a real consumer read: plain prose describing a formula (no
    fence at all), a markdown table/checklist row quoting a field name for documentation,
    and a '#'-comment INSIDE a python fence that merely mentions where a field is written
    elsewhere. All three were found empirically while testing Check U against the real
    corpus (6 of its first 7 flags were exactly this false-positive class) — this filter
    is what makes the check trustworthy rather than noisy."""
    lines = text.split('\n')
    fences = []
    for i, l in enumerate(lines, 1):
        st = l.lstrip()
        if st.startswith('```'):
            indent = len(l) - len(st)
            lang = st[3:].strip() or None
            fences.append((i, indent, lang))
    stack, pairs = [], []
    for (ln, ind, lang) in fences:
        if stack and lang is None:
            pairs.append((stack.pop(), (ln, ind, lang)))
        elif lang is not None:
            stack.append((ln, ind, lang))
        else:
            if stack: pairs.append((stack.pop(), (ln, ind, lang)))
            else: stack.append((ln, ind, lang))
    code_lines = set()
    for (op, cl) in pairs:
        if op[2] != 'python':
            continue
        for ln in range(op[0] + 1, cl[0]):
            if not lines[ln - 1].strip().startswith('#'):
                code_lines.add(ln)
    return code_lines

JSON_SCHEMA_REGISTRY = {
    'blueprint': {
        'var_names': ('bp', 'blueprint'),
        'schema_sections': [
            ('Framework_Blueprint.md',
             re.compile(r'^## §14 — BLUEPRINT JSON SCHEMA', re.M),
             re.compile(r'^## §', re.M)),
        ],
        'display_name': '§14 BLUEPRINT JSON SCHEMA (Framework_Blueprint.md)',
    },
    'registry': {
        'var_names': ('reg', 'registry'),
        'schema_sections': [
            ('Framework_Blueprint.md',
             re.compile(r'^## §12 — REGISTRY SCHEMA', re.M),
             re.compile(r'^## §', re.M)),
            ('Framework_MockTestCreate.md',
             re.compile(r'^# §14 — REGISTRY SCHEMA', re.M),
             re.compile(r'^# §', re.M)),
        ],
        'display_name': "§12/§14 REGISTRY SCHEMA (Framework_Blueprint.md + "
                         "Framework_MockTestCreate.md)",
    },
}

def _extract_bounded_section(text, start_pat, end_pat):
    m = start_pat.search(text)
    if not m:
        return None
    m2 = end_pat.search(text, m.end())
    return text[m.start():m2.start() if m2 else len(text)]

def _json_schema_fields(all_texts, artifact_key):
    """Union of every field name documented for artifact_key, across all its schema
    source files/sections that are present in this batch. Returns None (not an empty
    set) if none of the schema source files are in the batch, so the caller can skip
    the check entirely rather than flag everything as undocumented."""
    spec = JSON_SCHEMA_REGISTRY[artifact_key]
    fields = set()
    found_any = False
    for fname, start_pat, end_pat in spec['schema_sections']:
        text = all_texts.get(fname)
        if text is None:
            continue
        section = _extract_bounded_section(text, start_pat, end_pat)
        if section is None:
            continue
        found_any = True
        fields |= set(re.findall(r'"(\w+)"\s*:', section))          # JSON-literal keys
        for var in spec['var_names']:                                 # Python conditional
            fields |= set(re.findall(re.escape(var) + r"\['(\w+)'\]\s*=(?!=)", section))
    return fields if found_any else None

def check_u_json_field_contract(all_texts):
    """Batch-level: flag a bare-indexed d['field'] READ (var name bp/blueprint/reg/
    registry) where 'field' is not documented anywhere in that artifact's schema
    section(s) present in this batch. A trailing '=' (not '==') immediately after the
    subscript marks a WRITE, not a read, and is excluded — this check is specifically
    about the KeyError-on-read risk, not about who is allowed to populate the dict."""
    issues = []
    for artifact_key, spec in JSON_SCHEMA_REGISTRY.items():
        fields = _json_schema_fields(all_texts, artifact_key)
        if fields is None:
            continue  # none of this artifact's schema source files are in this batch
        for fname, text in all_texts.items():
            code_lines = _python_code_line_numbers(text)
            lines = text.split('\n')
            for i, l in enumerate(lines):
                if (i + 1) not in code_lines:
                    continue  # prose, table row, or comment — not live executable code
                for var in spec['var_names']:
                    for m in re.finditer(re.escape(var) + r"\['(\w+)'\]", l):
                        field = m.group(1)
                        after = l[m.end():].lstrip()
                        if after.startswith('=') and not after.startswith('=='):
                            continue  # write, not a read — out of scope for this check
                        if field not in fields:
                            issues.append((fname,
                                f"L{i+1}: bare {var}['{field}'] read — {field!r} not found "
                                f"in {spec['display_name']} (KeyError risk if this key is "
                                f"ever absent from a real {artifact_key}.json; either the "
                                f"schema doc is missing this field, or this reads an "
                                f"undocumented/nonexistent key — verify which)"))
    return issues

def _extract_function_body(text, def_line_substr):
    """Return the source text of the top-level function whose 'def name(' line matches
    def_line_substr EXACTLY as a def-statement (not a bare mention of the name elsewhere
    in the file), from that 'def ' line up to (but not including) the next top-level
    'def ' at column 0, or end of text. Returns None if no such def line exists."""
    m = re.search(r'^' + re.escape(def_line_substr), text, re.M)
    if not m:
        return None
    def_start = m.start()
    next_def = text.find('\ndef ', def_start + len(def_line_substr))
    return text[def_start:next_def] if next_def > 0 else text[def_start:]

def _producer_tokens(all_texts, artifact_key):
    """Collect real literal marker tokens the artifact_key's producer function emits,
    across whichever file in the batch actually defines that producer."""
    spec = PRODUCER_REGISTRY[artifact_key]
    tokens = set()
    producer_file = None
    for fname, text in all_texts.items():
        body = _extract_function_body(text, spec['produced_by'])
        if body:
            producer_file = fname
            for m in spec['token_pattern'].finditer(body):
                # normalise f-string placeholders like {section} / {e["subtopic"]} to a
                # wildcard so the token is testable as a realistic on-disk instance
                norm = re.sub(r'\{[^}]*\}', 'X', m.group(1))
                tokens.add(norm)
    return producer_file, tokens

def check_t_cross_file_contract(all_texts):
    """Batch-level: for every consumer's literal re.search()/re.match() applied against
    an artifact read via paths['KEY'], verify the literal pattern matches at least one of
    that artifact's producer's real emitted tokens. Returns list of (file, issue_msg)."""
    issues = []
    for artifact_key, spec in PRODUCER_REGISTRY.items():
        producer_file, tokens = _producer_tokens(all_texts, artifact_key)
        if not producer_file or not tokens:
            continue  # producer not in this batch; nothing to cross-check
        for fname, text in all_texts.items():
            lines = text.split('\n')
            for i, l in enumerate(lines):
                # a consumer read of this artifact: open(paths['KEY'], ...)
                if not re.search(r"paths\[\s*['\"]%s['\"]\s*\]" % re.escape(artifact_key), l):
                    continue
                # look at this line + next few for a re.search/re.match against the
                # variable this open() call assigned (simple proximity heuristic — the
                # existing P0.5-style pattern always reads then immediately checks)
                var_m = re.search(r'(\w+)\s*=\s*open\(', l)
                if not var_m:
                    continue
                var = var_m.group(1)
                window = '\n'.join(lines[i:i+6])
                for pm in re.finditer(
                        r"re\.(?:search|match)\(\s*r?['\"]([^'\"]+)['\"]\s*,\s*" + re.escape(var),
                        window):
                    consumer_pattern = pm.group(1)
                    try:
                        matches_any = any(re.search(consumer_pattern, tok, re.I) for tok in tokens)
                    except re.error:
                        continue  # not our concern here — Check F/B would catch a bad regex
                    if not matches_any:
                        line_no = i + 1
                        issues.append((fname,
                            f"L{line_no}: literal pattern {consumer_pattern!r} tested against "
                            f"'{artifact_key}' (produced by {spec['display_name']} in "
                            f"{producer_file}) does not match ANY real token that producer "
                            f"emits ({sorted(tokens)}) — likely hard-coded a doc-alias name "
                            f"instead of the actual on-disk literal (see A-INTEGRITY-FALSEPOS-01)"))
    return issues

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 validate_framework_md.py <file.md> [file2.md ...]')
        sys.exit(1)
    all_texts = {}
    file_list = [p for p in sys.argv[1:] if os.path.isfile(p)]
    for p in file_list:
        all_texts[os.path.basename(p)] = open(p, encoding='utf-8').read()
    n = len(all_texts)
    total = 0
    for p in file_list:
        total += validate(p, all_texts if n >= 2 else None)
    if n >= 2:
        t_issues = check_t_cross_file_contract(all_texts)
        print(f'\n{"="*60}')
        print(f'BATCH CHECK T: CROSS-FILE TOKEN CONTRACT ({n} files)')
        print('-'*60)
        if t_issues:
            for fname, msg in t_issues:
                print(f'  [T-CONTRACT] {fname}: {msg}')
            total += len(t_issues)
            print('-'*60)
            print(f'RESULT: ❌ {len(t_issues)} cross-file contract issue(s) found.')
        else:
            print('RESULT: ✅ 0 ISSUES — all cross-file literal-token contracts verified.')

        u_issues = check_u_json_field_contract(all_texts)
        print(f'\n{"="*60}')
        print(f'BATCH CHECK U: JSON PRODUCER/CONSUMER FIELD CONTRACT ({n} files)')
        print('-'*60)
        if u_issues:
            for fname, msg in u_issues:
                print(f'  [U-JSONFIELD] {fname}: {msg}')
            total += len(u_issues)
            print('-'*60)
            print(f'RESULT: ❌ {len(u_issues)} JSON field contract issue(s) found.')
        else:
            print('RESULT: ✅ 0 ISSUES — all bare-indexed JSON field reads are documented.')
        for _code, _label, _tag, _fn, _clean in (
            ('AF', 'DELIVERABLE FILENAME CONTRACT', 'AF-FILENAME',
             check_af_deliverable_filename_contract,
             'every watched glob pattern matches a declared deliverable.'),
            ('AG', 'SHARED ARTEFACT READERS', 'AG-READER',
             check_ag_shared_artefact_readers,
             'no spec hand-parses an artefact an engine owns a reader for.'),
        ):
            _iss = _fn(all_texts)
            print(f'\n{"="*60}')
            print(f'BATCH CHECK {_code}: {_label} ({n} files)')
            print('-'*60)
            if _iss:
                for fname, msg in _iss:
                    print(f'  [{_tag}] {fname}: {msg}')
                total += len(_iss)
                print('-'*60)
                print(f'RESULT: ❌ {len(_iss)} issue(s) found.')
            else:
                print(f'RESULT: ✅ 0 ISSUES — {_clean}')
    # ── AA / AB — corpus-level, run whenever the engines/routes sit beside the specs.
    # Both are directory-scoped rather than file-scoped: they check artefacts that are
    # not .md files at all, and that no single spec owns.
    _dirs = []
    for _p in file_list:
        _d = os.path.dirname(os.path.abspath(_p))
        if _d not in _dirs:
            _dirs.append(_d)
    for _d in _dirs:
        aa_issues = check_aa_routes_skill_sync(_d)
        ab_issues = check_ab_thin_core_purity(_d)
        if os.path.exists(os.path.join(_d, 'routes.json')):
            print(f'\n{"="*60}')
            print(f'CORPUS CHECK AA: ROUTES <-> SKILL SYNC ({os.path.basename(_d) or _d})')
            print('-'*60)
            if aa_issues:
                for who, msg in aa_issues:
                    print(f'  [AA-ROUTESYNC] {who}: {msg}')
                total += len(aa_issues)
                print('-'*60)
                print(f'RESULT: ❌ {len(aa_issues)} routing/skill sync issue(s) found.')
            else:
                print('RESULT: ✅ 0 ISSUES — routes.json and SKILL.md agree both ways.')
        if any(os.path.exists(os.path.join(_d, m)) for m in _AB_MODULES):
            print(f'\n{"="*60}')
            print(f'CORPUS CHECK AB: THIN-CORE PURITY ({", ".join(_AB_MODULES)})')
            print('-'*60)
            if ab_issues:
                for who, msg in ab_issues:
                    print(f'  [AB-THINCORE] {who}: {msg}')
                total += len(ab_issues)
                print('-'*60)
                print(f'RESULT: ❌ {len(ab_issues)} purity violation(s) found.')
            else:
                print('RESULT: ✅ 0 ISSUES — thin core imports only the standard library '
                      'and performs no file I/O.')

        _py = glob.glob(os.path.join(_d, '*.py'))
        if _py:
            for _code, _label, _fn, _clean in (
                ('AC', 'AGGREGATOR SINGLE-EXIT',
                 check_ac_aggregator_single_exit,
                 'every aggregator has a single exit.'),
                ('AD', 'EMITTED FINDING-CLASS DOCUMENTED',
                 check_ad_emitted_class_documented,
                 'every emitted finding class is documented in a spec.'),
                ('AE', 'NORMALIZATION CONFORMANCE',
                 check_ae_normalization_conformance,
                 'all name comparisons go through normalize_label().'),
                ('AH', 'SPEC <-> ENGINE ROUTING',
                 check_ah_spec_engine_routing,
                 'every engine a spec imports is routed to its triggers.'),
                ('AI', 'ENGINE <-> ENGINE DEPENDENCY PARITY',
                 check_ai_engine_dependency_parity,
                 'every engine an engine imports is routed alongside it.'),
                ('AJ', 'UNDEFINED-NAME SCAN',
                 check_aj_undefined_names,
                 'no engine reads a name it never binds.'),
                ('AK', 'B3 DELIVERABLE CARDINALITY',
                 check_ak_b3_cardinality,
                 'every site describing the B3 delivery states the same count.'),
                ('AL', 'STEP-7 DELIVERY-SET CONTRACT',
                 check_al_delivery_set,
                 'the delivery set is DERIVED, and every site agrees on it.'),
            ):
                _iss = _fn(_d)
                print(f'\n{"="*60}')
                print(f'CORPUS CHECK {_code}: {_label} ({len(_py)} .py file(s))')
                print('-'*60)
                if _iss:
                    for who, msg in _iss:
                        print(f'  [{_code}] {who}: {msg}')
                    total += len(_iss)
                    print('-'*60)
                    print(f'RESULT: ❌ {len(_iss)} issue(s) found.')
                else:
                    print(f'RESULT: ✅ 0 ISSUES — {_clean}')

    print(f'\n{"="*60}')
    if total == 0:
        print(f'GRAND TOTAL: ✅ ALL FILES CLEAN — 0 issues across {n} file(s)')
    else:
        print(f'GRAND TOTAL: ❌ {total} issue(s) across {n} file(s)')
    sys.exit(1 if total else 0)
