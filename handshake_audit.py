#!/usr/bin/env python3
"""
HANDSHAKE AUDIT — release 2026.11.03 (GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY).
Release 2026.11.21 (GAP-2026-11-16-DIFFICULTY-YARDSTICK) adds H-R3: the ladder chain, Step 5 to the auditor.
Release 2026.11.08 (GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER) adds H-DL: the difficulty layer as
one chain on three synthetic exams (_dl_handshake, below).

WHY THIS FILE EXISTS. Three cold reviews of that release found 48 defects, and 15 of them
were HANDSHAKE breaks: a producer wrote one shape and its consumer read another — an
inverted dict (common entities listed paper names), a field no step wrote (key_set_size),
29 quality-record fields dropped at commit so the final sweep could not see them, a
readiness probe testing field names no artefact carried, a judge-exemplar cascade with no
engine behind it. Every static gate in the estate was green through all of it, because a
static gate reads ONE side of a boundary. This audit runs the REAL engines and the REAL
executable fences of the specs as ONE chain on a synthetic exam, so each step's actual
output artefact is the next step's actual input:

  PYQExplain content records -> bc.dp_add_paper -> difficulty profile
    -> Step 5 (analyse_engine) QUALITY block / EXAM_QUALITY / exemplar bank
    -> Blueprint §7-8 + ScopedBlueprint S8-2d shape targets
    -> Create S3-2e readiness, S3-12d shape plan, judge packet
    -> S7-QUALITY sidecar -> audit_canonical pre-commit sweep -> certificate
    -> S13-2G phase 1 packet (internal) -> reviewer brief (MockReview S1-1..S3-2, a fresh
       sub-agent's work) -> phase 3 (two rounds; NOT_RUN; legacy verdict by content) — all in-run
    -> final_assembly.commit_registry -> audit_canonical final sweep (registry only)
    -> MockDeliver item 3f (refuse / accept) -> §8 handoff / footer lines.

Every assertion names the producer and the consumer it binds. Absolute paths the spec
fences hard-code (/home/claude, /mnt/project, /mnt/user-data) are RELOCATED under a
temporary root for the run, so the audit executes on any machine (CI included) and
never touches a real project. Run: `python3 handshake_audit.py --self-test`
(discovery-driven CI runs it). Exit 1 on any failed handshake.
"""
import json, os, re, shutil, subprocess, sys, tempfile, textwrap, zipfile, hashlib, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _relocate(code, root):
    """Rewrite the absolute roots a spec fence hard-codes to live under `root`."""
    for pre in ('/home/claude', '/mnt/user-data', '/mnt/project'):
        code = code.replace("'" + pre, "'" + root + pre).replace('"' + pre, '"' + root + pre)
    return code


def fences(path, marker=None):
    txt = open(path, encoding='utf-8').read().split('\n'); out = []; cur = None
    for i, l in enumerate(txt, 1):
        s = l.strip()
        if cur is None:
            if s == '```python': cur = (i, [])
            continue
        if s == '```':
            body = textwrap.dedent('\n'.join(cur[1]))
            # 2026.11.15 (GAP-2026-11-13-STEP7-SPEED G-02): a RUN-BLOCK's header lines (ID, PARAMS, DEFINES) come
            # before the block's own first comment — the marker is looked for after them
            _hd = '\n'.join(x for x in body.split('\n') if not x.lstrip().startswith(('# RUN-BLOCK', '# PARAMS:', '# DEFINES:')))
            if marker is None or marker in _hd[:120]: out.append((cur[0], body))
            cur = None; continue
        cur[1].append(l)
    return out


def _dl_handshake(check, ROOT, run_fence, W):
    """H-DL (release 2026.11.08, GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER) — the difficulty layer as
    ONE chain on THREE synthetic exams (a post-graduate organic exam, a shallower organic exam and a
    non-chemistry exam), so no rule is tuned to one paper (owner Q5):
      Step 5 bank (analyse_engine.write_exemplar_bank: profile sha256 + blind grades)
        -> Create S3-8L (ruler, shares source, freeze, target plan) -> S3-12c (pattern sources)
        -> CHECK 3c measured band (the spec's rule) -> S13-2G phase 1 packet (concept vocabulary,
           author concepts stripped) -> MockReview verdict file (concepts_used kept)
        -> phase 3 round 1 / round 2 (DL1) -> S13-2L paper gate -> final_assembly commit
           (difficulty_state + registry grade cache, kept by regcheck) -> audit_canonical
           A-CONTENTLEVEL / A-DIFFGATE -> S13-6 lines == MockDeliver 3f'' lines.
    Every assertion names the producer and the consumer it binds."""
    import blueprint_core as bc, analyse_engine as ae, final_assembly as fa, audit_canonical as ac
    import hashlib as _hl, random as _rnd
    labs = ['Easy', 'Medium', 'Hard']
    V = bc.l2_vocabulary()
    by_load = {l: [x['label'] for x in V if x['load'] == l] for l in range(1, 7)}
    CREATE = os.path.join(W, 'Framework_MockTestCreate.md')
    S = open(CREATE, encoding='utf-8').read()

    def blk(tag):
        i = S.index(tag); a = S.rfind('```python', 0, i); b = S.index('```', i)
        return textwrap.dedent(S[a + 9:b])

    def snip(start, end):
        i = S.index(start); j = S.index(end, i)
        return textwrap.dedent(S[i:j])

    # exam recipes: (concept loads per band, concepts per band, organic?)
    RECIPES = {
        'PGX': ({'Easy': (2, 3), 'Medium': (3, 4), 'Hard': (5, 6)}, {'Easy': 1, 'Medium': 2, 'Hard': 3}, True),
        'UGX': ({'Easy': (1, 1), 'Medium': (2, 2), 'Hard': (3, 3)}, {'Easy': 1, 'Medium': 1, 'Hard': 2}, True),
        'PHX': ({'Easy': (1, 1), 'Medium': (2, 2), 'Hard': (3, 3)}, {'Easy': 1, 'Medium': 1, 'Hard': 2}, False),
    }
    PAPERS = {'10-Jun-2024': '2024-06-10', '15-Dec-2024': '2024-12-15', '20-Jun-2025': '2025-06-20'}
    results = {}
    for EXAM, (loads, ncon, organic) in RECIPES.items():
        rng = _rnd.Random(EXAM)
        sec = 'Organic Chemistry' if organic else 'Mechanics'
        pfx = 'oc' if organic else 'ph'
        sids = [f'{pfx}.t{i}.s{i}' for i in range(1, 5)]
        man = {'subtopics': {s: {'display_name': s, 'section': sec, 'topic': f'{sec} topic'} for s in sids}}
        prof = {'_meta': {'difficulty_labels': labs, 'exam_code': EXAM}, 'papers': {}}
        for pk in PAPERS:
            qs = {}
            for i in range(1, 31):
                band = labs[0] if i <= 6 else labs[1] if i <= 21 else labs[2]
                lo, hi = loads[band]
                nc = [rng.choice(by_load[rng.randint(lo, hi)]) for _ in range(ncon[band])]
                qs[str(i)] = {'band': band, 'qtype': 'mcq', 'section': sec, 'subtopic_id': sids[i % 4],
                              'named_concepts': nc if organic else [], 'ask_type': 'direct', 'stereo_decl': 'none',
                              'distractor_mechanisms': (['regioisomer', 'stereoisomer_diastereomer', 'formula_error']
                                                        if band == 'Hard' else ['formula_error'] * 3)}
            prof['papers'][pk] = {'date': PAPERS[pk], 'questions': qs}
        PF = ROOT + f'/mnt/project/{EXAM}_difficulty_profile.json'
        json.dump(prof, open(PF, 'w'))
        sha = _hl.sha256(open(PF, 'rb').read()).hexdigest()
        grades = {f'{pk}:Q{q}': r['band'] for pk, pp in prof['papers'].items() for q, r in pp['questions'].items()}
        # Step 5 -> the bank Create attaches
        bpath, bank, _dr = ae.write_exemplar_bank(EXAM, [], out_dir=ROOT + '/tmp', profile_sha256=sha,
                                                  pyq_grades=bc.pyq_grades_record(sha, labs, grades, source='step5-blind'))
        bank = json.load(open(bpath, encoding='utf-8'))
        g_b, st_b = bc.bank_pyq_grades(bank, sha, labs)
        check(f'H-DL {EXAM} Step 5 bank -> Create: same profile sha256, grades fresh',
              st_b == 'fresh' and len(g_b) == 90, st_b)
        plan = {q: (labs[0] if q <= 4 else labs[1] if q <= 12 else labs[2]) for q in range(1, 21)}
        sub_by_q = {q: sids[q % 4] for q in plan}
        reg = {'question_index': []}
        bp = {'subtopic_list': [{'subtopic_id': s} for s in sids], 'difficulty_source': {'measured_pct': {'Easy': 20, 'Medium': 50, 'Hard': 30}},
              'difficulty_labels': labs, 'mocks': [{'mock': 1, 'paper_id': 'MOCK:M01'}]}
        G = {'bc': bc, 'EXAM': EXAM, 'N': 1, 'reg': reg, 'bp': bp, 'paper_id': 'MOCK:M01', '_pid_dp': 'MOCK:M01',
             'difficulty_labels': labs, 'MANIFEST_IDS': man['subtopics'], 'subtopic_list': bp['subtopic_list'],
             'DIFFICULTY_PROFILE': prof, 'EXEMPLAR_BANK': bank, 'PROFILE_CFG': {'cycle_gap_days': None},
             'SECTION_RULES_TEXT': '', 'DIFFICULTY_STATE': {'judge_dormant_qs': [], 'hard_missed': 0, 'n_level_items': 0},
             'difficulty_plan': dict(plan), 'subtopic_by_qnum': sub_by_q}
        run_fence(blk('# ── S3-8L (v5.94) ──'), G)
        # S3-12e (between S3-8L and S3-15L) may move top-band slots between subtopics, counts unchanged:
        # the target plan and the pattern sources must describe the plan AFTER that move
        G['difficulty_plan'][12], G['difficulty_plan'][13] = G['difficulty_plan'][13], G['difficulty_plan'][12]
        G['difficulty_plan'][4], G['difficulty_plan'][5] = G['difficulty_plan'][5], G['difficulty_plan'][4]
        plan = dict(G['difficulty_plan'])
        run_fence(blk('# ── S3-15L (v5.94) ──'), G)
        M = G['L2_MODEL']; DS = G['DIFFICULTY_STATE']
        check(f'H-DL {EXAM} S3-15L: target plan == the FINAL plan (after the S3-12e move), sources at the final band',
              G['DIFFICULTY_PLAN_TARGET'] == {str(q): b for q, b in plan.items()}
              and all(src.get('band') == plan[int(q)] for q, src in G['L2_SOURCES'].items()))
        if organic:   # paper 2 of the series reuses the frozen ruler AND still gets its pattern cards
            G2 = dict(G, reg={'question_index': [{'mock': 1, 'paper_id': 'MOCK:M01', 'difficulty_state': copy.deepcopy(DS)}]},
                      DIFFICULTY_STATE={'judge_dormant_qs': [], 'hard_missed': 0, 'n_level_items': 0},
                      paper_id='MOCK:M02', _pid_dp='MOCK:M02')
            run_fence(blk('# ── S3-8L (v5.94) ──'), G2)
            check(f'H-DL {EXAM} series: paper 2 reuses the frozen cut-offs and keeps every pattern card',
                  G2['L2_MODEL'].get('cuts_list') == M.get('cuts_list') and len(G2['L2_CARDS']) == len(G['L2_CARDS']) > 0
                  and bc.l2_band_load_floor(G2['L2_CARDS'], 'Hard') == bc.l2_band_load_floor(G['L2_CARDS'], 'Hard'))
        if organic:
            check(f'H-DL {EXAM} S3-8L: ruler active + binding, shares from the Step-5 blind grades',
                  bool(M and M.get('active') and M.get('binding')) and M.get('shares_source') == 'pyq_grades',
                  str({k: (M or {}).get(k) for k in ('active', 'binding', 'shares_source', 'vocab_coverage', 'n', 'reason', 'cuts_list')}))
            check(f'H-DL {EXAM} S3-8L: frozen model + scope ids + profile sha persisted for phase 3 / the series',
                  DS['l2_model']['frozen'] and DS['l2_model']['scope_ids'] == sids and DS['l2_model']['profile_sha256'] == sha)
            check(f'H-DL {EXAM} S3-15L: every organic slot has a pattern source; no card carries a stem / key / SMILES',
                  len(G['L2_SOURCES']) == 20 and all(not ({'stem', 'key', 'smiles', 'options'} & set(c)) for c in G['L2_CARDS']))
        else:
            check(f'H-DL {EXAM} S3-8L: no organic subtopic -> no ruler, no sources (generic layer only, owner Q4)',
                  M is None and G['L2_SOURCES'] == {} and 'l2_model' not in DS)
        # CHECK 3c (the spec's rule): an author who writes every slot one band too easy
        cm = {}
        for q, b in plan.items():
            wb = labs[max(0, labs.index(b) - 1)]
            lo, hi = loads[wb]
            nc = [rng.choice(by_load[rng.randint(lo, hi)]) for _ in range(ncon[wb])] if organic else []
            obs = {'qtype': 'mcq', 'named_concepts': nc, 'stereo_decl': 'none', 'ask_type': 'direct',
                   'distractor_mechanisms': ['formula_error'] * 3}
            l2 = bc.l2_record(obs, M, labs, 'mcq') if M else {'band': None}
            obs['l2'] = l2
            judge = None if organic else wb                         # the non-chemistry exam: the judge measures
            m = bc.difficulty_band_min({'judge': judge, 'ruler': l2['band'] if (M and M.get('binding')) else None}, labs)
            dc = {'scheduled': b, 'rated': judge or b, 'decision': 'agree', 'final_band': b, 'measured': m['band'],
                  'measured_source': m['source']}
            if m['band'] and labs.index(m['band']) < labs.index(b):
                dc['decision'] = 'carried_below'
            cm[str(q)] = {'subtopic_id': sub_by_q[q], 'difficulty': b, 'difficulty_obs': obs, 'difficulty_check': dc,
                          'distractor_mechanisms': ['formula_error'] * 3, 'stem_text': f'stem {q}', 'option_texts': ['a', 'b', 'c', 'd'],
                          # v2.0 (S0-OP-5): two FRESH blind graders measure the band the author actually wrote (wb);
                          # the key is unanimous (author + 2 blind solvers)
                          }
            # written by THE one writer (bc.op_record_controls — bound to the item's own text)
            cm[str(q)] = bc.op_record_controls(cm[str(q)], wb, wb, True,
                                               {'grader_1': {'context': 'fresh', 'sha256': 'a' * 64},
                                                'grader_2': {'context': 'fresh', 'sha256': 'b' * 64}},
                                               key_votes={'author': 1, 'solver_1': 1, 'solver_2': 1, 'unanimous': True})
        n_below = sum(1 for e in cm.values() if e['difficulty_check']['decision'] == 'carried_below')
        check(f'H-DL {EXAM} CHECK 3c: one-band-easier writing is measured below its slot ({n_below}/16 non-bottom slots)',
              n_below >= 12, str(n_below))
        # S13-2G phase 1: the packet the reviewer gets
        items = [{'q': int(q), 'subtopic_id': e['subtopic_id'], 'stem': e['stem_text'], 'options': e['option_texts'],
                  'named_concepts': e['difficulty_obs']['named_concepts'], 'figures': []} for q, e in cm.items()]
        P1 = {'bc': bc, 'batch_state': {'difficulty_state': copy.deepcopy(DS)}, '_items': items, '_slice': {},
              'PAPER_MD5': 'f' * 32, '_panel': [], '_switch': set()}
        run_fence(snip("  # v5.94: an organic paper's reviewer also names", "  REVIEW_ROUND = int("), P1)
        PK = P1['PACKET']
        _flat = json.dumps(PK)
        check(f'H-DL {EXAM} S13-2G phase 1 -> MockReview: vocabulary present iff organic; author concepts never in the packet',
              (('concept_vocabulary' in _flat) == organic) and '"named_concepts"' not in _flat)
        # MockReview S3-2 verdict file -> phase 3: concepts_used survives normalisation
        recs = {}
        for q, e in cm.items():
            recs[q] = {'own_key': 1, 'single_answer': 'yes', 'leak_or_paraphrase': 'none',
                       'difficulty_band_with_exemplar': f"{e['difficulty_check']['measured'] or e['difficulty']}, like exemplar {e['subtopic_id']}/1",
                       'distractor_existence_and_class': '1: x', 'key_derivation': 'd', 'confidence': 'high',
                       'consistency_and_names': 'ok', 'selectivity_basis': 'clean',   # a COMPLETE record (D0, 2026.11.09)
                       'concepts_used': list(e['difficulty_obs']['named_concepts'])}
        VF, _vprobs = bc.review_verdict_file(EXAM, 'm01', 'f' * 32, recs, reviewer='sub-agent')
        _vf_items = VF.get('items') if isinstance(VF, dict) else {}
        check(f'H-DL {EXAM} MockReview verdict file keeps concepts_used as a list (phase 3 reads it)',
              all(isinstance((_vf_items.get(q) or {}).get('concepts_used'), list) for q in cm))
        # phase 3 round 1 / round 2 + S13-2L, run from the spec's own fences on files
        HOME = ROOT + '/home/claude'
        RD = HOME + f'/{EXAM}_M1_review/round1'
        shutil.rmtree(HOME + f'/{EXAM}_M1_review', ignore_errors=True)
        bs = {'paper_id': 'MOCK:M01', 'difficulty_plan': {str(q): b for q, b in plan.items()},
              'difficulty_schedule_original': {str(q): b for q, b in plan.items()},
              'difficulty_plan_target': dict(G['DIFFICULTY_PLAN_TARGET']), 'l2_sources': dict(G['L2_SOURCES']),
              'difficulty_labels': labs, 'difficulty_state': copy.deepcopy(DS), 'paper_md5': 'f' * 32, 'review_round': 0}
        kd = {'concept_map': cm, 'answers': {q: 1 for q in cm}}
        for rnd in (1, 2):
            rd = RD.replace('round1', f'round{rnd}'); os.makedirs(rd + '/part1')
            bs['review_dir'] = rd
            json.dump(bs, open(HOME + f'/{EXAM}_M1_batch_state.json', 'w'))
            json.dump(kd, open(HOME + f'/{EXAM}_M1_answer_key.json', 'w'))
            json.dump({'paper_md5': 'f' * 32, 'reviewer': 'sub-agent', 'items': _vf_items}, open(rd + '/part1/verdicts.json', 'w'))
            json.dump({'parts': [{'part': 1, 'dir': rd + '/part1', 'qs': [int(q) for q in cm],
                                  'verdicts': rd + '/part1/verdicts.json', 'reviewer': 'sub-agent'}]}, open(rd + '/queue.json', 'w'))
            run_fence(blk('# ── S13-2G phase 3 (executable'), {'EXAM': EXAM, 'N': 1, 'UNCERTIFIED_ITEMS': []})
            bs = json.load(open(HOME + f'/{EXAM}_M1_batch_state.json')); kd = json.load(open(HOME + f'/{EXAM}_M1_answer_key.json'))
            if rnd == 1:
                rep = bs.get('review_dl_repair') or []
                check(f'H-DL {EXAM} phase 3 round 1: every below item is a REVIEW_REPAIR defect at DR1, none relabelled',
                      len(rep) == n_below and set(rep) <= set(bs['review_defects']) and bs['state'] == 'REVIEW_REPAIR'
                      and all(kd['concept_map'][q]['difficulty'] == plan[int(q)] for q in rep), str(len(rep)))
        below = sorted((q for q, e in kd['concept_map'].items() if e['difficulty_check'].get('decision') == 'carried_below'), key=int)
        check(f'H-DL {EXAM} phase 3 round 2 (OD-2026-11-09): below items stay AT their slot (carried_below) — never relabelled',
              len(below) == n_below and not (bs['difficulty_state'].get('dr3_qs') or [])
              and all(kd['concept_map'][q]['difficulty'] == plan[int(q)] and kd['concept_map'][q]['difficulty_check'].get('dl_rung') != 'DR3'
                      for q in below), str(len(below)))
        _bpp = HOME + f'/{EXAM}_hs_bp.json'; json.dump(bp, open(_bpp, 'w'))
        def _l2l():
            try:
                run_fence(blk('# ── S13-2L (v6.0) ──'), {'EXAM': EXAM, 'N': 1, 'BP_SRC_PATH': _bpp}); return None
            except RuntimeError as _x:
                return str(_x)
        _r1 = _l2l()
        bs = json.load(open(HOME + f'/{EXAM}_M1_batch_state.json')); kd = json.load(open(HOME + f'/{EXAM}_M1_answer_key.json'))
        check(f'H-DL {EXAM} S13-2L: every below slot opens a DIFFICULTY chain whose first action is rework DR1 (SLOT-CHAIN, no stop)',
              _r1 and 'SLOT-CHAIN' in _r1 and sorted((w['q'] for w in bs['slot_chain_work']), key=int) == below
              and all(w['action'] == 'rework_dr1' for w in bs['slot_chain_work'])
              and all(bs['slot_chain'][q]['kind'] == 'difficulty' for q in below), str(_r1)[:200])
        # every reviewed attempt of every chain fails (the worst case): exhaust stages 1-5 from the engine itself
        for q in below:
            c = bs['slot_chain'][q]
            for _i in range(40):
                nx = bc.slot_chain_next(c, siblings=['s1', 's2', 's3'])
                c = nx['chain']
                if nx['action'] not in ('rework_dr1', 'rework_dr2', 'replace', 'shape', 'sibling'):
                    break
                c = bc.slot_chain_record(c, nx['stage'], 'fail', sibling=nx['sibling'])
            bs['slot_chain'][q] = c
        bs['slot_chain_work'] = []
        json.dump(bs, open(HOME + f'/{EXAM}_M1_batch_state.json', 'w'))
        _rs = []
        for _pass in range(12):                       # v2.0: reserve_refill -> refill_session(s) -> bounded last resort
            _rs.append(_l2l())
            bs = json.load(open(HOME + f'/{EXAM}_M1_batch_state.json'))
            bs['slot_chain_work'] = []                # every refill worker of the worst case produces nothing usable
            json.dump(bs, open(HOME + f'/{EXAM}_M1_batch_state.json', 'w'))
            if _rs[-1] is None:
                break
        bs = json.load(open(HOME + f'/{EXAM}_M1_batch_state.json')); kd = json.load(open(HOME + f'/{EXAM}_M1_answer_key.json'))
        PG = bs['difficulty_state']['paper_gate']
        lr = sorted((str(f['q']) for f in PG.get('last_resort') or []), key=int)
        check(f'H-DL {EXAM} S13-2L v6.0: exhausted slots end at reserve_refill -> refill_session -> the bounded LAST RESORT; the loop ends (no stop)',
              _rs[-1] is None and lr == below and all(bs['slot_chain'][q]['outcome'] == 'last_resort' for q in below)
              and not any(c.get('outcome') in ('forced', 'band_swap', 'paired_upgrade', 'majority', 'amber')
                          for c in bs['slot_chain'].values())
              and bs.get('refill_sessions_used') == bc.C_REFILL_SESSIONS, str((_rs[-1], lr[:4]))[:300])
        check(f'H-DL {EXAM} S13-2L v6.0: never relabelled to the request — a last-resort slot is labelled at the band it MEASURED; every other slot exactly at its band',
              all(kd['concept_map'][q]['difficulty'] == labs[max(0, labs.index(plan[int(q)]) - 1)] for q in below)
              and all(kd['concept_map'][q]['difficulty'] == plan[int(q)] for q in kd['concept_map'] if q not in below)
              and PG.get('labels') == labs and PG.get('target_plan') == G['DIFFICULTY_PLAN_TARGET'], str(PG.get('counts_final')))
        check(f'H-DL {EXAM} LAW-ORG-5: every label verifies STRICTLY (measured_exact or last_resort); obs is never a basis',
              all(bc.verify_difficulty_label(kd['concept_map'][q], labs, strict=True)[0] for q in kd['concept_map'])
              and all(bc.verify_difficulty_label(kd['concept_map'][q], labs)[2] == 'last_resort' for q in below)
              and all(kd['concept_map'][q]['difficulty_obs'] == cm[q]['difficulty_obs'] for q in below))
        _cf = bs['difficulty_state'].get('chain_footer') or {}
        check(f'H-DL {EXAM} footer: one AMBER line per last-resort item naming requested and delivered band + one P0 incident each',
              len([x for x in _cf.get('amber') or [] if 'last resort' in x]) == len(below)
              and all(f"Q{q}: last resort — requested {plan[int(q)]}" in ' '.join(_cf['amber']) for q in below)
              and len(bs['difficulty_state'].get('incidents') or []) == len(below)
              and all(i['severity'] == 'P0' for i in bs['difficulty_state']['incidents']))
        # final_assembly: difficulty_state committed on the entry; the grade cache kept by regcheck
        R = {'question_index': [], 'papers_completed': []}
        qrecs = [dict(e, q=int(q)) for q, e in kd['concept_map'].items()]
        _ent = {'paper_id': 'MOCK:M01', 'mock': 1, 'questions': qrecs, 'difficulty_state': copy.deepcopy(bs['difficulty_state'])}
        R['question_index'].append(_ent)
        RG = {'registry': R, 'L2_PYQ_GRADES_RECORD': G['L2_PYQ_GRADES_RECORD']}
        run_fence(snip("  _pgr = globals().get('L2_PYQ_GRADES_RECORD')", "  # v5.52 (GAP-2026-08-12-S13-COMMIT-COMPLETE) — ATOMICITY"), RG)
        check(f'H-DL {EXAM} S13-4: the registry caches the blind grades for THIS profile only (organic exams)',
              (sorted((RG['registry'].get('pyq_grades') or {})) == [sha]) == organic
              and bc.pyq_grades_from_registry(RG['registry'], sha, labs) == (grades if organic else {}))
        # auditor twins read the committed record
        src = {'registry': RG['registry'], 'concept_map': {}, '_mockN': 1, 'paper_id': 'MOCK:M01', 'blueprint': bp}
        ac.RESULTS.clear(); ac.gate_contentlevel({'concept_map': kd['concept_map']}); ac.gate_diffgate(src)
        _r = {c: l for l, c, m in ac.RESULTS}
        check(f'H-DL {EXAM} audit_canonical: A-CONTENTLEVEL OK on DL decisions; A-DIFFGATE re-count == S13-2L gate',
              _r.get('A-CONTENTLEVEL') == 'OK' and _r.get('A-DIFFGATE') == 'OK', str(ac.RESULTS)[:200])
        # S13-6 lines (spec) == MockDeliver 3f'' lines (spec formula over the committed entry)
        S6 = {'bc': bc, '_ds': bs['difficulty_state'], '_kd6': kd, 'INFO_LINES_S136': [], 'AMBER_NOTES': []}
        run_fence(snip("  # v5.94 (GAP-2026-11-07): delivered vs target counts", "  _notes6 = {}"), S6)
        check(f'H-DL {EXAM} S13-6: the chain AMBER lines reach AMBER_NOTES (DeliveryFooter §LADDER) verbatim',
              S6['AMBER_NOTES'] == list(_cf.get('amber') or []))
        st = _ent['difficulty_state']
        _ids11 = set((st.get('l2_model') or {}).get('scope_ids') or [])
        L11 = bc.difficulty_layer_lines(st.get('paper_gate'), st.get('l2_model'),
                                        n_l2_items=sum(1 for qq in _ent['questions'] if str(qq.get('subtopic_id')) in _ids11),
                                        shares_source=(st.get('l2_model') or {}).get('grades_source'))
        check(f'H-DL {EXAM} S13-6 footer lines == MockDeliver 3f\'\' lines (one formatter, one record)',
              S6['INFO_LINES_S136'] == L11 and any('Difficulty vs schedule' in x for x in L11)
              and (any('Organic difficulty ruler' in x for x in L11) == organic), str(L11)[:200])
        results[EXAM] = (M or {}).get('cuts_list')
    # the relative ruler is the exam's own: the two organic exams get different cut-offs
    check('H-DL relative cuts: a shallower exam\'s Hard is ITS top band, not the post-graduate exam\'s (owner D5)',
          results.get('PGX') and results.get('UGX') and results['PGX'] != results['UGX'], str(results))
    # Step 5 and Create hash the SAME profile file (the sha handshake is a path handshake)
    A = open(os.path.join(W, 'Framework_MockTestAnalyse.md'), encoding='utf-8').read()
    check('H-DL Analyse S11-1c and Create S3-8L hash the same file (/mnt/project/<EXAM>_difficulty_profile.json)',
          "_qi_path = f'/mnt/project/{exam_code}_difficulty_profile.json'" in A
          and "open(f'/mnt/project/{EXAM}_difficulty_profile.json', 'rb')" in S)


def _lb_swap_handshake(check, ROOT, run_fence, W):
    """H-LB v2.0 (release 2026.11.10, GAP-2026-11-10 G-10; LAW-ORG-3/4/5) — the spec's own S13-2L / S13-2R code on a
    6-item paper: an exact item is based measured_exact on its two fresh blind grades; an item measured ABOVE its slot
    is REPAIRED (never held); an exhausted slot is refilled from the verified RESERVE; another goes through a fresh
    REFILL SESSION and then the bounded LAST RESORT (delivered at the band it measured, one AMBER line, one P0
    incident). No swap, no paired upgrade, no forced / held label, no stop."""
    import blueprint_core as bc
    labs = ['Easy', 'Medium', 'Hard']
    S = open(os.path.join(W, 'Framework_MockTestCreate.md'), encoding='utf-8').read()
    def blk(tag):
        a = S.index(tag); b = S.index('  ```', a)
        return '\n'.join(l[2:] if l.startswith('  ') else l for l in S[a:b].split('\n'))
    HOME = ROOT + '/home/claude'; os.makedirs(HOME, exist_ok=True)
    EXAM = 'LBX'
    tp = {'1': 'Hard', '2': 'Medium', '3': 'Hard', '4': 'Medium', '5': 'Easy', '6': 'Hard'}
    meas = {'1': 'Medium', '2': 'Hard', '3': 'Medium', '4': 'Medium', '5': 'Easy', '6': 'Hard'}
    hashes = {q: f'h{q}' * 8 for q in tp}
    PK = {'grader_1': {'context': 'fresh', 'sha256': 'a' * 64}, 'grader_2': {'context': 'fresh', 'sha256': 'b' * 64}}
    def graded(e, b, h):                    # THE one writer (bc.op_record_controls), bound to the item's text
        return bc.op_record_controls(e, b, b, True, PK, item_hash=h, key_votes={'unanimous': True})
    cm = {q: graded({'subtopic_id': 'oc.a.b', 'difficulty': tp[q], 'qtype': 'mcq', 'difficulty_check': {'decision': 'dl_agree'},
                     'stem_text': f'stem {q}', 'option_texts': ['a', 'b', 'c', 'd'],
                     'review': {'key_agrees': True, 'confidence': 'high', 'reviewer': 'sub-agent', 'item_hash': hashes[q]}},
                    meas[q], hashes[q]) for q in tp}
    chains = {}
    for q in ('1', '3'):
        c = bc.slot_chain_new(q, 'difficulty', tp[q], 'oc.a.b')
        for _i in range(40):
            nx = bc.slot_chain_next(c, siblings=['oc.a.c', 'oc.a.d', 'oc.a.e'])
            c = nx['chain']
            if nx['action'] not in ('rework_dr1', 'rework_dr2', 'replace', 'shape', 'sibling'):
                break
            c = bc.slot_chain_record(c, nx['stage'], 'fail', sibling=nx['sibling'])
        chains[q] = c
    bs = {'paper_id': 'MOCK:M01', 'difficulty_plan_target': dict(tp), 'difficulty_plan': dict(tp), 'difficulty_labels': labs,
          'slot_chain': chains, 'difficulty_state': {'ruler': {'ruler_version': 'R1'}}}
    bp = {'subtopic_list': [{'subtopic_id': 'oc.a.b', 'topic': 'A', 'section': 'S'}]}
    P = {'bs': f'{HOME}/{EXAM}_M1_batch_state.json', 'kd': f'{HOME}/{EXAM}_M1_answer_key.json',
         'hj': f'{HOME}/{EXAM}_M1_item_hashes.json', 'bp': f'{HOME}/{EXAM}_bp.json', 'rs': f'{HOME}/{EXAM}_reserve.json'}
    # the verified reserve holds one Hard mcq item of this subtopic (it passed every control in an earlier attempt)
    rs_item = {'q': 'r1', 'difficulty': 'Hard', 'qtype': 'mcq', 'subtopic_id': 'oc.a.b', 'key_smiles': 'O=C1CCCCC1c1ccccc1',
               'difficulty_check': {'label_basis': {'kind': 'measured_exact'}}, 'key_votes': {'unanimous': True},
               'figures': [{'identity_ok': True, 'vision_ok': True, 'gates_ok': True}], 'clone_check': {'status': 'PASS'}}
    rsv, _okr, _ = bc.reserve_add(bc.reserve_new(EXAM), rs_item, 'R1', 'MOCK:M00')
    json.dump(rsv, open(P['rs'], 'w'))
    json.dump(bs, open(P['bs'], 'w')); json.dump({'concept_map': cm, 'answers': {q: 1 for q in tp}}, open(P['kd'], 'w'))
    json.dump(hashes, open(P['hj'], 'w')); json.dump(bp, open(P['bp'], 'w'))
    def l2l():
        try:
            run_fence(blk('  # ── S13-2L (v6.0) ──'), {'EXAM': EXAM, 'N': 1, 'BP_SRC_PATH': P['bp']}); return None
        except RuntimeError as x:
            return str(x)
    r1 = l2l()
    bs = json.load(open(P['bs'])); kd = json.load(open(P['kd'])); cmx = kd['concept_map']
    W1 = {w['q']: w['action'] for w in bs['slot_chain_work']}
    check('H-LB v2.0 S13-2L: an item graded EXACTLY at its slot by two fresh blind graders is based measured_exact (LAW-ORG-5)',
          all(bc.verify_difficulty_label(cmx[q], labs, strict=True) == (True, tp[q], 'measured_exact') for q in ('4', '5', '6')), str(r1)[:200])
    check('H-LB v2.0 S13-2L: an item measured ABOVE its slot is REPAIRED (a difficulty chain, rework DR1) — never held at the slot',
          bs['slot_chain']['2']['kind'] == 'difficulty' and W1.get('2') == 'rework_dr1'
          and not bc.verify_difficulty_label(cmx['2'], labs, strict=True)[0], str(W1))
    check('H-LB v2.0 S13-2L: an exhausted slot takes a VERIFIED RESERVE item at its exact band; another goes to a REFILL SESSION',
          W1.get('1') == 'reserve_refill' and W1.get('3') == 'refill_session' and r1 and 'SLOT-CHAIN' in r1
          and json.load(open(P['rs']))['items'] == [] and bs.get('refill_sessions_used') == 1, str((r1, W1))[:300])
    # S13-2R: the work is performed (the session's CLASS J work) and recorded by the spec's record block
    for w in bs['slot_chain_work']:
        w['status'] = 'done'
    json.dump(bs, open(P['bs'], 'w'))
    run_fence(blk('  # ── S13-2R record (v6.0) ──'), {'EXAM': EXAM, 'N': 1})
    bs = json.load(open(P['bs'])); kd = json.load(open(P['kd']))
    check('H-LB v2.0 S13-2R record: every attempt PENDING (resume-safe), old bases cleared (E10), entries recorded',
          all(bs['slot_chain'][q]['attempts'][-1]['outcome'] == 'pending' for q in ('1', '2', '3'))
          and all(w['status'] == 'recorded' for w in bs['slot_chain_work'])
          and 'label_basis' not in kd['concept_map']['1']['difficulty_check'])
    # the new texts are swept, DELTA-reviewed and freshly graded: Q1 (reserve item) and Q2 (rework) exact; Q3 still Medium
    for q, b in (('1', 'Hard'), ('2', 'Medium'), ('3', 'Medium')):
        hashes[q] = f'z{q}' * 32
        kd['concept_map'][q]['stem_text'] = f'stem {q} (new text)'      # the re-authored text, freshly graded
        kd['concept_map'][q] = graded(kd['concept_map'][q], b, hashes[q])
        kd['concept_map'][q]['review'] = dict(kd['concept_map'][q]['review'], item_hash=hashes[q])
    json.dump(hashes, open(P['hj'], 'w')); json.dump(kd, open(P['kd'], 'w'))
    r2 = l2l()
    bs = json.load(open(P['bs'])); kd = json.load(open(P['kd'])); cmx = kd['concept_map']
    check('H-LB v2.0 S13-2L: the reserve item and the rework both measure EXACTLY at their slots -> measured_exact; Q3 refills again',
          bs['slot_chain']['1'].get('outcome') == 'reserve_refill' and bs['slot_chain']['2'].get('outcome') == 'rework_dr1'
          and bc.verify_difficulty_label(cmx['1'], labs, strict=True) == (True, 'Hard', 'measured_exact')
          and bc.verify_difficulty_label(cmx['2'], labs, strict=True) == (True, 'Medium', 'measured_exact')
          and any(w['q'] == '3' and w['action'] == 'refill_session' for w in bs['slot_chain_work']), str((r2, bs['slot_chain'].get('3')))[:300])
    # every remaining refill session produces nothing usable: the per-paper budget runs out -> the bounded last resort
    _rs = []
    for _p in range(10):
        bs = json.load(open(P['bs'])); bs['slot_chain_work'] = []; json.dump(bs, open(P['bs'], 'w'))
        _rs.append(l2l())
        if _rs[-1] is None:
            break
    bs = json.load(open(P['bs'])); kd = json.load(open(P['kd'])); cmx = kd['concept_map']
    check('H-LB v2.0 S13-2L: after C_REFILL_SESSIONS the slot ends at the LAST RESORT — delivered at the band it MEASURED (Medium), '
          'never labelled Hard; one AMBER line + one P0 incident; the block then ends (no stop)',
          _rs[-1] is None and bs['slot_chain']['3'].get('outcome') == 'last_resort' and cmx['3']['difficulty'] == 'Medium'
          and bc.verify_difficulty_label(cmx['3'], labs, strict=True)[:3:2] == (True, 'last_resort')
          and bs.get('refill_sessions_used') == bc.C_REFILL_SESSIONS
          and any('Q3: last resort — requested Hard, delivered Medium' in x for x in bs['difficulty_state']['chain_footer']['amber'])
          and [i['slot'] for i in bs['difficulty_state']['incidents']] == ['3']
          and bs['difficulty_state']['paper_gate']['last_resort'] == [{'q': '3', 'requested': 'Hard', 'delivered': 'Medium'}]
          and bc.qindex_count_band(cmx['3'], labs) == 'Hard', str((_rs[-3:], bs['slot_chain']['3']))[:400])
    check('H-LB v2.0: no retired SC1 ending anywhere (forced / held / swap / upgrade / panel / re-key / majority / amber)',
          not any(c.get('outcome') in ('forced', 'held', 'band_swap', 'paired_upgrade', 'panel', 'rekey', 'majority', 'amber')
                  for c in bs['slot_chain'].values())
          and all(bc.verify_difficulty_label(cmx[q], labs, strict=True)[0] for q in cmx))
    # ── S13-2F sweep >= 4: the spec's own REPLACE slice (new chain / pending fail / disclosed skipped) ──
    _ls2 = S[S.index("        _repl = {q: r['gates'] for q, r in _route['items'].items() if r['route'] == 'REPLACE'}"):].split('\n')
    _sl = []
    for _l in _ls2:
        _sl.append(_l)
        if 'Never UNRESOLVED (OD-2026-11-09).")' in _l:
            break
    _slice = '\n'.join(l[8:] for l in _sl)
    cq = {'1': bc.slot_chain_finish(bc.slot_chain_new('1', 'quality', rule='SC1'), 'amber', gates=['A-OPTDISTINCT']),
          '2': bc.slot_chain_record(bc.slot_chain_new('2', 'dispute'), 'replace', 'pending')}
    json.dump({'difficulty_plan_target': {'1': 'Hard', '2': 'Hard', '3': 'Hard'}, 'slot_chain': cq}, open(P['bs'], 'w'))
    json.dump({'concept_map': {'1': {'quality_status': 'DISCLOSED(A-OPTDISTINCT)'}, '2': {}, '3': {'subtopic_id': 'oc.a.b'}}},
              open(P['kd'], 'w'))
    _stp_t = P['bs'] + '.s13'; json.dump({'sweep': 4}, open(_stp_t, 'w'))
    _route_t = {'items': {'1': {'gates': ['A-OPTDISTINCT'], 'route': 'REPLACE'}, '2': {'gates': ['A-REVIEW'], 'route': 'REPLACE'},
                          '3': {'gates': ['A-STEMFORM'], 'route': 'REPLACE'}}, 'paper': {}, 'stop': False}
    _gr = {'json': json, 'os': os, 'bc': bc, '_route': _route_t, '_key': P['kd'], '_bsp': P['bs'], '_stp': _stp_t, '_st': {'sweep': 4}}
    _rx = None
    try:
        exec(_slice, _gr)
    except RuntimeError as x:
        _rx = str(x)
    bsr = json.load(open(P['bs']))
    check('H-LB S13-2F sweep 4: a new finding opens a QUALITY chain, a pending dispute attempt FAILS, a DISCLOSED item is never re-opened',
          bsr['slot_chain']['3']['kind'] == 'quality' and bsr['slot_chain']['2']['attempts'][-1]['outcome'] == 'fail'
          and bsr['slot_chain']['1'].get('outcome') == 'amber' and _rx and "['2', '3']" in _rx and not os.path.exists(_stp_t),
          str((_rx, bsr['slot_chain'].get('1'))))
    # ── S13-4c: after INFRA_HEAL_MAX heals the stop is a real stop (never a recursion) ──
    _ls = S[S.index('  def _infra4c(site, msg):'):].split('\n')
    _body = [_ls[0]]
    for _l in _ls[1:]:
        if _l.strip() and (len(_l) - len(_l.lstrip())) <= 2:
            break                                                  # the function body ends at the block indentation
        _body.append(_l)
    _src = '\n'.join(l[2:] for l in _body)
    _g4c = {'json': json, 'os': os, 'bc': bc, '_bs4c_p': P['bs']}
    exec(_src, _g4c)
    _seen = []
    for _i in range(4):
        try:
            _g4c['_infra4c']('S13-4c-2', 'broken tool')
        except RuntimeError as x:
            _seen.append('heal' if 'INFRA-HEAL' in str(x) else 'other')
        except SystemExit:
            _seen.append('stop')
        except RecursionError:
            _seen.append('recursion')
    check('H-LB S13-4c: heal, heal, then a real STOP (no recursion, no counter reset)', _seen == ['heal', 'heal', 'stop', 'stop'], str(_seen))


def _downstream_replay(check):
    """H-DOWN (release 2026.11.09 pre-deploy review; v2.0: a LEGACY paper — its chains are SC1 records and its
    registry entry carries no 2026.11.10 framework_release, so every reader keeps the legacy verdicts, GAP §9):
    a paper written by Create v5.96 (a FORCED, two SWAP, a HELD,
    a DISCLOSED, a panel- and a majority-certified question) replayed through EVERY later reader: final_assembly
    commit, S13-QINDEX (pp.validate_question_index), the check-8 verifier on the committed rows, the auditor's
    registry-only A-REVIEW and DISCLOSED reconcile, MockDeliver 3f certification and its difficulty / slot-chain
    lines, Explain P10, Step 9's difficulty gate, Notes recall. Every step reads what the earlier one wrote."""
    import copy, io, contextlib
    import blueprint_core as bc, paper_pipeline as pp, audit_canonical as ac, notes_core as nc, final_assembly as fa
    L = ['Easy', 'Medium', 'Hard']
    obs_hard = {'qtype': 'mcq', 'question_class': 'C-COMPUTATIONAL', 'facets': ['C-COMPUTATIONAL'],
                'deduction_steps': 6, 'axiom_concepts': 3, 'speed_hack_exists': False, 'is_negative': False}
    obs_med = dict(obs_hard, deduction_steps=3, axiom_concepts=2)
    # exhausted difficulty chain -> forced
    ch = bc.slot_chain_new('1', 'difficulty', 'Hard', 'S.A.x', rule='SC1')
    while True:
        nx = bc.slot_chain_next(ch, siblings=['S.A.y', 'S.A.z', 'S.A.w'])
        ch = nx['chain']
        if nx['action'] == 'forced':
            break
        ch = bc.slot_chain_record(ch, nx['stage'], 'fail', sibling=nx['sibling'])
    fch = bc.slot_chain_finish(ch, 'forced', measured='Medium')
    # exhausted quality chain -> disclosed; exhausted dispute -> majority
    def exhaust(kind, last):
        c = bc.slot_chain_new('x', kind, rule='SC1')
        while True:
            nx = bc.slot_chain_next(c, siblings=['a', 'b', 'c'])
            c = nx['chain']
            if nx['action'] == last:
                return bc.slot_chain_finish(c, last)
            c = bc.slot_chain_record(c, nx['stage'], 'fail', sibling=nx['sibling'])
    qch = bc.slot_chain_compact(exhaust('quality', 'amber'))
    dch = bc.slot_chain_compact(exhaust('dispute', 'majority'))
    H = {str(q): f'h{q}' * 16 for q in range(1, 7)}
    rv = lambda q, ok=True: {'key_agrees': ok, 'confidence': 'high', 'reviewer': 'sub-agent', 'item_hash': H[q]}
    cm = {}
    cm['1'], _, _ = bc.dl_set_label_basis({'difficulty': 'Medium', 'qtype': 'mcq', 'difficulty_obs': obs_hard,
                                           'difficulty_check': {'decision': 'carried_below'}}, 'forced', L, 'Hard',
                                          controls={'reviewer': 'Medium'}, chain=fch)
    cm['2'], _, _ = bc.dl_set_label_basis({'difficulty': 'Hard', 'qtype': 'mcq', 'difficulty_obs': obs_med,
                                           'difficulty_check': {}}, 'review', L, 'Medium', controls={'reviewer': 'Medium'}, partner='3')
    cm['3'], _, _ = bc.dl_set_label_basis({'difficulty': 'Medium', 'qtype': 'mcq', 'difficulty_obs': obs_hard,
                                           'difficulty_check': {}}, 'review', L, 'Hard', controls={'reviewer': 'Hard'}, partner='2')
    cm['4'], _, _ = bc.dl_set_label_basis({'difficulty': 'Medium', 'qtype': 'mcq', 'difficulty_obs': obs_hard,
                                           'difficulty_check': {}}, 'held', L, 'Medium', controls={'measured': 'Hard'})
    cm['5'] = {'difficulty': 'Medium', 'qtype': 'mcq', 'difficulty_obs': obs_med, 'difficulty_check': {'decision': 'dl_agree', 'final_band': 'Medium'},
               'quality_status': 'DISCLOSED(A-OPTDISTINCT)', 'slot_chain': qch}
    cm['6'] = {'difficulty': 'Hard', 'qtype': 'mcq', 'difficulty_obs': obs_hard, 'difficulty_check': {'decision': 'dl_agree', 'final_band': 'Hard'}}
    for q in cm:
        cm[q].update({'subtopic_id': 'S.A.x', 'review': rv(q)})
        cm[q].setdefault('quality_status', 'CERTIFIED')
    cm['6']['review'] = dict(rv('6', False), certified_by='majority', chain=dch, agree=2, n=4)
    pan = [rv('2'), rv('2'), rv('2', False)]
    cm['2']['review'] = dict(rv('2'), certified_by='panel', panel=pan, agree=2, n=3)
    labels_by_q = {q: e['difficulty'] for q, e in cm.items()}
    check('H-DOWN schedule exact: Easy 0 / Medium 3 / Hard 3 (forced, swap, held never move a count)',
          bc.dl_band_counts(labels_by_q, L) == {'Easy': 0, 'Medium': 3, 'Hard': 3})
    for q, e in cm.items():
        v = bc.verify_difficulty_label(e, L)
        check(f'H-DOWN Q{q} label verified by the ONE verifier (basis {v[2]})', v[0], v)

    # commit through the real final_assembly (registry rows)
    BP = {'exam_code': 'EX', 'blueprint_version': 't', 'difficulty_labels': L,
          'subtopic_list': [{'subtopic_id': 'S.A.x', 'section': 'S', 'topic': 'A'}],
          'difficulty_schedule': [{'mock': 1, 'simple': 0, 'medium': 3, 'hard': 3}],
          'mocks': [{'mock': 1, 'sections': [{'section_name': 'S', 'q_range': [1, 6],
                     'subtopic_allocations': [{'subtopic_id': 'S.A.x', 'q_count': 6}]}]}], 'total_questions': 6}
    reg0 = {'exam_code': 'EX', 'schema_version': '1.0', 'mocks_completed': [], 'papers_completed': [], 'question_hashes': [],
            'stem_texts': [], 'semantic_tuples': [], 'semantic_usage': [], 'exhausted_subtopics': {}, 'question_index': [],
            'image_phashes': [], 'image_sources_used': [], 'session_log': [], 'content_tracking': {k: [] for k in fa._REQUIRED_CT},
            'section_names': [], 'rc_manifests': [], 'figural_manifests': [], 'di_manifests': []}
    tp = {'1': 'Hard', '2': 'Medium', '3': 'Hard', '4': 'Medium', '5': 'Medium', '6': 'Hard'}
    gate = bc.difficulty_paper_gate(bc.dl_gate_items(tp, cm, L), L)
    check('H-DOWN S13-2L paper gate PASS with forced / swapped / held listed', gate['status'] == 'PASS' and gate['forced'][0]['q'] == '1'
          and sorted(gate['swapped']) == ['2', '3'] and gate['held'] == ['4'], gate)
    ds = {'paper_gate': dict({k: gate.get(k) for k in ('status', 'counts_final', 'counts_original', 'rework_qs', 'accepted_dr3',
                                                       'unmeasured', 'forced', 'swapped', 'held', 'rule')}, target_plan=tp, labels=L),
          'chain_footer': bc.chain_footer_lines({'1': fch, '5': dict(qch, q='5'), '6': dict(dch, q='6')})}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            res = fa.commit_registry(copy.deepcopy(reg0), {}, BP, 1, paper_id='MOCK:M01', batches_completed=1,
                                     axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                                     concept_map=copy.deepcopy(cm), difficulty_state=ds)
        reg = res['registry']
        entry = reg['question_index'][0]
        # v2.0: this replays a paper DELIVERED by 2026.11.09 — its committed entry carries that release (GAP §9: never
        # re-certified retroactively); the stamp the v1.16 committer writes is set back to the paper's own release
        entry['qindex_cert']['framework_release'] = '2026.11.09'
        rows = {str(r['q']): r for r in entry['questions']}
        check('H-DOWN final_assembly commit carries difficulty_check (basis), review, quality_status and slot_chain (DISCLOSED)',
              rows['1']['difficulty_check'].get('dl_rung') == 'FORCED' and rows['5'].get('slot_chain', {}).get('outcome') == 'amber'
              and rows['2']['review'].get('certified_by') == 'panel' and rows['5']['quality_status'].startswith('DISCLOSED'),
              {q: list(r) for q, r in rows.items()})
    except Exception as x:
        check('H-DOWN final_assembly commit', False, repr(x)); return

    # A-QINDEX (both copies) on the committed registry
    okq, repq = pp.validate_question_index(reg, BP, mock_n=1)
    check('H-DOWN paper_pipeline.validate_question_index (post-commit S13-QINDEX) OK — check 6 exact, no stop', okq, repq.get('fails'))
    for r in entry['questions']:
        v = bc.verify_difficulty_label(r, L)
        check(f'H-DOWN registry row Q{r["q"]}: check-8 verifier OK on the COMMITTED row (basis {v[2]})', v[0], v)
    # auditor final phase on the REGISTRY ONLY (no sidecar) — A-REVIEW and the DISCLOSED reconcile
    ac._reset()
    src = {'registry': reg, '_mockN': 1, 'concept_map': {}, '_item_hashes': H}
    ac.gate_review(src, type('A', (), {'phase': 'final'})())
    lv = [(l, m) for l, c, m in ac.RESULTS if c == 'A-REVIEW']
    check('H-DOWN auditor A-REVIEW registry-only: panel re-derived, majority AMBER (WARN), never FAIL',
          [l for l, _ in lv] == ['WARN'] and 'majority' in lv[0][1], lv)
    ac._reset(); ac._item('A-OPTDISTINCT', '5', 'x'); ac._fail('A-OPTDISTINCT', 'ITEM DEFECT Q5')
    ac._lb_reconcile_disclosed(src)
    check('H-DOWN auditor DISCLOSED reconcile from the registry alone: FAIL -> AMBER WARN',
          [l for l, c, m in ac.RESULTS if c == 'A-OPTDISTINCT'] == ['WARN'] and ac.DISCLOSED_ITEMS == {'5'})
    # Deliver certification (3f)
    act, rec = bc.certificate_uncertified_active({str(r['q']): r.get('quality_status') for r in entry['questions']},
                                                 entry.get('quality_readiness'), (entry.get('qindex_cert') or {}).get('producer_release'))
    check('H-DOWN MockDeliver 3f: no uncertified item (DISCLOSED / forced / majority are disclosures) -> delivered with no flag',
          act == [] and bc.deliver_allowed({'uncertified_items': act})[0], act)
    # Deliver 3f'' / 3f''' lines
    dl = bc.difficulty_layer_lines(entry['difficulty_state']['paper_gate'])
    cf = entry['difficulty_state']['chain_footer']
    check("MockDeliver 3f'' difficulty lines name forced / swaps / held",
          any('schedule-forced' in x for x in dl) and any('band swaps' in x for x in dl) and any('held at slot' in x for x in dl), dl)
    check("MockDeliver 3f''' slot-chain AMBER lines: forced Q1, disclosed Q5, majority Q6",
          any(x.startswith('Q1: labelled Hard') for x in cf['amber']) and any(x.startswith('Q5:') for x in cf['amber'])
          and any(x.startswith('Q6: certified by majority') for x in cf['amber']), cf)
    # Explain P10 canonical-label check
    check('H-DOWN MockTestExplain P10: every committed label is canonical', all(r['difficulty'] in L for r in entry['questions']))
    # Step 9 difficulty gate (engine) never FAILS on these labels
    try:
        g9 = bc.evaluate_difficulty_gate({int(q): e['difficulty'] for q, e in cm.items()},
                                         {int(q): bc.verify_difficulty_obs(e['difficulty'], e['difficulty_obs'], L)[1] for q, e in cm.items()}, L)
        check('H-DOWN Step 9 difficulty gate evaluates the forced / swapped / held labels without raising (its write is PASSED or DISCLOSED, never FAILED)',
              isinstance(g9, dict) and 'verdict' in g9, g9)
    except Exception as x:
        check('H-DOWN Step 9 difficulty gate', False, repr(x))
    # Notes recall verifier (shares the one verifier)
    for q in ('4', '6'):
        r = nc.recall_verify_difficulty(cm[q]['difficulty'], cm[q]['difficulty_obs'], L)
        check(f'H-DOWN notes_core.recall_verify_difficulty Q{q} never raises (a Recall carries no basis -> obs rule)', isinstance(r, tuple) and len(r) == 3, r)


def _bv_handshake(check, ROOT, run_fence, W):
    """H-BV (release 2026.11.11, GAP-2026-11-11-BATCH-VERIFICATION): every question verified in its own batch, run
    through the REAL Create fences and every downstream reader — author packet (S4-7 STEP A) -> STEP A2 (fresh grader
    / solver jobs, decisions, one rewrite, settle) across two batches -> worker report GRADE_REQUEST / ROTATE (bootstrap)
    -> S13-2L settled rule -> S13-2F disclosure gates -> final_assembly.commit_registry -> paper_pipeline S13-QINDEX
    -> registry-row verifier -> auditor A-CONTENTLEVEL / A-QINDEX / NF disclosure -> paper gate -> MockDeliver 3f ->
    footer text. Every assertion names the producer and the consumer it binds."""
    import copy, io, contextlib
    import blueprint_core as bc, paper_pipeline as pp, audit_canonical as ac, final_assembly as fa, bootstrap as bsm
    L = ['Easy', 'Medium', 'Hard']
    MTC = os.path.join(W, 'Framework_MockTestCreate.md')
    txt = open(MTC, encoding='utf-8').read()
    def blk(marker):
        for _ln, body in fences(MTC, marker):
            return body
        raise AssertionError(f'fence {marker!r} not found')
    EXAM, N = 'HBV', 1
    HOME = ROOT + '/home/claude'
    os.makedirs(HOME, exist_ok=True)
    stems = {'1': 'Calculate the work done when 2.00 mol of an ideal gas expands isothermally at 300 K from 5.0 L to 20.0 L',
             '2': 'Identify the point group of the molecule ClF3',
             '3': 'The number of unpaired electrons in [Fe(CN)6]3- is',
             '4': 'Calculate the work done when 1.50 mol of an ideal gas expands isothermally at 350 K from 4.0 L to 16.0 L'}
    opts = {'1': ['-6.92 kJ', '-3.46 kJ', '+6.92 kJ', '-13.8 kJ'], '2': ['C2v', 'D3h', 'C3v', 'Td'],
            '3': ['one', 'three', 'five', 'zero'], '4': ['-6.05 kJ', '-1.21 kJ', '+6.05 kJ', '-12.1 kJ']}
    sid = {'1': 'PC.THERMO.work', '2': 'IN.SYM.pg', '3': 'IN.CFT.mag', '4': 'PC.THERMO.work'}
    tgt = {'1': 'Hard', '2': 'Medium', '3': 'Medium', '4': 'Hard'}
    cm = {q: {'stem_text': stems[q], 'option_texts': opts[q], 'subtopic_id': sid[q], 'qtype': 'mcq', 'difficulty': tgt[q]}
          for q in ('1', '2')}
    kp, bsp = f'{HOME}/{EXAM}_M{N}_answer_key.json', f'{HOME}/{EXAM}_M{N}_batch_state.json'
    json.dump({'concept_map': cm, 'answers': {'1': 1, '2': 1}}, open(kp, 'w'))
    json.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}, {'batch_id': 2, 'q_start': 3, 'q_end': 4}],
               'current_batch': 1, 'difficulty_labels': L, 'difficulty_plan_target': dict(tgt),
               'difficulty_mode': 'br1'}, open(bsp, 'w'))     # 2026.11.21: H-BV tests the BV/BR1 path (mode 'br1')
    # v2026.11.12: the ruler is built by the REAL engine from past records SHAPED LIKE A PRODUCTION PROFILE — no
    # blind grades, only the PYQExplain band (CSIR's 358 records): its anchors must carry CONTENT for every band
    prof = {'papers': {'P1': {'questions': {
        str(i): {'section': 'Part B', 'subtopic_id': sid_, 'qtype': 'mcq', 'band': b_, 'confidence': 'full',
                 'stem_snippet': f'past {b_} item {i} on {sid_}', 'inferential_steps': {'Easy': 1, 'Medium': 2, 'Hard': 4}[b_],
                 'ask_format': 'direct', 'named_concepts': ['x']}
        for i, (sid_, b_) in enumerate([(s_, b0) for s_ in ('PC.THERMO.work', 'IN.SYM.pg', 'IN.CFT.mag') for b0 in L], 1)}}}}
    ruler = bc.build_difficulty_ruler(prof, L, 't', 'm', 'p', '2026-11-12')
    check('H-BV ruler from a production-shaped profile (no blind grades): content-carrying anchors for EVERY band, '
          'basis disclosed', ruler.get('anchor_basis') == 'pyq_explain_band'
          and all(ruler['anchor_records'].get(b) for b in L) and bc.ruler_needs_recalibration({'anchors': ruler['anchors']})[0],
          {b: len(ruler['anchor_records'].get(b) or []) for b in L})
    G = {'EXAM': EXAM, 'N': N, 'EXAM_RULER': ruler, 'manifest': {}, 'EXEMPLAR_BANK': {}}
    # S4-7 STEP A author packet — the author holds the reviewers' anchors before writing
    run_fence(blk('# ── S4-7 STEP A author packet (v6.1 BV1) ──'), G)
    with contextlib.redirect_stdout(io.StringIO()):
        ap = G['BV_AUTHOR_PACKET'](1, 'PC.THERMO.work')
    check('H-BV S4-7 STEP A author packet carries the slot band and REAL past-question content of the same subtopic',
          ap.get('band') == 'Hard' and (ap.get('anchors') or {}).get('Hard')
          and ap['anchors']['Hard'][0].get('subtopic_id') == 'PC.THERMO.work' and ap['anchors']['Hard'][0].get('stem_snippet'), ap)
    # simulated FRESH reviewers: each reads packet.json only and answers for every question it carries
    grades = {'1': [['Hard', 'Hard', 'Hard']], '2': [['Medium', 'Easy', 'Medium']], '3': [['Medium', 'Medium', 'Medium']],
              '4': [['Medium', 'Medium', 'Medium']]}
    seen = {}
    def answer_jobs():
        bs = json.load(open(bsp))
        lines = []
        for jb in bs['bv']['jobs']:
            pk = json.load(open(os.path.join(jb['dir'], 'packet.json')))
            brief = open(os.path.join(jb['dir'], 'JOB_BRIEF.txt')).read()
            items_ = pk.get('items') or []
            blind = (all('difficulty' not in json.dumps(r.get('item', {})) for r in items_) and 'decisions_author' not in json.dumps(pk)
                     and 'rewrite_brief' not in json.dumps(pk) and jb['dir'] in brief and jb['role'].startswith('reviewer_'))
            anchored = all(all((r.get('exemplars') or {}).get(b) for b in L) for r in items_)
            seen.setdefault('blind', []).append(blind)
            seen.setdefault('anchored', []).append(anchored)
            k = int(jb['role'].rsplit('_', 1)[-1])
            out = {}
            for r in items_:
                q = r['q']
                n_ = seen.setdefault(('n', q, k), 0)
                seen[('n', q, k)] = n_ + 1
                g = grades[q][min(n_, len(grades[q]) - 1)]
                # 2026.11.13 (BV-10): the reviewer LISTS its moves and principles; the band is computed from them
                _cnt = {'Easy': (['C-FACTUAL'], 1, 1), 'Medium': (['C-COMPUTATIONAL'], 2, 1),
                        'Hard': (['C-COMPUTATIONAL'], 4, 2)}[g[k - 1]]
                out[q] = {'band': ('Easy' if g[k - 1] != 'Easy' else 'Hard'),     # the judged band is ignored
                          'facets': _cnt[0], 'moves': [f'm{i}' for i in range(_cnt[1])],
                          'principles': [f'p{i}' for i in range(_cnt[2])], 'speed_hack': False, 'shortcut': '',
                          'negative': False, 'decisions': 2, 'rationale': 'counted moves', 'class': 'computation',
                          'computation_generic': False, 'concept': 'c' + q,
                          'answer': json.load(open(kp))['answers'][q], 'confidence': 'high', 'assumptions': []}
            json.dump({'items': out}, open(os.path.join(jb['dir'], 'result.json'), 'w'))
            lines.append(jb['dir'] + ' REVIEW DONE')
        open(f'{HOME}/{EXAM}_M{N}_bv/returned.txt', 'a').write('\n'.join(lines) + '\n')
    step = blk('# ── S4-7 STEP A2 (v6.1 BV1) ──')
    def a2():
        with contextlib.redirect_stdout(io.StringIO()):
            run_fence(step, G)
        return G['BV_STEP']
    r = a2()
    check('H-BV STEP A2 round 1: at most 3 reviewer jobs for the WHOLE batch (was 4 jobs per question)',
          r['status'] == 'jobs_out' and [d.rsplit('/', 1)[-1] for d in r['jobs']] == ['reviewer_1', 'reviewer_2', 'reviewer_3'], r)
    # PLANNED HANDOVER (Orchestrate O3-3 v1.4.0): the worker refreshes the CHECKPOINT; the fresh worker restores it
    env = dict(os.environ, FW_HOME=HOME, FW_OUTPUTS=ROOT + '/mnt/user-data/outputs')
    import subprocess
    def ck(cmd):
        return subprocess.run([sys.executable, os.path.join(W, 'bootstrap.py'), '--checkpoint', cmd, '--exam', EXAM,
                               '--paper', str(N)], env=env, capture_output=True, text=True).returncode
    before = (open(kp).read(), open(bsp).read())
    rcs = (ck('make'), ck('restore'))
    check('H-BV planned handover: checkpoint refreshed then restored by the fresh worker — the batch in work is kept',
          rcs == (0, 0) and (open(kp).read(), open(bsp).read()) == before, rcs)
    answer_jobs(); r = a2()
    check('H-BV batch 1 DONE in ONE reviewer round: both questions settled at their slot (a 2-1 split is a majority, no tiebreak)',
          r['status'] == 'done' and r['settled'] == ['1', '2'] and r['disclosed'] == [] and r['open'] == [], r)
    _cm_r = json.load(open(kp))['concept_map']
    check('H-BV 2026.11.13 BV-10: the band is COMPUTED from the reviewers\' counts (the judged band is ignored) and the '
          'reviewer packet carries the PYQ counting rules',
          all((_cm_r[q].get('difficulty_check') or {}).get('measure') == 'rubric_r2' for q in ('1', '2'))
          and 'counting_rules' in json.load(open(f'{HOME}/{EXAM}_M{N}_bv/b1/r1/reviewer_1/packet.json'))
          and 'score' not in json.dumps(json.load(open(f'{HOME}/{EXAM}_M{N}_bv/b1/r1/reviewer_1/packet.json'))['items']),
          _cm_r.get('1'))
    # 2026.11.13 (GAP-2026-11-13-RUN-NOT-READ): what bootstrap --session-start RUNS is exactly what the read does NOT serve
    import spec_sections as _ssx
    _mtc = os.path.join(W, 'Framework_MockTestCreate.md')
    _eb = bsm.ns_engine_blocks(_mtc)
    _sec = json.load(open(os.path.join(W, 'SPEC_SECTIONS.json')))
    _er = _sec['files']['Framework_MockTestCreate.md']['engine_ranges']
    _rd = {j for a, b in _ssx.read_plan(_sec, 'Framework_MockTestCreate.md', 'NON-FINAL') for j in range(a, b + 1)}
    _rf = {j for a, b in _ssx.read_plan(_sec, 'Framework_MockTestCreate.md', 'FINAL') for j in range(a, b + 1)}
    check('H-NS bootstrap --session-start runs every ENGINE-RUN block and the read (NON-FINAL and FINAL) serves none of their code, only '
          'the marker line',
          len(_eb) == len(_er) >= 40 and all(a + 1 in _rd and a + 1 in _rf for a, _b in [(l, 0) for l, _s in _eb])
          and not any(j in _rd or j in _rf for a, b in _er for j in range(a, b + 1)))
    _ss_txt = '\n'.join(src for _l, src in _eb)
    check('H-NS the engine blocks are §3 / S0-OP and pure helper libraries: none is a model-agency (CLASS J) block and '
          'none is the S4-7 author packet or the S7-CONCEPT generator',
          'CLASS: J' not in _ss_txt and 'def BV_AUTHOR_PACKET' not in _ss_txt and 'def build_question' not in _ss_txt
          and 'def derive_scenario_from_pattern' not in _ss_txt)
    _wpt = bsm.WORKER_PROMPT if hasattr(bsm, 'WORKER_PROMPT') else ''
    _ctx = open(_mtc, encoding='utf-8').read()
    check('H-NS the worker prompt, Create S1-0R and bootstrap name the same two commands',
          'bootstrap.py --session-start' in _wpt and 'bootstrap.py --run-block' in _wpt and 'PYTHON SESSION (v6.3' in _ctx
          and '`python3 bootstrap.py --session-start --exam <ExamCode> --paper <N>' in _ctx
          and bsm.NS_ENGINE_MARK == _ssx.ENGINE_MARK)
    # bootstrap worker report: GRADE_REQUEST needs job folders; ROTATE carries the progress sha
    check('H-BV bootstrap WORKER_STATES carry GRADE_REQUEST and ROTATE (Orchestrate O2-3 / O3-9)',
          'GRADE_REQUEST' in bsm.WORKER_STATES and 'ROTATE' in bsm.WORKER_STATES and 'GRADE_REQUEST' in bsm.WORKER_STATES_NEED_PARTS)
    # batch 2: Q4 repeats settled Q1 -> Q4 is the one rewritten (Q1 untouched); after the rewrite it measures Medium -> settled
    bs = json.load(open(bsp)); bs['current_batch'] = 2; json.dump(bs, open(bsp, 'w'))
    kd = json.load(open(kp))
    for q in ('3', '4'):
        kd['concept_map'][q] = {'stem_text': stems[q], 'option_texts': opts[q], 'subtopic_id': sid[q], 'qtype': 'mcq', 'difficulty': tgt[q]}
    kd['answers'].update({'3': 1, '4': 1})
    json.dump(kd, open(kp, 'w'))
    r = a2()
    check('H-BV batch 2: a question repeating an earlier settled question is ITS one rewrite (the earlier one untouched)',
          r['rewrite'] == ['4'] and bc.verify_difficulty_label(json.load(open(kp))['concept_map']['1'], L, strict=True)[0], r)
    kd = json.load(open(kp))      # the rewrite, exactly as write_q_to_sidecar does it: the entry is REPLACED
    kd['concept_map']['4'] = {'stem_text': 'A gas obeys the van der Waals equation with a = 3.6 L2 bar mol-2; its Boyle temperature ratio to Tc is',
                              'option_texts': ['27/8', '8/27', '3', '1/3'], 'subtopic_id': sid['4'], 'qtype': 'mcq', 'difficulty': 'Hard'}
    json.dump(kd, open(kp, 'w'))
    # 2026.11.16 (BATCH-COMPLETE LAW-BC-2): a level miss climbs rung 1 (the fix above) and rung 2 (a REPLACE) inside its
    # batch, then settles at its measured band — the worker writes each rung's text exactly as write_q_to_sidecar does
    _rung2 = {'stem_text': 'For a van der Waals gas with b = 0.040 L mol-1, the excluded volume per molecule is closest to',
              'option_texts': ['6.6e-26 L', '1.7e-26 L', '2.7e-26 L', '4.0e-26 L'], 'subtopic_id': sid['4'], 'qtype': 'mcq',
              'difficulty': 'Hard'}
    _rewrites = 0
    for _ in range(8):
        r = a2()
        if r['status'] == 'jobs_out':
            answer_jobs()
            continue
        if r['status'] == 'rewrite' and r['rewrite'] == ['4'] and _rewrites == 0:
            kd = json.load(open(kp)); kd['concept_map']['4'] = dict(_rung2); json.dump(kd, open(kp, 'w'))
            _rewrites += 1
            continue
        break
    bs = json.load(open(bsp)); kd = json.load(open(kp)); cm = kd['concept_map']
    check('H-BV 2026.11.16 LAW-BC-1/2: batch 2 DONE with Q4 taken through rung 1 and rung 2 in its own batch — nothing carried',
          r['status'] == 'done' and r['pending'] == [] and r['settled'] == ['3', '4'] and bs['bv_carry'] == []
          # 2026.11.17 (C4): the step that asks for a rewrite writes no job, so Q3's first round and Q4's re-review
          # go out together — 2 rounds where 2026.11.16 needed 3
          and bs['bv']['round'] == 2 and _rewrites == 1 and bs['bv']['items']['4']['rung'] == 2,
          (r, bs['bv']['round'], _rewrites, bs['bv']['items']['4'].get('rung')))
    fin = blk('# ── S13-1B FINAL COUNTING ROUND (v6.4 BV-14) ──')
    def a2f():
        with contextlib.redirect_stdout(io.StringIO()):
            run_fence(fin, G)
        return G['BV_FINAL']
    rf = a2f()
    check('H-BV 2026.11.16 S13-1B (LEGACY: the settlement batch) has nothing to do when every batch settled: no job, no folder',
          rf['status'] == 'done' and rf['jobs'] == [] and 'DONE' in rf['lines'][-1]
          and not os.path.isdir(f'{HOME}/{EXAM}_M{N}_bv/bS'), rf)
    check('H-BV batch 2 DONE: Q3 at slot; Q4 delivered at its measured band after rung 2 (disclosed), never rung 3 for a level miss',
          r['disclosed'] == ['4'] and cm['4']['difficulty'] == 'Medium'
          and bs['bv']['items']['4']['attempt'] == 3 and bs['difficulty_state']['bv_disclosed']['4'] == {'requested': 'Hard', 'delivered': 'Medium'}, r)
    check('H-BV every reviewer packet was blind (no band, author counts or rewrite notes), named its own folder, '
          'and carried past-question anchors for every band', seen.get('blind') and all(seen['blind'])
          and seen.get('anchored') and all(seen['anchored']))
    labs = {q: bc.verify_difficulty_label(cm[q], L, strict=True) for q in cm}
    check('H-BV every label verifies STRICTLY (LB2: measured_exact / measured_majority)', all(v[0] for v in labs.values()), labs)
    # S13-2L settled rule (the spec's _strict_ok) and S13-2G phase-3 advisory rule (bc.LB2_KINDS)
    check('H-BV S13-2L opens no difficulty chain on a settled question (bc.bv_settled) and S13-2G keeps LB2 labels',
          bc.bv_settled(cm['4'], L) and 'measured_majority' in bc.LB2_KINDS
          and "bc.bv_settled(_cm_l.get(q), _labs_l)" in txt)
    # S13-2F disclosure set is exactly what the auditor can FAIL for composition (A-STEMFIG stays a repair)
    check('H-BV S13-2F NF_DISCLOSE_GATES are auditor gate ids (no dead id; A-STEMFIG is repaired, not disclosed)',
          set(bc.NF_DISCLOSE_GATES) <= set(ac.NF_GATE_IDS) | {'A-AXIS2'} and 'A-STEMFIG' not in bc.NF_DISCLOSE_GATES)
    # commit through the REAL final_assembly
    BP = {'exam_code': EXAM, 'blueprint_version': 't', 'difficulty_labels': L,
          'subtopic_list': [{'subtopic_id': s, 'section': s.split('.')[0], 'topic': s.split('.')[1]} for s in sorted(set(sid.values()))],
          'difficulty_schedule': [{'mock': 1, 'simple': 0, 'medium': 2, 'hard': 2}],
          'mocks': [{'mock': 1, 'sections': [{'section_name': 'Part A', 'q_range': [1, 4],
                     'subtopic_allocations': [{'subtopic_id': s, 'q_count': list(sid.values()).count(s)} for s in sorted(set(sid.values()))]}]}],
          'total_questions': 4}
    reg0 = {'exam_code': EXAM, 'schema_version': '1.0', 'mocks_completed': [], 'papers_completed': [], 'question_hashes': [],
            'stem_texts': [], 'semantic_tuples': [], 'semantic_usage': [], 'exhausted_subtopics': {}, 'question_index': [],
            'image_phashes': [], 'image_sources_used': [], 'session_log': [], 'content_tracking': {k: [] for k in fa._REQUIRED_CT},
            'section_names': [], 'rc_manifests': [], 'figural_manifests': [], 'di_manifests': []}
    nfd = {'A-AXIS2': 'Format parity: short Part A/Physical: match 1'}
    gate = bc.difficulty_paper_gate(bc.dl_gate_items(tgt, cm, L), L)
    check('H-BV S13-2L paper gate: PASS, the settled question listed (requested vs delivered), nothing below',
          gate['status'] == 'PASS' and [x['q'] for x in gate['last_resort']] == ['4'] and gate['below'] == [], gate)
    ds = dict(bs.get('difficulty_state') or {}, paper_gate=dict(gate, target_plan=tgt, labels=L))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            res = fa.commit_registry(copy.deepcopy(reg0), {}, BP, 1, paper_id='MOCK:M01', batches_completed=2,
                                     axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                                     concept_map=copy.deepcopy(cm), difficulty_state=ds, nf_disclosed=nfd,
                                     manifest_hash=bc.manifest_hash({}))
        reg = res['registry']; entry = reg['question_index'][0]
        rows = {str(x['q']): x for x in entry['questions']}
    except Exception as x:
        check('H-BV final_assembly commit', False, repr(x)); return
    check('H-BV final_assembly commits the BV label, grades and key votes on every row, and nf_disclosed + manifest_hash on the entry',
          all(rows[q].get('difficulty_check', {}).get('label_basis', {}).get('kind') in ('measured_exact', 'measured_majority') for q in rows)
          and all((rows[q].get('key_votes') or {}).get('unanimous') is True for q in rows)
          and entry.get('nf_disclosed') == nfd and entry.get('manifest_hash'), {q: sorted(r) for q, r in rows.items()})
    check('H-BV registry difficulty_state carries bv_disclosed for MockDeliver / footer',
          (entry.get('difficulty_state') or {}).get('bv_disclosed', {}).get('4', {}).get('delivered') == 'Medium')
    for q, row in rows.items():
        check(f'H-BV committed row Q{q}: strict check-8 verifier OK', bc.verify_difficulty_label(row, L, strict=True)[0])
    okq, repq = pp.validate_question_index(reg, BP, mock_n=1)
    check('H-BV paper_pipeline.validate_question_index (S13-QINDEX): check 6 exact — a settled row counts at its slot', okq, repq.get('fails'))
    ac._reset(); ac.gate_contentlevel({'concept_map': cm})
    check('H-BV auditor A-CONTENTLEVEL accepts every BV decision (no VOID_ITEM)',
          [l for l, c, m in ac.RESULTS if c == 'A-CONTENTLEVEL'] and all(l != 'FAIL' for l, c, m in ac.RESULTS if c == 'A-CONTENTLEVEL'),
          [(l, m[:120]) for l, c, m in ac.RESULTS if c == 'A-CONTENTLEVEL'])
    ac._reset(); ac.gate_qindex({'registry': reg, 'blueprint': BP, '_mockN': 1})
    _qx = [(l, m) for l, c, m in ac.RESULTS if c == 'A-QINDEX']
    check('H-BV auditor A-QINDEX on the committed registry: ARMED (not dormant) and no FAIL (checks 6 and 8 on BV rows)',
          _qx and all(l != 'FAIL' for l, m in _qx) and not any('dormant' in m for l, m in _qx), [(l, m[:200]) for l, m in _qx])
    ac._reset(); ac._nf_verdict('A-AXIS2', 'Format parity: short', {'registry': reg, '_mockN': 1, 'nf_disclosed': entry['nf_disclosed']})
    check('H-BV auditor: a disclosed composition gate is AMBER (WARN), never a FAIL', [l for l, c, m in ac.RESULTS if c == 'A-AXIS2'] == ['WARN'])
    act, _rec = bc.certificate_uncertified_active({q: r.get('quality_status') for q, r in rows.items()}, entry.get('quality_readiness'),
                                                  (entry.get('qindex_cert') or {}).get('producer_release'))
    check('H-BV MockDeliver 3f: nothing uncertified (a settled question is a disclosure) -> deliverable', act == [], act)
    fdt = open(os.path.join(W, 'Framework_DeliveryFooter.md'), encoding='utf-8').read()
    check('H-BV footer: Create S13-2L writes the exact AMBER line the DeliveryFooter contract names',
          'Difficulty after one rewrite: Q{_qb} delivered {_db.get(\'delivered\')} (slot {_db.get(\'requested\')})' in txt
          and 'Difficulty after one rewrite: Q<q> delivered <band> (slot <band>)' in fdt)
    orc = open(os.path.join(W, 'Framework_MockTestOrchestrate.md'), encoding='utf-8').read()
    wp = bsm.WORKER_PROMPT if hasattr(bsm, 'WORKER_PROMPT') else ''
    check('H-BV worker prompt (bootstrap): GRADE RETURNED is in the closed message set and every checkpoint is the one command',
          'GRADE RETURNED    (followed by one line per job folder' in wp and '--checkpoint make|restore|drop' in wp
          and 'PLANNED HANDOVER' in wp)
    check('H-BV Orchestrate: GRADE_REQUEST, GRADE RETURNED and ROTATE are handled (O2-3 / O2-5 / O3-9), and Create hands over to O3-9',
          all(s in orc for s in ('- GRADE_REQUEST (v1.3.0', '- ROTATE (v1.3.0)', '`FINAL ASSEMBLY` — goes to the CURRENT worker', '## O3-9',
                                    '- PLANNED HANDOVER (v1.4.0', '## O2-9 — No framework question', 'each wave in ONE message',
                                    '## O2-10 — WARM STANDBY', 'A MODEL\'S LIMIT IS NOT A WORKER FAULT'))
          and 'Framework_MockTestOrchestrate O3-9' in txt)



# ── H-BC BEGIN ── (GAP-2026-11-14-BATCH-COMPLETE §10.2; audit_sync TEST-NO-HANDWRITE guards this block: every grade, key
# vote, verdict and review record reaches the paper ONLY through result.json files in the job folders fa.bv_batch_step
# created and REVIEW DONE / ADJUDICATE DONE lines in returned.txt — never written by hand)
def _bc_handshake(check, ROOT, W):
    """H-BC (release 2026.11.16): every question SETTLED inside its batch, run through the REAL I/O shell
    (final_assembly.bv_batch_step -> blueprint_core.bc_apply), the STEP A3 binder, the S13-1 byte copy, the auditor's
    A-REVIEW / A-FIGRECORD / ESCALATED rules and the commit. Sub-agents are simulated by writing their result.json."""
    import io, contextlib
    import blueprint_core as bc, final_assembly as fa, audit_canonical as ac
    L = ['Easy', 'Medium', 'Hard']
    base = os.path.join(ROOT, 'hbc')

    def paper(name, cm, answers, target, plan, current=1, extra=None):
        home = os.path.join(base, name)
        os.makedirs(home, exist_ok=True)
        json.dump({'concept_map': cm, 'answers': answers}, open(os.path.join(home, 'HBC_M1_answer_key.json'), 'w'))
        bs = {'batch_plan': plan, 'current_batch': current, 'difficulty_labels': L, 'difficulty_plan_target': target,
              'difficulty_mode': 'br1'}            # 2026.11.21: the H-BC scenarios test the BC1 ladder in mode 'br1';
        bs.update(extra or {})                     # Cluster R3 scenarios pass extra={'difficulty_mode': ...}
        json.dump(bs, open(os.path.join(home, 'HBC_M1_batch_state.json'), 'w'))
        return home

    def ld(home, which):
        return json.load(open(os.path.join(home, f'HBC_M1_{which}.json')))

    def sv(home, which, d):
        json.dump(d, open(os.path.join(home, f'HBC_M1_{which}.json'), 'w'))

    def step(home, **kw):
        with contextlib.redirect_stdout(io.StringIO()):
            return fa.bv_batch_step('HBC', 1, home=home, echo=False, **kw)

    def answer(home, rev=None, adj=None, fail=()):
        """The fresh sub-agents of the round: rev(q, k, packet_row) -> reviewer item dict; adj(q, packet) -> verdict."""
        bs = ld(home, 'batch_state')
        lines = []
        for jb in bs['bv']['jobs']:
            pk = json.load(open(os.path.join(jb['dir'], 'packet.json')))
            if jb['role'] == 'adjudicator':
                if 'adj' in fail:
                    lines.append(jb['dir'] + ' ADJUDICATE FAILED x'); continue
                json.dump(adj(jb['q'], pk), open(os.path.join(jb['dir'], 'result.json'), 'w'))
                lines.append(jb['dir'] + ' ADJUDICATE DONE')
                continue
            k = int(jb['role'].rsplit('_', 1)[-1])
            if k in fail:
                lines.append(jb['dir'] + ' REVIEW FAILED x'); continue
            json.dump({'items': {r['q']: rev(r['q'], k, r) for r in pk['items']}},
                      open(os.path.join(jb['dir'], 'result.json'), 'w'))
            lines.append(jb['dir'] + ' REVIEW DONE')
        open(os.path.join(home, 'HBC_M1_bv', 'returned.txt'), 'a').write('\n'.join(lines) + '\n')
        return bs['bv']['jobs']

    def R(band, ans, **kw):
        cnt = {'Easy': (['C-FACTUAL'], 1, 1), 'Medium': (['C-COMPUTATIONAL'], 2, 1), 'Hard': (['C-COMPUTATIONAL'], 4, 2)}[band]
        d = {'band': band, 'facets': cnt[0], 'moves': [f'move {i}' for i in range(cnt[1])],
             'principles': [f'p{i}' for i in range(cnt[2])], 'speed_hack': False, 'shortcut': '', 'negative': False,
             'decisions': 2, 'rationale': 'counted', 'class': 'computation', 'computation_generic': False, 'concept': 'c',
             'answer': ans, 'confidence': 'high', 'assumptions': [], 'single_answer': 'yes',
             'leak_or_paraphrase': 'none', 'distractor_existence_and_class': '1: real species, wrong because x',
             'consistency_and_names': 'ok', 'selectivity_basis': 'clean'}
        d.update(kw)
        return d

    def Q(stem, opts, sid='S.T.u', **kw):
        e = {'stem_text': stem, 'option_texts': opts, 'subtopic_id': sid, 'qtype': 'mcq'}
        e.update(kw)
        return e

    plan1 = [{'batch_id': 1, 'q_start': 1, 'q_end': 2}]
    # H-BC-1 (K1, L1): all agree -> settled in one round; STEP A3 binds every question; A-REVIEW final OK
    h = paper('k1', {'1': Q('Compute the enthalpy change of reaction one at 298 K', ['-10 kJ', '-20 kJ', '-30 kJ', '-40 kJ']),
                     '2': Q('Name the point group of the second molecule in the scheme', ['C2v', 'D3h', 'Td', 'Oh'])},
              {'1': 2, '2': 1}, {'1': 'Hard', '2': 'Medium'}, plan1)
    r1 = step(h)
    answer(h, rev=lambda q, k, row: R({'1': 'Hard', '2': 'Medium'}[q], {'1': 2, '2': 1}[q]))
    r2 = step(h)
    kd = ld(h, 'answer_key'); cm = kd['concept_map']
    check('H-BC-1 three reviewer jobs, ONE round, every question settled unanimous (three solver answers)',
          r1['status'] == 'jobs_out' and len(r1['jobs']) == 3 and r2['status'] == 'done' and r2['settled'] == ['1', '2']
          and cm['1']['key_votes']['certified_by'] == 'unanimous' and cm['1']['key_votes']['solver_3'] == 2
          and bc.verify_difficulty_label(cm['2'], L, strict=True)[0], r2)
    hashes = {q: bc.item_hash([f'Q.{q}', cm[q]['stem_text']] + cm[q]['option_texts']) for q in cm}
    texts = {q: f"Q.{q} {cm[q]['stem_text']} " + ' '.join(f'{i}. {o}' for i, o in enumerate(cm[q]['option_texts'], 1)) for q in cm}
    json.dump(hashes, open(os.path.join(h, 'h.json'), 'w')); json.dump(texts, open(os.path.join(h, 't.json'), 'w'))
    with contextlib.redirect_stdout(io.StringIO()):
        b1 = fa.bc_bind_batch('HBC', 1, os.path.join(h, 'h.json'), os.path.join(h, 't.json'), home=h, echo=False)
    cm = ld(h, 'answer_key')['concept_map']
    check('H-BC-1 STEP A3 binds a batch review record (reviewer batch, unanimous) to every block hash',
          b1['status'] == 'bound' and b1['bound'] == ['1', '2'] and cm['1']['review']['item_hash'] == hashes['1']
          and cm['1']['review']['reviewer'] == 'batch' and cm['2']['review']['verdict'] == 'PASS', b1)
    src = {'concept_map': cm, 'answers': {'1': 2, '2': 1}, '_item_hashes': hashes, '_mockN': 1, 'registry': {'question_index': [
        {'mock': 1, 'paper_id': 'MOCK:M01', 'qindex_cert': {'producer_release': '2026.11.16', 'framework_release': '2026.11.16'},
         'questions': [{'q': 1}, {'q': 2}]}]}}
    ac._reset(); ac.gate_review(src)
    check('H-BC-1 auditor A-REVIEW final phase OK on the batch-bound records (no S13-2G)',
          [l for l, c, m in ac.RESULTS if c == 'A-REVIEW'] == ['OK'], [(l, m[:160]) for l, c, m in ac.RESULTS if c == 'A-REVIEW'])
    # H-BC-16b (R2): the docx block alone changed after binding (a picture swapped, the text untouched) -> refused
    json.dump(dict(hashes, **{'1': 'docx-only-edit'}), open(os.path.join(h, 'h_edit.json'), 'w'))
    with contextlib.redirect_stdout(io.StringIO()):
        b1e = fa.bc_bind_batch('HBC', 1, os.path.join(h, 'h_edit.json'), None, home=h, echo=False)
    check('H-BC-16b STEP A3 refuses a block changed in the docx alone after it was bound (its text unchanged)',
          b1e['status'] == 'refused' and list(b1e['refused']) == ['1'] and 'docx block changed' in b1e['refused']['1'], b1e)
    # H-BC-16 (R2): a question edited after its review is refused by STEP A3
    kd = ld(h, 'answer_key'); kd['concept_map']['2']['stem_text'] += ' (edited)'; sv(h, 'answer_key', kd)
    with contextlib.redirect_stdout(io.StringIO()):
        b2 = fa.bc_bind_batch('HBC', 1, os.path.join(h, 'h.json'), None, home=h, echo=False)
    check('H-BC-16 STEP A3 refuses a question whose text changed after its review (names it; binds the rest)',
          b2['status'] == 'refused' and list(b2['refused']) == ['2'] and 'changed after its review' in b2['refused']['2'], b2)
    # H-BC-2 (K2, L6, R12): 3 solvers against the author -> adjudicator job -> re-key; options swapped; grades kept
    h = paper('k2', {'1': Q('Which reagent converts the ketone to the alcohol here', ['NaBH4', 'KMnO4', 'PCC', 'O3'])},
              {'1': 2}, {'1': 'Hard'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    step(h); answer(h, rev=lambda q, k, row: R('Hard', 1))
    ra = step(h)
    _adj_dirs = [d for d in ra['jobs'] if d.endswith('_adj')]
    _apk = json.load(open(os.path.join(_adj_dirs[0], 'packet.json'))) if _adj_dirs else {}
    check('H-BC-2 a disputed key gets ONE adjudicator job (folder q<n>_adj) with the three anonymised solvers and no band',
          ra['status'] == 'jobs_out' and len(_adj_dirs) == 1 and [s['solver'] for s in _apk.get('solvers', [])] == ['A', 'B', 'C']
          and "'Hard'" not in json.dumps(_apk) and 'ADJUDICATE DONE' in open(os.path.join(_adj_dirs[0], 'JOB_BRIEF.txt')).read(), ra)
    answer(h, adj=lambda q, pk: {'verdict': 'solver_correct', 'correct_answer': 1, 'single_answer': 'yes',
                                 'missing_condition': '', 'reason': 'NaBH4 reduces the ketone', 'confidence': 'high'})
    rp = step(h)
    check('H-BC-2 re-key keeps the planned key position: PERMUTE options 2 and 1 (content unchanged, no new review)',
          rp['status'] == 'rewrite' and rp['permute'] == {'1': {'swap': [2, 1], 'answer': 2}} and rp['jobs'] == [], rp)
    kd = ld(h, 'answer_key'); o = kd['concept_map']['1']['option_texts']; o[0], o[1] = o[1], o[0]; sv(h, 'answer_key', kd)
    rs = step(h)
    kd = ld(h, 'answer_key'); e = kd['concept_map']['1']
    check('H-BC-2 after the swap: settled rekey, key = planned position 2 (now NaBH4), grades kept, no new round',
          rs['status'] == 'done' and rs['jobs'] == [] and e['key_votes']['certified_by'] == 'rekey'
          and kd['answers']['1'] == 2 and e['option_texts'][1] == 'NaBH4' and e['difficulty'] == 'Hard'
          and ld(h, 'batch_state')['bv']['round'] == 2, rs)
    # H-BC-3 (K3): a 2-1 split with the author -> adjudicator author_correct -> settled 'adjudicated'
    h = paper('k3', {'1': Q('Predict the major product of the E2 elimination of 2-bromobutane', ['1-butene', '2-butene', 'butane', 'butanol'])},
              {'1': 2}, {'1': 'Medium'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    step(h); answer(h, rev=lambda q, k, row: R('Medium', 1 if k == 3 else 2)); step(h)
    answer(h, adj=lambda q, pk: {'verdict': 'author_correct', 'correct_answer': 2, 'single_answer': 'yes',
                                 'missing_condition': '', 'reason': 'Zaitsev', 'confidence': 'high'})
    r3 = step(h)
    check('H-BC-3 K3: adjudicator confirms the author -> settled adjudicated',
          r3['status'] == 'done' and ld(h, 'answer_key')['concept_map']['1']['key_votes']['certified_by'] == 'adjudicated', r3)
    # H-BC-3R (Cluster R3; release 2026.11.22 — GAP-2026-11-17-FALLBACK-CASCADE): the same 2-1 split in mode 'counted',
    # the adjudicator confirming the key, SETTLES as is — one solver of three missing a question is how a Hard question
    # measures; 2026.11.21 rewrote it (D-AMBIGUOUS) and the live batch climbed every such question to the text fallback
    h = paper('k3r', {'1': Q('Predict the major product of the E2 elimination of 2-bromobutane', ['1-butene', '2-butene', 'butane', 'butanol'])},
              {'1': 2}, {'1': 'Medium'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], extra={'difficulty_mode': 'counted'})
    step(h); answer(h, rev=lambda q, k, row: R('Medium', 1 if k == 3 else 2)); step(h)
    answer(h, adj=lambda q, pk: {'verdict': 'author_correct', 'correct_answer': 2, 'single_answer': 'yes',
                                 'missing_condition': '', 'reason': 'Zaitsev', 'confidence': 'high'})
    r3r = step(h)
    _e3r = ld(h, 'answer_key')['concept_map']['1']
    check('H-BC-3R r3: a solver split settled by the adjudicator is settled as is (adjudicated, rung 0), never rewritten',
          r3r['status'] == 'done' and r3r['rewrite'] == [] and _e3r['key_votes']['certified_by'] == 'adjudicated'
          and (_e3r.get('bv') or {}).get('rung', 0) == 0, r3r)
    # H-BC-4 (K6): all answers agree but a decisive assumption -> adjudicator states the missing condition -> rung 1
    h = paper('k6', {'1': Q('The product of the reaction of the enolate with the alkyl halide is', ['A', 'B', 'C', 'D'])},
              {'1': 3}, {'1': 'Hard'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    step(h)
    answer(h, rev=lambda q, k, row: R('Hard', 3, assumptions=[{'about': 'conditions', 'text': 'kinetic enolate assumed',
                                                               'changes_answer': k == 1}]))
    step(h)
    answer(h, adj=lambda q, pk: {'verdict': 'question_defective', 'correct_answer': 3, 'single_answer': 'yes',
                                 'missing_condition': 'state LDA at -78 C (kinetic control)', 'reason': 'two enolates possible',
                                 'confidence': 'high'})
    r4 = step(h)
    _cb = ld(h, 'batch_state')['bv']['items']['1'].get('climb_brief') or {}
    check('H-BC-4 K6: a decisive assumption -> adjudicator -> REWRITE rung 1 FIX whose brief carries the missing condition '
          'and the solvers\' own moves', r4['status'] == 'rewrite' and r4['rewrite'] == ['1'] and _cb.get('kind') == 'fix'
          and _cb.get('missing_condition') == 'state LDA at -78 C (kinetic control)'
          and (_cb.get('solvers') or [{}])[0].get('moves'), _cb)
    # H-BC-5 (K7): a second defensible option named by a reviewer -> adjudicator confirms -> rung 1
    h = paper('k7', {'1': Q('Which statement about the SN1 reaction of the tertiary halide is true', ['w', 'x', 'y', 'z'])},
              {'1': 1}, {'1': 'Medium'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    step(h); answer(h, rev=lambda q, k, row: R('Medium', 1, single_answer='no: option 3 is also true' if k == 2 else 'yes'))
    r5a = step(h)
    answer(h, adj=lambda q, pk: {'verdict': 'question_defective', 'correct_answer': 1, 'single_answer': 'no: 3 also',
                                 'missing_condition': '', 'reason': 'two true statements', 'confidence': 'high'})
    r5 = step(h)
    check('H-BC-5 K7: second defensible option -> adjudicator -> rung 1', r5a['status'] == 'jobs_out'
          and r5['rewrite'] == ['1'] and ld(h, 'batch_state')['bv']['items']['1']['rung'] == 1, r5)
    # H-BC-7 / H-BC-8 (K13, K14): dispute through rungs 1 and 2, rung 3 also disputed -> the confirmed rung-1 version is
    # RESTORED (R5b), no new review, AMBER line
    h = paper('k13', {'1': Q('Identify the major product P of the epoxidation and reduction sequence', ['a', 'b', 'c', 'd'])},
              {'1': 1}, {'1': 'Hard'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    rung_text = {0: 'Identify the major product P of the epoxidation and reduction sequence',
                 1: 'Identify the major product P of the epoxidation and reduction sequence at -20 C with L-(+)-DET',
                 2: 'Identify the starting material of the given two-step sequence',
                 3: 'Which reagent reduces an epoxide regioselectively at the less hindered carbon'}
    ans_by_rung = {0: (2, 3, 4), 1: (1, 1, 2), 2: (2, 3, 4), 3: (2, 3, 4)}
    verdict_by_rung = {0: 'question_defective', 1: 'author_correct', 2: 'question_defective', 3: 'question_defective'}
    conf_by_rung = {0: 'high', 1: 'low', 2: 'high', 3: 'high'}
    rung = 0
    restore = None
    for _guard in range(16):
        r = step(h)
        if r['status'] == 'jobs_out':
            rr = rung
            answer(h, rev=lambda q, k, row: R('Hard', ans_by_rung[rr][k - 1]),
                   adj=lambda q, pk: {'verdict': verdict_by_rung[rr], 'correct_answer': 1, 'single_answer': 'yes',
                                      'missing_condition': '', 'reason': 'r', 'confidence': conf_by_rung[rr]})
            continue
        if r['status'] == 'rewrite' and r['rewrite'] == ['1']:
            rung = ld(h, 'batch_state')['bv']['items']['1']['rung']
            kd = ld(h, 'answer_key'); kd['concept_map']['1']['stem_text'] = rung_text[rung]; sv(h, 'answer_key', kd)
            continue
        if r['status'] == 'rewrite' and r['restore']:
            restore = json.load(open(r['restore']['1']))
            kd = ld(h, 'answer_key')
            kd['concept_map']['1'] = {k_: v_ for k_, v_ in restore['entry'].items()}
            kd['answers']['1'] = restore['answer']
            sv(h, 'answer_key', kd)
            continue
        break
    kd = ld(h, 'answer_key'); e = kd['concept_map']['1']; bsx = ld(h, 'batch_state')
    check('H-BC-7 the ladder: rung 1 FIX, rung 2 REPLACE, rung 3 FALLBACK — each text reviewed in the SAME batch',
          rung == 3 and bsx['bv']['round'] <= bc.BV_MAX_ROUNDS and r['status'] == 'done', (rung, r))
    check('H-BC-8 R5b: the last version with an adjudicator-confirmed key and >= 2 of 3 solvers (rung 1) is restored, '
          'disclosed AMBER, never re-reviewed', restore is not None and restore['rung'] == 1
          and e['stem_text'] == rung_text[1] and e['key_votes']['certified_by'] == 'disclosed'
          and any('R5b' in t for _c, t in bsx['bc_footer']['1']), (restore and restore.get('rung'), bsx.get('bc_footer')))
    # H-BC-9 (K10-K12, R6): a reviewer that returns nothing 3 times -> NO-MODEL (state saved, never a carry); resume asks again
    h = paper('k12', {'1': Q('Compute the pH of the 0.01 M acetic acid solution given its Ka', ['3.4', '2.0', '4.7', '7.0'])},
              {'1': 1}, {'1': 'Medium'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    sts = []
    for _ in range(5):
        r = step(h); sts.append(r['status'])
        if r['status'] != 'jobs_out':
            break
        answer(h, rev=lambda q, k, row: R('Medium', 1), fail=(1, 2, 3))
    bsx = ld(h, 'batch_state')
    check('H-BC-9 LAW-BC-9: no reviewer after 3 asks (2nd and 3rd on a switched model) -> NO-MODEL with saved state, '
          'nothing carried', sts == ['jobs_out'] * 3 + ['no_model'] and bsx['bv_carry'] == [] and bsx['bv']['status'] == 'no_model'
          and '1' in r['no_model'], sts)
    r = step(h)
    answer(h, rev=lambda q, k, row: R('Medium', 1), fail=(3,))
    for _ in range(8):
        r = step(h)
        if r['status'] != 'jobs_out':
            break
        answer(h, rev=lambda q, k, row: R('Medium', 1), fail=(3,),
               adj=lambda q, pk: {'verdict': 'author_correct', 'correct_answer': 1, 'single_answer': 'yes',
                                  'missing_condition': '', 'reason': 'ok', 'confidence': 'high'})
    bsx = ld(h, 'batch_state')
    check('H-BC-9 the resume asks again; with 2 of 3 reviewers the adjudicator settles the key, AMBER "2 of 3 reviewers"',
          r['status'] == 'done' and any('2 of 3 reviewers' in t for _c, t in bsx['bc_footer']['1']), (r, bsx.get('bc_footer')))
    # H-BC-12 (F6, R3): proven SMILES ride in reviewer and adjudicator packets, never for a figure the reviewer reads back
    fig = os.path.join(base, 'q1_problem.png')
    os.makedirs(base, exist_ok=True)
    open(fig, 'wb').write(b'\x89PNG\r\n\x1a\nfake')
    h = paper('f6', {'1': Q('Identify the product drawn in the scheme', ['a', 'b', 'c', 'd'], organic=True,
                            figure_files=[fig], figure_dicts=[{'file': fig, 'smiles': 'C[C@H](O)CC', 'stereo_mode': 'abs',
                                                               'answer_depends_on_stereo': True}])},
              {'1': 1}, {'1': 'Hard'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}])
    rf = step(h)
    pks = {d.rsplit('/', 1)[-1]: json.load(open(os.path.join(d, 'packet.json'))) for d in rf['jobs']}
    row = {k_: v_['items'][0] for k_, v_ in pks.items()}
    check('H-BC-12 LAW-BC-5: reviewers 1-2 read the figure back blind (no proven SMILES); reviewer 3 gets the proven SMILES',
          set(row) == {'reviewer_1', 'reviewer_2', 'reviewer_3'} and row['reviewer_1']['figures_to_read']
          and 'C[C@H](O)CC' not in json.dumps(pks['reviewer_1']) and 'C[C@H](O)CC' not in json.dumps(pks['reviewer_2'])
          and row['reviewer_3']['proven_structures'] == [{'file': 'q1_problem.png', 'smiles': 'C[C@H](O)CC'}],
          {k_: (v_.get('figures_to_read'), v_.get('proven_structures')) for k_, v_ in row.items()})
    # H-BC-13 (P2): the last batch's whole-paper sweep names an EARLIER question -> re-opened INSIDE the last batch
    h = paper('p2', {'1': Q('Compute the work done in the reversible isothermal expansion here', ['1', '2', '3', '4']),
                     '2': Q('Find the entropy change of the isothermal mixing of two gases', ['a', 'b', 'c', 'd'])},
              {'1': 1, '2': 2}, {'1': 'Medium', '2': 'Medium'},
              [{'batch_id': 1, 'q_start': 1, 'q_end': 1}, {'batch_id': 2, 'q_start': 2, 'q_end': 2}])
    step(h); answer(h, rev=lambda q, k, row: R('Medium', {'1': 1, '2': 2}[q])); step(h)
    bs = ld(h, 'batch_state'); bs['current_batch'] = 2; sv(h, 'batch_state', bs)
    step(h); answer(h, rev=lambda q, k, row: R('Medium', {'1': 1, '2': 2}[q])); rl = step(h)
    with contextlib.redirect_stdout(io.StringIO()):
        fa.bc_reopen('HBC', 1, ['1'], 'A-STEMLEAK: the stem names the product', home=h)
    rr = step(h)
    _it1 = ld(h, 'batch_state')['bv']['items']['1']
    check('H-BC-13 LAW-BC-6: an earlier question named by the last batch\'s sweep is re-opened in the last batch and climbs '
          'there (rung 1, with reviewers next), never repaired at Final Assembly',
          rl['status'] == 'done' and rr['status'] == 'rewrite' and rr['rewrite'] == ['1'] and _it1['rung'] == 1
          and 'GATE: A-STEMLEAK' in json.dumps(_it1.get('climb_brief')), rr)
    # H-BC-18 (migration): a 2026.11.15 paper paused between batches with a key_chain question in batch 1 — it joins
    # batch 2 and enters the ladder (adjudication on its current text)
    # the legacy state is produced by the 2026.11.15 engine itself (bc.bv_apply, rule BV1): attempt 2, the two blind
    # solvers against the author -> key_chain (exactly what that release left for S13-2L)
    _q1 = Q('Identify the major product of the Diels-Alder reaction shown', ['a', 'b', 'c', 'd'], subject='X', bv={'attempt': 2})
    _gx = lambda b, k: {'result': {'band': b}, 'sha256': f'g{k}', 'context': 'fresh'}
    _sx = lambda a, k: {'result': {'answer': a, 'confidence': 'high', 'assumptions': []}, 'sha256': f's{k}', 'context': 'fresh'}
    _leg = bc.bv_apply(_q1, 'Hard', L, {}, 1, results={'grader_1': _gx('Hard', 1), 'grader_2': _gx('Hard', 2),
                                                       'grader_3': _gx('Hard', 3), 'solver_1': _sx(2, 1), 'solver_2': _sx(2, 2)})
    _legacy_entry = _leg['entry']
    h = paper('mig', {'1': {k_: v_ for k_, v_ in _legacy_entry.items() if k_ != 'bv'},
                      '2': Q('Compute the bond order of the dioxygen cation', ['2.5', '2', '1.5', '3'])},
              {'1': 1, '2': 1}, {'1': 'Hard', '2': 'Medium'},
              [{'batch_id': 1, 'q_start': 1, 'q_end': 1}, {'batch_id': 2, 'q_start': 2, 'q_end': 2}], current=2,
              extra={'bv': {'batch': 1, 'round': 2, 'jobs': [], 'items': {'1': _legacy_entry['bv']}}})
    check('H-BC-18 fixture: the 2026.11.15 engine itself left Q1 in key_chain (no hand-built state)',
          _leg['action'] == 'key_chain' and _legacy_entry.get('bv_state') == 'key_chain', _leg['action'])
    rm = step(h)
    _pkm = {d.rsplit('/', 1)[-1]: [x['q'] for x in json.load(open(os.path.join(d, 'packet.json'))).get('items', [])]
            for d in rm['jobs']}
    check('H-BC-18 migration: a key_chain question of an earlier batch joins the next batch\'s work with rung 1 spent — '
          'its measured grades and two solver answers are kept, only the third solver is asked (then adjudication) — named '
          'in the report', rm['status'] == 'jobs_out' and _pkm.get('reviewer_3') == ['1', '2']
          and _pkm.get('reviewer_1') == ['2'] and ld(h, 'batch_state')['bv']['items']['1']['rung'] == 1
          and 'earlier questions in this batch' in rm['lines'][0], (rm['lines'], _pkm))
    # H-BC-18b (migration): a 2026.11.15 paper whose old Final Assembly chain rewrote a question (its key votes no longer
    # describe its text) and left a chain open — the SETTLEMENT BATCH measures that question again and closes the chain
    _q2 = Q('Compute the spin-only magnetic moment of the complex ion', ['1.73 BM', '2.83 BM', '3.87 BM', '4.90 BM'],
            subject='X', bv={'attempt': 1})
    _leg2 = bc.bv_apply(_q2, 'Medium', L, {}, 1, results={'grader_1': _gx('Medium', 1), 'grader_2': _gx('Medium', 2),
                                                          'grader_3': _gx('Medium', 3), 'solver_1': _sx(1, 1), 'solver_2': _sx(1, 2)})
    _e2 = {k_: v_ for k_, v_ in _leg2['entry'].items() if k_ != 'bv'}
    _e2['stem_text'] = 'Compute the spin-only magnetic moment of the high-spin d6 complex ion'   # the old chain's rewrite
    h = paper('mig2', {'1': _e2}, {'1': 1}, {'1': 'Medium'}, [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], current=2,
              extra={'bv': {'batch': 1, 'round': 1, 'jobs': [], 'items': {'1': _leg2['entry']['bv']}},
                     'slot_chain': {'1': {'kind': 'quality', 'done': False, 'attempts': []}}})
    for _ in range(4):
        rmf = step(h, final=True)
        if rmf['status'] != 'jobs_out':
            break
        answer(h, rev=lambda q, k, row: R('Medium', 1))
    _bsm = ld(h, 'batch_state')
    check('H-BC-18b settlement batch: a legacy question rewritten after its key votes is reviewed again (BC1), and every '
          'open legacy chain is closed as migrated', _leg2['action'] == 'settled' and rmf['status'] == 'done'
          and _bsm['bv']['items']['1'].get('rule') == bc.BC_RULE and _bsm['slot_chain']['1']['outcome'] == 'migrated'
          and _bsm['slot_chain']['1']['done'] is True, (rmf, _bsm.get('slot_chain')))
    # H-BC-15 (6.6, LAW-BC-8): Final Assembly from a settled paper — byte copy, bound hashes equal, zero job folders
    h = os.path.join(base, 'k1')
    out = os.path.join(base, 'out'); os.makedirs(out, exist_ok=True)
    cum = os.path.join(out, 'HBC_SUBJ_X_01_Q1to2.docx'); open(cum, 'wb').write(b'PK\x03\x04 cumulative docx bytes')
    kd = ld(h, 'answer_key'); kd['concept_map']['2']['stem_text'] = kd['concept_map']['2']['stem_text'].replace(' (edited)', '')
    sv(h, 'answer_key', kd)
    jobs_before = sorted(os.listdir(os.path.join(h, 'HBC_M1_bv', 'b1')))
    asm = fa.assemble_final_docx(cum, os.path.join(out, 'HBC_SUBJ_X_01_Create.docx'))
    with contextlib.redirect_stdout(io.StringIO()):
        fa.bc_bind_batch('HBC', 1, os.path.join(h, 'h.json'), None, home=h, echo=False)
    chk = fa.bc_check_bound('HBC', 1, os.path.join(h, 'h.json'), home=h)
    json.dump(dict(hashes, **{'2': 'different'}), open(os.path.join(h, 'h2.json'), 'w'))
    chk2 = fa.bc_check_bound('HBC', 1, os.path.join(h, 'h2.json'), home=h)
    _kdk = ld(h, 'answer_key'); _kdk['answers']['1'] = 4; sv(h, 'answer_key', _kdk)
    chk3 = fa.bc_check_bound('HBC', 1, os.path.join(h, 'h.json'), home=h)
    _kdk['answers']['1'] = 2; sv(h, 'answer_key', _kdk)
    check('H-BC-15 S13-1 ASSEMBLE: a byte copy (sha equal), every review bound to the final hash, a changed block is an '
          'INFRA mismatch (never a re-review), and Final Assembly created no job folder',
          asm['ok'] and open(cum, 'rb').read() == open(os.path.join(out, 'HBC_SUBJ_X_01_Create.docx'), 'rb').read()
          and chk['ok'] and chk2['mismatch'] == ['2'] and chk3['key_mismatch'] == ['1'] and not chk3['ok']
          and sorted(os.listdir(os.path.join(h, 'HBC_M1_bv', 'b1'))) == jobs_before, (asm, chk, chk2, chk3))
    # H-BC-17 (R9, LAW-BC-8): an item finding first seen at Final Assembly is stamped ESCALATED -> AMBER, never repaired
    cm17 = ld(h, 'answer_key')['concept_map']
    cm17['1']['quality_status'] = 'ESCALATED(A-STEMLEAK)'
    ac._reset()
    ac._item('A-STEMLEAK', '1', 'A-STEMLEAK: the stem names the product', 'VOID_ITEM')
    ac._fail('A-STEMLEAK', 'stem leak on Q1')
    ac._lb_reconcile_disclosed({'concept_map': cm17, 'registry': {}})
    check('H-BC-17 LAW-BC-8: an ESCALATED item on a BATCH-COMPLETE paper turns its FAIL into AMBER (P0 recorded by S13-2F)',
          [l for l, c, m in ac.RESULTS if c == 'A-STEMLEAK'] == ['WARN'] and '1' in ac.DISCLOSED_ITEMS
          and 'ESCALATED' in [m for l, c, m in ac.RESULTS if c == 'A-STEMLEAK'][0], ac.RESULTS[-2:])
    # H-BC-20 (K16-K18, L8): an exam with no difficulty plan, MSQ and NAT — the same flow settles every question
    h = paper('k18', {'1': Q('Select every aromatic compound among the four listed', ['benzene', 'cyclohexene', 'pyridine', 'hexane'],
                             qtype='msq'),
                      '2': Q('Compute the molar mass of glucose to one decimal place', [], qtype='nat', ca_range=[179.9, 180.3])},
              {'1': ['1', '3'], '2': 180.1}, {}, plan1)
    step(h)
    answer(h, rev=lambda q, k, row: R('Medium', {'1': '3, 1' if k == 2 else [1, 3], '2': [180.1, 180.2, 180.0][k - 1]}[q]))
    r20 = step(h)
    check('H-BC-20 no difficulty plan, MSQ and NAT (tolerance) through the same flow: settled, no label written',
          r20['status'] == 'done' and r20['settled'] == ['1', '2']
          and 'difficulty_check' not in ld(h, 'answer_key')['concept_map']['2'], r20)
    # H-BC-11 (F4): a structure picture without its figure_dicts record fails A-FIGRECORD on a BATCH-COMPLETE paper
    ac._reset(); ac.gate_figrecord({'concept_map': {'1': {'organic': True, 'figure_files': ['x.png'], 'key_votes': {'rule': 'BC1'}}}})
    check('H-BC-11 A-FIGRECORD (Layer-2 twin of G-FIGRECORD) fails a structure picture without its record',
          [l for l, c, m in ac.RESULTS if c == 'A-FIGRECORD'] == ['FAIL'])
    # spec / engine / orchestration agree on the new path
    mtc = open(os.path.join(W, 'Framework_MockTestCreate.md'), encoding='utf-8').read()
    orc = open(os.path.join(W, 'Framework_MockTestOrchestrate.md'), encoding='utf-8').read()
    check('H-BC spec: S0-BC laws, STEP A3 binder, S13-1 byte copy and S13-2L.0 gate are wired; Orchestrate handles _adj',
          '## S0-BC — BATCH-COMPLETE' in mtc and 'fa.bc_bind_batch(' in mtc and 'fa.assemble_final_docx(' in mtc
          and 'RUN-BLOCK S13-2L.0' in mtc and '`_adj`' in orc and 'ADJUDICATE DONE' in orc
          and bc.BV_ROLES_SOLVE == ('solver_1', 'solver_2', 'solver_3') and bc.BC_TERMINAL == 'adjudicated_disclosed')
# ── H-BC END ──


# ── H-R3 BEGIN ── (release 2026.11.21, GAP-2026-11-16-DIFFICULTY-YARDSTICK; like H-BC, every grade and review record
# reaches the paper ONLY through result.json files in the job folders fa.bv_batch_step created and REVIEW DONE /
# ADJUDICATE DONE lines in returned.txt — never written by hand)
def _r3_handshake(check, ROOT, run_fence, W):
    """H-R3: the difficulty yardstick as ONE chain. Step 5 engine (analyse_engine.ladder_row / ladder_prepare /
    ladder_merge, rankings through the job folders) -> [Exam]_difficulty_ladder.json -> SESSION_BUDGET staging ->
    Create S3-2 mode freeze (bc.r3_mode) -> S4-7 STEP A author packet fence (ladder mode) -> STEP A2 fence (rank
    tasks, defect codes, PRE-REVIEW gates, one writer fix) -> RUN-BLOCK S13-2L.0 (footer lines) ->
    final_assembly.commit_registry -> paper_pipeline S13-QINDEX -> auditor A-CONTENTLEVEL / A-QINDEX / A-CLASSMIX ->
    DeliveryFooter §2R wording. Every assertion names the producer and the consumer it binds."""
    import copy, io, contextlib, fnmatch, random
    import blueprint_core as bc, analyse_engine as ae, final_assembly as fa, paper_pipeline as pp, audit_canonical as ac
    L = ['Easy', 'Medium', 'Hard']
    MTC = os.path.join(W, 'Framework_MockTestCreate.md')
    def blk(marker):
        for _ln, body in fences(MTC, marker):
            return body
        raise AssertionError(f'fence {marker!r} not found')
    EXAM, N = 'HR3', 1
    HOME = ROOT + '/home/claude'
    os.makedirs(HOME, exist_ok=True)
    rng = random.Random(21)
    # ── Step 5: 120 past questions of one subject, latent difficulty known; the 4-mark part is harder on average ──
    truth, rows = {}, []
    for i in range(120):
        d = rng.gauss(0, 1)
        truth[f'P1:Q{i + 1}'] = d
        rec = {'subtopic_id': f'oc.t{i % 3}.u{i % 5}', 'marks': 4 if d > -0.2 else 2, 'ask_format': 'direct',
               'has_figure': i % 4 == 0, 'decisions': ['concept_chain'] if d > 0.5 else ['specific_knowledge'],
               'content_objects': [{'role': 'problem', 'kind': 'STRUCTURE', 'canonical': 'C' * (4 + max(0, int(6 + 3 * d)))}]}
        pk = {'key': f'P1:Q{i + 1}', 'stem': f'Past question {i + 1}: which product forms', 'options': ['a', 'b', 'c', 'd']}
        rows.append(ae.ladder_row(pk, rec))
    check('H-R3 Step 5 ladder rows: what a candidate sees plus abstract features — never a band, count or key',
          len(rows) == 120 and all(r['text'] and not ({'band', 'score', 'key', 'answer'} & set(r)) for r in rows)
          and sum(1 for r in rows if r['content']) == 120)
    with contextlib.redirect_stdout(io.StringIO()):
        st = ae.ladder_prepare(EXAM, rows, L, home=HOME)
    q = json.load(open(f'{HOME}/{EXAM}_ladder/queue.json'))
    for jb in q['jobs']:                                  # fresh rankers: read packet.json only, write result.json
        pk = json.load(open(os.path.join(jb['dir'], 'packet.json')))
        brief = open(os.path.join(jb['dir'], 'JOB_BRIEF.txt')).read()
        assert jb['dir'] in brief and 'P1:Q' not in json.dumps(pk)
        res = {'rankings': {p['pid']: [it['label'] for it in sorted(p['items'], key=lambda it, m=jb['map'][p['pid']]:
                                                                       truth[m[it['label']]] + rng.gauss(0, 0.5))]
                            for p in pk['packets']}}
        json.dump(res, open(os.path.join(jb['dir'], 'result.json'), 'w'))
    mg = ae.ladder_merge(EXAM, home=HOME)
    lad = json.load(open(mg['path']))
    check('H-R3 Step 5 S11-1d: ranking jobs through job folders (no past-question id reaches a ranker) -> ladder OK',
          st['status'] == 'pending' and st['jobs'] > 0 and mg['status'] == 'ok' and bc.validate_ladder(lad) == []
          and mg['path'] == f'{HOME}/{EXAM}_difficulty_ladder.json', (st, mg.get('status'), mg.get('sanity')))
    sb = json.load(open(os.path.join(W, 'SESSION_BUDGET.json')))
    check('H-R3 SESSION_BUDGET stages the ladder run file for TestCreate and MockCreate (pattern matches the Step 5 name)',
          all(any(fnmatch.fnmatch(f'{EXAM}_difficulty_ladder.json', p) for p in sb['project_inputs'][t])
              for t in ('TestCreate', 'MockCreate')))
    check('H-R3 fa.bv_load_ladder reads exactly the file Step 5 wrote', fa.bv_load_ladder(EXAM, HOME) == lad)
    _lad2 = json.loads(json.dumps(lad)); _sc2 = next(iter(_lad2['scopes'].values())); _k2 = next(iter(_sc2['positions']))
    _fp1 = bc.ld_fingerprint(json.loads(json.dumps(lad))); _sc2['positions'][_k2] = _sc2['positions'][_k2] + 0.5
    check('H-R3 bc.ld_fingerprint: unchanged by a JSON round trip, changed when one ladder position moves (the per-paper '
          'freeze of Create S3-2e / bv_batch_step)', _fp1 == bc.ld_fingerprint(lad) and _fp1 != bc.ld_fingerprint(_lad2)
          and bc.ld_fingerprint(None) is None, (_fp1, bc.ld_fingerprint(_lad2)))
    _mtc_txt = open(MTC, encoding='utf-8').read()
    check('H-R3 Create S3-2e freezes the ladder per paper: a NEW paper loads the attached ladder first, a paper in '
          'progress its staged copy; batch_state records the fingerprint', 'fresh_first=_ld_inprog is None' in _mtc_txt
          and "'ladder_fingerprint'" in _mtc_txt and fa.bv_load_ladder(EXAM, HOME, fresh_first=False) == lad)
    _rows2 = [dict(r, id=r['id'].replace('P1:', 'P2:')) for r in rows]
    with contextlib.redirect_stdout(io.StringIO()):
        _st2 = ae.ladder_prepare(EXAM + 'Z', _rows2, L, home=HOME)
        _mg2 = ae.ladder_merge(EXAM + 'Z', home=HOME)
    check('H-R3 Step 5 phase C with no ranking returned writes NO ladder (Step 7 then runs rule r2.1, disclosed)',
          _st2['status'] == 'pending' and _mg2['status'] == 'none' and _mg2['path'] is None
          and not os.path.exists(f'{HOME}/{EXAM}Z_difficulty_ladder.json'), (_st2, _mg2))
    # ── Create: S3-2 mode freeze, then the author packet fence ──
    tgt = {'1': 'Hard', '2': 'Hard', '3': 'Hard', '4': 'Easy'}
    kp, bsp = f'{HOME}/{EXAM}_M{N}_answer_key.json', f'{HOME}/{EXAM}_M{N}_batch_state.json'
    mode = bc.r3_mode({}, lad, {})
    json.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 4}], 'current_batch': 1, 'difficulty_labels': L,
               'difficulty_plan_target': dict(tgt), 'difficulty_mode': mode}, open(bsp, 'w'))
    check('H-R3 Create S3-2 freezes difficulty_mode = ladder (bc.r3_mode) and fa.bv_difficulty_mode keeps it',
          mode == 'ladder' and fa.bv_difficulty_mode(json.load(open(bsp)), None) == 'ladder')
    G = {'EXAM': EXAM, 'N': N, 'LADDER': lad, 'EXAM_RULER': {}, 'manifest': {}, 'EXEMPLAR_BANK': {}}
    run_fence(blk('# ── S4-7 STEP A author packet (v6.1 BV1) ──'), G)
    with contextlib.redirect_stdout(io.StringIO()):
        ap = G['BV_AUTHOR_PACKET'](1, 'oc.t1.u1')
    _apt = json.dumps(ap)
    check('H-R3 S4-7 STEP A (ladder mode): level in words, levers, archetype cards, content floor — no score, count '
          'target, offset or grading anchor', ap.get('mode') == 'ladder' and ap.get('levers') and ap.get('archetype_cards')
          and ap.get('content_floor') and 'score' not in _apt.lower() and 'aim one point' not in _apt
          and not any(a in _apt for a in lad['scopes'][bc.ld_scope_for(lad, None, 'oc.t1.u1')]['grading']), ap)
    # ── STEP A2: four questions; Q3 has a dead row and is fixed by the writer when sent back ──
    dead = ['A-III, B-I, C-II, D-IV', 'A-II, B-I, C-III, D-IV', 'A-III, B-II, C-I, D-IV', 'A-I, B-III, C-II, D-IV']
    fixed = ['A-III, B-I, C-II, D-IV', 'A-II, B-I, C-IV, D-III', 'A-III, B-II, C-I, D-IV', 'A-IV, B-III, C-II, D-I']
    true_p = {'1': 0.93, '2': 0.60, '3': 0.95, '4': 0.20}
    stems = {'1': 'Identify the major product when 2-bromo-2-methylbutane is heated with ethanolic potassium tert-butoxide',
             '2': 'Which reagent converts benzaldehyde into cinnamic acid in one step under the conditions given',
             '3': 'Match each named reaction in List-I with the key intermediate it proceeds through in List-II',
             '4': 'The hybridisation of the carbonyl carbon atom in propanone is'}
    opts = {'1': ['2-methylbut-1-ene', '2-methylbut-2-ene', '3-methylbut-1-ene', 'pentan-2-ol'],
            '2': ['acetic anhydride and sodium acetate', 'malonic acid and pyridine', 'acetone and NaOH', 'HCN then hydrolysis'],
            '3': dead, '4': ['sp3', 'sp2', 'sp', 'dsp2']}
    cm = {q: {'stem_text': stems[q], 'subtopic_id': 'oc.t1.u1', 'qtype': 'mcq', 'ask_format': 'direct',
              'difficulty': tgt[q], 'option_texts': list(opts[q])} for q in tgt}
    json.dump({'concept_map': cm, 'answers': {q: 1 for q in tgt}}, open(kp, 'w'))
    seen = {'blind': [], 'tasks': []}
    def answer_jobs():
        bs = json.load(open(bsp)); lines = []
        for jb in bs['bv']['jobs']:
            pk = json.load(open(os.path.join(jb['dir'], 'packet.json')))
            if jb['role'] == 'adjudicator':
                json.dump({'verdict': 'author_correct', 'correct_answer': 1, 'single_answer': 'yes', 'missing_condition': '',
                           'reason': 'r', 'confidence': 'high'}, open(os.path.join(jb['dir'], 'result.json'), 'w'))
                lines.append(jb['dir'] + ' ADJUDICATE DONE'); continue
            seen['blind'].append('difficulty' not in json.dumps([r.get('item') for r in pk['items']])
                                 and 'exemplars' not in json.dumps(pk) and 'band_guide' not in pk)
            out = {}
            for r in pk['items']:
                qq = r['q']; tk = (jb.get('tasks') or {}).get(qq)
                seen['tasks'].append(r.get('task'))
                rec = {'answer': 1, 'confidence': 'high', 'assumptions': [], 'single_answer': 'yes', 'defects': [],
                       'depth': 3, 'breadth': 1, 'class': 'conceptual', 'concept': 'c' + qq,
                       'decisive_fact': {'entities': [f'species {qq}'], 'property': 'major product'}}
                if tk:
                    rec['ranking'] = sorted(tk['map'], key=lambda lb, t=tk, x=qq: (true_p[x] if t['map'][lb] == 'ITEM'
                                                                                   else t['meta'][t['map'][lb]]['p']) + rng.gauss(0, 0.03))
                out[qq] = rec
            json.dump({'items': out}, open(os.path.join(jb['dir'], 'result.json'), 'w'))
            lines.append(jb['dir'] + ' REVIEW DONE')
        open(f'{HOME}/{EXAM}_M{N}_bv/returned.txt', 'a').write('\n'.join(lines) + '\n')
    step = blk('# ── S4-7 STEP A2 (v6.1 BV1) ──')
    def a2():
        with contextlib.redirect_stdout(io.StringIO()):
            run_fence(step, G)
        return G['BV_STEP']
    r = a2()
    check('H-R3 STEP A2 PRE-REVIEW sends the dead-row question back to the writer before any reviewer is paid',
          any('PRE-REVIEW Q3' in x and 'G-DEADROW' in x for x in r.get('lines') or []), r.get('lines'))
    statuses, fixes = [r['status']], 0
    for _ in range(40):
        if r['status'] == 'done':
            break
        if r['status'] == 'jobs_out':
            answer_jobs()
        elif r['status'] == 'rewrite':
            kd = json.load(open(kp))                      # the writer's fix, exactly as write_q_to_sidecar replaces it
            for _rq in set(r.get('rewrite') or []) | {x.split('PRE-REVIEW Q')[1].split(' ')[0] for x in r.get('lines') or []
                                                       if 'PRE-REVIEW Q' in x}:
                if _rq == '3':
                    kd['concept_map']['3']['option_texts'] = list(fixed); fixes += 1
                else:
                    kd['concept_map'][_rq]['stem_text'] += ' (revised)'
            json.dump(kd, open(kp, 'w'))
        r = a2(); statuses.append(r['status'])
    kd = json.load(open(kp)); cm = kd['concept_map']; bs = json.load(open(bsp))
    check('H-R3 STEP A2 DONE within the round budget; every reviewer packet blind (no band, no exemplar, no band guide) '
          'and every placement a rank task', r['status'] == 'done' and bs['bv']['round'] <= bc.BV_MAX_ROUNDS
          and seen['blind'] and all(seen['blind']) and seen['tasks'] and all(t == 'rank' for t in seen['tasks']), statuses)
    check('H-R3 labels by placement: a hard question Hard, a padded one below Hard (shipped at its measured band), the '
          'fixed dead-row question Hard, an easy slot Easy', cm['1']['difficulty'] == 'Hard' and cm['2']['difficulty'] != 'Hard'
          and cm['3']['difficulty'] == 'Hard' and cm['4']['difficulty'] == 'Easy' and fixes >= 1
          and all((cm[x].get('difficulty_check') or {}).get('measure') == 'placement_r3' for x in ('1', '3')),
          {x: (cm[x].get('difficulty'), (cm[x].get('difficulty_check') or {}).get('measure')) for x in cm})
    labs_ok = {x: bc.verify_difficulty_label(cm[x], L, strict=True) for x in cm}
    check('H-R3 every placement label verifies STRICTLY (LB2 kinds)', all(v[0] for v in labs_ok.values()), labs_ok)
    # ── RUN-BLOCK S13-2L.0: the footer lines (count rule RED: 2 Hard of 3 requested) ──
    with contextlib.redirect_stdout(io.StringIO()):
        run_fence(blk('# ── S13-2L.0 PAPER DIFFICULTY GATE'), {'EXAM': EXAM, 'N': N, 'LADDER': lad})
    bs = json.load(open(bsp)); cf = (bs.get('difficulty_state') or {}).get('chain_footer') or {}
    fdt = open(os.path.join(W, 'Framework_DeliveryFooter.md'), encoding='utf-8').read()
    check('H-R3 S13-2L.0 writes the count-rule RED line and the placement line DeliveryFooter §2R names',
          any(x.startswith('DIFFICULTY (RED): requested counts not met') for x in cf.get('amber') or [])
          and any(x.startswith('PLACEMENT: ') for x in cf.get('info') or [])
          and 'DIFFICULTY (RED): requested counts not met' in fdt and 'PLACEMENT: <n>% of reviewer placements were void' in fdt
          and (bs['difficulty_state'].get('r3') or {}).get('mode') == 'ladder', cf)
    # ── commit through the REAL final_assembly, then every downstream reader ──
    BP = {'exam_code': EXAM, 'blueprint_version': 't', 'difficulty_labels': L,
          'subtopic_list': [{'subtopic_id': 'oc.t1.u1', 'section': 'oc', 'topic': 't1'}],
          'difficulty_schedule': [{'mock': 1, 'simple': 1, 'medium': 0, 'hard': 3}],
          'mocks': [{'mock': 1, 'sections': [{'section_name': 'Part A', 'q_range': [1, 4],
                     'subtopic_allocations': [{'subtopic_id': 'oc.t1.u1', 'q_count': 4}]}]}], 'total_questions': 4}
    reg0 = {'exam_code': EXAM, 'schema_version': '1.0', 'mocks_completed': [], 'papers_completed': [], 'question_hashes': [],
            'stem_texts': [], 'semantic_tuples': [], 'semantic_usage': [], 'exhausted_subtopics': {}, 'question_index': [],
            'image_phashes': [], 'image_sources_used': [], 'session_log': [], 'content_tracking': {k: [] for k in fa._REQUIRED_CT},
            'section_names': [], 'rc_manifests': [], 'figural_manifests': [], 'di_manifests': []}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            res = fa.commit_registry(copy.deepcopy(reg0), {}, BP, 1, paper_id='MOCK:M01', batches_completed=1,
                                     axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                                     concept_map=copy.deepcopy(cm), difficulty_state=bs.get('difficulty_state') or {},
                                     nf_disclosed={}, manifest_hash=bc.manifest_hash({}))
        reg = res['registry']; rows_r = {str(x['q']): x for x in reg['question_index'][0]['questions']}
    except Exception as x:
        check('H-R3 final_assembly commit', False, repr(x)); return
    check('H-R3 final_assembly commits every placement label; each committed row verifies strictly',
          all(bc.verify_difficulty_label(rows_r[x], L, strict=True)[0] for x in rows_r) and len(rows_r) == 4,
          {x: rows_r[x].get('difficulty') for x in rows_r})
    okq, repq = pp.validate_question_index(reg, BP, mock_n=1)
    check('H-R3 paper_pipeline.validate_question_index (S13-QINDEX) accepts the placement rows', okq, repq.get('fails'))
    ac._reset(); ac.gate_contentlevel({'concept_map': cm}); ac.gate_qindex({'registry': reg, 'blueprint': BP, '_mockN': 1})
    _fails = [(c, m[:160]) for l, c, m in ac.RESULTS if l == 'FAIL' and c in ('A-CONTENTLEVEL', 'A-QINDEX')]
    check('H-R3 auditor A-CONTENTLEVEL and A-QINDEX: no FAIL on a ladder-mode paper', not _fails, _fails)
# ── H-R3 END ──

def self_test():
    import blueprint_core as bc, analyse_engine as ae, final_assembly as fa, paper_pipeline as pp, figure_types as ft
    import audit_canonical as ac
    from docx import Document
    OK, BAD = [], []
    def check(name, cond, note=''):
        (OK if cond else BAD).append(name + (f' — {note}' if note and not cond else ''))
        print(('  ok  ' if cond else '  FAIL') + ' ' + name + ('' if cond else f'  <- {note}'))
    ROOT = tempfile.mkdtemp(prefix='handshake_')
    W = HERE
    EXAM = 'HSX'; N = 1; paper_id = 'MOCK:M01'
    TMP = os.path.join(ROOT, 'tmp'); PROJ = ROOT + '/mnt/project'; OUT = ROOT + '/mnt/user-data/outputs'; UPL = ROOT + '/mnt/user-data/uploads'
    HOME = ROOT + '/home/claude'
    for d in (TMP, PROJ, OUT, UPL, HOME): os.makedirs(d, exist_ok=True)
    def run_fence(code, g):
        exec(_relocate(code, ROOT), g)
    try:
        # ═══ H1  PYQExplain §13A-3 content records + S7A-6  ->  [Exam]_difficulty_profile.json ═══
        print('H1 PYQExplain -> difficulty profile')
        NQ = 10   # per paper; 4 papers -> 40 PYQ items (above the sparse / shape-pool thresholds)
        exam_config = {'exam_code': EXAM, 'total_questions': NQ, 'difficulty_labels': ['Easy', 'Medium', 'Hard'],
                       'sections': [{'name': 'Section A', 'q_range': [1, NQ]}]}
        BASE = ['The major product formed in the Friedel-Crafts acylation of anisole with acetyl chloride is',
                'Identify the reagent sequence that converts cyclohexanone into cyclohexylamine',
                'The number of stereoisomers possible for 2,3-dibromobutane is',
                'Arrange the following carbocations in the order of their stability',
                'Which of the following compounds undergoes nitration fastest under standard conditions',
                'The product of ozonolysis followed by reductive work-up of 1-methylcyclohexene is',
                'Identify the compound that shows a singlet at 2.1 ppm and a quartet at 4.1 ppm',
                'The relative configuration of the two stereocentres in the given aldol product is',
                'Which reagent converts the given alkyne into a cis alkene selectively',
                'The total number of signals in the proton NMR spectrum of the given ester is']
        YEARS = [2025, 2024, 2023, 2022, 2021]
        STEMS = {y: [f'[{y}] {b}' for b in BASE] for y in YEARS}      # distinct stems per paper (differ inside the 60-char key)
        ASK = ['identify_product', 'reagent_sequence', 'stereoisomer_count', 'property_order', 'identify_product',
               'identify_product', 'spectrum_to_structure', 'stereoisomer_count', 'reagent_sequence', 'spectrum_to_structure']
        def sub_of(i): return 'oc.arom' if i in (1, 2, 5, 6, 9) else 'oc.stereo'
        def obs(y, i):
            return {'question_class': ['C-APPLY'], 'deduction_steps': [1, 2, 3, 4, 5, 6, 2, 4, 6, 3][i - 1], 'axiom_concepts': [1, 1, 2, 2, 3, 3, 1, 2, 3, 2][i - 1], 'speed_hack_exists': False,
                    'derivation_confidence': 'full', 'is_negative': False, 'qtype': 'mcq', 'subtopic_id': sub_of(i),
                    'stem_snippet': STEMS[y][i - 1][:120],
                    # v2.26 §13A-3 tags (the keys the PYQExplain spec names)
                    'ask_type': ASK[i - 1],
                    'named_concepts': ['Friedel-Crafts acylation'] if i == 1 else ['ozonolysis'] if i == 6 else [], 'concept': 'eas' if sub_of(i) == 'oc.arom' else 'stereo',
                    'drawn_names': ['anisole'] if i == 1 else [], 'near_isomer_set': (i in (1, 6)),
                    'distractor_mechanisms': ['regioisomer', 'over_reaction', 'starting_material'], 'stereo_decl': None,
                    'content_objects': [{'role': 'problem', 'kind': 'STRUCTURE', 'canonical': 'COc1ccccc1'}] if i == 1 else []}
        profile = bc.dp_new_profile(EXAM, exam_config['difficulty_labels'])
        for y in YEARS:
            pk = f'HSX_15-Jun-{y}_S1.docx'
            qs = {str(i): obs(y, i) for i in range(1, NQ + 1)}
            profile, st, why = bc.dp_add_paper(profile, source_file=pk, exam_config=exam_config, questions=qs,
                                               paper_positions=list(range(1, NQ + 1)), written_by='test', now='2026-11-03T00:00:00+00:00')
            check(f'H1 dp_add_paper {pk} accepted', st in ('added', 'replaced', 'ok') or st not in ('excluded',), st)
        prof_path = f'{PROJ}/{EXAM}_difficulty_profile.json'; json.dump(profile, open(prof_path, 'w'))
        rec = list(profile['papers'].values())[0]['questions']['1']
        rec = list(profile['papers'].values())[0]['questions']['1']
        check('H1 profile record carries v2.26 tags (DP_CONTENT_KEYS)', all(k in rec for k in ('named_concepts', 'concept', 'drawn_names', 'near_isomer_set', 'distractor_mechanisms', 'ask_type')), str(sorted(rec)))
        check('H1 profile record carries band + stem_snippet', rec.get('band') in ('Easy', 'Medium', 'Hard') and rec.get('stem_snippet'))

        # ═══ H2  Step 5: profile -> QUALITY block (section_rules) + exemplar bank ═══
        print('H2 Step 5 (analyse_engine) <- profile')
        qi = ae.profile_quality_inputs(json.load(open(prof_path)))
        check('H2 profile_quality_inputs joins every PYQ by stem', len([v for v in qi['by_stem'].values() if v]) == 50 and qi['ambiguous'] == 0, str((len(qi['by_stem']), qi['ambiguous'])))
        def s5q(i, year):
            return {'stem': STEMS[year][i - 1], 'stem_raw': STEMS[year][i - 1], 'options': ['a', 'b', 'c', 'd'], 'section': 'Section A',
                    'topic': 'Aromatic' if sub_of(i) == 'oc.arom' else 'Stereo', 'subtopic': 'EAS' if sub_of(i) == 'oc.arom' else 'Isomerism', 'year': year,
                    'paper_id': f'P{year}', 'q_num': i, 'num': i, 'image_role': 'none', 'is_msq': False, 'option_label': '1/2/3/4'}
        progress = {('Section A', 'Aromatic', 'EAS'): [s5q(i, y) for y in YEARS for i in range(1, NQ + 1) if sub_of(i) == 'oc.arom'],
                    ('Section A', 'Stereo', 'Isomerism'): [s5q(i, y) for y in YEARS for i in range(1, NQ + 1) if sub_of(i) == 'oc.stereo'],
                    '_meta': {'papers_processed': [f'P{y}' for y in YEARS]}}
        entries = []
        for (sec, top, sub), qs in [(k, v) for k, v in progress.items() if isinstance(k, tuple)]:
            e = ae.synthesise_subtopic(sec, top, sub, qs, progress, quality_inputs=qi)
            entries.append(e)
        ae.mint_subtopic_ids(entries, {})
        Q0 = entries[0]['QUALITY']
        check('H2 QUALITY lexicon measured from profile named_concepts', 'friedel-crafts acylation' in Q0['tested_concept_lexicon'], str(Q0['tested_concept_lexicon']))
        check('H2 QUALITY n / shown_entity_named_rate / near_isomer_share measured', Q0['n'] == 25 and Q0['shown_entity_named_rate'] != 'unmeasured' and Q0['near_isomer_share'] != 'unmeasured', str({k: Q0[k] for k in ('n', 'shown_entity_named_rate', 'near_isomer_share')}))
        rules_path = ae.write_section_rules(entries, EXAM, exam_meta=None, progress=progress, out_dir=TMP)
        all_qs = [q for k, v in progress.items() if isinstance(k, tuple) for q in v]
        eq = ae.exam_quality_lines(all_qs, 5, entity_paper_sets=ae.entity_paper_sets(qi), text_leaks=None, quality_inputs=qi)
        open(rules_path, 'a', encoding='utf-8').write('\n' + '\n'.join(eq) + '\n')
        SR = open(rules_path, encoding='utf-8').read()
        sid0, sid1 = entries[0]['subtopic_id'], entries[1]['subtopic_id']
        qb = bc.quality_block_for_subtopic(SR, sid0)
        check('H2 section_rules QUALITY block round-trips through bc.quality_block_for_subtopic', qb and qb['n'] == 25 and qb['tested_concept_lexicon'] == Q0['tested_concept_lexicon'] and qb['shape_shares'] == Q0['shape_shares'], str(qb)[:200])
        check('H2 EXAM_QUALITY lines present', '=== EXAM_QUALITY ===' in SR and 'PYQ_COMMON_ENTITIES:' in SR and 'GATE_CALIBRATION:' in SR)
        _common, _calib = ac._qq_exam_quality_lines({'rules_txt': SR})
        check('H2 PYQ_COMMON_ENTITIES lists ENTITIES (anisole drawn in all 5 papers), never paper keys', 'anisole' in _common and not any(k.startswith('P2') or 'docx' in k for k in _common), str(_common))
        check('H2 GATE_CALIBRATION / PYQ_MODE parse in the auditor', isinstance(ac._qq_gate_calibration({'rules_txt': SR}), dict) and ac._qq_pyq_mode({'rules_txt': SR}) in ('sparse', 'full'))
        check('H2 shape_shares keys come from the profile family tag (ASK[] vocabulary), no "other"', set(k.split('|')[0] for k in Q0['shape_shares']) <= set(ASK) and 'other' not in {k.split('|')[0] for k in Q0['shape_shares']}, str(list(Q0['shape_shares'])))
        sid_of = {(e['section'], e['topic'], e['subtopic']): e['subtopic_id'] for e in entries}
        rows = ae.exemplar_rows(all_qs, qi, sid_of)
        bank_path, bank, dropped = ae.write_exemplar_bank(EXAM, rows, out_dir=TMP)
        check('H2 exemplar bank non-empty, keyed by the MINTED subtopic_id (what the blueprint / Create use), band, qtype', bank['cells'] and sid0 in bank['cells'] and any(b in bank['cells'][sid0] for b in ('Easy', 'Medium', 'Hard')), str(list(bank['cells']))[:200])
        check('H2 exemplar bank schema (_meta.schema_version, cells)', bank['_meta'].get('schema_version') == 1 and isinstance(bank['cells'], dict))
        shutil.copy(rules_path, f'{PROJ}/{EXAM}_section_rules.md'); shutil.copy(bank_path, f'{PROJ}/{EXAM}_exemplar_bank.json')

        # the auditor's reader of EXAM_QUALITY (A-ENTITYLEAK) must parse what Step 5 wrote
        src_probe = {'rules_txt': SR}
        _ce = ac._qq_exam_quality_lines(src_probe)
        check('H2 auditor parses the EXAM_QUALITY lines Step 5 wrote', _ce is not None and _ce != ({}, None) , str(_ce)[:120])

        # ═══ H3  Blueprint §7-8 / ScopedBlueprint S8-2d <- section_rules QUALITY ═══
        print('H3 blueprints <- section_rules')
        t = open(f'{W}/Framework_Blueprint.md', encoding='utf-8').read(); i = t.find('# §7-8 (v1.63.0'); j = t.find('# §7-8R', i)
        _labs_hs = list(exam_config['difficulty_labels'])
        g = {'_bc_ask': bc, 'bc': bc, 'MANIFEST_IDS': {sid0: {'display_name': 'EAS'}, sid1: {'display_name': 'Isomerism'}},
             'section_rules_text': SR, 'r_avg': {'EAS': 2.0, 'Isomerism': 1.0}, 'total_qs': 30, 'blueprint': {'total_mocks': 2},
             # v1.64.0 §7-9 (GAP-2026-11-05) reads the profile, the labels and PROFILE_CFG
             'PROFILE': profile, '_labels': _labs_hs, 'PROFILE_CFG': {'cycle_gap_days': exam_config.get('cycle_gap_days')}}
        run_fence(t[i:j], g)
        check('H3 Blueprint §7-8 writes shape_target_per_paper for every mock', set(g['blueprint']['shape_target_per_paper']) == {'1', '2'} and g['blueprint']['schema_version'] == 2, str(g['blueprint'].get('shape_target_per_paper'))[:120])
        check('H3 Blueprint §7-8 stamps shape_rule s1 on every target (G4)', all(tg.get('shape_rule') == bc.SHAPE_RULE_LEGACY for mk in g['blueprint']['shape_target_per_paper'].values() for tg in mk.values() if isinstance(tg, dict)))
        check('H3 Blueprint §7-9 writes the level-target fields (DL-31/33/34/36)', all(k in g['blueprint'] for k in ('axis2_format_floor_per_paper', 'level_targets', 'hard_share_by_subtopic', 'hard_supply')) and isinstance(g['blueprint']['hard_share_by_subtopic'], dict), str({k: g['blueprint'].get(k) for k in ('axis2_format_floor_per_paper', 'hard_share_by_subtopic')})[:160])
        check('H3 Blueprint §7-9 hard_share_by_subtopic == bc.hard_share_by_subtopic (same profile, same labels)', g['blueprint']['hard_share_by_subtopic'] == bc.hard_share_by_subtopic(profile, _labs_hs, gap_days=exam_config.get('cycle_gap_days')))
        check('H3 Blueprint §7-9 (e) records level_model_inputs the auditor and Create build from (DL-21)',
              isinstance(g['blueprint'].get('level_model_inputs'), dict) and g['blueprint']['level_model_inputs']['subtopic_ids'] == sorted([sid0, sid1])
              and g['blueprint']['level_model_inputs']['mix_rule'] == 'm1' and g['blueprint']['level_model_inputs']['labels'] == _labs_hs)
        t2 = open(f'{W}/Framework_ScopedBlueprint.md', encoding='utf-8').read(); i = t2.find('# S8-2d (v1.13.0'); j = t2.find('# S8-3', i)
        g2 = {'bc': bc, '_sr_text': SR, 'in_scope_ids': [sid0, sid1], 'r_avg': {sid0: 2.0, sid1: 1.0}, 'Q': 20, 'N': 2,
              'DIFFICULTY_PROFILE': profile, 'PROFILE_CFG': {'difficulty_labels': _labs_hs, 'cycle_gap_days': exam_config.get('cycle_gap_days')}}
        run_fence(t2[i:j], g2)
        check('H3 ScopedBlueprint S8-2d writes SHAPE_TARGET', set(g2['SHAPE_TARGET']) == {'1', '2'})
        check('H3 ScopedBlueprint S8-2e mirrors Blueprint §7-9 (hard share restricted to the scope; floors per paper)', isinstance(g2.get('HARD_SHARE_BY_SUBTOPIC'), dict) and set(g2['HARD_SHARE_BY_SUBTOPIC']) <= {sid0, sid1} and isinstance(g2.get('AXIS2_FORMAT_FLOOR'), dict) and isinstance(g2.get('LEVEL_TARGETS'), dict), str(g2.get('HARD_SHARE_BY_SUBTOPIC'))[:120])
        check('H3 ScopedBlueprint S8-2e (e) records level_model_inputs (scope ids, m2 default, tier None)',
              isinstance(g2.get('LEVEL_MODEL_INPUTS'), dict) and g2['LEVEL_MODEL_INPUTS']['subtopic_ids'] == sorted([sid0, sid1])
              and g2['LEVEL_MODEL_INPUTS']['mix_rule'] == 'm2' and g2['LEVEL_MODEL_INPUTS']['tier'] is None)
        BP = {'blueprint_version': 'hs-1', 'total_questions': 4, 'batch_size_qs': 10, 'exam_code': EXAM,
              'subtopic_list': [{'subtopic_id': sid0, 'section': 'Section A', 'subtopic': 'EAS'}, {'subtopic_id': sid1, 'section': 'Section A', 'subtopic': 'Isomerism'}],
              'difficulty_labels': ['Easy', 'Medium', 'Hard'], 'difficulty_schedule': [{'mock': 1, 'simple': 1, 'medium': 2, 'hard': 1}],
              'sections': [{'name': 'Section A', 'section_name': 'Section A', 'q_range': [1, 4], 'total_qs': 4}], 'mocks': [{'mock': 1, 'paper_id': paper_id}],
              'options_count': 4, 'option_label_format': '1/2/3/4',
              'shape_target_per_paper': {'1': bc.shape_targets({k.split('|')[0]: v for k, v in Q0['shape_shares'].items()}, 4, 0)}, 'schema_version': 2, 'producer': 'test'}
        bp_path = f'{PROJ}/{EXAM}_blueprint.json'; json.dump(BP, open(bp_path, 'w'))

        # ═══ H4  Create S3-2e readiness + S3-12d shape plan <- blueprint / section_rules / bank ═══
        print('H4 Create S3-2e / S3-12d')
        cre = f'{W}/Framework_MockTestCreate.md'
        f32e = [b for _, b in fences(cre) if 'S3-2e' in b[:200]]
        check('H4 S3-2e fence found', len(f32e) >= 1)
        bs_path = f'{HOME}/{EXAM}_M{N}_batch_state.json'
        for p in (bs_path,):
            if os.path.exists(p): os.remove(p)
        g4 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'bp': BP, 'bs_prev': {}}
        run_fence(f32e[0], g4)
        RD = g4['QUALITY_READINESS']
        check('H4 readiness reads exemplar bank / section_rules / profile / blueprint as PASS', all(RD['controls'][c]['status'] == 'PASS' for c in ('G-DIFF-JUDGE', 'G-STEMLEAK', 'G-STEMFORM', 'G-SHAPEMIX', 'G-TEMPLATE', 'G-DISTRACTOR', 'G-ENTITYLEAK')), str({c: v['status'] for c, v in RD['controls'].items()}))
        # GAP-2026-11-05 DL-46: the content floor is MEASURED — the synthetic profile holds fewer than
        # bc.LEVEL_MIN_POOL content-full records, so the control is DORMANT (not PASS on field presence,
        # not degraded, named in the printed block) and the footer formatter carries the reason.
        _n_full4 = sum(1 for _p4 in (g4.get('_rd_in', {}).get('difficulty_profile.json') or {}).get('papers', {}).values()
                       for _r4 in (_p4.get('questions') or {}).values()
                       if isinstance(_r4, dict) and _r4.get('content_vector') and str(_r4.get('content_confidence', 'full')) == 'full')
        _fl4 = RD['controls']['G-DIFF-FLOOR']
        check('H4 readiness measures the content floor (DL-46): DORMANT below LEVEL_MIN_POOL, never degraded, named in the block',
              (_fl4['status'] == 'DORMANT' if 0 < _n_full4 < bc.LEVEL_MIN_POOL else _fl4['status'] in ('PASS', 'N/A'))
              and 'G-DIFF-FLOOR' not in RD['degraded']
              and (_fl4['status'] == 'PASS' or 'G-DIFF-FLOOR' in str(bc.quality_readiness_block(RD)))
              and (_fl4['status'] == 'PASS' or bc.difficulty_unverified_lines(RD, None, n_level_items=1)[0].startswith('DIFFICULTY UNVERIFIED')),
              f"{_fl4} n_full={_n_full4}")
        check('H4 readiness: only the artefacts this test did not produce are MISSING (style_profile, pyq_index)', set(RD['degraded']) <= {'G-STYLE', 'G-PYQ-DIST', 'G-ITEM'}, str(RD['degraded']))
        check('H4 EXEMPLAR_BANK_PATH bound to the delivered run file', g4.get('EXEMPLAR_BANK_PATH') and os.path.exists(g4['EXEMPLAR_BANK_PATH']))
        f312d = [b for _, b in fences(cre) if 'S3-12d (executable' in b[:200]]
        # v5.92 S3-12e (GAP-2026-11-05 DL-33/34) reads the Blueprint §7-9 fields written in H3 and
        # re-places the top-band slots of difficulty_plan; counts must be conserved.
        BP['hard_share_by_subtopic'] = g['blueprint']['hard_share_by_subtopic']
        BP['axis2_format_floor_per_paper'] = g['blueprint']['axis2_format_floor_per_paper']
        _plan4 = {1: BP['difficulty_labels'][2], 2: BP['difficulty_labels'][0], 3: BP['difficulty_labels'][1], 4: BP['difficulty_labels'][1]}
        g4.update({'subtopic_by_qnum': {1: sid0, 2: sid0, 3: sid1, 4: sid1}, '_qtype_by_q': {q: 'mcq' for q in (1, 2, 3, 4)},
                   'SECTION_RULES_TEXT': SR, 'difficulty_plan': dict(_plan4), 'difficulty_labels': BP['difficulty_labels']})
        run_fence(f312d[0], g4)
        PLAN = g4['SHAPE_PLAN']
        check('H4 S3-12d assigns a shape to every slot from the blueprint targets', all(str(q) in PLAN for q in (1, 2, 3, 4)) and all(PLAN[str(q)] in BP['shape_target_per_paper']['1'] or PLAN[str(q)] is None for q in (1, 2, 3, 4)), str(PLAN))
        _after4 = g4['difficulty_plan']
        check('H4 S3-12e keeps every band count while placing top-band slots by subtopic share (DL-33)', sorted(_after4.values()) == sorted(_plan4.values()) and set(_after4) == set(_plan4), str(_after4))
        check('H4 S3-12e binds the paper\'s ask-format floors from the blueprint (DL-34)', isinstance(g4.get('AXIS2_FORMAT_FLOOR'), dict) and g4['AXIS2_FORMAT_FLOOR'] == dict((BP['axis2_format_floor_per_paper'] or {}).get(str(N)) or {}), str(g4.get('AXIS2_FORMAT_FLOOR')))
        # S7-QUALITY judge packet <- exemplar bank slice
        item = {'stem': BASE[0] + ' variant', 'options': ['a', 'b', 'c', 'd'], 'difficulty_plan': 'Hard', 'solution': 'x', 'subtopic_id': sid0}
        EX = bc.exemplars_for(g4['EXEMPLAR_BANK'], sid0, 'mcq', BP['difficulty_labels'])
        check('H4 bc.exemplars_for finds exemplars for every band from the Step-5 bank', EX['complete'] is True and all(EX['by_band'].get(b) for b in BP['difficulty_labels']), str({k: len(v) for k, v in EX['by_band'].items()}) + ' level=' + str(EX['level_used']))
        jin = bc.build_judge_input(item, EX['by_band'], BP['difficulty_labels'])
        check('H4 build_judge_input strips author fields and carries exemplars per band', isinstance(jin, dict) and 'solution' not in json.dumps(jin.get('item', jin)) and 'difficulty_plan' not in json.dumps(jin.get('item', jin)) and jin['exemplars'], str(jin)[:200])

        # ═══ H5  S7-QUALITY sidecar -> S13-2F auditor (precommit) -> stamps -> certificate ═══
        print('H5 sidecar -> auditor precommit')
        import re as _re
        def pattern_keys_for(sid):
            m = _re.search(r'^[ \t]*subtopic_id:[ \t]*' + _re.escape(sid) + r'[ \t\r]*$', SR, _re.M)
            seg = SR[m.start():(SR.find('\n--- Subtopic:', m.start()) if m and SR.find('\n--- Subtopic:', m.start()) > 0 else len(SR))] if m else ''
            return _re.findall(r'"pattern_key":\s*"([^"]+)"', seg)
        MQ = NQ
        order = [sid0 if i % 2 else sid1 for i in range(1, MQ + 1)]        # alternate subtopics: no adjacent same concept group
        d = Document()
        for n in range(1, MQ + 1):
            d.add_paragraph(f'Q.{n}  {" ".join(BASE[(n-1) % len(BASE)].split()[:12])} (mock {n})?')
            for i, o in enumerate(['Alpha', 'Beta', 'Gamma', 'Delta'], 1): d.add_paragraph(f'{i}.  {o}')
            d.add_paragraph('')
        docx = f'{OUT}/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'; d.save(docx)
        BP['total_questions'] = MQ; BP['sections'][0]['q_range'] = [1, MQ]; BP['sections'][0]['total_qs'] = MQ
        BP['difficulty_schedule'] = [{'mock': 1, 'simple': 3, 'medium': 4, 'hard': 3}]
        t = open(f'{W}/Framework_Blueprint.md', encoding='utf-8').read(); i = t.find('# §7-8 (v1.63.0'); j = t.find('# §7-8R', i)
        g78 = {'_bc_ask': bc, 'bc': bc, 'MANIFEST_IDS': {sid0: {'display_name': 'EAS'}, sid1: {'display_name': 'Isomerism'}},
               'section_rules_text': SR, 'r_avg': {'EAS': 2.0, 'Isomerism': 1.0}, 'total_qs': MQ, 'blueprint': {'total_mocks': 1},
               'PROFILE': profile, '_labels': _labs_hs, 'PROFILE_CFG': {'cycle_gap_days': exam_config.get('cycle_gap_days')}}
        run_fence(t[i:j], g78); BP['shape_target_per_paper'] = g78['blueprint']['shape_target_per_paper']
        BP['hard_share_by_subtopic'] = g78['blueprint']['hard_share_by_subtopic']; BP['axis2_format_floor_per_paper'] = g78['blueprint']['axis2_format_floor_per_paper']
        check('H5 blueprint §7-8 targets for the mock paper (both subtopics pooled)', set(BP['shape_target_per_paper']) == {'1'} and len(BP['shape_target_per_paper']['1']) >= 3, str(BP['shape_target_per_paper'])[:160])
        json.dump(BP, open(bp_path, 'w'))
        g4b = dict(g4); g4b.update({'subtopic_by_qnum': {n: order[n-1] for n in range(1, MQ + 1)}, 'bp': BP}); run_fence(f312d[0], g4b); PLAN = g4b['SHAPE_PLAN']
        bands = ['Easy'] * 3 + ['Medium'] * 4 + ['Hard'] * 3
        cm = {str(n): {'subtopic_id': order[n-1], 'difficulty': bands[n-1],
                       'shape': PLAN.get(str(n)) or 'identify_product', 'scheme_grammar': 'none', 'fingerprint': f'fp{n}', 'concept': f'c{n}',
                       'pattern_key': (pattern_keys_for(order[n-1]) or [None])[0],
                       'distractor_mechanisms': ['regioisomer', 'over_reaction', 'starting_material'], 'mechanism_family': 'chemistry',
                       'stem_text': ' '.join(BASE[(n-1) % len(BASE)].split()[:12]) + f' (mock {n})?', 'option_texts': ['Alpha', 'Beta', 'Gamma', 'Delta'], 'figure_files': []} for n in range(1, MQ + 1)}
        # v2.0 (GAP-2026-11-10 LAW-ORG-5 / LAW-ORG-7): a paper produced by THIS release carries an LB2 basis on every
        # label (two fresh blind grades + the recipe) and a unanimous key record — the synthetic paper does too
        _pk_hs = {'grader_1': {'context': 'fresh', 'sha256': 'a' * 64}, 'grader_2': {'context': 'fresh', 'sha256': 'b' * 64}}
        for _n_hs in list(cm):
            _b_hs = cm[_n_hs]['difficulty']
            cm[_n_hs] = bc.dl_set_label_basis_strict(cm[_n_hs], 'measured_exact', _labs_hs, _b_hs,
                                                     {'grader_1': _b_hs, 'grader_2': _b_hs, 'recipe': True}, _pk_hs)[0]
            cm[_n_hs] = bc.op_record_controls(cm[_n_hs], _b_hs, _b_hs, True, _pk_hs,
                                              key_votes={'author': 'k', 'solver_1': 'k', 'solver_2': 'k', 'unanimous': True})
        check('H5 v2.0 every label carries an LB2 measured_exact basis', all(
            bc.verify_difficulty_label(cm[_n], _labs_hs)[2] == 'measured_exact' and bc.verify_difficulty_label(cm[_n], _labs_hs)[0]
            for _n in cm), str({_n: bc.verify_difficulty_label(cm[_n], _labs_hs) for _n in cm})[:200])
        check('H5 S7-QUALITY pattern_key resolvable from section_rules PATTERN_KEYS', all(cm[str(n)]['pattern_key'] for n in range(1, MQ + 1)), str(pattern_keys_for(sid0))[:100])
        key_path = f'{HOME}/{EXAM}_M{N}_answer_key.json'
        ANS = {str(n): 1 + (n % 4) for n in range(1, MQ + 1)}
        ANS['2'] = [1, 3]; cm['2']['distractor_mechanisms'] = ['regioisomer', 'over_reaction']; cm['2']['key_set_size'] = 2   # MSQ item (M2)
        json.dump({'answers': ANS, 'concept_map': cm}, open(key_path, 'w'))
        reg = {'exam_code': EXAM, 'schema_version': '1.0', 'mocks_completed': [], 'papers_completed': [], 'question_hashes': [], 'stem_texts': [], 'semantic_tuples': [],
               'semantic_usage': [], 'exhausted_subtopics': {}, 'question_index': [], 'image_phashes': [], 'image_sources_used': [], 'session_log': [],
               'content_tracking': {k: [] for k in fa._REQUIRED_CT}, 'section_names': [], 'rc_manifests': [], 'figural_manifests': [], 'di_manifests': []}
        prev = fa.commit_registry(copy.deepcopy(reg), {}, BP, N, paper_id=paper_id, batches_completed=1, axis2_window_counts={}, passage_present=False, di_present=False,
                                  figural_present=False, concept_map=cm, quality_readiness=RD)
        check('H5 commit_registry preview ok and carries producer_release + V590 fields + quality_readiness', prev['ok'] and prev['registry']['question_index'][0]['qindex_cert']['producer_release'] == bc.QQ_RELEASE
              and 'shape' in prev['registry']['question_index'][0]['questions'][0] and prev['registry']['question_index'][0].get('quality_readiness'), str(prev.get('problems') or prev.get('error'))[:200])
        prev_path = f'{TMP}/prev.json'; json.dump(prev['registry'], open(prev_path, 'w'))
        def audit(phase, extra):
            cmd = [sys.executable, f'{W}/audit_canonical.py', docx, '--phase', phase, '--item-findings', f'{TMP}/if.json', '--write-certificate', f'{TMP}/cert.json',
                   '--blueprint', bp_path, '--rules', f'{PROJ}/{EXAM}_section_rules.md', '--registry', prev_path, '--mockN', str(N)] + extra
            r = subprocess.run(cmd, capture_output=True, text=True)
            return r, {l.split(']')[1].split()[0]: l.split(']')[0].strip('[ ') for l in r.stdout.split('\n') if l.startswith('[') and ']' in l}
        r, lv = audit('precommit', ['--key', key_path, '--profile', prof_path])
        qq = {g: lv.get(g) for g in ('A-QUALITYSTATUS', 'A-REVIEW', 'A-SHAPEMIX', 'A-TEMPLATE', 'A-STEMLEAK', 'A-DISTRACTOR', 'A-READINESS', 'A-OPTDISTINCT', 'A-ITEMRULE')}
        check('H5 precommit: no quality gate FAILs on a clean unstamped paper', all(v != 'FAIL' for v in qq.values()), str(qq))
        check('H5 precommit: A-READINESS reads the committed readiness record', lv.get('A-READINESS') in ('ok', 'WARN'), str(lv.get('A-READINESS')))
        check('H5 precommit: A-SHAPEMIX ARMED (reads concept_map.shape vs blueprint targets)', 'DORMANT' not in (r.stdout.split('A-SHAPEMIX')[1][:80] if 'A-SHAPEMIX' in r.stdout else 'DORMANT'), r.stdout.split('A-SHAPEMIX')[1][:120] if 'A-SHAPEMIX' in r.stdout else '')
        fails_other = [l for l in r.stdout.split('\n') if l.startswith('[ FAIL]')]
        check('H5 precommit: whole auditor clean on the synthetic paper (certificate written)', os.path.exists(f'{TMP}/cert.json'), '\n'.join(fails_other)[:600])
        CERT = json.load(open(f'{TMP}/cert.json')) if os.path.exists(f'{TMP}/cert.json') else {}
        check('H5 certificate schema 3 (LAW-CERT-1) with uncertified_items / certified / accepted_findings / auditor', CERT.get('schema') == 3 and 'uncertified_items' in CERT
              and CERT.get('certified') is True and isinstance(CERT.get('accepted_findings'), list) and str(CERT.get('auditor', '')).startswith('audit_canonical v2.'), str(CERT)[:200])
        # ═══ H5-CERT-DISCLOSED (GAP-2026-11-17-CERT-DISCLOSED-CONTRACT): the REAL S13-2F call (precommit,
        # --write-certificate) on a BATCH-COMPLETE paper whose Q3 is stamped ESCALATED(A-DISTRACTOR) (key_votes.rule BC1,
        # LAW-BC-8) and really fails A-DISTRACTOR, then the REAL S13-4c call (final, --certificate) on the same docx.
        # Release 2026.11.22 wrote this certificate and then FAILED A-CERT on it ("6 unresolved item finding(s)").
        _kd_cd = json.load(open(key_path))
        for _q, _e in _kd_cd['concept_map'].items():
            _e['key_votes'] = dict(_e.get('key_votes') or {}, rule='BC1')
        _kd_cd['concept_map']['3']['distractor_mechanisms'] = ['regioisomer']          # short record -> A-DISTRACTOR item finding
        _kd_cd['concept_map']['3']['quality_status'] = 'ESCALATED(A-DISTRACTOR)'
        _kcd = f'{TMP}/{EXAM}_M7_answer_key.json'; json.dump(_kd_cd, open(_kcd, 'w'))
        def _aud_cd(phase, extra):
            _c = [sys.executable, f'{W}/audit_canonical.py', docx, '--phase', phase, '--item-findings', f'{TMP}/if_cd_{phase}.json',
                  '--blueprint', bp_path, '--rules', f'{PROJ}/{EXAM}_section_rules.md', '--registry', prev_path, '--mockN', str(N),
                  '--key', _kcd, '--profile', prof_path] + extra
            _r = subprocess.run(_c, capture_output=True, text=True)
            return _r, [l for l in _r.stdout.split('\n') if l.startswith('[') and ']' in l]
        _r_cd, _l_cd = _aud_cd('precommit', ['--write-certificate', f'{TMP}/cert_cd.json'])
        _c_cd = json.load(open(f'{TMP}/cert_cd.json')) if os.path.exists(f'{TMP}/cert_cd.json') else {}
        _if_cd = json.load(open(f'{TMP}/if_cd_precommit.json')) if os.path.exists(f'{TMP}/if_cd_precommit.json') else {}
        check('H5-CERT-DISCLOSED S13-2F: A-DISTRACTOR fires on Q3 and is reconciled to AMBER — ESCALATED (not a FAIL line)',
              any(f.get('q') == '3' and f.get('gate') == 'A-DISTRACTOR' for f in _if_cd.get('item_findings') or [])
              and any('A-DISTRACTOR' in l and 'ESCALATED' in l and l.startswith('[ WARN]') for l in _l_cd), '\n'.join(l for l in _l_cd if 'DISTRACTOR' in l)[:300])
        check('H5-CERT-DISCLOSED S13-2F: certificate written — schema 3, disclosed/escalated [3], certified, a matching escalated row',
              _c_cd.get('schema') == 3 and _c_cd.get('disclosed_items') == ['3'] and _c_cd.get('escalated_items') == ['3']
              and _c_cd.get('certified') is True and _c_cd.get('uncertified_items') == [] and _c_cd.get('findings', 0) >= 1
              and all(r.get('q') == '3' and r.get('disposition') == 'escalated' for r in _c_cd.get('accepted_findings') or [{}]),
              (str(_c_cd)[:300] or _r_cd.stdout[-600:]))
        _r_cd4, _l_cd4 = _aud_cd('final', ['--certificate', f'{TMP}/cert_cd.json'])
        _ac_cd = [l for l in _l_cd4 if ' A-CERT ' in l + ' ']
        check('H5-CERT-DISCLOSED S13-4c: A-CERT ok — certified WITH DISCLOSURES, ESCALATED Q3 carried as AMBER; ONE A-CERT line',
              len(_ac_cd) == 1 and _ac_cd[0].startswith('[  ok ]') and 'WITH DISCLOSURES' in _ac_cd[0] and 'ESCALATED' in _ac_cd[0], str(_ac_cd)[:300])
        _c_bad = dict(_c_cd, certified=True, uncertified_items=['3'], disclosed_items=[], escalated_items=[],
                      accepted_findings=[dict(r, disposition='uncertified') for r in _c_cd.get('accepted_findings') or []])
        json.dump(_c_bad, open(f'{TMP}/cert_cd_bad.json', 'w'))
        _r_cdb, _l_cdb = _aud_cd('final', ['--certificate', f'{TMP}/cert_cd_bad.json'])
        check('H5-CERT-DISCLOSED S13-4c: a hand-edited certificate (items moved to uncertified, certified left true) FAILs CERT-CONTRACT, exit 1',
              _r_cdb.returncode == 1 and any(l.startswith('[ FAIL]') and 'A-CERT' in l and 'CERT-CONTRACT' in l for l in _l_cdb),
              str([l for l in _l_cdb if 'A-CERT' in l])[:300])
        # ═══ H5-V7-SIDECAR (G4): a PER-BATCH audit (no registry entry) of a current paper whose sidecar has the real v7+
        # shape — text_fingerprint / key_votes, NO top-level fingerprint — plus a batch_state with producer_release and
        # quality_readiness: no line may call it a 'pre-2026.11.03 paper'; levels are unchanged (owner decision 2026-11-17).
        _kd_v7 = json.load(open(_kcd))
        for _q, _e in _kd_v7['concept_map'].items():
            _e.pop('fingerprint', None); _e.pop('quality_status', None); _e['text_fingerprint'] = f'tf{_q}'
        _k_v7 = f'{TMP}/{EXAM}_M6_answer_key.json'; json.dump(_kd_v7, open(_k_v7, 'w'))
        json.dump({'producer_release': open(f'{W}/VERSION').read().strip(), 'quality_readiness': RD}, open(f'{TMP}/{EXAM}_M6_batch_state.json', 'w'))
        _r_v7 = subprocess.run([sys.executable, f'{W}/audit_canonical.py', docx, '--blueprint', bp_path, '--rules', f'{PROJ}/{EXAM}_section_rules.md',
                                '--mockN', '6', '--batch', '1', '--key', _k_v7, '--profile', prof_path, '--item-findings', f'{TMP}/if_v7.json'],
                               capture_output=True, text=True)
        _lines_v7 = [l for l in _r_v7.stdout.split('\n') if l.startswith('[')]
        check('H5-V7-SIDECAR per-batch audit of a current paper: no "pre-2026.11.03" label; A-DISTRACTOR still WARN (level unchanged) with the in-batch label',
              _lines_v7 and not [l for l in _lines_v7 if 'pre-2026.11.03' in l]
              and any(l.startswith('[ WARN]') and 'A-DISTRACTOR' in l and 'PRE-REVIEW' in l for l in _lines_v7),
              '\n'.join(l for l in _lines_v7 if 'pre-2026.11.03' in l or 'A-DISTRACTOR' in l)[:400])
        # ═══ H5-LEGACY (GAP-2026-11-04 T1): a project whose Step 5 predates the QUALITY
        # measurement (section_rules WITHOUT QUALITY / EXAM_QUALITY blocks — every existing
        # project) and a paper whose items all repeat ONE template: A-TEMPLATE is DORMANT,
        # no item is stamped, the certificate is certified. Release 2026.11.03 failed this
        # (default cap 2 -> UNRESOLVED -> NOT CERTIFIED).
        _sr_legacy = re.sub(r'QUALITY \(v[\d.]+\):\n(?:  .*\n?)*', '', SR).split('=== EXAM_QUALITY ===')[0]
        _rl = f'{TMP}/{EXAM}_section_rules_legacy.md'; open(_rl, 'w', encoding='utf-8').write(_sr_legacy)
        _kl = json.load(open(key_path))
        for _q, _e in _kl['concept_map'].items():
            _e['fingerprint'] = 'other|mcq|none|none'
        _klp = f'{TMP}/{EXAM}_M9_answer_key.json'; json.dump(_kl, open(_klp, 'w'))
        _rlg = subprocess.run([sys.executable, f'{W}/audit_canonical.py', docx, '--phase', 'precommit', '--item-findings', f'{TMP}/if_l.json',
                               '--write-certificate', f'{TMP}/cert_l.json', '--blueprint', bp_path, '--rules', _rl, '--registry', prev_path,
                               '--mockN', str(N), '--key', _klp, '--profile', prof_path], capture_output=True, text=True)
        _tl = [l for l in _rlg.stdout.split('\n') if 'A-TEMPLATE' in l][:1]
        check('H5-LEGACY T1: no QUALITY blocks -> A-TEMPLATE DORMANT (never a default cap), no A-TEMPLATE item finding',
              bool(_tl) and '[  ok ]' in _tl[0] and 'DORMANT' in _tl[0]
              and not [f for f in (json.load(open(f'{TMP}/if_l.json')).get('item_findings') or []) if f.get('gate') == 'A-TEMPLATE'], str(_tl))
        check('H5-LEGACY T1: certificate certified (no item UNRESOLVED by an unmeasured control)',
              os.path.exists(f'{TMP}/cert_l.json') and json.load(open(f'{TMP}/cert_l.json')).get('uncertified_items') == [],
              (_rlg.stdout[-800:] if not os.path.exists(f'{TMP}/cert_l.json') else str(json.load(open(f'{TMP}/cert_l.json')).get('uncertified_items'))))
        # ═══ H5-LEGACY-STAMPS (GAP-2026-11-04 release review): a paper PARKED by 2026.11.03 carries
        # UNRESOLVED(A-TEMPLATE) stamps from the default cap (sidecar AND registry preview). The REAL
        # S13-2F fence must clear them in both, and its certificate must come out certified.
        _kd_keep = open(key_path).read()
        _kl2 = json.load(open(key_path))
        for _q, _e in _kl2['concept_map'].items():
            _e['quality_status'] = 'UNRESOLVED(A-TEMPLATE)' if _q in ('1', '2') else 'CERTIFIED'
        json.dump(_kl2, open(key_path, 'w'))
        _pv2 = fa.commit_registry(copy.deepcopy(reg), {}, BP, N, paper_id=paper_id, batches_completed=1, axis2_window_counts={},
                                  passage_present=False, di_present=False, figural_present=False, concept_map=_kl2['concept_map'], quality_readiness=RD)
        json.dump(_pv2['registry'], open(f'{HOME}/{EXAM}_M{N}_registry_preview.json', 'w'))
        json.dump({'state': 'AWAITING_REVIEW', 'quality_readiness': RD, 'uncertified_items': ['1', '2']}, open(f'{HOME}/{EXAM}_M{N}_batch_state.json', 'w'))
        shutil.copy(f'{W}/audit_canonical.py', f'{HOME}/{EXAM}_mock_test_audit.py')
        if not os.path.exists(f'{PROJ}/{EXAM}_subtopic_manifest.json'):
            json.dump({'subtopics': []}, open(f'{PROJ}/{EXAM}_subtopic_manifest.json', 'w'))
        _f2f = [b for _l, b in fences(cre) if "_stp = f'/home/claude/{EXAM}_M{N}_s13_2f_state.json'" in b]
        check('H5-LEGACY-STAMPS S13-2F fence found', len(_f2f) == 1)
        g2f = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'bp': BP, 'BP_SRC_PATH': bp_path, 'AUDIT_AVAILABLE': True,
               'AUDIT_ENV': dict(os.environ, PYTHONPATH=W), 'STIM_PROFILE_PATH': None}
        _raised = None
        try:
            run_fence(_f2f[0], g2f)
        except BaseException as _ex:      # a LADDER-REPAIR raise means the sweep was NOT clean
            _raised = repr(_ex)[:300]
        _kl3 = json.load(open(key_path))
        _c2f = g2f.get('CERT') or {}
        check('H5-LEGACY-STAMPS: 2026.11.03 default-cap stamps cleared in sidecar AND preview; certificate certified; items re-stamped CERTIFIED',
              _raised is None and _c2f.get('uncertified_items') == [] and _c2f.get('certified') is True
              and _kl3['concept_map']['1'].get('quality_status') == 'CERTIFIED' and _kl3['concept_map']['2'].get('quality_status') == 'CERTIFIED',
              str((_raised, _c2f.get('uncertified_items'), _kl3['concept_map']['1'].get('quality_status'))))
        open(key_path, 'w').write(_kd_keep)
        for _f in (f'{HOME}/{EXAM}_M{N}_item_sweep_certificate.json', f'{HOME}/{EXAM}_M{N}_item_findings.json'):
            if os.path.exists(_f): os.remove(_f)
        # S13-2F stamps (as the spec does): CERTIFIED on every item
        kd = json.load(open(key_path))
        for q, e in kd['concept_map'].items():
            if not str(e.get('quality_status', '')).startswith('UNRESOLVED'): e['quality_status'] = 'CERTIFIED'
        json.dump(kd, open(key_path, 'w'))

        # ═══ H6  S13-2G IN-SESSION review: phase 1 -> reviewer (MockReview internal brief) -> phase 3 ═══
        # 2026.11.04 (GAP-2026-11-04 A1-A7, T4/T5/T7/T8): the review never leaves the run. The
        # packet lives under /home/claude ONLY; the reviewer (here: the brief's fences, exactly
        # what a fresh sub-agent executes) writes verdicts.json inside its part folder; phase 3
        # binds automatically. NOTHING may reach the user's outputs folder but the paper.
        print('H6 in-session review handshake')
        json.dump({'state': 'BATCHES', 'batches_completed': [1], 'current_batch': 2, 'quality_readiness': RD, 'shape_plan': PLAN, 'uncertified_items': []}, open(bs_path, 'w'))
        ph = fences(cre, 'S13-2G phase')
        def _nohead(b):          # 2026.11.15: a RUN-BLOCK's header lines come first (G-02)
            return '\n'.join(x for x in b.split('\n') if not x.lstrip().startswith(('# RUN-BLOCK', '# PARAMS:', '# DEFINES:')))
        check('H6 S13-2G has exactly two executable phases (1 and 3); phase 2 is CLASS T prose', len(ph) == 2 and 'phase 1' in _nohead(ph[0][1])[:80] and 'phase 3' in _nohead(ph[1][1])[:80], str([x[1][:60] for x in ph]))
        _cre_txt = open(cre, encoding='utf-8').read()
        _g2 = _cre_txt[_cre_txt.index('## S13-2G'):_cre_txt.index('## S13-3')]
        check('H6 S13-2G never hands the review to the user: no outputs path, no present_files of a packet, no new chat, no --resume step',
              '/mnt/user-data/outputs/{EXAM}_{pp.paper_slug(paper_id)}_review_packet' not in _g2 and 'present_files([_pkt])' not in _g2
              and 'AWAITING_REVIEW' not in _g2.split('PHASE 1')[1].split('PHASE 2')[0].replace("'AWAITING_REVIEW' is a LEGACY", ''),
              'phase-1 text still stages a packet for the user')
        _outs_before = sorted(os.listdir(OUT))
        _AENV = dict(os.environ, PYTHONPATH=W)
        g6 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}
        run_fence(ph[0][1], g6)
        check('H6 phase 1 writes NOTHING to the user outputs folder (contract: exactly the two files at the end)', sorted(os.listdir(OUT)) == _outs_before, str(sorted(set(os.listdir(OUT)) - set(_outs_before))))
        RQ = json.load(open(os.path.join(g6['REVIEW_DIR'], 'queue.json')))
        check('H6 review dir is internal (/home/claude), state REVIEW_RUNNING persisted', g6['REVIEW_DIR'].startswith(HOME) and json.load(open(bs_path))['state'] == 'REVIEW_RUNNING')
        pk = json.load(open(os.path.join(RQ['parts'][0]['dir'], 'review_packet.json')))
        check('H6 packet: md5 of the delivered docx, whole paper, exemplar slice for the paper subtopics', pk['paper_md5'] == hashlib.md5(open(docx, 'rb').read()).hexdigest() and sum(len(p_['qs']) for p_ in RQ['parts']) == MQ and pk['parts'][0]['exemplars'], str(list(pk['parts'][0]['exemplars']))[:100])
        _pk_keys = set().union(*[set(it) for part in pk['parts'] for it in part['items']])
        check('H6 packet items carry no key / difficulty / solution / per-option mechanisms', not (_pk_keys & {'difficulty', 'difficulty_plan', 'solution', 'answers', 'distractor_mechanisms', 'key', 'correct_option', 'band'}), str(sorted(_pk_keys)))
        mr = fences(f'{W}/Framework_MockReview.md')
        def _review(part_dir, disagree_q=None):
            g7 = {'WORK': part_dir, 'REVIEWER': 'sub-agent'}; run_fence(mr[0][1], g7); run_fence(mr[1][1], g7)
            qq = json.load(open(os.path.join(part_dir, 'queue.json')))
            ans = {str(it['q']): dict({c: 'ok' for c in bc.REVIEW_CHECKLIST}, own_key=('a, c' if it['q'] == 2 else 'abcd'[ANS[str(it['q'])] - 1]),
                                      confidence='high', selectivity_basis='clean', verdict='PASS', reason='') for it in qq['items']}
            if disagree_q and str(disagree_q) in ans:
                ans[str(disagree_q)]['own_key'] = 'abcd'[ANS[str(disagree_q)] % 4]
            json.dump(ans, open(os.path.join(part_dir, 'answers.json'), 'w'))
            run_fence(mr[2][1], g7); run_fence(mr[3][1], g7)
            return qq, json.load(open(os.path.join(part_dir, 'verdicts.json')))
        qq, VF = _review(RQ['parts'][0]['dir'], disagree_q=3)
        check('H6 reviewer queue: exam/slug from packet, every item with stem/options/exemplars', qq['exam'] == EXAM and all(it['stem'] and it['options'] for it in qq['items']) and qq['items'][0]['exemplars'], str(qq['items'][0])[:200])
        check('H6 verdicts written INSIDE the part folder, bound to the packet md5, key_agrees null, reviewer recorded', VF['paper_md5'] == pk['paper_md5'] and all(v['key_agrees'] is None for v in VF['items'].values()) and VF['reviewer'] == 'sub-agent' and sorted(os.listdir(OUT)) == _outs_before)
        # the sub-agent runs each script as a FRESH python process: WORK / REVIEWER come from the
        # environment (REVIEW_WORK / REVIEWER), never from a global it cannot have
        os.environ['REVIEW_WORK'] = RQ['parts'][0]['dir']; os.environ['REVIEWER'] = 'sub-agent'
        try:
            g7e = {}; run_fence(mr[0][1], g7e)
        finally:
            os.environ.pop('REVIEW_WORK', None); os.environ.pop('REVIEWER', None)
        check('H6 reviewer brief reads its part folder from the ENVIRONMENT (fresh process, no globals)',
              g7e.get('PACKET') is not None and g7e.get('WORK') == RQ['parts'][0]['dir'] and g7e.get('REVIEWER') == 'sub-agent')
        for p_ in RQ['parts'][1:]:
            _review(p_['dir'])
        g8 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id}; run_fence(ph[1][1], g8)
        kd = json.load(open(key_path)); bs = json.load(open(bs_path))
        check('H6 phase 3: key_agrees computed from sidecar answers (Q3 disagreement, MSQ Q2 agrees), state REVIEW_REPAIR, defects persisted',
              kd['concept_map']['1']['review']['key_agrees'] is True and kd['concept_map']['2']['review']['key_agrees'] is True and kd['concept_map']['3']['review']['key_agrees'] is False and bs['state'] == 'REVIEW_REPAIR' and bs['review_defects'] == ['3'], str((bs.get('state'), bs.get('review_defects'), kd['concept_map']['2']['review'].get('key_agrees'))))
        # round 2 (T5; 2026.11.15 G-07): a DELTA round over the repaired item only — every other item keeps its round-1
        # verdict, bound to its hash; the reviewer still disagrees on Q3 -> its DISPUTE chain
        shutil.copy(f'{TMP}/cert.json', f'{HOME}/{EXAM}_M{N}_item_sweep_certificate.json')
        g6b = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}; run_fence(ph[0][1], g6b)
        RQ2 = json.load(open(os.path.join(g6b['REVIEW_DIR'], 'queue.json')))
        check('H6 round 2 packet is a NEW round folder with ONLY the repaired item (delta, G-07)', g6b['REVIEW_DIR'].endswith('round2')
              and sorted(q for p_ in RQ2['parts'] for q in p_['qs']) == [3] and MQ > 1)
        for i_, p_ in enumerate(RQ2['parts']):
            _review(p_['dir'], disagree_q=3)
        g9 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id}; run_fence(ph[1][1], g9)
        _c_after = json.load(open(f'{HOME}/{EXAM}_M{N}_item_sweep_certificate.json'))
        check('H6 round 2 (OD-2026-11-09): the certificate is NOT rewritten NOT CERTIFIED (certified, no uncertified_items)', _c_after['uncertified_items'] == [] and _c_after['certified'] is True, str(_c_after))
        kd = json.load(open(key_path)); bs = json.load(open(bs_path))
        check('H6 round 2: Q3 enters its DISPUTE chain — never UNRESOLVED; REVIEWED, uncertified empty, review_summary recorded',
              not str(kd['concept_map']['3'].get('quality_status', '')).startswith('UNRESOLVED') and bs['state'] == 'REVIEWED'
              and bs['uncertified_items'] == [] and (bs.get('slot_chain') or {}).get('3', {}).get('kind') == 'dispute'
              and bs['review_summary']['repaired'] == ['3'] and bs['review_summary']['reviewer'] == ['sub-agent'], str(bs.get('slot_chain')))
        # v2026.11.09 — the dispute chain, end to end: S13-2L schedules a SWITCHED adjudication (delta round);
        # one agreement is not enough (the latest two on the current text must agree); the second certifies
        _l2l = fences(cre, '# ── S13-2L (v6.0) ──')
        check('H6 S13-2L fence found', len(_l2l) == 1)
        _bp_p = f'{HOME}/hs_bp.json'; json.dump(BP, open(_bp_p, 'w'))
        def _s13_2l():
            _gl = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'BP_SRC_PATH': _bp_p}
            try:
                run_fence(_l2l[0][1], _gl); return None
            except RuntimeError as _x:
                return str(_x)
        _m1 = _s13_2l(); bs = json.load(open(bs_path))
        check('H6 S13-2L: Q3 adjudication scheduled as a DELTA round with a switched reviewer (no content change)',
              _m1 and 'DELTA' in _m1 and bs['delta_qs'] == ['3'] and bs['delta_switch'] == ['3']
              and bs['slot_chain']['3']['attempts'][-1] == {'stage': 'adjudicate', 'outcome': 'pending'}, str((_m1, bs.get('delta_qs'))))
        for _rnd_d in (3, 4):
            gd = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}
            run_fence(ph[0][1], gd)
            RQd = json.load(open(os.path.join(gd['REVIEW_DIR'], 'queue.json')))
            if _rnd_d == 3:
                check('H6 delta round: a NEW delta folder carrying ONLY Q3, marked switch — in the FOLDER NAME too (the orchestrator sees only paths)',
                      gd['REVIEW_DIR'].endswith('delta3') and [q_ for p_ in RQd['parts'] for q_ in p_['qs']] == [3]
                      and all(p_.get('switch') and p_['dir'].endswith('_switch') for p_ in RQd['parts']), str(RQd)[:300])
            for p_ in RQd['parts']:
                _review(p_['dir'])
            run_fence(ph[1][1], {'EXAM': EXAM, 'N': N, 'paper_id': paper_id})
            bs = json.load(open(bs_path))
            if _rnd_d == 3:
                check('H6 delta round 3: one agreement after two disputes is NOT certification (chain still open)',
                      not bs['slot_chain']['3'].get('done'), str(bs['slot_chain']['3']))
                _m2 = _s13_2l(); bs = json.load(open(bs_path))
                check('H6 S13-2L: a second switched review is scheduled for Q3', _m2 and bs['delta_qs'] == ['3'], str(_m2))
        kd = json.load(open(key_path))
        check('H6 delta round 4: two consecutive agreeing reviews on the current text CERTIFY Q3 (chain closed, review bound to its hash)',
              bs['slot_chain']['3'].get('done') and bs['slot_chain']['3'].get('outcome') == 'adjudicate'
              and kd['concept_map']['3']['review']['key_agrees'] is True and kd['concept_map']['3']['review'].get('item_hash')
              and len(kd['concept_map']['3'].get('review_history') or []) >= 4, str(bs['slot_chain']['3']))
        _m3 = _s13_2l()
        check('H6 S13-2L: every chain closed and every item covered -> no further round (no raise)', _m3 is None, str(_m3))
        check('H6 the whole review left the user outputs folder untouched (T4/T5: exactly the paper so far)', sorted(os.listdir(OUT)) == _outs_before, str(sorted(os.listdir(OUT))))
        # 2026.11.09 review — LOOP GUARDS: a dispute attempt whose delta verdict is NOT_RUN or a same-session fallback
        # can never certify (E13); the attempt FAILS and the chain moves on — it is never queued again forever
        _kd_lg = json.load(open(key_path)); _bs_lg = json.load(open(bs_path))
        for _mode in ('not_run', 'same_session'):
            bs = json.load(open(bs_path))
            bs['slot_chain']['3'] = bc.slot_chain_record(bc.slot_chain_new('3', 'dispute'), 'adjudicate', 'pending')
            bs['delta_qs'], bs['delta_switch'], bs['delta_panel'] = ['3'], ['3'], []
            json.dump(bs, open(bs_path, 'w'))
            kd = json.load(open(key_path))                         # a fresh dispute: the latest independent verdict disagrees
            _h3 = kd['concept_map']['3']['review'].get('item_hash')
            kd['concept_map']['3'].setdefault('review_history', []).append(
                {'key_agrees': False, 'confidence': 'high', 'reviewer': 'sub-agent', 'item_hash': _h3})
            json.dump(kd, open(key_path, 'w'))
            ge = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}
            run_fence(ph[0][1], ge)
            _qp = os.path.join(ge['REVIEW_DIR'], 'queue.json'); RQe = json.load(open(_qp))
            for p_ in RQe['parts']:
                if _mode == 'not_run':
                    p_['error'] = 'sub-agent timed out twice'
                else:
                    _review(p_['dir']); p_['reviewer'] = 'same-session'
            json.dump(RQe, open(_qp, 'w'))
            run_fence(ph[1][1], {'EXAM': EXAM, 'N': N, 'paper_id': paper_id})
            bs = json.load(open(bs_path)); kd = json.load(open(key_path))
            check(f'H6 loop guard ({_mode}): the dispute attempt FAILS (no independent verdict) — the chain moves on',
                  bs['slot_chain']['3']['attempts'][-1]['outcome'] == 'fail' and not bs['slot_chain']['3'].get('done')
                  and bool((bs.get('review_hashes') or {}).get('3'))
                  and kd['concept_map']['3']['review'].get('item_hash') == (bs.get('review_hashes') or {}).get('3'),
                  str(bs['slot_chain']['3']))
            _me = _s13_2l(); bs = json.load(open(bs_path))
            check(f'H6 loop guard ({_mode}): S13-2L schedules the NEXT stage (replace) — not the same review again; Q3 covered',
                  any(w['q'] == '3' and w['action'] == 'replace' for w in bs.get('slot_chain_work') or [])
                  and '3' not in (bs.get('delta_qs') or []) and _me and 'SLOT-CHAIN' in _me, str((_me, bs.get('delta_qs'))))
        json.dump(_kd_lg, open(key_path, 'w')); json.dump(_bs_lg, open(bs_path, 'w'))
        # D0 is BOUNDED: a part disputing every item asks for a switched reviewer; one that never answers is asked
        # twice, then the first reviewer's disputes stand — phase 3 completes (never a loop)
        _kd_d0 = json.load(open(key_path)); _bs_d0 = json.load(open(bs_path))
        bs = json.load(open(bs_path)); bs['delta_qs'] = sorted(json.load(open(key_path))['concept_map'], key=int)
        bs['delta_switch'], bs['delta_panel'] = [], []
        json.dump(bs, open(bs_path, 'w'))
        g_d0 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}
        run_fence(ph[0][1], g_d0)
        RQ_d0 = json.load(open(os.path.join(g_d0['REVIEW_DIR'], 'queue.json')))
        for p_ in RQ_d0['parts']:
            _review(p_['dir'])
            _vfp = os.path.join(p_['dir'], 'verdicts.json'); _vf0 = json.load(open(_vfp))
            for _qk in _vf0['items']:
                _a0 = ANS[str(_qk)]
                _vf0['items'][_qk]['own_key'] = 'abcd'[_a0 % 4] if isinstance(_a0, int) else 'b'   # a wrong key
            json.dump(_vf0, open(_vfp, 'w'))
        _d0_seq = []
        for _i in range(3):
            try:
                run_fence(ph[1][1], {'EXAM': EXAM, 'N': N, 'paper_id': paper_id}); _d0_seq.append('done')
            except RuntimeError as _x:
                _d0_seq.append('void' if 'REVIEW-VOID' in str(_x) else 'other:' + str(_x)[:60])
            if _d0_seq[-1] == 'done':
                break
        check('H6 D0 bounded: a switched reviewer that never answers is asked twice, then phase 3 completes (disputes stand)',
              _d0_seq == ['void', 'void', 'done'], str(_d0_seq))
        json.dump(_kd_d0, open(key_path, 'w')); json.dump(_bs_d0, open(bs_path, 'w'))
        # T7: a part whose reviewer produced nothing (after the retry) -> NOT_RUN records, never a stop
        _kd_save = json.load(open(key_path)); _bs_save = json.load(open(bs_path))
        _bs_t7 = dict(_bs_save, review_round=0); json.dump(_bs_t7, open(bs_path, 'w'))
        g6c = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id, 'EXEMPLAR_BANK_PATH': g4['EXEMPLAR_BANK_PATH'], 'AUDIT_ENV': _AENV}; run_fence(ph[0][1], g6c)
        RQ3 = json.load(open(os.path.join(g6c['REVIEW_DIR'], 'queue.json')))
        RQ3['parts'][0]['error'] = 'sub-agent timed out twice'
        json.dump(RQ3, open(os.path.join(g6c['REVIEW_DIR'], 'queue.json'), 'w'))
        g10 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id}; run_fence(ph[1][1], g10)
        kd3 = json.load(open(key_path))
        check('H6 T7: no verdict for a part -> every item NOT_RUN with the reason; no exception, no user step',
              all((kd3['concept_map'][str(q_)]['review'] or {}).get('status') == 'NOT_RUN' and 'timed out' in kd3['concept_map'][str(q_)]['review']['reason'] for q_ in RQ3['parts'][0]['qs']))
        _lv_nr = {}
        ac._reset(); ac.gate_review({'concept_map': kd3['concept_map'], '_mockN': N, 'registry': {'question_index': [{'mock': N, 'paper_id': paper_id, 'qindex_cert': {'producer_release': '2026.11.03'}}]}}, type('A', (), {'phase': 'final'})())
        _lv_nr = [l_ for l_, c_, m_ in ac.RESULTS if c_ == 'A-REVIEW']
        check('H6 T7: the auditor reports NOT_RUN as WARN, never FAIL', _lv_nr == ['WARN'], str(_lv_nr))
        json.dump(_kd_save, open(key_path, 'w')); json.dump(_bs_save, open(bs_path, 'w'))
        # T8: a legacy AWAITING_REVIEW paper with a PREFIXED, SANITISED verdict upload is found by CONTENT
        s412 = fences(cre, 'S4-12 legacy verdict lookup')
        check('H6 S4-12 legacy lookup fence present', len(s412) == 1)
        _vf_legacy = dict(VF, exam_code=EXAM, paper_md5=hashlib.md5(open(docx, 'rb').read()).hexdigest())
        json.dump(_vf_legacy, open(f'{UPL}/ed4a4461-{EXAM}_SUBJ_General_Intelligence__Reasoning_02_review_verdicts.json', 'w'))
        json.dump(dict(_vf_legacy, paper_md5='other'), open(f'{UPL}/0badc0de-{EXAM}_x_review_verdicts.json', 'w'))
        g11 = {'EXAM': EXAM, 'N': N, 'paper_id': paper_id}; run_fence(s412[0][1], g11)
        check('H6 T8/E10: legacy verdict file found by content despite the upload prefix and sanitised slug; another md5 ignored', isinstance(g11.get('LEGACY_VERDICTS'), dict) and g11['LEGACY_VERDICTS']['paper_md5'] != 'other')
        for _f in os.listdir(UPL):
            if _f.endswith('_review_verdicts.json'): os.remove(os.path.join(UPL, _f))
        # A8/U8: a legacy packet and per-batch docx left in outputs are cleared before S13-7 check 6
        _leg = [f'{EXAM}_{pp.paper_slug(paper_id)}_review_packet.zip', f'{EXAM}_{pp.paper_slug(paper_id)}_Q1to2.docx']
        for _f in _leg: open(os.path.join(OUT, _f), 'w').write('x')
        _clr = fa.outputs_to_clear(os.listdir(OUT), docx_name=os.path.basename(docx), reg_name=f'{EXAM}_registry.json')
        check('H6 A8: fa.outputs_to_clear names this run\'s leftovers (legacy packet, per-batch docx) and never the paper', sorted(_clr) == sorted(_leg) and os.path.basename(docx) not in _clr, str(_clr))
        for _f in _leg: os.remove(os.path.join(OUT, _f))

        # ═══ H7  S13-4 commit -> S13-4c final audit (registry only) -> MockDeliver 3f -> footer ═══
        print('H7 commit -> final audit -> deliver')
        final = fa.commit_registry(copy.deepcopy(reg), {}, BP, N, paper_id=paper_id, batches_completed=1, axis2_window_counts={}, passage_present=False, di_present=False,
                                   figural_present=False, concept_map=kd['concept_map'], quality_readiness=bs['quality_readiness'],
                                   shape_infeasible=list((bs.get('shape_plan') or {}).get('_infeasible') or []))
        check('H7 every field commit_registry carries is a field the auditor overlay reads (QINDEX_V590_FIELDS <= _QQ_V590_FIELDS)',
              set(fa.QINDEX_V590_FIELDS) <= set(ac._QQ_V590_FIELDS), str(set(fa.QINDEX_V590_FIELDS) - set(ac._QQ_V590_FIELDS)))
        check('H7 commit carries pattern_key / scheme_grammar / key_set_size (fields the S13-4c gates read)', all(k in final['registry']['question_index'][0]['questions'][1] for k in ('pattern_key', 'scheme_grammar', 'key_set_size')), str(sorted(final['registry']['question_index'][0]['questions'][1]))[:300])
        check('H7 commit carries review + quality_status per question', final['ok'] and all('review' in qq and 'quality_status' in qq for qq in final['registry']['question_index'][0]['questions']))
        reg_path = f'{HOME}/{EXAM}_registry.json'; json.dump(final['registry'], open(reg_path, 'w')); prev_path = reg_path
        r2, lv2 = audit('final', ['--profile', prof_path, '--certificate', f'{HOME}/{EXAM}_M{N}_item_sweep_certificate.json'])   # NO --key: registry overlay only
        check('H7 final audit: A-CERT confirms the CERTIFIED docx, A-DISTRACTOR ok for the MSQ item from the registry record', lv2.get('A-CERT') in ('OK', 'ok') and lv2.get('A-DISTRACTOR') != 'FAIL', str((lv2.get('A-CERT'), lv2.get('A-DISTRACTOR'))))
        check('H7 final audit without sidecar (OD-2026-11-09): A-REVIEW OK — every review bound to the delivered text (computed hashes) — A-QUALITYSTATUS OK CERTIFIED, rc 0',
              lv2.get('A-REVIEW') in ('OK', 'ok') and lv2.get('A-QUALITYSTATUS') in ('OK', 'ok') and r2.returncode == 0,
              str((lv2.get('A-REVIEW'), lv2.get('A-QUALITYSTATUS'), r2.returncode, [l for l in r2.stdout.split('\n') if l.startswith('[ FAIL]')][:5])))
        # MockDeliver 3f
        t3 = open(f'{W}/Framework_MockDeliver.md', encoding='utf-8').read(); i = t3.find('# ── S1-2 item 3f (executable'); j = t3.find('# Build the tag-value lookup table', i)
        R = json.load(open(reg_path)); FP_BEFORE = pp.registry_fingerprint(R)
        gD = {'blueprint': BP, 'registry': R, 'N': N, 'ACCEPT_UNCERTIFIED': False}
        try:
            run_fence(t3[i:j], gD); refused = False
        except SystemExit:
            refused = True
        check('H7 MockDeliver delivers the v5.96 paper with NO flag (it is never uncertified, OD-2026-11-09)', not refused and gD.get('UNCERTIFIED_ITEMS') == [])
        # LEGACY: a registry committed NOT CERTIFIED by 2026.11.03-2026.11.08.1 keeps its old behaviour
        RL = copy.deepcopy(R)
        for _qq in RL['question_index'][0]['questions']:
            if str(_qq['q']) == '3':
                _qq['quality_status'] = 'UNRESOLVED(A-REVIEW)'
        FP_BEFORE = pp.registry_fingerprint(RL)
        gD = {'blueprint': BP, 'registry': RL, 'N': N, 'ACCEPT_UNCERTIFIED': False}
        try:
            run_fence(t3[i:j], gD); refused = False
        except SystemExit as e:
            refused = (e.code == 0)
        check('H7 MockDeliver still refuses a LEGACY NOT CERTIFIED registry (SystemExit 0 before render)', refused)
        gD = {'blueprint': BP, 'registry': RL, 'N': N, 'ACCEPT_UNCERTIFIED': True}; run_fence(t3[i:j], gD)
        check('H7 MockDeliver --accept-uncertified (legacy) records registry.accepted_uncertified and proceeds', gD['registry']['accepted_uncertified'][paper_id]['items'] == ['3'] and gD['UNCERTIFIED_ITEMS'] == ['3'])
        check('H7 registry change detected -> delivered under §8', pp.registry_changed(FP_BEFORE, gD['registry']) is True)
        # D5 (GAP-2026-11-04 U9): a paper committed NOT CERTIFIED under 2026.11.03 ONLY by the
        # unmeasured template cap (readiness G-TEMPLATE STALE) is re-certified at Deliver with no flag
        R5 = copy.deepcopy(R)
        _e5 = R5['question_index'][0]
        for _qq in _e5['questions']:
            _qq['quality_status'] = 'UNRESOLVED(A-TEMPLATE)' if str(_qq['q']) in ('1', '2') else 'CERTIFIED'
        _e5['quality_readiness'] = {'controls': {'G-TEMPLATE': {'status': 'STALE', 'reason': 'section_rules.md lacks fingerprint_max_per_paper'}}, 'degraded': ['G-TEMPLATE']}
        # a paper COMMITTED under 2026.11.03 has no qindex_cert.stamps_release
        R5b = copy.deepcopy(R5)                                  # same stamps, written by THIS release
        _e5['qindex_cert'] = {k: v for k, v in (_e5.get('qindex_cert') or {}).items() if k != 'stamps_release'}
        _e5['qindex_cert']['producer_release'] = '2026.11.03'
        gD5b = {'blueprint': BP, 'registry': R5b, 'N': N, 'ACCEPT_UNCERTIFIED': False}
        try:
            run_fence(t3[i:j], gD5b); _refused5b = False
        except SystemExit:
            _refused5b = True
        check('H7 D5: an A-TEMPLATE stamp written by THIS release (a measured concept cap) is never re-certified — refused without the flag',
              _refused5b is True and R5b['question_index'][0]['qindex_cert'].get('stamps_release') == bc.STAMPS_RELEASE)
        gD5 = {'blueprint': BP, 'registry': R5, 'N': N, 'ACCEPT_UNCERTIFIED': False}
        try:
            run_fence(t3[i:j], gD5); _refused5 = False
        except SystemExit:
            _refused5 = True
        check('H7 D5: a dormant-control-only NOT CERTIFIED paper is re-certified at Deliver (no --accept-uncertified, informational line)',
              not _refused5 and gD5.get('RECERTIFIED_ITEMS') == ['1', '2'] and gD5.get('UNCERTIFIED_ITEMS') == [], str((gD5.get('RECERTIFIED_ITEMS'), gD5.get('UNCERTIFIED_ITEMS'))))
        # footer lines
        fl = bc.degraded_footer_line(bs['quality_readiness'])
        check('H7 DeliveryFooter QUALITY_FOOTER_LINE from the persisted readiness', isinstance(fl, str) and fl)
        check('H7 certificate_uncertified(registry stamps) == batch_state uncertified_items == [] (nothing uncertified, OD-2026-11-09)',
              bc.certificate_uncertified({str(qq['q']): qq.get('quality_status') for qq in R['question_index'][0]['questions']}) == bs['uncertified_items'] == [])

        # ═══ H-DL  difficulty layer, three synthetic exams (release 2026.11.08) ═══
        print('H-DL difficulty layer: Step 5 bank -> Create S3-8L/S3-12c/CHECK 3c/S13-2G/S13-2L -> commit -> audit -> footer')
        _dl_handshake(check, ROOT, run_fence, W)
        print('H-LB band swap + paired upgrade through the spec\'s own S13-2L / S13-2R (release 2026.11.09)')
        _lb_swap_handshake(check, ROOT, run_fence, W)
        print('H-DOWN downstream replay of a v5.96 paper through every later reader (release 2026.11.09)')
        _downstream_replay(check)
        print('H-BV every question verified in its own batch: author packet -> STEP A2 -> commit -> audit -> deliver (release 2026.11.11)')
        _bv_handshake(check, ROOT, run_fence, W)
        print('H-BC every question SETTLED in its batch: ladder, adjudication, re-key, R5b, NO-MODEL, STEP A3, byte-copy Final Assembly (release 2026.11.16)')
        _bc_handshake(check, ROOT, W)
        print('H-R3 difficulty yardstick: Step 5 ladder -> staging -> STEP A packet -> STEP A2 placement -> S13-2L.0 -> commit -> audit (release 2026.11.21)')
        _r3_handshake(check, ROOT, run_fence, W)

    finally:
        shutil.rmtree(ROOT, ignore_errors=True)
    print(f'\nHANDSHAKE AUDIT: {len(OK)} ok, {len(BAD)} FAIL')
    for b in BAD:
        print('   FAIL', b)
    if len(OK) + len(BAD) != EXPECTED_CHECKS:
        print(f'HANDSHAKE AUDIT: ran {len(OK) + len(BAD)} checks, expected {EXPECTED_CHECKS} — a check was '
              f'skipped or added without updating EXPECTED_CHECKS (a skipped handshake is not a passing one)')
        return False
    return not BAD


EXPECTED_CHECKS = 267   # 2026.11.23 (GAP-2026-11-17-CERT-DISCLOSED-CONTRACT): H5 certificate schema 3; +4 H5-CERT-DISCLOSED (real S13-2F -> S13-4c on an ESCALATED item; hand-edit refused); +1 H5-V7-SIDECAR (per-batch label truth); 2026.11.21 (Cluster R3): +17 H-R3 (the difficulty yardstick, Step 5 -> Create -> commit -> audit); +1 H-BC-3R (a solver split is rewritten once in the new modes); H-BV / H-BC pinned to mode br1; 2026.11.16 (GAP-2026-11-14-BATCH-COMPLETE): +25 H-BC (job folders only — TEST-NO-HANDWRITE); 2026.11.15: +1 H-BV S13-1B is a check (G-06); 2026.11.14: +1 H-BV carry (BV-13) and S13-1B; 2026.11.13: +1 H-BV rubric (BV-10), +3 H-NS (bootstrap --session-start runs what the read does not serve);   # 2026.11.11 (GAP-2026-11-11-BATCH-VERIFICATION): +25 H-BV (author packet -> STEP A2 -> commit -> audit -> deliver);            # 2026.11.10 (GAP-2026-11-10 G-10): H-LB rewritten for the SC2 endings (8 checks replace 13 swap / upgrade / panel / forced checks), H5 +1 LB2 basis, H-DL forced -> last resort (same 4 x 3); before: 79 + 44 H-DL (2026.11.08) -> 2026.11.09: H6 dispute chain end to end (+10), legacy Deliver (+1), H-DL chains / forced / footer (+4 x 3), H-LB swap / upgrade (+5), loop guards (+4), hand-over edges (+3), S13-4c stop (+1), NOT_RUN edges (+2), forced_refused (+1), S13-2F replace slice (+1), D0 bound (+1), H-DOWN replay (+25)


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
