#!/usr/bin/env python3
"""
audit_specs_ext.py — SUPPLEMENTARY deep auditor for the framework spec corpus.

This does NOT replace validate_framework_md.py (Checks A-U). It adds five check
families targeting bug classes that A-U cannot structurally reach — each one
derived from a real defect that reached a delivered spec:

  V-SYNC     Cross-file sync-rule parity. When a spec declares a CROSS-FILE SYNC
             RULE binding an artifact (function / regex) to a copy in another
             file, verify the copies are byte-identical NOW. A sync rule that is
             only prose is a promise; this makes it enforceable.
             (Motivating risk: E-9/E-10 in MockTestAnalyse vs blueprint_core
             Cluster E; DATE_TAG_RE in PYQFormat §4 vs PYQDeliver §4A.)

  W-DECISION Decision-ID (D1..Dn) integrity: defined exactly once, every
             reference resolves, superseding is declared on both ends, and no
             live section cites a SUPERSEDED decision as authoritative.
             (Motivating defect class: D4 hardcode superseded by D11.)

  X-NUMBER   Numbered-list contiguity inside a section (edge cases, tiers,
             inputs): 1..N with no gaps, no duplicates, no restarts.
             (Motivating defect class: appended edge cases silently colliding.)

  Y-CONFIG   Config-field declaration contract: any exam_config field READ in a
             spec must be DECLARED in that spec's input contract.
             (Motivating defect: PYQDeliver v1.2 read exam_config.marks_default
             but declared it nowhere — found only by manual line audit.)

  Z-VERSION  Full 3-part semantic version comparison. validate_framework_md.py
             captures v(\\d+\\.\\d+) only, so a patch component is TRUNCATED:
             a header/changelog disagreement in the third component (v2.24.9 vs
             v2.24.10) is invisible to Check C. This closes that blind spot.

Exit code 0 iff zero issues. Pure stdlib.
"""

import re
import sys
import os
from collections import Counter, defaultdict

ISSUES = []


def add(check, path, msg):
    ISSUES.append((check, os.path.basename(path), msg))


# ─────────────────────────────────────────────────────────────────────────────
# V-SYNC — cross-file sync-rule parity
# ─────────────────────────────────────────────────────────────────────────────
def _extract_named_defs(text):
    """{func_name: body} for every top-level `def` in any python fence or raw .py."""
    out = {}
    # raw python file OR fenced blocks — normalise to a list of code strings
    blocks = re.findall(r'```python\n(.*?)\n```', text, re.S)
    if not blocks:
        blocks = [text]
    for b in blocks:
        for m in re.finditer(r'^(def (\w+)\(.*?)(?=^\S|\Z)', b, re.S | re.M):
            out.setdefault(m.group(2), m.group(1).rstrip())
    return out


def _extract_named_assigns(text):
    """{CONST_NAME: rhs} for module-level `NAME = re.compile(...)`-style assigns."""
    out = {}
    blocks = re.findall(r'```python\n(.*?)\n```', text, re.S) or [text]
    for b in blocks:
        for m in re.finditer(r'^([A-Z][A-Z0-9_]+)\s*=\s*(re\.compile\(.*?\)|.+?)$',
                             b, re.S | re.M):
            name = m.group(1)
            if name in out:
                continue
            # for re.compile, capture through the balanced closing paren
            if m.group(2).startswith('re.compile('):
                seg = b[m.start(2):]
                depth, end = 0, None
                for i, ch in enumerate(seg):
                    if ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                if end:
                    out[name] = seg[:end]
            else:
                out[name] = m.group(2).strip()
    return out


def check_v_sync(texts):
    """texts: {path: content}. Find sync-rule declarations and verify parity."""
    # A sync rule names peer files. Collect (declaring_file, peer_basename, artifacts)
    for path, text in texts.items():
        # BIDIRECTIONAL window. A sync rule's peer filename is frequently named in
        # the sentence BEFORE the marker ("This section MIRRORS Framework_X.md §4.
        # CROSS-FILE SYNC RULE: any change to DATE_TAG_RE..."). A forward-only
        # window silently found no peer and compared nothing — the check passed
        # while covering nothing. Verified by targeted mutation: a DATE_TAG_RE
        # drift went UNDETECTED before this fix.
        for m in re.finditer(r'CROSS-FILE SYNC RULE', text):
            span = text[max(0, m.start() - 500): m.end() + 600]
            peers = set(re.findall(r'\b([A-Za-z_]+\w*\.(?:md|py))\b', span))
            arts = set(re.findall(r'`(\w+)`', span)) | set(re.findall(r'\b([A-Z][A-Z0-9_]{3,})\b', span))
            arts = {a for a in arts if a not in {'RULE', 'MUST', 'SAME', 'STEP', 'NOT'}}
            for peer in peers:
                ppath = next((p for p in texts if os.path.basename(p) == peer), None)
                if ppath is None:
                    continue  # peer not in this batch — reported by V-SCOPE below
                mine_d, mine_a = _extract_named_defs(text), _extract_named_assigns(text)
                pd, pa = _extract_named_defs(texts[ppath]), _extract_named_assigns(texts[ppath])
                for art in sorted(arts):
                    a_here = mine_d.get(art, mine_a.get(art))
                    a_peer = pd.get(art, pa.get(art))
                    if a_here is None or a_peer is None:
                        continue  # artifact not present in both — not a parity claim
                    if a_here.strip() != a_peer.strip():
                        add('V-SYNC', path,
                            f'{art} DIVERGED from copy in {peer} '
                            f'(sync rule declared but bodies differ)')


def check_v_scope(texts, all_known):
    """Sync rule naming a peer that was not supplied to this run → coverage warning."""
    for path, text in texts.items():
        for m in re.finditer(r'CROSS-FILE SYNC RULE(.{0,600})', text, re.S):
            for peer in set(re.findall(r'\b([A-Za-z_]+\w*\.(?:md|py))\b', m.group(1))):
                if peer not in all_known:
                    add('V-SCOPE', path,
                        f'sync rule references {peer} which was not audited in this run '
                        f'(parity UNVERIFIED — pass it too)')


# ─────────────────────────────────────────────────────────────────────────────
# W-DECISION — decision-ID integrity
# ─────────────────────────────────────────────────────────────────────────────
def check_w_decision(path, text):
    defs = re.findall(r'^#\s+(D\d+)\.\s', text, re.M)
    dupes = [d for d, c in Counter(defs).items() if c > 1]
    for d in sorted(dupes):
        add('W-DECISION', path, f'{d} defined {Counter(defs)[d]} times')
    defined = set(defs)
    if not defined:
        return
    refs = set(re.findall(r'\((D\d+)[\),]', text)) | set(re.findall(r'\bper (D\d+)\b', text))
    refs |= set(re.findall(r'\b(D\d+)/D\d+\b', text)) | set(re.findall(r'\bD\d+/(D\d+)\b', text))
    for r in sorted(refs - defined):
        add('W-DECISION', path, f'reference to {r} but no {r} definition')
    # superseding must be declared on BOTH ends
    for m in re.finditer(r'^#\s+(D\d+)\.\s*\[SUPERSEDED BY (D\d+)', text, re.M):
        old, new = m.group(1), m.group(2)
        if new not in defined:
            add('W-DECISION', path, f'{old} says superseded by {new}, but {new} is not defined')
        else:
            blk = re.search(rf'^#\s+{new}\..*?(?=^#\s+D\d+\.|\Z)', text, re.M | re.S)
            if blk and 'supersede' not in blk.group(0).lower():
                add('W-DECISION', path,
                    f'{old} declares supersession by {new}, but {new} does not '
                    f'declare it supersedes {old} (one-sided)')


# ─────────────────────────────────────────────────────────────────────────────
# X-NUMBER — numbered-list contiguity within a section
# ─────────────────────────────────────────────────────────────────────────────
def check_x_number(path, text):
    # Split on top-level section headers, then check bolded numbered lists.
    parts = re.split(r'^# (§[\w-]+.*)$', text, flags=re.M)
    for i in range(1, len(parts), 2):
        header, body = parts[i].strip(), parts[i + 1]
        nums = [int(n) for n in re.findall(r'^(\d+)\.\s+\*\*', body, re.M)]
        if len(nums) < 3:
            continue
        exp = list(range(1, len(nums) + 1))
        if nums != exp:
            dup = [n for n, c in Counter(nums).items() if c > 1]
            gaps = sorted(set(exp) - set(nums))
            detail = []
            if dup:
                detail.append(f'duplicates {dup}')
            if gaps:
                detail.append(f'missing {gaps}')
            if not detail:
                detail.append(f'out of order: {nums}')
            add('X-NUMBER', path, f'{header[:40]}: numbered list not 1..{len(nums)} — ' +
                '; '.join(detail))


# ─────────────────────────────────────────────────────────────────────────────
# Y-CONFIG — config field read but not declared in the input contract
# ─────────────────────────────────────────────────────────────────────────────
CONFIG_NOISE = {'json', 'get', 'items', 'keys', 'values'}


def check_y_config(path, text):
    # Only real attribute reads. `exam_config.json <word>` is PROSE (a filename
    # followed by a sentence), never a field read — excluded via negative
    # lookahead, otherwise "exam_config.json missing" yields a phantom field.
    reads = set(re.findall(r'exam_config\.(?!json\b)(\w+)', text))
    reads |= set(re.findall(r"exam_config\.get\(['\"](\w+)['\"]", text))
    reads -= CONFIG_NOISE
    if not reads:
        return
    # APPLICABILITY GATE. This check is only meaningful for specs that use the
    # "§0 input contract" convention. Corpus-verified: Blueprint, ScopedBlueprint,
    # PYQSort, PYQPrepare, PYQAnalyse and MockTestAnalyse declare their inputs
    # under other headings (S1-3 "Load inputs", S2-1 "Reading exam structure",
    # header comment blocks). Running the check on those produced 31 false
    # positives and ZERO true findings. Skip rather than cry wolf — a checker
    # that reports noise trains its operator to ignore it.
    if not re.search(r'^# §0\b', text, re.M):
        return
    # A `.get('field', default)` inside a python fence is self-declaring: the
    # default IS the contract. Only prose/pseudo-code reads need a §0 entry.
    for blk in re.findall(r'```python\n(.*?)\n```', text, re.S):
        for f in re.findall(r"exam_config\.get\(['\"](\w+)['\"]\s*,", blk):
            reads.discard(f)
    # Declaration zone = the input contract (§0) plus explicit declaration lines
    # ONLY. Deliberately EXCLUDES generic words like "declared", which match
    # changelog prose ("...was read but declared nowhere") and would mask the
    # very defect this check exists to find (verified: that false-negative was
    # real before this narrowing).
    zone = ''
    m = re.search(r'^# §0.*?(?=^# §1\b)', text, re.M | re.S)
    if m:
        zone = m.group(0)
    zone += '\n'.join(l for l in text.splitlines()
                      if re.search(r'Provides|OPTIONAL field', l))
    for f in sorted(reads):
        if not re.search(rf'`?{re.escape(f)}`?', zone):
            add('Y-CONFIG', path,
                f'exam_config.{f} is READ but never declared in the input contract (§0)')


# ─────────────────────────────────────────────────────────────────────────────
# Z-VERSION — full 3-part version comparison (Check C truncates to 2)
# ─────────────────────────────────────────────────────────────────────────────
def _vt(v):
    return tuple(int(x) for x in v.split('.'))


def check_z_version(path, text):
    lines = text.splitlines()
    if not lines:
        return
    m = re.match(r'^#?\s*\S+\s+v(\d+(?:\.\d+)+)', lines[0])
    if not m:
        return
    header = m.group(1)
    entries = []
    for l in lines:
        mm = re.match(r'^[#*\s]*v(\d+(?:\.\d+)+)\s*(?:[—–-]\s*\d{4}|changes:)', l.strip())
        if mm:
            entries.append(mm.group(1))
    if entries:
        top = max(entries, key=_vt)
        if _vt(top) != _vt(header):
            add('Z-VERSION', path,
                f'header v{header} != highest changelog entry v{top} '
                f'(FULL 3-part compare — Check C truncates and misses this)')
        if len(set(entries)) != len(entries):
            dup = [v for v, c in Counter(entries).items() if c > 1]
            add('Z-VERSION', path, f'duplicate changelog entries for {dup}')
    for m2 in re.finditer(r'\*\*End of \S+ \(v(\d+(?:\.\d+)+)\)\*\*', text):
        if _vt(m2.group(1)) != _vt(header):
            add('Z-VERSION', path,
                f'end sentinel v{m2.group(1)} != header v{header}')


# ─────────────────────────────────────────────────────────────────────────────
def main(paths):
    texts = {}
    for p in paths:
        try:
            texts[p] = open(p, encoding='utf-8').read()
        except Exception as e:
            add('READ', p, f'cannot read: {e}')
    known = {os.path.basename(p) for p in texts}

    for p, t in texts.items():
        check_w_decision(p, t)
        check_x_number(p, t)
        check_y_config(p, t)
        check_z_version(p, t)
    check_v_sync(texts)
    check_v_scope(texts, known)

    if not ISSUES:
        print(f"✅ audit_specs_ext: 0 issues across {len(texts)} file(s) "
              f"[V-SYNC W-DECISION X-NUMBER Y-CONFIG Z-VERSION]")
        return 0
    by_file = defaultdict(list)
    for chk, f, msg in ISSUES:
        by_file[f].append((chk, msg))
    for f in sorted(by_file):
        print(f"\n{f}")
        for chk, msg in sorted(by_file[f]):
            print(f"  [{chk}] {msg}")
    print(f"\n❌ audit_specs_ext: {len(ISSUES)} issue(s) across {len(by_file)} file(s)")
    return 1


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args))
