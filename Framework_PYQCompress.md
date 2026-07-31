# Framework_PYQCompress v1.1.1 — Universal Document Size Remediation
# v1.1.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   9 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQCompress'. The current companion block, the
#   v1.1 entry, and all structural notes remain in-file. Body byte-untouched.
# [ExamCode] project | Layer 2 remediation | Exam-agnostic | Document-class-agnostic
#
# PURPOSE:
#   Bring an existing .docx under the Google Drive connector's download cap WITHOUT
#   losing a single figure, a single equation or a single character of text, so that
#   Steps 2b, 4 and 5 can fetch it automatically instead of asking the operator to
#   upload it by hand on every run.
#
# WHY THIS SPEC EXISTS:
#   The Drive connector refuses any download above blueprint_core.DRIVE_CAP. On
#   2026-07-24, 6 of 7 pending papers in a live corpus were above it. The pipeline had
#   no way to know until the download was attempted, which happened at batch 6 of a
#   clean-looking run.
#
#   That produced a two-layer response:
#     LAYER 1 — PREVENTION. Framework_PYQSort v1.12 S7-6 governs size at the moment a
#               Sorted file is written, so newly produced files are born fetchable.
#     LAYER 2 — REMEDIATION. THIS SPEC. Layer 1 cannot help a file that already exists
#               in Drive. Those files are compressed once, replaced in Drive, and then
#               behave normally for every future run of every step.
#   Without Layer 2 the upload lane is permanent: every Step 2b / 4 / 5 run for the rest
#   of that corpus's life needs manual uploads for the same papers.
#
# WHAT IT IS NOT:
#   Not a converter, not a reformatter, not a cleaner. It re-encodes IMAGE BYTES and
#   nothing else. Text, tables, OMML, styles, headers, footers, relationships and the
#   part count all come out identical, and that is asserted rather than assumed.
#
# PIPELINE POSITION:
#   PYQCompress sits OUTSIDE the 11-step pipeline. It consumes no pipeline state, writes
#   no progress file, and produces no artefact any step reads. It is a maintenance
#   operation on a file, callable at any time, in any order, on any document class:
#     Row file (Step 1 output) · Sorted file (Step 3 output) · Analysis doc ·
#     any other .docx that has become too large to fetch.
#
# INPUTS:
#   One or more .docx files UPLOADED TO CHAT.
#   Drive fetch is NOT used and cannot be: by definition these files are above the cap
#   the connector refuses, which is the entire reason this trigger exists. Attempting a
#   Drive fetch here would fail for exactly the reason the operator came.
#
# OUTPUT:
#   One compressed .docx per input, delivered via present_files with a BYTE-IDENTICAL
#   FILENAME (see §2 — this is load-bearing, not cosmetic).
#   EVERY attached file is compressed regardless of its size (v1.1). The only file not
#   delivered is one that came out no smaller than it went in — there is nothing to
#   replace in Drive, and delivering it invites a pointless " (1)" rename.
#
# TRIGGER FORMAT:
#   PYQCompress
#   Trigger matching is case-insensitive. No arguments, no flags, no ExamCode — the
#   operation is a property of the FILE, not of the exam. Attach the files and run it.
#
# MODULES (routed in routes.json):
#   blueprint_core.py  ENGINE    — SIZE_BUDGET, DRIVE_CAP, TIER_LADDER, transport_status
#   corpus_io.py       I/O SHELL — optimize_docx, assert_docx_parity, count_image_refs
#   Both are shared with Steps 1, 3, 4 and 5. This spec defines NO thresholds and NO
#   compression logic of its own — it is a thin operator-facing wrapper around the same
#   governor Step 3 uses, so a paper compressed here and a paper governed there come out
#   of the same code path. A second implementation would drift, and the drift would be
#   invisible until two copies of one paper disagreed.
#
# EXAM-AGNOSTIC GUARANTEE:
#   Zero hardcoded exam values, and zero document-class assumptions. The spec never
#   parses questions, never reads headings, never looks for a date label. It operates on
#   the OOXML package. The same run handles an SSC Row file and a GATE Analysis doc.
#
# VERSION HISTORY:
#   v1.1 — 2026-07-25 — SIZE GATE REMOVED. Every attached file is now compressed
#          regardless of size (corpus_io v1.0.3 `always=True`); previously anything at or
#          under SIZE_BUDGET was reported T0 and skipped. The operator selects what to
#          compress by selecting what to attach. SIZE_BUDGET is unchanged and still
#          governs the LADDER TARGET and the MARGINAL/BLOCKED verdicts — it is no longer
#          an eligibility test. New EC-C1b covers the file that cannot be improved:
#          corpus_io restores the original bytes and it is reported but not delivered,
#          which stops CHECK 5 from hard-stopping the run on an already-optimal document.
---

## §1 — SESSION START

### S1-1 — Trigger parsing

```
Trigger: PYQCompress
Trigger matching is case-insensitive.

No arguments. No ExamCode. No Drive link.
The operation depends only on the bytes of the attached file(s), so there is
nothing to parse and nothing to look up in project knowledge.

If a Drive link IS supplied, do not attempt to fetch it. Reply:
  "PYQCompress works on uploaded files only. A paper above the
   [DRIVE_CAP] byte cap cannot be downloaded from Drive — that is the
   problem this trigger exists to fix. Download it from Drive in your
   browser and attach it here."
(The cap value is read from blueprint_core.DRIVE_CAP, never typed as a literal.)
```

### S1-2 — Input inventory

```python
import os, glob, shutil
import blueprint_core as bc      # ENGINE  — thresholds and transport verdicts
import corpus_io                 # I/O SHELL — governor, parity, image accounting

UPLOAD_DIR = '/mnt/user-data/uploads'
WORK_DIR   = '/home/claude/compress'
OUT_DIR    = '/mnt/user-data/outputs'


def collect_inputs(upload_dir=UPLOAD_DIR):
    """Every .docx the operator attached, with its size and transport verdict.

    Word lock-files (~$name.docx) are skipped silently — they are an artefact of the
    file being open on the operator's machine, never a document to compress.

    NOTHING else is skipped silently. A non-.docx attachment is REPORTED, because an
    operator who attached the wrong file and is told nothing will conclude the run
    succeeded.
    """
    inputs, ignored = [], []
    for name in sorted(os.listdir(upload_dir)):
        path = os.path.join(upload_dir, name)
        if not os.path.isfile(path):
            continue
        if name.startswith('~$'):
            continue                              # Word lock-file
        if not name.lower().endswith('.docx'):
            ignored.append((name, 'not a .docx — PYQCompress re-encodes OOXML packages '
                                  'only; .doc, .pdf and images are not supported'))
            continue
        size = os.path.getsize(path)
        inputs.append({'name': name, 'path': path, 'bytes': size,
                       'status': bc.transport_status(size)})
    return inputs, ignored


def report_inventory(inputs, ignored):
    """State the transport verdict for every file BEFORE doing any work."""
    for name, reason in ignored:
        print(f"  IGNORED: {name} — {reason}")
    if not inputs:
        raise SystemExit(
            "HARD STOP: no .docx files attached.\n"
            "Attach the oversized document(s) to this chat and run PYQCompress again.")
    print(f"\n  {'FILE':<58} {'BYTES':>12}  VERDICT")
    for f in inputs:
        print(f"  {f['name'][:58]:<58} {f['bytes']:>12,}  {f['status']}")
    print(f"\n  budget {bc.SIZE_BUDGET:,} · cap {bc.DRIVE_CAP:,}")
    print(f"  (v1.1 — the budget is the ladder's TARGET, not an eligibility test: every")
    print(f"   attached file is compressed, including files already reported OK.)")
    print(f"  BLOCKED  = above the cap; cannot be fetched from Drive at all today")
    print(f"  MARGINAL = fetchable, but under 10% headroom — one re-save flips it")
    print(f"  OK       = comfortably fetchable; compression not required")
```

---

## §2 — THE FILENAME RULE (HARD — read this before anything else)

```
═══════════════════════════════════════════════════════════════════════
THE OUTPUT FILENAME MUST BE BYTE-IDENTICAL TO THE INPUT FILENAME.
No suffix. No "_compressed". No "(1)". No date stamp. Nothing.
═══════════════════════════════════════════════════════════════════════

WHY, CONCRETELY. Every enumeration in the pipeline derives a paper's identity from
its filename via blueprint_core.canonical_paper_key, which normalises case, strips a
trailing " (n)" and a leading "copy of ", and removes non-alphanumerics. It does NOT
strip an arbitrary suffix, and it cannot: "_compressed" is indistinguishable from a
legitimate part of a paper's name.

So a file delivered as

    EXAM_12-Sep-2025_Shift-1_Sorted_Q1-Q100_compressed.docx

has a DIFFERENT canonical identity from the original. If the operator uploads it to
Drive alongside the original — the natural thing to do when the name differs — then:

  * the duplicate HARD STOP does NOT fire, because the identities differ;
  * Step 4 counts BOTH files, so that paper's questions are counted twice;
  * Step 5 processes both, so that year is weighted twice in the frequency data;
  * §1-6's coverage gate sees an inflated available_years population.

None of that raises an error anywhere. A silent double count of one year is a worse
outcome than the transport problem being fixed, and it is caused entirely by a
filename. Hence: same name in, same name out, and the operator REPLACES rather than
adds.

WHAT THIS MEANS FOR THE OPERATOR — state it in the delivery message, every time:
  "Replace the file in Drive — do not upload alongside. The compressed file has the
   same name deliberately, so that Drive overwrites the original."

BROWSER " (1)" — when the operator downloads the compressed file while the original
is still in their Downloads folder, the browser appends " (1)". That is harmless HERE
(canonical_paper_key strips it) but it must not be carried into Drive. Say so.
```

---

## §3 — INPUT INTEGRITY (before any re-encode)

```python
def audit_input(path):
    """Prove the input is a sound package BEFORE touching it, and record what it holds.

    A file that is already broken must not be re-encoded: the governor would faithfully
    produce a smaller broken file, the parity assert would compare one damaged state
    against another, and the operator would conclude the tool corrupted their document.

    Returns the pre-state used by §5's independent survival gate.
    """
    refs, per_part, unresolved = corpus_io.count_image_refs(path)
    dangling = corpus_io.dangling_media_targets(path)

    if unresolved:
        raise SystemExit(
            f"HARD STOP: {os.path.basename(path)} references {len(unresolved)} image(s) "
            f"that no relationship resolves: {unresolved[:5]}\n"
            "The document is already damaged — compressing it would make that permanent "
            "and hide the cause. Repair it in the step that produced it, then re-run.")
    if dangling:
        raise SystemExit(
            f"HARD STOP: {os.path.basename(path)} has {len(dangling)} relationship(s) "
            f"pointing at a media part that is not in the package: {dangling[:5]}\n"
            "Word renders these as empty space. Repair before compressing.")

    extracted = corpus_io.extract_images(path, f'{WORK_DIR}/probe')
    vector = sorted(k for k, v in extracted.items() if v['kind'] == 'vector')
    unreadable = sorted(k for k, v in extracted.items() if v['kind'] == 'unreadable')

    if unreadable:
        print(f"    WARN: {len(unreadable)} media part(s) could not be opened as images "
              f"— {unreadable[:3]}. They are carried through UNCHANGED (the governor "
              f"never re-encodes what it cannot read) and will not shrink.")
    if vector:
        print(f"    note: {len(vector)} vector part(s) (EMF/WMF/SVG) — {vector[:3]}. "
              f"Vector data is already compact and is left as-is; a file that is mostly "
              f"vector will not shrink much, and that is correct rather than a failure.")

    return {'refs': refs, 'parts': len(per_part), 'media': len(extracted),
            'vector': len(vector), 'unreadable': len(unreadable)}
```

---

## §4 — THE GOVERNOR

```
DELEGATED ENTIRELY to corpus_io.optimize_docx, which walks
blueprint_core.TIER_LADDER and stops at the FIRST tier that meets the budget, so the
least invasive change that works is the one applied.

  T1  q88, no resize      — re-encode only; every pixel dimension preserved
  T2  q85, 300 DPI ceiling
  T3  q82, 240 DPI ceiling
  T4  q80, 200 DPI ceiling — THE FLOOR

On the measured production corpus every paper cleared at T1, meaning no image was
downscaled at all: 16,599,368 bytes → 1,259,169 bytes with pixel dimensions untouched.

GUARANTEES the governor makes, which §5 then verifies independently:
  * never grows a part — if a re-encode comes out larger, the ORIGINAL bytes are kept
  * never drops a part
  * never changes the part count
  * transparency survives (alpha-bearing images route to PNG, never JPEG)
  * line art routes to PNG — JPEG would ring on the thin strokes and subscripts that
    diagrams and chemical structures are made of

T4 IS THE FLOOR AND IS NOT NEGOTIABLE. Below q80 / 200 DPI at display size, figures
start losing the detail the whole pipeline exists to preserve. A file still over
budget at T4 is DELIVERED with a warning, never squeezed further and never rejected.
```

```python
def compress_one(path, name, pre):
    """Compress one document and prove nothing was lost. Returns a per-file report."""
    # v1.1 — NO SIZE GATE. Every attached file is compressed, whatever its size. The
    # operator decides what to compress by deciding what to attach; the spec does not
    # second-guess that with a threshold. `always=True` is what carries this into the
    # engine — see corpus_io v1.0.3 for why force_tier is NOT the right lever.
    #
    # The ladder still picks the least invasive tier by itself: a small file's T1 output
    # is under budget, so it returns at T1 with every pixel dimension preserved.
    dst = os.path.join(OUT_DIR, name)          # §2 — SAME NAME. Never a suffix.
    ok, report, log = corpus_io.optimize_docx(path, dst, budget=bc.SIZE_BUDGET,
                                              always=True)

    # allow_resample only for the tiers that downscale BY DESIGN. T1 re-encodes quality
    # only, so a pixel-dimension change there would mean something went wrong.
    corpus_io.assert_docx_parity(path, dst,
                                 allow_resample=report['tier'] not in ('T0', 'T1'))

    after = os.path.getsize(dst)
    if report.get('no_gain'):
        # Output was no smaller than the input, so corpus_io restored the original bytes.
        # Reported, NOT delivered: there is nothing to replace in Drive.
        return {'name': name, 'action': 'nogain', 'tier': report['tier'],
                'before': report['orig'], 'after': after, 'path': dst,
                'note': 'already optimal — nothing to gain, original retained'}
    return {'name': name, 'action': 'compressed', 'tier': report['tier'],
            'before': report['orig'], 'after': after,
            'ratio': after / float(report['orig']),
            'status': bc.transport_status(after),
            'floor_exceeded': not ok, 'log': log, 'pre': pre, 'path': dst}
```

---

## §5 — SURVIVAL GATE (independent of the governor's own assert)

```python
def assert_survived(rep):
    """Re-derive the image count from the OUTPUT package and compare it to the input.

    corpus_io.assert_docx_parity has already checked this, among 17 invariants. This
    check exists ANYWAY, and the duplication is deliberate: per the framework's
    anti-drift principle a caller asserts the property it depends on rather than
    trusting a module's self-report. If a future change to optimize_docx ever weakened
    its internal assert, this gate would still fire.

    It is also the same gate Step 3 runs (Framework_PYQSort S7-7 / CHECK 10), so a file
    that passes here passes there.
    """
    refs, _, unresolved = corpus_io.count_image_refs(rep['path'])
    if unresolved:
        raise SystemExit(
            f"HARD STOP — {rep['name']}: the compressed file has {len(unresolved)} "
            f"unresolved image reference(s). Do not deliver it.")
    if refs != rep['pre']['refs']:
        raise SystemExit(
            f"HARD STOP — IMAGE SURVIVAL, {rep['name']}:\n"
            f"  input  {rep['pre']['refs']} image reference(s)\n"
            f"  output {refs}\n"
            "The governor lost a figure. This should be unreachable — "
            "assert_docx_parity would have failed first — so treat a failure here as a "
            "defect in corpus_io, not in the document. Do not deliver the file.")
    dangling = corpus_io.dangling_media_targets(rep['path'])
    if dangling:
        raise SystemExit(
            f"HARD STOP — {rep['name']}: compressed output has dangling relationship(s): "
            f"{dangling[:5]}")
    return refs
```

---

## §6 — VERDICT AND REPORTING

```python
def report_results(reports):
    """One line per file, then the operator's next action. Never silent about a miss."""
    print(f"\n  {'FILE':<44} {'BEFORE':>12} {'AFTER':>12}  TIER  VERDICT")
    for r in reports:
        if r['action'] == 'nogain':
            print(f"  {r['name'][:44]:<44} {r['before']:>12,} {'—':>12}  "
                  f"{r['tier']:<5} no gain — already optimal, not delivered")
            continue
        print(f"  {r['name'][:44]:<44} {r['before']:>12,} {r['after']:>12,}  "
              f"{r['tier']:<5} {r['status']}")

    stuck = [r for r in reports if r.get('floor_exceeded')]
    for r in stuck:
        print(f"\n  ⚠️  WARN: {r['name']} is {r['after']:,} bytes after tier "
              f"{r['tier']} — still above the {bc.SIZE_BUDGET:,}-byte budget.")
        if r['status'] == 'BLOCKED':
            print(f"      It remains above the {bc.DRIVE_CAP:,}-byte cap, so Steps 2b/4/5 "
                  f"will still request it by chat upload. DELIVERED ANYWAY — the file is "
                  f"valid and complete; it is only awkward to transport.")
            print(f"      The ladder floor (q80 / 200 DPI at display size) was reached. "
                  f"Going lower would damage the figures. If this paper must become "
                  f"fetchable, the remaining options are structural, not compressive: "
                  f"split it into two documents, or accept the upload lane for it.")
        else:
            print(f"      It is under the cap, so Drive fetch still works — only the "
                  f"10% safety margin is gone.")

    done = [r for r in reports if r['action'] == 'compressed']
    if done:
        print(f"\n  NEXT: replace these file(s) in the Drive PYQ folder — REPLACE, do not "
              f"upload alongside. The names are unchanged deliberately so Drive "
              f"overwrites the original (§2). A second copy under a different name is "
              f"counted as a second paper by every step in the pipeline.")
        print(f"        If your browser adds ' (1)' on download, rename it back before "
              f"uploading to Drive.")
```

---

## §7 — VALIDATION (5 checks — every one must PASS before delivery)

```
CHECK 1 — PACKAGE VALIDITY
  The output opens as a valid OOXML package: zipfile.testzip() clean, every .xml and
  .rels part well-formed, python-docx opens it. Enforced inside
  corpus_io.docx_invariants, which assert_docx_parity calls on both files.

CHECK 2 — CONTENT FIDELITY (17 invariants)
  corpus_io.assert_docx_parity: part count, media count, paragraph count, table count,
  inline shape count, character count, table-cell character count, OMML count, drawing
  count, w:pict count, hyperlink count, the SHA256 of the extracted text, image
  reference count, malformed-XML count, zip integrity, dangling relationships, and
  per-image pixel dimensions.
  Byte size and "it opens in Word" are NOT evidence of correctness: a governor that
  quietly dropped a figure produces a smaller file that opens perfectly.

CHECK 3 — IMAGE SURVIVAL (independent)
  §5 assert_survived: image references re-derived from the output package equal the
  input's. Same gate as Framework_PYQSort S7-7 / CHECK 10.

CHECK 4 — FILENAME IDENTITY
  os.path.basename(output) == os.path.basename(input), exactly, byte for byte.
  A mismatch is a HARD STOP — see §2 for why this is a correctness property and not a
  cosmetic one.

CHECK 5 — NO GROWTH
  after <= before for every delivered file. Guaranteed twice over: _recode keeps the
  original bytes for any PART that would grow, and (v1.1) _no_gain_guard restores the
  original DOCUMENT whenever the container itself would grow. This check is therefore a
  backstop that should now be unreachable; if it fires, the defect is in corpus_io.
  HARD STOP.
```

```python
def validate_output(rep):
    """CHECK 3, 4 and 5 as executable assertions. 1 and 2 are inside the parity assert."""
    assert_survived(rep)                                              # CHECK 3
    if os.path.basename(rep['path']) != rep['name']:                  # CHECK 4
        raise SystemExit(
            f"HARD STOP — FILENAME IDENTITY: delivered as "
            f"{os.path.basename(rep['path'])!r} but the input was {rep['name']!r}. "
            "A renamed copy is a SECOND PAPER to every enumeration in the pipeline "
            "(§2). Fix the output path; never deliver under a changed name.")
    if rep['after'] > rep['before']:                                  # CHECK 5
        raise SystemExit(
            f"HARD STOP — {rep['name']} grew from {rep['before']:,} to "
            f"{rep['after']:,} bytes. The governor keeps original bytes when a "
            "re-encode would be larger, so this indicates a defect in corpus_io.")
```

---

## §8 — EXECUTION MODEL

```
SINGLE SCRIPT, 3 TOOL CALLS:

  CALL 1 — create_file: write compress_pipeline.py containing
    1. collect_inputs + report_inventory  (§1)
    2. audit_input                        (§3)
    3. compress_one                       (§4)
    4. assert_survived + validate_output  (§5, §7)
    5. report_results                     (§6)

  CALL 2 — bash_tool: run it
    → inventory table, per-file compression, all 5 checks, results table

  CALL 3 — present_files: deliver every COMPRESSED file

DELIVERABLE SET CONTRACT (CLOSED):
  present_files MUST contain EXACTLY the compressed outputs — one file per input that
  needed compressing — and NOTHING ELSE.

  DO NOT include:
    ✗ compress_pipeline.py
    ✗ files that came out no smaller than they went in (corpus_io restored the
      original bytes; delivering them invites a pointless Drive replace and a
      needless " (1)" rename)
    ✗ extracted images or any probe artefact from /home/claude/compress
    ✗ the uploaded originals

  If NO input came out smaller, deliver NOTHING and say so plainly:
    "All N file(s) are already optimally encoded — nothing to gain."
  An empty delivery is the correct outcome there, not a failure.

CHAT FILE LIMIT: the platform accepts bc.CHAT_FILE_LIMIT files per conversation, so at
most that many documents can be remediated per chat. With more, run PYQCompress in
successive chats — there is no state to carry, so the split costs nothing.

POST-DELIVERY FOOTER (MANDATORY after present_files):
  Render the standardised visual delivery footer as the LAST element in the response.
  Follow Framework_DeliveryFooter.md — footer type F2 (step-complete; PYQCompress has
  no batches), file badge "Use locally", next step: replace the file(s) in Drive.
```

---

## §9 — EDGE CASES

```
EC-C1: FILE ALREADY UNDER BUDGET
  v1.1 — COMPRESSED ANYWAY. Size is no longer an eligibility test: the operator selects
  what to compress by selecting what to attach, and the spec does not override that.
  Such a file clears at T1, so no image is downscaled and every pixel dimension is
  preserved; the saving comes from CMYK->RGB normalisation, not from resolution loss.
  Note the trade this makes: a re-encode is not free, and on an already-JPEG figure it
  costs one generation. That cost is the operator's to accept, and it is why the
  pre-v1.1 default was to skip these files.

EC-C1b: FILE THAT CANNOT BE IMPROVED
  Output no smaller than input. corpus_io._no_gain_guard restores the original bytes,
  and the file is REPORTED but NOT delivered — there is nothing to replace in Drive.
  Without that guard CHECK 5 (no growth) would treat it as a HARD STOP and abort the
  run, which is the wrong answer for a document that is simply already optimal.

EC-C2: LADDER FLOOR REACHED, STILL OVER CAP
  Delivered with a WARN naming the remaining options, which are structural rather than
  compressive: split the document, or accept the upload lane for that paper. Never a
  hard stop — the file is valid and complete.

EC-C3: MOSTLY-VECTOR DOCUMENT
  EMF/WMF/SVG parts are already compact and are not raster-encodable. Reported at §3,
  carried through unchanged. A file that barely shrinks for this reason has a stated
  cause rather than an unexplained result.

EC-C4: UNREADABLE MEDIA PART
  A media part that will not open as an image is carried through byte-for-byte — the
  governor never re-encodes what it cannot read. Reported, never silently dropped.

EC-C5: TRANSPARENCY
  Alpha-bearing images route to PNG and never to JPEG, which cannot hold an alpha
  channel. Delegated to blueprint_core.classify_media_route; not decided here.

EC-C6: LINE ART / DIAGRAMS
  Few-colour images (diagrams, chemical structures, plots) route to PNG. JPEG would
  ring on exactly the thin dark strokes and subscripts these figures consist of.

EC-C7: ALREADY-JPEG SOURCE
  Re-encoding a JPEG as PNG BLOATS it — the source is already lossy, so PNG stores the
  compression artefacts losslessly. Source format therefore wins over the line-art test
  for JPEG input. Delegated to classify_media_route.

EC-C8: RE-ENCODE COMES OUT LARGER
  The original bytes are kept for that part. A part is never grown. CHECK 5 asserts the
  same property for the document as a whole.

EC-C9: DAMAGED INPUT (unresolved rId or dangling media)
  HARD STOP at §3, BEFORE any re-encode. Compressing a damaged file would make the
  damage permanent and would leave the operator believing the tool caused it.

EC-C10: NON-.docx ATTACHMENT
  Reported as IGNORED with a reason. Never silently skipped: an operator who attached
  a .doc or a PDF and is told nothing will conclude the run succeeded.

EC-C11: WORD LOCK-FILE (~$name.docx)
  Skipped silently. It is an artefact of the document being open on the operator's
  machine, never a document to compress. This is the ONLY silent skip in the spec.

EC-C12: BROWSER APPENDS " (1)" ON DOWNLOAD
  Harmless here — canonical_paper_key strips it — but it MUST NOT reach Drive. The
  delivery message says so explicitly (§2, §6).

EC-C13: MORE FILES THAN THE CHAT LIMIT
  At most bc.CHAT_FILE_LIMIT documents per chat. Run PYQCompress again in a new chat
  for the remainder; there is no state to carry.

EC-C14: SAME PAPER ATTACHED TWICE UNDER DIFFERENT NAMES
  Both are compressed — this spec deliberately does not judge paper identity, because
  it is document-class-agnostic and has no taxonomy to judge against. The DUPLICATE
  gate lives at enumeration (corpus_io.collect_corpus_files) where identity is
  meaningful. What §2 prevents is this spec CREATING such a pair.

EC-C15: OPERATOR SUPPLIES A DRIVE LINK INSTEAD OF FILES
  Do not attempt a fetch: the file is above the cap by definition, which is why the
  operator is here. Reply with the S1-1 message asking for an upload.
```

---

## §10 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL (identical for every exam AND every document class):
  Trigger parsing · input inventory · transport verdicts · input integrity audit ·
  the tier ladder · parity assertion · image survival gate · filename rule ·
  all 5 validation checks · all 15 edge cases · 3-call execution model

READ FROM THE ENGINE, NEVER RESTATED HERE:
  blueprint_core.SIZE_BUDGET · DRIVE_CAP · CHAT_FILE_LIMIT · TIER_LADDER ·
  transport_status() · classify_media_route()

NOT USED AT ALL:
  exam_config.json · taxonomy · Analysis docs · blueprint.json · registry.json ·
  any progress file · any Drive call
  PYQCompress reads no project state and writes none. It cannot corrupt pipeline state
  because it never touches it.

PROOF OF DOCUMENT-CLASS INDEPENDENCE:
  The spec never parses a question, a heading, an option or a date label. It operates on
  the OOXML package. A Row file, a Sorted file, an Analysis doc and an unrelated Word
  document all take the identical path.
```

---

## §11 — DEFINITION OF DONE

```
☐ 1.  Inputs collected; every non-.docx attachment reported with a reason
☐ 2.  Transport verdict (OK / MARGINAL / BLOCKED) printed for every input BEFORE work
☐ 3.  Input integrity audited — unresolved rIds and dangling media are HARD STOPs
☐ 4.  Vector and unreadable parts reported, so a small saving has a stated cause
☐ 5.  Governor run via corpus_io.optimize_docx — no thresholds defined in this spec
☐ 6.  CHECK 1 package validity PASSED
☐ 7.  CHECK 2 content fidelity PASSED (17 invariants, allow_resample only for T2-T4)
☐ 8.  CHECK 3 image survival PASSED — independently re-derived, not taken on trust
☐ 9.  CHECK 4 filename identity PASSED — output name byte-identical to input name
☐ 10. CHECK 5 no growth PASSED
☐ 11. Every attached file compressed regardless of size; files that gained nothing
      reported and NOT delivered
☐ 12. Floor-exceeded files DELIVERED with a WARN naming the structural options
☐ 13. Results table printed: before, after, tier, verdict
☐ 14. Delivery message states REPLACE-do-not-add and the " (1)" rename warning
☐ 15. Deliverable set closed: exactly the compressed files, nothing else
☐ 16. Delivery footer rendered per Framework_DeliveryFooter.md (F2)

POST-DELIVERY:
  Operator replaces the file(s) in the Drive PYQ folder.
  Steps 2b, 4 and 5 then fetch them automatically on every future run — the upload
  lane is no longer needed for those papers.
```

---

## §12 — CRITICAL WARNINGS

```
⚠️ NEVER change the output filename
   A renamed copy is a SECOND PAPER to every enumeration in the pipeline. Uploaded
   alongside the original it produces a silent double count of that paper's year, which
   no gate anywhere catches — the canonical-identity HARD STOP cannot fire, because the
   identities genuinely differ. This is the single most damaging mistake available in
   this spec, and it looks like good hygiene.

⚠️ NEVER define a threshold or a tier in this spec
   SIZE_BUDGET, DRIVE_CAP, CHAT_FILE_LIMIT and TIER_LADDER live in blueprint_core and
   are shared with Steps 1, 3, 4 and 5. A local copy drifts, and the drift is invisible
   until a paper compressed here fails the governor there.

⚠️ NEVER re-implement compression here
   corpus_io.optimize_docx is the one implementation. A spec-local variant would
   produce files that differ from Step 3's output for the same input.

⚠️ NEVER deliver without assert_docx_parity
   A governor that dropped a figure produces a smaller file that opens cleanly in Word
   and reads normally, because the question stem is text. Size is not evidence.

⚠️ NEVER compress a damaged input
   Unresolved rIds and dangling media are HARD STOPs at §3. Re-encoding damage makes it
   permanent and misattributes the cause to this tool.

⚠️ NEVER go below the T4 floor
   q80 / 200 DPI at display size is where figures begin losing the detail the pipeline
   exists to preserve. A file still over budget at T4 is delivered with a warning; it is
   never squeezed further and never rejected.

⚠️ NEVER attempt a Drive fetch from this trigger
   The file is above the cap by definition. The fetch would fail for exactly the reason
   the operator ran PYQCompress.
```

---

# END OF Framework_PYQCompress v1.1.1
