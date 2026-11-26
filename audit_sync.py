"""audit_sync.py — CROSS-STEP SYNCHRONISATION AUDIT.
Does not test behaviour; tests whether the 11 steps AGREE with each other."""
import ast, json, os, re, sys
from collections import defaultdict

# GAP-2026-08-16-AUDITOR-FENCE-BLINDNESS: dedent each fence before it is
# parsed. MEASURED 2026-08-16: this extractor yielded 147 blocks across five
# specs and 61 of them failed ast.parse purely on uniform leading whitespace,
# so 41% of the python it appeared to audit was silently discarded.
# textwrap.dedent strips only the COMMON prefix and adds/removes no line, so
# nested code is untouched and every line number stays valid.
def blocks(t):
    """Return the dedented source of every ```python fence.

    GAP-2026-08-16-AUDITOR-FENCE-BLINDNESS. The dedent is the fix. A fence whose ```
    marker and body are BOTH indented yields uniformly-indented source, which
    ast.parse rejects as "unexpected indent", so the caller's try/except discarded it
    in silence. MEASURED across five specs: 61 of 147 blocks — 41% of the python this
    auditor appeared to be checking. textwrap.dedent strips only the COMMON prefix and
    adds or removes no line, so nested code is unaffected and every line number stays
    valid. Verified over all 259 fences in the corpus: nothing that parsed before
    stopped parsing, and no fence changed line count.

    THE REGEX IS GONE (2026-08-20). The non-greedy `(.*?)` ended the capture at the
    FIRST ``` in the body, so a fence containing a triple backtick inside a docstring
    was cut mid-string. That truncated Framework_MockTestAnalyse.md's S8-1 batch-loop
    acquisition fence — the whole Drive transport contract — into something that did
    not parse, so the caller's try/except discarded it and this auditor scanned code it
    had never read. Same fix, same release and same reasoning as audit_deep.py; see
    XSPEC_DIVERGENCE_BASELINE.json for the exemption mechanism that unblocked it there.
    Measured on the deployed corpus: regex 261 of 264 fences parse, line scanner
    263 of 263.
    """
    import textwrap
    out, cur = [], None
    for line in t.split('\n'):
        stripped = line.strip()
        if cur is None:
            if stripped == '```python':
                cur = []
            continue
        if stripped == '```':
            out.append(textwrap.dedent('\n'.join(cur)))
            cur = None
        else:
            cur.append(line)
    return out

def _self_test():
    """GAP-2026-08-14-AUDITOR-SELFTESTS. Script-style auditor, so fixtures run
    it as a SUBPROCESS against a mutated corpus copy and assert each check
    class still fires. Dispatched before the corpus loads."""
    import shutil, subprocess, tempfile
    passed, fails = 0, []
    here = os.path.dirname(os.path.abspath(__file__)) or '.'

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def run_in(root, env=None):
        _env = dict(os.environ, **env) if env else None
        r = subprocess.run([sys.executable, os.path.join(root, 'audit_sync.py')],
                           cwd=root, capture_output=True, text=True, env=_env)
        return r.returncode, r.stdout + r.stderr

    def _tracked_nonspec():
        """Every non-.md/.py artefact gen_manifest tracks, plus the release files.

        Read from gen_manifest itself so the two can never disagree. Falls back to a
        literal set only if gen_manifest is unimportable, which would be a broken
        checkout rather than a drift.
        """
        base = {'routes.json', 'MANIFEST.json', 'VERSION', 'CHANGELOG.md'}
        try:
            import importlib
            gm = importlib.import_module('gen_manifest')
            base |= set(getattr(gm, 'TRACKED_JSON', []))
            base |= set(getattr(gm, 'TRACKED_DOC', []))
        except Exception:
            base |= {'SPEC_MANIFEST.json', 'SPEC_SECTIONS.json',
                     'MUTATION_BUDGETS.json', 'LAW_REGISTRY.json', 'SPEC_HISTORY.md'}
        base.add('SPEC_MANIFEST.json')      # built by build_spec_manifest, not gen_manifest
        return base

    def mutated(mutate=None, env=None):
        d = tempfile.mkdtemp()
        for f in os.listdir(here):
            # SPEC_MANIFEST.json joins this list for DOC-COUNT (2026.08.15.7):
            # a fixture corpus missing it cannot verify CLAUDE.md's declared counts,
            # so the clean-copy baseline would fail for a reason that is not a defect.
            # SPEC_SECTIONS.json and MUTATION_BUDGETS.json join it for the SAME reason
            # (2026.08.15.11): every tracked non-.md/.py artefact must be copied, or
            # DOC-COUNT compares CLAUDE.md's declared total against a fixture corpus
            # that is short by exactly the files this list forgot. The recurrence is
            # the point — the list is hand-maintained and has now drifted twice, so
            # anything added to gen_manifest.TRACKED_JSON must be added here too.
            # DERIVED FROM gen_manifest, NEVER HAND-LISTED (2026.08.15.14). This
            # list drifted three times in six releases — SPEC_MANIFEST.json,
            # then SPEC_SECTIONS.json + MUTATION_BUDGETS.json, then SPEC_HISTORY.md
            # — and each time the symptom was identical: DOC-COUNT compared
            # CLAUDE.md's declared total against a fixture corpus short by exactly
            # the files this list forgot. Correcting the instance and not the class
            # is the failure the LAW-PROPAGATION LAW exists to remove, so the class
            # is removed here: whatever gen_manifest.py tracks, the fixture copies.
            if f.endswith(('.md', '.py')) or f in _tracked_nonspec():
                shutil.copy(os.path.join(here, f), os.path.join(d, f))
        if mutate:
            mutate(d)
        rc, out = run_in(d, env=env)
        shutil.rmtree(d, ignore_errors=True)
        return rc, out

    def append(root, fname, text):
        with open(os.path.join(root, fname), 'a', encoding='utf-8') as f:
            f.write(text)

    rc, out = mutated()
    check("clean corpus copy passes", rc == 0)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nimport blueprint_core as bc\nx = bc.no_such_fn_selftest(1)\n```\n"))
    check("ENGINE-API fires on a call into an API that does not exist",
          rc == 1 and 'ENGINE-API' in out and 'no_such_fn_selftest' in out)

    # ── ENGINE-SECTIONJOIN (GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE) ─────
    rc, out = mutated(lambda r: append(r, 'paper_pipeline.py',
        "\ndef _sj_probe(manifest_ids, sid, section_name):\n"
        "    return manifest_ids.get(sid, {}).get('section') == section_name\n"))
    check("ENGINE-SECTIONJOIN fires on .get('section') == section_name",
          rc == 1 and 'ENGINE-SECTIONJOIN' in out and 'paper_pipeline.py' in out)

    rc, out = mutated(lambda r: append(r, 'transport_core.py',
        "\ndef _sj_probe2(mv, section):\n"
        "    return mv['section'] != section['name']\n"))
    check("ENGINE-SECTIONJOIN fires on the subscript != section['name'] variant",
          rc == 1 and 'ENGINE-SECTIONJOIN' in out and 'transport_core.py' in out)

    rc, out = mutated(lambda r: append(r, 'frequency_xlsx.py',
        "\ndef _sj_probe3(v, section_name):\n"
        "    return v['section'] == section_name\n"))
    check("ENGINE-SECTIONJOIN allow-list is line-anchored, not file-wide",
          rc == 1 and 'ENGINE-SECTIONJOIN' in out and 'frequency_xlsx.py' in out)

    def relsync(r):
        open(os.path.join(r, 'VERSION'), 'w', encoding='utf-8').write('9999.99.99.9\n')
    rc, out = mutated(relsync)
    check("REL-SYNC fires when VERSION and CHANGELOG top entry disagree",
          rc == 1 and 'REL-SYNC' in out)

    def badroute(r):
        p = os.path.join(r, 'routes.json')
        routes = json.load(open(p, encoding='utf-8'))
        routes['PYQSort'] = routes['PYQSort'] + ['no_such_file_selftest.py']
        json.dump(routes, open(p, 'w', encoding='utf-8'))
    rc, out = mutated(badroute)
    check("ROUTE-MISSING fires on a routed file that does not exist",
          rc == 1 and 'ROUTE-MISSING' in out and 'no_such_file_selftest' in out)

    def chainbreak(r):
        p = os.path.join(r, 'Framework_MockDeliver.md')
        s = open(p, encoding='utf-8').read().replace('_Final.docx', '_FinalX.docx')
        open(p, 'w', encoding='utf-8').write(s)
    rc, out = mutated(chainbreak)
    check("FILENAME-CHAIN fires when a step stops naming its output suffix",
          rc == 1 and 'FILENAME-CHAIN' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\nSee Framework_Blueprint v99.99 for the schedule.\n"))
    check("VERSION-XREF fires on a forward reference to a version that "
          "does not exist", rc == 1 and 'VERSION-XREF' in out)

    # ── GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (P7) ─────────────────────
    def drop_from_governs(r):
        pth = os.path.join(r, 'LAW_REGISTRY.json')
        reg = json.load(open(pth, encoding='utf-8'))
        law = reg['laws']['EXECUTION-BOUNDARY-LAW']
        law['governs'] = [g for g in law['governs'] if g != 'Framework_PYQCount.md']
        json.dump(reg, open(pth, 'w', encoding='utf-8'), indent=2)
    rc, out = mutated(drop_from_governs)
    check("LAW-COVERAGE fires when a spec performs a governed operation but is "
          "absent from the registry",
          rc == 1 and 'LAW-COVERAGE' in out and 'Framework_PYQCount.md' in out)

    def break_the_law(r):
        pth = os.path.join(r, 'Framework_PYQCount.md')
        s = open(pth, encoding='utf-8').read().replace(
            'return corpus_io.fetch_drive_docx(resolver, paper, work_dir)',
            'return corpus_io.fetch_drive_docx(gdrive_download_file_selftest, '
            'paper, work_dir)')
        open(pth, 'w', encoding='utf-8').write(s)
    rc, out = mutated(break_the_law)
    check("LAW-VERIFY fires when a governed spec stops satisfying its verifier",
          rc == 1 and 'LAW-VERIFY' in out)

    # ── GAP-2026-08-26-REGISTRY-HANDOFF-SEAM ─────────────────────────────────
    def drop_rh_governs(r):
        pth = os.path.join(r, 'LAW_REGISTRY.json')
        reg = json.load(open(pth, encoding='utf-8'))
        law = reg['laws']['REGISTRY-HANDOFF-LAW']
        law['governs'] = [g for g in law['governs'] if g != 'Framework_MockTestExplain.md']
        json.dump(reg, open(pth, 'w', encoding='utf-8'), indent=2)
    rc, out = mutated(drop_rh_governs)
    check("LAW-COVERAGE derives the REGISTRY-HANDOFF performing set from registry-writer "
          "calls (a spec calling dg_write_verdict dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'REGISTRY-HANDOFF-LAW' in out
          and 'Framework_MockTestExplain.md' in out)

    # ── GAP-2026-09-14-REGISTRY-SOURCE ───────────────────────────────────────
    def drop_rs_governs(r):
        pth = os.path.join(r, 'LAW_REGISTRY.json')
        reg = json.load(open(pth, encoding='utf-8'))
        law = reg['laws']['REGISTRY-SOURCE-LAW']
        law['governs'] = [g for g in law['governs'] if g != 'Framework_MockDeliver.md']
        json.dump(reg, open(pth, 'w', encoding='utf-8'), indent=2)
    rc, out = mutated(drop_rs_governs)
    check("LAW-COVERAGE derives the REGISTRY-SOURCE performing set from resolve_registry "
          "calls (a spec calling pp.resolve_registry dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'REGISTRY-SOURCE-LAW' in out
          and 'Framework_MockDeliver.md' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\nreg = json.load(open(f'/mnt/project/{EXAM}_registry.json', encoding='utf-8'))\n"))
    check("LAW-COVERAGE derives the REGISTRY-SOURCE performing set from the retired "
          "direct-open idiom too (a new spec opening the Files path is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'REGISTRY-SOURCE-LAW' in out
          and 'Framework_PYQSort.md' in out)

    # ── GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY ─────────────
    def _drop_governs(law, spec):
        def _m(r):
            pth = os.path.join(r, 'LAW_REGISTRY.json')
            reg = json.load(open(pth, encoding='utf-8'))
            reg['laws'][law]['governs'] = [g for g in reg['laws'][law]['governs'] if g != spec]
            json.dump(reg, open(pth, 'w', encoding='utf-8'), indent=2)
        return _m
    rc, out = mutated(_drop_governs('FIGURE-TYPE-COVERAGE-LAW', 'Framework_ScopedBlueprint.md'))
    check("LAW-COVERAGE derives the FIGURE-TYPE-COVERAGE performing set from the presence-flag "
          "producer idiom (ScopedBlueprint dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'FIGURE-TYPE-COVERAGE-LAW' in out
          and 'Framework_ScopedBlueprint.md' in out)
    rc, out = mutated(_drop_governs('MANIFEST-COMMIT-LAW', 'Framework_MockTestCreate.md'))
    check("LAW-COVERAGE derives the MANIFEST-COMMIT performing set from fa.commit_registry( "
          "(MockTestCreate dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'MANIFEST-COMMIT-LAW' in out
          and 'Framework_MockTestCreate.md' in out)
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nflags = {'figural_present': exam_config.get('figural_present', False)}\n```\n"))
    check("LAW-COVERAGE derives the presence-flag performing set from the RETIRED inheritance "
          "idiom too (a new spec copying exam_config.get('figural_present' is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'Framework_PYQSort.md' in out
          and 'MANIFEST-COMMIT-LAW' in out)
    rc, out = mutated(_drop_governs('QUALITY-GATE-LAW', 'Framework_MockReview.md'))
    check("LAW-COVERAGE derives the QUALITY-GATE performing set from the Cluster QQ entry "
          "points (MockReview dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'QUALITY-GATE-LAW' in out
          and 'Framework_MockReview.md' in out)
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nx = 1   # bc.deliver_allowed(cert, False)\n```\n"))
    check("LAW-COVERAGE ignores a QQ entry point named only in a trailing comment",
          not ('LAW-COVERAGE' in out and 'Framework_PYQSort.md' in out and 'QUALITY-GATE-LAW' in out))
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nok, why = bc.deliver_allowed(cert, False)\n```\n"))
    check("LAW-COVERAGE flags a NEW spec that calls a QQ entry point without being governed",
          rc == 1 and 'LAW-COVERAGE' in out and 'Framework_PYQSort.md' in out
          and 'QUALITY-GATE-LAW' in out)
    rc, out = mutated(_drop_governs('FIGURE-RECORD-INTEGRITY-LAW', 'Framework_MockTestCreate.md'))
    check("LAW-COVERAGE derives the FIGURE-RECORD performing set from validate_semantic_object( "
          "(MockTestCreate dropped from governs is flagged)",
          rc == 1 and 'LAW-COVERAGE' in out and 'FIGURE-RECORD-INTEGRITY-LAW' in out
          and 'Framework_MockTestCreate.md' in out)

    rc, out = mutated(lambda r: os.remove(os.path.join(r, 'LAW_REGISTRY.json')))
    check("LAW-REGISTRY fires when the registry is missing",
          rc == 1 and 'LAW-REGISTRY' in out)

    def _bend_count(r):
        pth = os.path.join(r, 'CLAUDE.md')
        t = open(pth, encoding='utf-8').read()
        t = re.sub(r'(routes\.json triggers\s*:\s*)\d+', r'\g<1>999', t)
        open(pth, 'w', encoding='utf-8').write(t)
    rc, out = mutated(_bend_count)
    check("DOC-COUNT fires when a declared count drifts from the files on disk",
          rc == 1 and 'DOC-COUNT' in out and '999' in out)

    def _drop_count_line(r):
        pth = os.path.join(r, 'CLAUDE.md')
        t = open(pth, encoding='utf-8').read()
        t = re.sub(r'^\s*MANIFEST\.json files\s*:\s*\d+\s*$', '', t, flags=re.M)
        open(pth, 'w', encoding='utf-8').write(t)
    rc, out = mutated(_drop_count_line)
    check("DOC-COUNT fires when a required count line is missing entirely",
          rc == 1 and 'DOC-COUNT' in out)

    def _reintroduce_idiom(r):
        with open(os.path.join(r, 'CLAUDE.md'), 'a', encoding='utf-8') as f:
            f.write('\nThe workbench baseline is currently 51 files, including tooling.\n')
    rc, out = mutated(_reintroduce_idiom)
    check("DOC-COUNT-IDIOM fires when a live count is hand-written back into prose",
          rc == 1 and 'DOC-COUNT-IDIOM' in out)

    # ══ B12 (2026-08-21) — THE THIRTEEN UNMEASURED EMISSIONS ═════════════════
    # The first FULL mutation measurement of this auditor (28 emissions; the prior
    # record was 9, from 2026.08.15.13) found 13 survivors — near half the gate was
    # unproven. Six of them shared one cause: every SKILL.md-dependent check read the
    # file from a session mount that exists on no CI runner, so those branches had
    # never executed in the environment that gates the build. The fixtures below give
    # every previously-unproven emission a mutant-killer. Each mutates a corpus COPY
    # and asserts the finding fires — the same mutate-and-expect-red pattern as the
    # rest of this suite.

    def replace(root, fname, old, new):
        q = os.path.join(root, fname)
        t = open(q, encoding='utf-8').read()
        assert old in t, f'fixture stale: {old[:40]!r} not in {fname}'
        open(q, 'w', encoding='utf-8').write(t.replace(old, new))

    def remove(root, fname):
        os.remove(os.path.join(root, fname))

    # GAP-2026-08-23-AUDITSYNC-FIXTURE-STALE: these three fixtures pinned the
    # LIVE inventory literals ('All 17 ... plus the 6 ...') and crashed the
    # release that took the tracked count 6 -> 7 — the exact content-keyed
    # fixture class this file's own _fenced_python note legislates against, and
    # the live check itself already avoids (it reads the counts with a regex).
    # Keyed to the SHAPE now: extract the counts with the SAME regex the live
    # check uses and build the mutation strings from what is actually there.
    # Adding an engine never touches these fixtures again; only REWORDING the
    # line does — and the third fixture exists to prove rewording fails loudly.
    _inv = re.search(r'All\s+(\d+)\s+routed engine scripts, plus the\s+(\d+)\s+'
                     r'tracked-but-never-routed',
                     open(os.path.join(here, 'SKILL.md'), encoding='utf-8').read())
    assert _inv, 'SKILL.md inventory line not found — fixtures cannot key to shape'
    _live_routed  = f'All {_inv.group(1)} routed engine scripts'
    _live_tracked = f'plus the {_inv.group(2)} tracked-but-never-routed'

    # L305 — SKILL-INVENTORY, routed-engine count.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        _live_routed, 'All 99 routed engine scripts'))
    check("SKILL-INVENTORY fires on a wrong routed-engine count",
          rc == 1 and 'SKILL-INVENTORY' in out and '99' in out)

    # L307 — SKILL-INVENTORY, tracked-but-never-routed count. This exact claim WAS
    # stale on the live corpus (said 3, reality 6) the day the check was revived —
    # proof the parity matters, preserved here as the fixture's shape.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        _live_tracked, 'plus the 2 tracked-but-never-routed'))
    check("SKILL-INVENTORY fires on a wrong tracked-not-routed count",
          rc == 1 and 'SKILL-INVENTORY' in out and 'tracked-but' in out)

    # ...and the re-point tripwire: reword the inventory line entirely and the check
    # must SAY it can no longer verify, not silently match nothing. That silent
    # no-match is exactly how the previous regex died.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        f'{_live_routed}, {_live_tracked}',
        'Seventeen engines ride along, and some other scripts too'))
    check("SKILL-INVENTORY fires when the inventory line is reworded away",
          rc == 1 and 'no longer carries' in out)

    # L343 — INFO when VERSION/CHANGELOG is unreadable. An INFO is still an emission:
    # a release-sync check that skips SILENTLY is the ENV-SKEW shape.
    rc, out = mutated(lambda r: remove(r, 'VERSION'))
    check("INFO fires when VERSION is unreadable (release sync skipped LOUDLY)",
          'release sync not checked' in out)

    # L350 — TRIGGER-SYNC, forward: a routed trigger SKILL.md never mentions.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md', 'PYQCompress', 'PYQSquash'))
    check("TRIGGER-SYNC fires on a routed trigger missing from SKILL.md",
          rc == 1 and "trigger 'PYQCompress' not mentioned" in out)

    # L353 — TRIGGER-SYNC, reverse: SKILL.md naming a trigger that routes nowhere.
    # (PYQSquash from the same mutation matches the trigger-shaped regex.)
    check("TRIGGER-SYNC fires on a SKILL.md trigger routes.json lacks",
          "'PYQSquash' but routes.json has no such trigger" in out)

    # L355 — the not-readable INFO. With the B12 loader this branch means the repo
    # carries NO copy at all — which must be said, not skipped.
    _repo_only = {'AUDIT_SYNC_SKILL_PATHS':
                  os.pathsep.join(('SKILL.md', 'mocktestframework_SKILL.md'))}
    rc, out = mutated(lambda r: (remove(r, 'SKILL.md'),
                                 remove(r, 'mocktestframework_SKILL.md')),
                      env=_repo_only)
    check("INFO fires when no SKILL.md copy exists anywhere",
          'SKILL.md not readable' in out)

    # Watch the watcher: prove the override actually CONTROLS the search surface —
    # on a CLEAN copy (repo SKILL.md present), a search list naming only a file
    # that does not exist must produce the same INFO. If this fixture goes green
    # with the env plumbing removed, the loader has stopped honouring the
    # injection and the fixture above is back to being environment-dependent.
    rc, out = mutated(env={'AUDIT_SYNC_SKILL_PATHS': 'no_such_skill_selftest.md'})
    check("SKILL search-surface injection is honoured (override yields the INFO)",
          'SKILL.md not readable' in out)

    # L376 — ERA-SYNC: nobody writes pattern_eras. Neutralise the writer's mention.
    # (The producer string now lives in Framework_Blueprint.md — the Step 5 writer
    # moved into analyse_engine.py at Wave 2 Part C, so the spec-side mention that
    # keeps this check satisfied is the Blueprint consumer contract.)
    rc, out = mutated(lambda r: replace(r, 'Framework_Blueprint.md',
        'pattern_eras', 'zz_pattern_eras_gone'))
    check("ERA-SYNC fires when no spec writes manifest['pattern_eras']",
          rc == 1 and "no spec writes manifest['pattern_eras']" in out)

    # L379 — ERA-SYNC: frequency_scope used with no --frequency-scope flag declared.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        '\nThis step also honours frequency_scope when present.\n'))
    check("ERA-SYNC fires on frequency_scope without a declared trigger flag",
          rc == 1 and 'declares no --frequency-scope' in out)

    # L382 — ERA-SYNC: OUT_OF_PATTERN not sourced from the engine.
    # PYQSort already sources bc.OUT_OF_PATTERN, so a mutation there cannot trip the
    # per-file test — measured while writing this fixture. PYQApprove carries neither
    # spelling, so it isolates exactly the condition.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQApprove.md',
        '\nRows tagged OUT_OF_PATTERN are excluded here.\n'))
    check("ERA-SYNC fires on OUT_OF_PATTERN not sourced from bc",
          rc == 1 and 'without sourcing it from the engine' in out)

    # L395 — BP-SCHEMA: a reader consuming a blueprint field the writer never documents.
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        "\n```python\nzz = bp['zz_phantom_field']\n```\n"))
    check("BP-SCHEMA fires on an undocumented blueprint field read",
          rc == 1 and 'zz_phantom_field' in out)

    # L432 — LAW-REGISTRY: the registry exists but is not JSON. Distinct from the
    # already-proven missing-file emission: corruption must not read as absence.
    rc, out = mutated(lambda r: open(os.path.join(r, 'LAW_REGISTRY.json'), 'w',
                                     encoding='utf-8').write('{not json'))
    check("LAW-REGISTRY fires on a corrupt registry file",
          rc == 1 and 'not valid JSON' in out)

    # L498 — LAW-VERIFY: a governed spec that fails its declared verifier. The
    # mutation plants a C10 violation (a partition downstream of a CLASS T
    # acquisition, no consumed=) in a spec EXECUTION-BOUNDARY/SESSION-BUDGET governs,
    # then requires the finding to be relayed AS a LAW-VERIFY line — the whole point
    # of the registry is that the law's verdict surfaces here, not only in the
    # verifier's own run.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQCount.md',
        '\nA2. CHANNEL PROBE — download exactly ONE paper.\n\n'
        '```python\npart = bc.partition_by_transport(papers, channel=channel)\n```\n'))
    # The DETAIL is asserted, not just the category. LAW-VERIFY has two emissions:
    # the per-finding relay (which carries the verifier's own [C10] line) and a
    # catch-all fallback ("audit_callgraph exited 1"). A fixture that only asks for
    # the category passes with the relay deleted, because the fallback still speaks —
    # measured: that mutant survived the first B12 run at 28/29. The [C10] tag exists
    # only in the relayed line, so this kills exactly that mutant.
    check("LAW-VERIFY relays a verifier failure on a governed spec",
          rc == 1 and 'LAW-VERIFY' in out and '[C10]' in out)

    # L541 — DOC-COUNT when the manifests are unreadable. A count that cannot be
    # verified must fail the build, not pass vacuously: DOC-COUNT exists precisely
    # because unverified counts drift.
    rc, out = mutated(lambda r: remove(r, 'SPEC_MANIFEST.json'))
    check("DOC-COUNT fires when a manifest needed for verification is unreadable",
          rc == 1 and 'could not read a manifest' in out)

    # ── The fence SHAPE the old regex could not read (2026-08-20) ────────────
    # This fixture was written at 2026.08.20.2 against corpus CONTENT — it named the
    # three functions in Framework_MockTestAnalyse.md's S8-1 fence. One release later
    # batch 9 extracted that fence into transport_core.py and the fixture went RED for
    # a reason that had nothing to do with the scanner. A fixture keyed to content
    # measures the corpus; one keyed to the SHAPE measures the code. This builds the
    # shape — an INLINE nested marker, ``` mid-sentence inside a docstring, which is
    # what the corpus actually contained and what the non-greedy regex ended on.
    _tricky = ('```python\n'
               'def outer(a):\n'
               '    """This contract lives in a ```python fence ON PURPOSE."""\n'
               '    return a + 1\n'
               '\n'
               'def after_the_marker(b):\n'
               '    return b * 2\n'
               '```\n')
    _got = blocks(_tricky)
    check("line scanner does not truncate a fence at an inline nested marker",
          len(_got) == 1 and 'after_the_marker' in _got[0])
    # ...and the regex this replaced must demonstrably fail the same input, or the
    # fixture asserts a property nothing ever lacked.
    _old = re.findall(r"```python\n(.*?)```", _tricky, re.S)
    check("the regex this replaced DOES truncate the same input",
          bool(_old) and 'after_the_marker' not in _old[0])

    # ── 2026.11.09 (GAP-2026-11-08-DR3-QINDEX-CONFLICT) — LABEL-VERIFIER / REVIEW-COVERAGE / LADDER-COVERAGE ──
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\nok, m = bc.verify_difficulty_obs(label, obs, labels)\n```\n'))
    check("LABEL-VERIFIER fires when a governed spec verifies a label with the obs primitive",
          rc == 1 and 'LABEL-VERIFIER' in out and 'Framework_MockTestCreate.md' in out)
    def _strip_cov(r):
        p08 = os.path.join(r, 'Framework_MockTestCreate.md')
        t08 = open(p08, encoding='utf-8').read().replace('bc.review_coverage_missing(', 'bc.review_coverage_gone(')
        open(p08, 'w', encoding='utf-8').write(t08)
    rc, out = mutated(_strip_cov)
    check("REVIEW-COVERAGE fires when the governed spec stops checking coverage",
          rc == 1 and 'REVIEW-COVERAGE' in out)
    # ── 2026.11.10 (GAP-2026-11-10) — STOP-NEEDS-REPAIR / organic_parity_rule ──
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\nraise SystemExit("HARD STOP [HS:INPUT] (S3 difficulty feasibility, x)")\n```\n'))
    check("STOP-NEEDS-REPAIR fires when Create stops on a difficulty input again",
          rc == 1 and 'STOP-NEEDS-REPAIR' in out and 'difficulty feasibility' in out)
    def _sc1_back(r):
        p10 = os.path.join(r, 'Framework_MockTestCreate.md')
        t10 = open(p10, encoding='utf-8').read()
        i10 = t10.index('\n', t10.index('\n## S13-2L') + 1)          # just after the real S13-2L header line
        t10 = t10[:i10] + '\n```python\n_p = bc.dl_swap_partner(q, t, g, l)\n```\n' + t10[i10:]
        open(p10, 'w', encoding='utf-8').write(t10)
    rc, out = mutated(_sc1_back)
    check("STOP-NEEDS-REPAIR fires when S13-2L writes a retired SC1 ending again",
          rc == 1 and 'STOP-NEEDS-REPAIR' in out and 'dl_swap_partner(' in out)
    rc, out = mutated(lambda r: append(r, 'Framework_NotesCreate.md',
        '\n```python\nok = bc.clone_guard(item, past=p)\n```\n'))
    check("organic_parity_rule: a spec that calls an S0-OP entry point but is not governed fails LAW-COVERAGE",
          rc == 1 and 'LAW-COVERAGE' in out and 'Framework_NotesCreate.md' in out and 'LAW-ORG' in out)
    rc, out = mutated(lambda r: append(r, 'audit_canonical.py',
        "\n\ndef gate_unrouted_fixture(src):\n    _fail('A-UNROUTED-FIXTURE', 'x')\n"))
    check("LADDER-COVERAGE fires on an auditor FAIL gate with no route",
          rc == 1 and 'LADDER-COVERAGE' in out and 'A-UNROUTED-FIXTURE' in out)
    rc, out = mutated(lambda r: append(r, 'Framework_PYQCount.md',
        '\n```python\nok = bc.verify_difficulty_label(entry, labels)\n```\n'))
    check("LAW-COVERAGE derives the LABEL-BASIS-LAW performing set from the corpus",
          rc == 1 and 'LAW-COVERAGE' in out and 'LABEL-BASIS-LAW' in out and 'Framework_PYQCount.md' in out)

    # ── 2026.11.17 (GAP-2026-11-14-SPEED-AND-FIDELITY P5) — STOP-REPAIR-COVERAGE ──
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\nraise SystemExit("HARD STOP [HS:INFRA] (S13-9 fixture): the record is gone.")\n```\n'))
    check("STOP-REPAIR-COVERAGE fires on an INFRA stop after Q1 that names no repair",
          rc == 1 and 'STOP-REPAIR-COVERAGE' in out and 'S13-9 fixture' in out)
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\nraise SystemExit("HARD STOP [HS:INFRA] (S13-9 fixture): the record is gone — "\n'
        '                 "re-run S13-4, then this block.")\n```\n'))
    check("STOP-REPAIR-COVERAGE accepts an INFRA stop that names its repair",
          'STOP-REPAIR-COVERAGE' not in out)
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\n_act, st, n = bc.infra_heal_step(st, "S13-9")\nraise SystemExit("HARD STOP [HS:INFRA] (S13-9 fixture): gone.")\n```\n'))
    check("STOP-REPAIR-COVERAGE accepts an INFRA stop behind bc.infra_heal_step",
          'STOP-REPAIR-COVERAGE' not in out)
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        '\n```python\nraise SystemExit("HARD STOP [HS:INPUT] (S7 fixture): upload the file again")\n```\n'))
    check("STOP-REPAIR-COVERAGE fires on an INPUT stop after Q1",
          rc == 1 and 'STOP-REPAIR-COVERAGE' in out and 'HS:INPUT] after the first question' in out)

    # ── 2026.11.17 — ENGINE-STATUS-SYNC ──
    rc, out = mutated(lambda r: append(r, 'final_assembly.py', '\n_FIXTURE_LINE = "STEP A2: VANISH Q1"\n'))
    check("ENGINE-STATUS-SYNC fires on a printed status the spec never explains",
          rc == 1 and 'ENGINE-STATUS-SYNC' in out and 'VANISH' in out)

    # ── 2026.12.04 — RPAR-SYNC (GAP-2026-11-26-RENDER-PARITY) ──
    rc, out = mutated(lambda r: open(os.path.join(r, 'Framework_MockTestCreate.md'), 'w', encoding='utf-8').write(
        open(os.path.join(r, 'Framework_MockTestCreate.md'), encoding='utf-8').read().replace(
            ' \\\n                  --item-texts /home/claude/[ExamCode]_M[N]_item_texts.json', '')))
    check("RPAR-SYNC fires when STEP B stops writing --item-texts", rc == 1 and 'RPAR-SYNC' in out)
    rc, out = mutated(lambda r: open(os.path.join(r, 'blueprint_core.py'), 'w', encoding='utf-8').write(
        open(os.path.join(r, 'blueprint_core.py'), encoding='utf-8').read().replace(
            "'stem_lines_position', 'problem_labels')", "'problem_labels')")))
    check("RPAR-SYNC fires when the reviewer packet drops stem_lines_position", rc == 1 and 'RPAR-SYNC' in out
          and 'stem_lines_position' in out)
    print(f"audit_sync self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails

if __name__ == '__main__' and '--self-test' in sys.argv:
    sys.exit(0 if _self_test() else 1)

SPECS = sorted(f for f in os.listdir('.') if f.startswith('Framework_') and f.endswith('.md'))
TXT = {f: open(f, encoding='utf-8').read() for f in SPECS}
ROUTES = json.load(open('routes.json'))
ISSUES = defaultdict(list)
# ── SKILL.md — REPO ROOT FIRST (B12, 2026-08-21) ────────────────────────────
# This loader read ONLY '/mnt/skills/user/mock-test-framework/SKILL.md' — a session-
# sandbox mount that exists on NO CI runner. So SKILL-INVENTORY and both TRIGGER-SYNC
# directions never executed in the environment that gates the build; they ran only in
# an interactive session that happened to have the skill mounted, and the 'SKILL.md
# not readable' INFO printed everywhere else looked routine enough that nobody asked
# why a parity check against a file THE REPO ITSELF CARRIES needed a mount to run.
# Same class as GAP-2026-08-17-B4-ENV-SKEW: a check that silently skips in the gating
# environment is indistinguishable from one that passes. Found by the B12 full
# mutation measurement — all six SKILL-dependent emissions survived, including the
# fallback INFO itself, which is the signature of a branch that never runs.
# The repo copy is authoritative: it is version-controlled beside the routes.json it
# must agree with. The mount stays as a last resort for environments with no clone.
# The search list is ENV-INJECTABLE (AUDIT_SYNC_SKILL_PATHS, os.pathsep-separated)
# so the self-test can constrain the search surface: the "no SKILL.md copy exists
# anywhere" fixture removes both repo copies from its corpus COPY but cannot remove
# the session mount, so in any session with /mnt/skills mounted the fixture failed
# while CI (no mount) passed — the GAP-2026-08-17-B4-ENV-SKEW shape, inverted.
# Injecting the list is the same remedy as search_dirs/out_dir. Default UNCHANGED.
_skill_env = os.environ.get('AUDIT_SYNC_SKILL_PATHS')
SKILL_SEARCH_PATHS = (tuple(q for q in _skill_env.split(os.pathsep) if q)
                      if _skill_env is not None else
                      ('SKILL.md', 'mocktestframework_SKILL.md',
                       '/mnt/skills/user/mock-test-framework/SKILL.md'))
skill_txt = None
for _sp in SKILL_SEARCH_PATHS:
    if os.path.exists(_sp):
        skill_txt = open(_sp, encoding='utf-8').read()
        break
def rec(cat, msg): ISSUES[cat].append(msg)

def public(mod):
    try:
        src = open(mod + '.py', encoding='utf-8').read()
    except FileNotFoundError:
        return None
    names = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            # A re-exported import IS part of the module's public surface: after
            # `from t3_mathcomp import _T3_STATS as T3_STATS`, explain_engine.T3_STATS
            # resolves at runtime exactly like an assignment would. Collecting only
            # def/class/assign made every such name look absent, so a spec that used
            # one was reported as calling into an API that does not exist.
            for a in n.names:
                if a.name != '*':
                    names.add(a.asname or a.name.split('.')[0])
    return names

ALIAS = {'bc': 'blueprint_core', 'pp': 'paper_pipeline', 'ee': 'explain_engine'}
API = {a: public(m) for a, m in ALIAS.items()}
# Scope PER CODE BLOCK: an alias only means the module inside a block that imports it as
# that alias. `pp` is also a common local for doc.add_paragraph(), and `bc` for other locals
# — checking file-wide produces false positives (verified: Framework_MockTestCreate v5.29
# explicitly documents the pp module/paragraph name coexistence as safe).
for f, t in TXT.items():
    for blk in blocks(t):
        bound = {}
        for m in re.finditer(r'^\s*import\s+(\w+)\s+as\s+(\w+)', blk, re.M):
            if m.group(1) in ALIAS.values():
                bound[m.group(2)] = m.group(1)
        for alias, mod in bound.items():
            names = public(mod)
            if not names:
                continue
            # a local rebind of the alias inside the same block disqualifies it
            if re.search(rf'^\s*{alias}\s*=', blk, re.M):
                continue
            for m in re.finditer(rf'\b{alias}\.([A-Za-z_][A-Za-z0-9_]*)', blk):
                if m.group(1) not in names:
                    rec('ENGINE-API', f"{f}: {alias}.{m.group(1)} not found in {mod}.py")

# ── 1a-SJ. ENGINE-SECTIONJOIN — the Section↔Subject namespace-join ratchet ──
# GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE. Two blueprint_core functions joined
# the manifest 'section' field (taxonomy SUBJECT namespace: "Organic Chemistry")
# against an OTS section-label variable ("Section A") with a raw `==`. On every
# exam that is not a 1:1 section↔Subject identity map the namespaces never
# intersect, so the join matched NOTHING and both functions answered for an
# empty subtopic pool — every Axis-2 guarantee 'unsatisfiable', every targeted
# Axis-1 format 'unreachable' — with status still 'ok', so no gate fired.
# Framework_Blueprint §2-1 FIX D has forbidden this join since v1.32, but FIX D
# is prose in one spec: it constrains spec authors, not engine authors, and the
# engines are the shared 200-project code. This rule is the missing enforcement:
# the prohibition now FAILS THE BUILD, mechanically, on every engine .py.
#
# Detection is AST, not regex — a text regex misses reordered operands and
# false-positives on the docstrings that (correctly) QUOTE the banned pattern
# while narrating the fix. A finding is any Eq/NotEq Compare where one side
# reads a 'section' key (x['section'] or x.get('section'[, d])) and the other
# is a section-label-shaped identifier (sec/section[_name]/scope_label/*_label,
# incl. attribute form) or the section['name'] subscript FIX D itself quotes.
#
# ALLOW-LIST — content-anchored (line text, never line numbers), one entry per
# legitimate site, each with its reason. Both operands must live in the SAME
# namespace for an entry to belong here.
_SJ_ALLOW = {
    'frequency_xlsx.py': (
        # Subject-to-Subject: `section` iterates sorted({e['section'] ...}) —
        # both operands are taxonomy Subjects drawn from the same data.
        r"v\['section'\]\s*==\s*section(?!\w)",
        # Subject-to-Subject: `sec` iterates the same per-section sheet loop.
        r"e\['section'\]\s*==\s*sec(?!\w)",
    ),
}
_SJ_ID = re.compile(
    r"(?i)^(sec|section|sec_name|section_name|secname|sectionname|scope_label)$")

def _sj_reads_section_key(node):
    """x['section']  |  x.get('section')  |  x.get('section', default)"""
    if isinstance(node, ast.Subscript):
        s = node.slice
        return isinstance(s, ast.Constant) and s.value == 'section'
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == 'get' and node.args
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == 'section')

def _sj_is_section_label(node):
    """A section-name-shaped identifier, or the section['name'] subscript that
    FIX D's own forbidden example uses."""
    if isinstance(node, ast.Name):
        return bool(_SJ_ID.match(node.id)) or node.id.endswith('_label')
    if isinstance(node, ast.Attribute):
        return bool(_SJ_ID.match(node.attr)) or node.attr.endswith('_label')
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
        s = node.slice
        return (bool(_SJ_ID.match(node.value.id))
                and isinstance(s, ast.Constant) and s.value == 'name')
    return False

for _sj_file in sorted(f for f in os.listdir('.') if f.endswith('.py')):
    try:
        _sj_src = open(_sj_file, encoding='utf-8').read()
        _sj_tree = ast.parse(_sj_src)
    except (SyntaxError, UnicodeDecodeError, OSError):
        continue          # an unparseable engine is bootstrap/CI's finding, not ours
    _sj_lines = _sj_src.split('\n')
    for _sj_node in ast.walk(_sj_tree):
        if not (isinstance(_sj_node, ast.Compare) and len(_sj_node.ops) == 1
                and isinstance(_sj_node.ops[0], (ast.Eq, ast.NotEq))):
            continue
        _L, _R = _sj_node.left, _sj_node.comparators[0]
        if not ((_sj_reads_section_key(_L) and _sj_is_section_label(_R))
                or (_sj_reads_section_key(_R) and _sj_is_section_label(_L))):
            continue
        _sj_line = _sj_lines[_sj_node.lineno - 1].strip()
        if any(re.search(_rx, _sj_line) for _rx in _SJ_ALLOW.get(_sj_file, ())):
            continue
        rec('ENGINE-SECTIONJOIN',
            f"{_sj_file}:{_sj_node.lineno}: engine joins a manifest 'section' value "
            f"(taxonomy SUBJECT) against a section-name variable (OTS LABEL): "
            f"`{_sj_line[:90]}`. Framework_Blueprint §2-1 FIX D forbids this join — "
            f"it matches NOTHING on every non-identity exam and fails SILENTLY. "
            f"Trust the caller's pre-resolved id list (see "
            f"blueprint_core.axis1_mock_feasibility for the sanctioned no-filter "
            f"form) or require a bridged local view; if the site is genuinely "
            f"Subject-to-Subject, add a content-anchored _SJ_ALLOW entry with the "
            f"reason. Ref GAP-2026-08-18-AXIS-SECTIONKEY-RAWCOMPARE.")

# ── 1b. SKILL.md claimed inventory vs reality ───────────────────────────────
if skill_txt:
    # The claims that ACTUALLY exist in SKILL.md, not the sentence this check was
    # written against. The old regex looked for 'The N framework specs and M engine
    # scripts' — that phrasing left SKILL.md at some point and the check matched
    # nothing thereafter, a silent no-op even where the file WAS readable. Checking a
    # quote nobody maintains is checking nothing; these two phrases are the live
    # inventory line, and if they are ever reworded this check must be re-pointed —
    # which the mspec-is-None branch below now says out loud instead of passing.
    mspec = re.search(r'All\s+(\d+)\s+routed engine scripts, plus the\s+(\d+)\s+'
                      r'tracked-but-never-routed', skill_txt)
    if mspec:
        claim_routed, claim_unrouted = int(mspec.group(1)), int(mspec.group(2))
        _routed = {f for v in ROUTES.values() for f in v if f.endswith('.py')}
        real_routed = len(_routed)
        try:
            _tracked = {k for k in json.load(open('MANIFEST.json',
                        encoding='utf-8'))['files'] if k.endswith('.py')}
            real_unrouted = len(_tracked - _routed)
        except (OSError, ValueError, KeyError):
            real_unrouted = None
        if claim_routed != real_routed:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_routed} routed engine "
                                   f"scripts, routes.json routes {real_routed}")
        if real_unrouted is not None and claim_unrouted != real_unrouted:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_unrouted} tracked-but-"
                                   f"never-routed scripts, MANIFEST.json minus "
                                   f"routes.json gives {real_unrouted}")
    else:
        rec('SKILL-INVENTORY', "SKILL.md no longer carries the 'All N routed engine "
                               "scripts, plus the M tracked-but-never-routed' line "
                               "this check verifies. Re-point the check at the new "
                               "phrasing — an inventory claim nobody checks is how "
                               "the last one went stale by three engines.")

# ── 2. VERSION CROSS-REFERENCE SYNC ─────────────────────────────────────────
CUR = {}
for f, t in TXT.items():
    m = re.search(r'^#\s*(Framework_\w+)\s+v([0-9][0-9.]*)', t, re.M)
    if m:
        CUR[m.group(1)] = m.group(2)
for f, t in TXT.items():
    for m in re.finditer(r'(Framework_\w+)\s+v([0-9][0-9.]*)', t):
        name, ver = m.group(1), m.group(2)
        if name not in CUR or name == f[:-3]:
            continue
        cur = CUR[name]
        if ver != cur:
            # only flag FORWARD refs (claiming a version that doesn't exist yet)
            try:
                newer = tuple(int(x) for x in ver.split('.')) > tuple(int(x) for x in cur.split('.'))
            except ValueError:
                newer = False
            if newer:
                rec('VERSION-XREF', f"{f}: references {name} v{ver} but current is v{cur}")

# ── 2b. RELEASE SYNC: VERSION file vs CHANGELOG top entry (added after the
#        2026.07.31.4 partial deployment, where CHANGELOG.md missed the release
#        entry while VERSION/MANIFEST shipped — no checker caught it) ──────────
try:
    _ver = open('VERSION', encoding='utf-8').read().strip()
    _top = None
    for _l in open('CHANGELOG.md', encoding='utf-8'):
        _m = re.match(r'^## (\S+)', _l)
        if _m: _top = _m.group(1); break
    if _ver and _top and _ver != _top:
        rec('REL-SYNC', f"VERSION is {_ver} but CHANGELOG top entry is {_top} — "
                        f"partial deployment or unrecorded release")
except OSError:
    rec('INFO', 'VERSION or CHANGELOG.md unreadable — release sync not checked')

# ── 3. TRIGGER SYNC: routes.json vs SKILL.md vs specs ───────────────────────
skill = skill_txt
if skill:
    for trig in ROUTES:
        if not re.search(rf'\b{trig}\b', skill):
            rec('TRIGGER-SYNC', f"routes.json trigger '{trig}' not mentioned in SKILL.md")
    for m in re.finditer(r'\b(PYQ[A-Z]\w+|Mock[A-Z]\w+|Test[A-Z]\w+|ScopedBlueprint)\b', skill):
        if m.group(1) not in ROUTES:
            rec('TRIGGER-SYNC', f"SKILL.md names '{m.group(1)}' but routes.json has no such trigger")
else:
    rec('INFO', 'SKILL.md not readable from here — trigger/route parity vs SKILL not checked')

# ── 4. ROUTED FILES EXIST ───────────────────────────────────────────────────
for trig, files in ROUTES.items():
    for fl in files:
        if not os.path.exists(fl):
            rec('ROUTE-MISSING', f"{trig}: routed file {fl} does not exist")

# ── 5. PIPELINE FILENAME CHAIN (Steps 7, 9, 11) ─────────────────────────────
CHAIN = ['_Create.docx', '_Explanation.docx', '_Final.docx']
OWNER = {'_Create.docx': 'Framework_MockTestCreate.md',
         '_Explanation.docx': 'Framework_MockTestExplain.md',
         '_Final.docx': 'Framework_MockDeliver.md'}
for suffix, owner in OWNER.items():
    if suffix not in TXT.get(owner, ''):
        rec('FILENAME-CHAIN', f"{owner} never mentions its output suffix {suffix}")

# ── 6. PATTERN-ERA ARTEFACT SYNC (the new work) ─────────────────────────────
producers = [f for f, t in TXT.items() if "manifest['pattern_eras']" in t or '"pattern_eras"' in t]
consumers = [f for f, t in TXT.items() if "pattern_eras'" in t and f not in producers]
if not producers:
    rec('ERA-SYNC', "no spec writes manifest['pattern_eras']")
for f, t in TXT.items():
    if 'frequency_scope' in t and '--frequency-scope' not in t and f != 'Framework_Blueprint.md':
        rec('ERA-SYNC', f"{f}: uses frequency_scope but declares no --frequency-scope trigger flag")
for f, t in TXT.items():
    if 'OUT_OF_PATTERN' in t and 'bc.OUT_OF_PATTERN' not in t:
        rec('ERA-SYNC', f"{f}: references OUT_OF_PATTERN without sourcing it from the engine")

# ── 7. BLUEPRINT.JSON SCHEMA SYNC (writer §14 vs readers) ───────────────────
bp = TXT.get('Framework_Blueprint.md', '')
declared = set(re.findall(r'^([a-z_][a-z0-9_]*)\s*:\s', bp, re.M))
readers = ['Framework_MockTestCreate.md',
           'Framework_MockTestExplain.md', 'Framework_MockDeliver.md']
KNOWN = {'axis_schedule', 'difficulty_schedule', 'marking_scheme', 'subtopic_allocations',
         'mocks', 'exam_code', 'blueprint_version', 'sections', 'zero_pyq_rotation'}
for r in readers:
    for m in re.finditer(r"\bbp\.get\('([a-z_]+)'|\bbp\['([a-z_]+)'\]", TXT.get(r, '')):
        fld = m.group(1) or m.group(2)
        if fld not in bp:
            rec('BP-SCHEMA', f"{r}: reads blueprint['{fld}'] — not documented in Framework_Blueprint.md")

# ── 8. LAW PROPAGATION REGISTRY (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION, P7) ──
# The deepest cause of that GAP was not the undefined name. It was that a LAW was
# remediated FILE BY FILE from a changelog list, so a path nobody listed kept the
# defect, and a later "content byte-identical" split copied it into a brand-new file.
# Nothing in the repo could answer the question "which specs must carry this law, and
# do they all still carry it?" — so nothing noticed for 20 days.
#
# This check answers it in both directions, and the second direction is the one a
# hand-maintained list can never provide:
#   FORWARD  — every spec listed in 'governs' must still satisfy 'verified_by'.
#   REVERSE  — every spec that PERFORMS the governed operation must be listed. A spec
#              that performs it and is absent is a FAIL, so a new file (or a split
#              half) cannot inherit the law's surface without inheriting its checks.
_REG_WRITER_LIVE = re.compile(
    r'\b(commit_registry|dg_write_verdict|dg_add_rework_snapshot)\(')
_INJ_LIVE = re.compile(
    r'\b(fetch_drive_docx|collect_corpus_files|stage_drive_payload)\(\s*'
    r'[A-Za-z_][A-Za-z0-9_]*\s*[,)]')
# GAP-2026-09-14-REGISTRY-SOURCE. A spec PERFORMS a required registry read when its live
# text either resolves the registry through the one engine resolver, or opens / scans
# the registry file itself (the retired Files-only idiom the law replaces). An OPTIONAL
# read (Step 6 / 6S: `if os.path.exists(reg_path)` on a path bound earlier) is neither.
_REG_REQUIRED_READ_LIVE = re.compile(
    r'\bresolve_registry\('
    r"|open\(\s*f?['\"]/mnt/project/[^'\"]*_registry\.json"
    r"|endswith\(\s*['\"]_registry\.json['\"]\s*\)")


# GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY — three detect rules.
# A spec PERFORMS a presence-flag production when its live text writes the exam-level
# figural_present flag into a blueprint (the derived idiom of Blueprint §6-2 /
# ScopedBlueprint S8-4a) OR uses the RETIRED inheritance idiom — so a new spec that
# copies the retired line inherits the law's checks (MS-22 then fails it).
_PRESENCE_FLAG_LIVE = re.compile(
    r"blueprint\['figural_present'\]\s*=(?!=)"
    r"|'figural_present'\s*:\s*PRESENCE\b"
    r"|exam_config\.get\(\s*['\"]figural_present['\"]")
# A spec performs a MANIFEST-COMMIT operation when it calls the one manifest writer
# (final_assembly.commit_registry) or produces the presence flags.
_MANIFEST_COMMIT_LIVE = re.compile(r"\bfa\.commit_registry\(")
# A spec performs a FIGURE-RECORD write when it records a figure's object_type or
# registers a semantic object.
_FIGURE_RECORD_LIVE = re.compile(
    r"\bvalidate_semantic_object\(|\.object_type\s*=(?!=)|\bscheme_semantic_object\(")

# GAP-2026-11-03 QUALITY-GATE-LAW. A spec performs a QUALITY-GATE operation when its live
# text calls a blueprint_core Cluster QQ entry point or the Step-5 exemplar-bank writer.
_QUALITY_GATE_LIVE = re.compile(
    r"\b(?:quality_readiness|review_packet|bind_review_verdicts|review_verdict_file|"
    r"deliver_allowed|shape_targets|assign_shape_plan|write_exemplar_bank)\(")

# GAP-2026-11-04 STEP-CONTRACT-LAW. A spec performs a STEP-CONTRACT operation when its live
# text decides a final deliverable set or writes a user-waiting end state.
_STEP_CONTRACT_LIVE = re.compile(
    r"\bhandoff_set\(|\[['\"]state['\"]\]\s*=\s*['\"]AWAITING_")


def _live_text(t):
    """Full-line comments blanked. A spec is expected to QUOTE the defect it fixed;
    a commented-out call is documentation, not a call site."""
    return '\n'.join('' if ln.lstrip().startswith('#') else ln
                      for ln in t.split('\n'))


try:
    _REG = json.load(open('LAW_REGISTRY.json', encoding='utf-8'))
except FileNotFoundError:
    _REG = None
    rec('LAW-REGISTRY', "LAW_REGISTRY.json is missing. Every law the framework "
                        "enforces must be machine-checkable; without the registry "
                        "no check can tell whether a law reached every spec it "
                        "governs (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION P7).")
except ValueError as _exc:
    _REG = None
    rec('LAW-REGISTRY', f"LAW_REGISTRY.json is not valid JSON: {_exc}")

# GAP-2026-11-10 LAW-ORG-12 STOP-NEEDS-REPAIR (difficulty path) + LAW-ORG-3 / LAW-ORG-5: Step 7 may never again stop on a
# requested schedule or a difficulty input, and may never again WRITE a retired label basis or ladder ending.
_C7 = TXT.get('Framework_MockTestCreate.md') or ''
_C7L = _live_text(_C7)
for _stop in ('HARD STOP [HS:INPUT] (S3 difficulty feasibility', 'HARD STOP [HS:INPUT] (S3 per-section difficulty plan',
              'HARD STOP [HS:INPUT] (S3 difficulty profile', 'HARD STOP [HS:INPUT] (S3-2D)'):
    if _stop in _C7L:
        rec('STOP-NEEDS-REPAIR', f"Framework_MockTestCreate.md still raises '{_stop} ...' — LAW-ORG-12: a difficulty input "
                                 f"is repaired (bc.schedule_normalize / schedule_place / the exam ruler), never a stop.")
_C7S = _live_text(_C7.split('\n## S13-2L')[-1].split('\n## S13-3 ')[0]) if '\n## S13-2L' in _C7 else ''
for _w in ("bc.dl_set_label_basis(", "'band_swap'", "'paired_upgrade'", "'majority'", "dl_swap_partner(", "dl_upgrade_candidate("):
    if _w in _C7S:
        rec('STOP-NEEDS-REPAIR', f"Create S13-2L live code still uses the retired SC1 ending / writer {_w} — LAW-ORG-3 / "
                                 f"LAW-ORG-5 (SC2: reserve_refill -> refill_session -> last_resort; dl_set_label_basis_strict).")
try:
    import blueprint_core as _bc_org12
    _unrep = [k for k, v in _bc_org12.STOP_REPAIRS.items() if not v[0]]
    if _unrep or not set(v[1] for v in _bc_org12.STOP_REPAIRS.values() if v[1]) <= set(_bc_org12.ENVIRONMENT_FAILURES):
        rec('STOP-NEEDS-REPAIR', f"blueprint_core.STOP_REPAIRS: stop classes without a repair {_unrep} or an environment "
                                 f"failure outside ENVIRONMENT_FAILURES.")
except Exception as _e_org12:                                  # noqa: BLE001
    rec('STOP-NEEDS-REPAIR', f"blueprint_core.STOP_REPAIRS unreadable ({type(_e_org12).__name__}).")

if _REG is not None:
    if not _REG.get('laws'):
        rec('LAW-REGISTRY', "LAW_REGISTRY.json declares no laws — an empty registry "
                            "passes silently and is indistinguishable from no "
                            "enforcement at all.")
    for _law, _meta in sorted((_REG.get('laws') or {}).items()):
        _governs = _meta.get('governs') or []
        _verifiers = _meta.get('verified_by') or []
        if not _verifiers:
            rec('LAW-REGISTRY', f"{_law}: no 'verified_by' — a law with no verifier "
                                f"is a comment, not a check.")
        for _g in _governs:
            if not os.path.exists(_g):
                rec('LAW-REGISTRY', f"{_law}: governs '{_g}', which does not exist. "
                                    f"A stale entry silently shrinks the law's reach.")
        _rule = _meta.get('detect')
        if _rule not in ('live_injection_point_call',
                         'budget_spender_upstream_of_partition',
                         'registry_writer_call',
                         'registry_required_read',
                         'topic_density_gate_call',
                         'presence_flag_producer',
                         'manifest_commit_or_flag_producer',
                         'figure_record_writer',
                         'quality_gate_producer',
                         'step_contract_spec',
                         'chem_structure_rule',
                         'difficulty_layer_rule',
                         'label_basis_rule',
                         'review_coverage_rule',
                         'organic_parity_rule',
                         'nonorganic_fidelity_rule',
                         'batch_verification_rule',
                         'certificate_contract_rule'):
            rec('LAW-REGISTRY', f"{_law}: unknown detect rule "
                                f"{_meta.get('detect')!r}; audit_sync cannot derive "
                                f"the performing set, so the REVERSE direction of "
                                f"this law is unenforced.")
            continue

        # REVERSE — derive the performing set from the corpus, never from the list.
        # The half a hand-maintained 'governs' list can never supply: a NEW spec, or
        # the half of a split file, cannot inherit a law's SURFACE without inheriting
        # its CHECKS. GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION is exactly that shape.
        if _rule == 'budget_spender_upstream_of_partition':
            # GAP-2026-08-16-STEP5-SESSION-EXHAUSTION. A spec performs a SESSION-BUDGET
            # operation when it partitions a context budget in a file that also
            # acquires (so the acquisition is a spender), or when it writes the listing
            # cache the model transcribes. Prose does not count — the corollary law is
            # that anything a CI check must inspect has to live where it can read it.
            _performing = set()
            for _f, _t in TXT.items():
                _live = _live_text(_t)
                if ('partition_by_transport' in _live
                        and any(k in _t for k in ('CHANNEL PROBE', 'probe_drive_channel',
                                                  'probe_direct_egress'))):
                    _performing.add(_f)
                elif 'DRIVE_LISTING_CACHE' in _t and 'search_files' in _t:
                    _performing.add(_f)
        elif _rule == 'topic_density_gate_call':
            # GAP-2026-08-30-TYPE1-HALT-ELIMINATION. A spec performs a
            # GATE-AT-SOURCE operation when its live text calls (or hosts the
            # normative statement of) the single over-aggregation gate,
            # reconcile_taxonomy.check_topic_density. The verifier
            # (audit_specs_ext H-SELFSTOP) then requires the spec's live text
            # to be free of the retired self-stop phrasings that gate replaced.
            _performing = {f for f, t in TXT.items()
                           if 'check_topic_density' in _live_text(t)}
        elif _rule == 'registry_required_read':
            # GAP-2026-09-14-REGISTRY-SOURCE. A spec performs a REGISTRY-SOURCE
            # operation when its live text reads [ExamCode]_registry.json as a
            # REQUIRED input — through pp.resolve_registry, or by the retired direct
            # open / Files-scan idiom. The verifier (mock_sync_audit MS-20) then
            # requires the resolver and forbids the direct idiom.
            _performing = {f for f, t in TXT.items()
                           if _REG_REQUIRED_READ_LIVE.search(_live_text(t))}
        elif _rule == 'presence_flag_producer':
            # GAP-2026-11-01 FIGURE-TYPE-COVERAGE-LAW. A spec that produces the exam-level
            # figural_present flag is a blueprint producer and must run the KIND-COVERAGE
            # pre-flight (verifier: mock_sync_audit MS-23/MS-24).
            _performing = {f for f, t in TXT.items()
                           if _PRESENCE_FLAG_LIVE.search(_live_text(t))}
        elif _rule == 'manifest_commit_or_flag_producer':
            # GAP-2026-11-01 MANIFEST-COMMIT-LAW. The manifest writer's caller and every
            # flag producer (verifier: mock_sync_audit MS-21/MS-22).
            _performing = {f for f, t in TXT.items()
                           if _MANIFEST_COMMIT_LIVE.search(_live_text(t))
                           or _PRESENCE_FLAG_LIVE.search(_live_text(t))}
        elif _rule == 'figure_record_writer':
            # GAP-2026-11-01 FIGURE-RECORD-INTEGRITY-LAW. A spec that records what a figure
            # IS must carry the G-FIGTYPE-KIND gate (verifier: mock_sync_audit MS-25).
            _performing = {f for f, t in TXT.items()
                           if _FIGURE_RECORD_LIVE.search(_live_text(t))}
        elif _rule == 'quality_gate_producer':
            # GAP-2026-11-03 QUALITY-GATE-LAW. Any spec calling a Cluster QQ entry point
            # must be governed (verifier: mock_sync_audit MS-26). Trailing `# ...`
            # comments are cut too: a call name quoted in a comment performs nothing.
            def _qg_live(t):
                out = []
                for ln in _live_text(t).split('\n'):
                    m = re.search(r"(?<![\'\"\w])#", ln)
                    if m and ln[:m.start()].count("'") % 2 == 0 and ln[:m.start()].count('"') % 2 == 0:
                        ln = ln[:m.start()]
                    out.append(ln)
                return '\n'.join(out)
            _performing = {f for f, t in TXT.items() if _QUALITY_GATE_LIVE.search(_qg_live(t))}
        elif _rule == 'step_contract_spec':
            # GAP-2026-11-04 STEP-CONTRACT-LAW (owner decision D6). A spec that decides a
            # step's final deliverable set (pp.handoff_set) or ends a step in a user-waiting
            # AWAITING_* state carries a user contract and must be governed (verifier:
            # mock_sync_audit MS-27 against STEP_CONTRACTS.json).
            _performing = {f for f, t in TXT.items()
                           if _STEP_CONTRACT_LIVE.search(_live_text(t))}
        elif _rule == 'chem_structure_rule':
            # GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS CHEM-STRUCTURE-LAW. A spec
            # performs an RE-25 operation when its live text decides or names the
            # chem_structure_module record, or carries the RE-25 rule line itself.
            _performing = {f for f, t in TXT.items()
                           if 'chem_structure_module' in _live_text(t)
                           or 'RE-25 : CHEM-STRUCTURE STANDARD' in t}
        elif _rule == 'difficulty_layer_rule':
            # GAP-2026-11-07-ORGANIC-DIFFICULTY-RULER DIFFICULTY-LAYER-LAW. A spec performs a
            # difficulty-layer operation when its live text calls one of the five entry points.
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\bbc\.(?:difficulty_band_min|dl_phase3_decision|difficulty_paper_gate|'
                                        r'l2_model_for_scope|pyq_grade_packet)\(', _live_text(t))}
        elif _rule == 'label_basis_rule':
            # GAP-2026-11-08-DR3-QINDEX-CONFLICT LABEL-BASIS-LAW. A spec performs a label-basis operation
            # when its live text calls the ONE label verifier or the ONE basis writer.
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\bbc\.(?:verify_difficulty_label|dl_set_label_basis)\(', _live_text(t))}
        elif _rule == 'review_coverage_rule':
            # GAP-2026-11-08-UNCERTIFIED-DELIVERY REVIEW-COVERAGE-LAW. A spec performs a review-coverage
            # operation when its live text builds a review packet or decides review certification / coverage.
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\bbc\.(?:review_packet|review_item_certified|review_coverage_missing)\(',
                                        _live_text(t))}
        elif _rule == 'organic_parity_rule':
            # GAP-2026-11-10-ORGANIC-QUESTION-PARITY LAW-ORG-1..12. A spec performs an organic-parity /
            # difficulty-integrity operation when its live text calls an S0-OP engine entry point.
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\b(?:bc|_bc_s3)\.(?:dl_set_label_basis_strict|clone_guard|stem_stereo_gate|'
                                        r'schedule_normalize|schedule_place|build_difficulty_ruler|pyq_record_complete|'
                                        r'organic_flag)\(|\bfa\.paper_parity_gate\(', _live_text(t))}
        elif _rule == 'nonorganic_fidelity_rule':
            # GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY LAW-NF-1..11. A spec performs a non-organic fidelity operation
            # when its live text calls a Cluster NF engine entry point (bc. / blueprint_core. prefix).
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\b(?:bc|blueprint_core)\.(?:nested_allocate|subject_matrix_round|nf_targets_per_mock|'
                                        r'subject_band_split|schedule_place_by_subject|band_recipe_check_any|'
                                        r'minimal_identifying_parts|text_clone_guard|nf_series_registry_add|'
                                        r'intra_paper_duplicates|key_leak_check|manifest_hash|manifest_crosswalk|'
                                        r'format_plan_slots|stem_figure_consistency|metal_figure_convention)\(',
                                        _live_text(t))}
        elif _rule == 'batch_verification_rule':
            # GAP-2026-11-11-BATCH-VERIFICATION LAW-BV-1..6. A spec performs a batch-verification operation when its
            # live text calls a Cluster BV entry point (every question measured by fresh graders in its own batch).
            _performing = {f for f, t in TXT.items()
                           if re.search(r'\b(?:bc|blueprint_core)\.(?:bv_apply|bv_set_label|bv_jobs|bv_decide|'
                                        r'bv_batch_status|bv_anchors|bv_author_packet)\(|\b(?:fa|final_assembly)\.bv_batch_step\(', _live_text(t))}
        elif _rule == 'certificate_contract_rule':
            # GAP-2026-11-17-CERT-DISCLOSED-CONTRACT LAW-CERT-1. A spec performs a certificate operation when its live
            # text makes the auditor WRITE (--write-certificate) or READ (--certificate) the S13-2F certificate.
            _performing = {f for f, t in TXT.items()
                           if re.search(r"['\"]--(?:write-)?certificate['\"]", _live_text(t))}
        elif _rule == 'registry_writer_call':
            # GAP-2026-08-26-REGISTRY-HANDOFF-SEAM. A spec performs a REGISTRY-HANDOFF
            # operation when its live text calls one of the three registry writers.
            # The verifier (mock_sync_audit MS-14) then requires it to deliver the
            # registry through pp.handoff_set with the Replace badge.
            _performing = {f for f, t in TXT.items()
                           if _REG_WRITER_LIVE.search(_live_text(t))}
        else:
            _performing = {f for f, t in TXT.items() if _INJ_LIVE.search(_live_text(t))}
        for _f in sorted(_performing - set(_governs)):
            rec('LAW-COVERAGE',
                f"{_f} performs a {_law} operation (it calls a documented injection "
                f"point) but is NOT listed in LAW_REGISTRY.json 'governs'. Add it, "
                f"and make it satisfy {', '.join(_verifiers)}. This is the exact "
                f"shape of GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION: a spec "
                f"inherited a law's SURFACE without inheriting its CHECKS.")

        # FORWARD — every governed spec must still pass its verifiers.
        _cg = {v.split(':')[1] for v in _verifiers if v.startswith('audit_callgraph:')}
        if _cg and os.path.exists('audit_callgraph.py'):
            import subprocess as _sp
            _targets = [g for g in _governs if os.path.exists(g)]
            if _targets:
                _r = _sp.run([sys.executable, 'audit_callgraph.py'] + _targets,
                             capture_output=True, text=True)
                if _r.returncode != 0:
                    for _line in (_r.stdout + _r.stderr).split('\n'):
                        if re.match(r'\s*\[C\d', _line):
                            rec('LAW-VERIFY', f"{_law}: " + _line.strip()[:240])
                    if not any(c == 'LAW-VERIFY' for c in ISSUES):
                        rec('LAW-VERIFY', f"{_law}: audit_callgraph exited "
                                          f"{_r.returncode} on the governed specs.")

# ── 8b. LABEL-VERIFIER / REVIEW-COVERAGE / LADDER-COVERAGE (2026.11.09) ─────────────
# GAP-2026-11-08-DR3-QINDEX-CONFLICT. Release 2026.11.08 shipped two authorities over one field (the DR3
# relabel and A-QINDEX check 8) and a closed stop allow-list, and every gate was green: no check asked
# whether a spec still verified a label with the retired single-basis function, whether a reviewed item was
# bound to the text it reviewed, or whether a FAIL the auditor can emit has ANY repair route. Three checks:
#   LABEL-VERIFIER   — a spec governed by LABEL-BASIS-LAW never calls bc.verify_difficulty_obs( in live text
#                      (the label verifier is bc.verify_difficulty_label — one verifier, a recorded basis).
#   REVIEW-COVERAGE  — a spec governed by REVIEW-COVERAGE-LAW calls bc.review_coverage_missing( and passes
#                      '--item-hashes' to the auditor (the hash is computed, never declared).
#   LADDER-COVERAGE  — every gate id audit_canonical.py can FAIL is routable: it emits item findings, or it
#                      is in blueprint_core LADDER_ENTRY_RUNG / INFRA_GATES / PAPER_GATE_ROUTE. An unrouted
#                      FAIL is exactly the 2026.11.08 stop (bc.sweep_route).
_LAWS_08B = (_REG.get('laws') or {}) if _REG is not None else {}
for _f in (_LAWS_08B.get('LABEL-BASIS-LAW') or {}).get('governs') or []:
    if _f in TXT and re.search(r'\bbc\.verify_difficulty_obs\(', _live_text(TXT[_f])):
        rec('LABEL-VERIFIER', f"{_f}: live text calls bc.verify_difficulty_obs( — a label is verified ONLY by "
                              f"bc.verify_difficulty_label (LABEL-BASIS-LAW); the obs primitive alone cannot see "
                              f"a swap / forced / binding-ruler basis and recreates the 2026.11.08 clash.")
for _f in (_LAWS_08B.get('REVIEW-COVERAGE-LAW') or {}).get('governs') or []:
    if _f in TXT:
        _lv08 = _live_text(TXT[_f])
        if 'bc.review_coverage_missing(' not in _lv08 or "'--item-hashes'" not in _lv08:
            rec('REVIEW-COVERAGE', f"{_f}: governed by REVIEW-COVERAGE-LAW but its live text does not call "
                                   f"bc.review_coverage_missing( AND pass '--item-hashes' — a changed item could be "
                                   f"delivered with no review bound to its final text.")
# BV-COVERAGE (2026.11.11, GAP-2026-11-11-BATCH-VERIFICATION): a spec governed by LAW-BV-1 measures every question
# INSIDE its batch — its live text calls fa.bv_batch_step( (S4-7 STEP A2: fresh jobs, the bv_apply decision of every
# question and the bv_batch_status settlement of the batch) and bc.bv_author_packet( (the author holds the graders'
# anchors before the one write). Without them the first fresh measurement happens at Final
# Assembly — the 29-of-40 rewrite of 2026-11-11.
for _f in (_LAWS_08B.get('LAW-BV-1') or {}).get('governs') or []:
    if _f in TXT:
        _lvbv = _live_text(TXT[_f])
        if 'fa.bv_batch_step(' not in _lvbv or 'bc.bv_author_packet(' not in _lvbv:
            rec('BV-COVERAGE', f"{_f}: governed by LAW-BV-1 but its live text does not call fa.bv_batch_step( AND "
                               f"bc.bv_author_packet( — questions would be measured first at Final Assembly.")
# BC-COVERAGE (2026.11.16, GAP-2026-11-14-BATCH-COMPLETE; LAW-BC-1..9): a spec governed by LAW-BC-1 settles every
# question INSIDE its batch and keeps Final Assembly deterministic. Its live text must (a) run STEP B before STEP A2
# (LAW-BC-6), (b) bind the batch review records (fa.bc_bind_batch(, LAW-BC-7), (c) assemble the final docx by a byte copy
# (fa.assemble_final_docx( and fa.bc_check_bound(, LAW-BC-8), (d) escalate — never repair — an item finding first seen at
# Final Assembly (the S13-2F ESCALATED branch), and (e) keep the normal Final Assembly path (S13-1, S13-2L.0) free of any
# hand-over that starts a sub-agent (GRADE_REQUEST / REVIEW_REQUEST) or any call that writes question text.
def _bc_section(t, sid):
    m = re.search(r'^## ' + re.escape(sid) + r' .*$', t, re.M)
    if not m:
        return ''
    n = re.search(r'^## ', t[m.end():], re.M)
    return t[m.start(): m.end() + (n.start() if n else len(t) - m.end())]
for _f in (_LAWS_08B.get('LAW-BC-1 SETTLED-IN-BATCH') or {}).get('governs') or []:
    if _f not in TXT:
        continue
    _lvbc = _live_text(TXT[_f])
    # sections are cut from the RAW text (a heading is a '#' line, which _live_text blanks), then made live
    _s47 = _live_text(_bc_section(TXT[_f], 'S4-7'))
    _iB, _iA2, _iA3 = _s47.find('  STEP B — GATE CHECK'), _s47.find('  STEP A2 — SETTLE'), _s47.find('  STEP A3 — BIND')
    if not (0 <= _iB < _iA2 < _iA3):
        rec('BC-COVERAGE', f"{_f}: S4-7 must run STEP B, then STEP A2 (SETTLE), then STEP A3 (BIND), in that order "
                           f"(LAW-BC-6 / LAW-BC-7) — found B@{_iB}, A2@{_iA2}, A3@{_iA3}.")
    for _need, _law in (('fa.bc_bind_batch(', 'LAW-BC-7'), ('fa.assemble_final_docx(', 'LAW-BC-8'),
                        ('fa.bc_check_bound(', 'LAW-BC-8'), ('fa.bv_batch_step(', 'LAW-BC-1')):
        if _need not in _lvbc:
            rec('BC-COVERAGE', f"{_f}: live text does not call {_need} ({_law}).")
    _s2f = _live_text(_bc_section(TXT[_f], 'S13-2F'))
    if "'ESCALATED('" not in _s2f or 'bc.BC_RULE' not in _s2f:
        rec('BC-COVERAGE', f"{_f}: S13-2F has no LAW-BC-8 branch (an item finding first seen at Final Assembly must be "
                           f"stamped ESCALATED with a P0 record, never repaired there).")
    for _sid in ('S13-1', 'S13-2L'):
        _sec = _live_text(_bc_section(TXT[_f], _sid))
        if _sid == 'S13-2L':
            _sec = _sec.split('LEGACY (migration only) — the text and the RUN-BLOCK S13-2L below')[0]
        for _bad in ('GRADE_REQUEST', 'REVIEW_REQUEST', 'bv_batch_step(', 'write_q_to_sidecar(', 'slot_chain_next('):
            if _bad in _sec:
                rec('BC-COVERAGE', f"{_f}: the normal Final Assembly section {_sid} contains {_bad!r} — Final Assembly "
                                   f"starts no sub-agent and writes no question text (LAW-BC-8).")
    for _sid in ('S13-1B', 'S13-2G', 'S13-2R'):
        _sec = _bc_section(TXT[_f], _sid)
        if _sec and 'LEGACY (migration only' not in _sec.split('\n', 1)[0]:
            rec('BC-COVERAGE', f"{_f}: {_sid} is legacy under LAW-BC-8 — its heading must say 'LEGACY (migration only'.")
    # FA-TERM (2026.11.25, GAP-2026-11-19-S13-2F-LOOP; LAW-FA-TERM-1). Release 2026.11.24's S13-2F deleted its only
    # sweep counter when it opened slot chains for already-ESCALATED items, so Final Assembly never reached its sweep-6
    # escape and looped forever. The block must (1) use the persistent counter (bc.s13_2f_begin, batch_state['s13_2f'])
    # and the ONE engine decision (bc.s13_2f_plan), naming bc.S13_2F_TOTAL_CAP; (2) never delete or pop the persistent
    # counter anywhere in the spec; (3) leave the BATCH-COMPLETE path (the raise guarded by `if _BC1 or`) BEFORE any
    # slot_chain_reopen / SLOT-CHAIN / LADDER-REPAIR line of the legacy route.
    _s2f_ft = _live_text(_bc_section(TXT[_f], 'S13-2F'))
    for _need in ('bc.s13_2f_begin(', 'bc.s13_2f_plan(', 'bc.S13_2F_TOTAL_CAP', "['s13_2f']"):
        if _need not in _s2f_ft:
            rec('FA-TERM', f"{_f}: S13-2F lacks {_need!r} — the persistent counter / the one engine decision of "
                           f"LAW-FA-TERM-1 (Final Assembly must terminate on every paper).")
    _all_ft = _live_text(TXT[_f])
    for _bad_ft in ("pop('s13_2f'", 'pop("s13_2f"', "['s13_2f'] = {}", "['s13_2f'] = None", "del _bs_0['s13_2f']"):
        if _bad_ft in _all_ft:
            rec('FA-TERM', f"{_f}: {_bad_ft!r} resets the persistent S13-2F counter (LAW-FA-TERM-1).")
    # every auditor call that passes the S13-2F escalations (S13-2F, S13-4c) also passes --escalate-early, so the
    # confirmation sweep reaches the certificate's verdict (an early escalation demoted at S13-2F but FAILed at S13-4c
    # would be a stop on a certified paper)
    for _ln_ft in _all_ft.split('\n'):
        if "'--escalate-paper'" in _ln_ft and "'--escalate-early'" not in _ln_ft:
            rec('FA-TERM', f"{_f}: an auditor call passes --escalate-paper without --escalate-early — S13-4c would FAIL a "
                           f"gate S13-2F escalated early: {_ln_ft.strip()[:120]}")
    _gate_ft = _s2f_ft.find('if _BC1 or ')
    for _late in ('slot_chain_reopen', 'SLOT-CHAIN [HS:LADDER]', 'LADDER-REPAIR [HS:LADDER] (S13-2F sweep'):
        _ix = _s2f_ft.find(_late)
        if _ix != -1 and (_gate_ft == -1 or _ix < _gate_ft):
            rec('FA-TERM', f"{_f}: S13-2F reaches {_late!r} before the BATCH-COMPLETE exit (`if _BC1 or ...: raise "
                           f"DELTA`) — a BATCH-COMPLETE paper must never open a chain or re-author at Final Assembly.")
# CERT-CONTRACT (2026.11.23, GAP-2026-11-17-CERT-DISCLOSED-CONTRACT; LAW-CERT-1). The S13-2F certificate has ONE
# definition (audit_canonical.cert_contract). Release 2026.11.22 shipped a writer (v2.39: disclosed_items; v2.42:
# ESCALATED items in it) whose reader was never updated, and every paper with an ESCALATED item stopped at S13-4c. This
# family makes that drift a build failure: (1) every quality_status prefix written or tested anywhere in the engines /
# specs is in audit_canonical.QUALITY_STATUS_PREFIXES; (2) CERT_OUTCOME covers exactly those prefixes with a known
# outcome; (3) every key of the certificate built in write_item_outputs is read by the contract or listed info-only;
# (4) every prefix names a round-trip self-test (CERT_ROUNDTRIP_TESTS) that exists as a check(...) in the auditor;
# (5) AUDITOR_ID equals the auditor's newest header version; (6) gate_cert and write_item_outputs both call
# cert_contract, and gate_cert reads no certificate field directly except docx_sha256 / amber_notes; (7) the S13-4c
# block of every LAW-CERT-1 spec raises CERT-CONTRACT without a heal, and S13-REGCHECK stages no registry in outputs.
def _cert_contract_family():
    import ast as _ast_cc
    _acp = 'audit_canonical.py'
    if not os.path.exists(_acp):
        rec('CERT-CONTRACT', 'audit_canonical.py missing — the certificate contract cannot be checked.')
        return
    _src = open(_acp, encoding='utf-8').read()
    try:
        _tree = _ast_cc.parse(_src)
    except SyntaxError as _e:
        rec('CERT-CONTRACT', f'audit_canonical.py does not parse ({_e}).')
        return
    _consts, _funcs = {}, {}
    for _n in _tree.body:
        if isinstance(_n, _ast_cc.Assign) and len(_n.targets) == 1 and isinstance(_n.targets[0], _ast_cc.Name):
            try:
                _consts[_n.targets[0].id] = _ast_cc.literal_eval(_n.value)
            except Exception:                                   # noqa: BLE001 — not a literal
                pass
        elif isinstance(_n, _ast_cc.FunctionDef):
            _funcs[_n.name] = _n
    _need = ('QUALITY_STATUS_PREFIXES', 'CERT_OUTCOME', 'CERT_READ_FIELDS', 'CERT_INFO_ONLY', 'AUDITOR_ID',
             'CERT_SCHEMAS', 'CERT_ROUNDTRIP_TESTS')
    _miss = [k for k in _need if k not in _consts]
    if _miss or 'cert_contract' not in _funcs:
        rec('CERT-CONTRACT', f"audit_canonical.py lacks {_miss + ([] if 'cert_contract' in _funcs else ['cert_contract()'])} "
                             f"— LAW-CERT-1 has no single definition.")
        return
    _pref = set(_consts['QUALITY_STATUS_PREFIXES'])
    # (1) every prefix written / tested in the corpus is declared
    _pat_set = re.compile(r"""quality_status['"]?\]?\s*(?:=|:)\s*f?['"]([A-Z][A-Z_]+)""")
    _pat_sw = re.compile(r"""quality_status[^\n]{0,120}?startswith\(\(?\s*((?:f?['"][A-Z][A-Z_]+[('"]*\s*,?\s*)+)""")
    _seen = {}
    for _f in ('blueprint_core.py', 'final_assembly.py', 'audit_canonical.py', 'handshake_audit.py',
               'Framework_MockTestCreate.md', 'Framework_MockDeliver.md', 'Framework_DeliveryFooter.md',
               'Framework_MockTestOrchestrate.md'):
        if not os.path.exists(_f):
            continue
        _t = open(_f, encoding='utf-8').read()
        for _m in _pat_set.finditer(_t):
            _seen.setdefault(_m.group(1), set()).add(_f)
        for _m in _pat_sw.finditer(_t):
            for _x in re.findall(r'[A-Z][A-Z_]+', _m.group(1)):
                _seen.setdefault(_x, set()).add(_f)
    for _x, _fs in sorted(_seen.items()):
        if _x not in _pref:
            rec('CERT-CONTRACT', f"quality_status prefix {_x!r} is written / tested in {sorted(_fs)} but is not in "
                                 f"audit_canonical.QUALITY_STATUS_PREFIXES — declare it with its certificate outcome "
                                 f"(CERT_OUTCOME) and a writer->reader round-trip self-test in the SAME release (LAW-CERT-1).")
    # (2) outcome table
    _out = _consts['CERT_OUTCOME']
    if set(_out) != _pref or not set(_out.values()) <= {'none', 'uncertified', 'disclosed'}:
        rec('CERT-CONTRACT', f"CERT_OUTCOME {_out} must cover exactly QUALITY_STATUS_PREFIXES {sorted(_pref)} with outcomes "
                             f"in none / uncertified / disclosed.")
    # (3) writer keys
    _wk = set()
    for _n in _ast_cc.walk(_funcs.get('write_item_outputs') or _ast_cc.Module(body=[], type_ignores=[])):
        if isinstance(_n, _ast_cc.Assign) and any(isinstance(t, _ast_cc.Name) and t.id == 'cert' for t in _n.targets) \
                and isinstance(_n.value, _ast_cc.Dict):
            _wk |= {k.value for k in _n.value.keys if isinstance(k, _ast_cc.Constant)}
    _known = set(_consts['CERT_READ_FIELDS']) | set(_consts['CERT_INFO_ONLY'])
    if not _wk:
        rec('CERT-CONTRACT', 'write_item_outputs builds no `cert = {...}` literal — the writer cannot be checked.')
    for _k in sorted(_wk - _known):
        rec('CERT-CONTRACT', f"the certificate writer adds key {_k!r}, which cert_contract does not read and "
                             f"CERT_INFO_ONLY does not list — a field written for nobody is how this drift starts.")
    # (4) round-trip self-test per prefix
    _rt = _consts['CERT_ROUNDTRIP_TESTS']
    for _x in sorted(_pref):
        _tid = _rt.get(_x)
        if not _tid or not re.search(r"check\(\s*['\"]" + re.escape(_tid) + r"\b", _src):
            rec('CERT-CONTRACT', f"prefix {_x!r} has no writer->reader round-trip self-test (CERT_ROUNDTRIP_TESTS -> "
                                 f"{_tid!r} not found as a check(...) in audit_canonical.py).")
    # (5) provenance
    _hv = re.search(r'^# (v\d+\.\d+) — ', _src, re.M)
    if not _hv or _consts['AUDITOR_ID'] != 'audit_canonical ' + _hv.group(1):
        rec('CERT-CONTRACT', f"AUDITOR_ID {_consts['AUDITOR_ID']!r} != the newest header version "
                             f"{(_hv.group(1) if _hv else None)!r} — bump them together.")
    # (6) one reader: both ends call cert_contract; gate_cert reads only the sha / amber fields directly
    for _fn in ('gate_cert', 'write_item_outputs'):
        _body = _ast_cc.get_source_segment(_src, _funcs[_fn]) if _fn in _funcs else ''
        if 'cert_contract(' not in (_body or ''):
            rec('CERT-CONTRACT', f"{_fn} does not call cert_contract — LAW-CERT-1: ONE reading of the certificate.")
    _gc = _ast_cc.get_source_segment(_src, _funcs['gate_cert']) if 'gate_cert' in _funcs else ''
    for _fld in re.findall(r"cert\.get\(\s*'([a-z_]+)'", _gc or ''):
        if _fld not in ('docx_sha256', 'amber_notes'):
            rec('CERT-CONTRACT', f"gate_cert reads certificate field {_fld!r} directly — only cert_contract may interpret it.")
    # (7) the spec side
    for _f in (_LAWS_08B.get('LAW-CERT-1 ONE-CERTIFICATE-CONTRACT') or {}).get('governs') or []:
        if _f not in TXT:
            continue
        _s4c = _live_text(_bc_section(TXT[_f], 'S13-4c'))
        if 'certificate contract violated' not in _s4c or 'CERT-CONTRACT' not in _s4c:
            rec('CERT-CONTRACT', f"{_f}: S13-4c has no CERT-CONTRACT branch — a contract FAIL of A-CERT would spend "
                                 f"every heal cycle on a deterministic defect.")
        _rgc = _live_text(_bc_section(TXT[_f], 'S13-REGCHECK'))
        if re.search(r"outputs/\{EXAM\}_registry\.json['\"],\s*'w'", _rgc):
            rec('CERT-CONTRACT', f"{_f}: S13-REGCHECK writes the registry to outputs before S13-4c certified it (C7).")
_cert_contract_family()
# BC-CHECKLIST-SYNC (2026.11.16): the batch reviewer brief asks the MockReview S2-2 checklist fields (C-06) — every field
# of blueprint_core.BC_CHECKLIST_FIELDS is defined in Framework_MockReview.md S2-2 AND asked in BV_BRIEF_REVIEWER, so
# the in-batch review and the legacy S13-2G review can never drift apart.
if os.path.exists('blueprint_core.py') and os.path.exists('Framework_MockReview.md'):
    try:
        sys.path.insert(0, os.path.abspath('.'))
        import importlib as _ilbc
        _bcbc = _ilbc.import_module('blueprint_core')
        _mr = open('Framework_MockReview.md', encoding='utf-8').read()
        _s22 = _bc_section(_mr, 'S2-2')
        for _fld in getattr(_bcbc, 'BC_CHECKLIST_FIELDS', ()):
            if _fld not in _s22:
                rec('BC-CHECKLIST-SYNC', f"checklist field {_fld!r} is not defined in Framework_MockReview.md S2-2.")
            if f"'{_fld}'" not in getattr(_bcbc, 'BV_BRIEF_REVIEWER', '') and f'\"{_fld}\"' not in getattr(_bcbc, 'BV_BRIEF_REVIEWER', ''):
                rec('BC-CHECKLIST-SYNC', f"checklist field {_fld!r} is not asked in blueprint_core.BV_BRIEF_REVIEWER.")
        if not getattr(_bcbc, 'BC_CHECKLIST_FIELDS', ()):
            rec('BC-CHECKLIST-SYNC', 'blueprint_core.BC_CHECKLIST_FIELDS is missing or empty.')
    except Exception as _ebc:                                   # noqa: BLE001
        rec('BC-CHECKLIST-SYNC', f"could not verify the reviewer checklist ({type(_ebc).__name__}: {_ebc}).")
# TEST-NO-HANDWRITE (2026.11.16, GAP F-01): inside handshake_audit.py's H-BC block, grades, key votes and review records
# reach the paper ONLY through result.json files in the job folders fa.bv_batch_step created — a test that writes them
# by hand proves nothing about production (the 2026.11.15 tests did, so Final Assembly's dead end stayed green).
if os.path.exists('handshake_audit.py'):
    _hs = open('handshake_audit.py', encoding='utf-8').read()
    _a_hs, _b_hs = _hs.find('# ── H-BC BEGIN'), _hs.find('# ── H-BC END')
    if not (0 <= _a_hs < _b_hs):
        rec('TEST-NO-HANDWRITE', "handshake_audit.py has no '# ── H-BC BEGIN' ... '# ── H-BC END' block (the BATCH-COMPLETE "
                                 "end-to-end tests).")
    else:
        _blk = _live_text(_hs[_a_hs:_b_hs])
        for _bad, _why in (('op_record_controls(', 'writes grades by hand'),
                           ("['key_votes'] =", 'writes key votes by hand'), ("key_votes={", 'writes key votes by hand'),
                           ("['review'] =", 'writes a review record by hand'), ("['grades'] =", 'writes grades by hand'),
                           ('bc_apply(', 'calls the decision directly instead of through fa.bv_batch_step')):
            if _bad in _blk:
                rec('TEST-NO-HANDWRITE', f"handshake_audit.py H-BC block {_why} ({_bad!r}) — results must reach the paper "
                                         f"only through job folders and returned.txt.")
# STOP-REPAIR-COVERAGE (2026.11.17, GAP-2026-11-14-SPEED-AND-FIDELITY P5): after the first question is written (every
# line from the first '## S4-' heading on) a spec governed by LAW-BC-1 may stop only on a tool fault it names the
# repair for. Every HARD STOP [HS:INFRA] statement in a code block either goes through the self-heal wrapper
# (bc.infra_heal_step / an _infra*( call) or its message names the repair (re-run / restore / rebuild / re-copy /
# refresh / regenerate / repair / fix / re-author / reinstall / replace / re-render / delete / run <this|the|step ...>);
# a HARD STOP [HS:INPUT] after Q1 is forbidden (an exam input is checked before the first question, S3).
_STOP_REPAIR_RE = re.compile(r"(re-?run|\brun (this|the|step|RUN-BLOCK|S\d|it|every|each)|restore|rebuild|re-?copy|refresh|"
                             r"regenerate|repair|\bfix\b|re-?author|reinstall|replace|re-?render|delete)", re.I)


def stop_repair_findings(text, name='spec'):
    """[(line, why)] for every stop after Q1 that names no automatic repair (STOP-REPAIR-COVERAGE). Pure."""
    L = text.split('\n')
    try:
        s4 = next(i for i, l in enumerate(L) if l.startswith('## S4-'))
    except StopIteration:
        return []
    out, incode = [], False
    for i, l in enumerate(L):
        if l.strip().startswith('```'):
            incode = not incode
            continue
        if i < s4 or not incode or 'HARD STOP [HS:' not in l or l.lstrip().startswith('#'):
            continue
        tag = re.search(r'\[HS:(\w+)\]', l).group(1)
        if tag == 'INPUT':
            out.append((i + 1, 'HARD STOP [HS:INPUT] after the first question (inputs are checked in S3)'))
            continue
        if tag != 'INFRA':
            continue
        depth, j, txt = 0, i, ''
        while j < len(L) and j - i <= 16:
            txt += L[j] + '\n'
            depth += L[j].count('(') - L[j].count(')')
            nxt = L[j + 1].strip() if j + 1 < len(L) else ''
            if depth <= 0 and not nxt.startswith(('+', 'f"', '"', "f'", "'")):
                break
            j += 1
        above = '\n'.join(L[max(s4, i - 12):i])
        healed = bool(re.search(r'\b_infra\w*\(', L[i]) or re.search(r'\b_infra\w*\(', L[i - 1] if i else '')
                      or 'infra_heal_step(' in above)
        if not healed and not _STOP_REPAIR_RE.search(txt):
            out.append((i + 1, 'HARD STOP [HS:INFRA] names no repair: ' + ' '.join(txt.split())[:120]))
    return out


for _f in (_LAWS_08B.get('LAW-BC-1 SETTLED-IN-BATCH') or {}).get('governs') or []:
    if _f in TXT:
        for _ln, _why in stop_repair_findings(TXT[_f], _f):
            rec('STOP-REPAIR-COVERAGE', f"{_f}:{_ln}: {_why} — name the automatic repair (or route it through "
                                        f"bc.infra_heal_step).")
# ENGINE-STATUS-SYNC (2026.11.17, GAP-2026-11-14-SPEED-AND-FIDELITY): every status word final_assembly prints on a
# 'STEP A2: <WORD>' / 'STEP A3: <WORD>' line is explained in the spec section the worker acts on (Create S4-7, from
# STEP A2 to STEP C). A status the engine prints but the spec never explains is how 2026.11.16 lost rewrites (C4: a
# REWRITE printed only as JOBS OUT).
_ESS_RE = re.compile(r"""STEP (A[23]): ([A-Z][A-Z]+(?:-[A-Z]+)*(?: OUT)?)""")


def engine_status_findings(engine_text, spec_text):
    """[why] for every printed STEP A2 / A3 status word the Create S4-7 text does not explain. Pure."""
    words = sorted({(st, w) for st, w in _ESS_RE.findall(engine_text)})
    i, j = spec_text.find('  STEP A2 — SETTLE'), spec_text.find('  STEP C — PERSIST')
    region = spec_text[i:j] if 0 <= i < j else ''
    out = []
    if not region:
        return ['Framework_MockTestCreate.md S4-7 has no STEP A2 ... STEP C region']
    for st, w in words:
        if not (f'STEP {st}: {w}' in region or re.search(r'\n\s+' + re.escape(w) + r'\s+(?:q\s+)?->', region)):
            out.append(f"final_assembly prints 'STEP {st}: {w}' but Create S4-7 never explains it")
    return out


if os.path.exists('final_assembly.py') and 'Framework_MockTestCreate.md' in TXT:
    for _w in engine_status_findings(open('final_assembly.py', encoding='utf-8').read(),
                                     TXT['Framework_MockTestCreate.md']):
        rec('ENGINE-STATUS-SYNC', _w + ' — add it to the STEP A2 / A3 instructions.')
if os.path.exists('audit_canonical.py') and os.path.exists('blueprint_core.py'):
    try:
        sys.path.insert(0, os.path.abspath('.'))
        import importlib as _il08
        _bc08 = _il08.import_module('blueprint_core')
        _ac08 = open('audit_canonical.py', encoding='utf-8').read()
        _a08, _b08 = _ac08.find('\ndef self_test():'), _ac08.find('\ndef main():')
        _ac08 = _ac08[:_a08] + _ac08[_b08:] if 0 <= _a08 < _b08 else _ac08
        _fails08 = set(re.findall(r"_fail\(\s*'([A-Za-z0-9\-]+)'", _ac08))
        _items08 = set(re.findall(r"_item\(\s*'([A-Za-z0-9\-]+)'", _ac08))
        _routed08 = (set(getattr(_bc08, 'LADDER_ENTRY_RUNG', {})) | set(getattr(_bc08, 'INFRA_GATES', ()))
                     | set(getattr(_bc08, 'PAPER_GATE_ROUTE', {})) | _items08)
        for _g08 in sorted(_fails08 - _routed08):
            rec('LADDER-COVERAGE', f"audit_canonical.py can FAIL gate {_g08!r} but it has NO route — not an item "
                                   f"gate and not in blueprint_core LADDER_ENTRY_RUNG / INFRA_GATES / PAPER_GATE_ROUTE. "
                                   f"S13-2F would have no lawful repair for it (GAP-2026-11-08-DR3-QINDEX-CONFLICT).")
    except Exception as _e08:                                   # noqa: BLE001
        rec('LADDER-COVERAGE', f"could not verify gate routes ({type(_e08).__name__}: {_e08}) — an unverified "
                               f"route table is the 2026.11.08 defect waiting to recur.")

# ── 9. DOC COUNTS (2026.08.15.7) — no hand-maintained live count survives ────
# WHY. CLAUDE.md's deploy gate carried "39/39 — 23 specs + 16 engines" through six
# releases that changed both halves, and its SPEC_MANIFEST paragraph carried "51 files"
# against an actual 57. Neither was caught by any check; both were corrected by hand,
# one at a time, as reviewers happened to notice them. Correcting the instance and not
# the class is the same failure the LAW-PROPAGATION LAW was added to remove — so the
# class is removed here instead.
#
# TWO CHECKS, and the second is the one that makes it permanent:
#   DOC-COUNT       — the FRAMEWORK COUNTS block must equal the files on disk. The
#                     finding states the CORRECT value, so a drift is a build failure
#                     with the fix already written in the error message.
#   DOC-COUNT-IDIOM — a hand-written live count ANYWHERE ELSE in the document is itself
#                     a failure. You cannot reintroduce the defect by writing more prose.
#
# Historical measurements are deliberately untouched: "0 of 1719 questions", "153/153
# figural" and every CHANGELOG figure are frozen EVIDENCE, not live claims, and the
# idiom check is written to the "currently N <noun>" form precisely so it can never
# fire on them.
_DOC = 'CLAUDE.md'
_COUNT_LINE = re.compile(
    r'^\s*(MANIFEST\.json files|SPEC_MANIFEST\.json entries|routes\.json triggers)'
    r'\s*:\s*([0-9]+)\s*$', re.M)
_LIVE_COUNT_IDIOM = re.compile(r'currently\s+\**([0-9]+)\**\s+'
                               r'(files|entries|specs|engines|triggers|scripts)\b', re.I)

if os.path.exists(_DOC):
    _doc = open(_DOC, encoding='utf-8').read()
    try:
        _truth = {
            'MANIFEST.json files':
                len(json.load(open('MANIFEST.json', encoding='utf-8'))['files']),
            'SPEC_MANIFEST.json entries':
                len(json.load(open('SPEC_MANIFEST.json', encoding='utf-8'))['files']),
            'routes.json triggers': len(ROUTES),
        }
    except (OSError, ValueError, KeyError) as _exc:
        _truth = None
        rec('DOC-COUNT', f"could not read a manifest to verify {_DOC}'s counts: {_exc}")

    if _truth is not None:
        _claimed = {m.group(1): int(m.group(2)) for m in _COUNT_LINE.finditer(_doc)}
        for _label, _actual in sorted(_truth.items()):
            if _label not in _claimed:
                rec('DOC-COUNT',
                    f"{_DOC}: the FRAMEWORK COUNTS block has no '{_label}' line. It must "
                    f"read '{_label} : {_actual}'. A count that is not declared cannot be "
                    f"checked, and an unchecked count is the defect this rule removes.")
            elif _claimed[_label] != _actual:
                rec('DOC-COUNT',
                    f"{_DOC}: FRAMEWORK COUNTS says '{_label} : {_claimed[_label]}' but "
                    f"the files on disk give {_actual}. Correct value: {_actual}.")

    # the block's own lines are the ONLY place a live count may be written
    _block_spans = [m.span() for m in _COUNT_LINE.finditer(_doc)]
    for _m in _LIVE_COUNT_IDIOM.finditer(_doc):
        if any(a <= _m.start() < b for a, b in _block_spans):
            continue
        _ln = _doc[:_m.start()].count('\n') + 1
        rec('DOC-COUNT-IDIOM',
            f"{_DOC}:{_ln}: '{_m.group(0)}' is a hand-maintained live count written in "
            f"prose. Every such number in this file has gone stale at least once. Delete "
            f"it and refer to the FRAMEWORK COUNTS block, which audit_sync keeps true.")

# ── 8c. RPAR-SYNC (release 2026.12.04 — GAP-2026-11-26-RENDER-PARITY, LAW-PRINT-1) ─────────────────
# What the student sees must be what was reviewed, so the four parties that touch a question's text must agree:
# the WRITER (bc.stem_record writes the fields), the PRINTER (Create render_from_record reads them), the REVIEWER
# packet (bc.BV_GRADER_FIELDS carries them) and the CHECK (STEP B writes --item-texts, which STEP A2 / A3 read).
# A drift in any one of them would silently reopen the Q22 defect class.
try:
    _rp_ct = TXT.get('Framework_MockTestCreate.md', '')
    _rp_bc = open('blueprint_core.py', encoding='utf-8').read()
    _rp_need_spec = {
        'render_from_record(': 'the one printer (S10-8A) is not defined',
        "Q.get('stem_lines')": 'render_from_record does not read stem_lines',
        "Q.get('stem_lead')": 'render_from_record does not read stem_lead',
        "Q.get('stem_closing_ask')": 'render_from_record does not read stem_closing_ask',
        "Q.get('stem_lines_position')": 'render_from_record does not read stem_lines_position',
        "Q.get('problem_labels')": 'render_from_record does not read problem_labels',
        'bc.stem_record(': 'S7-QUALITY no longer tells the writer to record a series with bc.stem_record',
        "--item-texts /home/claude/[ExamCode]_M[N]_item_texts.json\n": None,
    }
    for _k, _why in _rp_need_spec.items():
        if _why is None:
            continue
        if _k not in _rp_ct:
            rec('RPAR-SYNC', f"Framework_MockTestCreate.md: {_why} ('{_k}' missing).")
    _rp_stepb = _rp_ct[_rp_ct.find('--item-findings /home/claude/[ExamCode]_M[N]_batch_findings.json'):][:400]
    if '--item-texts' not in _rp_stepb:
        rec('RPAR-SYNC', 'Framework_MockTestCreate.md: the STEP B auditor command no longer writes --item-texts — '
                         'STEP A2 cannot prove the printed block before a reviewer is paid.')
    for _k in ("'stem_lead'", "'stem_lines'", "'stem_closing_ask'", "'stem_lines_position'"):
        if _k not in _rp_bc[_rp_bc.find('def stem_record('):_rp_bc.find('def _rpar_cell_strings(')]:
            rec('RPAR-SYNC', f'blueprint_core.stem_record no longer writes {_k}.')
    _rp_gf = _rp_bc[_rp_bc.find('BV_GRADER_FIELDS = ('):][:700]
    for _k in ("'stem_lines_position'", "'problem_labels'", "'list_columns'"):
        if _k not in _rp_gf:
            rec('RPAR-SYNC', f'blueprint_core.BV_GRADER_FIELDS no longer carries {_k} — the reviewer packet would '
                             f'differ from the printed block.')
except OSError as _exc:
    rec('RPAR-SYNC', f'could not read the files RPAR-SYNC compares: {_exc}')

# ── REPORT ──────────────────────────────────────────────────────────────────
total = sum(len(v) for v in ISSUES.values())
print(f"specs audited: {len(SPECS)} | triggers: {len(ROUTES)} | findings: {total}\n")
for cat in sorted(ISSUES):
    print(f"[{cat}] {len(ISSUES[cat])}")
    for m in sorted(set(ISSUES[cat]))[:12]:
        print("   -", m)
    print()
sys.exit(1 if any(c != 'INFO' for c in ISSUES) else 0)
