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
             EXEMPTION (2026-07-29): a DELEGATION ADAPTER — a copy whose whole
             body calls or aliases the canonical copy — is skipped: its parity
             holds by construction, and byte-comparing it false-fires.
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
import json
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


def _is_delegation_adapter(body, art):
    """True when this copy's entire job is to CALL the canonical copy.

    2026-07-29 (follow-up recorded 2026.07.26.2): after GAP-2026-07-25-002 and
    GAP-2026-07-26-002 the spec-side copies of shared functions became thin
    adapters — `return bc.score_difficulty(...)`, `is_option = corpus_io.is_option`.
    Their bodies legitimately DIFFER from the engine's canonical body: parity is
    satisfied BY CONSTRUCTION (there is only one implementation to diverge from),
    not by byte identity. Comparing bytes here false-fired on every adapter
    (measured: determine_strip_mode + score_difficulty in MockTestAnalyse).
    An adapter is recognised and skipped, never byte-compared.
    """
    if not body:
        return False
    pat_call = r'\breturn\s+[A-Za-z_][\w.]*\.' + re.escape(art) + r'\s*\('
    pat_alias = r'^\s*' + re.escape(art) + r'\s*=\s*[A-Za-z_][\w.]*\.' + re.escape(art) + r'\s*$'
    return bool(re.search(pat_call, body) or re.search(pat_alias, body, re.M))


# Policy threshold (owner decision D1). Set where the corpus actually splits: every
# PYQ-phase trigger is far below it; PYQExtract (556,834 B), MockCreate (~563,000) and
# MockBlueprint (~420,000) are above it, and all three are batched multi-session steps.
SPEC_BUDGET_BYTES = 250_000

# RATCHET BASELINE — the same idiom as spec_name_audit_baseline.json. These routes are
# already over the threshold at 2026.08.15.9 and are KNOWN, SCOPED and DEFERRED: the
# read-set work for them is the next wave, and failing the build for them today would
# block a release that fixes the step actually on fire. What the ratchet guarantees is
# that NO NEW route may cross the threshold unnoticed, and that a route which has a
# read set can never lose it — both of those still fail the build.
#
# THE ONLY LEGITIMATE EDIT TO THIS LIST IS A DELETION. Adding a name to silence a new
# finding is the move this baseline exists to make visible, not to enable.
#   MockCreate / TestCreate  — Framework_MockTestCreate.md, 8,089 lines / 510,969 B,
#                              batched and multi-session: G-1 and G-4 apply unchanged.
#   MockBlueprint            — Framework_Blueprint.md, 6,901 lines / 367,480 B.
#   PYQPrepare/PYQScan/PYQCount — step file + Framework_PYQCore.md (now 1,993 lines
#                              after EC-P40..EC-P43) + Framework_DeliveryFooter.md.
#                              Single-session steps, so the cost is paid once per run
#                              rather than once per paper; lower priority, still real.
SPEC_BUDGET_BASELINE = {
    'MockBlueprint', 'MockCreate', 'TestCreate',
}
# RATCHETED DOWN at 2026.08.15.14 — the first deletions since the baseline was
# created. PYQCount (253,145 -> 237,140 B), PYQPrepare (258,251 -> 242,871) and
# PYQScan (260,072 -> 246,819) fell below SPEC_BUDGET_BYTES when the superseded
# changelog entries moved to SPEC_HISTORY.md, so they no longer need an exemption
# and now fail the build if they ever cross back. This is the mechanism working as
# designed: a debt paid down, not an allowance widened.


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
                    if _is_delegation_adapter(a_here, art) or _is_delegation_adapter(a_peer, art):
                        continue  # delegation adapter — parity by construction, not by bytes
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
def check_spec_budget(paths):
    """SPEC-BUDGET — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / G-1, EC-P42.

    For every trigger in routes.json, report the summed byte cost of the .md files a
    session must read before it may do anything, and FAIL when a route exceeds the
    threshold with no read-set declared in SPEC_SECTIONS.json.

    This is the check that did not exist. bootstrap.py printed filenames; MANIFEST.json
    carried the line count for INTEGRITY and never surfaced it as a COST; no EC, no DoD
    item and no gate mentioned read cost at all. Measured on PYQExtract: 556,834 B,
    ~139,208 tokens, >=36 view calls, MANDATORY, every session, on the one step that is
    inherently multi-session — 40 of 50 tool calls in the reference incident.

    The threshold is a POLICY number, not a law of nature. It is set where the corpus
    actually splits: every PYQ-phase trigger sits far below it; PYQExtract, MockCreate
    and MockBlueprint sit above it and are all batched, multi-session steps. Raising it
    to silence a finding is the wrong move and is why the reason is recorded here.
    """
    root = os.path.dirname(os.path.abspath(paths[0])) if paths else '.'
    rp = os.path.join(root, 'routes.json')
    sp = os.path.join(root, 'SPEC_SECTIONS.json')
    if not os.path.exists(rp):
        return
    routes = {k: v for k, v in json.load(open(rp, encoding='utf-8')).items()
              if not k.startswith('_')}
    sections = (json.load(open(sp, encoding='utf-8')).get('files', {})
                if os.path.exists(sp) else {})
    for trig, entry in sorted(routes.items()):
        mds = [f for f in entry if f.endswith('.md')]
        total = 0
        for f in mds:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
        if total <= SPEC_BUDGET_BYTES:
            continue
        covered = any(sections.get(f, {}).get('has_read_set') for f in mds)
        if not covered and trig not in SPEC_BUDGET_BASELINE:
            add('SPEC-BUDGET', f'routes.json[{trig}]',
                f'pre-work read is {total:,} B (~{total // 4:,} tok) across {len(mds)} '
                f'spec(s), above the {SPEC_BUDGET_BYTES:,} B threshold, and NO read set '
                f'is declared in SPEC_SECTIONS.json. A session must pay this before it '
                f'may do any work (EC-P42). Declare a FINAL/NON-FINAL read set for the '
                f'largest spec on this route, or move its executable fences into a '
                f'routed engine.')


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
    check_spec_budget(paths)

    if not ISSUES:
        print(f"✅ audit_specs_ext: 0 issues across {len(texts)} file(s) "
              f"[V-SYNC W-DECISION X-NUMBER Y-CONFIG Z-VERSION SPEC-BUDGET]")
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


def self_test():
    """GAP-2026-08-14-AUDITOR-SELFTESTS. Synthetic single-file fixtures, one per
    check family, run through a SUBPROCESS (ISSUES is module state; a fresh
    interpreter per fixture keeps every verdict independent)."""
    import subprocess, tempfile
    passed, fails = 0, []
    here = os.path.abspath(__file__)

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def probe(fname, content):
        d = tempfile.mkdtemp()
        p = os.path.join(d, fname)
        open(p, 'w', encoding='utf-8').write(content)
        r = subprocess.run([sys.executable, here, p],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    rc, out = probe("Framework_C.md",
        "# Framework_C v1.0.0 — t\n# v1.0.0 — 2026-01-01 — x\n"
        "# §1 — WORK\nplain body\n# END OF Framework_C v1.0.0\n")
    check("clean fixture passes", rc == 0 and '0 issues' in out)

    rc, out = probe("Framework_Z.md",
        "# Framework_Z v1.0.0 — t\n# v1.0.1 — 2026-08-14 — newer entry\nbody\n")
    check("Z-VERSION fires on a 3-part header/changelog disagreement",
          rc == 1 and 'Z-VERSION' in out)

    rc, out = probe("Framework_W.md",
        "# Framework_W v1.0.0 — t\n# v1.0.0 — 2026-01-01 — x\n"
        "# D1. First decision.\nUse the cap (D9) here.\n")
    check("W-DECISION fires on a citation of an undefined decision",
          rc == 1 and 'W-DECISION' in out and 'D9' in out)

    rc, out = probe("Framework_X.md",
        "# Framework_X v1.0.0 — t\n# v1.0.0 — 2026-01-01 — x\n"
        "# §1 EDGE CASES\n1. **a** one\n2. **b** two\n4. **d** four\n")
    check("X-NUMBER fires on a gapped numbered list",
          rc == 1 and 'X-NUMBER' in out)

    rc, out = probe("Framework_Y.md",
        "# Framework_Y v1.0.0 — t\n# v1.0.0 — 2026-01-01 — x\n"
        "# §0 — INPUTS\nnothing declared\n# §1 — WORK\n"
        "Read exam_config.marks_default and apply it.\n")
    check("Y-CONFIG fires on a config read the input contract omits",
          rc == 1 and 'Y-CONFIG' in out and 'marks_default' in out)

    # ── SPEC-BUDGET — GAP-2026-08-16-STEP5-SESSION-EXHAUSTION ────────────────
    # Shipped in 2026.08.15.9 without a fixture. Gut check_spec_budget to `return []`
    # and the must-flag check below must FAIL. The gate needs routes.json in the same
    # directory as the spec, so the fixture builds a miniature repo.
    def probe_budget(spec_bytes, trigger='FixtureStep', sections=None,
                     baseline_hack=None):
        d = tempfile.mkdtemp()
        name = "Framework_Big.md"
        body = ("# Framework_Big v1.0.0 — t\n# v1.0.0 — 2026-01-01 — x\n"
                "# §1 — WORK\n" + ("x" * spec_bytes) + "\n"
                "# END OF Framework_Big v1.0.0\n")
        open(os.path.join(d, name), 'w', encoding='utf-8').write(body)
        json.dump({trigger: [name]},
                  open(os.path.join(d, 'routes.json'), 'w', encoding='utf-8'))
        if sections is not None:
            json.dump({'files': {name: {'has_read_set': sections}}},
                      open(os.path.join(d, 'SPEC_SECTIONS.json'), 'w', encoding='utf-8'))
        r = subprocess.run([sys.executable, here, os.path.join(d, name)],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    rc, out = probe_budget(SPEC_BUDGET_BYTES + 5000)
    check("SPEC-BUDGET fires on an over-threshold route with no read set",
          rc == 1 and '[SPEC-BUDGET]' in out)

    rc, out = probe_budget(SPEC_BUDGET_BYTES + 5000, sections=True)
    check("SPEC-BUDGET silent once the route declares a read set",
          '[SPEC-BUDGET]' not in out)

    rc, out = probe_budget(1000)
    check("SPEC-BUDGET silent on a small route",
          '[SPEC-BUDGET]' not in out)

    # The ratchet must only ever be a DELETION list. A baselined trigger is exempt;
    # a NEW trigger crossing the threshold is not, which is the whole guarantee.
    rc, out = probe_budget(SPEC_BUDGET_BYTES + 5000, trigger='MockCreate')
    check("SPEC-BUDGET exempts a baselined trigger",
          '[SPEC-BUDGET]' not in out)
    rc, out = probe_budget(SPEC_BUDGET_BYTES + 5000, trigger='BrandNewStep')
    check("SPEC-BUDGET still fires for a trigger absent from the baseline",
          rc == 1 and '[SPEC-BUDGET]' in out)

    # The live corpus itself must pass with the standard invocation
    # (specs + engines together, per the V-SCOPE contract).
    root = os.path.dirname(here) or '.'
    corpus = sorted(
        os.path.join(root, f) for f in os.listdir(root)
        if (f.startswith('Framework_') and f.endswith('.md')) or f.endswith('.py'))
    r = subprocess.run([sys.executable, here] + corpus,
                       capture_output=True, text=True)
    check("live corpus passes the standard md+py invocation",
          r.returncode == 0 and '0 issues' in r.stdout)

    print(f"audit_specs_ext self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args))
