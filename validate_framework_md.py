#!/usr/bin/env python3
"""
validate_framework_md.py — Universal Framework .md Validator
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

Usage:
  python3 validate_framework_md.py <file.md>
  python3 validate_framework_md.py /mnt/project/*.md   (batch mode — enables Check T)
"""
import re, ast, sys, os
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════
# CANONICAL PIPELINE — the single source of truth for step numbers
# ═══════════════════════════════════════════════════════════════════════
PIPELINE = {
    'PYQPrepare': '1', 'PYQDraft': '2a', 'PYQScan': '2b', 'PYQApprove': '2c',
    'PYQSort': '3', 'PYQCount': '4', 'PYQExtract': '5',
    'MockTestAnalyse': '5', 'MockBlueprint': '6', 'Blueprint': '6', 'ScopedBlueprint': '6S',
    'MockCreate': '7', 'MockCreateAudit': '8',
    'MockExplain': '9', 'MockExplainAudit': '10', 'MockDeliver': '11',
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
    header_ver = None
    m = re.match(r'^#?\s*\S+\s+v(\d+\.\d+)', lines[0])
    if not m:  # try "Version: vX.Y" format
        for l in lines[:15]:
            m2 = re.match(r'^Version:\s*v?(\d+\.\d+)', l)
            if m2: header_ver = m2.group(1); break
    else:
        header_ver = m.group(1)

    footer_ver = None
    for l in reversed(lines):
        m = re.search(r'END OF \S+ v(\d+\.\d+)', l)
        if m: footer_ver = m.group(1); break
        m = re.search(r'^#\s*Version:\s*(\d+\.\d+)', l)
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
        m = re.match(r'^[#*\s]*v(\d+\.\d+)\s*(?:[—–-]\s*\d{4}|changes:)', l.strip())
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
    def_sections = set(re.findall(r'^#+ §(\d+)\b', text, re.M))
    ref_sections = set(re.findall(r'§(\d+)\b', text))
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
    has_explain_gate = ('AUDIT-COMPLETION-GATE' in text) or ('explain_audit_gate' in text)
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
        print(f'  Extended checks: {", ".join(extended_ran)}')
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
    print(f'\n{"="*60}')
    if total == 0:
        print(f'GRAND TOTAL: ✅ ALL FILES CLEAN — 0 issues across {n} file(s)')
    else:
        print(f'GRAND TOTAL: ❌ {total} issue(s) across {n} file(s)')
    sys.exit(1 if total else 0)
