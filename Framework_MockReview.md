# Framework_MockReview v2.1.0 — Independent Paper Review: the INTERNAL REVIEWER BRIEF of Create S13-2G
# v2.1.0 — 2026-11-08 — GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER (D1 (b), D4; paired with MockTestCreate
#   v5.94 S13-2G phase 3 DL1). The reviewer's band is BINDING when it cites an exemplar (Create takes
#   the LOWEST independent band). NEW optional key `concepts_used`: concepts the reviewer's OWN solution
#   used, SELECTED from the part's `concept_vocabulary` (organic papers; [] otherwise). Create scores
#   the ruler on the lower of the author's and reviewer's lists. Isolation and checklist unchanged.
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockReview.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.11.06 (GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.
#
# WHY THIS REVIEW EXISTS (measured, not assumed). Every verification of the incident paper —
#   answer, difficulty rating, "is a second option defensible" — ran in the context that WROTE
#   the item and agreed with itself (GAP G12). A context that has not seen the solution is
#   the only reader that cannot be anchored by having written it. The packet therefore
#   carries: the paper (docx), the exemplar-bank slice for the paper's subtopics (real PYQ
#   items per difficulty band, so the band judgement has a BENCHMARK, G07), the eight-field
#   checklist (bc.REVIEW_CHECKLIST) and paper_md5 — nothing else (bc.review_packet strips
#   difficulty/solution/rationale/author_notes/band fields; its self-test asserts it).
#
# ROUTE: routed WITH MockCreate / TestCreate (routes.json) — it is verified by bootstrap with
#   the rest of the corpus and read by the reviewer from /tmp/fw_effective. Engine:
#   blueprint_core.py only. The review itself is CLASS J over the part folder.
#
# INPUTS (given by Create S13-2G phase 2 — never by the user), as ENVIRONMENT variables of each
#   python script (REVIEW_WORK, REVIEWER), because every bash call is a fresh python process:
#   WORK     = the part folder, /home/claude/[ExamCode]_M[N]_review/round<k>/part<j>/, holding
#              review_packet.json (this part's items) and [ExamCode]_[slug]_Create.docx
#   REVIEWER = 'sub-agent' (a fresh context — the default) | 'same-session' (D1 fallback)
#   The reviewer reads NOTHING outside WORK except this spec: not the author's key sidecar,
#   not the batch state, not the registry, not the figure manifest, not any notes. Isolation
#   is by instruction (the reviewer shares the session's filesystem) — owner decision D4;
#   key_agrees is computed only by the author's session (S13-2G phase 3), never here.
#
# OUTPUT (internal, never delivered): WORK/verdicts.json — bc.review_verdict_file, bound to the
#   paper's md5. Create S13-2G phase 3 merges the parts (bc.review_merge_parts) and binds them.

# §1 — SESSION START

## S1-1 — Open the part folder (DETERMINISTIC)

  ```python
  # ── S1-1 (executable; WORK and REVIEWER are set by Create S13-2G phase 2) ─────────
  import glob, json, os, hashlib
  import blueprint_core as bc
  # WORK / REVIEWER come from the environment of the script (Create S13-2G phase 2 runs it as
  # `REVIEW_WORK=<part dir> REVIEWER=<kind> python3 - <<'EOF'`), else from an earlier binding
  # in the same python process.
  WORK = os.environ.get('REVIEW_WORK') or globals().get('WORK')
  REVIEWER = os.environ.get('REVIEWER') or globals().get('REVIEWER') or 'sub-agent'
  _pk_path = os.path.join(str(WORK or ''), 'review_packet.json')
  PACKET = None
  try:
      PACKET = json.load(open(_pk_path, encoding='utf-8'))
  except (OSError, ValueError) as _e:
      # never a stop and never a question to the user: the reviewer reports the failure in
      # its one-line reply ("REVIEW FAILED ..."); S13-2G retries once, then falls back (D1).
      print(f"REVIEW FAILED: no readable review_packet.json in {WORK!r} ({type(_e).__name__}: {_e})")
  if PACKET is not None:
      _docx = sorted(glob.glob(os.path.join(WORK, '*_Create.docx')))
      DOCX = _docx[0] if _docx else None
      EXAM = str(PACKET.get('exam') or '')
      PAPER_SLUG = str(PACKET.get('paper_slug') or '')
      REVIEW_ROUND = int(PACKET.get('review_round') or 1)
      PAPER_MD5 = PACKET.get('paper_md5')
      # The docx in the folder MUST be the paper the md5 names — otherwise the verdicts would
      # bind to a paper nobody read. A mismatch is recorded and the file still reviewed
      # (recorded only — the verdicts carry the packet's paper_md5 and bind as usual; a part
      # phase 3 cannot bind is recorded NOT_RUN, a WARN — OD-1).
      DOCX_MD5 = hashlib.md5(open(DOCX, 'rb').read()).hexdigest() if DOCX else None
      MD5_MATCH = (DOCX_MD5 == PAPER_MD5)
      if not MD5_MATCH:
          print(f"MockReview S1-1: WARNING — part docx md5 {DOCX_MD5} != packet paper_md5 {PAPER_MD5}.")
      N_ITEMS = int(PACKET.get('n_items') or 0)
      PARTS = PACKET.get('parts') or []
      print(f"MockReview ({REVIEWER}): {EXAM} {PAPER_SLUG} (review round {REVIEW_ROUND}) — {N_ITEMS} items; "
            f"checklist = {list(bc.REVIEW_CHECKLIST)}")
  ```

## S1-2 — Build the work queue (DETERMINISTIC)

  One file per part, each item with its stem, options, figure file names (the images are
  inside the docx — the reviewer opens the docx for figural items), the content record the
  author committed to (class word, stem agents, distractor mechanisms — these are the
  author's CLAIMS the reviewer tests, not the answer) and the exemplar slice for its
  subtopic. The queue is what Phase B reads; nothing is judged here.

  ```python
  # ── S1-2 (executable) ──────────────────────────────────────────────────────────
  QUEUE = []
  for _part in (PARTS if PACKET is not None else []):   # S1-1 printed REVIEW FAILED otherwise
      for _it in (_part.get('items') or []):
          _sid = str(_it.get('subtopic_id') or '')
          _ex = {c: v for c, v in (_part.get('exemplars') or {}).items()
                 if _sid == c or _sid.startswith(c + '.')} or (_part.get('exemplars') or {})
          QUEUE.append({'part': _part.get('part'), 'q': _it.get('q'), 'subtopic_id': _sid,
                        'stem': _it.get('stem'), 'options': _it.get('options'),
                        'figures': _it.get('figures') or [],
                        'author_claims': {'class_word': _it.get('class_word'),
                                          'stem_agents': _it.get('stem_agents'),
                                          'distractor_mechanisms_recorded': _it.get('distractor_mechanisms_recorded'),
                                          'content_record': _it.get('content_record') or {}},
                        'exemplars': _ex})
  QUEUE.sort(key=lambda r: int(r['q'] or 0))
  # v2.1.0: the controlled concept vocabulary (organic ruler items only; [] otherwise) — the
  # reviewer SELECTS its concepts_used from it (§2); it is the same list for every part.
  CONCEPT_VOCABULARY = next((list(_p.get('concept_vocabulary') or []) for _p in PARTS
                             if _p.get('concept_vocabulary')), []) if PACKET is not None else []
  if PACKET is not None:
      json.dump({'exam': EXAM, 'paper_slug': PAPER_SLUG, 'paper_md5': PAPER_MD5, 'docx': DOCX,
                 'review_round': REVIEW_ROUND, 'reviewer': REVIEWER, 'items': QUEUE,
                 'concept_vocabulary': CONCEPT_VOCABULARY},
                open(os.path.join(WORK, 'queue.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
      if len(QUEUE) != N_ITEMS:
          print(f"MockReview S1-2: queue holds {len(QUEUE)} items but the packet declares {N_ITEMS} — "
                "reviewing what is present; S13-2G phase 3 records the rest as NOT_RUN.")
      print(f"MockReview S1-2: queue written — {len(QUEUE)} items; figural items: "
            f"{sum(1 for r in QUEUE if r['figures'])}; concept vocabulary: "
            f"{len(CONCEPT_VOCABULARY)} entr{'y' if len(CONCEPT_VOCABULARY) == 1 else 'ies'}.")
  ```

# §2 — THE REVIEW (CLASS J — model judgement over the queue; NO python in this section)

## S2-1 — What the reviewer is, and is not

  The reviewer SOLVES each item cold, as a candidate would, and then tests the author's
  claims against what it found. It does not know the key, the intended band or the
  author's rationale, and it must not try to infer them from the author_claims block (the
  class word, the stem agents and the COUNT of recorded distractor mechanisms say what the
  author MEANT to test — the per-option mechanism list is withheld on purpose: it would
  give the key away by elimination — the reviewer decides
  whether the item as written does that). The exemplar slice is the ONLY difficulty
  benchmark: "Hard" means "as hard as the exam's own Hard PYQ for this cell", not "hard for
  me". For a figural item the reviewer opens the docx (view the page) — it never rates a
  structure from its file name. One pass, every item; nothing is skipped because it "looks
  fine".

## S2-2 — The eight checklist fields (bc.REVIEW_CHECKLIST, in this order, every item)

  ```
  # CLASS: J — one record per item, written by the model into
  # WORK/answers.json as {"<q>": {...}} with EXACTLY these keys:
  #
  #   own_key                      : the answer the reviewer derived on its own —
  #                                  a letter / position ("b", "(c)", 3), a sorted list for
  #                                  a multi-select ("a, c"), or the numeric value for a NAT
  #                                  (with unit-free number). NEVER blank: if the reviewer
  #                                  cannot decide, write the best candidate AND set
  #                                  confidence "low".
  #   single_answer                : "yes" | "no: <which other option is also defensible
  #                                  and why>" — the G02 test. Two defensible options is a
  #                                  FAIL whatever the key turns out to be.
  #   leak_or_paraphrase           : "none" | "<what in the stem gives the answer away, or
  #                                  which PYQ/exemplar it paraphrases>" — the G03/G09 test
  #                                  against the exemplar slice and against the stem's own
  #                                  wording (named mechanism, named product, trailing
  #                                  placeholder that is asked).
  #   difficulty_band_with_exemplar: "<Easy|Medium|Hard>, like exemplar <cell>/<index>" —
  #                                  the band the item SITS in next to the real PYQ of its
  #                                  cell; "no exemplar for this cell" when the slice is
  #                                  empty (then confidence "low" for this field only is
  #                                  acceptable; do not invent a benchmark). v2.0.1
  #                                  (GAP-2026-11-05 DL-52): this field HAS a consumer —
  #                                  Create S13-2G phase 3 compares it with the slot's
  #                                  scheduled band (the packet still carries NO band,
  #                                  NO difficulty_obs, NO level record — the reviewer
  #                                  never sees the schedule); "below" on a Hard slot is
  #                                  v2.1.0 (GAP-2026-11-07, DL1): BINDING — Create takes
  #                                  the LOWEST band of the independent controls; "below"
  #                                  the slot in round 1 is repaired, in round 2 it is
  #                                  the disclosed last resort. Only a band that names an
  #                                  exemplar counts (no benchmark, no control). Judge from
  #                                  the exemplar's CONTENT (structures, options, key),
  #                                  never from its length.
  #   distractor_existence_and_class: for EACH wrong option, one clause: "<label>: <real
  #                                  species/value of the same class, wrong because ...>" or
  #                                  "<label>: NOT a credible distractor (<impossible
  #                                  structure / wrong class / duplicate of ...>)" — the
  #                                  G04/G06 test.
  #   consistency_and_names        : "ok" | "<formula/name/count/figure that disagrees with
  #                                  the stem or with another option>" — the G08/G10 test
  #                                  (IUPAC name vs drawn structure, counts, units, a
  #                                  reagent named in the stem but absent in the scheme).
  #   confidence                   : "high" | "medium" | "low" — the reviewer's confidence
  #                                  in its OWN key and the fields above. "low" is a defect
  #                                  the author's session repairs; it is never a courtesy.
  #   selectivity_basis            : "clean" | "contested: <reason>" (the word
  #                                  "contested" first — the engine tests the prefix) — would a strong
  #                                  candidate and a weak one be separated by this item for
  #                                  the RIGHT reason (knowledge the subtopic tests), or
  #                                  for a wrong one (ambiguity, trivia, a trick of
  #                                  wording)? "contested" is a defect.
  #
  #   plus one OPTIONAL key (v2.1.0 — outside the eight-key checklist):
  #   concepts_used                : the named concepts YOUR OWN solution relied on (the
  #                                  reactions, rules, mechanisms you had to apply), as a
  #                                  list of `label` strings SELECTED from queue.json
  #                                  'concept_vocabulary'; a concept outside it is written
  #                                  "other:<name>". [] when the queue carries no vocabulary
  #                                  or no listed concept applies. Write what YOU used —
  #                                  never guess what the author meant (the author's list is
  #                                  not in the packet, on purpose).
  #
  #   plus two closing keys:
  #   verdict                      : "PASS" | "FAIL" — FAIL when single_answer starts with
  #                                  "no", leak_or_paraphrase is not "none", any distractor
  #                                  is "NOT a credible distractor", consistency_and_names
  #                                  is not "ok", confidence is "low", or selectivity_basis
  #                                  is "contested". Otherwise PASS.
  #   reason                       : one sentence the author can act on ("Option (c) is
  #                                  also the major product under kinetic control — stem
  #                                  must fix the temperature"); "" on a clean PASS.
  #
  # key_agrees is NOT written here (the reviewer has no key); the author's session fills
  # it (Create S13-2G phase 3, bc.review_key_agreement). Do not write it.
  ```

  Working order per item: read the stem and all options (open the docx page for a figure)
  → derive own_key → test single_answer → scan for leak_or_paraphrase against the
  exemplar slice → place the band beside the exemplars → classify every distractor → check
  names / counts / figures → set confidence and selectivity_basis → concepts_used (when the
  queue carries a vocabulary) → verdict + reason. Write
  the item's record before moving to the next one; a long paper is written in the packet's
  parts (<= 30 items each) so the file is never lost to a session boundary.

# §3 — ASSEMBLE, SELF-CHECK, DELIVER (DETERMINISTIC)

## S3-1 — Build and bind-check the verdict file

  ```python
  # ── S3-1 (executable; after every item in answers.json has a record) ──────────
  import json, os
  import blueprint_core as bc
  WORK = os.environ.get('REVIEW_WORK') or globals().get('WORK')      # the part folder (S1-1)
  REVIEWER = os.environ.get('REVIEWER') or globals().get('REVIEWER') or 'sub-agent'
  _q = json.load(open(os.path.join(WORK, 'queue.json'), encoding='utf-8'))
  _ans_path = os.path.join(WORK, 'answers.json')
  ANSWERS = json.load(open(_ans_path, encoding='utf-8')) if os.path.exists(_ans_path) else {}
  _expected = [str(r['q']) for r in _q['items']]
  _missing = [q for q in _expected if q not in ANSWERS]
  if _missing:
      # OD-1: never a stop. A missing record is written as 'not assessed' with confidence
      # 'low' (bc.review_verdict_file) so the author's phase 3 treats it as a defect and
      # the item gets a second look — a silent PASS is the one outcome this step must not
      # produce.
      print(f"MockReview S3-1: {len(_missing)} item(s) have no record ({_missing[:10]}{'...' if len(_missing) > 10 else ''}) "
            "— written as 'not assessed' / confidence low (a defect: repaired and re-reviewed after "
            "round 1; UNRESOLVED(A-REVIEW) after round 2).")
      for q in _missing:
          ANSWERS[q] = {}
  VERDICT_FILE, _probs = bc.review_verdict_file(_q['exam'], _q['paper_slug'], _q['paper_md5'], ANSWERS,
                                                reviewer=REVIEWER)
  VERDICT_FILE['review_round'] = int(_q.get('review_round') or 1)
  for _p in _probs:
      print("MockReview S3-1: " + _p)
  _bind = bc.bind_review_verdicts(VERDICT_FILE, _q['paper_md5'], len(_expected))
  print(f"MockReview S3-1: self-bind {'OK' if _bind['ok'] else 'PROBLEMS: ' + '; '.join(_bind['problems'])}; "
        f"defects flagged for the author's repair: {_bind['defects'] or 'none'}")
  _n_fail = sum(1 for r in VERDICT_FILE['items'].values() if r.get('verdict') == 'FAIL')
  print(f"MockReview S3-1: {len(VERDICT_FILE['items'])} items reviewed — {_n_fail} FAIL, "
        f"{len(VERDICT_FILE['items']) - _n_fail} PASS; low-confidence: "
        f"{sum(1 for r in VERDICT_FILE['items'].values() if r.get('confidence') == 'low')}; "
        f"contested: {sum(1 for r in VERDICT_FILE['items'].values() if str(r.get('selectivity_basis', '')).startswith('contested'))}.")
  ```

## S3-2 — Write the part verdicts (internal — NEVER delivered)

  ```python
  # ── S3-2 (executable) ──────────────────────────────────────────────────────────
  # The verdict file stays in the part folder; Create S13-2G phase 3 reads it. It is never
  # written to the user's output folder and never presented (GAP-2026-11-04 A2).
  out = os.path.join(WORK, 'verdicts.json')
  json.dump(VERDICT_FILE, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
  print(f"REVIEW DONE {len(VERDICT_FILE['items'])} items -> {out}")
  ```
  The reviewer's reply to the author session is that ONE line ("REVIEW DONE <n> items" or
  "REVIEW FAILED <reason>"). No file is presented; nothing is asked of the user.

# §4 — CHECKLIST (all 7 items must PASS)

  [ ] 1. Only the part folder (WORK) and this spec were read — no key sidecar, batch state,
         registry, figure manifest or notes (S1-1; D4).
  [ ] 2. The docx md5 was compared with paper_md5 and the result printed (S1-1).
  [ ] 3. Every item in the queue has a record with all eight checklist keys, verdict and
         reason (S2-2 / S3-1 — a blank field is 'not assessed' + confidence low, never a PASS).
  [ ] 4. key_agrees is null on every record — the reviewer never saw the key (S2-2).
  [ ] 5. bc.bind_review_verdicts on the file reports ok (S3-1).
  [ ] 6. verdicts.json written INSIDE WORK; nothing presented, nothing asked of the user (S3-2).
  [ ] 7. When queue.json carries a concept_vocabulary, every record carries concepts_used
         selected from it (or "other:<name>"), describing the reviewer's OWN solution (§2).

# END OF Framework_MockReview v2.1.0
