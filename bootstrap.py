#!/usr/bin/env python3
"""
LOAD-AND-VERIFY GATE  (runs inside a freshly-cloned framework repo)

Verifies the ENTIRE framework (every file in MANIFEST.json) on every run:
PRESENT + BYTE-EXACT (sha256) + expected VERSION (.md header) + WHOLE
(.md END-sentinel + exact line count). Because the whole framework is verified,
an imperfect routes.json can never cause a missing/partial dependency at runtime.

Contract:
  - Exit 0 AND write .verified  -> only when EVERY tracked file passes.
  - Exit 1 (HARD STOP)          -> on ANY failure. Caller MUST NOT proceed
                                   from memory / project knowledge.

PROJECT-FIRST OVERRIDES (2026.08.03.9)
  Specs are project-first: a Framework_*.md in the exam project's Files section
  overrides the repo copy (see spec_source.py). The resolved corpus in
  /tmp/fw_effective therefore contains specs that CANNOT match MANIFEST.json —
  the manifest describes the repo, and an override is by definition different.

  SKILL RULE 2 runs `bootstrap.py --trigger <Step>` from that overlay. Before
  2026.08.03.9 this reported the override as `sha256 MISMATCH` and hard-stopped
  for EVERY trigger, not just the overridden one, printing an instruction to
  abandon the run — contradicting SKILL rule 4 and Framework_DeliveryFooter §2A,
  which both promise a project-first run never halts.

  So: if a `.spec_provenance.json` written by spec_source.py sits beside the
  manifest, files it lists are reported as PROJECT-UNVERIFIED instead of
  MISMATCH, and do not halt.

  THIS IS NOT A BYPASS.
    - A listed file is still hashed, and must match the sha the RESOLVER
      recorded. Tampering with the overlay after resolution still HARD-STOPS.
    - Only `.md` specs may be listed. An engine can never be excused.
    - A file NOT listed that fails any check still HARD-STOPS, unchanged.
    - The completion banner says VERIFIED only when nothing was overridden;
      otherwise it says PARTIALLY VERIFIED and names every unverified spec.
  What is impossible, and is not attempted, is verifying an override against
  the repo: there is no reference to verify it against.

--trigger is optional and advisory: if given and known, the gate prints the
step's entry files SPLIT BY ROLE — .md specs are to be READ IN FULL; .py engines
are to be EXECUTED via `import` inside the spec's code blocks and must NOT be
read into context (an engine can be thousands of lines; reading it wastes the
session's context for zero benefit — the split exists because a route lists
BOTH kinds and the old single-line advisory said "read IN FULL" for all of
them). Verification always covers all files regardless of trigger.

Usage:
    python3 bootstrap.py                     # verify whole framework
    python3 bootstrap.py --trigger MockDeliver
"""
import argparse, hashlib, json, os, sys

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def fail(msg):
    print(f"[HARD STOP] {msg}")
    print("Do NOT generate anything from memory or project knowledge. Stop here.")
    sys.exit(1)

def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [ln.rstrip("\n") for ln in f]

def _session_class(progress_path, files_meta, trigger=None):
    # v2026.08.22.2 (GAP-2026-08-22-STEP9-READ-SET): Step 9's S0-3 law differs from
    # Step 5's §S8-0b on the UNKNOWN case — a fresh mock has no frozen batch plan
    # yet, and reading too little there can let a reduced read reach the end-of-mock
    # writer, so unknown -> FINAL for MockExplain/TestExplain. Step 5's fresh-corpus
    # NON-FINAL rule is unchanged.
    if trigger in ('MockExplain', 'TestExplain') and (
            not progress_path or not os.path.exists(progress_path)):
        return 'FINAL'
    # v2026.08.22.5 (GAP-1B-STEP7-READ-SET): Step 7's S1-0 law is the S0-3 shape,
    # not the §S8-0b shape — a fresh mock has no frozen batch plan yet (S3-16 builds
    # batch_state.json), and reading too little there can let a reduced read reach
    # the Final-Assembly writers, so unknown -> FINAL. With a batch_state.json the
    # plan itself decides: the session is FINAL iff the batch it will deliver is the
    # plan's last (current entry is_final, or remaining batches <= 1). A malformed
    # or schema-alien file is a corrupt state, not a fresh one -> FINAL.
    # v2026.08.22.7 (STEP6-READ-SET): Step 6's S0-READSET law. The progress
    # artefact IS blueprint.json — no file means B1 (read everything, it consumes
    # every input section AND delivers the skeleton per §14/§15); mocks complete
    # means B3 (read everything, it writes every closing output); in between is a
    # B2 batch, which works entirely from blueprint.json state -> NON-FINAL.
    # Malformed or schema-alien -> FINAL (corrupt state, not a fresh one).
    # v2026.08.23 (GAP-2026-08-23-PYQSCAN-SPECBUDGET): one-shot triggers. PYQDraft
    # and PYQApprove have no batch loop — their only session closes the books, and
    # under the generic fresh-corpus rule below (no progress file -> NON-FINAL) that
    # session would skip Framework_PYQCore.md's newly FINAL-only §11/§12 on the very
    # run that must consult them. One-shot => FINAL, unconditionally. The batched
    # PYQ routes are already safe both ways: a fresh PYQScan/PYQCount session is
    # genuinely NON-FINAL, and any session holding a scan/count progress file falls
    # to the schema-alien branch of the generic parser -> FINAL, the safe default.
    if trigger in ('PYQDraft', 'PYQApprove'):
        return 'FINAL'
    if trigger == 'MockBlueprint':
        if not progress_path or not os.path.exists(progress_path):
            return 'FINAL'
        try:
            bp = json.load(open(progress_path, encoding='utf-8'))
            n_done = len(bp['mocks'])
            n_total = int(bp['total_mocks'])
            if n_total > 0 and n_done < n_total:
                return 'NON-FINAL'
            return 'FINAL'
        except Exception:
            return 'FINAL'
    if trigger in ('MockCreate', 'TestCreate'):
        if not progress_path or not os.path.exists(progress_path):
            return 'FINAL'
        try:
            bs = json.load(open(progress_path, encoding='utf-8'))
            plan = bs['batch_plan']
            done = set(bs.get('batches_completed') or [])
            cur = bs.get('current_batch')
            remaining = [b for b in plan if b.get('batch_id') not in done]
            cur_entry = next((b for b in plan if b.get('batch_id') == cur), None)
            if len(remaining) <= 1 or (cur_entry or {}).get('is_final'):
                return 'FINAL'
            return 'NON-FINAL'
        except Exception:
            return 'FINAL'
    """FINAL vs NON-FINAL — Framework_MockTestAnalyse §S8-0b, Framework_PYQCore EC-P42.

    THE AXIS IS NOT FRESH vs RESUME. A session executes the same code whether it is
    session 1 or session 5; what decides which sections it reaches is whether it will
    CLOSE THE BOOKS. Routing on fresh/resume would leave session 1 of every one of the
    ~200 exams exactly as broken as the reference incident.

    Unknown -> FINAL. The default must be the SAFE one: reading too much costs a
    session, reading too little can let a reduced read reach a writer.
    """
    if not progress_path or not os.path.exists(progress_path):
        # FRESH CORPUS. GAP-2026-08-16, deployment review: this returned "FINAL", and
        # the model correctly followed the printed class — so session 1 of the very
        # first live run did a FULL read (552,313 B) when §S8-0b calls for the
        # NON-FINAL set. Measured on IIT_JAM_MATHEMATICS: both batches logged
        # spec_read_mode "full". The read-set fix did not engage on the session it was
        # designed for. It caused no harm only because the direct lane (EC-P43) had
        # removed all context pressure; on a connector-lane deployment session 1 would
        # be back at the original stall.
        # §S8-0b L6782 is the authority and says: "When no progress file exists the
        # corpus has not been enumerated yet, so the count is unknown; decide the class
        # immediately after PHASE A/A1b, which is the first moment it is knowable, and
        # read the NON-FINAL set until then." bootstrap now prints that instead of
        # contradicting it. The safe default is preserved where it belongs — an
        # UNREADABLE or malformed progress file still returns FINAL, because that is a
        # corrupt state rather than a fresh one.
        return "NON-FINAL"
    try:
        prog = json.load(open(progress_path, encoding="utf-8"))
    except Exception:
        # Unreadable/malformed progress file: FINAL. Reading too much costs a session;
        # reading too little can let a reduced read reach a writer.
        return "FINAL"
    meta = prog.get("_meta") or {}
    done = len(meta.get("papers_processed") or [])
    transport = meta.get("_transport") or {}
    # Tolerate the pre-v2.51.0 key for one release (EC-P38: a pre-patch progress file
    # is VALID INPUT and is never discarded).
    planned = transport.get("papers_planned", transport.get("papers_admitted")) or []
    deferred = transport.get("deferred_context") or []
    total = meta.get("total_papers") or (done + len(planned) + len(deferred))
    remaining = max(0, total - done)
    return "NON-FINAL" if remaining > 3 else "FINAL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trigger", default=None, help="optional step trigger, e.g. MockDeliver")
    ap.add_argument("--progress", default=None,
                    help="path to [ExamCode]_analysis_progress.json — decides SESSION "
                         "CLASS and prints the exact read plan (GAP-2026-08-16)")
    ap.add_argument("--manifest", default="MANIFEST.json")
    args = ap.parse_args()

    if not os.path.exists(args.manifest):
        fail("MANIFEST.json missing from clone (partial/failed clone?)")
    try:
        M = json.load(open(args.manifest, encoding="utf-8"))
    except Exception as e:
        fail(f"MANIFEST.json is not valid JSON: {e}")

    prov_path = os.path.join(os.path.dirname(os.path.abspath(args.manifest)),
                             ".spec_provenance.json")
    prov, overrides = None, {}
    if os.path.exists(prov_path):
        try:
            prov = json.load(open(prov_path, encoding="utf-8"))
        except Exception as e:
            fail(f".spec_provenance.json is not valid JSON: {e}")
        for entry in prov.get("project_unverified", []):
            fname = entry.get("file", "")
            if not fname.endswith(".md"):
                fail(f".spec_provenance.json lists a non-spec file '{fname}'. Only "
                     f".md specs may be project-sourced; an engine is never excused "
                     f"from manifest verification.")
            if not entry.get("sha256"):
                fail(f".spec_provenance.json entry for '{fname}' has no sha256 — the "
                     f"record is unusable and cannot excuse the file.")
            overrides[fname] = entry["sha256"]

    files_meta = M.get("files", {})
    routes = M.get("routes", {})
    fw_version = M.get("framework_version", "?")
    if not files_meta:
        fail("MANIFEST.json has no files listed")

    verified, unverified = [], []
    for fname, meta in sorted(files_meta.items()):
        if not os.path.exists(fname):
            fail(f"{fname}: file absent in clone (partial clone / deleted file)")
        actual = sha256(fname)
        if fname in overrides:
            # Deliberately overridden by the project. No repo reference exists, so
            # manifest comparison is meaningless — but the file must still be the one
            # the resolver inspected and approved (P1-P5).
            if actual != overrides[fname]:
                fail(f"{fname}: listed as a project override, but its sha256 does not "
                     f"match the resolver's record\n  resolver saw {overrides[fname]}"
                     f"\n  on disk now  {actual}\n"
                     f"The overlay was modified after resolution. Re-run "
                     f"spec_source.py --resolve.")
            unverified.append(fname)
            continue
        if actual != meta["sha256"]:
            fail(f"{fname}: sha256 MISMATCH\n  expected {meta['sha256']}\n  actual   {actual}")
        lines = read_lines(fname)
        if len(lines) != meta["lines"]:
            fail(f"{fname}: line count {len(lines)} != manifest {meta['lines']}")
        if fname.endswith(".md"):
            if not lines or lines[0].rstrip() != meta["version_header"].rstrip():
                fail(f"{fname}: version header mismatch\n  expected '{meta['version_header']}'\n  actual   '{(lines[0] if lines else '')}'")
            nonblank = [l for l in lines if l.strip() != ""]
            if not nonblank or nonblank[-1] != meta["end_sentinel"]:
                fail(f"{fname}: END sentinel not last line -> possible truncation. "
                     f"Expected: '{meta['end_sentinel']}'")
        verified.append(fname)

    token = {"framework_version": fw_version, "files": verified,
             "project_unverified": unverified,
             "read_rule": "Read each .md IN FULL to its END-sentinel line; line counts are exact."}
    with open(".verified", "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)

    if unverified:
        print(f"[OK] FRAMEWORK {fw_version} PARTIALLY VERIFIED — "
              f"{len(verified)}/{len(files_meta)} files pass all checksum/version/whole-file "
              f"checks; {len(unverified)} spec(s) are PROJECT-UNVERIFIED and cannot be "
              f"checked against the manifest:")
        for fname in unverified:
            print(f"  [PROJECT-UNVERIFIED] {fname} — sourced from the project Files "
                  f"section. Integrity unknown; it may be stale or out of step with the "
                  f"repo engines. Disclose in the delivery footer (§2A).")
        print("This is NOT a failure and does NOT halt the run (SKILL rule 4, "
              "Framework_DeliveryFooter §2A).")
    else:
        print(f"[OK] FRAMEWORK {fw_version} VERIFIED — {len(verified)}/{len(files_meta)} files, "
              f"all checksums/versions/whole-file checks PASS")

    if args.trigger:
        entry = routes.get(args.trigger)
        if entry:
            specs = [f for f in entry if f.endswith(".md")]
            engines = [f for f in entry if f.endswith(".py")]
            # ── GAP-2026-08-16-STEP5-SESSION-EXHAUSTION / Fix A1 ─────────────────
            # DISCLOSE THE COST BEFORE IT IS PAID. SKILL Rule 2 is a hard, unbounded
            # obligation and nothing anywhere priced it: this line printed filenames
            # only, MANIFEST.json carried the line count for integrity and never
            # surfaced it as a cost, and no EC, DoD item or gate mentioned read cost
            # at all. Measured on the reference incident: 40 of session 1's 50 tool
            # calls and ~139,208 tokens went to satisfying Rule 2, and the step
            # stalled before its first productive operation.
            # This is a DISCLOSURE LINE, NOT A GATE — same precedent as
            # Framework_DeliveryFooter §2A. It never blocks a run.
            sec = {}
            if os.path.exists("SPEC_SECTIONS.json"):
                try:
                    sec = json.load(open("SPEC_SECTIONS.json", encoding="utf-8"))
                except Exception:
                    sec = {}
            sfiles = sec.get("files", {})
            klass = _session_class(args.progress, files_meta, trigger=args.trigger)
            print(f"\nEntry-point spec(s) for '{args.trigger}' — READ IN FULL "
                  f"(subject to SESSION CLASS below):")
            tot_l = tot_b = tot_v = tot_bash = 0
            for f in specs:
                meta, info = files_meta.get(f, {}), sfiles.get(f, {})
                ln = info.get("lines") or meta.get("lines") or 0
                by = info.get("bytes") or meta.get("bytes") or 0
                use_b = (info.get("reduced_bytes", by)
                         if klass == "NON-FINAL" and info.get("has_read_set") else by)
                vc = -(-by // 16000) if by else 0
                bc_ = max(1, -(-use_b // 150000)) if use_b else 0
                tot_l += ln; tot_b += use_b; tot_v += vc; tot_bash += bc_
                tag = ""
                if klass == "NON-FINAL" and info.get("has_read_set"):
                    tag = f"  [reduced from {by:,} B — {len(info.get('final_only_titles', []))} section(s) skipped]"
                print(f"  {f:<34} {ln:>6} lines  {use_b:>9,} B  ~{use_b // 4:>8,} tok"
                      f"  ~{bc_} bash call(s){tag}")
            print(f"  {'-' * 96}")
            print(f"  {'PRE-WORK READ BUDGET':<34} {tot_l:>6} lines  {tot_b:>9,} B  "
                  f"~{tot_b // 4:>8,} tok  ~{tot_bash} bash call(s)")
            print(f"  SESSION CLASS: {klass}")
            if (klass == "NON-FINAL" and not args.progress
                    and args.trigger not in ("MockExplain", "TestExplain",
                                             "MockCreate", "TestCreate",
                                             "MockBlueprint")):
                print("    FRESH CORPUS — the paper count is not knowable until PHASE A/A1b.")
                print("    Read the NON-FINAL set now and re-decide the class there (§S8-0b).")
                print("    If A1b shows papers_remaining <= BATCH_SIZE, escalate to a FULL read")
                print("    BEFORE run_synthesise(). Escalation is MANDATORY and ONE-WAY.")
            elif klass == "NON-FINAL":
                print("    Reduced read is permitted: this session cannot clear the corpus, so it")
                print("    never reaches synthesis, QV, the summary or the schema/xlsx writers.")
                print("    ESCALATION IS MANDATORY AND ONE-WAY — if this session turns out to be")
                print("    final, read the omitted sections BEFORE run_synthesise(). §S8-0b.")
            else:
                print("    FULL READ REQUIRED — no exception. This session may write section_rules.md.")
            print(f"    Read with `sed -n 'A,Bp' <file>` in bash, NOT with view: measured in this")
            print(f"    container, view truncates above ~16,000 chars INCLUDING ranged reads "
                  f"(~{tot_v} calls);")
            print(f"    bash returned 188,024 chars intact in one call (~{tot_bash} calls). "
                  f"Ranges: SPEC_SECTIONS.json.")
            if engines:
                print(f"Routed engine(s) for '{args.trigger}' — EXECUTE via `import` inside the "
                      f"spec's code blocks; do NOT read these into context: {engines}")
        else:
            print(f"[note] trigger '{args.trigger}' not in advisory routes; "
                  f"read the spec whose header matches your step. All files are verified & present.")
    print(".verified written. Read the needed spec(s) (.md) in full; engines (.py) are "
          "executed, not read.")

if __name__ == "__main__":
    main()
