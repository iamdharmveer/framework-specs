#!/usr/bin/env python3
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
             'audit_canonical.py': 'audit'}
CONSUMERS = {'Framework_Blueprint.md': 'Step6',
             'Framework_MockTestCreate.md': 'Step7',
             'blueprint_core.py': 'engine',
             'audit_canonical.py': 'audit'}

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
    return out

def main(argv):
    root = argv[1] if len(argv) > 1 else '.'
    scope = re.compile(argv[2]) if len(argv) > 2 else re.compile(
        r'figural|axis1|axis3|option_image|di_rate|di_q|di_reducible|'
        r'by_class|target_series|total_mocks|observed_figural|unkeyed')
    W, R = collections.defaultdict(set), collections.defaultdict(set)
    for f, step in PRODUCERS.items():
        for k in writes(_read(os.path.join(root, f))):
            W[k].add(step)
    for f, step in CONSUMERS.items():
        for k in reads(_read(os.path.join(root, f))):
            R[k].add(step)

    keys = sorted(k for k in (set(W) | set(R)) if scope.search(k))
    findings = []
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
    if not findings:
        print(f"[OK] 0 seam findings across {len(keys)} field(s) — every cross-step field "
              f"has both a producer and a consumer.")
        return 0
    print(f"[FAIL] {len(findings)} seam finding(s) — a field with one side only is how "
          f"every 2026.08.06.x defect shipped:")
    for k, v in findings:
        print(f"    {v:14s} {k}")
    print("\n  Fix the wiring, or add the field to ALLOW with a reason if it is "
          "legitimately one-sided.")
    return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
