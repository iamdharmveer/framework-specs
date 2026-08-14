"""
notes_audit.py v2.5 — Engine for Notes Step NA (Framework_NotesAudit).

v2.5 — 2026-08-14 — G-13 INTEGRATION (in-subtopic Integration sections;
    pairs with Framework_NotesAudit v3.4.0 §5 G-13, Framework_NotesCreate
    v2.6.0 §4 B4a, Framework_NotesBlueprint v3.1.0 §3B B-1; notes_core >=
    v2.7). New gate gate_integration(model, target) with target from
    notes_core.integration_target_for — bank-derived with latest-partner
    filing, so the author (NC) and this gate can never disagree (the G-12
    idiom one feature over). What it enforces, and what it deliberately
    does not:
      HARD (only when the target attests a fusion for THIS unit) —
              every attested fusion is taught by an integration section: a
              concept block whose FIRST bullet is the Combines declaration
              ("Combines: ..." — NC §4 B4a I-2, the mechanical marker; no
              new model field, nothing new renders, W-3 untouched) naming
              every partner; integration sections sit AFTER every core
              concept section (before the tail); and a matched integration
              section carries >= 1 worked Example.
      DORMANT, never blocking — target=None (bank-less caller, the G-7a
              discipline) and target.dormant=True: the GRANDFATHERED case,
              a bank with no integration_partners anywhere predates
              notes-pyq-bank/1.2 and could not carry the evidence. Dormant
              is REPORTED, so every GATES identifier appears in every
              report and audit_summary shows the grandfathering plainly.
      ADVISORY (meta only) — unattested_sections: integration sections
              present without bank attestation (SME bridge-justified under
              D-6; listed for NA's judgement, never a finding).
    terminal_regate gains integration_target= and reports G-13 beside the
    other gates; a non-dormant G-13 failure blocks like any hard gate.
    REMEDIATION ROUTING (spec §2A/§4): a G-13 finding is a partner-homing
    gap — NA EXTENDS or ADDS the integration section (net-ADD licensed
    exactly like G-12's); it NEVER quarantines the fused question, because
    quarantine says "corrupt stem", not "the notes lack the partner bridge".

v2.4 — 2026-08-13 — G-12 COVERAGE (Phase 2, Recommendations 3+4; pairs with
    Framework_NotesAudit v3.3.0 §5 G-12, Framework_NotesCreate v2.5.0 §4 B3a,
    notes_core >= v2.6). New BLOCKING gate gate_coverage(model, target) with
    target from notes_core.coverage_target_for — bank-derived, so the author
    (NC) and this gate can never disagree. What it enforces, and what it
    deliberately does not:
      HARD  — every required_type (the types the unit's own PYQs attest) has
              >= 1 worked Example; and Examples span >=
              min_concepts_with_examples DISTINCT concept sections. An
              Example's concept is DERIVED from block order (the nearest
              preceding concept block — the same derivation discipline as
              numbering), so no new model field exists, nothing new renders,
              and the W-3 round trip is untouched.
      ADVISORY (meta only, never findings, never blocks) — requires_figure
              with no concept-content figure in the model; and
              duplicate_suspects: concept sections carrying more than one
              Example of the same qtype. A hard concept may legitimately
              need two scenarios of one type — no regex can tell diversity
              from redundancy, so that judgement is NA's (§2A), not a gate's.
    There is deliberately NO minimum example COUNT anywhere (owner decision,
    2026-08-13): a count is satisfiable by clones of one scenario; concept
    SPREAD is the thing being promised. G-12 joins GATES and terminal_regate:
    when a coverage target is supplied it BLOCKS like any mechanical gate;
    when no target is supplied (no bank in hand) it reports DORMANT-but-
    reported, exactly the G-7a discipline — absence never halts an audit.

v2.3 — 2026-08-13 — DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE ENFORCEMENT
    (Point 1; pairs with Framework_NotesAudit v3.2.0 G-5, Framework_NotesCreate
    v2.4.0 §4 B3 and notes_docx v1.3). gate_question_format (G-5) now re-asserts,
    on the SHIPPED model, what notes_docx.validate_model enforces at
    construction: every Example carries a one-line Educational Objective and one
    distractor-autopsy line per WRONG option (MCQ 3; MSQ 4 − #correct; NAT >= 1
    trap value), and a Recall carries NEITHER. No new gate identifier is added —
    the two elements are part of "the fixed template" G-5 already owns, so the
    GATES registry and the NA spec stay in agreement (S-2). The terminal
    re-gate (G-11) already runs G-5, so the shipped bytes are certified for the
    autopsy/objective too.

v2.2 — 2026-08-13 — TEXT AUTHORITY + PROSE-ONLY G-9 (GAP-2026-08-12-NAPARSE
    D-2, D-3; owner decisions OD-1 and OD-2).
      (1) gate_counters reads the document through notes_core.document_text —
          the boundary-preserving public authority — instead of a bare tag
          strip that welded "Answer: 1" to "2.10 MIND MAP" as "12.10" and
          failed a CORRECT document on the standard tail anatomy (D-2).
      (2) gate_orphan_terms scans PROSE (text/sym runs) via _prose_of, never
          json.dumps of the model, so OMML markup and model keys can never
          again surface as phantom "terms" (D-3).
      (3) OD-1: G-9's scope stays exactly stem/options/explanation — SPEED
          HACK is deliberately EXCLUDED (it teaches at point of use).
      (4) OD-2 Design A: DOMAIN-ANCHORED mode. gate_orphan_terms accepts
          syllabus_terms (build with the new syllabus_terms_for over the
          unit's bank concept_tags + names) and reports only syllabus-
          evidenced orphans; terminal_regate passes it through. A clean unit
          yields ZERO findings — the usability bar the self-test now pins.

v2.1 — 2026-08-12 — SYNC-AUDIT FIXES (GAP-2026-08-12-NOTESYNC). Two drifts
    found by notes_sync_audit.py, the new cross-step auditor:
      (1) The terminal re-gate claimed in Framework_NotesAudit section 5 to
          re-run "EVERY gate above", but only 11 of 14 identifiers were
          actually emitted: G-3 (anatomy), G-5 (question format and type
          coverage) and G-6 (outline integrity) were left to Claude-side
          judgement and appeared in no report. A spec promise nothing
          enforced. All three are now mechanical — gate_anatomy,
          gate_question_format and gate_outline — and the re-gate emits every
          identifier in GATES. G-6 in particular now resolves in-text
          cross-references ("see 7.3") against the derived outline, which is
          the one thing NA's editing can break silently.
      (2) GATES omitted G-11 while Framework_NotesAudit section 5 named it, so
          the engine's gate registry and the spec disagreed about what a report
          can contain. G-11 is now registered AND emitted by terminal_regate,
          carrying the certified sha256 and the count of gates run — which is
          what "the certification covers the bytes that ship" should look like
          in the report rather than only in prose.
      (3) REPORT_SCHEMA ("notes-audit-report/2.0") was emitted into
          audit_summary but cited by no spec, so a schema bump would have been
          invisible spec-side. Framework_NotesAudit section 6 now cites it.
    No behaviour change to any verdict, gate finding or pass decision.

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
# v2.1: G-11 is included. It is not a content check like the others — it is the
# assertion that the certification covers the BYTES THAT SHIP — but it is
# reported like one, so it belongs in the registry of gate identifiers. The
# cross-step sync auditor compares this tuple against the identifiers the NA
# spec names, and a gate present in one and absent from the other is a finding.
GATES = ("G-1", "G-2a", "G-2b", "G-2c", "G-3", "G-4", "G-5", "G-6",
         "G-7a", "G-7b", "G-8", "G-9", "G-10", "G-11", "G-12", "G-13")

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


def gate_anatomy(model):
    """G-3 — ANATOMY. Required blocks present and in section 6A order.

    notes_docx.validate_model owns the anatomy contract (it is the builder, so
    it is the authority). This re-asserts it on the model that produced the
    shipped file, which matters because NA edits the model after NC built it.
    """
    import notes_docx
    ok, findings = notes_docx.validate_model(model)
    structural = [f for f in findings
                  if any(w in f for w in ("KEY POINTS", "order", "title",
                                          "block", "tail"))]
    return (not structural, structural, {"blocks": len(model.get("blocks", []))})


def gate_question_format(model, allowed_types=()):
    """G-5 — QUESTION FORMAT AND TYPE COVERAGE.

    Every Example and Recall must match the fixed template, its type must be a
    member of the blueprint's allowed_question_types, and across the unit the
    allowed types must be represented where evidence permits.
    """
    findings = []
    allowed = {t.upper() for t in (allowed_types or ())}
    seen, n = set(), 0
    for i, b in enumerate(model.get("blocks", [])):
        t = b.get("type")
        if t not in ("example", "recall"):
            continue
        n += 1
        qt = (b.get("qtype") or "").upper()
        seen.add(qt)
        if allowed and qt not in allowed:
            findings.append(f"block {i}: type {qt} is not in the blueprint's "
                            f"allowed_question_types {sorted(allowed)}")
        if not b.get("stem"):
            findings.append(f"block {i}: no stem")
        if qt in ("MCQ", "MSQ") and len(b.get("options") or []) != 4:
            findings.append(f"block {i}: {qt} must print exactly 4 options")
        if qt == "NAT" and (b.get("options") or []):
            findings.append(f"block {i}: NAT must not print options")
        if t == "example" and not b.get("explanation"):
            findings.append(f"block {i}: Example without an Explanation")
        if t == "example":
            # v2.3: DISTRACTOR AUTOPSY + EDUCATIONAL OBJECTIVE (section 4 B3).
            # Re-assert on the shipped model what validate_model gates at
            # construction: a one-line Objective, and one autopsy line per
            # WRONG option (MCQ 3; MSQ 4 − #correct; NAT >= 1 trap value).
            if not b.get("objective"):
                findings.append(f"block {i}: Example without a one-line "
                                f"Educational Objective (section 4 B3)")
            ww = b.get("why_wrong") or []
            if qt == "MCQ":
                need = 3
            elif qt == "MSQ":
                need = 4 - len([p for p in str(b.get("answer", "")).split(",")
                                if p.strip()])
            else:                                        # NAT — no fixed count
                need = None
            if need is not None and len(ww) != need:
                findings.append(f"block {i}: {qt} needs one distractor-autopsy "
                                f"line per wrong option ({need}); found "
                                f"{len(ww)} (section 4 B3)")
            elif need is None and len(ww) < 1:
                findings.append(f"block {i}: NAT needs at least one trap-value "
                                f"line (section 4 B3)")
        if t == "recall" and (b.get("explanation") or b.get("speed_hack")):
            findings.append(f"block {i}: Recall must carry neither an "
                            f"Explanation nor a SPEED HACK (section 4 B7)")
        if t == "recall" and (b.get("why_wrong") or b.get("objective")):
            findings.append(f"block {i}: Recall must carry neither a distractor "
                            f"autopsy nor an Educational Objective (section 4 "
                            f"B7)")
    missing = sorted(allowed - seen) if allowed and n else []
    return (not findings, findings,
            {"questions": n, "types_present": sorted(seen),
             "allowed_types_unused": missing})


_XREF = re.compile(r"\bsee\s+(\d+(?:\.\d+){1,2})\b", re.I)


def gate_outline(model, docx_path=None):
    """G-6 — OUTLINE-NUMBER INTEGRITY.

    Level numbering gapless and sequential, and every in-text cross-reference
    resolving to a number that exists. notes_docx.outline_of is the oracle:
    numbers are derived from block order, so a stale reference is the only way
    this can break — and a stale reference is exactly what NA's editing can
    introduce.
    """
    import notes_docx
    o = notes_docx.outline_of(model)
    findings = []
    valid = {n for _, n, _ in o["l2"]} | {n for _, n, _ in o["l3"]}
    tail = [int(x.split(".")[1]) for _, x, _ in o["l2"]]
    if tail and tail != list(range(1, len(tail) + 1)):
        findings.append(f"level-2 numbers are not gapless: "
                        f"{[n for _, n, _ in o['l2']]}")
    body = json.dumps(model, ensure_ascii=False)
    refs = set(_XREF.findall(body))
    for r in sorted(refs - valid):
        findings.append(f"cross-reference 'see {r}' does not resolve to any "
                        f"outline number in this unit")
    return (not findings, findings,
            {"numbers": len(valid), "cross_references": len(refs)})


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
    # Boundary-preserving text (notes_core.document_text). The old form was
    # re.sub(r"<[^>]+>", "", document_xml(...)) — a bare tag strip, which welds
    # adjacent paragraphs together. A box ending "Answer: 1" immediately before
    # the heading "2.10 MIND MAP" then reads "12.10", the level-2 scan below
    # matches "12.10" instead of "2.10", and a CORRECT document is failed for a
    # missing outline number. Run boundaries must NOT separate (Word may split
    # "2.10" into two runs); paragraph boundaries MUST.
    text = notes_core.document_text(docx_path)
    for m in re.finditer(r"Example\s+(\d+)", text):
        printed_ex.append(int(m.group(1)))
    for m in re.finditer(r"Recall\s+(\d+)", text):
        printed_rc.append(int(m.group(1)))
    # The lookarounds must reject only a LEVEL-3 number ("7.3.1" must not
    # yield "7.3" or "3.1"), never an ordinary full stop in the preceding
    # sentence. An earlier form used (?<![\d.]) and therefore missed every bar
    # whose preceding text ended in "." — "…ceiling rate.7.2 TRAP BOX" — which
    # is most of them, since bullets end in full stops. That produced a
    # false-positive G-10 failure on a perfectly correct document.
    for m in re.finditer(r"(?<!\d)(?<!\d\.)(\d+)\.(\d+)(?!\.?\d)", text):
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


def _prose_of(node):
    """Human-readable PROSE carried by a model node — never its markup.

    The first form of this gate ran the term regex over json.dumps(block),
    which is a serialisation, not prose: every OMML tag and attribute name
    inside a math run ("degHide", "radPr", "subHide", "oMath", schema URL
    words) and every model KEY ("stem", "options", "explanation") became a
    "term". Those tokens are then orphans whenever they occur in a question's
    maths but not the body's, so a perfectly good unit reports dozens of
    findings and the advisory gate becomes noise that no one reads.
    Only "text" and "sym" runs carry prose; "math" runs are skipped whole.
    """
    out = []

    def walk(n):
        if isinstance(n, dict):
            if n.get("t") == "math":
                return                      # OMML is markup, never prose
            if n.get("t") == "text":
                out.append(n.get("s", ""))
                return
            if n.get("t") == "sym":
                out.extend([n.get("base", ""), n.get("sub", ""),
                            n.get("sup", "")])
                return
            for k, v in n.items():
                if k in ("image", "type", "k", "kind", "qtype", "schema"):
                    continue               # paths and enums are not prose
                if isinstance(v, str):
                    if k in ("name", "label", "answer"):
                        out.append(v)
                else:
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(node)
    return " ".join(x for x in out if x)


def syllabus_terms_for(unit_questions, extra=()):
    """Harvest the unit's SYLLABUS-EVIDENCED vocabulary for G-9's
    domain-anchored mode (GAP-2026-08-12-NAPARSE owner decision OD-2,
    Design A).

    Evidence the pipeline already carries: every bank question's concept_tags
    (written at Step NB) plus any extra strings the caller supplies — the
    resolved unit's subject/topic/subtopic names are the intended extras.
    Returns a lowercase frozenset of _TERM tokens. Nothing is downloaded and
    no stopword list exists anywhere: the exam's own artifacts are the only
    authority, which is what keeps the gate exam-agnostic across the corpus —
    an English stopword list would silently suppress words like 'potential'
    that ARE syllabus terms in Physics.
    """
    words = set()
    for q in unit_questions or ():
        for tag in (q.get("concept_tags") or ()):
            words |= {w.lower() for w in _TERM.findall(str(tag))}
    for s in extra:
        words |= {w.lower() for w in _TERM.findall(str(s))}
    return frozenset(words)


def gate_orphan_terms(model, allowed=(), syllabus_terms=None):
    """G-9 — ORPHAN TERMS. A term used in a question stem, option or
    explanation that appears NOWHERE in the notes body breaks the closed-book
    promise at vocabulary level.

    The solve in §2 is performed by a reader who already knows the subject, so
    it can silently supply a missing term and still reach the right answer.
    This gate cannot: it is pure set difference over the document's own text.
    Reported as findings for NA to judge, not as an automatic hard stop —
    common English is not a syllabus term.

    DOMAIN-ANCHORED MODE (owner decision OD-2, Design A — GAP-2026-08-12-
    NAPARSE §5.5). Passing syllabus_terms (build it with syllabus_terms_for)
    reports an orphan ONLY when it is also syllabus-evidenced — i.e. the term
    appears in the unit's concept_tags or names. That is what makes the gate
    mean what its name says: on the reference unit the raw set difference
    produced 46 findings of which exactly one ('potential') was real, and
    'potential' is an ordinary English word, so no stopword list could ever
    separate it from the noise — only domain evidence can. The unanchored
    form (syllabus_terms=None) is retained for callers with no bank in hand;
    its meta records mode 'unanchored' so a report always shows which form
    ran. USABILITY BAR: a clean unit must yield ZERO findings in anchored
    mode.
    """
    body_words, q_words = set(), {}
    for b in model.get("blocks", []):
        t = b.get("type")
        if t in ("title", "concept", "key_points", "trap", "rapid", "mindmap"):
            body_words |= {w.lower() for w in _TERM.findall(_prose_of(b))}
        elif t in ("example", "recall"):
            # Scope is EXACTLY §5 G-9's wording — "a term used in a stem,
            # option or explanation". SPEED HACK is deliberately excluded;
            # widening the scope is a SPEC decision, not an engine one.
            txt = _prose_of({k: v for k, v in b.items()
                             if k in ("stem", "options", "explanation")})
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
    if syllabus_terms is not None:
        anchor = {str(w).lower() for w in syllabus_terms}
        anchored = [w for w in orphans if w in anchor]
        return (not anchored,
                [f"syllabus term used only in a question, never taught in "
                 f"the notes: {w!r}" for w in anchored],
                {"terms_checked": len(q_words), "mode": "domain-anchored",
                 "suppressed_unanchored": len(orphans) - len(anchored)})
    return (not orphans, [f"term used only in a question, never taught in the "
                          f"notes: {w!r}" for w in orphans],
            {"terms_checked": len(q_words), "mode": "unanchored"})


def gate_coverage(model, target):
    """G-12 — COVERAGE (v2.4). target comes from
    notes_core.coverage_target_for on the unit's bank slice.

    HARD (findings, blocking): every required_type appears in >= 1 Example;
    Examples span >= min_concepts_with_examples DISTINCT concept sections.
    An Example's concept is the nearest PRECEDING concept block — derived
    from block order like every number in the document, so the mapping can
    never go stale and no new model field is needed.

    ADVISORY (meta only, never blocks): requires_figure with no concept
    figure in the model; duplicate_suspects — concept sections carrying more
    than one Example of the same qtype. Scenario diversity within a concept
    is NA's judgement (§2A), not a regex's.

    With target=None the gate reports DORMANT (the G-7a discipline): a
    caller with no bank in hand still gets every GATES identifier in its
    report, and absence never halts an audit."""
    if target is None:
        return (True, ["no coverage target supplied — gate DORMANT but "
                       "reported (build the target with "
                       "notes_core.coverage_target_for)"],
                {"dormant": True})
    findings = []
    cur_concept, concept_names = None, {}
    concepts_hit, types_present, dup_counter = set(), set(), {}
    has_figure = False
    for i, b in enumerate(model.get("blocks", [])):
        t = b.get("type")
        if t == "concept":
            cur_concept = i
            concept_names[i] = b.get("name", f"block {i}")
            if any(c.get("k") == "figure" for c in b.get("content", [])):
                has_figure = True
        elif t == "example":
            qt = (b.get("qtype") or "").upper()
            types_present.add(qt)
            if cur_concept is not None:
                concepts_hit.add(cur_concept)
                dup_counter[(cur_concept, qt)] = (
                    dup_counter.get((cur_concept, qt), 0) + 1)
    for rt in target.get("required_types", []):
        if rt not in types_present:
            findings.append(
                f"the unit's own bank attests question type {rt} but no "
                f"worked Example teaches it (section 4 B3a)")
    need = int(target.get("min_concepts_with_examples", 0))
    if len(concepts_hit) < need:
        findings.append(
            f"Examples span {len(concepts_hit)} distinct concept section(s) "
            f"but the unit's bank evidence requires {need} — concept SPREAD, "
            f"not example count, is the contract (section 4 B3a)")
    dup_suspects = sorted(
        f"{concept_names.get(ci, ci)} carries {n} Examples of one type"
        for (ci, _qt), n in dup_counter.items() if n > 1)
    meta = {"dormant": False,
            "concepts_with_examples": len(concepts_hit),
            "concepts_required": need,
            "types_present": sorted(types_present),
            "types_required": list(target.get("required_types", [])),
            "duplicate_suspects": dup_suspects,
            "figure_advisory": bool(target.get("requires_figure"))
            and not has_figure}
    return (not findings, findings, meta)


def gate_integration(model, target):
    """G-13 — INTEGRATION (v2.5). target comes from
    notes_core.integration_target_for on the bank (latest-partner filing).

    HARD (findings, blocking) only when the target ATTESTS a fusion for this
    unit: every attested fusion must be taught by an INTEGRATION SECTION — a
    concept block whose FIRST bullet is the Combines declaration ("Combines:
    ...", NC section 4 B4a I-2; the mechanical marker, so no new model field
    exists and W-3 is untouched) naming every partner subtopic; integration
    sections sit AFTER every core concept section (the end of the concept
    stack, before the Trap Box); and a matched section carries >= 1 worked
    Example.

    DORMANT, never blocking: target=None (bank-less caller — the G-7a
    discipline) and target["dormant"]=True — the GRANDFATHERED case: a bank
    with no integration_partners field anywhere predates notes-pyq-bank/1.2
    and could not have carried the evidence. Both are REPORTED.

    ADVISORY (meta only): unattested_sections — integration sections present
    with no bank attestation (SME bridge-justified under D-6; NA's judgement,
    never a finding)."""
    if target is None:
        return (True, ["no integration target supplied — gate DORMANT but "
                       "reported (build the target with "
                       "notes_core.integration_target_for)"],
                {"dormant": True})
    if target.get("dormant"):
        return (True, ["bank carries no integration_partners field anywhere "
                       "— gate DORMANT (grandfathered: the bank predates "
                       "notes-pyq-bank/1.2 and could not attest a fusion)"],
                {"dormant": True, "grandfathered": True})

    def _text(runs):
        return "".join(r.get("s", "") for r in runs or ()
                       if isinstance(r, dict))

    integ, cur = [], None
    core_after_integration = False
    for i, b in enumerate(model.get("blocks", [])):
        t = b.get("type")
        if t == "concept":
            content = b.get("content", [])
            first = content[0] if content else None
            declared = None
            if isinstance(first, dict) and first.get("k") == "bullet":
                s = _text(first.get("runs"))
                if s.strip().startswith("Combines:"):
                    declared = s
            if declared is not None:
                cur = {"i": i, "name": b.get("name", f"block {i}"),
                       "combines": declared, "examples": 0}
                integ.append(cur)
            else:
                if integ:
                    core_after_integration = True
                cur = None
        elif t == "example" and cur is not None:
            cur["examples"] += 1
        elif t in ("trap", "rapid", "recall", "mindmap"):
            cur = None
    findings = []
    if core_after_integration:
        findings.append(
            "a core concept section appears AFTER an integration section — "
            "integration sections close the concept stack, immediately "
            "before the Trap Box (NC section 4 B4a I-1)")
    norm = lambda s: " ".join(str(s).lower().split())
    matched = set()
    for f in target.get("fusions", []):
        partners = f.get("partners", [])
        hit = next((sec for sec in integ
                    if all(norm(p) in norm(sec["combines"])
                           for p in partners)), None)
        if hit is None:
            findings.append(
                f"the unit's own bank attests fusion with "
                f"{', '.join(partners)} ({len(f.get('bank_ids', []))} "
                f"question(s)) but no integration section declares it in a "
                f"Combines line (NC section 4 B4a)")
        else:
            matched.add(hit["i"])
            if hit["examples"] < 1:
                findings.append(
                    f"integration section {hit['name']!r} declares the "
                    f"fusion but carries no worked Example (NC section 4 "
                    f"B4a I-3)")
    meta = {"dormant": False,
            "integration_sections": len(integ),
            "fusions_required": len(target.get("fusions", [])),
            "fusions_taught": len(matched),
            "unattested_sections": sorted(sec["name"] for sec in integ
                                          if sec["i"] not in matched)}
    return (not findings, findings, meta)


def terminal_regate(docx_path, model, *, tier, page_count, exemptions=(),
                    expected_omml=0, orphan_allowed=(), allowed_types=(),
                    syllabus_terms=None, coverage_target=None,
                    integration_target=None):
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
    ok_an, f_an, m_an = gate_anatomy(model)
    g["G-3"] = {"ok": ok_an, "findings": f_an, "meta": m_an}
    ok_q, f_q, m_q = gate_question_format(model, allowed_types)
    g["G-5"] = {"ok": ok_q, "findings": f_q, "meta": m_q}
    ok_ol, f_ol, m_ol = gate_outline(model, docx_path)
    g["G-6"] = {"ok": ok_ol, "findings": f_ol, "meta": m_ol}
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
    ok_r, f_r, m_r = gate_orphan_terms(model, orphan_allowed,
                                       syllabus_terms=syllabus_terms)
    g["G-9"] = {"ok": ok_r, "findings": f_r, "meta": m_r}
    ok_c, f_c, m_c = gate_counters(model, docx_path)
    g["G-10"] = {"ok": ok_c, "findings": f_c, "meta": m_c}
    # v2.4: G-12 COVERAGE. BLOCKING when a coverage_target is supplied;
    # DORMANT-but-reported without one (the G-7a discipline) so every GATES
    # identifier still appears in every report.
    ok_v, f_v, m_v = gate_coverage(model, coverage_target)
    g["G-12"] = {"ok": ok_v, "findings": f_v, "meta": m_v,
                 "dormant": bool(m_v.get("dormant"))}
    # v2.5: G-13 INTEGRATION. BLOCKING when the target attests a fusion for
    # this unit; DORMANT-but-reported without a target OR when the bank is
    # GRANDFATHERED (no integration_partners anywhere — pre-1.2 bank).
    ok_g, f_g, m_g = gate_integration(model, integration_target)
    g["G-13"] = {"ok": ok_g, "findings": f_g, "meta": m_g,
                 "dormant": bool(m_g.get("dormant"))}
    sha = notes_core.file_sha256(docx_path)
    # G-11 IS this function: the assertion that everything above ran against
    # the file that will ship, not against the pre-patch draft. Recorded as a
    # gate so audit_summary shows plainly WHICH bytes were certified.
    ran = [k for k in g if k.startswith("G-")]
    g["G-11"] = {"ok": True, "findings": [],
                 "meta": {"certified_sha256": sha, "gates_run": len(ran),
                          "path": os.path.basename(docx_path)}}
    g["_sha256"] = sha
    # G-9 is advisory (English words are not syllabus terms); G-7a, a
    # target-less G-12 and a target-less or grandfathered G-13 may be
    # dormant; none of those block. Everything else is blocking.
    blocking = [k for k, v in g.items()
                if k.startswith("G-") and k not in ("G-9", "G-7a")
                and not v.get("dormant") and not v["ok"]]
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
    import copy
    import tempfile
    import notes_docx

    T = lambda s: [{"t": "text", "s": s}]

    def _tiny_png():
        """Smallest valid PNG, written once — the mindmap block requires an
        image and build() raises a raw KeyError without one."""
        import base64
        path = tempfile.mktemp(suffix=".png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42m"
                "NkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="))
        return path

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
                     "explanation": [T("Substrate saturates the enzyme.")],
                     # v2.3: default fixture is MCQ answer "2" -> 3 wrong.
                     "why_wrong": [T("Option a drops the denominator."),
                                   T("Option c inverts the ratio."),
                                   T("Option d confuses the two constants.")],
                     "objective": T("Read the rate from the saturating form.")},
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
    # A bar whose preceding text ends in a full stop must still be seen. The
    # first form of this gate used a (?<![\d.]) lookbehind and missed every
    # such bar — i.e. most of them, since bullets end in full stops — failing
    # a correct document. Full-anatomy fixture, prose ending in "." throughout.
    full = {"schema": notes_docx.SCHEMA, "exam_code": "EX",
            "unit": {"name": "Enzyme Kinetics", "tier": "TIER-2",
                     "seq_in_topic": 7},
            "blocks": [
                {"type": "title", "name": "Enzyme Kinetics"},
                {"type": "concept", "name": "Saturation kinetics",
                 "content": [{"k": "bullet",
                              "runs": T("Rate saturates as substrate rises.")}]},
                {"type": "example", "qtype": "MCQ", "stem": T("Which holds?"),
                 "options": [T("a"), T("b"), T("c"), T("d")], "answer": "2",
                 "explanation": [T("Substitute and simplify.")],
                 "why_wrong": [T("Option a drops the denominator."),
                               T("Option c inverts the ratio."),
                               T("Option d confuses the two constants.")],
                 "objective": T("Read the rate from the saturating form.")},
                {"type": "key_points",
                 "bullets": [T("Saturation sets the ceiling rate.")]},
                {"type": "trap",
                 "bullets": [T("It is not a binding constant.")]},
                {"type": "rapid",
                 "formulae": [[T("Name"), T("Form")], [T("MM"), T("v")]],
                 "associations": [[T("Term"), T("Link")], [T("x"), T("y")]]},
                {"type": "recall", "qtype": "MCQ",
                 "stem": T("Which is correct?"),
                 "options": [T("a"), T("b"), T("c"), T("d")],
                 "answer": "3"}]}
    fp = tempfile.mktemp(suffix=".docx")
    notes_docx.build(full, fp)
    ok_f, f_f, _ = gate_counters(full, fp)
    check("G-10 sees a bar preceded by a full stop (regression: the old "
          "lookbehind failed a correct full-anatomy document)",
          ok_f and not f_f)
    check("G-10 still rejects a level-3 number as if it were level-2",
          all("." not in n.split(".", 2)[-1]
              for n in [x for _, x, _ in notes_docx.outline_of(full)["l2"]]))

    # REGRESSION (GAP-2026-08-12-NAPARSE D-2): a section heading whose printed
    # number is immediately preceded by a DIGIT. The last RECALL CHECK item
    # ends "Answer: 1" and the MIND MAP heading follows, so a bare tag strip
    # yields "12.10" and the level-2 scan never sees "2.10". This fixture is
    # the standard tail anatomy — every unit in every exam ends this way — so
    # the old form failed a correct document on essentially the whole corpus.
    # SIX concepts + TRAP + RAPID + RECALL CHECK + MIND MAP = ten level-2
    # sections, so the MIND MAP heading derives the two-digit number "2.10" —
    # the shape that exposes the bug. A one-digit tail cannot expose it.
    tail = {"schema": notes_docx.SCHEMA, "exam_code": "EX",
            "unit": {"name": "Enzyme Kinetics", "tier": "TIER-2",
                     "seq_in_topic": 2},
            "blocks": [{"type": "title", "name": "Enzyme Kinetics"}]}
    for c in range(6):
        tail["blocks"] += [
            {"type": "concept", "name": f"Concept {c}",
             "content": [{"k": "bullet", "runs": T("A bullet ending in a "
                                                   "full stop.")}]},
            {"type": "key_points", "bullets": [T("A consolidating line.")]}]
    tail["blocks"] += [
        {"type": "trap", "bullets": [T("A recurring wrong-option pattern.")]},
        {"type": "rapid",
         "formulae": [[T("Name"), T("Form")], [T("MM"), T("v")]],
         "associations": [[T("Term"), T("Link")], [T("x"), T("y")]]},
        {"type": "recall", "qtype": "MCQ", "stem": T("Which is correct?"),
         "options": [T("a"), T("b"), T("c"), T("d")], "answer": "1"},
        {"type": "mindmap", "image": _tiny_png()}]
    tp = tempfile.mktemp(suffix=".docx")
    notes_docx.build(tail, tp, strict=False)
    derived_tail = [n for _, n, _ in notes_docx.outline_of(tail)["l2"]]
    ok_t, f_t, _ = gate_counters(tail, tp)
    check("G-10 sees a heading number preceded by a digit "
          "(Answer: 1 then 2.10 MIND MAP)", ok_t and not f_t)
    check("the digit-adjacency fixture really does derive a two-digit "
          "level-2 number", any(n.endswith(".10") for n in derived_tail))

    # ---- G-9 orphan terms ----------------------------------------------
    orph = demo_model()
    orph["blocks"][2]["stem"] = orph["blocks"][2]["stem"] + [
        {"t": "text", "s": " Assume allosteric behaviour."}]
    ok9, f9, _ = gate_orphan_terms(orph)
    joined9 = " ".join(f9)
    check("G-9 flags a term used only in the question and never taught",
          not ok9 and "allosteric" in joined9)
    # REGRESSION (GAP-2026-08-12-NAPARSE D-3): the gate used to run the term
    # regex over json.dumps(block), so OMML/LaTeX markup and model KEYS became
    # "terms". A clean unit then reported dozens of phantom orphans and the
    # advisory gate was noise. None of these may ever appear again.
    for phantom in ("frac", "latex", "stem", "options", "explanation",
                    "deghide", "radpr", "subhide", "omath"):
        check(f"G-9 never reports markup or a model key as a term "
              f"({phantom})", phantom not in joined9.lower())
    ok9c, f9c, _ = gate_orphan_terms(demo_model())
    check("G-9 is clean on a unit whose question vocabulary is all taught",
          ok9c and not f9c)
    # DOMAIN-ANCHORED MODE (GAP-2026-08-12-NAPARSE owner decision OD-2,
    # Design A). The reference unit produced 46 raw orphans of which exactly
    # ONE ('potential') was a genuine syllabus term; a stopword list would
    # suppress it, only domain evidence can keep it. These checks pin the
    # contract: syllabus-evidenced orphans REPORT, unevidenced ones are
    # SUPPRESSED and counted, and a clean unit yields ZERO findings.
    syl = syllabus_terms_for(
        [{"concept_tags": ["Allosteric regulation", "Enzyme kinetics"]}],
        extra=("Biochemistry",))
    check("syllabus_terms_for harvests concept_tags and extras",
          {"allosteric", "regulation", "enzyme", "kinetics",
           "biochemistry"} <= set(syl))
    ok9a, f9a, m9a = gate_orphan_terms(orph, syllabus_terms=syl)
    check("G-9 anchored mode reports a syllabus-evidenced orphan",
          not ok9a and "allosteric" in " ".join(f9a)
          and m9a["mode"] == "domain-anchored")
    noise = demo_model()
    noise["blocks"][2]["stem"] = noise["blocks"][2]["stem"] + [
        {"t": "text", "s": " Assume arbitrary behaviour hence."}]
    ok9n, f9n, m9n = gate_orphan_terms(noise, syllabus_terms=syl)
    check("G-9 anchored mode suppresses common-English orphans and counts "
          "them", ok9n and not f9n and m9n["suppressed_unanchored"] >= 1)
    ok9z, f9z, _ = gate_orphan_terms(demo_model(), syllabus_terms=syl)
    check("G-9 anchored mode is ZERO-findings on a clean unit (the "
          "usability bar)", ok9z and not f9z)
    check("G-9 unanchored mode records its mode",
          gate_orphan_terms(demo_model())[2]["mode"] == "unanchored")
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
    check("v2.1: G-11 is REPORTED as a gate, carrying the certified sha256",
          gates["G-11"]["ok"] is True
          and gates["G-11"]["meta"]["certified_sha256"] == gates["_sha256"]
          and gates["G-11"]["meta"]["gates_run"] >= 10)
    check("v2.1: every identifier in GATES appears in a re-gate report",
          set(GATES) <= set(k for k in gates if k.startswith("G-")))
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
    # v2.4: G-12 in the terminal re-gate — dormant without a target, blocking
    # with a violated one.
    check("v2.4: a target-less re-gate reports G-12 DORMANT and does not "
          "block on it",
          gates["G-12"]["dormant"] is True
          and "G-12" not in gates["_blocking_failures"])
    gates_cov = terminal_regate(
        good, m, tier="TIER-2", page_count=5, expected_omml=1,
        coverage_target={"required_types": ["MCQ", "NAT"],
                         "min_concepts_with_examples": 2,
                         "requires_figure": False, "pyq_count": 4,
                         "distinct_concept_tags": 2})
    check("v2.4: a violated coverage target BLOCKS the terminal re-gate "
          "(demo model has one concept, one MCQ)",
          not gates_cov["_ok"] and "G-12" in gates_cov["_blocking_failures"])
    gates_cov_ok = terminal_regate(
        good, m, tier="TIER-2", page_count=5, expected_omml=1,
        coverage_target={"required_types": ["MCQ"],
                         "min_concepts_with_examples": 1,
                         "requires_figure": False, "pyq_count": 1,
                         "distinct_concept_tags": 1})
    check("v2.4: a satisfied coverage target certifies", gates_cov_ok["_ok"])
    # v2.5: G-13 in the terminal re-gate — dormant without a target or
    # grandfathered, blocking with a violated live one.
    check("v2.5: a target-less re-gate reports G-13 DORMANT and does not "
          "block on it",
          gates["G-13"]["dormant"] is True
          and "G-13" not in gates["_blocking_failures"])
    gates_int = terminal_regate(
        good, m, tier="TIER-2", page_count=5, expected_omml=1,
        integration_target={"dormant": False, "attested": True,
                            "fusions": [{"partners": ["Capacitors"],
                                         "bank_ids": ["I-1"]}],
                            "pyq_count": 1})
    check("v2.5: an attested-but-untaught fusion BLOCKS the terminal "
          "re-gate (demo model has no integration section)",
          not gates_int["_ok"] and "G-13" in gates_int["_blocking_failures"])
    gates_gf = terminal_regate(
        good, m, tier="TIER-2", page_count=5, expected_omml=1,
        integration_target={"dormant": True, "attested": False,
                            "fusions": [], "pyq_count": 0})
    check("v2.5: a GRANDFATHERED pre-1.2 bank never blocks G-13",
          gates_gf["G-13"]["dormant"] is True
          and "G-13" not in gates_gf["_blocking_failures"])

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

    # ---- v2.1: G-3 / G-5 / G-6 are now MECHANICAL --------------------
    # Framework_NotesAudit section 5 said the terminal re-gate re-runs "EVERY
    # gate above", but three identifiers were emitted by nothing — a spec
    # promise with no enforcement behind it.
    ok_an, f_an, _ = gate_anatomy(m)
    check("G-3 passes a well-formed unit", ok_an)
    noKP = copy.deepcopy(m)
    noKP["blocks"] = [b for b in noKP["blocks"] if b["type"] != "key_points"]
    check("G-3 catches a concept with no KEY POINTS box",
          not gate_anatomy(noKP)[0])

    ok_q, f_q, m_q = gate_question_format(m, ("MCQ", "NAT"))
    check("G-5 passes a template-conformant question", ok_q)
    check("G-5 reports which allowed types went unused",
          m_q["allowed_types_unused"] == ["NAT"])
    check("G-5 catches a type outside the blueprint's allowed set",
          not gate_question_format(m, ("NAT",))[0])
    badopt = copy.deepcopy(m)
    badopt["blocks"][2]["options"] = [T("a"), T("b")]
    check("G-5 catches an MCQ that does not print 4 options",
          not gate_question_format(badopt, ("MCQ",))[0])
    # The demo model carries no Recall, so the block is ADDED here rather
    # than mutated in place — a mutation with no target silently passes and
    # proves nothing.
    recall_bad = copy.deepcopy(m)
    recall_bad["blocks"].append(
        {"type": "recall", "qtype": "MCQ", "stem": T("Which is correct?"),
         "options": [T("a"), T("b"), T("c"), T("d")], "answer": "3",
         "explanation": [T("a Recall must not carry this")]})
    ok_rb, f_rb, _ = gate_question_format(recall_bad, ("MCQ",))
    check("G-5 catches a Recall carrying an Explanation",
          not ok_rb and any("Recall must carry neither" in x for x in f_rb))
    recall_ok = copy.deepcopy(recall_bad)
    recall_ok["blocks"][-1].pop("explanation")
    check("G-5 accepts a well-formed Recall",
          gate_question_format(recall_ok, ("MCQ",))[0])
    # v2.3: G-5 enforces the distractor autopsy + Educational Objective.
    noobj = copy.deepcopy(m)
    noobj["blocks"][2].pop("objective")
    ok_no, f_no, _ = gate_question_format(noobj, ("MCQ",))
    check("G-5 catches an Example missing its Educational Objective",
          not ok_no and any("Educational Objective" in x for x in f_no))
    feww = copy.deepcopy(m)
    feww["blocks"][2]["why_wrong"] = [T("only one line")]
    ok_fw, f_fw, _ = gate_question_format(feww, ("MCQ",))
    check("G-5 catches an MCQ with fewer autopsy lines than wrong options",
          not ok_fw and any("per wrong option" in x for x in f_fw))
    rc_obj = copy.deepcopy(recall_ok)
    rc_obj["blocks"][-1]["objective"] = T("Recall must not carry this.")
    check("G-5 catches a Recall carrying an Educational Objective",
          not gate_question_format(rc_obj, ("MCQ",))[0])

    # ---- v2.4: G-12 coverage --------------------------------------------
    def cov_model(placements):
        """Two concepts; placements = [(concept_idx 0/1, qtype), ...]."""
        blocks = [{"type": "title", "name": "U"},
                  {"type": "concept", "name": "Regimes", "content": []},
                  {"type": "concept", "name": "Inhibition", "content": []}]
        cidx = {0: 1, 1: 2}
        out = blocks[:2]
        first = [{"type": "example", "qtype": qt,
                  "stem": T("s"), "options": [] if qt == "NAT"
                  else [T("a"), T("b"), T("c"), T("d")],
                  "answer": "1.0" if qt == "NAT" else "2"}
                 for c, qt in placements if c == 0]
        second = [{"type": "example", "qtype": qt,
                   "stem": T("s"), "options": [] if qt == "NAT"
                   else [T("a"), T("b"), T("c"), T("d")],
                   "answer": "1.0" if qt == "NAT" else "2"}
                  for c, qt in placements if c == 1]
        return {"schema": notes_docx.SCHEMA, "exam_code": "EX",
                "unit": {"name": "U", "tier": "TIER-2", "seq_in_topic": 1},
                "blocks": (out + first + [blocks[2]] + second)}
    tgt2 = {"required_types": ["MCQ", "NAT"],
            "min_concepts_with_examples": 2, "requires_figure": False,
            "pyq_count": 4, "distinct_concept_tags": 2}
    ok12, f12, m12 = gate_coverage(
        cov_model([(0, "MCQ"), (1, "NAT")]), tgt2)
    check("G-12 passes a unit whose Examples span the required concepts "
          "and types", ok12 and m12["concepts_with_examples"] == 2)
    ok12b, f12b, _ = gate_coverage(cov_model([(0, "MCQ"), (1, "MCQ")]), tgt2)
    check("G-12 catches a bank-attested type with no Example",
          not ok12b and any("attests question type NAT" in x for x in f12b))
    ok12c, f12c, _ = gate_coverage(cov_model([(0, "MCQ"), (0, "NAT")]), tgt2)
    check("G-12 catches concept HOGGING — types satisfied but Examples "
          "crowd one concept section",
          not ok12c and any("SPREAD" in x for x in f12c))
    tgt1 = dict(tgt2, min_concepts_with_examples=1, required_types=["MCQ"])
    ok12d, f12d, m12d = gate_coverage(
        cov_model([(0, "MCQ"), (0, "MCQ")]), tgt1)
    check("G-12 flags same-concept same-type clones as ADVISORY "
          "duplicate_suspects, never a block",
          ok12d and not f12d and len(m12d["duplicate_suspects"]) == 1)
    tgtf = dict(tgt1, requires_figure=True)
    ok12e, _, m12e = gate_coverage(cov_model([(0, "MCQ")]), tgtf)
    check("G-12 figure requirement is ADVISORY meta, never a finding",
          ok12e and m12e["figure_advisory"] is True)
    ok12f, f12f, m12f = gate_coverage(cov_model([(0, "MCQ")]), None)
    check("G-12 without a target is DORMANT-but-reported (the G-7a "
          "discipline)", ok12f and m12f["dormant"] is True and f12f)
    zero = {"required_types": [], "min_concepts_with_examples": 0,
            "requires_figure": False, "pyq_count": 0,
            "distinct_concept_tags": 0}
    check("G-12 passes a no-evidence unit against the ZERO target "
          "(no examples where no evidence)",
          gate_coverage({"blocks": [{"type": "title", "name": "U"}]},
                        zero)[0])

    # ---- v2.5: G-13 integration -----------------------------------------
    def integ_model(combines=None, integ_examples=1, core_after=False):
        """One core concept + optionally one integration section (a concept
        whose FIRST bullet is the Combines declaration)."""
        blocks = [{"type": "title", "name": "U"},
                  {"type": "concept", "name": "Core",
                   "content": [{"k": "bullet", "runs": T("core fact")}]},
                  {"type": "example", "qtype": "MCQ", "stem": T("s"),
                   "options": [T("a"), T("b"), T("c"), T("d")],
                   "answer": "2"}]
        if combines is not None:
            blocks.append({"type": "concept", "name": "Bridge",
                           "content": [{"k": "bullet", "runs": T(combines)},
                                       {"k": "bullet", "runs": T("seam fact")}]})
            blocks += [{"type": "example", "qtype": "MCQ", "stem": T("s"),
                        "options": [T("a"), T("b"), T("c"), T("d")],
                        "answer": "2"}] * integ_examples
        if core_after:
            blocks.append({"type": "concept", "name": "Late Core",
                           "content": [{"k": "bullet", "runs": T("x")}]})
        blocks.append({"type": "trap", "bullets": [T("t")]})
        return {"schema": notes_docx.SCHEMA, "exam_code": "EX",
                "unit": {"name": "U", "tier": "TIER-2", "seq_in_topic": 1},
                "blocks": blocks}
    tgt13 = {"dormant": False, "attested": True,
             "fusions": [{"partners": ["Capacitors"],
                          "bank_ids": ["I-1", "I-2"]}], "pyq_count": 2}
    ok13, f13, m13 = gate_integration(
        integ_model("Combines: Capacitors + this sub topic"), tgt13)
    check("G-13 passes an attested fusion taught by a Combines-led "
          "integration section with an Example",
          ok13 and m13["fusions_taught"] == 1
          and m13["integration_sections"] == 1)
    ok13b, f13b, _ = gate_integration(integ_model(None), tgt13)
    check("G-13 catches an attested fusion with NO integration section",
          not ok13b and any("no integration section declares" in x
                            for x in f13b))
    ok13c, f13c, _ = gate_integration(
        integ_model("Combines: Semiconductors + this sub topic"), tgt13)
    check("G-13 catches a Combines line that names the WRONG partner",
          not ok13c and any("Capacitors" in x for x in f13c))
    ok13d, f13d, _ = gate_integration(
        integ_model("Combines: Capacitors + this sub topic",
                    integ_examples=0), tgt13)
    check("G-13 catches an integration section with no worked Example",
          not ok13d and any("no worked Example" in x for x in f13d))
    ok13e, f13e, _ = gate_integration(
        integ_model("Combines: Capacitors + this sub topic",
                    core_after=True), tgt13)
    check("G-13 catches a core concept AFTER the integration section "
          "(placement: end of the concept stack)",
          not ok13e and any("AFTER an integration section" in x
                            for x in f13e))
    ok13f, f13f, m13f = gate_integration(
        integ_model(None), {"dormant": True, "attested": False,
                            "fusions": [], "pyq_count": 0})
    check("G-13 is DORMANT-but-reported for a GRANDFATHERED pre-1.2 bank",
          ok13f and m13f["dormant"] is True
          and m13f.get("grandfathered") is True and f13f)
    ok13g, f13g, m13g = gate_integration(integ_model(None), None)
    check("G-13 without a target is DORMANT-but-reported (the G-7a "
          "discipline)", ok13g and m13g["dormant"] is True and f13g)
    ok13h, _, m13h = gate_integration(
        integ_model("Combines: Capacitors + this sub topic"),
        {"dormant": False, "attested": False, "fusions": [], "pyq_count": 0})
    check("G-13 lists an unattested integration section as ADVISORY meta, "
          "never a finding",
          ok13h and m13h["unattested_sections"] == ["Bridge"])

    ok_ol, f_ol, m_ol = gate_outline(m)
    check("G-6 passes a gapless outline", ok_ol)
    stale = copy.deepcopy(m)
    stale["blocks"][1]["content"].append(
        {"k": "bullet", "runs": T("Compare with the result in see 9.7 above.")})
    ok_st, f_st, _ = gate_outline(stale)
    check("G-6 catches a cross-reference that resolves to nothing — the one "
          "thing NA's editing can break silently",
          not ok_st and any("does not resolve" in x for x in f_st))
    live_ref = copy.deepcopy(m)
    live_ref["blocks"][1]["content"].append(
        {"k": "bullet", "runs": T("As shown in see 3.1 earlier.")})
    check("G-6 accepts a cross-reference that does resolve",
          gate_outline(live_ref)[0])

    print(f"notes_audit self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("notes_audit.py — Notes Step NA engine. Run with --self-test.")
