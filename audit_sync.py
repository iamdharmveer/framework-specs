"""audit_sync.py — CROSS-STEP SYNCHRONISATION AUDIT.
Does not test behaviour; tests whether the 11 steps AGREE with each other."""
import ast, json, os, re, sys
from collections import defaultdict

SPECS = sorted(f for f in os.listdir('.') if f.startswith('Framework_') and f.endswith('.md'))
TXT = {f: open(f, encoding='utf-8').read() for f in SPECS}
ROUTES = json.load(open('routes.json'))
ISSUES = defaultdict(list)
skill_txt = None
_sp = '/mnt/skills/user/mock-test-framework/SKILL.md'
if os.path.exists(_sp):
    skill_txt = open(_sp, encoding='utf-8').read()
def rec(cat, msg): ISSUES[cat].append(msg)

def blocks(t): return re.findall(r"```python\n(.*?)```", t, re.S)

# ── 1. ENGINE API SYNC: every bc./pp./ee. attribute used must exist ──────────
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
    return names

ALIAS = {'bc': 'blueprint_core', 'pp': 'paper_pipeline', 'ee': 'explain_engine',
         'eg': 'explain_audit_gate'}
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

# ── 1b. SKILL.md claimed inventory vs reality ───────────────────────────────
if skill_txt:
    mspec = re.search(r'The\s+(\d+)\s+framework specs and\s+(\d+)\s+engine scripts', skill_txt)
    if mspec:
        claim_s, claim_e = int(mspec.group(1)), int(mspec.group(2))
        real_s = len(SPECS)
        real_e = len({f for v in ROUTES.values() for f in v if f.endswith('.py')})
        if claim_s != real_s:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_s} specs, corpus has {real_s}")
        if claim_e != real_e:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_e} engine scripts, routes.json routes {real_e}")

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

# ── 5. PIPELINE FILENAME CHAIN (Steps 7-11) ─────────────────────────────────
CHAIN = ['_Create.docx', '_Create_Complete.docx', '_Explanation.docx',
         '_Explanation_Complete.docx', '_Final.docx']
OWNER = {'_Create.docx': 'Framework_MockTestCreate.md',
         '_Create_Complete.docx': 'Framework_MockTestCreateAudit.md',
         '_Explanation.docx': 'Framework_MockTestExplain.md',
         '_Explanation_Complete.docx': 'Framework_MockTestExplainAudit.md',
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
readers = ['Framework_MockTestCreate.md', 'Framework_MockTestCreateAudit.md',
           'Framework_MockTestExplain.md', 'Framework_MockDeliver.md']
KNOWN = {'axis_schedule', 'difficulty_schedule', 'marking_scheme', 'subtopic_allocations',
         'mocks', 'exam_code', 'blueprint_version', 'sections', 'zero_pyq_rotation'}
for r in readers:
    for m in re.finditer(r"\bbp\.get\('([a-z_]+)'|\bbp\['([a-z_]+)'\]", TXT.get(r, '')):
        fld = m.group(1) or m.group(2)
        if fld not in bp:
            rec('BP-SCHEMA', f"{r}: reads blueprint['{fld}'] — not documented in Framework_Blueprint.md")

# ── REPORT ──────────────────────────────────────────────────────────────────
total = sum(len(v) for v in ISSUES.values())
print(f"specs audited: {len(SPECS)} | triggers: {len(ROUTES)} | findings: {total}\n")
for cat in sorted(ISSUES):
    print(f"[{cat}] {len(ISSUES[cat])}")
    for m in sorted(set(ISSUES[cat]))[:12]:
        print("   -", m)
    print()
sys.exit(1 if any(c != 'INFO' for c in ISSUES) else 0)
