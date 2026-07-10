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
  D. GATE COUNT DRIFT — all live gate-count totals agree (no hardcoded number)
  E. STEP NUMBER VALIDATION — Step N (Name) patterns vs the canonical pipeline
  F. VARIABLE REFERENCES — known dangerous patterns in code blocks
  G. CHECKLIST COUNT — "All N items" matches actual [ ] count in that section
  H. CROSS-REFERENCES — §N references resolve to defined section headers
  I. STALE MARKERS — TODO / FIXME / PLACEHOLDER / TBD
  J. SELF-TEST COUNT — prose "N/N PASS" matches actual unique check() names
  K. DUPLICATE SECTIONS — no §N or sub-section defined twice

  ═══ AUTO-DETECTED EXTENDED (run when patterns found) ═══
  M. GATE-CODE EMISSION — embedded script emitted codes vs documented A-* codes
  N. RA-RULE ANCHORS — every RA-N reference resolves to a definition
  O. MANDATE ANCHORS — every MANDATE X reference resolves to a definition
  P. CONSTANT CONSISTENCY — AUDIT_BATCH_SIZE, RUN_MAX values agree
  Q. DYNAMIC EXECUTION — extract + run the largest embedded script --self-test
  R. RA/SUB-SECTION DUPLICATES — RA-N and S/P sub-anchors not defined twice
  S. COMPLETION-GATE (v2.6) — S5-1A wiring + C1-C7 regression fixtures present

Usage:
  python3 validate_framework_md.py <file.md>
  python3 validate_framework_md.py /mnt/project/*.md   (batch mode)
"""
import re, ast, sys, os
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════
# CANONICAL PIPELINE — the single source of truth for step numbers
# ═══════════════════════════════════════════════════════════════════════
PIPELINE = {
    'PYQPrepare': '1', 'PYQDraft': '2a', 'PYQScan': '2b', 'PYQApprove': '2c',
    'PYQSort': '3', 'PYQCount': '4', 'PYQExtract': '5',
    'MockTestAnalyse': '5', 'MockBlueprint': '6', 'Blueprint': '6',
    'MockCreate': '7', 'MockCreateAudit': '8',
    'MockExplain': '9', 'MockExplainAudit': '10', 'MockDeliver': '11',
}

def validate(path):
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
    for l in lines:
        s = l.strip()
        # Accept BOTH changelog styles used across the framework specs:
        #   "vX.Y — 2026-07-07 — …"   (dated list entry)
        #   "vX.Y changes: …"          (top-of-file per-version summary)
        m = re.match(r'^[#*\s]*v(\d+\.\d+)\s*[—–-]\s*\d{4}', s) or \
            re.match(r'^[#*\s]*v(\d+\.\d+)\s+changes:', s)
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
    for kw in ('TODO', 'FIXME', 'PLACEHOLDER', 'TBD'):
        for i, l in enumerate(lines, 1):
            if re.search(rf'\b{kw}\b', l) and not l.strip().startswith('#') and not l.strip().startswith('*'):
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
        def_ra = set(re.findall(r'^\s{0,4}RA-(\d+)[a-z]?\s', text, re.M)) | set(GLOBAL_RA)
        ref_ra = set(re.findall(r'\bRA-(\d+)\b', text))
        for r in sorted(int(x) for x in (ref_ra - def_ra)):
            add('N-RA', f'reference to RA-{r} but no RA-{r} definition')
        for k, v in Counter(re.findall(r'^\s{0,4}(RA-\d+[a-z]?)\s', text, re.M)).items():
            if v > 1: add('N-RA', f'{k} defined {v} times')

    # ─────────────────── O: MANDATE ANCHORS ──────────────────────
    if has_mandates:
        extended_ran.append('O-MANDATE')
        # MANDATE definitions: "# MANDATE X —" where X is 0-9 or a single uppercase letter
        def_mand = set(re.findall(r'^#\s*MANDATE\s+([0-9A-Z])\b', text, re.M)) | set(GLOBAL_MANDATE)
        # References: "MANDATE X" where X is 0-9 or a single uppercase letter (not full words)
        ref_mand = set(re.findall(r'\bMANDATE\s+([0-9A-Z])\b', text))
        for m in sorted(ref_mand - def_mand):
            add('O-MANDATE', f'reference to MANDATE {m} but no MANDATE {m} definition')

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

GLOBAL_MANDATE, GLOBAL_RA = set(), set()

def _prescan(paths):
    """Corpus-wide anchor gather so a reference in file A to an anchor DEFINED
    in file B (batch runs) is not flagged as a missing definition."""
    gm, gr = set(), set()
    for p in paths:
        if not os.path.isfile(p): continue
        t = open(p, encoding='utf-8').read()
        gm |= set(re.findall(r'^#\s*MANDATE\s+([0-9A-Z])\b', t, re.M))
        gr |= set(re.findall(r'^\s{0,4}RA-(\d+)[a-z]?\s', t, re.M))
    return gm, gr

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 validate_framework_md.py <file.md> [file2.md ...]')
        sys.exit(1)
    GLOBAL_MANDATE, GLOBAL_RA = _prescan(sys.argv[1:])
    total = 0
    for p in sys.argv[1:]:
        if os.path.isfile(p): total += validate(p)
    print(f'\n{"="*60}')
    n = len([p for p in sys.argv[1:] if os.path.isfile(p)])
    if total == 0:
        print(f'GRAND TOTAL: ✅ ALL FILES CLEAN — 0 issues across {n} file(s)')
    else:
        print(f'GRAND TOTAL: ❌ {total} issue(s) across {n} file(s)')
    sys.exit(1 if total else 0)
