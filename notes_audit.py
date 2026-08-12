"""
notes_audit.py v2.0 — Engine for Notes Step NA (Framework_NotesAudit).

v2.0 — 2026-08-12 — NA BECOMES A WRITER (Framework_NotesAudit v3.0.0;
    GAP-2026-08-12-NADOCX patch P2 of 2). NA no longer routes defects back to
    NC: it parses NC's draft to a notes_docx content model, corrects and
    improves the MODEL, rebuilds through the shared builder, and emits the
    student-facing _Final.docx. Five things follow, and each closes a way that
    inversion could ship a wrong document.

    (1) FOURTH VERDICT — SOLVABLE_KEY_CORRECTED (owner decision, supersedes NA
        v2.0.0 decision 4a for the correction path only). The stored key is no
        longer treated as beyond appeal: where the notes-derived answer
        disagrees, NA teaches the CORRECT method and answer rather than
        bending the notes to a wrong key. It counts toward the pass, so a unit
        with a corrected key still certifies without weakening the
        vacuous-pass floor. classify_key_conflict() separates the two cases
        that matter:
          TIER 1 — the BANK CONTRADICTS ITSELF: its verbatim explanation
            concludes one option while its correct_answer field names another.
            That is a Step-5 extraction defect with evidence from inside the
            bank, so the correction is silent.
          TIER 2 — the bank is internally CONSISTENT and NA still disagrees.
            That is NA against the examiner AND the official explanation — a
            genuine judgement, so it is recorded and surfaced in the chat.
        Without the split, every disagreement would resolve in NA's favour and
        the ground-truth check would be decorative.
    (2) THE BANK IS NEVER WRITTEN. Corrections live in the report and the
        registry, never in notes_pyq_bank.json. Editing the bank would break
        the blueprint's bank_ref for EVERY unit in the exam and force a full NB
        re-run to recover.
    (3) TERMINAL RE-GATE — terminal_regate() certifies the BYTES THAT SHIP, not
        the pre-patch draft. A correction that fixes Q7 and breaks Q12's
        cross-reference is exactly what a pre-patch certification misses.
    (4) NEW GATES. G-7b (OMML/figure line-rule geometry) is the mechanical
        replacement for a visual equation check that LibreOffice cannot
        perform — it drops OMML silently on conversion (G-2a, verified
        2026-08-08), so a rendered page can never prove an equation fits.
        G-8 answer integrity, G-9 orphan terms, G-10 counter integrity.
        G-7a (visual layout) degrades to DORMANT-but-reported when no renderer
        is present, the figural_core idiom — absence never halts an audit.
    (5) NO .md REPORT. write_report() is retained for callers that want one,
        but the sanctioned artifact is audit_summary(), embedded in
        notes_registry.json. The report OBJECT stays: pass_for_unit operates on
        it and is the vacuous-pass floor, so dropping the object would delete
        the certification, not just the file.

    Companion: notes_core >= v2.3, notes_docx >= v1.0.

v1.3 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 2 (vacuous-pass floor wired). is_pass
    has carried an expected_count floor since v1.1, but nothing named WHO supplies
    it, so a run that audited 5 of 37 questions could still certify AUDITED_PASS.
    pass_for_unit(report, unit_bank_questions) closes that: it derives
    expected_count = len(unit_bank_questions) from the bank and calls is_pass, so
    the count can no longer be forgotten. The NA spec now determines a unit pass
    only through this helper. No other v1.2 surface changed.

v1.2 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES (Framework_NotesAudit v2.0.0).
    NB now ingests the corpus and stores, per question, the verbatim
    correct_answer, the explanation, and the stem_figures / solution_figures
    split. So NA changes: (1) figure handling — bind_figures() and
    extract_media() are REMOVED; figures are read from the bank question
    (figures_for()), never re-downloaded or re-bound (owner decision 1/6).
    (2) Answer mode — ground_truth is the default and only spec path; NA solves
    from the notes and matches the bank's answer with type-aware helpers
    verdict_against_key() / _mcq / msq (notes_core.msq_match) / nat
    (notes_core.nat_within_tolerance, rounding precision — owner decision 4b).
    (3) KEY_FLAG is DROPPED from the report (owner decision 4a); the doc key is
    authoritative and never re-derived. new_report() no longer carries
    key_flags. is_pass and the §4 convergence counters are unchanged; their
    v1.1 self-tests are retained verbatim.

v1.1 — 2026-08-08 — DEPLOYMENT-REVIEW FIXES. (1) is_pass now has a floor: an
    empty verdict set, or fewer verdicts than the bank's expected count, can
    never certify AUDITED_PASS (vacuous all() defect). (2) Convergence
    counters aligned to spec §4: the 3rd failed patch on a question returns
    REGENERATE (was off by one), and the 3rd regeneration returns DIAGNOSTIC,
    the same >= shape. (3) self_test() added per CLAUDE.md engine rule, with
    fixtures that fail on each rectified defect.

v1.0 — 2026-08-08 — INITIAL RELEASE. Verdict/report schema, convergence-loop
    bookkeeping (patch counter -> regen -> diagnostic per spec §4), figure
    extraction + positional binding (spec §1), and the audit-report writer.
    The closed-book SOLVE itself is Claude-driven; this engine keeps the
    state machine honest.
"""
import json, os, re
from datetime import datetime, timezone
import notes_core

# v2.0: SOLVABLE_KEY_CORRECTED counts toward the pass. The notes are correct
# and the STORED key was wrong; the student sees correct teaching either way.
VERDICTS = ("SOLVABLE", "SOLVABLE_KEY_CORRECTED", "PARTIAL", "NOT")
PASSING_VERDICTS = ("SOLVABLE", "SOLVABLE_KEY_CORRECTED")
REPORT_SCHEMA = "notes-audit-report/2.0"   # v2.0: key corrections, quarantine
MAX_PATCHES_PER_QUESTION = 3     # spec §4 L-2
MAX_REGENERATIONS = 3            # spec §4 L-3

# Gate identifiers, in report order. G-1..G-6 predate v2.0.
GATES = ("G-1", "G-2a", "G-2b", "G-2c", "G-3", "G-4", "G-5", "G-6",
         "G-7a", "G-7b", "G-8", "G-9", "G-10")

KEY_CORRECTION_TIERS = ("BANK_SELF_CONTRADICTS", "JUDGEMENT")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_report(unit_code, notes_version, mode="ground_truth"):
    """Ground-truth is the default and only spec path (owner decision 4): the
    bank carries the authoritative answer, so NA never self-generates one.
    KEY_FLAG is gone. figure_pending stays as an (normally empty) safety list
    for the degenerate case where a bank figure is missing; it is not the
    primary path since NB reads every image (owner decision 6)."""
    assert mode == "ground_truth", "self-answer mode retired (owner decision 4)"
    return {"schema": REPORT_SCHEMA, "unit_code": unit_code,
            "notes_version": notes_version, "mode": mode, "started": _now(),
            "items": {}, "patch_log": [], "regenerations": 0,
            "figure_pending": [], "gates": {},
            # v2.0
            "key_corrections": [], "quarantined": [], "improvements": [],
            "final_ref": None}


def record(report, qid, verdict, notes_location, answer, note=""):
    assert verdict in VERDICTS, verdict
    report["items"][qid] = {"verdict": verdict, "where": notes_location,
                            "answer": answer, "note": note,
                            "patches": report["items"].get(qid, {}).get("patches", 0)}


def log_patch(report, qid, gap, patch_ref):
    it = report["items"][qid]
    it["patches"] += 1
    report["patch_log"].append({"at": _now(), "qid": qid, "gap": gap,
                                "patch": patch_ref})
    if it["patches"] >= MAX_PATCHES_PER_QUESTION:
        return "REGENERATE"          # spec §4 L-2: the 3rd failed patch regenerates
    return "REAUDIT"


def log_regeneration(report):
    report["regenerations"] += 1
    if report["regenerations"] >= MAX_REGENERATIONS:
        return "DIAGNOSTIC"          # spec §4 L-3: data problem, stop looping
    return "CONTINUE"


def is_pass(report, expected_count=None):
    """100% SOLVABLE with a floor: zero audited questions is never a pass,
    and when the bank's expected question count is supplied, fewer verdicts
    than expected is never a pass. FIGURE_PENDING items permitted per §1."""
    items = report["items"]
    if not items:
        return False
    if expected_count is not None and len(items) < int(expected_count):
        return False
    # v2.0: a quarantined question is EXCLUDED from the solvable set but still
    # counted above, so quarantining can never be used to manufacture a pass by
    # shrinking the denominator.
    qids = {q["qid"] for q in report.get("quarantined", [])}
    live = [v for k, v in items.items() if k not in qids]
    if not live:
        return False
    return all(v["verdict"] in PASSING_VERDICTS for v in live)


def pass_for_unit(report, unit_bank_questions):
    """Fix 2: the ONLY sanctioned way NA certifies a unit. expected_count is
    derived from the bank (len of this unit's questions from
    notes_core.bank_questions_for), so the vacuous-pass floor can never be
    skipped by a caller that forgets to pass a count. A run that audited fewer
    questions than the unit's bank holds is never a pass."""
    return is_pass(report, expected_count=len(unit_bank_questions))


def write_report(report, path):
    report["finished"] = _now()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False); f.write("\n")
    return path


# ---------------------------------------------------------------- figures
# NB already extracted every image from Drive and bound it to its question,
# splitting stem figures from solution figures at the "Correct Answer:" line
# (owner decision 3). NA does NOT re-open any .docx. It reads the split off the
# bank question. extract_media()/bind_figures() are retired as of v1.2.
def figures_for(bank_question):
    """The stem figures a solver must SEE to answer this question. Solution
    figures are excluded — they are part of the key, not the prompt."""
    return list(bank_question.get("stem_figures", []))


def missing_figures(bank_question):
    """A stem figure the bank flagged but whose media file did not resolve.
    Normally empty (NB reads every image). A non-empty result parks the
    question in report['figure_pending'] rather than hard-stopping the run."""
    return [f for f in bank_question.get("stem_figures", [])
            if str(f).startswith("UNRESOLVED:")]


# ------------------------------------------------------ ground-truth matching
def verdict_against_key(qtype, computed, key, stem=""):
    """Type-aware ground-truth comparison (owner decision 4). Returns
    (matched: bool, detail: str). MCQ: option-token equality. MSQ: unordered
    set (notes_core.msq_match). NAT: rounding-precision tolerance from the stem
    (notes_core.nat_within_tolerance). None computed -> never a match."""
    t = (qtype or "").upper()
    if computed is None:
        return False, "no answer produced from the notes"
    if t == "MSQ":
        ok = notes_core.msq_match(computed, key)
        return ok, f"MSQ set {'==' if ok else '!='} key"
    if t == "NAT":
        p = notes_core.nat_precision_from_stem(stem)
        tgt = notes_core.normalize_answer("NAT", key)
        got = notes_core.normalize_answer("NAT", computed)
        ok = notes_core.nat_within_tolerance(got, tgt, p)
        return ok, f"NAT match at {p} dp ({got} vs {tgt})"
    ok = notes_core.normalize_answer("MCQ", computed) == \
        notes_core.normalize_answer("MCQ", key)
    return ok, f"MCQ option {'==' if ok else '!='} key"


# ================================================================ v2.0
# ---------------------------------------------------------- key corrections
def classify_key_conflict(explanation_supports_computed):
    """Which KIND of key conflict is this? Returns a KEY_CORRECTION_TIERS value.

    The caller (NA, reading the bank's VERBATIM explanation alongside its
    VERBATIM correct_answer) supplies one boolean: does the stored explanation's
    own reasoning arrive at the answer NA derived from the notes?

      True  -> BANK_SELF_CONTRADICTS. The bank disagrees with ITSELF: its
               explanation concludes X while its correct_answer field says Y.
               That is a Step-5 extraction defect — the wrong option token was
               captured — and the evidence is inside the bank, so the
               correction needs no judgement and is applied silently.
      False -> JUDGEMENT. The bank is internally consistent and NA still
               disagrees, i.e. NA against the examiner AND the official
               explanation. The correction is still applied (the student must
               be taught correctly), but it is recorded and surfaced in the
               chat so a human can check it.

    The split is the whole safeguard. Without it every disagreement would
    resolve in NA's favour — including the ones where NA is simply wrong — and
    the ground-truth comparison would stop meaning anything.
    """
    return ("BANK_SELF_CONTRADICTS" if explanation_supports_computed
            else "JUDGEMENT")


def record_key_correction(report, qid, stored_answer, corrected_answer,
                          tier, reasoning):
    """Record a key correction. NEVER writes the bank.

    The bank is NB's artifact and the blueprint holds bank_ref, a sha256 over
    its bytes. Editing it here would fail verify_bank_ref on the next NC and NA
    run for EVERY unit in the exam and force a full NB re-run to recover. The
    correction lives in the report and, via audit_summary, in the registry —
    which is also the form you would feed back into a Step-5 fix.
    """
    if tier not in KEY_CORRECTION_TIERS:
        raise ValueError(f"unknown key-correction tier: {tier!r}")
    if str(stored_answer).strip() == str(corrected_answer).strip():
        raise ValueError("key correction recorded with no actual change")
    report["key_corrections"].append(
        {"at": _now(), "qid": qid, "stored": str(stored_answer),
         "corrected": str(corrected_answer), "tier": tier,
         "reasoning": reasoning})
    if qid in report["items"]:
        report["items"][qid]["verdict"] = "SOLVABLE_KEY_CORRECTED"
    return report["key_corrections"][-1]


def disclosable_corrections(report):
    """The JUDGEMENT-tier corrections NA must surface in the chat delivery
    line. TIER 1 corrections are provable from the bank and stay silent."""
    return [c for c in report["key_corrections"] if c["tier"] == "JUDGEMENT"]


def quarantine(report, qid, reason):
    """Park a question that survived the full §4 loop without converging.

    With key-correction authority in place this is no longer 'the notes are
    badly written' — NA can always teach the correct method. It means the
    question does not belong to this subtopic, or its stem is corrupt. The
    unit still certifies on the remaining set; the list is what to check
    against Step 5, and a bank refresh re-audits it under the standing
    trigger.
    """
    report["quarantined"].append({"at": _now(), "qid": qid, "reason": reason})
    return report["quarantined"][-1]


def log_improvement(report, where, what):
    """Bounded discretionary improvement (owner decision). Recorded so the
    idempotence claim is checkable: a second NA run over its own output must
    log ZERO improvements."""
    report["improvements"].append({"at": _now(), "where": where, "what": what})
    return report["improvements"][-1]


# ---------------------------------------------------------------- gates
def preflight():
    """Which optional gate dependencies are present. Absence never halts an
    audit — the affected gate degrades to DORMANT and is REPORTED as such
    (the figural_core idiom)."""
    avail = {}
    for mod in ("docx", "matplotlib", "PIL"):
        try:
            __import__(mod)
            avail[mod] = True
        except ImportError:
            avail[mod] = False
    avail["libreoffice"] = bool(
        os.environ.get("SOFFICE_BIN") or
        any(os.path.exists(p) for p in ("/usr/bin/soffice",
                                        "/usr/bin/libreoffice")))
    return {"available": avail}


def gate_line_rules(docx_path):
    """G-7b — OMML AND FIGURE GEOMETRY. Returns (ok, findings).

    Every paragraph carrying an equation or an image must use an AUTO line
    rule. A fixed rule ("exact"/"atLeast") CLIPS the object: the equation is
    still present in the XML, so G-2a's presence assertion passes while the
    page is visibly wrong.

    This gate exists because the visual check cannot cover equations at all.
    LibreOffice drops OMML silently on conversion (G-2a, verified 2026-08-08),
    so a rendered page shows the maths MISSING whether or not it fits. The
    geometry is therefore asserted structurally, which is also stricter than a
    human glance.
    """
    import zipfile
    from lxml import etree
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    with zipfile.ZipFile(docx_path) as z:
        root = etree.fromstring(z.read("word/document.xml"))
    findings = []
    checked = 0
    for i, p in enumerate(root.iter(W + "p")):
        tall = (p.find(".//" + M + "oMath") is not None
                or p.find(".//" + A + "blip") is not None)
        if not tall:
            continue
        checked += 1
        pPr = p.find(W + "pPr")
        sp = pPr.find(W + "spacing") if pPr is not None else None
        rule = sp.get(W + "lineRule") if sp is not None else None
        if rule is None:
            findings.append(f"paragraph {i}: equation/figure paragraph has no "
                            f"explicit line rule — it inherits the style's, "
                            f"which may be fixed (rule F-7)")
        elif rule != "auto":
            findings.append(f"paragraph {i}: line rule is {rule!r}, not "
                            f"'auto' — a tall inline object will be CLIPPED "
                            f"and the XML gates will not see it (rule F-7)")
    return (not findings, findings, {"paragraphs_checked": checked})


def gate_answer_integrity(model):
    """G-8 — ANSWER INTEGRITY on the built document's own content.

    G-5 checks the question TEMPLATE. It does not check that the printed key is
    a usable answer to the printed options. A key of "5" against four options,
    or an MSQ key repeating an option, is the single worst defect that can
    reach a student, and nothing before v2.0 looked for it.
    """
    findings = []
    n = 0
    for i, b in enumerate(model.get("blocks", [])):
        if b.get("type") not in ("example", "recall"):
            continue
        n += 1
        qt = (b.get("qtype") or "").upper()
        ans = str(b.get("answer", "")).strip()
        opts = b.get("options") or []
        if not ans:
            findings.append(f"block {i}: no Answer printed")
            continue
        if qt == "MCQ":
            if ans not in {str(k) for k in range(1, len(opts) + 1)}:
                findings.append(f"block {i}: MCQ key {ans!r} is outside the "
                                f"{len(opts)} printed options")
        elif qt == "MSQ":
            parts = [p.strip() for p in ans.split(",") if p.strip()]
            valid = {str(k) for k in range(1, len(opts) + 1)}
            if not parts or any(p not in valid for p in parts):
                findings.append(f"block {i}: MSQ key {ans!r} is not a subset "
                                f"of the {len(opts)} printed options")
            if len(set(parts)) != len(parts):
                findings.append(f"block {i}: MSQ key {ans!r} repeats an option")
        elif qt == "NAT":
            if opts:
                findings.append(f"block {i}: NAT question printed options")
            try:
                float(ans)
            except ValueError:
                findings.append(f"block {i}: NAT key {ans!r} is not numeric")
    return (not findings, findings, {"questions_checked": n})


def gate_counters(model, docx_path=None):
    """G-10 — COUNTER INTEGRITY.

    IMPORTANT: this gate compares the counters PRINTED IN THE DOCUMENT against
    the counters DERIVED from the model. An earlier draft of this gate checked
    the derived sequence against itself — which notes_docx.outline_of makes
    gapless by construction, so the check could never fail. (Found by mutation
    testing: deleting the check changed nothing.) The real risk is a document
    whose printed labels have drifted from the model that is supposed to
    describe it — a hand-edited file, or a build/parse mismatch — and that is
    what is checked here.

    With docx_path omitted the gate reports the derived counts only and is
    explicitly marked as not having verified anything.
    """
    import notes_docx
    o = notes_docx.outline_of(model)
    findings = []
    derived_ex = [j for _, j in o["examples"]]
    derived_rc = [j for _, j in o["recalls"]]
    meta = {"examples": len(derived_ex), "recalls": len(derived_rc),
            "sections": len(o["l2"]), "verified_against_document": False}
    if docx_path is None:
        return (True, findings, meta)

    printed_ex, printed_rc, printed_l2 = [], [], []
    text = notes_docx.document_xml(docx_path).decode("utf-8")
    text = re.sub(r"<[^>]+>", "", text)
    for m in re.finditer(r"Example\s+(\d+)", text):
        printed_ex.append(int(m.group(1)))
    for m in re.finditer(r"Recall\s+(\d+)", text):
        printed_rc.append(int(m.group(1)))
    for m in re.finditer(r"(?<![\d.])(\d+)\.(\d+)(?![\d.])", text):
        printed_l2.append(f"{m.group(1)}.{m.group(2)}")
    meta["verified_against_document"] = True

    if printed_ex != derived_ex:
        findings.append(f"Example counters printed in the document "
                        f"{printed_ex} do not match the derived sequence "
                        f"{derived_ex}")
    if printed_rc != derived_rc:
        findings.append(f"Recall counters printed in the document "
                        f"{printed_rc} do not match the derived sequence "
                        f"{derived_rc}")
    derived_l2 = [n for _, n, _ in o["l2"]]
    missing = [n for n in derived_l2 if n not in printed_l2]
    if missing:
        findings.append(f"outline numbers derived but not printed: {missing}")
    if derived_ex and derived_ex != list(range(1, len(derived_ex) + 1)):
        findings.append(f"derived Example sequence is not gapless and "
                        f"1-based: {derived_ex}")
    return (not findings, findings, meta)


_TERM = re.compile(r"\b[A-Za-z][A-Za-z0-9\-]{3,}\b")


def gate_orphan_terms(model, allowed=()):
    """G-9 — ORPHAN TERMS. A term used in a question stem, option or
    explanation that appears NOWHERE in the notes body breaks the closed-book
    promise at vocabulary level.

    The solve in §2 is performed by a reader who already knows the subject, so
    it can silently supply a missing term and still reach the right answer.
    This gate cannot: it is pure set difference over the document's own text.
    Reported as findings for NA to judge, not as an automatic hard stop —
    common English is not a syllabus term.
    """
    import notes_docx
    body_words, q_words = set(), {}
    for b in model.get("blocks", []):
        t = b.get("type")
        if t in ("title", "concept", "key_points", "trap", "rapid", "mindmap"):
            txt = json.dumps(b, ensure_ascii=False)
            body_words |= {w.lower() for w in _TERM.findall(txt)}
        elif t in ("example", "recall"):
            txt = json.dumps({k: v for k, v in b.items()
                              if k in ("stem", "options", "explanation")},
                             ensure_ascii=False)
            for w in _TERM.findall(txt):
                q_words.setdefault(w.lower(), 0)
                q_words[w.lower()] += 1
    allow = {a.lower() for a in allowed} | {
        "text", "math", "true", "false", "which", "that", "this", "with",
        "from", "when", "then", "also", "each", "both", "what", "have",
        "there", "their", "these", "those", "will", "must", "only", "than",
        "into", "over", "under", "given", "find", "using", "value", "values",
        "correct", "answer", "option", "options", "following", "statement",
        "statements", "type", "base", "holds", "rounded", "decimal", "places"}
    orphans = sorted(w for w in q_words if w not in body_words and w not in allow)
    return (not orphans, [f"term used only in a question, never taught in the "
                          f"notes: {w!r}" for w in orphans],
            {"terms_checked": len(q_words)})


def terminal_regate(docx_path, model, *, tier, page_count, exemptions=(),
                    expected_omml=0, orphan_allowed=()):
    """G-11 — THE TERMINAL RE-GATE. Run EVERY mechanical gate over the bytes
    that will ship, and hash them.

    NA edits the document, so certifying the pre-patch draft certifies a file
    that no longer exists. A correction that fixes Q7 and breaks Q12's
    cross-reference is precisely what a pre-patch certification misses. This is
    the last thing NA runs and its result is what audit_summary records.
    """
    g = {}
    ok_d, f_d = notes_core.density_gate(docx_path, tier, page_count)
    g["G-1"] = {"ok": ok_d, "findings": f_d}
    try:
        # assert_omml RAISES on failure and returns the region count.
        n_omml = notes_core.assert_omml(docx_path, expected_omml)
        ok_o, f_o = True, []
    except AssertionError as exc:
        n_omml, ok_o, f_o = None, False, [str(exc)]
    except Exception as exc:                      # pragma: no cover
        n_omml, ok_o, f_o = None, False, [f"assert_omml raised: {exc}"]
    g["G-2a"] = {"ok": ok_o, "findings": f_o, "meta": {"regions": n_omml}}
    # These three scanners return a FINDINGS LIST (empty == clean), not a
    # (ok, findings) pair. Normalised here so every gate in the report has the
    # same shape.
    f_s = notes_core.scan_omml_structural(docx_path)
    g["G-2b"] = {"ok": not f_s, "findings": list(f_s)}
    f_t = notes_core.scan_flat_math_tokens(docx_path)
    g["G-2c"] = {"ok": not f_t, "findings": list(f_t)}
    f_b = notes_core.scan_prose_bans(docx_path, exemptions)
    g["G-4"] = {"ok": not f_b, "findings": list(f_b)}
    avail = preflight()["available"]
    g["G-7a"] = ({"ok": True, "dormant": True,
                  "findings": ["no renderer available — visual layout gate "
                               "DORMANT but reported (absence never halts an "
                               "audit)"]}
                 if not avail["libreoffice"] else
                 {"ok": True, "dormant": False, "findings": []})
    ok_l, f_l, m_l = gate_line_rules(docx_path)
    g["G-7b"] = {"ok": ok_l, "findings": f_l, "meta": m_l}
    ok_a, f_a, m_a = gate_answer_integrity(model)
    g["G-8"] = {"ok": ok_a, "findings": f_a, "meta": m_a}
    ok_r, f_r, m_r = gate_orphan_terms(model, orphan_allowed)
    g["G-9"] = {"ok": ok_r, "findings": f_r, "meta": m_r}
    ok_c, f_c, m_c = gate_counters(model, docx_path)
    g["G-10"] = {"ok": ok_c, "findings": f_c, "meta": m_c}
    g["_sha256"] = notes_core.file_sha256(docx_path)
    # G-9 is advisory (English words are not syllabus terms) and G-7a may be
    # dormant; neither blocks. Everything else is blocking.
    blocking = [k for k, v in g.items()
                if k.startswith("G-") and k not in ("G-9", "G-7a")
                and not v["ok"]]
    g["_blocking_failures"] = blocking
    g["_ok"] = not blocking
    return g


def audit_summary(report, gates, *, bank_ref=None, taxonomy_ref=None,
                  final_ref=None):
    """The registry-embedded replacement for the .md audit report.

    Dropping the report FILE is an operator convenience. Dropping the report
    OBJECT would delete the certification — pass_for_unit operates on it and is
    the vacuous-pass floor. This keeps the evidence that matters, at zero
    extra files: which bank and taxonomy the unit was audited against (so the
    standing re-audit trigger can tell which units a refreshed bank affects),
    the verdict counts, the corrections, the quarantine list and the sha256 of
    the bytes that shipped.
    """
    items = report["items"]
    counts = {v: sum(1 for x in items.values() if x["verdict"] == v)
              for v in VERDICTS}
    return {"schema": REPORT_SCHEMA,
            "audited": _now(),
            "notes_version": report.get("notes_version"),
            "questions": len(items),
            "verdicts": counts,
            "key_corrections": report.get("key_corrections", []),
            "judgement_corrections": len(disclosable_corrections(report)),
            "quarantined": report.get("quarantined", []),
            "improvements": len(report.get("improvements", [])),
            "patches": len(report.get("patch_log", [])),
            "regenerations": report.get("regenerations", 0),
            "figure_pending": report.get("figure_pending", []),
            "gates": {k: v for k, v in gates.items() if k.startswith("G-")},
            "gates_ok": gates.get("_ok"),
            "bank_ref": bank_ref, "taxonomy_ref": taxonomy_ref,
            "final_ref": final_ref}


# ---------------------------------------------------------------- self-test
def self_test():
    passed, fails = 0, []

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    # Defect fixture 1: vacuous pass on empty report (the shipped bug)
    r = new_report("U", "0.1", "ground_truth")
    check("empty report is never a pass", is_pass(r) is False)
    record(r, "Q1", "SOLVABLE", "1.1", "a")
    check("one solvable, no floor -> pass", is_pass(r) is True)
    check("floor: 1 of 37 is not a pass", is_pass(r, expected_count=37) is False)
    for i in range(2, 38):
        record(r, f"Q{i}", "SOLVABLE", "1.1", "a")
    check("floor: 37 of 37 passes", is_pass(r, expected_count=37) is True)
    record(r, "Q1", "PARTIAL", "1.1", None)
    check("any PARTIAL blocks pass", is_pass(r, expected_count=37) is False)

    # fix 2: pass_for_unit derives the floor from the bank (count can't be skipped)
    r3 = new_report("U", "0.1", "ground_truth")
    unit_qs = [{"bank_id": f"Q{i}"} for i in range(1, 38)]   # 37 in the bank
    for i in range(1, 6):
        record(r3, f"Q{i}", "SOLVABLE", "1.1", "a")
    check("pass_for_unit: 5 of 37 is not a pass", pass_for_unit(r3, unit_qs) is False)
    for i in range(6, 38):
        record(r3, f"Q{i}", "SOLVABLE", "1.1", "a")
    check("pass_for_unit: 37 of 37 passes", pass_for_unit(r3, unit_qs) is True)

    # Defect fixture 2: off-by-one convergence counters (the shipped bug)
    r2 = new_report("U", "0.1", "ground_truth")
    record(r2, "Q1", "PARTIAL", "1.2", None)
    check("patch 1 -> REAUDIT", log_patch(r2, "Q1", "g", "p1") == "REAUDIT")
    check("patch 2 -> REAUDIT", log_patch(r2, "Q1", "g", "p2") == "REAUDIT")
    check("patch 3 -> REGENERATE", log_patch(r2, "Q1", "g", "p3") == "REGENERATE")
    check("regen 1 -> CONTINUE", log_regeneration(r2) == "CONTINUE")
    check("regen 2 -> CONTINUE", log_regeneration(r2) == "CONTINUE")
    check("regen 3 -> DIAGNOSTIC", log_regeneration(r2) == "DIAGNOSTIC")

    # Verdict vocabulary + report write/read round trip
    try:
        record(r2, "QX", "MAYBE", "1.1", None)
        check("invalid verdict rejected", False)
    except AssertionError:
        check("invalid verdict rejected", True)
    import tempfile, os, json as _json
    fp = os.path.join(tempfile.gettempdir(), "na_selftest_report.json")
    write_report(r2, fp)
    check("report round-trips", _json.load(open(fp))["unit_code"] == "U")
    check("report has no key_flags (dropped)", "key_flags" not in r2)

    # v1.2: self-answer mode is retired
    try:
        new_report("U", "0.1", "question_only")
        check("self-answer mode rejected", False)
    except AssertionError:
        check("self-answer mode rejected", True)

    # v1.2: figures read from the bank question (no docx re-open)
    bq = {"stem_figures": ["image3.png", "UNRESOLVED:rId7"],
          "solution_figures": ["image9.png"]}
    check("figures_for returns stem figures only",
          figures_for(bq) == ["image3.png", "UNRESOLVED:rId7"])
    check("missing_figures flags only unresolved",
          missing_figures(bq) == ["UNRESOLVED:rId7"])

    # v1.2: ground-truth verdicts by type (owner decision 4)
    ok, _ = verdict_against_key("MCQ", "2", "2")
    check("MCQ match", ok is True)
    check("MCQ mismatch", verdict_against_key("MCQ", "3", "2")[0] is False)
    check("MSQ unordered match", verdict_against_key("MSQ", [3, 1], "1,3")[0] is True)
    check("MSQ mismatch", verdict_against_key("MSQ", [1, 2], "1,3")[0] is False)
    check("NAT within stem precision",
          verdict_against_key("NAT", 0.4149, "0.41",
                              "give the value to 2 decimal places")[0] is True)
    check("NAT outside precision",
          verdict_against_key("NAT", 0.418, "0.41",
                              "give the value to 2 decimal places")[0] is False)
    check("NAT nearest-integer stem",
          verdict_against_key("NAT", 711.4, "711",
                              "answer to the nearest integer")[0] is True)
    check("no computed answer never matches",
          verdict_against_key("NAT", None, "0.41", "")[0] is False)

    # ================================================== v2.0 fixtures
    import tempfile
    import notes_docx

    T = lambda s: [{"t": "text", "s": s}]

    def demo_model(answer="2", qtype="MCQ", opts=4):
        return {"schema": notes_docx.SCHEMA, "exam_code": "EX",
                "unit": {"name": "Enzyme Kinetics", "tier": "TIER-2",
                         "seq_in_topic": 3},
                "blocks": [
                    {"type": "title", "name": "Enzyme Kinetics"},
                    {"type": "concept", "name": "Saturation",
                     "content": [{"k": "bullet", "runs": T(
                         "Rate saturates as substrate concentration rises.")}]},
                    {"type": "example", "qtype": qtype,
                     "stem": [{"t": "text", "s": "Given "},
                              {"t": "math", "latex": "\\frac{V_{max}[S]}"
                                                     "{K_m+[S]}"},
                              {"t": "text", "s": " which saturation "
                                                 "statement holds?"}],
                     "options": [T("a"), T("b"), T("c"), T("d")][:opts],
                     "answer": answer,
                     "explanation": [T("Substrate saturates the enzyme.")]},
                    {"type": "key_points",
                     "bullets": [T("Saturation sets the ceiling rate.")]}]}

    # ---- fourth verdict ------------------------------------------------
    r = new_report("EX_S1_T1_ST01", "0.1")
    check("v2.0: SOLVABLE_KEY_CORRECTED is a legal verdict",
          "SOLVABLE_KEY_CORRECTED" in VERDICTS)
    record(r, "q1", "PARTIAL", "3.1", "2")
    record_key_correction(r, "q1", "3", "2", "BANK_SELF_CONTRADICTS",
                          "stored explanation concludes option 2")
    check("recording a key correction flips the verdict",
          r["items"]["q1"]["verdict"] == "SOLVABLE_KEY_CORRECTED")
    check("a corrected key still certifies the unit",
          pass_for_unit(r, [{"bank_id": "q1"}]))
    check("the bank is never written — the correction lives in the report",
          r["key_corrections"][0]["stored"] == "3"
          and r["key_corrections"][0]["corrected"] == "2")
    try:
        record_key_correction(r, "q1", "2", "2", "JUDGEMENT", "no change")
        check("a no-op key correction is rejected", False)
    except ValueError:
        check("a no-op key correction is rejected", True)
    try:
        record_key_correction(r, "q1", "1", "2", "MADE_UP", "x")
        check("an unknown correction tier is rejected", False)
    except ValueError:
        check("an unknown correction tier is rejected", True)

    # ---- tier classification is the safeguard ---------------------------
    check("tier 1 when the bank's own explanation supports the notes",
          classify_key_conflict(True) == "BANK_SELF_CONTRADICTS")
    check("tier 2 when the bank is internally consistent and NA disagrees",
          classify_key_conflict(False) == "JUDGEMENT")
    r2 = new_report("U", "0.1")
    record(r2, "a", "PARTIAL", "1.1", "2")
    record(r2, "b", "PARTIAL", "1.2", "4")
    record_key_correction(r2, "a", "1", "2", "BANK_SELF_CONTRADICTS", "x")
    record_key_correction(r2, "b", "3", "4", "JUDGEMENT", "y")
    check("only JUDGEMENT-tier corrections are disclosed in the chat "
          "(tier 1 is provable from the bank, so it stays silent)",
          [c["qid"] for c in disclosable_corrections(r2)] == ["b"])

    # ---- quarantine cannot manufacture a pass ---------------------------
    r3 = new_report("U", "0.1")
    record(r3, "a", "SOLVABLE", "1.1", "2")
    record(r3, "b", "NOT", "-", None)
    check("an unconverged question blocks the pass",
          not pass_for_unit(r3, [{"bank_id": "a"}, {"bank_id": "b"}]))
    quarantine(r3, "b", "stem does not belong to this subtopic")
    check("quarantining excludes the question but keeps the denominator, so "
          "the unit certifies on the remaining set",
          pass_for_unit(r3, [{"bank_id": "a"}, {"bank_id": "b"}]))
    r4 = new_report("U", "0.1")
    record(r4, "a", "NOT", "-", None)
    quarantine(r4, "a", "x")
    check("quarantining EVERY question is never a pass",
          not pass_for_unit(r4, [{"bank_id": "a"}]))

    # ---- G-7b line-rule geometry ---------------------------------------
    m = demo_model()
    good = tempfile.mktemp(suffix=".docx")
    notes_docx.build(m, good)
    ok_l, f_l, meta = gate_line_rules(good)
    check("G-7b passes on a document built by notes_docx", ok_l and not f_l)
    check("G-7b actually inspected the equation paragraph",
          meta["paragraphs_checked"] >= 1)
    # Mutate the built file to a FIXED line rule: the clip defect that G-2a
    # cannot see, because the equation is still present in the XML.
    import zipfile
    import shutil
    bad = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(good) as zin, zipfile.ZipFile(bad, "w") as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = data.replace(b'w:lineRule="auto"',
                                    b'w:lineRule="exact"')
            zout.writestr(it, data)
    ok_bad, f_bad, _ = gate_line_rules(bad)
    check("G-7b CATCHES a fixed line rule on an equation paragraph "
          "(the clip that G-2a passes straight through)",
          not ok_bad and any("exact" in x for x in f_bad))
    try:
        notes_core.assert_omml(bad, 1)
        ok_omml = True
    except AssertionError:
        ok_omml = False
    check("...and G-2a really does pass that same clipped file — which is "
          "why G-7b had to exist", ok_omml)

    # ---- G-8 answer integrity ------------------------------------------
    ok8, f8, m8 = gate_answer_integrity(m)
    check("G-8 passes a well-formed key", ok8 and m8["questions_checked"] == 1)
    bad8 = demo_model(answer="5")
    ok8b, f8b, _ = gate_answer_integrity(bad8)
    check("G-8 catches an MCQ key outside the printed options",
          not ok8b and any("outside" in x for x in f8b))
    bad8c = demo_model(answer="1,1", qtype="MSQ")
    check("G-8 catches an MSQ key repeating an option",
          not gate_answer_integrity(bad8c)[0])
    bad8d = demo_model(answer="x", qtype="NAT")
    bad8d["blocks"][2]["options"] = []
    check("G-8 catches a non-numeric NAT key",
          not gate_answer_integrity(bad8d)[0])

    # ---- G-10 counter integrity ----------------------------------------
    ok10, f10, m10 = gate_counters(m, good)
    check("G-10 passes a document whose printed counters match the model",
          ok10 and m10["examples"] == 1
          and m10["verified_against_document"] is True)
    # G-10 must compare the PRINTED counters against the DERIVED ones. An
    # earlier draft compared the derived sequence with itself, which
    # outline_of makes gapless by construction — so the gate could never
    # fire. Mutation testing found it. This fixture doctors the built file so
    # the printed label drifts from the model, which is the real risk.
    drift = tempfile.mktemp(suffix=".docx")
    with zipfile.ZipFile(good) as zin, zipfile.ZipFile(drift, "w") as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = data.replace(b"Example 1", b"Example 4")
            zout.writestr(it, data)
    ok10b, f10b, _ = gate_counters(m, drift)
    check("G-10 CATCHES a printed counter that has drifted from the model",
          not ok10b and any("do not match" in x for x in f10b))
    check("G-10 states plainly when it has verified nothing "
          "(no document supplied)",
          gate_counters(m)[2]["verified_against_document"] is False)

    # ---- G-9 orphan terms ----------------------------------------------
    ok9, f9, _ = gate_orphan_terms(m)
    check("G-9 flags a term used only in the question and never taught",
          not ok9 and any("saturation" not in x.lower()
                          or "term used only" in x for x in f9))
    taught = demo_model()
    taught["blocks"][1]["content"].append(
        {"k": "bullet", "runs": T("Given the Michaelis constant holds here.")})
    check("G-9 is advisory and reports a term count",
          gate_orphan_terms(taught)[2]["terms_checked"] > 0)

    # ---- terminal re-gate ----------------------------------------------
    gates = terminal_regate(good, m, tier="TIER-2", page_count=5,
                            expected_omml=1)
    check("terminal re-gate runs every mechanical gate",
          all(g in gates for g in ("G-1", "G-2a", "G-2b", "G-2c", "G-4",
                                   "G-7a", "G-7b", "G-8", "G-9", "G-10")))
    check("terminal re-gate hashes the bytes that ship",
          gates["_sha256"] == notes_core.file_sha256(good))
    check("terminal re-gate certifies the shipped file", gates["_ok"])
    check("G-9 is advisory — it never blocks on its own",
          "G-9" not in gates["_blocking_failures"])
    check("G-7a degrades to DORMANT-but-reported without a renderer "
          "(absence never halts an audit)",
          gates["G-7a"]["ok"] is True)
    gates_bad = terminal_regate(bad, m, tier="TIER-2", page_count=5,
                               expected_omml=1)
    check("terminal re-gate BLOCKS on the clipped file",
          not gates_bad["_ok"] and "G-7b" in gates_bad["_blocking_failures"])

    # ---- audit_summary --------------------------------------------------
    summ = audit_summary(r2, gates, bank_ref={"sha256": "b" * 64},
                         taxonomy_ref={"sha256": "t" * 64},
                         final_ref={"sha256": "f" * 64})
    check("audit_summary counts every verdict class",
          summ["verdicts"]["SOLVABLE_KEY_CORRECTED"] == 2)
    check("audit_summary discloses the judgement-tier count",
          summ["judgement_corrections"] == 1)
    check("audit_summary records WHICH bank and taxonomy the unit was audited "
          "against (so a refreshed bank knows which units to re-audit)",
          summ["bank_ref"]["sha256"].startswith("bbbb")
          and summ["taxonomy_ref"]["sha256"].startswith("tttt"))
    check("audit_summary carries the shipped file's reference",
          summ["final_ref"]["sha256"].startswith("ffff"))
    check("audit_summary is JSON-serialisable for the registry",
          isinstance(json.dumps(summ), str))

    # ---- idempotence bookkeeping ---------------------------------------
    r5 = new_report("U", "0.2")
    check("a fresh report logs zero improvements", len(r5["improvements"]) == 0)
    log_improvement(r5, "3.1", "tightened a bullet over the D-1 cap")
    check("improvements are logged so a second NA run can be shown to make "
          "none", len(r5["improvements"]) == 1)

    print(f"notes_audit self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_audit.py — Notes Step NA engine. Run with --self-test.")
