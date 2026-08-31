#!/usr/bin/env python3
# audit_seam.py v1.3 — 2026-08-28 — EXPLAIN-HALF + PROSE-READ WIDENING
#   (GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ). Five section_rules CATEGORY-C keys
#   were read by consumer specs and produced by NOTHING, and this auditor — built for
#   exactly that finding class — reported [OK] on a corpus it could not see, for TWO
#   independent reasons, both fixed here:
#     (a) WORLD MAP: Framework_MockTestExplain.md, Framework_PYQExplain.md and
#         explain_engine.py were in neither PRODUCERS nor CONSUMERS, so any field read
#         only by the Explain half of the pipeline was invisible. This is the v1.1
#         staleness lesson recurring with the worse artefact: a false clean instead of
#         a false finding. All three are now registered (explain_engine on BOTH sides,
#         the analyse_engine treatment, so its internal fields do not drown the run).
#     (b) READ IDIOM: reads() required Python syntax, but the Explain specs read
#         CATEGORY-C config in PROSE with a backtick-quoted key near an anchor phrase —
#         the correct idiom for spec-directed session work (§6A-6). A prose-read
#         pattern is added; the scope filter is widened so those keys can surface.
#   NOTE: the sibling gate validate_framework_md Check V covers the same class
#   self-scopingly (producer key set derived from write_section_rules' own body) —
#   ship both; each covers the other's staleness mode (LAW_REGISTRY
#   _derived_not_declared).
# audit_seam.py v1.2 — 2026-08-24 — KEY-SHAPE GATE (GAP-2026-08-24-AXIS-PAPER-SERIES-
#   COLLISION). Two releases in a row shipped the SAME defect in different fields:
#   options_by_q (v5.56) and axis1_paper/axis3_paper (v5.57) were both written as
#   reg['<field>'][str(N)] — the paper ORDINAL — onto a registry that ScopedBlueprint
#   §9 shares across series, so MOCK:M01 and SUBJ:PHYS:01 both landed on key '1' and
#   the later commit silently destroyed the earlier paper's data. Both were found by
#   hand (a dry-run harness, then a field-contract sweep); nothing in the corpus could
#   see the class. This gate closes it: every per-paper container in PER_PAPER must be
#   written under a paper_id key, and an ORDINAL-ONLY write FAILS the build. A third
#   instance now cannot ship. RULE: a per-paper container may ALSO carry the ordinal
#   key for the MOCK series (back-compat), but never ONLY the ordinal key.
# audit_seam.py v1.1 — 2026-08-14 — WORLD-MAP REFRESH (GAP-2026-08-14-AXISPAPER-
#   PERSISTENCE RESOLUTION). The 5 findings this auditor carried since the
#   2026.08.12.x wave were not broken data — they were THIS FILE's map of the
#   pipeline going stale while the pipeline grew:
#     (1) final_assembly.py (the Step-7 engine, released .12.11) WRITES
#         reg['axis1_paper']/reg['axis3_paper'] via setdefault and reads them
#         back — it was in neither PRODUCERS nor CONSUMERS, so its writes were
#         invisible and both fields reported ORPHAN-READ. It is now registered
#         on both sides as 'Step7-engine'.
#     (2) axis1_paper_counts / axis3_paper_counts are Step-7-INTERNAL
#         accumulator variables (initialised, subscript-filled and consumed
#         inside Framework_MockTestCreate §13-4 / S7-NEW-B) — local state,
#         never a cross-step contract. ALLOW-listed with that reason, exactly
#         like 'di_rate' (internal to Step 5).
#     (3) axis3_mechanism_lock is emitted by blueprint_core into the Step-7
#         report dict for AUDITABILITY (covered/gap counts, GAP-2026-08-12-
#         AXIS3-MECHLOCK); it is consumed by report prose, never by field
#         name. ALLOW-listed with that reason, exactly like
#         'figural_denominator'.
#   The lesson is the auditor's own: a checker whose world-model is not
#   updated alongside the world reports yesterday's architecture as today's
#   defect. CI now runs this file on every push (GAP-2026-08-14-CI-AUDITOR-
#   WIRING), so the next stale-map drift turns a build red instead of
#   waiting for a hand run.
# audit_seam.py v1.0 — 2026-08-06 — PRODUCER/CONSUMER SEAM AUDIT (GAP-2026-08-06-SEAM)
#
# WHY THIS EXISTS.
#   Every defect in the 2026.08.06.x series lived at a SEAM between steps, and not one
#   was caught by the existing tooling:
#     .1  Step 6 wrote axis1_target_per_mock; Step 7 never read it        -> 26 figures
#     .2  gates scored classes they had no evidence for                   -> false FAILs
#     .5  Step 7 forced figures from a flag instead of Step 6's frequency -> 14.3/mock
#     .6  Step 7 read a rotating series from a key load_sources never set -> inert
#     .7  Step 6 read total_mocks from a key Step 5 never writes          -> always 15
#     .8  Step 5 wrote di_rate; nothing consumed it                       -> DI unscheduled
#   The pattern is identical every time: ONE SIDE OF A CONTRACT CHANGED. Unit tests pass
#   because each side is individually correct. audit_callgraph catches an unreferenced
#   FUNCTION; nothing catches an unreferenced FIELD.
#
# WHAT IT CHECKS.
#   ORPHAN-WRITE : a step emits a field no downstream step or engine reads. Either dead
#                  weight or, worse, a feature someone believes is live.
#   ORPHAN-READ  : a step reads a field nothing upstream emits. Silently defaults —
#                  which is exactly how total_mocks became 15 for the whole estate.
#
#   Heuristic by nature: it reports CANDIDATES for a human to confirm, and carries an
#   explicit allow-list for fields that are legitimately one-sided (diagnostics awaiting
#   a consumer, compatibility shims). A finding here is a question, not a verdict.
#
#   WHAT IT DOES NOT CATCH — MEASURED, not assumed (release manager, 2026.08.06.8).
#   This tool was run against the historical trees that actually carried the defects
#   listed above. It reports NO finding for four of the six:
#     .1 axis1_target_per_mock @ e439bcb -> 'ok'      Step 6 writes AND reads it, and
#        blueprint_core is on both sides, so Step 7 dropping its read is invisible.
#     .6 axis1_target_series   @ effd50c -> 'ok'      the read exists textually; it was
#        unreachable because mock_n was never set. A regex cannot see reachability.
#     .7 total_mocks           @ 6299fd9 -> 'ok'      the defect was a NESTED read,
#        axis_dist["total_mocks"]; the flat field-name model cannot distinguish it.
#     .8 di_rate               @ 8b9ca85 -> 'allowed' it is on the ALLOW list above.
#   So an [OK] run means 'no field is entirely one-sided'. It does NOT mean the seam
#   class is covered, and it would not have caught the releases it cites as motivation.
#   Closing those needs per-consumer tracking, nested-key awareness and reachability —
#   none of which a token scan can provide.
#
# Pure stdlib. Exit 0 iff zero unexplained findings.

import re, sys, json, collections, os

PRODUCERS = {'Framework_MockTestAnalyse.md': 'Step5',
             'Framework_Blueprint.md': 'Step6',
             'blueprint_core.py': 'engine',
             # audit_canonical populates its own `src` dict and reads it back; without
             # it here every src key reads as an ORPHAN-READ and the real findings drown.
             'audit_canonical.py': 'audit',
             # v1.1: the Step-7 engine (released 2026.08.12.11) persists the
             # per-mock axis snapshots (reg['axis1_paper']/reg['axis3_paper']
             # via setdefault). Omitting it made both fields ORPHAN-READ.
             'final_assembly.py': 'Step7-engine',
             # WAVE 2 PART C (2026-08-17). Step 5's §2/§3/§4/§5/§6 implementation moved
             # out of Framework_MockTestAnalyse.md into analyse_engine.py, so every
             # field whose WRITER moved became invisible to this auditor and five
             # fields reported ORPHAN-READ: count_by_subtopic_by_class, di_reducible,
             # figural_rate, per_paper_mean_by_class, per_paper_observed_by_class.
             # Measured as PURE RELOCATION — occurrence counts identical before and
             # after, e.g. figural_rate 14 in the old spec, 14 in the engine, 0 left
             # behind. Same class release 2026.08.17.1 already fixed once for
             # audit_callgraph C4, and this auditor did not receive the same widening.
             'analyse_engine.py': 'Step5-engine',
             # corpus_io.figural_consistency() WRITES image_not_figural and
             # figural_no_image, which run_img5b reads. Both sides were previously
             # invisible — the write because corpus_io was unregistered, the read
             # because Framework_MockTestAnalyse.md is a PRODUCER here and never a
             # CONSUMER — so the field never appeared at all and the seam went
             # unchecked. Registering the engine surfaced the read; registering its
             # real writer is the honest completion, NOT an ALLOW entry, because
             # nothing about this pair is legitimately one-sided.
             'corpus_io.py': 'io-engine',
             # WAVE 2 PART C BATCH 9 (2026-08-20). Step 5's §S8-0 Drive transport block
             # moved out of Framework_MockTestAnalyse.md into transport_core.py, and its
             # _meta._transport writer (record_transport / log_session) moved with it.
             # Registering it here is the same completion analyse_engine.py needed after
             # batch 3: a field whose WRITER moves into an unregistered engine reads as
             # ORPHAN-READ, which is a finding about the auditor, not about the field.
             'transport_core.py': 'Step5-transport',
             # v1.3 — explain_engine populates its own dicts and reads them back;
             # registered on BOTH sides (the analyse_engine v1.1 treatment) so its
             # internal fields do not drown the run in false ORPHAN-READs.
             'explain_engine.py': 'Step9-engine'}
CONSUMERS = {'Framework_Blueprint.md': 'Step6',
             'Framework_MockTestCreate.md': 'Step7',
             'blueprint_core.py': 'engine',
             'audit_canonical.py': 'audit',
             'final_assembly.py': 'Step7-engine',
             'analyse_engine.py': 'Step5-engine',
             'transport_core.py': 'Step5-transport',
             # v1.3 — the Explain half of the pipeline (GAP-2026-08-28-CATEGORY-C-
             # ORPHAN-CONFIG-READ): any field read only here was invisible before.
             'Framework_MockTestExplain.md': 'Step9',
             'Framework_PYQExplain.md': 'PYQ-1',
             'explain_engine.py': 'Step9-engine'}

# Fields legitimately written by one side only. Each needs a REASON, so the list cannot
# quietly become a place to bury real findings.
ALLOW = {
    'figural_denominator': 'emitted for auditability of figural_rate; no consumer by design',
    'option_image_rate':   'emitted for auditability of figural_reducible; round-trips via the section_rules parser',
    'figural_q_count':     'read by the section_rules parser and by Step 6 via count_by_subtopic_by_class',
    'di_q_count':          'read by the section_rules parser; feeds the DI format rule inside Step 5',
    'image_role':          'per-question extractor field, not a cross-step contract',
    'figural_banned':      'legacy FIGURAL_BANNED escape hatch, still honoured by Step 7 prose',
    'di_rate':             'internal to Step 5: drives the DI format rule (has_tbl) in the same function',
    'figural_unkeyed_questions': 'superseded by unkeyed_questions_by_class (v2.46), kept for back-compat',
    'axis1_enforcement':   'read by gate_axis_ungated via endswith("_enforcement"), never by literal name',
    'axis3_enforcement':   'read by gate_axis_ungated via endswith("_enforcement"), never by literal name',
    'axis3':               'axis-distribution sub-dict, addressed structurally not by name',
    'figural_core':        'module name, not a data field',
    'figural_cue_keywords': 'figural_core internal, outside the Step5-7 seam',
    'figural_object_types': 'figural_core internal, outside the Step5-7 seam',
    'check_figural_conformance': 'engine FUNCTION name, not a data field',
    'figural_generation_profile': 'prose section heading, not a data field',
    'figural_data':        'function PARAMETER of synthesise_subtopic, not a cross-step field',
    # v1.1 (GAP-2026-08-14-AXISPAPER-PERSISTENCE resolution):
    'axis1_paper_counts':  'Step-7-INTERNAL accumulator variable (initialised, filled and '
                           'consumed inside MockTestCreate §13-4 / S7-NEW-B), not a '
                           'cross-step contract — same class as di_rate',
    'axis3_paper_counts':  'Step-7-INTERNAL accumulator variable (initialised, filled and '
                           'consumed inside MockTestCreate §13-4 / S7-NEW-B), not a '
                           'cross-step contract — same class as di_rate',
    'axis3_mechanism_lock': 'emitted by blueprint_core into the Step-7 report dict for '
                            'auditability (covered/gap counts, GAP-2026-08-12-AXIS3-'
                            'MECHLOCK); consumed by report prose, never by field name — '
                            'same class as figural_denominator',
    # v1.3 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ §6.4, operator decision D2
    # (2026-08-28): both latent CATEGORY-C soft reads are CORRECT as they stand.
    'paper_header_block':  'deliberate opt-in whose ABSENT state is the mandated default '
                           '(MockTestCreate R8b: the ban is absolute for every present '
                           'exam). Emitting it would imply an operator workflow that does '
                           'not exist. Operator decision 2026-08-28 (D2).',
    'formula_typography':  'per-exam opt-out whose DEFAULT (true) is the wanted behaviour '
                           'on every exam (§S8-0c). Operator decision 2026-08-28 (D2): '
                           'leave as is.',
    'renderer':            'field of the §6A-5 validation record on a RepresentationFigure '
                           '— written by self-test fixtures and validated at construction '
                           'via a tuple membership check this model cannot see; engine-'
                           'internal, never a cross-step contract — same class as di_rate.',
}

# HONEST LIMIT OF THIS CHECK, stated here so nobody reads a green run as more than it is.
#   It detects a field with NO consumer at all, or NO producer at all. It does NOT detect
#   one consumer among several dropping its read — GAP-2026-08-06-CONSUMER, where Step 7
#   stopped indexing axis1_target_series while the engine and the auditor still used it,
#   passes this check clean. That class needs a CONSUMER-SIDE FIXTURE, and the lesson has
#   now recurred twice: test the caller, not only the callee. This tool narrows the gap;
#   it does not close it.

TOKEN = re.compile(r'[a-z][a-z0-9_]{3,}')

def _read(p):
    try:
        return open(p, encoding='utf-8').read()
    except OSError:
        return ''

def writes(txt):
    out = set()
    # dict-literal form:  'key': value
    out |= {m.group(1) for m in re.finditer(r"['\"]([a-z][a-z0-9_]{3,})['\"]\s*:", txt)}
    # f-string emit form: f'key: {value}'   (section_rules writer)
    out |= {m.group(1) for m in re.finditer(r"f['\"]([a-z][a-z0-9_]{3,}):\s*\{", txt)}
    # ASSIGNMENT form:  src['key'] = ...   — audit_canonical populates its own src this
    # way, and omitting it made every src field read as an ORPHAN-READ, burying the real
    # findings under noise. A checker that cries wolf gets ignored, same as any gate.
    out |= {m.group(1) for m in re.finditer(
        r"\w+\[\s*['\"]([a-z][a-z0-9_]{3,})['\"]\s*\]\s*=", txt)}
    out |= {m.group(1) for m in re.finditer(
        r"\.setdefault\(\s*['\"]([a-z][a-z0-9_]{3,})['\"]", txt)}
    return out

def reads(txt):
    out = set()
    out |= {m.group(1) for m in re.finditer(r"\.get\(\s*['\"]([a-z][a-z0-9_]{3,})['\"]", txt)}
    out |= {m.group(1) for m in re.finditer(r"\[\s*['\"]([a-z][a-z0-9_]{3,})['\"]\s*\]", txt)}
    out |= {m.group(1) for m in re.finditer(r"_RE\s*=\s*re\.compile\(r?['\"].*?([a-z][a-z0-9_]{3,}):", txt)}
    # v1.3 — spec-directed config read: an anchor phrase followed within 200 chars by a
    # backtick-quoted key. Without this, a spec that reads config in PROSE (the correct
    # idiom for spec-directed session work, §6A-6) is invisible to this auditor —
    # GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ. The 200-char multi-line window is
    # required: real read sites wrap across lines. A HISTORICAL mention of a retired
    # key must be written WITHOUT backticks (the corpus convention), or it re-fires.
    out |= {m.group(1) for m in re.finditer(
        r"(?:CATEGORY\s+C|EXAM_STRUCTURE|section_rules(?:\.md)?)"
        r"[\s\S]{0,200}?`([a-z][a-z0-9_]{3,})(?::[^`]*)?`", txt, re.I)}
    return out

# v1.2 — PER-PAPER CONTAINERS. Registry fields whose VALUE is one entry per PAPER.
# The registry is SHARED across series (ScopedBlueprint §9), so an ordinal key ('1')
# collides between MOCK:M01, SUBJ:PHYS:01 and SUBJ:CHEM:01. Each must be written under
# a paper_id key; the ordinal key is permitted ALONGSIDE it (MOCK-series back-compat).
PER_PAPER_CONTAINERS = ('options_by_q', 'axis1_paper', 'axis3_paper',
                        'style_obs_by_q')   # v1.4 — GAP-2026-08-29 §6.5.5

_ORDINAL_WRITE = r"\[\s*str\(\s*(?:N|mock[a-z_]*)\s*\)\s*\]\s*="
_PAPERID_WRITE = r"\[\s*_?[a-z0-9_]*p(?:aper_)?id[a-z0-9_]*\s*\]\s*="

def key_shape_findings(root):
    """FAIL any per-paper container written ONLY under a paper-ordinal key.

    Alias-aware: the write may be inline (reg['f'][k] = v) or through a local
    bound to the container (a = reg.setdefault('f', {}); a[k] = v) — the shape
    final_assembly uses. Missing the aliased form would make this gate blind to
    the very code it was written for, so both are resolved.
    """
    out = []
    for fname in sorted(set(PRODUCERS) | set(CONSUMERS)):
        txt = _read(os.path.join(root, fname))
        if not txt:
            continue
        code = [l for l in txt.splitlines() if not l.lstrip().startswith('#')]
        for field in PER_PAPER_CONTAINERS:
            names = [rf"\w*\[\s*['\"]{field}['\"]\s*\]",
                     rf"\w*\.setdefault\(\s*['\"]{field}['\"][^)]*\)"]
            # locals bound to this container: `x = reg.setdefault('f', {})` / `= reg['f']`
            aliases = set()
            for l in code:
                for n in names:
                    m = re.search(rf"^\s*([A-Za-z_]\w*)\s*=\s*{n}\s*$", l)
                    if m:
                        aliases.add(m.group(1))
            targets = list(names) + [rf"{re.escape(a)}" for a in sorted(aliases)]
            assigns = [l for l in code
                       if any(re.search(rf"{tg}\s*\[[^\]]*\]\s*=", l) for tg in targets)]
            if not assigns:
                continue
            has_pid = any(re.search(_PAPERID_WRITE, l) for l in assigns)
            has_ord = any(re.search(_ORDINAL_WRITE, l) for l in assigns)
            if has_ord and not has_pid:
                out.append((field, fname,
                            'ORDINAL-ONLY per-paper key — collides across series on the '
                            'shared registry (GAP-2026-08-24-AXIS-PAPER-SERIES-COLLISION); '
                            'write [paper_id] as the authority'))
    return out


def main(argv):
    root = argv[1] if len(argv) > 1 else '.'
    scope = re.compile(argv[2]) if len(argv) > 2 else re.compile(
        r'figural|axis1|axis3|option_image|di_rate|di_q|di_reducible|'
        r'by_class|target_series|total_mocks|observed_figural|unkeyed|'
        # v1.3 — CATEGORY-C config-key families (GAP-2026-08-28-CATEGORY-C-ORPHAN-
        # CONFIG-READ): without these the prose-read widening finds the keys and the
        # scope filter then hides them, which is the same blindness with extra steps.
        r'renderer|subject_code|exam_convention|option_label|paper_header|'
        r'formula_typography')
    W, R = collections.defaultdict(set), collections.defaultdict(set)
    for f, step in PRODUCERS.items():
        for k in writes(_read(os.path.join(root, f))):
            W[k].add(step)
    for f, step in CONSUMERS.items():
        for k in reads(_read(os.path.join(root, f))):
            R[k].add(step)

    keys = sorted(k for k in (set(W) | set(R)) if scope.search(k))
    findings = []
    ks = key_shape_findings(root)
    print(f"{'field':38s} {'written by':22s} {'read by':26s} verdict")
    print('-' * 100)
    for k in keys:
        w, r = sorted(W.get(k, ())), sorted(R.get(k, ()))
        # a field written and read only by the same single component is internal
        internal = bool(w) and bool(r) and set(w) == set(r) and len(set(w)) == 1
        if not r and w and k not in ALLOW and not internal:
            v = 'ORPHAN-WRITE'; findings.append((k, v))
        elif not w and r and k not in ALLOW:
            v = 'ORPHAN-READ'; findings.append((k, v))
        elif k in ALLOW:
            v = 'allowed'
        else:
            v = 'ok'
        print(f"{k:38s} {','.join(w) or '-':22s} {','.join(r) or '-':26s} {v}")
    print('-' * 100)
    if ks:
        print(f"[FAIL] {len(ks)} KEY-SHAPE finding(s) (v1.2) — a per-paper container "
              f"keyed by ordinal is destroyed by the next paper of another series:")
        for field, fname, why in ks:
            print(f"    KEY-SHAPE      {field} in {fname}: {why}")
        return 1
    if not findings:
        print(f"[OK] 0 seam findings across {len(keys)} field(s) — every cross-step field "
              f"has both a producer and a consumer; {len(PER_PAPER_CONTAINERS)} per-paper "
              f"container(s) paper_id-keyed (v1.2 KEY-SHAPE).")
        return 0
    print(f"[FAIL] {len(findings)} seam finding(s) — a field with one side only is how "
          f"every 2026.08.06.x defect shipped:")
    for k, v in findings:
        print(f"    {v:14s} {k}")
    print("\n  Fix the wiring, or add the field to ALLOW with a reason if it is "
          "legitimately one-sided.")
    return 1

def self_test():
    """Fixtures that MUTATE a copy of the seam files and assert the auditor
    notices (GAP-2026-08-14-AUDITOR-SELFTESTS). The three v1.1 ALLOW
    justifications are also pinned as STANDING guards: the mutation evidence
    from the AXISPAPER resolution is now a permanent fixture, not a one-off
    commit note."""
    import io, shutil, tempfile, contextlib
    passed, fails = 0, []

    def _ks_fixture():
        """v1.2 KEY-SHAPE: the live corpus is clean, and REVERTING either fix
        (paper_id write -> ordinal-only) must be caught. Watch the watcher."""
        root = os.path.dirname(os.path.abspath(__file__))
        if key_shape_findings(root):
            return False, 'live corpus already has a KEY-SHAPE finding'
        d = tempfile.mkdtemp()
        for f in set(PRODUCERS) | set(CONSUMERS):
            src = os.path.join(root, f)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(d, f))
        fa_p = os.path.join(d, 'final_assembly.py')
        txt = open(fa_p, encoding='utf-8').read()
        mutated = txt.replace("_a1[_axpid] = copy.deepcopy(dict(axis1_snapshots))",
                              "_a1[str(N)] = copy.deepcopy(dict(axis1_snapshots))")
        if mutated == txt:
            return False, 'mutation anchor missing — final_assembly axis write changed shape?'
        open(fa_p, 'w', encoding='utf-8').write(mutated)
        got = key_shape_findings(d)
        return (any(f == 'axis1_paper' for f, _, _ in got),
                f'mutant findings={[f for f, _, _ in got]}')

    _ks_ok, _ks_why = _ks_fixture()
    if _ks_ok:
        passed += 1
    else:
        fails.append(f'KEY-SHAPE-catches-ordinal-only-revert ({_ks_why})')

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def run_root(root):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(['audit_seam.py', root])
        return rc, buf.getvalue()

    def copy_seam_files(dst, mutate=None):
        for f in set(PRODUCERS) | set(CONSUMERS):
            shutil.copy(f, os.path.join(dst, f))
        if mutate:
            mutate(dst)
        return dst

    # 1 — the live repo passes.
    rc, out = run_root('.')
    check("live repo is seam-clean", rc == 0 and '0 seam findings' in out)

    with tempfile.TemporaryDirectory() as d:
        # 2 — STANDING MUTATION (the AXISPAPER evidence, made permanent):
        # deleting final_assembly's axis1_paper write must go red again.
        def kill_write(root):
            p = os.path.join(root, 'final_assembly.py')
            s = open(p, encoding='utf-8').read()
            s2 = s.replace("reg.setdefault('axis1_paper', {})", "reg.setdefault('axis1_paper_gone', {})", 1)
            assert s2 != s, "mutation anchor missing — final_assembly no longer writes axis1_paper?"
            open(p, 'w', encoding='utf-8').write(s2)
        rc, out = run_root(copy_seam_files(d, kill_write))
        check("deleting the axis1_paper write fires ORPHAN-READ again",
              rc == 1 and 'ORPHAN-READ' in out and 'axis1_paper' in out)
    with tempfile.TemporaryDirectory() as d:
        # 3 — a fresh producer-side orphan write is caught.
        def orphan_write(root):
            with open(os.path.join(root, 'blueprint_core.py'), 'a', encoding='utf-8') as f:
                f.write('\n_SEAM_FIXTURE = {"figural_selftest_write": 1}\n')
        rc, out = run_root(copy_seam_files(d, orphan_write))
        check("a write nothing reads fires ORPHAN-WRITE",
              rc == 1 and 'ORPHAN-WRITE' in out and 'figural_selftest_write' in out)
    with tempfile.TemporaryDirectory() as d:
        # 4 — a fresh consumer-side orphan read is caught.
        def orphan_read(root):
            with open(os.path.join(root, 'Framework_MockTestCreate.md'), 'a', encoding='utf-8') as f:
                f.write('\n    snap = reg["figural_selftest_read"]\n')
        rc, out = run_root(copy_seam_files(d, orphan_read))
        check("a read nothing writes fires ORPHAN-READ",
              rc == 1 and 'ORPHAN-READ' in out and 'figural_selftest_read' in out)

    # v1.3 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ fixtures.
    # 4b — CATCH: a prose CATEGORY-C read of a key nothing emits must fire
    # ORPHAN-READ. This is the exact shape of the defect this version exists
    # for, appended to an Explain spec (the consumer class that was invisible).
    with tempfile.TemporaryDirectory() as d:
        def prose_orphan_read(root):
            with open(os.path.join(root, 'Framework_MockTestExplain.md'),
                      'a', encoding='utf-8') as f:
                f.write('\n  read section_rules CATEGORY C '
                        '`renderer_selftest_orphan` before solving.\n')
        rc, out = run_root(copy_seam_files(d, prose_orphan_read))
        check("v1.3 CATCH: a prose CATEGORY-C read nothing emits fires ORPHAN-READ",
              rc == 1 and 'ORPHAN-READ' in out and 'renderer_selftest_orphan' in out)
    # 4c — CLEAN: a prose read of a key the producer DOES emit must pass.
    # option_label_format is the standing true-positive control: read in the
    # same prose idiom by both Explain specs, and emitted by write_section_rules.
    check("v1.3 CLEAN: option_label_format (emitted + prose-read) verdict is ok",
          re.search(r'option_label_format\s+\S.*\sok', run_root('.')[1]) is not None)
    # 4d — the historical-mention convention: a retired key written WITHOUT
    # backticks near an anchor is NOT a read (else every HISTORY note re-fires).
    check("v1.3 convention: un-backticked historical mention is not a read",
          'subject_code' not in reads(
              'HISTORY: was read from section_rules CATEGORY C subject_code, retired.'))

    # 5 — regex units: every write/read form the model depends on.
    check("writes(): dict-literal form", 'axis1_k' in writes("x = {'axis1_k': 1}"))
    check("writes(): setdefault form (final_assembly's persistence path)",
          'axis1_k' in writes("reg.setdefault('axis1_k', {})[n] = s"))
    check("writes(): subscript-assign form", 'axis1_k' in writes("src['axis1_k'] = 1"))
    check("reads(): .get form", 'axis1_k' in reads("v = d.get('axis1_k', {})"))
    check("reads(): subscript form", 'axis1_k' in reads("v = d['axis1_k']"))
    # v1.3 — the prose-read form, in all three anchor spellings and line-wrapped.
    check("reads(): prose form, CATEGORY C anchor",
          'axis1_k' in reads("read section_rules CATEGORY C `axis1_k` here"))
    check("reads(): prose form, EXAM_STRUCTURE anchor",
          'axis1_k' in reads("the === EXAM_STRUCTURE === block's `axis1_k` value"))
    check("reads(): prose form, line-wrapped within 200 chars",
          'axis1_k' in reads("read section_rules CATEGORY C\n      `axis1_k` before solving"))
    check("reads(): prose form with inline value suffix",
          'axis1_k' in reads("section_rules CATEGORY C `axis1_k: false` switch"))

    # 6 — ALLOW hygiene: an entry without a real reason is where findings
    # get buried; the file's own comment says so.
    check("every ALLOW entry carries a substantive reason",
          all(isinstance(v, str) and len(v.strip()) >= 20 for v in ALLOW.values()))

    # 7 — STANDING GUARDS for the three v1.1 ALLOW justifications: each entry
    # stays honest only while its claim stays true of the corpus.
    prod_writes = set()
    for f in PRODUCERS:
        prod_writes |= writes(_read(f))
    check("allow-guard: no cross-step producer writes axis1_paper_counts "
          "(still Step-7-internal)", 'axis1_paper_counts' not in prod_writes)
    check("allow-guard: no cross-step producer writes axis3_paper_counts "
          "(still Step-7-internal)", 'axis3_paper_counts' not in prod_writes)
    mtc = _read('Framework_MockTestCreate.md')
    check("allow-guard: MockTestCreate still initialises the counts locally",
          'axis1_paper_counts = {}' in mtc and 'axis3_paper_counts = {}' in mtc)
    cons_reads = set()
    for f in CONSUMERS:
        cons_reads |= reads(_read(f))
    check("allow-guard: axis3_mechanism_lock still has no literal-name reader "
          "(report-only)", 'axis3_mechanism_lock' not in cons_reads)
    # v1.3 — STANDING GUARDS for the D2 ALLOW entries: each stays honest only
    # while its claim stays true of the corpus.
    check("allow-guard: paper_header_block emitted by no producer except "
          "audit_canonical's own internal findings dict "
          "(D2: absent state is the mandated default)",
          all('paper_header_block' not in writes(_read(f))
              for f in PRODUCERS if f != 'audit_canonical.py'))
    check("allow-guard: formula_typography still emitted by no producer "
          "(D2: default true is the wanted behaviour)",
          all('formula_typography' not in writes(_read(f)) for f in PRODUCERS))
    check("allow-guard: the retired keys are no longer read ANYWHERE in prose "
          "(the §6 fix holds; a reintroduction re-fires 4b's class)",
          not any(k in cons_reads for k in
                  ('representation_renderers', 'subject_code', 'exam_conventions')))

    print(f"audit_seam self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    sys.exit(main(sys.argv))
