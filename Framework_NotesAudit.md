# Framework_NotesAudit v3.0.0 — Notes Pipeline Step NA (Closed-Book Audit + Remediation)
# v3.0.0 — 2026-08-12 — NA BECOMES A WRITER (BREAKING; GAP-2026-08-12-NADOCX
#   patch P2 of 2; owner decisions of the 2026-08-12 design session).
#   Through v2.0.6 NA was a read-only certifier: it produced verdicts and
#   routed every defect BACK to NC (§4 L-2), and §7 stated the audited file was
#   "the SAME file ND ships — delivery never edits content". NA now VERIFIES,
#   CORRECTS, IMPROVES and EMITS the student-facing document itself. The seven
#   changes that follow, and why each one is load-bearing:
#     (1) INPUT BY ATTACHMENT (§0A). The unit .docx arrives attached to the
#         trigger message, never from Project Files. The bank, blueprint and
#         registry stay in Project Files. Attachment removes the implicit
#         guarantee that the file audited is the file NC produced, so §0B adds
#         three HARD-STOP preflights — filename identity, exam-code
#         cross-check, and sha256 against the registry's draft_ref.
#     (2) REBUILD, NEVER PATCH XML (§2A). NA parses the draft to a
#         notes_docx content model, edits the MODEL, and rebuilds through the
#         SHARED builder. notes_docx.py exists because construction was prose
#         until 2026-08-12: a writing NA hand-rolling paragraphs would have
#         been a second implementation of the §6A colour map, the cascade, box
#         styling, spacers, F-7 and the OMML conventions — the exact "one
#         contract, two implementations" class the 2026-08-10 sweep closed.
#     (3) KEY CORRECTION (§3A), superseding v2.0.0 owner decision 4a for the
#         correction path. Where the notes-derived answer disagrees with the
#         stored key, NA teaches the CORRECT method and answer instead of
#         bending the notes to a wrong key. Two tiers: a bank that contradicts
#         ITSELF is corrected silently; a bank that is internally consistent
#         is still corrected but the correction is DISCLOSED in the chat.
#         Without the tier split every disagreement would resolve in NA's
#         favour and the ground-truth check would be decorative.
#     (4) FOURTH VERDICT SOLVABLE_KEY_CORRECTED, counting toward the pass, so
#         a corrected unit certifies without weakening the vacuous-pass floor.
#     (5) NO .md REPORT (§6). The evidence moves into notes_registry.json as
#         audit_summary. The report OBJECT stays: pass_for_unit operates on it
#         and IS the vacuous-pass floor, so dropping the object would delete
#         the certification rather than just the file.
#     (6) NEW GATES (§5): G-7a visual layout (DORMANT without a renderer),
#         G-7b OMML/figure line-rule geometry, G-8 answer integrity, G-9
#         orphan terms, G-10 counter integrity, and G-11 the TERMINAL RE-GATE
#         that certifies the BYTES THAT SHIP rather than the pre-patch draft.
#     (7) ALWAYS DELIVER (§4/§9). NA emits exactly one file, always named by
#         notes_core.notes_final_filename, in every outcome. A question that
#         survives the loop is QUARANTINED, not shipped as a warning: nothing
#         inside the document ever marks a defect (F-6/§7 unchanged).
#   Companions: notes_core >= v2.4, notes_docx >= v1.1, notes_audit >= v2.0.
# v2.0.6 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §7's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename".
# v2.0.5 — 2026-08-10 — TAXONOMY SYNC (registry keyed by the Step-5 sid).
# v2.0.4 — 2026-08-10 — CROSS-CHAT HANDOFF + STALE-REF FIX.
# v2.0.3 — 2026-08-10 — POST-DEPLOY REVIEW (bank join recomputed from stored
#   fields).
# v2.0.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 2 (vacuous-pass floor wired).
# v2.0.0 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES.
# v1.1.0 — 2026-08-08 — REFINEMENT GATES (G-4, G-5, G-6).
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
# [ExamCode] project | Notes Step NA | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py  >= v2.4 — notes_final_filename, docx_ref_for/verify_docx_ref,
#                            registry schema notes-registry/2.1 (draft_ref,
#                            final_ref, audit_summary), resolve_unit, the
#                            density/math/prose gates, bank_questions_for
#   notes_docx.py  >= v1.1 — the SHARED builder/parser: build/parse/
#                            validate_model/outline_of. Derived numbering and
#                            the byte-identical round trip are its guarantees
#   notes_audit.py >= v2.1 — SOLVABLE_KEY_CORRECTED, classify_key_conflict,
#                            record_key_correction, quarantine, gate_line_rules,
#                            gate_answer_integrity, gate_counters,
#                            gate_orphan_terms, gate_anatomy,
#                            gate_question_format, gate_outline,
#                            terminal_regate, audit_summary
#
# PURPOSE:
#   Guarantee that the delivered document teaches every in-syllabus PYQ of one
#   subtopic well enough to solve it from the notes alone — and, where it does
#   not, MAKE it do so. NA is the ONLY quality gate in the Notes pipeline; no
#   human review exists anywhere in it.
#
# PIPELINE POSITION:
#   Notes Step NB (NotesBlueprint) -> notes_pyq_bank.json (the PYQ bank)
#   Notes Step NC (NotesCreate)    -> the unit's draft .docx + draft_ref
#   Notes Step NA (NotesAudit)     -> THIS SPEC -> the unit's _Final.docx
#   Notes Step ND (NotesDeliver)   -> portal formatting + delivery
#
# PREREQUISITE:
#   Unit state DRAFTED. The draft .docx is ATTACHED TO THE TRIGGER MESSAGE.
#   notes_pyq_bank.json, notes_blueprint.json and notes_registry.json are in
#   Project Files.

## §0 — TRIGGER AND UNIT RESOLUTION
The trigger is:

    NotesAudit <Subject :: Topic :: Sub Topic Name>

with the unit's draft .docx ATTACHED to the same message. The unit reference is
whatever cell the operator copied from [ExamCode]_taxonomy.xlsx, resolved by
notes_core.resolve_unit exactly as in Framework_NotesCreate section 0 — all
three tiers remain accepted (Sub Topic Id, the Subject::Topic::Sub Topic Name
scope above as the CANONICAL form, or the bare Sub Topic Name). A unique hit
proceeds; multiple bare-name hits STOP and list every candidate with its
Subject + Topic; zero hits STOP with nearest-name suggestions. NA never
fuzzy-picks. The resolved unit is confirmed in chat as
<Sub Topic Name> (<sid>).

## §0A — INPUTS
  ATTACHED to the trigger : the unit's draft .docx (NC's F-1 filename).
                            EXACTLY ONE .docx. Zero attachments STOPS; more
                            than one STOPS and lists them — NA never picks.
  PROJECT FILES           : notes_pyq_bank.json, notes_blueprint.json,
                            notes_registry.json, and (when present)
                            [ExamCode]_subtopic_manifest.json.
The attachment is READ-ONLY on disk. NA copies it to a working directory
before doing anything else; it never edits the uploaded file in place, and it
writes its output to the outputs directory.

## §0B — PREFLIGHT (three HARD STOPS, run before any solving)
Until v3.0.0 NA read its input from Project Files, where NC had put it. An
attachment carries no such chain, so the chain is CHECKED. Each stop names a
different defect with a different remedy, so they are reported separately —
notes_core.verify_docx_ref returns the kind.

  P-1 FILENAME IDENTITY. Recompute the unit's draft filename with
      notes_core.notes_filename(...) from the RESOLVED unit's persisted
      unit_code digits and sid_slug. If the attached file's name differs, STOP:
      "the wrong unit's document is attached". This is the likeliest operator
      error — triggering ST06 while attaching ST07 — and it is the one error
      that would otherwise produce a perfectly clean audit of the wrong notes.
  P-2 EXAM-CODE CROSS-CHECK. The trigger's scope form carries NO exam code, so
      the {EXAM} prefix of the attached filename is the only place it appears.
      It MUST equal the registry's exam_code. A mismatch STOPS.
  P-3 BYTE IDENTITY. Compare notes_core.file_sha256 of the attachment against
      the registry unit's draft_ref (written by NC, Framework_NotesCreate
      section 9A). A mismatch means the file was modified after NC wrote it; a
      missing draft_ref means the draft predates NotesCreate v2.3.0. Both
      STOP. An operator who deliberately hand-edited the draft re-issues the
      trigger with the token --accept-modified, which downgrades P-3 to a
      warning recorded in audit_summary; P-1 and P-2 are NEVER overridable.

  The v2.0.x staleness stops are unchanged and still run: verify_bank_ref
  against the blueprint's bank_ref, and verify_taxonomy_ref against
  [ExamCode]_subtopic_manifest.json when present. Either mismatch routes the
  unit back to NB.

## §1 — FIGURES (read from the bank; no re-extraction)
Unchanged from v2.0.0 for the SOLVE. NB extracted every image and split stem
figures from solution figures at the "Correct Answer:" line, so NA reads
solve-critical images with notes_audit.figures_for (stem figures only —
solution figures are part of the key, not the prompt) and views them with the
stem. A stem figure recorded "UNRESOLVED:..." parks that question in
report['figure_pending']; it never hard-stops the run.

NEW in v3.0.0: NA MAY RE-RENDER a figure it judges improvable, via
figural_core, subject to three conditions that keep section 8's idempotence
real:
  (a) the render must be DETERMINISTIC (fixed rcParams and DPI, no timestamp
      in the image metadata) — identical inputs must produce identical bytes;
  (b) each re-rendered figure's hash is recorded in audit_summary, and a
      figure already re-rendered by NA is NEVER re-judged on a later run;
  (c) every re-render re-passes F-4 (label drawn INSIDE the image, mathtext
      structural scripts, no exam or question-type vocabulary) and G-7a/G-7b.
notes_docx writes positional picture names, so a re-render to a different
temporary path does not churn document.xml.

## §2 — CLOSED-BOOK SOLVE PROTOCOL (ground-truth)
For each bank question, in order:
  P-1 Extract the tested concept(s).
  P-2 PRESENCE: locate where the notes teach each concept (block reference).
  P-3 SOLVE using ONLY the notes text plus the section 1 stem figures — no
      outside knowledge beyond the Level-assumed prerequisites declared in the
      blueprint.
  P-4 MATCH against the bank's verbatim correct_answer via
      notes_audit.verdict_against_key: MCQ option token; MSQ unordered set;
      NAT equal after rounding BOTH sides to the stem's stated precision.
  P-5 VERDICT: SOLVABLE | SOLVABLE_KEY_CORRECTED (section 3A) | PARTIAL (the
      notes teach the concept but the notes-derived answer misses the key) |
      NOT (the notes do not teach the concept). The notes location and the
      produced answer are recorded (notes_audit.record).

COVERAGE + PASS: NA audits EVERY one of the unit's bank questions —
unit_questions = notes_core.bank_questions_for(bank, subject, topic, subtopic)
— and certifies ONLY through notes_audit.pass_for_unit(report,
unit_questions), which derives expected_count from the bank. A run that
recorded fewer verdicts than the unit has questions can never certify.
A QUARANTINED question (section 4 L-4) is excluded from the solvable set but
STILL COUNTED in the denominator, so quarantining can never manufacture a pass
by shrinking what must be solved.

## §2A — WRITE AUTHORITY (rebuild, never XML surgery)
NA's edit cycle is exactly:
    model = notes_docx.parse(draft_path)
    ...correct and improve the MODEL...
    notes_docx.build(model, final_path)
NA NEVER edits .docx XML and NEVER hand-rolls a paragraph, colour, border or
line rule. Three properties follow from the shared builder and are the reason
this is safe:
  W-1 NUMBERS ARE DERIVED, NEVER STORED. Every n.k, n.k.m, "Example j" and
      "Recall j" is computed from block ORDER at render time
      (notes_docx.outline_of). Section 6A's renumber rule therefore cannot be
      violated by inserting or dropping a block — there is no stored number to
      go stale. outline_of is also G-10's oracle.
  W-2 UNTOUCHED MATHS IS NEVER RE-AUTHORED. parse preserves each oMath element
      verbatim; build re-inserts it. NA re-compiles only an equation it
      actually changed.
  W-3 THE REBUILD IS A FIXED POINT. build -> parse -> build reproduces
      word/document.xml byte-for-byte (notes_docx self-test), which is what
      makes section 8's idempotence rule checkable rather than asserted.

SCOPE OF THE WRITE:
  ALLOWED — defect remediation (anything a verdict or a gate identifies), and
    bounded improvement: tightening a bullet over the D-1 cap, converting >= 3
    parallel facts into a table (D-3), adding a clarifying bullet or KEY
    POINTS line, adding a genuine SPEED HACK, improving figure clarity,
    sharpening wording.
  FORBIDDEN — adding or removing Examples or Recall items (it moves the global
    j sequence and voids G-5's type-coverage proof); changing any Answer
    except through section 3A; and introducing any fact that is not
    syllabus-required, PYQ-anchored or BRIDGE-justified (D-6). Without that
    last guard "improvement" is an open door for off-syllabus content in a
    student document.
  Every improvement is logged (notes_audit.log_improvement) so section 8 is
  testable.

## §3 — PYQ PROTECTION (paraphrase rule)
Unchanged. Examples are PYQ-ANCHORED but PARAPHRASED: fresh numbers, fresh
wording. Anchors (exam-date + Q number) live in the bank and the audit_summary
ONLY — never in the document (section 7). Actual PYQ text is never reproduced.
This survives the loss of the .md report because the bank still holds the
anchors.

## §3A — KEY CORRECTION (supersedes v2.0.0 owner decision 4a)
A stored key is no longer beyond appeal. Where NA's notes-derived answer
disagrees with the bank's correct_answer, NA CORRECTS the key and teaches the
correct method — it never bends the notes to fit a wrong key, because that
would mean deliberately teaching a student the wrong method so the document
agrees with a defect.

Two tiers, classified by notes_audit.classify_key_conflict on ONE question:
does the bank's VERBATIM explanation itself arrive at NA's answer?
  TIER 1 — BANK_SELF_CONTRADICTS (yes). The bank disagrees with ITSELF: its
    explanation concludes X while its correct_answer field says Y. That is a
    Step-5 extraction defect with evidence from inside the bank, so the
    correction is applied SILENTLY.
  TIER 2 — JUDGEMENT (no). The bank is internally consistent and NA still
    disagrees — NA against the examiner AND the official explanation. The
    correction is still applied, but it is DISCLOSED: named in the chat
    delivery line and recorded in audit_summary with the stored answer, NA's
    answer and the reasoning.
There is NO CAP on corrections (owner decision). NA reports the COUNT in the
chat line, because an unusual number of corrections in one unit is far more
likely to mean the wrong paper or wrong subtopic was bound upstream at Step 5
than that the examiner erred that often. The count informs; it never blocks.

THE BANK IS NEVER WRITTEN. notes_pyq_bank.json is NB's artifact and the
blueprint holds bank_ref, a sha256 over its bytes; editing it would fail
verify_bank_ref for EVERY unit in the exam on the next run and force a full NB
re-run to recover. Corrections live in the report and the registry — which is
also the form to feed back into a Step-5 fix.

Both tiers record the verdict SOLVABLE_KEY_CORRECTED, which counts toward the
pass.

## §4 — CONVERGENCE LOOP (self-contained; always ends in a delivered file)
  L-1 Any PARTIAL/NOT verdict produces a targeted correction to the MODEL
      (section 2A); the affected questions re-audit; the notes minor version
      bumps.
  L-2 After MAX_PATCHES_PER_QUESTION (3) failed corrections on the same
      question: FULL REGENERATION of the unit's model by NA itself. v3.0.0
      does not route back to NC.
  L-3 After MAX_REGENERATIONS (3) without convergence: STOP LOOPING on that
      question. With section 3A in force this is no longer "the notes are
      badly written" — NA can always teach the correct method and the correct
      answer — so a question that still cannot be made solvable from
      in-syllabus notes indicates the question does not belong to this
      subtopic or its stem is corrupt.
  L-4 QUARANTINE that question (notes_audit.quarantine) with the reason. The
      unit certifies on the remaining set (section 2 COVERAGE). The quarantine
      list is named in the chat and stored in audit_summary; it is what to
      check against Step 5, and a bank refresh re-audits it under the section
      3 standing trigger. NOTHING about a quarantined question appears in the
      document.
  L-5 Every correction is logged in the report (patch_log).

## §5 — MACHINE GATES
  G-1 DENSITY (notes_core.density_gate): bullet word counts, table-first
      violations, page count within the tier band. The bullet count covers
      EVERY rendered bullet — concept bullets and the bullets inside KEY
      POINTS and TRAP boxes alike (notes_core v2.4; before it, the counter
      recognised only Word list paragraphs and the shared builder emits a
      literal glyph, so the D-1 check saw nothing at all). D-1 is also
      enforced at CONSTRUCTION by notes_docx.validate_model, so the two layers
      agree rather than one silently covering for the other.
  G-2 MATH — three separately reported gates, all reporting ZERO findings.
      They are named G-2a / G-2b / G-2c here because those are the exact keys
      terminal_regate writes into the report and audit_summary; "G-2" alone is
      the umbrella, never a report key.
      G-2a OMML presence by XML assertion (notes_core.assert_omml). NEVER
          verify equations through a LibreOffice-rendered preview: LibreOffice
          drops OMML SILENTLY (verified 2026-08-08 with a minimal fixture).
      G-2b STRUCTURAL-OMML SCAN (notes_core.scan_omml_structural): no textual
          exponent, no unicode super/subscript character inside any oMath
          region.
      G-2c FLAT-TOKEN SCAN (notes_core.scan_flat_math_tokens): no un-styled
          math token in any plain text run.
  G-3 ANATOMY (notes_audit.gate_anatomy): required blocks for the unit's tier
      present and in section 6A order; adjacent boxes separated by spacers.
      notes_docx.validate_model owns the contract and enforces it at
      CONSTRUCTION, so this gate re-asserts it on the model that produced the
      SHIPPED file — which matters because NA edits that model after NC built
      it.
  G-4 CONTENT-STYLE BAN SCAN (notes_core.scan_prose_bans), honouring per-unit
      exemptions declared in the blueprint.
  G-5 QUESTION-FORMAT (notes_audit.gate_question_format): every Example and
      Recall matches the fixed template, its type is a member of the
      blueprint's allowed_question_types, and a Recall carries neither an
      Explanation nor a SPEED HACK. The gate reports which allowed types went
      unused across the unit so type coverage is visible rather than assumed.
  G-6 OUTLINE-NUMBER INTEGRITY (notes_audit.gate_outline): numbering gapless
      and sequential, and every in-text cross-reference ("see n.k") resolving
      to a number that exists. notes_docx.outline_of is the oracle. Because
      numbers are DERIVED from block order, a stale cross-reference is the only
      way this can break — and it is exactly what NA's editing can introduce
      silently, since removing a block renumbers everything after it.
  G-7a VISUAL LAYOUT (notes_audit.preflight -> renderer). Render and inspect
      every page for tables past the margin, boxes split mid-Answer,
      illegible figures, orphan headings and trailing blank pages.
      LIMITATION, STATED RATHER THAN ASSUMED AWAY: LibreOffice drops OMML on
      conversion, so the rendered pages show the maths MISSING whether or not
      it fits. G-7a is therefore a NON-MATH layout gate; equation geometry is
      G-7b's job. Without a renderer the gate degrades to DORMANT and is
      REPORTED as dormant — absence never halts an audit.
  G-7b OMML AND FIGURE GEOMETRY (notes_audit.gate_line_rules): every paragraph
      carrying an equation or an image must use an AUTO line rule. A fixed
      rule CLIPS the object while leaving it present in the XML, so G-2a
      passes and the page is still wrong. This is the mechanical replacement
      for the visual check LibreOffice cannot perform, and it is stricter than
      a human glance would be.
  G-8 ANSWER INTEGRITY (notes_audit.gate_answer_integrity): every printed key
      must be a usable answer to the printed options — MCQ in range, MSQ a
      non-repeating subset, NAT numeric, none missing. G-5 checks the
      template; nothing before v3.0.0 checked the key itself, and a wrong key
      is the worst defect that can reach a student.
  G-9 ORPHAN TERMS (notes_audit.gate_orphan_terms): a term used in a stem,
      option or explanation but taught nowhere in the notes body breaks the
      closed-book promise at vocabulary level. The section 2 solver already
      knows the subject and can silently supply the missing term; this set
      difference cannot. ADVISORY — it reports for NA's judgement and does not
      block, because common English is not a syllabus term.
  G-10 COUNTER INTEGRITY (notes_audit.gate_counters): Example j and Recall j
      sequences gapless and 1-based. G-6 covers section 6A outline numbers
      only.
  G-11 TERMINAL RE-GATE (notes_audit.terminal_regate) — MANDATORY, LAST.
      After the final edit, re-run the FULL solve across ALL of the unit's
      bank questions and EVERY gate above over the bytes that will ship, then
      hash them. NA edits the document, so certifying the pre-patch draft
      certifies a file that no longer exists: a correction that fixes Q7 and
      breaks Q12's cross-reference is exactly what a pre-patch certification
      misses. Only G-9 (advisory) and a DORMANT G-7a are non-blocking.
      G-11 is itself REPORTED as a gate, carrying the certified sha256 and the
      number of gates run, so audit_summary shows plainly WHICH bytes were
      certified rather than asserting it in prose alone. Every identifier in
      notes_audit.GATES appears in the report; notes_sync_audit.py checks that
      this list and this section still agree.

## §6 — REPORT AND STATE
There is NO .md audit report. The report OBJECT (notes_audit.new_report) is
still built and is still the certification instrument — pass_for_unit operates
on it and is the vacuous-pass floor — but the persisted artifact is
notes_audit.audit_summary(...) stored INSIDE the registry unit record
(notes-registry/2.1). The summary itself carries the report schema string
notes-audit-report/2.0 (notes_audit.REPORT_SCHEMA), so a schema bump is
visible to a reader of the registry and to notes_sync_audit.py. It carries: verdict counts by class, the key-correction
list with tiers, the judgement-tier count, the quarantine list, the
improvement and patch counts, the FIGURE_PENDING queue, every gate result,
the bank_ref and taxonomy_ref the unit was audited against, and the final_ref
of the shipped bytes. The two refs are what let the section 3 standing
re-audit trigger identify which units a refreshed bank affects.

A unit passes ONLY when notes_audit.pass_for_unit(report, unit_questions) is
True, at which point it moves DRAFTED -> AUDITED_PASS with notes_version
bumped and final_ref set.

## §7 — CONTENT-STYLE BANS AND THE DOCUMENT ITSELF
Framework_NotesCreate section 7 and F-6 apply UNCHANGED to NA's output.
NOTHING inside the document ever marks a correction, a quarantine, a version,
a warning, a comment, a review note or any pipeline metadata. Every one of
those lives in the chat and the registry. A student-facing file carries
teaching and nothing else.

## §8 — RUNS, STATE AND IDEMPOTENCE
One subtopic per run; a multi-unit request splits into separate per-unit runs,
each a complete step ending in its own footer. On completion the unit moves
DRAFTED -> AUDITED_PASS.

IDEMPOTENCE RULE: re-running NA on its own _Final.docx MUST produce zero
corrections, zero improvements and a byte-identical document. This is what
bounds section 2A's discretionary improvement — an improvement licence with no
convergence criterion would otherwise let two runs of the same input produce
two different documents. The property rests on notes_docx's fixed-point round
trip (W-3) and on section 1's deterministic, never-re-judged figure renders.

## §9 — DELIVERY
NA emits EXACTLY ONE document in every outcome, named by
notes_core.notes_final_filename(...) — {unit_code}_{Slug}_Final.docx. The name
is derived by CALLING the engine, never by spelling the pattern.

On completion: present_files the _Final.docx AND the updated
notes_registry.json (unit -> AUDITED_PASS, carrying draft_ref, final_ref and
audit_summary), then RENDER THE F2 STEP-COMPLETE FOOTER as the LAST element of
the response (Framework_DeliveryFooter section 4-1; 4-cell NOTES bar "3 of 4";
header "Step NA · NotesAudit"; Next -> ND: NotesDeliver in a new chat). The
footer is obligatory after a present_files call (section 4-0 R1) and is never
omitted.

THE CHAT DELIVERY LINE carries what the document deliberately does not:
<Sub Topic Name> (<sid>), unit_code, notes_version, n/n solvable, the
key-correction count with the JUDGEMENT-tier ones named individually (section
3A), the quarantine list with reasons (section 4 L-4), any --accept-modified
warning (section 0B P-3), the FIGURE_PENDING count, and any DORMANT gate
(section 5 G-7a).

---

# END OF Framework_NotesAudit v3.0.0
