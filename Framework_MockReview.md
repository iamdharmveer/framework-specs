# Framework_MockReview v1.0.0 — Universal Independent Paper Review (fresh-context second reader)
# v1.0.0 — 2026-11-03 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY G12 (owner decision OD-5 (a):
#   MANDATORY independent review on every paper, WITH correction — paired with
#   MockTestCreate v5.90 S13-2G, blueprint_core v1.30 Cluster QQ, audit_canonical v2.35
#   A-REVIEW). This step is the PHASE 2 of the two-session review protocol: it runs in a
#   NEW chat, with ONLY the review packet attached, and never sees the answer key, the
#   author's notes, the scheduled difficulty bands or the registry. It writes
#   [ExamCode]_[slug]_review_verdicts.json (bc.review_verdict_file), bound to the paper's
#   md5, which the author's chat binds with `TestCreate --resume` / `MockCreate --resume`
#   (S13-2G phase 3: key_agrees is filled THERE from the sidecar; flagged items are REPAIRED
#   through §Q8b-LADDER, not merely listed). OD-1: this step never stops on a quality
#   finding — a finding is a record on the item; the only [HS:INPUT] is "no packet attached".
#
# WHY THIS STEP EXISTS (measured, not assumed). Every verification of the incident paper —
#   answer, difficulty rating, "is a second option defensible" — ran in the context that WROTE
#   the item and agreed with itself (GAP G12). A context that has not seen the solution is
#   the only reader that cannot be anchored by having written it. The packet therefore
#   carries: the paper (docx), the exemplar-bank slice for the paper's subtopics (real PYQ
#   items per difficulty band, so the band judgement has a BENCHMARK, G07), the eight-field
#   checklist (bc.REVIEW_CHECKLIST) and paper_md5 — nothing else (bc.review_packet strips
#   difficulty/solution/rationale/author_notes/band fields; its self-test asserts it).
#
# ROUTE: Framework_MockReview.md + blueprint_core.py (+ Framework_DeliveryFooter.md for the
#   delivery call conventions). No other engine: the review is CLASS J over the packet.
#
# INPUTS (attached to the trigger in this chat):
#   1. [ExamCode]_[slug]_review_packet.zip   — REQUIRED (written by Create S13-2G phase 1)
#      contains: [ExamCode]_[slug]_Create.docx, review_packet.json, README.txt
#   2. nothing else. Do NOT attach the registry, the answer key, the blueprint or the
#      author's chat — an attached key makes the review worthless; if one is attached this
#      step IGNORES it and prints a one-line warning (never a stop).
#
# OUTPUT (ONE file, ONE present_files call):
#   [ExamCode]_[slug]_review_verdicts.json
#
# TRIGGER FORMAT:
#   Step 7R: MockReview
#   Step 7R: TestReview            (alias — identical behaviour)
#   Trigger matching is case-insensitive. No arguments: the packet names the exam and paper.

# §1 — SESSION START

## S1-1 — Locate the packet (DETERMINISTIC)

  ```python
  # ── S1-1 (executable) ──────────────────────────────────────────────────────────
  import glob, json, os, hashlib, zipfile
  import blueprint_core as bc
  _pk = sorted(glob.glob('/mnt/user-data/uploads/*_review_packet.zip'))
  if not _pk:
      raise SystemExit("HARD STOP [HS:INPUT] (MockReview S1-1): attach the "
                       "[ExamCode]_[slug]_review_packet.zip written by TestCreate / MockCreate "
                       "(S13-2G phase 1) to this chat, then re-run MockReview.")
  if len(_pk) > 1:
      print(f"MockReview S1-1: {len(_pk)} packets attached — reviewing the first "
            f"({os.path.basename(_pk[0])}); run again for the others.")
  PACKET_ZIP = _pk[0]
  _stray = [f for f in glob.glob('/mnt/user-data/uploads/*') if f != PACKET_ZIP]
  if _stray:
      print(f"MockReview S1-1: ignoring {len(_stray)} other attachment(s) — this step reads ONLY the packet "
            "(an attached key or registry would anchor the review).")
  WORK = '/home/claude/review'
  os.makedirs(WORK, exist_ok=True)
  try:
      with zipfile.ZipFile(PACKET_ZIP) as _z:
          _z.extractall(WORK)
      PACKET = json.load(open(os.path.join(WORK, 'review_packet.json'), encoding='utf-8'))
  except (zipfile.BadZipFile, OSError, ValueError) as _e:
      raise SystemExit(f"HARD STOP [HS:INPUT] (MockReview S1-1): {os.path.basename(PACKET_ZIP)} is not a review "
                       f"packet written by TestCreate S13-2G ({type(_e).__name__}: {_e}) — attach the packet the "
                       "author's chat delivered, unmodified.")
  _docx = sorted(glob.glob(os.path.join(WORK, '*_Create.docx')))
  DOCX = _docx[0] if _docx else None
  # exam code and paper slug come from the packet itself (an exam code may contain '_',
  # so the filename is never split to find them); the filename is the fallback for a
  # packet written by an older Create.
  _base = os.path.basename(PACKET_ZIP)[:-len('_review_packet.zip')]
  EXAM = str(PACKET.get('exam') or _base.split('_', 1)[0])
  PAPER_SLUG = str(PACKET.get('paper_slug') or (_base[len(EXAM) + 1:] if _base.startswith(EXAM + '_') else _base))
  REVIEW_ROUND = int(PACKET.get('review_round') or 1)
  PAPER_MD5 = PACKET.get('paper_md5')
  # The docx in the packet MUST be the paper the md5 names — otherwise the verdicts would
  # bind to a paper nobody read. A mismatch is recorded and the file still reviewed
  # (the author's --resume rejects the binding and re-issues a packet; OD-1).
  DOCX_MD5 = hashlib.md5(open(DOCX, 'rb').read()).hexdigest() if DOCX else None
  MD5_MATCH = (DOCX_MD5 == PAPER_MD5)
  if not MD5_MATCH:
      print(f"MockReview S1-1: WARNING — packet docx md5 {DOCX_MD5} != packet paper_md5 {PAPER_MD5}; "
            "the verdict file will carry the packet md5 and the author's --resume will tell you "
            "whether it binds.")
  N_ITEMS = int(PACKET.get('n_items') or 0)
  PARTS = PACKET.get('parts') or []
  print(f"MockReview: {EXAM} {PAPER_SLUG} (review round {REVIEW_ROUND}) — {N_ITEMS} items in {len(PARTS)} part(s); "
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
  for _part in PARTS:
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
  json.dump({'exam': EXAM, 'paper_slug': PAPER_SLUG, 'paper_md5': PAPER_MD5, 'docx': DOCX,
             'review_round': REVIEW_ROUND, 'items': QUEUE},
            open(os.path.join(WORK, 'queue.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
  if len(QUEUE) != N_ITEMS:
      print(f"MockReview S1-2: queue holds {len(QUEUE)} items but the packet declares {N_ITEMS} — "
            "reviewing what is present; the author's --resume will report the count mismatch.")
  print(f"MockReview S1-2: queue written — {len(QUEUE)} items; figural items: "
        f"{sum(1 for r in QUEUE if r['figures'])}.")
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
  # /home/claude/review/answers.json as {"<q>": {...}} with EXACTLY these keys:
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
  #                                  acceptable; do not invent a benchmark).
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
  #                                  the author must look at; it is never a courtesy.
  #   selectivity_basis            : "clean" | "contested: <reason>" (the word
  #                                  "contested" first — the engine tests the prefix) — would a strong
  #                                  candidate and a weak one be separated by this item for
  #                                  the RIGHT reason (knowledge the subtopic tests), or
  #                                  for a wrong one (ambiguity, trivia, a trick of
  #                                  wording)? "contested" is a defect.
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
  # it (S13-2G phase 3, bc.review_key_agreement). Do not write it.
  ```

  Working order per item: read the stem and all options (open the docx page for a figure)
  → derive own_key → test single_answer → scan for leak_or_paraphrase against the
  exemplar slice → place the band beside the exemplars → classify every distractor → check
  names / counts / figures → set confidence and selectivity_basis → verdict + reason. Write
  the item's record before moving to the next one; a long paper is written in the packet's
  parts (<= 30 items each) so the file is never lost to a session boundary.

# §3 — ASSEMBLE, SELF-CHECK, DELIVER (DETERMINISTIC)

## S3-1 — Build and bind-check the verdict file

  ```python
  # ── S3-1 (executable; after every item in answers.json has a record) ──────────
  import json, os
  import blueprint_core as bc
  WORK = '/home/claude/review'
  _q = json.load(open(os.path.join(WORK, 'queue.json'), encoding='utf-8'))
  _ans_path = os.path.join(WORK, 'answers.json')
  ANSWERS = json.load(open(_ans_path, encoding='utf-8')) if os.path.exists(_ans_path) else {}
  _expected = [str(r['q']) for r in _q['items']]
  _missing = [q for q in _expected if q not in ANSWERS]
  if _missing:
      # OD-1: never a stop. A missing record is written as 'not assessed' with confidence
      # 'low' (bc.review_verdict_file) so the author's --resume treats it as a defect and
      # the item gets a second look — a silent PASS is the one outcome this step must not
      # produce.
      print(f"MockReview S3-1: {len(_missing)} item(s) have no record ({_missing[:10]}{'...' if len(_missing) > 10 else ''}) "
            "— written as 'not assessed' / confidence low (they will be re-reviewed after --resume).")
      for q in _missing:
          ANSWERS[q] = {}
  VERDICT_FILE, _probs = bc.review_verdict_file(_q['exam'], _q['paper_slug'], _q['paper_md5'], ANSWERS)
  VERDICT_FILE['review_round'] = int(_q.get('review_round') or 1)
  for _p in _probs:
      print("MockReview S3-1: " + _p)
  _bind = bc.bind_review_verdicts(VERDICT_FILE, _q['paper_md5'], len(_expected))
  print(f"MockReview S3-1: self-bind {'OK' if _bind['ok'] else 'PROBLEMS: ' + '; '.join(_bind['problems'])}; "
        f"defects flagged for the author: {_bind['defects'] or 'none'}")
  _n_fail = sum(1 for r in VERDICT_FILE['items'].values() if r.get('verdict') == 'FAIL')
  print(f"MockReview S3-1: {len(VERDICT_FILE['items'])} items reviewed — {_n_fail} FAIL, "
        f"{len(VERDICT_FILE['items']) - _n_fail} PASS; low-confidence: "
        f"{sum(1 for r in VERDICT_FILE['items'].values() if r.get('confidence') == 'low')}; "
        f"contested: {sum(1 for r in VERDICT_FILE['items'].values() if str(r.get('selectivity_basis', '')).startswith('contested'))}.")
  ```

## S3-2 — Deliver

  ```python
  # ── S3-2 (executable) ──────────────────────────────────────────────────────────
  out = f"/mnt/user-data/outputs/{_q['exam']}_{_q['paper_slug']}_review_verdicts.json"
  os.makedirs('/mnt/user-data/outputs', exist_ok=True)
  json.dump(VERDICT_FILE, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
  delivery = [out]
  print(f"MockReview: delivered {os.path.basename(out)} — attach it (with the registry) to the "
        "AUTHOR's chat and run TestCreate --resume / MockCreate --resume (S13-2G phase 3). "
        "Flagged items are repaired there through the ladder, re-swept, and re-packeted "
        "for one more review round at most; a disagreement that survives round 2 is an "
        "UNRESOLVED item and the paper proceeds NOT CERTIFIED (OD-9).")
  ```
  Then, in the model's own turn (CLASS T — never from python): present_files(delivery) — the
  one verdict file, ONE call.

# §4 — CHECKLIST (all 6 items must PASS)

  [ ] 1. Exactly one packet read; any other attachment ignored and printed (S1-1).
  [ ] 2. The docx md5 was compared with paper_md5 and the result printed (S1-1).
  [ ] 3. Every item in the queue has a record with all eight checklist keys, verdict and
         reason (S2-2 / S3-1 — a blank field is 'not assessed' + confidence low, never a PASS).
  [ ] 4. key_agrees is null on every record — this step never saw the key (S2-2).
  [ ] 5. bc.bind_review_verdicts on the file reports ok (S3-1).
  [ ] 6. ONE file, [ExamCode]_[slug]_review_verdicts.json, in ONE present_files call (S3-2).

# END OF Framework_MockReview v1.0.0
